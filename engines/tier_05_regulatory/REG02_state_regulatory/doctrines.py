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
        topic="Texas APA Rulemaking Requirements",
        keywords=["APA", "rulemaking", "notice and comment", "Texas Administrative Procedure Act", "agency rules"],
        conclusion_template="The agency's rulemaking process {complies/does not comply} with the Texas APA requirements.",
        reasoning_framework="""
1. Identify whether the agency action constitutes 'rulemaking' under Tex. Gov't Code § 2001.003(6).
2. Examine if the agency provided adequate notice of proposed rules as required by Tex. Gov't Code § 2001.023.
3. Assess whether the agency allowed for public comment and considered those comments per § 2001.029.
4. Determine if the adopted rule is a logical outgrowth of the proposed rule.
5. Evaluate the sufficiency of the rule's statement of reasons under § 2001.033.
6. Consider whether the agency filed the rule with the Secretary of State and published it in the Texas Register.
7. Analyze any procedural irregularities and their materiality to the outcome.
8. Apply harmless error doctrine if procedural defects are alleged.
9. Review the record for substantial compliance with statutory requirements.
10. Consider judicial review standards under § 2001.038 and relevant case law.
""",
        key_factors=[
            "Adequacy of notice",
            "Opportunity for public comment",
            "Logical outgrowth of proposed rule",
            "Statement of reasons",
            "Filing and publication requirements",
            "Materiality of procedural defects"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n, 247 S.W.3d 709 (Tex. 2008)"
        ],
        burden_holder="Challenger of the rule",
        adversary_position="Agency asserts compliance with APA",
        counter_arguments=[
            "Procedural defects were harmless",
            "Substantial compliance suffices",
            "Challenger lacks standing"
        ],
        resolution_strategy="Analyze procedural record, apply harmless error, and assess substantial compliance.",
        entity_scope="All Texas state agencies subject to APA",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n"
    ),
    DoctrineBlock(
        topic="Railroad Commission Oil and Gas Regulations",
        keywords=["Railroad Commission", "oil and gas", "state regulation", "well permitting", "environmental compliance"],
        conclusion_template="The operator's activities {comply/do not comply} with Railroad Commission oil and gas regulations.",
        reasoning_framework="""
1. Determine whether the operator holds a valid permit for drilling, production, or disposal activities.
2. Review compliance with spacing, density, and proration rules under 16 Tex. Admin. Code §§ 3.37, 3.38.
3. Assess adherence to environmental protection standards, including casing, cementing, and spill prevention.
4. Examine reporting and recordkeeping requirements for production and waste disposal.
5. Evaluate enforcement actions, including notices of violation and penalties.
6. Consider the operator’s history of compliance and any mitigating factors.
7. Analyze the scope of the Commission’s jurisdiction and preemption over local ordinances.
8. Review appeals process for contested enforcement actions.
""",
        key_factors=[
            "Permit status",
            "Compliance with technical rules",
            "Environmental safeguards",
            "Reporting obligations",
            "Prior violations"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapters 81-91",
            "16 Tex. Admin. Code Ch. 3",
            "Railroad Comm’n of Tex. v. Manziel, 361 S.W.2d 560 (Tex. 1962)"
        ],
        burden_holder="Operator",
        adversary_position="Commission alleges noncompliance",
        counter_arguments=[
            "Substantial compliance achieved",
            "Technical violation did not cause harm",
            "Commission exceeded its authority"
        ],
        resolution_strategy="Review administrative record, apply Commission rules, and consider mitigation.",
        entity_scope="Oil and gas operators in Texas",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Railroad Comm’n of Tex. v. Manziel"
    ),
    DoctrineBlock(
        topic="TCEQ Environmental Permitting and Enforcement",
        keywords=["TCEQ", "environmental permits", "enforcement", "air quality", "water quality", "waste management"],
        conclusion_template="The TCEQ's permitting/enforcement action {is/is not} consistent with statutory and regulatory requirements.",
        reasoning_framework="""
1. Identify the type of permit or enforcement action at issue (air, water, waste).
2. Review statutory authority under Texas Water Code and Texas Health & Safety Code.
3. Assess compliance with application and public notice requirements.
4. Evaluate technical standards for emissions, discharges, or waste handling.
5. Consider TCEQ’s discretion in permit conditions and enforcement remedies.
6. Analyze the sufficiency of the administrative record and findings of fact.
7. Examine due process afforded to the permittee or respondent.
8. Review available administrative and judicial remedies.
""",
        key_factors=[
            "Type of permit/action",
            "Technical compliance",
            "Notice and comment",
            "Due process",
            "Remedial measures"
        ],
        primary_authority=[
            "Texas Water Code Chapters 5, 26",
            "Texas Health & Safety Code Chapters 361, 382",
            "30 Tex. Admin. Code"
        ],
        burden_holder="Permittee or respondent",
        adversary_position="TCEQ asserts compliance and authority",
        counter_arguments=[
            "Agency exceeded statutory authority",
            "Insufficient notice or opportunity to be heard",
            "Technical standards not met"
        ],
        resolution_strategy="Apply statutory and regulatory criteria, review record for sufficiency.",
        entity_scope="Entities subject to TCEQ regulation",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Citizens for a Safe Future v. TCEQ, 254 S.W.3d 792 (Tex. App.—Austin 2008, pet. denied)"
    ),
    DoctrineBlock(
        topic="Texas Department of Insurance Regulation",
        keywords=["TDI", "insurance regulation", "rate approval", "solvency", "market conduct"],
        conclusion_template="The insurer's conduct {complies/does not comply} with Texas Department of Insurance regulations.",
        reasoning_framework="""
1. Determine the type of insurance product and applicable regulatory framework.
2. Review TDI’s authority under Texas Insurance Code.
3. Assess compliance with rate and form filing requirements.
4. Examine solvency standards and financial reporting obligations.
5. Evaluate market conduct rules, including claims handling and unfair practices.
6. Consider enforcement mechanisms: administrative penalties, license suspension, receivership.
7. Analyze any available exemptions or safe harbors.
8. Review administrative remedies and judicial review options.
""",
        key_factors=[
            "Type of insurance product",
            "Rate and form compliance",
            "Solvency",
            "Market conduct",
            "Enforcement history"
        ],
        primary_authority=[
            "Texas Insurance Code",
            "28 Tex. Admin. Code",
            "State Bd. of Ins. v. Deffebach, 631 S.W.2d 794 (Tex. App.—Austin 1982, writ ref’d n.r.e.)"
        ],
        burden_holder="Insurer",
        adversary_position="TDI alleges noncompliance",
        counter_arguments=[
            "Substantial compliance",
            "Exemption applies",
            "Agency exceeded authority"
        ],
        resolution_strategy="Apply Insurance Code and TDI rules, review administrative record.",
        entity_scope="Insurers and regulated entities in Texas",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="State Bd. of Ins. v. Deffebach"
    ),
    DoctrineBlock(
        topic="State Occupational Licensing Requirements",
        keywords=["occupational licensing", "state boards", "license denial", "disciplinary action", "good moral character"],
        conclusion_template="The applicant/licensee {meets/does not meet} the requirements for state occupational licensing.",
        reasoning_framework="""
1. Identify the relevant licensing board and statutory authority.
2. Review application requirements, including education, experience, and examination.
3. Assess grounds for denial, suspension, or revocation (e.g., criminal history, lack of good moral character).
4. Evaluate procedural protections: notice, hearing, appeal.
5. Consider rehabilitation and mitigating factors for past misconduct.
6. Analyze the board’s discretion and limits under the enabling statute.
7. Review judicial review standards for agency decisions.
""",
        key_factors=[
            "Statutory requirements",
            "Applicant qualifications",
            "Grounds for discipline",
            "Procedural protections",
            "Mitigating factors"
        ],
        primary_authority=[
            "Texas Occupations Code",
            "Texas Administrative Code (various titles)",
            "Texas State Bd. of Dental Examiners v. Brown, 281 S.W.2d 719 (Tex. Civ. App.—San Antonio 1955, writ ref’d n.r.e.)"
        ],
        burden_holder="Applicant or licensee",
        adversary_position="Board asserts statutory compliance",
        counter_arguments=[
            "Board abused discretion",
            "Procedural due process violated",
            "Mitigating evidence ignored"
        ],
        resolution_strategy="Apply statutory criteria, review record, consider due process.",
        entity_scope="Applicants and licensees of Texas state boards",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas State Bd. of Dental Examiners v. Brown"
    ),
    DoctrineBlock(
        topic="SOAH Contested Case Hearing Procedures",
        keywords=["SOAH", "contested case", "administrative hearing", "procedural rights", "evidence"],
        conclusion_template="The SOAH hearing {complied/did not comply} with applicable contested case procedures.",
        reasoning_framework="""
1. Determine whether the matter qualifies as a 'contested case' under Tex. Gov't Code § 2001.003(1).
2. Review notice of hearing and opportunity to be heard.
3. Assess the conduct of the hearing: presentation of evidence, cross-examination, recordkeeping.
4. Evaluate the impartiality of the administrative law judge (ALJ).
5. Analyze the application of rules of evidence and burden of proof.
6. Consider the issuance of a proposal for decision and exceptions process.
7. Review the agency’s final order for compliance with SOAH recommendations.
8. Examine available judicial review.
""",
        key_factors=[
            "Notice and opportunity to be heard",
            "Presentation of evidence",
            "Impartiality of ALJ",
            "Burden of proof",
            "Record of proceedings"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "1 Tex. Admin. Code Ch. 155",
            "SOAH enabling statute"
        ],
        burden_holder="Party challenging the hearing",
        adversary_position="SOAH asserts procedural compliance",
        counter_arguments=[
            "Harmless error",
            "Procedural defect not prejudicial",
            "ALJ acted within discretion"
        ],
        resolution_strategy="Review hearing record, apply APA and SOAH rules.",
        entity_scope="All SOAH contested cases",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="State Preemption of Local Regulation",
        keywords=["preemption", "local ordinances", "state law", "conflict", "express preemption", "implied preemption"],
        conclusion_template="The state law {preempts/does not preempt} the local regulation.",
        reasoning_framework="""
1. Identify the state statute and local ordinance at issue.
2. Determine whether the state statute contains an express preemption clause.
3. If not, analyze for implied preemption: field preemption or conflict preemption.
4. Assess the degree of conflict or interference between state and local law.
5. Consider the legislative intent and purpose of the state statute.
6. Review relevant case law interpreting preemption in the subject area.
7. Evaluate the severability of the local ordinance.
8. Apply the presumption against preemption unless clearly indicated.
""",
        key_factors=[
            "Express preemption language",
            "Conflict between laws",
            "Legislative intent",
            "Field occupied by state",
            "Purpose of local ordinance"
        ],
        primary_authority=[
            "Texas Constitution art. XI, § 5",
            "State enabling statutes",
            "BCCA Appeal Group, Inc. v. City of Houston, 496 S.W.3d 1 (Tex. 2016)"
        ],
        burden_holder="Party asserting preemption",
        adversary_position="Local government asserts authority",
        counter_arguments=[
            "No express preemption",
            "Ordinance complements state law",
            "Presumption against preemption"
        ],
        resolution_strategy="Apply statutory construction, analyze conflict, review legislative history.",
        entity_scope="All Texas local governments",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="BCCA Appeal Group, Inc. v. City of Houston"
    ),
    DoctrineBlock(
        topic="Public Utility Commission Regulation",
        keywords=["PUC", "public utilities", "electricity", "telecommunications", "rate regulation", "certificate of convenience and necessity"],
        conclusion_template="The utility's action {complies/does not comply} with PUC regulations.",
        reasoning_framework="""
1. Identify the type of utility and applicable regulatory framework (electric, telecom, water).
2. Review PUC’s statutory authority under Texas Utilities Code.
3. Assess compliance with rate filing and approval processes.
4. Examine requirements for certificates of convenience and necessity (CCN).
5. Evaluate customer protection rules and complaint procedures.
6. Consider enforcement actions and penalties.
7. Analyze the scope of PUC’s jurisdiction and preemption over local regulation.
8. Review available remedies and appeal rights.
""",
        key_factors=[
            "Type of utility",
            "Rate and tariff compliance",
            "CCN requirements",
            "Customer protections",
            "Jurisdictional scope"
        ],
        primary_authority=[
            "Texas Utilities Code",
            "16 Tex. Admin. Code Ch. 25, 26",
            "Public Utility Comm’n v. Gulf States Utils. Co., 809 S.W.2d 201 (Tex. 1991)"
        ],
        burden_holder="Utility",
        adversary_position="PUC alleges noncompliance",
        counter_arguments=[
            "Substantial compliance",
            "PUC exceeded statutory authority",
            "Local regulation not preempted"
        ],
        resolution_strategy="Apply Utilities Code and PUC rules, review administrative record.",
        entity_scope="Public utilities in Texas",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Public Utility Comm’n v. Gulf States Utils. Co."
    ),
    DoctrineBlock(
        topic="Texas Alcoholic Beverage Commission Regulation",
        keywords=["TABC", "alcohol regulation", "licensing", "enforcement", "public safety"],
        conclusion_template="The licensee's conduct {complies/does not comply} with TABC regulations.",
        reasoning_framework="""
1. Determine the type of license or permit at issue.
2. Review TABC’s statutory authority under Texas Alcoholic Beverage Code.
3. Assess compliance with licensing requirements and restrictions.
4. Examine enforcement actions: violations, penalties, suspension, revocation.
5. Evaluate due process afforded in enforcement proceedings.
6. Consider public safety and community impact factors.
7. Analyze available administrative and judicial remedies.
""",
        key_factors=[
            "Type of license/permit",
            "Compliance with restrictions",
            "Enforcement history",
            "Due process",
            "Public safety concerns"
        ],
        primary_authority=[
            "Texas Alcoholic Beverage Code",
            "16 Tex. Admin. Code Ch. 33-50",
            "Texas Alcoholic Beverage Comm’n v. Amusement & Music Operators, 997 S.W.2d 651 (Tex. App.—Austin 1999, pet. dism’d)"
        ],
        burden_holder="Licensee",
        adversary_position="TABC alleges violation",
        counter_arguments=[
            "No violation occurred",
            "Procedural due process violated",
            "Penalty disproportionate"
        ],
        resolution_strategy="Apply statutory and regulatory criteria, review enforcement record.",
        entity_scope="Alcohol licensees in Texas",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas Alcoholic Beverage Comm’n v. Amusement & Music Operators"
    ),
    DoctrineBlock(
        topic="Agency Enabling Statute Interpretation",
        keywords=["agency authority", "enabling statute", "statutory construction", "Chevron deference", "express powers"],
        conclusion_template="The agency's action {is/is not} authorized by its enabling statute.",
        reasoning_framework="""
1. Identify the enabling statute and relevant provisions.
2. Apply principles of statutory construction: plain meaning, legislative intent, context.
3. Determine whether the agency’s action is expressly authorized or impliedly necessary.
4. Assess the application of agency deference (Chevron or Skidmore) in state context.
5. Evaluate whether the action is within the agency’s subject matter jurisdiction.
6. Consider limits on implied powers and the non-delegation doctrine.
7. Review relevant case law interpreting the enabling statute.
""",
        key_factors=[
            "Statutory language",
            "Legislative intent",
            "Express vs. implied powers",
            "Agency subject matter jurisdiction",
            "Judicial deference"
        ],
        primary_authority=[
            "Agency enabling statutes",
            "Texas Government Code",
            "Railroad Comm’n v. Lone Star Gas Co., 844 S.W.2d 679 (Tex. 1992)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts ultra vires action",
        counter_arguments=[
            "Implied authority exists",
            "Action necessary to effectuate statute",
            "Deference owed to agency interpretation"
        ],
        resolution_strategy="Apply statutory construction, review legislative history, analyze precedent.",
        entity_scope="All Texas state agencies",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Railroad Comm’n v. Lone Star Gas Co."
    ),
    DoctrineBlock(
        topic="Texas Open Records Act and Agency Transparency",
        keywords=["open records", "public information", "transparency", "Texas Public Information Act", "exemptions"],
        conclusion_template="The requested information {is/is not} subject to disclosure under the Texas Public Information Act.",
        reasoning_framework="""
1. Identify the nature of the requested information.
2. Determine whether the information is 'public information' under Tex. Gov't Code § 552.002.
3. Review applicable exemptions under §§ 552.101–552.159.
4. Assess whether the agency timely sought an Attorney General opinion if withholding information.
5. Evaluate the balancing of public interest and privacy/confidentiality concerns.
6. Consider procedural requirements for requests and responses.
7. Analyze judicial review standards for disclosure disputes.
""",
        key_factors=[
            "Nature of information",
            "Applicability of exemptions",
            "Timeliness of agency response",
            "Public interest vs. privacy",
            "Attorney General opinion"
        ],
        primary_authority=[
            "Texas Government Code Chapter 552",
            "Texas Attorney General Open Records Decisions",
            "Industrial Foundation of the South v. Texas Indus. Accident Bd., 540 S.W.2d 668 (Tex. 1976)"
        ],
        burden_holder="Agency withholding information",
        adversary_position="Requester asserts right to disclosure",
        counter_arguments=[
            "Exemption applies",
            "Disclosure would violate privacy",
            "Attorney General opinion supports withholding"
        ],
        resolution_strategy="Apply statutory exemptions, seek AG opinion, balance interests.",
        entity_scope="All Texas governmental bodies",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Industrial Foundation of the South v. Texas Indus. Accident Bd."
    ),
    DoctrineBlock(
        topic="Due Process in Administrative Proceedings",
        keywords=["due process", "administrative hearing", "notice", "opportunity to be heard", "impartial tribunal"],
        conclusion_template="The administrative proceeding {complied/did not comply} with due process requirements.",
        reasoning_framework="""
1. Identify the nature of the interest at stake (property, liberty, license).
2. Review notice provided to the affected party.
3. Assess the opportunity for a meaningful hearing.
4. Evaluate the impartiality of the decisionmaker.
5. Examine the adequacy of the record and findings.
6. Consider the application of procedural rules and rights to counsel.
7. Analyze the availability of appeal or judicial review.
8. Apply the Mathews v. Eldridge balancing test as adopted in Texas.
""",
        key_factors=[
            "Notice",
            "Opportunity to be heard",
            "Impartial decisionmaker",
            "Adequacy of record",
            "Right to appeal"
        ],
        primary_authority=[
            "U.S. Constitution, Fourteenth Amendment",
            "Texas Constitution art. I, § 19",
            "Mathews v. Eldridge, 424 U.S. 319 (1976)",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts due process violation",
        counter_arguments=[
            "Harmless error",
            "Adequate process provided",
            "No protected interest at stake"
        ],
        resolution_strategy="Apply Mathews balancing, review record for procedural adequacy.",
        entity_scope="All Texas administrative proceedings",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Judicial Review of Agency Actions",
        keywords=["judicial review", "agency action", "substantial evidence", "arbitrary and capricious", "exhaustion of remedies"],
        conclusion_template="The agency's action {is/is not} supported by substantial evidence and {is/is not} arbitrary or capricious.",
        reasoning_framework="""
1. Determine the statutory basis for judicial review (APA, enabling act, other).
2. Assess whether the party has exhausted administrative remedies.
3. Review the standard of review (substantial evidence, de novo, abuse of discretion).
4. Evaluate the sufficiency of the agency record.
5. Analyze whether the agency's findings are supported by substantial evidence.
6. Consider whether the agency acted arbitrarily, capriciously, or contrary to law.
7. Review the scope of permissible judicial relief.
""",
        key_factors=[
            "Exhaustion of remedies",
            "Standard of review",
            "Sufficiency of record",
            "Support for findings",
            "Agency discretion"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Party seeking review",
        adversary_position="Agency asserts action is supported by record",
        counter_arguments=[
            "Record supports agency action",
            "Agency acted within discretion",
            "No error affecting substantial rights"
        ],
        resolution_strategy="Apply statutory review standards, review record, consider agency discretion.",
        entity_scope="All Texas agency actions subject to review",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Texas Ethics Commission Regulation",
        keywords=["ethics commission", "campaign finance", "lobbying", "financial disclosure", "enforcement"],
        conclusion_template="The regulated party's conduct {complies/does not comply} with Texas Ethics Commission regulations.",
        reasoning_framework="""
1. Identify the type of regulated activity (campaign finance, lobbying, disclosure).
2. Review statutory and regulatory requirements for registration, reporting, and conduct.
3. Assess compliance with contribution limits, reporting deadlines, and disclosure obligations.
4. Examine enforcement actions: investigations, penalties, hearings.
5. Evaluate due process protections in enforcement proceedings.
6. Consider available administrative and judicial remedies.
""",
        key_factors=[
            "Type of regulated activity",
            "Compliance with reporting",
            "Contribution limits",
            "Enforcement actions",
            "Due process"
        ],
        primary_authority=[
            "Texas Government Code Chapter 571",
            "1 Tex. Admin. Code Ch. 18-22",
            "Texas Ethics Commission opinions"
        ],
        burden_holder="Regulated party",
        adversary_position="Commission alleges violation",
        counter_arguments=[
            "No violation occurred",
            "Procedural due process violated",
            "Penalty disproportionate"
        ],
        resolution_strategy="Apply statutory and regulatory criteria, review enforcement record.",
        entity_scope="Candidates, lobbyists, and officials in Texas",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Ethics Commission v. Roach, 74 S.W.3d 439 (Tex. App.—Austin 2002, pet. denied)"
    ),
    DoctrineBlock(
        topic="Workers Compensation Commission Oversight",
        keywords=["workers compensation", "DWC", "benefits", "compliance", "enforcement", "medical review"],
        conclusion_template="The employer/insurer's conduct {complies/does not comply} with Workers Compensation Commission requirements.",
        reasoning_framework="""
1. Identify the type of workers compensation claim or compliance issue.
2. Review statutory and regulatory requirements for benefits, reporting, and medical review.
3. Assess compliance with timelines for benefit payments and dispute resolution.
4. Examine enforcement actions: penalties, sanctions, audits.
5. Evaluate due process protections in enforcement proceedings.
6. Consider administrative and judicial remedies.
""",
        key_factors=[
            "Type of claim/issue",
            "Timeliness of payments",
            "Medical review compliance",
            "Enforcement actions",
            "Due process"
        ],
        primary_authority=[
            "Texas Labor Code Chapters 401-419",
            "28 Tex. Admin. Code",
            "Texas Workers’ Compensation Comm’n v. Garcia, 893 S.W.2d 504 (Tex. 1995)"
        ],
        burden_holder="Employer/insurer",
        adversary_position="Commission alleges violation",
        counter_arguments=[
            "No violation occurred",
            "Procedural due process violated",
            "Penalty disproportionate"
        ],
        resolution_strategy="Apply statutory and regulatory criteria, review enforcement record.",
        entity_scope="Employers, insurers, and claimants in Texas",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas Workers’ Compensation Comm’n v. Garcia"
    ),
    DoctrineBlock(
        topic="State Procurement and Competitive Bidding",
        keywords=["procurement", "competitive bidding", "state contracts", "bid protest", "award criteria"],
        conclusion_template="The procurement process {complied/did not comply} with state competitive bidding requirements.",
        reasoning_framework="""
1. Identify the type of procurement and applicable statutory framework.
2. Review solicitation and notice requirements.
3. Assess compliance with competitive bidding and evaluation criteria.
4. Examine the process for bid protests and appeals.
5. Evaluate conflict of interest and ethics requirements.
6. Consider remedies for improper procurement actions.
""",
        key_factors=[
            "Type of procurement",
            "Notice and solicitation",
            "Bid evaluation",
            "Protest procedures",
            "Conflict of interest"
        ],
        primary_authority=[
            "Texas Government Code Chapters 2155-2262",
            "Texas Administrative Code",
            "Texas State Bd. of Control v. Express Pub. Co., 294 S.W. 937 (Tex. 1927)"
        ],
        burden_holder="Challenger of procurement",
        adversary_position="Agency asserts compliance",
        counter_arguments=[
            "Substantial compliance",
            "No prejudice to bidders",
            "Discretion in award"
        ],
        resolution_strategy="Apply statutory and regulatory criteria, review procurement record.",
        entity_scope="All Texas state agencies",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas State Bd. of Control v. Express Pub. Co."
    ),
    DoctrineBlock(
        topic="Cooperative Federalism and State Program Delegation",
        keywords=["cooperative federalism", "state delegation", "EPA", "federal standards", "state implementation"],
        conclusion_template="The state's implementation of the delegated program {complies/does not comply} with federal requirements.",
        reasoning_framework="""
1. Identify the federal program and delegation mechanism (e.g., Clean Air Act, Clean Water Act).
2. Review state enabling legislation and regulatory framework.
3. Assess compliance with minimum federal standards.
4. Examine the scope of state discretion and any more stringent state requirements.
5. Evaluate federal oversight and enforcement mechanisms.
6. Consider the process for state plan approval and amendments.
7. Analyze judicial review standards for state and federal actions.
""",
        key_factors=[
            "Federal program requirements",
            "State implementation plan",
            "Minimum standards",
            "State discretion",
            "Federal oversight"
        ],
        primary_authority=[
            "Federal enabling statutes (e.g., 42 U.S.C. § 7410)",
            "Texas Water Code, Health & Safety Code",
            "EPA delegation documents"
        ],
        burden_holder="State agency",
        adversary_position="EPA or challenger alleges noncompliance",
        counter_arguments=[
            "State standards meet or exceed federal minimums",
            "Federal oversight exceeded",
            "State discretion preserved"
        ],
        resolution_strategy="Compare state program to federal requirements, review delegation documents.",
        entity_scope="Texas state agencies implementing federal programs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="City of Arlington v. FCC, 569 U.S. 290 (2013)"
    ),
    DoctrineBlock(
        topic="Dormant Commerce Clause and State Regulation",
        keywords=["dormant commerce clause", "interstate commerce", "state regulation", "discrimination", "burden"],
        conclusion_template="The state regulation {violates/does not violate} the Dormant Commerce Clause.",
        reasoning_framework="""
1. Identify the state regulation and its effect on interstate commerce.
2. Determine whether the regulation discriminates against out-of-state interests on its face, in purpose, or in effect.
3. If discriminatory, apply strict scrutiny: is it justified by a legitimate local purpose that cannot be served by nondiscriminatory means?
4. If not discriminatory, apply the Pike balancing test: does the burden on interstate commerce clearly exceed local benefits?
5. Review relevant Supreme Court and Texas case law.
6. Consider available remedies for unconstitutional regulation.
""",
        key_factors=[
            "Discrimination against interstate commerce",
            "Legitimate local purpose",
            "Availability of nondiscriminatory alternatives",
            "Burden vs. benefit",
            "Judicial precedent"
        ],
        primary_authority=[
            "U.S. Constitution, Art. I, § 8, cl. 3",
            "Pike v. Bruce Church, Inc., 397 U.S. 137 (1970)",
            "Granholm v. Heald, 544 U.S. 460 (2005)"
        ],
        burden_holder="Challenger of state regulation",
        adversary_position="State asserts regulation is nondiscriminatory and justified",
        counter_arguments=[
            "No discrimination",
            "Local benefits outweigh burden",
            "Federal law authorizes regulation"
        ],
        resolution_strategy="Apply discrimination analysis, Pike balancing, review precedent.",
        entity_scope="All Texas state regulations affecting commerce",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Pike v. Bruce Church, Inc."
    ),
    DoctrineBlock(
        topic="Attorney General Enforcement and Opinions",
        keywords=["attorney general", "enforcement", "legal opinions", "statutory interpretation", "agency guidance"],
        conclusion_template="The Attorney General's opinion {is/is not} binding and {does/does not} control agency action.",
        reasoning_framework="""
1. Identify the subject of the Attorney General opinion or enforcement action.
2. Review statutory authority for AG opinions (Tex. Gov't Code § 402.042).
3. Assess the binding effect of AG opinions on state agencies and officials.
4. Analyze the persuasive value of AG opinions in judicial proceedings.
5. Consider the AG’s enforcement authority and relationship to agency jurisdiction.
6. Examine relevant case law interpreting AG opinions and enforcement powers.
""",
        key_factors=[
            "Statutory authority for AG opinion",
            "Binding vs. persuasive effect",
            "Agency compliance",
            "Judicial deference",
            "Scope of enforcement authority"
        ],
        primary_authority=[
            "Texas Government Code Chapter 402",
            "Texas Attorney General Opinions",
            "Holmes v. Morales, 924 S.W.2d 920 (Tex. 1996)"
        ],
        burden_holder="Agency or official subject to opinion",
        adversary_position="AG asserts binding effect",
        counter_arguments=[
            "Opinion is advisory only",
            "Agency has independent authority",
            "Judicial review available"
        ],
        resolution_strategy="Apply statutory and case law, review AG opinion, consider agency discretion.",
        entity_scope="All Texas state agencies and officials",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Holmes v. Morales"
    ),
    # Additional doctrines for comprehensive coverage (to reach 40+)
    DoctrineBlock(
        topic="Administrative Subpoena Power and Enforcement",
        keywords=["subpoena", "administrative investigation", "enforcement", "agency power", "judicial review"],
        conclusion_template="The agency's issuance of a subpoena {is/is not} within its statutory authority and {is/is not} enforceable.",
        reasoning_framework="""
1. Identify the agency's statutory authority to issue subpoenas.
2. Review the scope and purpose of the subpoena (investigative, adjudicative).
3. Assess procedural requirements for issuance and service.
4. Evaluate the relevance and specificity of the requested information.
5. Consider constitutional limits (Fourth Amendment, due process).
6. Analyze judicial review standards for enforcement or quashing.
7. Examine remedies for noncompliance or overbreadth.
""",
        key_factors=[
            "Statutory authority",
            "Scope and purpose",
            "Procedural compliance",
            "Relevance and specificity",
            "Constitutional limits"
        ],
        primary_authority=[
            "Agency enabling statutes",
            "Texas Government Code Chapter 2001",
            "United States v. Morton Salt Co., 338 U.S. 632 (1950)"
        ],
        burden_holder="Agency seeking enforcement",
        adversary_position="Recipient asserts overbreadth or lack of authority",
        counter_arguments=[
            "Subpoena exceeds statutory scope",
            "Request is unduly burdensome",
            "Constitutional rights violated"
        ],
        resolution_strategy="Apply statutory and constitutional standards, review for relevance and specificity.",
        entity_scope="All Texas state agencies with subpoena power",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="United States v. Morton Salt Co."
    ),
    DoctrineBlock(
        topic="Delegation of Authority to Agency Staff",
        keywords=["delegation", "agency staff", "decisionmaking", "statutory limits", "subdelegation"],
        conclusion_template="The agency's delegation of authority to staff {is/is not} consistent with statutory and regulatory requirements.",
        reasoning_framework="""
1. Identify the statutory and regulatory provisions governing delegation.
2. Review the scope of authority delegated and to whom.
3. Assess whether the delegation is expressly authorized or implied.
4. Evaluate limits on subdelegation and retention of final decisionmaking.
5. Consider procedural safeguards and oversight mechanisms.
6. Analyze relevant case law on improper delegation.
""",
        key_factors=[
            "Statutory authorization",
            "Scope of delegation",
            "Procedural safeguards",
            "Oversight and review",
            "Retention of final authority"
        ],
        primary_authority=[
            "Agency enabling statutes",
            "Texas Government Code",
            "Railroad Comm’n v. Lone Star Gas Co., 844 S.W.2d 679 (Tex. 1992)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts improper delegation",
        counter_arguments=[
            "Delegation is necessary for efficiency",
            "Final authority retained by agency head",
            "Statute permits delegation"
        ],
        resolution_strategy="Apply statutory construction, review delegation instruments, analyze oversight.",
        entity_scope="All Texas state agencies",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Railroad Comm’n v. Lone Star Gas Co."
    ),
    DoctrineBlock(
        topic="Rulemaking Exemptions and Emergency Rules",
        keywords=["rulemaking", "exemptions", "emergency rules", "APA", "notice waiver"],
        conclusion_template="The agency's adoption of an emergency rule {complies/does not comply} with statutory requirements.",
        reasoning_framework="""
1. Identify the statutory basis for emergency rulemaking or exemption.
2. Review the agency's findings of imminent peril or necessity.
3. Assess compliance with notice, publication, and duration requirements.
4. Evaluate the scope and limits of the emergency rule.
5. Consider judicial review standards for emergency rule challenges.
6. Analyze relevant case law on emergency rulemaking.
""",
        key_factors=[
            "Statutory authority for exemption",
            "Findings of necessity",
            "Notice and publication",
            "Duration and scope",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code § 2001.034",
            "Texas Administrative Code",
            "El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n, 247 S.W.3d 709 (Tex. 2008)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts improper emergency rule",
        counter_arguments=[
            "Imminent peril justified emergency rule",
            "Procedural requirements met",
            "Rule is temporary and limited"
        ],
        resolution_strategy="Apply statutory criteria, review findings, consider judicial review.",
        entity_scope="All Texas state agencies",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n"
    ),
    DoctrineBlock(
        topic="Standing to Challenge Agency Action",
        keywords=["standing", "agency action", "injury in fact", "zone of interests", "APA"],
        conclusion_template="The party {has/does not have} standing to challenge the agency action.",
        reasoning_framework="""
1. Identify the nature of the agency action and the party's interest.
2. Review statutory and constitutional requirements for standing.
3. Assess whether the party suffered an actual or imminent injury.
4. Evaluate whether the interest is within the zone protected by the statute.
5. Consider prudential standing doctrines and exceptions.
6. Analyze relevant Texas and federal case law.
""",
        key_factors=[
            "Actual or imminent injury",
            "Zone of interests",
            "Statutory standing",
            "Prudential limitations",
            "Case law"
        ],
        primary_authority=[
            "Texas Government Code § 2001.038",
            "Texas Constitution",
            "Texas Ass’n of Bus. v. Tex. Air Control Bd., 852 S.W.2d 440 (Tex. 1993)"
        ],
        burden_holder="Party seeking review",
        adversary_position="Agency asserts lack of standing",
        counter_arguments=[
            "Injury is speculative",
            "Interest not protected by statute",
            "No justiciable controversy"
        ],
        resolution_strategy="Apply standing requirements, review party’s interest, analyze precedent.",
        entity_scope="All Texas agency actions",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Ass’n of Bus. v. Tex. Air Control Bd."
    ),
    DoctrineBlock(
        topic="Exhaustion of Administrative Remedies",
        keywords=["exhaustion", "administrative remedies", "judicial review", "ripeness", "final agency action"],
        conclusion_template="The party {has/has not} exhausted administrative remedies required for judicial review.",
        reasoning_framework="""
1. Identify the administrative remedies available under statute or rule.
2. Assess whether the party has pursued all required steps before seeking judicial review.
3. Review exceptions to exhaustion: futility, irreparable harm, lack of adequate remedy.
4. Evaluate whether the agency action is final and ripe for review.
5. Analyze relevant Texas case law.
""",
        key_factors=[
            "Availability of remedies",
            "Pursuit of remedies",
            "Exceptions to exhaustion",
            "Finality of agency action",
            "Ripeness"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Water Comm’n v. Dellana, 849 S.W.2d 808 (Tex. 1993)"
        ],
        burden_holder="Party seeking review",
        adversary_position="Agency asserts failure to exhaust",
        counter_arguments=[
            "Remedies are inadequate",
            "Futility exception applies",
            "Agency action is final"
        ],
        resolution_strategy="Apply exhaustion doctrine, review procedural history, analyze exceptions.",
        entity_scope="All Texas agency actions",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Water Comm’n v. Dellana"
    ),
    DoctrineBlock(
        topic="Open Meetings Act Compliance",
        keywords=["open meetings", "public meetings", "notice", "transparency", "Texas Open Meetings Act"],
        conclusion_template="The agency's meeting {complied/did not comply} with the Texas Open Meetings Act.",
        reasoning_framework="""
1. Identify whether the body is subject to the Open Meetings Act.
2. Review notice requirements for meetings and agendas.
3. Assess compliance with open session and executive session provisions.
4. Evaluate the sufficiency of meeting minutes and records.
5. Consider remedies for violations, including voiding actions and criminal penalties.
6. Analyze relevant Attorney General opinions and case law.
""",
        key_factors=[
            "Applicability of Act",
            "Notice and agenda",
            "Open vs. executive session",
            "Recordkeeping",
            "Remedies for violation"
        ],
        primary_authority=[
            "Texas Government Code Chapter 551",
            "Texas Attorney General Opinions",
            "Acker v. Texas Water Comm’n, 790 S.W.2d 299 (Tex. 1990)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts violation",
        counter_arguments=[
            "Substantial compliance",
            "Notice was sufficient",
            "No prejudice resulted"
        ],
        resolution_strategy="Apply statutory requirements, review meeting records, consider remedies.",
        entity_scope="All Texas governmental bodies",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Acker v. Texas Water Comm’n"
    ),
    DoctrineBlock(
        topic="Administrative Record and Evidence Standards",
        keywords=["administrative record", "evidence", "substantial evidence", "recordkeeping", "judicial review"],
        conclusion_template="The administrative record {is/is not} sufficient to support the agency's decision.",
        reasoning_framework="""
1. Identify the contents of the administrative record.
2. Review statutory and regulatory requirements for recordkeeping.
3. Assess whether the record contains substantial evidence supporting findings.
4. Evaluate the admissibility and weight of evidence presented.
5. Consider challenges to the completeness or accuracy of the record.
6. Analyze judicial review standards for sufficiency of evidence.
""",
        key_factors=[
            "Contents of record",
            "Substantial evidence",
            "Admissibility of evidence",
            "Completeness of record",
            "Judicial review standards"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts insufficiency",
        counter_arguments=[
            "Record is complete",
            "Evidence supports findings",
            "No prejudice to party"
        ],
        resolution_strategy="Review record contents, apply evidence standards, consider judicial review.",
        entity_scope="All Texas agency proceedings",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Agency Rule Interpretation and Deference",
        keywords=["rule interpretation", "agency deference", "statutory construction", "Chevron", "Skidmore"],
        conclusion_template="The agency's interpretation of its rule {is/is not} entitled to deference.",
        reasoning_framework="""
1. Identify the rule at issue and the agency's interpretation.
2. Review the statutory basis for the rule and interpretive authority.
3. Assess whether the interpretation is reasonable and consistent with the rule's text and purpose.
4. Evaluate the level of deference (Chevron, Skidmore, or Texas-specific).
5. Consider judicial review standards for agency interpretations.
6. Analyze relevant Texas and federal case law.
""",
        key_factors=[
            "Statutory and rule text",
            "Reasonableness of interpretation",
            "Consistency with purpose",
            "Level of deference",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code",
            "Texas Administrative Code",
            "Railroad Comm’n v. Texas Citizens for a Safe Future, 336 S.W.3d 619 (Tex. 2011)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts misinterpretation",
        counter_arguments=[
            "Interpretation is unreasonable",
            "Contrary to statutory purpose",
            "No deference warranted"
        ],
        resolution_strategy="Apply deference standards, review interpretation, analyze precedent.",
        entity_scope="All Texas agencies",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Railroad Comm’n v. Texas Citizens for a Safe Future"
    ),
    DoctrineBlock(
        topic="Administrative Penalties and Sanctions",
        keywords=["penalties", "sanctions", "enforcement", "administrative fines", "due process"],
        conclusion_template="The administrative penalty {is/is not} authorized and {is/is not} proportionate to the violation.",
        reasoning_framework="""
1. Identify the statutory and regulatory basis for the penalty.
2. Review the process for notice, hearing, and opportunity to contest.
3. Assess the proportionality of the penalty to the violation.
4. Evaluate mitigating and aggravating factors.
5. Consider due process protections and appeal rights.
6. Analyze relevant case law on administrative penalties.
""",
        key_factors=[
            "Statutory authority",
            "Notice and hearing",
            "Proportionality",
            "Mitigating/aggravating factors",
            "Due process"
        ],
        primary_authority=[
            "Texas Government Code",
            "Texas Administrative Code",
            "State v. Credit Bureau of Laredo, Inc., 530 S.W.2d 288 (Tex. 1975)"
        ],
        burden_holder="Agency",
        adversary_position="Respondent asserts penalty is excessive or unauthorized",
        counter_arguments=[
            "Penalty within statutory limits",
            "Due process provided",
            "Mitigating factors considered"
        ],
        resolution_strategy="Apply statutory and regulatory criteria, review penalty record, consider proportionality.",
        entity_scope="All Texas agencies",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="State v. Credit Bureau of Laredo, Inc."
    ),
    DoctrineBlock(
        topic="Licensing Reciprocity and Interstate Practice",
        keywords=["reciprocity", "licensing", "interstate practice", "endorsement", "Texas Occupations Code"],
        conclusion_template="The applicant {is/is not} eligible for licensure in Texas based on reciprocity or endorsement.",
        reasoning_framework="""
1. Identify the profession and applicable licensing board.
2. Review statutory and regulatory provisions for reciprocity or endorsement.
3. Assess the applicant’s qualifications and licensure in another jurisdiction.
4. Evaluate any additional Texas-specific requirements.
5. Consider limitations on reciprocity (disciplinary history, scope of practice).
6. Analyze relevant case law and board policies.
""",
        key_factors=[
            "Reciprocity provisions",
            "Applicant qualifications",
            "Licensure in other state",
            "Texas-specific requirements",
            "Disciplinary history"
        ],
        primary_authority=[
            "Texas Occupations Code",
            "Texas Administrative Code",
            "Board rules and policies"
        ],
        burden_holder="Applicant",
        adversary_position="Board asserts ineligibility",
        counter_arguments=[
            "Qualifications substantially equivalent",
            "No disqualifying history",
            "Statute requires reciprocity"
        ],
        resolution_strategy="Apply statutory and board criteria, review applicant’s record.",
        entity_scope="Professionals seeking Texas licensure",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas State Bd. of Dental Examiners v. Brown"
    ),
    DoctrineBlock(
        topic="Administrative Res Judicata and Collateral Estoppel",
        keywords=["res judicata", "collateral estoppel", "administrative proceedings", "finality", "issue preclusion"],
        conclusion_template="The prior administrative decision {does/does not} preclude relitigation of the issue.",
        reasoning_framework="""
1. Identify the prior administrative proceeding and its finality.
2. Review the identity of parties and issues.
3. Assess whether the decision was on the merits and with opportunity to be heard.
4. Evaluate the applicability of res judicata and collateral estoppel doctrines.
5. Consider exceptions for changed circumstances or new evidence.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Finality of prior decision",
            "Identity of parties and issues",
            "Merits determination",
            "Opportunity to be heard",
            "Exceptions"
        ],
        primary_authority=[
            "Texas Government Code",
            "Texas Administrative Code",
            "City of Houston v. Houston Firefighters’ Relief & Retirement Fund, 502 S.W.3d 469 (Tex. 2016)"
        ],
        burden_holder="Party asserting preclusion",
        adversary_position="Opponent asserts new issues or changed circumstances",
        counter_arguments=[
            "Issues not identical",
            "No final decision",
            "New evidence or circumstances"
        ],
        resolution_strategy="Apply preclusion doctrines, review record, consider exceptions.",
        entity_scope="All Texas administrative proceedings",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="City of Houston v. Houston Firefighters’ Relief & Retirement Fund"
    ),
    DoctrineBlock(
        topic="Administrative Substantial Compliance Doctrine",
        keywords=["substantial compliance", "administrative law", "procedural defect", "harmless error", "APA"],
        conclusion_template="The agency's procedural defect {is/is not} cured by substantial compliance.",
        reasoning_framework="""
1. Identify the procedural requirement and alleged defect.
2. Review the purpose of the requirement and the harm, if any, caused by noncompliance.
3. Assess whether the agency substantially complied with the requirement.
4. Evaluate the application of harmless error doctrine.
5. Consider judicial review standards for procedural defects.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Nature of defect",
            "Purpose of requirement",
            "Harm or prejudice",
            "Degree of compliance",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n, 247 S.W.3d 709 (Tex. 2008)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts defect is fatal",
        counter_arguments=[
            "Substantial compliance achieved",
            "No prejudice resulted",
            "Requirement is directory, not mandatory"
        ],
        resolution_strategy="Apply substantial compliance and harmless error doctrines, review record.",
        entity_scope="All Texas agency proceedings",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n"
    ),
    DoctrineBlock(
        topic="Administrative Notice and Comment Sufficiency",
        keywords=["notice and comment", "rulemaking", "APA", "public participation", "Texas Register"],
        conclusion_template="The agency's notice and comment process {was/was not} sufficient under the APA.",
        reasoning_framework="""
1. Identify the notice provided and the method of publication.
2. Review the content and clarity of the notice.
3. Assess the opportunity for meaningful public comment.
4. Evaluate the agency's consideration of comments received.
5. Consider judicial review standards for sufficiency of notice and comment.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Adequacy of notice",
            "Opportunity for comment",
            "Consideration of comments",
            "Clarity of publication",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code § 2001.023",
            "Texas Administrative Code",
            "El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n, 247 S.W.3d 709 (Tex. 2008)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts insufficient notice or comment",
        counter_arguments=[
            "Notice was adequate",
            "Comments were considered",
            "No prejudice to public"
        ],
        resolution_strategy="Apply statutory requirements, review notice and comment record.",
        entity_scope="All Texas agency rulemakings",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="El Paso Hosp. Dist. v. Tex. Health & Human Servs. Comm’n"
    ),
    DoctrineBlock(
        topic="Administrative Discretion and Abuse of Discretion",
        keywords=["agency discretion", "abuse of discretion", "arbitrary and capricious", "judicial review", "APA"],
        conclusion_template="The agency's exercise of discretion {was/was not} an abuse of discretion.",
        reasoning_framework="""
1. Identify the discretionary decision at issue.
2. Review statutory and regulatory limits on agency discretion.
3. Assess whether the decision was arbitrary, capricious, or contrary to law.
4. Evaluate the record for rational basis and consistency with policy.
5. Consider judicial review standards for abuse of discretion.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Scope of discretion",
            "Statutory/regulatory limits",
            "Rational basis",
            "Consistency with policy",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Challenger",
        adversary_position="Agency asserts rational basis",
        counter_arguments=[
            "Decision supported by record",
            "Within agency discretion",
            "No legal error"
        ],
        resolution_strategy="Apply abuse of discretion standard, review record, analyze precedent.",
        entity_scope="All Texas agency actions",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Administrative Law Retroactivity and Vested Rights",
        keywords=["retroactivity", "vested rights", "agency rules", "APA", "due process"],
        conclusion_template="The agency's rule or action {does/does not} operate retroactively in violation of vested rights.",
        reasoning_framework="""
1. Identify the rule or action and its temporal application.
2. Review statutory and constitutional limits on retroactive application.
3. Assess whether the party has a vested right affected by the rule.
4. Evaluate the agency's intent and the language of the rule.
5. Consider judicial review standards for retroactivity.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Temporal application",
            "Vested rights",
            "Statutory/constitutional limits",
            "Agency intent",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Constitution art. I, § 16",
            "Texas Government Code",
            "City of Austin v. Whittington, 384 S.W.3d 766 (Tex. 2012)"
        ],
        burden_holder="Challenger",
        adversary_position="Agency asserts prospective application",
        counter_arguments=[
            "No vested right affected",
            "Rule is prospective only",
            "Retroactivity justified by public interest"
        ],
        resolution_strategy="Apply retroactivity standards, review rule language, analyze precedent.",
        entity_scope="All Texas agency rules and actions",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="City of Austin v. Whittington"
    ),
    DoctrineBlock(
        topic="Administrative Law Equal Protection Challenges",
        keywords=["equal protection", "administrative law", "discrimination", "rational basis", "constitutional challenge"],
        conclusion_template="The agency's action {does/does not} violate equal protection guarantees.",
        reasoning_framework="""
1. Identify the classification or disparate treatment at issue.
2. Review the applicable level of scrutiny (rational basis, intermediate, strict).
3. Assess the agency's justification for the classification.
4. Evaluate whether the action is rationally related to a legitimate government interest.
5. Consider judicial review standards for equal protection challenges.
6. Analyze relevant Texas and federal case law.
""",
        key_factors=[
            "Classification or disparate treatment",
            "Level of scrutiny",
            "Government interest",
            "Rational relationship",
            "Judicial review"
        ],
        primary_authority=[
            "U.S. Constitution, Fourteenth Amendment",
            "Texas Constitution art. I, § 3",
            "City of Cleburne v. Cleburne Living Center, 473 U.S. 432 (1985)"
        ],
        burden_holder="Challenger",
        adversary_position="Agency asserts rational basis",
        counter_arguments=[
            "Classification is rational",
            "No disparate treatment",
            "Government interest is legitimate"
        ],
        resolution_strategy="Apply equal protection analysis, review record, analyze precedent.",
        entity_scope="All Texas agency actions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="City of Cleburne v. Cleburne Living Center"
    ),
    DoctrineBlock(
        topic="Administrative Law Estoppel Against the Government",
        keywords=["estoppel", "agency", "government", "misrepresentation", "reliance"],
        conclusion_template="Estoppel {does/does not} apply against the agency in this administrative context.",
        reasoning_framework="""
1. Identify the alleged misrepresentation or conduct by the agency.
2. Review the elements of estoppel: misrepresentation, reliance, detriment.
3. Assess whether estoppel is available against the government under Texas law.
4. Evaluate the public interest and policy considerations.
5. Consider judicial review standards for estoppel claims.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Misrepresentation or conduct",
            "Reliance and detriment",
            "Availability of estoppel",
            "Public interest",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code",
            "City of Hutchins v. Prasifka, 450 S.W.2d 829 (Tex. 1970)"
        ],
        burden_holder="Party asserting estoppel",
        adversary_position="Agency asserts estoppel unavailable",
        counter_arguments=[
            "No misrepresentation",
            "No detrimental reliance",
            "Estoppel not available against government"
        ],
        resolution_strategy="Apply estoppel elements, review conduct, analyze precedent.",
        entity_scope="All Texas agency actions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="City of Hutchins v. Prasifka"
    ),
    DoctrineBlock(
        topic="Administrative Law Ultra Vires Actions",
        keywords=["ultra vires", "agency", "exceeding authority", "injunctive relief", "sovereign immunity"],
        conclusion_template="The agency's action {is/is not} ultra vires and {is/is not} subject to injunctive relief.",
        reasoning_framework="""
1. Identify the statutory or constitutional limits on agency authority.
2. Review the nature of the action and whether it exceeds granted powers.
3. Assess the availability of injunctive relief against ultra vires actions.
4. Evaluate the impact on sovereign immunity.
5. Consider judicial review standards for ultra vires claims.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Statutory/constitutional limits",
            "Nature of action",
            "Availability of injunctive relief",
            "Sovereign immunity",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code",
            "Heinrich v. City of San Antonio, 284 S.W.3d 366 (Tex. 2009)"
        ],
        burden_holder="Challenger",
        adversary_position="Agency asserts action within authority",
        counter_arguments=[
            "Action authorized by statute",
            "No violation of limits",
            "Sovereign immunity bars relief"
        ],
        resolution_strategy="Apply ultra vires doctrine, review statutory authority, analyze precedent.",
        entity_scope="All Texas agency actions",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Heinrich v. City of San Antonio"
    ),
    DoctrineBlock(
        topic="Administrative Law Severability of Rules",
        keywords=["severability", "agency rules", "invalid provision", "APA", "statutory construction"],
        conclusion_template="The invalid portion of the rule {is/is not} severable from the remainder.",
        reasoning_framework="""
1. Identify the invalid provision and basis for invalidity.
2. Review the rule's severability clause, if any.
3. Assess whether the remainder of the rule can function independently.
4. Evaluate the agency's intent and purpose of the rule.
5. Consider judicial review standards for severability.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Nature of invalid provision",
            "Severability clause",
            "Functionality of remainder",
            "Agency intent",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code",
            "Texas Administrative Code",
            "Commissioners Court of Houston County v. Rodgers, 691 S.W.2d 753 (Tex. App.—Tyler 1985, no writ)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts rule is not severable",
        counter_arguments=[
            "Remainder cannot function independently",
            "No severability clause",
            "Agency intent was for rule to operate as a whole"
        ],
        resolution_strategy="Apply severability doctrine, review rule text, analyze precedent.",
        entity_scope="All Texas agency rules",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Commissioners Court of Houston County v. Rodgers"
    ),
    DoctrineBlock(
        topic="Administrative Law Notice of Agency Decision",
        keywords=["notice", "agency decision", "final order", "APA", "timeliness"],
        conclusion_template="The agency's notice of decision {was/was not} sufficient and timely.",
        reasoning_framework="""
1. Identify the statutory and regulatory requirements for notice of decision.
2. Review the content and method of notice provided.
3. Assess the timeliness of notice in relation to decision date.
4. Evaluate the impact of deficient notice on appeal rights.
5. Consider judicial review standards for sufficiency of notice.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Statutory/regulatory requirements",
            "Content of notice",
            "Timeliness",
            "Impact on appeal rights",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts insufficient notice",
        counter_arguments=[
            "Notice was timely and sufficient",
            "No prejudice to party",
            "Harmless error"
        ],
        resolution_strategy="Apply notice requirements, review record, analyze prejudice.",
        entity_scope="All Texas agency decisions",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Administrative Law Timeliness of Appeals",
        keywords=["timeliness", "appeal", "judicial review", "APA", "limitations period"],
        conclusion_template="The appeal {is/is not} timely under applicable statutory and regulatory deadlines.",
        reasoning_framework="""
1. Identify the applicable limitations period for appeal or judicial review.
2. Review the date of final agency action and notice.
3. Assess whether the appeal was filed within the required time.
4. Evaluate exceptions for equitable tolling or delayed notice.
5. Consider judicial review standards for timeliness.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Limitations period",
            "Date of final action",
            "Filing date",
            "Equitable tolling",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Appellant",
        adversary_position="Agency asserts untimeliness",
        counter_arguments=[
            "Equitable tolling applies",
            "Notice was delayed",
            "Limitations period tolled by agency action"
        ],
        resolution_strategy="Apply statutory deadlines, review filing and notice dates, analyze exceptions.",
        entity_scope="All Texas agency appeals",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Administrative Law Burden of Proof",
        keywords=["burden of proof", "agency hearing", "contested case", "preponderance", "APA"],
        conclusion_template="The {party} {did/did not} meet the burden of proof in the administrative proceeding.",
        reasoning_framework="""
1. Identify the party with the burden of proof under statute or rule.
2. Review the standard of proof (preponderance, clear and convincing).
3. Assess the evidence presented by each party.
4. Evaluate the findings of fact and conclusions of law.
5. Consider judicial review standards for sufficiency of proof.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Statutory/rule assignment of burden",
            "Standard of proof",
            "Evidence presented",
            "Findings of fact",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Party assigned burden by statute or rule",
        adversary_position="Opposing party asserts failure of proof",
        counter_arguments=[
            "Burden not met",
            "Evidence insufficient",
            "Findings unsupported"
        ],
        resolution_strategy="Apply burden and standard of proof, review evidence and findings.",
        entity_scope="All Texas agency proceedings",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Administrative Law Judicial Notice",
        keywords=["judicial notice", "administrative law", "official records", "facts", "evidence"],
        conclusion_template="The agency's taking of judicial notice {was/was not} proper and {did/did not} affect the outcome.",
        reasoning_framework="""
1. Identify the fact or record subject to judicial notice.
2. Review statutory and regulatory authority for judicial notice in administrative proceedings.
3. Assess the opportunity for parties to contest or rebut noticed facts.
4. Evaluate the impact of judicial notice on findings and conclusions.
5. Consider judicial review standards for propriety of judicial notice.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Nature of fact or record",
            "Authority for judicial notice",
            "Opportunity to contest",
            "Impact on outcome",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Rules of Evidence",
            "Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="Agency",
        adversary_position="Challenger asserts improper notice",
        counter_arguments=[
            "Notice was proper",
            "Opportunity to contest was provided",
            "No prejudice to party"
        ],
        resolution_strategy="Apply rules for judicial notice, review record, analyze prejudice.",
        entity_scope="All Texas agency proceedings",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Health Facilities Comm’n v. Charter Medical-Dallas, Inc."
    ),
    DoctrineBlock(
        topic="Administrative Law Mandamus and Extraordinary Relief",
        keywords=["mandamus", "extraordinary relief", "agency action", "clear legal duty", "no adequate remedy"],
        conclusion_template="Mandamus {is/is not} available to compel or restrain the agency action.",
        reasoning_framework="""
1. Identify the agency action or inaction at issue.
2. Review the requirements for mandamus: clear legal duty, lack of adequate remedy at law.
3. Assess whether the agency has a ministerial or discretionary duty.
4. Evaluate the impact of sovereign immunity and statutory limitations.
5. Consider judicial review standards for mandamus relief.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Clear legal duty",
            "Adequacy of legal remedy",
            "Ministerial vs. discretionary duty",
            "Sovereign immunity",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code",
            "Texas Rules of Appellate Procedure",
            "Anderson v. City of Seven Points, 806 S.W.2d 791 (Tex. 1991)"
        ],
        burden_holder="Party seeking mandamus",
        adversary_position="Agency asserts no clear duty or adequate remedy exists",
        counter_arguments=[
            "Duty is discretionary",
            "Adequate remedy at law exists",
            "Sovereign immunity applies"
        ],
        resolution_strategy="Apply mandamus standards, review agency duty, analyze remedies.",
        entity_scope="All Texas agency actions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Anderson v. City of Seven Points"
    ),
    DoctrineBlock(
        topic="Administrative Law Official Immunity",
        keywords=["official immunity", "agency officials", "good faith", "discretionary acts", "liability"],
        conclusion_template="The agency official {is/is not} entitled to official immunity for the challenged action.",
        reasoning_framework="""
1. Identify the agency official and the nature of the challenged act.
2. Review the requirements for official immunity: discretionary act, within scope of authority, good faith.
3. Assess whether the act was ministerial or discretionary.
4. Evaluate evidence of good faith and scope of authority.
5. Consider judicial review standards for official immunity.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Nature of act",
            "Discretionary vs. ministerial",
            "Scope of authority",
            "Good faith",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code",
            "City of Lancaster v. Chambers, 883 S.W.2d 650 (Tex. 1994)"
        ],
        burden_holder="Official asserting immunity",
        adversary_position="Challenger asserts no immunity",
        counter_arguments=[
            "Act was ministerial",
            "Outside scope of authority",
            "Bad faith or malice"
        ],
        resolution_strategy="Apply immunity standards, review facts, analyze precedent.",
        entity_scope="All Texas agency officials",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="City of Lancaster v. Chambers"
    ),
    DoctrineBlock(
        topic="Administrative Law Public Participation and Intervention",
        keywords=["public participation", "intervention", "agency proceedings", "standing", "notice"],
        conclusion_template="The party {is/is not} entitled to participate or intervene in the agency proceeding.",
        reasoning_framework="""
1. Identify the statutory and regulatory provisions for public participation or intervention.
2. Review the party's interest and basis for intervention.
3. Assess procedural requirements for intervention (timeliness, notice).
4. Evaluate the impact of intervention on the proceeding.
5. Consider judicial review standards for participation rights.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Statutory/regulatory provisions",
            "Interest of party",
            "Procedural compliance",
            "Impact on proceeding",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 2001",
            "Texas Administrative Code",
            "Texas Ass’n of Bus. v. Tex. Air Control Bd., 852 S.W.2d 440 (Tex. 1993)"
        ],
        burden_holder="Party seeking intervention",
        adversary_position="Agency or other party opposes intervention",
        counter_arguments=[
            "No sufficient interest",
            "Untimely intervention",
            "Disruption of proceeding"
        ],
        resolution_strategy="Apply intervention standards, review interest, analyze impact.",
        entity_scope="All Texas agency proceedings",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Ass’n of Bus. v. Tex. Air Control Bd."
    ),
    DoctrineBlock(
        topic="Administrative Law Confidentiality and Sealing of Records",
        keywords=["confidentiality", "sealing", "agency records", "public information", "privacy"],
        conclusion_template="The agency's action {complies/does not comply} with confidentiality and sealing requirements.",
        reasoning_framework="""
1. Identify the nature of the records and applicable confidentiality provisions.
2. Review statutory and regulatory requirements for confidentiality and sealing.
3. Assess the process for requesting or ordering sealing of records.
4. Evaluate the balancing of public interest and privacy.
5. Consider judicial review standards for confidentiality orders.
6. Analyze relevant Texas case law.
""",
        key_factors=[
            "Nature of records",
            "Statutory/regulatory requirements",
            "Process for sealing",
            "Public interest vs. privacy",
            "Judicial review"
        ],
        primary_authority=[
            "Texas Government Code Chapter 552",
            "Texas Administrative Code",
            "Texas Attorney General Opinions"
        ],
        burden_holder="Party seeking confidentiality",
        adversary_position="Opposing party asserts right to access",
        counter_arguments=[
            "No statutory basis for confidentiality",
            "Public interest outweighs privacy",
            "Improper sealing process