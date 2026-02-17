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
        topic="PTC Implementation Requirements",
        keywords=["Positive Train Control", "PTC", "Safety", "Implementation", "Railroad", "Technology", "Mandate"],
        conclusion_template="PTC must be implemented on all lines as mandated by federal law unless an exception applies.",
        reasoning_framework="""
        The Rail Safety Improvement Act of 2008 (RSIA) requires Class I railroads and certain passenger railroads to implement Positive Train Control (PTC) systems on main lines carrying passengers or hazardous materials. The FRA sets technical standards for interoperability, reliability, and performance. Railroads must submit implementation plans, meet deadlines, and demonstrate compliance through testing and certification. Exceptions may be granted for lines not meeting risk thresholds. The doctrine weighs statutory mandates, technical feasibility, cost, and operational impact. Enforcement is through FRA oversight and civil penalties.
        """,
        key_factors=[
            "RSIA statutory mandate",
            "FRA technical standards",
            "Interoperability requirements",
            "Risk thresholds",
            "Implementation deadlines",
            "Certification and testing"
        ],
        primary_authority=[
            "Rail Safety Improvement Act (RSIA) of 2008",
            "Federal Railroad Administration (FRA) regulations"
        ],
        burden_holder="Railroad operator",
        adversary_position="PTC is unnecessary or cost-prohibitive for certain lines",
        counter_arguments=[
            "PTC reduces risk of collisions and derailments",
            "Exceptions are limited and must be justified",
            "Cost-benefit analysis favors safety improvements"
        ],
        resolution_strategy="FRA review and enforcement; appeals through administrative process",
        entity_scope="Class I railroads, passenger railroads",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="RSIA Section 104; FRA Final Rule 49 CFR Part 236"
    ),
    DoctrineBlock(
        topic="Grade Crossing Warning Systems",
        keywords=["Grade Crossing", "Warning", "Safety", "Signals", "Active Protection", "Passive Protection"],
        conclusion_template="Appropriate grade crossing warning systems must be installed and maintained to ensure public safety.",
        reasoning_framework="""
        The doctrine requires railroads and public authorities to evaluate grade crossing risks and install suitable warning systems, including active (gates, lights, bells) or passive (signs, markings) protections. The selection is based on traffic volume, train speed, accident history, and local conditions. FRA and FHWA provide guidelines and minimum standards. Maintenance and periodic inspections are mandatory. Liability may arise for inadequate protection or failure to maintain systems. Upgrades are recommended for high-risk crossings.
        """,
        key_factors=[
            "Traffic volume",
            "Train speed",
            "Accident history",
            "Local conditions",
            "FRA/FHWA standards",
            "Maintenance records"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Federal Highway Administration (FHWA)",
            "49 CFR Part 234"
        ],
        burden_holder="Railroad and public authority",
        adversary_position="Existing warning systems are sufficient; upgrades unnecessary",
        counter_arguments=[
            "Accident data supports need for upgrades",
            "Federal standards evolve with technology",
            "Public safety outweighs cost concerns"
        ],
        resolution_strategy="Risk assessment, compliance audits, and federal funding programs",
        entity_scope="Railroad crossings, public authorities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Grade Crossing Safety Regulations"
    ),
    DoctrineBlock(
        topic="FRA Track Safety Standards",
        keywords=["Track Safety", "FRA", "Inspection", "Maintenance", "Compliance", "Railroad"],
        conclusion_template="Railroads must comply with FRA track safety standards and conduct regular inspections.",
        reasoning_framework="""
        FRA track safety standards (49 CFR Part 213) specify minimum requirements for track structure, geometry, and maintenance. Railroads are obligated to inspect tracks at prescribed intervals, document findings, and address defects promptly. Standards vary by track class and intended speed. Non-compliance results in enforcement actions, including fines and operational restrictions. The doctrine emphasizes preventive maintenance, documentation, and continuous improvement.
        """,
        key_factors=[
            "Track class",
            "Inspection frequency",
            "Defect remediation",
            "Documentation",
            "Maintenance practices"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 213"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current inspection regime is adequate; stricter standards unnecessary",
        counter_arguments=[
            "Higher speeds require stricter standards",
            "Defect growth can cause catastrophic failures",
            "Regulatory compliance is mandatory"
        ],
        resolution_strategy="FRA audits, corrective action plans, and periodic reviews",
        entity_scope="All railroad tracks",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Track Safety Standards"
    ),
    DoctrineBlock(
        topic="Derailment Causation Analysis",
        keywords=["Derailment", "Causation", "Analysis", "Investigation", "Safety", "Root Cause"],
        conclusion_template="Derailment causation must be analyzed using systematic investigation protocols.",
        reasoning_framework="""
        Derailment analysis involves collecting evidence, interviewing witnesses, and reviewing operational data. Investigators apply root cause analysis techniques, considering track conditions, equipment failure, human factors, and environmental influences. The NTSB and FRA provide investigation protocols and reporting requirements. Findings inform corrective actions and regulatory changes. The doctrine prioritizes transparency, thoroughness, and prevention of future incidents.
        """,
        key_factors=[
            "Evidence collection",
            "Root cause analysis",
            "Operational data review",
            "Human factors",
            "Equipment and track conditions"
        ],
        primary_authority=[
            "National Transportation Safety Board (NTSB)",
            "Federal Railroad Administration (FRA)"
        ],
        burden_holder="Investigating authority",
        adversary_position="Derailment was unavoidable or caused by external factors",
        counter_arguments=[
            "Systematic analysis can reveal preventable causes",
            "Regulatory oversight ensures accountability",
            "Lessons learned improve safety"
        ],
        resolution_strategy="Comprehensive investigation, public reporting, and corrective actions",
        entity_scope="Railroad operators, investigators",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NTSB Railroad Investigation Procedures"
    ),
    DoctrineBlock(
        topic="Hazmat Rail Transport Regulations",
        keywords=["Hazmat", "Rail Transport", "Regulations", "Safety", "Tank Car", "Placarding"],
        conclusion_template="Hazmat rail transport must comply with federal regulations for packaging, labeling, and routing.",
        reasoning_framework="""
        The doctrine mandates compliance with DOT and FRA regulations for hazardous materials transport, including tank car standards, placarding, routing, and emergency response planning. Railroads must ensure proper classification, securement, and documentation. Special requirements apply to high-hazard flammable trains (HHFT). Violations result in civil penalties and operational restrictions. Coordination with local emergency responders is required.
        """,
        key_factors=[
            "Hazmat classification",
            "Tank car standards",
            "Placarding and labeling",
            "Routing restrictions",
            "Emergency response plans"
        ],
        primary_authority=[
            "Department of Transportation (DOT)",
            "Federal Railroad Administration (FRA)",
            "49 CFR Parts 172-174"
        ],
        burden_holder="Railroad operator",
        adversary_position="Hazmat regulations are overly burdensome",
        counter_arguments=[
            "Public safety requires strict controls",
            "Incidents can have catastrophic consequences",
            "Regulations are based on risk assessments"
        ],
        resolution_strategy="Compliance audits, enforcement actions, and stakeholder engagement",
        entity_scope="Railroads transporting hazardous materials",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOT Hazardous Materials Regulations"
    ),
    DoctrineBlock(
        topic="Locomotive Event Recorder Analysis",
        keywords=["Locomotive", "Event Recorder", "Analysis", "Data", "Accident Investigation", "Safety"],
        conclusion_template="Event recorder data must be preserved and analyzed following accidents or incidents.",
        reasoning_framework="""
        Locomotive event recorders capture operational data, including speed, throttle position, brake application, and communications. Following an accident, railroads must secure and preserve recorder data for investigation. Analysis provides insight into crew actions, equipment performance, and sequence of events. FRA mandates installation and maintenance of event recorders. Data integrity and chain of custody are critical for legal and regulatory proceedings.
        """,
        key_factors=[
            "Data preservation",
            "Event recorder maintenance",
            "Accident investigation protocols",
            "Data integrity",
            "Chain of custody"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 229"
        ],
        burden_holder="Railroad operator",
        adversary_position="Event recorder data is unreliable or incomplete",
        counter_arguments=[
            "Event recorders are designed for reliability",
            "Protocols ensure data integrity",
            "Data is essential for investigations"
        ],
        resolution_strategy="Technical review, validation, and expert analysis",
        entity_scope="Railroad operators, investigators",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Locomotive Event Recorder Regulations"
    ),
    DoctrineBlock(
        topic="Locomotive Alerter and Vigilance Systems",
        keywords=["Locomotive", "Alerter", "Vigilance", "Safety", "Crew Alertness", "Fatigue"],
        conclusion_template="Locomotive alerter systems must be installed and maintained to monitor crew alertness.",
        reasoning_framework="""
        Alerter and vigilance systems detect inactivity or lack of response from locomotive crews, triggering alarms or automatic braking if necessary. FRA regulations require installation on certain locomotives to prevent accidents caused by fatigue or incapacitation. Maintenance and periodic testing are mandatory. The doctrine considers human factors, operational risk, and technological reliability. Crew training and awareness complement technical solutions.
        """,
        key_factors=[
            "Alerter system installation",
            "Maintenance and testing",
            "Crew training",
            "Human factors",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 229"
        ],
        burden_holder="Railroad operator",
        adversary_position="Alerter systems are unnecessary or ineffective",
        counter_arguments=[
            "Fatigue is a known safety risk",
            "Alerter systems provide critical backup",
            "Regulations mandate installation"
        ],
        resolution_strategy="Regulatory enforcement, technical upgrades, and crew education",
        entity_scope="Railroad operators, locomotive crews",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Locomotive Safety Standards"
    ),
    DoctrineBlock(
        topic="End-of-Train Device (EOT) Requirements",
        keywords=["End-of-Train", "EOT", "Device", "Safety", "Brake Pipe", "Monitoring"],
        conclusion_template="EOT devices must be installed on freight trains to monitor brake pipe pressure and provide emergency signals.",
        reasoning_framework="""
        EOT devices are required on most freight trains to monitor brake pipe pressure and transmit emergency signals. FRA regulations specify technical standards, installation procedures, and maintenance requirements. EOT devices enhance safety by allowing remote monitoring and emergency brake application. Exceptions exist for certain train configurations. Compliance is verified through inspections and operational testing.
        """,
        key_factors=[
            "EOT device installation",
            "Technical standards",
            "Brake pipe monitoring",
            "Emergency signal capability",
            "Maintenance records"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 232"
        ],
        burden_holder="Railroad operator",
        adversary_position="EOT devices are redundant or unreliable",
        counter_arguments=[
            "EOT devices improve safety and operational efficiency",
            "Regulations mandate installation",
            "Technology is proven and reliable"
        ],
        resolution_strategy="Regulatory compliance, technical audits, and operational reviews",
        entity_scope="Freight trains",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA End-of-Train Device Regulations"
    ),
    DoctrineBlock(
        topic="Broken Rail Detection Technologies",
        keywords=["Broken Rail", "Detection", "Technology", "Safety", "Track Monitoring", "Sensor"],
        conclusion_template="Broken rail detection technologies should be deployed on high-risk lines to enhance safety.",
        reasoning_framework="""
        Broken rail detection technologies, including track circuit monitoring, acoustic sensors, and fiber optic systems, provide real-time alerts for rail fractures. Deployment is prioritized for high-speed, high-tonnage, or hazardous material routes. FRA encourages adoption through research grants and pilot programs. The doctrine weighs cost, reliability, and integration with existing infrastructure. Maintenance and calibration are critical for effectiveness.
        """,
        key_factors=[
            "Risk assessment",
            "Technology selection",
            "Integration with signaling",
            "Maintenance and calibration",
            "Cost-benefit analysis"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Industry best practices"
        ],
        burden_holder="Railroad operator",
        adversary_position="Detection technologies are too costly or unnecessary",
        counter_arguments=[
            "Broken rails cause derailments",
            "Early detection prevents accidents",
            "Technology costs are offset by safety gains"
        ],
        resolution_strategy="Pilot programs, federal funding, and phased deployment",
        entity_scope="High-risk rail lines",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA Research and Innovation Initiatives"
    ),
    DoctrineBlock(
        topic="Track Geometry Degradation Analysis",
        keywords=["Track Geometry", "Degradation", "Analysis", "Safety", "Inspection", "Maintenance"],
        conclusion_template="Track geometry must be regularly analyzed for degradation to prevent safety hazards.",
        reasoning_framework="""
        Track geometry degradation is monitored through automated inspection vehicles, manual measurements, and data analytics. Key parameters include alignment, profile, gauge, and cross-level. FRA sets minimum standards for geometry and mandates inspection intervals. Degradation trends inform maintenance planning and risk mitigation. The doctrine emphasizes early detection, data-driven decision-making, and compliance with regulatory standards.
        """,
        key_factors=[
            "Inspection frequency",
            "Automated measurement",
            "Data analytics",
            "Maintenance planning",
            "Regulatory standards"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 213"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current inspection methods are sufficient",
        counter_arguments=[
            "Automated inspections improve accuracy",
            "Degradation can lead to derailments",
            "Regulatory standards require continuous improvement"
        ],
        resolution_strategy="Data-driven maintenance, regulatory audits, and technology upgrades",
        entity_scope="All railroad tracks",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Track Geometry Standards"
    ),
    DoctrineBlock(
        topic="Signal System Types and Operations",
        keywords=["Signal System", "Types", "Operations", "Safety", "Interlocking", "Automatic Block"],
        conclusion_template="Railroads must operate and maintain signal systems in accordance with FRA regulations.",
        reasoning_framework="""
        Signal systems, including automatic block, interlocking, and centralized traffic control, are essential for train movement safety. FRA regulations specify technical standards, maintenance requirements, and operational protocols. Signal failures must be reported and addressed promptly. The doctrine considers system complexity, redundancy, and integration with PTC. Crew training and operational discipline are critical for safe operations.
        """,
        key_factors=[
            "Signal system type",
            "Maintenance and testing",
            "Failure reporting",
            "Integration with PTC",
            "Crew training"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 236"
        ],
        burden_holder="Railroad operator",
        adversary_position="Signal systems are outdated or unreliable",
        counter_arguments=[
            "Signal systems are regularly upgraded",
            "Redundancy reduces risk",
            "Regulations mandate safe operations"
        ],
        resolution_strategy="Technical audits, system upgrades, and regulatory enforcement",
        entity_scope="Railroad operators",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Signal System Regulations"
    ),
    DoctrineBlock(
        topic="NTSB Railroad Investigation Procedures",
        keywords=["NTSB", "Investigation", "Procedures", "Railroad", "Accident", "Safety"],
        conclusion_template="Railroad accidents must be investigated using NTSB procedures to determine cause and recommend improvements.",
        reasoning_framework="""
        NTSB investigations follow standardized protocols for evidence collection, witness interviews, and technical analysis. The process includes on-site examination, laboratory testing, and review of operational data. Findings are published in public reports, with recommendations for regulatory changes or industry practices. The doctrine emphasizes independence, transparency, and continuous safety improvement.
        """,
        key_factors=[
            "Evidence collection",
            "Technical analysis",
            "Public reporting",
            "Regulatory recommendations",
            "Transparency"
        ],
        primary_authority=[
            "National Transportation Safety Board (NTSB)",
            "49 CFR Part 835"
        ],
        burden_holder="Investigating authority",
        adversary_position="NTSB findings are disputed or incomplete",
        counter_arguments=[
            "NTSB procedures are rigorous and impartial",
            "Public reporting ensures accountability",
            "Recommendations drive safety improvements"
        ],
        resolution_strategy="Peer review, stakeholder engagement, and regulatory follow-up",
        entity_scope="Railroad operators, investigators",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NTSB Investigation Manual"
    ),
    DoctrineBlock(
        topic="Railroad Bridge Inspection and Safety",
        keywords=["Bridge", "Inspection", "Safety", "Railroad", "Structural Integrity", "Maintenance"],
        conclusion_template="Railroad bridges must be inspected and maintained to ensure structural integrity and safety.",
        reasoning_framework="""
        FRA regulations require railroads to develop bridge management programs, conduct regular inspections, and maintain records. Inspections must be performed by qualified personnel at prescribed intervals. Structural deficiencies must be addressed promptly. The doctrine considers bridge age, design, load capacity, and environmental factors. Failure to comply results in enforcement actions and operational restrictions.
        """,
        key_factors=[
            "Inspection frequency",
            "Qualified personnel",
            "Maintenance records",
            "Structural deficiency remediation",
            "Bridge management program"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 237"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current inspection regime is adequate",
        counter_arguments=[
            "Bridge failures cause catastrophic accidents",
            "Regulatory standards require continuous improvement",
            "Qualified inspections are essential"
        ],
        resolution_strategy="Regulatory audits, corrective action plans, and bridge upgrades",
        entity_scope="Railroad bridges",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Bridge Safety Standards"
    ),
    DoctrineBlock(
        topic="Freight Car Brake System Requirements",
        keywords=["Freight Car", "Brake System", "Requirements", "Safety", "Inspection", "Maintenance"],
        conclusion_template="Freight car brake systems must meet FRA requirements for installation, inspection, and maintenance.",
        reasoning_framework="""
        FRA regulations specify minimum standards for brake system design, installation, inspection, and maintenance. Railroads must conduct periodic brake tests, document results, and address deficiencies. Brake system failures are a leading cause of accidents; therefore, compliance is strictly enforced. The doctrine emphasizes preventive maintenance, crew training, and technical upgrades.
        """,
        key_factors=[
            "Brake system design",
            "Inspection frequency",
            "Maintenance records",
            "Crew training",
            "Deficiency remediation"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 232"
        ],
        burden_holder="Railroad operator",
        adversary_position="Brake system standards are outdated",
        counter_arguments=[
            "Regulations evolve with technology",
            "Brake failures cause derailments",
            "Preventive maintenance reduces risk"
        ],
        resolution_strategy="Technical audits, regulatory enforcement, and system upgrades",
        entity_scope="Freight cars",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Brake System Regulations"
    ),
    DoctrineBlock(
        topic="Railroad Worker Safety and Roadway Worker Protection",
        keywords=["Worker Safety", "Roadway Worker", "Protection", "Railroad", "Regulations", "Training"],
        conclusion_template="Railroads must implement worker safety programs and comply with roadway worker protection regulations.",
        reasoning_framework="""
        FRA regulations require railroads to develop and implement comprehensive worker safety programs, including training, protective equipment, and safe work practices. Roadway worker protection rules mandate communication protocols, job briefings, and use of safety devices. Violations result in civil penalties and increased liability. The doctrine prioritizes prevention, education, and continuous improvement.
        """,
        key_factors=[
            "Safety program implementation",
            "Training and education",
            "Protective equipment",
            "Communication protocols",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 214"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current safety programs are sufficient",
        counter_arguments=[
            "Worker injuries remain a concern",
            "Regulations require periodic review",
            "Continuous improvement is necessary"
        ],
        resolution_strategy="Safety audits, regulatory enforcement, and worker engagement",
        entity_scope="Railroad workers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Roadway Worker Protection Standards"
    ),
    DoctrineBlock(
        topic="Tank Car Thermal Protection Requirements",
        keywords=["Tank Car", "Thermal Protection", "Requirements", "Hazmat", "Safety", "Regulations"],
        conclusion_template="Tank cars transporting hazardous materials must meet thermal protection requirements.",
        reasoning_framework="""
        DOT and FRA regulations mandate thermal protection for tank cars carrying certain hazardous materials, including insulation, jackets, and pressure relief devices. Requirements are based on material properties, risk assessment, and accident history. Compliance is verified through inspections and certification. The doctrine considers technological advances, cost, and operational impact.
        """,
        key_factors=[
            "Thermal protection design",
            "Material properties",
            "Risk assessment",
            "Inspection and certification",
            "Regulatory standards"
        ],
        primary_authority=[
            "Department of Transportation (DOT)",
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 179"
        ],
        burden_holder="Railroad operator",
        adversary_position="Thermal protection is unnecessary or too costly",
        counter_arguments=[
            "Thermal protection reduces accident severity",
            "Regulations are based on risk",
            "Technological advances lower costs"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and industry collaboration",
        entity_scope="Tank cars transporting hazardous materials",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOT Tank Car Safety Regulations"
    ),
    DoctrineBlock(
        topic="Railroad Dispatching and Train Authority",
        keywords=["Dispatching", "Train Authority", "Railroad", "Safety", "Operations", "Communication"],
        conclusion_template="Railroads must establish clear dispatching protocols and train authority procedures.",
        reasoning_framework="""
        Dispatching and train authority are governed by operational rules, signaling systems, and communication protocols. FRA regulations require railroads to document procedures, train personnel, and maintain records. Train movements must be authorized and coordinated to prevent conflicts. The doctrine emphasizes clarity, redundancy, and compliance with regulatory standards.
        """,
        key_factors=[
            "Dispatching protocols",
            "Train authority procedures",
            "Communication systems",
            "Personnel training",
            "Recordkeeping"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 220"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current dispatching procedures are adequate",
        counter_arguments=[
            "Operational errors cause accidents",
            "Regulations require periodic review",
            "Redundancy improves safety"
        ],
        resolution_strategy="Operational audits, regulatory enforcement, and system upgrades",
        entity_scope="Railroad operators",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Dispatching and Train Authority Standards"
    ),
    DoctrineBlock(
        topic="Wheel Impact Load Detection (WILD)",
        keywords=["Wheel Impact", "Load Detection", "WILD", "Safety", "Track Monitoring", "Sensor"],
        conclusion_template="WILD systems must be deployed to detect wheel defects and prevent track damage.",
        reasoning_framework="""
        WILD systems use sensors to detect excessive wheel impacts, which can cause track damage and derailments. FRA encourages deployment on high-tonnage and high-speed routes. Detected defects must be addressed promptly, with records maintained for regulatory review. The doctrine considers sensor reliability, maintenance, and integration with asset management systems.
        """,
        key_factors=[
            "Sensor reliability",
            "Defect remediation",
            "Maintenance records",
            "Integration with asset management",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Industry best practices"
        ],
        burden_holder="Railroad operator",
        adversary_position="WILD systems are unnecessary or too costly",
        counter_arguments=[
            "Wheel defects cause derailments",
            "Early detection prevents accidents",
            "Technology costs are offset by safety gains"
        ],
        resolution_strategy="Federal funding, phased deployment, and technical audits",
        entity_scope="High-risk rail lines",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA Research and Innovation Initiatives"
    ),
    DoctrineBlock(
        topic="Passenger Rail Crashworthiness Standards",
        keywords=["Passenger Rail", "Crashworthiness", "Standards", "Safety", "Regulations", "Design"],
        conclusion_template="Passenger rail vehicles must meet crashworthiness standards to protect occupants.",
        reasoning_framework="""
        FRA regulations specify crashworthiness standards for passenger rail vehicles, including structural integrity, energy absorption, and occupant protection. Manufacturers must certify compliance through testing and documentation. The doctrine considers accident history, technological advances, and operational impact. Periodic reviews ensure standards reflect current best practices.
        """,
        key_factors=[
            "Structural integrity",
            "Energy absorption",
            "Occupant protection",
            "Testing and certification",
            "Regulatory standards"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 238"
        ],
        burden_holder="Rail vehicle manufacturer",
        adversary_position="Crashworthiness standards are too costly",
        counter_arguments=[
            "Passenger safety is paramount",
            "Regulations evolve with technology",
            "Accident history supports stricter standards"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and industry collaboration",
        entity_scope="Passenger rail vehicles",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Passenger Rail Safety Standards"
    ),
    DoctrineBlock(
        topic="Railroad Crossing Sight Distance Requirements",
        keywords=["Crossing", "Sight Distance", "Requirements", "Safety", "Visibility", "Regulations"],
        conclusion_template="Railroad crossings must meet sight distance requirements to ensure visibility and safety.",
        reasoning_framework="""
        Sight distance requirements are based on train speed, vehicle approach speed, and environmental factors. FRA and FHWA provide guidelines for minimum visibility standards. Railroads and public authorities must assess crossings, implement improvements, and maintain records. The doctrine considers accident history, local conditions, and technological solutions (e.g., active warning systems).
        """,
        key_factors=[
            "Train speed",
            "Vehicle approach speed",
            "Environmental factors",
            "Visibility standards",
            "Maintenance records"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Federal Highway Administration (FHWA)"
        ],
        burden_holder="Railroad and public authority",
        adversary_position="Current sight distance is adequate",
        counter_arguments=[
            "Accident history supports need for improvements",
            "Visibility is critical for safety",
            "Regulatory standards evolve"
        ],
        resolution_strategy="Risk assessment, compliance audits, and funding programs",
        entity_scope="Railroad crossings",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA/FHWA Crossing Safety Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Fuel System Safety",
        keywords=["Locomotive", "Fuel System", "Safety", "Design", "Maintenance", "Regulations"],
        conclusion_template="Locomotive fuel systems must meet safety standards for design, installation, and maintenance.",
        reasoning_framework="""
        FRA regulations specify requirements for fuel system design, installation, and maintenance to prevent leaks, fires, and environmental hazards. Railroads must inspect fuel systems regularly, document findings, and address deficiencies. The doctrine considers technological advances, accident history, and operational impact. Compliance is verified through inspections and certification.
        """,
        key_factors=[
            "Fuel system design",
            "Inspection frequency",
            "Maintenance records",
            "Deficiency remediation",
            "Regulatory standards"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 229"
        ],
        burden_holder="Railroad operator",
        adversary_position="Fuel system standards are outdated",
        counter_arguments=[
            "Accident history supports stricter standards",
            "Technological advances improve safety",
            "Regulatory compliance is mandatory"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and system upgrades",
        entity_scope="Locomotives",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Locomotive Safety Standards"
    ),
    DoctrineBlock(
        topic="Railroad Trespasser Prevention Measures",
        keywords=["Trespasser", "Prevention", "Railroad", "Safety", "Education", "Enforcement"],
        conclusion_template="Railroads must implement trespasser prevention measures, including education and enforcement.",
        reasoning_framework="""
        Trespasser prevention measures include public education campaigns, fencing, signage, and law enforcement collaboration. FRA and industry partners provide guidelines and funding for prevention programs. The doctrine considers accident history, local conditions, and effectiveness of interventions. Railroads must document efforts and evaluate outcomes.
        """,
        key_factors=[
            "Public education",
            "Fencing and signage",
            "Law enforcement collaboration",
            "Accident history",
            "Program evaluation"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Operation Lifesaver"
        ],
        burden_holder="Railroad operator",
        adversary_position="Trespasser incidents are unavoidable",
        counter_arguments=[
            "Prevention measures reduce incidents",
            "Education improves public awareness",
            "Collaboration enhances effectiveness"
        ],
        resolution_strategy="Program evaluation, stakeholder engagement, and funding",
        entity_scope="Railroad property",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Operation Lifesaver Guidelines"
    ),
    DoctrineBlock(
        topic="Rail Fatigue and Defect Growth",
        keywords=["Rail Fatigue", "Defect Growth", "Safety", "Inspection", "Maintenance", "Technology"],
        conclusion_template="Railroads must monitor rail fatigue and defect growth to prevent failures and accidents.",
        reasoning_framework="""
        Rail fatigue and defect growth are monitored through ultrasonic testing, visual inspections, and data analytics. FRA regulations specify inspection intervals and defect classification. Early detection and remediation prevent catastrophic failures. The doctrine emphasizes preventive maintenance, technological upgrades, and compliance with regulatory standards.
        """,
        key_factors=[
            "Ultrasonic testing",
            "Inspection frequency",
            "Defect classification",
            "Preventive maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 213"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current inspection methods are sufficient",
        counter_arguments=[
            "Defect growth can cause derailments",
            "Technological upgrades improve detection",
            "Regulatory standards require continuous improvement"
        ],
        resolution_strategy="Data-driven maintenance, regulatory audits, and technology upgrades",
        entity_scope="All railroad tracks",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA Rail Inspection Standards"
    ),
    DoctrineBlock(
        topic="Passenger Train Emergency Evacuation",
        keywords=["Passenger Train", "Emergency Evacuation", "Safety", "Procedures", "Training", "Regulations"],
        conclusion_template="Passenger rail operators must develop and implement emergency evacuation procedures.",
        reasoning_framework="""
        FRA regulations require passenger rail operators to develop emergency evacuation procedures, train personnel, and conduct drills. Procedures must address communication, coordination with emergency responders, and accessibility for disabled passengers. The doctrine considers accident history, operational complexity, and regulatory compliance. Periodic reviews and updates are mandatory.
        """,
        key_factors=[
            "Evacuation procedures",
            "Personnel training",
            "Emergency responder coordination",
            "Accessibility",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 239"
        ],
        burden_holder="Passenger rail operator",
        adversary_position="Current procedures are adequate",
        counter_arguments=[
            "Accident history supports need for improvements",
            "Training improves effectiveness",
            "Regulatory standards evolve"
        ],
        resolution_strategy="Drills, audits, and procedural updates",
        entity_scope="Passenger rail operators",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Passenger Train Emergency Standards"
    ),
    DoctrineBlock(
        topic="Superelevation and Curve Maintenance",
        keywords=["Superelevation", "Curve Maintenance", "Track Geometry", "Safety", "Inspection", "Regulations"],
        conclusion_template="Railroads must maintain superelevation and curve geometry to ensure safe train operations.",
        reasoning_framework="""
        Superelevation (cant) and curve geometry are critical for safe train operations, especially at higher speeds. FRA regulations specify minimum standards and inspection intervals. Railroads must monitor geometry, document findings, and address deficiencies. The doctrine considers train speed, curve radius, and maintenance practices. Non-compliance results in operational restrictions and enforcement actions.
        """,
        key_factors=[
            "Superelevation measurement",
            "Curve radius",
            "Inspection frequency",
            "Maintenance practices",
            "Regulatory standards"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 213"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current maintenance practices are sufficient",
        counter_arguments=[
            "Geometry deficiencies cause derailments",
            "Regulatory standards require continuous improvement",
            "Higher speeds demand stricter controls"
        ],
        resolution_strategy="Technical audits, regulatory enforcement, and system upgrades",
        entity_scope="All railroad tracks",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Track Geometry Standards"
    ),
    DoctrineBlock(
        topic="Railroad Signal System Reliability",
        keywords=["Signal System", "Reliability", "Failure", "Safety", "Maintenance", "Testing"],
        conclusion_template="Railroads must ensure signal system reliability through regular maintenance and testing.",
        reasoning_framework="""
        Signal system reliability is achieved through preventive maintenance, periodic testing, and redundancy. FRA regulations require documentation of maintenance activities and prompt remediation of failures. The doctrine considers system complexity, integration with PTC, and operational impact. Non-compliance results in enforcement actions and operational restrictions.
        """,
        key_factors=[
            "Preventive maintenance",
            "Testing frequency",
            "Redundancy",
            "Failure remediation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 236"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current reliability is adequate",
        counter_arguments=[
            "Signal failures cause accidents",
            "Regulatory standards require continuous improvement",
            "Integration with PTC enhances reliability"
        ],
        resolution_strategy="Technical audits, regulatory enforcement, and system upgrades",
        entity_scope="Railroad operators",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Signal System Standards"
    ),
    DoctrineBlock(
        topic="Railroad Emergency Response Coordination",
        keywords=["Emergency Response", "Coordination", "Railroad", "Safety", "Training", "Regulations"],
        conclusion_template="Railroads must coordinate emergency response plans with local authorities and conduct joint training.",
        reasoning_framework="""
        FRA regulations require railroads to develop emergency response plans, coordinate with local authorities, and conduct joint training exercises. Plans must address communication, resource allocation, and hazardous material incidents. The doctrine considers accident history, operational complexity, and regulatory compliance. Periodic reviews and updates are mandatory.
        """,
        key_factors=[
            "Emergency response planning",
            "Local authority coordination",
            "Joint training",
            "Communication protocols",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 239"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current coordination is adequate",
        counter_arguments=[
            "Accident history supports need for improvements",
            "Joint training improves effectiveness",
            "Regulatory standards evolve"
        ],
        resolution_strategy="Drills, audits, and procedural updates",
        entity_scope="Railroad operators",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Emergency Response Standards"
    ),
    DoctrineBlock(
        topic="Railroad Asset Management and Lifecycle Planning",
        keywords=["Asset Management", "Lifecycle Planning", "Railroad", "Maintenance", "Safety", "Investment"],
        conclusion_template="Railroads must implement asset management and lifecycle planning to optimize maintenance and safety.",
        reasoning_framework="""
        Asset management and lifecycle planning involve inventorying assets, assessing condition, forecasting maintenance needs, and prioritizing investments. FRA encourages adoption of asset management systems to improve reliability and reduce costs. The doctrine considers technological advances, data analytics, and regulatory compliance. Periodic reviews and updates are mandatory.
        """,
        key_factors=[
            "Asset inventory",
            "Condition assessment",
            "Maintenance forecasting",
            "Investment prioritization",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Industry best practices"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current asset management practices are sufficient",
        counter_arguments=[
            "Data-driven planning improves reliability",
            "Regulatory standards require continuous improvement",
            "Technological advances enhance effectiveness"
        ],
        resolution_strategy="System upgrades, audits, and procedural updates",
        entity_scope="Railroad operators",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA Asset Management Guidelines"
    ),
    DoctrineBlock(
        topic="Railroad Track Maintenance-of-Way Equipment Safety",
        keywords=["Track Maintenance", "Maintenance-of-Way", "Equipment", "Safety", "Inspection", "Regulations"],
        conclusion_template="Maintenance-of-way equipment must meet safety standards for operation, inspection, and maintenance.",
        reasoning_framework="""
        FRA regulations specify requirements for maintenance-of-way equipment, including inspection, maintenance, and operator training. Railroads must document activities and address deficiencies promptly. The doctrine considers technological advances, accident history, and operational impact. Compliance is verified through inspections and certification.
        """,
        key_factors=[
            "Equipment inspection",
            "Maintenance records",
            "Operator training",
            "Deficiency remediation",
            "Regulatory standards"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 214"
        ],
        burden_holder="Railroad operator",
        adversary_position="Equipment standards are outdated",
        counter_arguments=[
            "Accident history supports stricter standards",
            "Technological advances improve safety",
            "Regulatory compliance is mandatory"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and system upgrades",
        entity_scope="Maintenance-of-way equipment",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Maintenance-of-Way Equipment Standards"
    ),
    DoctrineBlock(
        topic="Railroad Environmental Impact Mitigation",
        keywords=["Environmental Impact", "Mitigation", "Railroad", "Safety", "Regulations", "Sustainability"],
        conclusion_template="Railroads must implement environmental impact mitigation measures in compliance with federal regulations.",
        reasoning_framework="""
        Environmental impact mitigation measures include pollution control, habitat preservation, and noise reduction. FRA and EPA regulations require railroads to assess impacts, implement mitigation strategies, and document compliance. The doctrine considers technological advances, cost, and operational impact. Periodic reviews and updates are mandatory.
        """,
        key_factors=[
            "Impact assessment",
            "Mitigation strategies",
            "Documentation",
            "Technological advances",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Environmental Protection Agency (EPA)"
        ],
        burden_holder="Railroad operator",
        adversary_position="Mitigation measures are too costly",
        counter_arguments=[
            "Environmental compliance is mandatory",
            "Technological advances lower costs",
            "Public support for sustainability"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and stakeholder engagement",
        entity_scope="Railroad operators",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="EPA Environmental Impact Regulations"
    ),
    DoctrineBlock(
        topic="Railroad Cybersecurity and Data Protection",
        keywords=["Cybersecurity", "Data Protection", "Railroad", "Safety", "Technology", "Regulations"],
        conclusion_template="Railroads must implement cybersecurity measures to protect operational and safety-critical data.",
        reasoning_framework="""
        FRA and DHS guidelines require railroads to implement cybersecurity measures, including firewalls, encryption, access controls, and incident response plans. The doctrine considers technological advances, threat landscape, and regulatory compliance. Periodic reviews and updates are mandatory. Data breaches can compromise safety and operational integrity.
        """,
        key_factors=[
            "Cybersecurity measures",
            "Incident response planning",
            "Access controls",
            "Technological advances",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Department of Homeland Security (DHS)"
        ],
        burden_holder="Railroad operator",
        adversary_position="Cybersecurity measures are unnecessary",
        counter_arguments=[
            "Data breaches compromise safety",
            "Regulatory standards require continuous improvement",
            "Technological advances enhance effectiveness"
        ],
        resolution_strategy="System upgrades, audits, and procedural updates",
        entity_scope="Railroad operators",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="DHS Cybersecurity Guidelines"
    ),
    DoctrineBlock(
        topic="Railroad Noise and Vibration Control",
        keywords=["Noise", "Vibration", "Control", "Railroad", "Safety", "Regulations"],
        conclusion_template="Railroads must implement noise and vibration control measures in compliance with federal regulations.",
        reasoning_framework="""
        FRA and EPA regulations require railroads to assess noise and vibration impacts, implement control measures, and document compliance. The doctrine considers technological advances, cost, and operational impact. Periodic reviews and updates are mandatory. Public complaints and environmental assessments drive improvements.
        """,
        key_factors=[
            "Impact assessment",
            "Control measures",
            "Documentation",
            "Technological advances",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Environmental Protection Agency (EPA)"
        ],
        burden_holder="Railroad operator",
        adversary_position="Control measures are too costly",
        counter_arguments=[
            "Environmental compliance is mandatory",
            "Technological advances lower costs",
            "Public support for mitigation"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and stakeholder engagement",
        entity_scope="Railroad operators",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="EPA Noise and Vibration Regulations"
    ),
    DoctrineBlock(
        topic="Railroad Grade Crossing Accident Liability",
        keywords=["Grade Crossing", "Accident", "Liability", "Railroad", "Safety", "Regulations"],
        conclusion_template="Railroads may be liable for grade crossing accidents if warning systems or maintenance are inadequate.",
        reasoning_framework="""
        Liability for grade crossing accidents is determined by evaluating warning system adequacy, maintenance records, and compliance with regulatory standards. Courts consider accident history, local conditions, and contributory negligence. FRA and FHWA provide guidelines for minimum standards. The doctrine emphasizes prevention, documentation, and continuous improvement.
        """,
        key_factors=[
            "Warning system adequacy",
            "Maintenance records",
            "Regulatory compliance",
            "Accident history",
            "Contributory negligence"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Federal Highway Administration (FHWA)"
        ],
        burden_holder="Railroad operator",
        adversary_position="Accident was caused by external factors",
        counter_arguments=[
            "Warning system upgrades reduce risk",
            "Regulatory standards require continuous improvement",
            "Documentation supports liability defense"
        ],
        resolution_strategy="Risk assessment, compliance audits, and legal review",
        entity_scope="Railroad crossings",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA/FHWA Crossing Safety Guidelines"
    ),
    DoctrineBlock(
        topic="Railroad Crew Fatigue Management",
        keywords=["Crew Fatigue", "Management", "Railroad", "Safety", "Regulations", "Scheduling"],
        conclusion_template="Railroads must implement crew fatigue management programs in compliance with federal regulations.",
        reasoning_framework="""
        FRA regulations require railroads to develop crew fatigue management programs, including scheduling practices, rest requirements, and education. The doctrine considers accident history, operational complexity, and regulatory compliance. Periodic reviews and updates are mandatory. Crew fatigue is a known safety risk.
        """,
        key_factors=[
            "Scheduling practices",
            "Rest requirements",
            "Education",
            "Accident history",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 228"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current fatigue management practices are sufficient",
        counter_arguments=[
            "Fatigue causes accidents",
            "Regulatory standards require continuous improvement",
            "Education improves effectiveness"
        ],
        resolution_strategy="Program evaluation, audits, and procedural updates",
        entity_scope="Railroad operators",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Crew Fatigue Management Standards"
    ),
    DoctrineBlock(
        topic="Railroad Track Clearance and Vegetation Control",
        keywords=["Track Clearance", "Vegetation Control", "Railroad", "Safety", "Inspection", "Regulations"],
        conclusion_template="Railroads must maintain track clearance and control vegetation to ensure safe operations.",
        reasoning_framework="""
        FRA regulations specify requirements for track clearance and vegetation control, including inspection intervals and remediation protocols. Railroads must document activities and address deficiencies promptly. The doctrine considers accident history, operational impact, and regulatory compliance. Non-compliance results in enforcement actions and operational restrictions.
        """,
        key_factors=[
            "Inspection frequency",
            "Remediation protocols",
            "Documentation",
            "Accident history",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 213"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current clearance practices are sufficient",
        counter_arguments=[
            "Vegetation can obscure signals and crossings",
            "Regulatory standards require continuous improvement",
            "Documentation supports compliance"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and system upgrades",
        entity_scope="All railroad tracks",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA Track Clearance Standards"
    ),
    DoctrineBlock(
        topic="Railroad Employee Training and Certification",
        keywords=["Employee Training", "Certification", "Railroad", "Safety", "Regulations", "Compliance"],
        conclusion_template="Railroads must provide employee training and certification in compliance with federal regulations.",
        reasoning_framework="""
        FRA regulations require railroads to provide training and certification for employees in safety-critical positions. Programs must address operational rules, emergency procedures, and technical skills. The doctrine considers accident history, operational complexity, and regulatory compliance. Periodic reviews and updates are mandatory.
        """,
        key_factors=[
            "Training program design",
            "Certification requirements",
            "Operational rules",
            "Emergency procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 240"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current training programs are sufficient",
        counter_arguments=[
            "Training improves safety",
            "Regulatory standards require continuous improvement",
            "Certification ensures competency"
        ],
        resolution_strategy="Program evaluation, audits, and procedural updates",
        entity_scope="Railroad employees",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Employee Training Standards"
    ),
    DoctrineBlock(
        topic="Railroad Grade Crossing Closure and Consolidation",
        keywords=["Grade Crossing", "Closure", "Consolidation", "Railroad", "Safety", "Regulations"],
        conclusion_template="Railroads and public authorities should pursue grade crossing closure and consolidation to reduce accident risk.",
        reasoning_framework="""
        FRA and FHWA encourage closure and consolidation of redundant or high-risk grade crossings to reduce accident risk. The doctrine considers traffic volume, accident history, and local conditions. Public engagement and funding programs support implementation. Railroads must document efforts and evaluate outcomes.
        """,
        key_factors=[
            "Traffic volume",
            "Accident history",
            "Local conditions",
            "Public engagement",
            "Funding programs"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "Federal Highway Administration (FHWA)"
        ],
        burden_holder="Railroad and public authority",
        adversary_position="Closure disrupts local access",
        counter_arguments=[
            "Consolidation reduces accident risk",
            "Funding supports alternative access",
            "Regulatory standards encourage closure"
        ],
        resolution_strategy="Risk assessment, compliance audits, and stakeholder engagement",
        entity_scope="Railroad crossings",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA/FHWA Crossing Closure Guidelines"
    ),
    DoctrineBlock(
        topic="Railroad Tank Car Retrofit and Replacement",
        keywords=["Tank Car", "Retrofit", "Replacement", "Railroad", "Safety", "Regulations"],
        conclusion_template="Railroads must retrofit or replace tank cars to meet current safety standards.",
        reasoning_framework="""
        DOT and FRA regulations require railroads to retrofit or replace tank cars carrying hazardous materials to meet current safety standards. Requirements include enhanced structural integrity, thermal protection, and pressure relief devices. Compliance is verified through inspections and certification. The doctrine considers technological advances, cost, and operational impact.
        """,
        key_factors=[
            "Structural integrity",
            "Thermal protection",
            "Pressure relief devices",
            "Inspection and certification",
            "Regulatory standards"
        ],
        primary_authority=[
            "Department of Transportation (DOT)",
            "Federal Railroad Administration (FRA)"
        ],
        burden_holder="Railroad operator",
        adversary_position="Retrofit and replacement are too costly",
        counter_arguments=[
            "Safety standards reduce accident severity",
            "Technological advances lower costs",
            "Regulatory compliance is mandatory"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and industry collaboration",
        entity_scope="Tank cars transporting hazardous materials",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="DOT Tank Car Safety Regulations"
    ),
    DoctrineBlock(
        topic="Railroad Track Structure and Ballast Maintenance",
        keywords=["Track Structure", "Ballast Maintenance", "Railroad", "Safety", "Inspection", "Regulations"],
        conclusion_template="Railroads must maintain track structure and ballast to ensure safe operations.",
        reasoning_framework="""
        FRA regulations specify requirements for track structure and ballast maintenance, including inspection intervals and remediation protocols. Railroads must document activities and address deficiencies promptly. The doctrine considers accident history, operational impact, and regulatory compliance. Non-compliance results in enforcement actions and operational restrictions.
        """,
        key_factors=[
            "Inspection frequency",
            "Remediation protocols",
            "Documentation",
            "Accident history",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 213"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current maintenance practices are sufficient",
        counter_arguments=[
            "Ballast deficiencies cause track instability",
            "Regulatory standards require continuous improvement",
            "Documentation supports compliance"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and system upgrades",
        entity_scope="All railroad tracks",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Track Structure Standards"
    ),
    DoctrineBlock(
        topic="Railroad Locomotive Cab Ergonomics",
        keywords=["Locomotive Cab", "Ergonomics", "Railroad", "Safety", "Design", "Regulations"],
        conclusion_template="Locomotive cabs must be designed for ergonomic safety and compliance with federal standards.",
        reasoning_framework="""
        FRA regulations specify requirements for locomotive cab ergonomics, including seating, controls, visibility, and environmental conditions. Railroads must document compliance and address deficiencies promptly. The doctrine considers accident history, operational impact, and regulatory compliance. Periodic reviews and updates are mandatory.
        """,
        key_factors=[
            "Seating design",
            "Control layout",
            "Visibility",
            "Environmental conditions",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 229"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current cab designs are sufficient",
        counter_arguments=[
            "Ergonomics improve crew safety",
            "Regulatory standards require continuous improvement",
            "Documentation supports compliance"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and system upgrades",
        entity_scope="Locomotives",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRA Locomotive Cab Standards"
    ),
    DoctrineBlock(
        topic="Railroad Track Buckling Prevention",
        keywords=["Track Buckling", "Prevention", "Railroad", "Safety", "Inspection", "Regulations"],
        conclusion_template="Railroads must implement track buckling prevention measures in compliance with federal standards.",
        reasoning_framework="""
        FRA regulations specify requirements for track buckling prevention, including inspection intervals, temperature monitoring, and remediation protocols. Railroads must document activities and address deficiencies promptly. The doctrine considers accident history, operational impact, and regulatory compliance. Non-compliance results in enforcement actions and operational restrictions.
        """,
        key_factors=[
            "Inspection frequency",
            "Temperature monitoring",
            "Remediation protocols",
            "Accident history",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Federal Railroad Administration (FRA)",
            "49 CFR Part 213"
        ],
        burden_holder="Railroad operator",
        adversary_position="Current prevention practices are sufficient",
        counter_arguments=[
            "Buckling causes derailments",
            "Regulatory standards require continuous improvement",
            "Documentation supports compliance"
        ],
        resolution_strategy="Technical review, regulatory enforcement, and system upgrades",
        entity_scope="All railroad tracks",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Track Buckling Standards"
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