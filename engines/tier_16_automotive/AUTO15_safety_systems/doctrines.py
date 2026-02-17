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
        topic="Frontal Airbag Non-Deployment Analysis",
        keywords=["frontal airbag", "non-deployment", "crash", "sensor", "threshold"],
        conclusion_template="If the crash severity exceeded deployment thresholds and the airbag did not deploy, a defect or calibration error may be indicated.",
        reasoning_framework=(
            "1. Review crash pulse data and compare with OEM deployment thresholds.\n"
            "2. Analyze sensor data (accelerometer, crash sensors) for proper function.\n"
            "3. Assess occupant position and seatbelt usage for suppression logic triggers.\n"
            "4. Examine airbag control module (ACM) for fault codes or pre-existing errors.\n"
            "5. Reference FMVSS 208 and OEM technical bulletins for deployment criteria.\n"
            "6. Consider environmental factors (temperature, impact angle) affecting deployment.\n"
            "7. Evaluate any recalls or field reports related to non-deployment in similar models.\n"
            "8. Synthesize findings to determine if non-deployment was justified or a system failure."
        ),
        key_factors=[
            "Crash severity (delta-V, pulse duration)",
            "Sensor integrity and calibration",
            "Occupant detection and suppression logic",
            "ACM fault codes",
            "OEM deployment thresholds",
            "Environmental and crash conditions"
        ],
        primary_authority=[
            "FMVSS 208",
            "OEM Service Manuals",
            "NHTSA Investigation Reports"
        ],
        burden_holder="Plaintiff (alleging defect)",
        adversary_position="Airbag non-deployment was consistent with system design and regulatory requirements.",
        counter_arguments=[
            "Deployment thresholds were met but system failed.",
            "Suppression logic was improperly triggered.",
            "Sensor malfunction or improper calibration."
        ],
        resolution_strategy="Conduct root cause analysis using crash data, ACM interrogation, and compare with regulatory and OEM standards.",
        entity_scope="AUTO15 Frontal Airbag System",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NHTSA ODI Investigation PE15-027"
    ),
    DoctrineBlock(
        topic="Seatbelt Pretensioner Failure Modes",
        keywords=["seatbelt", "pretensioner", "failure", "deployment", "load limiter"],
        conclusion_template="A seatbelt pretensioner that fails to deploy in a qualifying crash event may indicate a system fault or design defect.",
        reasoning_framework=(
            "1. Identify crash severity and pretensioner deployment criteria per OEM.\n"
            "2. Retrieve crash data recorder (CDR) logs for pretensioner activation signals.\n"
            "3. Inspect physical components for evidence of firing or mechanical failure.\n"
            "4. Review system diagnostics for pre-crash or crash event faults.\n"
            "5. Compare with FMVSS 209 and 210 requirements for seatbelt systems.\n"
            "6. Analyze any recalls or technical service bulletins related to pretensioner failures.\n"
            "7. Evaluate occupant kinematics and injury outcomes for causation analysis.\n"
            "8. Conclude if failure was due to system design, maintenance, or crash conditions."
        ),
        key_factors=[
            "Crash severity and direction",
            "CDR pretensioner activation data",
            "Physical evidence of deployment",
            "System diagnostics and faults",
            "Regulatory compliance",
            "Occupant injury patterns"
        ],
        primary_authority=[
            "FMVSS 209",
            "FMVSS 210",
            "OEM Technical Bulletins"
        ],
        burden_holder="Plaintiff (claiming non-deployment)",
        adversary_position="Pretensioner did not deploy due to crash severity or system logic.",
        counter_arguments=[
            "Crash severity met deployment criteria.",
            "System failed due to defect.",
            "Improper maintenance or prior damage."
        ],
        resolution_strategy="Integrate CDR data, physical inspection, and regulatory review to determine root cause.",
        entity_scope="AUTO15 Seatbelt System",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NHTSA Recall 20V-123"
    ),
    DoctrineBlock(
        topic="Automatic Emergency Braking (AEB) False Negatives",
        keywords=["AEB", "automatic emergency braking", "false negative", "sensor", "collision"],
        conclusion_template="AEB system failure to activate in imminent collision scenarios may indicate sensor limitations, algorithmic errors, or system defects.",
        reasoning_framework=(
            "1. Define the collision scenario and expected AEB response per OEM specifications.\n"
            "2. Analyze sensor data (radar, camera) for object detection and classification performance.\n"
            "3. Review event logs for AEB activation signals or suppression logic triggers.\n"
            "4. Assess environmental conditions (weather, lighting, road markings) affecting detection.\n"
            "5. Compare with NHTSA and Euro NCAP AEB test protocols.\n"
            "6. Investigate any relevant recalls or field reports of AEB false negatives.\n"
            "7. Determine if system limitations or malfunctions were the root cause.\n"
            "8. Document findings with reference to regulatory and industry standards."
        ),
        key_factors=[
            "Object detection accuracy",
            "Sensor performance and calibration",
            "Environmental and situational factors",
            "AEB algorithm logic",
            "Regulatory test protocols",
            "System diagnostics"
        ],
        primary_authority=[
            "NHTSA AEB Test Protocol",
            "Euro NCAP AEB Assessment",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging system failure)",
        adversary_position="AEB system performed within design and regulatory limits.",
        counter_arguments=[
            "AEB failed to detect obstacle due to sensor limitations.",
            "Algorithmic suppression was inappropriate.",
            "Environmental conditions were within operational design domain."
        ],
        resolution_strategy="Correlate sensor data, event logs, and regulatory standards to assess AEB performance.",
        entity_scope="AUTO15 AEB System",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="NHTSA ODI EA19-002"
    ),
    DoctrineBlock(
        topic="Side-Impact Airbag Deployment Thresholds",
        keywords=["side-impact", "airbag", "deployment", "threshold", "crash"],
        conclusion_template="Side-impact airbag deployment must occur when crash severity and intrusion exceed OEM and regulatory thresholds.",
        reasoning_framework=(
            "1. Analyze crash data for lateral acceleration and intrusion measurements.\n"
            "2. Compare with OEM side airbag deployment criteria and FMVSS 214.\n"
            "3. Inspect side airbag modules for evidence of deployment or malfunction.\n"
            "4. Review occupant position and seat adjustment for suppression logic.\n"
            "5. Assess system diagnostics for pre-crash or crash event faults.\n"
            "6. Consider any recalls or field reports of side airbag non-deployment.\n"
            "7. Synthesize findings to determine compliance and root cause."
        ),
        key_factors=[
            "Lateral crash severity",
            "Intrusion measurements",
            "Occupant position",
            "System diagnostics",
            "OEM deployment thresholds",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 214",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging non-deployment)",
        adversary_position="Side airbag did not deploy due to crash severity or suppression logic.",
        counter_arguments=[
            "Crash severity and intrusion exceeded thresholds.",
            "System failed due to defect.",
            "Suppression logic was improperly triggered."
        ],
        resolution_strategy="Compare crash data and system diagnostics with regulatory and OEM criteria.",
        entity_scope="AUTO15 Side Airbag System",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="NHTSA Recall 18V-123"
    ),
    DoctrineBlock(
        topic="Blind Spot Monitoring (BSM) System Limitations",
        keywords=["blind spot monitoring", "BSM", "sensor", "detection", "limitations"],
        conclusion_template="BSM system limitations must be disclosed to users, and performance must meet regulatory and industry standards.",
        reasoning_framework=(
            "1. Identify the operational design domain (ODD) for the BSM system.\n"
            "2. Evaluate sensor coverage, detection range, and blind spot zones.\n"
            "3. Review system response to various vehicle types and environmental conditions.\n"
            "4. Analyze false negative and false positive rates in NHTSA and IIHS tests.\n"
            "5. Assess OEM user manuals for disclosure of system limitations.\n"
            "6. Examine any field reports or recalls related to BSM performance.\n"
            "7. Determine if system limitations were adequately disclosed and within standards."
        ),
        key_factors=[
            "Sensor coverage and range",
            "Detection accuracy",
            "Environmental and situational factors",
            "User manual disclosures",
            "Regulatory and industry standards"
        ],
        primary_authority=[
            "NHTSA Blind Spot Detection Guidelines",
            "IIHS Test Protocols",
            "OEM User Manuals"
        ],
        burden_holder="Plaintiff (alleging inadequate disclosure or performance)",
        adversary_position="BSM system performed within disclosed limitations and standards.",
        counter_arguments=[
            "System limitations were not adequately disclosed.",
            "Detection range was insufficient for typical scenarios.",
            "False negatives led to preventable collisions."
        ],
        resolution_strategy="Review system specifications, test data, and user disclosures for adequacy and compliance.",
        entity_scope="AUTO15 BSM System",
        confidence=0.83,
        confidence_zone="Moderate-High",
        controlling_precedent="NHTSA Blind Spot Monitoring Assessment 2018"
    ),
    DoctrineBlock(
        topic="Pedestrian Detection System Performance",
        keywords=["pedestrian detection", "AEB", "sensor", "performance", "vulnerable road users"],
        conclusion_template="Pedestrian detection systems must reliably identify and respond to vulnerable road users within the operational design domain.",
        reasoning_framework=(
            "1. Define the ODD for pedestrian detection (speed, lighting, weather).\n"
            "2. Analyze sensor fusion (camera, radar, lidar) for detection accuracy.\n"
            "3. Review event logs for system response to pedestrian presence.\n"
            "4. Compare with Euro NCAP and NHTSA pedestrian AEB test protocols.\n"
            "5. Assess any recalls or field reports of system failures.\n"
            "6. Evaluate user manual disclosures regarding limitations.\n"
            "7. Synthesize findings to determine if system met performance expectations."
        ),
        key_factors=[
            "Sensor fusion accuracy",
            "Environmental conditions",
            "System response time",
            "Regulatory test protocols",
            "User disclosures"
        ],
        primary_authority=[
            "Euro NCAP Pedestrian AEB Protocol",
            "NHTSA Pedestrian AEB Test",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging system failure)",
        adversary_position="System performed within design and regulatory limits.",
        counter_arguments=[
            "System failed to detect pedestrian in ODD.",
            "Response time was inadequate.",
            "Limitations were not disclosed."
        ],
        resolution_strategy="Compare event logs and test results with regulatory protocols and disclosures.",
        entity_scope="AUTO15 Pedestrian Detection System",
        confidence=0.82,
        confidence_zone="Moderate-High",
        controlling_precedent="Euro NCAP Pedestrian AEB 2020"
    ),
    DoctrineBlock(
        topic="FMVSS 208 Advanced Airbag Rule Compliance",
        keywords=["FMVSS 208", "advanced airbag", "compliance", "suppression", "deployment"],
        conclusion_template="Advanced airbag systems must comply with FMVSS 208 suppression and deployment requirements for all occupant categories.",
        reasoning_framework=(
            "1. Review system design for occupant classification and suppression logic.\n"
            "2. Analyze crash data for airbag deployment or suppression in various occupant scenarios.\n"
            "3. Compare with FMVSS 208 test procedures and compliance documentation.\n"
            "4. Assess system diagnostics for faults or malfunctions.\n"
            "5. Examine any recalls or compliance failures in similar models.\n"
            "6. Synthesize findings to determine regulatory compliance."
        ),
        key_factors=[
            "Occupant classification accuracy",
            "Suppression logic performance",
            "Deployment thresholds",
            "Regulatory test results",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 208",
            "NHTSA Compliance Test Reports",
            "OEM Certification Documents"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="System failed to comply with FMVSS 208 in real-world scenarios.",
        counter_arguments=[
            "Suppression logic was improperly triggered.",
            "Occupant classification was inaccurate.",
            "Deployment thresholds were not met."
        ],
        resolution_strategy="Review compliance documentation, test results, and system diagnostics.",
        entity_scope="AUTO15 Advanced Airbag System",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Compliance Test 208-2017-001"
    ),
    DoctrineBlock(
        topic="Lane Departure Warning (LDW) vs. Lane Keep Assist (LKA) Functionality",
        keywords=["LDW", "lane departure warning", "LKA", "lane keep assist", "functionality"],
        conclusion_template="LDW and LKA systems must be clearly differentiated in user documentation and perform within defined operational parameters.",
        reasoning_framework=(
            "1. Define functional differences between LDW (alert) and LKA (active intervention).\n"
            "2. Review system activation criteria and operational design domain.\n"
            "3. Assess user interface and alert mechanisms for clarity.\n"
            "4. Compare with NHTSA and SAE definitions and test protocols.\n"
            "5. Examine any field reports of user confusion or system failures.\n"
            "6. Evaluate user manual disclosures for adequacy.\n"
            "7. Synthesize findings to determine if differentiation and performance were adequate."
        ),
        key_factors=[
            "Functional definitions",
            "Activation criteria",
            "User interface clarity",
            "Regulatory and industry standards",
            "User manual disclosures"
        ],
        primary_authority=[
            "NHTSA LDW/LKA Guidelines",
            "SAE J3016",
            "OEM User Manuals"
        ],
        burden_holder="Manufacturer (ensuring clarity and compliance)",
        adversary_position="User confusion led to improper system use or reliance.",
        counter_arguments=[
            "User interface was unclear.",
            "System did not perform as described.",
            "Disclosures were inadequate."
        ],
        resolution_strategy="Review user manuals, interface design, and field reports for clarity and compliance.",
        entity_scope="AUTO15 LDW/LKA Systems",
        confidence=0.84,
        confidence_zone="Moderate-High",
        controlling_precedent="NHTSA LDW/LKA Assessment 2019"
    ),
    DoctrineBlock(
        topic="Rollover Crash Roof Strength and Occupant Protection",
        keywords=["rollover", "roof strength", "occupant protection", "FMVSS 216", "injury"],
        conclusion_template="Roof structure must meet FMVSS 216 strength requirements to ensure occupant survival space during rollovers.",
        reasoning_framework=(
            "1. Review crash reconstruction for rollover dynamics and roof deformation.\n"
            "2. Compare roof strength with FMVSS 216 static crush test results.\n"
            "3. Assess occupant kinematics and injury mechanisms.\n"
            "4. Examine CDR data for seatbelt usage and airbag deployment.\n"
            "5. Review any recalls or field reports of roof collapse.\n"
            "6. Synthesize findings to determine compliance and occupant protection adequacy."
        ),
        key_factors=[
            "Roof deformation measurements",
            "FMVSS 216 compliance",
            "Occupant kinematics",
            "Seatbelt and airbag performance",
            "Crash dynamics"
        ],
        primary_authority=[
            "FMVSS 216",
            "NHTSA Rollover Test Reports",
            "OEM Structural Analysis"
        ],
        burden_holder="Plaintiff (alleging inadequate roof strength)",
        adversary_position="Roof met all regulatory requirements and performed as designed.",
        counter_arguments=[
            "Roof strength was insufficient for crash severity.",
            "Design did not provide adequate survival space.",
            "Prior damage or manufacturing defect."
        ],
        resolution_strategy="Compare crash data and test results with FMVSS 216 and OEM analysis.",
        entity_scope="AUTO15 Roof Structure",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NHTSA Rollover Test 216-2018-005"
    ),
    DoctrineBlock(
        topic="Crash Data Recorder (CDR) Admissibility and Interpretation",
        keywords=["CDR", "crash data recorder", "admissibility", "interpretation", "legal"],
        conclusion_template="CDR data is admissible if properly preserved and interpreted according to SAE J1698 and legal standards.",
        reasoning_framework=(
            "1. Verify chain of custody and data integrity for CDR extraction.\n"
            "2. Review extraction process for compliance with SAE J1698.\n"
            "3. Assess data relevance to crash events and occupant actions.\n"
            "4. Consider legal precedents for admissibility in jurisdiction.\n"
            "5. Evaluate expert interpretation for accuracy and objectivity.\n"
            "6. Synthesize findings to determine evidentiary value."
        ),
        key_factors=[
            "Chain of custody",
            "Extraction process",
            "Data relevance",
            "Expert interpretation",
            "Legal precedents"
        ],
        primary_authority=[
            "SAE J1698",
            "Federal Rules of Evidence",
            "State Case Law"
        ],
        burden_holder="Proponent of CDR evidence",
        adversary_position="CDR data is unreliable or improperly obtained.",
        counter_arguments=[
            "Chain of custody was broken.",
            "Extraction was not SAE-compliant.",
            "Data does not reflect actual events."
        ],
        resolution_strategy="Ensure proper extraction, documentation, and expert analysis per SAE and legal standards.",
        entity_scope="AUTO15 CDR System",
        confidence=0.92,
        confidence_zone="Very High",
        controlling_precedent="State v. Shabazz, 246 So.3d 131 (Fla. 2018)"
    ),
    DoctrineBlock(
        topic="Occupant Classification System (OCS) Suppression Logic",
        keywords=["OCS", "occupant classification", "suppression", "airbag", "child seat"],
        conclusion_template="OCS must accurately classify occupants and suppress airbags when required by FMVSS 208.",
        reasoning_framework=(
            "1. Review OCS sensor data for occupant weight and position classification.\n"
            "2. Analyze airbag deployment or suppression in crash events.\n"
            "3. Compare with FMVSS 208 suppression requirements for child seats and small occupants.\n"
            "4. Assess system diagnostics for faults or calibration errors.\n"
            "5. Examine any recalls or field reports related to OCS failures.\n"
            "6. Synthesize findings to determine compliance and system accuracy."
        ),
        key_factors=[
            "Occupant weight and position",
            "Sensor calibration",
            "Deployment/suppression events",
            "Regulatory compliance",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 208",
            "NHTSA OCS Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="OCS failed to suppress airbag for child seat or small occupant.",
        counter_arguments=[
            "Sensor misclassification.",
            "Calibration error.",
            "Suppression logic failure."
        ],
        resolution_strategy="Compare sensor data and event logs with FMVSS 208 and OEM criteria.",
        entity_scope="AUTO15 OCS System",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="NHTSA OCS Compliance 2017"
    ),
    DoctrineBlock(
        topic="Tire Pressure Monitoring System (TPMS) Warnings and Blowout Crashes",
        keywords=["TPMS", "tire pressure", "warning", "blowout", "crash"],
        conclusion_template="TPMS must provide timely warnings to prevent blowout-related crashes as required by FMVSS 138.",
        reasoning_framework=(
            "1. Review TPMS warning logs and timing relative to tire pressure loss.\n"
            "2. Compare with FMVSS 138 requirements for warning thresholds and response time.\n"
            "3. Assess user response to warnings and system interface clarity.\n"
            "4. Examine tire condition and maintenance records.\n"
            "5. Analyze any recalls or field reports of TPMS failures.\n"
            "6. Synthesize findings to determine compliance and causation."
        ),
        key_factors=[
            "Warning timing and thresholds",
            "User response",
            "System interface",
            "Tire condition",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 138",
            "NHTSA TPMS Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging inadequate warning)",
        adversary_position="TPMS performed within regulatory requirements.",
        counter_arguments=[
            "Warning was delayed or absent.",
            "System failed to detect pressure loss.",
            "User interface was unclear."
        ],
        resolution_strategy="Compare warning logs and system performance with FMVSS 138 and OEM standards.",
        entity_scope="AUTO15 TPMS",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="NHTSA TPMS Compliance 2016"
    ),
    DoctrineBlock(
        topic="Electronic Stability Control (ESC) Intervention and Limitations",
        keywords=["ESC", "electronic stability control", "intervention", "limitations", "FMVSS 126"],
        conclusion_template="ESC must intervene to prevent loss of control within the operational design domain, as required by FMVSS 126.",
        reasoning_framework=(
            "1. Review event data for ESC activation and intervention timing.\n"
            "2. Compare with FMVSS 126 test protocols for yaw rate and lateral acceleration.\n"
            "3. Assess environmental and road conditions affecting ESC performance.\n"
            "4. Analyze any recalls or field reports of ESC failures or limitations.\n"
            "5. Synthesize findings to determine compliance and system adequacy."
        ),
        key_factors=[
            "ESC activation timing",
            "Yaw rate and lateral acceleration",
            "Environmental conditions",
            "System diagnostics",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 126",
            "NHTSA ESC Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging inadequate intervention)",
        adversary_position="ESC performed within design and regulatory limits.",
        counter_arguments=[
            "ESC failed to intervene in loss of control.",
            "System limitations were not disclosed.",
            "Environmental conditions were within ODD."
        ],
        resolution_strategy="Compare event data and test results with FMVSS 126 and OEM criteria.",
        entity_scope="AUTO15 ESC System",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NHTSA ESC Compliance 2015"
    ),
    DoctrineBlock(
        topic="Seatbelt Webbing Failure and Load Limiter Function",
        keywords=["seatbelt", "webbing", "failure", "load limiter", "FMVSS 209"],
        conclusion_template="Seatbelt webbing and load limiter must function as required by FMVSS 209 to prevent occupant ejection and excessive force.",
        reasoning_framework=(
            "1. Inspect seatbelt webbing for tears, stretching, or separation post-crash.\n"
            "2. Review CDR data for load limiter activation and force levels.\n"
            "3. Compare with FMVSS 209 requirements for webbing strength and elongation.\n"
            "4. Assess any recalls or field reports of webbing or load limiter failures.\n"
            "5. Synthesize findings to determine compliance and causation."
        ),
        key_factors=[
            "Webbing condition",
            "Load limiter activation",
            "Occupant injury patterns",
            "Regulatory compliance",
            "Crash severity"
        ],
        primary_authority=[
            "FMVSS 209",
            "NHTSA Seatbelt Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging webbing failure)",
        adversary_position="Webbing and load limiter performed within regulatory requirements.",
        counter_arguments=[
            "Webbing failed below required strength.",
            "Load limiter did not activate as designed.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare physical evidence and CDR data with FMVSS 209 and OEM standards.",
        entity_scope="AUTO15 Seatbelt System",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="NHTSA Seatbelt Webbing Recall 17V-123"
    ),
    DoctrineBlock(
        topic="Adaptive Cruise Control (ACC) Following Distance and Emergency Braking",
        keywords=["ACC", "adaptive cruise control", "following distance", "emergency braking", "AEB"],
        conclusion_template="ACC must maintain safe following distances and initiate emergency braking as required by OEM and regulatory standards.",
        reasoning_framework=(
            "1. Review ACC system settings and user-selected following distances.\n"
            "2. Analyze sensor data for object detection and distance measurement.\n"
            "3. Assess system response to sudden deceleration of lead vehicle.\n"
            "4. Compare with NHTSA and Euro NCAP ACC test protocols.\n"
            "5. Examine any field reports or recalls related to ACC failures.\n"
            "6. Synthesize findings to determine compliance and system adequacy."
        ),
        key_factors=[
            "Following distance settings",
            "Sensor accuracy",
            "System response time",
            "Regulatory test protocols",
            "User manual disclosures"
        ],
        primary_authority=[
            "NHTSA ACC Test Protocol",
            "Euro NCAP ACC Assessment",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging inadequate following distance or braking)",
        adversary_position="ACC performed within design and regulatory limits.",
        counter_arguments=[
            "System failed to maintain safe distance.",
            "Emergency braking was not initiated.",
            "Sensor limitations were not disclosed."
        ],
        resolution_strategy="Compare system logs and test results with regulatory protocols and OEM standards.",
        entity_scope="AUTO15 ACC System",
        confidence=0.83,
        confidence_zone="Moderate-High",
        controlling_precedent="NHTSA ACC Assessment 2020"
    ),
    DoctrineBlock(
        topic="Curtain Airbag Deployment in Rollover Crashes",
        keywords=["curtain airbag", "rollover", "deployment", "FMVSS 226", "occupant protection"],
        conclusion_template="Curtain airbags must deploy in rollover crashes to provide occupant ejection mitigation as required by FMVSS 226.",
        reasoning_framework=(
            "1. Review crash data for rollover detection and curtain airbag deployment signals.\n"
            "2. Compare with FMVSS 226 requirements for ejection mitigation.\n"
            "3. Assess system diagnostics for faults or suppression logic triggers.\n"
            "4. Examine any recalls or field reports of curtain airbag non-deployment.\n"
            "5. Synthesize findings to determine compliance and occupant protection adequacy."
        ),
        key_factors=[
            "Rollover detection",
            "Curtain airbag deployment",
            "System diagnostics",
            "Regulatory compliance",
            "Occupant ejection risk"
        ],
        primary_authority=[
            "FMVSS 226",
            "NHTSA Rollover Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging non-deployment)",
        adversary_position="Curtain airbag did not deploy due to crash severity or system logic.",
        counter_arguments=[
            "Rollover was detected but airbag failed to deploy.",
            "System defect or calibration error.",
            "Suppression logic was improperly triggered."
        ],
        resolution_strategy="Compare crash data and system diagnostics with FMVSS 226 and OEM criteria.",
        entity_scope="AUTO15 Curtain Airbag System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NHTSA Curtain Airbag Compliance 2018"
    ),
    DoctrineBlock(
        topic="Forward Collision Warning (FCW) Alert Timing and Driver Response",
        keywords=["FCW", "forward collision warning", "alert timing", "driver response", "AEB"],
        conclusion_template="FCW must provide timely alerts to allow adequate driver response as defined by regulatory and industry standards.",
        reasoning_framework=(
            "1. Review event logs for FCW alert timing relative to collision threat.\n"
            "2. Compare with NHTSA and Euro NCAP FCW test protocols.\n"
            "3. Assess driver response time and crash outcome.\n"
            "4. Examine user manual disclosures for alert timing expectations.\n"
            "5. Synthesize findings to determine if alert timing was adequate."
        ),
        key_factors=[
            "Alert timing",
            "Driver response",
            "System settings",
            "Regulatory test protocols",
            "Crash outcome"
        ],
        primary_authority=[
            "NHTSA FCW Test Protocol",
            "Euro NCAP FCW Assessment",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging late or absent alert)",
        adversary_position="FCW performed within design and regulatory limits.",
        counter_arguments=[
            "Alert was delayed or absent.",
            "System settings were inappropriate.",
            "User manual disclosures were inadequate."
        ],
        resolution_strategy="Compare event logs and test results with regulatory protocols and OEM standards.",
        entity_scope="AUTO15 FCW System",
        confidence=0.84,
        confidence_zone="Moderate-High",
        controlling_precedent="NHTSA FCW Assessment 2019"
    ),
    DoctrineBlock(
        topic="Rear Cross-Traffic Alert (RCTA) Detection Zones and Limitations",
        keywords=["RCTA", "rear cross-traffic alert", "detection zone", "limitations", "sensor"],
        conclusion_template="RCTA detection zones and limitations must be disclosed, and system must perform within defined parameters.",
        reasoning_framework=(
            "1. Review RCTA sensor coverage and detection zone specifications.\n"
            "2. Analyze system response to cross-traffic in various scenarios.\n"
            "3. Compare with NHTSA and IIHS RCTA test protocols.\n"
            "4. Assess user manual disclosures for detection zone and limitations.\n"
            "5. Synthesize findings to determine adequacy of performance and disclosure."
        ),
        key_factors=[
            "Detection zone coverage",
            "System response time",
            "Environmental and situational factors",
            "User manual disclosures",
            "Regulatory test protocols"
        ],
        primary_authority=[
            "NHTSA RCTA Test Protocol",
            "IIHS RCTA Assessment",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging inadequate detection or disclosure)",
        adversary_position="RCTA performed within disclosed limitations and standards.",
        counter_arguments=[
            "Detection zone was insufficient.",
            "System failed to alert in typical scenarios.",
            "Limitations were not adequately disclosed."
        ],
        resolution_strategy="Compare system specifications, test results, and disclosures with regulatory and industry standards.",
        entity_scope="AUTO15 RCTA System",
        confidence=0.81,
        confidence_zone="Moderate",
        controlling_precedent="NHTSA RCTA Assessment 2018"
    ),
    DoctrineBlock(
        topic="Headrest and Whiplash Injury Mitigation",
        keywords=["headrest", "whiplash", "injury mitigation", "FMVSS 202a", "seat design"],
        conclusion_template="Headrest design must meet FMVSS 202a requirements to minimize whiplash injury risk.",
        reasoning_framework=(
            "1. Review seat and headrest geometry relative to occupant position.\n"
            "2. Compare with FMVSS 202a requirements for height, distance, and adjustment.\n"
            "3. Assess crash data for whiplash injury occurrence and severity.\n"
            "4. Examine any recalls or field reports of headrest failures.\n"
            "5. Synthesize findings to determine compliance and injury mitigation adequacy."
        ),
        key_factors=[
            "Headrest geometry",
            "Occupant position",
            "FMVSS 202a compliance",
            "Crash injury data",
            "Seat design"
        ],
        primary_authority=[
            "FMVSS 202a",
            "NHTSA Headrest Test Reports",
            "OEM Seat Design Specifications"
        ],
        burden_holder="Plaintiff (alleging inadequate headrest design)",
        adversary_position="Headrest met all regulatory requirements and performed as designed.",
        counter_arguments=[
            "Headrest geometry was insufficient.",
            "Design did not minimize whiplash risk.",
            "Manufacturing defect or improper adjustment."
        ],
        resolution_strategy="Compare seat and headrest design with FMVSS 202a and crash data.",
        entity_scope="AUTO15 Seat System",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="NHTSA Headrest Compliance 2017"
    ),
    DoctrineBlock(
        topic="Child Safety Seat Compatibility and LATCH System",
        keywords=["child safety seat", "LATCH", "compatibility", "FMVSS 225", "installation"],
        conclusion_template="LATCH system must provide secure and compatible attachment for child safety seats as required by FMVSS 225.",
        reasoning_framework=(
            "1. Review LATCH anchor locations and accessibility.\n"
            "2. Compare with FMVSS 225 requirements for anchor strength and spacing.\n"
            "3. Assess compatibility with common child safety seat models.\n"
            "4. Examine user manual instructions for installation clarity.\n"
            "5. Synthesize findings to determine compliance and compatibility."
        ),
        key_factors=[
            "Anchor location and strength",
            "Compatibility with child seats",
            "Installation instructions",
            "Regulatory compliance",
            "User feedback"
        ],
        primary_authority=[
            "FMVSS 225",
            "NHTSA LATCH Test Reports",
            "OEM User Manuals"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="LATCH system was incompatible or difficult to use.",
        counter_arguments=[
            "Anchor spacing was non-compliant.",
            "Installation instructions were unclear.",
            "Compatibility issues with common seats."
        ],
        resolution_strategy="Compare LATCH system design and user manuals with FMVSS 225 and field feedback.",
        entity_scope="AUTO15 LATCH System",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NHTSA LATCH Compliance 2016"
    ),
    DoctrineBlock(
        topic="Daytime Running Lights (DRL) and Rear-End Collision Visibility",
        keywords=["DRL", "daytime running lights", "rear-end collision", "visibility", "lighting"],
        conclusion_template="DRL must enhance vehicle visibility and reduce rear-end collision risk as required by FMVSS 108.",
        reasoning_framework=(
            "1. Review DRL design and activation logic.\n"
            "2. Compare with FMVSS 108 requirements for intensity and coverage.\n"
            "3. Assess crash data for rear-end collision rates with DRL active.\n"
            "4. Examine any recalls or field reports of DRL failures.\n"
            "5. Synthesize findings to determine compliance and effectiveness."
        ),
        key_factors=[
            "DRL intensity and coverage",
            "Activation logic",
            "Rear-end collision data",
            "Regulatory compliance",
            "Lighting system reliability"
        ],
        primary_authority=[
            "FMVSS 108",
            "NHTSA DRL Test Reports",
            "OEM Lighting Specifications"
        ],
        burden_holder="Plaintiff (alleging inadequate visibility)",
        adversary_position="DRL met all regulatory requirements and performed as designed.",
        counter_arguments=[
            "DRL intensity was insufficient.",
            "System failed to activate as required.",
            "Design did not reduce collision risk."
        ],
        resolution_strategy="Compare DRL design and crash data with FMVSS 108 and OEM standards.",
        entity_scope="AUTO15 Lighting System",
        confidence=0.84,
        confidence_zone="Moderate-High",
        controlling_precedent="NHTSA DRL Assessment 2018"
    ),
    DoctrineBlock(
        topic="Backup Camera and Rear Visibility Standards FMVSS 111",
        keywords=["backup camera", "rear visibility", "FMVSS 111", "display", "detection"],
        conclusion_template="Backup camera system must meet FMVSS 111 requirements for field of view and image quality.",
        reasoning_framework=(
            "1. Review backup camera field of view and image quality specifications.\n"
            "2. Compare with FMVSS 111 requirements for coverage and display.\n"
            "3. Assess system response time and user interface.\n"
            "4. Examine any recalls or field reports of camera failures.\n"
            "5. Synthesize findings to determine compliance and effectiveness."
        ),
        key_factors=[
            "Field of view coverage",
            "Image quality",
            "System response time",
            "User interface",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 111",
            "NHTSA Backup Camera Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="Backup camera did not meet FMVSS 111 requirements.",
        counter_arguments=[
            "Field of view was insufficient.",
            "Image quality was inadequate.",
            "System response was delayed."
        ],
        resolution_strategy="Compare camera specifications and test results with FMVSS 111 and OEM standards.",
        entity_scope="AUTO15 Backup Camera System",
        confidence=0.92,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Backup Camera Compliance 2019"
    ),
    DoctrineBlock(
        topic="Knee Airbag Deployment and Lower Extremity Injury",
        keywords=["knee airbag", "deployment", "lower extremity", "injury", "FMVSS 208"],
        conclusion_template="Knee airbags must deploy as required to mitigate lower extremity injury risk in frontal crashes.",
        reasoning_framework=(
            "1. Review crash data for knee airbag deployment signals and timing.\n"
            "2. Compare with FMVSS 208 requirements for lower extremity protection.\n"
            "3. Assess occupant injury data for lower limb injuries.\n"
            "4. Examine any recalls or field reports of knee airbag failures.\n"
            "5. Synthesize findings to determine compliance and injury mitigation adequacy."
        ),
        key_factors=[
            "Deployment timing",
            "Occupant injury data",
            "Regulatory compliance",
            "Crash severity",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 208",
            "NHTSA Knee Airbag Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging non-deployment or injury)",
        adversary_position="Knee airbag performed within design and regulatory limits.",
        counter_arguments=[
            "Deployment was delayed or absent.",
            "System defect or calibration error.",
            "Design did not mitigate injury risk."
        ],
        resolution_strategy="Compare crash data and injury outcomes with FMVSS 208 and OEM standards.",
        entity_scope="AUTO15 Knee Airbag System",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="NHTSA Knee Airbag Compliance 2017"
    ),
    DoctrineBlock(
        topic="Post-Crash Fuel System Integrity and Fire Risk FMVSS 301",
        keywords=["fuel system", "post-crash", "fire risk", "FMVSS 301", "integrity"],
        conclusion_template="Fuel system must maintain integrity and prevent fire risk after crash as required by FMVSS 301.",
        reasoning_framework=(
            "1. Review crash reconstruction for impact to fuel system components.\n"
            "2. Compare with FMVSS 301 requirements for fuel leakage and fire risk.\n"
            "3. Assess post-crash inspection for fuel leaks or ignition sources.\n"
            "4. Examine any recalls or field reports of post-crash fires.\n"
            "5. Synthesize findings to determine compliance and risk mitigation."
        ),
        key_factors=[
            "Fuel system integrity",
            "Post-crash leakage",
            "Fire ignition sources",
            "Regulatory compliance",
            "Crash severity"
        ],
        primary_authority=[
            "FMVSS 301",
            "NHTSA Fuel System Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging post-crash fire risk)",
        adversary_position="Fuel system met all regulatory requirements and performed as designed.",
        counter_arguments=[
            "Fuel leakage exceeded limits.",
            "Design did not prevent ignition.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare post-crash inspection and test results with FMVSS 301 and OEM standards.",
        entity_scope="AUTO15 Fuel System",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="NHTSA Fuel System Compliance 2018"
    ),
    # Additional doctrines for a total of 40+
    DoctrineBlock(
        topic="Side Airbag Out-of-Position Suppression",
        keywords=["side airbag", "out-of-position", "suppression", "occupant", "FMVSS 214"],
        conclusion_template="Side airbags must suppress deployment when occupants are out of position to prevent injury.",
        reasoning_framework=(
            "1. Review occupant position sensors and suppression logic.\n"
            "2. Compare with FMVSS 214 requirements for out-of-position protection.\n"
            "3. Assess crash data for side airbag deployment in out-of-position scenarios.\n"
            "4. Examine any recalls or field reports of suppression failures.\n"
            "5. Synthesize findings to determine compliance and injury mitigation."
        ),
        key_factors=[
            "Occupant position detection",
            "Suppression logic accuracy",
            "Deployment events",
            "Regulatory compliance",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 214",
            "NHTSA Side Airbag Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="Side airbag deployed in out-of-position scenario causing injury.",
        counter_arguments=[
            "Suppression logic failed.",
            "Sensor misclassification.",
            "Design did not prevent injury."
        ],
        resolution_strategy="Compare crash data and system diagnostics with FMVSS 214 and OEM standards.",
        entity_scope="AUTO15 Side Airbag System",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NHTSA Side Airbag Compliance 2017"
    ),
    DoctrineBlock(
        topic="Driver Monitoring System (DMS) Effectiveness",
        keywords=["driver monitoring", "DMS", "drowsiness", "distraction", "alert"],
        conclusion_template="DMS must effectively detect driver drowsiness and distraction and issue timely alerts.",
        reasoning_framework=(
            "1. Review DMS sensor data for detection of drowsiness and distraction events.\n"
            "2. Compare with Euro NCAP DMS test protocols for alert timing and accuracy.\n"
            "3. Assess user manual disclosures for system limitations.\n"
            "4. Examine any field reports or recalls related to DMS failures.\n"
            "5. Synthesize findings to determine effectiveness and compliance."
        ),
        key_factors=[
            "Detection accuracy",
            "Alert timing",
            "User manual disclosures",
            "System limitations",
            "Regulatory test protocols"
        ],
        primary_authority=[
            "Euro NCAP DMS Protocol",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging DMS failure)",
        adversary_position="DMS performed within design and disclosed limitations.",
        counter_arguments=[
            "System failed to detect drowsiness/distraction.",
            "Alert timing was inadequate.",
            "Limitations were not disclosed."
        ],
        resolution_strategy="Compare DMS logs and test results with regulatory protocols and OEM standards.",
        entity_scope="AUTO15 DMS",
        confidence=0.82,
        confidence_zone="Moderate-High",
        controlling_precedent="Euro NCAP DMS Assessment 2021"
    ),
    DoctrineBlock(
        topic="Automatic High Beam (AHB) System Performance",
        keywords=["automatic high beam", "AHB", "performance", "lighting", "visibility"],
        conclusion_template="AHB must switch between high and low beams to optimize visibility without dazzling other road users.",
        reasoning_framework=(
            "1. Review AHB sensor and camera data for detection of oncoming and leading vehicles.\n"
            "2. Compare with NHTSA and IIHS AHB test protocols for switching accuracy and timing.\n"
            "3. Assess user manual disclosures for system limitations.\n"
            "4. Examine any field reports or recalls related to AHB failures.\n"
            "5. Synthesize findings to determine performance and compliance."
        ),
        key_factors=[
            "Detection accuracy",
            "Switching timing",
            "User manual disclosures",
            "System limitations",
            "Regulatory test protocols"
        ],
        primary_authority=[
            "NHTSA AHB Test Protocol",
            "IIHS AHB Assessment",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging AHB failure)",
        adversary_position="AHB performed within design and disclosed limitations.",
        counter_arguments=[
            "System failed to switch beams appropriately.",
            "Detection accuracy was insufficient.",
            "Limitations were not disclosed."
        ],
        resolution_strategy="Compare AHB logs and test results with regulatory protocols and OEM standards.",
        entity_scope="AUTO15 AHB System",
        confidence=0.81,
        confidence_zone="Moderate",
        controlling_precedent="IIHS AHB Assessment 2019"
    ),
    DoctrineBlock(
        topic="Emergency Call (eCall) System Activation and Reliability",
        keywords=["eCall", "emergency call", "activation", "reliability", "crash"],
        conclusion_template="eCall system must reliably activate and transmit emergency data in crash events.",
        reasoning_framework=(
            "1. Review eCall activation logs and crash event correlation.\n"
            "2. Assess system diagnostics for communication failures.\n"
            "3. Compare with EU eCall Regulation (EU) 2015/758 requirements.\n"
            "4. Examine any field reports or recalls related to eCall failures.\n"
            "5. Synthesize findings to determine reliability and compliance."
        ),
        key_factors=[
            "Activation timing",
            "Data transmission reliability",
            "System diagnostics",
            "Regulatory compliance",
            "Crash severity"
        ],
        primary_authority=[
            "EU eCall Regulation (EU) 2015/758",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging eCall failure)",
        adversary_position="eCall performed within design and regulatory requirements.",
        counter_arguments=[
            "System failed to activate in qualifying crash.",
            "Data transmission was unreliable.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare activation logs and system diagnostics with regulatory and OEM standards.",
        entity_scope="AUTO15 eCall System",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="EU eCall Compliance 2018"
    ),
    DoctrineBlock(
        topic="Rear Seat Belt Reminder System Compliance",
        keywords=["rear seat belt", "reminder", "compliance", "FMVSS 208", "alert"],
        conclusion_template="Rear seat belt reminder system must comply with FMVSS 208 for alert timing and occupant detection.",
        reasoning_framework=(
            "1. Review system logs for rear seat occupancy and reminder activation.\n"
            "2. Compare with FMVSS 208 requirements for alert timing and duration.\n"
            "3. Assess user manual disclosures for system operation.\n"
            "4. Examine any field reports or recalls related to reminder failures.\n"
            "5. Synthesize findings to determine compliance and effectiveness."
        ),
        key_factors=[
            "Occupant detection accuracy",
            "Alert timing and duration",
            "User manual disclosures",
            "Regulatory compliance",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 208",
            "NHTSA Seat Belt Reminder Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="Reminder system failed to alert or detect occupants.",
        counter_arguments=[
            "System failed to detect rear seat occupancy.",
            "Alert timing was inadequate.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare system logs and test results with FMVSS 208 and OEM standards.",
        entity_scope="AUTO15 Seat Belt Reminder System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NHTSA Seat Belt Reminder Compliance 2019"
    ),
    DoctrineBlock(
        topic="Power Window Auto-Reverse and Pinch Protection",
        keywords=["power window", "auto-reverse", "pinch protection", "FMVSS 118", "injury"],
        conclusion_template="Power window auto-reverse must activate to prevent injury as required by FMVSS 118.",
        reasoning_framework=(
            "1. Review system logs for auto-reverse activation events.\n"
            "2. Compare with FMVSS 118 requirements for force and response time.\n"
            "3. Assess user manual disclosures for system operation.\n"
            "4. Examine any field reports or recalls related to auto-reverse failures.\n"
            "5. Synthesize findings to determine compliance and injury mitigation."
        ),
        key_factors=[
            "Activation force and timing",
            "System diagnostics",
            "User manual disclosures",
            "Regulatory compliance",
            "Injury reports"
        ],
        primary_authority=[
            "FMVSS 118",
            "NHTSA Power Window Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging auto-reverse failure)",
        adversary_position="Auto-reverse performed within design and regulatory requirements.",
        counter_arguments=[
            "System failed to reverse on obstruction.",
            "Activation force exceeded limits.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare activation logs and test results with FMVSS 118 and OEM standards.",
        entity_scope="AUTO15 Power Window System",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="NHTSA Power Window Compliance 2017"
    ),
    DoctrineBlock(
        topic="Steering Column Collapse and Driver Injury Mitigation",
        keywords=["steering column", "collapse", "driver injury", "FMVSS 204", "frontal crash"],
        conclusion_template="Steering column must collapse as required by FMVSS 204 to mitigate driver injury in frontal crashes.",
        reasoning_framework=(
            "1. Review crash data for steering column collapse event and timing.\n"
            "2. Compare with FMVSS 204 requirements for column displacement.\n"
            "3. Assess injury data for driver lower extremity and thoracic injuries.\n"
            "4. Examine any recalls or field reports of steering column failures.\n"
            "5. Synthesize findings to determine compliance and injury mitigation."
        ),
        key_factors=[
            "Column collapse timing",
            "Displacement measurements",
            "Driver injury data",
            "Regulatory compliance",
            "Crash severity"
        ],
        primary_authority=[
            "FMVSS 204",
            "NHTSA Steering Column Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging inadequate collapse or injury)",
        adversary_position="Steering column performed within design and regulatory requirements.",
        counter_arguments=[
            "Collapse timing was delayed.",
            "Displacement was insufficient.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare crash data and injury outcomes with FMVSS 204 and OEM standards.",
        entity_scope="AUTO15 Steering Column System",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NHTSA Steering Column Compliance 2018"
    ),
    DoctrineBlock(
        topic="Electronic Parking Brake (EPB) Failure Modes",
        keywords=["electronic parking brake", "EPB", "failure", "diagnostics", "FMVSS 135"],
        conclusion_template="EPB must engage and hold vehicle as required by FMVSS 135; failures must be diagnosed and addressed.",
        reasoning_framework=(
            "1. Review EPB activation logs and holding force measurements.\n"
            "2. Compare with FMVSS 135 requirements for parking brake performance.\n"
            "3. Assess system diagnostics for faults or error codes.\n"
            "4. Examine any recalls or field reports related to EPB failures.\n"
            "5. Synthesize findings to determine compliance and reliability."
        ),
        key_factors=[
            "Holding force",
            "Activation logs",
            "System diagnostics",
            "Regulatory compliance",
            "Field reports"
        ],
        primary_authority=[
            "FMVSS 135",
            "NHTSA Parking Brake Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging EPB failure)",
        adversary_position="EPB performed within design and regulatory requirements.",
        counter_arguments=[
            "Holding force was insufficient.",
            "System failed to engage or disengage.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare activation logs and holding force with FMVSS 135 and OEM standards.",
        entity_scope="AUTO15 EPB System",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="NHTSA EPB Compliance 2019"
    ),
    DoctrineBlock(
        topic="Automatic Door Lock and Unlock Logic",
        keywords=["automatic door lock", "unlock", "logic", "child safety", "FMVSS 206"],
        conclusion_template="Automatic door lock/unlock logic must comply with FMVSS 206 and ensure occupant egress in emergencies.",
        reasoning_framework=(
            "1. Review system logic for automatic locking and unlocking events.\n"
            "2. Compare with FMVSS 206 requirements for door latch and egress.\n"
            "3. Assess user manual disclosures for system operation.\n"
            "4. Examine any field reports or recalls related to locking failures.\n"
            "5. Synthesize findings to determine compliance and occupant safety."
        ),
        key_factors=[
            "Lock/unlock timing",
            "Egress capability",
            "User manual disclosures",
            "Regulatory compliance",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 206",
            "NHTSA Door Latch Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="Automatic logic prevented occupant egress in emergency.",
        counter_arguments=[
            "Unlock logic failed in crash.",
            "System defect or improper maintenance.",
            "User manual disclosures were inadequate."
        ],
        resolution_strategy="Compare system logic and test results with FMVSS 206 and OEM standards.",
        entity_scope="AUTO15 Door Lock System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NHTSA Door Latch Compliance 2018"
    ),
    DoctrineBlock(
        topic="Occupant Ejection Mitigation in Side Crashes",
        keywords=["occupant ejection", "side crash", "curtain airbag", "FMVSS 226", "injury"],
        conclusion_template="Curtain airbags and side glazing must work together to mitigate occupant ejection in side crashes as required by FMVSS 226.",
        reasoning_framework=(
            "1. Review crash data for curtain airbag deployment and side glazing integrity.\n"
            "2. Compare with FMVSS 226 requirements for ejection mitigation.\n"
            "3. Assess occupant kinematics and injury data.\n"
            "4. Examine any recalls or field reports of ejection events.\n"
            "5. Synthesize findings to determine compliance and injury mitigation."
        ),
        key_factors=[
            "Curtain airbag deployment",
            "Side glazing integrity",
            "Occupant kinematics",
            "Regulatory compliance",
            "Crash severity"
        ],
        primary_authority=[
            "FMVSS 226",
            "NHTSA Ejection Mitigation Test Reports",
            "OEM Service Manuals"
        ],
        burden_holder="Plaintiff (alleging ejection or injury)",
        adversary_position="Ejection mitigation features performed within regulatory requirements.",
        counter_arguments=[
            "Curtain airbag failed to deploy.",
            "Side glazing failed to retain occupant.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare crash data and injury outcomes with FMVSS 226 and OEM standards.",
        entity_scope="AUTO15 Side Ejection Mitigation",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="NHTSA Ejection Mitigation Compliance 2019"
    ),
    DoctrineBlock(
        topic="Pedal Misapplication and Brake Override System",
        keywords=["pedal misapplication", "brake override", "unintended acceleration", "diagnostics", "FMVSS 124"],
        conclusion_template="Brake override system must intervene in pedal misapplication scenarios to prevent unintended acceleration.",
        reasoning_framework=(
            "1. Review event logs for simultaneous accelerator and brake pedal application.\n"
            "2. Compare with FMVSS 124 requirements for brake override logic.\n"
            "3. Assess system diagnostics for faults or suppression events.\n"
            "4. Examine any field reports or recalls related to brake override failures.\n"
            "5. Synthesize findings to determine compliance and intervention adequacy."
        ),
        key_factors=[
            "Event log analysis",
            "Override logic performance",
            "System diagnostics",
            "Regulatory compliance",
            "Field reports"
        ],
        primary_authority=[
            "FMVSS 124",
            "NHTSA Unintended Acceleration Reports",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging override failure)",
        adversary_position="Brake override performed within design and regulatory requirements.",
        counter_arguments=[
            "System failed to intervene.",
            "Override logic was suppressed.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare event logs and system diagnostics with FMVSS 124 and OEM standards.",
        entity_scope="AUTO15 Brake Override System",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="NHTSA Brake Override Compliance 2017"
    ),
    DoctrineBlock(
        topic="Automatic Transmission Park Interlock Function",
        keywords=["automatic transmission", "park interlock", "FMVSS 114", "rollaway", "safety"],
        conclusion_template="Park interlock must prevent vehicle rollaway as required by FMVSS 114.",
        reasoning_framework=(
            "1. Review system logs for park interlock activation and override events.\n"
            "2. Compare with FMVSS 114 requirements for rollaway prevention.\n"
            "3. Assess user manual disclosures for system operation.\n"
            "4. Examine any field reports or recalls related to park interlock failures.\n"
            "5. Synthesize findings to determine compliance and reliability."
        ),
        key_factors=[
            "Activation and override events",
            "System diagnostics",
            "User manual disclosures",
            "Regulatory compliance",
            "Field reports"
        ],
        primary_authority=[
            "FMVSS 114",
            "NHTSA Park Interlock Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="Park interlock failed to prevent rollaway.",
        counter_arguments=[
            "System failed to engage.",
            "Override logic was improperly triggered.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare system logs and test results with FMVSS 114 and OEM standards.",
        entity_scope="AUTO15 Park Interlock System",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NHTSA Park Interlock Compliance 2018"
    ),
    DoctrineBlock(
        topic="Windshield Wiper System Performance and Visibility",
        keywords=["windshield wiper", "performance", "visibility", "FMVSS 104", "rain"],
        conclusion_template="Windshield wiper system must ensure adequate visibility in rain as required by FMVSS 104.",
        reasoning_framework=(
            "1. Review wiper activation logs and speed settings.\n"
            "2. Compare with FMVSS 104 requirements for wipe area and performance.\n"
            "3. Assess user manual disclosures for system operation.\n"
            "4. Examine any field reports or recalls related to wiper failures.\n"
            "5. Synthesize findings to determine compliance and effectiveness."
        ),
        key_factors=[
            "Wipe area coverage",
            "Activation speed",
            "System diagnostics",
            "Regulatory compliance",
            "Field reports"
        ],
        primary_authority=[
            "FMVSS 104",
            "NHTSA Wiper Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging inadequate visibility)",
        adversary_position="Wiper system performed within design and regulatory requirements.",
        counter_arguments=[
            "Wipe area was insufficient.",
            "Activation speed was inadequate.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare activation logs and test results with FMVSS 104 and OEM standards.",
        entity_scope="AUTO15 Wiper System",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="NHTSA Wiper Compliance 2017"
    ),
    DoctrineBlock(
        topic="Electronic Throttle Control (ETC) Fail-Safe Logic",
        keywords=["electronic throttle control", "ETC", "fail-safe", "diagnostics", "FMVSS 124"],
        conclusion_template="ETC must enter fail-safe mode in the event of sensor or actuator failure as required by FMVSS 124.",
        reasoning_framework=(
            "1. Review ETC system diagnostics for sensor and actuator faults.\n"
            "2. Compare with FMVSS 124 requirements for fail-safe logic.\n"
            "3. Assess event logs for fail-safe mode activation.\n"
            "4. Examine any field reports or recalls related to ETC failures.\n"
            "5. Synthesize findings to determine compliance and reliability."
        ),
        key_factors=[
            "Sensor and actuator diagnostics",
            "Fail-safe mode activation",
            "System reliability",
            "Regulatory compliance",
            "Field reports"
        ],
        primary_authority=[
            "FMVSS 124",
            "NHTSA ETC Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging ETC failure)",
        adversary_position="ETC performed within design and regulatory requirements.",
        counter_arguments=[
            "System failed to enter fail-safe mode.",
            "Sensor/actuator diagnostics were inadequate.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare diagnostics and event logs with FMVSS 124 and OEM standards.",
        entity_scope="AUTO15 ETC System",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="NHTSA ETC Compliance 2018"
    ),
    DoctrineBlock(
        topic="Rear Seat Occupant Alert System",
        keywords=["rear seat", "occupant alert", "child safety", "reminder", "FMVSS 208"],
        conclusion_template="Rear seat occupant alert system must remind drivers to check rear seats for children or pets as required by FMVSS 208.",
        reasoning_framework=(
            "1. Review system logs for rear seat occupancy detection and alert events.\n"
            "2. Compare with FMVSS 208 requirements for alert timing and duration.\n"
            "3. Assess user manual disclosures for system operation.\n"
            "4. Examine any field reports or recalls related to alert failures.\n"
            "5. Synthesize findings to determine compliance and effectiveness."
        ),
        key_factors=[
            "Occupancy detection accuracy",
            "Alert timing and duration",
            "User manual disclosures",
            "Regulatory compliance",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 208",
            "NHTSA Rear Seat Alert Test Reports",
            "OEM System Specifications"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="Alert system failed to detect or alert for rear seat occupants.",
        counter_arguments=[
            "System failed to detect occupancy.",
            "Alert timing was inadequate.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare system logs and test results with FMVSS 208 and OEM standards.",
        entity_scope="AUTO15 Rear Seat Alert System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NHTSA Rear Seat Alert Compliance 2020"
    ),
    DoctrineBlock(
        topic="Front Camera Sensor Cleaning and Performance",
        keywords=["front camera", "sensor", "cleaning", "performance", "AEB"],
        conclusion_template="Front camera sensor cleaning system must maintain sensor performance for AEB and LDW functionality.",
        reasoning_framework=(
            "1. Review sensor cleaning system activation logs and intervals.\n"
            "2. Assess impact of sensor contamination on AEB and LDW performance.\n"
            "3. Compare with OEM guidelines for sensor maintenance.\n"
            "4. Examine any field reports or recalls related to sensor cleaning failures.\n"
            "5. Synthesize findings to determine effectiveness and compliance."
        ),
        key_factors=[
            "Cleaning system activation",
            "Sensor performance",
            "AEB and LDW functionality",
            "OEM maintenance guidelines",
            "Field reports"
        ],
        primary_authority=[
            "OEM System Specifications",
            "NHTSA AEB/LDW Test Reports"
        ],
        burden_holder="Plaintiff (alleging sensor performance loss)",
        adversary_position="Sensor cleaning system performed within design and maintenance requirements.",
        counter_arguments=[
            "System failed to clean sensor.",
            "Sensor performance was degraded.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare activation logs and performance data with OEM guidelines.",
        entity_scope="AUTO15 Front Camera System",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="NHTSA AEB/LDW Sensor Assessment 2019"
    ),
    DoctrineBlock(
        topic="Vehicle Cybersecurity and Safety-Critical Systems",
        keywords=["cybersecurity", "safety-critical", "system", "vulnerability", "ISO/SAE 21434"],
        conclusion_template="Safety-critical systems must be protected from cybersecurity threats as required by ISO/SAE 21434.",
        reasoning_framework=(
            "1. Review system architecture for safety-critical network segmentation.\n"
            "2. Assess implementation of security controls and intrusion detection.\n"
            "3. Compare with ISO/SAE 21434 requirements for threat assessment and risk analysis.\n"
            "4. Examine any field reports or recalls related to cybersecurity vulnerabilities.\n"
            "5. Synthesize findings to determine adequacy of cybersecurity measures."
        ),
        key_factors=[
            "Network segmentation",
            "Security controls",
            "Intrusion detection",
            "Regulatory compliance",
            "Field reports"
        ],
        primary_authority=[
            "ISO/SAE 21434",
            "NHTSA Cybersecurity Best Practices",
            "OEM Security Documentation"
        ],
        burden_holder="Manufacturer (demonstrating compliance)",
        adversary_position="Cybersecurity measures were inadequate to protect safety-critical systems.",
        counter_arguments=[
            "Network was not properly segmented.",
            "Security controls were insufficient.",
            "Vulnerabilities were not addressed."
        ],
        resolution_strategy="Compare system architecture and controls with ISO/SAE 21434 and NHTSA best practices.",
        entity_scope="AUTO15 Safety-Critical Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO/SAE 21434 Implementation 2021"
    ),
    DoctrineBlock(
        topic="High Voltage Battery Isolation in Post-Crash Events",
        keywords=["high voltage battery", "isolation", "post-crash", "electric vehicle", "fire risk"],
        conclusion_template="High voltage battery must isolate automatically in post-crash events to prevent fire risk.",
        reasoning_framework=(
            "1. Review crash data for high voltage battery isolation signals and timing.\n"
            "2. Compare with SAE J2929 and OEM requirements for isolation.\n"
            "3. Assess post-crash inspection for battery integrity and fire risk.\n"
            "4. Examine any field reports or recalls related to battery isolation failures.\n"
            "5. Synthesize findings to determine compliance and risk mitigation."
        ),
        key_factors=[
            "Isolation timing",
            "Battery integrity",
            "Fire risk",
            "Regulatory compliance",
            "Crash severity"
        ],
        primary_authority=[
            "SAE J2929",
            "NHTSA EV Safety Reports",
            "OEM System Specifications"
        ],
        burden_holder="Plaintiff (alleging isolation failure or fire risk)",
        adversary_position="Battery isolation performed within design and regulatory requirements.",
        counter_arguments=[
            "Isolation was delayed or absent.",
            "Battery integrity was compromised.",
            "System defect or improper maintenance."
        ],
        resolution_strategy="Compare crash data and post-crash inspection with SAE J2929 and OEM standards.",
        entity_scope="AUTO15 High Voltage Battery System",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NHTSA EV Safety Compliance 2020"
    ),
    DoctrineBlock(
        topic="Event Data Recorder (EDR) Privacy and Data Access",
        keywords=["event data recorder", "EDR", "privacy", "data access", "legal"],
        conclusion_template="EDR data access must comply with privacy laws and user consent requirements.",
        reasoning_framework=(
            "1. Review data access logs and user consent documentation.\n"
            "2. Compare with federal and state privacy laws regarding EDR data.\n"
            "3. Assess OEM user manual disclosures for data access and privacy.\n"
            "4. Examine any field reports or legal cases related to unauthorized access.\n"
            "5. Synthesize findings to determine compliance and privacy protection."
        ),
        key_factors=[
            "User consent documentation",
            "Data access logs",
            "Privacy law compliance",
            "User manual disclosures",
            "Legal precedents"
        ],
        primary_authority=[
            "Driver Privacy Act of 2015",
            "State Privacy Laws",
            "OEM User Manuals"
        ],
        burden_holder="Data accessor (demonstrating lawful access)",
        adversary_position="EDR data was accessed without proper consent or legal authority.",
        counter_arguments=[
            "User consent was not obtained.",
            "Access was unauthorized.",
            "Privacy disclosures were inadequate."
        ],
        resolution_strategy="Compare access logs and consent documentation with privacy laws and OEM disclosures.",
        entity_scope="AUTO15 EDR System",
        confidence=0.92,
        confidence_zone="Very High",
        controlling_precedent="Driver Privacy Act of 2015"
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