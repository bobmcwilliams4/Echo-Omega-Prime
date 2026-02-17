"""
REG07 Energy Regulatory Engine v1.0.0
TIE-20 Compliant - Energy Sector Regulatory Compliance

Handles FERC regulations, NERC reliability standards, PUCT rules, ERCOT protocols,
natural gas pipeline regulation, LNG facility requirements, renewable energy credits,
RPS mandates, interconnection standards, rate cases, market manipulation rules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

ENGINE_ID = "REG07"
ENGINE_NAME = "Energy Regulatory Engine"
VERSION = "1.0.0"
PORT = 9127

logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


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
    FERC_REGULATION = "FERC_REGULATION"
    NERC_RELIABILITY = "NERC_RELIABILITY"
    STATE_COMMISSION = "STATE_COMMISSION"
    PIPELINE_SAFETY = "PIPELINE_SAFETY"
    MARKET_RULES = "MARKET_RULES"
    INTERCONNECTION = "INTERCONNECTION"
    RENEWABLE_STANDARDS = "RENEWABLE_STANDARDS"
    RATE_REGULATION = "RATE_REGULATION"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    COMPLIANCE_REPORTING = "COMPLIANCE_REPORTING"


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
    category: IssueCategory


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    entity_context: Optional[str] = None


class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    confidence: ConfidenceLevel
    authorities_cited: List[str]
    triggered_doctrines: List[str]
    epistemic_flags: List[str]
    response_time_ms: float
    determinism_hash: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_response_ms: float
    cache_hit_rate: float


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="FERC Jurisdiction Over Interstate Transmission",
        keywords=["FERC", "jurisdiction", "interstate", "transmission", "FPA Section 201"],
        conclusion_template=[
            "FERC has exclusive jurisdiction over interstate wholesale power sales and transmission in interstate commerce under Federal Power Act Section 201(b).",
            "State commissions retain authority over retail sales and local distribution facilities.",
            "Bright line test: facilities used for wholesale transmission are FERC-jurisdictional; retail distribution is state-jurisdictional."
        ],
        reasoning_framework="""
Federal Power Act Section 201(b)(1) grants FERC jurisdiction over:
1. Sale of electric energy at wholesale in interstate commerce
2. Transmission of electric energy in interstate commerce
3. All facilities for such transmission or sale

Section 201(a) reserves to states jurisdiction over:
1. Facilities used for generation
2. Facilities used in local distribution or only for intrastate commerce
3. Retail sales

Supreme Court in ONEOK v. Learjet (2015) and Hughes v. Talen (2016) clarified field preemption.
FERC determines jurisdictional classification via bright line test based on facility use, not voltage.
Transmission = high voltage bulk power movement; distribution = lower voltage delivery to end users.
Mixed-use facilities require functional test to allocate costs between FERC/state jurisdiction.
        """,
        key_factors=[
            "Voltage level and facility function",
            "Wholesale vs retail end use",
            "Interstate vs intrastate commerce",
            "FERC classification precedent",
            "Mixed-use facility cost allocation methodology"
        ],
        primary_authority=[
            "16 U.S.C. Section 824(b) - Federal Power Act Section 201(b)",
            "ONEOK, Inc. v. Learjet, Inc., 575 U.S. 373 (2015)",
            "Hughes v. Talen Energy Marketing, 578 U.S. 150 (2016)",
            "FERC Order 888 (Open Access Transmission)"
        ],
        burden_holder="Party claiming state jurisdiction must show facility is purely local distribution",
        adversary_position="State commissions may claim dual use facilities are primarily distribution",
        counter_arguments=[
            "High voltage alone does not prove FERC jurisdiction",
            "Radial lines to single customer may be distribution even at transmission voltage",
            "State commission classification may have comity weight",
            "Cost allocation formulas can shift jurisdictional balance"
        ],
        resolution_strategy="File declaratory order petition at FERC for jurisdictional determination; cite facility's actual function in wholesale markets; show interstate commerce nexus",
        entity_scope="Electric utilities, IPPs, transmission owners, RTOs, state commissions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Supreme Court precedent is controlling; FERC applies bright line test consistently",
        controlling_precedent="Federal Power Act Section 201(b); ONEOK and Hughes Supreme Court decisions",
        category=IssueCategory.FERC_REGULATION
    ),
    DoctrineBlock(
        topic="NERC CIP Critical Infrastructure Protection Standards",
        keywords=["NERC", "CIP", "cybersecurity", "critical infrastructure", "bulk electric system"],
        conclusion_template=[
            "NERC CIP standards impose mandatory cybersecurity controls on bulk electric system assets above impact rating thresholds.",
            "Medium and high impact BES cyber systems require physical security perimeters, electronic access controls, incident response plans, and personnel risk assessments.",
            "Violations carry civil penalties up to $1,000,000 per day per violation; willful violations may trigger criminal liability."
        ],
        reasoning_framework="""
Energy Policy Act of 2005 authorized FERC to approve mandatory reliability standards.
FERC delegated to NERC as Electric Reliability Organization under Section 215.
NERC CIP-002 through CIP-014 create tiered cybersecurity framework:

CIP-002: BES Cyber System Categorization (Low/Medium/High impact)
CIP-003: Security Management Controls (policies, awareness training)
CIP-004: Personnel and Training (background checks, cyber security training)
CIP-005: Electronic Security Perimeters (firewalls, access controls)
CIP-006: Physical Security (PSP, monitoring, access logging)
CIP-007: System Security Management (patch management, malware prevention)
CIP-008: Incident Reporting and Response Planning
CIP-009: Recovery Plans for BES Cyber Systems
CIP-010: Configuration Change Management and Vulnerability Assessments
CIP-011: Information Protection (data classification, secure handling)
CIP-013: Supply Chain Risk Management
CIP-014: Physical Security (critical transmission stations, substations)

Compliance enforced via self-certification, spot checks, and investigations.
Violations assessed via Sanction Guidelines considering risk, duration, repetition.
        """,
        key_factors=[
            "BES cyber system impact rating (low/medium/high)",
            "Critical cyber asset identification methodology",
            "Electronic Security Perimeter architecture",
            "Physical Security Perimeter controls",
            "Personnel cyber security training completion",
            "Incident response plan adequacy",
            "Patch management compliance timeline",
            "Supply chain risk assessment processes"
        ],
        primary_authority=[
            "16 U.S.C. Section 824o - Energy Policy Act Section 215",
            "18 CFR Part 39 - FERC Reliability Standards",
            "NERC CIP-002-5.1a through CIP-014-2",
            "NERC Sanction Guidelines (Appendix 4B to NERC Rules of Procedure)"
        ],
        burden_holder="Registered entity must demonstrate CIP compliance via evidence retention and audits",
        adversary_position="NERC compliance auditors may find inadequate documentation or control gaps",
        counter_arguments=[
            "Low impact BES cyber systems have reduced CIP requirements",
            "Approved implementation plan may defer compliance deadline",
            "Technical feasibility exceptions may excuse specific controls",
            "Self-reporting and mitigation may reduce penalties"
        ],
        resolution_strategy="Conduct CIP compliance gap analysis; implement defense-in-depth security architecture; maintain evidence repository; file self-reports for violations; negotiate mitigation plans",
        entity_scope="Transmission owners, generator owners, balancing authorities, reliability coordinators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statute and FERC-approved standards are binding; penalty amounts highly fact-specific",
        controlling_precedent="Energy Policy Act Section 215; NERC CIP standards approved by FERC",
        category=IssueCategory.NERC_RELIABILITY
    ),
    DoctrineBlock(
        topic="ERCOT Nodal Market Protocols and Settlement",
        keywords=["ERCOT", "nodal market", "LMP", "settlement", "protocols"],
        conclusion_template=[
            "ERCOT Nodal Protocols govern all market participation, congestion management, and financial settlement in Texas competitive wholesale market.",
            "Locational Marginal Pricing reflects energy, congestion, and loss components at each node.",
            "Protocol revisions require ERCOT board approval after stakeholder process; PUCT retains oversight authority."
        ],
        reasoning_framework="""
Texas ERCOT operates as independent system operator under PUCT authority (PURA Section 39.151).
ERCOT Nodal Protocols define market rules including:

Section 3: Definitions (LMP, SCED, AS, CRR, MCPE)
Section 4: Day-Ahead Market (DAMLMP, virtual transactions, Block Load Transfers)
Section 5: Adjustment Period (resource plan changes, OOE limits)
Section 6: Real-Time Market (SCED dispatch, LMP calculation every 5 minutes)
Section 7: Ancillary Services (Reg Up/Down, RRS, ECRS, Non-Spin)
Section 8: Congestion Revenue Rights (annual/monthly auctions, Point-to-Point obligations)
Section 9: Settlement and Billing (Day-Ahead, Real-Time, Uplift, resettlement timelines)

LMP = Energy price + Congestion price + Loss price
SCED co-optimizes energy and AS every 5 minutes based on resource offers and system conditions.
Three-part supply offers: energy curve, startup cost, minimum energy cost.
Settlement occurs at intervals (Day 4, Day 60, Day 180 true-up).
Disputes follow Protocol Section 20 process: informal resolution, then PUCT complaint.
        """,
        key_factors=[
            "Market participant registration and creditworthiness",
            "Resource telemetry and HSL accuracy",
            "Offer curve submission compliance",
            "Out-of-merit energy settlement impacts",
            "Congestion Revenue Rights hedge effectiveness",
            "Uplift allocation methodology",
            "Invoice dispute timeline (60 days from invoice date)"
        ],
        primary_authority=[
            "PURA Section 39.151 (ERCOT organization and duties)",
            "16 TAC Section 25.501 (ERCOT governance)",
            "ERCOT Nodal Protocols (entire document binding on market participants)",
            "ERCOT Operating Guides (technical implementation)"
        ],
        burden_holder="Market participant must comply with Protocols and submit accurate data; bears financial risk of offer strategy",
        adversary_position="ERCOT Market Monitor may allege physical withholding or economic withholding if offers deviate from competitive benchmarks",
        counter_arguments=[
            "Verifiable costs justify three-part offer amounts",
            "Forced outages excuse HSL underperformance",
            "Protocol ambiguity supports alternative interpretation",
            "Emergency conditions triggered atypical dispatch"
        ],
        resolution_strategy="Document all resource costs and operational constraints; file timely meter data corrections; engage Protocol Revision Request for structural issues; preserve invoice dispute rights",
        entity_scope="QSEs, REPs, generators, loads, CRR account holders",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Protocols have contract-like force; PUCT decisions provide interpretive guidance; market monitor opinions not binding",
        controlling_precedent="PURA Section 39; PUCT Substantive Rules 25 TAC Chapter 25; ERCOT Nodal Protocols",
        category=IssueCategory.MARKET_RULES
    ),
    DoctrineBlock(
        topic="FERC Market-Based Rate Authority and Mitigation",
        keywords=["MBR", "market-based rates", "market power", "mitigation", "horizontal", "vertical"],
        conclusion_template=[
            "FERC grants market-based rate authority to sellers lacking or adequately mitigating horizontal and vertical market power.",
            "Sellers must update market power analysis every three years and upon triggering change in status.",
            "FERC may revoke MBR authority or impose cost-based rates if seller fails indicative screens or cannot rebut market power presumption."
        ],
        reasoning_framework="""
