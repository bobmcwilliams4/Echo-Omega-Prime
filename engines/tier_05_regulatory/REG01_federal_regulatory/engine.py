"""
REG01 - Federal Regulatory Compliance Engine v1.0.0
TIE-grade intelligence engine for federal regulatory law analysis
Port 9121 | Authority Level 11.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import re
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "REG01"
ENGINE_NAME = "Federal Regulatory Compliance Engine"
VERSION = "1.0.0"
PORT = 9121
AUDIT_LOG = Path(__file__).parent / "audit_trail.jsonl"

logger.add(
    Path(__file__).parent / "reg01_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

# ============================================================================
# ENUMS
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

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    RULEMAKING = "RULEMAKING"
    ENFORCEMENT = "ENFORCEMENT"
    DEFERENCE = "DEFERENCE"
    JUDICIAL_REVIEW = "JUDICIAL_REVIEW"
    COST_BENEFIT = "COST_BENEFIT"
    SMALL_BUSINESS = "SMALL_BUSINESS"
    MAJOR_QUESTIONS = "MAJOR_QUESTIONS"
    EXHAUSTION = "EXHAUSTION"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None

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
    confidence_stratification: str
    controlling_precedent: str

class QueryResponse(BaseModel):
    query_id: str
    timestamp: str
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    sources: List[str]
    confidence: ConfidenceLevel
    latency_ms: int
    cache_hit: bool
    determinism_hash: str
    issues_identified: List[str]
    epistemic_caveat: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float

# ============================================================================
# DOCTRINE CACHE - 25+ REAL FEDERAL REGULATORY BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="APA Notice and Comment Rulemaking",
        keywords=["5 USC 553", "notice", "comment", "rulemaking", "APA", "publication"],
        conclusion_template=[
            "APA Section 553 requires notice of proposed rulemaking in Federal Register",
            "Opportunity for public comment must be meaningful, not pro forma",
            "Final rule must address significant comments and explain reasoning"
        ],
        reasoning_framework="""
Administrative Procedure Act 5 USC Section 553 mandates procedural fairness:
1. Notice Requirement - Agency must publish general notice of proposed rulemaking in Federal Register
2. Comment Period - Must provide interested persons opportunity to participate through submission of written data, views, or arguments
3. Statement of Basis - Final rule must include concise general statement of basis and purpose
4. Meaningful Opportunity - Courts require meaningful opportunity to comment, not mere formality
5. Response Duty - Agency must respond to significant comments, cannot ignore material objections
6. Logical Outreach - Final rule must be logical outgrowth of proposed rule
7. Exceptions - Exemptions for interpretative rules, general statements of policy, rules of agency organization
        """,
        key_factors=[
            "Federal Register publication timing",
            "Comment period duration (typically 30-60 days minimum)",
            "Substantive response to material comments",
            "Logical outreach test satisfaction",
            "Good cause exemption applicability"
        ],
        primary_authority=[
            "5 USC Section 553",
            "United States v. Florida East Coast Railway, 410 U.S. 224 (1973)",
            "Portland Cement Assn v. Ruckelshaus, 486 F.2d 375 (D.C. Cir. 1973)",
            "Perez v. Mortgage Bankers Assn, 575 U.S. 92 (2015)"
        ],
        burden_holder="Agency bears burden to follow APA procedures and demonstrate compliance",
        adversary_position="Challenger argues procedural defect invalidates rule",
        counter_arguments=[
            "Harmless error - defect did not prejudice outcome",
            "Good cause exception applies for emergencies",
            "Interpretative rule exempt from notice-comment",
            "Comment addressed substance even if agency response terse",
            "Logical outreach satisfied despite changes"
        ],
        resolution_strategy="Strict procedural compliance. Document robust comment process, substantive responses, logical connection to proposal.",
        entity_scope="All federal agencies subject to APA unless exempted by statute",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on core requirements; fact-specific on exemptions and harmless error",
        controlling_precedent="5 USC 553; D.C. Circuit notice-comment jurisprudence"
    ),
    DoctrineBlock(
        topic="Chevron Deference Framework",
        keywords=["Chevron", "deference", "ambiguity", "reasonable", "statutory interpretation"],
        conclusion_template=[
            "Chevron Step One: Determine if statute is ambiguous using traditional tools",
            "Chevron Step Two: If ambiguous, defer to reasonable agency interpretation",
            "Major questions doctrine limits Chevron in extraordinary cases"
        ],
        reasoning_framework="""
Chevron U.S.A. Inc. v. Natural Resources Defense Council, 467 U.S. 837 (1984):
Step One - Court determines whether Congress has directly spoken to precise question at issue
- Use traditional canons: text, structure, purpose, legislative history
- If intent clear, that is end of matter; court and agency must give effect to unambiguously expressed intent
Step Two - If statute silent or ambiguous, court defers to agency if interpretation is permissible
- Reasonable construction standard, not best interpretation
- Agency expertise and political accountability justify deference
- Implicit delegation of gap-filling authority
Post-Chevron Developments:
- Mead framework: Chevron applies only when Congress delegated authority to make rules with force of law
- Major questions doctrine: Extraordinary cases require clear Congressional authorization
- Auer deference: Similar framework for agency interpretation of own regulations (now cabined by Kisor)
        """,
        key_factors=[
            "Statutory ambiguity determination",
            "Agency authority to issue rule with force of law",
            "Reasonableness of agency interpretation",
            "Major questions doctrine applicability",
            "Notice-and-comment compliance for legislative rules"
        ],
        primary_authority=[
            "Chevron U.S.A. Inc. v. NRDC, 467 U.S. 837 (1984)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "West Virginia v. EPA, 142 S. Ct. 2587 (2022)",
            "Loper Bright Enterprises v. Raimondo (overruling Chevron 2024)"
        ],
        burden_holder="Agency bears burden at Step Two to show reasonableness; party challenging bears burden to show unreasonableness",
        adversary_position="Statute unambiguous or agency interpretation unreasonable",
        counter_arguments=[
            "Post-Loper Bright: No deference, de novo review of statutory interpretation",
            "Major questions: Economic and political significance triggers heightened scrutiny",
            "Mead exception: Informal guidance does not warrant Chevron",
            "Step One: Traditional tools resolve ambiguity against agency",
            "Step Two: Alternative interpretation more reasonable"
        ],
        resolution_strategy="Post-2024: Chevron overruled. Agencies must persuade on reasonableness without deference. Legislative rules still valid if within statutory authority.",
        entity_scope="All federal agencies interpreting statutes they administer",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Chevron overruled June 2024; transition period for applying de novo review standard",
        controlling_precedent="Loper Bright Enterprises v. Raimondo (2024) overruling Chevron"
    ),
    DoctrineBlock(
        topic="Auer/Kisor Deference to Regulatory Interpretation",
        keywords=["Auer", "Kisor", "Seminole Rock", "regulatory interpretation", "deference"],
        conclusion_template=[
            "Auer deference applies when regulation genuinely ambiguous",
            "Agency interpretation must be reasonable and reflect fair and considered judgment",
            "Kisor cabins Auer: deference not reflexive, requires rigorous analysis"
        ],
        reasoning_framework="""
Auer v. Robbins, 519 U.S. 452 (1997) and Kisor v. Wilkie, 139 S. Ct. 2400 (2019):
Traditional Auer: Agency interpretation of its own ambiguous regulation entitled to deference
Kisor Limitations:
1. Genuine Ambiguity - Regulation must be genuinely ambiguous after exhausting traditional tools of construction
2. Character and Context - Interpretation must be reasonable in light of regulatory text, structure, history, purpose
3. Authoritative Interpretation - Must reflect agency's authoritative, official position, not litigating position
4. Fair and Considered Judgment - Must implicate agency expertise and reflect fair and considered judgment
5. No Unfair Surprise - Cannot create unfair surprise or impose new obligations retroactively
Application: Deference now cabined, not automatic. Reviewing court conducts rigorous threshold analysis.
        """,
        key_factors=[
            "Regulation genuinely ambiguous after applying canons",
            "Agency interpretation reasonable in context",
            "Official authoritative position, not post-hoc rationalization",
            "Implicates substantive expertise",
            "No unfair surprise to regulated parties"
        ],
        primary_authority=[
            "Kisor v. Wilkie, 139 S. Ct. 2400 (2019)",
            "Auer v. Robbins, 519 U.S. 452 (1997)",
            "Bowles v. Seminole Rock, 325 U.S. 410 (1945)",
            "Christopher v. SmithKline Beecham, 567 U.S. 142 (2012)"
        ],
        burden_holder="Agency bears burden to demonstrate interpretation reasonable and authoritative",
        adversary_position="Regulation unambiguous or agency interpretation unreasonable/unfair surprise",
        counter_arguments=[
            "Text and context resolve ambiguity without deference",
            "Litigating position not authoritative agency view",
            "Post-hoc rationalization manufactured for litigation",
            "Unfair surprise: regulated parties reasonably relied on different reading",
            "Does not implicate agency expertise"
        ],
        resolution_strategy="Post-Kisor: rigorous threshold showing required. Document authoritative, considered interpretation in official guidance.",
        entity_scope="All federal agencies interpreting their own regulations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Kisor cabined but did not eliminate Auer; case-by-case analysis required",
        controlling_precedent="Kisor v. Wilkie (2019)"
    ),
    DoctrineBlock(
        topic="Major Questions Doctrine",
        keywords=["major questions", "clear statement", "extraordinary", "economic significance", "political"],
        conclusion_template=[
            "Extraordinary cases of economic and political significance require clear Congressional authorization",
            "Agency cannot claim discover vast regulatory authority in ancillary statutory provision",
            "Applies when agency asserts power over major portion of economy or issue of national significance"
        ],
        reasoning_framework="""
