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
        topic="CDL Requirements 49 CFR 383",
        keywords=["CDL", "commercial driver", "license", "49 CFR 383", "qualification", "endorsement"],
        conclusion_template="A driver must possess a valid Commercial Driver's License (CDL) with appropriate endorsements to operate a commercial motor vehicle (CMV) as defined by 49 CFR 383.",
        reasoning_framework=(
            "49 CFR 383 establishes the requirements for obtaining and maintaining a CDL. The regulation defines CMVs by weight, passenger capacity, and hazardous materials carriage. "
            "Drivers must meet age, medical, and knowledge requirements, pass skills tests, and obtain endorsements for specialized operations (e.g., air brakes, passenger, hazardous materials). "
            "Employers must verify CDL status and endorsements prior to assigning CMV operation. "
            "Disqualifications occur for offenses such as DUI, leaving the scene of an accident, or using a CMV in commission of a felony. "
            "States must maintain a system for tracking violations and disqualifications, and employers must check driving records periodically. "
            "CDL holders are subject to federal and state regulations, and reciprocity exists across states for CDL recognition. "
            "The burden of compliance lies with both the driver and employer, with penalties for violations including fines, disqualification, and employer sanctions. "
            "Exceptions exist for certain military drivers and farm vehicle operators. "
            "The doctrine is enforced through roadside inspections, audits, and employer record reviews."
        ),
        key_factors=[
            "CMV definition",
            "Driver age and medical qualification",
            "Knowledge and skills testing",
            "Endorsement requirements",
            "Disqualification criteria",
            "Employer verification",
            "State compliance and reciprocity"
        ],
        primary_authority=["49 CFR 383", "FMCSA Guidance"],
        burden_holder="Driver and Employer",
        adversary_position="Driver lacks valid CDL or proper endorsement for vehicle type",
        counter_arguments=[
            "Driver operates under a valid exemption",
            "Employer misinterpreted CMV definition",
            "State records not updated"
        ],
        resolution_strategy="Verify CDL status and endorsements via state and federal databases; review exemption applicability; ensure employer compliance with record checks.",
        entity_scope="Commercial drivers, motor carriers, state licensing agencies",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA v. XYZ Trucking Co., 2017"
    ),
    DoctrineBlock(
        topic="Hours of Service 49 CFR 395",
        keywords=["hours of service", "HOS", "driver fatigue", "logbook", "49 CFR 395", "rest break", "driving limit"],
        conclusion_template="Drivers of property-carrying CMVs must comply with hours of service limits, including maximum driving and on-duty time, mandatory rest breaks, and off-duty periods as specified in 49 CFR 395.",
        reasoning_framework=(
            "49 CFR 395 sets forth maximum driving and on-duty hours for CMV drivers to prevent fatigue-related incidents. "
            "Property-carrying drivers may drive up to 11 hours after 10 consecutive hours off duty, within a 14-hour window. "
            "Drivers must take a 30-minute break after 8 hours of driving. "
            "Weekly limits include 60 hours in 7 days or 70 hours in 8 days, depending on carrier operations. "
            "Short-haul exemptions apply for drivers operating within a 150 air-mile radius and returning to the same location. "
            "Electronic logging devices (ELDs) are required to record duty status, except for exempt drivers. "
            "Violations result in out-of-service orders, fines, and carrier safety rating impacts. "
            "Adversaries may claim operational necessity or misinterpretation of duty status. "
            "Resolution involves reviewing logbooks, ELD data, and applying regulatory exceptions."
        ),
        key_factors=[
            "Maximum driving hours",
            "On-duty time limits",
            "Mandatory rest breaks",
            "Weekly hour limits",
            "Short-haul exemption",
            "ELD requirement"
        ],
        primary_authority=["49 CFR 395", "FMCSA ELD Guidance"],
        burden_holder="Driver and Carrier",
        adversary_position="Driver exceeded HOS limits or failed to record duty status accurately",
        counter_arguments=[
            "Short-haul exemption applies",
            "ELD malfunction or data error",
            "Carrier misapplied duty status definitions"
        ],
        resolution_strategy="Audit ELD and logbook records; verify exemption applicability; review carrier training and compliance systems.",
        entity_scope="Property-carrying CMV drivers, carriers, enforcement agencies",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA v. ABC Logistics, 2019"
    ),
    DoctrineBlock(
        topic="ELD Mandate 49 CFR 395.8",
        keywords=["ELD", "electronic logging device", "49 CFR 395.8", "record of duty status", "compliance", "logbook"],
        conclusion_template="Drivers required to maintain records of duty status must use an FMCSA-registered ELD unless exempt under 49 CFR 395.8.",
        reasoning_framework=(
            "The ELD mandate requires most CMV drivers subject to HOS rules to use an electronic logging device to record duty status. "
            "ELDs must be registered with FMCSA and meet technical specifications for data capture, tamper resistance, and transferability. "
            "Exemptions include drivers operating within short-haul limits, drivers in vehicles manufactured before 2000, and certain agricultural operations. "
            "ELD malfunctions must be documented and resolved within 8 days, with paper logs used temporarily. "
            "Carriers must ensure ELDs are properly installed, drivers are trained, and records are retained for inspection. "
            "Non-compliance results in out-of-service orders and fines. "
            "Adversaries may argue technical issues or exemption applicability. "
            "Resolution involves reviewing ELD registration, exemption status, and malfunction documentation."
        ),
        key_factors=[
            "ELD registration",
            "Technical compliance",
            "Exemption applicability",
            "Malfunction documentation",
            "Carrier training"
        ],
        primary_authority=["49 CFR 395.8", "FMCSA ELD FAQ"],
        burden_holder="Carrier and Driver",
        adversary_position="Driver or carrier failed to use ELD or improperly claimed exemption",
        counter_arguments=[
            "Vehicle qualifies for exemption",
            "ELD malfunction documented",
            "Short-haul operation"
        ],
        resolution_strategy="Verify ELD registration and exemption status; review malfunction logs; audit carrier training records.",
        entity_scope="CMV drivers, carriers, enforcement personnel",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA ELD Final Rule, 2015"
    ),
    DoctrineBlock(
        topic="Drug and Alcohol Testing 49 CFR 382",
        keywords=["drug testing", "alcohol testing", "random testing", "pre-employment", "post-accident", "49 CFR 382"],
        conclusion_template="All drivers operating CMVs requiring a CDL must be subject to drug and alcohol testing as specified in 49 CFR 382, including pre-employment, random, post-accident, reasonable suspicion, and return-to-duty testing.",
        reasoning_framework=(
            "49 CFR 382 mandates drug and alcohol testing for safety-sensitive positions in transportation. "
            "Testing types include pre-employment, random, post-accident, reasonable suspicion, return-to-duty, and follow-up. "
            "Employers must maintain a testing program, select random pools, and report violations to FMCSA Clearinghouse. "
            "Drivers testing positive or refusing testing are immediately removed from safety-sensitive functions and must complete return-to-duty procedures. "
            "Adversaries may claim procedural errors or contest test results. "
            "Resolution involves reviewing testing records, chain-of-custody documentation, and compliance with regulatory timelines."
        ),
        key_factors=[
            "Testing program implementation",
            "Random selection",
            "Chain-of-custody",
            "Reporting requirements",
            "Return-to-duty process"
        ],
        primary_authority=["49 CFR 382", "FMCSA Clearinghouse Guidance"],
        burden_holder="Employer",
        adversary_position="Driver not tested or procedural errors in testing",
        counter_arguments=[
            "Testing not required for exempt driver",
            "Procedural error invalidates test",
            "False positive or laboratory error"
        ],
        resolution_strategy="Audit testing records; verify chain-of-custody; review exemption applicability.",
        entity_scope="CDL drivers, motor carriers, testing laboratories",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Clearinghouse Final Rule, 2019"
    ),
    DoctrineBlock(
        topic="Vehicle Inspection and Maintenance 49 CFR 396",
        keywords=["vehicle inspection", "maintenance", "49 CFR 396", "annual inspection", "defect report", "repair"],
        conclusion_template="Motor carriers must ensure CMVs are systematically inspected, maintained, and repaired as required by 49 CFR 396, including daily driver inspections and annual inspections.",
        reasoning_framework=(
            "49 CFR 396 requires motor carriers to establish systematic inspection, maintenance, and repair programs for CMVs. "
            "Drivers must complete daily vehicle inspection reports (DVIRs) identifying defects impacting safety. "
            "Annual inspections must be performed by qualified personnel, with documentation retained for 14 months. "
            "Defects must be repaired before vehicle operation, and carriers must maintain records of repairs and inspections. "
            "Adversaries may claim lack of defects or challenge inspection qualifications. "
            "Resolution involves reviewing DVIRs, annual inspection certificates, and maintenance logs."
        ),
        key_factors=[
            "Systematic inspection program",
            "Daily driver inspection",
            "Annual inspection",
            "Repair documentation",
            "Inspector qualification"
        ],
        primary_authority=["49 CFR 396", "FMCSA Inspection Guidance"],
        burden_holder="Carrier",
        adversary_position="Vehicle operated with unresolved defects or lack of inspection documentation",
        counter_arguments=[
            "Defect did not impact safety",
            "Inspection performed by qualified personnel",
            "Documentation lost or misplaced"
        ],
        resolution_strategy="Audit inspection and repair records; verify inspector qualifications; review defect impact.",
        entity_scope="Motor carriers, CMV drivers, inspectors",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA v. DEF Transport, 2018"
    ),
    DoctrineBlock(
        topic="Weight Limits and Bridge Formula 23 USC 127",
        keywords=["weight limits", "bridge formula", "23 USC 127", "axle weight", "gross weight", "overweight"],
        conclusion_template="CMVs operating on the Interstate System must comply with federal weight limits and the Bridge Formula as specified in 23 USC 127.",
        reasoning_framework=(
            "23 USC 127 establishes maximum allowable weights for CMVs on the Interstate System: 80,000 lbs gross vehicle weight, 20,000 lbs single axle, and 34,000 lbs tandem axle. "
            "The Bridge Formula calculates maximum weight based on axle spacing to prevent structural damage. "
            "States may issue permits for overweight vehicles under specific conditions. "
            "Violations result in fines, permit revocation, and potential vehicle impoundment. "
            "Adversaries may argue permit validity or state-specific exceptions. "
            "Resolution involves reviewing weight tickets, permit documentation, and bridge formula calculations."
        ),
        key_factors=[
            "Gross vehicle weight",
            "Axle weight",
            "Bridge Formula calculation",
            "Permit issuance",
            "State exceptions"
        ],
        primary_authority=["23 USC 127", "FHWA Guidance"],
        burden_holder="Carrier",
        adversary_position="Vehicle exceeds federal weight limits or improper permit",
        counter_arguments=[
            "Valid state-issued overweight permit",
            "Bridge Formula calculation error",
            "Vehicle not operating on Interstate"
        ],
        resolution_strategy="Verify weight tickets; review permit status; recalculate Bridge Formula.",
        entity_scope="CMV carriers, state DOTs, enforcement agencies",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FHWA Bridge Formula Policy, 2016"
    ),
    DoctrineBlock(
        topic="Oversize Permits and Routing",
        keywords=["oversize", "permit", "routing", "escort", "state DOT", "load dimensions"],
        conclusion_template="Oversize loads must obtain appropriate permits and follow designated routing, including escort requirements, as specified by state DOT regulations.",
        reasoning_framework=(
            "Oversize loads exceeding legal dimensions require permits from state DOTs. "
            "Permits specify allowable routes, travel times, escort vehicle requirements, and signage. "
            "Carriers must comply with permit conditions, including notification of changes and adherence to restrictions. "
            "Violations result in fines, permit revocation, and liability for infrastructure damage. "
            "Adversaries may claim permit ambiguity or route deviation due to emergency. "
            "Resolution involves reviewing permit documentation, route maps, and escort logs."
        ),
        key_factors=[
            "Permit issuance",
            "Route designation",
            "Escort requirements",
            "Signage and lighting",
            "Permit compliance"
        ],
        primary_authority=["State DOT regulations", "FHWA Oversize Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to obtain permit or deviated from designated route",
        counter_arguments=[
            "Emergency deviation",
            "Permit ambiguity",
            "Escort vehicle malfunction"
        ],
        resolution_strategy="Review permit and routing documentation; verify escort logs; assess emergency justification.",
        entity_scope="Carriers, state DOTs, escort services",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State DOT v. GHI Logistics, 2020"
    ),
    DoctrineBlock(
        topic="Hazmat Transportation 49 CFR 171-180 PHMSA",
        keywords=["hazmat", "hazardous materials", "PHMSA", "49 CFR 171-180", "placarding", "shipping paper"],
        conclusion_template="Hazmat shipments must comply with PHMSA regulations in 49 CFR 171-180, including classification, packaging, labeling, placarding, shipping papers, and emergency response information.",
        reasoning_framework=(
            "49 CFR 171-180 governs the transportation of hazardous materials. "
            "Shippers must classify materials, select proper packaging, and mark/label containers. "
            "Carriers must ensure vehicles are properly placarded, shipping papers are accessible, and emergency response information is provided. "
            "Drivers must be trained in hazmat handling and response. "
            "Violations include improper classification, packaging, placarding, or missing shipping papers. "
            "Adversaries may claim misclassification or packaging errors. "
            "Resolution involves reviewing shipping papers, placarding, and driver training records."
        ),
        key_factors=[
            "Material classification",
            "Packaging selection",
            "Labeling and placarding",
            "Shipping papers",
            "Driver training"
        ],
        primary_authority=["49 CFR 171-180", "PHMSA Guidance"],
        burden_holder="Shipper and Carrier",
        adversary_position="Improper classification, packaging, or missing placarding",
        counter_arguments=[
            "Material not regulated",
            "Packaging meets alternative standard",
            "Placarding not required for quantity"
        ],
        resolution_strategy="Audit shipping papers; verify placarding; review training records.",
        entity_scope="Shippers, carriers, drivers, enforcement agencies",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA v. JKL Transport, 2018"
    ),
    DoctrineBlock(
        topic="Railroad Safety FRA 49 CFR 213-243",
        keywords=["railroad safety", "FRA", "track inspection", "49 CFR 213-243", "signal system", "employee qualification"],
        conclusion_template="Railroad operations must comply with FRA safety regulations in 49 CFR 213-243, including track inspection, signal system maintenance, and employee qualification.",
        reasoning_framework=(
            "49 CFR 213-243 establishes safety standards for railroad operations. "
            "Track inspection and maintenance must meet FRA criteria for geometry, integrity, and defect remediation. "
            "Signal systems must be maintained and tested regularly. "
            "Employees must be qualified and trained for safety-sensitive functions. "
            "Violations include inadequate inspection, maintenance lapses, or unqualified personnel. "
            "Adversaries may claim compliance through alternative methods or challenge inspection findings. "
            "Resolution involves reviewing inspection logs, maintenance records, and employee qualification documentation."
        ),
        key_factors=[
            "Track inspection frequency",
            "Signal system maintenance",
            "Employee qualification",
            "Defect remediation",
            "Record retention"
        ],
        primary_authority=["49 CFR 213-243", "FRA Guidance"],
        burden_holder="Railroad Operator",
        adversary_position="Operator failed to inspect or maintain track/signal systems or used unqualified personnel",
        counter_arguments=[
            "Alternative compliance method approved",
            "Inspection findings disputed",
            "Personnel qualified under different standard"
        ],
        resolution_strategy="Review inspection and maintenance records; verify employee qualifications; assess alternative compliance.",
        entity_scope="Railroad operators, employees, FRA inspectors",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA v. MNO Railways, 2017"
    ),
    DoctrineBlock(
        topic="Aviation FAA 14 CFR Part 91 General Operating",
        keywords=["aviation", "FAA", "14 CFR Part 91", "general operating", "flight rules", "aircraft maintenance"],
        conclusion_template="Aircraft operations must comply with FAA general operating and flight rules in 14 CFR Part 91, including maintenance, pilot qualification, and operational limitations.",
        reasoning_framework=(
            "14 CFR Part 91 sets forth general operating and flight rules for civil aircraft. "
            "Operators must ensure aircraft are airworthy, maintained per manufacturer and FAA standards, and pilots are properly certified. "
            "Flight operations must adhere to weather minimums, airspace restrictions, and operational limitations. "
            "Violations include unqualified pilots, maintenance lapses, or operational rule breaches. "
            "Adversaries may claim compliance through alternative maintenance or pilot certification. "
            "Resolution involves reviewing maintenance logs, pilot certificates, and flight records."
        ),
        key_factors=[
            "Aircraft airworthiness",
            "Pilot certification",
            "Maintenance records",
            "Flight rule compliance",
            "Operational limitations"
        ],
        primary_authority=["14 CFR Part 91", "FAA Guidance"],
        burden_holder="Aircraft Operator",
        adversary_position="Operator failed to maintain aircraft, used unqualified pilot, or violated flight rules",
        counter_arguments=[
            "Alternative maintenance program approved",
            "Pilot certified under different standard",
            "Operational limitation misinterpreted"
        ],
        resolution_strategy="Audit maintenance and pilot records; review operational compliance; verify alternative approvals.",
        entity_scope="Aircraft operators, pilots, FAA inspectors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA v. PQR Aviation, 2019"
    ),
    DoctrineBlock(
        topic="FAA Part 121 Air Carrier Operations",
        keywords=["FAA", "Part 121", "air carrier", "crew qualification", "maintenance", "flight operations"],
        conclusion_template="Air carriers must comply with FAA Part 121 regulations, including crew qualification, aircraft maintenance, operational control, and flight safety procedures.",
        reasoning_framework=(
            "FAA Part 121 governs air carrier operations, requiring rigorous crew qualification, maintenance, and operational control procedures. "
            "Crew members must meet training and certification standards, including recurrent training. "
            "Aircraft must be maintained per approved programs, with records retained for inspection. "
            "Operational control must ensure flight safety, adherence to weather minimums, and emergency procedures. "
            "Violations include unqualified crew, maintenance lapses, or operational control failures. "
            "Adversaries may claim compliance through alternative programs or challenge crew qualification. "
            "Resolution involves reviewing crew training records, maintenance logs, and operational control documentation."
        ),
        key_factors=[
            "Crew qualification",
            "Maintenance program",
            "Operational control",
            "Flight safety procedures",
            "Record retention"
        ],
        primary_authority=["FAA Part 121", "FAA Guidance"],
        burden_holder="Air Carrier",
        adversary_position="Carrier failed to qualify crew, maintain aircraft, or ensure operational control",
        counter_arguments=[
            "Alternative qualification program approved",
            "Maintenance performed per manufacturer",
            "Operational control delegated"
        ],
        resolution_strategy="Audit crew and maintenance records; review operational control procedures; verify alternative approvals.",
        entity_scope="Air carriers, crew, FAA inspectors",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA v. STU Airlines, 2021"
    ),
    DoctrineBlock(
        topic="USDOT Number and Operating Authority",
        keywords=["USDOT number", "operating authority", "FMCSA", "registration", "motor carrier"],
        conclusion_template="Motor carriers must obtain a USDOT number and, where applicable, operating authority from FMCSA prior to commencing interstate operations.",
        reasoning_framework=(
            "FMCSA requires motor carriers operating in interstate commerce to obtain a USDOT number for identification and safety monitoring. "
            "Certain carriers must also obtain operating authority, including for-hire carriers, brokers, and freight forwarders. "
            "Registration is completed via the Unified Registration System (URS), with periodic updates required. "
            "Operating authority is subject to insurance and financial responsibility requirements. "
            "Violations include operating without registration or authority, resulting in fines and out-of-service orders. "
            "Adversaries may claim exemption or registration delay. "
            "Resolution involves reviewing registration status, authority documentation, and exemption applicability."
        ),
        key_factors=[
            "USDOT number registration",
            "Operating authority",
            "Insurance requirements",
            "URS compliance",
            "Exemption applicability"
        ],
        primary_authority=["FMCSA Registration Guidance", "49 CFR 390"],
        burden_holder="Carrier",
        adversary_position="Carrier operated without USDOT number or required authority",
        counter_arguments=[
            "Carrier exempt from registration",
            "Registration pending",
            "Authority not required for operation type"
        ],
        resolution_strategy="Verify registration and authority status; review exemption applicability; audit insurance records.",
        entity_scope="Motor carriers, brokers, FMCSA",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA v. VWX Logistics, 2020"
    ),
    DoctrineBlock(
        topic="State DOT Compliance and UCR",
        keywords=["state DOT", "UCR", "Unified Carrier Registration", "compliance", "motor carrier"],
        conclusion_template="Motor carriers operating interstate must comply with state DOT regulations and participate in the Unified Carrier Registration (UCR) program.",
        reasoning_framework=(
            "The UCR program requires interstate motor carriers, brokers, and freight forwarders to register and pay fees annually. "
            "State DOTs enforce compliance through audits and roadside inspections. "
            "Non-compliance results in fines, out-of-service orders, and registration revocation. "
            "Adversaries may claim exemption or registration delay. "
            "Resolution involves reviewing UCR registration, payment records, and exemption applicability."
        ),
        key_factors=[
            "UCR registration",
            "Fee payment",
            "State DOT enforcement",
            "Exemption applicability",
            "Record retention"
        ],
        primary_authority=["UCR Act", "State DOT regulations"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to register or pay UCR fees",
        counter_arguments=[
            "Carrier exempt from UCR",
            "Registration pending",
            "Fee payment delayed"
        ],
        resolution_strategy="Verify UCR registration and payment; review exemption status; audit carrier records.",
        entity_scope="Motor carriers, brokers, state DOTs",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State DOT v. YZA Transport, 2019"
    ),
    DoctrineBlock(
        topic="CSA Safety Measurement System",
        keywords=["CSA", "Safety Measurement System", "SMS", "FMCSA", "carrier safety", "BASICs"],
        conclusion_template="FMCSA's CSA Safety Measurement System evaluates carrier safety performance based on BASICs, inspections, and violations, impacting enforcement and intervention decisions.",
        reasoning_framework=(
            "The CSA Safety Measurement System (SMS) scores carriers based on Behavior Analysis and Safety Improvement Categories (BASICs): Unsafe Driving, Crash Indicator, HOS Compliance, Vehicle Maintenance, Controlled Substances/Alcohol, Hazardous Materials, and Driver Fitness. "
            "Scores are derived from inspection and violation data, updated monthly. "
            "High scores trigger interventions, audits, and potential out-of-service orders. "
            "Carriers may contest violations or request data reviews. "
            "Resolution involves reviewing SMS scores, inspection reports, and DataQs submissions."
        ),
        key_factors=[
            "BASICs scoring",
            "Inspection and violation data",
            "Intervention thresholds",
            "Data review process",
            "Carrier contestation"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 385"],
        burden_holder="Carrier",
        adversary_position="Carrier has high SMS score or disputed violation",
        counter_arguments=[
            "Violation incorrectly attributed",
            "Inspection data error",
            "Score calculation dispute"
        ],
        resolution_strategy="Review SMS scores and inspection reports; submit DataQs for correction; audit carrier safety program.",
        entity_scope="Motor carriers, FMCSA, enforcement agencies",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="Medical Certification 49 CFR 391.41-391.49",
        keywords=["medical certification", "CMV driver", "49 CFR 391.41", "physical qualification", "examiner"],
        conclusion_template="CMV drivers must meet physical qualification standards and possess valid medical certification as specified in 49 CFR 391.41-391.49.",
        reasoning_framework=(
            "49 CFR 391.41-391.49 outlines physical qualification standards for CMV drivers. "
            "Drivers must be examined by a certified medical examiner and possess a valid medical certificate. "
            "Medical conditions impacting safe operation, such as vision, hearing, cardiovascular, or neurological disorders, may disqualify a driver. "
            "Certificates must be renewed periodically and records maintained by carriers. "
            "Adversaries may claim medical exemption or contest examiner findings. "
            "Resolution involves reviewing medical certificates, examiner credentials, and exemption documentation."
        ),
        key_factors=[
            "Physical qualification standards",
            "Certified medical examiner",
            "Certificate renewal",
            "Record retention",
            "Exemption applicability"
        ],
        primary_authority=["49 CFR 391.41-391.49", "FMCSA Medical Guidance"],
        burden_holder="Driver and Carrier",
        adversary_position="Driver lacks valid medical certificate or fails physical qualification",
        counter_arguments=[
            "Medical exemption granted",
            "Examiner error",
            "Certificate pending renewal"
        ],
        resolution_strategy="Verify medical certificate status; review examiner credentials; assess exemption documentation.",
        entity_scope="CMV drivers, carriers, medical examiners",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Medical Certification Policy, 2017"
    ),
    DoctrineBlock(
        topic="Cargo Securement 49 CFR 393.100-393.142",
        keywords=["cargo securement", "49 CFR 393.100", "tie-down", "load stability", "inspection"],
        conclusion_template="Cargo transported by CMVs must be properly secured using methods and devices compliant with 49 CFR 393.100-393.142 to prevent shifting or loss during transit.",
        reasoning_framework=(
            "49 CFR 393.100-393.142 specifies cargo securement standards for CMVs. "
            "Cargo must be immobilized or secured using tie-downs, blocking, bracing, and other devices meeting strength requirements. "
            "Specific rules apply to different cargo types (e.g., logs, pipes, vehicles). "
            "Drivers must inspect securement devices before and during transit. "
            "Violations include inadequate securement, device failure, or improper inspection. "
            "Adversaries may claim device compliance or cargo stability. "
            "Resolution involves reviewing securement methods, device ratings, and inspection logs."
        ),
        key_factors=[
            "Securement device strength",
            "Cargo type-specific rules",
            "Inspection frequency",
            "Device failure",
            "Load stability"
        ],
        primary_authority=["49 CFR 393.100-393.142", "FMCSA Cargo Securement Guidance"],
        burden_holder="Carrier and Driver",
        adversary_position="Cargo not properly secured or securement device failed",
        counter_arguments=[
            "Device meets strength requirements",
            "Cargo stable without securement",
            "Inspection performed as required"
        ],
        resolution_strategy="Audit securement devices and methods; review inspection logs; assess cargo stability.",
        entity_scope="CMV carriers, drivers, enforcement agencies",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Cargo Securement Policy, 2016"
    ),
    DoctrineBlock(
        topic="Insurance and Financial Responsibility 49 CFR 387",
        keywords=["insurance", "financial responsibility", "49 CFR 387", "motor carrier", "minimum coverage"],
        conclusion_template="Motor carriers must maintain minimum levels of insurance and financial responsibility as specified in 49 CFR 387.",
        reasoning_framework=(
            "49 CFR 387 requires motor carriers to maintain minimum levels of liability insurance: $750,000 for property carriers, $5,000,000 for hazardous materials, and $1,500,000 for passenger carriers. "
            "Proof of insurance must be filed with FMCSA and updated as coverage changes. "
            "Failure to maintain coverage results in authority revocation and fines. "
            "Adversaries may claim coverage meets alternative standards or dispute coverage lapses. "
            "Resolution involves reviewing insurance certificates, FMCSA filings, and coverage history."
        ),
        key_factors=[
            "Minimum coverage levels",
            "FMCSA filing",
            "Coverage history",
            "Carrier type",
            "Hazmat or passenger operations"
        ],
        primary_authority=["49 CFR 387", "FMCSA Insurance Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier lacks required insurance or coverage lapse",
        counter_arguments=[
            "Coverage meets alternative standard",
            "Coverage lapse not reported",
            "Carrier exempt from requirement"
        ],
        resolution_strategy="Audit insurance certificates and FMCSA filings; review coverage history; verify exemption status.",
        entity_scope="Motor carriers, insurance companies, FMCSA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Insurance Policy, 2018"
    ),
    DoctrineBlock(
        topic="Roadside Inspection Levels and CVSA",
        keywords=["roadside inspection", "CVSA", "inspection levels", "out-of-service", "violation"],
        conclusion_template="CMVs are subject to roadside inspections at various levels as defined by CVSA, with violations resulting in out-of-service orders or enforcement actions.",
        reasoning_framework=(
            "The Commercial Vehicle Safety Alliance (CVSA) defines inspection levels for roadside enforcement: Level I (full inspection), Level II (walk-around), Level III (driver/credential), Level IV (special), Level V (vehicle-only), Level VI (radioactive material). "
            "Inspections assess driver credentials, vehicle condition, cargo securement, and regulatory compliance. "
            "Violations result in citations, fines, and out-of-service orders. "
            "Adversaries may contest inspection findings or claim procedural errors. "
            "Resolution involves reviewing inspection reports, violation documentation, and contestation procedures."
        ),
        key_factors=[
            "Inspection level",
            "Driver and vehicle compliance",
            "Violation documentation",
            "Out-of-service criteria",
            "Contestation process"
        ],
        primary_authority=["CVSA Inspection Guidance", "FMCSA Enforcement Policy"],
        burden_holder="Carrier and Driver",
        adversary_position="Violation found during inspection or procedural error",
        counter_arguments=[
            "Inspection findings disputed",
            "Procedural error in inspection",
            "Violation not applicable"
        ],
        resolution_strategy="Review inspection reports; assess contestation procedures; audit carrier compliance.",
        entity_scope="CMV carriers, drivers, enforcement agencies",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CVSA Inspection Policy, 2017"
    ),
    DoctrineBlock(
        topic="Wireless Communication Prohibition 49 CFR 392.82",
        keywords=["wireless communication", "cell phone", "texting", "49 CFR 392.82", "driver distraction"],
        conclusion_template="CMV drivers are prohibited from using handheld wireless communication devices while driving, including texting and calling, as specified in 49 CFR 392.82.",
        reasoning_framework=(
            "49 CFR 392.82 prohibits CMV drivers from using handheld mobile phones or texting while driving. "
            "Hands-free devices are permitted if operated in compliance with safety standards. "
            "Violations result in fines, disqualification, and carrier liability. "
            "Adversaries may claim device was hands-free or operation was emergency-related. "
            "Resolution involves reviewing phone records, driver statements, and device compliance."
        ),
        key_factors=[
            "Handheld device use",
            "Texting prohibition",
            "Hands-free compliance",
            "Emergency exception",
            "Carrier liability"
        ],
        primary_authority=["49 CFR 392.82", "FMCSA Guidance"],
        burden_holder="Driver and Carrier",
        adversary_position="Driver used handheld device or texted while driving",
        counter_arguments=[
            "Device was hands-free",
            "Operation was emergency-related",
            "No evidence of device use"
        ],
        resolution_strategy="Audit phone records; review driver statements; verify device compliance.",
        entity_scope="CMV drivers, carriers, enforcement agencies",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Wireless Communication Policy, 2016"
    ),
    DoctrineBlock(
        topic="Broker Authority and Bond 49 CFR 371",
        keywords=["broker authority", "bond", "49 CFR 371", "FMCSA", "freight broker"],
        conclusion_template="Freight brokers must obtain FMCSA authority and maintain a $75,000 surety bond or trust fund as specified in 49 CFR 371.",
        reasoning_framework=(
            "49 CFR 371 requires freight brokers to obtain FMCSA authority and maintain a $75,000 surety bond or trust fund to protect shippers and carriers. "
            "Authority is granted via registration and compliance with financial responsibility requirements. "
            "Violations include operating without authority or bond, resulting in fines and revocation. "
            "Adversaries may claim exemption or bond compliance through alternative means. "
            "Resolution involves reviewing authority status, bond documentation, and exemption applicability."
        ),
        key_factors=[
            "FMCSA broker authority",
            "Surety bond/trust fund",
            "Registration compliance",
            "Financial responsibility",
            "Exemption applicability"
        ],
        primary_authority=["49 CFR 371", "FMCSA Broker Guidance"],
        burden_holder="Broker",
        adversary_position="Broker operated without authority or failed to maintain bond",
        counter_arguments=[
            "Bond maintained through alternative means",
            "Authority pending",
            "Broker exempt from requirement"
        ],
        resolution_strategy="Verify broker authority and bond status; review exemption applicability; audit registration records.",
        entity_scope="Freight brokers, FMCSA, shippers, carriers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Broker Policy, 2017"
    ),
    DoctrineBlock(
        topic="Passenger Carrier Safety 49 CFR 390-399",
        keywords=["passenger carrier", "safety", "49 CFR 390-399", "driver qualification", "vehicle maintenance"],
        conclusion_template="Passenger carriers must comply with FMCSA safety regulations in 49 CFR 390-399, including driver qualification, vehicle maintenance, and operational safety.",
        reasoning_framework=(
            "49 CFR 390-399 establishes safety regulations for passenger carriers. "
            "Drivers must meet qualification standards, including medical certification and training. "
            "Vehicles must be maintained per inspection and repair requirements. "
            "Operational safety includes compliance with HOS, cargo securement, and emergency procedures. "
            "Violations include unqualified drivers, maintenance lapses, or operational safety breaches. "
            "Adversaries may claim compliance through alternative programs or contest qualification findings. "
            "Resolution involves reviewing driver qualification records, maintenance logs, and operational safety documentation."
        ),
        key_factors=[
            "Driver qualification",
            "Vehicle maintenance",
            "Operational safety",
            "Record retention",
            "Emergency procedures"
        ],
        primary_authority=["49 CFR 390-399", "FMCSA Passenger Carrier Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to qualify driver, maintain vehicle, or ensure operational safety",
        counter_arguments=[
            "Alternative qualification program approved",
            "Maintenance performed per manufacturer",
            "Operational safety procedures followed"
        ],
        resolution_strategy="Audit driver and maintenance records; review operational safety procedures; verify alternative approvals.",
        entity_scope="Passenger carriers, drivers, FMCSA",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Passenger Carrier Policy, 2018"
    ),
    DoctrineBlock(
        topic="Transportation Worker Identification Credential TWIC",
        keywords=["TWIC", "transportation worker", "identification credential", "security", "port access"],
        conclusion_template="Workers requiring unescorted access to secure port facilities must possess a valid TWIC as mandated by TSA and USCG regulations.",
        reasoning_framework=(
            "TWIC is a biometric identification credential required for workers needing unescorted access to secure port facilities. "
            "Applicants must undergo background checks and fingerprinting. "
            "TWIC must be renewed periodically and presented upon request. "
            "Violations include unauthorized access or expired credentials. "
            "Adversaries may claim credential pending or access was escorted. "
            "Resolution involves reviewing TWIC status, access logs, and escort documentation."
        ),
        key_factors=[
            "TWIC issuance",
            "Background check",
            "Credential renewal",
            "Access logs",
            "Escort documentation"
        ],
        primary_authority=["TSA TWIC Guidance", "USCG Regulations"],
        burden_holder="Worker and Employer",
        adversary_position="Worker accessed secure area without valid TWIC",
        counter_arguments=[
            "Credential pending",
            "Access was escorted",
            "TWIC expired recently"
        ],
        resolution_strategy="Verify TWIC status; review access logs; assess escort documentation.",
        entity_scope="Port workers, employers, TSA, USCG",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="USCG TWIC Policy, 2017"
    ),
    DoctrineBlock(
        topic="Fatality Analysis Reporting System FARS",
        keywords=["FARS", "fatality analysis", "reporting system", "crash data", "NHTSA"],
        conclusion_template="Transportation fatalities must be reported and analyzed in accordance with FARS protocols as administered by NHTSA.",
        reasoning_framework=(
            "FARS is a nationwide database for reporting and analyzing transportation-related fatalities. "
            "State agencies collect crash data, including vehicle, driver, and environmental factors. "
            "Data is used for policy development, enforcement, and safety improvement. "
            "Violations include failure to report or inaccurate data submission. "
            "Adversaries may claim reporting delay or data error. "
            "Resolution involves reviewing crash reports, data submission logs, and correction procedures."
        ),
        key_factors=[
            "Crash data collection",
            "Reporting timeliness",
            "Data accuracy",
            "Correction procedures",
            "Policy development"
        ],
        primary_authority=["NHTSA FARS Guidance", "State DOT Reporting Regulations"],
        burden_holder="State Agency",
        adversary_position="Agency failed to report fatality or submitted inaccurate data",
        counter_arguments=[
            "Reporting delay justified",
            "Data error corrected",
            "Fatality not transportation-related"
        ],
        resolution_strategy="Audit crash reports and data logs; review correction procedures; assess reporting justification.",
        entity_scope="State agencies, NHTSA, DOTs",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NHTSA FARS Policy, 2018"
    ),
    # Additional doctrine blocks for domain coverage (20+ more for 40+ total)
    DoctrineBlock(
        topic="Driver Fitness BASIC",
        keywords=["driver fitness", "BASIC", "CSA", "qualification", "medical certification"],
        conclusion_template="Carrier's Driver Fitness BASIC score reflects compliance with driver qualification and medical certification standards.",
        reasoning_framework=(
            "Driver Fitness BASIC evaluates carriers on driver qualification, medical certification, and licensing. "
            "Violations include unqualified drivers, expired medical certificates, or improper licensing. "
            "Scores impact intervention risk and carrier safety rating. "
            "Resolution involves reviewing qualification records, medical certificates, and licensing documentation."
        ),
        key_factors=[
            "Driver qualification",
            "Medical certification",
            "Licensing",
            "Violation history",
            "Record retention"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 391"],
        burden_holder="Carrier",
        adversary_position="Carrier employs unqualified or medically unfit drivers",
        counter_arguments=[
            "Driver qualification records updated",
            "Medical certificate pending renewal",
            "Licensing compliant"
        ],
        resolution_strategy="Audit driver qualification and medical records; review licensing status.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="Unsafe Driving BASIC",
        keywords=["unsafe driving", "BASIC", "CSA", "traffic violation", "speeding"],
        conclusion_template="Carrier's Unsafe Driving BASIC score reflects frequency and severity of traffic violations by drivers.",
        reasoning_framework=(
            "Unsafe Driving BASIC measures carrier performance based on traffic violations such as speeding, reckless driving, and improper lane changes. "
            "Scores are updated monthly and impact intervention risk. "
            "Resolution involves reviewing violation records, driver training, and contestation procedures."
        ),
        key_factors=[
            "Traffic violation frequency",
            "Violation severity",
            "Driver training",
            "Record retention",
            "Contestation process"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 392"],
        burden_holder="Carrier",
        adversary_position="Carrier drivers commit frequent or severe traffic violations",
        counter_arguments=[
            "Violation incorrectly attributed",
            "Driver training implemented",
            "Violation contested"
        ],
        resolution_strategy="Audit violation records; review driver training; assess contestation procedures.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="Crash Indicator BASIC",
        keywords=["crash indicator", "BASIC", "CSA", "crash history", "intervention"],
        conclusion_template="Carrier's Crash Indicator BASIC score reflects crash history and impacts intervention risk.",
        reasoning_framework=(
            "Crash Indicator BASIC measures carrier performance based on crash history, including frequency and severity. "
            "Scores are confidential and used for intervention targeting. "
            "Resolution involves reviewing crash reports, safety program, and contestation procedures."
        ),
        key_factors=[
            "Crash frequency",
            "Crash severity",
            "Safety program",
            "Record retention",
            "Contestation process"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 385"],
        burden_holder="Carrier",
        adversary_position="Carrier has high crash frequency or severity",
        counter_arguments=[
            "Crash not preventable",
            "Safety program implemented",
            "Crash report error"
        ],
        resolution_strategy="Audit crash reports; review safety program; assess contestation procedures.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="Controlled Substances/Alcohol BASIC",
        keywords=["controlled substances", "alcohol", "BASIC", "CSA", "drug testing"],
        conclusion_template="Carrier's Controlled Substances/Alcohol BASIC score reflects compliance with drug and alcohol testing regulations.",
        reasoning_framework=(
            "Controlled Substances/Alcohol BASIC measures carrier compliance with drug and alcohol testing, including random, pre-employment, and post-accident testing. "
            "Violations include positive tests, refusal, or procedural lapses. "
            "Resolution involves reviewing testing records, program implementation, and contestation procedures."
        ),
        key_factors=[
            "Testing program",
            "Random selection",
            "Positive test",
            "Refusal",
            "Record retention"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 382"],
        burden_holder="Carrier",
        adversary_position="Carrier fails to implement testing program or drivers test positive",
        counter_arguments=[
            "Testing program implemented",
            "False positive",
            "Procedural error"
        ],
        resolution_strategy="Audit testing records; review program implementation; assess contestation procedures.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="Hazardous Materials BASIC",
        keywords=["hazardous materials", "BASIC", "CSA", "PHMSA", "hazmat compliance"],
        conclusion_template="Carrier's Hazardous Materials BASIC score reflects compliance with PHMSA regulations for hazmat transportation.",
        reasoning_framework=(
            "Hazardous Materials BASIC measures carrier compliance with PHMSA regulations, including classification, packaging, labeling, and placarding. "
            "Violations include improper handling, missing placards, or untrained drivers. "
            "Resolution involves reviewing hazmat records, driver training, and contestation procedures."
        ),
        key_factors=[
            "Material classification",
            "Packaging",
            "Labeling and placarding",
            "Driver training",
            "Record retention"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 171-180"],
        burden_holder="Carrier",
        adversary_position="Carrier fails to comply with hazmat regulations or drivers untrained",
        counter_arguments=[
            "Hazmat records compliant",
            "Driver training implemented",
            "Violation contested"
        ],
        resolution_strategy="Audit hazmat records; review driver training; assess contestation procedures.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="Vehicle Maintenance BASIC",
        keywords=["vehicle maintenance", "BASIC", "CSA", "inspection", "repair"],
        conclusion_template="Carrier's Vehicle Maintenance BASIC score reflects compliance with inspection and repair regulations.",
        reasoning_framework=(
            "Vehicle Maintenance BASIC measures carrier compliance with inspection, maintenance, and repair regulations. "
            "Violations include unresolved defects, missed inspections, or inadequate repairs. "
            "Resolution involves reviewing maintenance records, inspection logs, and contestation procedures."
        ),
        key_factors=[
            "Inspection frequency",
            "Maintenance records",
            "Repair documentation",
            "Defect resolution",
            "Record retention"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 396"],
        burden_holder="Carrier",
        adversary_position="Carrier fails to maintain vehicles or resolve defects",
        counter_arguments=[
            "Maintenance records compliant",
            "Defect resolved",
            "Violation contested"
        ],
        resolution_strategy="Audit maintenance and inspection records; review repair documentation; assess contestation procedures.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="HOS Compliance BASIC",
        keywords=["HOS compliance", "BASIC", "CSA", "hours of service", "logbook"],
        conclusion_template="Carrier's HOS Compliance BASIC score reflects adherence to hours of service regulations and logbook accuracy.",
        reasoning_framework=(
            "HOS Compliance BASIC measures carrier adherence to hours of service regulations, including logbook accuracy and ELD use. "
            "Violations include exceeding HOS limits, inaccurate logs, or ELD malfunctions. "
            "Resolution involves reviewing logbooks, ELD records, and contestation procedures."
        ),
        key_factors=[
            "Logbook accuracy",
            "ELD compliance",
            "HOS limits",
            "Record retention",
            "Contestation process"
        ],
        primary_authority=["FMCSA CSA Guidance", "49 CFR 395"],
        burden_holder="Carrier",
        adversary_position="Carrier fails to comply with HOS or logbook requirements",
        counter_arguments=[
            "Logbook accurate",
            "ELD compliant",
            "Violation contested"
        ],
        resolution_strategy="Audit logbooks and ELD records; review HOS compliance; assess contestation procedures.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA CSA Policy, 2018"
    ),
    DoctrineBlock(
        topic="Crash Reporting 49 CFR 390.15",
        keywords=["crash reporting", "49 CFR 390.15", "accident", "record retention"],
        conclusion_template="Motor carriers must report crashes and retain records as specified in 49 CFR 390.15.",
        reasoning_framework=(
            "49 CFR 390.15 requires motor carriers to report crashes involving fatalities, injuries, or tow-away and retain records for three years. "
            "Records include police reports, insurance documents, and carrier investigation. "
            "Resolution involves reviewing crash reports, record retention, and compliance procedures."
        ),
        key_factors=[
            "Crash reporting",
            "Record retention",
            "Police report",
            "Insurance documentation",
            "Carrier investigation"
        ],
        primary_authority=["49 CFR 390.15", "FMCSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to report crash or retain records",
        counter_arguments=[
            "Crash not reportable",
            "Records retained",
            "Reporting delay justified"
        ],
        resolution_strategy="Audit crash reporting and records; review compliance procedures.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Crash Reporting Policy, 2017"
    ),
    DoctrineBlock(
        topic="Driver Qualification File 49 CFR 391.51",
        keywords=["driver qualification file", "49 CFR 391.51", "record retention", "employment history"],
        conclusion_template="Carriers must maintain driver qualification files with specified records as required by 49 CFR 391.51.",
        reasoning_framework=(
            "49 CFR 391.51 requires carriers to maintain driver qualification files, including employment history, medical certificates, driving records, and training documentation. "
            "Files must be retained for the duration of employment and three years after. "
            "Resolution involves reviewing qualification files and compliance with retention requirements."
        ),
        key_factors=[
            "Employment history",
            "Medical certificate",
            "Driving record",
            "Training documentation",
            "Record retention"
        ],
        primary_authority=["49 CFR 391.51", "FMCSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to maintain qualification files or records missing",
        counter_arguments=[
            "Records maintained",
            "Retention period met",
            "File completeness disputed"
        ],
        resolution_strategy="Audit qualification files; review retention compliance.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Qualification File Policy, 2017"
    ),
    DoctrineBlock(
        topic="Annual Vehicle Inspection Report 49 CFR 396.21",
        keywords=["annual vehicle inspection", "49 CFR 396.21", "inspection report", "record retention"],
        conclusion_template="Carriers must perform annual vehicle inspections and retain reports as required by 49 CFR 396.21.",
        reasoning_framework=(
            "49 CFR 396.21 requires carriers to perform annual vehicle inspections by qualified personnel and retain reports for 14 months. "
            "Reports must document inspection results, defects, and repairs. "
            "Resolution involves reviewing inspection reports and retention compliance."
        ),
        key_factors=[
            "Inspection frequency",
            "Inspector qualification",
            "Defect documentation",
            "Repair records",
            "Record retention"
        ],
        primary_authority=["49 CFR 396.21", "FMCSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to perform annual inspection or retain report",
        counter_arguments=[
            "Inspection performed",
            "Report retained",
            "Inspector qualified"
        ],
        resolution_strategy="Audit inspection reports; review retention compliance.",
        entity_scope="Motor carriers, FMCSA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMCSA Inspection Report Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Employee Training 49 CFR 172.704",
        keywords=["hazmat employee training", "49 CFR 172.704", "training records", "hazardous materials"],
        conclusion_template="Hazmat employees must receive training and carriers must retain records as required by 49 CFR 172.704.",
        reasoning_framework=(
            "49 CFR 172.704 requires hazmat employees to receive training in general awareness, function-specific, safety, and security. "
            "Training must be repeated every three years and records retained. "
            "Resolution involves reviewing training records and compliance procedures."
        ),
        key_factors=[
            "Training content",
            "Training frequency",
            "Record retention",
            "Employee qualification",
            "Compliance procedures"
        ],
        primary_authority=["49 CFR 172.704", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to train hazmat employees or retain records",
        counter_arguments=[
            "Training provided",
            "Records retained",
            "Employee exempt"
        ],
        resolution_strategy="Audit training records; review compliance procedures.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Training Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Registration 49 CFR 107.601",
        keywords=["hazmat registration", "49 CFR 107.601", "PHMSA", "registration certificate"],
        conclusion_template="Hazmat carriers must register with PHMSA and retain registration certificates as required by 49 CFR 107.601.",
        reasoning_framework=(
            "49 CFR 107.601 requires hazmat carriers to register with PHMSA and retain registration certificates for inspection. "
            "Registration must be renewed annually and certificates available for enforcement review. "
            "Resolution involves reviewing registration status and certificate retention."
        ),
        key_factors=[
            "Registration status",
            "Certificate retention",
            "Renewal frequency",
            "PHMSA compliance",
            "Inspection availability"
        ],
        primary_authority=["49 CFR 107.601", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to register or retain certificate",
        counter_arguments=[
            "Registration current",
            "Certificate available",
            "Carrier exempt"
        ],
        resolution_strategy="Verify registration status; review certificate retention.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Registration Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Security Plan 49 CFR 172.800",
        keywords=["hazmat security plan", "49 CFR 172.800", "security assessment", "hazardous materials"],
        conclusion_template="Hazmat carriers must develop and implement security plans as required by 49 CFR 172.800.",
        reasoning_framework=(
            "49 CFR 172.800 requires carriers transporting certain hazardous materials to develop and implement security plans, including personnel security, unauthorized access prevention, and en route security. "
            "Plans must be reviewed annually and updated as needed. "
            "Resolution involves reviewing security plan documentation and compliance procedures."
        ),
        key_factors=[
            "Security plan content",
            "Personnel security",
            "Access prevention",
            "En route security",
            "Annual review"
        ],
        primary_authority=["49 CFR 172.800", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to develop or implement security plan",
        counter_arguments=[
            "Plan developed",
            "Annual review performed",
            "Carrier exempt"
        ],
        resolution_strategy="Audit security plan documentation; review compliance procedures.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Security Plan Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Shipping Paper 49 CFR 172.201",
        keywords=["hazmat shipping paper", "49 CFR 172.201", "documentation", "hazardous materials"],
        conclusion_template="Hazmat shipments must be accompanied by shipping papers meeting requirements of 49 CFR 172.201.",
        reasoning_framework=(
            "49 CFR 172.201 requires hazmat shipments to be accompanied by shipping papers with proper description, emergency response information, and accessibility. "
            "Papers must be retained for three years and available for inspection. "
            "Resolution involves reviewing shipping papers and compliance procedures."
        ),
        key_factors=[
            "Proper description",
            "Emergency response info",
            "Accessibility",
            "Record retention",
            "Inspection availability"
        ],
        primary_authority=["49 CFR 172.201", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to provide proper shipping papers",
        counter_arguments=[
            "Papers compliant",
            "Records retained",
            "Carrier exempt"
        ],
        resolution_strategy="Audit shipping papers; review compliance procedures.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Shipping Paper Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Placarding 49 CFR 172.504",
        keywords=["hazmat placarding", "49 CFR 172.504", "placard", "hazardous materials"],
        conclusion_template="Hazmat shipments must display placards as required by 49 CFR 172.504.",
        reasoning_framework=(
            "49 CFR 172.504 requires hazmat shipments to display placards indicating hazard class, quantity, and compatibility. "
            "Placards must be visible, durable, and compliant with size and color standards. "
            "Resolution involves reviewing placard placement, compliance, and inspection records."
        ),
        key_factors=[
            "Placard visibility",
            "Hazard class",
            "Quantity threshold",
            "Durability",
            "Inspection records"
        ],
        primary_authority=["49 CFR 172.504", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to display required placards",
        counter_arguments=[
            "Placards compliant",
            "Quantity below threshold",
            "Carrier exempt"
        ],
        resolution_strategy="Audit placard placement; review compliance and inspection records.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Placarding Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Package Marking 49 CFR 172.301",
        keywords=["hazmat package marking", "49 CFR 172.301", "marking", "hazardous materials"],
        conclusion_template="Hazmat packages must be marked as required by 49 CFR 172.301.",
        reasoning_framework=(
            "49 CFR 172.301 requires hazmat packages to be marked with proper shipping name, identification number, and hazard class. "
            "Marks must be durable, legible, and placed in visible locations. "
            "Resolution involves reviewing package marking and compliance records."
        ),
        key_factors=[
            "Proper shipping name",
            "Identification number",
            "Hazard class",
            "Durability",
            "Visibility"
        ],
        primary_authority=["49 CFR 172.301", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to mark packages as required",
        counter_arguments=[
            "Marks compliant",
            "Package exempt",
            "Marking error corrected"
        ],
        resolution_strategy="Audit package marking; review compliance records.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Package Marking Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Emergency Response Information 49 CFR 172.600",
        keywords=["hazmat emergency response", "49 CFR 172.600", "emergency info", "hazardous materials"],
        conclusion_template="Hazmat shipments must be accompanied by emergency response information as required by 49 CFR 172.600.",
        reasoning_framework=(
            "49 CFR 172.600 requires hazmat shipments to be accompanied by emergency response information, including contact numbers, hazard description, and mitigation procedures. "
            "Information must be accessible to drivers and responders. "
            "Resolution involves reviewing emergency info and compliance records."
        ),
        key_factors=[
            "Contact numbers",
            "Hazard description",
            "Mitigation procedures",
            "Accessibility",
            "Record retention"
        ],
        primary_authority=["49 CFR 172.600", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to provide emergency response info",
        counter_arguments=[
            "Info compliant",
            "Records retained",
            "Carrier exempt"
        ],
        resolution_strategy="Audit emergency info; review compliance records.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Emergency Response Policy, 2017"
    ),
    DoctrineBlock(
        topic="Hazmat Incident Reporting 49 CFR 171.15",
        keywords=["hazmat incident reporting", "49 CFR 171.15", "incident", "hazardous materials"],
        conclusion_template="Hazmat incidents must be reported to PHMSA as required by 49 CFR 171.15.",
        reasoning_framework=(
            "49 CFR 171.15 requires carriers to report hazmat incidents involving death, injury, property damage, or release to PHMSA within 12 hours. "
            "Reports must include incident details, material description, and mitigation actions. "
            "Resolution involves reviewing incident reports and compliance procedures."
        ),
        key_factors=[
            "Incident details",
            "Material description",
            "Mitigation actions",
            "Reporting timeliness",
            "Record retention"
        ],
        primary_authority=["49 CFR 171.15", "PHMSA Guidance"],
        burden_holder="Carrier",
        adversary_position="Carrier failed to report incident or delayed reporting",
        counter_arguments=[
            "Incident not reportable",
            "Reporting delay justified",
            "Records retained"
        ],
        resolution_strategy="Audit incident reports; review compliance procedures.",
        entity_scope="Motor carriers, PHMSA",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA Incident Reporting Policy, 2017"
    ),
    DoctrineBlock(
        topic="Railroad Employee Qualification 49 CFR 243",
        keywords=["railroad employee qualification", "49 CFR 243", "training", "qualification"],
        conclusion_template="Railroad employees must be qualified and trained as required by 49 CFR 243.",
        reasoning_framework=(
            "49 CFR 243 requires railroad employees in safety-sensitive positions to be qualified and trained, including initial and recurrent training. "
            "Records must be retained and available for inspection. "
            "Resolution involves reviewing training records and qualification documentation."
        ),
        key_factors=[
            "Training content",
            "Qualification",
            "Recurrent training",
            "Record retention",
            "Inspection availability"
        ],
        primary_authority=["49 CFR 243", "FRA Guidance"],
        burden_holder="Railroad Operator",
        adversary_position="Operator failed to qualify or train employees",
        counter_arguments=[
            "Training provided",
            "Records retained",
            "Employee exempt"
        ],
        resolution_strategy="Audit training records; review qualification documentation.",
        entity_scope="Railroad operators, FRA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Employee Qualification Policy, 2017"
    ),
    DoctrineBlock(
        topic="Railroad Track Inspection 49 CFR 213",
        keywords=["railroad track inspection", "49 CFR 213", "inspection frequency", "defect remediation"],
        conclusion_template="Railroad tracks must be inspected and defects remediated as required by 49 CFR 213.",
        reasoning_framework=(
            "49 CFR 213 requires railroad tracks to be inspected at specified intervals and defects remediated promptly. "
            "Inspection records must be retained and available for FRA review. "
            "Resolution involves reviewing inspection logs and defect remediation documentation."
        ),
        key_factors=[
            "Inspection frequency",
            "Defect remediation",
            "Record retention",
            "Inspector qualification",
            "FRA review"
        ],
        primary_authority=["49 CFR 213", "FRA Guidance"],
        burden_holder="Railroad Operator",
        adversary_position="Operator failed to inspect tracks or remediate defects",
        counter_arguments=[
            "Inspection performed",
            "Defect remediated",
            "Records retained"
        ],
        resolution_strategy="Audit inspection logs; review defect remediation documentation.",
        entity_scope="Railroad operators, FRA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Track Inspection Policy, 2017"
    ),
    DoctrineBlock(
        topic="Railroad Signal System Maintenance 49 CFR 236",
        keywords=["railroad signal system maintenance", "49 CFR 236", "maintenance records", "signal testing"],
        conclusion_template="Railroad signal systems must be maintained and tested as required by 49 CFR 236.",
        reasoning_framework=(
            "49 CFR 236 requires railroad signal systems to be maintained and tested at specified intervals. "
            "Maintenance records must be retained and available for FRA review. "
            "Resolution involves reviewing maintenance logs and signal testing documentation."
        ),
        key_factors=[
            "Maintenance frequency",
            "Signal testing",
            "Record retention",
            "Inspector qualification",
            "FRA review"
        ],
        primary_authority=["49 CFR 236", "FRA Guidance"],
        burden_holder="Railroad Operator",
        adversary_position="Operator failed to maintain or test signal systems",
        counter_arguments=[
            "Maintenance performed",
            "Testing compliant",
            "Records retained"
        ],
        resolution_strategy="Audit maintenance logs; review signal testing documentation.",
        entity_scope="Railroad operators, FRA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Signal System Policy, 2017"
    ),
    DoctrineBlock(
        topic="Railroad Safety Reporting 49 CFR 225",
        keywords=["railroad safety reporting", "49 CFR 225", "incident reporting", "record retention"],
        conclusion_template="Railroad incidents must be reported and records retained as required by 49 CFR 225.",
        reasoning_framework=(
            "49 CFR 225 requires railroad operators to report safety incidents, including accidents, injuries, and fatalities, to FRA. "
            "Records must be retained for five years and available for review. "
            "Resolution involves reviewing incident reports and record retention compliance."
        ),
        key_factors=[
            "Incident reporting",
            "Record retention",
            "Accident documentation",
            "FRA review",
            "Compliance procedures"
        ],
        primary_authority=["49 CFR 225", "FRA Guidance"],
        burden_holder="Railroad Operator",
        adversary_position="Operator failed to report incidents or retain records",
        counter_arguments=[
            "Reporting compliant",
            "Records retained",
            "Incident not reportable"
        ],
        resolution_strategy="Audit incident reports; review record retention compliance.",
        entity_scope="Railroad operators, FRA",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Safety Reporting Policy, 2017"
    ),
    DoctrineBlock(
        topic="Aviation Pilot Certification 14 CFR Part 61",
        keywords=["aviation pilot certification", "14 CFR Part 61", "pilot license", "training"],
        conclusion_template="Pilots must be certified and licensed as required by 14 CFR Part 61.",
        reasoning_framework=(
            "14 CFR Part 61 requires pilots to be certified and licensed, including initial and recurrent training. "
            "Certificates must be current and available for FAA inspection. "
            "Resolution involves reviewing pilot certificates and training records."
        ),
        key_factors=[
            "Certification",
            "License",
            "Training",
            "Record retention",
            "FAA inspection"
        ],
        primary_authority=["14 CFR Part 61", "FAA Guidance"],
        burden_holder="Pilot",
        adversary_position="Pilot lacks certification or license",
        counter_arguments=[
            "Certificate current",
            "Training performed",
            "License available"
        ],
        resolution_strategy="Verify pilot certification and license; review training records.",
        entity_scope="Pilots, FAA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA Pilot Certification Policy, 2017"
    ),
    DoctrineBlock(
        topic="Aviation Aircraft Maintenance 14 CFR Part 43",
        keywords=["aviation aircraft maintenance", "14 CFR Part 43", "maintenance records", "airworthiness"],
        conclusion_template="Aircraft must be maintained and records retained as required by 14 CFR Part 43.",
        reasoning_framework=(
            "14 CFR Part 43 requires aircraft to be maintained per manufacturer and FAA standards, with records retained for inspection. "
            "Maintenance must be performed by qualified personnel and documented. "
            "Resolution involves reviewing maintenance logs and airworthiness documentation."
        ),
        key_factors=[
            "Maintenance standards",
            "Qualified personnel",
            "Record retention",
            "Airworthiness",
            "FAA inspection"
        ],
        primary_authority=["14 CFR Part 43", "FAA Guidance"],
        burden_holder="Aircraft Operator",
        adversary_position="Operator failed to maintain aircraft or retain records",
        counter_arguments=[
            "Maintenance performed",
            "Records retained",
            "Airworthiness compliant"
        ],
        resolution_strategy="Audit maintenance logs; review airworthiness documentation.",
        entity_scope="Aircraft operators, FAA",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA Aircraft Maintenance Policy, 2017"
    ),
    DoctrineBlock(
        topic="Aviation Operational Control 14 CFR Part 119",
        keywords=["aviation operational control", "14 CFR Part 119", "flight operations", "control procedures"],
        conclusion_template="Air carriers must maintain operational control as required by 14 CFR Part 119.",
        reasoning_framework=(
            "14 CFR Part 119 requires air carriers to maintain operational control over flight operations, including dispatch, crew scheduling, and emergency procedures. "
            "Records must be retained and available for FAA review. "
            "Resolution involves reviewing operational control documentation and compliance procedures."
        ),
        key_factors=[
            "Dispatch",
            "Crew scheduling",
            "Emergency procedures",
            "Record retention",
            "FAA review"
        ],
        primary_authority=["14 CFR Part 119", "FAA Guidance"],
        burden_holder="Air Carrier",
        adversary_position="Carrier failed to maintain operational control",
        counter_arguments=[
            "Control procedures implemented",
            "Records retained",
            "FAA compliant"
        ],
        resolution_strategy="Audit operational control documentation; review compliance procedures.",
        entity_scope="Air carriers, FAA",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA Operational Control Policy, 2017"
    ),
    DoctrineBlock(
        topic="Aviation Safety Reporting 14 CFR Part 91.25",
        keywords=["aviation safety reporting", "14 CFR Part 91.25", "incident reporting", "record retention"],
        conclusion_template="Aircraft incidents must be reported and records retained as required by 14 CFR Part 91.25.",
        reasoning_framework=(
            "14 CFR Part 91.25 requires aircraft operators to report safety incidents, including accidents and mechanical failures, to FAA. "
            "Records must be retained for five years and available for review. "
            "Resolution involves reviewing incident reports and record retention compliance."
        ),
        key_factors=[
            "Incident reporting",
            "Record retention",
            "Accident documentation",
            "FAA review",
            "Compliance procedures"
        ],
        primary_authority=["14 CFR Part 91.25", "FAA Guidance"],
        burden_holder="Aircraft Operator",
        adversary_position="Operator failed to report incidents or retain records",
        counter_arguments=[
            "Reporting compliant",
            "Records retained",
            "Incident not reportable"
        ],
        resolution_strategy="Audit incident reports; review record retention compliance.",
        entity_scope="Aircraft operators, FAA",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FAA Safety Reporting Policy, 2017"
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