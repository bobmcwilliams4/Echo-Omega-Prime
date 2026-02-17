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
        topic="Locomotive Prime Mover Overhaul Cycles",
        keywords=[
            "prime mover", "overhaul", "cycle", "locomotive", "maintenance", "engine hours", "FRA", "OEM", "AAR"
        ],
        conclusion_template="Locomotive prime movers must undergo major overhaul every 184,000 engine hours or 10 years, whichever comes first, unless condition-based evidence supports extension.",
        reasoning_framework="""
Prime mover overhaul intervals are established based on OEM recommendations, historical failure data, and regulatory mandates (FRA 49 CFR 229.23). The 184,000-hour/10-year standard reflects a balance between risk of catastrophic failure and operational cost. Condition-based evidence (e.g., oil analysis, vibration data) may justify extending intervals, but must be documented and defensible. Deviations require engineering justification and risk assessment. The burden is on the operator to demonstrate equivalent safety.
""",
        key_factors=[
            "Engine hour meter accuracy",
            "OEM recommendations",
            "FRA 49 CFR 229.23 compliance",
            "Condition-based monitoring results",
            "Maintenance records"
        ],
        primary_authority=[
            "FRA 49 CFR 229.23",
            "AAR Manual of Standards and Recommended Practices (MSRP)",
            "OEM Maintenance Manuals"
        ],
        burden_holder="Railroad operator",
        adversary_position="Overhaul intervals can be extended indefinitely with sufficient condition-based evidence.",
        counter_arguments=[
            "Condition-based evidence may be incomplete or subject to interpretation.",
            "Regulatory authorities may not accept extended intervals without robust data.",
            "Unexpected failures can have catastrophic consequences."
        ],
        resolution_strategy="Require documented engineering analysis and regulatory notification for overhaul interval extensions.",
        entity_scope="Locomotives with diesel-electric prime movers in freight service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA 49 CFR 229.23"
    ),
    DoctrineBlock(
        topic="Wheel Impact Load Detector (WILD) Response and Wheel Condemning Limits",
        keywords=[
            "WILD", "wheel impact", "condemning limit", "AAR", "FRA", "maintenance", "inspection", "freight car"
        ],
        conclusion_template="Any wheel registering a WILD reading above 90 kips must be removed at the next terminal; wheels above 80 kips require immediate inspection and possible removal per AAR Rule 41.",
        reasoning_framework="""
WILD systems are designed to detect wheels with high impact forces, which are correlated with defects such as flat spots or shelling. The AAR sets condemning limits at 90 kips (Rule 41), with 80-89 kips requiring further inspection. FRA 49 CFR 215.103 mandates removal of wheels with defects. The doctrine prioritizes safety and prevention of rail damage. The operator must act promptly upon WILD alerts, document actions, and ensure compliance with both AAR and FRA requirements.
""",
        key_factors=[
            "WILD system calibration",
            "Impact reading thresholds",
            "AAR Rule 41 compliance",
            "FRA 49 CFR 215.103",
            "Inspection documentation"
        ],
        primary_authority=[
            "AAR Field Manual Rule 41",
            "FRA 49 CFR 215.103"
        ],
        burden_holder="Railroad operator",
        adversary_position="WILD readings are only advisory and do not require mandatory action.",
        counter_arguments=[
            "Ignoring high WILD readings increases risk of derailment.",
            "AAR and FRA rules require action on high-impact wheels.",
            "Failure to act can result in regulatory penalties."
        ],
        resolution_strategy="Mandate removal or inspection per established thresholds and document all actions.",
        entity_scope="All freight cars equipped with steel wheels",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAR Rule 41"
    ),
    DoctrineBlock(
        topic="Air Brake Testing Requirements - Class I/IA/III Freight Car Inspections",
        keywords=[
            "air brake", "Class I", "Class IA", "Class III", "FRA", "brake test", "freight car", "inspection"
        ],
        conclusion_template="Class I brake tests are required at initial terminal or every 1,000 miles; Class IA tests at 500 miles; Class III tests at crew change or pick-up/set-out events.",
        reasoning_framework="""
Air brake testing is governed by FRA 49 CFR 232.205 and 232.209. Class I tests are the most comprehensive and must be performed at the initial terminal or every 1,000 miles. Class IA tests are required at 500-mile intervals, and Class III tests at crew changes or when cars are added/removed. Proper documentation and adherence to intervals are critical for safety and regulatory compliance. Failure to perform required tests can result in enforcement actions.
""",
        key_factors=[
            "Test interval tracking",
            "Proper test procedures",
            "Documentation",
            "Crew training",
            "FRA audit readiness"
        ],
        primary_authority=[
            "FRA 49 CFR 232.205",
            "FRA 49 CFR 232.209"
        ],
        burden_holder="Railroad operator",
        adversary_position="Class I tests can be skipped if recent Class IA or III tests were performed.",
        counter_arguments=[
            "Each class of test has specific requirements and cannot substitute for others.",
            "Skipping tests increases risk of brake failure.",
            "FRA regulations are explicit on test intervals."
        ],
        resolution_strategy="Enforce strict adherence to test intervals and maintain audit-ready records.",
        entity_scope="All freight cars in interchange service",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="FRA 49 CFR 232.205"
    ),
    DoctrineBlock(
        topic="Journal Bearing Hot Box Detection and Failure Prevention",
        keywords=[
            "journal bearing", "hot box", "failure prevention", "detection", "wayside detector", "maintenance"
        ],
        conclusion_template="Journal bearings exhibiting temperatures above 170°F above ambient or trending upward rapidly must be set out and inspected immediately.",
        reasoning_framework="""
Hot box detectors (HBD) monitor journal bearing temperatures to prevent failures that can lead to derailments. AAR and FRA guidelines set temperature thresholds for action (typically 170°F above ambient). Trending data is also critical; a rapid increase, even below threshold, warrants inspection. Operators must respond to HBD alerts, document findings, and remove defective bearings from service. Failure to act is a major safety risk.
""",
        key_factors=[
            "HBD calibration and reliability",
            "Temperature thresholds",
            "Trending analysis",
            "Inspection procedures",
            "Maintenance records"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 215.115"
        ],
        burden_holder="Railroad operator",
        adversary_position="Hot box alerts can be ignored if the train is not exhibiting operational issues.",
        counter_arguments=[
            "Bearing failures can occur suddenly and without warning.",
            "Regulations require action on HBD alerts.",
            "Ignoring alerts increases liability."
        ],
        resolution_strategy="Immediate inspection and set-out of cars with high or trending temperatures.",
        entity_scope="All freight cars with journal bearings",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Coupler Knuckle Inspection and Replacement Criteria",
        keywords=[
            "coupler", "knuckle", "inspection", "replacement", "AAR", "FRA", "freight car", "maintenance"
        ],
        conclusion_template="Coupler knuckles must be replaced if cracked, broken, or worn beyond 5/8 inch from the original contour per AAR Rule 21.",
        reasoning_framework="""
Coupler knuckles are critical for train integrity. AAR Rule 21 specifies that any knuckle with visible cracks, breaks, or wear exceeding 5/8 inch from the original contour must be replaced. FRA 49 CFR 215.121 reinforces these standards. Regular inspection is required during Class I/IA/III brake tests and at maintenance facilities. Proper documentation and use of AAR-approved replacement parts are mandatory.
""",
        key_factors=[
            "Visual inspection quality",
            "Wear measurement accuracy",
            "Replacement part certification",
            "Inspection intervals",
            "Maintenance records"
        ],
        primary_authority=[
            "AAR Field Manual Rule 21",
            "FRA 49 CFR 215.121"
        ],
        burden_holder="Railroad operator",
        adversary_position="Minor cracks or wear do not require immediate replacement.",
        counter_arguments=[
            "Small defects can propagate rapidly under load.",
            "AAR and FRA rules are explicit.",
            "Failure can result in train separation."
        ],
        resolution_strategy="Replace all non-conforming knuckles and document action.",
        entity_scope="All freight cars with AAR-standard couplers",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAR Rule 21"
    ),
    DoctrineBlock(
        topic="Tank Car Qualification - DOT-111 vs DOT-117 Standards",
        keywords=[
            "tank car", "DOT-111", "DOT-117", "qualification", "FRA", "PHMSA", "hazmat", "tank standards"
        ],
        conclusion_template="All tank cars transporting Class 3 flammable liquids must be retrofitted or built to DOT-117 standards by May 1, 2025.",
        reasoning_framework="""
The FAST Act and PHMSA HM-251 require that tank cars carrying Class 3 flammable liquids meet DOT-117 standards, which include enhanced shell thickness, thermal protection, and improved valves. DOT-111 cars must be retrofitted or removed from hazmat service by the deadline. FRA and PHMSA enforce compliance. Operators must track car qualifications, retrofit schedules, and ensure no non-compliant cars are loaded.
""",
        key_factors=[
            "Car type identification",
            "Retrofit documentation",
            "Commodity classification",
            "Regulatory deadlines",
            "Inspection records"
        ],
        primary_authority=[
            "PHMSA HM-251",
            "FRA 49 CFR 179.202-13",
            "FAST Act Section 7304"
        ],
        burden_holder="Tank car owner/operator",
        adversary_position="DOT-111 cars can remain in service if properly maintained.",
        counter_arguments=[
            "Regulations mandate phase-out for specific commodities.",
            "Non-compliance risks civil penalties.",
            "DOT-117 offers superior safety."
        ],
        resolution_strategy="Strict tracking and proactive retrofit/removal of non-compliant cars.",
        entity_scope="Tank cars transporting Class 3 flammable liquids",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="PHMSA HM-251"
    ),
    DoctrineBlock(
        topic="Traction Motor Inspection and Commutator Maintenance",
        keywords=[
            "traction motor", "commutator", "inspection", "maintenance", "locomotive", "AAR", "FRA"
        ],
        conclusion_template="Traction motors must be inspected every 92 days and commutators cleaned and undercut as needed to prevent flashover and arcing.",
        reasoning_framework="""
Traction motors are subject to electrical and mechanical wear. FRA 49 CFR 229.23 and AAR MSRP S-486 specify 92-day inspection intervals. Commutators must be checked for pitting, grooving, and carbon buildup; undercutting and cleaning are performed as needed. Failure to maintain commutators can result in flashover, arcing, and motor failure. Maintenance actions must be documented.
""",
        key_factors=[
            "Inspection interval compliance",
            "Commutator condition",
            "Cleaning/undercutting procedures",
            "Maintenance records",
            "Technician training"
        ],
        primary_authority=[
            "FRA 49 CFR 229.23",
            "AAR MSRP S-486"
        ],
        burden_holder="Locomotive owner/operator",
        adversary_position="Commutator maintenance can be deferred if no symptoms are present.",
        counter_arguments=[
            "Commutator degradation can be rapid and unpredictable.",
            "Regulations require periodic inspection.",
            "Deferred maintenance increases risk of failure."
        ],
        resolution_strategy="Enforce 92-day inspection intervals and condition-based maintenance.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA 49 CFR 229.23"
    ),
    DoctrineBlock(
        topic="Condition-Based Maintenance Using Vibration Analysis and Oil Sampling",
        keywords=[
            "condition-based maintenance", "vibration analysis", "oil sampling", "predictive maintenance", "locomotive", "freight car"
        ],
        conclusion_template="Vibration analysis and oil sampling must be performed at least annually; abnormal results require immediate engineering review and possible component replacement.",
        reasoning_framework="""
Condition-based maintenance leverages predictive diagnostics to identify emerging failures. Vibration analysis detects misalignment, imbalance, and bearing defects. Oil sampling reveals wear metals and contamination. AAR MSRP S-920 and OEM guidelines recommend annual testing, with more frequent intervals for high-utilization assets. Abnormal findings trigger engineering review and corrective action. Documentation supports regulatory compliance and warranty claims.
""",
        key_factors=[
            "Test interval adherence",
            "Diagnostic result interpretation",
            "Engineering review process",
            "Maintenance records",
            "Component replacement criteria"
        ],
        primary_authority=[
            "AAR MSRP S-920",
            "OEM Maintenance Manuals"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Predictive diagnostics are optional and not required for compliance.",
        counter_arguments=[
            "Condition-based maintenance reduces unplanned failures.",
            "AAR and OEMs recommend predictive diagnostics.",
            "Failure to act on abnormal findings increases risk."
        ],
        resolution_strategy="Integrate diagnostics into maintenance program and act on abnormal results.",
        entity_scope="Locomotives and freight cars in mainline service",
        confidence=0.95,
        confidence_zone="Medium-High",
        controlling_precedent="AAR MSRP S-920"
    ),
    DoctrineBlock(
        topic="Locomotive Fuel System Maintenance - Injector Testing and Cleaning",
        keywords=[
            "fuel system", "injector", "testing", "cleaning", "locomotive", "maintenance", "OEM", "FRA"
        ],
        conclusion_template="Fuel injectors must be tested for flow and spray pattern every 184,000 engine hours or 10 years, and cleaned or replaced as indicated by results.",
        reasoning_framework="""
Fuel injectors are critical for combustion efficiency and emissions control. OEMs specify test intervals aligned with overhaul cycles (typically 184,000 hours/10 years). Testing includes flow rate, spray pattern, and leakage. Cleaning or replacement is performed as indicated. Poor injector performance leads to increased fuel consumption, emissions, and potential engine damage. Maintenance actions must be documented for regulatory and warranty purposes.
""",
        key_factors=[
            "Injector test results",
            "Test interval compliance",
            "Cleaning/replacement procedures",
            "Maintenance records",
            "OEM specifications"
        ],
        primary_authority=[
            "OEM Maintenance Manuals",
            "FRA 49 CFR 229.23"
        ],
        burden_holder="Locomotive owner/operator",
        adversary_position="Injector maintenance can be deferred if no symptoms are present.",
        counter_arguments=[
            "Injector degradation may not be immediately apparent.",
            "OEMs require periodic testing.",
            "Deferred maintenance increases risk of engine damage."
        ],
        resolution_strategy="Test injectors at overhaul and act on abnormal results.",
        entity_scope="Diesel-electric locomotives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Manuals"
    ),
    DoctrineBlock(
        topic="Locomotive Cooling System Maintenance - Radiator and Coolant Management",
        keywords=[
            "cooling system", "radiator", "coolant", "maintenance", "locomotive", "OEM", "FRA"
        ],
        conclusion_template="Radiators must be inspected for leaks and blockages every 92 days; coolant must be tested for pH and freeze point at least annually.",
        reasoning_framework="""
Locomotive cooling systems prevent engine overheating. OEMs and FRA 49 CFR 229.23 require 92-day inspections for leaks, corrosion, and blockages. Coolant chemistry (pH, freeze point, inhibitor concentration) must be tested annually to prevent corrosion and freezing. Maintenance records support regulatory compliance and warranty claims. Failure to maintain cooling systems can result in engine damage and service interruptions.
""",
        key_factors=[
            "Inspection interval compliance",
            "Coolant chemistry test results",
            "Leak/blockage detection",
            "Maintenance records",
            "OEM recommendations"
        ],
        primary_authority=[
            "OEM Maintenance Manuals",
            "FRA 49 CFR 229.23"
        ],
        burden_holder="Locomotive owner/operator",
        adversary_position="Cooling system maintenance can be performed only when issues arise.",
        counter_arguments=[
            "Preventive maintenance reduces unplanned failures.",
            "OEMs and FRA require periodic inspection.",
            "Deferred maintenance increases risk of engine failure."
        ],
        resolution_strategy="Enforce inspection and testing intervals and act on abnormal findings.",
        entity_scope="Diesel-electric locomotives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Maintenance Manuals"
    ),
    DoctrineBlock(
        topic="Truck (Bogie) Frame Inspection and Crack Detection",
        keywords=[
            "truck frame", "bogie", "inspection", "crack detection", "AAR", "FRA", "freight car", "locomotive"
        ],
        conclusion_template="Truck frames must be visually inspected for cracks every 92 days and subjected to NDT (e.g., ultrasonic) at least every 5 years.",
        reasoning_framework="""
Truck (bogie) frames are subject to fatigue and cracking. AAR MSRP S-402 and FRA 49 CFR 229.23 require 92-day visual inspections and periodic non-destructive testing (NDT) every 5 years. Cracks must be documented and repaired or the frame replaced. Failure to detect cracks can result in catastrophic failure. Maintenance actions must be recorded for regulatory compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "NDT test results",
            "Crack documentation",
            "Repair/replacement procedures",
            "Maintenance records"
        ],
        primary_authority=[
            "AAR MSRP S-402",
            "FRA 49 CFR 229.23"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Crack detection is only necessary when visible damage is present.",
        counter_arguments=[
            "Fatigue cracks may not be visible.",
            "NDT is required for comprehensive detection.",
            "Regulations mandate periodic testing."
        ],
        resolution_strategy="Enforce inspection and NDT intervals and act on findings.",
        entity_scope="Locomotives and freight cars",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAR MSRP S-402"
    ),
    DoctrineBlock(
        topic="Safety Appliance Inspection - Ladders, Handholds, and Sill Steps",
        keywords=[
            "safety appliance", "ladder", "handhold", "sill step", "inspection", "AAR", "FRA", "freight car"
        ],
        conclusion_template="Ladders, handholds, and sill steps must be inspected for integrity and securement during every Class I/IA/III brake test and repaired or replaced if defective.",
        reasoning_framework="""
Safety appliances are critical for crew safety. FRA 49 CFR 231 and AAR Rule 90 require inspection of ladders, handholds, and sill steps during every brake test. Any loose, broken, or missing appliance must be repaired or replaced before the car is returned to service. Documentation supports regulatory compliance and safety audits.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Repair/replacement procedures",
            "Maintenance records",
            "Crew safety training"
        ],
        primary_authority=[
            "FRA 49 CFR 231",
            "AAR Field Manual Rule 90"
        ],
        burden_holder="Railroad operator",
        adversary_position="Minor defects in safety appliances can be deferred until next scheduled maintenance.",
        counter_arguments=[
            "Crew safety is paramount.",
            "Regulations require immediate action.",
            "Deferred repairs increase risk of injury."
        ],
        resolution_strategy="Inspect during every brake test and repair/replace as needed.",
        entity_scope="All freight cars",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="FRA 49 CFR 231"
    ),
    DoctrineBlock(
        topic="Freight Car Body Bolster Inspection and Replacement",
        keywords=[
            "body bolster", "inspection", "replacement", "AAR", "FRA", "freight car", "structural integrity"
        ],
        conclusion_template="Body bolsters must be inspected for cracks, corrosion, and deformation every 92 days; replacement is required if defects are found.",
        reasoning_framework="""
The body bolster is a critical structural component. AAR Rule 7 and FRA 49 CFR 215.121 require 92-day inspections for cracks, corrosion, and deformation. Any defect necessitates immediate replacement to maintain car integrity. Documentation of inspections and repairs is required for regulatory compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 7",
            "FRA 49 CFR 215.121"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor cracks or corrosion can be monitored without immediate replacement.",
        counter_arguments=[
            "Structural defects can propagate rapidly.",
            "Regulations require immediate action.",
            "Failure increases risk of failure."
        ],
        resolution_strategy="Replace defective bolsters and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 7"
    ),
    DoctrineBlock(
        topic="Brake Shoe and Pad Wear Limits",
        keywords=[
            "brake shoe", "brake pad", "wear limit", "inspection", "AAR", "FRA", "freight car", "locomotive"
        ],
        conclusion_template="Brake shoes and pads must be replaced when worn to 1/2 inch or less in thickness, or if uneven wear is detected.",
        reasoning_framework="""
Brake shoes and pads are critical for stopping performance. AAR Rule 2 and FRA 49 CFR 232.111 specify replacement when thickness reaches 1/2 inch or less. Uneven wear or contamination also requires replacement. Inspections occur during brake tests and routine maintenance. Failure to replace worn components increases stopping distance and risk of violation.
""",
        key_factors=[
            "Inspection interval compliance",
            "Wear measurement accuracy",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 2",
            "FRA 49 CFR 232.111"
        ],
        burden_holder="Railroad operator",
        adversary_position="Shoes and pads can be used until complete failure.",
        counter_arguments=[
            "Worn components reduce braking effectiveness.",
            "Regulations specify minimum thickness.",
            "Failure increases risk of accident."
        ],
        resolution_strategy="Replace at or before wear limit and document action.",
        entity_scope="All freight cars and locomotives",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAR Rule 2"
    ),
    DoctrineBlock(
        topic="Freight Car Draft Gear Inspection and Maintenance",
        keywords=[
            "draft gear", "inspection", "maintenance", "AAR", "FRA", "freight car", "shock absorption"
        ],
        conclusion_template="Draft gears must be inspected for cracks, wear, and proper operation every 92 days; defective units must be replaced.",
        reasoning_framework="""
Draft gears absorb shock between cars. AAR Rule 22 and FRA 49 CFR 215.121 require 92-day inspections for cracks, wear, and operation. Defective units must be replaced to maintain train integrity and reduce damage. Maintenance records support compliance and warranty claims.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 22",
            "FRA 49 CFR 215.121"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Draft gear defects can be deferred until next major overhaul.",
        counter_arguments=[
            "Defective draft gears increase risk of damage.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective draft gears and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 22"
    ),
    DoctrineBlock(
        topic="Freight Car Side Bearing Adjustment and Lubrication",
        keywords=[
            "side bearing", "adjustment", "lubrication", "AAR", "FRA", "freight car", "truck", "bogie"
        ],
        conclusion_template="Side bearings must be adjusted to maintain 1/16 to 3/16 inch clearance and lubricated every 92 days.",
        reasoning_framework="""
Side bearings control truck rotation and prevent hunting. AAR Rule 46 and FRA 49 CFR 215.119 require adjustment to maintain clearance between 1/16 and 3/16 inch. Lubrication is performed every 92 days to prevent wear and noise. Improper adjustment increases risk of derailment and truck hunting. Maintenance records support compliance.
""",
        key_factors=[
            "Clearance measurement accuracy",
            "Lubrication interval compliance",
            "Adjustment procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 46",
            "FRA 49 CFR 215.119"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Side bearing adjustment is only necessary if noise or hunting is reported.",
        counter_arguments=[
            "Improper adjustment increases risk of derailment.",
            "Regulations require periodic adjustment.",
            "Deferred maintenance increases liability."
        ],
        resolution_strategy="Adjust and lubricate at required intervals and document all actions.",
        entity_scope="All freight cars",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAR Rule 46"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Pipe Leakage Test",
        keywords=[
            "brake pipe", "leakage test", "air brake", "AAR", "FRA", "freight car", "inspection"
        ],
        conclusion_template="Brake pipe leakage must not exceed 5 psi per minute during Class I brake test; excess leakage requires repair.",
        reasoning_framework="""
Brake pipe leakage affects braking performance. FRA 49 CFR 232.217 and AAR Rule 3 require that leakage not exceed 5 psi per minute during a Class I brake test. Excess leakage must be repaired before the car is returned to service. Proper documentation is required for compliance and audit readiness.
""",
        key_factors=[
            "Leakage test accuracy",
            "Repair procedures",
            "Test interval compliance",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "FRA 49 CFR 232.217",
            "AAR Field Manual Rule 3"
        ],
        burden_holder="Railroad operator",
        adversary_position="Minor leakage can be tolerated if brakes function normally.",
        counter_arguments=[
            "Excess leakage reduces braking effectiveness.",
            "Regulations specify maximum allowable leakage.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Repair all leaks exceeding threshold and document action.",
        entity_scope="All freight cars",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FRA 49 CFR 232.217"
    ),
    DoctrineBlock(
        topic="Freight Car Door Securement and Inspection",
        keywords=[
            "door", "securement", "inspection", "AAR", "FRA", "freight car", "boxcar"
        ],
        conclusion_template="Freight car doors must be inspected for proper securement and operation during every brake test; defective doors must be repaired before the car is moved.",
        reasoning_framework="""
Freight car doors must be secure to prevent lading loss and injury. FRA 49 CFR 215.111 and AAR Rule 100 require inspection during every brake test. Any defective or insecure door must be repaired before the car is moved. Documentation supports compliance and claims defense.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Repair procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "FRA 49 CFR 215.111",
            "AAR Field Manual Rule 100"
        ],
        burden_holder="Railroad operator",
        adversary_position="Minor door defects can be deferred until next scheduled maintenance.",
        counter_arguments=[
            "Insecure doors increase risk of lading loss.",
            "Regulations require immediate repair.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Repair all defective doors before movement and document action.",
        entity_scope="All boxcars and cars with movable doors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA 49 CFR 215.111"
    ),
    DoctrineBlock(
        topic="Freight Car Wheel Profile and Flange Thickness Inspection",
        keywords=[
            "wheel profile", "flange thickness", "inspection", "AAR", "FRA", "freight car"
        ],
        conclusion_template="Wheels must be removed when flange thickness is less than 1 inch or profile is worn beyond AAR limits.",
        reasoning_framework="""
Wheel profile and flange thickness are critical for safe tracking. AAR Rule 41 and FRA 49 CFR 215.103 specify minimum flange thickness (1 inch) and profile limits. Inspections are performed during brake tests and routine maintenance. Worn wheels must be removed to prevent derailment. Documentation supports compliance.
""",
        key_factors=[
            "Flange thickness measurement",
            "Profile gauge accuracy",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 41",
            "FRA 49 CFR 215.103"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Wheels can remain in service until complete failure.",
        counter_arguments=[
            "Worn wheels increase risk of derailment.",
            "Regulations specify minimum limits.",
            "Deferred replacement increases liability."
        ],
        resolution_strategy="Remove wheels at or before limit and document action.",
        entity_scope="All freight cars",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAR Rule 41"
    ),
    DoctrineBlock(
        topic="Freight Car Spring Group Inspection and Replacement",
        keywords=[
            "spring group", "inspection", "replacement", "AAR", "FRA", "freight car", "truck", "bogie"
        ],
        conclusion_template="Springs must be inspected for cracks, breaks, and sag every 92 days; defective springs must be replaced.",
        reasoning_framework="""
Springs support car weight and absorb shocks. AAR Rule 47 and FRA 49 CFR 215.119 require 92-day inspections for cracks, breaks, and sag. Defective springs must be replaced to maintain ride quality and safety. Maintenance records support compliance and warranty claims.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 47",
            "FRA 49 CFR 215.119"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor spring defects can be deferred until next overhaul.",
        counter_arguments=[
            "Defective springs affect ride quality and safety.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective springs and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 47"
    ),
    DoctrineBlock(
        topic="Freight Car End-of-Car Cushioning Device Inspection",
        keywords=[
            "end-of-car cushioning", "inspection", "AAR", "FRA", "freight car", "shock absorption"
        ],
        conclusion_template="End-of-car cushioning devices must be inspected for leaks, damage, and proper operation every 92 days; defective units must be replaced.",
        reasoning_framework="""
End-of-car cushioning devices absorb longitudinal shocks. AAR Rule 22 and FRA 49 CFR 215.121 require 92-day inspections for leaks, damage, and operation. Defective units must be replaced to maintain car integrity and reduce damage. Maintenance records support compliance and warranty claims.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 22",
            "FRA 49 CFR 215.121"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Cushioning device defects can be deferred until next major overhaul.",
        counter_arguments=[
            "Defective devices increase risk of damage.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective devices and document all actions.",
        entity_scope="All freight cars with cushioning devices",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAR Rule 22"
    ),
    DoctrineBlock(
        topic="Freight Car Center Plate and Bowl Inspection",
        keywords=[
            "center plate", "center bowl", "inspection", "AAR", "FRA", "freight car", "truck", "bogie"
        ],
        conclusion_template="Center plates and bowls must be inspected for cracks, wear, and lubrication every 92 days; defective components must be replaced.",
        reasoning_framework="""
Center plates and bowls transfer load between car body and truck. AAR Rule 47 and FRA 49 CFR 215.119 require 92-day inspections for cracks, wear, and lubrication. Defective components must be replaced to maintain stability and prevent derailment. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Lubrication procedures",
            "Replacement procedures",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 47",
            "FRA 49 CFR 215.119"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor wear can be monitored without immediate replacement.",
        counter_arguments=[
            "Wear increases risk of instability.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective components and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 47"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Rigging Inspection and Adjustment",
        keywords=[
            "brake rigging", "inspection", "adjustment", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake rigging must be inspected and adjusted for proper travel and alignment every 92 days; defective or misaligned rigging must be repaired.",
        reasoning_framework="""
Brake rigging transmits force from the brake cylinder to the shoes. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections and adjustment for proper travel and alignment. Defective or misaligned rigging must be repaired to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Travel and alignment measurement",
            "Adjustment procedures",
            "Repair procedures",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Brake rigging adjustment is only necessary if braking issues are reported.",
        counter_arguments=[
            "Improper adjustment reduces braking effectiveness.",
            "Regulations require periodic inspection.",
            "Deferred maintenance increases risk."
        ],
        resolution_strategy="Inspect and adjust at required intervals and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Yoke Inspection and Replacement",
        keywords=[
            "yoke", "inspection", "replacement", "AAR", "FRA", "freight car", "coupler"
        ],
        conclusion_template="Yokes must be inspected for cracks and wear every 92 days; defective yokes must be replaced.",
        reasoning_framework="""
Yokes connect the coupler to the car body. AAR Rule 21 and FRA 49 CFR 215.121 require 92-day inspections for cracks and wear. Defective yokes must be replaced to maintain train integrity. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 21",
            "FRA 49 CFR 215.121"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor cracks can be monitored without immediate replacement.",
        counter_arguments=[
            "Cracks can propagate rapidly.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective yokes and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 21"
    ),
    DoctrineBlock(
        topic="Freight Car Axle Ultrasonic Testing",
        keywords=[
            "axle", "ultrasonic testing", "NDT", "AAR", "FRA", "freight car"
        ],
        conclusion_template="Axles must undergo ultrasonic testing for internal cracks at least every 5 years or at overhaul.",
        reasoning_framework="""
Axle failures can cause derailments. AAR MSRP S-402 and FRA 49 CFR 215.115 require ultrasonic testing for internal cracks every 5 years or at overhaul. Defective axles must be replaced. Maintenance records support compliance and warranty claims.
""",
        key_factors=[
            "Testing interval compliance",
            "NDT result interpretation",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR MSRP S-402",
            "FRA 49 CFR 215.115"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Ultrasonic testing is only necessary if visible cracks are present.",
        counter_arguments=[
            "Internal cracks may not be visible.",
            "NDT is required for comprehensive detection.",
            "Regulations mandate periodic testing."
        ],
        resolution_strategy="Test at required intervals and replace defective axles.",
        entity_scope="All freight cars",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAR MSRP S-402"
    ),
    DoctrineBlock(
        topic="Freight Car Roof and Side Sheet Inspection",
        keywords=[
            "roof", "side sheet", "inspection", "AAR", "FRA", "freight car", "boxcar"
        ],
        conclusion_template="Roof and side sheets must be inspected for cracks, corrosion, and holes every 92 days; repairs must be made before returning to service.",
        reasoning_framework="""
Roof and side sheets protect lading and maintain structural integrity. AAR Rule 100 and FRA 49 CFR 215.111 require 92-day inspections for cracks, corrosion, and holes. Repairs must be made before the car is returned to service. Maintenance records support compliance and claims defense.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Repair procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 100",
            "FRA 49 CFR 215.111"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor defects can be deferred until next scheduled maintenance.",
        counter_arguments=[
            "Defects can propagate and compromise integrity.",
            "Regulations require immediate repair.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Repair all defects before returning car to service.",
        entity_scope="All boxcars and covered cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 100"
    ),
    DoctrineBlock(
        topic="Freight Car Hand Brake Inspection and Testing",
        keywords=[
            "hand brake", "inspection", "testing", "AAR", "FRA", "freight car"
        ],
        conclusion_template="Hand brakes must be inspected and tested for proper operation every 92 days; defective hand brakes must be repaired.",
        reasoning_framework="""
Hand brakes secure parked cars. FRA 49 CFR 232.305 and AAR Rule 3 require 92-day inspections and testing for proper operation. Defective hand brakes must be repaired before the car is returned to service. Maintenance records support compliance and safety audits.
""",
        key_factors=[
            "Inspection interval compliance",
            "Testing procedures",
            "Repair procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "FRA 49 CFR 232.305",
            "AAR Field Manual Rule 3"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Hand brake testing is only necessary if issues are reported.",
        counter_arguments=[
            "Hand brake failures can cause roll-aways.",
            "Regulations require periodic testing.",
            "Deferred maintenance increases risk."
        ],
        resolution_strategy="Test and repair at required intervals and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA 49 CFR 232.305"
    ),
    DoctrineBlock(
        topic="Freight Car Coupler Height and Alignment Inspection",
        keywords=[
            "coupler height", "alignment", "inspection", "AAR", "FRA", "freight car"
        ],
        conclusion_template="Coupler height must be 33.5 to 34.5 inches above rail; misaligned couplers must be adjusted before the car is returned to service.",
        reasoning_framework="""
Proper coupler height and alignment are critical for safe train operation. AAR Rule 21 and FRA 49 CFR 231.31 specify a height range of 33.5 to 34.5 inches above rail. Misaligned couplers must be adjusted before the car is returned to service. Maintenance records support compliance.
""",
        key_factors=[
            "Measurement accuracy",
            "Adjustment procedures",
            "Inspection interval compliance",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 21",
            "FRA 49 CFR 231.31"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor misalignment can be tolerated.",
        counter_arguments=[
            "Misalignment increases risk of uncoupling.",
            "Regulations specify allowable range.",
            "Deferred adjustment increases liability."
        ],
        resolution_strategy="Adjust couplers to within allowable range and document action.",
        entity_scope="All freight cars",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAR Rule 21"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Cylinder Inspection and Replacement",
        keywords=[
            "brake cylinder", "inspection", "replacement", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake cylinders must be inspected for leaks and proper operation every 92 days; defective cylinders must be replaced.",
        reasoning_framework="""
Brake cylinders convert air pressure into mechanical force. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for leaks and operation. Defective cylinders must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Leak detection",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor leaks can be tolerated if brakes function normally.",
        counter_arguments=[
            "Leaks reduce braking effectiveness.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective cylinders and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Shoe Holder and Key Inspection",
        keywords=[
            "brake shoe holder", "key", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake shoe holders and keys must be inspected for wear and security every 92 days; defective components must be replaced.",
        reasoning_framework="""
Brake shoe holders and keys secure the brake shoe to the rigging. AAR Rule 2 and FRA 49 CFR 232.111 require 92-day inspections for wear and security. Defective components must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 2",
            "FRA 49 CFR 232.111"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor wear can be tolerated.",
        counter_arguments=[
            "Loose holders or keys can result in shoe loss.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective components and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 2"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Beam Inspection and Replacement",
        keywords=[
            "brake beam", "inspection", "replacement", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake beams must be inspected for cracks and deformation every 92 days; defective beams must be replaced.",
        reasoning_framework="""
Brake beams transfer force from the brake cylinder to the shoes. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for cracks and deformation. Defective beams must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor cracks can be monitored without immediate replacement.",
        counter_arguments=[
            "Cracks can propagate rapidly.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective beams and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Lever and Pin Inspection",
        keywords=[
            "brake lever", "pin", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake levers and pins must be inspected for wear and security every 92 days; defective components must be replaced.",
        reasoning_framework="""
Brake levers and pins transmit force within the rigging. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for wear and security. Defective components must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor wear can be tolerated.",
        counter_arguments=[
            "Worn levers or pins can result in brake failure.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective components and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Head and Lining Inspection",
        keywords=[
            "brake head", "lining", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake heads and linings must be inspected for cracks, wear, and securement every 92 days; defective components must be replaced.",
        reasoning_framework="""
Brake heads and linings are critical for force transfer to the wheel. AAR Rule 2 and FRA 49 CFR 232.111 require 92-day inspections for cracks, wear, and securement. Defective components must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 2",
            "FRA 49 CFR 232.111"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor cracks can be monitored without immediate replacement.",
        counter_arguments=[
            "Cracks can propagate rapidly.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective components and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 2"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Slack Adjuster Inspection and Maintenance",
        keywords=[
            "slack adjuster", "inspection", "maintenance", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Slack adjusters must be inspected and tested for proper operation every 92 days; defective adjusters must be repaired or replaced.",
        reasoning_framework="""
Slack adjusters maintain correct brake shoe clearance. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections and testing for proper operation. Defective adjusters must be repaired or replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Testing procedures",
            "Repair/replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Slack adjuster maintenance is only necessary if issues are reported.",
        counter_arguments=[
            "Improper adjustment reduces braking effectiveness.",
            "Regulations require periodic inspection.",
            "Deferred maintenance increases risk."
        ],
        resolution_strategy="Inspect and repair at required intervals and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Pipe Hose and Coupling Inspection",
        keywords=[
            "brake pipe hose", "coupling", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake pipe hoses and couplings must be inspected for leaks, wear, and securement every 92 days; defective components must be replaced.",
        reasoning_framework="""
Brake pipe hoses and couplings connect cars and transmit air pressure. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for leaks, wear, and securement. Defective components must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Leak detection",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor leaks can be tolerated.",
        counter_arguments=[
            "Leaks reduce braking effectiveness.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective components and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Reservoir Inspection and Replacement",
        keywords=[
            "brake reservoir", "inspection", "replacement", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake reservoirs must be inspected for leaks and corrosion every 92 days; defective reservoirs must be replaced.",
        reasoning_framework="""
Brake reservoirs store compressed air for braking. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for leaks and corrosion. Defective reservoirs must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Leak detection",
            "Corrosion identification",
            "Replacement procedures",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor leaks can be tolerated.",
        counter_arguments=[
            "Leaks reduce braking effectiveness.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective reservoirs and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Cylinder Piston Travel Inspection",
        keywords=[
            "brake cylinder piston", "travel", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake cylinder piston travel must be between 6 and 8 inches; out-of-range travel requires adjustment or repair.",
        reasoning_framework="""
Proper piston travel ensures effective braking. AAR Rule 3 and FRA 49 CFR 232.205 specify a range of 6 to 8 inches. Out-of-range travel indicates rigging or slack adjuster issues. Adjustment or repair is required before the car is returned to service. Maintenance records support compliance.
""",
        key_factors=[
            "Measurement accuracy",
            "Adjustment procedures",
            "Repair procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor deviations can be tolerated.",
        counter_arguments=[
            "Improper travel reduces braking effectiveness.",
            "Regulations specify allowable range.",
            "Deferred adjustment increases risk."
        ],
        resolution_strategy="Adjust or repair to within allowable range and document action.",
        entity_scope="All freight cars",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Cylinder Head and Seal Inspection",
        keywords=[
            "brake cylinder head", "seal", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake cylinder heads and seals must be inspected for leaks and wear every 92 days; defective components must be replaced.",
        reasoning_framework="""
Brake cylinder heads and seals prevent air leakage. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for leaks and wear. Defective components must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Leak detection",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor leaks can be tolerated.",
        counter_arguments=[
            "Leaks reduce braking effectiveness.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective components and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Cylinder Return Spring Inspection",
        keywords=[
            "brake cylinder return spring", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake cylinder return springs must be inspected for cracks and proper operation every 92 days; defective springs must be replaced.",
        reasoning_framework="""
Return springs ensure brake release. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for cracks and operation. Defective springs must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Defect identification",
            "Replacement procedures",
            "Maintenance records",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor cracks can be monitored without immediate replacement.",
        counter_arguments=[
            "Cracks can propagate rapidly.",
            "Regulations require immediate action.",
            "Deferred repairs increase liability."
        ],
        resolution_strategy="Replace defective springs and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Cylinder Push Rod Inspection",
        keywords=[
            "brake cylinder push rod", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake cylinder push rods must be inspected for wear and straightness every 92 days; defective rods must be replaced.",
        reasoning_framework="""
Push rods transfer force from the cylinder to the rigging. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for wear and straightness. Defective rods must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Wear measurement",
            "Straightness check",
            "Replacement procedures",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor wear can be tolerated.",
        counter_arguments=[
            "Worn or bent rods reduce braking effectiveness.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective rods and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Cylinder Mounting Inspection",
        keywords=[
            "brake cylinder mounting", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Brake cylinder mounting must be inspected for security and cracks every 92 days; defective mountings must be repaired.",
        reasoning_framework="""
Secure mounting prevents cylinder movement during braking. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for security and cracks. Defective mountings must be repaired to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Security check",
            "Crack identification",
            "Repair procedures",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor looseness can be tolerated.",
        counter_arguments=[
            "Loose mountings reduce braking effectiveness.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Repair defective mountings and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
    ),
    DoctrineBlock(
        topic="Freight Car Brake Cylinder Clevis Pin and Cotter Inspection",
        keywords=[
            "brake cylinder clevis pin", "cotter", "inspection", "AAR", "FRA", "freight car", "air brake"
        ],
        conclusion_template="Clevis pins and cotters must be inspected for wear and security every 92 days; defective components must be replaced.",
        reasoning_framework="""
Clevis pins and cotters secure the push rod to the rigging. AAR Rule 3 and FRA 49 CFR 232.205 require 92-day inspections for wear and security. Defective components must be replaced to ensure effective braking. Maintenance records support compliance.
""",
        key_factors=[
            "Inspection interval compliance",
            "Wear measurement",
            "Security check",
            "Replacement procedures",
            "AAR/FRA standards"
        ],
        primary_authority=[
            "AAR Field Manual Rule 3",
            "FRA 49 CFR 232.205"
        ],
        burden_holder="Railroad maintenance department",
        adversary_position="Minor wear can be tolerated.",
        counter_arguments=[
            "Worn or loose pins/cotters reduce braking effectiveness.",
            "Regulations require immediate repair.",
            "Deferred repairs increase risk."
        ],
        resolution_strategy="Replace defective components and document all actions.",
        entity_scope="All freight cars",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AAR Rule 3"
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