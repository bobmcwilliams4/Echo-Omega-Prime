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
        topic="VOR DME ILS Approach Navigation",
        keywords=["VOR", "DME", "ILS", "Approach", "Navigation", "Instrument Landing System"],
        conclusion_template="Aircraft must utilize VOR, DME, and ILS signals for precision approach navigation in accordance with ICAO Annex 10 and FAA 8260.3.",
        reasoning_framework="""
        The VOR (VHF Omnidirectional Range), DME (Distance Measuring Equipment), and ILS (Instrument Landing System) form the backbone of precision approach navigation. The doctrine requires pilots and avionics systems to interpret and respond to these signals, ensuring lateral and vertical guidance during approach. The reasoning is based on signal integrity, redundancy, and procedural compliance. The aircraft's navigation system must cross-check VOR and DME for position accuracy, while ILS provides glide slope and localizer information. The approach is validated against published procedures, ensuring obstacle clearance and alignment with runway thresholds. The doctrine emphasizes the use of fail-safe mechanisms and continuous monitoring of signal validity. In the event of signal degradation, alternate navigation sources must be engaged. The doctrine is rooted in regulatory requirements and operational best practices for instrument approaches.
        """,
        key_factors=[
            "Signal integrity",
            "Redundancy",
            "Procedural compliance",
            "Obstacle clearance",
            "Alignment with runway",
            "Fail-safe mechanisms"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA Order 8260.3",
            "EASA CS-25"
        ],
        burden_holder="Flight crew and avionics system",
        adversary_position="Reliance on legacy navigation may limit operational flexibility in GNSS-denied environments.",
        counter_arguments=[
            "ILS is still the most reliable precision approach method in adverse weather.",
            "VOR/DME provides redundancy when GNSS is unavailable."
        ],
        resolution_strategy="Maintain dual navigation capability and update navigation database regularly.",
        entity_scope="Commercial and business aviation",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA Order 8260.3"
    ),
    DoctrineBlock(
        topic="GPS WAAS SBAS GBAS Augmentation",
        keywords=["GPS", "WAAS", "SBAS", "GBAS", "Augmentation", "GNSS"],
        conclusion_template="Aircraft navigation systems must utilize GPS augmented by WAAS, SBAS, and GBAS for enhanced accuracy and integrity, as per RTCA DO-229 and ICAO Annex 10.",
        reasoning_framework="""
        The doctrine mandates the integration of GPS with augmentation systems such as WAAS (Wide Area Augmentation System), SBAS (Satellite-Based Augmentation System), and GBAS (Ground-Based Augmentation System) to improve positional accuracy and integrity. The reasoning is based on the need for reliable navigation in all phases of flight, especially during approaches and landings. WAAS and SBAS provide corrections for GPS signal errors, while GBAS supports precision approaches at specific airports. The avionics must validate augmentation signals and switch to alternate sources if integrity thresholds are not met. The doctrine emphasizes continuous monitoring, error correction, and compliance with published performance standards. The use of augmented GPS enables advanced procedures like LPV and GLS approaches, expanding operational capability and safety margins.
        """,
        key_factors=[
            "Signal correction",
            "Integrity monitoring",
            "Performance standards",
            "Operational capability",
            "Safety margins"
        ],
        primary_authority=[
            "RTCA DO-229",
            "ICAO Annex 10",
            "FAA AC 20-138"
        ],
        burden_holder="Avionics manufacturer and operator",
        adversary_position="Potential vulnerability to spoofing and jamming of GNSS signals.",
        counter_arguments=[
            "Augmentation systems improve resilience and detection of anomalies.",
            "Alternative navigation sources are available for contingency."
        ],
        resolution_strategy="Implement multi-layer integrity monitoring and regular system updates.",
        entity_scope="All GNSS-equipped aircraft",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="RTCA DO-229"
    ),
    DoctrineBlock(
        topic="INS Inertial Navigation Kalman Filtering",
        keywords=["INS", "Inertial Navigation", "Kalman Filter", "Sensor Fusion", "Position Estimation"],
        conclusion_template="INS must employ Kalman filtering for sensor fusion and error correction, ensuring robust position estimation as per ARINC 704 and FAA AC 20-138.",
        reasoning_framework="""
        The doctrine requires the use of Kalman filtering within Inertial Navigation Systems (INS) to fuse sensor data and correct for drift and bias. The Kalman filter algorithm combines accelerometer and gyroscope inputs, updating position and velocity estimates in real time. The reasoning is based on the need for autonomous navigation capability, especially in GNSS-denied environments. The filter must be tuned to minimize error propagation, and periodic alignment with external references (e.g., GPS) is recommended. The doctrine emphasizes robust initialization, continuous error monitoring, and adaptive filtering. INS must meet performance standards for accuracy and reliability, supporting critical flight operations such as oceanic crossings and military missions.
        """,
        key_factors=[
            "Sensor fusion",
            "Error correction",
            "Autonomous capability",
            "Filter tuning",
            "Performance standards"
        ],
        primary_authority=[
            "ARINC 704",
            "FAA AC 20-138",
            "MIL-STD-1553"
        ],
        burden_holder="Avionics software developer",
        adversary_position="Kalman filter complexity may introduce computational delays and instability.",
        counter_arguments=[
            "Modern processors handle real-time filtering efficiently.",
            "Adaptive filtering mitigates instability risks."
        ],
        resolution_strategy="Validate filter performance through simulation and flight testing.",
        entity_scope="Commercial, military, and business aircraft",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ARINC 704"
    ),
    DoctrineBlock(
        topic="FMS Flight Management System CDU Operation",
        keywords=["FMS", "CDU", "Flight Management", "Navigation", "Input Procedures"],
        conclusion_template="Flight crews must operate the FMS CDU in accordance with manufacturer procedures and FAA AC 20-131, ensuring accurate flight plan entry and execution.",
        reasoning_framework="""
        The doctrine stipulates that the Flight Management System (FMS) Control Display Unit (CDU) must be operated using standardized procedures to prevent input errors and ensure accurate navigation. The reasoning is based on human factors, system integrity, and compliance with regulatory guidance. Flight crews must verify all entries, cross-check against charts, and confirm active flight plans. The CDU interface must provide clear feedback and error messages. The doctrine emphasizes training, procedural discipline, and regular system updates. In the event of discrepancies, manual reversion and cross-verification are required. The doctrine supports safe and efficient operation of advanced navigation systems.
        """,
        key_factors=[
            "Human factors",
            "Procedural discipline",
            "System integrity",
            "Training",
            "Error prevention"
        ],
        primary_authority=[
            "FAA AC 20-131",
            "EASA AMC 20-27",
            "Manufacturer FMS manuals"
        ],
        burden_holder="Flight crew",
        adversary_position="CDU complexity may lead to input errors and confusion.",
        counter_arguments=[
            "Standardized procedures and training mitigate risks.",
            "Error messages and feedback support safe operation."
        ],
        resolution_strategy="Implement robust training programs and regular system audits.",
        entity_scope="All FMS-equipped aircraft",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-131"
    ),
    DoctrineBlock(
        topic="ADS-B Surveillance Transponder Modes",
        keywords=["ADS-B", "Surveillance", "Transponder", "Mode S", "Mode A", "Mode C"],
        conclusion_template="Aircraft must operate ADS-B transponders in Mode S, Mode A, or Mode C as required by airspace regulations and ICAO Annex 10.",
        reasoning_framework="""
        The doctrine requires aircraft to operate ADS-B (Automatic Dependent Surveillance-Broadcast) transponders in the appropriate mode based on airspace requirements. Mode S provides enhanced surveillance and communication, while Mode A and Mode C support legacy radar systems. The reasoning is based on regulatory mandates, interoperability, and safety. The avionics must automatically select the correct mode, transmit accurate position and identification, and respond to ATC interrogations. The doctrine emphasizes compliance with regional regulations, continuous monitoring, and timely maintenance. In the event of transponder failure, alternate procedures must be followed. The doctrine ensures safe and efficient surveillance in mixed-mode environments.
        """,
        key_factors=[
            "Regulatory compliance",
            "Interoperability",
            "Safety",
            "Automatic mode selection",
            "Maintenance"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA 14 CFR 91.225",
            "EASA CS-25"
        ],
        burden_holder="Aircraft operator",
        adversary_position="ADS-B reliance may expose aircraft to privacy and security risks.",
        counter_arguments=[
            "Encryption and anonymization mitigate privacy concerns.",
            "Fallback to legacy modes ensures continuity."
        ],
        resolution_strategy="Implement security protocols and monitor regulatory updates.",
        entity_scope="All aircraft operating in controlled airspace",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ICAO Annex 10"
    ),
    DoctrineBlock(
        topic="TCAS Collision Avoidance Resolution Advisories",
        keywords=["TCAS", "Collision Avoidance", "Resolution Advisory", "Traffic", "Surveillance"],
        conclusion_template="Aircraft must comply with TCAS resolution advisories unless overridden by ATC or safety considerations, per ICAO Annex 10 and FAA AC 120-55.",
        reasoning_framework="""
        The doctrine mandates compliance with Traffic Collision Avoidance System (TCAS) resolution advisories (RAs) to prevent mid-air collisions. The reasoning is based on real-time surveillance, algorithmic decision-making, and regulatory requirements. Pilots must follow RAs unless ATC instructions or overriding safety concerns dictate otherwise. The doctrine emphasizes training, system maintenance, and procedural discipline. TCAS must be integrated with other surveillance systems, and advisories must be communicated clearly to the flight crew. In the event of conflicting instructions, safety takes precedence. The doctrine supports safe separation and collision avoidance in dense traffic environments.
        """,
        key_factors=[
            "Real-time surveillance",
            "Algorithmic decision-making",
            "Regulatory requirements",
            "Training",
            "Procedural discipline"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA AC 120-55",
            "EASA AMC 20-15"
        ],
        burden_holder="Flight crew",
        adversary_position="TCAS advisories may conflict with ATC instructions or terrain avoidance.",
        counter_arguments=[
            "Safety takes precedence over conflicting instructions.",
            "Integrated systems reduce conflict risks."
        ],
        resolution_strategy="Establish clear procedures for resolving conflicts and prioritize safety.",
        entity_scope="Commercial and business aviation",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 120-55"
    ),
    DoctrineBlock(
        topic="EGPWS Terrain Awareness",
        keywords=["EGPWS", "Terrain Awareness", "Warning System", "TAWS", "Obstacle Avoidance"],
        conclusion_template="Aircraft must utilize EGPWS for terrain awareness and obstacle avoidance, complying with FAA TSO-C151 and EASA CS-25.",
        reasoning_framework="""
        The doctrine requires Enhanced Ground Proximity Warning System (EGPWS) operation for terrain awareness and obstacle avoidance. The reasoning is based on real-time terrain data, predictive algorithms, and regulatory mandates. EGPWS must provide timely alerts and guidance to the flight crew, enabling safe maneuvering. The system must be regularly updated with terrain databases and validated against operational scenarios. The doctrine emphasizes training, system maintenance, and procedural compliance. In the event of false or missed alerts, manual cross-verification and alternate procedures are required. The doctrine supports safe operations in challenging environments.
        """,
        key_factors=[
            "Real-time terrain data",
            "Predictive algorithms",
            "Regulatory mandates",
            "Database updates",
            "Training"
        ],
        primary_authority=[
            "FAA TSO-C151",
            "EASA CS-25",
            "ICAO Annex 6"
        ],
        burden_holder="Aircraft operator",
        adversary_position="EGPWS may generate nuisance alerts or miss terrain in database gaps.",
        counter_arguments=[
            "Regular database updates mitigate missed terrain risks.",
            "Training reduces response to nuisance alerts."
        ],
        resolution_strategy="Implement robust database management and crew training.",
        entity_scope="All EGPWS-equipped aircraft",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA TSO-C151"
    ),
    DoctrineBlock(
        topic="Weather Radar WXR Interpretation",
        keywords=["Weather Radar", "WXR", "Interpretation", "Storm Avoidance", "Precipitation"],
        conclusion_template="Flight crews must interpret weather radar data accurately for storm avoidance, per FAA AC 00-24 and manufacturer guidelines.",
        reasoning_framework="""
        The doctrine mandates accurate interpretation of weather radar (WXR) data for storm and precipitation avoidance. The reasoning is based on signal processing, display management, and operational procedures. Flight crews must understand radar limitations, attenuation effects, and display symbology. The doctrine emphasizes training, procedural discipline, and cross-verification with other weather sources. In the event of ambiguous data, conservative decision-making is required. The doctrine supports safe and efficient flight operations in adverse weather conditions.
        """,
        key_factors=[
            "Signal processing",
            "Display management",
            "Training",
            "Procedural discipline",
            "Cross-verification"
        ],
        primary_authority=[
            "FAA AC 00-24",
            "Manufacturer WXR manuals",
            "ICAO Annex 6"
        ],
        burden_holder="Flight crew",
        adversary_position="Radar interpretation errors may lead to inadvertent storm penetration.",
        counter_arguments=[
            "Training and cross-verification reduce interpretation errors.",
            "Modern radars provide enhanced symbology and attenuation correction."
        ],
        resolution_strategy="Implement recurrent training and system upgrades.",
        entity_scope="All WXR-equipped aircraft",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 00-24"
    ),
    DoctrineBlock(
        topic="HF VHF SATCOM Radio Systems",
        keywords=["HF", "VHF", "SATCOM", "Radio", "Communication", "Long-range"],
        conclusion_template="Aircraft must operate HF, VHF, and SATCOM radios in accordance with ICAO Annex 10 and FAA AC 20-50, ensuring reliable communication.",
        reasoning_framework="""
        The doctrine requires operation of HF (High Frequency), VHF (Very High Frequency), and SATCOM (Satellite Communication) radios for reliable communication across all flight phases. The reasoning is based on coverage, redundancy, and regulatory mandates. HF is used for oceanic and remote operations, VHF for continental and terminal areas, and SATCOM for global coverage. The avionics must automatically select the optimal communication channel, maintain signal integrity, and comply with ATC requirements. The doctrine emphasizes training, procedural discipline, and system maintenance. In the event of communication failure, alternate channels and emergency procedures must be engaged.
        """,
        key_factors=[
            "Coverage",
            "Redundancy",
            "Regulatory mandates",
            "Automatic channel selection",
            "Maintenance"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA AC 20-50",
            "EASA CS-25"
        ],
        burden_holder="Aircraft operator",
        adversary_position="HF and SATCOM may be subject to interference and signal degradation.",
        counter_arguments=[
            "Redundant systems ensure communication continuity.",
            "Automatic channel selection mitigates degradation risks."
        ],
        resolution_strategy="Maintain multiple communication channels and monitor signal integrity.",
        entity_scope="All aircraft operating internationally",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ICAO Annex 10"
    ),
    DoctrineBlock(
        topic="Datalink ACARS CPDLC",
        keywords=["Datalink", "ACARS", "CPDLC", "Communication", "Digital"],
        conclusion_template="Aircraft must utilize ACARS and CPDLC datalink for digital communication with ATC, per ICAO Doc 4444 and FAA AC 120-70.",
        reasoning_framework="""
        The doctrine mandates the use of ACARS (Aircraft Communications Addressing and Reporting System) and CPDLC (Controller Pilot Data Link Communications) for digital communication with ATC. The reasoning is based on operational efficiency, message integrity, and regulatory requirements. The avionics must support secure message transmission, automatic logging, and timely response. The doctrine emphasizes compliance with regional mandates, system maintenance, and crew training. In the event of datalink failure, manual voice communication procedures must be followed. The doctrine supports safe and efficient operations in high-density and oceanic airspace.
        """,
        key_factors=[
            "Operational efficiency",
            "Message integrity",
            "Regulatory requirements",
            "Secure transmission",
            "Training"
        ],
        primary_authority=[
            "ICAO Doc 4444",
            "FAA AC 120-70",
            "EASA AMC 20-14"
        ],
        burden_holder="Aircraft operator",
        adversary_position="Datalink may be vulnerable to cyber threats and message delays.",
        counter_arguments=[
            "Encryption and authentication mitigate cyber risks.",
            "Fallback to voice communication ensures continuity."
        ],
        resolution_strategy="Implement robust cybersecurity and maintain voice communication capability.",
        entity_scope="All datalink-equipped aircraft",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ICAO Doc 4444"
    ),
    DoctrineBlock(
        topic="Glass Cockpit EFIS PFD ND EICAS",
        keywords=["Glass Cockpit", "EFIS", "PFD", "ND", "EICAS", "Display"],
        conclusion_template="Aircraft must operate glass cockpit EFIS, PFD, ND, and EICAS displays in accordance with manufacturer guidelines and FAA AC 20-88.",
        reasoning_framework="""
        The doctrine requires operation of glass cockpit displays including EFIS (Electronic Flight Instrument System), PFD (Primary Flight Display), ND (Navigation Display), and EICAS (Engine Indication and Crew Alerting System). The reasoning is based on display management, human factors, and regulatory mandates. Flight crews must understand display symbology, manage alerts, and cross-verify information. The doctrine emphasizes training, procedural discipline, and regular system updates. In the event of display failure, manual reversion and alternate procedures must be followed. The doctrine supports safe and efficient flight operations with advanced avionics.
        """,
        key_factors=[
            "Display management",
            "Human factors",
            "Training",
            "Procedural discipline",
            "System updates"
        ],
        primary_authority=[
            "FAA AC 20-88",
            "EASA AMC 20-23",
            "Manufacturer manuals"
        ],
        burden_holder="Flight crew",
        adversary_position="Display complexity may lead to information overload and misinterpretation.",
        counter_arguments=[
            "Training and ergonomic design mitigate overload risks.",
            "Alert management supports safe operation."
        ],
        resolution_strategy="Implement recurrent training and ergonomic system design.",
        entity_scope="All glass cockpit-equipped aircraft",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-88"
    ),
    DoctrineBlock(
        topic="Autopilot Flight Director Servo Modes",
        keywords=["Autopilot", "Flight Director", "Servo", "Modes", "Automation"],
        conclusion_template="Autopilot and flight director systems must operate in designated servo modes as per FAA AC 25-11 and manufacturer specifications.",
        reasoning_framework="""
        The doctrine mandates operation of autopilot and flight director systems in designated servo modes for automated flight control. The reasoning is based on system integrity, operational safety, and regulatory compliance. The avionics must support mode selection, feedback monitoring, and fail-safe operation. Flight crews must understand mode transitions, alert management, and manual override procedures. The doctrine emphasizes training, procedural discipline, and system maintenance. In the event of automation failure, manual control and alternate procedures must be engaged. The doctrine supports safe and efficient flight operations with advanced automation.
        """,
        key_factors=[
            "System integrity",
            "Operational safety",
            "Mode selection",
            "Training",
            "Fail-safe operation"
        ],
        primary_authority=[
            "FAA AC 25-11",
            "EASA AMC 25.1329",
            "Manufacturer manuals"
        ],
        burden_holder="Flight crew and avionics engineer",
        adversary_position="Automation complexity may lead to mode confusion and loss of situational awareness.",
        counter_arguments=[
            "Training and alert management mitigate mode confusion.",
            "Manual override ensures safety."
        ],
        resolution_strategy="Implement robust training and ergonomic system design.",
        entity_scope="All autopilot-equipped aircraft",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 25-11"
    ),
    DoctrineBlock(
        topic="Air Data Computer Pitot Static",
        keywords=["Air Data Computer", "Pitot", "Static", "Pressure", "Altitude"],
        conclusion_template="Air data computers must accurately process pitot and static pressure inputs for altitude and speed calculation, per FAA AC 20-94 and EASA CS-25.",
        reasoning_framework="""
        The doctrine requires air data computers to process pitot and static pressure inputs for accurate altitude and speed calculation. The reasoning is based on sensor integrity, calibration, and regulatory mandates. The avionics must continuously monitor sensor inputs, detect anomalies, and provide reliable data to flight displays. The doctrine emphasizes maintenance, calibration, and procedural discipline. In the event of sensor failure, alternate sources and manual procedures must be engaged. The doctrine supports safe and efficient flight operations with accurate air data.
        """,
        key_factors=[
            "Sensor integrity",
            "Calibration",
            "Maintenance",
            "Procedural discipline",
            "Anomaly detection"
        ],
        primary_authority=[
            "FAA AC 20-94",
            "EASA CS-25",
            "Manufacturer manuals"
        ],
        burden_holder="Avionics engineer and maintenance crew",
        adversary_position="Pitot-static system failures may lead to unreliable air data and flight hazards.",
        counter_arguments=[
            "Redundant sensors and regular maintenance mitigate risks.",
            "Manual procedures support safe operation."
        ],
        resolution_strategy="Implement robust maintenance and sensor redundancy.",
        entity_scope="All aircraft with air data computers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-94"
    ),
    DoctrineBlock(
        topic="Radio Altimeter Decision Height",
        keywords=["Radio Altimeter", "Decision Height", "Approach", "Landing", "Altitude"],
        conclusion_template="Radio altimeters must provide accurate decision height information for approach and landing, per FAA AC 20-138 and ICAO Annex 10.",
        reasoning_framework="""
        The doctrine requires radio altimeters to provide accurate decision height information during approach and landing. The reasoning is based on sensor integrity, regulatory mandates, and operational safety. The avionics must continuously monitor altitude above ground level, alert the flight crew at decision height, and support automated landing systems. The doctrine emphasizes maintenance, calibration, and procedural discipline. In the event of sensor failure, alternate sources and manual procedures must be engaged. The doctrine supports safe and efficient approach and landing operations.
        """,
        key_factors=[
            "Sensor integrity",
            "Regulatory mandates",
            "Operational safety",
            "Calibration",
            "Alert management"
        ],
        primary_authority=[
            "FAA AC 20-138",
            "ICAO Annex 10",
            "EASA CS-25"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="Radio altimeter interference may lead to erroneous decision height alerts.",
        counter_arguments=[
            "Regular calibration and interference monitoring mitigate risks.",
            "Manual procedures support safe operation."
        ],
        resolution_strategy="Implement robust maintenance and interference detection.",
        entity_scope="All aircraft with radio altimeters",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-138"
    ),
    DoctrineBlock(
        topic="DME Arc Procedure Turns",
        keywords=["DME", "Arc", "Procedure Turn", "Navigation", "Approach"],
        conclusion_template="Aircraft must execute DME arc procedure turns in accordance with published approach charts and FAA Order 8260.3.",
        reasoning_framework="""
        The doctrine requires execution of DME arc procedure turns as published in approach charts. The reasoning is based on navigation accuracy, procedural discipline, and regulatory mandates. The avionics must calculate and display arc positions, alert the flight crew to turn points, and support manual or automated execution. The doctrine emphasizes training, chart verification, and system maintenance. In the event of navigation system failure, manual procedures and cross-verification must be engaged. The doctrine supports safe and efficient approach operations.
        """,
        key_factors=[
            "Navigation accuracy",
            "Procedural discipline",
            "Chart verification",
            "Training",
            "System maintenance"
        ],
        primary_authority=[
            "FAA Order 8260.3",
            "ICAO Annex 10",
            "EASA CS-25"
        ],
        burden_holder="Flight crew",
        adversary_position="DME arc execution errors may lead to missed approach and obstacle hazards.",
        counter_arguments=[
            "Training and chart verification mitigate execution errors.",
            "Automated systems support accurate arc navigation."
        ],
        resolution_strategy="Implement recurrent training and system upgrades.",
        entity_scope="All aircraft executing DME arc approaches",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA Order 8260.3"
    ),
    DoctrineBlock(
        topic="RNAV RNP Approaches",
        keywords=["RNAV", "RNP", "Approach", "Navigation", "Performance"],
        conclusion_template="Aircraft must execute RNAV RNP approaches in accordance with FAA AC 90-101 and ICAO PBN Manual.",
        reasoning_framework="""
        The doctrine mandates execution of RNAV (Area Navigation) and RNP (Required Navigation Performance) approaches as per published procedures. The reasoning is based on navigation accuracy, performance monitoring, and regulatory mandates. The avionics must support RNP values, alert the flight crew to deviations, and comply with operational minima. The doctrine emphasizes training, chart verification, and system maintenance. In the event of navigation system failure, alternate procedures and manual reversion must be engaged. The doctrine supports safe and efficient approach operations in complex airspace.
        """,
        key_factors=[
            "Navigation accuracy",
            "Performance monitoring",
            "Operational minima",
            "Training",
            "Chart verification"
        ],
        primary_authority=[
            "FAA AC 90-101",
            "ICAO PBN Manual",
            "EASA AMC 20-28"
        ],
        burden_holder="Flight crew and avionics engineer",
        adversary_position="RNP approach complexity may lead to navigation errors and missed approaches.",
        counter_arguments=[
            "Training and performance monitoring mitigate risks.",
            "Automated systems support accurate navigation."
        ],
        resolution_strategy="Implement robust training and system maintenance.",
        entity_scope="All aircraft executing RNAV RNP approaches",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 90-101"
    ),
    DoctrineBlock(
        topic="RVSM Reduced Vertical Separation",
        keywords=["RVSM", "Reduced Vertical Separation", "Altitude", "Airspace", "Compliance"],
        conclusion_template="Aircraft must comply with RVSM requirements for reduced vertical separation in designated airspace, per FAA AC 91-85 and ICAO Annex 11.",
        reasoning_framework="""
        The doctrine requires compliance with Reduced Vertical Separation Minimum (RVSM) requirements in designated airspace. The reasoning is based on altitude accuracy, equipment certification, and regulatory mandates. The avionics must support precise altitude measurement, alert the flight crew to deviations, and comply with operational procedures. The doctrine emphasizes equipment maintenance, certification, and crew training. In the event of equipment failure, alternate procedures and ATC notification must be engaged. The doctrine supports safe and efficient operations in high-density airspace.
        """,
        key_factors=[
            "Altitude accuracy",
            "Equipment certification",
            "Operational procedures",
            "Maintenance",
            "Training"
        ],
        primary_authority=[
            "FAA AC 91-85",
            "ICAO Annex 11",
            "EASA AMC 20-27"
        ],
        burden_holder="Aircraft operator",
        adversary_position="RVSM compliance may be compromised by equipment failures or maintenance lapses.",
        counter_arguments=[
            "Regular maintenance and certification mitigate risks.",
            "ATC notification supports safe operation."
        ],
        resolution_strategy="Implement robust maintenance and certification programs.",
        entity_scope="All aircraft operating in RVSM airspace",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 91-85"
    ),
    DoctrineBlock(
        topic="ELT Emergency Locator",
        keywords=["ELT", "Emergency Locator", "Beacon", "Search and Rescue", "Distress"],
        conclusion_template="Aircraft must operate ELT emergency locator beacons in accordance with ICAO Annex 6 and FAA 14 CFR 91.207.",
        reasoning_framework="""
        The doctrine requires operation of Emergency Locator Transmitter (ELT) beacons for search and rescue in distress situations. The reasoning is based on regulatory mandates, signal integrity, and operational safety. The avionics must automatically activate ELT in crash scenarios, transmit distress signals, and support search and rescue operations. The doctrine emphasizes maintenance, battery replacement, and periodic testing. In the event of ELT failure, alternate procedures and manual activation must be engaged. The doctrine supports safe and efficient emergency response.
        """,
        key_factors=[
            "Regulatory mandates",
            "Signal integrity",
            "Automatic activation",
            "Maintenance",
            "Testing"
        ],
        primary_authority=[
            "ICAO Annex 6",
            "FAA 14 CFR 91.207",
            "EASA CS-25"
        ],
        burden_holder="Aircraft operator",
        adversary_position="ELT signal may be lost or fail to activate in crash scenarios.",
        counter_arguments=[
            "Regular maintenance and testing mitigate risks.",
            "Manual activation supports emergency response."
        ],
        resolution_strategy="Implement robust maintenance and testing programs.",
        entity_scope="All aircraft with ELT beacons",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA 14 CFR 91.207"
    ),
    DoctrineBlock(
        topic="Cockpit Voice Recorder Flight Data Recorder",
        keywords=["Cockpit Voice Recorder", "Flight Data Recorder", "CVR", "FDR", "Accident Investigation"],
        conclusion_template="Aircraft must operate CVR and FDR systems in accordance with ICAO Annex 6 and FAA 14 CFR 121.359.",
        reasoning_framework="""
        The doctrine requires operation of Cockpit Voice Recorder (CVR) and Flight Data Recorder (FDR) systems for accident investigation and operational monitoring. The reasoning is based on regulatory mandates, data integrity, and operational safety. The avionics must continuously record cockpit audio and flight parameters, support data retrieval, and comply with retention requirements. The doctrine emphasizes maintenance, periodic testing, and procedural discipline. In the event of recorder failure, alternate procedures and manual logs must be engaged. The doctrine supports safe and efficient accident investigation and operational monitoring.
        """,
        key_factors=[
            "Regulatory mandates",
            "Data integrity",
            "Continuous recording",
            "Maintenance",
            "Retention requirements"
        ],
        primary_authority=[
            "ICAO Annex 6",
            "FAA 14 CFR 121.359",
            "EASA CS-25"
        ],
        burden_holder="Aircraft operator",
        adversary_position="Recorder failures may compromise accident investigation and operational monitoring.",
        counter_arguments=[
            "Regular maintenance and testing mitigate risks.",
            "Manual logs support investigation."
        ],
        resolution_strategy="Implement robust maintenance and testing programs.",
        entity_scope="All aircraft with CVR and FDR systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA 14 CFR 121.359"
    ),
    DoctrineBlock(
        topic="Performance Monitoring",
        keywords=["Performance Monitoring", "Navigation", "Accuracy", "Integrity", "Operational Safety"],
        conclusion_template="Aircraft navigation systems must continuously monitor performance for accuracy and integrity, per ICAO Annex 10 and FAA AC 20-138.",
        reasoning_framework="""
        The doctrine requires continuous performance monitoring of aircraft navigation systems for accuracy and integrity. The reasoning is based on regulatory mandates, operational safety, and system reliability. The avionics must monitor navigation accuracy, alert the flight crew to deviations, and comply with operational minima. The doctrine emphasizes system maintenance, calibration, and procedural discipline. In the event of performance degradation, alternate procedures and manual reversion must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "Operational safety",
            "System reliability",
            "Calibration",
            "Alert management"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA AC 20-138",
            "EASA AMC 20-28"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="Performance monitoring complexity may lead to false alerts and operational disruptions.",
        counter_arguments=[
            "Calibration and alert management mitigate risks.",
            "Manual procedures support safe operation."
        ],
        resolution_strategy="Implement robust calibration and alert management systems.",
        entity_scope="All aircraft with performance monitoring systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-138"
    ),
    DoctrineBlock(
        topic="Altitude Management",
        keywords=["Altitude Management", "Navigation", "Flight Level", "Compliance", "Safety"],
        conclusion_template="Aircraft must manage altitude in accordance with published procedures and ATC instructions, per ICAO Annex 11 and FAA AC 91-85.",
        reasoning_framework="""
        The doctrine requires aircraft to manage altitude in accordance with published procedures and ATC instructions. The reasoning is based on regulatory mandates, operational safety, and system reliability. The avionics must support precise altitude measurement, alert the flight crew to deviations, and comply with operational minima. The doctrine emphasizes system maintenance, calibration, and procedural discipline. In the event of altitude deviation, immediate correction and ATC notification must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "Operational safety",
            "System reliability",
            "Calibration",
            "ATC compliance"
        ],
        primary_authority=[
            "ICAO Annex 11",
            "FAA AC 91-85",
            "EASA AMC 20-27"
        ],
        burden_holder="Flight crew",
        adversary_position="Altitude management errors may lead to loss of separation and flight hazards.",
        counter_arguments=[
            "Training and alert management mitigate risks.",
            "ATC notification supports safe operation."
        ],
        resolution_strategy="Implement robust training and alert management systems.",
        entity_scope="All aircraft operating in controlled airspace",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 91-85"
    ),
    DoctrineBlock(
        topic="Surveillance Integrity Monitoring",
        keywords=["Surveillance", "Integrity Monitoring", "ADS-B", "TCAS", "Safety"],
        conclusion_template="Aircraft surveillance systems must continuously monitor integrity for operational safety, per ICAO Annex 10 and FAA AC 120-55.",
        reasoning_framework="""
        The doctrine requires continuous integrity monitoring of aircraft surveillance systems for operational safety. The reasoning is based on regulatory mandates, system reliability, and safety. The avionics must monitor surveillance data, alert the flight crew to anomalies, and comply with operational procedures. The doctrine emphasizes system maintenance, calibration, and procedural discipline. In the event of integrity degradation, alternate procedures and manual reversion must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System reliability",
            "Safety",
            "Calibration",
            "Alert management"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA AC 120-55",
            "EASA AMC 20-15"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="Integrity monitoring complexity may lead to false alerts and operational disruptions.",
        counter_arguments=[
            "Calibration and alert management mitigate risks.",
            "Manual procedures support safe operation."
        ],
        resolution_strategy="Implement robust calibration and alert management systems.",
        entity_scope="All aircraft with surveillance systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 120-55"
    ),
    DoctrineBlock(
        topic="Cockpit Display Management",
        keywords=["Cockpit Display", "Management", "EFIS", "EICAS", "PFD", "ND"],
        conclusion_template="Flight crews must manage cockpit displays in accordance with manufacturer guidelines and FAA AC 20-88.",
        reasoning_framework="""
        The doctrine requires flight crews to manage cockpit displays including EFIS, EICAS, PFD, and ND in accordance with manufacturer guidelines. The reasoning is based on display management, human factors, and regulatory mandates. Flight crews must understand display symbology, manage alerts, and cross-verify information. The doctrine emphasizes training, procedural discipline, and regular system updates. In the event of display failure, manual reversion and alternate procedures must be followed. The doctrine supports safe and efficient flight operations with advanced avionics.
        """,
        key_factors=[
            "Display management",
            "Human factors",
            "Training",
            "Procedural discipline",
            "System updates"
        ],
        primary_authority=[
            "FAA AC 20-88",
            "EASA AMC 20-23",
            "Manufacturer manuals"
        ],
        burden_holder="Flight crew",
        adversary_position="Display complexity may lead to information overload and misinterpretation.",
        counter_arguments=[
            "Training and ergonomic design mitigate overload risks.",
            "Alert management supports safe operation."
        ],
        resolution_strategy="Implement recurrent training and ergonomic system design.",
        entity_scope="All glass cockpit-equipped aircraft",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-88"
    ),
    DoctrineBlock(
        topic="Emergency Communications",
        keywords=["Emergency Communications", "HF", "VHF", "SATCOM", "Distress", "ATC"],
        conclusion_template="Aircraft must operate emergency communications in accordance with ICAO Annex 10 and FAA AC 20-50.",
        reasoning_framework="""
        The doctrine requires operation of emergency communications using HF, VHF, and SATCOM radios in accordance with regulatory mandates. The reasoning is based on coverage, redundancy, and operational safety. The avionics must support emergency channel selection, transmit distress signals, and comply with ATC requirements. The doctrine emphasizes training, procedural discipline, and system maintenance. In the event of communication failure, alternate channels and manual procedures must be engaged. The doctrine supports safe and efficient emergency response.
        """,
        key_factors=[
            "Coverage",
            "Redundancy",
            "Operational safety",
            "Emergency channel selection",
            "Training"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA AC 20-50",
            "EASA CS-25"
        ],
        burden_holder="Aircraft operator",
        adversary_position="Emergency communication failures may compromise distress response.",
        counter_arguments=[
            "Redundant systems and training mitigate risks.",
            "Manual procedures support emergency response."
        ],
        resolution_strategy="Implement robust maintenance and training programs.",
        entity_scope="All aircraft operating internationally",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ICAO Annex 10"
    ),
    DoctrineBlock(
        topic="Flight Plan Management",
        keywords=["Flight Plan", "Management", "FMS", "CDU", "Navigation"],
        conclusion_template="Flight crews must manage flight plans in accordance with manufacturer procedures and FAA AC 20-131.",
        reasoning_framework="""
        The doctrine requires flight crews to manage flight plans using FMS and CDU in accordance with manufacturer procedures. The reasoning is based on human factors, system integrity, and regulatory mandates. Flight crews must verify all entries, cross-check against charts, and confirm active flight plans. The doctrine emphasizes training, procedural discipline, and regular system updates. In the event of discrepancies, manual reversion and cross-verification are required. The doctrine supports safe and efficient operation of advanced navigation systems.
        """,
        key_factors=[
            "Human factors",
            "Procedural discipline",
            "System integrity",
            "Training",
            "Error prevention"
        ],
        primary_authority=[
            "FAA AC 20-131",
            "EASA AMC 20-27",
            "Manufacturer FMS manuals"
        ],
        burden_holder="Flight crew",
        adversary_position="Flight plan management errors may lead to navigation deviations.",
        counter_arguments=[
            "Standardized procedures and training mitigate risks.",
            "Error messages and feedback support safe operation."
        ],
        resolution_strategy="Implement robust training programs and regular system audits.",
        entity_scope="All FMS-equipped aircraft",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-131"
    ),
    DoctrineBlock(
        topic="System Redundancy",
        keywords=["System Redundancy", "Navigation", "Safety", "Reliability", "Backup"],
        conclusion_template="Aircraft navigation systems must maintain redundancy for operational safety, per ICAO Annex 10 and FAA AC 20-138.",
        reasoning_framework="""
        The doctrine requires aircraft navigation systems to maintain redundancy for operational safety. The reasoning is based on regulatory mandates, system reliability, and safety. The avionics must support backup systems, automatic switchover, and continuous monitoring. The doctrine emphasizes maintenance, calibration, and procedural discipline. In the event of primary system failure, backup systems and manual procedures must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System reliability",
            "Backup systems",
            "Maintenance",
            "Calibration"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA AC 20-138",
            "EASA AMC 20-28"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="Redundancy complexity may lead to operational confusion and maintenance challenges.",
        counter_arguments=[
            "Training and maintenance mitigate risks.",
            "Automatic switchover supports safe operation."
        ],
        resolution_strategy="Implement robust maintenance and training programs.",
        entity_scope="All aircraft with redundant navigation systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-138"
    ),
    DoctrineBlock(
        topic="Integrity Monitoring",
        keywords=["Integrity Monitoring", "Navigation", "Safety", "Performance", "Alert"],
        conclusion_template="Aircraft navigation systems must continuously monitor integrity for operational safety, per ICAO Annex 10 and FAA AC 20-138.",
        reasoning_framework="""
        The doctrine requires continuous integrity monitoring of aircraft navigation systems for operational safety. The reasoning is based on regulatory mandates, system reliability, and safety. The avionics must monitor navigation data, alert the flight crew to anomalies, and comply with operational procedures. The doctrine emphasizes system maintenance, calibration, and procedural discipline. In the event of integrity degradation, alternate procedures and manual reversion must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System reliability",
            "Safety",
            "Calibration",
            "Alert management"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "FAA AC 20-138",
            "EASA AMC 20-28"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="Integrity monitoring complexity may lead to false alerts and operational disruptions.",
        counter_arguments=[
            "Calibration and alert management mitigate risks.",
            "Manual procedures support safe operation."
        ],
        resolution_strategy="Implement robust calibration and alert management systems.",
        entity_scope="All aircraft with navigation systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-138"
    ),
    DoctrineBlock(
        topic="Navigation Database Management",
        keywords=["Navigation Database", "Management", "FMS", "CDU", "Updates"],
        conclusion_template="Aircraft navigation databases must be managed and updated regularly per FAA AC 20-153 and ICAO Annex 10.",
        reasoning_framework="""
        The doctrine requires regular management and updating of aircraft navigation databases in FMS and CDU systems. The reasoning is based on regulatory mandates, data integrity, and operational safety. The avionics must support database updates, cross-verification, and error detection. The doctrine emphasizes maintenance, procedural discipline, and regular audits. In the event of database errors, manual reversion and cross-verification must be engaged. The doctrine supports safe and efficient operation of advanced navigation systems.
        """,
        key_factors=[
            "Regulatory mandates",
            "Data integrity",
            "Database updates",
            "Maintenance",
            "Procedural discipline"
        ],
        primary_authority=[
            "FAA AC 20-153",
            "ICAO Annex 10",
            "EASA AMC 20-27"
        ],
        burden_holder="Avionics engineer and aircraft operator",
        adversary_position="Database management errors may lead to navigation deviations.",
        counter_arguments=[
            "Regular audits and updates mitigate risks.",
            "Manual reversion supports safe operation."
        ],
        resolution_strategy="Implement robust maintenance and audit programs.",
        entity_scope="All aircraft with navigation databases",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-153"
    ),
    DoctrineBlock(
        topic="Flight Data Monitoring",
        keywords=["Flight Data Monitoring", "FDM", "Safety", "Operational Analysis", "Compliance"],
        conclusion_template="Aircraft must implement flight data monitoring for safety and operational analysis, per ICAO Annex 6 and FAA AC 120-82.",
        reasoning_framework="""
        The doctrine requires implementation of flight data monitoring (FDM) for safety and operational analysis. The reasoning is based on regulatory mandates, data integrity, and operational safety. The avionics must support continuous data recording, retrieval, and analysis. The doctrine emphasizes maintenance, periodic testing, and procedural discipline. In the event of data monitoring failure, manual logs and alternate procedures must be engaged. The doctrine supports safe and efficient flight operations and compliance with safety programs.
        """,
        key_factors=[
            "Regulatory mandates",
            "Data integrity",
            "Continuous recording",
            "Maintenance",
            "Operational analysis"
        ],
        primary_authority=[
            "ICAO Annex 6",
            "FAA AC 120-82",
            "EASA CS-25"
        ],
        burden_holder="Aircraft operator",
        adversary_position="FDM failures may compromise safety and operational analysis.",
        counter_arguments=[
            "Regular maintenance and testing mitigate risks.",
            "Manual logs support operational analysis."
        ],
        resolution_strategy="Implement robust maintenance and testing programs.",
        entity_scope="All aircraft with FDM systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 120-82"
    ),
    DoctrineBlock(
        topic="Autopilot Servo Modes",
        keywords=["Autopilot", "Servo Modes", "Automation", "Flight Control", "Safety"],
        conclusion_template="Autopilot systems must operate in designated servo modes for automated flight control, per FAA AC 25-11 and manufacturer specifications.",
        reasoning_framework="""
        The doctrine mandates operation of autopilot systems in designated servo modes for automated flight control. The reasoning is based on system integrity, operational safety, and regulatory compliance. The avionics must support mode selection, feedback monitoring, and fail-safe operation. Flight crews must understand mode transitions, alert management, and manual override procedures. The doctrine emphasizes training, procedural discipline, and system maintenance. In the event of automation failure, manual control and alternate procedures must be engaged. The doctrine supports safe and efficient flight operations with advanced automation.
        """,
        key_factors=[
            "System integrity",
            "Operational safety",
            "Mode selection",
            "Training",
            "Fail-safe operation"
        ],
        primary_authority=[
            "FAA AC 25-11",
            "EASA AMC 25.1329",
            "Manufacturer manuals"
        ],
        burden_holder="Flight crew and avionics engineer",
        adversary_position="Automation complexity may lead to mode confusion and loss of situational awareness.",
        counter_arguments=[
            "Training and alert management mitigate mode confusion.",
            "Manual override ensures safety."
        ],
        resolution_strategy="Implement robust training and ergonomic system design.",
        entity_scope="All autopilot-equipped aircraft",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 25-11"
    ),
    DoctrineBlock(
        topic="GNSS Integrity Management",
        keywords=["GNSS", "Integrity Management", "GPS", "SBAS", "WAAS", "Safety"],
        conclusion_template="Aircraft GNSS systems must implement integrity management per ICAO Annex 10 and RTCA DO-229.",
        reasoning_framework="""
        The doctrine requires GNSS systems to implement integrity management for operational safety. The reasoning is based on regulatory mandates, signal reliability, and system performance. The avionics must monitor GNSS signal integrity, alert the flight crew to anomalies, and comply with operational procedures. The doctrine emphasizes system maintenance, calibration, and procedural discipline. In the event of integrity degradation, alternate procedures and manual reversion must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "Signal reliability",
            "System performance",
            "Calibration",
            "Alert management"
        ],
        primary_authority=[
            "ICAO Annex 10",
            "RTCA DO-229",
            "FAA AC 20-138"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="GNSS integrity management complexity may lead to false alerts and operational disruptions.",
        counter_arguments=[
            "Calibration and alert management mitigate risks.",
            "Manual procedures support safe operation."
        ],
        resolution_strategy="Implement robust calibration and alert management systems.",
        entity_scope="All GNSS-equipped aircraft",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="RTCA DO-229"
    ),
    DoctrineBlock(
        topic="Navigation System Fault Detection",
        keywords=["Navigation System", "Fault Detection", "Safety", "Integrity", "Redundancy"],
        conclusion_template="Aircraft navigation systems must implement fault detection and isolation per FAA AC 20-138 and ICAO Annex 10.",
        reasoning_framework="""
        The doctrine requires navigation systems to implement fault detection and isolation for operational safety. The reasoning is based on regulatory mandates, system reliability, and safety. The avionics must monitor navigation data, detect faults, and isolate affected components. The doctrine emphasizes system maintenance, calibration, and procedural discipline. In the event of fault detection, backup systems and manual procedures must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System reliability",
            "Fault detection",
            "Redundancy",
            "Maintenance"
        ],
        primary_authority=[
            "FAA AC 20-138",
            "ICAO Annex 10",
            "EASA AMC 20-28"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="Fault detection complexity may lead to operational confusion and maintenance challenges.",
        counter_arguments=[
            "Training and maintenance mitigate risks.",
            "Automatic isolation supports safe operation."
        ],
        resolution_strategy="Implement robust maintenance and training programs.",
        entity_scope="All aircraft with navigation systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-138"
    ),
    DoctrineBlock(
        topic="Flight Data Integrity Assurance",
        keywords=["Flight Data", "Integrity Assurance", "FDR", "CVR", "Safety"],
        conclusion_template="Aircraft must assure flight data integrity for operational safety and accident investigation, per ICAO Annex 6 and FAA 14 CFR 121.359.",
        reasoning_framework="""
        The doctrine requires assurance of flight data integrity for operational safety and accident investigation. The reasoning is based on regulatory mandates, data reliability, and safety. The avionics must support continuous data recording, error detection, and secure storage. The doctrine emphasizes maintenance, periodic testing, and procedural discipline. In the event of data integrity degradation, manual logs and alternate procedures must be engaged. The doctrine supports safe and efficient flight operations and accident investigation.
        """,
        key_factors=[
            "Regulatory mandates",
            "Data reliability",
            "Continuous recording",
            "Error detection",
            "Maintenance"
        ],
        primary_authority=[
            "ICAO Annex 6",
            "FAA 14 CFR 121.359",
            "EASA CS-25"
        ],
        burden_holder="Aircraft operator",
        adversary_position="Data integrity failures may compromise safety and accident investigation.",
        counter_arguments=[
            "Regular maintenance and testing mitigate risks.",
            "Manual logs support investigation."
        ],
        resolution_strategy="Implement robust maintenance and testing programs.",
        entity_scope="All aircraft with FDR and CVR systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA 14 CFR 121.359"
    ),
    DoctrineBlock(
        topic="Navigation System Cybersecurity",
        keywords=["Navigation System", "Cybersecurity", "Safety", "Integrity", "Protection"],
        conclusion_template="Aircraft navigation systems must implement cybersecurity measures per FAA AC 119-1 and ICAO Annex 10.",
        reasoning_framework="""
        The doctrine requires navigation systems to implement cybersecurity measures for operational safety. The reasoning is based on regulatory mandates, system protection, and safety. The avionics must support encryption, authentication, and intrusion detection. The doctrine emphasizes system maintenance, periodic testing, and procedural discipline. In the event of cybersecurity breach, manual procedures and alternate systems must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System protection",
            "Encryption",
            "Authentication",
            "Intrusion detection"
        ],
        primary_authority=[
            "FAA AC 119-1",
            "ICAO Annex 10",
            "EASA AMC 20-28"
        ],
        burden_holder="Avionics engineer and aircraft operator",
        adversary_position="Cybersecurity complexity may lead to operational disruptions and maintenance challenges.",
        counter_arguments=[
            "Training and maintenance mitigate risks.",
            "Encryption and authentication support safe operation."
        ],
        resolution_strategy="Implement robust maintenance and training programs.",
        entity_scope="All aircraft with navigation systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 119-1"
    ),
    DoctrineBlock(
        topic="Navigation System Software Assurance",
        keywords=["Navigation System", "Software Assurance", "Safety", "Integrity", "Certification"],
        conclusion_template="Aircraft navigation system software must comply with assurance requirements per RTCA DO-178C and FAA AC 20-115C.",
        reasoning_framework="""
        The doctrine requires navigation system software to comply with assurance requirements for operational safety. The reasoning is based on regulatory mandates, software reliability, and certification. The avionics must support software verification, validation, and error detection. The doctrine emphasizes system maintenance, periodic testing, and procedural discipline. In the event of software failure, manual procedures and alternate systems must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "Software reliability",
            "Verification",
            "Validation",
            "Certification"
        ],
        primary_authority=[
            "RTCA DO-178C",
            "FAA AC 20-115C",
            "EASA AMC 20-115"
        ],
        burden_holder="Avionics software developer",
        adversary_position="Software assurance complexity may lead to operational disruptions and certification challenges.",
        counter_arguments=[
            "Verification and validation mitigate risks.",
            "Certification supports safe operation."
        ],
        resolution_strategy="Implement robust maintenance and testing programs.",
        entity_scope="All aircraft with navigation system software",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="RTCA DO-178C"
    ),
    DoctrineBlock(
        topic="Navigation System Human Factors",
        keywords=["Navigation System", "Human Factors", "Safety", "Training", "Ergonomics"],
        conclusion_template="Aircraft navigation systems must address human factors for operational safety, per FAA AC 25-11 and ICAO Annex 10.",
        reasoning_framework="""
        The doctrine requires navigation systems to address human factors for operational safety. The reasoning is based on regulatory mandates, ergonomic design, and training. The avionics must support intuitive interfaces, alert management, and cross-verification. The doctrine emphasizes training, procedural discipline, and regular system updates. In the event of human factors errors, manual procedures and alternate systems must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "Ergonomic design",
            "Training",
            "Alert management",
            "Cross-verification"
        ],
        primary_authority=[
            "FAA AC 25-11",
            "ICAO Annex 10",
            "EASA AMC 20-23"
        ],
        burden_holder="Avionics engineer and flight crew",
        adversary_position="Human factors complexity may lead to operational errors and safety risks.",
        counter_arguments=[
            "Training and ergonomic design mitigate risks.",
            "Alert management supports safe operation."
        ],
        resolution_strategy="Implement recurrent training and ergonomic system design.",
        entity_scope="All aircraft with navigation systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 25-11"
    ),
    DoctrineBlock(
        topic="Navigation System Environmental Qualification",
        keywords=["Navigation System", "Environmental Qualification", "Safety", "Reliability", "Testing"],
        conclusion_template="Aircraft navigation systems must meet environmental qualification requirements per RTCA DO-160 and FAA AC 20-136.",
        reasoning_framework="""
        The doctrine requires navigation systems to meet environmental qualification requirements for operational safety. The reasoning is based on regulatory mandates, system reliability, and testing. The avionics must support environmental testing, qualification, and error detection. The doctrine emphasizes system maintenance, periodic testing, and procedural discipline. In the event of environmental qualification failure, manual procedures and alternate systems must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System reliability",
            "Environmental testing",
            "Qualification",
            "Maintenance"
        ],
        primary_authority=[
            "RTCA DO-160",
            "FAA AC 20-136",
            "EASA AMC 20-28"
        ],
        burden_holder="Avionics engineer and aircraft operator",
        adversary_position="Environmental qualification complexity may lead to operational disruptions and maintenance challenges.",
        counter_arguments=[
            "Testing and maintenance mitigate risks.",
            "Qualification supports safe operation."
        ],
        resolution_strategy="Implement robust maintenance and testing programs.",
        entity_scope="All aircraft with navigation systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="RTCA DO-160"
    ),
    DoctrineBlock(
        topic="Navigation System Maintenance Program",
        keywords=["Navigation System", "Maintenance Program", "Safety", "Reliability", "Compliance"],
        conclusion_template="Aircraft navigation systems must implement maintenance programs per FAA AC 120-16 and ICAO Annex 6.",
        reasoning_framework="""
        The doctrine requires navigation systems to implement maintenance programs for operational safety. The reasoning is based on regulatory mandates, system reliability, and compliance. The avionics must support scheduled maintenance, error detection, and documentation. The doctrine emphasizes procedural discipline, periodic testing, and regular audits. In the event of maintenance program failure, manual procedures and alternate systems must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System reliability",
            "Scheduled maintenance",
            "Error detection",
            "Documentation"
        ],
        primary_authority=[
            "FAA AC 120-16",
            "ICAO Annex 6",
            "EASA AMC 20-28"
        ],
        burden_holder="Aircraft operator",
        adversary_position="Maintenance program complexity may lead to operational disruptions and compliance challenges.",
        counter_arguments=[
            "Procedural discipline and audits mitigate risks.",
            "Scheduled maintenance supports safe operation."
        ],
        resolution_strategy="Implement robust maintenance and audit programs.",
        entity_scope="All aircraft with navigation systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 120-16"
    ),
    DoctrineBlock(
        topic="Navigation System Certification",
        keywords=["Navigation System", "Certification", "Safety", "Compliance", "Approval"],
        conclusion_template="Aircraft navigation systems must be certified per FAA AC 20-138 and EASA AMC 20-28.",
        reasoning_framework="""
        The doctrine requires navigation systems to be certified for operational safety. The reasoning is based on regulatory mandates, system reliability, and compliance. The avionics must support certification testing, documentation, and approval. The doctrine emphasizes procedural discipline, periodic testing, and regular audits. In the event of certification failure, manual procedures and alternate systems must be engaged. The doctrine supports safe and efficient flight operations.
        """,
        key_factors=[
            "Regulatory mandates",
            "System reliability",
            "Certification testing",
            "Documentation",
            "Approval"
        ],
        primary_authority=[
            "FAA AC 20-138",
            "EASA AMC 20-28",
            "ICAO Annex 10"
        ],
        burden_holder="Avionics engineer and aircraft operator",
        adversary_position="Certification complexity may lead to operational disruptions and compliance challenges.",
        counter_arguments=[
            "Procedural discipline and audits mitigate risks.",
            "Certification supports safe operation."
        ],
        resolution_strategy="Implement robust certification and audit programs.",
        entity_scope="All aircraft with navigation systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA AC 20-138"
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