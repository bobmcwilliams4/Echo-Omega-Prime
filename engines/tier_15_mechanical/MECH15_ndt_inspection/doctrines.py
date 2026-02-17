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
        topic="UT Pulse-Echo Thickness Measurement Accuracy",
        keywords=["ultrasonic testing", "pulse-echo", "thickness measurement", "accuracy", "NDT"],
        conclusion_template="The accuracy of pulse-echo ultrasonic thickness measurements must be within ±0.1 mm or ±1% of nominal thickness, whichever is greater, provided calibration standards are traceable and environmental factors are controlled.",
        reasoning_framework=(
            "1. Review ASME Section V, Article 5, and ASTM E797 for accuracy requirements.\n"
            "2. Assess calibration procedures, including use of reference standards traceable to national standards.\n"
            "3. Evaluate instrument linearity and couplant consistency.\n"
            "4. Consider temperature, surface condition, and geometry effects on sound velocity and measurement.\n"
            "5. Confirm operator qualification per SNT-TC-1A or equivalent.\n"
            "6. Validate repeatability and reproducibility through multiple measurements.\n"
            "7. Compare measured values to acceptance criteria in API 510 or client specification.\n"
            "8. Document all calibration and measurement records for traceability.\n"
            "9. Address potential sources of error such as surface roughness, curvature, and coatings.\n"
            "10. Resolve disputes by reference to ASME Section V and calibration records."
        ),
        key_factors=[
            "Calibration traceability",
            "Instrument linearity",
            "Surface condition",
            "Operator qualification",
            "Environmental controls",
            "Reference standards",
            "Measurement repeatability"
        ],
        primary_authority=["ASME Section V", "ASTM E797", "API 510"],
        burden_holder="NDT service provider",
        adversary_position="Measured thickness accuracy is insufficient for acceptance",
        counter_arguments=[
            "Calibration was performed with traceable standards",
            "Environmental factors were controlled",
            "Operator is certified and experienced",
            "Repeat measurements confirm accuracy"
        ],
        resolution_strategy="Review calibration records, repeat measurements, and reference ASME Section V criteria.",
        entity_scope="NDT inspection personnel, quality assurance, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 5"
    ),
    DoctrineBlock(
        topic="Phased Array UT Sector Scan Coverage for Weld Inspection",
        keywords=["phased array", "ultrasonic testing", "sector scan", "weld inspection", "coverage"],
        conclusion_template="Phased Array UT sector scans must provide full volumetric coverage of welds, with scan plans documented and validated against ASME Section V and project specifications.",
        reasoning_framework=(
            "1. Identify weld geometry and applicable code requirements (ASME Section V, Article 4).\n"
            "2. Develop scan plan ensuring all critical weld zones (root, fusion faces, HAZ) are covered.\n"
            "3. Select probe frequency, aperture, and sector scan angles to maximize coverage and sensitivity.\n"
            "4. Simulate coverage using modeling software or coverage maps.\n"
            "5. Validate scan plan through demonstration on calibration blocks with representative flaws.\n"
            "6. Document scan parameters, encoder positions, and coverage maps.\n"
            "7. Ensure operator qualification per SNT-TC-1A or ISO 9712.\n"
            "8. Address limitations due to access, geometry, or material properties.\n"
            "9. Resolve disputes by reviewing scan plan, coverage maps, and code requirements."
        ),
        key_factors=[
            "Weld geometry",
            "Scan plan documentation",
            "Sector angle selection",
            "Probe characteristics",
            "Operator qualification",
            "Coverage validation"
        ],
        primary_authority=["ASME Section V", "API 1104", "ISO 13588"],
        burden_holder="NDT service provider",
        adversary_position="Sector scan coverage is insufficient to detect critical flaws",
        counter_arguments=[
            "Scan plan validated against code and client requirements",
            "Coverage maps demonstrate full volumetric inspection",
            "Operator is certified and experienced"
        ],
        resolution_strategy="Review scan plan, coverage maps, and demonstration records; repeat scans if necessary.",
        entity_scope="NDT inspectors, welding engineers, client QA/QC",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 4"
    ),
    DoctrineBlock(
        topic="TOFD Crack Height Sizing Accuracy",
        keywords=["TOFD", "crack sizing", "ultrasonic testing", "accuracy", "NDT"],
        conclusion_template="TOFD crack height sizing is accurate within ±1 mm for cracks ≥5 mm, provided calibration is performed on representative reference blocks and operator is qualified.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 4 and ISO 10863 for TOFD sizing accuracy.\n"
            "2. Ensure calibration blocks contain representative flaw sizes and geometries.\n"
            "3. Evaluate system resolution and dead zone effects on near-surface flaw detection.\n"
            "4. Confirm operator qualification and experience with TOFD technique.\n"
            "5. Assess signal interpretation protocols and software accuracy.\n"
            "6. Validate results through comparison with destructive testing or alternative NDT methods.\n"
            "7. Document all calibration and measurement procedures.\n"
            "8. Address limitations such as coarse grain structure or access restrictions.\n"
            "9. Resolve disputes by reviewing calibration, operator certification, and cross-validation data."
        ),
        key_factors=[
            "Calibration block representativeness",
            "System resolution",
            "Operator qualification",
            "Signal interpretation",
            "Cross-validation with other NDT methods"
        ],
        primary_authority=["ASME Section V", "ISO 10863"],
        burden_holder="NDT service provider",
        adversary_position="TOFD sizing is not reliable for critical crack assessment",
        counter_arguments=[
            "Calibration performed on representative blocks",
            "Operator is certified and experienced",
            "Results validated with alternative NDT or destructive testing"
        ],
        resolution_strategy="Review calibration and cross-validation records; repeat measurements if necessary.",
        entity_scope="NDT inspectors, fracture mechanics engineers, client QA/QC",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 4"
    ),
    DoctrineBlock(
        topic="Radiographic Film IQI Sensitivity Requirements",
        keywords=["radiography", "film", "IQI", "sensitivity", "image quality indicator"],
        conclusion_template="Radiographic film must achieve an IQI sensitivity of 2-2T or better, with proper placement and exposure per ASME Section V and ASTM E1030.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 2 and ASTM E1030 for IQI sensitivity criteria.\n"
            "2. Select appropriate IQI type (wire or hole) and size based on part thickness.\n"
            "3. Ensure IQI is placed on source side or as close as practical to the weld.\n"
            "4. Verify exposure parameters (kV, mA, time, source-to-film distance) are adequate for sensitivity.\n"
            "5. Assess film processing quality and viewing conditions.\n"
            "6. Document IQI placement, exposure parameters, and film identification.\n"
            "7. Address limitations such as geometry, access, or high-density materials.\n"
            "8. Resolve disputes by reviewing radiographs, exposure charts, and code requirements."
        ),
        key_factors=[
            "IQI selection and placement",
            "Exposure parameters",
            "Film processing quality",
            "Viewing conditions",
            "Documentation"
        ],
        primary_authority=["ASME Section V", "ASTM E1030"],
        burden_holder="NDT service provider",
        adversary_position="Film sensitivity is inadequate for flaw detection",
        counter_arguments=[
            "IQI sensitivity meets or exceeds code requirements",
            "Exposure and processing parameters are documented",
            "Radiographs reviewed by certified Level II/III"
        ],
        resolution_strategy="Review radiographs, exposure records, and code criteria.",
        entity_scope="Radiographers, QA/QC, client representatives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 2"
    ),
    DoctrineBlock(
        topic="Digital Radiography (DR) vs Computed Radiography (CR) Sensitivity",
        keywords=["digital radiography", "computed radiography", "sensitivity", "DR", "CR"],
        conclusion_template="DR and CR must achieve equivalent sensitivity to film radiography, with a minimum basic spatial resolution of 100 μm and IQI sensitivity of 2-2T, per ASME Section V and ASTM E2445.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 2 and ASTM E2445 for DR/CR sensitivity requirements.\n"
            "2. Compare basic spatial resolution (BSR) and contrast sensitivity to film radiography.\n"
            "3. Select appropriate detector system and exposure parameters to meet BSR and IQI criteria.\n"
            "4. Validate system performance using reference blocks and IQIs.\n"
            "5. Document system calibration, exposure parameters, and image processing protocols.\n"
            "6. Ensure operator qualification and training on DR/CR systems.\n"
            "7. Address limitations such as detector size, geometry, and access.\n"
            "8. Resolve disputes by reviewing system calibration and image quality records."
        ),
        key_factors=[
            "Basic spatial resolution",
            "IQI sensitivity",
            "System calibration",
            "Operator qualification",
            "Documentation"
        ],
        primary_authority=["ASME Section V", "ASTM E2445"],
        burden_holder="NDT service provider",
        adversary_position="DR/CR sensitivity is inferior to film radiography",
        counter_arguments=[
            "System calibration and IQI sensitivity meet code requirements",
            "Operator is certified and trained on DR/CR",
            "Image quality validated with reference blocks"
        ],
        resolution_strategy="Review image quality records, calibration data, and code criteria.",
        entity_scope="Radiographers, QA/QC, client representatives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 2"
    ),
    DoctrineBlock(
        topic="Magnetic Particle Testing AC vs DC Magnetization",
        keywords=["magnetic particle testing", "AC", "DC", "magnetization", "NDT"],
        conclusion_template="AC magnetization is preferred for surface crack detection due to shallow penetration, while DC (or HWDC) is used for subsurface flaw detection, per ASTM E709 and ASME Section V.",
        reasoning_framework=(
            "1. Reference ASTM E709 and ASME Section V, Article 7 for magnetization methods.\n"
            "2. Understand that AC produces a rapidly reversing magnetic field, enhancing surface crack sensitivity.\n"
            "3. Recognize DC (or HWDC) provides deeper field penetration, suitable for subsurface flaws.\n"
            "4. Select magnetization method based on flaw type, material thickness, and inspection objectives.\n"
            "5. Document current type, amperage, and magnetization technique used.\n"
            "6. Ensure operator qualification and equipment calibration.\n"
            "7. Address limitations such as geometry, material permeability, and access.\n"
            "8. Resolve disputes by reviewing technique selection, calibration, and code requirements."
        ),
        key_factors=[
            "Current type (AC/DC)",
            "Flaw type (surface/subsurface)",
            "Material thickness",
            "Operator qualification",
            "Documentation"
        ],
        primary_authority=["ASTM E709", "ASME Section V"],
        burden_holder="NDT service provider",
        adversary_position="Selected magnetization method is inadequate for flaw detection",
        counter_arguments=[
            "Technique selection based on flaw type and code requirements",
            "Operator is certified and equipment calibrated",
            "Documentation supports method selection"
        ],
        resolution_strategy="Review technique selection, calibration records, and code criteria.",
        entity_scope="MT inspectors, QA/QC, client representatives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM E709"
    ),
    DoctrineBlock(
        topic="Liquid Penetrant Testing Type I Fluorescent Sensitivity Levels",
        keywords=["liquid penetrant testing", "Type I", "fluorescent", "sensitivity", "NDT"],
        conclusion_template="Type I fluorescent penetrants must meet sensitivity Level 2 or higher for critical applications, with system performance verified per ASTM E1417.",
        reasoning_framework=(
            "1. Reference ASTM E1417 for penetrant sensitivity levels and performance verification.\n"
            "2. Select Type I (fluorescent) penetrant for maximum sensitivity to fine surface cracks.\n"
            "3. Specify sensitivity Level 2 (medium) or higher for safety-critical components.\n"
            "4. Verify system performance using reference test panels (e.g., TAM panels).\n"
            "5. Document penetrant type, sensitivity level, and system checks.\n"
            "6. Ensure operator qualification and adherence to process controls.\n"
            "7. Address limitations such as surface condition, contamination, and geometry.\n"
            "8. Resolve disputes by reviewing system performance records and code requirements."
        ),
        key_factors=[
            "Penetrant type and sensitivity",
            "System performance verification",
            "Operator qualification",
            "Process controls",
            "Documentation"
        ],
        primary_authority=["ASTM E1417"],
        burden_holder="NDT service provider",
        adversary_position="Penetrant sensitivity is inadequate for critical flaw detection",
        counter_arguments=[
            "Penetrant meets or exceeds Level 2 sensitivity",
            "System performance verified with reference panels",
            "Operator is certified and process controls documented"
        ],
        resolution_strategy="Review system performance records, penetrant certification, and code criteria.",
        entity_scope="PT inspectors, QA/QC, client representatives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM E1417"
    ),
    DoctrineBlock(
        topic="Eddy Current Testing Frequency Selection for Depth of Penetration",
        keywords=["eddy current testing", "frequency selection", "depth of penetration", "NDT"],
        conclusion_template="Eddy current frequency must be selected to achieve a skin depth appropriate for flaw depth, typically 1-3 times the expected flaw depth, per ASTM E3052.",
        reasoning_framework=(
            "1. Reference ASTM E3052 and E243 for eddy current frequency selection.\n"
            "2. Calculate skin depth using material conductivity, permeability, and frequency.\n"
            "3. Select frequency to ensure penetration to flaw depth while maintaining sensitivity.\n"
            "4. Validate frequency selection with reference standards containing known flaws.\n"
            "5. Document frequency, probe type, and calibration results.\n"
            "6. Ensure operator qualification and equipment calibration.\n"
            "7. Address limitations such as material variations, lift-off, and geometry.\n"
            "8. Resolve disputes by reviewing frequency selection rationale and calibration records."
        ),
        key_factors=[
            "Frequency selection",
            "Skin depth calculation",
            "Reference standards",
            "Operator qualification",
            "Documentation"
        ],
        primary_authority=["ASTM E3052", "ASTM E243"],
        burden_holder="NDT service provider",
        adversary_position="Frequency selection does not provide adequate flaw detection",
        counter_arguments=[
            "Frequency selected based on skin depth calculations",
            "Calibration performed on reference standards",
            "Operator is certified and equipment calibrated"
        ],
        resolution_strategy="Review frequency selection, calibration records, and code criteria.",
        entity_scope="ET inspectors, QA/QC, client representatives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASTM E3052"
    ),
    DoctrineBlock(
        topic="Acoustic Emission Monitoring for Crack Growth Detection",
        keywords=["acoustic emission", "crack growth", "monitoring", "NDT"],
        conclusion_template="Acoustic emission monitoring must be capable of detecting crack growth events above the background noise threshold, with system performance validated per ASTM E1316 and E750.",
        reasoning_framework=(
            "1. Reference ASTM E1316 and E750 for acoustic emission monitoring protocols.\n"
            "2. Establish background noise threshold and event discrimination criteria.\n"
            "3. Select sensor type, placement, and system sensitivity to maximize detection capability.\n"
            "4. Validate system performance using simulated crack growth or reference sources.\n"
            "5. Document system calibration, sensor layout, and monitoring parameters.\n"
            "6. Ensure operator qualification and training.\n"
            "7. Address limitations such as access, material attenuation, and environmental noise.\n"
            "8. Resolve disputes by reviewing system performance records and code requirements."
        ),
        key_factors=[
            "System sensitivity",
            "Background noise threshold",
            "Sensor placement",
            "Operator qualification",
            "Documentation"
        ],
        primary_authority=["ASTM E1316", "ASTM E750"],
        burden_holder="NDT service provider",
        adversary_position="Acoustic emission monitoring is not sensitive enough for crack detection",
        counter_arguments=[
            "System performance validated with reference sources",
            "Operator is certified and trained",
            "Documentation supports monitoring capability"
        ],
        resolution_strategy="Review system performance records, calibration data, and code criteria.",
        entity_scope="AE inspectors, QA/QC, client representatives",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM E750"
    ),
    DoctrineBlock(
        topic="ASNT SNT-TC-1A Personnel Qualification Requirements",
        keywords=["ASNT", "SNT-TC-1A", "personnel qualification", "NDT certification"],
        conclusion_template="NDT personnel must be qualified and certified in accordance with employer's written practice based on ASNT SNT-TC-1A, with records maintained and reviewed.",
        reasoning_framework=(
            "1. Reference ASNT SNT-TC-1A for personnel qualification and certification requirements.\n"
            "2. Employer must develop and maintain a written practice outlining training, experience, and examination criteria.\n"
            "3. Personnel must meet minimum training hours, experience, and pass written, practical, and vision exams.\n"
            "4. Certification records must be maintained and available for audit.\n"
            "5. Recertification and annual vision exams are required.\n"
            "6. Address equivalency of other schemes (e.g., ISO 9712) as permitted by client or code.\n"
            "7. Resolve disputes by reviewing written practice, certification records, and exam results."
        ),
        key_factors=[
            "Written practice",
            "Training and experience",
            "Examination results",
            "Certification records",
            "Recertification"
        ],
        primary_authority=["ASNT SNT-TC-1A"],
        burden_holder="NDT employer",
        adversary_position="Personnel are not properly qualified or certified",
        counter_arguments=[
            "Written practice is in place and followed",
            "Certification records are current and complete",
            "Personnel meet or exceed SNT-TC-1A requirements"
        ],
        resolution_strategy="Review written practice, certification records, and exam results.",
        entity_scope="NDT personnel, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASNT SNT-TC-1A"
    ),
    DoctrineBlock(
        topic="ASME Section V Code Requirements for NDE Methods",
        keywords=["ASME Section V", "NDE", "code requirements", "NDT methods"],
        conclusion_template="All NDE methods must comply with ASME Section V requirements for procedure qualification, personnel certification, and documentation.",
        reasoning_framework=(
            "1. Reference ASME Section V for general and method-specific NDE requirements.\n"
            "2. Procedures must be qualified and approved per Article 1 and method-specific articles.\n"
            "3. Personnel must be qualified and certified per SNT-TC-1A or equivalent.\n"
            "4. All NDE records, including calibration, examination, and results, must be maintained.\n"
            "5. Address any project-specific or client-imposed requirements.\n"
            "6. Resolve disputes by reviewing procedures, personnel records, and documentation."
        ),
        key_factors=[
            "Procedure qualification",
            "Personnel certification",
            "Documentation",
            "Project/client requirements"
        ],
        primary_authority=["ASME Section V"],
        burden_holder="NDT service provider",
        adversary_position="NDE methods do not comply with code requirements",
        counter_arguments=[
            "Procedures are qualified and approved",
            "Personnel are certified per code",
            "Documentation is complete and traceable"
        ],
        resolution_strategy="Review procedures, personnel records, and documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="API 510 Pressure Vessel Inspection Acceptance Criteria",
        keywords=["API 510", "pressure vessel", "inspection", "acceptance criteria"],
        conclusion_template="Inspection results must be evaluated against API 510 acceptance criteria for wall loss, crack-like flaws, and corrosion, with repairs or replacements as required.",
        reasoning_framework=(
            "1. Reference API 510 for pressure vessel inspection and acceptance criteria.\n"
            "2. Evaluate wall thickness measurements against minimum allowable thickness.\n"
            "3. Assess crack-like flaws and corrosion per API 579/ASME FFS-1 if required.\n"
            "4. Document all inspection findings and compare to acceptance limits.\n"
            "5. Recommend repairs or replacements if criteria are not met.\n"
            "6. Resolve disputes by reviewing inspection records, calculations, and code requirements."
        ),
        key_factors=[
            "Minimum allowable thickness",
            "Crack and corrosion assessment",
            "Documentation",
            "Repair/replacement recommendations"
        ],
        primary_authority=["API 510", "API 579", "ASME FFS-1"],
        burden_holder="Owner/user",
        adversary_position="Inspection results do not meet acceptance criteria",
        counter_arguments=[
            "Findings are documented and evaluated per code",
            "Repairs/replacements recommended as required",
            "Calculations and assessments are traceable"
        ],
        resolution_strategy="Review inspection records, calculations, and code criteria.",
        entity_scope="Inspectors, engineers, owner/users",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 510"
    ),
    # Additional doctrines for 40+ coverage
    DoctrineBlock(
        topic="Surface Preparation Requirements for NDT",
        keywords=["surface preparation", "cleanliness", "NDT", "inspection"],
        conclusion_template="Surfaces must be free of scale, paint, oil, and other contaminants prior to NDT, as required by ASME Section V and method-specific standards.",
        reasoning_framework=(
            "1. Reference ASME Section V and method-specific standards for surface preparation.\n"
            "2. Identify contaminants that may affect test sensitivity or accuracy.\n"
            "3. Specify cleaning methods appropriate for the NDT method (e.g., solvent, abrasive, mechanical).\n"
            "4. Verify surface condition prior to inspection and document findings.\n"
            "5. Address limitations such as in-service inspections or access restrictions.\n"
            "6. Resolve disputes by reviewing cleaning records and surface condition documentation."
        ),
        key_factors=[
            "Surface cleanliness",
            "Cleaning method",
            "Documentation",
            "Inspection sensitivity"
        ],
        primary_authority=["ASME Section V", "ASTM E165", "ASTM E709"],
        burden_holder="NDT service provider",
        adversary_position="Surface condition is inadequate for reliable NDT",
        counter_arguments=[
            "Surface was cleaned and inspected prior to NDT",
            "Cleaning method documented and appropriate",
            "Inspection sensitivity verified"
        ],
        resolution_strategy="Review cleaning records and surface condition documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="Calibration Frequency for NDT Equipment",
        keywords=["calibration", "frequency", "NDT equipment", "traceability"],
        conclusion_template="NDT equipment must be calibrated prior to use, after repairs, and at intervals not exceeding 12 months, with records maintained per ASME Section V and manufacturer recommendations.",
        reasoning_framework=(
            "1. Reference ASME Section V and equipment manufacturer guidelines for calibration intervals.\n"
            "2. Calibrate equipment prior to use, after repairs, or if accuracy is in doubt.\n"
            "3. Maintain calibration records traceable to national standards.\n"
            "4. Address project-specific or client-imposed calibration intervals.\n"
            "5. Resolve disputes by reviewing calibration records and traceability documentation."
        ),
        key_factors=[
            "Calibration interval",
            "Traceability",
            "Documentation",
            "Manufacturer recommendations"
        ],
        primary_authority=["ASME Section V", "Equipment manufacturer"],
        burden_holder="NDT service provider",
        adversary_position="Equipment calibration is out of date or not traceable",
        counter_arguments=[
            "Calibration performed within required interval",
            "Records are traceable and complete",
            "Manufacturer recommendations followed"
        ],
        resolution_strategy="Review calibration records and traceability documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Report Traceability and Record Retention",
        keywords=["NDT report", "traceability", "record retention", "documentation"],
        conclusion_template="NDT reports must be traceable to the inspected item and retained for the period specified by code or client, typically 5-10 years, per ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V and client requirements for record retention.\n"
            "2. Ensure reports are uniquely identified and traceable to the inspected item.\n"
            "3. Maintain records in a secure and retrievable format.\n"
            "4. Address client or regulatory requirements for retention period.\n"
            "5. Resolve disputes by reviewing report traceability and retention practices."
        ),
        key_factors=[
            "Report traceability",
            "Retention period",
            "Secure storage",
            "Client/regulatory requirements"
        ],
        primary_authority=["ASME Section V", "Client specification"],
        burden_holder="NDT service provider",
        adversary_position="NDT reports are not traceable or retained as required",
        counter_arguments=[
            "Reports are uniquely identified and traceable",
            "Retention period meets or exceeds requirements",
            "Records are securely stored and retrievable"
        ],
        resolution_strategy="Review report traceability and retention practices.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="Acceptance Criteria for Indications in Magnetic Particle Testing",
        keywords=["magnetic particle testing", "acceptance criteria", "indications", "NDT"],
        conclusion_template="Linear indications longer than 1/16 inch or rounded indications greater than 1/8 inch are rejectable per ASME Section V and ASTM E709.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 7 and ASTM E709 for acceptance criteria.\n"
            "2. Classify indications as linear or rounded.\n"
            "3. Measure indication length and compare to code limits.\n"
            "4. Document all relevant indications and measurements.\n"
            "5. Address client-specific or project acceptance criteria.\n"
            "6. Resolve disputes by reviewing indication records and code requirements."
        ),
        key_factors=[
            "Indication classification",
            "Measurement accuracy",
            "Documentation",
            "Code/client criteria"
        ],
        primary_authority=["ASME Section V", "ASTM E709"],
        burden_holder="NDT service provider",
        adversary_position="Indications are not properly evaluated or documented",
        counter_arguments=[
            "Indications classified and measured per code",
            "Documentation is complete",
            "Client criteria are addressed"
        ],
        resolution_strategy="Review indication records and code criteria.",
        entity_scope="MT inspectors, QA/QC, client representatives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 7"
    ),
    DoctrineBlock(
        topic="Visual Testing Lighting Requirements",
        keywords=["visual testing", "lighting", "illumination", "NDT"],
        conclusion_template="A minimum of 1000 lux (100 foot-candles) of white light is required for visual testing, measured at the inspection surface per ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 9 for lighting requirements.\n"
            "2. Measure illumination at the inspection surface using a calibrated light meter.\n"
            "3. Document lighting measurements and conditions.\n"
            "4. Address limitations such as access or in-service inspections.\n"
            "5. Resolve disputes by reviewing lighting measurement records."
        ),
        key_factors=[
            "Illumination measurement",
            "Calibration of light meter",
            "Documentation",
            "Access limitations"
        ],
        primary_authority=["ASME Section V"],
        burden_holder="NDT service provider",
        adversary_position="Lighting is inadequate for reliable visual testing",
        counter_arguments=[
            "Lighting measured and documented",
            "Light meter is calibrated",
            "Inspection performed under adequate conditions"
        ],
        resolution_strategy="Review lighting measurement records and calibration certificates.",
        entity_scope="VT inspectors, QA/QC, client representatives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 9"
    ),
    DoctrineBlock(
        topic="Ultrasonic Couplant Selection and Control",
        keywords=["ultrasonic testing", "couplant", "selection", "control", "NDT"],
        conclusion_template="Couplant must be compatible with the material and not degrade test sensitivity or cause corrosion, per ASTM E797 and ASME Section V.",
        reasoning_framework=(
            "1. Reference ASTM E797 and ASME Section V for couplant requirements.\n"
            "2. Select couplant compatible with material and inspection environment.\n"
            "3. Ensure couplant does not cause corrosion or degrade test sensitivity.\n"
            "4. Document couplant type, batch, and application method.\n"
            "5. Address limitations such as high temperature or in-service inspections.\n"
            "6. Resolve disputes by reviewing couplant selection and documentation."
        ),
        key_factors=[
            "Couplant compatibility",
            "Corrosion potential",
            "Test sensitivity",
            "Documentation"
        ],
        primary_authority=["ASTM E797", "ASME Section V"],
        burden_holder="NDT service provider",
        adversary_position="Couplant selection degrades test results or causes corrosion",
        counter_arguments=[
            "Couplant is compatible and documented",
            "No evidence of corrosion or sensitivity loss",
            "Selection meets code requirements"
        ],
        resolution_strategy="Review couplant documentation and test results.",
        entity_scope="UT inspectors, QA/QC, client representatives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM E797"
    ),
    DoctrineBlock(
        topic="Minimum Training Hours for Level II NDT Personnel",
        keywords=["training hours", "Level II", "NDT personnel", "qualification"],
        conclusion_template="Level II personnel must complete minimum training hours as specified in SNT-TC-1A (e.g., 40 hours for UT, 32 hours for MT), with documentation maintained.",
        reasoning_framework=(
            "1. Reference SNT-TC-1A for minimum training hours by method and level.\n"
            "2. Verify training records and course content.\n"
            "3. Ensure training is conducted by qualified instructors.\n"
            "4. Maintain documentation for audit and client review.\n"
            "5. Address equivalency of other qualification schemes as permitted.\n"
            "6. Resolve disputes by reviewing training records and written practice."
        ),
        key_factors=[
            "Training hours",
            "Course content",
            "Instructor qualification",
            "Documentation"
        ],
        primary_authority=["ASNT SNT-TC-1A"],
        burden_holder="NDT employer",
        adversary_position="Personnel do not meet minimum training requirements",
        counter_arguments=[
            "Training hours and content documented",
            "Instructors are qualified",
            "Records available for review"
        ],
        resolution_strategy="Review training records and written practice.",
        entity_scope="NDT personnel, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASNT SNT-TC-1A"
    ),
    DoctrineBlock(
        topic="Acceptance Criteria for Liquid Penetrant Testing",
        keywords=["liquid penetrant testing", "acceptance criteria", "indications", "NDT"],
        conclusion_template="Linear indications longer than 1/16 inch or rounded indications greater than 1/8 inch are rejectable per ASME Section V and ASTM E165.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 6 and ASTM E165 for acceptance criteria.\n"
            "2. Classify indications as linear or rounded.\n"
            "3. Measure indication length and compare to code limits.\n"
            "4. Document all relevant indications and measurements.\n"
            "5. Address client-specific or project acceptance criteria.\n"
            "6. Resolve disputes by reviewing indication records and code requirements."
        ),
        key_factors=[
            "Indication classification",
            "Measurement accuracy",
            "Documentation",
            "Code/client criteria"
        ],
        primary_authority=["ASME Section V", "ASTM E165"],
        burden_holder="NDT service provider",
        adversary_position="Indications are not properly evaluated or documented",
        counter_arguments=[
            "Indications classified and measured per code",
            "Documentation is complete",
            "Client criteria are addressed"
        ],
        resolution_strategy="Review indication records and code criteria.",
        entity_scope="PT inspectors, QA/QC, client representatives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 6"
    ),
    DoctrineBlock(
        topic="Minimum Wall Thickness for Pressure Retaining Components",
        keywords=["minimum wall thickness", "pressure retaining", "inspection", "NDT"],
        conclusion_template="Measured wall thickness must not be less than the minimum allowable calculated per ASME Section VIII or API 510, with allowances for corrosion and manufacturing tolerances.",
        reasoning_framework=(
            "1. Reference ASME Section VIII and API 510 for minimum wall thickness calculations.\n"
            "2. Consider design pressure, material strength, and corrosion allowance.\n"
            "3. Compare measured thickness to calculated minimum.\n"
            "4. Document calculations and measurements.\n"
            "5. Address client or regulatory requirements.\n"
            "6. Resolve disputes by reviewing calculations and code requirements."
        ),
        key_factors=[
            "Design pressure",
            "Material strength",
            "Corrosion allowance",
            "Measurement accuracy",
            "Documentation"
        ],
        primary_authority=["ASME Section VIII", "API 510"],
        burden_holder="Owner/user",
        adversary_position="Measured thickness is below minimum allowable",
        counter_arguments=[
            "Calculations and measurements are documented",
            "Allowances are included",
            "Code requirements are met"
        ],
        resolution_strategy="Review calculations, measurements, and code criteria.",
        entity_scope="Inspectors, engineers, owner/users",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII"
    ),
    DoctrineBlock(
        topic="Acceptance Criteria for Ultrasonic Testing of Welds",
        keywords=["ultrasonic testing", "welds", "acceptance criteria", "NDT"],
        conclusion_template="UT indications exceeding amplitude and length limits specified in ASME Section V and project specifications are rejectable.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 4 and project specifications for UT acceptance criteria.\n"
            "2. Measure indication amplitude and length.\n"
            "3. Compare to code and client acceptance limits.\n"
            "4. Document all relevant indications and measurements.\n"
            "5. Address client-specific or project acceptance criteria.\n"
            "6. Resolve disputes by reviewing indication records and code requirements."
        ),
        key_factors=[
            "Indication amplitude",
            "Indication length",
            "Documentation",
            "Code/client criteria"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Indications are not properly evaluated or documented",
        counter_arguments=[
            "Indications measured and documented per code",
            "Client criteria are addressed",
            "Records are complete"
        ],
        resolution_strategy="Review indication records and code criteria.",
        entity_scope="UT inspectors, QA/QC, client representatives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 4"
    ),
    DoctrineBlock(
        topic="Acceptance Criteria for Radiographic Testing of Welds",
        keywords=["radiographic testing", "welds", "acceptance criteria", "NDT"],
        conclusion_template="Radiographic indications exceeding size or density limits specified in ASME Section V and project specifications are rejectable.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 2 and project specifications for RT acceptance criteria.\n"
            "2. Measure indication size and density.\n"
            "3. Compare to code and client acceptance limits.\n"
            "4. Document all relevant indications and measurements.\n"
            "5. Address client-specific or project acceptance criteria.\n"
            "6. Resolve disputes by reviewing indication records and code requirements."
        ),
        key_factors=[
            "Indication size",
            "Indication density",
            "Documentation",
            "Code/client criteria"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Indications are not properly evaluated or documented",
        counter_arguments=[
            "Indications measured and documented per code",
            "Client criteria are addressed",
            "Records are complete"
        ],
        resolution_strategy="Review indication records and code criteria.",
        entity_scope="RT inspectors, QA/QC, client representatives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 2"
    ),
    DoctrineBlock(
        topic="Acceptance Criteria for Eddy Current Testing",
        keywords=["eddy current testing", "acceptance criteria", "indications", "NDT"],
        conclusion_template="Indications exceeding reference standard amplitude or specified limits are rejectable per ASTM E243 and project specifications.",
        reasoning_framework=(
            "1. Reference ASTM E243 and project specifications for ET acceptance criteria.\n"
            "2. Compare indication amplitude to reference standard.\n"
            "3. Document all relevant indications and measurements.\n"
            "4. Address client-specific or project acceptance criteria.\n"
            "5. Resolve disputes by reviewing indication records and code requirements."
        ),
        key_factors=[
            "Indication amplitude",
            "Reference standard",
            "Documentation",
            "Code/client criteria"
        ],
        primary_authority=["ASTM E243", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Indications are not properly evaluated or documented",
        counter_arguments=[
            "Indications measured and documented per code",
            "Client criteria are addressed",
            "Records are complete"
        ],
        resolution_strategy="Review indication records and code criteria.",
        entity_scope="ET inspectors, QA/QC, client representatives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASTM E243"
    ),
    DoctrineBlock(
        topic="Acceptance Criteria for Acoustic Emission Testing",
        keywords=["acoustic emission", "acceptance criteria", "indications", "NDT"],
        conclusion_template="Acoustic emission events exceeding threshold levels or correlating with crack growth are rejectable per ASTM E750 and project specifications.",
        reasoning_framework=(
            "1. Reference ASTM E750 and project specifications for AE acceptance criteria.\n"
            "2. Establish event threshold levels and discrimination criteria.\n"
            "3. Document all relevant events and analysis.\n"
            "4. Address client-specific or project acceptance criteria.\n"
            "5. Resolve disputes by reviewing event records and code requirements."
        ),
        key_factors=[
            "Event threshold",
            "Event analysis",
            "Documentation",
            "Code/client criteria"
        ],
        primary_authority=["ASTM E750", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Events are not properly evaluated or documented",
        counter_arguments=[
            "Events analyzed and documented per code",
            "Client criteria are addressed",
            "Records are complete"
        ],
        resolution_strategy="Review event records and code criteria.",
        entity_scope="AE inspectors, QA/QC, client representatives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASTM E750"
    ),
    DoctrineBlock(
        topic="Acceptance Criteria for Visual Testing",
        keywords=["visual testing", "acceptance criteria", "indications", "NDT"],
        conclusion_template="Surface discontinuities exceeding code or client-specified limits are rejectable per ASME Section V and project specifications.",
        reasoning_framework=(
            "1. Reference ASME Section V, Article 9 and project specifications for VT acceptance criteria.\n"
            "2. Measure and document all relevant discontinuities.\n"
            "3. Compare to code and client acceptance limits.\n"
            "4. Address client-specific or project acceptance criteria.\n"
            "5. Resolve disputes by reviewing indication records and code requirements."
        ),
        key_factors=[
            "Discontinuity measurement",
            "Documentation",
            "Code/client criteria"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Discontinuities are not properly evaluated or documented",
        counter_arguments=[
            "Discontinuities measured and documented per code",
            "Client criteria are addressed",
            "Records are complete"
        ],
        resolution_strategy="Review indication records and code criteria.",
        entity_scope="VT inspectors, QA/QC, client representatives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASME Section V, Article 9"
    ),
    DoctrineBlock(
        topic="NDT Procedure Qualification and Approval",
        keywords=["NDT procedure", "qualification", "approval", "documentation"],
        conclusion_template="NDT procedures must be qualified and approved by a Level III or authorized representative per ASME Section V and project specifications.",
        reasoning_framework=(
            "1. Reference ASME Section V for procedure qualification and approval requirements.\n"
            "2. Develop procedures in accordance with code and client requirements.\n"
            "3. Obtain approval from a Level III or authorized representative.\n"
            "4. Document qualification and approval records.\n"
            "5. Address client-specific or project approval requirements.\n"
            "6. Resolve disputes by reviewing procedure and approval documentation."
        ),
        key_factors=[
            "Procedure qualification",
            "Approval authority",
            "Documentation",
            "Code/client requirements"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Procedures are not properly qualified or approved",
        counter_arguments=[
            "Procedures qualified and approved per code",
            "Records are complete",
            "Client requirements are addressed"
        ],
        resolution_strategy="Review procedure and approval documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Equipment Maintenance and Function Checks",
        keywords=["NDT equipment", "maintenance", "function checks", "NDT"],
        conclusion_template="NDT equipment must undergo regular maintenance and function checks per manufacturer recommendations and ASME Section V, with records maintained.",
        reasoning_framework=(
            "1. Reference ASME Section V and equipment manufacturer guidelines for maintenance and function checks.\n"
            "2. Perform function checks before each use and at regular intervals.\n"
            "3. Document maintenance and function check records.\n"
            "4. Address project-specific or client-imposed requirements.\n"
            "5. Resolve disputes by reviewing maintenance and function check documentation."
        ),
        key_factors=[
            "Maintenance interval",
            "Function check results",
            "Documentation",
            "Manufacturer recommendations"
        ],
        primary_authority=["ASME Section V", "Equipment manufacturer"],
        burden_holder="NDT service provider",
        adversary_position="Equipment maintenance or function checks are inadequate",
        counter_arguments=[
            "Maintenance and function checks performed and documented",
            "Manufacturer recommendations followed",
            "Records are complete"
        ],
        resolution_strategy="Review maintenance and function check documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Subcontractor Qualification and Oversight",
        keywords=["NDT subcontractor", "qualification", "oversight", "NDT"],
        conclusion_template="NDT subcontractors must be qualified per ASME Section V and project requirements, with oversight and audits by the primary contractor.",
        reasoning_framework=(
            "1. Reference ASME Section V and project requirements for subcontractor qualification.\n"
            "2. Verify subcontractor procedures, personnel, and equipment meet code and client requirements.\n"
            "3. Conduct regular audits and oversight.\n"
            "4. Document qualification and audit records.\n"
            "5. Address client-specific or project oversight requirements.\n"
            "6. Resolve disputes by reviewing qualification and audit documentation."
        ),
        key_factors=[
            "Subcontractor qualification",
            "Audit records",
            "Oversight procedures",
            "Documentation"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="Primary contractor",
        adversary_position="Subcontractor does not meet qualification or oversight requirements",
        counter_arguments=[
            "Subcontractor qualification and audits documented",
            "Oversight procedures in place",
            "Client requirements are addressed"
        ],
        resolution_strategy="Review qualification and audit documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Personnel Vision Requirements",
        keywords=["NDT personnel", "vision requirements", "eye examination", "NDT"],
        conclusion_template="NDT personnel must pass annual near-vision and color-vision examinations per SNT-TC-1A and ASME Section V, with records maintained.",
        reasoning_framework=(
            "1. Reference SNT-TC-1A and ASME Section V for vision requirements.\n"
            "2. Conduct near-vision and color-vision exams annually.\n"
            "3. Maintain examination records for audit and client review.\n"
            "4. Address equivalency of other qualification schemes as permitted.\n"
            "5. Resolve disputes by reviewing vision examination records."
        ),
        key_factors=[
            "Near-vision exam",
            "Color-vision exam",
            "Documentation",
            "Annual frequency"
        ],
        primary_authority=["ASNT SNT-TC-1A", "ASME Section V"],
        burden_holder="NDT employer",
        adversary_position="Personnel do not meet vision requirements",
        counter_arguments=[
            "Vision exams performed and documented",
            "Records are current",
            "Requirements are met"
        ],
        resolution_strategy="Review vision examination records.",
        entity_scope="NDT personnel, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASNT SNT-TC-1A"
    ),
    DoctrineBlock(
        topic="NDT Method Selection for Specific Flaw Types",
        keywords=["NDT method selection", "flaw type", "inspection planning", "NDT"],
        conclusion_template="NDT methods must be selected based on flaw type, material, geometry, and code requirements, with rationale documented per ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V and project requirements for method selection.\n"
            "2. Assess flaw type, material, and geometry to determine appropriate NDT method.\n"
            "3. Document method selection rationale and approval.\n"
            "4. Address client-specific or project requirements.\n"
            "5. Resolve disputes by reviewing method selection documentation."
        ),
        key_factors=[
            "Flaw type",
            "Material",
            "Geometry",
            "Documentation"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Method selection is not appropriate for flaw detection",
        counter_arguments=[
            "Method selection rationale documented",
            "Code and client requirements are addressed",
            "Records are complete"
        ],
        resolution_strategy="Review method selection documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Personnel Recertification Requirements",
        keywords=["NDT personnel", "recertification", "qualification", "NDT"],
        conclusion_template="NDT personnel must be recertified at intervals not exceeding 5 years per SNT-TC-1A and employer's written practice.",
        reasoning_framework=(
            "1. Reference SNT-TC-1A and employer's written practice for recertification intervals.\n"
            "2. Conduct recertification exams and review experience records.\n"
            "3. Maintain recertification documentation for audit and client review.\n"
            "4. Address equivalency of other qualification schemes as permitted.\n"
            "5. Resolve disputes by reviewing recertification records."
        ),
        key_factors=[
            "Recertification interval",
            "Examination results",
            "Experience records",
            "Documentation"
        ],
        primary_authority=["ASNT SNT-TC-1A", "Employer written practice"],
        burden_holder="NDT employer",
        adversary_position="Personnel are not properly recertified",
        counter_arguments=[
            "Recertification exams performed and documented",
            "Records are current",
            "Requirements are met"
        ],
        resolution_strategy="Review recertification records.",
        entity_scope="NDT personnel, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASNT SNT-TC-1A"
    ),
    DoctrineBlock(
        topic="NDT Method Demonstration and Validation",
        keywords=["NDT method", "demonstration", "validation", "NDT"],
        conclusion_template="NDT methods must be demonstrated and validated on representative samples or calibration blocks prior to production use, per ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V for demonstration and validation requirements.\n"
            "2. Perform demonstration on representative samples or calibration blocks with known flaws.\n"
            "3. Document demonstration results and approval.\n"
            "4. Address client-specific or project demonstration requirements.\n"
            "5. Resolve disputes by reviewing demonstration and validation records."
        ),
        key_factors=[
            "Demonstration results",
            "Sample representativeness",
            "Documentation",
            "Approval authority"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="NDT service provider",
        adversary_position="Method demonstration or validation is inadequate",
        counter_arguments=[
            "Demonstration performed and documented",
            "Samples are representative",
            "Records are complete"
        ],
        resolution_strategy="Review demonstration and validation records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Procedure Deviation and Nonconformance Management",
        keywords=["NDT procedure", "deviation", "nonconformance", "NDT"],
        conclusion_template="All deviations from approved NDT procedures must be documented, evaluated, and dispositioned per ASME Section V and client requirements.",
        reasoning_framework=(
            "1. Reference ASME Section V and client requirements for deviation management.\n"
            "2. Document all deviations and nonconformances.\n"
            "3. Evaluate impact on inspection results and product quality.\n"
            "4. Obtain approval for disposition from authorized personnel.\n"
            "5. Address client-specific or project deviation management requirements.\n"
            "6. Resolve disputes by reviewing deviation and disposition records."
        ),
        key_factors=[
            "Deviation documentation",
            "Impact evaluation",
            "Disposition approval",
            "Code/client requirements"
        ],
        primary_authority=["ASME Section V", "Client specification"],
        burden_holder="NDT service provider",
        adversary_position="Deviations are not properly managed or documented",
        counter_arguments=[
            "Deviations documented and evaluated",
            "Disposition approved by authorized personnel",
            "Records are complete"
        ],
        resolution_strategy="Review deviation and disposition records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Data Security and Electronic Record Management",
        keywords=["NDT data security", "electronic records", "record management", "NDT"],
        conclusion_template="Electronic NDT records must be securely stored, backed up, and protected from unauthorized access per ASME Section V and client requirements.",
        reasoning_framework=(
            "1. Reference ASME Section V and client requirements for electronic record management.\n"
            "2. Implement secure storage and backup protocols.\n"
            "3. Restrict access to authorized personnel only.\n"
            "4. Maintain data integrity and retrievability.\n"
            "5. Address client-specific or project data security requirements.\n"
            "6. Resolve disputes by reviewing data security and access records."
        ),
        key_factors=[
            "Data security",
            "Backup protocols",
            "Access control",
            "Documentation"
        ],
        primary_authority=["ASME Section V", "Client specification"],
        burden_holder="NDT service provider",
        adversary_position="Electronic records are not secure or retrievable",
        counter_arguments=[
            "Data security and backup protocols implemented",
            "Access restricted to authorized personnel",
            "Records are retrievable and complete"
        ],
        resolution_strategy="Review data security and access records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Equipment Identification and Traceability",
        keywords=["NDT equipment", "identification", "traceability", "NDT"],
        conclusion_template="All NDT equipment must be uniquely identified and traceable to calibration and maintenance records per ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V for equipment identification and traceability requirements.\n"
            "2. Assign unique identification numbers to all equipment.\n"
            "3. Maintain traceability to calibration and maintenance records.\n"
            "4. Address client-specific or project identification requirements.\n"
            "5. Resolve disputes by reviewing identification and traceability records."
        ),
        key_factors=[
            "Unique identification",
            "Traceability",
            "Documentation",
            "Code/client requirements"
        ],
        primary_authority=["ASME Section V"],
        burden_holder="NDT service provider",
        adversary_position="Equipment is not properly identified or traceable",
        counter_arguments=[
            "Equipment uniquely identified",
            "Traceability to records maintained",
            "Requirements are met"
        ],
        resolution_strategy="Review identification and traceability records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Personnel Training Program Documentation",
        keywords=["NDT personnel", "training program", "documentation", "NDT"],
        conclusion_template="NDT personnel training programs must be documented, including course content, instructor qualifications, and participant records per SNT-TC-1A.",
        reasoning_framework=(
            "1. Reference SNT-TC-1A for training program documentation requirements.\n"
            "2. Document course content, instructor qualifications, and participant records.\n"
            "3. Maintain records for audit and client review.\n"
            "4. Address client-specific or project training documentation requirements.\n"
            "5. Resolve disputes by reviewing training program documentation."
        ),
        key_factors=[
            "Course content",
            "Instructor qualification",
            "Participant records",
            "Documentation"
        ],
        primary_authority=["ASNT SNT-TC-1A"],
        burden_holder="NDT employer",
        adversary_position="Training program documentation is inadequate",
        counter_arguments=[
            "Course content and instructor qualifications documented",
            "Participant records maintained",
            "Requirements are met"
        ],
        resolution_strategy="Review training program documentation.",
        entity_scope="NDT personnel, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASNT SNT-TC-1A"
    ),
    DoctrineBlock(
        topic="NDT Method Limitations and Applicability",
        keywords=["NDT method", "limitations", "applicability", "NDT"],
        conclusion_template="Limitations and applicability of NDT methods must be documented and communicated to stakeholders per ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V for method limitations and applicability.\n"
            "2. Document limitations such as material, geometry, and flaw detectability.\n"
            "3. Communicate limitations to stakeholders and obtain acknowledgment.\n"
            "4. Address client-specific or project communication requirements.\n"
            "5. Resolve disputes by reviewing limitation documentation and communication records."
        ),
        key_factors=[
            "Limitation documentation",
            "Stakeholder communication",
            "Acknowledgment records",
            "Code/client requirements"
        ],
        primary_authority=["ASME Section V"],
        burden_holder="NDT service provider",
        adversary_position="Method limitations are not properly documented or communicated",
        counter_arguments=[
            "Limitations documented and communicated",
            "Stakeholder acknowledgment obtained",
            "Records are complete"
        ],
        resolution_strategy="Review limitation documentation and communication records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Subcontractor Personnel Qualification",
        keywords=["NDT subcontractor", "personnel qualification", "NDT"],
        conclusion_template="NDT subcontractor personnel must be qualified and certified per SNT-TC-1A or equivalent, with records available for audit.",
        reasoning_framework=(
            "1. Reference SNT-TC-1A and project requirements for subcontractor personnel qualification.\n"
            "2. Verify certification records and training.\n"
            "3. Maintain records for audit and client review.\n"
            "4. Address client-specific or project qualification requirements.\n"
            "5. Resolve disputes by reviewing certification records."
        ),
        key_factors=[
            "Certification records",
            "Training",
            "Documentation",
            "Code/client requirements"
        ],
        primary_authority=["ASNT SNT-TC-1A", "Project specification"],
        burden_holder="NDT subcontractor",
        adversary_position="Subcontractor personnel are not properly qualified or certified",
        counter_arguments=[
            "Certification and training records documented",
            "Requirements are met",
            "Records available for audit"
        ],
        resolution_strategy="Review certification records.",
        entity_scope="NDT subcontractor personnel, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASNT SNT-TC-1A"
    ),
    DoctrineBlock(
        topic="NDT Method Change Control",
        keywords=["NDT method", "change control", "NDT"],
        conclusion_template="All changes to NDT methods or procedures must be documented, reviewed, and approved per ASME Section V and client requirements.",
        reasoning_framework=(
            "1. Reference ASME Section V and client requirements for change control.\n"
            "2. Document all changes to methods or procedures.\n"
            "3. Obtain review and approval from authorized personnel.\n"
            "4. Maintain change control records for audit and client review.\n"
            "5. Resolve disputes by reviewing change control documentation."
        ),
        key_factors=[
            "Change documentation",
            "Review and approval",
            "Audit records",
            "Code/client requirements"
        ],
        primary_authority=["ASME Section V", "Client specification"],
        burden_holder="NDT service provider",
        adversary_position="Method changes are not properly controlled or documented",
        counter_arguments=[
            "Changes documented, reviewed, and approved",
            "Records maintained",
            "Requirements are met"
        ],
        resolution_strategy="Review change control documentation.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Equipment Storage and Handling",
        keywords=["NDT equipment", "storage", "handling", "NDT"],
        conclusion_template="NDT equipment must be stored and handled to prevent damage, contamination, or calibration loss per manufacturer recommendations and ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V and equipment manufacturer guidelines for storage and handling.\n"
            "2. Store equipment in clean, dry, and secure locations.\n"
            "3. Handle equipment to prevent damage or calibration loss.\n"
            "4. Document storage and handling procedures.\n"
            "5. Address client-specific or project storage requirements.\n"
            "6. Resolve disputes by reviewing storage and handling records."
        ),
        key_factors=[
            "Storage conditions",
            "Handling procedures",
            "Documentation",
            "Manufacturer recommendations"
        ],
        primary_authority=["ASME Section V", "Equipment manufacturer"],
        burden_holder="NDT service provider",
        adversary_position="Equipment storage or handling is inadequate",
        counter_arguments=[
            "Storage and handling procedures documented",
            "Manufacturer recommendations followed",
            "Records are complete"
        ],
        resolution_strategy="Review storage and handling records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Subcontractor Oversight and Audit Frequency",
        keywords=["NDT subcontractor", "oversight", "audit frequency", "NDT"],
        conclusion_template="NDT subcontractors must be audited at intervals not exceeding 12 months, with oversight records maintained per ASME Section V.",
        reasoning_framework=(
            "1. Reference ASME Section V and project requirements for subcontractor oversight and audit frequency.\n"
            "2. Conduct audits at intervals not exceeding 12 months.\n"
            "3. Maintain oversight and audit records for audit and client review.\n"
            "4. Address client-specific or project oversight requirements.\n"
            "5. Resolve disputes by reviewing oversight and audit records."
        ),
        key_factors=[
            "Audit frequency",
            "Oversight records",
            "Documentation",
            "Code/client requirements"
        ],
        primary_authority=["ASME Section V", "Project specification"],
        burden_holder="Primary contractor",
        adversary_position="Subcontractor oversight or audit frequency is inadequate",
        counter_arguments=[
            "Audits conducted and documented",
            "Records maintained",
            "Requirements are met"
        ],
        resolution_strategy="Review oversight and audit records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section V"
    ),
    DoctrineBlock(
        topic="NDT Equipment Calibration Labeling",
        keywords=["NDT equipment", "calibration labeling", "NDT"],
        conclusion_template="NDT equipment must display current calibration status and due date labeling per ASME Section V and manufacturer recommendations.",
        reasoning_framework=(
            "1. Reference ASME Section V and equipment manufacturer guidelines for calibration labeling.\n"
            "2. Label equipment with calibration status and due date.\n"
            "3. Maintain labeling records for audit and client review.\n"
            "4. Address client-specific or project labeling requirements.\n"
            "5. Resolve disputes by reviewing labeling and calibration records."
        ),
        key_factors=[
            "Calibration status labeling",
            "Due date labeling",
            "Documentation",
            "Code/client requirements"
        ],
        primary_authority=["ASME Section V", "Equipment manufacturer"],
        burden_holder="NDT service provider",
        adversary_position="Calibration labeling is missing or out of date",
        counter_arguments=[
            "Labeling is current and documented",
            "Records maintained",
            "Requirements are met"
        ],
        resolution_strategy="Review labeling and calibration records.",
        entity_scope="NDT inspectors, QA/QC, client representatives",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section V"
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