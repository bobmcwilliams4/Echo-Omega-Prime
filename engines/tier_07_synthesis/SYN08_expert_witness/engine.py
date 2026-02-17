"""
SYN08 Expert Witness Preparation Engine v1.0.0
TIE-Grade Intelligence Engine for Expert Witness Analysis

Covers: Daubert/Frye admissibility, expert report requirements, methodology validation,
opinion scope, foundation requirements, cross-examination preparation, rebuttal analysis,
Rule 26 disclosure, deposition preparation, trial testimony support.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

ENGINE_ID = "SYN08"
ENGINE_NAME = "Expert Witness Preparation Engine"
VERSION = "1.0.0"
PORT = 9168

logger.add(f"{ENGINE_ID}_engine.log", rotation="100 MB", retention="30 days", level="INFO")

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
    ADMISSIBILITY = "ADMISSIBILITY"
    METHODOLOGY = "METHODOLOGY"
    QUALIFICATIONS = "QUALIFICATIONS"
    DISCLOSURE = "DISCLOSURE"
    FOUNDATION = "FOUNDATION"
    CROSS_EXAM = "CROSS_EXAM"
    REBUTTAL = "REBUTTAL"
    OPINION_SCOPE = "OPINION_SCOPE"
    ETHICS = "ETHICS"
    DEPOSITION = "DEPOSITION"

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
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    category: IssueCategory = IssueCategory.ADMISSIBILITY
    disclosure_caveat: str = ""

    def matches(self, query_lower: str, keywords_lower: List[str]) -> float:
        score = 0.0
        for kw in self.keywords:
            if kw.lower() in query_lower:
                score += 2.0
            for qkw in keywords_lower:
                if kw.lower() == qkw or kw.lower() in qkw or qkw in kw.lower():
                    score += 1.5
        if self.topic.lower() in query_lower:
            score += 3.0
        return score

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Daubert Standard Federal Admissibility",
        keywords=["daubert", "admissibility", "federal", "reliability", "scientific"],
        conclusion_template="Under Daubert v. Merrell Dow Pharmaceuticals, 509 U.S. 579 (1993), the trial judge serves as gatekeeper to exclude unreliable expert testimony. The proponent must show the expert's methodology is scientifically valid and reliably applied.",
        reasoning_framework="""1. FRE 702 sets baseline: qualified expert, reliable principles/methods, reliable application
2. Daubert factors (non-exhaustive): testability, peer review, error rate, standards/controls, general acceptance
3. Judge has discretion to admit/exclude based on totality of reliability indicia
4. Applies to scientific, technical, and other specialized knowledge per Kumho Tire
5. Proponent bears burden by preponderance of evidence""",
        key_factors=["Testability of theory", "Peer review publication", "Known/potential error rate", "Standards controlling operation", "General acceptance in field", "Qualifications of expert", "Fit between testimony and case facts"],
        primary_authority=["Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "FRE 702 (amended 2000, 2023)", "Kumho Tire v. Carmichael, 526 U.S. 137 (1999)", "General Electric v. Joiner, 522 U.S. 136 (1997)"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Opponent challenges methodology, application, qualifications, or relevance via Daubert motion",
        counter_arguments=["Expert testimony not truly scientific or technical", "Methodology developed solely for litigation", "Insufficient data or flawed application", "Opinion exceeds scope of expertise", "Alternative methodologies more reliable"],
        resolution_strategy="Submit detailed expert report, demonstrate methodology peer-reviewed or field-accepted, show error rates acceptable, prove reliable application to case facts, prepare for Daubert hearing with foundational testimony",
        entity_scope="Federal courts, FRE jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Black letter law, well-established gatekeeping standard",
        controlling_precedent="Daubert trilogy: Daubert, Joiner, Kumho Tire",
        category=IssueCategory.ADMISSIBILITY,
        disclosure_caveat="State variations exist; some states follow Frye instead"
    ),
    DoctrineBlock(
        topic="Frye General Acceptance Test",
        keywords=["frye", "general acceptance", "state", "scientific", "community"],
        conclusion_template="Under Frye v. United States, 293 F. 1013 (D.C. Cir. 1923), novel scientific evidence is admissible only if the methodology has gained general acceptance in the relevant scientific community.",
        reasoning_framework="""1. Focus on acceptance of methodology, not conclusions
2. Relevant community is the scientific field, not legal community
3. No specific factors; court assesses consensus
4. More conservative than Daubert; excludes cutting-edge techniques
5. Some states retain Frye despite FRE adoption""",
        key_factors=["General acceptance in field", "Peer review publication", "Use in non-litigation contexts", "Professional consensus", "Recognized standards or protocols"],
        primary_authority=["Frye v. United States, 293 F. 1013 (1923)", "State-specific codifications", "People v. Kelly, 17 Cal.3d 24 (1976) (California Frye-Kelly)"],
        burden_holder="Proponent of scientific evidence",
        adversary_position="Opponent argues methodology novel, unproven, or lacks consensus acceptance",
        counter_arguments=["Methodology too new to be generally accepted", "Field experts disagree on validity", "Technique used only by small subset", "Lacking independent verification"],
        resolution_strategy="Demonstrate methodology established in field via expert testimony, peer-reviewed studies, professional standards, textbooks, widespread use; avoid reliance on expert's ipse dixit",
        entity_scope="Federal courts pre-Daubert, some state courts (CA, FL, IL, MD, NY, PA, WA)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established but jurisdiction-specific",
        controlling_precedent="Frye v. United States",
        category=IssueCategory.ADMISSIBILITY,
        disclosure_caveat="Check state-specific rules; Daubert supersedes Frye in federal court"
    ),
    DoctrineBlock(
        topic="FRE 702 Expert Testimony Requirements",
        keywords=["rule 702", "expert", "qualified", "reliable", "helpful"],
        conclusion_template="FRE 702 permits expert testimony if: (a) specialized knowledge helps trier of fact; (b) expert qualified by knowledge/skill/experience/training/education; (c) testimony based on sufficient facts/data; (d) testimony product of reliable principles/methods; (e) expert reliably applied principles/methods to case facts.",
        reasoning_framework="""1. 2000 amendment codified Daubert reliability requirement
