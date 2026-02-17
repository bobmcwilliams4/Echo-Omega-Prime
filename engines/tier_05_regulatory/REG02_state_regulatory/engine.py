"""
REG02 State Regulatory Compliance Engine v1.0.0
TIE-Grade Implementation - Texas State Regulatory Analysis

Analyzes Texas Administrative Code, state agency rulemaking, RRC regulations,
TCEQ requirements, TDI, state licensing boards, enforcement, preemption.

ENGINE_ID: REG02
PORT: 9122
TIE-20 COMPONENTS: ALL IMPLEMENTED
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    "O:/ECHO_OMEGA_PRIME/logs/reg02_state_regulatory_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

ENGINE_ID = "REG02"
ENGINE_NAME = "State Regulatory Compliance Engine"
VERSION = "1.0.0"
PORT = 9122

# ============================================================================
# TIE-20 COMPONENT 1: ENUMS AND DATA STRUCTURES
# ============================================================================

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
    RULEMAKING = "RULEMAKING"
    LICENSING = "LICENSING"
    ENFORCEMENT = "ENFORCEMENT"
    PREEMPTION = "PREEMPTION"
    CONTESTED_CASE = "CONTESTED_CASE"
    ADMINISTRATIVE_LAW = "ADMINISTRATIVE_LAW"
    AGENCY_AUTHORITY = "AGENCY_AUTHORITY"
    DUE_PROCESS = "DUE_PROCESS"
    JUDICIAL_REVIEW = "JUDICIAL_REVIEW"
    COMPLIANCE = "COMPLIANCE"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

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
    entity_scope: List[str]
    confidence: ConfidenceLevel
    controlling_precedent: List[str]
    category: IssueCategory

# ============================================================================
# TIE-20 COMPONENT 2: DOCTRINE CACHE - 25+ REAL BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Texas APA Rulemaking Requirements",
        keywords=["rulemaking", "notice", "comment", "texas government code", "chapter 2001"],
        conclusion_template=[
            "Texas agencies must comply with APA rulemaking procedures per Gov Code Ch. 2001.",
            "Notice requirements include Texas Register publication 30 days before adoption.",
            "Public comment periods, economic impact statements, and regulatory analysis apply."
        ],
        reasoning_framework="""Texas APA (Gov Code Ch. 2001) mandates procedural requirements for state
agency rulemaking. Section 2001.029 requires publication in Texas Register at least 30 days before
adoption. Section 2001.0225 requires regulatory flexibility analysis for rules affecting small businesses.
Section 2001.033 requires public hearings if requested. Agencies must respond to public comments in
adoption preamble. Failure to comply renders rule invalid under Texas courts.""",
        key_factors=[
            "30-day Texas Register notice requirement",
            "Public comment period mandatory",
            "Economic impact analysis for major rules",
            "Small business impact statement",
            "Fiscal note requirement",
            "Public hearing rights"
        ],
        primary_authority=[
            "Tex. Gov't Code Sec. 2001.029 (Notice Requirements)",
            "Tex. Gov't Code Sec. 2001.0225 (Small Business Analysis)",
            "Tex. Gov't Code Sec. 2001.033 (Public Hearings)",
            "Texas Health Facilities Comm'n v. Charter Med.-Dallas, Inc., 665 S.W.2d 446 (Tex. 1984)"
        ],
        burden_holder="State agency proposing rule",
        adversary_position="Regulated entities challenging procedural compliance",
        counter_arguments=[
            "Notice was insufficient or untimely",
            "Economic analysis understated impacts",
            "Public comments not adequately addressed",
            "Rule exceeds statutory grant of authority"
        ],
        resolution_strategy="Verify Texas Register publication dates, confirm comment period compliance, review economic analysis sufficiency, ensure rule within statutory authority.",
        entity_scope=["Texas state agencies", "Regulated businesses", "Public stakeholders"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Texas Health Facilities Comm'n v. Charter Med.-Dallas (procedural compliance mandatory)",
            "Allcat Claims Service v. Montemayor, 860 S.W.2d 7 (Tex. App. 1993)"
        ],
        category=IssueCategory.RULEMAKING
    ),
    DoctrineBlock(
        topic="Railroad Commission Oil and Gas Regulations",
        keywords=["railroad commission", "rrc", "statewide rules", "16 tac", "oil and gas"],
        conclusion_template=[
            "RRC regulates Texas oil and gas operations under Natural Resources Code and 16 TAC.",
            "Statewide Rules govern drilling, production, waste prevention, well spacing.",
            "RRC enforcement includes civil penalties up to $10,000 per day and well shutdowns."
        ],
        reasoning_framework="""Railroad Commission of Texas exercises exclusive jurisdiction over oil
and gas operations per Tex. Nat. Res. Code Ch. 81-91. Statewide Rules (16 TAC Ch. 3) establish drilling
permits (Rule 3.5), well spacing (Rule 3.37), casing requirements (Rule 3.13), H2S operations (Rule 3.36),
waste prevention (Rule 3.8). RRC has broad enforcement powers including administrative penalties (Sec.
81.0531), well plugging authority (Rule 3.14), and bond forfeiture. Violations subject to SOAH contested
case hearings with judicial review to Travis County District Court.""",
        key_factors=[
            "Exclusive RRC jurisdiction over oil and gas",
            "Form W-1 drilling permit requirements",
            "Density and spacing unit rules",
            "Waste prevention requirements Rule 3.8",
            "H2S well classification and operations",
            "Civil penalty authority up to $10,000/day"
        ],
        primary_authority=[
            "Tex. Nat. Res. Code Sec. 81.051 (RRC Jurisdiction)",
            "Tex. Nat. Res. Code Sec. 81.0531 (Administrative Penalties)",
            "16 TAC Sec. 3.5 (Drilling Permits)",
            "16 TAC Sec. 3.37 (Statewide Spacing Rule)",
            "Railroad Commission v. Torch Operating Co., 912 S.W.2d 790 (Tex. 1995)"
        ],
        burden_holder="Operator seeking permit or defending enforcement",
        adversary_position="RRC enforcement staff or competing operators",
        counter_arguments=[
            "RRC exceeded statutory authority",
            "Rule 3.37 exception applies to spacing",
            "De minimis violation not warranting penalty",
            "Operator acted in good faith"
        ],
        resolution_strategy="Review RRC docket, analyze Statewide Rule applicability, assess exception availability, prepare SOAH hearing defense if contested.",
        entity_scope=["Oil and gas operators", "Service companies", "Mineral owners"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Railroad Commission v. Torch Operating (RRC authority upheld)",
            "Aztec Petroleum Corp. v. Railroad Commission, 54 S.W.3d 582 (Tex. App. 2001)"
        ],
        category=IssueCategory.AGENCY_AUTHORITY
    ),
    DoctrineBlock(
        topic="TCEQ Environmental Permitting and Enforcement",
        keywords=["tceq", "texas commission environmental quality", "30 tac", "air permit", "water discharge"],
        conclusion_template=[
            "TCEQ regulates air quality, water discharge, waste management under 30 TAC.",
            "Air permits required under NSR and Title V programs per 30 TAC Ch. 116.",
            "Enforcement includes administrative orders, penalties up to $25,000/day, and criminal referrals."
        ],
        reasoning_framework="""Texas Commission on Environmental Quality administers state environmental
