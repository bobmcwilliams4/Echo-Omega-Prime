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
        topic="SIL Determination Using Risk Graph Method",
        keywords=["SIL", "Risk Graph", "IEC 61511", "Risk Reduction", "SIF", "Safety Integrity Level"],
        conclusion_template="The required SIL for the SIF is determined by applying the risk graph method per IEC 61511, considering consequence, frequency, probability of avoidance, and likelihood of unwanted occurrence.",
        reasoning_framework=(
            "1. Identify the hazardous event and associated SIF.\n"
            "2. Assign values for consequence severity, frequency and exposure, probability of avoiding the hazard, and likelihood of unwanted occurrence.\n"
            "3. Use the risk graph matrix (IEC 61511 Annex F) to map these factors to a required SIL (1-4).\n"
            "4. Document the rationale for each input value and the resulting SIL assignment.\n"
            "5. Validate the SIL assignment with a multi-disciplinary team and ensure traceability to the hazard analysis.\n"
            "6. Review for alignment with corporate and regulatory risk tolerability criteria.\n"
            "7. Update the risk graph if process or operational changes occur.\n"
            "8. Ensure the SIL determination is auditable and justified in the safety requirements specification."
        ),
        key_factors=[
            "Severity of consequence",
            "Frequency and exposure",
            "Probability of avoiding hazard",
            "Likelihood of unwanted occurrence",
            "Risk tolerability criteria"
        ],
        primary_authority=["IEC 61511", "ISA TR84.00.02", "Company Risk Policy"],
        burden_holder="SIS Design Authority",
        adversary_position="SIL is over- or under-specified due to subjective input values or lack of consensus.",
        counter_arguments=[
            "Inputs are based on best available data and expert judgement.",
            "Multi-disciplinary review ensures balanced assessment.",
            "Conservative approach taken where uncertainty exists."
        ],
        resolution_strategy="Facilitate consensus through risk workshops and document all assumptions; escalate unresolved disputes to the Functional Safety Manager.",
        entity_scope="All SIFs within the SIS lifecycle",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 9.2"
    ),
    DoctrineBlock(
        topic="Safety PLC Architecture: 1oo1 vs 1oo2 vs 2oo3 Selection",
        keywords=["Safety PLC", "1oo1", "1oo2", "2oo3", "Architecture", "Redundancy", "Fault Tolerance"],
        conclusion_template="The selection of 1oo1, 1oo2, or 2oo3 architecture for the Safety PLC is based on required SIL, availability targets, and tolerance to common cause failure.",
        reasoning_framework=(
            "1. Determine the required SIL for the SIF(s) to be implemented.\n"
            "2. Evaluate the failure rates and diagnostic coverage of candidate PLC hardware.\n"
            "3. Assess the risk of common cause failure and the need for redundancy.\n"
            "4. Compare architectures:\n"
            "   - 1oo1: Simple, cost-effective, but single point of failure.\n"
            "   - 1oo2: Redundant, higher availability, can tolerate one failure.\n"
            "   - 2oo3: Triple modular redundancy, highest fault tolerance, complex.\n"
            "5. Consider spurious trip rates and maintenance implications.\n"
            "6. Select architecture that meets SIL and availability requirements with justified cost.\n"
            "7. Document rationale and ensure compliance with IEC 61508/61511 hardware fault tolerance tables."
        ),
        key_factors=[
            "Required SIL",
            "Hardware fault tolerance",
            "Diagnostic coverage",
            "Common cause failure risk",
            "Cost and complexity"
        ],
        primary_authority=["IEC 61508", "IEC 61511", "Vendor Safety Manuals"],
        burden_holder="SIS Hardware Engineer",
        adversary_position="Higher redundancy increases cost and complexity without proportional risk reduction.",
        counter_arguments=[
            "Redundancy justified for high SIL or critical SIFs.",
            "Cost-benefit analysis supports selected architecture.",
            "Single channel may be sufficient for low SIL with proven hardware."
        ],
        resolution_strategy="Perform quantitative reliability analysis and review with stakeholders; escalate to Safety Review Board if unresolved.",
        entity_scope="SIS hardware design and implementation",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61508:2010, Part 2, Table 3"
    ),
    DoctrineBlock(
        topic="ESD System Cause and Effect Matrix Design",
        keywords=["ESD", "Emergency Shutdown", "Cause and Effect Matrix", "Logic", "Trip", "SIS"],
        conclusion_template="The ESD system cause and effect matrix is structured to ensure all credible causes are mapped to appropriate effects, supporting safe process shutdown.",
        reasoning_framework=(
            "1. Identify all credible initiating events (causes) requiring ESD action.\n"
            "2. Define the required process responses (effects) for each cause.\n"
            "3. Develop a matrix mapping each cause to its effects, ensuring clarity and completeness.\n"
            "4. Validate the matrix with process, operations, and safety representatives.\n"
            "5. Ensure matrix logic is implementable in the SIS logic solver.\n"
            "6. Review for potential conflicts, overlaps, or gaps in cause/effect assignments.\n"
            "7. Maintain traceability to hazard analysis and SRS.\n"
            "8. Update the matrix as process or safety requirements evolve."
        ),
        key_factors=[
            "Completeness of causes and effects",
            "Traceability to hazard analysis",
            "Clarity of logic",
            "Stakeholder validation"
        ],
        primary_authority=["IEC 61511", "Company ESD Philosophy", "Process Hazard Analysis"],
        burden_holder="Process Safety Engineer",
        adversary_position="Matrix is overly complex or omits critical scenarios.",
        counter_arguments=[
            "Matrix reviewed by multi-disciplinary team.",
            "All credible scenarios addressed.",
            "Simplification performed where possible without loss of coverage."
        ],
        resolution_strategy="Iterative review and validation; unresolved issues escalated to Process Safety Committee.",
        entity_scope="All ESD systems within SIS scope",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 10.3"
    ),
    DoctrineBlock(
        topic="Fire and Gas Detection System Design: Detector Types and Coverage",
        keywords=["Fire and Gas", "Detector", "Coverage", "Point", "Open Path", "Flame", "Gas", "Mapping"],
        conclusion_template="Fire and gas detection system design selects detector types and placement to achieve required coverage per risk assessment and industry standards.",
        reasoning_framework=(
            "1. Perform a fire and gas hazard assessment to identify target areas and release scenarios.\n"
            "2. Select appropriate detector types (point gas, open path, flame, smoke) based on hazard characteristics.\n"
            "3. Use coverage mapping tools to optimize detector placement and quantify coverage percentage.\n"
            "4. Validate that coverage meets or exceeds company and industry targets (e.g., 80% for gas, 90% for fire).\n"
            "5. Consider environmental factors, maintenance access, and potential obstructions.\n"
            "6. Document the rationale for detector selection and placement.\n"
            "7. Review design with operations and safety personnel.\n"
            "8. Update mapping as process or layout changes."
        ),
        key_factors=[
            "Hazard assessment results",
            "Detector technology suitability",
            "Coverage percentage",
            "Environmental and operational constraints"
        ],
        primary_authority=["ISA TR84.00.07", "NFPA 72", "Company Fire and Gas Philosophy"],
        burden_holder="Fire and Gas System Designer",
        adversary_position="Detector layout is insufficient or excessive, leading to risk or unnecessary cost.",
        counter_arguments=[
            "Coverage mapping demonstrates compliance.",
            "Detector selection based on risk and environment.",
            "Design reviewed by stakeholders."
        ],
        resolution_strategy="Independent review and coverage validation; escalate to Safety Manager if unresolved.",
        entity_scope="All fire and gas detection systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISA TR84.00.07-2018"
    ),
    DoctrineBlock(
        topic="Pressure Safety Valve Sizing per API 520/521",
        keywords=["PSV", "Pressure Relief", "Sizing", "API 520", "API 521", "Relief Scenario"],
        conclusion_template="PSV sizing is performed per API 520/521, considering all credible relief scenarios and ensuring adequate relieving capacity.",
        reasoning_framework=(
            "1. Identify all credible overpressure scenarios for the protected equipment.\n"
            "2. Calculate required relief rates for each scenario per API 521.\n"
            "3. Select the governing scenario (highest required rate).\n"
            "4. Size the PSV orifice using API 520 equations, accounting for backpressure, fluid properties, and set pressure.\n"
            "5. Ensure selected PSV can relieve the governing scenario without exceeding allowable accumulation.\n"
            "6. Document all assumptions, calculations, and scenario justifications.\n"
            "7. Review sizing with process and mechanical engineering.\n"
            "8. Update sizing if process conditions change."
        ),
        key_factors=[
            "Credible relief scenarios",
            "Relief rate calculation",
            "Equipment design pressure",
            "Fluid properties"
        ],
        primary_authority=["API 520", "API 521", "ASME Section VIII"],
        burden_holder="Process Engineer",
        adversary_position="PSV is undersized or oversized, risking equipment or causing operational issues.",
        counter_arguments=[
            "All scenarios evaluated per API standards.",
            "Sizing calculations independently checked.",
            "Conservative assumptions used where uncertainty exists."
        ],
        resolution_strategy="Peer review and third-party verification for critical services.",
        entity_scope="All pressure relief devices",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API 520/521, Latest Edition"
    ),
    DoctrineBlock(
        topic="HIPPS (High Integrity Pressure Protection System) as PSV Alternative",
        keywords=["HIPPS", "PSV", "Pressure Protection", "SIL", "IEC 61511", "API 521"],
        conclusion_template="HIPPS may be used as an alternative to PSV where justified by risk reduction requirements and compliance with IEC 61511 and API 521.",
        reasoning_framework=(
            "1. Identify scenarios where conventional PSV protection is impractical or insufficient (e.g., environmental, process constraints).\n"
            "2. Perform risk assessment to justify HIPPS application and required SIL.\n"
            "3. Design HIPPS per IEC 61511, ensuring hardware fault tolerance, independence, and reliability.\n"
            "4. Validate that HIPPS achieves risk reduction equivalent to or better than PSV per API 521.\n"
            "5. Ensure regulatory acceptance and document all design and validation steps.\n"
            "6. Implement robust proof testing and maintenance procedures.\n"
            "7. Maintain traceability to hazard analysis and SRS.\n"
            "8. Update HIPPS design as process or regulatory requirements evolve."
        ),
        key_factors=[
            "Risk reduction requirements",
            "SIL achievement",
            "Regulatory acceptance",
            "Proof testing"
        ],
        primary_authority=["IEC 61511", "API 521", "Company Pressure Protection Philosophy"],
        burden_holder="Process Safety Engineer",
        adversary_position="HIPPS may not provide equivalent protection or may not be accepted by regulators.",
        counter_arguments=[
            "HIPPS designed and validated per IEC 61511.",
            "Risk reduction demonstrated quantitatively.",
            "Regulatory engagement performed early in design."
        ],
        resolution_strategy="Obtain regulatory approval and third-party validation; escalate to Safety Review Board if unresolved.",
        entity_scope="All HIPPS applications",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 521, Section 6.2; IEC 61511"
    ),
    DoctrineBlock(
        topic="Proof Test Intervals and PFD Calculation for SIL Verification",
        keywords=["Proof Test", "PFD", "SIL Verification", "Test Interval", "IEC 61511", "Reliability"],
        conclusion_template="Proof test intervals and PFDavg are calculated to ensure SIFs meet required SIL targets per IEC 61511.",
        reasoning_framework=(
            "1. Identify all SIF components and their failure rates (λ) and diagnostic coverage.\n"
            "2. Calculate PFDavg using IEC 61511 formulas, incorporating proof test interval (T), test coverage, and repair times.\n"
            "3. Select proof test interval that ensures PFDavg is within the SIL target range.\n"
            "4. Document all assumptions, failure data sources, and calculation methods.\n"
            "5. Review proof test procedures for completeness and effectiveness.\n"
            "6. Validate calculations with reliability engineering and functional safety personnel.\n"
            "7. Update intervals and calculations as failure data or operating experience evolves."
        ),
        key_factors=[
            "Component failure rates",
            "Test coverage",
            "Proof test interval",
            "Repair time"
        ],
        primary_authority=["IEC 61511", "ISA TR84.00.02", "Company Proof Test Philosophy"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Test intervals are too long, risking undetected failures, or too short, causing operational burden.",
        counter_arguments=[
            "Intervals selected based on quantitative analysis.",
            "Proof test effectiveness validated.",
            "Intervals reviewed periodically with operating experience."
        ],
        resolution_strategy="Independent review and periodic reassessment; escalate to Functional Safety Manager if unresolved.",
        entity_scope="All SIFs requiring SIL verification",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.9"
    ),
    DoctrineBlock(
        topic="Functional Safety Management and Lifecycle per IEC 61511",
        keywords=["Functional Safety", "Management", "Lifecycle", "IEC 61511", "SIS", "SIF"],
        conclusion_template="Functional safety is managed throughout the SIS lifecycle per IEC 61511, with defined roles, responsibilities, and verification activities.",
        reasoning_framework=(
            "1. Define the SIS lifecycle phases per IEC 61511 (concept, design, implementation, operation, decommissioning).\n"
            "2. Assign clear roles and responsibilities for each phase, including independent verification.\n"
            "3. Implement functional safety management plan, including competence, documentation, and change management.\n"
            "4. Ensure all lifecycle activities are traceable and auditable.\n"
            "5. Perform periodic functional safety assessments to confirm compliance.\n"
            "6. Maintain records of all decisions, deviations, and verification results.\n"
            "7. Update management plan as organization or regulatory requirements evolve."
        ),
        key_factors=[
            "Defined lifecycle phases",
            "Competence and independence",
            "Documentation and traceability",
            "Verification and assessment"
        ],
        primary_authority=["IEC 61511", "Company Functional Safety Policy"],
        burden_holder="Functional Safety Manager",
        adversary_position="Lifecycle activities are incomplete or lack independence, risking non-compliance.",
        counter_arguments=[
            "Lifecycle activities mapped to IEC 61511.",
            "Independent verification documented.",
            "Periodic assessments performed."
        ],
        resolution_strategy="Functional safety audits and corrective action tracking.",
        entity_scope="All SIS and SIFs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 5"
    ),
    DoctrineBlock(
        topic="SIF Validation Testing and Factory/Site Acceptance Testing (FAT/SAT)",
        keywords=["SIF", "Validation", "FAT", "SAT", "Testing", "IEC 61511"],
        conclusion_template="SIF validation is performed through documented FAT and SAT procedures, ensuring all safety requirements are met before commissioning.",
        reasoning_framework=(
            "1. Develop FAT and SAT procedures based on the safety requirements specification (SRS).\n"
            "2. Test all SIF logic, hardware, and interfaces for correct operation and fail-safe behavior.\n"
            "3. Simulate all credible process conditions and fault scenarios.\n"
            "4. Document all test results, deviations, and corrective actions.\n"
            "5. Obtain sign-off from functional safety, operations, and engineering representatives.\n"
            "6. Update SRS and test procedures as design changes occur."
        ),
        key_factors=[
            "Test coverage",
            "Traceability to SRS",
            "Simulation of fault scenarios",
            "Stakeholder sign-off"
        ],
        primary_authority=["IEC 61511", "Company FAT/SAT Procedures"],
        burden_holder="SIS Commissioning Engineer",
        adversary_position="Testing is incomplete or not representative of real process conditions.",
        counter_arguments=[
            "Test procedures reviewed and approved.",
            "All credible scenarios simulated.",
            "Testing witnessed by independent party."
        ],
        resolution_strategy="Independent validation and sign-off; escalate to Project Manager if unresolved.",
        entity_scope="All SIFs prior to commissioning",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 14"
    ),
    DoctrineBlock(
        topic="Common Cause Failure Analysis and Beta Factor Estimation",
        keywords=["Common Cause Failure", "Beta Factor", "CCF", "SIL", "Reliability", "IEC 61508"],
        conclusion_template="Common cause failure analysis is performed using beta factor estimation to ensure SIS redundancy provides real risk reduction.",
        reasoning_framework=(
            "1. Identify redundant SIS components subject to common cause failure.\n"
            "2. Estimate beta factor (β) using industry data, OREDA, or IEC 61508 guidelines.\n"
            "3. Calculate impact of CCF on overall system PFD and SIL achievement.\n"
            "4. Implement design and procedural measures to minimize beta (physical separation, diversity, etc.).\n"
            "5. Document all assumptions and data sources.\n"
            "6. Review analysis with reliability and functional safety experts.\n"
            "7. Update CCF analysis as design or operating experience evolves."
        ),
        key_factors=[
            "Redundancy architecture",
            "Physical and functional separation",
            "Industry beta factor data",
            "Design diversity"
        ],
        primary_authority=["IEC 61508", "OREDA", "Company Reliability Guidelines"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Beta factor underestimated, overestimating risk reduction.",
        counter_arguments=[
            "Conservative beta factors used.",
            "Industry data and expert judgement applied.",
            "Design measures implemented to minimize CCF."
        ],
        resolution_strategy="Independent review and periodic reassessment.",
        entity_scope="All redundant SIS components",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61508:2010, Part 6, Annex D"
    ),
    # 30+ additional DoctrineBlock instances follow with real domain content
    DoctrineBlock(
        topic="Separation and Independence of SIS from BPCS",
        keywords=["SIS", "BPCS", "Separation", "Independence", "IEC 61511", "Common Cause"],
        conclusion_template="The SIS must be physically and functionally independent from the BPCS to prevent common cause failures, as required by IEC 61511.",
        reasoning_framework=(
            "1. Review system architecture to identify shared components between SIS and BPCS.\n"
            "2. Ensure SIS has separate power supplies, communication networks, and I/O modules where feasible.\n"
            "3. Implement physical separation in cabinets and wiring.\n"
            "4. Validate independence through design reviews and testing.\n"
            "5. Document all measures and justify any exceptions.\n"
            "6. Update separation strategy as system changes."
        ),
        key_factors=[
            "Physical separation",
            "Functional independence",
            "Shared components",
            "Power and communication segregation"
        ],
        primary_authority=["IEC 61511", "Company SIS Design Standard"],
        burden_holder="SIS System Integrator",
        adversary_position="Shared components may introduce common cause failure risk.",
        counter_arguments=[
            "Separation measures exceed minimum requirements.",
            "Exceptions justified and risk assessed.",
            "Design independently reviewed."
        ],
        resolution_strategy="Design review and periodic audit.",
        entity_scope="All SIS and BPCS interfaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.2"
    ),
    DoctrineBlock(
        topic="SIS Software Change Management",
        keywords=["SIS", "Software", "Change Management", "Configuration", "IEC 61511"],
        conclusion_template="All SIS software changes must follow formal change management procedures to ensure traceability, validation, and risk control.",
        reasoning_framework=(
            "1. Document all requested changes, including rationale and risk assessment.\n"
            "2. Review and approve changes by authorized personnel.\n"
            "3. Test changes in a controlled environment before deployment.\n"
            "4. Update all affected documentation and configuration records.\n"
            "5. Maintain audit trail of all changes and approvals.\n"
            "6. Periodically review change management effectiveness."
        ),
        key_factors=[
            "Change documentation",
            "Approval process",
            "Testing and validation",
            "Audit trail"
        ],
        primary_authority=["IEC 61511", "Company SIS Change Management Policy"],
        burden_holder="SIS Software Engineer",
        adversary_position="Uncontrolled changes may compromise SIS integrity.",
        counter_arguments=[
            "Formal procedures enforced.",
            "All changes independently reviewed.",
            "Audit trail maintained."
        ],
        resolution_strategy="Regular audits and corrective actions.",
        entity_scope="All SIS software and configuration",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 17"
    ),
    DoctrineBlock(
        topic="SIS Cybersecurity Requirements",
        keywords=["SIS", "Cybersecurity", "IEC 62443", "IEC 61511", "Access Control"],
        conclusion_template="SIS must meet cybersecurity requirements per IEC 62443 and IEC 61511 to prevent unauthorized access and manipulation.",
        reasoning_framework=(
            "1. Perform cybersecurity risk assessment for SIS.\n"
            "2. Implement access controls, network segmentation, and intrusion detection.\n"
            "3. Apply security patches and updates per vendor recommendations.\n"
            "4. Monitor SIS for suspicious activity and respond to incidents.\n"
            "5. Document all cybersecurity measures and review regularly."
        ),
        key_factors=[
            "Access control",
            "Network segmentation",
            "Patch management",
            "Incident response"
        ],
        primary_authority=["IEC 62443", "IEC 61511", "Company Cybersecurity Policy"],
        burden_holder="SIS Cybersecurity Officer",
        adversary_position="Cyber threats may compromise SIS availability or integrity.",
        counter_arguments=[
            "Defense-in-depth strategy implemented.",
            "Regular vulnerability assessments performed.",
            "Incident response plan in place."
        ],
        resolution_strategy="Continuous monitoring and periodic audits.",
        entity_scope="All SIS components and networks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 62443-2-1"
    ),
    DoctrineBlock(
        topic="SIS Proof Test Coverage and Effectiveness",
        keywords=["SIS", "Proof Test", "Coverage", "Effectiveness", "SIL"],
        conclusion_template="Proof tests must be designed to detect all dangerous undetected failures relevant to the SIF's SIL target.",
        reasoning_framework=(
            "1. Analyze SIF architecture to identify all failure modes.\n"
            "2. Develop proof test procedures that detect each dangerous undetected failure.\n"
            "3. Validate proof test coverage through test records and failure data.\n"
            "4. Review procedures for completeness and practicality.\n"
            "5. Update proof test as new failure modes are identified."
        ),
        key_factors=[
            "Failure mode analysis",
            "Test procedure completeness",
            "Test records",
            "SIL requirements"
        ],
        primary_authority=["IEC 61511", "ISA TR84.00.02"],
        burden_holder="SIS Maintenance Engineer",
        adversary_position="Proof test does not detect all relevant failures.",
        counter_arguments=[
            "Procedures reviewed by reliability experts.",
            "Test coverage validated with field data.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Periodic review and update of proof test procedures.",
        entity_scope="All SIFs subject to proof testing",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS Maintenance and Bypass Management",
        keywords=["SIS", "Maintenance", "Bypass", "Override", "SIL", "IEC 61511"],
        conclusion_template="SIS maintenance and bypasses must be managed to minimize risk and maintain compliance with SIL requirements.",
        reasoning_framework=(
            "1. Document all planned SIS maintenance and required bypasses.\n"
            "2. Assess risk of bypass and implement compensating measures.\n"
            "3. Limit bypass duration and monitor status.\n"
            "4. Obtain approval from authorized personnel before applying bypass.\n"
            "5. Restore SIS to normal operation as soon as possible.\n"
            "6. Record all bypass activity and review periodically."
        ),
        key_factors=[
            "Bypass documentation",
            "Risk assessment",
            "Compensating measures",
            "Approval and monitoring"
        ],
        primary_authority=["IEC 61511", "Company Bypass Policy"],
        burden_holder="SIS Maintenance Supervisor",
        adversary_position="Bypasses increase risk of undetected failures or unsafe operation.",
        counter_arguments=[
            "Bypass use minimized and controlled.",
            "Compensating measures implemented.",
            "Bypass activity reviewed regularly."
        ],
        resolution_strategy="Bypass log review and functional safety audit.",
        entity_scope="All SIS maintenance and bypass activities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.7"
    ),
    DoctrineBlock(
        topic="SIS Competence Management",
        keywords=["SIS", "Competence", "Training", "IEC 61511", "Personnel"],
        conclusion_template="All personnel involved in SIS lifecycle activities must be competent and trained per IEC 61511 requirements.",
        reasoning_framework=(
            "1. Define competence requirements for each SIS lifecycle role.\n"
            "2. Assess personnel qualifications and provide training as needed.\n"
            "3. Maintain records of competence and training.\n"
            "4. Review competence periodically and update as necessary."
        ),
        key_factors=[
            "Role-based competence requirements",
            "Training records",
            "Periodic competence review",
            "Regulatory compliance"
        ],
        primary_authority=["IEC 61511", "Company Training Policy"],
        burden_holder="Functional Safety Manager",
        adversary_position="Incompetent personnel may compromise SIS integrity.",
        counter_arguments=[
            "Competence requirements defined and enforced.",
            "Training provided and documented.",
            "Competence reviewed regularly."
        ],
        resolution_strategy="Competence audits and corrective actions.",
        entity_scope="All SIS lifecycle personnel",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 5.2"
    ),
    DoctrineBlock(
        topic="SIS Documentation and Record Keeping",
        keywords=["SIS", "Documentation", "Record Keeping", "IEC 61511", "Traceability"],
        conclusion_template="All SIS lifecycle activities must be documented and records maintained to ensure traceability and compliance.",
        reasoning_framework=(
            "1. Identify all SIS documents required by IEC 61511 and company policy.\n"
            "2. Maintain records of hazard analysis, SIL determination, design, verification, testing, and operation.\n"
            "3. Ensure documents are controlled, accessible, and up to date.\n"
            "4. Periodically review documentation for completeness and accuracy."
        ),
        key_factors=[
            "Document control",
            "Traceability",
            "Accessibility",
            "Completeness"
        ],
        primary_authority=["IEC 61511", "Company Document Control Policy"],
        burden_holder="SIS Project Manager",
        adversary_position="Incomplete or outdated documentation may hinder compliance.",
        counter_arguments=[
            "Document control system in place.",
            "Records reviewed and updated regularly.",
            "Documentation requirements mapped to standards."
        ],
        resolution_strategy="Periodic documentation audits.",
        entity_scope="All SIS lifecycle activities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 5.3"
    ),
    DoctrineBlock(
        topic="SIS Periodic Functional Safety Assessment",
        keywords=["SIS", "Functional Safety Assessment", "IEC 61511", "Audit", "Verification"],
        conclusion_template="Periodic functional safety assessments are required to verify SIS compliance with IEC 61511 and company policy.",
        reasoning_framework=(
            "1. Schedule functional safety assessments at defined SIS lifecycle phases.\n"
            "2. Assign independent, competent assessors.\n"
            "3. Review SIS design, operation, and maintenance records for compliance.\n"
            "4. Document findings and track corrective actions.\n"
            "5. Update assessment schedule as system changes."
        ),
        key_factors=[
            "Assessment schedule",
            "Assessor independence",
            "Corrective action tracking",
            "Documentation review"
        ],
        primary_authority=["IEC 61511", "Company Audit Policy"],
        burden_holder="Functional Safety Manager",
        adversary_position="Assessments may be superficial or lack independence.",
        counter_arguments=[
            "Assessors are independent and competent.",
            "Assessment findings tracked to closure.",
            "Assessment scope covers all SIS lifecycle activities."
        ],
        resolution_strategy="Periodic review of assessment process.",
        entity_scope="All SIS installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 5.2.6"
    ),
    DoctrineBlock(
        topic="SIS Demand Rate Classification",
        keywords=["SIS", "Demand Rate", "Low Demand", "High Demand", "IEC 61511"],
        conclusion_template="SIS demand rate classification (low, high, continuous) determines applicable SIL verification methods per IEC 61511.",
        reasoning_framework=(
            "1. Analyze process to determine SIS demand frequency.\n"
            "2. Classify demand as low (<1/yr), high (≥1/yr), or continuous.\n"
            "3. Apply appropriate SIL verification method (PFDavg for low demand, PFH for high/continuous).\n"
            "4. Document classification and rationale."
        ),
        key_factors=[
            "Process demand frequency",
            "SIL verification method",
            "Documentation",
            "IEC 61511 definitions"
        ],
        primary_authority=["IEC 61511", "ISA TR84.00.02"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Incorrect classification may lead to inappropriate SIL verification.",
        counter_arguments=[
            "Classification based on process data.",
            "Reviewed by process and safety experts.",
            "Documented and periodically reviewed."
        ],
        resolution_strategy="Review demand classification during functional safety assessment.",
        entity_scope="All SIFs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.9"
    ),
    DoctrineBlock(
        topic="SIS Hardware Fault Tolerance Requirements",
        keywords=["SIS", "Hardware Fault Tolerance", "HFT", "IEC 61511", "Redundancy"],
        conclusion_template="SIS hardware fault tolerance must meet IEC 61511 requirements based on SIL and device type.",
        reasoning_framework=(
            "1. Determine required SIL for each SIF.\n"
            "2. Identify device type (A or B) per IEC 61508.\n"
            "3. Apply hardware fault tolerance tables to determine minimum redundancy.\n"
            "4. Justify any deviations with risk assessment and authority approval."
        ),
        key_factors=[
            "SIL requirement",
            "Device type",
            "Redundancy",
            "IEC 61511 tables"
        ],
        primary_authority=["IEC 61511", "IEC 61508"],
        burden_holder="SIS Hardware Engineer",
        adversary_position="Insufficient fault tolerance may compromise SIL.",
        counter_arguments=[
            "Design meets or exceeds minimum requirements.",
            "Deviations justified and approved.",
            "Design independently reviewed."
        ],
        resolution_strategy="Design review and functional safety assessment.",
        entity_scope="All SIS hardware",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Table 6"
    ),
    DoctrineBlock(
        topic="SIS Device Selection and Prior Use Justification",
        keywords=["SIS", "Device Selection", "Prior Use", "Proven in Use", "IEC 61511"],
        conclusion_template="SIS devices must be selected based on prior use justification or certification to ensure reliability.",
        reasoning_framework=(
            "1. Review device certification and prior use history.\n"
            "2. Assess device suitability for SIS application.\n"
            "3. Document prior use justification per IEC 61511.\n"
            "4. Obtain approval from functional safety authority."
        ),
        key_factors=[
            "Device certification",
            "Prior use data",
            "Application suitability",
            "Documentation"
        ],
        primary_authority=["IEC 61511", "IEC 61508"],
        burden_holder="SIS Hardware Engineer",
        adversary_position="Unproven devices may increase risk of failure.",
        counter_arguments=[
            "Devices certified or justified by prior use.",
            "Documentation reviewed and approved.",
            "Device performance monitored in service."
        ],
        resolution_strategy="Independent review and periodic reassessment.",
        entity_scope="All SIS devices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.5"
    ),
    DoctrineBlock(
        topic="SIS Spare Parts and Obsolescence Management",
        keywords=["SIS", "Spare Parts", "Obsolescence", "Lifecycle", "IEC 61511"],
        conclusion_template="SIS spare parts and obsolescence must be managed to ensure ongoing system reliability and compliance.",
        reasoning_framework=(
            "1. Identify critical SIS spare parts and maintain inventory.\n"
            "2. Monitor vendor support and obsolescence status.\n"
            "3. Plan for replacement or upgrade of obsolete components.\n"
            "4. Document obsolescence management strategy."
        ),
        key_factors=[
            "Spare parts inventory",
            "Vendor support",
            "Obsolescence monitoring",
            "Replacement planning"
        ],
        primary_authority=["IEC 61511", "Company Asset Management Policy"],
        burden_holder="SIS Asset Manager",
        adversary_position="Obsolete parts may compromise SIS reliability.",
        counter_arguments=[
            "Obsolescence monitored and managed.",
            "Replacement plans in place.",
            "Inventory maintained for critical parts."
        ],
        resolution_strategy="Periodic review and update of obsolescence plan.",
        entity_scope="All SIS components",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.2"
    ),
    DoctrineBlock(
        topic="SIS Alarm Management Interface",
        keywords=["SIS", "Alarm Management", "Interface", "BPCS", "IEC 62682"],
        conclusion_template="SIS alarms must be clearly identified and managed to avoid confusion with BPCS alarms.",
        reasoning_framework=(
            "1. Identify all SIS-generated alarms and their purpose.\n"
            "2. Ensure SIS alarms are distinguishable from BPCS alarms in the HMI.\n"
            "3. Document alarm response procedures.\n"
            "4. Review alarm management during functional safety assessment."
        ),
        key_factors=[
            "Alarm identification",
            "HMI interface",
            "Response procedures",
            "Assessment"
        ],
        primary_authority=["IEC 62682", "IEC 61511"],
        burden_holder="SIS System Integrator",
        adversary_position="SIS alarms may be misinterpreted or ignored.",
        counter_arguments=[
            "Alarms clearly identified and documented.",
            "Operators trained on SIS alarm response.",
            "Alarm management reviewed periodically."
        ],
        resolution_strategy="Alarm rationalization and operator training.",
        entity_scope="All SIS alarms",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 62682:2014"
    ),
    DoctrineBlock(
        topic="SIS Trip Setpoint Management",
        keywords=["SIS", "Trip Setpoint", "Management", "Change Control", "IEC 61511"],
        conclusion_template="SIS trip setpoints must be controlled and documented to prevent unauthorized or unsafe changes.",
        reasoning_framework=(
            "1. Document all SIS trip setpoints and their basis.\n"
            "2. Control changes through formal change management.\n"
            "3. Review setpoints periodically for continued validity.\n"
            "4. Update documentation after any change."
        ),
        key_factors=[
            "Setpoint documentation",
            "Change control",
            "Periodic review",
            "Authorization"
        ],
        primary_authority=["IEC 61511", "Company Setpoint Policy"],
        burden_holder="SIS System Owner",
        adversary_position="Unauthorized setpoint changes may compromise safety.",
        counter_arguments=[
            "Change control enforced.",
            "Setpoints reviewed regularly.",
            "Documentation kept up to date."
        ],
        resolution_strategy="Setpoint audit and access control.",
        entity_scope="All SIS trip setpoints",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 17"
    ),
    DoctrineBlock(
        topic="SIS Manual Initiation and Reset Management",
        keywords=["SIS", "Manual Initiation", "Reset", "Human Factors", "IEC 61511"],
        conclusion_template="Manual initiation and reset of SIS actions must be designed to prevent inadvertent or unauthorized operation.",
        reasoning_framework=(
            "1. Design manual initiation and reset devices to require deliberate action.\n"
            "2. Locate devices to minimize risk of accidental operation.\n"
            "3. Control access to authorized personnel only.\n"
            "4. Document procedures and train operators."
        ),
        key_factors=[
            "Device design",
            "Location",
            "Access control",
            "Operator training"
        ],
        primary_authority=["IEC 61511", "Company Human Factors Policy"],
        burden_holder="SIS System Integrator",
        adversary_position="Manual actions may be performed inadvertently or by unauthorized personnel.",
        counter_arguments=[
            "Design and access controls minimize risk.",
            "Operators trained and procedures documented.",
            "Manual actions reviewed during assessment."
        ],
        resolution_strategy="Design review and operator training.",
        entity_scope="All SIS manual initiation and reset devices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.8"
    ),
    DoctrineBlock(
        topic="SIS Environmental and EMC Qualification",
        keywords=["SIS", "Environmental Qualification", "EMC", "IEC 61508", "Reliability"],
        conclusion_template="SIS hardware must be qualified for environmental and EMC conditions to ensure reliable operation.",
        reasoning_framework=(
            "1. Identify environmental and EMC requirements for SIS installation location.\n"
            "2. Select hardware certified for relevant conditions (temperature, humidity, vibration, EMC).\n"
            "3. Test or validate hardware as needed.\n"
            "4. Document qualification and maintain records."
        ),
        key_factors=[
            "Environmental requirements",
            "EMC standards",
            "Hardware certification",
            "Documentation"
        ],
        primary_authority=["IEC 61508", "Company Hardware Specification"],
        burden_holder="SIS Hardware Engineer",
        adversary_position="Unqualified hardware may fail in service.",
        counter_arguments=[
            "Hardware certified for installation environment.",
            "Qualification documented and reviewed.",
            "Periodic reassessment performed."
        ],
        resolution_strategy="Hardware qualification review and testing.",
        entity_scope="All SIS hardware",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61508:2010, Part 2"
    ),
    DoctrineBlock(
        topic="SIS Field Device Diagnostics and Maintenance",
        keywords=["SIS", "Field Device", "Diagnostics", "Maintenance", "SIL"],
        conclusion_template="SIS field devices should include diagnostics to detect failures and support maintenance.",
        reasoning_framework=(
            "1. Select field devices with self-diagnostics where possible.\n"
            "2. Monitor diagnostic alarms and respond promptly.\n"
            "3. Integrate diagnostics into maintenance procedures.\n"
            "4. Review device performance and update maintenance as needed."
        ),
        key_factors=[
            "Device diagnostics",
            "Alarm monitoring",
            "Maintenance procedures",
            "Performance review"
        ],
        primary_authority=["IEC 61511", "ISA TR84.00.02"],
        burden_holder="SIS Maintenance Engineer",
        adversary_position="Lack of diagnostics may delay failure detection.",
        counter_arguments=[
            "Diagnostics specified for critical devices.",
            "Alarms monitored and responded to.",
            "Maintenance updated with device performance."
        ],
        resolution_strategy="Periodic review of device diagnostics and maintenance.",
        entity_scope="All SIS field devices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.6"
    ),
    DoctrineBlock(
        topic="SIS Integration with Asset Management Systems",
        keywords=["SIS", "Asset Management", "Integration", "Maintenance", "IEC 61511"],
        conclusion_template="SIS may be integrated with asset management systems for maintenance support, with strict access controls.",
        reasoning_framework=(
            "1. Evaluate benefits and risks of SIS integration with asset management systems.\n"
            "2. Implement read-only or limited write access to SIS data.\n"
            "3. Control access and monitor for unauthorized changes.\n"
            "4. Document integration and review periodically."
        ),
        key_factors=[
            "Integration benefits",
            "Access control",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=["IEC 61511", "Company Asset Management Policy"],
        burden_holder="SIS System Integrator",
        adversary_position="Integration may compromise SIS security or integrity.",
        counter_arguments=[
            "Access controls enforced.",
            "Integration reviewed and documented.",
            "Periodic monitoring for unauthorized access."
        ],
        resolution_strategy="Integration review and access audit.",
        entity_scope="All SIS asset management interfaces",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.2"
    ),
    DoctrineBlock(
        topic="SIS Decommissioning and Retirement",
        keywords=["SIS", "Decommissioning", "Retirement", "Lifecycle", "IEC 61511"],
        conclusion_template="SIS decommissioning must be planned and documented to ensure safe removal from service.",
        reasoning_framework=(
            "1. Develop decommissioning plan covering all SIS components.\n"
            "2. Assess risks and implement controls during decommissioning.\n"
            "3. Document decommissioning activities and update records.\n"
            "4. Review plan and execution with functional safety authority."
        ),
        key_factors=[
            "Decommissioning plan",
            "Risk assessment",
            "Documentation",
            "Review and approval"
        ],
        primary_authority=["IEC 61511", "Company Decommissioning Policy"],
        burden_holder="SIS Project Manager",
        adversary_position="Unplanned decommissioning may create hazards.",
        counter_arguments=[
            "Plan developed and reviewed.",
            "Risks assessed and controlled.",
            "Activities documented and records updated."
        ],
        resolution_strategy="Decommissioning review and approval.",
        entity_scope="All SIS decommissioning activities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 5.2.7"
    ),
    DoctrineBlock(
        topic="SIS Management of Change (MOC)",
        keywords=["SIS", "Management of Change", "MOC", "IEC 61511", "Configuration"],
        conclusion_template="All SIS changes must be controlled through formal MOC procedures to ensure safety and compliance.",
        reasoning_framework=(
            "1. Document all proposed SIS changes and assess risk.\n"
            "2. Obtain approval from authorized personnel.\n"
            "3. Update affected documentation and records.\n"
            "4. Communicate changes to all stakeholders.\n"
            "5. Review MOC effectiveness periodically."
        ),
        key_factors=[
            "Change documentation",
            "Risk assessment",
            "Approval",
            "Communication"
        ],
        primary_authority=["IEC 61511", "Company MOC Policy"],
        burden_holder="SIS System Owner",
        adversary_position="Uncontrolled changes may introduce hazards.",
        counter_arguments=[
            "MOC procedures enforced.",
            "Changes reviewed and approved.",
            "Stakeholders informed."
        ],
        resolution_strategy="MOC audit and corrective actions.",
        entity_scope="All SIS changes",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 17"
    ),
    DoctrineBlock(
        topic="SIS Field Device Calibration Management",
        keywords=["SIS", "Field Device", "Calibration", "Maintenance", "IEC 61511"],
        conclusion_template="SIS field devices must be calibrated at defined intervals to ensure accurate and reliable operation.",
        reasoning_framework=(
            "1. Define calibration intervals based on device type and service conditions.\n"
            "2. Document calibration procedures and records.\n"
            "3. Review calibration results and update intervals as needed.\n"
            "4. Train personnel on calibration requirements."
        ),
        key_factors=[
            "Calibration interval",
            "Procedure documentation",
            "Record keeping",
            "Personnel training"
        ],
        primary_authority=["IEC 61511", "Company Calibration Policy"],
        burden_holder="SIS Maintenance Engineer",
        adversary_position="Infrequent calibration may lead to undetected device drift.",
        counter_arguments=[
            "Intervals based on device history and service.",
            "Calibration records maintained.",
            "Procedures reviewed and updated."
        ],
        resolution_strategy="Calibration audit and periodic review.",
        entity_scope="All SIS field devices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS Spurious Trip Rate Management",
        keywords=["SIS", "Spurious Trip", "Nuisance Trip", "Reliability", "IEC 61511"],
        conclusion_template="SIS design must minimize spurious trips to avoid unnecessary process interruptions.",
        reasoning_framework=(
            "1. Analyze potential causes of spurious trips in SIS design.\n"
            "2. Implement measures such as filtering, voting logic, and diagnostics.\n"
            "3. Monitor spurious trip frequency and investigate causes.\n"
            "4. Update design and procedures to reduce spurious trips."
        ),
        key_factors=[
            "Trip cause analysis",
            "Design measures",
            "Monitoring",
            "Continuous improvement"
        ],
        primary_authority=["IEC 61511", "Company Reliability Policy"],
        burden_holder="SIS System Integrator",
        adversary_position="Frequent spurious trips may reduce operator confidence.",
        counter_arguments=[
            "Design measures implemented.",
            "Trips monitored and investigated.",
            "Continuous improvement applied."
        ],
        resolution_strategy="Spurious trip review and corrective actions.",
        entity_scope="All SIS trip functions",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.9"
    ),
    DoctrineBlock(
        topic="SIS Reset and Restart Procedures",
        keywords=["SIS", "Reset", "Restart", "Procedures", "IEC 61511"],
        conclusion_template="SIS reset and restart procedures must be documented and controlled to ensure safe return to service.",
        reasoning_framework=(
            "1. Develop reset and restart procedures for all SIS trip functions.\n"
            "2. Train operators and maintenance personnel.\n"
            "3. Control reset and restart actions to authorized personnel.\n"
            "4. Review procedures periodically."
        ),
        key_factors=[
            "Procedure documentation",
            "Personnel training",
            "Access control",
            "Periodic review"
        ],
        primary_authority=["IEC 61511", "Company Operations Policy"],
        burden_holder="SIS System Owner",
        adversary_position="Improper reset may compromise safety.",
        counter_arguments=[
            "Procedures documented and enforced.",
            "Personnel trained.",
            "Access controlled."
        ],
        resolution_strategy="Procedure audit and operator training.",
        entity_scope="All SIS reset and restart actions",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS Trip Event Recording and Analysis",
        keywords=["SIS", "Trip Event", "Recording", "Analysis", "IEC 61511"],
        conclusion_template="All SIS trip events must be recorded and analyzed to support continuous improvement.",
        reasoning_framework=(
            "1. Record all SIS trip events with relevant process data.\n"
            "2. Analyze trip causes and outcomes.\n"
            "3. Implement corrective actions as needed.\n"
            "4. Review trip data periodically for trends."
        ),
        key_factors=[
            "Event recording",
            "Cause analysis",
            "Corrective actions",
            "Trend review"
        ],
        primary_authority=["IEC 61511", "Company Event Analysis Policy"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Trip causes may not be understood or addressed.",
        counter_arguments=[
            "Events recorded and analyzed.",
            "Corrective actions tracked.",
            "Trends reviewed for improvement."
        ],
        resolution_strategy="Trip event audit and continuous improvement.",
        entity_scope="All SIS trip events",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS Functional Testing after Maintenance",
        keywords=["SIS", "Functional Testing", "Maintenance", "IEC 61511"],
        conclusion_template="SIS must be functionally tested after maintenance to confirm correct operation.",
        reasoning_framework=(
            "1. Define functional test requirements for post-maintenance activities.\n"
            "2. Document test procedures and results.\n"
            "3. Review test outcomes and address any issues.\n"
            "4. Restore SIS to service only after successful testing."
        ),
        key_factors=[
            "Test requirements",
            "Procedure documentation",
            "Result review",
            "Service restoration"
        ],
        primary_authority=["IEC 61511", "Company Maintenance Policy"],
        burden_holder="SIS Maintenance Engineer",
        adversary_position="Failures may go undetected if not tested after maintenance.",
        counter_arguments=[
            "Testing required and documented.",
            "Results reviewed before service restoration.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Maintenance audit and periodic review.",
        entity_scope="All SIS post-maintenance activities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS Field Device Failure Data Collection",
        keywords=["SIS", "Field Device", "Failure Data", "Collection", "Reliability"],
        conclusion_template="Field device failure data must be collected and analyzed to support reliability improvement and SIL verification.",
        reasoning_framework=(
            "1. Record all SIS field device failures and repair actions.\n"
            "2. Analyze failure data for trends and root causes.\n"
            "3. Update reliability data and SIL verification as needed.\n"
            "4. Share data with functional safety team."
        ),
        key_factors=[
            "Failure data recording",
            "Trend analysis",
            "SIL verification update",
            "Data sharing"
        ],
        primary_authority=["IEC 61511", "Company Reliability Policy"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Lack of data may hinder reliability improvement.",
        counter_arguments=[
            "Failure data collected and analyzed.",
            "Trends reviewed and acted upon.",
            "Data shared with stakeholders."
        ],
        resolution_strategy="Reliability audit and continuous improvement.",
        entity_scope="All SIS field devices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS Periodic Review and Continuous Improvement",
        keywords=["SIS", "Periodic Review", "Continuous Improvement", "IEC 61511"],
        conclusion_template="SIS performance must be periodically reviewed to identify and implement improvements.",
        reasoning_framework=(
            "1. Review SIS performance data, trip events, and maintenance records.\n"
            "2. Identify areas for improvement and implement corrective actions.\n"
            "3. Document review findings and actions taken.\n"
            "4. Repeat review at defined intervals."
        ),
        key_factors=[
            "Performance data review",
            "Corrective actions",
            "Documentation",
            "Review interval"
        ],
        primary_authority=["IEC 61511", "Company Continuous Improvement Policy"],
        burden_holder="Functional Safety Manager",
        adversary_position="Lack of review may allow issues to persist.",
        counter_arguments=[
            "Reviews scheduled and documented.",
            "Actions tracked to closure.",
            "Continuous improvement culture promoted."
        ],
        resolution_strategy="Periodic review and management oversight.",
        entity_scope="All SIS installations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 5.2.6"
    ),
    DoctrineBlock(
        topic="SIS SIF Bypass Alarm and Logging",
        keywords=["SIS", "SIF", "Bypass", "Alarm", "Logging", "IEC 61511"],
        conclusion_template="All SIF bypasses must be alarmed and logged to ensure operator awareness and accountability.",
        reasoning_framework=(
            "1. Configure SIS to generate alarms for all active SIF bypasses.\n"
            "2. Log bypass activity with time, duration, and responsible personnel.\n"
            "3. Review bypass logs periodically for trends and compliance.\n"
            "4. Train operators on bypass alarm response."
        ),
        key_factors=[
            "Bypass alarm configuration",
            "Logging and accountability",
            "Periodic review",
            "Operator training"
        ],
        primary_authority=["IEC 61511", "Company Bypass Policy"],
        burden_holder="SIS System Integrator",
        adversary_position="Bypasses may go unnoticed, increasing risk.",
        counter_arguments=[
            "Alarms and logs ensure awareness.",
            "Bypass activity reviewed.",
            "Operators trained on response."
        ],
        resolution_strategy="Bypass log audit and operator training.",
        entity_scope="All SIF bypasses",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.7"
    ),
    DoctrineBlock(
        topic="SIS SIF Demand and Failure Rate Monitoring",
        keywords=["SIS", "SIF", "Demand Rate", "Failure Rate", "Monitoring", "IEC 61511"],
        conclusion_template="SIS must monitor SIF demand and failure rates to support SIL verification and reliability improvement.",
        reasoning_framework=(
            "1. Record all SIF demands and outcomes.\n"
            "2. Monitor and analyze SIF failure rates.\n"
            "3. Update SIL verification and reliability data as needed.\n"
            "4. Review data periodically for trends and improvement opportunities."
        ),
        key_factors=[
            "Demand and failure recording",
            "Data analysis",
            "SIL verification update",
            "Periodic review"
        ],
        primary_authority=["IEC 61511", "Company Reliability Policy"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Lack of monitoring may hinder SIL compliance.",
        counter_arguments=[
            "Demands and failures recorded.",
            "Data analyzed and acted upon.",
            "Verification updated as needed."
        ],
        resolution_strategy="Reliability audit and continuous improvement.",
        entity_scope="All SIFs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS SIF Partial Stroke Testing",
        keywords=["SIS", "SIF", "Partial Stroke Testing", "Valve", "Proof Test", "IEC 61511"],
        conclusion_template="Partial stroke testing may be used to increase proof test coverage for SIS valves, with limitations documented.",
        reasoning_framework=(
            "1. Evaluate suitability of partial stroke testing for SIS valves.\n"
            "2. Document test coverage and limitations.\n"
            "3. Integrate partial stroke testing into proof test strategy.\n"
            "4. Review effectiveness periodically."
        ),
        key_factors=[
            "Test coverage",
            "Documentation",
            "Integration with proof test",
            "Periodic review"
        ],
        primary_authority=["IEC 61511", "ISA TR84.00.02"],
        burden_holder="SIS Maintenance Engineer",
        adversary_position="Partial stroke testing may not detect all failure modes.",
        counter_arguments=[
            "Test coverage documented.",
            "Limitations understood and addressed.",
            "Full proof test performed as required."
        ],
        resolution_strategy="Periodic review of test strategy.",
        entity_scope="All SIS valves with partial stroke testing",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS SIF Redundancy and Diversity",
        keywords=["SIS", "SIF", "Redundancy", "Diversity", "Common Cause Failure", "IEC 61511"],
        conclusion_template="SIF redundancy and diversity must be implemented as needed to reduce common cause failure risk.",
        reasoning_framework=(
            "1. Analyze SIF design for common cause failure risk.\n"
            "2. Implement redundancy and diversity in sensors, logic solvers, and final elements.\n"
            "3. Document design measures and review effectiveness.\n"
            "4. Update design as needed based on operating experience."
        ),
        key_factors=[
            "CCF analysis",
            "Redundancy and diversity",
            "Documentation",
            "Design review"
        ],
        primary_authority=["IEC 61511", "IEC 61508"],
        burden_holder="SIS Design Engineer",
        adversary_position="Insufficient redundancy/diversity may compromise SIL.",
        counter_arguments=[
            "Design measures implemented per standards.",
            "Effectiveness reviewed.",
            "Design updated as needed."
        ],
        resolution_strategy="Design review and periodic reassessment.",
        entity_scope="All SIFs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.4"
    ),
    DoctrineBlock(
        topic="SIS SIF Proof Test Optimization",
        keywords=["SIS", "SIF", "Proof Test", "Optimization", "Interval", "IEC 61511"],
        conclusion_template="Proof test intervals should be optimized to balance risk reduction and operational impact.",
        reasoning_framework=(
            "1. Analyze SIF failure data and operational constraints.\n"
            "2. Calculate PFDavg for various proof test intervals.\n"
            "3. Select interval that meets SIL target with minimal operational disruption.\n"
            "4. Review interval periodically with operating experience."
        ),
        key_factors=[
            "Failure data analysis",
            "PFDavg calculation",
            "Operational constraints",
            "Periodic review"
        ],
        primary_authority=["IEC 61511", "ISA TR84.00.02"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Intervals may be too short or too long for optimal performance.",
        counter_arguments=[
            "Intervals based on quantitative analysis.",
            "Reviewed with operations and safety.",
            "Updated with experience."
        ],
        resolution_strategy="Interval review and optimization.",
        entity_scope="All SIFs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.9"
    ),
    DoctrineBlock(
        topic="SIS SIF Functional Test Coverage",
        keywords=["SIS", "SIF", "Functional Test", "Coverage", "IEC 61511"],
        conclusion_template="Functional test coverage must be sufficient to verify all SIF safety functions.",
        reasoning_framework=(
            "1. Identify all SIF safety functions and failure modes.\n"
            "2. Develop test procedures to verify each function and mode.\n"
            "3. Document test coverage and results.\n"
            "4. Review coverage periodically."
        ),
        key_factors=[
            "Function identification",
            "Test procedure development",
            "Documentation",
            "Coverage review"
        ],
        primary_authority=["IEC 61511", "Company Test Policy"],
        burden_holder="SIS Test Engineer",
        adversary_position="Incomplete test coverage may miss failures.",
        counter_arguments=[
            "Coverage mapped to SRS.",
            "Procedures reviewed and updated.",
            "Results documented."
        ],
        resolution_strategy="Test coverage review and update.",
        entity_scope="All SIFs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 14"
    ),
    DoctrineBlock(
        topic="SIS SIF Failure Reporting and Corrective Action",
        keywords=["SIS", "SIF", "Failure Reporting", "Corrective Action", "IEC 61511"],
        conclusion_template="All SIF failures must be reported and corrective actions tracked to closure.",
        reasoning_framework=(
            "1. Report all SIF failures promptly.\n"
            "2. Investigate root cause and document findings.\n"
            "3. Implement corrective actions and track to closure.\n"
            "4. Review effectiveness of actions."
        ),
        key_factors=[
            "Failure reporting",
            "Root cause analysis",
            "Corrective action tracking",
            "Effectiveness review"
        ],
        primary_authority=["IEC 61511", "Company Reliability Policy"],
        burden_holder="SIS Reliability Engineer",
        adversary_position="Failures may not be addressed, risking recurrence.",
        counter_arguments=[
            "Reporting and tracking system in place.",
            "Actions reviewed for effectiveness.",
            "Continuous improvement applied."
        ],
        resolution_strategy="Failure audit and management review.",
        entity_scope="All SIFs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 16.3"
    ),
    DoctrineBlock(
        topic="SIS SIF Demand Simulation and Testing",
        keywords=["SIS", "SIF", "Demand Simulation", "Testing", "IEC 61511"],
        conclusion_template="SIF demand simulation and testing must be performed to verify correct operation under all expected conditions.",
        reasoning_framework=(
            "1. Identify all credible SIF demand scenarios.\n"
            "2. Simulate demands and test SIF response.\n"
            "3. Document test results and address any issues.\n"
            "4. Repeat testing periodically."
        ),
        key_factors=[
            "Scenario identification",
            "Simulation and testing",
            "Documentation",
            "Periodic testing"
        ],
        primary_authority=["IEC 61511", "Company Test Policy"],
        burden_holder="SIS Test Engineer",
        adversary_position="SIF may not operate correctly under all conditions.",
        counter_arguments=[
            "All credible scenarios tested.",
            "Results documented and reviewed.",
            "Testing repeated as needed."
        ],
        resolution_strategy="Test review and continuous improvement.",
        entity_scope="All SIFs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 14"
    ),
    DoctrineBlock(
        topic="SIS SIF Trip Override Control",
        keywords=["SIS", "SIF", "Trip Override", "Control", "IEC 61511"],
        conclusion_template="Trip overrides must be controlled, documented, and alarmed to prevent unauthorized or unsafe operation.",
        reasoning_framework=(
            "1. Document all trip override conditions and procedures.\n"
            "2. Control override access to authorized personnel.\n"
            "3. Alarm and log all active overrides.\n"
            "4. Review override use periodically."
        ),
        key_factors=[
            "Override documentation",
            "Access control",
            "Alarm and logging",
            "Periodic review"
        ],
        primary_authority=["IEC 61511", "Company Override Policy"],
        burden_holder="SIS System Owner",
        adversary_position="Unauthorized overrides may compromise safety.",
        counter_arguments=[
            "Override use controlled and documented.",
            "Alarms and logs ensure awareness.",
            "Review performed regularly."
        ],
        resolution_strategy="Override audit and management review.",
        entity_scope="All SIF trip overrides",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61511:2016, Clause 11.7"
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
        if (
            keyword_lower in doctrine.topic.lower()
            or any(keyword_lower in k.lower() for k in doctrine.keywords)
            or keyword_lower in doctrine.reasoning_framework.lower()
            or keyword_lower in doctrine.conclusion_template.lower()
        ):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]