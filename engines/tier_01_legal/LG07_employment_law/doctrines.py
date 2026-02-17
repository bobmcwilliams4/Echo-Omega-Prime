"""
LG07 Employment Law Engine - Doctrines Module
================================================
Pre-compiled employment law doctrine cache with structured legal knowledge
covering all major federal employment statutes, state law, and common
employment dispute categories.

Each doctrine block contains:
    - topic: Canonical topic identifier
    - title: Human-readable title
    - category: Employment law category
    - summary: Concise legal summary
    - key_statutes: Governing statutes/regulations
    - elements: Legal elements for the claim/defense
    - defenses: Available defenses
    - remedies: Available remedies
    - leading_cases: Key case law citations
    - confidence: Base confidence score (0.0-1.0)
    - last_updated: Date of last content review
    - tags: Searchable tags

Version: 1.0.0
Engine: LG07 Employment Law
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# DOCTRINE RESPONSE
# ============================================================================

@dataclass
class DoctrineResponse:
    """A structured response from the doctrine cache."""
    topic: str
    title: str
    category: str
    content: str
    authority: str
    confidence: float
    confidence_band: str
    citations: List[str]
    tags: List[str]
    last_updated: str
    determinism_hash: str
    layer: str = "doctrine_cache"
    response_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "authority": self.authority,
            "confidence": round(self.confidence, 4),
            "confidence_band": self.confidence_band,
            "citations": self.citations,
            "tags": self.tags,
            "last_updated": self.last_updated,
            "determinism_hash": self.determinism_hash,
            "layer": self.layer,
            "response_time_ms": round(self.response_time_ms, 3),
        }


# ============================================================================
# DOCTRINE CACHE - TITLE VII DISCRIMINATION
# ============================================================================

DOCTRINE_CACHE: Dict[str, Dict[str, Any]] = {

    "title_vii_overview": {
        "topic": "title_vii_overview",
        "title": "Title VII of the Civil Rights Act of 1964 - Overview",
        "category": "title_vii",
        "summary": "Title VII prohibits employment discrimination based on race, color, religion, sex, and national origin. Applies to employers with 15 or more employees, employment agencies, labor organizations, and the federal government. Enforced by the Equal Employment Opportunity Commission (EEOC). Covers hiring, firing, compensation, terms, conditions, and privileges of employment. The Pregnancy Discrimination Act (1978) and Bostock v. Clayton County (2020) expanded sex discrimination to include pregnancy, sexual orientation, and gender identity.",
        "key_statutes": ["42 U.S.C. 2000e et seq.", "42 U.S.C. 2000e-2 (unlawful practices)", "42 U.S.C. 2000e-3 (retaliation)", "29 C.F.R. Part 1604 (sex discrimination guidelines)"],
        "elements": ["Membership in a protected class", "Qualified for the position", "Adverse employment action", "Circumstances giving rise to inference of discrimination"],
        "defenses": ["Bona fide occupational qualification (BFOQ)", "Business necessity", "Legitimate nondiscriminatory reason", "Same-decision defense (mixed motive)", "After-acquired evidence", "Statute of limitations (180/300 days)"],
        "remedies": ["Back pay", "Front pay", "Compensatory damages (capped by employer size)", "Punitive damages (capped)", "Injunctive relief", "Attorneys fees", "Reinstatement"],
        "leading_cases": ["Griggs v. Duke Power Co., 401 U.S. 424 (1971)", "McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)", "Texas Dept. of Community Affairs v. Burdine, 450 U.S. 248 (1981)", "Price Waterhouse v. Hopkins, 490 U.S. 228 (1989)", "Bostock v. Clayton County, 590 U.S. ___ (2020)"],
        "confidence": 0.95,
        "last_updated": "2026-01-15",
        "tags": ["title_vii", "discrimination", "protected_class", "eeoc", "civil_rights"],
    },

    "disparate_treatment": {
        "topic": "disparate_treatment",
        "title": "Disparate Treatment - Intentional Discrimination",
        "category": "title_vii",
        "summary": "Disparate treatment occurs when an employer intentionally discriminates against an individual because of a protected characteristic. The McDonnell Douglas burden-shifting framework governs individual disparate treatment cases: (1) plaintiff establishes prima facie case, (2) employer articulates legitimate nondiscriminatory reason, (3) plaintiff shows pretext. In mixed-motive cases under Price Waterhouse/Desert Palace, plaintiff must show protected characteristic was a motivating factor. Direct evidence of discriminatory intent shifts burden to employer to show same decision regardless.",
        "key_statutes": ["42 U.S.C. 2000e-2(a)", "42 U.S.C. 2000e-2(m) (motivating factor)", "42 U.S.C. 2000e-5(g)(2)(B) (mixed-motive remedy limitation)"],
        "elements": ["Protected class membership", "Qualification for the position", "Adverse employment action", "Similarly situated comparator treated more favorably OR other inference of discriminatory intent"],
        "defenses": ["Legitimate nondiscriminatory reason (not pretext)", "BFOQ (narrow)", "Same-decision defense (limits remedies in mixed-motive)", "After-acquired evidence (limits remedies)"],
        "remedies": ["Full compensatory and punitive damages if sole factor", "Limited to declaratory/injunctive relief and attorneys fees if mixed-motive same-decision proven"],
        "leading_cases": ["McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)", "Desert Palace, Inc. v. Costa, 539 U.S. 90 (2003)", "Reeves v. Sanderson Plumbing Products, 530 U.S. 133 (2000)"],
        "confidence": 0.93,
        "last_updated": "2026-01-15",
        "tags": ["disparate_treatment", "intentional_discrimination", "mcdonnell_douglas", "burden_shifting"],
    },

    "disparate_impact": {
        "topic": "disparate_impact",
        "title": "Disparate Impact - Unintentional Discrimination",
        "category": "title_vii",
        "summary": "Disparate impact claims challenge facially neutral employment practices that disproportionately affect a protected group. No intent to discriminate is required. The plaintiff must identify a specific practice causing statistical disparity (four-fifths rule as guideline). The employer may defend with business necessity and job-relatedness. Even if business necessity is shown, the plaintiff may prevail by demonstrating a less discriminatory alternative. Ricci v. DeStefano (2009) held that employer cannot discard test results based on racial outcomes unless strong basis in evidence that disparate impact liability would follow.",
        "key_statutes": ["42 U.S.C. 2000e-2(k) (burden of proof)", "29 C.F.R. 1607 (Uniform Guidelines on Employee Selection)"],
        "elements": ["Facially neutral employment practice", "Statistical disparity against protected group (four-fifths rule guideline)", "Identification of specific practice causing disparity"],
        "defenses": ["Business necessity and job-relatedness", "Practice is required by law", "Bona fide seniority system (Section 703(h))"],
        "remedies": ["Back pay", "Injunctive relief (modify or eliminate practice)", "Attorneys fees", "NOTE: Punitive damages NOT available for disparate impact"],
        "leading_cases": ["Griggs v. Duke Power Co., 401 U.S. 424 (1971)", "Wards Cove Packing Co. v. Atonio, 490 U.S. 642 (1989)", "Ricci v. DeStefano, 557 U.S. 557 (2009)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["disparate_impact", "four_fifths_rule", "business_necessity", "statistical_analysis"],
    },

    "sexual_harassment": {
        "topic": "sexual_harassment",
        "title": "Sexual Harassment Under Title VII",
        "category": "title_vii",
        "summary": "Sexual harassment is a form of sex discrimination under Title VII. Two recognized forms: (1) Quid pro quo - submission to or rejection of unwelcome sexual conduct used as basis for employment decisions; (2) Hostile work environment - unwelcome sexual conduct sufficiently severe or pervasive to alter conditions of employment. Under Ellerth/Faragher, employer is vicariously liable for supervisor harassment resulting in tangible employment action. For non-tangible cases, employer has affirmative defense if it exercised reasonable care to prevent/correct and plaintiff unreasonably failed to use preventive opportunities.",
        "key_statutes": ["42 U.S.C. 2000e-2(a)(1)", "29 C.F.R. 1604.11 (EEOC Guidelines)"],
        "elements": ["Unwelcome conduct", "Based on sex", "Severe or pervasive (hostile environment) OR tangible employment action (quid pro quo)", "Imputed to employer"],
        "defenses": ["Ellerth/Faragher affirmative defense (no tangible action)", "Conduct not severe or pervasive", "Conduct was welcomed", "Prompt remedial action taken"],
        "remedies": ["Compensatory damages", "Punitive damages", "Back pay", "Injunctive relief", "Attorneys fees"],
        "leading_cases": ["Meritor Savings Bank v. Vinson, 477 U.S. 57 (1986)", "Burlington Industries v. Ellerth, 524 U.S. 742 (1998)", "Faragher v. City of Boca Raton, 524 U.S. 775 (1998)", "Harris v. Forklift Systems, 510 U.S. 17 (1993)", "Oncale v. Sundowner Offshore Services, 523 U.S. 75 (1998)"],
        "confidence": 0.94,
        "last_updated": "2026-01-15",
        "tags": ["sexual_harassment", "hostile_work_environment", "quid_pro_quo", "ellerth_faragher"],
    },

    "retaliation_title_vii": {
        "topic": "retaliation_title_vii",
        "title": "Title VII Retaliation",
        "category": "title_vii",
        "summary": "Section 704(a) prohibits retaliation against employees who oppose unlawful practices (opposition clause) or participate in Title VII proceedings (participation clause). Burlington Northern v. White (2006) established that actionable retaliation includes any materially adverse action that would dissuade a reasonable worker from making or supporting a charge. Causation standard is but-for under University of Texas Southwestern Medical Center v. Nassar (2013). Protected activity includes filing EEOC charges, testifying, complaining internally about discrimination, and refusing to obey discriminatory orders.",
        "key_statutes": ["42 U.S.C. 2000e-3(a)"],
        "elements": ["Protected activity (opposition or participation)", "Materially adverse action", "Causal connection (but-for causation under Nassar)"],
        "defenses": ["No protected activity occurred", "No materially adverse action", "No causal connection", "Legitimate non-retaliatory reason"],
        "remedies": ["Full compensatory and punitive damages", "Back pay", "Reinstatement", "Injunctive relief", "Attorneys fees"],
        "leading_cases": ["Burlington Northern & Santa Fe Ry. v. White, 548 U.S. 53 (2006)", "University of Texas Southwestern Medical Center v. Nassar, 570 U.S. 338 (2013)", "Crawford v. Metropolitan Government of Nashville, 555 U.S. 271 (2009)"],
        "confidence": 0.93,
        "last_updated": "2026-01-15",
        "tags": ["retaliation", "protected_activity", "opposition_clause", "participation_clause", "nassar"],
    },

    # ============================================================================
    # ADA / DISABILITY DISCRIMINATION
    # ============================================================================

    "ada_overview": {
        "topic": "ada_overview",
        "title": "Americans with Disabilities Act - Employment (Title I)",
        "category": "ada",
        "summary": "The ADA prohibits disability discrimination against qualified individuals with disabilities in all employment practices. A qualified individual can perform essential functions with or without reasonable accommodation. The ADAAA (2008) broadened the definition of disability: (1) physical or mental impairment substantially limiting major life activities, (2) record of such impairment, or (3) regarded as having such impairment. Major life activities include caring for oneself, performing manual tasks, seeing, hearing, eating, sleeping, walking, standing, lifting, bending, speaking, breathing, learning, reading, concentrating, thinking, communicating, and working. Major bodily functions also qualify.",
        "key_statutes": ["42 U.S.C. 12101-12117", "42 U.S.C. 12112 (discrimination prohibition)", "29 C.F.R. Part 1630 (EEOC regulations)", "ADA Amendments Act of 2008 (ADAAA)"],
        "elements": ["Disability (actual, record, or regarded as)", "Qualified individual (can perform essential functions)", "Adverse employment action", "Because of disability"],
        "defenses": ["Not a qualified individual", "Direct threat defense", "Undue hardship (for accommodation claims)", "Job-related and consistent with business necessity (qualification standards)", "Not disabled under ADA definition"],
        "remedies": ["Same as Title VII: compensatory damages (capped), punitive damages (capped), back pay, front pay, reinstatement, injunctive relief, attorneys fees"],
        "leading_cases": ["Toyota Motor Mfg. v. Williams, 534 U.S. 184 (2002) (superseded by ADAAA)", "US Airways v. Barnett, 535 U.S. 391 (2002)", "Sutton v. United Air Lines, 527 U.S. 471 (1999) (superseded by ADAAA)", "Cleveland v. Policy Management Systems, 526 U.S. 795 (1999)"],
        "confidence": 0.94,
        "last_updated": "2026-01-15",
        "tags": ["ada", "disability", "reasonable_accommodation", "qualified_individual", "adaaa"],
    },

    "reasonable_accommodation_ada": {
        "topic": "reasonable_accommodation_ada",
        "title": "Reasonable Accommodation Under the ADA",
        "category": "ada",
        "summary": "Employers must provide reasonable accommodations to qualified individuals with disabilities unless doing so would cause undue hardship. The interactive process requires good-faith dialogue between employer and employee to identify effective accommodations. Examples: modified work schedules, reassignment to vacant position, job restructuring, modified equipment, readers/interpreters, telework, leave of absence. The employer need not provide the specific accommodation requested, but must provide an effective one. Failure to engage in the interactive process can itself constitute discrimination.",
        "key_statutes": ["42 U.S.C. 12111(9)", "42 U.S.C. 12112(b)(5)(A)", "29 C.F.R. 1630.2(o)", "29 C.F.R. 1630.9"],
        "elements": ["Known disability", "Request for accommodation (or employer awareness of need)", "Employer failure to provide reasonable accommodation", "No undue hardship"],
        "defenses": ["Undue hardship (significant difficulty or expense)", "Direct threat to safety", "Employee failed to engage in interactive process", "No effective accommodation exists", "Accommodation would eliminate essential function"],
        "remedies": ["Compensatory damages", "Back pay", "Injunctive relief (provide accommodation)", "Attorneys fees"],
        "leading_cases": ["US Airways v. Barnett, 535 U.S. 391 (2002)", "Humphrey v. Memorial Hospitals Assn., 239 F.3d 1128 (9th Cir. 2001)", "EEOC v. Sears, Roebuck & Co., 417 F.3d 789 (7th Cir. 2005)"],
        "confidence": 0.93,
        "last_updated": "2026-01-15",
        "tags": ["reasonable_accommodation", "interactive_process", "undue_hardship", "ada"],
    },

    # ============================================================================
    # ADEA / AGE DISCRIMINATION
    # ============================================================================

    "adea_overview": {
        "topic": "adea_overview",
        "title": "Age Discrimination in Employment Act (ADEA)",
        "category": "adea",
        "summary": "The ADEA protects individuals age 40 and over from employment discrimination based on age. Applies to employers with 20+ employees. Unlike Title VII, the ADEA requires but-for causation under Gross v. FBL Financial Services (2009) - no mixed-motive framework. The Older Workers Benefit Protection Act (OWBPA) governs age-related benefit differentials and sets strict requirements for valid waivers of ADEA claims (21-day consideration period for individuals, 45 days for group, 7-day revocation period). State ADEA analogs may apply to smaller employers.",
        "key_statutes": ["29 U.S.C. 621-634", "29 U.S.C. 623 (prohibitions)", "29 U.S.C. 626 (enforcement)", "Older Workers Benefit Protection Act (OWBPA)", "29 C.F.R. Part 1625"],
        "elements": ["Age 40 or older", "Qualified for position", "Adverse employment action", "But-for causation (age was the determinative factor)", "Replaced by substantially younger person or other age-related evidence"],
        "defenses": ["Reasonable factors other than age (RFOA)", "Bona fide occupational qualification (BFOQ)", "Bona fide seniority system", "Bona fide employee benefit plan (OWBPA)", "Good cause"],
        "remedies": ["Back pay", "Liquidated damages (willful violations - double back pay)", "Front pay", "Reinstatement", "Attorneys fees", "NOTE: No compensatory or punitive damages under federal ADEA"],
        "leading_cases": ["Gross v. FBL Financial Services, 557 U.S. 167 (2009)", "Hazen Paper Co. v. Biggins, 507 U.S. 604 (1993)", "Smith v. City of Jackson, 544 U.S. 228 (2005)", "OConnor v. Consolidated Coin Caterers, 517 U.S. 308 (1996)"],
        "confidence": 0.93,
        "last_updated": "2026-01-15",
        "tags": ["adea", "age_discrimination", "over_40", "owbpa", "but_for_causation"],
    },

    # ============================================================================
    # FMLA / FAMILY AND MEDICAL LEAVE
    # ============================================================================

    "fmla_overview": {
        "topic": "fmla_overview",
        "title": "Family and Medical Leave Act (FMLA)",
        "category": "fmla",
        "summary": "FMLA entitles eligible employees of covered employers to 12 workweeks of unpaid, job-protected leave per year for: (1) birth/adoption/foster placement of child, (2) serious health condition of spouse/parent/child, (3) employee own serious health condition, (4) qualifying military exigency. Military caregiver leave provides 26 weeks. Eligibility requires 12 months employment and 1,250 hours worked in prior 12 months at a worksite with 50+ employees within 75 miles. Employer must maintain group health insurance. Employee entitled to same or equivalent position upon return. Two claim types: interference (denying rights) and retaliation (adverse action for exercising rights).",
        "key_statutes": ["29 U.S.C. 2601-2654", "29 U.S.C. 2612 (leave entitlement)", "29 U.S.C. 2614 (employment and benefits protection)", "29 U.S.C. 2615 (prohibited acts)", "29 C.F.R. Part 825"],
        "elements": ["Eligible employee (12 months, 1250 hours, 50-employee threshold)", "Qualifying reason (serious health condition, birth/adoption, military)", "Proper notice given", "Employer interference or retaliation"],
        "defenses": ["Employee not eligible", "Not a qualifying reason", "Not a serious health condition", "Employee failed to provide adequate notice", "Employee failed to provide required certification", "Key employee defense (top 10% salaried)"],
        "remedies": ["Back pay and benefits", "Liquidated damages (equal to back pay for willful)", "Equitable relief (reinstatement)", "Attorneys fees and costs"],
        "leading_cases": ["Ragsdale v. Wolverine World Wide, 535 U.S. 81 (2002)", "Hodgens v. General Dynamics Corp., 144 F.3d 151 (1st Cir. 1998)", "Liu v. Amway Corp., 347 F.3d 1125 (9th Cir. 2003)"],
        "confidence": 0.94,
        "last_updated": "2026-01-15",
        "tags": ["fmla", "family_leave", "medical_leave", "serious_health_condition", "job_protection"],
    },

    "fmla_interference": {
        "topic": "fmla_interference",
        "title": "FMLA Interference Claims",
        "category": "fmla",
        "summary": "FMLA interference occurs when an employer denies or impedes an employee's exercise of FMLA rights. Unlike retaliation, interference does not require discriminatory intent. The employer's motive is irrelevant - the question is whether the employee was denied a benefit to which they were entitled. Examples include: refusing to authorize leave, discouraging employee from taking leave, counting FMLA absences as attendance violations, failing to inform employee of FMLA rights, failing to maintain health insurance during leave, failing to restore to same or equivalent position.",
        "key_statutes": ["29 U.S.C. 2615(a)(1)", "29 C.F.R. 825.220"],
        "elements": ["Entitled to FMLA leave", "Employer denied the benefit or interfered with the right", "Prejudice to employee from denial"],
        "defenses": ["Employee not eligible for FMLA", "No qualifying reason", "Employee would have been terminated regardless (honest suspicion doctrine)", "Employee failed to comply with notice requirements"],
        "remedies": ["Reinstatement", "Back pay and benefits lost", "Liquidated damages", "Attorneys fees"],
        "leading_cases": ["Ragsdale v. Wolverine World Wide, 535 U.S. 81 (2002)", "Stallings v. Hussmann Corp., 447 F.3d 1041 (8th Cir. 2006)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["fmla", "interference", "denial_of_leave", "restoration_right"],
    },

    # ============================================================================
    # FLSA / WAGE AND HOUR
    # ============================================================================

    "flsa_overtime": {
        "topic": "flsa_overtime",
        "title": "FLSA Overtime Compensation Requirements",
        "category": "flsa",
        "summary": "The FLSA requires covered nonexempt employees to receive overtime pay at 1.5 times their regular rate for all hours worked over 40 in a workweek. The regular rate includes all remuneration except statutory exclusions (gifts, vacation pay, retirement contributions, etc.). Compensatory time in lieu of overtime is generally prohibited in the private sector. The fluctuating workweek method may apply for salaried nonexempt employees. Employers cannot average hours across workweeks. Each workweek stands alone. Willful violations have a 3-year statute of limitations (2 years for non-willful).",
        "key_statutes": ["29 U.S.C. 207(a)(1)", "29 U.S.C. 207(e) (regular rate definition)", "29 C.F.R. Part 778 (overtime computation)", "29 C.F.R. Part 541 (exemptions)"],
        "elements": ["Covered, nonexempt employee", "Hours worked exceeding 40 in workweek", "Failure to pay at 1.5x regular rate", "Employer knew or should have known of hours worked"],
        "defenses": ["Employee is exempt (executive, administrative, professional, computer, outside sales)", "Employee is not covered", "De minimis overtime", "Good faith reliance on DOL opinion letter", "Portal-to-Portal Act defenses"],
        "remedies": ["Unpaid overtime wages", "Liquidated damages (equal to unpaid wages, presumed unless good faith)", "Attorneys fees and costs", "3-year SOL for willful violations"],
        "leading_cases": ["IBP, Inc. v. Alvarez, 546 U.S. 21 (2005)", "Encino Motorcars v. Navarro, 584 U.S. ___ (2018)", "Integrity Staffing Solutions v. Busk, 574 U.S. 27 (2014)"],
        "confidence": 0.94,
        "last_updated": "2026-01-15",
        "tags": ["flsa", "overtime", "regular_rate", "workweek", "time_and_a_half"],
    },

    "flsa_exemptions": {
        "topic": "flsa_exemptions",
        "title": "FLSA White Collar Exemptions",
        "category": "flsa",
        "summary": "The FLSA exempts from overtime (and sometimes minimum wage) employees meeting specific duties and salary tests. Executive: manages enterprise/department, supervises 2+ FTEs, has hiring authority. Administrative: office/non-manual work directly related to management/business operations, exercises discretion and independent judgment. Professional: learned (advanced knowledge, intellectual character, prolonged education) or creative (invention, imagination, originality). Computer: systems analyst, programmer, software engineer at salary/hourly threshold. Outside Sales: customarily works away from employer premises making sales. Highly Compensated Employee (HCE): $107,432+ total annual compensation performing at least one exempt duty.",
        "key_statutes": ["29 U.S.C. 213(a)(1)", "29 C.F.R. Part 541", "29 C.F.R. 541.100 (executive)", "29 C.F.R. 541.200 (administrative)", "29 C.F.R. 541.300 (professional)", "29 C.F.R. 541.400 (computer)", "29 C.F.R. 541.500 (outside sales)", "29 C.F.R. 541.601 (HCE)"],
        "elements": ["Salary basis test (minimum $844/week as of 2024 DOL rule)", "Salary level test", "Duties test for specific exemption category"],
        "defenses": ["Employee meets all three tests for applicable exemption", "Combination exemption (HCE)", "Window of correction for improper deductions"],
        "remedies": ["Reclassification to nonexempt", "Back overtime pay for 2-3 years", "Liquidated damages", "Attorneys fees"],
        "leading_cases": ["Encino Motorcars v. Navarro, 584 U.S. ___ (2018)", "Auer v. Robbins, 519 U.S. 452 (1997)", "Christopher v. SmithKline Beecham, 567 U.S. 142 (2012)"],
        "confidence": 0.93,
        "last_updated": "2026-01-15",
        "tags": ["flsa", "exemptions", "executive", "administrative", "professional", "salary_test", "duties_test"],
    },

    "worker_misclassification": {
        "topic": "worker_misclassification",
        "title": "Worker Misclassification - Employee vs. Independent Contractor",
        "category": "flsa",
        "summary": "Worker classification determines entitlement to wage/hour protections, benefits, tax treatment, and other employment rights. The FLSA uses the economic reality test (6 factors): (1) nature and degree of employer control, (2) workers opportunity for profit or loss, (3) workers investment in equipment/materials, (4) whether work requires special skill, (5) degree of permanence, (6) whether work is integral part of employers business. The DOL 2024 rule restored the totality-of-circumstances economic reality test. IRS uses the common law right-to-control test (3 categories: behavioral control, financial control, type of relationship). ABC test used in some states (California AB5). Misclassification exposes employers to back taxes, FLSA liability, benefits liability, and penalties.",
        "key_statutes": ["29 U.S.C. 203(e)(1) (employee definition)", "29 C.F.R. Part 795 (DOL rule)", "IRC 3401/3121 (IRS classification)", "IRS Rev. Rul. 87-41 (20 factors)"],
        "elements": ["Worker performing services", "Employer treating worker as independent contractor", "Economic reality factors favoring employee status"],
        "defenses": ["Legitimate independent contractor relationship", "Section 530 safe harbor (IRS)", "Industry practice", "Written contractor agreement (not dispositive)"],
        "remedies": ["Reclassification and back wages", "Overtime pay", "Tax liability and penalties", "Benefits enrollment", "Workers compensation coverage"],
        "leading_cases": ["Nationwide Mutual Insurance v. Darden, 503 U.S. 318 (1992)", "Rutherford Food Corp. v. McComb, 331 U.S. 722 (1947)", "Dynamex Operations West v. Superior Court, 4 Cal. 5th 903 (2018)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["misclassification", "independent_contractor", "employee", "economic_reality", "abc_test"],
    },

    # ============================================================================
    # OSHA / WORKPLACE SAFETY
    # ============================================================================

    "osha_general_duty": {
        "topic": "osha_general_duty",
        "title": "OSHA General Duty Clause and Workplace Safety",
        "category": "osha",
        "summary": "Section 5(a)(1) of the OSH Act (General Duty Clause) requires employers to furnish a workplace free from recognized hazards causing or likely to cause death or serious physical harm. OSHA enforces specific standards (29 C.F.R. Parts 1910/1926) and the general duty clause where no specific standard exists. Citation categories: Other-Than-Serious, Serious, Willful, Repeat, Failure to Abate. Penalties range from advisory to $156,259 per willful violation (2024). Employees have right to file complaints without retaliation under Section 11(c). Multi-employer worksite doctrine extends liability to controlling, creating, correcting, and exposing employers.",
        "key_statutes": ["29 U.S.C. 654(a)(1) (General Duty Clause)", "29 U.S.C. 654(a)(2) (compliance with standards)", "29 U.S.C. 660(c) (anti-retaliation)", "29 C.F.R. Part 1910 (General Industry)", "29 C.F.R. Part 1926 (Construction)"],
        "elements": ["Recognized hazard", "Causing or likely to cause death or serious harm", "Feasible means to abate hazard", "Employer knew or should have known"],
        "defenses": ["Greater hazard defense", "Infeasibility of compliance", "Unpreventable employee misconduct", "De minimis violation", "Variance from standard"],
        "remedies": ["Abatement of hazard", "Monetary penalties (up to $156,259 per willful violation)", "Criminal prosecution for willful violations causing death"],
        "leading_cases": ["Secretary of Labor v. Trinity Industries, 15 BNA OSHC 1481 (1992)", "National Realty & Construction v. OSHRC, 489 F.2d 1257 (D.C. Cir. 1973)", "SeaWorld of Florida v. Perez, 748 F.3d 1202 (D.C. Cir. 2014)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["osha", "general_duty", "workplace_safety", "citation", "hazard"],
    },

    # ============================================================================
    # ERISA / EMPLOYEE BENEFITS
    # ============================================================================

    "erisa_overview": {
        "topic": "erisa_overview",
        "title": "Employee Retirement Income Security Act (ERISA)",
        "category": "erisa",
        "summary": "ERISA sets minimum standards for most private employee benefit plans (pension and welfare). Preempts state laws relating to employee benefit plans (broad preemption). Fiduciary duties: loyalty (exclusive benefit of participants), prudence (prudent expert standard), diversification (pension investments), plan document compliance. Section 510 prohibits interference with protected rights (firing to prevent vesting). ERISA claims are reviewed under arbitrary and capricious standard (where plan grants discretionary authority) or de novo. Remedies under Section 502(a) include plan benefits, breach of fiduciary duty actions, injunctive relief, and attorneys fees in courts discretion.",
        "key_statutes": ["29 U.S.C. 1001-1461", "29 U.S.C. 1104 (fiduciary duties)", "29 U.S.C. 1132(a) (civil enforcement)", "29 U.S.C. 1140 (Section 510 interference)", "29 U.S.C. 1144 (preemption)"],
        "elements": ["Employee benefit plan covered by ERISA", "Denial of benefits or fiduciary breach", "Exhaustion of administrative remedies (for benefits claims)"],
        "defenses": ["Plan terms support denial", "Reasonable interpretation of ambiguous terms", "ERISA preemption of state law claims", "Statute of limitations"],
        "remedies": ["Recovery of plan benefits (502(a)(1)(B))", "Equitable relief for fiduciary breach (502(a)(3))", "Attorneys fees in court discretion", "Surcharge for fiduciary breach"],
        "leading_cases": ["Firestone Tire & Rubber v. Bruch, 489 U.S. 101 (1989)", "Metropolitan Life Insurance v. Glenn, 554 U.S. 105 (2008)", "Conkright v. Frommert, 559 U.S. 506 (2010)", "CIGNA Corp. v. Amara, 563 U.S. 421 (2011)"],
        "confidence": 0.91,
        "last_updated": "2026-01-15",
        "tags": ["erisa", "benefits", "fiduciary_duty", "preemption", "pension", "section_510"],
    },

    # ============================================================================
    # NLRA / LABOR RELATIONS
    # ============================================================================

    "nlra_overview": {
        "topic": "nlra_overview",
        "title": "National Labor Relations Act (NLRA) - Concerted Activity",
        "category": "nlra",
        "summary": "The NLRA protects employees right to organize, bargain collectively, and engage in concerted activities for mutual aid or protection (Section 7). Also protects the right to refrain from such activities. Employer unfair labor practices (Section 8(a)) include: interfering with Section 7 rights, dominating/assisting labor organizations, discriminating for union activity, retaliating for NLRB charges, and refusing to bargain. Union unfair labor practices (Section 8(b)). NLRB enforces through administrative proceedings and federal court injunctions. Protected concerted activity extends beyond union contexts to include non-union employees acting together regarding wages, hours, or working conditions. Social media policies that chill Section 7 rights may violate the NLRA.",
        "key_statutes": ["29 U.S.C. 151-169", "29 U.S.C. 157 (Section 7 rights)", "29 U.S.C. 158(a) (employer ULPs)", "29 U.S.C. 158(b) (union ULPs)", "29 C.F.R. Parts 101-103"],
        "elements": ["Concerted activity (two or more employees OR individual acting on behalf of group)", "For mutual aid or protection", "Not unprotected (violence, disloyalty, breach of confidentiality of labor relations info)"],
        "defenses": ["Activity was not concerted", "Activity not for mutual aid/protection", "Activity lost protection (violence, insubordination)", "Wright Line mixed-motive analysis (employer would have taken same action)"],
        "remedies": ["Reinstatement with back pay", "Cease and desist order", "Notice posting", "Bargaining order", "Make-whole relief"],
        "leading_cases": ["NLRB v. Washington Aluminum Co., 370 U.S. 9 (1962)", "NLRB v. Weingarten, 420 U.S. 251 (1975)", "Epic Systems Corp. v. Lewis, 584 U.S. ___ (2018)", "Wright Line, 251 NLRB 1083 (1980)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["nlra", "section_7", "concerted_activity", "union", "unfair_labor_practice"],
    },

    # ============================================================================
    # WORKERS COMPENSATION
    # ============================================================================

    "workers_compensation": {
        "topic": "workers_compensation",
        "title": "Workers Compensation - General Principles",
        "category": "workers_comp",
        "summary": "Workers compensation is a state-regulated no-fault insurance system providing benefits for work-related injuries and illnesses. The exclusive remedy doctrine generally bars tort claims against the employer (exceptions: intentional tort, dual capacity). Benefits include: medical expenses, temporary total/partial disability, permanent total/partial disability, vocational rehabilitation, death benefits. Employee must show injury arising out of and in the course of employment. Key issues: compensability, degree of disability, maximum medical improvement, independent medical examination. Retaliation for filing workers comp claims is prohibited in most states (Texas Labor Code Chapter 451). Federal employees covered by FECA.",
        "key_statutes": ["State Workers Compensation Acts (vary by state)", "Texas Labor Code Ch. 401-506", "Texas Labor Code Ch. 451 (anti-retaliation)", "5 U.S.C. 8101-8193 (FECA for federal employees)"],
        "elements": ["Employment relationship", "Injury or occupational disease", "Arising out of employment (causal connection)", "In the course of employment (time, place, activity)"],
        "defenses": ["Injury did not arise out of employment", "Employee was not in course of employment", "Willful misconduct (some states)", "Intoxication (some states)", "Pre-existing condition", "Statute of limitations"],
        "remedies": ["Medical benefits", "Income benefits (temporary/permanent, total/partial)", "Vocational rehabilitation", "Death benefits", "Supplemental income benefits"],
        "leading_cases": ["State-specific case law predominates", "Kroger Co. v. Keng, 23 S.W.3d 347 (Tex. 2000)", "Transcontinental Insurance Co. v. Crump, 330 S.W.3d 211 (Tex. 2010)"],
        "confidence": 0.88,
        "last_updated": "2026-01-15",
        "tags": ["workers_comp", "work_injury", "no_fault", "exclusive_remedy", "disability_benefits"],
    },

    # ============================================================================
    # AT-WILL EMPLOYMENT
    # ============================================================================

    "at_will_employment": {
        "topic": "at_will_employment",
        "title": "At-Will Employment Doctrine and Exceptions",
        "category": "termination",
        "summary": "Under the at-will doctrine, either employer or employee may terminate the employment relationship at any time, for any reason not prohibited by law. All US states recognize at-will employment as the default rule. Three major exceptions: (1) Public Policy Exception - termination violates clear public policy (refusing illegal act, exercising legal right, reporting violation). Recognized in most states (NOT recognized in some states including at-will-pure states). (2) Implied Contract Exception - employer statements or conduct create implied promise of continued employment (handbooks, policies, oral assurances). (3) Implied Covenant of Good Faith and Fair Dealing - recognized in few states (e.g., Montana Wrongful Discharge from Employment Act). Texas follows at-will with narrow public policy exception (Sabine Pilot).",
        "key_statutes": ["State common law (varies by jurisdiction)", "Montana Wrongful Discharge from Employment Act (MCA 39-2-901)", "Texas: Sabine Pilot Service v. Hauck, 687 S.W.2d 733 (Tex. 1985)"],
        "elements": ["Employment relationship existed", "Termination occurred", "Termination violated recognized exception (public policy, implied contract, good faith)"],
        "defenses": ["At-will relationship with no applicable exception", "Legitimate business reason", "No implied contract formed", "Public policy exception not recognized in jurisdiction", "Employee handbook disclaimer effective"],
        "remedies": ["Contract damages (if implied contract)", "Tort damages (if public policy)", "Lost wages", "Emotional distress (some jurisdictions)", "Punitive damages (some jurisdictions)"],
        "leading_cases": ["Sabine Pilot Service v. Hauck, 687 S.W.2d 733 (Tex. 1985)", "Toussaint v. Blue Cross, 408 Mich. 579 (1980)", "Foley v. Interactive Data Corp., 47 Cal.3d 654 (1988)", "Woolley v. Hoffmann-La Roche, 99 N.J. 284 (1985)"],
        "confidence": 0.91,
        "last_updated": "2026-01-15",
        "tags": ["at_will", "wrongful_termination", "public_policy", "implied_contract", "good_faith"],
    },

    # ============================================================================
    # NON-COMPETE AGREEMENTS
    # ============================================================================

    "non_compete_enforceability": {
        "topic": "non_compete_enforceability",
        "title": "Non-Compete Agreement Enforceability",
        "category": "non_compete",
        "summary": "Non-compete agreements restrict former employees from competing with their employer for a specified period in a defined geographic area. Enforceability varies dramatically by state. General rule: must be (1) supported by adequate consideration, (2) reasonable in scope (duration, geography, activity restricted), (3) necessary to protect legitimate business interest (trade secrets, customer relationships, specialized training). Texas Business and Commerce Code 15.50: enforceable if ancillary to otherwise enforceable agreement, reasonable scope, and protects goodwill or trade secrets. California generally prohibits non-competes (Cal. Bus. & Prof. Code 16600). FTC proposed rule to ban most non-competes (challenged in court). Blue-pencil doctrine allows courts to reform overbroad provisions in some states. Texas courts will reform to make reasonable.",
        "key_statutes": ["Texas Bus. & Com. Code 15.50-15.52", "Cal. Bus. & Prof. Code 16600", "FTC Non-Compete Rule (proposed/challenged)", "Uniform Trade Secrets Act (adopted in most states)", "18 U.S.C. 1836 (Defend Trade Secrets Act)"],
        "elements": ["Valid agreement (offer, acceptance, consideration)", "Reasonable duration (typically 1-2 years)", "Reasonable geographic scope", "Reasonable activity restriction", "Protects legitimate business interest"],
        "defenses": ["Overbroad (duration, geography, or activity)", "Lack of consideration", "Unconscionable", "Employee did not have access to protectable interests", "Employer breach (unclean hands)", "Statutory prohibition (California)", "Changed circumstances"],
        "remedies": ["Injunctive relief (TRO/preliminary/permanent)", "Damages for breach", "Attorneys fees (contractual or statutory)", "Reformation (blue pencil) in some jurisdictions"],
        "leading_cases": ["Marsh USA v. Cook, 354 S.W.3d 764 (Tex. 2011)", "Alex Sheshunoff Management v. Johnson, 209 S.W.3d 644 (Tex. 2006)", "Edwards v. Arthur Andersen LLP, 44 Cal.4th 937 (2008)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["non_compete", "restrictive_covenant", "enforceability", "trade_secrets", "blue_pencil"],
    },

    # ============================================================================
    # WARN ACT
    # ============================================================================

    "warn_act": {
        "topic": "warn_act",
        "title": "Worker Adjustment and Retraining Notification Act (WARN)",
        "category": "warn_act",
        "summary": "The WARN Act requires covered employers (100+ full-time employees) to provide 60 calendar days advance written notice before plant closings or mass layoffs. Plant closing: permanent/temporary shutdown of single site or operating unit causing 50+ employee employment losses. Mass layoff: employment loss at single site affecting 500+ employees OR 50-499 employees if 33%+ of active workforce. Employment loss includes termination, layoff exceeding 6 months, and 50%+ hours reduction for 6+ months. Notice required to affected workers, state dislocated worker unit, and chief elected official of local government.",
        "key_statutes": ["29 U.S.C. 2101-2109", "20 C.F.R. Part 639"],
        "elements": ["Covered employer (100+ employees)", "Plant closing or mass layoff", "Failure to provide 60-day written notice", "Employment loss to affected employees"],
        "defenses": ["Faltering company exception (plant closing only, actively seeking capital)", "Unforeseeable business circumstances", "Natural disaster", "Strike or lockout", "Temporary facility or project completion", "Employee on leave who received adequate notice"],
        "remedies": ["Back pay for each day of violation (up to 60 days)", "Benefits for violation period", "Civil penalty up to $500/day to local government (can be avoided by paying employees within 3 weeks)", "Attorneys fees"],
        "leading_cases": ["Local 397, IUE v. Midwest Fasteners, 763 F. Supp. 78 (D.N.J. 1990)", "Rifkin v. McDonnell Douglas Corp., 78 F.3d 1277 (8th Cir. 1996)", "Gross v. Hale-Halsell Co., 554 F.3d 870 (10th Cir. 2009)"],
        "confidence": 0.91,
        "last_updated": "2026-01-15",
        "tags": ["warn_act", "mass_layoff", "plant_closing", "60_day_notice", "employment_loss"],
    },

    # ============================================================================
    # WHISTLEBLOWER PROTECTION
    # ============================================================================

    "whistleblower_protection": {
        "topic": "whistleblower_protection",
        "title": "Federal Whistleblower Protection Laws",
        "category": "whistleblower",
        "summary": "Multiple federal statutes protect employee whistleblowers from retaliation. Sarbanes-Oxley Section 806 (18 U.S.C. 1514A): protects employees of publicly traded companies who report securities fraud. Dodd-Frank Section 922: protects individuals who report securities violations to the SEC (bounty program 10-30% of sanctions over $1M). False Claims Act (31 U.S.C. 3730): qui tam provisions allow individuals to sue on behalf of US government for fraud, with protection from retaliation. OSHA Section 11(c): protects employees who report safety violations. Many industry-specific protections: airline (AIR21), nuclear (ERA), pipeline (PSIA), environmental (CAA, CWA, SWDA). State whistleblower statutes also apply.",
        "key_statutes": ["18 U.S.C. 1514A (SOX)", "15 U.S.C. 78u-6 (Dodd-Frank)", "31 U.S.C. 3730 (False Claims Act)", "29 U.S.C. 660(c) (OSHA 11(c))", "Texas Gov. Code Ch. 554 (TX Whistleblower)"],
        "elements": ["Protected disclosure (reasonable belief of violation)", "Adverse action by employer", "Causal connection between disclosure and adverse action"],
        "defenses": ["No reasonable belief of violation", "No adverse action", "No causal connection", "After-acquired evidence", "Legitimate business reason"],
        "remedies": ["Reinstatement", "Back pay with interest", "Compensatory damages", "Special damages", "Attorneys fees", "SEC bounty (Dodd-Frank: 10-30% of sanctions over $1M)", "Double back pay (False Claims Act)"],
        "leading_cases": ["Digital Realty Trust v. Somers, 583 U.S. ___ (2018)", "Lawson v. FMR LLC, 571 U.S. 429 (2014)", "Murray v. UBS Securities, 601 U.S. ___ (2024)"],
        "confidence": 0.91,
        "last_updated": "2026-01-15",
        "tags": ["whistleblower", "sox", "dodd_frank", "false_claims", "qui_tam", "retaliation"],
    },

    # ============================================================================
    # TEXAS LABOR CODE
    # ============================================================================

    "texas_payday_law": {
        "topic": "texas_payday_law",
        "title": "Texas Payday Law (Chapter 61)",
        "category": "texas_labor",
        "summary": "The Texas Payday Law (Labor Code Chapter 61) governs payment of wages in Texas. Employers must pay wages in full on regularly scheduled paydays. Upon separation, final wages due within 6 days if fired, or next regular payday if employee quits. Wages include compensation owed under employment agreement (salary, commissions, bonuses, overtime, vacation accrual if promised). TWC administers wage claims. Employee must file claim within 180 days of wages becoming due. Employer penalty for failure to pay: liable for wages plus potential administrative penalty. No private cause of action (must go through TWC). Preempted by FLSA for minimum wage and overtime claims.",
        "key_statutes": ["Tex. Lab. Code 61.001-61.095", "Tex. Lab. Code 61.011 (pay periods)", "Tex. Lab. Code 61.014 (final pay timing)", "Tex. Lab. Code 61.051 (wage claims)"],
        "elements": ["Employer-employee relationship in Texas", "Wages due under agreement", "Failure to pay on time", "Claim filed within 180 days"],
        "defenses": ["No agreement to pay disputed amount", "Wages were paid in full", "Claim filed outside 180-day window", "Independent contractor relationship"],
        "remedies": ["Payment of unpaid wages through TWC order", "Administrative penalties", "No private right of action (TWC administrative process only)"],
        "leading_cases": ["Midland Judicial District Community Supervision v. Jones, 92 S.W.3d 486 (Tex. 2002)", "Texas Workforce Commission precedent decisions"],
        "confidence": 0.89,
        "last_updated": "2026-01-15",
        "tags": ["texas", "payday_law", "wage_claim", "twc", "final_pay"],
    },

    "texas_employment_discrimination": {
        "topic": "texas_employment_discrimination",
        "title": "Texas Commission on Human Rights Act (TCHRA)",
        "category": "texas_labor",
        "summary": "The TCHRA (Texas Labor Code Chapter 21) is the state analog to Title VII and the ADA. Prohibits discrimination based on race, color, disability, religion, sex, national origin, and age (40+). Applies to employers with 15+ employees (age: 20+). Provides for compensatory and punitive damages with caps matching Title VII. Requires filing with TWC Civil Rights Division within 180 days (or 300 days if cross-filed with EEOC). Exhaustion of administrative remedies required. 60-day right-to-sue waiting period. Claims substantially mirror federal standards but interpreted under Texas law. Important: Texas courts apply Quantum Chemical burden-shifting framework similar to McDonnell Douglas.",
        "key_statutes": ["Tex. Lab. Code 21.001-21.556", "Tex. Lab. Code 21.051 (unlawful practices)", "Tex. Lab. Code 21.125 (disability accommodation)", "Tex. Lab. Code 21.201-21.262 (enforcement)"],
        "elements": ["Protected class under TCHRA", "Qualified for position", "Adverse employment action", "Causal connection to protected status"],
        "defenses": ["Legitimate nondiscriminatory reason", "BFOQ", "Undue hardship (disability)", "Not covered employer", "Untimely filing"],
        "remedies": ["Compensatory damages (capped by employer size)", "Punitive damages (capped)", "Back pay", "Equitable relief", "Attorneys fees", "Injunctive relief"],
        "leading_cases": ["Quantum Chemical Corp. v. Toennies, 47 S.W.3d 473 (Tex. 2001)", "Mission Consolidated ISD v. Garcia, 372 S.W.3d 629 (Tex. 2012)", "Prairie View A&M University v. Chatha, 381 S.W.3d 500 (Tex. 2012)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["texas", "tchra", "discrimination", "twc_civil_rights", "chapter_21"],
    },

    # ============================================================================
    # CONSTRUCTIVE DISCHARGE
    # ============================================================================

    "constructive_discharge": {
        "topic": "constructive_discharge",
        "title": "Constructive Discharge Claims",
        "category": "termination",
        "summary": "Constructive discharge occurs when an employer makes working conditions so intolerable that a reasonable person would feel compelled to resign. Under Pennsylvania State Police v. Suders (2004), the standard is whether a reasonable person in the employees position would have felt compelled to resign. In the harassment context, if constructive discharge involves an official act (demotion, undesirable transfer), the Ellerth/Faragher affirmative defense is unavailable. The employee must show: (1) deliberate employer action or a knowing failure to act, (2) conditions so difficult that a reasonable employee would feel compelled to resign. Courts consider factors such as demotion, reduction in pay, reduced responsibilities, reassignment to degrading work, badgering and harassment, and denial of promotion. The employee generally should give the employer notice and opportunity to correct before resigning.",
        "key_statutes": ["42 U.S.C. 2000e-2(a)(1) (via case law development)", "Common law tort principles"],
        "elements": ["Intolerable working conditions", "Conditions created or permitted by employer", "Reasonable person would have resigned", "Employee actually resigned", "Employer action was deliberate or foreseeable"],
        "defenses": ["Conditions were not intolerable by objective standard", "Employee failed to use available grievance procedures", "Employee resigned for other reasons", "Employer took prompt corrective action", "Insufficient duration or severity of conditions"],
        "remedies": ["Same as wrongful termination: back pay, front pay, compensatory damages, punitive damages (if underlying violation supports), reinstatement, attorneys fees"],
        "leading_cases": ["Pennsylvania State Police v. Suders, 542 U.S. 129 (2004)", "Green v. Brennan, 578 U.S. 547 (2016)", "Colwell v. Rite Aid Corp., 602 F.3d 495 (3d Cir. 2010)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["constructive_discharge", "forced_resignation", "intolerable_conditions", "termination"],
    },

    # ============================================================================
    # EQUAL PAY ACT
    # ============================================================================

    "equal_pay_act": {
        "topic": "equal_pay_act",
        "title": "Equal Pay Act of 1963",
        "category": "flsa",
        "summary": "The Equal Pay Act (29 U.S.C. 206(d)) prohibits sex-based wage discrimination for equal work on jobs requiring substantially equal skill, effort, and responsibility under similar working conditions at the same establishment. Unlike Title VII, no EEOC filing is required before suit. Strict liability applies - no intent to discriminate required. The plaintiff must show: (1) different wages paid to employees of opposite sex, (2) for equal work on jobs requiring substantially equal skill, effort, and responsibility, (3) performed under similar working conditions. The employer has four affirmative defenses: (1) seniority system, (2) merit system, (3) quantity/quality of production, (4) any factor other than sex. The fourth defense (factor other than sex) is the most litigated. Liquidated damages are available for willful violations.",
        "key_statutes": ["29 U.S.C. 206(d)", "29 C.F.R. Part 1620 (EEOC interpretation)", "Lilly Ledbetter Fair Pay Act of 2009"],
        "elements": ["Employees of opposite sex", "Equal work (substantially equal skill, effort, responsibility)", "Similar working conditions", "Same establishment", "Unequal pay"],
        "defenses": ["Seniority system", "Merit system", "Quantity or quality of production", "Factor other than sex (any legitimate factor)", "Jobs are not substantially equal"],
        "remedies": ["Back pay (difference in wages)", "Liquidated damages (equal to back pay for willful violations)", "Attorneys fees", "Injunctive relief", "2-year SOL (3 years for willful)"],
        "leading_cases": ["Corning Glass Works v. Brennan, 417 U.S. 188 (1974)", "Ledbetter v. Goodyear Tire & Rubber Co., 550 U.S. 618 (2007) (superseded by Ledbetter Act)", "EEOC v. Madison Community Unit School Dist., 818 F.2d 577 (7th Cir. 1987)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["equal_pay", "epa", "wage_discrimination", "sex_discrimination", "ledbetter"],
    },

    # ============================================================================
    # EMPLOYMENT ARBITRATION
    # ============================================================================

    "employment_arbitration": {
        "topic": "employment_arbitration",
        "title": "Employment Arbitration Agreements",
        "category": "general_employment",
        "summary": "Employment arbitration agreements are generally enforceable under the Federal Arbitration Act (FAA). Epic Systems Corp. v. Lewis (2018) held that class/collective action waivers in arbitration agreements are enforceable and do not violate the NLRA. Unconscionability remains the primary defense: procedural unconscionability (take-it-or-leave-it, no negotiation, hidden terms) and substantive unconscionability (one-sided fee allocation, limited remedies, shortened SOL, unfair discovery limits). The Ending Forced Arbitration of Sexual Assault and Sexual Harassment Act of 2022 (EFAA) allows employees to void pre-dispute arbitration agreements for sexual assault and sexual harassment claims. Delegation clauses (arbitrator decides arbitrability) enforceable if clear and unmistakable. State law may impose additional requirements (California PAGA claims have unique rules).",
        "key_statutes": ["9 U.S.C. 1-16 (Federal Arbitration Act)", "Ending Forced Arbitration Act of 2022 (EFAA)", "9 U.S.C. 401-402 (EFAA provisions)"],
        "elements": ["Valid arbitration agreement", "Covered dispute", "Mutual assent", "Adequate consideration"],
        "defenses": ["Procedural unconscionability", "Substantive unconscionability", "EFAA exemption (sexual assault/harassment)", "Waiver by litigation conduct", "Agreement does not cover the dispute", "FAA transportation worker exemption (9 U.S.C. 1)"],
        "remedies": ["Motion to compel arbitration", "Stay of litigation pending arbitration", "Arbitration award (monetary, injunctive)", "Limited judicial review of award (FAA 10-11)"],
        "leading_cases": ["Epic Systems Corp. v. Lewis, 584 U.S. ___ (2018)", "AT&T Mobility v. Concepcion, 563 U.S. 333 (2011)", "New Prime Inc. v. Oliveira, 586 U.S. ___ (2019)", "Morgan v. Sundance, 596 U.S. ___ (2022)"],
        "confidence": 0.91,
        "last_updated": "2026-01-15",
        "tags": ["arbitration", "faa", "class_waiver", "unconscionability", "efaa"],
    },

    # ============================================================================
    # GENETIC INFORMATION (GINA)
    # ============================================================================

    "gina_discrimination": {
        "topic": "gina_discrimination",
        "title": "Genetic Information Nondiscrimination Act (GINA)",
        "category": "title_vii",
        "summary": "GINA Title II prohibits employment discrimination based on genetic information. Genetic information includes: (1) individual genetic tests, (2) family member genetic tests, (3) family medical history, (4) requests for or receipt of genetic services, (5) genetic information of a fetus or embryo. Employers cannot use genetic information in employment decisions, cannot request or require genetic information (with narrow exceptions), and cannot retaliate against employees who oppose GINA violations or participate in proceedings. Exceptions include inadvertent acquisition (water cooler rule), wellness programs with voluntary genetic testing, FMLA certification (family medical history), commercially available monitoring of biological effects of toxic substances, and law enforcement DNA programs.",
        "key_statutes": ["42 U.S.C. 2000ff et seq.", "42 U.S.C. 2000ff-1 (employer practices)", "29 C.F.R. Part 1635 (EEOC regulations)"],
        "elements": ["Genetic information (as defined)", "Use in employment decision OR unlawful acquisition OR retaliation", "Covered employer (15+ employees)"],
        "defenses": ["Inadvertent acquisition", "Wellness program exception (voluntary)", "FMLA certification exception", "Commercially available monitoring exception", "Information not genetic under GINA definition"],
        "remedies": ["Same as Title VII: compensatory damages (capped), punitive damages (capped), back pay, injunctive relief, attorneys fees"],
        "leading_cases": ["Lowe v. Atlas Logistics Group Retail Services, 102 F. Supp. 3d 1360 (N.D. Ga. 2015)", "EEOC v. Fabricut Inc., No. 13-CV-248 (N.D. Okla. 2013)"],
        "confidence": 0.88,
        "last_updated": "2026-01-15",
        "tags": ["gina", "genetic_information", "genetic_testing", "family_medical_history"],
    },

    # ============================================================================
    # USERRA (Military Service)
    # ============================================================================

    "userra_military": {
        "topic": "userra_military",
        "title": "Uniformed Services Employment and Reemployment Rights Act (USERRA)",
        "category": "general_employment",
        "summary": "USERRA protects service members rights to civilian employment before, during, and after military service. Key provisions: (1) reemployment rights after military service (up to 5 cumulative years), (2) anti-discrimination - cannot deny employment, reemployment, retention, promotion, or benefits because of military obligation, (3) escalator principle - reemployment in position the person would have attained with reasonable certainty absent the service, (4) health insurance continuation (up to 24 months), (5) pension service credit for periods of military service. Applies to all employers regardless of size. No EEOC filing required. Enforced by DOL VETS and private right of action. Reporting requirements: advance notice (written or oral) unless military necessity prevents. No statute of limitations for USERRA claims.",
        "key_statutes": ["38 U.S.C. 4301-4335", "38 U.S.C. 4311 (discrimination)", "38 U.S.C. 4312 (reemployment rights)", "38 U.S.C. 4316 (health/pension)", "20 C.F.R. Part 1002"],
        "elements": ["Uniformed service (as defined)", "Gave advance notice to employer", "Cumulative service not exceeding 5 years", "Timely application for reemployment", "Honorable discharge or equivalent"],
        "defenses": ["Changed circumstances making reemployment impossible or unreasonable", "Undue hardship to employer (accommodation only)", "Service exceeding 5-year limit (with exceptions)", "Less than honorable discharge", "Employee failed to timely report/apply"],
        "remedies": ["Reinstatement to escalator position", "Back pay and benefits", "Liquidated damages for willful violations", "Attorneys fees", "No damages cap"],
        "leading_cases": ["Staub v. Proctor Hospital, 562 U.S. 411 (2011)", "Fishgold v. Sullivan Drydock & Repair Corp., 328 U.S. 275 (1946)", "Coffy v. Republic Steel Corp., 447 U.S. 191 (1980)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["userra", "military", "reemployment", "service_member", "escalator_principle"],
    },

    # ============================================================================
    # WORKPLACE PRIVACY
    # ============================================================================

    "employee_privacy": {
        "topic": "employee_privacy",
        "title": "Employee Privacy Rights in the Workplace",
        "category": "general_employment",
        "summary": "Employee workplace privacy is governed by a patchwork of federal and state laws. Key areas: (1) Electronic monitoring - ECPA (18 U.S.C. 2510) permits employer monitoring of business communications with prior notice or business extension exception. State laws (CA, CT, DE, NY) may require additional notice. (2) Drug testing - Fourth Amendment applies only to public employers. Private sector largely governed by state law. ADA limits disability-related inquiries but post-offer drug testing is permitted. (3) Background checks - FCRA requires disclosure and authorization for consumer reports used in employment. Ban-the-box laws in many jurisdictions. (4) Social media - many states prohibit employers from requiring access to personal social media accounts. NLRA protects concerted activity on social media. (5) Biometric data - BIPA (Illinois) and similar state laws require consent for collection. (6) Medical information - ADA confidentiality requirements, HIPAA (through group health plans).",
        "key_statutes": ["18 U.S.C. 2510-2522 (ECPA)", "15 U.S.C. 1681 (FCRA)", "42 U.S.C. 12112(d) (ADA medical inquiries)", "740 ILCS 14 (Illinois BIPA)", "State-specific privacy statutes"],
        "elements": ["Reasonable expectation of privacy", "Employer intrusion into private affairs", "Intrusion highly offensive to reasonable person (tort claims)"],
        "defenses": ["Legitimate business reason", "Employee consent", "Business extension exception (ECPA)", "Public safety concern", "Compliance with law"],
        "remedies": ["Statutory damages (ECPA, FCRA, BIPA)", "Actual damages", "Injunctive relief", "Attorneys fees", "BIPA: $1,000 per negligent violation, $5,000 per willful violation"],
        "leading_cases": ["City of Ontario v. Quon, 560 U.S. 746 (2010)", "Spokeo, Inc. v. Robins, 578 U.S. 330 (2016)", "Calhoun v. Google LLC, 2024 WL 137856 (N.D. Cal. 2024)"],
        "confidence": 0.85,
        "last_updated": "2026-01-15",
        "tags": ["privacy", "monitoring", "drug_testing", "background_check", "social_media", "bipa"],
    },

    # ============================================================================
    # EXECUTIVE COMPENSATION & SEVERANCE
    # ============================================================================

    "severance_agreements": {
        "topic": "severance_agreements",
        "title": "Severance Agreement Negotiation and Enforceability",
        "category": "general_employment",
        "summary": "Severance agreements are contracts providing compensation in exchange for a release of claims. Key enforceability requirements: (1) adequate consideration (something beyond what employee is already owed), (2) knowing and voluntary waiver, (3) OWBPA compliance for ADEA waivers (21-day consideration period for individuals, 45 days for group, 7-day revocation period, written in plain language, specific reference to ADEA rights, advice to consult attorney, demographic disclosure for group waivers). Common provisions: general release, confidentiality, non-disparagement, non-compete/non-solicitation, cooperation, return of property, payment terms. Unenforceable provisions: release of future claims, release of non-waivable rights (FLSA, workers comp in some states), unconscionable terms. NLRB has challenged broad confidentiality and non-disparagement provisions as violating Section 7 (McLaren Macomb, 2023). Tax considerations: severance generally taxable as ordinary income, structured payments may reduce tax impact.",
        "key_statutes": ["29 U.S.C. 626(f) (OWBPA waiver requirements)", "29 C.F.R. 1625.22 (EEOC waiver regulations)", "IRC 409A (deferred compensation rules)", "McLaren Macomb, 372 NLRB No. 58 (2023)"],
        "elements": ["Offer and acceptance", "Adequate consideration", "Knowing and voluntary execution", "OWBPA compliance (if ADEA release)", "No coercion or fraud"],
        "defenses": ["Knowing and voluntary waiver", "Adequate consideration provided", "OWBPA fully complied with", "Employee had opportunity to consult attorney", "Plain language and specific statutory references"],
        "remedies": ["If invalid: underlying claims may proceed", "Contract damages if employer breaches", "Rescission for fraud or duress", "Recovery of consideration already paid (employers defense)"],
        "leading_cases": ["Oubre v. Entergy Operations, 522 U.S. 422 (1998)", "Skrbina v. Fleming Companies, 45 F.3d 1449 (10th Cir. 1995)", "McLaren Macomb, 372 NLRB No. 58 (2023)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["severance", "release", "owbpa", "separation_agreement", "waiver", "mclaren_macomb"],
    },

    # ============================================================================
    # EMPLOYER RECORD-KEEPING
    # ============================================================================

    "employer_recordkeeping": {
        "topic": "employer_recordkeeping",
        "title": "Employer Recordkeeping Requirements",
        "category": "compliance",
        "summary": "Federal employment laws impose extensive recordkeeping requirements. FLSA: payroll records for 3 years (name, address, DOB if under 19, sex, occupation, hours worked, regular rate, overtime earnings, deductions, pay dates, pay periods). Title VII/ADA/ADEA/GINA: employment records for 1 year from making or action (personnel, application, hiring, demotion, transfer, layoff, termination, rates of pay, selection for training). FMLA: 3 years (leave records, policies, premium payments, disputes). OSHA: 5 years for injury/illness logs (OSHA 300/300A/301), 30 years for medical/exposure records. I-9 forms: 3 years from hire or 1 year after separation (whichever is later). EEO-1 reports: retain most recent plus previous year. ERISA: 6 years for plan documents. Failure to maintain records creates adverse inference in litigation and may result in penalties.",
        "key_statutes": ["29 C.F.R. 516 (FLSA records)", "29 C.F.R. 1602 (EEO records)", "29 C.F.R. 825.500 (FMLA records)", "29 C.F.R. 1904 (OSHA records)", "8 C.F.R. 274a.2 (I-9 records)", "29 U.S.C. 1027 (ERISA records)"],
        "elements": ["Covered employer", "Records required by applicable statute", "Failure to create or maintain required records", "Within applicable retention period"],
        "defenses": ["Records were properly maintained", "Statute does not require specific record", "Records destroyed after retention period expired", "Good faith compliance effort"],
        "remedies": ["Adverse inference in litigation", "Statutory penalties (OSHA, FLSA)", "Spoliation sanctions", "Shift of burden of proof to employer", "OSHA penalties for recordkeeping violations"],
        "leading_cases": ["Anderson v. Mt. Clemens Pottery Co., 328 U.S. 680 (1946) (just and reasonable inference)", "Donovan v. New Floridian Hotel, 676 F.2d 468 (11th Cir. 1982)"],
        "confidence": 0.88,
        "last_updated": "2026-01-15",
        "tags": ["recordkeeping", "compliance", "retention", "flsa_records", "osha_records", "i9"],
    },

    # ============================================================================
    # EMPLOYMENT CLASS ACTIONS
    # ============================================================================

    "employment_class_actions": {
        "topic": "employment_class_actions",
        "title": "Employment Class and Collective Actions",
        "category": "litigation",
        "summary": "Employment claims may be brought as class actions (Rule 23) or collective actions (FLSA 216(b)). FLSA collective actions: opt-in mechanism, conditionally certified at early stage, decertified at later stage if common issues do not predominate. Title VII class actions: Rule 23 requirements (numerosity, commonality, typicality, adequacy). Wal-Mart v. Dukes (2011) tightened commonality standard for discrimination class actions - must show common question with common answer. Pattern-or-practice claims typically require statistical evidence of discrimination plus anecdotal evidence. PAGA (California) allows representative actions for Labor Code violations with state-share of penalties. Arbitration class waivers enforceable under Epic Systems. Settlement class actions require court approval, notice to class, and fairness hearing.",
        "key_statutes": ["Fed. R. Civ. P. 23 (class actions)", "29 U.S.C. 216(b) (FLSA collective actions)", "Cal. Lab. Code 2698-2699.8 (PAGA)", "28 U.S.C. 1715 (CAFA notice)"],
        "elements": ["Numerosity (Rule 23(a)(1))", "Commonality - common question with common answer (Rule 23(a)(2))", "Typicality (Rule 23(a)(3))", "Adequacy of representation (Rule 23(a)(4))", "For FLSA: similarly situated employees"],
        "defenses": ["Class action waiver in arbitration agreement", "Lack of commonality", "Individual issues predominate", "Named plaintiff atypical", "Inadequate representation", "Manageability concerns"],
        "remedies": ["Individual damages for class members", "Injunctive relief (Rule 23(b)(2))", "PAGA penalties (75% to state)", "Attorneys fees and costs", "Equitable relief"],
        "leading_cases": ["Wal-Mart Stores v. Dukes, 564 U.S. 338 (2011)", "Genesis Healthcare Corp. v. Symczyk, 569 U.S. 66 (2013)", "Hoffmann-La Roche v. Sperling, 493 U.S. 165 (1989)", "Tyson Foods v. Bouaphakeo, 577 U.S. 442 (2016)"],
        "confidence": 0.89,
        "last_updated": "2026-01-15",
        "tags": ["class_action", "collective_action", "rule_23", "flsa_216b", "paga", "dukes"],
    },

    # ============================================================================
    # INDEPENDENT CONTRACTOR / GIG ECONOMY
    # ============================================================================

    "gig_economy_classification": {
        "topic": "gig_economy_classification",
        "title": "Gig Economy and Platform Worker Classification",
        "category": "flsa",
        "summary": "The classification of gig and platform workers (Uber, Lyft, DoorDash, etc.) remains heavily contested. The DOL 2024 final rule restored the economic reality test with six factors (no single factor dispositive): (1) opportunity for profit or loss depending on managerial skill, (2) investments by the worker and the potential employer, (3) degree of permanence of work relationship, (4) nature and degree of control, (5) extent work is integral part of employers business, (6) skill and initiative. California AB5 codified the ABC test: worker is employee unless (A) free from control and direction, (B) performs work outside usual course of hiring entitys business, (C) customarily engaged in independently established trade. Proposition 22 carved out app-based drivers. State DOL enforcement actions and private lawsuits ongoing nationwide. Joint employer doctrine may extend liability to platform companies even if direct employment relationship is disputed.",
        "key_statutes": ["29 C.F.R. Part 795 (DOL 2024 rule)", "Cal. Lab. Code 2775 (AB5/ABC test)", "Cal. Bus. & Prof. Code 7451 (Prop 22)", "State-specific independent contractor statutes"],
        "elements": ["Worker performs services for putative employer", "Putative employer exercises control or right to control", "Economic reality factors weigh toward employment", "Worker is economically dependent on employer"],
        "defenses": ["Worker is genuinely independent (own business, multiple clients)", "Written independent contractor agreement (not dispositive)", "ABC test B prong (work outside usual course of business)", "Industry practice", "Section 530 safe harbor (IRS)"],
        "remedies": ["Reclassification as employee", "Back wages and overtime", "Benefits enrollment", "Tax liability (employer share FICA/FUTA)", "State unemployment insurance liability", "Class/collective action damages"],
        "leading_cases": ["Dynamex Operations West v. Superior Court, 4 Cal. 5th 903 (2018)", "National Federation of Independent Business v. DOL (pending)", "Lawson v. Grubhub, 13 F.4th 908 (9th Cir. 2021)"],
        "confidence": 0.87,
        "last_updated": "2026-01-15",
        "tags": ["gig_economy", "platform_worker", "abc_test", "economic_reality", "ab5", "classification"],
    },

    # ============================================================================
    # IMMIGRATION AND EMPLOYMENT
    # ============================================================================

    "immigration_employment": {
        "topic": "immigration_employment",
        "title": "Immigration-Related Employment Practices (IRCA)",
        "category": "general_employment",
        "summary": "The Immigration Reform and Control Act (IRCA) prohibits: (1) hiring unauthorized workers (employer sanctions), (2) document abuse (requiring specific documents for I-9 verification), (3) citizenship/immigration status discrimination in hiring, firing, or recruitment (enforced by DOJ Immigrant and Employee Rights Section, not EEOC). I-9 compliance requires verification of identity and work authorization within 3 business days of hire. E-Verify is mandatory for federal contractors and in some states. Anti-discrimination provisions apply to employers with 4-14 employees (15+ covered by Title VII national origin). Penalties: civil fines for I-9 violations ($252-$2,507 per I-9 for paperwork violations, $698-$27,894 per unauthorized worker for substantive violations). Worksite enforcement actions (ICE audits) require Notice of Inspection. Employers cannot use immigration status to retaliate against employees who assert labor rights.",
        "key_statutes": ["8 U.S.C. 1324a (employer sanctions)", "8 U.S.C. 1324b (anti-discrimination)", "INA 274A, 274B", "8 C.F.R. 274a (I-9 regulations)", "Executive Order 12989 (E-Verify for federal contractors)"],
        "elements": ["Employment relationship", "Knowing hire of unauthorized worker OR failure to complete I-9 OR discrimination based on citizenship/immigration status"],
        "defenses": ["Good faith compliance with I-9 requirements", "Employee presented facially valid documents", "Technical/procedural I-9 violation (correction opportunity)", "Safe harbor (proper I-9 completion)"],
        "remedies": ["Civil monetary penalties", "Debarment from government contracts", "Criminal penalties for pattern or practice", "Back pay and reinstatement (discrimination)", "Cease and desist orders"],
        "leading_cases": ["Hoffman Plastic Compounds v. NLRB, 535 U.S. 137 (2002) (limited back pay for unauthorized workers)", "EEOC v. Aqua Chemical, No. 10-cv-5765 (N.D. Ill. 2011)"],
        "confidence": 0.87,
        "last_updated": "2026-01-15",
        "tags": ["immigration", "irca", "i9", "e_verify", "unauthorized_worker", "document_abuse"],
    },

    # ============================================================================
    # EMPLOYMENT PRACTICES LIABILITY
    # ============================================================================

    "epli_insurance": {
        "topic": "epli_insurance",
        "title": "Employment Practices Liability Insurance (EPLI)",
        "category": "compliance",
        "summary": "EPLI provides coverage for claims arising from employment-related practices including wrongful termination, discrimination, sexual harassment, retaliation, breach of employment contract, negligent evaluation, failure to promote, wrongful discipline, deprivation of career opportunity, mismanagement of employee benefit plans, and wage and hour violations (often sublimited or excluded). Standard exclusions: intentional/criminal acts, punitive damages (in some states), prior known claims, ERISA benefits, WARN Act, OSHA penalties, workers compensation, unemployment insurance, COBRA, NLRA proceedings. Key coverage considerations: defense costs (duty to defend vs. duty to reimburse), retention/deductible levels, sublimits for wage and hour, consent-to-settle clauses, third-party coverage (customer/vendor claims), and prior acts coverage. EPLI is critical for risk management but does not replace employment law compliance.",
        "key_statutes": ["State insurance regulations", "Policy-specific terms and conditions"],
        "elements": ["Covered employment practice", "Claim made during policy period", "Notice to insurer within policy terms", "No applicable exclusion"],
        "defenses": ["Policy exclusion applies", "Late notice", "Intentional act exclusion", "Prior knowledge exclusion", "Claim outside policy period"],
        "remedies": ["Defense costs coverage", "Indemnity for settlements and judgments", "Mediation/arbitration funding"],
        "leading_cases": ["Policy interpretation governed by state contract law", "Chubb Custom Insurance v. Space Systems/Loral (coverage dispute precedent)"],
        "confidence": 0.83,
        "last_updated": "2026-01-15",
        "tags": ["epli", "insurance", "risk_management", "coverage", "defense_costs"],
    },

    # ============================================================================
    # PAY TRANSPARENCY AND EQUITY
    # ============================================================================

    "pay_transparency": {
        "topic": "pay_transparency",
        "title": "Pay Transparency Laws and Pay Equity",
        "category": "compliance",
        "summary": "A growing number of states and localities have enacted pay transparency laws requiring employers to disclose salary ranges in job postings or upon request. Colorado (2021), Washington, California, New York (effective 2023-2024) require salary ranges in job postings. Many states prohibit salary history inquiries (California, New York, Massachusetts, Illinois, and others). The Paycheck Fairness Act (proposed federal legislation) would strengthen EPA by limiting factor other than sex defense. State pay equity laws may impose stricter standards than the federal EPA - for example, requiring equal pay for substantially similar work (broader than equal work) and limiting acceptable pay differentials to bona fide factors such as education, training, or experience. Employers should conduct privileged pay equity audits, document legitimate pay factors, and update compensation structures proactively.",
        "key_statutes": ["Colo. Rev. Stat. 8-5-201 (Equal Pay Transparency)", "Cal. Lab. Code 432.3 (salary history ban)", "N.Y. Lab. Law 194-b (pay transparency)", "Mass. G.L. c. 149 156 (pay equity)", "State-specific pay transparency statutes"],
        "elements": ["Covered employer in applicable jurisdiction", "Job posting or position subject to transparency requirement", "Failure to include salary range or disclose upon request"],
        "defenses": ["Not a covered employer", "Position exempt from disclosure", "Good faith compliance effort", "Range disclosed upon request (where posting not required)"],
        "remedies": ["Civil penalties per violation", "Private right of action (some states)", "Injunctive relief", "Attorneys fees"],
        "leading_cases": ["State enforcement actions and administrative guidance predominate (evolving area)"],
        "confidence": 0.82,
        "last_updated": "2026-01-15",
        "tags": ["pay_transparency", "salary_range", "pay_equity", "salary_history_ban", "compensation"],
    },

    # ============================================================================
    # JOINT EMPLOYER LIABILITY
    # ============================================================================

    "joint_employer": {
        "topic": "joint_employer",
        "title": "Joint Employer Liability",
        "category": "general_employment",
        "summary": "Joint employer doctrine imposes employment law liability on entities that share or co-determine essential terms and conditions of employment. The DOL 2024 FLSA joint employer rule uses the economic reality test: an entity is a joint employer if it exercises significant control over the terms and conditions of the workers employment. The NLRB uses a broader standard examining reserved and indirect control. Key factors: power to hire/fire, supervision and control of work schedules, determination of rate and method of payment, and maintenance of employment records. Common contexts: staffing agencies and client companies, franchisors and franchisees, parent companies and subsidiaries, general contractors and subcontractors. Courts apply different tests depending on the statute (FLSA, Title VII, NLRA have different frameworks). Browning-Ferris Industries (2015 NLRB decision) expanded joint employer to include indirect and reserved control, partially codified in 2023 NLRB rule (vacated in 2024). The analysis remains fact-intensive and circuit-dependent.",
        "key_statutes": ["29 C.F.R. 791.2 (FLSA joint employer)", "NLRB Joint Employer Rule (2023, vacated 2024)", "29 U.S.C. 203(d) (FLSA employer definition)", "State-specific joint employer standards"],
        "elements": ["Two or more entities benefiting from workers labor", "Entities share or co-determine material terms of employment", "Worker is economically dependent on or controlled by both entities", "Under applicable test (economic reality, common law, or hybrid)"],
        "defenses": ["No control over employment terms", "Arms-length business relationship", "Independent contractor relationship with intermediary", "Franchise agreement does not confer employment control", "Corporate separateness maintained"],
        "remedies": ["Joint and several liability for wage/hour violations", "Joint liability for discrimination claims", "Expanded bargaining obligations (NLRA)", "Aggregate employee counts for statutory coverage"],
        "leading_cases": ["Browning-Ferris Industries of California, 362 NLRB No. 186 (2015)", "Zheng v. Liberty Apparel Co., 355 F.3d 61 (2d Cir. 2003)", "NLRB v. CNN America, Inc., 865 F.3d 740 (D.C. Cir. 2017)"],
        "confidence": 0.86,
        "last_updated": "2026-01-15",
        "tags": ["joint_employer", "staffing", "franchisor", "shared_control", "browning_ferris"],
    },

    # ============================================================================
    # WORKPLACE VIOLENCE PREVENTION
    # ============================================================================

    "workplace_violence": {
        "topic": "workplace_violence",
        "title": "Workplace Violence Prevention and Employer Liability",
        "category": "osha",
        "summary": "Employers have a duty to maintain a safe workplace under OSHA General Duty Clause, which extends to preventing workplace violence when the employer knows or should know of a recognized hazard. OSHA has issued specific standards for healthcare (29 C.F.R. 1910.1030) and enforcement guidance for all industries. California SB 553 (effective July 2024) requires written workplace violence prevention plans for nearly all employers. Key employer obligations: (1) risk assessment for workplace violence, (2) written prevention policy, (3) training for managers and employees, (4) incident response procedures, (5) post-incident support. Employer liability theories: negligent hiring (failure to screen), negligent retention (failure to act on warning signs), negligent supervision, premises liability, workers compensation (exclusive remedy for physical injuries). Domestic violence spillover into the workplace is increasingly recognized as an employer concern requiring accommodation and safety planning.",
        "key_statutes": ["29 U.S.C. 654(a)(1) (OSHA General Duty Clause)", "Cal. Lab. Code 6401.7 (IIPP)", "Cal. Lab. Code 6401.9 (SB 553 Workplace Violence Prevention)", "29 C.F.R. 1910.1030 (healthcare)"],
        "elements": ["Known or foreseeable risk of violence", "Employer failure to take reasonable preventive measures", "Physical or psychological injury", "Employer control over workplace conditions"],
        "defenses": ["No known or foreseeable risk", "Reasonable prevention measures taken", "Unforeseeable criminal act of third party", "Workers comp exclusive remedy (for injury claims)", "Independent contractor performed the harm"],
        "remedies": ["Workers comp benefits (exclusive for physical injury in most states)", "Tort damages if exclusive remedy exception applies", "OSHA citations and penalties", "Injunctive relief (restraining orders)", "State penalties for non-compliance with prevention requirements"],
        "leading_cases": ["OSHA enforcement actions and state regulatory guidance predominate", "Cal/OSHA enforcement of SB 553"],
        "confidence": 0.83,
        "last_updated": "2026-01-15",
        "tags": ["workplace_violence", "osha", "prevention_plan", "negligent_hiring", "duty_of_care"],
    },

    # ============================================================================
    # EMPLOYEE HANDBOOK POLICIES
    # ============================================================================

    "employee_handbook": {
        "topic": "employee_handbook",
        "title": "Employee Handbook Best Practices and Legal Risks",
        "category": "compliance",
        "summary": "Employee handbooks serve as critical compliance tools and potential legal evidence. Key required/recommended policies: at-will disclaimer (conspicuous, signed acknowledgment), EEO/anti-discrimination, anti-harassment (complaint procedure), FMLA (if applicable), ADA reasonable accommodation, wage and hour (pay practices, overtime), attendance and leave, social media and electronic communications, drug and alcohol, workplace safety, confidentiality, conflicts of interest, progressive discipline (with disclaimer that it does not create contract), complaint and grievance procedures. Legal risks: implied contract claims (handbook creates binding promise absent clear disclaimer), NLRA Section 7 issues (overly broad confidentiality, social media, non-disparagement policies per McLaren Macomb), inconsistent enforcement (disparate treatment evidence), outdated policies (failure to update for new laws). Best practices: annual review, legal counsel review, signed acknowledgments, electronic distribution with tracking, consistent enforcement.",
        "key_statutes": ["State-specific implied contract law", "29 U.S.C. 157-158 (NLRA Section 7/8 - handbook rules)", "McLaren Macomb, 372 NLRB No. 58 (2023)", "EEOC Enforcement Guidance"],
        "elements": ["Handbook provision constitutes offer", "Employee acceptance through continued employment", "Employer failed to include effective at-will disclaimer", "Employee relied on handbook promise to their detriment"],
        "defenses": ["Clear and conspicuous at-will disclaimer", "Signed acknowledgment of at-will status", "Disclaimer that handbook does not create contract", "Reservation of right to modify at any time", "Consistent application of policies"],
        "remedies": ["Contract damages (if implied contract found)", "Reinstatement", "Back pay", "Attorneys fees"],
        "leading_cases": ["Toussaint v. Blue Cross, 408 Mich. 579 (1980)", "Woolley v. Hoffmann-La Roche, 99 N.J. 284 (1985)", "McLaren Macomb, 372 NLRB No. 58 (2023)", "Demasse v. ITT Corp., 984 P.2d 1138 (Ariz. 1999)"],
        "confidence": 0.87,
        "last_updated": "2026-01-15",
        "tags": ["handbook", "at_will_disclaimer", "implied_contract", "policy", "compliance", "mclaren_macomb"],
    },

    # ============================================================================
    # RELIGIOUS ACCOMMODATION
    # ============================================================================

    "religious_accommodation": {
        "topic": "religious_accommodation",
        "title": "Religious Accommodation Under Title VII",
        "category": "title_vii",
        "summary": "Title VII requires employers to reasonably accommodate employees sincerely held religious beliefs, observances, and practices unless doing so would cause undue hardship. The Supreme Court in Groff v. DeJoy (2023) significantly strengthened religious accommodation by overruling the de minimis standard from TWA v. Hardison (1977). Under Groff, undue hardship now means substantial increased costs in relation to the conduct of the employers particular business - a much higher threshold than the prior de minimis standard. Religious beliefs need not be part of an organized religion; they must be sincerely held and religious in nature. Employers should engage in an interactive process similar to ADA. Common accommodations: schedule changes, shift swaps, dress code modifications, exemptions from union dues. An employer cannot deny accommodation based on co-worker preferences or customer preferences.",
        "key_statutes": ["42 U.S.C. 2000e(j) (religious accommodation definition)", "42 U.S.C. 2000e-2(a)(1)", "29 C.F.R. 1605 (EEOC guidelines on religious discrimination)"],
        "elements": ["Sincerely held religious belief", "Belief conflicts with employment requirement", "Employee notified employer of conflict", "Employer failed to accommodate or retaliated"],
        "defenses": ["Undue hardship (substantial increased costs per Groff)", "Belief not sincerely held", "Employee did not provide notice of need", "Accommodation provided but employee rejected it", "Direct threat to safety"],
        "remedies": ["Same as Title VII: compensatory damages (capped), punitive damages (capped), back pay, reinstatement, attorneys fees, injunctive relief"],
        "leading_cases": ["Groff v. DeJoy, 600 U.S. 447 (2023)", "TWA v. Hardison, 432 U.S. 63 (1977) (overruled in part by Groff)", "EEOC v. Abercrombie & Fitch Stores, 575 U.S. 768 (2015)", "Heller v. EBB Auto Co., 8 F.3d 1433 (9th Cir. 1993)"],
        "confidence": 0.93,
        "last_updated": "2026-01-15",
        "tags": ["religious_accommodation", "title_vii", "groff", "sincerely_held_belief", "undue_hardship"],
    },

    # ============================================================================
    # COBRA CONTINUATION COVERAGE
    # ============================================================================

    "cobra_coverage": {
        "topic": "cobra_coverage",
        "title": "COBRA Health Insurance Continuation",
        "category": "erisa",
        "summary": "COBRA (Consolidated Omnibus Budget Reconciliation Act) requires employers with 20+ employees to offer continuation of group health insurance to qualified beneficiaries after qualifying events. Qualifying events for employees: termination (other than gross misconduct) and reduction in hours. Qualifying events for dependents additionally include: employee death, divorce/legal separation, employee becoming Medicare-eligible, and dependent child aging out. Duration: 18 months for termination/reduction in hours (29 months if disabled), 36 months for other qualifying events. Employer must provide initial COBRA notice when employee first covered and election notice within 14 days of qualifying event. Qualified beneficiary has 60 days to elect and 45 days to make first premium payment. Premium: up to 102% of total cost (employer + employee share). Employer failures: $110/day penalty per affected individual, excise tax, ERISA breach of fiduciary duty, and potential personal liability for plan administrators.",
        "key_statutes": ["29 U.S.C. 1161-1169 (ERISA Part 6 - COBRA)", "26 U.S.C. 4980B (excise tax for noncompliance)", "29 C.F.R. 2590.606 (DOL COBRA regulations)", "State mini-COBRA laws (for employers under 20)"],
        "elements": ["Covered employer (20+ employees)", "Qualifying event occurred", "Qualified beneficiary status", "Timely election within 60 days", "Premium payment within grace period"],
        "defenses": ["Employer has fewer than 20 employees", "Termination was for gross misconduct", "Qualified beneficiary failed to timely elect", "Qualified beneficiary obtained other coverage", "Premium payment not timely made"],
        "remedies": ["$110/day statutory penalty per affected individual", "Excise tax under IRC 4980B", "Plan benefits (court may order coverage)", "Attorneys fees in courts discretion", "Equitable relief under ERISA 502(a)(3)"],
        "leading_cases": ["Geissal v. Moore Medical Corp., 524 U.S. 74 (1998)", "National Companies Health Benefit Plan v. St. Joseph's Hospital, 929 F.2d 1558 (11th Cir. 1991)"],
        "confidence": 0.89,
        "last_updated": "2026-01-15",
        "tags": ["cobra", "health_insurance", "continuation", "qualifying_event", "erisa"],
    },

    # ============================================================================
    # NEGLIGENT HIRING AND RETENTION
    # ============================================================================

    "negligent_hiring_retention": {
        "topic": "negligent_hiring_retention",
        "title": "Negligent Hiring, Retention, and Supervision",
        "category": "termination",
        "summary": "Employers may be directly liable under tort theories for negligently hiring, retaining, or supervising employees who harm third parties or co-workers. Negligent hiring: employer failed to exercise reasonable care in selecting employee, and the employees unfitness was foreseeable through reasonable investigation (background check, reference check, license verification). Negligent retention: employer knew or should have known employee posed a risk and failed to take appropriate action (termination, reassignment, additional supervision). Negligent supervision: employer failed to adequately monitor or control employee conduct. These claims exist independently from respondeat superior (vicarious liability) and can establish independent employer fault. Important considerations: FCRA compliance for background checks, ban-the-box laws limiting inquiry timing, ADA restrictions on medical inquiries, and state laws governing negligence standards. Texas recognizes all three theories under common law tort.",
        "key_statutes": ["State common law tort principles (Restatement (Second) of Torts 317, 413)", "15 U.S.C. 1681 (FCRA for background checks)", "State-specific negligent hiring standards"],
        "elements": ["Employer knew or should have known of employees unfitness", "Employees unfitness created foreseeable risk of harm", "Employers negligence was proximate cause of injury", "Damages resulted"],
        "defenses": ["Reasonable investigation conducted", "No information suggesting unfitness", "Unforeseeable criminal act", "Workers comp exclusive remedy (for co-worker claims in some states)", "FCRA-compliant background check revealed nothing"],
        "remedies": ["Compensatory damages (actual harm)", "Punitive damages (for egregious conduct)", "No statutory cap (common law tort)", "Attorneys fees (in some jurisdictions)"],
        "leading_cases": ["Doe v. Garcia, 961 P.2d 1181 (Idaho 1998)", "Ponticas v. K.M.S. Investments, 331 N.W.2d 907 (Minn. 1983)", "Hiring/retention cases vary significantly by state"],
        "confidence": 0.86,
        "last_updated": "2026-01-15",
        "tags": ["negligent_hiring", "negligent_retention", "background_check", "employer_tort", "foreseeability"],
    },

    # ============================================================================
    # UNEMPLOYMENT INSURANCE
    # ============================================================================

    "unemployment_insurance": {
        "topic": "unemployment_insurance",
        "title": "Unemployment Insurance Benefits and Employer Obligations",
        "category": "general_employment",
        "summary": "Unemployment insurance (UI) is a joint federal-state program providing temporary income to workers who lose employment through no fault of their own. Federal framework: Federal Unemployment Tax Act (FUTA) imposes 6.0% tax on first $7,000 of wages (5.4% credit for state tax compliance, yielding 0.6% net). States administer benefits with varying eligibility, benefit amounts, and duration. Texas UI: maximum $577/week, up to 26 weeks. Eligibility: (1) unemployed through no fault of own (not for cause), (2) able and available to work, (3) actively seeking employment, (4) meet base period wage requirements. Disqualification: voluntary quit without good cause, discharge for misconduct connected with work (not mere unsatisfactory performance), refusal of suitable work, fraud. Employer responsibilities: SUTA tax, quarterly wage reporting, timely response to claims, participation in hearings. Employer experience rating affects tax rate. Independent contractors not eligible. Misclassification exposure: employer liable for back UI taxes.",
        "key_statutes": ["26 U.S.C. 3301-3311 (FUTA)", "Tex. Lab. Code Ch. 201-214 (Texas Unemployment Compensation Act)", "State-specific unemployment insurance statutes"],
        "elements": ["Former employee filed UI claim", "Separation from employment", "Claimant meets eligibility requirements (wages, availability, job search)", "Separation was not disqualifying (misconduct, voluntary quit)"],
        "defenses": ["Discharge for misconduct connected with work", "Voluntary quit without good cause attributable to employer", "Claimant not able and available", "Claimant refused suitable work", "Claimant does not meet wage requirements"],
        "remedies": ["Weekly UI benefits (state-determined amount and duration)", "Employer tax rate adjustment (experience rating)", "Employer penalties for misclassification", "Fraud overpayment recovery from claimant"],
        "leading_cases": ["State administrative law decisions predominate", "TWC precedent decisions (Texas)"],
        "confidence": 0.85,
        "last_updated": "2026-01-15",
        "tags": ["unemployment", "ui_benefits", "futa", "suta", "misconduct", "voluntary_quit"],
    },

    # ============================================================================
    # DRUG TESTING IN EMPLOYMENT
    # ============================================================================

    "drug_testing": {
        "topic": "drug_testing",
        "title": "Drug and Alcohol Testing in Employment",
        "category": "general_employment",
        "summary": "Drug and alcohol testing in employment is governed primarily by state law (for private employers) and federal regulations (for safety-sensitive positions). Federal requirements: DOT drug and alcohol testing (49 C.F.R. Part 40) mandates testing for commercial drivers, pilots, transit operators, and other safety-sensitive positions (pre-employment, random, post-accident, reasonable suspicion, return-to-duty, follow-up). Drug-Free Workplace Act (41 U.S.C. 8101) requires federal contractors/grantees to maintain drug-free workplace policies. ADA limits: current illegal drug use not protected disability, but employer cannot discriminate against employee in recovery or on prescribed medication. Marijuana: despite state legalization, federal contractors and DOT-regulated employers must comply with federal standards. Many states (California, New York, New Jersey, and others) now restrict testing for marijuana metabolites for non-safety-sensitive positions. Texas allows drug testing with few restrictions for private employers.",
        "key_statutes": ["49 C.F.R. Part 40 (DOT testing procedures)", "41 U.S.C. 8101-8106 (Drug-Free Workplace Act)", "42 U.S.C. 12114 (ADA drug/alcohol provisions)", "State-specific drug testing laws", "Tex. Lab. Code 21.051 (not specifically addressing drug testing)"],
        "elements": ["Employment relationship", "Drug or alcohol test administered", "Adverse action based on test results", "Test not conducted in accordance with applicable law or policy"],
        "defenses": ["Safety-sensitive position justification", "Federal regulation requirement (DOT)", "Policy clearly communicated to employees", "Proper chain of custody and testing procedures", "Positive test confirmed by MRO (Medical Review Officer)", "State law permits testing"],
        "remedies": ["Reinstatement (if wrongful termination)", "Back pay", "Disability discrimination damages (if ADA violation)", "State-specific penalties", "Invasion of privacy damages (if applicable)"],
        "leading_cases": ["Skinner v. Railway Labor Executives Assn., 489 U.S. 602 (1989) (public employer)", "National Treasury Employees Union v. Von Raab, 489 U.S. 656 (1989)", "State-specific cases for private employer testing"],
        "confidence": 0.84,
        "last_updated": "2026-01-15",
        "tags": ["drug_testing", "dot_testing", "marijuana", "ada_substance", "drug_free_workplace"],
    },

    # ============================================================================
    # TITLE IX AND EDUCATIONAL EMPLOYMENT
    # ============================================================================

    "title_ix_employment": {
        "topic": "title_ix_employment",
        "title": "Title IX Employment Protections in Educational Institutions",
        "category": "discrimination",
        "summary": "Title IX of the Education Amendments of 1972 (20 U.S.C. 1681-1688) prohibits sex discrimination in education programs receiving federal financial assistance, including employment discrimination. Title IX covers hiring, promotion, compensation, and termination decisions in educational institutions. The statute provides an independent cause of action for employment discrimination separate from Title VII, with potential advantages: no administrative exhaustion requirement (no EEOC filing needed), no damages cap, and broader definition of 'employer' (covers institutions with as few as one employee receiving federal funds). However, after the Supreme Court's decision in Jackson v. Birmingham Board of Education, 544 U.S. 167 (2005), Title IX also protects against retaliation for complaining about sex discrimination. Key overlap with Title VII: when both statutes apply, courts are split on whether Title IX provides an implied private right of action for employment claims post-Fitzgerald v. Barnstable School Committee, 555 U.S. 246 (2009). Recent developments include expanded coverage of gender identity and sexual orientation discrimination under Title IX regulations (2024 amendments). Remedies include injunctive relief, compensatory damages, and potentially punitive damages under some circuit interpretations.",
        "key_statutes": ["20 U.S.C. 1681-1688 (Title IX)", "34 C.F.R. Part 106 (Title IX regulations)", "42 U.S.C. 2000e et seq. (Title VII overlap)", "20 U.S.C. 1687 (program or activity definition)"],
        "elements": ["Plaintiff is employee of educational institution", "Institution receives federal financial assistance", "Adverse employment action based on sex", "Causal connection between sex and adverse action"],
        "defenses": ["Legitimate non-discriminatory reason (pretext analysis)", "BFOQ (narrow in educational context)", "Religious organization exemption (20 U.S.C. 1681(a)(3))", "Military training exemption", "Action based on non-sex factors", "Title VII preemption argument (circuit split)"],
        "remedies": ["Injunctive relief (reinstatement, policy changes)", "Compensatory damages (no cap unlike Title VII)", "Back pay and front pay", "Attorneys fees (42 U.S.C. 1988 via Spending Clause theory)", "Potential loss of federal funding (rarely invoked)"],
        "leading_cases": ["North Haven Board of Education v. Bell, 456 U.S. 512 (1982) (Title IX covers employment)", "Jackson v. Birmingham Board of Education, 544 U.S. 167 (2005) (retaliation covered)", "Fitzgerald v. Barnstable School Committee, 555 U.S. 246 (2009) (Title IX and Section 1983 not mutually exclusive)", "Lakoski v. James, 66 F.3d 751 (5th Cir. 1995) (Title VII precludes Title IX employment claims)", "Preston v. Virginia ex rel. New River Community College, 31 F.3d 203 (4th Cir. 1994)"],
        "confidence": 0.82,
        "last_updated": "2026-01-15",
        "tags": ["title_ix", "education_employment", "sex_discrimination", "federal_funding", "no_exhaustion"],
    },

    # ============================================================================
    # SECTION 1981 RACE DISCRIMINATION
    # ============================================================================

    "section_1981_race": {
        "topic": "section_1981_race",
        "title": "Section 1981 Race Discrimination in Employment",
        "category": "discrimination",
        "summary": "42 U.S.C. Section 1981 guarantees all persons the same right to make and enforce contracts as is enjoyed by white citizens. As amended by the Civil Rights Act of 1991, Section 1981 covers the making, performance, modification, and termination of contracts, and the enjoyment of all benefits, privileges, terms, and conditions of the contractual relationship. Key advantages over Title VII: (1) no administrative exhaustion requirement, (2) no employer size threshold (covers employers with fewer than 15 employees), (3) no damages cap, (4) longer statute of limitations (4 years under 28 U.S.C. 1658), (5) individual liability for supervisors. However, Section 1981 only covers race discrimination (including ethnicity and alienage in some circuits) - it does not cover sex, age, disability, or religion. The burden-shifting framework follows McDonnell Douglas for circumstantial evidence cases. For 1981 claims against state actors, Section 1983 provides the enforcement mechanism (Jett v. Dallas Independent School District, 491 U.S. 701 (1989)). After Comcast Corp. v. National Association of African American-Owned Media, 589 U.S. 327 (2020), plaintiffs must show but-for causation at the pleading stage. Section 1981 is frequently paired with Title VII claims as a parallel cause of action for race discrimination.",
        "key_statutes": ["42 U.S.C. 1981 (equal rights under the law)", "42 U.S.C. 1981a (damages in intentional discrimination cases)", "42 U.S.C. 1983 (enforcement mechanism for state actors)", "28 U.S.C. 1658 (4-year statute of limitations for federal statutes)"],
        "elements": ["Plaintiff is member of a racial minority", "Defendant intended to discriminate on the basis of race", "Discrimination related to making, performing, modifying, or terminating a contract", "But-for causation (post-Comcast)"],
        "defenses": ["Legitimate non-discriminatory reason", "Same-decision defense", "Statute of limitations (4 years)", "No but-for causation (Comcast standard)", "After-acquired evidence (limits remedies)", "Sovereign immunity (for state employers without Section 1983)"],
        "remedies": ["Compensatory damages (no cap)", "Punitive damages (no cap)", "Back pay and front pay", "Equitable relief (reinstatement, injunction)", "Attorneys fees (42 U.S.C. 1988)", "Pre-judgment and post-judgment interest"],
        "leading_cases": ["Comcast Corp. v. National Association of African American-Owned Media, 589 U.S. 327 (2020) (but-for causation required)", "Patterson v. McLean Credit Union, 491 U.S. 164 (1989) (pre-1991 amendments)", "Jones v. R.R. Donnelley & Sons Co., 541 U.S. 369 (2004) (4-year limitations period)", "Jett v. Dallas Independent School District, 491 U.S. 701 (1989) (Section 1983 required for state actors)", "CBOCS West, Inc. v. Humphries, 553 U.S. 442 (2008) (retaliation claims cognizable)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["section_1981", "race_discrimination", "no_cap_damages", "no_exhaustion", "but_for_causation"],
    },

    # ============================================================================
    # PREGNANCY DISCRIMINATION ACT
    # ============================================================================

    "pregnancy_discrimination": {
        "topic": "pregnancy_discrimination",
        "title": "Pregnancy Discrimination Act and Related Protections",
        "category": "discrimination",
        "summary": "The Pregnancy Discrimination Act (PDA), 42 U.S.C. 2000e(k), amended Title VII to prohibit discrimination on the basis of pregnancy, childbirth, or related medical conditions. The PDA requires that pregnant employees be treated the same as other employees similar in their ability or inability to work. The Pregnant Workers Fairness Act (PWFA), effective June 27, 2023 (42 U.S.C. 2000gg et seq.), goes further by requiring covered employers (15+ employees) to provide reasonable accommodations for known limitations related to pregnancy, childbirth, or related medical conditions, unless it causes undue hardship - similar to the ADA framework. Key PWFA provisions: employers cannot require leave if another accommodation is available, cannot deny employment opportunities based on need for accommodation, and cannot retaliate for requesting accommodation. The PUMP Act (Providing Urgent Maternal Protections for Nursing Mothers Act, 2022) expands break time and space protections for nursing employees to virtually all FLSA-covered workers (previously limited to non-exempt). Texas has limited state-level pregnancy protections beyond federal law, but the Texas Commission on Human Rights Act (Chapter 21 of the Texas Labor Code) incorporates Title VII standards including the PDA. Intersectional claims: pregnancy discrimination may overlap with ADA claims (pregnancy-related complications as temporary disabilities), FMLA (pregnancy qualifies as serious health condition), and state workers compensation.",
        "key_statutes": ["42 U.S.C. 2000e(k) (Pregnancy Discrimination Act)", "42 U.S.C. 2000gg et seq. (Pregnant Workers Fairness Act)", "29 U.S.C. 218d (PUMP Act for nursing mothers)", "29 U.S.C. 2612(a)(1)(A) (FMLA for pregnancy)", "Tex. Lab. Code 21.106 (pregnancy discrimination under Texas law)"],
        "elements": ["Employee is pregnant, recently gave birth, or has related medical condition", "Adverse employment action taken", "Pregnancy/related condition was motivating factor (PDA) OR known limitation not accommodated (PWFA)", "Similarly situated non-pregnant employees treated more favorably (PDA) OR accommodation would not cause undue hardship (PWFA)"],
        "defenses": ["Legitimate non-discriminatory reason", "BFOQ (extremely rare for pregnancy)", "Undue hardship (PWFA accommodation claims)", "Employee did not disclose pregnancy/limitation (for accommodation claims)", "Action based on job performance unrelated to pregnancy", "Business necessity for facially neutral policy with disparate impact"],
        "remedies": ["Reinstatement", "Back pay and front pay", "Compensatory damages (Title VII caps apply for PDA via Title VII)", "Punitive damages", "Reasonable accommodation (PWFA)", "Attorneys fees and costs", "Injunctive relief"],
        "leading_cases": ["Young v. United Parcel Service, Inc., 575 U.S. 206 (2015) (PDA burden-shifting for accommodation)", "International Union, UAW v. Johnson Controls, Inc., 499 U.S. 187 (1991) (fetal protection policies = sex discrimination)", "AT&T Corp. v. Hulteen, 556 U.S. 701 (2009) (pre-PDA pension accrual)", "California Federal Savings & Loan Assn. v. Guerra, 479 U.S. 272 (1987) (PDA as floor, not ceiling)"],
        "confidence": 0.91,
        "last_updated": "2026-01-15",
        "tags": ["pregnancy", "pda", "pwfa", "pump_act", "accommodation", "nursing_mothers", "maternity"],
    },

    # ============================================================================
    # EXECUTIVE COMPENSATION AND GOLDEN PARACHUTES
    # ============================================================================

    "executive_compensation": {
        "topic": "executive_compensation",
        "title": "Executive Compensation, Non-Competes, and Golden Parachutes",
        "category": "executive_employment",
        "summary": "Executive compensation law involves a complex intersection of contract law, tax law (IRC Sections 162(m), 280G, 409A), securities law (SEC proxy disclosure, say-on-pay), and ERISA. Key issues: (1) IRC Section 162(m) limits deductibility of compensation over $1M for covered employees of public companies (post-TCJA, performance-based exception eliminated). (2) IRC Section 280G imposes a 20% excise tax on excess parachute payments (3x base amount) triggered by change in control, with a nondeductibility penalty for the employer. (3) IRC Section 409A governs deferred compensation, imposing strict timing rules for elections and distributions - violations trigger immediate taxation plus 20% penalty plus interest. (4) Clawback provisions: Dodd-Frank Section 954 (SEC Rule 10D-1) mandates recovery of incentive-based compensation from current/former executive officers following a restatement. (5) Employment agreements for executives typically include: base salary, bonus/incentive structures, equity grants (options, RSUs, performance shares), change-in-control provisions, severance terms, non-compete/non-solicitation clauses, confidentiality obligations, and dispute resolution mechanisms. Texas enforces executive non-competes under the Texas Business and Commerce Code Section 15.50-15.52, requiring the covenant to be ancillary to an otherwise enforceable agreement and reasonable in scope, geography, and duration.",
        "key_statutes": ["IRC Section 162(m) (deductibility limit)", "IRC Section 280G (golden parachute excise tax)", "IRC Section 409A (deferred compensation rules)", "IRC Section 457A (offshore deferred compensation)", "15 U.S.C. 78j-4 (Dodd-Frank clawback)", "Tex. Bus. & Com. Code 15.50-15.52 (Texas non-compete)", "17 C.F.R. 229.402 (SEC executive compensation disclosure)"],
        "elements": ["Executive-level employment relationship", "Compensation arrangement (cash, equity, deferred, contingent)", "Applicable regulatory framework (tax, securities, ERISA, state)", "Compliance with timing, disclosure, and structural requirements"],
        "defenses": ["Reasonable business judgment in compensation decisions", "Independent compensation committee with advisors", "Shareholder approval (say-on-pay favorable vote)", "Market data benchmarking", "409A compliance via good faith reasonable interpretation", "280G shareholder approval exception (private companies)"],
        "remedies": ["Contract damages for breach of employment agreement", "Equitable relief (specific performance of contract terms)", "Tax penalties (20% Section 409A excise, 20% Section 4999 excise)", "SEC enforcement actions (clawback, disgorgement)", "Injunctive relief for non-compete violations", "Attorneys fees per contract provisions"],
        "leading_cases": ["Schein v. Northern Rio Arriba Electric Cooperative, 100 T.C. 292 (1993) (Section 280G)", "Marsh & McLennan Companies v. Brumley, No. 652406/2018 (NY Sup. Ct.) (clawback enforcement)", "In re Dole Food Co., Inc. Stockholder Litigation, C.A. No. 8703-VCL (Del. Ch. 2015) (golden parachute valuation)"],
        "confidence": 0.83,
        "last_updated": "2026-01-15",
        "tags": ["executive_comp", "golden_parachute", "409a", "280g", "162m", "clawback", "non_compete", "deferred_comp"],
    },

    # ============================================================================
    # TRADE SECRETS AND NON-DISCLOSURE AGREEMENTS
    # ============================================================================

    "trade_secrets_nda": {
        "topic": "trade_secrets_nda",
        "title": "Trade Secret Protection and Non-Disclosure Agreements in Employment",
        "category": "confidential_information",
        "summary": "Trade secret protection in employment involves both federal and state law. The Defend Trade Secrets Act (DTSA), 18 U.S.C. 1836-1839, provides a federal private right of action for trade secret misappropriation, including ex parte seizure orders in extraordinary circumstances. Texas adopted the Uniform Trade Secrets Act (TUTSA), Tex. Civ. Prac. & Rem. Code Chapter 134A, effective September 1, 2013. Key elements: information must derive independent economic value from not being generally known, and the owner must take reasonable measures to maintain secrecy. Non-disclosure agreements (NDAs) in employment must be carefully drafted: overbroad NDAs may be unenforceable, and post-employment NDAs require consideration. The DTSA includes a whistleblower immunity provision (18 U.S.C. 1833(b)) protecting employees who disclose trade secrets to government officials or in court filings in connection with reporting suspected violations of law. Employers must provide notice of this immunity in any NDA or contract governing trade secrets. Failure to provide this notice results in the employer being unable to recover exemplary damages or attorneys fees in a DTSA action. Inevitable disclosure doctrine: some courts (not Texas) enjoin employees from working for competitors based on the inevitability that they will use or disclose trade secrets. Texas courts have generally rejected the inevitable disclosure doctrine, requiring proof of actual or threatened misappropriation. Practical issues include: defining what constitutes company trade secrets vs. employee general knowledge and skills, return of materials obligations, garden leave provisions, computer forensics evidence of misappropriation, and the intersection with non-compete agreements.",
        "key_statutes": ["18 U.S.C. 1836-1839 (Defend Trade Secrets Act)", "18 U.S.C. 1833(b) (whistleblower immunity for trade secret disclosure)", "18 U.S.C. 1832 (criminal theft of trade secrets)", "Tex. Civ. Prac. & Rem. Code Ch. 134A (Texas UTSA)", "Tex. Bus. & Com. Code 15.50 (non-compete interaction)"],
        "elements": ["Information qualifies as trade secret (economic value from secrecy)", "Owner took reasonable measures to maintain secrecy", "Defendant acquired, disclosed, or used trade secret", "Acquisition was by improper means OR breach of duty of confidentiality"],
        "defenses": ["Information is publicly available or generally known", "Independent development", "Reverse engineering (if legitimate)", "Inadequate secrecy measures by plaintiff", "Employee general knowledge and skills", "Whistleblower immunity (18 U.S.C. 1833(b))", "Statute of limitations (3 years DTSA, 3 years TUTSA)"],
        "remedies": ["Injunctive relief (including ex parte seizure under DTSA)", "Actual damages (lost profits, unjust enrichment)", "Reasonable royalty in lieu of actual damages", "Exemplary damages (up to 2x actual for willful misappropriation)", "Attorneys fees (for willful misappropriation or bad faith claim)", "Criminal penalties under Economic Espionage Act"],
        "leading_cases": ["PepsiCo, Inc. v. Redmond, 54 F.3d 1262 (7th Cir. 1995) (inevitable disclosure)", "T-N-T Motorsports, Inc. v. Hennessey Motorsports, Inc., 965 S.W.2d 18 (Tex. App. 1998)", "Southwestern Energy Production Co. v. Berry-Helfand, 491 S.W.3d 699 (Tex. 2016)", "Cardinal Health Staffing Network, Inc. v. Bowen, 106 S.W.3d 230 (Tex. App. 2003)"],
        "confidence": 0.88,
        "last_updated": "2026-01-15",
        "tags": ["trade_secrets", "nda", "dtsa", "tutsa", "misappropriation", "inevitable_disclosure", "whistleblower_immunity"],
    },

    # ============================================================================
    # INDEPENDENT CONTRACTOR VS EMPLOYEE (EXPANDED)
    # ============================================================================

    "abc_test_classification": {
        "topic": "abc_test_classification",
        "title": "ABC Test and State Worker Classification Standards",
        "category": "classification",
        "summary": "Beyond the federal economic reality test (FLSA) and common law control test (IRS/FICA), many states have adopted the ABC test for worker classification, which presumes workers are employees unless the hiring entity demonstrates all three factors. The ABC test (as codified in California's AB5, Cal. Lab. Code Section 2775): (A) the worker is free from control and direction of the hiring entity in performing the work, both under the contract and in fact; (B) the worker performs work that is outside the usual course of the hiring entity's business; and (C) the worker is customarily engaged in an independently established trade, occupation, or business of the same nature as that involved in the work performed. The 'B' prong is the most impactful - it effectively prevents companies from classifying their core service providers as independent contractors. States using some form of ABC test include California, Massachusetts, New Jersey, Illinois, and others. Texas does NOT use the ABC test; instead, Texas uses a 20-factor right-to-control analysis under Texas Labor Code Section 201.041 for unemployment insurance purposes. The IRS uses a three-category analysis: (1) behavioral control, (2) financial control, (3) relationship type. Misclassification penalties are severe: employer FICA liability (IRC 3509), FMLA/ADA/Title VII exposure, overtime liability, benefits eligibility, workers comp exposure, and state tax/unemployment penalties. The DOL issued a final rule effective March 11, 2024, rescinding the 2021 independent contractor rule and returning to a totality-of-circumstances economic reality test under the FLSA.",
        "key_statutes": ["29 U.S.C. 203(e)(1) (FLSA employee definition)", "Cal. Lab. Code 2775 (ABC test - AB5)", "Tex. Lab. Code 201.041 (Texas classification)", "IRC Section 3509 (misclassification penalties)", "IRC Section 530 (safe harbor for good faith misclassification)", "29 C.F.R. 795 (2024 DOL final rule)"],
        "elements": ["Services performed by worker for hiring entity", "Hiring entity exercises control or has right to control work (common law) OR fails to prove all ABC prongs (ABC test states)", "Economic dependence on hiring entity (FLSA economic reality)", "Worker not customarily engaged in independent business"],
        "defenses": ["IRC Section 530 safe harbor (reasonable basis, filing consistency, substantive consistency)", "Industry practice and custom", "Written independent contractor agreement (necessary but not sufficient)", "Worker holds own business license, insurance, tools", "Worker serves multiple clients", "BFOQ for independent contractor structure"],
        "remedies": ["Reclassification as employee with retroactive benefits", "Back overtime under FLSA (2-3 years)", "Back payroll taxes plus penalties (IRC 3509: 1.5% wages + 20% withheld FICA)", "State unemployment tax liability", "Workers compensation coverage/penalties", "Benefits eligibility (health insurance, retirement)", "Joint and several liability for staffing arrangements"],
        "leading_cases": ["Dynamex Operations West, Inc. v. Superior Court, 4 Cal. 5th 903 (2018) (ABC test adoption in California)", "National Labor Relations Board v. Hearst Publications, Inc., 322 U.S. 111 (1944) (economic reality)", "Nationwide Mutual Insurance Co. v. Darden, 503 U.S. 318 (1992) (common law test for ERISA)", "Borello & Sons, Inc. v. Department of Industrial Relations, 48 Cal. 3d 341 (1989)"],
        "confidence": 0.89,
        "last_updated": "2026-01-15",
        "tags": ["abc_test", "worker_classification", "ab5", "independent_contractor", "economic_reality", "misclassification", "irs_530"],
    },

    # ============================================================================
    # EMPLOYMENT TORTS (INTENTIONAL)
    # ============================================================================

    "employment_torts": {
        "topic": "employment_torts",
        "title": "Intentional Employment Torts: IIED, Fraud, Defamation",
        "category": "torts",
        "summary": "Employment relationships give rise to several intentional tort claims that exist independently of statutory discrimination claims. Intentional Infliction of Emotional Distress (IIED): requires extreme and outrageous conduct exceeding all bounds of decency tolerated in civilized society. In Texas, IIED in employment is very difficult to prove - the conduct must go beyond mere employment disputes, harassment, or even most termination scenarios (GTE Southwest, Inc. v. Bruce, 998 S.W.2d 605 (Tex. 1999)). Courts typically require a pattern of conduct rather than isolated incidents. Fraud/Fraudulent Inducement: actionable when employer makes material misrepresentations to induce employment (e.g., false promises about job security, compensation, position duties). In Texas, fraudulent inducement is a recognized exception to the at-will doctrine. Elements: material misrepresentation, knowledge of falsity or reckless disregard, intent to induce reliance, actual reliance, damages. Defamation in employment: most commonly arises from negative references, termination communications, or internal investigation disclosures. Texas provides a qualified privilege for employer communications made in good faith regarding job performance to parties with legitimate interest (former/prospective employers, internal management). Privilege is defeated by actual malice, excessive publication, or knowing falsehood. Tortious interference: applicable when third party (e.g., individual supervisor acting outside scope) interferes with at-will employment relationship. Invasion of privacy: electronic monitoring, search of personal belongings, drug testing procedures, public disclosure of private medical information. Assault and battery: physical confrontations in workplace, forced medical examinations.",
        "key_statutes": ["Tex. Civ. Prac. & Rem. Code 41.001 et seq. (exemplary damages)", "Tex. Lab. Code 103.001-103.004 (employment reference immunity)", "Tex. Civ. Prac. & Rem. Code 73.001 et seq. (defamation)", "Restatement (Second) of Torts 46 (IIED)", "Restatement (Second) of Torts 766B (tortious interference)"],
        "elements": ["IIED: extreme/outrageous conduct, intentional/reckless, severe emotional distress, causation", "Fraud: material misrepresentation, scienter, intent to induce reliance, justifiable reliance, damages", "Defamation: false statement of fact, publication to third party, fault, damages (per se or actual)", "Tortious interference: existing contract/relationship, willful and intentional interference, proximately causing damage"],
        "defenses": ["IIED: conduct not sufficiently outrageous, workers comp exclusivity bar, preemption by statutory scheme", "Fraud: at-will doctrine (no promise of continued employment), puffery/opinion defense, reasonable reliance lacking", "Defamation: truth, qualified privilege (good faith employer communications), opinion, consent", "Tortious interference: privilege/justification, acting within scope of authority"],
        "remedies": ["Actual damages (economic and non-economic)", "Exemplary/punitive damages (Texas cap: greater of 2x economic + equal to non-economic up to $750K, or $200K)", "Mental anguish damages", "Lost wages and benefits", "Medical expenses for emotional distress treatment", "Attorneys fees (some tort theories)", "Injunctive relief (restraining order for harassment/stalking)"],
        "leading_cases": ["GTE Southwest, Inc. v. Bruce, 998 S.W.2d 605 (Tex. 1999) (IIED in employment)", "Sterner v. Marathon Oil Company, 767 S.W.2d 686 (Tex. 1989) (fraudulent inducement of employment)", "Randalls Food Markets, Inc. v. Johnson, 891 S.W.2d 640 (Tex. 1995) (defamation privilege)", "Prudential Insurance Co. v. Financial Review Services, 29 S.W.3d 74 (Tex. 2000) (tortious interference)", "Duffield v. Memorial Hermann Health System, No. 01-18-00926-CV (Tex. App. 2020) (IIED threshold)"],
        "confidence": 0.86,
        "last_updated": "2026-01-15",
        "tags": ["iied", "fraud", "defamation", "tortious_interference", "employment_torts", "punitive_damages", "privilege"],
    },

    # ============================================================================
    # COLLECTIVE BARGAINING AND UNION LAW
    # ============================================================================

    "collective_bargaining": {
        "topic": "collective_bargaining",
        "title": "Collective Bargaining, Union Rights, and Labor Relations",
        "category": "labor_relations",
        "summary": "The National Labor Relations Act (NLRA), 29 U.S.C. 151-169, governs private sector labor-management relations. Section 7 guarantees employees the right to self-organization, form/join unions, bargain collectively, engage in concerted activity for mutual aid and protection, and refrain from these activities. Section 8(a) defines employer unfair labor practices (ULPs): interfering with Section 7 rights, dominating labor organizations, discriminating based on union activity, retaliating for filing charges, and refusing to bargain in good faith. Section 8(b) defines union ULPs: restraining employees, causing discrimination, refusing to bargain, engaging in prohibited strikes/boycotts, excessive fees, featherbedding, and recognitional/organizational picketing violations. The duty to bargain in good faith covers mandatory subjects (wages, hours, working conditions), permissive subjects (by agreement only), and illegal subjects (cannot be bargained). Texas is a right-to-work state (Tex. Lab. Code Chapter 101), meaning union security agreements (requiring union membership or dues payment as condition of employment) are prohibited. The NLRB has exclusive jurisdiction over most private-sector labor disputes, with limited exceptions for supervisors (excluded from NLRA coverage), agricultural laborers, domestic servants, and independent contractors. Recent NLRB developments include expanded joint employer standards, increased scrutiny of employer handbook policies, and broader interpretation of protected concerted activity (including social media posts). Weingarten rights: employees in unionized workplaces have the right to union representation during investigatory interviews that may lead to discipline. Non-union employees do not have Weingarten rights under current Board law (IBM Corp., 341 NLRB 1288 (2004)).",
        "key_statutes": ["29 U.S.C. 151-169 (NLRA)", "29 U.S.C. 157 (Section 7 employee rights)", "29 U.S.C. 158(a) (employer unfair labor practices)", "29 U.S.C. 158(b) (union unfair labor practices)", "29 U.S.C. 158(d) (duty to bargain in good faith)", "Tex. Lab. Code Ch. 101 (right-to-work)"],
        "elements": ["Section 8(a)(1): employer conduct, tendency to interfere with Section 7 rights", "Section 8(a)(3): union activity, employer knowledge, adverse action, anti-union animus", "Section 8(a)(5): valid bargaining obligation, mandatory subject, refusal to bargain in good faith", "Section 8(b)(1): union restraint/coercion of employees in exercise of Section 7 rights"],
        "defenses": ["Employer speech rights (Section 8(c) - opinion/prediction without threat/promise)", "Business justification for action (Wright Line dual motive analysis)", "Management rights clause in CBA", "Right-to-work state law (no compulsory union fees)", "Supervisory exclusion from NLRA coverage", "Statute of limitations (6 months for ULP charges, 29 U.S.C. 160(b))"],
        "remedies": ["Cease and desist order", "Reinstatement with back pay (less interim earnings)", "Bargaining order (in extraordinary cases, Gissel)", "Notice posting (physical and electronic)", "Make-whole relief for consequential damages (Thryv Inc., 372 NLRB No. 22 (2022))", "Attorneys fees (in exceptional circumstances)"],
        "leading_cases": ["NLRB v. Jones & Laughlin Steel Corp., 301 U.S. 1 (1937) (NLRA constitutionality)", "NLRB v. Gissel Packing Co., 395 U.S. 575 (1969) (bargaining orders)", "Wright Line, a Division of Wright Line, Inc., 251 NLRB 1083 (1980) (dual motive analysis)", "NLRB v. J. Weingarten, Inc., 420 U.S. 251 (1975) (union rep at investigatory interviews)", "Cemex Construction Materials Pacific, LLC, 372 NLRB No. 130 (2023) (revised recognition framework)"],
        "confidence": 0.87,
        "last_updated": "2026-01-15",
        "tags": ["nlra", "collective_bargaining", "union", "ulp", "section_7", "right_to_work", "weingarten", "concerted_activity"],
    },

    # ============================================================================
    # WAGE THEFT AND FLSA ENFORCEMENT
    # ============================================================================

    "wage_theft_enforcement": {
        "topic": "wage_theft_enforcement",
        "title": "Wage Theft Prevention and FLSA Enforcement Mechanisms",
        "category": "wage_and_hour",
        "summary": "Wage theft encompasses a range of employer violations: failure to pay minimum wage, unpaid overtime, off-the-clock work, tip stealing, illegal deductions, misclassification to avoid overtime, meal/rest period violations, and failure to pay final wages. The FLSA provides two enforcement mechanisms: (1) Department of Labor (WHD) enforcement actions, and (2) private lawsuits under 29 U.S.C. 216(b), which allows collective actions (opt-in, not opt-out like class actions). FLSA statute of limitations: 2 years (3 years for willful violations). Liquidated damages: equal to unpaid wages (effectively doubling recovery) unless employer proves good faith reasonable belief of compliance. Texas Payday Law (Tex. Lab. Code Chapter 61) requires timely payment of wages upon separation: within 6 days for fired employees, next regular payday for employees who quit. Penalties for Texas Payday Law violations: TWC can order triple the wages owed plus administrative penalties. State wage theft criminal statutes: several states have enacted criminal penalties for wage theft; Texas has Tex. Penal Code 31.04 (theft of services) that can apply. Portal-to-Portal Act (29 U.S.C. 251-262): exempts employers from compensating for travel to/from work and certain preliminary/postliminary activities, unless they are integral and indispensable to principal activities (Integrity Staffing Solutions v. Busk, 574 U.S. 27 (2014)). Recent FLSA developments: 2024 overtime rule raising salary threshold to $58,656 (effective Jan. 1, 2025, but subject to litigation in Texas v. DOL, No. 4:24-cv-00468-SDJ (E.D. Tex.)).",
        "key_statutes": ["29 U.S.C. 206 (minimum wage)", "29 U.S.C. 207 (overtime)", "29 U.S.C. 216(b) (private right of action, collective actions)", "29 U.S.C. 255 (statute of limitations)", "29 U.S.C. 260 (good faith defense to liquidated damages)", "Tex. Lab. Code Ch. 61 (Texas Payday Law)", "29 U.S.C. 251-262 (Portal-to-Portal Act)"],
        "elements": ["Employment relationship (not independent contractor)", "Work performed for employer's benefit", "Employer knew or should have known of work (suffered or permitted)", "Wages not paid in accordance with FLSA/state requirements", "For overtime: hours exceed 40 in workweek, no valid exemption"],
        "defenses": ["FLSA exemption (executive, administrative, professional, computer, outside sales, highly compensated)", "Good faith reasonable belief of compliance (reduces liquidated damages)", "De minimis doctrine (trivial off-the-clock time)", "Portal-to-Portal Act (non-compensable preliminary/postliminary activities)", "Statute of limitations (2 years standard, 3 years willful)", "Section 259 reliance on DOL regulations or written rulings"],
        "remedies": ["Unpaid wages (minimum wage differential or overtime premium)", "Liquidated damages equal to unpaid wages (29 U.S.C. 216(b))", "Attorneys fees and costs (mandatory for prevailing plaintiff)", "Pre-judgment interest (in lieu of liquidated damages if good faith defense succeeds)", "Injunctive relief (DOL enforcement actions)", "Criminal penalties (willful violations: up to $10,000 fine, 6 months imprisonment)", "Texas Payday Law: triple damages plus administrative penalties"],
        "leading_cases": ["Integrity Staffing Solutions, Inc. v. Busk, 574 U.S. 27 (2014) (security screening not compensable)", "Encino Motorcars, LLC v. Navarro, 584 U.S. 79 (2018) (service advisor exemption)", "Genesis Healthcare Corp. v. Symczyk, 569 U.S. 66 (2013) (mootness of FLSA collective actions)", "Tyson Foods, Inc. v. Bouaphakeo, 577 U.S. 442 (2016) (representative evidence in FLSA class action)", "IBP, Inc. v. Alvarez, 546 U.S. 21 (2005) (walking time to donning/doffing stations compensable)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["wage_theft", "flsa_enforcement", "collective_action", "overtime", "minimum_wage", "liquidated_damages", "texas_payday"],
    },

    # ============================================================================
    # EMPLOYEE BENEFITS AND ERISA LITIGATION
    # ============================================================================

    "erisa_litigation": {
        "topic": "erisa_litigation",
        "title": "ERISA Litigation: Benefits Claims, Fiduciary Duty, and Preemption",
        "category": "benefits",
        "summary": "ERISA (29 U.S.C. 1001-1461) governs employer-sponsored benefit plans, creating a comprehensive federal regulatory framework. Key litigation areas: (1) Benefits claims under Section 502(a)(1)(B): participants may sue to recover benefits due, enforce rights, or clarify future benefits. Standard of review depends on plan language: if plan grants administrator discretionary authority, courts apply abuse of discretion standard (Firestone Tire & Rubber Co. v. Bruch, 489 U.S. 101 (1989)); otherwise, de novo review. (2) Fiduciary duty claims under Section 502(a)(2): fiduciaries must act solely in participants' interest with prudence (prudent expert standard), diversify investments, and follow plan documents. Recent wave of excessive fee litigation (401(k) plans charging above-market fees) under Section 502(a)(2) (Hughes v. Northwestern University, 595 U.S. 170 (2022)). (3) ERISA preemption: Section 514(a) preempts all state laws that 'relate to' employee benefit plans, creating a powerful defense. However, preemption does not apply to state laws of general applicability (insurance regulation, banking, securities), and the savings clause preserves state insurance regulation (Section 514(b)(2)(A)). ERISA's exclusive remedies limitation means participants typically cannot recover punitive damages or extra-contractual damages for benefit denials. (4) COBRA continuation coverage (29 U.S.C. 1161-1168): employers with 20+ employees must offer 18/36 month continuation upon qualifying events. Failure to provide timely COBRA notice: statutory penalty of $110/day. Texas mini-COBRA (Tex. Ins. Code Chapter 1251) extends continuation rights for employers with 2-19 employees (up to 9 months).",
        "key_statutes": ["29 U.S.C. 1132(a)(1)(B) (benefits claims)", "29 U.S.C. 1132(a)(2) (fiduciary breach claims)", "29 U.S.C. 1104 (fiduciary duties - prudence, loyalty)", "29 U.S.C. 1144 (ERISA preemption)", "29 U.S.C. 1161-1168 (COBRA)", "Tex. Ins. Code Ch. 1251 (Texas mini-COBRA)"],
        "elements": ["Benefits claim: covered plan, eligible participant, benefits due under plan terms, proper claim procedure exhausted", "Fiduciary claim: plan fiduciary status, breach of duty (prudence, loyalty, diversification), loss to plan, causation", "Preemption: state law claim, relates to employee benefit plan, no savings clause exception"],
        "defenses": ["Plan terms support denial (substantial evidence under abuse of discretion review)", "Timely and adequate notice of adverse determination", "Full and fair review provided on appeal", "Fiduciary prudence: documented investigation and decision process", "ERISA preemption of state law claims", "Statute of limitations: 6 years from breach (fiduciary) or 3 years from earliest date of knowledge", "Exhaustion of administrative remedies requirement"],
        "remedies": ["Benefits due under plan terms (502(a)(1)(B))", "Equitable relief (injunction, declaratory judgment)", "Plan-wide relief for fiduciary breach (disgorgement, surcharge)", "Statutory COBRA penalty ($110/day)", "Attorneys fees (discretionary, five-factor test)", "No punitive damages under ERISA (Mertens v. Hewitt Assocs., 508 U.S. 248 (1993))", "No consequential or extra-contractual damages for benefit denials"],
        "leading_cases": ["Firestone Tire & Rubber Co. v. Bruch, 489 U.S. 101 (1989) (standard of review)", "Hughes v. Northwestern University, 595 U.S. 170 (2022) (excessive fee claims survive motion to dismiss)", "Metropolitan Life Insurance Co. v. Glenn, 554 U.S. 105 (2008) (conflict of interest as factor)", "Mertens v. Hewitt Associates, 508 U.S. 248 (1993) (equitable relief limitation)", "CIGNA Corp. v. Amara, 563 U.S. 421 (2011) (equitable surcharge remedy)", "Pilot Life Insurance Co. v. Dedeaux, 481 U.S. 41 (1987) (preemption of state bad faith claims)"],
        "confidence": 0.88,
        "last_updated": "2026-01-15",
        "tags": ["erisa_litigation", "benefits_claims", "fiduciary_duty", "preemption", "cobra", "excessive_fees", "standard_of_review"],
    },

    # ============================================================================
    # WORKPLACE SAFETY AND OSHA ENFORCEMENT (EXPANDED)
    # ============================================================================

    "osha_enforcement_expanded": {
        "topic": "osha_enforcement_expanded",
        "title": "OSHA Enforcement: Citations, Penalties, and Employer Obligations",
        "category": "workplace_safety",
        "summary": "The Occupational Safety and Health Act (29 U.S.C. 651-678) requires employers to provide workplaces free from recognized hazards causing or likely to cause death or serious physical harm (General Duty Clause, Section 5(a)(1)) and to comply with specific OSHA standards (Section 5(a)(2)). OSHA enforcement begins with inspections (triggered by imminent danger, fatality/hospitalization, complaints, referrals, targeted programs, or follow-up). Employer rights during inspection: limit scope to warrant/complaint basis, accompany inspector, require warrant (absent consent or recognized exception). Citation types: Other-Than-Serious (up to $16,131), Serious ($1,116-$16,131), Willful ($11,524-$161,323), Repeat ($11,524-$161,323), Failure to Abate ($16,131/day). Criminal penalties: willful violation causing employee death (up to $250,000 individual/$500,000 corporate, 6 months imprisonment; doubled for repeat). Multi-employer worksite doctrine: OSHA can cite creating, exposing, correcting, and controlling employers. Employer obligations include: hazard communication (GHS labeling, SDS, training), recordkeeping (OSHA 300 log, 300A summary, 301 incident reports), reporting (8 hours for fatality, 24 hours for hospitalization/amputation/eye loss), anti-retaliation (Section 11(c) - 30 day filing deadline), and industry-specific standards (construction, general industry, maritime, agriculture). Texas does not have a state OSHA plan for private sector employers; federal OSHA has jurisdiction. Texas has its own program for state and local government employees only. Abatement obligations: employer must correct cited hazards within prescribed timeframe and certify abatement.",
        "key_statutes": ["29 U.S.C. 654(a)(1) (General Duty Clause)", "29 U.S.C. 654(a)(2) (compliance with standards)", "29 U.S.C. 660(c) (anti-retaliation)", "29 U.S.C. 666 (penalties)", "29 C.F.R. 1904 (recordkeeping)", "29 C.F.R. 1910 (general industry standards)", "29 C.F.R. 1926 (construction standards)"],
        "elements": ["General Duty Clause: recognized hazard, causing or likely to cause death/serious harm, feasible abatement exists, employer failed to abate", "Specific standard: applicable standard exists, employer failed to comply, employee exposed to hazard, employer knew or should have known", "Willful: employer aware of standard and consciously disregarded or was plainly indifferent"],
        "defenses": ["Greater hazard (compliance creates greater danger than noncompliance)", "Infeasibility (technical or economic impossibility of compliance)", "Employee misconduct (isolated, unforeseeable, rule against violated)", "De minimis violation (no direct safety impact)", "Variance (approved alternative method)", "Statute of limitations (6 months from occurrence)", "Multi-employer site: no control, creation, or exposure responsibility"],
        "remedies": ["Citation and monetary penalties (adjusted annually for inflation)", "Abatement requirement with deadline", "Informal conference and settlement", "Formal hearing before OSHRC (Occupational Safety and Health Review Commission)", "Federal court appeal from OSHRC decision", "Criminal prosecution (willful violation causing death)", "Section 11(c) retaliation: reinstatement, back pay, compensatory damages"],
        "leading_cases": ["Secretary of Labor v. Trinity Industries, Inc., 504 F.3d 397 (3d Cir. 2007) (multi-employer doctrine)", "Whirlpool Corp. v. Marshall, 445 U.S. 1 (1980) (employee right to refuse dangerous work)", "National Realty & Construction Co. v. OSHRC, 489 F.2d 1257 (D.C. Cir. 1973) (General Duty Clause elements)", "Hern Iron Works, Inc. v. Donovan, 670 F.2d 838 (9th Cir. 1982) (employee misconduct defense)", "SeaWorld of Florida, LLC v. Perez, 748 F.3d 1202 (D.C. Cir. 2014) (General Duty Clause in entertainment)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["osha_enforcement", "citations", "penalties", "general_duty", "multi_employer", "recordkeeping", "anti_retaliation"],
    },

    # ============================================================================
    # EMPLOYMENT AGREEMENTS AND RESTRICTIVE COVENANTS
    # ============================================================================

    "restrictive_covenants": {
        "topic": "restrictive_covenants",
        "title": "Restrictive Covenants: Non-Competes, Non-Solicitation, No-Hire",
        "category": "contracts",
        "summary": "Restrictive covenants in employment include non-compete agreements, non-solicitation agreements (customers and employees), no-hire/no-poach agreements, garden leave provisions, and forfeiture-for-competition clauses. Texas enforces non-competes under the Covenants Not to Compete Act (Tex. Bus. & Com. Code Section 15.50-15.52) if: (1) ancillary to or part of an otherwise enforceable agreement, and (2) reasonable in time, geographical area, and scope of activity. The 'otherwise enforceable agreement' requires the employer to provide consideration that gives rise to an interest worthy of protection (e.g., confidential information, trade secrets, specialized training, customer relationships). For at-will employees, the Texas Supreme Court in Marsh USA Inc. v. Cook, 354 S.W.3d 764 (Tex. 2011), held that stock options and performance-based compensation can constitute adequate consideration. If a non-compete is unreasonable, Texas courts must reform (not void) the covenant to make it reasonable (Tex. Bus. & Com. Code Section 15.51(c)). FTC Non-Compete Rule: On April 23, 2024, the FTC issued a final rule banning most non-compete agreements nationwide, but it was vacated by Ryan LLC v. FTC, No. 3:24-cv-00986-E (N.D. Tex. Aug. 20, 2024) and remains unenforceable. Non-solicitation agreements: generally more enforceable than non-competes because they are narrower in scope. Must still be reasonable and supported by legitimate protectable interest. No-poach/no-hire agreements between employers: DOJ criminally prosecuted these as per se antitrust violations under the Sherman Act (United States v. DaVita Inc., No. 22-cr-00264 (D. Colo. 2022)). Garden leave: employer pays employee during restricted period - increasing enforceability.",
        "key_statutes": ["Tex. Bus. & Com. Code 15.50-15.52 (Covenants Not to Compete Act)", "Tex. Bus. & Com. Code 15.51(c) (judicial reformation)", "15 U.S.C. 1 (Sherman Act - no-poach agreements)", "Uniform Trade Secrets Act (protectable interest foundation)", "FTC Non-Compete Rule (vacated, 16 C.F.R. Part 910)"],
        "elements": ["Valid restrictive covenant (non-compete, non-solicit, no-hire)", "Ancillary to otherwise enforceable agreement with adequate consideration", "Reasonable restrictions (time: typically 1-2 years; geography: area of operations; scope: related activities)", "Protectable interest (trade secrets, confidential information, customer relationships, specialized training)", "Breach by former employee/competing employer"],
        "defenses": ["Lack of adequate consideration", "Unreasonable scope (too broad in time, geography, or activity)", "Changed circumstances (job duties different from agreement scope)", "Employer's prior material breach (unclean hands)", "Public policy exception (healthcare professionals in some states)", "Antitrust violation (employer-to-employer no-poach)", "FTC rule applicability (if reinstated on appeal)"],
        "remedies": ["Temporary restraining order and preliminary injunction", "Permanent injunction", "Actual damages (lost profits, customer diversion)", "Liquidated damages (if contract provision)", "Attorneys fees (Tex. Bus. & Com. Code 15.51(c))", "Forfeiture of deferred compensation (forfeiture-for-competition clauses)", "Reformation to make covenant reasonable (mandatory in Texas)"],
        "leading_cases": ["Marsh USA Inc. v. Cook, 354 S.W.3d 764 (Tex. 2011) (stock options as consideration)", "Alex Sheshunoff Management Services, L.P. v. Johnson, 209 S.W.3d 644 (Tex. 2006) (reformation requirement)", "Ryan LLC v. FTC, No. 3:24-cv-00986-E (N.D. Tex. 2024) (FTC rule vacated)", "Light v. Centel Cellular Co., 883 S.W.2d 642 (Tex. 1994) (continued employment as consideration)", "United States v. DaVita Inc., No. 22-cr-00264 (D. Colo. 2022) (criminal no-poach prosecution)"],
        "confidence": 0.91,
        "last_updated": "2026-01-15",
        "tags": ["non_compete", "non_solicitation", "no_poach", "garden_leave", "restrictive_covenant", "ftc_rule", "reformation"],
    },

    # ============================================================================
    # WRONGFUL TERMINATION IN VIOLATION OF PUBLIC POLICY
    # ============================================================================

    "wrongful_termination_public_policy": {
        "topic": "wrongful_termination_public_policy",
        "title": "Wrongful Termination in Violation of Public Policy (Sabine Pilot Doctrine)",
        "category": "termination",
        "summary": "Texas is an at-will employment state, meaning either party can terminate the employment relationship at any time for any reason or no reason. However, the Texas Supreme Court recognized a narrow public policy exception in Sabine Pilot Service, Inc. v. Hauck, 687 S.W.2d 733 (Tex. 1985): an employee may bring a wrongful termination claim if discharged solely for refusing to perform an illegal act that carries criminal penalties. This is the ONLY common law exception to at-will employment recognized by Texas courts. The exception is extremely narrow: (1) the illegal act must carry criminal penalties (not merely civil liability or regulatory violations); (2) the employee must have been specifically asked to commit the criminal act; (3) the sole reason for termination must have been the refusal to commit the act; (4) the employee bears the burden of proving sole causation. Texas courts have consistently refused to expand the Sabine Pilot exception to cover other public policy grounds such as filing workers compensation claims (which is covered by statute, Tex. Lab. Code 451.001), serving on a jury, reporting safety violations, or general whistleblowing (covered by the Texas Whistleblower Act for public employees only). Other states have much broader public policy exceptions: California's Tameny doctrine covers termination for refusing to violate any statute, exercising a statutory right, or performing a statutory duty. Comparison: most wrongful termination claims in Texas are pursued under specific statutory protections rather than common law public policy theory. Remedies for Sabine Pilot claims include lost wages, mental anguish damages, and potentially exemplary damages under Texas Civil Practice and Remedies Code Section 41.003.",
        "key_statutes": ["Sabine Pilot Service, Inc. v. Hauck, 687 S.W.2d 733 (Tex. 1985) (judicial doctrine)", "Tex. Lab. Code 451.001 (workers comp retaliation - separate statutory claim)", "Tex. Gov. Code Ch. 554 (Texas Whistleblower Act - public employees only)", "Tex. Civ. Prac. & Rem. Code 41.003 (exemplary damages)"],
        "elements": ["At-will employment relationship existed", "Employer directed employee to perform an act carrying criminal penalties", "Employee refused to perform the criminal act", "Refusal was sole cause of termination (not merely contributing factor)", "Employee can identify the specific criminal statute that would be violated"],
        "defenses": ["Termination based on legitimate non-pretextual reasons", "Act requested was not actually criminal (merely civil violation or regulatory breach)", "Employee was not actually asked to commit the illegal act", "Employee voluntarily resigned", "Mixed-motive (other valid reasons for termination beyond refusal)", "Statute of limitations (2 years for wrongful termination in Texas)"],
        "remedies": ["Lost wages (back pay and front pay)", "Mental anguish damages", "Exemplary damages (if clear and convincing evidence of malice or gross negligence)", "Court costs", "No attorneys fees under common law (unless equity exception applies)", "Reinstatement (rarely ordered in at-will context)"],
        "leading_cases": ["Sabine Pilot Service, Inc. v. Hauck, 687 S.W.2d 733 (Tex. 1985) (establishing the doctrine)", "Ed Rachal Foundation v. D'Unger, 207 S.W.3d 330 (Tex. 2006) (refusing to expand exception)", "Winters v. Houston Chronicle Publishing Co., 795 S.W.2d 723 (Tex. 1990) (no expansion to refusal to testify)", "White v. FCI USA, Inc., 319 F.3d 672 (5th Cir. 2003) (applying Sabine Pilot in federal court)", "Austin v. HealthTrust, Inc., 967 S.W.2d 400 (Tex. 1998) (no common law claim where statutory remedy exists)"],
        "confidence": 0.93,
        "last_updated": "2026-01-15",
        "tags": ["wrongful_termination", "public_policy", "sabine_pilot", "at_will", "criminal_act_refusal", "texas_employment"],
    },

    # ============================================================================
    # EMPLOYMENT DISCRIMINATION INVESTIGATION PROCEDURES
    # ============================================================================

    "workplace_investigation_procedures": {
        "topic": "workplace_investigation_procedures",
        "title": "Workplace Investigation Procedures and Best Practices",
        "category": "compliance",
        "summary": "Prompt and thorough investigation of workplace complaints is a critical component of employer compliance with Title VII, ADA, ADEA, and state anti-discrimination laws. The Faragher-Ellerth defense to vicarious liability for supervisor harassment requires the employer to show it exercised reasonable care to prevent and promptly correct harassment, which includes conducting adequate investigations. Investigation triggers include: formal complaints, informal complaints to any manager, observed misconduct, anonymous hotline reports, exit interview disclosures, EEOC charges, and pattern indicators. Investigation steps: (1) assign investigator (internal HR, employment counsel, or third-party investigator - choose based on severity and conflict of interest analysis); (2) develop investigation plan (scope, witnesses, documents, timeline); (3) interim measures (separation of parties, temporary reassignment - avoid penalizing complainant); (4) conduct witness interviews (complainant first, then witnesses, respondent last; document with contemporaneous notes; advise of non-retaliation policy); (5) gather documentary evidence (emails, texts, surveillance, access logs, HR records); (6) assess credibility (demeanor, corroboration, consistency, motive to fabricate, plausibility); (7) make factual findings (preponderance of evidence standard for internal investigations); (8) determine appropriate remedial action (proportionate to violation: training, warning, PIP, suspension, transfer, demotion, termination); (9) communicate findings to parties (limited disclosure on need-to-know basis); (10) follow up to ensure no retaliation. Documentation is critical: maintain investigation file with complaint, notes, evidence, findings, and remedial action. Privilege considerations: work-product doctrine and attorney-client privilege may protect investigation documents, but only if investigation is conducted at the direction of counsel for the purpose of providing legal advice (Upjohn Co. v. United States, 449 U.S. 383 (1981)). Common pitfalls: failing to investigate at all, delayed investigation, predetermined conclusions, failing to interview key witnesses, inadequate documentation, disproportionate remedial measures, and retaliating against complainant or witnesses.",
        "key_statutes": ["42 U.S.C. 2000e-5(b) (EEOC investigation authority)", "29 C.F.R. 1604.11(d) (employer's duty to investigate harassment)", "EEOC Enforcement Guidance on Harassment (2024 update)", "Faragher/Ellerth defense requirements (judicial doctrine)"],
        "elements": ["Complaint or notice of potential misconduct received", "Prompt initiation of investigation (within 1-3 business days)", "Investigation conducted by neutral investigator without conflict of interest", "Thorough documentation of all evidence and witness statements", "Factual findings based on preponderance of evidence", "Proportionate remedial action implemented", "Follow-up to ensure complaint resolved and no retaliation"],
        "defenses": ["Employer conducted prompt, thorough, and impartial investigation", "Appropriate remedial action taken promptly upon finding violation", "Investigation consistent with published employer policies", "Complainant failed to use available complaint procedures (Faragher-Ellerth)", "No actual knowledge of harassment/discrimination (where required)"],
        "remedies": ["Internal disciplinary action against wrongdoer", "Policy revisions and enhanced training", "Monitoring for compliance", "If investigation was inadequate: employer loses Faragher-Ellerth defense", "EEOC may find cause and pursue enforcement action", "Punitive damages exposure increases with failure to investigate"],
        "leading_cases": ["Faragher v. City of Boca Raton, 524 U.S. 775 (1998) (affirmative defense)", "Burlington Industries, Inc. v. Ellerth, 524 U.S. 742 (1998) (same)", "Upjohn Co. v. United States, 449 U.S. 383 (1981) (attorney-client privilege for corporate investigations)", "Staub v. Proctor Hospital, 562 U.S. 411 (2011) (cat's paw liability - biased subordinate influence)", "Vance v. Ball State University, 570 U.S. 421 (2013) (supervisor definition for harassment liability)"],
        "confidence": 0.89,
        "last_updated": "2026-01-15",
        "tags": ["investigation", "harassment_complaint", "faragher_ellerth", "remedial_action", "compliance", "documentation", "credibility"],
    },

    # ============================================================================
    # MASS LAYOFFS AND REDUCTION IN FORCE
    # ============================================================================

    "reduction_in_force": {
        "topic": "reduction_in_force",
        "title": "Reduction in Force (RIF): Planning, Selection, and Legal Compliance",
        "category": "termination",
        "summary": "Reductions in force (RIFs) require careful legal planning to minimize litigation risk. Key legal requirements: (1) WARN Act (29 U.S.C. 2101-2109): employers with 100+ employees must provide 60 days written notice before plant closings (permanent/temporary shutdown affecting 50+ employees at single site) or mass layoffs (50+ employees constituting 33% of workforce, or 500+ employees regardless of percentage, at single site). Exceptions: faltering company (limited to plant closings), unforeseeable business circumstances, and natural disaster. Penalties: back pay and benefits for up to 60 days plus $500/day civil penalty. (2) OWBPA (Older Workers Benefit Protection Act, 29 U.S.C. 626(f)): for group termination programs, waivers of ADEA claims must include: consideration beyond what employee is already entitled to, written agreement advising employee to consult attorney, 45-day consideration period (not 21 as for individual waivers), 7-day revocation period, and information about the decisional unit (job titles, ages of selected and non-selected employees). (3) Disparate impact analysis: employers should conduct statistical analysis of RIF selections by protected category (age, race, sex, disability) BEFORE implementing to identify and address disproportionate impact. (4) Selection criteria must be objective and job-related: performance ratings, seniority, skills, certifications. Subjective criteria increase litigation risk. (5) Document business justification: financial data supporting necessity, alternatives considered and rejected, selection methodology and criteria weights. (6) Severance and release: standard practice to offer severance in exchange for general release; OWBPA compliance required for employees 40+. (7) COBRA and benefits continuation notification. (8) State-specific requirements: some states (California, New York, Illinois) have additional notice requirements or expanded coverage beyond federal WARN.",
        "key_statutes": ["29 U.S.C. 2101-2109 (WARN Act)", "29 U.S.C. 626(f) (OWBPA waiver requirements for group terminations)", "29 U.S.C. 623 (ADEA disparate impact)", "42 U.S.C. 2000e-2 (Title VII disparate impact)", "Tex. Lab. Code 61.014-61.015 (final pay requirements)"],
        "elements": ["Business justification for reduction (financial, operational, strategic)", "Objective selection criteria applied consistently", "Statistical analysis showing no disparate impact on protected groups", "WARN Act notice provided 60 days in advance (if threshold met)", "OWBPA-compliant waiver for employees 40+ in group termination", "Severance consideration beyond existing entitlement", "Documentation of decision-making process"],
        "defenses": ["Legitimate business reasons for RIF (economic downturn, restructuring, redundancy)", "Objective, job-related selection criteria", "Statistical analysis demonstrates no adverse impact", "Reasonable factor other than age (RFOA) for ADEA claims", "Employee signed valid release and waiver", "WARN Act exception (faltering company, unforeseeable circumstances, natural disaster)", "Same-decision defense (would have been selected regardless of protected status)"],
        "remedies": ["WARN Act: 60 days back pay and benefits per affected employee, $500/day civil penalty", "Title VII/ADEA: reinstatement, back pay, compensatory/liquidated damages", "OWBPA violation: waiver is void, employee retains right to sue under ADEA", "State law penalties for failure to provide required notice", "Attorneys fees for prevailing plaintiffs", "Class/collective action exposure for pattern-or-practice claims"],
        "leading_cases": ["Meacham v. Knolls Atomic Power Laboratory, 554 U.S. 84 (2008) (RFOA defense - employer burden)", "Smith v. City of Jackson, 544 U.S. 228 (2005) (ADEA disparate impact claims)", "Oubre v. Entergy Operations, Inc., 522 U.S. 422 (1998) (defective OWBPA waiver is voidable)", "Loewen v. Lykes Bros. Steamship Co., 557 F.2d 1237 (5th Cir. 1977) (RIF selection criteria)", "United Food and Commercial Workers Union v. Brown Group, Inc., 517 U.S. 544 (1996) (WARN Act standing)"],
        "confidence": 0.90,
        "last_updated": "2026-01-15",
        "tags": ["rif", "reduction_in_force", "warn_act", "owbpa", "mass_layoff", "disparate_impact", "severance", "plant_closing"],
    },

    # ============================================================================
    # EMPLOYMENT RECORDS AND PRIVACY
    # ============================================================================

    "personnel_records_privacy": {
        "topic": "personnel_records_privacy",
        "title": "Personnel Records, Employee Monitoring, and Workplace Privacy",
        "category": "privacy",
        "summary": "Employment records and workplace privacy involves multiple intersecting legal frameworks. Personnel records: while there is no general federal law requiring employers to maintain or provide access to personnel files, many states have personnel file access statutes (California, Massachusetts, Illinois, and others). Texas does NOT have a personnel file access statute. However, EEOC regulations require retention of personnel records for one year from date of making the record or taking the personnel action (29 C.F.R. 1602.14), and ADEA regulations require retention for three years for payroll records (29 C.F.R. 1627.3). FLSA requires retention of pay records for three years (29 C.F.R. 516.5). Employee monitoring: the Electronic Communications Privacy Act (ECPA, 18 U.S.C. 2510-2522) generally prohibits interception of electronic communications, but the business extension exception (18 U.S.C. 2510(5)(a)) permits monitoring on employer-provided equipment in the ordinary course of business. The Stored Communications Act (18 U.S.C. 2701-2712) restricts access to stored electronic communications but generally allows employer access to communications on employer systems. Texas is a one-party consent state for recording conversations (Tex. Penal Code 16.02). BYOD (Bring Your Own Device) policies create additional privacy complexities regarding employer access to personal devices. Social media: the National Labor Relations Act protects some employee social media activity as concerted activity; many states (but not Texas) prohibit employers from requesting social media passwords. Video surveillance: generally permissible in common areas; prohibited in areas with expectation of privacy (restrooms, changing rooms). GPS tracking of company vehicles is generally permissible during work hours; tracking personal vehicles or after hours raises privacy concerns. Biometric data: Illinois BIPA (740 ILCS 14/) is the strictest; Texas has a narrower biometric identifier statute (Tex. Bus. & Com. Code Chapter 503) requiring notice and consent for capture of biometric identifiers but providing no private right of action (enforcement by AG only, up to $25,000/violation).",
        "key_statutes": ["18 U.S.C. 2510-2522 (ECPA/Wiretap Act)", "18 U.S.C. 2701-2712 (Stored Communications Act)", "29 C.F.R. 1602.14 (EEOC record retention)", "29 C.F.R. 516.5 (FLSA record retention)", "Tex. Penal Code 16.02 (one-party consent)", "Tex. Bus. & Com. Code Ch. 503 (biometric identifiers)", "29 U.S.C. 157 (Section 7 NLRA - social media as concerted activity)"],
        "elements": ["Employment or applicant relationship", "Collection, use, or disclosure of employee personal information", "Privacy expectation (reasonable under circumstances)", "Employer monitoring or access (type, scope, notice provided)", "Applicable federal/state privacy framework"],
        "defenses": ["Legitimate business purpose for monitoring/collection", "Written policy notifying employees of monitoring (handbook acknowledgment)", "Business extension exception (ECPA) for company equipment", "Employee consent (express or implied through policy acknowledgment)", "Company-owned equipment/systems", "Safety or security justification", "Regulatory compliance requirement (recordkeeping obligations)"],
        "remedies": ["ECPA: $10,000 minimum statutory damages per violation, actual damages, punitive damages, attorneys fees", "Texas wiretap violation: civil damages or Class A misdemeanor", "NLRB: reinstatement, back pay for social media retaliation", "State privacy tort claims: actual and punitive damages", "Texas biometric: AG enforcement, $25,000/violation (no private action)", "Common law invasion of privacy: actual damages, mental anguish, punitive damages"],
        "leading_cases": ["City of Ontario v. Quon, 560 U.S. 746 (2010) (limited expectation of privacy in employer-provided pager)", "Stengart v. Loving Care Agency, Inc., 201 N.J. 300 (2010) (attorney-client privilege on employer computer)", "Pietrylo v. Hillstone Restaurant Group, No. 06-5754 (D.N.J. 2009) (SCA violation for accessing employee social media)", "Purple Communications, Inc., 361 NLRB 1050 (2014) (employee right to use employer email for Section 7 activity)", "Riley v. California, 573 U.S. 373 (2014) (cell phone privacy - limited applicability to private employers)"],
        "confidence": 0.85,
        "last_updated": "2026-01-15",
        "tags": ["personnel_records", "employee_monitoring", "privacy", "ecpa", "biometric", "social_media", "surveillance", "record_retention"],
    },

    # ============================================================================
    # JOINT EMPLOYMENT AND STAFFING AGENCY LIABILITY
    # ============================================================================

    "staffing_agency_liability": {
        "topic": "staffing_agency_liability",
        "title": "Joint Employment, Staffing Agencies, and Co-Employment Liability",
        "category": "employment_relationships",
        "summary": "Joint employment and staffing agency arrangements create complex liability allocation questions under federal and state employment law. Under the FLSA, joint employment exists when: (1) two or more employers each employ a worker simultaneously (horizontal joint employment, e.g., employee working for two related companies), or (2) one employer provides workers to another employer where both exercise sufficient control (vertical joint employment, e.g., staffing agency and client company). The DOL's 2024 guidance applies an economic reality test for FLSA joint employment. Under Title VII and the ADA, courts use various tests: the common law control test (examining right to hire/fire, supervise, set schedules, determine pay, maintain records), the economic reality test, and hybrid tests. The NLRB applies its own joint employer standard, revised in 2023 (Cemex Construction Materials Pacific, LLC), to examine whether entities share or codetermine essential terms and conditions of employment (wages, benefits, hours, hiring, discharge, discipline, supervision, direction of work). For staffing agencies specifically: both the staffing firm (the employer of record) and the client company (the host employer) may be jointly liable for discrimination, wage violations, workplace safety, and other employment law obligations. The allocation depends on which entity exercises control over the relevant employment function. Practical implications: client companies that set schedules, direct daily work, determine pay rates, or make termination decisions are more likely to be found joint employers. Indemnification agreements between staffing firms and clients do not affect employee rights but can allocate liability between the entities. Texas courts follow federal joint employer analysis for claims under federal statutes and apply common law agency principles for state law claims. Professional Employer Organizations (PEOs): co-employment arrangements where PEO handles HR, payroll, and benefits while client retains operational control. Texas has a PEO licensing statute (Tex. Lab. Code Chapter 91) that specifically addresses the allocation of employer obligations in PEO arrangements.",
        "key_statutes": ["29 U.S.C. 203(d)-(e) (FLSA employer/employee definitions)", "29 C.F.R. 791.2 (FLSA joint employment regulation)", "29 U.S.C. 152(2) (NLRA employer definition)", "42 U.S.C. 2000e(b) (Title VII employer definition)", "Tex. Lab. Code Ch. 91 (Texas PEO licensing)", "29 U.S.C. 654(a) (OSHA employer obligations)"],
        "elements": ["Two or more entities involved in employment arrangement", "Both entities exercise control over workers (functional analysis)", "Control factors: hiring/firing, pay determination, supervision, work scheduling, discipline", "Worker performs services that benefit both entities", "Economic dependence analysis (FLSA) or common law control (Title VII/ADA)"],
        "defenses": ["No actual control over relevant employment decisions", "Contractual allocation of employer responsibilities (staffing agreement)", "Independent contractor relationship (not employee of either entity)", "PEO arrangement with statutory allocation under state law", "Limited involvement in day-to-day supervision", "Client company exercises no control over hiring, firing, pay, or discipline"],
        "remedies": ["Joint and several liability for wage and hour violations (FLSA)", "Joint and several liability for discrimination (Title VII/ADA)", "OSHA citations to both creating and controlling employers", "Workers compensation obligations for both entities", "Benefits obligations may extend to joint employers", "Staffing agency indemnification (contractual, not limiting employee rights)"],
        "leading_cases": ["Zheng v. Liberty Apparel Co., 355 F.3d 61 (2d Cir. 2003) (vertical joint employment)", "Browning-Ferris Industries of California, Inc., 362 NLRB 1599 (2015) (NLRB joint employer standard)", "Graves v. Lowery, 117 F.3d 723 (3d Cir. 1997) (staffing agency joint employment)", "Butler v. Drive Automotive Industries of America, Inc., 793 F.3d 404 (5th Cir. 2015) (Title VII joint employment in 5th Circuit)", "Moldenhauer v. Tazewell-Pekin Consolidated Communications Center, 536 F.3d 640 (7th Cir. 2008)"],
        "confidence": 0.86,
        "last_updated": "2026-01-15",
        "tags": ["joint_employer", "staffing_agency", "co_employment", "peo", "temporary_workers", "control_test", "economic_reality"],
    },

    # ============================================================================
    # EMPLOYMENT DISCRIMINATION BASED ON CRIMINAL HISTORY
    # ============================================================================

    "criminal_history_discrimination": {
        "topic": "criminal_history_discrimination",
        "title": "Criminal History Discrimination and Ban-the-Box Laws",
        "category": "discrimination",
        "summary": "Using criminal history in employment decisions implicates Title VII disparate impact analysis because criminal history screening disproportionately affects Black and Hispanic applicants. The EEOC's 2012 Enforcement Guidance on criminal records and employment establishes a framework requiring employers to conduct an individualized assessment using the Green v. Missouri Pacific Railroad factors: (1) the nature and gravity of the offense, (2) the time that has elapsed since the offense or completion of sentence, and (3) the nature of the job held or sought. Blanket policies excluding all applicants with criminal records are presumptively unlawful under disparate impact theory. Ban-the-box laws (also called fair chance hiring): over 37 states and 150 municipalities have enacted laws restricting when in the hiring process employers can inquire about criminal history. These generally prohibit criminal history questions on initial applications and delay background checks until after a conditional offer. Texas does NOT have a statewide ban-the-box law for private employers, but Austin passed a local ordinance in 2016 (later partially preempted by Texas Government Code Section 83.001, which prohibits cities from regulating private employer hiring practices). Federal contractors: Executive Order 11246 and OFCCP guidance address criminal history screening for federal contractors. Fair Credit Reporting Act (FCRA, 15 U.S.C. 1681): criminal background checks through third-party consumer reporting agencies must comply with FCRA requirements including: (1) standalone written disclosure to applicant, (2) written authorization from applicant, (3) pre-adverse action notice with copy of report and summary of rights, (4) reasonable waiting period (typically 5 business days), (5) adverse action notice with information about CRA and dispute rights. State and local variations: California (SB 731 - record sealing), New York (Article 23-A factors), Illinois (Employee Background Fairness Act), New Jersey (Opportunity to Compete Act). Expungement and record sealing may limit employer access to criminal records, but this varies significantly by jurisdiction.",
        "key_statutes": ["42 U.S.C. 2000e-2 (Title VII disparate impact)", "15 U.S.C. 1681 et seq. (Fair Credit Reporting Act)", "EEOC Enforcement Guidance on Criminal Records (April 25, 2012, updated 2023)", "Tex. Gov. Code 83.001 (preemption of local ban-the-box ordinances)", "Executive Order 11246 (federal contractor requirements)", "29 C.F.R. 60-1.3 (OFCCP regulations)"],
        "elements": ["Employment decision based in whole or part on criminal history", "Disparate impact: facially neutral policy with disproportionate effect on protected group", "Statistical evidence of disparate impact (EEOC data showing racial disparities)", "Failure to conduct individualized assessment using Green factors", "FCRA procedural violations (if third-party background check used)"],
        "defenses": ["Job-related and consistent with business necessity (Title VII)", "Individualized assessment using Green factors conducted", "Criminal history directly related to job duties (security, childcare, financial services)", "Federal, state, or local law requires exclusion based on certain convictions", "FCRA procedural compliance (proper disclosure, authorization, pre-adverse action notice)", "Employer relied on good faith compliance with published EEOC guidance"],
        "remedies": ["Title VII: reinstatement, back pay, compensatory damages (caps apply), punitive damages, attorneys fees", "FCRA: statutory damages ($100-$1,000 per violation), actual damages, punitive damages for willful violations, attorneys fees", "State fair chance law penalties (vary by jurisdiction)", "Injunctive relief (policy modification requirements)", "Class action exposure for pattern-or-practice screening policies"],
        "leading_cases": ["Green v. Missouri Pacific Railroad Co., 523 F.2d 1290 (8th Cir. 1975) (three-factor balancing test)", "El v. Southeastern Pennsylvania Transportation Authority, 479 F.3d 232 (3d Cir. 2007) (business necessity defense)", "EEOC v. Freeman, 778 F.3d 463 (4th Cir. 2015) (EEOC's statistical evidence insufficient)", "EEOC v. BMW Manufacturing Co., No. 13-cv-1583 (D.S.C. 2015) (consent decree for blanket criminal exclusion)", "Griggs v. Duke Power Co., 401 U.S. 424 (1971) (foundational disparate impact case)"],
        "confidence": 0.85,
        "last_updated": "2026-01-15",
        "tags": ["criminal_history", "ban_the_box", "fcra", "background_check", "disparate_impact", "green_factors", "fair_chance"],
    },

    # ============================================================================
    # EMPLOYMENT ARBITRATION AND CLASS/COLLECTIVE ACTION WAIVERS
    # ============================================================================

    "employment_arbitration_waivers": {
        "topic": "employment_arbitration_waivers",
        "title": "Mandatory Employment Arbitration and Class/Collective Action Waivers",
        "category": "dispute_resolution",
        "summary": "Mandatory arbitration agreements in employment have become pervasive, with over 60 million American workers subject to mandatory arbitration clauses. The Supreme Court in Epic Systems Corp. v. Lewis, 584 U.S. 497 (2018), held that the Federal Arbitration Act (FAA, 9 U.S.C. 1-16) permits employers to require employees to arbitrate disputes individually and waive the right to participate in class or collective actions, notwithstanding the NLRA's Section 7 protections for concerted activity. The Ending Forced Arbitration of Sexual Assault and Sexual Harassment Act of 2021 (EFAA, 9 U.S.C. 401-402) amends the FAA to invalidate pre-dispute arbitration agreements for claims of sexual assault or sexual harassment - the employee may elect to bring these claims in court regardless of any arbitration agreement. The EFAA applies at the election of the person alleging such conduct and applies to disputes arising on or after March 3, 2022. Key enforceability issues: (1) Unconscionability: procedural unconscionability (take-it-or-leave-it, no meaningful choice, buried in documents) plus substantive unconscionability (one-sided terms, excessive costs, limitation of remedies, shortened statute of limitations, discovery restrictions). Texas courts apply a two-prong unconscionability analysis and will sever unconscionable provisions if possible rather than voiding the entire agreement. (2) Adequate consideration: in Texas, continued at-will employment alone may be sufficient consideration if the agreement is bilateral (binding on both employer and employee). However, an employer's unilateral right to modify or terminate the arbitration agreement may render it illusory (In re Halliburton Co., 80 S.W.3d 566 (Tex. 2002)). (3) Delegation clauses: some arbitration agreements delegate the question of arbitrability itself to the arbitrator - courts generally enforce delegation clauses unless specifically challenged (Rent-A-Center, West, Inc. v. Jackson, 561 U.S. 63 (2010)). (4) Waiver of arbitration: a party that substantially invokes the litigation machinery may waive the right to compel arbitration (Morgan v. Sundance, Inc., 596 U.S. 411 (2022) - no prejudice requirement for waiver). (5) PAGA claims: in Adolph v. Uber Technologies, Inc., 14 Cal. 5th 1104 (2023), the California Supreme Court held that standing to bring representative PAGA claims survives arbitration of individual claims. Practical considerations for Texas employers: include clear opt-out period, bilateral obligation, AAA or JAMS rules reference, adequate discovery provisions, employer pays arbitrator costs, no limitation on statutory remedies, and compliance with EFAA.",
        "key_statutes": ["9 U.S.C. 1-16 (Federal Arbitration Act)", "9 U.S.C. 401-402 (EFAA - sexual assault/harassment exception)", "29 U.S.C. 216(b) (FLSA collective action waiver context)", "29 U.S.C. 157 (NLRA Section 7 - concerted activity)", "Tex. Civ. Prac. & Rem. Code Ch. 171 (Texas Arbitration Act)"],
        "elements": ["Valid arbitration agreement exists (offer, acceptance, consideration)", "Agreement covers the dispute at issue (scope analysis)", "Agreement is not unconscionable (procedural + substantive)", "Dispute is not exempt under EFAA (sexual assault/harassment claims)", "No waiver of right to arbitrate through litigation conduct"],
        "defenses": ["Unconscionability (procedural + substantive)", "Illusory agreement (employer unilateral modification right)", "EFAA exemption for sexual assault/harassment claims", "Waiver through substantial invocation of litigation process", "Agreement not supported by adequate consideration", "Transportation worker exemption from FAA (9 U.S.C. 1)", "State law defense applicable under FAA savings clause (9 U.S.C. 2)"],
        "remedies": ["Court order compelling arbitration (if agreement valid)", "Court order denying arbitration (if agreement unenforceable)", "Arbitration award (damages, reinstatement, fees as applicable under governing law)", "Judicial confirmation, modification, or vacatur of arbitration award (9 U.S.C. 9-11)", "Attorneys fees (per applicable substantive statute or arbitration agreement terms)"],
        "leading_cases": ["Epic Systems Corp. v. Lewis, 584 U.S. 497 (2018) (class/collective waivers enforceable)", "Morgan v. Sundance, Inc., 596 U.S. 411 (2022) (no prejudice required for waiver)", "Rent-A-Center, West, Inc. v. Jackson, 561 U.S. 63 (2010) (delegation clauses)", "In re Halliburton Co., 80 S.W.3d 566 (Tex. 2002) (illusory arbitration agreement)", "Lamps Plus, Inc. v. Varela, 587 U.S. 176 (2019) (no class arbitration without explicit agreement)", "AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011) (FAA preempts state law prohibiting class waivers)", "New Prime Inc. v. Oliveira, 586 U.S. 105 (2019) (transportation worker exemption)"],
        "confidence": 0.92,
        "last_updated": "2026-01-15",
        "tags": ["arbitration", "class_waiver", "faa", "efaa", "unconscionability", "epic_systems", "delegation_clause", "mandatory_arbitration"],
    },
}


# ============================================================================
# EMPLOYMENT DOCTRINE ENGINE
# ============================================================================

class EmploymentDoctrineEngine:
    """Engine for querying the employment law doctrine cache."""

    def __init__(self) -> None:
        """Initialize with the doctrine cache."""
        self._cache = DOCTRINE_CACHE
        self._topic_index: Dict[str, str] = {}
        self._category_index: Dict[str, List[str]] = defaultdict(list)
        self._tag_index: Dict[str, List[str]] = defaultdict(list)
        self._build_indexes()
        self._cache_hash = self._compute_cache_hash()
        logger.info("EmploymentDoctrineEngine initialized with {} doctrines, hash={}",
                     len(self._cache), self._cache_hash[:12])

    def _build_indexes(self) -> None:
        """Build lookup indexes from the doctrine cache."""
        for key, block in self._cache.items():
            topic = block["topic"]
            category = block.get("category", "general")
            tags = block.get("tags", [])
            self._topic_index[topic] = key
            self._category_index[category].append(key)
            for tag in tags:
                self._tag_index[tag].append(key)

    def _compute_cache_hash(self) -> str:
        """Compute SHA-256 hash of the entire doctrine cache."""
        cache_json = json.dumps(self._cache, sort_keys=True)
        return hashlib.sha256(cache_json.encode("utf-8")).hexdigest()

    def _get_confidence_band(self, confidence: float) -> str:
        """Map confidence score to a human-readable band."""
        if confidence >= 0.90:
            return "HIGH"
        if confidence >= 0.75:
            return "MEDIUM-HIGH"
        if confidence >= 0.60:
            return "MEDIUM"
        if confidence >= 0.40:
            return "LOW-MEDIUM"
        return "LOW"

    def lookup(self, topic: str) -> Optional[DoctrineResponse]:
        """Look up a doctrine by topic key."""
        start = time.monotonic()
        key = self._topic_index.get(topic)
        if key is None:
            # Try direct key lookup
            if topic in self._cache:
                key = topic
            else:
                return None

        block = self._cache[key]
        content_parts = [block.get("summary", "")]
        if block.get("elements"):
            content_parts.append("ELEMENTS: " + "; ".join(block["elements"]))
        if block.get("defenses"):
            content_parts.append("DEFENSES: " + "; ".join(block["defenses"]))
        if block.get("remedies"):
            content_parts.append("REMEDIES: " + "; ".join(block["remedies"]))

        content = "\n\n".join(content_parts)
        confidence = block.get("confidence", 0.5)

        det_hash = hashlib.sha256(
            f"{topic}:{content}:{confidence}".encode("utf-8")
        ).hexdigest()[:16]

        elapsed = (time.monotonic() - start) * 1000.0

        return DoctrineResponse(
            topic=block["topic"],
            title=block["title"],
            category=block.get("category", "general"),
            content=content,
            authority="; ".join(block.get("key_statutes", [])),
            confidence=confidence,
            confidence_band=self._get_confidence_band(confidence),
            citations=block.get("leading_cases", []),
            tags=block.get("tags", []),
            last_updated=block.get("last_updated", ""),
            determinism_hash=det_hash,
            response_time_ms=elapsed,
        )

    def search_by_category(self, category: str) -> List[DoctrineResponse]:
        """Get all doctrines in a category."""
        keys = self._category_index.get(category, [])
        results: List[DoctrineResponse] = []
        for key in keys:
            block = self._cache[key]
            resp = self.lookup(block["topic"])
            if resp:
                results.append(resp)
        return results

    def search_by_tag(self, tag: str) -> List[DoctrineResponse]:
        """Get all doctrines with a specific tag."""
        keys = self._tag_index.get(tag, [])
        results: List[DoctrineResponse] = []
        for key in keys:
            block = self._cache[key]
            resp = self.lookup(block["topic"])
            if resp:
                results.append(resp)
        return results

    def search_by_text(self, query: str, max_results: int = 10) -> List[DoctrineResponse]:
        """Simple text search across doctrine summaries."""
        query_lower = query.lower()
        scored: List[Tuple[float, str]] = []

        for key, block in self._cache.items():
            score = 0.0
            summary_lower = block.get("summary", "").lower()
            title_lower = block.get("title", "").lower()
            tags = " ".join(block.get("tags", [])).lower()
            statutes = " ".join(block.get("key_statutes", [])).lower()

            query_words = query_lower.split()
            for word in query_words:
                if word in title_lower:
                    score += 3.0
                if word in tags:
                    score += 2.0
                if word in statutes:
                    score += 1.5
                if word in summary_lower:
                    score += 1.0

            if score > 0:
                scored.append((score, key))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: List[DoctrineResponse] = []
        for _, key in scored[:max_results]:
            block = self._cache[key]
            resp = self.lookup(block["topic"])
            if resp:
                results.append(resp)
        return results

    def get_all_topics(self) -> List[str]:
        """Get all doctrine topics."""
        return sorted(self._topic_index.keys())

    def get_all_categories(self) -> List[str]:
        """Get all doctrine categories."""
        return sorted(self._category_index.keys())

    def get_category_counts(self) -> Dict[str, int]:
        """Get count of doctrines per category."""
        return {cat: len(keys) for cat, keys in self._category_index.items()}

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get doctrine cache statistics."""
        return {
            "total_doctrines": len(self._cache),
            "categories": self.get_category_counts(),
            "total_tags": len(self._tag_index),
            "cache_hash": self._cache_hash[:16],
            "avg_confidence": round(
                sum(b.get("confidence", 0.5) for b in self._cache.values()) / max(len(self._cache), 1), 4
            ),
        }

    def get_doctrine_block(self, topic: str) -> Optional[Dict[str, Any]]:
        """Get raw doctrine block data."""
        key = self._topic_index.get(topic, topic)
        return self._cache.get(key)

    def get_statutes_for_topic(self, topic: str) -> List[str]:
        """Get key statutes for a topic."""
        block = self.get_doctrine_block(topic)
        if block:
            return block.get("key_statutes", [])
        return []

    def get_elements_for_topic(self, topic: str) -> List[str]:
        """Get legal elements for a topic."""
        block = self.get_doctrine_block(topic)
        if block:
            return block.get("elements", [])
        return []

    def get_defenses_for_topic(self, topic: str) -> List[str]:
        """Get available defenses for a topic."""
        block = self.get_doctrine_block(topic)
        if block:
            return block.get("defenses", [])
        return []

    def get_remedies_for_topic(self, topic: str) -> List[str]:
        """Get available remedies for a topic."""
        block = self.get_doctrine_block(topic)
        if block:
            return block.get("remedies", [])
        return []

    def get_cases_for_topic(self, topic: str) -> List[str]:
        """Get leading cases for a topic."""
        block = self.get_doctrine_block(topic)
        if block:
            return block.get("leading_cases", [])
        return []

    def get_statutes_for_topic(self, topic: str) -> List[str]:
        """Get key statutes for a topic."""
        block = self.get_doctrine_block(topic)
        if block:
            return block.get("key_statutes", [])
        return []

    def get_confidence_for_topic(self, topic: str) -> float:
        """Get confidence score for a topic."""
        block = self.get_doctrine_block(topic)
        if block:
            return block.get("confidence", 0.0)
        return 0.0

    def get_high_confidence_doctrines(self, threshold: float = 0.90) -> List[DoctrineResponse]:
        """Get all doctrine blocks above a confidence threshold."""
        results: List[DoctrineResponse] = []
        for key, block in self._cache.items():
            if block.get("confidence", 0.0) >= threshold:
                resp = self.lookup(block["topic"])
                if resp:
                    results.append(resp)
        return sorted(results, key=lambda r: r.confidence, reverse=True)

    def get_doctrine_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the doctrine cache."""
        categories = self.get_category_counts()
        total = len(self._cache)
        avg_confidence = sum(b.get("confidence", 0.0) for b in self._cache.values()) / max(total, 1)
        all_statutes: set = set()
        all_cases: set = set()
        for block in self._cache.values():
            all_statutes.update(block.get("key_statutes", []))
            all_cases.update(block.get("leading_cases", []))
        return {
            "total_doctrines": total,
            "categories": categories,
            "average_confidence": round(avg_confidence, 3),
            "total_unique_statutes": len(all_statutes),
            "total_unique_cases": len(all_cases),
            "cache_hash": self._cache_hash[:16],
            "last_updated": max(
                (b.get("last_updated", "1970-01-01") for b in self._cache.values()),
                default="unknown",
            ),
        }


# ============================================================================
# MODULE-LEVEL SINGLETON AND CONVENIENCE FUNCTIONS
# ============================================================================

_engine: Optional[EmploymentDoctrineEngine] = None


def get_engine() -> EmploymentDoctrineEngine:
    """Get or create the global doctrine engine."""
    global _engine
    if _engine is None:
        _engine = EmploymentDoctrineEngine()
    return _engine


def get_doctrine_hash() -> str:
    """Get the doctrine cache integrity hash."""
    return get_engine()._cache_hash[:16]


def get_doctrine_count() -> int:
    """Get the total number of doctrine blocks."""
    return len(DOCTRINE_CACHE)