2. 2023 amendment requires proponent show by preponderance that expert's opinion reflects reliable application
3. All five prongs must be met
4. Qualified does not mean infallible; weight vs. admissibility
5. Judge may exclude even if some factors satisfied""",
        key_factors=["Helpfulness to jury", "Expert qualifications", "Sufficient factual basis", "Reliable methodology", "Reliable application", "Preponderance standard (2023)"],
        primary_authority=["FRE 702 (as amended 2023)", "Advisory Committee Notes 2000, 2023", "Daubert, Joiner, Kumho Tire trilogy"],
        burden_holder="Proponent by preponderance of evidence",
        adversary_position="Opponent challenges any of five elements; requests exclusion or limiting instruction",
        counter_arguments=["Expert unqualified in specific field", "Opinion based on insufficient data", "Methodology unreliable or novel", "Expert failed to reliably apply method", "Testimony not helpful or invades province of jury"],
        resolution_strategy="Prepare detailed CV, demonstrate expertise in relevant subfield, ensure opinion based on adequate investigation, use peer-reviewed methods, document reliable application, address 2023 amendment preponderance standard in briefing",
        entity_scope="Federal courts, states adopting FRE 702",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Codified rule, uniformly applied with Daubert gloss",
        controlling_precedent="FRE 702, Daubert trilogy",
        category=IssueCategory.ADMISSIBILITY,
        disclosure_caveat="2023 amendment raises bar; older case law may not reflect current standard"
    ),
    DoctrineBlock(
        topic="Kumho Tire Extension to Technical Experts",
        keywords=["kumho", "technical", "non-scientific", "tire", "engineer"],
        conclusion_template="Kumho Tire Co. v. Carmichael extended Daubert gatekeeping to all expert testimony, not just scientific. Technical and specialized knowledge must also satisfy reliability and fit requirements.",
        reasoning_framework="""1. Daubert factors not mandatory checklist; flexible approach
2. Trial judge has discretion to determine appropriate reliability factors for technical field
3. Experience-based testimony still subject to reliability scrutiny
4. Pure ipse dixit insufficient; must explain basis and methodology
5. Abuse of discretion standard on appeal""",
        key_factors=["Nature of issue", "Expert's particular expertise", "Type of testimony (scientific vs. experience-based)", "Daubert factors where applicable", "Other indicia of reliability"],
        primary_authority=["Kumho Tire v. Carmichael, 526 U.S. 137 (1999)", "FRE 702", "Advisory Committee Notes 2000"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Opponent argues technical opinion lacks foundation or reliable methodology",
        counter_arguments=["Expert relies solely on personal experience without methodology", "No objective verification of conclusions", "Lack of accepted standards in field", "Opinion contradicts established principles"],
        resolution_strategy="Articulate clear methodology even for experience-based opinions; explain reasoning process, cite industry standards or practices, demonstrate how experience translates to reliable opinion, avoid conclusory statements",
        entity_scope="Federal courts, FRE jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Supreme Court precedent, uniformly applied",
        controlling_precedent="Kumho Tire v. Carmichael",
        category=IssueCategory.ADMISSIBILITY,
        disclosure_caveat="Flexibility can lead to inconsistent application across judges"
    ),
    DoctrineBlock(
        topic="FRCP Rule 26(a)(2) Expert Disclosure",
        keywords=["rule 26", "disclosure", "expert report", "frcp", "written report"],
        conclusion_template="FRCP 26(a)(2)(B) requires expert witnesses retained or specially employed to provide written reports containing complete statement of opinions, bases, data considered, qualifications, compensation, and prior testimony.",
        reasoning_framework="""1. Disclosure mandatory unless stipulated otherwise or court-ordered exemption
2. Report must be signed by expert, not counsel
3. Timing per scheduling order or Rule 26(a)(2)(D) default (90 days before trial)
4. Failure to disclose = exclusion under Rule 37(c)(1) unless harmless
5. Supplements required if information incomplete or incorrect (Rule 26(e))""",
        key_factors=["Complete statement of opinions", "Bases and reasons for opinions", "Facts/data considered", "Exhibits to be used", "Expert qualifications", "Compensation", "Prior testimony (4 years)", "Timely disclosure"],
        primary_authority=["FRCP 26(a)(2)(B)", "FRCP 26(e) (supplementation)", "FRCP 37(c)(1) (exclusion sanction)", "Advisory Committee Notes"],
        burden_holder="Party designating expert witness",
        adversary_position="Opponent moves to exclude for insufficient or untimely disclosure",
        counter_arguments=["Report lacks detail on methodology", "Opinions not fully disclosed", "Data considered omitted", "Untimely disclosure or supplementation", "Expert report ghostwritten by counsel"],
        resolution_strategy="Draft comprehensive report early; ensure expert signs and owns opinions; disclose all bases and data; supplement promptly if opinions evolve; comply with scheduling order deadlines; maintain clear attorney-expert communication boundaries",
        entity_scope="Federal civil litigation, state courts with analogous rules",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mandatory procedural rule, strictly enforced",
        controlling_precedent="FRCP 26(a)(2)(B), case law on exclusion sanctions",
        category=IssueCategory.DISCLOSURE
    ),
    DoctrineBlock(
        topic="Expert Report Content Requirements",
        keywords=["expert report", "content", "opinions", "methodology", "data"],
        conclusion_template="An expert report must contain: (1) complete statement of all opinions; (2) bases and reasons for each opinion; (3) facts or data considered; (4) exhibits; (5) qualifications including publications; (6) list of cases with testimony in prior 4 years; (7) statement of compensation.",
        reasoning_framework="""1. Report serves as expert's direct testimony in written form
2. Prevents trial by ambush; opponent entitled to full disclosure
3. Opinions not in report generally excluded
4. Bases must explain why opinion reached, not just what opinion is
5. Data considered includes reviewed documents, depositions, interviews, tests""",
        key_factors=["Clarity and completeness", "Methodology explanation", "Alternative opinions considered and rejected", "Assumptions stated", "Limitations acknowledged", "Sufficient detail for rebuttal expert"],
        primary_authority=["FRCP 26(a)(2)(B)", "Daubert gatekeeping standards", "Sierra Club v. Cedar Point Oil Co., 73 F.3d 546 (5th Cir. 1996)", "Salgado v. General Motors, 150 F.3d 735 (7th Cir. 1998)"],
        burden_holder="Disclosing party and expert witness",
        adversary_position="Opponent scrutinizes for gaps, ambiguities, or undisclosed opinions to move for exclusion",
        counter_arguments=["Report too vague or conclusory", "Methodology not explained", "Data considered incomplete", "Opinions exceed scope of disclosed bases", "Supplementation inadequate"],
        resolution_strategy="Collaborate with expert early; ensure report self-contained and detailed; disclose all data considered even if not relied upon; explain methodology step-by-step; anticipate challenges and address weaknesses; supplement timely",
        entity_scope="Federal civil litigation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-defined procedural requirement",
        controlling_precedent="FRCP 26(a)(2)(B), circuit case law on sufficiency",
        category=IssueCategory.DISCLOSURE
    ),
    DoctrineBlock(
        topic="FRE 703 Basis of Expert Opinion",
        keywords=["rule 703", "basis", "facts", "data", "inadmissible", "hearsay"],
        conclusion_template="FRE 703 allows experts to base opinions on facts/data not admissible in evidence if of type reasonably relied upon by experts in the field. However, inadmissible underlying facts may not be disclosed to jury unless probative value substantially outweighs prejudicial effect.",
        reasoning_framework="""1. Experts can rely on hearsay, privileged materials, or otherwise inadmissible evidence
