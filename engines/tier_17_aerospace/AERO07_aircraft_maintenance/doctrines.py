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
        topic="MSG-3 Maintenance Steering Group Analysis Fundamentals",
        keywords=["MSG-3", "maintenance program", "task development", "preventive maintenance", "failure modes"],
        conclusion_template="MSG-3 analysis is the foundational methodology for developing the AERO07 maintenance program, ensuring tasks are justified by safety, operational, and economic considerations.",
        reasoning_framework="""
MSG-3 is an industry-standard analytical process for developing scheduled maintenance tasks for aircraft and engines. The process involves identifying potential failure modes, evaluating their effects, and determining appropriate maintenance actions. The analysis is structured into three primary task types: Lubrication/Servicing, Operational/Functional Checks, and Restoration/Discard tasks. Each task is justified based on safety, operational reliability, and economic impact. The MSG-3 process is iterative, requiring periodic review as operational data accumulates. For AERO07, MSG-3 ensures that only necessary and effective maintenance tasks are included, optimizing cost and safety.
        """,
        key_factors=[
            "Failure mode identification",
            "Safety and operational impact",
            "Task effectiveness and necessity",
            "Economic justification",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ATA MSG-3 Guidelines",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Maintenance Program Developer",
        adversary_position="Overly conservative or excessive maintenance tasks increase cost without proportional safety benefit.",
        counter_arguments=[
            "MSG-3 process ensures tasks are justified and not excessive.",
            "Periodic review allows for task optimization based on real-world data."
        ],
        resolution_strategy="Apply MSG-3 methodology rigorously, document all task justifications, and review tasks periodically.",
        entity_scope="AERO07 Engine Maintenance Program",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ATA MSG-3 Implementation Manual"
    ),
    DoctrineBlock(
        topic="Airworthiness Directive (AD) Compliance Requirements",
        keywords=["AD", "airworthiness directive", "regulatory compliance", "mandatory", "FAA", "EASA"],
        conclusion_template="All AERO07 engines must comply with applicable Airworthiness Directives within the specified timeframes to maintain airworthiness.",
        reasoning_framework="""
Airworthiness Directives (ADs) are legally enforceable rules issued by aviation authorities (FAA, EASA, etc.) to correct unsafe conditions. Compliance is mandatory and must be tracked and documented. For AERO07, the maintenance program must include procedures to identify applicable ADs, ensure timely compliance, and record all actions taken. Failure to comply with an AD renders the engine unairworthy and may result in regulatory action. Operators must establish a system for monitoring new ADs and integrating them into maintenance planning.
        """,
        key_factors=[
            "Identification of applicable ADs",
            "Timely compliance",
            "Documentation and recordkeeping",
            "Integration into maintenance schedule"
        ],
        primary_authority=[
            "14 CFR Part 39",
            "EASA Part 21A.3B",
            "FAA Order 8110.103"
        ],
        burden_holder="Operator and Maintenance Provider",
        adversary_position="ADs may be burdensome or operationally disruptive.",
        counter_arguments=[
            "ADs address known safety issues and are legally required.",
            "Non-compliance risks safety and regulatory penalties."
        ],
        resolution_strategy="Maintain an up-to-date AD tracking system and integrate compliance into routine maintenance.",
        entity_scope="All AERO07 engines in service",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="FAA AD Compliance Policy"
    ),
    DoctrineBlock(
        topic="Reliability-Centered Maintenance (RCM) Program Requirements",
        keywords=["RCM", "reliability", "maintenance optimization", "failure analysis", "maintenance program"],
        conclusion_template="RCM principles must be integrated into the AERO07 maintenance program to optimize task selection based on reliability data.",
        reasoning_framework="""
Reliability-Centered Maintenance (RCM) is a process for determining the most effective maintenance approach based on reliability data and failure consequences. RCM for AERO07 involves collecting operational data, analyzing failure modes, and adjusting maintenance tasks to maximize safety and minimize unnecessary work. The process requires continuous monitoring and feedback to refine maintenance intervals and procedures. RCM ensures that maintenance resources are focused on tasks that provide the greatest benefit to engine reliability and safety.
        """,
        key_factors=[
            "Operational reliability data",
            "Failure mode and effect analysis",
            "Task effectiveness",
            "Continuous improvement"
        ],
        primary_authority=[
            "SAE JA1011",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Maintenance Program Manager",
        adversary_position="RCM implementation may require significant data collection and analysis resources.",
        counter_arguments=[
            "RCM reduces long-term maintenance costs and improves safety.",
            "Modern data systems facilitate RCM implementation."
        ],
        resolution_strategy="Implement RCM as an ongoing process, leveraging available data and technology.",
        entity_scope="AERO07 Engine Maintenance Program",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="SAE JA1011 Standard"
    ),
    DoctrineBlock(
        topic="Non-Destructive Testing (NDT) Method Selection and Qualification",
        keywords=["NDT", "inspection", "qualification", "method selection", "certification"],
        conclusion_template="NDT methods for AERO07 must be selected based on component material, geometry, and failure modes, with personnel qualified to recognized standards.",
        reasoning_framework="""
Non-Destructive Testing (NDT) is essential for detecting flaws without damaging components. The selection of NDT methods (e.g., ultrasonic, eddy current, magnetic particle, dye penetrant) must consider the material, geometry, and typical failure modes of AERO07 engine parts. Personnel performing NDT must be certified to standards such as NAS 410 or EN 4179. Procedures must be validated and periodically reviewed. Proper NDT ensures early detection of defects, preventing failures and ensuring airworthiness.
        """,
        key_factors=[
            "Component material and geometry",
            "Typical failure modes",
            "NDT method suitability",
            "Personnel qualification"
        ],
        primary_authority=[
            "NAS 410",
            "EN 4179",
            "FAA AC 43-13-1B"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="NDT can be time-consuming and costly.",
        counter_arguments=[
            "NDT is critical for safety and required by regulations.",
            "Proper planning minimizes operational impact."
        ],
        resolution_strategy="Establish clear NDT procedures and maintain a roster of qualified personnel.",
        entity_scope="AERO07 Engine Inspection and Maintenance",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NAS 410 Certification Requirements"
    ),
    DoctrineBlock(
        topic="Supplemental Structural Inspection Program (SSIP) Requirements",
        keywords=["SSIP", "structural inspection", "aging aircraft", "fatigue", "inspection intervals"],
        conclusion_template="AERO07 engines must comply with SSIP requirements to address structural fatigue and aging, ensuring continued airworthiness.",
        reasoning_framework="""
The Supplemental Structural Inspection Program (SSIP) addresses the risk of structural fatigue and aging in critical engine components. For AERO07, SSIP requires identification of fatigue-critical parts, establishment of inspection intervals, and implementation of enhanced inspection techniques. Compliance with SSIP is mandatory for continued airworthiness, especially as the fleet ages. Inspection results must be documented, and findings reported to regulatory authorities as required.
        """,
        key_factors=[
            "Identification of fatigue-critical components",
            "Inspection interval determination",
            "Enhanced inspection techniques",
            "Documentation and reporting"
        ],
        primary_authority=[
            "FAA AC 91-56B",
            "EASA AMC 20-20",
            "OEM SSIP Documentation"
        ],
        burden_holder="Operator and Maintenance Provider",
        adversary_position="SSIP may require increased downtime and inspection costs.",
        counter_arguments=[
            "SSIP prevents catastrophic failures due to undetected fatigue.",
            "Regulatory compliance is non-negotiable."
        ],
        resolution_strategy="Integrate SSIP inspections into scheduled maintenance to minimize disruption.",
        entity_scope="AERO07 Engine Structural Components",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA AC 91-56B"
    ),
    DoctrineBlock(
        topic="Corrosion Prevention and Control Program (CPCP) Implementation",
        keywords=["CPCP", "corrosion", "inspection", "prevention", "control", "environmental factors"],
        conclusion_template="AERO07 maintenance must include CPCP measures to detect, prevent, and control corrosion, tailored to operational environment.",
        reasoning_framework="""
Corrosion is a major threat to engine integrity and safety. The Corrosion Prevention and Control Program (CPCP) for AERO07 must include regular inspections, application of protective coatings, and prompt corrective actions. The program should be tailored to the operational environment (e.g., salt, humidity). Documentation of findings and remedial actions is essential. CPCP compliance extends component life and ensures regulatory compliance.
        """,
        key_factors=[
            "Environmental exposure",
            "Inspection frequency",
            "Protective measures",
            "Corrective action procedures"
        ],
        primary_authority=[
            "FAA AC 43-4B",
            "EASA AMC 20-22",
            "OEM CPCP Guidelines"
        ],
        burden_holder="Operator and Maintenance Provider",
        adversary_position="CPCP increases maintenance workload.",
        counter_arguments=[
            "Corrosion can cause catastrophic failures if unchecked.",
            "Preventive measures are more cost-effective than major repairs."
        ],
        resolution_strategy="Schedule CPCP tasks during routine maintenance and train personnel in corrosion detection.",
        entity_scope="AERO07 Engine and Nacelle",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA AC 43-4B"
    ),
    DoctrineBlock(
        topic="Engine Health Monitoring (EHM) and Condition Trend Analysis",
        keywords=["EHM", "trend monitoring", "condition-based maintenance", "data analysis", "predictive maintenance"],
        conclusion_template="EHM and trend analysis must be used for AERO07 to detect emerging issues, optimize maintenance, and prevent failures.",
        reasoning_framework="""
Engine Health Monitoring (EHM) involves continuous or periodic collection of engine parameters (e.g., temperatures, pressures, vibration) to detect abnormal trends. For AERO07, EHM enables early detection of issues, supports condition-based maintenance, and reduces unscheduled removals. Data analysis tools must be in place, and personnel trained to interpret results. EHM findings should be integrated into maintenance planning and reported as required.
        """,
        key_factors=[
            "Parameter selection and data quality",
            "Trend analysis capability",
            "Integration with maintenance planning",
            "Personnel training"
        ],
        primary_authority=[
            "OEM EHM Guidelines",
            "FAA AC 120-79A",
            "EASA AMC 20-25"
        ],
        burden_holder="Operator",
        adversary_position="EHM systems can be costly and require specialized training.",
        counter_arguments=[
            "EHM reduces long-term costs by preventing major failures.",
            "Regulatory authorities increasingly expect EHM for modern engines."
        ],
        resolution_strategy="Invest in EHM infrastructure and ensure data-driven maintenance decisions.",
        entity_scope="AERO07 Engine Fleet",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-79A"
    ),
    DoctrineBlock(
        topic="FAR Part 145 Repair Station Certification and Capabilities",
        keywords=["FAR 145", "repair station", "certification", "capabilities", "maintenance organization"],
        conclusion_template="All maintenance on AERO07 must be performed by FAR Part 145-certified repair stations with appropriate capabilities.",
        reasoning_framework="""
FAR Part 145 sets the requirements for repair station certification, including personnel qualifications, facilities, equipment, and quality systems. Only certified repair stations with approved capabilities may perform maintenance on AERO07 engines. The repair station must maintain current capability lists, ensure personnel are trained and qualified, and comply with all quality assurance requirements. Use of uncertified facilities invalidates maintenance and may compromise airworthiness.
        """,
        key_factors=[
            "Certification status",
            "Capability list accuracy",
            "Personnel qualification",
            "Quality assurance"
        ],
        primary_authority=[
            "14 CFR Part 145",
            "EASA Part 145",
            "FAA Order 8900.1"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Certification requirements may limit available maintenance options.",
        counter_arguments=[
            "Certification ensures maintenance quality and regulatory compliance.",
            "Operators can select from a global network of certified stations."
        ],
        resolution_strategy="Verify repair station certification and capabilities before contracting maintenance.",
        entity_scope="AERO07 Engine Maintenance",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="14 CFR Part 145"
    ),
    DoctrineBlock(
        topic="A-Check, B-Check, C-Check, and D-Check Intervals and Scope",
        keywords=["A-Check", "B-Check", "C-Check", "D-Check", "maintenance intervals", "scheduled maintenance"],
        conclusion_template="AERO07 maintenance must follow OEM-recommended intervals and scope for A, B, C, and D-Checks, adjusted for operational experience and regulatory requirements.",
        reasoning_framework="""
Scheduled maintenance for AERO07 is structured into A, B, C, and D-Checks, each with increasing depth and scope. A-Checks are frequent, light inspections; D-Checks are comprehensive overhauls. Intervals and task content are defined by the OEM and must be tailored based on operational experience and regulatory directives. Deviation from recommended intervals requires justification and regulatory approval. Proper scheduling ensures continued airworthiness and operational reliability.
        """,
        key_factors=[
            "OEM recommendations",
            "Operational experience",
            "Regulatory requirements",
            "Task content and depth"
        ],
        primary_authority=[
            "OEM Maintenance Planning Document",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Frequent checks can disrupt operations and increase costs.",
        counter_arguments=[
            "Scheduled checks prevent unscheduled failures and ensure compliance.",
            "Interval escalation is possible with supporting reliability data."
        ],
        resolution_strategy="Optimize check scheduling using reliability data and seek interval extensions as justified.",
        entity_scope="AERO07 Engine Maintenance Schedule",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Planning Document"
    ),
    DoctrineBlock(
        topic="Service Bulletin (SB) Compliance and Mandatory vs. Optional Status",
        keywords=["service bulletin", "SB", "compliance", "mandatory", "optional", "OEM"],
        conclusion_template="AERO07 operators must evaluate each SB for applicability and comply with those designated as mandatory by the OEM or regulatory authorities.",
        reasoning_framework="""
Service Bulletins (SBs) are issued by the OEM to address product improvements, safety issues, or regulatory requirements. SBs may be classified as mandatory (often linked to ADs) or optional. For AERO07, operators must review each SB, determine applicability, and comply with mandatory SBs within specified timeframes. Optional SBs may be implemented based on operational needs or reliability improvements. Documentation of SB compliance is required for continued airworthiness.
        """,
        key_factors=[
            "SB classification (mandatory/optional)",
            "Applicability to engine configuration",
            "Compliance timeframe",
            "Documentation"
        ],
        primary_authority=[
            "OEM Service Bulletin",
            "FAA AC 43-16A",
            "EASA Part 21"
        ],
        burden_holder="Operator",
        adversary_position="Optional SBs may be costly with unclear benefit.",
        counter_arguments=[
            "Optional SBs can improve reliability or reduce long-term costs.",
            "Mandatory SBs are required for safety and compliance."
        ],
        resolution_strategy="Establish a review process for all SBs and document compliance decisions.",
        entity_scope="AERO07 Engine Fleet",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Service Bulletin Policy"
    ),
    DoctrineBlock(
        topic="Component Time-Between-Overhaul (TBO) and Life-Limited Parts",
        keywords=["TBO", "life-limited parts", "overhaul", "component limits", "replacement intervals"],
        conclusion_template="AERO07 components must be overhauled or replaced at or before TBO or life limits to ensure safety and regulatory compliance.",
        reasoning_framework="""
Each AERO07 component has a defined Time-Between-Overhaul (TBO) or life limit, established by the OEM and approved by regulatory authorities. Exceeding these limits is not permitted without formal extension approval. Maintenance records must track component hours/cycles and ensure timely removal. Life-limited parts are critical for safety; failure to comply can result in catastrophic failure and regulatory action.
        """,
        key_factors=[
            "OEM and regulatory limits",
            "Accurate tracking of hours/cycles",
            "Timely removal/replacement",
            "Documentation"
        ],
        primary_authority=[
            "OEM Component Maintenance Manual",
            "14 CFR Part 43",
            "EASA Part 145"
        ],
        burden_holder="Operator and Maintenance Provider",
        adversary_position="TBO and life limits may be conservative, increasing costs.",
        counter_arguments=[
            "Limits are based on extensive testing and analysis.",
            "Extensions are possible with supporting reliability data and regulatory approval."
        ],
        resolution_strategy="Implement robust tracking systems and review extension opportunities based on reliability data.",
        entity_scope="AERO07 Engine Components",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="OEM Component Maintenance Manual"
    ),
    DoctrineBlock(
        topic="ETOPS Maintenance Requirements and Significant Systems",
        keywords=["ETOPS", "extended operations", "maintenance", "significant systems", "dispatch"],
        conclusion_template="AERO07 engines used in ETOPS operations must meet enhanced maintenance and reliability requirements for significant systems.",
        reasoning_framework="""
Extended-range Twin-engine Operations (ETOPS) require engines and systems to meet higher reliability and maintenance standards. For AERO07, this includes enhanced pre-departure checks, additional EHM, and strict adherence to maintenance intervals. Significant systems (e.g., fuel, oil, controls) must be identified and maintained per ETOPS requirements. Documentation and reporting are critical. Non-compliance may result in loss of ETOPS approval.
        """,
        key_factors=[
            "ETOPS approval status",
            "Identification of significant systems",
            "Enhanced maintenance procedures",
            "Documentation and reporting"
        ],
        primary_authority=[
            "FAA AC 120-42B",
            "EASA AMC 20-6",
            "OEM ETOPS Maintenance Manual"
        ],
        burden_holder="Operator",
        adversary_position="ETOPS requirements increase maintenance workload and cost.",
        counter_arguments=[
            "ETOPS enables more flexible and efficient operations.",
            "Enhanced reliability reduces in-flight failures."
        ],
        resolution_strategy="Integrate ETOPS requirements into standard maintenance and provide additional training.",
        entity_scope="AERO07 Engines in ETOPS Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-42B"
    ),
    DoctrineBlock(
        topic="FAR Part 43 Maintenance Record Requirements and Return to Service",
        keywords=["FAR 43", "maintenance records", "return to service", "documentation", "logbooks"],
        conclusion_template="All maintenance on AERO07 must be documented per FAR Part 43, and engines may only be returned to service by authorized personnel.",
        reasoning_framework="""
FAR Part 43 mandates detailed documentation of all maintenance actions, including description, date, signature, and certificate number of the person approving return to service. For AERO07, maintenance records must be accurate, complete, and retained for regulatory inspection. Only authorized personnel (e.g., A&P mechanics, Part 145 repair stations) may return engines to service. Incomplete records can invalidate maintenance and impact airworthiness.
        """,
        key_factors=[
            "Accurate and complete documentation",
            "Authorized signatories",
            "Record retention",
            "Regulatory inspection readiness"
        ],
        primary_authority=[
            "14 CFR Part 43",
            "EASA Part M.A.305",
            "FAA Order 8900.1"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Recordkeeping can be burdensome and time-consuming.",
        counter_arguments=[
            "Proper records are essential for safety, compliance, and asset value.",
            "Electronic record systems can streamline compliance."
        ],
        resolution_strategy="Implement electronic recordkeeping and train personnel in documentation requirements.",
        entity_scope="AERO07 Engine Maintenance Records",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="14 CFR Part 43"
    ),
    DoctrineBlock(
        topic="Minimum Equipment List (MEL) Dispatch Deviations and Restrictions",
        keywords=["MEL", "dispatch", "deviation", "restrictions", "minimum equipment"],
        conclusion_template="AERO07 dispatch with inoperative equipment must comply with MEL provisions, including limitations and repair intervals.",
        reasoning_framework="""
The Minimum Equipment List (MEL) specifies which equipment may be inoperative for dispatch and under what conditions. For AERO07, MEL compliance ensures safety while maintaining operational flexibility. Deviations must be documented, and repair intervals strictly observed. MEL procedures must be approved by regulatory authorities and integrated into dispatch planning. Non-compliance can result in regulatory action and operational risk.
        """,
        key_factors=[
            "MEL approval status",
            "Deviations and limitations",
            "Repair interval compliance",
            "Documentation"
        ],
        primary_authority=[
            "14 CFR Part 91.213",
            "EASA Part MEL",
            "FAA MMEL Policy Letter"
        ],
        burden_holder="Operator",
        adversary_position="MEL restrictions may limit operational flexibility.",
        counter_arguments=[
            "MEL provides a structured approach to safe dispatch with inoperative items.",
            "Strict limits ensure safety is not compromised."
        ],
        resolution_strategy="Train dispatch and maintenance personnel in MEL procedures and monitor compliance.",
        entity_scope="AERO07 Engine Dispatch Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA MMEL Policy Letter"
    ),
    DoctrineBlock(
        topic="Progressive Maintenance Program Requirements and Segmentation",
        keywords=["progressive maintenance", "segmentation", "maintenance program", "continuous airworthiness"],
        conclusion_template="AERO07 operators may implement progressive maintenance programs, segmenting tasks to minimize downtime while ensuring continuous airworthiness.",
        reasoning_framework="""
Progressive maintenance programs divide major maintenance tasks into smaller segments performed more frequently, reducing downtime and improving scheduling flexibility. For AERO07, such programs must be approved by regulatory authorities and ensure that all required tasks are completed within defined intervals. Documentation and tracking are critical. Progressive programs can improve operational efficiency without compromising safety.
        """,
        key_factors=[
            "Regulatory approval",
            "Task segmentation and scheduling",
            "Documentation and tracking",
            "Continuous airworthiness"
        ],
        primary_authority=[
            "FAA AC 120-17A",
            "EASA Part M",
            "OEM Maintenance Planning Document"
        ],
        burden_holder="Operator",
        adversary_position="Segmentation may increase administrative complexity.",
        counter_arguments=[
            "Progressive programs reduce major downtime and improve asset utilization.",
            "Modern maintenance tracking systems facilitate segmentation."
        ],
        resolution_strategy="Develop robust tracking systems and seek regulatory approval for program design.",
        entity_scope="AERO07 Engine Maintenance Program",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-17A"
    ),
    DoctrineBlock(
        topic="Human Factors in Aircraft Maintenance and Error Prevention",
        keywords=["human factors", "maintenance error", "training", "error prevention", "safety culture"],
        conclusion_template="AERO07 maintenance programs must address human factors through training, procedures, and safety culture to minimize errors.",
        reasoning_framework="""
Human error is a leading cause of maintenance-related incidents. For AERO07, maintenance programs must incorporate human factors principles, including comprehensive training, clear procedures, and a strong safety culture. Error reporting systems, fatigue management, and ergonomic considerations are essential. Continuous improvement based on error analysis reduces risk and improves safety outcomes.
        """,
        key_factors=[
            "Comprehensive training",
            "Clear procedures",
            "Error reporting and analysis",
            "Fatigue management"
        ],
        primary_authority=[
            "FAA AC 120-72A",
            "EASA Part 145.A.30(e)",
            "ICAO Doc 9859"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Human factors initiatives may increase training costs.",
        counter_arguments=[
            "Error prevention reduces costly incidents and improves safety.",
            "Regulatory authorities require human factors programs."
        ],
        resolution_strategy="Invest in human factors training and foster a just safety culture.",
        entity_scope="AERO07 Engine Maintenance Personnel",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-72A"
    ),
    # Additional 25+ DoctrineBlock instances with real content below
    DoctrineBlock(
        topic="Parts Tagging and Traceability Requirements",
        keywords=["parts tagging", "traceability", "documentation", "airworthiness", "certification"],
        conclusion_template="All AERO07 parts must be tagged and traceable to an approved source, with supporting documentation for airworthiness.",
        reasoning_framework="""
Parts tagging and traceability are essential for ensuring that only approved and airworthy components are installed on AERO07 engines. Each part must be accompanied by appropriate documentation (e.g., FAA Form 8130-3, EASA Form 1) and be traceable to an approved source. Unapproved or undocumented parts compromise safety and regulatory compliance. Maintenance providers must verify documentation before installation and retain records for inspection.
        """,
        key_factors=[
            "Approved source verification",
            "Proper documentation",
            "Record retention",
            "Regulatory compliance"
        ],
        primary_authority=[
            "14 CFR Part 21",
            "EASA Part 21",
            "FAA Order 8130.21"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Strict traceability may delay repairs.",
        counter_arguments=[
            "Traceability ensures component integrity and safety.",
            "Expedited processes can minimize delays."
        ],
        resolution_strategy="Implement robust parts tracking and verification procedures.",
        entity_scope="AERO07 Engine Components",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA Order 8130.21"
    ),
    DoctrineBlock(
        topic="Tooling Control and Calibration Standards",
        keywords=["tooling", "calibration", "control", "maintenance tools", "quality assurance"],
        conclusion_template="All tools used for AERO07 maintenance must be controlled, calibrated, and traceable to national standards.",
        reasoning_framework="""
Proper tooling is critical for safe and effective maintenance. All tools used on AERO07 must be controlled, regularly calibrated, and traceable to national/international standards (e.g., NIST). Calibration intervals must be documented, and out-of-tolerance tools removed from service. Tooling control prevents maintenance errors and ensures compliance with quality standards.
        """,
        key_factors=[
            "Tool control procedures",
            "Calibration interval compliance",
            "Traceability to standards",
            "Documentation"
        ],
        primary_authority=[
            "FAA AC 145-9",
            "EASA Part 145.A.40",
            "ISO 17025"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Tool control programs can be resource-intensive.",
        counter_arguments=[
            "Proper tooling prevents costly errors and rework.",
            "Calibration is a regulatory requirement."
        ],
        resolution_strategy="Automate tooling control and calibration tracking where possible.",
        entity_scope="AERO07 Engine Maintenance Facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 145-9"
    ),
    DoctrineBlock(
        topic="Foreign Object Damage (FOD) Prevention Programs",
        keywords=["FOD", "foreign object damage", "prevention", "inspection", "engine safety"],
        conclusion_template="AERO07 maintenance environments must implement FOD prevention programs to minimize risk of engine damage.",
        reasoning_framework="""
Foreign Object Damage (FOD) is a significant risk to engine safety and reliability. Maintenance environments for AERO07 must have FOD prevention programs, including regular inspections, tool and parts accountability, and personnel training. FOD events must be reported and analyzed to prevent recurrence. Effective FOD control reduces unscheduled removals and costly repairs.
        """,
        key_factors=[
            "FOD awareness training",
            "Inspection and cleaning procedures",
            "Tool and parts accountability",
            "Incident reporting"
        ],
        primary_authority=[
            "FAA AC 150/5210-24",
            "EASA AMC 20-8",
            "OEM FOD Prevention Guidelines"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="FOD programs may slow maintenance processes.",
        counter_arguments=[
            "FOD prevention reduces costly engine damage.",
            "Programs can be integrated into routine procedures."
        ],
        resolution_strategy="Integrate FOD checks into all maintenance steps and foster a culture of accountability.",
        entity_scope="AERO07 Engine Maintenance Areas",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 150/5210-24"
    ),
    DoctrineBlock(
        topic="Engine Run-Up and Functional Test Procedures",
        keywords=["engine run-up", "functional test", "post-maintenance", "procedures", "performance verification"],
        conclusion_template="AERO07 engines must undergo run-up and functional tests after major maintenance to verify performance and airworthiness.",
        reasoning_framework="""
After major maintenance or repair, AERO07 engines must be subjected to run-up and functional tests per OEM and regulatory procedures. Tests verify correct operation, performance parameters, and absence of leaks or abnormal vibrations. Only authorized personnel may conduct and certify tests. Results must be documented and retained for inspection.
        """,
        key_factors=[
            "Test procedure compliance",
            "Authorized personnel",
            "Performance parameter verification",
            "Documentation"
        ],
        primary_authority=[
            "OEM Engine Maintenance Manual",
            "FAA AC 43-13-1B",
            "EASA Part 145"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Run-up tests may be time-consuming and require special facilities.",
        counter_arguments=[
            "Functional tests are critical for safety and regulatory compliance.",
            "Proper scheduling minimizes operational impact."
        ],
        resolution_strategy="Plan run-up tests in advance and ensure all required resources are available.",
        entity_scope="AERO07 Engine Post-Maintenance",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM Engine Maintenance Manual"
    ),
    DoctrineBlock(
        topic="Oil Analysis and Lubrication Monitoring",
        keywords=["oil analysis", "lubrication", "monitoring", "wear detection", "condition-based maintenance"],
        conclusion_template="Regular oil analysis must be performed on AERO07 engines to detect wear and optimize lubrication intervals.",
        reasoning_framework="""
Oil analysis provides early detection of abnormal wear, contamination, or lubrication issues in AERO07 engines. Samples must be taken at defined intervals and analyzed for metal content, viscosity, and contaminants. Results inform maintenance decisions and may trigger additional inspections or early removal. Lubrication intervals should be adjusted based on analysis trends and OEM recommendations.
        """,
        key_factors=[
            "Sampling interval",
            "Analysis parameters",
            "Trend monitoring",
            "Maintenance response"
        ],
        primary_authority=[
            "OEM Maintenance Manual",
            "FAA AC 43-12A",
            "ASTM D5185"
        ],
        burden_holder="Operator",
        adversary_position="Oil analysis programs add operational complexity.",
        counter_arguments=[
            "Early detection of wear prevents major failures.",
            "Oil analysis can extend component life and reduce costs."
        ],
        resolution_strategy="Automate oil sampling and integrate results into EHM systems.",
        entity_scope="AERO07 Engine Lubrication System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Manual"
    ),
    DoctrineBlock(
        topic="Environmental Compliance and Hazardous Material Handling",
        keywords=["environmental compliance", "hazardous materials", "waste disposal", "EPA", "safety"],
        conclusion_template="AERO07 maintenance must comply with environmental regulations for hazardous material handling, storage, and disposal.",
        reasoning_framework="""
Maintenance on AERO07 engines involves use and disposal of hazardous materials (e.g., oils, solvents, batteries). Compliance with environmental regulations (EPA, EASA, local) is mandatory. Procedures must address safe handling, storage, labeling, and disposal. Personnel must be trained, and records maintained for regulatory inspection. Non-compliance can result in fines and operational restrictions.
        """,
        key_factors=[
            "Hazardous material identification",
            "Safe handling and storage",
            "Proper disposal",
            "Training and documentation"
        ],
        primary_authority=[
            "EPA 40 CFR",
            "EASA Part 145.A.50",
            "OEM Environmental Guidelines"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Environmental compliance increases operational costs.",
        counter_arguments=[
            "Non-compliance risks severe penalties and reputational damage.",
            "Proper procedures protect personnel and the environment."
        ],
        resolution_strategy="Implement environmental management systems and provide regular training.",
        entity_scope="AERO07 Engine Maintenance Facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR"
    ),
    DoctrineBlock(
        topic="Aircraft-On-Ground (AOG) Support and Response Protocols",
        keywords=["AOG", "aircraft-on-ground", "support", "response", "maintenance"],
        conclusion_template="AERO07 operators must have AOG support protocols to minimize downtime and restore airworthiness rapidly.",
        reasoning_framework="""
Aircraft-On-Ground (AOG) situations require rapid response to restore airworthiness and minimize operational disruption. For AERO07, operators must have AOG support agreements, access to critical spares, and established communication protocols. Maintenance providers must prioritize AOG cases and document all actions taken. Effective AOG response reduces financial impact and improves customer satisfaction.
        """,
        key_factors=[
            "AOG response agreements",
            "Critical spares availability",
            "Communication protocols",
            "Prioritization and documentation"
        ],
        primary_authority=[
            "OEM AOG Support Policy",
            "FAA AC 120-79A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="AOG support may increase inventory and staffing costs.",
        counter_arguments=[
            "Rapid AOG response minimizes revenue loss and customer dissatisfaction.",
            "AOG protocols are an industry standard."
        ],
        resolution_strategy="Establish AOG teams and maintain critical spares inventory.",
        entity_scope="AERO07 Engine Operators",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM AOG Support Policy"
    ),
    DoctrineBlock(
        topic="Engine Removal and Installation Best Practices",
        keywords=["engine removal", "installation", "procedures", "best practices", "safety"],
        conclusion_template="AERO07 engine removal and installation must follow OEM procedures and best practices to ensure safety and prevent damage.",
        reasoning_framework="""
Engine removal and installation are critical maintenance tasks for AERO07. Procedures must follow OEM guidelines, including use of proper tooling, support equipment, and sequence of steps. Personnel must be trained and authorized. All connections (electrical, fluid, mechanical) must be verified, and post-installation checks documented. Deviations from procedures increase risk of damage or safety incidents.
        """,
        key_factors=[
            "OEM procedure compliance",
            "Proper tooling and equipment",
            "Personnel training",
            "Post-installation checks"
        ],
        primary_authority=[
            "OEM Engine Maintenance Manual",
            "FAA AC 43-13-1B",
            "EASA Part 145"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Strict adherence to procedures may increase time required.",
        counter_arguments=[
            "Best practices prevent costly errors and rework.",
            "Proper planning minimizes downtime."
        ],
        resolution_strategy="Train personnel and audit compliance with removal/installation procedures.",
        entity_scope="AERO07 Engine Maintenance",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM Engine Maintenance Manual"
    ),
    DoctrineBlock(
        topic="Unscheduled Engine Removal Analysis and Reporting",
        keywords=["unscheduled removal", "engine analysis", "reporting", "failure investigation", "root cause"],
        conclusion_template="All unscheduled removals of AERO07 engines must be analyzed and reported to identify root causes and prevent recurrence.",
        reasoning_framework="""
Unscheduled engine removals indicate underlying reliability or maintenance issues. For AERO07, each event must be analyzed to determine root cause, with findings documented and reported to OEM and regulatory authorities as required. Data from unscheduled removals informs reliability improvement and maintenance program adjustments. Failure to analyze and report can mask systemic issues.
        """,
        key_factors=[
            "Root cause analysis",
            "Documentation and reporting",
            "Reliability data integration",
            "Corrective action implementation"
        ],
        primary_authority=[
            "OEM Reliability Program",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Analysis and reporting may delay return to service.",
        counter_arguments=[
            "Root cause analysis prevents repeat failures.",
            "Reporting is a regulatory requirement."
        ],
        resolution_strategy="Establish rapid analysis protocols and integrate findings into reliability programs.",
        entity_scope="AERO07 Engine Fleet",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Reliability Program"
    ),
    DoctrineBlock(
        topic="Modification and Repair Approval Process",
        keywords=["modification", "repair", "approval", "engineering", "regulatory"],
        conclusion_template="All modifications and repairs to AERO07 must be approved by OEM or regulatory authorities before implementation.",
        reasoning_framework="""
Modifications and repairs to AERO07 engines must be approved through OEM engineering or regulatory authorities (FAA, EASA). Unapproved modifications or repairs may compromise safety and airworthiness. Approval requires submission of engineering data, analysis, and sometimes testing. Documentation of approval must be retained. Field repairs outside approved data are prohibited.
        """,
        key_factors=[
            "Engineering data submission",
            "Regulatory approval",
            "Documentation retention",
            "Compliance verification"
        ],
        primary_authority=[
            "14 CFR Part 21",
            "EASA Part 21",
            "OEM Engineering Procedures"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Approval process may delay urgent repairs.",
        counter_arguments=[
            "Approval ensures safety and regulatory compliance.",
            "Expedited processes are available for urgent cases."
        ],
        resolution_strategy="Plan modifications/repairs in advance and maintain communication with OEM/regulators.",
        entity_scope="AERO07 Engine Maintenance and Repair",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="14 CFR Part 21"
    ),
    DoctrineBlock(
        topic="Service Life Extension and Escalation Procedures",
        keywords=["service life extension", "escalation", "interval extension", "reliability data", "regulatory approval"],
        conclusion_template="AERO07 service life or maintenance intervals may be extended only through approved escalation procedures based on reliability data.",
        reasoning_framework="""
Service life extensions or escalation of maintenance intervals for AERO07 require analysis of reliability data and formal approval from OEM and regulatory authorities. Extensions must be justified by operational experience, low failure rates, and supporting analysis. Documentation of the approval process and ongoing monitoring are required. Unauthorized extensions are prohibited.
        """,
        key_factors=[
            "Reliability data analysis",
            "OEM and regulatory approval",
            "Documentation",
            "Ongoing monitoring"
        ],
        primary_authority=[
            "OEM Escalation Procedures",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Escalation process may be complex and slow.",
        counter_arguments=[
            "Proper escalation can reduce costs and improve utilization.",
            "Process ensures continued safety and compliance."
        ],
        resolution_strategy="Maintain detailed reliability records and engage with OEM/regulators early.",
        entity_scope="AERO07 Engine Maintenance Program",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Escalation Procedures"
    ),
    DoctrineBlock(
        topic="Engine Preservation and Storage Procedures",
        keywords=["engine preservation", "storage", "procedures", "long-term", "corrosion prevention"],
        conclusion_template="AERO07 engines in storage must be preserved per OEM procedures to prevent corrosion and maintain airworthiness.",
        reasoning_framework="""
When AERO07 engines are removed from service for storage, preservation procedures must be followed to prevent corrosion and degradation. Procedures include draining fluids, applying protective coatings, sealing openings, and periodic inspections. Documentation of preservation actions is required. Improper storage can result in costly repairs and loss of airworthiness.
        """,
        key_factors=[
            "OEM preservation procedures",
            "Environmental controls",
            "Periodic inspection",
            "Documentation"
        ],
        primary_authority=[
            "OEM Preservation Manual",
            "FAA AC 43-13-1B",
            "EASA Part 145"
        ],
        burden_holder="Operator",
        adversary_position="Preservation procedures may increase storage costs.",
        counter_arguments=[
            "Proper preservation protects asset value and reduces reactivation costs.",
            "Procedures are industry standard."
        ],
        resolution_strategy="Train personnel and audit compliance with preservation procedures.",
        entity_scope="AERO07 Engines in Storage",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Preservation Manual"
    ),
    DoctrineBlock(
        topic="Fire Protection and Detection System Maintenance",
        keywords=["fire protection", "detection", "system maintenance", "inspection", "testing"],
        conclusion_template="AERO07 fire protection and detection systems must be inspected and tested at defined intervals to ensure functionality.",
        reasoning_framework="""
Fire protection and detection systems are critical for AERO07 safety. Maintenance must include regular inspection, functional testing, and replacement of time-limited components (e.g., sensors, extinguishers). Procedures must follow OEM and regulatory requirements. Documentation of inspection and test results is required. Inoperative fire systems are a no-go item for dispatch.
        """,
        key_factors=[
            "Inspection and test intervals",
            "Component replacement",
            "OEM and regulatory procedures",
            "Documentation"
        ],
        primary_authority=[
            "OEM Maintenance Manual",
            "FAA AC 20-42D",
            "EASA CS-E"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Testing may require special equipment and training.",
        counter_arguments=[
            "Fire system functionality is critical for safety.",
            "OEM provides detailed procedures and support."
        ],
        resolution_strategy="Schedule fire system maintenance with other major checks and provide necessary training.",
        entity_scope="AERO07 Engine Fire Systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Manual"
    ),
    DoctrineBlock(
        topic="Engine Control System Software Configuration Management",
        keywords=["software", "engine control", "configuration management", "FADEC", "updates"],
        conclusion_template="AERO07 engine control software (e.g., FADEC) must be managed and updated per OEM configuration management procedures.",
        reasoning_framework="""
Software in AERO07 engine control systems (e.g., FADEC) is critical for performance and safety. Configuration management ensures only approved software versions are installed. Updates must be performed per OEM procedures, with documentation and verification. Unauthorized software changes are prohibited. Regular audits ensure compliance and traceability.
        """,
        key_factors=[
            "Approved software version control",
            "Update procedures",
            "Documentation and verification",
            "Audit and traceability"
        ],
        primary_authority=[
            "OEM Configuration Management Manual",
            "FAA AC 20-115D",
            "EASA AMC 20-115"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Software management may require specialized tools and training.",
        counter_arguments=[
            "Proper configuration management prevents software-related failures.",
            "OEM provides support and training."
        ],
        resolution_strategy="Maintain a software version database and audit compliance regularly.",
        entity_scope="AERO07 Engine Control Systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Configuration Management Manual"
    ),
    DoctrineBlock(
        topic="Technical Publications and Data Control",
        keywords=["technical publications", "data control", "manuals", "revisions", "maintenance procedures"],
        conclusion_template="AERO07 maintenance must use current technical publications, with robust data control to ensure procedures are up-to-date.",
        reasoning_framework="""
Maintenance on AERO07 must be performed using current technical publications (e.g., maintenance manuals, service bulletins). Data control systems must track revisions and ensure only current procedures are used. Outdated or unauthorized publications may result in maintenance errors and regulatory non-compliance. Regular audits and training are required.
        """,
        key_factors=[
            "Revision control",
            "Access to current manuals",
            "Audit procedures",
            "Personnel training"
        ],
        primary_authority=[
            "FAA AC 120-78A",
            "EASA Part 145.A.45",
            "OEM Data Management Policy"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Data control systems may require investment in IT infrastructure.",
        counter_arguments=[
            "Accurate data control prevents costly errors.",
            "Electronic systems improve efficiency and compliance."
        ],
        resolution_strategy="Implement electronic data management and train personnel in data control procedures.",
        entity_scope="AERO07 Engine Maintenance Documentation",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-78A"
    ),
    DoctrineBlock(
        topic="Training and Qualification of Maintenance Personnel",
        keywords=["training", "qualification", "maintenance personnel", "certification", "competency"],
        conclusion_template="All personnel performing AERO07 maintenance must be trained and qualified per regulatory and OEM requirements.",
        reasoning_framework="""
Competency of maintenance personnel is critical for AERO07 safety and reliability. Training programs must cover technical skills, regulatory requirements, and human factors. Qualification must be documented, and recurrent training provided. Only certified personnel may perform and certify maintenance. Training records must be retained for inspection.
        """,
        key_factors=[
            "Initial and recurrent training",
            "Certification and qualification",
            "Documentation",
            "Audit and oversight"
        ],
        primary_authority=[
            "FAA AC 145-10",
            "EASA Part 145.A.30",
            "OEM Training Program"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Training programs increase operational costs.",
        counter_arguments=[
            "Proper training reduces errors and improves safety.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Invest in comprehensive training and maintain detailed records.",
        entity_scope="AERO07 Engine Maintenance Personnel",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="FAA AC 145-10"
    ),
    DoctrineBlock(
        topic="Safety Management System (SMS) Integration in Maintenance Operations",
        keywords=["SMS", "safety management system", "maintenance", "risk assessment", "continuous improvement"],
        conclusion_template="AERO07 maintenance organizations must integrate SMS principles to proactively manage risk and improve safety.",
        reasoning_framework="""
A Safety Management System (SMS) provides a structured approach to managing safety risk in AERO07 maintenance operations. SMS includes hazard identification, risk assessment, safety assurance, and promotion. Integration of SMS is required by regulatory authorities and supports continuous improvement. Documentation and regular review of SMS effectiveness are required.
        """,
        key_factors=[
            "Hazard identification and reporting",
            "Risk assessment and mitigation",
            "Safety assurance",
            "Continuous improvement"
        ],
        primary_authority=[
            "ICAO Annex 19",
            "FAA AC 120-92B",
            "EASA Part 145.A.62"
        ],
        burden_holder="Maintenance Organization",
        adversary_position="SMS implementation may require cultural change and resource allocation.",
        counter_arguments=[
            "SMS reduces incidents and improves safety outcomes.",
            "Regulatory authorities mandate SMS integration."
        ],
        resolution_strategy="Appoint SMS focal points and provide training to all personnel.",
        entity_scope="AERO07 Engine Maintenance Organizations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-92B"
    ),
    DoctrineBlock(
        topic="Maintenance Program Escalation and De-Escalation Procedures",
        keywords=["maintenance program", "escalation", "de-escalation", "interval adjustment", "reliability"],
        conclusion_template="AERO07 maintenance intervals may be escalated or de-escalated based on reliability data and regulatory approval.",
        reasoning_framework="""
Maintenance program intervals for AERO07 can be adjusted (escalated or de-escalated) based on analysis of reliability data, operational experience, and regulatory approval. Escalation increases intervals for proven reliability; de-escalation shortens intervals in response to adverse trends. All changes must be documented and justified. Unauthorized interval changes are prohibited.
        """,
        key_factors=[
            "Reliability data analysis",
            "Regulatory approval",
            "Documentation",
            "Ongoing monitoring"
        ],
        primary_authority=[
            "OEM Maintenance Planning Document",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Frequent interval changes may cause confusion.",
        counter_arguments=[
            "Structured procedures ensure changes are justified and controlled.",
            "Interval adjustments optimize maintenance efficiency."
        ],
        resolution_strategy="Establish formal escalation/de-escalation procedures and communicate changes to all stakeholders.",
        entity_scope="AERO07 Engine Maintenance Program",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Planning Document"
    ),
    DoctrineBlock(
        topic="Maintenance Error Investigation and Corrective Action",
        keywords=["maintenance error", "investigation", "corrective action", "root cause", "reporting"],
        conclusion_template="All maintenance errors on AERO07 must be investigated, with corrective actions implemented and reported.",
        reasoning_framework="""
Maintenance errors can have serious safety consequences. For AERO07, all errors must be promptly investigated to determine root cause. Corrective actions must be implemented to prevent recurrence, and findings reported to management and regulatory authorities as required. Error data informs training and process improvement.
        """,
        key_factors=[
            "Error detection and reporting",
            "Root cause analysis",
            "Corrective action implementation",
            "Documentation and communication"
        ],
        primary_authority=[
            "FAA AC 120-72A",
            "EASA Part 145.A.60",
            "OEM Error Management Policy"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Investigation may delay return to service.",
        counter_arguments=[
            "Prompt investigation prevents future incidents.",
            "Regulatory authorities require error reporting."
        ],
        resolution_strategy="Establish error reporting systems and train personnel in investigation procedures.",
        entity_scope="AERO07 Engine Maintenance Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-72A"
    ),
    DoctrineBlock(
        topic="Critical Task Identification and Independent Inspection",
        keywords=["critical task", "independent inspection", "double inspection", "safety", "quality assurance"],
        conclusion_template="AERO07 maintenance programs must identify critical tasks and require independent inspection to verify completion.",
        reasoning_framework="""
Critical maintenance tasks on AERO07 (those affecting flight safety) must be identified in the maintenance program. Completion of these tasks requires independent inspection (double check) by a second qualified person. Documentation of both completion and inspection is required. This reduces the risk of undetected errors in safety-critical areas.
        """,
        key_factors=[
            "Critical task identification",
            "Independent inspection procedures",
            "Qualified personnel",
            "Documentation"
        ],
        primary_authority=[
            "EASA Part 145.A.48",
            "FAA AC 120-72A",
            "OEM Maintenance Program"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Double inspection increases labor requirements.",
        counter_arguments=[
            "Independent inspection prevents catastrophic errors.",
            "Regulatory authorities require this for critical tasks."
        ],
        resolution_strategy="Maintain a list of critical tasks and train personnel in independent inspection procedures.",
        entity_scope="AERO07 Engine Maintenance Program",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EASA Part 145.A.48"
    ),
    DoctrineBlock(
        topic="Consumables and Expendables Management",
        keywords=["consumables", "expendables", "management", "shelf life", "traceability"],
        conclusion_template="AERO07 maintenance must ensure consumables and expendables are within shelf life and traceable to approved sources.",
        reasoning_framework="""
Consumables and expendables (e.g., lubricants, sealants, O-rings) used in AERO07 maintenance must be managed to ensure they are within shelf life and sourced from approved suppliers. Expired or unapproved materials may compromise safety and airworthiness. Inventory control systems and documentation are required to track usage and shelf life.
        """,
        key_factors=[
            "Shelf life monitoring",
            "Approved supplier verification",
            "Inventory control",
            "Documentation"
        ],
        primary_authority=[
            "OEM Maintenance Manual",
            "FAA AC 20-62E",
            "EASA Part 145.A.42"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Strict management may increase administrative workload.",
        counter_arguments=[
            "Proper management prevents use of degraded materials.",
            "Inventory systems can automate compliance."
        ],
        resolution_strategy="Implement electronic inventory control and audit consumables regularly.",
        entity_scope="AERO07 Engine Maintenance Facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-62E"
    ),
    DoctrineBlock(
        topic="Warranty Claim and Reporting Procedures",
        keywords=["warranty", "claim", "reporting", "OEM", "maintenance"],
        conclusion_template="AERO07 operators must follow OEM warranty claim and reporting procedures to ensure coverage for eligible failures.",
        reasoning_framework="""
Warranty coverage for AERO07 engines requires prompt reporting of eligible failures, submission of required documentation, and compliance with OEM procedures. Failure to follow procedures may void warranty coverage. Maintenance providers must be familiar with claim processes and maintain records of all claims and correspondence.
        """,
        key_factors=[
            "Eligibility determination",
            "Timely reporting",
            "Documentation submission",
            "Record retention"
        ],
        primary_authority=[
            "OEM Warranty Policy",
            "FAA AC 43-9C",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Warranty claim processes may be complex and time-consuming.",
        counter_arguments=[
            "Proper claims reduce maintenance costs.",
            "OEM provides support for claim submission."
        ],
        resolution_strategy="Train personnel in warranty procedures and maintain a warranty claim log.",
        entity_scope="AERO07 Engine Fleet",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Warranty Policy"
    ),
    DoctrineBlock(
        topic="Reliability Data Collection and Reporting",
        keywords=["reliability data", "collection", "reporting", "maintenance program", "continuous improvement"],
        conclusion_template="AERO07 operators must collect and report reliability data to support maintenance program optimization.",
        reasoning_framework="""
Reliability data (e.g., failure rates, unscheduled removals, in-service events) is essential for optimizing AERO07 maintenance programs. Operators must collect, analyze, and report data to OEM and regulatory authorities as required. Data informs task interval adjustments, escalation, and continuous improvement. Incomplete data hampers program effectiveness.
        """,
        key_factors=[
            "Data collection systems",
            "Analysis capability",
            "Reporting procedures",
            "Continuous improvement"
        ],
        primary_authority=[
            "OEM Reliability Program",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Data collection may require investment in IT systems.",
        counter_arguments=[
            "Reliability data improves safety and reduces costs.",
            "Modern systems automate much of the process."
        ],
        resolution_strategy="Invest in reliability data systems and train personnel in data analysis.",
        entity_scope="AERO07 Engine Operators",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Reliability Program"
    ),
    DoctrineBlock(
        topic="Aircraft Maintenance Program Approval and Revision Control",
        keywords=["maintenance program", "approval", "revision control", "regulatory", "continuous airworthiness"],
        conclusion_template="AERO07 maintenance programs must be approved by regulatory authorities and subject to strict revision control.",
        reasoning_framework="""
Maintenance programs for AERO07 must be approved by the relevant regulatory authority (FAA, EASA). Any changes or revisions require formal submission and approval. Revision control ensures only current, approved procedures are used. Unauthorized changes may invalidate the program and compromise airworthiness.
        """,
        key_factors=[
            "Regulatory approval",
            "Revision submission and tracking",
            "Documentation",
            "Audit and compliance"
        ],
        primary_authority=[
            "FAA AC 120-16G",
            "EASA Part M.A.302",
            "OEM Maintenance Program"
        ],
        burden_holder="Operator",
        adversary_position="Approval and revision processes may delay implementation of improvements.",
        counter_arguments=[
            "Formal processes ensure safety and regulatory compliance.",
            "Expedited review is available for urgent changes."
        ],
        resolution_strategy="Maintain a revision log and communicate changes to all stakeholders.",
        entity_scope="AERO07 Engine Maintenance Program",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-16G"
    ),
    DoctrineBlock(
        topic="Outsourcing and Subcontractor Oversight",
        keywords=["outsourcing", "subcontractor", "oversight", "maintenance", "quality assurance"],
        conclusion_template="AERO07 maintenance tasks outsourced to subcontractors require oversight and quality assurance to ensure compliance.",
        reasoning_framework="""
Outsourcing maintenance tasks for AERO07 is permitted only to approved subcontractors. The primary maintenance provider remains responsible for oversight, quality assurance, and regulatory compliance. Subcontractors must be audited regularly, and performance documented. Failure to oversee subcontractors can result in non-compliance and safety risks.
        """,
        key_factors=[
            "Subcontractor approval",
            "Oversight and auditing",
            "Quality assurance procedures",
            "Documentation"
        ],
        primary_authority=[
            "FAA AC 145-11",
            "EASA Part 145.A.75",
            "OEM Maintenance Policy"
        ],
        burden_holder="Primary Maintenance Provider",
        adversary_position="Oversight increases administrative workload.",
        counter_arguments=[
            "Oversight ensures quality and compliance.",
            "Subcontracting can improve efficiency if managed properly."
        ],
        resolution_strategy="Establish formal oversight procedures and audit subcontractors regularly.",
        entity_scope="AERO07 Engine Maintenance Operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 145-11"
    ),
    DoctrineBlock(
        topic="Maintenance Task Card Development and Control",
        keywords=["task card", "development", "control", "maintenance procedures", "documentation"],
        conclusion_template="AERO07 maintenance task cards must be developed, controlled, and updated to reflect current procedures and regulatory requirements.",
        reasoning_framework="""
Task cards provide step-by-step instructions for AERO07 maintenance tasks. Development must follow OEM and regulatory guidelines, ensuring clarity and completeness. Task cards must be controlled, with revision tracking and distribution to ensure only current versions are used. Outdated or incomplete task cards can result in maintenance errors.
        """,
        key_factors=[
            "Task card development procedures",
            "Revision control",
            "Distribution and access",
            "Audit and compliance"
        ],
        primary_authority=[
            "OEM Maintenance Manual",
            "FAA AC 120-78A",
            "EASA Part 145.A.45"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Task card control may require investment in document management systems.",
        counter_arguments=[
            "Accurate task cards prevent errors and improve efficiency.",
            "Electronic systems streamline control and distribution."
        ],
        resolution_strategy="Implement electronic task card management and audit usage regularly.",
        entity_scope="AERO07 Engine Maintenance Documentation",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Manual"
    ),
    DoctrineBlock(
        topic="Maintenance Facilities Security and Access Control",
        keywords=["security", "access control", "maintenance facilities", "asset protection", "regulatory compliance"],
        conclusion_template="AERO07 maintenance facilities must implement security and access control measures to protect assets and ensure regulatory compliance.",
        reasoning_framework="""
Security of AERO07 maintenance facilities is essential to protect assets, prevent unauthorized access, and comply with regulatory requirements. Measures include physical barriers, access control systems, personnel identification, and visitor management. Security incidents must be reported and investigated. Compliance with TSA and local regulations is required.
        """,
        key_factors=[
            "Physical security measures",
            "Access control systems",
            "Incident reporting",
            "Regulatory compliance"
        ],
        primary_authority=[
            "TSA 49 CFR 1542",
            "FAA AC 150/5210-49",
            "EASA Part 145.A.55"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Security measures may increase operational complexity.",
        counter_arguments=[
            "Security protects valuable assets and sensitive information.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Conduct regular security audits and train personnel in access control procedures.",
        entity_scope="AERO07 Engine Maintenance Facilities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="TSA 49 CFR 1542"
    ),
    DoctrineBlock(
        topic="Maintenance Planning and Scheduling Optimization",
        keywords=["maintenance planning", "scheduling", "optimization", "resource allocation", "downtime reduction"],
        conclusion_template="AERO07 maintenance planning must optimize scheduling to minimize downtime and maximize resource utilization.",
        reasoning_framework="""
Effective maintenance planning and scheduling for AERO07 reduces downtime, improves resource utilization, and ensures timely completion of required tasks. Planners must consider task priorities, parts availability, personnel, and operational requirements. Use of computerized maintenance management systems (CMMS) is recommended. Continuous review and adjustment improve efficiency.
        """,
        key_factors=[
            "Task prioritization",
            "Resource allocation",
            "Parts and personnel availability",
            "Use of CMMS"
        ],
        primary_authority=[
            "OEM Maintenance Planning Document",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Optimization may require investment in IT and training.",
        counter_arguments=[
            "Optimized planning reduces costs and improves reliability.",
            "CMMS systems are widely available and supported."
        ],
        resolution_strategy="Implement CMMS and provide training to planners and schedulers.",
        entity_scope="AERO07 Engine Maintenance Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Planning Document"
    ),
    DoctrineBlock(
        topic="Maintenance Cost Tracking and Control",
        keywords=["maintenance cost", "tracking", "control", "budgeting", "cost reduction"],
        conclusion_template="AERO07 operators must track and control maintenance costs to support budgeting and identify cost reduction opportunities.",
        reasoning_framework="""
Maintenance cost tracking for AERO07 involves collecting data on labor, parts, and overhead. Accurate tracking supports budgeting, cost analysis, and identification of inefficiencies. Operators should use financial management systems integrated with maintenance data. Regular review of costs enables identification of cost reduction opportunities without compromising safety.
        """,
        key_factors=[
            "Accurate cost data collection",
            "Integration with maintenance systems",
            "Regular cost review",
            "Cost reduction analysis"
        ],
        primary_authority=[
            "OEM Maintenance Management Guidelines",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Cost tracking may increase administrative workload.",
        counter_arguments=[
            "Cost control improves profitability and competitiveness.",
            "Integrated systems automate much of the process."
        ],
        resolution_strategy="Implement integrated cost tracking and review costs regularly with maintenance teams.",
        entity_scope="AERO07 Engine Operators",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Management Guidelines"
    ),
    DoctrineBlock(
        topic="Maintenance Contract Management and Performance Monitoring",
        keywords=["maintenance contract", "management", "performance monitoring", "service level agreement", "compliance"],
        conclusion_template="AERO07 maintenance contracts must be managed and monitored for performance and compliance with service level agreements.",
        reasoning_framework="""
Maintenance contracts for AERO07 must define service levels, performance metrics, and compliance requirements. Operators must monitor contractor performance, document compliance, and address deficiencies promptly. Regular contract reviews and performance audits ensure value for money and regulatory compliance.
        """,
        key_factors=[
            "Service level definition",
            "Performance monitoring",
            "Compliance documentation",
            "Contract review and audit"
        ],
        primary_authority=[
            "OEM Maintenance Contract Guidelines",
            "FAA AC 145-11",
            "EASA Part 145.A.75"
        ],
        burden_holder="Operator",
        adversary_position="Contract management may require dedicated resources.",
        counter_arguments=[
            "Effective contract management ensures quality and compliance.",
            "Performance monitoring identifies improvement opportunities."
        ],
        resolution_strategy="Assign contract managers and conduct regular performance reviews.",
        entity_scope="AERO07 Engine Maintenance Contracts",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Contract Guidelines"
    ),
    DoctrineBlock(
        topic="Maintenance Discrepancy Reporting and Resolution",
        keywords=["discrepancy", "reporting", "resolution", "maintenance", "corrective action"],
        conclusion_template="AERO07 maintenance discrepancies must be reported, tracked, and resolved with documented corrective actions.",
        reasoning_framework="""
Maintenance discrepancies (e.g., defects, out-of-tolerance findings) on AERO07 must be reported promptly, tracked in a discrepancy log, and resolved with documented corrective actions. Unresolved discrepancies must be reviewed before return to service. Regular review of discrepancy data supports continuous improvement.
        """,
        key_factors=[
            "Prompt reporting",
            "Discrepancy tracking",
            "Corrective action documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "OEM Maintenance Manual",
            "FAA AC 43-9C",
            "EASA Part 145.A.50"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Discrepancy tracking may increase administrative workload.",
        counter_arguments=[
            "Proper tracking ensures all issues are addressed before return to service.",
            "Data supports reliability improvement."
        ],
        resolution_strategy="Implement electronic discrepancy tracking and review logs regularly.",
        entity_scope="AERO07 Engine Maintenance Operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Manual"
    ),
    DoctrineBlock(
        topic="Maintenance Data Sharing and Industry Benchmarking",
        keywords=["data sharing", "industry benchmarking", "maintenance", "best practices", "continuous improvement"],
        conclusion_template="AERO07 operators are encouraged to share maintenance data and participate in industry benchmarking to improve best practices.",
        reasoning_framework="""
Sharing maintenance data and participating in industry benchmarking allows AERO07 operators to compare performance, identify best practices, and drive continuous improvement. Data sharing may be voluntary or required by OEM or regulatory authorities. Benchmarking supports identification of areas for improvement and adoption of proven solutions.
        """,
        key_factors=[
            "Data sharing agreements",
            "Benchmarking participation",
            "Performance analysis",
            "Continuous improvement"
        ],
        primary_authority=[
            "OEM Reliability Program",
            "FAA AC 120-17A",
            "EASA Part M"
        ],
        burden_holder="Operator",
        adversary_position="Data sharing may raise confidentiality concerns.",
        counter_arguments=[
            "Benchmarking improves safety and efficiency.",
            "Data can be anonymized to protect confidentiality."
        ],
        resolution_strategy="Participate in industry groups and anonymize data where necessary.",
        entity_scope="AERO07 Engine Operators",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Reliability Program"
    ),
    DoctrineBlock(
        topic="Customer Communication and Notification Procedures",
        keywords=["customer communication", "notification", "maintenance", "service disruption", "information sharing"],
        conclusion_template="AERO07 maintenance providers must have procedures for timely communication and notification to customers regarding maintenance status and disruptions.",
        reasoning_framework="""
Effective communication with customers (airlines, lessors) is essential during AERO07 maintenance, especially in case of delays or disruptions. Providers must have procedures for timely notification, status updates, and resolution of customer concerns. Documentation of communications supports transparency and customer satisfaction.
        """,
        key_factors=[
            "Notification procedures",
            "Status update frequency",
            "Documentation",
            "Customer feedback"
        ],
        primary_authority=[
            "OEM Customer Support Policy",
            "FAA AC 120-79A",
            "EASA Part M"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Frequent updates may increase administrative workload.",
        counter_arguments=[
            "Proactive communication improves customer satisfaction.",
            "Electronic systems can automate notifications."
        ],
        resolution_strategy="Implement customer communication protocols and document all notifications.",
        entity_scope="AERO07 Engine Maintenance Providers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Customer Support Policy"
    ),
    DoctrineBlock(
        topic="Incident and Accident Investigation Procedures",
        keywords=["incident", "accident", "investigation", "maintenance", "reporting"],
        conclusion_template="AERO07 operators must follow formal procedures for investigating and reporting incidents and accidents involving engine maintenance.",
        reasoning_framework="""
Incidents and accidents involving AERO07 maintenance require formal investigation to determine root cause and prevent recurrence. Procedures must comply with regulatory requirements, including prompt notification, evidence preservation, and reporting to authorities (NTSB, FAA, EASA). Findings inform safety improvements and may result in maintenance program changes.
        """,
        key_factors=[
            "Prompt notification",
            "Evidence preservation",
            "Root cause analysis",
            "Regulatory reporting"
        ],
        primary_authority=[
            "NTSB 49 CFR 830",
            "FAA Order 8020.11",
            "EASA Part 145.A.60"
        ],
        burden_holder="Operator",
        adversary_position="Investigations may delay return to service.",
        counter_arguments=[
            "Thorough investigation prevents future incidents.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Train personnel in investigation procedures and maintain incident logs.",
        entity_scope="AERO07 Engine Operators",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NTSB 49 CFR 830"
    ),
    DoctrineBlock(
        topic="Regulatory Change Management and Compliance Monitoring",
        keywords=["regulatory change", "management", "compliance", "monitoring", "maintenance program"],
        conclusion_template="AERO07 maintenance programs must include processes for monitoring and implementing regulatory changes.",
        reasoning_framework="""
Regulatory requirements for AERO07 maintenance evolve over time. Operators must monitor regulatory changes, assess impact, and update maintenance programs accordingly. Compliance monitoring ensures continued airworthiness and avoids penalties. Documentation of changes and communication to affected personnel are required.
        """,
        key_factors=[
            "Regulatory monitoring",
            "Impact assessment",
            "Program update procedures",
            "Communication and documentation"
        ],
        primary_authority=[
            "FAA AC 120-16G",
            "EASA Part M",
            "OEM Regulatory Affairs"
        ],
        burden_holder="Operator",
        adversary_position="Change management may increase administrative workload.",
        counter_arguments=[
            "Proactive management prevents compliance gaps.",
            "Electronic systems can automate monitoring."
        ],
        resolution_strategy="Assign regulatory affairs focal points and review changes regularly.",
        entity_scope="AERO07 Engine Operators",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-16G"
    ),
    DoctrineBlock(
        topic="Maintenance Human Resources Planning and Succession Management",
        keywords=["human resources", "succession management", "maintenance", "workforce planning", "competency"],
        conclusion_template="AERO07 maintenance organizations must plan for workforce needs and succession to ensure ongoing competency.",
        reasoning_framework="""
Effective human resources planning ensures that AERO07 maintenance organizations have sufficient qualified personnel to meet operational needs. Succession management addresses retirement, turnover, and promotion. Workforce planning must consider training, recruitment, and retention strategies. Documentation supports regulatory compliance and business continuity.
        """,
        key_factors=[
            "Workforce needs assessment",
            "Succession planning",
            "Training and recruitment",
            "Documentation"
        ],
        primary_authority=[
            "FAA AC 145-10",
            "EASA Part 145.A.30",
            "OEM HR Policy"
        ],
        burden_holder="Maintenance Organization",
        adversary_position="Workforce planning may require investment in HR systems.",
        counter_arguments=[
            "Succession management ensures business continuity.",
            "Proper planning reduces risk of skill gaps."
        ],
        resolution_strategy="Develop HR plans and review workforce needs annually.",
        entity_scope="AERO07 Engine Maintenance Organizations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 145-10"
    ),
    DoctrineBlock(
        topic="Maintenance-Related Occupational Health and Safety Compliance",
        keywords=["occupational health", "safety", "compliance", "maintenance", "OSHA"],
        conclusion_template="AERO07 maintenance facilities must comply with occupational health and safety regulations to protect personnel.",
        reasoning_framework="""
Occupational health and safety compliance is essential in AERO07 maintenance environments. Facilities must meet OSHA and local safety standards, including hazard communication, PPE, and incident reporting. Regular safety audits and training are required. Non-compliance can result in injuries, fines, and operational disruption.
        """,
        key_factors=[
            "Hazard identification",
            "PPE and safety equipment",
            "Incident reporting",
            "Training and audits"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910",
            "EASA Part 145.A.30",
            "OEM Safety Policy"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Safety compliance may require investment in equipment and training.",
        counter_arguments=[
            "Protecting personnel is a legal and ethical obligation.",
            "Proper safety reduces lost time and insurance costs."
        ],
        resolution_strategy="Conduct regular safety training and audits.",
        entity_scope="AERO07 Engine Maintenance Facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OSHA 29 CFR 1910"
    ),
    DoctrineBlock(
        topic="Maintenance IT Systems Security and Data Protection",
        keywords=["IT systems", "security", "data protection", "maintenance", "cybersecurity"],
        conclusion_template="AERO07 maintenance IT systems must be secured to protect sensitive data and ensure operational continuity.",
        reasoning_framework="""
IT systems supporting AERO07 maintenance (e.g., CMMS