Federal Power Act Section 205 requires just and reasonable rates; Section 206 allows FERC modification.
FERC presumes market-based rates are just and reasonable if seller lacks market power.

Market power screens per Order 816:
1. Horizontal Market Power: Pivotal supplier analysis in each season; must fail pivotal supplier test or deliver margin screen <20%
2. Vertical Market Power: Transmission market share <20% in each relevant market
3. Barriers to Entry: No control over inputs essential for generation entry

Categories of MBR sellers:
- Category 1: Fails screens in one or more markets, must do Delivered Price Test
- Category 2: Satisfies screens in all markets
- Category 3: Power marketers, no generation/transmission, blank screen

Mitigation options if screens fail:
- Divest generation to reduce pivotal supplier status
- OATT Amendment to ensure open access transmission
- RTO/ISO membership (rebuttable presumption of no market power in RTO footprint)
- Cost-based rate cap in specific markets

Triggering events requiring updated filing:
- Merger/acquisition over 100 MW
- Affiliation change affecting market power
- Change in RTO/ISO status
        """,
        key_factors=[
            "Seasonal pivotal supplier status in first tier markets",
            "Delivered margin percentage in DPT markets",
            "Transmission ownership share in control area",
            "RTO/ISO market monitoring and mitigation",
            "Affiliate generation aggregation",
            "Joint dispatch agreements impact"
        ],
        primary_authority=[
            "16 U.S.C. Sections 824d, 824e (FPA Sections 205, 206)",
            "FERC Order 816 (Market-Based Rate Final Rule, 2016)",
            "18 CFR Section 35.37 (MBR tariff and reporting requirements)",
            "FERC Market-Based Rate Tariff (individual seller tariff on file)"
        ],
        burden_holder="MBR seller must prove lack of market power via indicative screens or DPT; bears burden in updated filings",
        adversary_position="Protestors or FERC staff may allege seller is pivotal supplier or has affiliate coordination conferring market power",
        counter_arguments=[
            "Seller fails screens but DPT shows competitive delivered prices",
            "Minimal capacity compared to market size",
            "RTO Day-Ahead and Real-Time markets have structural mitigation",
            "Affiliate operates independently with no coordinated offers"
        ],
        resolution_strategy="Conduct triennial market power analysis using FERC screens; model pivotal supplier scenarios; demonstrate independent operation of affiliates; consider RTO membership or divestiture",
        entity_scope="Public utilities selling at wholesale, exempt wholesale generators, power marketers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="FERC applies screens mechanically but allows DPT rebuttal; case law supports market power findings based on pivotal supplier test",
        controlling_precedent="FPA Sections 205/206; FERC Order 816; AEP Power Marketing v. FERC precedent",
        category=IssueCategory.RATE_REGULATION
    ),
    DoctrineBlock(
        topic="FERC Section 205 Rate Filing Requirements",
        keywords=["Section 205", "rate filing", "FPA", "tariff", "suspension", "refund"],
        conclusion_template=[
            "Public utilities must file rate changes under FPA Section 205 with 60 days notice; FERC may suspend for up to 5 months.",
            "Filed rates must be just, reasonable, and not unduly discriminatory or preferential.",
            "FERC may order refunds subject to 15-month refund period if Section 206 proceeding initiated."
        ],
        reasoning_framework="""
Federal Power Act Section 205 governs utility-initiated rate changes:

Filing requirements:
- 60 days advance notice (or waived for good cause)
- Statement of basis supporting just and reasonable standard
- Cost support for cost-based rates; market power analysis for MBR
- Clean and redline tariff sheets

FERC action window:
- May suspend rate for up to 5 months (hearing and settlement procedures)
- Accepted rates go into effect subject to refund if later found unjust
- Refund liability begins on suspension date or 60 days after filing if not suspended

Section 206 Complaint or Investigation:
- FERC or third party may challenge rate as unjust, unreasonable, or unduly discriminatory
- 15-month refund period from complaint or investigation order date
- Burden shifts to utility to prove existing rate is just and reasonable

Rate design principles:
- Cost causation: rates allocated to those causing costs
- No undue discrimination between similarly situated customers
- Recovery of prudently incurred costs plus reasonable return on equity
        """,
        key_factors=[
            "Adequacy of cost support and testimony",
            "Changed circumstances justifying rate increase",
            "Protests from customers or state commissions",
            "Settlement potential to avoid full litigation",
            "Refund liability exposure if rates suspended",
            "ROE within zone of reasonableness (recent precedent: 9.3% midpoint)"
        ],
        primary_authority=[
            "16 U.S.C. Section 824d (FPA Section 205)",
            "16 U.S.C. Section 824e (FPA Section 206)",
            "18 CFR Part 35 (FERC rate filing regulations)",
            "Hope Natural Gas (1944) - just and reasonable standard",
            "Opinion 569 series (ROE methodology)"
        ],
        burden_holder="Utility filing rate increase bears burden to prove rate is just and reasonable",
        adversary_position="Customers or state advocates may protest rate as excessive or improperly allocated",
        counter_arguments=[
            "Costs are prudently incurred and necessary for reliability",
            "ROE reflects current capital market conditions and risk",
            "Rate design follows cost causation and avoids undue discrimination",
            "Settlement reflects give-and-take and should be approved in public interest"
        ],
        resolution_strategy="Prepare detailed cost study and ROE testimony; engage customers early for settlement; respond fully to data requests; consider black box settlement to preserve precedent",
        entity_scope="Public utilities with FERC-jurisdictional transmission or wholesale sales",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Section 205 process is well-established; ROE outcomes vary based on DCF/CAPM models and panel discretion",
        controlling_precedent="FPA Sections 205/206; Hope/Bluefield standards; Opinion 569 ROE methodology",
        category=IssueCategory.RATE_REGULATION
    ),
    DoctrineBlock(
        topic="Natural Gas Pipeline Certificate Authority Under NGA Section 7",
        keywords=["NGA Section 7", "certificate", "pipeline", "public convenience", "eminent domain"],
        conclusion_framework="""
Natural Gas Act Section 7(c) requires interstate pipelines to obtain FERC certificate before construction.
Certificate granted if project is in public convenience and necessity.
Certificate confers federal eminent domain authority under NGA Section 7(h).
        """,
        reasoning_framework="""
NGA Section 7 certificate process:
1. Pre-filing under 18 CFR 157.21 (optional but typical for major projects)
2. Application filed with environmental report, engineering, market analysis, precedent agreements
3. NEPA environmental review (EA or EIS depending on scope)
4. Public comment period and interventions
5. FERC issues certificate order or denial

Public convenience and necessity standard (Certificate Policy Statement 1999):
- Pipeline must demonstrate market need (precedent agreements, open season results)
- Pipeline bears financial risk, not ratepayers (no rolled-in rate subsidies)
- Environmental impacts adequately mitigated
- Landowner and community interests considered but not dispositive

Eminent domain (NGA Section 7(h)):
- Certificate confers federal right to condemn property for pipeline right-of-way
- Pipeline must negotiate in good faith; if no agreement, files condemnation in federal district court
- Compensation is fair market value of easement plus damages
- State law governs valuation but federal statute authorizes taking

Rehearing and judicial review:
- 30-day rehearing period at FERC required before court appeal
- D.C. Circuit has exclusive jurisdiction over certificate appeals
- Arbitrary and capricious review standard; FERC decisions upheld if reasoned basis
        """,
        key_factors=[
            "Precedent agreement coverage as percent of capacity",
            "Open season process and shipper interest",
            "Environmental impacts and mitigation measures",
            "Landowner opposition and routing alternatives",
            "Financial viability of project sponsor",
            "Need for incremental capacity in region"
        ],
        primary_authority=[
            "15 U.S.C. Section 717f (NGA Section 7)",
            "18 CFR Part 157 (Pipeline certificate applications)",
            "FERC Certificate Policy Statement (88 FERC 61,227, 1999)",
            "18 CFR Part 380 (NEPA regulations)"
        ],
        burden_holder="Pipeline applicant must demonstrate public convenience and necessity",
        adversary_position="Landowners, environmental groups, competing pipelines may protest on need, environmental, or routing grounds",
        counter_arguments=[
            "Precedent agreements show market demand for capacity",
            "Environmental impacts mitigated to less than significant",
            "Routing avoids sensitive areas and minimizes impacts",
            "Regional benefits outweigh localized landowner concerns",
            "No viable alternative to meet demand growth"
        ],
        resolution_strategy="Conduct robust pre-filing process; secure long-term precedent agreements; prepare comprehensive environmental analysis; engage landowners early with fair compensation offers; respond to all protests",
        entity_scope="Interstate natural gas pipelines, LNG terminals, storage facilities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Certificate Policy Statement framework well-established; environmental challenges increasingly common but rarely dispositive",
        controlling_precedent="NGA Section 7; FERC Certificate Policy Statement; D.C. Circuit certificate appeal precedent",
        category=IssueCategory.FERC_REGULATION
    ),
    DoctrineBlock(
        topic="Pipeline Safety Regulations 49 CFR 192 and 195",
        keywords=["pipeline safety", "DOT", "PHMSA", "integrity management", "HCA", "leak detection"],
        conclusion_template=[
            "PHMSA enforces pipeline safety under 49 CFR 192 (gas) and 195 (hazardous liquids).",
            "Operators must implement integrity management programs for high consequence areas.",
            "Violations may result in civil penalties, corrective action orders, or criminal prosecution."
        ],
        reasoning_framework="""
Pipeline Safety Act grants PHMSA authority to regulate pipeline safety (49 U.S.C. Chapter 601).

Key regulatory frameworks:
49 CFR Part 192: Gas transmission and distribution pipeline safety
- Subpart O: Integrity management for gas transmission in HCAs
- Pressure testing, corrosion control, leak surveys
- Incident reporting within 1 hour for significant events

49 CFR Part 195: Hazardous liquid pipeline safety
- Subpart F: Integrity management in HCAs
- SCADA, leak detection, valve spacing, spill response
- Public awareness programs under API RP 1162

High Consequence Area (HCA) determination:
- Gas: potential impact radius includes HCA if buildings, population, or other criteria met
- Liquid: unusually sensitive areas, commercially navigable waterways, population areas