2. Rationale: experts in field routinely rely on such data (e.g., medical records, reports)
3. Expert may testify to opinion without disclosing inadmissible basis
4. If basis disclosed, court must balance FRE 403: probative value vs. prejudice
5. Opponent may object to disclosure of inadmissible hearsay as backdoor admission""",
        key_factors=["Type of data reasonably relied upon in field", "Probative value of disclosing basis", "Prejudicial effect of inadmissible evidence", "Limiting instruction feasibility", "Alternative admissible basis available"],
        primary_authority=["FRE 703 (amended 2000)", "Advisory Committee Notes 2000", "Daubert reliability requirement", "Williams v. Illinois, 567 U.S. 50 (2012)"],
        burden_holder="Proponent if seeking to disclose inadmissible basis; opponent if objecting",
        adversary_position="Opponent objects to disclosure of inadmissible hearsay or unreliable data as basis",
        counter_arguments=["Data not type reasonably relied upon", "Disclosure prejudicial and unnecessary", "Basis itself unreliable", "Expert acting as conduit for inadmissible evidence"],
        resolution_strategy="Identify admissible bases where possible; for inadmissible data, establish field custom of reliance; request limiting instruction; avoid unnecessary disclosure of prejudicial hearsay; challenge opponent's expert reliance on unreliable data",
        entity_scope="Federal courts, FRE jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established evidentiary rule with 2000 amendment clarification",
        controlling_precedent="FRE 703, Williams v. Illinois",
        category=IssueCategory.FOUNDATION,
        disclosure_caveat="Confrontation Clause concerns in criminal cases (Melendez-Diaz, Bullcoming)"
    ),
    DoctrineBlock(
        topic="Daubert Motion Practice and Timing",
        keywords=["daubert motion", "challenge", "timing", "pretrial", "hearing"],
        conclusion_template="Daubert challenges are typically raised via motion in limine before trial to exclude unreliable expert testimony. Courts hold evidentiary hearings to assess reliability under FRE 104(a). Untimely motions may be waived.",
        reasoning_framework="""1. Pretrial Daubert motion preserves objection and avoids trial disruption
2. Hearing under FRE 104(a): court determines admissibility as preliminary question
3. Proponent bears burden by preponderance to show reliability
4. Expert and opposing expert may testify at hearing
5. Court decision reviewed for abuse of discretion""",
        key_factors=["Timing per local rules or scheduling order", "Specificity of challenge", "Expert testimony at hearing", "Scientific literature and authorities cited", "Judicial notice of reliability"],
        primary_authority=["FRE 104(a)", "Daubert v. Merrell Dow", "Local rules re motion in limine timing", "General Electric v. Joiner (abuse of discretion standard)"],
        burden_holder="Proponent of expert testimony at hearing",
        adversary_position="Moving party seeks exclusion; cross-examines proponent's expert at hearing",
        counter_arguments=["Motion untimely or waived", "Challenge goes to weight not admissibility", "Reliability shown by preponderance", "Methodology generally accepted despite flaws"],
        resolution_strategy="File Daubert motion early per scheduling order; attach expert declaration or competing expert report; cite specific reliability defects; prepare for evidentiary hearing with expert testimony; respond to opponent's motion with detailed expert affidavit addressing challenges",
        entity_scope="Federal courts, state courts with Daubert-like gatekeeping",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard pretrial procedure in complex cases",
        controlling_precedent="Daubert, Joiner, local rules",
        category=IssueCategory.ADMISSIBILITY
    ),
    DoctrineBlock(
        topic="Qualifications of Expert Witness",
        keywords=["qualifications", "expert", "knowledge", "skill", "experience", "education"],
        conclusion_template="FRE 702 requires expert qualified by knowledge, skill, experience, training, or education. Qualifications must match the specific subject matter of testimony. Opposing counsel may voir dire on qualifications.",
        reasoning_framework="""1. Broad standard: any of five bases (knowledge, skill, experience, training, education)
2. Relevant experience more important than credentials alone
3. Expert need not be best qualified; weight vs. admissibility
4. Specialist within field may be required for narrow issues
5. Voir dire before jury hears substantive testimony""",
        key_factors=["Education and degrees", "Professional licenses/certifications", "Years of experience in field", "Publications and presentations", "Prior testimony experience", "Relevance to specific issue"],
        primary_authority=["FRE 702", "Daubert trilogy", "Kumho Tire (experience-based expertise)", "Circuit case law on qualifications challenges"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Opponent voir dires to expose lack of qualifications, moves to exclude",
        counter_arguments=["Expert lacks relevant experience in subfield", "Education insufficient for specialized topic", "No publications or peer recognition", "Professional discipline or censure", "Prior excluded testimony"],
        resolution_strategy="Vet expert credentials early; ensure CV current and accurate; match expert to specific issues; prepare expert for qualification voir dire; highlight relevant experience; address gaps proactively in direct examination",
        entity_scope="All courts applying FRE or similar rules",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Low threshold for qualifications; weight issue for jury",
        controlling_precedent="FRE 702, Kumho Tire",
        category=IssueCategory.QUALIFICATIONS
    ),
    DoctrineBlock(
        topic="Hypothetical Questions to Experts",
        keywords=["hypothetical", "question", "assume", "facts", "opinion"],
        conclusion_template="Experts may be asked hypothetical questions assuming facts in evidence or to be proven. Hypothetical must fairly represent evidence and not omit material facts. Opposing counsel may object if hypothetical misleading or unsupported.",
        reasoning_framework="""1. Hypothetical allows expert opinion when expert lacks personal knowledge of case facts
2. Attorney constructs hypothetical based on anticipated evidence
3. Expert assumes hypothetical facts true and opines accordingly
4. Opposing counsel cross-examines by altering hypothetical assumptions
5. Jury decides which set of assumed facts matches actual evidence""",
        key_factors=["Accuracy of assumed facts", "Inclusion of material facts", "Support in evidence or proffer", "Misleading omissions", "Expert understanding of assumptions"],
        primary_authority=["Common law tradition", "FRE 703 (expert may rely on inadmissible facts if reasonable)", "State-specific rules"],
        burden_holder="Proponent to ensure hypothetical supported by evidence",
        adversary_position="Opponent objects to unsupported or misleading hypothetical; cross-examines with alternative assumptions",
        counter_arguments=["Hypothetical omits key facts", "Assumptions contradicted by evidence", "Expert unfamiliar with factual nuances", "Hypothetical assumes disputed facts"],
        resolution_strategy="Draft hypothetical carefully including all material facts; ensure evidentiary support for each assumption; prepare expert to explain opinion based on hypothetical; anticipate opponent's cross-hypothetical; object to incomplete opponent hypotheticals",
        entity_scope="Common law jurisdictions, federal and state courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Traditional practice, well-established",
        controlling_precedent="Common law, FRE 703",
        category=IssueCategory.FOUNDATION
    ),
    DoctrineBlock(
        topic="Cross-Examination of Expert Witnesses",
        keywords=["cross-examination", "impeachment", "bias", "prior testimony", "treatise"],
        conclusion_template="Experts are subject to cross-examination on qualifications, methodology, bias, compensation, prior inconsistent testimony, and learned treatises under FRE 803(18). Effective cross-examination challenges reliability and credibility.",
        reasoning_framework="""1. Broad scope: qualifications, bases, methodology, assumptions, bias, fees
