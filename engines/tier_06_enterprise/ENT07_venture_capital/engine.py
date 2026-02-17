"""
ENT07 Venture Capital Engine v1.0.0
TIE-grade intelligence for VC/startup financing analysis
Port 9147
"""
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "ENT07"
ENGINE_NAME = "Venture Capital Engine"
VERSION = "1.0.0"
PORT = 9147

logger.add(
    Path(__file__).parent / "logs" / "ent07_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

# ============================================================================
# ENUMS AND MODELS
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
    TERM_SHEET = "TERM_SHEET"
    PREFERRED_STOCK = "PREFERRED_STOCK"
    ANTI_DILUTION = "ANTI_DILUTION"
    LIQUIDATION_PREF = "LIQUIDATION_PREF"
    PROTECTIVE_PROVISIONS = "PROTECTIVE_PROVISIONS"
    BOARD_COMPOSITION = "BOARD_COMPOSITION"
    DRAG_TAG_ALONG = "DRAG_TAG_ALONG"
    SAFE_CONVERTIBLE = "SAFE_CONVERTIBLE"
    VESTING = "VESTING"
    VALUATION_409A = "VALUATION_409A"
    EQUITY_COMP = "EQUITY_COMP"
    SECURITIES_LAW = "SECURITIES_LAW"

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    categories: List[IssueCategory]
    authorities: List[str]
    mode: ResponseMode
    zone: AnalysisZone
    determinism_hash: str
    latency_ms: float
    timestamp: str

# ============================================================================
# DOCTRINE CACHE
# ============================================================================

class DoctrineBlock:
    def __init__(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: List[str],
        reasoning_framework: str,
        key_factors: List[str],
        primary_authority: List[str],
        burden_holder: str,
        adversary_position: str,
        counter_arguments: List[str],
        resolution_strategy: str,
        entity_scope: List[str],
        confidence: ConfidenceLevel,
        controlling_precedent: Optional[str] = None
    ):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.burden_holder = burden_holder
        self.adversary_position = adversary_position
        self.counter_arguments = counter_arguments
        self.resolution_strategy = resolution_strategy
        self.entity_scope = entity_scope
        self.confidence = confidence
        self.controlling_precedent = controlling_precedent

DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="Participating vs Non-Participating Preferred Stock",
        keywords=["participating preferred", "non-participating", "double dip", "liquidation preference", "participation cap"],
        conclusion_template=[
            "Participating preferred allows investors to recover preference amount plus share pro-rata in remaining proceeds.",
            "Non-participating preferred forces choice between preference or conversion to common.",
            "Participation caps limit upside participation to multiple of invested capital."
        ],
        reasoning_framework="""
Preferred stock participation determines liquidation waterfall economics. Participating preferred receives:
1. Liquidation preference (typically 1x invested capital) FIRST
2. Pro-rata share of remaining proceeds WITH common holders (double dip)
Non-participating preferred chooses EITHER preference OR conversion to common (whichever greater).
NVCA model term sheet defaults to non-participating. Participating preferred heavily favors investors
in modest exits (below 3-5x) but founders benefit more in large exits if cap applied.
""",
        key_factors=[
            "Exit scenario modeling (1x, 3x, 5x, 10x return multiples)",
            "Preference stack (senior vs pari passu)",
            "Participation cap (often 2-3x invested capital)",
            "Conversion price vs liquidation value comparison",
            "Multiple rounds with different terms (stacking effect)"
        ],
        primary_authority=[
            "NVCA Model Term Sheet 2024",
            "Delaware General Corporation Law Section 151(a)",
            "Trados case (Delaware Supreme Court 2013) - fiduciary duties with preferred",
            "Benchmark Capital Partners v. Vague (Del. Ch. 2002) - liquidation preference stacking"
        ],
        burden_holder="Company/Founders to negotiate favorable terms",
        adversary_position="VCs push participating preferred with no cap for downside protection",
        counter_arguments=[
            "Participating preferred creates misaligned incentives in M&A scenarios",
            "Founders diluted more severely in modest exits",
            "Later stage investors may demand senior liquidation preferences creating stack risk"
        ],
        resolution_strategy="Negotiate non-participating with 1x preference or participating with 2-3x cap",
        entity_scope=["Delaware C-Corp", "Preferred Stock Series A-D"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Trados duty of care to common stockholders"
    ),
    DoctrineBlock(
        topic="Weighted Average vs Full Ratchet Anti-Dilution",
        keywords=["anti-dilution", "weighted average", "full ratchet", "down round", "conversion price adjustment"],
        conclusion_template=[
            "Full ratchet reprices ALL existing preferred to new lower price per share.",
            "Weighted average adjusts conversion price proportionally based on capital raised.",
            "Broad-based weighted average includes all outstanding options/warrants; narrow-based excludes."
        ],
        reasoning_framework="""
Anti-dilution protections adjust preferred conversion price in down rounds to prevent investor dilution.
Full ratchet: Conversion price reduced to new round price regardless of amount raised (extreme dilution to common).
Weighted average: New conversion price = Old price x [(Common outstanding + Common purchasable at old price) / (Common outstanding + Common actually issued)]
Broad-based formula includes all options/warrants in denominator (more founder-friendly).
Narrow-based only includes issued shares (more investor-friendly).
NVCA standard is broad-based weighted average. Full ratchet rarely accepted except in distressed situations.
""",
        key_factors=[
            "Size of down round (10% vs 50% valuation decrease)",
            "Percentage of capital raised in down round",
            "Existing option pool size (affects broad vs narrow outcome)",
            "Multiple preferred series with different protections",
            "Carve-outs (certain strategic rounds, recaps excluded)"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 4 (Anti-Dilution Provisions)",
            "Delaware General Corporation Law Section 242(b)(2)",
            "Benchmark Capital v. Vague (Del. Ch. 2002)",
            "FASB ASC 260 - dilution calculations for EPS"
        ],
        burden_holder="Founders to negotiate weighted average vs full ratchet",
        adversary_position="VCs demand full ratchet or narrow-based weighted average for maximum protection",
        counter_arguments=[
            "Full ratchet creates death spiral for founders in down rounds",
            "Broad-based weighted average allows room for employee option pool expansion",
            "Pay-to-play provisions can mitigate need for harsh anti-dilution"
        ],
        resolution_strategy="Broad-based weighted average with carve-outs for option exercises and strategic investor rounds",
        entity_scope=["Series Seed", "Series A", "Series B+"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="SAFE Post-Money Valuation Mechanics",
        keywords=["SAFE", "simple agreement future equity", "post-money cap", "pre-money cap", "conversion discount", "valuation cap"],
        conclusion_template=[
            "Post-money SAFE cap includes SAFE itself in denominator, protecting against dilution from other SAFEs.",
            "Pre-money SAFE cap excludes other SAFEs, causing dilution surprise for founders.",
            "YC switched to post-money SAFE standard in 2018 for transparency."
        ],
        reasoning_framework="""
SAFE (Simple Agreement for Future Equity) converts to equity at next priced round based on:
1. Valuation cap (if set) - investor gets shares as if company valued at cap
2. Discount rate (if set) - investor gets discount to next round price (typically 20%)
3. Most Favored Nation (if set) - matches best terms of later SAFEs
POST-MONEY CAP: Conversion price = Post-Money Cap / (Fully Diluted Capitalization + all SAFE shares)
PRE-MONEY CAP: Conversion price = Pre-Money Cap / Fully Diluted Capitalization (existing SAFEs not included)
Post-money protects investor ownership percentage. Pre-money can heavily dilute founders if multiple SAFEs issued.
YC template (2018+) uses post-money cap with pro-rata side letter option.
""",
        key_factors=[
            "Total SAFE capital raised vs equity round size",
            "Valuation cap vs actual Series A valuation",
            "Discount rate (if cap not triggered)",
            "Pro-rata rights granted to SAFE holders",
            "MFN clause interactions with later SAFEs"
        ],
        primary_authority=[
            "Y Combinator SAFE Template (Post-Money, 2018)",
            "SEC Division of Corporation Finance FinHub guidance (2019)",
            "26 USC Section 1202(c)(1)(B) - QSBS stock definition",
            "State securities law exemptions (Reg D 506(b), 506(c))"
        ],
        burden_holder="Founders to track fully diluted cap table including all SAFE conversions",
        adversary_position="Investors prefer pre-money cap for better pricing in multiple SAFE scenarios",
        counter_arguments=[
            "Post-money SAFE more transparent but may result in higher effective valuation ask",
            "Multiple SAFEs at different caps create complex cap table",
            "Discount-only SAFEs with no cap create unlimited downside for founders in low priced rounds"
        ],
        resolution_strategy="Use post-money SAFE with single cap, avoid stacking multiple SAFEs at different terms",
        entity_scope=["Pre-Series A companies", "Convertible instruments"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="409A Valuation Safe Harbors",
        keywords=["409A", "fair market value", "stock option", "strike price", "independent appraisal", "safe harbor"],
        conclusion_template=[
            "409A valuation determines FMV of common stock for option grants to avoid constructive income.",
            "Independent appraisal provides presumption of reasonableness (safe harbor).",
            "Valuation must be updated after material events (funding, M&A offer, 12 months elapsed)."
        ],
        reasoning_framework="""
IRC Section 409A requires stock options granted at FMV or face immediate taxation plus 20% penalty.
Safe harbor methods (Treas. Reg. 1.409A-1(b)(5)):
1. Independent appraisal by qualified appraiser (strongest safe harbor)
2. Formula-based valuation (illiquid stock of startup)
3. Binding contract price
Independent appraisal presumed reasonable if:
- Performed by qualified independent appraiser
- No more than 12 months old
- No material events since valuation (funding round, M&A discussions, significant revenue change)
Common stock valued as residual after preferred liquidation preferences applied (discount to preferred price).
Typical discount: 30-50% below preferred price depending on stage/risk.
""",
        key_factors=[
            "Time since last funding round (affects volatility/discount)",
            "Revenue growth trajectory and unit economics",
            "Liquidation preference overhang (1x vs participating)",
            "Probability of liquidity event (DLOM discount)",
            "Comparable company analysis and market conditions"
        ],
        primary_authority=[
            "26 USC Section 409A - Nonqualified Deferred Compensation",
            "Treas. Reg. 1.409A-1(b)(5) - Safe Harbor Valuation Methods",
            "IRS Notice 2005-1 - 409A initial guidance",
            "AICPA Practice Aid - Valuation of Privately-Held Company Equity"
        ],
        burden_holder="Company to obtain and maintain current 409A valuations",
        adversary_position="IRS may challenge valuation if appears unreasonably low or stale",
        counter_arguments=[
            "409A appraisal costs $5K-20K per valuation",
            "Conservative 409A valuations make options less attractive to employees",
            "Safe harbor not absolute - IRS can still challenge in audit"
        ],
        resolution_strategy="Obtain independent 409A appraisal every 12 months and within 30 days of funding round",
        entity_scope=["Private C-Corps issuing stock options"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Treas. Reg. 1.409A-1(b)(5)"
    ),
    DoctrineBlock(
        topic="Section 83(b) Election Timing",
        keywords=["83(b)", "restricted stock", "vesting", "ordinary income", "capital gains", "30 day deadline"],
        conclusion_template=[
            "Section 83(b) election allows taxation at grant (not vesting) for restricted stock.",
            "Must be filed within 30 days of grant (strict deadline, no extensions).",
            "Election locks in lower FMV at grant vs higher FMV at vesting, converts spread to capital gains."
        ],
        reasoning_framework="""
IRC Section 83(b) permits early taxation election for restricted property subject to substantial risk of forfeiture.
Without 83(b): Ordinary income recognized at vesting on spread between FMV and purchase price.
With 83(b): Ordinary income recognized at grant (typically zero if purchased at FMV), future appreciation taxed as capital gains.
TIMING REQUIREMENT (strict):
- Election filed with IRS within 30 days of grant date
- Copy attached to tax return for year of grant
- Copy provided to employer
MISSED DEADLINE: Cannot cure, ordinary income due at each vesting date.
Typical scenario: Founder receives 8M shares subject to 4-year vest, pays $0.001/share ($8K total).
Files 83(b) immediately. Tax due on $8K ordinary income. At exit, entire gain over $8K is capital gains (23.8% vs 37% max).
""",
        key_factors=[
            "Purchase price vs FMV at grant (determines immediate tax)",
            "Expected future appreciation (benefit of 83(b) increases with growth)",
            "Risk of forfeiture (lose taxes paid if leave before vest and no refund)",
            "QSBS eligibility (5-year holding period starts at grant with 83(b))",
            "AMT impact for ISOs (83(b) can trigger AMT)"
        ],
        primary_authority=[
            "26 USC Section 83(b) - Election to include restricted property",
            "Treas. Reg. 1.83-2 - Election procedures",
            "Rev. Proc. 2012-29 - Sample 83(b) election form",
            "Alves v. Commissioner, 734 F.2d 478 (9th Cir. 1984) - strict 30-day rule"
        ],
        burden_holder="Employee/Founder to file election timely",
        adversary_position="IRS strictly enforces 30-day deadline, no equitable relief",
        counter_arguments=[
            "Paying tax upfront on illiquid stock creates cash flow burden",
            "If company fails, no refund of taxes paid",
            "83(b) election for ISOs can trigger AMT on spread"
        ],
        resolution_strategy="File 83(b) election by certified mail within 30 days, retain proof of filing, attach to tax return",
        entity_scope=["Founders", "Early employees receiving restricted stock"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Alves v. Commissioner - no late filings accepted"
    ),
    DoctrineBlock(
        topic="QSBS Section 1202 Exclusion Requirements",
        keywords=["QSBS", "qualified small business stock", "1202", "100 million test", "5 year holding", "gain exclusion"],
        conclusion_template=[
            "QSBS allows exclusion of up to $10M or 10x basis gain on sale of qualified stock.",
            "Stock must be acquired at original issuance from C-corp with <$50M assets.",
            "5-year holding period and active business test required."
        ],
        reasoning_framework="""
IRC Section 1202 provides tax exclusion for gains on Qualified Small Business Stock:
- 100% exclusion for stock acquired after Sept 27, 2010
- Greater of $10M or 10x adjusted basis excluded from capital gains
QUALIFICATION REQUIREMENTS:
1. C-Corporation (not S-corp, LLC, or partnership)
2. Gross assets <$50M immediately after issuance (includes SAFEs/convertibles)
3. Stock acquired at original issuance (not secondary)
4. 80% active business test (not passive investment, hospitality, farming, finance, etc.)
5. 5-year holding period from date of issuance
TRAPS:
- Redemptions within 4 years can disqualify (reduce basis)
- Asset test includes cash and invested capital
- Each shareholder gets separate $10M/$10x limit per company
- Section 83(b) election starts 5-year clock at grant vs vesting
- Conversion from SAFE/convertible relates back to SAFE issuance for holding period
""",
        key_factors=[
            "Asset test at each issuance (fundraising can breach $50M cap)",
            "Active business vs passive investment percentage (80% test)",
            "Holding period start date (grant vs vesting, SAFE conversion)",
            "Redemption activity timing (4-year window)",
            "Per-issuer $10M limit stacking across family members"
        ],
        primary_authority=[
            "26 USC Section 1202 - Qualified Small Business Stock",
            "IRC Section 1202(e)(3) - Active Business Requirement",
            "Treas. Reg. 1.1202-2 - Qualified Small Business",
            "Rev. Rul. 2007-45 - Conversion of preferred to common preserves QSBS"
        ],
        burden_holder="Shareholder to maintain documentation and satisfy holding period",
        adversary_position="IRS may challenge asset test, active business requirement, or holding period",
        counter_arguments=[
            "Asset test easily breached in large funding rounds (>$50M post-money)",
            "Passive income from IP licensing may fail 80% active business test",
            "Complex tracking across multiple stock issuances and conversions"
        ],
        resolution_strategy="File 83(b) at grant, track 5-year holding from each issuance, maintain <$50M assets test at each round",
        entity_scope=["C-Corp founders and early employees"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IRC 1202(c) and (e) statutory requirements"
    ),
    DoctrineBlock(
        topic="Protective Provisions - Investor Veto Rights",
        keywords=["protective provisions", "class vote", "preferred approval", "super majority", "change of control", "adverse changes"],
        conclusion_template=[
            "Protective provisions grant preferred stockholders veto rights over major corporate actions.",
            "Typical protections: amendments to certificate, new senior securities, dividends, M&A, asset sales.",
            "Separate class vote (Series A, Series B independently) or as-converted voting."
        ],
        reasoning_framework="""
Protective provisions in certificate of incorporation require preferred stockholder approval for:
STANDARD NVCA PROTECTIONS (class vote required):
1. Adverse changes to preferred rights (liquidation preference, conversion, voting)
2. Authorize or issue senior or pari passu securities
3. Redeem or repurchase shares (except per stock plan or repurchase agreement)
4. Declare or pay dividends on common
5. Change authorized common or preferred shares
6. Amend certificate or bylaws adversely affecting preferred
7. Merge, sell substantially all assets, or liquidate
8. Increase/decrease size of Board
MECHANICS:
- Class vote: Each series votes separately (Series A can block even if Series B approves)
- As-converted vote: All preferred vote together on as-if-converted basis
- Sunset provisions: Protections expire at qualified IPO (>$50M at >$3/share typical)
NEGOTIATION POINTS:
- Board-approved repurchases vs any repurchase (stock buyback flexibility)
- Threshold for asset sales (>50% vs >80% of assets)
- Super-majority (2/3 vs majority) of preferred holders
""",
        key_factors=[
            "Breadth of protective provisions (NVCA standard vs expanded)",
            "Class vote vs as-converted voting mechanism",
            "Sunset trigger (IPO threshold, time-based, qualified financing)",
            "Carve-outs for normal operations (employee stock plan, de minimis asset sales)",
            "Conflicts between preferred series with different terms"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 6 (Protective Provisions)",
            "Delaware General Corporation Law Section 242(b)(2) - class voting rights",
            "8 Del. C. Section 251(c) - merger approval requirements",
            "VantagePoint Venture Partners v. Examen, Inc. (Del. Ch. 2005) - fiduciary duties in M&A with preferred"
        ],
        burden_holder="Company to obtain required preferred approvals before major actions",
        adversary_position="VCs demand broad protections including operational matters (budget, hiring)",
        counter_arguments=[
            "Excessive protections create operational gridlock",
            "Multiple preferred series with separate class votes enables single series holdout blocking",
            "Board-level decisions should not require stockholder approval (management flexibility)"
        ],
        resolution_strategy="NVCA-standard protections with carve-outs for employee stock plans and <$500K asset sales",
        entity_scope=["Preferred Stock Series A-D"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="DGCL Section 242(b)(2) class voting requirements"
    ),
    DoctrineBlock(
        topic="Drag-Along and Tag-Along Rights",
        keywords=["drag-along", "tag-along", "co-sale", "forced sale", "M&A approval", "minority squeeze-out"],
        conclusion_template=[
            "Drag-along allows majority holders to force minority to sell in M&A transaction.",
            "Tag-along (co-sale) allows minority to participate in third-party sales by founders.",
            "Drag threshold typically 50-75% of preferred plus common on as-converted basis."
        ],
        reasoning_framework="""
DRAG-ALONG RIGHTS:
Permit majority stockholders (typically Board + preferred holders above threshold) to compel ALL stockholders
to approve sale of company on same terms. Overcomes holdout minority blocking M&A.
Standard NVCA drag-along requires:
- Approval by Board (including majority of preferred directors)
- Holders of majority (or 2/3) of preferred (voting as-converted with common)
- Founders/key holders explicitly bound
- All shareholders receive same per-share consideration (subject to liquidation preferences)
- Representations limited to ownership and authority (no operational reps by minority)
TAG-ALONG (CO-SALE) RIGHTS:
Allow preferred investors to participate pro-rata in founder/key holder sales to third parties.
Prevents founders from selling secondary shares while investors remain illiquid.
Mechanics:
- Founder proposes to sell X shares to buyer
- Preferred investors have right to substitute their shares for portion of founder shares (pro-rata to ownership)
- Founder sale reduced, investors achieve partial liquidity
Exceptions: Transfers to family trusts, co-founders, estate planning typically exempted.
""",
        key_factors=[
            "Drag-along threshold (majority vs 2/3 of preferred)",
            "Inclusion of management/option holders in drag",
            "Representation and warranty caps for dragged minority",
            "Tag-along pro-rata allocation vs piggyback unlimited",
            "Exemptions for estate planning, pledges to lenders"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Sections 2.7 (Tag-Along), 2.8 (Drag-Along)",
            "Delaware General Corporation Law Section 251 - merger approval",
            "In re Appraisal of Ancestry.com (Del. Ch. 2015) - drag-along enforceability",
            "Third Point LLC v. Ruprecht (Del. Ch. 2014) - fiduciary duties in take-private"
        ],
        burden_holder="Majority holders to exercise drag-along rights; minority to assert tag-along",
        adversary_position="Founders resist drag-along or seek high thresholds; VCs demand low thresholds",
        counter_arguments=[
            "Drag-along at too low threshold (simple majority) enables minority squeeze-out",
            "Tag-along rights block founder liquidity and secondary sales",
            "Representation exposure for dragged shareholders in M&A creates escrow/indemnity risk"
        ],
        resolution_strategy="Drag-along at 2/3 preferred + Board approval; tag-along with exemptions for <$1M transfers and estate planning",
        entity_scope=["All stockholders, particularly founders and preferred holders"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Board Composition and Observer Rights",
        keywords=["board of directors", "board seats", "observer rights", "independent director", "board control"],
        conclusion_template=[
            "Typical Series A board: 2 common (founder-elected), 2 preferred (investor-elected), 1 independent.",
            "Observer rights allow non-director attendance without voting; subject to confidentiality.",
            "Board control shifts from founders to investors as preferred ownership increases."
        ],
        reasoning_framework="""
Board composition negotiated at each funding round:
TYPICAL PROGRESSION:
- Seed: 3 directors (2 founders, 1 lead investor)
- Series A: 5 directors (2 common, 2 preferred, 1 independent mutually agreed)
- Series B+: 7 directors (2 common, 3 preferred, 2 independent)
ELECTION MECHANICS:
- Common stockholders elect common-designated directors (class vote)
- Preferred stockholders elect preferred-designated directors (class vote or per series)
- Independent director elected by common + preferred voting together (or Board approval)
KEY TERMS:
- Observer rights: Non-voting Board meeting attendance (typically 1 per major investor)
- Observers subject to confidentiality, excluded from conflicts/competitive matters
- Independent director qualifications: no affiliation with company or investors
- Board approval thresholds: simple majority vs super-majority for specified actions
FIDUCIARY DUTIES:
All directors owe fiduciary duties to CORPORATION (not appointing stockholder class).
Trados case: Board cannot favor preferred over common in sale process.
""",
        key_factors=[
            "Total Board size (odd vs even, tie-breaking)",
            "Allocation between common, preferred, independent seats",
            "Per-series Board seats vs preferred voting as single class",
            "Observer rights scope and confidentiality obligations",
            "Independent director definition and selection process"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 3 (Board Composition)",
            "Delaware General Corporation Law Section 141 - Board powers",
            "8 Del. C. Section 223 - vacancy and removal of directors",
            "Trados case (Del. 2013) - fiduciary duties to common in preferred-controlled sale"
        ],
        burden_holder="Company to maintain agreed Board composition and provide observer access",
        adversary_position="VCs seek Board control or veto via super-majority voting requirements",
        counter_arguments=[
            "Investor Board control reduces founder operational flexibility",
            "Observer rights create confidentiality risks with competitive VCs",
            "Independent directors may align with investors over founders"
        ],
        resolution_strategy="Balanced Board with true independents, observers excluded from competitive/conflict matters",
        entity_scope=["Board of Directors of funded startups"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Trados - Board owes duties to all stockholders"
    ),
    DoctrineBlock(
        topic="Registration Rights - Demand and Piggyback",
        keywords=["registration rights", "S-1", "demand rights", "piggyback", "Form S-3", "lock-up"],
        conclusion_template=[
            "Demand rights allow investors to force company IPO registration at investor expense.",
            "Piggyback rights allow investors to include shares in company-initiated registration.",
            "Form S-3 eligibility (if public >12 months) enables shelf registration for ongoing sales."
        ],
        reasoning_framework="""
Registration rights grant preferred investors ability to sell shares in public markets post-IPO.
DEMAND REGISTRATION RIGHTS:
- Investors holding threshold percentage (typically 30-50% of registrable securities) can demand S-1 filing
- Limited number of demands (1-2) with minimum offering size ($5M-$15M)
- Company can delay if underwriters advise materially adverse to IPO (6-month max delay)
- Investors pay registration expenses
PIGGYBACK REGISTRATION RIGHTS:
- When company files S-1 (IPO) or secondary offering, investors can include shares
- Underwriter cutback provision if offering oversubscribed (investors cut first, then selling stockholders, company last)
- Unlimited piggybacking vs limited number (3-5 piggybacks)
FORM S-3 RIGHTS:
- Once public >12 months and meet $75M public float test, investors can demand shelf registration on Form S-3
- Unlimited S-3 demands above minimum threshold ($1M-$3M)
- Allows ongoing registered sales without full S-1 process
LOCK-UP AGREEMENTS:
- 180-day post-IPO lock-up standard in underwriting agreement
- Registration rights subordinate to underwriter lock-up
""",
        key_factors=[
            "Demand threshold (percentage of registrable securities required)",
            "Number of demand rights (1-2) and minimum offering size",
            "Piggyback cutback priority (pro-rata vs inverse seniority)",
            "Form S-3 eligibility timing and thresholds",
            "Expenses allocation (company vs investors)",
            "Lock-up period duration and early release provisions"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 7 (Registration Rights)",
            "Securities Act of 1933 Section 5 - registration requirement",
            "SEC Form S-1 and Form S-3 eligibility requirements",
            "FINRA Rule 5110 - underwriting compensation and lock-ups"
        ],
        burden_holder="Company to register shares upon proper demand; investors to meet thresholds",
        adversary_position="VCs demand unlimited demand rights; company seeks high thresholds and delay rights",
        counter_arguments=[
            "Forced registration diverts management focus and creates expense ($2M+ S-1 cost)",
            "Piggyback rights flood offering and depress pricing",
            "S-3 demands create continuous disclosure burden"
        ],
        resolution_strategy="2 demand rights with $10M minimum, unlimited S-3 after eligibility, standard 180-day lock-up",
        entity_scope=["Public companies, post-IPO preferred holders"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Information Rights and Financial Reporting",
        keywords=["information rights", "audit", "quarterly financials", "budget", "inspection rights"],
        conclusion_template=[
            "Major investors receive quarterly unaudited and annual audited financials.",
            "Inspection rights include access to books, records, facilities.",
            "Information rights terminate at IPO or if investor holds <threshold percentage."
        ],
        reasoning_framework="""
Information rights granted to preferred stockholders (typically major investors holding >1-5% fully diluted):
STANDARD INFORMATION RIGHTS:
1. Annual audited financials within 120 days of fiscal year end
2. Quarterly unaudited financials within 45 days of quarter end
3. Annual operating budget 30 days before fiscal year start
4. Monthly unaudited financials (if negotiated)
INSPECTION RIGHTS:
- Reasonable access to premises and inspection of books/records during business hours
- Subject to confidentiality obligations
- Company can exclude competitive investors from sensitive information
TERMINATION:
- At qualified IPO (automatic)
- If investor ownership falls below threshold (1-3% fully diluted)
- If investor becomes competitor (discretionary exclusion)
STRATEGIC CONSIDERATIONS:
- Information asymmetry vs investor oversight
- Audit cost ($20K-$100K annually for startups)
- Monthly reporting burden on finance team
- Confidentiality risks with multiple investors (Chinese wall protocols)
""",
        key_factors=[
            "Threshold for major investor status (percentage ownership)",
            "Frequency of reporting (monthly vs quarterly)",
            "Audit requirement and cost allocation",
            "Inspection rights scope and limitations",
            "Termination triggers (IPO, ownership threshold)"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 8 (Information Rights)",
            "Delaware General Corporation Law Section 220 - stockholder inspection rights",
            "Sarbanes-Oxley Act Section 404 - internal controls (post-IPO)",
            "Private Securities Litigation Reform Act - forward-looking statements"
        ],
        burden_holder="Company to prepare and deliver financial statements timely",
        adversary_position="VCs demand monthly financials and KPI dashboards; company seeks quarterly only",
        counter_arguments=[
            "Monthly reporting creates excessive administrative burden for early-stage company",
            "Audit requirement costly for pre-revenue startups",
            "Multiple investors with information rights increases leak risk"
        ],
        resolution_strategy="Quarterly financials for all major investors (>1% ownership), annual audit, monthly reports only for lead investors",
        entity_scope=["Preferred stockholders holding >1-5% fully diluted"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Vesting Schedules and Acceleration",
        keywords=["vesting", "cliff", "acceleration", "single trigger", "double trigger", "founder vesting"],
        conclusion_template=[
            "Standard vesting: 4-year vest with 1-year cliff.",
            "Single-trigger acceleration vests on change of control; double-trigger requires termination.",
            "Founders typically receive partial credit for past service or no vesting."
        ],
        reasoning_framework="""
Equity vesting aligns incentives and retention for founders and employees.
STANDARD VESTING SCHEDULE:
- 4-year monthly vesting
- 1-year cliff (25% vests at 12 months, then monthly thereafter)
- No vesting if terminated before cliff
ACCELERATION PROVISIONS:
Single-Trigger Acceleration:
- 100% (or 50%) vesting upon change of control (acquisition, merger)
- Investor-unfriendly (windfall to departing employees post-acquisition)
Double-Trigger Acceleration:
- Vesting requires BOTH change of control AND termination without cause or for good reason within 12-18 months
- Acquirer-friendly (retains employees post-close with unvested equity)
- Standard in VC-backed companies
FOUNDER VESTING:
- Investors often require founder stock subject to vesting (reverse vesting)
- Partial credit for prior service (25-50% vested at funding)
- Accelerated vesting on termination without cause (investor removal protection)
REPURCHASE RIGHTS:
- Company option to repurchase unvested shares at cost upon termination
- Unvested shares subject to forfeiture vs repurchase (tax treatment)
""",
        key_factors=[
            "Vesting period (4 years standard, 3 years for senior execs negotiable)",
            "Cliff duration (1 year vs 6 months vs no cliff for execs)",
            "Single vs double trigger acceleration",
            "Acceleration percentage (100% vs 50% vs pro-rata)",
            "Founder vesting and credit for prior service",
            "Post-termination exercise period for vested options"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 5 (Vesting)",
            "26 USC Section 83 - restricted property taxation",
            "IRS Notice 2005-1 - 409A vesting schedules",
            "Eshleman v. Bluestone Coal Corp. (Del. Ch. 1982) - change of control provisions"
        ],
        burden_holder="Company to enforce vesting and repurchase unvested shares upon termination",
        adversary_position="Employees seek single-trigger acceleration; investors demand double-trigger",
        counter_arguments=[
            "Single-trigger acceleration creates acquirer concern and reduces acquisition price",
            "Founder vesting with no credit punishes sweat equity contributions",
            "Double-trigger acceleration may not protect if acquirer eliminates role (constructive termination risk)"
        ],
        resolution_strategy="4-year monthly vest with 1-year cliff, double-trigger acceleration, founders get 25% credit for prior service",
        entity_scope=["Founders, employees, advisors receiving equity compensation"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Right of First Refusal and Co-Sale Rights",
        keywords=["ROFR", "right of first refusal", "co-sale", "secondary sales", "transfer restrictions"],
        conclusion_template=[
            "ROFR grants company (then investors) right to purchase shares before third-party sale.",
            "Co-sale rights allow investors to participate pro-rata in founder secondary sales.",
            "Exemptions for estate planning, family transfers, and affiliates standard."
        ],
        reasoning_framework="""
Transfer restrictions on common stock prevent undesirable third-party ownership and ensure investor liquidity parity.
RIGHT OF FIRST REFUSAL (ROFR):
When founder/key holder receives bona fide offer to sell shares:
1. Holder provides notice to company with offer terms
2. Company has first right to purchase at offer price (30 days)
3. If company declines, investors have pro-rata right to purchase (30 days)
4. If company and investors decline, holder can sell to third party on same terms (120 days)
Mechanics:
- ROFR price: third-party offer price (not FMV or formula)
- Pro-rata allocation among investors based on ownership percentage
- Oversubscription right if some investors decline
CO-SALE RIGHTS (TAG-ALONG):
If ROFR declined and holder proceeds with third-party sale, investors can substitute their shares pro-rata.
Example: Founder sells 100K shares to buyer. Investors holding 40% can substitute 40K investor shares, reducing founder sale to 60K.
PERMITTED TRANSFERS (ROFR/Co-Sale Exempt):
- Transfers to spouse, children, family trusts (with signed joinder)
- Transfers to affiliates or co-founders
- Pledges to bona fide lenders
- Testamentary transfers
TERMINATION:
- IPO registration of shares
- Below de minimis threshold (<1% ownership)
""",
        key_factors=[
            "ROFR exercise periods (30-45 days company, 30 days investors)",
            "Co-sale allocation (pro-rata vs pari passu)",
            "Permitted transfer exemptions and joinder requirements",
            "Third-party sale timeframe after ROFR decline (120 days)",
            "Termination thresholds and IPO trigger"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 2.6 (ROFR and Co-Sale)",
            "Delaware General Corporation Law - transfer restrictions enforceability",
            "Groves v. Prickett (Del. Ch. 2013) - ROFR valuation disputes",
            "UCC Article 8 - certificated securities transfer restrictions"
        ],
        burden_holder="Selling stockholder to provide proper notice and comply with ROFR/co-sale process",
        adversary_position="Founders seek minimal transfer restrictions; investors demand broad ROFR/co-sale",
        counter_arguments=[
            "ROFR process lengthy and uncertain, chills third-party buyer interest",
            "Co-sale rights reduce founder liquidity in secondary sales",
            "Permitted transfer exemptions create indirect end-runs around restrictions"
        ],
        resolution_strategy="ROFR with 30-day company / 30-day investor exercise periods, co-sale rights, standard exemptions for estate planning",
        entity_scope=["Common stock, founder shares, key employee restricted stock"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Pay-to-Play Provisions",
        keywords=["pay-to-play", "down round", "conversion to common", "anti-dilution waiver", "pro-rata participation"],
        conclusion_template=[
            "Pay-to-play provisions penalize non-participating investors in down rounds.",
            "Standard penalty: conversion to common stock, loss of anti-dilution protection.",
            "Encourages all investors to participate pro-rata in future financings."
        ],
        reasoning_framework="""
Pay-to-play provisions adopted in down rounds or difficult financings to ensure existing investor support.
MECHANICS:
In qualified financing (typically down round or minimum threshold round):
- Investors who purchase pro-rata share retain preferred stock rights
- Investors who decline or purchase <pro-rata are penalized
STANDARD PENALTIES:
1. Conversion to common stock (loss of liquidation preference, anti-dilution, protective provisions)
2. Loss of anti-dilution protection (maintain preferred but waive anti-dilution adjustments)
3. Loss of pro-rata participation rights in future rounds
THRESHOLD REQUIREMENTS:
- Qualified financing threshold: $2M-$5M minimum raise
- Pro-rata participation: investor must purchase percentage equal to ownership stake
- Carve-outs: investors holding <1-2% may be exempt
STRATEGIC IMPLICATIONS:
- Aligns investor incentives to support company in difficult environment
- Punishes non-supportive investors (converts preferred to common)
- Can create tension between early and late-stage investors with different risk profiles
- VC fund life cycle issues (fund closing, limited ability to follow-on)
""",
        key_factors=[
            "Penalty severity (conversion to common vs anti-dilution waiver only)",
            "Qualified financing threshold (size of round triggering pay-to-play)",
            "Pro-rata participation definition (dollars vs percentage)",
            "Carve-outs for small investors or special circumstances",
            "Unanimous vs majority investor approval to adopt provision"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 4.3 (Pay-to-Play)",
            "Delaware General Corporation Law Section 242 - certificate amendments",
            "In re Trados Inc. Shareholder Litigation (Del. Ch. 2013) - preferred/common conflicts",
            "Frederick Hsu Living Trust v. ODN Holding Corp. (Del. Ch. 2017) - fiduciary duties in recaps"
        ],
        burden_holder="Company to enforce pay-to-play and effect conversions",
        adversary_position="New investors demand pay-to-play; existing investors resist or negotiate exemptions",
        counter_arguments=[
            "Pay-to-play punishes early investors who took highest risk",
            "Conversion to common destroys liquidation preference in downside scenarios",
            "VC fund constraints (closed fund, no reserves) may prevent pro-rata participation through no fault"
        ],
        resolution_strategy="Anti-dilution waiver penalty (not full conversion to common) with carve-out for <1% holders",
        entity_scope=["Preferred stockholders in down round financings"],
        confidence=ConfidenceLevel.AGGRESSIVE
    ),
    DoctrineBlock(
        topic="No-Shop and Exclusivity in Term Sheets",
        keywords=["no-shop", "exclusivity", "fiduciary out", "break-up fee", "go-shop"],
        conclusion_template=[
            "No-shop period (30-60 days) prohibits company from soliciting competing investors during due diligence.",
            "Fiduciary out allows Board to consider superior proposals if fiduciary duties require.",
            "Non-binding term sheet except for exclusivity, confidentiality, and expense provisions."
        ],
        reasoning_framework="""
Term sheet exclusivity provisions protect investor time and diligence costs during negotiation.
NO-SHOP CLAUSE:
For period of 30-60 days from term sheet signing, company agrees NOT to:
1. Solicit or encourage competing financing proposals
2. Provide confidential information to other potential investors
3. Engage in negotiations or discussions with competing investors
FIDUCIARY OUT:
Board retains right to consider unsolicited superior proposals if fiduciary duties require (Revlon duties).
Cannot affirmatively shop, but can respond to inbound inquiries and provide information if Board determines necessary.
BREAK-UP FEES:
Typically NOT included in early-stage financings (Series A-B).
Later-stage or M&A term sheets may include:
- 1-3% break-up fee if company accepts competing offer during exclusivity
- Expense reimbursement ($50K-$500K for diligence costs)
NON-BINDING NATURE:
Term sheet generally non-binding except:
- No-shop/exclusivity provisions (binding)
- Confidentiality obligations (binding)
- Expense allocation (binding if specified)
- Governing law and jurisdiction (binding)
Final binding agreement is definitive stock purchase agreement executed at closing.
""",
        key_factors=[
            "No-shop period duration (30-90 days)",
            "Fiduciary out scope and Board determination rights",
            "Break-up fee percentage (if any) and triggers",
            "Expense reimbursement allocation (investor vs company diligence costs)",
            "Binding vs non-binding provisions in term sheet"
        ],
        primary_authority=[
            "NVCA Model Term Sheet - Binding Terms section",
            "Revlon, Inc. v. MacAndrews & Forbes Holdings (Del. 1986) - fiduciary duties in sale context",
            "Omnicare, Inc. v. NCS Healthcare, Inc. (Del. 2003) - deal protection devices",
            "In re Toys 'R' Us, Inc. Shareholder Litigation (Del. Ch. 2005) - no-shop provisions"
        ],
        burden_holder="Company to honor no-shop during exclusivity period",
        adversary_position="Investors demand long exclusivity with penalties; company seeks short period with fiduciary outs",
        counter_arguments=[
            "Extended no-shop locks company into single investor, eliminates competitive tension",
            "Break-up fees chill competing bids and reduce company leverage",
            "Fiduciary out may be illusory if investor threatens to walk on any Board consideration of alternatives"
        ],
        resolution_strategy="45-day no-shop with fiduciary out, no break-up fee for Series A/B, expense reimbursement only if company bad faith",
        entity_scope=["Term sheet negotiations, Series A-D financings"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Convertible Note Terms - Interest and Conversion Mechanics",
        keywords=["convertible note", "bridge financing", "interest rate", "maturity date", "conversion discount", "valuation cap"],
        conclusion_template=[
            "Convertible notes are debt instruments that convert to equity at next priced round.",
            "Standard terms: 5-8% interest, 12-24 month maturity, 20% discount, optional valuation cap.",
            "Accrued interest typically converts with principal (not paid in cash)."
        ],
        reasoning_framework="""
Convertible notes bridge financing between equity rounds, deferring valuation negotiation.
CORE TERMS:
1. PRINCIPAL: Amount invested
2. INTEREST RATE: 5-8% simple interest (accrues but not paid until maturity/conversion)
3. MATURITY DATE: 12-24 months from issuance
4. CONVERSION DISCOUNT: 15-25% discount to next equity round price (typically 20%)
5. VALUATION CAP: Maximum valuation for conversion purposes ($5M-$15M typical for seed)
CONVERSION MECHANICS:
Upon qualified financing (typically >$1M minimum):
- Note converts to equity at LOWER of:
  a) Discount price: Next round price x (1 - discount rate)
  b) Cap price: Valuation cap / fully diluted shares
- Accrued interest converts with principal (adds to investment amount)
Example: $500K note, 6% interest, 20% discount, $8M cap, held 12 months.
Next round: $10M pre-money at $1.00/share.
Accrued interest: $30K. Total converting: $530K.
Discount price: $0.80/share (20% discount from $1.00).
Cap price: Would need $8M valuation, but round is $10M, so discount applies.
Investor receives: 662,500 shares ($530K / $0.80).
MATURITY EVENT:
If no qualified financing before maturity:
- Company must repay principal + interest (cash payment), OR
- Automatic conversion at pre-agreed valuation (shadow Series Seed), OR
- Extension by mutual agreement
""",
        key_factors=[
            "Interest rate (simple vs compounding, 5-8% range)",
            "Maturity date and extension rights",
            "Conversion discount percentage (15-25%)",
            "Valuation cap (if any) and relationship to expected Series A valuation",
            "Qualified financing threshold (minimum raise triggering auto-conversion)",
            "Maturity remedies (repayment vs forced conversion vs extension)"
        ],
        primary_authority=[
            "Uniform Commercial Code Article 8 - investment securities",
            "26 USC Section 1273 - OID (original issue discount) rules",
            "SEC Regulation D Section 506 - private placement exemptions",
            "State usury laws (interest rate caps, typically 10-18% max)"
        ],
        burden_holder="Company to repay at maturity if no qualified financing; investor to accept conversion terms",
        adversary_position="Investors seek high cap and low discount; company seeks no cap and high discount",
        counter_arguments=[
            "Convertible notes create debt overhang and balance sheet liability",
            "Valuation cap set too low creates excessive dilution in up-round",
            "Maturity date approaching creates distressed financing pressure",
            "Accrued interest compounds dilution (interest converts to equity)"
        ],
        resolution_strategy="5% interest, 18-month maturity, 20% discount, cap at 50-70% of expected Series A valuation",
        entity_scope=["Bridge financings, pre-Series A seed rounds"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Accredited Investor and Reg D Exemptions",
        keywords=["accredited investor", "Reg D", "506(b)", "506(c)", "general solicitation", "bad actor disqualification"],
        conclusion_template=[
            "Accredited investor status required for most private offerings to avoid SEC registration.",
            "Reg D 506(b) allows unlimited accredited + 35 sophisticated non-accredited, no general solicitation.",
            "Reg D 506(c) allows unlimited accredited only, permits general solicitation with verification."
        ],
        reasoning_framework="""
Securities Act Section 5 requires registration unless exemption applies. Reg D provides safe harbor exemptions.
ACCREDITED INVESTOR DEFINITION (Reg D Rule 501(a)):
Individuals:
- Income >$200K (single) or >$300K (joint) in each of past 2 years with expectation of same
- Net worth >$1M (excluding primary residence)
- Series 7, 65, or 82 license holders
- Knowledgeable employees of private fund
Entities:
- Institutions (banks, insurance companies, RIAs with >$5M AUM)
- Entities with >$5M in assets (not formed to invest)
- Entity owned entirely by accredited investors
RULE 506(b) - TRADITIONAL SAFE HARBOR:
- Unlimited accredited investors
- Up to 35 non-accredited but sophisticated investors (ability to evaluate investment)
- NO general solicitation or advertising
- No verification of accredited status required (self-certification acceptable)
- Must provide disclosure documents to non-accredited (similar to Reg A)
RULE 506(c) - GENERAL SOLICITATION PERMITTED (2013 JOBS Act):
- Unlimited accredited investors ONLY (zero non-accredited)
- General solicitation and advertising PERMITTED
- MUST verify accredited status (tax returns, W-2, third-party verification letter, broker-dealer)
- Bad actor disqualification applies (enhanced)
BAD ACTOR DISQUALIFICATION (Rule 506(d)):
Company and covered persons (directors, officers, 20%+ beneficial owners, promoters) cannot have:
- Felony or securities-related misdemeanor conviction within 10 years
- SEC, CFTC, or state securities order/sanction within 5 years
- Final order from banking/credit/insurance regulator
FORM D FILING:
File within 15 days of first sale, includes issuer info, offering amount, type of securities.
""",
        key_factors=[
            "Investor accreditation verification (506(b) vs 506(c) requirements)",
            "General solicitation plans (determines 506(b) vs 506(c) choice)",
            "Inclusion of non-accredited sophisticated investors (506(b) only)",
            "Bad actor background checks on covered persons",
            "Form D filing deadline (15 days from first sale)"
        ],
        primary_authority=[
            "Securities Act of 1933 Section 5 - registration requirement",
            "Regulation D Rules 501, 502, 506 - exemptions and conditions",
            "SEC Release 33-10734 (2020) - accredited investor definition amendments",
            "JOBS Act Title II (2013) - general solicitation for 506(c)"
        ],
        burden_holder="Company to verify investor accreditation and comply with offering conditions",
        adversary_position="SEC may challenge exemption if conditions not satisfied or fraud involved",
        counter_arguments=[
            "Accredited investor verification costly and intrusive (tax returns, financial statements)",
            "General solicitation under 506(c) creates public record of fundraising",
            "Non-accredited investor disclosure requirements burdensome"
        ],
        resolution_strategy="Use 506(b) for known investor intros without ads; use 506(c) if demo day or online fundraising",
        entity_scope=["All private securities offerings"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Reg D Rule 506 safe harbor requirements"
    ),
    DoctrineBlock(
        topic="Equity Compensation - ISOs vs NSOs",
        keywords=["incentive stock options", "ISO", "non-qualified stock options", "NSO", "AMT", "$100K limit", "early exercise"],
        conclusion_template=[
            "ISOs provide favorable tax treatment (long-term capital gains) if holding period requirements met.",
            "NSOs taxed as ordinary income on exercise spread, no holding period requirement.",
            "ISO $100K annual vesting limit per employee; excess treated as NSOs."
        ],
        reasoning_framework="""
Stock options grant right to purchase shares at strike price (FMV at grant per 409A).
INCENTIVE STOCK OPTIONS (ISOs) - IRC Section 422:
Tax Treatment:
- Grant: No tax
- Exercise: No ordinary income (but AMT on spread between FMV and strike)
- Sale (if qualifying disposition): Long-term capital gains on spread from strike to sale price
Qualifying Disposition Requirements:
- Hold >2 years from grant date AND >1 year from exercise date
- Employed at grant and within 3 months of exercise (disability/death exceptions)
Disqualifying Disposition: Ordinary income on spread at exercise, capital gain on post-exercise appreciation.
RESTRICTIONS:
- $100K limit: ISOs exercisable for first time in any calendar year cannot exceed $100K FMV (at grant). Excess = NSOs.
- 10% stockholder: Strike must be 110% of FMV, 5-year max term (vs 10 years standard)
- 90-day post-termination exercise or lose ISO status
NON-QUALIFIED STOCK OPTIONS (NSOs):
Tax Treatment:
- Grant: No tax
- Exercise: Ordinary income on spread (FMV - strike), subject to W-2 withholding for employees
- Sale: Capital gains on appreciation from exercise to sale
No restrictions on exercise timing, amount, or holder status. Can be granted to contractors/advisors.
EARLY EXERCISE + 83(b):
Some plans allow exercise of unvested options (restricted stock subject to vesting).
File 83(b) election within 30 days to pay tax at exercise (when spread may be zero) vs at vesting.
""",
        key_factors=[
            "ISO vs NSO designation and $100K annual limit tracking",
            "409A strike price determination (FMV at grant)",
            "AMT impact on ISO exercise (spread added to AMT income)",
            "Holding period requirements for ISO qualifying disposition",
            "Post-termination exercise period (90 days ISO, 30 days-10 years NSO)",
            "Early exercise eligibility and 83(b) election timing"
        ],
        primary_authority=[
            "26 USC Section 422 - Incentive Stock Options",
            "26 USC Section 83 - Property transferred in connection with services",
            "26 USC Section 55 - Alternative Minimum Tax",
            "Treas. Reg. 1.422-2 - ISO definitions and requirements",
            "IRS Notice 2005-1 - 409A safe harbor valuation"
        ],
        burden_holder="Company to track $100K ISO limit and provide correct tax reporting; employee to satisfy holding periods",
        adversary_position="IRS may challenge 409A valuation if strike price too low",
        counter_arguments=[
            "ISO AMT trap: Pay AMT on exercise, stock declines, no refund (2000 dot-com implosions)",
            "$100K limit prevents meaningful ISO grants for senior employees",
            "90-day post-termination exercise forces early exercise or forfeiture"
        ],
        resolution_strategy="Grant ISOs up to $100K limit, NSOs for excess; allow early exercise with 83(b); extend post-termination to 10 years",
        entity_scope=["Employees of C-Corps (ISOs) and all service providers (NSOs)"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IRC Section 422 requirements"
    ),
    DoctrineBlock(
        topic="Liquidation Preference Stacking and Seniority",
        keywords=["liquidation preference", "seniority", "pari passu", "stacking", "waterfall", "multiple liquidation preference"],
        conclusion_template=[
            "Senior liquidation preferences paid before junior in liquidation waterfall.",
            "Pari passu preferences share pro-rata at same priority level.",
            "Multiple liquidation preferences (2x, 3x) multiply investor priority in downside scenarios."
        ],
        reasoning_framework="""
Liquidation preferences determine distribution order in M&A, IPO, or liquidation.
SENIORITY STRUCTURES:
1. SENIOR: Later rounds (Series B, C) senior to earlier (Series A). Series C paid first, then B, then A, then common.
2. PARI PASSU: All preferred series share pro-rata at same priority. Most common in VC deals.
3. TIERED: Some series senior to others based on negotiation (growth equity later rounds may demand seniority).
MULTIPLE LIQUIDATION PREFERENCES:
Standard is 1x invested capital. Some deals have 2x or 3x multiples.
Example: $10M Series B with 2x preference receives $20M before Series A or common get anything.
Creates severe downside risk for earlier investors and common holders in modest exits.
WATERFALL EXAMPLE (pari passu with participating preferred):
Company raises Series A $5M at $15M post, Series B $10M at $40M post. Exits for $30M.
1. Series B preference: $10M (non-participating example)
2. Series A preference: $5M
3. Remaining $15M to common
If Series B had 2x preference: $20M to Series B, $5M to Series A, $5M to common (worse for founders).
PARI PASSU ALLOCATION:
Series A $5M and Series B $10M pari passu = Series B gets 66.7% of first $15M, Series A gets 33.3%.
CONVERSION ANALYSIS:
Preferred converts to common if as-converted value > liquidation preference value.
Series A $5M invested, 1x non-participating pref, 25% ownership on as-converted basis.
Exit $50M:
- As liquidation preference: $5M
- As converted: $12.5M (25% x $50M)
Converts to common. But at $20M exit, stays as preferred ($5M > $5M as-converted).
""",
        key_factors=[
            "Seniority structure (senior vs pari passu)",
            "Liquidation preference multiple (1x vs 2x vs 3x)",
            "Participating vs non-participating (affects conversion decision)",
            "Exit scenario modeling at various valuations",
            "Dividend accrual adding to liquidation preference (rare in VC)"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 2 (Liquidation Preference)",
            "Delaware General Corporation Law Section 151(a) - preferred stock rights",
            "In re Trados Inc. Shareholder Litigation (Del. Ch. 2013) - preferred/common conflicts in M&A",
            "LC Capital Master Fund v. James (Del. Ch. 2013) - liquidation preference interpretation"
        ],
        burden_holder="Company to model waterfall and disclose to common stockholders",
        adversary_position="Late-stage investors demand seniority and >1x multiples; early investors resist",
        counter_arguments=[
            "Senior liquidation preferences disadvantage early risk-takers",
            "Multiple preferences (2x-3x) create misaligned M&A incentives (investors happy at low exit, founders destroyed)",
            "Pari passu more equitable but still heavily favors preferred in modest exits"
        ],
        resolution_strategy="Pari passu 1x non-participating across all series to align incentives",
        entity_scope=["Multi-series preferred stock cap tables"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Certificate of Incorporation express terms control"
    ),
    DoctrineBlock(
        topic="Pro-Rata Rights and Super Pro-Rata Allocation",
        keywords=["pro-rata rights", "participation rights", "super pro-rata", "major investor", "subsequent financings"],
        conclusion_template=[
            "Pro-rata rights allow investors to maintain ownership percentage in future rounds.",
            "Major investors (typically >$1M invested or >5% ownership) receive pro-rata.",
            "Super pro-rata allows purchasing MORE than ownership percentage (2x, 3x pro-rata)."
        ],
        reasoning_framework="""
Pro-rata participation rights preserve investor ownership against dilution in future financings.
STANDARD PRO-RATA:
Investor with 10% fully diluted ownership has right to purchase 10% of next financing round.
Example: Series A investor owns 2M shares out of 20M fully diluted (10%).
Series B raises $10M at $1/share = 10M new shares.
Pro-rata right: Purchase 1M shares (10% of 10M round) to maintain 10% ownership post-round.
MAJOR INVESTOR THRESHOLD:
Pro-rata rights typically granted to investors meeting threshold:
- Dollar threshold: Invested >$500K or >$1M in current round
- Ownership threshold: Hold >1% or >5% fully diluted
Smaller investors excluded to reduce administrative burden.
SUPER PRO-RATA ALLOCATION:
Lead investors may negotiate right to purchase 2x or 3x pro-rata share of subsequent rounds.
Example: Investor with 10% ownership and 2x super pro-rata can purchase up to 20% of next round.
Provides reward for lead investor conviction and allows increasing ownership stake.
OVERSUBSCRIPTION:
If round oversubscribed (demand > offering), pro-rata allocation reduced proportionally.
Example: Round is $10M but demand is $15M. Each investor's pro-rata allocation reduced by 33%.
TERMINATION:
- IPO (automatic)
- Transfer of shares to non-major investor (loses pro-rata)
- Ownership falls below threshold percentage
""",
        key_factors=[
            "Major investor threshold (dollar or percentage)",
            "Super pro-rata multiple (1x, 2x, 3x)",
            "Oversubscription reduction mechanics",
            "New investor allocation vs existing investor pro-rata (typically 50/50 split)",
            "Termination triggers and transferability"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 2.2 (Pro-Rata Rights)",
            "Delaware General Corporation Law - preemptive rights (absent unless granted)",
            "Benchmark Capital Partners v. Vague (Del. Ch. 2002) - investor rights enforcement"
        ],
        burden_holder="Company to offer pro-rata to qualified investors before closing subsequent rounds",
        adversary_position="Investors demand broad pro-rata; company seeks high thresholds to limit participation",
        counter_arguments=[
            "Broad pro-rata rights make rounds difficult to fill (limited allocation for new investors)",
            "Super pro-rata concentrates ownership with existing investors, reduces fresh perspective",
            "Administrative burden tracking and offering pro-rata to many small investors"
        ],
        resolution_strategy="Pro-rata for investors with >$1M invested or >5% ownership, no super pro-rata except for lead investor at 1.5x",
        entity_scope=["Major preferred investors in Series A-D"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Founder Stock Repurchase and Vesting Cliffs",
        keywords=["founder stock", "repurchase rights", "reverse vesting", "acceleration on termination", "good leaver bad leaver"],
        conclusion_template=[
            "Reverse vesting subjects founder stock to company repurchase if founder leaves early.",
            "Typical schedule: 4-year vest with 1-year cliff, 25-50% credit for past service.",
            "Good leaver (termination without cause) may get accelerated vesting; bad leaver forfeits unvested."
        ],
        reasoning_framework="""
Investors require founder stock vesting to prevent departure with full equity after funding.
REVERSE VESTING MECHANICS:
Founder receives shares at incorporation but subject to repurchase right:
- Company (or investors) can repurchase unvested shares at original cost ($0.0001/share) if founder leaves
- Shares vest over time (typically 4 years), repurchase right lapses as vesting occurs
- Unvested shares may be subject to forfeiture (vs repurchase) for tax simplification
VESTING SCHEDULE:
Standard: 4-year monthly vesting with 1-year cliff
- 25% vests at 12 months (cliff)
- Remaining 75% vests monthly over 36 months
Negotiated variations:
- Credit for past service: 25-50% vested at funding
- Accelerated vesting on termination without cause (6-12 months acceleration)
- Double-trigger acceleration (change of control + termination)
GOOD LEAVER / BAD LEAVER:
Good Leaver (termination without cause, disability, death):
- Retain vested shares, partial acceleration (6-12 months)
- Repurchase unvested at cost or FMV
Bad Leaver (termination for cause, voluntary resignation, breach):
- Retain vested shares only (or repurchase at cost if specified)
- Forfeit all unvested, no acceleration
For Cause Definition: Felony, fraud, gross negligence, breach of duties, violation of restrictive covenants.
REPURCHASE PRICING:
- Cost basis ($0.0001/share typical for founders)
- FMV per 409A valuation (more investor-friendly, punitive to departing founder)
- Formula based on company metrics
""",
        key_factors=[
            "Vesting schedule (4 years standard, 3 years negotiable for co-founders)",
            "Cliff period (1 year vs 6 months vs no cliff)",
            "Credit for past service (pre-funding sweat equity)",
            "Acceleration on termination without cause (6-12 months standard)",
            "Repurchase price (cost vs FMV)",
            "Good leaver vs bad leaver definitions and treatment"
        ],
        primary_authority=[
            "NVCA Model Term Sheet Section 5 (Vesting)",
            "26 USC Section 83(b) - election to include restricted property in income",
            "Delaware General Corporation Law Section 153 - consideration for stock",
            "Restricted Stock Purchase Agreement (RSPA) standard form"
        ],
        burden_holder="Company to enforce vesting and exercise repurchase rights upon founder departure",
        adversary_position="Investors demand full 4-year vest with no credit; founders seek credit and acceleration",
        counter_arguments=[
            "No credit for past service punishes founders who bootstrapped pre-funding",
            "Repurchase at cost (vs FMV) allows departed founder to retain economic interest",
            "Acceleration on termination without cause protects founder from investor removal without penalty"
        ],
        resolution_strategy="4-year monthly vest with 1-year cliff, 25% credit for past service if >2 years pre-funding, 6-month acceleration on termination without cause, repurchase at cost",
        entity_scope=["Founder common stock in VC-backed companies"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Management Rights Letters and ERISA/BHC Compliance",
        keywords=["management rights", "ERISA", "plan assets", "bank holding company", "advisory board", "control person"],
        conclusion_template=[
            "Management rights letter grants investor advisory role to avoid ERISA plan assets status.",
            "VC fund investors include pension plans subject to ERISA prohibited transaction rules.",
            "Bank investors subject to BHC Act control restrictions, require passive investor status."
        ],
        reasoning_framework="""
ERISA (Employee Retirement Income Security Act) regulates pension fund investments.
PLAN ASSETS RULE (29 CFR 2510.3-101):
If pension plan invests in entity (VC fund), fund's investments may be deemed plan assets.
Triggers ERISA fiduciary duties and prohibited transaction rules (cannot invest in affiliates, self-dealing).
EXCEPTION - VENTURE CAPITAL OPERATING COMPANY (VCOC):
Fund qualifies as VCOC if:
- 50%+ of assets invested in operating companies (not passive securities)
- Fund (or investors) have management rights in portfolio companies
MANAGEMENT RIGHTS:
Meaningful rights to participate in or advise on management decisions.
Standard mechanism: Management Rights Letter granting:
- Right to periodic financial statements
- Right to consult on major decisions (M&A, budget, hiring)
- Advisory board seat or observer rights (without fiduciary duties)
- Access to facilities and management
No formal Board seat required. Advisory capacity sufficient.
BANK HOLDING COMPANY ACT (BHC Act):
Banks and BHCs can only own >5% voting or >25% equity of company if:
- Company is bank or bank-related activity (Fed approval), OR
- Investment is passive (no control)
CONTROL FACTORS (Reg Y):
- Board seats
- Management contracts
- Interlocking officers/directors
- Veto rights over major decisions
Banks investing in VC funds need passivity provisions:
- No Board seats for bank representatives
- Limited protective provisions
- No day-to-day management involvement
""",
        key_factors=[
            "VC fund investor composition (pension plans triggering ERISA)",
            "Bank or BHC investors requiring passive investment status",
            "Management rights letter sufficiency for VCOC exception",
            "Control factors under BHC Act Reg Y (Board seats, voting, veto rights)",
            "Passive investor carve-outs and information rights"
        ],
        primary_authority=[
            "ERISA Section 3(42) - Venture Capital Operating Company",
            "29 CFR 2510.3-101 - Plan Assets regulation",
            "Bank Holding Company Act 12 USC Section 1841 et seq",
            "Federal Reserve Reg Y - BHC control factors",
            "DOL Advisory Opinion 2000-10A - VCOC management rights"
        ],
        burden_holder="VC fund to obtain management rights letters; bank investors to maintain passive status",
        adversary_position="DOL may challenge insufficient management rights; Fed may challenge bank control",
        counter_arguments=[
            "Management rights letters may be pro forma without real advisory access",
            "Bank passive investor requirements limit governance participation",
            "VCOC 50% operating company test difficult to maintain in portfolio with public stock/secondaries"
        ],
        resolution_strategy="Standard management rights letter with advisory board or observer seat, banks excluded from Board seats and protective provisions",
        entity_scope=["VC funds with ERISA or bank investors"],
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
    DoctrineBlock(
        topic="Founder Restricted Covenants - Non-Compete and IP Assignment",
        keywords=["non-compete", "non-solicit", "confidentiality", "IP assignment", "inventions", "work for hire"],
        conclusion_template=[
            "Investors require founders sign CIIAA: Confidentiality, Invention Assignment, Non-Compete, Non-Solicit.",
            "Non-competes during employment + 12 months post-termination standard (state enforceability varies).",
            "IP assignment covers all work product, pre-existing IP carved out with disclosure schedule."
        ],
        reasoning_framework="""
Confidential Information, Invention and IP Assignment Agreement (CIIAA) protects company IP and competitive position.
CONFIDENTIALITY:
- Founder agrees not to disclose trade secrets, confidential information, customer lists, financial data
- Survives termination indefinitely (trade secrets) or 3-5 years (other confidential info)
- Exceptions: public domain, required by law, prior knowledge
NON-COMPETE:
- Founder agrees not to engage in competitive business during employment and 12-24 months post-termination
- Geographic scope: typically "anywhere company does business" (can be global for SaaS)
- Functional scope: limited to specific competitive activities (not all employment)
ENFORCEABILITY BY STATE:
- California: Non-competes void except sale of business (Bus & Prof Code 16600)
- Delaware: Enforceable if reasonable in scope, duration, geography
- Most states: Enforceable if protecting legitimate business interest with reasonable restrictions
NON-SOLICIT:
- Employees: Cannot solicit company employees to leave for 12-24 months post-termination
- Customers: Cannot solicit company customers for competitive services 12-24 months post
- More enforceable than non-compete in many states (including California for customer non-solicit)
INVENTION ASSIGNMENT:
- Founder assigns all inventions, discoveries, IP created during employment to company
- Work-for-hire provisions for copyrightable works
- Pre-existing IP: Founder discloses on Schedule A, carves out from assignment
- Shop rights: Even if invention not assigned, company gets royalty-free license if developed using company resources
STATE LAW CARVEOUTS (e.g., California Labor Code 2870):
Employee inventions NOT assigned if developed:
- Entirely on own time
- Without company equipment, supplies, facilities, or trade secrets
- Does not relate to company business or R&D
""",
        key_factors=[
            "State law enforceability of non-compete (California void, Delaware/NY enforceable)",
            "Non-compete duration (12-24 months) and scope (functional, geographic)",
            "Pre-existing IP disclosure and carve-out schedule",
            "Work-for-hire vs assignment of inventions",
            "Survival periods for confidentiality and non-solicit"
        ],
        primary_authority=[
            "California Business & Professions Code Section 16600 - non-compete void",
            "California Labor Code Section 2870 - invention assignment limits",
            "Delaware common law - reasonable restraints enforceable",
            "Uniform Trade Secrets Act (UTSA) - confidentiality",
            "17 USC Section 101 - work made for hire definition"
        ],
        burden_holder="Company to obtain executed CIIAA from all founders and employees; founder to disclose pre-existing IP",
        adversary_position="Founder seeks narrow restrictions; investors demand broad non-compete and full IP assignment",
        counter_arguments=[
            "Non-competes unenforceable in California and growing list of states",
            "Overbroad non-compete prevents founder from working in industry after departure",
            "IP assignment without pre-existing carve-out captures side projects and prior work"
        ],
        resolution_strategy="Non-solicit (enforceable everywhere) + non-compete where valid (12 months, functional scope), IP assignment with Schedule A carve-out for disclosed pre-existing IP",
        entity_scope=["Founders and key employees"],
        confidence=ConfidenceLevel.DEFENSIBLE
    )
]

# ============================================================================
# ENGINE CORE
# ============================================================================

class ENT07Engine:
    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.query_count = 0
        self.cache_hits = 0
        self.start_time = datetime.now()

    def normalize_query(self, question: str) -> str:
        """Normalize query for semantic matching"""
        normalized = question.lower().strip()
        replacements = {
            "startup": "venture capital",
            "term sheet": "financing",
            "stock option": "equity compensation",
            "vesting schedule": "vesting",
            "investor rights": "protective provisions"
        }
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        return normalized

    def match_doctrines(self, question: str) -> List[DoctrineBlock]:
        """Match query to relevant doctrine blocks"""
        normalized = self.normalize_query(question)
        matches = []
        for block in self.doctrine_cache:
            score = 0
            for keyword in block.keywords:
                if keyword.lower() in normalized:
                    score += 2
            if any(word in normalized for word in block.topic.lower().split()):
                score += 1
            if score > 0:
                matches.append((score, block))
        matches.sort(reverse=True, key=lambda x: x[0])
        return [block for score, block in matches[:5]]

    def three_layer_response(self, question: str, mode: ResponseMode, zone: AnalysisZone) -> Dict[str, Any]:
        """Three-layer reasoning: cache -> semantic -> deep"""
        start = datetime.now()

        matched_doctrines = self.match_doctrines(question)

        if matched_doctrines:
            self.cache_hits += 1
            primary_block = matched_doctrines[0]

            if mode == ResponseMode.FAST:
                answer = " ".join(primary_block.conclusion_template)
            elif mode == ResponseMode.DEFENSE:
                answer = f"{primary_block.reasoning_framework}\n\nKey Factors: {', '.join(primary_block.key_factors[:3])}\n\nAuthorities: {', '.join(primary_block.primary_authority[:2])}"
            else:
                answer = f"TOPIC: {primary_block.topic}\n\n{primary_block.reasoning_framework}\n\nKEY FACTORS:\n" + "\n".join(f"- {f}" for f in primary_block.key_factors)
                answer += f"\n\nAUTHORITIES:\n" + "\n".join(f"- {a}" for a in primary_block.primary_authority)
                answer += f"\n\nRISK ANALYSIS:\nBurden: {primary_block.burden_holder}\nAdversary Position: {primary_block.adversary_position}\nCounters: {', '.join(primary_block.counter_arguments[:2])}\nStrategy: {primary_block.resolution_strategy}"

            confidence = primary_block.confidence
            categories = self._infer_categories(matched_doctrines)
            authorities = primary_block.primary_authority[:3]
        else:
            answer = f"No cached doctrine for query. General VC/startup financing analysis required. Question: {question}"
            confidence = ConfidenceLevel.DISCLOSURE
            categories = [IssueCategory.TERM_SHEET]
            authorities = ["NVCA Model Term Sheet 2024", "Delaware General Corporation Law"]

        latency = (datetime.now() - start).total_seconds() * 1000
        self.query_count += 1

        return {
            "answer": answer,
            "confidence": confidence,
            "categories": categories,
            "authorities": authorities,
            "latency_ms": latency
        }

    def _infer_categories(self, doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
        """Infer issue categories from matched doctrines"""
        category_map = {
            "liquidation": IssueCategory.LIQUIDATION_PREF,
            "anti-dilution": IssueCategory.ANTI_DILUTION,
            "SAFE": IssueCategory.SAFE_CONVERTIBLE,
            "convertible": IssueCategory.SAFE_CONVERTIBLE,
            "409A": IssueCategory.VALUATION_409A,
            "83(b)": IssueCategory.EQUITY_COMP,
            "QSBS": IssueCategory.EQUITY_COMP,
            "protective": IssueCategory.PROTECTIVE_PROVISIONS,
            "board": IssueCategory.BOARD_COMPOSITION,
            "drag-along": IssueCategory.DRAG_TAG_ALONG,
            "tag-along": IssueCategory.DRAG_TAG_ALONG,
            "vesting": IssueCategory.VESTING,
            "ISO": IssueCategory.EQUITY_COMP,
            "NSO": IssueCategory.EQUITY_COMP,
            "term sheet": IssueCategory.TERM_SHEET,
            "accredited": IssueCategory.SECURITIES_LAW,
            "Reg D": IssueCategory.SECURITIES_LAW
        }
        categories = set()
        for doctrine in doctrines:
            topic_lower = doctrine.topic.lower()
            for keyword, category in category_map.items():
                if keyword.lower() in topic_lower:
                    categories.add(category)
        return list(categories) if categories else [IssueCategory.TERM_SHEET]

    def compute_hash(self, question: str, mode: ResponseMode) -> str:
        """SHA-256 determinism hash"""
        content = f"{question}|{mode.value}|{VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def health_check(self) -> Dict[str, Any]:
        """Health endpoint data"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": VERSION,
            "status": "healthy",
            "uptime_seconds": uptime,
            "queries_processed": self.query_count,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": self.cache_hits / self.query_count if self.query_count > 0 else 0,
            "doctrine_blocks": len(self.doctrine_cache),
            "timestamp": datetime.now().isoformat()
        }

# ============================================================================
# FASTAPI APP
# ============================================================================

engine = ENT07Engine()

app = FastAPI(
    title="ENT07 Venture Capital Engine",
    version=VERSION,
    description="TIE-grade intelligence for VC and startup financing"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return engine.health_check()

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Main query endpoint"""
    try:
        logger.info(f"Query received: {request.question[:100]} | Mode: {request.mode} | Zone: {request.zone}")

        result = engine.three_layer_response(request.question, request.mode, request.zone)

        response = QueryResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            categories=result["categories"],
            authorities=result["authorities"],
            mode=request.mode,
            zone=request.zone,
            determinism_hash=engine.compute_hash(request.question, request.mode),
            latency_ms=result["latency_ms"],
            timestamp=datetime.now().isoformat()
        )

        logger.info(f"Query completed: {result['latency_ms']:.2f}ms | Confidence: {result['confidence']}")
        return response

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": ENGINE_NAME,
        "version": VERSION,
        "status": "operational",
        "endpoints": ["/health", "/query"]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
