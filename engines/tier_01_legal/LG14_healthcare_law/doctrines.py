"""
LG14 Healthcare Law Engine - Doctrine Cache Module
======================================================
Pre-compiled healthcare law doctrine blocks for instant retrieval on common
HIPAA, fraud/abuse, malpractice, FDA, EMTALA, telemedicine, clinical trials,
ACA, mental health parity, pharmacy, and regulatory compliance queries.

Each doctrine block contains:
    - topic: Canonical topic identifier
    - summary: Executive-level overview of the doctrine
    - key_statutes: Controlling statutory references
    - elements: Legal elements or requirements
    - defenses: Common defenses or exceptions
    - remedies: Available remedies or relief
    - leading_cases: Landmark case citations

Components:
    - DOCTRINE_BLOCKS: List of pre-compiled doctrine cache entries
    - DoctrineCacheBlock: Structured doctrine entry model
    - DoctrineCacheIndex: Fast O(1) lookup by topic/category
    - build_doctrine_cache(): Build the complete cache from blocks
    - get_doctrine_block(): Retrieve a single block by topic
    - search_doctrines(): Free-text search over doctrine blocks
    - get_coverage_map(): Map of all topics with staleness data

Version: 2.0.0
Engine: LG14 Healthcare Law
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Any, ClassVar, Dict, List, Optional, Set

from loguru import logger


# ============================================================================
# DOCTRINE CACHE BLOCK MODEL
# ============================================================================

@dataclass
class DoctrineCacheBlock:
    """A single pre-compiled healthcare law doctrine cache entry."""

    topic: str
    summary: str
    key_statutes: List[str]
    elements: List[str]
    defenses: List[str]
    remedies: List[str]
    leading_cases: List[str]
    category: str
    subcategory: str = ""
    jurisdiction: str = "federal"
    authority_score: float = 0.75
    confidence: float = 0.80
    last_updated: str = ""
    staleness_days: int = 0
    related_topics: List[str] = dc_field(default_factory=list)
    practice_tips: List[str] = dc_field(default_factory=list)
    risk_factors: List[str] = dc_field(default_factory=list)
    regulatory_notes: str = ""

    def __post_init__(self) -> None:
        if not self.last_updated:
            self.last_updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "summary": self.summary,
            "key_statutes": self.key_statutes,
            "elements": self.elements,
            "defenses": self.defenses,
            "remedies": self.remedies,
            "leading_cases": self.leading_cases,
            "category": self.category,
            "subcategory": self.subcategory,
            "jurisdiction": self.jurisdiction,
            "authority_score": round(self.authority_score, 4),
            "confidence": round(self.confidence, 4),
            "last_updated": self.last_updated,
            "staleness_days": self.staleness_days,
            "related_topics": self.related_topics,
            "practice_tips": self.practice_tips,
            "risk_factors": self.risk_factors,
            "regulatory_notes": self.regulatory_notes,
        }

    def content_for_search(self) -> str:
        """Generate searchable text content from all fields."""
        parts = [
            self.topic,
            self.summary,
            " ".join(self.key_statutes),
            " ".join(self.elements),
            " ".join(self.defenses),
            " ".join(self.remedies),
            " ".join(self.leading_cases),
            self.category,
            self.subcategory,
            self.regulatory_notes,
            " ".join(self.practice_tips),
        ]
        return " ".join(parts)

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of the block content."""
        content = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# DOCTRINE BLOCKS - HIPAA PRIVACY
# ============================================================================

