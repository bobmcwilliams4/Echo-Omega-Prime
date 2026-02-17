"""
ENT03 Mergers & Acquisitions Intelligence Engine v1.0.0
TIE-20 Gold Standard - Asset/Stock Purchase, HSR, CFIUS, IRC 368, Delaware 251, MAC, R&W Insurance, Earnouts
Port: 9143 | ENGINE_ID: ENT03
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib, time, json
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

ENGINE_ID, ENGINE_NAME, VERSION, PORT = "ENT03", "Mergers & Acquisitions Engine", "1.0.0", 9143
logger.add(f"logs/ent03_ma_{datetime.now():%Y%m%d}.log", rotation="100 MB", retention="30 days", level="INFO")

class ResponseMode(str, Enum):
    FAST, DEFENSE, MEMO = "FAST", "DEFENSE", "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE, AGGRESSIVE, DISCLOSURE, HIGH_RISK = "DEFENSIBLE", "AGGRESSIVE", "DISCLOSURE", "HIGH_RISK"

class AnalysisZone(str, Enum):
    PLANNING, REPORTING, AUDIT = "PLANNING", "REPORTING", "AUDIT"

class IssueCategory(str, Enum):
    STRUCTURE, TAX, ANTITRUST, DILIGENCE, FINANCING, REGULATORY, CONTRACT, LABOR, IP, CLOSING = "STRUCTURE", "TAX", "ANTITRUST", "DILIGENCE", "FINANCING", "REGULATORY", "CONTRACT", "LABOR", "IP", "CLOSING"

@dataclass
class DoctrineBlock:
    topic: str; keywords: List[str]; conclusion_template: str; reasoning_framework: str
    key_factors: List[str]; primary_authority: List[str]; burden_holder: str
    adversary_position: str; counter_arguments: List[str]; resolution_strategy: str
    entity_scope: str; confidence: ConfidenceLevel; confidence_stratification: str
    controlling_precedent: str; category: IssueCategory

class QueryRequest(BaseModel):
    question: str = Field(..., description="M&A question")
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.PLANNING
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str; confidence: ConfidenceLevel; sources: List[str]; reasoning_chain: List[str]
    triggered_doctrines: List[str]; latency_ms: float; determinism_hash: str
    zone: AnalysisZone; mode: ResponseMode

class HealthResponse(BaseModel):
    status: str; engine_id: str; version: str; doctrines_loaded: int
    uptime_seconds: float; queries_processed: int

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Asset Purchase vs Stock Purchase Structure",
        keywords=["asset", "stock", "purchase", "structure", "338", "election"],
        conclusion_template="Asset purchases allow buyer to step up basis and exclude liabilities; stock purchases transfer entity intact. IRC 338(h)(10) election allows stock purchase with asset tax treatment.",
        reasoning_framework="Asset: Buyer selects assets/liabilities, stepped-up basis IRC 1060, no successor liability, excludes unwanted items, depreciation deductions. Stock: Contracts transfer automatically, no transfer taxes, simpler structure, preserves NOLs if continuity met, less third-party consent. IRC 338(h)(10): Available when target is S-corp or consolidated subsidiary, both parties elect Form 8023, stock sale treated as asset sale for tax, seller pays corporate-level tax on deemed sale, buyer gets stepped-up basis, due 15th day 9th month after acquisition. IRC 338(g): Buyer-only election for C-corps, rarely used (double tax).",
        key_factors=["Liability exposure", "Tax basis step-up value", "Contract assignments", "Transfer taxes", "Seller tax preference", "Regulatory complexity"],
        primary_authority=["IRC 1060 (allocation)", "IRC 338(h)(10)", "IRC 197 (intangibles)", "Treas Reg 1.338-1 to 1.338-11"],
        burden_holder="Buyer to prove economic benefit justifies complexity",
        adversary_position="Seller prefers stock sale for capital gains and clean exit",
        counter_arguments=["Asset requires individual transfers", "Assignability issues", "Higher transaction costs", "Loss of tax attributes"],
        resolution_strategy="Negotiate 338(h)(10) for asset treatment via stock purchase, or price adjustment for seller tax cost",
        entity_scope="C-corps and S-corps (338(h)(10) limited to S-corps and subsidiaries)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-settled statutory framework with extensive guidance",
        controlling_precedent="IRC 338 and Treasury Regulations",
        category=IssueCategory.STRUCTURE
    ),
    DoctrineBlock(
        topic="Hart-Scott-Rodino HSR Filing Thresholds",
        keywords=["HSR", "antitrust", "filing", "threshold", "FTC", "DOJ", "premerger"],
        conclusion_template="HSR Act 15 USC 18a requires premerger notification for transactions exceeding size thresholds, with 30-day waiting period (15 days for cash tender offers).",
        reasoning_framework="2024 Thresholds (adjusted annually): Size of Transaction >$111.4M automatic filing. Size of Person (if $111.4M-$445.5M): one party $222.7M+ assets/sales AND other $22.3M+. Transactions >$445.5M require filing regardless. Value Calculation: Include all consideration (cash, stock, debt, earnouts), voting securities at acquisition price, assets at FMV, aggregate acquisitions within 180 days. Waiting: 30 days standard, 15 days cash tender, starts day after substantial compliance, early termination possible, Second Request extends indefinitely. Exemptions: Below thresholds, investment-only <10%, intracompany, certain bank mergers, ordinary course real property.",
        key_factors=["Adjusted threshold amounts", "Aggregation of prior acquisitions", "Ultimate parent determination", "Timing constraints", "Gun-jumping penalty $50,740/day 2024", "Second Request burden"],
        primary_authority=["15 USC 18a (Clayton Act 7A)", "16 CFR 801 (coverage)", "16 CFR 802 (exemptions)", "16 CFR 803 (transmittal)"],
        burden_holder="Acquiring person to determine applicability and file",
        adversary_position="FTC/DOJ may challenge if anticompetitive",
        counter_arguments=["Market definition nuances", "Investment-only exemption", "Ordinary course exemption"],
        resolution_strategy="Calculate using adjusted amounts, file conservatively if close, request early termination",
        entity_scope="All acquiring persons except exempted",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Bright-line thresholds with detailed guidance",
        controlling_precedent="HSR Act and FTC premerger regulations",
        category=IssueCategory.ANTITRUST
    ),
    DoctrineBlock(
        topic="CFIUS Foreign Investment Review FIRRMA",
        keywords=["CFIUS", "foreign", "investment", "FIRRMA", "national security", "critical"],
        conclusion_template="FIRRMA expanded CFIUS jurisdiction to critical infrastructure, technology, and sensitive data, with mandatory filing for certain transactions.",
        reasoning_framework="Jurisdiction (31 CFR 800): Foreign control of US business, non-controlling in TID US businesses (critical tech/infra/data), real estate near sensitive facilities, foreign government investors. Mandatory Filing: Foreign government 49%+ in TID, critical tech requiring export license, Committee determines national security risk. TID Business: Critical technologies (ITAR, EAR, emerging/foundational), critical infrastructure (28 sectors Appendix A), sensitive personal data (>1M individuals). Timeline: 45-day review + 45-day investigation + 15-day presidential decision, safe harbor if no action in 45 days, can re-review non-notified up to 3 years post-close, presidential authority to block/unwind. Mitigation: NSA, limited tech use, board observer restrictions, data security, facilities access controls.",
        key_factors=["Foreign government ties", "Critical tech/infrastructure role", "Sensitive personal data access", "Proximity to military facilities", "Export control classification", "Non-notified review risk"],
        primary_authority=["50 USC 4565 (FIRRMA)", "31 CFR 800 (CFIUS)", "31 CFR 802 (real estate)", "EO 11858"],
        burden_holder="Foreign investor to demonstrate no national security risk",
        adversary_position="CFIUS may require mitigation or block if unmitigable",
        counter_arguments=["Allied nation investor", "Not export controlled", "Passive investment no control", "Not critical infrastructure"],
        resolution_strategy="File voluntarily if any TID or foreign government, propose mitigation upfront, consider US investor structure",
        entity_scope="Foreign persons acquiring US businesses/real estate",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statute clear but critical tech/infra definitions require analysis",
        controlling_precedent="FIRRMA and CFIUS regulations",
        category=IssueCategory.REGULATORY
    ),
    DoctrineBlock(
        topic="Tax-Free Reorganizations IRC Section 368",
        keywords=["tax-free", "reorganization", "368", "continuity", "merger", "stock"],
        conclusion_template="IRC 368 permits tax-free treatment for qualifying reorganizations meeting statutory requirements and continuity of interest, business enterprise, and business purpose.",
        reasoning_framework="Type A (Statutory Merger): State law merger, target merges into acquirer, 40%+ COI required, can use cash boot (triggers gain), most flexible. Type B (Stock-for-Stock): Voting stock for target stock, must acquire 80% control, solely for voting stock (no boot), can be creeping, target becomes subsidiary. Type C (Stock-for-Assets): Voting stock for substantially all assets (90% FMV net/70% gross), target liquidates, boot limited to 20%. Type D (Divisive/Acquisitive): Transfer to controlled corp + distribution, spin-offs/split-offs/split-ups, requires 80% control. Continuity: COI 40%+ equity interest, COBE acquirer continues business or uses significant assets, Business Purpose legitimate beyond tax avoidance. Tax Treatment: Shareholders no gain/loss on stock exchanged (carryover basis), boot recognized up to value, corporations no gain/loss (carryover basis/attributes).",
        key_factors=["Stock vs cash percentage", "State law merger compliance", "Voting stock requirement", "Substantially all assets test", "Pre-reorg distributions/redemptions", "Post-reorg continuity"],
        primary_authority=["IRC 368(a)(1)(A)-(G)", "IRC 354 (no gain/loss)", "Treas Reg 1.368-1(e) (COI)", "Rev Proc 77-37"],
        burden_holder="Taxpayer to establish all statutory and common-law requirements",
        adversary_position="IRS may challenge if lacks business purpose or continuity",
        counter_arguments=["Excessive boot disqualifies", "Post-acquisition sale breaks continuity", "Asset disposition violates COBE", "Step transaction collapses plan"],
        resolution_strategy="Structure 60%+ stock consideration, obtain tax opinion, consider IRS private letter ruling",
        entity_scope="Corporations only (not partnerships/LLCs)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Complex interaction of statutory rules and common-law doctrines with gray areas",
        controlling_precedent="IRC 368 and extensive continuity case law",
        category=IssueCategory.TAX
    ),
    DoctrineBlock(
        topic="Delaware Merger Statute DGCL Section 251",
        keywords=["Delaware", "merger", "251", "appraisal", "stockholder", "vote"],
        conclusion_template="DGCL 251 governs statutory mergers requiring board approval, stockholder vote (majority outstanding), and providing appraisal rights to dissenters.",
        reasoning_framework="Procedure: (1) Board adopts merger agreement, (2) Majority outstanding shares vote approval, (3) File Certificate of Merger with DE Secretary, (4) Effective upon filing or later specified. Vote: Majority of outstanding (not votes cast), each class separate if rights affected, short-form (253) no vote if parent owns 90%+, medium-form (251(h)) no target vote if public tender for all shares. Appraisal (262): Available to stockholders voting against, must perfect by written demand before vote and not voting favor, fair value determined by Court of Chancery excluding merger value, recent cases trend toward deal price as best evidence, quasi-appraisal even if not perfected if breach of fiduciary duty. Fiduciary Duties: Revlon if sale (maximize value), Unocal if defensive (reasonable response), enhanced scrutiny if conflicts, entire fairness if interested transaction.",
        key_factors=["Ownership percentage and vote count", "Appraisal arbitrage risk", "Stockholder meeting timing", "Board fiduciary duty standard", "Deal protection (termination fees, no-shops)", "MFW framework for conflicted controller"],
        primary_authority=["DGCL 251 (merger)", "DGCL 253 (short-form)", "DGCL 262 (appraisal)", "Weinberger v UOP", "Revlon v MacAndrews"],
        burden_holder="Board to demonstrate fiduciary duty compliance and proper procedure",
        adversary_position="Dissenting stockholders seek appraisal or breach challenge",
        counter_arguments=["Market price reflects fair value", "Board satisfied Revlon via market check", "MFW cleansed conflicts", "Business judgment rule applies"],
        resolution_strategy="Robust sale process, document deliberations, obtain fairness opinion, consider MFW if conflicted, price to minimize appraisal risk",
        entity_scope="Delaware corporations (most public companies)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-developed Delaware case law with clear procedures",
        controlling_precedent="DGCL and Delaware Court of Chancery precedents",
        category=IssueCategory.STRUCTURE
    ),
    DoctrineBlock(
        topic="Material Adverse Change MAC Clauses",
        keywords=["MAC", "MAE", "material adverse", "change", "effect", "closing condition"],
        conclusion_template="MAC clauses permit buyer to walk if target suffers qualifying adverse change between signing and closing, but narrowly construed and rarely successful.",
        reasoning_framework="Standard MAC: Any event/change/effect that has had or would reasonably be expected to have material adverse effect on business, assets, liabilities, financial condition, or results of operations, taken as a whole. Typical Carve-Outs (not MAC): General economic/market conditions, industry changes affecting peers similarly, acts of war/terrorism/disasters, changes in law/GAAP, failure to meet projections (absent underlying MAC), actions required by agreement, effects of announcement/pendency. Delaware Principles: Extremely high bar - materially adverse to long-term earnings power, short-term earnings misses insufficient, must be durationally significant (not temporary), buyer assumed risk of known trends, specific often trumps general. Notable Cases: IBP v Axcan (64% EBITDA decline NOT MAC), Frontier v Avaya (50%+ drop but settled), Akorn v Fresenius (regulatory failures constituted MAC), AB Stable v MAPS (COVID 90% revenue drop NOT MAC).",
        key_factors=["Magnitude and duration of change", "Long-term earnings power impact", "Disproportionate vs peers", "Carve-out exceptions", "Buyer knowledge at signing", "Specific disclosure schedules"],
        primary_authority=["IBP v Axcan 789 A.2d 14 (Del Ch 2001)", "Akorn v Fresenius 2018 WL 4719347", "AB Stable v MAPS 2020 WL 7024929"],
        burden_holder="Buyer to prove MAC under specific agreement language",
        adversary_position="Seller argues temporary, normal fluctuations, or carved out",
        counter_arguments=["Short-term already reversing", "Industry-wide carve-out triggers", "Buyer had knowledge", "Specific reps still true"],
        resolution_strategy="Draft narrow MAC with broad carve-outs and disproportionate qualifier, specific reps for key concerns, price adjustment or escrow for known risks",
        entity_scope="All merger agreements with closing conditions",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Fact-intensive high burden with limited successful invocations",
        controlling_precedent="Delaware Court of Chancery MAC case law",
        category=IssueCategory.CONTRACT
    ),
    DoctrineBlock(
        topic="Representations and Warranties Insurance",
        keywords=["RWI", "insurance", "warranty", "representation", "indemnity"],
        conclusion_template="R&W Insurance shifts indemnification risk from seller to insurer, allowing cleaner exits and reduced escrows, with buyer-side policies now market standard.",
        reasoning_framework="Types: Buyer-side (buyer purchases, claims directly, 95%+ market), seller-side (seller purchases to backstop indemnity, rare). Standard Terms: Retention 0.5-1.5% EV (buyer deductible), policy limit 10-30% EV (typically 10-15%), premium 2-6% of limit, coverage 3-6 years (statute of limitations), fundamental reps 6-7 years. Coverage: Unknown/undisclosed breaches of reps/warranties, excludes known issues/forward-looking/fraud, covers losses and defense costs, recourse retention (buyer bears first $X), tipping basket (once retention met covers all). Deal Impact: Seller indemnity capped at retention (mini-basket), escrow reduced/eliminated, survival periods match policy, reduces post-closing friction, enables complete exit. Underwriting: Insurer reviews documents and diligence, underwriting call with parties/counsel, identifies exclusions for known issues, 2-4 weeks from binding indication to policy.",
        key_factors=["Cost-benefit vs escrow/indemnity", "Seller tail liability elimination", "Diligence and disclosure quality", "Known issues requiring exclusions", "Claims administration risk", "Competitive auction favoring clean exit"],
        primary_authority=["Insurance policies governed by contract law of chosen jurisdiction", "State insurance regulations re surplus lines if non-admitted carrier", "No controlling statutes - purely contractual"],
        burden_holder="Buyer to prove loss from breach and satisfy retention",
        adversary_position="Insurer may deny based on exclusions, knowledge, or coverage gaps",
        counter_arguments=["Known issues should have been priced", "Diligence insufficient", "Claim in exclusion/retention", "Seller fraud voids coverage"],
        resolution_strategy="Thorough diligence to minimize exclusions, negotiate retention/limits based on risk, use experienced broker, consider seller mini-basket for disclosure incentive",
        entity_scope="Private M&A typically $50M+ enterprise value",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Market-standard terms with well-understood coverage and claims process",
        controlling_precedent="Insurance policy terms and general contract law",
        category=IssueCategory.CONTRACT
    ),
    DoctrineBlock(
        topic="Earnouts and Contingent Consideration",
        keywords=["earnout", "contingent", "milestone", "EBITDA", "revenue", "performance"],
        conclusion_template="Earnouts bridge valuation gaps via performance-contingent payments, but create disputes without clear definitions, calculation mechanics, and seller control provisions.",
        reasoning_framework="Structures: Financial metrics (EBITDA, revenue, margin targets), operational milestones (product launch, regulatory approval, customer acquisition), hybrid. Terms: Period 1-3 years (longer for pharma), target specific level, payment formula (% of excess, sliding scale), cap maximum payment, acceleration on change of control/buyer breach. Critical Drafting: EBITDA definition with adjustments (add-backs, one-time, purchase accounting), calculation methodology (GAAP vs non-GAAP, preparer, dispute resolution), seller involvement (non-compete, employment, consent for major decisions), business operation (good faith, reasonable best efforts), integration restrictions (cost allocations, transfer pricing), independent accounting firm review. Tax: If employment-contingent (compensation income, ordinary rates), if performance-contingent (purchase price, capital gains), IRC 483/1274 imputed interest on deferred payments, ASC 805 fair value at acquisition with mark-to-market. Common Disputes: Buyer reduced marketing to depress earnout, buyer accelerated expenses/deferred revenue, buyer integration impaired standalone performance, transfer pricing/cost allocations distorted results, seller left employment reducing performance.",
        key_factors=["Earnout metric definition clarity", "Seller influence on results post-close", "Buyer discretion over operations", "Integration plans impact on metrics", "Tax characterization as price vs compensation", "Probability of achieving targets"],
        primary_authority=["Sonoran Scanners v Perkinelmer 585 F.3d 535 (1st Cir 2009) (good faith)", "Lazard Tech v Qinetiq 2014 WL 6669891 (Del Ch 2014) (best efforts)", "ASC 805 (business combinations)", "IRC 483 (imputed interest)"],
        burden_holder="Party challenging earnout calculation proves breach",
        adversary_position="Buyer argues good faith decisions; seller argues manipulation",
        counter_arguments=["Business judgment protects buyer decisions", "Earnout gave buyer discretion", "Seller employment termination caused decline", "Market conditions not buyer actions"],
        resolution_strategy="Define EBITDA precisely with all adjustments, require operation consistent with past practice, provide seller limited veto rights, independent accounting review, escrow upfront payment portion",
        entity_scope="Common in private M&A with valuation gap",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High litigation risk due to inherent conflicts and ambiguous terms",
        controlling_precedent="State contract law and implied covenant of good faith",
        category=IssueCategory.CONTRACT
    ),
    DoctrineBlock(
        topic="Due Diligence and Sandbagging",
        keywords=["diligence", "VDR", "material", "disclosure", "sandbagging"],
        conclusion_template="Buyer's diligence does not waive indemnification for breached reps unless agreement contains pro-sandbagging clause, but knowledge affects materiality qualifiers and MAC.",
        reasoning_framework="Process: Virtual Data Room (seller posts, buyer reviews), management presentations (business, strategy, financials), Q&A (written questions/responses), expert review (legal, accounting, tax, environmental, IT), site visits (facilities, customer/supplier meetings). Scope by Deal Type: Public (limited, confirm-only relying on SEC filings), Private Equity buy-side (extensive 100+ day VDR across all functions), Strategic acquisition (focus on strategic fit, synergies, integration), Distressed (accelerated, focus on deal-breakers). Anti-Sandbagging vs Pro-Sandbagging: Anti (buyer cannot claim indemnity for known breaches), Pro (buyer can claim even for known breaches), Delaware Default pro-sandbagging (Abry Partners v F&W Acquisition), Most Agreements include explicit pro-sandbagging provision. Materiality Qualifiers: MAE defined term in agreement, Material/Materiality often $X threshold or percentage, Scrapes disclosure schedules often scrape materiality qualifiers for indemnity, Knowledge actual knowledge of specified individuals sometimes with inquiry. Disclosure Schedules: Lists exceptions to reps/warranties, must be specific and detailed to qualify, general disclosures or VDR dumps insufficient, updated at closing for changes since signing.",
        key_factors=["Sandbagging clause presence and scope", "Definition of materiality and MAE", "Buyer actual vs imputed knowledge", "Disclosure schedule quality and specificity", "Reliance on diligence vs seller reps", "Public vs private target customs"],
        primary_authority=["Abry Partners V v F&W Acquisition 891 A.2d 1032 (Del Ch 2006)", "CBS Inc v Ziff-Davis Publ'g 553 N.E.2d 997 (NY 1990)", "ABA Model Stock Purchase Agreement"],
        burden_holder="Seller to prove buyer had knowledge defeating indemnity (if anti-sandbagging)",
        adversary_position="Buyer argues knowledge irrelevant under pro-sandbagging; seller argues waiver",
        counter_arguments=["Buyer's diligence uncovered issue, cannot claim surprise", "Materiality qualifier means de minimis breach not actionable", "Disclosure schedule referenced VDR with full details", "Buyer knowledge defeats reliance"],
        resolution_strategy="Include explicit pro-sandbagging clause, define materiality clearly with dollar thresholds, scrape materiality qualifiers in indemnity, limit knowledge to actual knowledge of named individuals, require specific disclosure items",
        entity_scope="All M&A with reps/warranties and indemnification",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear Delaware precedent on pro-sandbagging default, but agreement terms control",
        controlling_precedent="Abry Partners and jurisdiction-specific case law on knowledge and reliance",
        category=IssueCategory.DILIGENCE
    ),
    DoctrineBlock(
        topic="Working Capital Adjustments",
        keywords=["working capital", "adjustment", "NWC", "peg", "target", "closing"],
        conclusion_template="Working capital adjustments true-up purchase price based on target's actual closing working capital vs peg amount, using specific definitions and calculation mechanics.",
        reasoning_framework="Mechanics: Peg/Target amount agreed at signing (usually trailing 12-month average), closing estimate (parties estimate closing WC, adjust price at close), post-closing true-up (final WC calculated 60-90 days post-close), dollar-for-dollar adjustment (buyer receives credit if below peg, pays seller if above). WC Definition: Current assets minus current liabilities, specific line items from balance sheet identified in agreement, excludes cash/debt/transaction expenses (enterprise value items), calculated consistent with sample WC statement. Common Disputes: Classification (is item current asset/liability or excluded?), calculation method (GAAP vs sample statement methodology), cutoff (timing of revenue recognition, expense accrual), inventory valuation (FIFO vs LIFO, obsolescence reserves), accounts receivable (bad debt reserves, contra-revenue items). Sample WC Statement: Prepared at signing showing calculation methodology, acts as binding template for closing calculation, specifies GAAP with specific exceptions, identifies each included/excluded line item. Resolution Process: Seller prepares initial closing statement (or buyer in some deals), buyer has 60-90 days to review and dispute, good faith negotiation period (30 days), independent accounting firm resolves remaining disputes, accounting firm decision final and binding, limited to specific disputed items (not full recalculation).",
        key_factors=["Peg amount negotiated vs trailing average", "WC level volatility", "Seasonal business considerations", "Sample statement precision and clarity", "Independent accounting firm selection process", "Escrow amount to secure adjustment"],
        primary_authority=["Contract law of governing jurisdiction", "GAAP or specified accounting principles", "No statutory authority - purely contractual"],
        burden_holder="Disputing party to prove calculation error under agreement terms",
        adversary_position="Opposing party defends calculation as consistent with sample statement",
        counter_arguments=["GAAP requires different treatment than sample", "Item should be classified differently", "Timing cutoff affects accruals", "Reserves excessive or insufficient"],
        resolution_strategy="Prepare detailed sample WC statement, specify GAAP with exceptions, engage independent accounting firm at signing to avoid selection disputes, escrow 10-20% of estimated adjustment, align definitions with company historical accounting",
        entity_scope="Most private M&A using locked-box or closing accounts mechanism",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-understood mechanism but execution details drive disputes",
        controlling_precedent="Merger agreement terms and specified accounting principles",
        category=IssueCategory.CONTRACT
    ),
    DoctrineBlock(
        topic="Tender Offers and Williams Act",
        keywords=["tender", "offer", "Williams Act", "14d", "13e", "schedule TO"],
        conclusion_template="Securities Exchange Act 14(d) regulates tender offers requiring Schedule TO disclosure, minimum 20 business day offer period, and all-holders/best-price rules.",
        reasoning_framework="Williams Act Requirements (15 USC 78n(d)): Schedule TO filed when tender offer commences, disclosure (offer terms, purpose, source of funds, buyer identity, plans), timing (minimum 20 business days, extended 10 days for competing offer or amendment), all-holders rule (open to all security holders), best-price rule (all tendering shareholders receive highest price paid), withdrawal rights (during offer period), pro rata acceptance (if oversubscribed). Issuer Tender Offers (13(e)): Company repurchasing own shares, Schedule TO filed by issuer, same timing/pricing rules, often used for going-private transactions. Merger Without Vote (DGCL 251(h)): Acquirer can complete merger without target stockholder vote if tender offer for all shares with minimum condition (majority outstanding), merger consummated promptly after tender, remaining stockholders receive same consideration, reduces timeline by eliminating stockholder meeting. Hostile Tender Offers: Schedule 14D-9 (target response recommend accept/reject/neutral), defensive measures (poison pill, white knight, Pac-Man defense), board fiduciary duties (Unocal review - threat analysis, proportionate response), Revlon duties (once sale inevitable, maximize value).",
        key_factors=["20 business day minimum offer period", "Minimum tender condition (typically 50%+ or 90%+ for short-form merger)", "Financing condition and committed financing", "Regulatory approval conditions (HSR, CFIUS)", "Target board recommendation or opposition", "Competing offers and deal protection"],
        primary_authority=["15 USC 78n(d) (Williams Act)", "17 CFR 240.14d-1 et seq (tender offer rules)", "17 CFR 240.13e-4 (issuer tenders)", "DGCL 251(h) (medium-form merger)"],
        burden_holder="Offeror to comply with Williams Act disclosure and timing requirements",
        adversary_position="Target board may recommend rejection and deploy defensive measures",
        counter_arguments=["Offer coercive and inadequate (Unocal)", "Financing not committed, condition illusory", "Regulatory approvals unlikely to obtain", "Target has superior alternative"],
        resolution_strategy="Ensure full Schedule TO disclosure, committed financing, reasonable minimum condition, negotiate with target board to avoid defensive measures, consider 251(h) structure to accelerate back-end merger",
        entity_scope="Public companies with registered equity securities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear SEC rules with detailed compliance requirements",
        controlling_precedent="Williams Act and SEC tender offer regulations",
        category=IssueCategory.STRUCTURE
    ),
    DoctrineBlock(
        topic="Indemnification Baskets and Caps",
        keywords=["indemnity", "basket", "cap", "deductible", "threshold", "survival"],
        conclusion_template="Indemnification provisions allocate post-closing risk through baskets (minimum claim thresholds), caps (maximum liability), and survival periods.",
        reasoning_framework="Basket Types: Deductible/Dollar-One (losses must exceed basket, then recover all), Tipping (losses must exceed basket, then recover only excess), Mini-Basket (applies only to non-fundamental reps, fundamental are dollar-one), Market 0.5-1% EV. Cap Structures: General cap (non-fundamental reps, market 10-25% EV), fundamental rep cap (higher or unlimited for title, authority, capitalization), tax/environmental (often separate higher caps or unlimited), fraud (unlimited and uncapped), multiple tiers (different caps for different rep categories). Survival Periods: General reps 12-24 months post-close, fundamental reps indefinite or statute of limitations, tax reps until statute expires plus 60 days (typically 3-6 years), environmental 3-5 years or statute, fraud indefinite (cannot contract away fraud liability). Market Terms by Deal Size: $50-250M (basket 1%, cap 10%, survival 18 months), $250M-1B (basket 0.75%, cap 10-15%, survival 12-18 months), $1B+ (basket 0.5%, cap 10-20%, survival 12 months). R&W Insurance Impact: Basket replaced by insurance retention (0.5-1.5%), cap replaced by policy limit (10-30%), seller indemnity often limited to retention amount only, fundamental reps may have seller indemnity up to full cap.",
        key_factors=["Relative bargaining power and deal competition", "R&W insurance use reducing seller exposure", "Risk profile and diligence findings", "Size of transaction (percentages scale)", "Seller creditworthiness and escrow amount", "Public vs private seller (public minimal indemnity)"],
        primary_authority=["Contract law of governing jurisdiction", "ABA Private Target M&A Deal Points Study (market terms)", "No statutory requirements - purely negotiated"],
        burden_holder="Buyer to prove loss, causation, and satisfaction of basket",
        adversary_position="Seller argues loss below basket, outside survival, or exceeds cap",
        counter_arguments=["Losses de minimis and below basket", "Claim after survival period expired", "Total claims exceed cap, must allocate pro rata", "Loss not caused by breach"],
        resolution_strategy="Negotiate basket/cap percentages based on market data for comparable deals, use R&W insurance to reduce seller exposure, escrow amount equal to or greater than basket plus expected near-term claims, specific increased caps for key risks identified in diligence",
        entity_scope="All private M&A with seller indemnification",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Market terms well-established with variation based on deal specifics",
        controlling_precedent="Merger agreement terms and general contract law",
        category=IssueCategory.CONTRACT
    ),
    DoctrineBlock(
        topic="Financing Conditions and Committed Financing",
        keywords=["financing", "committed", "condition", "MAC", "market", "flex"],
        conclusion_template="Buyer's obligation to close typically requires committed financing, with financing conditions limited to senior debt and equity committed by sponsor, while debt market conditions do not excuse performance.",
        reasoning_framework="Committed Financing Structure: Equity commitment letter (sponsor commits to fund equity portion), debt commitment letter (banks commit senior debt), limited conditionality (only breaches of target reps, regulatory denial, MAC), market flex (banks right to adjust terms - pricing, structure - based on market). Financing Condition in Merger Agreement: Private equity deals (financing condition typical but highly negotiated), strategic buyers (often no financing condition - balance sheet funding), sponsor must use reasonable best efforts (to obtain financing and satisfy conditions), target cooperation (provide financials, participate in marketing, deliver diligence). Reverse Termination Fee: Payable if buyer fails to close due to financing failure, typical range 3-8% EV, caps buyer liability (replaces specific performance remedy), often sole remedy absent fraud or intentional breach. Specific Performance: Target can require buyer to close if equity funded, limited to equity portion (cannot force debt to fund), conditioned on debt financing being available, declining remedy in large-cap M&A (reverse breakup fee preferred). SunGard Doctrine: If all conditions satisfied except unavailable financing buyer must close, buyer bears risk of committed financing failing to fund, banks' failure to fund does not excuse buyer, led to more robust reverse termination fees.",
        key_factors=["Debt vs equity commitment letter terms", "Financing condition scope and exceptions", "Reverse termination fee as percentage of deal value", "Specific performance availability", "Market flex provisions and pricing impact", "Target cooperation obligations"],
        primary_authority=["In re IBP Inc S'holders Litig 789 A.2d 14 (Del Ch 2001)", "Hexion Specialty Chems v Huntsman Corp 965 A.2d 715 (Del Ch 2008)", "Martin Marietta Materials v Vulcan Materials 56 A.3d 1072 (Del Ch 2012)"],
        burden_holder="Buyer to use reasonable best efforts to obtain financing and close",
        adversary_position="Target argues buyer did not satisfy efforts standard or financing available",
        counter_arguments=["MAC in target business excuses financing commitment", "Market MAC makes financing unavailable on committed terms", "Target failed to cooperate in financing process", "Buyer satisfied reasonable best efforts standard"],
        resolution_strategy="Obtain committed equity and debt financing before signing, limit debt commitment conditions to target MAC/reps, negotiate reverse termination fee as cap on liability, avoid specific performance remedy in favor of fee, include marketing period for debt syndication",
        entity_scope="Leveraged buyouts and large M&A requiring debt financing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-developed case law on efforts standards and financing failure allocation",
        controlling_precedent="Delaware Chancery Court precedents on financing conditions",
        category=IssueCategory.FINANCING
    ),
    DoctrineBlock(
        topic="Regulatory Approval Conditions and Efforts Standards",
        keywords=["regulatory", "HSR", "approval", "condition", "hell or high water", "efforts"],
        conclusion_template="Merger agreements condition closing on required regulatory approvals, with buyer's efforts standard ranging from reasonable best efforts to hell-or-high-water commitment depending on antitrust risk.",
        reasoning_framework="Standard Regulatory Conditions: HSR clearance (expiration of waiting period or early termination), CFIUS clearance (no adverse determination or mitigation agreement), industry regulators (FCC, FERC, state insurance, banking regulators), foreign antitrust (EU, UK, China, other jurisdictions). Efforts Standards: Reasonable efforts (take reasonable steps, no material burden), reasonable best efforts (more than reasonable, stop short of material detriment), best efforts (exhaust all options, only stop at extreme burden), hell or high water (no limitation, must accept any remedy to obtain approval). Antitrust Remedies Buyer May Be Required to Accept: Divestitures (sell overlapping business lines), behavioral remedies (firewalls, non-discrimination commitments), license requirements (license IP or facilities to competitors), caps on market share or customer concentration. Material Burdens and Carve-Outs: Revenue/EBITDA thresholds (no divestiture if exceeds $Xm or Y%), specified assets (protect certain crown jewel assets from divestiture), buyer business (limits on remedies affecting buyer's existing business), target business only (remedies limited to target operations). Reverse Termination Rights: If approval denied or unacceptable conditions imposed, reverse termination fee (3-10% of value) may be payable, sometimes no fee if regulatory denial (risk on target). Outside Date: 6-18 months from signing depending on complexity, extended if HSR Second Request or CFIUS review, automatic extensions for regulatory delays, either party can walk if outside date passes without approval.",
        key_factors=["Market overlap and HHI increase (antitrust risk)", "Foreign investment sensitivity (CFIUS risk)", "Industry-specific regulatory complexity", "Buyer willingness to accept divestitures", "Revenue/EBITDA carve-outs defining material burden", "Allocation of regulatory risk via fee or no fee"],
        primary_authority=["15 USC 18a (HSR Act)", "50 USC 4565 (CFIUS)", "Williams Cos v Energy Transfer 2016 WL 3576682 (Del Ch 2016) (efforts)", "Akorn v Fresenius 2018 WL 4719347 (Del Ch 2018) (efforts breach)"],
        burden_holder="Buyer to use specified efforts standard to obtain approvals",
        adversary_position="Target argues buyer did not satisfy efforts standard or improperly terminated",
        counter_arguments=["Remedy required exceeded material burden threshold", "Buyer used best efforts but approval denied", "Target's business changes caused regulatory issues", "Outside date expired through no fault of buyer"],
        resolution_strategy="Define efforts standard clearly with specific remedy limitations, set revenue/EBITDA caps on acceptable divestitures, exclude buyer's core business from remedies, reverse termination fee if buyer walks due to regulatory denial, realistic outside date with extensions",
        entity_scope="All M&A subject to HSR, CFIUS, or industry-specific regulation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fact-intensive efforts analysis but clear standards from case law",
        controlling_precedent="Williams Companies and Akorn on efforts obligations",
        category=IssueCategory.REGULATORY
    ),
    DoctrineBlock(
        topic="Non-Compete and Non-Solicitation Covenants",
        keywords=["non-compete", "non-solicit", "restrictive covenant", "goodwill", "blue pencil"],
        conclusion_template="Non-compete and non-solicitation covenants protect buyer's investment in acquired goodwill, enforceable if reasonable in scope, duration, and geography, with state-law variations on blue-pencil reformation.",
        reasoning_framework="Enforceability Requirements: Reasonable time (1-5 years typical, often 2-3 for non-compete), reasonable geography (limited to areas where business operates), reasonable scope (limited to competing business activities), legitimate business interest (protect goodwill, trade secrets, customer relationships), consideration (adequate paid for covenant - purchase price or continued employment). State-Law Variations: California (non-competes void except sale of business BPC 16600), Texas (enforceable if ancillary to transaction and reasonable BCC 15.50), Delaware (reasonableness standard, blue-pencil modification allowed), New York (enforceable if reasonable, no bright-line rules), Massachusetts (12-month limit under 2018 statute). Non-Solicitation of Customers: Prohibits soliciting customers of acquired business, more readily enforceable than non-compete, limited to actual customers not prospective, duration 2-5 years typical. Non-Solicitation of Employees: Prohibits hiring or soliciting target employees, 1-3 years typical, may carve out general solicitations (ads, recruiters), key employee definitions important. Blue-Pencil Doctrine: Court may narrow overbroad covenant to make enforceable, some states refuse to blue-pencil (all-or-nothing), divisible covenants more amenable to modification, avoid overreaching in drafting. Remedies: Injunctive relief (primary remedy for breach), monetary damages (difficult to prove and quantify), liquidated damages (may be specified in agreement), tolling (breach tolls running of period).",
        key_factors=["State law governing enforceability", "Seller role post-closing (employment, consulting, rollover)", "Nature of business and geographic footprint", "Customer relationships and goodwill protected", "Seller ability to earn livelihood elsewhere", "Blue-pencil availability in jurisdiction"],
        primary_authority=["Restatement (Second) of Contracts 188", "Cal Bus & Prof Code 16600 (non-competes void)", "Tex Bus & Com Code 15.50 (enforceability)", "Mass Gen Laws ch 149 24L (2018 non-compete statute)"],
        burden_holder="Buyer to prove covenant reasonable and breach occurred",
        adversary_position="Seller argues covenant overbroad, no legitimate interest, or not breached",
        counter_arguments=["Geographic scope too broad for actual operations", "Duration excessive given industry dynamics", "Seller not competing, only tangential field", "Covenant void in California as unrelated to sale"],
        resolution_strategy="Tailor geography to actual business footprint, limit duration to 2-3 years for non-compete and 3-5 for non-solicit, draft divisible covenants to aid blue-pencil, specify liquidated damages, consider employment/consulting agreements to add consideration, avoid California choice of law",
        entity_scope="All M&A where seller or key employees may compete post-closing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-settled reasonableness standard but state-specific enforcement variations",
        controlling_precedent="State law of governing jurisdiction and Restatement principles",
        category=IssueCategory.CONTRACT
    ),
]

class MergersAcquisitionsEngine:
    def __init__(self):
        self.doctrine_cache = {d.topic: d for d in DOCTRINE_CACHE}
        self.start_time = time.time()
        self.query_count = 0
        self.telemetry: Dict[str, List[float]] = defaultdict(list)
        self.coverage_map: Dict[str, int] = defaultdict(int)
        logger.info(f"{ENGINE_NAME} v{VERSION} initialized with {len(self.doctrine_cache)} doctrines")

    def query(self, req: QueryRequest) -> QueryResponse:
        start = time.time()
        self.query_count += 1
        logger.info(f"Query {self.query_count}: {req.question[:100]} | Mode: {req.mode} | Zone: {req.zone}")

        triggered = self._match_doctrines(req.question)
        if triggered:
            answer, confidence, sources, chain = self._generate_response(triggered, req)
        else:
            answer = "No specific M&A doctrine matched. Consider structure, tax, regulatory, or contractual framework."
            confidence = ConfidenceLevel.DISCLOSURE
            sources, chain = [], ["No doctrine cache hit", "General M&A principles apply"]

        latency = (time.time() - start) * 1000
        self.telemetry['latency'].append(latency)
        for topic in triggered:
            self.coverage_map[topic] += 1
        det_hash = self._determinism_hash(req.question, answer)
        self._log_audit_trail(req, answer, triggered, latency)
        logger.info(f"Response: {len(answer)} chars, {len(triggered)} doctrines, {latency:.1f}ms")

        return QueryResponse(
            answer=answer, confidence=confidence, sources=sources, reasoning_chain=chain,
            triggered_doctrines=triggered, latency_ms=round(latency, 2),
            determinism_hash=det_hash, zone=req.zone, mode=req.mode
        )

    def _match_doctrines(self, question: str) -> List[str]:
        q_lower = question.lower()
        matches = [topic for topic, doctrine in self.doctrine_cache.items() if any(kw in q_lower for kw in doctrine.keywords)]
        return matches[:5]

    def _generate_response(self, triggered: List[str], req: QueryRequest) -> tuple:
        doctrines = [self.doctrine_cache[t] for t in triggered]
        primary = doctrines[0]

        if req.mode == ResponseMode.FAST:
            answer = f"{primary.conclusion_template}\n\nKey Factors: {'; '.join(primary.key_factors[:3])}"
            chain = ["Cache hit", "Fast conclusion"]
        elif req.mode == ResponseMode.DEFENSE:
            answer = f"{primary.conclusion_template}\n\n{primary.reasoning_framework}\n\nAuthority: {'; '.join(primary.primary_authority)}\n\nBurden: {primary.burden_holder}\n\nCounterarguments: {'; '.join(primary.counter_arguments[:2])}"
            chain = ["Cache hit", "Full reasoning", "Authority cited", "Adversary position analyzed"]
        else:  # MEMO
            answer = f"MEMORANDUM\n\nIssue: {req.question}\n\nConclusion: {primary.conclusion_template}\n\nAnalysis:\n{primary.reasoning_framework}\n\nKey Factors:\n" + "\n".join(f"- {f}" for f in primary.key_factors)
            answer += f"\n\nAuthority:\n" + "\n".join(f"- {a}" for a in primary.primary_authority)
            answer += f"\n\nAdversary Position: {primary.adversary_position}\n\nCounterarguments:\n" + "\n".join(f"- {c}" for c in primary.counter_arguments)
            answer += f"\n\nResolution Strategy: {primary.resolution_strategy}"
            chain = ["Cache hit", "Memo format", "Full analysis", "Strategic recommendations"]

        return answer, primary.confidence, primary.primary_authority, chain

    def _determinism_hash(self, question: str, answer: str) -> str:
        payload = f"{question}|{answer}|{VERSION}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def _log_audit_trail(self, req: QueryRequest, answer: str, triggered: List[str], latency: float):
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "question": req.question,
            "mode": req.mode,
            "zone": req.zone,
            "triggered_doctrines": triggered,
            "answer_length": len(answer),
            "latency_ms": round(latency, 2)
        }
        with open(f"logs/ent03_audit_{datetime.now():%Y%m%d}.jsonl", "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

    def health(self) -> HealthResponse:
        uptime = time.time() - self.start_time
        return HealthResponse(
            status="healthy", engine_id=ENGINE_ID, version=VERSION,
            doctrines_loaded=len(self.doctrine_cache),
            uptime_seconds=round(uptime, 2), queries_processed=self.query_count
        )

app = FastAPI(title=ENGINE_NAME, version=VERSION)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
engine = MergersAcquisitionsEngine()

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    try:
        return engine.query(req)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    return engine.health()

@app.get("/")
async def root():
    return {"engine": ENGINE_NAME, "version": VERSION, "port": PORT, "doctrines": len(DOCTRINE_CACHE), "endpoints": ["/query", "/health"]}

if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
