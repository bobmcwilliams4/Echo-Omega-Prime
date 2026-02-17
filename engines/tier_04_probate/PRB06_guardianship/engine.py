"""
PRB06 Guardianship Engine v1.0.0
TIE-Grade Intelligence Engine for Guardianship and Conservatorship Law

Port: 9116 | Texas Estates Code Ch. 1001-1355 | Uniform Guardianship Act
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "PRB06"
ENGINE_NAME = "Guardianship Engine"
VERSION = "1.0.0"
PORT = 9116

logger.add(
    f"prb06_guardianship_{datetime.now():%Y%m%d}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════

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
    CAPACITY = "CAPACITY"
    APPOINTMENT = "APPOINTMENT"
    DUTIES = "DUTIES"
    POWERS = "POWERS"
    OVERSIGHT = "OVERSIGHT"
    REMOVAL = "REMOVAL"
    ALTERNATIVES = "ALTERNATIVES"
    PROCEDURE = "PROCEDURE"

# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None

class DoctrineBlock(BaseModel):
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
    controlling_precedent: str
    category: IssueCategory

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    authorities_cited: List[str]
    determinism_hash: str
    telemetry: Dict[str, Any]
    warnings: List[str] = []
    zone: AnalysisZone

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 26 REAL GUARDIANSHIP LAW BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Incapacity Standard - Texas Definition",
        keywords=["incapacity", "capacity", "determination", "definition", "standard", "mental ability"],
        conclusion_template="Under Texas Estates Code Section 1002.017, incapacity means lacking sufficient understanding or capacity to make or communicate responsible decisions concerning oneself due to physical or mental condition. The standard requires clear and convincing evidence that the person cannot manage property or provide for health and safety.",
        reasoning_framework="""Texas law defines incapacity through a functional assessment rather than a diagnosis. The court must find by clear and convincing evidence that the proposed ward lacks sufficient understanding or capacity to make or communicate responsible decisions concerning the person's person, including decisions about where to live or medical treatment, or the person's property. The statute distinguishes between partial and total incapacity, allowing courts to tailor guardianships to individual needs. Medical evidence typically required but not alone sufficient - court must evaluate functional abilities in real-world contexts. The determination must be based on current abilities, not anticipated future decline. Courts examine whether the person can understand consequences of decisions, communicate choices, and manage daily affairs without assistance.""",
        key_factors=[
            "Ability to understand consequences of decisions",
            "Capacity to communicate choices effectively",
            "Understanding of basic health and safety needs",
            "Ability to manage financial affairs and property",
            "Mental or physical condition causing impairment",
            "Whether impairment is total or partial",
            "Current functional abilities not future predictions"
        ],
        primary_authority=[
            "Texas Estates Code Section 1002.017",
            "Texas Estates Code Section 1101.001",
            "In re Guardianship of Jones, 456 S.W.3d 162 (Tex. App. 2015)"
        ],
        burden_holder="Applicant seeking guardianship",
        adversary_position="Proposed ward or interested parties may argue person retains sufficient capacity for less restrictive alternatives",
        counter_arguments=[
            "Temporary confusion or impairment does not equal incapacity",
            "Ability to make some decisions indicates partial capacity only",
            "Supported decision-making could preserve autonomy",
            "Power of attorney already executed when competent"
        ],
        resolution_strategy="Present clear and convincing medical evidence combined with functional assessments showing inability to make responsible decisions. Demonstrate specific examples of impaired judgment causing harm or risk. Consider whether limited guardianship addresses identified deficits while preserving maximum autonomy.",
        entity_scope="Individual proposed wards, guardianship applicants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Clear and convincing evidence standard strictly applied",
        category=IssueCategory.CAPACITY
    ),
    DoctrineBlock(
        topic="Least Restrictive Alternative Requirement",
        keywords=["least restrictive", "alternatives", "power of attorney", "supported decision-making", "limited guardianship"],
        conclusion_template="Texas law requires courts to impose only the least restrictive form of guardianship necessary to protect the incapacitated person. Courts must consider alternatives including power of attorney, supported decision-making agreements, representative payees, or limited guardianships before appointing a full guardian.",
        reasoning_framework="""The least restrictive alternative principle recognizes that guardianship is a substantial deprivation of liberty requiring constitutional due process protections. Texas Estates Code Section 1001.001 mandates that guardianship proceedings promote the well-being and autonomy of incapacitated persons while providing necessary protection. Courts must explicitly consider whether less restrictive means would adequately protect the proposed ward. Limited guardianships restrict only those rights and powers the ward cannot exercise. Supported decision-making agreements allow persons with disabilities to retain autonomy while receiving assistance. The statute creates a preference for preserving individual rights to the maximum extent possible. Applicants must demonstrate why alternatives are insufficient before full guardianship will be granted.""",
        key_factors=[
            "Existence of executed power of attorney",
            "Availability of family or friends for informal support",
            "Possibility of supported decision-making agreement",
            "Whether limited guardianship could address deficits",
            "Specific rights and powers requiring restriction",
            "Ability to modify guardianship if capacity changes"
        ],
        primary_authority=[
            "Texas Estates Code Section 1001.001",
            "Texas Estates Code Section 1101.151 (limited guardianship)",
            "Texas Estates Code Section 1357.001 (supported decision-making)"
        ],
        burden_holder="Guardianship applicant to prove alternatives insufficient",
        adversary_position="Proposed ward argues alternatives preserve autonomy while providing needed assistance",
        counter_arguments=[
            "Power of attorney provides same protection without court involvement",
            "Family willing to assist informally without legal intervention",
            "Supported decision-making preserves dignity and autonomy",
            "Limited guardianship sufficient for identified deficits"
        ],
        resolution_strategy="Demonstrate specific inadequacies of alternatives through evidence of failed informal arrangements, revoked or abused powers of attorney, lack of willing supporters, or need for court oversight. Show that proposed ward's condition requires ongoing judicial supervision that alternatives cannot provide.",
        entity_scope="Proposed wards, guardianship applicants, family members",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Constitutional due process requires least restrictive means",
        category=IssueCategory.ALTERNATIVES
    ),
    DoctrineBlock(
        topic="Guardian Qualification and Priority",
        keywords=["qualification", "priority", "disqualification", "appointment", "who can serve", "eligibility"],
        conclusion_template="Texas law establishes priority preferences for guardian appointments while disqualifying persons with conflicts of interest or criminal histories. Courts must appoint the person best qualified to serve, considering the proposed ward's preferences, family relationships, and ability to fulfill guardian duties.",
        reasoning_framework="""Texas Estates Code Section 1104.351 creates statutory priority for guardian appointments: ward's spouse, nearest of kin, person nominated by will or declaration, person nominated by power of attorney. However, priority is not absolute - courts must determine who is best qualified considering all circumstances. Disqualifications include incapacity, bad conduct, conflicts of interest, certain criminal convictions, and adverse interests. Courts give substantial weight to ward's preferences expressed while competent, including guardian designations in declarations. Professional guardians may be appointed when family members unavailable or unsuitable. The statute requires investigation of proposed guardians including criminal history and credit checks. Courts consider the proposed guardian's ability to perform duties, relationship with ward, and absence of conflicts.""",
        key_factors=[
            "Statutory priority based on relationship to ward",
            "Ward's expressed preferences when competent",
            "Absence of disqualifying factors",
            "Ability to perform guardian duties",
            "Conflicts of interest or adverse interests",
            "Prior relationship and knowledge of ward",
            "Criminal history and credit background"
        ],
        primary_authority=[
            "Texas Estates Code Section 1104.351 (priority)",
            "Texas Estates Code Section 1104.352 (disqualification)",
            "Texas Estates Code Section 1104.402 (declarations)"
        ],
        burden_holder="Applicant to prove qualification and fitness",
        adversary_position="Competing applicants or family members argue priority or better qualification",
        counter_arguments=[
            "Higher priority applicant available under statute",
            "Proposed guardian has conflict of interest",
            "Ward previously designated different guardian",
            "Proposed guardian lacks ability to perform duties"
        ],
        resolution_strategy="Present evidence of qualification including absence of disqualifying factors, relationship with ward, ability to manage affairs, and ward's preferences. If not highest priority applicant, demonstrate unfitness of priority applicants or superior ability to serve ward's interests.",
        entity_scope="Proposed guardians, applicants, family members",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Best interest of ward controls over strict priority",
        category=IssueCategory.APPOINTMENT
    ),
    DoctrineBlock(
        topic="Guardian of Person Duties and Powers",
        keywords=["guardian of person", "duties", "care", "custody", "medical decisions", "residence"],
        conclusion_template="A guardian of the person has custody of the ward and must provide for the ward's care, control, and protection. The guardian has authority to make decisions regarding the ward's residence, medical treatment, personal care, and other matters affecting the ward's well-being, subject to court approval for major decisions.",
        reasoning_framework="""Texas Estates Code Section 1151.051 grants guardians of the person broad authority over the ward's personal care while imposing corresponding duties. The guardian must take reasonable care of the ward's person, ensure proper food, clothing, shelter, and medical care. The guardian decides the ward's residence subject to court approval for institutional placement. Medical decision authority includes routine care but court approval required for psychoactive medications, ECT, or experimental treatments. The guardian must visit the ward regularly and report to court on the ward's condition. The guardian may not delegate core duties but may employ others to assist with care. The standard of care is that of an ordinarily prudent person managing their own affairs. Guardians must respect the ward's preferences to extent possible and encourage maximum self-reliance.""",
        key_factors=[
            "Custody and control of ward's person",
            "Authority over medical treatment decisions",
            "Power to determine ward's residence",
            "Duty to provide necessities of life",
            "Requirement to visit ward regularly",
            "Court approval needed for major decisions",
            "Obligation to respect ward's preferences"
        ],
        primary_authority=[
            "Texas Estates Code Section 1151.051",
            "Texas Estates Code Section 1151.052 (residence)",
            "Texas Estates Code Section 1151.102 (medical consent)"
        ],
        burden_holder="Guardian to prove compliance with duties",
        adversary_position="Ward or family members challenge care decisions as not in ward's best interest",
        counter_arguments=[
            "Guardian made unauthorized major decision without court approval",
            "Care provided falls below reasonable standard",
            "Guardian ignoring ward's clearly expressed preferences",
            "Institutional placement inappropriate for ward's needs"
        ],
        resolution_strategy="Document regular visits and care decisions. Obtain court approval before major decisions. Demonstrate care decisions based on professional recommendations and ward's best interests. Show consideration of ward's preferences and efforts to maximize autonomy.",
        entity_scope="Guardians of person, wards, family members",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Guardian acts as fiduciary owing highest duty of care",
        category=IssueCategory.DUTIES
    ),
    DoctrineBlock(
        topic="Guardian of Estate Financial Duties",
        keywords=["guardian of estate", "financial", "property", "accounting", "fiduciary", "investments"],
        conclusion_template="A guardian of the estate serves as fiduciary for the ward's property with duties to preserve assets, invest prudently, maintain accurate records, and file annual accountings with the court. The guardian must obtain court approval for major transactions and may not self-deal or benefit personally from the guardianship.",
        reasoning_framework="""Texas Estates Code imposes strict fiduciary duties on guardians of the estate. The guardian must take possession of all ward's property, maintain it in good repair, invest funds prudently under the Texas Trust Code standards, and account for every dollar. Annual accountings must detail all receipts, disbursements, investments, and current assets. The guardian may not commingle ward's funds with personal funds, lend ward's money to self or family, or profit from transactions involving ward's property. Court approval required for sales of real property, business operations, investments outside normal course, and compensation to guardian. The guardian must obtain bond unless waived by court. Breach of fiduciary duty may result in surcharge requiring guardian to reimburse estate. The standard is that of an ordinarily prudent person managing their own property.""",
        key_factors=[
            "Duty to take possession and preserve assets",
            "Prudent investor standard for investments",
            "Prohibition on self-dealing and conflicts",
            "Annual accounting requirement",
            "Court approval for major transactions",
            "Bond requirement to protect estate",
            "Duty of loyalty and avoidance of personal benefit"
        ],
        primary_authority=[
            "Texas Estates Code Section 1151.151",
            "Texas Estates Code Section 1163.001 (accounting)",
            "Texas Property Code Section 117.004 (prudent investor)"
        ],
        burden_holder="Guardian to prove proper management and accounting",
        adversary_position="Court or interested parties challenge mismanagement or breach of fiduciary duty",
        counter_arguments=[
            "Guardian engaged in self-dealing transactions",
            "Investments imprudent or speculative",
            "Accounting incomplete or inaccurate",
            "Guardian commingled funds or borrowed from estate",
            "Major transaction completed without court approval"
        ],
        resolution_strategy="Maintain meticulous records of all transactions. Obtain court approval before any questionable transaction. Invest conservatively following prudent investor standards. File timely and complete annual accountings. Avoid any appearance of self-dealing or personal benefit.",
        entity_scope="Guardians of estate, wards, courts, creditors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Strict fiduciary duty with potential personal liability for breaches",
        category=IssueCategory.DUTIES
    ),
    DoctrineBlock(
        topic="Annual Report and Accounting Requirements",
        keywords=["annual report", "accounting", "inventory", "reporting", "court oversight", "deadline"],
        conclusion_template="Guardians must file annual reports describing the ward's condition and annual accountings detailing all financial transactions. The initial inventory is due within 30 days of appointment. Annual accountings are due within 60 days after the anniversary of qualification. Failure to timely file may result in removal and personal liability.",
        reasoning_framework="""Court oversight of guardianships occurs primarily through required annual reports and accountings. Texas Estates Code Section 1163.001 requires guardians of estates to file verified annual accountings showing all property received, disbursements made, current assets, and financial condition. Guardians of the person file annual reports describing the ward's residence, physical and mental condition, and care provided. The initial inventory must list all ward's property and be filed within 30 days of qualification. Annual accountings due within 60 days after each anniversary of qualification. Courts may require more frequent accountings if circumstances warrant. The accounting must be verified under oath and supported by vouchers for disbursements. Interested parties may object to accountings and request hearings. Failure to file constitutes grounds for removal. Guardians may be held personally liable for estate losses if accounting reveals mismanagement.""",
        key_factors=[
            "Initial inventory due within 30 days of appointment",
            "Annual accounting due within 60 days of anniversary",
            "Accounting must detail all receipts and disbursements",
            "Verification under oath required",
            "Annual report on ward's condition for person guardians",
            "Court may order more frequent reports",
            "Failure to file is grounds for removal"
        ],
        primary_authority=[
            "Texas Estates Code Section 1163.001",
            "Texas Estates Code Section 1154.051 (inventory)",
            "Texas Estates Code Section 1163.101 (annual report of guardian of person)"
        ],
        burden_holder="Guardian to file timely and accurate reports",
        adversary_position="Court or interested parties challenge accuracy or seek removal for failure to file",
        counter_arguments=[
            "Accounting incomplete or inaccurate",
            "Vouchers missing for disbursements",
            "Filing deadline missed without excuse",
            "Report omits material information about ward's condition"
        ],
        resolution_strategy="Maintain detailed contemporaneous records throughout the year. Calendar filing deadlines carefully. Prepare draft accountings well in advance. Include all required information and supporting documentation. File electronically if available for proof of timely filing.",
        entity_scope="Guardians, wards, courts, interested parties",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Strict compliance with filing deadlines enforced",
        category=IssueCategory.OVERSIGHT
    ),
    DoctrineBlock(
        topic="Guardian Ad Litem Role and Duties",
        keywords=["guardian ad litem", "GAL", "attorney ad litem", "investigation", "independent", "court appointee"],
        conclusion_template="A guardian ad litem is a court-appointed advocate who investigates the proposed ward's circumstances and reports findings to the court. The GAL must interview the proposed ward, review medical records, investigate living conditions, and make recommendations regarding necessity of guardianship and appropriate guardian. The GAL represents the ward's best interests, not necessarily the ward's expressed wishes.",
        reasoning_framework="""Texas law requires appointment of guardian ad litem and attorney ad litem in most guardianship proceedings. The guardian ad litem conducts an independent investigation and advocates for the proposed ward's best interests. Unlike the attorney ad litem who represents the ward's expressed wishes, the GAL may recommend against the ward's stated preferences if doing so serves the ward's welfare. The GAL must personally visit the proposed ward, interview medical providers and family members, review relevant documents, and file a written report with specific findings. The report must address whether guardianship is necessary, whether alternatives are available, who should serve as guardian, and what powers the guardian needs. Courts give substantial weight to GAL recommendations. The GAL serves as the court's eyes and ears, providing independent assessment free from family or financial interests.""",
        key_factors=[
            "Court appointment required in most cases",
            "Personal interview with proposed ward mandatory",
            "Investigation of medical records and living situation",
            "Written report with specific findings required",
            "Advocate for best interests not expressed wishes",
            "Assessment of necessity and alternatives",
            "Recommendation regarding guardian selection"
        ],
        primary_authority=[
            "Texas Estates Code Section 1054.001",
            "Texas Estates Code Section 1054.005 (duties)",
            "Texas Estates Code Section 1054.054 (report)"
        ],
        burden_holder="GAL to conduct thorough investigation and report",
        adversary_position="Parties may challenge GAL's findings or recommendations",
        counter_arguments=[
            "GAL failed to personally interview ward",
            "Investigation inadequate or incomplete",
            "Recommendations based on insufficient information",
            "GAL has conflict of interest"
        ],
        resolution_strategy="For GALs: conduct thorough investigation including personal ward visit, review all relevant records, interview key persons, and prepare detailed report addressing statutory factors. For parties: present evidence contradicting GAL findings and demonstrate superior information.",
        entity_scope="Courts, proposed wards, guardianship applicants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="GAL investigation and report required for valid guardianship",
        category=IssueCategory.PROCEDURE
    ),
    DoctrineBlock(
        topic="Temporary Guardianship Emergency Appointment",
        keywords=["temporary", "emergency", "immediate", "irreparable harm", "ex parte", "pending"],
        conclusion_template="Courts may appoint temporary guardians without full hearing when immediate action necessary to prevent imminent harm to the proposed ward or estate. Temporary guardianships require showing of immediate and irreparable harm and are limited in duration. Full hearing must follow within strict timeframe.",
        reasoning_framework="""Texas Estates Code Section 1251.001 authorizes temporary guardianship appointments when necessary to protect the proposed ward's person or property from imminent harm that will occur before a full hearing can be held. The applicant must demonstrate specific facts showing immediate danger - general allegations of vulnerability are insufficient. Examples include medical emergency requiring immediate consent, financial exploitation in progress, or imminent placement in dangerous living situation. Temporary guardians have limited powers specified in the court order and typically serve only until full hearing, usually 10-20 days. Bond may be required even if waived for permanent guardians. Courts are cautious about ex parte temporary appointments and prefer notice to proposed ward if possible. The temporary order must specify findings supporting emergency appointment and enumerate the temporary guardian's powers.""",
        key_factors=[
            "Immediate and irreparable harm if appointment delayed",
            "Specific facts showing imminent danger required",
            "Limited duration until full hearing",
            "Powers restricted to those necessary for emergency",
            "Bond may be required",
            "Full hearing must follow within days or weeks",
            "Ex parte appointment only if notice impractical"
        ],
        primary_authority=[
            "Texas Estates Code Section 1251.001",
            "Texas Estates Code Section 1251.003 (duration)",
            "In re Guardianship of Miller, 333 S.W.3d 582 (Tex. App. 2011)"
        ],
        burden_holder="Temporary guardianship applicant to prove immediate emergency",
        adversary_position="Proposed ward or family argue no emergency exists or alternatives available",
        counter_arguments=[
            "No immediate harm - situation stable",
            "Family member available to address issue informally",
            "Power of attorney already in place",
            "Delay for notice would not cause irreparable harm"
        ],
        resolution_strategy="Present specific evidence of imminent harm with timeframe demonstrating injury will occur before full hearing. Show why informal alternatives insufficient. Limit requested powers to minimum necessary to address emergency. Commit to expedited full hearing.",
        entity_scope="Proposed wards facing emergencies, temporary guardians",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Strict scrutiny of temporary appointments to protect due process",
        category=IssueCategory.APPOINTMENT
    ),
    DoctrineBlock(
        topic="Removal of Guardian for Cause",
        keywords=["removal", "termination", "cause", "misconduct", "breach of duty", "unsuitable"],
        conclusion_template="Courts may remove guardians for failure to perform duties, mismanagement of estate, abuse or neglect of ward, conviction of crime, becoming incapacitated, or other conduct making the guardian unsuitable. Interested parties or the court may initiate removal proceedings. The guardian may be surcharged for estate losses.",
        reasoning_framework="""Texas Estates Code Section 1203.001 provides grounds for guardian removal including: failure to file required reports or accountings, mismanagement or self-dealing with estate assets, failure to provide adequate care for ward, conviction of felony or crime involving moral turpitude, becoming incapacitated or unsuitable, gross misconduct, or other conduct detrimental to the ward. Removal may be initiated by interested parties, the ward if partially competent, or the court sua sponte. The applicant must prove grounds by preponderance of evidence. Courts have broad discretion to remove guardians when continuation not in ward's best interest even if specific statutory grounds not proven. Upon removal, the guardian must file final accounting and deliver estate property to successor. Courts may surcharge removed guardians for estate losses caused by mismanagement. Criminal prosecution may follow for theft or abuse. The removal does not discharge the guardian's bond - liability continues for acts during service.""",
        key_factors=[
            "Statutory grounds including failure of duty or misconduct",
            "Court discretion based on ward's best interest",
            "Interested parties or court may initiate removal",
            "Preponderance of evidence standard",
            "Final accounting required from removed guardian",
            "Potential surcharge for estate losses",
            "Bond liability continues for acts during service"
        ],
        primary_authority=[
            "Texas Estates Code Section 1203.001",
            "Texas Estates Code Section 1203.052 (procedure)",
            "Texas Estates Code Section 1204.001 (final accounting)"
        ],
        burden_holder="Removal applicant to prove grounds",
        adversary_position="Guardian defends performance and contests removal",
        counter_arguments=[
            "Allegations exaggerated or without merit",
            "Minor deficiencies corrected when discovered",
            "Ward's family members have ulterior motives",
            "Removal would harm ward by disrupting care"
        ],
        resolution_strategy="For removal applicants: document specific instances of breach of duty, mismanagement, or neglect. Present evidence of harm to ward or estate. Show pattern of misconduct not isolated incident. For guardians: demonstrate overall faithful performance, correction of any deficiencies, and detriment to ward from removal.",
        entity_scope="Guardians, wards, interested parties, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Removal appropriate when guardian unsuitable even without proven misconduct",
        category=IssueCategory.REMOVAL
    ),
    DoctrineBlock(
        topic="Ward Rights and Due Process Protections",
        keywords=["ward rights", "due process", "notice", "hearing", "attorney", "jury trial", "appeal"],
        conclusion_template="Proposed wards have constitutional and statutory rights including notice of proceedings, right to attend hearings, right to attorney, right to jury trial, right to present evidence, and right to appeal. Courts must ensure procedural protections before imposing guardianship given the significant deprivation of liberty involved.",
        reasoning_framework="""Guardianship proceedings implicate fundamental liberty interests triggering constitutional due process protections. The Supreme Court has held that proposed wards must receive notice reasonably calculated to inform them of proceedings and opportunity to be heard. Texas law provides robust procedural protections: proposed ward must receive personal service of citation, has right to court-appointed attorney if indigent, may request jury trial, can present evidence and cross-examine witnesses, and may appeal adverse decisions. The proposed ward has right to attend all hearings unless court finds attendance would be injurious to health. Courts must conduct hearings in least restrictive setting and accommodate disabilities. The ward retains all legal rights except those specifically restricted by court order. Guardianship orders must specify which rights are restricted. Wards may petition for modification or restoration of rights. The procedural safeguards recognize that guardianship substantially curtails individual autonomy and requires careful judicial oversight.""",
        key_factors=[
            "Personal service of citation required",
            "Right to court-appointed attorney if indigent",
            "Right to attend hearings unless injurious to health",
            "Right to jury trial on request",
            "Right to present evidence and witnesses",
            "Right to appeal adverse decisions",
            "Only rights specifically restricted may be removed"
        ],
        primary_authority=[
            "Texas Estates Code Section 1051.001 (citation)",
            "Texas Estates Code Section 1054.001 (attorney ad litem)",
            "Texas Estates Code Section 1054.006 (jury trial)"
        ],
        burden_holder="Court to ensure due process protections afforded",
        adversary_position="Proposed ward contests adequacy of procedural protections",
        counter_arguments=[
            "Notice inadequate or not provided",
            "Attorney provided was ineffective",
            "Ward denied opportunity to testify or present evidence",
            "Hearing conducted without ward present without proper findings"
        ],
        resolution_strategy="Ensure strict compliance with procedural requirements. Document service of citation. Provide competent attorney. Allow ward to attend unless clear medical evidence attendance harmful. Create thorough record of hearing. Specify in order which rights restricted and reasons.",
        entity_scope="Proposed wards, courts, attorneys",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Constitutional due process requires strict procedural compliance",
        category=IssueCategory.PROCEDURE
    ),
    DoctrineBlock(
        topic="Modification and Restoration of Capacity",
        keywords=["modification", "restoration", "capacity restored", "rights restoration", "termination", "changed circumstances"],
        conclusion_template="Wards may petition for restoration of rights or termination of guardianship upon showing that capacity has been restored or guardianship no longer necessary. Courts must grant hearing on restoration petition and terminate guardianship if ward proves capacity by preponderance of evidence. Guardianship orders may also be modified to expand or restrict powers based on changed circumstances.",
        reasoning_framework="""Texas Estates Code Section 1202.001 provides mechanism for wards to petition for restoration of capacity and termination or modification of guardianship. The ward bears burden to prove by preponderance of evidence that capacity has been restored and guardianship no longer necessary. Courts must grant hearing on restoration petition. Medical and psychological evaluations typically required. If partial capacity restored, court may modify guardianship to expand ward's rights while maintaining protection where still needed. The guardian ad litem investigates and reports on restoration petition. Courts liberally grant restoration petitions when evidence supports capacity restoration, recognizing the goal of guardianship is protection not punishment. The law presumes capacity and encourages maximum autonomy. Changed circumstances may also warrant modification even without full restoration - for example, limited guardianship may be expanded or restricted based on ward's current needs. The guardianship should be the least restrictive means necessary at all times.""",
        key_factors=[
            "Ward may petition for restoration at any time",
            "Court must grant hearing on petition",
            "Ward proves restoration by preponderance of evidence",
            "Medical evaluation typically required",
            "Partial restoration possible through modification",
            "Guardian ad litem investigates and reports",
            "Changed circumstances warrant modification of powers"
        ],
        primary_authority=[
            "Texas Estates Code Section 1202.001",
            "Texas Estates Code Section 1202.051 (modification)",
            "In re Guardianship of Brown, 387 S.W.3d 723 (Tex. App. 2012)"
        ],
        burden_holder="Ward seeking restoration to prove capacity",
        adversary_position="Guardian or interested parties argue capacity not restored",
        counter_arguments=[
            "Recent incidents demonstrate continued incapacity",
            "Medical evidence does not support restoration",
            "Partial capacity only - modification more appropriate",
            "Ward lacks insight into limitations"
        ],
        resolution_strategy="For ward: present current medical evaluations showing capacity, demonstrate functional abilities, show successful management during trial period. For opponents: present evidence of recent incidents showing continued impairment, medical opinions supporting continued need, functional assessments.",
        entity_scope="Wards, guardians, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Presumption favors restoration when capacity proven",
        category=IssueCategory.REMOVAL
    ),
    DoctrineBlock(
        topic="Minor Guardianship Distinctions",
        keywords=["minor", "child", "parent", "natural guardian", "18 years", "emancipation"],
        conclusion_template="Parents are natural guardians of their minor children and guardianship appointments for minors are generally unnecessary unless parents are deceased, incapacitated, or unfit. Minor guardianships terminate automatically when the child reaches age 18 unless incapacity continues. Different standards apply than for adult guardianships.",
        reasoning_framework="""Texas law distinguishes between guardianships of minors and incapacitated adults. Parents have inherent authority as natural guardians of their minor children and court-appointed guardianships are unnecessary in most cases. Court-appointed guardianships for minors typically arise when: both parents deceased, parents incapacitated or unfit, parents consent to appointment, or minor receives property requiring management. The capacity determination differs - minors are legally incapacitated solely due to age, not mental or physical condition. Minor guardianships automatically terminate when ward reaches age 18 unless the ward remains incapacitated and continuing guardianship is established. Guardians of minors have similar duties as guardians of incapacitated adults but certain provisions differ. Minors have limited capacity to contract and sue. Guardians of minor estates must preserve assets for ward's benefit until majority. Educational decisions are part of guardian of person duties for minors.""",
        key_factors=[
            "Parents are natural guardians unless unavailable or unfit",
            "Guardianship terminates automatically at age 18",
            "Capacity based on age not mental condition",
            "Different procedural rules for minor guardianships",
            "Guardian must preserve estate for ward's benefit",
            "Educational decisions included in guardian duties"
        ],
        primary_authority=[
            "Texas Estates Code Section 1104.001",
            "Texas Family Code Section 151.001 (parental rights)",
            "Texas Estates Code Section 1113.001 (termination at majority)"
        ],
        burden_holder="Applicant to prove need for guardianship of minor",
        adversary_position="Parents or minor contest necessity of guardianship",
        counter_arguments=[
            "Parents available and fit to serve",
            "Minor nearly 18 - guardianship unnecessary",
            "Informal arrangements adequate",
            "Proposed guardian has ulterior motive"
        ],
        resolution_strategy="Demonstrate parents deceased, incapacitated, or unfit. Show specific need for court-appointed guardian. If minor has estate, prove need for formal management. Address what will occur when minor reaches 18.",
        entity_scope="Minors, parents, guardians",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Parents have presumptive right to custody of minor children",
        category=IssueCategory.CAPACITY
    ),
    DoctrineBlock(
        topic="Guardian Bond Requirements and Waiver",
        keywords=["bond", "surety", "waiver", "bonding company", "security", "protection"],
        conclusion_template="Guardians of estates must post bond unless waived by court, typically in amount equal to estimated value of estate plus one year's income. Bond protects the estate from guardian mismanagement or theft. Courts may waive bond for certain corporate guardians or when all interested parties consent and waiver serves ward's interests.",
        reasoning_framework="""Texas Estates Code Section 1105.001 requires guardians of estates to post bond before qualifying unless waived by court. The bond amount must equal the estimated value of ward's personal property plus one year's estimated income. The bond serves as insurance protecting the estate from guardian misconduct or negligence. Bonding companies issue bonds for annual premium paid from estate. Corporate guardians and certain other entities may qualify for bond waiver. Courts may waive bond if all interested parties consent in writing and court finds waiver in ward's best interest. Guardians of person only (no estate) need not post bond unless ordered by court. The bond remains in force during the guardianship and for period after discharge to allow claims. Increasing estate value may require increased bond. Breach of fiduciary duty triggers surety's obligation to pay estate for losses. Guardians failing to post required bond cannot qualify and may be removed.""",
        key_factors=[
            "Bond required for guardians of estate unless waived",
            "Amount equals estate value plus one year income",
            "Bonding company surety required",
            "Premium paid from estate funds",
            "Court may waive for corporate guardians or with consent",
            "Bond protects estate from mismanagement",
            "Failure to post bond prevents qualification"
        ],
        primary_authority=[
            "Texas Estates Code Section 1105.001",
            "Texas Estates Code Section 1105.051 (amount)",
            "Texas Estates Code Section 1105.152 (waiver)"
        ],
        burden_holder="Guardian to post bond before qualifying",
        adversary_position="Interested parties may object to bond amount or waiver",
        counter_arguments=[
            "Bond amount insufficient to protect estate",
            "Waiver inappropriate given guardian's background",
            "Bonding company not financially sound",
            "Guardian should pay premium not estate"
        ],
        resolution_strategy="For guardians seeking waiver: obtain written consent of all interested parties and demonstrate waiver serves ward's interests. For objectors: show need for bond protection given estate value and guardian's circumstances. Present evidence questioning guardian's trustworthiness.",
        entity_scope="Guardians of estate, bonding companies, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Bond required unless statutory grounds for waiver exist",
        category=IssueCategory.PROCEDURE
    ),
    DoctrineBlock(
        topic="Guardianship Venue and Jurisdiction",
        keywords=["venue", "jurisdiction", "county", "domicile", "residence", "transfer"],
        conclusion_template="Guardianship venue lies in the county of the proposed ward's domicile or residence. If the ward is a nonresident, venue may lie where ward's principal estate is located. Improper venue may be challenged by plea in abatement. Guardianships may be transferred to another county upon showing of good cause.",
        reasoning_framework="""Texas Estates Code Section 1023.001 establishes venue for guardianship proceedings. Proper venue is: county of proposed ward's domicile, or if ward is nonresident, county where principal estate located. Domicile means the place where person intends to remain permanently. Residence means actual dwelling place. Domicile controls over mere residence. If ward has been moved to another county specifically to create venue, the move may be disregarded. Improper venue is raised by verified plea in abatement. Venue is determined at time of filing application. Once guardianship established, it may be transferred to another county upon motion showing good cause. Transfer typically granted when ward moves to another county. The transferring court sends certified copies of all documents to receiving court. Continuing jurisdiction remains in the transferee county unless again transferred. Competing guardianship applications in different counties raise complex issues - generally first-filed application controls but courts may consolidate.""",
        key_factors=[
            "Domicile of proposed ward controls venue",
            "Residence distinguished from domicile",
            "Principal estate location for nonresidents",
            "Improper venue raised by plea in abatement",
            "Transfer permitted upon good cause shown",
            "Ward's move to new county supports transfer",
            "First-filed application generally controls if multiple"
        ],
        primary_authority=[
            "Texas Estates Code Section 1023.001",
            "Texas Estates Code Section 1023.002 (nonresident)",
            "Texas Estates Code Section 1024.001 (transfer)"
        ],
        burden_holder="Applicant to establish proper venue",
        adversary_position="Respondent challenges venue as improper",
        counter_arguments=[
            "Ward's presence in county is temporary not domicile",
            "Ward moved to county solely to create venue",
            "Principal estate located in different county",
            "First-filed application in different county"
        ],
        resolution_strategy="Establish ward's intent to remain permanently in county, length of residence, location of family and property. For venue transfers, show ward's permanent move to new county and good cause for transfer. Contest improper venue by plea in abatement with evidence of domicile elsewhere.",
        entity_scope="Courts, proposed wards, applicants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Domicile controls venue determination",
        category=IssueCategory.PROCEDURE
    ),
    DoctrineBlock(
        topic="Supported Decision-Making Agreement Alternative",
        keywords=["supported decision-making", "SDM", "supporter", "alternative", "autonomy", "disability rights"],
        conclusion_template="Supported decision-making agreements allow adults with disabilities to retain legal capacity while designating supporters to help understand, make, and communicate decisions. SDMAs provide less restrictive alternative to guardianship consistent with disability rights movement emphasizing autonomy and self-determination.",
        reasoning_framework="""Texas enacted supported decision-making legislation in 2015 as alternative to guardianship for persons with intellectual or developmental disabilities. Texas Estates Code Chapter 1357 authorizes adults to enter agreements designating supporters who assist with decisions regarding finances, medical care, and daily living without removing the person's legal capacity. The supporter does not have authority to make decisions for the person but rather helps the person understand options, considerations, and consequences so the person can make informed choices. The agreement must be in writing, signed by principal and supporters, and may be revoked at any time. Supporters have access to medical records and financial information to extent specified in agreement. Third parties must honor decisions made by principal with supporter assistance. SDMAs recognize that many persons with disabilities can make decisions with appropriate support and that guardianship's removal of legal capacity should be last resort. Courts must consider whether SDMA would adequately protect proposed ward before appointing guardian.""",
        key_factors=[
            "Principal retains full legal capacity",
            "Supporters assist but do not make decisions",
            "Agreement must be in writing and signed",
            "Principal may revoke agreement at any time",
            "Supporters have access to specified information",
            "Less restrictive alternative to guardianship",
            "Promotes autonomy and self-determination"
        ],
        primary_authority=[
            "Texas Estates Code Section 1357.001",
            "Texas Estates Code Section 1357.051 (authority of supporters)",
            "Texas Estates Code Section 1357.101 (agreement requirements)"
        ],
        burden_holder="Guardianship applicant to show SDMA insufficient",
        adversary_position="Proposed ward argues SDMA adequate to protect interests",
        counter_arguments=[
            "Principal capable of making decisions with support",
            "SDMA preserves dignity and autonomy",
            "Guardianship unnecessarily restrictive",
            "Willing supporters available to assist"
        ],
        resolution_strategy="For SDMA proponents: demonstrate principal's ability to understand with support, identify willing supporters, draft comprehensive agreement. For guardianship applicants: show principal unable to make decisions even with support, need for legal authority to bind third parties, inadequacy of informal assistance.",
        entity_scope="Adults with disabilities, supporters, courts",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="SDMA must be considered before guardianship appointed",
        category=IssueCategory.ALTERNATIVES
    ),
    DoctrineBlock(
        topic="Interstate Transfer of Guardianship",
        keywords=["interstate", "transfer", "UAGPPJA", "Uniform Act", "another state", "jurisdiction"],
        conclusion_template="The Uniform Adult Guardianship and Protective Proceedings Jurisdiction Act (UAGPPJA) governs transfer of guardianships between states. Texas courts may accept transfer of out-of-state guardianships or transfer Texas guardianships to other states following specific procedures ensuring continuity of protection.",
        reasoning_framework="""Texas adopted UAGPPJA in 2009 to facilitate interstate guardianship transfers and resolve jurisdictional conflicts. The Act establishes hierarchy of jurisdiction: home state (where respondent resided 6+ months), significant connection state, or state accepting jurisdiction. Courts may transfer guardianship to another state if transfer is in ward's best interest and courts of both states agree. Transfer requires petition in both states, notice to interested parties, opportunity for hearing, and findings that transfer serves ward's interest. Upon transfer, the transferring state relinquishes jurisdiction and the receiving state assumes all powers. Registered orders from other states are enforceable in Texas without new proceeding. Emergency jurisdiction allows temporary orders to protect persons or property in state. The Act provides clear rules for determining which state's court has authority, reducing litigation over jurisdiction and enabling efficient transfers when wards relocate.""",
        key_factors=[
            "Home state jurisdiction preferred",
            "Transfer requires petition and hearing in both states",
            "Courts must find transfer in ward's best interest",
            "Transferring state relinquishes jurisdiction",
            "Receiving state assumes all powers",
            "Out-of-state orders enforceable by registration",
            "Emergency jurisdiction for temporary protection"
        ],
        primary_authority=[
            "Texas Estates Code Chapter 1351 (UAGPPJA)",
            "Texas Estates Code Section 1351.051 (home state jurisdiction)",
            "Texas Estates Code Section 1351.301 (transfer)"
        ],
        burden_holder="Transfer petitioner to prove best interest and jurisdictional facts",
        adversary_position="Interested parties may contest transfer or jurisdiction",
        counter_arguments=[
            "Ward's presence in state is temporary",
            "Transfer not in ward's best interest",
            "Other state lacks jurisdiction under UAGPPJA",
            "Guardian forum shopping to avoid oversight"
        ],
        resolution_strategy="Establish ward's permanent move to other state and contacts there. Show transfer serves ward's interest by proximity to family, services, or guardian. Ensure both states' courts agree. For jurisdictional disputes, analyze UAGPPJA factors showing appropriate forum.",
        entity_scope="Wards relocating between states, courts, guardians",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="UAGPPJA establishes clear jurisdictional hierarchy",
        category=IssueCategory.PROCEDURE
    ),
    DoctrineBlock(
        topic="Guardian Compensation and Expenses",
        keywords=["compensation", "fees", "payment", "expenses", "reimbursement", "reasonableness"],
        conclusion_template="Guardians are entitled to reasonable compensation for services and reimbursement of expenses from the ward's estate. Courts must approve compensation considering the guardian's duties, time expended, estate size, and results obtained. Family guardians often serve without compensation while professional guardians charge statutory or hourly fees.",
        reasoning_framework="""Texas Estates Code Section 1155.001 authorizes guardian compensation as the court considers just and reasonable. Factors include: nature and difficulty of duties performed, time and labor required, estate size and income, results obtained, customary compensation for similar services, and whether guardian is family member or professional. Professional guardians typically charge either statutory percentage or hourly rates. Family guardians often serve without compensation. All compensation must be approved by court, typically in annual accounting proceedings. Guardians may petition for compensation at accounting or when resigning. Unreasonable compensation may be denied or reduced. Guardians are entitled to reimbursement of reasonable expenses including attorney fees, accountant fees, and costs of estate administration. Expenses must be documented and reasonable. Courts scrutinize compensation carefully to protect ward's estate from excessive fees.""",
        key_factors=[
            "Compensation must be approved by court",
            "Reasonableness determined by multiple factors",
            "Professional guardians typically charge fees",
            "Family guardians often serve without pay",
            "Expenses must be reasonable and documented",
            "Attorney fees reimbursable from estate",
            "Requested compensation may be reduced as excessive"
        ],
        primary_authority=[
            "Texas Estates Code Section 1155.001",
            "Texas Estates Code Section 1155.002 (court approval required)",
            "In re Guardianship of Davis, 299 S.W.3d 588 (Tex. App. 2009)"
        ],
        burden_holder="Guardian requesting compensation to prove reasonableness",
        adversary_position="Interested parties or court challenge compensation as excessive",
        counter_arguments=[
            "Compensation excessive compared to services rendered",
            "Guardian seeking payment for routine family duties",
            "Expenses unnecessary or unreasonable",
            "Estate size does not support requested fees"
        ],
        resolution_strategy="Document time spent on guardian duties with detailed records. Obtain fee agreements in advance when possible. Present evidence of customary fees for similar services. For objectors: compare requested compensation to statutory guidelines and services actually rendered.",
        entity_scope="Guardians, wards' estates, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Compensation must be reasonable and approved by court",
        category=IssueCategory.POWERS
    ),
    DoctrineBlock(
        topic="Medical Consent and Treatment Decisions",
        keywords=["medical consent", "treatment", "psychoactive medication", "ECT", "experimental", "DNR", "end of life"],
        conclusion_template="Guardians of the person have authority to consent to medical treatment for wards but court approval is required for psychoactive medications, electroconvulsive therapy, experimental treatments, and certain other major medical decisions. Guardians must make treatment decisions in ward's best interest considering ward's expressed wishes.",
        reasoning_framework="""Texas Estates Code Section 1151.102 grants guardians authority to consent to medical care while requiring court approval for specified treatments: psychoactive medications (except emergency), electroconvulsive therapy, surgical procedures involving significant risk, and experimental treatments. The guardian should involve the ward in medical decisions to extent possible and consider ward's values and previously expressed wishes. For routine medical care, guardian consent is sufficient. Emergency medical treatment may be provided without guardian consent when delay would risk serious harm. Do-not-resuscitate orders require specific court authorization. Guardians may not consent to abortion, sterilization, or withholding life-sustaining treatment without court approval. The guardian must balance the ward's right to refuse treatment with duty to protect ward's health. Medical providers may refuse to follow guardian directives they believe contrary to standard of care.""",
        key_factors=[
            "Guardian may consent to routine medical care",
            "Court approval required for psychoactive medications",
            "Court approval required for ECT and experimental treatment",
            "Emergency treatment permitted without guardian consent",
            "Guardian must consider ward's expressed wishes",
            "DNR orders require specific court authorization",
            "Abortion and sterilization require court approval"
        ],
        primary_authority=[
            "Texas Estates Code Section 1151.102",
            "Texas Estates Code Section 1151.103 (psychoactive medication)",
            "Texas Health and Safety Code Section 166.002 (advance directives)"
        ],
        burden_holder="Guardian to show treatment in ward's best interest",
        adversary_position="Ward, family, or medical providers challenge treatment decision",
        counter_arguments=[
            "Treatment violates ward's religious beliefs",
            "Ward expressed opposition when competent",
            "Less invasive alternatives available",
            "Treatment not medically necessary",
            "Guardian exceeded authority without court approval"
        ],
        resolution_strategy="Obtain court approval before major treatments. Document ward's participation in decision-making. Consult medical professionals and consider ward's values. For objectors: present evidence of ward's previously expressed wishes, religious or personal values, or medical alternatives.",
        entity_scope="Guardians of person, wards, medical providers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Court approval required for specified major treatments",
        category=IssueCategory.POWERS
    ),
    DoctrineBlock(
        topic="Guardian Duty to Avoid Conflicts of Interest",
        keywords=["conflict of interest", "self-dealing", "fiduciary duty", "loyalty", "adverse interest", "transactions"],
        conclusion_template="Guardians owe fiduciary duties of loyalty and must avoid conflicts of interest. Transactions between guardian and ward's estate are prohibited unless court-approved after full disclosure. Guardians may not profit from position or place personal interests above ward's interests.",
        reasoning_framework="""As fiduciaries, guardians must act solely in the ward's best interest and avoid conflicts of interest. Texas law prohibits self-dealing transactions including: guardian purchasing ward's property, lending ward's money to self or relatives, using ward's assets for personal benefit, employing self or family members without court approval, or placing personal interests above ward's. All transactions between guardian and estate must be disclosed to court and approved. The duty of loyalty is highest fiduciary duty - guardian may not profit from position except approved compensation. Conflicts may arise from business relationships, family interests, or personal financial benefit. Guardian should disclose potential conflicts and obtain court guidance. Breach of fiduciary duty may result in removal, denial of compensation, and surcharge requiring guardian to reimburse estate. The no-conflict rule protects vulnerable wards from exploitation.""",
        key_factors=[
            "Guardian owes duty of loyalty to ward",
            "Self-dealing transactions prohibited",
            "Court approval required after full disclosure",
            "Guardian may not profit except approved compensation",
            "Personal interests must not override ward's interests",
            "Conflicts must be disclosed to court",
            "Breach may result in removal and surcharge"
        ],
        primary_authority=[
            "Texas Estates Code Section 1151.151 (fiduciary duty)",
            "Texas Trust Code Section 114.008 (duty of loyalty)",
            "In re Guardianship of Thompson, 398 S.W.3d 712 (Tex. App. 2013)"
        ],
        burden_holder="Guardian to avoid conflicts and disclose potential conflicts",
        adversary_position="Interested parties challenge conflicted transactions",
        counter_arguments=[
            "Guardian engaged in self-dealing transaction",
            "Guardian profited personally from position",
            "Transaction favored guardian's interests over ward's",
            "Guardian failed to disclose conflict to court"
        ],
        resolution_strategy="Avoid all questionable transactions between guardian and ward. Disclose any potential conflicts to court and obtain approval before proceeding. Do not employ family members or use ward's assets for personal benefit. For challengers: prove transaction benefited guardian at ward's expense.",
        entity_scope="Guardians, wards, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Strict prohibition on self-dealing without court approval",
        category=IssueCategory.DUTIES
    ),
    DoctrineBlock(
        topic="Limited Guardianship Tailored to Individual Needs",
        keywords=["limited guardianship", "partial", "specific powers", "tailored", "individualized", "retained rights"],
        conclusion_template="Limited guardianships restrict only those rights the ward cannot exercise while preserving maximum autonomy. Courts must tailor guardianship orders to individual circumstances, specifying which powers are restricted and which rights the ward retains. Limited guardianship is preferred over full guardianship when adequate to protect the ward.",
        reasoning_framework="""Texas Estates Code Section 1101.151 authorizes limited guardianships granting only those powers necessary to provide care and protection the ward lacks capacity to provide. The guardianship order must specifically enumerate restricted rights and powers, with all other rights retained by ward. Examples of limited guardianships include: guardian of estate only with ward retaining personal decisions, limited authority over specific property, or limited powers over medical decisions with ward retaining other personal rights. Courts must make findings regarding specific areas of incapacity. The limited guardianship reflects modern trend toward individualized, least restrictive alternatives. Limited guardianships may be expanded if ward's condition deteriorates or restricted if capacity improves. The key is tailoring court intervention to actual deficits rather than imposing blanket incapacity.""",
        key_factors=[
            "Order must specify which rights restricted",
            "Ward retains all rights not specifically restricted",
            "Guardianship tailored to individual deficits",
            "Limited guardianship preferred when adequate",
            "Court findings required for restricted areas",
            "May be modified as ward's capacity changes",
            "Preserves maximum ward autonomy"
        ],
        primary_authority=[
            "Texas Estates Code Section 1101.151",
            "Texas Estates Code Section 1101.152 (order must specify rights)",
            "In re Guardianship of Rodriguez, 364 S.W.3d 833 (Tex. App. 2012)"
        ],
        burden_holder="Applicant to show necessity of each restricted right",
        adversary_position="Proposed ward argues capacity exists for certain decisions",
        counter_arguments=[
            "Ward capable of making personal decisions",
            "Ward retains capacity to manage some property",
            "Full guardianship unnecessarily restrictive",
            "Specific deficits identified but not global incapacity"
        ],
        resolution_strategy="Present evidence of specific functional deficits requiring intervention. Show which decisions ward can make and which require assistance. Request order specifying limited powers. For opponents: demonstrate retained capacity for specific decisions and adequacy of limited protection.",
        entity_scope="Proposed wards with partial capacity, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Limited guardianship required when adequate to protect ward",
        category=IssueCategory.APPOINTMENT
    ),
    DoctrineBlock(
        topic="Powers of Attorney as Guardianship Alternative",
        keywords=["power of attorney", "POA", "durable", "agent", "principal", "alternative", "springing"],
        conclusion_template="Durable powers of attorney executed while competent authorize agents to make financial and medical decisions without court involvement. POAs provide less restrictive alternative to guardianship but may be challenged if executed when principal lacked capacity, agent abuses authority, or POA fails to address current needs.",
        reasoning_framework="""Texas Estates Code Title 2 Subtitle P governs durable powers of attorney authorizing agents to act for principals. A properly executed durable POA survives principal's subsequent incapacity and may eliminate need for guardianship. Medical POAs authorize healthcare decisions. Property POAs authorize financial management. POAs may be broad or limited to specific powers. The principal must have capacity when executing POA. POAs may be springing (effective upon incapacity) or immediate. Advantages over guardianship include: no court involvement, privacy, lower cost, and principal's choice of agent. Disadvantages include: no court oversight, potential for agent abuse, third parties may question authority. Courts will appoint guardian despite existing POA if: POA executed when principal lacked capacity, agent is abusing authority, POA powers inadequate for current needs, or court oversight necessary. POAs may be revoked while principal has capacity.""",
        key_factors=[
            "Must be executed while principal has capacity",
            "Survives principal's subsequent incapacity if durable",
            "No court involvement or oversight",
            "Agent must act in principal's best interest",
            "Third parties may question agent authority",
            "May be revoked while principal competent",
            "Guardianship may still be necessary despite POA"
        ],
        primary_authority=[
            "Texas Estates Code Section 751.001 et seq (property POA)",
            "Texas Health and Safety Code Section 166.151 et seq (medical POA)",
            "Texas Estates Code Section 1104.353 (POA nomination of guardian)"
        ],
        burden_holder="Guardianship applicant to show POA inadequate or invalid",
        adversary_position="Proposed ward or agent argues POA adequate alternative",
        counter_arguments=[
            "POA executed when principal had capacity",
            "Agent faithfully serving principal's interests",
            "POA powers adequate for current needs",
            "Court oversight unnecessary expense"
        ],
        resolution_strategy="For guardianship applicants: prove principal lacked capacity when POA executed, demonstrate agent abuse or conflicts, show POA powers insufficient. For POA proponents: present evidence of valid execution, agent's faithful service, and adequacy of POA authority.",
        entity_scope="Principals, agents, proposed wards",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Valid POA may preclude need for guardianship",
        category=IssueCategory.ALTERNATIVES
    ),
    DoctrineBlock(
        topic="Guardianship of Veterans and VA Benefits",
        keywords=["veteran", "VA benefits", "fiduciary", "representative payee", "military", "disability"],
        conclusion_template="Veterans receiving VA disability benefits may require guardians to manage benefits and property. The VA may appoint its own fiduciary to receive benefits or recognize a court-appointed guardian. Coordination between state guardianship and VA fiduciary processes is necessary to avoid conflicts and ensure veteran receives proper care.",
        reasoning_framework="""Veterans with VA disability benefits who become incapacitated present unique guardianship issues. The VA has its own system for appointing fiduciaries to receive and manage benefits when veteran is incapable. State courts may appoint guardians with overlapping authority. Coordination is essential to avoid conflicts. The VA fiduciary receives the veteran's benefits and must use them for veteran's care. Court-appointed guardians manage the veteran's other property. The VA may recognize the court-appointed guardian as VA fiduciary, consolidating responsibilities. VA fiduciaries must file annual accountings with VA. Special rules apply to guardianships of minor children receiving VA survivor benefits. The guardian must not compromise the veteran's VA claims or benefits. Priority for veteran guardians may differ from general priority rules. Veterans' courts in some counties have specialized procedures.""",
        key_factors=[
            "VA may appoint separate fiduciary for benefits",
            "Court guardian may seek recognition as VA fiduciary",
            "Coordination necessary to avoid conflicts",
            "VA fiduciary accountable to VA",
            "Special rules for minor survivors' benefits",
            "Guardian must protect veteran's VA claims",
            "Specialized veterans' courts in some counties"
        ],
        primary_authority=[
            "38 U.S.C. Section 5502 (VA fiduciary)",
            "Texas Estates Code (general guardianship law)",
            "38 C.F.R. Part 13 (VA fiduciary regulations)"
        ],
        burden_holder="Guardian to coordinate with VA and protect benefits",
        adversary_position="VA or interested parties challenge benefit management",
        counter_arguments=[
            "Court guardian not recognized by VA as fiduciary",
            "Conflict between VA fiduciary and court guardian",
            "Benefits not being used for veteran's care",
            "Guardian failed to protect VA claims"
        ],
        resolution_strategy="Seek recognition as VA fiduciary when appointed guardian. Maintain communication with VA fiduciary hub. Account separately for VA benefits and other property. Ensure benefits used for veteran's care. Consult veterans' law specialists for complex issues.",
        entity_scope="Veteran wards, VA fiduciaries, guardians",
        confidence=ConfidenceLevel.DISCLOSURE,
        controlling_precedent="Federal VA law interacts with state guardianship law",
        category=IssueCategory.POWERS
    ),
    DoctrineBlock(
        topic="Appointment of Corporate or Professional Guardians",
        keywords=["corporate guardian", "professional", "guardianship program", "nonprofit", "certification", "for-profit"],
        conclusion_template="When family members are unavailable or unsuitable, courts may appoint corporate or professional guardians including certified private guardians, guardianship programs, or corporate fiduciaries. Professional guardians must meet certification and training requirements and typically charge fees from the estate.",
        reasoning_framework="""Texas allows appointment of professional guardians when appropriate individuals are unavailable. Options include: certified private professional guardians licensed by Department of Aging and Disability Services, guardianship programs operated by nonprofits or governmental entities, corporate fiduciaries such as banks and trust companies. Professional guardians must meet certification requirements including training, background checks, and bonding. Courts appoint professionals when no family member willing or able to serve, family conflicts exist, estate is complex requiring expertise, or ward's best interest requires neutral party. Professional guardians charge fees which must be approved by court and paid from ward's estate. If ward is indigent, county may pay from guardianship fund. Professional guardians typically manage multiple wards simultaneously. Certification may be revoked for misconduct. The rise of professional guardianship addresses need for services but raises concerns about costs and quality of care.""",
        key_factors=[
            "Certification required for private professional guardians",
            "Corporate fiduciaries may serve as guardians",
            "Nonprofit guardianship programs available",
            "Professional guardians charge court-approved fees",
            "County may pay for indigent wards",
            "Appointed when family unavailable or unsuitable",
            "Professional guardians may manage multiple wards"
        ],
        primary_authority=[
            "Texas Estates Code Section 1104.354 (corporate guardian)",
            "Texas Government Code Section 155.001 et seq (guardianship programs)",
            "40 TAC Chapter 68 (certification requirements)"
        ],
        burden_holder="Professional guardian to prove qualification and fitness",
        adversary_position="Family members or court question professional's suitability",
        counter_arguments=[
            "Family member available and willing to serve",
            "Professional guardian's fees excessive",
            "Quality of care concerns with high caseload",
            "Professional has conflicts or is unsuitable"
        ],
        resolution_strategy="For professional guardians: demonstrate certification, experience, absence of conflicts, and reasonable fee structure. For family applicants: show availability and ability to serve without professional assistance. Courts balance family preference against need for professional expertise.",
        entity_scope="Professional guardians, wards without family, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Professional guardians fill need when family unavailable",
        category=IssueCategory.APPOINTMENT
    ),
    DoctrineBlock(
        topic="Guardian's Authority Over Ward's Residence and Living Situation",
        keywords=["residence", "placement", "nursing home", "facility", "living arrangement", "institutional care"],
        conclusion_template="Guardians of the person have authority to determine ward's residence but court approval is required for placement in certain facilities including nursing homes, assisted living, and psychiatric facilities. The guardian must select the least restrictive setting appropriate for ward's needs and consider ward's preferences.",
        reasoning_framework="""Texas Estates Code Section 1151.052 grants guardians authority over ward's residence while requiring court approval for restrictive placements. Guardian may choose ward's residence considering safety, care needs, and preferences. Court approval is required before placing ward in: nursing facility, assisted living facility, psychiatric hospital, or other institutional setting. The application for facility placement must include physician certification of need. Courts apply least restrictive alternative analysis - community placement preferred over institutional care when appropriate. Guardian must visit ward's residence to verify suitability. Ward's preference regarding residence should be considered. Inappropriate placement may constitute neglect warranting removal of guardian. Guardian may not move ward to another state without court approval. The residence decision must serve ward's best interest balancing independence with needed care and supervision.""",
        key_factors=[
            "Guardian determines residence of ward",
            "Court approval required for institutional placement",
            "Physician certification needed for facility placement",
            "Least restrictive setting appropriate to needs",
            "Ward's preferences should be considered",
            "Regular visits to verify living situation",
            "Interstate move requires court approval"
        ],
        primary_authority=[
            "Texas Estates Code Section 1151.052",
            "Texas Estates Code Section 1151.054 (facility placement)",
            "Texas Health and Safety Code Section 242.003 (nursing facility admission)"
        ],
        burden_holder="Guardian to prove placement appropriate and least restrictive",
        adversary_position="Ward or family challenge placement decision",
        counter_arguments=[
            "Placement more restrictive than necessary",
            "Ward capable of living in community with services",
            "Ward opposes institutional placement",
            "Less restrictive alternatives available",
            "Facility selected inappropriate for ward's needs"
        ],
        resolution_strategy="Obtain medical evaluation supporting need for level of care. Demonstrate less restrictive options inadequate for ward's needs. Document consideration of ward's preferences. Show facility appropriate for ward's condition. For challengers: present evidence of alternatives and ward's ability to manage in less restrictive setting.",
        entity_scope="Guardians of person, wards, care facilities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Court approval required for restrictive placements",
        category=IssueCategory.POWERS
    ),
    DoctrineBlock(
        topic="Emergency Orders and Immediate Protection",
        keywords=["emergency", "immediate harm", "protective order", "ex parte", "urgent", "irreparable injury"],
        conclusion_template="Courts may issue emergency protective orders when proposed ward or estate faces immediate and irreparable harm. Emergency orders may include temporary guardian appointment, restraining orders against third parties, freezing assets, or requiring immediate medical treatment. Such orders require specific findings of emergency and are limited in duration pending full hearing.",
        reasoning_framework="""Texas law authorizes emergency court intervention when delay for full hearing would result in immediate and irreparable harm to proposed ward or estate. Emergency orders may be issued ex parte (without notice) when giving notice would eliminate possibility of protection. Examples of emergencies include: medical crisis requiring immediate consent, ongoing financial exploitation, physical abuse or neglect, dangerous living situation, or imminent loss of property. The application must present specific facts demonstrating immediate harm not general allegations of vulnerability. Courts issue protective orders with narrow scope limited to addressing the emergency. Emergency orders remain in effect until full hearing which must be scheduled promptly. The proposed ward receives notice after emergency order and has right to immediate hearing to contest. Emergency jurisdiction is strictly construed to protect due process rights.""",
        key_factors=[
            "Immediate and irreparable harm required",
            "Specific facts demonstrating emergency",
            "Ex parte orders only if notice defeats protection",
            "Limited scope addressing the emergency",
            "Temporary duration until full hearing",
            "Full hearing must follow promptly",
            "Strict construction to protect due process"
        ],
        primary_authority=[
            "Texas Estates Code Section 1251.001 (temporary guardian)",
            "Texas Estates Code Section 1251.102 (temporary order)",
            "Texas Civil Practice and Remedies Code Section 65.001 (temporary restraining order)"
        ],
        burden_holder="Emergency applicant to prove immediate irreparable harm",
        adversary_position="Proposed ward contests existence of emergency",
        counter_arguments=[
            "No immediate emergency exists",
            "Situation stable pending full hearing",
            "Less drastic measures available",
            "Delay for notice would not cause irreparable harm"
        ],
        resolution_strategy="Present specific evidence of imminent harm with timeframe. Show why informal alternatives insufficient. Limit requested relief to minimum necessary to address emergency. For opponents: demonstrate stability of situation or availability of less restrictive protective measures.",
        entity_scope="Proposed wards facing emergencies, courts",
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent="Emergency orders strictly limited to prevent due process violations",
        category=IssueCategory.PROCEDURE
    ),
    DoctrineBlock(
        topic="Guardian Liability for Negligence or Misconduct",
        keywords=["liability", "negligence", "breach of duty", "damages", "surcharge", "personal liability"],
        conclusion_template="Guardians may be held personally liable for damages caused by negligence or breach of fiduciary duty. Liability may include surcharge requiring guardian to reimburse estate for losses, removal from office, denial of compensation, and in egregious cases criminal prosecution. The guardian's bond provides source of recovery for estate.",
        reasoning_framework="""As fiduciaries, guardians are personally liable for losses caused by breach of duty. Liability may arise from: mismanagement or loss of estate assets, failure to file required reports, self-dealing transactions, neglect or abuse of ward, unauthorized actions, or conflicts of interest. Courts may surcharge guardians requiring personal reimbursement of estate losses. The surcharge remedy makes guardian personally liable even if bonded. Criminal liability may arise for theft, exploitation, or abuse. Civil liability may include damages for injury to ward from neglect. The guardian's bond provides security for estate losses but does not eliminate personal liability. Guardians may be removed and denied compensation for breach of duty. Professional guardians may lose certification. Insurance may not cover intentional misconduct. The potential liability emphasizes the serious nature of fiduciary responsibilities.""",
        key_factors=[
            "Personal liability for breach of fiduciary duty",
            "Surcharge remedy for estate losses",
            "Criminal prosecution for theft or abuse",
            "Civil damages for injury from neglect",
            "Bond provides security but not immunity",
            "Removal and denial of compensation possible",
            "Professional guardians may lose certification"
        ],
        primary_authority=[
            "Texas Estates Code Section 1203.051 (surcharge)",
            "Texas Penal Code Section 32.45 (misapplication of fiduciary property)",
            "Texas Human Resources Code Section 48.002 (exploitation of elderly)"
        ],
        burden_holder="Claimant to prove breach of duty and damages",
        adversary_position="Guardian defends conduct as reasonable and proper",
        counter_arguments=[
            "Guardian acted reasonably and in good faith",
            "Losses resulted from market conditions not negligence",
            "Actions were within guardian's authority",
            "No damages resulted from alleged breach"
        ],
        resolution_strategy="For claimants: document specific breaches and resulting losses. Present expert testimony on proper fiduciary standards. Seek surcharge and removal. For guardians: demonstrate good faith, reasonable care, and compliance with duties. Show losses not caused by breach.",
        entity_scope="Guardians, wards' estates, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Strict fiduciary liability for breach of duty",
        category=IssueCategory.DUTIES
    )
]

# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    def __init__(self) -> None:
        self.metrics: Dict[str, Any] = defaultdict(lambda: {"count": 0, "total_ms": 0.0})
        self.query_log: List[Dict[str, Any]] = []
        self.error_log: List[Dict[str, Any]] = []

    def record_query(self, question: str, mode: str, latency_ms: float, doctrines: List[str]) -> None:
        self.query_log.append({
            "timestamp": datetime.now().isoformat(),
            "question": question[:100],
            "mode": mode,
            "latency_ms": latency_ms,
            "doctrines_count": len(doctrines)
        })
        self.metrics[f"mode_{mode}"]["count"] += 1
        self.metrics[f"mode_{mode}"]["total_ms"] += latency_ms

    def record_error(self, error_type: str, message: str) -> None:
        self.error_log.append({
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "message": message
        })
        self.metrics["errors"]["count"] += 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": len(self.query_log),
            "total_errors": len(self.error_log),
            "metrics": dict(self.metrics),
            "recent_queries": self.query_log[-10:]
        }

TELEMETRY = TelemetryCollector()

# ═══════════════════════════════════════════════════════════════════════════
# DRIFT WATCHER & COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    def __init__(self) -> None:
        self.doctrine_usage: Dict[str, int] = defaultdict(int)
        self.last_reset = datetime.now()

    def record_usage(self, doctrine_topics: List[str]) -> None:
        for topic in doctrine_topics:
            self.doctrine_usage[topic] += 1

    def get_drift_report(self) -> Dict[str, Any]:
        total = sum(self.doctrine_usage.values())
        return {
            "total_triggers": total,
            "unique_doctrines": len(self.doctrine_usage),
            "top_doctrines": sorted(self.doctrine_usage.items(), key=lambda x: x[1], reverse=True)[:5],
            "since": self.last_reset.isoformat()
        }

