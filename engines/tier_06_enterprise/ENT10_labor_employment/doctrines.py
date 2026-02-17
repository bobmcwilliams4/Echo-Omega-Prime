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
        topic="FLSA Overtime Exemption - Executive",
        keywords=["FLSA", "overtime", "exemption", "executive", "salary basis", "primary duty"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the executive exemption under FLSA.",
        reasoning_framework="""To determine whether an employee is exempt from overtime under the executive exemption, analyze:
1. Salary Basis: The employee must be compensated on a salary basis at a rate not less than $684 per week.
2. Primary Duty: The employee’s primary duty must be management of the enterprise or a recognized department/subdivision.
3. Authority: The employee must customarily and regularly direct the work of at least two or more other employees.
4. Hiring/Firing: The employee must have authority to hire or fire other employees, or their recommendations must be given particular weight.
Evaluate each factor based on factual evidence and compare against regulatory definitions and DOL guidance.""",
        key_factors=[
            "Salary basis ($684/week minimum)",
            "Primary duty is management",
            "Directs at least two employees",
            "Hiring/firing authority or significant influence"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(1)",
            "29 C.F.R. Part 541",
            "Department of Labor Wage and Hour Division Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status and overtime entitlement",
        counter_arguments=[
            "Employee performs non-managerial tasks as primary duty",
            "Employee lacks hiring/firing authority",
            "Salary basis not met"
        ],
        resolution_strategy="Apply regulatory definitions and review job duties, salary records, and organizational hierarchy.",
        entity_scope="Private and public sector employers subject to FLSA",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Christopher v. SmithKline Beecham Corp., 567 U.S. 142 (2012)"
    ),
    DoctrineBlock(
        topic="FMLA Eligibility and Entitlement",
        keywords=["FMLA", "eligibility", "entitlement", "leave", "employee rights"],
        conclusion_template="The employee {employee_name} is/is not eligible for FMLA leave and is/is not entitled to job protection.",
        reasoning_framework="""FMLA eligibility requires:
1. Employer Coverage: Employer must have 50+ employees within 75 miles.
2. Employee Tenure: Employee must have worked for at least 12 months and 1,250 hours in the preceding 12 months.
3. Qualifying Reason: Leave must be for a qualifying reason (serious health condition, birth/adoption, military exigency).
Entitlement includes up to 12 weeks of unpaid leave and restoration to the same/equivalent position. Analyze each requirement and supporting documentation.""",
        key_factors=[
            "Employer size and coverage",
            "Employee tenure (12 months, 1,250 hours)",
            "Qualifying reason for leave"
        ],
        primary_authority=[
            "29 U.S.C. § 2611 et seq.",
            "29 C.F.R. Part 825"
        ],
        burden_holder="Employee",
        adversary_position="Employer disputes eligibility or entitlement",
        counter_arguments=[
            "Insufficient hours worked",
            "Employer not covered",
            "Leave not for qualifying reason"
        ],
        resolution_strategy="Review personnel records, employer census, and medical/documentary evidence.",
        entity_scope="Covered employers and eligible employees",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Ragsdale v. Wolverine World Wide, Inc., 535 U.S. 81 (2002)"
    ),
    DoctrineBlock(
        topic="ADA Reasonable Accommodation - Interactive Process",
        keywords=["ADA", "reasonable accommodation", "interactive process", "disability", "employer obligations"],
        conclusion_template="The employer {employer_name} has/has not fulfilled its ADA obligations regarding reasonable accommodation for {employee_name}.",
        reasoning_framework="""The ADA requires employers to engage in an interactive process to identify reasonable accommodations for qualified individuals with disabilities.
1. Employee must disclose disability and request accommodation.
2. Employer must promptly initiate dialogue, gather relevant information, and explore possible accommodations.
3. Accommodation must be effective and not impose undue hardship.
4. Employer must document efforts and communicate decisions.
Analyze the adequacy of the interactive process, the feasibility of accommodations, and the impact on business operations.""",
        key_factors=[
            "Disclosure of disability",
            "Request for accommodation",
            "Employer response and engagement",
            "Effectiveness and feasibility of accommodation",
            "Undue hardship assessment"
        ],
        primary_authority=[
            "42 U.S.C. § 12101 et seq.",
            "29 C.F.R. § 1630.2(o)",
            "EEOC Enforcement Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Employee alleges failure to accommodate",
        counter_arguments=[
            "Accommodation not requested",
            "Accommodation not reasonable",
            "Undue hardship"
        ],
        resolution_strategy="Review communication records, accommodation proposals, and business impact analyses.",
        entity_scope="Covered employers and qualified employees with disabilities",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="U.S. Airways, Inc. v. Barnett, 535 U.S. 391 (2002)"
    ),
    DoctrineBlock(
        topic="Title VII Disparate Treatment - McDonnell Douglas Framework",
        keywords=["Title VII", "disparate treatment", "discrimination", "McDonnell Douglas", "prima facie case"],
        conclusion_template="The employee {employee_name} has/has not established a prima facie case of disparate treatment under Title VII.",
        reasoning_framework="""Disparate treatment claims under Title VII follow the McDonnell Douglas burden-shifting framework:
1. Employee must establish a prima facie case of discrimination (protected class, adverse action, qualification, replacement by non-protected individual).
2. Employer must articulate a legitimate, non-discriminatory reason for the action.
3. Employee must show the reason is pretextual.
Evaluate evidence at each stage, including comparators, employer explanations, and circumstantial proof.""",
        key_factors=[
            "Protected class membership",
            "Adverse employment action",
            "Qualification for position",
            "Replacement or treatment compared to others",
            "Employer’s stated reason",
            "Evidence of pretext"
        ],
        primary_authority=[
            "42 U.S.C. § 2000e-2",
            "McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)"
        ],
        burden_holder="Employee (prima facie), Employer (articulation)",
        adversary_position="Employer denies discriminatory motive",
        counter_arguments=[
            "Legitimate business reason",
            "No evidence of pretext",
            "Employee not qualified"
        ],
        resolution_strategy="Apply burden-shifting analysis and review documentary and testimonial evidence.",
        entity_scope="Covered employers and employees",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)"
    ),
    DoctrineBlock(
        topic="Title VII Disparate Impact",
        keywords=["Title VII", "disparate impact", "neutral policy", "adverse effect", "business necessity"],
        conclusion_template="The employer's policy {policy_name} does/does not have a disparate impact under Title VII.",
        reasoning_framework="""Disparate impact claims arise when a neutral policy disproportionately affects a protected group.
1. Employee must identify a specific employment practice and show statistical evidence of adverse impact.
2. Employer must demonstrate business necessity for the practice.
3. Employee may rebut with evidence of less discriminatory alternatives.
Analyze statistical data, business justifications, and alternative practices.""",
        key_factors=[
            "Identification of employment practice",
            "Statistical evidence of impact",
            "Business necessity",
            "Availability of less discriminatory alternatives"
        ],
        primary_authority=[
            "42 U.S.C. § 2000e-2(k)",
            "Griggs v. Duke Power Co., 401 U.S. 424 (1971)"
        ],
        burden_holder="Employee (impact), Employer (necessity)",
        adversary_position="Employer asserts business necessity",
        counter_arguments=[
            "Policy is job-related and consistent with business necessity",
            "No significant statistical disparity",
            "No less discriminatory alternative"
        ],
        resolution_strategy="Review statistical analyses, business records, and alternative proposals.",
        entity_scope="Covered employers and employees",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Griggs v. Duke Power Co., 401 U.S. 424 (1971)"
    ),
    DoctrineBlock(
        topic="ADEA Age Discrimination",
        keywords=["ADEA", "age discrimination", "protected class", "employment action", "burden shifting"],
        conclusion_template="The employee {employee_name} has/has not established age discrimination under the ADEA.",
        reasoning_framework="""ADEA protects employees aged 40 and older from discrimination.
1. Employee must show membership in protected class, adverse action, and replacement by younger person or less favorable treatment.
2. Employer must provide legitimate, non-discriminatory reason.
3. Employee must prove reason is pretextual.
Analyze direct and circumstantial evidence, comparators, and employer explanations.""",
        key_factors=[
            "Age (40+)",
            "Adverse employment action",
            "Replacement by younger employee",
            "Employer’s stated reason",
            "Evidence of pretext"
        ],
        primary_authority=[
            "29 U.S.C. § 623",
            "Gross v. FBL Financial Services, Inc., 557 U.S. 167 (2009)"
        ],
        burden_holder="Employee (prima facie), Employer (articulation)",
        adversary_position="Employer denies age motivation",
        counter_arguments=[
            "Legitimate business reason",
            "No evidence of age bias",
            "Employee not qualified"
        ],
        resolution_strategy="Apply burden-shifting framework and review age-related statements, comparators, and employment records.",
        entity_scope="Covered employers and employees aged 40+",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Gross v. FBL Financial Services, Inc., 557 U.S. 167 (2009)"
    ),
    DoctrineBlock(
        topic="WARN Act - Mass Layoff Notification",
        keywords=["WARN Act", "mass layoff", "notification", "employer obligations", "plant closing"],
        conclusion_template="The employer {employer_name} has/has not complied with WARN Act notification requirements for mass layoff.",
        reasoning_framework="""The WARN Act requires covered employers to provide 60 days’ advance written notice of mass layoffs or plant closings.
1. Employer must have 100+ employees.
2. Mass layoff involves 50+ employees at a single site or plant closing.
3. Notice must be provided to affected employees, state dislocated worker unit, and local government.
4. Exceptions: faltering company, unforeseeable business circumstances, natural disaster.
Analyze employer size, layoff scope, notice timing, and applicability of exceptions.""",
        key_factors=[
            "Employer size (100+ employees)",
            "Number of affected employees",
            "Notice timing and recipients",
            "Applicability of exceptions"
        ],
        primary_authority=[
            "29 U.S.C. § 2101 et seq.",
            "20 C.F.R. Part 639"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims insufficient notice",
        counter_arguments=[
            "Layoff does not meet threshold",
            "Exception applies",
            "Proper notice given"
        ],
        resolution_strategy="Review layoff records, notice documentation, and exception evidence.",
        entity_scope="Covered employers and affected employees",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="Local 217, Hotel & Restaurant Employees Union v. MHM, Inc., 976 F.2d 805 (2d Cir. 1992)"
    ),
    DoctrineBlock(
        topic="NLRA Section 7 Protected Concerted Activity",
        keywords=["NLRA", "Section 7", "protected concerted activity", "union", "employee rights"],
        conclusion_template="The activity {activity_description} is/is not protected concerted activity under NLRA Section 7.",
        reasoning_framework="""NLRA Section 7 protects employees’ rights to engage in concerted activities for mutual aid or protection.
1. Activity must involve two or more employees acting together.
2. Activity must relate to terms and conditions of employment.
3. Protection extends to union and non-union settings.
4. Exceptions: egregious misconduct, purely personal grievances.
Analyze the nature of the activity, participants, and employer response.""",
        key_factors=[
            "Number of employees involved",
            "Purpose of activity",
            "Relation to employment terms",
            "Employer response",
            "Misconduct or exceptions"
        ],
        primary_authority=[
            "29 U.S.C. § 157",
            "NLRB v. Washington Aluminum Co., 370 U.S. 9 (1962)"
        ],
        burden_holder="Employee",
        adversary_position="Employer claims activity not protected",
        counter_arguments=[
            "Activity was not concerted",
            "Activity involved misconduct",
            "Activity unrelated to employment"
        ],
        resolution_strategy="Review activity records, witness statements, and employer policies.",
        entity_scope="Private sector employees",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NLRB v. Washington Aluminum Co., 370 U.S. 9 (1962)"
    ),
    DoctrineBlock(
        topic="ERISA Fiduciary Duty - Retirement Plan Management",
        keywords=["ERISA", "fiduciary duty", "retirement plan", "investment", "prudence"],
        conclusion_template="The plan fiduciary {fiduciary_name} has/has not breached ERISA fiduciary duties in managing retirement plan assets.",
        reasoning_framework="""ERISA imposes fiduciary duties on plan administrators:
1. Duty of loyalty: Act solely in the interest of plan participants.
2. Duty of prudence: Manage assets with care, skill, prudence, and diligence.
3. Duty to diversify investments.
4. Duty to follow plan documents unless inconsistent with ERISA.
Analyze investment decisions, conflicts of interest, and adherence to plan terms.""",
        key_factors=[
            "Loyalty to participants",
            "Prudent investment management",
            "Diversification",
            "Compliance with plan documents"
        ],
        primary_authority=[
            "29 U.S.C. § 1104",
            "Fifth Third Bancorp v. Dudenhoeffer, 573 U.S. 409 (2014)"
        ],
        burden_holder="Plan participant",
        adversary_position="Fiduciary denies breach",
        counter_arguments=[
            "Investment decisions were prudent",
            "No conflict of interest",
            "Plan documents followed"
        ],
        resolution_strategy="Review investment records, plan documents, and fiduciary communications.",
        entity_scope="ERISA-covered retirement plans",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Fifth Third Bancorp v. Dudenhoeffer, 573 U.S. 409 (2014)"
    ),
    DoctrineBlock(
        topic="Non-Compete Agreement - Reasonableness",
        keywords=["non-compete", "agreement", "reasonableness", "duration", "geographic scope"],
        conclusion_template="The non-compete agreement {agreement_name} is/is not enforceable based on reasonableness.",
        reasoning_framework="""Enforceability of non-compete agreements depends on reasonableness:
1. Legitimate business interest (protection of trade secrets, customer relationships).
2. Duration and geographic scope must be reasonable.
3. Cannot impose undue hardship on employee or public policy.
4. State law varies; some states ban or restrict non-competes.
Analyze business justification, scope, hardship, and applicable state law.""",
        key_factors=[
            "Legitimate business interest",
            "Duration",
            "Geographic scope",
            "Hardship to employee",
            "Public policy"
        ],
        primary_authority=[
            "State statutes and common law",
            "Restatement (Second) of Contracts § 188"
        ],
        burden_holder="Employer",
        adversary_position="Employee challenges enforceability",
        counter_arguments=[
            "Scope is overly broad",
            "No legitimate interest",
            "Agreement violates public policy"
        ],
        resolution_strategy="Review agreement terms, business rationale, and state law.",
        entity_scope="Employers and employees subject to non-compete agreements",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="Bimbo Bakeries USA, Inc. v. Botticella, 613 F.3d 102 (3d Cir. 2010)"
    ),
    DoctrineBlock(
        topic="Trade Secrets - DTSA and State UTSA",
        keywords=["trade secrets", "DTSA", "UTSA", "misappropriation", "confidentiality"],
        conclusion_template="The information {info_description} qualifies/does not qualify as a trade secret under DTSA/UTSA.",
        reasoning_framework="""Trade secrets are protected under DTSA and state UTSA:
1. Information must derive independent economic value from not being generally known.
2. Owner must take reasonable measures to maintain secrecy.
3. Misappropriation involves improper acquisition, disclosure, or use.
Analyze economic value, secrecy measures, and evidence of misappropriation.""",
        key_factors=[
            "Economic value from secrecy",
            "Reasonable secrecy measures",
            "Evidence of misappropriation"
        ],
        primary_authority=[
            "18 U.S.C. § 1836 (DTSA)",
            "Uniform Trade Secrets Act (UTSA)"
        ],
        burden_holder="Trade secret owner",
        adversary_position="Alleged misappropriator denies trade secret status",
        counter_arguments=[
            "Information is generally known",
            "Secrecy measures inadequate",
            "No misappropriation"
        ],
        resolution_strategy="Review confidentiality policies, access controls, and evidence of disclosure/use.",
        entity_scope="Employers and employees handling confidential information",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Epic Systems Corp. v. Tata Consultancy Services Ltd., 980 F.3d 1117 (7th Cir. 2020)"
    ),
    DoctrineBlock(
        topic="Independent Contractor vs Employee - ABC Test and Economic Reality",
        keywords=["independent contractor", "employee", "ABC test", "economic reality", "classification"],
        conclusion_template="{worker_name} is/is not properly classified as an independent contractor under applicable law.",
        reasoning_framework="""Worker classification is determined by:
1. ABC Test (some states): (A) Worker is free from control, (B) Work is outside usual course of business, (C) Worker is customarily engaged in independent trade.
2. Economic Reality Test (federal): Analyze degree of control, opportunity for profit/loss, investment, skill, permanence, and integration.
Apply the relevant test based on jurisdiction and factual circumstances.""",
        key_factors=[
            "Degree of control",
            "Nature of work",
            "Worker’s business independence",
            "Opportunity for profit/loss",
            "Investment in equipment",
            "Skill and permanence"
        ],
        primary_authority=[
            "Fair Labor Standards Act",
            "State statutes (e.g., California Labor Code § 2750.3)",
            "U.S. Dept. of Labor Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Worker claims employee status",
        counter_arguments=[
            "Worker is subject to control",
            "Work is integral to business",
            "No independent business"
        ],
        resolution_strategy="Apply ABC or economic reality test, review contracts, and analyze work practices.",
        entity_scope="Employers and workers",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Dynamex Operations West, Inc. v. Superior Court, 416 P.3d 1 (Cal. 2018)"
    ),
    DoctrineBlock(
        topic="At-Will Employment - Exceptions to Terminability",
        keywords=["at-will employment", "termination", "exceptions", "public policy", "implied contract"],
        conclusion_template="The termination of {employee_name} is/is not subject to an exception to at-will employment.",
        reasoning_framework="""At-will employment allows termination for any reason except:
1. Public policy exception (e.g., retaliation for whistleblowing).
2. Implied contract exception (promises in handbook or oral assurances).
3. Covenant of good faith and fair dealing (some states).
Analyze facts for evidence of exception, employer policies, and state law.""",
        key_factors=[
            "Public policy violation",
            "Implied contract",
            "Good faith and fair dealing",
            "Employer policies"
        ],
        primary_authority=[
            "State statutes and common law",
            "Restatement (Second) of Employment § 2.02"
        ],
        burden_holder="Employee",
        adversary_position="Employer asserts at-will status",
        counter_arguments=[
            "No public policy violation",
            "No implied contract",
            "Termination was in good faith"
        ],
        resolution_strategy="Review termination records, handbook language, and state law.",
        entity_scope="Employers and employees",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="Toussaint v. Blue Cross & Blue Shield of Michigan, 292 N.W.2d 880 (Mich. 1980)"
    ),
    DoctrineBlock(
        topic="Employee Handbook - Contractual Effect and Disclaimers",
        keywords=["employee handbook", "contract", "disclaimer", "employment terms", "policy"],
        conclusion_template="The employee handbook {handbook_name} does/does not create contractual rights for {employee_name}.",
        reasoning_framework="""Employee handbooks may create contractual rights if:
1. Handbook contains specific promises regarding employment terms.
2. Disclaimers are absent or ineffective.
3. Employee relied on handbook provisions.
4. State law governs enforceability.
Analyze handbook language, disclaimers, and employee reliance.""",
        key_factors=[
            "Specific promises in handbook",
            "Presence and effectiveness of disclaimers",
            "Employee reliance",
            "State law"
        ],
        primary_authority=[
            "State statutes and common law",
            "Restatement (Second) of Contracts"
        ],
        burden_holder="Employee",
        adversary_position="Employer denies contractual effect",
        counter_arguments=[
            "Effective disclaimer",
            "No specific promise",
            "No reliance"
        ],
        resolution_strategy="Review handbook, disclaimers, and employee testimony.",
        entity_scope="Employers and employees",
        confidence=0.81,
        confidence_zone="Medium",
        controlling_precedent="Perry v. Sindermann, 408 U.S. 593 (1972)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Administrative",
        keywords=["FLSA", "overtime", "exemption", "administrative", "salary basis", "primary duty"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the administrative exemption under FLSA.",
        reasoning_framework="""Administrative exemption requires:
1. Salary basis ($684/week minimum).
2. Primary duty is office or non-manual work related to management or general business operations.
3. Exercise of discretion and independent judgment with respect to matters of significance.
Analyze job duties, salary, and decision-making authority.""",
        key_factors=[
            "Salary basis",
            "Primary duty (management/business operations)",
            "Discretion and independent judgment"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(1)",
            "29 C.F.R. § 541.200"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is routine or clerical",
            "No discretion or judgment",
            "Salary basis not met"
        ],
        resolution_strategy="Review job descriptions, salary records, and decision-making evidence.",
        entity_scope="Covered employers and employees",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="Davis v. J.P. Morgan Chase & Co., 587 F.3d 529 (2d Cir. 2009)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Professional",
        keywords=["FLSA", "overtime", "exemption", "professional", "salary basis", "learned profession"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the professional exemption under FLSA.",
        reasoning_framework="""Professional exemption applies to employees:
1. Compensated on a salary basis ($684/week minimum).
2. Primary duty is work requiring advanced knowledge in a field of science or learning, acquired by specialized education.
3. Includes teachers, lawyers, doctors, engineers, etc.
Analyze educational requirements, job duties, and salary.""",
        key_factors=[
            "Salary basis",
            "Advanced knowledge",
            "Specialized education",
            "Primary duty"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(1)",
            "29 C.F.R. § 541.300"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work does not require advanced knowledge",
            "No specialized education",
            "Salary basis not met"
        ],
        resolution_strategy="Review educational credentials, job descriptions, and salary records.",
        entity_scope="Covered employers and employees",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="Young v. Cooper Cameron Corp., 586 F.3d 201 (2d Cir. 2009)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Outside Sales",
        keywords=["FLSA", "overtime", "exemption", "outside sales", "primary duty"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the outside sales exemption under FLSA.",
        reasoning_framework="""Outside sales exemption applies if:
1. Primary duty is making sales or obtaining orders/contracts.
2. Customarily and regularly engaged away from employer’s place of business.
3. No minimum salary requirement.
Analyze sales activities, work location, and job duties.""",
        key_factors=[
            "Primary duty (sales)",
            "Work performed away from business",
            "Nature of sales activities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(1)",
            "29 C.F.R. § 541.500"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work performed at employer’s location",
            "Not engaged in sales",
            "No regular sales activity"
        ],
        resolution_strategy="Review sales records, travel logs, and job descriptions.",
        entity_scope="Covered employers and employees",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="Christopher v. SmithKline Beecham Corp., 567 U.S. 142 (2012)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Highly Compensated Employees",
        keywords=["FLSA", "overtime", "exemption", "highly compensated", "salary"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify as a highly compensated employee under FLSA exemption.",
        reasoning_framework="""Highly compensated employees are exempt if:
1. Total annual compensation is $107,432+.
2. Customarily and regularly performs at least one exempt duty (executive, administrative, or professional).
Analyze compensation records and job duties.""",
        key_factors=[
            "Annual compensation ($107,432+)",
            "Exempt duties performed",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 C.F.R. § 541.601"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Insufficient compensation",
            "No exempt duties performed"
        ],
        resolution_strategy="Review compensation records and job descriptions.",
        entity_scope="Covered employers and employees",
        confidence=0.81,
        confidence_zone="Medium",
        controlling_precedent="IntraComm, Inc. v. Bajaj, 492 F.3d 285 (4th Cir. 2007)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Computer Employees",
        keywords=["FLSA", "overtime", "exemption", "computer employees", "salary", "hourly"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the computer employee exemption under FLSA.",
        reasoning_framework="""Computer employee exemption applies if:
1. Compensated on a salary basis ($684/week) or hourly ($27.63/hour).
2. Primary duty is application of systems analysis, programming, software engineering, or similar.
Analyze compensation and job duties.""",
        key_factors=[
            "Salary or hourly compensation",
            "Primary duty (computer-related)",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 C.F.R. § 541.400"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not computer-related",
            "Compensation below threshold"
        ],
        resolution_strategy="Review compensation records and job descriptions.",
        entity_scope="Covered employers and computer employees",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="Pippins v. KPMG LLP, 759 F.3d 235 (2d Cir. 2014)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Creative Professional",
        keywords=["FLSA", "overtime", "exemption", "creative professional", "salary", "artistic"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the creative professional exemption under FLSA.",
        reasoning_framework="""Creative professional exemption applies if:
1. Compensated on a salary basis ($684/week minimum).
2. Primary duty is work requiring invention, imagination, originality, or talent in recognized artistic fields.
Analyze job duties, compensation, and creative requirements.""",
        key_factors=[
            "Salary basis",
            "Creative/artistic duties",
            "Originality and talent"
        ],
        primary_authority=[
            "29 C.F.R. § 541.302"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not creative",
            "No originality or talent",
            "Salary basis not met"
        ],
        resolution_strategy="Review job descriptions, portfolio, and compensation records.",
        entity_scope="Covered employers and creative professionals",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="Reich v. Newspapers of New England, Inc., 44 F.3d 1060 (1st Cir. 1995)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Learned Professional",
        keywords=["FLSA", "overtime", "exemption", "learned professional", "advanced knowledge"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the learned professional exemption under FLSA.",
        reasoning_framework="""Learned professional exemption applies if:
1. Compensated on a salary basis ($684/week minimum).
2. Primary duty requires advanced knowledge in a field of science or learning.
3. Knowledge acquired by prolonged specialized instruction.
Analyze educational credentials and job duties.""",
        key_factors=[
            "Salary basis",
            "Advanced knowledge",
            "Specialized instruction",
            "Primary duty"
        ],
        primary_authority=[
            "29 C.F.R. § 541.301"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "No advanced knowledge",
            "No specialized instruction",
            "Salary basis not met"
        ],
        resolution_strategy="Review educational records, job descriptions, and compensation.",
        entity_scope="Covered employers and learned professionals",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="Young v. Cooper Cameron Corp., 586 F.3d 201 (2d Cir. 2009)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Executive Assistant",
        keywords=["FLSA", "overtime", "exemption", "executive assistant", "salary", "management"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the executive assistant exemption under FLSA.",
        reasoning_framework="""Executive assistant exemption applies if:
1. Salary basis ($684/week minimum).
2. Primary duty is assisting high-level executives with management functions.
3. Exercise of discretion and independent judgment.
Analyze job duties, salary, and decision-making authority.""",
        key_factors=[
            "Salary basis",
            "Management assistance",
            "Discretion and judgment"
        ],
        primary_authority=[
            "29 C.F.R. § 541.203"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is clerical",
            "No discretion or judgment",
            "Salary basis not met"
        ],
        resolution_strategy="Review job descriptions, salary records, and executive testimony.",
        entity_scope="Covered employers and executive assistants",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="Davis v. J.P. Morgan Chase & Co., 587 F.3d 529 (2d Cir. 2009)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Combination Exemption",
        keywords=["FLSA", "overtime", "exemption", "combination", "multiple duties"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for combination exemption under FLSA.",
        reasoning_framework="""Combination exemption applies if employee performs duties from two or more exempt categories (executive, administrative, professional).
1. Salary basis ($684/week minimum).
2. Duties collectively meet exemption criteria.
Analyze job duties, salary, and exemption categories.""",
        key_factors=[
            "Salary basis",
            "Combination of exempt duties",
            "Exemption criteria met"
        ],
        primary_authority=[
            "29 C.F.R. § 541.708"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Duties do not meet exemption criteria",
            "Salary basis not met"
        ],
        resolution_strategy="Review job descriptions, salary records, and exemption analysis.",
        entity_scope="Covered employers and employees",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="IntraComm, Inc. v. Bajaj, 492 F.3d 285 (4th Cir. 2007)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Retail or Service Establishment",
        keywords=["FLSA", "overtime", "exemption", "retail", "service establishment", "commission"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the retail or service establishment exemption under FLSA.",
        reasoning_framework="""Retail or service establishment exemption applies if:
1. Employee works at a retail/service establishment.
2. Regular rate of pay exceeds 1.5 times minimum wage.
3. More than half of earnings are commissions.
Analyze pay records, establishment type, and commission structure.""",
        key_factors=[
            "Retail/service establishment",
            "Regular rate of pay",
            "Commission earnings"
        ],
        primary_authority=[
            "29 U.S.C. § 207(i)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Establishment not retail/service",
            "Earnings not commission-based",
            "Pay rate below threshold"
        ],
        resolution_strategy="Review pay records, commission statements, and establishment classification.",
        entity_scope="Retail/service employers and employees",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Motor Carrier Act",
        keywords=["FLSA", "overtime", "exemption", "motor carrier", "interstate commerce"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the motor carrier exemption under FLSA.",
        reasoning_framework="""Motor carrier exemption applies if:
1. Employee is a driver, loader, mechanic, or similar.
2. Works for employer subject to Motor Carrier Act.
3. Engaged in interstate commerce.
Analyze job duties, employer coverage, and commerce involvement.""",
        key_factors=[
            "Job duties (driver, loader, mechanic)",
            "Employer subject to Motor Carrier Act",
            "Interstate commerce"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(1)",
            "49 U.S.C. § 31502"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not subject to Act",
            "No interstate commerce",
            "Job duties not covered"
        ],
        resolution_strategy="Review job descriptions, employer records, and commerce evidence.",
        entity_scope="Motor carrier employers and employees",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="Morrison v. Quality Transports Services, Inc., 474 F. Supp. 2d 130 (D. Mass. 2007)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Seasonal Recreational Establishment",
        keywords=["FLSA", "overtime", "exemption", "seasonal", "recreational", "establishment"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the seasonal recreational establishment exemption under FLSA.",
        reasoning_framework="""Seasonal recreational establishment exemption applies if:
1. Establishment operates for less than seven months per year or earns most revenue in six months.
2. Employee works for such establishment.
Analyze operating schedule and revenue records.""",
        key_factors=[
            "Seasonal operation",
            "Revenue distribution",
            "Employment at establishment"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(3)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Establishment operates year-round",
            "Revenue not seasonal",
            "Employee not covered"
        ],
        resolution_strategy="Review operating schedules, revenue records, and employment history.",
        entity_scope="Seasonal recreational employers and employees",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="Jeffery v. Sarasota White Sox, Inc., 64 F.3d 590 (11th Cir. 1995)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Agricultural Employees",
        keywords=["FLSA", "overtime", "exemption", "agricultural", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the agricultural exemption under FLSA.",
        reasoning_framework="""Agricultural exemption applies if:
1. Employee is engaged in primary agriculture (farming, cultivation, harvesting).
2. Work is performed for employer in agriculture.
Analyze job duties and employer industry.""",
        key_factors=[
            "Primary agriculture duties",
            "Employer in agriculture",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(12)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not agricultural",
            "Employer not in agriculture"
        ],
        resolution_strategy="Review job descriptions, employer records, and industry classification.",
        entity_scope="Agricultural employers and employees",
        confidence=0.72,
        confidence_zone="Medium",
        controlling_precedent="Holly Farms Corp. v. NLRB, 517 U.S. 392 (1996)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Domestic Service Employees",
        keywords=["FLSA", "overtime", "exemption", "domestic service", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the domestic service exemption under FLSA.",
        reasoning_framework="""Domestic service exemption applies if:
1. Employee provides services in private home (cleaning, childcare, etc.).
2. Certain live-in employees exempt from overtime.
Analyze job duties and living arrangements.""",
        key_factors=[
            "Domestic service duties",
            "Private home employment",
            "Live-in status"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(21)",
            "29 C.F.R. § 552.102"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not domestic service",
            "Employee not live-in"
        ],
        resolution_strategy="Review job descriptions, employment records, and living arrangements.",
        entity_scope="Private household employers and employees",
        confidence=0.71,
        confidence_zone="Medium",
        controlling_precedent="Home Care Ass'n of America v. Weil, 799 F.3d 1084 (D.C. Cir. 2015)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Small Newspaper Employees",
        keywords=["FLSA", "overtime", "exemption", "small newspaper", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the small newspaper exemption under FLSA.",
        reasoning_framework="""Small newspaper exemption applies if:
1. Newspaper has circulation under 4,000.
2. Employee works for such newspaper.
Analyze circulation records and employment status.""",
        key_factors=[
            "Newspaper circulation",
            "Employment at newspaper",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(8)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Circulation exceeds threshold",
            "Employee not covered"
        ],
        resolution_strategy="Review circulation records, employment history, and job descriptions.",
        entity_scope="Small newspaper employers and employees",
        confidence=0.70,
        confidence_zone="Medium",
        controlling_precedent="Reich v. Newspapers of New England, Inc., 44 F.3d 1060 (1st Cir. 1995)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Fishing Employees",
        keywords=["FLSA", "overtime", "exemption", "fishing", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the fishing exemption under FLSA.",
        reasoning_framework="""Fishing exemption applies if:
1. Employee is employed in fishing operations (catching, processing, transporting fish).
2. Work is performed for employer in fishing industry.
Analyze job duties and employer industry.""",
        key_factors=[
            "Fishing operations duties",
            "Employer in fishing industry",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(19)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not fishing",
            "Employer not in fishing industry"
        ],
        resolution_strategy="Review job descriptions, employer records, and industry classification.",
        entity_scope="Fishing employers and employees",
        confidence=0.69,
        confidence_zone="Medium",
        controlling_precedent="Marshall v. Gulf & Western Industries, Inc., 554 F.2d 615 (4th Cir. 1977)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Switchboard Operators",
        keywords=["FLSA", "overtime", "exemption", "switchboard operator", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the switchboard operator exemption under FLSA.",
        reasoning_framework="""Switchboard operator exemption applies if:
1. Employee is employed as switchboard operator at telephone exchange with fewer than 750 stations.
2. Work is performed for such employer.
Analyze employer records and job duties.""",
        key_factors=[
            "Switchboard operator duties",
            "Telephone exchange size",
            "Employment status"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(10)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Exchange exceeds station threshold",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, station count, and job descriptions.",
        entity_scope="Telephone exchange employers and employees",
        confidence=0.68,
        confidence_zone="Medium",
        controlling_precedent="Reich v. Newspapers of New England, Inc., 44 F.3d 1060 (1st Cir. 1995)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Taxicab Drivers",
        keywords=["FLSA", "overtime", "exemption", "taxicab driver", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the taxicab driver exemption under FLSA.",
        reasoning_framework="""Taxicab driver exemption applies if:
1. Employee is employed as taxicab driver.
2. Work is performed for employer in taxicab business.
Analyze job duties and employer industry.""",
        key_factors=[
            "Taxicab driver duties",
            "Employer in taxicab business",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(17)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not taxicab driving",
            "Employer not in taxicab business"
        ],
        resolution_strategy="Review job descriptions, employer records, and industry classification.",
        entity_scope="Taxicab employers and drivers",
        confidence=0.67,
        confidence_zone="Medium",
        controlling_precedent="Rosenberg v. Renal Advantage, Inc., 2013 WL 3205422 (D. Nev. 2013)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Newspaper Delivery Employees",
        keywords=["FLSA", "overtime", "exemption", "newspaper delivery", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the newspaper delivery exemption under FLSA.",
        reasoning_framework="""Newspaper delivery exemption applies if:
1. Employee is engaged in delivery of newspapers to consumers.
2. Work is performed for employer in newspaper business.
Analyze job duties and employer industry.""",
        key_factors=[
            "Newspaper delivery duties",
            "Employer in newspaper business",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(8)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not newspaper delivery",
            "Employer not in newspaper business"
        ],
        resolution_strategy="Review job descriptions, employer records, and industry classification.",
        entity_scope="Newspaper employers and delivery employees",
        confidence=0.66,
        confidence_zone="Medium",
        controlling_precedent="Reich v. Newspapers of New England, Inc., 44 F.3d 1060 (1st Cir. 1995)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Amusement or Recreational Establishments",
        keywords=["FLSA", "overtime", "exemption", "amusement", "recreational", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the amusement or recreational establishment exemption under FLSA.",
        reasoning_framework="""Amusement or recreational establishment exemption applies if:
1. Establishment operates for less than seven months per year or earns most revenue in six months.
2. Employee works for such establishment.
Analyze operating schedule and revenue records.""",
        key_factors=[
            "Amusement/recreational operation",
            "Seasonal schedule",
            "Revenue distribution"
        ],
        primary_authority=[
            "29 U.S.C. § 213(a)(3)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Establishment operates year-round",
            "Revenue not seasonal",
            "Employee not covered"
        ],
        resolution_strategy="Review operating schedules, revenue records, and employment history.",
        entity_scope="Amusement/recreational employers and employees",
        confidence=0.65,
        confidence_zone="Medium",
        controlling_precedent="Jeffery v. Sarasota White Sox, Inc., 64 F.3d 590 (11th Cir. 1995)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Local Delivery Companies",
        keywords=["FLSA", "overtime", "exemption", "local delivery", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the local delivery exemption under FLSA.",
        reasoning_framework="""Local delivery exemption applies if:
1. Employee is engaged in local delivery of goods.
2. Work is performed for employer in local delivery business.
Analyze job duties and employer industry.""",
        key_factors=[
            "Local delivery duties",
            "Employer in local delivery business",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(11)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not local delivery",
            "Employer not in local delivery business"
        ],
        resolution_strategy="Review job descriptions, employer records, and industry classification.",
        entity_scope="Local delivery employers and employees",
        confidence=0.64,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Motion Picture Theaters",
        keywords=["FLSA", "overtime", "exemption", "motion picture theater", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the motion picture theater exemption under FLSA.",
        reasoning_framework="""Motion picture theater exemption applies if:
1. Employee works for motion picture theater.
2. Work is performed for such employer.
Analyze job duties and employer industry.""",
        key_factors=[
            "Motion picture theater duties",
            "Employer in theater business",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(27)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Work is not theater-related",
            "Employer not in theater business"
        ],
        resolution_strategy="Review job descriptions, employer records, and industry classification.",
        entity_scope="Motion picture theater employers and employees",
        confidence=0.63,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Certain Nonprofit Organizations",
        keywords=["FLSA", "overtime", "exemption", "nonprofit", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the nonprofit exemption under FLSA.",
        reasoning_framework="""Nonprofit exemption applies if:
1. Employee works for nonprofit organization not engaged in commercial activities.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Nonprofit status",
            "Commercial activity",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 203(r)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer engaged in commercial activity",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, nonprofit status, and job descriptions.",
        entity_scope="Nonprofit employers and employees",
        confidence=0.62,
        confidence_zone="Medium",
        controlling_precedent="Tony & Susan Alamo Foundation v. Secretary of Labor, 471 U.S. 290 (1985)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Religious Organizations",
        keywords=["FLSA", "overtime", "exemption", "religious organization", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the religious organization exemption under FLSA.",
        reasoning_framework="""Religious organization exemption applies if:
1. Employee works for religious organization not engaged in commercial activities.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Religious organization status",
            "Commercial activity",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 203(r)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer engaged in commercial activity",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, religious status, and job descriptions.",
        entity_scope="Religious employers and employees",
        confidence=0.61,
        confidence_zone="Medium",
        controlling_precedent="Tony & Susan Alamo Foundation v. Secretary of Labor, 471 U.S. 290 (1985)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Educational Institutions",
        keywords=["FLSA", "overtime", "exemption", "educational institution", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the educational institution exemption under FLSA.",
        reasoning_framework="""Educational institution exemption applies if:
1. Employee works for educational institution.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Educational institution status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 203(e)(2)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not educational institution",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, educational status, and job descriptions.",
        entity_scope="Educational institution employers and employees",
        confidence=0.60,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Hospitals",
        keywords=["FLSA", "overtime", "exemption", "hospital", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the hospital exemption under FLSA.",
        reasoning_framework="""Hospital exemption applies if:
1. Employee works for hospital.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Hospital status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 203(e)(2)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not hospital",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, hospital status, and job descriptions.",
        entity_scope="Hospital employers and employees",
        confidence=0.59,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Public Agencies",
        keywords=["FLSA", "overtime", "exemption", "public agency", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the public agency exemption under FLSA.",
        reasoning_framework="""Public agency exemption applies if:
1. Employee works for public agency (government).
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Public agency status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 203(e)(2)(C)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not public agency",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, agency status, and job descriptions.",
        entity_scope="Public agency employers and employees",
        confidence=0.58,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Railroads",
        keywords=["FLSA", "overtime", "exemption", "railroad", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the railroad exemption under FLSA.",
        reasoning_framework="""Railroad exemption applies if:
1. Employee works for railroad.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Railroad status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(2)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not railroad",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, railroad status, and job descriptions.",
        entity_scope="Railroad employers and employees",
        confidence=0.57,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Air Carriers",
        keywords=["FLSA", "overtime", "exemption", "air carrier", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the air carrier exemption under FLSA.",
        reasoning_framework="""Air carrier exemption applies if:
1. Employee works for air carrier.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Air carrier status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(3)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not air carrier",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, air carrier status, and job descriptions.",
        entity_scope="Air carrier employers and employees",
        confidence=0.56,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Maritime Vessels",
        keywords=["FLSA", "overtime", "exemption", "maritime vessel", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the maritime vessel exemption under FLSA.",
        reasoning_framework="""Maritime vessel exemption applies if:
1. Employee works for maritime vessel.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Maritime vessel status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(6)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not maritime vessel",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, vessel status, and job descriptions.",
        entity_scope="Maritime vessel employers and employees",
        confidence=0.55,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Fire Protection and Law Enforcement Agencies",
        keywords=["FLSA", "overtime", "exemption", "fire protection", "law enforcement", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the fire protection/law enforcement exemption under FLSA.",
        reasoning_framework="""Fire protection and law enforcement exemption applies if:
1. Employee works for fire protection or law enforcement agency.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Fire protection/law enforcement status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(20)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not fire/law enforcement",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, agency status, and job descriptions.",
        entity_scope="Fire/law enforcement employers and employees",
        confidence=0.54,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Certain Transportation Companies",
        keywords=["FLSA", "overtime", "exemption", "transportation company", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the transportation company exemption under FLSA.",
        reasoning_framework="""Transportation company exemption applies if:
1. Employee works for transportation company.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Transportation company status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(1)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not transportation company",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, company status, and job descriptions.",
        entity_scope="Transportation company employers and employees",
        confidence=0.53,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Certain Public Utilities",
        keywords=["FLSA", "overtime", "exemption", "public utility", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the public utility exemption under FLSA.",
        reasoning_framework="""Public utility exemption applies if:
1. Employee works for public utility.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Public utility status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(13)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not public utility",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, utility status, and job descriptions.",
        entity_scope="Public utility employers and employees",
        confidence=0.52,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Certain Shipbuilding and Repair Companies",
        keywords=["FLSA", "overtime", "exemption", "shipbuilding", "repair company", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the shipbuilding/repair company exemption under FLSA.",
        reasoning_framework="""Shipbuilding and repair company exemption applies if:
1. Employee works for shipbuilding or repair company.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Shipbuilding/repair company status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(14)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not shipbuilding/repair company",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, company status, and job descriptions.",
        entity_scope="Shipbuilding/repair company employers and employees",
        confidence=0.51,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
    ),
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Employees of Certain Logging Companies",
        keywords=["FLSA", "overtime", "exemption", "logging company", "employee"],
        conclusion_template="The employee {employee_name} qualifies/does not qualify for the logging company exemption under FLSA.",
        reasoning_framework="""Logging company exemption applies if:
1. Employee works for logging company.
2. Work is performed for such employer.
Analyze employer status and job duties.""",
        key_factors=[
            "Logging company status",
            "Job responsibilities"
        ],
        primary_authority=[
            "29 U.S.C. § 213(b)(15)"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims non-exempt status",
        counter_arguments=[
            "Employer not logging company",
            "Employee not covered"
        ],
        resolution_strategy="Review employer records, company status, and job descriptions.",
        entity_scope="Logging company employers and employees",
        confidence=0.50,
        confidence_zone="Medium",
        controlling_precedent="Alvarez v. IBP, Inc., 339 F.3d 894 (9th Cir. 2003)"
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
        if any(keyword_lower in k.lower() for k in doctrine.keywords) or keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]