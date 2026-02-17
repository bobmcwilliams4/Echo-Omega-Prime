"""
ENT10 Labor & Employment Engine v1.0.0
TIE-grade engine for labor and employment law analysis
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

ENGINE_ID = "ENT10"
ENGINE_NAME = "Labor & Employment Engine"
VERSION = "1.0.0"
PORT = 9150

logger.add(f"logs/{ENGINE_ID}_{{time}}.log", rotation="100 MB", retention="30 days", level="INFO")

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    WAGE_HOUR = "WAGE_HOUR"
    LEAVE = "LEAVE"
    ACCOMMODATION = "ACCOMMODATION"
    DISCRIMINATION = "DISCRIMINATION"
    LABOR_RELATIONS = "LABOR_RELATIONS"
    BENEFITS = "BENEFITS"
    NON_COMPETE = "NON_COMPETE"
    CLASSIFICATION = "CLASSIFICATION"
    TERMINATION = "TERMINATION"
    HANDBOOK = "HANDBOOK"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="FLSA Overtime Exemption - Executive",
        keywords=["overtime", "exempt", "executive", "salary", "management", "FLSA"],
        conclusion_template=[
            "Executive exemption requires: salary >= $684/week, primary duty managing enterprise or department, regularly directs 2+ employees.",
            "Employee meets/fails exemption because [management duties analysis].",
            "Recommend treating as [exempt/non-exempt] and [maintain time records/pay overtime]."
        ],
        reasoning_framework="""
29 USC §213(a)(1) exempts bona fide executive employees from FLSA overtime.
29 CFR §541.100 defines executive: (1) salary >= $684/week on salary basis, (2) primary duty managing enterprise or recognized department, (3) customarily and regularly directs work of 2+ employees, (4) authority to hire/fire or recommendations given particular weight.
Primary duty = principal, main, major, or most important duty. Determined by nature of work, time spent, relative freedom from supervision, relationship between salary and wages paid to hourly workers.
Concurrent duties test: Employee who performs exempt and non-exempt work may still qualify if primary duty is management.
Salary basis: Must receive predetermined amount each pay period, not subject to reduction based on quality or quantity of work (subject to narrow exceptions for disciplinary deductions in full-day increments).
        """,
        key_factors=[
            "Actual job duties, not job title or description",
            "Percentage of time on managerial tasks vs non-exempt tasks",
            "Genuine authority to hire, fire, discipline, or recommend personnel actions",
            "Management of a department (recognized subdivision with permanent status)",
            "Salary level meets threshold ($684/week, $35,568/year)",
            "Salary paid on true salary basis (no improper deductions)"
        ],
        primary_authority=[
            "29 USC §213(a)(1) - FLSA exemptions",
            "29 CFR §541.100-106 - Executive exemption regulations",
            "29 CFR §541.700 - Primary duty test",
            "DOL Fact Sheet #17B - Exemption for Executive Employees"
        ],
        burden_holder="Employer bears burden of proving exemption applicability",
        adversary_position="Employee argues performing substantial non-exempt work, lacks genuine management authority, salary basis violations invalidate exemption",
        counter_arguments=[
            "Employee spends majority of time on non-managerial tasks such as customer service or production work",
            "Recommendations on personnel actions are not given particular weight by higher management",
            "Does not supervise 2 full-time equivalent employees (4+ half-time employees may suffice)",
            "Salary docked for partial-day absences or performance issues violates salary basis test",
            "Department managed is not a recognized subdivision with permanent status"
        ],
        resolution_strategy="Conduct job analysis documenting actual duties, time allocation, authority exercised. Review salary deduction practices. If exemption questionable, reclassify to non-exempt and implement time tracking.",
        entity_scope="All employers covered by FLSA (enterprises with $500K+ annual revenue or engaged in interstate commerce)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when salary >= threshold and clear management of 2+ employees; AGGRESSIVE when concurrent duties substantial; DISCLOSURE if salary basis violations; HIGH_RISK if no genuine hire/fire authority",
        controlling_precedent="Auer v Robbins, 519 US 452 (1997) - deference to DOL regulations; Christopher v SmithKline Beecham, 567 US 142 (2012) - pharmaceutical sales reps not exempt outside salespersons"
    ),
    DoctrineBlock(
        topic="FMLA Eligibility and Entitlement",
        keywords=["FMLA", "leave", "12 weeks", "serious health condition", "eligible employee"],
        conclusion_template=[
            "Employee is/is not FMLA-eligible because [1250 hours and 12 months analysis].",
            "Condition qualifies/does not qualify as serious health condition under [incapacity/treatment test].",
            "Employer must [grant unpaid leave/may deny if ineligible]."
        ],
        reasoning_framework="""