DOCTRINE_BLOCKS: List[DoctrineCacheBlock] = [
    DoctrineCacheBlock(
        topic="hipaa_privacy_rule",
        summary="The HIPAA Privacy Rule (45 CFR Part 164 Subpart E) establishes national standards for the protection of individually identifiable health information (protected health information or PHI). Covered entities (health plans, healthcare clearinghouses, and healthcare providers who transmit health information electronically) must implement policies and procedures to protect PHI, provide patients with rights regarding their information, and limit uses and disclosures to the minimum necessary. The Privacy Rule permits uses and disclosures for treatment, payment, and healthcare operations (TPO) without individual authorization. Other uses generally require written authorization. The Rule also establishes individual rights including the right to access, amend, and receive an accounting of disclosures of PHI.",
        key_statutes=[
            "45 CFR 164.500-164.534 (Privacy Rule)",
            "45 CFR 164.502 (Uses and disclosures of PHI)",
            "45 CFR 164.508 (Authorization requirements)",
            "45 CFR 164.510 (Uses for facility directories and emergencies)",
            "45 CFR 164.512 (Uses and disclosures without authorization)",
            "45 CFR 164.524 (Right of access)",
            "45 CFR 164.526 (Right to amend)",
            "42 USC 1320d et seq. (HIPAA statutory authority)",
        ],
        elements=[
            "Entity is a covered entity or business associate",
            "Information constitutes protected health information (PHI)",
            "Use or disclosure of PHI occurred",
            "No applicable exception to authorization requirement",
            "Minimum necessary standard not applied",
            "Notice of Privacy Practices not provided or inadequate",
            "Individual rights not honored (access, amendment, accounting)",
            "Policies and procedures not implemented or followed",
        ],
        defenses=[
            "Treatment, payment, or healthcare operations (TPO) exception",
            "Valid individual authorization obtained",
            "Public health activity exception (45 CFR 164.512(b))",
            "Judicial or administrative proceeding exception",
            "Law enforcement exception (45 CFR 164.512(f))",
            "De-identified data (Safe Harbor or Expert Determination method)",
            "Limited data set with data use agreement",
            "Incidental disclosure with reasonable safeguards",
            "Minimum necessary standard properly applied",
        ],
        remedies=[
            "OCR corrective action plan and compliance agreement",
            "Civil monetary penalties (42 USC 1320d-5): $100-$50,000 per violation, up to $1.5M per calendar year per identical provision",
            "Criminal penalties (42 USC 1320d-6): up to $250,000 fine and 10 years imprisonment for knowingly obtaining/disclosing PHI",
            "State attorney general enforcement (HITECH SS 13410(e))",
            "Resolution agreements with HHS OCR",
            "Individual complaint to OCR",
        ],
        leading_cases=[
            "Byrne v. Avery Center for Obstetrics and Gynecology, 314 Conn. 433 (2014) - state negligence claims not preempted by HIPAA",
            "Dittman v. UPMC, 196 A.3d 1036 (Pa. 2018) - negligence action for data breach",
            "Ciox Health LLC v. Azar, 435 F. Supp. 3d 30 (D.D.C. 2020) - challenge to HHS right of access guidance",
            "University of Texas MD Anderson Cancer Center v. HHS, 973 F.3d 1 (5th Cir. 2020) - $4.3M CMP reversed on reasonableness grounds",
        ],
        category="hipaa",
        subcategory="privacy_rule",
        authority_score=0.90,
        confidence=0.92,
        related_topics=["hipaa_security_rule", "hipaa_breach_notification", "business_associate_agreements", "patient_access_rights", "minimum_necessary"],
        practice_tips=[
            "Conduct regular Privacy Rule training for all workforce members",
            "Maintain an up-to-date Notice of Privacy Practices",
            "Document all authorization and disclosure decisions",
            "Implement minimum necessary policies for every role",
            "Track the 30-day deadline for patient access requests",
        ],
        risk_factors=[
            "OCR Right of Access Initiative has resulted in numerous enforcement actions",
            "State laws may impose stricter privacy protections that are not preempted",
            "Business associate breaches trigger covered entity notification obligations",
        ],
        regulatory_notes="OCR has made Right of Access enforcement a top priority since 2019, with over 40 enforcement actions. The 2024 HIPAA Privacy Rule NPRM proposes strengthening individual access rights and reducing authorization requirements for care coordination.",
    ),

    DoctrineCacheBlock(
        topic="hipaa_security_rule",
        summary="The HIPAA Security Rule (45 CFR Part 164 Subpart C) establishes national standards for protecting electronic protected health information (ePHI). Covered entities and business associates must implement administrative, physical, and technical safeguards to ensure the confidentiality, integrity, and availability of ePHI. The Security Rule requires a risk analysis, risk management plan, and ongoing evaluation. Safeguards are classified as required or addressable; addressable safeguards must be implemented if reasonable and appropriate, or the entity must document why they are not and implement an alternative measure.",
        key_statutes=[
            "45 CFR 164.302-164.318 (Security Rule)",
            "45 CFR 164.308 (Administrative safeguards)",
            "45 CFR 164.310 (Physical safeguards)",
            "45 CFR 164.312 (Technical safeguards)",
            "45 CFR 164.314 (Organizational requirements)",
            "45 CFR 164.316 (Policies, procedures, documentation)",
        ],
        elements=[
            "Entity is a covered entity or business associate handling ePHI",
            "Failure to conduct accurate and thorough risk analysis",
            "Failure to implement required administrative safeguards",
            "Failure to implement physical safeguards for ePHI",
            "Failure to implement technical safeguards (access controls, audit controls, integrity controls, transmission security)",
            "Failure to maintain documentation of security policies",
            "Addressable specification not implemented without documented rationale",
            "Failure to regularly review and update security measures",
        ],
        defenses=[
            "Risk analysis conducted and documented per NIST SP 800-66",
            "Addressable specifications documented with alternative measures",
            "Reasonable and appropriate safeguards in place given entity size and complexity",
            "Encryption at rest and in transit implemented",
            "Incident response plan tested and followed",
            "Security awareness training conducted for all workforce members",
        ],
        remedies=[
            "OCR enforcement: corrective action plans, resolution agreements",
            "Civil monetary penalties: tiered penalty structure up to $1.5M per violation category per year",
            "State attorney general enforcement under HITECH",
            "FTC enforcement for unfair or deceptive practices",
            "Private litigation (where state law permits)",
        ],
        leading_cases=[
            "Premera Blue Cross OCR Settlement (2020) - $6.85M for breach affecting 10.4M individuals",
            "Anthem Inc. OCR Settlement (2018) - $16M for largest health data breach",
            "Banner Health OCR Settlement (2023) - $1.25M for phishing attack failures",
            "HHS v. University of Texas MD Anderson, 973 F.3d 1 (5th Cir. 2020) - encryption requirement analysis",
        ],
        category="hipaa",
        subcategory="security_rule",
        authority_score=0.90,
        confidence=0.90,
        related_topics=["hipaa_privacy_rule", "hipaa_breach_notification", "risk_analysis", "encryption_requirements"],
        practice_tips=[
            "Conduct an enterprise-wide risk analysis at least annually using NIST SP 800-66 framework",
            "Document all addressable specification decisions with rationale",
            "Implement encryption for all ePHI at rest and in transit",
            "Test incident response plans through tabletop exercises",
            "Maintain audit logs with automated review capabilities",
        ],
        risk_factors=[
            "Failure to conduct risk analysis is the most frequently cited HIPAA deficiency",
            "Legacy systems without encryption create significant exposure",
            "Business associate oversight failures compound covered entity liability",
        ],
        regulatory_notes="HHS proposed significant HIPAA Security Rule updates in 2024 that would make all safeguards required (eliminating addressable distinction), mandate encryption, require annual compliance audits, and add new technology asset inventory requirements.",
    ),

    DoctrineCacheBlock(
        topic="hipaa_breach_notification",
        summary="The HIPAA Breach Notification Rule (45 CFR Part 164 Subpart D) requires covered entities and business associates to notify affected individuals, HHS, and in some cases the media, following a breach of unsecured PHI. A breach is the acquisition, access, use, or disclosure of PHI in a manner not permitted by the Privacy Rule that compromises the security or privacy of the PHI. The 2013 Omnibus Rule established a presumption that any impermissible use or disclosure constitutes a breach unless the covered entity can demonstrate through a risk assessment that there is a low probability the PHI has been compromised.",
        key_statutes=[
            "45 CFR 164.400-164.414 (Breach Notification Rule)",
            "45 CFR 164.402 (Definitions - breach, unsecured PHI)",
            "45 CFR 164.404 (Individual notification)",
            "45 CFR 164.406 (Media notification)",
            "45 CFR 164.408 (HHS notification)",
            "HITECH Act SS 13402 (Breach notification requirements)",
        ],
        elements=[
            "Impermissible acquisition, access, use, or disclosure of PHI",
            "PHI was unsecured (not rendered unusable per HHS guidance)",
            "Four-factor risk assessment not conducted or shows compromise",
            "Notification to individuals not provided within 60 days of discovery",
            "Notification to HHS not provided (annually for <500 individuals; within 60 days for 500+)",
            "Media notification not provided for breaches affecting 500+ in a state or jurisdiction",
        ],
        defenses=[
            "PHI was encrypted per NIST standards (safe harbor - renders PHI unusable)",
            "Four-factor risk assessment demonstrates low probability of compromise",
            "Unintentional acquisition by workforce member acting in good faith",
            "Inadvertent disclosure to another authorized person within the entity",
            "Good faith belief that unauthorized recipient could not retain the information",
            "Notification was provided within required timeframes",
        ],
        remedies=[
            "Individual notification with description of breach, types of PHI involved, remediation steps",
            "HHS OCR investigation and corrective action plan",
            "Civil monetary penalties for failure to notify",
            "State attorney general enforcement and state breach notification law penalties",
            "Identity theft monitoring services for affected individuals",
            "Class action litigation for damages",
        ],
        leading_cases=[
            "In re Anthem Data Breach Litigation, 162 F. Supp. 3d 953 (N.D. Cal. 2016) - standing for data breach claims",
            "Dittman v. UPMC, 196 A.3d 1036 (Pa. 2018) - employer duty to safeguard employee data",
            "Banner Health OCR Resolution Agreement (2023) - breach notification obligations after phishing",
            "Community Health Systems Settlement (2019) - $5M state AG settlement for breach",
        ],
        category="hipaa",
        subcategory="breach_notification",
        authority_score=0.88,
        confidence=0.90,
        related_topics=["hipaa_privacy_rule", "hipaa_security_rule", "encryption_requirements", "risk_analysis"],
        practice_tips=[
            "Apply the four-factor risk assessment to every potential breach: nature of PHI, unauthorized person, actual viewing, extent of mitigation",
            "Maintain a breach log even for breaches affecting fewer than 500 individuals",
            "Train workforce on immediate internal breach reporting procedures",
            "Have pre-drafted notification templates ready for rapid deployment",
            "Coordinate with state breach notification law requirements which may have shorter timelines",
        ],
        risk_factors=[
            "60-day notification clock starts on discovery, not investigation completion",
            "State laws may require faster notification (e.g., California 15 days for certain breaches)",
            "Large breaches attract media attention and class action litigation",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - FRAUD AND ABUSE
    # ============================================================================

    DoctrineCacheBlock(
        topic="false_claims_act",
        summary="The False Claims Act (31 USC 3729-3733) is the federal government's primary tool for combating healthcare fraud. It imposes liability on any person who knowingly submits or causes the submission of a false or fraudulent claim for payment to the federal government. The FCA's qui tam provisions allow private whistleblowers (relators) to bring suits on behalf of the government and receive a share (15-30%) of any recovery. The 2009 FERA amendments broadened the definition of 'claim' and clarified that overpayment retention can constitute a false claim. Treble damages and per-claim penalties make FCA exposure significant.",
        key_statutes=[
            "31 USC 3729(a)(1)(A) (Knowing presentation of false claim)",
            "31 USC 3729(a)(1)(B) (Knowingly making false record or statement)",
            "31 USC 3729(a)(1)(G) (Reverse false claims - concealing overpayment)",
            "31 USC 3730 (Qui tam provisions)",
            "31 USC 3731 (False Claims Procedure)",
            "42 USC 1320a-7k(d) (60-day overpayment refund obligation)",
        ],
        elements=[
            "Submission of a claim for payment to the federal government",
            "The claim was false or fraudulent",
            "Defendant acted knowingly (actual knowledge, deliberate ignorance, or reckless disregard)",
            "Materiality: the falsity was material to the government's payment decision",
            "Causation: defendant caused the false claim to be submitted",
        ],
        defenses=[
            "Lack of knowledge (mere negligence insufficient)",
            "Claim was not false or fraudulent (good faith interpretation of ambiguous regulation)",
            "Falsity was not material to government payment decision (Escobar materiality test)",
            "Government knowledge of the facts (government knowledge defense)",
            "Public disclosure bar (31 USC 3730(e)(4))",
            "First-to-file bar for qui tam actions",
            "Statute of limitations (6 years from violation or 3 years from government knowledge, max 10 years)",
            "Voluntary self-disclosure and timely overpayment return",
        ],
        remedies=[
            "Treble damages (3x amount of false claims)",
            "Per-claim civil penalties (adjusted annually, approximately $13,508-$27,018 per claim as of 2024)",
            "Exclusion from federal healthcare programs",
            "Corporate integrity agreement (CIA) with OIG",
            "Qui tam relator share: 15-25% if DOJ intervenes, 25-30% if DOJ declines",
            "Attorney fees and costs for successful relators",
        ],
        leading_cases=[
            "Universal Health Services v. United States ex rel. Escobar, 579 U.S. 176 (2016) - implied false certification theory and materiality standard",
            "United States ex rel. Schutte v. SuperValu, 598 U.S. 739 (2023) - subjective intent standard for scienter",
            "Azar v. Allina Health Services, 587 U.S. 566 (2019) - notice and comment for Medicare rules",
            "United States v. Kellogg Brown & Root, 525 F.3d 370 (4th Cir. 2008) - government knowledge defense",
            "United States ex rel. Polansky v. Executive Health Resources, 599 U.S. 419 (2023) - DOJ authority to dismiss qui tam actions",
        ],
        category="fraud_abuse",
        subcategory="false_claims_act",
        authority_score=0.92,
        confidence=0.93,
        related_topics=["anti_kickback_statute", "stark_law", "medicare_fraud", "qui_tam", "overpayment_refund"],
        practice_tips=[
            "Implement robust compliance programs with internal reporting mechanisms",
            "Return identified overpayments within the 60-day window (42 USC 1320a-7k(d))",
            "Evaluate voluntary self-disclosure to OIG before qui tam exposure",
            "Apply the Escobar materiality framework when assessing FCA risk",
            "After SuperValu, focus on subjective belief at time of claim submission for scienter analysis",
        ],
        risk_factors=[
            "FCA recoveries exceed $70 billion since 1986; healthcare accounts for 80%+",
            "Qui tam filings average 600+ per year in healthcare",
            "60-day overpayment rule creates ongoing FCA exposure for identified overpayments",
        ],
    ),

    DoctrineCacheBlock(
        topic="anti_kickback_statute",
        summary="The Anti-Kickback Statute (AKS) (42 USC 1320a-7b(b)) is a criminal statute that prohibits knowingly and willfully offering, paying, soliciting, or receiving remuneration to induce or reward referrals of items or services payable by federal healthcare programs. Unlike the Stark Law, the AKS applies to all items and services and requires proof of intent. The OIG has established regulatory safe harbors (42 CFR 1001.952) that provide protection if all elements are met. A violation of the AKS also constitutes a false claim under the FCA per the ACA amendment (42 USC 1320a-7b(g)).",
        key_statutes=[
            "42 USC 1320a-7b(b) (Anti-Kickback Statute)",
            "42 USC 1320a-7b(g) (AKS violation = FCA false claim per ACA)",
            "42 CFR 1001.952 (Safe harbors)",
            "42 USC 1320a-7d(b) (OIG Advisory Opinions)",
            "OIG Special Advisory Bulletins",
        ],
        elements=[
            "Remuneration: anything of value, directly or indirectly, overtly or covertly, in cash or in kind",
            "Knowingly and willfully offered, paid, solicited, or received",
            "Purpose of inducing or rewarding referrals",
            "Items or services payable by a federal healthcare program",
            "One purpose test: only one purpose of the remuneration need be to induce referrals",
        ],
        defenses=[
            "Safe harbor compliance (42 CFR 1001.952) - all elements must be met",
            "Statutory exception for bona fide employment (42 USC 1320a-7b(b)(3)(B))",
            "Statutory exception for discounts properly disclosed (42 USC 1320a-7b(b)(3)(A))",
            "Group purchasing organization exception",
            "Lack of willful intent (mere negligence insufficient)",
            "No federal healthcare program involvement",
            "OIG Advisory Opinion providing favorable guidance",
            "Voluntary self-disclosure to OIG",
        ],
        remedies=[
            "Criminal penalties: felony, up to $100,000 fine and 10 years imprisonment per violation",
            "Civil monetary penalties: up to $100,000 per violation plus 3x damages (42 USC 1320a-7a)",
            "Mandatory exclusion from federal healthcare programs",
            "False Claims Act liability per ACA amendment (treble damages + per-claim penalties)",
            "Corporate integrity agreement with OIG",
            "Loss of professional licensure",
        ],
        leading_cases=[
            "United States v. Greber, 760 F.2d 68 (3d Cir. 1985) - one purpose test",
            "United States v. McClatchey, 217 F.3d 823 (10th Cir. 2000) - on-call payment arrangements",
            "United States v. Borrasi, 639 F.3d 774 (7th Cir. 2011) - remuneration in sale of medical practice",
            "OIG Advisory Opinion 23-04 (2023) - value-based arrangement analysis",
        ],
        category="fraud_abuse",
        subcategory="anti_kickback",
        authority_score=0.92,
        confidence=0.91,
        related_topics=["stark_law", "false_claims_act", "safe_harbors", "physician_compensation", "fair_market_value"],
        practice_tips=[
            "Structure arrangements to meet all elements of applicable safe harbors",
            "Obtain fair market value and commercial reasonableness opinions for compensation arrangements",
            "Consider OIG Advisory Opinions for novel arrangements",
            "Document the legitimate business purposes for each arrangement",
            "Train physicians and staff on AKS requirements and red flags",
        ],
        risk_factors=[
            "ACA amendment means every AKS violation is automatically an FCA false claim",
            "One purpose test sets a very low threshold for intent",
            "OIG has identified physician compensation arrangements as a top enforcement priority",
        ],
        regulatory_notes="The 2020 AKS safe harbor final rule added protections for value-based arrangements, CMS-sponsored model arrangements, patient engagement tools, and cybersecurity technology donations.",
    ),

    DoctrineCacheBlock(
        topic="stark_law",
        summary="The Stark Law (42 USC 1395nn) prohibits physicians from making referrals for designated health services (DHS) payable by Medicare or Medicaid to entities with which the physician (or an immediate family member) has a financial relationship, unless an exception applies. Unlike the AKS, the Stark Law is a strict liability statute - no intent to violate is required. Financial relationships include ownership/investment interests and compensation arrangements. Claims submitted in violation of the Stark Law are false claims, potentially triggering FCA liability. The Stark Law is complex with detailed regulatory exceptions at 42 CFR 411.350-411.389.",
        key_statutes=[
            "42 USC 1395nn (Stark Law)",
            "42 CFR 411.350-411.389 (Stark Law regulations)",
            "42 CFR 411.351 (Definitions - DHS, financial relationship, referral)",
            "42 CFR 411.354 (Financial relationship definitions)",
            "42 CFR 411.355 (In-office ancillary services exception)",
            "42 CFR 411.357 (Compensation arrangement exceptions)",
        ],
        elements=[
            "Physician (or immediate family member) has a financial relationship with the entity",
            "Physician makes a referral for designated health services (DHS)",
            "DHS are payable by Medicare or Medicaid",
            "No applicable exception is satisfied",
            "Designated health services include: clinical lab, physical therapy, occupational therapy, outpatient speech-language, radiology, radiation therapy, DME, parenteral/enteral nutrients, prosthetics, home health, outpatient prescription drugs, inpatient/outpatient hospital services",
        ],
        defenses=[
            "In-office ancillary services exception (42 CFR 411.355(b))",
            "Bona fide employment exception (42 CFR 411.357(c))",
            "Personal services arrangement exception (42 CFR 411.357(d))",
            "Fair market value exception (42 CFR 411.357(l))",
            "Rental of office space exception (42 CFR 411.357(a))",
            "Rental of equipment exception (42 CFR 411.357(b))",
            "Isolated transactions exception (42 CFR 411.357(f))",
            "Academic medical centers exception (42 CFR 411.355(e))",
            "Group practice requirements met (42 CFR 411.352)",
            "Value-based arrangements exception (42 CFR 411.357(aa))",
            "Voluntary self-referral disclosure protocol (CMS SRDP)",
        ],
        remedies=[
            "Denial of payment for DHS claims",
            "Refund of amounts collected for DHS furnished pursuant to prohibited referral",
            "Civil monetary penalties: up to $15,000 per service and up to $100,000 per circumvention scheme",
            "Exclusion from federal healthcare programs",
            "False Claims Act liability for claims submitted in violation",
            "CMS overpayment recovery",
        ],
        leading_cases=[
            "United States ex rel. Drakeford v. Tuomey Healthcare, 792 F.3d 364 (4th Cir. 2015) - $237M FCA verdict for Stark violations",
            "United States v. Halifax Hospital Medical Center, No. 6:09-cv-1002 (M.D. Fla. 2014) - $85M Stark/FCA settlement",
            "Kosenske v. Carlisle HMA, 554 F.3d 88 (3d Cir. 2009) - no implied private right of action under Stark",
            "United States ex rel. Villafane v. Solinger, 543 F. Supp. 2d 678 (W.D. Ky. 2008) - personal services exception analysis",
        ],
        category="fraud_abuse",
        subcategory="stark_law",
        authority_score=0.92,
        confidence=0.91,
        related_topics=["anti_kickback_statute", "false_claims_act", "physician_compensation", "designated_health_services", "fair_market_value"],
        practice_tips=[
            "Document all physician financial relationships and map to applicable exceptions",
            "Ensure compensation is consistent with fair market value and commercially reasonable",
            "Track all Stark exception requirements as ongoing compliance obligations",
            "Monitor the 'stand in the shoes' provisions for indirect compensation",
            "Consider CMS Self-Referral Disclosure Protocol for identified violations",
        ],
        risk_factors=[
            "Strict liability - no intent requirement means technical violations create liability",
            "Tuomey Healthcare verdict demonstrates massive FCA exposure from Stark violations",
            "In-office ancillary services exception is narrow and frequently misapplied",
        ],
        regulatory_notes="The 2020 Stark Law final rule modernized exceptions with value-based arrangements, meaningful downside risk, and full financial risk exceptions. The 2021 rule finalized changes to the group practice definition and special rules for profit shares.",
    ),

    DoctrineCacheBlock(
        topic="medicare_fraud_enforcement",
        summary="Medicare fraud enforcement is a multi-agency effort involving DOJ, HHS-OIG, CMS, FBI, and state Medicaid Fraud Control Units (MFCUs). The primary enforcement tools are the False Claims Act, Anti-Kickback Statute, Stark Law, and the Civil Monetary Penalties Law (42 USC 1320a-7a). The Health Care Fraud Prevention and Enforcement Action Team (HEAT) coordinates federal and state resources. Medicare Strike Force teams operate in high-fraud geographic areas. Common fraud schemes include phantom billing, upcoding, unbundling, medically unnecessary services, and kickback arrangements. The OIG Work Plan identifies annual enforcement priorities.",
        key_statutes=[
            "18 USC 1347 (Healthcare fraud criminal statute)",
            "42 USC 1320a-7a (Civil Monetary Penalties Law)",
            "42 USC 1320a-7 (Exclusion statute)",
            "42 USC 1320a-7k (Additional fraud provisions - ACA)",
            "31 USC 3729 (False Claims Act)",
            "42 USC 1320a-7b (Anti-Kickback Statute)",
        ],
        elements=[
            "Submission of claims to Medicare for items or services not provided as claimed",
            "Knowledge of falsity (for FCA: actual knowledge, deliberate ignorance, or reckless disregard)",
            "Material misrepresentation affecting payment",
            "Pattern of fraudulent conduct (for criminal prosecution)",
            "Items or services not medically necessary",
        ],
        defenses=[
            "Good faith compliance program with effective monitoring",
            "Reasonable interpretation of billing guidelines",
            "Medical necessity supported by clinical documentation",
            "Voluntary self-disclosure to OIG",
            "Cooperation with government investigation",
            "Individual lack of involvement in billing decisions",
            "Statistical sampling methodology challenges",
        ],
        remedies=[
            "Criminal prosecution: up to 10 years imprisonment per count (18 USC 1347)",
            "Civil monetary penalties: $50,000-$100,000 per false claim plus 3x damages",
            "Mandatory exclusion from federal healthcare programs (minimum 5 years)",
            "Permissive exclusion for lesser offenses",
            "Corporate integrity agreements (CIAs) with OIG oversight",
            "Qui tam whistleblower recoveries",
            "Recoupment of overpayments plus interest",
        ],
        leading_cases=[
            "United States v. Patel, 778 F.3d 607 (7th Cir. 2015) - healthcare fraud sentencing",
            "Hays v. Sebelius, 2013 WL 2468714 (W.D. Ky. 2013) - Medicare exclusion due process",
            "Friedman v. Sebelius, 686 F.3d 813 (D.C. Cir. 2012) - exclusion authority scope",
        ],
        category="fraud_abuse",
        subcategory="medicare_fraud",
        authority_score=0.88,
        confidence=0.89,
        related_topics=["false_claims_act", "anti_kickback_statute", "stark_law", "exclusion", "civil_monetary_penalties"],
        practice_tips=[
            "Implement OIG-recommended compliance program elements",
            "Conduct regular audits of coding and billing practices",
            "Monitor OIG Work Plan for current enforcement priorities",
            "Establish internal reporting hotline for compliance concerns",
            "Respond to CMS audit findings within applicable timeframes",
        ],
        risk_factors=[
            "Medicare Strike Force teams operate with data analytics to identify statistical outliers",
            "DOJ recovers $3B+ annually in healthcare fraud settlements and judgments",
            "Exclusion from Medicare effectively ends a healthcare provider career",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - MEDICAL MALPRACTICE
    # ============================================================================

    DoctrineCacheBlock(
        topic="medical_malpractice",
        summary="Medical malpractice is professional negligence by a healthcare provider whose treatment falls below the accepted standard of care in the medical community and causes injury or death to the patient. The four elements of a malpractice claim are duty, breach, causation, and damages. States impose various procedural requirements including certificates of merit, screening panels, statutes of limitations (typically 2-3 years with discovery rule), and damages caps. Expert testimony is generally required to establish the standard of care and breach. Many states have enacted tort reform legislation limiting noneconomic damages, modifying joint and several liability, and requiring alternative dispute resolution.",
        key_statutes=[
            "State medical malpractice statutes (vary by jurisdiction)",
            "Restatement (Third) of Torts: Liability for Physical and Emotional Harm",
            "State tort reform statutes (e.g., MICRA in California, Tex. Civ. Prac. & Rem. Code Ch. 74)",
            "State statutes of limitations (typically 2-3 years from injury or discovery)",
            "State certificate of merit/affidavit of merit requirements",
        ],
        elements=[
            "Duty: physician-patient relationship establishing duty of care",
            "Breach: failure to meet the applicable standard of care",
            "Causation: proximate cause connecting breach to injury (but-for and legal cause)",
            "Damages: actual harm (physical, emotional, economic) suffered by patient",
            "Standard of care: what a reasonably prudent practitioner in the same specialty would do under similar circumstances",
        ],
        defenses=[
            "No deviation from standard of care (expert testimony)",
            "No proximate causation (injury would have occurred regardless)",
            "Contributory or comparative negligence of the patient",
            "Assumption of risk / informed consent defense",
            "Statute of limitations expired",
            "Respectable minority doctrine (alternative acceptable treatment)",
            "Good Samaritan statute protection (emergency situations)",
            "Error in judgment defense (if based on reasonable assessment)",
            "Compliance with clinical guidelines or protocols",
        ],
        remedies=[
            "Compensatory damages: economic (medical bills, lost wages) and noneconomic (pain and suffering)",
            "Punitive damages (available in some states for gross negligence or reckless conduct)",
            "Medical board disciplinary action",
            "Loss of hospital privileges",
            "Mandatory reporting to NPDB",
            "Settlement with confidentiality provisions",
        ],
        leading_cases=[
            "Helling v. Carey, 83 Wash.2d 514 (1974) - standard of care may exceed customary practice",
            "Canterbury v. Spence, 464 F.2d 772 (D.C. Cir. 1972) - patient-centered informed consent standard",
            "Daubert v. Merrell Dow Pharmaceuticals, 509 U.S. 579 (1993) - expert testimony admissibility",
            "T.J. Hooper v. Northern Barge Corp., 60 F.2d 737 (2d Cir. 1932) - custom may not define standard of care",
        ],
        category="malpractice",
        subcategory="medical_negligence",
        authority_score=0.85,
        confidence=0.88,
        related_topics=["informed_consent", "vicarious_liability", "hospital_liability", "telemedicine_liability", "damages_caps"],
        practice_tips=[
            "Verify applicable statute of limitations including discovery rule and minor tolling provisions",
            "Identify certificate of merit or screening panel requirements early",
            "Determine whether damages caps apply and their constitutional status in the jurisdiction",
            "Evaluate whether national or locality-based standard of care applies",
            "Assess vicarious liability theories (respondeat superior, ostensible agency, nondelegable duty)",
        ],
        risk_factors=[
            "Expert witness qualifications vary significantly by state",
            "Tort reform constitutionality challenges can change the landscape mid-litigation",
            "NPDB reporting creates long-term career consequences for practitioners",
        ],
    ),

    DoctrineCacheBlock(
        topic="informed_consent",
        summary="Informed consent is a legal and ethical doctrine requiring healthcare providers to disclose material information about proposed treatment, including risks, benefits, alternatives, and the consequences of declining treatment, to enable the patient to make an informed decision. Two standards exist: the physician-based standard (what a reasonable physician would disclose) and the patient-based standard (what a reasonable patient would want to know). Failure to obtain informed consent may give rise to a battery claim (no consent at all) or a negligence claim (inadequate disclosure). Exceptions include emergencies, therapeutic privilege, patient waiver, and incompetent patients where surrogate consent is obtained.",
        key_statutes=[
            "State informed consent statutes",
            "Canterbury v. Spence, 464 F.2d 772 (D.C. Cir. 1972) (patient-centered standard)",
            "Restatement (Third) of Torts: Liability for Physical and Emotional Harm SS 18-19",
            "45 CFR 46.116 (Informed consent for research - Common Rule)",
            "21 CFR 50.20-50.27 (FDA informed consent for clinical trials)",
        ],
        elements=[
            "Provider proposed a treatment, procedure, or intervention",
            "Provider failed to disclose material risks and alternatives",
            "A reasonable patient would have declined treatment if properly informed",
            "Patient suffered injury from the undisclosed risk",
            "Patient did not provide valid consent (voluntary, informed, competent)",
        ],
        defenses=[
            "Full and adequate disclosure was made and documented",
            "Emergency exception (patient unconscious, no surrogate available, delay endangers life)",
            "Therapeutic privilege (disclosure would harm patient's well-being)",
            "Patient waiver (patient explicitly declined information)",
            "Risk was commonly known and need not be disclosed",
            "Patient would have consented even with full disclosure (causation defense)",
            "Written consent form signed and witnessed",
        ],
        remedies=[
            "Damages for battery (if no consent at all)",
            "Negligence damages for inadequate disclosure",
            "Compensatory damages including additional medical costs",
            "Emotional distress damages",
            "Loss of bodily autonomy / dignitary harm",
        ],
        leading_cases=[
            "Canterbury v. Spence, 464 F.2d 772 (D.C. Cir. 1972) - patient-centered disclosure standard",
            "Cobbs v. Grant, 8 Cal.3d 229 (1972) - material risk disclosure requirement",
            "Truman v. Thomas, 27 Cal.3d 285 (1980) - duty to disclose risks of refusing treatment",
            "Schloendorff v. Society of New York Hospital, 211 N.Y. 125 (1914) - right to bodily self-determination",
        ],
        category="malpractice",
        subcategory="informed_consent",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["medical_malpractice", "patient_rights", "clinical_trials", "telemedicine"],
        practice_tips=[
            "Use a structured informed consent process with both written and verbal communication",
            "Document the specific risks, benefits, and alternatives discussed",
            "Allow adequate time for patient questions and deliberation",
            "Use interpreters for patients with limited English proficiency",
            "Obtain separate consent for each distinct procedure or treatment change",
        ],
        risk_factors=[
            "Consent forms alone may not demonstrate adequate informed consent process",
            "Telemedicine creates additional informed consent challenges regarding technology limitations",
            "Research consent requires additional regulatory elements under 45 CFR 46",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - EMTALA
    # ============================================================================

    DoctrineCacheBlock(
        topic="emtala",
        summary="The Emergency Medical Treatment and Active Labor Act (EMTALA) (42 USC 1395dd) requires Medicare-participating hospitals with dedicated emergency departments (DEDs) to provide a medical screening examination (MSE) to any individual who comes to the ED seeking treatment, regardless of insurance status or ability to pay. If an emergency medical condition (EMC) is identified, the hospital must stabilize the patient before discharge or transfer. Transfers are permitted only if the patient requests transfer, a physician certifies the medical benefits of transfer outweigh risks, and the receiving facility accepts the transfer with appropriate capabilities. EMTALA violations can result in CMS termination from Medicare, civil monetary penalties, and private lawsuits.",
        key_statutes=[
            "42 USC 1395dd (EMTALA)",
            "42 USC 1395dd(a) (Medical screening examination requirement)",
            "42 USC 1395dd(b) (Stabilization requirement)",
            "42 USC 1395dd(c) (Appropriate transfer requirements)",
            "42 USC 1395dd(d) (Enforcement - CMP, private right of action)",
            "42 CFR 489.24 (EMTALA regulations)",
        ],
        elements=[
            "Hospital participates in Medicare and has a dedicated emergency department",
            "Individual came to the emergency department requesting examination or treatment",
            "Hospital failed to provide appropriate medical screening examination",
            "Emergency medical condition existed and hospital failed to stabilize",
            "Inappropriate transfer without physician certification and receiving facility acceptance",
            "On-call physician failed to respond within reasonable time",
        ],
        defenses=[
            "Hospital is not a Medicare participant or does not have a DED",
            "Individual did not present to the DED (e.g., scheduled outpatient, inpatient)",
            "Appropriate MSE was provided and no EMC identified",
            "EMC was stabilized before discharge or transfer",
            "Transfer met all regulatory requirements (certification, acceptance, records)",
            "Patient left against medical advice (LWBS/AMA) with documented refusal",
            "Patient was appropriately transferred to higher level of care",
        ],
        remedies=[
            "CMS termination from Medicare program",
            "Civil monetary penalties: up to $50,000 per violation (up to $103,139 per violation for hospitals with 100+ beds, adjusted for inflation)",
            "Private right of action for individuals who suffer personal harm (42 USC 1395dd(d)(2))",
            "Physician civil monetary penalties and exclusion from Medicare",
            "Receiving hospital liability for failure to accept appropriate transfer (reverse dumping)",
        ],
        leading_cases=[
            "Roberts v. Galen of Virginia, 525 U.S. 249 (1999) - no improper motive required for EMTALA claim",
            "Cleland v. Bronson Health Care Group, 917 F.2d 266 (6th Cir. 1990) - MSE compared to hospital's standard screening",
            "Baber v. Hospital Corp. of America, 977 F.2d 872 (4th Cir. 1992) - scope of stabilization obligation",
            "Bryant v. Adventist Health System, 289 F.3d 1162 (9th Cir. 2002) - on-call physician liability",
        ],
        category="emtala",
        subcategory="emergency_treatment",
        authority_score=0.88,
        confidence=0.90,
        related_topics=["medical_malpractice", "patient_rights", "hospital_liability", "medical_screening"],
        practice_tips=[
            "Ensure MSE protocols are applied uniformly regardless of insurance status",
            "Document on-call physician response times and communications",
            "Maintain transfer agreements with specialty and higher-level facilities",
            "Train all ED staff on EMTALA obligations including triage nurses",
            "Document patient refusals of treatment with informed refusal language",
        ],
        risk_factors=[
            "EMTALA applies 250 yards from the main hospital building",
            "Hospital-owned urgent care centers may qualify as DEDs",
            "Psychiatric emergencies create stabilization challenges",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - FDA REGULATION
    # ============================================================================

    DoctrineCacheBlock(
        topic="fda_drug_regulation",
        summary="The Federal Food, Drug, and Cosmetic Act (FD&C Act, 21 USC 301 et seq.) grants the FDA authority to regulate drugs, biologics, and medical devices. New drugs require premarket approval through the New Drug Application (NDA) process, demonstrating safety and efficacy through clinical trials (Phase I-III). Generic drugs follow the Abbreviated New Drug Application (ANDA) pathway demonstrating bioequivalence. Biologics are regulated under the Public Health Service Act (42 USC 262) with Biologics License Applications (BLAs). The 2010 BPCIA created a biosimilar approval pathway. The Hatch-Waxman Act (Drug Price Competition and Patent Term Restoration Act of 1984) balances innovation incentives with generic competition through patent term extensions and Paragraph IV certifications.",
        key_statutes=[
            "21 USC 301 et seq. (Federal Food, Drug, and Cosmetic Act)",
            "21 USC 355 (New drug applications)",
            "21 USC 355(j) (Abbreviated new drug applications - generics)",
            "42 USC 262 (Biologics License Applications)",
            "42 USC 262(k) (Biosimilar applications - BPCIA)",
            "21 CFR Parts 312, 314 (IND and NDA regulations)",
            "Drug Price Competition and Patent Term Restoration Act of 1984 (Hatch-Waxman)",
        ],
        elements=[
            "Substance is a drug, biologic, or combination product under FDA jurisdiction",
            "Drug is new and has not received FDA approval (misbranding/adulteration)",
            "Clinical trial requirements: IND application, Phase I-III trials, NDA submission",
            "Post-market requirements: adverse event reporting, REMS, labeling updates",
            "Manufacturing compliance with current Good Manufacturing Practices (cGMP)",
        ],
        defenses=[
            "FDA-approved labeling and marketing (preemption in some circuits)",
            "Compliance with IND/NDA requirements throughout development",
            "Practice of medicine exception (physician off-label prescribing)",
            "Orphan Drug Act exclusivity protection",
            "Patent term extension under Hatch-Waxman",
            "Emergency Use Authorization (EUA) under 21 USC 360bbb-3",
        ],
        remedies=[
            "FDA Warning Letters and untitled letters",
            "Consent decrees and injunctions",
            "Product seizure (21 USC 334)",
            "Criminal prosecution for misbranding or adulteration",
            "Debarment from drug development activities",
            "Withdrawal of drug approval",
            "Mandatory recalls",
            "Civil monetary penalties for REMS violations",
        ],
        leading_cases=[
            "Wyeth v. Levine, 555 U.S. 555 (2009) - FDA labeling does not preempt state failure-to-warn claims",
            "PLIVA Inc. v. Mensing, 564 U.S. 604 (2011) - federal law preempts state failure-to-warn for generics",
            "Mutual Pharmaceutical Co. v. Bartlett, 570 U.S. 472 (2013) - design defect preemption for generics",
            "Buckman Co. v. Plaintiffs' Legal Committee, 531 U.S. 341 (2001) - fraud-on-the-FDA claims preempted",
        ],
        category="fda",
        subcategory="drug_regulation",
        authority_score=0.88,
        confidence=0.89,
        related_topics=["fda_device_regulation", "clinical_trials", "off_label_promotion", "drug_pricing", "pharmacy_law"],
        practice_tips=[
            "Engage FDA early through pre-IND meetings for novel drug products",
            "Monitor FDA guidance documents for evolving review standards",
            "Maintain pharmacovigilance systems for post-market adverse event reporting",
            "Evaluate preemption defense availability based on product type (branded vs. generic)",
            "Structure promotional activities to avoid off-label promotion enforcement",
        ],
        risk_factors=[
            "Accelerated approval products face post-market study withdrawal risk",
            "REMS non-compliance can trigger significant CMPs",
            "Off-label promotion remains a top DOJ enforcement priority",
        ],
    ),

    DoctrineCacheBlock(
        topic="fda_device_regulation",
        summary="Medical devices are regulated under the FD&C Act based on a risk classification system (Class I, II, III). Class I devices are subject to general controls. Class II devices require 510(k) premarket notification demonstrating substantial equivalence to a predicate device. Class III devices require premarket approval (PMA) with clinical data demonstrating safety and efficacy. The De Novo pathway provides an alternative for novel low-to-moderate risk devices without a predicate. Post-market requirements include Medical Device Reporting (MDR), Unique Device Identification (UDI), and Quality System Regulation (QSR/21 CFR 820) compliance. The 2023 MDUFA V reauthorization updated review timelines and user fee structures.",
        key_statutes=[
            "21 USC 360c (Device classification)",
            "21 USC 360(k) (510(k) premarket notification)",
            "21 USC 360e (Premarket approval - PMA)",
            "21 USC 360e-1 (De Novo classification)",
            "21 CFR 820 (Quality System Regulation)",
            "21 CFR 803 (Medical Device Reporting)",
            "21 USC 360j(f) (Custom device exemption)",
        ],
        elements=[
            "Product meets statutory definition of a medical device (21 USC 321(h))",
            "Device is classified as Class I, II, or III based on risk",
            "Premarket clearance or approval obtained (510(k), PMA, or De Novo)",
            "Compliance with Quality System Regulation (QSR)",
            "Adverse event and malfunction reporting under MDR",
            "Unique Device Identification (UDI) labeling requirements",
        ],
        defenses=[
            "Express preemption for PMA-approved devices (Riegel v. Medtronic)",
            "510(k) clearance does not trigger express preemption (Medtronic v. Lohr)",
            "Custom device exemption (21 USC 360j(f))",
            "Humanitarian Device Exemption (HDE)",
            "Investigational Device Exemption (IDE) for clinical trials",
            "Emergency use provisions",
        ],
        remedies=[
            "FDA Warning Letters and Form 483 observations",
            "Mandatory and voluntary recalls (Class I, II, III)",
            "Consent decrees with production shutdowns",
            "Import detention and refusal",
            "Criminal prosecution for knowing violations",
            "Debarment of individuals",
            "Product liability litigation (where not preempted)",
        ],
        leading_cases=[
            "Riegel v. Medtronic, 552 U.S. 312 (2008) - PMA devices expressly preempt state tort claims",
            "Medtronic v. Lohr, 518 U.S. 470 (1996) - 510(k) clearance does not preempt state claims",
            "Buckman Co. v. Plaintiffs' Legal Committee, 531 U.S. 341 (2001) - fraud-on-FDA preempted",
        ],
        category="fda",
        subcategory="device_regulation",
        authority_score=0.88,
        confidence=0.88,
        related_topics=["fda_drug_regulation", "clinical_trials", "product_liability", "quality_system"],
        practice_tips=[
            "Evaluate the predicate device strategy early in 510(k) development",
            "Consider De Novo pathway for novel devices without clear predicates",
            "Implement robust complaint handling and MDR systems",
            "Prepare for QSR inspections with regular internal audits",
            "Assess preemption defense availability based on clearance/approval pathway",
        ],
        risk_factors=[
            "Form 483 observations can escalate to Warning Letters and consent decrees",
            "Software as a Medical Device (SaMD) classification is evolving rapidly",
            "Cybersecurity requirements for connected devices are increasing",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - ACA / INSURANCE / PARITY
    # ============================================================================

    DoctrineCacheBlock(
        topic="aca_compliance",
        summary="The Affordable Care Act (ACA, 42 USC 18001 et seq.) enacted comprehensive health insurance reforms including the individual mandate (effectively zeroed by TCJA but structurally intact in some states), employer shared responsibility provisions (26 USC 4980H), Health Insurance Exchanges/Marketplaces, essential health benefits requirements, prohibition of pre-existing condition exclusions, dependent coverage to age 26, Medicaid expansion, premium tax credits (26 USC 36B), and cost-sharing reductions. Applicable large employers (ALEs, 50+ full-time equivalent employees) face penalties for failing to offer affordable minimum essential coverage. The ACA also included significant fraud and abuse, quality, and transparency provisions.",
        key_statutes=[
            "42 USC 18001 et seq. (Patient Protection and Affordable Care Act)",
            "26 USC 4980H (Employer shared responsibility)",
            "26 USC 36B (Premium tax credit)",
            "42 USC 18022 (Essential health benefits)",
            "42 USC 300gg (Insurance market reforms)",
            "42 USC 300gg-11 to 300gg-19a (Individual and group market reforms)",
            "42 USC 1396a(a)(10)(A)(i)(VIII) (Medicaid expansion)",
        ],
        elements=[
            "Employer is an applicable large employer (50+ FTE employees)",
            "Failure to offer minimum essential coverage to substantially all full-time employees",
            "Coverage offered is not affordable (employee premium exceeds affordability threshold of W-2 wages)",
            "Coverage offered does not provide minimum value (pays less than 60% of total allowed costs)",
            "At least one full-time employee enrolls in Exchange coverage and receives premium tax credit",
        ],
        defenses=[
            "Employer is not an ALE (fewer than 50 FTEs)",
            "Minimum essential coverage offered to substantially all (95%+) full-time employees",
            "Coverage meets affordability safe harbors (W-2, rate of pay, or federal poverty level)",
            "Coverage provides minimum value (60% actuarial value)",
            "Transition relief provisions for certain employer categories",
            "Multiemployer plan interim relief",
        ],
        remedies=[
            "Section 4980H(a) penalty: ~$2,970 per full-time employee minus 30 (2024, indexed annually)",
            "Section 4980H(b) penalty: ~$4,460 per employee receiving premium tax credit (2024, indexed)",
            "IRS Letter 226-J assessment process",
            "Employer reporting penalties for Forms 1094-C/1095-C failures",
            "Individual market special enrollment violations",
        ],
        leading_cases=[
            "King v. Burwell, 576 U.S. 473 (2015) - premium tax credits available on federal Exchange",
            "NFIB v. Sebelius, 567 U.S. 519 (2012) - individual mandate upheld as tax; Medicaid expansion cannot be coerced",
            "California v. Texas, 593 U.S. 378 (2021) - plaintiffs lack standing to challenge individual mandate",
            "Little Sisters of the Poor v. Pennsylvania, 591 U.S. 171 (2020) - religious and moral exemptions to contraceptive mandate",
        ],
        category="aca",
        subcategory="employer_compliance",
        authority_score=0.88,
        confidence=0.89,
        related_topics=["employer_mandate", "essential_health_benefits", "medicaid_expansion", "premium_tax_credits"],
        practice_tips=[
            "Conduct annual ALE determination using look-back measurement method",
            "Track full-time employee status monthly using permissible measurement methods",
            "Apply affordability safe harbors to demonstrate compliance",
            "File Forms 1094-C and 1095-C accurately and timely (March deadline)",
            "Monitor IRS Letter 226-J and respond within 30-day window",
        ],
        risk_factors=[
            "ALE determination for variable-hour employees is complex and litigation-prone",
            "Controlled group and affiliated service group rules aggregate related employers",
            "State individual mandates (CA, DC, MA, NJ, RI, VT) create parallel compliance obligations",
        ],
    ),

    DoctrineCacheBlock(
        topic="mental_health_parity",
        summary="The Mental Health Parity and Addiction Equity Act (MHPAEA) (29 USC 1185a) requires group health plans and health insurance issuers offering mental health/substance use disorder (MH/SUD) benefits to ensure parity with medical/surgical benefits. Parity must be maintained for financial requirements (copays, deductibles, coinsurance), quantitative treatment limitations (visit limits, day limits), and nonquantitative treatment limitations (NQTLs) such as prior authorization, step therapy, and network adequacy. The Consolidated Appropriations Act of 2021 (CAA 2021) requires plans to conduct and document comparative analyses of NQTLs. The Departments of Labor, HHS, and Treasury jointly enforce MHPAEA.",
        key_statutes=[
            "29 USC 1185a (MHPAEA - ERISA plans)",
            "42 USC 300gg-26 (MHPAEA - individual and group market)",
            "26 USC 9812 (MHPAEA - Internal Revenue Code)",
            "45 CFR 146.136 (MHPAEA regulations)",
            "29 CFR 2590.712 (DOL MHPAEA regulations)",
            "CAA 2021 SS 203 (NQTL comparative analysis requirements)",
        ],
        elements=[
            "Group health plan or issuer provides MH/SUD benefits",
            "Financial requirements or treatment limitations applied to MH/SUD benefits",
            "Limitations are more restrictive than the predominant limitation applied to substantially all medical/surgical benefits in the same classification",
            "NQTL applied to MH/SUD benefits that is not comparable to and applied no more stringently than for medical/surgical benefits",
            "Failure to perform or document NQTL comparative analysis",
        ],
        defenses=[
            "Plan does not offer MH/SUD benefits (MHPAEA applies only if benefits are offered)",
            "Financial requirements and QTLs pass the substantially all / predominant test",
            "NQTLs are comparable and applied no more stringently in writing and in operation",
            "Small employer exemption (fewer than 50 employees)",
            "Increased cost exemption (2% cost increase threshold)",
            "Comparative analysis documented and provided upon request",
        ],
        remedies=[
            "DOL investigation and enforcement action",
            "State insurance department enforcement",
            "ERISA civil enforcement by plan participants (29 USC 1132)",
            "CMS enforcement for non-federal governmental plans",
            "Corrective action requiring retroactive coverage and reprocessing of denied claims",
            "Participant class actions for systematic NQTL violations",
        ],
        leading_cases=[
            "Wit v. United Behavioral Health, 58 F.4th 1080 (9th Cir. 2023) - level of care guidelines must comply with MHPAEA",
            "New York State Psychiatric Association v. UnitedHealth Group, 798 F.3d 125 (2d Cir. 2015) - MHPAEA NQTL analysis",
            "David P. v. United Healthcare Insurance Co., 2021 WL 1169579 (D. Utah 2021) - step therapy parity violation",
        ],
        category="parity",
        subcategory="mental_health_parity",
        authority_score=0.85,
        confidence=0.87,
        related_topics=["aca_compliance", "substance_abuse_confidentiality", "insurance_regulation", "prior_authorization"],
        practice_tips=[
            "Perform the substantially all / predominant test for each benefit classification",
            "Document NQTL comparative analysis with factors, data, and evidentiary standards used",
            "Compare network adequacy, reimbursement rates, and prior authorization requirements between MH/SUD and medical/surgical",
            "Prepare for DOL NQTL comparative analysis requests with supporting data",
            "Monitor the 2024 MHPAEA proposed rule for expanded NQTL requirements",
        ],
        risk_factors=[
            "DOL enforcement of NQTL comparative analysis requirements is increasing",
            "State parity laws may impose additional requirements beyond federal MHPAEA",
            "Failure to produce comparative analysis upon request triggers enforcement action",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - TELEMEDICINE
    # ============================================================================

    DoctrineCacheBlock(
        topic="telemedicine_regulation",
        summary="Telemedicine regulation involves a complex intersection of state medical practice acts, federal prescribing laws, reimbursement rules, and technology standards. Physicians must generally be licensed in the state where the patient is located at the time of the encounter. The Interstate Medical Licensure Compact facilitates multi-state licensure. The Ryan Haight Act (21 USC 829(e)) restricts online prescribing of controlled substances, requiring at least one in-person evaluation (temporarily waived during COVID-19 PHE with DEA extending flexibilities). Medicare telehealth coverage was significantly expanded during the PHE and partially made permanent by legislation. State telehealth parity laws require insurers to cover telehealth services comparably to in-person services.",
        key_statutes=[
            "21 USC 829(e) (Ryan Haight Online Pharmacy Consumer Protection Act)",
            "State medical practice acts (physician licensing requirements)",
            "Interstate Medical Licensure Compact (IMLC)",
            "42 USC 1395m(m) (Medicare telehealth coverage)",
            "42 CFR 410.78 (Medicare telehealth services)",
            "State telehealth parity laws",
            "DEA telemedicine prescribing regulations (21 CFR 1300 et seq.)",
        ],
        elements=[
            "Physician-patient relationship established via telemedicine technology",
            "Physician licensed in the state where the patient is located",
            "Appropriate standard of care maintained via telemedicine modality",
            "Informed consent for telemedicine encounter obtained",
            "Technology meets applicable privacy and security requirements",
            "Prescribing complies with Ryan Haight Act and state prescribing rules",
            "Documentation meets medical record requirements",
        ],
        defenses=[
            "Physician properly licensed in patient's state",
            "Interstate Medical Licensure Compact participation",
            "Standard of care met via telemedicine modality",
            "COVID-19 PHE waivers and flexibilities applied",
            "DEA telemedicine registration exception",
            "Consultation exception (specialist consulted by treating physician)",
            "State border exception in some jurisdictions",
        ],
        remedies=[
            "State medical board disciplinary action for unlicensed practice",
            "DEA enforcement for Ryan Haight Act violations",
            "Malpractice liability for telemedicine-related injuries",
            "Medicare/Medicaid fraud liability for improper telehealth billing",
            "State insurance department enforcement for parity violations",
            "HIPAA enforcement for inadequate technology safeguards",
        ],
        leading_cases=[
            "Hageseth v. Superior Court, 150 Cal. App. 4th 1399 (2007) - out-of-state physician subject to California jurisdiction for telemedicine",
            "Teladoc Inc. v. Texas Medical Board, 112 F. Supp. 3d 529 (W.D. Tex. 2015) - antitrust challenge to telemedicine restrictions",
        ],
        category="telemedicine",
        subcategory="telehealth_regulation",
        authority_score=0.82,
        confidence=0.84,
        related_topics=["informed_consent", "medical_malpractice", "prescribing", "medicare_coverage", "state_licensing"],
        practice_tips=[
            "Verify licensure requirements in every state where patients are located",
            "Implement telemedicine-specific informed consent protocols",
            "Monitor DEA rulemaking on post-PHE controlled substance prescribing via telemedicine",
            "Maintain robust authentication and identity verification for patients",
            "Document clinical rationale for treatment modality selection (telemedicine vs. in-person)",
        ],
        risk_factors=[
            "Post-PHE rollback of telehealth flexibilities creates compliance uncertainty",
            "Ryan Haight Act in-person requirement for controlled substances remains subject to DEA rulemaking",
            "State-by-state licensure requirements create significant compliance burden for multi-state programs",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - CLINICAL TRIALS
    # ============================================================================

    DoctrineCacheBlock(
        topic="clinical_trials_irb",
        summary="Clinical research involving human subjects is governed by the Common Rule (45 CFR Part 46), FDA regulations (21 CFR Parts 50, 56, 312, 812), and institutional policies. Institutional Review Boards (IRBs) must review and approve research protocols before enrollment begins. IRBs evaluate risks to subjects, adequacy of informed consent, subject selection equity, data monitoring, privacy protections, and additional protections for vulnerable populations (children, prisoners, pregnant women). The 2018 Revised Common Rule introduced single IRB review requirements for multi-site studies, broadened continuing review exemptions, and revised consent requirements. FDA regulations apply to research involving drugs (IND) or devices (IDE) regardless of federal funding.",
        key_statutes=[
            "45 CFR Part 46 (Common Rule - Protection of Human Subjects)",
            "21 CFR Part 50 (FDA - Protection of Human Subjects, Informed Consent)",
            "21 CFR Part 56 (FDA - Institutional Review Boards)",
            "21 CFR Part 312 (Investigational New Drug Application)",
            "21 CFR Part 812 (Investigational Device Exemptions)",
            "42 USC 289 (Research subject protections)",
        ],
        elements=[
            "Research involves human subjects (living individuals, identifiable data/specimens)",
            "IRB review and approval obtained before enrollment",
            "Informed consent obtained per 45 CFR 46.116 requirements",
            "Risks minimized and reasonable in relation to anticipated benefits",
            "Equitable subject selection",
            "Data monitoring adequate to ensure subject safety",
            "Privacy and confidentiality of subjects protected",
            "Continuing review conducted at least annually (unless exempt under 2018 revisions)",
        ],
        defenses=[
            "Activity does not meet definition of research or human subjects",
            "Exempt research category applies (45 CFR 46.104)",
            "Expedited review properly utilized (45 CFR 46.110)",
            "Waiver of informed consent or documentation (45 CFR 46.116(f), 46.117(c))",
            "Emergency use exception (21 CFR 50.23)",
            "IRB approval obtained and protocol followed",
        ],
        remedies=[
            "FDA Form 483 observations and Warning Letters",
            "Clinical hold on IND/IDE (21 CFR 312.42)",
            "Disqualification of clinical investigator (21 CFR 312.70)",
            "Debarment from conducting research",
            "OHRP compliance determination letters and corrective action",
            "Institutional suspension or termination of research",
            "Civil litigation for research-related injuries",
            "Loss of federal funding eligibility",
        ],
        leading_cases=[
            "Grimes v. Kennedy Krieger Institute, 782 A.2d 807 (Md. 2001) - duty to children in research",
            "Moore v. Regents of the University of California, 51 Cal.3d 120 (1990) - informed consent for tissue use in research",
            "Wright v. Fred Hutchinson Cancer Research Center, 269 F. Supp. 2d 1286 (W.D. Wash. 2002) - research participant informed consent",
        ],
        category="clinical_trials",
        subcategory="irb_oversight",
        authority_score=0.86,
        confidence=0.88,
        related_topics=["informed_consent", "fda_drug_regulation", "fda_device_regulation", "research_ethics"],
        practice_tips=[
            "Use single IRB for multi-site studies per 2018 Revised Common Rule",
            "Apply the new consent form requirements (concise summary at beginning)",
            "Distinguish FDA-regulated from non-FDA-regulated research for applicable requirements",
            "Implement data safety monitoring boards for higher-risk studies",
            "Ensure ClinicalTrials.gov registration and results posting compliance",
        ],
        risk_factors=[
            "Failure to register on ClinicalTrials.gov can result in civil penalties",
            "Vulnerable population protections require additional scrutiny",
            "International research adds ICH-GCP and local regulatory requirements",
        ],
    ),

    # ============================================================================
    # DOCTRINE BLOCKS - ADDITIONAL HEALTHCARE LAW TOPICS
    # ============================================================================

    DoctrineCacheBlock(
        topic="tax_exempt_hospitals_501r",
        summary="IRC Section 501(r), added by the ACA, imposes additional requirements on tax-exempt hospitals (Section 501(c)(3) hospital organizations). These requirements include: (1) conducting a community health needs assessment (CHNA) at least every three years and adopting an implementation strategy; (2) establishing a written financial assistance policy (FAP) widely publicized in the community; (3) limiting charges to financially assisted patients to amounts generally billed (AGB) to insured patients; and (4) refraining from extraordinary collection actions (ECAs) before making reasonable efforts to determine financial assistance eligibility. Failure to comply can result in excise taxes under IRC 4959 and potential loss of tax-exempt status.",
        key_statutes=[
            "IRC 501(r) (Additional requirements for charitable hospitals)",
            "IRC 501(r)(3) (Community health needs assessment)",
            "IRC 501(r)(4) (Financial assistance policy)",
            "IRC 501(r)(5) (Limitation on charges)",
            "IRC 501(r)(6) (Billing and collection requirements)",
            "26 CFR 1.501(r)-1 through 1.501(r)-7 (Treasury regulations)",
            "IRC 4959 (Excise tax for CHNA failures)",
        ],
        elements=[
            "Organization is a 501(c)(3) hospital organization",
            "Each hospital facility must separately comply with 501(r)",
            "CHNA conducted and adopted every three years",
            "FAP established with eligibility criteria, basis for assistance, and application process",
            "Charges to FAP-eligible patients limited to AGB",
            "No ECAs taken before reasonable efforts to determine FAP eligibility (240-day notification period)",
        ],
        defenses=[
            "Organization is not a hospital organization under IRC 501(r)(2)",
            "CHNA conducted with community input and adopted by authorized body",
            "FAP widely publicized including on website and in billing communications",
            "AGB calculated using look-back or prospective Medicare method",
            "Reasonable efforts made before any ECA (written notice, 240-day period, individual determination)",
            "Minor and inadvertent omission corrected and disclosed (reasonable cause exception)",
        ],
        remedies=[
            "Excise tax of $50,000 per hospital facility per taxable year for CHNA failure (IRC 4959)",
            "Potential revocation of 501(c)(3) tax-exempt status",
            "IRS Form 990 Schedule H disclosure of noncompliance",
            "Private litigation by patients for ECA violations",
            "State attorney general enforcement",
            "Media and reputational harm from aggressive billing practices",
        ],
        leading_cases=[
            "Rideout Health v. IRS (administrative proceedings) - CHNA compliance requirements",
            "Various state AG investigations of nonprofit hospital billing practices",
        ],
        category="tax_exempt",
        subcategory="501r_compliance",
        authority_score=0.83,
        confidence=0.85,
        related_topics=["aca_compliance", "hospital_billing", "charitable_care", "community_benefit"],
        practice_tips=[
            "Calendar CHNA cycle to ensure compliance every three years",
            "Calculate AGB using both look-back and prospective methods to determine favorable approach",
            "Implement ECA hold procedures until 240-day notification period expires",
            "Translate FAP materials into languages spoken by significant community populations",
            "Document reasonable efforts to determine FAP eligibility before each ECA",
        ],
        risk_factors=[
            "Each hospital facility must independently comply - system-wide approach insufficient",
            "ECA definition includes lawsuits, wage garnishment, liens, credit reporting, and sale of debt",
            "IRS has increased scrutiny of 501(r) compliance on Form 990 Schedule H",
        ],
    ),

    DoctrineCacheBlock(
        topic="substance_abuse_confidentiality",
        summary="42 CFR Part 2 provides heightened confidentiality protections for patient records created by federally assisted substance use disorder (SUD) treatment programs. Part 2 is more restrictive than HIPAA and generally prohibits redisclosure of SUD treatment records without patient consent. The 2024 final rule aligned Part 2 with HIPAA in several respects, permitting disclosures for treatment, payment, and healthcare operations with a single prior consent, and permitting use of Part 2 records in civil, criminal, administrative, and legislative proceedings against the patient only with a court order. Part 2 applies to any program that is federally assisted (including Medicare/Medicaid participation) and holds itself out as providing SUD diagnosis, treatment, or referral.",
        key_statutes=[
            "42 USC 290dd-2 (Confidentiality of substance use disorder records)",
            "42 CFR Part 2 (Confidentiality of SUD Patient Records)",
            "42 CFR 2.11 (Definitions - program, patient, records)",
            "42 CFR 2.12 (Applicability)",
            "42 CFR 2.31-2.35 (Consent requirements)",
            "42 CFR 2.63-2.67 (Court orders for disclosure)",
        ],
        elements=[
            "Program is federally assisted (receives any form of federal funding/participation)",
            "Program holds itself out as providing SUD diagnosis, treatment, or referral for treatment",
            "Records identify a patient as having or having had a substance use disorder",
            "Disclosure made without valid patient consent or other regulatory authorization",
            "Recipient of information redisclosed in violation of Part 2 notice requirements",
        ],
        defenses=[
            "Valid patient consent obtained with all required elements (42 CFR 2.31)",
            "Single prior consent for TPO purposes under 2024 final rule",
            "Medical emergency exception (42 CFR 2.51)",
            "Audit or evaluation exception (42 CFR 2.53)",
            "Qualified service organization agreement (QSOA) in place",
            "Court order obtained per 42 CFR 2.63-2.67",
            "Research exception with IRB/Privacy Board approval",
            "Records are not from a Part 2 program",
        ],
        remedies=[
            "Criminal penalties: first offense up to $500 fine; subsequent offenses up to $5,000",
            "Civil litigation for unauthorized disclosure",
            "SAMHSA enforcement",
            "State law penalties (many states have parallel SUD confidentiality laws)",
            "HIPAA enforcement where applicable",
            "Professional disciplinary action",
        ],
        leading_cases=[
            "Doe v. SEPTA, No. 2:17-cv-04975 (E.D. Pa. 2018) - Part 2 violation in employment context",
            "United States v. Eide, 875 F.2d 1429 (9th Cir. 1989) - scope of Part 2 protections",
        ],
        category="substance_abuse",
        subcategory="42_cfr_part_2",
        authority_score=0.83,
        confidence=0.85,
        related_topics=["hipaa_privacy_rule", "patient_rights", "substance_use_treatment", "mental_health_parity"],
        practice_tips=[
            "Determine whether the program meets the Part 2 definition before applying HIPAA-only policies",
            "Update consent forms to reflect 2024 final rule changes allowing single prior consent for TPO",
            "Implement segmentation or flagging of Part 2 records in EHR systems",
            "Train workforce on redisclosure prohibition and required Part 2 notice",
            "Coordinate Part 2 compliance with state SUD confidentiality requirements",
        ],
        risk_factors=[
            "2024 final rule changes create transition compliance obligations",
            "Part 2 records in integrated EHR systems risk inadvertent redisclosure",
            "Criminal penalties attach to individuals who willfully violate Part 2",
        ],
    ),

    DoctrineCacheBlock(
        topic="pharmacy_law",
        summary="Pharmacy law encompasses federal and state regulation of the dispensing, distribution, and management of prescription drugs and controlled substances. The Controlled Substances Act (21 USC 801 et seq.) establishes schedules and requirements for controlled substance prescribing, dispensing, and record-keeping. The Drug Supply Chain Security Act (DSCSA) mandates an interoperable electronic system for drug tracing by 2024. The Drug Quality and Security Act (DQSA) established federal oversight of compounding pharmacies under Section 503A (traditional compounding) and Section 503B (outsourcing facilities). The 340B Drug Pricing Program (42 USC 256b) requires drug manufacturers to provide discounted drugs to eligible covered entities. State pharmacy practice acts govern pharmacist scope of practice, pharmacy licensing, and dispensing requirements.",
        key_statutes=[
            "21 USC 801 et seq. (Controlled Substances Act)",
            "21 USC 353a (Pharmacy compounding - Section 503A)",
            "21 USC 353b (Outsourcing facilities - Section 503B)",
            "21 USC 360eee et seq. (Drug Supply Chain Security Act)",
            "42 USC 256b (340B Drug Pricing Program)",
            "State pharmacy practice acts",
            "21 CFR Parts 1301-1321 (DEA regulations)",
        ],
        elements=[
            "Pharmacy or pharmacist operating within scope of state and federal law",
            "Valid prescription from authorized prescriber",
            "Controlled substance dispensing within DEA registration and record-keeping requirements",
            "Compliance with drug supply chain tracing requirements",
            "340B eligibility and duplicate discount prohibition compliance",
            "State pharmacy practice act licensing and operational requirements",
        ],
        defenses=[
            "Valid prescription from licensed prescriber within scope of practice",
            "Corresponding responsibility obligation met (pharmacist verification)",
            "DEA registration current and in good standing",
            "Compliance with state pharmacy practice act",
            "503A compounding exemption requirements met",
            "503B outsourcing facility registration and cGMP compliance",
        ],
        remedies=[
            "DEA registration revocation or suspension",
            "State pharmacy board disciplinary action (license suspension, revocation, probation)",
            "Criminal prosecution for controlled substance violations",
            "FDA enforcement against compounding violations (Warning Letters, injunctions)",
            "HRSA enforcement of 340B program requirements",
            "Civil monetary penalties",
            "Manufacturer dispute resolution for 340B pricing violations",
        ],
        leading_cases=[
            "Thompson v. Western States Medical Center, 535 U.S. 357 (2002) - commercial speech and compounding advertising",
            "Caremark Rx v. Tamoxifen Citrate Antitrust Litigation (settlements re: pharmacy benefit practices)",
            "AstraZeneca v. HRSA (340B dispute resolution proceedings)",
        ],
        category="pharmacy",
        subcategory="pharmacy_regulation",
        authority_score=0.82,
        confidence=0.84,
        related_topics=["controlled_substances", "fda_drug_regulation", "drug_pricing", "compounding"],
        practice_tips=[
            "Implement corresponding responsibility policies for controlled substance prescriptions",
            "Track DSCSA compliance deadlines for transaction information, history, and statements",
            "Conduct regular 340B program audits to prevent duplicate discounts and diversion",
            "Distinguish 503A traditional compounding from 503B outsourcing facility requirements",
            "Monitor state pharmacy practice act amendments for expanded pharmacist scope of practice",
        ],
        risk_factors=[
            "DEA targets pharmacies and prescribers with statistical outlier dispensing patterns",
            "340B program audit findings can result in manufacturer refusal to provide discounted drugs",
            "Compounding pharmacies face heightened scrutiny since NECC meningitis outbreak",
        ],
    ),

    DoctrineCacheBlock(
        topic="public_health_emergency",
        summary="Public health emergency (PHE) law authorizes federal, state, and local governments to take extraordinary measures during health emergencies. The HHS Secretary can declare a PHE under 42 USC 247d, triggering waiver authorities, liability protections, and funding mechanisms. The PREP Act (42 USC 247d-6d) provides broad immunity from liability for the manufacture, distribution, and administration of covered countermeasures. CMS Section 1135 waivers allow modification of Medicare/Medicaid requirements during emergencies. Emergency Use Authorizations (EUAs) permit FDA to authorize unapproved medical products during declared emergencies. The Stafford Act and National Emergencies Act provide additional emergency authorities.",
        key_statutes=[
            "42 USC 247d (Public Health Service Act - PHE declaration)",
            "42 USC 247d-6d (PREP Act - liability immunity)",
            "42 USC 1320b-5 (CMS Section 1135 waivers)",
            "21 USC 360bbb-3 (Emergency Use Authorization)",
            "42 USC 5121 et seq. (Stafford Act)",
            "50 USC 1601 et seq. (National Emergencies Act)",
        ],
        elements=[
            "HHS Secretary determination that PHE exists",
            "Disease or disorder presents a public health emergency or significant potential",
            "Scope of emergency declaration (geographic, temporal, subject matter)",
            "Waiver requests submitted and approved under applicable authority",
            "Covered countermeasure identified for PREP Act immunity",
        ],
        defenses=[
            "PREP Act immunity for administration of covered countermeasures",
            "Good faith compliance with emergency orders and directives",
            "Volunteer Protection Act immunity for uncompensated volunteers",
            "State emergency powers immunity provisions",
            "CMS Section 1135 waiver approved for specific requirement",
            "Emergency Use Authorization compliance",
        ],
        remedies=[
            "Countermeasures Injury Compensation Program (CICP) for PREP Act covered countermeasure injuries",
            "National Vaccine Injury Compensation Program (VICP) for routine vaccine injuries",
            "Federal tort claims for government employee negligence",
            "State tort claims where PREP Act immunity does not apply (willful misconduct exception)",
            "Administrative penalties for violation of emergency orders",
        ],
        leading_cases=[
            "Maglioli v. Alliance HC Holdings, 16 F.4th 393 (3d Cir. 2021) - PREP Act preemption and immunity scope",
            "Saldana v. Glenhaven Healthcare, 27 F.4th 679 (9th Cir. 2022) - PREP Act does not completely preempt state claims",
            "Cannon v. Watermark Retirement Communities, 2022 WL 2307590 (M.D. Fla. 2022) - PREP Act immunity analysis",
        ],
        category="public_health",
        subcategory="emergency_law",
        authority_score=0.82,
        confidence=0.83,
        related_topics=["fda_drug_regulation", "emtala", "telemedicine_regulation", "hipaa_privacy_rule"],
        practice_tips=[
            "Track active PHE declarations and associated waiver authorities",
            "Document reliance on CMS Section 1135 waivers with specific waiver citations",
            "Ensure PREP Act coverage by verifying countermeasure coverage and administration protocols",
            "Monitor PHE termination dates and transition planning for post-PHE operations",
            "Maintain emergency preparedness plans with legal authority documentation",
        ],
        risk_factors=[
            "PHE termination can abruptly end waiver authorities and liability protections",
            "PREP Act willful misconduct exception creates potential exposure",
            "State emergency declarations may have different scope and duration than federal PHE",
        ],
    ),

    DoctrineCacheBlock(
        topic="information_blocking",
        summary="The 21st Century Cures Act (Section 4004) and the ONC Information Blocking Final Rule (45 CFR Part 171) prohibit healthcare providers, health IT developers, and health information networks/exchanges from engaging in practices likely to interfere with the access, exchange, or use of electronic health information (EHI). Eight regulatory exceptions define permissible practices: preventing harm, privacy, security, infeasibility, health IT performance, content and manner, fees, and licensing. Healthcare providers face enforcement through appropriate disincentives determined by the HHS Secretary, while health IT developers and HIEs/HINs face civil monetary penalties of up to $1 million per violation.",
        key_statutes=[
            "42 USC 300jj-52 (Information blocking prohibition - Cures Act SS 4004)",
            "45 CFR Part 171 (Information Blocking regulations)",
            "45 CFR 171.100-171.103 (Definitions and applicability)",
            "45 CFR 171.200-171.202 (Exceptions for health IT developers/HIEs)",
            "45 CFR 171.300-171.303 (Exceptions available to all actors)",
            "45 CFR 171.400-171.403 (Exceptions for providers)",
        ],
        elements=[
            "Actor is a healthcare provider, health IT developer, or HIE/HIN",
            "Practice is likely to interfere with access, exchange, or use of EHI",
            "Actor knows or should know the practice is likely to interfere",
            "No applicable exception satisfied",
            "EHI includes USCDI data elements and broader electronic health information",
        ],
        defenses=[
            "Preventing harm exception (45 CFR 171.201): practice reasonably necessary to prevent harm",
            "Privacy exception (45 CFR 171.202): tailored to privacy concerns",
            "Security exception (45 CFR 171.203): tailored to security risks",
            "Infeasibility exception (45 CFR 171.204): practice is infeasible under the circumstances",
            "Health IT performance exception (45 CFR 171.205): maintaining or improving health IT",
            "Content and manner exception (45 CFR 171.301): offering alternative means of access",
            "Fees exception (45 CFR 171.302): fees are reasonable and justified",
            "Licensing exception (45 CFR 171.303): reasonable licensing terms",
        ],
        remedies=[
            "Civil monetary penalties up to $1M per violation (health IT developers and HIEs/HINs)",
            "Appropriate disincentives for healthcare providers (per HHS rulemaking)",
            "OIG enforcement authority",
            "ONC complaint process and investigation",
            "Certification program penalties for health IT developers",
            "Private litigation theories emerging",
        ],
        leading_cases=[
            "ONC Information Blocking Final Rule (85 FR 25642, May 1, 2020)",
            "HHS-OIG Final Rule on CMPs (88 FR 42820, July 3, 2023)",
        ],
        category="interoperability",
        subcategory="information_blocking",
        authority_score=0.80,
        confidence=0.82,
        related_topics=["hipaa_privacy_rule", "hipaa_security_rule", "healthcare_it", "patient_access_rights"],
        practice_tips=[
            "Conduct information blocking risk assessments for all data sharing practices",
            "Document reliance on specific exceptions with factual basis",
            "Ensure USCDI data elements are available through certified health IT",
            "Train workforce on information blocking prohibition and exception requirements",
            "Monitor ONC complaint investigations and enforcement trends",
        ],
        risk_factors=[
            "Definition of EHI expanded beyond USCDI to all electronic health information as of October 2022",
            "Provider disincentives rulemaking may create significant enforcement consequences",
            "Health IT developers face up to $1M per violation in civil monetary penalties",
        ],
    ),

    DoctrineCacheBlock(
        topic="healthcare_ma_con",
        summary="Healthcare mergers and acquisitions involve complex regulatory considerations including antitrust review, certificate of need (CON) laws, change of ownership (CHOW) requirements, state attorney general notification, and professional licensing transfers. The FTC and DOJ review healthcare transactions under the Hart-Scott-Rodino Act and Clayton Act. Approximately 35 states maintain CON programs requiring government approval before establishing or expanding healthcare facilities. CMS CHOW requirements (42 CFR 489.18) govern Medicare provider agreement transfers. Many states require advance notification to the attorney general for nonprofit hospital transactions. Professional licensing, accreditation, and managed care contract assignment add additional complexity.",
        key_statutes=[
            "15 USC 18 (Clayton Act Section 7 - mergers)",
            "15 USC 18a (Hart-Scott-Rodino Act - premerger notification)",
            "42 CFR 489.18 (CMS change of ownership requirements)",
            "State certificate of need statutes (approximately 35 states)",
            "State attorney general nonprofit conversion notification statutes",
            "State facility licensing transfer requirements",
        ],
        elements=[
            "Transaction involves healthcare entities (hospitals, physician groups, post-acute, etc.)",
            "HSR Act reporting thresholds met (size of transaction and parties)",
            "State CON approval required for new facility, service expansion, or capital expenditure",
            "Medicare/Medicaid CHOW notification and enrollment requirements",
            "State AG notification for nonprofit healthcare entity transactions",
            "Professional license and accreditation transfer or new application",
        ],
        defenses=[
            "HSR Act exemption (below reporting thresholds or exempt transaction type)",
            "No CON requirement in the jurisdiction or for the service at issue",
            "Asset purchase structured to avoid CHOW triggering (CMS guidance)",
            "State AG waiver or approval obtained",
            "Procompetitive justifications for the merger (efficiencies, quality improvement)",
            "Failing firm defense in antitrust review",
        ],
        remedies=[
            "FTC/DOJ injunction to block the transaction",
            "Consent decree with divestitures or behavioral conditions",
            "State AG challenge or conditions on approval",
            "CON denial preventing facility establishment or expansion",
            "CMS denial of new enrollment or assignment of provider agreement",
            "Post-closing antitrust enforcement (unwinding completed transactions)",
        ],
        leading_cases=[
            "FTC v. Hackensack Meridian Health, 30 F.4th 160 (3d Cir. 2022) - hospital merger challenge",
            "FTC v. Sanford Health/Sanford Bismarck, No. 1:17-cv-133 (D.N.D. 2017) - hospital merger blocked",
            "Saint Alphonsus Medical Center v. St. Luke's Health System, 778 F.3d 775 (9th Cir. 2015) - physician group acquisition",
            "FTC v. Advocate Health Care, 841 F.3d 460 (7th Cir. 2016) - geographic market definition",
        ],
        category="healthcare_ma",
        subcategory="mergers_acquisitions",
        authority_score=0.83,
        confidence=0.85,
        related_topics=["antitrust", "certificate_of_need", "change_of_ownership", "regulatory_approvals"],
        practice_tips=[
            "Map all federal, state, and local regulatory approvals early in transaction timeline",
            "Conduct CON assessment for all states where target operates facilities",
            "File CMS CHOW notification timely (before or within 30 days of closing)",
            "Evaluate state AG notification requirements for nonprofit entity transactions",
            "Structure transition services agreements to maintain continuity during regulatory transition",
        ],
        risk_factors=[
            "FTC has significantly increased healthcare merger enforcement since 2021",
            "State AG offices are increasingly active in reviewing healthcare transactions",
            "CON approval timelines can significantly delay transaction closing",
        ],
    ),

    DoctrineCacheBlock(
        topic="patient_rights",
        summary="Patient rights encompass a broad set of legal protections derived from federal and state law, constitutional principles, and professional ethics. Key federal rights include HIPAA privacy rights (access, amendment, accounting), EMTALA emergency treatment rights, ADA disability rights in healthcare settings, Section 1557 ACA nondiscrimination protections, informed consent rights, and the right to refuse treatment. Many states have enacted patient bills of rights covering hospital admission, information, consent, privacy, complaints, and advance directives. The Patient Self-Determination Act (42 USC 1395cc(f)) requires Medicare/Medicaid participating providers to inform patients of their rights regarding advance directives.",
        key_statutes=[
            "42 USC 1395cc(f) (Patient Self-Determination Act)",
            "45 CFR 164.524 (HIPAA right of access)",
            "42 USC 12182 (ADA Title III - public accommodations)",
            "42 USC 18116 (ACA Section 1557 - nondiscrimination)",
            "42 USC 1395dd (EMTALA)",
            "State patient bills of rights",
            "State advance directive statutes",
        ],
        elements=[
            "Patient has a legal right under applicable federal or state law",
            "Healthcare provider or facility has an obligation to honor the right",
            "Patient was denied the right or inadequately informed of the right",
            "Patient suffered harm or deprivation from the denial",
        ],
        defenses=[
            "Right was honored and documented",
            "Clinical justification for limitation (e.g., safety, capacity)",
            "Emergency exception to informed consent or advance directive",
            "Patient waived the right voluntarily and with understanding",
            "Surrogate decision-maker properly involved for incapacitated patients",
        ],
        remedies=[
            "OCR enforcement for HIPAA and Section 1557 violations",
            "ADA enforcement (DOJ, private right of action)",
            "State health department enforcement",
            "Medical malpractice or negligence claims",
            "State patient advocate or ombudsman intervention",
            "CMS conditions of participation enforcement",
        ],
        leading_cases=[
            "Cruzan v. Director, MDH, 497 U.S. 261 (1990) - constitutional right to refuse treatment",
            "Washington v. Glucksberg, 521 U.S. 702 (1997) - no constitutional right to physician-assisted suicide",
            "Ciox Health LLC v. Azar, 435 F. Supp. 3d 30 (D.D.C. 2020) - HIPAA right of access enforcement",
        ],
        category="patient_rights",
        subcategory="rights_overview",
        authority_score=0.84,
        confidence=0.86,
        related_topics=["hipaa_privacy_rule", "informed_consent", "emtala", "advance_directives", "nondiscrimination"],
        practice_tips=[
            "Provide patients with written notice of rights upon admission or first encounter",
            "Implement advance directive inquiry and documentation process per PSDA",
            "Honor patient access requests within 30 days per HIPAA",
            "Ensure language access services for limited English proficiency patients",
            "Train staff on recognizing and responding to patient rights complaints",
        ],
        risk_factors=[
            "OCR Right of Access Initiative enforcement is aggressive",
            "ADA and Section 1557 enforcement extends to telehealth accessibility",
            "State patient bills of rights may create additional obligations not present in federal law",
        ],
    ),

    DoctrineCacheBlock(
        topic="hospital_vicarious_liability",
        summary="Hospitals face vicarious liability for the acts of their employees under respondeat superior and may also be liable for the acts of independent contractor physicians under ostensible agency (apparent authority), nondelegable duty, or corporate negligence theories. The corporate negligence doctrine (established in Darling v. Charleston Community Memorial Hospital) imposes a direct duty on hospitals to ensure the quality of care provided within their facilities, including obligations to credential and privilege physicians, maintain adequate staffing, enforce policies and procedures, and oversee the quality of patient care. Many states recognize ostensible agency liability when the hospital holds the physician out as its agent and the patient looks to the hospital for care.",
        key_statutes=[
            "Restatement (Third) of Agency SS 2.03 (Apparent authority)",
            "Restatement (Third) of Agency SS 7.07 (Respondeat superior)",
            "State vicarious liability and agency statutes",
            "HCQIA (42 USC 11101 et seq.) - peer review protections",
            "State credentialing and peer review statutes",
        ],
        elements=[
            "Hospital-physician relationship (employment, contract, privileges)",
            "Physician negligence or malpractice",
            "Agency relationship (actual or apparent) between hospital and physician",
            "Patient reasonably relied on the appearance of agency",
            "Hospital failed to exercise reasonable care in credentialing, supervision, or oversight",
        ],
        defenses=[
            "Independent contractor relationship with clear patient disclosure",
            "HCQIA immunity for peer review actions taken in good faith",
            "Adequate credentialing and privileging process followed",
            "State damage caps for hospital malpractice",
            "Physician exercised independent medical judgment",
            "Patient was aware physician was not a hospital employee",
        ],
        remedies=[
            "Compensatory damages for medical malpractice",
            "Punitive damages where gross negligence or reckless conduct shown",
            "NPDB reporting for adverse privileging actions",
            "Loss of accreditation (Joint Commission, state)",
            "CMS conditions of participation enforcement",
        ],
        leading_cases=[
            "Darling v. Charleston Community Memorial Hospital, 33 Ill.2d 326 (1965) - corporate negligence doctrine",
            "Petrovich v. Share Health Plan, 188 Ill.2d 17 (1999) - ostensible agency in managed care",
            "Sword v. NKC Hospitals, 714 N.E.2d 142 (Ind. 1999) - apparent authority for ER physicians",
        ],
        category="malpractice",
        subcategory="vicarious_liability",
        authority_score=0.84,
        confidence=0.86,
        related_topics=["medical_malpractice", "informed_consent", "credentialing", "peer_review"],
        practice_tips=[
            "Require independent contractor physicians to disclose their status to patients",
            "Implement robust credentialing and privileging processes with ongoing monitoring",
            "Maintain adequate malpractice insurance covering all agency theories",
            "Document peer review proceedings under HCQIA protections",
            "Review marketing materials to ensure they do not create apparent agency",
        ],
        risk_factors=[
            "ED physicians almost always create ostensible agency liability for hospitals",
            "Failure to investigate red flags in credentialing exposes hospital to corporate negligence",
            "NPDB queries are mandatory every two years for privileged practitioners",
        ],
    ),

    DoctrineCacheBlock(
        topic="state_medical_licensing",
        summary="State medical boards regulate physician licensing, scope of practice, continuing medical education, professional conduct, and disciplinary proceedings. Each state has a medical practice act defining the practice of medicine, licensing requirements, grounds for discipline, and due process protections. The Interstate Medical Licensure Compact (IMLC) streamlines multi-state licensure for qualified physicians. Disciplinary actions include letters of reprimand, probation, suspension, and revocation. The NPDB requires reporting of adverse licensing and privileging actions. Telemedicine has intensified licensing issues as physicians must generally be licensed in the state where the patient is located.",
        key_statutes=[
            "State medical practice acts (each state)",
            "Interstate Medical Licensure Compact (IMLC)",
            "42 USC 11101 et seq. (HCQIA and NPDB reporting)",
            "State continuing medical education requirements",
            "State scope of practice statutes for APRNs, PAs",
        ],
        elements=[
            "Physician practicing medicine within the jurisdiction",
            "Valid license required for the practice of medicine in the state",
            "Grounds for discipline: unprofessional conduct, incompetence, impairment, fraud, criminal conviction",
            "Due process protections in disciplinary proceedings (notice, hearing, appeal)",
            "NPDB reporting obligations for adverse actions",
        ],
        defenses=[
            "Valid and current medical license in the state",
            "Conduct does not constitute the practice of medicine",
            "IMLC license covers the jurisdiction",
            "Consultation exception (some states)",
            "Due process violation in disciplinary proceeding",
            "Rehabilitation and monitoring programs for impaired physicians",
        ],
        remedies=[
            "License suspension or revocation",
            "Probation with conditions (monitoring, CME, practice restrictions)",
            "Letter of reprimand or admonition",
            "Civil penalties",
            "Criminal prosecution for unlicensed practice of medicine",
            "NPDB reporting of adverse action",
            "Injunctive relief against unlicensed practice",
        ],
        leading_cases=[
            "Goldfarb v. Virginia State Bar, 421 U.S. 773 (1975) - professional regulation subject to antitrust",
            "North Carolina Board of Dental Examiners v. FTC, 574 U.S. 494 (2015) - state action immunity for licensing boards",
        ],
        category="licensing",
        subcategory="medical_licensing",
        authority_score=0.82,
        confidence=0.84,
        related_topics=["telemedicine_regulation", "scope_of_practice", "credentialing", "peer_review"],
        practice_tips=[
            "Verify licensure in every state where patients are treated including via telemedicine",
            "Consider IMLC for physicians practicing in multiple compact states",
            "Monitor license renewal deadlines and CME requirements",
            "Report adverse actions to NPDB within required timeframes",
            "Engage healthcare licensing counsel early in disciplinary investigations",
        ],
        risk_factors=[
            "Practicing without a license is a criminal offense in every state",
            "NPDB reports are permanent and visible to all querying entities",
            "Board disciplinary proceedings can result in loss of hospital privileges and insurance panels",
        ],
    ),

    DoctrineCacheBlock(
        topic="business_associate_agreements",
        summary="HIPAA requires covered entities to enter into business associate agreements (BAAs) with business associates - persons or entities that perform functions or activities on behalf of a covered entity involving the use or disclosure of PHI. The HITECH Act extended direct HIPAA liability to business associates for Security Rule compliance and certain Privacy Rule provisions. BAAs must contain required provisions including permitted uses and disclosures, safeguards, breach notification obligations, subcontractor BAA requirements, and termination provisions. The BAA must ensure the business associate will not use or disclose PHI other than as permitted by the agreement or required by law.",
        key_statutes=[
            "45 CFR 164.502(e) (Business associate requirements)",
            "45 CFR 164.504(e) (BAA required provisions)",
            "45 CFR 160.103 (Business associate definition)",
            "HITECH Act SS 13401 (Direct business associate liability)",
            "HITECH Act SS 13404 (Business associate security obligations)",
        ],
        elements=[
            "Entity performs functions or activities involving PHI on behalf of covered entity",
            "Relationship meets the definition of business associate (not workforce member)",
            "Written business associate agreement required",
            "BAA contains all required provisions per 45 CFR 164.504(e)",
            "Business associate complies with applicable HIPAA requirements",
        ],
        defenses=[
            "Entity is not a business associate (e.g., conduit exception for mere transmission)",
            "Valid BAA in place with all required provisions",
            "Covered entity took reasonable steps to cure BA violation",
            "Business associate complied with BAA requirements",
            "Employment relationship (workforce member, not BA)",
        ],
        remedies=[
            "OCR enforcement against both covered entity and business associate",
            "Civil monetary penalties for BA agreement failures",
            "Termination of business associate relationship required upon knowledge of material violation",
            "Breach notification obligations triggered by BA breaches",
            "State AG enforcement under HITECH",
        ],
        leading_cases=[
            "CHSPSC LLC OCR Settlement (2020) - $2.3M for BA breach affecting 6M individuals",
            "Advanced Care Hospitalists OCR Settlement (2018) - BA oversight failures",
        ],
        category="hipaa",
        subcategory="business_associate",
        authority_score=0.87,
        confidence=0.89,
        related_topics=["hipaa_privacy_rule", "hipaa_security_rule", "hipaa_breach_notification", "subcontractor_oversight"],
        practice_tips=[
            "Maintain an inventory of all business associates with BAA status tracking",
            "Include indemnification and cyber liability insurance provisions in BAAs",
            "Require business associates to complete due diligence questionnaires annually",
            "Establish BA breach notification timelines shorter than the 60-day regulatory maximum",
            "Address subcontractor BAA requirements in the primary BAA",
        ],
        risk_factors=[
            "Many data breaches originate from business associate systems",
            "Failure to have a BAA in place is itself an independent HIPAA violation",
            "Covered entities must terminate BA relationships upon knowledge of material BAA violation",
        ],
    ),
]


# ============================================================================
# DOCTRINE CACHE INDEX
# ============================================================================

class DoctrineCacheIndex:
    """Fast O(1) lookup index over doctrine cache blocks."""

    def __init__(self, blocks: List[DoctrineCacheBlock]) -> None:
        self._blocks: List[DoctrineCacheBlock] = blocks
        self._by_topic: Dict[str, DoctrineCacheBlock] = {}
        self._by_category: Dict[str, List[DoctrineCacheBlock]] = {}
        self._by_subcategory: Dict[str, List[DoctrineCacheBlock]] = {}
        self._all_topics: Set[str] = set()
        self._all_categories: Set[str] = set()
        self._build_index()

    def _build_index(self) -> None:
        """Build the index from blocks."""
        for block in self._blocks:
            self._by_topic[block.topic] = block
            self._all_topics.add(block.topic)
            self._all_categories.add(block.category)
            if block.category not in self._by_category:
                self._by_category[block.category] = []
            self._by_category[block.category].append(block)
            if block.subcategory:
                if block.subcategory not in self._by_subcategory:
                    self._by_subcategory[block.subcategory] = []
                self._by_subcategory[block.subcategory].append(block)
        logger.info(
            f"DoctrineCacheIndex built | topics={len(self._by_topic)} | "
            f"categories={len(self._by_category)} | subcategories={len(self._by_subcategory)}"
        )

    def get_by_topic(self, topic: str) -> Optional[DoctrineCacheBlock]:
        """Retrieve a block by canonical topic name."""
        return self._by_topic.get(topic)

    def get_by_category(self, category: str) -> List[DoctrineCacheBlock]:
        """Retrieve all blocks in a category."""
        return self._by_category.get(category, [])

    def get_by_subcategory(self, subcategory: str) -> List[DoctrineCacheBlock]:
        """Retrieve all blocks in a subcategory."""
        return self._by_subcategory.get(subcategory, [])

    def search_blocks(self, query: str, top_k: int = 5) -> List[DoctrineCacheBlock]:
        """Free-text search over doctrine blocks by keyword matching."""
        query_lower = query.lower()
        query_tokens = set(query_lower.split())
        scored: List[tuple[float, DoctrineCacheBlock]] = []

        for block in self._blocks:
            content = block.content_for_search().lower()
            score = 0.0
            for token in query_tokens:
                if token in content:
                    score += 1.0
                if token in block.topic.lower():
                    score += 2.0
                if token in block.category.lower():
                    score += 1.5
            if score > 0:
                scored.append((score * block.authority_score, block))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [block for _, block in scored[:top_k]]

    @property
    def all_topics(self) -> Set[str]:
        """Return all indexed topics."""
        return self._all_topics

    @property
    def all_categories(self) -> Set[str]:
        """Return all indexed categories."""
        return self._all_categories

    @property
    def block_count(self) -> int:
        """Return total number of indexed blocks."""
        return len(self._blocks)


# ============================================================================
# MODULE-LEVEL FUNCTIONS
# ============================================================================

_CACHE_INSTANCE: Optional[DoctrineCacheIndex] = None


def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build the doctrine cache index from DOCTRINE_BLOCKS."""
    global _CACHE_INSTANCE
    _CACHE_INSTANCE = DoctrineCacheIndex(DOCTRINE_BLOCKS)
    logger.info(f"Doctrine cache built with {len(DOCTRINE_BLOCKS)} blocks")
    return _CACHE_INSTANCE


def get_doctrine_cache() -> DoctrineCacheIndex:
    """Get or build the doctrine cache index."""
    global _CACHE_INSTANCE
    if _CACHE_INSTANCE is None:
        return build_doctrine_cache()
    return _CACHE_INSTANCE


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Retrieve a single doctrine block by topic."""
    cache = get_doctrine_cache()
    return cache.get_by_topic(topic)


def search_doctrines(query: str, top_k: int = 5) -> List[DoctrineCacheBlock]:
    """Free-text search over doctrine blocks."""
    cache = get_doctrine_cache()
    return cache.search_blocks(query, top_k=top_k)


def get_coverage_map() -> Dict[str, Any]:
    """Return coverage map of all doctrine topics with staleness data."""
    cache = get_doctrine_cache()
    coverage: Dict[str, Any] = {}
    for block in DOCTRINE_BLOCKS:
        coverage[block.topic] = {
            "category": block.category,
            "subcategory": block.subcategory,
            "authority_score": block.authority_score,
            "confidence": block.confidence,
            "last_updated": block.last_updated,
            "staleness_days": block.staleness_days,
            "related_topics": block.related_topics,
            "jurisdiction": block.jurisdiction,
            "hash": block.compute_hash(),
        }
    return coverage


def get_all_doctrine_topics() -> List[str]:
    """Return list of all doctrine topics."""
    return [block.topic for block in DOCTRINE_BLOCKS]


def get_all_doctrine_categories() -> List[str]:
    """Return list of all unique doctrine categories."""
    return list(set(block.category for block in DOCTRINE_BLOCKS))


def get_doctrine_cache_stats() -> Dict[str, Any]:
    """Return statistics about the doctrine cache."""
    categories = {}
    for block in DOCTRINE_BLOCKS:
        if block.category not in categories:
            categories[block.category] = 0
        categories[block.category] += 1

    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "categories": categories,
        "total_categories": len(categories),
        "avg_authority_score": round(sum(b.authority_score for b in DOCTRINE_BLOCKS) / max(len(DOCTRINE_BLOCKS), 1), 4),
        "avg_confidence": round(sum(b.confidence for b in DOCTRINE_BLOCKS) / max(len(DOCTRINE_BLOCKS), 1), 4),
    }


def get_doctrine_cache_hash() -> str:
    """Compute SHA-256 hash of the entire doctrine cache for integrity verification."""
    content = json.dumps([b.to_dict() for b in DOCTRINE_BLOCKS], sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get_stale_doctrines(threshold_days: int = 90) -> List[DoctrineCacheBlock]:
    """Return doctrine blocks that exceed the staleness threshold."""
    return [b for b in DOCTRINE_BLOCKS if b.staleness_days > threshold_days]


def verify_doctrine_integrity() -> Dict[str, Any]:
    """Verify the integrity of the doctrine cache."""
    issues: List[str] = []
    topics_seen: Set[str] = set()

    for i, block in enumerate(DOCTRINE_BLOCKS):
        if not block.topic:
            issues.append(f"Block {i} has empty topic")
        if block.topic in topics_seen:
            issues.append(f"Duplicate topic: {block.topic}")
        topics_seen.add(block.topic)
        if not block.summary:
            issues.append(f"Block {block.topic} has empty summary")
        if not block.key_statutes:
            issues.append(f"Block {block.topic} has no key statutes")
        if not block.elements:
            issues.append(f"Block {block.topic} has no elements")
        if not block.category:
            issues.append(f"Block {block.topic} has no category")
        if block.authority_score < 0.0 or block.authority_score > 1.0:
            issues.append(f"Block {block.topic} has invalid authority score: {block.authority_score}")
        if block.confidence < 0.0 or block.confidence > 1.0:
            issues.append(f"Block {block.topic} has invalid confidence: {block.confidence}")

    return {
        "valid": len(issues) == 0,
        "total_blocks": len(DOCTRINE_BLOCKS),
        "unique_topics": len(topics_seen),
        "issues": issues,
        "cache_hash": get_doctrine_cache_hash(),
    }
