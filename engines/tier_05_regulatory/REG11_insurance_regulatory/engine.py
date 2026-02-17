"""
REG11 Insurance Regulatory Engine v1.0.0
TIE-Grade Domain Expertise: Insurance Regulatory Compliance

Authority: 11.0 SOVEREIGN | Commander: Bobby Don McWilliams II
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Engine Constants
ENGINE_ID = "REG11"
ENGINE_NAME = "Insurance Regulatory Engine"
VERSION = "1.0.0"
PORT = 9131

# Response Modes
class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

# Confidence Levels
class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

# Issue Categories
class IssueCategory(str, Enum):
    RATE_FILING = "RATE_FILING"
    FORM_APPROVAL = "FORM_APPROVAL"
    SURPLUS_LINES = "SURPLUS_LINES"
    SOLVENCY = "SOLVENCY"
    MARKET_CONDUCT = "MARKET_CONDUCT"
    CLAIMS_HANDLING = "CLAIMS_HANDLING"
    PRODUCER_LICENSING = "PRODUCER_LICENSING"
    UNFAIR_PRACTICES = "UNFAIR_PRACTICES"
    REINSURANCE = "REINSURANCE"
    GUARANTY_ASSOCIATION = "GUARANTY_ASSOCIATION"
    FINANCIAL_REPORTING = "FINANCIAL_REPORTING"
    EXAMINATION = "EXAMINATION"

# Analysis Zones
class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

@dataclass
class DoctrineBlock:
    """Single reusable insurance regulatory reasoning block"""
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
    category: IssueCategory

@dataclass
class QueryMetrics:
    """Telemetry for single query"""
    query_id: str
    timestamp: float
    mode: str
    category: Optional[str]
    cache_hit: bool
    cache_latency_ms: float
    semantic_latency_ms: float
    total_latency_ms: float
    doctrines_triggered: List[str]
    confidence_level: str
    determinism_hash: str

class TelemetryCollector:
    """Performance metrics aggregation"""
    def __init__(self):
        self.queries: List[QueryMetrics] = []
        self.start_time = time.time()

    def record(self, metrics: QueryMetrics):
        self.queries.append(metrics)

    def get_stats(self) -> Dict[str, Any]:
        if not self.queries:
            return {"error": "no_queries"}
        total = len(self.queries)
        cache_hits = sum(1 for q in self.queries if q.cache_hit)
        avg_latency = sum(q.total_latency_ms for q in self.queries) / total
        return {
            "total_queries": total,
            "cache_hit_rate": cache_hits / total,
            "avg_latency_ms": round(avg_latency, 2),
            "uptime_seconds": round(time.time() - self.start_time, 2),
            "queries_per_hour": round(total / ((time.time() - self.start_time) / 3600), 2)
        }

class DriftWatcher:
    """Detect doctrine drift over time"""
    def __init__(self):
        self.baseline_hashes: Dict[str, str] = {}

    def set_baseline(self, topic: str, content: str):
        self.baseline_hashes[topic] = hashlib.sha256(content.encode()).hexdigest()

    def check_drift(self, topic: str, content: str) -> bool:
        current = hashlib.sha256(content.encode()).hexdigest()
        baseline = self.baseline_hashes.get(topic)
        return baseline is not None and baseline != current

class CoverageMap:
    """Track triggered vs missed doctrines"""
    def __init__(self):
        self.triggered: Set[str] = set()
        self.available: Set[str] = set()

    def mark_available(self, topic: str):
        self.available.add(topic)

    def mark_triggered(self, topic: str):
        self.triggered.add(topic)

    def get_gaps(self) -> List[str]:
        return list(self.available - self.triggered)

    def get_coverage_rate(self) -> float:
        if not self.available:
            return 0.0
        return len(self.triggered) / len(self.available)

# Doctrine Cache (25+ blocks with REAL insurance regulatory content)
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="McCarran-Ferguson Act Federal Antitrust Exemption",
        keywords=["mccarran-ferguson", "antitrust", "federal exemption", "state regulation", "business of insurance"],
        conclusion_template=[
            "The McCarran-Ferguson Act provides limited federal antitrust exemption for the business of insurance",
            "State regulation must be comprehensive for exemption to apply",
            "Exemption does not cover boycott, coercion, or intimidation"
        ],
        reasoning_framework="""
        15 USC 1011-1015 grants states authority to regulate insurance and provides federal antitrust
        exemption to the extent state law regulates. The exemption applies to the 'business of insurance'
        (spreading and underwriting risk). Courts apply three-part test: (1) practice must involve
        risk transfer or underwriting, (2) practice must be integral to insurer-policyholder relationship,
        (3) practice must be limited to insurance industry. Even if all three met, exemption does not
        apply to agreements to boycott, coerce, or intimidate. Sherman Act and Clayton Act apply if
        state does not regulate the conduct. FTC Act applies unless state regulation exists.
        Royal Drug 440 US 205 (1979) narrowed 'business of insurance' definition. Union Labor Life
        Ins. v. Pireno 458 US 119 (1982) established three-part test. State must 'regulate' not merely
        allow the practice. Adequacy of state regulation is fact-specific.
        """,
        key_factors=[
            "Three-part test: risk transfer, integral to insurer-policyholder relationship, limited to industry",
            "Boycott/coercion/intimidation exception removes all exemption",
            "State must affirmatively regulate, not merely permit",
            "Exemption applies to Sherman/Clayton, not FTC Act if state regulates",
            "Royal Drug and Pireno narrow scope significantly"
        ],
        primary_authority=["15 USC 1011-1015", "Royal Drug 440 US 205", "Union Labor Life 458 US 119"],
        burden_holder="Party asserting exemption bears burden of proving all three elements",
        adversary_position="Conduct is commercial activity not integral to insurance; state law inadequate",
        counter_arguments=[
            "Conduct involves price-fixing among competitors",
            "No state statute specifically approves the practice",
            "Conduct harms consumers without risk-spreading justification",
            "Exemption is disfavored and narrowly construed"
        ],
        resolution_strategy="Apply three-part test strictly; examine state statutes for affirmative authorization; distinguish commercial vs insurance activity",
        entity_scope="Insurers, agents, trade associations, reinsurers claiming antitrust exemption",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established Supreme Court precedent with clear multi-factor test",
        controlling_precedent="Royal Drug 440 US 205; Union Labor Life 458 US 119",
        category=IssueCategory.UNFAIR_PRACTICES
    ),
    DoctrineBlock(
        topic="Texas Rate Filing Prior Approval Requirement",
        keywords=["rate filing", "prior approval", "texas insurance code", "TDI", "actuarial justification"],
        conclusion_template=[
            "Texas requires prior TDI approval for property and casualty insurance rates",
            "Rates must not be excessive, inadequate, or unfairly discriminatory",
            "Insurers must file actuarial justification supporting proposed rates"
        ],
        reasoning_framework="""
        Texas Insurance Code Art. 5.13 and Chapter 2251 mandate prior approval of property and casualty
        insurance rates. Insurer must file rates with supporting actuarial data at least 30 days before
        use. TDI may disapprove if rates are excessive, inadequate, or unfairly discriminatory. 'Excessive'
        means rates are unreasonably high for coverage provided. 'Inadequate' means rates are insufficient
        to sustain future obligations. 'Unfairly discriminatory' means price differences not justified
        by cost differences or reasonably anticipated experience. Actuarial justification must include
        loss experience, trend factors, expense loadings, profit margin. Rating factors (territory, class,
        individual risk characteristics) must be actuarially sound. TDI has 60 days to act; silence = approval.
        28 TAC 5.9310-5.9315 specify filing requirements and actuarial standards. Appeal lies to Travis
        County district court. Life/health uses file-and-use system, not prior approval.
        """,
        key_factors=[
            "Prior approval required for property/casualty; file-and-use for life/health",
            "30-day waiting period before rate effective unless emergency approval",
            "Actuarial justification must support all rating factors and profit margins",
            "Three statutory prohibitions: excessive, inadequate, unfairly discriminatory",
            "TDI has 60-day review window; failure to act = deemed approved"
        ],
        primary_authority=["Texas Insurance Code Art. 5.13", "TIC Chapter 2251", "28 TAC 5.9310-5.9315"],
        burden_holder="Insurer bears burden of proving rates are not excessive, inadequate, or unfairly discriminatory",
        adversary_position="Rates lack actuarial support; profit margin excessive; classification unfairly discriminatory",
        counter_arguments=[
            "Industry-wide loss ratios do not support proposed increase",
            "Expense loadings include non-insurance costs",
            "Classification based on proxies (credit score) not causally related to loss",
            "Proposed rate exceeds competitive market rate"
        ],
        resolution_strategy="Produce detailed actuarial memorandum with loss triangles, trend analysis, expense studies, profit provision justification; respond to TDI interrogatories within 10 days",
        entity_scope="Property/casualty insurers writing in Texas",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established regulatory framework with detailed administrative rules",
        controlling_precedent="State Farm v. TDI (Travis County litigation on rate disapprovals)",
        category=IssueCategory.RATE_FILING
    ),
    DoctrineBlock(
        topic="Surplus Lines Eligibility and Tax Code Section 226",
        keywords=["surplus lines", "non-admitted", "diligent search", "stamping office", "tax code 226"],
        conclusion_template=[
            "Surplus lines placement requires diligent search of admitted market and placement with eligible non-admitted insurer",
            "Texas Tax Code Section 226 imposes 4.85 percent premium tax on surplus lines",
            "Agent must remit tax to stamping office within 60 days of policy effective date"
        ],
        reasoning_framework="""
        Texas Insurance Code Chapter 981 governs surplus lines. Agent may place coverage with non-admitted
        insurer only if: (1) diligent search of admitted market yields no coverage, (2) non-admitted
        insurer meets financial eligibility (minimum capital/surplus, ratings), (3) placement reported
        to Texas Surplus Lines Stamping Office within 60 days. 'Diligent search' requires written
        declinations from at least three admitted insurers or affidavit that coverage unavailable.
        Certain risks exempt from diligent search (large commercial risks over $100,000 premium).
        Eligible surplus lines insurers must have minimum $15M capital and surplus or appear on NAIC
        Quarterly Listing. Texas Tax Code Section 226.051 imposes 4.85 percent tax on gross premium
        (higher than admitted insurer premium tax of 1.6 percent). Agent responsible for collecting
        tax from insured and remitting to stamping office with Form RP-1. Failure to remit = agent
        personally liable. Stamping office forwards tax to Comptroller. No coverage for workers'
        compensation via surplus lines (exclusive state fund monopoly broken 1991 but surplus lines
        still prohibited). Recent NRRA preempts some state surplus lines regulation for non-resident
        agents placing coverage for home-state insured.
        """,
        key_factors=[
            "Diligent search required unless exempt (large commercial risk exception)",
            "Non-admitted insurer must meet financial eligibility: $15M capital/surplus or NAIC Quarterly Listing",
            "4.85 percent premium tax vs 1.6 percent for admitted insurers",
            "Agent personally liable for uncollected/unremitted tax",
            "60-day reporting deadline to stamping office"
        ],
        primary_authority=["Texas Insurance Code Chapter 981", "Texas Tax Code Section 226", "28 TAC 15.1-15.30"],
        burden_holder="Agent bears burden of proving diligent search and insurer eligibility; agent liable for tax collection",
        adversary_position="Diligent search not conducted; insurer ineligible; tax not remitted; coverage voidable",
        counter_arguments=[
            "Admitted market could have provided coverage with modifications",
            "Affidavit of unavailability insufficient without actual declinations",
            "Non-admitted insurer below $15M capital at placement",
            "Agent failed to collect tax from insured; personal liability follows"
        ],
        resolution_strategy="Maintain declination letters or detailed affidavit; verify insurer on NAIC list before binding; collect tax at inception and remit timely; use Form RP-1 for all placements",
        entity_scope="Surplus lines agents, wholesale brokers, commercial insureds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strict statutory framework with bright-line tests and defined procedures",
        controlling_precedent="Continental Cas. Co. v. Functional Restoration (5th Cir. on surplus lines compliance)",
        category=IssueCategory.SURPLUS_LINES
    ),
    DoctrineBlock(
        topic="Risk-Based Capital (RBC) Requirements and Solvency Monitoring",
        keywords=["RBC", "solvency", "NAIC", "corrective action", "ACL", "CAL", "mandatory control"],
        conclusion_template=[
            "Insurers must maintain capital and surplus above RBC thresholds to avoid regulatory action",
            "NAIC RBC formula calculates required capital based on asset, underwriting, credit, and operational risk",
            "Four action levels trigger progressively severe regulatory intervention: company action, regulatory action, authorized control, mandatory control"
        ],
        reasoning_framework="""
        NAIC Risk-Based Capital Model Act (adopted by all states including Texas via TIC 404.001-.059)
        establishes formula-based solvency standard. Insurer calculates Total Adjusted Capital (TAC)
        and compares to Authorized Control Level (ACL). ACL = 50 percent of RBC. Four action levels:
        (1) Company Action Level (200 percent RBC) requires insurer to submit plan to commissioner,
        (2) Regulatory Action Level (150 percent RBC) requires commissioner to examine and issue order,
        (3) Authorized Control Level (100 percent RBC) permits commissioner to place insurer in
        rehabilitation or liquidation, (4) Mandatory Control Level (70 percent RBC) requires commissioner
        to place insurer under regulatory control. RBC formula incorporates: asset risk (C-1), underwriting
        risk for reserves (C-2), asset/liability matching risk (C-3), business risk (C-4), operational risk.
        Life, P&C, and health insurers have separate formulas. Annual RBC report due March 1 following
        year-end. Trend test compares current to prior year; negative trend 10 percent or more triggers
        action. Confidential unless insurer falls below CAL. Commissioner has discretion to waive action
        if decline due to extraordinary circumstances. RBC not sole solvency measure; states also examine
        liquidity, reinsurance, reserve adequacy, investment quality.
        """,
        key_factors=[
            "Four action levels: 200 percent (company action), 150 percent (regulatory action), 100 percent (authorized control), 70 percent (mandatory control)",
            "Total Adjusted Capital compared to risk-weighted required capital",
            "Separate formulas for life, P&C, health insurers",
            "Negative trend test applies even if above action level",
            "Report due March 1; confidential unless below CAL"
        ],
        primary_authority=["NAIC RBC Model Act", "Texas Insurance Code 404.001-.059", "28 TAC 3.901-3.909"],
        burden_holder="Insurer must maintain adequate capital and file accurate RBC reports; burden shifts to commissioner to justify control action",
        adversary_position="RBC formula overstates risk; extraordinary event justifies waiver; voluntary surplus contribution cures deficiency",
        counter_arguments=[
            "Insurer inflated TAC by including non-admitted assets",
            "Reserves understated to improve RBC ratio",
            "Reinsurance credits for unauthorized reinsurer improperly included",
            "Trend test decline requires immediate corrective plan"
        ],
        resolution_strategy="File accurate RBC report with full disclosure; if below action level prepare detailed corrective plan with capital infusion timeline; engage actuary and auditor; consider extraordinary dividend restrictions",
        entity_scope="All licensed insurers writing life, P&C, or health coverage",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Uniform national standard with objective formula and clear thresholds",
        controlling_precedent="NAIC Model Act uniformly adopted; little case law due to administrative nature",
        category=IssueCategory.SOLVENCY
    ),
    DoctrineBlock(
        topic="Market Conduct Examinations and NAIC Market Regulation Handbook",
        keywords=["market conduct exam", "NAIC handbook", "claims practices", "underwriting", "sales practices", "complaint ratio"],
        conclusion_template=[
            "State insurance departments conduct market conduct exams to ensure compliance with insurance laws and fair treatment of policyholders",
            "NAIC Market Regulation Handbook provides uniform examination standards and procedures",
            "Examiners review claims handling, underwriting, rating, advertising, producer licensing, and complaint ratios"
        ],
        reasoning_framework="""
        State insurance codes grant commissioner authority to examine insurer market conduct at any time.
        Texas Insurance Code 401.051-.155 and 28 TAC 1.501-.515 govern examination process. NAIC Market
        Regulation Handbook (adopted by TDI) provides examination standards for: claims practices
        (timely acknowledgment, investigation, payment; unfair settlement offers; misrepresentation
        of policy provisions), underwriting and rating (unfair discrimination, adherence to filed rates,
        proper classification), producer licensing and appointment (training, errors and omissions,
        termination reporting), advertising and sales (disclosure, misrepresentation, twisting, churning),
        policyholder service (billing, cancellation/non-renewal notice, policy delivery), complaint handling
        (complaint ratio vs industry average; responsiveness). Examination notice gives 30 days to produce
        records. Examiners sample policies, claims, underwriting files, advertising materials. Exit
        conference presents preliminary findings. Draft report allows 30-day response. Final report
        may include violations requiring corrective action plan, fines, or license sanctions. Insurer
        pays exam costs (per diem plus expenses). Targeted exams focus on specific issue (claims,
        underwriting); comprehensive exams review all areas. Exam frequency risk-based: high-complaint
        insurers examined more often. NAIC adopted Compliance Self-Evaluation as alternative for low-risk
        insurers. Exam report public record 30 days after final.
        """,
        key_factors=[
            "NAIC Handbook provides uniform standards adopted by TDI",
            "Examiners review claims, underwriting, rating, advertising, licensing, complaints",
            "File sampling methodology determines scope (random, targeted)",
            "30-day response period to draft report before final",
            "Insurer pays examination costs; final report becomes public record"
        ],
        primary_authority=["Texas Insurance Code 401.051-.155", "28 TAC 1.501-.515", "NAIC Market Regulation Handbook"],
        burden_holder="Insurer must produce records timely and cooperate; burden to rebut findings in response to draft report",
        adversary_position="Systemic violations found; corrective action plan inadequate; fines and sanctions warranted",
        counter_arguments=[
            "Sampling methodology biased; not statistically valid",
            "Violations isolated to individual adjuster; corrective action already taken",
            "Underwriting guidelines followed; no unfair discrimination",
            "Complaint ratio inflated by single large event; not indicative of practices"
        ],
        resolution_strategy="Cooperate fully with exam; designate compliance officer as liaison; conduct internal audit pre-exam; respond to draft report with detailed rebuttals and corrective plan; negotiate consent order to avoid public sanctions",
        entity_scope="All insurers and producers subject to TDI jurisdiction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established regulatory framework with detailed procedural rules",
        controlling_precedent="Administrative law standards apply; courts defer to agency expertise unless arbitrary/capricious",
        category=IssueCategory.MARKET_CONDUCT
    ),
    DoctrineBlock(
        topic="Unfair Claims Settlement Practices Act (UCSPA)",
        keywords=["UCSPA", "unfair claims", "prompt payment", "misrepresentation", "low-ball offer", "bad faith"],
        conclusion_template=[
            "UCSPA prohibits 12 categories of unfair claims practices including misrepresentation, delay, and low-ball offers",
            "Pattern or practice required; single violation insufficient for regulatory action",
            "Texas prompt payment statute imposes strict timelines and penalty interest for late payment"
        ],
        reasoning_framework="""
        Texas Insurance Code 541.060 adopts NAIC Unfair Claims Settlement Practices Model Act. Prohibits:
        (1) misrepresenting policy provisions, (2) failing to acknowledge/act on claims timely,
        (3) failing to adopt reasonable claims standards, (4) refusing to pay without reasonable investigation,
        (5) failing to affirm/deny coverage timely, (6) not attempting good faith settlement when liability
        clear, (7) compelling litigation by offering substantially less than ultimately recovered,
        (8) delaying investigation/payment by requiring unnecessary proof, (9) failing to explain denial,
        (10) failing to provide claim forms/assistance, (11) making claims contingent on giving recorded
        statement when not reasonably required, (12) engaging in pattern of failing to settle in good faith.
        'Pattern or practice' requires multiple violations showing general business practice, not isolated
        acts. Texas Insurance Code 542.051-.061 (Prompt Payment of Claims Act) imposes strict timelines:
        15 days to acknowledge claim, 15 days to request additional info, 5 business days to accept/reject
        after receiving all info. Failure to comply results in 18 percent annual interest penalty from
        date claim filed. Interest mandatory, not discretionary. UCSPA violations give rise to private
        cause of action under Chapter 541 for actual damages, but punitive damages require knowing
        violation. Common law bad faith also available (breach of duty of good faith and fair dealing).
        TDI may impose administrative penalties up to $25,000 per violation for pattern/practice.
        """,
        key_factors=[
            "12 prohibited practices; pattern or practice required for regulatory action",
            "Prompt payment timelines: 15 days acknowledge, 15 days request info, 5 days accept/reject",
            "18 percent penalty interest for late payment (mandatory, not discretionary)",
            "Private cause of action under 541.060; punitive damages require knowing violation",
            "Common law bad faith separate claim (breach of duty of good faith)"
        ],
        primary_authority=["Texas Insurance Code 541.060", "TIC 542.051-.061", "Vail v. Texas Farm Bureau 754 SW2d 129"],
        burden_holder="Claimant bears burden of proving pattern/practice for UCSPA; insurer bears burden of reasonable investigation and timely payment",
        adversary_position="Single violation or mistake insufficient; no pattern shown; investigation reasonable; low offer based on medical review",
        counter_arguments=[
            "Multiple claims delayed beyond statutory period showing pattern",
            "No reasonable basis to deny; liability clear and damages documented",
            "Low-ball offer compelled litigation; recovery 3x offer shows lack of good faith",
            "Requested proof not reasonably necessary (surveillance when medical records sufficient)"
        ],
        resolution_strategy="Document all claims handling steps with timestamps; ensure acknowledgment within 15 days; make settlement offers based on thorough investigation; explain denial with specific policy provisions; train adjusters on UCSPA compliance",
        entity_scope="All insurers and third-party administrators handling claims in Texas",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statutory framework with objective timelines; case law clarifies pattern/practice standard",
        controlling_precedent="Vail v. Texas Farm Bureau 754 SW2d 129 (pattern or practice required); Aranda v. Insurance Co. of North America 748 SW2d 210 (prompt payment interest mandatory)",
        category=IssueCategory.CLAIMS_HANDLING
    ),
    DoctrineBlock(
        topic="Producer Licensing and Appointment Requirements",
        keywords=["producer license", "appointment", "continuing education", "E&O", "termination reporting"],
        conclusion_template=[
            "Producers must hold valid license and company appointment to sell insurance in Texas",
            "Continuing education (CE) required: 30 hours every two years including 2 hours ethics",
            "Insurers must report producer termination for cause within 30 days"
        ],
        reasoning_framework="""
        Texas Insurance Code Chapter 4051-4060 governs producer licensing. Applicant must pass state exam,
        complete pre-licensing education, submit fingerprints, and pay fee. License categories: life,
        accident and health, property, casualty, personal lines, adjuster. Non-resident license available
        via reciprocity if home state grants Texas producers same. License renewable every two years
        on birth month. Continuing education: 30 credit hours per 2-year period including 2 hours ethics
        and 2 hours on annuities (for life-licensed). CE waived for producers over age 60 with 20+ years
        licensure. Appointment required for each insurer producer represents. Insurer files appointment
        via NIPR within 15 days of contracting. Appointment fee paid by insurer. Termination for cause
        must be reported to TDI within 30 days on Termination for Cause form explaining misconduct.
        Failure to report = administrative penalty. Producer must notify TDI of change of address within
        30 days. Errors and Omissions (E&O) insurance required for health producers under ACA; recommended
        for all. TDI may deny, suspend, or revoke license for: providing false info, misappropriation,
        fraud, conviction of felony, twisting, rebating, unfair discrimination. Administrative penalties
        up to $25,000 per violation. Resident license held for 48 months required before sponsoring new
        producers. Temporary license available for 180 days in case of death/disability of licensed producer.
        """,
        key_factors=[
            "State exam, pre-licensing education, fingerprints required for initial license",
            "30 CE hours per 2 years (2 ethics, 2 annuities for life-licensed)",
            "Appointment filed by insurer within 15 days; termination for cause reported within 30 days",
            "E&O insurance required for health producers (ACA mandate)",
            "License revocable for fraud, misappropriation, twisting, rebating, felony conviction"
        ],
        primary_authority=["Texas Insurance Code Chapter 4051-4060", "28 TAC 19.101-19.1019"],
        burden_holder="Producer bears burden of maintaining valid license and CE compliance; insurer responsible for timely appointment and termination reporting",
        adversary_position="Producer unlicensed or appointment lapsed; commissions earned during unlicensed period forfeited",
        counter_arguments=[
            "Producer failed to complete CE before renewal deadline; license lapsed",
            "Insurer delayed appointment filing; producer sold policies without valid appointment",
            "Termination for cause not reported; subsequent employer unaware of prior misconduct",
            "Conviction of felony involving dishonesty requires automatic revocation"
        ],
        resolution_strategy="Track CE completion 90 days before renewal; use TDI-approved providers; maintain appointment list; immediately report terminations for cause; conduct background checks on new hires; require E&O coverage in producer agreements",
        entity_scope="All insurance producers (agents, brokers, adjusters) operating in Texas",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Detailed statutory and regulatory framework with clear requirements",
        controlling_precedent="Administrative enforcement standards; courts uphold TDI licensing actions unless arbitrary",
        category=IssueCategory.PRODUCER_LICENSING
    ),
    DoctrineBlock(
        topic="Texas Guaranty Association Coverage and Assessments",
        keywords=["guaranty association", "TIGA", "TAHIGA", "insolvent insurer", "assessment", "covered claims"],
        conclusion_template=[
            "Texas Insurance Guaranty Association (TIGA) covers property/casualty claims when insurer becomes insolvent",
            "Coverage capped at $300,000 per claim; certain exclusions apply (e.g., punitive damages, reinsurance)",
            "Solvent insurers assessed to fund TIGA based on proportionate share of premiums written"
        ],
        reasoning_framework="""
        Texas Insurance Code Chapter 462 creates TIGA to protect policyholders of insolvent P&C insurers.
        All P&C insurers writing in Texas must be members. When member insurer declared insolvent,
        TIGA steps into claims obligations. Coverage limits: $300,000 per covered claim; $100,000 per
        claimant for return of unearned premium. Covered claims include first-party property, liability,
        workers compensation (subject to separate workers comp guaranty fund). Excluded: punitive damages,
        fines, penalties, interest prior to insolvency order, reinsurance (reinsurer's claim), claims
        filed after deadline (18 months post-insolvency). Deductibles and policy limits apply as if
        insurer still solvent. TIGA funded by assessments on solvent member insurers. Board of directors
        determines assessment amount based on funding needs. Each insurer assessed proportionate to
        premiums written in relevant line of business. Assessment limited to 2 percent of premiums
        annually; excess carried forward. Insurers may recoup assessments via premium surcharges or
        tax credits. Texas Association of Health Insurance Guaranty Association (TAHIGA) covers health
        insurers similarly. Life and annuity guaranty association (TLIGA) separate. Insured must file
        proof of claim with TIGA; 1-year limitations period from date of insolvency order. TIGA may
        settle, compromise, or litigate claims. Statute of limitations tolled during insolvency proceeding.
        No punitive damages against TIGA. Insurers may not self-insure out of guaranty association obligations.
        """,
        key_factors=[
            "$300,000 per claim cap; $100,000 for unearned premium",
            "Punitive damages, pre-insolvency interest, reinsurance claims excluded",
            "Assessment on solvent insurers capped at 2 percent of premiums annually",
            "Insurers recoup via premium surcharge or tax credit",
            "1-year limitations to file claim with TIGA from insolvency order"
        ],
        primary_authority=["Texas Insurance Code Chapter 462 (TIGA)", "Chapter 463 (TAHIGA)", "Chapter 464 (TLIGA)"],
        burden_holder="Claimant bears burden of timely filing proof of claim with TIGA; TIGA may assert policy defenses available to insolvent insurer",
        adversary_position="Claim exceeds cap; claimant delayed filing past deadline; claim for punitive damages not covered",
        counter_arguments=[
            "Policy limit $1M but TIGA cap $300,000; claimant suffers $700,000 shortfall",
            "Assessment recoupment via premium increase harms policyholders of solvent insurers",
            "Claimant unaware of insolvency; filing deadline equitable tolling warranted",
            "Reinsurer should contribute to TIGA funding (but excluded by statute)"
        ],
        resolution_strategy="Monitor insurer financial ratings to anticipate insolvency; file proof of claim immediately upon insolvency order; accept TIGA settlement offers if within cap; coordinate multiple claims from same insured to maximize recovery; seek tax credit for assessments paid",
        entity_scope="P&C insurers, policyholders of insolvent insurers, claimants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statutory guaranty association framework uniform across states; Texas caps and procedures well-established",
        controlling_precedent="Guaranty association statutes construed to effectuate policyholder protection; coverage disputes governed by policy terms",
        category=IssueCategory.GUARANTY_ASSOCIATION
    ),
    DoctrineBlock(
        topic="Form Approval and Policy Language Requirements",
        keywords=["form approval", "policy language", "readability", "file and use", "non-disapproval"],
        conclusion_template=[
            "Texas requires insurers to file policy forms for approval or non-disapproval depending on line of business",
            "Forms must be clear, unambiguous, and not contrary to law or public policy",
            "Readability standards require plain language and minimum font size"
        ],
        reasoning_framework="""
        Texas Insurance Code 2301.006 and 2301.007 establish form filing requirements. Property/casualty
        forms use file-and-use system: insurer files with TDI and may use immediately unless TDI
        disapproves within 60 days. Life/health forms require prior approval: insurer may not use
        until TDI approves. HMO forms subject to prior approval. Workers compensation forms promulgated
        by TDI; insurers may not deviate. Standard forms (ISO, AAIS) filed once by organization; insurers
        adopt by reference. TDI reviews for: compliance with statutes, clarity and lack of ambiguity,
        fair and not misleading, not contrary to public policy. Readability standards: plain language
        (avoid legalese), minimum 10-point font, clearly titled sections, definitions section, table
        of contents for policies over 3,000 words, index of endorsements. Ambiguities construed against
        drafter (contra proferentem). Reasonable expectations doctrine: insured's objectively reasonable
        expectations honored even if policy terms technically exclude. Unfair/deceptive policy terms
        prohibited. Disclosure requirements: mandated statutory notices (e.g., Texas windstorm exclusion
        notice for coastal properties). Electronic delivery permitted if insured consents. Form amendments
        require re-filing. Disapproved forms may be appealed to TDI; hearing before administrative law
        judge; appeal to Travis County district court.
        """,
        key_factors=[
            "File-and-use for P&C; prior approval for life/health; workers comp forms promulgated by TDI",
            "60-day TDI review period for file-and-use; silence = approval",
            "Plain language, 10-point minimum font, clear structure required",
            "Ambiguities construed against insurer; reasonable expectations doctrine applies",
            "Statutory disclosure notices required (e.g., windstorm exclusion)"
        ],
        primary_authority=["Texas Insurance Code 2301.006-.007", "28 TAC 3.3001-.3009"],
        burden_holder="Insurer bears burden of drafting clear and lawful forms; burden to prove form complies with statutes and readability standards",
        adversary_position="Form ambiguous or misleading; exclusion buried in dense text; violates readability standards; contrary to public policy",
        counter_arguments=[
            "Exclusion language clear on face but insured had reasonable expectation of coverage",
            "Font size below 10-point; definitions not in separate section",
            "Mandated statutory notice omitted or inadequate",
            "Form uses ISO template but insurer endorsement conflicts"
        ],
        resolution_strategy="Use TDI-approved standard forms (ISO, AAIS) where possible; submit custom forms 90 days before intended use; conduct readability audit; include all mandated notices; avoid ambiguous exclusions; obtain legal review before filing",
        entity_scope="All insurers filing policy forms with TDI",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established regulatory framework with detailed filing procedures",
        controlling_precedent="National Union Fire Ins. v. CBI Industries (contra proferentem); Arnold v. National County Mut. (reasonable expectations doctrine)",
        category=IssueCategory.FORM_APPROVAL
    ),
    DoctrineBlock(
        topic="Reinsurance Credit and Unauthorized Reinsurer Collateral Requirements",
        keywords=["reinsurance", "credit for reinsurance", "unauthorized reinsurer", "collateral", "trust fund"],
        conclusion_template=[
            "Insurers may take statutory financial statement credit for reinsurance only if reinsurer authorized or provides collateral",
            "Authorized reinsurers include licensed US insurers and accredited/certified reinsurers on TDI list",
            "Unauthorized reinsurers must post 100 percent collateral (cash, letter of credit, trust fund) for credit"
        ],
        reasoning_framework="""
        Texas Insurance Code Chapter 493 governs reinsurance credit. Ceding insurer may reduce liabilities
        on statutory financial statement only for reinsurance ceded to authorized reinsurer or secured
        by collateral. 'Authorized reinsurer' includes: (1) insurer licensed in Texas, (2) accredited
        reinsurer (licensed in another state, files financial statements, meets minimum capital/surplus,
        submits to TDI jurisdiction), (3) certified reinsurer (meets TDI financial strength and rating
        requirements; credit limited by tier: Tier 1 (S&P A- or higher) 100 percent, Tier 2 (BBB) 75 percent,
        Tier 3 (BB) 50 percent, Tier 4 (B+) 20 percent). Unauthorized reinsurer: no license, accreditation,
        or certification. Credit allowed only if 100 percent collateral posted. Collateral forms: cash,
        letter of credit from qualified bank, securities listed by SVO, clean irrevocable trust agreement.
        Trust must be under New York or Texas law, with qualified trustee, sole benefit of ceding insurer.
        Collateral must be maintained throughout life of reinsured obligations. Reduction requires actuarial
        certification. Reinsurance agreement must include: insolvency clause (reinsurer pays claims even
        if ceding insurer insolvent), offset clause (ceding insurer may offset balances), arbitration
        clause (dispute resolution). Fronting arrangements (ceding insurer cedes 100 percent to unauthorized
        reinsurer) heavily scrutinized; TDI may disallow credit if arrangement lacks substance. Multi-year
        prospective reinsurance requires approval. Credit for reinsurance reduces ceding insurer's RBC
        requirement but TDI may add back if reinsurer financial strength deteriorates.
        """,
        key_factors=[
            "Credit allowed for authorized (licensed, accredited, certified) reinsurers",
            "Certified reinsurer credit limited by tier based on rating (100 percent/75 percent/50 percent/20 percent)",
            "Unauthorized reinsurer requires 100 percent collateral (cash, LOC, securities, trust)",
            "Insolvency clause required in all reinsurance agreements",
            "Fronting arrangements scrutinized; TDI may disallow credit if lacks substance"
        ],
        primary_authority=["Texas Insurance Code Chapter 493", "28 TAC 15.101-.123", "NAIC Credit for Reinsurance Model Law"],
        burden_holder="Ceding insurer bears burden of proving reinsurer authorized or collateral adequate; must monitor collateral sufficiency",
        adversary_position="Reinsurer not on accredited list; collateral below 100 percent; trust agreement deficient; fronting lacks substance",
        counter_arguments=[
            "Reinsurer financial strength deteriorated post-accreditation; TDI should revoke",
            "Letter of credit expires before reinsured obligations run off",
            "Trust agreement allows trustee discretion to release funds (not clean irrevocable)",
            "Ceding insurer retained no underwriting risk; fronting for unauthorized reinsurer improper"
        ],
        resolution_strategy="Use only authorized/accredited/certified reinsurers from TDI list; for unauthorized reinsurers require 100 percent trust with irrevocable terms and qualified trustee; include standard insolvency and offset clauses; obtain actuarial opinion before reducing collateral; avoid fronting arrangements or structure with substance (ceding insurer retains meaningful risk)",
        entity_scope="All insurers ceding reinsurance and seeking statutory financial statement credit",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Uniform state adoption of NAIC model law with detailed collateral and authorization requirements",
        controlling_precedent="Administrative standards govern; courts uphold TDI disallowance of credit for non-compliant reinsurance",
        category=IssueCategory.REINSURANCE
    ),
    DoctrineBlock(
        topic="NAIC Model Laws and Uniform State Adoption",
        keywords=["NAIC", "model law", "uniform adoption", "interstate compact", "accreditation"],
        conclusion_template=[
            "NAIC develops model insurance laws and regulations adopted by states to promote uniformity",
            "State adoption voluntary but NAIC accreditation program incentivizes compliance",
            "Key models include RBC, holding company regulation, market conduct, credit for reinsurance"
        ],
        reasoning_framework="""
        National Association of Insurance Commissioners (NAIC) is voluntary organization of state insurance
        regulators. NAIC develops model laws and regulations to promote regulatory uniformity across
        states. Models are recommendations; each state legislature/insurance department decides whether
        to adopt. NAIC Financial Regulation Standards and Accreditation Program requires states to
        adopt certain models for accreditation (ability to conduct financial examinations of multi-state
        insurers). Accreditation requirements include: risk-based capital, holding company regulation
        (Form B/C/D/E filings), insurance holding company system, receivership, credit for reinsurance,
        annual financial reporting. Non-accredited states lose authority to examine out-of-state insurers;
        domestic insurers face obstacles in other states. Texas and all major states accredited. Key
        NAIC models: RBC Model Act, Unfair Claims Practices Act, Market Conduct Model Law, Credit for
        Reinsurance, Surplus Lines, Producer Licensing Model Act, Holding Company Model Act, Standard
        Valuation Law, Own Risk and Solvency Assessment (ORSA), Life and Health Insurance Guaranty
        Association Model Act. Some models adopted uniformly (RBC, holding company); others vary by
        state. NAIC also produces model regulations (detail beneath statute level) and guidelines
        (best practices). Interstate Insurance Product Regulation Compact (IIPRC) allows multi-state
        approval of life/annuity/disability products via single filing. 47 states participate.
        Speed-to-market benefit but limited to certain product types. NAIC accreditation reviewed
        every 5 years. Failure to maintain accreditation threatens state insurance department funding
        and authority. NAIC also operates data systems (financial statement filings, producer licensing
        database, complaint database).
        """,
        key_factors=[
            "NAIC models voluntary but accreditation program creates strong incentive for adoption",
            "Accreditation requires adoption of core models: RBC, holding company, credit for reinsurance",
            "Non-accredited states lose examination authority over out-of-state insurers",
            "IIPRC compact allows single filing for life/annuity/disability products in 47 states",
            "Texas accredited and participates in IIPRC"
        ],
        primary_authority=["NAIC Model Laws and Regulations", "NAIC Accreditation Standards", "Interstate Insurance Product Regulation Compact"],
        burden_holder="States bear burden of maintaining accreditation; insurers benefit from uniformity but must comply with variations where states deviate",
        adversary_position="State law deviates from NAIC model; insurer must comply with state-specific requirements",
        counter_arguments=[
            "Texas adopted NAIC model but added stricter requirements (e.g., higher RBC thresholds)",
            "IIPRC approval does not preempt state variations (e.g., non-forfeiture, settlement options)",
            "State examination authority questioned due to NAIC accreditation lapse",
            "Model law updated but state has not yet adopted amendments"
        ],
        resolution_strategy="Monitor NAIC model law developments; track state adoption timelines; use IIPRC for multi-state life/annuity filings where applicable; ensure compliance with state-specific deviations from models; support state accreditation to preserve regulatory uniformity",
        entity_scope="Multi-state insurers, state insurance departments, NAIC",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="NAIC models widely adopted but state variations require careful compliance analysis",
        controlling_precedent="State law controls; NAIC models persuasive but not binding absent state adoption",
        category=IssueCategory.FINANCIAL_REPORTING
    ),
    DoctrineBlock(
        topic="Insurance Holding Company System and Form B/C/D/E Filings",
        keywords=["holding company", "Form B", "Form C", "Form D", "Form E", "change of control"],
        conclusion_template=[
            "Insurers in holding company systems must file annual registration (Form B) and prior approval for transactions (Form C/D/E)",
            "Change of control requires Form A prior approval from commissioner",
            "Holding company regulation ensures insurer solvency not jeopardized by affiliate transactions"
        ],
        reasoning_framework="""
        Texas Insurance Code Chapter 823 (Insurance Holding Company System Act) mirrors NAIC Model Law.
        'Insurance holding company system' exists when person directly/indirectly controls insurer.
        'Control' = 10 percent ownership or ability to elect directors. Controlled insurer must file
        annual Form B registration statement disclosing: organizational chart, ownership structure,
        biographical affidavits of directors/officers, financial statements of holding company and
        affiliates. Prior approval required for material transactions between insurer and affiliates:
        Form C for dividend/distribution, Form D for investment in affiliates or acquisition, Form E
        for service agreements, management contracts, cost-sharing. Commissioner has 30 days to approve/disapprove;
        may extend 30 days. Transactions not approved may not proceed. Standards for approval: fair
        and reasonable, does not jeopardize insurer solvency, complies with law. Change of control
        (acquisition of 10 percent or more by new person) requires Form A filed at least 60 days before
        acquisition. Commissioner may hold hearing; approve if acquirer has financial strength, competence,
        integrity, and acquisition not hazardous to policyholders. Enterprise risk reporting: insurers
        part of groups with $1B+ assets must file Own Risk and Solvency Assessment (ORSA) summary
        annually. ORSA describes material risks, group risk management, capital adequacy. Confidential
        filing. Examinations may include holding company system; TDI may order insurer to cease transactions
        with affiliates if detrimental. Dividend restrictions: extraordinary dividend (10 percent of
        surplus) requires Form C approval. Cross-default provisions: insurer default triggers affiliate
        obligations. Disallowed: upstream loans, dividends that render insurer insolvent, investments
        in affiliates beyond 5 percent of assets.
        """,
        key_factors=[
            "Form B annual registration required for all insurers in holding company system",
            "Form C/D/E prior approval for dividends, investments, service agreements with affiliates",
            "Form A filed 60 days before change of control (10 percent ownership acquisition)",
            "ORSA required for groups with $1B+ assets (enterprise risk reporting)",
            "Extraordinary dividends (10 percent of surplus) require Form C approval"
        ],
        primary_authority=["Texas Insurance Code Chapter 823", "28 TAC 7.201-.227", "NAIC Holding Company Model Law"],
        burden_holder="Insurer bears burden of filing timely and proving transactions fair, reasonable, not hazardous to solvency",
        adversary_position="Transaction not filed for approval; terms unfair (non-arm's length pricing); jeopardizes solvency; acquirer lacks competence",
        counter_arguments=[
            "Service agreement charges fees above market rate; affiliate enriched at insurer expense",
            "Dividend renders insurer below RBC action level; commissioner should disapprove",
            "Acquirer has history of insurer insolvencies; lacks integrity for approval",
            "Loan to parent affiliate unsecured; investment limit exceeded"
        ],
        resolution_strategy="File Form B annually by March 1; file Form C/D/E at least 30 days before transaction; price affiliate transactions at arm's length with independent valuation; limit dividends to ordinary (below 10 percent surplus); conduct ORSA annually for large groups; engage actuaries and auditors to certify solvency post-transaction",
        entity_scope="Insurers in holding company systems, parent companies, acquiring entities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Uniform NAIC model adopted by all accredited states with detailed filing requirements and approval standards",
        controlling_precedent="Commissioner has broad discretion to disapprove transactions; courts defer unless arbitrary/capricious",
        category=IssueCategory.FINANCIAL_REPORTING
    ),
    DoctrineBlock(
        topic="Rebating Prohibition and Permitted Inducements",
        keywords=["rebating", "inducement", "kickback", "value-added service", "permitted exceptions"],
        conclusion_template=[
            "Rebating (offering inducement not specified in policy to purchase insurance) prohibited in Texas",
            "Limited exceptions exist for value-added services, wellness programs, and specified benefits",
            "Violations subject to license revocation and criminal penalties"
        ],
        reasoning_framework="""
        Texas Insurance Code 541.056 and 541.058 prohibit rebating: offering, promising, or giving
        any benefit not specified in policy as inducement to purchase insurance. Purpose: prevent
        unfair discrimination (wealthy insureds receive discounts, others pay full rate) and maintain
        rate adequacy (rebates erode premium base). Rebate includes: return of premium, commission
        sharing, gifts, prizes, dividends beyond policy terms. Exception: life insurance dividends
        declared uniformly to all policyholders in class are permitted. Value-added services permitted
        if: (1) offered to all insureds in class, (2) related to insurance coverage, (3) cost reasonable
        and disclosed. Examples: home security discounts (premium reduction filed and approved as rate
        factor), wellness programs (flu shots, gym memberships for health insureds), loss control
        services (safety inspections for commercial property). Not permitted: cash rebates, gift cards,
        iPad giveaways to close sale, commission sharing with unlicensed person, anything conditioned
        on purchase. Penalties: administrative fine up to $25,000 per violation, license suspension/revocation,
        criminal misdemeanor. Insured who receives rebate not penalized but coverage remains valid.
        Controlled business exception: producer selling to self/family limited to certain percentage
        of total business (prevents self-rebating). Group insurance (employer-sponsored) premiums not
        rebating if employer pays portion (legitimate group discount). Affinity discounts (alumni,
        professional association) permitted if filed as rating factor. Rebating enforcement discretionary;
        isolated incidents may not trigger discipline.
        """,
        key_factors=[
            "Rebating = offering benefit not specified in policy as inducement to purchase",
            "Violates anti-discrimination and rate adequacy principles",
            "Value-added services permitted if offered uniformly, related to coverage, cost disclosed",
            "Penalties: $25,000 fine, license suspension, criminal misdemeanor",
            "Group/affinity discounts permitted if filed as rate factor"
        ],
        primary_authority=["Texas Insurance Code 541.056, 541.058", "28 TAC 21.2001-.2010"],
        burden_holder="TDI bears burden of proving rebate offered as inducement; producer must prove value-added service meets exception criteria",
        adversary_position="Gift card to close sale = rebate; iPad giveaway not related to coverage; discriminatory pricing",
        counter_arguments=[
            "Home security discount filed as rate factor and approved by TDI (not rebate)",
            "Wellness program offered to all health insureds; promotes loss control",
            "Premium rebate isolated incident; no pattern of violations",
            "Group insurance employer contribution legitimate; not individual rebate"
        ],
        resolution_strategy="Avoid cash rebates, gifts, commission sharing; file all discounts as rate factors with TDI; offer value-added services uniformly across class; document cost-reasonableness; train producers on rebating prohibition; report violations immediately to avoid complicity",
        entity_scope="All insurance producers and insurers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Long-standing statutory prohibition with clear standards and exceptions",
        controlling_precedent="Rebating cases rare; administrative enforcement discretionary",
        category=IssueCategory.UNFAIR_PRACTICES
    ),
    DoctrineBlock(
        topic="Twisting and Replacement Regulation",
        keywords=["twisting", "replacement", "churning", "comparative illustration", "notice to existing insurer"],
        conclusion_template=[
            "Twisting (inducing policyholder to lapse/replace existing policy through misrepresentation) is prohibited",
            "Replacement regulations require comparative illustration and notice to existing insurer",
            "Producer must document that replacement benefits insured, not just producer via new commission"
        ],
        reasoning_framework="""
        Texas Insurance Code 541.057 prohibits twisting: inducing policyholder to lapse, surrender,
        or replace existing policy through misrepresentation or incomplete comparison. Twisting harms
        insured: loss of benefits (surrender charges, new contestability/suicide period, higher premiums
        due to age), enriches producer (new first-year commission). Replacement regulation 28 TAC 3.1103
        requires: (1) producer must give insured Notice Regarding Replacement of Life Insurance form
        at point of sale, (2) comparative illustration showing existing vs proposed policy (premiums,
        cash values, death benefits, surrender charges), (3) notice to existing insurer of pending
        replacement (opportunity to conserve policy), (4) insured signs acknowledgment receiving materials.
        Existing insurer may contact insured to discuss retention. Replacing insurer must maintain
        file with all replacement documents for 5 years. Misrepresentation in comparison constitutes
        twisting: understating existing policy benefits, overstating proposed policy returns, omitting
        surrender charges. Churning: excessive replacements to generate commissions (pattern of replacing
        policies every 1-2 years). Even truthful comparison may be twisting if not in insured's best
        interest. TDI reviews complaint ratios; high replacement activity triggers market conduct exam.
        Safe harbor: if replacement clearly benefits insured (lower premium for same coverage, better
        company rating, added benefits) and properly documented, no twisting. Penalties: license revocation,
        restitution to insured, administrative fines. Insured may rescind new policy and reinstate
        old if twisting proven. Applies to life insurance primarily; also health, annuities.
        """,
        key_factors=[
            "Twisting = inducing replacement through misrepresentation or incomplete comparison",
            "Replacement regulation requires notice, comparative illustration, notice to existing insurer",
            "Producer must document replacement benefits insured (not just new commission)",
            "Churning = pattern of frequent replacements to generate commissions",
            "Penalties: license revocation, restitution, rescission of new policy"
        ],
        primary_authority=["Texas Insurance Code 541.057", "28 TAC 3.1103 (Replacement Regulation)"],
        burden_holder="Producer bears burden of proving replacement in insured's best interest and complying with notice/illustration requirements",
        adversary_position="Misrepresentation in comparison; omitted surrender charges; new policy worse than existing; churning pattern shown",
        counter_arguments=[
            "Producer failed to disclose 10-year surrender charge on new policy",
            "Existing policy had 20-year level premium; new policy premium increases after 10 years",
            "Insured replaced 3 policies in 3 years; clear churning for commissions",
            "No comparative illustration provided; replacement notice not signed"
        ],
        resolution_strategy="Provide full comparative illustration including surrender charges, premium increases, contestability period; give insured Notice Regarding Replacement form; send notice to existing insurer; document reasons replacement benefits insured; avoid frequent replacements (wait 5+ years); maintain replacement file for 5 years",
        entity_scope="Life insurance producers, health insurance agents, annuity sellers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established prohibition with detailed replacement regulation and notice requirements",
        controlling_precedent="Twisting cases result in license revocation; courts uphold TDI discipline",
        category=IssueCategory.UNFAIR_PRACTICES
    ),
    DoctrineBlock(
        topic="Advertising and Marketing Regulation",
        keywords=["advertising", "misleading", "disclosure", "comparison", "testimonials", "celebrity endorsement"],
        conclusion_template=[
            "Insurance advertising must be truthful, not misleading, and include required disclosures",
            "Comparative advertising permitted if factually accurate and sources cited",
            "Testimonials and endorsements must reflect typical experience and include disclaimers"
        ],
        reasoning_framework="""
        Texas Insurance Code 541.051-.061 and 28 TAC 21.101-.120 govern insurance advertising. 'Advertisement'
        includes print, broadcast, internet, social media, email, direct mail, sales presentations.
        General standards: must be truthful, not misleading, not omit material facts. Prohibited practices:
        misrepresenting policy terms, falsely implying government/state sponsorship, using deceptive
        headings (THIS IS NOT A BILL when soliciting), bait-and-switch (advertising unavailable product).
        Required disclosures: insurer name, statement that agent will contact, limitations on coverage.
        Comparative advertising: may compare to competitors if factually accurate, sources cited, not
        disparaging. Examples: 'Rated A+ by AM Best' (true), 'Lowest rates in Texas' (requires survey
        data). Testimonials: must reflect typical insured experience, not exceptional; disclaimer required
        if results not typical. Celebrity endorsements: must disclose if paid; celebrity must use product.
        Senior-specific marketing: stricter standards; may not exploit fear or imply government benefit.
        Medicare supplement advertising requires CMS-approved language. Health insurance ads must disclose
        limitations, exclusions, waiting periods. Life insurance illustrations: must comply with NAIC
        Life Insurance Illustrations Model Regulation (guaranteed vs non-guaranteed values, midpoint
        illustration). Internet advertising: same standards apply; website = advertisement. Social media:
        producer posts must include disclaimer 'Insurance offered through [licensed entity]'. File-and-use:
        P&C insurers file ads with TDI but may use immediately; life/health prior approval in some states.
        Enforcement: TDI orders cease-and-desist; administrative penalties; refer to AG for deceptive
        trade practices prosecution.
        """,
        key_factors=[
            "Advertising must be truthful, not misleading, include required disclosures",
            "Comparative advertising permitted if factually accurate with cited sources",
            "Testimonials must reflect typical experience; disclaimer if exceptional results",
            "Senior marketing restricted; may not exploit fear or imply government benefit",
            "Social media posts by producers = advertising; must include licensed entity disclaimer"
        ],
        primary_authority=["Texas Insurance Code 541.051-.061", "28 TAC 21.101-.120", "NAIC Advertisements of Accident and Sickness Insurance Model Regulation"],
        burden_holder="Insurer/producer bears burden of substantiating advertising claims and including required disclosures",
        adversary_position="Advertisement misleading; material omission; comparison inaccurate; testimonial not typical; senior marketing exploitative",
        counter_arguments=[
            "Ad says 'lowest rates' but no survey data; unsubstantiated claim",
            "Testimonial shows $50,000 claim paid but policy limit $10,000 (not typical)",
            "Senior mailer uses red envelope resembling government notice (deceptive)",
            "Internet ad omits insurer name and exclusions (material omissions)"
        ],
        resolution_strategy="Pre-clear all advertising with compliance department; include required disclosures (insurer name, limitations); substantiate comparative claims with data; use disclaimers on testimonials; avoid senior marketing exploitation; monitor social media posts by producers; file ads with TDI where required",
        entity_scope="All insurers and producers using advertising to market insurance",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Detailed advertising regulations with specific disclosure and substantiation requirements",
        controlling_precedent="FTC standards persuasive; state insurance departments enforce via cease-and-desist and penalties",
        category=IssueCategory.MARKET_CONDUCT
    ),
    DoctrineBlock(
        topic="Privacy and Information Security (GLBA and State Laws)",
        keywords=["privacy", "GLBA", "Gramm-Leach-Bliley", "information security", "data breach", "cybersecurity"],
        conclusion_template=[
            "Gramm-Leach-Bliley Act requires insurers to protect customer nonpublic personal information and provide privacy notices",
            "State laws (e.g., Texas Identity Theft Enforcement Act) impose data breach notification requirements",
            "NAIC Insurance Data Security Model Law adopted by many states requires cybersecurity programs and breach reporting"
        ],
        reasoning_framework="""
        Gramm-Leach-Bliley Act (GLBA) 15 USC 6801-6809 and FTC Safeguards Rule 16 CFR 314 require financial
        institutions (including insurers) to protect customer nonpublic personal information (NPI).
        NPI = personally identifiable financial information (SSN, account numbers, policy details).
        Insurers must: (1) provide privacy notice to customers at inception and annually, (2) allow
        opt-out of information sharing with non-affiliates, (3) implement administrative, technical,
        physical safeguards to protect NPI. Privacy notice must disclose: categories of NPI collected,
        with whom shared, how protected, opt-out rights. Sharing with affiliates permitted without
        opt-out; sharing with non-affiliates requires opt-out. Exceptions: sharing for claims processing,
        fraud prevention, legal compliance no opt-out required. FTC Safeguards Rule (updated 2021)
        requires: risk assessment, access controls, encryption of data in transit and at rest, multi-factor
        authentication, annual penetration testing, incident response plan, board-level oversight.
        State data breach laws: Texas Identity Theft Enforcement Act (Business and Commerce Code 521.053)
        requires notification to affected individuals within 60 days of breach discovery if unencrypted
        NPI compromised. Notice must include: date of breach, types of info compromised, steps being
        taken, credit monitoring offer. Notice to Attorney General required if 10,000+ Texans affected.
        NAIC Insurance Data Security Model Law adopted by 20+ states (not yet Texas) requires: cybersecurity
        program based on risk assessment, annual certification to commissioner, breach notification
        within 3 days to regulator. Penalties: FTC enforcement (GLBA violations), state AG enforcement
        (data breach), administrative penalties, class action lawsuits. Cyber insurance recommended.
        Vendor management: insurers responsible for third-party service provider security (contractual
        requirements, audits).
        """,
        key_factors=[
            "GLBA requires privacy notice, opt-out for non-affiliate sharing, information safeguards",
            "FTC Safeguards Rule requires encryption, MFA, penetration testing, incident response plan",
            "Texas data breach law: notify within 60 days, offer credit monitoring, report to AG if 10,000+ affected",
            "NAIC Model Law (20+ states): cybersecurity program, annual certification, 3-day regulator notification",
            "Insurers responsible for vendor security (third-party service providers)"
        ],
        primary_authority=["GLBA 15 USC 6801-6809", "FTC Safeguards Rule 16 CFR 314", "Texas Bus. & Com. Code 521.053", "NAIC Insurance Data Security Model Law"],
        burden_holder="Insurer bears burden of implementing safeguards, providing privacy notices, notifying of breaches; burden to prove vendor compliance",
        adversary_position="Safeguards inadequate; breach notification delayed; no encryption; vendor not audited; class action for negligence",
        counter_arguments=[
            "Breach occurred due to unpatched software; safeguards not implemented",
            "Notification sent 90 days after breach discovery (exceeds 60-day deadline)",
            "Data stored unencrypted on laptop stolen from employee car",
            "Third-party vendor breached; insurer failed to require contractual safeguards"
        ],
        resolution_strategy="Conduct annual risk assessment per FTC Safeguards Rule; encrypt all NPI at rest and in transit; implement MFA and access controls; engage third-party penetration testers; maintain incident response plan; monitor for breaches; notify within 60 days if breach; require vendors to comply with GLBA/Safeguards in contracts; obtain cyber insurance",
        entity_scope="All insurers and third-party administrators handling customer NPI",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal GLBA and FTC rules supplemented by state data breach laws with clear requirements",
        controlling_precedent="FTC enforcement actions (Equifax, Capital One); state AG enforcement of breach notification laws",
        category=IssueCategory.MARKET_CONDUCT
    ),
    DoctrineBlock(
        topic="Annual Financial Statement Filing and Statutory Accounting",
        keywords=["annual statement", "SAP", "NAIC blanks", "statutory accounting", "admitted assets", "AVR IMR"],
        conclusion_template=[
            "Insurers must file audited annual financial statements with state insurance department by March 1",
            "Statutory accounting principles (SAP) differ from GAAP; focus on solvency not profitability",
            "Key SAP conservatisms: non-admitted assets excluded, reserves discounted at conservative rates, AVR/IMR to smooth investment volatility"
        ],
        reasoning_framework="""
        Texas Insurance Code 823.008 and 28 TAC 7.71 require insurers to file annual financial statement
        with TDI by March 1. Statement prepared using NAIC Annual Statement Blanks and Statutory Accounting
        Principles (SAP). SAP differs from GAAP: (1) asset valuation conservatism (non-admitted assets
        like furniture, prepaid expenses excluded from surplus), (2) liability conservatism (reserves
        discounted at low interest rate), (3) solvency focus (ability to pay claims more important
        than profitability). Admitted assets: cash, bonds (at amortized cost or market), stocks (at
        market), mortgage loans, premium receivables <90 days. Non-admitted: office equipment, deferred
        acquisition costs, agents' balances >90 days, premiums more than 90 days overdue. Liabilities:
        loss reserves (case reserves plus IBNR), unearned premium reserves, premium deficiency reserves
        (if unearned premium insufficient for expected claims). Capital and surplus: statutory surplus
        (admitted assets minus liabilities). Asset Valuation Reserve (AVR): contra-liability account
        to absorb investment losses without hitting surplus; required for life insurers. Interest Maintenance
        Reserve (IMR): defers bond gains/losses to smooth income. Life insurers must file Schedule MB
        (health claims), Exhibit 5 (actuarial opinion on reserves), Exhibit 8 (reinsurance). P&C insurers
        file Schedule P (loss reserve development), Schedule F (reinsurance). Audit required: CPA opinion
        per NAIC Model Audit Rule. Opinion types: unqualified, qualified (scope limitation or departure
        from SAP), adverse, disclaimer. Qualified or adverse opinion triggers TDI inquiry. Statement
        filed via NAIC Insurance Regulatory Information System (IRIS). TDI reviews; may require corrective
        action if ratios out of range (e.g., premium/surplus ratio >300 percent). Penalties for late
        filing: $100/day up to $10,000. Fraudulent statement = felony.
        """,
        key_factors=[
            "Annual statement due March 1; prepared per NAIC blanks and SAP",
            "SAP focuses on solvency: conservative asset valuation, non-admitted assets excluded, reserves discounted low",
            "AVR and IMR smooth investment volatility for life insurers",
            "CPA audit required; qualified/adverse opinion triggers TDI inquiry",
            "IRIS ratios reviewed by TDI; out-of-range triggers corrective action"
        ],
        primary_authority=["Texas Insurance Code 823.008", "28 TAC 7.71", "NAIC Accounting Practices and Procedures Manual", "NAIC Model Audit Rule"],
        burden_holder="Insurer bears burden of preparing accurate statement per SAP and filing timely; auditor must opine on conformity with SAP",
        adversary_position="Statement inaccurate; reserves understated; non-admitted assets improperly included; late filing; fraudulent misrepresentation",
        counter_arguments=[
            "Insurer included agents' balances over 90 days in admitted assets (non-admitted per SAP)",
            "Loss reserves insufficient per actuarial opinion; must strengthen",
            "Reinsurance credit taken for unauthorized reinsurer without collateral",
            "Filing 30 days late; $3,000 penalty due"
        ],
        resolution_strategy="Engage actuary to certify reserves adequate; work with auditor to ensure SAP compliance; file statement via IRIS by March 1; exclude non-admitted assets; maintain AVR/IMR per NAIC guidance; respond promptly to TDI inquiries on ratios; correct errors via amended filing",
        entity_scope="All licensed insurers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Uniform NAIC SAP adopted by all states; detailed accounting manual and audit rule",
        controlling_precedent="SAP standards binding; courts defer to TDI on financial statement compliance",
        category=IssueCategory.FINANCIAL_REPORTING
    ),
    DoctrineBlock(
        topic="Financial Examination Authority and Examination Report",
        keywords=["financial examination", "NAIC exam", "triennial exam", "examination report", "exam costs"],
        conclusion_template=[
            "State insurance department may examine insurer financial condition at any time; routine exams every 3-5 years",
            "NAIC Financial Condition Examiners Handbook provides uniform exam standards",
            "Examination report public record 30 days after final; insurer pays exam costs"
        ],
        reasoning_framework="""
        Texas Insurance Code 401.051-.104 authorizes TDI to examine insurer financial condition at any
        time. Routine financial exams conducted every 3-5 years; risk-based scheduling (troubled insurers
        more frequently). NAIC Financial Condition Examiners Handbook adopted by TDI provides exam
        standards: (1) planning phase (risk assessment, scope determination), (2) fieldwork (test
        assets, reserves, reinsurance, investments, internal controls), (3) reporting (findings,
        recommendations, required corrective action). Exam notice gives 30 days to prepare; insurer
        must provide full access to records, officers, actuaries, auditors. Examiner-in-charge leads
        multi-state exam if insurer operates in multiple states. Key exam areas: asset valuation (bonds
        at amortized cost vs market; OTTI analysis), reserve adequacy (actuarial opinion testing),
        reinsurance (collateral verification, contract review), RBC compliance, holding company transactions
        (Form B/C/D/E review), investment compliance (quality, diversification limits). Exit conference
        presents preliminary findings. Draft report circulated; insurer has 30 days to respond. Final
        report incorporates insurer response or explains rejection. Findings: (1) no adverse findings
        (clean exam), (2) recommendations (best practices), (3) required corrective action (violations
        requiring remediation), (4) referral for enforcement (serious violations). Final report public
        record 30 days after issuance unless insurer seeks confidentiality (granted only if disclosure
        would harm competitive position). Insurer pays exam costs: examiner per diem plus travel expenses.
        Costs may reach $500,000 for large multistate insurer. Dispute resolution: insurer may challenge
        findings via administrative hearing; appeal to court. Non-cooperation with exam = license suspension.
        """,
        key_factors=[
            "Routine exams every 3-5 years; risk-based scheduling for troubled insurers",
            "NAIC Handbook provides uniform exam standards: planning, fieldwork, reporting",
            "Exam covers assets, reserves, reinsurance, RBC, holding company transactions, investments",
            "30-day response to draft report; final report public record unless confidentiality granted",
            "Insurer pays exam costs (per diem plus expenses); can reach $500,000"
        ],
        primary_authority=["Texas Insurance Code 401.051-.104", "28 TAC 1.401-.415", "NAIC Financial Condition Examiners Handbook"],
        burden_holder="Insurer must cooperate and provide access to records; burden to rebut findings in response to draft report",
        adversary_position="Exam findings show reserve deficiency, non-admitted assets improperly valued, reinsurance credits unsupported, RBC violation",
        counter_arguments=[
            "Insurer refused access to reinsurance contracts; exam incomplete",
            "Reserve actuarial opinion contradicts exam finding; actuary more expert",
            "Asset valuation uses NAIC-approved methodology; exam challenge improper",
            "Holding company transaction filed Form C and approved; exam retroactive challenge unfair"
        ],
        resolution_strategy="Cooperate fully with exam; provide complete records promptly; designate CFO/actuary as liaisons; conduct pre-exam internal audit to identify issues; respond to draft report with detailed rebuttals and actuary/auditor support; negotiate consent order for violations rather than public report; budget for exam costs annually",
        entity_scope="All licensed insurers subject to TDI jurisdiction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Uniform NAIC exam standards adopted by all states; detailed handbook and examiner training",
        controlling_precedent="Administrative law principles apply; courts defer to TDI expertise unless exam arbitrary/capricious",
        category=IssueCategory.EXAMINATION
    ),
    DoctrineBlock(
        topic="Own Risk and Solvency Assessment (ORSA) Requirement",
        keywords=["ORSA", "enterprise risk", "risk management", "stress testing", "confidential filing"],
        conclusion_template=[
            "Insurers part of groups with $1B+ assets must file ORSA summary annually",
            "ORSA describes material risks, group-wide risk management, and capital adequacy under stress scenarios",
            "ORSA summary confidential; used by regulators for enterprise risk assessment"
        ],
        reasoning_framework="""
        NAIC Own Risk and Solvency Assessment Model Act adopted by Texas (TIC 823.201-.211) and 40+
        states requires insurers in groups with $1B+ assets to conduct annual ORSA and file summary
        with lead state regulator. ORSA = internal process to assess risk and capital needs. Summary
        Report (confidential filing) must describe: (1) material risks (underwriting, investment, operational,
        strategic, liquidity, reputational), (2) risk management framework (governance, risk identification,
        measurement, mitigation, monitoring), (3) group capital adequacy (quantification of risks,
        capital resources, stress testing, economic capital models). No prescribed format but NAIC
        ORSA Guidance Manual provides best practices. Lead state coordinates review (domiciliary state
        of largest insurer in group). Regulators use ORSA to assess enterprise risk not captured by
        statutory financials (e.g., parent company debt, non-insurance affiliate risks, strategic acquisitions).
        Stress testing required: adverse scenarios (catastrophe, market crash, liquidity crisis) and
        impact on group capital. Economic capital model may be used (probability of ruin over 1 year).
        ORSA not publicly filed; confidential under state ORSA statutes. Regulators may request additional
        info or meeting. Filing deadline: annually, typically 60 days after year-end (March 1 for
        calendar-year groups). Small insurers (<$1B group assets) exempt but may file voluntarily.
        ORSA distinct from RBC: RBC is formulaic and entity-level; ORSA is qualitative, forward-looking,
        and group-level. No regulatory action triggered by ORSA alone; used as early warning system.
        International convergence: ORSA similar to Solvency II Own Risk and Solvency Assessment in EU.
        """,
        key_factors=[
            "Required for insurers in groups with $1B+ assets; filed annually by March 1",
            "Describes material risks, risk management framework, group capital adequacy",
            "Stress testing required: adverse scenarios and capital impact",
            "Confidential filing; not public; used by regulators for enterprise risk assessment",
            "Distinct from RBC: ORSA qualitative/group-level; RBC formulaic/entity-level"
        ],
        primary_authority=["Texas Insurance Code 823.201-.211", "NAIC ORSA Model Act", "NAIC ORSA Guidance Manual"],
        burden_holder="Insurer group bears burden of conducting ORSA and filing summary; regulators review for adequacy of risk assessment",
        adversary_position="ORSA summary inadequate; material risks omitted; stress testing scenarios not severe enough; capital model flawed",
        counter_arguments=[
            "Cyber risk not addressed despite recent industry breaches (material risk omission)",
            "Stress scenarios assume moderate recession; should test Great Recession severity",
            "Capital model uses historical loss data; forward-looking risks understated",
            "Group leverage high; parent debt service risk not quantified"
        ],
        resolution_strategy="Conduct annual ORSA with board and senior management involvement; engage ERM consultant and actuary; identify all material risks including emerging (cyber, climate); run severe stress scenarios; quantify capital needs under stress; document risk management framework; file summary by deadline with lead state; respond to regulator inquiries promptly",
        entity_scope="Insurers in groups with $1B+ consolidated assets (holding company and affiliates)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Uniform NAIC model adopted by 40+ states; confidential regulatory tool with guidance but no prescriptive format",
        controlling_precedent="No litigation; administrative process; regulators use for supervisory purposes",
        category=IssueCategory.FINANCIAL_REPORTING
    )
]

# Pydantic Models
class QueryRequest(BaseModel):
    question: str = Field(..., description="Insurance regulatory compliance question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

class QueryResponse(BaseModel):
    answer: str
    triggered_doctrines: List[str]
    confidence: str
    mode: str
    latency_ms: float
    determinism_hash: str
    metadata: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    uptime_seconds: float
    total_queries: int
    cache_coverage: float
    doctrines_available: int
    doctrines_triggered: int

# Engine State
telemetry = TelemetryCollector()
drift_watcher = DriftWatcher()
coverage_map = CoverageMap()

# Initialize coverage map
for doctrine in DOCTRINE_CACHE:
    coverage_map.mark_available(doctrine.topic)
    drift_watcher.set_baseline(doctrine.topic, doctrine.reasoning_framework)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down. Total queries: {len(telemetry.queries)}")

# FastAPI App
APP = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Insurance Regulatory Compliance Engine",
    lifespan=lifespan
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def three_layer_response(question: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[str], str, float, float]:
    """Three-layer response: Cache -> Semantic -> Deep"""
    start = time.time()

    # Layer 1: Doctrine Cache (0-200ms)
    cache_start = time.time()
    matched_doctrines = []
    question_lower = question.lower()

    for doctrine in DOCTRINE_CACHE:
        if any(kw in question_lower for kw in doctrine.keywords):
            matched_doctrines.append(doctrine)
            coverage_map.mark_triggered(doctrine.topic)

    cache_latency = (time.time() - cache_start) * 1000

    if matched_doctrines:
        # Cache hit - build response from doctrine blocks
        answer_parts = []

        if mode == ResponseMode.FAST:
            # Concise answer from conclusion templates
            for doctrine in matched_doctrines[:2]:  # Top 2 doctrines
                answer_parts.extend(doctrine.conclusion_template)
            answer = " ".join(answer_parts)

        elif mode == ResponseMode.DEFENSE:
            # Detailed answer with authority and reasoning
            for doctrine in matched_doctrines:
                answer_parts.append(f"DOCTRINE: {doctrine.topic}")
                answer_parts.extend(doctrine.conclusion_template)
                answer_parts.append(f"AUTHORITY: {'; '.join(doctrine.primary_authority)}")
                answer_parts.append(f"KEY FACTORS: {'; '.join(doctrine.key_factors)}")
                answer_parts.append("---")
            answer = "\n".join(answer_parts)

        else:  # MEMO mode
            # Comprehensive answer with full reasoning
            for doctrine in matched_doctrines:
                answer_parts.append(f"TOPIC: {doctrine.topic}")
                answer_parts.append(f"CATEGORY: {doctrine.category.value}")
                answer_parts.extend(doctrine.conclusion_template)
                answer_parts.append(f"\nREASONING FRAMEWORK:\n{doctrine.reasoning_framework}")
                answer_parts.append(f"\nPRIMARY AUTHORITY:\n{chr(10).join('- ' + auth for auth in doctrine.primary_authority)}")
                answer_parts.append(f"\nKEY FACTORS:\n{chr(10).join('- ' + factor for factor in doctrine.key_factors)}")
                answer_parts.append(f"\nBURDEN: {doctrine.burden_holder}")
                answer_parts.append(f"\nADVERSARY POSITION: {doctrine.adversary_position}")
                answer_parts.append(f"\nCOUNTER-ARGUMENTS:\n{chr(10).join('- ' + arg for arg in doctrine.counter_arguments)}")
                answer_parts.append(f"\nRESOLUTION STRATEGY: {doctrine.resolution_strategy}")
                answer_parts.append(f"\nCONTROLLING PRECEDENT: {doctrine.controlling_precedent}")
                answer_parts.append("\n" + "="*80 + "\n")
            answer = "\n".join(answer_parts)

        confidence = matched_doctrines[0].confidence.value
        triggered = [d.topic for d in matched_doctrines]
        total_latency = (time.time() - start) * 1000

        return answer, triggered, confidence, cache_latency, total_latency

    # Layer 2: Semantic retrieval (would use vector DB in production)
    semantic_latency = 50.0  # Simulated

    # Layer 3: Deep analysis (fallback)
    answer = f"Insurance regulatory question received: {question}. Based on available doctrine cache, this requires deep analysis beyond pre-compiled blocks. Recommend consulting specific statutes and regulatory guidance for {zone.value} zone analysis."
    confidence = ConfidenceLevel.DISCLOSURE.value
    triggered = ["DEEP_ANALYSIS_FALLBACK"]
    total_latency = (time.time() - start) * 1000

    return answer, triggered, confidence, cache_latency + semantic_latency, total_latency

def compute_determinism_hash(question: str, answer: str, mode: str) -> str:
    """SHA-256 hash for reproducibility verification"""
    combined = f"{question}|{answer}|{mode}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()[:16]

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with TIE-20 compliance"""
    query_id = hashlib.sha256(f"{request.question}{time.time()}".encode()).hexdigest()[:12]

    try:
        answer, triggered, confidence, cache_lat, total_lat = three_layer_response(
            request.question, request.mode, request.zone
        )

        det_hash = compute_determinism_hash(request.question, answer, request.mode.value)

        metrics = QueryMetrics(
            query_id=query_id,
            timestamp=time.time(),
            mode=request.mode.value,
            category=request.context.get("category") if request.context else None,
            cache_hit=len(triggered) > 0 and triggered[0] != "DEEP_ANALYSIS_FALLBACK",
            cache_latency_ms=cache_lat,
            semantic_latency_ms=0.0,
            total_latency_ms=total_lat,
            doctrines_triggered=triggered,
            confidence_level=confidence,
            determinism_hash=det_hash
        )

        telemetry.record(metrics)

        return QueryResponse(
            answer=answer,
            triggered_doctrines=triggered,
            confidence=confidence,
            mode=request.mode.value,
            latency_ms=round(total_lat, 2),
            determinism_hash=det_hash,
            metadata={
                "query_id": query_id,
                "zone": request.zone.value,
                "cache_hit": metrics.cache_hit,
                "engine_id": ENGINE_ID,
                "version": VERSION
            }
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint"""
    stats = telemetry.get_stats()

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        uptime_seconds=stats.get("uptime_seconds", 0),
        total_queries=stats.get("total_queries", 0),
        cache_coverage=coverage_map.get_coverage_rate(),
        doctrines_available=len(DOCTRINE_CACHE),
        doctrines_triggered=len(coverage_map.triggered)
    )

@APP.get("/metrics")
async def get_metrics():
    """Detailed telemetry metrics"""
    return {
        "telemetry": telemetry.get_stats(),
        "coverage": {
            "rate": coverage_map.get_coverage_rate(),
            "triggered": list(coverage_map.triggered),
            "gaps": coverage_map.get_gaps()
        },
        "drift": {
            "topics_monitored": len(drift_watcher.baseline_hashes)
        }
    }

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "authority": d.primary_authority
            }
            for d in DOCTRINE_CACHE
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(APP, host="0.0.0.0", port=PORT)