2. FRE 803(18): learned treatises admissible for impeachment if established as authoritative
3. Prior testimony from depositions or other cases may be used for impeachment
4. Financial interest and litigation consulting explored
5. Hypothetical variations test opinion robustness""",
        key_factors=["Expert's qualifications and experience", "Methodology employed", "Data considered and omitted", "Compensation and frequency of testifying", "Bias or financial interest", "Prior inconsistent statements", "Authoritative treatises contradicting opinion"],
        primary_authority=["FRE 803(18) (learned treatises)", "FRE 613 (prior statements)", "Daubert factors", "Common law cross-examination principles"],
        burden_holder="Cross-examiner to impeach; expert to maintain credibility",
        adversary_position="Expert defends methodology and conclusions; direct examiner rehabilitates on re-direct",
        counter_arguments=["Treatise not authoritative or out of context", "Prior testimony distinguishable", "Compensation reasonable and disclosed", "Methodology sound despite challenges"],
        resolution_strategy="Prepare expert for cross-examination on weaknesses; review prior testimony for consistency; disclose compensation and bias proactively; rehearse responses to treatise impeachment; identify authoritative treatises supporting your expert; cross-examine opponent expert with learned treatises contradicting their opinion",
        entity_scope="All courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core trial advocacy, well-established",
        controlling_precedent="FRE 803(18), FRE 613, common law",
        category=IssueCategory.CROSS_EXAM
    ),
    DoctrineBlock(
        topic="Rebuttal Expert Testimony",
        keywords=["rebuttal", "expert", "reply", "responsive", "surrebuttal"],
        conclusion_template="Rebuttal expert testimony is permitted to respond to opponent's expert evidence. Rebuttal must be genuinely responsive, not new affirmative evidence. Timing governed by scheduling orders and FRCP 26(a)(2)(D).",
        reasoning_framework="""1. Rebuttal evidence limited to scope of opponent's case-in-chief or expert opinions
2. Cannot introduce entirely new theories or opinions in rebuttal
3. FRCP 26(a)(2)(D)(ii): rebuttal expert disclosures due 30 days after opponent's disclosure
4. Court discretion to allow surrebuttal or exclude untimely rebuttal
5. Strategic choice: designate as case-in-chief expert vs. rebuttal expert""",
        key_factors=["Responsiveness to opponent's expert", "Timeliness of disclosure", "Prejudice to opponent", "New vs. responsive opinions", "Court's case management discretion"],
        primary_authority=["FRCP 26(a)(2)(D)(ii)", "FRE 611(a) (court control of evidence)", "Local rules and scheduling orders", "Circuit case law on rebuttal scope"],
        burden_holder="Party offering rebuttal expert",
        adversary_position="Opponent objects to untimely or non-responsive rebuttal testimony; moves to exclude",
        counter_arguments=["Rebuttal opinion not responsive", "New affirmative theory in guise of rebuttal", "Untimely disclosure", "Unfair surprise"],
        resolution_strategy="Disclose rebuttal expert timely per Rule 26(a)(2)(D)(ii); ensure opinions directly respond to opponent's expert; avoid new affirmative theories; request leave if timing issue; challenge opponent's rebuttal as exceeding scope; prepare case-in-chief expert to anticipate and preempt opponent's rebuttal",
        entity_scope="Federal civil litigation, state courts with similar rules",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Procedural rule, discretionary enforcement",
        controlling_precedent="FRCP 26(a)(2)(D)(ii), case law on rebuttal scope",
        category=IssueCategory.REBUTTAL
    ),
    DoctrineBlock(
        topic="Expert Deposition Preparation",
        keywords=["deposition", "expert", "preparation", "testimony", "video"],
        conclusion_template="Expert depositions are critical for discovering opinions, testing methodology, and locking in testimony. Experts must be thoroughly prepared on report content, methodology, and potential impeachment. Depositions often recorded for trial use.",
        reasoning_framework="""1. FRCP 26(b)(4)(A): expert deposition permitted after report disclosure
2. Expert deposition testimony admissible at trial as prior inconsistent statement or if expert unavailable
3. Attorney-expert communications generally protected; draft reports discoverable (FRCP 26(b)(4)(B)-(C))
4. Preparation crucial: expert must own opinions, not parrot counsel
5. Video deposition for trial presentation""",
        key_factors=["Thorough review of report and file", "Consistency with prior testimony", "Defense of methodology", "Handling of hypotheticals and alternative scenarios", "Disclosure of all bases", "Avoiding speculation beyond expertise"],
        primary_authority=["FRCP 26(b)(4)(A)", "FRCP 26(b)(4)(B)-(C) (privilege and work product)", "FRCP 32(a)(4) (use at trial)", "Local rules on deposition procedure"],
        burden_holder="Expert to testify consistently and credibly; attorney to prepare expert",
        adversary_position="Deposing counsel seeks inconsistencies, admissions, and impeachment material",
        counter_arguments=["Expert unprepared or inconsistent", "Deposition testimony contradicts report", "Expert speculates beyond expertise", "Coaching apparent"],
        resolution_strategy="Conduct mock deposition; review report line-by-line with expert; identify weaknesses and rehearse responses; ensure expert speaks in own words; instruct on objections and 'I don't know' acceptable answer; review prior deposition transcripts; prepare expert for video presentation",
        entity_scope="Federal and state civil litigation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard litigation practice",
        controlling_precedent="FRCP 26(b)(4), FRCP 32(a)(4)",
        category=IssueCategory.DEPOSITION
    ),
    DoctrineBlock(
        topic="Opinion Scope and Ultimate Issue",
        keywords=["opinion scope", "ultimate issue", "legal conclusion", "permitted", "helpful"],
        conclusion_template="FRE 704(a) permits expert opinions on ultimate issues to be decided by trier of fact, but FRE 704(b) prohibits experts in criminal cases from opining on defendant's mental state. Opinions must be helpful and not mere legal conclusions.",
        reasoning_framework="""1. FRE 704(a): ultimate issue opinions allowed in civil cases and most criminal issues
2. FRE 704(b): criminal mental state opinions excluded (insanity, intent, etc.)
3. Expert may not simply state legal conclusion (e.g., 'contract breached')
4. Opinion must apply expertise to facts, not recite law
5. Helpfulness requirement: opinion must assist jury beyond common knowledge""",
        key_factors=["Civil vs. criminal case", "Opinion on mental state (criminal)", "Legal conclusion vs. expert analysis", "Helpfulness to jury", "Invading province of jury"],
        primary_authority=["FRE 704(a)", "FRE 704(b)", "FRE 702 (helpfulness requirement)", "United States v. Bilzerian, 926 F.2d 1285 (2d Cir. 1991)"],
        burden_holder="Proponent to show opinion helpful and not improper legal conclusion",
        adversary_position="Opponent objects to legal conclusions or unhelpful opinions",
        counter_arguments=["Opinion merely states legal standard", "Expert usurps jury function", "Opinion on ultimate issue not helpful", "Criminal mental state opinion improper"],
        resolution_strategy="Frame expert opinion as application of expertise to facts, not legal conclusion; avoid reciting law or elements of claim; focus on technical, scientific, or specialized analysis; in criminal cases, avoid mental state opinions; challenge opponent's expert for improper legal conclusions",
        entity_scope="Federal courts, FRE jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established rule with narrow criminal exception",
        controlling_precedent="FRE 704(a), FRE 704(b)",
        category=IssueCategory.OPINION_SCOPE
    ),
    DoctrineBlock(
        topic="Expert Witness Immunity and Ethics",
        keywords=["immunity", "ethics", "liability", "malpractice", "perjury"],
        conclusion_template="Expert witnesses generally enjoy absolute immunity from civil liability for testimony given in judicial proceedings. However, experts remain subject to perjury prosecution, ethical rules, and potential sanctions for misconduct.",
        reasoning_framework="""1. Absolute immunity for testimony: protects expert from defamation and negligence claims
