"""
LG12 Bankruptcy Law Engine - Doctrine Cache Module
=====================================================
Pre-compiled bankruptcy doctrine blocks for instant retrieval on common
chapter selection, means test, automatic stay, discharge, exemption,
avoidance action, plan confirmation, adversary proceeding, trustee power,
cramdown, lien stripping, reaffirmation, and Texas-specific queries.

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
Engine: LG12 Bankruptcy Law
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
    """A single pre-compiled bankruptcy doctrine cache entry."""

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
    texas_notes: str = ""

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
            "texas_notes": self.texas_notes,
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
            " ".join(self.related_topics),
            " ".join(self.practice_tips),
            " ".join(self.risk_factors),
            self.texas_notes,
        ]
        return " ".join(p for p in parts if p)


# ============================================================================
# DOCTRINE CACHE INDEX
# ============================================================================

class DoctrineCacheIndex:
    """Fast O(1) lookup index over doctrine cache blocks."""

    def __init__(self) -> None:
        self._by_topic: Dict[str, DoctrineCacheBlock] = {}
        self._by_category: Dict[str, List[DoctrineCacheBlock]] = {}
        self._by_subcategory: Dict[str, List[DoctrineCacheBlock]] = {}
        self._all_topics: List[str] = []
        self._all_categories: Set[str] = set()
        self._build_time_ms: float = 0.0

    def build(self, blocks: List[DoctrineCacheBlock]) -> None:
        """Build the index from a list of blocks."""
        start = time.monotonic()
        self._by_topic.clear()
        self._by_category.clear()
        self._by_subcategory.clear()
        self._all_topics.clear()
        self._all_categories.clear()
        for block in blocks:
            self._by_topic[block.topic] = block
            self._all_topics.append(block.topic)
            self._all_categories.add(block.category)
            if block.category not in self._by_category:
                self._by_category[block.category] = []
            self._by_category[block.category].append(block)
            if block.subcategory:
                if block.subcategory not in self._by_subcategory:
                    self._by_subcategory[block.subcategory] = []
                self._by_subcategory[block.subcategory].append(block)
        self._build_time_ms = (time.monotonic() - start) * 1000.0
        logger.info(
            f"DoctrineCacheIndex built: {len(blocks)} blocks, "
            f"{len(self._all_categories)} categories, {self._build_time_ms:.1f}ms"
        )

    def get(self, topic: str) -> Optional[DoctrineCacheBlock]:
        """Get a block by topic name."""
        return self._by_topic.get(topic)

    def get_by_category(self, category: str) -> List[DoctrineCacheBlock]:
        """Get all blocks in a category."""
        return self._by_category.get(category, [])

    def get_by_subcategory(self, subcategory: str) -> List[DoctrineCacheBlock]:
        """Get all blocks in a subcategory."""
        return self._by_subcategory.get(subcategory, [])

    def all_topics(self) -> List[str]:
        """Return all topic names."""
        return list(self._all_topics)

    def all_categories(self) -> Set[str]:
        """Return all category names."""
        return set(self._all_categories)

    def stats(self) -> Dict[str, Any]:
        """Return index statistics."""
        return {
            "total_blocks": len(self._by_topic),
            "categories": sorted(self._all_categories),
            "category_count": len(self._all_categories),
            "build_time_ms": round(self._build_time_ms, 3),
        }


# ============================================================================
# DOCTRINE BLOCKS - COMPREHENSIVE BANKRUPTCY LAW CACHE
# ============================================================================

DOCTRINE_BLOCKS: List[DoctrineCacheBlock] = [
    # ========== CHAPTER 7 LIQUIDATION ==========
    DoctrineCacheBlock(
        topic="chapter_7_liquidation_overview",
        summary="Chapter 7 provides for liquidation of a debtor's nonexempt assets by a trustee, with distribution to creditors according to statutory priority. Individual debtors receive a discharge of most pre-petition debts. BAPCPA (2005) added the means test to limit access by debtors with ability to repay. The process typically completes in 3-6 months from filing to discharge.",
        key_statutes=["11 USC 701-784", "11 USC 707(b)", "11 USC 726", "11 USC 727"],
        elements=[
            "Eligibility: Individual, partnership, corporation (not railroad, bank, insurance, S&L, credit union)",
            "Filing: Voluntary petition with schedules, SOFA, means test form, credit counseling certificate",
            "Automatic stay triggered upon filing under 362",
            "Trustee appointed from panel under 701 to administer case",
            "341 meeting of creditors within 20-40 days of filing",
            "Trustee investigates assets, examines debtor under oath",
            "Nonexempt assets liquidated, proceeds distributed per 726 priority",
            "Discharge entered approximately 60 days after 341 meeting if no objection",
            "Debtor must complete financial management course before discharge",
        ],
        defenses=[
            "Below-median income (means test safe harbor under 707(b)(7))",
            "Disabled veteran exemption from means test",
            "Non-consumer debts exceed 50% of total scheduled debts",
            "Special circumstances demonstrating no abuse under 707(b)(2)(B)",
            "Totality of circumstances does not show abuse under 707(b)(3)",
        ],
        remedies=[
            "Discharge of qualifying pre-petition debts under 727",
            "Fresh start for individual debtor",
            "Exemption of protected assets from liquidation",
            "Automatic stay protection during pendency",
        ],
        leading_cases=[
            "Marrama v. Citizens Bank, 549 U.S. 365 (2007) - conversion right limitations",
            "Ransom v. FIA Card Services, 562 U.S. 61 (2011) - means test vehicle ownership deduction",
            "Hamilton v. Lanning, 560 U.S. 505 (2010) - projected disposable income forward-looking",
            "Milavetz v. United States, 559 U.S. 229 (2010) - attorney as debt relief agency under BAPCPA",
        ],
        category="chapter_types",
        subcategory="chapter_7",
        authority_score=0.95,
        confidence=0.92,
        related_topics=["means_test", "exemptions", "discharge", "trustee_powers"],
        practice_tips=[
            "Always run means test before advising Chapter 7 eligibility",
            "Check for prior discharges within 8 years (727(a)(8))",
            "Review all asset transfers in 2 years prior for avoidance risk",
            "Ensure credit counseling certificate is obtained pre-filing",
        ],
        risk_factors=[
            "Means test presumption of abuse triggers UST review",
            "Pre-filing asset transfers may be avoided",
            "Prior Chapter 7 discharge within 8 years bars new discharge",
            "Failure to disclose assets can lead to denial of discharge under 727(a)(2)",
        ],
        texas_notes="Texas debtors must use state exemptions (opt-out state). Texas unlimited homestead exemption is a major advantage. 2-year domicile requirement for state exemptions under BAPCPA 522(b)(3)(A). Homestead cap of $189,050 for property acquired within 1215 days (3 1/3 years) before filing under 522(p).",
    ),

    # ========== CHAPTER 11 REORGANIZATION ==========
    DoctrineCacheBlock(
        topic="chapter_11_reorganization_overview",
        summary="Chapter 11 enables business debtors (and qualifying individuals) to reorganize debts through a plan of reorganization while continuing operations as a debtor-in-possession. The plan must be accepted by creditor classes or crammed down. Subchapter V (SBRA) provides streamlined process for small business debtors with debts under $7.5M.",
        key_statutes=["11 USC 1101-1174", "11 USC 1181-1195 (Sub V)", "11 USC 1121-1129"],
        elements=[
            "DIP status: Debtor operates business with trustee powers under 1107",
            "Exclusivity period for filing plan (120 days, extendable to 18 months)",
            "Disclosure statement with adequate information under 1125",
            "Plan classification of claims and interests under 1122",
            "Solicitation of votes from impaired classes",
            "Confirmation requirements under 1129(a) (consensual) or 1129(b) (cramdown)",
            "Best interests test: each holder gets at least Chapter 7 liquidation value",
            "Feasibility: plan not likely to be followed by further liquidation",
            "Good faith: plan proposed in good faith, not by means forbidden by law",
        ],
        defenses=[
            "Administrative insolvency (insufficient funds to confirm plan)",
            "Lack of feasibility — plan projections unrealistic",
            "Bad faith filing (filed for improper purpose)",
            "Single asset real estate debtor limitations under 362(d)(3)",
        ],
        remedies=[
            "Restructuring of debts with reduced payments",
            "Extension of debt maturity dates",
            "Asset sales free and clear under 363(f)",
            "Assumption or rejection of executory contracts under 365",
            "Fresh start for individual Chapter 11 debtors",
        ],
        leading_cases=[
            "Bank of America v. 203 North LaSalle, 526 U.S. 434 (1999) - new value exception to APR",
            "Till v. SCS Credit Corp., 541 U.S. 465 (2004) - cramdown interest rate (formula approach)",
            "RadLAX Gateway Hotel v. Amalgamated Bank, 566 U.S. 639 (2012) - credit bidding rights",
            "Czyzewski v. Jevic Holding Corp., 580 U.S. 451 (2017) - structured dismissals and priority rules",
        ],
        category="chapter_types",
        subcategory="chapter_11",
        authority_score=0.95,
        confidence=0.90,
        related_topics=["plan_confirmation", "cramdown", "dip_financing", "disclosure_statement", "absolute_priority_rule"],
        practice_tips=[
            "File first day motions for cash collateral, DIP financing, critical vendor payments",
            "Subchapter V eliminates need for disclosure statement and absolute priority rule",
            "Monitor exclusivity deadlines closely — loss of exclusivity invites competing plans",
            "Adequate protection payments typically required for use of cash collateral",
        ],
        risk_factors=[
            "High administrative costs may consume estate value",
            "Loss of exclusivity allows creditors to file competing plans",
            "Conversion to Chapter 7 if reorganization not feasible",
            "US Trustee may seek appointment of Chapter 11 trustee for cause",
        ],
        texas_notes="Western District of Texas (Midland division) handles significant oil/gas bankruptcy cases. Local rules require 14-day notice for most motions. Texas is a deed of trust state — impacts foreclosure timeline in cases.",
    ),

    # ========== CHAPTER 13 WAGE EARNER ==========
    DoctrineCacheBlock(
        topic="chapter_13_wage_earner_plan",
        summary="Chapter 13 allows individual debtors with regular income to propose a 3-5 year repayment plan to creditors. Debtors retain property while making payments through a standing trustee. Plan must commit all projected disposable income (below-median: 36 months, above-median: 60 months). Chapter 13 offers advantages including mortgage cure, lien stripping, and co-debtor stay.",
        key_statutes=["11 USC 1301-1330", "11 USC 1322", "11 USC 1325", "11 USC 1328"],
        elements=[
            "Eligibility: Individual with regular income; secured debts under $2,750,000 and unsecured under $2,750,000",
            "Good faith plan under 1325(a)(3)",
            "Best interests test: unsecured creditors receive at least Chapter 7 liquidation value",
            "Disposable income test: commit all projected disposable income for applicable commitment period",
            "Below-median debtors: 36-month minimum plan",
            "Above-median debtors: 60-month plan required",
            "Current on all post-petition domestic support obligations",
            "All tax returns filed for 4 years pre-filing",
            "Secured claims paid present value of collateral or surrendered",
        ],
        defenses=[
            "Inability to make plan payments due to changed circumstances",
            "Plan not proposed in good faith (e.g., minimal payment to unsecured)",
            "Failure to meet best interests test",
        ],
        remedies=[
            "Mortgage cure and reinstatement under 1322(b)(5)",
            "Lien stripping of wholly unsecured junior liens under 506(a)",
            "Co-debtor stay protection under 1301",
            "Cramdown of secured claims to collateral value",
            "Broader discharge than Chapter 7 (historically, narrowed by BAPCPA)",
            "Hardship discharge under 1328(b) if modification not practicable",
        ],
        leading_cases=[
            "Hamilton v. Lanning, 560 U.S. 505 (2010) - projected disposable income is forward-looking",
            "Nobelman v. American Savings Bank, 508 U.S. 324 (1993) - anti-modification of principal residence mortgages",
            "Bank of America v. Caulkett, 575 U.S. 790 (2015) - cannot strip partially secured junior lien in Ch 7",
            "Johnson v. Home State Bank, 501 U.S. 78 (1991) - mortgage lien survives Chapter 7 discharge",
        ],
        category="chapter_types",
        subcategory="chapter_13",
        authority_score=0.93,
        confidence=0.90,
        related_topics=["lien_stripping", "mortgage_cure", "disposable_income", "codebtor_stay", "chapter_20"],
        practice_tips=[
            "Calculate projected disposable income using forward-looking approach per Lanning",
            "Lien stripping requires bifurcation motion or plan provision plus confirmation",
            "Chapter 20 strategy: Ch 7 discharge then Ch 13 to strip liens (no Ch 13 discharge required for lien strip)",
            "Standing trustee percentage (typically 4-10%) must be factored into plan payments",
        ],
        risk_factors=[
            "60-month commitment for above-median debtors is substantial",
            "Dismissal or conversion if payments missed",
            "Cannot modify principal residence mortgage (anti-modification rule)",
            "Co-debtor stay only applies to consumer debts",
        ],
        texas_notes="Western District of Texas standing trustee offices in San Antonio and Austin. Mortgage cure is critical in Texas given nonjudicial foreclosure speed. Texas unlimited homestead means less nonexempt property to satisfy best interests test.",
    ),

    # ========== CHAPTER 12 FAMILY FARMER ==========
    DoctrineCacheBlock(
        topic="chapter_12_family_farmer",
        summary="Chapter 12 provides debt adjustment for family farmers and family fishermen with regular annual income. Similar to Chapter 13 but with higher debt limits and provisions tailored to agricultural operations including seasonal income fluctuations. Family farmer debt limit is $11,097,350 with 50% farm income requirement.",
        key_statutes=["11 USC 1201-1231", "11 USC 101(18)-(21)"],
        elements=[
            "Family farmer: individual/couple with aggregate debts under $11,097,350",
            "At least 50% of debts arise from farming operations",
            "More than 50% of gross income in preceding tax year from farming",
            "Regular annual income sufficient to make plan payments",
            "Plan filed within 90 days of order for relief",
            "Plan may modify secured and unsecured claims including home mortgage",
        ],
        defenses=[
            "Debtor does not meet definition of family farmer",
            "Debts exceed statutory limit",
            "Income does not meet 50% farming threshold",
        ],
        remedies=[
            "Restructuring of farm debt over plan period",
            "Modification of secured claims including farmland mortgage",
            "Seasonal payment scheduling to match crop/livestock cycles",
            "Cramdown of secured claims to collateral value",
        ],
        leading_cases=[
            "Hall v. United States, 566 U.S. 506 (2012) - post-petition tax liability in Chapter 12",
            "In re Gage, 394 B.R. 184 (Bankr. M.D. Ga. 2008) - family farmer definition",
        ],
        category="chapter_types",
        subcategory="chapter_12",
        authority_score=0.80,
        confidence=0.82,
        related_topics=["plan_confirmation", "secured_claim_modification", "seasonal_income"],
        practice_tips=[
            "Chapter 12 allows modification of home mortgage (unlike Chapter 13)",
            "Seasonal payment provisions are critical for agricultural debtors",
            "50% income test looks at preceding tax year — timing of filing matters",
        ],
        texas_notes="Texas agriculture (cattle, cotton, oil/gas related) creates significant Chapter 12 filings. Permian Basin oilfield service companies may qualify if farming/ranching income meets threshold.",
    ),

    # ========== CHAPTER 15 CROSS-BORDER ==========
    DoctrineCacheBlock(
        topic="chapter_15_cross_border_insolvency",
        summary="Chapter 15 provides the mechanism for U.S. recognition of foreign insolvency proceedings and cooperation between U.S. and foreign courts. Based on the UNCITRAL Model Law, it enables foreign representatives to access U.S. courts and obtain relief. Key determination is the debtor's center of main interests (COMI).",
        key_statutes=["11 USC 1501-1532", "UNCITRAL Model Law on Cross-Border Insolvency"],
        elements=[
            "Foreign representative files petition for recognition",
            "Court determines if proceeding is foreign main or foreign nonmain",
            "COMI determination: where debtor conducts administration of interests on regular basis",
            "Presumption: COMI is registered office unless rebutted",
            "Recognition of foreign main proceeding triggers automatic stay equivalent",
            "Foreign nonmain proceeding: court may grant discretionary relief",
        ],
        defenses=[
            "Public policy exception under 1506",
            "Debtor's COMI is actually in the United States",
            "Foreign proceeding does not meet Chapter 15 requirements",
        ],
        remedies=[
            "Stay of proceedings against debtor's U.S. assets",
            "Turnover of U.S. assets to foreign representative",
            "Cooperation and coordination with foreign courts",
            "Authority to examine witnesses and take evidence",
        ],
        leading_cases=[
            "In re Brit. Am. Ins. Co., 488 B.R. 205 (Bankr. S.D. Fla. 2013) - COMI analysis",
            "In re Bear Stearns High-Grade Structured Credit Strategies Master Fund, 389 B.R. 325 (Bankr. S.D.N.Y. 2008) - COMI factors",
        ],
        category="chapter_types",
        subcategory="chapter_15",
        authority_score=0.78,
        confidence=0.78,
        related_topics=["comi_determination", "foreign_representative", "comity"],
        practice_tips=[
            "COMI analysis focuses on where third parties perceive administration occurs",
            "Multiple Chapter 15 cases may be filed in different districts for same debtor group",
            "U.S. counsel needed even though proceeding is ancillary",
        ],
    ),

    # ========== MEANS TEST ==========
    DoctrineCacheBlock(
        topic="means_test_calculation",
        summary="The means test under 707(b)(2) determines whether a Chapter 7 filing constitutes abuse for above-median income debtors. Current monthly income (CMI) averaged over 6 months pre-filing is annualized and compared to state median. If above median, allowed deductions are subtracted to determine presumption of abuse. BAPCPA Form 122A-2 implements the calculation.",
        key_statutes=["11 USC 707(b)(2)", "11 USC 707(b)(7)", "11 USC 101(10A)"],
        elements=[
            "Calculate current monthly income (CMI) per 101(10A): 6-month lookback average",
            "CMI includes all sources except Social Security benefits",
            "Annualize CMI and compare to applicable state median for household size",
            "Below median: no presumption of abuse (safe harbor under 707(b)(7))",
            "Above median: apply IRS National/Local Standards deductions",
            "Calculate monthly disposable income after allowed deductions",
            "Multiply by 60 months: >$12,850 = presumption; $7,700-$12,850 = 25% test; <$7,700 = no presumption",
        ],
        defenses=[
            "Below state median income safe harbor",
            "Disabled veteran exemption",
            "Reservist/National Guard exemption after qualifying service",
            "Primarily non-consumer debts (>50%)",
            "Special circumstances to rebut presumption (medical condition, called to active duty)",
        ],
        remedies=[
            "If no presumption: Chapter 7 filing proceeds",
            "If presumption arises: rebut with special circumstances or convert to Chapter 13",
            "UST motion to dismiss under 707(b)(1) (totality of circumstances)",
        ],
        leading_cases=[
            "Ransom v. FIA Card Services, 562 U.S. 61 (2011) - vehicle ownership deduction requires actual payment",
            "Hamilton v. Lanning, 560 U.S. 505 (2010) - forward-looking approach to disposable income",
            "Baud v. Carroll, 634 F.3d 327 (6th Cir. 2011) - Social Security exclusion from CMI",
        ],
        category="eligibility",
        subcategory="means_test",
        authority_score=0.92,
        confidence=0.90,
        related_topics=["chapter_7_liquidation_overview", "disposable_income", "median_income"],
        practice_tips=[
            "Run means test for every potential Chapter 7 filer regardless of apparent income level",
            "6-month lookback can be advantageous: time filing to avoid high-income months",
            "Social Security income excluded from CMI but appears on schedule I",
            "Marital adjustment for non-filing spouse income under 707(b)(2)(C)(ii)",
        ],
        risk_factors=[
            "Inaccurate income reporting can lead to denial of discharge",
            "UST actively reviews above-median cases",
            "Bonus or overtime income in lookback period inflates CMI",
        ],
        texas_notes="Texas median income updated periodically by Census Bureau. Midland-Odessa area may have higher actual income than state median due to oil/gas industry. Housing allowance for TX varies by county.",
    ),

    # ========== AUTOMATIC STAY ==========
    DoctrineCacheBlock(
        topic="automatic_stay_362",
        summary="The automatic stay under Section 362 is one of the most powerful protections in bankruptcy. It immediately halts virtually all collection actions, lawsuits, foreclosures, repossessions, and utility disconnections upon filing. BAPCPA added limitations for serial filers: 30-day stay for second filing in 1 year, no stay for third filing in 1 year.",
        key_statutes=["11 USC 362(a)", "11 USC 362(b)", "11 USC 362(c)", "11 USC 362(d)", "11 USC 362(k)"],
        elements=[
            "Automatic upon filing — no motion required",
            "Stays commencement or continuation of judicial/administrative proceedings",
            "Stays enforcement of pre-petition judgments",
            "Stays acts to obtain possession of property of the estate",
            "Stays acts to create, perfect, or enforce liens against property of the estate",
            "Stays setoff of pre-petition debts",
            "Duration: until case closed, dismissed, or discharge entered",
        ],
        defenses=[
            "Exception under 362(b): criminal proceedings, DSO establishment, tax audit, eviction with pre-petition judgment",
            "Serial filer limitation: 30-day stay (2nd filing in year) or no stay (3rd filing in year)",
            "Relief for cause including lack of adequate protection under 362(d)(1)",
            "No equity and property not necessary for reorganization under 362(d)(2)",
            "Single asset real estate debtor under 362(d)(3)",
            "Bad faith filing under 362(d)(4)",
        ],
        remedies=[
            "Damages for willful violation under 362(k): actual damages, costs, attorneys fees",
            "Punitive damages in appropriate cases for egregious violations",
            "Contempt sanctions",
            "Voiding of actions taken in violation of stay",
        ],
        leading_cases=[
            "Midlantic National Bank v. New Jersey DEP, 474 U.S. 494 (1986) - regulatory police power exception",
            "Ritzen Group v. Jackson Masonry, 589 U.S. ___ (2020) - stay relief orders are final appealable orders",
            "City of Chicago v. Fulton, 592 U.S. ___ (2021) - passive retention of property does not violate stay",
        ],
        category="stay",
        subcategory="automatic_stay",
        authority_score=0.95,
        confidence=0.93,
        related_topics=["stay_relief", "stay_violation", "codebtor_stay", "serial_filer", "adequate_protection"],
        practice_tips=[
            "Send stay notice letters to all creditors immediately upon filing",
            "Document all stay violations meticulously for potential damages claim",
            "For serial filers, file motion to extend/impose stay within 30 days",
            "Adequate protection payments often needed to maintain stay on secured property",
        ],
        risk_factors=[
            "Creditor may obtain ex parte relief in emergency situations",
            "Serial filer limitations severely limit stay protection",
            "Failure to provide adequate protection leads to stay relief",
        ],
        texas_notes="Texas nonjudicial foreclosure proceeds rapidly (21 days notice). Automatic stay stops foreclosure but creditor may seek stay relief promptly. Texas deed of trust foreclosure is first Tuesday of month.",
    ),

    # ========== DISCHARGE ==========
    DoctrineCacheBlock(
        topic="discharge_and_dischargeability",
        summary="Discharge eliminates the debtor's personal liability for qualifying debts, providing the 'fresh start' that is the hallmark of bankruptcy. Section 523 lists specific nondischargeable debt categories. Section 727 provides grounds for complete denial of discharge. BAPCPA expanded nondischargeable categories and tightened discharge requirements.",
        key_statutes=["11 USC 523", "11 USC 524", "11 USC 727", "11 USC 1328"],
        elements=[
            "Chapter 7: discharge entered ~60 days after 341 meeting absent objection",
            "Chapter 13: discharge upon completion of all plan payments",
            "Nondischargeable debts survive: DSO, student loans, fraud, DUI, tax (certain)",
            "Denial of discharge under 727(a): fraud, concealment, perjury, prior discharge",
            "Discharge injunction under 524(a): prohibits collection on discharged debts",
            "Reaffirmation agreement under 524(c) to keep paying discharged debt voluntarily",
        ],
        defenses=[
            "Prior discharge within 8 years (Ch 7) or 6 years (Ch 13) bars new Ch 7 discharge",
            "Debtor failed to complete financial management course",
            "Debtor committed fraud or concealment during case",
            "Creditor timely files adversary proceeding for 523 exception",
        ],
        remedies=[
            "Discharge eliminates personal liability",
            "Discharge injunction bars all future collection attempts",
            "Contempt sanctions for post-discharge collection violations",
            "Reopening case to add omitted creditor",
        ],
        leading_cases=[
            "Grogan v. Garner, 498 U.S. 279 (1991) - preponderance standard for 523 dischargeability",
            "Cohen v. de la Cruz, 523 U.S. 213 (1998) - treble damages from fraud are nondischargeable",
            "Kawaauhau v. Geiger, 523 U.S. 57 (1998) - willful and malicious injury requires intent",
            "Husky International Electronics v. Ritz, 578 U.S. 356 (2016) - actual fraud under 523(a)(2)(A) includes fraudulent transfer schemes",
        ],
        category="discharge",
        subcategory="general_discharge",
        authority_score=0.95,
        confidence=0.92,
        related_topics=["nondischargeable_debt", "student_loan_discharge", "tax_discharge", "reaffirmation", "discharge_denial"],
        practice_tips=[
            "Carefully review all debts for potential 523 exceptions before filing",
            "Advise clients on reaffirmation risks — particularly for depreciating assets",
            "Track bar date for 523(c) complaints (60 days after first 341 meeting date)",
            "Financial management course must be completed before discharge — track deadline",
        ],
        risk_factors=[
            "Failure to disclose assets or income risks denial under 727(a)",
            "Creditors may bring adversary proceedings on discharge",
            "Post-filing misconduct can lead to revocation of discharge under 727(d)",
        ],
        texas_notes="In the 5th Circuit, the Brunner test applies for student loan undue hardship. Texas courts apply strict interpretation of willful and malicious injury under 523(a)(6).",
    ),

    # ========== EXEMPTIONS ==========
    DoctrineCacheBlock(
        topic="bankruptcy_exemptions",
        summary="Exemptions protect certain debtor property from liquidation in Chapter 7 and establish the baseline for the best interests test in Chapter 13. Federal exemptions under 522(d) or state exemptions apply depending on state opt-out. Texas is an opt-out state with unlimited homestead value exemption, making it one of the most debtor-friendly exemption schemes in the nation.",
        key_statutes=["11 USC 522", "Tex. Prop. Code Ch. 41", "Tex. Prop. Code Ch. 42", "Tex. Const. Art. XVI"],
        elements=[
            "Federal exemptions under 522(d) OR state exemptions (debtor's domicile state controls)",
            "Texas opts out of federal exemptions — must use Texas scheme",
            "Homestead: Urban 10 acres, Rural 100 single/200 family, unlimited value",
            "Personal property: $100,000 family / $50,000 single aggregate",
            "Categories within personal property limit: furnishings, clothing, tools of trade, vehicles (1 per licensed member), jewelry, athletics/sporting, 2 firearms, livestock, pets, feed",
            "Current wages: fully exempt",
            "Retirement accounts (ERISA): fully exempt, IRAs exempt per 522(n) cap",
            "Life insurance: cash value fully exempt under Texas Insurance Code",
            "Burial plots: fully exempt",
            "730-day domicile requirement for state exemptions under BAPCPA",
            "Homestead cap: $189,050 if property acquired within 1215 days",
        ],
        defenses=[
            "Bad faith exemption conversion within close proximity to filing",
            "Homestead cap for property acquired within 1215 days under 522(p)",
            "Domicile requirement not met — must use prior state or federal exemptions",
            "Fraudulent concealment of assets",
        ],
        remedies=[
            "Protected assets retained by debtor in Chapter 7",
            "Establishes best interests test floor in Chapter 13",
            "Avoid judicial liens that impair exemptions under 522(f)",
            "Avoid nonpossessory, nonpurchase-money security interests in certain exempt property under 522(f)(1)(B)",
        ],
        leading_cases=[
            "Clark v. Rameker, 573 U.S. 122 (2014) - inherited IRAs not exempt under 522(d)",
            "Schwab v. Reilly, 560 U.S. 770 (2010) - trustee objection to exemptions",
            "Law v. Siegel, 571 U.S. 415 (2014) - court cannot surcharge exempt property for debtor misconduct",
            "In re Cowin, 864 F.3d 344 (5th Cir. 2017) - Texas homestead exemption scope",
        ],
        category="exemptions",
        subcategory="exemption_overview",
        authority_score=0.93,
        confidence=0.90,
        related_topics=["texas_homestead_exemption", "federal_exemptions", "exemption_planning", "wildcard_exemption"],
        practice_tips=[
            "Texas unlimited homestead is the single most valuable exemption — maximize",
            "Check 730-day domicile carefully for clients who recently moved to Texas",
            "Personal property aggregate includes ALL categories — track carefully",
            "Lien avoidance under 522(f) is separate motion — do not overlook",
        ],
        risk_factors=[
            "Pre-filing homestead conversion may be attacked as bad faith",
            "1215-day homestead cap limits new homestead acquisitions",
            "Inherited IRA not exempt after Clark v. Rameker",
        ],
        texas_notes="Texas has one of the most generous exemption schemes in the U.S. Unlimited homestead value (urban 10 ac, rural 200 ac family) combined with $100K personal property makes Texas extremely debtor-friendly. Key: vehicles are counted within personal property aggregate but have no individual cap (1 per licensed member).",
    ),

    # ========== PREFERENCE ACTIONS ==========
    DoctrineCacheBlock(
        topic="preference_avoidance_actions",
        summary="Section 547 empowers the trustee to avoid preferential transfers made within 90 days of filing (1 year for insiders) that enabled the transferee to receive more than it would in a Chapter 7 liquidation. The goal is equality of distribution among creditors. Multiple statutory defenses exist including ordinary course of business, contemporaneous exchange, and subsequent new value.",
        key_statutes=["11 USC 547(b)", "11 USC 547(c)", "11 USC 550"],
        elements=[
            "Transfer of an interest of the debtor in property",
            "To or for the benefit of a creditor",
            "For or on account of an antecedent debt",
            "Made while the debtor was insolvent (presumed 90 days pre-filing)",
            "Within 90 days of filing (or 1 year if insider)",
            "That enables creditor to receive more than in Chapter 7 liquidation",
        ],
        defenses=[
            "Contemporaneous exchange for new value 547(c)(1)",
            "Ordinary course of business 547(c)(2)",
            "Purchase money security interest 547(c)(3)",
            "Subsequent new value 547(c)(4)",
            "Floating lien on inventory/receivables 547(c)(5)",
            "Statutory lien fixing 547(c)(6)",
            "Domestic support obligation payment 547(c)(7)",
            "Small preference: <$7,575 non-business, <$7,575 business 547(c)(9)",
        ],
        remedies=[
            "Recovery of transferred property or its value under 550",
            "Recovery from initial or immediate/mediate transferee",
            "Good faith transferee defense for value under 550(b)",
        ],
        leading_cases=[
            "Union Bank v. Wolas, 502 U.S. 151 (1991) - ordinary course applies to long-term and short-term debt",
            "Barnhill v. Johnson, 503 U.S. 393 (1992) - check payment is transfer on honor date, not delivery",
            "Begier v. IRS, 496 U.S. 53 (1990) - trust fund taxes not property of the estate",
        ],
        category="avoidance",
        subcategory="preferences",
        authority_score=0.90,
        confidence=0.88,
        related_topics=["fraudulent_transfer", "strong_arm_power", "ordinary_course_defense"],
        practice_tips=[
            "Review 90-day and 1-year lookback periods for all significant payments",
            "Ordinary course defense is the most commonly asserted — document payment patterns",
            "Subsequent new value must be unpaid to offset preference",
            "Small preference threshold adjusted periodically — verify current amount",
        ],
        risk_factors=[
            "Insider payments have 1-year lookback — much longer than 90 days",
            "Insolvency presumed during 90-day period — shifts burden to defendant",
            "Trustee may pursue marginal claims to maximize estate recovery",
        ],
    ),

    # ========== FRAUDULENT TRANSFERS ==========
    DoctrineCacheBlock(
        topic="fraudulent_transfer_avoidance",
        summary="Section 548 allows the trustee to avoid transfers made with actual intent to defraud or for less than reasonably equivalent value while insolvent (constructive fraud). The trustee may also invoke state fraudulent transfer law (UFTA/UVTA) via Section 544(b) with its longer statutes of limitation. Badges of fraud are circumstantial indicators of actual intent.",
        key_statutes=["11 USC 548", "11 USC 544(b)", "Tex. Bus. & Com. Code Ch. 24 (TUFTA)"],
        elements=[
            "ACTUAL FRAUD (548(a)(1)(A)): Transfer with actual intent to hinder, delay, or defraud creditors",
            "CONSTRUCTIVE FRAUD (548(a)(1)(B)): Transfer for less than reasonably equivalent value AND debtor was insolvent/became insolvent/undercapitalized/intended to incur debts beyond ability to pay",
            "Federal reach-back: 2 years pre-filing",
            "State TUFTA reach-back via 544(b): 4 years actual fraud, 1 year constructive fraud (Texas)",
            "Badges of fraud: insider transfer, concealment, pending suit, substantially all assets, absconding, inadequate consideration, insolvency, close to debt incurrence",
        ],
        defenses=[
            "Good faith transferee for reasonably equivalent value under 548(c)",
            "Transfer was arm's length transaction for fair value",
            "Transferee had no knowledge of debtor's insolvency or intent",
            "Transfer predates reach-back period",
            "Charitable donation defense under 548(a)(2) (up to 15% of gross income)",
        ],
        remedies=[
            "Recovery of property transferred or value under 550",
            "Preservation of avoided transfer for benefit of estate under 551",
        ],
        leading_cases=[
            "BFP v. Resolution Trust Corp., 511 U.S. 531 (1994) - foreclosure sale price conclusively establishes reasonably equivalent value",
            "Husky International v. Ritz, 578 U.S. 356 (2016) - actual fraud includes fraudulent transfer schemes even without misrepresentation",
        ],
        category="avoidance",
        subcategory="fraudulent_transfers",
        authority_score=0.90,
        confidence=0.87,
        related_topics=["preference_avoidance_actions", "strong_arm_power", "badges_of_fraud"],
        practice_tips=[
            "Always consider state law via 544(b) for longer reach-back periods",
            "Document badges of fraud systematically for actual fraud claims",
            "Constructive fraud requires only insolvency + inadequate value — easier to prove",
            "Texas TUFTA provides additional remedies and may have longer reach-back",
        ],
    ),

    # ========== PLAN CONFIRMATION ==========
    DoctrineCacheBlock(
        topic="plan_confirmation_requirements",
        summary="Plan confirmation is the culmination of a Chapter 11 or Chapter 13 case. In Chapter 11, the plan must be accepted by impaired classes (2/3 in amount, >1/2 in number) or confirmed via cramdown. In Chapter 13, the plan must satisfy good faith, best interests, and disposable income tests. Confirmation makes the plan binding on all parties.",
        key_statutes=["11 USC 1129", "11 USC 1325", "11 USC 1225"],
        elements=[
            "CHAPTER 11: Plan complies with Code, proposed in good faith, feasible, best interests test, acceptance by all impaired classes OR cramdown",
            "CRAMDOWN (1129(b)): Fair and equitable + no unfair discrimination for each dissenting impaired class",
            "Absolute priority rule (secured→unsecured→equity) unless new value exception",
            "CHAPTER 13: Good faith, best interests, disposable income commitment, DSO current, tax returns filed",
            "Secured claims: retain liens + receive present value of claim, or surrender collateral",
        ],
        defenses=[
            "Plan not feasible — debtor cannot make proposed payments",
            "Bad faith — plan proposed for improper purpose",
            "Best interests test failure — creditors receive less than in Chapter 7",
            "Unfair discrimination between similarly situated classes",
            "Absolute priority rule violation (Chapter 11)",
        ],
        remedies=[
            "Confirmation order binds debtor and all creditors",
            "Vesting of property in debtor (or plan entity) under plan terms",
            "Discharge upon plan completion (or at confirmation in some Chapter 11 cases)",
            "Modification pre-confirmation or post-confirmation for cause",
        ],
        leading_cases=[
            "Bank of America v. 203 North LaSalle, 526 U.S. 434 (1999) - new value exception requires competitive process",
            "Till v. SCS Credit Corp., 541 U.S. 465 (2004) - formula rate for cramdown interest (prime + risk adjustment)",
            "Associates Commercial Corp. v. Rash, 520 U.S. 953 (1997) - replacement value for cramdown valuation",
        ],
        category="plan",
        subcategory="confirmation",
        authority_score=0.93,
        confidence=0.89,
        related_topics=["cramdown", "absolute_priority_rule", "best_interests_test", "feasibility", "disclosure_statement"],
        practice_tips=[
            "Till formula rate: prime rate + 1-3% risk adjustment is standard",
            "Rash replacement value applies for secured claim valuation in cramdown",
            "Classification strategy is critical — avoid gerrymandering",
            "Subchapter V eliminates absolute priority rule for small business debtors",
        ],
    ),

    # ========== CRAMDOWN ==========
    DoctrineCacheBlock(
        topic="cramdown_and_lien_stripping",
        summary="Cramdown allows confirmation over the objection of dissenting impaired classes if the plan is fair and equitable and does not unfairly discriminate. For secured claims, cramdown requires the creditor retain its lien and receive deferred payments with present value equal to the secured claim. Lien stripping in Chapter 13 allows removal of wholly unsecured junior liens on principal residence.",
        key_statutes=["11 USC 1129(b)", "11 USC 506(a)", "11 USC 1322(b)(2)", "11 USC 506(d)"],
        elements=[
            "CRAMDOWN SECURED: Retain liens + present value of secured claim (replacement value per Rash)",
            "CRAMDOWN UNSECURED: APR — no junior class receives unless senior paid in full",
            "CRAMDOWN EQUITY: Cannot retain interest unless all classes paid in full or new value contributed",
            "LIEN STRIPPING (Ch 13): Junior lien on principal residence wholly unsecured (no equity) → treated as unsecured",
            "Valuation: 506(a) bifurcation — secured to extent of value, unsecured for remainder",
            "Interest rate: Till formula (prime + 1-3% risk adjustment)",
            "Hanging paragraph: 910-day vehicle / 1-year other PMSI cannot be crammed down",
        ],
        defenses=[
            "Anti-modification rule: cannot modify rights of holder of claim secured only by principal residence mortgage (Ch 13)",
            "Hanging paragraph protects recent vehicle PMSI from cramdown",
            "Caulkett: partially secured junior lien cannot be stripped in Chapter 7",
        ],
        remedies=[
            "Secured claim reduced to collateral value (cramdown)",
            "Junior lien stripped and treated as unsecured claim (Ch 13 lien strip)",
            "Reduced monthly payments to secured creditors",
            "Plan confirmed despite creditor objection",
        ],
        leading_cases=[
            "Bank of America v. Caulkett, 575 U.S. 790 (2015) - cannot strip partially secured junior lien in Chapter 7",
            "Associates Commercial Corp. v. Rash, 520 U.S. 953 (1997) - replacement value standard",
            "Till v. SCS Credit Corp., 541 U.S. 465 (2004) - formula rate for cramdown interest",
            "Nobelman v. American Savings Bank, 508 U.S. 324 (1993) - anti-modification of home mortgage",
        ],
        category="plan",
        subcategory="cramdown",
        authority_score=0.92,
        confidence=0.88,
        related_topics=["plan_confirmation_requirements", "absolute_priority_rule", "secured_claim_valuation"],
        practice_tips=[
            "Lien stripping requires that junior lien be WHOLLY unsecured — get appraisal",
            "Chapter 20 strategy: Ch 7 discharge eliminates personal liability, then Ch 13 strips lien",
            "Hanging paragraph prevents cramdown on vehicles financed within 910 days — check purchase date",
            "Till formula rate typically prime + 1.5% to 3% depending on risk",
        ],
        texas_notes="Texas home values and oil/gas property valuations are critical for lien stripping and cramdown analysis. Appraisals in Midland/Odessa area should account for commodity price volatility.",
    ),

    # ========== ADVERSARY PROCEEDINGS ==========
    DoctrineCacheBlock(
        topic="adversary_proceedings",
        summary="Adversary proceedings are the bankruptcy equivalent of civil lawsuits, governed by FRBP Part VII (Rules 7001-7087) which incorporate Federal Rules of Civil Procedure. They are required for dischargeability determinations, objections to discharge, avoidance actions, and other contested matters beyond routine motions.",
        key_statutes=["FRBP 7001-7087", "11 USC 523(c)", "11 USC 727(c)"],
        elements=[
            "Complaint required (not motion) for: dischargeability (523(c)), discharge objection (727), avoidance actions, lien validity, subordination, turnover",
            "Bar date for 523(c) complaints: 60 days after first 341 meeting date set",
            "Service of process under FRBP 7004",
            "Discovery under FRBP 7026-7037 (incorporating FRCP)",
            "Summary judgment available under FRBP 7056",
            "Trial before bankruptcy judge",
            "Appeal to BAP or district court under 28 USC 158",
        ],
        defenses=[
            "Failure to timely file complaint (bar date expired)",
            "Standing: only certain parties may bring specific AP types",
            "Failure to state a claim (FRBP 7012 motion to dismiss)",
        ],
        remedies=[
            "Determination of nondischargeability",
            "Denial of discharge",
            "Recovery of avoided transfers",
            "Determination of lien validity",
            "Subordination or recharacterization of claims",
        ],
        leading_cases=[
            "Stern v. Marshall, 564 U.S. 462 (2011) - constitutional limits on bankruptcy court authority",
            "Wellness International v. Sharif, 575 U.S. 665 (2015) - parties may consent to bankruptcy court final adjudication",
        ],
        category="adversary",
        subcategory="proceedings",
        authority_score=0.88,
        confidence=0.85,
        related_topics=["discharge_and_dischargeability", "preference_avoidance_actions", "fraudulent_transfer_avoidance"],
        practice_tips=[
            "Calendar the 60-day bar date for 523(c) complaints immediately upon case filing",
            "Stern v. Marshall limits require careful analysis of whether bankruptcy court has constitutional authority",
            "Consider consent to bankruptcy court adjudication under Wellness International where appropriate",
        ],
    ),

    # ========== TRUSTEE POWERS ==========
    DoctrineCacheBlock(
        topic="trustee_powers_and_duties",
        summary="The bankruptcy trustee is a fiduciary charged with collecting and liquidating estate property (Chapter 7) or overseeing plan payments (Chapter 13). The trustee has powerful avoidance powers under Sections 544-550 and investigative authority to examine the debtor and financial affairs. The US Trustee monitors trustees and enforces compliance.",
        key_statutes=["11 USC 704", "11 USC 1302", "11 USC 544-550", "28 USC 586"],
        elements=[
            "Chapter 7 trustee: collect property, liquidate, examine claims, oppose discharge if warranted, file returns",
            "Chapter 13 standing trustee: review plan, collect and distribute payments, appear at confirmation",
            "Strong-arm powers under 544(a): hypothetical lien creditor, BFP of real property",
            "Avoidance powers: preferences (547), fraudulent transfers (548), post-petition transfers (549)",
            "Turnover power under 542: compel turnover of estate property",
            "US Trustee (28 USC 586): monitor means test compliance, move to dismiss abuse, oversee trustees",
        ],
        defenses=[
            "Property claimed as exempt under 522",
            "Good faith transferee defense under 548(c)/550(b)",
            "Ordinary course defense to preference under 547(c)(2)",
            "Property abandoned by trustee under 554",
        ],
        remedies=[
            "Recovery of estate property",
            "Avoidance of improper transfers",
            "Surcharge of estate for unauthorized actions",
            "Removal of trustee for cause under 324",
        ],
        leading_cases=[
            "Harris v. Viegelahn, 575 U.S. 510 (2015) - trustee must return undistributed funds upon conversion to Ch 7",
            "Hartford Underwriters Insurance Co. v. Union Planters Bank, 530 U.S. 1 (2000) - only trustee can pursue 506(c) surcharge",
        ],
        category="estate",
        subcategory="trustee",
        authority_score=0.88,
        confidence=0.86,
        related_topics=["preference_avoidance_actions", "fraudulent_transfer_avoidance", "strong_arm_power", "us_trustee_oversight"],
        practice_tips=[
            "Cooperate with trustee examination — failure can lead to denial of discharge",
            "Trustee abandonment of burdensome property can benefit estate",
            "US Trustee actively monitors for means test abuse in every district",
        ],
    ),

    # ========== STUDENT LOAN DISCHARGE ==========
    DoctrineCacheBlock(
        topic="student_loan_undue_hardship",
        summary="Student loans are presumptively nondischargeable under 523(a)(8) unless the debtor demonstrates undue hardship through an adversary proceeding. The Brunner test (majority of circuits) requires showing: (1) inability to maintain minimal standard of living, (2) additional circumstances indicating this will persist, and (3) good faith effort to repay. Some circuits use a totality of circumstances test.",
        key_statutes=["11 USC 523(a)(8)", "FRBP 7001"],
        elements=[
            "BRUNNER TEST (2d Cir., adopted by majority): (1) Cannot maintain minimal standard of living based on current income/expenses if forced to repay, (2) Additional circumstances exist indicating this will persist for significant portion of repayment period, (3) Debtor has made good faith effort to repay",
            "TOTALITY TEST (1st, 7th, 8th Cir.): Court considers all relevant facts including debtor's past/present/future financial resources, reasonable living expenses, other circumstances unique to debtor",
            "Must be educational benefit overpayment or loan (qualified educational loan)",
            "Adversary proceeding required — cannot discharge by motion alone",
            "Burden of proof on debtor (preponderance standard per Grogan)",
        ],
        defenses=[
            "Debtor has ability to maintain minimal standard AND repay",
            "Debtor did not make good faith repayment effort (never entered IDR, deferment without basis)",
            "Circumstances likely to improve (young debtor, recent degree, employable field)",
            "Debtor has not explored Income-Driven Repayment (IDR) programs",
        ],
        remedies=[
            "Full discharge of student loan if undue hardship shown on all elements",
            "Partial discharge (some courts): discharge portion of loan",
            "Modified repayment terms ordered by court",
        ],
        leading_cases=[
            "Brunner v. New York State Higher Education Services Corp., 831 F.2d 395 (2d Cir. 1987) - three-part test",
            "In re Oyler, 397 F.3d 382 (6th Cir. 2005) - adopting Brunner test",
            "Krieger v. Educational Credit Mgmt. Corp., 713 F.3d 882 (7th Cir. 2013) - totality approach",
        ],
        category="discharge",
        subcategory="student_loans",
        authority_score=0.90,
        confidence=0.85,
        related_topics=["discharge_and_dischargeability", "adversary_proceedings", "brunner_test"],
        practice_tips=[
            "Document EVERY attempt at repayment and income-driven repayment application",
            "Medical conditions, disability, and age are strong 'additional circumstances'",
            "Some courts allow partial discharge — negotiate before trial if possible",
            "DOJ 2022 guidance creates new attestation-based streamlined process for USAs",
        ],
        risk_factors=[
            "Brunner test is extremely difficult to satisfy — most courts apply strictly",
            "Failure to explore IDR programs undermines good faith element",
            "Cost of adversary proceeding may exceed benefit for smaller loan balances",
        ],
        texas_notes="5th Circuit applies the Brunner test. Texas courts have historically applied it strictly. However, DOJ 2022 guidance may soften approach in cases where USA is creditor.",
    ),

    # ========== TAX DEBT DISCHARGE ==========
    DoctrineCacheBlock(
        topic="tax_debt_discharge_rules",
        summary="Income tax debts can be discharged in bankruptcy if all five conditions are met: (1) 3-year rule — return was due more than 3 years ago, (2) 2-year rule — return was actually filed more than 2 years ago, (3) 240-day rule — tax was assessed more than 240 days ago, (4) no fraud, (5) debtor actually filed a return. Toll periods for prior bankruptcy, collection suspensions, and OIC offers must be calculated.",
        key_statutes=["11 USC 523(a)(1)", "11 USC 507(a)(8)", "26 USC 6020(b)"],
        elements=[
            "3-YEAR RULE: Tax return was due (including extensions) more than 3 years before petition date",
            "2-YEAR RULE: Tax return was actually filed more than 2 years before petition date",
            "240-DAY RULE: Tax was assessed more than 240 days before petition date (plus toll periods)",
            "NO FRAUD: Debtor did not file a fraudulent return or willfully attempt to evade the tax",
            "FILED RETURN: Debtor actually filed a tax return (substitute for return by IRS under 6020(b) may not count)",
        ],
        defenses=[
            "Return filed late does not restart 3-year period (3 years from original due date)",
            "Toll periods: prior bankruptcy filing, collection due process, OIC, installment agreement request",
            "IRS assessment after audit restarts 240-day clock",
            "6020(b) substitute for return — split among circuits whether it counts as 'filed return'",
        ],
        remedies=[
            "Full discharge of income tax debt if all 5 rules satisfied",
            "Tax liens survive discharge but can be addressed through lien avoidance or lien stripping",
            "Chapter 13: tax priority claims paid 100% through plan without interest (in some districts)",
        ],
        leading_cases=[
            "In re Hindenlang, 164 F.3d 1029 (6th Cir. 1999) - late-filed return still counts as 'return' filed",
            "Beard v. Commissioner, 793 F.2d 139 (6th Cir. 1986) - four-part test for what constitutes a 'return'",
            "In re McCoy, 666 F.3d 924 (5th Cir. 2012) - 6020(b) SFR is not a 'return' for discharge purposes",
        ],
        category="discharge",
        subcategory="tax_discharge",
        authority_score=0.88,
        confidence=0.85,
        related_topics=["discharge_and_dischargeability", "priority_claims", "tax_lien_survival"],
        practice_tips=[
            "Create a year-by-year tax discharge eligibility chart for each tax year",
            "Calculate toll periods meticulously — they extend the lookback periods",
            "Tax liens survive discharge but attach only to pre-petition property",
            "Consider filing all delinquent returns at least 2 years before filing bankruptcy",
        ],
        risk_factors=[
            "SFR (6020(b)) may prevent discharge in circuits that do not treat it as a return",
            "Tax fraud or willful evasion is absolute bar to discharge",
            "Toll periods can extend windows significantly",
        ],
        texas_notes="5th Circuit (In re McCoy) holds that 6020(b) substitute for return does NOT count as a filed return for discharge purposes. This is critical for Texas debtors with IRS-prepared SFRs.",
    ),

    # ========== REAFFIRMATION ==========
    DoctrineCacheBlock(
        topic="reaffirmation_agreements",
        summary="A reaffirmation agreement under 524(c) allows a debtor to voluntarily agree to remain personally liable on a debt that would otherwise be discharged. Commonly used for vehicle loans to retain the collateral. BAPCPA strengthened judicial oversight, requiring court approval if the debtor is unrepresented by counsel and the agreement creates a presumption of undue hardship.",
        key_statutes=["11 USC 524(c)", "11 USC 524(d)", "11 USC 524(k)", "Official Form 240A/B"],
        elements=[
            "Agreement made before discharge is entered",
            "Debtor was fully informed and agreement is voluntary",
            "Agreement does not impose undue hardship on debtor or dependents",
            "Court approval required if debtor is not represented by attorney",
            "60-day rescission period after agreement filed with court",
            "Presumption of undue hardship if budget shows negative disposable income",
            "Attorney certification of informed consent and no undue hardship (if represented)",
        ],
        defenses=[
            "Debtor may rescind within 60 days of filing or before discharge (whichever is later)",
            "Court may refuse to approve if undue hardship demonstrated",
            "Agreement not enforceable if not filed with court before discharge",
        ],
        remedies=[
            "Debtor retains collateral and credit history on that account",
            "Creditor retains personal liability of debtor on the debt",
            "If debtor defaults post-reaffirmation: full collection rights including deficiency",
        ],
        leading_cases=[
            "In re Schwass, 378 B.R. 859 (Bankr. S.D. Cal. 2007) - judicial duty to evaluate undue hardship",
        ],
        category="discharge",
        subcategory="reaffirmation",
        authority_score=0.82,
        confidence=0.84,
        related_topics=["discharge_and_dischargeability", "chapter_7_liquidation_overview", "ride_through"],
        practice_tips=[
            "Carefully evaluate whether reaffirmation is in client's best interest — depreciating assets are risky",
            "Consider alternatives: redemption under 722, ride-through (where permitted), surrender",
            "Attorney certification creates professional responsibility obligation",
            "Budget analysis must show ability to make payments without undue hardship",
        ],
        risk_factors=[
            "Debtor re-assumes full personal liability on a potentially underwater debt",
            "Default after reaffirmation: creditor has full collection rights including deficiency",
            "Vehicle reaffirmation on underwater loan is frequently ill-advised",
        ],
    ),

    # ========== BAPCPA ==========
    DoctrineCacheBlock(
        topic="bapcpa_overview",
        summary="The Bankruptcy Abuse Prevention and Consumer Protection Act of 2005 (BAPCPA) was the most significant reform of bankruptcy law since 1978. It added the means test, credit counseling/financial management requirements, increased documentation burdens, limited automatic stay for serial filers, imposed attorney liability as debt relief agencies, and added the homestead cap.",
        key_statutes=["Pub. L. 109-8 (April 20, 2005)", "effective October 17, 2005"],
        elements=[
            "Means test under 707(b)(2) to screen Chapter 7 eligibility",
            "Mandatory pre-filing credit counseling (180 days before filing)",
            "Mandatory post-filing financial management course (before discharge)",
            "Increased documentation: tax returns, pay stubs, means test forms",
            "Attorney defined as 'debt relief agency' with advertising/disclosure requirements",
            "Automatic stay limitations for serial filers (30 days/no stay)",
            "Homestead cap: $189,050 for property acquired within 1215 days",
            "730-day domicile requirement for state exemptions",
            "Luxury goods presumption: >$800 within 90 days",
            "Cash advance presumption: >$1,100 within 70 days",
            "DSO priority elevated to first priority under 507(a)(1)",
        ],
        defenses=[],
        remedies=[],
        leading_cases=[
            "Milavetz v. United States, 559 U.S. 229 (2010) - attorney as debt relief agency constitutional",
            "Ransom v. FIA Card Services, 562 U.S. 61 (2011) - means test deduction interpretation",
        ],
        category="legislation",
        subcategory="bapcpa",
        authority_score=0.92,
        confidence=0.90,
        related_topics=["means_test_calculation", "automatic_stay_362", "bankruptcy_exemptions", "credit_counseling"],
        practice_tips=[
            "BAPCPA requirements are jurisdictional prerequisites — non-compliance can result in dismissal",
            "Credit counseling must be from approved provider AND within 180 days",
            "Financial management course must be completed before discharge entry",
            "Attorney must carefully comply with debt relief agency requirements",
        ],
    ),

    # ========== EXECUTORY CONTRACTS ==========
    DoctrineCacheBlock(
        topic="executory_contracts_and_leases",
        summary="Section 365 governs the assumption, rejection, or assignment of executory contracts and unexpired leases. The trustee/DIP may assume a beneficial contract (after curing defaults) or reject a burdensome one (treated as pre-petition breach). Assignment of non-personal-service contracts is permitted if adequate assurance of future performance is provided.",
        key_statutes=["11 USC 365", "11 USC 362"],
        elements=[
            "Executory contract: Material unperformed obligations on both sides (Countryman definition)",
            "ASSUMPTION requires: cure of defaults, compensate for actual pecuniary loss, adequate assurance of future performance",
            "REJECTION treated as pre-petition breach — gives rise to general unsecured claim",
            "Deadline for commercial real property leases: 210 days (with possible 90-day extension)",
            "Anti-assignment clauses unenforceable in bankruptcy for most contracts",
            "Ipso facto clauses (termination upon bankruptcy filing) unenforceable under 365(e)",
        ],
        defenses=[
            "Contract is personal services contract — cannot be assigned without consent",
            "Debtor cannot provide adequate assurance of future performance",
            "Applicable law excuses non-debtor party from performing with assignee",
        ],
        remedies=[
            "Assumption preserves beneficial contract for the estate",
            "Rejection limits liability to pre-petition breach claim",
            "Assignment transfers contract to purchaser in asset sale",
        ],
        leading_cases=[
            "NLRB v. Bildisco, 465 U.S. 513 (1984) - CBA rejection standard (pre-Section 1113)",
            "Mission Product Holdings v. Tempnology, 587 U.S. ___ (2019) - rejection does not rescind trademark license",
        ],
        category="contracts",
        subcategory="executory_contracts",
        authority_score=0.85,
        confidence=0.83,
        related_topics=["chapter_11_reorganization_overview", "dip_operations"],
        practice_tips=[
            "Calendar the 210-day deadline for commercial real property lease assumption",
            "Rejection of below-market lease is a key strategy for retailers in Chapter 11",
            "Mission Product overruled Lubrizol for trademark licenses — licenses survive rejection",
        ],
    ),

    # ========== DIP FINANCING ==========
    DoctrineCacheBlock(
        topic="dip_financing_and_cash_collateral",
        summary="Section 364 governs post-petition financing for Chapter 11 debtors-in-possession. DIP financing ranges from unsecured credit in the ordinary course to superpriority administrative claims and priming liens. Section 363(c)(2) requires court authorization or creditor consent for use of cash collateral (cash, deposit accounts, receivables subject to a lien).",
        key_statutes=["11 USC 364", "11 USC 363(c)(2)", "11 USC 363(e)"],
        elements=[
            "364(a): Unsecured credit in ordinary course without court approval",
            "364(b): Unsecured credit outside ordinary course — court approval needed",
            "364(c)(1): Superpriority administrative expense claim",
            "364(c)(2): Senior lien on unencumbered property",
            "364(c)(3): Junior lien on already-encumbered property",
            "364(d): Priming lien on already-encumbered property (requires adequate protection of existing lien)",
            "Cash collateral: court approval or consent of secured party required for use",
            "Adequate protection: replacement lien, cash payments, equity cushion, or other relief",
        ],
        defenses=[
            "DIP lender's terms are not in best interest of estate",
            "Existing lienholders not adequately protected",
            "DIP loan imposes excessive fees, warrants, or other terms",
            "Priming lien cannot be authorized without adequate protection of existing liens",
        ],
        remedies=[
            "Court authorization for DIP financing",
            "Interim and final cash collateral orders",
            "Superpriority claims and priming liens for DIP lenders",
            "Adequate protection for existing secured creditors",
        ],
        leading_cases=[
            "In re Lyondell Chemical Co., 402 B.R. 571 (Bankr. S.D.N.Y. 2009) - DIP financing approval standards",
        ],
        category="operations",
        subcategory="dip_financing",
        authority_score=0.85,
        confidence=0.82,
        related_topics=["chapter_11_reorganization_overview", "adequate_protection", "cash_collateral"],
        practice_tips=[
            "File first-day motion for interim cash collateral authorization",
            "DIP financing terms should be market-tested — courts scrutinize excessive fees",
            "Adequate protection typically requires ongoing payments or equity cushion",
            "Priming liens are disfavored — demonstrate inability to obtain credit on lesser terms",
        ],
    ),

    # ========== CHAPTER 20 STRATEGY ==========
    DoctrineCacheBlock(
        topic="chapter_20_strategy",
        summary="Chapter 20 is the colloquial term for filing Chapter 7 followed by Chapter 13. The debtor obtains a Chapter 7 discharge eliminating personal liability, then files Chapter 13 to deal with surviving liens (particularly lien stripping of wholly unsecured junior mortgages). Although the debtor cannot receive a Chapter 13 discharge, courts generally allow lien stripping through plan confirmation.",
        key_statutes=["11 USC 727", "11 USC 1322(b)(2)", "11 USC 1325", "11 USC 506(a)"],
        elements=[
            "Step 1: File Chapter 7, receive discharge (eliminates personal liability on unsecured debts)",
            "Step 2: File Chapter 13 (no waiting period for filing, but no discharge available within 4 years)",
            "Lien stripping: wholly unsecured junior liens can be stripped through Chapter 13 plan",
            "No discharge needed for lien stripping — lien strip effective upon plan completion",
            "Good faith requirement: must have legitimate purpose beyond abuse of process",
        ],
        defenses=[
            "Bad faith filing — Chapter 13 filed solely to abuse process",
            "Some courts restrict Chapter 20 strategies",
            "Junior lien must be WHOLLY unsecured (not partially secured)",
        ],
        remedies=[
            "Personal liability eliminated via Chapter 7 discharge",
            "Junior liens stripped through Chapter 13 plan completion",
            "Net result: debtor retains home free of underwater junior liens",
        ],
        leading_cases=[
            "Johnson v. Home State Bank, 501 U.S. 78 (1991) - mortgage lien survives Chapter 7 discharge; Chapter 13 can address surviving liens",
            "In re Branigan, 465 B.R. 492 (9th Cir. BAP 2012) - Chapter 20 lien stripping permitted",
        ],
        category="strategy",
        subcategory="chapter_20",
        authority_score=0.80,
        confidence=0.78,
        related_topics=["cramdown_and_lien_stripping", "chapter_7_liquidation_overview", "chapter_13_wage_earner_plan"],
        practice_tips=[
            "Verify junior lien is wholly unsecured — get current appraisal",
            "Chapter 13 plan must be completed in full for lien strip to take effect",
            "Document legitimate purpose to defend against bad faith challenge",
            "Circuit law varies — confirm Chapter 20 lien stripping is permitted in jurisdiction",
        ],
        texas_notes="Texas home values in Permian Basin can fluctuate significantly with oil prices. Timing of appraisal is critical for demonstrating junior lien is wholly unsecured.",
    ),

    # ========== SERIAL FILER STAY LIMITATIONS ==========
    DoctrineCacheBlock(
        topic="serial_filer_stay_limitations",
        summary="BAPCPA added automatic stay limitations for serial filers. If debtor had a case pending and dismissed within 1 year before current filing, the stay automatically terminates after 30 days unless the court extends it. If debtor had 2+ cases pending and dismissed within 1 year, no automatic stay arises at all unless the court specifically imposes it.",
        key_statutes=["11 USC 362(c)(3)", "11 USC 362(c)(4)"],
        elements=[
            "362(c)(3): One prior dismissal within 1 year — stay terminates after 30 days unless extended",
            "362(c)(4): Two or more prior dismissals within 1 year — no stay at all unless court imposes",
            "Extension/imposition requires motion within 30 days showing good faith",
            "Good faith: change in financial circumstances, legitimate purpose, no abuse pattern",
            "Stay terminates as to debtor AND property of the estate (majority view)",
        ],
        defenses=[
            "Prior dismissal was not the debtor's fault (involuntary dismissal)",
            "Changed circumstances since prior dismissal",
            "Current filing in good faith and not part of scheme to delay creditors",
        ],
        remedies=[
            "Motion to extend stay beyond 30 days under 362(c)(3)(B)",
            "Motion to impose stay under 362(c)(4)(B)",
            "Demonstrate good faith change in circumstances",
        ],
        leading_cases=[
            "In re Daniel, 404 B.R. 318 (Bankr. N.D. Ill. 2009) - good faith analysis for stay extension",
        ],
        category="stay",
        subcategory="serial_filer",
        authority_score=0.82,
        confidence=0.83,
        related_topics=["automatic_stay_362", "bad_faith_filing"],
        practice_tips=[
            "File motion to extend/impose stay IMMEDIATELY upon filing — before 30 days runs",
            "Document changed financial circumstances thoroughly",
            "Consider whether prior dismissal was voluntary or involuntary",
            "Some courts hold stay termination applies only to debtor, not estate property — check circuit law",
        ],
    ),

    # ========== PROOF OF CLAIM ==========
    DoctrineCacheBlock(
        topic="proof_of_claim_and_claims_process",
        summary="Creditors must file proof of claim to participate in distribution from the bankruptcy estate. FRBP 3001-3007 govern the claims process including form requirements, bar dates, and objection procedures. Claims are classified as secured, priority unsecured, or general unsecured, with distribution following the priority waterfall of Section 726/507.",
        key_statutes=["11 USC 501-502", "11 USC 506-507", "11 USC 726", "FRBP 3001-3007"],
        elements=[
            "Proof of claim filed on Official Form 410",
            "Bar date set by court (typically 70 days after petition in Ch 7/13; various in Ch 11)",
            "Claim allowed unless party in interest objects under 502(b)",
            "Claims classification: secured (506(a)), priority (507(a)), general unsecured",
            "Priority waterfall: DSO → administrative → wages → contributions → grain/fish → consumer deposits → taxes → DUI claims → FDIC",
        ],
        defenses=[
            "Claim filed after bar date (may be disallowed unless excused)",
            "Claim is unenforceable under applicable nonbankruptcy law",
            "Claim for unmatured interest (502(b)(2))",
            "Claim for insider compensation exceeding reasonable value",
        ],
        remedies=[
            "Allowed claim participates in distribution",
            "Objection to claim reduces or eliminates it",
            "Subordination under 510(c) for inequitable conduct",
            "Recharacterization of debt as equity (judicially created remedy)",
        ],
        leading_cases=[
            "Travelers Casualty & Surety Co. v. Pacific Gas & Electric Co., 549 U.S. 443 (2007) - claim for attorney fees as actual loss",
        ],
        category="claims",
        subcategory="proof_of_claim",
        authority_score=0.85,
        confidence=0.84,
        related_topics=["priority_claim", "secured_claim_valuation", "discharge_and_dischargeability"],
        practice_tips=[
            "Calendar the bar date and file claims well in advance",
            "Review all claims filed against the estate and object where appropriate",
            "506(a) valuation motion critical for bifurcating undersecured claims",
        ],
    ),

    # ========== ADEQUATE PROTECTION ==========
    DoctrineCacheBlock(
        topic="adequate_protection",
        summary="Adequate protection is the mechanism by which secured creditors are compensated for the diminution in value of their collateral during the pendency of a bankruptcy case. Required for use of cash collateral (363), to prevent stay relief (362(d)(1)), and for DIP financing with priming liens (364(d)). Forms include periodic cash payments, additional or replacement liens, and equity cushion.",
        key_statutes=["11 USC 361", "11 USC 362(d)(1)", "11 USC 363(e)", "11 USC 364(d)"],
        elements=[
            "Section 361 provides non-exclusive list of adequate protection methods",
            "Cash payments to compensate for decrease in collateral value",
            "Additional or replacement lien on other property",
            "Other relief resulting in the indivisible equivalent of the creditor's interest",
            "Equity cushion: difference between collateral value and debt may constitute adequate protection",
            "Adequate protection failure is an administrative claim under 507(b)",
        ],
        defenses=[
            "Collateral is not declining in value (no diminution)",
            "Equity cushion is sufficient to protect against decline",
            "Debtor is maintaining and insuring the collateral",
        ],
        remedies=[
            "Court-ordered adequate protection payments",
            "Additional liens on unencumbered property",
            "Relief from stay if adequate protection cannot be provided",
            "507(b) superpriority administrative claim if adequate protection fails",
        ],
        leading_cases=[
            "United Savings Association v. Timbers of Inwood Forest, 484 U.S. 365 (1988) - undersecured creditor not entitled to interest as adequate protection; no lost opportunity cost",
            "In re Murel Trading Ltd., 38 B.R. 478 (Bankr. S.D.N.Y. 1984) - indubitable equivalent standard",
        ],
        category="operations",
        subcategory="adequate_protection",
        authority_score=0.90,
        confidence=0.87,
        related_topics=["automatic_stay_362", "dip_financing_and_cash_collateral", "stay_relief"],
        practice_tips=[
            "Timbers controls: undersecured creditors cannot demand interest as adequate protection",
            "Equity cushion of 20%+ is generally considered adequate in most courts",
            "Monthly adequate protection payments should be proposed in first-day motions",
            "507(b) claim for adequate protection failure has superpriority over all other administrative claims",
        ],
    ),

    # ========== EQUITABLE SUBORDINATION ==========
    DoctrineCacheBlock(
        topic="equitable_subordination",
        summary="Under Section 510(c), the bankruptcy court may subordinate all or part of an allowed claim to some or all other allowed claims, or transfer the subordinated lien to the estate. Most commonly used against insiders or controlling parties who have engaged in inequitable conduct that harmed other creditors. The three-prong Mobile Steel test governs.",
        key_statutes=["11 USC 510(c)", "11 USC 510(a)", "11 USC 510(b)"],
        elements=[
            "MOBILE STEEL TEST: (1) Claimant engaged in inequitable conduct, (2) Conduct injured other creditors or conferred unfair advantage, (3) Subordination is consistent with bankruptcy law provisions",
            "Insiders face greater scrutiny under fiduciary duty analysis",
            "Non-insider claimants require showing of egregious misconduct",
            "Contractual subordination under 510(a) enforced per agreement terms",
            "Securities fraud claims subordinated under 510(b) to all claims except equity interests",
        ],
        defenses=[
            "Conduct was not inequitable — arm's length transaction",
            "Other creditors were not harmed by the conduct",
            "Claimant is not an insider and did not engage in egregious conduct",
        ],
        remedies=[
            "Subordination of claim to junior position in distribution",
            "Transfer of subordinated lien to estate for benefit of other creditors",
            "Recharacterization of debt as equity (judicially created, distinct from subordination)",
        ],
        leading_cases=[
            "In re Mobile Steel Co., 563 F.2d 692 (5th Cir. 1977) - three-prong test for equitable subordination",
            "United States v. Noland, 517 U.S. 535 (1996) - categorical subordination of tax penalties not permitted",
        ],
        category="claims",
        subcategory="subordination",
        authority_score=0.83,
        confidence=0.80,
        related_topics=["proof_of_claim_and_claims_process", "adversary_proceedings"],
        practice_tips=[
            "5th Circuit (Mobile Steel) originated the test — strong precedent in Texas",
            "Insiders include officers, directors, persons in control, relatives, entities controlled by debtor",
            "Recharacterization is distinct — reclassifies the nature of the claim, not just priority",
        ],
    ),

    # ========== PROPERTY OF THE ESTATE ==========
    DoctrineCacheBlock(
        topic="property_of_the_estate",
        summary="Section 541 defines property of the estate broadly to include all legal or equitable interests of the debtor in property as of the commencement of the case, wherever located and by whomever held. This includes tangible and intangible property, causes of action, tax refunds, and interests in trusts. Certain exclusions apply including spendthrift trust interests, power exercisable solely for benefit of non-debtor, and certain educational deposits.",
        key_statutes=["11 USC 541", "11 USC 542 (turnover)", "11 USC 554 (abandonment)"],
        elements=[
            "All legal or equitable interests of the debtor as of petition date",
            "Includes community property under debtor's sole, joint, or equal control",
            "Includes property recovered under avoidance powers (541(a)(3))",
            "Includes property preserved for benefit of estate under 551",
            "Includes interests in property that debtor acquires within 180 days after filing: inheritance, property settlement, life insurance",
            "Post-petition earnings of individual debtor are NOT property of the estate in Chapter 7 (but ARE in Chapter 13)",
        ],
        defenses=[
            "Spendthrift trust interest excluded under 541(c)(2)",
            "Power exercisable solely for benefit of entity other than debtor excluded",
            "Debtor's interest expired pre-petition",
            "Property was properly exempted under 522",
        ],
        remedies=[
            "Turnover of property to trustee under 542",
            "Recovery of property transferred post-petition under 549",
            "Trustee may abandon burdensome or valueless property under 554",
        ],
        leading_cases=[
            "United States v. Whiting Pools, 462 U.S. 198 (1983) - property seized by IRS is property of the estate subject to turnover",
            "Butner v. United States, 440 U.S. 48 (1979) - property interests determined by state law",
        ],
        category="estate",
        subcategory="property_of_estate",
        authority_score=0.92,
        confidence=0.90,
        related_topics=["trustee_powers_and_duties", "bankruptcy_exemptions", "automatic_stay_362"],
        practice_tips=[
            "541 is deliberately broad — err on side of inclusion when analyzing",
            "180-day post-petition acquisition rule catches inheritances and life insurance",
            "Individual Chapter 7: post-petition wages NOT estate property",
            "Individual Chapter 13: post-petition wages ARE estate property (1306)",
            "Butner doctrine: look to state law to determine nature of debtor's property interest",
        ],
        texas_notes="Under Texas community property law, both spouses' community property interests become property of the estate when either spouse files. This can have dramatic consequences for the non-filing spouse. Sole management community property of the debtor is fully in the estate; joint management community property requires coordination.",
    ),

    # ========== CLAIM PRIORITY ==========
    DoctrineCacheBlock(
        topic="priority_claims_waterfall",
        summary="Sections 507(a) and 726 establish the priority waterfall for distribution in bankruptcy. In Chapter 7, distribution follows strict priority: secured claims first (from collateral), then unsecured claims in order of priority, then general unsecured, then equity. In Chapter 11/13, the plan must respect these priorities or obtain class consent. Priority claims must be paid in full unless the claimant agrees otherwise.",
        key_statutes=["11 USC 507(a)", "11 USC 726", "11 USC 1129(a)(9)"],
        elements=[
            "507(a)(1): Domestic support obligations (DSO) — highest priority after secured claims",
            "507(a)(2): Administrative expenses under 503(b) — trustee fees, professional fees, operating expenses",
            "507(a)(3): Gap period claims in involuntary cases",
            "507(a)(4): Employee wages/commissions within 180 days before filing (up to $15,150 per employee)",
            "507(a)(5): Employee benefit plan contributions within 180 days",
            "507(a)(6): Grain farmer and fisherman claims (up to $7,575)",
            "507(a)(7): Consumer deposits (up to $3,350)",
            "507(a)(8): Tax claims (income, property, employment, excise) with specific lookback periods",
            "507(a)(9): FDIC deposit commitments",
            "507(a)(10): DUI personal injury claims",
            "726 distribution order: Priority → general unsecured → penalties → interest → equity",
        ],
        defenses=[
            "Claim does not meet statutory requirements for priority status",
            "Tax claim is for a period outside the lookback windows",
            "Administrative claim was not necessary for preservation of estate",
        ],
        remedies=[
            "Priority claims paid before general unsecured creditors",
            "In Chapter 11/13, priority claims must be paid in full through the plan (1129(a)(9), 1322(a)(2))",
            "507(b) superpriority for failed adequate protection — paid before all other administrative claims",
        ],
        leading_cases=[
            "Howard Delivery Service v. Zurich American Insurance Co., 547 U.S. 651 (2006) - workers comp premiums are not 507(a)(5) priority",
            "Begier v. IRS, 496 U.S. 53 (1990) - trust fund tax payments not property of the estate",
        ],
        category="claims",
        subcategory="priority",
        authority_score=0.90,
        confidence=0.88,
        related_topics=["proof_of_claim_and_claims_process", "plan_confirmation_requirements", "tax_debt_discharge_rules"],
        practice_tips=[
            "DSO has highest priority — must be current for Chapter 13 plan confirmation",
            "Administrative claims can consume significant estate value in Chapter 11",
            "Tax priority periods are complex — create year-by-year chart",
            "In Chapter 13, priority claims must be paid 100% (no cramdown on priority)",
        ],
        texas_notes="Texas franchise tax and sales tax claims receive priority under 507(a)(8). Property tax claims for assessments within 1 year are also priority. Track priority vs. non-priority tax years carefully.",
    ),

    # ========== SINGLE ASSET REAL ESTATE ==========
    DoctrineCacheBlock(
        topic="single_asset_real_estate",
        summary="A single asset real estate (SARE) debtor owns real property constituting a single property or project generating substantially all gross income, with no more than $2M in noncontingent, liquidated secured debts. SARE cases face expedited stay relief under 362(d)(3): the debtor must file a reasonable plan within 90 days or begin making interest payments on the secured claim's value.",
        key_statutes=["11 USC 101(51B)", "11 USC 362(d)(3)"],
        elements=[
            "Real property constituting single property or project",
            "Generates substantially all gross income of the debtor",
            "Aggregate noncontingent, liquidated secured debts do not exceed $2,000,000 (BAPCPA removed the cap for large SARE)",
            "Within 90 days: file plan with reasonable possibility of confirmation OR begin monthly interest payments on secured claim value",
            "Expedited stay relief: creditor need only show SARE status and failure to meet 90-day requirement",
        ],
        defenses=[
            "Debtor is not a SARE debtor (multiple properties, significant non-real-estate income)",
            "Debtor filed a plan with reasonable possibility of confirmation within 90 days",
            "Debtor began making adequate interest payments within 90 days",
        ],
        remedies=[
            "Stay relief for secured creditor to pursue foreclosure",
            "Debtor may retain property by filing plan or making interest payments",
        ],
        leading_cases=[
            "In re 8th Street Village Ltd., 94 B.R. 993 (Bankr. N.D. Ill. 1988) - SARE definition analysis",
        ],
        category="chapter_types",
        subcategory="sare",
        authority_score=0.80,
        confidence=0.80,
        related_topics=["automatic_stay_362", "chapter_11_reorganization_overview", "adequate_protection"],
        practice_tips=[
            "90-day clock starts upon filing — have plan strategy ready before filing",
            "BAPCPA removed the $4M cap — all SARE debtors now subject to 362(d)(3)",
            "Interest payments at current fair market rate on value of secured claim",
            "Lender strategy: file SARE motion early to apply pressure",
        ],
        texas_notes="Significant SARE filings in Texas due to commercial real estate and oil/gas property. Midland and Houston divisions see regular SARE cases. Texas nonjudicial foreclosure makes stay relief particularly impactful.",
    ),

    # ========== INVOLUNTARY BANKRUPTCY ==========
    DoctrineCacheBlock(
        topic="involuntary_bankruptcy",
        summary="Section 303 permits creditors to file an involuntary petition against a debtor under Chapter 7 or 11. If the debtor has 12 or more creditors, three or more must join with aggregate unsecured claims of at least $18,600. If fewer than 12 creditors, a single creditor may file. The debtor may contest, and if the petition is dismissed, the court may award damages including attorneys fees against the petitioning creditors.",
        key_statutes=["11 USC 303", "11 USC 303(h)", "11 USC 303(i)"],
        elements=[
            "Debtor must be generally not paying debts as they become due (303(h)(1))",
            "OR custodian was appointed within 120 days (303(h)(2))",
            "12+ creditors: 3 or more petitioning creditors with aggregate unsecured claims >= $18,600",
            "Fewer than 12 creditors: 1 petitioning creditor with claim >= $18,600",
            "Claims must not be contingent as to liability or subject to bona fide dispute",
            "Not available for farmers, family farmers, or charitable organizations (303(a))",
        ],
        defenses=[
            "Debtor is generally paying debts as they become due",
            "Petitioning creditors' claims are subject to bona fide dispute",
            "Debtor is a farmer, family farmer, or charitable organization",
            "Petitioning creditors do not meet threshold requirements",
        ],
        remedies=[
            "Order for relief entered if grounds established",
            "If dismissed: costs, attorneys fees, and damages (including punitive) against petitioners under 303(i)",
            "303(i) damages serve as strong deterrent to bad faith involuntary petitions",
        ],
        leading_cases=[
            "In re Busick, 831 F.2d 745 (7th Cir. 1987) - bad faith involuntary petition damages",
        ],
        category="chapter_types",
        subcategory="involuntary",
        authority_score=0.78,
        confidence=0.80,
        related_topics=["automatic_stay_362", "chapter_7_liquidation_overview", "chapter_11_reorganization_overview"],
        practice_tips=[
            "Involuntary petitions are high-risk for petitioning creditors — 303(i) damages",
            "Bona fide dispute defense is heavily litigated — any legitimate dispute defeats petition",
            "Gap period between filing and order for relief creates special administrative priority claims",
        ],
    ),
]


# ============================================================================
# MODULE-LEVEL CACHE CONSTRUCTION
# ============================================================================

_DOCTRINE_CACHE: Optional[DoctrineCacheIndex] = None
_DOCTRINE_CACHE_HASH: Optional[str] = None


def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build the complete doctrine cache index from DOCTRINE_BLOCKS."""
    global _DOCTRINE_CACHE, _DOCTRINE_CACHE_HASH
    index = DoctrineCacheIndex()
    index.build(DOCTRINE_BLOCKS)
    _DOCTRINE_CACHE = index
    _DOCTRINE_CACHE_HASH = None
    return index