Integrity management elements:
- Baseline assessment (ILI, pressure test, or direct assessment)
- Risk analysis and reassessment intervals (7 years for gas, 5 years for liquid)
- Preventive and mitigative measures
- Performance metrics and continuous improvement

Enforcement:
- PHMSA inspections and audits
- Civil penalties up to $200,000 per violation per day (maximum $2 million for related series)
- Corrective Action Orders for imminent hazards
- Criminal penalties for knowing and willful violations
        """,
        key_factors=[
            "HCA identification methodology accuracy",
            "Baseline assessment completion within regulatory deadlines",
            "ILI tool selection and anomaly remediation",
            "Corrosion control program effectiveness",
            "Leak detection system sensitivity and response time",
            "Public awareness program reach and content",
            "Incident investigation root cause analysis"
        ],
        primary_authority=[
            "49 U.S.C. Chapter 601 (Pipeline Safety Act)",
            "49 CFR Part 192 (Gas Pipeline Safety)",
            "49 CFR Part 195 (Hazardous Liquid Pipeline Safety)",
            "ASME B31.8S (Gas Pipeline Integrity Management Standard)",
            "API 1160 (Liquid Pipeline Integrity Management Standard)"
        ],
        burden_holder="Pipeline operator must demonstrate compliance with integrity management program and baseline assessment schedules",
        adversary_position="PHMSA may allege inadequate risk analysis, delayed anomaly remediation, or deficient procedures",
        counter_arguments=[
            "Assessment methodology follows industry standards",
            "Anomaly remediation prioritized by risk score",
            "Immediate repair conditions addressed within timelines",
            "Economic hardship justifies extended compliance schedule"
        ],
        resolution_strategy="Implement robust IMP program with third-party validation; conduct gap analysis against PHMSA inspection protocols; document all remediation decisions; file special permits if needed",
        entity_scope="Gas transmission operators, hazardous liquid pipeline operators, gathering line operators in HCAs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory requirements explicit; enforcement discretion varies by regional office; settlement common to avoid maximum penalties",
        controlling_precedent="49 CFR 192/195; PHMSA enforcement guidance; industry consensus standards",
        category=IssueCategory.PIPELINE_SAFETY
    ),
    DoctrineBlock(
        topic="PUCT Ratemaking for Texas Electric Utilities",
        keywords=["PUCT", "rate case", "PURA", "revenue requirement", "test year", "ROE"],
        conclusion_template=[
            "PUCT sets rates for non-ERCOT utilities and transmission/distribution utilities in ERCOT under PURA Section 36.",
            "Revenue requirement = Rate base x ROE + operating expenses + depreciation + taxes.",
            "Rate case process includes test year, adjustments, intervenor testimony, and final order within statutory timeline."
        ],
        reasoning_framework="""
Public Utility Regulatory Act Section 36.051 establishes ratemaking principles:
1. Rates must be just and reasonable
2. Utility entitled to reasonable opportunity to earn reasonable return on invested capital
3. Rates set based on original cost of property less depreciation
4. Rate design must avoid undue discrimination

Rate case procedure (PURA Section 36.053):
- Utility files application with test year data
- PUCT staff and intervenors (cities, customer groups) participate
- Discovery, testimony, hearing, briefing
- PUCT issues final order within 185 days (or 245 with suspension)

Revenue requirement formula:
Rate Base (original cost - accumulated depreciation + working capital)
x Rate of Return (weighted cost of debt and equity)
+ Operating Expenses (normalized, excluding non-recurring items)
+ Depreciation Expense (based on approved lives and methods)
+ Taxes (income tax, property tax, regulatory assessments)

Rate base issues:
- Construction work in progress (AFUDC vs rate base)
- Accumulated deferred income taxes (reduce rate base)
- Regulatory assets/liabilities
- Plant used and useful standard

ROE determination:
- DCF model (dividend yield + growth rate)
- CAPM (risk-free rate + beta x market risk premium)
- Comparable earnings approach
- Recent PUCT-approved ROEs: 9.4% to 9.8% range
        """,
        key_factors=[
            "Test year selection and normalization adjustments",
            "Plant additions since test year (known and measurable)",
            "ROE model inputs (growth rates, risk-free rate, beta)",
            "Operating expense prudence review",
            "Depreciation rate changes",
            "Cost allocation among customer classes",
            "Rate design (demand charges, customer charges, energy charges)"
        ],
        primary_authority=[
            "PURA Sections 36.001-36.211 (Texas Public Utility Regulatory Act)",
            "16 TAC Chapter 25 Subchapter E (PUCT substantive rules on ratemaking)",
            "Bluefield Water Works (1923) and Hope Natural Gas (1944) U.S. Supreme Court standards"
        ],
        burden_holder="Utility must prove proposed rates are just and reasonable; prudence of costs challenged by intervenors",
        adversary_position="Cities and consumer advocates argue for lower ROE, disallowances of imprudent costs, shorter depreciation lives",
        counter_arguments=[
            "ROE reflects current capital market conditions and utility risk",
            "All costs prudently incurred based on information available at time",
            "Depreciation lives supported by engineering study",
            "Rate design balances revenue stability and customer bill impacts"
        ],
        resolution_strategy="File comprehensive rate case with detailed cost studies; retain expert witnesses on ROE and depreciation; negotiate settlement with major cities; prepare for contested hearing if settlement fails",
        entity_scope="Investor-owned electric utilities in Texas, including transmission and distribution in ERCOT and vertically integrated utilities outside ERCOT",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PURA and PUCT rules provide clear framework; ROE outcomes vary based on capital market conditions; settlement common to avoid litigation risk",
        controlling_precedent="PURA Section 36; 16 TAC Chapter 25; PUCT rate case orders; Bluefield/Hope standards",
        category=IssueCategory.STATE_COMMISSION
    ),
    DoctrineBlock(
        topic="Renewable Portfolio Standards and REC Compliance",
        keywords=["RPS", "renewable portfolio standard", "REC", "renewable energy credit", "compliance"],
        conclusion_template=[
            "State RPS mandates require load-serving entities to procure specified percentages of renewable energy or RECs.",
            "RECs represent environmental attributes of 1 MWh renewable generation, tradable separately from energy.",
            "Compliance demonstrated via REC retirement in state tracking system; penalties or alternative compliance payments for shortfalls."
        ],
        reasoning_framework="""
RPS structure varies by state but common elements:
- Percentage target escalating over time (e.g., 50% by 2030)
- Eligible renewable technologies (wind, solar, hydro, biomass, geothermal)
- Carve-outs or multipliers for specific technologies (e.g., solar, offshore wind)
- Geographic eligibility (in-state generation, regional grid, or broader)

REC mechanics:
- 1 REC = 1 MWh renewable generation certified by tracking system (e.g., ERCOT, PJM-GATS, WREGIS, NEPOOL-GIS)
- RECs created at point of generation, transferred via registry accounts
- Vintage year and eligibility attributes tracked
- RECs retired to demonstrate compliance; double-counting prohibited

Compliance demonstration:
- LSE reports retail sales and REC retirements annually
- Shortfalls subject to alternative compliance payment (ACP) or penalty
- ACP functions as price cap on REC market (e.g., $50/MWh in some states)
- RECs may be banked for 1-3 years depending on state rules

Market dynamics:
- Oversupply drives REC prices to near zero
- Undersupply pushes prices toward ACP level
- Long-term REC contracts provide revenue certainty for renewable projects
- Voluntary REC market exists for corporate sustainability goals (separate from compliance)
        """,
        key_factors=[
            "State-specific RPS percentage target and schedule",
            "Eligible resource types and geographic boundaries",
            "Carve-out compliance and multiplier application",
            "REC tracking system registration and transfers",
            "Long-term REC contract pricing vs spot market",
            "ACP rate and shortfall penalty exposure",
            "Voluntary vs compliance REC market distinction"
        ],
        primary_authority=[
            "State statutes establishing RPS (varies by state: CA SB 100, NY Climate Act, MA Green Communities Act, etc.)",
            "State PUC regulations implementing RPS",
            "REC tracking system rules (ERCOT, PJM-GATS, WREGIS, NAR, NEPOOL-GIS, M-RETS)",
            "FERC Order 888 (transmission access for renewable resources)"
        ],
        burden_holder="Load-serving entity must demonstrate RPS compliance via sufficient REC retirements",
        adversary_position="State regulators may disallow RECs not meeting eligibility criteria or improperly documented",
        counter_arguments=[
            "RECs meet all state eligibility requirements for vintage, technology, location",
            "Tracking system records establish valid chain of custody",
            "Force majeure or market conditions beyond LSE control justify shortfall",
            "Voluntary market RECs properly excluded from compliance accounting"
        ],
        resolution_strategy="Register generation in appropriate tracking system; maintain detailed REC procurement records; model RPS obligations and REC supply annually; secure long-term contracts for compliance certainty",
        entity_scope="Load-serving entities (utilities, competitive suppliers), renewable generators, REC aggregators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="RPS statutes and tracking system rules are explicit; compliance mechanics well-established; market price volatility creates procurement risk",
        controlling_precedent="State RPS statutes and PUC regulations; tracking system operating rules",
        category=IssueCategory.RENEWABLE_STANDARDS
    ),
    DoctrineBlock(
        topic="FERC Anti-Manipulation Rule and Market Behavior",
        keywords=["anti-manipulation", "EPAct 2005", "fraud", "market manipulation", "civil penalties"],
        conclusion_template=[
            "FERC anti-manipulation rule (18 CFR 1c.1) prohibits fraud and market manipulation in jurisdictional energy markets.",
            "Violations require (1) fraudulent device/scheme, (2) with scienter, (3) in connection with jurisdictional transaction.",
            "Civil penalties up to $1,000,000 per day per violation; disgorgement of unjust profits; potential criminal referral."
        ],
        reasoning_framework="""
Energy Policy Act of 2005 Section 1283 granted FERC anti-manipulation authority modeled on SEC Rule 10b-5.
18 CFR Section 1c.1 prohibits:
(a) Fraudulent devices, schemes, or artifices to defraud
(b) Untrue statements or omissions of material fact
(c) Engaging in acts or practices that operate as fraud or deceit

Elements for violation:
1. Fraudulent device, scheme, or artifice
2. Scienter (intent to defraud or reckless disregard)
3. In connection with: (i) jurisdictional sale/purchase/transmission, (ii) RTO/ISO market activities, or (iii) receipt of RTO/ISO services

Types of manipulative conduct:
- Physical withholding (uneconomic generation curtailment to raise prices)
- Economic withholding (inflated offer prices not reflecting true costs)
- Wash trades (offsetting transactions to create false volume/price signals)
- False information to system operator (inaccurate resource capability data)
- Cross-market manipulation (RTO market positions hedged with FTR gaming)

Enforcement process:
- Office of Enforcement investigation (data requests, depositions)
- Preliminary findings and show cause order
- Settlement negotiations or hearing before ALJ
- FERC final order subject to D.C. Circuit appeal