West Virginia v. EPA, 142 S. Ct. 2587 (2022) crystallized major questions doctrine:
Doctrine Triggers:
1. Economic Significance - Regulation affects major portion of economy or imposes vast economic costs
2. Political Significance - Issue of deep political significance or transforms agency's regulatory authority
3. Ancillary Provision - Agency claims authority from vague or ancillary statutory text
Application: Court will not presume delegation of extraordinary authority absent clear Congressional statement
Historical Applications:
- FDA tobacco regulation (Brown & Williamson)
- OSHA vaccine mandate (NFIB v. OSHA)
- CDC eviction moratorium (Alabama Assn of Realtors)
- EPA carbon emissions (West Virginia v. EPA)
Rationale: Non-delegation concerns, separation of powers, political accountability
        """,
        key_factors=[
            "Economic magnitude of regulation",
            "Political significance and public debate",
            "Clarity of statutory authorization",
            "History of agency regulation in area",
            "Ancillary vs. central statutory provision"
        ],
        primary_authority=[
            "West Virginia v. EPA, 142 S. Ct. 2587 (2022)",
            "NFIB v. OSHA, 142 S. Ct. 661 (2022)",
            "Alabama Assn of Realtors v. HHS, 141 S. Ct. 2485 (2021)",
            "FDA v. Brown & Williamson, 529 U.S. 120 (2000)"
        ],
        burden_holder="Agency bears burden to point to clear Congressional authorization for major regulatory action",
        adversary_position="Agency exceeded statutory authority in asserting vast new regulatory power",
        counter_arguments=[
            "Not major question: limited economic impact, traditional agency role",
            "Clear statement exists: statutory text directly authorizes action",
            "Longstanding practice: agency regulated in area for decades",
            "Post-enactment developments: Congress acquiesced to interpretation",
            "Necessary implication: authority implicit in core mandate"
        ],
        resolution_strategy="Secure explicit Congressional authorization for major regulatory initiatives. Document economic analysis and statutory nexus.",
        entity_scope="All federal agencies, particularly EPA, HHS, OSHA, FCC, SEC in major rulemakings",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Doctrine expanding; unclear boundaries on what constitutes 'major' question",
        controlling_precedent="West Virginia v. EPA (2022)"
    ),
    DoctrineBlock(
        topic="Arbitrary and Capricious Review - APA Section 706",
        keywords=["arbitrary", "capricious", "reasoned decision", "hard look", "record support"],
        conclusion_template=[
            "Agency action arbitrary if fails to consider important aspect of problem",
            "Must articulate rational connection between facts found and choice made",
            "Hard look review requires reasoned explanation supported by record"
        ],
        reasoning_framework="""
APA 5 USC Section 706(2)(A): Court shall set aside agency action found to be arbitrary, capricious, abuse of discretion, or not in accordance with law
Motor Vehicle Manufacturers v. State Farm, 463 U.S. 29 (1983):
Agency action arbitrary and capricious if:
1. Failed to consider important aspect of problem
2. Offered explanation runs counter to evidence
3. So implausible it could not be ascribed to difference in view or product of agency expertise
4. Failed to articulate rational connection between facts and choice
Hard Look Requirements:
- Examine relevant data and articulate satisfactory explanation
- Consider reasonable alternatives
- Respond to significant comments
- Provide contemporaneous explanation, not post-hoc rationalization
- Connect evidence to conclusions with logical reasoning
Standard: Narrow review, deferential but not toothless
        """,
        key_factors=[
            "Consideration of relevant factors",
            "Explanation quality and logical reasoning",
            "Record support for factual findings",
            "Response to significant objections",
            "Rational connection between facts and decision"
        ],
        primary_authority=[
            "5 USC Section 706(2)(A)",
            "Motor Vehicle Mfrs. v. State Farm, 463 U.S. 29 (1983)",
            "Citizens to Preserve Overton Park v. Volpe, 401 U.S. 402 (1971)",
            "Dep't of Commerce v. New York, 139 S. Ct. 2551 (2019)"
        ],
        burden_holder="Agency bears burden to provide reasoned explanation; challenger bears burden to show arbitrariness",
        adversary_position="Agency failed to consider key factor or explanation contradicts evidence",
        counter_arguments=[
            "Rational basis: decision within zone of reasonableness",
            "Expertise: technical judgment entitled to deference",
            "Alternatives considered: agency addressed in record",
            "Record support: substantial evidence for findings",
            "Changed circumstances: reasonable to alter policy"
        ],
        resolution_strategy="Document thorough consideration of factors, respond to comments, connect evidence to conclusions with clear reasoning.",
        entity_scope="All reviewable federal agency action",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-settled standard; fact-intensive application",
        controlling_precedent="State Farm (1983); Overton Park (1971)"
    ),
    DoctrineBlock(
        topic="Executive Order 12866 and OIRA Review",
        keywords=["EO 12866", "OIRA", "regulatory review", "cost-benefit", "significant regulatory action"],
        conclusion_template=[
            "Significant regulatory actions must undergo OIRA review",
            "Agencies must submit regulatory impact analysis for economically significant rules",
            "Cost-benefit analysis required showing benefits justify costs"
        ],
        reasoning_framework="""
Executive Order 12866 (as amended by EO 13563 and EO 14094):
Regulatory Philosophy:
1. Problem Identification - Each agency shall identify problem regulation intends to address
2. Assessment of Necessity - Determine whether existing regulations or alternatives could better address problem
3. Cost-Benefit - Benefits must justify costs
4. Maximize Net Benefits - Design regulation to maximize net benefits to society
Significant Regulatory Action: $200 million annual economic impact OR raises novel legal/policy issues
OIRA Review Process:
- Draft RIA (Regulatory Impact Analysis) required
- Submit to OIRA Office of Management and Budget
- 90-day review period for significant rules
- OIRA may return for reconsideration
- Interagency coordination and resolution of conflicts
Independent Agencies: Generally exempt from OIRA review (SEC, FTC, CFTC, FERC, FCC on case-by-case)
        """,
        key_factors=[
            "Economic significance threshold ($200M annual)",
            "RIA quality and completeness",
            "Benefit-cost ratio demonstration",
            "Alternatives analysis",
            "OIRA coordination and clearance"
        ],
        primary_authority=[
            "Executive Order 12866 (Sept. 30, 1993)",
            "Executive Order 13563 (Jan. 18, 2011)",
            "Executive Order 14094 (April 6, 2023)",
            "OMB Circular A-4 (2023 revision)"
        ],
        burden_holder="Agency bears burden to demonstrate benefits justify costs and comply with EO process",
        adversary_position="Agency failed to conduct adequate cost-benefit analysis or bypassed OIRA",
        counter_arguments=[
            "Not significant: below $200M threshold",
            "Independent agency: exempt from OIRA",
            "Statutory mandate: cost-benefit not required by statute",
            "Qualitative benefits: difficult to monetize but substantial",
            "OIRA approved: cleared review process"
        ],
        resolution_strategy="Conduct robust RIA early, coordinate with OIRA, document quantified benefits exceed costs, analyze alternatives.",
        entity_scope="Executive branch agencies; independent agencies exempted",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="EO process well-established; enforceability via political oversight not judicial review",
        controlling_precedent="Executive Order 12866 as amended; OMB Circular A-4"
    ),
    DoctrineBlock(
        topic="Regulatory Flexibility Act - Small Business Impact",
        keywords=["RFA", "small business", "SBREFA", "IRFA", "FRFA", "regulatory flexibility"],
        conclusion_template=[
            "RFA requires analysis of small entity impact for rules with significant economic impact",
            "Initial and Final Regulatory Flexibility Analysis required",
            "Small Business Regulatory Enforcement Fairness Act adds congressional review"
        ],
        reasoning_framework="""
Regulatory Flexibility Act (5 USC 601-612) and SBREFA amendments:
Coverage: Rules with significant economic impact on substantial number of small entities
Small Entities: Small businesses, small governmental jurisdictions, small nonprofit organizations
Requirements:
1. Initial Regulatory Flexibility Analysis (IRFA) with proposed rule:
   - Description of small entities affected
   - Projected compliance costs
   - Alternatives considered to minimize impact
2. Final Regulatory Flexibility Analysis (FRFA) with final rule:
   - Summary of significant issues raised by public
   - Response to comments
   - Estimate of number of small entities affected
   - Description of projected compliance requirements
   - Steps to minimize impact while achieving objectives
