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
        topic="COSO Internal Control Framework Foundation",
        keywords=["COSO", "internal control", "framework", "control environment", "risk assessment"],
        conclusion_template="The entity's internal control system is evaluated against the COSO Internal Control Framework, focusing on the five integrated components.",
        reasoning_framework=(
            "1. Identify the presence and adequacy of the five COSO components: Control Environment, Risk Assessment, "
            "Control Activities, Information & Communication, and Monitoring Activities.\n"
            "2. Assess whether the 17 principles supporting the components are present and functioning.\n"
            "3. Evaluate the integration of controls into business processes and their effectiveness in mitigating risk.\n"
            "4. Consider the role of management oversight and the tone at the top.\n"
            "5. Review documentation, interviews, and walk-throughs to evidence control design and operation.\n"
            "6. Benchmark practices against COSO guidance and industry standards.\n"
            "7. Identify gaps and recommend remediation where principles are not met.\n"
            "8. Document findings with reference to COSO's authoritative literature.\n"
            "9. Assess the impact of control deficiencies on overall objectives.\n"
            "10. Conclude on the adequacy of the internal control framework implementation."
        ),
        key_factors=[
            "Presence of five COSO components",
            "Effectiveness of 17 principles",
            "Management oversight",
            "Integration with business processes",
            "Documentation and evidence"
        ],
        primary_authority=[
            "COSO Internal Control-Integrated Framework (2013)",
            "AICPA guidance on internal controls"
        ],
        burden_holder="Management",
        adversary_position="Controls are not sufficiently designed or operating effectively.",
        counter_arguments=[
            "Controls are documented but not implemented.",
            "Management override undermines control environment.",
            "Principles are not tailored to entity's risk profile."
        ],
        resolution_strategy="Perform gap analysis, recommend remediation, and monitor corrective actions.",
        entity_scope="Enterprise-wide",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="COSO 2013 Framework"
    ),
    DoctrineBlock(
        topic="Three Lines of Defense Model",
        keywords=["three lines", "defense", "governance", "risk management", "assurance"],
        conclusion_template="The entity's governance structure is assessed using the Three Lines of Defense Model to determine role clarity and effectiveness.",
        reasoning_framework=(
            "1. Define the roles and responsibilities of the first, second, and third lines (operations, risk/compliance, internal audit).\n"
            "2. Evaluate the independence of the second and third lines from operational management.\n"
            "3. Assess communication and reporting lines to senior management and the board.\n"
            "4. Review policies and procedures delineating responsibilities.\n"
            "5. Examine the effectiveness of risk identification, management, and assurance activities.\n"
            "6. Identify overlaps, gaps, or conflicts in roles.\n"
            "7. Benchmark against IIA guidance and regulatory expectations.\n"
            "8. Recommend enhancements to clarify roles and strengthen governance."
        ),
        key_factors=[
            "Role clarity among three lines",
            "Independence of assurance functions",
            "Communication with governance bodies",
            "Policy documentation"
        ],
        primary_authority=[
            "IIA Position Paper: The Three Lines of Defense in Effective Risk Management and Control",
            "COSO Guidance"
        ],
        burden_holder="Board and Senior Management",
        adversary_position="Lines of defense are not clearly defined or independent.",
        counter_arguments=[
            "Operational and assurance roles are combined.",
            "Reporting lines are ambiguous.",
            "Insufficient resources for second/third line."
        ],
        resolution_strategy="Clarify roles, segregate duties, and reinforce reporting structures.",
        entity_scope="Enterprise governance",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IIA Three Lines Model (2020)"
    ),
    DoctrineBlock(
        topic="Risk-Based Audit Planning Methodology",
        keywords=["risk-based", "audit planning", "methodology", "risk assessment", "audit universe"],
        conclusion_template="The audit plan is developed using a risk-based methodology, prioritizing areas of highest risk to the organization.",
        reasoning_framework=(
            "1. Define the audit universe, including all auditable entities and processes.\n"
            "2. Conduct a comprehensive risk assessment considering inherent and residual risks.\n"
            "3. Engage stakeholders to validate risk assessments and priorities.\n"
            "4. Allocate audit resources to areas with the highest risk exposure.\n"
            "5. Document the rationale for audit selection and frequency.\n"
            "6. Align the audit plan with organizational objectives and regulatory requirements.\n"
            "7. Review and update the plan periodically to reflect emerging risks.\n"
            "8. Ensure board/committee approval of the risk-based audit plan."
        ),
        key_factors=[
            "Comprehensive audit universe",
            "Stakeholder engagement",
            "Alignment with risk profile",
            "Resource allocation"
        ],
        primary_authority=[
            "IIA International Standards for the Professional Practice of Internal Auditing (Standard 2010)",
            "COSO Risk Assessment Principles"
        ],
        burden_holder="Chief Audit Executive",
        adversary_position="Audit plan does not reflect current risk profile or is not updated.",
        counter_arguments=[
            "Plan is static and not responsive to changes.",
            "Audit coverage is not risk-prioritized.",
            "Stakeholders not consulted."
        ],
        resolution_strategy="Update risk assessment, engage stakeholders, and re-prioritize audit coverage.",
        entity_scope="Internal audit function",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IIA Standard 2010"
    ),
    DoctrineBlock(
        topic="Control Testing Sampling and Evidence",
        keywords=["control testing", "sampling", "audit evidence", "test of controls", "sampling methodology"],
        conclusion_template="Control testing is performed using statistically valid sampling methods, and sufficient, appropriate evidence is obtained.",
        reasoning_framework=(
            "1. Define the population and sampling unit for the control test.\n"
            "2. Select an appropriate sampling method (random, stratified, judgmental).\n"
            "3. Determine sample size based on risk, population size, and expected error rate.\n"
            "4. Document the rationale for sampling choices.\n"
            "5. Collect and evaluate evidence for each sample item.\n"
            "6. Assess whether deviations are isolated or indicative of control failure.\n"
            "7. Conclude on control effectiveness based on sample results and extrapolation.\n"
            "8. Retain documentation supporting sampling and evidence sufficiency."
        ),
        key_factors=[
            "Sampling methodology",
            "Sample size determination",
            "Evidence sufficiency",
            "Deviation analysis"
        ],
        primary_authority=[
            "IIA Standard 2310",
            "AICPA Audit Sampling Guidance"
        ],
        burden_holder="Internal Auditor",
        adversary_position="Sampling is not statistically valid or evidence is insufficient.",
        counter_arguments=[
            "Sample size too small to draw conclusions.",
            "Non-random selection introduces bias.",
            "Evidence is incomplete or not retained."
        ],
        resolution_strategy="Re-perform testing with valid sampling and obtain additional evidence.",
        entity_scope="Audit engagements",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AICPA AU-C Section 530"
    ),
    DoctrineBlock(
        topic="IIA International Standards for Professional Practice",
        keywords=["IIA", "standards", "internal audit", "professional practice", "compliance"],
        conclusion_template="Internal audit activities are assessed for compliance with IIA International Standards for the Professional Practice of Internal Auditing.",
        reasoning_framework=(
            "1. Review the internal audit charter, policies, and procedures for alignment with IIA Standards.\n"
            "2. Evaluate auditor independence, objectivity, and proficiency.\n"
            "3. Assess the planning, execution, and reporting of audit engagements.\n"
            "4. Verify adherence to quality assurance and improvement programs.\n"
            "5. Benchmark practices against the IIA Code of Ethics and Attribute/Performance Standards.\n"
            "6. Identify non-conformities and recommend corrective actions.\n"
            "7. Document compliance status and communicate results to the board."
        ),
        key_factors=[
            "Audit charter and policies",
            "Independence and objectivity",
            "Quality assurance program",
            "Engagement documentation"
        ],
        primary_authority=[
            "IIA International Standards",
            "IIA Code of Ethics"
        ],
        burden_holder="Internal Audit Function",
        adversary_position="Internal audit does not comply with IIA Standards.",
        counter_arguments=[
            "Lack of independence from management.",
            "No quality assurance program.",
            "Engagements not documented per standards."
        ],
        resolution_strategy="Implement corrective actions and periodic quality assessments.",
        entity_scope="Internal audit department",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IIA International Standards"
    ),
    DoctrineBlock(
        topic="DOJ Evaluation of Corporate Compliance Programs",
        keywords=["DOJ", "compliance program", "evaluation", "effectiveness", "prosecutors"],
        conclusion_template="The compliance program is evaluated using DOJ guidance to determine effectiveness and adequacy for mitigating misconduct.",
        reasoning_framework=(
            "1. Assess whether the compliance program is well-designed, implemented, and enforced.\n"
            "2. Review risk assessments and tailoring of controls to identified risks.\n"
            "3. Evaluate the autonomy and resources of the compliance function.\n"
            "4. Examine training, communication, and reporting mechanisms.\n"
            "5. Consider the program's track record in detecting and remediating misconduct.\n"
            "6. Benchmark against DOJ's three fundamental questions for prosecutors.\n"
            "7. Document findings and provide recommendations for enhancement."
        ),
        key_factors=[
            "Program design and implementation",
            "Risk assessment process",
            "Compliance function independence",
            "Training and communication"
        ],
        primary_authority=[
            "DOJ Evaluation of Corporate Compliance Programs (2020)",
            "Federal Sentencing Guidelines for Organizations"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Compliance program is a paper program, not effective in practice.",
        counter_arguments=[
            "Program lacks resources or authority.",
            "Training is not risk-based.",
            "No evidence of enforcement or remediation."
        ],
        resolution_strategy="Enhance program design, resource allocation, and enforcement mechanisms.",
        entity_scope="Corporate compliance",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DOJ Guidance 2020"
    ),
    DoctrineBlock(
        topic="Federal Sentencing Guidelines for Organizations",
        keywords=["federal sentencing", "guidelines", "organizations", "compliance", "mitigation"],
        conclusion_template="The organization's compliance program is assessed for alignment with the Federal Sentencing Guidelines for Organizations to determine eligibility for mitigation.",
        reasoning_framework=(
            "1. Review the existence and effectiveness of compliance and ethics programs.\n"
            "2. Assess whether the program prevents and detects criminal conduct.\n"
            "3. Evaluate senior management's commitment and oversight.\n"
            "4. Examine due diligence in hiring and retention practices.\n"
            "5. Review training, communication, and reporting systems.\n"
            "6. Assess enforcement and discipline for violations.\n"
            "7. Consider periodic program evaluation and improvement.\n"
            "8. Document compliance with the seven elements of an effective program."
        ),
        key_factors=[
            "Seven elements of effective compliance program",
            "Management oversight",
            "Training and communication",
            "Enforcement and discipline"
        ],
        primary_authority=[
            "Federal Sentencing Guidelines for Organizations (U.S.S.G. §8B2.1)",
            "DOJ Guidance"
        ],
        burden_holder="Organization",
        adversary_position="Compliance program is not effective or lacks key elements.",
        counter_arguments=[
            "No evidence of program enforcement.",
            "Training is not documented.",
            "Management is not involved."
        ],
        resolution_strategy="Implement and document all seven elements, with board oversight.",
        entity_scope="All U.S. organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="U.S.S.G. §8B2.1"
    ),
    DoctrineBlock(
        topic="Gap Analysis Methodology",
        keywords=["gap analysis", "methodology", "compliance gaps", "remediation", "benchmarking"],
        conclusion_template="A structured gap analysis is conducted to identify and remediate deficiencies relative to regulatory or best practice standards.",
        reasoning_framework=(
            "1. Define the benchmark standard or regulatory requirement.\n"
            "2. Map current practices and controls against the benchmark.\n"
            "3. Identify gaps, deficiencies, and areas of non-compliance.\n"
            "4. Assess the impact and risk associated with each gap.\n"
            "5. Prioritize remediation efforts based on risk and resource constraints.\n"
            "6. Develop and track corrective action plans.\n"
            "7. Monitor progress and re-assess periodically."
        ),
        key_factors=[
            "Benchmark selection",
            "Gap identification",
            "Impact and risk assessment",
            "Remediation planning"
        ],
        primary_authority=[
            "COSO Framework",
            "IIA Standards",
            "Relevant regulatory guidance"
        ],
        burden_holder="Process Owner",
        adversary_position="Gaps are not identified or remediated timely.",
        counter_arguments=[
            "Benchmark is not appropriate.",
            "Gaps are underestimated.",
            "Remediation is not tracked."
        ],
        resolution_strategy="Use structured methodology and track corrective actions to closure.",
        entity_scope="All business units",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="COSO Gap Analysis Guidance"
    ),
    DoctrineBlock(
        topic="Regulatory Change Management and Horizon Scanning",
        keywords=["regulatory change", "horizon scanning", "compliance", "change management", "monitoring"],
        conclusion_template="The entity's regulatory change management process is evaluated for effectiveness in identifying, assessing, and implementing new requirements.",
        reasoning_framework=(
            "1. Establish processes for monitoring regulatory developments and horizon scanning.\n"
            "2. Assign responsibility for regulatory intelligence gathering.\n"
            "3. Assess the process for impact analysis and stakeholder communication.\n"
            "4. Review tracking and implementation of regulatory changes.\n"
            "5. Evaluate documentation and evidence of compliance with new requirements.\n"
            "6. Benchmark against industry best practices and regulatory expectations.\n"
            "7. Recommend improvements to enhance responsiveness and compliance."
        ),
        key_factors=[
            "Regulatory monitoring process",
            "Responsibility assignment",
            "Impact analysis",
            "Change implementation"
        ],
        primary_authority=[
            "OCC Heightened Standards",
            "FFIEC Guidance",
            "Relevant industry regulations"
        ],
        burden_holder="Compliance Department",
        adversary_position="Regulatory changes are missed or not implemented timely.",
        counter_arguments=[
            "No formal horizon scanning process.",
            "Impact analysis is not performed.",
            "Implementation is not tracked."
        ],
        resolution_strategy="Formalize change management, assign accountability, and track implementation.",
        entity_scope="Regulated entities",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="OCC Bulletin 2014-16"
    ),
    DoctrineBlock(
        topic="Audit Workpaper Standards and Documentation",
        keywords=["audit workpapers", "documentation", "standards", "evidence", "retention"],
        conclusion_template="Audit workpapers are reviewed for compliance with professional standards, ensuring sufficient, appropriate documentation of audit work.",
        reasoning_framework=(
            "1. Review workpaper organization, indexing, and cross-referencing.\n"
            "2. Assess sufficiency and appropriateness of evidence documented.\n"
            "3. Verify that workpapers support audit conclusions and findings.\n"
            "4. Evaluate retention policies and security of workpapers.\n"
            "5. Benchmark documentation practices against IIA and AICPA standards.\n"
            "6. Identify deficiencies and recommend improvements."
        ),
        key_factors=[
            "Workpaper organization",
            "Evidence sufficiency",
            "Retention and security",
            "Support for findings"
        ],
        primary_authority=[
            "IIA Standard 2330",
            "AICPA AU-C Section 230"
        ],
        burden_holder="Internal Auditor",
        adversary_position="Workpapers do not support findings or are not retained.",
        counter_arguments=[
            "Documentation is incomplete.",
            "Evidence is not cross-referenced.",
            "Retention policies are not followed."
        ],
        resolution_strategy="Enhance documentation standards and perform periodic reviews.",
        entity_scope="Audit engagements",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IIA Standard 2330"
    ),
    DoctrineBlock(
        topic="Finding Classification: Critical, Major, Minor, Observation",
        keywords=["finding classification", "critical", "major", "minor", "observation", "risk rating"],
        conclusion_template="Audit findings are classified based on risk and impact, using defined criteria for critical, major, minor, and observation.",
        reasoning_framework=(
            "1. Establish criteria for each finding classification, considering impact, likelihood, and regulatory requirements.\n"
            "2. Assess the risk and impact of each finding to the organization.\n"
            "3. Assign classification based on established criteria and supporting evidence.\n"
            "4. Document rationale for classification and communicate to stakeholders.\n"
            "5. Review classifications periodically for consistency and appropriateness."
        ),
        key_factors=[
            "Defined classification criteria",
            "Risk and impact assessment",
            "Consistency in application",
            "Stakeholder communication"
        ],
        primary_authority=[
            "IIA Practice Guide: Audit Findings",
            "COSO Risk Assessment"
        ],
        burden_holder="Internal Auditor",
        adversary_position="Findings are not classified consistently or criteria are unclear.",
        counter_arguments=[
            "Criteria are subjective or not documented.",
            "Risk assessment is not performed.",
            "Stakeholders are not informed."
        ],
        resolution_strategy="Develop and communicate clear classification criteria, and review for consistency.",
        entity_scope="Audit reporting",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="IIA Practice Guide"
    ),
    DoctrineBlock(
        topic="Corrective Action Plan (CAP) Development and Tracking",
        keywords=["corrective action plan", "CAP", "remediation", "tracking", "audit finding"],
        conclusion_template="Corrective Action Plans (CAPs) are developed and tracked for all audit findings, ensuring timely and effective remediation.",
        reasoning_framework=(
            "1. Assign responsibility for CAP development and implementation.\n"
            "2. Define clear actions, timelines, and success criteria for each CAP.\n"
            "3. Track progress and completion of CAPs.\n"
            "4. Validate remediation through follow-up testing.\n"
            "5. Escalate overdue or ineffective CAPs to management.\n"
            "6. Document CAP status and communicate with stakeholders."
        ),
        key_factors=[
            "Responsibility assignment",
            "Action definition and timelines",
            "Progress tracking",
            "Follow-up validation"
        ],
        primary_authority=[
            "IIA Standard 2500",
            "OCC Heightened Standards"
        ],
        burden_holder="Process Owner",
        adversary_position="CAPs are not implemented or tracked effectively.",
        counter_arguments=[
            "No responsible party assigned.",
            "Actions are vague or timelines are unclear.",
            "No follow-up testing performed."
        ],
        resolution_strategy="Formalize CAP process, assign accountability, and monitor progress.",
        entity_scope="All audit findings",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IIA Standard 2500"
    ),
    DoctrineBlock(
        topic="Regulatory Exam Preparation and Response",
        keywords=["regulatory exam", "preparation", "response", "regulator", "supervisory"],
        conclusion_template="The entity's regulatory exam preparation and response process is evaluated for effectiveness in ensuring positive regulatory outcomes.",
        reasoning_framework=(
            "1. Establish a regulatory exam management process, including pre-exam preparation and post-exam response.\n"
            "2. Assign roles and responsibilities for gathering documentation and coordinating responses.\n"
            "3. Conduct mock exams and readiness assessments.\n"
            "4. Review communication protocols with regulators.\n"
            "5. Track and respond to regulatory findings and recommendations.\n"
            "6. Document exam outcomes and lessons learned."
        ),
        key_factors=[
            "Exam management process",
            "Roles and responsibilities",
            "Mock exams and readiness",
            "Response tracking"
        ],
        primary_authority=[
            "OCC Exam Guidance",
            "FFIEC IT Examination Handbook"
        ],
        burden_holder="Compliance Department",
        adversary_position="Exam preparation is ad hoc and responses are delayed or incomplete.",
        counter_arguments=[
            "No formal exam management process.",
            "Roles are unclear.",
            "Findings are not tracked or remediated."
        ],
        resolution_strategy="Implement formal exam management and response tracking.",
        entity_scope="Regulated entities",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="OCC Exam Management Guidance"
    ),
    DoctrineBlock(
        topic="Compliance Calendar and Periodic Deliverables Tracking",
        keywords=["compliance calendar", "deliverables", "tracking", "periodic", "obligations"],
        conclusion_template="A compliance calendar is maintained and periodic deliverables are tracked to ensure timely fulfillment of regulatory obligations.",
        reasoning_framework=(
            "1. Identify all periodic regulatory and contractual deliverables.\n"
            "2. Maintain a centralized compliance calendar with deadlines and responsible parties.\n"
            "3. Monitor completion and escalate overdue items.\n"
            "4. Review calendar accuracy and completeness periodically.\n"
            "5. Communicate obligations and deadlines to relevant stakeholders."
        ),
        key_factors=[
            "Centralized compliance calendar",
            "Responsibility assignment",
            "Monitoring and escalation",
            "Periodic review"
        ],
        primary_authority=[
            "OCC Heightened Standards",
            "FFIEC Guidance"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Deliverables are missed or calendar is not maintained.",
        counter_arguments=[
            "Calendar is incomplete or not updated.",
            "No monitoring or escalation process.",
            "Stakeholders are unaware of obligations."
        ],
        resolution_strategy="Implement automated tracking and periodic reviews.",
        entity_scope="All compliance obligations",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="OCC Bulletin 2014-16"
    ),
    # Additional DoctrineBlocks for comprehensive coverage (20+ more)
    DoctrineBlock(
        topic="Management Override of Controls",
        keywords=["management override", "internal control", "fraud risk", "governance"],
        conclusion_template="The risk of management override of controls is assessed and mitigated through enhanced governance and monitoring.",
        reasoning_framework=(
            "1. Identify controls susceptible to management override.\n"
            "2. Assess the effectiveness of board and audit committee oversight.\n"
            "3. Review segregation of duties and approval hierarchies.\n"
            "4. Evaluate monitoring and exception reporting mechanisms.\n"
            "5. Test for evidence of override or circumvention.\n"
            "6. Recommend enhancements to reduce override risk."
        ),
        key_factors=[
            "Susceptibility of controls",
            "Board oversight",
            "Segregation of duties",
            "Exception monitoring"
        ],
        primary_authority=[
            "COSO Principle 10",
            "AICPA AU-C Section 240"
        ],
        burden_holder="Management",
        adversary_position="Controls are easily overridden by management.",
        counter_arguments=[
            "No independent oversight.",
            "Override is not detected.",
            "Segregation of duties is weak."
        ],
        resolution_strategy="Strengthen oversight and implement automated controls.",
        entity_scope="Enterprise-wide",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="COSO Principle 10"
    ),
    DoctrineBlock(
        topic="Continuous Monitoring and Assurance",
        keywords=["continuous monitoring", "assurance", "data analytics", "internal audit"],
        conclusion_template="Continuous monitoring and assurance activities are implemented to provide timely detection of control failures.",
        reasoning_framework=(
            "1. Identify key risk indicators and control points for continuous monitoring.\n"
            "2. Implement automated data analytics and exception reporting.\n"
            "3. Assign responsibility for monitoring and follow-up.\n"
            "4. Integrate monitoring results into risk assessments and audit planning.\n"
            "5. Document monitoring activities and outcomes."
        ),
        key_factors=[
            "Key risk indicators",
            "Automation and analytics",
            "Responsibility assignment",
            "Integration with risk assessment"
        ],
        primary_authority=[
            "IIA Practice Guide: Continuous Auditing",
            "COSO Monitoring Activities"
        ],
        burden_holder="Internal Audit/Management",
        adversary_position="Monitoring is ad hoc or not integrated.",
        counter_arguments=[
            "No automation or analytics.",
            "Monitoring results not used.",
            "Responsibilities are unclear."
        ],
        resolution_strategy="Automate monitoring and integrate with risk management.",
        entity_scope="Enterprise-wide",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="IIA Practice Guide"
    ),
    DoctrineBlock(
        topic="Whistleblower Program Effectiveness",
        keywords=["whistleblower", "hotline", "reporting", "retaliation", "program effectiveness"],
        conclusion_template="The whistleblower program is evaluated for effectiveness in encouraging reporting and protecting against retaliation.",
        reasoning_framework=(
            "1. Assess accessibility and awareness of whistleblower channels.\n"
            "2. Review policies prohibiting retaliation and protecting anonymity.\n"
            "3. Evaluate investigation and follow-up processes.\n"
            "4. Benchmark against regulatory requirements (e.g., SOX, Dodd-Frank).\n"
            "5. Document program outcomes and improvements."
        ),
        key_factors=[
            "Channel accessibility",
            "Anti-retaliation policies",
            "Investigation process",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SOX Section 301",
            "Dodd-Frank Act"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Program is not trusted or used by employees.",
        counter_arguments=[
            "Reports are not investigated.",
            "Retaliation occurs.",
            "Channels are not anonymous."
        ],
        resolution_strategy="Enhance awareness, protect anonymity, and monitor outcomes.",
        entity_scope="All employees",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SOX Section 301"
    ),
    DoctrineBlock(
        topic="Vendor and Third-Party Risk Management",
        keywords=["vendor risk", "third-party", "due diligence", "contract management", "monitoring"],
        conclusion_template="Vendor and third-party risk management processes are evaluated for adequacy in identifying, assessing, and mitigating risks.",
        reasoning_framework=(
            "1. Identify all vendors and third parties with access to critical systems or data.\n"
            "2. Conduct due diligence prior to onboarding.\n"
            "3. Assess contract terms for compliance and risk mitigation clauses.\n"
            "4. Monitor vendor performance and compliance.\n"
            "5. Document risk assessments and ongoing monitoring."
        ),
        key_factors=[
            "Vendor inventory",
            "Due diligence process",
            "Contract terms",
            "Ongoing monitoring"
        ],
        primary_authority=[
            "OCC Bulletin 2013-29",
            "FFIEC Guidance"
        ],
        burden_holder="Vendor Management Office",
        adversary_position="Vendor risks are not identified or managed.",
        counter_arguments=[
            "No due diligence performed.",
            "Contracts lack key clauses.",
            "Monitoring is not ongoing."
        ],
        resolution_strategy="Enhance due diligence and contract management.",
        entity_scope="All third-party relationships",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="OCC Bulletin 2013-29"
    ),
    DoctrineBlock(
        topic="Data Privacy and Protection Compliance",
        keywords=["data privacy", "protection", "GDPR", "CCPA", "personal data"],
        conclusion_template="Data privacy and protection controls are assessed for compliance with applicable regulations (e.g., GDPR, CCPA).",
        reasoning_framework=(
            "1. Identify personal data collected, processed, and stored.\n"
            "2. Assess controls for data minimization, access, and security.\n"
            "3. Review policies for data subject rights and breach notification.\n"
            "4. Benchmark against regulatory requirements and best practices.\n"
            "5. Document compliance gaps and recommend remediation."
        ),
        key_factors=[
            "Personal data inventory",
            "Access controls",
            "Data subject rights",
            "Breach notification"
        ],
        primary_authority=[
            "GDPR",
            "CCPA",
            "NIST Privacy Framework"
        ],
        burden_holder="Data Protection Officer",
        adversary_position="Controls are insufficient for regulatory compliance.",
        counter_arguments=[
            "No data inventory.",
            "Access is not restricted.",
            "No breach notification process."
        ],
        resolution_strategy="Implement comprehensive privacy controls and monitor compliance.",
        entity_scope="All personal data processing",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="GDPR Article 32"
    ),
    DoctrineBlock(
        topic="Incident Response and Reporting",
        keywords=["incident response", "reporting", "security incident", "breach", "escalation"],
        conclusion_template="Incident response and reporting processes are evaluated for effectiveness in timely detection, escalation, and resolution.",
        reasoning_framework=(
            "1. Review incident response policies and procedures.\n"
            "2. Assess incident detection, escalation, and communication protocols.\n"
            "3. Evaluate incident investigation and root cause analysis.\n"
            "4. Benchmark against regulatory requirements and best practices.\n"
            "5. Document incident outcomes and lessons learned."
        ),
        key_factors=[
            "Incident detection",
            "Escalation protocols",
            "Investigation process",
            "Regulatory reporting"
        ],
        primary_authority=[
            "NIST SP 800-61",
            "GDPR Article 33"
        ],
        burden_holder="Incident Response Team",
        adversary_position="Incidents are not detected or reported timely.",
        counter_arguments=[
            "No formal response plan.",
            "Escalation is unclear.",
            "Lessons learned are not documented."
        ],
        resolution_strategy="Formalize response plan and conduct regular training.",
        entity_scope="All business units",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="NIST SP 800-61"
    ),
    DoctrineBlock(
        topic="Policy and Procedure Management",
        keywords=["policy management", "procedure", "document control", "review", "approval"],
        conclusion_template="Policy and procedure management processes are evaluated for adequacy in ensuring current, approved, and communicated controls.",
        reasoning_framework=(
            "1. Inventory all policies and procedures.\n"
            "2. Assess document control, versioning, and approval processes.\n"
            "3. Review periodic review and update schedules.\n"
            "4. Evaluate communication and training on policies.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Policy inventory",
            "Version control",
            "Approval process",
            "Communication and training"
        ],
        primary_authority=[
            "COSO Control Activities",
            "IIA Standards"
        ],
        burden_holder="Policy Owner",
        adversary_position="Policies are outdated or not communicated.",
        counter_arguments=[
            "No version control.",
            "Approval is informal.",
            "Employees are unaware of policies."
        ],
        resolution_strategy="Implement document control and regular reviews.",
        entity_scope="All policies and procedures",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="COSO Control Activities"
    ),
    DoctrineBlock(
        topic="Training and Awareness Programs",
        keywords=["training", "awareness", "compliance training", "employee education"],
        conclusion_template="Training and awareness programs are assessed for adequacy in communicating compliance obligations and risks.",
        reasoning_framework=(
            "1. Review training curriculum and frequency.\n"
            "2. Assess participation rates and completion tracking.\n"
            "3. Evaluate training effectiveness through testing and feedback.\n"
            "4. Benchmark against regulatory requirements.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Curriculum coverage",
            "Participation tracking",
            "Effectiveness assessment",
            "Regulatory alignment"
        ],
        primary_authority=[
            "Federal Sentencing Guidelines",
            "DOJ Guidance"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Training is not risk-based or not completed.",
        counter_arguments=[
            "Low participation rates.",
            "No effectiveness testing.",
            "Curriculum is outdated."
        ],
        resolution_strategy="Update curriculum and monitor participation.",
        entity_scope="All employees",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Federal Sentencing Guidelines"
    ),
    DoctrineBlock(
        topic="Records Retention and Destruction",
        keywords=["records retention", "destruction", "document management", "compliance"],
        conclusion_template="Records retention and destruction practices are evaluated for compliance with legal and regulatory requirements.",
        reasoning_framework=(
            "1. Review records retention schedules and policies.\n"
            "2. Assess compliance with legal and regulatory retention periods.\n"
            "3. Evaluate secure destruction processes.\n"
            "4. Benchmark against industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Retention schedules",
            "Legal/regulatory requirements",
            "Destruction process",
            "Policy compliance"
        ],
        primary_authority=[
            "Sarbanes-Oxley Act",
            "SEC Rule 17a-4"
        ],
        burden_holder="Records Manager",
        adversary_position="Records are not retained or destroyed per requirements.",
        counter_arguments=[
            "Retention periods are not followed.",
            "Destruction is not secure.",
            "Policy is not communicated."
        ],
        resolution_strategy="Update policies and monitor compliance.",
        entity_scope="All records",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="SEC Rule 17a-4"
    ),
    DoctrineBlock(
        topic="Conflict of Interest Management",
        keywords=["conflict of interest", "disclosure", "policy", "monitoring"],
        conclusion_template="Conflict of interest management processes are evaluated for effectiveness in identifying and mitigating conflicts.",
        reasoning_framework=(
            "1. Review conflict of interest policy and disclosure process.\n"
            "2. Assess monitoring and investigation of disclosed conflicts.\n"
            "3. Evaluate training and awareness efforts.\n"
            "4. Benchmark against regulatory requirements.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Policy and disclosure process",
            "Monitoring and investigation",
            "Training and awareness",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SEC Rules",
            "IIA Code of Ethics"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Conflicts are not disclosed or managed.",
        counter_arguments=[
            "No disclosure process.",
            "Monitoring is ineffective.",
            "Policy is not communicated."
        ],
        resolution_strategy="Enhance disclosure and monitoring processes.",
        entity_scope="All employees and directors",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SEC Rule 17j-1"
    ),
    DoctrineBlock(
        topic="Ethics and Code of Conduct Enforcement",
        keywords=["ethics", "code of conduct", "enforcement", "discipline"],
        conclusion_template="Ethics and code of conduct enforcement is evaluated for effectiveness in promoting ethical behavior and addressing violations.",
        reasoning_framework=(
            "1. Review code of conduct and disciplinary policies.\n"
            "2. Assess communication and training on ethical standards.\n"
            "3. Evaluate enforcement and disciplinary actions for violations.\n"
            "4. Benchmark against regulatory and industry standards.\n"
            "5. Document outcomes and recommend improvements."
        ),
        key_factors=[
            "Code of conduct",
            "Training and communication",
            "Enforcement actions",
            "Disciplinary process"
        ],
        primary_authority=[
            "IIA Code of Ethics",
            "Federal Sentencing Guidelines"
        ],
        burden_holder="Management",
        adversary_position="Ethics violations are not addressed.",
        counter_arguments=[
            "Discipline is inconsistent.",
            "Training is not conducted.",
            "Code is not communicated."
        ],
        resolution_strategy="Reinforce training and consistent enforcement.",
        entity_scope="All employees",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="IIA Code of Ethics"
    ),
    DoctrineBlock(
        topic="Fraud Risk Assessment",
        keywords=["fraud risk", "assessment", "anti-fraud controls", "detection"],
        conclusion_template="Fraud risk assessment processes are evaluated for adequacy in identifying and mitigating fraud risks.",
        reasoning_framework=(
            "1. Identify inherent and residual fraud risks.\n"
            "2. Assess anti-fraud controls and monitoring activities.\n"
            "3. Review training and awareness efforts.\n"
            "4. Benchmark against COSO and regulatory guidance.\n"
            "5. Document findings and recommend improvements."
        ),
        key_factors=[
            "Fraud risk identification",
            "Anti-fraud controls",
            "Monitoring activities",
            "Training and awareness"
        ],
        primary_authority=[
            "COSO Fraud Risk Management Guide",
            "AICPA AU-C Section 240"
        ],
        burden_holder="Management",
        adversary_position="Fraud risks are not assessed or mitigated.",
        counter_arguments=[
            "No fraud risk assessment.",
            "Controls are ineffective.",
            "Training is not conducted."
        ],
        resolution_strategy="Conduct regular fraud risk assessments and enhance controls.",
        entity_scope="All business units",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="COSO Fraud Risk Guide"
    ),
    DoctrineBlock(
        topic="Board and Committee Oversight",
        keywords=["board oversight", "committee", "governance", "risk management"],
        conclusion_template="Board and committee oversight is evaluated for effectiveness in governing risk and compliance activities.",
        reasoning_framework=(
            "1. Review board and committee charters and meeting minutes.\n"
            "2. Assess frequency and quality of risk and compliance reporting.\n"
            "3. Evaluate board engagement and challenge.\n"
            "4. Benchmark against regulatory expectations.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Charters and meeting minutes",
            "Reporting quality",
            "Board engagement",
            "Regulatory expectations"
        ],
        primary_authority=[
            "OCC Heightened Standards",
            "FFIEC Guidance"
        ],
        burden_holder="Board of Directors",
        adversary_position="Oversight is ineffective or not documented.",
        counter_arguments=[
            "Charters are outdated.",
            "Reporting is infrequent.",
            "Board is not engaged."
        ],
        resolution_strategy="Update charters and enhance reporting.",
        entity_scope="Board and committees",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="OCC Heightened Standards"
    ),
    DoctrineBlock(
        topic="Internal Audit Independence and Objectivity",
        keywords=["internal audit", "independence", "objectivity", "assurance"],
        conclusion_template="Internal audit independence and objectivity are evaluated for compliance with IIA Standards.",
        reasoning_framework=(
            "1. Review reporting lines and organizational structure.\n"
            "2. Assess auditor assignments for conflicts of interest.\n"
            "3. Evaluate policies supporting independence and objectivity.\n"
            "4. Benchmark against IIA Standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Reporting lines",
            "Assignment conflicts",
            "Independence policies",
            "IIA Standards"
        ],
        primary_authority=[
            "IIA Standard 1100",
            "IIA Code of Ethics"
        ],
        burden_holder="Chief Audit Executive",
        adversary_position="Internal audit is not independent.",
        counter_arguments=[
            "Reports to management, not board.",
            "Assignments create conflicts.",
            "Policies are not enforced."
        ],
        resolution_strategy="Strengthen reporting lines and enforce policies.",
        entity_scope="Internal audit function",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IIA Standard 1100"
    ),
    DoctrineBlock(
        topic="Quality Assurance and Improvement Program (QAIP)",
        keywords=["QAIP", "quality assurance", "improvement", "internal audit"],
        conclusion_template="The Quality Assurance and Improvement Program (QAIP) is evaluated for compliance with IIA Standards and effectiveness in driving improvement.",
        reasoning_framework=(
            "1. Review QAIP policies and procedures.\n"
            "2. Assess internal and external quality assessments.\n"
            "3. Evaluate corrective actions for identified deficiencies.\n"
            "4. Benchmark against IIA Standards.\n"
            "5. Document outcomes and recommend improvements."
        ),
        key_factors=[
            "QAIP policies",
            "Internal/external assessments",
            "Corrective actions",
            "IIA Standards"
        ],
        primary_authority=[
            "IIA Standard 1300",
            "IIA Practice Guide"
        ],
        burden_holder="Chief Audit Executive",
        adversary_position="QAIP is not implemented or effective.",
        counter_arguments=[
            "No external assessments.",
            "Corrective actions are not tracked.",
            "QAIP is not documented."
        ],
        resolution_strategy="Implement QAIP and monitor corrective actions.",
        entity_scope="Internal audit function",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IIA Standard 1300"
    ),
    DoctrineBlock(
        topic="Regulatory Reporting and Disclosure",
        keywords=["regulatory reporting", "disclosure", "filing", "compliance"],
        conclusion_template="Regulatory reporting and disclosure processes are evaluated for accuracy, timeliness, and completeness.",
        reasoning_framework=(
            "1. Identify all regulatory reporting and disclosure obligations.\n"
            "2. Review processes for data collection, validation, and filing.\n"
            "3. Assess accuracy and timeliness of reports.\n"
            "4. Benchmark against regulatory requirements.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Obligation inventory",
            "Data validation",
            "Timeliness",
            "Regulatory requirements"
        ],
        primary_authority=[
            "SEC Rules",
            "OCC Guidance"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Reports are inaccurate or late.",
        counter_arguments=[
            "Obligations are not identified.",
            "Data is not validated.",
            "Deadlines are missed."
        ],
        resolution_strategy="Enhance reporting controls and monitor deadlines.",
        entity_scope="All regulatory filings",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SEC Rule 13a-15"
    ),
    DoctrineBlock(
        topic="Business Continuity and Disaster Recovery",
        keywords=["business continuity", "disaster recovery", "BCP", "DRP", "resilience"],
        conclusion_template="Business continuity and disaster recovery plans are evaluated for adequacy in ensuring operational resilience.",
        reasoning_framework=(
            "1. Review BCP and DRP documentation and testing schedules.\n"
            "2. Assess risk assessments and impact analyses.\n"
            "3. Evaluate plan activation and communication protocols.\n"
            "4. Benchmark against regulatory and industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Plan documentation",
            "Testing and exercises",
            "Impact analysis",
            "Communication protocols"
        ],
        primary_authority=[
            "FFIEC Business Continuity Handbook",
            "NIST SP 800-34"
        ],
        burden_holder="Business Continuity Manager",
        adversary_position="Plans are outdated or untested.",
        counter_arguments=[
            "No testing performed.",
            "Plans are not communicated.",
            "Impact analysis is missing."
        ],
        resolution_strategy="Update and test plans regularly.",
        entity_scope="All business units",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="FFIEC BCP Handbook"
    ),
    DoctrineBlock(
        topic="Information Security Governance",
        keywords=["information security", "governance", "cybersecurity", "policies"],
        conclusion_template="Information security governance is evaluated for adequacy in managing cybersecurity risks.",
        reasoning_framework=(
            "1. Review information security policies and governance structure.\n"
            "2. Assess risk assessments and security controls.\n"
            "3. Evaluate board and management oversight.\n"
            "4. Benchmark against regulatory and industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Security policies",
            "Risk assessments",
            "Governance structure",
            "Oversight"
        ],
        primary_authority=[
            "NIST Cybersecurity Framework",
            "FFIEC Guidance"
        ],
        burden_holder="CISO",
        adversary_position="Governance is weak or not documented.",
        counter_arguments=[
            "Policies are outdated.",
            "Oversight is ineffective.",
            "Risk assessments are not performed."
        ],
        resolution_strategy="Update policies and strengthen oversight.",
        entity_scope="All information assets",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="NIST CSF"
    ),
    DoctrineBlock(
        topic="Access Management and Segregation of Duties",
        keywords=["access management", "segregation of duties", "user access", "privileged access"],
        conclusion_template="Access management and segregation of duties controls are evaluated for adequacy in preventing unauthorized activities.",
        reasoning_framework=(
            "1. Review user access provisioning and deprovisioning processes.\n"
            "2. Assess segregation of duties for key processes.\n"
            "3. Evaluate privileged access controls and monitoring.\n"
            "4. Benchmark against regulatory and industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Access provisioning",
            "Segregation of duties",
            "Privileged access",
            "Monitoring"
        ],
        primary_authority=[
            "SOX Section 404",
            "NIST SP 800-53"
        ],
        burden_holder="IT Security",
        adversary_position="Access is not controlled or duties are not segregated.",
        counter_arguments=[
            "No access reviews.",
            "Segregation is not enforced.",
            "Privileged access is not monitored."
        ],
        resolution_strategy="Implement access reviews and automate controls.",
        entity_scope="All systems and processes",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="SOX Section 404"
    ),
    DoctrineBlock(
        topic="Model Risk Management",
        keywords=["model risk", "model validation", "model governance", "testing"],
        conclusion_template="Model risk management processes are evaluated for adequacy in identifying, assessing, and mitigating model risks.",
        reasoning_framework=(
            "1. Inventory all models used in decision-making.\n"
            "2. Assess model development, validation, and approval processes.\n"
            "3. Evaluate ongoing monitoring and performance testing.\n"
            "4. Benchmark against regulatory guidance.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Model inventory",
            "Validation process",
            "Performance testing",
            "Governance"
        ],
        primary_authority=[
            "OCC Bulletin 2011-12",
            "SR 11-7"
        ],
        burden_holder="Model Risk Manager",
        adversary_position="Models are not validated or monitored.",
        counter_arguments=[
            "No model inventory.",
            "Validation is not independent.",
            "Performance is not tested."
        ],
        resolution_strategy="Enhance validation and monitoring processes.",
        entity_scope="All models",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="OCC Bulletin 2011-12"
    ),
    DoctrineBlock(
        topic="Environmental, Social, and Governance (ESG) Compliance",
        keywords=["ESG", "environmental", "social", "governance", "sustainability"],
        conclusion_template="ESG compliance processes are evaluated for adequacy in meeting stakeholder and regulatory expectations.",
        reasoning_framework=(
            "1. Identify ESG reporting and compliance obligations.\n"
            "2. Assess policies and controls for environmental, social, and governance risks.\n"
            "3. Evaluate ESG data collection and reporting processes.\n"
            "4. Benchmark against industry standards and frameworks.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "ESG obligations",
            "Policies and controls",
            "Data collection",
            "Reporting"
        ],
        primary_authority=[
            "SASB Standards",
            "GRI Standards"
        ],
        burden_holder="ESG Officer",
        adversary_position="ESG risks are not managed or reported.",
        counter_arguments=[
            "No ESG policies.",
            "Data is not collected.",
            "Reporting is incomplete."
        ],
        resolution_strategy="Implement ESG controls and enhance reporting.",
        entity_scope="All business units",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="SASB Standards"
    ),
    DoctrineBlock(
        topic="Outsourcing and Cloud Risk Management",
        keywords=["outsourcing", "cloud", "risk management", "third-party", "SLA"],
        conclusion_template="Outsourcing and cloud risk management processes are evaluated for adequacy in managing third-party risks.",
        reasoning_framework=(
            "1. Identify all outsourced and cloud services.\n"
            "2. Assess due diligence and contract management processes.\n"
            "3. Evaluate ongoing monitoring and SLA compliance.\n"
            "4. Benchmark against regulatory and industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Outsourcing inventory",
            "Due diligence",
            "SLA compliance",
            "Ongoing monitoring"
        ],
        primary_authority=[
            "FFIEC Outsourcing Handbook",
            "NIST SP 800-144"
        ],
        burden_holder="Vendor Management Office",
        adversary_position="Outsourcing risks are not managed.",
        counter_arguments=[
            "No due diligence.",
            "SLAs are not enforced.",
            "Monitoring is not ongoing."
        ],
        resolution_strategy="Enhance due diligence and SLA monitoring.",
        entity_scope="All outsourced services",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="FFIEC Outsourcing Handbook"
    ),
    DoctrineBlock(
        topic="Financial Reporting Controls",
        keywords=["financial reporting", "internal controls", "SOX", "accuracy"],
        conclusion_template="Financial reporting controls are evaluated for adequacy in ensuring accurate and reliable financial statements.",
        reasoning_framework=(
            "1. Review key controls over financial reporting.\n"
            "2. Assess control design and operating effectiveness.\n"
            "3. Evaluate management review and oversight.\n"
            "4. Benchmark against SOX and industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Key controls",
            "Design and effectiveness",
            "Management oversight",
            "SOX compliance"
        ],
        primary_authority=[
            "SOX Section 404",
            "COSO Framework"
        ],
        burden_holder="CFO",
        adversary_position="Controls are ineffective or not documented.",
        counter_arguments=[
            "No evidence of control operation.",
            "Oversight is weak.",
            "Controls are not tested."
        ],
        resolution_strategy="Test controls and remediate deficiencies.",
        entity_scope="Financial reporting",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SOX Section 404"
    ),
    DoctrineBlock(
        topic="Anti-Money Laundering (AML) Compliance",
        keywords=["AML", "anti-money laundering", "compliance", "KYC", "monitoring"],
        conclusion_template="AML compliance processes are evaluated for adequacy in detecting and preventing money laundering.",
        reasoning_framework=(
            "1. Review AML policies and procedures.\n"
            "2. Assess customer due diligence (KYC) processes.\n"
            "3. Evaluate transaction monitoring and suspicious activity reporting.\n"
            "4. Benchmark against regulatory requirements.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "AML policies",
            "KYC processes",
            "Transaction monitoring",
            "Regulatory reporting"
        ],
        primary_authority=[
            "Bank Secrecy Act",
            "FinCEN Guidance"
        ],
        burden_holder="AML Officer",
        adversary_position="AML controls are ineffective.",
        counter_arguments=[
            "KYC is not performed.",
            "Monitoring is not automated.",
            "Reports are not filed."
        ],
        resolution_strategy="Enhance KYC and monitoring processes.",
        entity_scope="All customers and transactions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Bank Secrecy Act"
    ),
    DoctrineBlock(
        topic="Sanctions and OFAC Compliance",
        keywords=["sanctions", "OFAC", "compliance", "screening"],
        conclusion_template="Sanctions and OFAC compliance processes are evaluated for adequacy in screening and preventing prohibited transactions.",
        reasoning_framework=(
            "1. Review sanctions screening policies and procedures.\n"
            "2. Assess customer and transaction screening processes.\n"
            "3. Evaluate escalation and reporting protocols.\n"
            "4. Benchmark against OFAC and regulatory requirements.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Screening policies",
            "Customer/transaction screening",
            "Escalation protocols",
            "OFAC requirements"
        ],
        primary_authority=[
            "OFAC Regulations",
            "FinCEN Guidance"
        ],
        burden_holder="Sanctions Officer",
        adversary_position="Screening is incomplete or ineffective.",
        counter_arguments=[
            "No screening performed.",
            "Escalation is unclear.",
            "Policies are outdated."
        ],
        resolution_strategy="Automate screening and update policies.",
        entity_scope="All customers and transactions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OFAC Regulations"
    ),
    DoctrineBlock(
        topic="Customer Complaint Management",
        keywords=["customer complaint", "management", "tracking", "resolution"],
        conclusion_template="Customer complaint management processes are evaluated for adequacy in tracking, investigating, and resolving complaints.",
        reasoning_framework=(
            "1. Review complaint intake and tracking processes.\n"
            "2. Assess investigation and resolution protocols.\n"
            "3. Evaluate communication with complainants.\n"
            "4. Benchmark against regulatory requirements.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Intake and tracking",
            "Investigation protocols",
            "Communication",
            "Regulatory requirements"
        ],
        primary_authority=[
            "CFPB Guidance",
            "OCC Guidance"
        ],
        burden_holder="Customer Service Manager",
        adversary_position="Complaints are not tracked or resolved.",
        counter_arguments=[
            "No tracking system.",
            "Investigation is not documented.",
            "Complainants are not informed."
        ],
        resolution_strategy="Implement tracking and enhance communication.",
        entity_scope="All customer interactions",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="CFPB Guidance"
    ),
    DoctrineBlock(
        topic="Records of Processing Activities (RoPA) Compliance",
        keywords=["RoPA", "records of processing", "GDPR", "data inventory"],
        conclusion_template="Records of processing activities are evaluated for compliance with GDPR Article 30 requirements.",
        reasoning_framework=(
            "1. Inventory all processing activities involving personal data.\n"
            "2. Document purposes, categories, recipients, and retention periods.\n"
            "3. Assess controls for maintaining and updating records.\n"
            "4. Benchmark against GDPR requirements.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Processing activity inventory",
            "Documentation",
            "Update controls",
            "GDPR compliance"
        ],
        primary_authority=[
            "GDPR Article 30",
            "EDPB Guidelines"
        ],
        burden_holder="Data Protection Officer",
        adversary_position="Records are incomplete or not maintained.",
        counter_arguments=[
            "No inventory exists.",
            "Records are outdated.",
            "Controls are not enforced."
        ],
        resolution_strategy="Implement inventory and update controls.",
        entity_scope="All personal data processing",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="GDPR Article 30"
    ),
    DoctrineBlock(
        topic="Physical Security Controls",
        keywords=["physical security", "access controls", "facility security", "monitoring"],
        conclusion_template="Physical security controls are evaluated for adequacy in protecting assets and personnel.",
        reasoning_framework=(
            "1. Review facility access controls and monitoring systems.\n"
            "2. Assess visitor management and badge protocols.\n"
            "3. Evaluate incident response for physical security breaches.\n"
            "4. Benchmark against industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Access controls",
            "Visitor management",
            "Incident response",
            "Monitoring systems"
        ],
        primary_authority=[
            "NIST SP 800-53",
            "ISO 27001"
        ],
        burden_holder="Facilities Manager",
        adversary_position="Physical security is weak or not enforced.",
        counter_arguments=[
            "Access is not controlled.",
            "Visitor logs are not maintained.",
            "Incidents are not reported."
        ],
        resolution_strategy="Enhance controls and conduct regular reviews.",
        entity_scope="All facilities",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="NIST SP 800-53"
    ),
    DoctrineBlock(
        topic="Change Management Controls",
        keywords=["change management", "controls", "IT change", "approval", "testing"],
        conclusion_template="Change management controls are evaluated for adequacy in managing IT and operational changes.",
        reasoning_framework=(
            "1. Review change management policies and procedures.\n"
            "2. Assess approval, testing, and documentation processes.\n"
            "3. Evaluate segregation of duties and emergency changes.\n"
            "4. Benchmark against industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Change approval",
            "Testing and documentation",
            "Segregation of duties",
            "Emergency changes"
        ],
        primary_authority=[
            "ITIL Change Management",
            "NIST SP 800-128"
        ],
        burden_holder="IT Change Manager",
        adversary_position="Changes are not controlled or documented.",
        counter_arguments=[
            "No approval process.",
            "Testing is not performed.",
            "Emergency changes are not tracked."
        ],
        resolution_strategy="Formalize approval and testing processes.",
        entity_scope="All IT and operational changes",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="ITIL Change Management"
    ),
    DoctrineBlock(
        topic="Key Risk Indicator (KRI) Framework",
        keywords=["KRI", "key risk indicator", "risk monitoring", "metrics"],
        conclusion_template="The Key Risk Indicator (KRI) framework is evaluated for adequacy in monitoring and reporting risk exposures.",
        reasoning_framework=(
            "1. Identify and define KRIs for key risks.\n"
            "2. Assess data sources and calculation methodologies.\n"
            "3. Evaluate thresholds, escalation, and reporting protocols.\n"
            "4. Benchmark against industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "KRI definition",
            "Data sources",
            "Thresholds and escalation",
            "Reporting"
        ],
        primary_authority=[
            "COSO ERM Framework",
            "Basel Committee Guidance"
        ],
        burden_holder="Risk Management",
        adversary_position="KRIs are not defined or monitored.",
        counter_arguments=[
            "No KRI framework.",
            "Data is unreliable.",
            "Escalation is unclear."
        ],
        resolution_strategy="Implement KRI framework and automate reporting.",
        entity_scope="All risk areas",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="COSO ERM Framework"
    ),
    DoctrineBlock(
        topic="Internal Control Self-Assessment (ICSA)",
        keywords=["ICSA", "internal control", "self-assessment", "testing"],
        conclusion_template="Internal Control Self-Assessment (ICSA) processes are evaluated for adequacy in identifying and mitigating control weaknesses.",
        reasoning_framework=(
            "1. Review ICSA policies and procedures.\n"
            "2. Assess participation and coverage of key controls.\n"
            "3. Evaluate testing and documentation processes.\n"
            "4. Benchmark against COSO and industry standards.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "ICSA policies",
            "Participation and coverage",
            "Testing and documentation",
            "COSO standards"
        ],
        primary_authority=[
            "COSO Framework",
            "IIA Practice Guide"
        ],
        burden_holder="Process Owner",
        adversary_position="ICSA is not performed or documented.",
        counter_arguments=[
            "Participation is low.",
            "Testing is not performed.",
            "Documentation is incomplete."
        ],
        resolution_strategy="Enhance participation and testing coverage.",
        entity_scope="All business units",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="COSO Framework"
    ),
    DoctrineBlock(
        topic="Remediation of Regulatory Findings",
        keywords=["remediation", "regulatory findings", "tracking", "corrective action"],
        conclusion_template="Remediation processes for regulatory findings are evaluated for adequacy in ensuring timely and effective closure.",
        reasoning_framework=(
            "1. Review tracking and escalation processes for regulatory findings.\n"
            "2. Assess assignment of responsibility and deadlines.\n"
            "3. Evaluate validation and closure protocols.\n"
            "4. Benchmark against regulatory expectations.\n"
            "5. Document gaps and recommend improvements."
        ),
        key_factors=[
            "Tracking and escalation",
            "Responsibility assignment",
            "Validation and closure",
            "Regulatory expectations"
        ],
        primary_authority=[
            "OCC Heightened Standards",
            "FFIEC Guidance"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Findings are not remediated timely.",
        counter_arguments=[
            "Tracking is informal.",
            "Deadlines are missed.",
            "Validation is not performed."
        ],
        resolution_strategy="Formalize tracking and validation processes.",
        entity_scope="All regulatory findings",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="OCC Heightened Standards"
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