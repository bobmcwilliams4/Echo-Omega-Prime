import enum
from dataclasses import dataclass, field
from typing import List, Optional
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
        topic="CBHP MPD Fundamental Principle",
        keywords=["CBHP", "MPD", "Managed Pressure Drilling", "Bottomhole Pressure", "Hydrostatic", "Surface Backpressure"],
        conclusion_template="Maintaining a constant bottomhole pressure (CBHP) is essential to MPD operations, achieved by dynamically adjusting surface backpressure and fluid density.",
        reasoning_framework="""
1. The primary objective of CBHP MPD is to maintain the bottomhole pressure (BHP) within a narrow window between pore and fracture pressures.
2. This is achieved by manipulating surface backpressure using a choke manifold and, if necessary, adjusting mud weight.
3. The system must respond dynamically to changes in wellbore conditions, such as influxes, losses, or changes in drilling parameters.
4. Real-time pressure monitoring and automated choke control are critical for maintaining CBHP.
5. Failure to maintain CBHP can result in well control incidents, formation influx, or losses.
6. The doctrine is supported by IADC MPD guidelines and API RP 92M.
7. The CBHP principle underpins all MPD variants and is a controlling factor in equipment selection and operational procedures.
8. The doctrine is universally applicable to all MPD wells except where PMCD is intentionally applied.
9. The operator holds the burden to demonstrate that CBHP is maintained at all times during MPD operations.
10. Adversaries may argue that CBHP is not always practical in highly depleted or fractured formations.
11. Counter-arguments rely on technological advances in real-time monitoring and automated control.
12. Resolution involves risk assessment, equipment redundancy, and adherence to industry standards.
""",
        key_factors=[
            "Real-time BHP monitoring",
            "Choke control system responsiveness",
            "Mud weight management",
            "Drilling parameter changes",
            "Wellbore stability"
        ],
        primary_authority=[
            "IADC MPD Guidelines",
            "API RP 92M",
            "Operator Well Control Policy"
        ],
        burden_holder="Operator",
        adversary_position="CBHP is not always feasible in complex or depleted formations.",
        counter_arguments=[
            "Advanced automation and instrumentation enable CBHP in most scenarios.",
            "Risk-based exceptions must be justified and documented."
        ],
        resolution_strategy="Apply risk assessment, ensure equipment redundancy, and adhere to API/IADC standards.",
        entity_scope="All MPD operations using CBHP mode",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 5.2"
    ),
    DoctrineBlock(
        topic="RCD Selection and Rating Criteria",
        keywords=["RCD", "Rotating Control Device", "Pressure Rating", "MPD", "Seal Element", "Certification"],
        conclusion_template="RCDs must be selected and rated based on maximum anticipated surface pressure, certification, and compatibility with the drilling program.",
        reasoning_framework="""
1. The RCD is a primary pressure-containing barrier in MPD operations.
2. Selection is based on maximum anticipated surface pressure (MASP), wellhead configuration, and operational envelope.
3. RCDs must be certified to API 16RCD or equivalent, with traceable documentation.
4. Seal element material must be compatible with drilling fluids, temperature, and expected wear.
5. The RCD must be tested and maintained per manufacturer and API recommendations.
6. The operator is responsible for ensuring RCD integrity and suitability.
7. Adversaries may argue for cost-saving by using lower-rated or uncertified RCDs.
8. Counter-arguments cite regulatory and safety requirements.
9. Resolution involves strict adherence to certification and testing protocols.
""",
        key_factors=[
            "MASP",
            "Seal element material compatibility",
            "Certification and documentation",
            "Maintenance and testing records"
        ],
        primary_authority=[
            "API 16RCD",
            "Operator Equipment Policy"
        ],
        burden_holder="Operator",
        adversary_position="Lower-rated or uncertified RCDs are sufficient for some operations.",
        counter_arguments=[
            "Regulatory compliance and safety require certified RCDs.",
            "Failure history supports strict adherence to rating criteria."
        ],
        resolution_strategy="Enforce certification, perform regular testing, and maintain records.",
        entity_scope="All wells using RCDs in MPD",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 16RCD Section 7"
    ),
    DoctrineBlock(
        topic="Pressurized Mud Cap Drilling (PMCD) for Total Losses",
        keywords=["PMCD", "Total Losses", "MPD", "Mud Cap", "Well Control", "Fractured Formation"],
        conclusion_template="PMCD is the preferred MPD variant for drilling in total loss zones where CBHP cannot be maintained.",
        reasoning_framework="""
1. PMCD is applied when formation losses prevent maintaining CBHP.
2. The well is operated with a mud cap above the loss zone and a sacrificial fluid is injected below.
3. The objective is to continue drilling while preventing surface influx and maintaining well control.
4. PMCD requires specialized procedures for fluid management and monitoring.
5. The operator must demonstrate that CBHP is not feasible before switching to PMCD.
6. Adversaries may argue for continued CBHP attempts or alternative loss mitigation.
7. Counter-arguments focus on operational efficiency and safety.
8. Resolution involves risk assessment and regulatory notification.
""",
        key_factors=[
            "Loss zone characterization",
            "Mud cap integrity",
            "Fluid management procedures",
            "Well control monitoring"
        ],
        primary_authority=[
            "IADC MPD Guidelines",
            "API RP 92M"
        ],
        burden_holder="Operator",
        adversary_position="CBHP should be maintained at all costs.",
        counter_arguments=[
            "PMCD is safer and more efficient in total loss scenarios.",
            "Industry guidelines support PMCD application."
        ],
        resolution_strategy="Document loss history, perform risk assessment, and notify regulators.",
        entity_scope="MPD operations in total loss zones",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 6.4"
    ),
    DoctrineBlock(
        topic="Dual Gradient Drilling - Subsea Mudlift System",
        keywords=["Dual Gradient", "Subsea Mudlift", "Deepwater", "MPD", "Riser", "Pressure Management"],
        conclusion_template="Dual gradient drilling with a subsea mudlift system enables precise pressure management in deepwater wells by decoupling riser and wellbore gradients.",
        reasoning_framework="""
1. Dual gradient drilling (DGD) addresses narrow pressure windows in deepwater by reducing riser hydrostatic pressure.
2. Subsea mudlift pumps return mud to the surface, allowing independent control of riser and wellbore pressures.
3. This enables drilling in formations that would otherwise be inaccessible due to narrow margins.
4. The system requires robust equipment and real-time monitoring.
5. The operator must demonstrate technical and operational readiness for DGD.
6. Adversaries may claim increased complexity and cost.
7. Counter-arguments highlight improved safety and access to reserves.
8. Resolution involves cost-benefit analysis and regulatory engagement.
""",
        key_factors=[
            "Riser pressure management",
            "Mudlift pump reliability",
            "Real-time monitoring",
            "Operational readiness"
        ],
        primary_authority=[
            "API RP 92P",
            "IADC DGD Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="DGD is too complex and costly for most projects.",
        counter_arguments=[
            "DGD enables access to reserves otherwise undrillable.",
            "Safety and well control benefits outweigh complexity."
        ],
        resolution_strategy="Perform cost-benefit analysis and engage with regulators.",
        entity_scope="Deepwater MPD operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 92P Section 8"
    ),
    DoctrineBlock(
        topic="Automated Choke Control - PID Loop Tuning",
        keywords=["Automated Choke", "PID", "Control Loop", "MPD", "Pressure Control", "Tuning"],
        conclusion_template="Automated choke control systems must be properly tuned using PID parameters to ensure stable and responsive pressure management.",
        reasoning_framework="""
1. Automated choke systems use PID control loops to maintain setpoint pressures.
2. Proper tuning of proportional, integral, and derivative parameters is essential for system stability.
3. Poorly tuned systems can lead to oscillations, slow response, or loss of control.
4. Tuning must be performed during commissioning and revisited after significant system changes.
5. The operator is responsible for ensuring tuning is documented and validated.
6. Adversaries may argue manual control is sufficient.
7. Counter-arguments cite human limitations and the need for rapid response.
8. Resolution involves training, documentation, and periodic review.
""",
        key_factors=[
            "PID parameter selection",
            "System response time",
            "Pressure setpoint stability",
            "Operator training"
        ],
        primary_authority=[
            "API RP 92M",
            "Vendor Control System Manuals"
        ],
        burden_holder="Operator",
        adversary_position="Manual choke control is adequate for most wells.",
        counter_arguments=[
            "Automated control provides faster and more consistent response.",
            "Industry incidents support automation."
        ],
        resolution_strategy="Document tuning procedures and provide operator training.",
        entity_scope="All MPD operations using automated choke systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.3"
    ),
    DoctrineBlock(
        topic="Narrow Margin Drilling - Pore Pressure to Frac Gradient",
        keywords=["Narrow Margin", "Pore Pressure", "Fracture Gradient", "MPD", "Well Design", "Pressure Window"],
        conclusion_template="MPD enables drilling in narrow margin wells by precisely managing bottomhole pressure between pore and fracture gradients.",
        reasoning_framework="""
1. Narrow margin wells have a small window between pore pressure and fracture gradient.
2. MPD allows for dynamic adjustment of BHP to stay within this window.
3. Real-time data and automated control systems are essential.
4. Well design must consider margin variability and contingency planning.
5. The operator must document margin calculations and MPD procedures.
6. Adversaries may argue for conventional drilling with higher mud weights.
7. Counter-arguments focus on reduced risk of losses and kicks.
8. Resolution involves engineering review and regulatory approval.
""",
        key_factors=[
            "Margin calculation accuracy",
            "Real-time pressure data",
            "Automated control systems",
            "Well design documentation"
        ],
        primary_authority=[
            "API RP 92M",
            "IADC Well Control Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Conventional drilling is sufficient with higher mud weights.",
        counter_arguments=[
            "Higher mud weights increase risk of losses and formation damage.",
            "MPD provides safer, more precise control."
        ],
        resolution_strategy="Perform engineering review and obtain regulatory approval.",
        entity_scope="Narrow margin MPD wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 5.4"
    ),
    DoctrineBlock(
        topic="Kick Detection Sensitivity in MPD Operations",
        keywords=["Kick Detection", "MPD", "Sensitivity", "Flow Monitoring", "Well Control", "Early Warning"],
        conclusion_template="MPD operations must employ high-sensitivity kick detection systems to enable early intervention and maintain well control.",
        reasoning_framework="""
1. Early kick detection is critical for well control in MPD operations.
2. High-sensitivity flow and pressure monitoring systems are required.
3. Automated alarms and trending analysis enhance detection capability.
4. The operator must calibrate and test detection systems regularly.
5. Adversaries may argue that standard systems are sufficient.
6. Counter-arguments cite the reduced margin for error in MPD wells.
7. Resolution involves technology upgrades and procedural enforcement.
""",
        key_factors=[
            "Flow and pressure sensor accuracy",
            "Alarm system configuration",
            "Calibration and testing frequency",
            "Operator response procedures"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Well Control Manual"
        ],
        burden_holder="Operator",
        adversary_position="Standard kick detection systems are adequate.",
        counter_arguments=[
            "MPD wells have less margin for error, requiring higher sensitivity.",
            "Early detection reduces risk of escalation."
        ],
        resolution_strategy="Upgrade technology and enforce calibration/testing protocols.",
        entity_scope="All MPD wells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 8.2"
    ),
    DoctrineBlock(
        topic="IADC MPD Classification - Reactive vs Proactive",
        keywords=["IADC", "MPD", "Classification", "Reactive", "Proactive", "Well Control"],
        conclusion_template="MPD applications are classified as reactive or proactive based on the primary objective: well control response or pressure management.",
        reasoning_framework="""
1. IADC classifies MPD as reactive (responding to well control events) or proactive (preventing influx/losses).
2. Proactive MPD focuses on precise pressure management to avoid incidents.
3. Reactive MPD is initiated in response to detected well control issues.
4. The classification impacts equipment selection, procedures, and regulatory requirements.
5. The operator must document the intended MPD application.
6. Adversaries may argue for a hybrid approach.
7. Counter-arguments emphasize clarity for safety and compliance.
8. Resolution involves clear documentation and regulatory engagement.
""",
        key_factors=[
            "MPD objective definition",
            "Documentation of application",
            "Equipment and procedure selection",
            "Regulatory requirements"
        ],
        primary_authority=[
            "IADC MPD Guidelines",
            "API RP 92M"
        ],
        burden_holder="Operator",
        adversary_position="Hybrid or undefined MPD applications are acceptable.",
        counter_arguments=[
            "Clarity improves safety and regulatory compliance.",
            "Hybrid approaches must be clearly justified."
        ],
        resolution_strategy="Document MPD classification and engage with regulators.",
        entity_scope="All MPD projects",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IADC MPD Classification Framework"
    ),
    DoctrineBlock(
        topic="MPD Well Design - Casing Shoe Depth Optimization",
        keywords=["MPD", "Well Design", "Casing Shoe", "Depth Optimization", "Pressure Window", "Contingency"],
        conclusion_template="Casing shoe depth in MPD wells must be optimized to maximize pressure window utilization and allow for contingency operations.",
        reasoning_framework="""
1. Casing shoe depth determines the available pressure window for subsequent drilling.
2. MPD enables deeper shoe setting by managing BHP more precisely.
3. Optimization involves balancing operational risk, formation integrity, and contingency planning.
4. The operator must document shoe depth selection and supporting analysis.
5. Adversaries may argue for conservative, shallower shoe depths.
6. Counter-arguments focus on improved efficiency and reduced casing strings.
7. Resolution involves peer review and regulatory approval.
""",
        key_factors=[
            "Pressure window analysis",
            "Formation integrity tests",
            "Contingency planning",
            "Well design documentation"
        ],
        primary_authority=[
            "API RP 92M",
            "IADC Well Construction Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Shallower shoe depths are safer and more conservative.",
        counter_arguments=[
            "MPD allows for deeper, more efficient shoe setting.",
            "Contingency planning mitigates risk."
        ],
        resolution_strategy="Conduct peer review and obtain regulatory approval.",
        entity_scope="MPD well design",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 4.3"
    ),
    DoctrineBlock(
        topic="MPD System Redundancy Requirements",
        keywords=["MPD", "System Redundancy", "Equipment", "Reliability", "Well Control", "Backup"],
        conclusion_template="Critical MPD components must have redundancy to ensure operational continuity and well control integrity.",
        reasoning_framework="""
1. Redundancy in critical MPD systems (choke, RCD, sensors) reduces risk of single-point failure.
2. Backup systems must be tested and available during operations.
3. The operator must document redundancy provisions and test results.
4. Adversaries may argue redundancy increases cost and complexity.
5. Counter-arguments focus on incident history and regulatory requirements.
6. Resolution involves risk assessment and cost-benefit analysis.
""",
        key_factors=[
            "Identification of critical components",
            "Backup system availability",
            "Testing and documentation",
            "Risk assessment"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Equipment Policy"
        ],
        burden_holder="Operator",
        adversary_position="Redundancy is unnecessary and costly.",
        counter_arguments=[
            "Incident history supports redundancy.",
            "Regulatory requirements mandate backup systems."
        ],
        resolution_strategy="Perform risk assessment and enforce redundancy protocols.",
        entity_scope="All MPD operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.4"
    ),
    DoctrineBlock(
        topic="MPD Operations - Regulatory Notification and Reporting",
        keywords=["MPD", "Regulatory", "Notification", "Reporting", "Compliance", "Documentation"],
        conclusion_template="Operators must notify regulators before commencing MPD operations and submit required reports as per jurisdictional requirements.",
        reasoning_framework="""
1. Regulatory bodies require notification prior to MPD operations.
2. Documentation must include MPD procedures, risk assessments, and equipment certifications.
3. Ongoing reporting of incidents, deviations, and performance is required.
4. The operator is responsible for compliance and timely submissions.
5. Adversaries may argue for minimal reporting to reduce administrative burden.
6. Counter-arguments cite transparency and regulatory oversight.
7. Resolution involves establishing internal compliance systems.
""",
        key_factors=[
            "Notification procedures",
            "Documentation completeness",
            "Timeliness of reporting",
            "Regulatory engagement"
        ],
        primary_authority=[
            "Jurisdictional Regulations",
            "API RP 92M"
        ],
        burden_holder="Operator",
        adversary_position="Minimal reporting is sufficient.",
        counter_arguments=[
            "Transparency and oversight improve safety.",
            "Non-compliance risks regulatory action."
        ],
        resolution_strategy="Establish internal compliance and audit systems.",
        entity_scope="All MPD operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Jurisdictional Regulatory Codes"
    ),
    DoctrineBlock(
        topic="MPD Crew Training and Competency Standards",
        keywords=["MPD", "Crew Training", "Competency", "Certification", "Well Control", "Human Factors"],
        conclusion_template="All MPD crew members must meet competency standards and receive specialized training in MPD equipment and procedures.",
        reasoning_framework="""
1. MPD operations require specialized skills beyond conventional drilling.
2. Crew competency reduces risk of human error and well control incidents.
3. Training must cover equipment operation, emergency procedures, and well control.
4. Certification and periodic refresher courses are required.
5. The operator is responsible for maintaining training records.
6. Adversaries may argue for on-the-job training only.
7. Counter-arguments cite incident investigations and regulatory requirements.
8. Resolution involves third-party certification and audits.
""",
        key_factors=[
            "Training curriculum",
            "Certification records",
            "Emergency procedure drills",
            "Competency assessment"
        ],
        primary_authority=[
            "IADC Well Control Guidelines",
            "Operator Training Policy"
        ],
        burden_holder="Operator",
        adversary_position="On-the-job training is sufficient.",
        counter_arguments=[
            "Specialized training reduces risk.",
            "Certification is required by regulators."
        ],
        resolution_strategy="Implement third-party certification and regular audits.",
        entity_scope="All MPD crew",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="IADC Well Control Guidelines Section 9"
    ),
    DoctrineBlock(
        topic="MPD Well Control Transition Procedures",
        keywords=["MPD", "Well Control", "Transition", "Procedures", "Contingency", "Hand-off"],
        conclusion_template="Clear procedures must be in place for transitioning from MPD to conventional well control in the event of an incident.",
        reasoning_framework="""
1. Transitioning from MPD to conventional well control is a critical operation.
2. Procedures must define triggers, roles, communication, and equipment hand-off.
3. Training and drills are required to ensure crew readiness.
4. The operator must document and review transition procedures regularly.
5. Adversaries may argue that transitions are intuitive and need no documentation.
6. Counter-arguments cite incident history and regulatory findings.
7. Resolution involves procedural enforcement and regular drills.
""",
        key_factors=[
            "Transition trigger definition",
            "Role assignment",
            "Communication protocols",
            "Drill frequency"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Well Control Manual"
        ],
        burden_holder="Operator",
        adversary_position="Transitions are intuitive and do not require formal procedures.",
        counter_arguments=[
            "Incidents have occurred due to unclear transitions.",
            "Regulators require documented procedures."
        ],
        resolution_strategy="Document procedures and conduct regular drills.",
        entity_scope="All MPD operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 8.3"
    ),
    DoctrineBlock(
        topic="MPD Data Acquisition and Real-Time Monitoring",
        keywords=["MPD", "Data Acquisition", "Real-Time Monitoring", "Sensors", "Data Quality", "Decision Support"],
        conclusion_template="MPD operations require high-quality real-time data acquisition and monitoring systems for effective decision-making.",
        reasoning_framework="""
1. Real-time data is essential for MPD pressure management and well control.
2. Systems must capture flow, pressure, temperature, and other critical parameters.
3. Data quality assurance and redundancy are required.
4. The operator must ensure data is accessible for decision support and regulatory review.
5. Adversaries may argue for minimal instrumentation.
6. Counter-arguments cite the need for rapid response and incident prevention.
7. Resolution involves technology investment and quality control.
""",
        key_factors=[
            "Sensor accuracy",
            "Data redundancy",
            "System uptime",
            "Data accessibility"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Data Policy"
        ],
        burden_holder="Operator",
        adversary_position="Minimal instrumentation is sufficient.",
        counter_arguments=[
            "High-quality data enables rapid, informed decisions.",
            "Regulatory review requires comprehensive data."
        ],
        resolution_strategy="Invest in technology and implement quality control.",
        entity_scope="All MPD operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.2"
    ),
    DoctrineBlock(
        topic="MPD Equipment Maintenance and Inspection",
        keywords=["MPD", "Equipment", "Maintenance", "Inspection", "Reliability", "Preventive"],
        conclusion_template="All MPD equipment must be maintained and inspected per manufacturer and industry standards to ensure reliability.",
        reasoning_framework="""
1. Equipment reliability is critical for MPD safety and performance.
2. Maintenance schedules must follow manufacturer and API recommendations.
3. Inspection records must be maintained and available for audit.
4. The operator is responsible for preventive maintenance and timely repairs.
5. Adversaries may argue for reactive maintenance only.
6. Counter-arguments cite failure history and regulatory requirements.
7. Resolution involves preventive maintenance programs and audits.
""",
        key_factors=[
            "Maintenance schedule adherence",
            "Inspection record keeping",
            "Preventive vs reactive maintenance",
            "Audit readiness"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Maintenance Policy"
        ],
        burden_holder="Operator",
        adversary_position="Reactive maintenance is sufficient.",
        counter_arguments=[
            "Preventive maintenance reduces failure risk.",
            "Regulators require documented maintenance."
        ],
        resolution_strategy="Implement preventive maintenance and maintain records.",
        entity_scope="All MPD equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.5"
    ),
    DoctrineBlock(
        topic="MPD Kick Tolerance Calculations",
        keywords=["MPD", "Kick Tolerance", "Calculations", "Well Control", "Design", "Safety Margin"],
        conclusion_template="Kick tolerance must be calculated for all MPD wells, considering dynamic pressure management and operational contingencies.",
        reasoning_framework="""
1. Kick tolerance defines the maximum influx that can be safely handled.
2. MPD requires dynamic calculations due to variable BHP management.
3. Calculations must include operational contingencies and equipment limits.
4. The operator must document and review kick tolerance regularly.
5. Adversaries may argue for static, conventional calculations.
6. Counter-arguments focus on MPD-specific risks and variability.
7. Resolution involves engineering review and procedural updates.
""",
        key_factors=[
            "Dynamic BHP management",
            "Equipment limits",
            "Operational contingencies",
            "Documentation and review"
        ],
        primary_authority=[
            "API RP 92M",
            "IADC Well Control Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Static kick tolerance calculations are sufficient.",
        counter_arguments=[
            "MPD operations require dynamic, scenario-based calculations.",
            "Safety margins must reflect operational realities."
        ],
        resolution_strategy="Perform dynamic calculations and update procedures.",
        entity_scope="All MPD well designs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 5.5"
    ),
    DoctrineBlock(
        topic="MPD Integration with Drilling Automation Systems",
        keywords=["MPD", "Drilling Automation", "Integration", "Control Systems", "Interoperability", "Data Exchange"],
        conclusion_template="MPD systems must be integrated with drilling automation platforms to enable coordinated control and data exchange.",
        reasoning_framework="""
1. Integration enables coordinated control of drilling and MPD systems.
2. Data exchange improves decision-making and automation effectiveness.
3. Interoperability standards must be followed to ensure compatibility.
4. The operator is responsible for integration planning and testing.
5. Adversaries may argue for standalone MPD systems.
6. Counter-arguments cite improved safety and efficiency.
7. Resolution involves technology selection and interface validation.
""",
        key_factors=[
            "Interoperability standards",
            "Data exchange protocols",
            "Integration testing",
            "Operator training"
        ],
        primary_authority=[
            "API RP 92M",
            "Vendor Integration Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Standalone MPD systems are sufficient.",
        counter_arguments=[
            "Integration improves safety and operational efficiency.",
            "Automation requires coordinated control."
        ],
        resolution_strategy="Follow interoperability standards and validate interfaces.",
        entity_scope="MPD and drilling automation systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.6"
    ),
    DoctrineBlock(
        topic="MPD Drilling Fluid Selection and Management",
        keywords=["MPD", "Drilling Fluid", "Selection", "Management", "Rheology", "Compatibility"],
        conclusion_template="Drilling fluid selection for MPD must consider rheology, compatibility with equipment, and pressure management objectives.",
        reasoning_framework="""
1. Fluid properties affect MPD pressure management and equipment performance.
2. Selection must consider rheology, density, and compatibility with RCD seals and sensors.
3. Fluid management includes monitoring, treatment, and contingency planning.
4. The operator must document fluid selection criteria and management procedures.
5. Adversaries may argue for conventional fluid programs.
6. Counter-arguments focus on MPD-specific requirements and equipment compatibility.
7. Resolution involves engineering review and vendor consultation.
""",
        key_factors=[
            "Rheological properties",
            "Equipment compatibility",
            "Fluid management procedures",
            "Contingency planning"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Fluid Policy"
        ],
        burden_holder="Operator",
        adversary_position="Conventional fluid programs are sufficient.",
        counter_arguments=[
            "MPD requires fluids compatible with specialized equipment.",
            "Pressure management objectives dictate fluid selection."
        ],
        resolution_strategy="Document selection criteria and consult with vendors.",
        entity_scope="MPD drilling fluids",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 6.2"
    ),
    DoctrineBlock(
        topic="MPD Emergency Shutdown and Isolation Procedures",
        keywords=["MPD", "Emergency Shutdown", "Isolation", "Procedures", "Well Control", "Contingency"],
        conclusion_template="MPD operations must have documented emergency shutdown and isolation procedures, including roles and equipment actions.",
        reasoning_framework="""
1. Emergency shutdowns are critical for well control and crew safety.
2. Procedures must define triggers, roles, and equipment actions (e.g., closing RCD, isolating choke).
3. Training and drills are required to ensure crew readiness.
4. The operator must review and update procedures regularly.
5. Adversaries may argue for informal, experience-based responses.
6. Counter-arguments cite regulatory requirements and incident history.
7. Resolution involves procedural enforcement and regular drills.
""",
        key_factors=[
            "Trigger definition",
            "Role assignment",
            "Equipment isolation steps",
            "Drill frequency"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Emergency Response Plan"
        ],
        burden_holder="Operator",
        adversary_position="Informal responses are sufficient.",
        counter_arguments=[
            "Documented procedures reduce confusion and error.",
            "Regulators require formal emergency plans."
        ],
        resolution_strategy="Document and drill emergency procedures.",
        entity_scope="All MPD operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 8.5"
    ),
    DoctrineBlock(
        topic="MPD Well Integrity Testing",
        keywords=["MPD", "Well Integrity", "Testing", "Pressure Test", "Barriers", "Verification"],
        conclusion_template="All MPD wells must undergo integrity testing of barriers and pressure-containing equipment before and during operations.",
        reasoning_framework="""
1. Well integrity testing verifies the effectiveness of pressure barriers.
2. Tests must be conducted before operations and after any significant event or equipment change.
3. Documentation of test results is required for audit and regulatory review.
4. The operator is responsible for test planning and execution.
5. Adversaries may argue for reduced testing frequency.
6. Counter-arguments focus on risk reduction and regulatory compliance.
7. Resolution involves adherence to testing schedules and documentation.
""",
        key_factors=[
            "Test frequency",
            "Barrier verification",
            "Documentation",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Well Integrity Policy"
        ],
        burden_holder="Operator",
        adversary_position="Reduced testing frequency is sufficient.",
        counter_arguments=[
            "Frequent testing reduces risk of barrier failure.",
            "Regulators require documented integrity tests."
        ],
        resolution_strategy="Adhere to test schedules and maintain records.",
        entity_scope="All MPD wells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 6.3"
    ),
    DoctrineBlock(
        topic="MPD Annular Pressure Profile Management",
        keywords=["MPD", "Annular Pressure", "Profile Management", "Pressure Gradient", "Wellbore Stability"],
        conclusion_template="Annular pressure profiles must be managed dynamically to maintain wellbore stability and prevent influx or losses.",
        reasoning_framework="""
1. MPD enables real-time management of annular pressure profiles.
2. Dynamic adjustments are required to respond to formation changes and operational events.
3. The operator must monitor and document pressure profiles continuously.
4. Adversaries may argue for static pressure management.
5. Counter-arguments cite the benefits of dynamic control for wellbore stability.
6. Resolution involves technology investment and procedural updates.
""",
        key_factors=[
            "Real-time monitoring",
            "Dynamic adjustment capability",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "API RP 92M",
            "IADC MPD Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Static pressure management is sufficient.",
        counter_arguments=[
            "Dynamic management improves wellbore stability.",
            "MPD technology enables real-time adjustments."
        ],
        resolution_strategy="Invest in real-time monitoring and update procedures.",
        entity_scope="All MPD wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 5.6"
    ),
    DoctrineBlock(
        topic="MPD Surface Backpressure Management",
        keywords=["MPD", "Surface Backpressure", "Choke Control", "Pressure Management", "Well Control"],
        conclusion_template="Surface backpressure must be managed using automated or manual choke systems to maintain target bottomhole pressure.",
        reasoning_framework="""
1. Surface backpressure is a primary means of controlling BHP in MPD.
2. Automated choke systems are preferred for precision and responsiveness.
3. Manual override capability must be available for contingency.
4. The operator must document backpressure management procedures.
5. Adversaries may argue for manual control only.
6. Counter-arguments cite improved safety and control with automation.
7. Resolution involves technology selection and operator training.
""",
        key_factors=[
            "Choke system capability",
            "Manual override procedures",
            "Operator training",
            "Documentation"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Well Control Manual"
        ],
        burden_holder="Operator",
        adversary_position="Manual choke control is sufficient.",
        counter_arguments=[
            "Automated systems provide faster, more precise control.",
            "Manual override ensures contingency readiness."
        ],
        resolution_strategy="Document procedures and provide operator training.",
        entity_scope="All MPD operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.3"
    ),
    DoctrineBlock(
        topic="MPD Managed Wellbore Strengthening",
        keywords=["MPD", "Wellbore Strengthening", "Lost Circulation", "Pressure Management", "Drilling Fluid"],
        conclusion_template="MPD can be used to strengthen wellbores by managing pressure and fluid properties to mitigate lost circulation.",
        reasoning_framework="""
1. Wellbore strengthening involves increasing the effective fracture gradient.
2. MPD enables precise pressure management to minimize losses.
3. Drilling fluids may be engineered to seal fractures and support wellbore integrity.
4. The operator must document strengthening strategies and results.
5. Adversaries may argue for conventional lost circulation material (LCM) only.
6. Counter-arguments cite the benefits of dynamic pressure management.
7. Resolution involves engineering review and procedural updates.
""",
        key_factors=[
            "Pressure management capability",
            "Fluid engineering",
            "Documentation",
            "Lost circulation history"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Drilling Fluid Policy"
        ],
        burden_holder="Operator",
        adversary_position="LCM is sufficient for lost circulation.",
        counter_arguments=[
            "MPD provides additional strengthening via pressure management.",
            "Combined approaches are most effective."
        ],
        resolution_strategy="Document strategies and review engineering results.",
        entity_scope="MPD wells with lost circulation risk",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 6.5"
    ),
    DoctrineBlock(
        topic="MPD Well Control Event Investigation and Reporting",
        keywords=["MPD", "Well Control Event", "Investigation", "Reporting", "Root Cause", "Regulatory"],
        conclusion_template="All MPD well control events must be investigated, documented, and reported to regulators with root cause analysis.",
        reasoning_framework="""
1. Incident investigation identifies root causes and corrective actions.
2. Documentation supports regulatory compliance and organizational learning.
3. The operator must submit reports per jurisdictional requirements.
4. Adversaries may argue for internal-only investigations.
5. Counter-arguments cite transparency and industry improvement.
6. Resolution involves formal investigation protocols and regulatory engagement.
""",
        key_factors=[
            "Root cause analysis",
            "Documentation",
            "Regulatory reporting",
            "Corrective action tracking"
        ],
        primary_authority=[
            "Jurisdictional Regulations",
            "Operator Incident Policy"
        ],
        burden_holder="Operator",
        adversary_position="Internal investigation is sufficient.",
        counter_arguments=[
            "Regulators require formal reporting.",
            "Transparency improves industry safety."
        ],
        resolution_strategy="Follow formal protocols and engage with regulators.",
        entity_scope="All MPD well control events",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Jurisdictional Regulatory Codes"
    ),
    DoctrineBlock(
        topic="MPD Pressure Testing of Surface Equipment",
        keywords=["MPD", "Pressure Testing", "Surface Equipment", "Verification", "Integrity", "Documentation"],
        conclusion_template="All MPD surface equipment must be pressure tested before use and after maintenance to verify integrity.",
        reasoning_framework="""
1. Pressure testing verifies the integrity of surface equipment (RCD, choke, manifolds).
2. Tests must be performed before initial use and after any maintenance or repair.
3. Documentation of test results is required for audit and regulatory review.
4. The operator is responsible for test planning and execution.
5. Adversaries may argue for reduced testing frequency.
6. Counter-arguments cite equipment failure history and regulatory requirements.
7. Resolution involves adherence to testing schedules and documentation.
""",
        key_factors=[
            "Test frequency",
            "Test documentation",
            "Equipment identification",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Equipment Policy"
        ],
        burden_holder="Operator",
        adversary_position="Reduced testing is sufficient.",
        counter_arguments=[
            "Frequent testing reduces risk of failure.",
            "Regulators require documented tests."
        ],
        resolution_strategy="Adhere to test schedules and maintain records.",
        entity_scope="All MPD surface equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.7"
    ),
    DoctrineBlock(
        topic="MPD Well Construction Risk Assessment",
        keywords=["MPD", "Well Construction", "Risk Assessment", "Hazard Identification", "Mitigation", "Contingency"],
        conclusion_template="A comprehensive risk assessment must be conducted for all MPD well construction projects, including hazard identification and mitigation planning.",
        reasoning_framework="""
1. Risk assessment identifies hazards and informs mitigation strategies.
2. The process must cover all phases of well construction.
3. Documentation supports regulatory compliance and operational readiness.
4. The operator is responsible for updating assessments as conditions change.
5. Adversaries may argue for informal risk management.
6. Counter-arguments cite regulatory requirements and incident history.
7. Resolution involves formal risk assessment protocols and regular review.
""",
        key_factors=[
            "Hazard identification",
            "Mitigation planning",
            "Documentation",
            "Review frequency"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Risk Management Policy"
        ],
        burden_holder="Operator",
        adversary_position="Informal risk management is sufficient.",
        counter_arguments=[
            "Formal risk assessment reduces incidents.",
            "Regulators require documented assessments."
        ],
        resolution_strategy="Follow formal protocols and review regularly.",
        entity_scope="All MPD well construction projects",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 4.2"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Certification",
        keywords=["MPD", "Well Control Equipment", "Certification", "Compliance", "Inspection", "Documentation"],
        conclusion_template="All MPD well control equipment must be certified and documented for compliance with industry standards.",
        reasoning_framework="""
1. Certification ensures equipment meets industry standards for safety and performance.
2. Documentation must be traceable and available for audit.
3. The operator is responsible for verifying certification status.
4. Adversaries may argue for use of uncertified equipment to reduce cost.
5. Counter-arguments cite regulatory requirements and incident history.
6. Resolution involves strict certification protocols and audits.
""",
        key_factors=[
            "Certification status",
            "Documentation",
            "Audit readiness",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Equipment Policy"
        ],
        burden_holder="Operator",
        adversary_position="Uncertified equipment is acceptable for cost savings.",
        counter_arguments=[
            "Certification reduces risk of failure.",
            "Regulators require certified equipment."
        ],
        resolution_strategy="Enforce certification protocols and conduct audits.",
        entity_scope="All MPD well control equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.8"
    ),
    DoctrineBlock(
        topic="MPD Well Control Barrier Philosophy",
        keywords=["MPD", "Well Control", "Barrier Philosophy", "Primary Barrier", "Secondary Barrier", "Redundancy"],
        conclusion_template="MPD operations must adhere to a two-barrier philosophy, ensuring both primary and secondary barriers are in place at all times.",
        reasoning_framework="""
1. The two-barrier philosophy is foundational to well control.
2. MPD may use dynamic barriers (pressure, equipment) as part of the system.
3. Both primary (fluid column, RCD) and secondary (BOP, annular) barriers must be verified.
4. The operator must document barrier status and verification results.
5. Adversaries may argue for single-barrier operation in low-risk scenarios.
6. Counter-arguments cite incident history and regulatory requirements.
7. Resolution involves procedural enforcement and regular verification.
""",
        key_factors=[
            "Barrier identification",
            "Verification procedures",
            "Documentation",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 92M",
            "IADC Well Control Guidelines"
        ],
        burden_holder="Operator",
        adversary_position="Single-barrier operation is sufficient in some cases.",
        counter_arguments=[
            "Two-barrier philosophy reduces risk.",
            "Regulators require dual barriers."
        ],
        resolution_strategy="Enforce two-barrier protocols and verify regularly.",
        entity_scope="All MPD operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 8.1"
    ),
    DoctrineBlock(
        topic="MPD Well Control Contingency Planning",
        keywords=["MPD", "Well Control", "Contingency Planning", "Emergency Response", "Scenarios", "Mitigation"],
        conclusion_template="Comprehensive contingency plans must be in place for all foreseeable MPD well control scenarios.",
        reasoning_framework="""
1. Contingency planning prepares the crew for emergency scenarios.
2. Plans must cover equipment failure, influx, losses, and transition to conventional well control.
3. The operator must document and review plans regularly.
4. Training and drills are required to ensure crew readiness.
5. Adversaries may argue for informal contingency planning.
6. Counter-arguments cite regulatory requirements and incident history.
7. Resolution involves formal planning and regular review.
""",
        key_factors=[
            "Scenario identification",
            "Mitigation strategies",
            "Documentation",
            "Training and drills"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Emergency Response Plan"
        ],
        burden_holder="Operator",
        adversary_position="Informal planning is sufficient.",
        counter_arguments=[
            "Formal plans improve readiness.",
            "Regulators require documented contingency plans."
        ],
        resolution_strategy="Document and review contingency plans regularly.",
        entity_scope="All MPD operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 8.4"
    ),
    DoctrineBlock(
        topic="MPD Well Control Alarm Management",
        keywords=["MPD", "Well Control", "Alarm Management", "Automation", "Human Factors", "Response"],
        conclusion_template="MPD well control systems must have effective alarm management to ensure timely crew response and avoid alarm fatigue.",
        reasoning_framework="""
1. Alarm management is critical for timely detection and response.
2. Systems must prioritize alarms and avoid unnecessary notifications.
3. The operator must configure, test, and review alarm settings regularly.
4. Training is required to ensure crew understand alarm protocols.
5. Adversaries may argue for default system settings.
6. Counter-arguments cite alarm fatigue and missed events.
7. Resolution involves configuration management and regular review.
""",
        key_factors=[
            "Alarm prioritization",
            "Configuration management",
            "Training",
            "Review frequency"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Automation Policy"
        ],
        burden_holder="Operator",
        adversary_position="Default alarm settings are sufficient.",
        counter_arguments=[
            "Custom configuration reduces alarm fatigue.",
            "Training improves response."
        ],
        resolution_strategy="Configure alarms and review settings regularly.",
        entity_scope="All MPD well control systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.9"
    ),
    DoctrineBlock(
        topic="MPD Well Control Crew Communication Protocols",
        keywords=["MPD", "Well Control", "Crew Communication", "Protocols", "Human Factors", "Emergency Response"],
        conclusion_template="Structured crew communication protocols must be established for all MPD well control operations.",
        reasoning_framework="""
1. Effective communication reduces human error in well control events.
2. Protocols must define terminology, roles, and escalation paths.
3. Training and drills are required to reinforce protocols.
4. The operator must document and review communication procedures.
5. Adversaries may argue for informal communication.
6. Counter-arguments cite incident history and regulatory findings.
7. Resolution involves procedural enforcement and regular drills.
""",
        key_factors=[
            "Protocol documentation",
            "Role assignment",
            "Training and drills",
            "Review frequency"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Well Control Manual"
        ],
        burden_holder="Operator",
        adversary_position="Informal communication is sufficient.",
        counter_arguments=[
            "Structured protocols reduce error.",
            "Regulators require documented procedures."
        ],
        resolution_strategy="Document and drill communication protocols.",
        entity_scope="All MPD well control operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 8.6"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Redress and Recertification",
        keywords=["MPD", "Well Control Equipment", "Redress", "Recertification", "Maintenance", "Compliance"],
        conclusion_template="All MPD well control equipment must be redressed and recertified per manufacturer and industry schedules.",
        reasoning_framework="""
1. Redress and recertification ensure equipment reliability and compliance.
2. Schedules must follow manufacturer and API recommendations.
3. Documentation of redress and recertification is required for audit.
4. The operator is responsible for compliance and record-keeping.
5. Adversaries may argue for extended intervals.
6. Counter-arguments cite failure history and regulatory requirements.
7. Resolution involves adherence to schedules and audits.
""",
        key_factors=[
            "Redress schedule",
            "Recertification documentation",
            "Audit readiness",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Equipment Policy"
        ],
        burden_holder="Operator",
        adversary_position="Extended intervals are acceptable.",
        counter_arguments=[
            "Frequent redress reduces failure risk.",
            "Regulators require documented recertification."
        ],
        resolution_strategy="Adhere to schedules and maintain records.",
        entity_scope="All MPD well control equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.10"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Traceability",
        keywords=["MPD", "Well Control Equipment", "Traceability", "Serial Number", "Documentation", "Audit"],
        conclusion_template="All MPD well control equipment must be traceable by serial number and documented in equipment registers.",
        reasoning_framework="""
1. Traceability ensures accountability and supports incident investigation.
2. Equipment registers must include serial numbers, certification, and maintenance history.
3. The operator is responsible for maintaining up-to-date registers.
4. Adversaries may argue for minimal documentation.
5. Counter-arguments cite regulatory requirements and audit findings.
6. Resolution involves strict documentation protocols and audits.
""",
        key_factors=[
            "Serial number tracking",
            "Equipment registers",
            "Documentation",
            "Audit readiness"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Equipment Policy"
        ],
        burden_holder="Operator",
        adversary_position="Minimal documentation is sufficient.",
        counter_arguments=[
            "Traceability supports safety and compliance.",
            "Regulators require equipment registers."
        ],
        resolution_strategy="Maintain up-to-date registers and conduct audits.",
        entity_scope="All MPD well control equipment",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.11"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Change Management",
        keywords=["MPD", "Well Control Equipment", "Change Management", "Configuration", "Documentation", "Audit"],
        conclusion_template="All changes to MPD well control equipment configuration must be documented and reviewed for operational impact.",
        reasoning_framework="""
1. Change management ensures equipment changes do not compromise safety or compliance.
2. All changes must be documented, reviewed, and approved before implementation.
3. The operator is responsible for maintaining change logs and conducting impact assessments.
4. Adversaries may argue for informal change processes.
5. Counter-arguments cite incident history and regulatory requirements.
6. Resolution involves formal change management protocols and audits.
""",
        key_factors=[
            "Change documentation",
            "Impact assessment",
            "Review and approval",
            "Audit readiness"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Change Management Policy"
        ],
        burden_holder="Operator",
        adversary_position="Informal change processes are sufficient.",
        counter_arguments=[
            "Formal change management reduces risk.",
            "Regulators require documented processes."
        ],
        resolution_strategy="Implement formal change management and conduct audits.",
        entity_scope="All MPD well control equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.12"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Deviation Management",
        keywords=["MPD", "Well Control Equipment", "Deviation Management", "Nonconformance", "Waiver", "Documentation"],
        conclusion_template="All deviations from standard MPD well control equipment specifications must be documented, justified, and approved.",
        reasoning_framework="""
1. Deviation management ensures nonconformances are controlled and justified.
2. All deviations must be documented, risk-assessed, and approved by competent authority.
3. The operator is responsible for maintaining deviation records.
4. Adversaries may argue for informal deviation handling.
5. Counter-arguments cite regulatory requirements and audit findings.
6. Resolution involves formal deviation management protocols and audits.
""",
        key_factors=[
            "Deviation documentation",
            "Risk assessment",
            "Approval process",
            "Audit readiness"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Deviation Management Policy"
        ],
        burden_holder="Operator",
        adversary_position="Informal deviation handling is sufficient.",
        counter_arguments=[
            "Formal deviation management reduces risk.",
            "Regulators require documented processes."
        ],
        resolution_strategy="Implement formal deviation management and conduct audits.",
        entity_scope="All MPD well control equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.13"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Obsolescence Management",
        keywords=["MPD", "Well Control Equipment", "Obsolescence", "Replacement", "Lifecycle", "Documentation"],
        conclusion_template="Obsolete MPD well control equipment must be identified, documented, and replaced according to lifecycle management policies.",
        reasoning_framework="""
1. Obsolescence management ensures equipment remains fit for purpose.
2. The operator must maintain an inventory of equipment and identify obsolete items.
3. Replacement planning must be documented and scheduled.
4. Adversaries may argue for continued use of obsolete equipment.
5. Counter-arguments cite safety, performance, and regulatory requirements.
6. Resolution involves lifecycle management protocols and audits.
""",
        key_factors=[
            "Inventory management",
            "Obsolescence identification",
            "Replacement planning",
            "Documentation"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Lifecycle Management Policy"
        ],
        burden_holder="Operator",
        adversary_position="Obsolete equipment can be used until failure.",
        counter_arguments=[
            "Obsolescence increases risk of failure.",
            "Regulators require lifecycle management."
        ],
        resolution_strategy="Implement lifecycle management and conduct audits.",
        entity_scope="All MPD well control equipment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.14"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Spare Parts Management",
        keywords=["MPD", "Well Control Equipment", "Spare Parts", "Inventory", "Availability", "Documentation"],
        conclusion_template="Adequate spare parts for MPD well control equipment must be maintained and documented to ensure operational continuity.",
        reasoning_framework="""
1. Spare parts management reduces downtime and supports operational continuity.
2. The operator must maintain an inventory of critical spares and document usage.
3. Inventory levels must be reviewed and replenished regularly.
4. Adversaries may argue for minimal spare parts inventory.
5. Counter-arguments cite incident history and operational delays.
6. Resolution involves inventory management protocols and audits.
""",
        key_factors=[
            "Inventory records",
            "Critical spares identification",
            "Review and replenishment frequency",
            "Documentation"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Inventory Management Policy"
        ],
        burden_holder="Operator",
        adversary_position="Minimal spare parts inventory is sufficient.",
        counter_arguments=[
            "Adequate spares reduce downtime and risk.",
            "Regulators require documented inventory management."
        ],
        resolution_strategy="Maintain inventory and conduct regular audits.",
        entity_scope="All MPD well control equipment",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.15"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Performance Monitoring",
        keywords=["MPD", "Well Control Equipment", "Performance Monitoring", "KPIs", "Data Analysis", "Reliability"],
        conclusion_template="Performance of MPD well control equipment must be monitored using KPIs and data analysis to ensure reliability.",
        reasoning_framework="""
1. Performance monitoring identifies trends and supports proactive maintenance.
2. KPIs must be defined for critical equipment (e.g., uptime, failure rate).
3. Data analysis informs maintenance and replacement decisions.
4. The operator must document performance monitoring procedures.
5. Adversaries may argue for reactive maintenance only.
6. Counter-arguments cite improved reliability and reduced incidents.
7. Resolution involves technology investment and procedural updates.
""",
        key_factors=[
            "KPI definition",
            "Data analysis capability",
            "Documentation",
            "Maintenance planning"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Performance Monitoring Policy"
        ],
        burden_holder="Operator",
        adversary_position="Reactive maintenance is sufficient.",
        counter_arguments=[
            "Performance monitoring improves reliability.",
            "Regulators require documented procedures."
        ],
        resolution_strategy="Invest in technology and update procedures.",
        entity_scope="All MPD well control equipment",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.16"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Failure Reporting",
        keywords=["MPD", "Well Control Equipment", "Failure Reporting", "Incident", "Root Cause", "Regulatory"],
        conclusion_template="All MPD well control equipment failures must be reported, investigated, and documented with root cause analysis.",
        reasoning_framework="""
1. Failure reporting supports incident investigation and corrective action.
2. Documentation is required for regulatory compliance and organizational learning.
3. The operator must submit reports per jurisdictional requirements.
4. Adversaries may argue for internal-only reporting.
5. Counter-arguments cite transparency and industry improvement.
6. Resolution involves formal reporting protocols and regulatory engagement.
""",
        key_factors=[
            "Failure documentation",
            "Root cause analysis",
            "Regulatory reporting",
            "Corrective action tracking"
        ],
        primary_authority=[
            "Jurisdictional Regulations",
            "Operator Incident Policy"
        ],
        burden_holder="Operator",
        adversary_position="Internal reporting is sufficient.",
        counter_arguments=[
            "Regulators require formal reporting.",
            "Transparency improves industry safety."
        ],
        resolution_strategy="Follow formal protocols and engage with regulators.",
        entity_scope="All MPD well control equipment failures",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Jurisdictional Regulatory Codes"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Lessons Learned Management",
        keywords=["MPD", "Well Control Equipment", "Lessons Learned", "Knowledge Management", "Continuous Improvement", "Documentation"],
        conclusion_template="Lessons learned from MPD well control equipment incidents must be documented and integrated into continuous improvement processes.",
        reasoning_framework="""
1. Lessons learned management supports organizational learning and improvement.
2. Documentation must include incident description, root cause, corrective actions, and outcomes.
3. The operator is responsible for integrating lessons into procedures and training.
4. Adversaries may argue for informal knowledge sharing.
5. Counter-arguments cite improved safety and regulatory requirements.
6. Resolution involves formal lessons learned processes and audits.
""",
        key_factors=[
            "Incident documentation",
            "Procedure updates",
            "Training integration",
            "Audit readiness"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Knowledge Management Policy"
        ],
        burden_holder="Operator",
        adversary_position="Informal knowledge sharing is sufficient.",
        counter_arguments=[
            "Formal processes improve safety and compliance.",
            "Regulators require documented lessons learned."
        ],
        resolution_strategy="Implement formal processes and integrate lessons into procedures.",
        entity_scope="All MPD well control equipment incidents",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.17"
    ),
    DoctrineBlock(
        topic="MPD Well Control Equipment Regulatory Audit Readiness",
        keywords=["MPD", "Well Control Equipment", "Regulatory Audit", "Readiness", "Documentation", "Compliance"],
        conclusion_template="MPD well control equipment and documentation must be maintained in a state of readiness for regulatory audit at all times.",
        reasoning_framework="""
1. Audit readiness ensures compliance and supports regulatory engagement.
2. Documentation must be complete, up-to-date, and accessible.
3. The operator is responsible for audit preparation and response.
4. Adversaries may argue for minimal audit preparation.
5. Counter-arguments cite regulatory penalties and operational delays.
6. Resolution involves regular internal audits and documentation reviews.
""",
        key_factors=[
            "Documentation completeness",
            "Accessibility",
            "Internal audit frequency",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 92M",
            "Operator Compliance Policy"
        ],
        burden_holder="Operator",
        adversary_position="Minimal audit preparation is sufficient.",
        counter_arguments=[
            "Audit readiness reduces risk of penalties.",
            "Regulators require accessible documentation."
        ],
        resolution_strategy="Conduct regular internal audits and maintain documentation.",
        entity_scope="All MPD well control equipment",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 92M Section 7.18"
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