SBREFA Panel: EPA and OSHA must convene Small Business Advocacy Review Panel before proposing certain rules
Judicial Review: Courts review compliance under arbitrary and capricious standard
        """,
        key_factors=[
            "Significant economic impact determination",
            "Substantial number of small entities affected",
            "Quality of IRFA and FRFA",
            "Consideration of regulatory alternatives",
            "SBREFA panel process compliance (EPA/OSHA)"
        ],
        primary_authority=[
            "5 USC Sections 601-612",
            "Small Business Regulatory Enforcement Fairness Act, Pub. L. 104-121 (1996)",
            "American Trucking Assns v. EPA, 175 F.3d 1027 (D.C. Cir. 1999)",
            "Alenco Communications v. FCC, 201 F.3d 608 (5th Cir. 2000)"
        ],
        burden_holder="Agency bears burden to conduct RFA analysis and demonstrate compliance",
        adversary_position="Agency failed to prepare adequate IRFA/FRFA or consider small entity alternatives",
        counter_arguments=[
            "Certification: No significant impact on substantial number",
            "Alternatives infeasible: less burdensome options fail to achieve objectives",
            "IRFA adequate: addressed required elements",
            "FRFA responsive: considered comments and revised analysis",
            "Harmless error: defect did not prejudice outcome"
        ],
        resolution_strategy="Prepare thorough IRFA and FRFA, document small entity outreach, analyze flexible compliance alternatives.",
        entity_scope="All federal agencies subject to APA notice-comment rulemaking",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="RFA compliance frequently litigated; courts review for adequacy not perfection",
        controlling_precedent="5 USC 601-612; D.C. Circuit RFA jurisprudence"
    ),
    DoctrineBlock(
        topic="Congressional Review Act",
        keywords=["CRA", "congressional review", "resolution of disapproval", "5 USC 801", "major rule"],
        conclusion_template=[
            "CRA requires submission of all rules to Congress before taking effect",
            "Major rules subject to 60-day delay and potential disapproval resolution",
            "Disapproved rules cannot be reissued in substantially same form"
        ],
        reasoning_framework="""
Congressional Review Act (5 USC 801-808):
Process:
1. Submission - Agency must submit rule to Congress and GAO before effective
2. Major Rule Determination - GAO determines if rule is major ($100M economic impact, major cost increase, or significant adverse effect)
3. Delay - Major rules delayed 60 days (non-major 30 days with exceptions)
4. Resolution of Disapproval - Congress may pass joint resolution disapproving rule
5. Presidential Signature - Resolution requires President signature (or veto override)
Effect of Disapproval:
- Rule has no force or effect
- Substantially same rule cannot be reissued without subsequent statutory authorization
- Rarely used but potent tool (used 16 times 2001-2017, then surge in 2017)
Strategic Timing: Lookback period allows Congress to review rules from end of prior session
        """,
        key_factors=[
            "Timely submission to Congress and GAO",
            "Major rule determination",
            "60-day delay for major rules",
            "Congressional disapproval resolution risk",
            "Reissuance prohibition if disapproved"
        ],
        primary_authority=[
            "5 USC Sections 801-808",
            "Congressional Review Act, Pub. L. 104-121 (1996)",
            "GAO, Congressional Review Act: Rules Submitted Reports",
            "Congressional Research Service, The Congressional Review Act: Frequently Asked Questions"
        ],
        burden_holder="Agency bears burden to submit timely and accurately designate major rule status",
        adversary_position="Agency failed to submit or incorrectly designated non-major as major",
        counter_arguments=[
            "Timely submitted: compliance with CRA procedures",
            "Not major: below $100M threshold",
            "Political process: resolution unlikely to pass",
            "Presidential veto: disapproval subject to veto",
            "Substantially different: revised rule not same form"
        ],
        resolution_strategy="Submit all rules promptly, coordinate with GAO on major rule designation, minimize political controversy to avoid CRA resolution.",
        entity_scope="All federal agencies issuing rules",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CRA process clear; major rule designation sometimes disputed",
        controlling_precedent="5 USC 801-808; GAO guidance"
    ),
    DoctrineBlock(
        topic="Administrative Exhaustion Requirement",
        keywords=["exhaustion", "administrative remedies", "ripeness", "finality", "waiver"],
        conclusion_template=[
            "Plaintiff must exhaust administrative remedies before seeking judicial review",
            "Exceptions for inadequate remedy, irreparable harm, or futility",
            "Failure to raise issue in comments may result in waiver"
        ],
        reasoning_framework="""
Exhaustion Doctrine:
General Rule: Party challenging agency action must exhaust administrative remedies before judicial review
Rationales:
1. Agency Expertise - Allow agency to apply expertise and correct own errors
2. Judicial Efficiency - Develop factual record and legal issues
3. Autonomy - Respect agency autonomy and avoid premature interference
4. Issue Preservation - Ensure agency had opportunity to address objection
Exceptions:
- Inadequate Remedy - Administrative process cannot provide relief sought
- Irreparable Harm - Exhaustion would cause irreparable injury
- Futility - Agency lacks authority to grant relief or reversal clearly foreclosed
- Constitutional Claims - Pure questions of law, no factual development needed
- Systemic Challenge - Facial challenge to statute or regulation
Notice-Comment Context: Failure to raise issue in comments may waive judicial review (D.C. Circuit applies strictly)
        """,
        key_factors=[
            "Availability of administrative remedy",
            "Adequacy of administrative process",
            "Irreparable harm from delay",
            "Futility of exhaustion",
            "Issue preservation in comments"
        ],
        primary_authority=[
            "Darby v. Cisneros, 509 U.S. 137 (1993)",
            "McCarthy v. Madigan, 503 U.S. 140 (1992)",
            "Woodford v. Ngo, 548 U.S. 81 (2006)",
            "United States v. L.A. Tucker Truck Lines, 344 U.S. 33 (1952)"
        ],
        burden_holder="Plaintiff bears burden to exhaust or demonstrate exception",
        adversary_position="Plaintiff failed to exhaust administrative remedies",
        counter_arguments=[
            "Exception applies: irreparable harm, futility, inadequate remedy",
            "Pure legal question: no factual development needed",
            "Systemic challenge: exhaustion would not cure fundamental defect",
            "Issue raised: comments flagged objection to agency",
            "Waiver excused: issue not reasonably ascertainable from proposal"
        ],
        resolution_strategy="Raise all objections in administrative process, document exhaustion, petition for reconsideration if available.",
        entity_scope="All administrative proceedings with internal review mechanisms",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Exhaustion requirement well-settled; exceptions fact-specific",
        controlling_precedent="Darby v. Cisneros (1993)"
    ),
    DoctrineBlock(
        topic="Enforcement Discretion and Prosecutorial Discretion",
        keywords=["enforcement discretion", "prosecutorial discretion", "non-enforcement", "Heckler", "resources"],
        conclusion_template=[
            "Agency enforcement decisions generally committed to agency discretion",
            "Heckler v. Chaney: presumption against judicial review of non-enforcement",
            "Exceptions for systematic abdication or statutory mandate"
        ],
        reasoning_framework="""
Heckler v. Chaney, 470 U.S. 821 (1985):
Rule: Agency decision not to enforce generally unreviewable
Rationales:
1. Resource Allocation - Enforcement requires budgeting limited resources among priorities
2. Expertise - Agency best positioned to assess enforcement priorities
3. Complexity - Involves mixture of law, policy, and factual assessment
4. Committed to Discretion - APA Section 701(a)(2) precludes review when committed to agency discretion
Exceptions:
- Statutory Mandate - Statute uses mandatory language requiring enforcement
- Systematic Abdication - Agency adopts policy of total non-enforcement contrary to statute
- Procedural Requirements - Statute imposes procedural requirements on enforcement decisions
- Constitutional Violation - Non-enforcement motivated by improper factors (viewpoint discrimination)
Deferred Action Programs: Courts split on reviewability of large-scale non-enforcement policies (DACA litigation)
        """,
        key_factors=[
            "Resource constraints and priorities",
            "Individualized vs. categorical non-enforcement",
            "Statutory language (shall vs. may)",
            "Policy of systematic abdication",
            "Constitutional concerns"
        ],
        primary_authority=[
            "Heckler v. Chaney, 470 U.S. 821 (1985)",
            "5 USC Section 701(a)(2)",
            "Dunlop v. Bachowski, 421 U.S. 560 (1975)",
            "Texas v. United States (DACA litigation, ongoing)"
        ],
        burden_holder="Plaintiff bears heavy burden to overcome presumption of unreviewability",
        adversary_position="Agency systematically abdicated statutory duty",
        counter_arguments=[
            "Committed to discretion: core enforcement decision",
            "Resource allocation: insufficient resources for all violations",
            "Individualized: case-by-case assessment, not categorical policy",
            "Permissive statute: 'may' language, not 'shall'",
            "Policy within bounds: prioritization not abdication"
        ],
        resolution_strategy="Document individualized enforcement decisions, resource constraints, alignment with statutory purpose.",
        entity_scope="All agencies with enforcement authority",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core enforcement discretion unreviewable; boundaries unsettled for categorical policies",
        controlling_precedent="Heckler v. Chaney (1985)"
    ),
    DoctrineBlock(
        topic="Consent Decrees and Settlements",
        keywords=["consent decree", "settlement", "notice", "fairness hearing", "modification"],
        conclusion_template=[
            "Consent decrees must be fair, reasonable, and consistent with public interest",
            "Notice and opportunity for public comment generally required",
            "Modification requires showing of changed circumstances or initial invalidity"
        ],
        reasoning_framework="""
