"""
REG10 Data Privacy Regulatory Engine v1.0.0
Handles CCPA/CPRA, GDPR, state privacy laws, COPPA, FERPA, GLBA, FTC enforcement
Port 9130 | TIE-Grade | 25+ Real Doctrine Blocks
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

ENGINE_ID = "REG10"
ENGINE_NAME = "Data Privacy Regulatory Engine"
VERSION = "1.0.0"
PORT = 9130

logger.add(f"REG10_privacy_{datetime.now():%Y%m%d}.log", rotation="100 MB", retention="30 days", level="INFO")


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
    CCPA_CPRA = "CCPA_CPRA"
    GDPR = "GDPR"
    STATE_PRIVACY = "STATE_PRIVACY"
    COPPA = "COPPA"
    FERPA = "FERPA"
    GLBA = "GLBA"
    FTC_ENFORCEMENT = "FTC_ENFORCEMENT"
    BREACH_NOTIFICATION = "BREACH_NOTIFICATION"
    CROSS_BORDER = "CROSS_BORDER"
    CONSENT_MANAGEMENT = "CONSENT_MANAGEMENT"
    DPO_REQUIREMENTS = "DPO_REQUIREMENTS"
    DPIA = "DPIA"


class DoctrineBlock(BaseModel):
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
    controlling_precedent: Optional[str] = None


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    engine: str
    version: str
    query: str
    response: str
    mode: str
    confidence: str
    doctrines_triggered: List[str]
    latency_ms: float
    determinism_hash: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float


START_TIME = time.time()
AUDIT_LOG = []


DOCTRINES = [
    DoctrineBlock(
        topic="CCPA Consumer Rights - Access, Deletion, Portability",
        keywords=["ccpa", "consumer request", "data access", "right to delete", "portability", "cal civ code 1798.100"],
        conclusion_template=[
            "Under CCPA Cal. Civ. Code Section 1798.100-110, consumers have verifiable rights to request disclosure of personal information categories and specific pieces collected, sources, business purposes, and third parties with whom shared.",
            "Section 1798.105 grants deletion rights subject to enumerated exceptions (transaction completion, security, legal compliance, internal lawful uses).",
            "Businesses must respond within 45 days (extendable 45 more with notice), provide information free of charge twice per 12-month period."
        ],
        reasoning_framework="""CCPA applies if business meets any threshold: (1) $25M+ annual gross revenue, (2) buys/sells PI of 100K+ CA consumers/households/devices annually, or (3) derives 50%+ revenue from selling/sharing PI. Consumer has right to know categories and specific pieces of PI collected (1798.100), sources (1798.110(c)(1)), business/commercial purposes (1798.110(c)(2)), categories of third parties with whom shared (1798.110(c)(3)). Business must provide this information within 45 days of verifiable request, extendable another 45 days with consumer notice. Information must be delivered by mail or electronically at consumer's option, in portable and readily usable format. Consumer may make such request twice in 12-month period free of charge; business may charge reasonable fee for additional requests. Deletion right under 1798.105 allows consumer to request deletion of PI collected from consumer, subject to exceptions: (1) complete transaction for which PI collected, (2) detect security incidents, (3) debug to identify/repair errors, (4) exercise free speech or ensure another consumer's exercise of free speech, (5) comply with California Electronic Communications Privacy Act (Cal. Penal Code 1546 seq.), (6) engage in public/peer-reviewed scientific, historical, or statistical research in public interest adhering to other privacy laws, (7) enable solely internal uses reasonably aligned with consumer expectations, (8) comply with legal obligation, (9) make other internal and lawful uses of information compatible with context in which consumer provided it. Business must delete PI from its records and direct service providers to delete unless exception applies. Verifiable consumer request requires business to verify identity to reasonable degree of certainty, using existing authentication methods for account holders or matching at least two or three data points for non-account holders depending on sensitivity.""",
        key_factors=[
            "Business meets CCPA applicability threshold ($25M revenue, 100K+ consumers, or 50%+ revenue from selling PI)",
            "Consumer submits verifiable request (identity verified to reasonable degree)",
            "Request seeks disclosure of categories, specific pieces, sources, purposes, or third-party sharing",
            "Deletion request subject to enumerated exceptions (transaction, security, legal, internal use)",
            "Business responds within 45 days (extendable 45 more with notice)",
            "Information provided free of charge (up to 2 requests per 12 months)",
            "Portable and readily usable format required"
        ],
        primary_authority=[
            "Cal. Civ. Code Section 1798.100 (right to know categories of PI)",
            "Cal. Civ. Code Section 1798.110 (right to know specific pieces and sources)",
            "Cal. Civ. Code Section 1798.105 (right to delete)",
            "Cal. Civ. Code Section 1798.130 (response timing and format)",
            "CCPA Regulations 11 CCR Section 999.313 (verification methods)"
        ],
        burden_holder="Business to verify consumer identity and respond within statutory timelines; business may deny unverifiable requests",
        adversary_position="Request is not verifiable, consumer has not provided sufficient identification, deletion would fall under exception (e.g., legal compliance, internal lawful use), request is third or subsequent in 12-month period justifying reasonable fee",
        counter_arguments=[
            "Consumer identity cannot be verified despite reasonable methods employed",
            "Deletion would impair business's ability to complete transaction or comply with legal obligation (Cal. Civ. Code 1798.105(d) exceptions)",
            "Information requested is not personal information under CCPA (publicly available information from government records, deidentified or aggregate data)",
            "Business is not subject to CCPA (does not meet revenue, volume, or sale-derived revenue threshold)",
            "Request is excessive or manifestly unfounded (third+ request in 12 months, business may charge reasonable fee per 1798.145(a)(5))"
        ],
        resolution_strategy="Verify consumer identity using existing authentication for account holders or two/three data-point matching for non-account holders. Provide required disclosures in portable, readily usable format within 45 days. If deletion requested, assess whether any Section 1798.105(d) exceptions apply; if exception applies, retain PI and explain exception to consumer. If no exception, delete from records and direct service providers to delete. Document verification steps, response timing, and exception analysis in compliance records.",
        entity_scope="Businesses meeting CCPA applicability thresholds operating in California or collecting PI of CA residents",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Cal. Civ. Code Sections 1798.100-199.100 (CCPA as amended by CPRA)"
    ),
    DoctrineBlock(
        topic="CPRA Amendments - Sensitive Personal Information, Opt-Out Rights",
        keywords=["cpra", "sensitive personal information", "opt-out", "limit use", "sale of pi", "sharing", "cal civ code 1798.121"],
        conclusion_template=[
            "CPRA (effective January 1, 2023) created new category of Sensitive Personal Information (SPI) under Cal. Civ. Code Section 1798.140(ae), including SSN, driver's license, precise geolocation, racial/ethnic origin, religious beliefs, genetic data, biometric data, health data, sex life/orientation, and contents of mail/email/text unless business is intended recipient.",
            "Section 1798.121 grants consumers right to limit use and disclosure of SPI to purposes necessary to perform services or provide goods reasonably expected by average consumer or as authorized by regulations.",
            "Business must provide clear and conspicuous Do Not Sell or Share My Personal Information link (1798.135), honor opt-out within 15 business days, wait 12 months before requesting opt-in."
        ],
        reasoning_framework="""CPRA amended CCPA effective January 1, 2023, adding new consumer rights and business obligations. Sensitive Personal Information (SPI) is defined in Cal. Civ. Code Section 1798.140(ae) as (1) government-issued identifiers (SSN, driver's license, state ID, passport), (2) account log-in with security/access code, (3) financial account/debit/credit card number with security code, (4) precise geolocation, (5) racial or ethnic origin, religious or philosophical beliefs, or union membership, (6) contents of mail, email, text messages unless business is intended recipient, (7) genetic data, (8) biometric information processed to uniquely identify consumer, (9) personal information collected and analyzed concerning health, (10) personal information collected and analyzed concerning sex life or sexual orientation. Section 1798.121 grants consumers right to direct business to limit use and disclosure of SPI to (A) use necessary to perform services or provide goods reasonably expected by average consumer who requests those goods/services, (B) other uses specified in Section 1798.140(e) (preventing malicious/illegal activity, short-term transient use, certain internal research, quality/safety verification and improvement, and certain other enumerated purposes), and (C) purposes authorized by regulations. Business collecting SPI must provide conspicuous notice of right to limit and provide method for submitting requests. Business must comply with limit request within 15 business days. Opt-out of sale/sharing under Section 1798.120 and 1798.135 requires business to provide Do Not Sell or Share My Personal Information link on homepage and any California-specific page, honor opt-out signal (e.g., Global Privacy Control) for known California consumers, and refrain from selling/sharing PI for at least 12 months after opt-out unless consumer later affirmatively authorizes sale/sharing. Sale is defined broadly as selling, renting, releasing, disclosing, disseminating, making available, transferring, or otherwise communicating orally, in writing, or electronically, personal information to third party for monetary or other valuable consideration (Section 1798.140(ad)).""",
        key_factors=[
            "Business collects Sensitive Personal Information as enumerated in Section 1798.140(ae)",
            "Consumer directs business to limit use/disclosure of SPI beyond necessary purposes",
            "Business provides conspicuous notice of right to limit and submission method",
            "Business complies with limit request within 15 business days",
            "For sale/sharing opt-out: business provides Do Not Sell or Share link, honors opt-out signals (GPC), refrains from sale/sharing for 12 months post-opt-out",
            "Sale defined as transfer for monetary or other valuable consideration (including cross-context behavioral advertising)"
        ],
        primary_authority=[
            "Cal. Civ. Code Section 1798.140(ae) (SPI definition)",
            "Cal. Civ. Code Section 1798.121 (right to limit use of SPI)",
            "Cal. Civ. Code Section 1798.120 (right to opt-out of sale/sharing)",
            "Cal. Civ. Code Section 1798.135 (opt-out method and link requirements)",
            "CPRA Regulations (forthcoming final rules on SPI uses)"
        ],
        burden_holder="Business to provide notice, honor limit/opt-out requests within 15 days, respect opt-out for 12 months minimum",
        adversary_position="Use of SPI falls within necessary purposes or enumerated exceptions, consumer has not submitted valid opt-out, opt-out signal (GPC) not legally binding or not properly implemented, business did not sell PI but rather shared for limited business purpose qualifying as service provider relationship",
        counter_arguments=[
            "Use of SPI is necessary to perform services reasonably expected by consumer (e.g., geolocation for ride-hailing, financial data for payment processing)",
            "Use falls within Section 1798.140(e) enumerated purposes (security, short-term transient use, internal research)",
            "Opt-out signal (GPC) not properly configured or consumer later affirmatively authorized sale",
            "Transfer to third party is not a sale but rather a service provider relationship under written contract limiting use (Section 1798.140(ag))",
            "Business does not sell or share PI as defined (no monetary or valuable consideration exchanged)"
        ],
        resolution_strategy="Classify all collected data as PI or SPI per Section 1798.140 definitions. If collecting SPI, provide conspicuous notice of right to limit and implement mechanism to receive and honor limit requests within 15 business days. Limit SPI use to necessary purposes and enumerated exceptions unless consumer has not opted to limit. For sale/sharing, implement Do Not Sell or Share link, honor GPC and other opt-out signals, maintain opt-out for 12+ months unless consumer affirmatively opts back in. Document data classification, purpose necessity analysis, and opt-out/limit compliance in privacy records.",
        entity_scope="Businesses subject to CCPA/CPRA collecting Sensitive Personal Information or selling/sharing PI",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Cal. Civ. Code Sections 1798.120, 1798.121, 1798.135, 1798.140 (CPRA amendments effective 2023)"
    ),
    DoctrineBlock(
        topic="GDPR Lawful Basis and Data Minimization",
        keywords=["gdpr", "lawful basis", "consent", "legitimate interest", "data minimization", "article 5", "article 6"],
        conclusion_template=[
            "GDPR Article 6(1) requires one of six lawful bases for processing: (a) consent, (b) contract performance, (c) legal obligation, (d) vital interests, (e) public task, or (f) legitimate interests (except for public authorities in performance of tasks).",
            "Article 5(1)(c) mandates data minimization: personal data must be adequate, relevant, and limited to what is necessary in relation to purposes for which processed.",
            "Controller bears burden of demonstrating compliance with lawful basis and data minimization principles (accountability principle Article 5(2))."
        ],
        reasoning_framework="""GDPR applies to processing of personal data in context of establishment of controller or processor in EU, or processing of personal data of data subjects in EU where activities relate to offering goods/services (regardless of payment) or monitoring behavior (Article 3). Article 6(1) specifies six lawful bases: (a) data subject has given consent to processing for one or more specific purposes; (b) processing is necessary for performance of contract to which data subject is party or to take steps at request of data subject prior to entering contract; (c) processing is necessary for compliance with legal obligation to which controller is subject; (d) processing is necessary to protect vital interests of data subject or another natural person; (e) processing is necessary for performance of task carried out in public interest or in exercise of official authority vested in controller; (f) processing is necessary for purposes of legitimate interests pursued by controller or third party, except where such interests are overridden by interests or fundamental rights and freedoms of data subject requiring protection of personal data, particularly where data subject is child (not available for processing by public authorities in performance of tasks). Consent under Article 4(11) must be freely given, specific, informed, and unambiguous indication of wishes by statement or clear affirmative action. Consent cannot be valid basis if imbalance between controller and data subject (e.g., employer-employee, public authority). Legitimate interests basis requires balancing test (Recital 47): controller must weigh necessity and proportionality of processing against data subject's rights and freedoms, considering reasonable expectations of data subject based on relationship with controller, nature and sensitivity of data, safeguards implemented. Data minimization principle (Article 5(1)(c)) requires that personal data be adequate, relevant, and limited to what is necessary in relation to purposes for which processed. Controller must assess whether processing can be achieved with less data or anonymized/pseudonymized data. Accountability principle (Article 5(2)) requires controller to be able to demonstrate compliance with all GDPR principles.""",
        key_factors=[
            "Controller identifies valid lawful basis under Article 6(1) before processing begins",
            "If relying on consent: consent is freely given, specific, informed, unambiguous, and documented",
            "If relying on legitimate interests: balancing test conducted, documented, and demonstrates interests not overridden by data subject's rights",
            "If relying on contract: processing is objectively necessary for contract performance",
            "Data collected is adequate, relevant, and limited to purposes (data minimization)",
            "Controller can demonstrate compliance (accountability records, DPIAs where required)"
        ],
        primary_authority=[
            "GDPR Article 3 (territorial scope)",
            "GDPR Article 5(1)(c) (data minimization principle)",
            "GDPR Article 5(2) (accountability principle)",
            "GDPR Article 6(1) (lawfulness of processing)",
            "GDPR Article 4(11) (definition of consent)",
            "EDPB Guidelines 2/2019 on processing of personal data under Article 6(1)(b)",
            "EDPB Guidelines 3/2019 on processing of personal data through video devices"
        ],
        burden_holder="Controller to identify and document lawful basis, conduct and document balancing test if relying on legitimate interests, demonstrate data minimization and accountability",
        adversary_position="Supervisory authority or data subject challenges lawfulness of processing, argues consent was not freely given (imbalance, bundled conditions, lack of granularity), legitimate interests do not override data subject's rights (no balancing test or inadequate balancing), processing not necessary for contract (could perform contract without data), or data collection exceeds minimum necessary (violates data minimization)",
        counter_arguments=[
            "Consent was not freely given due to imbalance of power (EDPB Guidelines: employer-employee consent presumptively invalid)",
            "Consent was bundled with terms of service (not freely given per Article 7(4))",
            "Legitimate interests balancing test not documented or inadequate (must consider data subject expectations, sensitivity, safeguards per Recital 47)",
            "Processing claimed as necessary for contract but EDPB Guidelines 2/2019 say necessity must be objective and contract could be performed without data",
            "Data collected exceeds purposes (e.g., collecting date of birth when only age verification needed violates minimization)",
            "No DPIA conducted where required (Article 35 high-risk processing)"
        ],
        resolution_strategy="Before processing, select and document appropriate Article 6(1) lawful basis. If consent, ensure it meets Article 4(11) definition and document consent mechanism, granularity, and withdrawal method. If legitimate interests, conduct and document balancing test per Recital 47 and EDPB Guidelines, assessing necessity, proportionality, data subject expectations, and safeguards. If contract, ensure processing is objectively necessary per EDPB Guidelines 2/2019. Assess data minimization: collect only data adequate, relevant, and necessary for stated purposes. Maintain records of processing activities (Article 30) and conduct DPIA if processing likely results in high risk (Article 35). Regularly review lawful bases and data minimization as purposes or processing evolve.",
        entity_scope="Controllers and processors subject to GDPR (establishments in EU or targeting EU data subjects)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="GDPR Articles 3, 5, 6; EDPB Guidelines 2/2019, 3/2019"
    ),
    DoctrineBlock(
        topic="GDPR Data Subject Rights - Access, Rectification, Erasure, Portability",
        keywords=["gdpr rights", "data subject access", "right to erasure", "right to be forgotten", "data portability", "article 15", "article 17", "article 20"],
        conclusion_template=[
            "GDPR Article 15 grants data subjects right to obtain confirmation of processing, access to personal data, and information on purposes, categories, recipients, retention periods, and rights.",
            "Article 17 grants right to erasure (right to be forgotten) where data no longer necessary, consent withdrawn, objection raised, unlawfully processed, or legal obligation to erase, subject to exceptions for legal compliance, public interest, legal claims.",
            "Article 20 grants right to data portability: receive personal data in structured, commonly used, machine-readable format and transmit to another controller where processing based on consent or contract and carried out by automated means. Controller must respond within one month (extendable two months)."
        ],
        reasoning_framework="""GDPR grants data subjects extensive rights. Article 15 (right of access): data subject has right to obtain from controller (1) confirmation whether personal data concerning them is being processed, (2) if so, access to personal data and information including purposes, categories of data, recipients or categories of recipients, retention period or criteria, existence of rights (rectification, erasure, restriction, objection, complaint to supervisory authority), source of data if not collected from data subject, existence of automated decision-making including profiling and meaningful information about logic and significance. Controller must provide copy of personal data undergoing processing (Article 15(3)); first copy free, reasonable fee for additional copies. Article 17 (right to erasure): data subject has right to obtain erasure of personal data without undue delay where (a) data no longer necessary for purposes, (b) data subject withdraws consent and no other legal ground exists, (c) data subject objects under Article 21(1) and no overriding legitimate grounds, (d) personal data unlawfully processed, (e) erasure required for compliance with legal obligation, (f) data collected in relation to offer of information society services to child (Article 8(1)). Right does not apply where processing necessary for (a) exercising right of freedom of expression and information, (b) compliance with legal obligation or performance of public interest task, (c) public health, (d) archiving, research, statistics purposes if erasure likely to render impossible or seriously impair achievement of objectives, (e) establishment, exercise, or defense of legal claims. Article 20 (right to data portability): where processing based on consent (Article 6(1)(a) or 9(2)(a)) or contract (Article 6(1)(b)) and processing carried out by automated means, data subject has right to (1) receive personal data in structured, commonly used, machine-readable format, and (2) transmit that data to another controller without hindrance. Where technically feasible, data subject has right to have data transmitted directly from one controller to another. Right applies only to personal data provided by data subject, not inferred or derived data. Controller must respond to rights requests within one month of receipt, extendable by two further months considering complexity and number of requests (must inform data subject of extension within one month). If controller does not take action, must inform data subject within one month of reasons and possibility to lodge complaint with supervisory authority or judicial remedy.""",
        key_factors=[
            "Data subject submits valid request (identity verified per Article 12(6))",
            "For access (Article 15): controller confirms processing, provides copy of data and enumerated information",
            "For erasure (Article 17): one of six grounds exists (no longer necessary, consent withdrawn, objection, unlawful, legal obligation, child data) AND none of five exceptions apply (freedom of expression, legal obligation, public health, archiving/research, legal claims)",
            "For portability (Article 20): processing based on consent or contract, carried out by automated means, data provided by data subject (not inferred)",
            "Controller responds within one month (extendable two months with notice)",
            "If refusing request, controller explains reasons and informs of complaint/remedy rights"
        ],
        primary_authority=[
            "GDPR Article 12 (transparent information and modalities)",
            "GDPR Article 15 (right of access)",
            "GDPR Article 17 (right to erasure)",
            "GDPR Article 20 (right to data portability)",
            "EDPB Guidelines 01/2022 on data subject rights - right of access",
            "CJEU C-131/12 Google Spain (right to be forgotten)"
        ],
        burden_holder="Controller to verify data subject identity, respond within one month, provide data/information in accessible format, erase data if grounds exist and no exception applies, port data in machine-readable format if conditions met",
        adversary_position="Request is manifestly unfounded or excessive (Article 12(5) allows reasonable fee or refusal), identity cannot be verified (Article 12(6)), erasure exception applies (legal obligation, legal claims, public interest), portability does not apply (processing not based on consent/contract, not automated, data is inferred not provided), responding would require disproportionate effort",
        counter_arguments=[
            "Request is manifestly unfounded or excessive (repeated requests, no legitimate interest) justifying fee or refusal per Article 12(5)",
            "Identity of data subject cannot be verified despite reasonable means (Article 12(6) allows controller to request additional information)",
            "Erasure requested but exception applies: processing necessary for legal compliance (e.g., tax records retention), establishment/exercise/defense of legal claims (e.g., ongoing litigation), public interest task (e.g., archiving)",
            "Portability requested but processing not based on consent or contract (e.g., legal obligation basis), processing not automated (manual processing excluded), or data requested is inferred/derived not provided by data subject (EDPB clarifies portability applies only to observed data provided by data subject, not inferred profiles)",
            "Providing access would adversely affect rights and freedoms of others (Article 15(4), e.g., trade secrets, third-party personal data)"
        ],
        resolution_strategy="Verify data subject identity using reasonable means proportionate to risk (Article 12(6)). For access requests, compile all personal data processed, provide copy in accessible format (electronic preferred if request submitted electronically), and include Article 15 enumerated information (purposes, categories, recipients, retention, rights, source, automated decision-making). For erasure, assess whether any Article 17(1) ground exists; if yes, assess whether any Article 17(3) exception applies; if no exception, erase data from all systems and inform recipients per Article 19 unless impossible or disproportionate effort. For portability, verify processing is based on consent or contract and carried out by automated means; provide data in structured, commonly used, machine-readable format (e.g., JSON, CSV, XML); limit to data provided by data subject, not inferred. Respond within one month; if complexity/volume requires extension, notify data subject within one month of extension and reasons. If refusing request, explain reasons and inform of complaint rights. Document all requests and responses for accountability.",
        entity_scope="Controllers subject to GDPR processing personal data of EU data subjects",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="GDPR Articles 12, 15, 17, 20; EDPB Guidelines 01/2022; CJEU C-131/12 Google Spain"
    ),
    DoctrineBlock(
        topic="COPPA Parental Consent and Notice Requirements",
        keywords=["coppa", "children under 13", "verifiable parental consent", "direct notice to parent", "15 usc 6502", "ftc coppa rule"],
        conclusion_template=[
            "COPPA (15 USC Section 6502, 16 CFR Part 312) applies to operators of websites/online services directed to children under 13 or with actual knowledge of collecting personal information from children under 13.",
            "Operator must provide direct notice to parent of information practices (types of data collected, uses, disclosure practices, parental rights) and obtain verifiable parental consent before collecting, using, or disclosing personal information from child.",
            "FTC Rule Section 312.5 specifies methods for verifiable consent: signed form (email/fax/mail), credit card/payment verification, toll-free call with trained personnel, video conference, government-issued ID, or FTC-approved method. Email plus confirmation acceptable for internal use only (email plus)."
        ],
        reasoning_framework="""COPPA applies to operators of (1) commercial websites or online services directed to children under 13, or (2) general audience sites/services with actual knowledge they are collecting personal information from children under 13 (15 USC 6502(a)(1)). Directed to children means site is targeted to children under 13 based on subject matter, visual/audio content, age of models, language, advertising, competent and reliable empirical evidence of age of audience, or whether site uses animated characters or child-oriented activities and incentives (16 CFR 312.2 definition). Operator includes person who operates website/service and collects or maintains personal information, or on whose behalf such information is collected/maintained where site/service is directed to children (includes app developers, plug-in/ad network providers if they collect PI from child-directed site). Personal information includes first and last name, home/physical address, email, telephone number, SSN, persistent identifier usable to recognize user over time and across sites (cookies, IP, device ID if used to recognize over time), photograph/video/audio file containing child's image or voice, geolocation sufficient to identify street name and city/town, and information concerning child or child's parent combined with identifier (16 CFR 312.2). Before collecting PI from child, operator must: (1) post clear and comprehensive privacy policy on homepage and at each area where PI is collected, describing types of information collected, how used, whether disclosed to third parties, and parental rights (Section 312.4(d)); (2) provide direct notice to parent (separate from privacy policy), including operator identity and contact info, types of PI to be collected and how collected, how operator will use PI, whether operator will disclose to third parties and types of third parties, that operator will not require child to disclose more information than reasonably necessary to participate in activity, and that parent can review child's PI, direct operator to delete it, and refuse further collection/use (Section 312.4(c)); (3) obtain verifiable parental consent before collecting, using, or disclosing child's PI (Section 312.5). Verifiable parental consent methods (Section 312.5(b)): signed consent form via fax/mail/electronic scan, use of credit card/debit card/other payment system that provides notification of each transaction, toll-free telephone call to trained personnel, video conference with trained personnel, government-issued ID checked against database, or method approved by FTC. Email plus confirmation acceptable only if operator uses PI for internal use only and does not disclose to third parties (email plus: parent provides consent via email and operator sends confirmation to email address, and parent must reply or take affirmative step to confirm). Operator must make reasonable effort to ensure parent providing consent is child's parent by using one of enumerated methods commensurate with risk (higher risk of harm or public disclosure requires more robust method).""",
        key_factors=[
            "Website or online service is directed to children under 13 OR operator has actual knowledge of collecting PI from child under 13",
            "Operator posts clear, comprehensive privacy policy on homepage and at collection points",
            "Operator provides direct notice to parent with required elements (operator identity, PI types, uses, disclosures, parental rights)",
            "Operator obtains verifiable parental consent using FTC-approved method before collecting/using/disclosing PI",
            "Consent method is commensurate with risk (email plus acceptable only for internal use only; disclosure or public posting requires signed form, credit card, or other robust method)",
            "Operator does not condition child's participation on disclosure of more PI than reasonably necessary"
        ],
        primary_authority=[
            "15 USC Section 6501-6506 (COPPA statute)",
            "16 CFR Part 312 (COPPA Rule)",
            "FTC COPPA Frequently Asked Questions",
            "FTC Complying with COPPA: Frequently Asked Questions (2013, updated 2020)"
        ],
        burden_holder="Operator to determine if site is child-directed or has actual knowledge, post privacy policy, provide direct notice to parent, obtain verifiable parental consent using appropriate method, and comply with parental requests for access/deletion",
        adversary_position="FTC alleges operator failed to obtain verifiable parental consent, used email plus method for activity involving disclosure to third parties or public posting (not just internal use), did not provide required direct notice to parent, privacy policy was not clear and comprehensive, or operator conditioned participation on collection of more PI than reasonably necessary (Section 312.7 prohibition)",
        counter_arguments=[
            "Operator used email plus method for consent but disclosed PI to third parties or allowed public posting (email plus acceptable only for internal use per Section 312.5(b)(2))",
            "Consent method not sufficiently robust given risk (e.g., email plus used for activity involving public posting, but FTC guidance requires signed form or credit card for such use)",
            "Direct notice to parent omitted required elements (did not disclose third-party recipients, did not inform of parental rights)",
            "Operator conditioned child's participation on disclosure of PI not reasonably necessary (Section 312.7: operator may not require child to disclose more PI than reasonably necessary to participate in activity as condition of participation)",
            "Operator did not post privacy policy on homepage or at each PI collection point (Section 312.4(d) requirement)"
        ],
        resolution_strategy="Determine if site/service is directed to children under 13 using Section 312.2 factors (subject matter, visual content, age of models, empirical evidence, child-oriented features). If child-directed or operator has actual knowledge, post clear privacy policy on homepage and at each collection area. Before collecting PI, provide direct notice to parent including all required elements per Section 312.4(c). Obtain verifiable parental consent using method commensurate with risk: if PI used only internally, email plus acceptable; if disclosed to third parties or publicly posted, use signed form, credit card, toll-free call, video conference, or government ID. Do not condition participation on collection of more PI than necessary. Provide mechanism for parent to review, delete, and refuse further collection. Maintain records of consent and compliance. Consult FTC COPPA FAQs and Business Center guidance for method selection and safe harbor programs.",
        entity_scope="Operators of websites or online services directed to children under 13 or with actual knowledge of collecting PI from children under 13",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="15 USC 6501-6506; 16 CFR Part 312; FTC enforcement actions (e.g., FTC v. TikTok (Musical.ly), FTC v. YouTube)"
    ),
    DoctrineBlock(
        topic="FERPA Education Records Privacy and Disclosure Exceptions",
        keywords=["ferpa", "education records", "parental consent", "directory information", "legitimate educational interest", "20 usc 1232g", "34 cfr 99"],
        conclusion_template=[
            "FERPA (20 USC Section 1232g, 34 CFR Part 99) protects privacy of student education records at educational institutions receiving federal funds. Generally prohibits disclosure without written consent of parent (or eligible student if 18+ or attending postsecondary institution).",
            "Exceptions allow disclosure without consent to: school officials with legitimate educational interest, officials of another school where student seeks enrollment, authorized federal/state/local education authorities, accrediting organizations, financial aid determinations, state/local juvenile justice system pursuant to state law, organizations conducting studies for educational agency, compliance with judicial order/subpoena (with notice), health/safety emergency, and directory information (if notice and opt-out provided).",
            "34 CFR Section 99.31-99.37 enumerate exceptions; Section 99.32 requires record of disclosures; Section 99.37 defines directory information and notice requirements."
        ],
        reasoning_framework="""FERPA applies to educational agencies and institutions receiving federal funds under any program administered by Department of Education (20 USC 1232g(a)(3)). Education records are records directly related to student and maintained by educational agency or person acting for agency (34 CFR 99.3), excluding sole possession records, law enforcement records, employment records (if not contingent on attendance), medical treatment records, and alumni records created after individual no longer in attendance. Parent (or eligible student: student who has reached 18 or attends postsecondary institution per 34 CFR 99.3) has right to inspect/review education records (Section 99.10), request amendment (Section 99.20), and consent to disclosure (Section 99.30). General rule: educational agency may not disclose personally identifiable information from education records without prior written consent of parent or eligible student, except as provided in Section 99.31 exceptions. Key exceptions (34 CFR 99.31): (a)(1) school officials with legitimate educational interest (must be defined in annual notification, typically teachers, administrators, counselors who need access to perform institutional responsibilities); (a)(2) officials of another school/school system/postsecondary institution where student seeks or intends to enroll or is already enrolled, provided disclosure is for purposes related to enrollment/transfer and agency makes reasonable attempt to notify parent (unless annual notification states records will be forwarded on request or disclosure is initiated by parent/student); (a)(3) authorized representatives of US Comptroller General, Attorney General, Secretary of Education, or state/local educational authorities for audit/evaluation of federal/state-supported education programs or enforcement of federal legal requirements; (a)(4) connection with financial aid application; (a)(5) state and local officials/authorities to whom disclosure is specifically authorized by state statute adopted before November 19, 1974; (a)(6) organizations conducting studies for or on behalf of educational agency to develop/validate tests, administer student aid, improve instruction, provided agreement limits use and requires destruction when no longer needed; (a)(7) accrediting organizations; (a)(8) parents of dependent student as defined in IRS code (institution may but is not required to disclose); (a)(9) compliance with judicial order or lawfully issued subpoena, provided educational agency makes reasonable effort to notify parent or eligible student before compliance unless subpoena orders nondisclosure or is issued for law enforcement purpose and court/issuing agency orders nondisclosure; (a)(10) health or safety emergency if information necessary to protect health/safety of student or others (Section 99.36 factors: severity of threat, need for information, time to respond, ability of parties to address emergency, consider totality of circumstances); (a)(11) information required by state juvenile justice system pursuant to specific state law. Directory information exception (34 CFR 99.37): educational agency may disclose directory information (name, address, telephone, email, photo, date/place of birth, major, participation in activities/sports, weight/height of athletic team members, dates of attendance, degrees/awards, most recent previous school attended, student ID number if cannot be used alone to access records) without consent if agency has given public notice of types of information designated as directory, explained right to opt out, and allowed reasonable time to opt out. Agency must annually notify parents and eligible students of FERPA rights, directory information policy, and how to opt out (Section 99.7).""",
        key_factors=[
            "Educational institution receives federal funds (FERPA applies)",
            "Record is education record (directly related to student, maintained by institution, not excluded category)",
            "Disclosure sought without prior written consent of parent or eligible student",
            "If exception claimed: disclosure fits within one of Section 99.31 enumerated exceptions",
            "If school official exception: official has legitimate educational interest as defined in annual notification",
            "If directory information: institution provided annual notice, defined directory categories, explained opt-out right, allowed reasonable opt-out period, and student/parent did not opt out",
            "If health/safety emergency: totality of circumstances demonstrates severity of threat and necessity of disclosure",
            "Institution maintains record of disclosures per Section 99.32 (except disclosures to school officials, directory info, or parent/eligible student)"
        ],
        primary_authority=[
            "20 USC Section 1232g (FERPA statute)",
            "34 CFR Part 99 (FERPA regulations)",
            "US Dept of Education FERPA Model Notification of Rights",
            "US Dept of Education Letter to Fordham University (2009) re health/safety emergency",
            "Gonzaga Univ. v. Doe, 536 U.S. 273 (2002) (FERPA creates no private right of action)"
        ],
        burden_holder="Educational institution to obtain written consent or fit disclosure within enumerated exception, maintain disclosure records, provide annual notification of rights, and honor opt-out of directory information",
        adversary_position="Dept of Education alleges institution disclosed education records without consent and without fitting exception, failed to provide annual notification, disclosed directory information without notice/opt-out, or disclosed under health/safety emergency exception when threat did not warrant disclosure under Section 99.36 factors",
        counter_arguments=[
            "Disclosure made to school official but official lacked legitimate educational interest as defined in annual notification (e.g., accessing records out of curiosity not related to institutional responsibility)",
            "Disclosure under directory information but institution did not provide annual notice, did not allow reasonable opt-out period, or student/parent had opted out",
            "Disclosure under health/safety emergency but threat was not articulable and significant (Section 99.36 requires severity, imminence, and necessity; speculative threat insufficient)",
            "Disclosure to another school but institution did not make reasonable attempt to notify parent (unless annual notification states records forwarded on request or parent initiated)",
            "Disclosure pursuant to subpoena but institution did not make reasonable effort to notify parent (unless subpoena or court ordered nondisclosure)"
        ],
        resolution_strategy="Provide annual notification to parents and eligible students of FERPA rights, including right to inspect/review, request amendment, consent to disclosure, and opt out of directory information; define directory information categories and explain opt-out process. Define legitimate educational interest in annual notification (e.g., school official has responsibilities requiring access, access serves institutional purpose, access is necessary to perform task). Before disclosing without consent, identify applicable Section 99.31 exception and ensure conditions met (e.g., if school official, verify legitimate educational interest; if directory, verify notice provided and student did not opt out; if health/safety emergency, assess severity/imminence/necessity under Section 99.36). Maintain record of disclosures per Section 99.32 (except to school officials, directory, parent/eligible student). For disclosures to other schools, make reasonable attempt to notify parent unless annual notification states forwarding policy or parent initiated. For subpoenas, notify parent unless nondisclosure ordered. Consult Dept of Education FERPA guidance and model notifications.",
        entity_scope="Educational agencies and institutions receiving federal Department of Education funds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="20 USC 1232g; 34 CFR Part 99; Gonzaga Univ. v. Doe, 536 U.S. 273 (2002)"
    ),
    DoctrineBlock(
        topic="GLBA Privacy Rule and Safeguards for Financial Institutions",
        keywords=["glba", "gramm-leach-bliley", "financial institution", "nonpublic personal information", "privacy notice", "opt-out", "15 usc 6801", "16 cfr 313"],
        conclusion_template=[
            "GLBA (15 USC Section 6801-6809, 16 CFR Part 313 Privacy Rule, 16 CFR Part 314 Safeguards Rule) requires financial institutions to provide privacy notices and protect nonpublic personal information (NPI).",
            "Privacy Rule Section 313.5-313.9: institution must provide initial privacy notice when customer relationship established, annual notices, and opt-out notice if sharing NPI with nonaffiliated third parties outside exceptions. Customer may opt out of such sharing.",
            "Safeguards Rule Section 314.3-314.4: institution must develop, implement, and maintain comprehensive information security program with administrative, technical, and physical safeguards to protect customer information, including risk assessment, access controls, encryption, employee training, service provider oversight."
        ],
        reasoning_framework="""GLBA applies to financial institutions: any institution significantly engaged in financial activities as determined by Federal Reserve Board under Bank Holding Company Act (12 USC 1843(k)), including banks, securities firms, insurance companies, loan/finance companies, credit counselors, career counselors, and entities FTC has jurisdiction over that are significantly engaged in financial activities (16 CFR 313.3(k)). Nonpublic personal information (NPI) is personally identifiable financial information (name, address, SSN, account number, credit/debit card number, account balance, payment history, loan application info) provided by consumer, resulting from transaction with consumer, or otherwise obtained by financial institution about consumer in connection with providing financial product/service, excluding publicly available information (16 CFR 313.3(n), (p)). Consumer is individual who obtains or has obtained financial product/service from institution for personal, family, or household purposes (16 CFR 313.3(e)). Customer is consumer with customer relationship (continuing relationship per 16 CFR 313.3(i), e.g., deposit account, loan, brokerage account, advisory contract). Privacy Rule Section 313.5: institution must provide clear, conspicuous initial privacy notice to customer no later than when customer relationship established, describing categories of NPI collected, categories of NPI disclosed, categories of affiliates/nonaffiliated third parties to whom disclosed, consumer's right to opt out, policies on protecting confidentiality/security, and disclosures under FCRA Section 603(d)(2)(A)(iii) if applicable. Section 313.8: if institution discloses NPI to nonaffiliated third party (other than exceptions in Sections 313.13-313.15: service providers/joint marketing, processing/servicing transactions, credit reporting, fraud/legal compliance), institution must provide opt-out notice explaining consumer's right to direct institution not to disclose NPI to nonaffiliated third party, and must honor opt-out. Exceptions to opt-out requirement: disclosures to service providers (Section 313.13: if contract prohibits third party from disclosing or using except to perform services or as required by law), disclosures necessary to process/service transactions (Section 313.14: to consummate transaction, administer/enforce transaction, effect/enforce transaction), disclosures required by law or for fraud/legal/enforcement purposes (Section 313.15). Section 313.7: institution must provide annual privacy notice to customers (at least once in any 12-month period) describing same elements as initial notice. Safeguards Rule 16 CFR Part 314: financial institution must develop, implement, maintain comprehensive written information security program containing administrative, technical, physical safeguards appropriate to size/complexity/nature/scope of activities and sensitivity of customer information (Section 314.3). Program must include: (1) designated employee(s) to coordinate program, (2) risk assessment identifying reasonably foreseeable internal/external threats to security/integrity/confidentiality of customer information and assessing sufficiency of safeguards to control risks, (3) safeguards to control identified risks (access controls, encryption, authentication, secure development, monitoring, incident response), (4) service provider oversight (contracts requiring maintenance of safeguards), (5) periodic evaluation and adjustment of program (at least annually or when material change to operations/risks). Section 314.4: program must include specific safeguards such as access controls, data inventory/classification, encryption of customer information in transit and at rest (unless compensating controls achieve equivalent protection), multi-factor authentication for access to customer information, secure disposal, change management, monitoring/logging, incident response plan, periodic penetration testing and vulnerability assessment, employee training.""",
        key_factors=[
            "Entity is financial institution (significantly engaged in financial activities, FTC jurisdiction)",
            "Information is nonpublic personal information (PIFI provided by, resulting from, or obtained about consumer in connection with financial product/service, not publicly available)",
            "Institution provides initial privacy notice when customer relationship established",
            "Institution provides annual privacy notice to customers",
            "If sharing NPI with nonaffiliated third parties (outside exceptions): institution provides opt-out notice and honors opt-out",
            "Sharing fits within exception (service provider with contract, transaction processing, required by law, fraud/legal compliance)",
            "Institution implements comprehensive information security program with required safeguards (risk assessment, access controls, encryption, MFA, monitoring, incident response, employee training, service provider oversight)"
        ],
        primary_authority=[
            "15 USC Sections 6801-6809 (GLBA Privacy and Safeguards provisions)",
            "16 CFR Part 313 (Privacy of Consumer Financial Information - Privacy Rule)",
            "16 CFR Part 314 (Standards for Safeguarding Customer Information - Safeguards Rule)",
            "Interagency Guidelines Establishing Information Security Standards (Appendix B to Part 30, OCC; 12 CFR Part 208 Appendix D-2, Federal Reserve; 12 CFR Part 364 Appendix B, FDIC)",
            "FTC Safeguards Rule FAQs"
        ],
        burden_holder="Financial institution to provide initial and annual privacy notices, provide opt-out for nonaffiliated third-party sharing outside exceptions, honor opt-out, and implement comprehensive information security program with enumerated safeguards",
        adversary_position="FTC or regulatory agency alleges institution failed to provide required privacy notices, disclosed NPI to nonaffiliated third party without opt-out (and disclosure did not fit exception), failed to honor consumer's opt-out, or failed to implement adequate safeguards (no risk assessment, no encryption, no MFA, no incident response plan, no service provider oversight, no employee training, no periodic testing)",
        counter_arguments=[
            "Privacy notice not provided at customer relationship establishment or not provided annually (Section 313.5, 313.7 violations)",
            "NPI disclosed to nonaffiliated third party but no opt-out notice provided (Section 313.10 violation) or opt-out not honored",
            "Claimed service provider exception but no written contract requiring safeguards (Section 313.13 requires contract limiting use/disclosure)",
            "Information security program inadequate: no designated coordinator, no risk assessment, no encryption of NPI in transit/at rest, no MFA, no logging/monitoring, no incident response plan, no penetration testing, no employee training, no service provider oversight (Section 314.3-314.4 violations)",
            "Claimed exception for transaction processing but disclosure was not necessary to effect/administer/enforce transaction (Section 313.14 exception applies only to disclosures necessary to consummate, administer, or enforce transaction)"
        ],
        resolution_strategy="Determine if entity is financial institution under 16 CFR 313.3(k). Classify all consumer information as NPI or publicly available. Provide initial privacy notice to all customers when customer relationship established, including all required elements per Section 313.5 (NPI collected, NPI disclosed, third parties, opt-out rights, security policies). Provide annual privacy notice to customers at least once per 12 months. Before disclosing NPI to nonaffiliated third parties, determine if exception applies (service provider with contract per Section 313.13, transaction processing per 313.14, required by law/fraud/legal per 313.15); if no exception, provide opt-out notice and mechanism, and honor opt-out. Develop, implement, maintain written information security program per Section 314.3-314.4: designate coordinator, conduct risk assessment, implement safeguards (access controls, encryption of NPI in transit and at rest, MFA, monitoring/logging, incident response, secure disposal, change management, penetration testing, vulnerability assessment), oversee service providers via contracts requiring safeguards, train employees, evaluate and adjust program at least annually. Maintain records of program, risk assessments, testing, and training. Consult FTC Safeguards Rule FAQs and Interagency Guidelines for implementation guidance.",
        entity_scope="Financial institutions significantly engaged in financial activities and subject to FTC jurisdiction (banks, securities firms, insurance companies, loan/finance companies, credit counselors, etc.)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="15 USC 6801-6809; 16 CFR Parts 313, 314; FTC enforcement actions (e.g., FTC v. TaxSlayer, FTC v. Chegg)"
    ),
    DoctrineBlock(
        topic="FTC Act Section 5 Unfair/Deceptive Privacy and Security Practices",
        keywords=["ftc act section 5", "unfair practices", "deceptive practices", "privacy policy enforcement", "reasonable security", "15 usc 45"],
        conclusion_template=[
            "FTC Act Section 5 (15 USC Section 45(a)) prohibits unfair or deceptive acts or practices in or affecting commerce. FTC uses Section 5 authority to enforce privacy and data security obligations even where no specific privacy statute applies.",
            "Practice is deceptive if it involves material misrepresentation or omission likely to mislead reasonable consumer. FTC enforces privacy policy promises: failure to honor stated privacy practices is deceptive (e.g., FTC v. Facebook, FTC v. Google Buzz).",
            "Practice is unfair if it causes or is likely to cause substantial injury to consumers not reasonably avoidable and not outweighed by benefits. FTC enforces reasonable security: failure to implement reasonable data security measures is unfair (e.g., FTC v. Wyndham, FTC v. LabMD, FTC v. Equifax)."
        ],
        reasoning_framework="""FTC Act Section 5(a) declares unlawful unfair or deceptive acts or practices in or affecting commerce (15 USC 45(a)). FTC has jurisdiction over persons, partnerships, corporations (excluding banks, savings and loans, federal credit unions, common carriers subject to Communications Act, air carriers, and other narrow exemptions per 15 USC 45(a)(2)). Deceptive acts or practices: FTC Policy Statement on Deception (1983) establishes three-part test: (1) representation, omission, or practice likely to mislead, (2) from perspective of reasonable consumer under circumstances, (3) material (likely to affect consumer's conduct or decision). Material misrepresentations include express claims, implied claims, and failure to disclose information necessary to prevent express/implied claim from being misleading. FTC applies deception standard to privacy policies: if company makes representation about its privacy/data practices in privacy policy, failure to honor those representations is deceptive act (FTC v. Facebook consent order 2011: Facebook promised not to share user data with third parties but did, violating policy and constituting deception; FTC v. Google Buzz 2011: Google used Gmail contacts for Buzz without notice, contrary to Gmail privacy policy). Unfair acts or practices: Section 5(n) (added by FTC Act Amendments 1994) codifies three-part test: act or practice is unfair if (1) it causes or is likely to cause substantial injury to consumers, (2) which is not reasonably avoidable by consumers themselves, and (3) not outweighed by countervailing benefits to consumers or competition (15 USC 45(n)). FTC applies unfairness standard to data security: failure to employ reasonable measures to protect consumer data constitutes unfair practice. FTC v. Wyndham Worldwide Corp., 799 F.3d 236 (3d Cir. 2015): Wyndham suffered three data breaches affecting 619,000 accounts due to inadequate security (storing payment card info in clear text, default/weak passwords, inadequate firewall, no intrusion detection); FTC alleged unfair practice; Third Circuit held FTC has authority under Section 5 to regulate cybersecurity and Wyndham had fair notice that its practices could be unfair; case settled with consent order requiring comprehensive security program, annual assessments for 20 years. FTC v. LabMD, Inc., 894 F.3d 1221 (11th Cir. 2018): LabMD exposed 1,700 patient files on peer-to-peer network due to inadequate security; FTC alleged unfair practice; Eleventh Circuit held FTC failed to show substantial consumer injury (mere exposure to risk insufficient, must show actual or likely identity theft, financial harm) but did not disturb FTC's general authority to regulate data security under Section 5. FTC settlements typically require: (1) comprehensive information security program addressing identified risks, (2) designation of employee(s) responsible for program, (3) risk assessments, (4) safeguards testing/monitoring, (5) service provider oversight, (6) incident response plan, (7) biennial third-party assessments for 10-20 years, (8) FTC reporting. Reasonable security standard is fact-specific, considering nature/sensitivity of data, size/complexity of operations, cost of safeguards, and current standards in industry (multi-factor authentication, encryption, access controls, logging/monitoring, employee training, patching, network segmentation).""",
        key_factors=[
            "FTC has jurisdiction (entity not within statutory exemptions)",
            "For deception: representation or omission in privacy policy or elsewhere, likely to mislead reasonable consumer, material to consumer decision, and actual practice diverges from representation",
            "For unfairness: practice causes or likely causes substantial injury (data breach, exposure, unauthorized access), injury not reasonably avoidable by consumer, injury not outweighed by benefits",
            "For security unfairness: failure to implement reasonable security measures (encryption, MFA, access controls, monitoring, patching, training) given nature/sensitivity of data and size/resources of entity",
            "Consumer harm (identity theft, financial loss, or in some circuits mere exposure to risk may suffice per Wyndham; compare LabMD requiring actual/likely harm)"
        ],
        primary_authority=[
            "15 USC Section 45(a) (FTC Act Section 5 prohibition on unfair/deceptive practices)",
            "15 USC Section 45(n) (unfairness definition)",
            "FTC Policy Statement on Deception (1983)",
            "FTC Policy Statement on Unfairness (1980)",
            "FTC v. Wyndham Worldwide Corp., 799 F.3d 236 (3d Cir. 2015)",
            "FTC v. LabMD, Inc., 894 F.3d 1221 (11th Cir. 2018)",
            "FTC consent orders: Facebook (2011, 2019), Google Buzz (2011), Equifax (2019), Uber (2017), Zoom (2020)"
        ],
        burden_holder="Entity to honor stated privacy policy, implement reasonable security measures commensurate with data sensitivity and entity size/resources, avoid practices causing substantial injury not outweighed by benefits",
        adversary_position="FTC alleges entity made deceptive representations in privacy policy (promised not to share data but shared, promised to delete but retained, promised security but failed to implement), or entity's security practices were unreasonable (no encryption, weak/default passwords, no MFA, no monitoring, inadequate patching, no employee training) causing substantial consumer injury (data breach, identity theft, financial loss)",
        counter_arguments=[
            "Privacy policy representation was ambiguous or not material, consumer would not have relied on representation, or actual practice did not diverge from policy as reasonably interpreted",
            "Security measures were reasonable given entity's size, resources, and data sensitivity (smaller entity may have fewer resources than large enterprise; publicly available data may require less protection than SSN/financial data)",
            "Injury was reasonably avoidable by consumers (e.g., consumers could have used stronger passwords, enabled MFA, monitored accounts)",
            "Injury not substantial (LabMD: Eleventh Circuit held mere exposure to risk without showing actual or likely identity theft/financial harm insufficient for unfairness; compare Wyndham where 619,000 accounts compromised and fraudulent charges occurred)",
            "Benefits to consumers or competition outweigh injury (difficult to sustain for data breach scenarios)"
        ],
        resolution_strategy="Draft privacy policy accurately reflecting actual data practices; do not promise practices entity will not follow (e.g., do not promise not to share if business model involves sharing; do not promise deletion after X days if retention longer; do not promise encryption if not encrypting). Implement reasonable data security program addressing recognized risks: (1) encrypt sensitive data in transit (TLS) and at rest, (2) implement multi-factor authentication for access to sensitive data/systems, (3) enforce access controls (least privilege, role-based access), (4) log and monitor access/activities, (5) timely patching of known vulnerabilities, (6) network segmentation, (7) employee training on phishing/social engineering, (8) incident response plan, (9) vendor/service provider security assessments and contracts, (10) periodic penetration testing and vulnerability scanning. Tailor security measures to data sensitivity: higher protection for SSN, financial data, health data, biometric data; reasonable protection for less sensitive data. Consider entity size and resources but note FTC expects baseline security (encryption, MFA, patching) even from smaller entities. Document security program, risk assessments, testing, and training. If breach occurs, notify FTC if significant (cf. Health Breach Notification Rule 16 CFR Part 318 for PHR vendors). Consult FTC Start with Security guide, Data Security Made Simpler resources, and consent order patterns for industry best practices.",
        entity_scope="Entities subject to FTC jurisdiction (excludes banks, federal credit unions, common carriers, air carriers per 15 USC 45(a)(2))",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="15 USC 45(a), (n); FTC v. Wyndham, 799 F.3d 236 (3d Cir. 2015); FTC v. LabMD, 894 F.3d 1221 (11th Cir. 2018); FTC consent orders"
    ),
    DoctrineBlock(
        topic="State Data Breach Notification Laws - General Obligations",
        keywords=["breach notification", "state law", "personal information", "unauthorized access", "security breach", "notice to consumer", "notice to attorney general"],
        conclusion_template=[
            "All 50 states, DC, and territories have data breach notification laws requiring entities to notify affected individuals when personal information is subject to unauthorized acquisition or access. Statutes vary by state but share core elements.",
            "Typical statute defines personal information as name combined with SSN, driver's license, financial account number, or other sensitive data. Security breach is unauthorized acquisition of unencrypted PI or encrypted PI with acquired encryption key, compromising security/confidentiality.",
            "Upon discovering breach, entity must conduct investigation, determine if notification required (risk of harm analysis in some states, strict liability in others), notify affected individuals without unreasonable delay (most states: without unreasonable delay; some specify 30-90 days), and notify attorney general/regulators if threshold met (often 500-1,000+ residents or state-specific threshold)."
        ],
        reasoning_framework="""Data breach notification laws exist in all 50 states, DC, Puerto Rico, Virgin Islands, Guam. First enacted California SB 1386 (2002), effective 2003 (Cal. Civ. Code 1798.82). Statutes vary significantly but common framework: (1) Applicability: applies to persons/businesses that own, license, or maintain personal information (some states apply only to data owners, others include licensees/service providers). (2) Personal Information (PI) definition: generally name (first + last or first + middle initial) combined with one or more of: SSN, driver's license or state ID number, financial account/credit/debit card number with security code/access code/password, medical/health insurance information, biometric data, username/email with password/security question answer. Some states include additional categories (e.g., passport number, taxpayer ID, genetic data, individual health info). PI must be unencrypted/unredacted; if encrypted and encryption key not acquired, many states exclude from breach definition. (3) Security Breach definition: unauthorized acquisition (most states) or access (fewer states: Alabama, Maryland use access; most use acquisition) of unencrypted/unredacted PI that compromises security, confidentiality, or integrity of PI. Acquisition by employee/agent if for legitimate business purpose often excluded. Good-faith acquisition by employee/agent followed by good-faith use/disclosure within entity's authority often excluded. Some states require breach compromise security/confidentiality (e.g., California: unauthorized acquisition that compromises security, confidentiality, or integrity; contrast Alabama: breach of security means unauthorized access and acquisition). (4) Notice Trigger: upon discovery or notification of breach. Discovery typically when entity or service provider determines breach occurred (some states: when reasonably believes breach occurred). (5) Investigation and Risk Assessment: many states allow or require entity to conduct reasonable investigation to determine scope of breach and whether notification required. Some states (e.g., Ohio, Wisconsin, Colorado) allow entity to forgo notice if after investigation entity reasonably determines breach unlikely to cause harm (risk-of-harm exception). Most states require notice regardless of risk (strict liability). (6) Timing: notice must be made without unreasonable delay and consistent with needs of law enforcement and measures to determine scope and restore integrity. Specific timelines vary: e.g., California: without unreasonable delay, Florida: without unreasonable delay (caselaw suggests 30 days), New York: without unreasonable delay (statute suggests most expedient time possible but allows reasonable delay to determine scope and restore integrity), Massachusetts: as soon as practicable and without unreasonable delay, Illinois: without unreasonable delay, Ohio: without unreasonable delay or within 45 days after discovery (some states specify days: Colorado 30 days, Connecticut notification without unreasonable delay, Iowa without unreasonable delay, Washington without unreasonable delay). (7) Content of Notice: typically must include description of breach, types of PI involved, steps entity has taken, contact information, advice to consumer (e.g., obtain credit report, place fraud alert, contact FTC), toll-free numbers for credit bureaus and FTC. Some states specify required and prohibited content (e.g., California: general description, type of PI, date or estimated date, remedial steps, contact info; do not include unnecessary PI in notice). (8) Method of Notice: written notice (mail), electronic notice (email if established email relationship and consistent with E-SIGN Act), or substitute notice if cost exceeds threshold (typically $250,000-500,000), affected population exceeds threshold (typically 500,000), or insufficient contact information (substitute notice: email if email address available, conspicuous posting on website, notice to major statewide media). (9) Notice to Attorney General/Regulators: many states require notice to state attorney general if breach affects threshold number of state residents (e.g., California: 500+, New York: 500+, Florida: 500+, Massachusetts: notification to AG and Director of Consumer Affairs, Illinois: AG if 500+ IL residents, Texas: AG if breach requires notice, North Carolina: AG without unreasonable delay). Some require notice to consumer reporting agencies if large number affected (e.g., 1,000+ per federal FCRA 15 USC 1681c-2). (10) Service Provider Obligations: if service provider discovers breach of data it maintains for third party, must notify third-party owner/licensee (most states impose this duty). (11) Exceptions and Safe Harbors: entity complying with HIPAA, GLBA, or other federal law notification requirements may be deemed in compliance (varies by state). Encrypted data often excluded from PI definition if encryption key not acquired. Some states allow delay for law enforcement investigation. (12) Penalties: state AG enforcement, private right of action (some states: California allows private action if failure to implement/maintain reasonable security and breach, Montana allows if willful, others vary), statutory damages or actual damages, injunctive relief.""",
        key_factors=[
            "Entity owns, licenses, or maintains personal information of state residents",
            "Security breach occurs: unauthorized acquisition/access of unencrypted PI (or encrypted PI with acquired key) compromising security/confidentiality",
            "Personal information defined by statute is involved (name + SSN, driver's license, financial account, or other enumerated data)",
            "Investigation determines notice is required (risk-of-harm analysis if state allows; most states strict liability)",
            "Notice provided to affected individuals without unreasonable delay (or within state-specific timeline: 30-90 days)",
            "Notice includes required elements (description, PI types, date, remedial steps, contact info, consumer advice)",
            "If state threshold met (e.g., 500+ residents): notice to state attorney general and/or regulators",
            "If service provider: notification to data owner/licensee"
        ],
        primary_authority=[
            "Cal. Civ. Code Section 1798.82 (California breach notification)",
            "N.Y. Gen. Bus. Law Section 899-aa (New York breach notification)",
            "Tex. Bus. & Com. Code Section 521.053 (Texas breach notification)",
            "Mass. Gen. Laws ch. 93H (Massachusetts data security and breach notification)",
            "Fla. Stat. Section 501.171 (Florida breach notification)",
            "Ill. Comp. Stat. 5/815/530/10 (Illinois PIPA breach notification)",
            "NCSL Security Breach Notification Laws (state-by-state compilation)"
        ],
        burden_holder="Entity owning, licensing, or maintaining PI to investigate breach, determine scope, notify affected individuals and regulators per state law timelines, implement reasonable security to prevent breach",
        adversary_position="State AG alleges entity failed to provide timely notice (delayed beyond unreasonable period or state-specific deadline), notice omitted required elements, entity did not notify AG despite exceeding threshold, entity failed to implement reasonable security leading to breach (some states allow AG action for unreasonable security even absent breach statute), or entity did not notify service provider/data owner",
        counter_arguments=[
            "Notice delayed beyond unreasonable period (e.g., 6+ months after discovery absent law enforcement delay or valid investigation complexity)",
            "Notice content inadequate (did not describe breach, PI types, remedial steps, or consumer advice as required by state statute)",
            "AG notification not provided despite breach affecting 500+ state residents (California, New York, Illinois, Florida, etc. require AG notice at 500+ threshold)",
            "Risk-of-harm analysis not documented or unreasonable (in states allowing risk-of-harm exception, entity must show reasonable investigation and determination that breach unlikely to cause harm; speculative or conclusory assessment insufficient)",
            "Substitute notice used when not justified (substitute allowed only if cost exceeds threshold, insufficient contact info, or large affected population; entity cannot use substitute to avoid mail cost when contact info available)",
            "Service provider failed to notify data owner/licensee (most states impose duty on service provider discovering breach of data maintained for third party)"
        ],
        resolution_strategy="Implement incident response plan addressing breach detection, investigation, notification decision, and execution. Upon discovering potential breach: (1) Contain incident and preserve evidence. (2) Investigate to determine if unauthorized acquisition occurred, what PI involved, how many individuals affected, by state. (3) Determine notification trigger: most states require notice regardless of risk; some (Ohio, Wisconsin, Colorado) allow risk-of-harm analysis to forgo notice if unlikely to harm (document analysis if relying on exception). (4) Determine timing: without unreasonable delay per most states; comply with state-specific deadlines (e.g., Colorado 30 days). Delay only for law enforcement coordination or scope determination (document reason and duration). (5) Draft notice including required elements per affected states: description of incident, types of PI, date or estimated date, remedial steps taken, contact information, consumer advice (credit report, fraud alert, FTC), toll-free numbers for credit bureaus. (6) Deliver notice by written mail (preferred), email (if prior email relationship and E-SIGN compliant), or substitute (if cost > $250K-500K, population > 500K, or insufficient contact info). (7) Notify state attorneys general if threshold met (typically 500+ residents; check each state: California, New York, Florida, Illinois, Massachusetts, etc.). (8) Notify consumer reporting agencies if 1,000+ individuals per FCRA Section 1681c-2. (9) If service provider: immediately notify data owner/licensee. (10) Document all decisions, timelines, analyses, and notices for regulatory defense. Consult state-specific statutes for each affected state; consider retaining breach counsel for multi-state incidents.",
        entity_scope="Entities owning, licensing, or maintaining personal information of residents of states with breach notification laws (all 50 states, DC, territories)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="State breach notification statutes (50 states + DC); Cal. Civ. Code 1798.82; N.Y. Gen. Bus. Law 899-aa; Tex. Bus. & Com. Code 521.053; NCSL compilation"
    ),
    DoctrineBlock(
        topic="GDPR Data Protection Impact Assessment (DPIA) Requirements",
        keywords=["dpia", "data protection impact assessment", "article 35", "high risk processing", "privacy impact assessment", "gdpr"],
        conclusion_template=[
            "GDPR Article 35 requires controller to carry out Data Protection Impact Assessment (DPIA) where type of processing (in particular using new technologies) is likely to result in high risk to rights and freedoms of natural persons, considering nature, scope, context, and purposes.",
            "Article 35(3) specifies DPIA required for: (a) systematic and extensive automated processing including profiling with legal/similarly significant effects, (b) large-scale processing of special categories (Article 9) or criminal data (Article 10), (c) systematic monitoring of publicly accessible area on large scale (e.g., CCTV).",
            "DPIA must contain at least: description of processing and purposes, assessment of necessity and proportionality, assessment of risks to data subjects, and measures to address risks and demonstrate compliance. Supervisory authority must be consulted if DPIA indicates high risk and controller cannot sufficiently mitigate (Article 36)."
        ],
        reasoning_framework="""GDPR Article 35(1): where type of processing is likely to result in high risk to rights and freedoms of natural persons, controller shall, prior to processing, carry out assessment of impact of envisaged processing operations on protection of personal data (Data Protection Impact Assessment). Article 35(3) lists processing operations requiring DPIA: (a) systematic and extensive evaluation of personal aspects relating to natural persons based on automated processing, including profiling, on which decisions are based that produce legal effects concerning natural person or similarly significantly affect natural person, (b) processing on large scale of special categories of data (Article 9: racial/ethnic origin, political opinions, religious/philosophical beliefs, trade union membership, genetic data, biometric data for unique identification, health data, sex life/sexual orientation) or personal data relating to criminal convictions and offences (Article 10), (c) systematic monitoring of publicly accessible area on large scale. Article 35(4): supervisory authority shall establish and make public list of processing operations subject to DPIA requirement (blacklist). Article 35(5): supervisory authority may establish and make public list of processing operations for which DPIA not required (whitelist). Article 29 Working Party (now EDPB) Guidelines on DPIA (WP248 rev.01, 2017) provide criteria for high risk: (1) evaluation or scoring (including profiling and predicting), (2) automated decision-making with legal or similarly significant effect, (3) systematic monitoring, (4) sensitive data or data of highly personal nature (special categories, criminal data, location, financial, children, employee, communications content), (5) large-scale processing (consider number of data subjects, volume of data, duration, geographical extent), (6) matching or combining datasets (e.g., from different sources or purposes), (7) data concerning vulnerable data subjects (children, employees, elderly, mentally ill, asylum seekers), (8) innovative use or applying technological/organizational solutions (e.g., AI, IoT, facial recognition), (9) processing itself prevents data subjects from exercising right or using service/contract (e.g., screening for credit, insurance, employment). Two or more criteria typically indicates DPIA required. Article 35(7) minimum content: (a) systematic description of envisaged processing operations and purposes of processing, including where applicable legitimate interests pursued by controller, (b) assessment of necessity and proportionality of processing operations in relation to purposes, (c) assessment of risks to rights and freedoms of data subjects, (d) measures envisaged to address risks, including safeguards, security measures, mechanisms to ensure protection of personal data and demonstrate compliance with GDPR, taking into account rights and legitimate interests of data subjects and other persons concerned. DPIA process: controller must (1) consult DPO if designated (Article 35(2)), (2) seek views of data subjects or their representatives where appropriate (Article 35(9)), (3) assess whether single DPIA may address set of similar processing operations (Article 35(1)), (4) conduct DPIA before processing begins (Article 35(1), (10)), (5) review DPIA when change in risk (Article 35(11)). If DPIA indicates processing would result in high risk in absence of measures to mitigate risk, and controller cannot sufficiently mitigate, controller must consult supervisory authority prior to processing (Article 36(1)). Supervisory authority may provide written advice within 8 weeks (extendable 6 weeks if complex), and may use investigative/corrective powers including ban on processing (Article 36(2), (5)).""",
        key_factors=[
            "Processing is likely to result in high risk to rights and freedoms (assess using Article 29 WP criteria: two+ factors = likely high risk)",
            "Processing falls within Article 35(3) categories: automated decision-making with legal/similar effect, large-scale special categories/criminal data, or systematic monitoring of public area",
            "Processing involves new technologies, innovative use, or particularly intrusive methods",
            "DPIA conducted before processing begins",
            "DPIA contains required elements: description of processing/purposes, necessity/proportionality assessment, risk assessment, mitigation measures",
            "DPO consulted if designated; data subjects' views sought where appropriate",
            "If residual high risk cannot be mitigated: supervisory authority consulted per Article 36 prior to processing"
        ],
        primary_authority=[
            "GDPR Article 35 (Data Protection Impact Assessment)",
            "GDPR Article 36 (Prior consultation with supervisory authority)",
            "Article 29 Working Party Guidelines on DPIA (WP248 rev.01, 2017)",
            "EDPB Guidelines 3/2019 on processing of personal data through video devices (DPIA for video surveillance)",
            "ICO guidance on DPIAs",
            "CNIL DPIA methodology"
        ],
        burden_holder="Controller to determine if DPIA required, conduct DPIA with required elements, consult DPO and data subjects where appropriate, mitigate risks, and consult supervisory authority if high residual risk",
        adversary_position="Supervisory authority alleges controller failed to conduct DPIA where required (processing met Article 35(3) criteria or WP248 high-risk criteria but no DPIA performed), DPIA inadequate (missing required elements: no necessity/proportionality assessment, superficial risk assessment, no mitigation measures), DPIA not conducted before processing began (retrospective DPIA insufficient), controller did not consult supervisory authority despite high residual risk, or controller did not review DPIA when processing changed",
        counter_arguments=[
            "DPIA not conducted but processing met Article 35(3) criteria (e.g., large-scale health data processing, systematic CCTV monitoring, automated credit scoring with legal effect) or two+ WP248 factors (violation of Article 35(1))",
            "DPIA inadequate: did not include systematic description of processing and purposes, did not assess necessity and proportionality (could purposes be achieved with less intrusive processing?), did not assess risks to data subjects (likelihood and severity of harm), did not describe mitigation measures and safeguards (Article 35(7) required elements missing)",
            "DPIA conducted after processing began (Article 35(1) requires prior to processing; retrospective DPIA does not satisfy obligation)",
            "DPIA showed high residual risk but controller did not consult supervisory authority before processing (Article 36(1) mandatory consultation if high risk cannot be mitigated)",
            "DPIA not reviewed when processing significantly changed (Article 35(11): DPIA must be reviewed when change in risk represented by processing operations)"
        ],
        resolution_strategy="Before beginning new processing or significantly changing existing processing, assess whether DPIA required using Article 35(3) criteria and WP248 factors. If processing involves two+ WP248 factors (evaluation/scoring, automated decisions, systematic monitoring, sensitive data, large scale, dataset matching, vulnerable subjects, innovative tech, prevents exercise of rights) or fits Article 35(3) (automated legal/significant decisions, large-scale special categories/criminal data, systematic public monitoring), conduct DPIA. Consult supervisory authority's blacklist/whitelist if published. Conduct DPIA with required elements per Article 35(7): (1) Systematic description: describe processing operations, data flows, purposes, lawful basis, legitimate interests if applicable, retention periods, recipients. (2) Necessity and proportionality: assess whether processing necessary to achieve purposes and whether less intrusive means available (data minimization, pseudonymization, anonymization). (3) Risk assessment: identify risks to data subjects' rights and freedoms (unauthorized access, accidental loss, discrimination, reputational harm, loss of confidentiality); assess likelihood and severity (WP248 methodology: consider origin, nature, particularity, severity of risk; rate likelihood and severity low/medium/high). (4) Mitigation measures: describe safeguards, security, organizational measures to reduce risk to acceptable level (encryption, access controls, MFA, monitoring, DPO oversight, training, contracts with processors, breach response, rights mechanisms). Consult DPO if designated. Seek data subjects' views where appropriate (e.g., representative survey, consultation with advocacy groups). If residual risk remains high after mitigation, consult supervisory authority per Article 36 before processing. Document DPIA, including date, participants, risk scores, mitigation measures, and consultation records. Review DPIA at least annually or when processing changes materially. Use DPIA templates from supervisory authorities (ICO, CNIL, EDPB) to ensure completeness.",
        entity_scope="Controllers subject to GDPR conducting processing likely to result in high risk to data subjects",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="GDPR Articles 35, 36; Article 29 WP Guidelines WP248 rev.01; EDPB Guidelines 3/2019"
    ),
    DoctrineBlock(
        topic="GDPR Cross-Border Data Transfers and Standard Contractual Clauses",
        keywords=["gdpr cross-border transfer", "third country", "adequacy decision", "standard contractual clauses", "scc", "article 44", "article 45", "article 46", "schrems ii"],
        conclusion_template=[
            "GDPR Chapter V (Articles 44-50) restricts transfer of personal data to third countries (outside EEA) or international organizations. Transfer permitted only if controller/processor complies with Chapter V conditions, ensuring level of protection of natural persons not undermined.",
            "Article 45: transfer permitted to third country/international organization if European Commission has decided country ensures adequate level of protection (adequacy decision). Current adequate countries: UK, Switzerland, Andorra, Argentina, Canada (commercial), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, South Korea, Uruguay, and EU-US Data Privacy Framework participants (2023).",
            "Article 46: absent adequacy decision, transfer permitted if controller/processor provides appropriate safeguards (Standard Contractual Clauses, Binding Corporate Rules, approved codes/certifications) and data subjects have enforceable rights and effective remedies. Post-Schrems II, supplementary measures required if third country law/practice impairs SCC safeguards."
        ],
        reasoning_framework="""GDPR Article 44: transfer of personal data undergoing processing or intended for processing after transfer to third country (country outside EEA) or international organization permitted only if conditions in Chapter V met, ensuring level of protection of natural persons guaranteed by GDPR not undermined (including onward transfers). Article 45 adequacy decision: Commission may decide third country, territory, sector, or international organization ensures adequate level of protection considering rule of law, human rights, data protection legislation, independent supervisory authority, international commitments (Article 45(1), (2)). If adequacy decision, transfer may take place without specific authorization (Article 45(1)). Commission monitors adequacy decisions and may amend/repeal if protection no longer ensured (Article 45(3), (5)). Current adequacy decisions (as of 2024): Argentina, Canada (commercial organizations subject to PIPEDA), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, United Kingdom, Uruguay, Andorra, and entities self-certifying under EU-US Data Privacy Framework (DPF, adopted July 2023 replacing invalidated Privacy Shield per Executive Order 14086 and implementing regulations). Article 46 appropriate safeguards: absent adequacy decision, controller/processor may transfer if appropriate safeguards provided and enforceable data subject rights and effective legal remedies available (Article 46(1)). Appropriate safeguards include: (a) legally binding and enforceable instrument between public authorities, (b) Binding Corporate Rules (BCRs) per Article 47, (c) Standard Contractual Clauses (SCCs) adopted by Commission per Article 46(2)(c) (Commission Implementing Decision (EU) 2021/914 for controller-to-controller and controller-to-processor; Decision 2010/87/EU for processor-to-processor repealed and replaced by 2021 SCCs), (d) SCCs adopted by supervisory authority and approved by Commission per Article 46(2)(d), (e) approved code of conduct per Article 40 with binding enforceable commitments in third country, (f) approved certification mechanism per Article 42 with binding enforceable commitments, (g) contractual clauses authorized by supervisory authority per Article 46(3)(a), (h) administrative arrangements authorized by supervisory authority per Article 46(3)(b). Standard Contractual Clauses (SCCs): Commission Decision 2021/914 (effective September 27, 2021) provides modular SCCs for controller-to-controller (Module One), controller-to-processor (Module Two), processor-to-processor (Module Three), and processor-to-controller (Module Four). SCCs include: mandatory clauses (cannot be modified), optional clauses (parties select applicable modules and options), Annex I (parties, contact details, description of transfer, competent supervisory authority), Annex II (technical and organizational measures), Annex III (sub-processors if Module Two or Three). Clause 14 of SCCs: parties and data subjects can invoke and enforce SCCs as third-party beneficiaries. Data exporter and data subjects can seek remedies against data importer in courts of EU Member State where data exporter established; data subjects can seek remedies in courts of Member State where they have habitual residence (Clause 18). Schrems II (CJEU C-311/18, July 16, 2020): Court invalidated EU-US Privacy Shield, held SCCs remain valid mechanism but requires case-by-case assessment of third country law and practice (focusing on government surveillance and data subject redress) and supplementary measures if law/practice impairs SCC safeguards. EDPB Recommendations 01/2020 on supplementary measures (November 2020, updated June 2021) provide six-step roadmap: (1) know your transfers (map data flows), (2) verify transfer tool (SCCs, BCRs, etc.), (3) assess third country law (does law allow government access that would be unlawful under GDPR? e.g., FISA 702, EO 12333 in US), (4) identify and adopt supplementary measures if needed (technical: encryption, pseudonymization, splitting/multi-party processing, trusted execution environments; organizational: contractual clauses on government requests, transparency commitments, data minimization, only transfers to countries with strong rule of law; legal: challenging unlawful requests), (5) take formal procedural steps (supervisory authority approval if required), (6) re-evaluate at appropriate intervals. If effective supplementary measures cannot be implemented and third country law impairs SCC guarantees, transfer must be suspended or terminated (EDPB Recommendations, Schrems II).""",
        key_factors=[
            "Transfer involves personal data moving from EEA to third country (non-EEA) or international organization",
            "If adequacy decision exists for destination country/entity (e.g., UK, Switzerland, Japan, DPF participants): transfer permitted without additional safeguards (Article 45)",
            "If no adequacy decision: appropriate safeguards required (SCCs, BCRs, approved codes/certifications per Article 46)",
            "If using SCCs: 2021 Commission SCCs (Decision 2021/914) executed, appropriate module selected, Annexes completed, technical/organizational measures documented",
            "Post-Schrems II: transfer impact assessment (TIA) conducted, assessing third country law (government access, surveillance, redress) and practice affecting SCC safeguards",
            "If third country law impairs SCCs: supplementary measures implemented (encryption, pseudonymization, contractual commitments, trusted execution) or transfer suspended",
            "Data subjects have enforceable rights and effective remedies (Clause 14 third-party beneficiary, Clause 18 jurisdiction)"
        ],
        primary_authority=[
            "GDPR Chapter V Articles 44-50 (international transfers)",
            "GDPR Article 45 (adequacy decisions)",
            "GDPR Article 46 (appropriate safeguards)",
            "Commission Implementing Decision (EU) 2021/914 (Standard Contractual Clauses)",
            "CJEU C-311/18 Data Protection Commissioner v. Facebook Ireland and Schrems (Schrems II, July 16, 2020)",
            "EDPB Recommendations 01/2020 on measures supplementing transfer tools (version 2.0, June 2021)",
            "EDPB Recommendations 02/2020 on European Essential Guarantees for surveillance measures"
        ],
        burden_holder="Controller/processor to verify adequacy decision or implement appropriate safeguards (SCCs, BCRs), conduct transfer impact assessment post-Schrems II, implement supplementary measures if third country law impairs safeguards, suspend transfer if effective measures unavailable",
        adversary_position="Supervisory authority or data subject challenges transfer, alleges no adequacy decision and no appropriate safeguards (no SCCs or invalid clauses), SCCs used but no transfer impact assessment conducted, TIA inadequate (superficial review, did not assess third country surveillance laws like FISA 702 or equivalent), no supplementary measures despite third country law impairing SCC safeguards, or supplementary measures ineffective (e.g., claimed encryption but keys accessible to government, or contractual commitment to resist unlawful access but third country law prohibits such resistance)",
        counter_arguments=[
            "Transfer to non-adequate third country without SCCs or other Article 46 safeguard (Article 46(1) violation)",
            "SCCs used but not 2021 Commission SCCs (old 2001/2004/2010 SCCs must be replaced by September 27, 2022 per Decision 2021/914 Article 4; continued use of old SCCs after deadline invalid)",
            "SCCs executed but Annexes incomplete (Annex I missing transfer description or competent SA, Annex II missing technical/organizational measures, Annex III missing sub-processor list if Module Two/Three)",
            "No transfer impact assessment conducted post-Schrems II (EDPB Recommendations 01/2020 require case-by-case assessment of third country law; failure to assess is non-compliance with Article 46 requirement that safeguards ensure essentially equivalent protection)",
            "TIA conducted but superficial (did not analyze surveillance laws: e.g., US transfers must assess FISA 702, EO 12333, CLOUD Act, PATRIOT Act; China transfers must assess National Intelligence Law, Cybersecurity Law, Data Security Law; Russia transfers must assess SORM, data localization; conclusion that no risk without analyzing laws is insufficient)",
            "Third country law identified as impairing SCCs but no supplementary measures (e.g., data transferred to US cloud provider subject to FISA 702, no encryption, no pseudonymization, no contractual clauses, no trusted execution environment; EDPB Recommendations require supplementary measures or suspension)",
            "Supplementary measures claimed but ineffective (encryption but keys stored in same jurisdiction accessible by government, contractual clause requiring importer to resist unlawful access but third country law criminalizes resistance or imposes gag order, pseudonymization but re-identification possible with auxiliary data in third country)"
        ],
        resolution_strategy="Map all cross-border data transfers (know your transfers: identify third countries, data categories, recipients, purposes per EDPB step 1). For each transfer, determine if destination country has adequacy decision (check European Commission adequacy website: if yes, transfer permitted under Article 45 without additional measures). If no adequacy, select appropriate Article 46 safeguard: typically Standard Contractual Clauses (SCCs) per Commission Decision 2021/914. Execute 2021 SCCs with third country recipient: select appropriate module (Module One: C2C, Module Two: C2P, Module Three: P2P, Module Four: P2C), complete Annexes (Annex I: parties, transfer description, competent SA; Annex II: technical/organizational measures including encryption, access controls, logging, breach response; Annex III: sub-processor list if applicable). Conduct Transfer Impact Assessment (TIA) per Schrems II and EDPB Recommendations 01/2020 step 3: research third country law (government access to data, surveillance, mandatory disclosure, lack of redress); assess whether law/practice in third country would impair Article 46 safeguards (compare to European Essential Guarantees per EDPB 02/2020: necessity, proportionality, independent oversight, effective remedies); consider recipient's sector (telecom/internet providers more likely subject to surveillance than non-electronic sectors), data sensitivity, and likelihood of government access. If TIA reveals third country law impairs SCC safeguards (e.g., FISA 702 allows US government access without GDPR-equivalent safeguards; China National Intelligence Law requires cooperation with intelligence; Russia SORM allows warrantless intercept), identify and implement supplementary measures per EDPB Recommendations step 4: technical (end-to-end encryption with EU-held keys, pseudonymization/anonymization, trusted execution environments, multi-party computation, split processing where sensitive operations remain in EEA), organizational (data minimization to reduce transfer scope, contractual clauses requiring importer to challenge unlawful access requests and notify exporter, transparency reporting, selection of providers in jurisdictions with stronger rule of law), legal (challenge unlawful requests, assess case law on government access). If no effective supplementary measures can be implemented (e.g., government access is lawful under third country law and cannot be technically prevented, or encrypted data must be decrypted in third country for processing), suspend or terminate transfer per Schrems II and EDPB Recommendations. Document TIA, supplementary measures, and reassessment schedule. Re-evaluate transfers at appropriate intervals (at least annually or when third country law changes, new surveillance legislation enacted, or court decisions affect legal landscape). Consult supervisory authority guidance (ICO International Transfers Risk Assessment, CNIL Transfer Tools, EDPB case studies) and consider using EDPB-endorsed supplementary measures examples.",
        entity_scope="Controllers and processors subject to GDPR transferring personal data to third countries or international organizations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="GDPR Articles 44-46; Commission Decision 2021/914; CJEU C-311/18 Schrems II; EDPB Recommendations 01/2020, 02/2020"
    ),
]