Penalties assessed based on:
- Seriousness of violation (harm to markets, consumers)
- Duration and repetition
- Unjust profits obtained
- Cooperation with investigation
- History of prior violations
        """,
        key_factors=[
            "Intent or reckless disregard (scienter element)",
            "Economic rationale for resource offers and bidding behavior",
            "Accuracy of data submitted to RTO/ISO",
            "Unjust profits calculation methodology",
            "Cooperation with FERC investigation",
            "Implementation of compliance program post-violation"
        ],
        primary_authority=[
            "16 U.S.C. Section 824v (EPAct 2005 Section 1283)",
            "18 CFR Section 1c.1 (FERC anti-manipulation rule)",
            "FERC Enforcement Policy Statement (2011)",
            "Barclays, BP, and Deutsche Bank FERC enforcement orders (precedent on manipulation theories)"
        ],
        burden_holder="FERC Office of Enforcement must prove fraud and scienter by preponderance of evidence",
        adversary_position="FERC may allege offers deviated from marginal cost without economic justification, or data submissions were knowingly false",
        counter_arguments=[
            "Offers reflected legitimate costs, risks, and opportunity costs",
            "No intent to defraud; pricing errors were inadvertent",
            "RTO market rules permitted bidding strategy employed",
            "Unjust profits calculation ignores losses on other positions",
            "Robust compliance program in place and enhanced post-investigation"
        ],
        resolution_strategy="Document economic basis for all offers and market strategies; implement surveillance and compliance controls; cooperate fully with FERC investigation; retain counsel early; consider settlement to cap penalty exposure",
        entity_scope="Market participants in FERC-jurisdictional RTO/ISO markets, physical and financial traders",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Manipulation standard requires scienter; FERC bears burden but enforcement actions often settle; intent determinations highly fact-specific",
        controlling_precedent="16 U.S.C. Section 824v; 18 CFR 1c.1; Barclays enforcement order (D.C. Cir. 2016 upholding FERC authority)",
        category=IssueCategory.MARKET_RULES
    ),
    DoctrineBlock(
        topic="Large Generator Interconnection Process",
        keywords=["interconnection", "LGIP", "LGIA", "network upgrades", "cost allocation"],
        conclusion_template=[
            "FERC pro forma Large Generator Interconnection Procedures govern interconnection of generators over 20 MW to transmission system.",
            "Generator pays for interconnection facilities and network upgrades; may receive credits for network upgrade costs if subsequent generators benefit.",
            "Interconnection study queue managed by transmission provider; FERC Order 2023 reforms address queue backlog."
        ],
        reasoning_framework="""
FERC Order 2003 established standardized LGIP and LGIA for generators >20 MW.
FERC Order 2023 (2023) reformed queue process to address backlog.

Interconnection process stages:
1. Interconnection request filed with transmission provider (refundable deposit)
2. Feasibility study (optional, identifies potential issues)
3. System impact study (contingency analysis, short circuit, stability)
4. Facilities study (detailed cost estimate for interconnection and network upgrades)
5. LGIA execution (or unexecuted filing at FERC)
6. Construction of facilities
7. In-service and commencement of commercial operation

Cost allocation:
- Generator pays 100% of interconnection facilities (gen-tie, substation gear)
- Generator pays upfront for network upgrades (transmission system modifications needed for reliability)
- Generator may receive credits if subsequent generators cause same upgrades (but credits uncertain and long-delayed)
- Transmission provider owns network upgrades; generator gets option to build

Order 2023 reforms:
- Cluster study process replaces first-come-first-served
- Site control and financial deposits required earlier
- Increased deposits and penalties for withdrawals
- Accelerated timelines for study completion
- Technology-specific variations (energy storage, co-located resources)

Common disputes:
- Scope and cost of network upgrades
- Study assumptions (dispatch levels, future generation)
- Delay in study completion by transmission provider
- Allocation of upgrade costs among multiple generators
        """,
        key_factors=[
            "Site control demonstration (ownership or option)",
            "Commercial readiness deposit amount",
            "Study assumptions (MW capacity, dispatch profile)",
            "Network upgrade scope and cost estimate accuracy",
            "Construction timeline and in-service date",
            "Withdrawal penalties and deposit refund terms",
            "Affected system coordination (if impacting neighbor transmission system)"
        ],
        primary_authority=[
            "FERC Order 2003 (Standardized Generator Interconnection Procedures)",
            "FERC Order 2023 (Interconnection Queue Reforms, 2023)",
            "Pro forma LGIP and LGIA (Appendix to transmission provider OATT)",
            "Individual transmission provider LGIP/LGIA (may have regional variations)"
        ],
        burden_holder="Generator must demonstrate commercial readiness and financial ability to complete project; transmission provider must complete studies on schedule",
        adversary_position="Transmission provider may claim generator failed to meet milestones or withdrew without penalty justification",
        counter_arguments=[
            "Study delays caused by transmission provider exceeded timelines",
            "Network upgrade costs excessive and not supported by detailed engineering",
            "Affected system upgrades improperly allocated to generator",
            "Commercial operation date delays due to force majeure"
        ],
        resolution_strategy="Submit interconnection request with site control and robust commercial readiness showing; engage early with transmission provider on study assumptions; challenge upgrade scope via independent engineering review; preserve FERC complaint rights",
        entity_scope="Wind, solar, battery storage, and conventional generators over 20 MW; transmission providers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="LGIP framework well-established; Order 2023 reforms create new procedural hurdles; cost allocation disputes common but FERC precedent favors generator paying network upgrades",
        controlling_precedent="FERC Orders 2003, 2023; Pro forma LGIP/LGIA; individual transmission provider tariffs",
        category=IssueCategory.INTERCONNECTION
    ),
    DoctrineBlock(
        topic="FERC Reliability Coordinator and Balancing Authority Registration",
        keywords=["reliability coordinator", "balancing authority", "registration", "NERC functional entity"],
        conclusion_template=[
            "Reliability Coordinators and Balancing Authorities must register with NERC and comply with applicable reliability standards.",
            "RC responsibilities include wide-area reliability monitoring and authority to direct BAs and TOPs.",
            "BA responsibilities include load-resource balance, frequency control, and interchange scheduling."
        ],
        reasoning_framework="""
FERC designated NERC as Electric Reliability Organization under Section 215.
NERC Functional Model defines roles:

Reliability Coordinator (RC):
- Wide-area view of bulk electric system
- Real-time monitoring and analysis
- Authority to direct BAs, TOPs, GOPs in emergencies
- Coordinate outages and operating plans
- Applicable standards: TOP, IRO series

Balancing Authority (BA):
- Maintain load-resource balance in BA area
- Ensure ACE (Area Control Error) within limits
- Deploy frequency regulation and contingency reserves
- Schedule interchange with neighboring BAs
- Applicable standards: BAL series (BAL-001, BAL-002, BAL-003)

Registration process:
- Entity self-identifies functional role(s)
- Submits registration to Regional Entity
- NERC approves registration
- Entity becomes subject to compliance audits for applicable standards

De-registration:
- Must transfer responsibilities to successor entity
- NERC approval required
- Transition plan ensures no reliability gap
        """,
        key_factors=[
            "Functional entity role determination",
            "Compliance program adequacy for applicable standards",
            "Real-time monitoring and control center capabilities",
            "Coordination agreements with neighboring entities",
            "Qualified system operators and training programs"
        ],
        primary_authority=[
            "16 U.S.C. Section 824o (Energy Policy Act Section 215)",
            "NERC Rules of Procedure Section 500 (Registration)",
            "NERC Functional Model and glossary of terms",
            "NERC Reliability Standards (TOP, IRO, BAL series)"
        ],
        burden_holder="Registered entity must demonstrate compliance with applicable reliability standards via audits and self-certifications",
        adversary_position="NERC Regional Entity may cite violations of TOP/IRO/BAL standards in compliance audits",
        counter_arguments=[
            "Actions taken were consistent with operating procedures and good utility practice",
            "System conditions were beyond entity's control",
            "Standard language is ambiguous and entity's interpretation was reasonable"
        ],
        resolution_strategy="Conduct gap analysis of compliance obligations; implement compliance program with evidence repository; train operators on standards; file self-reports for potential violations; mitigate and remediate promptly",
        entity_scope="ISOs, RTOs, large utilities serving as RC or BA",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Registration requirements and standards compliance framework well-established; violation determinations are fact-specific",
        controlling_precedent="Energy Policy Act Section 215; NERC Rules of Procedure; applicable reliability standards",
        category=IssueCategory.NERC_RELIABILITY
    ),
    DoctrineBlock(
        topic="Texas Transmission Cost Recovery Factor (TCCRF)",
        keywords=["TCCRF", "ERCOT", "transmission", "cost recovery", "TSP"],
        conclusion_template=[
            "ERCOT transmission service providers recover wholesale transmission costs via TCCRF charges allocated to loads.",
            "TCCRF updated annually based on TSP revenue requirement filings reviewed by PUCT.",
            "Costs include FERC-approved ROE (currently 9.4%) applied to rate base of ERCOT transmission facilities."
        ],
        reasoning_framework="""
PURA Section 35.004 requires retail rates to include wholesale transmission cost component.
ERCOT transmission cost recovery:

Annual process:
- Each TSP files revenue requirement and rate base with PUCT (March filing)
- PUCT staff reviews for prudence and compliance with PURA Section 36 ratemaking
- PUCT approves or modifies revenue requirement (June order)
- ERCOT calculates TCCRF rate based on approved revenue requirements and load ratio share
- TCCRF effective September 1 annually

Revenue requirement components:
- Return on invested capital: Rate base x WACC (debt + equity ROE)
- Depreciation expense
- Operation and maintenance expense
- Property taxes and regulatory assessments

Rate base:
- Original cost of transmission facilities (>60 kV)
- Construction work in progress (subject to AFUDC rules)
- Less: accumulated depreciation, ADIT

Load ratio share allocation:
- Each load serving entity pays TCCRF based on 4CP (four coincident peak) contribution to ERCOT peak demand
- Encourages demand response during peak periods to reduce transmission charges