2. Immunity does not extend to pre-testimony consulting or non-testimonial conduct
3. Perjury: knowingly false testimony is criminal offense
4. Professional ethics: experts bound by field-specific ethical codes
5. Court sanctions: Rule 37(c)(1) exclusion, attorney fee awards for discovery abuse""",
        key_factors=["Testimonial vs. consulting conduct", "Knowingly false statements", "Professional discipline risk", "Court-imposed sanctions", "Reputational consequences"],
        primary_authority=["Briscoe v. LaHue, 460 U.S. 325 (1983) (witness immunity)", "18 U.S.C. 1621 (perjury)", "Professional codes of ethics (medical, engineering, etc.)", "FRCP 37(c)(1) (sanctions)"],
        burden_holder="Expert to comply with ethical duties; party to avoid sanctionable conduct",
        adversary_position="Opponent may report ethical violations to professional boards or seek sanctions",
        counter_arguments=["Immunity does not protect unethical conduct", "Expert's reputation suffers from bias or false testimony", "Professional discipline separate from legal immunity"],
        resolution_strategy="Vet expert for ethical violations or disciplinary history; ensure expert testifies truthfully and within scope of expertise; avoid hiring 'hired gun' experts with history of excluded testimony; report egregious expert misconduct to court or professional boards; maintain expert independence to avoid sanctions",
        entity_scope="All U.S. jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established immunity doctrine with ethical overlay",
        controlling_precedent="Briscoe v. LaHue, perjury statutes, professional ethics codes",
        category=IssueCategory.ETHICS
    ),
    DoctrineBlock(
        topic="Testability and Falsifiability Daubert Factor",
        keywords=["testability", "falsifiability", "hypothesis", "popper", "scientific method"],
        conclusion_template="A key Daubert factor is whether the expert's theory or technique can be and has been tested. Karl Popper's falsifiability criterion is relevant: scientific theories must be capable of empirical refutation.",
        reasoning_framework="""1. Scientific method requires hypothesis testing
2. Unfalsifiable theories not scientific (e.g., astrology, psychoanalysis)
3. Expert must explain how methodology tested or could be tested
4. Testing need not be perfect; existence of testing mechanism relevant
5. Untestable opinions may be excluded as unreliable""",
        key_factors=["Hypothesis formulation", "Empirical testing conducted", "Potential for testing if not yet done", "Results replicable", "Methodology falsifiable"],
        primary_authority=["Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "Karl Popper, The Logic of Scientific Discovery (1959)", "FRE 702"],
        burden_holder="Proponent to show methodology testable",
        adversary_position="Opponent challenges untestable or unfalsifiable methodology",
        counter_arguments=["Methodology not testable in principle", "No testing conducted despite feasibility", "Results not replicable", "Theory ad hoc or post hoc rationalization"],
        resolution_strategy="Demonstrate methodology tested via experiments, studies, or field trials; cite peer-reviewed testing; explain how theory could be falsified; acknowledge testing limitations; challenge opponent's untested methodology as unreliable",
        entity_scope="Federal courts, Daubert jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core Daubert factor, scientifically grounded",
        controlling_precedent="Daubert, scientific literature on falsifiability",
        category=IssueCategory.METHODOLOGY
    ),
    DoctrineBlock(
        topic="Peer Review and Publication Daubert Factor",
        keywords=["peer review", "publication", "journal", "scientific community", "daubert"],
        conclusion_template="Publication in peer-reviewed journals is a significant Daubert factor indicating reliability. Peer review subjects methodology to scrutiny by qualified scientists, though publication is not dispositive.",
        reasoning_framework="""1. Peer review process filters unreliable methodologies
2. Publication demonstrates acceptance by scientific community
3. Lack of publication not fatal if methodology well-established or new
4. 'Litigation science' developed solely for case is suspect
5. Court assesses quality and relevance of publications""",
        key_factors=["Number and quality of peer-reviewed publications", "Reputation of journals", "Peer review process rigor", "Publication recency", "Citations by other researchers"],
        primary_authority=["Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "FRE 702", "General Electric v. Joiner, 522 U.S. 136 (1997)"],
        burden_holder="Proponent to establish publication record or explain absence",
        adversary_position="Opponent challenges lack of peer review or reliance on unpublished methodology",
        counter_arguments=["Methodology unpublished and untested by peers", "Publications in low-quality or non-peer-reviewed outlets", "Expert's opinions contradict published research", "Litigation-driven methodology"],
        resolution_strategy="Cite peer-reviewed publications supporting methodology; demonstrate expert's own publication record; explain if methodology new or proprietary; distinguish litigation consulting from sound methodology; challenge opponent's reliance on unpublished or non-peer-reviewed sources",
        entity_scope="Federal courts, Daubert jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Daubert factor, strong indicator of reliability",
        controlling_precedent="Daubert, Joiner",
        category=IssueCategory.METHODOLOGY
    ),
    DoctrineBlock(
        topic="Known or Potential Error Rate Daubert Factor",
        keywords=["error rate", "accuracy", "false positive", "false negative", "reliability"],
        conclusion_template="Daubert considers the known or potential error rate of the methodology. Low error rates enhance reliability; high or unknown error rates may justify exclusion.",
        reasoning_framework="""1. Error rate measures methodology's accuracy and precision
2. Expert must know and disclose error rate or explain why unknown
3. Different methodologies have different acceptable error rates
4. False positives vs. false negatives depending on field
5. Absence of error rate data may indicate unreliable or novel technique""",
        key_factors=["Empirical error rate studies", "Statistical significance", "Confidence intervals", "Field-specific acceptable error thresholds", "Error rate disclosure"],
        primary_authority=["Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "FRE 702", "Kumho Tire v. Carmichael, 526 U.S. 137 (1999)"],
        burden_holder="Proponent to establish acceptable error rate",
        adversary_position="Opponent challenges high, unknown, or undisclosed error rate",
        counter_arguments=["Error rate unknown or undisclosed", "Error rate unacceptably high for purpose", "No validation studies conducted", "Methodology unreliable due to error rate"],
        resolution_strategy="Cite validation studies with error rate data; explain acceptable error rate in field; disclose limitations and confidence intervals; if error rate unknown, explain methodology still reliable based on other factors; challenge opponent's methodology for lack of error rate validation",
        entity_scope="Federal courts, Daubert jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Daubert factor, empirical reliability measure",
        controlling_precedent="Daubert, Kumho Tire",
        category=IssueCategory.METHODOLOGY
    ),
    DoctrineBlock(
        topic="Standards and Controls Daubert Factor",
        keywords=["standards", "controls", "protocols", "daubert", "methodology"],
        conclusion_template="Existence of standards controlling the technique's operation is a Daubert reliability factor. Recognized protocols and industry standards enhance confidence in methodology.",
        reasoning_framework="""1. Standards provide objective criteria for methodology application
