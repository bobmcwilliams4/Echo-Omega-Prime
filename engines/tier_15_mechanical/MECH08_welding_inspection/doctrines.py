from dataclasses import dataclass
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
        topic="SMAW Stick Welding Process Selection",
        keywords=["SMAW", "Stick Welding", "Process Selection", "Manual Welding", "Shielded Metal Arc Welding"],
        conclusion_template="SMAW is selected for field welding applications requiring portability and versatility.",
        reasoning_framework="""SMAW is chosen based on its adaptability to various site conditions, minimal equipment requirements, and suitability for ferrous metals. The process is preferred where access is limited and power sources are constrained. Selection is guided by material thickness, joint configuration, and environmental factors such as wind and humidity. SMAW electrodes offer a range of AWS classifications, allowing tailored mechanical properties. The process is less sensitive to surface contaminants than GMAW or GTAW, making it ideal for maintenance and repair. The decision matrix weighs cost, productivity, and weld quality, referencing ASME Section IX and AWS D1.1 for procedural compliance. Operator skill and welder qualification are critical, with performance tests required under ASME IX. The selection is validated by historical performance in similar applications and consultation with welding engineers.""",
        key_factors=["Portability", "Material Compatibility", "Joint Accessibility", "Electrode Selection", "Operator Skill"],
        primary_authority=["ASME Section IX", "AWS D1.1"],
        burden_holder="Welding Engineer",
        adversary_position="GMAW/MIG may offer higher productivity and cleaner welds in controlled environments.",
        counter_arguments=[
            "GMAW requires shielding gas and is less portable.",
            "GTAW offers superior weld quality but is slower and more expensive.",
            "SMAW may produce more slag and require additional cleaning."
        ],
        resolution_strategy="Compare process suitability via weld trials and reference procedural standards.",
        entity_scope="Field Welding Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 3.0"
    ),
    DoctrineBlock(
        topic="GMAW/MIG Welding Process Parameters",
        keywords=["GMAW", "MIG", "Welding Parameters", "Shielding Gas", "Wire Feed", "Voltage", "Current"],
        conclusion_template="GMAW parameters are set according to material thickness, joint design, and AWS D1.1 recommendations.",
        reasoning_framework="""Parameter selection for GMAW involves balancing wire feed speed, voltage, and amperage to achieve optimal penetration and bead profile. Shielding gas composition (typically Argon-CO2 blends) is chosen based on base metal and desired mechanical properties. Joint design and material thickness dictate heat input, with thicker materials requiring higher amperage. Travel speed and torch angle are adjusted to minimize defects such as porosity and lack of fusion. Reference tables in AWS D1.1 and manufacturer guidelines provide baseline settings, which are fine-tuned during procedure qualification. Welders must monitor arc stability and adjust parameters to compensate for variations in fit-up and environmental conditions. Quality control includes destructive and non-destructive testing per ASME IX. Documentation of parameter settings is mandatory for traceability and compliance.""",
        key_factors=["Wire Feed Speed", "Voltage", "Amperage", "Shielding Gas", "Travel Speed"],
        primary_authority=["AWS D1.1", "ASME Section IX"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper parameter selection may lead to weld defects and non-compliance.",
        counter_arguments=[
            "Manual adjustments may be inconsistent.",
            "Automated systems can improve repeatability but require calibration.",
            "Environmental factors can affect shielding gas effectiveness."
        ],
        resolution_strategy="Establish parameter ranges via procedure qualification and monitor with in-process controls.",
        entity_scope="Shop and Field Welding",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Table 4.5"
    ),
    DoctrineBlock(
        topic="GTAW/TIG Welding for Critical Applications",
        keywords=["GTAW", "TIG", "Critical Applications", "Precision Welding", "Stainless Steel", "Alloy"],
        conclusion_template="GTAW is mandated for critical joints requiring high integrity and minimal contamination.",
        reasoning_framework="""GTAW is selected for applications demanding superior weld quality, such as pressure vessels, piping, and aerospace structures. The process offers precise control over heat input and filler addition, minimizing distortion and ensuring clean welds. GTAW is preferred for stainless steels, nickel alloys, and thin sections where contamination and oxidation must be avoided. Procedure qualification per ASME IX includes rigorous testing for mechanical properties and corrosion resistance. Welder performance qualification is essential, with periodic requalification required. Shielding gas purity and flow rates are monitored to prevent atmospheric contamination. Joint preparation and fit-up are critical, with strict adherence to cleanliness standards. Inspection protocols include radiography and ultrasonic testing, referencing API 1104 and AWS D1.6 for acceptance criteria. Documentation ensures traceability and compliance.""",
        key_factors=["Weld Quality", "Material Sensitivity", "Heat Input Control", "Shielding Gas Purity", "Joint Preparation"],
        primary_authority=["ASME Section IX", "API 1104", "AWS D1.6"],
        burden_holder="Quality Assurance Manager",
        adversary_position="GMAW may be faster but lacks precision for critical joints.",
        counter_arguments=[
            "GTAW is slower and more costly.",
            "Requires highly skilled operators.",
            "Limited productivity compared to semi-automatic processes."
        ],
        resolution_strategy="Mandate GTAW for critical applications via WPS and enforce qualification standards.",
        entity_scope="Critical Welds in Pressure Vessels and Piping",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="ASME Section IX QW-200"
    ),
    DoctrineBlock(
        topic="Welding Procedure Specification (WPS) per ASME Section IX",
        keywords=["WPS", "Procedure Specification", "ASME IX", "Qualification", "Documentation"],
        conclusion_template="WPS must be developed, qualified, and documented in accordance with ASME Section IX.",
        reasoning_framework="""A WPS outlines the essential variables for welding, including process, materials, joint design, preheat, interpass temperature, and post-weld heat treatment. Qualification involves producing test welds and subjecting them to mechanical and non-destructive tests as specified in ASME IX. Changes to essential variables require requalification. The WPS serves as the basis for welder qualification and ensures repeatability and compliance. Documentation includes records of procedure qualification tests (PQR) and welder performance qualification (WPQ). The WPS is reviewed and approved by the responsible engineer and maintained for traceability. Audits and inspections reference the WPS to verify adherence. The WPS is updated as new materials or processes are introduced, with revisions tracked per quality management system.""",
        key_factors=["Essential Variables", "Qualification Testing", "Documentation", "Traceability", "Revision Control"],
        primary_authority=["ASME Section IX"],
        burden_holder="Responsible Welding Engineer",
        adversary_position="Failure to qualify WPS may result in non-compliance and rejected welds.",
        counter_arguments=[
            "WPS development is time-consuming.",
            "Frequent changes to materials/processes require ongoing qualification.",
            "Lack of proper documentation undermines traceability."
        ],
        resolution_strategy="Implement robust qualification and documentation procedures per ASME IX.",
        entity_scope="All Welding Operations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="ASME Section IX QW-200.2"
    ),
    DoctrineBlock(
        topic="Welder Performance Qualification per ASME Section IX",
        keywords=["Welder Qualification", "Performance Test", "ASME IX", "WPQ", "Certification"],
        conclusion_template="Welder performance must be qualified and documented per ASME Section IX requirements.",
        reasoning_framework="""Welder qualification involves performing test welds under controlled conditions, followed by destructive and/or non-destructive testing to verify compliance with WPS requirements. Essential variables include process, position, material, and thickness. Successful completion results in issuance of a Welder Performance Qualification (WPQ) certificate, which is valid for a specified period and must be renewed if the welder ceases welding for more than six months. Qualification records are maintained for audit and traceability. The qualification process ensures welders possess the necessary skills and knowledge to produce compliant welds. Failure to qualify or lapses in certification may result in rejected welds and regulatory penalties. The process is overseen by the quality assurance department and reviewed by third-party inspectors as required.""",
        key_factors=["Test Welds", "Essential Variables", "Certification", "Traceability", "Renewal"],
        primary_authority=["ASME Section IX"],
        burden_holder="Quality Assurance Department",
        adversary_position="Unqualified welders may compromise weld integrity and compliance.",
        counter_arguments=[
            "Qualification tests may not reflect actual production conditions.",
            "Certification lapses can occur due to administrative oversight.",
            "Third-party verification may add cost and complexity."
        ],
        resolution_strategy="Enforce periodic qualification and maintain comprehensive records.",
        entity_scope="All Welders",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section IX QW-300"
    ),
    DoctrineBlock(
        topic="Preheat and Interpass Temperature Requirements",
        keywords=["Preheat", "Interpass Temperature", "Welding", "Heat Control", "ASME IX"],
        conclusion_template="Preheat and interpass temperatures are established per material and code requirements to prevent weld defects.",
        reasoning_framework="""Preheat is applied to reduce the risk of hydrogen-induced cracking and to improve weldability, especially in high-strength steels and thick sections. Interpass temperature control ensures consistent mechanical properties and prevents excessive heat input, which can cause grain growth or reduced toughness. Temperature requirements are specified in the WPS and verified using calibrated instruments. ASME IX and AWS D1.1 provide guidelines for minimum and maximum values. Failure to adhere may result in weld defects such as cracks or poor fusion. Monitoring is performed during welding, with records maintained for traceability. Adjustments are made based on ambient conditions and material thickness. The process is audited by quality assurance and reviewed during procedure qualification.""",
        key_factors=["Material Type", "Thickness", "Hydrogen Control", "Temperature Monitoring", "WPS Compliance"],
        primary_authority=["ASME Section IX", "AWS D1.1"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper temperature control can lead to weld failure and non-compliance.",
        counter_arguments=[
            "Ambient conditions can affect temperature maintenance.",
            "Insufficient preheat may not be detected without proper instrumentation.",
            "Excessive interpass temperature can degrade mechanical properties."
        ],
        resolution_strategy="Establish and monitor temperature requirements per WPS and code.",
        entity_scope="All Welding Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 5.10"
    ),
    DoctrineBlock(
        topic="Post-Weld Heat Treatment (PWHT) Requirements",
        keywords=["PWHT", "Post-Weld Heat Treatment", "Stress Relief", "ASME IX", "WPS"],
        conclusion_template="PWHT is performed as required by material, thickness, and code to relieve residual stresses and improve properties.",
        reasoning_framework="""PWHT is applied to reduce residual stresses, improve toughness, and restore mechanical properties after welding. Requirements are specified in the WPS and based on material type, thickness, and service conditions. ASME IX and API 1104 provide guidelines for temperature, duration, and cooling rates. PWHT is monitored using calibrated instruments, with records maintained for traceability. Failure to perform PWHT may result in brittle fracture, reduced fatigue life, and non-compliance. The process is validated during procedure qualification and reviewed by quality assurance. Exceptions may be granted for certain materials or weld configurations, but must be documented and justified. PWHT is critical for pressure vessels, pipelines, and sour service applications.""",
        key_factors=["Material Type", "Thickness", "Service Conditions", "Temperature Control", "Documentation"],
        primary_authority=["ASME Section IX", "API 1104"],
        burden_holder="Responsible Welding Engineer",
        adversary_position="Omitting PWHT may compromise weld integrity and violate code.",
        counter_arguments=[
            "PWHT adds cost and time to production.",
            "Some materials may not require PWHT.",
            "Improper PWHT can cause adverse effects."
        ],
        resolution_strategy="Perform PWHT per WPS and code, with exceptions documented.",
        entity_scope="Pressure Vessels, Pipelines",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section IX QW-407"
    ),
    DoctrineBlock(
        topic="Filler Metal Selection and AWS Classification",
        keywords=["Filler Metal", "AWS Classification", "Welding", "Material Compatibility", "Mechanical Properties"],
        conclusion_template="Filler metal is selected based on base material, service requirements, and AWS classification.",
        reasoning_framework="""Filler metal selection is guided by compatibility with base material, required mechanical properties, and service environment. AWS provides classification systems (e.g., E7018 for SMAW, ER70S-6 for GMAW) detailing chemical composition and performance characteristics. Selection is documented in the WPS and validated during procedure qualification. Considerations include strength, ductility, corrosion resistance, and weldability. For sour service, NACE MR0175/ISO 15156 requirements are referenced. Filler metal certificates and batch traceability are maintained for audit. Substitution or changes require requalification and approval. The process is overseen by welding engineers and quality assurance, with periodic review of supplier performance.""",
        key_factors=["Base Material", "Service Conditions", "Mechanical Properties", "AWS Classification", "Traceability"],
        primary_authority=["AWS", "ASME Section IX", "NACE MR0175/ISO 15156"],
        burden_holder="Welding Engineer",
        adversary_position="Incorrect filler selection may result in weld failure or non-compliance.",
        counter_arguments=[
            "Supplier variations can affect quality.",
            "Batch traceability may be difficult to maintain.",
            "Service conditions may change, requiring re-evaluation."
        ],
        resolution_strategy="Select filler metal per AWS and code, maintain traceability, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Table 3.1"
    ),
    DoctrineBlock(
        topic="Weld Joint Design and Preparation",
        keywords=["Joint Design", "Preparation", "Fit-Up", "Welding", "ASME IX"],
        conclusion_template="Joint design and preparation are performed per code and WPS to ensure weld quality and integrity.",
        reasoning_framework="""Joint design is determined based on material thickness, service requirements, and accessibility. Preparation includes cleaning, beveling, and fit-up to ensure proper penetration and fusion. ASME IX and AWS D1.1 provide guidelines for joint types and tolerances. Poor preparation can lead to defects such as lack of fusion, porosity, and cracks. Inspection of joint preparation is performed prior to welding, with records maintained for traceability. Adjustments are made based on field conditions and material variability. The process is documented in the WPS and reviewed during procedure qualification. Quality assurance oversees compliance and audits preparation procedures. Joint design is updated as new materials or processes are introduced.""",
        key_factors=["Material Thickness", "Joint Type", "Fit-Up", "Cleaning", "Code Compliance"],
        primary_authority=["ASME Section IX", "AWS D1.1"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper joint design/preparation may compromise weld quality.",
        counter_arguments=[
            "Field conditions may limit preparation options.",
            "Material variability can affect fit-up.",
            "Time constraints may lead to shortcuts."
        ],
        resolution_strategy="Enforce joint design and preparation standards per WPS and code.",
        entity_scope="All Welding Operations",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 5.3"
    ),
    DoctrineBlock(
        topic="Weld Defects - Porosity",
        keywords=["Weld Defects", "Porosity", "Gas Entrapment", "Inspection", "AWS D1.1"],
        conclusion_template="Porosity is identified and evaluated per AWS D1.1 acceptance criteria; corrective actions are implemented as required.",
        reasoning_framework="""Porosity results from gas entrapment during solidification, often due to contamination, improper shielding gas, or excessive travel speed. Inspection includes visual, radiographic, and ultrasonic methods. Acceptance criteria are specified in AWS D1.1, with limits based on weld size and application. Excessive porosity may require repair or rejection. Root cause analysis is performed to identify contributing factors, such as moisture, oil, or incorrect parameters. Corrective actions include improving cleaning procedures, adjusting shielding gas, and modifying welding technique. Documentation of defects and repairs is maintained for traceability. Quality assurance reviews defect trends and implements preventive measures.""",
        key_factors=["Contamination", "Shielding Gas", "Travel Speed", "Inspection", "Acceptance Criteria"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Control Inspector",
        adversary_position="Porosity may compromise weld strength and integrity.",
        counter_arguments=[
            "Minor porosity may be acceptable in non-critical applications.",
            "Repair may not be feasible for certain welds.",
            "Inspection methods may miss subsurface porosity."
        ],
        resolution_strategy="Evaluate porosity per code, implement corrective actions, and document findings.",
        entity_scope="All Welds",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="AWS D1.1 Table 6.1"
    ),
    DoctrineBlock(
        topic="Weld Defects - Lack of Fusion and Incomplete Penetration",
        keywords=["Weld Defects", "Lack of Fusion", "Incomplete Penetration", "Inspection", "AWS D1.1"],
        conclusion_template="Lack of fusion and incomplete penetration are identified and evaluated per AWS D1.1; repairs are performed as required.",
        reasoning_framework="""Lack of fusion and incomplete penetration occur when the weld fails to fully bond with the base material or previous weld passes. Causes include improper joint preparation, incorrect welding parameters, and inadequate technique. Inspection methods include visual, ultrasonic, and radiographic testing. AWS D1.1 specifies acceptance criteria and repair procedures. Root cause analysis identifies contributing factors, such as low heat input or poor fit-up. Corrective actions include adjusting parameters, improving joint preparation, and retraining welders. Documentation of defects and repairs is maintained for traceability. Quality assurance monitors defect rates and implements preventive measures.""",
        key_factors=["Joint Preparation", "Welding Parameters", "Technique", "Inspection", "Acceptance Criteria"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Control Inspector",
        adversary_position="Defects may compromise weld integrity and require costly repairs.",
        counter_arguments=[
            "Minor lack of fusion may be acceptable in non-critical applications.",
            "Repair may not be feasible for certain welds.",
            "Inspection methods may miss subsurface defects."
        ],
        resolution_strategy="Evaluate defects per code, perform repairs, and document findings.",
        entity_scope="All Welds",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Table 6.1"
    ),
    DoctrineBlock(
        topic="Weld Defects - Cracks (Hot Cracks and Cold Cracks)",
        keywords=["Weld Defects", "Cracks", "Hot Cracks", "Cold Cracks", "Inspection", "AWS D1.1"],
        conclusion_template="Cracks are identified and evaluated per AWS D1.1; repairs and preventive measures are implemented.",
        reasoning_framework="""Cracks are the most serious weld defects, potentially leading to catastrophic failure. Hot cracks occur during solidification due to alloy segregation or excessive heat input. Cold cracks develop after cooling, often due to hydrogen embrittlement or residual stresses. Inspection includes visual, magnetic particle, and ultrasonic testing. AWS D1.1 specifies zero tolerance for cracks in most applications. Root cause analysis identifies contributing factors, such as improper preheat, excessive restraint, or contamination. Corrective actions include adjusting welding parameters, improving joint design, and implementing preheat or PWHT. Repairs involve complete removal of cracks and re-welding. Documentation is maintained for traceability. Quality assurance monitors crack incidence and implements preventive measures.""",
        key_factors=["Heat Input", "Preheat", "Residual Stress", "Inspection", "Acceptance Criteria"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Control Inspector",
        adversary_position="Cracks may compromise structural integrity and require extensive repairs.",
        counter_arguments=[
            "Detection may be difficult for subsurface cracks.",
            "Repair may not restore original properties.",
            "Prevention requires comprehensive controls."
        ],
        resolution_strategy="Identify and repair cracks per code, implement preventive measures, and document findings.",
        entity_scope="All Welds",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="AWS D1.1 Clause 6.14"
    ),
    DoctrineBlock(
        topic="Ultrasonic Testing (UT) for Weld Inspection",
        keywords=["Ultrasonic Testing", "UT", "Weld Inspection", "Non-Destructive Testing", "ASME IX"],
        conclusion_template="UT is performed per ASME IX and AWS D1.1 to detect subsurface weld defects.",
        reasoning_framework="""UT uses high-frequency sound waves to detect internal defects such as cracks, lack of fusion, and inclusions. The process is performed by qualified technicians using calibrated equipment. ASME IX and AWS D1.1 specify procedures, acceptance criteria, and technician qualification requirements. UT is preferred for thick sections and critical welds where radiography is impractical. Results are documented and reviewed by quality assurance. Interpretation requires expertise, with potential for false positives or missed defects. UT is supplemented by other NDT methods as required. Records are maintained for traceability and audit. Periodic calibration and proficiency testing ensure reliability.""",
        key_factors=["Technician Qualification", "Equipment Calibration", "Acceptance Criteria", "Documentation", "Traceability"],
        primary_authority=["ASME Section IX", "AWS D1.1"],
        burden_holder="NDT Technician",
        adversary_position="UT may miss certain defect types or require extensive interpretation.",
        counter_arguments=[
            "Radiography may be more effective for certain defects.",
            "UT requires highly skilled technicians.",
            "Equipment calibration is critical for accuracy."
        ],
        resolution_strategy="Perform UT per code, supplement with other NDT methods, and maintain records.",
        entity_scope="Critical Welds",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.20"
    ),
    DoctrineBlock(
        topic="Radiographic Testing (RT) for Weld Inspection",
        keywords=["Radiographic Testing", "RT", "Weld Inspection", "Non-Destructive Testing", "ASME IX"],
        conclusion_template="RT is performed per ASME IX and AWS D1.1 to detect internal weld defects.",
        reasoning_framework="""RT uses X-rays or gamma rays to produce images of welds, revealing internal defects such as porosity, cracks, and inclusions. The process is performed by qualified technicians, with procedures and acceptance criteria specified in ASME IX and AWS D1.1. RT is preferred for thin sections and welds where UT is impractical. Interpretation requires expertise, with potential for missed defects or false positives. RT is supplemented by other NDT methods as required. Safety protocols are strictly enforced due to radiation hazards. Results are documented and reviewed by quality assurance. Records are maintained for traceability and audit. Periodic calibration and proficiency testing ensure reliability.""",
        key_factors=["Technician Qualification", "Safety Protocols", "Acceptance Criteria", "Documentation", "Traceability"],
        primary_authority=["ASME Section IX", "AWS D1.1"],
        burden_holder="NDT Technician",
        adversary_position="RT may miss certain defect types or pose safety risks.",
        counter_arguments=[
            "UT may be more effective for thick sections.",
            "Radiation hazards require strict controls.",
            "Interpretation is subject to human error."
        ],
        resolution_strategy="Perform RT per code, enforce safety protocols, and maintain records.",
        entity_scope="Critical Welds",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.20"
    ),
    DoctrineBlock(
        topic="Magnetic Particle Testing (MT) for Surface Crack Detection",
        keywords=["Magnetic Particle Testing", "MT", "Surface Crack Detection", "Non-Destructive Testing", "AWS D1.1"],
        conclusion_template="MT is performed per AWS D1.1 to detect surface and near-surface cracks in ferromagnetic materials.",
        reasoning_framework="""MT uses magnetic fields and ferrous particles to reveal surface and near-surface cracks in ferromagnetic materials. The process is performed by qualified technicians using calibrated equipment. AWS D1.1 specifies procedures, acceptance criteria, and technician qualification requirements. MT is preferred for detecting surface cracks in welds and heat-affected zones. Results are documented and reviewed by quality assurance. Interpretation requires expertise, with potential for missed defects or false positives. MT is supplemented by other NDT methods as required. Records are maintained for traceability and audit. Periodic calibration and proficiency testing ensure reliability.""",
        key_factors=["Technician Qualification", "Equipment Calibration", "Acceptance Criteria", "Documentation", "Traceability"],
        primary_authority=["AWS D1.1"],
        burden_holder="NDT Technician",
        adversary_position="MT is limited to ferromagnetic materials and may miss subsurface defects.",
        counter_arguments=[
            "PT is required for non-magnetic materials.",
            "MT may miss deep cracks.",
            "Interpretation is subject to human error."
        ],
        resolution_strategy="Perform MT per code, supplement with other NDT methods, and maintain records.",
        entity_scope="Ferromagnetic Welds",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.23"
    ),
    DoctrineBlock(
        topic="Liquid Penetrant Testing (PT) for Non-Magnetic Materials",
        keywords=["Liquid Penetrant Testing", "PT", "Non-Magnetic Materials", "Surface Crack Detection", "AWS D1.1"],
        conclusion_template="PT is performed per AWS D1.1 to detect surface cracks in non-magnetic materials.",
        reasoning_framework="""PT uses liquid penetrants and developers to reveal surface cracks in non-magnetic materials. The process is performed by qualified technicians using calibrated equipment. AWS D1.1 specifies procedures, acceptance criteria, and technician qualification requirements. PT is preferred for detecting surface cracks in stainless steels, aluminum, and nickel alloys. Results are documented and reviewed by quality assurance. Interpretation requires expertise, with potential for missed defects or false positives. PT is supplemented by other NDT methods as required. Records are maintained for traceability and audit. Periodic calibration and proficiency testing ensure reliability.""",
        key_factors=["Technician Qualification", "Equipment Calibration", "Acceptance Criteria", "Documentation", "Traceability"],
        primary_authority=["AWS D1.1"],
        burden_holder="NDT Technician",
        adversary_position="PT is limited to surface defects and may miss subsurface cracks.",
        counter_arguments=[
            "MT is required for ferromagnetic materials.",
            "PT may miss deep cracks.",
            "Interpretation is subject to human error."
        ],
        resolution_strategy="Perform PT per code, supplement with other NDT methods, and maintain records.",
        entity_scope="Non-Magnetic Welds",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.24"
    ),
    DoctrineBlock(
        topic="Visual Inspection (VT) and Acceptance Criteria",
        keywords=["Visual Inspection", "VT", "Acceptance Criteria", "Weld Quality", "AWS D1.1"],
        conclusion_template="VT is performed per AWS D1.1 to assess weld quality and compliance with acceptance criteria.",
        reasoning_framework="""VT is the most basic and widely used inspection method, assessing weld size, profile, and surface condition. AWS D1.1 specifies acceptance criteria for weld dimensions, undercut, overlap, and surface defects. VT is performed by qualified inspectors using calibrated tools. Results are documented and reviewed by quality assurance. VT is supplemented by other NDT methods as required. Records are maintained for traceability and audit. Periodic calibration and proficiency testing ensure reliability. VT is critical for identifying gross defects and ensuring compliance before more advanced NDT methods are applied.""",
        key_factors=["Inspector Qualification", "Calibrated Tools", "Acceptance Criteria", "Documentation", "Traceability"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Control Inspector",
        adversary_position="VT may miss subsurface defects and relies on inspector skill.",
        counter_arguments=[
            "NDT methods are required for internal defects.",
            "VT is subject to human error.",
            "Acceptance criteria may vary by application."
        ],
        resolution_strategy="Perform VT per code, supplement with NDT as required, and maintain records.",
        entity_scope="All Welds",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="API 1104 Pipeline Welding Standard",
        keywords=["API 1104", "Pipeline Welding", "Standard", "Qualification", "Inspection"],
        conclusion_template="Pipeline welding is performed and qualified per API 1104 requirements.",
        reasoning_framework="""API 1104 specifies requirements for welding, qualification, inspection, and repair of pipeline welds. Procedures include WPS development, welder qualification, and NDT methods such as UT and RT. Acceptance criteria are based on service conditions and material type. Documentation is maintained for traceability and audit. Repairs are performed per API 1104 guidelines, with root cause analysis for recurring defects. Quality assurance oversees compliance and audits procedures. API 1104 is referenced for pipeline construction, maintenance, and repair, with periodic review as standards evolve.""",
        key_factors=["WPS", "Welder Qualification", "NDT Methods", "Acceptance Criteria", "Documentation"],
        primary_authority=["API 1104"],
        burden_holder="Pipeline Welding Supervisor",
        adversary_position="Failure to comply with API 1104 may result in rejected welds and regulatory penalties.",
        counter_arguments=[
            "Other codes may apply for offshore or specialty pipelines.",
            "API 1104 is periodically updated, requiring ongoing review.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Perform pipeline welding per API 1104, maintain documentation, and review standards periodically.",
        entity_scope="Pipeline Welding Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 1104 Section 3"
    ),
    DoctrineBlock(
        topic="AWS D1.1 Structural Welding Code - Steel",
        keywords=["AWS D1.1", "Structural Welding", "Steel", "Code", "Qualification"],
        conclusion_template="Structural welding is performed and qualified per AWS D1.1 requirements.",
        reasoning_framework="""AWS D1.1 specifies requirements for welding, qualification, inspection, and repair of structural steel welds. Procedures include WPS development, welder qualification, and NDT methods such as VT, UT, RT, MT, and PT. Acceptance criteria are based on service conditions and material type. Documentation is maintained for traceability and audit. Repairs are performed per AWS D1.1 guidelines, with root cause analysis for recurring defects. Quality assurance oversees compliance and audits procedures. AWS D1.1 is referenced for structural steel construction, maintenance, and repair, with periodic review as standards evolve.""",
        key_factors=["WPS", "Welder Qualification", "NDT Methods", "Acceptance Criteria", "Documentation"],
        primary_authority=["AWS D1.1"],
        burden_holder="Structural Welding Supervisor",
        adversary_position="Failure to comply with AWS D1.1 may result in rejected welds and regulatory penalties.",
        counter_arguments=[
            "Other codes may apply for specialty applications.",
            "AWS D1.1 is periodically updated, requiring ongoing review.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Perform structural welding per AWS D1.1, maintain documentation, and review standards periodically.",
        entity_scope="Structural Steel Welding Operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="AWS D1.1 Section 4"
    ),
    DoctrineBlock(
        topic="NACE MR0175/ISO 15156 Sour Service Welding Requirements",
        keywords=["NACE MR0175", "ISO 15156", "Sour Service", "Welding", "Qualification"],
        conclusion_template="Sour service welding is performed and qualified per NACE MR0175/ISO 15156 requirements.",
        reasoning_framework="""NACE MR0175/ISO 15156 specifies requirements for welding materials and procedures in sour service environments, where hydrogen sulfide may cause cracking or corrosion. Procedures include WPS development, welder qualification, and selection of compatible materials and filler metals. Acceptance criteria are based on service conditions and material type. Documentation is maintained for traceability and audit. Repairs are performed per NACE MR0175/ISO 15156 guidelines, with root cause analysis for recurring defects. Quality assurance oversees compliance and audits procedures. NACE MR0175/ISO 15156 is referenced for pipeline and pressure vessel construction, maintenance, and repair, with periodic review as standards evolve.""",
        key_factors=["Material Compatibility", "WPS", "Welder Qualification", "Acceptance Criteria", "Documentation"],
        primary_authority=["NACE MR0175", "ISO 15156"],
        burden_holder="Sour Service Welding Supervisor",
        adversary_position="Failure to comply may result in cracking, corrosion, and regulatory penalties.",
        counter_arguments=[
            "Other codes may apply for specialty applications.",
            "NACE MR0175/ISO 15156 is periodically updated, requiring ongoing review.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Perform sour service welding per NACE MR0175/ISO 15156, maintain documentation, and review standards periodically.",
        entity_scope="Sour Service Welding Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 7"
    ),
    DoctrineBlock(
        topic="Repair Welding Procedures and Limitations",
        keywords=["Repair Welding", "Procedures", "Limitations", "Qualification", "ASME IX"],
        conclusion_template="Repair welding is performed per qualified procedures, with limitations documented and approved by responsible engineer.",
        reasoning_framework="""Repair welding is performed to restore weld integrity, following procedures qualified per ASME IX and AWS D1.1. Repairs are limited by material type, defect location, and service conditions. Approval is required from the responsible engineer, with documentation maintained for traceability. Repairs are inspected using NDT methods and evaluated per acceptance criteria. Root cause analysis is performed for recurring defects. Quality assurance oversees compliance and audits procedures. Limitations include maximum number of repairs, material compatibility, and impact on mechanical properties. Repairs are documented, with records maintained for audit. Periodic review ensures procedures remain current and effective.""",
        key_factors=["Qualified Procedures", "Approval", "Documentation", "Inspection", "Limitations"],
        primary_authority=["ASME Section IX", "AWS D1.1"],
        burden_holder="Responsible Welding Engineer",
        adversary_position="Improper repairs may compromise weld integrity and violate code.",
        counter_arguments=[
            "Repairs may not restore original properties.",
            "Documentation may be difficult to maintain.",
            "Approval process may delay repairs."
        ],
        resolution_strategy="Perform repairs per qualified procedures, document limitations, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASME Section IX QW-401"
    ),
    DoctrineBlock(
        topic="Weld Documentation and Traceability",
        keywords=["Weld Documentation", "Traceability", "Records", "Audit", "ASME IX"],
        conclusion_template="Weld documentation and traceability are maintained per code and quality management system requirements.",
        reasoning_framework="""Documentation includes WPS, PQR, WPQ, inspection records, repair logs, and material certificates. Traceability is maintained via unique identifiers, batch numbers, and weld maps. Records are reviewed by quality assurance and maintained for audit. Documentation is critical for regulatory compliance, root cause analysis, and warranty claims. Electronic systems may be used for recordkeeping, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to maintain documentation may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Records", "Identifiers", "Audit", "Quality Management", "Compliance"],
        primary_authority=["ASME Section IX", "AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of documentation undermines traceability and compliance.",
        counter_arguments=[
            "Paper records may be lost or damaged.",
            "Electronic systems require security and backup.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Maintain comprehensive documentation per code and quality management system.",
        entity_scope="All Welding Operations",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="ASME Section IX QW-401"
    ),
    DoctrineBlock(
        topic="Weld Joint Fit-Up and Tolerance Control",
        keywords=["Joint Fit-Up", "Tolerance Control", "Welding", "Quality", "AWS D1.1"],
        conclusion_template="Joint fit-up and tolerances are controlled per AWS D1.1 to ensure weld quality and minimize defects.",
        reasoning_framework="""Proper joint fit-up is essential for achieving full penetration and minimizing defects such as lack of fusion and incomplete penetration. AWS D1.1 specifies tolerance limits for joint gaps, alignment, and bevel angles. Fit-up is inspected prior to welding, with adjustments made as necessary. Poor fit-up can lead to excessive weld metal consumption, distortion, and reduced mechanical properties. Tolerance control is documented in the WPS and verified during procedure qualification. Quality assurance oversees compliance and audits fit-up procedures. Records are maintained for traceability and audit. Periodic review ensures procedures remain current and effective.""",
        key_factors=["Fit-Up", "Tolerance Limits", "Inspection", "Documentation", "Quality Assurance"],
        primary_authority=["AWS D1.1"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper fit-up may compromise weld quality and increase defect rates.",
        counter_arguments=[
            "Field conditions may limit fit-up options.",
            "Material variability can affect tolerance control.",
            "Time constraints may lead to shortcuts."
        ],
        resolution_strategy="Control fit-up and tolerances per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 5.3"
    ),
    DoctrineBlock(
        topic="Weld Consumable Storage and Handling",
        keywords=["Consumable Storage", "Handling", "Electrode", "Filler Metal", "AWS D1.1"],
        conclusion_template="Weld consumables are stored and handled per AWS D1.1 to prevent contamination and ensure quality.",
        reasoning_framework="""Proper storage and handling of electrodes and filler metals is critical to prevent contamination and moisture absorption, which can lead to weld defects such as porosity and cracking. AWS D1.1 specifies requirements for storage conditions, including temperature, humidity, and segregation by batch. Consumables are inspected prior to use, with damaged or expired materials discarded. Handling procedures include minimizing exposure to moisture and contaminants. Records are maintained for traceability and audit. Quality assurance oversees compliance and audits storage procedures. Periodic review ensures procedures remain current and effective.""",
        key_factors=["Storage Conditions", "Handling Procedures", "Inspection", "Traceability", "Quality Assurance"],
        primary_authority=["AWS D1.1"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper storage may compromise weld quality and increase defect rates.",
        counter_arguments=[
            "Field conditions may limit storage options.",
            "Consumable traceability may be difficult to maintain.",
            "Time constraints may lead to shortcuts."
        ],
        resolution_strategy="Store and handle consumables per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 5.4"
    ),
    DoctrineBlock(
        topic="Weld Sequence Planning and Distortion Control",
        keywords=["Weld Sequence", "Distortion Control", "Planning", "Welding", "AWS D1.1"],
        conclusion_template="Weld sequence is planned and executed per AWS D1.1 to minimize distortion and residual stresses.",
        reasoning_framework="""Proper weld sequence planning is essential to control distortion and residual stresses, especially in large or complex assemblies. AWS D1.1 provides guidelines for sequencing, including alternating sides, staggered welds, and controlled heat input. Sequence is documented in the WPS and reviewed during procedure qualification. Distortion is monitored during welding, with corrective actions implemented as necessary. Quality assurance oversees compliance and audits sequence planning. Records are maintained for traceability and audit. Periodic review ensures procedures remain current and effective.""",
        key_factors=["Sequence Planning", "Heat Input", "Distortion Monitoring", "Documentation", "Quality Assurance"],
        primary_authority=["AWS D1.1"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper sequence may increase distortion and compromise weld quality.",
        counter_arguments=[
            "Complex assemblies may require custom sequencing.",
            "Distortion may not be fully controlled by sequence alone.",
            "Time constraints may limit planning options."
        ],
        resolution_strategy="Plan and execute sequence per code, monitor distortion, and document procedures.",
        entity_scope="All Welding Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 5.17"
    ),
    DoctrineBlock(
        topic="Weld Cleaning and Surface Preparation",
        keywords=["Weld Cleaning", "Surface Preparation", "Contamination", "Quality", "AWS D1.1"],
        conclusion_template="Weld cleaning and surface preparation are performed per AWS D1.1 to prevent contamination and defects.",
        reasoning_framework="""Proper cleaning and surface preparation are essential to prevent contamination and defects such as porosity, lack of fusion, and cracking. AWS D1.1 specifies requirements for removal of oil, grease, rust, and other contaminants prior to welding. Cleaning methods include mechanical, chemical, and abrasive techniques. Surface preparation is inspected prior to welding, with records maintained for traceability and audit. Quality assurance oversees compliance and audits cleaning procedures. Periodic review ensures procedures remain current and effective.""",
        key_factors=["Cleaning Methods", "Inspection", "Documentation", "Quality Assurance", "Contamination Control"],
        primary_authority=["AWS D1.1"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper cleaning may compromise weld quality and increase defect rates.",
        counter_arguments=[
            "Field conditions may limit cleaning options.",
            "Contaminants may be difficult to detect.",
            "Time constraints may lead to shortcuts."
        ],
        resolution_strategy="Clean and prepare surfaces per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 5.15"
    ),
    DoctrineBlock(
        topic="Weld Size and Profile Control",
        keywords=["Weld Size", "Profile Control", "Quality", "Inspection", "AWS D1.1"],
        conclusion_template="Weld size and profile are controlled per AWS D1.1 to ensure compliance and structural integrity.",
        reasoning_framework="""Proper control of weld size and profile is essential for achieving structural integrity and compliance with code requirements. AWS D1.1 specifies acceptance criteria for weld dimensions, profile, and reinforcement. Size and profile are inspected during and after welding, with records maintained for traceability and audit. Quality assurance oversees compliance and audits size control procedures. Periodic review ensures procedures remain current and effective. Improper size or profile may compromise strength, increase stress concentrations, and lead to rejection.""",
        key_factors=["Size Control", "Profile Inspection", "Documentation", "Quality Assurance", "Acceptance Criteria"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Control Inspector",
        adversary_position="Improper size or profile may compromise structural integrity and compliance.",
        counter_arguments=[
            "Field conditions may limit size control.",
            "Profile may vary due to operator skill.",
            "Time constraints may lead to shortcuts."
        ],
        resolution_strategy="Control size and profile per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Heat Input Calculation and Control",
        keywords=["Heat Input", "Calculation", "Control", "Welding", "ASME IX"],
        conclusion_template="Heat input is calculated and controlled per ASME IX to ensure weld quality and mechanical properties.",
        reasoning_framework="""Proper calculation and control of heat input is essential for achieving desired mechanical properties and preventing defects such as cracking and distortion. ASME IX specifies methods for calculating heat input based on voltage, current, and travel speed. Heat input is documented in the WPS and monitored during welding. Quality assurance oversees compliance and audits heat input procedures. Records are maintained for traceability and audit. Periodic review ensures procedures remain current and effective. Excessive or insufficient heat input may compromise weld quality and lead to rejection.""",
        key_factors=["Heat Input Calculation", "Monitoring", "Documentation", "Quality Assurance", "Acceptance Criteria"],
        primary_authority=["ASME Section IX"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper heat input may compromise weld quality and mechanical properties.",
        counter_arguments=[
            "Field conditions may affect heat input control.",
            "Calculation may be inaccurate due to equipment variability.",
            "Time constraints may limit monitoring."
        ],
        resolution_strategy="Calculate and control heat input per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASME Section IX QW-409"
    ),
    DoctrineBlock(
        topic="Weld Pass Sequence and Layer Control",
        keywords=["Pass Sequence", "Layer Control", "Welding", "Quality", "AWS D1.1"],
        conclusion_template="Weld pass sequence and layer control are executed per AWS D1.1 to ensure weld quality and minimize defects.",
        reasoning_framework="""Proper control of weld pass sequence and layer thickness is essential for achieving desired mechanical properties and preventing defects such as lack of fusion and incomplete penetration. AWS D1.1 specifies requirements for pass sequence, layer thickness, and interpass cleaning. Sequence and layer control are documented in the WPS and monitored during welding. Quality assurance oversees compliance and audits pass sequence procedures. Records are maintained for traceability and audit. Periodic review ensures procedures remain current and effective. Improper sequence or layer control may compromise weld quality and lead to rejection.""",
        key_factors=["Pass Sequence", "Layer Thickness", "Interpass Cleaning", "Documentation", "Quality Assurance"],
        primary_authority=["AWS D1.1"],
        burden_holder="Welding Supervisor",
        adversary_position="Improper sequence or layer control may compromise weld quality and increase defect rates.",
        counter_arguments=[
            "Field conditions may limit sequence options.",
            "Layer thickness may vary due to operator skill.",
            "Time constraints may lead to shortcuts."
        ],
        resolution_strategy="Control pass sequence and layer per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 5.17"
    ),
    DoctrineBlock(
        topic="Weld Defect Repair and Evaluation",
        keywords=["Defect Repair", "Evaluation", "Welding", "Inspection", "AWS D1.1"],
        conclusion_template="Weld defects are repaired and evaluated per AWS D1.1, with documentation maintained for traceability.",
        reasoning_framework="""Proper repair and evaluation of weld defects is essential for restoring integrity and compliance with code requirements. AWS D1.1 specifies procedures for defect repair, including removal, re-welding, and inspection. Repairs are documented, with records maintained for traceability and audit. Quality assurance oversees compliance and audits repair procedures. Root cause analysis is performed for recurring defects. Periodic review ensures procedures remain current and effective. Improper repair may compromise weld quality and lead to rejection.""",
        key_factors=["Repair Procedures", "Inspection", "Documentation", "Quality Assurance", "Root Cause Analysis"],
        primary_authority=["AWS D1.1"],
        burden_holder="Responsible Welding Engineer",
        adversary_position="Improper repair may compromise weld integrity and compliance.",
        counter_arguments=[
            "Repair may not restore original properties.",
            "Documentation may be difficult to maintain.",
            "Approval process may delay repairs."
        ],
        resolution_strategy="Repair defects per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.14"
    ),
    DoctrineBlock(
        topic="Weld Inspection Personnel Qualification",
        keywords=["Inspection Personnel", "Qualification", "Certification", "AWS D1.1", "ASME IX"],
        conclusion_template="Inspection personnel are qualified and certified per AWS D1.1 and ASME IX requirements.",
        reasoning_framework="""Proper qualification and certification of inspection personnel is essential for ensuring reliable weld inspection and compliance with code requirements. AWS D1.1 and ASME IX specify requirements for inspector qualification, including training, experience, and certification. Personnel are periodically requalified and records maintained for traceability and audit. Quality assurance oversees compliance and audits qualification procedures. Improper qualification may compromise inspection reliability and lead to rejection.""",
        key_factors=["Qualification", "Certification", "Training", "Documentation", "Quality Assurance"],
        primary_authority=["AWS D1.1", "ASME Section IX"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Unqualified personnel may compromise inspection reliability and compliance.",
        counter_arguments=[
            "Certification may lapse due to administrative oversight.",
            "Training may not reflect actual inspection conditions.",
            "Third-party verification may add cost and complexity."
        ],
        resolution_strategy="Qualify and certify personnel per code, document procedures, and review periodically.",
        entity_scope="All Inspection Personnel",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Recordkeeping and Audit",
        keywords=["Inspection Recordkeeping", "Audit", "Documentation", "Traceability", "AWS D1.1"],
        conclusion_template="Inspection records are maintained and audited per AWS D1.1 and quality management system requirements.",
        reasoning_framework="""Proper recordkeeping and audit of inspection results is essential for traceability, regulatory compliance, and root cause analysis. AWS D1.1 specifies requirements for documentation, including inspection reports, repair logs, and material certificates. Records are reviewed by quality assurance and maintained for audit. Electronic systems may be used for recordkeeping, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to maintain records may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Recordkeeping", "Audit", "Documentation", "Quality Management", "Compliance"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of records undermines traceability and compliance.",
        counter_arguments=[
            "Paper records may be lost or damaged.",
            "Electronic systems require security and backup.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Maintain comprehensive records per code and quality management system, audit periodically.",
        entity_scope="All Welding Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Material Identification and Control",
        keywords=["Material Identification", "Control", "Welding", "Traceability", "ASME IX"],
        conclusion_template="Weld material identification and control are maintained per ASME IX and quality management system requirements.",
        reasoning_framework="""Proper identification and control of welding materials is essential for traceability, regulatory compliance, and prevention of mix-ups. ASME IX specifies requirements for material certificates, batch numbers, and unique identifiers. Materials are inspected prior to use, with records maintained for traceability and audit. Quality assurance oversees compliance and audits material control procedures. Electronic systems may be used for recordkeeping, with periodic backups and access controls. Documentation is updated as materials or suppliers change. Audits are performed to verify completeness and accuracy. Failure to maintain material control may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Material Certificates", "Batch Numbers", "Identifiers", "Documentation", "Quality Assurance"],
        primary_authority=["ASME Section IX"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of material control undermines traceability and compliance.",
        counter_arguments=[
            "Supplier variations can affect quality.",
            "Batch traceability may be difficult to maintain.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Maintain material identification and control per code and quality management system.",
        entity_scope="All Welding Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section IX QW-401"
    ),
    DoctrineBlock(
        topic="Weld Inspection Equipment Calibration",
        keywords=["Inspection Equipment", "Calibration", "Traceability", "Quality Assurance", "AWS D1.1"],
        conclusion_template="Inspection equipment is calibrated per AWS D1.1 and quality management system requirements.",
        reasoning_framework="""Proper calibration of inspection equipment is essential for reliable results, traceability, and regulatory compliance. AWS D1.1 specifies requirements for calibration intervals, procedures, and documentation. Equipment is inspected and calibrated prior to use, with records maintained for traceability and audit. Quality assurance oversees compliance and audits calibration procedures. Electronic systems may be used for recordkeeping, with periodic backups and access controls. Documentation is updated as equipment or calibration standards change. Audits are performed to verify completeness and accuracy. Failure to maintain calibration may result in unreliable results, rejected welds, and regulatory penalties.""",
        key_factors=["Calibration Intervals", "Procedures", "Documentation", "Quality Assurance", "Traceability"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of calibration undermines reliability and compliance.",
        counter_arguments=[
            "Equipment may drift between calibrations.",
            "Calibration standards may change.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Calibrate equipment per code and quality management system, document procedures, and audit periodically.",
        entity_scope="All Inspection Equipment",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Acceptance and Rejection Criteria",
        keywords=["Inspection Acceptance", "Rejection Criteria", "Welding", "AWS D1.1", "ASME IX"],
        conclusion_template="Weld inspection acceptance and rejection criteria are applied per AWS D1.1 and ASME IX requirements.",
        reasoning_framework="""Proper application of acceptance and rejection criteria is essential for compliance, structural integrity, and prevention of defects. AWS D1.1 and ASME IX specify requirements for acceptance of weld size, profile, and defect types. Criteria are documented in the WPS and inspection reports. Quality assurance oversees compliance and audits application of criteria. Records are maintained for traceability and audit. Periodic review ensures procedures remain current and effective. Improper application may compromise quality and lead to rejection.""",
        key_factors=["Acceptance Criteria", "Rejection Criteria", "Documentation", "Quality Assurance", "Traceability"],
        primary_authority=["AWS D1.1", "ASME Section IX"],
        burden_holder="Quality Control Inspector",
        adversary_position="Improper application may compromise quality and compliance.",
        counter_arguments=[
            "Criteria may vary by application.",
            "Inspector interpretation may differ.",
            "Documentation may be difficult to maintain."
        ],
        resolution_strategy="Apply criteria per code, document procedures, and review periodically.",
        entity_scope="All Welding Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Reporting and Communication",
        keywords=["Inspection Reporting", "Communication", "Welding", "Quality Assurance", "AWS D1.1"],
        conclusion_template="Inspection reporting and communication are performed per AWS D1.1 and quality management system requirements.",
        reasoning_framework="""Proper reporting and communication of inspection results is essential for traceability, regulatory compliance, and root cause analysis. AWS D1.1 specifies requirements for inspection reports, repair logs, and communication protocols. Reports are reviewed by quality assurance and communicated to responsible personnel. Electronic systems may be used for reporting, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to communicate results may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Reporting", "Communication", "Documentation", "Quality Assurance", "Traceability"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of communication undermines traceability and compliance.",
        counter_arguments=[
            "Reports may be delayed or lost.",
            "Electronic systems require security and backup.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Report and communicate results per code and quality management system, audit periodically.",
        entity_scope="All Welding Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Discrepancy Resolution",
        keywords=["Inspection Discrepancy", "Resolution", "Welding", "Quality Assurance", "AWS D1.1"],
        conclusion_template="Inspection discrepancies are resolved per AWS D1.1 and quality management system requirements.",
        reasoning_framework="""Proper resolution of inspection discrepancies is essential for compliance, traceability, and prevention of defects. AWS D1.1 specifies requirements for discrepancy resolution, including investigation, corrective actions, and documentation. Discrepancies are reviewed by quality assurance and resolved in consultation with responsible personnel. Electronic systems may be used for tracking, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to resolve discrepancies may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Discrepancy Resolution", "Investigation", "Corrective Actions", "Documentation", "Quality Assurance"],
        primary_authority=["AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Unresolved discrepancies undermine traceability and compliance.",
        counter_arguments=[
            "Investigation may be delayed or incomplete.",
            "Corrective actions may not address root cause.",
            "Documentation may be difficult to maintain."
        ],
        resolution_strategy="Resolve discrepancies per code and quality management system, document actions, and audit periodically.",
        entity_scope="All Welding Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Data Management and Security",
        keywords=["Inspection Data", "Management", "Security", "Welding", "Quality Assurance"],
        conclusion_template="Inspection data is managed and secured per quality management system and regulatory requirements.",
        reasoning_framework="""Proper management and security of inspection data is essential for traceability, regulatory compliance, and prevention of data loss or tampering. Quality management systems specify requirements for data storage, access controls, backups, and security protocols. Electronic systems may be used for data management, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to manage and secure data may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Data Management", "Security", "Backups", "Access Controls", "Quality Assurance"],
        primary_authority=["Quality Management System", "AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of data management undermines traceability and compliance.",
        counter_arguments=[
            "Electronic systems require security and backup.",
            "Data may be lost or tampered with.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Manage and secure data per quality management system, document procedures, and audit periodically.",
        entity_scope="All Welding Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Quality Management System Integration",
        keywords=["Inspection", "Quality Management System", "Integration", "Welding", "AWS D1.1"],
        conclusion_template="Inspection procedures are integrated with the quality management system per AWS D1.1 and regulatory requirements.",
        reasoning_framework="""Proper integration of inspection procedures with the quality management system is essential for traceability, regulatory compliance, and prevention of defects. AWS D1.1 specifies requirements for integration, including documentation, audit, and corrective actions. Procedures are reviewed by quality assurance and updated as necessary. Electronic systems may be used for integration, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to integrate procedures may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Integration", "Documentation", "Audit", "Corrective Actions", "Quality Assurance"],
        primary_authority=["AWS D1.1", "Quality Management System"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of integration undermines traceability and compliance.",
        counter_arguments=[
            "Electronic systems require security and backup.",
            "Integration may be difficult for legacy procedures.",
            "Documentation may be difficult to maintain for field repairs."
        ],
        resolution_strategy="Integrate procedures per code and quality management system, document actions, and audit periodically.",
        entity_scope="All Welding Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Continuous Improvement and Feedback",
        keywords=["Inspection", "Continuous Improvement", "Feedback", "Welding", "Quality Assurance"],
        conclusion_template="Inspection procedures are continuously improved based on feedback and audit results per quality management system requirements.",
        reasoning_framework="""Continuous improvement of inspection procedures is essential for maintaining compliance, traceability, and prevention of defects. Quality management systems specify requirements for feedback, corrective actions, and periodic review. Procedures are reviewed by quality assurance and updated as necessary. Electronic systems may be used for tracking feedback and improvement actions, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to improve procedures may result in recurring defects, rejected welds, and regulatory penalties.""",
        key_factors=["Continuous Improvement", "Feedback", "Corrective Actions", "Documentation", "Quality Assurance"],
        primary_authority=["Quality Management System", "AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of improvement undermines compliance and increases defect rates.",
        counter_arguments=[
            "Feedback may be delayed or incomplete.",
            "Improvement actions may not address root cause.",
            "Documentation may be difficult to maintain."
        ],
        resolution_strategy="Continuously improve procedures per quality management system, document actions, and audit periodically.",
        entity_scope="All Welding Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Regulatory Compliance and Certification",
        keywords=["Inspection", "Regulatory Compliance", "Certification", "Welding", "AWS D1.1"],
        conclusion_template="Inspection procedures are performed per regulatory requirements and certification standards, with documentation maintained for traceability.",
        reasoning_framework="""Proper compliance with regulatory requirements and certification standards is essential for maintaining traceability, structural integrity, and prevention of defects. AWS D1.1 and ASME IX specify requirements for inspection, documentation, and certification. Procedures are reviewed by quality assurance and updated as necessary. Electronic systems may be used for recordkeeping, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to comply may result in rejected welds, regulatory penalties, and loss of certification.""",
        key_factors=["Regulatory Compliance", "Certification", "Documentation", "Audit", "Quality Assurance"],
        primary_authority=["AWS D1.1", "ASME Section IX"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of compliance undermines traceability and certification.",
        counter_arguments=[
            "Regulations may change, requiring ongoing review.",
            "Certification may lapse due to administrative oversight.",
            "Documentation may be difficult to maintain."
        ],
        resolution_strategy="Comply with regulations and certification standards, document procedures, and audit periodically.",
        entity_scope="All Welding Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
    ),
    DoctrineBlock(
        topic="Weld Inspection Training and Competency Development",
        keywords=["Inspection", "Training", "Competency", "Development", "Quality Assurance"],
        conclusion_template="Inspection personnel are trained and competency is developed per quality management system and regulatory requirements.",
        reasoning_framework="""Proper training and competency development of inspection personnel is essential for reliable results, traceability, and regulatory compliance. Quality management systems specify requirements for training, competency assessment, and periodic review. Training records are maintained for traceability and audit. Quality assurance oversees compliance and audits training procedures. Electronic systems may be used for recordkeeping, with periodic backups and access controls. Documentation is updated as procedures, materials, or personnel change. Audits are performed to verify completeness and accuracy. Failure to train and develop competency may result in unreliable results, rejected welds, and regulatory penalties.""",
        key_factors=["Training", "Competency", "Assessment", "Documentation", "Quality Assurance"],
        primary_authority=["Quality Management System", "AWS D1.1"],
        burden_holder="Quality Assurance Manager",
        adversary_position="Lack of training undermines reliability and compliance.",
        counter_arguments=[
            "Training may not reflect actual inspection conditions.",
            "Competency assessment may be subjective.",
            "Documentation may be difficult to maintain."
        ],
        resolution_strategy="Train and assess personnel per quality management system, document procedures, and audit periodically.",
        entity_scope="All Inspection Personnel",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AWS D1.1 Clause 6.1"
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