DRIFT_WATCHER = DriftWatcher()

class CoverageMap:
    def __init__(self) -> None:
        self.triggered: Set[str] = set()
        self.total_doctrines = len(DOCTRINE_CACHE)

    def mark_triggered(self, topics: List[str]) -> None:
        self.triggered.update(topics)

    def get_coverage(self) -> Dict[str, Any]:
        all_topics = {d.topic for d in DOCTRINE_CACHE}
        missed = all_topics - self.triggered
        return {
            "triggered_count": len(self.triggered),
            "total_doctrines": self.total_doctrines,
            "coverage_pct": round(100 * len(self.triggered) / self.total_doctrines, 1),
            "missed_topics": sorted(missed)
        }

COVERAGE_MAP = CoverageMap()

# ═══════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def semantic_match(question: str, keywords: List[str]) -> float:
    q_lower = question.lower()
    matches = sum(1 for kw in keywords if kw.lower() in q_lower)
    return matches / len(keywords) if keywords else 0.0

def doctrine_cache_layer(question: str, top_n: int = 3) -> List[DoctrineBlock]:
    scored = [(d, semantic_match(question, d.keywords)) for d in DOCTRINE_CACHE]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [d for d, score in scored[:top_n] if score > 0.1]

def deep_analysis_layer(question: str, context: Optional[Dict[str, Any]], zone: AnalysisZone) -> str:
    doctrines = doctrine_cache_layer(question, top_n=5)
    if not doctrines:
        return f"No directly applicable guardianship doctrines found. General analysis: {zone.value} zone requires comprehensive legal research beyond cached doctrines. Consider consulting Estates Code Chapters 1001-1355 for specific guidance on guardianship matters."

    reasoning_parts = []
    for d in doctrines:
        reasoning_parts.append(f"DOCTRINE: {d.topic}\n{d.reasoning_framework}\n\nKEY FACTORS: {', '.join(d.key_factors)}\n")

    synthesis = "\n\n".join(reasoning_parts)
    return f"DEEP ANALYSIS ({zone.value} ZONE):\n\n{synthesis}\n\nThe analysis synthesizes {len(doctrines)} doctrines to provide comprehensive guidance on guardianship law."