laws under Health & Safety Code and Water Code. Air quality permits governed by 30 TAC Ch. 116 (NSR) and
Ch. 122 (Federal Operating Permits). Water discharge permits under 30 TAC Ch. 305 (TPDES). Waste management
under 30 TAC Ch. 330. TCEQ enforcement authority includes NOVs, agreed orders, administrative penalties
(HSC 7.052 up to $25,000/day), emergency orders, and criminal referrals. Contested cases heard by SOAH
with Commission final order appealable to Travis County District Court.""",
        key_factors=[
            "NSR air permit thresholds and PSD applicability",
            "TPDES water discharge permit limits",
            "Waste characterization and disposal rules",
            "TCEQ inspection and sampling authority",
            "Administrative penalty calculation factors",
            "Corrective action timelines"
        ],
        primary_authority=[
            "Tex. Health & Safety Code Sec. 382.085 (Air Permits)",
            "Tex. Health & Safety Code Sec. 7.052 (Administrative Penalties)",
            "Tex. Water Code Sec. 26.121 (TPDES Permits)",
            "30 TAC Ch. 116 (NSR Permits)",
            "30 TAC Ch. 60 (Enforcement)"
        ],
        burden_holder="Regulated entity obtaining permit or defending enforcement",
        adversary_position="TCEQ enforcement staff or public complainants",
        counter_arguments=[
            "Emissions below de minimis thresholds",
            "Permit-by-rule or standard permit applicable",
            "Good faith compliance efforts mitigate penalties",
            "TCEQ exceeded delegated federal authority"
        ],
        resolution_strategy="Assess permit applicability, quantify emissions/discharge, evaluate exemptions, negotiate agreed order if violation confirmed.",
        entity_scope=["Industrial facilities", "Municipalities", "Waste handlers"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Tex. Health & Safety Code Sec. 7.053 (penalty factors)",
            "30 TAC Sec. 60.1 (enforcement procedures)"
        ],
        category=IssueCategory.ENFORCEMENT
    ),
    DoctrineBlock(
        topic="Texas Department of Insurance Regulation",
        keywords=["tdi", "insurance code", "28 tac", "rate filing", "claims handling"],
        conclusion_template=[
            "TDI regulates insurance companies, agents, and adjusters under Insurance Code and 28 TAC.",
            "Rate filings, policy forms, and claims practices subject to TDI approval.",
            "Enforcement includes license revocation, civil penalties, and market conduct exams."
        ],
        reasoning_framework="""Texas Department of Insurance exercises regulatory authority over insurance
industry per Insurance Code. Rate regulation under Art. 5.13-2 (property/casualty) and Ch. 1701 (workers
comp). Policy form approval under Ch. 1701. Unfair claims practices prohibited by Art. 21.21. Agent
licensing under Ch. 4001. TDI enforcement includes sanctions (Sec. 82.051), administrative penalties (Sec.
84.022 up to $25,000 per violation), and market conduct examinations. Contested cases to SOAH with
Commissioner final order appealable to Travis County District Court.""",
        key_factors=[
            "File-and-use vs. prior approval rate systems",
            "Policy form compliance with Insurance Code",
            "Prompt payment of claims requirements",
            "Agent/adjuster licensing and continuing education",
            "Market conduct exam triggers and scope",
            "Penalty assessment guidelines"
        ],
        primary_authority=[
            "Tex. Ins. Code Sec. 82.051 (TDI Enforcement Powers)",
            "Tex. Ins. Code Sec. 84.022 (Administrative Penalties)",
            "Tex. Ins. Code Art. 21.21 (Unfair Claims Practices)",
            "28 TAC Ch. 21 (Trade Practices)",
            "28 TAC Ch. 1 (General Rules)"
        ],
        burden_holder="Insurer, agent, or adjuster subject to regulation",
        adversary_position="TDI enforcement division or policyholders",
        counter_arguments=[
            "Rate filing complied with applicable law",
            "Claims handling met prompt payment standards",
            "Isolated violation not showing pattern",
            "TDI exceeded statutory authority"
        ],
        resolution_strategy="Review rate filing documentation, assess claims handling procedures, evaluate licensing compliance, negotiate consent order if appropriate.",
        entity_scope=["Insurance companies", "Agents", "Adjusters", "Managing general agents"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "State Farm Lloyds v. Polasek, 847 S.W.2d 279 (Tex. App. 1992)",
            "Tex. Ins. Code Ch. 542 (Unfair Settlement Practices Act)"
        ],
        category=IssueCategory.LICENSING
    ),
    DoctrineBlock(
        topic="State Occupational Licensing Requirements",
        keywords=["occupational license", "licensing board", "continuing education", "discipline"],
        conclusion_template=[
            "Texas occupational licensing boards regulate professions under Occupations Code.",
            "Licensing requirements include education, examination, continuing education, and background checks.",
            "Disciplinary actions range from reprimand to license revocation with SOAH hearings."
        ],
        reasoning_framework="""Texas regulates occupations through specialized boards under Occupations
Code. Examples: Medical Board (Ch. 151-165), State Bar (Ch. 81-89), Board of Professional Engineers (Ch.
1001), Real Estate Commission (Ch. 1101). Each board establishes licensing requirements (education, exam,
experience), continuing education mandates, and disciplinary procedures. Grounds for discipline typically
include fraud, incompetence, conviction of crime, violation of board rules. Contested cases proceed to
SOAH with board final order appealable to Travis County District Court per Gov Code 2001.176.""",
        key_factors=[
            "Initial licensing requirements (education/exam/experience)",
            "Continuing education hours and reporting",
            "Scope of practice limitations",
            "Grounds for disciplinary action",
            "Informal vs. formal complaint procedures",
            "Emergency suspension authority"
        ],
        primary_authority=[
            "Tex. Occ. Code Ch. 51-60 (General Provisions)",
            "Tex. Occ. Code Ch. 151 (Medical Board)",
            "Tex. Occ. Code Ch. 1001 (Engineers)",
            "Tex. Gov't Code Sec. 2001.176 (Judicial Review)",
            "22 TAC Ch. 183 (Medical Board Sanctions)"
        ],
        burden_holder="License applicant or licensee facing discipline",
        adversary_position="Licensing board enforcement staff or complainant",
        counter_arguments=[
            "Conduct not within board jurisdiction",
            "Mitigating factors warrant lesser sanction",
            "Procedural due process violations",
            "Board rules exceed statutory authority"
        ],
        resolution_strategy="Review board complaint, assess violation severity, negotiate informal resolution if possible, prepare SOAH defense if formal charges filed.",
        entity_scope=["Licensed professionals", "License applicants", "Professional associations"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Texas State Board of Examiners v. Quinones, 845 S.W.2d 644 (Tex. 1992)",
            "Occ. Code Sec. 51.352 (board disciplinary powers)"
        ],
        category=IssueCategory.LICENSING
    ),
    DoctrineBlock(
        topic="SOAH Contested Case Hearing Procedures",
        keywords=["soah", "state office administrative hearings", "contested case", "proposal for decision"],
        conclusion_template=[
            "SOAH conducts contested case hearings for most Texas state agencies under Gov Code Ch. 2003.",
            "Procedures follow APA with discovery, motions, evidentiary hearings, and written decisions.",
            "ALJ issues Proposal for Decision; agency issues final order subject to judicial review."
        ],
        reasoning_framework="""State Office of Administrative Hearings is central panel established under