2. Industry standards (ASTM, ISO, NIST, etc.) indicate field acceptance
3. Controls in experimental design ensure validity (positive/negative controls)
4. Deviation from standards must be explained
5. Absence of standards not fatal if methodology otherwise reliable""",
        key_factors=["Published standards (ASTM, ISO, NIST, etc.)", "Industry best practices", "Professional protocols", "Experimental controls", "Adherence to standards"],
        primary_authority=["Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "FRE 702", "Industry standard-setting organizations (ASTM, ISO, NIST)"],
        burden_holder="Proponent to establish compliance with standards",
        adversary_position="Opponent challenges deviation from standards or absence of controls",
        counter_arguments=["No recognized standards exist", "Expert deviated from established protocols", "Lack of experimental controls", "Standards not followed or inapplicable"],
        resolution_strategy="Cite applicable industry standards; demonstrate methodology complies with standards; explain any deviations as reasonable; use experimental controls in testing; challenge opponent's failure to follow standards or lack of controls in methodology",
        entity_scope="Federal courts, Daubert jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Daubert factor, objective reliability measure",
        controlling_precedent="Daubert, industry standards",
        category=IssueCategory.METHODOLOGY
    ),
    DoctrineBlock(
        topic="General Acceptance in Scientific Community",
        keywords=["general acceptance", "scientific community", "consensus", "daubert", "frye"],
        conclusion_template="General acceptance in the relevant scientific community is a key Daubert factor and the sole Frye test. Widespread acceptance indicates reliability, though novel techniques may be admissible under Daubert.",
        reasoning_framework="""1. Daubert: general acceptance important but not dispositive
2. Frye: general acceptance is sole test
3. Relevant community is field of expertise, not general public
4. Novel methodologies may be reliable despite lack of widespread acceptance
5. Expert must demonstrate acceptance via publications, professional consensus, standards""",
        key_factors=["Peer-reviewed publications", "Professional organization endorsements", "Textbook inclusion", "Judicial acceptance in other cases", "Expert testimony from field"],
        primary_authority=["Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "Frye v. United States, 293 F. 1013 (1923)", "FRE 702"],
        burden_holder="Proponent to establish general acceptance",
        adversary_position="Opponent challenges lack of acceptance or novel methodology",
        counter_arguments=["Methodology not generally accepted", "Rejected by mainstream science", "Only fringe experts support methodology", "Novel and unproven"],
        resolution_strategy="Cite peer-reviewed literature showing acceptance; present expert testimony from field leaders; demonstrate textbook inclusion or professional endorsements; distinguish novelty from unreliability; in Frye jurisdictions, focus heavily on general acceptance; challenge opponent's methodology as fringe or discredited",
        entity_scope="Federal courts (Daubert factor), Frye jurisdictions (sole test)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established reliability factor",
        controlling_precedent="Daubert, Frye",
        category=IssueCategory.METHODOLOGY
    ),
    DoctrineBlock(
        topic="Relevance and Fit Requirement",
        keywords=["relevance", "fit", "helpful", "daubert", "rule 702"],
        conclusion_template="Under Daubert and FRE 702, expert testimony must be relevant and fit the facts of the case. Reliable methodology applied to irrelevant facts is inadmissible.",
        reasoning_framework="""1. Reliability alone insufficient; testimony must assist trier of fact
2. Fit requirement: methodology must apply to specific case facts and issues
3. Expert cannot opine on facts not in evidence or outside case scope
4. Helpfulness requirement: testimony beyond common knowledge
5. General causation vs. specific causation in toxic tort cases""",
        key_factors=["Applicability to case facts", "Assistance to jury", "Connection between methodology and legal issues", "Specificity of opinion", "Avoid speculation"],
        primary_authority=["Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "FRE 702", "FRE 401, 402 (relevance)"],
        burden_holder="Proponent to show relevance and fit",
        adversary_position="Opponent challenges testimony as irrelevant or unhelpful",
        counter_arguments=["Testimony does not fit case facts", "Methodology inapplicable to specific issue", "Opinion too general or speculative", "Not helpful to jury"],
        resolution_strategy="Ensure expert opinion directly addresses case issues; tie methodology to specific facts in evidence; avoid overly general or abstract opinions; demonstrate how opinion assists jury beyond common knowledge; challenge opponent's expert for lack of fit or relevance",
        entity_scope="Federal courts, FRE jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core Daubert and FRE 702 requirement",
        controlling_precedent="Daubert, FRE 702, FRE 401-402",
        category=IssueCategory.ADMISSIBILITY
    ),
    DoctrineBlock(
        topic="Supplementation of Expert Disclosures",
        keywords=["supplementation", "rule 26(e)", "new opinions", "correct", "update"],
        conclusion_template="FRCP 26(e) requires parties to supplement expert disclosures if information is incomplete or incorrect, or if additional opinions are formed. Failure to supplement may result in exclusion under Rule 37(c)(1).",
        reasoning_framework="""1. Duty to supplement arises if report incomplete, incorrect, or superseded
2. New opinions formed before trial must be disclosed
3. Timing: seasonably supplement, typically before discovery cutoff or as ordered
4. Supplementation must be timely to avoid exclusion sanction
5. Opponent entitled to depose expert on supplemental opinions""",
        key_factors=["Material new information", "Timeliness of supplementation", "Prejudice to opponent", "Good faith vs. gamesmanship", "Opportunity for opponent to depose"],
        primary_authority=["FRCP 26(e)(2)", "FRCP 37(c)(1) (exclusion sanction)", "Advisory Committee Notes", "Circuit case law on timeliness"],
        burden_holder="Disclosing party to supplement promptly",
        adversary_position="Opponent moves to exclude untimely supplemental opinions",
        counter_arguments=["Supplementation untimely", "New opinions unfairly surprise opponent", "Failure to supplement incomplete report", "Bad faith delay"],
        resolution_strategy="Monitor expert's evolving opinions; supplement promptly upon new information; provide detailed supplemental disclosures; allow opponent time to depose on supplementation; challenge opponent's untimely or inadequate supplementation; seek exclusion of undisclosed opinions",
        entity_scope="Federal civil litigation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mandatory procedural duty, strictly enforced",
        controlling_precedent="FRCP 26(e), FRCP 37(c)(1)",
        category=IssueCategory.DISCLOSURE
    ),
    DoctrineBlock(
        topic="Exclusion of Expert Testimony as Sanction",
        keywords=["exclusion", "sanction", "rule 37", "untimely", "violation"],
        conclusion_template="FRCP 37(c)(1) mandates exclusion of expert testimony not properly disclosed unless failure was substantially justified or harmless. Exclusion is automatic absent justification or harmlessness.",
        reasoning_framework="""1. Self-executing sanction: court must exclude unless exception met
