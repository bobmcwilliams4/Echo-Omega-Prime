"""
REG08: Healthcare Regulatory Intelligence Engine v1.0.0
TIE-Grade Compliance Engine for HIPAA, Stark, AKS, FCA, FDA, DEA, EMTALA, 340B
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Literal
from dataclasses import dataclass, field, asdict
from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger

# ==================== ENUMS ====================
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class IssueCategory(str, Enum):
    HIPAA_PRIVACY = "HIPAA_PRIVACY"
    HIPAA_SECURITY = "HIPAA_SECURITY"
    STARK_LAW = "STARK_LAW"
    ANTI_KICKBACK = "ANTI_KICKBACK"
    FALSE_CLAIMS = "FALSE_CLAIMS"
    MEDICARE_COP = "MEDICARE_COP"
    MEDICAID_MC = "MEDICAID_MC"
    FDA_COMPLIANCE = "FDA_COMPLIANCE"
    DEA_CONTROLLED = "DEA_CONTROLLED"
    EMTALA = "EMTALA"
    DRUG_340B = "DRUG_340B"
    TELEHEALTH = "TELEHEALTH"
    STATE_MEDICAL = "STATE_MEDICAL"

class Zone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

# ==================== DATA MODELS ====================
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
    controlling_precedent: List[str]
    category: IssueCategory

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    mode: ResponseMode = ResponseMode.FAST
    zone: Zone = Zone.PLANNING

class QueryResponse(BaseModel):
    response: str
    mode: ResponseMode
    zone: Zone
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    latency_ms: int
    determinism_hash: str
    sources: List[str]

# ==================== DOCTRINE CACHE ====================
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="HIPAA Privacy Rule - Protected Health Information",
        keywords=["phi", "protected health information", "privacy", "minimum necessary", "use disclosure"],
        conclusion_template=[
            "PHI disclosures must satisfy the minimum necessary standard under 45 CFR 164.502(b).",
            "Covered entities must limit PHI use/disclosure to the minimum necessary to accomplish the intended purpose.",
            "Treatment, payment, and healthcare operations have specific minimum necessary exceptions."
        ],
        reasoning_framework="""45 CFR 164.502(b) requires covered entities to make reasonable efforts to limit PHI to the minimum necessary to accomplish the intended purpose. The rule applies to uses, disclosures, and requests for PHI. Exceptions exist for treatment providers (no minimum necessary limit), disclosures to the individual, disclosures pursuant to authorization, required by law disclosures, and disclosures to HHS for compliance investigations. Covered entities must implement policies limiting routine and non-routine uses/disclosures and requests for PHI. Business associates inherit the same minimum necessary obligations under 45 CFR 164.504(e). Violations carry civil penalties up to $1.5M per violation category per year, plus criminal penalties for knowing violations (42 USC 1320d-5, 1320d-6).""",
        key_factors=["purpose of use/disclosure", "workforce role-based access", "treatment exception", "authorization scope", "business associate agreement"],
        primary_authority=["45 CFR 164.502(b)", "45 CFR 164.514(d)", "45 CFR 164.504(e)", "42 USC 1320d-5"],
        burden_holder="covered entity",
        adversary_position="OCR enforcement claims unnecessary disclosure",
        counter_arguments=["treatment exception applied", "individual authorized disclosure", "required by law", "minimum necessary policy documented"],
        resolution_strategy="Document minimum necessary determination with role-based access controls and routine/non-routine disclosure policies",
        entity_scope="covered entities, business associates, hybrid entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statute is explicit on minimum necessary requirement, extensive OCR guidance available",
        controlling_precedent=["45 CFR 164.502(b)", "OCR Minimum Necessary Guidance 2013"],
        category=IssueCategory.HIPAA_PRIVACY
    ),
    DoctrineBlock(
        topic="HIPAA Security Rule - Technical Safeguards",
        keywords=["security", "technical safeguards", "encryption", "access controls", "audit controls"],
        conclusion_template=[
            "Technical safeguards under 45 CFR 164.312 require access controls, audit controls, integrity controls, and transmission security.",
            "Encryption is addressable, not required, but unencrypted PHI creates breach notification obligations.",
            "Risk analysis determines the appropriate technical safeguard implementation."
        ],
        reasoning_framework="""45 CFR 164.312 mandates technical safeguards to protect ePHI. Required specifications: access control (unique user identification, emergency access, automatic logoff, encryption/decryption addressable), audit controls (hardware/software/procedural mechanisms recording ePHI access), integrity (mechanisms to corroborate ePHI has not been altered), person or entity authentication, transmission security (integrity controls required, encryption addressable). Encryption is addressable - if not implemented, covered entity must document why and implement equivalent alternative measure. Unencrypted ePHI breach triggers notification under 45 CFR 164.404-414 unless covered entity demonstrates low probability of compromise. Safe harbor: encrypted ePHI using NIST-approved algorithms is not a breach. Risk analysis under 45 CFR 164.308(a)(1)(ii)(A) drives implementation decisions.""",
        key_factors=["risk analysis", "encryption implementation", "access control mechanisms", "audit log retention", "transmission security"],
        primary_authority=["45 CFR 164.312", "45 CFR 164.308(a)(1)(ii)(A)", "45 CFR 164.402(2)", "NIST SP 800-66r1"],
        burden_holder="covered entity",
        adversary_position="OCR claims inadequate technical safeguards after breach",
        counter_arguments=["risk analysis documented encryption decision", "equivalent alternative implemented", "NIST-compliant encryption used", "low probability of compromise shown"],
        resolution_strategy="Conduct annual risk analysis, document encryption decision, implement NIST-approved algorithms for ePHI at rest and in transit",
        entity_scope="covered entities, business associates",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulation provides addressable vs required distinction, OCR guidance on encryption safe harbor",
        controlling_precedent=["45 CFR 164.312", "OCR Breach Notification Guidance 2013"],
        category=IssueCategory.HIPAA_SECURITY
    ),
    DoctrineBlock(
        topic="Stark Law - Physician Self-Referral Prohibition",
        keywords=["stark", "self-referral", "designated health services", "financial relationship", "compensation exception"],
        conclusion_template=[
            "Stark Law prohibits physician referrals for designated health services to entities with which the physician has a financial relationship, unless an exception applies (42 USC 1395nn).",
            "Strict liability statute - no intent required, violation triggers payment denial and refund obligations.",
            "Compensation arrangements must satisfy an exception (fair market value, commercially reasonable, no volume/value consideration)."
        ],
        reasoning_framework="""42 USC 1395nn(a)(1) prohibits a physician from making a referral for designated health services (DHS) to an entity with which the physician or immediate family member has a financial relationship, unless an exception applies. DHS includes clinical lab, PT/OT, radiology, radiation therapy, DME, parenteral/enteral nutrients, prosthetics, home health, outpatient prescription drugs, inpatient/outpatient hospital services. Financial relationship = ownership/investment interest or compensation arrangement. Strict liability - no scienter required. Violation consequences: Medicare denies payment for referred services, entity must refund payments, civil penalties up to $15K per service plus $100K for circumvention schemes (42 USC 1395nn(g)). Exceptions in 42 USC 1395nn(b)-(e): physician services, in-office ancillary services, ownership in publicly traded securities, rental of office space/equipment (if at FMV, commercially reasonable, no volume/value), bona fide employment (if at FMV, commercially reasonable, no volume/value), personal services arrangements (same requirements). Exception burden is on the entity. CMS Phase IV final rule (2021) added value-based exceptions.""",
        key_factors=["DHS referral", "financial relationship", "exception applicability", "fair market value", "commercial reasonableness", "volume/value of referrals"],
        primary_authority=["42 USC 1395nn", "42 CFR 411.350-411.389", "CMS-1734-F Phase IV Final Rule"],
        burden_holder="entity receiving referral",
        adversary_position="CMS claims financial relationship violates Stark, no exception satisfied",
        counter_arguments=["no DHS involved", "exception fully satisfied", "FMV determination documented", "commercially reasonable independent of referrals", "no volume/value consideration"],
        resolution_strategy="Document exception compliance (FMV valuation, commercial reasonableness analysis, no volume/value linkage), annual Stark audit",
        entity_scope="physicians, DHS entities, group practices",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strict liability statute with extensive regulatory exceptions, CMS guidance available",
        controlling_precedent=["42 USC 1395nn", "42 CFR 411.357"],
        category=IssueCategory.STARK_LAW
    ),
    DoctrineBlock(
        topic="Anti-Kickback Statute - Remuneration for Referrals",
        keywords=["anti-kickback", "remuneration", "referral", "safe harbor", "one purpose test"],
        conclusion_template=[
            "AKS prohibits knowingly and willfully offering, paying, soliciting, or receiving remuneration to induce or reward referrals of federal healthcare program business (42 USC 1320a-7b(b)).",
            "Criminal statute - one purpose test: if one purpose is to induce referrals, violation occurs even if other legitimate purposes exist.",
            "Safe harbors protect arrangements that fully comply with regulatory requirements."
        ],
        reasoning_framework="""42 USC 1320a-7b(b) makes it a felony to knowingly and willfully offer, pay, solicit, or receive any remuneration (including kickback, bribe, rebate) to induce or reward referrals for items/services reimbursable by federal healthcare programs. Remuneration is broadly defined - anything of value. One purpose test (US v. Greber, 760 F.2d 68): if one purpose of remuneration is to induce referrals, the statute is violated even if there are other legitimate purposes. Intent requirement: knowing and willful, but knowledge of the statute not required (US v. Jain, 93 F.3d 436). Penalties: criminal (up to 5 years, $25K fine per violation), civil ($50K per violation plus 3x damages), exclusion from federal programs. Safe harbors in 42 CFR 1001.952 provide complete protection if all elements satisfied: investment interests, space/equipment rental, employment, personal services, discounts, waivers of coinsurance, others. Safe harbors are voluntary - arrangement can be lawful without fitting a safe harbor, but bears enforcement risk.""",
        key_factors=["remuneration provided", "referral inducement purpose", "federal program involvement", "safe harbor compliance", "knowing and willful intent"],
        primary_authority=["42 USC 1320a-7b(b)", "42 CFR 1001.952", "US v. Greber, 760 F.2d 68", "US v. Jain, 93 F.3d 436"],
        burden_holder="government (criminal), relator (civil)",
        adversary_position="DOJ/OIG claims remuneration designed to induce referrals",
        counter_arguments=["safe harbor fully satisfied", "no referral inducement purpose", "fair market value for legitimate services", "no federal program business involved"],
        resolution_strategy="Structure arrangements to fit safe harbors (FMV, advance writing, no volume/value), obtain OIG advisory opinion for novel arrangements",
        entity_scope="healthcare providers, suppliers, federal program participants",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Criminal statute with one purpose test creates enforcement risk even with legitimate business purposes",
        controlling_precedent=["42 USC 1320a-7b(b)", "US v. Greber"],
        category=IssueCategory.ANTI_KICKBACK
    ),
    DoctrineBlock(
        topic="False Claims Act - Healthcare Fraud",
        keywords=["false claims", "knowingly", "implied certification", "worthless services", "qui tam"],
        conclusion_template=[
            "FCA imposes liability for knowingly presenting false or fraudulent claims for payment to the federal government (31 USC 3729(a)(1)(A)).",
            "Implied certification theory: submitting a claim impliedly certifies compliance with material statutory, regulatory, or contractual requirements.",
            "Penalties: $11,665 to $23,331 per false claim plus treble damages, qui tam relators receive 15-30% of recovery."
        ],
        reasoning_framework="""31 USC 3729(a)(1)(A) imposes liability on anyone who knowingly presents a false or fraudulent claim for payment to the US. Knowingly means actual knowledge, deliberate ignorance, or reckless disregard (31 USC 3729(b)(1)) - no specific intent to defraud required. Implied certification theory (Universal Health Services v. US ex rel. Escobar, 579 US 176, 2016): submitting a claim for payment impliedly certifies compliance with material statutory, regulatory, or contractual requirements; violation of material conditions can be FCA violation. Materiality requires showing government payment decision would be affected. Worthless services doctrine: services so deficient they have no value. Stark/AKS violations can be predicate for FCA liability if they taint the claim. Penalties: civil penalties $11,665-$23,331 per claim (2023 amounts) plus treble damages. Qui tam provisions (31 USC 3730(b)) allow private relators to bring suit on behalf of US, receive 15-30% of recovery. 60-day statute of limitations to repay overpayments (42 USC 1320a-7k(d)) - failure triggers FCA liability.""",
        key_factors=["false claim submission", "knowing standard", "materiality of requirement", "government payment decision", "worthless services", "overpayment retention"],
        primary_authority=["31 USC 3729", "Universal Health Services v. Escobar, 579 US 176", "42 USC 1320a-7k(d)"],
        burden_holder="government or qui tam relator",
        adversary_position="DOJ/relator claims false claims knowingly submitted",
        counter_arguments=["no false statement", "no materiality", "disclosed violation to government", "services had value", "overpayment repaid within 60 days"],
        resolution_strategy="Implement compliance program, voluntary self-disclosure of violations, repay overpayments within 60 days of identification",
        entity_scope="healthcare providers, suppliers, billing entities",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Implied certification theory expands FCA liability, materiality is fact-intensive",
        controlling_precedent=["31 USC 3729", "Universal Health Services v. Escobar"],
        category=IssueCategory.FALSE_CLAIMS
    ),
    DoctrineBlock(
        topic="Medicare Conditions of Participation - Hospital Requirements",
        keywords=["conditions of participation", "cop", "hospital", "deemed status", "immediate jeopardy"],
        conclusion_template=[
            "Hospitals participating in Medicare must comply with Conditions of Participation in 42 CFR 482.",
            "Non-compliance can result in termination of Medicare provider agreement, loss of deemed status, or immediate jeopardy findings.",
            "CoPs cover governing body, medical staff, nursing services, pharmaceutical services, infection control, patient rights, quality assessment."
        ],
        reasoning_framework="""42 CFR 482 establishes Conditions of Participation (CoPs) for hospitals participating in Medicare. Requirements include: governing body responsible for management/policies (482.12), medical staff credentialing/privileging (482.22), nursing services with sufficient RN staff (482.23), pharmaceutical services with policies for safe medication use (482.25), infection prevention/control program (482.42), patient rights including informed consent/advance directives (482.13), quality assessment/performance improvement program (482.21), medical record services (482.24), emergency services if provided (482.55). Surveys conducted by state agencies or accrediting organizations (Joint Commission, DNV). Deemed status: Joint Commission accreditation deems CoP compliance. Findings: standard-level deficiency (plan of correction), condition-level deficiency (threat to patient health/safety, 90-day correction period or termination), immediate jeopardy (serious injury/harm/death likely, immediate correction required or termination). Termination consequences: no Medicare reimbursement, 2-year re-enrollment bar. Appeal rights under 42 CFR 498.""",
        key_factors=["CoP requirement violated", "deficiency level", "immediate jeopardy finding", "correction timeline", "deemed status"],
        primary_authority=["42 CFR 482", "42 CFR 488", "42 CFR 498", "CMS State Operations Manual"],
        burden_holder="hospital",
        adversary_position="CMS/state agency claims CoP violation threatens patient safety",
        counter_arguments=["no deficiency exists", "deficiency corrected", "no immediate jeopardy", "deemed status applies", "appeal pending"],
        resolution_strategy="Implement compliance monitoring, immediate correction for immediate jeopardy, plan of correction for standard deficiencies, maintain Joint Commission accreditation",
        entity_scope="Medicare-participating hospitals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CoPs are detailed regulatory requirements with CMS enforcement guidance",
        controlling_precedent=["42 CFR 482", "CMS SOM Appendix A"],
        category=IssueCategory.MEDICARE_COP
    ),
    DoctrineBlock(
        topic="EMTALA - Emergency Medical Treatment and Labor Act",
        keywords=["emtala", "emergency department", "screening", "stabilization", "transfer", "patient dumping"],
        conclusion_template=[
            "EMTALA requires hospitals with emergency departments to provide medical screening exam and stabilization for anyone requesting emergency treatment (42 USC 1395dd).",
            "Hospitals cannot delay screening/stabilization to inquire about insurance or payment.",
            "Unstable patients can only be transferred if benefits outweigh risks and receiving facility accepts."
        ],
        reasoning_framework="""42 USC 1395dd applies to hospitals with emergency departments participating in Medicare. Requirements: (1) Medical screening exam: hospital must provide appropriate medical screening exam to determine if emergency medical condition exists (1395dd(a)). (2) Stabilization: if emergency condition exists, hospital must provide treatment to stabilize condition or transfer under specified conditions (1395dd(b)). (3) Transfer restrictions: unstable patient can only be transferred if (a) individual requests transfer, (b) physician certifies benefits outweigh risks, (c) receiving facility accepts, (d) transferring hospital provides medical records, (e) transfer uses qualified personnel/equipment (1395dd(c)). Emergency medical condition = condition manifesting acute symptoms such that absence of immediate medical attention could reasonably result in serious jeopardy to health, serious impairment to bodily functions, or serious dysfunction of bodily organ. Includes active labor. On-call physician obligations (42 CFR 489.24(j)). Penalties: civil penalties up to $119,942 per violation (2023), termination of Medicare agreement, private cause of action for individuals harmed. Hospital cannot delay screening/stabilization/transfer to inquire about payment.""",
        key_factors=["emergency department", "request for examination", "emergency medical condition", "stabilization provided", "transfer appropriateness"],
        primary_authority=["42 USC 1395dd", "42 CFR 489.24", "CMS EMTALA Interpretive Guidelines"],
        burden_holder="hospital",
        adversary_position="CMS/patient claims EMTALA violation - inadequate screening, failure to stabilize, inappropriate transfer",
        counter_arguments=["appropriate screening conducted", "no emergency condition found", "patient stabilized", "transfer met all requirements", "patient requested transfer"],
        resolution_strategy="Implement EMTALA policies, train ED staff, maintain on-call physician list, document all screening/stabilization, never delay for payment inquiry",
        entity_scope="hospitals with emergency departments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statute is explicit on screening/stabilization requirements, extensive CMS guidance",
        controlling_precedent=["42 USC 1395dd", "42 CFR 489.24"],
        category=IssueCategory.EMTALA
    ),
    DoctrineBlock(
        topic="340B Drug Pricing Program",
        keywords=["340b", "covered entity", "disproportionate share", "contract pharmacy", "duplicate discount"],
        conclusion_template=[
            "340B program requires drug manufacturers to provide discounts to covered entities serving vulnerable populations (42 USC 256b).",
            "Covered entities include DSH hospitals, FQHCs, Ryan White clinics, and other specified facilities.",
            "Program integrity requirements: no duplicate discounts, no diversion to ineligible patients, accurate data reporting."
        ],
        reasoning_framework="""42 USC 256b requires drug manufacturers participating in Medicaid to offer discounted pricing to covered entities. Covered entities include: disproportionate share hospitals (DSH hospitals with DSH adjustment percentage >11.75%), federally qualified health centers (FQHCs), Ryan White HIV/AIDS Program grantees, family planning clinics, tuberculosis clinics, hemophilia treatment centers, others specified in statute. Eligibility verified through HRSA Office of Pharmacy Affairs (OPA). Contract pharmacy arrangements allowed but subject to HRSA oversight. Program integrity requirements: (1) No duplicate discounts - cannot use 340B and Medicaid rebate on same drug, (2) No diversion - drugs purchased at 340B price only for eligible patients, (3) Accurate data reporting to OPA. Eligible patient definition (HRSA guidance): individual receiving healthcare service from covered entity, covered entity has provider-patient relationship, drug prescribed by covered entity provider, drug ordered/dispensed by covered entity. Manufacturer penalties for overcharging: refund plus civil penalties. HRSA audit and sanctions for covered entity violations. Orphan drug exclusion for certain hospitals (Pub. L. 115-262, 2018).""",
        key_factors=["covered entity status", "eligible patient definition", "contract pharmacy arrangement", "duplicate discount prevention", "diversion controls"],
        primary_authority=["42 USC 256b", "HRSA OPA Guidance", "Pub. L. 115-262"],
        burden_holder="covered entity",
        adversary_position="HRSA/manufacturer claims diversion or duplicate discount",
        counter_arguments=["patient eligible under HRSA definition", "duplicate discount prevention in place", "no diversion occurred", "contract pharmacy arrangement authorized"],
        resolution_strategy="Implement 340B compliance policies, auditable patient eligibility determination, duplicate discount prevention mechanisms, contract pharmacy agreements",
        entity_scope="340B covered entities, contract pharmacies",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Eligible patient definition is guidance-based, contract pharmacy arrangements face increasing scrutiny",
        controlling_precedent=["42 USC 256b", "HRSA OPA Patient Definition Guidance"],
        category=IssueCategory.DRUG_340B
    ),
    DoctrineBlock(
        topic="FDA Drug Approval - New Drug Application",
        keywords=["fda", "nda", "new drug", "anda", "substantial evidence", "safety and efficacy"],
        conclusion_template=[
            "New drugs require FDA approval via New Drug Application (NDA) demonstrating substantial evidence of safety and efficacy (21 USC 355).",
            "Substantial evidence = adequate and well-controlled clinical investigations.",
            "Generic drugs use Abbreviated New Drug Application (ANDA) showing bioequivalence to reference listed drug."
        ],
        reasoning_framework="""21 USC 355(a) prohibits introduction of new drugs into interstate commerce without FDA approval. NDA process (21 CFR 314): (1) Preclinical testing (animal studies), (2) Investigational New Drug application (IND) for clinical trials (21 CFR 312), (3) Clinical trials Phase I (safety, dose), Phase II (efficacy, side effects), Phase III (large-scale efficacy/safety), (4) NDA submission with full reports of investigations, (5) FDA review (standard 10 months, priority 6 months), (6) Approval or approvable/not approvable letter. Substantial evidence requirement (21 USC 355(d)): evidence consisting of adequate and well-controlled investigations by qualified experts from which it could fairly and responsibly be concluded that the drug will have the effect it is claimed to have. Generic drugs: ANDA (21 USC 355(j)) requires showing bioequivalence to reference listed drug, no need to repeat clinical trials. Bioequivalence = rate and extent of absorption not significantly different. Post-approval requirements: adverse event reporting (21 CFR 314.80), annual reports, changes via supplements. FDA can withdraw approval for safety reasons (21 USC 355(e)).""",
        key_factors=["new drug status", "substantial evidence", "adequate/well-controlled studies", "bioequivalence (generics)", "post-approval compliance"],
        primary_authority=["21 USC 355", "21 CFR 314", "21 CFR 312"],
        burden_holder="drug sponsor",
        adversary_position="FDA claims insufficient evidence of safety/efficacy or noncompliance",
        counter_arguments=["substantial evidence demonstrated", "adequate/well-controlled studies conducted", "bioequivalence shown", "post-approval requirements met"],
        resolution_strategy="Conduct rigorous clinical trials meeting FDA guidance, submit complete NDA/ANDA, maintain post-approval compliance, monitor safety signals",
        entity_scope="drug manufacturers, sponsors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statute and regulations are explicit on substantial evidence requirement, FDA guidance detailed",
        controlling_precedent=["21 USC 355", "21 CFR 314"],
        category=IssueCategory.FDA_COMPLIANCE
    ),
    DoctrineBlock(
        topic="DEA Controlled Substances - Schedule Classification",
        keywords=["dea", "controlled substance", "schedule", "registration", "prescription requirements"],
        conclusion_template=[
            "DEA classifies controlled substances into five schedules based on abuse potential and medical use (21 USC 812).",
            "Schedule I: high abuse potential, no accepted medical use (heroin, LSD, marijuana under federal law).",
            "Schedule II-V: decreasing abuse potential, accepted medical use, varying prescription requirements."
        ],
        reasoning_framework="""21 USC 812 establishes five schedules of controlled substances. Schedule I: (A) high potential for abuse, (B) no currently accepted medical use in treatment in US, (C) lack of accepted safety for use under medical supervision (heroin, LSD, MDMA, marijuana - federal classification). Schedule II: (A) high potential for abuse, (B) currently accepted medical use with severe restrictions, (C) abuse may lead to severe psychological or physical dependence (oxycodone, fentanyl, cocaine, methamphetamine). Schedule III: lower abuse potential than I/II, accepted medical use, moderate/low physical dependence or high psychological dependence (ketamine, anabolic steroids, buprenorphine). Schedule IV: low abuse potential relative to III, accepted medical use, limited dependence (benzodiazepines, tramadol, zolpidem). Schedule V: lowest abuse potential, accepted medical use, limited dependence (cough preparations with codeine). DEA registration required to manufacture, distribute, or dispense (21 USC 823). Prescription requirements: Schedule II requires written prescription (limited exceptions for emergency), no refills; III-V allow oral/written prescriptions and refills with limits (21 CFR 1306). Record-keeping and security requirements (21 CFR 1304, 1301).""",
        key_factors=["schedule classification", "abuse potential", "medical use acceptance", "DEA registration", "prescription compliance"],
        primary_authority=["21 USC 812", "21 USC 823", "21 CFR 1306", "21 CFR 1304"],
        burden_holder="registrant",
        adversary_position="DEA claims improper prescribing, diversion, or recordkeeping violations",
        counter_arguments=["prescription requirements met", "legitimate medical purpose", "DEA registration current", "security/recordkeeping compliant"],
        resolution_strategy="Maintain DEA registration, comply with schedule-specific prescription requirements, implement diversion prevention, secure recordkeeping",
        entity_scope="DEA registrants, prescribers, pharmacies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Schedule classifications and prescription requirements are clearly defined in statute and regulations",
        controlling_precedent=["21 USC 812", "21 CFR 1306"],
        category=IssueCategory.DEA_CONTROLLED
    ),
    DoctrineBlock(
        topic="Telehealth - Interstate Licensure",
        keywords=["telehealth", "telemedicine", "licensure", "interstate compact", "ryan haight act"],
        conclusion_template=[
            "Physicians providing telehealth across state lines must be licensed in the state where the patient is located.",
            "Interstate Medical Licensure Compact expedites multi-state licensure for eligible physicians.",
            "Ryan Haight Act restricts controlled substance prescribing via telemedicine without in-person exam."
        ],
        reasoning_framework="""State medical practice acts generally require licensure in the state where the patient is located during the telehealth encounter. Interstate Medical Licensure Compact (IMLC) allows physicians licensed in member state to obtain expedited licensure in other member states (40 states participating as of 2024). Compact eligibility: primary state of residence medical license, board certification or time-unlimited specialty certification, no disciplinary history, state medical board verification. Ryan Haight Online Pharmacy Consumer Protection Act of 2008 (21 USC 829(e)) requires at least one in-person medical evaluation before controlled substance prescription via internet/telemedicine. Exception: DEA registered telemedicine practitioner in DEA-registered location. COVID-19 public health emergency waivers (expired May 2023) allowed controlled substance prescribing via telehealth without in-person exam - DEA proposed permanent rules. State parity laws may require commercial insurers to reimburse telehealth same as in-person. Medicare telehealth coverage: originating site requirements relaxed post-COVID for mental health, audio-only allowed for certain services (42 CFR 410.78, CMS waivers). HIPAA applies to telehealth - covered entities must use platforms with BAAs.""",
        key_factors=["patient location state licensure", "IMLC participation", "controlled substance prescribing", "in-person exam requirement", "HIPAA compliance"],
        primary_authority=["State Medical Practice Acts", "Interstate Medical Licensure Compact", "21 USC 829(e)", "42 CFR 410.78"],
        burden_holder="telehealth provider",
        adversary_position="State board claims unlicensed practice or DEA claims Ryan Haight violation",
        counter_arguments=["licensed in patient state", "IMLC compact license obtained", "in-person exam conducted", "DEA exemption applies", "HIPAA-compliant platform used"],
        resolution_strategy="Obtain licenses in all states where patients located or use IMLC, comply with Ryan Haight in-person requirements, use HIPAA-compliant platforms with BAAs",
        entity_scope="telehealth providers, telemedicine platforms",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="State licensure requirements vary, Ryan Haight permanent rules pending, COVID waivers expired creating regulatory uncertainty",
        controlling_precedent=["State Medical Practice Acts", "21 USC 829(e)"],
        category=IssueCategory.TELEHEALTH
    ),
    DoctrineBlock(
        topic="Medicaid Managed Care - Network Adequacy",
        keywords=["medicaid", "managed care", "network adequacy", "access to care", "mco"],
        conclusion_template=[
            "Medicaid managed care organizations (MCOs) must maintain networks meeting time/distance standards for provider access (42 CFR 438.68).",
            "Network adequacy requirements ensure enrollees have timely access to covered services.",
            "States set quantitative network standards and MCOs must demonstrate compliance."
        ],
        reasoning_framework="""42 CFR 438.68 requires Medicaid MCOs to maintain networks sufficient to provide adequate access to covered services for all enrollees. Requirements: (1) Network adequacy standards - MCO network must meet state-established quantitative standards for time/distance to providers, (2) Appointment availability - primary care within 30 days, specialist within 60 days for non-urgent, (3) Provider directories - online directory updated monthly with provider locations/specialties/languages, (4) Access to essential community providers (ECPs) - MCO must demonstrate sufficient number/geographic distribution of ECPs serving low-income/medically underserved populations, (5) Out-of-network coverage - if network insufficient, MCO must cover out-of-network at in-network cost, (6) Network adequacy submission - MCO submits network data demonstrating compliance with state standards. State responsibilities: establish time/distance standards by provider type and geography, review MCO network adequacy, approve MCO networks. CMS reviews state standards and MCO submissions. Penalties for noncompliance: state may require MCO to add providers, impose corrective action, or terminate contract.""",
        key_factors=["time/distance standards", "appointment availability", "provider directory accuracy", "ECP participation", "out-of-network coverage"],
        primary_authority=["42 CFR 438.68", "42 CFR 438.206", "42 CFR 438.10(h)"],
        burden_holder="MCO",
        adversary_position="State/CMS claims network inadequate, enrollees lack access",
        counter_arguments=["network meets state standards", "appointment availability demonstrated", "ECP participation sufficient", "out-of-network coverage provided"],
        resolution_strategy="Conduct network adequacy analysis against state standards, recruit providers in underserved areas, monitor appointment availability, maintain accurate directories",
        entity_scope="Medicaid MCOs, states",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulations establish clear network adequacy requirements, state standards vary",
        controlling_precedent=["42 CFR 438.68"],
        category=IssueCategory.MEDICAID_MC
    ),
    DoctrineBlock(
        topic="State Medical Board - Scope of Practice",
        keywords=["scope of practice", "medical board", "licensure", "supervision", "nurse practitioner"],
        conclusion_template=[
            "State medical boards define scope of practice for licensed healthcare professionals.",
            "Practice outside authorized scope can result in licensure discipline, civil liability, and criminal charges.",
            "Advanced practice providers (NPs, PAs) have varying levels of independence by state."
        ],
        reasoning_framework="""State medical practice acts define what activities constitute the practice of medicine and establish licensure requirements. Unauthorized practice: practicing medicine without a license is typically a misdemeanor or felony. Scope of practice violations: licensed professional practicing outside authorized scope may face board discipline (reprimand, probation, suspension, revocation), civil malpractice liability, and criminal charges. Advanced practice providers (nurse practitioners, physician assistants): state laws vary widely on level of required physician supervision. Full practice authority states (28 states for NPs as of 2024): NPs can practice, prescribe, diagnose without physician supervision or collaboration. Reduced practice states: NPs require collaborative agreement or protocol with physician. Restricted practice states: NPs require physician supervision or delegation. Physician assistants: all states require some level of physician supervision/collaboration. Prescription authority: controlled substances require DEA registration plus state authorization, scope varies by state and provider type. Telemedicine may trigger scope questions when provider licensed in State A treats patient in State B - patient location state scope applies.""",
        key_factors=["state licensure", "authorized scope of practice", "supervision requirements", "prescription authority", "cross-state practice"],
        primary_authority=["State Medical Practice Acts", "State Nurse Practice Acts", "State Board Regulations"],
        burden_holder="healthcare provider",
        adversary_position="Medical board claims unauthorized practice or scope violation",
        counter_arguments=["within authorized scope", "supervision requirements met", "appropriate licensure held", "delegated authority documented"],
        resolution_strategy="Understand state-specific scope of practice, maintain required supervision/collaboration agreements, limit practice to authorized scope, obtain cross-state licenses as needed",
        entity_scope="physicians, NPs, PAs, other licensed providers",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Scope of practice laws vary significantly by state, enforcement is fact-intensive",
        controlling_precedent=["State Medical Practice Acts"],
        category=IssueCategory.STATE_MEDICAL
    ),
    DoctrineBlock(
        topic="HIPAA Breach Notification",
        keywords=["breach", "notification", "unsecured phi", "harm threshold", "business associate"],
        conclusion_template=[
            "Breach of unsecured PHI triggers notification obligations to individuals, HHS, and media (45 CFR 164.400-414).",
            "Breach = impermissible acquisition, access, use, or disclosure of PHI that compromises security or privacy.",
            "Notification timelines: individuals within 60 days, HHS concurrent or annually, media if 500+ affected in jurisdiction."
        ],
        reasoning_framework="""45 CFR 164.402 defines breach as impermissible acquisition, access, use, or disclosure of PHI that compromises the security or privacy of the PHI. Exceptions: (1) unintentional acquisition/access by workforce member acting under authority, (2) inadvertent disclosure from authorized person to another authorized person at same covered entity/business associate, (3) disclosure where covered entity/BA has good faith belief recipient could not reasonably retain the information. Unsecured PHI = PHI not secured through encryption or destruction per NIST guidance. If unsecured PHI breach, covered entity must conduct risk assessment of probability of compromise considering (1) nature/extent of PHI, (2) unauthorized person who used/received PHI, (3) whether actually acquired/viewed, (4) extent of mitigation. If low probability of compromise not demonstrated, breach presumed. Notification requirements: (1) Individuals - written notice within 60 days by first-class mail or email if authorized, (2) HHS - if 500+ affected, notify HHS concurrent with individuals; if <500, notify HHS annually, (3) Media - if 500+ in a state/jurisdiction, notify prominent media outlets. Business associate breach: BA notifies covered entity within 60 days, covered entity does notifications. Penalties: civil penalties up to $1.5M per violation category per year.""",
        key_factors=["unsecured PHI", "impermissible use/disclosure", "probability of compromise", "notification timeliness", "business associate obligations"],
        primary_authority=["45 CFR 164.400-414", "45 CFR 164.402", "NIST SP 800-66r1"],
        burden_holder="covered entity",
        adversary_position="OCR claims breach occurred and notification inadequate or untimely",
        counter_arguments=["PHI was encrypted", "low probability of compromise shown", "exception applies", "notification timely", "BA notified CE promptly"],
        resolution_strategy="Encrypt PHI at rest and in transit, conduct breach risk assessments, notify within 60 days if breach, implement breach response plan",
        entity_scope="covered entities, business associates",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulation provides explicit breach definition and risk assessment factors, OCR guidance available",
        controlling_precedent=["45 CFR 164.402", "OCR Breach Notification Rule Guidance"],
        category=IssueCategory.HIPAA_PRIVACY
    ),
    DoctrineBlock(
        topic="Medicare Part D - Medication Therapy Management",
        keywords=["part d", "mtm", "medication therapy management", "targeted beneficiary", "comprehensive medication review"],
        conclusion_template=[
            "Medicare Part D plans must offer medication therapy management (MTM) programs to targeted beneficiaries (42 CFR 423.153(d)).",
            "Targeting criteria: multiple chronic conditions, multiple Part D drugs, likely to incur high costs.",
            "MTM services include comprehensive medication review and targeted medication reviews."
        ],
        reasoning_framework="""42 CFR 423.153(d) requires Part D sponsors to establish MTM programs for targeted beneficiaries. Targeting criteria (minimum): (1) multiple chronic diseases (at least 3 from CMS core set: diabetes, COPD, CHF, dyslipidemia, hypertension, chronic pain, Alzheimer's, etc.), (2) multiple Part D drugs (at least 8), (3) likely annual Part D drug costs exceeding threshold ($5,272 in 2024). Sponsors may use broader criteria to expand enrollment. MTM services: (1) Comprehensive medication review (CMR) - interactive person-to-person or telehealth review of all medications by pharmacist or other qualified provider, at least annually, results in written summary of medication action plan and personal medication list. (2) Targeted medication reviews (TMRs) - focused reviews addressing specific medications or therapeutic classes, at least quarterly. (3) Interventions for medication problems. Beneficiary opt-out allowed. MTM program required elements: comprehensive review, action plan, documentation, follow-up. Standardized format for CMR outputs. CMS oversight includes annual MTM program submissions and performance metrics.""",
        key_factors=["targeted beneficiary criteria", "CMR completion", "medication action plan", "beneficiary enrollment/opt-out", "standardized format"],
        primary_authority=["42 CFR 423.153(d)", "CMS MTM Guidance"],
        burden_holder="Part D sponsor",
        adversary_position="CMS claims MTM program inadequate or enrollment criteria too restrictive",
        counter_arguments=["minimum targeting criteria met", "CMR completion rates documented", "action plans provided", "standardized format used", "expanded criteria beyond minimum"],
        resolution_strategy="Implement MTM program meeting regulatory criteria, document CMR completion, use standardized formats, track beneficiary enrollment and outcomes",
        entity_scope="Part D sponsors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulations provide explicit MTM program requirements, CMS issues detailed annual guidance",
        controlling_precedent=["42 CFR 423.153(d)", "CMS MTM Program Guidance"],
        category=IssueCategory.MEDICARE_COP
    ),
    DoctrineBlock(
        topic="Clinical Laboratory Improvement Amendments (CLIA)",
        keywords=["clia", "laboratory", "waived", "moderate complexity", "high complexity", "certificate"],
        conclusion_template=[
            "Clinical laboratories must obtain CLIA certification based on test complexity (42 USC 263a, 42 CFR 493).",
            "Waived tests: simple, low-risk, certificate of waiver required.",
            "Moderate/high complexity: personnel, quality control, proficiency testing, inspections required."
        ],
        reasoning_framework="""42 USC 263a (CLIA) requires all clinical laboratories to be certified by HHS. Test categorization: (1) Waived - simple tests with low error risk (pregnancy, glucose, dipstick urinalysis, etc.), certificate of waiver required ($150 biennially), minimal QC. (2) Moderate complexity - more complex tests requiring technical skill, certificate of compliance or accreditation required, personnel standards, QC, proficiency testing (PT), biennial inspections. (3) High complexity - most complex tests, same requirements as moderate plus higher personnel qualifications. FDA categorizes tests by complexity using 7 criteria (knowledge, training, reagent prep, equipment, interpretation, troubleshooting, test system). CLIA certificate types: waiver, provider-performed microscopy (PPM), compliance, accreditation (deemed if Joint Commission/CAP/other), registration (pending inspection). Personnel requirements (42 CFR 493.1400s): lab director, technical consultant, clinical consultant, testing personnel with specified education/training. Quality control: verify test accuracy/reliability daily (42 CFR 493.1200s). Proficiency testing: moderate/high complexity labs must enroll and score 80%+ on PT (42 CFR 493.800s). Sanctions: suspension, limitation, revocation of certificate, civil penalties up to $10K per violation, criminal penalties.""",
        key_factors=["test complexity", "CLIA certificate type", "personnel qualifications", "QC/PT compliance", "inspection findings"],
        primary_authority=["42 USC 263a", "42 CFR 493", "FDA CLIA Categorization"],
        burden_holder="laboratory",
        adversary_position="CMS/state claims CLIA violations - inadequate personnel, QC failures, PT failures",
        counter_arguments=["certificate appropriate for tests performed", "personnel meet qualifications", "QC documented", "PT scores >80%", "corrective action implemented"],
        resolution_strategy="Obtain appropriate CLIA certificate, hire qualified personnel, implement QC/PT programs, prepare for inspections, maintain documentation",
        entity_scope="clinical laboratories",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CLIA requirements are detailed in statute and regulations, CMS provides extensive guidance",
        controlling_precedent=["42 USC 263a", "42 CFR 493"],
        category=IssueCategory.FDA_COMPLIANCE
    ),
    DoctrineBlock(
        topic="FDA Medical Device Classification",
        keywords=["medical device", "class I", "class II", "class III", "510k", "pma", "substantial equivalence"],
        conclusion_template=[
            "FDA classifies medical devices into Class I (low risk), Class II (moderate risk), Class III (high risk) (21 USC 360c).",
            "Class II devices typically require 510(k) premarket notification demonstrating substantial equivalence to predicate device.",
            "Class III devices require premarket approval (PMA) with clinical trials demonstrating safety and effectiveness."
        ],
        reasoning_framework="""21 USC 360c establishes three medical device classes based on risk. Class I (low risk): general controls (registration, listing, good manufacturing practices) sufficient, most exempt from premarket notification (tongue depressors, elastic bandages). Class II (moderate risk): general controls insufficient, special controls needed (performance standards, postmarket surveillance, guidance), requires 510(k) premarket notification unless exempt (infusion pumps, surgical drapes, blood pressure cuffs). Class III (high risk): supports/sustains life, prevents impairment, presents unreasonable illness/injury risk, requires PMA with clinical data (heart valves, implanted pacemakers, breast implants). 510(k) process (21 CFR 807 subpart E): manufacturer submits 510(k) demonstrating substantial equivalence to legally marketed predicate device, FDA reviews within 90 days, clearance if substantially equivalent. Substantial equivalence = same intended use and either same technological characteristics or different characteristics that do not raise new safety/effectiveness questions. PMA process (21 CFR 814): manufacturer submits PMA with valid scientific evidence (usually clinical trials) demonstrating reasonable assurance of safety and effectiveness, FDA review 180 days, approval panel review/inspection. De novo classification for novel low/moderate risk devices with no predicate (21 USC 360c(f)(2)).""",
        key_factors=["device classification", "510(k) substantial equivalence", "PMA clinical evidence", "predicate device", "intended use"],
        primary_authority=["21 USC 360c", "21 CFR 807", "21 CFR 814"],
        burden_holder="device manufacturer",
        adversary_position="FDA claims device not substantially equivalent or PMA insufficient",
        counter_arguments=["substantial equivalence demonstrated", "predicate device appropriate", "clinical data supports safety/effectiveness", "special controls met"],
        resolution_strategy="Determine device classification, identify appropriate predicate for 510(k), conduct clinical trials for PMA, submit complete premarket submissions",
        entity_scope="medical device manufacturers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Classification and premarket pathways are well-defined in statute and regulations, FDA guidance extensive",
        controlling_precedent=["21 USC 360c", "21 CFR 807", "21 CFR 814"],
        category=IssueCategory.FDA_COMPLIANCE
    ),
    DoctrineBlock(
        topic="HIPAA Business Associate Agreements",
        keywords=["business associate", "baa", "subcontractor", "phi", "breach notification"],
        conclusion_template=[
            "Covered entities must have written business associate agreements (BAAs) with entities that create, receive, maintain, or transmit PHI on their behalf (45 CFR 164.502(e), 164.504(e)).",
            "BAAs must include required elements: permitted uses, safeguard obligations, breach reporting, subcontractor flow-down.",
            "Business associates have direct HIPAA liability for violations."
        ],
        reasoning_framework="""45 CFR 164.502(e) prohibits covered entities from disclosing PHI to business associates without written contract or other arrangement. Business associate (45 CFR 160.103) = person/entity that performs functions/activities involving PHI on behalf of covered entity (claims processing, data analysis, utilization review, billing, legal, actuarial, accounting, consulting, accreditation, management, administrative, financial services). Not BA: workforce members, healthcare providers in treatment capacity, plan sponsors, members of covered entity organized healthcare arrangement. BAA required elements (45 CFR 164.504(e)): (1) Permitted uses/disclosures of PHI, (2) BA will not use/disclose except as permitted or required by law, (3) BA will use appropriate safeguards, (4) BA will report breaches/security incidents, (5) BA will ensure subcontractors comply (flow-down), (6) BA will make PHI available to individuals, (7) BA will make PHI available for amendments, (8) BA will make PHI available for accounting of disclosures, (9) BA will make internal practices/books/records available to HHS, (10) BA will return/destroy PHI at termination if feasible, (11) Authorization for covered entity to terminate if BA materially breaches. Business associates have direct HIPAA compliance obligations - Privacy Rule 45 CFR 164.500s, Security Rule 45 CFR 164.308-318, Breach Notification Rule 45 CFR 164.400s. Subcontractors are also business associates requiring BAAs.""",
        key_factors=["business associate relationship", "BAA execution", "required BAA elements", "subcontractor flow-down", "breach reporting"],
        primary_authority=["45 CFR 164.502(e)", "45 CFR 164.504(e)", "45 CFR 160.103"],
        burden_holder="covered entity and business associate",
        adversary_position="OCR claims no BAA or BAA lacks required elements",
        counter_arguments=["BAA executed", "all required elements included", "subcontractor BAAs in place", "breach reporting timely"],
        resolution_strategy="Execute BAAs before PHI disclosure, use HHS model BAA or ensure all required elements included, obtain BAAs from subcontractors, monitor BA compliance",
        entity_scope="covered entities, business associates, subcontractors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="BAA requirements explicitly detailed in regulations, HHS provides model BAA",
        controlling_precedent=["45 CFR 164.504(e)"],
        category=IssueCategory.HIPAA_PRIVACY
    ),
    DoctrineBlock(
        topic="Medicare Physician Fee Schedule - Physician Self-Referral",
        keywords=["physician fee schedule", "incident-to", "supervision", "billing", "stark"],
        conclusion_template=[
            "Medicare Physician Fee Schedule governs payment for physician services (42 CFR 414).",
            "Incident-to billing allows NPP services to be billed under physician NPI if supervision and other requirements met.",
            "Improper billing can trigger FCA liability and Stark Law violations."
        ],
        reasoning_framework="""42 CFR 414 establishes Medicare Physician Fee Schedule (MPFS) for payment of physician services. Incident-to services (42 CFR 410.26): services/supplies furnished incident to physician's professional services may be billed under physician NPI at 100% MPFS rate. Requirements: (1) integral part of physician's service in course of diagnosis/treatment, (2) commonly furnished in physician offices, (3) direct personal supervision of physician (physician in office suite and immediately available), (4) initiated by physician with established plan of care, (5) furnished by employee or contractor of physician/group. Non-physician practitioners (NPPs - NPs, PAs, CNSs) can bill under own NPI at 85% MPFS rate without supervision. Incident-to billing at 100% requires direct supervision - physician must see new patients and patients with new problems, NPP can provide follow-up under physician supervision. Teaching physician rules (42 CFR 415.172): teaching physician must be present during key portion of service, document participation. Split/shared E/M services (CY2022 rule): physician and NPP both provide substantive portion, bill under whoever provides >50% time or medical decision-making. Stark implications: if physician refers to entity and bills incident-to, Stark financial relationship exists unless exception met. False Claims Act: billing incident-to without proper supervision is false claim.""",
        key_factors=["incident-to requirements", "direct supervision", "established plan of care", "new vs established patient", "split/shared services"],
        primary_authority=["42 CFR 410.26", "42 CFR 414", "42 CFR 415.172", "CMS MPFS Final Rules"],
        burden_holder="billing provider",
        adversary_position="Medicare contractor claims improper incident-to billing, overpayment",
        counter_arguments=["direct supervision documented", "established plan of care", "services integral to physician service", "split/shared rules met"],
        resolution_strategy="Implement incident-to billing policies, ensure direct supervision for incident-to, document physician involvement, train staff on billing rules",
        entity_scope="physicians, NPPs, group practices",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Incident-to requirements are detailed but supervision enforcement varies, split/shared rules are new (2022)",
        controlling_precedent=["42 CFR 410.26", "CMS MPFS Incident-to Guidance"],
        category=IssueCategory.MEDICARE_COP
    ),
    DoctrineBlock(
        topic="State Certificate of Need Laws",
        keywords=["certificate of need", "con", "facility", "capital expenditure", "service expansion"],
        conclusion_template=[
            "35 states require Certificate of Need (CON) approval before healthcare facilities can expand, add services, or make major capital expenditures.",
            "CON laws aim to control healthcare costs and ensure adequate access by preventing unnecessary duplication.",
            "Violations can result in fines, facility closure, and inability to receive Medicare/Medicaid reimbursement."
        ],
        reasoning_framework="""State CON laws (varying by state) require healthcare facilities to obtain state approval before (1) constructing new facilities, (2) expanding bed capacity, (3) acquiring major medical equipment (thresholds e.g. $750K-$2M), (4) offering new services (e.g. cardiac surgery, neonatal ICU, transplant). CON process: applicant submits application demonstrating need based on state criteria (population projections, utilization data, access gaps, cost-effectiveness), state agency reviews against state health plan, public comment period, competitors may intervene, agency issues decision (approval, denial, approval with conditions), appeal rights. Need criteria vary by state but typically include: (1) public need exists, (2) project consistent with state health plan, (3) project financially feasible, (4) project will improve access for underserved, (5) less costly/intrusive alternatives not available. Penalties for operating without CON: civil penalties ($100-$500 per day in some states), injunction to cease operations, inability to obtain Medicare/Medicaid provider agreements, exclusion from state health plans, voiding of contracts. Federal CON history: National Health Planning and Resources Development Act 1974 encouraged states to adopt CON, federal mandate repealed 1987, states continued CON voluntarily. Criticism: CON laws may restrict competition and innovation. Trend: some states repealing CON laws.""",
        key_factors=["state CON requirements", "threshold amounts", "need demonstration", "state health plan consistency", "competitor intervention"],
        primary_authority=["State CON Statutes", "State Health Planning Agency Regulations"],
        burden_holder="applicant",
        adversary_position="State agency or competitor claims need not demonstrated or plan inconsistent",
        counter_arguments=["public need exists", "state health plan supports", "financially feasible", "underserved access improved", "no less costly alternative"],
        resolution_strategy="Conduct needs assessment, engage consultants for CON application, demonstrate state health plan alignment, prepare for competitor challenges, consider CON-exempt alternatives",
        entity_scope="healthcare facilities, developers",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="CON criteria are state-specific and often subjective, competitor challenges common, enforcement varies",
        controlling_precedent=["State CON Statutes"],
        category=IssueCategory.STATE_MEDICAL
    ),
    DoctrineBlock(
        topic="FDA Dietary Supplement Regulation",
        keywords=["dietary supplement", "dshea", "structure function", "disease claim", "new dietary ingredient"],
        conclusion_template=[
            "Dietary supplements are regulated under Dietary Supplement Health and Education Act (DSHEA) (21 USC 321(ff), 350b).",
            "Manufacturers can make structure/function claims without FDA approval, but cannot make disease claims.",
            "New dietary ingredients (NDIs) require premarket notification to FDA demonstrating safety."
        ],
        reasoning_framework="""21 USC 321(ff) defines dietary supplement as product intended to supplement diet containing dietary ingredients (vitamins, minerals, herbs, amino acids, etc.), intended for ingestion, labeled as dietary supplement. DSHEA framework: (1) Dietary supplements are foods, not drugs, (2) Manufacturers responsible for safety, no FDA premarket approval required (unlike drugs), (3) Structure/function claims allowed without FDA approval if substantiated and disclaim FDA evaluation, (4) Disease claims not allowed without drug approval process. Structure/function claims (21 USC 343(r)(6)): describe role of nutrient/ingredient in affecting structure/function of body (e.g. calcium builds strong bones), must have substantiation, must include disclaimer this statement has not been evaluated by FDA, product is not intended to diagnose/treat/cure/prevent any disease, must notify FDA within 30 days of marketing. Disease claims: claim to diagnose, treat, cure, mitigate, or prevent disease requires drug approval. New dietary ingredient (NDI) (21 USC 350b): ingredient not marketed in US before Oct 15, 1994 requires premarket notification to FDA at least 75 days before marketing, must include evidence of safety. cGMP requirements (21 CFR 111): manufacturers must establish quality control, test ingredients/finished products. Adverse event reporting (21 USC 379aa-1): manufacturers must report serious adverse events to FDA within 15 days.""",
        key_factors=["structure/function vs disease claim", "NDI notification", "substantiation", "cGMP compliance", "adverse event reporting"],
        primary_authority=["21 USC 321(ff)", "21 USC 350b", "21 USC 343(r)(6)", "21 CFR 111"],
        burden_holder="manufacturer",
        adversary_position="FDA claims unauthorized disease claim, NDI not notified, or safety issue",
        counter_arguments=["structure/function claim only", "claim substantiated", "NDI notification submitted", "cGMP compliant", "no safety signals"],
        resolution_strategy="Avoid disease claims, substantiate structure/function claims, submit NDI notifications for new ingredients, implement cGMP, monitor adverse events",
        entity_scope="dietary supplement manufacturers",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Line between structure/function and disease claims is often unclear, FDA enforcement discretion high",
        controlling_precedent=["21 USC 343(r)(6)", "FDA DSHEA Guidance"],
        category=IssueCategory.FDA_COMPLIANCE
    ),
    DoctrineBlock(
        topic="Medicare Advantage Risk Adjustment",
        keywords=["medicare advantage", "risk adjustment", "hcc", "hierarchical condition category", "risk score"],
        conclusion_template=[
            "Medicare Advantage (MA) plans receive risk-adjusted capitation payments based on enrollee health status (42 CFR 422.308).",
            "Hierarchical Condition Categories (HCCs) from diagnosis codes determine risk scores and payment.",
            "Improper coding (upcoding, unsupported diagnoses) can trigger FCA liability and CMS audits."
        ],
        reasoning_framework="""42 CFR 422.308 establishes risk adjustment for MA payments. CMS pays MA plans monthly capitation based on enrollee risk scores. Risk score calculation: diagnosis codes from enrollee medical records map to Hierarchical Condition Categories (HCCs), HCCs have assigned weights, total weights plus demographic factors = risk score, risk score x benchmark rate = payment. HCC requirements: (1) diagnosis must be documented in medical record during payment year, (2) diagnosis must be from face-to-face encounter with physician/NPP, (3) diagnosis must be coded to highest specificity, (4) chronic conditions require annual documentation, (5) diagnosis must be supported by clinical evidence. MA plan responsibilities: submit enrollee diagnosis data via Risk Adjustment Processing System (RAPS) or Encounter Data System (EDS), ensure accurate coding, conduct coding reviews. CMS oversight: Risk Adjustment Data Validation (RADV) audits - CMS samples enrollees, requests medical records, validates HCCs, extrapolates payment error across plan, recovers overpayments. FCA risk: submitting unsupported HCCs is false claim (US ex rel. Poehling v. UnitedHealth Group, settlement $32.5M). OIG concern: MA plans incentivizing providers to code more HCCs, health risk assessments to identify HCCs.""",
        key_factors=["diagnosis documentation", "face-to-face encounter", "coding specificity", "annual recapture", "RADV audit"],
        primary_authority=["42 CFR 422.308", "CMS-HCC Risk Adjustment Model", "RADV Audit Methodology"],
        burden_holder="MA plan",
        adversary_position="CMS claims unsupported HCCs in RADV audit, FCA relator claims upcoding",
        counter_arguments=["diagnosis supported by medical record", "face-to-face encounter documented", "coding to highest specificity", "provider documentation standards met"],
        resolution_strategy="Implement coding compliance program, train providers on documentation, conduct internal RADV audits, avoid HCC-focused incentives, repay identified overpayments",
        entity_scope="Medicare Advantage plans",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="RADV audit extrapolation methodology under litigation, documentation standards are evolving, FCA enforcement active",
        controlling_precedent=["42 CFR 422.308", "CMS RADV Audit Guidance"],
        category=IssueCategory.MEDICARE_COP
    ),
    DoctrineBlock(
        topic="HIPAA Right of Access",
        keywords=["right of access", "designated record set", "timely", "fee", "electronic format"],
        conclusion_template=[
            "Individuals have right to access their protected health information in designated record sets (45 CFR 164.524).",
            "Covered entities must provide access within 30 days (extendable 30 days once).",
            "Fees limited to reasonable cost-based charges; must provide in requested electronic format if readily producible."
        ],
        reasoning_framework="""45 CFR 164.524 grants individuals right to inspect and obtain copies of PHI in designated record sets. Designated record set = medical/billing records used to make decisions about individual, enrollment/payment/claims records maintained by health plan. Scope: individual may access all PHI in designated record set except (1) psychotherapy notes, (2) information compiled for legal proceeding, (3) PHI subject to CLIA, (4) inmates in certain circumstances, (5) research records during trial if individual agreed to suspension, (6) Privacy Act restricted information. Timeliness: covered entity must act on request within 30 days, may extend one time for 30 days with written notice to individual. Form: individual may request copies, inspection, or direct transmission to designated person/entity. Electronic format: if PHI maintained electronically, must provide in electronic format requested if readily producible, otherwise in readable electronic form as agreed. Fees: may charge reasonable cost-based fee limited to cost of copying (labor + supplies), postage if mailed, preparing summary if agreed. OCR guidance: no retrieval fees, no per-page fees if transmitted electronically, fees should not be prohibitive. Denial: if access denied (limited grounds), must provide written denial with reason, review rights (if applicable), complaint process. OCR enforcement priority: right of access violations result in significant penalties.""",
        key_factors=["designated record set", "30-day timeline", "electronic format requested", "reasonable cost-based fee", "denial grounds"],
        primary_authority=["45 CFR 164.524", "OCR Right of Access Guidance 2016, 2020"],
        burden_holder="covered entity",
        adversary_position="OCR/individual claims access denied or unreasonable fees charged",
        counter_arguments=["access provided timely", "fee reasonable and cost-based", "electronic format provided", "denial justified under exception"],
        resolution_strategy="Establish access request procedures, respond within 30 days, charge only cost-based fees, provide electronic format when requested, train staff on access rights",
        entity_scope="covered entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Right of access requirements detailed in regulation, OCR provides extensive guidance and actively enforces",
        controlling_precedent=["45 CFR 164.524", "OCR Right of Access Initiative"],
        category=IssueCategory.HIPAA_PRIVACY
    ),
    DoctrineBlock(
        topic="FDA Accelerated Approval Pathway",
        keywords=["accelerated approval", "surrogate endpoint", "confirmatory trial", "serious condition", "unmet need"],
        conclusion_template=[
            "FDA may grant accelerated approval for drugs treating serious conditions with unmet need based on surrogate endpoints (21 CFR 314.500, 21 USC 356(c)).",
            "Sponsor must conduct confirmatory trials to verify clinical benefit.",
            "FDA can withdraw accelerated approval if confirmatory trial fails or sponsor does not conduct trial with due diligence."
        ],
        reasoning_framework="""21 USC 356(c) and 21 CFR 314.500 establish accelerated approval pathway. Eligibility: (1) drug treats serious/life-threatening condition, (2) provides meaningful advantage over available therapies (unmet need), (3) demonstrates effect on surrogate endpoint or intermediate clinical endpoint reasonably likely to predict clinical benefit. Surrogate endpoint = marker (lab measurement, radiographic image, physical sign) used as substitute for clinical endpoint, reasonably likely to predict clinical benefit. Process: sponsor submits NDA with data on surrogate endpoint, FDA reviews and may grant accelerated approval with post-approval requirements. Post-approval requirements: sponsor must conduct confirmatory trials (usually already underway at approval) to verify and describe clinical benefit, submit progress reports. Withdrawal: FDA may withdraw approval using expedited procedures if (1) confirmatory trial fails to verify clinical benefit, (2) other evidence shows drug not safe/effective, (3) sponsor fails to conduct confirmatory trial with due diligence, (4) promotional materials false/misleading. Recent reforms (FDORA 2022): FDA must explain why confirmatory trial not completed, may require interim milestones, public transparency on overdue confirmatory trials. Examples: cancer drugs based on tumor response rate, HIV drugs based on CD4 count.""",
        key_factors=["serious condition", "unmet need", "surrogate endpoint validity", "confirmatory trial design", "due diligence in conducting trial"],
        primary_authority=["21 USC 356(c)", "21 CFR 314.500", "FDORA 2022"],
        burden_holder="sponsor",
        adversary_position="FDA claims confirmatory trial failed or not conducted with due diligence",
        counter_arguments=["confirmatory trial verified benefit", "trial conducted diligently", "surrogate endpoint reasonably predicted benefit", "interim milestones met"],
        resolution_strategy="Design robust confirmatory trials before accelerated approval, enroll trials rapidly, meet interim milestones, prepare for potential withdrawal if trial fails",
        entity_scope="drug sponsors",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Surrogate endpoint validity can be uncertain, confirmatory trials may fail, FDA withdrawal authority enhanced by recent reforms",
        controlling_precedent=["21 USC 356(c)", "21 CFR 314.500"],
        category=IssueCategory.FDA_COMPLIANCE
    )
]