METRICS = {
    "queries_handled": 0,
    "doctrines_triggered": {},
    "avg_latency_ms": 0.0,
    "cache_hits": 0,
    "deep_analysis_invoked": 0
}


def normalize_term(term: str) -> str:
    term_map = {
        "ccpa": ["california consumer privacy act", "cal civ code 1798", "1798.100"],
        "cpra": ["california privacy rights act", "1798.121", "sensitive personal information"],
        "gdpr": ["general data protection regulation", "article 6", "article 15", "article 17", "article 35", "article 45", "article 46"],
        "coppa": ["children's online privacy protection act", "15 usc 6502", "verifiable parental consent"],
        "ferpa": ["family educational rights and privacy act", "20 usc 1232g", "education records"],
        "glba": ["gramm-leach-bliley", "15 usc 6801", "financial institution", "safeguards rule", "privacy rule"],
        "ftc": ["federal trade commission", "section 5", "unfair practices", "deceptive practices"],
        "breach notification": ["data breach", "security breach", "unauthorized acquisition"],
        "dpia": ["data protection impact assessment", "article 35", "high risk processing"],
        "cross-border transfer": ["third country", "adequacy decision", "standard contractual clauses", "scc", "schrems"],
        "consent": ["freely given", "specific", "informed", "unambiguous", "opt-in"],
        "legitimate interest": ["balancing test", "article 6(1)(f)", "necessity", "proportionality"],
        "right to erasure": ["right to be forgotten", "article 17", "deletion"],
        "data portability": ["article 20", "machine-readable format"],
        "dpo": ["data protection officer", "article 37"]
    }
    normalized = term.lower().strip()
    for canonical, variants in term_map.items():
        if normalized in variants or any(v in normalized for v in variants):
            return canonical
    return normalized


