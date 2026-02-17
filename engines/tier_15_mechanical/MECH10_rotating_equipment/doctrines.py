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
        topic="electric_motor_nema_frame_sizing",
        keywords=["NEMA", "motor frame", "sizing", "electric motor", "rotating equipment"],
        conclusion_template="Select NEMA frame size based on horsepower, speed, and mounting requirements.",
        reasoning_framework=(
            "NEMA frame sizing is determined by evaluating the motor's horsepower, speed (RPM), and mounting configuration. "
            "Frame size affects shaft height, mounting dimensions, and interchangeability. The selection process involves referencing "
            "the NEMA MG-1 standard tables, ensuring compatibility with driven equipment, and verifying that the frame size supports "
            "the required torque and mechanical loads. Considerations include space constraints, vibration characteristics, and ease "
            "of maintenance. Oversizing frames may lead to unnecessary cost and footprint, while undersizing risks mechanical failure. "
            "The engineer must also ensure that the selected frame allows for proper alignment and coupling with the driven equipment. "
            "Where retrofits are involved, frame size must match existing mounting and shaft dimensions. The process should include "
            "consultation with motor manufacturers and cross-reference with OEM recommendations. Final selection is validated by "
            "reviewing the application environment, such as temperature, humidity, and exposure to corrosive agents."
        ),
        key_factors=[
            "Horsepower rating",
            "Speed (RPM)",
            "Mounting configuration",
            "Shaft height and diameter",
            "NEMA MG-1 standard",
            "Interchangeability",
            "Application environment"
        ],
        primary_authority=["NEMA MG-1", "IEEE 112", "Motor OEM manuals"],
        burden_holder="Design Engineer",
        adversary_position="Frame size selection can be arbitrary; any frame will suffice if horsepower matches.",
        counter_arguments=[
            "Incorrect frame size can cause misalignment, vibration, and premature failure.",
            "Frame dimensions affect coupling and mounting compatibility.",
            "NEMA standards ensure interchangeability and reliability."
        ],
        resolution_strategy="Reference NEMA MG-1 tables and validate against application-specific requirements.",
        entity_scope="Electric motors for industrial rotating equipment",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEMA MG-1 Section 1.05"
    ),
    DoctrineBlock(
        topic="motor_efficiency_classes_ie_standards",
        keywords=["motor efficiency", "IE standards", "IE2", "IE3", "IE4", "energy savings"],
        conclusion_template="Select motor efficiency class based on regulatory requirements and lifecycle cost analysis.",
        reasoning_framework=(
            "Motor efficiency classes (IE2, IE3, IE4) are defined by IEC 60034-30, specifying minimum efficiency levels for induction motors. "
            "Selection involves compliance with regional regulations (e.g., DOE, EU Ecodesign), assessment of energy consumption, and evaluation "
            "of lifecycle costs. Higher efficiency classes reduce operational expenses but increase initial capital cost. The engineer must "
            "consider payback period, utility incentives, and environmental impact. For critical applications, IE3 or IE4 is recommended to "
            "maximize reliability and minimize losses. The selection process includes reviewing motor loading profiles, hours of operation, "
            "and potential for retrofitting existing equipment. Efficiency testing should be performed per IEEE 112 or IEC 60034-2-1. "
            "Final decision is documented with justification based on energy audit and regulatory compliance."
        ),
        key_factors=[
            "Regulatory requirements",
            "Lifecycle cost analysis",
            "Energy consumption",
            "Motor loading profile",
            "Initial capital cost",
            "Payback period"
        ],
        primary_authority=["IEC 60034-30", "DOE regulations", "EU Ecodesign Directive"],
        burden_holder="Plant Engineer",
        adversary_position="Higher efficiency motors are unnecessary for low-duty applications.",
        counter_arguments=[
            "Even low-duty motors contribute to aggregate energy consumption.",
            "Regulatory compliance may mandate minimum efficiency levels.",
            "Long-term savings outweigh initial cost for most applications."
        ],
        resolution_strategy="Perform energy audit and select efficiency class per IEC and regulatory mandates.",
        entity_scope="Industrial electric motors",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEC 60034-30 Table 2"
    ),
    DoctrineBlock(
        topic="motor_service_factor_thermal_margin",
        keywords=["motor service factor", "thermal margin", "overload", "NEMA", "rotating equipment"],
        conclusion_template="Specify motor service factor to provide adequate thermal margin for overload conditions.",
        reasoning_framework=(
            "Motor service factor is defined by NEMA MG-1 as the multiplier of rated horsepower that a motor can safely handle under "
            "specified conditions. The engineer must evaluate the application's load profile, frequency of overloads, ambient temperature, "
            "and cooling method. Service factor above 1.0 provides additional thermal margin, reducing risk of insulation degradation and "
            "premature failure. For applications with frequent overloads, a service factor of 1.15 or higher is recommended. However, "
            "continuous operation above rated load is discouraged. The selection process includes reviewing OEM recommendations, verifying "
            "that the motor's insulation class and cooling system can support the increased load, and documenting the rationale for the "
            "chosen service factor. Consideration must also be given to harmonics, voltage fluctuations, and environmental conditions."
        ),
        key_factors=[
            "Load profile",
            "Frequency of overloads",
            "Ambient temperature",
            "Cooling method",
            "Insulation class",
            "NEMA MG-1"
        ],
        primary_authority=["NEMA MG-1", "IEEE 112", "Motor OEM manuals"],
        burden_holder="System Designer",
        adversary_position="Service factor is irrelevant if motor is sized correctly.",
        counter_arguments=[
            "Unexpected overloads can occur due to process upsets.",
            "Thermal margin improves reliability and reduces maintenance.",
            "NEMA standards require service factor consideration."
        ],
        resolution_strategy="Select service factor based on load profile and environmental conditions; validate per NEMA MG-1.",
        entity_scope="Electric motors in rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEMA MG-1 Section 1.30"
    ),
    DoctrineBlock(
        topic="vfd_harmonics_mitigation",
        keywords=["VFD", "harmonics", "mitigation", "IEEE 519", "rotating equipment"],
        conclusion_template="Implement harmonic mitigation strategies for VFD-driven motors to comply with IEEE 519.",
        reasoning_framework=(
            "Variable Frequency Drives (VFDs) introduce harmonics into the power system, potentially causing overheating, nuisance tripping, "
            "and interference with sensitive equipment. Harmonic mitigation is guided by IEEE 519, which sets limits for total harmonic distortion "
            "at the point of common coupling. The engineer must assess the harmonic profile using simulation or measurement, and select mitigation "
            "methods such as passive filters, active filters, multi-pulse rectifiers, or line reactors. The selection depends on system size, "
            "criticality, and budget. Coordination with power quality specialists is advised. Documentation includes harmonic study results, "
            "chosen mitigation strategy, and compliance verification. For large installations, periodic monitoring is recommended."
        ),
        key_factors=[
            "Harmonic profile",
            "System size",
            "Criticality",
            "Budget",
            "IEEE 519 limits",
            "Mitigation technology"
        ],
        primary_authority=["IEEE 519", "IEC 61000-2-4", "VFD OEM manuals"],
        burden_holder="Electrical Engineer",
        adversary_position="Harmonics are negligible for small VFD installations.",
        counter_arguments=[
            "Even small VFDs can cause local power quality issues.",
            "Sensitive equipment may be affected by harmonics.",
            "Regulatory compliance requires mitigation."
        ],
        resolution_strategy="Perform harmonic analysis and implement mitigation per IEEE 519.",
        entity_scope="VFD-driven rotating equipment",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 519-2014 Section 10.0"
    ),
    DoctrineBlock(
        topic="gear_drive_types_selection",
        keywords=["gear drive", "types", "selection", "spur", "helical", "bevel", "worm", "rotating equipment"],
        conclusion_template="Select gear drive type based on torque, speed, efficiency, and application requirements.",
        reasoning_framework=(
            "Gear drive selection involves evaluating torque transmission, speed reduction, efficiency, noise, and application constraints. "
            "Spur gears are suitable for low-speed, high-torque applications but are noisy. Helical gears offer smoother operation and higher "
            "efficiency. Bevel gears are used for intersecting shafts, while worm gears provide high reduction ratios and self-locking features. "
            "The engineer must assess load characteristics, space availability, maintenance requirements, and lubrication needs. Reference AGMA "
            "standards for gear design and selection. Consideration should be given to backlash, alignment, and vibration. Final selection is "
            "validated by reviewing OEM recommendations and performing stress analysis."
        ),
        key_factors=[
            "Torque transmission",
            "Speed reduction",
            "Efficiency",
            "Noise",
            "Application constraints",
            "AGMA standards"
        ],
        primary_authority=["AGMA 2001", "Gear OEM manuals"],
        burden_holder="Mechanical Engineer",
        adversary_position="Any gear type can be used if torque and speed match.",
        counter_arguments=[
            "Different gear types have distinct operational characteristics.",
            "Noise and efficiency vary significantly.",
            "AGMA standards mandate proper selection."
        ],
        resolution_strategy="Evaluate application requirements and select gear type per AGMA standards.",
        entity_scope="Gear drives in rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AGMA 2001-D04"
    ),
    DoctrineBlock(
        topic="coupling_selection_flexible_vs_rigid",
        keywords=["coupling", "flexible", "rigid", "selection", "misalignment", "rotating equipment"],
        conclusion_template="Choose flexible or rigid coupling based on misalignment tolerance, torque transmission, and application dynamics.",
        reasoning_framework=(
            "Coupling selection is critical for ensuring reliable torque transmission and accommodating misalignment between shafts. Flexible "
            "couplings absorb misalignment, vibration, and shock, making them suitable for applications with dynamic loads or imperfect alignment. "
            "Rigid couplings are used where precise alignment and minimal vibration are required. The engineer must evaluate shaft alignment, "
            "load characteristics, maintenance accessibility, and space constraints. Reference API 671 and OEM guidelines. Consideration should "
            "be given to coupling balance, runout, and operational environment. Final selection is documented with rationale and validated by "
            "reviewing installation and maintenance procedures."
        ),
        key_factors=[
            "Misalignment tolerance",
            "Torque transmission",
            "Application dynamics",
            "Maintenance accessibility",
            "API 671",
            "Coupling balance"
        ],
        primary_authority=["API 671", "Coupling OEM manuals"],
        burden_holder="Mechanical Engineer",
        adversary_position="Flexible couplings are unnecessary if shafts are aligned precisely.",
        counter_arguments=[
            "Perfect alignment is rarely achievable in practice.",
            "Flexible couplings reduce maintenance and downtime.",
            "API standards recommend flexible couplings for most applications."
        ],
        resolution_strategy="Assess alignment and application dynamics; select coupling per API 671.",
        entity_scope="Couplings in rotating equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 671 Section 4.2"
    ),
    DoctrineBlock(
        topic="shaft_alignment_methods_precision",
        keywords=["shaft alignment", "methods", "precision", "laser", "dial indicator", "rotating equipment"],
        conclusion_template="Use precision shaft alignment methods to minimize vibration and maximize equipment life.",
        reasoning_framework=(
            "Precision shaft alignment is essential for reducing vibration, preventing premature bearing and seal failure, and maximizing "
            "equipment reliability. Methods include laser alignment, dial indicator, and reverse indicator techniques. Laser alignment offers "
            "high accuracy and repeatability, while dial indicators are cost-effective but require skilled operators. The engineer must assess "
            "equipment criticality, alignment tolerances, and available tools. Reference API 610 and ISO 1940. Documentation includes alignment "
            "records, tolerance verification, and corrective actions. Periodic re-alignment is recommended for critical equipment."
        ),
        key_factors=[
            "Alignment accuracy",
            "Equipment criticality",
            "Alignment tolerances",
            "Available tools",
            "API 610",
            "ISO 1940"
        ],
        primary_authority=["API 610", "ISO 1940", "Alignment OEM manuals"],
        burden_holder="Maintenance Engineer",
        adversary_position="Manual alignment is sufficient for most applications.",
        counter_arguments=[
            "Manual alignment may not meet precision requirements.",
            "Laser alignment reduces downtime and improves reliability.",
            "API and ISO standards mandate precision alignment."
        ],
        resolution_strategy="Select alignment method based on equipment criticality and tolerance requirements.",
        entity_scope="Shaft alignment in rotating equipment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 7.3"
    ),
    DoctrineBlock(
        topic="mechanical_seal_api_682_plans",
        keywords=["mechanical seal", "API 682", "seal plans", "rotating equipment", "fluid containment"],
        conclusion_template="Select mechanical seal plan per API 682 based on process fluid, pressure, and temperature.",
        reasoning_framework=(
            "Mechanical seal selection and piping plan are governed by API 682, which defines standard seal configurations and auxiliary systems. "
            "The engineer must evaluate process fluid properties, pressure, temperature, and environmental requirements. Seal plan selection involves "
            "choosing between single, double, or tandem seals, and specifying appropriate flush, quench, or barrier systems. Reference API 682 tables "
            "and consult with seal OEMs. Documentation includes seal plan justification, compatibility analysis, and maintenance procedures. "
            "Periodic review of seal performance and auxiliary system integrity is recommended."
        ),
        key_factors=[
            "Process fluid properties",
            "Pressure",
            "Temperature",
            "Environmental requirements",
            "API 682",
            "Seal OEM recommendations"
        ],
        primary_authority=["API 682", "Seal OEM manuals"],
        burden_holder="Mechanical Engineer",
        adversary_position="Any seal plan will suffice if seal is properly installed.",
        counter_arguments=[
            "Incorrect seal plan can cause leakage and environmental incidents.",
            "API 682 ensures reliability and safety.",
            "Seal OEMs provide application-specific recommendations."
        ],
        resolution_strategy="Select seal plan per API 682 and validate against process requirements.",
        entity_scope="Mechanical seals in rotating equipment",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 682 Table 2"
    ),
    DoctrineBlock(
        topic="packing_vs_mechanical_seal_selection",
        keywords=["packing", "mechanical seal", "selection", "fluid containment", "rotating equipment"],
        conclusion_template="Choose between packing and mechanical seal based on leakage tolerance, maintenance, and process fluid characteristics.",
        reasoning_framework=(
            "Packing and mechanical seals are used for fluid containment in rotating equipment. Packing is cost-effective and easy to maintain but "
            "allows controlled leakage. Mechanical seals offer superior containment and reliability but require higher initial investment and "
            "specialized maintenance. The engineer must assess leakage tolerance, process fluid properties, maintenance resources, and environmental "
            "regulations. For hazardous or expensive fluids, mechanical seals are preferred. Reference API 610 and API 682. Documentation includes "
            "selection rationale, maintenance procedures, and compliance verification."
        ),
        key_factors=[
            "Leakage tolerance",
            "Process fluid properties",
            "Maintenance resources",
            "Environmental regulations",
            "API 610",
            "API 682"
        ],
        primary_authority=["API 610", "API 682", "Seal OEM manuals"],
        burden_holder="Process Engineer",
        adversary_position="Packing is sufficient for all applications.",
        counter_arguments=[
            "Packing may not meet environmental or safety requirements.",
            "Mechanical seals reduce downtime and improve reliability.",
            "API standards require mechanical seals for hazardous fluids."
        ],
        resolution_strategy="Evaluate process requirements and select containment method per API standards.",
        entity_scope="Fluid containment in rotating equipment",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 8.1"
    ),
    DoctrineBlock(
        topic="shaft_design_keyway_stress_analysis",
        keywords=["shaft design", "keyway", "stress analysis", "rotating equipment", "failure prevention"],
        conclusion_template="Perform stress analysis on shaft keyways to prevent fatigue and failure.",
        reasoning_framework=(
            "Keyways introduce stress concentrations in shafts, increasing risk of fatigue and failure. The engineer must perform detailed stress "
            "analysis using FEA or analytical methods, referencing AGMA and ASME standards. Consideration includes shaft material, geometry, load "
            "profile, and keyway dimensions. Stress concentration factors are calculated per ASME B17.1. Documentation includes analysis results, "
            "design modifications, and verification against allowable stress limits. Periodic inspection of keyways is recommended for critical "
            "equipment."
        ),
        key_factors=[
            "Shaft material",
            "Geometry",
            "Load profile",
            "Keyway dimensions",
            "Stress concentration factors",
            "AGMA/ASME standards"
        ],
        primary_authority=["AGMA 6001", "ASME B17.1", "FEA software manuals"],
        burden_holder="Design Engineer",
        adversary_position="Keyway stress is negligible for most shaft designs.",
        counter_arguments=[
            "Stress concentrations can cause premature failure.",
            "AGMA and ASME standards mandate analysis.",
            "FEA improves reliability of design."
        ],
        resolution_strategy="Perform stress analysis and validate design per AGMA and ASME standards.",
        entity_scope="Shafts in rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AGMA 6001 Section 5.2"
    ),
    DoctrineBlock(
        topic="torsional_critical_speed_analysis",
        keywords=["torsional", "critical speed", "analysis", "rotating equipment", "resonance"],
        conclusion_template="Conduct torsional critical speed analysis to avoid resonance and equipment failure.",
        reasoning_framework=(
            "Torsional critical speed analysis identifies resonance frequencies in rotating equipment, preventing catastrophic failure. The engineer "
            "must model the shaft system, including couplings, gears, and driven equipment, using analytical or FEA methods. Reference API 684 and "
            "ISO 10494. Analysis includes calculation of natural frequencies, mode shapes, and damping. Operational speed ranges are compared to "
            "critical speeds, and design modifications are made to avoid resonance. Documentation includes analysis results, mitigation strategies, "
            "and periodic review recommendations."
        ),
        key_factors=[
            "Shaft system modeling",
            "Couplings and gears",
            "Natural frequencies",
            "Mode shapes",
            "Damping",
            "API 684",
            "ISO 10494"
        ],
        primary_authority=["API 684", "ISO 10494", "FEA software manuals"],
        burden_holder="Design Engineer",
        adversary_position="Torsional resonance is rare and can be ignored.",
        counter_arguments=[
            "Resonance can cause catastrophic failure.",
            "API and ISO standards require analysis.",
            "FEA improves reliability of prediction."
        ],
        resolution_strategy="Model shaft system and perform analysis per API 684 and ISO 10494.",
        entity_scope="Rotating equipment shaft systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 684 Section 6.1"
    ),
    DoctrineBlock(
        topic="lateral_critical_speed_bearing_stiffness",
        keywords=["lateral critical speed", "bearing stiffness", "rotating equipment", "vibration", "analysis"],
        conclusion_template="Analyze lateral critical speed and bearing stiffness to minimize vibration and ensure reliability.",
        reasoning_framework=(
            "Lateral critical speed analysis evaluates the shaft's response to bending and vibration, considering bearing stiffness and support "
            "geometry. The engineer must model the shaft and bearing system, calculate natural frequencies, and compare operational speeds to "
            "critical speeds. Reference API 610 and ISO 7919. Design modifications are made to shift critical speeds away from operating range. "
            "Documentation includes analysis results, bearing selection rationale, and vibration monitoring recommendations."
        ),
        key_factors=[
            "Shaft and bearing modeling",
            "Natural frequencies",
            "Bearing stiffness",
            "Support geometry",
            "API 610",
            "ISO 7919"
        ],
        primary_authority=["API 610", "ISO 7919", "FEA software manuals"],
        burden_holder="Design Engineer",
        adversary_position="Lateral critical speed is only relevant for high-speed equipment.",
        counter_arguments=[
            "Even moderate-speed equipment can experience vibration issues.",
            "API and ISO standards require analysis.",
            "Proper bearing selection improves reliability."
        ],
        resolution_strategy="Perform lateral critical speed analysis and validate bearing selection per API 610 and ISO 7919.",
        entity_scope="Rotating equipment shaft and bearing systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 6.2"
    ),
    DoctrineBlock(
        topic="api_610_centrifugal_pump_standard",
        keywords=["API 610", "centrifugal pump", "standard", "rotating equipment", "design"],
        conclusion_template="Design and select centrifugal pumps per API 610 standard for reliability and safety.",
        reasoning_framework=(
            "API 610 sets requirements for centrifugal pump design, materials, testing, and documentation for petroleum, chemical, and gas industry "
            "applications. The engineer must evaluate process conditions, material compatibility, and mechanical integrity. Reference API 610 tables "
            "for pump type selection, bearing arrangements, and seal systems. Documentation includes compliance verification, test reports, and "
            "maintenance procedures. Periodic review of pump performance and integrity is recommended."
        ),
        key_factors=[
            "Process conditions",
            "Material compatibility",
            "Mechanical integrity",
            "Pump type selection",
            "API 610",
            "Testing and documentation"
        ],
        primary_authority=["API 610", "Pump OEM manuals"],
        burden_holder="Design Engineer",
        adversary_position="API 610 is only required for critical applications.",
        counter_arguments=[
            "API 610 improves reliability and safety for all applications.",
            "Industry standards mandate compliance.",
            "OEMs design pumps to API 610 requirements."
        ],
        resolution_strategy="Design and select pumps per API 610 and document compliance.",
        entity_scope="Centrifugal pumps in rotating equipment",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 3.1"
    ),
    DoctrineBlock(
        topic="api_617_centrifugal_compressor_standard",
        keywords=["API 617", "centrifugal compressor", "standard", "rotating equipment", "design"],
        conclusion_template="Design and select centrifugal compressors per API 617 standard for reliability and safety.",
        reasoning_framework=(
            "API 617 defines requirements for centrifugal compressor design, materials, testing, and documentation for petroleum, chemical, and gas "
            "industry applications. The engineer must evaluate process conditions, material compatibility, and mechanical integrity. Reference API 617 "
            "tables for compressor type selection, bearing arrangements, and seal systems. Documentation includes compliance verification, test reports, "
            "and maintenance procedures. Periodic review of compressor performance and integrity is recommended."
        ),
        key_factors=[
            "Process conditions",
            "Material compatibility",
            "Mechanical integrity",
            "Compressor type selection",
            "API 617",
            "Testing and documentation"
        ],
        primary_authority=["API 617", "Compressor OEM manuals"],
        burden_holder="Design Engineer",
        adversary_position="API 617 is only required for critical applications.",
        counter_arguments=[
            "API 617 improves reliability and safety for all applications.",
            "Industry standards mandate compliance.",
            "OEMs design compressors to API 617 requirements."
        ],
        resolution_strategy="Design and select compressors per API 617 and document compliance.",
        entity_scope="Centrifugal compressors in rotating equipment",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 617 Section 4.1"
    ),
    DoctrineBlock(
        topic="api_670_machinery_protection_systems",
        keywords=["API 670", "machinery protection", "systems", "rotating equipment", "monitoring"],
        conclusion_template="Implement machinery protection systems per API 670 to monitor and prevent equipment failure.",
        reasoning_framework=(
            "API 670 specifies requirements for machinery protection systems, including vibration monitoring, overspeed detection, and shutdown logic. "
            "The engineer must assess equipment criticality, failure modes, and monitoring requirements. Selection involves choosing appropriate sensors, "
            "logic controllers, and communication interfaces. Reference API 670 and consult with system OEMs. Documentation includes protection system "
            "design, testing procedures, and maintenance protocols. Periodic review and calibration of protection systems are recommended."
        ),
        key_factors=[
            "Equipment criticality",
            "Failure modes",
            "Monitoring requirements",
            "Sensor selection",
            "API 670",
            "Testing and maintenance"
        ],
        primary_authority=["API 670", "System OEM manuals"],
        burden_holder="Reliability Engineer",
        adversary_position="Machinery protection systems are unnecessary for non-critical equipment.",
        counter_arguments=[
            "Even non-critical equipment can cause process upsets.",
            "API 670 improves reliability and safety.",
            "Industry standards mandate protection systems."
        ],
        resolution_strategy="Implement protection systems per API 670 and document compliance.",
        entity_scope="Machinery protection in rotating equipment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 670 Section 5.1"
    ),
    DoctrineBlock(
        topic="vibration_analysis_fault_diagnosis",
        keywords=["vibration analysis", "fault diagnosis", "rotating equipment", "monitoring", "maintenance"],
        conclusion_template="Perform vibration analysis for fault diagnosis and predictive maintenance of rotating equipment.",
        reasoning_framework=(
            "Vibration analysis is a key tool for diagnosing faults in rotating equipment, including imbalance, misalignment, bearing defects, and gear "
            "issues. The engineer must collect vibration data using accelerometers, analyze frequency spectra, and correlate findings with equipment "
            "failure modes. Reference ISO 10816 and API 670. Documentation includes analysis reports, corrective actions, and maintenance recommendations. "
            "Periodic vibration monitoring is recommended for critical equipment."
        ),
        key_factors=[
            "Vibration data collection",
            "Frequency spectra analysis",
            "Failure mode correlation",
            "ISO 10816",
            "API 670",
            "Maintenance recommendations"
        ],
        primary_authority=["ISO 10816", "API 670", "Vibration OEM manuals"],
        burden_holder="Reliability Engineer",
        adversary_position="Vibration analysis is only needed after failure occurs.",
        counter_arguments=[
            "Predictive maintenance reduces downtime and costs.",
            "ISO and API standards mandate periodic vibration analysis.",
            "Early diagnosis prevents catastrophic failure."
        ],
        resolution_strategy="Perform periodic vibration analysis and document findings.",
        entity_scope="Rotating equipment fault diagnosis",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 10816 Section 4.2"
    ),
    DoctrineBlock(
        topic="condition_monitoring_program_development",
        keywords=["condition monitoring", "program development", "rotating equipment", "predictive maintenance"],
        conclusion_template="Develop condition monitoring programs for rotating equipment to enable predictive maintenance.",
        reasoning_framework=(
            "Condition monitoring programs involve systematic collection and analysis of equipment health data, enabling predictive maintenance and "
            "failure prevention. The engineer must define monitoring parameters, select appropriate sensors, and establish data analysis protocols. "
            "Reference ISO 17359 and API 670. Documentation includes program scope, monitoring schedules, and corrective action procedures. Periodic "
            "review and program optimization are recommended."
        ),
        key_factors=[
            "Monitoring parameters",
            "Sensor selection",
            "Data analysis protocols",
            "ISO 17359",
            "API 670",
            "Program optimization"
        ],
        primary_authority=["ISO 17359", "API 670", "Condition Monitoring OEM manuals"],
        burden_holder="Reliability Engineer",
        adversary_position="Condition monitoring is unnecessary for non-critical equipment.",
        counter_arguments=[
            "All equipment benefits from predictive maintenance.",
            "ISO and API standards recommend condition monitoring.",
            "Program optimization improves reliability and reduces costs."
        ],
        resolution_strategy="Develop and optimize condition monitoring programs per ISO 17359 and API 670.",
        entity_scope="Rotating equipment predictive maintenance",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 17359 Section 3.1"
    ),
    DoctrineBlock(
        topic="root_cause_analysis_machinery_failures",
        keywords=["root cause analysis", "machinery failures", "rotating equipment", "failure investigation"],
        conclusion_template="Conduct root cause analysis for machinery failures to prevent recurrence and improve reliability.",
        reasoning_framework=(
            "Root cause analysis (RCA) involves systematic investigation of machinery failures to identify underlying causes and implement corrective "
            "actions. The engineer must collect failure data, interview operators, and analyze maintenance records. Reference ISO 14224 and API 684. "
            "Documentation includes RCA reports, corrective action plans, and follow-up procedures. Periodic review of RCA effectiveness is recommended."
        ),
        key_factors=[
            "Failure data collection",
            "Operator interviews",
            "Maintenance records analysis",
            "ISO 14224",
            "API 684",
            "Corrective action plans"
        ],
        primary_authority=["ISO 14224", "API 684", "RCA manuals"],
        burden_holder="Reliability Engineer",
        adversary_position="Root cause analysis is time-consuming and unnecessary for minor failures.",
        counter_arguments=[
            "Minor failures can indicate systemic issues.",
            "ISO and API standards recommend RCA for all failures.",
            "RCA improves reliability and reduces costs."
        ],
        resolution_strategy="Conduct RCA per ISO 14224 and API 684; document findings and corrective actions.",
        entity_scope="Machinery failure investigation in rotating equipment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14224 Section 7.1"
    ),
    DoctrineBlock(
        topic="spare_parts_strategy_insurance_vs_consumable",
        keywords=["spare parts", "strategy", "insurance", "consumable", "rotating equipment", "inventory"],
        conclusion_template="Develop spare parts strategy distinguishing insurance and consumable parts for rotating equipment.",
        reasoning_framework=(
            "Spare parts strategy involves categorizing parts as insurance (critical, rarely replaced) or consumable (regularly replaced). The engineer "
            "must assess equipment criticality, failure history, and lead times. Insurance parts are stocked for catastrophic failures, while consumables "
            "are managed based on usage rates. Reference ISO 55000 and plant reliability standards. Documentation includes inventory records, stocking "
            "rationale, and periodic review of strategy effectiveness."
        ),
        key_factors=[
            "Equipment criticality",
            "Failure history",
            "Lead times",
            "ISO 55000",
            "Inventory management",
            "Strategy effectiveness"
        ],
        primary_authority=["ISO 55000", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="All spare parts should be treated equally.",
        counter_arguments=[
            "Critical parts require special stocking strategies.",
            "Consumables are managed based on usage rates.",
            "ISO standards recommend differentiated strategies."
        ],
        resolution_strategy="Categorize parts and develop stocking strategy per ISO 55000.",
        entity_scope="Spare parts management for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 55000 Section 4.2"
    ),
    DoctrineBlock(
        topic="motor_enclosure_types_nema_ratings",
        keywords=["motor enclosure", "NEMA ratings", "enclosure types", "rotating equipment", "environmental protection"],
        conclusion_template="Select motor enclosure type based on NEMA ratings and environmental protection requirements.",
        reasoning_framework=(
            "Motor enclosure types are defined by NEMA standards, specifying protection against dust, water, and hazardous environments. The engineer "
            "must assess application environment, exposure to contaminants, and cooling requirements. Common types include Open Drip Proof (ODP), "
            "Totally Enclosed Fan Cooled (TEFC), and Explosion Proof. Reference NEMA MG-1 and IEEE 841. Documentation includes enclosure selection "
            "rationale, environmental assessment, and compliance verification."
        ),
        key_factors=[
            "Application environment",
            "Contaminant exposure",
            "Cooling requirements",
            "NEMA MG-1",
            "IEEE 841",
            "Compliance verification"
        ],
        primary_authority=["NEMA MG-1", "IEEE 841", "Motor OEM manuals"],
        burden_holder="Design Engineer",
        adversary_position="Any enclosure type will suffice if motor is properly maintained.",
        counter_arguments=[
            "Environmental conditions dictate enclosure selection.",
            "NEMA and IEEE standards mandate proper enclosure.",
            "Incorrect enclosure can cause premature failure."
        ],
        resolution_strategy="Select enclosure type per NEMA MG-1 and validate against environmental requirements.",
        entity_scope="Motor enclosures for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEMA MG-1 Section 1.26"
    ),
    DoctrineBlock(
        topic="gearbox_lubrication_oil_vs_grease",
        keywords=["gearbox lubrication", "oil", "grease", "rotating equipment", "maintenance"],
        conclusion_template="Select gearbox lubrication method (oil vs. grease) based on operating conditions and maintenance requirements.",
        reasoning_framework=(
            "Gearbox lubrication is critical for minimizing wear and ensuring reliability. Oil is preferred for high-speed, high-load applications, "
            "while grease is suitable for low-speed, sealed gearboxes. The engineer must assess operating conditions, maintenance accessibility, and "
            "OEM recommendations. Reference AGMA 250.04 and ISO 12925. Documentation includes lubrication selection rationale, maintenance schedules, "
            "and periodic review of lubricant performance."
        ),
        key_factors=[
            "Operating conditions",
            "Maintenance accessibility",
            "OEM recommendations",
            "AGMA 250.04",
            "ISO 12925",
            "Lubricant performance"
        ],
        primary_authority=["AGMA 250.04", "ISO 12925", "Gearbox OEM manuals"],
        burden_holder="Maintenance Engineer",
        adversary_position="Oil and grease are interchangeable for all gearboxes.",
        counter_arguments=[
            "Lubrication method affects reliability and maintenance.",
            "AGMA and ISO standards mandate proper selection.",
            "Incorrect lubricant can cause premature failure."
        ],
        resolution_strategy="Select lubrication method per AGMA and ISO standards; validate against operating conditions.",
        entity_scope="Gearbox lubrication in rotating equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AGMA 250.04 Section 3.1"
    ),
    DoctrineBlock(
        topic="api_611_steam_turbine_applications",
        keywords=["API 611", "steam turbine", "applications", "rotating equipment", "design"],
        conclusion_template="Design and select steam turbines per API 611 standard for reliability and safety.",
        reasoning_framework=(
            "API 611 defines requirements for steam turbine design, materials, testing, and documentation for general-purpose applications. The engineer "
            "must evaluate process conditions, material compatibility, and mechanical integrity. Reference API 611 tables for turbine type selection, "
            "bearing arrangements, and seal systems. Documentation includes compliance verification, test reports, and maintenance procedures. Periodic "
            "review of turbine performance and integrity is recommended."
        ),
        key_factors=[
            "Process conditions",
            "Material compatibility",
            "Mechanical integrity",
            "Turbine type selection",
            "API 611",
            "Testing and documentation"
        ],
        primary_authority=["API 611", "Turbine OEM manuals"],
        burden_holder="Design Engineer",
        adversary_position="API 611 is only required for critical applications.",
        counter_arguments=[
            "API 611 improves reliability and safety for all applications.",
            "Industry standards mandate compliance.",
            "OEMs design turbines to API 611 requirements."
        ],
        resolution_strategy="Design and select turbines per API 611 and document compliance.",
        entity_scope="Steam turbines in rotating equipment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 611 Section 4.1"
    ),
    DoctrineBlock(
        topic="coupling_balance_and_alignment_runout",
        keywords=["coupling balance", "alignment", "runout", "rotating equipment", "reliability"],
        conclusion_template="Ensure coupling balance and alignment runout are within acceptable limits to maximize reliability.",
        reasoning_framework=(
            "Coupling balance and alignment runout are critical for minimizing vibration and maximizing equipment reliability. The engineer must measure "
            "runout using dial indicators or laser tools, compare results to API 671 and ISO 1940 tolerances, and perform corrective actions as needed. "
            "Documentation includes balance and alignment records, tolerance verification, and maintenance procedures. Periodic review of coupling "
            "performance is recommended for critical equipment."
        ),
        key_factors=[
            "Runout measurement",
            "Balance verification",
            "API 671",
            "ISO 1940",
            "Corrective actions",
            "Maintenance procedures"
        ],
        primary_authority=["API 671", "ISO 1940", "Coupling OEM manuals"],
        burden_holder="Maintenance Engineer",
        adversary_position="Runout is only relevant for high-speed couplings.",
        counter_arguments=[
            "Even moderate-speed couplings can experience vibration issues.",
            "API and ISO standards mandate runout verification.",
            "Proper balance improves reliability."
        ],
        resolution_strategy="Measure and correct runout per API 671 and ISO 1940.",
        entity_scope="Coupling balance and alignment in rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 671 Section 5.3"
    ),
    # Additional authoritative doctrine blocks for coverage and depth:
    DoctrineBlock(
        topic="bearing_selection_life_calculation",
        keywords=["bearing selection", "life calculation", "rotating equipment", "reliability"],
        conclusion_template="Select bearings and calculate life expectancy using L10 formula and application-specific factors.",
        reasoning_framework=(
            "Bearing selection and life calculation are governed by ISO 281 and manufacturer guidelines. The engineer must evaluate load, speed, "
            "lubrication, and environmental conditions. The L10 life formula estimates bearing life based on dynamic load rating and applied load. "
            "Consideration includes contamination, misalignment, and shock loads. Documentation includes bearing selection rationale, life calculation, "
            "and maintenance schedules. Periodic review of bearing performance is recommended."
        ),
        key_factors=[
            "Load and speed",
            "Lubrication",
            "Environmental conditions",
            "ISO 281",
            "Manufacturer guidelines",
            "Life calculation"
        ],
        primary_authority=["ISO 281", "Bearing OEM manuals"],
        burden_holder="Design Engineer",
        adversary_position="Any bearing will suffice if size matches.",
        counter_arguments=[
            "Incorrect bearing selection reduces reliability.",
            "ISO standards require life calculation.",
            "Manufacturer guidelines improve selection accuracy."
        ],
        resolution_strategy="Select bearings and calculate life per ISO 281 and OEM guidelines.",
        entity_scope="Bearings in rotating equipment",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 281 Section 4.1"
    ),
    DoctrineBlock(
        topic="lubrication_management_program",
        keywords=["lubrication management", "program", "rotating equipment", "maintenance"],
        conclusion_template="Develop lubrication management program to optimize equipment reliability and minimize wear.",
        reasoning_framework=(
            "Lubrication management programs involve systematic scheduling, monitoring, and analysis of lubricant application. The engineer must "
            "define lubrication intervals, select appropriate lubricants, and establish contamination control procedures. Reference ISO 12925 and "
            "plant reliability standards. Documentation includes program scope, lubricant selection rationale, and periodic review of program "
            "effectiveness."
        ),
        key_factors=[
            "Lubrication intervals",
            "Lubricant selection",
            "Contamination control",
            "ISO 12925",
            "Program effectiveness",
            "Maintenance schedules"
        ],
        primary_authority=["ISO 12925", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Lubrication can be managed reactively.",
        counter_arguments=[
            "Reactive lubrication increases wear and downtime.",
            "ISO standards recommend systematic programs.",
            "Proper lubrication improves reliability."
        ],
        resolution_strategy="Develop and optimize lubrication management program per ISO 12925.",
        entity_scope="Lubrication management for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 12925 Section 3.2"
    ),
    DoctrineBlock(
        topic="equipment_failure_modes_effects_analysis",
        keywords=["failure modes", "effects analysis", "FMEA", "rotating equipment", "reliability"],
        conclusion_template="Conduct FMEA for rotating equipment to identify and mitigate potential failure modes.",
        reasoning_framework=(
            "Failure Modes and Effects Analysis (FMEA) is a systematic approach to identifying potential failure modes and their effects on equipment "
            "reliability. The engineer must assemble a multidisciplinary team, review equipment design and operation, and document failure modes, "
            "causes, and mitigation strategies. Reference ISO 31010 and plant reliability standards. Documentation includes FMEA reports, risk "
            "assessment, and corrective action plans. Periodic review and update of FMEA are recommended."
        ),
        key_factors=[
            "Multidisciplinary team",
            "Equipment design review",
            "Failure mode documentation",
            "ISO 31010",
            "Risk assessment",
            "Corrective actions"
        ],
        primary_authority=["ISO 31010", "Plant reliability standards"],
        burden_holder="Reliability Engineer",
        adversary_position="FMEA is unnecessary for proven equipment designs.",
        counter_arguments=[
            "Even proven designs can fail under unexpected conditions.",
            "ISO standards recommend FMEA for all equipment.",
            "FMEA improves reliability and reduces risk."
        ],
        resolution_strategy="Conduct FMEA per ISO 31010 and document findings.",
        entity_scope="Failure modes analysis for rotating equipment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 31010 Section 5.1"
    ),
    DoctrineBlock(
        topic="equipment_risk_assessment_process",
        keywords=["risk assessment", "process", "rotating equipment", "safety", "reliability"],
        conclusion_template="Perform risk assessment for rotating equipment to prioritize maintenance and safety actions.",
        reasoning_framework=(
            "Risk assessment involves evaluating the likelihood and consequence of equipment failures, prioritizing maintenance and safety actions. "
            "The engineer must review equipment history, failure modes, and operational context. Reference ISO 31000 and plant safety standards. "
            "Documentation includes risk assessment reports, mitigation strategies, and periodic review of risk profiles."
        ),
        key_factors=[
            "Equipment history",
            "Failure modes",
            "Operational context",
            "ISO 31000",
            "Mitigation strategies",
            "Risk profiles"
        ],
        primary_authority=["ISO 31000", "Plant safety standards"],
        burden_holder="Safety Engineer",
        adversary_position="Risk assessment is unnecessary for non-critical equipment.",
        counter_arguments=[
            "All equipment poses some risk.",
            "ISO standards recommend risk assessment.",
            "Prioritization improves safety and reliability."
        ],
        resolution_strategy="Perform risk assessment per ISO 31000 and document findings.",
        entity_scope="Risk assessment for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 31000 Section 6.1"
    ),
    DoctrineBlock(
        topic="equipment_reliability_centered_maintenance",
        keywords=["reliability centered maintenance", "RCM", "rotating equipment", "maintenance strategy"],
        conclusion_template="Implement reliability centered maintenance (RCM) for rotating equipment to optimize maintenance strategy.",
        reasoning_framework=(
            "Reliability Centered Maintenance (RCM) is a systematic approach to optimizing maintenance strategy based on equipment reliability and "
            "failure modes. The engineer must review equipment history, perform FMEA, and develop maintenance schedules. Reference SAE JA1012 and "
            "plant reliability standards. Documentation includes RCM analysis reports, maintenance schedules, and periodic review of strategy "
            "effectiveness."
        ),
        key_factors=[
            "Equipment history",
            "FMEA",
            "Maintenance schedules",
            "SAE JA1012",
            "Strategy effectiveness",
            "Reliability analysis"
        ],
        primary_authority=["SAE JA1012", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="RCM is unnecessary for proven maintenance strategies.",
        counter_arguments=[
            "RCM improves reliability and reduces costs.",
            "SAE standards recommend RCM for all equipment.",
            "Periodic review optimizes maintenance strategy."
        ],
        resolution_strategy="Implement RCM per SAE JA1012 and document findings.",
        entity_scope="RCM for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE JA1012 Section 4.1"
    ),
    DoctrineBlock(
        topic="equipment_life_cycle_cost_analysis",
        keywords=["life cycle cost analysis", "LCCA", "rotating equipment", "cost optimization"],
        conclusion_template="Perform life cycle cost analysis for rotating equipment to optimize selection and maintenance decisions.",
        reasoning_framework=(
            "Life Cycle Cost Analysis (LCCA) evaluates total cost of ownership, including acquisition, operation, maintenance, and disposal. The engineer "
            "must collect cost data, estimate maintenance and energy expenses, and compare alternatives. Reference ISO 15686 and plant cost standards. "
            "Documentation includes LCCA reports, selection rationale, and periodic review of cost optimization strategies."
        ),
        key_factors=[
            "Cost data collection",
            "Maintenance and energy expenses",
            "Alternative comparison",
            "ISO 15686",
            "Cost optimization",
            "Selection rationale"
        ],
        primary_authority=["ISO 15686", "Plant cost standards"],
        burden_holder="Plant Engineer",
        adversary_position="Initial cost is the only relevant factor.",
        counter_arguments=[
            "LCCA improves decision-making and reduces total cost.",
            "ISO standards recommend LCCA for equipment selection.",
            "Periodic review optimizes cost strategies."
        ],
        resolution_strategy="Perform LCCA per ISO 15686 and document findings.",
        entity_scope="Life cycle cost analysis for rotating equipment",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 15686 Section 3.2"
    ),
    DoctrineBlock(
        topic="equipment_energy_efficiency_improvement",
        keywords=["energy efficiency", "improvement", "rotating equipment", "cost savings"],
        conclusion_template="Implement energy efficiency improvement measures for rotating equipment to reduce operational costs.",
        reasoning_framework=(
            "Energy efficiency improvement involves upgrading equipment, optimizing operation, and implementing monitoring systems. The engineer must "
            "review energy consumption, identify inefficiencies, and propose improvement measures. Reference ISO 50001 and plant energy standards. "
            "Documentation includes energy audit reports, improvement plans, and periodic review of energy savings."
        ),
        key_factors=[
            "Energy consumption review",
            "Inefficiency identification",
            "Improvement measures",
            "ISO 50001",
            "Energy audit reports",
            "Savings verification"
        ],
        primary_authority=["ISO 50001", "Plant energy standards"],
        burden_holder="Energy Manager",
        adversary_position="Energy efficiency is only relevant for large equipment.",
        counter_arguments=[
            "All equipment contributes to energy consumption.",
            "ISO standards recommend efficiency improvement.",
            "Periodic review maximizes savings."
        ],
        resolution_strategy="Implement efficiency improvement per ISO 50001 and document findings.",
        entity_scope="Energy efficiency for rotating equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 50001 Section 4.1"
    ),
    DoctrineBlock(
        topic="equipment_upgrade_and_modification_process",
        keywords=["upgrade", "modification", "process", "rotating equipment", "reliability"],
        conclusion_template="Follow structured process for equipment upgrade and modification to ensure reliability and compliance.",
        reasoning_framework=(
            "Equipment upgrade and modification process involves systematic evaluation of upgrade needs, design review, and implementation. The engineer "
            "must assess reliability improvement opportunities, review compliance requirements, and document modification rationale. Reference ISO 9001 "
            "and plant reliability standards. Documentation includes modification reports, compliance verification, and periodic review of upgrade "
            "effectiveness."
        ),
        key_factors=[
            "Upgrade needs assessment",
            "Design review",
            "Compliance requirements",
            "ISO 9001",
            "Modification reports",
            "Upgrade effectiveness"
        ],
        primary_authority=["ISO 9001", "Plant reliability standards"],
        burden_holder="Project Engineer",
        adversary_position="Upgrades can be implemented ad hoc.",
        counter_arguments=[
            "Structured process improves reliability and compliance.",
            "ISO standards recommend systematic upgrades.",
            "Periodic review optimizes upgrade effectiveness."
        ],
        resolution_strategy="Follow structured process per ISO 9001 and document findings.",
        entity_scope="Upgrade and modification for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 8.5"
    ),
    DoctrineBlock(
        topic="equipment_documentation_and_recordkeeping",
        keywords=["documentation", "recordkeeping", "rotating equipment", "compliance"],
        conclusion_template="Maintain comprehensive documentation and recordkeeping for rotating equipment to ensure compliance and reliability.",
        reasoning_framework=(
            "Equipment documentation and recordkeeping involve systematic collection and maintenance of design, operation, and maintenance records. The "
            "engineer must define documentation scope, establish recordkeeping protocols, and ensure compliance with regulatory requirements. Reference "
            "ISO 9001 and plant reliability standards. Documentation includes design records, maintenance logs, and compliance verification reports. "
            "Periodic review and update of documentation are recommended."
        ),
        key_factors=[
            "Documentation scope",
            "Recordkeeping protocols",
            "Regulatory requirements",
            "ISO 9001",
            "Compliance verification",
            "Periodic review"
        ],
        primary_authority=["ISO 9001", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Documentation is only needed for new equipment.",
        counter_arguments=[
            "Documentation improves reliability and compliance.",
            "ISO standards mandate recordkeeping.",
            "Periodic review ensures accuracy."
        ],
        resolution_strategy="Maintain documentation per ISO 9001 and review periodically.",
        entity_scope="Documentation for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 7.5"
    ),
    DoctrineBlock(
        topic="equipment_training_and_skill_development",
        keywords=["training", "skill development", "rotating equipment", "maintenance"],
        conclusion_template="Implement training and skill development programs for personnel handling rotating equipment.",
        reasoning_framework=(
            "Training and skill development programs ensure personnel are competent in operating, maintaining, and troubleshooting rotating equipment. "
            "The engineer must define training scope, develop curriculum, and assess skill gaps. Reference ISO 9001 and plant reliability standards. "
            "Documentation includes training records, skill assessment reports, and periodic review of program effectiveness."
        ),
        key_factors=[
            "Training scope",
            "Curriculum development",
            "Skill gap assessment",
            "ISO 9001",
            "Program effectiveness",
            "Training records"
        ],
        primary_authority=["ISO 9001", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Training is only needed for new hires.",
        counter_arguments=[
            "Ongoing training improves reliability and reduces errors.",
            "ISO standards mandate skill development.",
            "Periodic review optimizes training effectiveness."
        ],
        resolution_strategy="Implement training programs per ISO 9001 and review periodically.",
        entity_scope="Training for rotating equipment personnel",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 7.2"
    ),
    DoctrineBlock(
        topic="equipment_safety_management_systems",
        keywords=["safety management", "systems", "rotating equipment", "compliance"],
        conclusion_template="Implement safety management systems for rotating equipment to ensure compliance and minimize risk.",
        reasoning_framework=(
            "Safety management systems involve systematic identification, assessment, and mitigation of risks associated with rotating equipment. The "
            "engineer must define safety scope, establish protocols, and ensure compliance with regulatory requirements. Reference ISO 45001 and plant "
            "safety standards. Documentation includes safety management plans, risk assessment reports, and periodic review of system effectiveness."
        ),
        key_factors=[
            "Safety scope",
            "Protocol establishment",
            "Regulatory compliance",
            "ISO 45001",
            "System effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 45001", "Plant safety standards"],
        burden_holder="Safety Manager",
        adversary_position="Safety management is only relevant for hazardous equipment.",
        counter_arguments=[
            "All equipment poses some safety risk.",
            "ISO standards mandate safety management.",
            "Periodic review improves safety effectiveness."
        ],
        resolution_strategy="Implement safety management systems per ISO 45001 and review periodically.",
        entity_scope="Safety management for rotating equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 45001 Section 6.1"
    ),
    DoctrineBlock(
        topic="equipment_environmental_compliance_management",
        keywords=["environmental compliance", "management", "rotating equipment", "regulations"],
        conclusion_template="Ensure environmental compliance management for rotating equipment to meet regulatory requirements.",
        reasoning_framework=(
            "Environmental compliance management involves systematic monitoring and control of emissions, waste, and environmental impact from rotating "
            "equipment. The engineer must define compliance scope, establish monitoring protocols, and ensure adherence to regulatory requirements. "
            "Reference ISO 14001 and plant environmental standards. Documentation includes compliance management plans, monitoring reports, and periodic "
            "review of compliance effectiveness."
        ),
        key_factors=[
            "Compliance scope",
            "Monitoring protocols",
            "Regulatory requirements",
            "ISO 14001",
            "Compliance effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 14001", "Plant environmental standards"],
        burden_holder="Environmental Manager",
        adversary_position="Environmental compliance is only relevant for large equipment.",
        counter_arguments=[
            "All equipment contributes to environmental impact.",
            "ISO standards mandate compliance management.",
            "Periodic review improves compliance effectiveness."
        ],
        resolution_strategy="Implement compliance management per ISO 14001 and review periodically.",
        entity_scope="Environmental compliance for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14001 Section 6.1"
    ),
    DoctrineBlock(
        topic="equipment_performance_monitoring_and_reporting",
        keywords=["performance monitoring", "reporting", "rotating equipment", "reliability"],
        conclusion_template="Establish performance monitoring and reporting systems for rotating equipment to optimize reliability.",
        reasoning_framework=(
            "Performance monitoring and reporting systems involve systematic collection and analysis of equipment performance data. The engineer must "
            "define monitoring parameters, establish reporting protocols, and review performance trends. Reference ISO 17359 and plant reliability "
            "standards. Documentation includes performance reports, trend analysis, and periodic review of monitoring effectiveness."
        ),
        key_factors=[
            "Monitoring parameters",
            "Reporting protocols",
            "Performance trends",
            "ISO 17359",
            "Monitoring effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 17359", "Plant reliability standards"],
        burden_holder="Reliability Engineer",
        adversary_position="Performance monitoring is only needed for critical equipment.",
        counter_arguments=[
            "All equipment benefits from performance monitoring.",
            "ISO standards recommend monitoring and reporting.",
            "Periodic review optimizes reliability."
        ],
        resolution_strategy="Establish monitoring and reporting systems per ISO 17359 and review periodically.",
        entity_scope="Performance monitoring for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 17359 Section 4.1"
    ),
    DoctrineBlock(
        topic="equipment_obsolescence_management",
        keywords=["obsolescence management", "rotating equipment", "upgrade", "replacement"],
        conclusion_template="Implement obsolescence management for rotating equipment to ensure reliability and minimize downtime.",
        reasoning_framework=(
            "Obsolescence management involves systematic identification and mitigation of risks associated with obsolete equipment and components. The "
            "engineer must review equipment age, availability of spare parts, and upgrade opportunities. Reference ISO 55000 and plant reliability "
            "standards. Documentation includes obsolescence management plans, upgrade reports, and periodic review of obsolescence risk."
        ),
        key_factors=[
            "Equipment age",
            "Spare parts availability",
            "Upgrade opportunities",
            "ISO 55000",
            "Obsolescence risk",
            "Periodic review"
        ],
        primary_authority=["ISO 55000", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Obsolescence management is only needed for critical equipment.",
        counter_arguments=[
            "All equipment can become obsolete.",
            "ISO standards recommend obsolescence management.",
            "Periodic review minimizes downtime."
        ],
        resolution_strategy="Implement obsolescence management per ISO 55000 and review periodically.",
        entity_scope="Obsolescence management for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 55000 Section 5.1"
    ),
    DoctrineBlock(
        topic="equipment_spare_parts_quality_management",
        keywords=["spare parts quality management", "rotating equipment", "reliability"],
        conclusion_template="Establish spare parts quality management system for rotating equipment to ensure reliability.",
        reasoning_framework=(
            "Spare parts quality management involves systematic evaluation and control of spare parts quality, ensuring compatibility and reliability. "
            "The engineer must define quality criteria, establish inspection protocols, and review supplier performance. Reference ISO 9001 and plant "
            "reliability standards. Documentation includes quality management plans, inspection reports, and periodic review of spare parts quality."
        ),
        key_factors=[
            "Quality criteria",
            "Inspection protocols",
            "Supplier performance",
            "ISO 9001",
            "Quality management plans",
            "Periodic review"
        ],
        primary_authority=["ISO 9001", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Spare parts quality management is only needed for critical parts.",
        counter_arguments=[
            "All spare parts affect reliability.",
            "ISO standards mandate quality management.",
            "Periodic review improves reliability."
        ],
        resolution_strategy="Establish quality management system per ISO 9001 and review periodically.",
        entity_scope="Spare parts quality management for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 8.4"
    ),
    DoctrineBlock(
        topic="equipment_maintenance_planning_and_scheduling",
        keywords=["maintenance planning", "scheduling", "rotating equipment", "reliability"],
        conclusion_template="Develop maintenance planning and scheduling system for rotating equipment to optimize reliability.",
        reasoning_framework=(
            "Maintenance planning and scheduling involve systematic development of maintenance schedules, resource allocation, and performance tracking. "
            "The engineer must define maintenance scope, establish scheduling protocols, and review performance metrics. Reference ISO 55000 and plant "
            "reliability standards. Documentation includes maintenance plans, scheduling reports, and periodic review of planning effectiveness."
        ),
        key_factors=[
            "Maintenance scope",
            "Scheduling protocols",
            "Performance metrics",
            "ISO 55000",
            "Planning effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 55000", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Maintenance planning is only needed for critical equipment.",
        counter_arguments=[
            "All equipment benefits from maintenance planning.",
            "ISO standards recommend planning and scheduling.",
            "Periodic review optimizes reliability."
        ],
        resolution_strategy="Develop planning and scheduling system per ISO 55000 and review periodically.",
        entity_scope="Maintenance planning for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 55000 Section 6.1"
    ),
    DoctrineBlock(
        topic="equipment_failure_reporting_and_analysis",
        keywords=["failure reporting", "analysis", "rotating equipment", "reliability"],
        conclusion_template="Establish failure reporting and analysis system for rotating equipment to improve reliability.",
        reasoning_framework=(
            "Failure reporting and analysis systems involve systematic collection and analysis of equipment failure data. The engineer must define "
            "reporting scope, establish analysis protocols, and review failure trends. Reference ISO 14224 and plant reliability standards. Documentation "
            "includes failure reports, analysis findings, and periodic review of reporting effectiveness."
        ),
        key_factors=[
            "Reporting scope",
            "Analysis protocols",
            "Failure trends",
            "ISO 14224",
            "Reporting effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 14224", "Plant reliability standards"],
        burden_holder="Reliability Engineer",
        adversary_position="Failure reporting is only needed for critical equipment.",
        counter_arguments=[
            "All equipment benefits from failure reporting.",
            "ISO standards recommend reporting and analysis.",
            "Periodic review improves reliability."
        ],
        resolution_strategy="Establish reporting and analysis system per ISO 14224 and review periodically.",
        entity_scope="Failure reporting for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14224 Section 6.1"
    ),
    DoctrineBlock(
        topic="equipment_spare_parts_inventory_optimization",
        keywords=["spare parts inventory optimization", "rotating equipment", "reliability"],
        conclusion_template="Optimize spare parts inventory for rotating equipment to minimize downtime and costs.",
        reasoning_framework=(
            "Spare parts inventory optimization involves systematic review of inventory levels, usage rates, and lead times. The engineer must define "
            "optimization scope, establish inventory protocols, and review performance metrics. Reference ISO 55000 and plant reliability standards. "
            "Documentation includes inventory optimization plans, performance reports, and periodic review of inventory effectiveness."
        ),
        key_factors=[
            "Optimization scope",
            "Inventory protocols",
            "Performance metrics",
            "ISO 55000",
            "Inventory effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 55000", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Inventory optimization is only needed for critical parts.",
        counter_arguments=[
            "All spare parts affect downtime and costs.",
            "ISO standards recommend inventory optimization.",
            "Periodic review improves reliability."
        ],
        resolution_strategy="Optimize inventory per ISO 55000 and review periodically.",
        entity_scope="Inventory optimization for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 55000 Section 7.1"
    ),
    DoctrineBlock(
        topic="equipment_spare_parts_supplier_management",
        keywords=["spare parts supplier management", "rotating equipment", "reliability"],
        conclusion_template="Establish supplier management system for spare parts to ensure reliability and quality.",
        reasoning_framework=(
            "Supplier management system involves systematic evaluation and control of spare parts suppliers, ensuring reliability and quality. The engineer "
            "must define supplier evaluation criteria, establish management protocols, and review supplier performance. Reference ISO 9001 and plant "
            "reliability standards. Documentation includes supplier management plans, evaluation reports, and periodic review of supplier effectiveness."
        ),
        key_factors=[
            "Evaluation criteria",
            "Management protocols",
            "Supplier performance",
            "ISO 9001",
            "Supplier effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 9001", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Supplier management is only needed for critical parts.",
        counter_arguments=[
            "All suppliers affect reliability and quality.",
            "ISO standards mandate supplier management.",
            "Periodic review improves reliability."
        ],
        resolution_strategy="Establish supplier management system per ISO 9001 and review periodically.",
        entity_scope="Supplier management for rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 8.4"
    ),
    DoctrineBlock(
        topic="equipment_spare_parts_standardization",
        keywords=["spare parts standardization", "rotating equipment", "reliability"],
        conclusion_template="Implement spare parts standardization for rotating equipment to improve reliability and reduce costs.",
        reasoning_framework=(
            "Spare parts standardization involves systematic selection of parts based on compatibility and interchangeability, reducing inventory and "
            "improving reliability. The engineer must define standardization scope, establish selection protocols, and review performance metrics. "
            "Reference ISO 9001 and plant reliability standards. Documentation includes standardization plans, selection reports, and periodic review "
            "of standardization effectiveness."
        ),
        key_factors=[
            "Standardization scope",
            "Selection protocols",
            "Performance metrics",
            "ISO 9001",
            "Standardization effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 9001", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Standardization is only needed for critical parts.",
        counter_arguments=[
            "All parts benefit from standardization.",
            "ISO standards recommend standardization.",
            "Periodic review improves reliability."
        ],
        resolution_strategy="Implement standardization per ISO 9001 and review periodically.",
        entity_scope="Standardization for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 8.3"
    ),
    DoctrineBlock(
        topic="equipment_spare_parts_cost_management",
        keywords=["spare parts cost management", "rotating equipment", "reliability"],
        conclusion_template="Establish cost management system for spare parts to optimize reliability and minimize expenses.",
        reasoning_framework=(
            "Cost management system involves systematic review of spare parts costs, budgeting, and expense tracking. The engineer must define cost "
            "management scope, establish budgeting protocols, and review expense trends. Reference ISO 9001 and plant reliability standards. Documentation "
            "includes cost management plans, budgeting reports, and periodic review of cost effectiveness."
        ),
        key_factors=[
            "Cost management scope",
            "Budgeting protocols",
            "Expense trends",
            "ISO 9001",
            "Cost effectiveness",
            "Periodic review"
        ],
        primary_authority=["ISO 9001", "Plant reliability standards"],
        burden_holder="Maintenance Manager",
        adversary_position="Cost management is only needed for critical parts.",
        counter_arguments=[
            "All parts affect expenses and reliability.",
            "ISO standards recommend cost management.",
            "Periodic review improves reliability."
        ],
        resolution_strategy="Establish cost management system per ISO 9001 and review periodically.",
        entity_scope="Cost management for rotating equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 6.2"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    result = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            result.append(doctrine)
    return result

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]