def get_doctrine_cache() -> DoctrineCacheIndex:
    """Get or build the doctrine cache singleton."""
    global _DOCTRINE_CACHE
    if _DOCTRINE_CACHE is None:
        _DOCTRINE_CACHE = build_doctrine_cache()
    return _DOCTRINE_CACHE


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Retrieve a single doctrine block by topic."""
    return get_doctrine_cache().get(topic)


def search_doctrines(query: str, top_k: int = 5) -> List[DoctrineCacheBlock]:
    """Search doctrine blocks by free text."""
    query_lower = query.lower()
    results: List[tuple] = []
    for block in DOCTRINE_BLOCKS:
        content = block.content_for_search().lower()
        score = 0.0
        query_tokens = query_lower.split()
        for token in query_tokens:
            if token in content:
                score += 1.0
                if token in block.topic.lower():
                    score += 2.0
                if token in block.category.lower():
                    score += 0.5
        if score > 0:
            results.append((score, block))
    results.sort(key=lambda x: x[0], reverse=True)
    return [block for _, block in results[:top_k]]


def get_all_doctrine_topics() -> List[str]:
    """Return all doctrine topic names."""
    return get_doctrine_cache().all_topics()


def get_all_doctrine_categories() -> Set[str]:
    """Return all doctrine categories."""
    return get_doctrine_cache().all_categories()


def get_coverage_map() -> Dict[str, Dict[str, Any]]:
    """Return a coverage map of all topics with staleness data."""
    coverage: Dict[str, Dict[str, Any]] = {}
    for block in DOCTRINE_BLOCKS:
        coverage[block.topic] = {
            "category": block.category,
            "subcategory": block.subcategory,
            "confidence": block.confidence,
            "authority_score": block.authority_score,
            "last_updated": block.last_updated,
            "staleness_days": block.staleness_days,
            "related_count": len(block.related_topics),
        }
    return coverage


def get_stale_doctrines(threshold_days: int = 90) -> List[DoctrineCacheBlock]:
    """Return doctrine blocks exceeding staleness threshold."""
    return [b for b in DOCTRINE_BLOCKS if b.staleness_days > threshold_days]


def get_doctrine_cache_hash() -> str:
    """Return SHA-256 hash of the doctrine cache for integrity verification."""
    global _DOCTRINE_CACHE_HASH
    if _DOCTRINE_CACHE_HASH is None:
        content = json.dumps(
            [b.to_dict() for b in DOCTRINE_BLOCKS],
            sort_keys=True,
            default=str,
        )
        _DOCTRINE_CACHE_HASH = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return _DOCTRINE_CACHE_HASH


def get_doctrine_cache_stats() -> Dict[str, Any]:
    """Return statistics about the doctrine cache."""
    categories: Dict[str, int] = {}
    for block in DOCTRINE_BLOCKS:
        categories[block.category] = categories.get(block.category, 0) + 1
    return {
        "total_blocks": len(DOCTRINE_BLOCKS),
        "categories": categories,
        "avg_confidence": sum(b.confidence for b in DOCTRINE_BLOCKS) / max(len(DOCTRINE_BLOCKS), 1),
        "avg_authority": sum(b.authority_score for b in DOCTRINE_BLOCKS) / max(len(DOCTRINE_BLOCKS), 1),
        "hash": get_doctrine_cache_hash(),
    }


def verify_doctrine_integrity() -> Dict[str, Any]:
    """Verify structural integrity of all doctrine blocks."""
    errors: List[str] = []
    warnings: List[str] = []
    for i, block in enumerate(DOCTRINE_BLOCKS):
        if not block.topic:
            errors.append(f"Block {i}: missing topic")
        if not block.summary:
            errors.append(f"Block {i} ({block.topic}): missing summary")
        if not block.key_statutes:
            warnings.append(f"Block {i} ({block.topic}): no key statutes")
        if not block.elements:
            warnings.append(f"Block {i} ({block.topic}): no elements")
        if not block.leading_cases:
            warnings.append(f"Block {i} ({block.topic}): no leading cases")
        if block.confidence < 0.5:
            warnings.append(f"Block {i} ({block.topic}): low confidence {block.confidence}")
    return {
        "valid": len(errors) == 0,
        "total_blocks": len(DOCTRINE_BLOCKS),
        "errors": errors,
        "warnings": warnings,
        "hash": get_doctrine_cache_hash(),
    }