def compute_determinism_hash(query: str, response: str, mode: str) -> str:
    payload = f"{query}|{response}|{mode}".encode('utf-8')
    return hashlib.sha256(payload).hexdigest()[:16]


def doctrine_cache_lookup(query: str) -> Tuple[Optional[str], List[str]]:
    query_lower = query.lower()
    keywords_found = []
    triggered_doctrines = []
    for doctrine in DOCTRINES:
        for kw in doctrine.keywords:
            if kw.lower() in query_lower:
                keywords_found.append(kw)
                if doctrine.topic not in triggered_doctrines:
                    triggered_doctrines.append(doctrine.topic)
    if not triggered_doctrines:
        return None, []
    selected_doctrine = None
    for topic in triggered_doctrines:
        selected_doctrine = next((d for d in DOCTRINES if d.topic == topic), None)
        if selected_doctrine:
            break
    if not selected_doctrine:
        return None, []
    METRICS["cache_hits"] += 1
    response_text = " ".join(selected_doctrine.conclusion_template)
    response_text += f"\n\nKey Factors: {'; '.join(selected_doctrine.key_factors[:3])}"
    return response_text, triggered_doctrines


def semantic_retrieval(query: str) -> Tuple[str, List[str]]:
    query_terms = set(normalize_term(t) for t in query.lower().split())
    scores = []
    for doctrine in DOCTRINES:
        doctrine_terms = set(normalize_term(k) for k in doctrine.keywords)
        overlap = len(query_terms.intersection(doctrine_terms))
        scores.append((overlap, doctrine))
    scores.sort(reverse=True, key=lambda x: x[0])
    if scores and scores[0][0] > 0:
        top_doctrine = scores[0][1]
        response = f"Semantic retrieval matched: {top_doctrine.topic}.\n\n"
        response += top_doctrine.reasoning_framework[:800]
        response += f"\n\nPrimary Authority: {'; '.join(top_doctrine.primary_authority[:3])}"
        return response, [top_doctrine.topic]
    return "No strong semantic match found. Falling back to deep analysis.", []