Consent Decree Framework:
Nature: Hybrid - contractual settlement with judicial imprimatur
Requirements:
1. Voluntary Agreement - Parties consent, not imposed
2. Judicial Approval - Court reviews for fairness, reasonableness, consistency with law and public interest
3. Public Participation - Notice and comment for significant environmental decrees (often required)
4. Entry of Judgment - Becomes court order, enforceable through contempt
Modification Standard (Rufo v. Inmates, 502 U.S. 367 (1992)):
- Changed circumstances make compliance substantially more onerous
- Decree proven unworkable due to unforeseen obstacles
- Enforcement no longer equitable
- Initial decree based on erroneous legal premise
Strategic Issues:
- Consent decree binds agency to specific action, limits future discretion
- Subsequent administrations may seek modification
- Third parties may intervene to enforce or oppose modification
- Regulatory negotiations and settlement as alternative to litigation
        """,
        key_factors=[
            "Voluntary nature of agreement",
            "Judicial fairness review",
            "Public comment adequacy",
            "Changed circumstances for modification",
            "Impact on agency discretion"
        ],
        primary_authority=[
            "Rufo v. Inmates of Suffolk County Jail, 502 U.S. 367 (1992)",
            "Local Number 93 v. Cleveland, 478 U.S. 501 (1986)",
            "United States v. Armour & Co., 402 U.S. 673 (1971)",
            "Federal Rule of Civil Procedure 23 (class actions)"
        ],
        burden_holder="Moving party bears burden to show grounds for modification",
        adversary_position="Consent decree should be enforced as written or modified",
        counter_arguments=[
            "Voluntary settlement: parties agreed to terms",
            "Public interest: decree serves statutory objectives",
            "No changed circumstances: conditions foreseeable",
            "Modification denied: insufficient showing under Rufo",
            "Good faith compliance: agency meeting decree obligations"
        ],
        resolution_strategy="Negotiate consent decrees with flexibility provisions, sunset clauses, preserve discretion on implementation details.",
        entity_scope="All agencies settling litigation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Modification standard clear; application fact-intensive",
        controlling_precedent="Rufo v. Inmates (1992)"
    ),
    DoctrineBlock(
        topic="Preemption of State Law by Federal Regulation",
        keywords=["preemption", "supremacy clause", "express", "field", "conflict", "savings clause"],
        conclusion_template=[
            "Federal regulations can preempt state law through express provision, field occupation, or conflict",
            "Presumption against preemption in traditional state areas",
            "Savings clauses preserve state authority unless clearly displaced"
        ],
        reasoning_framework="""
Preemption Doctrine (Supremacy Clause, Article VI):
Types:
1. Express Preemption - Statute or regulation explicitly preempts state law
2. Field Preemption - Federal scheme so pervasive it occupies field
3. Conflict Preemption - Impossible to comply with both or state law obstructs federal objectives
Presumption Against: In areas of traditional state regulation (health, safety, family law), courts presume no preemption absent clear Congressional intent
Agency Authority to Preempt:
- Wyeth v. Levine, 555 U.S. 555 (2009): Preamble statements insufficient, must have force of law
- Chevron applies: If statute authorizes preemption, agency interpretation entitled to deference (post-Loper: de novo review)
Savings Clauses: Many statutes preserve state authority; courts interpret strictly
Strategic Considerations: State enforcement can supplement federal or create patchwork; industry often seeks preemption for uniformity
        """,
        key_factors=[
            "Express preemption language in statute or regulation",
            "Pervasiveness of federal scheme",
            "Conflict between state and federal requirements",
            "Traditional state police power area",
            "Savings clause interpretation"
        ],
        primary_authority=[
            "Wyeth v. Levine, 555 U.S. 555 (2009)",
            "Gade v. National Solid Wastes Mgmt. Assn., 505 U.S. 88 (1992)",
            "Medtronic, Inc. v. Lohr, 518 U.S. 470 (1996)",
            "Arizona v. United States, 567 U.S. 387 (2012)"
        ],
        burden_holder="Party asserting preemption bears burden to demonstrate clear Congressional intent",
        adversary_position="Federal regulation preempts conflicting state law",
        counter_arguments=[
            "No express preemption: statute/regulation silent",
            "Not field preemption: federal scheme allows state supplementation",
            "No conflict: possible to comply with both",
            "Presumption against: traditional state power area",
            "Savings clause: Congress preserved state authority"
        ],
        resolution_strategy="Draft regulations with clear preemption scope; defer to states in traditional areas unless necessary for uniformity.",
        entity_scope="All federal agencies issuing regulations affecting state law",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Preemption analysis fact-intensive; Supreme Court divided on breadth",
        controlling_precedent="Wyeth v. Levine (2009); Gade (1992)"
    ),
    DoctrineBlock(
        topic="OMB Circular A-4 Cost-Benefit Analysis",
        keywords=["OMB A-4", "cost-benefit", "discount rate", "monetization", "distributional effects"],
        conclusion_template=[
            "OMB Circular A-4 provides framework for regulatory impact analysis",
            "Monetize costs and benefits, discount to present value",
            "2023 update emphasizes distributional analysis and equity"
        ],
        reasoning_framework="""
OMB Circular A-4 (2003, updated 2023):
Core Requirements:
1. Identify Need - Market failure, equity, other compelling public need
2. Baseline - Describe current and future state absent regulation
3. Alternatives - Examine range of regulatory and non-regulatory options
4. Benefits - Quantify and monetize benefits (health, safety, environmental)
5. Costs - Direct compliance costs, indirect costs, opportunity costs
6. Net Benefits - Compare benefits minus costs for each alternative
7. Discount Rate - Present value using 3% and 7% (2023: 2% and 7%)
8. Uncertainty - Conduct sensitivity analysis, quantify uncertainty
2023 Updates:
- Distributional Analysis: Assess impacts across income groups, communities
- Equity: Consider effects on disadvantaged populations
- Climate Impacts: Social cost of carbon, methane, other GHGs
- Behavioral Insights: Incorporate behavioral economics
Limitations: Not legally binding judicial standard, but political accountability and OIRA review lever
        """,
        key_factors=[
            "Comprehensive benefit and cost quantification",
            "Appropriate discount rate selection",
            "Distributional analysis inclusion",
            "Uncertainty characterization",
            "Alternatives analysis breadth"
        ],
        primary_authority=[
            "OMB Circular A-4 (Sept. 17, 2003, updated Nov. 9, 2023)",
            "Executive Order 12866",
            "Executive Order 13563",
            "Executive Order 14094"
        ],
        burden_holder="Agency bears burden to conduct RIA and demonstrate net benefits",
        adversary_position="Agency understated costs, overstated benefits, or failed to monetize properly",
        counter_arguments=[
            "Qualitative benefits: difficult to monetize but real",
            "Conservative estimates: benefits likely higher",
            "Statutory mandate: cost-benefit not required by statute",
            "Distributional gains: significant benefits to disadvantaged",
            "Sensitivity analysis: results robust to assumptions"
        ],
        resolution_strategy="Conduct rigorous RIA, quantify and monetize where feasible, acknowledge uncertainty, document distributional effects.",
        entity_scope="Executive branch agencies subject to EO 12866",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="A-4 methodology well-established; 2023 updates expand scope but core framework stable",
        controlling_precedent="OMB Circular A-4 (2023)"
    ),
    DoctrineBlock(
        topic="Unfunded Mandates Reform Act",
        keywords=["UMRA", "unfunded mandates", "intergovernmental", "private sector", "cost threshold"],
        conclusion_template=[
            "UMRA requires analysis of federal mandates imposing costs on state/local governments or private sector",
            "Threshold: $100 million annually (inflation-adjusted to ~$177M)",
            "Alternatives analysis required to minimize burden"
        ],
        reasoning_framework="""
Unfunded Mandates Reform Act (2 USC 1501-1571, 1995):
Coverage: Rules imposing enforceable duty on state/local governments or private sector
Threshold: $100 million annually in 1996 dollars (adjusted ~$177 million today)
Requirements:
1. Written Statement - Qualitative and quantitative assessment of costs
2. Cost-Benefit Analysis - Compare costs and benefits
3. Alternatives - Identify least costly or least burdensome alternative
4. Consultation - Meaningful consultation with state/local governments
5. Small Government Impact - Assess effect on small governments
Exemptions: National security, emergency, treaty implementation, statutory/constitutional rights enforcement
Enforcement: Procedural only, not judicially enforceable, but congressional point of order available
Strategic: Rarely triggers judicial challenge, but political tool for states/localities to oppose rules
        """,
        key_factors=[
            "Threshold determination ($177M adjusted)",
            "Enforceable duty vs. condition on grants",
            "Quality of alternatives analysis",
            "State/local consultation adequacy",
            "Small government impacts"
        ],
        primary_authority=[
            "2 USC Sections 1501-1571",
            "Unfunded Mandates Reform Act, Pub. L. 104-4 (1995)",
            "Congressional Budget Office, The Impact of Unfunded Mandates Reform Act",
            "OMB guidance on UMRA implementation"
        ],
        burden_holder="Agency bears burden to prepare UMRA analysis if threshold met",
        adversary_position="Agency failed to conduct required UMRA analysis or consider alternatives",
        counter_arguments=[
            "Below threshold: costs do not exceed $177M annually",
            "Not mandate: voluntary or condition on federal funds",
            "Exemption applies: statutory right enforcement",
            "Analysis complete: considered alternatives and consulted",
            "Not judicially enforceable: procedural requirement only"
        ],
        resolution_strategy="Quantify costs early, consult with states/localities, document alternatives considered, distinguish mandates from grant conditions.",
        entity_scope="All federal agencies subject to APA rulemaking",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="UMRA compliance straightforward; judicial review unavailable but political scrutiny significant",
        controlling_precedent="2 USC 1501-1571"
    ),
    DoctrineBlock(
        topic="Paperwork Reduction Act",
        keywords=["PRA", "OMB approval", "information collection", "burden hours", "ICR"],
        conclusion_template=[
            "PRA requires OMB approval for agency information collection from 10+ persons",
            "Burden hour estimates and necessity justification required",
            "Unapproved collections cannot be enforced"
        ],
        reasoning_framework="""