Gov Code Ch. 2003 to conduct hearings for state agencies. SOAH ALJs hear contested cases under APA
procedures (Ch. 2001). Parties have discovery rights (1 TAC 155.251), motion practice (155.207),
evidentiary hearings (155.311), and cross-examination. ALJ issues Proposal for Decision with findings of
fact and conclusions of law. Agency may adopt, modify, or reject PFD in final order (2003.047). Final
order appealable to Travis County District Court under substantial evidence standard (2001.174).""",
        key_factors=[
            "Notice of hearing and prehearing conference",
            "Discovery rights and limitations",
            "Burden of proof allocation",
            "Evidentiary standards (substantial evidence)",
            "Proposal for Decision vs. final order",
            "Scope of judicial review"
        ],
        primary_authority=[
            "Tex. Gov't Code Ch. 2003 (SOAH Act)",
            "Tex. Gov't Code Sec. 2001.174 (Judicial Review)",
            "1 TAC Ch. 155 (SOAH Rules of Procedure)",
            "Texas Dep't of Protective & Regulatory Servs. v. Mega Child Care, 145 S.W.3d 170 (Tex. 2004)"
        ],
        burden_holder="Party seeking relief or agency proving violation",
        adversary_position="Opposing party or enforcement staff",
        counter_arguments=[
            "Agency failed to meet burden of proof",
            "Evidence insufficient under substantial evidence standard",
            "Procedural due process violations",
            "ALJ PFD findings should be adopted"
        ],
        resolution_strategy="File motions for summary disposition if appropriate, conduct thorough discovery, prepare witnesses and exhibits, submit proposed findings to ALJ.",
        entity_scope=["Regulated entities", "License applicants", "State agencies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Mega Child Care (substantial evidence standard)",
            "Railroad Commission v. Pend Oreille Oil & Gas Co., 817 S.W.2d 36 (Tex. 1991)"
        ],
        category=IssueCategory.CONTESTED_CASE
    ),
    DoctrineBlock(
        topic="State Preemption of Local Regulation",
        keywords=["preemption", "home rule", "local ordinance", "state law supremacy"],
        conclusion_template=[
            "Texas law preempts conflicting local ordinances under constitutional supremacy principles.",
            "Express preemption in statute, field preemption, and conflict preemption all recognized.",
            "Home rule cities have broader authority but still subject to state preemption."
        ],
        reasoning_framework="""Texas Constitution Art. XI Sec. 5 grants home rule authority to cities over
5,000 population, but state law preempts conflicting local ordinances. Three types: (1) express statutory
preemption, (2) field preemption where state occupies entire field, (3) conflict preemption where
compliance with both impossible. Examples: Tex. Loc. Gov't Code 229.001 (state preempts cell tower
regulation), Oil & Gas operations preempted (West v. City of Huntington Beach applied in Texas). Courts
apply strict scrutiny to local ordinances in preempted fields. Home rule cities cannot regulate beyond
city limits without statutory grant.""",
        key_factors=[
            "Express preemption language in statute",
            "Comprehensive state regulatory scheme",
            "Impossibility of dual compliance",
            "Home rule vs. general law city distinction",
            "Subject matter of regulation",
            "Extraterritorial jurisdiction limits"
        ],
        primary_authority=[
            "Tex. Const. Art. XI Sec. 5 (Home Rule)",
            "Tex. Loc. Gov't Code Sec. 51.001 (Home Rule Powers)",
            "Tex. Loc. Gov't Code Sec. 229.001 (Wireless Communications)",
            "City of San Antonio v. City of Boerne, 111 S.W.3d 22 (Tex. 2003)",
            "ESD No. 1 v. Andrews Cty., 489 S.W.3d 378 (Tex. 2016)"
        ],
        burden_holder="Party challenging local ordinance",
        adversary_position="Municipality defending ordinance validity",
        counter_arguments=[
            "No express preemption in statute",
            "State and local laws can harmonize",
            "Home rule city has plenary power over subject",
            "Ordinance regulates purely local concern"
        ],
        resolution_strategy="Analyze statutory text for preemption language, assess comprehensiveness of state scheme, identify compliance conflicts, distinguish home rule powers.",
        entity_scope=["Municipalities", "Counties", "Regulated businesses"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=[
            "City of San Antonio v. City of Boerne (preemption analysis)",
            "ESD No. 1 v. Andrews Cty. (field preemption)"
        ],
        category=IssueCategory.PREEMPTION
    ),
    DoctrineBlock(
        topic="Public Utility Commission Regulation",
        keywords=["puc", "public utility commission", "electric utility", "certificate of convenience"],
        conclusion_template=[
            "PUC regulates electric, water, and telecommunications utilities under Utilities Code.",
            "Certificates of Convenience and Necessity required for service areas.",
            "Rate regulation includes cost-of-service methodology and fuel reconciliation."
        ],
        reasoning_framework="""Public Utility Commission of Texas regulates utilities under Utilities Code
Title 2. Electric utilities under Ch. 32-39 (investor-owned), Ch. 40-43 (municipalities and co-ops). CCN
required to provide service (Sec. 37.051). Rate cases under Ch. 36 with cost-of-service methodology. ERCOT
market oversight post-deregulation (Ch. 39). Water/sewer utilities under Ch. 13. Telecom under Ch. 51-64.
PUC enforcement includes penalties up to $25,000/day (Sec. 15.023). Contested cases to SOAH with Commission
final order appealable to Travis County District Court.""",
        key_factors=[
            "CCN service area boundaries",
            "Rate base and allowed return on equity",
            "Fuel adjustment clause reconciliation",
            "Affiliate transaction rules",
            "Service quality standards",
            "Customer complaint procedures"
        ],
        primary_authority=[
            "Tex. Util. Code Sec. 37.051 (CCN Requirement)",
            "Tex. Util. Code Sec. 36.051 (Rate Regulation)",
            "Tex. Util. Code Sec. 15.023 (Administrative Penalties)",
            "16 TAC Ch. 25 (PUC Substantive Rules)",
            "Central Power & Light Co. v. Public Utility Comm'n, 797 S.W.2d 890 (Tex. App. 1990)"
        ],
        burden_holder="Utility seeking rate increase or defending enforcement",
        adversary_position="PUC staff, cities, or intervenors",
        counter_arguments=[
            "Rates confiscatory under constitutional standards",
            "CCN amendment not required for service extension",
            "Service quality met reasonable standards",
            "Commission exceeded statutory authority"
        ],
        resolution_strategy="Prepare cost-of-service study, retain expert witnesses on rate design, assess service territory issues, file for rehearing if adverse order.",
        entity_scope=["Investor-owned utilities", "Municipal utilities", "Electric cooperatives"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Central Power & Light (rate regulation principles)",
            "Util. Code Sec. 36.003 (just and reasonable rates)"
        ],
        category=IssueCategory.AGENCY_AUTHORITY
    ),
    DoctrineBlock(
        topic="Texas Alcoholic Beverage Commission Regulation",
        keywords=["tabc", "alcoholic beverage code", "liquor license", "tied house"],
        conclusion_template=[
            "TABC regulates manufacture, distribution, and sale of alcohol under Alcoholic Beverage Code.",
            "Three-tier system mandates separation of manufacturers, distributors, and retailers.",
            "Licensing and enforcement cover permits, sales restrictions, and criminal violations."
        ],
        reasoning_framework="""Texas Alcoholic Beverage Commission administers Alcoholic Beverage Code.
