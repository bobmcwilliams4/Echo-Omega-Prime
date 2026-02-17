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
        topic="CT String Fatigue Life Tracking",
        keywords=["fatigue", "life", "tracking", "coil", "tubing", "CT", "string", "cycles", "damage", "monitoring"],
        conclusion_template="CT string fatigue life must be tracked using real-time cycle counting and validated against manufacturer thresholds to prevent premature failure.",
        reasoning_framework="""
        Fatigue life tracking for coiled tubing strings is essential to ensure operational safety and prevent catastrophic failures. The process involves monitoring the number of bend cycles experienced by the CT string, quantifying accumulated damage using Miner's Rule, and comparing the total fatigue against manufacturer-provided fatigue curves. Real-time software tools (e.g., Schlumberger CoilLife, NOV Fatigue Tracker) are used to log cycles and calculate remaining life. Operators must account for operational variables such as bend radius, tension, and pressure, as these significantly affect fatigue accumulation. The doctrine mandates periodic validation of software logs against manual records and requires that CT strings be retired or re-spliced when fatigue thresholds are reached. The burden of proof lies with the operator to demonstrate compliance with fatigue management protocols. Adversaries may argue for extended use based on visual inspection, but empirical fatigue data supersedes subjective assessments. Resolution involves strict adherence to manufacturer guidelines, real-time monitoring, and periodic audits.
        """,
        key_factors=[
            "Bend radius",
            "Cycle count",
            "Tension and pressure",
            "Manufacturer fatigue curves",
            "Real-time monitoring",
            "Software validation"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger CoilLife Documentation",
            "NOV Fatigue Tracker Manual"
        ],
        burden_holder="CT Operator",
        adversary_position="Visual inspection suffices for fatigue assessment; software tracking is unnecessary.",
        counter_arguments=[
            "Visual inspection cannot detect micro-crack propagation.",
            "Empirical cycle counting provides objective fatigue assessment.",
            "Manufacturer guidelines require cycle-based tracking."
        ],
        resolution_strategy="Strict compliance with software-based fatigue tracking and periodic audits.",
        entity_scope="CT Operations",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 6.2"
    ),
    DoctrineBlock(
        topic="BHA Design for CT Drilling Applications",
        keywords=["BHA", "bottom hole assembly", "design", "CT", "drilling", "vibration", "tool selection", "motor", "stabilizer"],
        conclusion_template="BHA design for CT drilling must optimize for vibration mitigation, directional control, and tool compatibility, following industry standards and site-specific requirements.",
        reasoning_framework="""
        The design of the bottom hole assembly (BHA) for coiled tubing drilling operations is governed by the need to minimize vibration, maximize directional control, and ensure compatibility with downhole tools. The doctrine requires selection of appropriate drilling motors, stabilizers, and measurement-while-drilling (MWD) tools. Vibration mitigation is achieved through proper placement of stabilizers and use of shock subs. The BHA must be tailored to the well profile, formation properties, and operational objectives. The operator is responsible for validating BHA configuration against engineering models and manufacturer recommendations. Adversaries may propose alternative configurations based on cost or tool availability, but safety and performance take precedence. Resolution involves engineering review, simulation, and adherence to API and manufacturer standards.
        """,
        key_factors=[
            "Vibration mitigation",
            "Directional control",
            "Tool compatibility",
            "Formation properties",
            "Engineering validation"
        ],
        primary_authority=[
            "API RP 7G",
            "Schlumberger BHA Design Manual",
            "NOV CT Drilling Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Alternative BHA configurations are acceptable if cost-effective.",
        counter_arguments=[
            "Cost savings cannot compromise safety or performance.",
            "Engineering validation is mandatory.",
            "Manufacturer recommendations must be followed."
        ],
        resolution_strategy="Engineering review and simulation; adherence to API and manufacturer standards.",
        entity_scope="CT Drilling",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 7G Section 4.1"
    ),
    DoctrineBlock(
        topic="Injector Head Operation and Gripper Block Maintenance",
        keywords=["injector head", "operation", "gripper block", "maintenance", "CT", "lubrication", "inspection"],
        conclusion_template="Injector head operation requires routine gripper block maintenance, including lubrication, inspection, and replacement per manufacturer schedules.",
        reasoning_framework="""
        The injector head is a critical component in CT operations, responsible for driving the tubing into and out of the wellbore. Gripper blocks must be regularly inspected for wear, lubricated, and replaced according to manufacturer maintenance schedules. Failure to maintain gripper blocks can result in slippage, tubing damage, and operational downtime. The doctrine mandates daily visual inspections, weekly lubrication, and monthly replacement checks. Operators must document all maintenance activities and retain records for regulatory compliance. Adversaries may argue for extended maintenance intervals, but empirical evidence shows increased risk of failure with lax maintenance. Resolution involves strict adherence to maintenance schedules and documentation.
        """,
        key_factors=[
            "Gripper block wear",
            "Lubrication frequency",
            "Inspection intervals",
            "Manufacturer schedules",
            "Documentation"
        ],
        primary_authority=[
            "NOV CT Injector Manual",
            "API RP 5C7",
            "Schlumberger Maintenance Guidelines"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Extended maintenance intervals are acceptable if no visible wear is present.",
        counter_arguments=[
            "Invisible wear can lead to sudden failure.",
            "Manufacturer schedules are based on empirical data.",
            "Regulatory compliance requires documentation."
        ],
        resolution_strategy="Routine maintenance and documentation; adherence to manufacturer schedules.",
        entity_scope="Surface Equipment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NOV CT Injector Manual Section 3.2"
    ),
    DoctrineBlock(
        topic="CT BOP Configuration and Stripper/Packer Operation",
        keywords=["CT", "BOP", "configuration", "stripper", "packer", "operation", "pressure control", "well control"],
        conclusion_template="CT BOP configuration must ensure proper pressure control, with stripper and packer operation validated before each run.",
        reasoning_framework="""
        Coiled tubing blowout preventer (BOP) configuration is fundamental to well control during CT operations. The doctrine requires that BOPs be configured according to well pressure, tubing size, and operational objectives. Stripper and packer elements must be tested for integrity before each run, and pressure tests documented. Operators must ensure redundancy in pressure control and have contingency plans for element failure. Adversaries may argue that testing is unnecessary for short runs, but regulatory requirements mandate testing before every operation. Resolution involves compliance with API standards, manufacturer guidelines, and regulatory requirements.
        """,
        key_factors=[
            "Pressure control",
            "BOP configuration",
            "Stripper/packer integrity",
            "Testing frequency",
            "Documentation"
        ],
        primary_authority=[
            "API RP 16ST",
            "Schlumberger CT BOP Manual",
            "NOV Pressure Control Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Testing is unnecessary for short runs.",
        counter_arguments=[
            "Regulatory requirements mandate testing.",
            "Short runs can still experience pressure anomalies.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Testing before every run; documentation and compliance with API standards.",
        entity_scope="Pressure Control",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 16ST Section 5.1"
    ),
    DoctrineBlock(
        topic="Reel Capacity Calculations and CT String Length Management",
        keywords=["reel", "capacity", "calculations", "CT", "string", "length", "management", "spooling", "diameter"],
        conclusion_template="Reel capacity calculations must be performed before each operation to ensure CT string length is adequate and does not exceed reel limits.",
        reasoning_framework="""
        Proper management of CT string length and reel capacity is critical to prevent overloading and ensure operational efficiency. The doctrine requires calculation of reel capacity based on tubing diameter, wall thickness, and reel dimensions. Operators must verify that the planned CT string length does not exceed reel capacity, accounting for spooling efficiency and residual tubing. Adversaries may argue that conservative estimates are unnecessary, but exceeding reel capacity can result in equipment damage and safety hazards. Resolution involves pre-operation calculations, validation against manufacturer specifications, and documentation.
        """,
        key_factors=[
            "Tubing diameter",
            "Wall thickness",
            "Reel dimensions",
            "Spooling efficiency",
            "Residual tubing"
        ],
        primary_authority=[
            "NOV Reel Capacity Calculator",
            "API RP 5C7",
            "Schlumberger CT Reel Manual"
        ],
        burden_holder="CT Engineer",
        adversary_position="Conservative estimates are unnecessary; actual spooling can be used.",
        counter_arguments=[
            "Exceeding reel capacity can cause equipment damage.",
            "Manufacturer specifications must be followed.",
            "Pre-operation calculations prevent operational delays."
        ],
        resolution_strategy="Pre-operation calculations and validation against manufacturer specifications.",
        entity_scope="CT Logistics",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NOV Reel Capacity Calculator User Guide"
    ),
    DoctrineBlock(
        topic="CT Tubing OD Selection and Grade Specification",
        keywords=["CT", "tubing", "OD", "selection", "grade", "specification", "material", "strength"],
        conclusion_template="CT tubing OD and grade must be selected based on well requirements, operational objectives, and manufacturer recommendations.",
        reasoning_framework="""
        Selection of CT tubing outside diameter (OD) and grade is governed by wellbore requirements, operational objectives, and material strength. The doctrine mandates evaluation of formation pressure, required flow rates, and mechanical properties. Operators must consult manufacturer recommendations and API standards to ensure tubing selection meets operational and safety requirements. Adversaries may propose alternative grades for cost savings, but safety and performance take precedence. Resolution involves engineering review, adherence to standards, and documentation.
        """,
        key_factors=[
            "Formation pressure",
            "Flow rate requirements",
            "Material strength",
            "Manufacturer recommendations",
            "API standards"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Tubing Selection Guide",
            "NOV CT Tubing Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Alternative grades are acceptable for cost savings.",
        counter_arguments=[
            "Safety and performance cannot be compromised.",
            "Manufacturer recommendations must be followed.",
            "API standards are mandatory."
        ],
        resolution_strategy="Engineering review and adherence to standards.",
        entity_scope="CT Design",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.1"
    ),
    DoctrineBlock(
        topic="Nitrogen Pumping Through CT for Underbalanced Operations",
        keywords=["nitrogen", "pumping", "CT", "underbalanced", "operations", "pressure", "flow", "safety"],
        conclusion_template="Nitrogen pumping through CT must be performed under strict safety protocols, with flow rates and pressures validated against well requirements.",
        reasoning_framework="""
        Nitrogen pumping through coiled tubing is used for underbalanced operations to minimize formation damage and enhance well productivity. The doctrine requires calculation of nitrogen flow rates and pressures based on well parameters and operational objectives. Safety protocols must be strictly followed, including monitoring for leaks, proper venting, and emergency shut-down procedures. Operators must document all nitrogen pumping activities and validate against well requirements. Adversaries may argue for relaxed safety protocols, but regulatory requirements mandate strict adherence. Resolution involves compliance with safety standards, engineering validation, and documentation.
        """,
        key_factors=[
            "Flow rate calculation",
            "Pressure validation",
            "Safety protocols",
            "Leak monitoring",
            "Emergency procedures"
        ],
        primary_authority=[
            "API RP 17A",
            "Schlumberger Nitrogen Pumping Manual",
            "NOV CT Operations Handbook"
        ],
        burden_holder="CT Operator",
        adversary_position="Relaxed safety protocols are acceptable for short operations.",
        counter_arguments=[
            "Regulatory requirements mandate strict safety protocols.",
            "Short operations can still pose safety risks.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Strict adherence to safety protocols and documentation.",
        entity_scope="CT Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 17A Section 8.2"
    ),
    DoctrineBlock(
        topic="CT Fracturing Operations and Proppant Limitations",
        keywords=["CT", "fracturing", "operations", "proppant", "limitations", "flow", "pressure", "screen-out"],
        conclusion_template="CT fracturing operations must account for proppant limitations, flow rates, and screen-out risks, with real-time monitoring and contingency planning.",
        reasoning_framework="""
        Fracturing operations using coiled tubing require careful management of proppant concentrations, flow rates, and pressure to prevent screen-outs and equipment damage. The doctrine mandates real-time monitoring of proppant delivery, validation against fracture design, and contingency planning for screen-out events. Operators must document all fracturing activities and adhere to manufacturer and API guidelines. Adversaries may argue for increased proppant concentrations to enhance productivity, but operational risks must be mitigated. Resolution involves engineering review, real-time monitoring, and adherence to standards.
        """,
        key_factors=[
            "Proppant concentration",
            "Flow rate",
            "Pressure management",
            "Screen-out risk",
            "Real-time monitoring"
        ],
        primary_authority=[
            "API RP 19B",
            "Schlumberger Fracturing Manual",
            "NOV CT Fracturing Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Increased proppant concentrations are acceptable for enhanced productivity.",
        counter_arguments=[
            "Screen-out risk increases with higher concentrations.",
            "Equipment damage can occur.",
            "Manufacturer and API guidelines must be followed."
        ],
        resolution_strategy="Real-time monitoring and adherence to guidelines.",
        entity_scope="CT Fracturing",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 5.3"
    ),
    DoctrineBlock(
        topic="Real-Time Depth Tracking and Weight Indicator Monitoring",
        keywords=["real-time", "depth", "tracking", "weight", "indicator", "monitoring", "CT", "operations"],
        conclusion_template="Real-time depth tracking and weight indicator monitoring are mandatory for all CT operations to ensure operational safety and accuracy.",
        reasoning_framework="""
        Accurate real-time depth tracking and weight indicator monitoring are essential for safe and efficient CT operations. The doctrine requires use of calibrated depth tracking systems and weight indicators, with periodic validation against manual measurements. Operators must document all readings and investigate discrepancies. Adversaries may argue that manual measurements suffice, but real-time systems provide greater accuracy and safety. Resolution involves use of real-time systems, periodic validation, and documentation.
        """,
        key_factors=[
            "Calibration",
            "Real-time systems",
            "Manual validation",
            "Documentation",
            "Discrepancy investigation"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Depth Tracking Manual",
            "NOV Weight Indicator Handbook"
        ],
        burden_holder="CT Operator",
        adversary_position="Manual measurements are sufficient for depth and weight tracking.",
        counter_arguments=[
            "Real-time systems provide greater accuracy.",
            "Safety is enhanced with real-time monitoring.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Use of real-time systems and periodic validation.",
        entity_scope="CT Operations",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 7.1"
    ),
    DoctrineBlock(
        topic="Wellbore Cleanout Operations and Circulation Design",
        keywords=["wellbore", "cleanout", "operations", "circulation", "design", "CT", "fluid", "debris", "removal"],
        conclusion_template="Wellbore cleanout operations must be designed with optimal circulation rates and fluid selection to maximize debris removal and minimize formation damage.",
        reasoning_framework="""
        Wellbore cleanout operations using CT require careful design of circulation rates and fluid selection to maximize debris removal and minimize formation damage. The doctrine mandates calculation of optimal circulation rates based on wellbore geometry, debris type, and formation properties. Fluid selection must consider compatibility with formation and debris. Operators must document all cleanout activities and validate against engineering models. Adversaries may argue for increased circulation rates to enhance debris removal, but formation damage risks must be mitigated. Resolution involves engineering review, real-time monitoring, and adherence to standards.
        """,
        key_factors=[
            "Circulation rate",
            "Fluid selection",
            "Debris type",
            "Formation properties",
            "Engineering validation"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Cleanout Manual",
            "NOV CT Operations Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Increased circulation rates are acceptable for enhanced debris removal.",
        counter_arguments=[
            "Formation damage risk increases with higher rates.",
            "Fluid compatibility must be ensured.",
            "Engineering validation is required."
        ],
        resolution_strategy="Engineering review and real-time monitoring.",
        entity_scope="CT Cleanout",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 8.1"
    ),
    DoctrineBlock(
        topic="CT Fishing Operations and Stuck Pipe Recovery",
        keywords=["CT", "fishing", "operations", "stuck pipe", "recovery", "tool", "selection", "procedure"],
        conclusion_template="CT fishing operations require selection of appropriate tools and adherence to recovery procedures validated against engineering models.",
        reasoning_framework="""
        Fishing operations using coiled tubing involve recovery of stuck pipe and downhole tools. The doctrine mandates selection of appropriate fishing tools based on stuck pipe location, debris type, and wellbore geometry. Recovery procedures must be validated against engineering models and manufacturer recommendations. Operators must document all fishing activities and adhere to API and manufacturer guidelines. Adversaries may argue for expedited procedures, but safety and recovery success take precedence. Resolution involves engineering review, tool selection, and adherence to procedures.
        """,
        key_factors=[
            "Tool selection",
            "Stuck pipe location",
            "Debris type",
            "Wellbore geometry",
            "Procedure validation"
        ],
        primary_authority=[
            "API RP 10F",
            "Schlumberger Fishing Manual",
            "NOV CT Fishing Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Expedited procedures are acceptable for fishing operations.",
        counter_arguments=[
            "Safety and recovery success take precedence.",
            "Engineering validation is required.",
            "Manufacturer guidelines must be followed."
        ],
        resolution_strategy="Engineering review and adherence to procedures.",
        entity_scope="CT Fishing",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 10F Section 4.2"
    ),
    DoctrineBlock(
        topic="CT Power Pack Hydraulic System and Preventive Maintenance",
        keywords=["CT", "power pack", "hydraulic system", "preventive maintenance", "inspection", "fluid", "pressure"],
        conclusion_template="CT power pack hydraulic systems require routine preventive maintenance, including fluid inspection, pressure validation, and component replacement per manufacturer schedules.",
        reasoning_framework="""
        The hydraulic system of the CT power pack is critical for safe and efficient operations. The doctrine mandates routine preventive maintenance, including inspection of hydraulic fluid levels, pressure validation, and replacement of components according to manufacturer schedules. Operators must document all maintenance activities and retain records for regulatory compliance. Adversaries may argue for extended maintenance intervals, but empirical evidence shows increased risk of failure with lax maintenance. Resolution involves strict adherence to maintenance schedules and documentation.
        """,
        key_factors=[
            "Fluid inspection",
            "Pressure validation",
            "Component replacement",
            "Manufacturer schedules",
            "Documentation"
        ],
        primary_authority=[
            "NOV Power Pack Manual",
            "API RP 5C7",
            "Schlumberger Maintenance Guidelines"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Extended maintenance intervals are acceptable if no visible issues are present.",
        counter_arguments=[
            "Invisible issues can lead to sudden failure.",
            "Manufacturer schedules are based on empirical data.",
            "Regulatory compliance requires documentation."
        ],
        resolution_strategy="Routine maintenance and documentation; adherence to manufacturer schedules.",
        entity_scope="Surface Equipment",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NOV Power Pack Manual Section 2.3"
    ),
    DoctrineBlock(
        topic="CT Fatigue Modeling Using Schlumberger CoilLife and NOV Software",
        keywords=["CT", "fatigue", "modeling", "Schlumberger", "CoilLife", "NOV", "software", "cycle counting"],
        conclusion_template="CT fatigue modeling must utilize validated software tools (CoilLife, NOV Fatigue Tracker) for cycle counting and damage assessment, with periodic calibration against manufacturer data.",
        reasoning_framework="""
        Fatigue modeling for coiled tubing strings is performed using validated software tools such as Schlumberger CoilLife and NOV Fatigue Tracker. The doctrine requires real-time cycle counting, damage assessment, and periodic calibration of software outputs against manufacturer-provided fatigue curves. Operators must document all modeling activities and validate results against empirical data. Adversaries may argue for manual calculations, but software tools provide greater accuracy and efficiency. Resolution involves use of validated software, periodic calibration, and documentation.
        """,
        key_factors=[
            "Software validation",
            "Cycle counting",
            "Damage assessment",
            "Calibration",
            "Documentation"
        ],
        primary_authority=[
            "Schlumberger CoilLife Documentation",
            "NOV Fatigue Tracker Manual",
            "API RP 5C7"
        ],
        burden_holder="CT Engineer",
        adversary_position="Manual calculations are sufficient for fatigue modeling.",
        counter_arguments=[
            "Software tools provide greater accuracy and efficiency.",
            "Periodic calibration ensures reliability.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Use of validated software and periodic calibration.",
        entity_scope="CT Operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Schlumberger CoilLife Documentation Section 4.1"
    ),
    DoctrineBlock(
        topic="Surface Equipment Layout and Rig-Up Safety",
        keywords=["surface equipment", "layout", "rig-up", "safety", "CT", "operations", "hazard", "assessment"],
        conclusion_template="Surface equipment layout and rig-up must be designed for optimal safety, with hazard assessments and compliance with regulatory standards.",
        reasoning_framework="""
        Proper layout of surface equipment and rig-up procedures are essential for safe CT operations. The doctrine mandates hazard assessments, compliance with regulatory standards, and documentation of rig-up activities. Operators must ensure clear access, proper spacing, and secure placement of all equipment. Adversaries may argue for expedited rig-up, but safety and compliance take precedence. Resolution involves hazard assessments, engineering review, and adherence to standards.
        """,
        key_factors=[
            "Hazard assessment",
            "Regulatory compliance",
            "Equipment spacing",
            "Access",
            "Documentation"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Rig-Up Manual",
            "NOV Surface Equipment Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Expedited rig-up is acceptable if no hazards are visible.",
        counter_arguments=[
            "Invisible hazards can pose risks.",
            "Regulatory compliance is mandatory.",
            "Documentation is required."
        ],
        resolution_strategy="Hazard assessments and adherence to standards.",
        entity_scope="Surface Operations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 9.1"
    ),
    DoctrineBlock(
        topic="CT Cement Squeeze Operations",
        keywords=["CT", "cement", "squeeze", "operations", "pressure", "fluid", "placement", "validation"],
        conclusion_template="CT cement squeeze operations require precise pressure control, fluid placement validation, and documentation of all activities.",
        reasoning_framework="""
        Cement squeeze operations using CT require precise pressure control and validation of fluid placement. The doctrine mandates calculation of squeeze pressures, monitoring of cement placement, and documentation of all activities. Operators must validate cement placement using pressure charts and post-operation logs. Adversaries may argue for expedited procedures, but proper validation is essential for long-term well integrity. Resolution involves engineering review, real-time monitoring, and documentation.
        """,
        key_factors=[
            "Pressure control",
            "Fluid placement validation",
            "Documentation",
            "Engineering review",
            "Post-operation logs"
        ],
        primary_authority=[
            "API RP 10F",
            "Schlumberger Cementing Manual",
            "NOV CT Cement Squeeze Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Expedited procedures are acceptable for cement squeeze operations.",
        counter_arguments=[
            "Proper validation is essential for well integrity.",
            "Documentation is required for compliance.",
            "Engineering review ensures success."
        ],
        resolution_strategy="Engineering review and real-time monitoring.",
        entity_scope="CT Cementing",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 10F Section 5.1"
    ),
    DoctrineBlock(
        topic="CT Plug Drill-Out and Composite Frac Plug Milling",
        keywords=["CT", "plug", "drill-out", "composite", "frac plug", "milling", "tool selection", "procedure"],
        conclusion_template="CT plug drill-out and composite frac plug milling require selection of appropriate tools and adherence to validated procedures.",
        reasoning_framework="""
        Plug drill-out and composite frac plug milling using CT require selection of appropriate milling tools and adherence to validated procedures. The doctrine mandates engineering review of tool selection, validation against wellbore geometry, and documentation of all activities. Operators must monitor milling progress and adjust procedures as necessary. Adversaries may argue for expedited procedures, but safety and success take precedence. Resolution involves engineering review, tool selection, and adherence to procedures.
        """,
        key_factors=[
            "Tool selection",
            "Wellbore geometry",
            "Procedure validation",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "API RP 10F",
            "Schlumberger Plug Drill-Out Manual",
            "NOV CT Plug Milling Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Expedited procedures are acceptable for plug drill-out operations.",
        counter_arguments=[
            "Safety and success take precedence.",
            "Engineering validation is required.",
            "Documentation is necessary."
        ],
        resolution_strategy="Engineering review and adherence to procedures.",
        entity_scope="CT Plug Milling",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 10F Section 6.1"
    ),
    DoctrineBlock(
        topic="Flowback Operations Through CT and Production Testing",
        keywords=["flowback", "operations", "CT", "production", "testing", "pressure", "fluid", "monitoring"],
        conclusion_template="Flowback operations through CT require real-time monitoring of pressure and fluid rates, with documentation and validation against production testing objectives.",
        reasoning_framework="""
        Flowback operations using CT require real-time monitoring of pressure and fluid rates to ensure safety and achieve production testing objectives. The doctrine mandates use of calibrated monitoring systems, documentation of all activities, and validation against production objectives. Operators must investigate discrepancies and adjust procedures as necessary. Adversaries may argue for manual monitoring, but real-time systems provide greater accuracy and safety. Resolution involves use of real-time systems, periodic validation, and documentation.
        """,
        key_factors=[
            "Pressure monitoring",
            "Fluid rate monitoring",
            "Calibration",
            "Documentation",
            "Production objectives"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Flowback Manual",
            "NOV CT Operations Handbook"
        ],
        burden_holder="CT Operator",
        adversary_position="Manual monitoring is sufficient for flowback operations.",
        counter_arguments=[
            "Real-time systems provide greater accuracy.",
            "Safety is enhanced with real-time monitoring.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Use of real-time systems and periodic validation.",
        entity_scope="CT Flowback",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 10.1"
    ),
    # Additional doctrine blocks for domain completeness
    DoctrineBlock(
        topic="CT String Inspection and Non-Destructive Testing",
        keywords=["CT", "string", "inspection", "non-destructive testing", "NDT", "ultrasonic", "eddy current"],
        conclusion_template="CT string inspection must include periodic non-destructive testing (NDT) using ultrasonic and eddy current methods to detect flaws.",
        reasoning_framework="""
        Periodic inspection of CT strings is essential for detecting flaws such as cracks, corrosion, and wall thinning. The doctrine mandates use of non-destructive testing (NDT) methods, including ultrasonic and eddy current testing, at intervals specified by manufacturer and regulatory guidelines. Operators must document all inspection activities and retain records for compliance. Adversaries may argue for visual inspection only, but NDT methods provide greater accuracy. Resolution involves routine NDT, documentation, and adherence to standards.
        """,
        key_factors=[
            "Ultrasonic testing",
            "Eddy current testing",
            "Inspection intervals",
            "Documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger NDT Manual",
            "NOV CT Inspection Handbook"
        ],
        burden_holder="CT Inspector",
        adversary_position="Visual inspection is sufficient for CT string assessment.",
        counter_arguments=[
            "NDT methods detect flaws invisible to the eye.",
            "Regulatory compliance requires NDT.",
            "Documentation is necessary."
        ],
        resolution_strategy="Routine NDT and documentation.",
        entity_scope="CT Inspection",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 4.2"
    ),
    DoctrineBlock(
        topic="CT String Splicing and Repair Procedures",
        keywords=["CT", "string", "splicing", "repair", "procedures", "welding", "integrity"],
        conclusion_template="CT string splicing and repair must follow validated welding procedures and integrity testing before return to service.",
        reasoning_framework="""
        Splicing and repair of CT strings require validated welding procedures and integrity testing. The doctrine mandates engineering review of repair procedures, use of qualified welders, and post-repair testing for integrity. Operators must document all repair activities and retain records for compliance. Adversaries may argue for expedited repairs, but safety and integrity take precedence. Resolution involves engineering review, qualified personnel, and integrity testing.
        """,
        key_factors=[
            "Welding procedures",
            "Integrity testing",
            "Qualified personnel",
            "Documentation",
            "Engineering review"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Repair Manual",
            "NOV CT Repair Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Expedited repairs are acceptable for CT string splicing.",
        counter_arguments=[
            "Safety and integrity take precedence.",
            "Qualified personnel are required.",
            "Documentation is necessary."
        ],
        resolution_strategy="Engineering review and integrity testing.",
        entity_scope="CT Repair",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 5.1"
    ),
    DoctrineBlock(
        topic="CT String Retirement and Disposal",
        keywords=["CT", "string", "retirement", "disposal", "criteria", "regulatory", "environmental"],
        conclusion_template="CT string retirement and disposal must follow regulatory and environmental guidelines, with documentation of retirement criteria and disposal methods.",
        reasoning_framework="""
        Retirement and disposal of CT strings must follow regulatory and environmental guidelines. The doctrine mandates documentation of retirement criteria, such as fatigue life, damage, and inspection results. Disposal methods must comply with environmental regulations. Operators must retain records for compliance. Adversaries may argue for extended use, but safety and regulatory compliance take precedence. Resolution involves adherence to guidelines, documentation, and environmental compliance.
        """,
        key_factors=[
            "Retirement criteria",
            "Disposal methods",
            "Regulatory compliance",
            "Environmental guidelines",
            "Documentation"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Retirement Manual",
            "NOV CT Disposal Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Extended use is acceptable if no visible damage is present.",
        counter_arguments=[
            "Fatigue life and inspection results must be considered.",
            "Regulatory compliance is mandatory.",
            "Documentation is required."
        ],
        resolution_strategy="Adherence to guidelines and environmental compliance.",
        entity_scope="CT Retirement",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 6.3"
    ),
    DoctrineBlock(
        topic="CT String Corrosion Management",
        keywords=["CT", "string", "corrosion", "management", "inhibitor", "inspection"],
        conclusion_template="CT string corrosion management requires use of inhibitors, periodic inspection, and documentation of all activities.",
        reasoning_framework="""
        Corrosion management for CT strings is essential for extending service life and preventing failures. The doctrine mandates use of corrosion inhibitors, periodic inspection for corrosion, and documentation of all activities. Operators must follow manufacturer and regulatory guidelines. Adversaries may argue for reduced inhibitor use, but empirical evidence shows increased risk of failure. Resolution involves routine inhibitor application, inspection, and documentation.
        """,
        key_factors=[
            "Corrosion inhibitor",
            "Inspection",
            "Documentation",
            "Manufacturer guidelines",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Corrosion Manual",
            "NOV CT Corrosion Handbook"
        ],
        burden_holder="CT Operator",
        adversary_position="Reduced inhibitor use is acceptable for cost savings.",
        counter_arguments=[
            "Empirical evidence shows increased risk of failure.",
            "Manufacturer guidelines must be followed.",
            "Documentation is required."
        ],
        resolution_strategy="Routine inhibitor application and inspection.",
        entity_scope="CT Corrosion",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 4.3"
    ),
    DoctrineBlock(
        topic="CT String Pressure Testing",
        keywords=["CT", "string", "pressure", "testing", "validation", "documentation"],
        conclusion_template="CT string pressure testing must be performed before each operation, with validation against manufacturer specifications and documentation.",
        reasoning_framework="""
        Pressure testing of CT strings is essential for validating integrity before operations. The doctrine mandates testing before each operation, validation against manufacturer specifications, and documentation of all activities. Operators must investigate discrepancies and retain records for compliance. Adversaries may argue for reduced testing frequency, but regulatory requirements mandate testing before every operation. Resolution involves strict adherence to testing protocols and documentation.
        """,
        key_factors=[
            "Testing frequency",
            "Validation",
            "Documentation",
            "Manufacturer specifications",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Pressure Testing Manual",
            "NOV CT Pressure Testing Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Reduced testing frequency is acceptable for routine operations.",
        counter_arguments=[
            "Regulatory requirements mandate testing.",
            "Manufacturer specifications must be followed.",
            "Documentation is necessary."
        ],
        resolution_strategy="Strict adherence to testing protocols and documentation.",
        entity_scope="CT Pressure Testing",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 7.2"
    ),
    DoctrineBlock(
        topic="CT String Leak Detection and Repair",
        keywords=["CT", "string", "leak", "detection", "repair", "procedure", "validation"],
        conclusion_template="CT string leak detection and repair must follow validated procedures, with documentation and post-repair integrity testing.",
        reasoning_framework="""
        Leak detection and repair for CT strings require validated procedures and integrity testing. The doctrine mandates routine leak detection, use of qualified personnel for repairs, and post-repair testing. Operators must document all activities and retain records for compliance. Adversaries may argue for expedited repairs, but safety and integrity take precedence. Resolution involves adherence to procedures, qualified personnel, and integrity testing.
        """,
        key_factors=[
            "Leak detection",
            "Repair procedures",
            "Qualified personnel",
            "Integrity testing",
            "Documentation"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Leak Detection Manual",
            "NOV CT Leak Repair Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Expedited repairs are acceptable for leak detection.",
        counter_arguments=[
            "Safety and integrity take precedence.",
            "Qualified personnel are required.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and integrity testing.",
        entity_scope="CT Leak Repair",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 5.2"
    ),
    DoctrineBlock(
        topic="CT String Inventory Management",
        keywords=["CT", "string", "inventory", "management", "tracking", "documentation"],
        conclusion_template="CT string inventory management requires real-time tracking, documentation, and validation against operational requirements.",
        reasoning_framework="""
        Inventory management for CT strings is essential for operational efficiency and regulatory compliance. The doctrine mandates real-time tracking of inventory, documentation of all activities, and validation against operational requirements. Operators must retain records for compliance. Adversaries may argue for manual tracking, but real-time systems provide greater accuracy. Resolution involves use of real-time systems, documentation, and validation.
        """,
        key_factors=[
            "Real-time tracking",
            "Documentation",
            "Validation",
            "Operational requirements",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Inventory Manual",
            "NOV CT Inventory Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Manual tracking is sufficient for inventory management.",
        counter_arguments=[
            "Real-time systems provide greater accuracy.",
            "Documentation is required for compliance.",
            "Validation ensures operational efficiency."
        ],
        resolution_strategy="Use of real-time systems and documentation.",
        entity_scope="CT Inventory",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.2"
    ),
    DoctrineBlock(
        topic="CT String Storage and Handling",
        keywords=["CT", "string", "storage", "handling", "procedures", "environmental", "protection"],
        conclusion_template="CT string storage and handling must follow validated procedures, with environmental protection and documentation of all activities.",
        reasoning_framework="""
        Proper storage and handling of CT strings are essential for preventing damage and ensuring operational readiness. The doctrine mandates use of validated procedures, environmental protection measures, and documentation of all activities. Operators must follow manufacturer and regulatory guidelines. Adversaries may argue for expedited handling, but safety and protection take precedence. Resolution involves adherence to procedures, environmental protection, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Environmental protection",
            "Documentation",
            "Manufacturer guidelines",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Storage Manual",
            "NOV CT Storage Handbook"
        ],
        burden_holder="CT Operator",
        adversary_position="Expedited handling is acceptable for storage operations.",
        counter_arguments=[
            "Safety and protection take precedence.",
            "Manufacturer guidelines must be followed.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and environmental protection.",
        entity_scope="CT Storage",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.3"
    ),
    DoctrineBlock(
        topic="CT String Transportation and Logistics",
        keywords=["CT", "string", "transportation", "logistics", "procedures", "documentation"],
        conclusion_template="CT string transportation and logistics must follow validated procedures, with documentation and compliance with regulatory requirements.",
        reasoning_framework="""
        Transportation and logistics for CT strings require validated procedures and compliance with regulatory requirements. The doctrine mandates documentation of all activities, use of qualified personnel, and adherence to manufacturer guidelines. Operators must retain records for compliance. Adversaries may argue for expedited transportation, but safety and compliance take precedence. Resolution involves adherence to procedures, qualified personnel, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Qualified personnel",
            "Documentation",
            "Manufacturer guidelines",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Logistics Manual",
            "NOV CT Transportation Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Expedited transportation is acceptable for logistics operations.",
        counter_arguments=[
            "Safety and compliance take precedence.",
            "Manufacturer guidelines must be followed.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and compliance with regulatory requirements.",
        entity_scope="CT Logistics",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.4"
    ),
    DoctrineBlock(
        topic="CT String Identification and Traceability",
        keywords=["CT", "string", "identification", "traceability", "documentation", "tracking"],
        conclusion_template="CT string identification and traceability require real-time tracking, documentation, and validation against operational requirements.",
        reasoning_framework="""
        Identification and traceability of CT strings are essential for operational efficiency and regulatory compliance. The doctrine mandates real-time tracking, documentation of all activities, and validation against operational requirements. Operators must retain records for compliance. Adversaries may argue for manual tracking, but real-time systems provide greater accuracy. Resolution involves use of real-time systems, documentation, and validation.
        """,
        key_factors=[
            "Real-time tracking",
            "Documentation",
            "Validation",
            "Operational requirements",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Identification Manual",
            "NOV CT Traceability Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Manual tracking is sufficient for identification and traceability.",
        counter_arguments=[
            "Real-time systems provide greater accuracy.",
            "Documentation is required for compliance.",
            "Validation ensures operational efficiency."
        ],
        resolution_strategy="Use of real-time systems and documentation.",
        entity_scope="CT Identification",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.5"
    ),
    DoctrineBlock(
        topic="CT String Data Management and Record Keeping",
        keywords=["CT", "string", "data management", "record keeping", "documentation", "tracking"],
        conclusion_template="CT string data management and record keeping require real-time tracking, documentation, and validation against operational requirements.",
        reasoning_framework="""
        Data management and record keeping for CT strings are essential for operational efficiency and regulatory compliance. The doctrine mandates real-time tracking, documentation of all activities, and validation against operational requirements. Operators must retain records for compliance. Adversaries may argue for manual record keeping, but real-time systems provide greater accuracy. Resolution involves use of real-time systems, documentation, and validation.
        """,
        key_factors=[
            "Real-time tracking",
            "Documentation",
            "Validation",
            "Operational requirements",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Data Management Manual",
            "NOV CT Record Keeping Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Manual record keeping is sufficient for data management.",
        counter_arguments=[
            "Real-time systems provide greater accuracy.",
            "Documentation is required for compliance.",
            "Validation ensures operational efficiency."
        ],
        resolution_strategy="Use of real-time systems and documentation.",
        entity_scope="CT Data Management",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.6"
    ),
    DoctrineBlock(
        topic="CT String Operational Readiness and Pre-Job Checks",
        keywords=["CT", "string", "operational readiness", "pre-job checks", "validation", "documentation"],
        conclusion_template="CT string operational readiness requires completion of pre-job checks, validation against operational requirements, and documentation.",
        reasoning_framework="""
        Operational readiness for CT strings requires completion of pre-job checks, validation against operational requirements, and documentation. The doctrine mandates use of validated checklists, engineering review, and retention of records for compliance. Operators must investigate discrepancies and resolve issues before operations. Adversaries may argue for expedited checks, but safety and compliance take precedence. Resolution involves adherence to checklists, engineering review, and documentation.
        """,
        key_factors=[
            "Pre-job checks",
            "Validation",
            "Documentation",
            "Engineering review",
            "Operational requirements"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Pre-Job Manual",
            "NOV CT Operational Readiness Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Expedited checks are acceptable for operational readiness.",
        counter_arguments=[
            "Safety and compliance take precedence.",
            "Engineering review ensures readiness.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to checklists and engineering review.",
        entity_scope="CT Operations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.7"
    ),
    DoctrineBlock(
        topic="CT String Emergency Response Procedures",
        keywords=["CT", "string", "emergency response", "procedures", "validation", "documentation"],
        conclusion_template="CT string emergency response procedures require validated protocols, documentation, and periodic drills.",
        reasoning_framework="""
        Emergency response procedures for CT strings require validated protocols, documentation, and periodic drills. The doctrine mandates engineering review of protocols, retention of records for compliance, and periodic drills to ensure readiness. Operators must investigate discrepancies and resolve issues. Adversaries may argue for reduced drill frequency, but regulatory requirements mandate periodic drills. Resolution involves adherence to protocols, engineering review, and documentation.
        """,
        key_factors=[
            "Validated protocols",
            "Documentation",
            "Periodic drills",
            "Engineering review",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Emergency Response Manual",
            "NOV CT Emergency Procedures Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Reduced drill frequency is acceptable for emergency response.",
        counter_arguments=[
            "Regulatory requirements mandate periodic drills.",
            "Engineering review ensures readiness.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to protocols and periodic drills.",
        entity_scope="CT Emergency Response",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.8"
    ),
    DoctrineBlock(
        topic="CT String Training and Competency Assessment",
        keywords=["CT", "string", "training", "competency assessment", "documentation", "validation"],
        conclusion_template="CT string training and competency assessment require validated programs, documentation, and periodic evaluation.",
        reasoning_framework="""
        Training and competency assessment for CT string operations require validated programs, documentation, and periodic evaluation. The doctrine mandates use of qualified trainers, retention of records for compliance, and periodic evaluation of personnel. Operators must investigate discrepancies and resolve issues. Adversaries may argue for reduced training frequency, but regulatory requirements mandate periodic evaluation. Resolution involves adherence to programs, qualified trainers, and documentation.
        """,
        key_factors=[
            "Validated programs",
            "Documentation",
            "Periodic evaluation",
            "Qualified trainers",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Training Manual",
            "NOV CT Training Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Reduced training frequency is acceptable for competency assessment.",
        counter_arguments=[
            "Regulatory requirements mandate periodic evaluation.",
            "Qualified trainers ensure competency.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to programs and periodic evaluation.",
        entity_scope="CT Training",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.9"
    ),
    DoctrineBlock(
        topic="CT String Quality Assurance and Quality Control",
        keywords=["CT", "string", "quality assurance", "quality control", "QA", "QC", "documentation"],
        conclusion_template="CT string quality assurance and quality control require validated procedures, documentation, and periodic audits.",
        reasoning_framework="""
        Quality assurance and quality control for CT strings require validated procedures, documentation, and periodic audits. The doctrine mandates engineering review of QA/QC procedures, retention of records for compliance, and periodic audits to ensure quality. Operators must investigate discrepancies and resolve issues. Adversaries may argue for reduced audit frequency, but regulatory requirements mandate periodic audits. Resolution involves adherence to procedures, engineering review, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Documentation",
            "Periodic audits",
            "Engineering review",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger QA/QC Manual",
            "NOV CT Quality Control Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Reduced audit frequency is acceptable for QA/QC.",
        counter_arguments=[
            "Regulatory requirements mandate periodic audits.",
            "Engineering review ensures quality.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and periodic audits.",
        entity_scope="CT QA/QC",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.10"
    ),
    DoctrineBlock(
        topic="CT String Regulatory Compliance and Reporting",
        keywords=["CT", "string", "regulatory compliance", "reporting", "documentation", "validation"],
        conclusion_template="CT string regulatory compliance and reporting require validated procedures, documentation, and periodic review.",
        reasoning_framework="""
        Regulatory compliance and reporting for CT strings require validated procedures, documentation, and periodic review. The doctrine mandates engineering review of compliance procedures, retention of records for regulatory review, and periodic audits. Operators must investigate discrepancies and resolve issues. Adversaries may argue for reduced reporting frequency, but regulatory requirements mandate periodic review. Resolution involves adherence to procedures, engineering review, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Documentation",
            "Periodic review",
            "Engineering review",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Compliance Manual",
            "NOV CT Regulatory Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Reduced reporting frequency is acceptable for regulatory compliance.",
        counter_arguments=[
            "Regulatory requirements mandate periodic review.",
            "Engineering review ensures compliance.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and periodic review.",
        entity_scope="CT Regulatory",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.11"
    ),
    DoctrineBlock(
        topic="CT String Incident Investigation and Root Cause Analysis",
        keywords=["CT", "string", "incident investigation", "root cause analysis", "documentation", "validation"],
        conclusion_template="CT string incident investigation and root cause analysis require validated procedures, documentation, and periodic review.",
        reasoning_framework="""
        Incident investigation and root cause analysis for CT strings require validated procedures, documentation, and periodic review. The doctrine mandates engineering review of investigation procedures, retention of records for compliance, and periodic audits. Operators must investigate discrepancies and resolve issues. Adversaries may argue for expedited investigations, but thorough analysis is essential for preventing recurrence. Resolution involves adherence to procedures, engineering review, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Documentation",
            "Periodic review",
            "Engineering review",
            "Incident prevention"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Incident Manual",
            "NOV CT Incident Investigation Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Expedited investigations are acceptable for incident analysis.",
        counter_arguments=[
            "Thorough analysis is essential for prevention.",
            "Engineering review ensures accuracy.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and periodic review.",
        entity_scope="CT Incident Investigation",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.12"
    ),
    DoctrineBlock(
        topic="CT String Performance Optimization",
        keywords=["CT", "string", "performance optimization", "engineering", "validation", "documentation"],
        conclusion_template="CT string performance optimization requires engineering validation, documentation, and periodic review of operational parameters.",
        reasoning_framework="""
        Performance optimization for CT strings requires engineering validation, documentation, and periodic review of operational parameters. The doctrine mandates use of validated engineering models, retention of records for compliance, and periodic review of performance metrics. Operators must investigate discrepancies and resolve issues. Adversaries may argue for expedited optimization, but thorough validation is essential for success. Resolution involves adherence to engineering models, periodic review, and documentation.
        """,
        key_factors=[
            "Engineering validation",
            "Documentation",
            "Periodic review",
            "Performance metrics",
            "Operational parameters"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Optimization Manual",
            "NOV CT Performance Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Expedited optimization is acceptable for performance improvement.",
        counter_arguments=[
            "Thorough validation is essential for success.",
            "Engineering models ensure accuracy.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to engineering models and periodic review.",
        entity_scope="CT Performance",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.13"
    ),
    DoctrineBlock(
        topic="CT String Environmental Protection and Sustainability",
        keywords=["CT", "string", "environmental protection", "sustainability", "documentation", "regulatory compliance"],
        conclusion_template="CT string environmental protection and sustainability require validated procedures, documentation, and compliance with regulatory requirements.",
        reasoning_framework="""
        Environmental protection and sustainability for CT strings require validated procedures, documentation, and compliance with regulatory requirements. The doctrine mandates engineering review of environmental procedures, retention of records for compliance, and periodic audits. Operators must investigate discrepancies and resolve issues. Adversaries may argue for reduced environmental protection, but regulatory requirements mandate compliance. Resolution involves adherence to procedures, engineering review, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Documentation",
            "Regulatory compliance",
            "Engineering review",
            "Periodic audits"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Environmental Manual",
            "NOV CT Sustainability Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Reduced environmental protection is acceptable for cost savings.",
        counter_arguments=[
            "Regulatory requirements mandate compliance.",
            "Engineering review ensures protection.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and compliance with regulatory requirements.",
        entity_scope="CT Environmental",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.14"
    ),
    DoctrineBlock(
        topic="CT String Innovation and Technology Adoption",
        keywords=["CT", "string", "innovation", "technology adoption", "validation", "documentation"],
        conclusion_template="CT string innovation and technology adoption require engineering validation, documentation, and periodic review of new technologies.",
        reasoning_framework="""
        Innovation and technology adoption for CT strings require engineering validation, documentation, and periodic review of new technologies. The doctrine mandates use of validated engineering models, retention of records for compliance, and periodic review of technology adoption. Operators must investigate discrepancies and resolve issues. Adversaries may argue for expedited adoption, but thorough validation is essential for success. Resolution involves adherence to engineering models, periodic review, and documentation.
        """,
        key_factors=[
            "Engineering validation",
            "Documentation",
            "Periodic review",
            "Technology adoption",
            "Operational parameters"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Technology Manual",
            "NOV CT Innovation Handbook"
        ],
        burden_holder="CT Engineer",
        adversary_position="Expedited adoption is acceptable for technology improvement.",
        counter_arguments=[
            "Thorough validation is essential for success.",
            "Engineering models ensure accuracy.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to engineering models and periodic review.",
        entity_scope="CT Technology",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.15"
    ),
    DoctrineBlock(
        topic="CT String Communication and Coordination",
        keywords=["CT", "string", "communication", "coordination", "documentation", "validation"],
        conclusion_template="CT string communication and coordination require validated protocols, documentation, and periodic review.",
        reasoning_framework="""
        Communication and coordination for CT string operations require validated protocols, documentation, and periodic review. The doctrine mandates use of validated communication protocols, retention of records for compliance, and periodic review of coordination activities. Operators must investigate discrepancies and resolve issues. Adversaries may argue for informal communication, but validated protocols ensure accuracy and safety. Resolution involves adherence to protocols, periodic review, and documentation.
        """,
        key_factors=[
            "Validated protocols",
            "Documentation",
            "Periodic review",
            "Coordination activities",
            "Operational requirements"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Communication Manual",
            "NOV CT Coordination Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Informal communication is acceptable for coordination.",
        counter_arguments=[
            "Validated protocols ensure accuracy and safety.",
            "Documentation is required for compliance.",
            "Periodic review ensures effectiveness."
        ],
        resolution_strategy="Adherence to protocols and periodic review.",
        entity_scope="CT Communication",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.16"
    ),
    DoctrineBlock(
        topic="CT String Risk Management and Mitigation",
        keywords=["CT", "string", "risk management", "mitigation", "documentation", "validation"],
        conclusion_template="CT string risk management and mitigation require validated procedures, documentation, and periodic review.",
        reasoning_framework="""
        Risk management and mitigation for CT strings require validated procedures, documentation, and periodic review. The doctrine mandates engineering review of risk management procedures, retention of records for compliance, and periodic audits. Operators must investigate discrepancies and resolve issues. Adversaries may argue for reduced risk management, but regulatory requirements mandate compliance. Resolution involves adherence to procedures, engineering review, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Documentation",
            "Periodic audits",
            "Engineering review",
            "Risk mitigation"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Risk Management Manual",
            "NOV CT Risk Mitigation Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Reduced risk management is acceptable for cost savings.",
        counter_arguments=[
            "Regulatory requirements mandate compliance.",
            "Engineering review ensures mitigation.",
            "Documentation is necessary."
        ],
        resolution_strategy="Adherence to procedures and periodic audits.",
        entity_scope="CT Risk Management",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.17"
    ),
    DoctrineBlock(
        topic="CT String Stakeholder Engagement and Reporting",
        keywords=["CT", "string", "stakeholder engagement", "reporting", "documentation", "validation"],
        conclusion_template="CT string stakeholder engagement and reporting require validated procedures, documentation, and periodic review.",
        reasoning_framework="""
        Stakeholder engagement and reporting for CT strings require validated procedures, documentation, and periodic review. The doctrine mandates use of validated engagement protocols, retention of records for compliance, and periodic review of reporting activities. Operators must investigate discrepancies and resolve issues. Adversaries may argue for informal engagement, but validated procedures ensure accuracy and compliance. Resolution involves adherence to protocols, periodic review, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Documentation",
            "Periodic review",
            "Engagement protocols",
            "Operational requirements"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Stakeholder Manual",
            "NOV CT Reporting Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Informal engagement is acceptable for reporting.",
        counter_arguments=[
            "Validated procedures ensure accuracy and compliance.",
            "Documentation is required for compliance.",
            "Periodic review ensures effectiveness."
        ],
        resolution_strategy="Adherence to protocols and periodic review.",
        entity_scope="CT Stakeholder Engagement",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.18"
    ),
    DoctrineBlock(
        topic="CT String Continuous Improvement and Feedback",
        keywords=["CT", "string", "continuous improvement", "feedback", "documentation", "validation"],
        conclusion_template="CT string continuous improvement and feedback require validated procedures, documentation, and periodic review.",
        reasoning_framework="""
        Continuous improvement and feedback for CT strings require validated procedures, documentation, and periodic review. The doctrine mandates use of validated improvement protocols, retention of records for compliance, and periodic review of feedback activities. Operators must investigate discrepancies and resolve issues. Adversaries may argue for informal feedback, but validated procedures ensure accuracy and effectiveness. Resolution involves adherence to protocols, periodic review, and documentation.
        """,
        key_factors=[
            "Validated procedures",
            "Documentation",
            "Periodic review",
            "Improvement protocols",
            "Operational requirements"
        ],
        primary_authority=[
            "API RP 5C7",
            "Schlumberger Improvement Manual",
            "NOV CT Feedback Handbook"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Informal feedback is acceptable for improvement.",
        counter_arguments=[
            "Validated procedures ensure accuracy and effectiveness.",
            "Documentation is required for compliance.",
            "Periodic review ensures continuous improvement."
        ],
        resolution_strategy="Adherence to protocols and periodic review.",
        entity_scope="CT Continuous Improvement",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5C7 Section 3.19"
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