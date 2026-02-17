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
        topic="UIC Class II Injection Well Permit Requirements",
        keywords=[
            "UIC", "Class II", "permit", "application", "EPA", "authorization", "well construction", "compliance"
        ],
        conclusion_template="A Class II injection well must obtain a UIC permit by demonstrating compliance with EPA and state-specific requirements.",
        reasoning_framework=(
            "The UIC Class II permit process is governed by 40 CFR 144-146 and relevant state regulations. "
            "Applicants must submit detailed well construction plans, area of review (AOR) delineation, "
            "demonstrate mechanical integrity, and provide evidence of financial responsibility. "
            "The reviewing authority evaluates the proposed injection zone, confining layers, "
            "potential for endangerment of underground sources of drinking water (USDWs), "
            "and the operator's compliance history. "
            "Public notice and comment are required prior to permit issuance. "
            "Permit conditions may include monitoring, reporting, and operational limits. "
            "Failure to meet requirements results in denial or revocation of the permit."
        ),
        key_factors=[
            "Well construction standards",
            "AOR delineation",
            "Mechanical integrity demonstration",
            "Financial responsibility",
            "Public notice and comment",
            "USDW protection"
        ],
        primary_authority=[
            "40 CFR 144-146",
            "EPA UIC Program Guidance",
            "State UIC regulations"
        ],
        burden_holder="Applicant (well operator)",
        adversary_position="Permitting authority may deny permit if requirements are not met or if USDWs are at risk.",
        counter_arguments=[
            "Applicant may argue that proposed controls are sufficient to protect USDWs.",
            "Operator may challenge the extent of AOR or stringency of construction requirements."
        ],
        resolution_strategy="Technical review, public comment, and administrative appeal processes.",
        entity_scope="Class II injection wells (brine, EOR, hydrocarbon storage)",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34; 40 CFR 144.31"
    ),
    DoctrineBlock(
        topic="Injection Pressure Limits and Fracture Gradient",
        keywords=[
            "injection pressure", "fracture gradient", "formation integrity", "pressure monitoring", "permit condition"
        ],
        conclusion_template="Injection pressure must not exceed the calculated fracture gradient to prevent migration of fluids into USDWs.",
        reasoning_framework=(
            "The maximum allowable injection pressure is determined by the fracture gradient of the injection formation, "
            "which is calculated based on site-specific geologic and hydrostatic data. "
            "Operators must conduct formation tests to establish the fracture pressure, "
            "and regulatory authorities set permit limits accordingly. "
            "Continuous pressure monitoring is required to ensure compliance. "
            "Exceeding the pressure limit can result in loss of mechanical integrity, "
            "fracturing of confining layers, and migration of injected fluids. "
            "Violations may lead to permit suspension or revocation."
        ),
        key_factors=[
            "Formation fracture gradient",
            "Site-specific geologic data",
            "Continuous pressure monitoring",
            "Permit-specified pressure limits"
        ],
        primary_authority=[
            "40 CFR 146.13(a)",
            "EPA UIC Guidance #39"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege that pressure limits are exceeded, risking USDW contamination.",
        counter_arguments=[
            "Operator may argue that pressure excursions were transient and did not compromise integrity.",
            "Operator may present additional formation test data."
        ],
        resolution_strategy="Review of pressure logs, formation test results, and third-party technical analysis.",
        entity_scope="All UIC injection wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="In re Enron Oil & Gas, EPA UIC Docket 92-3"
    ),
    DoctrineBlock(
        topic="Mechanical Integrity Test (MIT) Requirements",
        keywords=[
            "mechanical integrity", "MIT", "well integrity", "pressure test", "annulus monitoring", "compliance"
        ],
        conclusion_template="Injection wells must demonstrate mechanical integrity at least once every five years or as required by the permit.",
        reasoning_framework=(
            "Mechanical integrity is demonstrated through two main methods: "
            "(1) No significant leak in the casing, tubing, or packer (internal MIT), "
            "and (2) No significant fluid movement into USDWs through channels adjacent to the wellbore (external MIT). "
            "Testing methods include pressure tests, radioactive tracer surveys, and temperature logs. "
            "MITs must be performed prior to initial injection, after workovers, and at prescribed intervals. "
            "Failure to demonstrate integrity requires immediate cessation of injection and corrective action."
        ),
        key_factors=[
            "Test frequency",
            "Test method selection",
            "Test result interpretation",
            "Corrective action requirements"
        ],
        primary_authority=[
            "40 CFR 146.8",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may assert that MITs are insufficient or improperly conducted.",
        counter_arguments=[
            "Operator may provide additional test data or request alternative MIT methods.",
            "Operator may challenge interpretation of test results."
        ],
        resolution_strategy="Review of test records, third-party verification, and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Area of Review (AOR) Calculations",
        keywords=[
            "AOR", "area of review", "confinement", "well inventory", "plume modeling", "endangerment"
        ],
        conclusion_template="The AOR must be calculated using either a fixed radius or computational model to identify wells that may be affected by injection activities.",
        reasoning_framework=(
            "The AOR is the region surrounding the injection well where USDWs may be endangered by fluid movement. "
            "Operators may use a fixed radius (typically 1/4 mile for Class II) or a computational model based on site-specific hydrogeology. "
            "All wells within the AOR must be identified, evaluated for integrity, and remediated if necessary. "
            "AOR must be reassessed at permit renewal or when operational parameters change."
        ),
        key_factors=[
            "AOR calculation method",
            "Well inventory completeness",
            "Hydrogeologic data",
            "Remediation of deficient wells"
        ],
        primary_authority=[
            "40 CFR 146.6",
            "EPA UIC Guidance #24"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may challenge adequacy of AOR or completeness of well inventory.",
        counter_arguments=[
            "Operator may present additional modeling or well survey data.",
            "Operator may argue for alternative AOR delineation based on site conditions."
        ],
        resolution_strategy="Technical review, third-party modeling, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #24"
    ),
    DoctrineBlock(
        topic="Well Casing Requirements for Injection Wells",
        keywords=[
            "well casing", "steel casing", "cementing", "corrosion protection", "construction standards"
        ],
        conclusion_template="Injection wells must be constructed with casing and cementing practices that prevent fluid migration into USDWs.",
        reasoning_framework=(
            "Well casing must be of sufficient strength and corrosion resistance to withstand injection pressures and chemical exposure. "
            "Casing must be cemented to at least 50 feet above the injection zone and extend to the surface. "
            "Cement bond logs and casing inspection logs are required to verify placement. "
            "Additional casing strings may be required for deep or high-pressure wells. "
            "Deficient casing must be repaired or the well must be plugged."
        ),
        key_factors=[
            "Casing material and grade",
            "Cementing practices",
            "Verification logs",
            "Repair and remediation"
        ],
        primary_authority=[
            "40 CFR 146.22",
            "API RP 10B-2"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate casing or cementing, risking USDW contamination.",
        counter_arguments=[
            "Operator may provide additional logs or engineering analysis.",
            "Operator may propose alternative casing designs."
        ],
        resolution_strategy="Review of construction records, cement bond logs, and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #17"
    ),
    DoctrineBlock(
        topic="Cement Bond Evaluation for Injection Wells",
        keywords=[
            "cement bond", "cement evaluation", "CBL", "well integrity", "cement logging"
        ],
        conclusion_template="Cement bond logs must demonstrate adequate cement placement to prevent fluid migration.",
        reasoning_framework=(
            "Cement bond evaluation is performed using acoustic or sonic logs to assess the quality and continuity of cement behind casing. "
            "Logs must be interpreted by qualified personnel. "
            "Poor cement bonds may require remedial cementing or squeeze jobs. "
            "Cement evaluation is required after well construction and after major workovers. "
            "Inadequate cement placement is grounds for permit denial or enforcement action."
        ),
        key_factors=[
            "CBL interpretation",
            "Remedial cementing",
            "Qualified personnel",
            "Documentation"
        ],
        primary_authority=[
            "40 CFR 146.22",
            "API RP 10B-2"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may dispute adequacy of cement bond or interpretation of logs.",
        counter_arguments=[
            "Operator may provide additional logs or third-party interpretations.",
            "Operator may propose alternative evaluation methods."
        ],
        resolution_strategy="Independent log review and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #17"
    ),
    DoctrineBlock(
        topic="Annular Pressure Monitoring Requirements",
        keywords=[
            "annular pressure", "pressure monitoring", "well integrity", "annulus", "continuous monitoring"
        ],
        conclusion_template="Annular pressure must be continuously monitored and maintained within permit-specified limits.",
        reasoning_framework=(
            "Annular pressure monitoring detects leaks or loss of mechanical integrity. "
            "Operators must install pressure gauges and record annular pressure at prescribed intervals, "
            "typically continuously or at least daily. "
            "Significant changes in annular pressure require immediate investigation and reporting. "
            "Failure to maintain or monitor annular pressure is a violation of permit conditions."
        ),
        key_factors=[
            "Monitoring frequency",
            "Alarm thresholds",
            "Response procedures",
            "Data recording"
        ],
        primary_authority=[
            "40 CFR 146.13(d)",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate monitoring or failure to respond to pressure anomalies.",
        counter_arguments=[
            "Operator may demonstrate proper monitoring and timely response.",
            "Operator may argue that pressure changes were not indicative of integrity loss."
        ],
        resolution_strategy="Review of pressure records, incident reports, and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Plugging and Abandonment Requirements",
        keywords=[
            "plugging", "abandonment", "well closure", "cement plugs", "site restoration"
        ],
        conclusion_template="Injection wells must be plugged and abandoned in accordance with regulatory standards to prevent fluid migration.",
        reasoning_framework=(
            "Plugging and abandonment procedures require placement of cement plugs across all USDW intervals and the injection zone. "
            "Operators must submit a plugging plan for approval prior to well closure. "
            "Site restoration includes removal of surface equipment and remediation of contamination. "
            "Plugging records must be submitted for regulatory review. "
            "Improperly plugged wells are subject to enforcement and corrective action."
        ),
        key_factors=[
            "Plugging plan approval",
            "Cement plug placement",
            "Site restoration",
            "Record submission"
        ],
        primary_authority=[
            "40 CFR 146.10",
            "EPA UIC Guidance #20"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate plugging or failure to restore site.",
        counter_arguments=[
            "Operator may provide additional documentation or third-party verification.",
            "Operator may challenge restoration requirements."
        ],
        resolution_strategy="Regulatory inspection and review of plugging records.",
        entity_scope="All UIC injection wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #20"
    ),
    DoctrineBlock(
        topic="EPA UIC Regulations 40 CFR 144-148 Overview",
        keywords=[
            "EPA", "UIC", "regulations", "40 CFR", "overview", "compliance"
        ],
        conclusion_template="All injection well operations must comply with EPA UIC regulations as codified in 40 CFR Parts 144-148.",
        reasoning_framework=(
            "The UIC program establishes minimum federal requirements for injection well permitting, construction, operation, monitoring, "
            "and closure. States may implement more stringent requirements. "
            "Operators must comply with all applicable provisions, including permit application, mechanical integrity, "
            "monitoring, and reporting. "
            "Non-compliance may result in enforcement actions, including fines and permit revocation."
        ),
        key_factors=[
            "Federal and state requirements",
            "Permit compliance",
            "Monitoring and reporting",
            "Enforcement provisions"
        ],
        primary_authority=[
            "40 CFR 144-148",
            "Safe Drinking Water Act (SDWA)"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege non-compliance with UIC regulations.",
        counter_arguments=[
            "Operator may demonstrate compliance or challenge regulatory interpretation.",
            "Operator may seek variance or alternative compliance."
        ],
        resolution_strategy="Administrative review and appeal processes.",
        entity_scope="All UIC injection wells",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Safe Drinking Water Act, 42 U.S.C. § 300h"
    ),
    DoctrineBlock(
        topic="Injection Well Classification (Class I, II, III, IV, V, VI)",
        keywords=[
            "well classification", "Class I", "Class II", "Class III", "Class IV", "Class V", "Class VI", "UIC"
        ],
        conclusion_template="Injection wells are classified by the type of fluid injected and purpose, determining applicable regulatory requirements.",
        reasoning_framework=(
            "Class I: Industrial and municipal waste disposal wells. "
            "Class II: Oil and gas related injection wells (EOR, brine disposal, hydrocarbon storage). "
            "Class III: Solution mining wells. "
            "Class IV: Hazardous waste injection into or above USDWs (generally banned). "
            "Class V: All other injection wells not covered by Classes I-IV. "
            "Class VI: CO2 geologic sequestration wells. "
            "Each class has distinct construction, monitoring, and reporting requirements."
        ),
        key_factors=[
            "Fluid type",
            "Injection purpose",
            "Regulatory requirements by class"
        ],
        primary_authority=[
            "40 CFR 144.6",
            "EPA UIC Program"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may reclassify well or allege non-compliance with class-specific requirements.",
        counter_arguments=[
            "Operator may provide evidence supporting well classification.",
            "Operator may challenge regulatory interpretation."
        ],
        resolution_strategy="Review of well records, fluid analysis, and regulatory classification.",
        entity_scope="All UIC injection wells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Enhanced Oil Recovery (EOR) Injection Wells",
        keywords=[
            "EOR", "enhanced oil recovery", "CO2 injection", "waterflood", "Class II", "tertiary recovery"
        ],
        conclusion_template="EOR injection wells must comply with Class II UIC requirements and demonstrate protection of USDWs.",
        reasoning_framework=(
            "EOR wells inject fluids (water, CO2, polymers) to enhance hydrocarbon recovery. "
            "They are regulated as Class II wells and must meet construction, monitoring, and reporting standards. "
            "Operators must demonstrate that injection activities will not endanger USDWs. "
            "EOR projects may require additional monitoring due to pressure interference and plume migration."
        ),
        key_factors=[
            "Fluid type and volume",
            "Pressure management",
            "Monitoring and reporting",
            "USDW protection"
        ],
        primary_authority=[
            "40 CFR 146.5(b)",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege EOR operations risk USDW contamination.",
        counter_arguments=[
            "Operator may provide site-specific monitoring and modeling data.",
            "Operator may propose additional controls."
        ],
        resolution_strategy="Technical review, site inspection, and regulatory oversight.",
        entity_scope="Class II EOR injection wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="CO2 Sequestration Class VI Injection Wells",
        keywords=[
            "CO2 sequestration", "Class VI", "geologic storage", "carbon capture", "long-term monitoring"
        ],
        conclusion_template="Class VI wells for CO2 sequestration must meet stringent siting, construction, monitoring, and post-injection care requirements.",
        reasoning_framework=(
            "Class VI wells are designed for long-term geologic storage of CO2. "
            "Operators must conduct extensive site characterization, including geologic, hydrologic, and seismic studies. "
            "Construction standards require multiple casing strings and cementing to protect USDWs. "
            "Monitoring includes pressure, plume migration, and groundwater quality. "
            "A post-injection site care (PISC) period of at least 50 years is required. "
            "Financial responsibility must be demonstrated for the duration of the project."
        ),
        key_factors=[
            "Site characterization",
            "Construction and cementing",
            "Long-term monitoring",
            "Financial responsibility"
        ],
        primary_authority=[
            "40 CFR 146.81-95",
            "EPA UIC Guidance #83"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate site characterization or monitoring.",
        counter_arguments=[
            "Operator may provide additional studies or propose enhanced monitoring.",
            "Operator may challenge duration of PISC."
        ],
        resolution_strategy="Technical review, public comment, and regulatory oversight.",
        entity_scope="Class VI CO2 sequestration wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #83"
    ),
    DoctrineBlock(
        topic="Formation Compatibility Testing",
        keywords=[
            "formation compatibility", "fluid compatibility", "scaling", "precipitation", "formation damage"
        ],
        conclusion_template="Operators must conduct formation compatibility testing to prevent scaling, precipitation, or formation damage.",
        reasoning_framework=(
            "Formation compatibility testing involves laboratory analysis of injection fluids and formation water/rock. "
            "Testing identifies risks of mineral scaling, precipitation, or chemical reactions that may reduce injectivity or compromise integrity. "
            "Results inform selection of injection fluids and treatment protocols. "
            "Testing is required prior to initial injection and after significant changes in fluid composition."
        ),
        key_factors=[
            "Laboratory analysis",
            "Fluid and formation chemistry",
            "Risk of scaling/precipitation",
            "Mitigation measures"
        ],
        primary_authority=[
            "40 CFR 146.13(b)",
            "API RP 45"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate testing or risk of formation damage.",
        counter_arguments=[
            "Operator may provide additional laboratory data or propose mitigation measures.",
            "Operator may challenge necessity of repeated testing."
        ],
        resolution_strategy="Review of laboratory reports and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 45"
    ),
    DoctrineBlock(
        topic="Injection Rate Optimization",
        keywords=[
            "injection rate", "optimization", "injectivity", "formation pressure", "operational efficiency"
        ],
        conclusion_template="Injection rates must be optimized to maximize injectivity while maintaining formation integrity and regulatory compliance.",
        reasoning_framework=(
            "Injection rate optimization balances operational efficiency with regulatory and geomechanical constraints. "
            "Operators must monitor formation pressure, injectivity index, and wellhead pressure. "
            "Excessive rates may exceed fracture gradient or reduce sweep efficiency in EOR operations. "
            "Regulatory limits on maximum injection rate and pressure must be observed."
        ),
        key_factors=[
            "Injectivity index",
            "Formation pressure",
            "Regulatory limits",
            "Operational efficiency"
        ],
        primary_authority=[
            "40 CFR 146.13(a)",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege that injection rates exceed safe or permitted limits.",
        counter_arguments=[
            "Operator may provide injectivity and pressure data supporting current rates.",
            "Operator may propose operational changes."
        ],
        resolution_strategy="Review of injection logs, pressure data, and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Wellbore Failure Modes and Risk Mitigation",
        keywords=[
            "wellbore failure", "risk mitigation", "casing collapse", "corrosion", "cement failure", "integrity"
        ],
        conclusion_template="Operators must identify and mitigate wellbore failure modes to maintain mechanical integrity.",
        reasoning_framework=(
            "Wellbore failure modes include casing collapse, corrosion, cement failure, and loss of zonal isolation. "
            "Risk mitigation involves proper material selection, corrosion monitoring, regular integrity testing, "
            "and timely remediation of detected issues. "
            "Failure to address risks may result in loss of containment and regulatory enforcement."
        ),
        key_factors=[
            "Failure mode identification",
            "Material selection",
            "Monitoring and testing",
            "Remediation protocols"
        ],
        primary_authority=[
            "40 CFR 146.8",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate risk mitigation or failure to remediate.",
        counter_arguments=[
            "Operator may provide risk assessments and remediation records.",
            "Operator may propose alternative mitigation strategies."
        ],
        resolution_strategy="Review of risk assessments, inspection records, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring in Injection Wells",
        keywords=[
            "corrosion monitoring", "corrosion coupons", "electrical resistance", "well integrity", "chemical treatment"
        ],
        conclusion_template="Operators must implement corrosion monitoring and mitigation programs to ensure well integrity.",
        reasoning_framework=(
            "Corrosion monitoring is performed using corrosion coupons, electrical resistance probes, and fluid analysis. "
            "Results inform chemical treatment programs and maintenance schedules. "
            "Significant corrosion requires remediation or replacement of affected components. "
            "Corrosion monitoring records must be maintained and submitted as required."
        ),
        key_factors=[
            "Monitoring method selection",
            "Frequency of monitoring",
            "Remediation of detected corrosion",
            "Recordkeeping"
        ],
        primary_authority=[
            "40 CFR 146.8",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate monitoring or failure to remediate corrosion.",
        counter_arguments=[
            "Operator may provide monitoring records and evidence of timely remediation.",
            "Operator may propose alternative monitoring methods."
        ],
        resolution_strategy="Review of monitoring records, inspection reports, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Injection Well Network Design and Pressure Interference",
        keywords=[
            "network design", "pressure interference", "well spacing", "plume migration", "hydraulic communication"
        ],
        conclusion_template="Injection well networks must be designed to minimize pressure interference and prevent unintended fluid migration.",
        reasoning_framework=(
            "Well spacing and placement must account for hydraulic communication between wells and formations. "
            "Pressure interference can cause plume migration or exceedance of fracture pressure. "
            "Operators must model pressure fields and demonstrate that network design will not endanger USDWs or reduce operational efficiency."
        ),
        key_factors=[
            "Well spacing",
            "Pressure field modeling",
            "Hydraulic communication",
            "Plume migration risk"
        ],
        primary_authority=[
            "40 CFR 146.6",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege that network design risks USDW protection.",
        counter_arguments=[
            "Operator may provide modeling data and propose operational controls.",
            "Operator may challenge regulatory assumptions."
        ],
        resolution_strategy="Technical review, modeling validation, and regulatory oversight.",
        entity_scope="All UIC injection well networks",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Pressure Interference and Formation Fracture Risk",
        keywords=[
            "pressure interference", "fracture risk", "formation integrity", "pressure monitoring", "plume migration"
        ],
        conclusion_template="Operators must monitor and manage pressure interference to prevent formation fracturing and fluid migration.",
        reasoning_framework=(
            "Pressure interference between wells or formations can increase the risk of exceeding fracture pressure. "
            "Operators must monitor pressure trends, model interference effects, and adjust injection rates as needed. "
            "Failure to manage interference may result in regulatory enforcement or operational shutdown."
        ),
        key_factors=[
            "Pressure monitoring",
            "Interference modeling",
            "Operational adjustments",
            "Regulatory compliance"
        ],
        primary_authority=[
            "40 CFR 146.13(a)",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege that pressure interference is inadequately managed.",
        counter_arguments=[
            "Operator may provide monitoring and modeling data.",
            "Operator may propose operational changes."
        ],
        resolution_strategy="Review of pressure data, modeling reports, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Injection Well Permit Renewal and Compliance",
        keywords=[
            "permit renewal", "compliance", "permit term", "regulatory review", "operational history"
        ],
        conclusion_template="Permit renewal requires demonstration of ongoing compliance with all permit conditions and regulatory requirements.",
        reasoning_framework=(
            "Permit renewal is subject to regulatory review of operational history, monitoring records, and compliance with permit conditions. "
            "Operators must submit renewal applications prior to permit expiration and address any deficiencies identified by regulators. "
            "Failure to demonstrate compliance may result in permit denial or additional conditions."
        ),
        key_factors=[
            "Operational history",
            "Monitoring and reporting",
            "Regulatory review",
            "Deficiency resolution"
        ],
        primary_authority=[
            "40 CFR 144.36",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege non-compliance or operational deficiencies.",
        counter_arguments=[
            "Operator may provide additional documentation or corrective action plans.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Administrative review, public comment, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Injection Well Data Reporting Requirements",
        keywords=[
            "data reporting", "monitoring", "compliance", "recordkeeping", "regulatory submission"
        ],
        conclusion_template="Operators must submit required monitoring and operational data in accordance with permit and regulatory schedules.",
        reasoning_framework=(
            "Data reporting includes injection volumes, pressures, fluid characteristics, and monitoring results. "
            "Reports must be submitted monthly, quarterly, or as specified in the permit. "
            "Failure to report or submission of inaccurate data is a violation subject to enforcement."
        ),
        key_factors=[
            "Reporting frequency",
            "Data accuracy",
            "Record retention",
            "Regulatory submission"
        ],
        primary_authority=[
            "40 CFR 146.13(c)",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege non-compliance or data inaccuracies.",
        counter_arguments=[
            "Operator may provide corrected data or explain reporting discrepancies.",
            "Operator may challenge reporting requirements."
        ],
        resolution_strategy="Review of submitted data, audits, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Epistemic Gap Detection in Injection Well Analysis",
        keywords=[
            "epistemic gap", "uncertainty", "data quality", "knowledge gap", "risk assessment"
        ],
        conclusion_template="Operators and regulators must identify and address epistemic gaps in data and analysis to ensure robust risk management.",
        reasoning_framework=(
            "Epistemic gaps arise from incomplete or uncertain data, model limitations, or lack of site-specific information. "
            "Risk assessments must identify key uncertainties and propose data acquisition or conservative assumptions. "
            "Regulators may require additional studies or monitoring to close knowledge gaps."
        ),
        key_factors=[
            "Data completeness",
            "Model limitations",
            "Uncertainty analysis",
            "Mitigation measures"
        ],
        primary_authority=[
            "EPA UIC Guidance #83",
            "API RP 90"
        ],
        burden_holder="Operator (for site-specific gaps), Regulator (for programmatic gaps)",
        adversary_position="Regulator may allege that epistemic gaps compromise risk management.",
        counter_arguments=[
            "Operator may propose additional data collection or conservative operational limits.",
            "Operator may challenge the significance of identified gaps."
        ],
        resolution_strategy="Iterative risk assessment and regulatory review.",
        entity_scope="All UIC injection wells",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="EPA UIC Guidance #83"
    ),
    DoctrineBlock(
        topic="Drift Detection in Injection Well Compliance",
        keywords=[
            "drift detection", "compliance monitoring", "trend analysis", "anomaly detection", "regulatory response"
        ],
        conclusion_template="Operators must implement drift detection protocols to identify trends or anomalies indicating loss of compliance.",
        reasoning_framework=(
            "Drift detection involves statistical analysis of monitoring data to identify trends or deviations from baseline. "
            "Significant drift may indicate loss of mechanical integrity, changes in injectivity, or risk to USDWs. "
            "Operators must investigate and report detected anomalies, and take corrective action as required."
        ),
        key_factors=[
            "Baseline establishment",
            "Statistical analysis",
            "Anomaly investigation",
            "Corrective action"
        ],
        primary_authority=[
            "EPA UIC Guidance #21",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate drift detection or failure to respond to anomalies.",
        counter_arguments=[
            "Operator may provide analysis protocols and incident response records.",
            "Operator may challenge the significance of detected drift."
        ],
        resolution_strategy="Review of monitoring data, incident reports, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Injection Well Audit Trail and Recordkeeping",
        keywords=[
            "audit trail", "recordkeeping", "compliance", "data integrity", "regulatory inspection"
        ],
        conclusion_template="Operators must maintain a complete audit trail and records of all injection well activities for regulatory inspection.",
        reasoning_framework=(
            "Recordkeeping includes construction records, monitoring data, maintenance logs, and incident reports. "
            "Records must be retained for the duration specified in the permit (typically at least 3-5 years after well closure). "
            "Records must be made available for regulatory inspection upon request. "
            "Failure to maintain adequate records is a violation subject to enforcement."
        ),
        key_factors=[
            "Record retention period",
            "Data integrity",
            "Accessibility for inspection",
            "Comprehensiveness"
        ],
        primary_authority=[
            "40 CFR 146.13(c)",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate recordkeeping or data integrity.",
        counter_arguments=[
            "Operator may provide records or demonstrate data management protocols.",
            "Operator may challenge record retention requirements."
        ],
        resolution_strategy="Regulatory inspection and review of records.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Injection Well Determinism and Reproducibility",
        keywords=[
            "determinism", "reproducibility", "well operations", "data consistency", "regulatory review"
        ],
        conclusion_template="Injection well operations and data analysis must be deterministic and reproducible for regulatory acceptance.",
        reasoning_framework=(
            "Determinism requires that well operations and data analysis produce consistent results under identical conditions. "
            "Reproducibility is demonstrated through repeat testing, independent verification, and transparent documentation. "
            "Regulators may require third-party verification of key analyses or operational outcomes."
        ),
        key_factors=[
            "Operational consistency",
            "Repeat testing",
            "Independent verification",
            "Documentation"
        ],
        primary_authority=[
            "EPA UIC Guidance #83",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege lack of reproducibility or inconsistent data.",
        counter_arguments=[
            "Operator may provide repeat test results and third-party verification.",
            "Operator may challenge regulatory requirements for reproducibility."
        ],
        resolution_strategy="Review of test records, independent analysis, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Injection Well Epistemic Guardrails",
        keywords=[
            "epistemic guardrails", "uncertainty management", "risk mitigation", "regulatory oversight", "conservative assumptions"
        ],
        conclusion_template="Epistemic guardrails must be established to manage uncertainty and ensure protection of USDWs.",
        reasoning_framework=(
            "Epistemic guardrails are conservative operational or design limits set to account for uncertainty in data or models. "
            "Examples include safety factors on injection pressure, additional monitoring, or restricted operational envelopes. "
            "Guardrails are reviewed and adjusted as new data becomes available."
        ),
        key_factors=[
            "Uncertainty identification",
            "Conservative limit setting",
            "Adaptive management",
            "Regulatory review"
        ],
        primary_authority=[
            "EPA UIC Guidance #83",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege that guardrails are insufficient or not properly implemented.",
        counter_arguments=[
            "Operator may provide justification for guardrail selection and adaptive management plans.",
            "Operator may challenge regulatory conservatism."
        ],
        resolution_strategy="Iterative review and adjustment of guardrails based on monitoring data.",
        entity_scope="All UIC injection wells",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="EPA UIC Guidance #83"
    ),
    DoctrineBlock(
        topic="Injection Well Semantic Normalization",
        keywords=[
            "semantic normalization", "data standardization", "terminology", "regulatory reporting", "data integration"
        ],
        conclusion_template="Operators must use standardized terminology and data formats for regulatory reporting and analysis.",
        reasoning_framework=(
            "Semantic normalization ensures that data submitted to regulators is consistent, unambiguous, and interoperable. "
            "Operators must use standardized field names, units, and definitions as specified in regulatory guidance. "
            "Failure to normalize data may result in reporting errors or regulatory delays."
        ),
        key_factors=[
            "Standardized terminology",
            "Data format compliance",
            "Regulatory guidance adherence",
            "Data integration"
        ],
        primary_authority=[
            "EPA UIC Guidance #21",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege non-compliance with data standards.",
        counter_arguments=[
            "Operator may demonstrate adherence to standards or request clarification.",
            "Operator may propose alternative data formats."
        ],
        resolution_strategy="Review of submitted data, regulatory feedback, and data integration testing.",
        entity_scope="All UIC injection wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Financial Responsibility for Injection Wells",
        keywords=[
            "financial responsibility", "bonding", "insurance", "closure costs", "remediation"
        ],
        conclusion_template="Operators must demonstrate financial responsibility for closure, remediation, and post-closure care.",
        reasoning_framework=(
            "Financial responsibility is demonstrated through surety bonds, insurance, trust funds, or other approved mechanisms. "
            "The amount must cover estimated costs of plugging, abandonment, and site remediation. "
            "Proof of financial responsibility must be maintained throughout the well's operational life and post-closure period."
        ),
        key_factors=[
            "Approved financial mechanisms",
            "Cost estimation",
            "Continuous coverage",
            "Regulatory approval"
        ],
        primary_authority=[
            "40 CFR 146.85",
            "EPA UIC Guidance #83"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate financial coverage or lapses in responsibility.",
        counter_arguments=[
            "Operator may provide updated cost estimates or alternative financial mechanisms.",
            "Operator may challenge cost assumptions."
        ],
        resolution_strategy="Review of financial documents, regulatory approval, and periodic reassessment.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #83"
    ),
    DoctrineBlock(
        topic="Public Participation in Injection Well Permitting",
        keywords=[
            "public participation", "public notice", "comment period", "stakeholder engagement", "permit process"
        ],
        conclusion_template="Public notice and comment are required prior to issuance of UIC permits.",
        reasoning_framework=(
            "The UIC permitting process requires public notice of permit applications and an opportunity for public comment. "
            "Stakeholders may submit comments or request public hearings. "
            "Regulators must consider public input in permit decisions and respond to significant comments."
        ),
        key_factors=[
            "Notice publication",
            "Comment period duration",
            "Public hearing requests",
            "Regulatory response"
        ],
        primary_authority=[
            "40 CFR 124.10-12",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Regulator",
        adversary_position="Public or stakeholders may allege inadequate notice or insufficient response to comments.",
        counter_arguments=[
            "Regulator may provide evidence of notice and comment process.",
            "Regulator may address comments in permit decision documents."
        ],
        resolution_strategy="Administrative record review and, if necessary, legal challenge.",
        entity_scope="All UIC injection wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Emergency Response Planning for Injection Wells",
        keywords=[
            "emergency response", "contingency planning", "spill response", "incident management", "regulatory reporting"
        ],
        conclusion_template="Operators must develop and maintain emergency response plans for injection well incidents.",
        reasoning_framework=(
            "Emergency response plans must address potential incidents such as spills, blowouts, or loss of containment. "
            "Plans must include notification procedures, response actions, and coordination with local authorities. "
            "Plans must be reviewed and updated regularly, and personnel must be trained in their implementation."
        ),
        key_factors=[
            "Incident identification",
            "Response procedures",
            "Coordination with authorities",
            "Training and drills"
        ],
        primary_authority=[
            "40 CFR 146.13(d)",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate planning or failure to respond to incidents.",
        counter_arguments=[
            "Operator may provide updated plans and training records.",
            "Operator may demonstrate effective incident response."
        ],
        resolution_strategy="Review of emergency plans, incident reports, and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Wellhead Protection and Security",
        keywords=[
            "wellhead protection", "security", "access control", "vandalism prevention", "site safety"
        ],
        conclusion_template="Operators must implement wellhead protection and security measures to prevent unauthorized access and ensure site safety.",
        reasoning_framework=(
            "Wellhead protection includes fencing, signage, and access controls to prevent unauthorized entry or tampering. "
            "Security measures must comply with regulatory and industry standards. "
            "Incidents of vandalism or unauthorized access must be reported and addressed promptly."
        ),
        key_factors=[
            "Physical security measures",
            "Access control",
            "Incident reporting",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EPA UIC Guidance #21",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate security or failure to report incidents.",
        counter_arguments=[
            "Operator may provide security plans and incident records.",
            "Operator may propose additional security measures."
        ],
        resolution_strategy="Regulatory inspection and review of security protocols.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Surface Spill Prevention and Control",
        keywords=[
            "spill prevention", "surface control", "secondary containment", "spill response", "environmental protection"
        ],
        conclusion_template="Operators must implement spill prevention and control measures to protect surface and groundwater resources.",
        reasoning_framework=(
            "Spill prevention includes secondary containment, regular inspection of tanks and piping, and prompt response to leaks. "
            "Operators must develop and maintain spill prevention, control, and countermeasure (SPCC) plans. "
            "Spills must be reported and remediated in accordance with regulatory requirements."
        ),
        key_factors=[
            "Secondary containment",
            "Inspection frequency",
            "SPCC plan implementation",
            "Spill reporting and remediation"
        ],
        primary_authority=[
            "40 CFR 112",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate spill prevention or delayed response.",
        counter_arguments=[
            "Operator may provide SPCC plans and inspection records.",
            "Operator may demonstrate timely spill response."
        ],
        resolution_strategy="Regulatory inspection and review of SPCC plans.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="40 CFR 112"
    ),
    DoctrineBlock(
        topic="Groundwater Monitoring for Injection Wells",
        keywords=[
            "groundwater monitoring", "monitor wells", "water quality", "USDW protection", "sampling"
        ],
        conclusion_template="Operators must implement groundwater monitoring programs to detect potential impacts to USDWs.",
        reasoning_framework=(
            "Groundwater monitoring includes installation of monitor wells, regular sampling, and analysis for indicator parameters. "
            "Monitoring data must be reported to regulators and used to assess potential impacts. "
            "Detection of contamination requires immediate investigation and corrective action."
        ),
        key_factors=[
            "Monitor well placement",
            "Sampling frequency",
            "Parameter selection",
            "Data reporting"
        ],
        primary_authority=[
            "40 CFR 146.13(d)",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate monitoring or failure to detect impacts.",
        counter_arguments=[
            "Operator may provide monitoring data and propose additional wells.",
            "Operator may challenge sampling protocols."
        ],
        resolution_strategy="Review of monitoring data, site inspection, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Injection Fluid Characterization",
        keywords=[
            "fluid characterization", "chemical analysis", "fluid properties", "regulatory reporting", "compatibility"
        ],
        conclusion_template="Operators must characterize and report the chemical and physical properties of injection fluids.",
        reasoning_framework=(
            "Fluid characterization includes laboratory analysis of chemical composition, pH, specific gravity, and other relevant properties. "
            "Results inform compatibility testing, operational planning, and regulatory reporting. "
            "Changes in fluid composition must be reported and may require permit modification."
        ),
        key_factors=[
            "Laboratory analysis",
            "Reporting requirements",
            "Compatibility assessment",
            "Permit modification triggers"
        ],
        primary_authority=[
            "40 CFR 146.13(b)",
            "API RP 45"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate characterization or unreported changes.",
        counter_arguments=[
            "Operator may provide laboratory data and notification records.",
            "Operator may challenge reporting thresholds."
        ],
        resolution_strategy="Review of laboratory reports and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 45"
    ),
    DoctrineBlock(
        topic="Well Logging and Testing Requirements",
        keywords=[
            "well logging", "testing", "CBL", "temperature logs", "integrity testing"
        ],
        conclusion_template="Operators must conduct and report well logging and testing to verify construction and integrity.",
        reasoning_framework=(
            "Well logging includes cement bond logs, temperature logs, and other diagnostic tests. "
            "Logs must be interpreted by qualified personnel and submitted to regulators. "
            "Testing is required after construction, workovers, and as part of periodic integrity assessments."
        ),
        key_factors=[
            "Log type and frequency",
            "Qualified interpretation",
            "Reporting",
            "Regulatory review"
        ],
        primary_authority=[
            "40 CFR 146.22",
            "API RP 10B-2"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate logging or misinterpretation.",
        counter_arguments=[
            "Operator may provide additional logs or third-party interpretations.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Review of logs, independent analysis, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2"
    ),
    DoctrineBlock(
        topic="Injection Well Workover and Maintenance",
        keywords=[
            "workover", "maintenance", "well repair", "integrity testing", "regulatory notification"
        ],
        conclusion_template="Operators must notify regulators and conduct integrity testing after significant workover or maintenance activities.",
        reasoning_framework=(
            "Workovers include replacement of tubing, packers, or casing repairs. "
            "Operators must notify regulators prior to significant workovers and conduct post-workover integrity testing. "
            "Records of workover activities and test results must be submitted for review."
        ),
        key_factors=[
            "Notification requirements",
            "Integrity testing",
            "Recordkeeping",
            "Regulatory review"
        ],
        primary_authority=[
            "40 CFR 146.8",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate notification or testing.",
        counter_arguments=[
            "Operator may provide workover records and test results.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Review of workover records, test results, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Injection Well Permit Modification",
        keywords=[
            "permit modification", "operational change", "regulatory approval", "notification", "compliance"
        ],
        conclusion_template="Operators must obtain regulatory approval for significant modifications to injection well operations.",
        reasoning_framework=(
            "Permit modifications are required for changes in injection fluid, rate, pressure, or well construction. "
            "Operators must submit modification requests with supporting data and await regulatory approval before implementing changes. "
            "Unauthorized modifications are violations subject to enforcement."
        ),
        key_factors=[
            "Modification triggers",
            "Supporting data",
            "Regulatory approval",
            "Compliance monitoring"
        ],
        primary_authority=[
            "40 CFR 144.39",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege unauthorized modifications or inadequate supporting data.",
        counter_arguments=[
            "Operator may provide additional data or justification.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Administrative review and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Injection Well Closure and Post-Closure Care",
        keywords=[
            "well closure", "post-closure care", "monitoring", "site restoration", "regulatory approval"
        ],
        conclusion_template="Operators must implement closure and post-closure care plans to ensure long-term protection of USDWs.",
        reasoning_framework=(
            "Closure includes plugging, abandonment, and site restoration. "
            "Post-closure care may include groundwater monitoring and site inspections for a specified period. "
            "Operators must submit closure and post-closure plans for regulatory approval and provide financial assurance for required activities."
        ),
        key_factors=[
            "Closure plan approval",
            "Post-closure monitoring",
            "Financial assurance",
            "Regulatory oversight"
        ],
        primary_authority=[
            "40 CFR 146.10",
            "EPA UIC Guidance #20"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate closure or post-closure care.",
        counter_arguments=[
            "Operator may provide closure records and monitoring data.",
            "Operator may challenge duration or scope of post-closure care."
        ],
        resolution_strategy="Review of closure plans, monitoring data, and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #20"
    ),
    DoctrineBlock(
        topic="Injection Well Site Assessment and Baseline Studies",
        keywords=[
            "site assessment", "baseline studies", "geology", "hydrogeology", "environmental impact"
        ],
        conclusion_template="Operators must conduct site assessment and baseline studies prior to injection well permitting.",
        reasoning_framework=(
            "Site assessment includes geologic, hydrogeologic, and environmental studies to characterize site conditions and potential risks. "
            "Baseline studies establish pre-injection conditions for groundwater, surface water, and soil. "
            "Results inform permit application and ongoing monitoring requirements."
        ),
        key_factors=[
            "Geologic and hydrogeologic characterization",
            "Baseline sampling",
            "Environmental impact assessment",
            "Data reporting"
        ],
        primary_authority=[
            "40 CFR 146.13(b)",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate assessment or incomplete data.",
        counter_arguments=[
            "Operator may provide additional studies or data.",
            "Operator may challenge assessment scope."
        ],
        resolution_strategy="Review of assessment reports, data validation, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Regulatory Enforcement and Penalties for Non-Compliance",
        keywords=[
            "enforcement", "penalties", "non-compliance", "fines", "permit revocation"
        ],
        conclusion_template="Regulators may impose penalties, including fines and permit revocation, for non-compliance with UIC requirements.",
        reasoning_framework=(
            "Enforcement actions may include notices of violation, administrative orders, monetary penalties, and permit suspension or revocation. "
            "Penalties are assessed based on severity, duration, and potential for environmental harm. "
            "Operators have the right to appeal enforcement actions through administrative or judicial processes."
        ),
        key_factors=[
            "Severity and duration of violation",
            "Environmental impact",
            "Corrective action",
            "Appeal rights"
        ],
        primary_authority=[
            "40 CFR 144.51",
            "Safe Drinking Water Act"
        ],
        burden_holder="Regulator",
        adversary_position="Operator may challenge enforcement action or penalty severity.",
        counter_arguments=[
            "Operator may provide evidence of compliance or corrective action.",
            "Operator may challenge penalty calculation."
        ],
        resolution_strategy="Administrative review, appeal, and, if necessary, judicial proceedings.",
        entity_scope="All UIC injection wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Safe Drinking Water Act, 42 U.S.C. § 300h"
    ),
    DoctrineBlock(
        topic="Operator Training and Qualification Requirements",
        keywords=[
            "operator training", "qualification", "personnel competency", "regulatory compliance", "safety"
        ],
        conclusion_template="Operators must ensure personnel are trained and qualified to perform injection well operations in compliance with regulations.",
        reasoning_framework=(
            "Training programs must cover regulatory requirements, operational procedures, emergency response, and safety. "
            "Records of training and qualifications must be maintained and available for regulatory inspection. "
            "Unqualified personnel may not perform critical operational or monitoring tasks."
        ),
        key_factors=[
            "Training program content",
            "Qualification verification",
            "Recordkeeping",
            "Regulatory inspection"
        ],
        primary_authority=[
            "EPA UIC Guidance #21",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate training or unqualified personnel.",
        counter_arguments=[
            "Operator may provide training records and certification documentation.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Review of training records, personnel interviews, and regulatory inspection.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Third-Party Review and Independent Verification",
        keywords=[
            "third-party review", "independent verification", "data validation", "regulatory confidence", "quality assurance"
        ],
        conclusion_template="Regulators may require third-party review or independent verification of critical data and analyses.",
        reasoning_framework=(
            "Independent verification enhances regulatory confidence in data quality and analysis. "
            "Third-party reviewers must be qualified and free from conflicts of interest. "
            "Operators must cooperate with third-party reviews and provide all requested data."
        ),
        key_factors=[
            "Reviewer qualifications",
            "Conflict of interest screening",
            "Data accessibility",
            "Regulatory acceptance"
        ],
        primary_authority=[
            "EPA UIC Guidance #83",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate cooperation or challenge reviewer independence.",
        counter_arguments=[
            "Operator may provide reviewer credentials and documentation of cooperation.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Review of third-party reports, regulatory oversight, and, if necessary, additional verification.",
        entity_scope="All UIC injection wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #83"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing and UIC Program Applicability",
        keywords=[
            "hydraulic fracturing", "fracking", "UIC applicability", "Class II wells", "regulatory jurisdiction"
        ],
        conclusion_template="Most hydraulic fracturing activities are exempt from UIC regulation, except when diesel fuels are used as injection fluids.",
        reasoning_framework=(
            "The Energy Policy Act of 2005 amended the Safe Drinking Water Act to exclude most hydraulic fracturing from UIC regulation, "
            "except when diesel fuels are used. "
            "Operators using diesel fuels must obtain a UIC permit and comply with Class II requirements. "
            "States may impose additional requirements for hydraulic fracturing."
        ),
        key_factors=[
            "Injection fluid composition",
            "Regulatory jurisdiction",
            "State-specific requirements",
            "Permit triggers"
        ],
        primary_authority=[
            "Safe Drinking Water Act, § 1421(d)(1)(B)",
            "EPA UIC Guidance #84"
        ],
        burden_holder="Operator (if using diesel fuels)",
        adversary_position="Regulator may allege unauthorized use of regulated fluids.",
        counter_arguments=[
            "Operator may provide fluid composition data and regulatory correspondence.",
            "Operator may challenge applicability of UIC requirements."
        ],
        resolution_strategy="Review of fluid records, regulatory guidance, and, if necessary, legal interpretation.",
        entity_scope="Hydraulic fracturing operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #84"
    ),
    DoctrineBlock(
        topic="Class II Brine Disposal Well Requirements",
        keywords=[
            "brine disposal", "Class II", "disposal well", "fluid management", "regulatory compliance"
        ],
        conclusion_template="Class II brine disposal wells must comply with all UIC construction, monitoring, and reporting requirements.",
        reasoning_framework=(
            "Brine disposal wells inject produced water and other fluids associated with oil and gas production. "
            "Operators must demonstrate well integrity, monitor injection volumes and pressures, and report data as required. "
            "Disposal wells are subject to periodic mechanical integrity testing and area of review reassessment."
        ),
        key_factors=[
            "Well integrity",
            "Monitoring and reporting",
            "AOR reassessment",
            "Permit compliance"
        ],
        primary_authority=[
            "40 CFR 146.5(b)",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege non-compliance or operational deficiencies.",
        counter_arguments=[
            "Operator may provide monitoring data and integrity test records.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Review of monitoring data, test records, and regulatory oversight.",
        entity_scope="Class II brine disposal wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Injection Well Permit Transfer and Successor Liability",
        keywords=[
            "permit transfer", "successor liability", "ownership change", "regulatory approval", "ongoing compliance"
        ],
        conclusion_template="Permit transfers require regulatory approval and successors assume all ongoing compliance obligations.",
        reasoning_framework=(
            "Permit transfers occur when ownership or operational control of an injection well changes. "
            "Regulators must approve transfers and verify that the successor can meet all permit and regulatory requirements. "
            "Successors assume liability for ongoing compliance, closure, and remediation."
        ),
        key_factors=[
            "Transfer approval process",
            "Successor qualifications",
            "Liability assumption",
            "Regulatory notification"
        ],
        primary_authority=[
            "40 CFR 144.38",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Successor operator",
        adversary_position="Regulator may allege inadequate qualifications or failure to assume liability.",
        counter_arguments=[
            "Successor may provide evidence of qualifications and financial responsibility.",
            "Successor may challenge transfer conditions."
        ],
        resolution_strategy="Administrative review and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Well Location and Setback Requirements",
        keywords=[
            "well location", "setback", "distance to USDW", "property boundaries", "regulatory compliance"
        ],
        conclusion_template="Injection wells must be located in compliance with setback requirements from USDWs, property lines, and sensitive receptors.",
        reasoning_framework=(
            "Setback requirements are established to protect USDWs, property boundaries, and sensitive environmental or community receptors. "
            "Operators must demonstrate compliance with federal, state, and local setback standards as part of the permit application. "
            "Non-compliance may result in permit denial or required relocation."
        ),
        key_factors=[
            "Setback distance standards",
            "Site survey accuracy",
            "Regulatory approval",
            "Permit application documentation"
        ],
        primary_authority=[
            "40 CFR 146.12",
            "State and local regulations"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege non-compliance with setback requirements.",
        counter_arguments=[
            "Operator may provide site surveys and regulatory correspondence.",
            "Operator may challenge setback interpretations."
        ],
        resolution_strategy="Review of site surveys, permit applications, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="40 CFR 146.12"
    ),
    DoctrineBlock(
        topic="Injection Well Permit Variance and Alternative Compliance",
        keywords=[
            "permit variance", "alternative compliance", "regulatory flexibility", "site-specific conditions", "approval process"
        ],
        conclusion_template="Operators may request permit variances or alternative compliance based on site-specific conditions, subject to regulatory approval.",
        reasoning_framework=(
            "Permit variances allow for alternative methods or standards where site-specific conditions justify deviation from standard requirements. "
            "Requests must be supported by technical data and demonstrate equivalent or greater protection of USDWs. "
            "Regulators review and approve or deny variance requests based on risk assessment and public input."
        ),
        key_factors=[
            "Technical justification",
            "Equivalent protection demonstration",
            "Regulatory review",
            "Public input"
        ],
        primary_authority=[
            "40 CFR 146.4",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may deny variance or require additional controls.",
        counter_arguments=[
            "Operator may provide additional data or propose enhanced controls.",
            "Operator may challenge regulatory findings."
        ],
        resolution_strategy="Technical review, public comment, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
    ),
    DoctrineBlock(
        topic="Injection Well Notification and Reporting of Incidents",
        keywords=[
            "incident reporting", "notification", "regulatory reporting", "compliance", "spill response"
        ],
        conclusion_template="Operators must promptly notify regulators of reportable incidents and submit required follow-up reports.",
        reasoning_framework=(
            "Reportable incidents include spills, loss of mechanical integrity, unauthorized fluid migration, or other events with potential environmental impact. "
            "Operators must notify regulators within specified timeframes and submit detailed incident reports. "
            "Failure to report is a violation subject to enforcement."
        ),
        key_factors=[
            "Incident identification",
            "Notification timeframe",
            "Report content",
            "Regulatory follow-up"
        ],
        primary_authority=[
            "40 CFR 146.13(d)",
            "EPA UIC Guidance #21"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege failure to report or inadequate reporting.",
        counter_arguments=[
            "Operator may provide incident records and notification documentation.",
            "Operator may challenge reporting thresholds."
        ],
        resolution_strategy="Review of incident records, regulatory correspondence, and, if necessary, enforcement action.",
        entity_scope="All UIC injection wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #21"
    ),
    DoctrineBlock(
        topic="Injection Well Integrity Management Programs",
        keywords=[
            "integrity management", "well integrity", "risk assessment", "monitoring", "preventive maintenance"
        ],
        conclusion_template="Operators must implement integrity management programs to proactively identify and mitigate risks to well integrity.",
        reasoning_framework=(
            "Integrity management programs include risk assessment, regular monitoring, preventive maintenance, and timely remediation of detected issues. "
            "Programs must be documented, updated based on monitoring results, and subject to regulatory review. "
            "Failure to implement effective integrity management may result in enforcement action."
        ),
        key_factors=[
            "Risk assessment",
            "Monitoring protocols",
            "Preventive maintenance",
            "Program documentation"
        ],
        primary_authority=[
            "EPA UIC Guidance #21",
            "API RP 90"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may allege inadequate integrity management or failure to address risks.",
        counter_arguments=[
            "Operator may provide program documentation and monitoring data.",
            "Operator may propose program improvements."
        ],
        resolution_strategy="Review of program documentation, monitoring data, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Injection Well Permit Suspension and Reinstatement",
        keywords=[
            "permit suspension", "reinstatement", "regulatory enforcement", "compliance restoration", "operational shutdown"
        ],
        conclusion_template="Regulators may suspend injection well permits for non-compliance; reinstatement requires demonstration of compliance restoration.",
        reasoning_framework=(
            "Permit suspension may occur due to violations, loss of mechanical integrity, or risk to USDWs. "
            "Operators must cease injection and implement corrective actions. "
            "Reinstatement requires demonstration of compliance and regulatory approval."
        ),
        key_factors=[
            "Violation or risk identification",
            "Corrective action implementation",
            "Compliance demonstration",
            "Regulatory approval"
        ],
        primary_authority=[
            "40 CFR 144.51",
            "EPA UIC Guidance #34"
        ],
        burden_holder="Operator",
        adversary_position="Regulator may deny reinstatement if compliance is not demonstrated.",
        counter_arguments=[
            "Operator may provide corrective action documentation and compliance data.",
            "Operator may challenge suspension basis."
        ],
        resolution_strategy="Review of corrective action records, compliance demonstration, and regulatory oversight.",
        entity_scope="All UIC injection wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA UIC Guidance #34"
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]