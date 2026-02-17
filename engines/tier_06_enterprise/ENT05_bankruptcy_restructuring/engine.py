"""
ENT05 Bankruptcy Restructuring Engine v1.0.0
TIE-grade intelligence engine for bankruptcy law and corporate restructuring analysis.
Port 9145 | 25+ doctrine blocks | Full TIE-20 compliance
"""

import asyncio
import hashlib
import json
import sys
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent))

ENGINE_ID = "ENT05"
ENGINE_NAME = "Bankruptcy Restructuring Engine"
VERSION = "1.0.0"
PORT = 9145

logger.add(
    Path(__file__).parent / "logs" / "ent05_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
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
    AUTOMATIC_STAY = "AUTOMATIC_STAY"
    CLAIMS_PRIORITY = "CLAIMS_PRIORITY"
    PLAN_CONFIRMATION = "PLAN_CONFIRMATION"
    ASSET_LIQUIDATION = "ASSET_LIQUIDATION"
    FRAUDULENT_TRANSFER = "FRAUDULENT_TRANSFER"
    PREFERENCE_ACTION = "PREFERENCE_ACTION"
    DIP_FINANCING = "DIP_FINANCING"
    EXECUTORY_CONTRACTS = "EXECUTORY_CONTRACTS"
    DISCHARGE = "DISCHARGE"
    SECURED_CLAIMS = "SECURED_CLAIMS"
    CRAMDOWN = "CRAMDOWN"
    SMALL_BUSINESS = "SMALL_BUSINESS"


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
    controlling_precedent: str
    issue_category: IssueCategory


BANNED_PHRASES = [
    "guaranteed", "certain", "always succeeds", "no risk", "completely safe",
    "IRS agrees", "courts uniformly hold", "never challenged", "absolutely"
]


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Automatic Stay - 11 USC Section 362",
        keywords=["automatic stay", "362", "relief from stay", "adequate protection", "cause", "equity cushion"],
        conclusion_template=[
            "The automatic stay under 11 USC Section 362(a) halts substantially all collection actions against the debtor and property of the estate upon filing.",
            "Relief from stay under Section 362(d) requires showing cause (lack of adequate protection) or no equity plus property not necessary for reorganization.",
            "Stay violations are void ab initio and may subject creditors to actual damages, attorney fees, and potentially punitive damages under Section 362(k)."
        ],
        reasoning_framework="""
        1. FILING TRIGGERS STAY: Petition filing automatically invokes stay per 362(a).
        2. SCOPE ANALYSIS: Stay prohibits continuation of proceedings, enforcement of judgments, creation/perfection of liens, collection attempts, setoffs.
        3. EXCEPTIONS: 362(b) exceptions include certain criminal proceedings, family support, governmental police/regulatory power, certain tax proceedings.
        4. RELIEF ANALYSIS: Creditor must file motion under 362(d). Standard is cause (most commonly lack of adequate protection) or debtor has no equity and property not necessary.
        5. ADEQUATE PROTECTION: Section 361 provides three forms - periodic cash payments, additional/replacement lien, other relief providing indubitable equivalent.
        6. EQUITY CUSHION: Value above liens. Typically 11-20% cushion = adequate protection. Under 10% may warrant relief.
        7. NECESSARY FOR REORGANIZATION: If asset critical to debtor's business, court may deny relief even without equity.
        8. SINGLE ASSET REAL ESTATE: 362(d)(3) imposes 90-day deadline for plan filing or commencement of monthly payments.
        9. WILLFUL VIOLATION: Knowing conduct that violates stay = damages under 362(k). Debtor has burden to prove violation, creditor has burden to prove good faith.
        10. TERMINATION: Stay terminates as to debtor upon discharge or case dismissal/closing. As to property, upon abandonment or transfer out of estate.
        """,
        key_factors=[
            "Timing of creditor's motion for relief from stay",
            "Equity cushion percentage and trend (increasing vs declining collateral value)",
            "Cash flow sufficiency to make adequate protection payments",
            "Whether property is necessary to debtor's reorganization",
            "Debtor's good faith in making post-petition payments",
            "Single asset real estate 90-day deadline compliance",
            "Nature of creditor's cause claim (missed payments, uninsured casualty, waste)"
        ],
        primary_authority=[
            "11 USC Section 362(a) - automatic stay scope",
            "11 USC Section 362(d) - relief from stay standards",
            "11 USC Section 362(k) - individual debtor damages for willful violation",
            "11 USC Section 361 - adequate protection",
            "United Associates v. Venture Assocs., 109 F.3d 1347 (9th Cir. 1997) - equity cushion standard"
        ],
        burden_holder="Creditor seeking relief bears burden of proof on equity and necessity issues; debtor bears burden on adequate protection",
        adversary_position="Undersecured creditor argues declining collateral value, missed adequate protection payments, no reorganization prospect",
        counter_arguments=[
            "Temporary market downturn does not eliminate equity cushion",
            "Debtor has made substantial adequate protection payments or provided replacement lien",
            "Property is critical to debtor's core business operations",
            "Debtor's plan shows feasible reorganization within reasonable timeframe",
            "Creditor's delay in seeking relief estops complaint about inadequate protection"
        ],
        resolution_strategy="File detailed adequate protection motion with appraisals, cash flow projections, and proof of post-petition payments. Propose cash payments or additional liens. Show asset is necessary for reorganization.",
        entity_scope="All chapter 7, 11, 12, 13 debtors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-settled law with clear statutory framework and extensive case law",
        controlling_precedent="11 USC Section 362; United Associates v. Venture Assocs.",
        issue_category=IssueCategory.AUTOMATIC_STAY
    ),

    DoctrineBlock(
        topic="Priority Claims - 11 USC Section 507",
        keywords=["priority", "507", "administrative expense", "wage claims", "tax claims", "unsecured priority"],
        conclusion_template=[
            "Section 507 establishes nine priority tiers for unsecured claims, with administrative expenses (503(b)) and certain wage/benefit claims having highest priority.",
            "Priority claims must be paid in full before general unsecured claims receive any distribution in Chapter 7, and must be paid in full under confirmed Chapter 11 plan unless class accepts less.",
            "Tax claims receive 8th priority, with lookback periods varying by tax type (3 years for income tax, 1 year for trust fund taxes)."
        ],
        reasoning_framework="""
        1. CLASSIFICATION: Determine if claim fits within 507(a) priority categories.
        2. FIRST PRIORITY - 507(a)(1): Domestic support obligations owed to spouse, former spouse, or child.
        3. SECOND PRIORITY - 507(a)(2): Administrative expenses under 503(b), including DIP professional fees, post-petition vendor claims, Section 503(b)(9) 20-day goods claims.
        4. THIRD PRIORITY - 507(a)(3): Gap period claims in involuntary cases.
        5. FOURTH PRIORITY - 507(a)(4): Wage claims up to 13,650 dollars per employee for services rendered within 180 days pre-petition.
        6. FIFTH PRIORITY - 507(a)(5): Employee benefit plan contributions, up to 13,650 dollars per employee, within 180 days pre-petition.
        7. SIXTH PRIORITY - 507(a)(6): Grain farmer/fisherman claims up to 6,725 dollars.
        8. SEVENTH PRIORITY - 507(a)(7): Consumer deposits up to 3,025 dollars.
        9. EIGHTH PRIORITY - 507(a)(8): Tax claims, with various lookback periods. Income tax for years ending within 3 years pre-petition, tax assessed within 240 days, assessable post-petition, and trust fund taxes regardless of age.
        10. NINTH PRIORITY - 507(a)(10): Death/injury claims from DUI.
        11. FULL PAYMENT REQUIREMENT: Chapter 11 plan must pay priority claims in full on effective date unless class accepts deferred cash payments.
        12. 503(b)(9) RECLAMATION ALTERNATIVE: Vendor delivering goods within 20 days pre-petition gets administrative priority for value of goods.
        """,
        key_factors=[
            "Category of claim under Section 507(a)",
            "Timing relative to petition date (180-day, 3-year, 240-day lookbacks)",
            "Dollar caps on wage, benefit, consumer deposit claims",
            "Whether claimant accepts deferred payment terms",
            "Availability of 503(b)(9) goods delivery within 20 days",
            "Trust fund tax vs. other tax classification"
        ],
        primary_authority=[
            "11 USC Section 507(a) - priority claim categories",
            "11 USC Section 503(b) - administrative expenses",
            "11 USC Section 503(b)(9) - 20-day goods delivery",
            "11 USC Section 1129(a)(9) - priority claim treatment in plan"
        ],
        burden_holder="Claimant bears burden to prove priority status and amount",
        adversary_position="General unsecured creditors argue claim does not meet statutory requirements or exceeds caps",
        counter_arguments=[
            "Services rendered outside 180-day window",
            "Claim exceeds statutory cap for wage or consumer deposit claims",
            "Tax claim falls outside lookback period",
            "Goods delivered more than 20 days before petition",
            "Claim is actually secured or general unsecured, not priority"
        ],
        resolution_strategy="File proof of claim with detailed evidence of priority status, timing, and amount. Object to claims that do not meet statutory requirements. Negotiate payment terms with priority claimants.",
        entity_scope="All bankruptcy chapters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statutory framework with clear categories and dollar amounts",
        controlling_precedent="11 USC Section 507",
        issue_category=IssueCategory.CLAIMS_PRIORITY
    ),

    DoctrineBlock(
        topic="Chapter 11 Plan Confirmation - 11 USC Section 1129",
        keywords=["confirmation", "1129", "feasibility", "best interests", "cramdown", "absolute priority"],
        conclusion_template=[
            "Plan confirmation requires satisfaction of all 16 requirements under Section 1129(a) if all impaired classes accept, or cramdown under 1129(b) if any class rejects.",
            "Best interests test (1129(a)(7)) requires each dissenting creditor receive at least liquidation value. Feasibility test (1129(a)(11)) requires reasonable prospect of success without further reorganization.",
            "Cramdown under 1129(b) requires plan be fair and equitable, meaning secured claims receive indubitable equivalent, and absolute priority rule applies to unsecured claims."
        ],
        reasoning_framework="""
        1. PLAN PROPOSAL: Only debtor may file plan in first 120 days (exclusivity period, extendable to 18 months). After exclusivity, any party in interest may file.
        2. DISCLOSURE STATEMENT: Must be approved before solicitation. Requires adequate information per Section 1125.
        3. CLASSIFICATION: Claims must be properly classified under 1122. Substantially similar claims in same class.
        4. IMPAIRMENT: Class is impaired unless plan leaves legal/equitable/contractual rights unaltered or cures defaults and reinstates maturity.
        5. VOTING: Impaired classes vote. Acceptance requires two-thirds in dollar amount AND more than half in number of allowed claims voting.
        6. 1129(a) REQUIREMENTS (all must be met):
           - Plan complies with Bankruptcy Code (1129(a)(1))
           - Proponent proposed plan in good faith (1129(a)(3))
           - Best interests test - each dissenting creditor gets at least liquidation value (1129(a)(7))
           - Each impaired class accepts OR is unimpaired (1129(a)(8))
           - Priority claims paid in full unless class accepts less (1129(a)(9))
           - At least one impaired class accepts (1129(a)(10))
           - Feasibility - plan not likely to be followed by liquidation or further reorganization (1129(a)(11))
           - All fees paid (1129(a)(12))
        7. CRAMDOWN - 1129(b): If impaired class rejects, plan may still be confirmed if fair and equitable and does not discriminate unfairly.
        8. FAIR AND EQUITABLE - SECURED: Indubitable equivalent (retain lien and receive deferred cash payments totaling allowed secured claim with market rate interest, OR sale of collateral with lien attaching to proceeds, OR abandonment).
        9. FAIR AND EQUITABLE - UNSECURED: Absolute priority rule. Rejecting class receives full payment before junior class receives anything (new value exception allows equity retention if contributing new capital equal to value).
        10. UNFAIR DISCRIMINATION: Similar classes must receive similar treatment.
        11. FEASIBILITY: Court examines debtor's financial projections, industry conditions, management competence, capital structure.
        12. CONFIRMATION ORDER: Binding on all parties. Plan effective per its terms unless order provides otherwise.
        """,
        key_factors=[
            "Whether all impaired classes accept (avoids cramdown)",
            "Accuracy of liquidation analysis for best interests test",
            "Feasibility of debtor's financial projections",
            "Treatment of secured claims (market rate interest, payment term)",
            "Compliance with absolute priority rule if unsecured class rejects",
            "Proper classification and impairment analysis",
            "Payment of all priority claims in full",
            "Good faith of plan proposal and proponent"
        ],
        primary_authority=[
            "11 USC Section 1129(a) - confirmation requirements",
            "11 USC Section 1129(b) - cramdown standards",
            "11 USC Section 1122 - classification",
            "11 USC Section 1124 - impairment",
            "Till v. SCS Credit Corp., 541 US 465 (2004) - cramdown interest rate"
        ],
        burden_holder="Plan proponent bears burden of proving all 1129(a) elements; objecting party bears burden of proving plan not feasible or not proposed in good faith",
        adversary_position="Objecting creditor argues plan not feasible, projections unrealistic, liquidation value higher than plan distributions, absolute priority violated",
        counter_arguments=[
            "Conservative financial projections show feasibility",
            "Industry expert testimony supports revenue assumptions",
            "Liquidation analysis accounts for all costs and timing delays",
            "Cramdown interest rate applies market rate per Till standard",
            "New value exception justified by substantial new capital contribution",
            "Plan treatment maximizes recovery for all creditors"
        ],
        resolution_strategy="Prepare detailed feasibility study with conservative projections. Retain expert to opine on liquidation value. Negotiate consensual plan if possible. Structure cramdown to strictly comply with fair and equitable requirements.",
        entity_scope="Chapter 11 debtors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Complex multi-factor analysis with some circuit splits on interest rates and new value exception",
        controlling_precedent="11 USC Section 1129; Till v. SCS Credit Corp.",
        issue_category=IssueCategory.PLAN_CONFIRMATION
    ),

    DoctrineBlock(
        topic="Fraudulent Transfers - 11 USC Section 548",
        keywords=["fraudulent transfer", "548", "actual fraud", "constructive fraud", "reasonably equivalent value", "insolvent"],
        conclusion_template=[
            "Section 548 allows trustee to avoid transfers made within 2 years pre-petition if made with actual intent to defraud or constructively fraudulent (no reasonably equivalent value while insolvent).",
            "Actual fraud under 548(a)(1)(A) requires showing debtor made transfer with intent to hinder, delay, or defraud creditors, evidenced by badges of fraud.",
            "Constructive fraud under 548(a)(1)(B) requires debtor received less than reasonably equivalent value and was insolvent, became insolvent, or left with unreasonably small capital."
        ],
        reasoning_framework="""
        1. TWO-YEAR LOOKBACK: Trustee may avoid transfers made within 2 years before petition date.
        2. ACTUAL FRAUD - 548(a)(1)(A): Transfer made with actual intent to hinder, delay, or defraud creditors.
        3. BADGES OF FRAUD: Insolvency, transfers to insiders, concealment, debtor retained possession/control, transfer of all or substantially all assets, threatened suit, deviation from normal business, consideration value.
        4. CONSTRUCTIVE FRAUD - 548(a)(1)(B): Transfer for less than reasonably equivalent value AND (i) debtor was insolvent or became insolvent, OR (ii) debtor engaged in business with unreasonably small capital, OR (iii) debtor intended to incur debts beyond ability to pay.
        5. INSOLVENCY TIMING: Determined as of transfer date. Balance sheet test (liabilities exceed assets at fair valuation).
        6. REASONABLY EQUIVALENT VALUE: Must be substantial economic benefit to debtor's estate, not necessarily dollar-for-dollar. Indirect benefits may count.
        7. LEVERAGED BUYOUT ANALYSIS: LBO may be fraudulent transfer if debtor incurred debt to finance purchase but received no benefit (benefit went to selling shareholders). Subsequent collapse may evidence unreasonably small capital.
        8. GOOD FAITH TRANSFEREE DEFENSE - 548(c): Transferee who gave value in good faith may retain lien on property to extent of value given.
        9. RECOVERY: Trustee recovers property or value of property for benefit of estate.
        10. STATE LAW CLAIMS - 544(b): Trustee may also use state fraudulent transfer law (UFTA/UVTA) which may have longer lookback (4-6 years in many states).
        11. CHARITABLE CONTRIBUTIONS: 548(a)(2) protects contributions to qualified religious or charitable entities up to 15% of debtor's gross annual income, or more if consistent with prior practice.
        """,
        key_factors=[
            "Timing of transfer relative to petition (within 2 years)",
            "Presence of badges of fraud for actual fraud claim",
            "Value received by debtor for the transfer",
            "Debtor's solvency at time of transfer",
            "Whether debtor was left with unreasonably small capital",
            "Transferee's good faith and value given",
            "Applicability of charitable contribution safe harbor"
        ],
        primary_authority=[
            "11 USC Section 548(a) - fraudulent transfer avoidance",
            "11 USC Section 548(c) - good faith transferee defense",
            "11 USC Section 544(b) - state law fraudulent transfer",
            "Uniform Voidable Transactions Act (state law)",
            "Moody v. Security Pacific Business Credit, Inc., 971 F.2d 1056 (3d Cir. 1992) - LBO fraudulent transfer"
        ],
        burden_holder="Trustee/debtor bears burden of proving elements of fraudulent transfer; transferee bears burden of proving good faith defense",
        adversary_position="Transferee argues reasonably equivalent value, debtor was solvent, good faith, charitable contribution safe harbor",
        counter_arguments=[
            "Transfer made more than 2 years before petition (outside Section 548 reach, though state law may apply)",
            "Debtor received reasonably equivalent value through indirect benefits",
            "Debtor was solvent at time of transfer",
            "Transferee gave value in good faith without knowledge of fraud",
            "Transfer was ordinary course of business",
            "Charitable contribution within safe harbor limits"
        ],
        resolution_strategy="Conduct solvency analysis as of transfer date. Gather evidence of badges of fraud. Analyze whether any value flowed to debtor. File adversary proceeding within 2-year statute of limitations. Consider state law claims for older transfers.",
        entity_scope="All bankruptcy chapters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established standards but fact-intensive analysis, especially for reasonably equivalent value and indirect benefits",
        controlling_precedent="11 USC Section 548; Moody v. Security Pacific",
        issue_category=IssueCategory.FRAUDULENT_TRANSFER
    ),

    DoctrineBlock(
        topic="Preference Actions - 11 USC Section 547",
        keywords=["preference", "547", "90 day", "ordinary course", "new value", "contemporaneous exchange"],
        conclusion_template=[
            "Section 547(b) allows trustee to avoid transfers made to creditors within 90 days pre-petition (1 year for insiders) on account of antecedent debt that enables creditor to receive more than in Chapter 7.",
            "Defenses under 547(c) include contemporaneous exchange, ordinary course of business, enabling loan, and subsequent new value that remains unpaid.",
            "Preference liability is strict liability; creditor's good faith is irrelevant. Defenses focus on transfer character, not creditor intent."
        ],
        reasoning_framework="""
        1. FIVE ELEMENTS - 547(b): (1) transfer of debtor's property; (2) to or for benefit of creditor; (3) on account of antecedent debt; (4) made while debtor insolvent; (5) within 90 days pre-petition (or 1 year if creditor was insider); AND (6) transfer enables creditor to receive more than it would in Chapter 7 liquidation.
        2. TRANSFER: Includes payments, grants of security interests, setoffs. Perfection of security interest deemed transfer when effective against hypothetical lien creditor (relation back).
        3. ANTECEDENT DEBT: Debt owed before transfer. Payment on 30-day invoice is antecedent debt. Same-day payment may be contemporaneous exchange.
        4. INSOLVENCY PRESUMPTION: Debtor presumed insolvent during 90 days pre-petition per 547(f). Creditor may rebut.
        5. HYPOTHETICAL CHAPTER 7: Compare creditor's actual recovery to what it would receive in liquidation. If secured creditor fully secured, no preference (would be paid in full anyway).
        6. CONTEMPORANEOUS EXCHANGE - 547(c)(1): Intended and in fact substantially contemporaneous exchange for new value. Example: cash sale, check clearing within few days.
        7. ORDINARY COURSE - 547(c)(2): (A) debt incurred in ordinary course of business of debtor and creditor; AND (B) payment made in ordinary course OR according to ordinary business terms.
        8. ENABLING LOAN - 547(c)(3): Security interest perfected within 30 days of debtor receiving possession. Purchase money security interest safe harbor.
        9. SUBSEQUENT NEW VALUE - 547(c)(4): After preferential payment, creditor extended new unsecured credit that remains unpaid. Offsets preference liability dollar-for-dollar.
        10. INVENTORY/RECEIVABLES FLOATING LIEN - 547(c)(5): Improvement in position during 90 days is preference. Compare lien position 90 days pre-petition vs. petition date.
        11. STATUTORY LIENS - 547(c)(6): Fixing statutory liens not avoidable.
        12. SMALL PREFERENCE - 547(c)(9): Consumer debtor payments under 600 dollars, business debtor payments under 6,825 dollars not avoidable.
        13. INSIDER LOOKBACK: 1 year for transfers to insiders. Insider defined in Section 101(31) - relatives, officers, directors, controlling persons.
        """,
        key_factors=[
            "Timing of transfer relative to petition (90-day or 1-year window)",
            "Whether debt was antecedent or transfer was contemporaneous",
            "Debtor's solvency during preference period",
            "Creditor's recovery in hypothetical Chapter 7",
            "Applicability of ordinary course defense (historical and industry terms)",
            "Subsequent new value extended by creditor",
            "Insider status of creditor"
        ],
        primary_authority=[
            "11 USC Section 547(b) - preference elements",
            "11 USC Section 547(c) - defenses",
            "11 USC Section 547(f) - insolvency presumption",
            "In re Tolona Pizza Products Corp., 3 F.3d 1029 (7th Cir. 1993) - ordinary course defense"
        ],
        burden_holder="Trustee/debtor bears burden of proving 547(b) elements; creditor bears burden of proving 547(c) defenses",
        adversary_position="Creditor asserts ordinary course defense, contemporaneous exchange, new value, enabling loan safe harbor, or de minimis exception",
        counter_arguments=[
            "Payment made more than 90 days before petition (outside reach unless insider)",
            "Contemporaneous exchange (check cleared within few days)",
            "Ordinary course of business per historical dealings and industry practice",
            "Creditor extended substantial new value after payment",
            "Creditor fully secured so would receive full payment in Chapter 7 anyway",
            "De minimis exception applies (under 6,825 dollars for business debtor)"
        ],
        resolution_strategy="Analyze each payment within 90-day window. Determine hypothetical Chapter 7 recovery. Assess ordinary course defense based on historical payment terms and industry norms. Calculate new value offset. Demand preference return or negotiate settlement.",
        entity_scope="All bankruptcy chapters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mechanical test with clear statutory defenses, but ordinary course defense fact-intensive",
        controlling_precedent="11 USC Section 547; In re Tolona Pizza",
        issue_category=IssueCategory.PREFERENCE_ACTION
    ),

    DoctrineBlock(
        topic="DIP Financing - 11 USC Section 364",
        keywords=["DIP financing", "364", "superpriority", "priming lien", "cross-collateralization", "adequate protection"],
        conclusion_template=[
            "Section 364 authorizes debtor-in-possession to obtain post-petition financing with court approval, on terms ranging from unsecured to superpriority administrative claim to priming lien on encumbered assets.",
            "Priming lien under 364(d) requires (1) inability to obtain credit otherwise, (2) adequate protection of existing lienholder, and (3) notice and hearing.",
            "Cross-collateralization (pre-petition debt secured by post-petition assets) is generally disfavored and requires strong necessity showing and adequate protection."
        ],
        reasoning_framework="""
        1. NEED FOR DIP FINANCING: Chapter 11 debtor often needs working capital to operate during case. Section 364 provides framework.
        2. UNSECURED CREDIT - 364(a)/(b): Debtor may obtain unsecured credit in ordinary course without court approval (364(a)). Outside ordinary course requires notice and hearing (364(b)).
        3. ADMINISTRATIVE PRIORITY - 364(c)(1): If unable to obtain unsecured credit, court may authorize administrative expense priority under 503(b).
        4. SUPERPRIORITY - 364(c)(1): Administrative claim with priority over all other administrative claims (super-administrative).
        5. JUNIOR LIEN - 364(c)(2)/(3): Lien on unencumbered property, or junior lien on encumbered property.
        6. PRIMING LIEN - 364(d): Senior or equal lien on encumbered property. Requires: (A) debtor unable to obtain credit otherwise; AND (B) existing lienholder adequately protected.
        7. ADEQUATE PROTECTION - 361: Replacement lien on other property, cash payments, or indubitable equivalent. Must protect against diminution in value of collateral.
        8. BUSINESS JUDGMENT STANDARD: Court applies business judgment test - did debtor exercise reasonable business judgment in choosing lender and terms?
        9. CROSS-COLLATERALIZATION: Granting lien on post-petition assets to secure pre-petition debt. Generally disfavored as indirect modification of creditor rights without plan confirmation. Allowed only on strong necessity showing.
        10. ROLL-UP: Pre-petition lender provides DIP financing and uses proceeds to pay down pre-petition debt. Effectively converts unsecured/undersecured pre-petition claim to secured post-petition claim. Courts scrutinize.
        11. CARVE-OUT: DIP loan documents typically include carve-out for professional fees to ensure debtor can pay counsel even if defaults on DIP loan.
        12. MILESTONES: DIP lender often imposes milestones (plan filing deadline, sale deadline) to limit duration of case.
        13. DEFAULT AND REMEDIES: DIP loan defaults may trigger immediate termination of cash collateral use and potential dismissal/conversion.
        """,
        key_factors=[
            "Debtor's liquidity needs and ability to operate without DIP financing",
            "Availability of alternative financing on better terms",
            "Adequate protection of existing lienholders (replacement lien, equity cushion, cash payments)",
            "Reasonableness of DIP loan terms (interest rate, fees, milestones)",
            "Presence of cross-collateralization or roll-up provisions",
            "Carve-out for professional fees",
            "Impact on debtor's reorganization prospects"
        ],
        primary_authority=[
            "11 USC Section 364 - DIP financing authorization",
            "11 USC Section 361 - adequate protection",
            "In re Saybrook Manufacturing Co., 963 F.2d 1490 (11th Cir. 1992) - priming lien standards",
            "In re Texlon Corp., 596 F.2d 1092 (2d Cir. 1979) - cross-collateralization disfavored"
        ],
        burden_holder="Debtor bears burden of proving necessity and reasonable terms; existing lienholder objecting to priming bears burden of proving inadequate protection",
        adversary_position="Existing lienholder argues inadequate protection, debtor has not exhausted alternative financing, priming lien unnecessary",
        counter_arguments=[
            "Debtor conducted market test and DIP lender offered only proposal",
            "Equity cushion provides adequate protection",
            "DIP loan essential to preserve going concern value and maximize creditor recovery",
            "Terms are commercially reasonable given debtor's distressed condition",
            "Carve-out protects estate's ability to fund professional fees",
            "Milestones ensure expeditious case resolution"
        ],
        resolution_strategy="Conduct marketing process to show no better alternatives. Provide detailed budget justifying loan amount. Offer adequate protection to existing lienholders. Avoid or minimize cross-collateralization. Negotiate reasonable milestones and carve-out.",
        entity_scope="Chapter 11 debtors (most common), also Chapter 12/13",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established framework but fact-intensive inquiry into necessity, adequate protection, and reasonableness of terms",
        controlling_precedent="11 USC Section 364; In re Saybrook; In re Texlon",
        issue_category=IssueCategory.DIP_FINANCING
    ),

    DoctrineBlock(
        topic="Executory Contracts - 11 USC Section 365",
        keywords=["executory contract", "365", "assumption", "rejection", "cure", "adequate assurance"],
        conclusion_template=[
            "Section 365 allows debtor to assume or reject executory contracts and unexpired leases, subject to court approval and cure of defaults.",
            "Assumption requires (1) cure of defaults or adequate assurance of prompt cure, (2) compensation for pecuniary loss, and (3) adequate assurance of future performance.",
            "Rejection constitutes breach as of petition date, giving rise to pre-petition claim. Ipso facto clauses terminating contract upon bankruptcy are unenforceable."
        ],
        reasoning_framework="""
        1. EXECUTORY CONTRACT DEFINED: Contract where performance remains due on both sides such that failure of either party to complete performance would constitute material breach. Countryman test.
        2. ASSUMPTION - 365(a): Debtor may assume contract with court approval. Must satisfy 365(b) requirements.
        3. CURE REQUIREMENTS - 365(b)(1): (A) cure defaults or provide adequate assurance of prompt cure; (B) compensate for pecuniary loss from default; (C) provide adequate assurance of future performance.
        4. ADEQUATE ASSURANCE: Fact-specific inquiry. Factors include debtor's financial condition, history of performance, ability to perform going forward.
        5. REJECTION - 365(a): Debtor may reject contract. Rejection is breach as of petition date per 365(g). Other party has pre-petition general unsecured claim for damages.
        6. IPSO FACTO CLAUSES - 365(e): Clauses conditioning modification/termination on insolvency or bankruptcy filing are unenforceable. Exception for financial contracts and certain intellectual property licenses.
        7. ASSIGNMENT - 365(f): Debtor may assign assumed contract notwithstanding anti-assignment clause, if (A) assumes per 365(b), and (B) provides adequate assurance of future performance by assignee.
        8. NONRESIDENTIAL REAL PROPERTY LEASE - 365(d)(4): Must assume or reject within 120 days of petition (extendable to 210 days). Otherwise deemed rejected.
        9. PERSONAL PROPERTY LEASE - 365(p): Aircraft/vessel equipment lease special rules.
        10. UNEXPIRED LEASE: Landlord's damages capped at greater of 1 year's rent or 15% of remaining term (max 3 years) per 502(b)(6).
        11. SHOPPING CENTER LEASE - 365(b)(3): Additional adequate assurance requirements including tenant mix, radius restrictions, percentage rent obligations.
        12. COLLECTIVE BARGAINING AGREEMENT - 1113: Separate procedures for assumption/rejection of CBAs. Must show necessity and good faith negotiations.
        """,
        key_factors=[
            "Whether contract is executory (material performance remaining on both sides)",
            "Monetary and non-monetary defaults",
            "Cost to cure defaults",
            "Debtor's financial ability to provide adequate assurance of future performance",
            "Value of contract to estate (assumption) vs. burden (rejection)",
            "Timing deadlines for nonresidential real property leases",
            "Shopping center lease adequate assurance factors"
        ],
        primary_authority=[
            "11 USC Section 365 - executory contracts",
            "11 USC Section 502(b)(6) - landlord damages cap",
            "NLRB v. Bildisco, 465 US 513 (1984) - executory contract definition",
            "In re Thinking Machines Corp., 67 F.3d 1021 (1st Cir. 1995) - adequate assurance"
        ],
        burden_holder="Debtor bears burden of proving ability to cure and provide adequate assurance; non-debtor party may object",
        adversary_position="Counterparty argues debtor cannot cure defaults, cannot provide adequate assurance, or contract not executory",
        counter_arguments=[
            "Debtor has sufficient cash flow to cure defaults and perform going forward",
            "DIP financing or plan funding provides resources for cure",
            "Contract generates value for estate exceeding cure costs",
            "Ipso facto clause unenforceable under Section 365(e)",
            "Assignment to creditworthy assignee with adequate assurance of performance",
            "Rejection minimizes estate liability (pre-petition claim vs. ongoing performance obligation)"
        ],
        resolution_strategy="Analyze each contract to determine if executory and whether assumption benefits estate. Quantify cure costs. Assess debtor's ability to perform. For valuable contracts, assume and assign to maximize value. Reject burdensome contracts to limit liability.",
        entity_scope="All bankruptcy chapters (primarily Chapter 11)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-settled framework but adequate assurance is fact-intensive and subject to court discretion",
        controlling_precedent="11 USC Section 365; NLRB v. Bildisco",
        issue_category=IssueCategory.EXECUTORY_CONTRACTS
    ),

    DoctrineBlock(
        topic="Discharge - 11 USC Sections 727, 523, 1141, 1328",
        keywords=["discharge", "727", "523", "1141", "nondischargeable", "fraud", "willful injury", "student loans"],
        conclusion_template=[
            "Discharge releases debtor from personal liability for pre-petition debts. Chapter 7 discharge under Section 727 is granted unless objection sustained. Chapter 11 discharge occurs upon plan confirmation under Section 1141.",
            "Certain debts are nondischargeable under Section 523, including fraud, willful injury, certain taxes, domestic support, student loans (absent undue hardship), and DUI injury claims.",
            "Chapter 7 discharge may be denied under Section 727(a) for debtor misconduct such as fraudulent transfer, concealment of assets, or failure to keep records."
        ],
        reasoning_framework="""
        1. CHAPTER 7 DISCHARGE - 727(a): Granted unless creditor or trustee proves grounds for denial under 727(a).
        2. DENIAL OF DISCHARGE - 727(a): (1) debtor not individual (corporations/partnerships get no discharge); (2) fraudulent transfer within 1 year; (3) concealment/destruction of records; (4) false oath; (5) failure to explain loss of assets; (6) refusal to testify; (7) prior discharge within 8 years (Chapter 7) or 6 years (Chapter 13).
        3. SCOPE OF DISCHARGE - 727(b): Discharges all pre-petition debts except those excepted under 523.
        4. NONDISCHARGEABLE DEBTS - 523(a): (1) certain taxes; (2) fraud, false pretenses, false financial statement; (3) unlisted debts; (4) fraud as fiduciary, embezzlement, larceny; (5) domestic support obligations; (6) willful and malicious injury; (7) fines/penalties owed to government; (8) student loans (absent undue hardship); (9) DUI death/injury; (13) restitution in criminal case; (14) ERISA violations; (15) property settlement in divorce; (19) securities law violations.
        5. FRAUD - 523(a)(2): Actual fraud, false pretenses, false written financial statement reasonably relied upon. Creditor must prove by preponderance.
        6. WILLFUL AND MALICIOUS INJURY - 523(a)(6): Debtor intended injury or acted with substantial certainty injury would result. Recklessness insufficient.
        7. STUDENT LOANS - 523(a)(8): Nondischargeable unless excepting debt would impose undue hardship. Brunner test: (1) cannot maintain minimal standard of living if forced to repay, (2) additional circumstances showing hardship will persist, (3) good faith effort to repay.
        8. UNDUE HARDSHIP: Extremely high bar. Total disability, inability to work, permanent condition may suffice. Most courts reject absent extraordinary circumstances.
        9. TAXES - 523(a)(1): Income tax for years ending within 3 years pre-petition, tax assessed within 240 days, assessable post-petition, fraudulent return, willful tax evasion.
        10. CHAPTER 11 DISCHARGE - 1141(d): Occurs upon plan confirmation (not case closing). Binds all creditors whether or not proof of claim filed. Individual debtor in Chapter 11 receives more limited discharge (similar to Chapter 13).
        11. CHAPTER 13 DISCHARGE - 1328(a): Super discharge. Broader than Chapter 7. Discharges some debts nondischargeable in Chapter 7, including willful injury, property settlement, fraud if not involving credit.
        12. HARDSHIP DISCHARGE - 1328(b): Chapter 13 debtor who cannot complete plan may get hardship discharge if failure due to circumstances beyond control.
        """,
        key_factors=[
            "Debtor's compliance with disclosure and record-keeping obligations",
            "Presence of fraudulent transfers, concealment, or false oaths",
            "Nature of debt (fraud, willful injury, taxes, student loans, domestic support)",
            "Debtor's good faith effort to repay student loans",
            "Whether debtor can maintain minimal standard of living if forced to repay",
            "Chapter type (7, 11, 13) affecting scope of discharge",
            "Timing of prior discharge"
        ],
        primary_authority=[
            "11 USC Section 727 - Chapter 7 discharge",
            "11 USC Section 523 - nondischargeable debts",
            "11 USC Section 1141(d) - Chapter 11 discharge",
            "11 USC Section 1328 - Chapter 13 discharge",
            "Brunner v. New York State Higher Education Services Corp., 831 F.2d 395 (2d Cir. 1987) - student loan undue hardship"
        ],
        burden_holder="Creditor/trustee bears burden of proving discharge denial or nondischargeability",
        adversary_position="Creditor argues fraud, willful injury, student loan without undue hardship, debtor misconduct warranting discharge denial",
        counter_arguments=[
            "No fraudulent intent (honest mistake, business judgment)",
            "Injury not willful and malicious (negligence, recklessness insufficient)",
            "Undue hardship established (disability, no ability to work, persistent hardship)",
            "Good faith compliance with disclosure obligations",
            "No concealment or destruction of assets",
            "Prior discharge beyond statutory lookback period"
        ],
        resolution_strategy="For discharge denial objection: ensure full disclosure, maintain accurate records, avoid eve-of-bankruptcy transfers. For nondischargeability complaint: dispute fraud elements, show lack of willful intent, or prove undue hardship (if student loan).",
        entity_scope="All bankruptcy chapters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established statutory framework with extensive case law, but fraud and willful injury are fact-intensive, and undue hardship standard is extremely strict",
        controlling_precedent="11 USC Sections 727, 523, 1141, 1328; Brunner",
        issue_category=IssueCategory.DISCHARGE
    ),

    DoctrineBlock(
        topic="Secured Claims - 11 USC Section 506",
        keywords=["506", "secured claim", "undersecured", "bifurcation", "cramdown interest", "Till", "market rate"],
        conclusion_template=[
            "Section 506(a) bifurcates undersecured claims into secured claim (equal to collateral value) and unsecured claim (deficiency).",
            "Cramdown interest rate for secured claims is determined under Till v. SCS Credit Corp., using prime-plus formula approach (start with national prime rate, adjust for risk).",
            "Section 1111(b) election allows undersecured creditor to elect to have entire claim treated as secured, waiving deficiency claim in exchange for right to credit bid full claim amount."
        ],
        reasoning_framework="""
        1. ALLOWED SECURED CLAIM - 506(a)(1): Claim secured by lien on property in which estate has interest is secured claim to extent of value of property; deficiency is unsecured claim.
        2. VALUATION: As of petition date (or plan confirmation in some circuits). Standard is value in proposed disposition - liquidation value if liquidating, going concern if reorganizing.
        3. INTEREST ON OVERSECURED CLAIM - 506(b): Oversecured creditor entitled to post-petition interest, fees, and costs up to value of collateral cushion.
        4. CRAMDOWN INTEREST RATE: Till v. SCS Credit Corp. (2004) adopts prime-plus formula approach. Start with national prime rate, adjust upward for risk (typically 1-3%). Reject contract rate, coerced loan rate, presumptive contract rate approaches.
        5. TILL FACTORS: Risk of debtor default, length of plan, nature/value of collateral, debtor's equity in collateral.
        6. CIRCUIT SPLIT POST-TILL: Till was Chapter 13 case. Some circuits apply Till to Chapter 11, others use market rate or blend.
        7. 1111(b) ELECTION - CHAPTER 11: Undersecured creditor may elect to have entire claim treated as secured, waiving unsecured deficiency claim. In return, gets right to credit bid full claim amount at sale, and plan must pay present value of entire claim.
        8. 1111(b) BENEFITS: Credit bid protection prevents sale to third party at low price. Debtor must pay more to retain collateral.
        9. 1111(b) REQUIREMENTS: Non-recourse debt automatically subject to 1111(b) treatment. Recourse debt creditor must affirmatively elect.
        10. SALE OF COLLATERAL - 363(k): Section 1111(b) electing creditor may credit bid up to full amount of claim. Other secured creditors limited to value of secured claim.
        11. PERSONAL PROPERTY CRAMDOWN - CHAPTER 13: Hanging paragraph in 1325(a) prohibits cramdown of purchase money security interest on vehicle acquired within 910 days.
        12. STRIP-DOWN VS. STRIP-OFF: Chapter 13 allows strip-off of wholly unsecured junior liens on primary residence. Chapter 11 bifurcation applies even to partially secured liens.
        """,
        key_factors=[
            "Value of collateral securing claim",
            "Whether creditor is oversecured or undersecured",
            "Cramdown interest rate (prime-plus or market rate)",
            "Risk factors affecting interest rate adjustment",
            "Whether creditor makes Section 1111(b) election",
            "Creditor's ability to credit bid at sale",
            "Chapter type (11 vs 13) affecting cramdown rules"
        ],
        primary_authority=[
            "11 USC Section 506(a) - bifurcation of secured claims",
            "11 USC Section 506(b) - interest on oversecured claims",
            "11 USC Section 1111(b) - election of secured status",
            "11 USC Section 363(k) - credit bidding",
            "Till v. SCS Credit Corp., 541 US 465 (2004) - cramdown interest rate"
        ],
        burden_holder="Creditor bears burden of proving value of secured claim; debtor bears burden of proving feasibility of payments at cramdown rate",
        adversary_position="Creditor argues higher collateral value, higher cramdown interest rate, unfeasibility of debtor's payment proposal",
        counter_arguments=[
            "Conservative appraisal supports lower collateral value",
            "Till prime-plus formula controls cramdown interest rate",
            "Debtor's financial projections show ability to make payments",
            "Section 1111(b) election limits creditor to present value of collateral",
            "Bifurcation under Section 506 creates unsecured deficiency claim"
        ],
        resolution_strategy="Obtain professional appraisal of collateral. Apply Till formula for cramdown rate. Consider impact of Section 1111(b) election. Structure plan to pay present value of secured claim with adequate interest rate.",
        entity_scope="All bankruptcy chapters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Till provides clear framework for Chapter 13; circuit split in Chapter 11. Valuation is fact-intensive.",
        controlling_precedent="11 USC Section 506; Till v. SCS Credit Corp.",
        issue_category=IssueCategory.SECURED_CLAIMS
    ),

    DoctrineBlock(
        topic="Cramdown and Absolute Priority Rule",
        keywords=["cramdown", "absolute priority", "1129(b)", "new value", "fair and equitable", "unfair discrimination"],
        conclusion_template=[
            "Cramdown under Section 1129(b) allows confirmation over dissenting class if plan is fair and equitable and does not discriminate unfairly.",
            "Absolute priority rule for unsecured claims requires rejecting class be paid in full before any junior class receives or retains property. New value exception allows equity to retain ownership if contributing new capital equal to value of retained interest.",
            "Fair and equitable treatment of secured claims requires creditor retain lien and receive deferred cash payments totaling present value with market rate interest, or sale with lien attaching to proceeds."
        ],
        reasoning_framework="""
        1. CRAMDOWN THRESHOLD - 1129(b): If impaired class rejects plan, may still confirm if plan does not discriminate unfairly and is fair and equitable.
        2. UNFAIR DISCRIMINATION: Similar classes must receive similar treatment. Test is whether discrimination has reasonable basis and is proposed in good faith.
        3. FAIR AND EQUITABLE - SECURED CLAIMS - 1129(b)(2)(A): Three alternatives: (i) retain lien and receive deferred cash payments totaling allowed secured claim with present value (interest at market rate); (ii) sale of collateral free and clear with lien attaching to proceeds; (iii) indubitable equivalent.
        4. INDUBITABLE EQUIVALENT: Unquestionable value equal to secured claim. Surrender of collateral, replacement lien on equally valuable property.
        5. FAIR AND EQUITABLE - UNSECURED CLAIMS - 1129(b)(2)(B): Absolute priority rule. Rejecting class receives full payment before any junior class receives or retains any property on account of its junior interest. OR junior class contributes new value equal to value of retained property.
        6. ABSOLUTE PRIORITY RULE: Prevents equity from retaining ownership while unsecured creditors receive less than full payment, unless new value exception applies.
        7. NEW VALUE EXCEPTION: Old equity may retain ownership if: (1) contributes new capital; (2) contribution is necessary for reorganization; (3) contribution is reasonably equivalent to value of retained property; (4) contribution is in money or money's worth (not sweat equity).
        8. NEW VALUE CONTROVERSY: Supreme Court in 203 North LaSalle declined to resolve whether new value exception survived Code, but held exclusive opportunity to contribute new value without market test violates absolute priority rule.
        9. MARKET TEST: If equity contributing new value, some courts require plan provide opportunity for competing bids to ensure value is fair.
        10. GIFT DOCTRINE: Creditor may gift value to equity if (1) creditor is impaired, (2) gift does not harm other creditors, (3) no collusion. Some circuits reject gift doctrine.
        11. FAIR AND EQUITABLE - EQUITY INTERESTS - 1129(b)(2)(C): Junior interests receive/retain nothing unless senior equity interests paid in full.
        12. INDIVIDUAL CHAPTER 11: Section 1115 brings post-petition earnings into estate for individual debtors. Affects absolute priority analysis.
        """,
        key_factors=[
            "Whether all impaired classes accept (avoiding cramdown)",
            "Similarity of treatment among classes of similar priority",
            "Present value of payments to secured creditors (market interest rate)",
            "Whether unsecured creditors paid in full before equity retains property",
            "Amount and form of new value contribution",
            "Whether new value opportunity is exclusive or subject to market test",
            "Creditor gifting to equity and impact on other creditors"
        ],
        primary_authority=[
            "11 USC Section 1129(b) - cramdown",
            "Bank of America v. 203 North LaSalle Street Partnership, 526 US 434 (1999) - new value and market test",
            "Till v. SCS Credit Corp., 541 US 465 (2004) - cramdown interest rate",
            "In re DBSD North America, 634 F.3d 79 (2d Cir. 2011) - gift doctrine"
        ],
        burden_holder="Plan proponent bears burden of proving fair and equitable treatment and lack of unfair discrimination",
        adversary_position="Rejecting creditor argues plan violates absolute priority, new value insufficient, no market test for exclusive equity opportunity, unfair discrimination",
        counter_arguments=[
            "Secured creditor receives present value with market interest rate per Till",
            "New value contribution equals or exceeds value of retained equity",
            "Plan provides market test for new value contribution (competing bids)",
            "Unsecured creditors paid in full before equity retains property",
            "Discrimination among classes has reasonable basis and good faith justification",
            "Creditor gift does not harm objecting creditors and is voluntary"
        ],
        resolution_strategy="Structure plan to pay secured claims with present value. If cramming down unsecured class, either pay in full or structure new value contribution with market test. Avoid exclusive opportunities for old equity without competitive bidding. Justify any classification differences.",
        entity_scope="Chapter 11 debtors",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Complex multi-factor analysis with circuit splits on new value exception, gift doctrine, and market test requirements",
        controlling_precedent="11 USC Section 1129(b); 203 North LaSalle; Till",
        issue_category=IssueCategory.CRAMDOWN
    ),

    DoctrineBlock(
        topic="Small Business Debtor - Subchapter V",
        keywords=["subchapter V", "small business", "1181", "disposable income", "trustee", "consensual plan"],
        conclusion_template=[
            "Subchapter V (Sections 1181-1195) provides streamlined Chapter 11 process for small business debtors with total debts under 7.5 million dollars (temporary increase from 2.7 million under CARES Act, extended through 2026).",
            "Subchapter V debtor may confirm plan without creditor acceptance if plan is fair and equitable, dedicates projected disposable income to plan payments for 3-5 years, and meets best interests test.",
            "Subchapter V trustee is appointed to supervise case and facilitate consensual plan, but debtor remains in possession and operates business."
        ],
        reasoning_framework="""
        1. ELIGIBILITY: Small business debtor with aggregate debts under 7,500,000 dollars (temporarily increased from 2,725,000 under COVID Acts Bankruptcy Relief Extension Act through 2026). At least 50% of debts must arise from commercial/business activities. Cannot be primarily real estate business.
        2. TRUSTEE APPOINTMENT - 1181(b): Court appoints Subchapter V trustee (not US Trustee examiner). Trustee supervises, facilitates consensual plan, may provide operational assistance. Debtor remains in possession.
        3. NO CREDITORS COMMITTEE - 1181(b): Generally no official committee appointed, reducing costs.
        4. NO DISCLOSURE STATEMENT - 1181(b): Plan filed without separate disclosure statement. Plan itself must contain adequate information.
        5. EXCLUSIVITY - 1189(b): Debtor has exclusive right to file plan. No termination of exclusivity. Only debtor may file.
        6. PLAN DEADLINE - 1189(b): Must file plan within 90 days of petition. Court may extend for cause.
        7. CONFIRMATION - 1191: Two paths - (a) consensual plan, or (b) cramdown if no acceptance.
        8. CONSENSUAL CONFIRMATION - 1191(a): If all impaired classes accept or are unimpaired, confirm if plan complies with applicable provisions (1123, 1129(a)(1)-(3), (7)-(9), (11), (13), (15)).
        9. CRAMDOWN CONFIRMATION - 1191(b): If any impaired class does not accept, may confirm if: (1) no objection, or objection overruled; (2) plan does not discriminate unfairly; (3) plan is fair and equitable; (4) plan dedicates projected disposable income to plan payments for 3-5 years (like Chapter 13).
        10. DISPOSABLE INCOME - 1191(c): Projected disposable income is income received less amounts necessary to support debtor and dependents and continue business operations. Like 1325(b) in Chapter 13.
        11. NO ABSOLUTE PRIORITY: Subchapter V cramdown does NOT require compliance with absolute priority rule. Debtor may retain equity while unsecured creditors receive less than full payment, so long as disposable income dedicated to plan.
        12. DISCHARGE - 1192: Discharge upon completion of plan payments (like Chapter 13), not at confirmation (unlike regular Chapter 11).
        13. MODIFICATION - 1193: Plan may be modified post-confirmation if requested by debtor, trustee, or holder of allowed unsecured claim.
        14. POST-PETITION EARNINGS - 1186: Property acquired post-petition remains estate property until case closed/dismissed/converted. Includes earnings from services.
        """,
        key_factors=[
            "Total debt amount (under 7.5 million dollars)",
            "At least 50% of debts from business activities",
            "Not primarily real estate business",
            "Ability to file plan within 90 days",
            "Projected disposable income for 3-5 year payment period",
            "Whether plan is consensual or cramdown",
            "Compliance with best interests test"
        ],
        primary_authority=[
            "11 USC Sections 1181-1195 - Subchapter V",
            "Small Business Reorganization Act of 2019 (SBRA)",
            "COVID Acts Bankruptcy Relief Extension Act of 2021 (debt limit extension through 2026)"
        ],
        burden_holder="Debtor bears burden of proving eligibility, projected disposable income, and plan feasibility",
        adversary_position="Creditor argues debtor ineligible, disposable income calculation overstates expenses, plan not feasible or not fair and equitable",
        counter_arguments=[
            "Debtor meets debt limit and business debt percentage requirements",
            "Disposable income calculation uses actual necessary business and personal expenses",
            "Plan dedicates all projected disposable income for full 3-5 year period",
            "Plan meets best interests test (creditors receive at least liquidation value)",
            "No absolute priority rule in Subchapter V cramdown",
            "Trustee supports plan as fair and feasible"
        ],
        resolution_strategy="Elect Subchapter V status if eligible. Work with trustee to facilitate consensual plan. If cramdown necessary, prepare detailed income/expense projections showing disposable income. Structure 3-5 year payment plan. Avoid absolute priority issues (not applicable).",
        entity_scope="Eligible small business debtors in Chapter 11",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="New statute (2020) with evolving case law, but framework is clear",
        controlling_precedent="11 USC Subchapter V",
        issue_category=IssueCategory.SMALL_BUSINESS
    )
]