2. Party opposing exclusion bears burden to show substantial justification or harmlessness
3. Substantial justification: good faith, reasonable basis for non-disclosure
4. Harmlessness: no prejudice to opponent, curative measures available
5. Exclusion may extend to entire expert or specific opinions""",
        key_factors=["Timeliness and completeness of disclosure", "Prejudice to opponent", "Good faith of disclosing party", "Availability of curative measures (continuance, additional deposition)", "Importance of excluded testimony"],
        primary_authority=["FRCP 37(c)(1)", "Advisory Committee Notes", "Goodman v. Staples The Office Superstore, LLC, 644 F.3d 817 (9th Cir. 2011)"],
        burden_holder="Party opposing exclusion to show substantial justification or harmlessness",
        adversary_position="Moving party seeks exclusion; argues prejudice and lack of justification",
        counter_arguments=["Disclosure timely and complete", "No prejudice to opponent", "Substantial justification for any delay", "Harmless error, curative measures available"],
        resolution_strategy="Ensure timely and complete disclosures to avoid sanctions; if disclosure defective, promptly supplement and seek leave; argue harmlessness and offer curative measures (continuance, additional deposition); challenge opponent's late or incomplete disclosures; move for exclusion of undisclosed opinions",
        entity_scope="Federal civil litigation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strict procedural sanction, narrowly construed exceptions",
        controlling_precedent="FRCP 37(c)(1), circuit case law on exclusion",
        category=IssueCategory.DISCLOSURE
    ),
    DoctrineBlock(
        topic="Court-Appointed Experts Under FRE 706",
        keywords=["rule 706", "court-appointed", "neutral expert", "special master", "independent"],
        conclusion_template="FRE 706 allows courts to appoint independent experts on their own or on party motion. Court-appointed experts are neutral and may be questioned by all parties. Appointment is discretionary.",
        reasoning_framework="""1. Court may appoint expert on complex or technical issues
2. Expert selected by court, compensated by parties or as court directs
3. Expert's report disclosed to all parties
4. Parties may depose and cross-examine court-appointed expert
5. Jury informed of court appointment (may give expert's testimony weight)""",
        key_factors=["Complexity of issue", "Conflicting party experts", "Need for neutral opinion", "Cost allocation", "Impact on jury"],
        primary_authority=["FRE 706", "Advisory Committee Notes", "Case law on court-appointed experts"],
        burden_holder="Court to determine necessity and select qualified expert",
        adversary_position="Parties may agree or object to appointment; cross-examine appointed expert",
        counter_arguments=["Appointment unnecessary given party experts", "Appointed expert biased or unqualified", "Unfair weight given to court expert"],
        resolution_strategy="Request court-appointed expert if party experts deadlocked or issue highly technical; vet proposed expert for qualifications and neutrality; depose court expert thoroughly; cross-examine on methodology and conclusions; argue appointed expert not infallible",
        entity_scope="Federal courts, states with FRE 706 equivalent",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Discretionary procedural tool, infrequently used",
        controlling_precedent="FRE 706",
        category=IssueCategory.ADMISSIBILITY
    ),
    DoctrineBlock(
        topic="Treating Physician as Expert Witness",
        keywords=["treating physician", "expert", "medical", "opinion", "disclosure"],
        conclusion_template="Treating physicians may testify as expert witnesses about diagnosis, treatment, and prognosis. FRCP 26(a)(2)(C) exempts treating physicians from written report requirement but requires disclosure of opinions and bases.",
        reasoning_framework="""1. Treating physician qualifies as expert re: patient's medical condition
2. May opine on causation, disability, future treatment needs
3. No written report required under Rule 26(a)(2)(C)
4. Must disclose subject matter and summary of opinions and bases
5. Deposition permitted; testimony subject to Daubert/FRE 702""",
        key_factors=["Treatment relationship with patient", "Opinions formed during treatment vs. for litigation", "Disclosure of opinions and bases", "Deposition testimony", "Daubert reliability if causation opinion"],
        primary_authority=["FRCP 26(a)(2)(C)", "FRE 702", "Daubert trilogy", "State medical expert rules"],
        burden_holder="Proponent to disclose treating physician opinions; physician to provide reliable opinions",
        adversary_position="Opponent may depose and challenge treating physician's opinions as unreliable or litigation-driven",
        counter_arguments=["Treating physician acting as hired expert, not solely treating", "Opinions not formed during treatment", "Causation opinion unreliable or unsupported", "Inadequate disclosure of bases"],
        resolution_strategy="Distinguish treatment-based opinions (admissible) from litigation-driven opinions (require full report); ensure treating physician discloses all opinions and bases per Rule 26(a)(2)(C); prepare treating physician for deposition; challenge opponent's treating physician if opinions exceed treatment scope or lack reliability",
        entity_scope="Federal civil litigation, personal injury and medical malpractice cases",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established exception to full report requirement",
        controlling_precedent="FRCP 26(a)(2)(C), FRE 702",
        category=IssueCategory.DISCLOSURE
    ),
    DoctrineBlock(
        topic="Ipse Dixit Rejection and Explained Methodology",
        keywords=["ipse dixit", "because i said so", "methodology", "explanation", "joiner"],
        conclusion_template="General Electric v. Joiner held that expert testimony based solely on the expert's say-so (ipse dixit) without explained methodology is insufficient. Experts must articulate reasoning and methodological basis.",
        reasoning_framework="""1. Ipse dixit = unsupported assertion, 'because I said so'
2. Expert must explain how methodology leads to conclusion
3. Experience-based opinions require articulated reasoning process
4. Joiner: analytical gap between data and conclusion warrants exclusion
5. Conclusory affidavits insufficient to defeat summary judgment or Daubert motion""",
        key_factors=["Explanation of reasoning", "Connection between data and conclusion", "Methodological steps articulated", "Avoidance of bare conclusions", "Transparency of analysis"],
        primary_authority=["General Electric v. Joiner, 522 U.S. 136 (1997)", "Daubert v. Merrell Dow, 509 U.S. 579 (1993)", "FRE 702"],
        burden_holder="Proponent to ensure expert explains methodology",
        adversary_position="Opponent challenges ipse dixit opinions as unreliable",
        counter_arguments=["Expert fails to explain reasoning", "Analytical gap between data and opinion", "Conclusory statements without support", "Methodology opaque or missing"],
        resolution_strategy="Require expert to articulate step-by-step reasoning in report and testimony; avoid conclusory statements; ensure expert explains how data supports opinion; challenge opponent's expert for ipse dixit; cite Joiner to exclude unsupported opinions",
        entity_scope="Federal courts, FRE jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established anti-ipse dixit principle",
        controlling_precedent="Joiner, Daubert",
        category=IssueCategory.METHODOLOGY
    )
]

class QueryRequest(BaseModel):
    query: str = Field(..., description="Legal query regarding expert witness preparation")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    session_id: Optional[str] = Field(default=None, description="Session tracking ID")

class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    reasoning_chain: List[str]
    authority_citations: List[str]
    determinism_hash: str
    latency_ms: float
    session_id: Optional[str]