def deep_analysis(query: str, mode: ResponseMode) -> Tuple[str, List[str]]:
    METRICS["deep_analysis_invoked"] += 1
    all_topics = [d.topic for d in DOCTRINES[:5]]
    response = f"Deep analysis mode invoked for query: '{query[:100]}'...\n\n"
    response += "This query requires synthesis across multiple privacy regulatory frameworks. "
    response += f"Relevant doctrines: {', '.join(all_topics)}. "
    response += "Consider applicability of CCPA/CPRA consumer rights, GDPR lawful basis and data subject rights, "
    response += "COPPA parental consent, FERPA education records exceptions, GLBA financial privacy, "
    response += "FTC Section 5 unfair/deceptive enforcement, state breach notification laws, "
    response += "GDPR DPIA requirements, and cross-border transfer mechanisms. "
    if mode == ResponseMode.DEFENSE:
        response += "For audit defense: document lawful basis, maintain records of processing activities (Article 30), "
        response += "conduct and document DPIA if high-risk, implement privacy by design/default, "
        response += "ensure vendor contracts contain required safeguards (GDPR Article 28, CCPA service provider definition), "
        response += "honor data subject rights within statutory timelines, maintain breach response plan."
    elif mode == ResponseMode.MEMO:
        response += "Memorandum-level detail: Analyze jurisdiction (which laws apply based on entity location, data subject location, targeting). "
        response += "Assess lawful basis under GDPR Article 6(1) or CCPA business purpose. "
        response += "Evaluate consent validity if relying on consent (GDPR Article 4(11): freely given, specific, informed, unambiguous; CCPA opt-in for sale/sharing/SPI). "
        response += "For transfers: determine if adequacy decision exists, otherwise execute SCCs and conduct transfer impact assessment per Schrems II. "
        response += "For breach scenarios: apply state notification statutes (all 50 states), assess PI definition, timing (without unreasonable delay), content, and AG notification thresholds. "
        response += "Cite primary authority and document compliance steps."
    else:
        response += "Fast mode summary: Comply with applicable privacy laws, obtain valid consent or other lawful basis, honor rights requests, implement reasonable security, notify breaches timely, conduct DPIA if high-risk."
    return response, all_topics


