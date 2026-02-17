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
        topic="Triplex vs Duplex Pump Selection",
        keywords=["triplex", "duplex", "pump selection", "mud pump", "OFE01"],
        conclusion_template="Triplex pumps are generally preferred for high-pressure, high-volume mud applications in OFE01 systems, while duplex pumps may be suitable for lower-pressure, lower-volume operations.",
        reasoning_framework=(
            "Evaluate operational requirements including desired flow rate, pressure, and mud properties. "
            "Triplex pumps offer smoother flow, higher efficiency, and reduced pulsation compared to duplex pumps. "
            "Consider maintenance intervals, spare parts availability, and compatibility with existing infrastructure. "
            "Assess cost-benefit ratio, including capital expenditure and lifecycle costs. "
            "Review OEM recommendations and field performance data. "
            "Factor in mud weight, liner wear rates, and hydraulic horsepower requirements. "
            "Analyze historical failure modes and downtime statistics. "
            "Consult regulatory and safety standards for pump selection. "
            "Balance operational flexibility with reliability and maintenance overhead. "
            "Compare Gardner Denver, National Oilwell, and SPM models for suitability. "
            "Document selection rationale and communicate to stakeholders."
        ),
        key_factors=[
            "Required flow rate",
            "Operating pressure",
            "Mud weight",
            "Pulsation characteristics",
            "Maintenance frequency",
            "OEM support",
            "Lifecycle cost"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Technical Manual", "National Oilwell Varco Application Guide"],
        burden_holder="Engineering Team",
        adversary_position="Duplex pumps are more cost-effective and easier to maintain.",
        counter_arguments=[
            "Triplex pumps provide smoother flow and higher efficiency.",
            "Triplex pumps reduce pulsation and liner wear.",
            "Triplex pumps are preferred for high-pressure applications."
        ],
        resolution_strategy="Conduct comparative analysis based on field data and operational requirements; select pump type aligned with safety and performance standards.",
        entity_scope="OFE01 mud pump systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 7K Section 9.3"
    ),
    DoctrineBlock(
        topic="Liner Sizing and Material Selection",
        keywords=["liner sizing", "material selection", "mud pump liner", "OFE01"],
        conclusion_template="Liner size and material should be selected based on required flow rate, mud weight, abrasion resistance, and compatibility with OFE01 pump specifications.",
        reasoning_framework=(
            "Determine desired flow rate and pressure for the mud pump system. "
            "Select liner size to optimize stroke rate and hydraulic horsepower. "
            "Evaluate mud properties, including weight, abrasiveness, and chemical composition. "
            "Choose liner materials (e.g., hardened steel, ceramic, chrome-plated) based on wear resistance and compatibility with mud chemistry. "
            "Review OEM recommendations and field performance data. "
            "Consider cost, availability, and maintenance intervals. "
            "Assess impact of liner size on pump efficiency and pulsation. "
            "Analyze historical liner failure modes and root causes. "
            "Ensure compliance with API and OEM standards. "
            "Document selection rationale and communicate to operations and maintenance teams."
        ),
        key_factors=[
            "Flow rate",
            "Mud weight",
            "Abrasion resistance",
            "Chemical compatibility",
            "Pump stroke rate",
            "OEM recommendations"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Liner Guide", "SPM Mud Pump Handbook"],
        burden_holder="Design Engineer",
        adversary_position="Standard steel liners are sufficient for all mud weights.",
        counter_arguments=[
            "High mud weights and abrasive muds require advanced liner materials.",
            "Ceramic liners offer superior wear resistance.",
            "Chrome-plated liners reduce corrosion and extend service life."
        ],
        resolution_strategy="Select liner size and material based on operational requirements and documented field performance; review with OEM and maintenance teams.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Liner Selection Guide 2019"
    ),
    DoctrineBlock(
        topic="Valve Maintenance and Failure Analysis",
        keywords=["valve maintenance", "failure analysis", "mud pump valve", "OFE01"],
        conclusion_template="Regular valve maintenance and failure analysis are critical to minimizing downtime and preventing catastrophic failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish routine inspection and maintenance schedules for pump valves. "
            "Monitor valve wear, seating, and spring integrity. "
            "Document and analyze valve failures, identifying root causes such as improper seating, material fatigue, or foreign object damage. "
            "Use predictive maintenance tools (e.g., vibration analysis, acoustic monitoring) to detect early signs of valve failure. "
            "Review OEM maintenance guidelines and historical failure data. "
            "Implement corrective actions based on failure analysis, including material upgrades or design changes. "
            "Train maintenance personnel on best practices and failure modes. "
            "Ensure spare parts availability and inventory management. "
            "Communicate findings and recommendations to engineering and operations teams."
        ),
        key_factors=[
            "Inspection frequency",
            "Valve material",
            "Failure history",
            "Predictive maintenance tools",
            "OEM guidelines"
        ],
        primary_authority=["API Spec 7K", "National Oilwell Varco Valve Maintenance Manual", "SPM Failure Analysis Report"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Valve failures are random and cannot be prevented with maintenance.",
        counter_arguments=[
            "Predictive maintenance reduces unplanned downtime.",
            "Root cause analysis enables targeted corrective actions.",
            "OEM guidelines provide proven maintenance intervals."
        ],
        resolution_strategy="Implement structured maintenance and failure analysis program; review outcomes quarterly and adjust practices as needed.",
        entity_scope="OFE01 mud pump valves",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="National Oilwell Varco Valve Maintenance Manual 2020"
    ),
    DoctrineBlock(
        topic="Pulsation Dampener Sizing and Function",
        keywords=["pulsation dampener", "sizing", "function", "mud pump", "OFE01"],
        conclusion_template="Proper sizing and maintenance of pulsation dampeners are essential for reducing pressure fluctuations and protecting downstream equipment in OFE01 mud pump systems.",
        reasoning_framework=(
            "Calculate required dampener volume based on pump displacement, stroke rate, and mud properties. "
            "Select dampener type (e.g., bladder, piston, diaphragm) based on compatibility with mud chemistry and pressure range. "
            "Review OEM sizing charts and field performance data. "
            "Assess impact of dampener sizing on pressure stability and equipment protection. "
            "Monitor dampener performance using pressure sensors and acoustic monitoring. "
            "Implement routine inspection and maintenance schedules. "
            "Document dampener failures and analyze root causes. "
            "Ensure compliance with API and OEM standards. "
            "Communicate sizing rationale and maintenance requirements to operations teams."
        ),
        key_factors=[
            "Pump displacement",
            "Stroke rate",
            "Mud properties",
            "Dampener type",
            "Pressure range",
            "OEM sizing charts"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Pulsation Dampener Guide", "SPM Dampener Sizing Manual"],
        burden_holder="System Designer",
        adversary_position="Standard dampener sizes are adequate for all mud pump systems.",
        counter_arguments=[
            "Improper sizing leads to excessive pressure fluctuations.",
            "Field data supports customized sizing for optimal performance.",
            "OEM charts provide proven sizing methodologies."
        ],
        resolution_strategy="Size dampeners based on operational requirements and field data; implement maintenance program and review performance quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Pulsation Dampener Guide 2018"
    ),
    DoctrineBlock(
        topic="Fluid End Failure Modes and Root Causes",
        keywords=["fluid end", "failure modes", "root causes", "mud pump", "OFE01"],
        conclusion_template="Understanding fluid end failure modes and root causes is vital for developing targeted maintenance strategies and reducing downtime in OFE01 mud pump systems.",
        reasoning_framework=(
            "Identify common fluid end failure modes, including cracking, erosion, corrosion, and fatigue. "
            "Analyze root causes such as improper material selection, excessive pressure, abrasive mud, and inadequate maintenance. "
            "Review historical failure data and OEM reports. "
            "Implement predictive maintenance tools to detect early signs of failure. "
            "Upgrade materials and design based on failure analysis. "
            "Train personnel on recognizing failure symptoms and best practices. "
            "Document all failures and corrective actions. "
            "Communicate findings to engineering and operations teams for continuous improvement."
        ),
        key_factors=[
            "Failure mode identification",
            "Root cause analysis",
            "Material selection",
            "Pressure management",
            "Maintenance practices"
        ],
        primary_authority=["API Spec 7K", "SPM Fluid End Failure Analysis", "Gardner Denver Technical Report"],
        burden_holder="Maintenance Engineer",
        adversary_position="Fluid end failures are unavoidable and random.",
        counter_arguments=[
            "Root cause analysis enables targeted corrective actions.",
            "Material upgrades reduce failure rates.",
            "Predictive maintenance detects early signs of failure."
        ],
        resolution_strategy="Implement structured failure analysis and corrective action program; review outcomes quarterly and adjust practices as needed.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPM Fluid End Failure Analysis 2019"
    ),
    DoctrineBlock(
        topic="Power End Diagnostics - Bearing and Gear Failures",
        keywords=["power end", "diagnostics", "bearing failure", "gear failure", "mud pump", "OFE01"],
        conclusion_template="Routine diagnostics and failure analysis of bearings and gears in the power end are essential for preventing catastrophic failures and optimizing maintenance in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish routine inspection and diagnostic schedules for bearings and gears. "
            "Use vibration analysis, thermography, and oil sampling to detect early signs of failure. "
            "Document and analyze failures, identifying root causes such as lubrication issues, misalignment, overload, and material fatigue. "
            "Review OEM maintenance guidelines and historical failure data. "
            "Implement corrective actions based on failure analysis, including lubrication upgrades, alignment checks, and material improvements. "
            "Train maintenance personnel on diagnostic tools and best practices. "
            "Ensure spare parts availability and inventory management. "
            "Communicate findings and recommendations to engineering and operations teams."
        ),
        key_factors=[
            "Diagnostic tools",
            "Inspection frequency",
            "Lubrication quality",
            "Alignment",
            "Material selection"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Maintenance Manual", "SPM Bearing Failure Analysis"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Bearing and gear failures are random and cannot be prevented.",
        counter_arguments=[
            "Predictive diagnostics reduce unplanned downtime.",
            "Root cause analysis enables targeted corrective actions.",
            "OEM guidelines provide proven maintenance intervals."
        ],
        resolution_strategy="Implement structured diagnostic and failure analysis program; review outcomes quarterly and adjust practices as needed.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Maintenance Manual 2021"
    ),
    DoctrineBlock(
        topic="Stroke Rate Optimization and Hydraulic Horsepower",
        keywords=["stroke rate", "optimization", "hydraulic horsepower", "mud pump", "OFE01"],
        conclusion_template="Optimizing stroke rate and hydraulic horsepower is critical for maximizing mud pump efficiency and minimizing liner and valve wear in OFE01 systems.",
        reasoning_framework=(
            "Calculate required hydraulic horsepower based on mud weight, flow rate, and pressure. "
            "Adjust stroke rate to optimize pump efficiency and reduce wear. "
            "Monitor pump performance using efficiency curves and field data. "
            "Review OEM recommendations and historical performance data. "
            "Assess impact of stroke rate on liner and valve wear. "
            "Implement real-time monitoring and control systems. "
            "Document optimization strategies and communicate to operations teams."
        ),
        key_factors=[
            "Hydraulic horsepower calculation",
            "Stroke rate adjustment",
            "Pump efficiency curves",
            "Wear rates",
            "OEM recommendations"
        ],
        primary_authority=["API Spec 7K", "SPM Pump Efficiency Guide", "Gardner Denver Stroke Rate Optimization Manual"],
        burden_holder="Operations Engineer",
        adversary_position="Fixed stroke rates are adequate for all mud pump operations.",
        counter_arguments=[
            "Optimized stroke rates reduce wear and increase efficiency.",
            "Field data supports real-time stroke rate adjustment.",
            "OEM guidelines provide proven optimization methodologies."
        ],
        resolution_strategy="Optimize stroke rate based on operational requirements and field data; implement real-time monitoring and review performance quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPM Pump Efficiency Guide 2020"
    ),
    DoctrineBlock(
        topic="Pressure Relief System Design and Safety",
        keywords=["pressure relief", "system design", "safety", "mud pump", "OFE01"],
        conclusion_template="Pressure relief systems must be designed and maintained to ensure safe operation and prevent overpressure incidents in OFE01 mud pump systems.",
        reasoning_framework=(
            "Determine required relief valve set points based on maximum allowable working pressure (MAWP) and operational parameters. "
            "Select relief valve type and size based on pump displacement and mud properties. "
            "Review OEM and API standards for relief system design. "
            "Implement routine inspection and maintenance schedules. "
            "Document and analyze relief system failures and incidents. "
            "Train personnel on relief system operation and emergency procedures. "
            "Ensure compliance with regulatory and safety standards. "
            "Communicate design rationale and maintenance requirements to operations teams."
        ),
        key_factors=[
            "MAWP",
            "Relief valve set points",
            "Valve type and size",
            "Inspection frequency",
            "Regulatory standards"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Pressure Relief System Guide", "SPM Safety Manual"],
        burden_holder="System Designer",
        adversary_position="Standard relief valves are adequate for all mud pump systems.",
        counter_arguments=[
            "Improper relief system design can lead to catastrophic failures.",
            "Field data supports customized relief system design.",
            "API standards require specific relief system parameters."
        ],
        resolution_strategy="Design relief systems based on operational requirements and regulatory standards; implement maintenance program and review performance quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API Spec 7K Section 10.2"
    ),
    DoctrineBlock(
        topic="Mud Weight Impact on Pump Performance",
        keywords=["mud weight", "pump performance", "mud pump", "OFE01"],
        conclusion_template="Mud weight significantly impacts pump performance, including flow rate, pressure, and wear rates in OFE01 mud pump systems.",
        reasoning_framework=(
            "Calculate required pump parameters based on mud weight, flow rate, and pressure. "
            "Assess impact of mud weight on pump efficiency, liner and valve wear, and hydraulic horsepower. "
            "Review OEM recommendations and field performance data. "
            "Implement real-time monitoring and control systems. "
            "Document performance impacts and communicate to operations teams."
        ),
        key_factors=[
            "Mud weight",
            "Flow rate",
            "Pressure",
            "Wear rates",
            "Pump efficiency"
        ],
        primary_authority=["API Spec 7K", "SPM Mud Weight Impact Study", "Gardner Denver Pump Performance Guide"],
        burden_holder="Operations Engineer",
        adversary_position="Mud weight has minimal impact on pump performance.",
        counter_arguments=[
            "High mud weights increase wear rates and reduce efficiency.",
            "Field data supports significant performance impacts.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Adjust pump parameters based on mud weight and field data; implement real-time monitoring and review performance quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPM Mud Weight Impact Study 2018"
    ),
    DoctrineBlock(
        topic="Pump Efficiency Curves and Performance Mapping",
        keywords=["pump efficiency", "performance mapping", "mud pump", "OFE01"],
        conclusion_template="Utilizing pump efficiency curves and performance mapping is essential for optimizing mud pump operation and minimizing wear in OFE01 systems.",
        reasoning_framework=(
            "Review OEM efficiency curves and performance maps for mud pumps. "
            "Monitor pump performance using real-time data and field measurements. "
            "Adjust operational parameters to optimize efficiency and reduce wear. "
            "Document performance mapping strategies and communicate to operations teams. "
            "Implement real-time monitoring and control systems. "
            "Review outcomes quarterly and adjust practices as needed."
        ),
        key_factors=[
            "Efficiency curves",
            "Performance mapping",
            "Operational parameters",
            "Wear rates",
            "Real-time monitoring"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Pump Efficiency Guide", "SPM Performance Mapping Manual"],
        burden_holder="Operations Engineer",
        adversary_position="Efficiency curves are theoretical and not applicable to field operations.",
        counter_arguments=[
            "Field data supports use of efficiency curves.",
            "Real-time monitoring enables performance mapping.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Utilize efficiency curves and performance mapping based on field data; implement real-time monitoring and review performance quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Pump Efficiency Guide 2019"
    ),
    DoctrineBlock(
        topic="Gardner Denver vs National Oilwell vs SPM - OEM Comparison",
        keywords=["Gardner Denver", "National Oilwell", "SPM", "OEM comparison", "mud pump", "OFE01"],
        conclusion_template="OEM selection should be based on performance, reliability, support, and compatibility with OFE01 mud pump system requirements.",
        reasoning_framework=(
            "Compare OEMs based on pump performance, reliability, and field data. "
            "Review support services, spare parts availability, and maintenance intervals. "
            "Assess compatibility with existing infrastructure and operational requirements. "
            "Document comparison rationale and communicate to stakeholders. "
            "Review OEM recommendations and field performance data."
        ),
        key_factors=[
            "Performance",
            "Reliability",
            "Support services",
            "Compatibility",
            "Spare parts availability"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver OEM Comparison Report", "SPM OEM Analysis"],
        burden_holder="Procurement Engineer",
        adversary_position="All OEMs provide equivalent performance and reliability.",
        counter_arguments=[
            "Field data supports significant differences in performance and reliability.",
            "OEM support services impact maintenance and downtime.",
            "Compatibility with existing infrastructure is critical."
        ],
        resolution_strategy="Select OEM based on comparative analysis and field data; review outcomes annually and adjust procurement strategies as needed.",
        entity_scope="OFE01 mud pump system",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver OEM Comparison Report 2020"
    ),
    DoctrineBlock(
        topic="Liner Wash Detection and Prevention",
        keywords=["liner wash", "detection", "prevention", "mud pump", "OFE01"],
        conclusion_template="Early detection and prevention of liner wash are critical for reducing downtime and maintenance costs in OFE01 mud pump systems.",
        reasoning_framework=(
            "Implement real-time monitoring tools (e.g., acoustic sensors, vibration analysis) to detect early signs of liner wash. "
            "Establish routine inspection and maintenance schedules. "
            "Review OEM guidelines and field performance data. "
            "Document liner wash incidents and analyze root causes. "
            "Implement corrective actions based on failure analysis, including material upgrades and operational adjustments. "
            "Train personnel on detection tools and best practices. "
            "Ensure spare parts availability and inventory management. "
            "Communicate findings and recommendations to engineering and operations teams."
        ),
        key_factors=[
            "Detection tools",
            "Inspection frequency",
            "Material selection",
            "Operational parameters",
            "OEM guidelines"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Liner Wash Detection Guide", "SPM Failure Analysis Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Liner wash is unavoidable and random.",
        counter_arguments=[
            "Early detection reduces downtime and maintenance costs.",
            "Material upgrades prevent liner wash.",
            "OEM guidelines provide proven detection methodologies."
        ],
        resolution_strategy="Implement structured detection and prevention program; review outcomes quarterly and adjust practices as needed.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Liner Wash Detection Guide 2019"
    ),
    DoctrineBlock(
        topic="Valve Seat Material Selection",
        keywords=["valve seat", "material selection", "mud pump", "OFE01"],
        conclusion_template="Valve seat material should be selected based on mud chemistry, abrasion resistance, and compatibility with OFE01 pump specifications.",
        reasoning_framework=(
            "Evaluate mud properties, including weight, abrasiveness, and chemical composition. "
            "Select valve seat materials (e.g., tungsten carbide, hardened steel, ceramic) based on wear resistance and compatibility. "
            "Review OEM recommendations and field performance data. "
            "Consider cost, availability, and maintenance intervals. "
            "Assess impact of material selection on valve performance and lifespan. "
            "Document selection rationale and communicate to maintenance teams."
        ),
        key_factors=[
            "Mud chemistry",
            "Abrasion resistance",
            "Material compatibility",
            "Valve performance",
            "OEM recommendations"
        ],
        primary_authority=["API Spec 7K", "SPM Valve Seat Material Guide", "Gardner Denver Technical Manual"],
        burden_holder="Design Engineer",
        adversary_position="Standard steel valve seats are sufficient for all mud weights.",
        counter_arguments=[
            "High mud weights and abrasive muds require advanced materials.",
            "Tungsten carbide offers superior wear resistance.",
            "Ceramic seats reduce corrosion and extend service life."
        ],
        resolution_strategy="Select valve seat material based on operational requirements and documented field performance; review with OEM and maintenance teams.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPM Valve Seat Material Guide 2020"
    ),
    DoctrineBlock(
        topic="Fluid End Lubrication Practices",
        keywords=["fluid end", "lubrication", "practices", "mud pump", "OFE01"],
        conclusion_template="Proper lubrication practices are essential for minimizing wear and preventing failures in OFE01 mud pump fluid ends.",
        reasoning_framework=(
            "Establish routine lubrication schedules based on OEM recommendations and field data. "
            "Select appropriate lubricants for mud pump fluid ends. "
            "Monitor lubricant quality and performance using sampling and analysis tools. "
            "Document lubrication practices and failures. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Lubrication schedule",
            "Lubricant selection",
            "Quality monitoring",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Lubrication Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Lubrication is not critical for fluid end performance.",
        counter_arguments=[
            "Proper lubrication reduces wear and prevents failures.",
            "Field data supports structured lubrication practices.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured lubrication program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Lubrication Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Lubrication Practices",
        keywords=["power end", "lubrication", "practices", "mud pump", "OFE01"],
        conclusion_template="Routine lubrication of power end components is critical for preventing bearing and gear failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish routine lubrication schedules based on OEM recommendations and field data. "
            "Select appropriate lubricants for power end bearings and gears. "
            "Monitor lubricant quality and performance using sampling and analysis tools. "
            "Document lubrication practices and failures. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Lubrication schedule",
            "Lubricant selection",
            "Quality monitoring",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Lubrication Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Lubrication is not critical for power end performance.",
        counter_arguments=[
            "Proper lubrication reduces wear and prevents failures.",
            "Field data supports structured lubrication practices.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured lubrication program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Lubrication Guide 2019"
    ),
    DoctrineBlock(
        topic="Valve Spring Selection and Maintenance",
        keywords=["valve spring", "selection", "maintenance", "mud pump", "OFE01"],
        conclusion_template="Valve spring selection and maintenance are critical for ensuring proper valve operation and minimizing failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Select valve springs based on OEM recommendations and mud pump operational parameters. "
            "Monitor spring performance and integrity using inspection tools. "
            "Establish routine maintenance and replacement schedules. "
            "Document spring failures and analyze root causes. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Spring selection",
            "Inspection frequency",
            "Maintenance schedule",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "SPM Valve Spring Guide", "Gardner Denver Technical Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Standard springs are adequate for all mud pump operations.",
        counter_arguments=[
            "Proper spring selection reduces failures.",
            "Routine maintenance prevents unplanned downtime.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Select and maintain valve springs based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPM Valve Spring Guide 2019"
    ),
    DoctrineBlock(
        topic="Fluid End Alignment and Assembly",
        keywords=["fluid end", "alignment", "assembly", "mud pump", "OFE01"],
        conclusion_template="Proper alignment and assembly of fluid end components are essential for minimizing wear and preventing failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish alignment and assembly procedures based on OEM recommendations and field data. "
            "Use precision tools to ensure proper alignment of fluid end components. "
            "Monitor assembly quality using inspection tools. "
            "Document alignment and assembly failures and analyze root causes. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Alignment procedures",
            "Assembly quality",
            "Inspection tools",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Fluid End Assembly Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Alignment and assembly are not critical for fluid end performance.",
        counter_arguments=[
            "Proper alignment reduces wear and prevents failures.",
            "Field data supports structured alignment and assembly procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured alignment and assembly program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Fluid End Assembly Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Alignment and Assembly",
        keywords=["power end", "alignment", "assembly", "mud pump", "OFE01"],
        conclusion_template="Proper alignment and assembly of power end components are essential for preventing bearing and gear failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish alignment and assembly procedures based on OEM recommendations and field data. "
            "Use precision tools to ensure proper alignment of power end components. "
            "Monitor assembly quality using inspection tools. "
            "Document alignment and assembly failures and analyze root causes. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Alignment procedures",
            "Assembly quality",
            "Inspection tools",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Assembly Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Alignment and assembly are not critical for power end performance.",
        counter_arguments=[
            "Proper alignment reduces wear and prevents failures.",
            "Field data supports structured alignment and assembly procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured alignment and assembly program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Assembly Guide 2019"
    ),
    DoctrineBlock(
        topic="Fluid End Pressure Testing",
        keywords=["fluid end", "pressure testing", "mud pump", "OFE01"],
        conclusion_template="Routine pressure testing of fluid end components is critical for ensuring integrity and preventing failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish pressure testing procedures based on OEM recommendations and API standards. "
            "Use calibrated pressure testing equipment to verify fluid end integrity. "
            "Document pressure testing results and failures. "
            "Analyze root causes of pressure testing failures. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Testing procedures",
            "Equipment calibration",
            "Documentation",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Fluid End Pressure Testing Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Pressure testing is not necessary for fluid end integrity.",
        counter_arguments=[
            "Routine pressure testing prevents failures.",
            "Field data supports structured pressure testing procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured pressure testing program based on OEM recommendations and API standards; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Fluid End Pressure Testing Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Vibration Monitoring",
        keywords=["power end", "vibration monitoring", "mud pump", "OFE01"],
        conclusion_template="Routine vibration monitoring of power end components is essential for detecting early signs of bearing and gear failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish vibration monitoring procedures based on OEM recommendations and field data. "
            "Use vibration analysis tools to detect early signs of bearing and gear failures. "
            "Document vibration monitoring results and failures. "
            "Analyze root causes of vibration anomalies. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Monitoring procedures",
            "Analysis tools",
            "Documentation",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Vibration Monitoring Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Vibration monitoring is not necessary for power end integrity.",
        counter_arguments=[
            "Routine vibration monitoring detects early failures.",
            "Field data supports structured vibration monitoring procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured vibration monitoring program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Vibration Monitoring Guide 2019"
    ),
    DoctrineBlock(
        topic="Fluid End Corrosion Prevention",
        keywords=["fluid end", "corrosion prevention", "mud pump", "OFE01"],
        conclusion_template="Corrosion prevention strategies are essential for extending fluid end lifespan and reducing maintenance costs in OFE01 mud pump systems.",
        reasoning_framework=(
            "Evaluate mud chemistry and corrosiveness. "
            "Select corrosion-resistant materials for fluid end components. "
            "Implement corrosion inhibitors and protective coatings. "
            "Monitor corrosion rates using inspection tools. "
            "Document corrosion incidents and analyze root causes. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Mud chemistry",
            "Material selection",
            "Corrosion inhibitors",
            "Protective coatings",
            "Inspection tools"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Corrosion Prevention Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Design Engineer",
        adversary_position="Corrosion prevention is not necessary for fluid end performance.",
        counter_arguments=[
            "Corrosion-resistant materials extend lifespan.",
            "Corrosion inhibitors reduce maintenance costs.",
            "Field data supports structured corrosion prevention strategies."
        ],
        resolution_strategy="Implement corrosion prevention strategies based on mud chemistry and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Corrosion Prevention Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Overload Protection",
        keywords=["power end", "overload protection", "mud pump", "OFE01"],
        conclusion_template="Overload protection strategies are essential for preventing bearing and gear failures in OFE01 mud pump power ends.",
        reasoning_framework=(
            "Establish overload protection procedures based on OEM recommendations and field data. "
            "Implement overload protection devices (e.g., torque limiters, overload relays). "
            "Monitor overload incidents using real-time data. "
            "Document overload incidents and analyze root causes. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Protection devices",
            "Monitoring procedures",
            "Documentation",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Overload Protection Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Overload protection is not necessary for power end performance.",
        counter_arguments=[
            "Overload protection prevents failures.",
            "Field data supports structured overload protection strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement overload protection strategies based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Overload Protection Guide 2019"
    ),
    DoctrineBlock(
        topic="Fluid End Temperature Monitoring",
        keywords=["fluid end", "temperature monitoring", "mud pump", "OFE01"],
        conclusion_template="Routine temperature monitoring of fluid end components is essential for detecting early signs of overheating and preventing failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish temperature monitoring procedures based on OEM recommendations and field data. "
            "Use temperature sensors to detect early signs of overheating. "
            "Document temperature monitoring results and failures. "
            "Analyze root causes of temperature anomalies. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Monitoring procedures",
            "Sensor selection",
            "Documentation",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Fluid End Temperature Monitoring Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Temperature monitoring is not necessary for fluid end integrity.",
        counter_arguments=[
            "Routine temperature monitoring detects early failures.",
            "Field data supports structured temperature monitoring procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured temperature monitoring program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Fluid End Temperature Monitoring Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Temperature Monitoring",
        keywords=["power end", "temperature monitoring", "mud pump", "OFE01"],
        conclusion_template="Routine temperature monitoring of power end components is essential for detecting early signs of overheating and preventing failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish temperature monitoring procedures based on OEM recommendations and field data. "
            "Use temperature sensors to detect early signs of overheating. "
            "Document temperature monitoring results and failures. "
            "Analyze root causes of temperature anomalies. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Monitoring procedures",
            "Sensor selection",
            "Documentation",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Temperature Monitoring Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Temperature monitoring is not necessary for power end integrity.",
        counter_arguments=[
            "Routine temperature monitoring detects early failures.",
            "Field data supports structured temperature monitoring procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured temperature monitoring program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Temperature Monitoring Guide 2019"
    ),
    DoctrineBlock(
        topic="Fluid End Crack Detection and Repair",
        keywords=["fluid end", "crack detection", "repair", "mud pump", "OFE01"],
        conclusion_template="Early detection and repair of fluid end cracks are critical for preventing catastrophic failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Implement crack detection tools (e.g., ultrasonic testing, dye penetrant inspection) based on OEM recommendations and field data. "
            "Establish routine inspection schedules. "
            "Document crack detection results and failures. "
            "Analyze root causes of cracks. "
            "Implement repair procedures based on OEM guidelines. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Detection tools",
            "Inspection frequency",
            "Repair procedures",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Fluid End Crack Detection Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Crack detection and repair are not necessary for fluid end integrity.",
        counter_arguments=[
            "Early crack detection prevents catastrophic failures.",
            "Field data supports structured crack detection and repair procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured crack detection and repair program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Fluid End Crack Detection Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Crack Detection and Repair",
        keywords=["power end", "crack detection", "repair", "mud pump", "OFE01"],
        conclusion_template="Early detection and repair of power end cracks are critical for preventing catastrophic failures in OFE01 mud pump systems.",
        reasoning_framework=(
            "Implement crack detection tools (e.g., ultrasonic testing, dye penetrant inspection) based on OEM recommendations and field data. "
            "Establish routine inspection schedules. "
            "Document crack detection results and failures. "
            "Analyze root causes of cracks. "
            "Implement repair procedures based on OEM guidelines. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Detection tools",
            "Inspection frequency",
            "Repair procedures",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Crack Detection Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Crack detection and repair are not necessary for power end integrity.",
        counter_arguments=[
            "Early crack detection prevents catastrophic failures.",
            "Field data supports structured crack detection and repair procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured crack detection and repair program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Crack Detection Guide 2019"
    ),
    DoctrineBlock(
        topic="Fluid End Replacement Strategies",
        keywords=["fluid end", "replacement", "strategies", "mud pump", "OFE01"],
        conclusion_template="Structured fluid end replacement strategies are essential for minimizing downtime and maintenance costs in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish replacement strategies based on OEM recommendations, field data, and failure analysis. "
            "Monitor fluid end performance using real-time data and inspection tools. "
            "Document replacement intervals and failures. "
            "Analyze root causes of fluid end failures. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Replacement intervals",
            "Performance monitoring",
            "Failure analysis",
            "OEM recommendations",
            "Cost analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Fluid End Replacement Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Fluid end replacement is random and cannot be structured.",
        counter_arguments=[
            "Structured replacement reduces downtime and maintenance costs.",
            "Field data supports replacement strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured replacement strategies based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Fluid End Replacement Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Replacement Strategies",
        keywords=["power end", "replacement", "strategies", "mud pump", "OFE01"],
        conclusion_template="Structured power end replacement strategies are essential for minimizing downtime and maintenance costs in OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish replacement strategies based on OEM recommendations, field data, and failure analysis. "
            "Monitor power end performance using real-time data and inspection tools. "
            "Document replacement intervals and failures. "
            "Analyze root causes of power end failures. "
            "Train personnel on best practices and failure modes. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Replacement intervals",
            "Performance monitoring",
            "Failure analysis",
            "OEM recommendations",
            "Cost analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Power End Replacement Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Power end replacement is random and cannot be structured.",
        counter_arguments=[
            "Structured replacement reduces downtime and maintenance costs.",
            "Field data supports replacement strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured replacement strategies based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Power End Replacement Guide 2019"
    ),
    DoctrineBlock(
        topic="Fluid End Spare Parts Inventory Management",
        keywords=["fluid end", "spare parts", "inventory management", "mud pump", "OFE01"],
        conclusion_template="Effective spare parts inventory management is essential for minimizing downtime and ensuring availability of critical components in OFE01 mud pump fluid ends.",
        reasoning_framework=(
            "Establish inventory management procedures based on OEM recommendations and field data. "
            "Monitor spare parts usage and availability using inventory management tools. "
            "Document inventory levels and failures. "
            "Analyze root causes of inventory shortages. "
            "Train personnel on best practices and inventory management tools. "
            "Communicate findings and recommendations to procurement teams."
        ),
        key_factors=[
            "Inventory management procedures",
            "Usage monitoring",
            "Availability",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Spare Parts Inventory Guide", "SPM Fluid End Maintenance Manual"],
        burden_holder="Procurement Supervisor",
        adversary_position="Inventory management is not critical for fluid end performance.",
        counter_arguments=[
            "Effective inventory management reduces downtime.",
            "Field data supports structured inventory management procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured inventory management program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump fluid end",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Spare Parts Inventory Guide 2018"
    ),
    DoctrineBlock(
        topic="Power End Spare Parts Inventory Management",
        keywords=["power end", "spare parts", "inventory management", "mud pump", "OFE01"],
        conclusion_template="Effective spare parts inventory management is essential for minimizing downtime and ensuring availability of critical components in OFE01 mud pump power ends.",
        reasoning_framework=(
            "Establish inventory management procedures based on OEM recommendations and field data. "
            "Monitor spare parts usage and availability using inventory management tools. "
            "Document inventory levels and failures. "
            "Analyze root causes of inventory shortages. "
            "Train personnel on best practices and inventory management tools. "
            "Communicate findings and recommendations to procurement teams."
        ),
        key_factors=[
            "Inventory management procedures",
            "Usage monitoring",
            "Availability",
            "OEM recommendations",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Spare Parts Inventory Guide", "SPM Power End Maintenance Manual"],
        burden_holder="Procurement Supervisor",
        adversary_position="Inventory management is not critical for power end performance.",
        counter_arguments=[
            "Effective inventory management reduces downtime.",
            "Field data supports structured inventory management procedures.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement structured inventory management program based on OEM recommendations and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump power end",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Spare Parts Inventory Guide 2019"
    ),
    DoctrineBlock(
        topic="Mud Pump Automation and Control Systems",
        keywords=["automation", "control systems", "mud pump", "OFE01"],
        conclusion_template="Automation and control systems are essential for optimizing mud pump performance and reducing operator error in OFE01 systems.",
        reasoning_framework=(
            "Evaluate automation and control system requirements based on operational parameters and field data. "
            "Select appropriate control systems (e.g., PLC, SCADA) based on compatibility and performance. "
            "Monitor system performance using real-time data. "
            "Document automation failures and analyze root causes. "
            "Train personnel on best practices and control system operation. "
            "Communicate findings and recommendations to engineering teams."
        ),
        key_factors=[
            "System requirements",
            "Control system selection",
            "Performance monitoring",
            "Compatibility",
            "Failure analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Automation Guide", "SPM Control Systems Manual"],
        burden_holder="Automation Engineer",
        adversary_position="Automation is not necessary for mud pump performance.",
        counter_arguments=[
            "Automation reduces operator error and optimizes performance.",
            "Field data supports structured automation strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement automation and control systems based on operational requirements and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Automation Guide 2020"
    ),
    DoctrineBlock(
        topic="Mud Pump Noise and Vibration Mitigation",
        keywords=["noise", "vibration", "mitigation", "mud pump", "OFE01"],
        conclusion_template="Noise and vibration mitigation strategies are essential for protecting personnel and equipment in OFE01 mud pump systems.",
        reasoning_framework=(
            "Evaluate noise and vibration levels using monitoring tools. "
            "Implement mitigation strategies (e.g., dampeners, isolation mounts, acoustic enclosures) based on field data and OEM recommendations. "
            "Document mitigation outcomes and failures. "
            "Analyze root causes of excessive noise and vibration. "
            "Train personnel on best practices and mitigation tools. "
            "Communicate findings and recommendations to engineering teams."
        ),
        key_factors=[
            "Monitoring tools",
            "Mitigation strategies",
            "OEM recommendations",
            "Failure analysis",
            "Personnel safety"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Noise and Vibration Mitigation Guide", "SPM Maintenance Manual"],
        burden_holder="Safety Engineer",
        adversary_position="Noise and vibration mitigation is not necessary for mud pump performance.",
        counter_arguments=[
            "Mitigation protects personnel and equipment.",
            "Field data supports structured mitigation strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement noise and vibration mitigation strategies based on field data and OEM recommendations; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Noise and Vibration Mitigation Guide 2018"
    ),
    DoctrineBlock(
        topic="Mud Pump Energy Efficiency Optimization",
        keywords=["energy efficiency", "optimization", "mud pump", "OFE01"],
        conclusion_template="Energy efficiency optimization strategies are essential for reducing operational costs and environmental impact in OFE01 mud pump systems.",
        reasoning_framework=(
            "Evaluate energy efficiency using OEM efficiency curves and field data. "
            "Implement optimization strategies (e.g., variable frequency drives, stroke rate adjustment) based on operational requirements. "
            "Monitor energy usage using real-time data. "
            "Document optimization outcomes and failures. "
            "Analyze root causes of energy inefficiency. "
            "Train personnel on best practices and optimization tools. "
            "Communicate findings and recommendations to engineering teams."
        ),
        key_factors=[
            "Efficiency curves",
            "Optimization strategies",
            "Energy usage monitoring",
            "OEM recommendations",
            "Cost analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Energy Efficiency Guide", "SPM Maintenance Manual"],
        burden_holder="Operations Engineer",
        adversary_position="Energy efficiency optimization is not necessary for mud pump performance.",
        counter_arguments=[
            "Optimization reduces operational costs and environmental impact.",
            "Field data supports structured optimization strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement energy efficiency optimization strategies based on field data and OEM recommendations; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Energy Efficiency Guide 2019"
    ),
    DoctrineBlock(
        topic="Mud Pump Remote Monitoring and Diagnostics",
        keywords=["remote monitoring", "diagnostics", "mud pump", "OFE01"],
        conclusion_template="Remote monitoring and diagnostics are essential for detecting early signs of failure and optimizing maintenance in OFE01 mud pump systems.",
        reasoning_framework=(
            "Implement remote monitoring tools (e.g., sensors, data acquisition systems) based on OEM recommendations and field data. "
            "Monitor pump performance using real-time data. "
            "Document remote monitoring outcomes and failures. "
            "Analyze root causes of failures detected remotely. "
            "Train personnel on best practices and remote monitoring tools. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Monitoring tools",
            "Performance monitoring",
            "OEM recommendations",
            "Failure analysis",
            "Maintenance optimization"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Remote Monitoring Guide", "SPM Maintenance Manual"],
        burden_holder="Maintenance Engineer",
        adversary_position="Remote monitoring is not necessary for mud pump performance.",
        counter_arguments=[
            "Remote monitoring detects early failures.",
            "Field data supports structured remote monitoring strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement remote monitoring and diagnostics based on field data and OEM recommendations; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Remote Monitoring Guide 2020"
    ),
    DoctrineBlock(
        topic="Mud Pump Environmental Compliance",
        keywords=["environmental compliance", "mud pump", "OFE01"],
        conclusion_template="Environmental compliance strategies are essential for minimizing environmental impact and ensuring regulatory compliance in OFE01 mud pump systems.",
        reasoning_framework=(
            "Evaluate environmental compliance requirements based on regulatory standards and field data. "
            "Implement compliance strategies (e.g., containment, spill prevention, waste management) based on operational requirements. "
            "Monitor compliance using real-time data and inspection tools. "
            "Document compliance outcomes and failures. "
            "Analyze root causes of compliance failures. "
            "Train personnel on best practices and compliance tools. "
            "Communicate findings and recommendations to safety teams."
        ),
        key_factors=[
            "Regulatory standards",
            "Compliance strategies",
            "Monitoring tools",
            "Failure analysis",
            "Personnel training"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Environmental Compliance Guide", "SPM Maintenance Manual"],
        burden_holder="Safety Engineer",
        adversary_position="Environmental compliance is not necessary for mud pump performance.",
        counter_arguments=[
            "Compliance minimizes environmental impact and ensures regulatory adherence.",
            "Field data supports structured compliance strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement environmental compliance strategies based on regulatory standards and field data; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Environmental Compliance Guide 2019"
    ),
    DoctrineBlock(
        topic="Mud Pump Safety Training and Procedures",
        keywords=["safety training", "procedures", "mud pump", "OFE01"],
        conclusion_template="Structured safety training and procedures are essential for protecting personnel and ensuring safe operation of OFE01 mud pump systems.",
        reasoning_framework=(
            "Establish safety training and procedures based on OEM recommendations and regulatory standards. "
            "Train personnel on best practices and emergency procedures. "
            "Monitor safety performance using real-time data and inspection tools. "
            "Document safety outcomes and incidents. "
            "Analyze root causes of safety incidents. "
            "Communicate findings and recommendations to safety teams."
        ),
        key_factors=[
            "Training procedures",
            "Emergency procedures",
            "Monitoring tools",
            "Regulatory standards",
            "Incident analysis"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Safety Training Guide", "SPM Maintenance Manual"],
        burden_holder="Safety Supervisor",
        adversary_position="Safety training and procedures are not necessary for mud pump operation.",
        counter_arguments=[
            "Structured training protects personnel and ensures safe operation.",
            "Field data supports structured safety training strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement safety training and procedures based on regulatory standards and OEM recommendations; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Safety Training Guide 2020"
    ),
    DoctrineBlock(
        topic="Mud Pump Data Analytics for Predictive Maintenance",
        keywords=["data analytics", "predictive maintenance", "mud pump", "OFE01"],
        conclusion_template="Data analytics and predictive maintenance strategies are essential for reducing downtime and optimizing maintenance in OFE01 mud pump systems.",
        reasoning_framework=(
            "Implement data analytics tools (e.g., machine learning, statistical analysis) based on OEM recommendations and field data. "
            "Monitor pump performance using real-time data. "
            "Document predictive maintenance outcomes and failures. "
            "Analyze root causes of failures detected by analytics. "
            "Train personnel on best practices and analytics tools. "
            "Communicate findings and recommendations to maintenance teams."
        ),
        key_factors=[
            "Analytics tools",
            "Performance monitoring",
            "OEM recommendations",
            "Failure analysis",
            "Maintenance optimization"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Predictive Maintenance Guide", "SPM Maintenance Manual"],
        burden_holder="Maintenance Engineer",
        adversary_position="Data analytics and predictive maintenance are not necessary for mud pump performance.",
        counter_arguments=[
            "Predictive maintenance reduces downtime.",
            "Field data supports structured analytics strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement data analytics and predictive maintenance based on field data and OEM recommendations; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Predictive Maintenance Guide 2020"
    ),
    DoctrineBlock(
        topic="Mud Pump Performance Benchmarking",
        keywords=["performance benchmarking", "mud pump", "OFE01"],
        conclusion_template="Performance benchmarking is essential for identifying improvement opportunities and optimizing mud pump operation in OFE01 systems.",
        reasoning_framework=(
            "Establish benchmarking procedures based on OEM recommendations and field data. "
            "Monitor pump performance using real-time data and benchmarking tools. "
            "Document benchmarking outcomes and failures. "
            "Analyze root causes of performance gaps. "
            "Train personnel on best practices and benchmarking tools. "
            "Communicate findings and recommendations to engineering teams."
        ),
        key_factors=[
            "Benchmarking procedures",
            "Performance monitoring",
            "OEM recommendations",
            "Failure analysis",
            "Improvement strategies"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver Performance Benchmarking Guide", "SPM Maintenance Manual"],
        burden_holder="Operations Engineer",
        adversary_position="Performance benchmarking is not necessary for mud pump operation.",
        counter_arguments=[
            "Benchmarking identifies improvement opportunities.",
            "Field data supports structured benchmarking strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement performance benchmarking based on field data and OEM recommendations; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver Performance Benchmarking Guide 2019"
    ),
    DoctrineBlock(
        topic="Mud Pump System Integration and Compatibility",
        keywords=["system integration", "compatibility", "mud pump", "OFE01"],
        conclusion_template="System integration and compatibility strategies are essential for ensuring reliable operation and minimizing downtime in OFE01 mud pump systems.",
        reasoning_framework=(
            "Evaluate integration and compatibility requirements based on operational parameters and field data. "
            "Select compatible components and systems based on OEM recommendations. "
            "Monitor integration outcomes using real-time data. "
            "Document compatibility failures and analyze root causes. "
            "Train personnel on best practices and integration tools. "
            "Communicate findings and recommendations to engineering teams."
        ),
        key_factors=[
            "Integration requirements",
            "Compatibility",
            "OEM recommendations",
            "Failure analysis",
            "Improvement strategies"
        ],
        primary_authority=["API Spec 7K", "Gardner Denver System Integration Guide", "SPM Maintenance Manual"],
        burden_holder="System Engineer",
        adversary_position="System integration and compatibility are not necessary for mud pump operation.",
        counter_arguments=[
            "Integration ensures reliable operation and minimizes downtime.",
            "Field data supports structured integration strategies.",
            "OEM guidelines provide proven methodologies."
        ],
        resolution_strategy="Implement system integration and compatibility strategies based on field data and OEM recommendations; review outcomes quarterly.",
        entity_scope="OFE01 mud pump system",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Gardner Denver System Integration Guide 2018"
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