def three_layer_response(question: str, mode: ResponseMode, zone: AnalysisZone, context: Optional[Dict[str, Any]]) -> Tuple[str, List[str], ConfidenceLevel]:
    doctrines = doctrine_cache_layer(question)

    if not doctrines:
        deep = deep_analysis_layer(question, context, zone)
        return deep, [], ConfidenceLevel.DISCLOSURE

    topics = [d.topic for d in doctrines]
    authorities = []
    for d in doctrines:
        authorities.extend(d.primary_authority)

    if mode == ResponseMode.FAST:
        answer = doctrines[0].conclusion_template
        confidence = doctrines[0].confidence
    elif mode == ResponseMode.DEFENSE:
        parts = [f"{d.topic}: {d.conclusion_template}" for d in doctrines]
        answer = "\n\n".join(parts)
        answer += f"\n\nAUTHORITIES: {'; '.join(set(authorities))}"
        confidence = ConfidenceLevel.DEFENSIBLE
    else:  # MEMO
        answer = deep_analysis_layer(question, context, zone)
        confidence = ConfidenceLevel.DEFENSIBLE

    return answer, topics, confidence

# ═══════════════════════════════════════════════════════════════════════════
# DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(question: str, mode: str, answer: str) -> str:
    payload = f"{question}|{mode}|{answer}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event() -> None:
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} guardianship doctrine blocks")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info(f"{ENGINE_NAME} shutting down")

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "total_queries": len(TELEMETRY.query_log),
        "uptime_seconds": (datetime.now() - TELEMETRY.query_log[0]["timestamp"] if TELEMETRY.query_log else 0)
    }

