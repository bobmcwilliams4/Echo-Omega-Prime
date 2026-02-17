"""
REG05 Securities Regulatory Engine v1.0.0
Port 9125 | TIE-Grade Securities Compliance Intelligence

Covers: Securities Act 1933, Exchange Act 1934, Investment Company Act 1940,
Sarbanes-Oxley, Dodd-Frank, SEC registration, Reg D/A+/CF exemptions, Rule 144,
10b-5, insider trading, beneficial ownership reporting.
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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

ENGINE_ID = "REG05"
ENGINE_NAME = "Securities Regulatory Engine"
VERSION = "1.0.0"
PORT = 9125

logger.add(f"{ENGINE_ID}_audit.log", rotation="100 MB", retention="1 year", level="INFO")

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
    REGISTRATION = "REGISTRATION"
    EXEMPTIONS = "EXEMPTIONS"
    DISCLOSURE = "DISCLOSURE"
    INSIDER_TRADING = "INSIDER_TRADING"
    BENEFICIAL_OWNERSHIP = "BENEFICIAL_OWNERSHIP"
    FRAUD = "FRAUD"
    OFFERING_COMPLIANCE = "OFFERING_COMPLIANCE"
    PUBLIC_COMPANY = "PUBLIC_COMPANY"
    WHISTLEBLOWER = "WHISTLEBLOWER"
    BROKER_DEALER = "BROKER_DEALER"

@dataclass
class Authority:
    citation: str
    weight: int
    jurisdiction: str
    hierarchy_level: int

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[Authority]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_categories: List[IssueCategory] = field(default_factory=list)

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    authorities: List[str]
    reasoning_chain: List[str]
    triggered_doctrines: List[str]
    analysis_zone: AnalysisZone
    determinism_hash: str
    response_time_ms: int
    epistemic_status: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Securities Act Section 5 Registration Requirement",
        keywords=["section 5", "registration", "securities act", "public offering", "prospectus", "s-1"],
        conclusion_template=[
            "Securities Act Section 5 prohibits offers or sales of securities unless registered or exempt.",
            "Registration requires filing Form S-1 with SEC and delivery of prospectus to investors.",
            "Violations create strict liability for sellers and potential rescission rights for purchasers."
        ],
        reasoning_framework="""
        Section 5(a) prohibits sale unless registration statement is in effect.
        Section 5(b) prohibits delivery of security unless prospectus precedes or accompanies.
        Section 5(c) prohibits offers before filing registration statement.
        No scienter required - strict liability applies to Section 5 violations.
        Exemptions under Sections 3, 4 must be affirmatively established by issuer.
        Gun-jumping rules prohibit pre-filing publicity beyond tombstone ads.
        Testing-the-waters permitted for emerging growth companies post-JOBS Act.
        Shelf registration Rule 415 allows delayed offerings for eligible issuers.
        """,
        key_factors=[
            "Whether security offered or sold",
            "Registration statement filed and effective",
            "Prospectus delivered to purchasers",
            "Available exemption from registration",
            "Compliance with waiting period rules",
            "EGC status for testing-the-waters"
        ],
        primary_authority=[
            Authority("15 USC Section 77e", 100, "Federal", 1),
            Authority("17 CFR 230.415", 85, "Federal", 2),
            Authority("SEC v. Ralston Purina Co., 346 US 119 (1953)", 95, "Federal", 1)
        ],
        burden_holder="Issuer bears burden to establish exemption applicability",
        adversary_position="SEC argues broad interpretation of 'offer' and 'sale' to capture fundraising activity",
        counter_arguments=[
            "Exemption applies under Regulation D or Regulation A+",
            "No public offering under Ralston Purina private placement test",
            "Intrastate exemption Section 3(a)(11) satisfied",
            "Regulation S offshore safe harbor applies"
        ],
        resolution_strategy="File registration or establish clear exemption with legal opinion; cure defects via rescission offer if violation occurred",
        entity_scope="All issuers offering securities in US",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core securities law principle with Supreme Court precedent",
        controlling_precedent="SEC v. Ralston Purina Co. - registration required unless issuer proves exemption",
        issue_categories=[IssueCategory.REGISTRATION, IssueCategory.OFFERING_COMPLIANCE]
    ),
    DoctrineBlock(
        topic="Regulation D Rule 506(b) Private Placement Exemption",
        keywords=["reg d", "rule 506", "506(b)", "accredited investor", "private placement", "general solicitation"],
        conclusion_template=[
            "Rule 506(b) exempts private placements to unlimited accredited and up to 35 sophisticated investors.",
            "General solicitation and advertising prohibited; pre-existing relationship required.",
            "Form D filing required within 15 days; state registration preempted for covered securities."
        ],
        reasoning_framework="""
        Rule 506(b) safe harbor under Section 4(a)(2) private offering exemption.
        Permits unlimited accredited investors as defined in Rule 501(a).
        Up to 35 non-accredited but sophisticated investors permitted.
        Sophistication means knowledge/experience to evaluate merits and risks.
        No general solicitation or advertising - must have substantive pre-existing relationship.
        Reasonable inquiry required to verify accredited status (bank statements, tax returns, CPA letter).
        Form D filing mandatory via EDGAR within 15 days of first sale.
        Securities are restricted - Rule 144 holding period and resale restrictions apply.
        Blue sky preemption under Section 18 of Securities Act for covered securities.
        """,
        key_factors=[
            "Accredited investor status verified",
            "Non-accredited investors sophisticated",
            "No general solicitation or advertising",
            "Pre-existing substantive relationship",
            "Form D timely filed",
            "Restricted securities legend applied"
        ],
        primary_authority=[
            Authority("17 CFR 230.506(b)", 100, "Federal", 1),
            Authority("17 CFR 230.501(a)", 95, "Federal", 1),
            Authority("17 CFR 230.502(c)", 90, "Federal", 2)
        ],
        burden_holder="Issuer must prove exemption requirements satisfied",
        adversary_position="SEC scrutinizes general solicitation violations and inadequate verification procedures",
        counter_arguments=[
            "Communications were not general solicitation but private outreach",
            "Pre-existing relationship established through prior business dealings",
            "Reasonable steps taken to verify accredited status",
            "Form D filing delay was inadvertent and cured promptly"
        ],
        resolution_strategy="Document pre-existing relationships; implement robust verification procedures; file Form D timely; use restrictive legends",
        entity_scope="Private companies and funds raising capital",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established safe harbor with clear compliance requirements",
        controlling_precedent="SEC Release 33-10844 (2020) - harmonizing Reg D requirements",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.OFFERING_COMPLIANCE]
    ),
    DoctrineBlock(
        topic="Regulation D Rule 506(c) General Solicitation Exemption",
        keywords=["rule 506(c)", "general solicitation", "accredited investor", "verification", "jobs act"],
        conclusion_template=[
            "Rule 506(c) permits general solicitation if all purchasers are accredited and verified.",
            "Reasonable steps to verify accredited status required - heightened standard vs 506(b).",
            "Created by JOBS Act 2012; preempts state registration like 506(b)."
        ],
        reasoning_framework="""
        JOBS Act Section 201(a) directed SEC to eliminate general solicitation ban.
        Rule 506(c) adopted July 2013 as alternative to 506(b).
        Permits general solicitation and advertising to reach potential investors.
        All purchasers must be accredited investors - no sophisticated non-accredited allowed.
        Issuer must take reasonable steps to verify accredited status - higher standard than 506(b).
        Safe harbor verification methods: review IRS forms, W-2s, bank/brokerage statements, CPA/attorney letters.
        Third-party verification services acceptable if reasonable basis to rely.
        Form D filing required like 506(b).
        No integration concerns with 506(b) offerings per 2016 amendments.
        """,
        key_factors=[
            "General solicitation permitted",
            "All purchasers verified accredited",
            "Reasonable verification steps documented",
            "Safe harbor method or equivalent used",
            "Form D filed timely",
            "No sales to non-accredited"
        ],
        primary_authority=[
            Authority("17 CFR 230.506(c)", 100, "Federal", 1),
            Authority("17 CFR 230.506(d)", 95, "Federal", 1),
            Authority("SEC Release 33-9415 (2013)", 90, "Federal", 2)
        ],
        burden_holder="Issuer must verify accredited status with reasonable steps",
        adversary_position="SEC examines verification procedures for reasonableness and documentation",
        counter_arguments=[
            "Third-party verification service provided reasonable assurance",
            "Multiple verification methods used for each investor",
            "Bank statements and tax returns reviewed within 90 days",
            "Attorney opinion obtained confirming accredited status"
        ],
        resolution_strategy="Use safe harbor verification methods; document all verification steps; maintain investor files for 5+ years",
        entity_scope="Issuers seeking to publicly advertise private placements",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear safe harbor with detailed verification guidance from SEC",
        controlling_precedent="SEC Release 33-9415 - adoption of Rule 506(c)",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.OFFERING_COMPLIANCE]
    ),
    DoctrineBlock(
        topic="Regulation A+ Mini-IPO Exemption",
        keywords=["regulation a", "reg a+", "tier 1", "tier 2", "mini-ipo", "testing the waters"],
        conclusion_template=[
            "Regulation A+ allows offerings up to $75M via Tier 1 or Tier 2 with SEC qualification.",
            "Tier 2 offerings preempt state registration but require audited financials and ongoing reports.",
            "Testing-the-waters permitted before filing to gauge investor interest."
        ],
        reasoning_framework="""
        Regulation A exemption under Section 3(b) for offerings up to $75M in 12 months.
        Tier 1: up to $20M, state registration required, less disclosure.
        Tier 2: $20M to $75M, state preemption, audited financials, ongoing reports on Form 1-K/1-SA.
        Offering circular filed on Form 1-A reviewed by SEC but qualified not registered.
        Testing-the-waters solicitation permitted before and after filing.
        Investment limits for non-accredited in Tier 2: greater of 10% income or net worth.
        Resale restrictions: none for Tier 2 if listed or quoted; 12-month holding for Tier 1.
        Bad actor disqualification under Rule 262 similar to Reg D.
        Exit report on Form 1-Z required post-offering.
        """,
        key_factors=[
            "Offering amount within tier limits",
            "Form 1-A qualified by SEC",
            "Audited financials for Tier 2",
            "Ongoing reporting compliance",
            "Investment limits observed for non-accredited",
            "No bad actor disqualifications"
        ],
        primary_authority=[
            Authority("17 CFR 230.251-263", 100, "Federal", 1),
            Authority("SEC Release 33-9741 (2015)", 95, "Federal", 2),
            Authority("15 USC Section 77c(b)", 90, "Federal", 1)
        ],
        burden_holder="Issuer must ensure offering circular accuracy and ongoing compliance",
        adversary_position="SEC reviews disclosure quality and financial statement accuracy during qualification process",
        counter_arguments=[
            "Offering circular contained all material information",
            "Audited financials prepared by PCAOB-registered firm",
            "Ongoing reports filed timely on EDGAR",
            "Investment limits verified for each non-accredited investor"
        ],
        resolution_strategy="Engage securities counsel early; prepare detailed offering circular; retain qualified auditor; implement reporting compliance system",
        entity_scope="Small to mid-size companies seeking public capital under $75M",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Enhanced exemption with clear SEC guidance post-JOBS Act amendments",
        controlling_precedent="SEC Release 33-9741 - final Regulation A+ rules",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.OFFERING_COMPLIANCE, IssueCategory.DISCLOSURE]
    ),
    DoctrineBlock(
        topic="Regulation Crowdfunding Exemption",
        keywords=["regulation cf", "reg cf", "crowdfunding", "funding portal", "broker-dealer", "$5 million"],
        conclusion_template=[
            "Regulation CF permits offerings up to $5M via registered broker-dealer or funding portal.",
            "Investment limits based on investor income/net worth; issuer must provide financial statements.",
            "Ongoing reporting required on Form C-U annually until exemption or registration."
        ],
        reasoning_framework="""
        JOBS Act Title III directed SEC to create crowdfunding exemption.
        Regulation CF adopted under Section 4(a)(6) - effective May 2016.
        Offering limit increased to $5M per 12-month period (2021 amendment).
        Must be conducted through SEC-registered intermediary - broker-dealer or funding portal.
        Investment limits: if income/net worth under $124K, greater of $2,500 or 5% of lesser amount; if over $124K, 10% of lesser of income or net worth up to $124K cap.
        Financial statements required: under $124K - tax returns; $124K-$618K - reviewed; over $618K - audited.
        Form C filed with SEC and provided to investors via intermediary platform.
        12-month resale restriction - securities are restricted.
        Annual reporting on Form C-U until company registers, files Exchange Act reports, or ceases to be public.
        """,
        key_factors=[
            "Offering conducted through registered intermediary",
            "Offering amount under $5M annually",
            "Investment limits enforced by intermediary",
            "Appropriate financial statements provided",
            "Form C and C-U filed timely",
            "12-month resale restrictions applied"
        ],
        primary_authority=[
            Authority("17 CFR 227.100-503", 100, "Federal", 1),
            Authority("15 USC Section 77d(a)(6)", 95, "Federal", 1),
            Authority("SEC Release 33-10883 (2021)", 90, "Federal", 2)
        ],
        burden_holder="Issuer and intermediary share compliance responsibilities",
        adversary_position="SEC and FINRA examine intermediary compliance and investment limit enforcement",
        counter_arguments=[
            "Funding portal registered with SEC and FINRA member",
            "Platform enforced investment limits via investor questionnaires",
            "Financial statements prepared by independent CPA",
            "Form C-U filed within 120 days of fiscal year-end"
        ],
        resolution_strategy="Select reputable registered intermediary; prepare clear offering materials; obtain appropriate financial statements; implement annual reporting calendar",
        entity_scope="Startups and small businesses raising up to $5M from the crowd",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Complex exemption with joint issuer-intermediary obligations",
        controlling_precedent="SEC Release 33-10883 - amendments increasing offering and investment limits",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.OFFERING_COMPLIANCE, IssueCategory.DISCLOSURE]
    ),
    DoctrineBlock(
        topic="Rule 144 Resale of Restricted Securities",
        keywords=["rule 144", "restricted securities", "holding period", "volume limitations", "current information"],
        conclusion_template=[
            "Rule 144 permits resale of restricted securities after holding period with volume and manner limits.",
            "Non-affiliates: 6-month hold for reporting companies, 12-month for non-reporting, then unrestricted.",
            "Affiliates: always subject to volume, manner, and current information requirements."
        ],
        reasoning_framework="""
        Rule 144 safe harbor for resales under Section 4(a)(1) - not issuer, not underwriter, not dealer.
        Restricted securities acquired in unregistered transaction (Reg D, Reg S, etc).
        Holding period: 6 months for reporting company, 12 months for non-reporting (2008 amendments).
        Non-affiliates can resell freely after holding period if reporting company; must also satisfy current information for non-reporting.
        Affiliates always subject to conditions: holding period, current information, volume limitations, manner of sale, Form 144 notice.
        Volume limit: greater of 1% outstanding shares or 4-week average trading volume.
        Manner of sale: brokers transaction or market maker transaction - no solicitation.
        Current information: reporting company must be current in Exchange Act reports.
        Form 144 filed concurrently with sale if over 5,000 shares or $50K.
        Tacking allowed for securities received in corporate reorganization or estate.
        """,
        key_factors=[
            "Holding period satisfied",
            "Affiliate vs non-affiliate status",
            "Current information available",
            "Volume limitations calculated",
            "Manner of sale requirements",
            "Form 144 filing if required"
        ],
        primary_authority=[
            Authority("17 CFR 230.144", 100, "Federal", 1),
            Authority("SEC Release 33-8869 (2007)", 95, "Federal", 2),
            Authority("SEC v. Chinese Consolidated Benevolent Assn, 120 F.2d 738 (2d Cir. 1941)", 85, "Federal", 1)
        ],
        burden_holder="Seller must establish compliance with Rule 144 conditions",
        adversary_position="SEC challenges affiliate status determination and volume calculations",
        counter_arguments=[
            "Non-affiliate status established - no control or 10% ownership",
            "Holding period satisfied with tacking from predecessor",
            "Company current in all Exchange Act reports",
            "Volume limit calculated using 4-week ADTV from primary market"
        ],
        resolution_strategy="Obtain legal opinion on affiliate status; document holding period with purchase records; verify current information status; work with broker on volume limits",
        entity_scope="Holders of restricted securities and affiliates of issuers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Detailed safe harbor with extensive SEC interpretive guidance",
        controlling_precedent="SEC Release 33-8869 - 2007 amendments shortening holding periods",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.OFFERING_COMPLIANCE]
    ),
    DoctrineBlock(
        topic="Exchange Act Section 10(b) and Rule 10b-5 Antifraud",
        keywords=["10b-5", "section 10(b)", "fraud", "material misstatement", "scienter", "reliance", "damages"],
        conclusion_template=[
            "Section 10(b) and Rule 10b-5 prohibit material misstatements and omissions in connection with securities transactions.",
            "Private right of action requires: materiality, scienter, reliance, causation, damages.",
            "Higher pleading standard under PSLRA - particularity for fraud, strong inference for scienter."
        ],
        reasoning_framework="""
        Section 10(b) grants SEC authority to prohibit manipulative and deceptive devices.
        Rule 10b-5 implements Section 10(b) with three subsections: (a) scheme to defraud, (b) material misstatement or omission, (c) fraudulent act.
        Implied private right of action recognized in Superintendent of Insurance v. Bankers Life (1971).
        Elements: (1) material misstatement or omission, (2) scienter, (3) in connection with purchase or sale, (4) reliance/transaction causation, (5) loss causation, (6) damages.
        Materiality: substantial likelihood reasonable investor would consider important - TSC Industries.
        Scienter: intent to deceive, manipulate, or defraud - Ernst & Ernst v. Hochfelder.
        Reliance: fraud on the market theory allows presumption if efficient market - Basic Inc. v. Levinson.
        PSLRA heightened pleading: particularity under FRCP 9(b), strong inference of scienter.
        Loss causation: economic loss proximately caused by fraud - Dura Pharmaceuticals.
        Statute of limitations: 2 years from discovery, 5 years from violation.
        """,
        key_factors=[
            "Material misstatement or omission",
            "Scienter - intentional or reckless",
            "Connection with securities transaction",
            "Plaintiff reliance on misstatement",
            "Loss causation established",
            "Damages calculable"
        ],
        primary_authority=[
            Authority("15 USC Section 78j(b)", 100, "Federal", 1),
            Authority("17 CFR 240.10b-5", 100, "Federal", 1),
            Authority("Basic Inc. v. Levinson, 485 US 224 (1988)", 95, "Federal", 1),
            Authority("Dura Pharmaceuticals v. Broudo, 544 US 336 (2005)", 95, "Federal", 1)
        ],
        burden_holder="Plaintiff bears burden on all elements; defendant rebuts scienter inference",
        adversary_position="Plaintiffs plead fraud on the market and seek class certification; SEC brings parallel enforcement",
        counter_arguments=[
            "Statement not material - no substantial likelihood of investor consideration",
            "Forward-looking statement protected by PSLRA safe harbor",
            "No scienter - statement made with reasonable basis and good faith",
            "Truth-on-the-market defense - corrective disclosure already public",
            "Loss causation broken by intervening events"
        ],
        resolution_strategy="Move to dismiss under PSLRA pleading standards; challenge materiality and scienter; rebut loss causation; assert affirmative defenses",
        entity_scope="All securities transactions in US markets",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Supreme Court precedent with detailed circuit court development",
        controlling_precedent="Basic Inc. v. Levinson - fraud on the market; Dura Pharmaceuticals - loss causation requirement",
        issue_categories=[IssueCategory.FRAUD, IssueCategory.DISCLOSURE]
    ),
    DoctrineBlock(
        topic="Section 16(b) Short-Swing Profit Recovery",
        keywords=["section 16", "16(b)", "insider", "short-swing", "six months", "strict liability"],
        conclusion_template=[
            "Section 16(b) requires disgorgement of profits from matching purchases and sales within 6 months.",
            "Applies to officers, directors, and 10% shareholders - strict liability, no scienter required.",
            "Calculated using lowest-in highest-out matching; Form 4 reporting violations don't affect liability."
        ],
        reasoning_framework="""
        Exchange Act Section 16(b) prevents insiders from profiting on short-term trading.
        Strict liability - no intent, knowledge, or use of inside information required.
        Covered persons: officers (policy-making function per Rule 16a-1(f)), directors, 10% beneficial owners.
        10% status at time of both purchase and sale required (Foremost-McKesson exception).
        Purchase and sale within any 6-month period trigger disgorgement.
        Profits calculated using lowest-in highest-out matching to maximize recovery.
        Issuer or shareholders can sue to recover profits; attorneys fees awarded to successful plaintiff.
        Exemptions: Rule 16b-3 for issuer equity compensation plans with committee approval.
        Derivative securities under Rule 16a-1(c) - options, warrants, convertibles.
        Form 4 due within 2 business days of transaction; Form 5 for delayed reporting.
        """,
        key_factors=[
            "Officer, director, or 10% owner status",
            "Purchase and sale within 6-month window",
            "Profit calculable using matching",
            "Issuer or shareholder standing to sue",
            "Available exemptions applicable",
            "Form 4/5 reporting compliance"
        ],
        primary_authority=[
            Authority("15 USC Section 78p(b)", 100, "Federal", 1),
            Authority("17 CFR 240.16b-3", 90, "Federal", 2),
            Authority("Foremost-McKesson v. Provident Securities, 423 US 232 (1976)", 95, "Federal", 1)
        ],
        burden_holder="Plaintiff must show matching purchase and sale within 6 months by covered person",
        adversary_position="Shareholder plaintiffs seek disgorgement plus attorneys fees",
        counter_arguments=[
            "10% ownership not held at both purchase and sale times",
            "Transaction exempt under Rule 16b-3 board approval",
            "Derivative security conversion exempt under Rule 16b-6",
            "Unorthodox transaction not within Section 16(b) purpose"
        ],
        resolution_strategy="Structure transactions to avoid 6-month windows; obtain board committee approval for equity compensation; consider voluntary disgorgement to moot litigation",
        entity_scope="Reporting company insiders - officers, directors, 10% owners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strict liability statute with objective application and bright-line rules",
        controlling_precedent="Foremost-McKesson - 10% owner must hold at both ends of transaction",
        issue_categories=[IssueCategory.INSIDER_TRADING, IssueCategory.PUBLIC_COMPANY]
    ),
    DoctrineBlock(
        topic="Section 13(d) Beneficial Ownership Reporting",
        keywords=["13d", "5 percent", "beneficial ownership", "schedule 13d", "schedule 13g", "tender offer"],
        conclusion_template=[
            "Section 13(d) requires Schedule 13D filing within 10 days of acquiring 5% beneficial ownership.",
            "Beneficial ownership includes voting or investment power - direct or indirect control.",
            "Schedule 13G short form available for passive investors; amendments required for material changes."
        ],
        reasoning_framework="""
        Exchange Act Section 13(d) requires disclosure of significant equity stakes.
        5% beneficial ownership threshold triggers reporting - calculated per Rule 13d-3.
        Beneficial ownership: voting or investment power directly or indirectly through contract, arrangement, understanding.
        Schedule 13D long form for activist or control investors - 10 calendar days from crossing 5%.
        Schedule 13G short form for passive institutional investors - qualified institutional investors, passive investors under 20%.
        Amendment requirements: Schedule 13D/A for material changes; Schedule 13G/A annually and promptly for 5%+ change.
        Group formation under Section 13(d)(3): agreement to act together creates group with aggregated holdings.
        Rule 13d-1(b)(1): 10-day filing period for Schedule 13D.
        Rule 13d-1(c): standstill during 10-day period - no additional purchases.
        Voting trust, proxy, or other arrangement can trigger beneficial ownership.
        Derivatives can create beneficial ownership if economically equivalent to direct ownership.
        """,
        key_factors=[
            "Beneficial ownership reaches 5%",
            "Direct or indirect voting/investment power",
            "Group formation with aggregation",
            "10-day filing deadline met",
            "Standstill during reporting period",
            "Material changes triggering amendments"
        ],
        primary_authority=[
            Authority("15 USC Section 78m(d)", 100, "Federal", 1),
            Authority("17 CFR 240.13d-1", 95, "Federal", 1),
            Authority("17 CFR 240.13d-3", 95, "Federal", 1),
            Authority("CSX Corp. v. Children's Investment Fund, 562 F.3d 1072 (2d Cir. 2009)", 90, "Federal", 2)
        ],
        burden_holder="Acquiror must timely file and accurately disclose beneficial ownership",
        adversary_position="SEC and target company scrutinize group formation and derivative positions",
        counter_arguments=[
            "No group - discussions preliminary without agreement to act in concert",
            "Cash-settled derivatives not beneficial ownership - no voting rights",
            "Passive investment intent - Schedule 13G appropriate",
            "Amendment not required - change not material"
        ],
        resolution_strategy="Monitor ownership daily; file promptly upon crossing 5%; avoid group discussions pre-filing; consider Hart-Scott-Rodino implications",
        entity_scope="Investors in reporting companies acquiring 5%+ stakes",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Complex factual determinations around indirect ownership and group formation",
        controlling_precedent="CSX Corp. v. Children's Investment Fund - cash-settled derivatives can create beneficial ownership",
        issue_categories=[IssueCategory.BENEFICIAL_OWNERSHIP, IssueCategory.PUBLIC_COMPANY]
    ),
    DoctrineBlock(
        topic="Sarbanes-Oxley Section 302 CEO/CFO Certifications",
        keywords=["sox 302", "certification", "internal controls", "disclosure controls", "ceo", "cfo"],
        conclusion_template=[
            "SOX Section 302 requires CEO and CFO to certify accuracy of financial statements and effectiveness of controls.",
            "Personal certification creates individual liability for false statements.",
            "Certification covers review, accuracy, fair presentation, disclosure controls, and material changes."
        ],
        reasoning_framework="""
        Sarbanes-Oxley Section 302 enacted after Enron/WorldCom to ensure executive accountability.
        CEO and CFO must personally certify each Form 10-Q and 10-K.
        Certification statements: (1) reviewed report, (2) no untrue statements or omissions, (3) financial statements fairly present, (4) responsible for establishing and maintaining disclosure controls, (5) evaluated effectiveness of disclosure controls, (6) disclosed control deficiencies to auditors and audit committee, (7) disclosed material changes in internal control.
        Disclosure controls and procedures: designed to ensure material information timely flows to certifying officers.
        Internal control over financial reporting: process to provide reasonable assurance on reliability of financial reporting.
        Certification liability: Section 906 criminal penalties for knowing/willful false certification (up to $5M fine, 20 years prison).
        Civil liability: Section 302 certifications can support securities fraud claims - evidence of scienter.
        Officers cannot delegate certification responsibility - personal duty.
        Sub-certifications from business unit leaders recommended but don't eliminate CEO/CFO responsibility.
        """,
        key_factors=[
            "CEO and CFO personally sign certifications",
            "Financial statements reviewed before certification",
            "Disclosure controls evaluated within 90 days",
            "Material control deficiencies disclosed",
            "Changes in internal controls reported",
            "No material misstatements in certified reports"
        ],
        primary_authority=[
            Authority("15 USC Section 7241", 100, "Federal", 1),
            Authority("18 USC Section 1350", 95, "Federal", 1),
            Authority("17 CFR 229.601(b)(31)", 90, "Federal", 2)
        ],
        burden_holder="CEO and CFO bear personal responsibility for certification accuracy",
        adversary_position="SEC and DOJ pursue certification violations as evidence of securities fraud",
        counter_arguments=[
            "Reasonable reliance on sub-certifications from business units",
            "Disclosure controls adequate - error not material",
            "No scienter - mistake in good faith",
            "Internal investigation conducted and disclosed"
        ],
        resolution_strategy="Implement robust sub-certification process; conduct quarterly disclosure committee meetings; document control evaluations; consider D&O insurance enhancement",
        entity_scope="CEOs and CFOs of all SEC reporting companies",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear statutory requirements with bright-line certification obligations",
        controlling_precedent="15 USC 7241 - statutory certification requirements",
        issue_categories=[IssueCategory.PUBLIC_COMPANY, IssueCategory.DISCLOSURE]
    ),
    DoctrineBlock(
        topic="Sarbanes-Oxley Section 404 Internal Control Audits",
        keywords=["sox 404", "internal controls", "pcaob", "auditor attestation", "material weakness", "icfr"],
        conclusion_template=[
            "SOX Section 404 requires management assessment and auditor attestation of internal control over financial reporting.",
            "Material weaknesses must be disclosed and remediated to maintain effective ICFR.",
            "Smaller reporting companies exempt from auditor attestation requirement."
        ],
        reasoning_framework="""
        Section 404(a): management must assess and report on internal control over financial reporting (ICFR).
        Section 404(b): auditor must attest to and report on management's assessment.
        ICFR: process to provide reasonable assurance on reliability of financial reporting and preparation of statements per GAAP.
        COSO framework widely used for ICFR design and evaluation.
        Material weakness: deficiency or combination such that reasonable possibility of material misstatement not prevented or detected.
        Significant deficiency: important enough to merit audit committee attention but less severe than material weakness.
        Management report in Item 9A of Form 10-K must conclude effective or not effective.
        Auditor attestation under AS 2201 (PCAOB standard) - integrated audit of financials and ICFR.
        Accelerated filers and large accelerated filers subject to 404(b) auditor attestation.
        Non-accelerated filers and smaller reporting companies permanently exempt from 404(b).
        Remediation plan required for disclosed material weaknesses.
        Restatements often trigger material weakness disclosures.
        """,
        key_factors=[
            "ICFR framework designed and documented",
            "Annual management assessment conducted",
            "Testing of key controls completed",
            "Material weaknesses identified and disclosed",
            "Auditor attestation obtained if required",
            "Remediation plans implemented"
        ],
        primary_authority=[
            Authority("15 USC Section 7262", 100, "Federal", 1),
            Authority("17 CFR 229.308", 95, "Federal", 1),
            Authority("PCAOB AS 2201", 90, "Federal", 2)
        ],
        burden_holder="Management responsible for designing, implementing, and assessing ICFR effectiveness",
        adversary_position="Auditors issue adverse opinions if material weaknesses exist; SEC examines remediation efforts",
        counter_arguments=[
            "Deficiency was significant but not material weakness",
            "Compensating controls mitigated risk to reasonable level",
            "Remediation completed before year-end - effective as of report date",
            "Smaller reporting company exemption applies"
        ],
        resolution_strategy="Engage experienced ICFR consultants; conduct quarterly control testing; maintain detailed documentation; remediate deficiencies promptly; consider SRC status election",
        entity_scope="Accelerated and large accelerated SEC filers; all filers for 404(a)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Complex compliance area with PCAOB audit standards and SEC interpretive guidance",
        controlling_precedent="PCAOB AS 2201 - auditing internal control over financial reporting",
        issue_categories=[IssueCategory.PUBLIC_COMPANY, IssueCategory.DISCLOSURE]
    ),
    DoctrineBlock(
        topic="Dodd-Frank Section 922 Whistleblower Protections and Bounties",
        keywords=["dodd-frank", "whistleblower", "section 922", "bounty", "anti-retaliation", "10 to 30 percent"],
        conclusion_template=[
            "Dodd-Frank Section 922 provides bounties of 10-30% of monetary sanctions for whistleblowers providing original information.",
            "Anti-retaliation provisions protect whistleblowers from discharge, demotion, or discrimination.",
            "Whistleblower can report directly to SEC without internal reporting requirement."
        ],
        reasoning_framework="""
        Dodd-Frank Act Section 922 added Exchange Act Section 21F creating SEC whistleblower program.
        Whistleblower: individual who provides original information leading to successful enforcement over $1M.
        Award range: 10% to 30% of monetary sanctions collected - SEC discretion within range based on factors.
        Original information: derived from independent knowledge or analysis, not already known to SEC.
        Voluntary provision - not compelled by law, regulation, or agreement.
        SEC receives tips via online portal; identity kept confidential subject to legal exceptions.
        No internal reporting requirement - can report directly to SEC, though internal reporting may increase award.
        Anti-retaliation: employer cannot discharge, demote, suspend, threaten, harass, or discriminate.
        Private right of action for retaliation: reinstatement, double back pay, attorneys fees and costs.
        Statute of limitations: 6 years for retaliation claim (extended from 2-3 years in 2020 amendments).
        Attorney-client privilege protections: reporting privileged communications may forfeit award eligibility.
        Over $1.5B awarded to whistleblowers since program inception 2011.
        """,
        key_factors=[
            "Original information provided to SEC",
            "Information leads to successful enforcement over $1M",
            "Voluntary reporting not legally compelled",
            "No attorney-client privilege violations",
            "Anti-retaliation protections apply",
            "Award determination within 10-30% range"
        ],
        primary_authority=[
            Authority("15 USC Section 78u-6", 100, "Federal", 1),
            Authority("17 CFR 240.21F-1 to 21F-17", 95, "Federal", 1),
            Authority("Berman v. Neo@Ogilvy LLC, 801 F.3d 145 (2d Cir. 2015)", 85, "Federal", 2)
        ],
        burden_holder="Whistleblower must demonstrate original information led to successful enforcement",
        adversary_position="Employers defend retaliation claims; SEC evaluates award amount within statutory range",
        counter_arguments=[
            "Information not original - already known to SEC from other sources",
            "Reporting compelled by legal or contractual obligation",
            "Disclosed attorney-client privileged communications - ineligible for award",
            "Adverse employment action for legitimate business reasons unrelated to whistleblowing"
        ],
        resolution_strategy="Report via SEC online portal; retain experienced whistleblower counsel; document retaliation if occurs; file retaliation claim within 6 years",
        entity_scope="Individuals with knowledge of securities law violations; employers of potential whistleblowers",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Evolving area with increasing awards and expanding interpretations of protected activity",
        controlling_precedent="Berman v. Neo@Ogilvy - anti-retaliation protections apply even if report to SEC not qualifying",
        issue_categories=[IssueCategory.WHISTLEBLOWER, IssueCategory.PUBLIC_COMPANY]
    ),
    DoctrineBlock(
        topic="Broker-Dealer Registration and Finder Exemptions",
        keywords=["broker-dealer", "registration", "section 15", "finder", "transaction-based compensation"],
        conclusion_template=[
            "Section 15(a) requires broker-dealer registration for persons effecting securities transactions for others.",
            "Transaction-based compensation is hallmark of broker activity triggering registration.",
            "Finders claiming exemption bear high burden - limited to ministerial introductions without negotiation."
        ],
        reasoning_framework="""
        Exchange Act Section 15(a)(1) prohibits broker-dealer activity without SEC registration.
        Broker: person engaged in business of effecting securities transactions for account of others.
        Dealer: person engaged in business of buying/selling securities for own account.
        Registration requires Form BD filing, FINRA membership, compliance with FINRA rules, state notice filings.
        Transaction-based compensation strongly indicates broker status - commissions, success fees, carried interest.
        Finder exception: narrow, ill-defined, high-risk - limited to passive introductions.
        SEC Staff position (1999 Brumberg No-Action Letter withdrawn): finders must not negotiate terms, receive documents only for introduction, provide lists not specific recommendations.
        Active solicitation, participation in negotiations, due diligence involvement push toward broker status.
        Consequences of unregistered broker activity: rescission rights for investors, disgorgement of compensation, SEC enforcement.
        Safe harbor: issuer officers/employees with limited compensation (Rule 3a4-1) for own company only.
        M&A brokers: conditional exemption under Section 15(b)(12) for certain M&A transactions (2016 amendment).
        """,
        key_factors=[
            "Transaction-based compensation received",
            "Regular participation in securities transactions",
            "Solicitation of investors or purchasers",
            "Negotiation of terms or price",
            "Handling of securities or funds",
            "Holding out as securities professional"
        ],
        primary_authority=[
            Authority("15 USC Section 78o(a)", 100, "Federal", 1),
            Authority("SEC v. Hansen, 1984 WL 2413 (SD NY 1984)", 85, "Federal", 2),
            Authority("SEC Release 34-87017 (2019)", 80, "Federal", 2)
        ],
        burden_holder="Person claiming finder exemption bears burden to demonstrate limited ministerial role",
        adversary_position="SEC broadly interprets broker definition to protect investors; FINRA examines unregistered activity",
        counter_arguments=[
            "Purely ministerial introduction without involvement in negotiations",
            "Compensation not transaction-based but flat fee for consulting",
            "Officer of issuer conducting offering for own company under Rule 3a4-1",
            "M&A broker exemption applies to business combination transaction"
        ],
        resolution_strategy="Register as broker-dealer if regular activity; structure compensation as non-transaction-based; limit role to passive introductions; engage registered broker for placement agent services",
        entity_scope="Finders, intermediaries, placement agents, M&A advisors in securities transactions",
        confidence=ConfidenceLevel.HIGH_RISK,
        confidence_stratification="Finder exemption poorly defined with significant enforcement risk for transaction-based compensation",
        controlling_precedent="SEC v. Hansen - transaction-based compensation is hallmark of broker activity",
        issue_categories=[IssueCategory.BROKER_DEALER, IssueCategory.REGISTRATION]
    ),
    DoctrineBlock(
        topic="Integration of Securities Offerings",
        keywords=["integration", "general solicitation", "separate offerings", "safe harbor", "regulation d"],
        conclusion_template=[
            "Integration doctrine treats ostensibly separate offerings as single offering if factually related.",
            "Safe harbors: 6-month gap, different exemptions (Reg D/Reg A+), no general solicitation in prior offering.",
            "2016 amendments eliminated integration between concurrent Reg D and other offerings."
        ],
        reasoning_framework="""
        Integration prevents issuers from circumventing registration by artificially splitting single offering.
        Five-factor test (Release 33-4552): (1) same class of securities, (2) same time, (3) same type of consideration, (4) same general purpose, (5) same purchasers.
        Safe harbors in Regulation D Rule 502(a): 6-month gap before/after Reg D offering; different exemption if no general solicitation in first offering.
        2016 amendments (Release 33-10238): no integration between Reg D and other offerings, between different Reg D offerings, or different Rule 701 offerings.
        Rule 152 safe harbor: offering 6+ months after registered offering won't integrate.
        General solicitation in Section 4(a)(2) offering followed by Reg D 506(b) risks integration - prior solicitation taints later offering.
        Offering period: begins with first offer, ends when distribution complete - not limited to formal closing.
        Single plan of financing indicator: business plan showing phased capital raising can evidence single integrated offering.
        """,
        key_factors=[
            "Time gap between offerings",
            "Same or different classes of securities",
            "Different exemptions relied upon",
            "General solicitation in prior offering",
            "Overlap in purchaser groups",
            "Single plan of financing documented"
        ],
        primary_authority=[
            Authority("17 CFR 230.502(a)", 100, "Federal", 1),
            Authority("17 CFR 230.152", 90, "Federal", 2),
            Authority("SEC Release 33-10238 (2016)", 95, "Federal", 2)
        ],
        burden_holder="Issuer must establish separate offerings not integrated",
        adversary_position="SEC examines totality of circumstances to find integration where exemptions evaded",
        counter_arguments=[
            "6-month safe harbor gap between offerings satisfied",
            "Different securities classes - debt vs equity",
            "No overlap in investor groups between offerings",
            "Reg D 506(c) used - integration rules liberalized in 2016 amendments"
        ],
        resolution_strategy="Observe 6-month gaps; avoid general solicitation if relying on 506(b); document separate business purposes; rely on 2016 safe harbors for concurrent offerings",
        entity_scope="Issuers conducting multiple capital raises within short time periods",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Fact-intensive analysis with liberalized rules post-2016 but residual enforcement risk",
        controlling_precedent="SEC Release 33-10238 - elimination of integration for concurrent Reg D offerings",
        issue_categories=[IssueCategory.OFFERING_COMPLIANCE, IssueCategory.EXEMPTIONS]
    ),
    DoctrineBlock(
        topic="Accredited Investor Definition and Verification",
        keywords=["accredited investor", "rule 501", "income test", "net worth test", "verification", "reasonable steps"],
        conclusion_template=[
            "Accredited investor status based on income ($200K/$300K), net worth ($1M excluding residence), or professional criteria.",
            "2020 amendments added professional certifications and knowledgeable employee categories.",
            "Verification requirements depend on exemption: reasonable belief for 506(b), reasonable steps for 506(c)."
        ],
        reasoning_framework="""
        Rule 501(a) defines accredited investor with multiple categories.
        Natural persons: (1) income over $200K individual or $300K joint for each of last 2 years with reasonable expectation of same level current year, OR (2) net worth over $1M individually or jointly excluding primary residence, OR (3) holding Series 7/65/82 or other qualifying professional certifications.
        Net worth calculation: assets minus liabilities; primary residence excluded per Dodd-Frank; investment in issuer not counted toward net worth.
        Entities: $5M in assets for entities; all equity owners accredited for LLCs/partnerships; registered investment advisers; rural business investment companies; family offices with $5M+ AUM and sophisticated purchaser.
        Knowledgeable employees of private funds: executive officers, directors, trustees, general partners, advisory board members, employees with investment function who participate in investment activities.
        2020 amendments (Release 33-10824): added Series 7/65/82 holders; knowledgeable employees; family offices; spousal equivalents for joint net worth.
        Verification for 506(b): reasonable belief - can rely on investor representation if no reason to question.
        Verification for 506(c): reasonable steps to verify - safe harbors include review of tax returns, W-2s, bank statements, credit reports, CPA/attorney letters, use of registered broker-dealer or SEC-registered investment adviser.
        """,
        key_factors=[
            "Income or net worth thresholds met",
            "Professional certifications held",
            "Entity asset levels or ownership structure",
            "Verification method appropriate for exemption",
            "Documentation retained for SEC examination",
            "Spousal equivalent included in joint calculations"
        ],
        primary_authority=[
            Authority("17 CFR 230.501(a)", 100, "Federal", 1),
            Authority("17 CFR 230.506(c)", 95, "Federal", 1),
            Authority("SEC Release 33-10824 (2020)", 95, "Federal", 2)
        ],
        burden_holder="Issuer must establish investor accredited status with appropriate verification",
        adversary_position="SEC examines verification procedures for reasonableness and documentation",
        counter_arguments=[
            "Investor provided Series 65 certification - accredited per 2020 amendments",
            "Third-party RIA verified accredited status using safe harbor methods",
            "Reasonable belief standard for 506(b) - investor representation adequate",
            "Joint net worth with spousal equivalent exceeds $1M excluding residence"
        ],
        resolution_strategy="Use safe harbor verification methods for 506(c); obtain professional certifications or third-party verification letters; document verification procedures; update investor questionnaires for 2020 amendments",
        entity_scope="Issuers relying on Reg D and investors claiming accredited status",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear definitional criteria with safe harbor verification methods",
        controlling_precedent="SEC Release 33-10824 - 2020 amendments expanding accredited investor definition",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.OFFERING_COMPLIANCE]
    ),
    DoctrineBlock(
        topic="Form 10-K Annual Report and MD&A Disclosure",
        keywords=["form 10-k", "annual report", "md&a", "management discussion", "known trends", "liquidity"],
        conclusion_template=[
            "Form 10-K annual report filed within 60-90 days of fiscal year-end depending on filer status.",
            "MD&A requires disclosure of known trends, demands, commitments, events, and uncertainties.",
            "Disclosure obligation triggered when management knows trend reasonably likely to have material effects."
        ],
        reasoning_framework="""
        Exchange Act Section 13(a) requires registered companies to file annual reports per SEC rules.
        Form 10-K due date: large accelerated filers 60 days, accelerated filers 75 days, non-accelerated 90 days.
        Part I: business description, risk factors, selected financial data, MD&A.
        Part II: audited financial statements, management certifications, auditor report.
        Item 303 MD&A: narrative explanation of financial statements enabling investors to see company through management's eyes.
        MD&A disclosure triggers: (1) management knows of trend, demand, commitment, event, or uncertainty, AND (2) management knows or reasonably likely to have material effects, THEN must disclose unless management reasonably determines not reasonably likely to occur.
        Known trends: economic conditions, regulatory changes, competitive developments.
        Liquidity and capital resources: contractual obligations table, off-balance sheet arrangements, working capital needs.
        Critical accounting estimates: assumptions and judgments with significant impact on financial statements.
        Forward-looking statement safe harbor applies to MD&A with meaningful cautionary language.
        Accelerated filer status: $75M public float for large accelerated, $75M-$700M for accelerated.
        """,
        key_factors=[
            "Timely filing within filer category deadline",
            "Known trends disclosed if reasonably likely material",
            "Liquidity analysis includes contractual obligations",
            "Critical accounting policies identified and explained",
            "SOX 302 CEO/CFO certifications included",
            "Audited financials per PCAOB standards"
        ],
        primary_authority=[
            Authority("17 CFR 249.310", 100, "Federal", 1),
            Authority("17 CFR 229.303", 100, "Federal", 1),
            Authority("SEC Release 33-8350 (2003)", 95, "Federal", 2)
        ],
        burden_holder="Management responsible for full and fair MD&A disclosure of known material trends",
        adversary_position="SEC Division of Corporation Finance reviews MD&A for adequacy and issues comment letters",
        counter_arguments=[
            "Trend not reasonably likely to have material effect based on management determination",
            "Forward-looking information protected by PSLRA safe harbor with cautionary language",
            "Disclosure of trend would reveal confidential business information harming competitive position",
            "Subsequent event disclosure in next quarterly report adequate"
        ],
        resolution_strategy="Implement robust disclosure controls; conduct quarterly disclosure committee meetings; document MD&A determinations in writing; respond promptly to SEC comment letters",
        entity_scope="All SEC reporting companies filing Form 10-K",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core periodic reporting obligation with detailed Item 303 guidance",
        controlling_precedent="SEC Release 33-8350 - comprehensive MD&A interpretive guidance",
        issue_categories=[IssueCategory.DISCLOSURE, IssueCategory.PUBLIC_COMPANY]
    ),
    DoctrineBlock(
        topic="Regulation S Offshore Sales Exemption",
        keywords=["regulation s", "offshore", "category 1", "category 2", "directed selling efforts", "flowback"],
        conclusion_template=[
            "Regulation S exempts offshore sales to non-US persons with no directed selling efforts in US.",
            "Category 1 (non-reporting foreign issuers): no flowback restrictions or holding period.",
            "Category 2/3 (US issuers and reporting foreign): 6-month to 1-year restricted period and certification requirements."
        ],
        reasoning_framework="""
        Regulation S safe harbor under Section 4(a)(2) for offshore transactions outside US jurisdiction.
        Two conditions: (1) offer/sale in offshore transaction per Rule 903(a), (2) no directed selling efforts in US per Rule 902(c).
        Offshore transaction: buyer outside US or seller reasonably believes buyer outside US; offer not made to person in US.
        Directed selling efforts: activities undertaken for purpose of conditioning US market - prohibited during distribution compliance period.
        Category 1: foreign issuers with no substantial US market interest - no distribution compliance period.
        Category 2: US reporting companies - 6-month distribution compliance period, certification, no hedging.
        Category 3: US non-reporting or substantial US market interest - 1-year distribution compliance period, additional restrictions.
        Substantial US market interest: >10% trading volume in US or >300 US record holders.
        Distribution compliance period: securities restricted, legends required, transfer restrictions.
        Resale under Reg S: dealer 40-day waiting period for Category 1, 1-year for Category 2/3.
        Flowback prevention: legends stating securities not registered and may not be offered/sold in US except pursuant to registration or exemption.
        """,
        key_factors=[
            "Offshore transaction - buyer outside US",
            "No directed selling efforts in US market",
            "Appropriate category determined",
            "Distribution compliance period observed",
            "Certifications obtained from offshore buyers",
            "Restrictive legends applied to certificates"
        ],
        primary_authority=[
            Authority("17 CFR 230.901-905", 100, "Federal", 1),
            Authority("SEC Release 33-6863 (1990)", 95, "Federal", 2),
            Authority("SEC Release 33-7505 (1998)", 90, "Federal", 2)
        ],
        burden_holder="Issuer and distributors must ensure compliance with offshore and no US directed selling requirements",
        adversary_position="SEC scrutinizes flowback to US market and compliance with distribution compliance periods",
        counter_arguments=[
            "Buyer certified offshore status and non-US person representation",
            "No directed selling efforts - offering materials not distributed in US",
            "Category 1 classification appropriate - foreign issuer with no substantial US market interest",
            "Distribution compliance period expired before US resales"
        ],
        resolution_strategy="Obtain offshore buyer certifications; impose transfer restrictions during compliance period; use restrictive legends; avoid US marketing activities; consider combined Reg S / Reg D offerings with appropriate integration analysis",
        entity_scope="Issuers conducting offshore capital raises to non-US investors",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Complex exemption with flowback prevention requirements and category determinations",
        controlling_precedent="SEC Release 33-6863 - original adoption of Regulation S",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.OFFERING_COMPLIANCE]
    ),
    DoctrineBlock(
        topic="Regulation FD Selective Disclosure Prohibition",
        keywords=["regulation fd", "selective disclosure", "material nonpublic", "simultaneous disclosure", "8-k"],
        conclusion_template=[
            "Regulation FD prohibits selective disclosure of material nonpublic information to securities market professionals.",
            "Intentional disclosure requires simultaneous public disclosure via Form 8-K or other means.",
            "Non-intentional disclosure requires prompt public disclosure within 24 hours or next business day open."
        ],
        reasoning_framework="""
        Regulation FD (Fair Disclosure) adopted 2000 to prevent selective disclosure to analysts and institutional investors.
        Rule 100(a): when issuer or person acting on its behalf discloses material nonpublic information to enumerated persons, must make public disclosure.
        Enumerated persons: broker-dealers, investment advisers, investment companies, holders of issuer securities if reasonably foreseeable person will trade.
        Intentional disclosure: simultaneous public disclosure required.
        Non-intentional disclosure: prompt public disclosure - by later of 24 hours or commencement of next business day trading.
        Public disclosure methods: Form 8-K filing, press release via widely disseminated news service, conference call with advance public notice and webcast.
        Materiality: substantial likelihood reasonable investor would consider important in making investment decision - TSC Industries standard.
        Exclusions: disclosures to persons who owe duty of trust or confidence (attorneys, accountants, underwriters under confidentiality agreements); credit rating agencies; SEC.
        No private right of action - SEC enforcement only.
        Violations support insider trading cases as evidence of materiality and timing of information.
        """,
        key_factors=[
            "Material nonpublic information disclosed",
            "Disclosure to enumerated person",
            "Intentional vs non-intentional disclosure",
            "Simultaneous or prompt public disclosure made",
            "Method of public disclosure adequate",
            "Exclusions for confidential relationships"
        ],
        primary_authority=[
            Authority("17 CFR 243.100-103", 100, "Federal", 1),
            Authority("SEC Release 34-43154 (2000)", 95, "Federal", 2),
            Authority("SEC v. Siebel Systems, 384 F.Supp.2d 694 (SD NY 2005)", 85, "Federal", 2)
        ],
        burden_holder="Issuer responsible for ensuring material information publicly disclosed before or simultaneously with selective disclosure",
        adversary_position="SEC examines earnings guidance, analyst communications, and investor meeting practices",
        counter_arguments=[
            "Information not material - no substantial likelihood of investor importance",
            "Information already public via prior Form 8-K filing",
            "Disclosure to attorney under duty of confidentiality - exclusion applies",
            "Non-intentional disclosure followed by prompt 8-K within 24 hours"
        ],
        resolution_strategy="Train executives and IR staff on Reg FD; pre-clear analyst communications; webcast all earnings calls with advance notice; file Form 8-K for material disclosures; implement disclosure committee process",
        entity_scope="SEC reporting companies and their executives, IR personnel, and representatives",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear prohibition with defined exclusions and public disclosure methods",
        controlling_precedent="SEC Release 34-43154 - adoption of Regulation FD",
        issue_categories=[IssueCategory.DISCLOSURE, IssueCategory.PUBLIC_COMPANY, IssueCategory.INSIDER_TRADING]
    ),
    DoctrineBlock(
        topic="Investment Company Act Section 3(c)(1) and 3(c)(7) Exemptions",
        keywords=["investment company act", "3c1", "3c7", "100 investors", "qualified purchaser", "private fund"],
        conclusion_template=[
            "Section 3(c)(1) exempts funds with 100 or fewer beneficial owners not held out to public.",
            "Section 3(c)(7) exempts funds owned exclusively by qualified purchasers with no public offering.",
            "Both exemptions subject to integration and look-through rules for counting beneficial owners."
        ],
        reasoning_framework="""
        Investment Company Act Section 3(a)(1) defines investment company as issuer primarily engaged in investing/trading securities.
        Section 3(c)(1) exemption: beneficial owners limited to 100 persons; securities not publicly offered.
        Section 3(c)(7) exemption: owned exclusively by qualified purchasers; securities not publicly offered; created by National Securities Markets Improvement Act 1996.
        Qualified purchaser: individual with $5M+ investments; family company with $5M+ investments; trust with $5M+ investments if trustees are QPs; entity with $25M+ investments; investment manager with $25M+ AUM.
        Beneficial owner counting: look-through for knowledgeable employee trusts and certain family trusts; no look-through for corporations, partnerships, LLCs unless formed to evade 100-person limit.
        Integration: related funds may be integrated as single issuer for counting purposes if common control and investment strategy.
        Not held out to public: no general solicitation; pre-existing relationships; limited investor sophistication.
        Section 3(c)(5) exemption: 40% of assets in mortgages, real estate, or short-term paper.
        Section 3(c)(6) exemption: wholly-owned subsidiary of 3(c)(1) or 3(c)(7) fund.
        Consequences of loss of exemption: must register as investment company or liquidate/restructure.
        """,
        key_factors=[
            "Beneficial owners within 100-person limit for 3(c)(1)",
            "All owners are qualified purchasers for 3(c)(7)",
            "No public offering of fund interests",
            "Look-through rules applied correctly",
            "Integration with related funds assessed",
            "Investor eligibility verified before admission"
        ],
        primary_authority=[
            Authority("15 USC Section 80a-3(c)(1)", 100, "Federal", 1),
            Authority("15 USC Section 80a-3(c)(7)", 100, "Federal", 1),
            Authority("17 CFR 270.2a51-1 to 2a51-3", 95, "Federal", 2),
            Authority("Goldstein v. SEC, 451 F.3d 873 (DC Cir. 2006)", 85, "Federal", 2)
        ],
        burden_holder="Fund manager must ensure exemption requirements continuously satisfied",
        adversary_position="SEC examines beneficial owner counting, QP verification, and inadvertent public offerings",
        counter_arguments=[
            "Beneficial owners properly counted with look-through for eligible trusts",
            "All investors provided QP certifications and financial documentation",
            "No integration - funds have separate managers and investment strategies",
            "Fund interests offered only via pre-existing relationships without solicitation"
        ],
        resolution_strategy="Implement robust investor onboarding with eligibility verification; monitor beneficial owner count; restrict transfers to maintain exemption; conduct integration analysis for related funds; consider 3(c)(7) for larger/growing funds",
        entity_scope="Private investment funds including hedge funds, venture funds, private equity funds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established exemptions with detailed SEC guidance and no-action letters",
        controlling_precedent="Goldstein v. SEC - advisers to 3(c)(1)/3(c)(7) funds exempt from Advisers Act registration pre-Dodd-Frank",
        issue_categories=[IssueCategory.EXEMPTIONS, IssueCategory.REGISTRATION]
    ),
    DoctrineBlock(
        topic="Blue Sky State Securities Registration and Coordination",
        keywords=["blue sky", "state registration", "nsmia", "covered security", "coordination", "notice filing"],
        conclusion_template=[
            "State securities laws require registration or exemption for intrastate offerings not preempted by NSMIA.",
            "NSMIA Section 18 preempts state registration for covered securities including Reg D Rule 506 and exchange-listed.",
            "States retain antifraud authority and can require notice filings with fees."
        ],
        reasoning_framework="""
        Blue sky laws: state securities regulation dating to Kansas 1911.
        Uniform Securities Act model adopted by most states with variations.
        Registration by coordination: file in state simultaneously with SEC registration.
        Registration by qualification: merit review states examine investment quality.
        National Securities Markets Improvement Act 1996 (NSMIA) Section 18: preempts state registration for covered securities.
        Covered securities: listed on national exchange, issued by registered investment company, offered via Rule 506 or Section 4(a)(6), sold to qualified purchasers.
        State notice filing permitted: Form D and state fee required within 15 days of first sale even though registration preempted.
        Antifraud authority preserved: states can investigate and prosecute fraud even for covered securities.
        Intrastate exemption: Section 3(a)(11) and Rule 147/147A exempt purely intrastate offerings but states can still regulate.
        State bad actor provisions: some states impose additional disqualifications beyond federal rules.
        NASAA coordination: North American Securities Administrators Association coordinates state regulation.
        """,
        key_factors=[
            "Covered security status under NSMIA",
            "State registration or exemption identified",
            "Notice filing timely submitted with fees",
            "Intrastate offering requirements if applicable",
            "State antifraud compliance",
            "Bad actor disqualifications in applicable states"
        ],
        primary_authority=[
            Authority("15 USC Section 77r", 100, "Federal", 1),
            Authority("Uniform Securities Act Section 301-306", 85, "State", 2),
            Authority("Blue Sky Law Reporter (CCH)", 75, "State", 3)
        ],
        burden_holder="Issuer must comply with applicable state registration or notice filing requirements",
        adversary_position="State securities regulators examine fraud and can deny exemptions or require registration",
        counter_arguments=[
            "Rule 506 offering - state registration preempted as covered security",
            "Notice filing submitted with Form D and state fee within 15 days",
            "Exchange listing on NYSE - covered security under NSMIA",
            "Purely intrastate offering under Rule 147A - no interstate commerce"
        ],
        resolution_strategy="Determine covered security status; file state Form D notices promptly; engage state blue sky counsel for non-covered offerings; track state fee and filing deadlines; monitor state antifraud developments",
        entity_scope="Issuers offering securities to investors in multiple states",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal preemption clear for covered securities but state variations require counsel review",
        controlling_precedent="NSMIA Section 18 - federal preemption of state registration for covered securities",
        issue_categories=[IssueCategory.REGISTRATION, IssueCategory.OFFERING_COMPLIANCE]
    ),
    DoctrineBlock(
        topic="JOBS Act Emerging Growth Company Benefits",
        keywords=["jobs act", "egc", "emerging growth company", "scaled disclosure", "testing the waters", "auditor attestation"],
        conclusion_template=[
            "Emerging Growth Company status available until $1.235B revenue, $700M public float, or 5 years post-IPO.",
            "EGC benefits: scaled disclosure, exempt from SOX 404(b) auditor attestation, confidential SEC review, testing-the-waters.",
            "Can elect out of EGC benefits irrevocably at any time."
        ],
        reasoning_framework="""
        JOBS Act Title I enacted 2012 to ease IPO process for smaller companies.
        EGC definition: company with under $1.235B total annual revenues in most recent fiscal year (indexed for inflation).
        EGC status maintained until earliest of: (1) last day of fiscal year with $1.235B+ revenues, (2) last day of fiscal year 5 years after IPO, (3) issuance of $1B+ non-convertible debt in 3-year period, (4) $700M+ public float as of last business day of second fiscal quarter.
        Scaled disclosure: 2 years audited financials instead of 3; no CD&A compensation discussion; exempt from say-on-pay advisory votes; exempt from auditor attestation under SOX 404(b).
        Testing-the-waters: can gauge investor interest before or after IPO filing with qualified institutional buyers and institutional accredited investors.
        Confidential SEC review: can submit draft registration statement for non-public SEC review; public filing required 21 days before roadshow.
        Extended transition period: can elect to delay adoption of new accounting standards until applicable to private companies.
        Irrevocable opt-out: can elect to waive EGC benefits before or during IPO; election permanent and irrevocable.
        """,
        key_factors=[
            "Annual revenues under $1.235B threshold",
            "Within 5 years of IPO date",
            "Public float under $700M",
            "Non-convertible debt under $1B threshold",
            "Election to use EGC benefits or opt out",
            "Compliance with scaled disclosure requirements"
        ],
        primary_authority=[
            Authority("15 USC Section 77b(a)(19)", 100, "Federal", 1),
            Authority("Jumpstart Our Business Startups Act (2012)", 100, "Federal", 1),
            Authority("SEC Release 33-9741 (2015)", 90, "Federal", 2)
        ],
        burden_holder="Company must monitor EGC status thresholds and disclose status in SEC filings",
        adversary_position="Institutional investors may prefer full disclosure over EGC scaled requirements",
        counter_arguments=[
            "Revenue threshold not exceeded in most recent fiscal year",
            "IPO occurred within last 5 years - still within eligibility window",
            "Public float measured on required date below $700M",
            "Testing-the-waters communications permitted under JOBS Act Section 105(c)"
        ],
        resolution_strategy="Monitor revenue and public float thresholds quarterly; disclose EGC status prominently in filings; consider opt-out if investor demand for full disclosure; use confidential SEC review to refine registration statement before public filing",
        entity_scope="Companies planning IPOs or recently public with under $1.235B revenues",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear statutory thresholds with detailed SEC implementation guidance",
        controlling_precedent="JOBS Act Sections 101-108 - comprehensive EGC benefits framework",
        issue_categories=[IssueCategory.PUBLIC_COMPANY, IssueCategory.DISCLOSURE, IssueCategory.REGISTRATION]
    ),
    DoctrineBlock(
        topic="Proxy Solicitation and Schedule 14A Requirements",
        keywords=["proxy", "schedule 14a", "shareholder meetings", "proxy statement", "rule 14a", "annual meeting"],
        conclusion_template=[
            "Proxy solicitation for reporting companies requires filing preliminary and definitive Schedule 14A with SEC.",
            "Proxy statement must contain material information about matters voted on and participants in solicitation.",
            "Shareholder proposals under Rule 14a-8 can be excluded for enumerated substantive and procedural grounds."
        ],
        reasoning_framework="""
        Exchange Act Section 14(a) prohibits proxy solicitation unless rules complied with.
        Proxy: authorization to vote shares on behalf of shareholder.
        Solicitation: broadly defined to include any communication reasonably calculated to result in procurement, withholding, or revocation of proxy.
        Schedule 14A: preliminary filed at least 10 days before mailing to shareholders; definitive filed when sent to shareholders.
        Required disclosure: management proposals, director nominees with bios, executive compensation, related party transactions, ratification of auditors.
        Rule 14a-8 shareholder proposals: eligible shareholders can include proposals in company proxy statement.
        Eligibility: $2,000 or 1% ownership for 1+ years; one proposal per meeting; 500-word limit.
        Exclusion grounds: not proper subject for shareholder action, violation of law, contrary to proxy rules, personal grievance, not significantly related to business, beyond company power, relates to ordinary business, conflicts with company proposal, already implemented, duplicates another proposal, resubmission within 3 years below threshold, relates to specific dividends.
        No-action process: company submits request to SEC staff seeking permission to exclude proposal; SEC staff issues no-action letter or denies request.
        Universal proxy rules (2022): dissident slates must use company's proxy card format.
        """,
        key_factors=[
            "Preliminary Schedule 14A filed 10+ days before mailing",
            "Definitive proxy contains all material information",
            "Shareholder proposals meet eligibility requirements",
            "Company exclusion requests supported by legal analysis",
            "No-action relief obtained before excluding proposals",
            "Universal proxy rules followed for contested elections"
        ],
        primary_authority=[
            Authority("15 USC Section 78n(a)", 100, "Federal", 1),
            Authority("17 CFR 240.14a-1 to 14a-21", 100, "Federal", 1),
            Authority("17 CFR 240.14a-8", 95, "Federal", 1)
        ],
        burden_holder="Company bears burden to demonstrate grounds for excluding shareholder proposals",
        adversary_position="Shareholder proponents challenge exclusions; SEC staff scrutinizes no-action requests",
        counter_arguments=[
            "Proposal relates to ordinary business operations - excludable under Rule 14a-8(i)(7)",
            "Proponent lacks requisite $2,000 or 1% ownership for 1 year",
            "Proposal substantially implemented by existing company policy",
            "Proposal conflicts with management proposal on same subject - Rule 14a-8(i)(9)"
        ],
        resolution_strategy="File timely preliminary and definitive proxy statements; engage proponents to negotiate withdrawals; submit well-reasoned no-action requests; retain proxy solicitor for contested situations; comply with universal proxy card requirements",
        entity_scope="Public reporting companies soliciting proxies for shareholder meetings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Detailed regulatory framework with extensive SEC staff interpretations via no-action letters",
        controlling_precedent="Rule 14a-8 - comprehensive shareholder proposal procedures and exclusion grounds",
        issue_categories=[IssueCategory.PUBLIC_COMPANY, IssueCategory.DISCLOSURE]
    ),
    DoctrineBlock(
        topic="Tender Offer Regulation and Schedule TO",
        keywords=["tender offer", "schedule to", "williams act", "rule 14d", "rule 14e", "all holders", "best price"],
        conclusion_template=[
            "Tender offers require Schedule TO filing before commencement and compliance with Williams Act timing and procedural rules.",
            "All-holders and best-price rules ensure equal treatment of all security holders in tender offers.",
            "Target company files Schedule 14D-9 with recommendation to shareholders - accept, reject, or remain neutral."
        ],
        reasoning_framework="""
        Williams Act 1968 added Sections 13(d), 14(d), 14(e) to regulate tender offers.
        Tender offer: no statutory definition; eight-factor Wellman test used - active/widespread solicitation, premium price, firm offer terms, contingent on minimum tenders, limited time, pressure to tender, public announcements, substantial percentage sought.
        Schedule TO filing: before commencement of tender offer; filed by bidder; discloses identity, source of funds, purpose, plans, material contracts.
        Rule 14d-1: commenced when offer materials first published, sent, or given.
        Minimum offering period: 20 business days from commencement; extend 10 business days if terms changed.
        Rule 14d-10 all-holders rule: offer must be open to all security holders of same class.
        Rule 14d-10 best-price rule: highest consideration paid to any holder must be paid to all.
        Pro rata acceptance: if oversubscribed, accept shares on pro rata basis.
        Withdrawal rights: shareholders can withdraw during offering period and after 60 days.
        Schedule 14D-9: target company recommendation - must file within 10 business days of offer commencement.
        Rule 14e-1: minimum 20 business days; prompt payment; pro rata in oversubscribed.
        Rule 14e-2: target must publish recommendation within 10 business days.
        Rule 14e-3: trading on material nonpublic information about tender offer prohibited.
        """,
        key_factors=[
            "Schedule TO filed before commencement",
            "Minimum 20 business day offering period",
            "All holders of class included in offer",
            "Best price paid to all tendering holders",
            "Pro rata acceptance if oversubscribed",
            "Target Schedule 14D-9 filed timely"
        ],
        primary_authority=[
            Authority("15 USC Section 78n(d)", 100, "Federal", 1),
            Authority("17 CFR 240.14d-1 to 14d-103", 100, "Federal", 1),
            Authority("17 CFR 240.14e-1 to 14e-8", 95, "Federal", 1),
            Authority("Wellman v. Dickinson, 682 F.2d 355 (2d Cir. 1982)", 90, "Federal", 2)
        ],
        burden_holder="Bidder must comply with all Williams Act timing and procedural requirements",
        adversary_position="Target companies and shareholders challenge tender offer compliance; SEC examines disclosure and timing",
        counter_arguments=[
            "Offer open to all holders - all-holders rule satisfied",
            "Same price paid to all tendering shareholders - best-price rule compliance",
            "Offering period extended by 10 business days after material term change",
            "Pro rata acceptance applied to oversubscribed offer in first 10 days"
        ],
        resolution_strategy="Engage experienced M&A counsel; prepare comprehensive Schedule TO; allow sufficient offering period; structure consideration to satisfy best-price rule; coordinate with financing sources; prepare for target defensive tactics",
        entity_scope="Acquirors making tender offers for reporting company equity securities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Detailed Williams Act regulations with bright-line timing and procedural rules",
        controlling_precedent="Wellman v. Dickinson - eight-factor test for tender offer definition",
        issue_categories=[IssueCategory.PUBLIC_COMPANY, IssueCategory.DISCLOSURE]
    ),
    DoctrineBlock(
        topic="Executive Compensation Disclosure and Say-on-Pay",
        keywords=["executive compensation", "cd&a", "say-on-pay", "compensation discussion", "golden parachute", "clawback"],
        conclusion_template=[
            "Item 402 requires detailed compensation disclosure including CD&A, summary table, and narrative explanations.",
            "Say-on-pay advisory votes required at least every 3 years per Dodd-Frank Section 951.",
            "Clawback policies required for accounting restatements per Dodd-Frank Section 954 and NYSE/Nasdaq listing standards."
        ],
        reasoning_framework="""
        Item 402 of Regulation S-K mandates comprehensive executive compensation disclosure.
        Compensation Discussion and Analysis (CD&A): narrative explaining compensation decisions and policies.
        Summary Compensation Table: 3-year tabular disclosure of CEO, CFO, and next 3 highest-paid executive officers (NEOs).
        Compensation elements: salary, bonus, stock awards, option awards, non-equity incentive plan, change-in-control payments, pension, deferred compensation, all other compensation.
        Pay ratio disclosure: ratio of CEO total compensation to median employee total compensation.
        Say-on-pay (Section 951): non-binding advisory vote on NEO compensation at least every 3 years.
        Say-on-frequency: shareholders vote on frequency of say-on-pay (1, 2, or 3 years).
        Say-on-golden-parachute: advisory vote on change-in-control payments if not previously approved.
        Clawback policy (Section 954): NYSE/Nasdaq listing standards require recovery of erroneously awarded incentive compensation based on accounting restatements.
        Pay-versus-performance disclosure (Item 402(v)): table showing relationship between executive pay and company performance.
        Hedging and pledging: must disclose policies prohibiting hedging or pledging of company stock.
        """,
        key_factors=[
            "CD&A narrative explains compensation decisions",
            "Summary Compensation Table accurate and complete",
            "Pay ratio calculated using consistent methodology",
            "Say-on-pay vote held at elected frequency",
            "Clawback policy adopted and disclosed",
            "Pay-versus-performance table included in proxy"
        ],
        primary_authority=[
            Authority("17 CFR 229.402", 100, "Federal", 1),
            Authority("15 USC Section 78n-1", 95, "Federal", 1),
            Authority("SEC Release 34-96492 (2022)", 90, "Federal", 2)
        ],
        burden_holder="Company must provide comprehensive, clear, and accurate compensation disclosure",
        adversary_position="Institutional investors scrutinize pay practices; proxy advisors recommend against say-on-pay if concerns exist",
        counter_arguments=[
            "Compensation aligned with performance - pay-versus-performance table demonstrates correlation",
            "Clawback policy complies with NYSE listing standard Rule 303A.14",
            "Pay ratio calculated using reasonable methodology and disclosed assumptions",
            "Golden parachute payments previously approved by shareholders in equity plan"
        ],
        resolution_strategy="Implement robust compensation committee process; retain independent compensation consultant; draft clear CD&A explaining rationale; adopt compliant clawback policy; engage with institutional investors pre-proxy season; monitor ISS/Glass Lewis voting recommendations",
        entity_scope="Public reporting companies disclosing executive compensation in proxy statements",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Detailed Item 402 requirements with specific tabular and narrative disclosure mandates",
        controlling_precedent="SEC Release 34-96492 - final pay-versus-performance rules",
        issue_categories=[IssueCategory.PUBLIC_COMPANY, IssueCategory.DISCLOSURE]
    )
]

class TelemetryCollector:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.doctrine_hits: Dict[str, int] = {}
        self.latencies: List[float] = []
        self.errors: Dict[str, int] = {}

    def record_query(self, query: str, mode: ResponseMode, zone: AnalysisZone,
                     latency_ms: int, triggered: List[str], confidence: ConfidenceLevel):
        self.queries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "query": query[:200],
            "mode": mode.value,
            "zone": zone.value,
            "latency_ms": latency_ms,
            "triggered_count": len(triggered),
            "confidence": confidence.value
        })
        self.latencies.append(latency_ms)
        for doctrine in triggered:
            self.doctrine_hits[doctrine] = self.doctrine_hits.get(doctrine, 0) + 1

    def record_error(self, error_domain: str):
        self.errors[error_domain] = self.errors.get(error_domain, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0,
            "doctrine_coverage": len(self.doctrine_hits) / len(DOCTRINE_CACHE) if DOCTRINE_CACHE else 0,
            "error_count": sum(self.errors.values()),
            "top_doctrines": sorted(self.doctrine_hits.items(), key=lambda x: x[1], reverse=True)[:10]
        }

TELEMETRY = TelemetryCollector()

def match_doctrines(question: str) -> List[DoctrineBlock]:
    question_lower = question.lower()
    scored = []
    for doctrine in DOCTRINE_CACHE:
        score = sum(2 for kw in doctrine.keywords if kw in question_lower)
        score += sum(1 for cat in doctrine.issue_categories if cat.value.lower() in question_lower)
        if doctrine.topic.lower() in question_lower:
            score += 5
        if score > 0:
            scored.append((score, doctrine))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for s, d in scored[:5]]

def three_layer_response(question: str, mode: ResponseMode, zone: AnalysisZone,
                         context: Optional[Dict[str, Any]]) -> QueryResponse:
    start_time = time.time()
    matched = match_doctrines(question)

    if not matched:
        TELEMETRY.record_error("no_doctrine_match")
        return QueryResponse(
            answer="No applicable securities regulatory doctrine found for query.",
            confidence=ConfidenceLevel.DISCLOSURE,
            authorities=[],
            reasoning_chain=["Query outside securities regulatory domain"],
            triggered_doctrines=[],
            analysis_zone=zone,
            determinism_hash=hashlib.sha256(question.encode()).hexdigest()[:16],
            response_time_ms=int((time.time() - start_time) * 1000),
            epistemic_status="INSUFFICIENT_DOMAIN_MATCH"
        )

    primary = matched[0]
    authorities = [f"{a.citation} (weight {a.weight})" for a in primary.primary_authority[:3]]
    reasoning = [primary.reasoning_framework[:300]]

    if mode == ResponseMode.FAST:
        answer = f"{primary.conclusion_template[0]} Applicable authority: {primary.primary_authority[0].citation}."
    elif mode == ResponseMode.DEFENSE:
        answer = "\n\n".join(primary.conclusion_template)
        answer += f"\n\nAuthority: {', '.join(authorities)}."
        answer += f"\n\nKey factors: {', '.join(primary.key_factors[:5])}."
    else:
        answer = f"MEMORANDUM RE: {primary.topic}\n\n"
        answer += "CONCLUSION:\n" + "\n".join(primary.conclusion_template) + "\n\n"
        answer += "ANALYSIS:\n" + primary.reasoning_framework[:800] + "\n\n"
        answer += f"AUTHORITIES:\n" + "\n".join([f"- {a}" for a in authorities]) + "\n\n"
        answer += f"COUNTER-ARGUMENTS:\n" + "\n".join([f"- {c}" for c in primary.counter_arguments[:4]])

    if zone == AnalysisZone.AUDIT:
        answer += f"\n\n[AUDIT] Controlling precedent: {primary.controlling_precedent}. Burden: {primary.burden_holder}."

    triggered = [d.topic for d in matched]
    latency_ms = int((time.time() - start_time) * 1000)

    TELEMETRY.record_query(question, mode, zone, latency_ms, triggered, primary.confidence)

    determinism_input = question + mode.value + zone.value + "".join(triggered)
    determinism_hash = hashlib.sha256(determinism_input.encode()).hexdigest()[:16]

    logger.info(f"Query: {question[:100]} | Mode: {mode.value} | Confidence: {primary.confidence.value} | Latency: {latency_ms}ms")

    return QueryResponse(
        answer=answer,
        confidence=primary.confidence,
        authorities=authorities,
        reasoning_chain=reasoning,
        triggered_doctrines=triggered,
        analysis_zone=zone,
        determinism_hash=determinism_hash,
        response_time_ms=latency_ms,
        epistemic_status="DOCTRINE_MATCHED"
    )

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} securities regulatory doctrine blocks")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{ENGINE_NAME} shutting down. Final stats: {TELEMETRY.get_stats()}")

@app.get("/health")
async def health():
    stats = TELEMETRY.get_stats()
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "queries_processed": stats["total_queries"],
        "avg_latency_ms": stats["avg_latency_ms"],
        "doctrine_coverage": stats["doctrine_coverage"],
        "error_count": stats["error_count"]
    }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    try:
        return three_layer_response(req.question, req.mode, req.zone, req.context)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        TELEMETRY.record_error("query_exception")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "categories": [c.value for c in d.issue_categories],
                "confidence": d.confidence.value,
                "authorities": [a.citation for a in d.primary_authority]
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/telemetry")
async def telemetry():
    return TELEMETRY.get_stats()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
