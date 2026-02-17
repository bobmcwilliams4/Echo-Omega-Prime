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
        topic="General Duty Clause 5(a)(1) Application",
        keywords=["general duty clause", "5(a)(1)", "hazard", "recognized", "serious", "feasible", "abatement"],
        conclusion_template="The employer violated the General Duty Clause if a recognized hazard likely to cause death or serious harm existed, the employer or industry recognized the hazard, feasible means to abate existed, and the employer failed to implement them.",
        reasoning_framework=(
            "The General Duty Clause (29 U.S.C. § 654(a)(1)) requires employers to furnish employment free from recognized hazards likely to cause death or serious physical harm. "
            "To establish a violation, OSHA must prove: (1) a condition or activity in the workplace presented a hazard; (2) the hazard was recognized by the employer or industry; "
            "(3) the hazard was likely to cause death or serious harm; (4) feasible and useful methods to correct the hazard were available. "
            "Recognition can be established by employer knowledge, industry standards, or common sense. Feasibility is based on technological and economic capability. "
            "The employer may defend by showing lack of recognition, infeasibility, or employee misconduct. The doctrine is applied case-by-case, considering the specific workplace context."
        ),
        key_factors=[
            "Existence of a hazardous condition",
            "Recognition of the hazard",
            "Likelihood of death or serious harm",
            "Feasibility of abatement methods",
            "Employer's knowledge or constructive knowledge"
        ],
        primary_authority=[
            "29 U.S.C. § 654(a)(1) (OSH Act General Duty Clause)",
            "OSHRC case law (e.g., National Realty & Construction Co., Inc. v. OSHRC, 489 F.2d 1257 (D.C. Cir. 1973))"
        ],
        burden_holder="OSHA",
        adversary_position="No recognized hazard or infeasibility of abatement",
        counter_arguments=[
            "Hazard not recognized by industry or employer",
            "No feasible abatement method exists",
            "Employee misconduct was the sole cause",
            "Hazard did not pose risk of death or serious harm"
        ],
        resolution_strategy="Evaluate evidence of hazard recognition, feasibility, and abatement; assess employer's safety program and industry standards.",
        entity_scope="All employers under OSH Act jurisdiction",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="National Realty & Construction Co., Inc. v. OSHRC (1973)"
    ),
    DoctrineBlock(
        topic="PSM 29 CFR 1910.119 Covered Processes Threshold",
        keywords=["PSM", "process safety management", "threshold quantity", "highly hazardous chemicals", "covered process"],
        conclusion_template="A process is covered by PSM if it involves a threshold quantity or more of a listed highly hazardous chemical as specified in 29 CFR 1910.119 Appendix A.",
        reasoning_framework=(
            "The Process Safety Management (PSM) standard (29 CFR 1910.119) applies to processes involving highly hazardous chemicals (HHCs) at or above specified threshold quantities (TQs). "
            "Appendix A lists HHCs and their TQs. Coverage is determined by aggregating all vessels, interconnected piping, and storage within proximity and under control of the employer. "
            "Mixtures are covered if the total quantity of HHCs meets or exceeds the TQ, considering the concentration. Certain exemptions apply (e.g., retail facilities, oil/gas well drilling). "
            "Employers must assess inventories and process boundaries to determine coverage. Failure to recognize coverage may result in citation."
        ),
        key_factors=[
            "Presence of listed HHCs",
            "Total quantity on-site",
            "Process boundaries and aggregation",
            "Mixture concentrations",
            "Applicability of exemptions"
        ],
        primary_authority=[
            "29 CFR 1910.119",
            "OSHA PSM Standard Interpretations"
        ],
        burden_holder="OSHA",
        adversary_position="Process does not meet threshold or is exempt",
        counter_arguments=[
            "Quantity below threshold",
            "Chemical not listed in Appendix A",
            "Exemption applies (e.g., retail, oil/gas production)",
            "Process boundaries incorrectly defined"
        ],
        resolution_strategy="Review chemical inventories, process diagrams, and applicability of exemptions; consult Appendix A and OSHA letters of interpretation.",
        entity_scope="Employers with processes involving HHCs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OSHA CPL 02-02-045 (PSM Covered Process Guidance)"
    ),
    DoctrineBlock(
        topic="Lockout/Tagout 1910.147 Energy Control Procedures",
        keywords=["lockout", "tagout", "LOTO", "energy control", "servicing", "maintenance", "hazardous energy"],
        conclusion_template="Employers must establish and implement written energy control procedures for servicing and maintenance of machines and equipment where unexpected energization could cause injury.",
        reasoning_framework=(
            "29 CFR 1910.147 requires employers to develop, document, and utilize procedures for controlling hazardous energy during servicing and maintenance. "
            "Procedures must outline the scope, purpose, authorization, and steps for shutting down, isolating, blocking, and securing machines. "
            "Affected employees must be trained, and periodic inspections conducted. "
            "Exceptions exist for cord-and-plug equipment and minor tool changes if alternative protection is provided. "
            "Failure to implement effective procedures or train employees constitutes a violation."
        ),
        key_factors=[
            "Existence of hazardous energy sources",
            "Written energy control procedures",
            "Employee training and authorization",
            "Periodic inspections",
            "Applicability of exceptions"
        ],
        primary_authority=[
            "29 CFR 1910.147",
            "OSHA Directive CPL 02-00-147"
        ],
        burden_holder="OSHA",
        adversary_position="No hazardous energy or exception applies",
        counter_arguments=[
            "Task does not involve hazardous energy",
            "Cord-and-plug exemption applies",
            "Minor servicing exception applies",
            "Procedures are adequate and implemented"
        ],
        resolution_strategy="Review written procedures, training records, and applicability of exceptions; interview employees.",
        entity_scope="All employers with machines/equipment subject to servicing",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-00-147"
    ),
    DoctrineBlock(
        topic="Confined Space Entry 1910.146 Permit Requirements",
        keywords=["confined space", "permit-required", "entry", "hazard", "atmospheric testing", "rescue"],
        conclusion_template="Entry into a permit-required confined space is prohibited unless the employer implements a written permit program meeting 1910.146 requirements.",
        reasoning_framework=(
            "29 CFR 1910.146 defines permit-required confined spaces (PRCS) as spaces with one or more hazards such as hazardous atmosphere, engulfment, or configuration hazards. "
            "Employers must develop and implement a written permit space program, including atmospheric testing, entry permits, training, and rescue provisions. "
            "Entry is prohibited without a permit unless the space is reclassified as non-permit. "
            "Failure to follow permit procedures or provide rescue capability is a serious violation. "
            "Employers may argue the space is not permit-required or that alternate entry procedures apply."
        ),
        key_factors=[
            "Presence of permit-required hazards",
            "Written permit space program",
            "Atmospheric testing and monitoring",
            "Entry permits and authorization",
            "Rescue and emergency provisions"
        ],
        primary_authority=[
            "29 CFR 1910.146",
            "OSHA Letters of Interpretation"
        ],
        burden_holder="OSHA",
        adversary_position="Space is not permit-required or alternate procedures apply",
        counter_arguments=[
            "Space does not meet PRCS definition",
            "Hazards eliminated or controlled",
            "Alternate entry procedures used",
            "No entry occurred"
        ],
        resolution_strategy="Inspect space characteristics, review written program, and evaluate entry records.",
        entity_scope="Employers with confined spaces",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OSHA CPL 02-00-100"
    ),
    DoctrineBlock(
        topic="Fall Protection 1926.501 Construction Standards",
        keywords=["fall protection", "construction", "1926.501", "elevated work", "guardrails", "personal fall arrest"],
        conclusion_template="Employers must provide fall protection for employees exposed to fall hazards at heights specified in 1926.501, using guardrails, safety nets, or personal fall arrest systems.",
        reasoning_framework=(
            "29 CFR 1926.501 requires employers to protect construction workers from falls at elevations of 6 feet or more above lower levels. "
            "Acceptable methods include guardrail systems, safety net systems, or personal fall arrest systems. "
            "Specific requirements apply to various activities (e.g., leading edge work, roofing, scaffolds). "
            "Employers must assess worksite hazards and select appropriate protection. "
            "Failure to provide adequate protection or train employees is a serious violation."
        ),
        key_factors=[
            "Employee exposure to fall hazards",
            "Height above lower level",
            "Type of work activity",
            "Provision and use of protection systems",
            "Employee training"
        ],
        primary_authority=[
            "29 CFR 1926.501",
            "OSHA Fall Protection Standard Interpretations"
        ],
        burden_holder="OSHA",
        adversary_position="No exposure or exception applies",
        counter_arguments=[
            "No exposure to fall hazard",
            "Work not covered by standard",
            "Protection system infeasible",
            "Employee misconduct"
        ],
        resolution_strategy="Review worksite conditions, interview employees, and examine training records.",
        entity_scope="Construction employers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Bratton Corp., OSHRC Docket No. 88-2903"
    ),
    DoctrineBlock(
        topic="HazCom 2012 GHS SDS and Labeling Requirements",
        keywords=["hazcom", "hazard communication", "GHS", "SDS", "labeling", "chemical safety"],
        conclusion_template="Employers must ensure all hazardous chemicals are labeled and Safety Data Sheets (SDS) are available and accessible to employees in accordance with HazCom 2012.",
        reasoning_framework=(
            "The Hazard Communication Standard (29 CFR 1910.1200) aligns with the Globally Harmonized System (GHS) and requires employers to label containers of hazardous chemicals, "
            "maintain Safety Data Sheets (SDS) for each chemical, and provide employee training. "
            "Labels must include product identifier, signal word, hazard statements, pictograms, and supplier information. "
            "SDS must follow a 16-section format and be readily accessible. "
            "Employers are responsible for ensuring compliance, even for chemicals received from suppliers."
        ),
        key_factors=[
            "Presence of hazardous chemicals",
            "Labeling of containers",
            "Availability and accessibility of SDS",
            "Employee training",
            "Supplier information"
        ],
        primary_authority=[
            "29 CFR 1910.1200",
            "OSHA HazCom 2012 Guidance"
        ],
        burden_holder="OSHA",
        adversary_position="No hazardous chemicals or labeling/SDS not required",
        counter_arguments=[
            "Chemical not hazardous",
            "Labeling/SDS requirements not triggered",
            "SDS not available from supplier",
            "Employee not exposed"
        ],
        resolution_strategy="Review chemical inventory, inspect labels and SDS, and interview employees.",
        entity_scope="All employers with hazardous chemicals",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-02-079"
    ),
    DoctrineBlock(
        topic="OSHA 300 Log Recordkeeping Requirements",
        keywords=["recordkeeping", "OSHA 300", "injury", "illness", "log", "reporting"],
        conclusion_template="Employers must record work-related injuries and illnesses on the OSHA 300 Log within seven days of learning of the case, as required by 29 CFR 1904.",
        reasoning_framework=(
            "29 CFR 1904 requires employers to record work-related injuries and illnesses that meet general recording criteria (e.g., medical treatment, restricted work, days away) on the OSHA 300 Log. "
            "Cases must be entered within seven calendar days of learning of the event. "
            "Certain low-hazard industries are partially exempt. "
            "Employers must also prepare the OSHA 301 Incident Report and post the 300A Summary annually. "
            "Failure to record, late recording, or inaccurate records may result in citation."
        ),
        key_factors=[
            "Employer coverage under Part 1904",
            "Work-relatedness of injury/illness",
            "General recording criteria met",
            "Timeliness and accuracy of records",
            "Availability for inspection"
        ],
        primary_authority=[
            "29 CFR 1904",
            "OSHA Recordkeeping Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Case not recordable or employer exempt",
        counter_arguments=[
            "Injury/illness not work-related",
            "Does not meet recording criteria",
            "Employer is partially exempt",
            "Case was recorded timely and accurately"
        ],
        resolution_strategy="Review injury/illness records, OSHA 300 Log, and supporting documentation.",
        entity_scope="Employers with 11+ employees (unless exempt)",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OSHA Recordkeeping Standard Interpretations"
    ),
    DoctrineBlock(
        topic="Citation Classifications and Penalty Calculations",
        keywords=["citation", "classification", "penalty", "serious", "willful", "repeat", "other-than-serious"],
        conclusion_template="OSHA classifies violations as serious, willful, repeat, or other-than-serious and calculates penalties based on statutory factors including gravity, size, history, and good faith.",
        reasoning_framework=(
            "OSHA citations are classified based on the nature of the violation: serious, willful, repeat, or other-than-serious. "
            "A serious violation exists if there is a substantial probability of death or serious harm. "
            "Willful violations involve intentional disregard or plain indifference. "
            "Repeat violations are similar to previous violations. "
            "Penalties are calculated considering the gravity of the violation, employer size, history of violations, and good faith efforts. "
            "Maximum and minimum penalties are set by statute and adjusted annually for inflation."
        ),
        key_factors=[
            "Nature and gravity of violation",
            "Employer knowledge and intent",
            "History of prior violations",
            "Employer size and good faith",
            "Statutory penalty limits"
        ],
        primary_authority=[
            "29 U.S.C. § 666",
            "OSHA Field Operations Manual"
        ],
        burden_holder="OSHA",
        adversary_position="Violation not serious/willful/repeat; penalty excessive",
        counter_arguments=[
            "Violation is not serious or willful",
            "No prior similar violations",
            "Penalty calculation errors",
            "Good faith not considered"
        ],
        resolution_strategy="Review citation documentation, employer history, and penalty calculation worksheets.",
        entity_scope="All employers cited by OSHA",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHRC case law on citation classification"
    ),
    DoctrineBlock(
        topic="Multi-Employer Worksite Citation Policy",
        keywords=["multi-employer", "worksite", "controlling employer", "creating employer", "exposing employer", "correcting employer"],
        conclusion_template="OSHA may cite multiple employers at a worksite if they create, expose, correct, or control a hazardous condition, per the multi-employer citation policy.",
        reasoning_framework=(
            "OSHA's multi-employer citation policy allows citations to be issued to more than one employer at a worksite. "
            "Employers are classified as creating, exposing, correcting, or controlling employers. "
            "A creating employer causes a hazard; an exposing employer's employees are exposed; a correcting employer is responsible for hazard correction; a controlling employer has general supervisory authority. "
            "Each employer's role and efforts to meet obligations are evaluated. "
            "The doctrine is especially relevant in construction and multi-contractor settings."
        ),
        key_factors=[
            "Employer's role at the worksite",
            "Employee exposure to hazards",
            "Authority and contractual obligations",
            "Efforts to correct or prevent hazards",
            "Communication among employers"
        ],
        primary_authority=[
            "OSHA Instruction CPL 02-00-124",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="Employer not responsible under policy",
        counter_arguments=[
            "No authority or control over hazard",
            "No employee exposure",
            "Hazard created by another employer",
            "Obligations met under contract"
        ],
        resolution_strategy="Analyze contractual relationships, worksite control, and exposure records.",
        entity_scope="Employers at multi-employer worksites",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Summit Contractors, Inc., OSHRC Docket No. 03-1622"
    ),
    DoctrineBlock(
        topic="Abatement Requirements and Verification",
        keywords=["abatement", "correction", "verification", "abatement certification", "documentation"],
        conclusion_template="Employers must abate cited hazards by the abatement date and provide OSHA with abatement certification and, if required, documentation and verification.",
        reasoning_framework=(
            "After a citation, employers are required to correct (abate) the hazardous condition by the specified abatement date. "
            "For most violations, abatement certification must be submitted to OSHA, and for certain violations, additional documentation (e.g., photos, receipts) is required. "
            "Failure to abate may result in additional penalties. "
            "OSHA may require abatement verification for willful, repeat, or serious violations. "
            "Employers may contest abatement requirements through the OSHRC process."
        ),
        key_factors=[
            "Timely abatement of hazards",
            "Submission of abatement certification",
            "Provision of supporting documentation",
            "OSHA verification requirements",
            "Employer contest rights"
        ],
        primary_authority=[
            "29 CFR 1903.19",
            "OSHA Field Operations Manual"
        ],
        burden_holder="Employer",
        adversary_position="Abatement completed or not required",
        counter_arguments=[
            "Hazard already abated",
            "Documentation not required",
            "Abatement infeasible",
            "Citation contested"
        ],
        resolution_strategy="Review abatement records, certification forms, and supporting documentation.",
        entity_scope="All cited employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-00-148"
    ),
    DoctrineBlock(
        topic="Whistleblower Retaliation Section 11(c) Protection",
        keywords=["whistleblower", "retaliation", "11(c)", "protected activity", "adverse action"],
        conclusion_template="Employers are prohibited from retaliating against employees for engaging in protected activities under Section 11(c) of the OSH Act.",
        reasoning_framework=(
            "Section 11(c) of the OSH Act prohibits employers from discharging or otherwise discriminating against employees for exercising rights under the Act, including reporting injuries, filing complaints, or participating in OSHA proceedings. "
            "Protected activities include raising safety concerns, refusing dangerous work, and cooperating with OSHA. "
            "Adverse actions include termination, demotion, reduction in pay, or other negative employment actions. "
            "Employees must file complaints within 30 days. "
            "OSHA investigates and may order reinstatement, back pay, and other remedies."
        ),
        key_factors=[
            "Employee engagement in protected activity",
            "Adverse employment action",
            "Causal connection between activity and action",
            "Timeliness of complaint",
            "Employer's stated reasons for action"
        ],
        primary_authority=[
            "29 U.S.C. § 660(c)",
            "OSHA Whistleblower Investigations Manual"
        ],
        burden_holder="Employee/OSHA",
        adversary_position="Action not retaliatory or not causally connected",
        counter_arguments=[
            "No protected activity",
            "Adverse action unrelated to protected activity",
            "Legitimate business reason for action",
            "Complaint not timely filed"
        ],
        resolution_strategy="Interview parties, review employment records, and assess timing and motivation.",
        entity_scope="All employees under OSH Act",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OSHRC and federal court whistleblower decisions"
    ),
    DoctrineBlock(
        topic="Serious Violation Determination",
        keywords=["serious violation", "substantial probability", "death", "serious harm", "citation"],
        conclusion_template="A violation is classified as serious if there is a substantial probability that death or serious physical harm could result from the hazard.",
        reasoning_framework=(
            "Under 29 U.S.C. § 666(k), a serious violation exists if the employer knew or should have known of a hazard with a substantial probability of death or serious harm. "
            "The probability refers to the degree of harm, not the likelihood of an accident. "
            "OSHA must show employer knowledge and that feasible means of abatement existed. "
            "Employers may argue lack of knowledge or infeasibility."
        ),
        key_factors=[
            "Existence of a hazard",
            "Employer knowledge (actual or constructive)",
            "Potential for death or serious harm",
            "Feasibility of abatement"
        ],
        primary_authority=[
            "29 U.S.C. § 666(k)",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="Hazard not serious or employer lacked knowledge",
        counter_arguments=[
            "No substantial probability of serious harm",
            "Employer did not know or could not have known",
            "Feasible abatement not available"
        ],
        resolution_strategy="Assess hazard severity, employer knowledge, and abatement options.",
        entity_scope="All employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Waldon Healthcare Center, OSHRC Docket No. 89-2804"
    ),
    DoctrineBlock(
        topic="Willful Violation Criteria",
        keywords=["willful violation", "intentional disregard", "plain indifference", "citation", "penalty"],
        conclusion_template="A willful violation occurs when an employer intentionally disregards or is plainly indifferent to OSHA requirements.",
        reasoning_framework=(
            "A willful violation is one committed with intentional disregard of, or plain indifference to, OSHA requirements. "
            "Evidence may include prior citations, employer statements, or failure to act despite awareness. "
            "Willful violations carry higher penalties and may result in criminal prosecution if a fatality occurs. "
            "Employers may argue good faith efforts or misunderstanding of requirements."
        ),
        key_factors=[
            "Employer knowledge of requirements",
            "Intentional disregard or indifference",
            "Prior OSHA citations or warnings",
            "Employer actions or inactions"
        ],
        primary_authority=[
            "29 U.S.C. § 666(a)",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="No willful intent; good faith effort",
        counter_arguments=[
            "Good faith misunderstanding",
            "No prior knowledge of requirement",
            "Corrective actions taken",
            "Violation not willful"
        ],
        resolution_strategy="Review employer history, statements, and corrective actions.",
        entity_scope="All employers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. A.P. O'Horo Company, OSHRC Docket No. 00-0369"
    ),
    DoctrineBlock(
        topic="Repeat Violation Determination",
        keywords=["repeat violation", "prior citation", "substantially similar", "OSHRC", "penalty"],
        conclusion_template="A violation is repeat if the employer was previously cited for a substantially similar condition and the citation has become a final order.",
        reasoning_framework=(
            "A repeat violation exists when an employer is cited for a condition substantially similar to one previously cited, and the prior citation has become a final order. "
            "Similarity is based on the nature of the hazard, not identical circumstances. "
            "There is no time limit, but OSHA generally looks back five years. "
            "Employers may argue the prior citation is not final or the conditions are not substantially similar."
        ),
        key_factors=[
            "Existence of prior final citation",
            "Substantial similarity of conditions",
            "Employer knowledge",
            "Time frame since prior citation"
        ],
        primary_authority=[
            "29 U.S.C. § 666(a)",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="No prior final citation or similarity",
        counter_arguments=[
            "Prior citation not final",
            "Conditions not substantially similar",
            "Time frame too remote",
            "Corrective actions taken"
        ],
        resolution_strategy="Compare citation records, review hazard descriptions, and assess similarity.",
        entity_scope="All employers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Potlatch Corp., 7 BNA OSHC 1061 (OSHRC 1979)"
    ),
    DoctrineBlock(
        topic="Other-Than-Serious Violation Criteria",
        keywords=["other-than-serious", "violation", "citation", "penalty"],
        conclusion_template="A violation is other-than-serious if it has a direct relationship to job safety and health but would not likely cause death or serious harm.",
        reasoning_framework=(
            "Other-than-serious violations are those that have a direct relationship to safety and health but are not likely to cause death or serious physical harm. "
            "Penalties may be assessed but are typically lower. "
            "OSHA considers the gravity of the violation, employer size, history, and good faith in penalty assessment."
        ),
        key_factors=[
            "Relationship to safety and health",
            "Potential for death or serious harm",
            "Employer knowledge",
            "Abatement efforts"
        ],
        primary_authority=[
            "29 U.S.C. § 666(c)",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="No direct relationship to safety/health",
        counter_arguments=[
            "No direct relationship to job safety/health",
            "Violation is de minimis",
            "Abatement completed"
        ],
        resolution_strategy="Assess the nature of the violation and its relationship to safety and health.",
        entity_scope="All employers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OSHRC case law on other-than-serious violations"
    ),
    DoctrineBlock(
        topic="De Minimis Violation Exception",
        keywords=["de minimis", "violation", "no direct relationship", "no citation"],
        conclusion_template="A de minimis violation has no direct relationship to safety or health and does not result in a citation or penalty.",
        reasoning_framework=(
            "De minimis violations are technical violations of OSHA standards that have no direct or immediate relationship to safety or health. "
            "OSHA does not issue citations or penalties for de minimis conditions but may note them in inspection reports. "
            "Employers are encouraged to correct de minimis conditions but are not required to do so."
        ),
        key_factors=[
            "Technical violation of standard",
            "No direct relationship to safety/health",
            "No potential for injury or illness"
        ],
        primary_authority=[
            "OSHA Field Operations Manual",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="Condition is not de minimis",
        counter_arguments=[
            "Condition poses a safety/health risk",
            "Violation is not merely technical",
            "Correction required"
        ],
        resolution_strategy="Evaluate the relationship of the violation to safety and health.",
        entity_scope="All employers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OSHRC case law on de minimis violations"
    ),
    DoctrineBlock(
        topic="Employee Misconduct Defense",
        keywords=["employee misconduct", "affirmative defense", "unpreventable", "violation"],
        conclusion_template="An employer may avoid liability if it proves the violation resulted from unpreventable employee misconduct despite an adequate safety program.",
        reasoning_framework=(
            "The employee misconduct defense is an affirmative defense requiring the employer to prove: (1) an established work rule to prevent the violation; "
            "(2) adequate communication of the rule; (3) steps to discover violations; and (4) effective enforcement when violations are found. "
            "If the violation resulted from unpreventable employee misconduct, the employer is not liable."
        ),
        key_factors=[
            "Existence of work rule",
            "Communication and training",
            "Monitoring and enforcement",
            "Unpreventability of misconduct"
        ],
        primary_authority=[
            "OSHRC case law",
            "OSHA Field Operations Manual"
        ],
        burden_holder="Employer",
        adversary_position="Misconduct was preventable or rule inadequate",
        counter_arguments=[
            "No established work rule",
            "Rule not communicated or enforced",
            "Misconduct was foreseeable",
            "Employer failed to monitor"
        ],
        resolution_strategy="Review safety program, training records, and disciplinary actions.",
        entity_scope="All employers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Archer-Western Contractors, Ltd., OSHRC Docket No. 03-0747"
    ),
    DoctrineBlock(
        topic="Imminent Danger Abatement",
        keywords=["imminent danger", "abatement", "injunction", "OSH Act", "inspection"],
        conclusion_template="OSHA may seek an injunction to restrain conditions or practices that present an imminent danger to employees.",
        reasoning_framework=(
            "When an OSHA compliance officer identifies an imminent danger—any condition or practice reasonably expected to cause death or serious harm immediately or before abatement can be accomplished—"
            "the Secretary of Labor may seek a federal court injunction to restrain the condition. "
            "Employers must abate imminent dangers immediately. "
            "Refusal to abate may result in court action and possible criminal penalties."
        ),
        key_factors=[
            "Existence of imminent danger",
            "Employer's response to hazard",
            "OSHA inspection findings",
            "Timeliness of abatement"
        ],
        primary_authority=[
            "29 U.S.C. § 662",
            "OSHA Field Operations Manual"
        ],
        burden_holder="OSHA",
        adversary_position="No imminent danger exists",
        counter_arguments=[
            "No immediate risk of death or serious harm",
            "Hazard abated promptly",
            "Condition misclassified"
        ],
        resolution_strategy="Assess hazard severity, employer actions, and inspection reports.",
        entity_scope="All employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHRC and federal court decisions on imminent danger"
    ),
    DoctrineBlock(
        topic="Feasibility of Abatement Measures",
        keywords=["feasibility", "abatement", "engineering controls", "administrative controls", "cost"],
        conclusion_template="OSHA must demonstrate that feasible abatement methods exist and are capable of being implemented by the employer.",
        reasoning_framework=(
            "Feasibility of abatement is a key element in many OSHA standards and General Duty Clause cases. "
            "Feasibility includes both technological and economic feasibility. "
            "OSHA must show that abatement methods are available and capable of being implemented. "
            "Employers may argue that controls are technologically impossible or economically ruinous."
        ),
        key_factors=[
            "Availability of abatement methods",
            "Technological feasibility",
            "Economic feasibility",
            "Industry practice",
            "Employer resources"
        ],
        primary_authority=[
            "OSHRC case law",
            "OSHA Field Operations Manual"
        ],
        burden_holder="OSHA",
        adversary_position="Abatement not feasible",
        counter_arguments=[
            "No feasible method exists",
            "Cost is prohibitive",
            "Technology not available",
            "Industry does not use method"
        ],
        resolution_strategy="Review industry standards, cost analyses, and technological options.",
        entity_scope="All employers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="American Iron & Steel Institute v. OSHA, 577 F.2d 825 (3d Cir. 1978)"
    ),
    DoctrineBlock(
        topic="Employer Knowledge Requirement",
        keywords=["employer knowledge", "actual knowledge", "constructive knowledge", "violation"],
        conclusion_template="OSHA must prove the employer knew or, with reasonable diligence, could have known of the violative condition.",
        reasoning_framework=(
            "Employer knowledge is an element of every OSHA violation. "
            "Knowledge may be actual (direct awareness) or constructive (should have known with round diligence). "
            "Supervisors' knowledge is imputed to the employer. "
            "Employers may defend by showing lack of knowledge and reasonable safety program."
        ),
        key_factors=[
            "Awareness of hazardous condition",
            "Reasonable diligence",
            "Supervisor knowledge",
            "Safety program effectiveness"
        ],
        primary_authority=[
            "OSHRC case law",
            "OSHA Field Operations Manual"
        ],
        burden_holder="OSHA",
        adversary_position="Employer lacked knowledge",
        counter_arguments=[
            "Condition not reasonably discoverable",
            "No supervisor knowledge",
            "Effective safety program in place"
        ],
        resolution_strategy="Review inspection records, safety program, and supervisory oversight.",
        entity_scope="All employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Tampa Shipyards, Inc., OSHRC Docket No. 86-360"
    ),
    DoctrineBlock(
        topic="Good Faith Defense in OSHA Proceedings",
        keywords=["good faith", "defense", "OSHA", "violation", "penalty reduction"],
        conclusion_template="An employer's good faith efforts to comply with OSHA standards may mitigate penalties but do not excuse violations.",
        reasoning_framework=(
            "Good faith is considered in penalty assessment but is not a defense to the existence of a violation. "
            "Employers demonstrating honest and reasonable efforts to comply may receive penalty reductions. "
            "Evidence includes safety programs, training, and corrective actions. "
            "Willful violations are not mitigated by good faith."
        ),
        key_factors=[
            "Employer's efforts to comply",
            "Safety program implementation",
            "Training and corrective actions",
            "Nature of violation"
        ],
        primary_authority=[
            "OSHRC case law",
            "OSHA Field Operations Manual"
        ],
        burden_holder="Employer (for mitigation)",
        adversary_position="No good faith effort",
        counter_arguments=[
            "No evidence of good faith",
            "Efforts insufficient",
            "Violation was willful"
        ],
        resolution_strategy="Review safety policies, training records, and abatement actions.",
        entity_scope="All employers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OSHRC case law on good faith"
    ),
    DoctrineBlock(
        topic="Multi-Employer Worksite: Controlling Employer Liability",
        keywords=["multi-employer", "controlling employer", "liability", "worksite", "supervision"],
        conclusion_template="A controlling employer may be cited if it failed to exercise reasonable care to prevent and detect violations at the worksite.",
        reasoning_framework=(
            "A controlling employer is one with general supervisory authority over the worksite, including power to correct hazards or require others to correct them. "
            "Liability depends on whether the employer exercised reasonable care in preventing and detecting violations. "
            "Factors include frequency of inspections, enforcement of safety requirements, and contractual obligations."
        ),
        key_factors=[
            "Supervisory authority",
            "Efforts to prevent/detect violations",
            "Inspection frequency",
            "Enforcement of safety rules"
        ],
        primary_authority=[
            "OSHA Instruction CPL 02-00-124",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="No control or reasonable care exercised",
        counter_arguments=[
            "No authority over worksite",
            "Reasonable care exercised",
            "No employee exposure"
        ],
        resolution_strategy="Review contracts, inspection records, and employer policies.",
        entity_scope="Controlling employers at multi-employer worksites",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Summit Contractors, Inc."
    ),
    DoctrineBlock(
        topic="Multi-Employer Worksite: Exposing Employer Defense",
        keywords=["multi-employer", "exposing employer", "defense", "worksite", "hazard"],
        conclusion_template="An exposing employer may avoid citation if it lacked authority to correct the hazard and took reasonable steps to protect its employees.",
        reasoning_framework=(
            "An exposing employer is one whose employees are exposed to a hazard created by another employer. "
            "To avoid citation, the exposing employer must show it lacked authority to correct the hazard and took reasonable steps, such as warning employees or removing them from exposure. "
            "The doctrine encourages communication and hazard avoidance."
        ),
        key_factors=[
            "Employee exposure",
            "Authority to correct hazard",
            "Steps taken to protect employees",
            "Communication with other employers"
        ],
        primary_authority=[
            "OSHA Instruction CPL 02-00-124",
            "OSHRC case law"
        ],
        burden_holder="Exposing employer",
        adversary_position="Reasonable steps not taken",
        counter_arguments=[
            "Employer had authority to correct",
            "No steps taken to protect employees",
            "No communication with other employers"
        ],
        resolution_strategy="Review worksite communications, exposure records, and employer policies.",
        entity_scope="Exposing employers at multi-employer worksites",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Summit Contractors, Inc."
    ),
    DoctrineBlock(
        topic="Multi-Employer Worksite: Creating Employer Liability",
        keywords=["multi-employer", "creating employer", "liability", "worksite", "hazard"],
        conclusion_template="A creating employer may be cited if it created a hazardous condition, regardless of which employees are exposed.",
        reasoning_framework=(
            "A creating employer is one that creates a hazardous condition at a multi-employer worksite. "
            "Liability attaches even if only other employers' employees are exposed. "
            "The focus is on the act of creating the hazard, not on control or exposure."
        ),
        key_factors=[
            "Creation of hazardous condition",
            "Employee exposure (any employer)",
            "Worksite context",
            "Corrective actions taken"
        ],
        primary_authority=[
            "OSHA Instruction CPL 02-00-124",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="Employer did not create hazard",
        counter_arguments=[
            "Hazard created by another employer",
            "No hazardous condition existed",
            "Hazard abated promptly"
        ],
        resolution_strategy="Review worksite activities, hazard creation, and abatement records.",
        entity_scope="Creating employers at multi-employer worksites",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Summit Contractors, Inc."
    ),
    DoctrineBlock(
        topic="Multi-Employer Worksite: Correcting Employer Responsibility",
        keywords=["multi-employer", "correcting employer", "responsibility", "worksite", "hazard"],
        conclusion_template="A correcting employer is liable if it failed to exercise reasonable care in correcting a hazard it was responsible for.",
        reasoning_framework=(
            "A correcting employer is responsible for implementing measures to correct a hazard at a multi-employer worksite. "
            "Liability depends on whether the employer exercised reasonable care in correcting the hazard. "
            "Factors include contractual obligations, corrective actions, and communication with other employers."
        ),
        key_factors=[
            "Responsibility for hazard correction",
            "Corrective actions taken",
            "Reasonable care exercised",
            "Communication with other employers"
        ],
        primary_authority=[
            "OSHA Instruction CPL 02-00-124",
            "OSHRC case law"
        ],
        burden_holder="OSHA",
        adversary_position="Reasonable care exercised; no responsibility",
        counter_arguments=[
            "Employer not responsible for correction",
            "Reasonable care exercised",
            "Hazard corrected promptly"
        ],
        resolution_strategy="Review contracts, corrective action records, and communications.",
        entity_scope="Correcting employers at multi-employer worksites",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Secretary of Labor v. Summit Contractors, Inc."
    ),
    DoctrineBlock(
        topic="Hazard Recognition Standard",
        keywords=["hazard recognition", "industry recognition", "employer recognition", "common sense"],
        conclusion_template="A hazard is recognized if it is known in the industry, by the employer, or is obvious to a reasonable person.",
        reasoning_framework=(
            "Hazard recognition is established by evidence that the employer or industry recognizes the hazard, or that it is obvious to a reasonable person. "
            "Sources include industry standards, consensus standards, prior incidents, and employer safety policies. "
            "Recognition is a key element in General Duty Clause and other OSHA cases."
        ),
        key_factors=[
            "Industry standards",
            "Employer safety policies",
            "Prior incidents",
            "Obviousness to reasonable person"
        ],
        primary_authority=[
            "OSHRC case law",
            "OSHA Field Operations Manual"
        ],
        burden_holder="OSHA",
        adversary_position="Hazard not recognized",
        counter_arguments=[
            "No industry or employer recognition",
            "Hazard not obvious",
            "No prior incidents"
        ],
        resolution_strategy="Review industry standards, employer policies, and incident history.",
        entity_scope="All employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="National Realty & Construction Co., Inc. v. OSHRC"
    ),
    DoctrineBlock(
        topic="OSHA Inspection Rights and Employer Obligations",
        keywords=["inspection", "warrant", "employer rights", "employee rights", "compliance officer"],
        conclusion_template="OSHA may conduct workplace inspections with or without a warrant; employers must allow entry or may require a warrant.",
        reasoning_framework=(
            "OSHA compliance officers have authority to inspect workplaces. "
            "Employers may consent or require a warrant. "
            "Inspections may be programmed, complaint-driven, or accident-related. "
            "Employers must not interfere with inspections but may participate in opening/closing conferences and accompany the officer."
        ),
        key_factors=[
            "Inspection authority",
            "Employer consent or warrant",
            "Scope and purpose of inspection",
            "Employer and employee rights"
        ],
        primary_authority=[
            "29 U.S.C. § 657",
            "OSHA Field Operations Manual"
        ],
        burden_holder="OSHA (for warrant)",
        adversary_position="Inspection exceeds scope or lacks warrant",
        counter_arguments=[
            "No probable cause for warrant",
            "Inspection exceeds agreed scope",
            "Employer rights violated"
        ],
        resolution_strategy="Review warrant, inspection scope, and employer participation.",
        entity_scope="All employers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Marshall v. Barlow's, Inc., 436 U.S. 307 (1978)"
    ),
    DoctrineBlock(
        topic="Employee Right to Refuse Dangerous Work",
        keywords=["employee right", "refusal", "dangerous work", "imminent danger", "retaliation"],
        conclusion_template="Employees may refuse work if they reasonably believe they face imminent danger and there is insufficient time to eliminate the hazard.",
        reasoning_framework=(
            "Employees have the right to refuse dangerous work if: (1) they have a reasonable belief of imminent danger; (2) there is insufficient time to correct the hazard through regular enforcement channels; "
            "and (3) they have sought correction from the employer. "
            "Retaliation for such refusal is prohibited under Section 11(c)."
        ),
        key_factors=[
            "Reasonable belief of imminent danger",
            "Efforts to seek correction",
            "Timeliness of hazard",
            "Employer response"
        ],
        primary_authority=[
            "29 U.S.C. § 660(c)",
            "OSHA Whistleblower Investigations Manual"
        ],
        burden_holder="Employee",
        adversary_position="No imminent danger or reasonable belief",
        counter_arguments=[
            "No imminent danger",
            "Refusal not reasonable",
            "Hazard could be corrected"
        ],
        resolution_strategy="Review employee complaints, employer response, and hazard documentation.",
        entity_scope="All employees",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHRC and federal court decisions on Section 11(c)"
    ),
    DoctrineBlock(
        topic="OSHA Posting Requirements",
        keywords=["posting", "OSHA poster", "notice", "employee rights", "workplace"],
        conclusion_template="Employers must post the OSHA Job Safety and Health poster in a conspicuous location where employees are likely to see it.",
        reasoning_framework=(
            "OSHA regulations require employers to display the OSHA Job Safety and Health poster (or state equivalent) in a prominent location. "
            "Failure to post may result in citation. "
            "The poster informs employees of their rights and responsibilities under the OSH Act."
        ),
        key_factors=[
            "Poster displayed in conspicuous location",
            "Employee access",
            "Poster content up to date",
            "State plan requirements"
        ],
        primary_authority=[
            "29 CFR 1903.2",
            "OSHA Field Operations Manual"
        ],
        burden_holder="OSHA",
        adversary_position="Poster was displayed or not required",
        counter_arguments=[
            "Poster was posted",
            "Employees were informed by other means",
            "State plan requirements differ"
        ],
        resolution_strategy="Inspect workplace for poster, interview employees, and review state plan rules.",
        entity_scope="All employers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OSHA Field Operations Manual"
    ),
    DoctrineBlock(
        topic="Recordable Injury and Illness Criteria",
        keywords=["recordable", "injury", "illness", "OSHA 300", "recordkeeping"],
        conclusion_template="An injury or illness is recordable if it is work-related and meets general recording criteria under 29 CFR 1904.",
        reasoning_framework=(
            "A case is recordable if it is work-related and results in death, days away from work, restricted work, transfer, medical treatment beyond first aid, or loss of consciousness. "
            "Certain significant injuries/illnesses are always recordable. "
            "Employers must evaluate work-relatedness and the nature of the outcome."
        ),
        key_factors=[
            "Work-relatedness",
            "Outcome (death, days away, etc.)",
            "Medical treatment beyond first aid",
            "Significant injuries/illnesses"
        ],
        primary_authority=[
            "29 CFR 1904.4-1904.7",
            "OSHA Recordkeeping Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Case not work-related or does not meet criteria",
        counter_arguments=[
            "Injury/illness not work-related",
            "Does not meet recording criteria",
            "Case was recorded"
        ],
        resolution_strategy="Review medical records, OSHA 300 Log, and work activity.",
        entity_scope="Employers covered by Part 1904",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Recordkeeping Standard Interpretations"
    ),
    DoctrineBlock(
        topic="OSHA 300A Summary Posting Requirement",
        keywords=["OSHA 300A", "summary", "posting", "recordkeeping", "injury", "illness"],
        conclusion_template="Employers must post the OSHA 300A Summary of Work-Related Injuries and Illnesses from February 1 to April 30 each year.",
        reasoning_framework=(
            "The OSHA 300A Summary must be completed and posted in a conspicuous location annually from February 1 to April 30. "
            "The summary includes total numbers of cases, days away, and types of injuries/illnesses. "
            "A company executive must certify the summary. "
            "Failure to post or certify is a recordkeeping violation."
        ),
        key_factors=[
            "Completion of 300A Summary",
            "Posting in conspicuous location",
            "Certification by executive",
            "Posting period compliance"
        ],
        primary_authority=[
            "29 CFR 1904.32",
            "OSHA Recordkeeping Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Summary posted or employer exempt",
        counter_arguments=[
            "Summary was posted",
            "Employer is exempt",
            "Certification completed"
        ],
        resolution_strategy="Inspect posting location, review summary, and verify certification.",
        entity_scope="Employers covered by Part 1904",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA Recordkeeping Standard Interpretations"
    ),
    DoctrineBlock(
        topic="OSHA 301 Incident Report Requirement",
        keywords=["OSHA 301", "incident report", "recordkeeping", "injury", "illness"],
        conclusion_template="Employers must complete an OSHA 301 Incident Report or equivalent for each recordable injury or illness.",
        reasoning_framework=(
            "For each recordable injury or illness, employers must complete an OSHA 301 Incident Report or equivalent within seven days. "
            "The report must include details of the incident, affected employee, and treatment. "
            "Reports must be maintained for five years and made available to OSHA upon request."
        ),
        key_factors=[
            "Completion of 301 Incident Report",
            "Timeliness of completion",
            "Record retention",
            "Availability for inspection"
        ],
        primary_authority=[
            "29 CFR 1904.29",
            "OSHA Recordkeeping Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Report completed or employer exempt",
        counter_arguments=[
            "Report was completed",
            "Employer is exempt",
            "Equivalent form used"
        ],
        resolution_strategy="Review incident reports, retention records, and inspection logs.",
        entity_scope="Employers covered by Part 1904",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA Recordkeeping Standard Interpretations"
    ),
    DoctrineBlock(
        topic="HazCom Program Written Plan Requirement",
        keywords=["hazcom", "written plan", "hazard communication", "chemical safety"],
        conclusion_template="Employers must develop, implement, and maintain a written hazard communication program for workplaces with hazardous chemicals.",
        reasoning_framework=(
            "29 CFR 1910.1200(e) requires employers to have a written hazard communication program describing how labels, SDS, and training requirements are met. "
            "The plan must include a list of hazardous chemicals, methods of informing employees, and procedures for multi-employer worksites. "
            "Failure to have a written plan is a citation."
        ),
        key_factors=[
            "Presence of hazardous chemicals",
            "Written plan content",
            "Employee training",
            "Multi-employer worksite procedures"
        ],
        primary_authority=[
            "29 CFR 1910.1200(e)",
            "OSHA HazCom Standard"
        ],
        burden_holder="OSHA",
        adversary_position="No hazardous chemicals or plan not required",
        counter_arguments=[
            "No hazardous chemicals present",
            "Plan not required for employer",
            "Plan was in place"
        ],
        resolution_strategy="Review written plan, chemical inventory, and training records.",
        entity_scope="All employers with hazardous chemicals",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-02-079"
    ),
    DoctrineBlock(
        topic="HazCom Employee Training Requirement",
        keywords=["hazcom", "employee training", "hazard communication", "chemical safety"],
        conclusion_template="Employers must provide effective training to employees on hazardous chemicals at the time of initial assignment and when new hazards are introduced.",
        reasoning_framework=(
            "Employers must train employees on hazardous chemicals in their work area at the time of initial assignment and when new hazards are introduced. "
            "Training must cover label elements, SDS, protective measures, and methods to detect chemical presence. "
            "Training must be comprehensible and documented."
        ),
        key_factors=[
            "Employee exposure to hazardous chemicals",
            "Timing of training",
            "Training content and comprehension",
            "Documentation of training"
        ],
        primary_authority=[
            "29 CFR 1910.1200(h)",
            "OSHA HazCom Standard"
        ],
        burden_holder="OSHA",
        adversary_position="No hazardous chemicals or training provided",
        counter_arguments=[
            "No hazardous chemicals present",
            "Training provided and documented",
            "Employees not exposed"
        ],
        resolution_strategy="Review training records, interview employees, and inspect chemical inventory.",
        entity_scope="All employers with hazardous chemicals",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-02-079"
    ),
    DoctrineBlock(
        topic="HazCom Labeling Requirements for Secondary Containers",
        keywords=["hazcom", "labeling", "secondary container", "chemical safety"],
        conclusion_template="Employers must ensure secondary containers of hazardous chemicals are labeled with the product identifier and general hazard information.",
        reasoning_framework=(
            "Secondary containers must be labeled unless intended for immediate use by the employee who transferred the chemical. "
            "Labels must include the product identifier and general hazard information consistent with HazCom 2012. "
            "Failure to label is a citation."
        ),
        key_factors=[
            "Transfer of hazardous chemicals",
            "Use of secondary containers",
            "Label content",
            "Immediate use exception"
        ],
        primary_authority=[
            "29 CFR 1910.1200(f)",
            "OSHA HazCom Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Immediate use exception applies",
        counter_arguments=[
            "Container for immediate use only",
            "Label present",
            "No hazardous chemical"
        ],
        resolution_strategy="Inspect secondary containers, review labeling practices, and interview employees.",
        entity_scope="All employers with hazardous chemicals",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-02-079"
    ),
    DoctrineBlock(
        topic="HazCom Multi-Employer Worksite Communication",
        keywords=["hazcom", "multi-employer", "worksite", "communication", "chemical safety"],
        conclusion_template="Employers must inform other employers at the worksite about hazardous chemicals and provide access to SDS and labeling information.",
        reasoning_framework=(
            "At multi-employer worksites, each employer must inform other employers about hazardous chemicals, labeling, and SDS availability. "
            "Procedures must be described in the written HazCom program. "
            "Failure to communicate may result in citation."
        ),
        key_factors=[
            "Presence of multiple employers",
            "Hazardous chemicals on site",
            "Communication procedures",
            "Access to SDS and labels"
        ],
        primary_authority=[
            "29 CFR 1910.1200(e)(2)",
            "OSHA HazCom Standard"
        ],
        burden_holder="OSHA",
        adversary_position="No hazardous chemicals or communication occurred",
        counter_arguments=[
            "No hazardous chemicals present",
            "Communication procedures in place",
            "Other employers informed"
        ],
        resolution_strategy="Review written program, communication records, and interview employers.",
        entity_scope="All employers at multi-employer worksites",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-02-079"
    ),
    DoctrineBlock(
        topic="Lockout/Tagout Periodic Inspection Requirement",
        keywords=["lockout", "tagout", "LOTO", "periodic inspection", "energy control"],
        conclusion_template="Employers must conduct and document periodic inspections of energy control procedures at least annually.",
        reasoning_framework=(
            "29 CFR 1910.147(c)(6) requires annual periodic inspections of energy control procedures to ensure they are being followed. "
            "Inspections must be performed by an authorized employee other than the one(s) using the procedure. "
            "Deficiencies must be corrected and inspections documented."
        ),
        key_factors=[
            "Written energy control procedures",
            "Annual inspection frequency",
            "Inspector qualifications",
            "Documentation of inspection"
        ],
        primary_authority=[
            "29 CFR 1910.147(c)(6)",
            "OSHA LOTO Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Inspections conducted and documented",
        counter_arguments=[
            "Inspections performed as required",
            "No energy control procedures in use",
            "Equipment exempt"
        ],
        resolution_strategy="Review inspection records, interview authorized employees, and inspect procedures.",
        entity_scope="All employers with LOTO procedures",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-00-147"
    ),
    DoctrineBlock(
        topic="Lockout/Tagout Training Requirement",
        keywords=["lockout", "tagout", "LOTO", "training", "energy control"],
        conclusion_template="Employers must train authorized, affected, and other employees on lockout/tagout procedures relevant to their duties.",
        reasoning_framework=(
            "Training must ensure that authorized employees understand the recognition of hazardous energy sources, the type and magnitude of energy, and methods for energy isolation and control. "
            "Affected employees must be instructed on the purpose and use of procedures. "
            "Other employees must be informed about the prohibition against restarting equipment. "
            "Retraining is required when procedures change or deficiencies are found."
        ),
        key_factors=[
            "Employee classification (authorized, affected, other)",
            "Training content and delivery",
            "Retraining triggers",
            "Documentation of training"
        ],
        primary_authority=[
            "29 CFR 1910.147(c)(7)",
            "OSHA LOTO Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Training provided and documented",
        counter_arguments=[
            "Training conducted as required",
            "No hazardous energy present",
            "Employees not exposed"
        ],
        resolution_strategy="Review training records, interview employees, and inspect procedures.",
        entity_scope="All employers with LOTO procedures",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-00-147"
    ),
    DoctrineBlock(
        topic="Lockout/Tagout Cord-and-Plug Exception",
        keywords=["lockout", "tagout", "cord-and-plug", "exception", "energy control"],
        conclusion_template="Cord-and-plug connected equipment is exempt from LOTO if unplugging and exclusive control by the employee eliminates the hazard.",
        reasoning_framework=(
            "The LOTO standard exempts cord-and-plug connected equipment if the plug is under the exclusive control of the employee performing servicing or maintenance. "
            "No additional energy control procedures are required if unplugging eliminates the hazard. "
            "Employers must ensure that the plug remains under exclusive control."
        ),
        key_factors=[
            "Cord-and-plug connection",
            "Exclusive control by employee",
            "Hazard eliminated by unplugging",
            "No stored energy"
        ],
        primary_authority=[
            "29 CFR 1910.147(a)(2)(iii)(A)",
            "OSHA LOTO Standard"
        ],
        burden_holder="Employer",
        adversary_position="Exception does not apply",
        counter_arguments=[
            "Plug not under exclusive control",
            "Stored energy present",
            "Additional hazards exist"
        ],
        resolution_strategy="Inspect equipment, review procedures, and interview employees.",
        entity_scope="All employers with cord-and-plug equipment",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-00-147"
    ),
    DoctrineBlock(
        topic="Confined Space Atmospheric Testing Requirement",
        keywords=["confined space", "atmospheric testing", "permit-required", "hazard"],
        conclusion_template="Employers must test the internal atmosphere of a permit-required confined space before entry and monitor as necessary during entry.",
        reasoning_framework=(
            "Atmospheric testing must be conducted for oxygen content, flammable gases/vapors, and potential toxic air contaminants before entry. "
            "Continuous or periodic monitoring is required if hazards may develop. "
            "Testing must be performed by a competent person using calibrated instruments."
        ),
        key_factors=[
            "Permit-required confined space",
            "Atmospheric hazards present",
            "Testing and monitoring procedures",
            "Instrument calibration"
        ],
        primary_authority=[
            "29 CFR 1910.146(d)(5)",
            "OSHA Confined Space Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Testing conducted as required",
        counter_arguments=[
            "Testing performed and documented",
            "No atmospheric hazards present",
            "Space reclassified as non-permit"
        ],
        resolution_strategy="Review testing records, inspect instruments, and interview entry personnel.",
        entity_scope="Employers with permit-required confined spaces",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA CPL 02-00-100"
    ),
    DoctrineBlock(
        topic="Confined Space Entry Permit Content",
        keywords=["confined space", "entry permit", "permit-required", "hazard"],
        conclusion_template="Entry permits for permit-required confined spaces must contain information specified by 1910.146(f), including space identification, hazards, and authorization.",
        reasoning_framework=(
            "The entry permit must identify the space, authorized entrants, attendants, hazards, measures to isolate hazards, communication procedures, rescue services, and permit duration. "
            "Permits must be reviewed and canceled after entry. "
            "Failure to include required information is a citation."
        ),
        key_factors=[
            "Permit-required confined space",
            "Permit content",
            "Authorization and review",
            "Record retention"
        ],
        primary_authority=[
            "29 CFR 1910.146(f)",
            "OSHA Confined Space Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Permit content complete and procedures followed",
        counter_arguments=[
            "Permit included all required information",
            "No entry occurred",
            "Space reclassified as non-permit"
        ],
        resolution_strategy="Review entry permits, inspect space, and interview entry personnel.",
        entity_scope="Employers with permit-required confined spaces",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA CPL 02-00-100"
    ),
    DoctrineBlock(
        topic="Confined Space Rescue and Emergency Services",
        keywords=["confined space", "rescue", "emergency services", "permit-required"],
        conclusion_template="Employers must provide for timely rescue and emergency services for entrants into permit-required confined spaces.",
        reasoning_framework=(
            "Employers must evaluate and select rescue services capable of timely response. "
            "Rescue personnel must be trained and equipped, and practice rescues must be conducted at least annually. "
            "Non-entry rescue systems must be provided where feasible. "
            "Failure to provide for rescue is a serious violation."
        ),
        key_factors=[
            "Rescue service capability",
            "Training and equipment",
            "Practice rescues",
            "Non-entry rescue systems"
        ],
        primary_authority=[
            "29 CFR 1910.146(k)",
            "OSHA Confined Space Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Rescue services provided and documented",
        counter_arguments=[
            "Rescue services evaluated and selected",
            "Practice rescues conducted",
            "Non-entry rescue provided"
        ],
        resolution_strategy="Review rescue service evaluations, training records, and practice rescue documentation.",
        entity_scope="Employers with permit-required confined spaces",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA CPL 02-00-100"
    ),
    DoctrineBlock(
        topic="Confined Space Reclassification Procedures",
        keywords=["confined space", "reclassification", "permit-required", "hazard elimination"],
        conclusion_template="A permit-required confined space may be reclassified as non-permit if all hazards are eliminated without entry.",
        reasoning_framework=(
            "If all hazards within a permit-required confined space are eliminated without entry, the space may be reclassified as non-permit. "
            "The basis for reclassification must be documented and certified by the employer. "
            "Continuous monitoring is required if hazards could reappear."
        ),
        key_factors=[
            "Hazard elimination without entry",
            "Documentation and certification",
            "Continuous monitoring",
            "Reclassification procedures"
        ],
        primary_authority=[
            "29 CFR 1910.146(c)(7)",
            "OSHA Confined Space Standard"
        ],
        burden_holder="Employer",
        adversary_position="Hazards not eliminated or reclassification not documented",
        counter_arguments=[
            "Hazards not fully eliminated",
            "Entry required for elimination",
            "No documentation"
        ],
        resolution_strategy="Review reclassification records, hazard elimination procedures, and monitoring data.",
        entity_scope="Employers with permit-required confined spaces",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OSHA CPL 02-00-100"
    ),
    DoctrineBlock(
        topic="Fall Protection Training Requirement",
        keywords=["fall protection", "training", "construction", "1926.503"],
        conclusion_template="Construction employers must train employees exposed to fall hazards to recognize and minimize such hazards.",
        reasoning_framework=(
            "29 CFR 1926.503 requires employers to provide training for employees exposed to fall hazards. "
            "Training must cover the nature of fall hazards, correct procedures for erecting, maintaining, and using fall protection systems, and the use of personal protective equipment. "
            "Retraining is required when deficiencies are identified."
        ),
        key_factors=[
            "Employee exposure to fall hazards",
            "Training content and delivery",
            "Retraining triggers",
            "Documentation of training"
        ],
        primary_authority=[
            "29 CFR 1926.503",
            "OSHA Fall Protection Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Training provided and documented",
        counter_arguments=[
            "Training conducted as required",
            "No fall hazards present",
            "Employees not exposed"
        ],
        resolution_strategy="Review training records, interview employees, and inspect worksite.",
        entity_scope="Construction employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-01-049"
    ),
    DoctrineBlock(
        topic="Fall Protection System Selection",
        keywords=["fall protection", "system selection", "construction", "guardrails", "personal fall arrest"],
        conclusion_template="Employers must select and implement appropriate fall protection systems based on the nature of the work and site conditions.",
        reasoning_framework=(
            "Employers must assess the worksite and select fall protection systems (guardrails, safety nets, personal fall arrest) appropriate for the task and site conditions. "
            "Selection must consider feasibility, effectiveness, and employee training. "
            "Failure to select or implement appropriate systems is a violation."
        ),
        key_factors=[
            "Worksite assessment",
            "Nature of work",
            "System feasibility and effectiveness",
            "Employee training"
        ],
        primary_authority=[
            "29 CFR 1926.501",
            "OSHA Fall Protection Standard"
        ],
        burden_holder="OSHA",
        adversary_position="System selection appropriate and implemented",
        counter_arguments=[
            "System selected and implemented",
            "No fall hazards present",
            "Feasibility issues"
        ],
        resolution_strategy="Review worksite assessment, system selection records, and employee training.",
        entity_scope="Construction employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-01-049"
    ),
    DoctrineBlock(
        topic="Fall Protection for Leading Edge Work",
        keywords=["fall protection", "leading edge", "construction", "1926.501(b)(2)"],
        conclusion_template="Employees engaged in leading edge work must be protected from falls by guardrails, safety nets, or personal fall arrest systems.",
        reasoning_framework=(
            "For leading edge work, 29 CFR 1926.501(b)(2) requires fall protection at heights of 6 feet or more. "
            "Employers must provide guardrails, safety nets, or personal fall arrest systems unless infeasibility is demonstrated and a written plan is implemented. "
            "Failure to provide protection is a serious violation."
        ),
        key_factors=[
            "Employee exposure to leading edge",
            "Height above lower level",
            "Provision of protection systems",
            "Feasibility and written plan"
        ],
        primary_authority=[
            "29 CFR 1926.501(b)(2)",
            "OSHA Fall Protection Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Protection provided or infeasibility demonstrated",
        counter_arguments=[
            "Protection provided",
            "Infeasibility documented",
            "Written plan in place"
        ],
        resolution_strategy="Review worksite, protection systems, and written plans.",
        entity_scope="Construction employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-01-049"
    ),
    DoctrineBlock(
        topic="Fall Protection for Roofing Work",
        keywords=["fall protection", "roofing", "construction", "1926.501(b)(10)"],
        conclusion_template="Employees performing roofing work on low-slope roofs must be protected by guardrails, safety nets, personal fall arrest, or a combination of warning lines and safety monitoring.",
        reasoning_framework=(
            "29 CFR 1926.501(b)(10) specifies fall protection for roofing work on low-slope roofs. "
            "Employers may use guardrails, safety nets, personal fall arrest, or a combination of warning lines and safety monitoring. "
            "Selection depends on roof slope, height, and work activity."
        ),
        key_factors=[
            "Roof slope and height",
            "Type of roofing work",
            "Protection system selection",
            "Employee training"
        ],
        primary_authority=[
            "29 CFR 1926.501(b)(10)",
            "OSHA Fall Protection Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Protection provided or not required",
        counter_arguments=[
            "Protection provided",
            "Roof not low-slope",
            "Work not covered"
        ],
        resolution_strategy="Review worksite, roof characteristics, and protection systems.",
        entity_scope="Construction employers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-01-049"
    ),
    DoctrineBlock(
        topic="HazCom GHS Pictogram and Labeling Compliance",
        keywords=["hazcom", "GHS", "pictogram", "labeling", "chemical safety"],
        conclusion_template="Employers must ensure GHS pictograms and label elements are present on all hazardous chemical containers.",
        reasoning_framework=(
            "HazCom 2012 requires GHS pictograms, signal words, hazard statements, and precautionary statements on labels for hazardous chemicals. "
            "Employers must not deface or remove labels and must ensure secondary containers are labeled appropriately."
        ),
        key_factors=[
            "Presence of hazardous chemicals",
            "GHS pictogram and label elements",
            "Label maintenance",
            "Secondary container labeling"
        ],
        primary_authority=[
            "29 CFR 1910.1200(f), Appendix C",
            "OSHA HazCom Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Labels present and compliant",
        counter_arguments=[
            "Labels present and not defaced",
            "No hazardous chemicals present",
            "Employer not responsible for labeling"
        ],
        resolution_strategy="Inspect labels, review chemical inventory, and interview employees.",
        entity_scope="All employers with hazardous chemicals",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-02-079"
    ),
    DoctrineBlock(
        topic="HazCom SDS Accessibility Requirement",
        keywords=["hazcom", "SDS", "accessibility", "chemical safety"],
        conclusion_template="Employers must ensure Safety Data Sheets are readily accessible to employees for all hazardous chemicals in the workplace.",
        reasoning_framework=(
            "SDS must be available to employees during each work shift. "
            "Accessibility may be paper or electronic, but employees must know how to access them. "
            "Failure to provide access is a citation."
        ),
        key_factors=[
            "Presence of hazardous chemicals",
            "SDS availability and accessibility",
            "Employee knowledge of access",
            "Shift coverage"
        ],
        primary_authority=[
            "29 CFR 1910.1200(g)",
            "OSHA HazCom Standard"
        ],
        burden_holder="OSHA",
        adversary_position="SDS accessible and employees informed",
        counter_arguments=[
            "SDS accessible and available",
            "No hazardous chemicals present",
            "Employees trained on access"
        ],
        resolution_strategy="Inspect SDS locations, interview employees, and review training records.",
        entity_scope="All employers with hazardous chemicals",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Instruction CPL 02-02-079"
    ),
    DoctrineBlock(
        topic="HazCom Non-English Labeling and SDS",
        keywords=["hazcom", "non-english", "labeling", "SDS", "employee comprehension"],
        conclusion_template="Employers must ensure that labels and SDS are comprehensible to employees, including providing information in other languages as necessary.",
        reasoning_framework=(
            "HazCom requires that hazard information be understandable to employees. "
            "If employees do not understand English, employers must provide labels and SDS information in a language they understand. "
            "Failure to ensure comprehension is a violation."
        ),
        key_factors=[
            "Employee language proficiency",
            "Label and SDS translation",
            "Employee training and comprehension",
            "Documentation"
        ],
        primary_authority=[
            "29 CFR 1910.1200(h)",
            "OSHA HazCom Standard"
        ],
        burden_holder="OSHA",
        adversary_position="Employees understand labels and SDS",
        counter_arguments=[
            "Employees understand English",
            "Translation provided",
            "Training conducted"
        ],
        resolution_strategy="Interview employees, review training records, and inspect labels/SDS.",
        entity_scope="All employers with non-English speaking employees",