def three_layer_response(query: str, mode: ResponseMode) -> Tuple[str, List[str], float]:
    start = time.time()
    cache_result, cache_doctrines = doctrine_cache_lookup(query)
    if cache_result:
        latency = (time.time() - start) * 1000
        logger.info(f"Cache hit for query: {query[:50]}, latency {latency:.2f}ms")
        return cache_result, cache_doctrines, latency
    semantic_result, semantic_doctrines = semantic_retrieval(query)
    if semantic_doctrines:
        latency = (time.time() - start) * 1000
        logger.info(f"Semantic retrieval for query: {query[:50]}, latency {latency:.2f}ms")
        return semantic_result, semantic_doctrines, latency
    deep_result, deep_doctrines = deep_analysis(query, mode)
    latency = (time.time() - start) * 1000
    logger.info(f"Deep analysis for query: {query[:50]}, latency {latency:.2f}ms")
    return deep_result, deep_doctrines, latency


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINES)} doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down. Metrics: {METRICS}")


app = FastAPI(title=ENGINE_NAME, version=VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="operational",
        engine=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINES),
        uptime_seconds=time.time() - START_TIME
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    METRICS["queries_handled"] += 1
    response_text, doctrines_triggered, latency_ms = three_layer_response(req.query, req.mode)
    for d in doctrines_triggered:
        METRICS["doctrines_triggered"][d] = METRICS["doctrines_triggered"].get(d, 0) + 1
    total_latencies = METRICS["avg_latency_ms"] * (METRICS["queries_handled"] - 1)
    METRICS["avg_latency_ms"] = (total_latencies + latency_ms) / METRICS["queries_handled"]
    det_hash = compute_determinism_hash(req.query, response_text, req.mode.value)
    confidence = ConfidenceLevel.DEFENSIBLE.value
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": req.query,
        "mode": req.mode.value,
        "doctrines": doctrines_triggered,
        "latency_ms": latency_ms,
        "hash": det_hash
    }
    AUDIT_LOG.append(audit_entry)
    logger.info(f"Query processed: {req.query[:50]}, mode={req.mode.value}, latency={latency_ms:.2f}ms, doctrines={doctrines_triggered}")
    return QueryResponse(
        engine=ENGINE_ID,
        version=VERSION,
        query=req.query,
        response=response_text,
        mode=req.mode.value,
        confidence=confidence,
        doctrines_triggered=doctrines_triggered,
        latency_ms=round(latency_ms, 2),
        determinism_hash=det_hash,
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/metrics")
async def metrics():
    return {
        "engine": ENGINE_ID,
        "version": VERSION,
        "metrics": METRICS,
        "uptime_seconds": time.time() - START_TIME
    }


@app.get("/doctrines")
async def list_doctrines():
    return {
        "engine": ENGINE_ID,
        "version": VERSION,
        "doctrines": [{"topic": d.topic, "keywords": d.keywords, "confidence": d.confidence.value} for d in DOCTRINES]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