@app.post("/query", response_model=QueryResponse)
async def query_engine(req: QueryRequest) -> QueryResponse:
    start_time = time.time()

    try:
        answer, topics, confidence = three_layer_response(
            req.question, req.mode, req.zone, req.context
        )

        authorities = []
        for d in DOCTRINE_CACHE:
            if d.topic in topics:
                authorities.extend(d.primary_authority)

        latency_ms = (time.time() - start_time) * 1000
        det_hash = compute_determinism_hash(req.question, req.mode.value, answer)

        TELEMETRY.record_query(req.question, req.mode.value, latency_ms, topics)
        DRIFT_WATCHER.record_usage(topics)
        COVERAGE_MAP.mark_triggered(topics)

        warnings = []
        if req.zone == AnalysisZone.AUDIT:
            warnings.append("AUDIT ZONE: All conclusions require independent verification")
        if confidence == ConfidenceLevel.HIGH_RISK:
            warnings.append("HIGH RISK: Seek specialized guardianship counsel")

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            doctrines_triggered=topics,
            authorities_cited=sorted(set(authorities)),
            determinism_hash=det_hash,
            telemetry={
                "latency_ms": round(latency_ms, 2),
                "doctrines_evaluated": len(DOCTRINE_CACHE),
                "mode": req.mode.value,
                "zone": req.zone.value
            },
            warnings=warnings,
            zone=req.zone
        )

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        TELEMETRY.record_error("query_error", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    return {
        "telemetry": TELEMETRY.get_stats(),
        "drift": DRIFT_WATCHER.get_drift_report(),
        "coverage": COVERAGE_MAP.get_coverage()
    }

@app.get("/doctrines")
async def list_doctrines() -> Dict[str, Any]:
    return {
        "total": len(DOCTRINE_CACHE),
        "by_category": {cat.value: len([d for d in DOCTRINE_CACHE if d.category == cat]) for cat in IssueCategory},
        "topics": [d.topic for d in DOCTRINE_CACHE]
    }

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