Common issues:
- Plant classification (transmission vs distribution; voltage level not dispositive)
- CWIP vs AFUDC treatment during construction
- ROE level (currently 9.4% approved for most TSPs)
- Prudence of capital projects (need demonstration, competitive procurement)
        """,
        key_factors=[
            "Transmission plant additions and retirements during year",
            "ROE approved by PUCT (9.4% current benchmark)",
            "CWIP balance and AFUDC accrual",
            "O&M expense levels and prudence review",
            "Depreciation rate changes",
            "Load ratio share impact of demand profile"
        ],
        primary_authority=[
            "PURA Section 35.004 (wholesale transmission costs in retail rates)",
            "PURA Section 36 (ratemaking principles)",
            "16 TAC Section 25.192 (TCCRF process)",
            "PUCT annual TCCRF docket orders"
        ],
        burden_holder="TSP must prove costs are reasonable and prudently incurred; PUCT staff and intervenors may challenge",
        adversary_position="Intervenors may argue capital projects lack demonstrated need or costs are excessive",
        counter_arguments=[
            "Transmission plan approved by ERCOT planning process demonstrates need",
            "Competitive procurement shows costs are reasonable",
            "ROE reflects current capital costs and TSP risk profile",
            "CWIP treatment consistent with FERC precedent and ensures timely cost recovery"
        ],
        resolution_strategy="Document need for transmission projects via ERCOT planning; use competitive bidding for construction; file complete TCCRF application with detailed cost support; respond to discovery requests",
        entity_scope="ERCOT transmission service providers (investor-owned utilities, cooperatives, municipals owning transmission)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="TCCRF process well-established; PUCT applies PURA Section 36 ratemaking consistently; ROE disputes possible but within narrow range",
        controlling_precedent="PURA Sections 35.004, 36; 16 TAC 25.192; PUCT TCCRF docket orders",
        category=IssueCategory.STATE_COMMISSION
    ),
    DoctrineBlock(
        topic="FERC Demand Response Compensation Order 745",
        keywords=["demand response", "Order 745", "LMP", "net benefits test", "EPSA"],
        conclusion_template=[
            "FERC Order 745 requires RTOs to compensate demand response at full locational marginal price when DR clears Day-Ahead or Real-Time markets.",
            "Compensation conditioned on DR passing net benefits test (LMP exceeds DR cost plus generation displaced).",
            "Supreme Court in EPSA v. FERC upheld FERC jurisdiction over RTO demand response programs."
        ],
        reasoning_framework="""
FERC Order 745 (2011) established compensation framework for demand response in organized markets:

Compensation rule:
- DR resources clearing RTO/ISO energy market paid full LMP
- Applies when: (1) DR balances supply/demand as alternative to generation, (2) DR passes net benefits test

Net benefits test:
- LMP at DR location > (cost of DR + cost of generation not served by DR)
- Ensures DR payment does not raise rates to other customers
- RTO calculates test using dispatch model

Threshold issue - retail vs wholesale:
- DR aggregators enroll retail customers to bid load reduction into wholesale market
- Supreme Court EPSA v. FERC (2016): FERC has jurisdiction over RTO DR programs because they directly affect wholesale rates
- State retail rate authority not preempted because FERC rule does not set retail rates

RTO implementation:
- PJM, NYISO, ISO-NE, MISO, CAISO each have DR programs
- Registration, telemetry, baseline calculation, performance measurement
- Penalties for non-performance during dispatch

Baseline methodology:
- Customer baseline (CBL) = load that would have occurred absent DR event
- High 5 of 10 method common (5 highest usage days of prior 10 similar days)
- Baseline accuracy critical to avoid over-compensation
        """,
        key_factors=[
            "DR clearing RTO Day-Ahead or Real-Time market",
            "Net benefits test result",
            "Baseline methodology accuracy",
            "Telemetry and performance measurement",
            "Dual participation rules (DR + bilateral contract conflicts)",
            "Non-performance penalties"
        ],
        primary_authority=[
            "FERC Order 745 (Demand Response Compensation, 2011)",
            "FERC v. Electric Power Supply Association, 577 U.S. 260 (2016) (EPSA)",
            "RTO tariffs implementing Order 745 (PJM Manual 11, NYISO Demand Response Manual, etc.)"
        ],
        burden_holder="DR provider must demonstrate performance via telemetry and baseline comparison",
        adversary_position="RTO may disallow payments if baseline inflated or performance not verified; states may challenge FERC jurisdiction",
        counter_arguments=[
            "Baseline methodology follows RTO tariff and FERC-approved protocols",
            "Performance verified by independent meter data",
            "Net benefits test passed; DR reduced LMP and benefited all customers",
            "FERC jurisdiction upheld by Supreme Court in EPSA"
        ],
        resolution_strategy="Implement robust telemetry and baseline protocols; model net benefits test under various dispatch scenarios; engage with RTO on performance measurement disputes; cite EPSA precedent if jurisdiction challenged",
        entity_scope="Demand response providers, curtailment service providers, retail customers enrolled in DR",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Order 745 and EPSA provide clear framework; baseline disputes common but tariff protocols apply; net benefits test is mechanical calculation",
        controlling_precedent="FERC Order 745; EPSA v. FERC (Supreme Court 2016); RTO tariffs",
        category=IssueCategory.MARKET_RULES
    ),
    DoctrineBlock(
        topic="Environmental Compliance for Generation Facilities",
        keywords=["EPA", "air emissions", "water discharge", "NPDES", "NSPS", "MATS"],
        conclusion_template=[
            "EPA regulates power plant air emissions under Clean Air Act (NSPS, NESHAP, state SIPs) and water discharges under Clean Water Act (NPDES permits).",
            "Coal and gas-fired units subject to mercury, SO2, NOx, particulate matter, and CO2 emission limits.",
            "Violations may result in civil penalties, injunctive relief, and citizen suits; state agencies enforce delegated programs."
        ],
        reasoning_framework="""
Clean Air Act (CAA) regulatory framework for power plants:
- New Source Performance Standards (NSPS): 40 CFR Part 60 Subpart Da (utility boilers), TTTT (gas turbines)
- National Emission Standards for Hazardous Air Pollutants (NESHAP): 40 CFR Part 63 Subpart UUUUU (MATS for coal/oil units)
- Regional Haze and SIP requirements: NOx and SO2 controls for visibility protection
- Greenhouse Gas: EPA Section 111(d) regulation for existing units (fluctuating regulatory status)

Key emission limits:
- Mercury and Air Toxics Standards (MATS): Hg, acid gases, non-Hg metals from coal units
- Cross-State Air Pollution Rule (CSAPR): SO2 and NOx budgets for interstate transport
- Ozone season NOx controls: CEMS monitoring and allowance surrender

Clean Water Act (CWA):
- NPDES permit required for discharge of pollutants to waters of U.S.
- Effluent limitation guidelines (40 CFR Part 423): thermal discharge, metals, pH
- Cooling water intake structures (316(b)): minimize impingement and entrainment of aquatic organisms

Compliance monitoring:
- Continuous Emission Monitoring Systems (CEMS) for NOx, SO2, CO2
- Quarterly excess emissions reports to EPA/state
- Annual compliance certification
- Violation = any hour exceeding limit triggers report and potential enforcement

Enforcement:
- EPA or state agency notice of violation
- Administrative compliance order or civil penalty (up to $25,000/day pre-2008, $50,000+/day post-2008 adjusted for inflation)
- Citizen suits under CAA Section 304 or CWA Section 505
- Supplemental environmental projects may offset penalties
        """,
        key_factors=[
            "Unit type (coal, gas, oil) and size (MW capacity)",
            "Age (existing vs new source triggering NSPS)",
            "Emission control technology installed (scrubber, SCR, baghouse, ESP)",
            "CEMS data quality and excess emission events",
            "NPDES permit limits and monitoring requirements",
            "State SIP applicability and stricter state standards",
            "Compliance history and good faith efforts"
        ],
        primary_authority=[
            "42 U.S.C. Sections 7401 et seq (Clean Air Act)",
            "40 CFR Part 60 (NSPS), Part 63 (NESHAP)",
            "40 CFR Part 423 (Steam Electric Effluent Limitations)",
            "33 U.S.C. Section 1251 et seq (Clean Water Act)",
            "State SIP regulations and NPDES permit conditions"
        ],
        burden_holder="Facility operator must demonstrate continuous compliance via monitoring and reporting",
        adversary_position="EPA or state may allege excess emissions or monitoring failures; citizen groups may sue for ongoing violations",
        counter_arguments=[
            "Excess emissions due to malfunction or startup/shutdown (upset defense)",
            "Control equipment operated consistent with manufacturer specs and good practices",
            "Prompt reporting and corrective action taken",
            "Compliance plan and capital investments demonstrate good faith"
        ],
        resolution_strategy="Implement preventive maintenance to minimize excess emission events; file timely deviation reports; engage EPA/state early on compliance issues; consider SEP to resolve enforcement; defend malfunction claims with detailed documentation",
        entity_scope="Coal, gas, and oil-fired power plants; industrial boilers; combustion turbines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CAA and CWA regulatory frameworks explicit; CEMS data hard to refute; upset defense available but fact-intensive; settlement common",
        controlling_precedent="CAA Sections 111, 112; CWA Section 402; 40 CFR Parts 60, 63, 423; state SIPs and NPDES permits",
        category=IssueCategory.ENVIRONMENTAL
    ),
    DoctrineBlock(
        topic="FERC Open Access Transmission Tariff (OATT) Administration",
        keywords=["OATT", "Order 888", "ATC", "reservation", "curtailment", "network service"],
        conclusion_template=[
            "FERC Order 888 requires utilities to file non-discriminatory open access transmission tariffs.",
            "OATT provides firm and non-firm point-to-point service and network integration service.",
            "Available Transfer Capability posted via OASIS; curtailments follow pro-rata or other approved priority rules."
        ],
        reasoning_framework="""
FERC Order 888 (1996) and Order 890 (2007) establish open access transmission framework.

OATT service types:
1. Firm Point-to-Point: Reservation from Point of Receipt to Point of Delivery, not curtailed except in emergencies
2. Non-Firm Point-to-Point: Hourly, daily, weekly, monthly; curtailed before firm service
3. Network Integration: Allows load-serving entity to integrate generation across transmission system

Transmission provider obligations:
- File OATT with rates, terms, conditions
- Post Available Transfer Capability (ATC) on OASIS every hour
- Process reservation requests in OASIS queue (first-come-first-served for point-to-point)
- Curtail non-firm before firm; within firm, pro-rata or approved priority

Rates:
- Stated rate for point-to-point ($/kW-month)
- Network service rate = revenue requirement / monthly 12CP load
- Ancillary services: scheduling, reactive supply, frequency regulation, operating reserves, etc.

Comparability standard:
- Transmission provider must offer same terms to third parties as it takes for its own uses
- Functional separation of transmission and merchant functions
- Standards of conduct prevent undue preference