# ==================== METRICS & TELEMETRY ====================
@dataclass
class QueryMetrics:
    total_queries: int = 0
    fast_mode: int = 0
    defense_mode: int = 0
    memo_mode: int = 0
    avg_latency_ms: float = 0.0
    doctrine_hit_rate: float = 0.0
    error_count: int = 0

    def record_query(self, mode: ResponseMode, latency_ms: int, hit: bool):
        self.total_queries += 1
        if mode == ResponseMode.FAST:
            self.fast_mode += 1
        elif mode == ResponseMode.DEFENSE:
            self.defense_mode += 1
        else:
            self.memo_mode += 1

        self.avg_latency_ms = (self.avg_latency_ms * (self.total_queries - 1) + latency_ms) / self.total_queries
        if hit:
            hit_count = int(self.doctrine_hit_rate * (self.total_queries - 1)) + 1
            self.doctrine_hit_rate = hit_count / self.total_queries
        else:
            hit_count = int(self.doctrine_hit_rate * (self.total_queries - 1))
            self.doctrine_hit_rate = hit_count / self.total_queries

METRICS = QueryMetrics()
AUDIT_LOG = Path(__file__).parent / "audit_trail.jsonl"
TRIGGERED_DOCTRINES: Set[str] = set()
MISSED_QUERIES: List[str] = []