@dataclass
class TelemetryRecord:
    timestamp: str
    query: str
    mode: str
    zone: str
    triggered_doctrines: List[str]
    latency_ms: float
    confidence: str
    error: Optional[str] = None

class ExpertWitnessEngine:
    def __init__(self):
        self.telemetry: List[TelemetryRecord] = []
        self.query_count = 0
        self.error_count = 0
        self.doctrine_hit_counts: Counter = Counter()
        self.coverage_triggered: set = set()
        self.coverage_total = len(DOCTRINE_CACHE)
        logger.info(f"{ENGINE_NAME} v{VERSION} initialized with {self.coverage_total} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> Dict[str, Any]:
        start_time = time.time()
        query_lower = query.lower()
        keywords_lower = query_lower.split()

        scored_blocks = []
        for block in DOCTRINE_CACHE:
            score = block.matches(query_lower, keywords_lower)
            if score > 0:
                scored_blocks.append((score, block))

        scored_blocks.sort(reverse=True, key=lambda x: x[0])
        top_blocks = [b for s, b in scored_blocks[:5]]

        triggered_topics = [b.topic for b in top_blocks]
        for topic in triggered_topics:
            self.doctrine_hit_counts[topic] += 1
            self.coverage_triggered.add(topic)

        if top_blocks and scored_blocks[0][0] >= 3.0:
            answer, reasoning, authorities, confidence = self._build_from_cache(top_blocks, mode, zone)
        else:
            answer, reasoning, authorities, confidence = self._semantic_search(query, mode, zone)

        latency_ms = (time.time() - start_time) * 1000

        self.telemetry.append(TelemetryRecord(
            timestamp=datetime.utcnow().isoformat(),
            query=query,
            mode=mode.value,
            zone=zone.value,
            triggered_doctrines=triggered_topics,
            latency_ms=latency_ms,
            confidence=confidence.value
        ))
        self.query_count += 1

        return {
            "answer": answer,
            "reasoning_chain": reasoning,
            "authority_citations": authorities,
            "triggered_doctrines": triggered_topics,
            "confidence": confidence,
            "latency_ms": latency_ms
        }

    def _build_from_cache(self, blocks: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> tuple:
        primary = blocks[0]

        if mode == ResponseMode.FAST:
            answer = f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}."
            reasoning = [primary.reasoning_framework.split('\n')[0]]
        elif mode == ResponseMode.DEFENSE:
            answer = f"{primary.conclusion_template}\n\nAnalysis:\n{primary.reasoning_framework}\n\n"
            answer += f"Authority: {'; '.join(primary.primary_authority[:2])}\n\n"
            answer += f"Risk: {primary.adversary_position}\n\nStrategy: {primary.resolution_strategy}"
            reasoning = primary.reasoning_framework.split('\n')
        else:
            answer = f"EXPERT WITNESS ANALYSIS MEMORANDUM\n\n{primary.conclusion_template}\n\n"
            answer += f"REASONING:\n{primary.reasoning_framework}\n\n"
            answer += f"KEY FACTORS:\n" + "\n".join(f"- {kf}" for kf in primary.key_factors) + "\n\n"
            answer += f"AUTHORITY:\n" + "\n".join(f"- {auth}" for auth in primary.primary_authority) + "\n\n"
            answer += f"ADVERSARY POSITION: {primary.adversary_position}\n\n"
            answer += f"COUNTER-ARGUMENTS:\n" + "\n".join(f"- {ca}" for ca in primary.counter_arguments) + "\n\n"
            answer += f"STRATEGY: {primary.resolution_strategy}\n\n"
            if primary.disclosure_caveat:
                answer += f"DISCLOSURE: {primary.disclosure_caveat}\n\n"
            if len(blocks) > 1:
                answer += "RELATED CONSIDERATIONS:\n"
                for b in blocks[1:3]:
                    answer += f"- {b.topic}: {b.conclusion_template[:150]}...\n"
            reasoning = primary.reasoning_framework.split('\n') + [f"Related: {b.topic}" for b in blocks[1:3]]

        authorities = primary.primary_authority + [b.controlling_precedent for b in blocks[1:3]]

        if zone == AnalysisZone.AUDIT:
            answer += f"\n\n[AUDIT TRAIL: Triggered {len(blocks)} doctrines. Primary: {primary.topic}. Confidence: {primary.confidence.value}]"

        return answer, reasoning, authorities, primary.confidence

    def _semantic_search(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> tuple:
        answer = "Expert witness preparation requires careful analysis of admissibility standards (Daubert/Frye), methodology validation, proper disclosure under FRCP 26, and thorough preparation for deposition and trial testimony. Consult specific doctrine blocks for detailed analysis."
        reasoning = ["Semantic search fallback: no high-scoring doctrine cache hit", "General expert witness principles apply"]
        authorities = ["FRE 702", "FRCP 26(a)(2)", "Daubert v. Merrell Dow, 509 U.S. 579 (1993)"]
        confidence = ConfidenceLevel.DISCLOSURE
        return answer, reasoning, authorities, confidence

    def generate_determinism_hash(self, query: str, answer: str, mode: str) -> str:
        content = f"{query}|{answer}|{mode}|{VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()

    def health_check(self) -> Dict[str, Any]:
        coverage_pct = (len(self.coverage_triggered) / self.coverage_total * 100) if self.coverage_total > 0 else 0
        avg_latency = sum(t.latency_ms for t in self.telemetry[-100:]) / len(self.telemetry[-100:]) if self.telemetry else 0

        return {
            "status": "operational",
            "engine_id": ENGINE_ID,
            "version": VERSION,
            "queries_processed": self.query_count,
            "errors": self.error_count,
            "doctrine_coverage_pct": round(coverage_pct, 2),
            "doctrines_triggered": len(self.coverage_triggered),
            "doctrines_total": self.coverage_total,
            "avg_latency_ms": round(avg_latency, 2),
            "top_doctrines": [{"topic": topic, "hits": count} for topic, count in self.doctrine_hit_counts.most_common(5)]
        }

app = FastAPI(title=ENGINE_NAME, version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

engine = ExpertWitnessEngine()

@app.get("/health")
def health():
    return engine.health_check()

@app.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    try:
        result = engine.three_layer_response(req.query, req.mode, req.zone)
        det_hash = engine.generate_determinism_hash(req.query, result["answer"], req.mode.value)

        return QueryResponse(
            query=req.query,
            answer=result["answer"],
            mode=req.mode,
            zone=req.zone,
            confidence=result["confidence"],
            triggered_doctrines=result["triggered_doctrines"],
            reasoning_chain=result["reasoning_chain"],
            authority_citations=result["authority_citations"],
            determinism_hash=det_hash,
            latency_ms=result["latency_ms"],
            session_id=req.session_id
        )
    except Exception as e:
        engine.error_count += 1
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [{"topic": b.topic, "category": b.category.value, "keywords": b.keywords} for b in DOCTRINE_CACHE]
    }

@app.get("/telemetry")
def get_telemetry(limit: int = 100):
    return {"telemetry": [asdict(t) for t in engine.telemetry[-limit:]]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