Common disputes:
- ATC calculation methodology
- Curtailment allocation (pro-rata vs other)
- Redirect rights and rollover priority
- Native load priority vs OATT customers
        """,
        key_factors=[
            "Reservation priority and timing (OASIS queue time stamp)",
            "Firm vs non-firm service type",
            "ATC availability at time of request",
            "Curtailment methodology and notice",
            "Ancillary service charges",
            "Contract path vs flow-based rights"
        ],
        primary_authority=[
            "FERC Order 888 (Open Access Transmission, 1996)",
            "FERC Order 890 (Transmission Planning and Cost Allocation, 2007)",
            "Pro forma OATT (Attachment to Order 888, as amended)",
            "18 CFR Part 37 (OASIS regulations)"
        ],
        burden_holder="Transmission customer must submit timely reservation request; transmission provider must process non-discriminatorily",
        adversary_position="Transmission provider may deny request due to insufficient ATC; customer may allege undue discrimination",
        counter_arguments=[
            "ATC calculation follows FERC-approved methodology",
            "Curtailments applied pro-rata to all non-firm service",
            "Denial based on reliability criteria, not commercial preference",
            "OATT terms applied uniformly to all customers"
        ],
        resolution_strategy="Monitor OASIS ATC postings; submit reservation requests promptly; challenge denials via FERC complaint if discrimination alleged; negotiate bilateral agreements for firm capacity",
        entity_scope="Transmission providers, transmission customers (utilities, marketers, generators)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="OATT framework well-established; ATC disputes turn on modeling assumptions; comparability standard enforced via complaint process",
        controlling_precedent="FERC Orders 888, 890; Pro forma OATT; transmission provider-specific OATT",
        category=IssueCategory.FERC_REGULATION
    ),
    DoctrineBlock(
        topic="State Renewable Energy Siting and Permitting",
        keywords=["siting", "permitting", "renewable energy", "wind", "solar", "state jurisdiction"],
        conclusion_template=[
            "States retain primary authority over siting and permitting of generation facilities including renewables.",
            "State processes vary: some have expedited renewable siting statutes, others use general utility siting laws.",
            "Local zoning may apply; some states preempt local authority for projects above size thresholds."
        ],
        reasoning_framework="""
Federal Power Act Section 201(b)(1) reserves to states authority over facilities used for generation.
State siting processes vary widely:

Centralized state siting (e.g., NY Article 10, CA Energy Commission):
- State agency has exclusive or primary jurisdiction
- Consolidated review of environmental, land use, public interest
- Preempts local zoning for large projects
- Certificate or permit issued after evidentiary hearing

Dual state/local (e.g., Texas):
- State permit for air quality (TCEQ) and water (TCEQ)
- Local zoning and special use permits (county or city)
- No state preemption for most renewable projects
- Landowner agreements and community engagement critical

Streamlined renewable siting (e.g., some Midwest states):
- Expedited timelines for wind/solar
- Standard setback and decommissioning requirements
- Financial assurance for decommissioning
- Wildlife and visual impact studies

Common permit requirements:
- Environmental review (state NEPA-equivalent or SEPA)
- Endangered species surveys and avoidance plans
- Wetlands and water quality certifications (CWA Section 401)
- FAA determination of no hazard for wind turbines
- Interconnection agreement (separate process)
- Local property tax abatement or PILOT negotiations

Challenges:
- Local opposition (noise, visual, property value concerns)
- Endangered species (bats for wind, desert tortoise for solar)
- Cultural resources (tribal consultation, historic sites)
- Agricultural land conversion
        """,
        key_factors=[
            "State siting statute applicability and thresholds",
            "Local zoning authority and preemption",
            "Environmental impact assessment requirements",
            "Endangered species presence and mitigation",
            "Public hearing and community opposition",
            "Interconnection queue position and viability",
            "Property tax treatment and PILOT agreements"
        ],
        primary_authority=[
            "State utility siting statutes (vary by state)",
            "State environmental review statutes (state NEPA equivalents)",
            "Local zoning ordinances",
            "Federal Endangered Species Act (consultation with USFWS)",
            "Clean Water Act Section 401 (state water quality certification)"
        ],
        burden_holder="Project developer must demonstrate compliance with state/local siting criteria and environmental standards",
        adversary_position="Local governments, residents, environmental groups may oppose on environmental, aesthetic, or economic grounds",
        counter_arguments=[
            "Project complies with all setback and noise standards",
            "Wildlife surveys show minimal impact; avoidance and minimization measures in place",
            "Economic benefits (tax revenue, jobs) outweigh aesthetic concerns",
            "State preemption statute bars local zoning restrictions",
            "Decommissioning plan and financial assurance protect county"
        ],
        resolution_strategy="Engage local stakeholders early; site to avoid sensitive areas; offer community benefit agreements; conduct thorough environmental studies; retain experienced permitting counsel",
        entity_scope="Wind, solar, battery storage developers; state siting agencies; local governments",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="State siting laws vary widely; local political dynamics unpredictable; environmental challenges fact-intensive; preemption doctrines state-specific",
        controlling_precedent="State-specific siting statutes and case law; federal ESA and CWA apply nationally",
        category=IssueCategory.RENEWABLE_STANDARDS
    ),
    DoctrineBlock(
        topic="Electric Reliability Council (ERCOT) Governance and Oversight",
        keywords=["ERCOT", "governance", "PUCT", "board", "independent market monitor", "protocols"],
        conclusion_template=[
            "ERCOT operates Texas electric grid under PUCT oversight as independent system operator.",
            "ERCOT governance includes board of directors with diverse stakeholder representation.",
            "PUCT retains authority to approve protocol changes, investigate market operations, and enforce PURA."
        ],
        reasoning_framework="""
PURA Section 39.151 establishes ERCOT as independent organization to operate electric grid in ERCOT region.

ERCOT structure:
- Board of Directors: mix of market participants (generators, REPs, TDUs) and independent/unaffiliated members
- CEO and staff operate markets and grid
- Technical Advisory Committee (TAC): stakeholder body recommending protocol changes
- Independent Market Monitor: monitors for market power abuse and recommends rule changes

PUCT oversight:
- Approves ERCOT budget and fees (PURA 39.151(e))
- Approves Nodal Protocol Revision Requests (NPRRs)
- Investigates market events and outages
- Can decertify ERCOT if fails duties (never exercised)

Protocol governance:
- NPRR filed by market participant or ERCOT staff
- TAC reviews and votes recommendation
- ERCOT board approves (for most NPRRs)
- PUCT approves if protocol materially affects rates or reliability
- Emergency protocols can be approved out-of-cycle

Market Monitor role:
- Publishes annual State of the Market report
- Investigates anomalous market outcomes
- Reports potential manipulation to PUCT Enforcement
- Recommends protocol changes to improve competition

Major events tested governance:
- Winter Storm Uri (Feb 2021): ERCOT/PUCT criticized for market pricing and rolling blackouts
- Subsequent legislative reforms: weatherization mandates, ERCOT board restructuring, market redesign debates
        """,
        key_factors=[
            "Board composition and stakeholder representation",
            "TAC voting dynamics on protocol changes",
            "PUCT discretion to approve/modify NPRRs",
            "Market Monitor findings and recommendations",
            "Legislative oversight and reform pressures",
            "ERCOT operational performance during extreme weather"
        ],
        primary_authority=[
            "PURA Section 39.151 (ERCOT organization)",
            "16 TAC Section 25.361 (ERCOT governance)",
            "ERCOT Bylaws (board structure, voting)",
            "ERCOT Nodal Protocols Section 21 (governance and revision process)"
        ],
        burden_holder="ERCOT must operate grid reliably and administer markets consistent with PURA and PUCT rules; board owes fiduciary duty to Texas electricity market",
        adversary_position="Market participants may challenge protocol changes as unfair or economically harmful; PUCT may investigate ERCOT for operational failures",
        counter_arguments=[
            "Protocol change approved via stakeholder process and ERCOT board vote",
            "Operational decisions made in real-time based on reliability needs",
            "ERCOT followed protocols in effect at time of event",
            "Legislative reforms addressed identified gaps post-Uri"
        ],
        resolution_strategy="Participate actively in TAC and NPRR process; engage PUCT staff on market design issues; document operational decisions during emergency events; advocate for fair protocol changes",
        entity_scope="ERCOT, market participants, PUCT, Texas Legislature",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PURA grants PUCT broad oversight authority; ERCOT governance framework established but evolving post-Uri; protocol disputes resolved via PUCT process",
        controlling_precedent="PURA Section 39.151; 16 TAC 25.361; ERCOT Bylaws and Protocols",
        category=IssueCategory.STATE_COMMISSION
    ),
    DoctrineBlock(
        topic="Tax Treatment of Renewable Energy Tax Credits",
        keywords=["ITC", "PTC", "investment tax credit", "production tax credit", "IRS", "26 USC"],
        conclusion_template=[
            "Federal investment tax credit (ITC) and production tax credit (PTC) incentivize renewable energy projects.",
            "ITC = 30% of qualified cost basis (solar, offshore wind); PTC = $/MWh for 10 years (onshore wind, others).",
            "Bonus credits available for domestic content, energy communities, low-income projects; transferability and direct pay rules under Inflation Reduction Act."
        ],
        reasoning_framework="""
Internal Revenue Code Section 48 (ITC) and Section 45 (PTC) provide renewable energy tax credits.
Inflation Reduction Act (2022) extended and enhanced credits.

ITC (26 USC Section 48):
- 30% of qualified property cost basis for solar, offshore wind, geothermal, certain storage
- Qualified property must be depreciable, used in U.S., placed in service by applicable deadline
- Recapture if property disposed within 5 years
- Technology-neutral ITC for zero-emission facilities (Section 48E, 2025+)

PTC (26 USC Section 45):
- $/MWh credit for electricity produced from qualified renewable resources
- 10-year production period starting with placed-in-service date
- Onshore wind: 2.75 cents/kWh base, higher with prevailing wage/apprenticeship
- Technology-neutral PTC (Section 45Y, 2025+)

Bonus credits (IRA adders):
- Domestic content: +10% ITC or +10% PTC if steel/iron and manufactured components U.S.-made
- Energy communities: +10% if in brownfield, coal closure area, or fossil fuel employment area
- Low-income communities: +10-20% for solar in low-income or tribal areas

Transferability (26 USC Section 6418):
- Credits can be sold to unrelated third party for cash
- Buyer claims credit on tax return; seller has no further benefit
- Replaces tax equity structures for many projects

Direct pay (26 USC Section 6417):
- Tax-exempt entities and governmental bodies can elect cash payment instead of credit
- IRS pays refundable credit within prescribed timeline
- Simplifies financing for municipal and cooperative projects