# ==================== CORE INTELLIGENCE ====================
def search_doctrines(query: str, top_k: int = 5) -> List[DoctrineBlock]:
    query_lower = query.lower()
    scored = []
    for doctrine in DOCTRINE_CACHE:
        score = sum(1 for kw in doctrine.keywords if kw in query_lower)
        if score > 0:
            scored.append((score, doctrine))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [d for _, d in scored[:top_k]]

def three_layer_response(query: str, mode: ResponseMode, zone: Zone) -> Dict[str, Any]:
    start = time.time()

    # Layer 1: Doctrine Cache (0-200ms)
    doctrines = search_doctrines(query, top_k=3)
    hit = len(doctrines) > 0

    if hit:
        primary = doctrines[0]
        TRIGGERED_DOCTRINES.add(primary.topic)

        if mode == ResponseMode.FAST:
            response = primary.conclusion_template[0]
        elif mode == ResponseMode.DEFENSE:
            response = f"{primary.conclusion_template[0]} {primary.reasoning_framework[:300]}... Authority: {', '.join(primary.primary_authority[:3])}. Confidence: {primary.confidence.value}."
        else:  # MEMO
            response = f"MEMORANDUM\n\nRE: {primary.topic}\n\n"
            response += "CONCLUSION:\n" + "\n".join(primary.conclusion_template) + "\n\n"
            response += f"REASONING:\n{primary.reasoning_framework}\n\n"
            response += f"KEY FACTORS:\n" + "\n".join(f"- {f}" for f in primary.key_factors) + "\n\n"
            response += f"AUTHORITY:\n" + "\n".join(f"- {a}" for a in primary.primary_authority) + "\n\n"
            response += f"CONFIDENCE: {primary.confidence_stratification}"

        sources = primary.primary_authority
        confidence = primary.confidence
    else:
        MISSED_QUERIES.append(query)
        response = "No direct healthcare regulatory doctrine matched. Recommend legal counsel review for HIPAA, Stark, AKS, FDA, DEA, or state-specific requirements."
        sources = ["General Healthcare Regulatory Compliance"]
        confidence = ConfidenceLevel.DISCLOSURE

    latency_ms = int((time.time() - start) * 1000)
    METRICS.record_query(mode, latency_ms, hit)

    # Determinism hash
    hash_input = f"{query}|{mode.value}|{zone.value}|{response}"
    determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    # Audit trail
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "mode": mode.value,
        "zone": zone.value,
        "hit": hit,
        "triggered_doctrines": [d.topic for d in doctrines],
        "latency_ms": latency_ms,
        "confidence": confidence.value,
        "determinism_hash": determinism_hash
    }
    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(audit_entry) + "\n")

    return {
        "response": response,
        "confidence": confidence,
        "triggered_doctrines": [d.topic for d in doctrines],
        "latency_ms": latency_ms,
        "determinism_hash": determinism_hash,
        "sources": sources
    }