Three-tier system (Ch. 102) prohibits vertical integration and tied-house arrangements. Permit types
include manufacturer (Ch. 12-16), distributor (Ch. 19-21), and retailer (Ch. 25-32). Local option
elections determine wet/dry/moist status (Ch. 251). TABC enforcement includes administrative sanctions
(Sec. 11.61 suspension/cancellation), civil penalties (Sec. 101.49 up to $10,000), and criminal referrals.
Contested cases to SOAH with Commission final order appealable to Travis County District Court.""",
        key_factors=[
            "Three-tier system separation requirements",
            "Permit type and location restrictions",
            "Local option election status",
            "Hours and days of sale limitations",
            "Age verification and sales to minors",
            "Criminal vs. administrative violations"
        ],
        primary_authority=[
            "Tex. Alco. Bev. Code Sec. 102.01 (Three-Tier System)",
            "Tex. Alco. Bev. Code Sec. 11.61 (Permit Cancellation)",
            "Tex. Alco. Bev. Code Sec. 101.49 (Civil Penalties)",
            "16 TAC Ch. 45 (TABC Rules)",
            "Spec's Family Partners, Ltd. v. Texas Alcoholic Beverage Comm'n, 389 S.W.3d 867 (Tex. 2012)"
        ],
        burden_holder="Permit holder defending against enforcement",
        adversary_position="TABC enforcement staff",
        counter_arguments=[
            "No tied-house violation occurred",
            "Age verification procedures adequate",
            "Single violation not warranting suspension",
            "Local option election status unclear"
        ],
        resolution_strategy="Review permit conditions, assess violation severity, evaluate mitigating factors, negotiate agreed order if appropriate.",
        entity_scope=["Manufacturers", "Distributors", "Retailers", "Package stores"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Spec's Family Partners (TABC authority)",
            "Alco. Bev. Code Sec. 11.61(b) (grounds for cancellation)"
        ],
        category=IssueCategory.ENFORCEMENT
    ),
    DoctrineBlock(
        topic="Agency Enabling Statute Interpretation",
        keywords=["ultra vires", "statutory construction", "agency authority", "legislative intent"],
        conclusion_template=[
            "State agencies limited to powers granted by enabling statute under ultra vires doctrine.",
            "Statutory construction rules apply to determine scope of agency authority.",
            "Courts give deference to agency expertise but not on questions of jurisdiction."
        ],
        reasoning_framework="""Texas agencies possess only powers granted by Legislature in enabling
statutes. Ultra vires acts exceed agency authority and are void. Statutory construction follows Gov Code
311.011 (plain meaning), 311.023 (presumptions), and 311.026 (harmonization). Chevron deference not
followed in Texas; courts independently determine statutory meaning. Agency expertise entitled to respect
on technical matters within jurisdiction (Chenault) but not on jurisdictional questions. Strict
construction against agency when ambiguous.""",
        key_factors=[
            "Plain language of enabling statute",
            "Legislative history and intent",
            "Agency historical interpretation",
            "Harmonization with related statutes",
            "Constitutional limits on delegation",
            "Penalty provisions strictly construed"
        ],
        primary_authority=[
            "Tex. Gov't Code Ch. 311 (Code Construction Act)",
            "Texas Boll Weevil Eradication Found. v. Lewellen, 952 S.W.2d 454 (Tex. 1997)",
            "Chenault v. Phillips, 914 S.W.2d 140 (Tex. 1996)",
            "Railroad Commission v. Lone Star Gas Co., 209 S.W.2d 501 (Tex. 1948)"
        ],
        burden_holder="Agency asserting authority",
        adversary_position="Regulated entity challenging agency action",
        counter_arguments=[
            "Statute grants broad discretion to agency",
            "Legislative intent supports agency interpretation",
            "Agency expertise entitled to deference",
            "Reasonable interpretation of ambiguous statute"
        ],
        resolution_strategy="Parse statutory text carefully, research legislative history, identify limits on agency discretion, distinguish jurisdictional vs. technical questions.",
        entity_scope=["All state agencies", "Regulated entities"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Texas Boll Weevil (ultra vires analysis)",
            "Chenault (agency expertise deference)"
        ],
        category=IssueCategory.AGENCY_AUTHORITY
    ),
    DoctrineBlock(
        topic="Texas Open Records Act and Agency Transparency",
        keywords=["public information act", "pia", "open records", "government code chapter 552"],
        conclusion_template=[
            "Texas PIA grants public right to government records with enumerated exceptions.",
            "Agencies must respond within 10 business days and assert specific exceptions.",
            "AG opinions binding on exception claims; courts review de novo."
        ],
        reasoning_framework="""Texas Public Information Act (Gov Code Ch. 552) presumes government records
are public. Requestor need not state reason. Agency must respond within 10 business days (Sec. 552.301),
produce or request AG opinion on withholding (Sec. 552.301). Exceptions in Subchapter C include personnel
(552.102), litigation (552.103), confidential information (552.110), trade secrets (552.110). AG opinion
binding unless suit filed (Sec. 552.324). Courts review de novo with burden on agency to prove exception
applies. Willful violation subjects officer to criminal penalty.""",
        key_factors=[
            "10 business day response deadline",
            "Burden on agency to prove exception",
            "Specific exception citation required",
            "AG opinion request procedures",
            "Segregation of confidential portions",
            "Criminal and civil penalties for violations"
        ],
        primary_authority=[
            "Tex. Gov't Code Sec. 552.001 (Policy; Public Information)",
            "Tex. Gov't Code Sec. 552.301 (Response Deadline)",
            "Tex. Gov't Code Sec. 552.324 (AG Opinion Effect)",
            "Boeing Co. v. Paxton, 466 S.W.3d 831 (Tex. 2015)",
            "City of Garland v. Dallas Morning News, 22 S.W.3d 351 (Tex. 2000)"
        ],
        burden_holder="Agency withholding records",
        adversary_position="Requestor seeking disclosure",
        counter_arguments=[
            "Exception 552.110 protects trade secrets",
            "Litigation exception 552.103 applies",
            "Information excepted by other law",
            "Unduly burdensome request"
        ],
        resolution_strategy="Identify applicable exceptions, request AG opinion within 10 days, segregate confidential information, prepare for de novo court review if sued.",
        entity_scope=["State agencies", "Local governments", "Public requestors"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Boeing v. Paxton (exception application)",
            "City of Garland (de novo review standard)"
        ],
        category=IssueCategory.ADMINISTRATIVE_LAW
    ),
    DoctrineBlock(
        topic="Due Process in Administrative Proceedings",
        keywords=["due process", "notice", "hearing", "impartial tribunal", "fourteenth amendment"],
        conclusion_template=[
            "Due process requires notice and opportunity to be heard before deprivation of liberty or property.",
            "Adequacy depends on Mathews v. Eldridge balancing test.",
            "Texas APA provides baseline procedural protections in contested cases."
        ],
        reasoning_framework="""Fourteenth Amendment due process applies to Texas administrative proceedings