IRS guidance and compliance:
- Notice of energy project registration required
- Beginning of construction rules (physical work or 5% safe harbor)
- Prevailing wage and apprenticeship attestations
- Domestic content certification from suppliers
        """,
        key_factors=[
            "Qualified technology and placed-in-service deadline",
            "Eligible cost basis (direct costs, no land or intangibles)",
            "Beginning of construction safe harbor compliance",
            "Prevailing wage and apprenticeship compliance for bonus credit",
            "Domestic content certification and tracking",
            "Transferability buyer creditworthiness and pricing",
            "Direct pay election timing and IRS registration"
        ],
        primary_authority=[
            "26 USC Section 48 (Investment Tax Credit)",
            "26 USC Section 45 (Production Tax Credit)",
            "26 USC Sections 48E, 45Y (technology-neutral credits post-2024)",
            "26 USC Section 6417 (direct pay election)",
            "26 USC Section 6418 (credit transferability)",
            "IRS Notice 2023-17, 2024-XX (guidance on IRA credits)"
        ],
        burden_holder="Taxpayer must substantiate qualified costs, prevailing wage compliance, domestic content; transferee verifies credit validity",
        adversary_position="IRS may disallow credit if placed-in-service deadline missed, costs not qualified, or prevailing wage/apprenticeship noncompliance",
        counter_arguments=[
            "Costs properly capitalized and depreciable under tax accounting",
            "Beginning of construction physical work test met with sworn affidavit",
            "Prevailing wage paid and certified payroll records maintained",
            "Domestic content attestations obtained from suppliers in good faith",
            "Transfer agreement terms comply with Section 6418 requirements"
        ],
        resolution_strategy="Engage tax counsel early in project development; document beginning of construction; implement prevailing wage compliance program; obtain domestic content certifications; model transferability vs tax equity economics",
        entity_scope="Renewable energy project developers, tax equity investors, transferability buyers, tax-exempt/governmental entities",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="ITC/PTC statutory framework clear but IRS guidance evolving; transferability and direct pay new as of 2023; domestic content and prevailing wage compliance operationally complex",
        controlling_precedent="26 USC Sections 45, 48, 45Y, 48E, 6417, 6418; IRS Notices and Revenue Procedures",
        category=IssueCategory.RENEWABLE_STANDARDS
    ),
    DoctrineBlock(
        topic="FERC Compliance and Self-Reporting Obligations",
        keywords=["compliance", "self-report", "audit", "FERC enforcement", "violation"],
        conclusion_template=[
            "FERC-regulated entities must self-report violations of statutes, regulations, tariffs, and reliability standards.",
            "Self-reporting may reduce penalties under FERC Penalty Guidelines via cooperation credit.",
            "Entities subject to FERC compliance audits covering financial reporting, tariff compliance, and reliability standards."
        ],
        reasoning_framework="""
FERC enforcement framework:
- Office of Enforcement (OE) investigates violations via audits, data analysis, and complaints
- Penalty Guidelines assess violations based on seriousness, harm, duration, and culpability
- Settlement encouraged; hearing before ALJ if no settlement; FERC final order; D.C. Circuit appeal

Self-reporting requirement:
- Tariff violations, market rule violations, reliability standard violations should be promptly self-reported
- No express statutory deadline but prompt reporting expected
- Self-report triggers OE investigation but earns cooperation credit in penalty calculation

Penalty Guidelines factors:
1. Seriousness: harm to customers, markets, or reliability
2. Duration: single day vs ongoing violation
3. Baseline penalty per day
4. Culpability: intentional, reckless, negligent, or strict liability
5. Cooperation: self-report, remediation, audit cooperation
6. History: prior violations or clean record
7. Ability to pay (financial hardship)

Cooperation credit:
- Self-report within reasonable time: up to 50% penalty reduction
- Full cooperation with investigation: additional reduction
- Remedial measures implemented: mitigation credit

Compliance audits:
- Financial audits (formula rates, fuel cost recovery)
- Tariff compliance audits (OATT administration, affiliate transactions)
- Reliability audits (conducted by NERC Regional Entities, not FERC directly)

Common violations:
- Late filing of tariff revisions or reports
- Failure to follow OATT procedures (ATC posting, curtailment allocation)
- Market manipulation (addressed separately under 18 CFR 1c.1)
- Reliability standard violations (delegated to NERC but FERC can review)
        """,
        key_factors=[
            "Timing of self-report after violation discovery",
            "Cooperation with FERC investigation and data requests",
            "Remedial measures taken to prevent recurrence",
            "Prior compliance history with FERC",
            "Seriousness of violation and harm caused",
            "Whether violation was willful or inadvertent"
        ],
        primary_authority=[
            "16 U.S.C. Section 825e (FERC investigative authority)",
            "18 CFR Part 1b (FERC Penalty Guidelines)",
            "FERC Enforcement Policy Statement (2011)",
            "FERC Audit Program guidance"
        ],
        burden_holder="Regulated entity must self-report and cooperate; FERC OE must prove violation",
        adversary_position="FERC may impose maximum penalties if entity fails to self-report, conceals violation, or impedes investigation",
        counter_arguments=[
            "Violation promptly self-reported upon discovery",
            "Full cooperation with FERC audit and investigation",
            "Remedial measures prevent recurrence",
            "No harm to customers or markets",
            "Inadvertent error, not willful misconduct"
        ],
        resolution_strategy="Implement compliance monitoring to detect violations early; self-report promptly with detailed remediation plan; cooperate fully with FERC inquiries; negotiate settlement to cap penalty exposure",
        entity_scope="Public utilities, RTOs, pipelines, market participants subject to FERC jurisdiction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Penalty Guidelines provide predictable framework; cooperation credit incentivizes self-reporting; settlement common to avoid litigation",
        controlling_precedent="FERC Penalty Guidelines 18 CFR 1b; FERC Enforcement Policy Statement; FERC settlement precedent",
        category=IssueCategory.COMPLIANCE_REPORTING
    ),
    DoctrineBlock(
        topic="RTO/ISO Capacity Market Mechanisms",
        keywords=["capacity market", "RPM", "FCM", "ICAP", "resource adequacy", "MOPR"],
        conclusion_template=[
            "RTOs operate capacity markets to ensure long-term resource adequacy: PJM RPM, ISO-NE FCM, NYISO ICAP.",
            "Capacity obligations based on forecasted peak load plus reserve margin; resources clear via auction.",
            "FERC minimum offer price rule (MOPR) limits state-subsidized resources from suppressing capacity prices."
        ],
        reasoning_framework="""
Capacity market design ensures adequate generation and demand response to meet peak load plus reserves.

Market structures:
- PJM: Reliability Pricing Model (RPM), 3-year forward auction, descending clock, locational deliverability areas
- ISO-NE: Forward Capacity Market (FCM), 3-year forward, downward-sloping demand curve
- NYISO: Installed Capacity (ICAP) market, monthly and strip auctions, in-city and G-J locality requirements

Capacity obligation:
- LSEs allocated share of RTO forecasted peak load plus reserve margin (e.g., 15%)
- Resources bid to supply capacity; cleared resources receive capacity payment
- Performance requirements: must be available during peak hours or face penalties

MOPR (Minimum Offer Price Rule):
- Prevents state-subsidized new resources from offering below competitive level
- FERC Order 841 expanded MOPR in PJM to all state-subsidized resources
- Hughes v. Talen and subsequent FERC orders addressed state RPS/ZEC subsidies
- Exemptions for renewables and existing resources vary by RTO

Buyer-side mitigation:
- Screens new resources for market power (pivotal supplier, economic offer threshold)
- MOPR floor applied if resource receives out-of-market payment
- Controversy: state climate policies vs FERC rate authority

Resource accreditation:
- Effective load carrying capability (ELCC) for variable renewables
- Unforced capacity (UCAP) for thermal units based on forced outage rates
- Demand response capacity based on baseline and performance guarantees

Performance incentives:
- ISO-NE Pay-for-Performance: bonus/penalty based on actual output during shortage events
- PJM Capacity Performance: non-performance charges if fail to deliver during emergency
        """,
        key_factors=[
            "RTO capacity obligation forecast and reserve margin",
            "Resource accreditation methodology (UCAP, ELCC)",
            "Auction clearing price and locational price separation",
            "MOPR applicability to state-subsidized resources",
            "Performance measurement during peak events",
            "Contract duration (1 year vs multi-year)",
            "Replacement capacity rules if resource fails to qualify"
        ],
        primary_authority=[
            "PJM Reliability Assurance Agreement and tariff (RPM rules)",
            "ISO-NE Market Rule 1 Section III.13 (FCM)",
            "NYISO Services Tariff (ICAP)",
            "FERC Order 841 (expanded MOPR, 2019, partially reversed 2021)",
            "Hughes v. Talen Energy, 578 U.S. 150 (2016)"
        ],
        burden_holder="Resource owner must qualify and perform to earn capacity revenue; LSE must procure sufficient capacity or pay deficiency charge",
        adversary_position="RTO Market Monitor may challenge resource offer as below competitive price; state regulators may challenge MOPR as preempting state policy",
        counter_arguments=[
            "Resource offer reflects true going-forward costs",
            "State subsidy does not affect competitive offer behavior",
            "MOPR exemption applies (renewables in some RTOs)",
            "Capacity Performance penalties unjustified due to force majeure",
            "Resource accreditation methodology undervalues contribution"
        ],
        resolution_strategy="Model capacity revenues under various auction scenarios; challenge MOPR application via tariff complaint; demonstrate performance capability via historical data; negotiate bilateral capacity contracts outside auction as hedge",
        entity_scope="Generators, demand response providers, LSEs in PJM, ISO-NE, NYISO",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Capacity market rules complex and evolving; MOPR subject to FERC reconsideration and court review; performance incentives increasingly strict; state/federal tension unresolved",
        controlling_precedent="RTO tariffs; FERC capacity market orders; Hughes v. Talen precedent",
        category=IssueCategory.MARKET_RULES
    ),
    DoctrineBlock(
        topic="FERC Abandonment Authority for Pipelines",
        keywords=["abandonment", "pipeline", "NGA Section 7", "certificate", "environmental", "dismantlement"],
        conclusion_template=[
            "Interstate pipelines must obtain FERC authorization under NGA Section 7(b) to abandon facilities or service.",
            "Abandonment must not be detrimental to public interest; FERC considers customer impacts and alternatives.",
            "Pipeline may be required to dismantle facilities and restore site; cost recovery depends on tariff and rate case."
        ],
        reasoning_framework="""
Natural Gas Act Section 7(b) prohibits abandonment of facilities or service without FERC approval.

Abandonment application requirements:
- Description of facilities to be abandoned
- Reason for abandonment (lack of demand, uneconomic service, facility condition)
- Impact on customers (alternative supply sources)
- Environmental analysis (dismantlement, site restoration, or in-place abandonment)
- Cost estimate and rate impact

FERC public interest test:
- Customer needs and availability of alternative service
- Environmental impacts of abandonment vs continued operation
- Financial condition of pipeline and cost recovery
- Safety considerations

Dismantlement vs abandonment in place:
- Dismantlement required if environmental risk (contaminated soil, water crossings)
- Abandonment in place allowed if less environmental impact
- Pipeline must demonstrate landowner agreement or restoration plan

Cost recovery:
- Abandonment costs may be recoverable in rates if prudent
- Stranded costs (unrecovered investment) may be allocated to customers or shareholders
- Rate case proceeding determines allocation

