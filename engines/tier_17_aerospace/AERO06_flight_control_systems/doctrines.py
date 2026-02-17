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
        topic="Airbus FBW Normal Law Architecture",
        keywords=["FBW", "Normal Law", "Airbus", "Flight Envelope Protection", "Pitch", "Roll", "Yaw"],
        conclusion_template="The Airbus FBW Normal Law provides full flight envelope protection and harmonized control response.",
        reasoning_framework=(
            "The Airbus Fly-By-Wire (FBW) Normal Law is designed to ensure aircraft stability and control by implementing "
            "flight envelope protections, load factor demand, and harmonized pitch/roll/yaw response. The system interprets pilot inputs "
            "as requests for flight path changes rather than direct surface deflections. Protections include high angle-of-attack, "
            "high speed, and load factor limits. The Normal Law transitions to Alternate or Direct Law in case of system degradation. "
            "The architecture is triplex redundant, with cross-monitoring between Flight Control Computers (FCCs). "
            "Failure detection and reconfiguration logic are embedded to maintain safety and controllability."
        ),
        key_factors=[
            "Triplex redundancy of FCCs",
            "Flight envelope protection algorithms",
            "Transition logic to Alternate/Direct Law",
            "Load factor demand control",
            "Pilot input interpretation"
        ],
        primary_authority=[
            "Airbus FCS Design Manual",
            "EASA CS-25.671",
            "FAR 25.671"
        ],
        burden_holder="System Integrator",
        adversary_position="Direct control laws offer more pilot authority and may be preferable in some failure scenarios.",
        counter_arguments=[
            "Normal Law ensures safety by preventing exceedance of structural and aerodynamic limits.",
            "Direct laws lack envelope protection, increasing risk in high workload scenarios."
        ],
        resolution_strategy="Retain Normal Law as default; ensure robust transition logic to degraded modes.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Airbus A320/A330/A340 FBW Certification"
    ),
    DoctrineBlock(
        topic="Airbus FBW Alternate Law Degradation",
        keywords=["FBW", "Alternate Law", "Degradation", "Protections", "Failure Modes"],
        conclusion_template="Alternate Law provides reduced protections and is activated upon certain system failures.",
        reasoning_framework=(
            "Alternate Law is engaged when certain failures or sensor discrepancies are detected in the Normal Law architecture. "
            "This law retains some, but not all, flight envelope protections (e.g., load factor limitation may remain, but high angle-of-attack "
            "protection is lost). The system automatically transitions to Alternate Law based on predefined failure logic. "
            "The pilot is notified via ECAM and PFD annunciations. The design ensures that the aircraft remains controllable, "
            "but with increased pilot responsibility for maintaining safe flight parameters."
        ),
        key_factors=[
            "Failure detection logic",
            "Loss of specific protections",
            "Pilot notification",
            "Manual trim requirements"
        ],
        primary_authority=[
            "Airbus FCS Failure Management",
            "EASA AMC 25.1309",
            "FAR 25.1309"
        ],
        burden_holder="Flight Control System Architect",
        adversary_position="Alternate Law transition may surprise pilots and increase workload.",
        counter_arguments=[
            "Comprehensive pilot training mitigates surprise.",
            "System provides clear annunciations and checklists."
        ],
        resolution_strategy="Ensure clear transition logic and pilot notification; update training programs.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Airbus A320 Alternate Law Implementation"
    ),
    DoctrineBlock(
        topic="Boeing Control Law Philosophy vs Airbus",
        keywords=["Boeing", "Airbus", "Control Law", "Philosophy", "Pilot Authority", "Protections"],
        conclusion_template="Boeing and Airbus differ fundamentally in FBW control law philosophy regarding pilot authority and protections.",
        reasoning_framework=(
            "Boeing FBW systems (e.g., 777, 787) are designed to preserve traditional pilot authority, allowing override of envelope protections, "
            "whereas Airbus FBW prioritizes flight envelope protection, preventing the pilot from exceeding structural/aerodynamic limits. "
            "Boeing's approach is to provide tactile feedback and warnings, but not hard limits, while Airbus uses hard limits and automatic recovery. "
            "These philosophies impact pilot training, system design, and failure mode management."
        ),
        key_factors=[
            "Pilot authority vs system protection",
            "Override capability",
            "Training implications",
            "Certification requirements"
        ],
        primary_authority=[
            "Boeing 777/787 System Description",
            "Airbus FCS Philosophy",
            "FAA AC 25-7C"
        ],
        burden_holder="Certification Applicant",
        adversary_position="Hard limits may prevent pilot recovery in some scenarios; full authority may increase risk.",
        counter_arguments=[
            "Envelope protection reduces risk of loss-of-control.",
            "Override capability allows recovery from system faults."
        ],
        resolution_strategy="Balance between protection and authority based on operational analysis and certification guidance.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA/EASA Certification of 777 vs A320"
    ),
    DoctrineBlock(
        topic="C* Control Law Implementation",
        keywords=["C*", "Control Law", "Pitch Rate", "Load Factor", "FBW"],
        conclusion_template="C* control law provides harmonized pitch response by blending pitch rate and load factor feedback.",
        reasoning_framework=(
            "The C* control law is a pitch axis control strategy that combines pitch rate and load factor feedback to achieve consistent handling qualities "
            "across the flight envelope. It is implemented in both Boeing and Airbus FBW systems. The C* law is tuned to provide a linear relationship "
            "between sidestick/yoke input and aircraft response, reducing pilot workload and improving safety. Implementation requires accurate sensor data, "
            "robust filtering, and failure monitoring."
        ),
        key_factors=[
            "Pitch rate feedback",
            "Load factor feedback",
            "Sensor accuracy",
            "Control law tuning"
        ],
        primary_authority=[
            "MIL-F-8785C",
            "Airbus/Boeing FCS Design Guides"
        ],
        burden_holder="Control Law Designer",
        adversary_position="Over-reliance on feedback may mask underlying aircraft response issues.",
        counter_arguments=[
            "Extensive flight test validation ensures safe and predictable response.",
            "Redundant sensors mitigate risk of erroneous feedback."
        ],
        resolution_strategy="Validate C* law implementation with simulation and flight test; ensure robust sensor monitoring.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="C* Law in Airbus A320/Boeing 777"
    ),
    DoctrineBlock(
        topic="Hydraulic vs Electro-Hydrostatic Actuator Trade-offs",
        keywords=["Hydraulic", "EHA", "Actuator", "Trade-off", "Reliability", "Weight"],
        conclusion_template="Electro-Hydrostatic Actuators (EHAs) offer weight and maintenance advantages but require robust power and thermal management.",
        reasoning_framework=(
            "Traditional hydraulic actuators rely on centralized hydraulic systems, offering proven reliability but at the cost of weight, complexity, "
            "and maintenance. EHAs are self-contained units powered electrically, reducing hydraulic plumbing and potential leak points. "
            "However, EHAs require careful design for electrical power redundancy, thermal dissipation, and failure detection. Certification requires "
            "demonstration of equivalent safety and reliability."
        ),
        key_factors=[
            "System weight",
            "Power redundancy",
            "Thermal management",
            "Maintenance requirements"
        ],
        primary_authority=[
            "EASA CS-25.901",
            "FAR 25.901",
            "Airbus/Boeing EHA Evaluation Reports"
        ],
        burden_holder="Actuator System Designer",
        adversary_position="EHAs may introduce new failure modes (e.g., electrical faults, thermal runaway).",
        counter_arguments=[
            "Redundant power supplies and thermal monitoring mitigate risks.",
            "EHAs have demonstrated reliability in service (e.g., A380, B787)."
        ],
        resolution_strategy="Implement EHAs with robust redundancy and monitoring; retain hydraulics for critical surfaces as needed.",
        entity_scope="AERO06 Actuation Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EHA Use on A380/B787"
    ),
    DoctrineBlock(
        topic="Actuator Jam Detection and Mitigation",
        keywords=["Actuator Jam", "Detection", "Mitigation", "Redundancy", "FBW"],
        conclusion_template="Redundant actuator design and jam detection logic are essential for continued safe flight after a jam.",
        reasoning_framework=(
            "Actuator jams can result from mechanical or electrical faults. Detection is achieved through monitoring of commanded vs actual position, "
            "force fight detection, and cross-channel comparison. Mitigation strategies include mechanical disconnects, force-limited breakouts, "
            "and control law reconfiguration. Certification requires demonstration that a single jam does not lead to loss of control."
        ),
        key_factors=[
            "Commanded vs actual position monitoring",
            "Force fight detection",
            "Mechanical disconnects",
            "Control law reconfiguration"
        ],
        primary_authority=[
            "EASA AMC 25.671",
            "FAR 25.671",
            "Airbus/Boeing Jam Mitigation Studies"
        ],
        burden_holder="Flight Control System Safety Engineer",
        adversary_position="Complex detection logic may increase false positives, leading to nuisance alerts.",
        counter_arguments=[
            "Adaptive thresholds and cross-validation reduce false positives.",
            "Mechanical solutions provide last-resort safety."
        ],
        resolution_strategy="Combine electronic detection with mechanical mitigation; validate with system safety analysis.",
        entity_scope="AERO06 Actuation Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="A320/B777 Jam Detection Certification"
    ),
    DoctrineBlock(
        topic="Flight Control Computer Redundancy Architecture",
        keywords=["FCC", "Redundancy", "Architecture", "Triplex", "Quadruplex", "Voting"],
        conclusion_template="Triplex or quadruplex redundant FCC architectures ensure continued safe operation after single failures.",
        reasoning_framework=(
            "Flight Control Computer (FCC) redundancy is achieved through triplex or quadruplex architectures, with cross-monitoring and voting logic. "
            "Each FCC operates independently, comparing results with peers. Disagreement triggers isolation of faulty units. "
            "Redundancy ensures compliance with fail-operational/fail-safe requirements. Power and data bus segregation further enhance reliability."
        ),
        key_factors=[
            "Number of FCC channels",
            "Cross-monitoring logic",
            "Power/data segregation",
            "Failure isolation"
        ],
        primary_authority=[
            "EASA CS-25.1309",
            "FAR 25.1309",
            "DO-254"
        ],
        burden_holder="System Architect",
        adversary_position="Increased complexity may introduce integration and maintenance challenges.",
        counter_arguments=[
            "Redundancy is essential for safety-critical functions.",
            "Modular design and built-in test simplify maintenance."
        ],
        resolution_strategy="Adopt triplex/quadruplex FCCs with robust cross-monitoring; document maintenance procedures.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="A320/B777 FCC Redundancy"
    ),
    DoctrineBlock(
        topic="Autopilot LNAV and VNAV Mode Logic",
        keywords=["Autopilot", "LNAV", "VNAV", "Mode Logic", "Lateral Navigation", "Vertical Navigation"],
        conclusion_template="Autopilot LNAV/VNAV logic must ensure smooth transitions and robust mode annunciation for pilot awareness.",
        reasoning_framework=(
            "Lateral Navigation (LNAV) and Vertical Navigation (VNAV) modes automate flight path tracking and altitude management. "
            "Mode logic must handle transitions (e.g., from climb to cruise, or approach modes), with clear annunciation on the Primary Flight Display (PFD). "
            "Robust engagement/disengagement logic and failure monitoring are required to prevent mode confusion and ensure compliance with flight crew expectations."
        ),
        key_factors=[
            "Mode transition logic",
            "Annunciation and alerts",
            "Engagement/disengagement criteria",
            "Failure monitoring"
        ],
        primary_authority=[
            "EASA CS-25.1329",
            "FAR 25.1329",
            "DO-178C"
        ],
        burden_holder="Autopilot System Designer",
        adversary_position="Complex mode logic may increase risk of pilot confusion and mode errors.",
        counter_arguments=[
            "Standardized mode annunciation and pilot training mitigate confusion.",
            "Mode logic is validated through extensive simulation and flight test."
        ],
        resolution_strategy="Implement clear mode transitions and annunciation; conduct human factors evaluation.",
        entity_scope="AERO06 Autopilot System",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Boeing/Airbus Autopilot Certification"
    ),
    DoctrineBlock(
        topic="Autoland System Requirements and Categories",
        keywords=["Autoland", "System Requirements", "Categories", "CAT II", "CAT III", "Redundancy"],
        conclusion_template="Autoland systems must meet CAT II/III requirements for redundancy, failure monitoring, and alerting.",
        reasoning_framework=(
            "Autoland systems enable automatic landing in low-visibility conditions. Certification categories (CAT II, CAT IIIa/b/c) define minimum "
            "performance, redundancy, and alerting requirements. The system must detect and annunciate failures, revert to safe modes, and provide "
            "adequate redundancy in sensors, computers, and actuators. Pilot alerting and go-around logic are essential for safe operation."
        ),
        key_factors=[
            "Certification category (CAT II/III)",
            "Redundancy of sensors and computers",
            "Failure detection and alerting",
            "Go-around logic"
        ],
        primary_authority=[
            "EASA CS-AWO",
            "FAR 25.1329",
            "ICAO Annex 6"
        ],
        burden_holder="Autoland System Integrator",
        adversary_position="High redundancy increases cost and complexity.",
        counter_arguments=[
            "Safety and operational capability in low-visibility conditions justify complexity.",
            "Modular design can optimize cost."
        ],
        resolution_strategy="Design to meet or exceed CAT IIIb requirements for critical surfaces; modularize where possible.",
        entity_scope="AERO06 Autoland System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Autoland Certification"
    ),
    DoctrineBlock(
        topic="Yaw Damper System Design and Failure Effects",
        keywords=["Yaw Damper", "System Design", "Failure Effects", "Dutch Roll", "Redundancy"],
        conclusion_template="Yaw damper systems must provide automatic Dutch roll damping and fail-safe operation.",
        reasoning_framework=(
            "Yaw damper systems automatically counteract Dutch roll oscillations, improving lateral stability and passenger comfort. "
            "Design must include redundant actuators and control channels, with failure detection and automatic disengagement logic. "
            "Certification requires demonstration that a single failure does not lead to unsafe yaw excursions or pilot workload increase."
        ),
        key_factors=[
            "Dutch roll damping",
            "Redundant actuators/channels",
            "Failure detection",
            "Automatic disengagement"
        ],
        primary_authority=[
            "EASA CS-25.1309",
            "FAR 25.1309",
            "Airbus/Boeing Yaw Damper Certification"
        ],
        burden_holder="Yaw Damper System Designer",
        adversary_position="Automatic disengagement may reduce lateral stability in degraded modes.",
        counter_arguments=[
            "Manual override and pilot training mitigate risk.",
            "Redundant design minimizes likelihood of total loss."
        ],
        resolution_strategy="Implement dual-redundant yaw dampers with robust failure detection and pilot override.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="A320/B777 Yaw Damper Implementation"
    ),
    DoctrineBlock(
        topic="High Angle-of-Attack Protection and Alpha Floor",
        keywords=["High Angle-of-Attack", "Alpha Floor", "Protection", "FBW", "Stall Prevention"],
        conclusion_template="High angle-of-attack protection and alpha floor logic prevent stall and loss-of-control.",
        reasoning_framework=(
            "FBW systems implement high angle-of-attack (AoA) protection by limiting pitch command authority and activating automatic recovery logic (alpha floor) "
            "when critical AoA is approached. Alpha floor triggers automatic thrust increase to prevent stall. These protections are active in Normal Law and are lost "
            "in degraded modes. Sensor redundancy and validation are critical to prevent nuisance activation or missed protection."
        ),
        key_factors=[
            "AoA sensor redundancy",
            "Pitch command limiting",
            "Alpha floor logic",
            "Degraded mode behavior"
        ],
        primary_authority=[
            "EASA CS-25.201",
            "FAR 25.201",
            "Airbus FCS Protection Design"
        ],
        burden_holder="Control Law Designer",
        adversary_position="Sensor faults may trigger inappropriate protection or loss of protection.",
        counter_arguments=[
            "Sensor cross-checking and validation logic mitigate risks.",
            "Pilot training addresses degraded mode operation."
        ],
        resolution_strategy="Implement robust sensor validation and clear pilot annunciation of protection status.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320 Alpha Floor Protection"
    ),
    DoctrineBlock(
        topic="DO-178C Software Certification for Flight Control Systems",
        keywords=["DO-178C", "Software Certification", "Flight Control", "DAL A", "Verification"],
        conclusion_template="Flight control software must be developed and verified to DO-178C DAL A standards.",
        reasoning_framework=(
            "DO-178C defines objectives for software development and verification in airborne systems. Flight control software is typically classified as "
            "Design Assurance Level (DAL) A, requiring the highest rigor in requirements traceability, code review, testing, and independence of verification. "
            "All software components must be covered by requirements-based tests, and structural coverage analysis must demonstrate full path coverage. "
            "Configuration management and change control are strictly enforced."
        ),
        key_factors=[
            "DAL A classification",
            "Requirements traceability",
            "Verification independence",
            "Structural coverage analysis"
        ],
        primary_authority=[
            "DO-178C",
            "EASA AMC 20-115C",
            "FAR 25.1309"
        ],
        burden_holder="Software Development Organization",
        adversary_position="DO-178C compliance increases cost and schedule.",
        counter_arguments=[
            "Rigorous process reduces risk of latent software defects.",
            "Certification is mandatory for flight control systems."
        ],
        resolution_strategy="Allocate sufficient resources for DO-178C compliance; use model-based development where appropriate.",
        entity_scope="AERO06 Flight Control Software",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="A320/B777 FCS Software Certification"
    ),
    DoctrineBlock(
        topic="Control Surface Flutter Analysis and Prevention",
        keywords=["Control Surface", "Flutter", "Analysis", "Prevention", "Aeroelasticity"],
        conclusion_template="Comprehensive flutter analysis and prevention measures are required for all control surfaces.",
        reasoning_framework=(
            "Flutter is a dynamic aeroelastic instability that can lead to catastrophic structural failure. All control surfaces must undergo flutter analysis "
            "using ground vibration testing, computational models, and flight test validation. Prevention measures include mass balancing, structural stiffening, "
            "and active damping. Certification requires demonstration that flutter will not occur within the operational flight envelope plus safety margins."
        ),
        key_factors=[
            "Ground vibration testing",
            "Computational aeroelastic analysis",
            "Mass balancing",
            "Active damping"
        ],
        primary_authority=[
            "EASA CS-25.629",
            "FAR 25.629",
            "Airbus/Boeing Flutter Prevention Reports"
        ],
        burden_holder="Aeroelasticity Engineer",
        adversary_position="Flutter prevention measures may increase weight and complexity.",
        counter_arguments=[
            "Safety requirements take precedence over weight savings.",
            "Advanced materials and design optimization can minimize impact."
        ],
        resolution_strategy="Conduct thorough flutter analysis; optimize prevention measures for weight and performance.",
        entity_scope="AERO06 Flight Control Surfaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Flutter Certification"
    ),
    DoctrineBlock(
        topic="FAR Part 25 Flight Control System Certification Requirements",
        keywords=["FAR Part 25", "Certification", "Flight Control System", "Compliance"],
        conclusion_template="AERO06 flight control system must comply with all applicable FAR Part 25 requirements.",
        reasoning_framework=(
            "FAR Part 25 specifies airworthiness standards for transport category airplanes, including flight control system requirements for reliability, "
            "redundancy, failure effects, and crew interface. Compliance is demonstrated through analysis, simulation, and flight test. "
            "Key sections include 25.671 (control systems), 25.1309 (system safety), and 25.201 (stall). All design and verification activities must be "
            "documented for certification authority review."
        ),
        key_factors=[
            "System safety analysis",
            "Redundancy and reliability",
            "Crew interface",
            "Certification documentation"
        ],
        primary_authority=[
            "FAR Part 25",
            "EASA CS-25",
            "FAA/EASA Certification Procedures"
        ],
        burden_holder="Certification Applicant",
        adversary_position="Certification process is resource-intensive and may delay entry into service.",
        counter_arguments=[
            "Compliance is mandatory for market access.",
            "Early engagement with authorities streamlines process."
        ],
        resolution_strategy="Plan certification activities from program inception; allocate resources for compliance demonstration.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="All Part 25 Certified Aircraft"
    ),
    DoctrineBlock(
        topic="Runaway Stabilizer Failure Analysis",
        keywords=["Runaway Stabilizer", "Failure Analysis", "Mitigation", "Certification"],
        conclusion_template="Runaway stabilizer scenarios must be analyzed and mitigated to prevent loss-of-control.",
        reasoning_framework=(
            "Runaway stabilizer failures can result from electrical or mechanical faults causing uncommanded movement. "
            "Analysis includes identification of failure modes, detection logic, and pilot intervention procedures. "
            "Mitigation strategies include cutout switches, automatic disconnects, and control law reconfiguration. "
            "Certification requires demonstration that the pilot can recover control within acceptable workload limits."
        ),
        key_factors=[
            "Failure mode identification",
            "Detection and alerting",
            "Pilot intervention procedures",
            "Automatic disconnects"
        ],
        primary_authority=[
            "EASA CS-25.255",
            "FAR 25.255",
            "FAA AC 25.7C"
        ],
        burden_holder="Flight Control System Safety Engineer",
        adversary_position="Complex mitigation logic may delay pilot intervention.",
        counter_arguments=[
            "Clear alerting and cutout switches enable rapid response.",
            "Automatic disconnects provide backup."
        ],
        resolution_strategy="Combine electronic and manual mitigation; validate with flight crew evaluation.",
        entity_scope="AERO06 Stabilizer System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="B737/A320 Runaway Stabilizer Certification"
    ),
    # Additional 25+ DoctrineBlocks with real domain content follow:
    DoctrineBlock(
        topic="Sidestick Priority and Takeover Logic",
        keywords=["Sidestick", "Priority", "Takeover", "FBW", "Pilot Input"],
        conclusion_template="Sidestick priority logic ensures only one pilot's input is effective at a time, with clear takeover annunciation.",
        reasoning_framework=(
            "In dual-sidestick FBW systems, priority logic is required to resolve simultaneous inputs. The system must annunciate which sidestick is active, "
            "and allow for takeover by pressing a priority button. Both pilots are alerted via visual and aural cues. This prevents control ambiguity and ensures "
            "clear crew coordination. Certification requires demonstration that inadvertent dual input does not compromise safety."
        ),
        key_factors=[
            "Simultaneous input detection",
            "Priority button logic",
            "Annunciation and alerting",
            "Crew procedures"
        ],
        primary_authority=[
            "Airbus FCS Crew Interface",
            "EASA CS-25.1322",
            "FAR 25.1322"
        ],
        burden_holder="Crew Interface Designer",
        adversary_position="Priority logic may delay response in time-critical situations.",
        counter_arguments=[
            "Aural/visual alerts and training mitigate risk.",
            "System defaults to last input for safety."
        ],
        resolution_strategy="Implement clear priority logic and crew alerts; include in crew training.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="A320 Sidestick Priority Certification"
    ),
    DoctrineBlock(
        topic="Load Alleviation Function Implementation",
        keywords=["Load Alleviation", "Function", "Implementation", "Structural Loads", "FBW"],
        conclusion_template="Load alleviation functions reduce structural loads during turbulence and maneuvers, enhancing airframe life.",
        reasoning_framework=(
            "Load alleviation functions use flight control surfaces (e.g., ailerons, elevators, spoilers) to reduce wing and fuselage loads during turbulence, "
            "gusts, or high-g maneuvers. Implementation requires accurate load sensors, real-time data processing, and integration with FBW laws. "
            "Certification requires demonstration that load alleviation does not interfere with primary control or introduce adverse handling qualities."
        ),
        key_factors=[
            "Load sensor accuracy",
            "Control law integration",
            "Real-time processing",
            "Certification flight test"
        ],
        primary_authority=[
            "EASA CS-25.302",
            "FAR 25.302",
            "Airbus/Boeing Load Alleviation Reports"
        ],
        burden_holder="FBW Control Law Designer",
        adversary_position="Load alleviation may conflict with pilot inputs in extreme maneuvers.",
        counter_arguments=[
            "Priority logic ensures pilot authority is maintained.",
            "Flight test validation addresses adverse interactions."
        ],
        resolution_strategy="Integrate load alleviation with pilot input priority; validate with simulation and flight test.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="A350/B787 Load Alleviation Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Power Supply Redundancy",
        keywords=["Power Supply", "Redundancy", "Flight Control System", "Electrical", "Hydraulic"],
        conclusion_template="Flight control systems require multiple independent power sources to ensure continued operation after failures.",
        reasoning_framework=(
            "FBW and hydraulic systems must be powered by at least two independent sources (e.g., AC, DC, RAT, APU, engine-driven generators). "
            "Critical surfaces require triple redundancy for power supply. Automatic load shedding and power transfer logic ensure continued operation "
            "in abnormal conditions. Certification requires demonstration that no single power failure leads to loss of control."
        ),
        key_factors=[
            "Number of independent power sources",
            "Automatic transfer logic",
            "Load shedding",
            "Failure effects analysis"
        ],
        primary_authority=[
            "EASA CS-25.1351",
            "FAR 25.1351",
            "Airbus/Boeing Power Redundancy Design"
        ],
        burden_holder="System Architect",
        adversary_position="Increased redundancy adds weight and complexity.",
        counter_arguments=[
            "Essential for safety-critical systems.",
            "Design optimization can minimize impact."
        ],
        resolution_strategy="Implement triple-redundant power for critical surfaces; optimize for weight and maintainability.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Power Redundancy Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Data Bus Architecture",
        keywords=["Data Bus", "Architecture", "ARINC 429", "AFDX", "Redundancy"],
        conclusion_template="Redundant data bus architectures (e.g., dual/triple AFDX or ARINC 429) are required for flight control system integrity.",
        reasoning_framework=(
            "Flight control systems use redundant data buses (e.g., ARINC 429, AFDX) to ensure reliable communication between FCCs, sensors, and actuators. "
            "Bus segregation prevents single-point failures. Bus guardian logic and error detection/correction are implemented to maintain data integrity. "
            "Certification requires demonstration of continued safe operation after any single bus failure."
        ),
        key_factors=[
            "Bus redundancy and segregation",
            "Error detection/correction",
            "Bus guardian logic",
            "Failure mode analysis"
        ],
        primary_authority=[
            "ARINC 429/AFDX Standards",
            "EASA CS-25.1309",
            "FAR 25.1309"
        ],
        burden_holder="Avionics Architect",
        adversary_position="Bus complexity may increase integration and troubleshooting effort.",
        counter_arguments=[
            "Standardized interfaces and diagnostics simplify maintenance.",
            "Redundancy is essential for safety."
        ],
        resolution_strategy="Adopt dual/triple redundant buses; implement robust diagnostics and documentation.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A350/B787 Data Bus Certification"
    ),
    DoctrineBlock(
        topic="Control Law Transition Logic",
        keywords=["Control Law", "Transition Logic", "Normal Law", "Alternate Law", "Direct Law"],
        conclusion_template="Control law transition logic must ensure safe and predictable reconfiguration after system failures.",
        reasoning_framework=(
            "FBW systems must automatically transition between Normal, Alternate, and Direct Laws based on system health. Transition logic is triggered by "
            "sensor failures, FCC faults, or loss of redundancy. The logic must ensure that the aircraft remains controllable and that the pilot is clearly "
            "notified of the current law. Certification requires demonstration that transitions do not introduce adverse handling or confusion."
        ),
        key_factors=[
            "Failure detection and transition triggers",
            "Pilot notification",
            "Handling qualities in degraded laws",
            "Certification flight test"
        ],
        primary_authority=[
            "Airbus FCS Law Transition Design",
            "EASA CS-25.1309",
            "FAR 25.1309"
        ],
        burden_holder="Control Law Designer",
        adversary_position="Automatic transitions may surprise pilots and increase workload.",
        counter_arguments=[
            "Clear annunciation and training mitigate risk.",
            "Transition logic is validated in simulation and flight test."
        ],
        resolution_strategy="Implement robust transition logic with clear annunciation; update pilot training.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="A320 Law Transition Certification"
    ),
    DoctrineBlock(
        topic="Manual Reversion Procedures",
        keywords=["Manual Reversion", "Procedures", "FBW", "Direct Law", "Degraded Modes"],
        conclusion_template="Manual reversion procedures must be clearly defined and trained for operation in Direct Law.",
        reasoning_framework=(
            "In the event of multiple system failures, FBW systems may revert to Direct Law, where pilot inputs are directly mapped to control surfaces. "
            "Manual reversion procedures must be documented in the QRH and FCOM, with clear training for pilots. Certification requires demonstration that "
            "the aircraft remains controllable and that workload is acceptable."
        ),
        key_factors=[
            "Direct Law handling qualities",
            "QRH/FCOM procedures",
            "Pilot training",
            "Certification flight test"
        ],
        primary_authority=[
            "Airbus FCOM/QRH",
            "EASA CS-25.671",
            "FAR 25.671"
        ],
        burden_holder="Flight Operations",
        adversary_position="Manual reversion may lead to increased workload and reduced handling quality.",
        counter_arguments=[
            "Training and clear procedures mitigate risk.",
            "Direct Law is a last-resort mode."
        ],
        resolution_strategy="Document and train manual reversion procedures; validate in simulator and flight test.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="A320 Manual Reversion Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Built-In Test (BIT)",
        keywords=["Built-In Test", "BIT", "Flight Control System", "Health Monitoring"],
        conclusion_template="Comprehensive BIT is required for continuous health monitoring and fault isolation.",
        reasoning_framework=(
            "BIT functions continuously monitor FCCs, sensors, actuators, and data buses for faults. BIT results are logged and reported to maintenance and crew. "
            "Fault isolation logic enables rapid identification and replacement of failed components. Certification requires demonstration that BIT does not interfere "
            "with normal operation or introduce nuisance alerts."
        ),
        key_factors=[
            "Continuous health monitoring",
            "Fault isolation logic",
            "Crew/maintenance alerting",
            "Certification analysis"
        ],
        primary_authority=[
            "DO-254",
            "EASA CS-25.1309",
            "FAR 25.1309"
        ],
        burden_holder="System Integrator",
        adversary_position="Overly sensitive BIT may increase nuisance alerts and maintenance burden.",
        counter_arguments=[
            "Adaptive thresholds and filtering reduce false positives.",
            "BIT is essential for rapid fault detection."
        ],
        resolution_strategy="Tune BIT sensitivity; validate with operational data and maintenance feedback.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320/B777 BIT Implementation"
    ),
    DoctrineBlock(
        topic="Control Surface Position Feedback and Monitoring",
        keywords=["Control Surface", "Position Feedback", "Monitoring", "Redundancy"],
        conclusion_template="Redundant position feedback sensors are required for all critical control surfaces.",
        reasoning_framework=(
            "Control surface position is monitored by redundant sensors (e.g., LVDTs, RVDTs, potentiometers) to ensure accurate feedback to FCCs. "
            "Discrepancies between sensors trigger fault isolation and reversion logic. Certification requires demonstration that a single sensor failure "
            "does not compromise control."
        ),
        key_factors=[
            "Sensor redundancy",
            "Discrepancy detection",
            "Fault isolation",
            "Certification analysis"
        ],
        primary_authority=[
            "EASA CS-25.671",
            "FAR 25.671",
            "Airbus/Boeing Position Feedback Design"
        ],
        burden_holder="Actuation System Designer",
        adversary_position="Sensor redundancy increases cost and weight.",
        counter_arguments=[
            "Essential for safety-critical feedback.",
            "Design optimization can minimize impact."
        ],
        resolution_strategy="Implement dual/triple redundant sensors; optimize for weight and maintainability.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Position Feedback Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Maintenance Philosophy",
        keywords=["Maintenance", "Philosophy", "Flight Control System", "BIT", "LRU Replacement"],
        conclusion_template="AERO06 FCS maintenance philosophy emphasizes BIT-driven LRU replacement and rapid fault isolation.",
        reasoning_framework=(
            "The maintenance philosophy for AERO06 FCS is based on continuous BIT, modular LRU design, and rapid fault isolation. "
            "BIT alerts maintenance personnel to failed components, which are replaced as LRUs. This minimizes aircraft downtime and ensures high dispatch reliability. "
            "Certification requires demonstration that maintenance procedures do not introduce new hazards."
        ),
        key_factors=[
            "BIT-driven maintenance",
            "LRU modularity",
            "Fault isolation procedures",
            "Certification analysis"
        ],
        primary_authority=[
            "Airbus/Boeing Maintenance Manuals",
            "EASA CS-25.1529",
            "FAR 25.1529"
        ],
        burden_holder="Maintenance Organization",
        adversary_position="LRU replacement may increase spares inventory cost.",
        counter_arguments=[
            "Reduces troubleshooting time and aircraft downtime.",
            "Standardizes maintenance procedures."
        ],
        resolution_strategy="Optimize LRU design and spares management; train maintenance personnel.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="A320/B777 Maintenance Philosophy"
    ),
    DoctrineBlock(
        topic="Flight Control System Security and Data Integrity",
        keywords=["Security", "Data Integrity", "Flight Control System", "Cybersecurity"],
        conclusion_template="Flight control systems must be protected against unauthorized access and data corruption.",
        reasoning_framework=(
            "Flight control systems are increasingly networked, raising cybersecurity and data integrity concerns. "
            "Security measures include physical access controls, encrypted data links, authentication protocols, and intrusion detection. "
            "Certification requires demonstration that unauthorized access or data corruption cannot compromise safety."
        ),
        key_factors=[
            "Physical and logical access controls",
            "Data encryption",
            "Authentication and intrusion detection",
            "Certification analysis"
        ],
        primary_authority=[
            "DO-326A",
            "EASA AMC 20-42",
            "FAR 25.1309"
        ],
        burden_holder="Avionics Security Engineer",
        adversary_position="Security measures may increase system latency and complexity.",
        counter_arguments=[
            "Essential for protection against evolving threats.",
            "Design optimization can minimize performance impact."
        ],
        resolution_strategy="Implement layered security; validate with penetration testing and certification analysis.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="A350/B787 Cybersecurity Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Electromagnetic Compatibility (EMC)",
        keywords=["EMC", "Electromagnetic Compatibility", "Flight Control System", "Susceptibility"],
        conclusion_template="FCS must be designed and tested for EMC to prevent interference and ensure safe operation.",
        reasoning_framework=(
            "Flight control systems must be immune to electromagnetic interference (EMI) from internal and external sources. "
            "Design measures include shielding, filtering, and grounding. EMC testing is performed per RTCA/DO-160 standards. "
            "Certification requires demonstration that EMI does not affect system performance or safety."
        ),
        key_factors=[
            "Shielding and filtering",
            "Grounding",
            "EMC testing",
            "Certification analysis"
        ],
        primary_authority=[
            "RTCA/DO-160",
            "EASA CS-25.1309",
            "FAR 25.1309"
        ],
        burden_holder="Avionics Engineer",
        adversary_position="EMC measures may add weight and complexity.",
        counter_arguments=[
            "Essential for safety in high-EMI environments.",
            "Design optimization can minimize impact."
        ],
        resolution_strategy="Implement EMC measures; validate with laboratory and flight test.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320/B777 EMC Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Environmental Qualification",
        keywords=["Environmental Qualification", "Flight Control System", "DO-160", "Temperature", "Vibration"],
        conclusion_template="All FCS components must be qualified to DO-160 environmental standards.",
        reasoning_framework=(
            "Environmental qualification ensures that all FCS components operate reliably under expected temperature, vibration, humidity, and pressure conditions. "
            "Testing is performed per RTCA/DO-160, with results documented for certification. Qualification covers both normal and abnormal operating environments."
        ),
        key_factors=[
            "Temperature and vibration testing",
            "Humidity and pressure testing",
            "Certification documentation",
            "Abnormal environment analysis"
        ],
        primary_authority=[
            "RTCA/DO-160",
            "EASA CS-25.1309",
            "FAR 25.1309"
        ],
        burden_holder="Environmental Test Engineer",
        adversary_position="Environmental testing increases development time and cost.",
        counter_arguments=[
            "Essential for reliability and certification.",
            "Early planning minimizes schedule impact."
        ],
        resolution_strategy="Plan environmental qualification early; document all results for certification.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Environmental Qualification"
    ),
    DoctrineBlock(
        topic="Flight Control System Human Factors Evaluation",
        keywords=["Human Factors", "Evaluation", "Flight Control System", "Crew Interface"],
        conclusion_template="Human factors evaluation is required to ensure safe and intuitive crew interaction with FCS.",
        reasoning_framework=(
            "Human factors evaluation assesses crew interaction with FCS displays, controls, and alerts. Methods include simulator studies, workload analysis, "
            "and pilot feedback. Certification requires demonstration that crew can operate the system safely under all conditions, with acceptable workload."
        ),
        key_factors=[
            "Simulator studies",
            "Workload analysis",
            "Pilot feedback",
            "Certification flight test"
        ],
        primary_authority=[
            "EASA CS-25.1302",
            "FAR 25.1302",
            "FAA Human Factors Guidance"
        ],
        burden_holder="Human Factors Engineer",
        adversary_position="Human factors evaluation may delay development.",
        counter_arguments=[
            "Essential for safe and intuitive operation.",
            "Early evaluation minimizes late design changes."
        ],
        resolution_strategy="Conduct human factors evaluation early; incorporate feedback into design.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="A320/B777 Human Factors Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Failure Mode and Effects Analysis (FMEA)",
        keywords=["FMEA", "Failure Mode and Effects Analysis", "Flight Control System", "Safety"],
        conclusion_template="Comprehensive FMEA is required to identify and mitigate all credible FCS failure modes.",
        reasoning_framework=(
            "FMEA systematically identifies potential failure modes, their effects, and mitigations for all FCS components. "
            "Results inform redundancy, monitoring, and reversion logic. Certification requires documentation of FMEA and demonstration that all catastrophic "
            "failure modes are mitigated to an acceptable level of risk."
        ),
        key_factors=[
            "Failure mode identification",
            "Effect analysis",
            "Mitigation strategies",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA CS-25.1309",
            "FAR 25.1309",
            "SAE ARP4761"
        ],
        burden_holder="System Safety Engineer",
        adversary_position="FMEA is resource-intensive and may delay development.",
        counter_arguments=[
            "Essential for safety and certification.",
            "Early FMEA reduces late design changes."
        ],
        resolution_strategy="Conduct FMEA early; update throughout development.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="A320/B777 FMEA Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Fault Tree Analysis (FTA)",
        keywords=["FTA", "Fault Tree Analysis", "Flight Control System", "Safety"],
        conclusion_template="FTA is required to demonstrate that catastrophic failure probabilities meet certification requirements.",
        reasoning_framework=(
            "FTA is a top-down analysis method used to quantify the probability of catastrophic FCS failures. "
            "Results guide redundancy and monitoring requirements. Certification requires demonstration that the probability of catastrophic failure is below "
            "10^-9 per flight hour for DAL A functions."
        ),
        key_factors=[
            "Top-down failure analysis",
            "Probability quantification",
            "Redundancy requirements",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA CS-25.1309",
            "FAR 25.1309",
            "SAE ARP4761"
        ],
        burden_holder="System Safety Engineer",
        adversary_position="FTA requires detailed system modeling and may be time-consuming.",
        counter_arguments=[
            "Essential for certification of safety-critical systems.",
            "Supports design optimization."
        ],
        resolution_strategy="Conduct FTA in parallel with design; update as system evolves.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 FTA Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Latency and Response Time",
        keywords=["Latency", "Response Time", "Flight Control System", "FBW"],
        conclusion_template="FCS must meet stringent latency and response time requirements to ensure safe and predictable handling.",
        reasoning_framework=(
            "FBW systems must process pilot inputs and sensor data with minimal latency. Certification requires demonstration that total system response time "
            "meets handling quality standards (e.g., MIL-F-8785C). Latency is minimized through high-speed processors, efficient software, and optimized data paths."
        ),
        key_factors=[
            "Processor speed",
            "Software efficiency",
            "Data path optimization",
            "Certification flight test"
        ],
        primary_authority=[
            "MIL-F-8785C",
            "EASA CS-25.671",
            "FAR 25.671"
        ],
        burden_holder="System Architect",
        adversary_position="Minimizing latency may increase hardware cost.",
        counter_arguments=[
            "Essential for handling quality and safety.",
            "Design optimization can balance cost and performance."
        ],
        resolution_strategy="Optimize architecture for low latency; validate with simulation and flight test.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320/B777 Latency Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Software Partitioning",
        keywords=["Software Partitioning", "Flight Control System", "DO-178C", "DAL"],
        conclusion_template="Software partitioning is required to isolate DAL A functions from lower-assurance software.",
        reasoning_framework=(
            "Software partitioning ensures that faults in lower-assurance software (e.g., DAL C/D) cannot propagate to safety-critical DAL A functions. "
            "Partitioning is achieved through time and space separation, enforced by RTOS or hypervisor. Certification requires demonstration of partitioning "
            "integrity per DO-178C/DO-297."
        ),
        key_factors=[
            "Time and space separation",
            "RTOS/hypervisor enforcement",
            "Certification analysis",
            "Verification testing"
        ],
        primary_authority=[
            "DO-178C",
            "DO-297",
            "EASA AMC 20-115C"
        ],
        burden_holder="Software Architect",
        adversary_position="Partitioning may increase resource usage and complexity.",
        counter_arguments=[
            "Essential for mixed-criticality systems.",
            "Design optimization can minimize impact."
        ],
        resolution_strategy="Implement robust partitioning; validate with analysis and testing.",
        entity_scope="AERO06 Flight Control Software",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A350/B787 Software Partitioning Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Configuration Management",
        keywords=["Configuration Management", "Flight Control System", "Software", "Hardware"],
        conclusion_template="Comprehensive configuration management is required for all FCS software and hardware.",
        reasoning_framework=(
            "Configuration management ensures traceability and control of all FCS software and hardware versions. "
            "Processes include version control, change tracking, and release documentation. Certification requires demonstration that only approved configurations "
            "are installed on aircraft."
        ),
        key_factors=[
            "Version control",
            "Change tracking",
            "Release documentation",
            "Certification analysis"
        ],
        primary_authority=[
            "DO-178C",
            "DO-254",
            "EASA CS-25.1309"
        ],
        burden_holder="Configuration Manager",
        adversary_position="Configuration management may increase administrative workload.",
        counter_arguments=[
            "Essential for certification and airworthiness.",
            "Automation tools can reduce workload."
        ],
        resolution_strategy="Implement automated configuration management tools; train personnel.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="A320/B777 Configuration Management Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Obsolescence Management",
        keywords=["Obsolescence Management", "Flight Control System", "LRU", "Spares"],
        conclusion_template="Obsolescence management is required to ensure long-term supportability of FCS components.",
        reasoning_framework=(
            "Obsolescence management plans identify and mitigate risks from discontinued components (e.g., LRUs, processors). "
            "Strategies include lifetime buys, alternate sourcing, and proactive redesign. Certification requires demonstration that obsolescence does not "
            "compromise safety or airworthiness."
        ),
        key_factors=[
            "Obsolescence risk identification",
            "Alternate sourcing",
            "Redesign planning",
            "Certification analysis"
        ],
        primary_authority=[
            "EASA CS-25.1529",
            "FAR 25.1529",
            "Airbus/Boeing Obsolescence Management"
        ],
        burden_holder="Program Manager",
        adversary_position="Obsolescence management increases program cost.",
        counter_arguments=[
            "Essential for long-term supportability.",
            "Early planning minimizes impact."
        ],
        resolution_strategy="Develop and maintain obsolescence management plan; review regularly.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="A320/B777 Obsolescence Management"
    ),
    DoctrineBlock(
        topic="Flight Control System Change Control",
        keywords=["Change Control", "Flight Control System", "Configuration Management"],
        conclusion_template="All FCS changes must be controlled, documented, and approved per configuration management plan.",
        reasoning_framework=(
            "Change control ensures that all modifications to FCS software or hardware are reviewed, tested, and approved before implementation. "
            "Processes include change requests, impact analysis, and certification authority notification. Certification requires demonstration of "
            "traceability and approval for all changes."
        ),
        key_factors=[
            "Change request process",
            "Impact analysis",
            "Approval and documentation",
            "Certification authority notification"
        ],
        primary_authority=[
            "DO-178C",
            "DO-254",
            "EASA CS-25.1309"
        ],
        burden_holder="Configuration Manager",
        adversary_position="Change control may slow development.",
        counter_arguments=[
            "Essential for safety and certification.",
            "Automation tools can streamline process."
        ],
        resolution_strategy="Implement automated change control tools; train personnel.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="A320/B777 Change Control Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Documentation and Training",
        keywords=["Documentation", "Training", "Flight Control System", "Certification"],
        conclusion_template="Comprehensive documentation and training are required for all FCS users and maintainers.",
        reasoning_framework=(
            "All FCS design, operation, and maintenance procedures must be documented in manuals and training materials. "
            "Certification requires demonstration that crew and maintenance personnel are trained to operate and maintain the system safely."
        ),
        key_factors=[
            "Manuals and training materials",
            "Certification documentation",
            "Training programs",
            "Crew/maintenance evaluation"
        ],
        primary_authority=[
            "EASA CS-25.1529",
            "FAR 25.1529",
            "Airbus/Boeing Training Programs"
        ],
        burden_holder="Training Manager",
        adversary_position="Training increases program cost and schedule.",
        counter_arguments=[
            "Essential for safe operation and maintenance.",
            "Standardized programs reduce long-term cost."
        ],
        resolution_strategy="Develop comprehensive documentation and training; update regularly.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Training Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Airworthiness Directives (AD) Compliance",
        keywords=["Airworthiness Directive", "AD", "Compliance", "Flight Control System"],
        conclusion_template="All applicable ADs must be tracked and complied with for continued airworthiness.",
        reasoning_framework=(
            "Airworthiness Directives (ADs) are mandatory instructions issued by authorities to address unsafe conditions. "
            "All FCS ADs must be tracked, assessed for applicability, and complied with in a timely manner. Certification requires demonstration of compliance."
        ),
        key_factors=[
            "AD tracking",
            "Applicability assessment",
            "Compliance documentation",
            "Certification authority reporting"
        ],
        primary_authority=[
            "EASA Part 21",
            "FAR Part 39",
            "Airbus/Boeing AD Compliance Procedures"
        ],
        burden_holder="Airworthiness Manager",
        adversary_position="AD compliance may require unplanned modifications.",
        counter_arguments=[
            "Essential for continued airworthiness.",
            "Proactive tracking minimizes disruption."
        ],
        resolution_strategy="Implement AD tracking system; review applicability regularly.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="All Part 25 Aircraft AD Compliance"
    ),
    DoctrineBlock(
        topic="Flight Control System Service Bulletin (SB) Implementation",
        keywords=["Service Bulletin", "SB", "Implementation", "Flight Control System"],
        conclusion_template="Relevant SBs should be assessed and implemented to improve FCS safety and reliability.",
        reasoning_framework=(
            "Service Bulletins (SBs) provide recommended or optional changes to improve safety, reliability, or maintainability. "
            "All relevant SBs should be assessed for applicability and implemented as appropriate. Documentation of SB status is required for certification."
        ),
        key_factors=[
            "SB assessment",
            "Implementation planning",
            "Documentation",
            "Certification authority notification"
        ],
        primary_authority=[
            "EASA Part 21",
            "FAR Part 43",
            "Airbus/Boeing SB Implementation Procedures"
        ],
        burden_holder="Maintenance Manager",
        adversary_position="SB implementation may increase maintenance workload.",
        counter_arguments=[
            "Improves safety and reliability.",
            "Proactive planning minimizes impact."
        ],
        resolution_strategy="Assess and implement SBs as appropriate; document status.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320/B777 SB Implementation"
    ),
    DoctrineBlock(
        topic="Flight Control System Reliability Analysis",
        keywords=["Reliability Analysis", "Flight Control System", "MTBF", "Dispatch Reliability"],
        conclusion_template="Reliability analysis is required to demonstrate FCS meets MTBF and dispatch reliability targets.",
        reasoning_framework=(
            "Reliability analysis quantifies FCS Mean Time Between Failure (MTBF) and dispatch reliability. "
            "Results inform maintenance intervals and spares planning. Certification requires demonstration that reliability targets are met or exceeded."
        ),
        key_factors=[
            "MTBF calculation",
            "Dispatch reliability analysis",
            "Maintenance interval planning",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA CS-25.1309",
            "FAR 25.1309",
            "Airbus/Boeing Reliability Reports"
        ],
        burden_holder="Reliability Engineer",
        adversary_position="Reliability analysis may require extensive operational data.",
        counter_arguments=[
            "Essential for maintenance planning and certification.",
            "Early analysis informs design improvements."
        ],
        resolution_strategy="Conduct reliability analysis throughout development and operation.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Reliability Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Dispatch Deviation Guide (DDG) Policy",
        keywords=["Dispatch Deviation Guide", "DDG", "Policy", "Flight Control System"],
        conclusion_template="DDG policy defines allowable FCS dispatch deviations and required maintenance actions.",
        reasoning_framework=(
            "The DDG specifies conditions under which the aircraft may be dispatched with inoperative FCS components, and the required maintenance actions. "
            "Policy is based on system redundancy and safety analysis. Certification requires demonstration that DDG does not compromise safety."
        ),
        key_factors=[
            "Dispatch deviation conditions",
            "Required maintenance actions",
            "Safety analysis",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA CS-25.1529",
            "FAR 25.1529",
            "Airbus/Boeing DDG Policy"
        ],
        burden_holder="Flight Operations",
        adversary_position="DDG may increase operational complexity.",
        counter_arguments=[
            "Provides operational flexibility.",
            "Safety analysis ensures risk is acceptable."
        ],
        resolution_strategy="Develop DDG policy based on safety analysis; review regularly.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320/B777 DDG Policy"
    ),
    DoctrineBlock(
        topic="Flight Control System Software Tool Qualification",
        keywords=["Software Tool Qualification", "Flight Control System", "DO-330", "Verification"],
        conclusion_template="All software tools used for FCS development and verification must be qualified per DO-330.",
        reasoning_framework=(
            "Software tools that automate or replace human verification steps must be qualified per DO-330. "
            "Qualification includes tool assessment, documentation, and verification of correct operation. Certification requires demonstration that tool output is reliable."
        ),
        key_factors=[
            "Tool assessment",
            "Qualification documentation",
            "Verification testing",
            "Certification analysis"
        ],
        primary_authority=[
            "DO-330",
            "DO-178C",
            "EASA AMC 20-115C"
        ],
        burden_holder="Software Verification Engineer",
        adversary_position="Tool qualification increases development time and cost.",
        counter_arguments=[
            "Essential for certification of automated tools.",
            "Early planning minimizes impact."
        ],
        resolution_strategy="Identify and qualify tools early in development.",
        entity_scope="AERO06 Flight Control Software",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A350/B787 Tool Qualification Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Supplier Management",
        keywords=["Supplier Management", "Flight Control System", "Quality Assurance"],
        conclusion_template="Supplier management ensures FCS components meet quality and certification requirements.",
        reasoning_framework=(
            "Supplier management includes qualification, quality audits, and ongoing oversight of FCS component suppliers. "
            "Certification requires demonstration that all supplied components meet applicable standards and are traceable."
        ),
        key_factors=[
            "Supplier qualification",
            "Quality audits",
            "Traceability",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA Part 21",
            "FAR Part 21",
            "Airbus/Boeing Supplier Management"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Supplier management increases administrative workload.",
        counter_arguments=[
            "Essential for quality and certification.",
            "Automation tools can reduce workload."
        ],
        resolution_strategy="Implement supplier management plan; conduct regular audits.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320/B777 Supplier Management Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Export Control Compliance",
        keywords=["Export Control", "Compliance", "Flight Control System", "ITAR", "EAR"],
        conclusion_template="FCS design and documentation must comply with all applicable export control regulations.",
        reasoning_framework=(
            "Export control regulations (e.g., ITAR, EAR) restrict sharing of FCS design and documentation with foreign nationals. "
            "Compliance includes classification, licensing, and access controls. Certification requires demonstration of compliance for all export-controlled items."
        ),
        key_factors=[
            "Export control classification",
            "Licensing",
            "Access controls",
            "Certification documentation"
        ],
        primary_authority=[
            "ITAR",
            "EAR",
            "EASA/FAA Export Control Guidance"
        ],
        burden_holder="Export Compliance Manager",
        adversary_position="Export control compliance increases administrative burden.",
        counter_arguments=[
            "Essential for legal compliance.",
            "Automation tools can reduce workload."
        ],
        resolution_strategy="Implement export control plan; train personnel.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="A320/B777 Export Control Compliance"
    ),
    DoctrineBlock(
        topic="Flight Control System Weight and Balance Management",
        keywords=["Weight and Balance", "Management", "Flight Control System", "Certification"],
        conclusion_template="FCS design must support aircraft weight and balance requirements throughout operational envelope.",
        reasoning_framework=(
            "FCS components must be located and designed to support aircraft weight and balance requirements. "
            "Certification requires demonstration that FCS installation does not compromise center of gravity limits or handling qualities."
        ),
        key_factors=[
            "Component location",
            "Weight tracking",
            "CG analysis",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA CS-25.23",
            "FAR 25.23",
            "Airbus/Boeing Weight and Balance Reports"
        ],
        burden_holder="Aircraft Integration Engineer",
        adversary_position="Weight and balance management may constrain FCS design.",
        counter_arguments=[
            "Essential for safe operation.",
            "Design optimization can balance constraints."
        ],
        resolution_strategy="Integrate weight and balance management into FCS design process.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Weight and Balance Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Lightning Protection",
        keywords=["Lightning Protection", "Flight Control System", "Certification", "EMC"],
        conclusion_template="FCS must be protected against lightning strikes per certification requirements.",
        reasoning_framework=(
            "Lightning protection includes shielding, bonding, and surge suppression for all FCS components. "
            "Certification requires demonstration that lightning strikes do not compromise system safety or integrity."
        ),
        key_factors=[
            "Shielding and bonding",
            "Surge suppression",
            "Certification testing",
            "Documentation"
        ],
        primary_authority=[
            "RTCA/DO-160",
            "EASA CS-25.1316",
            "FAR 25.1316"
        ],
        burden_holder="Avionics Engineer",
        adversary_position="Lightning protection may increase weight and cost.",
        counter_arguments=[
            "Essential for safety and certification.",
            "Design optimization can minimize impact."
        ],
        resolution_strategy="Implement lightning protection; validate with certification testing.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="A320/B777 Lightning Protection Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Redundancy Management",
        keywords=["Redundancy Management", "Flight Control System", "Certification"],
        conclusion_template="Redundancy management ensures continued safe operation after single failures.",
        reasoning_framework=(
            "Redundancy management includes design, monitoring, and reconfiguration logic to ensure that no single failure leads to loss of control. "
            "Certification requires demonstration that redundancy is sufficient for all critical FCS functions."
        ),
        key_factors=[
            "Redundancy design",
            "Monitoring and reconfiguration",
            "Certification analysis",
            "Failure mode testing"
        ],
        primary_authority=[
            "EASA CS-25.1309",
            "FAR 25.1309",
            "SAE ARP4761"
        ],
        burden_holder="System Architect",
        adversary_position="Redundancy increases weight and complexity.",
        counter_arguments=[
            "Essential for safety-critical systems.",
            "Design optimization can minimize impact."
        ],
        resolution_strategy="Optimize redundancy for safety and performance; validate with analysis and testing.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="A320/B777 Redundancy Certification"
    ),
    DoctrineBlock(
        topic="Flight Control System Certification Flight Test Policy",
        keywords=["Certification Flight Test", "Policy", "Flight Control System"],
        conclusion_template="Certification flight test policy defines required tests and acceptance criteria for FCS.",
        reasoning_framework=(
            "Certification flight test policy specifies required tests for handling qualities, failure modes, and system performance. "
            "Acceptance criteria are based on certification standards and operational requirements. Results are documented for authority review."
        ),
        key_factors=[
            "Test planning",
            "Acceptance criteria",
            "Documentation",
            "Authority review"
        ],
        primary_authority=[
            "EASA CS-25.1309",
            "FAR 25.1309",
            "Airbus/Boeing Flight Test Policy"
        ],
        burden_holder="Flight Test Manager",
        adversary_position="Flight test policy may increase program duration.",
        counter_arguments=[
            "Essential for certification and safety.",
            "Early planning minimizes impact."
        ],
        resolution_strategy="Develop flight test policy early; coordinate with authorities.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Certification Flight Test"
    ),
    DoctrineBlock(
        topic="Flight Control System End-of-Life (EOL) Policy",
        keywords=["End-of-Life", "EOL", "Policy", "Flight Control System"],
        conclusion_template="EOL policy defines procedures for withdrawal and disposal of FCS components.",
        reasoning_framework=(
            "EOL policy specifies procedures for withdrawal, disposal, and replacement of FCS components. "
            "Certification requires demonstration that EOL does not compromise safety, and that hazardous materials are managed per regulations."
        ),
        key_factors=[
            "Withdrawal procedures",
            "Disposal and replacement",
            "Hazardous material management",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA Part 21",
            "FAR Part 43",
            "Airbus/Boeing EOL Policy"
        ],
        burden_holder="Program Manager",
        adversary_position="EOL policy may increase program cost.",
        counter_arguments=[
            "Essential for safety and regulatory compliance.",
            "Early planning minimizes impact."
        ],
        resolution_strategy="Develop and implement EOL policy; review regularly.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="A320/B777 EOL Policy"
    ),
    DoctrineBlock(
        topic="Flight Control System Continuous Airworthiness Monitoring",
        keywords=["Continuous Airworthiness", "Monitoring", "Flight Control System"],
        conclusion_template="Continuous airworthiness monitoring ensures ongoing safety and compliance of FCS.",
        reasoning_framework=(
            "Continuous airworthiness monitoring includes operational data analysis, reliability tracking, and regular reviews of service experience. "
            "Certification requires demonstration that monitoring processes are in place and effective."
        ),
        key_factors=[
            "Operational data analysis",
            "Reliability tracking",
            "Service experience review",
            "Certification documentation"
        ],
        primary_authority=[
            "EASA Part M",
            "FAR Part 43",
            "Airbus/Boeing Airworthiness Monitoring"
        ],
        burden_holder="Airworthiness Manager",
        adversary_position="Continuous monitoring increases operational workload.",
        counter_arguments=[
            "Essential for ongoing safety and compliance.",
            "Automation tools can reduce workload."
        ],
        resolution_strategy="Implement monitoring processes; review regularly.",
        entity_scope="AERO06 Flight Control System",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="A320/B777 Airworthiness Monitoring"
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