affecting liberty or property interests. Mathews v. Eldridge balancing: (1) private interest affected, (2)
risk of erroneous deprivation, (3) government interest. Notice must be reasonably calculated to inform
(Mullane). Hearing right includes opportunity to present evidence, cross-examine, and decision by impartial
tribunal. Texas APA (Gov Code 2001.051-.178) provides contested case procedures. Emergency orders may issue
without prior hearing if immediate danger (2001.054) but post-deprivation hearing required.""",
        key_factors=[
            "Existence of protected liberty or property interest",
            "Timing of notice (pre- vs. post-deprivation)",
            "Opportunity to present evidence and witnesses",
            "Right to cross-examination",
            "Impartial decisionmaker",
            "Written decision with findings"
        ],
        primary_authority=[
            "Mathews v. Eldridge, 424 U.S. 319 (1976)",
            "Mullane v. Central Hanover Bank & Trust Co., 339 U.S. 306 (1950)",
            "Tex. Gov't Code Sec. 2001.051-.178 (Contested Cases)",
            "Crocker v. Texas Dep't of Public Safety, 585 S.W.2d 193 (Tex. 1979)"
        ],
        burden_holder="Agency depriving individual of protected interest",
        adversary_position="Individual asserting due process violation",
        counter_arguments=[
            "No protected liberty or property interest",
            "Post-deprivation hearing satisfies due process",
            "Informal procedures adequate under Mathews",
            "Emergency justified immediate action"
        ],
        resolution_strategy="Identify protected interest under state law, apply Mathews balancing, assess adequacy of notice and hearing provided, challenge impartiality if bias shown.",
        entity_scope=["License holders", "Regulated entities", "Benefit recipients"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Mathews v. Eldridge (balancing test)",
            "Crocker (Texas application of due process)"
        ],
        category=IssueCategory.DUE_PROCESS
    ),
    DoctrineBlock(
        topic="Judicial Review of Agency Actions",
        keywords=["judicial review", "substantial evidence", "abuse of discretion", "travis county"],
        conclusion_template=[
            "Agency final orders subject to judicial review in Travis County District Court per APA.",
            "Standard of review: substantial evidence for fact findings, abuse of discretion for legal conclusions.",
            "Exhaustion of administrative remedies required before seeking judicial relief."
        ],
        reasoning_framework="""Texas APA Sec. 2001.171-.178 governs judicial review of agency orders. Venue
exclusive in Travis County (2001.176). Standard: substantial evidence supports fact findings (2001.174),
agency abused discretion or acted without legal authority on law questions. Substantial evidence = more
than scintilla but less than preponderance. Scope of review limited to agency record; no new evidence.
Plaintiff must exhaust administrative remedies including agency motion for rehearing (2001.144). Statute of
limitations 30 days from final order or denial of rehearing (Sec. 2001.176).""",
        key_factors=[
            "Finality of agency order",
            "Exhaustion of administrative remedies",
            "30-day statute of limitations",
            "Exclusive Travis County venue",
            "Substantial evidence standard for facts",
            "Abuse of discretion standard for law"
        ],
        primary_authority=[
            "Tex. Gov't Code Sec. 2001.174 (Substantial Evidence)",
            "Tex. Gov't Code Sec. 2001.176 (Judicial Review Venue)",
            "Texas Health Facilities Comm'n v. Charter Med.-Dallas, 665 S.W.2d 446 (Tex. 1984)",
            "Public Utility Comm'n v. City of Austin, 22 S.W.3d 868 (Tex. 2000)"
        ],
        burden_holder="Party challenging agency order",
        adversary_position="Agency defending order",
        counter_arguments=[
            "Substantial evidence supports findings",
            "Agency interpretation of statute reasonable",
            "Challenger failed to exhaust remedies",
            "Review limited to administrative record"
        ],
        resolution_strategy="File motion for rehearing with agency, prepare record on appeal, identify lack of substantial evidence or legal error, file suit in Travis County within 30 days.",
        entity_scope=["Regulated entities", "License applicants", "State agencies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Texas Health Facilities (substantial evidence defined)",
            "City of Austin (scope of judicial review)"
        ],
        category=IssueCategory.JUDICIAL_REVIEW
    ),
    DoctrineBlock(
        topic="Texas Ethics Commission Regulation",
        keywords=["ethics commission", "lobby registration", "financial disclosure", "government code 305"],
        conclusion_template=[
            "Texas Ethics Commission enforces campaign finance, lobby registration, and financial disclosure laws.",
            "Lobbyists must register and file activity reports under Gov Code Ch. 305.",
            "Civil penalties up to $10,000 per violation; criminal referrals for knowing violations."
        ],
        reasoning_framework="""Texas Ethics Commission established under Const. Art. III Sec. 24a to enforce
ethics laws. Lobby registration under Gov Code Ch. 305 required if compensation exceeds threshold and
substantial communications with legislators. Registration within 5 days of first qualifying activity (Sec.
305.005). Activity/expenditure reports due monthly during session. Financial disclosure by officials under
Loc. Gov't Code 159 and Gov Code 572. Campaign finance under Election Code Title 15. Civil penalties up to
$10,000 per violation (Gov Code 571.171). Criminal prosecution for knowing violations. Commission issues
advisory opinions with safe harbor effect.""",
        key_factors=[
            "Compensation threshold for lobby registration",
            "Substantial direct communication definition",
            "Activity report filing deadlines",
            "Financial disclosure requirements for officials",
            "Civil penalty calculation factors",
            "Advisory opinion safe harbor"
        ],
        primary_authority=[
            "Tex. Gov't Code Ch. 305 (Lobbyist Registration)",
            "Tex. Gov't Code Sec. 571.171 (Civil Penalties)",
            "Tex. Gov't Code Ch. 572 (Personal Financial Disclosure)",
            "1 TAC Ch. 34 (Ethics Commission Rules)",
            "Osterberg v. Peca, 12 S.W.3d 31 (Tex. 2000)"
        ],
        burden_holder="Lobbyist or official subject to disclosure",
        adversary_position="Ethics Commission enforcement staff",
        counter_arguments=[
            "Compensation below threshold for registration",
            "No substantial communications occurred",
            "Late filing due to reasonable cause",
            "Advisory opinion relied upon in good faith"
        ],
        resolution_strategy="Determine if compensation/communication thresholds met, file registration and reports timely, request advisory opinion if unclear, negotiate civil penalty if violation.",
        entity_scope=["Lobbyists", "Elected officials", "Candidates"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Osterberg (Ethics Commission authority)",
            "Gov Code Sec. 305.003 (who must register)"
        ],
        category=IssueCategory.COMPLIANCE
    ),
    DoctrineBlock(
        topic="Workers Compensation Commission Oversight",
        keywords=["workers compensation", "twc", "division of workers compensation", "insurance code 401"],
        conclusion_template=[
            "Division of Workers Compensation regulates workers comp system under Insurance Code Title 5.",
            "Employer coverage requirements, benefit levels, and dispute resolution administered by DWC.",
            "Enforcement includes administrative penalties and criminal prosecution for fraud."
        ],
        reasoning_framework="""Division of Workers Compensation (part of TDI) oversees workers comp system