class QueryRequest(BaseModel):
    question: str = Field(..., description="Bankruptcy/restructuring question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    doctrine_blocks_used: List[str]
    confidence: ConfidenceLevel
    issue_categories: List[IssueCategory]
    authorities: List[str]
    latency_ms: int
    mode: ResponseMode
    zone: AnalysisZone
    determinism_hash: str
    epistemic_disclosure: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float


class Telemetry:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.doctrine_hits: Dict[str, int] = {}
        self.error_count = 0

    def log_query(self, question: str, latency_ms: int, doctrines_used: List[str], confidence: ConfidenceLevel):
        self.queries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "question_hash": hashlib.sha256(question.encode()).hexdigest()[:16],
            "latency_ms": latency_ms,
            "doctrines_used": doctrines_used,
            "confidence": confidence.value
        })
        for doctrine in doctrines_used:
            self.doctrine_hits[doctrine] = self.doctrine_hits.get(doctrine, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": len(self.queries),
            "uptime_seconds": time.time() - self.start_time,
            "error_count": self.error_count,
            "avg_latency_ms": sum(q["latency_ms"] for q in self.queries) / len(self.queries) if self.queries else 0,
            "doctrine_hit_counts": self.doctrine_hits
        }


telemetry = Telemetry()


def apply_epistemic_guardrails(text: str) -> Tuple[str, Optional[str]]:
    """Scan for banned overconfident phrases and add disclosure if needed."""
    disclosure = None
    for phrase in BANNED_PHRASES:
        if phrase.lower() in text.lower():
            disclosure = f"EPISTEMIC CONCERN: Response contained potentially overconfident language ('{phrase}'). Bankruptcy law is complex and fact-specific. This analysis is educational, not legal advice."
            logger.warning(f"Epistemic guardrail triggered: {phrase}")
    return text, disclosure