Common scenarios:
- Low-throughput lateral abandonment (customers switched to alternative pipeline)
- Offshore platform abandonment (depleted field)
- Replacement of aging pipeline (new route, old route abandoned)
        """,
        key_factors=[
            "Remaining customer base and alternative supply options",
            "Environmental impacts of abandonment methods",
            "Dismantlement cost estimate and rate recovery",
            "Landowner agreements for site restoration",
            "Safety risks of continued operation vs abandonment",
            "Stranded cost allocation to customers vs shareholders"
        ],
        primary_authority=[
            "15 U.S.C. Section 717f(b) (NGA Section 7(b) abandonment)",
            "18 CFR Section 157.18 (abandonment applications)",
            "FERC Certificate Policy Statement (abandonment considerations)",
            "18 CFR Part 380 (environmental review of abandonment)"
        ],
        burden_holder="Pipeline must demonstrate abandonment is not detrimental to public interest",
        adversary_position="Customers may protest loss of service; environmental groups may demand full dismantlement and restoration",
        counter_arguments=[
            "Customers have alternative supply sources at comparable cost",
            "Environmental analysis supports abandonment in place as lower impact",
            "Dismantlement costs are excessive relative to environmental benefit",
            "Continued operation poses safety risk due to pipeline age"
        ],
        resolution_strategy="Conduct customer outreach early; evaluate alternative supply options; prepare robust environmental analysis comparing dismantlement vs in place; negotiate cost recovery in rate case",
        entity_scope="Interstate natural gas pipelines, LNG terminals",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Section 7(b) framework clear; public interest test allows FERC discretion; environmental review may extend timeline",
        controlling_precedent="NGA Section 7(b); FERC abandonment precedent; NEPA compliance",
        category=IssueCategory.FERC_REGULATION
    )
]

START_TIME = datetime.utcnow()
QUERY_COUNT = 0
TOTAL_RESPONSE_TIME_MS = 0.0
CACHE_HITS = 0
CACHE_QUERIES = 0


class REG07EnergyRegulatoryEngine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.query_log: List[Dict[str, Any]] = []
        self.coverage_map: Dict[str, int] = {d.topic: 0 for d in self.doctrines}
        logger.info(f"{ENGINE_NAME} initialized with {len(self.doctrines)} doctrine blocks")

    def search_doctrines(self, query: str, top_k: int = 5) -> List[DoctrineBlock]:
        query_lower = query.lower()
        scored = []
        for doctrine in self.doctrines:
            score = 0
            for keyword in doctrine.keywords:
                if keyword.lower() in query_lower:
                    score += 2
            if any(word in query_lower for word in doctrine.topic.lower().split()):
                score += 3
            for auth in doctrine.primary_authority:
                if any(term in query_lower for term in auth.lower().split()):
                    score += 1
            if score > 0:
                scored.append((score, doctrine))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for s, d in scored[:top_k]]

    def three_layer_response(
        self, query: str, mode: ResponseMode, zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        matched = self.search_doctrines(query, top_k=3)
        if not matched:
            return self.deep_analysis_fallback(query, mode, zone)

        for doctrine in matched:
            self.coverage_map[doctrine.topic] += 1

        primary = matched[0]
        authorities = primary.primary_authority[:]
        triggered = [primary.topic]
        confidence = primary.confidence

        if mode == ResponseMode.FAST:
            answer = primary.conclusion_template[0]
            if len(matched) > 1:
                triggered.append(matched[1].topic)
                authorities.extend(matched[1].primary_authority[:2])

        elif mode == ResponseMode.DEFENSE:
            parts = []
            parts.append("REGULATORY ANALYSIS:\n")
            parts.append(primary.conclusion_template[0])
            parts.append("\n\nAUTHORITY:")
            for auth in primary.primary_authority[:3]:
                parts.append(f"\n- {auth}")
            parts.append("\n\nKEY FACTORS:")
            for factor in primary.key_factors[:5]:
                parts.append(f"\n- {factor}")
            parts.append(f"\n\nBURDEN: {primary.burden_holder}")
            if zone == AnalysisZone.AUDIT:
                parts.append(f"\n\nCONFIDENCE: {primary.confidence_stratification}")
            answer = "".join(parts)
            for doc in matched[1:]:
                triggered.append(doc.topic)
                authorities.extend(doc.primary_authority[:1])

        else:
            parts = []
            parts.append(f"MEMORANDUM: {primary.topic}\n")
            parts.append("="*60 + "\n\n")
            parts.append("CONCLUSIONS:\n")
            for i, concl in enumerate(primary.conclusion_template, 1):
                parts.append(f"{i}. {concl}\n")
            parts.append("\nANALYSIS:\n")
            parts.append(primary.reasoning_framework)
            parts.append("\n\nKEY FACTORS:\n")
            for factor in primary.key_factors:
                parts.append(f"- {factor}\n")
            parts.append("\nCONTROLLING AUTHORITY:\n")
            for auth in primary.primary_authority:
                parts.append(f"- {auth}\n")
            parts.append(f"\nBURDEN OF PROOF: {primary.burden_holder}\n")
            parts.append(f"\nADVERSARY POSITION: {primary.adversary_position}\n")
            parts.append("\nCOUNTER-ARGUMENTS:\n")
            for arg in primary.counter_arguments:
                parts.append(f"- {arg}\n")
            parts.append(f"\nRESOLUTION STRATEGY: {primary.resolution_strategy}\n")
            parts.append(f"\nCONFIDENCE: {primary.confidence_stratification}\n")
            if len(matched) > 1:
                parts.append("\n\nRELATED DOCTRINES:\n")
                for doc in matched[1:]:
                    parts.append(f"- {doc.topic}: {doc.conclusion_template[0]}\n")
                    triggered.append(doc.topic)
                    authorities.extend(doc.primary_authority[:2])
            answer = "".join(parts)

        epistemic_flags = self.apply_epistemic_guardrails(answer, zone)
        return answer, authorities, triggered, confidence

    def deep_analysis_fallback(
        self, query: str, mode: ResponseMode, zone: AnalysisZone
    ) -> Tuple[str, List[str], List[str], ConfidenceLevel]:
        answer = (
            f"Deep regulatory analysis for: {query}\n\n"
            "This query requires synthesis across energy regulatory frameworks. "
            "Key considerations include federal vs state jurisdiction (FPA Section 201), "
            "applicable FERC orders and tariffs, NERC reliability standards if transmission/generation, "
            "state PUC rules if retail or distribution, and environmental compliance under CAA/CWA. "
            "Recommend detailed legal research on specific regulatory authority and precedent."
        )
        authorities = [
            "16 U.S.C. Section 824 (Federal Power Act)",
            "PURA (if Texas jurisdiction)",
            "NERC Reliability Standards"
        ]
        triggered = ["Deep Analysis Fallback"]
        confidence = ConfidenceLevel.DISCLOSURE
        return answer, authorities, triggered, confidence

    def apply_epistemic_guardrails(self, answer: str, zone: AnalysisZone) -> List[str]:
        flags = []
        if zone == AnalysisZone.PLANNING:
            if "must" in answer.lower() or "required" in answer.lower():
                flags.append("Planning zone answer uses mandatory language; verify for final reporting")
        if "penalty" in answer.lower() or "violation" in answer.lower():
            flags.append("Enforcement implications present; verify current penalty amounts and case law")
        if len(answer) > 3000 and zone != AnalysisZone.MEMO:
            flags.append("Response length exceeds typical FAST/DEFENSE scope")
        return flags

    async def query(self, request: QueryRequest) -> QueryResponse:
        global QUERY_COUNT, TOTAL_RESPONSE_TIME_MS, CACHE_HITS, CACHE_QUERIES
        start = datetime.utcnow()
        QUERY_COUNT += 1
        CACHE_QUERIES += 1

        logger.info(f"Query received: {request.query[:100]}... | Mode: {request.mode} | Zone: {request.zone}")

        answer, authorities, triggered, confidence = self.three_layer_response(
            request.query, request.mode, request.zone
        )
        epistemic_flags = self.apply_epistemic_guardrails(answer, request.zone)

        response_time_ms = (datetime.utcnow() - start).total_seconds() * 1000
        TOTAL_RESPONSE_TIME_MS += response_time_ms

        determinism_hash = hashlib.sha256(
            f"{request.query}{request.mode}{answer}".encode()
        ).hexdigest()[:16]

        self.query_log.append({
            "timestamp": start.isoformat(),
            "query": request.query,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "triggered_doctrines": triggered,
            "response_time_ms": response_time_ms,
            "confidence": confidence.value
        })

        logger.info(f"Query completed in {response_time_ms:.2f}ms | Doctrines: {len(triggered)}")

        return QueryResponse(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            answer=answer,
            confidence=confidence,
            authorities_cited=authorities,
            triggered_doctrines=triggered,
            epistemic_flags=epistemic_flags,
            response_time_ms=response_time_ms,
            determinism_hash=determinism_hash,
            timestamp=start.isoformat()
        )

    def get_health(self) -> HealthResponse:
        uptime = (datetime.utcnow() - START_TIME).total_seconds()
        avg_response = TOTAL_RESPONSE_TIME_MS / QUERY_COUNT if QUERY_COUNT > 0 else 0.0
        cache_hit_rate = CACHE_HITS / CACHE_QUERIES if CACHE_QUERIES > 0 else 0.0
        return HealthResponse(
            status="healthy",
            engine_id=ENGINE_ID,
            engine_name=ENGINE_NAME,
            version=VERSION,
            port=PORT,
            doctrines_loaded=len(self.doctrines),
            uptime_seconds=uptime,
            total_queries=QUERY_COUNT,
            avg_response_ms=avg_response,
            cache_hit_rate=cache_hit_rate
        )


engine_instance = REG07EnergyRegulatoryEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} energy regulatory doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down. Total queries: {QUERY_COUNT}")


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


@app.get("/health", response_model=HealthResponse)
async def health():
    return engine_instance.get_health()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        return await engine_instance.query(request)
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "categories": {cat.value: sum(1 for d in DOCTRINE_CACHE if d.category == cat) for cat in IssueCategory},
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "confidence": d.confidence.value,
                "keywords": d.keywords[:5]
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/coverage")
async def coverage_map():
    return {
        "coverage": engine_instance.coverage_map,
        "total_triggered": sum(engine_instance.coverage_map.values()),
        "untriggered": [topic for topic, count in engine_instance.coverage_map.items() if count == 0]
    }


@app.get("/")
async def root():
    return {
        "engine": ENGINE_NAME,
        "engine_id": ENGINE_ID,
        "version": VERSION,
        "status": "operational",
        "doctrines": len(DOCTRINE_CACHE),
        "categories": len(IssueCategory),
        "endpoints": ["/health", "/query", "/doctrines", "/coverage"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