Paperwork Reduction Act (44 USC 3501-3521):
Purpose: Minimize paperwork burden on public, ensure information collection necessary
Coverage: Information collection requests to 10 or more persons (surveys, reports, recordkeeping)
Process:
1. Information Collection Request (ICR) - Agency prepares describing collection, burden, necessity
2. Public Comment - 60-day and 30-day Federal Register notices
3. OMB Review - OMB has 60 days to approve, disapprove, or request revision
4. OMB Control Number - Approved collections receive control number, must be displayed
Burden Estimate: Agency must estimate time required per respondent and total annual burden hours
Exemptions: During public health emergency, for first 10 respondents, certain criminal investigations
Enforcement: Agency cannot impose penalty for non-response to unapproved collection
Strategic: Significant compliance burden, can delay rulemakings, OMB approval sometimes denied
        """,
        key_factors=[
            "Applicability to 10+ persons",
            "Burden hour estimation accuracy",
            "Necessity and practical utility demonstration",
            "OMB approval obtained",
            "Control number displayed"
        ],
        primary_authority=[
            "44 USC Sections 3501-3521",
            "Dole v. United Steelworkers, 494 U.S. 26 (1990)",
            "OMB regulations at 5 CFR Part 1320",
            "Federal Register notice requirements"
        ],
        burden_holder="Agency bears burden to justify necessity and obtain OMB approval",
        adversary_position="Agency imposed unapproved information collection or underestimated burden",
        counter_arguments=[
            "OMB approved: valid control number issued",
            "Burden reasonable: estimated hours accurate",
            "Necessity: information needed for program operation",
            "Exemption: emergency or less than 10 persons",
            "Third-party disclosure: not information collection"
        ],
        resolution_strategy="Prepare thorough ICR, realistic burden estimates, coordinate with OMB early, publish required Federal Register notices.",
        entity_scope="All federal agencies collecting information from public",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PRA compliance procedural and clear; burden estimate disputes common",
        controlling_precedent="44 USC 3501-3521; 5 CFR Part 1320"
    ),
    DoctrineBlock(
        topic="Federal Advisory Committee Act",
        keywords=["FACA", "advisory committee", "charter", "open meetings", "public participation"],
        conclusion_template=[
            "FACA regulates advisory committees providing advice to federal agencies",
            "Requirements: charter, open meetings, balanced membership, public access",
            "Private groups advising agencies may trigger FACA obligations"
        ],
        reasoning_framework="""
Federal Advisory Committee Act (5 USC Appendix 2):
Coverage: Committees established or utilized by agency to obtain advice or recommendations
Exemptions: Wholly intra-agency, committees of federal officials, certain operational committees
Requirements:
1. Charter - File charter with Congress describing purpose, membership, duration
2. Balanced Membership - Fairly balanced in terms of points of view
3. Open Meetings - Meetings open to public with advance notice
4. Records - Meeting minutes, records publicly available
5. Designated Federal Officer - Federal employee must attend all meetings
6. Termination - Committee terminates after 2 years unless renewed
Utilized Committee: Private group can become FACA committee if agency exercises control over formation, work product, or membership
Strategic Issues: Agencies often structure informal stakeholder consultations to avoid FACA; litigation over utilized committee status
        """,
        key_factors=[
            "Committee establishment or utilization by agency",
            "Provision of advice vs. operational function",
            "Agency control over group",
            "Charter filing and renewal",
            "Meeting notice and openness"
        ],
        primary_authority=[
            "5 USC Appendix 2",
            "Food Chemical News v. Young, 900 F.2d 328 (D.C. Cir. 1990)",
            "Public Citizen v. DOJ, 491 U.S. 440 (1989)",
            "General Services Administration FACA regulations"
        ],
        burden_holder="Agency bears burden to comply with FACA if committee covered",
        adversary_position="Agency improperly utilized private committee without FACA compliance",
        counter_arguments=[
            "Not advisory: operational, not advice-giving",
            "Exemption: wholly federal officials",
            "No utilization: agency did not exercise control",
            "FACA compliant: charter filed, meetings open",
            "Informal consultation: not committee"
        ],
        resolution_strategy="Structure stakeholder engagement to avoid FACA (individual consultations, no voting, no collective advice), or comply fully if committee established.",
        entity_scope="All federal agencies using advisory committees",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="FACA coverage disputes common; utilized committee standard fact-intensive",
        controlling_precedent="5 USC App. 2; Public Citizen v. DOJ (1989)"
    ),
    DoctrineBlock(
        topic="Negotiated Rulemaking Act",
        keywords=["reg-neg", "negotiated rulemaking", "consensus", "stakeholders", "facilitated process"],
        conclusion_template=[
            "Negotiated rulemaking allows agency to convene stakeholders to reach consensus on proposed rule",
            "Committee develops proposed rule through facilitated negotiation",
            "Agency retains discretion to accept, modify, or reject consensus"
        ],
        reasoning_framework="""
Negotiated Rulemaking Act (5 USC 561-570):
Purpose: Enhance informal rulemaking by facilitating consensus among stakeholders
Process:
1. Determination - Agency determines reg-neg appropriate (limited issues, identifiable stakeholders, feasible consensus)
2. Notice - Federal Register notice of intent to establish negotiating committee
3. Committee Formation - Representatives of affected interests appointed
4. Facilitation - Neutral facilitator assists negotiation
5. Consensus - Committee seeks consensus on proposed rule text
6. Report - Committee submits consensus or report of areas of agreement/disagreement
7. Proposed Rule - Agency publishes as proposed rule (or modifies and explains)
8. Notice-Comment - Standard APA notice-comment process follows
FACA Applies: Negotiating committee is FACA advisory committee
Strategic: Time-intensive but can reduce litigation, build stakeholder support; used in environmental, labor, safety rules
Criticism: Can be captured by industry or devolve into position-taking
        """,
        key_factors=[
            "Limited issues and identifiable stakeholders",
            "Good faith participation by all interests",
            "Feasibility of consensus",
            "Agency resource commitment",
            "FACA compliance"
        ],
        primary_authority=[
            "5 USC Sections 561-570",
            "Negotiated Rulemaking Act, Pub. L. 101-648 (1990)",
            "Administrative Conference recommendations on reg-neg",
            "Agency reg-neg procedures (EPA, OSHA)"
        ],
        burden_holder="Agency bears burden to conduct process in good faith and comply with statute",
        adversary_position="Consensus process flawed or agency improperly rejected consensus",
        counter_arguments=[
            "Consensus achieved: all parties agreed",
            "Agency discretion: not bound by committee recommendation",
            "Process fair: balanced representation, neutral facilitator",
            "Modified for good cause: explained departure from consensus",
            "APA satisfied: notice-comment completed post-negotiation"
        ],
        resolution_strategy="Use reg-neg for complex rules with discrete stakeholder groups; ensure balanced representation; retain agency discretion.",
        entity_scope="All agencies considering negotiated rulemaking",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Reg-neg procedural framework clear; consensus achievement variable",
        controlling_precedent="5 USC 561-570"
    ),
    DoctrineBlock(
        topic="Data Quality Act and Information Quality",
        keywords=["Data Quality Act", "information quality", "OMB guidelines", "peer review", "reproducibility"],
        conclusion_template=[
            "Data Quality Act requires agencies to ensure quality, objectivity, utility, and integrity of information disseminated",
            "OMB guidelines establish standards and correction mechanisms",
            "Not independently judicially enforceable but procedural requirement"
        ],
        reasoning_framework="""
Data Quality Act (Section 515 of Treasury and General Government Appropriations Act for FY 2001):
Requirements:
1. OMB Guidelines - OMB issues government-wide guidelines for information quality
2. Agency Guidelines - Each agency issues own guidelines consistent with OMB
3. Quality Standards - Ensure quality, objectivity, utility, integrity of information
4. Correction Mechanism - Administrative mechanism to allow affected persons to seek correction
OMB Guidelines:
- Quality: Accuracy, reliability, unbiased presentation
- Objectivity: Accurate, reliable, unbiased, presented in context
- Utility: Usefulness to intended users
- Integrity: Security from unauthorized access or revision
Peer Review: OMB Bulletin on Peer Review requires independent expert review of influential scientific information
Judicial Review: Courts split on whether violations independently reviewable; generally considered procedural only
Strategic: Industry uses to challenge agency data, scientific studies; agencies must document quality control
        """,
        key_factors=[
            "Information dissemination vs. internal use",
            "Influential scientific information designation",
            "Peer review adequacy",
            "Correction request response",
            "Quality control documentation"
        ],
        primary_authority=[
            "Section 515, Pub. L. 106-554 (2000)",
            "OMB Guidelines for Ensuring and Maximizing the Quality of Information (2002)",
            "OMB Bulletin on Peer Review (2004, updated 2005)",
            "Salt Inst. v. Leavitt, 440 F.3d 156 (4th Cir. 2006)"
        ],
        burden_holder="Agency bears burden to ensure information quality and respond to correction requests",
        adversary_position="Agency disseminated low-quality or biased information",
        counter_arguments=[
            "Quality assured: peer review, validation, documentation",
            "Procedural compliance: followed agency guidelines",
            "Correction process: responded to requests substantively",
            "Not independently enforceable: no judicial remedy for violation alone",
            "Utility: information useful for regulatory purpose"
        ],
        resolution_strategy="Document data sources, peer review, quality control; respond substantively to correction requests; transparency in methods.",
        entity_scope="All federal agencies disseminating information",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Data quality standards clear; judicial enforceability limited",
        controlling_precedent="Section 515, Pub. L. 106-554; OMB Guidelines"
    ),
    DoctrineBlock(
        topic="Regulatory Lookback and Retrospective Review",
        keywords=["retrospective review", "lookback", "EO 13563", "sunset", "regulatory reform"],
        conclusion_template=[
            "Executive Order 13563 requires periodic retrospective review of existing rules",
            "Agencies must identify rules for modification, streamlining, expansion, or repeal",
            "Public participation in retrospective review process"
        ],
        reasoning_framework="""