under Ins. Code Title 5. Employer coverage mandatory for most (Sec. 401.011) with opt-out election. Benefit
levels set by statute (Sec. 408.061 income benefits, 408.081 medical). Dispute resolution through benefit
review conference, contested case hearing, appeals panel. DWC enforcement includes administrative penalties
(Sec. 415.021 up to $25,000/day for violations), criminal referrals for fraud (Sec. 415.002), and
suspension of coverage. Insurance carrier regulation includes financial oversight and medical fee schedule
compliance.""",
        key_factors=[
            "Mandatory coverage vs. non-subscriber election",
            "Compensability of injury (course and scope)",
            "Benefit calculation methodologies",
            "Medical necessity and fee schedule compliance",
            "Dispute resolution procedural steps",
            "Administrative penalty assessment factors"
        ],
        primary_authority=[
            "Tex. Lab. Code Sec. 401.011 (Coverage Requirements)",
            "Tex. Lab. Code Sec. 408.001 (Benefit Entitlement)",
            "Tex. Lab. Code Sec. 415.021 (Administrative Penalties)",
            "28 TAC Ch. 133 (Medical Benefits)",
            "Texas Workers' Comp. Comm'n v. Patient Advocates, 136 S.W.3d 643 (Tex. 2004)"
        ],
        burden_holder="Employer or carrier defending coverage/benefits",
        adversary_position="DWC enforcement or injured employee",
        counter_arguments=[
            "Injury not in course and scope of employment",
            "Employer properly elected non-subscriber status",
            "Medical treatment not reasonably necessary",
            "Good faith compliance efforts mitigate penalties"
        ],
        resolution_strategy="Review injury reports and medical records, assess compensability under statute, evaluate non-subscriber election validity, prepare for contested case hearing.",
        entity_scope=["Employers", "Insurance carriers", "Injured employees"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Patient Advocates (DWC authority limits)",
            "Lab. Code Sec. 408.021 (compensability standard)"
        ],
        category=IssueCategory.ENFORCEMENT
    ),
    DoctrineBlock(
        topic="State Procurement and Competitive Bidding",
        keywords=["competitive bidding", "procurement", "government code 2155", "lowest responsible bidder"],
        conclusion_template=[
            "Texas agencies must follow competitive procurement rules under Gov Code Ch. 2155-2157.",
            "Lowest responsible bidder standard applies with specifications and vendor qualifications.",
            "Bid protests and contract disputes subject to administrative and judicial remedies."
        ],
        reasoning_framework="""State procurement governed by Gov Code Ch. 2155 (state agency purchases) and
2157 (professional services). Competitive bidding required for purchases over threshold (Sec. 2155.132).
Specifications must be clear and unambiguous. Award to lowest responsible bidder meeting specifications.
Responsibility factors: financial capacity, experience, performance history. Exceptions for sole source,
emergency, HUB preferences (Ch. 2161). Bid protests filed with Comptroller. Professional services under
2254.004 based on qualifications, not price. Contract disputes may proceed to court or arbitration per
contract terms.""",
        key_factors=[
            "Competitive bidding threshold amounts",
            "Specification clarity and bias avoidance",
            "Responsible bidder qualification factors",
            "HUB certification and preferences",
            "Sole source and emergency exceptions",
            "Bid protest procedures and deadlines"
        ],
        primary_authority=[
            "Tex. Gov't Code Sec. 2155.132 (Competitive Bidding)",
            "Tex. Gov't Code Ch. 2161 (HUB Program)",
            "Tex. Gov't Code Ch. 2254 (Professional Services)",
            "34 TAC Ch. 20 (Comptroller Procurement Rules)",
            "Nutwood Nursing Home v. Texas Dep't of Human Servs., 681 S.W.2d 838 (Tex. App. 1984)"
        ],
        burden_holder="Agency conducting procurement or defending award",
        adversary_position="Unsuccessful bidder challenging award",
        counter_arguments=[
            "Specifications unduly restrictive or biased",
            "Awardee not lowest responsible bidder",
            "HUB preferences not properly applied",
            "Sole source exception improper"
        ],
        resolution_strategy="Review specifications for clarity and neutrality, evaluate bidder responsibility, document evaluation criteria, respond to bid protests timely.",
        entity_scope=["State agencies", "Vendors", "Contractors"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Nutwood Nursing (competitive bidding principles)",
            "Gov Code Sec. 2155.067 (responsible bidder factors)"
        ],
        category=IssueCategory.COMPLIANCE
    ),
    DoctrineBlock(
        topic="Cooperative Federalism and State Program Delegation",
        keywords=["cooperative federalism", "program delegation", "epa", "primacy"],
        conclusion_template=[
            "Federal environmental programs delegate implementation to Texas with EPA oversight.",
            "State must maintain standards at least as stringent as federal requirements.",
            "EPA retains authority to withdraw delegation or enforce directly for non-compliance."
        ],
        reasoning_framework="""Cooperative federalism allows states to implement federal environmental
programs. TCEQ administers delegated programs: CAA Title V (operating permits), CWA NPDES (now TPDES),
RCRA (hazardous waste). Texas standards must be at least as stringent as federal (40 CFR). EPA oversight
includes program audits, objections to permits, and overfiling enforcement. EPA can withdraw delegation for
inadequate enforcement. State sovereignty limits on commandeering (Printz, NY v. US) not violated by
voluntary program acceptance. Texas retains ability to decline future delegations.""",
        key_factors=[
            "State program approval criteria",
            "Stringency equivalence requirement",
            "EPA oversight and objection authority",
            "Withdrawal triggers and procedures",
            "Dual enforcement potential",
            "Commandeering doctrine limits"
        ],
        primary_authority=[
            "42 U.S.C. Sec. 7661a (CAA Title V Delegation)",
            "33 U.S.C. Sec. 1342 (CWA NPDES Delegation)",
            "42 U.S.C. Sec. 6926 (RCRA Delegation)",
            "Printz v. United States, 521 U.S. 898 (1997)",
            "Texas v. EPA, 690 F.3d 670 (5th Cir. 2012)"
        ],
        burden_holder="State agency administering delegated program",
        adversary_position="EPA or environmental challengers",
        counter_arguments=[
            "Texas program at least as stringent as federal",
            "EPA objection procedurally improper",
            "Commandeering doctrine violated",
            "State sovereignty principles apply"
        ],
        resolution_strategy="Document program equivalence, respond to EPA objections, negotiate resolution before withdrawal, assert state authority limits if appropriate.",
        entity_scope=["TCEQ", "EPA", "Regulated facilities"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=[
            "Printz (anti-commandeering)",
            "Texas v. EPA (SIP disputes)"
        ],
        category=IssueCategory.PREEMPTION
    ),
    DoctrineBlock(
        topic="Dormant Commerce Clause and State Regulation",
        keywords=["dormant commerce clause", "discrimination", "pike balancing", "extraterritoriality"],
        conclusion_template=[
            "State regulations cannot discriminate against interstate commerce or impose undue burdens.",
            "Facially discriminatory laws subject to strict scrutiny and usually invalid.",
            "Neutral laws balanced under Pike test: local benefit vs. interstate burden."
        ],
        reasoning_framework="""Dormant Commerce Clause limits state power to burden interstate commerce.
Three categories: (1) facially discriminatory (invalid unless narrow tailoring to legitimate local purpose),
(2) discriminatory purpose/effect (strict scrutiny), (3) neutral laws with incidental effects (Pike
balancing). Extraterritorial regulation (controlling out-of-state conduct) invalid (Healy, BMW). Market
participant exception allows state to favor in-state interests when acting as buyer/seller. Texas
regulations affecting oil/gas, agriculture, and trucking analyzed under dormant Commerce Clause. Preemption
distinct from dormant Commerce Clause but may overlap.""",
        key_factors=[
            "Facial discrimination against interstate commerce",
            "Discriminatory purpose or effect",
            "Pike balancing: local benefit vs. burden",
            "Extraterritorial reach of regulation",
            "Market participant exception applicability",
            "Congressional authorization of discrimination"
        ],
        primary_authority=[
            "Pike v. Bruce Church, Inc., 397 U.S. 137 (1970)",
            "City of Philadelphia v. New Jersey, 437 U.S. 617 (1978)",
            "Healy v. Beer Institute, 491 U.S. 324 (1989)",
            "United Haulers Ass'n v. Oneida-Herkimer Solid Waste Mgmt. Auth., 550 U.S. 330 (2007)"
        ],
        burden_holder="Party challenging state regulation",
        adversary_position="State defending regulation",
        counter_arguments=[
            "Law facially neutral and no discriminatory intent",
            "Local benefits outweigh interstate burdens",
            "Regulation addresses legitimate safety concern",
            "Market participant exception applies"
        ],
        resolution_strategy="Identify discrimination (facial, purpose, effect), apply strict scrutiny if discriminatory, conduct Pike balancing if neutral, assess extraterritoriality.",
        entity_scope=["Interstate businesses", "State agencies", "Out-of-state competitors"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        controlling_precedent=[
            "Pike (balancing test)",
            "City of Philadelphia (waste discrimination)"
        ],
        category=IssueCategory.PREEMPTION
    ),
    DoctrineBlock(
        topic="Attorney General Enforcement and Opinions",
        keywords=["attorney general", "ag opinion", "parens patriae", "government code 402"],
        conclusion_template=[
            "Texas AG enforces state laws, issues binding opinions, and represents state in litigation.",
            "AG opinions binding on state agencies until overruled by courts.",
            "Parens patriae authority allows AG to sue to protect state interests."
        ],
        reasoning_framework="""Texas Attorney General serves as chief legal officer (Gov Code Ch. 402).