29 USC §2612 grants eligible employees 12 workweeks of unpaid leave per 12-month period for: (1) birth/care of newborn, (2) placement of child for adoption/foster care, (3) care for spouse/child/parent with serious health condition, (4) employee's own serious health condition making them unable to perform job functions.
Eligible employee: employed for 12+ months (need not be consecutive), worked 1250+ hours in 12 months preceding leave, employer has 50+ employees within 75-mile radius.
Serious health condition: illness/injury/impairment/physical/mental condition involving either (A) inpatient care in hospital/hospice/residential facility, or (B) continuing treatment by healthcare provider, defined as: (1) incapacity 3+ consecutive days plus 2+ treatments by healthcare provider, or (2) incapacity due to pregnancy or prenatal care, or (3) incapacity due to chronic serious health condition requiring periodic visits and continuing treatment, or (4) permanent/long-term incapacity (e.g., Alzheimer's, terminal cancer).
Intermittent or reduced schedule leave permitted when medically necessary for serious health condition.
        """,
        key_factors=[
            "Employee worked 1250 hours in prior 12 months (based on FLSA principles)",
            "Employee completed 12 months of employment (need not be consecutive)",
            "Employer has 50+ employees within 75 miles of employee's worksite",
            "Condition involves inpatient care OR continuing treatment meeting regulatory definition",
            "Healthcare provider certification supports medical necessity of leave",
            "Intermittent leave schedule medically necessary, not merely preferred by employee"
        ],
        primary_authority=[
            "29 USC §2611-2612 - FMLA definitions and leave entitlement",
            "29 CFR §825.110 - Eligible employee",
            "29 CFR §825.115 - Serious health condition",
            "29 CFR §825.202-203 - Intermittent and reduced schedule leave"
        ],
        burden_holder="Employee must provide sufficient information to put employer on notice of FMLA-qualifying reason; employer may require medical certification",
        adversary_position="Employer argues employee ineligible (hours/tenure), condition not serious (routine illness), or leave not medically necessary (elective timing)",
        counter_arguments=[
            "Employee worked fewer than 1250 hours due to part-time status or recent hire",
            "Employer has fewer than 50 employees within 75-mile radius (measured as crow flies)",
            "Condition is routine illness (cold, flu, minor infection) not meeting 3-day incapacity plus 2 treatments test",
            "Employee requests intermittent leave for convenience rather than medical necessity",
            "Employee failed to provide sufficient notice (30 days when foreseeable, as soon as practicable when emergency)"
        ],
        resolution_strategy="Determine eligibility via payroll records (1250 hours, 12 months tenure) and employee count within 75 miles. Obtain healthcare provider certification (DOL Form WH-380) to verify serious health condition. If certified, grant leave and maintain health benefits.",
        entity_scope="Covered employers: private employers with 50+ employees in 20+ workweeks in current or prior calendar year, plus all public agencies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when certification supports serious health condition; AGGRESSIVE when condition borderline (e.g., 2-day flu); DISCLOSURE for mental health conditions; HIGH_RISK if employer retaliates for leave request",
        controlling_precedent="Ragsdale v Wolverine World Wide, 535 US 81 (2002) - FMLA notice requirements; Spangler v Federal Home Loan Bank, 278 F3d 847 (8th Cir 2002) - chronic conditions"
    ),
    DoctrineBlock(
        topic="ADA Reasonable Accommodation - Interactive Process",
        keywords=["ADA", "accommodation", "disability", "interactive process", "undue hardship"],
        conclusion_template=[
            "Employee has/does not have a disability under ADA because [substantial limitation analysis].",
            "Proposed accommodation is/is not reasonable and does/does not impose undue hardship.",
            "Employer must [engage in interactive process/provide accommodation/deny as undue hardship]."
        ],
        reasoning_framework="""
42 USC §12112(b)(5)(A) requires employers to make reasonable accommodations to known physical/mental limitations of qualified individual with disability unless undue hardship.
Disability: (1) physical or mental impairment that substantially limits one or more major life activities, (2) record of such impairment, or (3) regarded as having such impairment.
2008 ADAAA Amendments Act: broadened definition, made "substantially limits" easier to meet, expanded major life activities to include major bodily functions (immune system, cell growth, etc.).
Qualified individual: can perform essential functions of job with or without reasonable accommodation.
Interactive process: employer and employee engage in informal dialogue to identify accommodation that enables employee to perform essential functions. Failure to engage in good faith can be independent ADA violation.
Reasonable accommodation examples: modified work schedule, reassignment to vacant position, modified equipment, leave of absence, removal of marginal functions.
Undue hardship: significant difficulty or expense considering employer's size, financial resources, nature of operation. Direct threat defense: poses significant risk to health/safety that cannot be eliminated by reasonable accommodation.
        """,
        key_factors=[
            "Impairment substantially limits major life activity (walking, seeing, hearing, working, sleeping, eating, concentrating, communicating, caring for oneself)",
            "Employee can perform essential functions of job with accommodation",
            "Proposed accommodation is effective (enables performance of essential functions)",
            "Cost and difficulty of accommodation relative to employer's resources",
            "Both parties engaged in good faith interactive process",
            "Accommodation does not create direct threat to safety"
        ],
        primary_authority=[
            "42 USC §12111-12112 - ADA employment provisions",
            "29 CFR §1630.2(o) - Qualified individual with disability",
            "29 CFR §1630.2(p) - Undue hardship",
            "EEOC Enforcement Guidance on Reasonable Accommodation (2002)"
        ],
        burden_holder="Employee bears initial burden of showing disability and need for accommodation; employer bears burden of proving undue hardship or direct threat",
        adversary_position="Employee argues failure to engage in interactive process, refusal of effective accommodation, or pretextual undue hardship claim; employer argues no disability, cannot perform essential functions even with accommodation",
        counter_arguments=[
            "Impairment is transitory and minor (under 6 months) so not a disability",
            "Employee cannot perform essential functions even with reasonable accommodation",
            "Proposed accommodation fundamentally alters nature of job or eliminates essential function",
            "Cost of accommodation creates undue hardship given employer's financial condition",
            "Accommodation requires elimination of another employee's position (not required)",
            "Employee refused to engage in interactive process or rejected all proposed accommodations"
        ],
        resolution_strategy="Obtain medical documentation of impairment and limitations. Identify essential vs marginal job functions. Explore multiple accommodation options through interactive dialogue. Document process and cost analysis. If undue hardship, show particularized assessment of financial impact.",
        entity_scope="Employers with 15+ employees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when interactive process documented and legitimate undue hardship; AGGRESSIVE when cost analysis marginal; DISCLOSURE for mental health accommodations; HIGH_RISK if interactive process not attempted",
        controlling_precedent="US Airways v Barnett, 535 US 391 (2002) - seniority system as undue hardship; Chevron USA Inc v Echazabal, 536 US 73 (2002) - direct threat defense"
    ),
    DoctrineBlock(
        topic="Title VII Disparate Treatment - McDonnell Douglas Framework",
        keywords=["discrimination", "Title VII", "disparate treatment", "pretext", "McDonnell Douglas"],
        conclusion_template=[
            "Employee establishes/fails prima facie case of [race/sex/religion/national origin] discrimination.",
            "Employer's stated reason is/is not legitimate and nondiscriminatory.",
            "Evidence of pretext includes [comparator analysis/temporal proximity/shifting explanations]."
        ],
        reasoning_framework="""
42 USC §2000e-2(a) prohibits discrimination based on race, color, religion, sex, or national origin.
McDonnell Douglas burden-shifting framework (411 US 792, 1973):
(1) Plaintiff establishes prima facie case: (a) member of protected class, (b) qualified for position, (c) adverse employment action, (d) position remained open or filled by person outside protected class (or similarly situated person outside class treated better).
(2) Burden shifts to employer to articulate legitimate, nondiscriminatory reason for action.
(3) Burden shifts back to plaintiff to prove reason is pretext for discrimination.
Pretext shown by: temporal proximity between protected activity and adverse action, inconsistent application of policy, more favorable treatment of similarly situated employees outside protected class, shifting or inconsistent explanations, employer's stated reason factually false, statistical evidence of discriminatory pattern.
Similarly situated comparator: engaged in same/similar conduct, similar job responsibilities, same supervisor, same performance standards. Must be nearly identical to defeat summary judgment.
Mixed motive: plaintiff shows protected characteristic was motivating factor; employer may avoid damages (but not injunctive relief) by showing would have made same decision anyway (Price Waterhouse, Desert Palace).
        """,
        key_factors=[
            "Employee member of protected class and employer aware of protected status",
            "Adverse action (termination, demotion, denial of promotion, significant pay reduction, hostile transfer)",
            "Employee qualified for position (met legitimate job requirements)",
            "Comparator employees outside protected class treated more favorably for same conduct",
            "Temporal proximity between complaint of discrimination and adverse action (weeks, not months)",
            "Employer's explanation inconsistent, shifting, or pretextual"
        ],
        primary_authority=[
            "42 USC §2000e-2 - Title VII unlawful employment practices",
            "McDonnell Douglas Corp v Green, 411 US 792 (1973)",
            "Texas Dept of Community Affairs v Burdine, 450 US 248 (1981)",
            "Price Waterhouse v Hopkins, 490 US 228 (1989)",
            "Desert Palace v Costa, 539 US 90 (2003) - mixed motive"
        ],
        burden_holder="Plaintiff bears ultimate burden of proving intentional discrimination; burdens of production shift under McDonnell Douglas",
        adversary_position="Plaintiff argues similarly situated comparators treated better, temporal proximity, or shifting explanations prove pretext; employer argues legitimate business reason and no comparators",
        counter_arguments=[
            "No similarly situated comparator exists (different supervisor, different conduct, different performance history)",
            "Adverse action based on legitimate, nondiscriminatory reason (performance deficiencies documented before protected activity)",
            "Plaintiff not qualified (failed to meet objective job requirements or performed poorly)",
            "Decision-maker unaware of protected characteristic (race, religion, etc.)",
            "Temporal proximity too attenuated (months or years between events)",
            "Statistical evidence shows balanced workforce or no pattern of discrimination"
        ],
        resolution_strategy="Document legitimate, nondiscriminatory reasons contemporaneously. Apply policies consistently. Identify any comparators and document distinguishing factors. Avoid retaliatory timing (delay action or show decision predated complaint).",
        entity_scope="Employers with 15+ employees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when comparators clearly distinguishable and contemporaneous documentation; AGGRESSIVE when temporal proximity close; DISCLOSURE when mixed motive evidence; HIGH_RISK when shifting explanations or no documentation",
        controlling_precedent="Reeves v Sanderson Plumbing, 530 US 133 (2000) - pretext alone may support inference of discrimination; St. Mary's Honor Center v Hicks, 509 US 502 (1993) - plaintiff must prove discrimination, not just pretext"
    ),
    DoctrineBlock(
        topic="Title VII Disparate Impact",
        keywords=["disparate impact", "adverse impact", "business necessity", "four-fifths rule"],
        conclusion_template=[
            "Policy/practice has disparate impact on [protected class] shown by [statistical analysis].",
            "Employer establishes/fails to establish business necessity because [job-relatedness analysis].",
            "Less discriminatory alternative is/is not available."
        ],
        reasoning_framework="""
42 USC §2000e-2(k) - disparate impact occurs when facially neutral employment practice has disproportionate adverse effect on protected class and is not job-related and consistent with business necessity.
Plaintiff's burden: (1) identify specific employment practice, (2) show practice causes disparate impact through statistical evidence (four-fifths rule: selection rate for protected class < 80% of selection rate for highest-performing class).
Employer's burden: prove practice is job-related for position and consistent with business necessity. Business necessity requires showing practice bears significant relationship to successful job performance.
Plaintiff's rebuttal: show alternative practice with less discriminatory impact that serves employer's legitimate interest, and employer refused to adopt it.
Examples: educational requirements (Griggs - high school diploma not job-related for custodian), strength tests (women disproportionately fail), arrest/conviction records (disparate impact on minorities), height/weight requirements, written tests.
        """,
        key_factors=[
            "Statistical significance of disparity (four-fifths rule, standard deviation analysis)",
            "Sample size sufficient for reliable statistical inference",
            "Practice is specific and identifiable (not general subjective decision-making)",
            "Job-relatedness validated through professional standards (Uniform Guidelines on Employee Selection Procedures)",
            "Alternative practice available with less adverse impact and similar effectiveness",
            "Business necessity is compelling (safety-related or essential operational requirement)"
        ],
        primary_authority=[
            "42 USC §2000e-2(k) - disparate impact",
            "Griggs v Duke Power Co, 401 US 424 (1971)",
            "Wards Cove Packing v Atonio, 490 US 642 (1989)",
            "Uniform Guidelines on Employee Selection Procedures, 29 CFR §1607"
        ],
        burden_holder="Plaintiff bears initial burden of showing disparate impact; employer bears burden of proving business necessity; burden shifts back to plaintiff for less discriminatory alternative",
        adversary_position="Plaintiff argues employer's validation study flawed, alternative exists, or business necessity not compelling; employer argues no disparate impact or compelling necessity",
        counter_arguments=[
            "Statistical disparity not statistically significant (fails four-fifths rule or small sample size)",
            "Practice not specific enough (challenge to subjective decision-making process too broad)",
            "Practice validated through content validity, criterion validity, or construct validity study",
            "No less discriminatory alternative achieves same business goal with equal effectiveness",
            "Business necessity is safety-related (e.g., strength test for firefighters)",
            "Plaintiff failed to identify specific practice causing disparity"
        ],
        resolution_strategy="Conduct validation study showing job-relatedness (content, criterion, or construct validity per Uniform Guidelines). Search for alternative selection methods with less adverse impact. Document business necessity (safety, security, essential function).",
        entity_scope="Employers with 15+ employees",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="DEFENSIBLE when rigorous validation study and no alternative; AGGRESSIVE when validation marginal; DISCLOSURE when alternative exists but not adopted; HIGH_RISK when no validation and significant disparity",
        controlling_precedent="Ricci v DeStefano, 557 US 557 (2009) - employer cannot discard test results solely to avoid disparate impact without strong basis in evidence"
    ),
    DoctrineBlock(
        topic="ADEA Age Discrimination",
        keywords=["age discrimination", "ADEA", "40 years", "RFOA", "reasonable factor other than age"],
        conclusion_template=[
            "Employee establishes/fails prima facie case of age discrimination.",
            "Employer's reason is/is not reasonable factor other than age (RFOA).",
            "Evidence supports/refutes that age was but-for cause of adverse action."
        ],
        reasoning_framework="""
29 USC §623(a) prohibits discrimination against individuals 40+ years of age.
Prima facie case (similar to McDonnell Douglas): (1) member of protected class (40+), (2) qualified for position, (3) adverse action, (4) position filled by younger person or similarly situated younger employees treated better.
BUT-FOR causation: Gross v FBL Financial (557 US 167, 2009) - plaintiff must prove age was but-for cause of adverse action, not just a motivating factor (higher standard than Title VII mixed motive).
RFOA defense: 29 USC §623(f)(1) - not unlawful to take action based on reasonable factor other than age, even if correlated with age. Employer bears burden of proving RFOA.
RFOA analysis (EEOC regulations, 29 CFR §1625.7): (1) practice reasonably designed to achieve legitimate business purpose, (2) extent to which employer limited supervisory discretion, (3) extent to which employer assessed adverse impact on older workers, (4) degree of harm to older workers, (5) whether employer took steps to reduce harm.
Reduction in force: employer may lay off higher-paid employees (who tend to be older) if decision based on cost, not age proxy for cost.
Waivers: ADEA claims may be waived if knowing and voluntary under OWBPA (21-day consideration period, 7-day revocation, written advice to consult attorney, separate consideration for waiver).
        """,
        key_factors=[
            "Employee 40+ years old at time of adverse action",
            "Evidence age was determinative factor (but-for cause), not just a contributing factor",
            "Comparator: similarly situated younger employee treated more favorably",
            "Direct evidence of age animus (comments, stereotypes, statements about retirement)",
            "Employer's stated reason is reasonable factor other than age (performance, cost reduction, skill set)",
            "RFOA reasonable and employer assessed impact on older workers"
        ],
        primary_authority=[
            "29 USC §621-634 - ADEA",
            "Gross v FBL Financial Services, 557 US 167 (2009) - but-for causation",
            "Hazen Paper Co v Biggins, 507 US 604 (1993) - age vs tenure/pension status",
            "29 CFR §1625.7 - RFOA regulation"
        ],
        burden_holder="Plaintiff bears burden of proving age was but-for cause; employer bears burden of proving RFOA defense",
        adversary_position="Plaintiff argues age-based comments, reduction in force targeted older workers, or cost-cutting is age proxy; employer argues RFOA (performance, skills, reorganization)",
        counter_arguments=[
            "Decision based on compensation level, not age (although correlated)",
            "Younger employee had superior performance or different skill set needed for reorganized job",
            "Reduction in force based on objective criteria (seniority, performance ratings) applied neutrally",
            "Decision-maker unaware of employee's age or age not considered",
            "No direct evidence of age animus; circumstantial evidence insufficient for but-for causation",
            "Employee's claim based on mixed motive (age plus performance), but ADEA requires but-for causation"
        ],
        resolution_strategy="Avoid age-related comments or stereotypes. Document legitimate, nondiscriminatory reasons contemporaneously. If RIF, use objective criteria and document analysis. Ensure RFOA is reasonable and assess impact on older workers. For waivers, comply with OWBPA requirements.",
        entity_scope="Employers with 20+ employees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when RFOA well-documented and no direct age animus; AGGRESSIVE when cost-cutting correlates with age; DISCLOSURE when age-related comments exist; HIGH_RISK when RIF disproportionately impacts older workers without objective justification",
        controlling_precedent="Kentucky Retirement Systems v EEOC, 554 US 135 (2008) - pension status is not age proxy per se"
    ),
    DoctrineBlock(
        topic="WARN Act - Mass Layoff Notification",
        keywords=["WARN", "mass layoff", "plant closing", "60 days notice", "notification"],
        conclusion_template=[
            "Employer is/is not covered by WARN Act (100+ full-time employees).",
            "Layoff constitutes/does not constitute mass layoff or plant closing.",
            "Employer must provide [60 days notice/may claim exception]."
        ],
        reasoning_framework="""
29 USC §2101-2109 - WARN Act requires 60 days advance written notice to affected employees before mass layoff or plant closing.
Covered employer: 100+ full-time employees (or 100+ employees working 4000+ hours/week aggregate, excluding overtime).
Plant closing: permanent or temporary shutdown of single site or facility resulting in employment loss for 50+ employees during 30-day period.
Mass layoff: reduction in force at single site resulting in employment loss during 30-day period for either (1) 500+ employees, or (2) 50-499 employees if they constitute 33%+ of active workforce.
Employment loss: termination (other than discharge for cause, voluntary departure, retirement), layoff exceeding 6 months, or reduction in work hours by 50%+ for 6+ months.
90-day aggregation rule: employment losses within 90-day period aggregated to determine if threshold met, unless employer shows losses result from separate and distinct actions.
Exceptions: (1) faltering company (seeking capital/business, notice would harm ability to obtain), (2) unforeseeable business circumstances, (3) natural disaster.
Notice to: (1) affected employees or union, (2) state dislocated worker unit, (3) local chief elected official.
Penalties: back pay and benefits for up to 60 days for each affected employee.
        """,
        key_factors=[
            "Employer has 100+ full-time employees (or equivalent part-time)",
            "Single site of employment (not multiple locations aggregated)",
            "50+ employees lose employment within 30-day period (or 90-day aggregation)",
            "Employment loss meets statutory definition (not voluntary departures or for-cause terminations)",
            "Layoff is 500+ or 50-499 constituting 33%+ of active workforce",
            "Exception does not apply (faltering company, unforeseeable circumstances, natural disaster)"
        ],
        primary_authority=[
            "29 USC §2101-2109 - WARN Act",
            "20 CFR §639 - WARN regulations",
            "DOL WARN Advisor guidance"
        ],
        burden_holder="Employer bears burden of proving exception applicability; employees/government enforce notification requirement",
        adversary_position="Employees argue employer failed to provide 60-day notice or exception inapplicable; employer argues exception or thresholds not met",
        counter_arguments=[
            "Layoffs occurred at multiple sites, so single-site threshold not met",
            "Employment losses spread over 90+ days and result from separate, distinct actions (no aggregation)",
            "Employees terminated for cause or voluntarily departed (not employment loss)",
            "Employer has fewer than 100 full-time employees (or equivalent)",
            "Faltering company exception: employer actively seeking financing and notice would have precluded obtaining it",
            "Unforeseeable business circumstances: caused by sudden, unexpected action outside employer's control"
        ],
        resolution_strategy="Determine if covered employer and if layoff meets plant closing or mass layoff thresholds. Provide 60-day written notice to affected employees, union, state, and local officials. Document if exception applies (faltering company: evidence of financing efforts; unforeseeable: sudden contract loss, natural disaster). If notice not given, negotiate settlement for back pay/benefits.",
        entity_scope="Private employers with 100+ full-time employees; excludes part-time (under 20 hours/week or employed less than 6 months in prior year)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when 60-day notice provided or clear exception; AGGRESSIVE when aggregation rule applies; DISCLOSURE when faltering company claimed; HIGH_RISK when no notice and no exception",
        controlling_precedent="United Mine Workers v Decker Coal, 926 F Supp 191 (SD W Va 1996) - unforeseeable business circumstances exception"
    ),
    DoctrineBlock(
        topic="NLRA Section 7 Protected Concerted Activity",
        keywords=["NLRA", "concerted activity", "Section 7", "union", "collective bargaining"],
        conclusion_template=[
            "Employee engaged/did not engage in protected concerted activity under Section 7.",
            "Employer's adverse action constitutes/does not constitute unfair labor practice under Section 8.",
            "NLRB would likely find [violation/no violation]."
        ],
        reasoning_framework="""
29 USC §157 (Section 7) - employees have right to self-organization, form/join/assist labor organizations, bargain collectively, engage in other concerted activities for mutual aid or protection.
29 USC §158 (Section 8) - unfair labor practices include: (a)(1) interference/restraint/coercion of Section 7 rights, (a)(3) discrimination to encourage/discourage union membership, (a)(5) refusal to bargain with union representative.
Protected concerted activity: activity by 2+ employees OR individual employee acting on authority of other employees for mutual aid or protection regarding terms and conditions of employment. Examples: discussing wages/benefits, complaints about safety/working conditions, circulating petition, walkout, strike.
NOT protected: (1) activity not concerted (purely individual gripe), (2) not for mutual aid or protection (personal grievance), (3) disloyalty (disparagement of employer's product), (4) unlawful conduct (sabotage, violence), (5) unprotected by proviso (supervisors excluded from NLRA).
Social media posts: may be protected if discussing terms/conditions with other employees, seeking to induce group action, or bringing workplace issues to attention of other employees or union.
At-will employment does not override Section 7 rights; employer cannot discharge for protected concerted activity even absent union.
        """,
        key_factors=[
            "Activity involves 2+ employees or individual acting on behalf of group",
            "Activity relates to terms and conditions of employment (wages, hours, safety, benefits)",
            "Activity is for mutual aid or protection, not purely personal grievance",
            "Conduct does not lose protection (violence, sabotage, disloyalty, insubordination)",
            "Employer's adverse action motivated by protected activity",
            "Employee is not a supervisor (supervisors excluded from NLRA)"
        ],
        primary_authority=[
            "29 USC §157-158 - NLRA Sections 7-8",
            "NLRB v Washington Aluminum Co, 370 US 9 (1962) - walkout over cold workplace protected",
            "Eastex Inc v NLRB, 437 US 556 (1978) - mutual aid or protection extends beyond immediate workplace",
            "NLRB v Electrical Workers Local 1229 (Jefferson Standard), 346 US 464 (1953) - disloyalty exception"
        ],
        burden_holder="General Counsel (NLRB) bears burden of proving unfair labor practice (adverse action motivated by protected activity); employer may assert affirmative defense (legitimate business reason)",
        adversary_position="Union/employee argues protected concerted activity and pretext for discipline; employer argues activity not protected (individual gripe, disloyalty, misconduct) or legitimate business reason",
        counter_arguments=[
            "Activity was individual gripe, not concerted (no evidence employee acting with/on behalf of others)",
            "Complaint was personal grievance unrelated to terms/conditions affecting other employees",
            "Employee's conduct lost protection (violence, threats, sabotage, refusal to work, disloyalty)",
            "Employer unaware of protected activity when taking adverse action",
            "Adverse action based on legitimate business reason (performance, policy violation) unrelated to protected activity",
            "Employee is supervisor excluded from NLRA protection (authority to hire, fire, discipline, or responsibly direct)"
        ],
        resolution_strategy="Determine if activity is concerted (2+ employees or acting on behalf of group) and relates to terms/conditions. Assess if conduct lost protection (violence, disloyalty). Ensure adverse action not motivated by protected activity; document legitimate business reasons contemporaneously. Train supervisors on NLRA rights.",
        entity_scope="Private sector employers (NLRA excludes agricultural workers, independent contractors, supervisors, railroad/airline workers under RLA)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when activity clearly individual or unprotected conduct; AGGRESSIVE when borderline concerted activity; DISCLOSURE when social media posts; HIGH_RISK when discipline immediately follows group complaint",
        controlling_precedent="Meyers Industries, 268 NLRB 493 (1984) - concerted activity requires more than individual action"
    ),
    DoctrineBlock(
        topic="ERISA Fiduciary Duty - Retirement Plan Management",
        keywords=["ERISA", "fiduciary", "retirement plan", "401k", "prudent investor"],
        conclusion_template=[
            "Person is/is not ERISA fiduciary with respect to plan.",
            "Fiduciary breached/did not breach duty of prudence/loyalty.",
            "Remedies include [restoration of losses/removal of fiduciary/civil penalties]."
        ],
        reasoning_framework="""
29 USC §1002(21)(A) - fiduciary is person who (1) exercises discretionary authority/control over plan management or assets, (2) renders investment advice for fee, or (3) has discretionary authority/responsibility for plan administration.
29 USC §1104(a)(1) - fiduciary duties: (A) prudence - discharge duties with care, skill, prudence, diligence of prudent man in like capacity, (B) loyalty - act solely in interest of participants/beneficiaries for exclusive purpose of providing benefits and defraying reasonable expenses, (C) diversification - diversify plan investments to minimize risk of large losses unless clearly prudent not to do so, (D) plan documents - act in accordance with plan documents unless inconsistent with ERISA.
Prohibited transactions (29 USC §1106): self-dealing, transactions with party in interest, use of plan assets for fiduciary's benefit.
Investment selection: fiduciary must engage in procedurally prudent process (consider investment objectives, risk/return, role in portfolio, fees/expenses, diversification). Actual performance not determinative if process prudent.
Participant-directed accounts (404c safe harbor): if plan offers broad range of investment alternatives and participants exercise control, fiduciary not liable for participant's investment choices.
Revenue sharing/excessive fees: fiduciary must ensure fees reasonable for services provided; excessive recordkeeping or investment management fees can be breach.
        """,
        key_factors=[
            "Person has discretionary authority over plan assets or administration (named fiduciary, investment manager, plan administrator)",
            "Fiduciary engaged in prudent investigation before investment decision (RFP, due diligence, periodic review)",
            "Investment fees reasonable in relation to services provided (recordkeeping, investment management, advisory)",
            "Fiduciary acted solely in interest of participants, not employer or own interest",
            "Plan assets diversified across asset classes and investment options",
            "Prohibited transaction occurred (self-dealing, party in interest)"
        ],
        primary_authority=[
            "29 USC §1104 - ERISA fiduciary duties",
            "29 USC §1106 - prohibited transactions",
            "29 CFR §2550.404c-1 - ERISA 404(c) participant-directed safe harbor",
            "DOL Field Assistance Bulletin 2018-01 - selecting plan investments"
        ],
        burden_holder="Plaintiff bears burden of proving fiduciary status and breach; fiduciary bears burden of proving compliance with duties",
        adversary_position="Participants argue fiduciary breach (imprudent investment selection, excessive fees, self-dealing); fiduciary argues prudent process and reasonable fees",
        counter_arguments=[
            "Person is not fiduciary (no discretionary authority; ministerial functions only)",
            "Fiduciary engaged in prudent process (documented investigation, consideration of alternatives, periodic review)",
            "Fees are reasonable for services provided (comparison to industry benchmarks, competitive RFP)",
            "Investment losses due to market conditions, not imprudent process",
            "404(c) safe harbor applies: participants directed investments from broad range of alternatives",
            "Prohibited transaction exemption applies (statutory or DOL administrative exemption)"
        ],
        resolution_strategy="Document prudent process for investment selection (RFP, due diligence, benchmarking fees, periodic review). Ensure fees reasonable (compare to industry averages, negotiate). Avoid conflicts of interest and prohibited transactions. Provide participant education if 404(c) safe harbor sought. Obtain fiduciary liability insurance.",
        entity_scope="Employee benefit plans (pension, 401k, 403b) covered by ERISA (excludes governmental plans, church plans)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when prudent process documented and fees benchmarked; AGGRESSIVE when fees above industry average; DISCLOSURE when self-dealing alleged; HIGH_RISK when no documentation of prudent process",
        controlling_precedent="Tibble v Edison International, 575 US 523 (2015) - continuing duty to monitor investments; Fifth Third Bancorp v Dudenhoeffer, 573 US 409 (2014) - prudence standard for ESOP investments"
    ),
    DoctrineBlock(
        topic="Non-Compete Agreement - Reasonableness",
        keywords=["non-compete", "restrictive covenant", "restraint of trade", "blue pencil", "reasonable scope"],
        conclusion_template=[
            "Non-compete is enforceable/unenforceable because [reasonableness analysis].",
            "Geographic scope is [reasonable/overbroad]; temporal scope is [reasonable/excessive].",
            "Court may [enforce as written/blue pencil/refuse enforcement]."
        ],
        reasoning_framework="""
Common law: non-compete agreements are restraints of trade, disfavored but enforceable if: (1) supported by consideration, (2) protect legitimate business interest, (3) reasonable in scope (geography, duration, activity), (4) not unduly harsh on employee, (5) not contrary to public interest.
Legitimate business interests: trade secrets, confidential information, customer relationships, specialized training, goodwill (state-specific).
Reasonableness: (a) geographic scope limited to areas where employer does business or employee worked, (b) duration typically 1-2 years (longer if protecting trade secrets), (c) activity restricted narrowly tailored to competitive harm (e.g., prohibit working for competitor, not all employment).
Blue pencil doctrine: some jurisdictions allow court to modify overbroad covenant to make it reasonable (delete/narrow excessive restrictions); other jurisdictions refuse enforcement if overbroad.
FTC Rule (proposed 2023, finalized 2024): bans non-competes for workers except senior executives (>$151K, policy-making). Effective 120 days after publication. Expected legal challenges.
State law variations: California/North Dakota/Oklahoma - generally void; other states vary on enforceability standards, blue pencil availability, consideration requirements.
        """,
        key_factors=[
            "Adequate consideration (new employment, promotion, specialized training, continued employment in at-will state may be insufficient)",
            "Protects legitimate business interest (trade secrets, customer relationships, not general skills/experience)",
            "Geographic scope limited to employer's market area or employee's territory",
            "Duration limited (typically 1-2 years; longer if trade secrets)",
            "Scope of prohibited activity narrowly tailored (competitor in same industry, not all employment)",
            "Employee's level (executive/senior vs low-wage worker)"
        ],
        primary_authority=[
            "Restatement (Second) of Contracts §188 - Ancillary Restraints on Competition",
            "State-specific statutes (e.g., Cal Bus & Prof Code §16600, Fla Stat §542.335)",
            "FTC Rule on Non-Compete Clauses (16 CFR §910, effective 2024)",
            "Edwards v Arthur Andersen, 44 Cal4th 937 (2008) - California voids non-competes"
        ],
        burden_holder="Employer bears burden of proving non-compete reasonable and protects legitimate interest",
        adversary_position="Employee argues non-compete overbroad, lacks consideration, or protects no legitimate interest; employer argues reasonable and necessary to protect business",
        counter_arguments=[
            "No consideration: at-will employee, no promotion/raise/specialized training in exchange for covenant",
            "No legitimate interest: no trade secrets, no customer relationships unique to employer, employee's skills/experience are general",
            "Geographic scope overbroad: nationwide restriction when employer operates regionally",
            "Duration excessive: 5+ years unreasonable for most positions",
            "Activity restriction overbroad: prohibits all employment, not just competitive work",
            "Public interest: restriction on low-wage worker or essential profession (healthcare) contrary to policy"
        ],
        resolution_strategy="Draft narrow non-compete: limited geography (employer's actual market), short duration (1-2 years), specific activity (direct competitors). Provide consideration (signing bonus, specialized training). Use non-solicitation of customers/employees instead of full non-compete. Check state law (California/ND/OK ban enforcement). Post-FTC Rule, consider alternatives for non-executive employees.",
        entity_scope="Varies by state; FTC Rule applies to all workers except senior executives (>$151K, policy-making)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="DEFENSIBLE when narrow scope, legitimate interest, and state allows enforcement; AGGRESSIVE when state law uncertain or blue pencil needed; DISCLOSURE when low-wage worker; HIGH_RISK post-FTC Rule for non-executives",
        controlling_precedent="BDO Seidman v Hirshberg, 93 NY2d 382 (1999) - customer relationships; Marsh USA Inc v Cook, 354 SW3d 764 (Tex 2011) - consideration requirement"
    ),
    DoctrineBlock(
        topic="Trade Secrets - DTSA and State UTSA",
        keywords=["trade secrets", "DTSA", "UTSA", "misappropriation", "inevitable disclosure"],
        conclusion_template=[
            "Information qualifies/does not qualify as trade secret under DTSA/UTSA.",
            "Employee misappropriated/did not misappropriate trade secrets by [disclosure/use].",
            "Remedies include [injunction/damages/attorney fees]."
        ],
        reasoning_framework="""
18 USC §1836 (DTSA, 2016) - creates federal civil remedy for trade secret misappropriation. Applies to trade secrets related to product/service in interstate/foreign commerce.
UTSA (Uniform Trade Secrets Act, adopted by 47 states + DC) - state-law trade secret protection.
Trade secret: information (formula, pattern, compilation, program, device, method, technique, process) that (1) derives independent economic value from not being generally known or readily ascertainable, (2) subject to reasonable efforts to maintain secrecy.
Misappropriation: (1) acquisition by improper means (theft, breach of duty, espionage), or (2) disclosure/use by person who knew or should have known trade secret acquired by improper means or under duty of confidentiality.
Reasonable efforts to maintain secrecy: NDAs, restricted access, password protection, marking documents confidential, employee training. Need not be absolute secrecy, but must show effort.
Inevitable disclosure doctrine: some jurisdictions allow injunction against employee working for competitor if trade secrets disclosure inevitable due to new role; other jurisdictions reject doctrine absent evidence of actual or threatened misappropriation.
DTSA remedies: injunctive relief (up to 3 years; permanent if trade secret destroyed), damages (actual loss + unjust enrichment, or reasonable royalty), exemplary damages (up to 2x) if willful/malicious, attorney fees if bad faith.
DTSA immunity: whistleblowers immune from liability for disclosure to government or in court filing under seal.
        """,
        key_factors=[
            "Information not generally known or readily ascertainable by proper means",
            "Information has independent economic value from secrecy",
            "Employer took reasonable steps to maintain secrecy (NDAs, access controls, confidential markings)",
            "Employee acquired information by improper means or in confidence",
            "Employee disclosed or used information in new employment or business",
            "New role creates inevitable disclosure risk (similar responsibilities, direct competitor)"
        ],
        primary_authority=[
            "18 USC §1836 - DTSA",
            "Uniform Trade Secrets Act (adopted by 47 states + DC)",
            "Defend Trade Secrets Act of 2016, Pub L 114-153",
            "Restatement (Third) of Unfair Competition §39-45"
        ],
        burden_holder="Plaintiff bears burden of proving information is trade secret and misappropriation occurred",
        adversary_position="Plaintiff argues employee took confidential information and used/disclosed in new role; employee argues information not trade secret, no misappropriation, or independent development",
        counter_arguments=[
            "Information is generally known in industry or readily ascertainable from public sources",
            "Employer failed to take reasonable steps to maintain secrecy (no NDAs, no access restrictions, no confidential markings)",
            "Employee did not acquire information by improper means (learned through own experience, independent development)",
            "Employee has not disclosed or used information; inevitable disclosure doctrine rejected in jurisdiction",
            "Information is general skills/knowledge acquired in course of employment (not protectable as trade secret)",
            "Disclosure protected by DTSA whistleblower immunity (disclosure to government or in sealed court filing)"
        ],
        resolution_strategy="Identify protectable trade secrets (not general knowledge or publicly available). Implement security measures (NDAs, access controls, exit interviews, return of materials). Obtain evidence of misappropriation (forensic analysis, customer diversion, use of proprietary information). Seek preliminary injunction to prevent irreparable harm. Consider inevitable disclosure argument if jurisdiction permits.",
        entity_scope="DTSA: federal jurisdiction if trade secret related to product/service in interstate/foreign commerce; UTSA: state law varies by state",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when clear trade secret, security measures, and evidence of use/disclosure; AGGRESSIVE when inevitable disclosure theory; DISCLOSURE when information borderline general knowledge; HIGH_RISK when no security measures or publicly available information",
        controlling_precedent="PepsiCo Inc v Redmond, 54 F3d 1262 (7th Cir 1995) - inevitable disclosure; Bimbo Bakeries USA v Botticella, 613 F3d 102 (3d Cir 2010) - rejecting inevitable disclosure"
    ),
    DoctrineBlock(
        topic="Independent Contractor vs Employee - ABC Test and Economic Reality",
        keywords=["independent contractor", "employee", "ABC test", "economic reality", "misclassification"],
        conclusion_template=[
            "Worker is employee/independent contractor under [ABC test/economic reality test].",
            "Misclassification exposes employer to [wage/hour claims/payroll tax/benefits liability].",
            "Recommend [reclassify/restructure relationship/defend as IC]."
        ],
        reasoning_framework="""
FLSA/common law economic reality test (multi-factor): (1) degree of control by employer, (2) worker's opportunity for profit/loss, (3) worker's investment in facilities/equipment, (4) permanence of relationship, (5) skill/initiative required, (6) integration into employer's business. No single factor determinative; totality of circumstances.
ABC test (California Dynamex, PRO Act proposed federally, some state wage/hour laws): Worker is employee unless employer proves ALL three: (A) free from control/direction in performance of work, (B) work is outside usual course of employer's business, (C) worker customarily engaged in independently established trade/occupation/business of same nature.
Prong B (outside usual course of business) is strict: Uber driver performs work within Uber's usual business (transportation), so employee under ABC test (CA AB5).
IRS 20-factor test (for tax purposes): similar to economic reality test; includes behavioral control, financial control, relationship type.
Consequences of misclassification: FLSA wage/hour violations (unpaid overtime, minimum wage), FICA/FUTA payroll tax liability, unemployment insurance, workers' comp, employee benefits (ERISA), joint employer liability, liquidated damages/penalties.
DOL 2024 Rule (final Jan 2024): rescinds 2021 independent contractor rule; returns to multi-factor economic reality test with no single or primary factor.
        """,
        key_factors=[
            "Employer controls when/where/how work performed (training, supervision, evaluation)",
            "Worker has no opportunity for profit/loss based on managerial skill",
            "Worker does not invest in equipment/facilities (employer provides tools)",
            "Relationship is ongoing/indefinite, not project-based",
            "Work requires no specialized skill or worker uses employer-provided training",
            "Work is integral to employer's business (not ancillary service)"
        ],
        primary_authority=[
            "FLSA, 29 USC §203(e)(1), §203(g) - employee definition",
            "Dynamex Operations West Inc v Superior Court, 4 Cal5th 903 (2018) - ABC test",
            "DOL Final Rule on Employee or Independent Contractor Classification, 89 FR 1638 (2024)",
            "IRS Rev Rul 87-41 (20-factor test)"
        ],
        burden_holder="Under ABC test, employer bears burden of proving all 3 prongs; under economic reality test, analysis is totality of circumstances",
        adversary_position="Worker argues employee status to claim wage/hour protections, unemployment, workers' comp; employer argues IC status to avoid liability",
        counter_arguments=[
            "Worker has freedom to set own hours, work for multiple clients, and control how work performed",
            "Worker has opportunity for profit/loss (e.g., can hire assistants, invest in efficiency)",
            "Worker provides own tools, equipment, facilities (significant capital investment)",
            "Relationship is project-based or short-term, not ongoing employment relationship",
            "Worker has specialized skills/licenses and markets services independently",
            "Work is outside employer's usual business (ancillary service, e.g., janitorial for tech company)"
        ],
        resolution_strategy="Apply ABC test if jurisdiction uses it (CA, MA, NJ for wage/hour); otherwise apply economic reality test. Assess control, profit/loss opportunity, investment, permanence, skill, integration. If employee, reclassify and provide wage/hour protections, withhold taxes, provide benefits. If defending IC, document lack of control, worker's independent business, and project-based nature.",
        entity_scope="FLSA: employers engaged in interstate commerce or $500K+ annual revenue; state law: varies by state (ABC test in CA/MA/NJ for wage/hour)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="DEFENSIBLE when worker has independent business and no employer control; AGGRESSIVE when factors mixed; DISCLOSURE under ABC test prong B (work within usual business); HIGH_RISK when employer exercises control and worker integrated into business",
        controlling_precedent="Saleem v Corporate Transportation Group, 854 F3d 131 (2d Cir 2017) - economic reality test; Vazquez v Jan-Pro Franchising Intl, 10 Cal5th 944 (2021) - ABC test"
    ),
    DoctrineBlock(
        topic="At-Will Employment - Exceptions to Terminability",
        keywords=["at-will", "wrongful termination", "public policy", "implied contract", "covenant of good faith"],
        conclusion_template=[
            "Employment is at-will, but exception applies: [public policy/implied contract/good faith].",
            "Termination violates [state statute/public policy/contractual promise].",
            "Employee may recover [lost wages/emotional distress/punitive damages]."
        ],
        reasoning_framework="""
Default rule: at-will employment means employer or employee may terminate relationship at any time for any reason or no reason (absent contract or statute to contrary).
Exceptions: (1) public policy, (2) implied contract, (3) covenant of good faith and fair dealing (minority of states).
Public policy exception: wrongful termination if fired for (a) refusing to violate law (e.g., commit perjury, file false reports), (b) performing statutory duty (e.g., jury duty, military service), (c) exercising statutory right (e.g., filing workers' comp claim, whistleblowing), (d) reporting employer's illegal conduct (whistleblower). Policy must be clearly established in constitution/statute/regulation/judicial decision.
Implied contract exception: handbook, policies, oral representations, course of dealing may create implied promise of job security (e.g., termination only for cause, progressive discipline). Disclaimer language in handbook can preserve at-will status.
Covenant of good faith and fair dealing: minority of states (CA, MA) imply covenant prohibiting termination in bad faith or motivated by malice (e.g., to avoid paying commissions, to retaliate). Some states apply only to limit bad-faith motives, not impose just-cause requirement.
Montana Wrongful Discharge from Employment Act: only state to abolish at-will by statute; requires just cause after probationary period.
        """,
        key_factors=[
            "State recognizes exception (not all states recognize all exceptions)",
            "Public policy clearly established in statute/constitution/regulation (not vague social norms)",
            "Handbook or policy creates implied promise (for-cause termination, progressive discipline, specific procedures)",
            "Employer made oral representations of job security or long-term employment",
            "Termination motivated by bad faith (avoiding commission, bonus, or vested benefits)",
            "Disclaimer language in handbook (at-will status, no contract, employment terminable at any time)"
        ],
        primary_authority=[
            "Restatement (Third) of Employment Law §5.01-5.02 - public policy exception",
            "Foley v Interactive Data Corp, 47 Cal3d 654 (1988) - implied covenant",
            "Toussaint v Blue Cross, 408 Mich 579 (1980) - implied contract",
            "Mont Code Ann §39-2-901 et seq - Wrongful Discharge Act"
        ],
        burden_holder="Employee bears burden of proving exception applies and termination violates public policy/contract/good faith",
        adversary_position="Employee argues termination violated public policy, implied contract, or covenant of good faith; employer argues at-will status and legitimate reason",
        counter_arguments=[
            "Handbook contains clear at-will disclaimer negating implied contract",
            "No public policy violation: employee not fired for protected reason (jury duty, whistleblowing, etc.)",
            "State does not recognize implied covenant of good faith exception (majority rule)",
            "Employer had legitimate, nondiscriminatory reason for termination (performance, misconduct)",
            "Public policy not clearly established (vague ethical norm, not statute/regulation)",
            "No implied contract: handbook/policy explicitly states at-will employment and procedures are not contractual"
        ],
        resolution_strategy="Include at-will disclaimer in offer letter and handbook. Apply policies consistently. Document legitimate reasons for termination contemporaneously. Avoid terminating for public policy reasons (whistleblowing, workers' comp, jury duty). If implied contract claim, show disclaimer language and lack of contractual intent.",
        entity_scope="State law governs; exceptions vary by state (public policy widely recognized, implied contract/good faith minority of states)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when at-will disclaimer and legitimate reason; AGGRESSIVE when handbook creates implied promise; DISCLOSURE when termination close to protected activity; HIGH_RISK when public policy violation (whistleblower retaliation)",
        controlling_precedent="Petermann v International Brotherhood of Teamsters, 174 CalApp2d 184 (1959) - first public policy exception; Fortune v National Cash Register, 373 Mass 96 (1977) - covenant of good faith"
    ),
    DoctrineBlock(
        topic="Employee Handbook - Contractual Effect and Disclaimers",
        keywords=["handbook", "policy", "implied contract", "disclaimer", "at-will"],
        conclusion_template=[
            "Handbook creates/does not create implied contract because [disclaimer/promissory language analysis].",
            "Policy is/is not binding on employer.",
            "Employer must [follow policy/may deviate if at-will preserved]."
        ],
        reasoning_framework="""
General rule: employee handbook may create implied contract if contains promissory language (for-cause termination, progressive discipline, specific procedures) and employer does not include effective disclaimer.
Implied contract factors: (1) specificity of policy terms, (2) promissory language (shall, will vs may, generally), (3) course of dealing (employer followed policies consistently), (4) employee reliance, (5) disclaimer language.
Effective disclaimer: conspicuous statement that (a) employment is at-will, (b) handbook is not contract, (c) policies may be changed at any time, (d) employer retains right to terminate with or without cause. Must be clear, prominent, and unambiguous.
Location of disclaimer: front of handbook, signed acknowledgment, offer letter. Buried disclaimer may be ineffective.
Modification of handbook: employer may change policies, but if handbook is implied contract, modification requires consideration (continued employment may be sufficient in some states, insufficient in others).
Promissory estoppel: even if no contract, employee may argue detrimental reliance on policy (e.g., refused other job based on job security representation).
        """,
        key_factors=[
            "Disclaimer language clear and conspicuous (front of handbook, signed acknowledgment)",
            "Handbook uses permissive language (may, generally) vs mandatory (shall, will)",
            "Policy creates specific procedural protections (progressive discipline, just-cause termination)",
            "Employer consistently followed policies (course of dealing)",
            "Employee relied on policy to detriment (rejected other employment, relocated)",
            "Disclaimer signed by employee acknowledging at-will status and no contractual rights"
        ],
        primary_authority=[
            "Woolley v Hoffmann-La Roche, 99 NJ 284 (1985) - handbook as implied contract",
            "Duldulao v Saint Mary of Nazareth Hospital, 115 Ill2d 482 (1987) - disclaimer effectiveness",
            "Restatement (Third) of Employment Law §2.03-2.05 - handbooks and policies"
        ],
        burden_holder="Employee bears burden of proving handbook created implied contract; employer may assert disclaimer as affirmative defense",
        adversary_position="Employee argues handbook created implied contract (promissory language, consistent enforcement); employer argues disclaimer preserved at-will status",
        counter_arguments=[
            "Conspicuous at-will disclaimer negates implied contract (signed acknowledgment, front of handbook)",
            "Handbook uses permissive language (may, generally) not mandatory (shall, will)",
            "Employer did not consistently follow policies (deviation shows no contractual intent)",
            "State law requires clear mutual intent to contract (handbook alone insufficient without meeting of minds)",
            "Policy contains reservation of rights clause (employer retains discretion to deviate)",
            "No detrimental reliance: employee cannot show changed position based on policy"
        ],
        resolution_strategy="Draft handbook with clear at-will disclaimer (front page, signed acknowledgment). Use permissive language (may, generally) not mandatory (shall, will). Include reservation of rights (employer retains discretion to deviate from policies). Require signed acknowledgment of at-will status and no contractual rights. Review state law on disclaimer effectiveness.",
        entity_scope="State law governs; enforceability of disclaimers varies by state (some require clear mutual intent to contract, others enforce conspicuous disclaimers)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when clear disclaimer signed by employee; AGGRESSIVE when promissory language used; DISCLOSURE when employer deviated from stated policy; HIGH_RISK when no disclaimer and for-cause language",
        controlling_precedent="Nicosia v Wakefern Food Corp, 136 NJ 401 (1994) - disclaimer effectiveness; Guz v Bechtel National Inc, 24 Cal4th 317 (2000) - personnel policies generally not contracts"
    )
]

class QueryRequest(BaseModel):
    query: str = Field(..., description="Employment law query")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")

class QueryResponse(BaseModel):
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    latency_ms: float
    cache_hit: bool
    triggered_doctrines: List[str]
    determinism_hash: str
    timestamp: str

APP = FastAPI(title=ENGINE_NAME, version=VERSION)
APP.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

METRICS = {"queries": 0, "cache_hits": 0, "cache_misses": 0, "errors": 0, "total_latency_ms": 0}

def compute_determinism_hash(query: str, mode: str, zone: str, answer: str) -> str:
    payload = f"{query}|{mode}|{zone}|{answer}"
    return hashlib.sha256(payload.encode()).hexdigest()[:16]

def search_doctrine_cache(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    matches = []
    for block in DOCTRINE_CACHE:
        if any(kw in query_lower for kw in block.keywords):
            matches.append(block)
    return matches

def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> tuple[str, bool, List[str], ConfidenceLevel]:
    start = datetime.now()
    doctrines = search_doctrine_cache(query)
    if doctrines:
        primary = doctrines[0]
        if mode == ResponseMode.FAST:
            answer = f"{primary.conclusion_template[0]} {primary.conclusion_template[1]}"
        elif mode == ResponseMode.DEFENSE:
            answer = f"DOCTRINE: {primary.topic}\n\n"
            answer += f"CONCLUSION: {' '.join(primary.conclusion_template)}\n\n"
            answer += f"KEY FACTORS: {'; '.join(primary.key_factors[:3])}\n\n"
            answer += f"AUTHORITY: {primary.primary_authority[0]}"
        else:
            answer = f"MEMORANDUM RE: {primary.topic}\n\n"
            answer += f"CONCLUSION:\n{' '.join(primary.conclusion_template)}\n\n"
            answer += f"REASONING:\n{primary.reasoning_framework}\n\n"
            answer += f"KEY FACTORS:\n" + "\n".join(f"- {f}" for f in primary.key_factors) + "\n\n"
            answer += f"AUTHORITY:\n" + "\n".join(f"- {a}" for a in primary.primary_authority) + "\n\n"
            answer += f"ADVERSARY POSITION: {primary.adversary_position}\n\n"
            answer += f"COUNTER-ARGUMENTS:\n" + "\n".join(f"- {c}" for c in primary.counter_arguments[:3])

        return answer, True, [d.topic for d in doctrines], primary.confidence

    fallback = "Employment law query received. For specific guidance, provide details on: applicable statute (FLSA/FMLA/ADA/Title VII/ADEA/WARN/NLRA/ERISA), jurisdiction, fact pattern."
    return fallback, False, [], ConfidenceLevel.DISCLOSURE

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    start = datetime.now()
    try:
        answer, cache_hit, doctrines, confidence = three_layer_response(req.query, req.mode, req.zone)
        latency = (datetime.now() - start).total_seconds() * 1000

        METRICS["queries"] += 1
        if cache_hit:
            METRICS["cache_hits"] += 1
        else:
            METRICS["cache_misses"] += 1
        METRICS["total_latency_ms"] += latency

        det_hash = compute_determinism_hash(req.query, req.mode.value, req.zone.value, answer)

        logger.info(f"Query processed | mode={req.mode.value} zone={req.zone.value} cache_hit={cache_hit} latency={latency:.1f}ms")

        return QueryResponse(
            answer=answer,
            mode=req.mode,
            zone=req.zone,
            confidence=confidence,
            latency_ms=round(latency, 2),
            cache_hit=cache_hit,
            triggered_doctrines=doctrines,
            determinism_hash=det_hash,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        METRICS["errors"] += 1
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health")
async def health():
    avg_latency = METRICS["total_latency_ms"] / METRICS["queries"] if METRICS["queries"] > 0 else 0
    cache_rate = METRICS["cache_hits"] / METRICS["queries"] if METRICS["queries"] > 0 else 0

    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "status": "operational",
        "port": PORT,
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "metrics": {
            "total_queries": METRICS["queries"],
            "cache_hits": METRICS["cache_hits"],
            "cache_misses": METRICS["cache_misses"],
            "cache_hit_rate": round(cache_rate, 3),
            "errors": METRICS["errors"],
            "avg_latency_ms": round(avg_latency, 2)
        },
        "components": {
            "three_layer_response": "active",
            "doctrine_cache": "active",
            "response_modes": ["FAST", "DEFENSE", "MEMO"],
            "analysis_zones": ["PLANNING", "REPORTING", "AUDIT"],
            "determinism_hash": "SHA-256",
            "telemetry": "active"
        }
    }

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    uvicorn.run(APP, host="0.0.0.0", port=PORT)