Executive Order 13563 Section 6 (Retrospective Analysis):
Requirement: Agencies must develop and submit to OIRA plan for periodic retrospective review of existing significant regulations
Goals:
1. Identify rules that may be outmoded, ineffective, insufficient, or excessively burdensome
2. Modify, streamline, expand, or repeal rules as appropriate
3. Consider cumulative effects and interactions among rules
4. Solicit public input on rules to review
Process:
1. Preliminary Plan - Agency submits plan to OIRA
2. Public Comment - Solicit input on which rules to review
3. Review - Analyze costs, benefits, effectiveness
4. Report - Public progress reports
5. Action - Initiate rulemaking to modify or repeal as needed
Related: Some statutes contain sunset provisions or mandatory periodic review
Strategic: Used to reduce regulatory burden, respond to changed circumstances, update outdated rules; also political tool for deregulation
        """,
        key_factors=[
            "Plan submission and OIRA approval",
            "Public participation in selection",
            "Quality of retrospective analysis",
            "Follow-through on identified reforms",
            "Coordination across rules"
        ],
        primary_authority=[
            "Executive Order 13563 Section 6 (Jan. 18, 2011)",
            "Executive Order 13579 (retrospective review for independent agencies)",
            "OMB guidance on retrospective review",
            "Agency retrospective review plans"
        ],
        burden_holder="Agency bears burden to conduct retrospective review and justify retention of existing rules",
        adversary_position="Agency failed to review outdated rule or ignored evidence of ineffectiveness",
        counter_arguments=[
            "Reviewed: conducted retrospective analysis",
            "Still effective: rule achieving objectives",
            "Benefits justify costs: net benefits remain positive",
            "Modified: amended rule based on review",
            "Discretion: agency prioritization of reviews"
        ],
        resolution_strategy="Conduct meaningful retrospective reviews, solicit stakeholder input, update rules proactively, document cost-benefit of retention.",
        entity_scope="All agencies subject to EO 12866 regulatory review",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="EO requirement clear; enforcement via political oversight not judicial review",
        controlling_precedent="Executive Order 13563 Section 6"
    ),
    DoctrineBlock(
        topic="Interim Final Rules and Good Cause Exception",
        keywords=["interim final rule", "good cause", "emergency", "immediate effectiveness", "5 USC 553"],
        conclusion_template=[
            "Good cause exception allows agency to skip notice-comment for emergencies or when impracticable",
            "Interim final rules take immediate effect with post-promulgation comment",
            "Agency bears burden to demonstrate good cause"
        ],
        reasoning_framework="""
APA 5 USC Section 553(b)(B) and (d)(3) Good Cause Exception:
Standard: Notice-comment not required when agency finds (and incorporates in rule) that notice and public procedure are impracticable, unnecessary, or contrary to public interest
Applications:
1. Emergency - Imminent threat to health, safety, or security requiring immediate action
2. Impracticable - Deadlines or external events make process infeasible
3. Unnecessary - Ministerial, technical, or non-controversial amendments
4. Contrary to Public Interest - Notice would defeat purpose (e.g., prevent market manipulation)
Interim Final Rules: Agency issues rule immediately effective, solicits post-promulgation comment, may revise based on comments
Judicial Review: Courts interpret exception narrowly; agency bears burden to demonstrate particularized good cause, not generic assertions
Risks: Vulnerable to challenge if good cause showing weak; political criticism for bypassing public input
        """,
        key_factors=[
            "Genuine emergency or impracticability",
            "Particularized showing, not boilerplate",
            "Necessity for immediate effectiveness",
            "Post-promulgation comment opportunity",
            "Responsiveness to comments received"
        ],
        primary_authority=[
            "5 USC Sections 553(b)(B), 553(d)(3)",
            "Mack Trucks, Inc. v. EPA, 682 F.3d 87 (D.C. Cir. 2012)",
            "Util. Solid Waste Activities Grp. v. EPA, 236 F.3d 749 (D.C. Cir. 2001)",
            "Tennessee Gas Pipeline v. FERC, 969 F.2d 1141 (D.C. Cir. 1992)"
        ],
        burden_holder="Agency bears burden to demonstrate good cause with particularized findings",
        adversary_position="Agency improperly invoked good cause to bypass public participation",
        counter_arguments=[
            "Genuine emergency: imminent threat to public",
            "Impracticable: statutory deadline or external constraint",
            "Post-promulgation comment: opportunity provided",
            "Responsive: considered comments and revised",
            "Narrow scope: limited to emergency measures"
        ],
        resolution_strategy="Reserve good cause for genuine emergencies, provide detailed factual basis, solicit post-promulgation comment, revise if warranted.",
        entity_scope="All agencies subject to APA Section 553",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Good cause exception narrowly construed; frequent litigation target",
        controlling_precedent="5 USC 553; D.C. Circuit good cause jurisprudence"
    ),
    DoctrineBlock(
        topic="Direct Final Rules",
        keywords=["direct final rule", "non-controversial", "adverse comment", "withdrawal", "streamlined"],
        conclusion_template=[
            "Direct final rules allow expedited process for non-controversial rules",
            "Rule effective on specified date unless adverse comment received",
            "Agency withdraws if significant adverse comment, proceeds with notice-comment"
        ],
        reasoning_framework="""
Direct Final Rule Procedure (not in APA, but permitted):
Process:
1. Simultaneous Publication - Agency publishes direct final rule and parallel proposed rule in Federal Register
2. Comment Period - Typically 30-60 days
3. No Adverse Comment - If no significant adverse comment, rule becomes effective on stated date
4. Adverse Comment - If significant adverse comment received, agency withdraws direct final rule and proceeds with standard notice-comment on parallel proposal
Rationale: Streamline rulemaking for routine, technical, non-controversial amendments (e.g., updating cross-references, correcting errors, extending compliance deadlines)
Risks: Misjudgment of controversy leads to withdrawal and delay; adverse commenters can force full process
Strategic: Test for consensus; if opposition emerges, agency has proposed rule already in pipeline
Agencies Using: EPA, DOT, FDA, other agencies with high-volume routine amendments
        """,
        key_factors=[
            "Non-controversial nature of amendment",
            "Significance of adverse comments",
            "Withdrawal decision if comments received",
            "Parallel proposed rule publication",
            "Effective date conditioned on no adverse comment"
        ],
        primary_authority=[
            "Administrative Conference Recommendation 95-4 (1995)",
            "Agency direct final rule procedures (EPA, DOT, FDA)",
            "No specific APA provision, but consistent with Section 553"
        ],
        burden_holder="Agency bears burden to accurately assess non-controversial nature",
        adversary_position="Rule controversial, adverse comment ignored, or withdrawal arbitrary",
        counter_arguments=[
            "Non-controversial: routine technical amendment",
            "Adverse comment: not significant or reasoned",
            "Withdrawn: properly withdrew upon adverse comment",
            "Parallel proposal: proceeded with notice-comment",
            "Efficient: streamlined process for uncontested rule"
        ],
        resolution_strategy="Use direct final for truly non-controversial rules, clearly state withdrawal policy, promptly withdraw if adverse comment received.",
        entity_scope="Agencies with high-volume routine rulemakings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Direct final rule procedure well-accepted for appropriate cases",
        controlling_precedent="Admin. Conf. Recommendation 95-4; agency practice"
    ),
    DoctrineBlock(
        topic="Guidance Documents and Interpretive Rules",
        keywords=["guidance", "interpretive rule", "general statement of policy", "force of law", "notice-comment exemption"],
        conclusion_template=[
            "Guidance documents and interpretive rules exempt from notice-comment if no legal force",
            "Cannot create new obligations or rights, only interpret existing law",
            "Agencies must comply with OMB and agency guidance policies"
        ],
        reasoning_framework="""