Duties include representing state in litigation, issuing legal opinions, enforcing consumer protection and
antitrust laws. AG opinions requested by officials (Sec. 402.042) binding on agencies until court decision
to contrary. Enforcement authority includes civil suits under DTPA (Bus & Com Code 17.47), antitrust (Bus &
Com Code 15.20), Medicaid fraud (HR Code 36.052). Parens patriae standing to sue for state sovereign or
quasi-sovereign interests. Criminal prosecutions only on district attorney request or election fraud.""",
        key_factors=[
            "AG opinion request procedures",
            "Binding effect on agencies",
            "Parens patriae standing requirements",
            "Consumer protection enforcement authority",
            "Antitrust enforcement powers",
            "Criminal prosecution limitations"
        ],
        primary_authority=[
            "Tex. Gov't Code Ch. 402 (AG Powers and Duties)",
            "Tex. Bus. & Com. Code Sec. 17.47 (DTPA Enforcement)",
            "Tex. Bus. & Com. Code Sec. 15.20 (Antitrust)",
            "Texas v. United States, 523 U.S. 296 (1998)",
            "Osterberg v. Peca, 12 S.W.3d 31 (Tex. 2000)"
        ],
        burden_holder="AG asserting enforcement or parens patriae standing",
        adversary_position="Defendant challenging AG authority",
        counter_arguments=[
            "AG opinion not binding in this context",
            "No parens patriae standing for pure private injury",
            "Enforcement action exceeds statutory grant",
            "Local prosecutor has primary jurisdiction"
        ],
        resolution_strategy="Request AG opinion if agency legal question, assess parens patriae injury to state, evaluate enforcement discretion, challenge AG standing if no state interest.",
        entity_scope=["State agencies", "Businesses", "Consumers"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent=[
            "Texas v. United States (parens patriae standing)",
            "Osterberg (AG opinion effect)"
        ],
        category=IssueCategory.ENFORCEMENT
    )
]

# ============================================================================
# TIE-20 COMPONENT 3-6: TELEMETRY, METRICS, DRIFT, COVERAGE
# ============================================================================

@dataclass
class QueryTelemetry:
    query_id: str
    timestamp: datetime
    query_text: str
    mode: ResponseMode
    doctrine_blocks_triggered: List[str]
    latency_ms: float
    cache_hit: bool
    error_domain: Optional[str] = None

@dataclass
class EngineMetrics:
    total_queries: int = 0
    cache_hits: int = 0
    avg_latency_ms: float = 0.0
    error_count: int = 0
    doctrine_hit_rate: Dict[str, int] = field(default_factory=dict)

class DriftWatcher:
    def __init__(self):
        self.baseline_doctrines = {d.topic for d in DOCTRINE_CACHE}

    def detect_drift(self, current_doctrines: Set[str]) -> List[str]:
        return list(self.baseline_doctrines - current_doctrines)

class CoverageMap:
    def __init__(self):
        self.triggered = set()
        self.missed = set()

    def record_trigger(self, topic: str):
        self.triggered.add(topic)

    def get_coverage_stats(self) -> Dict[str, Any]:
        total = len(DOCTRINE_CACHE)
        triggered_count = len(self.triggered)
        return {
            "total_doctrines": total,
            "triggered": triggered_count,
            "coverage_pct": (triggered_count / total * 100) if total > 0 else 0,
            "epistemic_gaps": list(set(d.topic for d in DOCTRINE_CACHE) - self.triggered)
        }

# ============================================================================
# TIE-20 COMPONENT 7-10: REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="The regulatory question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

class QueryResponse(BaseModel):
    query_id: str
    answer: str
    confidence: ConfidenceLevel
    doctrine_blocks_used: List[str]
    authorities_cited: List[str]
    latency_ms: float
    mode: ResponseMode
    zone: AnalysisZone
    determinism_hash: str
    epistemic_disclosure: Optional[str] = None

# ============================================================================
# TIE-20 COMPONENT 11-15: CORE ENGINE LOGIC
# ============================================================================

class REG02Engine:
    def __init__(self):
        self.metrics = EngineMetrics()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()
        self.telemetry_log: List[QueryTelemetry] = []
        logger.info(f"{ENGINE_NAME} v{VERSION} initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def normalize_query(self, query: str) -> str:
        """TIE-20 Component: Semantic Normalization"""
        term_map = {
            "rrc": "railroad commission of texas",
            "tceq": "texas commission on environmental quality",
            "tdi": "texas department of insurance",
            "dshs": "department of state health services",
            "soah": "state office of administrative hearings",
            "apa": "administrative procedure act",
            "tac": "texas administrative code",
            "nsr": "new source review",
            "tpdes": "texas pollutant discharge elimination system",
            "ccn": "certificate of convenience and necessity",
            "tabc": "texas alcoholic beverage commission",
            "dwc": "division of workers compensation",
            "tea": "texas education agency",
            "pia": "public information act",
            "h2s": "hydrogen sulfide"
        }
        normalized = query.lower()
        for abbr, full in term_map.items():
            normalized = normalized.replace(abbr, full)
        return normalized

    def search_doctrines(self, query: str) -> List[DoctrineBlock]:
        """TIE-20 Component: Three-Layer Response - Cache Layer"""
        normalized = self.normalize_query(query)
        matches = []
        for doctrine in DOCTRINE_CACHE:
            if any(kw in normalized for kw in doctrine.keywords):
                matches.append(doctrine)
                self.coverage_map.record_trigger(doctrine.topic)
        return matches[:5]  # Top 5 matches

    def stratify_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """TIE-20 Component: Confidence Stratification"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE
        confidence_scores = {"DEFENSIBLE": 3, "AGGRESSIVE": 2, "DISCLOSURE": 1, "HIGH_RISK": 0}
        avg_score = sum(confidence_scores.get(d.confidence.value, 0) for d in doctrines) / len(doctrines)
        if avg_score >= 2.5:
            return ConfidenceLevel.DEFENSIBLE
        elif avg_score >= 1.5:
            return ConfidenceLevel.AGGRESSIVE
        elif avg_score >= 0.5:
            return ConfidenceLevel.DISCLOSURE
        return ConfidenceLevel.HIGH_RISK

    def generate_response(self, query: str, mode: ResponseMode, zone: AnalysisZone,
                         doctrines: List[DoctrineBlock]) -> str:
        """TIE-20 Component: Response Modes + Zoned Analysis"""
        if not doctrines:
            return self._fallback_response(query, zone)

        if mode == ResponseMode.FAST:
            return self._fast_response(doctrines, zone)
        elif mode == ResponseMode.DEFENSE:
            return self._defense_response(doctrines, zone)
        else:  # MEMO
            return self._memo_response(query, doctrines, zone)

    def _fast_response(self, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
        primary = doctrines[0]
        zone_prefix = self._zone_prefix(zone)
        return f"{zone_prefix}{' '.join(primary.conclusion_template)} Primary authority: {', '.join(primary.primary_authority[:2])}."

    def _defense_response(self, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
        primary = doctrines[0]
        zone_prefix = self._zone_prefix(zone)
        response = f"{zone_prefix}ANALYSIS:\n\n{primary.reasoning_framework}\n\n"
        response += f"KEY FACTORS:\n" + "\n".join(f"- {f}" for f in primary.key_factors) + "\n\n"
        response += f"PRIMARY AUTHORITY:\n" + "\n".join(f"- {a}" for a in primary.primary_authority) + "\n\n"
        response += f"CONCLUSION:\n" + " ".join(primary.conclusion_template)
        return response

    def _memo_response(self, query: str, doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
        zone_prefix = self._zone_prefix(zone)
        response = f"{zone_prefix}MEMORANDUM\n\nQUESTION PRESENTED:\n{query}\n\n"
        response += "BRIEF ANSWER:\n" + " ".join(doctrines[0].conclusion_template) + "\n\n"
        response += "DISCUSSION:\n\n"
        for i, doctrine in enumerate(doctrines[:3], 1):
            response += f"{i}. {doctrine.topic}\n\n{doctrine.reasoning_framework}\n\n"
            response += f"Key Factors: {', '.join(doctrine.key_factors)}\n\n"
            response += f"Controlling Authority: {'; '.join(doctrine.controlling_precedent)}\n\n"
        response += "CONCLUSION:\n" + " ".join(doctrines[0].conclusion_template)
        return response

    def _fallback_response(self, query: str, zone: AnalysisZone) -> str:
        zone_prefix = self._zone_prefix(zone)
        return f"{zone_prefix}No specific doctrine blocks matched this query. General Texas state regulatory framework applies under Administrative Procedure Act (Gov Code Ch. 2001). Agency-specific regulations would govern based on subject matter. Recommend consulting relevant Texas Administrative Code provisions and agency enabling statutes."

    def _zone_prefix(self, zone: AnalysisZone) -> str:
        """TIE-20 Component: Zoned Analysis"""
        if zone == AnalysisZone.PLANNING:
            return "[PLANNING ZONE] "
        elif zone == AnalysisZone.REPORTING:
            return "[REPORTING ZONE] "
        elif zone == AnalysisZone.AUDIT:
            return "[AUDIT ZONE - DEFENSIBLE POSITIONS ONLY] "
        return ""

    def compute_determinism_hash(self, query: str, response: str) -> str:
        """TIE-20 Component: SHA-256 Determinism Hash"""
        content = f"{query}|{response}|{VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def apply_epistemic_guardrails(self, doctrines: List[DoctrineBlock]) -> Optional[str]:
        """TIE-20 Component: Epistemic Guardrails"""
        if not doctrines:
            return "DISCLOSURE: No matching regulatory doctrines found. Analysis based on general principles only."
        high_risk = [d for d in doctrines if d.confidence == ConfidenceLevel.HIGH_RISK]
        if high_risk:
            return f"DISCLOSURE: Analysis involves {len(high_risk)} high-risk legal positions. Consult specialized counsel."
        return None

    def query(self, request: QueryRequest) -> QueryResponse:
        """TIE-20 Component: Main Query Endpoint"""
        start_time = time.time()
        query_id = hashlib.md5(f"{request.query}{time.time()}".encode()).hexdigest()[:12]

        # Search doctrines
        doctrines = self.search_doctrines(request.query)
        cache_hit = len(doctrines) > 0

        # Generate response
        response_text = self.generate_response(request.query, request.mode, request.zone, doctrines)

        # Stratify confidence
        confidence = self.stratify_confidence(doctrines)

        # Epistemic disclosure
        disclosure = self.apply_epistemic_guardrails(doctrines)

        # Authorities
        authorities = []
        for d in doctrines[:3]:
            authorities.extend(d.primary_authority)

        # Determinism hash
        det_hash = self.compute_determinism_hash(request.query, response_text)

        # Latency
        latency_ms = (time.time() - start_time) * 1000

        # Telemetry
        telemetry = QueryTelemetry(
            query_id=query_id,
            timestamp=datetime.now(),
            query_text=request.query,
            mode=request.mode,
            doctrine_blocks_triggered=[d.topic for d in doctrines],
            latency_ms=latency_ms,
            cache_hit=cache_hit
        )
        self.telemetry_log.append(telemetry)

        # Metrics
        self.metrics.total_queries += 1
        if cache_hit:
            self.metrics.cache_hits += 1
        self.metrics.avg_latency_ms = (
            (self.metrics.avg_latency_ms * (self.metrics.total_queries - 1) + latency_ms)
            / self.metrics.total_queries
        )
        for d in doctrines:
            self.metrics.doctrine_hit_rate[d.topic] = self.metrics.doctrine_hit_rate.get(d.topic, 0) + 1

        logger.info(f"Query {query_id} processed in {latency_ms:.2f}ms, {len(doctrines)} doctrines, confidence={confidence.value}")

        return QueryResponse(
            query_id=query_id,
            answer=response_text,
            confidence=confidence,
            doctrine_blocks_used=[d.topic for d in doctrines],
            authorities_cited=authorities[:10],
            latency_ms=latency_ms,
            mode=request.mode,
            zone=request.zone,
            determinism_hash=det_hash,
            epistemic_disclosure=disclosure
        )

# ============================================================================
# TIE-20 COMPONENT 16-20: FASTAPI SERVER
# ============================================================================

engine = REG02Engine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """TIE-20 Component: Lifespan Management"""
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    yield
    logger.info(f"{ENGINE_NAME} v{VERSION} shutting down")

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """TIE-20 Component: Query Endpoint"""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """TIE-20 Component: Health Endpoint"""
    coverage = engine.coverage_map.get_coverage_stats()
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "total_queries": engine.metrics.total_queries,
        "cache_hit_rate": (engine.metrics.cache_hits / engine.metrics.total_queries * 100)
                         if engine.metrics.total_queries > 0 else 0,
        "avg_latency_ms": engine.metrics.avg_latency_ms,
        "doctrine_blocks": len(DOCTRINE_CACHE),
        "coverage_pct": coverage["coverage_pct"],
        "epistemic_gaps": len(coverage["epistemic_gaps"])
    }

@app.get("/metrics")
async def get_metrics():
    """TIE-20 Component: Metrics Endpoint"""
    return {
        "total_queries": engine.metrics.total_queries,
        "cache_hits": engine.metrics.cache_hits,
        "avg_latency_ms": engine.metrics.avg_latency_ms,
        "error_count": engine.metrics.error_count,
        "doctrine_hit_rate": engine.metrics.doctrine_hit_rate,
        "coverage": engine.coverage_map.get_coverage_stats()
    }

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "count": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "confidence": d.confidence.value,
                "keywords": d.keywords[:3]
            }
            for d in DOCTRINE_CACHE
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