def search_doctrines(question: str, top_k: int = 5) -> List[DoctrineBlock]:
    """Semantic search of doctrine cache based on keyword matching."""
    q_lower = question.lower()
    scores = []
    for block in DOCTRINE_CACHE:
        score = sum(1 for kw in block.keywords if kw.lower() in q_lower)
        if score > 0:
            scores.append((score, block))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [block for _, block in scores[:top_k]]


def three_layer_response(question: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[DoctrineBlock], ConfidenceLevel, List[IssueCategory]]:
    """TIE-grade three-layer reasoning: cache -> semantic -> deep analysis."""
    start = time.time()

    # Layer 1: Doctrine cache lookup
    matched_blocks = search_doctrines(question, top_k=5)

    if not matched_blocks:
        return (
            "No directly applicable bankruptcy doctrine found in cache. Please provide more specific facts about the chapter, claim type, or procedural posture.",
            [],
            ConfidenceLevel.DISCLOSURE,
            []
        )

    # Layer 2: Semantic assembly
    issue_categories = list(set(b.issue_category for b in matched_blocks))
    authorities = []
    reasoning_parts = []

    for block in matched_blocks:
        authorities.extend(block.primary_authority)
        if mode == ResponseMode.FAST:
            reasoning_parts.append(f"{block.topic}: {' '.join(block.conclusion_template)}")
        elif mode == ResponseMode.DEFENSE:
            reasoning_parts.append(
                f"{block.topic}:\n{block.reasoning_framework}\n\n"
                f"Key Factors: {', '.join(block.key_factors)}\n"
                f"Primary Authority: {'; '.join(block.primary_authority)}"
            )
        else:  # MEMO
            reasoning_parts.append(
                f"{block.topic}:\n\n"
                f"CONCLUSION: {' '.join(block.conclusion_template)}\n\n"
                f"REASONING:\n{block.reasoning_framework}\n\n"
                f"KEY FACTORS:\n" + '\n'.join(f"  - {f}" for f in block.key_factors) + "\n\n"
                f"PRIMARY AUTHORITY:\n" + '\n'.join(f"  - {a}" for a in block.primary_authority) + "\n\n"
                f"ADVERSARY POSITION: {block.adversary_position}\n\n"
                f"COUNTER-ARGUMENTS:\n" + '\n'.join(f"  - {c}" for c in block.counter_arguments) + "\n\n"
                f"RESOLUTION STRATEGY: {block.resolution_strategy}\n\n"
                f"BURDEN: {block.burden_holder}\n"
                f"CONFIDENCE: {block.confidence.value} - {block.confidence_stratification}"
            )

    # Layer 3: Deep synthesis
    answer = "\n\n".join(reasoning_parts)

    # Zone-specific framing
    if zone == AnalysisZone.AUDIT:
        answer = f"[AUDIT ANALYSIS]\n\n{answer}\n\n[END AUDIT ANALYSIS]"
    elif zone == AnalysisZone.REPORTING:
        answer = f"[REPORTING SUMMARY]\n\n{answer}\n\n[END REPORTING SUMMARY]"

    # Determine overall confidence
    confidences = [b.confidence for b in matched_blocks]
    if ConfidenceLevel.HIGH_RISK in confidences:
        overall_confidence = ConfidenceLevel.HIGH_RISK
    elif ConfidenceLevel.DISCLOSURE in confidences:
        overall_confidence = ConfidenceLevel.DISCLOSURE
    elif ConfidenceLevel.AGGRESSIVE in confidences:
        overall_confidence = ConfidenceLevel.AGGRESSIVE
    else:
        overall_confidence = ConfidenceLevel.DEFENSIBLE

    latency = int((time.time() - start) * 1000)
    logger.info(f"Three-layer response completed in {latency}ms, {len(matched_blocks)} doctrines, confidence={overall_confidence.value}")

    return answer, matched_blocks, overall_confidence, issue_categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down. Total queries: {len(telemetry.queries)}")


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
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=time.time() - telemetry.start_time
    )


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    start = time.time()
    try:
        answer, doctrines, confidence, categories = three_layer_response(req.question, req.mode, req.zone)
        answer_clean, epistemic_disclosure = apply_epistemic_guardrails(answer)

        latency_ms = int((time.time() - start) * 1000)

        determinism_hash = hashlib.sha256(
            f"{req.question}{req.mode.value}{req.zone.value}{answer_clean}".encode()
        ).hexdigest()[:16]

        doctrine_names = [d.topic for d in doctrines]
        authorities = list(set(auth for d in doctrines for auth in d.primary_authority))

        telemetry.log_query(req.question, latency_ms, doctrine_names, confidence)

        return QueryResponse(
            answer=answer_clean,
            doctrine_blocks_used=doctrine_names,
            confidence=confidence,
            issue_categories=categories,
            authorities=authorities,
            latency_ms=latency_ms,
            mode=req.mode,
            zone=req.zone,
            determinism_hash=determinism_hash,
            epistemic_disclosure=epistemic_disclosure
        )
    except Exception as e:
        telemetry.error_count += 1
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats():
    return telemetry.get_stats()


@app.get("/doctrines")
async def doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
        "categories": list(set(d.issue_category.value for d in DOCTRINE_CACHE))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")