APA Section 553(b)(A) Exemptions:
1. Interpretive Rules - Clarify or explain existing statute or regulation, do not add new requirements
2. General Statements of Policy - Announce agency policy but do not bind agency or public
Test for Legislative vs. Interpretive (D.C. Circuit):
- Does rule have legally binding effect?
- Does it create new rights or obligations?
- Does agency intend to bind itself?
- Does it fill gap in statute vs. interpret existing text?
Perez v. Mortgage Bankers (2015): Agencies need not use notice-comment to revise prior interpretive rules
OMB Final Bulletin on Good Guidance Practices (2007, rescinded 2021, elements remain best practice):
- Significant guidance documents require public comment
- Must be labeled, publicly accessible
- Cannot use to coerce regulated parties
Strategic Issues: Agencies use guidance to avoid notice-comment but risk judicial invalidation if deemed legislative; regulated parties uncertain whether guidance binding
        """,
        key_factors=[
            "Creates new obligations vs. interprets existing",
            "Legally binding effect",
            "Agency intent to bind",
            "Gap-filling vs. interpretation",
            "Public participation opportunity"
        ],
        primary_authority=[
            "5 USC Section 553(b)(A)",
            "Perez v. Mortgage Bankers Assn, 575 U.S. 92 (2015)",
            "Appalachian Power Co. v. EPA, 208 F.3d 1015 (D.C. Cir. 2000)",
            "OMB Final Bulletin on Good Guidance Practices (2007, rescinded)"
        ],
        burden_holder="Agency bears burden to demonstrate guidance is interpretive, not legislative",
        adversary_position="Guidance is legislative rule requiring notice-comment",
        counter_arguments=[
            "Interpretive: clarifies existing law, no new obligations",
            "Policy statement: non-binding, advisory only",
            "No force of law: regulated parties not bound",
            "Public input: solicited comment even if not required",
            "Perez: can revise interpretive rules without notice-comment"
        ],
        resolution_strategy="Draft guidance as interpretive, label clearly, disclaim binding effect, solicit public input for significant guidance.",
        entity_scope="All agencies issuing guidance documents",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Legislative vs. interpretive line blurry; frequent litigation",
        controlling_precedent="Perez v. Mortgage Bankers (2015); Appalachian Power (2000)"
    ),
    DoctrineBlock(
        topic="Scientific and Technical Rulemaking Standards",
        keywords=["scientific evidence", "peer review", "best available science", "transparency", "reproducibility"],
        conclusion_template=[
            "Agencies must base rules on best available science and peer-reviewed evidence",
            "Transparency in data and methods required for reproducibility",
            "Courts defer to agency scientific judgments if reasoned and supported"
        ],
        reasoning_framework="""
Standards for Scientific Rulemaking:
1. Best Available Science - Use current, peer-reviewed, scientifically valid evidence
2. Peer Review - OMB Peer Review Bulletin requires independent expert review of influential scientific information
3. Transparency - Disclose data, methods, models for public scrutiny and reproducibility
4. Uncertainty - Acknowledge and characterize scientific uncertainty
5. Conflicts of Interest - Disclose financial conflicts of advisory committee members
Influential Scientific Information: Information agency reasonably determines will have clear and substantial impact on important public policy or private sector decisions ($500M threshold)
Judicial Review: Courts defer to agency scientific judgments if reasonable and supported (arbitrary and capricious standard), but require transparent explanation
Criticism: Industry challenges alleging cherry-picked data, lack of transparency; environmentalists challenge inadequate consideration of precautionary principle
        """,
        key_factors=[
            "Quality and currency of scientific evidence",
            "Peer review adequacy",
            "Data and methods transparency",
            "Uncertainty characterization",
            "Expert conflicts of interest"
        ],
        primary_authority=[
            "OMB Bulletin on Peer Review (2004, updated 2005)",
            "Data Quality Act and OMB guidelines",
            "Information Quality Act correction mechanisms",
            "Baltimore Gas & Elec. v. NRDC, 462 U.S. 87 (1983)"
        ],
        burden_holder="Agency bears burden to demonstrate scientific basis and respond to scientific critiques",
        adversary_position="Agency relied on junk science, cherry-picked data, or ignored contrary evidence",
        counter_arguments=[
            "Peer-reviewed: independent experts validated",
            "Best available: used current scientific consensus",
            "Transparent: data and methods disclosed",
            "Uncertainty acknowledged: characterized limitations",
            "Weight of evidence: considered all studies, explained reliance"
        ],
        resolution_strategy="Commission peer review, disclose data and methods, address scientific critiques substantively, document weight-of-evidence analysis.",
        entity_scope="All agencies issuing science-based regulations (EPA, FDA, OSHA, etc.)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Scientific review standards well-established; battles over application to specific studies",
        controlling_precedent="OMB Peer Review Bulletin; Baltimore Gas (1983)"
    ),
    DoctrineBlock(
        topic="Environmental Justice in Rulemaking",
        keywords=["environmental justice", "EJ", "EO 12898", "disproportionate impact", "disadvantaged communities"],
        conclusion_template=[
            "Executive Order 12898 requires federal agencies to identify and address disproportionately high adverse environmental and health effects on minority and low-income populations",
            "OMB Circular A-4 (2023) requires distributional analysis",
            "Environmental justice analysis increasingly required in EIS and regulatory impact analysis"
        ],
        reasoning_framework="""
Environmental Justice Framework:
Executive Order 12898 (1994):
1. Identify Effects - Agencies must identify disproportionately high and adverse human health or environmental effects on minority and low-income populations
2. Address Effects - Develop strategy to address effects
3. Public Participation - Provide opportunities for community input
4. Data Collection - Improve data on environmental health effects
OMB Circular A-4 (2023 Update):
- Distributional Analysis - Assess how costs and benefits distributed across income groups, racial/ethnic groups, geographic areas
- Equity - Consider effects on communities with environmental justice concerns
NEPA: EPA guidance requires EJ analysis in Environmental Impact Statements
Strategic Considerations: Rules affecting industrial facilities, transportation, air/water quality trigger EJ scrutiny; community engagement essential; litigation risk if disparate impacts ignored
        """,
        key_factors=[
            "Identification of affected minority/low-income populations",
            "Disproportionate adverse impact assessment",
            "Community engagement and input",
            "Mitigation measures for disparate impacts",
            "Distributional analysis in RIA"
        ],
        primary_authority=[
            "Executive Order 12898 (Feb. 11, 1994)",
            "OMB Circular A-4 (2023)",
            "EPA Environmental Justice Guidance (1998, updated)",
            "CEQ NEPA Guidance on Environmental Justice (1997)"
        ],
        burden_holder="Agency bears burden to identify and address disproportionate impacts",
        adversary_position="Agency ignored environmental justice impacts or failed to mitigate",
        counter_arguments=[
            "Analysis conducted: assessed disparate impacts",
            "No disproportionate effect: impacts distributed equitably",
            "Mitigation: measures adopted to reduce impacts on EJ communities",
            "Community input: consulted with affected populations",
            "Net benefit: rule provides overall benefit including to EJ communities"
        ],
        resolution_strategy="Conduct EJ screening early, engage communities meaningfully, quantify distributional effects, adopt mitigation measures where feasible.",
        entity_scope="All federal agencies, particularly EPA, DOT, HUD, USDA",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="EJ analysis increasingly expected but standards evolving",
        controlling_precedent="Executive Order 12898; OMB A-4 (2023)"
    ),
    DoctrineBlock(
        topic="Regulatory Takings and Fifth Amendment",
        keywords=["takings", "regulatory taking", "Fifth Amendment", "just compensation", "Penn Central"],
        conclusion_template=[
            "Regulation may constitute taking requiring just compensation if goes too far",
            "Penn Central factors: economic impact, investment-backed expectations, character of action",
            "Categorical takings: physical invasion or denial of all economically beneficial use"
        ],
        reasoning_framework="""
