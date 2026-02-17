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
        topic="Absolute Permissive Block (APB) - Signal Spacing",
        keywords=["APB", "signal spacing", "block length", "train separation"],
        conclusion_template="APB signal spacing must ensure safe train separation based on maximum authorized speed and braking distance.",
        reasoning_framework="""
        The APB system relies on fixed blocks with signals spaced to provide adequate stopping distance for the worst-case train scenario. Signal placement must account for train length, maximum speed, grade, and braking characteristics. The block length should be calculated to ensure that a train encountering a stop signal can safely stop before reaching an occupied block. Regulatory standards such as FRA 49 CFR Part 236 and AREMA guidelines provide minimum requirements for block lengths and signal placement. Local operational practices and historical accident data should inform adjustments to standard calculations.
        """,
        key_factors=[
            "Maximum authorized speed",
            "Train braking distance",
            "Track gradient",
            "Signal visibility",
            "Regulatory minimums"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236",
            "AREMA Communications & Signals Manual"
        ],
        burden_holder="Signal system designer",
        adversary_position="Shorter block lengths increase capacity but may compromise safety.",
        counter_arguments=[
            "Shorter blocks can be justified with advanced train control or lower speeds.",
            "Longer blocks may reduce capacity but increase safety margin."
        ],
        resolution_strategy="Apply conservative calculations, validate with simulations, and seek regulatory approval for deviations.",
        entity_scope="Mainline APB installations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA Signal System Safety Reviews 2017"
    ),
    DoctrineBlock(
        topic="Interlocking Systems - Mechanical vs. Relay Interlocking",
        keywords=["interlocking", "mechanical", "relay", "fail-safe", "route locking"],
        conclusion_template="Relay interlocking supersedes mechanical interlocking for complex junctions due to scalability and reliability.",
        reasoning_framework="""
        Mechanical interlocking, while historically significant, is limited in scalability and susceptible to wear. Relay interlocking offers electrical route locking, remote control, and easier maintenance. Both systems must enforce fail-safe principles, but relay systems provide more robust error detection and flexibility for future upgrades. Regulatory authorities require that any transition from mechanical to relay interlocking be validated for equivalent or superior safety performance.
        """,
        key_factors=[
            "Complexity of track layout",
            "Required number of routes",
            "Maintenance resources",
            "Fail-safe design features"
        ],
        primary_authority=[
            "AREMA Manual Chapter 14",
            "FRA Technical Bulletins"
        ],
        burden_holder="Railroad infrastructure manager",
        adversary_position="Mechanical systems are more robust against electrical faults.",
        counter_arguments=[
            "Relay systems have proven reliability and allow for redundancy.",
            "Mechanical systems are labor-intensive and less adaptable."
        ],
        resolution_strategy="Conduct risk assessment and cost-benefit analysis prior to conversion.",
        entity_scope="Interlocking plants at junctions and terminals",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AREMA C&S Committee Reports 2009-2018"
    ),
    DoctrineBlock(
        topic="Signal Aspects - Color Light vs. Position Light",
        keywords=["signal aspects", "color light", "position light", "visibility", "interpretation"],
        conclusion_template="Color light signals are preferred for new installations due to superior visibility and standardized interpretation.",
        reasoning_framework="""
        Color light signals use distinct colors to convey movement authority, reducing ambiguity and improving recognition under varied lighting conditions. Position light signals, while historically used in certain regions (e.g., PRR), can be misinterpreted in adverse weather or by unfamiliar crews. Modern standards prioritize color light signals for consistency and safety. Exceptions may be made for heritage lines or where position light signals have proven effective and crews are properly trained.
        """,
        key_factors=[
            "Signal visibility",
            "Crew familiarity",
            "Standardization",
            "Maintenance requirements"
        ],
        primary_authority=[
            "FRA Signal Standards",
            "AREMA Manual Chapter 7"
        ],
        burden_holder="Railroad signal engineer",
        adversary_position="Position light signals are less affected by color blindness.",
        counter_arguments=[
            "Color light signals can be supplemented with shapes or patterns.",
            "Crew training mitigates misinterpretation risks."
        ],
        resolution_strategy="Adopt color light signals except where justified by operational history and crew proficiency.",
        entity_scope="All mainline and branch line signal installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Signal System Guidance 2015"
    ),
    DoctrineBlock(
        topic="Track Circuits - DC vs. AC",
        keywords=["track circuits", "DC", "AC", "electrical interference", "track bonding"],
        conclusion_template="AC track circuits are preferred in electrified territories to mitigate DC traction current interference.",
        reasoning_framework="""
        DC track circuits are susceptible to stray currents from DC electrification systems, leading to false occupancy indications or failures. AC track circuits, particularly those using audio frequencies, are less affected by DC interference and allow for jointless operation. The choice must consider compatibility with existing infrastructure, cost, and regulatory requirements. Where DC track circuits are used, additional bonding and filtering may be required.
        """,
        key_factors=[
            "Type of electrification",
            "Existing track circuit infrastructure",
            "Cost of conversion",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "IEEE Std 1478"
        ],
        burden_holder="Signal system designer",
        adversary_position="DC track circuits are simpler and less expensive.",
        counter_arguments=[
            "Long-term reliability and safety favor AC circuits in electrified zones.",
            "Modern AC circuits support advanced diagnostics."
        ],
        resolution_strategy="Conduct site-specific interference studies and select the circuit type accordingly.",
        entity_scope="Electrified and non-electrified mainlines",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEEE Railway Signaling Standards"
    ),
    DoctrineBlock(
        topic="Positive Train Control (PTC) - I-ETMS Architecture",
        keywords=["PTC", "I-ETMS", "train control", "enforcement", "wireless communication"],
        conclusion_template="I-ETMS PTC architecture must provide real-time enforcement of movement authorities and speed restrictions.",
        reasoning_framework="""
        I-ETMS (Interoperable Electronic Train Management System) is a wireless-based PTC solution that enforces movement authorities, speed restrictions, and work zone limits. The system integrates onboard computers, wayside interface units, and back-office servers. Compliance with FRA 49 CFR Part 236 Subpart I is mandatory. The architecture must ensure secure, reliable communication, positive enforcement, and interoperability with other PTC systems. System validation includes laboratory and field testing, with ongoing monitoring for exceptions and failures.
        """,
        key_factors=[
            "System interoperability",
            "Wireless communication reliability",
            "Authority enforcement logic",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart I",
            "AAR PTC Implementation Guidelines"
        ],
        burden_holder="PTC system integrator",
        adversary_position="PTC may cause operational delays due to false enforcement.",
        counter_arguments=[
            "Rigorous testing reduces false positives.",
            "System design includes override protocols for emergencies."
        ],
        resolution_strategy="Follow FRA certification process and implement robust exception handling.",
        entity_scope="All PTC-mandated routes",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FRA PTC Certification Decisions 2018"
    ),
    DoctrineBlock(
        topic="Centralized Traffic Control (CTC) - Dispatcher Authority",
        keywords=["CTC", "dispatcher", "authority", "remote control", "route setting"],
        conclusion_template="CTC dispatchers retain sole authority for route setting and movement authorization within controlled territory.",
        reasoning_framework="""
        CTC systems centralize control of signals and switches, enabling dispatchers to set routes and authorize train movements remotely. The dispatcher’s authority is defined by railroad operating rules and must not be overridden by local personnel except in emergencies. All route changes and authorities must be logged. Fail-safe design ensures that loss of communication defaults to restrictive indications. Regulatory oversight is provided by the FRA and internal audits.
        """,
        key_factors=[
            "Dispatcher training",
            "System redundancy",
            "Logging and record-keeping",
            "Fail-safe defaults"
        ],
        primary_authority=[
            "FRA Operating Practices",
            "Railroad General Code of Operating Rules (GCOR)"
        ],
        burden_holder="Railroad operations management",
        adversary_position="Local control may be necessary for maintenance or emergencies.",
        counter_arguments=[
            "CTC systems include local control panels for authorized use.",
            "Procedures exist for safe transfer of control."
        ],
        resolution_strategy="Define clear protocols for local control and dispatcher override.",
        entity_scope="CTC-controlled mainlines and sidings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA CTC System Reviews 2016"
    ),
    DoctrineBlock(
        topic="Grade Crossing Warning Systems - Active vs. Passive Protection",
        keywords=["grade crossing", "warning system", "active protection", "passive protection", "risk assessment"],
        conclusion_template="Active protection (gates, lights, bells) is required at public crossings with significant vehicle or train traffic.",
        reasoning_framework="""
        The selection of grade crossing protection is based on risk assessment considering train speed, traffic volume, sight distance, and accident history. Active protection systems provide positive warning and are required by FRA and FHWA at crossings with high risk. Passive protection (signs, markings) may be used at low-volume, low-speed crossings. Upgrades to active protection are prioritized based on risk ranking and funding availability.
        """,
        key_factors=[
            "Train and vehicle traffic volume",
            "Accident history",
            "Sight distance",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA Grade Crossing Safety Regulations",
            "FHWA MUTCD"
        ],
        burden_holder="Railroad and highway authority",
        adversary_position="Passive protection is sufficient for low-risk crossings.",
        counter_arguments=[
            "Active systems reduce accident rates significantly.",
            "Passive-only crossings are subject to periodic review."
        ],
        resolution_strategy="Conduct regular risk assessments and prioritize upgrades.",
        entity_scope="All public and private grade crossings",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Grade Crossing Safety Reports"
    ),
    DoctrineBlock(
        topic="Fail-Safe Design Principles - Signal System Hardware",
        keywords=["fail-safe", "signal hardware", "design principles", "default to safe", "redundancy"],
        conclusion_template="Signal system hardware must default to the safest state upon failure, in accordance with fail-safe principles.",
        reasoning_framework="""
        Fail-safe design ensures that any single failure, including loss of power or component malfunction, results in the most restrictive signal indication. Hardware components such as relays, power supplies, and wiring must be selected and installed to minimize the risk of unsafe failure. Redundancy and periodic testing are required. Regulatory standards mandate documentation of fail-safe features and regular audits.
        """,
        key_factors=[
            "Component reliability",
            "Redundancy",
            "Testing frequency",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236",
            "AREMA Manual Chapter 17"
        ],
        burden_holder="Signal system engineer",
        adversary_position="Redundant systems increase cost and complexity.",
        counter_arguments=[
            "Safety is paramount; cost is secondary.",
            "Modern hardware allows efficient redundancy."
        ],
        resolution_strategy="Document all fail-safe features and conduct regular system audits.",
        entity_scope="All signal system hardware deployments",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FRA Signal System Audits 2019"
    ),
    DoctrineBlock(
        topic="APB - Approach Lighting of Signals",
        keywords=["APB", "approach lighting", "energy savings", "signal visibility"],
        conclusion_template="Approach lighting may be used in APB systems to reduce energy consumption, provided signal visibility is not compromised.",
        reasoning_framework="""
        Approach lighting extinguishes signals when no train is approaching, reducing energy use and lamp wear. The system must reliably detect approaching trains and illuminate signals in sufficient time for crew recognition. Regulatory guidance requires that approach lighting not impair safety or violate minimum visibility requirements. Periodic testing and monitoring are necessary to ensure reliability.
        """,
        key_factors=[
            "Detection reliability",
            "Signal visibility",
            "Crew reaction time",
            "Energy savings"
        ],
        primary_authority=[
            "AREMA Manual Chapter 7",
            "FRA Signal System Guidance"
        ],
        burden_holder="Signal maintainer",
        adversary_position="Approach lighting may delay signal recognition.",
        counter_arguments=[
            "Detection zones are designed for ample warning.",
            "Failures default to signals being lit."
        ],
        resolution_strategy="Test detection circuits regularly and monitor crew feedback.",
        entity_scope="APB-equipped mainlines",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Signal Lighting Practices"
    ),
    DoctrineBlock(
        topic="Interlocking - Route Locking Requirements",
        keywords=["interlocking", "route locking", "signal control", "safety"],
        conclusion_template="All interlockings must provide route locking to prevent conflicting movements.",
        reasoning_framework="""
        Route locking ensures that once a route is set and a signal cleared, no conflicting route can be established until the first route is released. This is achieved through mechanical, relay, or electronic means. Regulatory standards require route locking for all interlockings handling mainline movements. Exceptions are rare and must be justified by operational analysis and risk assessment.
        """,
        key_factors=[
            "Track layout complexity",
            "Type of interlocking",
            "Movement frequency",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 14",
            "FRA 49 CFR Part 236"
        ],
        burden_holder="Signal system designer",
        adversary_position="Route locking may reduce operational flexibility.",
        counter_arguments=[
            "Safety outweighs flexibility concerns.",
            "Modern systems allow for conditional releases."
        ],
        resolution_strategy="Document all route locking logic and review during audits.",
        entity_scope="All interlockings",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA Interlocking Reviews"
    ),
    DoctrineBlock(
        topic="Signal Aspects - Searchlight Signal Maintenance",
        keywords=["signal aspects", "searchlight", "maintenance", "lamp failure", "indication"],
        conclusion_template="Searchlight signals require frequent maintenance due to mechanical complexity and single-lamp dependency.",
        reasoning_framework="""
        Searchlight signals use a single lamp and moving color filter mechanism, making them vulnerable to mechanical and electrical failures. A lamp failure extinguishes all aspects, potentially causing operational delays. Regular inspection, lubrication, and lamp replacement are necessary. Many railroads are phasing out searchlight signals in favor of LED color light signals for improved reliability.
        """,
        key_factors=[
            "Lamp reliability",
            "Mechanical wear",
            "Spare parts availability",
            "Signal replacement programs"
        ],
        primary_authority=[
            "AREMA Manual Chapter 7",
            "Railroad Maintenance Bulletins"
        ],
        burden_holder="Signal maintainer",
        adversary_position="Searchlight signals are cost-effective and familiar.",
        counter_arguments=[
            "Modern alternatives offer lower lifecycle costs.",
            "LED signals reduce maintenance intervals."
        ],
        resolution_strategy="Prioritize replacement of searchlight signals in capital programs.",
        entity_scope="All lines with searchlight signals",
        confidence=0.93,
        confidence_zone="Medium-High",
        controlling_precedent="Railroad Signal Replacement Initiatives"
    ),
    DoctrineBlock(
        topic="Track Circuits - Audio Frequency Jointless Circuits",
        keywords=["track circuits", "audio frequency", "jointless", "insulated joints", "maintenance"],
        conclusion_template="Audio frequency jointless track circuits are preferred for high-speed lines to reduce maintenance and improve reliability.",
        reasoning_framework="""
        Jointless track circuits eliminate the need for insulated rail joints, reducing maintenance and improving ride quality. Audio frequency circuits can be tuned to avoid interference and support longer block lengths. They are compatible with continuous welded rail and high-speed operations. Regulatory standards require periodic calibration and monitoring for signal integrity.
        """,
        key_factors=[
            "Track structure",
            "Train speed",
            "Signal integrity",
            "Maintenance practices"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "IEEE Std 1478"
        ],
        burden_holder="Signal system designer",
        adversary_position="Audio frequency circuits are more expensive to install.",
        counter_arguments=[
            "Lower maintenance costs offset initial investment.",
            "Improved reliability enhances safety."
        ],
        resolution_strategy="Evaluate lifecycle costs and operational benefits.",
        entity_scope="High-speed and mainline tracks",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="High-Speed Rail Signal Standards"
    ),
    DoctrineBlock(
        topic="PTC - Data Integrity and Cybersecurity",
        keywords=["PTC", "data integrity", "cybersecurity", "encryption", "system protection"],
        conclusion_template="PTC systems must implement robust cybersecurity measures to ensure data integrity and prevent unauthorized access.",
        reasoning_framework="""
        PTC relies on wireless data transmission between trains, wayside devices, and back-office servers. This exposes the system to potential cyber threats. Regulatory requirements mandate encryption, authentication, and intrusion detection. Regular vulnerability assessments and software updates are essential. The system must be designed to fail safe in the event of detected tampering or data corruption.
        """,
        key_factors=[
            "Encryption standards",
            "Authentication protocols",
            "Intrusion detection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart I",
            "NIST Cybersecurity Framework"
        ],
        burden_holder="PTC system operator",
        adversary_position="Cybersecurity measures may impact system performance.",
        counter_arguments=[
            "Security is essential for safety-critical systems.",
            "Modern hardware supports efficient encryption."
        ],
        resolution_strategy="Integrate cybersecurity from system design through operation.",
        entity_scope="All PTC deployments",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA PTC Cybersecurity Guidance"
    ),
    DoctrineBlock(
        topic="CTC - Loss of Communication Protocols",
        keywords=["CTC", "communication loss", "fail-safe", "dispatcher", "train operation"],
        conclusion_template="CTC systems must default to restrictive indications upon loss of communication with the control center.",
        reasoning_framework="""
        Reliable communication is critical for CTC operation. In the event of communication loss, signals and switches must revert to the most restrictive state to prevent unauthorized movements. Local control may be authorized under strict protocols. All incidents of communication loss must be logged and investigated. Regulatory oversight ensures compliance with fail-safe requirements.
        """,
        key_factors=[
            "Communication reliability",
            "Fail-safe defaults",
            "Local control protocols",
            "Incident logging"
        ],
        primary_authority=[
            "FRA CTC Regulations",
            "Railroad Operating Rules"
        ],
        burden_holder="Signal system operator",
        adversary_position="Restrictive defaults may cause operational delays.",
        counter_arguments=[
            "Safety takes precedence over efficiency.",
            "Procedures exist for controlled restoration."
        ],
        resolution_strategy="Regularly test communication failover and train personnel in loss protocols.",
        entity_scope="All CTC-controlled territories",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA CTC System Reviews"
    ),
    DoctrineBlock(
        topic="Grade Crossing - Event Data Recorders",
        keywords=["grade crossing", "event recorder", "data logging", "accident investigation"],
        conclusion_template="Event data recorders are required at active grade crossings to support accident investigation and system monitoring.",
        reasoning_framework="""
        Event data recorders capture activation times, warning device status, and train passage data. This information is critical for post-incident analysis and regulatory compliance. FRA regulations specify minimum data retention periods and accessibility requirements. Data must be protected from tampering and made available to authorized investigators.
        """,
        key_factors=[
            "Data retention",
            "Device reliability",
            "Regulatory requirements",
            "Incident response"
        ],
        primary_authority=[
            "FRA Grade Crossing Safety Regulations",
            "NTSB Recommendations"
        ],
        burden_holder="Railroad crossing maintenance manager",
        adversary_position="Recorders increase maintenance and data management costs.",
        counter_arguments=[
            "Accurate data is essential for safety improvement.",
            "Modern recorders are highly reliable."
        ],
        resolution_strategy="Integrate recorders into all new and upgraded crossing systems.",
        entity_scope="All active grade crossings",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NTSB Accident Reports"
    ),
    DoctrineBlock(
        topic="Fail-Safe - Software Validation in Electronic Interlockings",
        keywords=["fail-safe", "software validation", "electronic interlocking", "testing"],
        conclusion_template="All software controlling safety-critical functions in electronic interlockings must undergo rigorous validation and verification.",
        reasoning_framework="""
        Electronic interlockings rely on software logic for route locking, signal control, and safety enforcement. Software errors can have catastrophic consequences. Regulatory standards require formal validation and verification processes, including simulation, field testing, and independent review. All software changes must be documented, tested, and approved prior to deployment.
        """,
        key_factors=[
            "Software quality assurance",
            "Testing protocols",
            "Change management",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart H",
            "IEEE Std 1483"
        ],
        burden_holder="Signal system software engineer",
        adversary_position="Extensive validation increases project timelines.",
        counter_arguments=[
            "Safety-critical software demands rigorous testing.",
            "Automated tools can streamline validation."
        ],
        resolution_strategy="Adopt industry-standard software lifecycle management.",
        entity_scope="All electronic interlockings",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA Software Safety Reviews"
    ),
    DoctrineBlock(
        topic="APB - Permissive Signal Operation",
        keywords=["APB", "permissive signal", "train following", "restricted speed"],
        conclusion_template="Permissive signals in APB systems allow train following under restricted speed, with strict adherence to operating rules.",
        reasoning_framework="""
        Permissive signals display a restricting aspect when the block ahead is occupied, allowing a following train to proceed at restricted speed. Operating rules require the crew to be prepared to stop short of any obstruction. Signal system design must ensure clear indication of permissive status and prevent misinterpretation. Regulatory oversight includes periodic review of train handling incidents.
        """,
        key_factors=[
            "Signal aspect clarity",
            "Crew training",
            "Operating rule enforcement",
            "Incident reporting"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236",
            "Railroad Operating Rules"
        ],
        burden_holder="Train crew and dispatcher",
        adversary_position="Permissive operation increases risk of rear-end collisions.",
        counter_arguments=[
            "Restricted speed rules mitigate risk.",
            "Permissive operation increases line capacity."
        ],
        resolution_strategy="Emphasize crew training and monitor compliance.",
        entity_scope="APB-equipped lines",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA APB System Reviews"
    ),
    DoctrineBlock(
        topic="Interlocking - Approach Locking",
        keywords=["interlocking", "approach locking", "signal control", "train approach"],
        conclusion_template="Approach locking must be provided at interlockings to prevent unsafe route changes as a train approaches.",
        reasoning_framework="""
        Approach locking prevents a cleared route from being changed once a train is detected approaching the interlocking. This is achieved by track circuit occupancy or timer logic. The locking is released after the train passes or after a defined timeout if the train stops short. Regulatory standards require approach locking for all mainline interlockings.
        """,
        key_factors=[
            "Detection reliability",
            "Locking release logic",
            "Signal system design",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 14",
            "FRA 49 CFR Part 236"
        ],
        burden_holder="Signal system designer",
        adversary_position="Approach locking may cause unnecessary delays.",
        counter_arguments=[
            "Timeouts allow for operational flexibility.",
            "Safety is prioritized over efficiency."
        ],
        resolution_strategy="Optimize locking logic and review incident data.",
        entity_scope="All interlockings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Interlocking Safety Reviews"
    ),
    DoctrineBlock(
        topic="Signal Aspects - Lunar Indication Usage",
        keywords=["signal aspects", "lunar indication", "restricting aspect", "crew interpretation"],
        conclusion_template="Lunar indications are reserved for restricting aspects and must not be used for proceed indications.",
        reasoning_framework="""
        The lunar (white) aspect is used to indicate restricted movement authority, requiring the train to proceed at restricted speed and be prepared to stop. Using lunar for proceed aspects risks misinterpretation, especially at night. Regulatory and industry standards specify color and aspect usage to prevent confusion.
        """,
        key_factors=[
            "Aspect clarity",
            "Crew training",
            "Standardization",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 7",
            "Railroad Signal Standards"
        ],
        burden_holder="Signal system designer",
        adversary_position="Lunar is more visible in certain conditions.",
        counter_arguments=[
            "Standardization prevents misinterpretation.",
            "Alternative colors are available for proceed aspects."
        ],
        resolution_strategy="Audit signal aspects for compliance and retrain crews as needed.",
        entity_scope="All signal installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Signal Aspect Guidance"
    ),
    DoctrineBlock(
        topic="Track Circuits - Broken Rail Detection",
        keywords=["track circuits", "broken rail", "detection", "signal integrity"],
        conclusion_template="Track circuits must reliably detect broken rails and transmit occupancy to the signal system.",
        reasoning_framework="""
        Track circuits are the primary means of detecting broken rails, which disrupt the electrical circuit and cause the signal to display stop. Regular testing and monitoring are required to ensure detection reliability. Advanced systems may use additional sensors or continuous monitoring for high-risk locations. Regulatory standards mandate prompt response to track circuit failures.
        """,
        key_factors=[
            "Detection reliability",
            "Testing frequency",
            "Response protocols",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "FRA Track Safety Standards"
        ],
        burden_holder="Track and signal maintenance personnel",
        adversary_position="Track circuits may fail to detect certain types of breaks.",
        counter_arguments=[
            "Supplement with visual inspections and advanced sensors.",
            "Prompt repair protocols mitigate risk."
        ],
        resolution_strategy="Integrate multiple detection methods where feasible.",
        entity_scope="All signaled tracks",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Track Circuit Safety Reports"
    ),
    DoctrineBlock(
        topic="PTC - Temporary Speed Restriction Enforcement",
        keywords=["PTC", "temporary speed restriction", "enforcement", "work zones"],
        conclusion_template="PTC systems must enforce temporary speed restrictions with real-time updates to onboard equipment.",
        reasoning_framework="""
        Temporary speed restrictions (TSRs) are critical for work zone safety and must be communicated to PTC-equipped trains in real time. The system must allow for rapid input and distribution of TSRs, with onboard enforcement logic to prevent overspeed. Regulatory standards require logging and auditing of all TSR enforcement actions.
        """,
        key_factors=[
            "Communication latency",
            "Onboard enforcement logic",
            "Work zone management",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart I",
            "AAR PTC Implementation Guidelines"
        ],
        burden_holder="PTC system operator",
        adversary_position="Frequent TSR updates may cause operational complexity.",
        counter_arguments=[
            "Automated tools streamline TSR management.",
            "Safety benefits outweigh complexity."
        ],
        resolution_strategy="Integrate TSR management into dispatcher workflows.",
        entity_scope="All PTC-equipped lines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA PTC Enforcement Reviews"
    ),
    DoctrineBlock(
        topic="CTC - Switch Position Indication",
        keywords=["CTC", "switch position", "indication", "dispatcher", "remote monitoring"],
        conclusion_template="CTC systems must provide positive indication of all controlled switch positions to the dispatcher.",
        reasoning_framework="""
        Dispatchers rely on accurate, real-time indication of switch positions to safely route trains. Switch indication circuits must be fail-safe, with loss of indication defaulting to restrictive signal aspects. Periodic testing and maintenance are required to ensure reliability. Regulatory standards specify minimum requirements for switch indication systems.
        """,
        key_factors=[
            "Indication reliability",
            "Fail-safe defaults",
            "Testing frequency",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA CTC Regulations",
            "AREMA Manual Chapter 14"
        ],
        burden_holder="Signal maintainer",
        adversary_position="Indication failures may cause unnecessary delays.",
        counter_arguments=[
            "Delays are preferable to unsafe movements.",
            "Modern systems have high reliability."
        ],
        resolution_strategy="Monitor indication reliability and prioritize repairs.",
        entity_scope="All CTC-controlled switches",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA CTC System Reviews"
    ),
    DoctrineBlock(
        topic="Grade Crossing - Preemption for Highway Traffic Signals",
        keywords=["grade crossing", "preemption", "highway traffic signal", "coordination"],
        conclusion_template="Grade crossing warning systems must be coordinated with adjacent highway traffic signals to provide preemption for train movements.",
        reasoning_framework="""
        Preemption ensures that highway traffic signals clear vehicles from the crossing before train arrival. Coordination requires precise timing and communication between railroad and highway agencies. Regulatory standards specify minimum warning times and interconnection requirements. Regular testing and joint reviews are necessary to maintain effective preemption.
        """,
        key_factors=[
            "Signal timing",
            "Interagency coordination",
            "Warning time calculation",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FHWA MUTCD",
            "FRA Grade Crossing Safety Regulations"
        ],
        burden_holder="Railroad and highway signal engineers",
        adversary_position="Preemption may disrupt highway traffic flow.",
        counter_arguments=[
            "Safety at the crossing is the highest priority.",
            "Signal timing can be optimized to minimize disruption."
        ],
        resolution_strategy="Conduct joint timing studies and update preemption plans regularly.",
        entity_scope="All grade crossings with adjacent traffic signals",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FHWA Railroad-Highway Crossing Handbook"
    ),
    DoctrineBlock(
        topic="Fail-Safe - Relay Interlocking Maintenance",
        keywords=["fail-safe", "relay interlocking", "maintenance", "testing", "component failure"],
        conclusion_template="Relay interlockings require periodic testing and preventive maintenance to ensure fail-safe operation.",
        reasoning_framework="""
        Relay interlockings depend on electromechanical relays, which are subject to wear and environmental degradation. Preventive maintenance includes cleaning, adjustment, and replacement of worn components. Testing protocols verify correct operation of all locking and indication circuits. Regulatory standards require documentation of maintenance activities and periodic audits.
        """,
        key_factors=[
            "Relay reliability",
            "Testing frequency",
            "Environmental controls",
            "Documentation"
        ],
        primary_authority=[
            "AREMA Manual Chapter 14",
            "FRA 49 CFR Part 236"
        ],
        burden_holder="Signal maintenance supervisor",
        adversary_position="Frequent maintenance increases labor costs.",
        counter_arguments=[
            "Preventive maintenance reduces risk of failure.",
            "Automated monitoring can reduce manual effort."
        ],
        resolution_strategy="Implement maintenance management systems and track performance metrics.",
        entity_scope="All relay interlockings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Interlocking Maintenance Reviews"
    ),
    DoctrineBlock(
        topic="APB - Block Occupancy Detection",
        keywords=["APB", "block occupancy", "detection", "track circuit"],
        conclusion_template="APB systems must provide reliable block occupancy detection using track circuits or equivalent technology.",
        reasoning_framework="""
        Reliable detection of train presence in each block is essential for APB safety. Track circuits are the standard method, but axle counters or other technologies may be used where justified. Detection failures must default to restrictive signal aspects. Regular testing and incident analysis are required to maintain system integrity.
        """,
        key_factors=[
            "Detection reliability",
            "Testing protocols",
            "Technology selection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "FRA 49 CFR Part 236"
        ],
        burden_holder="Signal system operator",
        adversary_position="Alternative technologies may be less proven.",
        counter_arguments=[
            "Redundant detection methods can be used.",
            "Technology selection should be site-specific."
        ],
        resolution_strategy="Monitor detection reliability and update technology as needed.",
        entity_scope="All APB-equipped lines",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA APB System Reviews"
    ),
    DoctrineBlock(
        topic="Interlocking - Detector Integration",
        keywords=["interlocking", "detector", "hot box", "dragging equipment", "integration"],
        conclusion_template="Interlockings must integrate wayside detectors to prevent unsafe train movements.",
        reasoning_framework="""
        Wayside detectors (hot box, dragging equipment, etc.) provide critical safety data. Interlocking logic must prevent signal clearance if a defect is detected. Integration includes real-time data transmission and alarm protocols. Regulatory standards require documentation of detector integration and periodic testing.
        """,
        key_factors=[
            "Detector reliability",
            "Data integration",
            "Alarm protocols",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 14",
            "FRA Safety Advisories"
        ],
        burden_holder="Signal system integrator",
        adversary_position="Integration increases system complexity.",
        counter_arguments=[
            "Safety benefits justify complexity.",
            "Standard interfaces simplify integration."
        ],
        resolution_strategy="Standardize integration protocols and test regularly.",
        entity_scope="All interlockings with detectors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Detector Integration Guidance"
    ),
    DoctrineBlock(
        topic="Signal Aspects - LED Signal Conversion",
        keywords=["signal aspects", "LED", "conversion", "energy efficiency", "maintenance"],
        conclusion_template="Conversion to LED signal aspects is recommended for improved reliability and reduced maintenance.",
        reasoning_framework="""
        LED signals offer longer life, lower energy consumption, and improved visibility compared to incandescent lamps. Conversion programs should prioritize high-traffic and high-risk locations. Regulatory standards require that LED aspects meet brightness and color requirements. Maintenance protocols must be updated for new technology.
        """,
        key_factors=[
            "Signal reliability",
            "Energy efficiency",
            "Conversion cost",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 7",
            "FRA Signal System Guidance"
        ],
        burden_holder="Signal system manager",
        adversary_position="Conversion costs may be prohibitive.",
        counter_arguments=[
            "Lifecycle savings offset initial investment.",
            "LEDs reduce emergency maintenance."
        ],
        resolution_strategy="Phase conversion based on risk and cost-benefit analysis.",
        entity_scope="All signal installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Railroad LED Conversion Programs"
    ),
    DoctrineBlock(
        topic="Track Circuits - Ballast Resistance Management",
        keywords=["track circuits", "ballast resistance", "track maintenance", "signal reliability"],
        conclusion_template="Ballast resistance must be monitored and maintained to ensure reliable track circuit operation.",
        reasoning_framework="""
        Low ballast resistance, often caused by wet or contaminated ballast, can lead to false occupancy indications or signal failures. Regular measurement and maintenance of ballast conditions are required. Remedial actions include cleaning, drainage improvement, and ballast renewal. Regulatory standards specify minimum resistance values for safe operation.
        """,
        key_factors=[
            "Ballast condition",
            "Track drainage",
            "Measurement protocols",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "FRA Track Safety Standards"
        ],
        burden_holder="Track maintenance supervisor",
        adversary_position="Ballast maintenance is costly and labor-intensive.",
        counter_arguments=[
            "Reliable signals are essential for safety.",
            "Preventive maintenance reduces long-term costs."
        ],
        resolution_strategy="Integrate ballast monitoring into track maintenance programs.",
        entity_scope="All signaled tracks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Track Circuit Reliability Reports"
    ),
    DoctrineBlock(
        topic="PTC - Interoperability with Legacy Signal Systems",
        keywords=["PTC", "interoperability", "legacy signal system", "integration"],
        conclusion_template="PTC systems must be interoperable with existing legacy signal systems to ensure seamless operation.",
        reasoning_framework="""
        Many railroads operate a mix of legacy and PTC-equipped lines. Interoperability requires consistent movement authority logic, data exchange, and fail-safe integration. Regulatory standards require demonstration of interoperability prior to system certification. Ongoing monitoring and testing are required as systems evolve.
        """,
        key_factors=[
            "System compatibility",
            "Data exchange protocols",
            "Testing and validation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart I",
            "AAR PTC Interoperability Guidelines"
        ],
        burden_holder="PTC system integrator",
        adversary_position="Integration increases project complexity.",
        counter_arguments=[
            "Standard interfaces facilitate integration.",
            "Interoperability is required for safe operations."
        ],
        resolution_strategy="Develop and test interface specifications prior to deployment.",
        entity_scope="All PTC-equipped and legacy lines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA PTC Interoperability Reviews"
    ),
    DoctrineBlock(
        topic="CTC - Dispatcher Workload Management",
        keywords=["CTC", "dispatcher", "workload", "human factors", "automation"],
        conclusion_template="CTC system design must account for dispatcher workload to prevent errors and ensure safe operations.",
        reasoning_framework="""
        Dispatcher workload is influenced by territory size, traffic density, and system complexity. Excessive workload increases risk of error. Automation of routine tasks, clear user interfaces, and workload monitoring are recommended. Regulatory standards require periodic review of dispatcher workload and system performance.
        """,
        key_factors=[
            "Territory size",
            "Traffic density",
            "System automation",
            "Human factors analysis"
        ],
        primary_authority=[
            "FRA Human Factors Guidance",
            "Railroad Operating Practices"
        ],
        burden_holder="Railroad operations management",
        adversary_position="Automation may reduce dispatcher situational awareness.",
        counter_arguments=[
            "Automation is limited to routine, low-risk tasks.",
            "Training and monitoring mitigate risks."
        ],
        resolution_strategy="Conduct human factors studies and adjust system design as needed.",
        entity_scope="All CTC-controlled territories",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Dispatcher Workload Studies"
    ),
    DoctrineBlock(
        topic="Grade Crossing - Quiet Zone Implementation",
        keywords=["grade crossing", "quiet zone", "horn rule", "supplemental safety measures"],
        conclusion_template="Quiet zones may be established at grade crossings if supplemental safety measures meet or exceed federal requirements.",
        reasoning_framework="""
        Quiet zones allow for suspension of routine train horn sounding at crossings, provided risk is mitigated by supplemental safety measures (SSMs) such as four-quadrant gates or medians. FRA regulations specify risk thresholds and required SSMs. Community requests must be evaluated against safety impact and compliance with federal rules.
        """,
        key_factors=[
            "Risk assessment",
            "Supplemental safety measures",
            "Community input",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA Quiet Zone Rule (49 CFR Part 222)",
            "FHWA MUTCD"
        ],
        burden_holder="Local government and railroad",
        adversary_position="Quiet zones may increase crossing accident risk.",
        counter_arguments=[
            "SSMs mitigate increased risk.",
            "Periodic reviews ensure ongoing compliance."
        ],
        resolution_strategy="Conduct risk analysis and implement SSMs as required.",
        entity_scope="All public grade crossings",
        confidence=0.93,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Quiet Zone Approvals"
    ),
    DoctrineBlock(
        topic="Fail-Safe - Power Supply Redundancy",
        keywords=["fail-safe", "power supply", "redundancy", "signal system"],
        conclusion_template="Signal systems must have redundant power supplies to maintain operation during outages.",
        reasoning_framework="""
        Redundant power supplies, including batteries and backup generators, ensure continuous operation of signals and interlockings during utility outages. Regulatory standards specify minimum backup durations and testing intervals. Power supply failures must default to restrictive signal aspects. Maintenance protocols include regular battery testing and generator servicing.
        """,
        key_factors=[
            "Backup duration",
            "Testing frequency",
            "Automatic switchover",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 17",
            "FRA 49 CFR Part 236"
        ],
        burden_holder="Signal maintenance supervisor",
        adversary_position="Redundant systems increase installation and maintenance costs.",
        counter_arguments=[
            "Power reliability is essential for safety.",
            "Modern systems automate switchover and monitoring."
        ],
        resolution_strategy="Document power supply configuration and test regularly.",
        entity_scope="All signal system installations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA Signal Power Supply Reviews"
    ),
    DoctrineBlock(
        topic="APB - Reverse Running Protection",
        keywords=["APB", "reverse running", "signal protection", "wrong direction"],
        conclusion_template="APB systems must provide protection against unauthorized reverse running through signal logic and detection.",
        reasoning_framework="""
        APB systems are designed for bi-directional operation but must prevent unauthorized reverse movements. Signal logic includes directional locking and detection circuits. Unauthorized reverse running must result in restrictive signal aspects and alarm the dispatcher. Regulatory standards require documentation of reverse running protection.
        """,
        key_factors=[
            "Directional locking",
            "Detection circuits",
            "Alarm protocols",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "FRA APB System Guidance"
        ],
        burden_holder="Signal system designer",
        adversary_position="Reverse running is rarely needed and adds complexity.",
        counter_arguments=[
            "Bi-directional operation increases flexibility.",
            "Protection is required for safety."
        ],
        resolution_strategy="Test reverse running logic and document all procedures.",
        entity_scope="All APB-equipped lines",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA APB Safety Reviews"
    ),
    DoctrineBlock(
        topic="Interlocking - Time Locking",
        keywords=["interlocking", "time locking", "signal control", "safety"],
        conclusion_template="Time locking must be provided at interlockings to prevent premature route release after a signal is cleared.",
        reasoning_framework="""
        Time locking prevents a route from being released immediately after a signal is cleared, ensuring that a train has sufficient time to enter the interlocking. The locking period is based on train speed and interlocking length. Regulatory standards specify minimum time locking intervals. The system must allow for manual override in emergencies.
        """,
        key_factors=[
            "Train speed",
            "Interlocking length",
            "Locking interval",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 14",
            "FRA 49 CFR Part 236"
        ],
        burden_holder="Signal system designer",
        adversary_position="Time locking may delay operations.",
        counter_arguments=[
            "Intervals are optimized for efficiency.",
            "Safety is prioritized."
        ],
        resolution_strategy="Review time locking intervals during system audits.",
        entity_scope="All interlockings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Interlocking Safety Reviews"
    ),
    DoctrineBlock(
        topic="Signal Aspects - Marker Light Usage",
        keywords=["signal aspects", "marker light", "indication", "crew interpretation"],
        conclusion_template="Marker lights must be used in accordance with standard aspect charts and must not conflict with primary signal indications.",
        reasoning_framework="""
        Marker lights provide additional information, such as route or speed, but must not cause confusion with primary aspects. Regulatory standards specify marker light color, placement, and usage. Crew training is essential to ensure correct interpretation. Periodic audits verify compliance.
        """,
        key_factors=[
            "Aspect clarity",
            "Standardization",
            "Crew training",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 7",
            "Railroad Signal Standards"
        ],
        burden_holder="Signal system designer",
        adversary_position="Marker lights may be misinterpreted by unfamiliar crews.",
        counter_arguments=[
            "Training and standardization mitigate risk.",
            "Marker lights enhance operational flexibility."
        ],
        resolution_strategy="Audit marker light usage and update training materials.",
        entity_scope="All signal installations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Signal Aspect Guidance"
    ),
    DoctrineBlock(
        topic="Track Circuits - Lightning Protection",
        keywords=["track circuits", "lightning protection", "surge suppression", "signal reliability"],
        conclusion_template="Track circuits must be protected against lightning-induced surges to prevent failures and false indications.",
        reasoning_framework="""
        Lightning strikes can induce surges in track circuits, causing component damage or false occupancy indications. Surge protection devices and proper grounding are required. Regular inspection and testing of protection systems are necessary. Regulatory standards specify minimum protection requirements.
        """,
        key_factors=[
            "Surge protection devices",
            "Grounding",
            "Inspection protocols",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "IEEE Std 1478"
        ],
        burden_holder="Signal maintenance supervisor",
        adversary_position="Protection devices increase installation cost.",
        counter_arguments=[
            "Prevents costly failures and service interruptions.",
            "Protection is standard practice."
        ],
        resolution_strategy="Integrate surge protection into all new and upgraded installations.",
        entity_scope="All signaled tracks",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Track Circuit Reliability Reports"
    ),
    DoctrineBlock(
        topic="PTC - Crew Training and Qualification",
        keywords=["PTC", "crew training", "qualification", "system operation"],
        conclusion_template="Train crews must be thoroughly trained and qualified in PTC system operation and troubleshooting.",
        reasoning_framework="""
        Effective PTC operation depends on crew understanding of system functions, indications, and response protocols. Training programs must cover normal and abnormal operations, including system failures and overrides. Regulatory standards specify minimum training content and periodic requalification. Records of crew qualification must be maintained.
        """,
        key_factors=[
            "Training content",
            "Qualification records",
            "Periodic requalification",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart I",
            "AAR PTC Training Guidelines"
        ],
        burden_holder="Railroad training department",
        adversary_position="Extensive training increases crew time off duty.",
        counter_arguments=[
            "Qualified crews reduce risk of incidents.",
            "Training can be integrated into regular schedules."
        ],
        resolution_strategy="Maintain comprehensive training and requalification programs.",
        entity_scope="All PTC-equipped lines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA PTC Training Audits"
    ),
    DoctrineBlock(
        topic="CTC - System Redundancy and Backup",
        keywords=["CTC", "redundancy", "backup", "system reliability"],
        conclusion_template="CTC systems must include redundant communication and control paths to ensure continuous operation.",
        reasoning_framework="""
        Redundant systems prevent single points of failure from disrupting CTC operation. Backup communication links, servers, and power supplies are required. Regulatory standards specify minimum redundancy levels and testing intervals. Incident response protocols must be documented and rehearsed.
        """,
        key_factors=[
            "Redundancy level",
            "Testing frequency",
            "Incident response",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA CTC Regulations",
            "AREMA Manual Chapter 14"
        ],
        burden_holder="Signal system operator",
        adversary_position="Redundancy increases system cost and complexity.",
        counter_arguments=[
            "Redundancy is essential for safety-critical systems.",
            "Modern technology reduces incremental cost."
        ],
        resolution_strategy="Document redundancy design and test regularly.",
        entity_scope="All CTC-controlled territories",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA CTC System Reviews"
    ),
    DoctrineBlock(
        topic="Grade Crossing - Remote Monitoring",
        keywords=["grade crossing", "remote monitoring", "system status", "fault detection"],
        conclusion_template="Remote monitoring of grade crossing warning systems is required for timely fault detection and response.",
        reasoning_framework="""
        Remote monitoring systems transmit status and fault data to maintenance personnel, enabling rapid response to failures. Regulatory standards require minimum monitoring capabilities for new installations. Data must be logged and reviewed for trends. Integration with event recorders enhances incident analysis.
        """,
        key_factors=[
            "Monitoring reliability",
            "Data transmission",
            "Incident response",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA Grade Crossing Safety Regulations",
            "AREMA Manual Chapter 17"
        ],
        burden_holder="Railroad maintenance manager",
        adversary_position="Remote monitoring adds to system cost.",
        counter_arguments=[
            "Reduces response time and improves safety.",
            "Modern systems are cost-effective."
        ],
        resolution_strategy="Integrate remote monitoring into all new and upgraded installations.",
        entity_scope="All active grade crossings",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Grade Crossing Monitoring Guidance"
    ),
    DoctrineBlock(
        topic="Fail-Safe - Human Factors in System Design",
        keywords=["fail-safe", "human factors", "system design", "error prevention"],
        conclusion_template="Signal and control system design must account for human factors to minimize risk of operator error.",
        reasoning_framework="""
        Human factors engineering addresses interface design, workload, and error prevention. Clear displays, logical control layouts, and confirmation prompts reduce risk of operator mistakes. Regulatory standards require human factors review for new systems. Incident data should inform ongoing design improvements.
        """,
        key_factors=[
            "Interface clarity",
            "Workload management",
            "Error prevention features",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA Human Factors Guidance",
            "AREMA Manual Chapter 14"
        ],
        burden_holder="System designer",
        adversary_position="Human factors reviews increase project timelines.",
        counter_arguments=[
            "Prevents costly incidents and improves safety.",
            "Lessons learned inform future designs."
        ],
        resolution_strategy="Conduct human factors analysis for all new systems.",
        entity_scope="All signal and control systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Human Factors Reviews"
    ),
    DoctrineBlock(
        topic="APB - Signal Aspect Progression",
        keywords=["APB", "signal aspect", "progression", "train movement"],
        conclusion_template="APB signal aspect progression must provide clear and timely indication of movement authority to train crews.",
        reasoning_framework="""
        Signal aspect progression is designed to provide advance warning of upcoming restrictions, allowing crews to adjust speed safely. Aspects must be visible at required distances and change in a predictable sequence. Regulatory standards specify minimum sighting distances and aspect logic. Periodic review of incident data informs adjustments to progression logic.
        """,
        key_factors=[
            "Aspect visibility",
            "Sequence logic",
            "Crew training",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 7",
            "FRA Signal System Guidance"
        ],
        burden_holder="Signal system designer",
        adversary_position="Complex progression logic may confuse crews.",
        counter_arguments=[
            "Standardization and training mitigate confusion.",
            "Progression improves safety and efficiency."
        ],
        resolution_strategy="Audit aspect progression and update as needed.",
        entity_scope="APB-equipped lines",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA APB System Reviews"
    ),
    DoctrineBlock(
        topic="Interlocking - Emergency Release Procedures",
        keywords=["interlocking", "emergency release", "manual override", "safety"],
        conclusion_template="All interlockings must have documented emergency release procedures for manual override in case of system failure.",
        reasoning_framework="""
        Emergency release procedures allow authorized personnel to manually release route locking in the event of system failure. Procedures must be documented, accessible, and regularly reviewed. Regulatory standards specify authorization, logging, and post-release inspection requirements. Training is required for all personnel authorized to perform emergency releases.
        """,
        key_factors=[
            "Procedure documentation",
            "Authorization protocols",
            "Training",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 14",
            "FRA 49 CFR Part 236"
        ],
        burden_holder="Railroad operations management",
        adversary_position="Manual releases may be misused or performed incorrectly.",
        counter_arguments=[
            "Training and logging mitigate misuse.",
            "Procedures are only used in emergencies."
        ],
        resolution_strategy="Review and drill emergency procedures regularly.",
        entity_scope="All interlockings",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Interlocking Safety Reviews"
    ),
    DoctrineBlock(
        topic="Signal Aspects - Approach Medium Indication",
        keywords=["signal aspects", "approach medium", "speed control", "crew response"],
        conclusion_template="Approach Medium indication must be used to warn crews of an upcoming diverging or restricted route, allowing safe speed reduction.",
        reasoning_framework="""
        Approach Medium (typically yellow over green) provides advance warning of a diverging or restricted route ahead. Crews must reduce speed as specified in operating rules. Signal placement and visibility must support timely recognition and response. Regulatory standards specify aspect usage and placement.
        """,
        key_factors=[
            "Aspect clarity",
            "Placement",
            "Crew training",
            "Regulatory compliance"
        ],
        primary_authority=[
            "AREMA Manual Chapter 7",
            "Railroad Signal Standards"
        ],
        burden_holder="Signal system designer",
        adversary_position="Approach Medium may be misinterpreted by inexperienced crews.",
        counter_arguments=[
            "Training and standardization mitigate risk.",
            "Aspect usage is industry standard."
        ],
        resolution_strategy="Audit aspect usage and update training as needed.",
        entity_scope="All signal installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Signal Aspect Guidance"
    ),
    DoctrineBlock(
        topic="Track Circuits - Axle Counter Integration",
        keywords=["track circuits", "axle counter", "block occupancy", "integration"],
        conclusion_template="Axle counters may be used as an alternative or supplement to track circuits for block occupancy detection, subject to regulatory approval.",
        reasoning_framework="""
        Axle counters provide reliable block occupancy detection, especially where track circuits are impractical (e.g., poor ballast, insulated joint issues). Integration with signal logic must ensure fail-safe operation. Regulatory approval is required, and periodic testing is mandated. Hybrid systems may combine both technologies for redundancy.
        """,
        key_factors=[
            "Detection reliability",
            "Integration logic",
            "Testing protocols",
            "Regulatory requirements"
        ],
        primary_authority=[
            "AREMA Manual Chapter 8",
            "FRA Technology Approvals"
        ],
        burden_holder="Signal system designer",
        adversary_position="Axle counters may be less familiar to maintenance staff.",
        counter_arguments=[
            "Training addresses knowledge gaps.",
            "Hybrid systems enhance reliability."
        ],
        resolution_strategy="Pilot axle counter installations and monitor performance.",
        entity_scope="All signaled tracks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Axle Counter Approvals"
    ),
    DoctrineBlock(
        topic="PTC - System Health Monitoring",
        keywords=["PTC", "system health", "monitoring", "fault detection"],
        conclusion_template="PTC systems must include continuous health monitoring and automatic fault reporting.",
        reasoning_framework="""
        Continuous monitoring of PTC system components enables rapid detection and response to faults. Health data must be logged and transmitted to maintenance personnel. Regulatory standards specify minimum monitoring requirements. Automated alerts and diagnostic tools improve system reliability and reduce downtime.
        """,
        key_factors=[
            "Monitoring coverage",
            "Data logging",
            "Alert protocols",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart I",
            "AAR PTC Implementation Guidelines"
        ],
        burden_holder="PTC system operator",
        adversary_position="Monitoring systems add to system complexity.",
        counter_arguments=[
            "Improved reliability offsets complexity.",
            "Automated tools streamline maintenance."
        ],
        resolution_strategy="Integrate health monitoring into all PTC deployments.",
        entity_scope="All PTC-equipped lines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA PTC System Reviews"
    ),
    DoctrineBlock(
        topic="CTC - Local Control Panel Authorization",
        keywords=["CTC", "local control panel", "authorization", "dispatcher override"],
        conclusion_template="Local control panels in CTC territory may only be used with dispatcher authorization, except in emergencies.",
        reasoning_framework="""
        Local control panels allow for manual operation of signals and switches during maintenance or emergencies. Use must be authorized by the dispatcher, with all actions logged. Regulatory standards specify authorization, logging, and restoration protocols. Training is required for all personnel authorized to use local panels.
        """,
        key_factors=[
            "Authorization protocols",
            "Logging",
            "Training",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA CTC Regulations",
            "Railroad Operating Rules"
        ],
        burden_holder="Railroad operations management",
        adversary_position="Local control may be misused or cause confusion.",
        counter_arguments=[
            "Strict protocols and training mitigate risk.",
            "Local control is essential for safe maintenance."
        ],
        resolution_strategy="Audit local control usage and update procedures as needed.",
        entity_scope="All CTC-controlled territories",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA CTC System Reviews"
    ),
    DoctrineBlock(
        topic="Grade Crossing - Pedestrian Warning Devices",
        keywords=["grade crossing", "pedestrian warning", "active protection", "safety"],
        conclusion_template="Active pedestrian warning devices are required at grade crossings with significant foot traffic.",
        reasoning_framework="""
        Pedestrian warning devices (flashing lights, audible alarms, gates) reduce risk at crossings with high pedestrian use. Regulatory standards specify minimum requirements based on risk assessment. Devices must be maintained in good working order and tested regularly. Community outreach and education supplement physical protection.
        """,
        key_factors=[
            "Pedestrian volume",
            "Device reliability",
            "Maintenance protocols",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA Grade Crossing Safety Regulations",
            "FHWA MUTCD"
        ],
        burden_holder="Railroad and local government",
        adversary_position="Devices increase installation and maintenance costs.",
        counter_arguments=[
            "Safety benefits outweigh costs.",
            "Funding is available for high-risk locations."
        ],
        resolution_strategy="Prioritize installation at high-risk crossings.",
        entity_scope="All public grade crossings",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Grade Crossing Safety Reports"
    ),
    DoctrineBlock(
        topic="Fail-Safe - Periodic System Audits",
        keywords=["fail-safe", "system audit", "regulatory compliance", "continuous improvement"],
        conclusion_template="Periodic system audits are required to verify fail-safe operation and regulatory compliance.",
        reasoning_framework="""
        Regular audits review system design, maintenance records, and incident data to ensure ongoing compliance with fail-safe principles. Audits identify areas for improvement and inform future upgrades. Regulatory authorities may conduct independent audits in addition to internal reviews. Findings must be documented and corrective actions tracked.
        """,
        key_factors=[
            "Audit frequency",
            "Documentation",
            "Corrective action tracking",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236",
            "AREMA Manual Chapter 17"
        ],
        burden_holder="Railroad safety manager",
        adversary_position="Audits require significant resources.",
        counter_arguments=[
            "Audits prevent costly incidents.",
            "Continuous improvement enhances safety."
        ],
        resolution_strategy="Schedule regular audits and track corrective actions.",
        entity_scope="All signal and control systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA System Audit Reports"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]