# ==================== FASTAPI APP ====================
APP = FastAPI(title="REG08 Healthcare Regulatory Engine", version="1.0.0")

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@APP.on_event("startup")
async def startup():
    logger.info("REG08 Healthcare Regulatory Engine v1.0.0 starting on port 9128")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} healthcare regulatory doctrine blocks")

@APP.get("/health")
async def health():
    return {
        "status": "healthy",
        "engine": "REG08_healthcare_regulatory",
        "version": "1.0.0",
        "port": 9128,
        "doctrines": len(DOCTRINE_CACHE),
        "categories": len(IssueCategory),
        "metrics": asdict(METRICS),
        "triggered_doctrines": len(TRIGGERED_DOCTRINES),
        "missed_queries": len(MISSED_QUERIES)
    }

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    try:
        result = three_layer_response(req.query, req.mode, req.zone)
        return QueryResponse(
            response=result["response"],
            mode=req.mode,
            zone=req.zone,
            confidence=result["confidence"],
            triggered_doctrines=result["triggered_doctrines"],
            latency_ms=result["latency_ms"],
            determinism_hash=result["determinism_hash"],
            sources=result["sources"]
        )
    except Exception as e:
        METRICS.error_count += 1
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "categories": {cat.value: sum(1 for d in DOCTRINE_CACHE if d.category == cat) for cat in IssueCategory},
        "doctrines": [{"topic": d.topic, "category": d.category.value, "keywords": d.keywords} for d in DOCTRINE_CACHE]
    }

@APP.get("/metrics")
async def get_metrics():
    return {
        "metrics": asdict(METRICS),
        "triggered_doctrines": list(TRIGGERED_DOCTRINES),
        "missed_queries": MISSED_QUERIES[-20:],
        "coverage": {
            "hit_rate": METRICS.doctrine_hit_rate,
            "total_queries": METRICS.total_queries
        }
    }

if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=9128)