Fifth Amendment Takings Clause: Nor shall private property be taken for public use, without just compensation
Regulatory Takings Doctrine:
Penn Central Transp. Co. v. New York City, 438 U.S. 104 (1978):
Three Factors:
1. Economic Impact - Extent of diminution in value
2. Investment-Backed Expectations - Reasonable reliance on prior legal regime
3. Character of Government Action - Physical invasion, public benefit, reciprocity of advantage
Categorical Takings:
- Loretto: Permanent physical occupation is per se taking
- Lucas: Regulation denying all economically beneficial use is taking unless background principles of property law
Mitigating Factors: Reciprocity of advantage, nuisance exception, notice (regulation predates acquisition)
Remedies: Invalidation of regulation, or regulation upheld but compensation paid
Strategic: Rare for federal regulations to constitute taking; property owners must exhaust state procedures (Williamson County, now overruled by Knick)
        """,
        key_factors=[
            "Magnitude of economic impact",
            "Reasonable investment-backed expectations",
            "Physical invasion vs. use restriction",
            "Denial of all beneficial use",
            "Public benefit and reciprocity"
        ],
        primary_authority=[
            "U.S. Const. Amend. V",
            "Penn Central Transp. Co. v. NYC, 438 U.S. 104 (1978)",
            "Lucas v. South Carolina Coastal Council, 505 U.S. 1003 (1992)",
            "Loretto v. Teleprompter Manhattan CATV, 458 U.S. 419 (1982)",
            "Knick v. Township of Scott, 139 S. Ct. 2162 (2019)"
        ],
        burden_holder="Property owner bears burden to demonstrate taking",
        adversary_position="Regulation effects a taking requiring compensation",
        counter_arguments=[
            "No categorical taking: no physical invasion or total wipeout",
            "Penn Central: economic impact not severe, expectations unreasonable, public benefit",
            "Background principles: nuisance exception or pre-existing limit",
            "Reciprocity: owner benefits from similar restrictions on neighbors",
            "Notice: regulation predated acquisition"
        ],
        resolution_strategy="Avoid categorical takings (total prohibition), provide reciprocal benefits, tie to nuisance or harm prevention, grandfather existing uses.",
        entity_scope="All agencies issuing regulations affecting property rights",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Takings claims fact-intensive; Penn Central balancing standard flexible",
        controlling_precedent="Penn Central (1978); Lucas (1992); Loretto (1982)"
    )
]

# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

START_TIME = time.time()
TOTAL_QUERIES = 0
CACHE_HITS = 0
LATENCIES: List[float] = []

# ============================================================================
# CORE LOGIC - TIE-20 COMPONENTS
# ============================================================================

def compute_determinism_hash(query: str, answer: str) -> str:
    """SHA-256 hash for reproducibility verification"""
    content = f"{query}||{answer}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def log_to_audit_trail(query_id: str, query: str, response: QueryResponse) -> None:
    """Append-only JSONL audit log"""
    record = {
        "query_id": query_id,
        "timestamp": response.timestamp,
        "query": query,
        "mode": response.mode,
        "zone": response.zone,
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
        "latency_ms": response.latency_ms,
        "cache_hit": response.cache_hit,
        "determinism_hash": response.determinism_hash,
        "issues_identified": response.issues_identified
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def match_doctrine_cache(query: str) -> Optional[DoctrineBlock]:
    """Doctrine cache layer - 0-200ms response"""
    query_lower = query.lower()
    for block in DOCTRINE_CACHE:
        if any(kw in query_lower for kw in block.keywords):
            return block
    return None

def identify_issues(query: str) -> List[str]:
    """Multi-doctrine decomposition - categorize issues"""
    issues = []
    query_lower = query.lower()

    if any(x in query_lower for x in ["notice", "comment", "rulemaking", "553", "federal register"]):
        issues.append("RULEMAKING")
    if any(x in query_lower for x in ["enforce", "penalty", "violation", "compliance"]):
        issues.append("ENFORCEMENT")
    if any(x in query_lower for x in ["chevron", "auer", "deference", "interpretation"]):
        issues.append("DEFERENCE")
    if any(x in query_lower for x in ["review", "arbitrary", "capricious", "706"]):
        issues.append("JUDICIAL_REVIEW")
    if any(x in query_lower for x in ["cost", "benefit", "economic", "impact", "rfa"]):
        issues.append("COST_BENEFIT")
    if any(x in query_lower for x in ["small business", "small entity", "sbrefa"]):
        issues.append("SMALL_BUSINESS")
    if any(x in query_lower for x in ["major question", "extraordinary", "vast", "clear statement"]):
        issues.append("MAJOR_QUESTIONS")
    if any(x in query_lower for x in ["exhaust", "administrative", "remedy", "petition"]):
        issues.append("EXHAUSTION")

    return issues if issues else ["GENERAL_REGULATORY"]

def apply_epistemic_guardrails(answer: str, confidence: ConfidenceLevel) -> Tuple[str, Optional[str]]:
    """Fact fragility scoring and disclosure caveats"""
    banned = ["guaranteed", "certainly", "definitely will", "no risk", "impossible to"]
    for phrase in banned:
        if phrase in answer.lower():
            logger.warning(f"Banned phrase detected: {phrase}")

    caveat = None
    if confidence in [ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.HIGH_RISK]:
        caveat = "This analysis involves significant legal uncertainty. Consult qualified regulatory counsel before relying on this assessment."
    elif confidence == ConfidenceLevel.DISCLOSURE:
        caveat = "Regulatory landscape evolving. Recent case law may impact this analysis."

    return answer, caveat

def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[str], ConfidenceLevel, bool]:
    """TIE-grade three-layer analysis: cache -> semantic -> deep"""

    # Layer 1: Doctrine Cache (0-200ms)
    block = match_doctrine_cache(query)
    cache_hit = block is not None

    if block and mode == ResponseMode.FAST:
        answer = " ".join(block.conclusion_template)
        sources = block.primary_authority
        confidence = block.confidence
        return answer, sources, confidence, cache_hit

    # Layer 2: Semantic reasoning
    if block:
        if mode == ResponseMode.DEFENSE:
            answer = f"REGULATORY ANALYSIS:\n\n{block.reasoning_framework}\n\nKEY FACTORS: {', '.join(block.key_factors)}\n\nPRIMARY AUTHORITY: {'; '.join(block.primary_authority)}\n\nBURDEN: {block.burden_holder}\n\nCOUNTER-ARGUMENTS: {'; '.join(block.counter_arguments)}\n\nRESOLUTION STRATEGY: {block.resolution_strategy}"
            sources = block.primary_authority
            confidence = block.confidence
            return answer, sources, confidence, cache_hit

        elif mode == ResponseMode.MEMO:
            issues = identify_issues(query)
            answer = f"MEMORANDUM - FEDERAL REGULATORY COMPLIANCE\n\nQUESTION PRESENTED:\n{query}\n\nSHORT ANSWER:\n{' '.join(block.conclusion_template)}\n\nDISCUSSION:\n\nI. LEGAL FRAMEWORK\n{block.reasoning_framework}\n\nII. APPLICATION\n{block.topic} analysis:\n- Burden Holder: {block.burden_holder}\n- Key Factors: {', '.join(block.key_factors)}\n- Adversary Position: {block.adversary_position}\n\nIII. COUNTER-ARGUMENTS\n{chr(10).join('- ' + arg for arg in block.counter_arguments)}\n\nIV. STRATEGIC RECOMMENDATION\n{block.resolution_strategy}\n\nV. AUTHORITY\n{chr(10).join(block.primary_authority)}\n\nCONFIDENCE LEVEL: {block.confidence}\nISSUES IDENTIFIED: {', '.join(issues)}\nAPPLICABLE SCOPE: {block.entity_scope}"
            sources = block.primary_authority
            confidence = block.confidence
            return answer, sources, confidence, cache_hit

    # Layer 3: Deep analysis fallback
    answer = f"Federal regulatory analysis required. Query: {query}. This query may involve: {', '.join(identify_issues(query))}. Recommend consulting Administrative Procedure Act 5 USC 551-559, Executive Orders 12866/13563, and relevant agency-specific statutes. Analysis depends on: (1) statutory authority, (2) procedural compliance (APA Section 553), (3) substantive review (arbitrary and capricious), (4) deference framework post-Loper Bright, (5) cost-benefit justification. Consult regulatory counsel for case-specific application."
    sources = ["5 USC 551-559 (APA)", "Executive Order 12866", "OMB Circular A-4"]
    confidence = ConfidenceLevel.DISCLOSURE
    return answer, sources, confidence, False

def coverage_map_tracker(query: str, cache_hit: bool) -> Dict[str, int]:
    """Track doctrine coverage and gaps"""
    triggered = []
    if cache_hit:
        block = match_doctrine_cache(query)
        if block:
            triggered.append(block.topic)

    return {"triggered_doctrines": triggered, "total_doctrines": len(DOCTRINE_CACHE)}

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Doctrine cache loaded: {len(DOCTRINE_CACHE)} blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down. Total queries: {TOTAL_QUERIES}")

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
    allow_headers=["*"]
)

@app.get("/health", response_model=HealthResponse)
async def health():
    """Comprehensive health check"""
    uptime = time.time() - START_TIME
    hit_rate = (CACHE_HITS / TOTAL_QUERIES * 100) if TOTAL_QUERIES > 0 else 0.0

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=uptime,
        total_queries=TOTAL_QUERIES,
        cache_hit_rate=hit_rate
    )

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """Main query endpoint with TIE-20 components"""
    global TOTAL_QUERIES, CACHE_HITS

    start = time.time()
    query_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    TOTAL_QUERIES += 1

    # Three-layer analysis
    answer, sources, confidence, cache_hit = three_layer_response(req.query, req.mode, req.zone)

    if cache_hit:
        CACHE_HITS += 1

    # Epistemic guardrails
    answer, caveat = apply_epistemic_guardrails(answer, confidence)

    # Issue identification
    issues = identify_issues(req.query)

    # Determinism hash
    det_hash = compute_determinism_hash(req.query, answer)

    latency_ms = int((time.time() - start) * 1000)
    LATENCIES.append(latency_ms)

    response = QueryResponse(
        query_id=query_id,
        timestamp=timestamp,
        mode=req.mode,
        zone=req.zone,
        answer=answer,
        sources=sources,
        confidence=confidence,
        latency_ms=latency_ms,
        cache_hit=cache_hit,
        determinism_hash=det_hash,
        issues_identified=issues,
        epistemic_caveat=caveat
    )

    # Audit trail
    log_to_audit_trail(query_id, req.query, response)

    logger.info(f"Query {query_id} | Mode={req.mode} | Latency={latency_ms}ms | Cache={cache_hit}")

    return response

@app.get("/metrics")
async def metrics():
    """Performance telemetry"""
    avg_latency = sum(LATENCIES) / len(LATENCIES) if LATENCIES else 0
    hit_rate = (CACHE_HITS / TOTAL_QUERIES * 100) if TOTAL_QUERIES > 0 else 0.0

    return {
        "total_queries": TOTAL_QUERIES,
        "cache_hits": CACHE_HITS,
        "cache_hit_rate_pct": hit_rate,
        "avg_latency_ms": avg_latency,
        "p50_latency_ms": sorted(LATENCIES)[len(LATENCIES)//2] if LATENCIES else 0,
        "p95_latency_ms": sorted(LATENCIES)[int(len(LATENCIES)*0.95)] if LATENCIES else 0,
        "doctrine_blocks": len(DOCTRINE_CACHE)
    }

@app.get("/doctrines")
async def list_doctrines():
    """Doctrine coverage map"""
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [block.topic for block in DOCTRINE_CACHE]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
