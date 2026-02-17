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
        topic="API 675 Chemical Metering Pump Selection",
        keywords=["API 675", "metering pump", "chemical injection", "selection criteria", "stroke adjustment", "flow rate", "pressure", "material compatibility"],
        conclusion_template="The selected metering pump must comply with API 675 standards, match process flow and pressure requirements, and ensure material compatibility with injected chemicals.",
        reasoning_framework="""
        1. Review process requirements: required flow rate, discharge pressure, chemical type, and viscosity.
        2. Confirm API 675 compliance for pump design, including accuracy, repeatability, and safety features.
        3. Evaluate pump material compatibility with injected chemicals to prevent corrosion or degradation.
        4. Assess stroke adjustment mechanism for precise dosing and operational flexibility.
        5. Analyze installation constraints, including available footprint and environmental conditions.
        6. Consider maintenance requirements and local support availability.
        7. Validate vendor documentation and performance curves against site conditions.
        8. Ensure integration with control systems for automated dosing.
        9. Review historical reliability data and mean time between failure (MTBF).
        10. Final selection based on lifecycle cost, compliance, and operational risk mitigation.
        """,
        key_factors=[
            "API 675 compliance",
            "Flow rate and pressure requirements",
            "Material compatibility",
            "Stroke adjustment mechanism",
            "Maintenance and reliability",
            "Integration with control systems"
        ],
        primary_authority=["API 675 Standard", "Manufacturer Technical Datasheets", "Site Process Engineering"],
        burden_holder="Process Engineer",
        adversary_position="Vendor proposing non-compliant or unsuitable pump",
        counter_arguments=[
            "Alternative pump offers lower upfront cost but lacks API 675 certification",
            "Vendor claims material compatibility without supporting data",
            "Pump performance curves not validated for site conditions"
        ],
        resolution_strategy="Require documented compliance, site-specific performance validation, and material compatibility certificates.",
        entity_scope="OFE14 chemical injection system",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 675:2014 Chemical Metering Pumps Standard"
    ),
    DoctrineBlock(
        topic="Injection Quill Design and Placement",
        keywords=["injection quill", "design", "placement", "chemical distribution", "mixing", "corrosion", "erosion", "velocity profile"],
        conclusion_template="Injection quill design and placement must ensure optimal chemical distribution, minimize corrosion/erosion, and comply with process velocity profiles.",
        reasoning_framework="""
        1. Analyze process pipe diameter, flow velocity, and turbulence characteristics.
        2. Select quill material compatible with injected chemical and process fluid.
        3. Design quill length to reach the center of pipe or desired injection zone.
        4. Incorporate anti-vortex and check valve features to prevent backflow and ensure mixing.
        5. Position quill downstream of pumps, bends, or valves to maximize mixing and minimize dead zones.
        6. Evaluate risk of erosion and corrosion at injection point; reinforce with suitable alloys or coatings.
        7. Confirm quill installation meets ASME B31.3 and site safety standards.
        8. Validate placement via CFD modeling or empirical testing.
        9. Document maintenance access and isolation provisions.
        10. Finalize design based on operational feedback and historical performance.
        """,
        key_factors=[
            "Pipe diameter and velocity profile",
            "Material compatibility",
            "Quill length and design",
            "Mixing efficiency",
            "Corrosion and erosion risk",
            "Safety and maintenance access"
        ],
        primary_authority=["ASME B31.3", "CFD Modeling Reports", "Site Engineering Standards"],
        burden_holder="Mechanical Engineer",
        adversary_position="Process operator concerned about quill-induced erosion",
        counter_arguments=[
            "Quill may cause localized erosion or turbulence",
            "Improper placement leads to poor chemical mixing",
            "Material selection may not withstand process conditions"
        ],
        resolution_strategy="Conduct CFD analysis, select robust materials, and validate placement with process data.",
        entity_scope="OFE14 injection points",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.3 Process Piping Code"
    ),
    DoctrineBlock(
        topic="Corrosion Inhibitor Film-Forming Amine Programs",
        keywords=["corrosion inhibitor", "film-forming amine", "program design", "dosage", "monitoring", "efficacy", "pipeline protection"],
        conclusion_template="Corrosion inhibitor programs must optimize film-forming amine dosage, monitor efficacy, and ensure pipeline protection under all operating conditions.",
        reasoning_framework="""
        1. Identify pipeline metallurgy, fluid composition, and operating temperature/pressure.
        2. Select film-forming amine based on compatibility and proven efficacy for site conditions.
        3. Establish initial dosage via laboratory testing and field trials.
        4. Implement real-time monitoring (e.g., corrosion coupons, ER probes) to assess inhibitor performance.
        5. Adjust dosing based on monitoring feedback and process changes.
        6. Maintain inhibitor inventory and ensure continuous injection during critical operations.
        7. Document program performance, including corrosion rate reduction and operational incidents.
        8. Review regulatory compliance and environmental impact.
        9. Conduct periodic audits and optimize program based on historical data.
        10. Communicate results to stakeholders and update program as needed.
        """,
        key_factors=[
            "Pipeline metallurgy",
            "Fluid composition",
            "Dosage optimization",
            "Monitoring and feedback",
            "Regulatory compliance",
            "Inventory management"
        ],
        primary_authority=["NACE SP0106", "Laboratory Test Reports", "Site Corrosion Monitoring Data"],
        burden_holder="Corrosion Engineer",
        adversary_position="Operations questioning inhibitor effectiveness",
        counter_arguments=[
            "Observed corrosion rates remain high despite inhibitor injection",
            "Film-forming amine may not be compatible with process fluids",
            "Environmental concerns about amine discharge"
        ],
        resolution_strategy="Increase monitoring frequency, adjust dosage, and validate compatibility via lab tests.",
        entity_scope="OFE14 pipeline protection",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0106-2006 Corrosion Inhibitor Application"
    ),
    DoctrineBlock(
        topic="Scale Inhibitor Squeeze Treatment Design",
        keywords=["scale inhibitor", "squeeze treatment", "design", "reservoir", "adsorption", "desorption", "treatment life", "chemical selection"],
        conclusion_template="Scale inhibitor squeeze treatment must be designed for optimal adsorption/desorption, maximize treatment life, and ensure chemical compatibility with reservoir fluids.",
        reasoning_framework="""
        1. Characterize reservoir mineralogy, permeability, and fluid composition.
        2. Select scale inhibitor based on adsorption characteristics and compatibility with formation water.
        3. Design squeeze treatment volume and injection rate to maximize inhibitor placement.
        4. Model adsorption/desorption kinetics to predict treatment life.
        5. Validate design via laboratory core flood tests and field pilot trials.
        6. Monitor post-treatment scale deposition and adjust program as needed.
        7. Document treatment performance and update design based on historical data.
        8. Ensure compliance with environmental regulations regarding chemical discharge.
        9. Communicate results to reservoir and production teams.
        10. Optimize future treatments based on feedback and performance metrics.
        """,
        key_factors=[
            "Reservoir mineralogy and permeability",
            "Inhibitor adsorption/desorption",
            "Treatment volume and injection rate",
            "Chemical compatibility",
            "Monitoring and optimization"
        ],
        primary_authority=["SPE Technical Papers", "Laboratory Core Flood Reports", "Site Production Data"],
        burden_holder="Reservoir Engineer",
        adversary_position="Production questioning squeeze treatment efficacy",
        counter_arguments=[
            "Scale deposition persists post-treatment",
            "Inhibitor may not adsorb effectively in formation",
            "Environmental concerns about chemical discharge"
        ],
        resolution_strategy="Conduct additional lab tests, optimize injection parameters, and monitor treatment outcomes.",
        entity_scope="OFE14 reservoir scale management",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 123456 Scale Squeeze Treatment Guidelines"
    ),
    DoctrineBlock(
        topic="Paraffin Management - Crystal Modifiers vs Solvents",
        keywords=["paraffin", "management", "crystal modifier", "solvent", "pipeline", "wax deposition", "chemical selection"],
        conclusion_template="Paraffin management must balance crystal modifier and solvent use to minimize wax deposition and optimize pipeline flow.",
        reasoning_framework="""
        1. Assess pipeline temperature profile, crude composition, and wax content.
        2. Evaluate crystal modifier efficacy in preventing wax crystallization and deposition.
        3. Compare solvent effectiveness in dissolving existing wax deposits.
        4. Model wax deposition rates under various treatment scenarios.
        5. Select chemical program based on cost, efficacy, and operational constraints.
        6. Monitor pipeline flow and wax deposition via pigging and visual inspection.
        7. Adjust chemical dosing based on monitoring feedback and seasonal variations.
        8. Document program performance and optimize based on historical data.
        9. Ensure compliance with environmental regulations regarding solvent discharge.
        10. Communicate results to operations and update program as needed.
        """,
        key_factors=[
            "Pipeline temperature and crude composition",
            "Crystal modifier efficacy",
            "Solvent effectiveness",
            "Wax deposition monitoring",
            "Cost and environmental compliance"
        ],
        primary_authority=["SPE Technical Papers", "Laboratory Wax Deposition Reports", "Site Operations Data"],
        burden_holder="Production Engineer",
        adversary_position="Operations favoring solvent-only approach",
        counter_arguments=[
            "Solvents provide faster wax removal but higher environmental impact",
            "Crystal modifiers may not prevent deposition under low temperatures",
            "Cost concerns with combined chemical approach"
        ],
        resolution_strategy="Conduct comparative trials, optimize dosing, and select chemicals based on efficacy and compliance.",
        entity_scope="OFE14 pipeline wax management",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 654321 Paraffin Management Guidelines"
    ),
    DoctrineBlock(
        topic="Demulsifier Optimization via Bottle Testing",
        keywords=["demulsifier", "optimization", "bottle testing", "emulsion", "water cut", "chemical selection", "efficacy"],
        conclusion_template="Demulsifier selection and dosing must be optimized via bottle testing to maximize water separation and minimize residual emulsion.",
        reasoning_framework="""
        1. Collect representative process samples for bottle testing.
        2. Screen demulsifier candidates based on chemical compatibility and prior performance.
        3. Conduct bottle tests at process temperature and agitation conditions.
        4. Evaluate water separation, residual emulsion, and interface quality.
        5. Select optimal demulsifier and dosage based on test results.
        6. Validate selection via field trials and monitor water cut improvement.
        7. Adjust dosing based on ongoing process feedback and seasonal variations.
        8. Document program performance and update selection based on historical data.
        9. Ensure compliance with environmental discharge limits.
        10. Communicate results to operations and optimize program as needed.
        """,
        key_factors=[
            "Sample representativeness",
            "Demulsifier compatibility",
            "Bottle test conditions",
            "Water separation efficacy",
            "Environmental compliance"
        ],
        primary_authority=["ASTM D1401", "Laboratory Bottle Test Reports", "Site Operations Data"],
        burden_holder="Process Chemist",
        adversary_position="Operations questioning bottle test representativeness",
        counter_arguments=[
            "Bottle tests may not reflect actual process conditions",
            "Demulsifier may not perform under field conditions",
            "Environmental concerns about demulsifier discharge"
        ],
        resolution_strategy="Conduct field validation, adjust dosing, and ensure compliance with discharge limits.",
        entity_scope="OFE14 emulsion management",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM D1401 Demulsifier Testing Protocol"
    ),
    DoctrineBlock(
        topic="H2S Scavenger Systems - Triazine vs Solid-Based",
        keywords=["H2S scavenger", "triazine", "solid-based", "system design", "efficacy", "chemical selection", "safety"],
        conclusion_template="H2S scavenger system selection must weigh triazine and solid-based options for efficacy, safety, and operational compatibility.",
        reasoning_framework="""
        1. Assess H2S concentration, flow rate, and process conditions.
        2. Evaluate triazine scavenger efficacy and compatibility with process fluids.
        3. Compare solid-based scavenger performance, including removal efficiency and operational footprint.
        4. Model scavenger consumption rates and replacement frequency.
        5. Analyze safety risks associated with chemical handling and byproduct formation.
        6. Select system based on cost, efficacy, and site constraints.
        7. Monitor H2S levels post-treatment and adjust program as needed.
        8. Document system performance and optimize based on historical data.
        9. Ensure compliance with safety and environmental regulations.
        10. Communicate results to operations and update selection as needed.
        """,
        key_factors=[
            "H2S concentration and flow rate",
            "Triazine efficacy",
            "Solid-based scavenger performance",
            "Safety and byproduct risks",
            "Cost and operational footprint"
        ],
        primary_authority=["API RP 55", "Manufacturer Technical Datasheets", "Site Safety Standards"],
        burden_holder="Process Safety Engineer",
        adversary_position="Operations favoring triazine for ease of dosing",
        counter_arguments=[
            "Triazine may form hazardous byproducts",
            "Solid-based systems require frequent replacement",
            "Cost concerns with solid-based approach"
        ],
        resolution_strategy="Conduct comparative trials, assess safety risks, and select based on efficacy and compliance.",
        entity_scope="OFE14 H2S management",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 55 H2S Scavenger Guidelines"
    ),
    DoctrineBlock(
        topic="Biocide Programs for Microbiological Control",
        keywords=["biocide", "microbiological control", "program design", "dosage", "monitoring", "efficacy", "chemical selection"],
        conclusion_template="Biocide programs must optimize chemical selection and dosing to control microbiological activity and prevent biofilm formation.",
        reasoning_framework="""
        1. Identify target microorganisms and assess biofilm risk.
        2. Select biocide based on efficacy, compatibility, and environmental impact.
        3. Establish initial dosage via laboratory testing and field trials.
        4. Implement real-time monitoring (e.g., ATP testing, microbial counts) to assess biocide performance.
        5. Adjust dosing based on monitoring feedback and process changes.
        6. Maintain biocide inventory and ensure continuous injection during critical operations.
        7. Document program performance, including biofilm reduction and operational incidents.
        8. Review regulatory compliance and environmental impact.
        9. Conduct periodic audits and optimize program based on historical data.
        10. Communicate results to stakeholders and update program as needed.
        """,
        key_factors=[
            "Target microorganisms",
            "Biocide efficacy",
            "Dosage optimization",
            "Monitoring and feedback",
            "Regulatory compliance"
        ],
        primary_authority=["EPA Biocide Registration", "Laboratory Test Reports", "Site Microbiological Monitoring Data"],
        burden_holder="Process Chemist",
        adversary_position="Operations questioning biocide effectiveness",
        counter_arguments=[
            "Observed biofilm persists despite biocide injection",
            "Biocide may not be compatible with process fluids",
            "Environmental concerns about biocide discharge"
        ],
        resolution_strategy="Increase monitoring frequency, adjust dosage, and validate compatibility via lab tests.",
        entity_scope="OFE14 microbiological control",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Biocide Registration Guidelines"
    ),
    DoctrineBlock(
        topic="Chemical Dosing Rate Optimization via MEC Testing",
        keywords=["chemical dosing", "rate optimization", "MEC testing", "minimum effective concentration", "efficacy", "cost", "process control"],
        conclusion_template="Chemical dosing rates must be optimized via MEC testing to ensure efficacy and minimize cost.",
        reasoning_framework="""
        1. Conduct laboratory MEC (Minimum Effective Concentration) tests for target chemicals.
        2. Establish initial dosing rates based on MEC results and process requirements.
        3. Validate dosing rates via field trials and monitor process performance.
        4. Adjust dosing based on real-time feedback and seasonal variations.
        5. Document dosing optimization and update based on historical data.
        6. Ensure compliance with environmental discharge limits.
        7. Communicate results to operations and optimize program as needed.
        8. Review cost implications and minimize chemical consumption.
        9. Integrate dosing control with automated systems for precision.
        10. Conduct periodic audits and update dosing strategy.
        """,
        key_factors=[
            "MEC test results",
            "Process requirements",
            "Field validation",
            "Cost optimization",
            "Environmental compliance"
        ],
        primary_authority=["Laboratory MEC Reports", "Site Operations Data", "Process Control Standards"],
        burden_holder="Process Engineer",
        adversary_position="Operations favoring higher dosing for perceived safety",
        counter_arguments=[
            "Higher dosing may not improve efficacy",
            "Excess chemical increases cost and environmental impact",
            "MEC tests may not reflect field conditions"
        ],
        resolution_strategy="Validate dosing via field trials, adjust based on feedback, and ensure compliance.",
        entity_scope="OFE14 chemical dosing optimization",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Laboratory MEC Testing Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Compatibility Testing Protocol",
        keywords=["chemical compatibility", "testing protocol", "laboratory", "field validation", "injection", "corrosion", "scaling"],
        conclusion_template="Chemical compatibility must be validated via laboratory and field testing to prevent adverse reactions and ensure injection efficacy.",
        reasoning_framework="""
        1. Review process fluid composition and identify potential incompatibilities.
        2. Conduct laboratory compatibility tests for candidate chemicals.
        3. Evaluate corrosion, scaling, and emulsion risks in test results.
        4. Validate compatibility via field trials and monitor process performance.
        5. Document compatibility findings and update chemical selection.
        6. Communicate results to operations and optimize program as needed.
        7. Ensure compliance with safety and environmental regulations.
        8. Review historical incidents and lessons learned.
        9. Conduct periodic audits and update compatibility protocol.
        10. Integrate compatibility testing into chemical selection workflow.
        """,
        key_factors=[
            "Process fluid composition",
            "Laboratory compatibility tests",
            "Field validation",
            "Corrosion and scaling risk",
            "Safety and environmental compliance"
        ],
        primary_authority=["ASTM D6979", "Laboratory Compatibility Reports", "Site Operations Data"],
        burden_holder="Process Chemist",
        adversary_position="Vendor proposing untested chemical blends",
        counter_arguments=[
            "Untested blends may cause adverse reactions",
            "Laboratory tests may not reflect field conditions",
            "Compatibility protocol may delay chemical selection"
        ],
        resolution_strategy="Require laboratory and field validation, update protocol based on incidents.",
        entity_scope="OFE14 chemical compatibility",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM D6979 Chemical Compatibility Testing"
    ),
    DoctrineBlock(
        topic="Chemical Inventory and Tote Farm Management",
        keywords=["chemical inventory", "tote farm", "management", "tracking", "safety", "storage", "logistics"],
        conclusion_template="Chemical inventory and tote farm management must ensure accurate tracking, safe storage, and efficient logistics.",
        reasoning_framework="""
        1. Implement inventory tracking system for all chemicals and totes.
        2. Ensure tote farm layout complies with safety and fire codes.
        3. Maintain segregation of incompatible chemicals.
        4. Monitor inventory levels and reorder points to prevent stockouts.
        5. Document storage conditions and inspect totes regularly for leaks or damage.
        6. Train personnel in safe handling and emergency response.
        7. Review logistics for chemical delivery and onsite movement.
        8. Ensure compliance with environmental and safety regulations.
        9. Conduct periodic audits and update management procedures.
        10. Communicate inventory status to operations and optimize logistics.
        """,
        key_factors=[
            "Inventory tracking",
            "Safety and fire code compliance",
            "Segregation of chemicals",
            "Storage conditions",
            "Logistics and delivery"
        ],
        primary_authority=["NFPA 30", "Site Safety Standards", "Inventory Management System"],
        burden_holder="Warehouse Manager",
        adversary_position="Operations concerned about stockouts or unsafe storage",
        counter_arguments=[
            "Inventory tracking system may not be updated in real time",
            "Tote farm layout may not comply with latest codes",
            "Segregation may be compromised during peak operations"
        ],
        resolution_strategy="Implement real-time tracking, conduct safety audits, and update procedures.",
        entity_scope="OFE14 chemical inventory",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 30 Flammable and Combustible Liquids Code"
    ),
    DoctrineBlock(
        topic="Safety Data Sheet (SDS) and GHS Compliance",
        keywords=["SDS", "GHS", "compliance", "chemical safety", "hazard communication", "regulatory", "training"],
        conclusion_template="All chemicals must have current SDS and GHS-compliant labeling; personnel must be trained in hazard communication and emergency response.",
        reasoning_framework="""
        1. Ensure all chemicals onsite have current SDS from manufacturer.
        2. Verify GHS-compliant labeling and hazard pictograms on all containers.
        3. Train personnel in SDS interpretation and hazard communication.
        4. Maintain SDS repository accessible to all staff.
        5. Review regulatory requirements for SDS and GHS compliance.
        6. Conduct periodic audits to verify labeling and documentation.
        7. Document training records and update as regulations change.
        8. Communicate hazards and emergency response procedures to all personnel.
        9. Integrate SDS and GHS compliance into procurement workflow.
        10. Update SDS repository and labeling as new chemicals are introduced.
        """,
        key_factors=[
            "Current SDS availability",
            "GHS-compliant labeling",
            "Personnel training",
            "Regulatory compliance",
            "Audit and documentation"
        ],
        primary_authority=["OSHA 1910.1200", "GHS Regulations", "Site Safety Standards"],
        burden_holder="Safety Manager",
        adversary_position="Operations using unlabeled or undocumented chemicals",
        counter_arguments=[
            "SDS may not be available for all chemicals",
            "Labeling may not comply with GHS pictograms",
            "Personnel may lack training in hazard communication"
        ],
        resolution_strategy="Conduct training, update SDS repository, and audit labeling compliance.",
        entity_scope="OFE14 chemical safety",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910.1200 Hazard Communication Standard"
    ),
    DoctrineBlock(
        topic="Injection Pressure Control for Chemical Pumps",
        keywords=["injection pressure", "chemical pump", "pressure control", "safety", "pump protection", "process integration"],
        conclusion_template="Injection pressure must be monitored and controlled to protect chemical pumps and ensure safe, effective injection.",
        reasoning_framework="""
        1. Set pressure limits based on pump manufacturer specifications and process requirements.
        2. Install pressure sensors and transmitters at injection points.
        3. Integrate pressure control into automated pump systems.
        4. Implement alarms and shutdown protocols for overpressure events.
        5. Document pressure control procedures and train operators.
        6. Review historical pressure excursions and update control strategy.
        7. Conduct periodic calibration and maintenance of sensors.
        8. Communicate pressure control requirements to engineering and operations.
        9. Ensure compliance with safety and process standards.
        10. Audit pressure control system performance and optimize as needed.
        """,
        key_factors=[
            "Pressure limits",
            "Sensor installation",
            "Automation integration",
            "Alarm and shutdown protocols",
            "Operator training"
        ],
        primary_authority=["API 675", "Manufacturer Specifications", "Site Safety Standards"],
        burden_holder="Process Engineer",
        adversary_position="Operations bypassing pressure alarms",
        counter_arguments=[
            "Pressure alarms may cause unnecessary shutdowns",
            "Sensors may fail or drift out of calibration",
            "Pressure control may limit operational flexibility"
        ],
        resolution_strategy="Regular sensor maintenance, operator training, and review of alarm thresholds.",
        entity_scope="OFE14 chemical injection pressure control",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 675 Chemical Injection Pump Standard"
    ),
    DoctrineBlock(
        topic="Automated Chemical Injection System Integration",
        keywords=["automated injection", "system integration", "PLC", "SCADA", "chemical dosing", "process control"],
        conclusion_template="Automated chemical injection systems must be integrated with PLC/SCADA for precise dosing and real-time monitoring.",
        reasoning_framework="""
        1. Review process requirements and dosing accuracy targets.
        2. Select PLC/SCADA platform compatible with chemical injection equipment.
        3. Integrate pump controls, dosing feedback, and alarm management.
        4. Validate system performance via factory acceptance testing (FAT).
        5. Train operators in system operation and troubleshooting.
        6. Document integration procedures and update as new chemicals are introduced.
        7. Monitor dosing accuracy and system reliability.
        8. Conduct periodic audits and optimize integration.
        9. Ensure compliance with process control standards.
        10. Communicate integration results to engineering and operations.
        """,
        key_factors=[
            "PLC/SCADA compatibility",
            "Dosing accuracy",
            "Alarm management",
            "Operator training",
            "System reliability"
        ],
        primary_authority=["ISA 88", "Site Process Control Standards", "Manufacturer Integration Guides"],
        burden_holder="Automation Engineer",
        adversary_position="Operations preferring manual dosing",
        counter_arguments=[
            "Manual dosing offers flexibility",
            "Automated systems may fail or require complex troubleshooting",
            "Integration may increase upfront cost"
        ],
        resolution_strategy="Conduct FAT, train operators, and optimize integration for reliability.",
        entity_scope="OFE14 automated injection",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 88 Batch Control Standard"
    ),
    DoctrineBlock(
        topic="Chemical Injection Line Flushing Protocol",
        keywords=["line flushing", "chemical injection", "protocol", "maintenance", "contamination", "safety"],
        conclusion_template="Chemical injection lines must be flushed according to protocol to prevent contamination and ensure safe maintenance.",
        reasoning_framework="""
        1. Establish flushing frequency based on chemical type and injection line usage.
        2. Select flushing fluid compatible with process and injected chemicals.
        3. Document flushing procedures and train maintenance personnel.
        4. Monitor line cleanliness and verify absence of residual chemicals.
        5. Ensure compliance with safety and environmental standards.
        6. Conduct periodic audits and update protocol as needed.
        7. Communicate flushing requirements to operations and maintenance teams.
        8. Review historical contamination incidents and optimize protocol.
        9. Integrate flushing into maintenance workflow.
        10. Validate protocol effectiveness via laboratory and field testing.
        """,
        key_factors=[
            "Flushing frequency",
            "Fluid compatibility",
            "Procedure documentation",
            "Safety compliance",
            "Protocol validation"
        ],
        primary_authority=["Site Maintenance Standards", "Manufacturer Flushing Guides", "Safety Regulations"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Operations questioning flushing necessity",
        counter_arguments=[
            "Flushing may interrupt injection operations",
            "Procedure may not remove all residual chemicals",
            "Environmental concerns about flushing fluid disposal"
        ],
        resolution_strategy="Optimize flushing frequency, validate protocol, and ensure safe disposal.",
        entity_scope="OFE14 injection line maintenance",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Maintenance Flushing Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Leak Detection",
        keywords=["leak detection", "chemical injection", "system integrity", "safety", "monitoring", "environmental compliance"],
        conclusion_template="Chemical injection systems must employ leak detection to ensure system integrity, safety, and environmental compliance.",
        reasoning_framework="""
        1. Install leak detection sensors at critical injection points and lines.
        2. Integrate leak alarms into process control systems.
        3. Document leak detection procedures and train personnel.
        4. Review historical leak incidents and update detection strategy.
        5. Conduct periodic sensor calibration and maintenance.
        6. Communicate leak detection requirements to operations and maintenance teams.
        7. Ensure compliance with safety and environmental regulations.
        8. Audit system performance and optimize detection methods.
        9. Integrate leak detection into emergency response planning.
        10. Validate effectiveness via field testing and incident review.
        """,
        key_factors=[
            "Sensor installation",
            "Alarm integration",
            "Procedure documentation",
            "Regulatory compliance",
            "System performance auditing"
        ],
        primary_authority=["EPA Leak Detection Guidelines", "Site Safety Standards", "Manufacturer Sensor Datasheets"],
        burden_holder="Safety Engineer",
        adversary_position="Operations questioning sensor reliability",
        counter_arguments=[
            "Sensors may fail or provide false alarms",
            "Detection system may not cover all leak scenarios",
            "Cost concerns with sensor installation"
        ],
        resolution_strategy="Regular sensor maintenance, audit coverage, and optimize detection strategy.",
        entity_scope="OFE14 injection system integrity",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Leak Detection and Repair (LDAR) Guidelines"
    ),
    DoctrineBlock(
        topic="Chemical Injection Flow Assurance Strategy",
        keywords=["flow assurance", "chemical injection", "strategy", "paraffin", "hydrate", "scale", "corrosion"],
        conclusion_template="Chemical injection flow assurance strategies must address paraffin, hydrate, scale, and corrosion risks to maintain pipeline integrity.",
        reasoning_framework="""
        1. Identify flow assurance risks based on process conditions and fluid composition.
        2. Select chemicals for paraffin, hydrate, scale, and corrosion control.
        3. Design injection program to address all identified risks.
        4. Monitor pipeline performance and adjust chemical dosing as needed.
        5. Document strategy and communicate to operations and engineering teams.
        6. Review historical incidents and optimize strategy.
        7. Ensure compliance with safety and environmental regulations.
        8. Conduct periodic audits and update strategy based on performance data.
        9. Integrate flow assurance into process control systems.
        10. Validate strategy effectiveness via field trials and monitoring.
        """,
        key_factors=[
            "Risk identification",
            "Chemical selection",
            "Injection program design",
            "Monitoring and adjustment",
            "Regulatory compliance"
        ],
        primary_authority=["SPE Flow Assurance Papers", "Site Operations Data", "Process Engineering Standards"],
        burden_holder="Flow Assurance Engineer",
        adversary_position="Operations questioning multi-chemical approach",
        counter_arguments=[
            "Single chemical may address multiple risks",
            "Multi-chemical approach increases cost and complexity",
            "Strategy may not adapt to changing process conditions"
        ],
        resolution_strategy="Conduct comparative trials, optimize dosing, and update strategy based on feedback.",
        entity_scope="OFE14 pipeline flow assurance",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Flow Assurance Guidelines"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Commissioning Protocol",
        keywords=["commissioning", "chemical injection", "protocol", "system startup", "validation", "safety"],
        conclusion_template="Chemical injection system commissioning must follow protocol to validate performance, ensure safety, and document startup.",
        reasoning_framework="""
        1. Review commissioning checklist and validate system installation.
        2. Conduct pressure and leak tests prior to startup.
        3. Verify chemical pump calibration and dosing accuracy.
        4. Document commissioning procedures and train personnel.
        5. Monitor system performance during initial operation.
        6. Ensure compliance with safety and environmental standards.
        7. Communicate commissioning results to engineering and operations.
        8. Review historical commissioning incidents and update protocol.
        9. Integrate commissioning into project workflow.
        10. Audit system performance and optimize as needed.
        """,
        key_factors=[
            "Checklist review",
            "Pressure and leak testing",
            "Pump calibration",
            "Procedure documentation",
            "Safety compliance"
        ],
        primary_authority=["Site Commissioning Standards", "Manufacturer Startup Guides", "Safety Regulations"],
        burden_holder="Commissioning Engineer",
        adversary_position="Operations questioning commissioning necessity",
        counter_arguments=[
            "Commissioning may delay system startup",
            "Procedure may not identify all issues",
            "Cost concerns with commissioning activities"
        ],
        resolution_strategy="Optimize protocol, validate performance, and ensure safety compliance.",
        entity_scope="OFE14 injection system commissioning",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Commissioning Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Shutdown Procedure",
        keywords=["shutdown", "chemical injection", "procedure", "safety", "system integrity", "maintenance"],
        conclusion_template="Chemical injection system shutdown must follow procedure to ensure safety, maintain system integrity, and prepare for maintenance.",
        reasoning_framework="""
        1. Document shutdown procedures and train personnel.
        2. Isolate chemical pumps and injection lines.
        3. Flush lines to remove residual chemicals.
        4. Monitor system status and verify safe shutdown.
        5. Ensure compliance with safety and environmental standards.
        6. Communicate shutdown requirements to operations and maintenance teams.
        7. Review historical shutdown incidents and update procedure.
        8. Integrate shutdown into maintenance workflow.
        9. Audit procedure effectiveness and optimize as needed.
        10. Validate shutdown via field testing and incident review.
        """,
        key_factors=[
            "Procedure documentation",
            "Isolation and flushing",
            "Safety compliance",
            "Training",
            "Audit and optimization"
        ],
        primary_authority=["Site Shutdown Standards", "Manufacturer Shutdown Guides", "Safety Regulations"],
        burden_holder="Operations Supervisor",
        adversary_position="Maintenance questioning shutdown necessity",
        counter_arguments=[
            "Shutdown may interrupt injection operations",
            "Procedure may not remove all residual chemicals",
            "Environmental concerns about flushing fluid disposal"
        ],
        resolution_strategy="Optimize shutdown procedure, validate effectiveness, and ensure safe disposal.",
        entity_scope="OFE14 injection system shutdown",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Shutdown Procedure"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Emergency Response Plan",
        keywords=["emergency response", "chemical injection", "plan", "spill", "leak", "safety", "regulatory"],
        conclusion_template="Chemical injection systems must have an emergency response plan for spills, leaks, and safety incidents.",
        reasoning_framework="""
        1. Develop emergency response plan covering spills, leaks, and safety incidents.
        2. Train personnel in emergency procedures and response roles.
        3. Install spill containment and leak detection equipment.
        4. Document emergency response procedures and update as regulations change.
        5. Conduct periodic drills and review incident response.
        6. Communicate plan requirements to operations and maintenance teams.
        7. Ensure compliance with safety and environmental regulations.
        8. Audit plan effectiveness and optimize as needed.
        9. Integrate emergency response into site safety workflow.
        10. Validate plan via field testing and incident review.
        """,
        key_factors=[
            "Plan development",
            "Personnel training",
            "Containment equipment",
            "Regulatory compliance",
            "Audit and optimization"
        ],
        primary_authority=["EPA Emergency Response Guidelines", "Site Safety Standards", "Manufacturer Spill Containment Guides"],
        burden_holder="Safety Manager",
        adversary_position="Operations questioning plan necessity",
        counter_arguments=[
            "Plan may not cover all incident scenarios",
            "Training may not be updated",
            "Cost concerns with containment equipment"
        ],
        resolution_strategy="Conduct drills, update plan, and audit effectiveness.",
        entity_scope="OFE14 injection system emergency response",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Emergency Response Guidelines"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Performance Monitoring",
        keywords=["performance monitoring", "chemical injection", "system reliability", "efficacy", "data analysis", "optimization"],
        conclusion_template="Chemical injection system performance must be monitored and analyzed to ensure reliability and optimize efficacy.",
        reasoning_framework="""
        1. Install monitoring equipment for chemical dosing, flow, and system status.
        2. Collect performance data and analyze for reliability and efficacy.
        3. Document monitoring procedures and train personnel.
        4. Review historical performance incidents and update monitoring strategy.
        5. Conduct periodic audits and optimize system based on data.
        6. Communicate monitoring requirements to operations and engineering teams.
        7. Ensure compliance with process and safety standards.
        8. Integrate monitoring into process control systems.
        9. Validate monitoring effectiveness via field testing.
        10. Update monitoring strategy based on performance feedback.
        """,
        key_factors=[
            "Monitoring equipment",
            "Data analysis",
            "Procedure documentation",
            "System reliability",
            "Audit and optimization"
        ],
        primary_authority=["Site Performance Monitoring Standards", "Manufacturer Monitoring Guides", "Process Engineering Standards"],
        burden_holder="Process Engineer",
        adversary_position="Operations questioning monitoring necessity",
        counter_arguments=[
            "Monitoring may not capture all performance issues",
            "Equipment may fail or require maintenance",
            "Cost concerns with monitoring installation"
        ],
        resolution_strategy="Optimize monitoring equipment, conduct audits, and update strategy.",
        entity_scope="OFE14 injection system performance",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Performance Monitoring Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Maintenance Program",
        keywords=["maintenance", "chemical injection", "program", "preventive", "corrective", "system reliability"],
        conclusion_template="Chemical injection systems must have a maintenance program to ensure reliability and prevent failures.",
        reasoning_framework="""
        1. Develop preventive and corrective maintenance schedules for injection equipment.
        2. Document maintenance procedures and train personnel.
        3. Monitor system reliability and update maintenance program based on incidents.
        4. Conduct periodic audits and optimize maintenance strategy.
        5. Communicate maintenance requirements to operations and engineering teams.
        6. Ensure compliance with safety and process standards.
        7. Integrate maintenance into site workflow.
        8. Validate maintenance effectiveness via field testing.
        9. Review historical maintenance incidents and update program.
        10. Audit maintenance records and optimize as needed.
        """,
        key_factors=[
            "Preventive and corrective schedules",
            "Procedure documentation",
            "System reliability",
            "Audit and optimization",
            "Personnel training"
        ],
        primary_authority=["Site Maintenance Standards", "Manufacturer Maintenance Guides", "Process Engineering Standards"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Operations questioning maintenance frequency",
        counter_arguments=[
            "Maintenance may interrupt injection operations",
            "Procedure may not prevent all failures",
            "Cost concerns with maintenance activities"
        ],
        resolution_strategy="Optimize maintenance frequency, validate effectiveness, and audit records.",
        entity_scope="OFE14 injection system maintenance",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Maintenance Program"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Calibration Protocol",
        keywords=["calibration", "chemical injection", "protocol", "pump accuracy", "dosing", "maintenance"],
        conclusion_template="Chemical injection system calibration must follow protocol to ensure pump accuracy and dosing reliability.",
        reasoning_framework="""
        1. Establish calibration frequency based on pump manufacturer recommendations.
        2. Document calibration procedures and train personnel.
        3. Monitor dosing accuracy and update calibration protocol based on incidents.
        4. Conduct periodic audits and optimize calibration strategy.
        5. Communicate calibration requirements to operations and maintenance teams.
        6. Ensure compliance with process and safety standards.
        7. Integrate calibration into maintenance workflow.
        8. Validate calibration effectiveness via field testing.
        9. Review historical calibration incidents and update protocol.
        10. Audit calibration records and optimize as needed.
        """,
        key_factors=[
            "Calibration frequency",
            "Procedure documentation",
            "Dosing accuracy",
            "Audit and optimization",
            "Personnel training"
        ],
        primary_authority=["Manufacturer Calibration Guides", "Site Maintenance Standards", "Process Engineering Standards"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Operations questioning calibration necessity",
        counter_arguments=[
            "Calibration may interrupt injection operations",
            "Procedure may not ensure dosing accuracy",
            "Cost concerns with calibration activities"
        ],
        resolution_strategy="Optimize calibration frequency, validate effectiveness, and audit records.",
        entity_scope="OFE14 injection system calibration",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manufacturer Calibration Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Documentation and Recordkeeping",
        keywords=["documentation", "recordkeeping", "chemical injection", "compliance", "audit", "system performance"],
        conclusion_template="Chemical injection systems must maintain documentation and records for compliance, audit, and performance analysis.",
        reasoning_framework="""
        1. Document all injection system procedures, maintenance, and performance data.
        2. Maintain records in accessible format for audit and compliance.
        3. Train personnel in documentation and recordkeeping requirements.
        4. Review regulatory requirements for documentation and update as needed.
        5. Conduct periodic audits and optimize recordkeeping strategy.
        6. Communicate documentation requirements to operations and engineering teams.
        7. Integrate recordkeeping into site workflow.
        8. Validate documentation effectiveness via audit and incident review.
        9. Review historical documentation incidents and update strategy.
        10. Audit records and optimize as needed.
        """,
        key_factors=[
            "Procedure documentation",
            "Recordkeeping format",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Documentation Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Operations Supervisor",
        adversary_position="Auditor questioning record completeness",
        counter_arguments=[
            "Records may not be complete or accessible",
            "Documentation may not meet regulatory requirements",
            "Personnel may lack training in recordkeeping"
        ],
        resolution_strategy="Conduct audits, update documentation, and train personnel.",
        entity_scope="OFE14 injection system documentation",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Documentation and Recordkeeping Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Training Program",
        keywords=["training", "chemical injection", "program", "personnel", "safety", "compliance"],
        conclusion_template="Chemical injection system personnel must be trained in operation, safety, and compliance requirements.",
        reasoning_framework="""
        1. Develop training program covering operation, safety, and compliance.
        2. Document training procedures and maintain records.
        3. Conduct periodic training sessions and update as regulations change.
        4. Review regulatory requirements for training and update program.
        5. Audit training effectiveness and optimize strategy.
        6. Communicate training requirements to operations and engineering teams.
        7. Integrate training into site workflow.
        8. Validate training effectiveness via audit and incident review.
        9. Review historical training incidents and update program.
        10. Audit training records and optimize as needed.
        """,
        key_factors=[
            "Training program development",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Training Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Training Coordinator",
        adversary_position="Operations questioning training necessity",
        counter_arguments=[
            "Training may not cover all operational scenarios",
            "Personnel may lack training records",
            "Training may not meet regulatory requirements"
        ],
        resolution_strategy="Conduct audits, update training program, and train personnel.",
        entity_scope="OFE14 injection system training",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Training Program"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Regulatory Compliance",
        keywords=["regulatory compliance", "chemical injection", "safety", "environmental", "audit", "documentation"],
        conclusion_template="Chemical injection systems must comply with all regulatory requirements for safety, environmental protection, and documentation.",
        reasoning_framework="""
        1. Review all applicable regulatory requirements for chemical injection systems.
        2. Document compliance procedures and maintain records.
        3. Train personnel in regulatory compliance requirements.
        4. Conduct periodic audits and update compliance strategy.
        5. Communicate compliance requirements to operations and engineering teams.
        6. Integrate compliance into site workflow.
        7. Validate compliance effectiveness via audit and incident review.
        8. Review historical compliance incidents and update strategy.
        9. Audit compliance records and optimize as needed.
        10. Update compliance procedures as regulations change.
        """,
        key_factors=[
            "Regulatory requirements review",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["EPA Regulations", "OSHA Standards", "Site Regulatory Compliance Standards"],
        burden_holder="Compliance Officer",
        adversary_position="Auditor questioning compliance effectiveness",
        counter_arguments=[
            "Compliance procedures may not cover all regulations",
            "Records may not be complete or accessible",
            "Personnel may lack training in compliance"
        ],
        resolution_strategy="Conduct audits, update compliance procedures, and train personnel.",
        entity_scope="OFE14 injection system regulatory compliance",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA and OSHA Regulatory Compliance Standards"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Environmental Impact Assessment",
        keywords=["environmental impact", "chemical injection", "assessment", "regulatory", "compliance", "documentation"],
        conclusion_template="Chemical injection systems must undergo environmental impact assessment and comply with all regulatory requirements.",
        reasoning_framework="""
        1. Conduct environmental impact assessment for chemical injection systems.
        2. Document assessment procedures and maintain records.
        3. Review regulatory requirements for environmental impact.
        4. Train personnel in environmental compliance requirements.
        5. Conduct periodic audits and update assessment strategy.
        6. Communicate assessment requirements to operations and engineering teams.
        7. Integrate assessment into site workflow.
        8. Validate assessment effectiveness via audit and incident review.
        9. Review historical environmental incidents and update strategy.
        10. Update assessment procedures as regulations change.
        """,
        key_factors=[
            "Environmental impact assessment",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["EPA Environmental Assessment Guidelines", "Site Environmental Standards", "Regulatory Requirements"],
        burden_holder="Environmental Engineer",
        adversary_position="Auditor questioning assessment effectiveness",
        counter_arguments=[
            "Assessment may not cover all environmental risks",
            "Records may not be complete or accessible",
            "Personnel may lack training in environmental compliance"
        ],
        resolution_strategy="Conduct audits, update assessment procedures, and train personnel.",
        entity_scope="OFE14 injection system environmental impact",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Environmental Impact Assessment Guidelines"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Incident Investigation Protocol",
        keywords=["incident investigation", "chemical injection", "protocol", "safety", "documentation", "audit"],
        conclusion_template="Chemical injection system incidents must be investigated according to protocol and documented for audit and compliance.",
        reasoning_framework="""
        1. Develop incident investigation protocol for chemical injection systems.
        2. Document investigation procedures and maintain records.
        3. Train personnel in incident investigation requirements.
        4. Conduct periodic audits and update investigation strategy.
        5. Communicate investigation requirements to operations and engineering teams.
        6. Integrate investigation into site workflow.
        7. Validate investigation effectiveness via audit and incident review.
        8. Review historical incident investigation incidents and update protocol.
        9. Audit investigation records and optimize as needed.
        10. Update investigation procedures as regulations change.
        """,
        key_factors=[
            "Incident investigation protocol",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Incident Investigation Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Safety Manager",
        adversary_position="Auditor questioning investigation completeness",
        counter_arguments=[
            "Investigation may not cover all incident scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in investigation"
        ],
        resolution_strategy="Conduct audits, update investigation protocol, and train personnel.",
        entity_scope="OFE14 injection system incident investigation",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Incident Investigation Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Change Management Procedure",
        keywords=["change management", "chemical injection", "procedure", "documentation", "audit", "compliance"],
        conclusion_template="Chemical injection system changes must follow change management procedure and be documented for audit and compliance.",
        reasoning_framework="""
        1. Develop change management procedure for chemical injection systems.
        2. Document change procedures and maintain records.
        3. Train personnel in change management requirements.
        4. Conduct periodic audits and update change management strategy.
        5. Communicate change management requirements to operations and engineering teams.
        6. Integrate change management into site workflow.
        7. Validate change management effectiveness via audit and incident review.
        8. Review historical change management incidents and update procedure.
        9. Audit change management records and optimize as needed.
        10. Update change management procedures as regulations change.
        """,
        key_factors=[
            "Change management procedure",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Change Management Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Operations Supervisor",
        adversary_position="Auditor questioning change management completeness",
        counter_arguments=[
            "Change management may not cover all change scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in change management"
        ],
        resolution_strategy="Conduct audits, update change management procedure, and train personnel.",
        entity_scope="OFE14 injection system change management",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Change Management Procedure"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Risk Assessment Protocol",
        keywords=["risk assessment", "chemical injection", "protocol", "safety", "documentation", "audit"],
        conclusion_template="Chemical injection system risks must be assessed according to protocol and documented for audit and compliance.",
        reasoning_framework="""
        1. Develop risk assessment protocol for chemical injection systems.
        2. Document risk assessment procedures and maintain records.
        3. Train personnel in risk assessment requirements.
        4. Conduct periodic audits and update risk assessment strategy.
        5. Communicate risk assessment requirements to operations and engineering teams.
        6. Integrate risk assessment into site workflow.
        7. Validate risk assessment effectiveness via audit and incident review.
        8. Review historical risk assessment incidents and update protocol.
        9. Audit risk assessment records and optimize as needed.
        10. Update risk assessment procedures as regulations change.
        """,
        key_factors=[
            "Risk assessment protocol",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Risk Assessment Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Safety Manager",
        adversary_position="Auditor questioning risk assessment completeness",
        counter_arguments=[
            "Risk assessment may not cover all risk scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in risk assessment"
        ],
        resolution_strategy="Conduct audits, update risk assessment protocol, and train personnel.",
        entity_scope="OFE14 injection system risk assessment",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Risk Assessment Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Continuous Improvement Program",
        keywords=["continuous improvement", "chemical injection", "program", "optimization", "audit", "documentation"],
        conclusion_template="Chemical injection systems must have a continuous improvement program for optimization, audit, and documentation.",
        reasoning_framework="""
        1. Develop continuous improvement program for chemical injection systems.
        2. Document improvement procedures and maintain records.
        3. Train personnel in continuous improvement requirements.
        4. Conduct periodic audits and update improvement strategy.
        5. Communicate improvement requirements to operations and engineering teams.
        6. Integrate improvement into site workflow.
        7. Validate improvement effectiveness via audit and incident review.
        8. Review historical improvement incidents and update program.
        9. Audit improvement records and optimize as needed.
        10. Update improvement procedures as regulations change.
        """,
        key_factors=[
            "Continuous improvement program",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Continuous Improvement Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Operations Supervisor",
        adversary_position="Auditor questioning improvement completeness",
        counter_arguments=[
            "Improvement program may not cover all optimization scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in continuous improvement"
        ],
        resolution_strategy="Conduct audits, update improvement program, and train personnel.",
        entity_scope="OFE14 injection system continuous improvement",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Continuous Improvement Program"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Stakeholder Communication Protocol",
        keywords=["stakeholder communication", "chemical injection", "protocol", "documentation", "audit", "compliance"],
        conclusion_template="Chemical injection system stakeholder communication must follow protocol and be documented for audit and compliance.",
        reasoning_framework="""
        1. Develop stakeholder communication protocol for chemical injection systems.
        2. Document communication procedures and maintain records.
        3. Train personnel in stakeholder communication requirements.
        4. Conduct periodic audits and update communication strategy.
        5. Communicate communication requirements to operations and engineering teams.
        6. Integrate communication into site workflow.
        7. Validate communication effectiveness via audit and incident review.
        8. Review historical communication incidents and update protocol.
        9. Audit communication records and optimize as needed.
        10. Update communication procedures as regulations change.
        """,
        key_factors=[
            "Stakeholder communication protocol",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Communication Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Operations Supervisor",
        adversary_position="Auditor questioning communication completeness",
        counter_arguments=[
            "Communication protocol may not cover all stakeholder scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in communication"
        ],
        resolution_strategy="Conduct audits, update communication protocol, and train personnel.",
        entity_scope="OFE14 injection system stakeholder communication",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Stakeholder Communication Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Procurement Procedure",
        keywords=["procurement", "chemical injection", "procedure", "vendor selection", "documentation", "audit"],
        conclusion_template="Chemical injection system procurement must follow procedure for vendor selection, documentation, and audit.",
        reasoning_framework="""
        1. Develop procurement procedure for chemical injection systems.
        2. Document procurement procedures and maintain records.
        3. Train personnel in procurement requirements.
        4. Conduct periodic audits and update procurement strategy.
        5. Communicate procurement requirements to operations and engineering teams.
        6. Integrate procurement into site workflow.
        7. Validate procurement effectiveness via audit and incident review.
        8. Review historical procurement incidents and update procedure.
        9. Audit procurement records and optimize as needed.
        10. Update procurement procedures as regulations change.
        """,
        key_factors=[
            "Procurement procedure",
            "Vendor selection",
            "Documentation and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Procurement Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Procurement Officer",
        adversary_position="Auditor questioning procurement completeness",
        counter_arguments=[
            "Procurement procedure may not cover all vendor scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in procurement"
        ],
        resolution_strategy="Conduct audits, update procurement procedure, and train personnel.",
        entity_scope="OFE14 injection system procurement",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Procurement Procedure"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Vendor Qualification Protocol",
        keywords=["vendor qualification", "chemical injection", "protocol", "documentation", "audit", "compliance"],
        conclusion_template="Chemical injection system vendors must be qualified according to protocol and documented for audit and compliance.",
        reasoning_framework="""
        1. Develop vendor qualification protocol for chemical injection systems.
        2. Document qualification procedures and maintain records.
        3. Train personnel in vendor qualification requirements.
        4. Conduct periodic audits and update qualification strategy.
        5. Communicate qualification requirements to operations and engineering teams.
        6. Integrate qualification into site workflow.
        7. Validate qualification effectiveness via audit and incident review.
        8. Review historical qualification incidents and update protocol.
        9. Audit qualification records and optimize as needed.
        10. Update qualification procedures as regulations change.
        """,
        key_factors=[
            "Vendor qualification protocol",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Vendor Qualification Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Procurement Officer",
        adversary_position="Auditor questioning qualification completeness",
        counter_arguments=[
            "Qualification protocol may not cover all vendor scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in qualification"
        ],
        resolution_strategy="Conduct audits, update qualification protocol, and train personnel.",
        entity_scope="OFE14 injection system vendor qualification",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Vendor Qualification Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Cost Optimization Strategy",
        keywords=["cost optimization", "chemical injection", "strategy", "procurement", "operation", "audit"],
        conclusion_template="Chemical injection system costs must be optimized via procurement, operation, and audit strategies.",
        reasoning_framework="""
        1. Develop cost optimization strategy for chemical injection systems.
        2. Document cost optimization procedures and maintain records.
        3. Train personnel in cost optimization requirements.
        4. Conduct periodic audits and update optimization strategy.
        5. Communicate optimization requirements to operations and engineering teams.
        6. Integrate optimization into site workflow.
        7. Validate optimization effectiveness via audit and incident review.
        8. Review historical optimization incidents and update strategy.
        9. Audit optimization records and optimize as needed.
        10. Update optimization procedures as regulations change.
        """,
        key_factors=[
            "Cost optimization strategy",
            "Procurement and operation",
            "Documentation and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Cost Optimization Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Operations Supervisor",
        adversary_position="Auditor questioning optimization completeness",
        counter_arguments=[
            "Optimization strategy may not cover all cost scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in optimization"
        ],
        resolution_strategy="Conduct audits, update optimization strategy, and train personnel.",
        entity_scope="OFE14 injection system cost optimization",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Cost Optimization Strategy"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Data Management Protocol",
        keywords=["data management", "chemical injection", "protocol", "documentation", "audit", "compliance"],
        conclusion_template="Chemical injection system data must be managed according to protocol and documented for audit and compliance.",
        reasoning_framework="""
        1. Develop data management protocol for chemical injection systems.
        2. Document data management procedures and maintain records.
        3. Train personnel in data management requirements.
        4. Conduct periodic audits and update data management strategy.
        5. Communicate data management requirements to operations and engineering teams.
        6. Integrate data management into site workflow.
        7. Validate data management effectiveness via audit and incident review.
        8. Review historical data management incidents and update protocol.
        9. Audit data management records and optimize as needed.
        10. Update data management procedures as regulations change.
        """,
        key_factors=[
            "Data management protocol",
            "Procedure documentation",
            "Compliance and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Data Management Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Data Manager",
        adversary_position="Auditor questioning data management completeness",
        counter_arguments=[
            "Data management protocol may not cover all data scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in data management"
        ],
        resolution_strategy="Conduct audits, update data management protocol, and train personnel.",
        entity_scope="OFE14 injection system data management",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Data Management Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Cybersecurity Protocol",
        keywords=["cybersecurity", "chemical injection", "protocol", "system integration", "audit", "compliance"],
        conclusion_template="Chemical injection system cybersecurity must follow protocol for system integration, audit, and compliance.",
        reasoning_framework="""
        1. Develop cybersecurity protocol for chemical injection system integration.
        2. Document cybersecurity procedures and maintain records.
        3. Train personnel in cybersecurity requirements.
        4. Conduct periodic audits and update cybersecurity strategy.
        5. Communicate cybersecurity requirements to operations and engineering teams.
        6. Integrate cybersecurity into site workflow.
        7. Validate cybersecurity effectiveness via audit and incident review.
        8. Review historical cybersecurity incidents and update protocol.
        9. Audit cybersecurity records and optimize as needed.
        10. Update cybersecurity procedures as regulations change.
        """,
        key_factors=[
            "Cybersecurity protocol",
            "System integration",
            "Documentation and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["ISA/IEC 62443", "Site Cybersecurity Standards", "Process Engineering Standards"],
        burden_holder="IT Security Manager",
        adversary_position="Auditor questioning cybersecurity completeness",
        counter_arguments=[
            "Cybersecurity protocol may not cover all integration scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in cybersecurity"
        ],
        resolution_strategy="Conduct audits, update cybersecurity protocol, and train personnel.",
        entity_scope="OFE14 injection system cybersecurity",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA/IEC 62443 Cybersecurity Standard"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Sustainability Assessment",
        keywords=["sustainability", "chemical injection", "assessment", "environmental", "audit", "optimization"],
        conclusion_template="Chemical injection system sustainability must be assessed and optimized for environmental and operational performance.",
        reasoning_framework="""
        1. Develop sustainability assessment protocol for chemical injection systems.
        2. Document assessment procedures and maintain records.
        3. Train personnel in sustainability requirements.
        4. Conduct periodic audits and update sustainability strategy.
        5. Communicate sustainability requirements to operations and engineering teams.
        6. Integrate sustainability into site workflow.
        7. Validate sustainability effectiveness via audit and incident review.
        8. Review historical sustainability incidents and update protocol.
        9. Audit sustainability records and optimize as needed.
        10. Update sustainability procedures as regulations change.
        """,
        key_factors=[
            "Sustainability assessment protocol",
            "Environmental and operational performance",
            "Documentation and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Sustainability Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Sustainability Officer",
        adversary_position="Auditor questioning sustainability completeness",
        counter_arguments=[
            "Sustainability protocol may not cover all assessment scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in sustainability"
        ],
        resolution_strategy="Conduct audits, update sustainability protocol, and train personnel.",
        entity_scope="OFE14 injection system sustainability",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Sustainability Assessment Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Innovation Management Procedure",
        keywords=["innovation management", "chemical injection", "procedure", "optimization", "audit", "documentation"],
        conclusion_template="Chemical injection system innovation must be managed according to procedure for optimization, audit, and documentation.",
        reasoning_framework="""
        1. Develop innovation management procedure for chemical injection systems.
        2. Document innovation procedures and maintain records.
        3. Train personnel in innovation management requirements.
        4. Conduct periodic audits and update innovation strategy.
        5. Communicate innovation requirements to operations and engineering teams.
        6. Integrate innovation management into site workflow.
        7. Validate innovation effectiveness via audit and incident review.
        8. Review historical innovation incidents and update procedure.
        9. Audit innovation records and optimize as needed.
        10. Update innovation procedures as regulations change.
        """,
        key_factors=[
            "Innovation management procedure",
            "Optimization",
            "Documentation and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Innovation Management Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Innovation Manager",
        adversary_position="Auditor questioning innovation completeness",
        counter_arguments=[
            "Innovation management may not cover all optimization scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in innovation management"
        ],
        resolution_strategy="Conduct audits, update innovation management procedure, and train personnel.",
        entity_scope="OFE14 injection system innovation management",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Innovation Management Procedure"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Lifecycle Management Protocol",
        keywords=["lifecycle management", "chemical injection", "protocol", "optimization", "audit", "documentation"],
        conclusion_template="Chemical injection system lifecycle must be managed according to protocol for optimization, audit, and documentation.",
        reasoning_framework="""
        1. Develop lifecycle management protocol for chemical injection systems.
        2. Document lifecycle procedures and maintain records.
        3. Train personnel in lifecycle management requirements.
        4. Conduct periodic audits and update lifecycle strategy.
        5. Communicate lifecycle management requirements to operations and engineering teams.
        6. Integrate lifecycle management into site workflow.
        7. Validate lifecycle effectiveness via audit and incident review.
        8. Review historical lifecycle incidents and update protocol.
        9. Audit lifecycle records and optimize as needed.
        10. Update lifecycle procedures as regulations change.
        """,
        key_factors=[
            "Lifecycle management protocol",
            "Optimization",
            "Documentation and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Lifecycle Management Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Lifecycle Manager",
        adversary_position="Auditor questioning lifecycle completeness",
        counter_arguments=[
            "Lifecycle management may not cover all optimization scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in lifecycle management"
        ],
        resolution_strategy="Conduct audits, update lifecycle management protocol, and train personnel.",
        entity_scope="OFE14 injection system lifecycle management",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Lifecycle Management Protocol"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Stakeholder Engagement Strategy",
        keywords=["stakeholder engagement", "chemical injection", "strategy", "communication", "audit", "optimization"],
        conclusion_template="Chemical injection system stakeholder engagement must follow strategy for communication, audit, and optimization.",
        reasoning_framework="""
        1. Develop stakeholder engagement strategy for chemical injection systems.
        2. Document engagement procedures and maintain records.
        3. Train personnel in stakeholder engagement requirements.
        4. Conduct periodic audits and update engagement strategy.
        5. Communicate engagement requirements to operations and engineering teams.
        6. Integrate engagement into site workflow.
        7. Validate engagement effectiveness via audit and incident review.
        8. Review historical engagement incidents and update strategy.
        9. Audit engagement records and optimize as needed.
        10. Update engagement procedures as regulations change.
        """,
        key_factors=[
            "Stakeholder engagement strategy",
            "Communication",
            "Documentation and audit",
            "Personnel training",
            "Audit and optimization"
        ],
        primary_authority=["Site Stakeholder Engagement Standards", "Regulatory Requirements", "Process Engineering Standards"],
        burden_holder="Stakeholder Engagement Manager",
        adversary_position="Auditor questioning engagement completeness",
        counter_arguments=[
            "Engagement strategy may not cover all communication scenarios",
            "Records may not be complete or accessible",
            "Personnel may lack training in stakeholder engagement"
        ],
        resolution_strategy="Conduct audits, update engagement strategy, and train personnel.",
        entity_scope="OFE14 injection system stakeholder engagement",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Site Stakeholder Engagement Strategy"
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