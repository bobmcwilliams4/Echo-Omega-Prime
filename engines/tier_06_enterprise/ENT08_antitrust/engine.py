"""
ENT08 Antitrust Analysis Engine - TIE Gold Standard
Handles Sherman Act, Clayton Act, FTC Act, merger analysis, market power, competitive conduct
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

ENGINE_ID = "ENT08"
ENGINE_NAME = "Antitrust Analysis Engine"
VERSION = "1.0.0"
PORT = 9148

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
    HORIZONTAL_AGREEMENT = "HORIZONTAL_AGREEMENT"
    VERTICAL_RESTRAINT = "VERTICAL_RESTRAINT"
    MONOPOLIZATION = "MONOPOLIZATION"
    MERGER_REVIEW = "MERGER_REVIEW"
    PRICE_DISCRIMINATION = "PRICE_DISCRIMINATION"
    TYING_EXCLUSIVE = "TYING_EXCLUSIVE"
    IMMUNITY_EXEMPTION = "IMMUNITY_EXEMPTION"
    MARKET_DEFINITION = "MARKET_DEFINITION"

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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    categories: List[IssueCategory] = field(default_factory=list)

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Sherman Act Section 1 - Horizontal Price Fixing",
        keywords=["price fixing", "horizontal agreement", "competitors", "cartel", "per se", "pricing coordination"],
        conclusion_template=[
            "Horizontal price fixing agreements are per se illegal under Sherman Act Section 1.",
            "Any agreement among competitors to fix prices violates the law regardless of reasonableness.",
            "Circumstantial evidence (parallel conduct plus factor) may establish conspiracy."
        ],
        reasoning_framework="""
        15 USC Section 1: Every contract, combination, or conspiracy in restraint of trade is illegal.
        Per se rule applies to horizontal price fixing - no inquiry into competitive effects needed.
        Elements: (1) agreement among competitors, (2) fixing price terms.
        Direct evidence (meeting minutes, emails) establishes agreement.
        Circumstantial evidence requires conscious parallelism PLUS additional factors showing concert of action.
        Plus factors: motive to conspire, identical pricing despite different costs, price changes against economic interest,
        advance price announcements, information exchange beyond normal competitive intelligence.
        Criminal prosecution under 15 USC Section 1 carries up to 10 years imprisonment.
        Competitor communications about price are inherently suspect - business justification rarely saves them.
        Hub-and-spoke conspiracies: vertical relationships used to facilitate horizontal conspiracy among competitors.
        """,
        key_factors=[
            "Existence of competitor communications about pricing",
            "Identical price increases despite cost variations",
            "Trade association meetings with pricing discussions",
            "Information exchanges reducing pricing uncertainty",
            "Parallel conduct plus factors showing agreement",
            "Absence of legitimate procompetitive justification"
        ],
        primary_authority=[
            "15 USC Section 1",
            "United States v. Socony-Vacuum Oil Co., 310 U.S. 150 (1940)",
            "Catalano, Inc. v. Target Sales, Inc., 446 U.S. 643 (1980)",
            "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)",
            "2023 DOJ/FTC Horizontal Merger Guidelines Section 7.2"
        ],
        burden_holder="Government or plaintiff",
        adversary_position="Legitimate independent pricing, conscious parallelism lawful without agreement",
        counter_arguments=[
            "Parallel pricing explained by cost changes or market conditions",
            "No communications or meetings showing agreement",
            "Price differences exist among alleged conspirators",
            "Prices declined during alleged conspiracy period",
            "Industry-wide price announcements for customer planning"
        ],
        resolution_strategy="Examine communications, timing of price changes, economic rationality of parallel conduct, presence of plus factors",
        entity_scope="Competitors in same relevant market",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Per se illegality well-established, circumstantial cases fact-intensive",
        controlling_precedent="Socony-Vacuum (per se rule), Twombly (plausibility pleading standard)",
        categories=[IssueCategory.HORIZONTAL_AGREEMENT]
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Bid Rigging",
        keywords=["bid rigging", "collusive bidding", "complementary bids", "cover bids", "bid suppression", "procurement"],
        conclusion_template=[
            "Bid rigging is per se illegal under Sherman Act Section 1.",
            "Agreements to submit complementary bids, suppress bids, or rotate winning bids violate antitrust law.",
            "Government procurement cases often involve criminal prosecution."
        ],
        reasoning_framework="""
        Bid rigging includes: (1) bid suppression (agreement not to bid), (2) complementary bidding (submission of intentionally
        high bids to create appearance of competition), (3) bid rotation (taking turns being low bidder), (4) subcontracting
        agreements (losing bidders compensated via subcontracts from winner).
        Per se illegal - no competitive justification defense available.
        Frequently prosecuted criminally - Sherman Act Section 1 felony.
        DOJ Procurement Collusion Strike Force targets government procurement fraud.
        Evidence: pre-bid communications, pattern of rotating winners, complementary bids at identical or implausible levels,
        subcontracts awarded to bid losers, bid withdrawal shortly before deadline.
        Identical bid amounts, especially to multiple decimal places, create strong inference of collusion.
        """,
        key_factors=[
            "Pattern of rotating low bidders",
            "Communications among bidders before submission",
            "Complementary bids at identical or suspicious levels",
            "Bid withdrawals benefiting specific competitor",
            "Subcontracts to losing bidders",
            "Bids higher than prior winning bids without cost justification"
        ],
        primary_authority=[
            "15 USC Section 1",
            "United States v. Reicher, 983 F.3d 168 (4th Cir. 2020)",
            "DOJ Price Fixing, Bid Rigging, and Market Allocation Primer (2023)",
            "15 USC Section 645(d) (criminal penalties for SBA fraud)"
        ],
        burden_holder="Government or contracting authority",
        adversary_position="Independent bidding decisions, legitimate subcontracting relationships",
        counter_arguments=[
            "Parallel pricing due to identical cost structures",
            "Subcontracting based on specialty capabilities",
            "Communications limited to joint venture formation",
            "High bids reflect risk assessment or capacity constraints"
        ],
        resolution_strategy="Analyze bid patterns, communications, economic rationality, subcontract relationships",
        entity_scope="Bidders on same procurement or contract",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Per se illegality clear, but proving agreement requires evidence beyond parallel conduct",
        controlling_precedent="Reicher (bid rigging conspiracy elements)",
        categories=[IssueCategory.HORIZONTAL_AGREEMENT]
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Market Allocation",
        keywords=["market allocation", "customer allocation", "territorial division", "horizontal restraint"],
        conclusion_template=[
            "Horizontal market allocation agreements are per se illegal.",
            "Agreements among competitors to divide markets, customers, or territories violate Section 1.",
            "No inquiry into reasonableness required for naked market division."
        ],
        reasoning_framework="""
        Market allocation: competitors agree to divide markets by geography, customer type, or product line.
        Per se illegal when horizontal (among competitors) and naked (no integration or efficiency justification).
        Palmer v. BRG, 498 U.S. 46 (1990): agreement between competitors to respect territorial boundaries is per se illegal.
        Ancillary restraints (reasonably necessary to legitimate collaboration) analyzed under rule of reason.
        Customer allocation: agreement not to solicit each other's customers.
        Product allocation: agreement to stay out of each other's product lines.
        Evidence: non-solicitation agreements, territorial restrictions in distributor agreements when horizontal,
        customer lists shared to avoid competition, product line withdrawal agreements.
        Criminal prosecution available under 15 USC Section 1.
        """,
        key_factors=[
            "Agreement among competitors, not vertical relationships",
            "Division of markets, customers, or territories",
            "Lack of integration or procompetitive collaboration",
            "Naked restraint not ancillary to legitimate joint venture",
            "Evidence of agreement (written or circumstantial)",
            "Competitive harm from reduced rivalry"
        ],
        primary_authority=[
            "15 USC Section 1",
            "Palmer v. BRG of Georgia, Inc., 498 U.S. 46 (1990)",
            "United States v. Topco Associates, Inc., 405 U.S. 596 (1972)",
            "Rothery Storage & Van Co. v. Atlas Van Lines, 792 F.2d 210 (D.C. Cir. 1986)"
        ],
        burden_holder="Government or plaintiff",
        adversary_position="Vertical non-compete, ancillary restraint to legitimate joint venture, unilateral conduct",
        counter_arguments=[
            "Restraint is vertical (manufacturer-distributor) not horizontal",
            "Restraint ancillary to efficiency-creating integration",
            "Legitimate joint venture with necessary territorial divisions",
            "Unilateral policy, not agreement with competitors"
        ],
        resolution_strategy="Distinguish horizontal from vertical, assess whether restraint is ancillary to procompetitive integration",
        entity_scope="Competitors in same relevant market",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Per se rule applies to naked horizontal market division, rule of reason for ancillary restraints",
        controlling_precedent="Palmer (per se illegality), Rothery (ancillary restraints test)",
        categories=[IssueCategory.HORIZONTAL_AGREEMENT]
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Rule of Reason Framework",
        keywords=["rule of reason", "competitive effects", "procompetitive justifications", "balancing test"],
        conclusion_template=[
            "Most vertical restraints and non-price horizontal restraints are analyzed under rule of reason.",
            "Plaintiff must prove anticompetitive effects in relevant market.",
            "Defendant may offer procompetitive justifications that are balanced against harms."
        ],
        reasoning_framework="""
        Rule of reason analysis: restraint illegal only if anticompetitive effects outweigh procompetitive benefits.
        Three-step burden-shifting: (1) plaintiff proves anticompetitive effects in relevant market, (2) defendant offers
        procompetitive justifications, (3) plaintiff shows less restrictive alternatives or net harm.
        Market power often required (but not always - NCAA quick look for restraints with obvious anticompetitive effects).
        Relevant market definition critical - geographic and product dimensions.
        Anticompetitive effects: higher prices, reduced output, diminished innovation, foreclosure of rivals.
        Procompetitive justifications: cost savings, quality improvements, new product introduction, risk sharing.
        Quick look: restraints with obvious anticompetitive effects but potential justifications (shortened rule of reason).
        Examples of rule of reason conduct: non-price vertical restraints (Leegin), some joint ventures, standard-setting,
        exclusive dealing (if below foreclosure thresholds), loyalty discounts.
        """,
        key_factors=[
            "Defendant's market power or share",
            "Actual or likely price effects",
            "Output reduction or quality degradation",
            "Foreclosure of competitors",
            "Procompetitive efficiencies claimed",
            "Less restrictive alternatives available",
            "Duration and scope of restraint"
        ],
        primary_authority=[
            "15 USC Section 1",
            "Standard Oil Co. v. United States, 221 U.S. 1 (1911)",
            "NCAA v. Board of Regents, 468 U.S. 85 (1984)",
            "California Dental Assn v. FTC, 526 U.S. 756 (1999)",
            "Ohio v. American Express Co., 585 U.S. 529 (2018)"
        ],
        burden_holder="Plaintiff to prove anticompetitive effects, then shifts to defendant for justifications",
        adversary_position="No market power, no anticompetitive effects, strong procompetitive justifications",
        counter_arguments=[
            "Defendant lacks market power to harm competition",
            "No price increase or output reduction proven",
            "Efficiencies outweigh any theoretical harms",
            "Restraint necessary to achieve procompetitive benefits",
            "Interbrand competition constrains any intrabrand restraint"
        ],
        resolution_strategy="Define relevant market, assess market power, quantify effects, weigh efficiencies, consider alternatives",
        entity_scope="Varies by conduct - vertical restraints, joint ventures, non-core horizontal restraints",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fact-intensive, outcome depends on market definition and economic evidence",
        controlling_precedent="NCAA (rule of reason framework), AmEx (two-sided markets)",
        categories=[IssueCategory.HORIZONTAL_AGREEMENT, IssueCategory.VERTICAL_RESTRAINT]
    ),
    DoctrineBlock(
        topic="Sherman Act Section 2 - Monopolization Elements",
        keywords=["monopolization", "monopoly power", "willful acquisition", "exclusionary conduct", "market power"],
        conclusion_template=[
            "Monopolization requires (1) monopoly power in relevant market and (2) willful acquisition or maintenance via exclusionary conduct.",
            "Monopoly power alone is not illegal - conduct must be exclusionary, not growth or development as consequence of superior product.",
            "Relevant market definition and market share analysis are critical threshold issues."
        ],
        reasoning_framework="""
        Sherman Act Section 2, 15 USC Section 2: monopolization, attempted monopolization, conspiracy to monopolize.
        Elements: (1) possession of monopoly power (ability to control prices or exclude competition), (2) willful acquisition
        or maintenance of that power through exclusionary conduct (not superior skill, foresight, or industry).
        Monopoly power: typically requires >50% market share, barriers to entry, ability to raise prices sustainably.
        Relevant market: product and geographic dimensions using SSNIP test (small but significant non-transitory increase in price).
        Exclusionary conduct: conduct that harms competition, not just competitors - refusal to deal (Aspen Skiing), exclusive
        dealing (if forecloses substantial share), predatory pricing (below-cost pricing with dangerous probability of recoupment),
        tying (if monopoly power in tying product), bundling, raising rivals' costs, denial of essential facility (limited doctrine).
        United States v. Grinnell Corp., 384 U.S. 563 (1966): monopoly power + exclusionary conduct.
        Verizon v. Trinko, 540 U.S. 398 (2004): no duty to aid competitors, narrow scope for refusal to deal.
        """,
        key_factors=[
            "Market share in properly defined relevant market",
            "Barriers to entry and expansion",
            "Duration and stability of high market share",
            "Conduct's effect on competition vs. competitors",
            "Efficiency justifications for challenged conduct",
            "Less restrictive alternatives available",
            "Intent evidence (but not sufficient alone)"
        ],
        primary_authority=[
            "15 USC Section 2",
            "United States v. Grinnell Corp., 384 U.S. 563 (1966)",
            "Verizon Communications v. Law Offices of Curtis V. Trinko, 540 U.S. 398 (2004)",
            "Aspen Skiing Co. v. Aspen Highlands Skiing Corp., 472 U.S. 585 (1985)",
            "Brooke Group Ltd. v. Brown & Williamson Tobacco Corp., 509 U.S. 209 (1993)"
        ],
        burden_holder="Government or plaintiff",
        adversary_position="Lack of monopoly power, conduct is procompetitive or competitively neutral, legitimate business justification",
        counter_arguments=[
            "Market share below monopoly threshold (under 50%)",
            "Relevant market too narrow - broader substitutes exist",
            "Conduct improves efficiency or consumer welfare",
            "Refusal to deal with no prior course of dealing (Trinko)",
            "Pricing above cost (no predatory pricing)",
            "Superior product, skill, or foresight explains dominance"
        ],
        resolution_strategy="Define relevant market rigorously, assess market power objectively, distinguish exclusionary from competitive conduct",
        entity_scope="Single firm with monopoly or near-monopoly power",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High legal bar for monopolization, market definition disputes common, conduct characterization fact-intensive",
        controlling_precedent="Grinnell (elements), Trinko (no duty to deal), Brooke Group (predatory pricing standard)",
        categories=[IssueCategory.MONOPOLIZATION]
    ),
    DoctrineBlock(
        topic="Sherman Act Section 2 - Attempted Monopolization",
        keywords=["attempted monopolization", "specific intent", "dangerous probability", "predatory conduct"],
        conclusion_template=[
            "Attempted monopolization requires (1) specific intent to monopolize, (2) predatory or exclusionary conduct, (3) dangerous probability of success.",
            "Dangerous probability requires market share typically above 30-50% depending on circuit.",
            "Specific intent may be inferred from exclusionary conduct itself."
        ],
        reasoning_framework="""
        Elements: (1) specific intent to monopolize, (2) anticompetitive or exclusionary conduct directed toward accomplishing
        unlawful purpose, (3) dangerous probability of achieving monopoly power in relevant market.
        Spectrum Sports, Inc. v. McQuillan, 506 U.S. 447 (1993): all three elements required, dangerous probability not presumed.
        Specific intent: purpose to control prices or destroy competition - may infer from conduct's nature and effect.
        Dangerous probability: defendant must be close to achieving monopoly power - market share analysis critical.
        Market share thresholds vary: some circuits require 50%+, others as low as 30% with other factors.
        Predatory pricing: below-cost pricing with dangerous probability of recoupment (Brooke Group standard applies).
        Exclusionary conduct: same types as monopolization (refusal to deal, exclusive contracts, predatory pricing, tying).
        Higher bar than monopolization because defendant lacks current monopoly power.
        """,
        key_factors=[
            "Market share in relevant market (typically 30-50% minimum)",
            "Barriers to entry that would permit monopoly maintenance",
            "Conduct's exclusionary nature and effect",
            "Intent evidence (internal documents, testimony)",
            "Market trends showing path toward monopoly",
            "Foreclosure of competitors or distribution channels"
        ],
        primary_authority=[
            "15 USC Section 2",
            "Spectrum Sports, Inc. v. McQuillan, 506 U.S. 447 (1993)",
            "Brooke Group Ltd. v. Brown & Williamson Tobacco Corp., 509 U.S. 209 (1993)",
            "Rebel Oil Co. v. Atlantic Richfield Co., 51 F.3d 1421 (9th Cir. 1995)"
        ],
        burden_holder="Government or plaintiff",
        adversary_position="Insufficient market share, lack of specific intent, legitimate business justification, no dangerous probability",
        counter_arguments=[
            "Market share insufficient for dangerous probability",
            "Low barriers to entry prevent monopoly maintenance",
            "Conduct has procompetitive justification",
            "No intent to monopolize - competitive response",
            "Market conditions changed, monopoly no longer probable"
        ],
        resolution_strategy="Assess market share rigorously, evaluate entry barriers, distinguish aggressive competition from exclusionary conduct",
        entity_scope="Firm with significant but not yet monopoly market share",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Harder to prove than monopolization, dangerous probability threshold uncertain, intent often disputed",
        controlling_precedent="Spectrum Sports (three-element test)",
        categories=[IssueCategory.MONOPOLIZATION]
    ),
    DoctrineBlock(
        topic="Clayton Act Section 7 - Merger Analysis Framework",
        keywords=["merger", "acquisition", "Clayton Act", "competitive effects", "market concentration", "HHI"],
        conclusion_template=[
            "Clayton Act Section 7 prohibits mergers that may substantially lessen competition in any line of commerce.",
            "Merger analysis examines market concentration, competitive effects, entry conditions, and efficiencies.",
            "2023 Merger Guidelines reflect more aggressive enforcement posture than prior versions."
        ],
        reasoning_framework="""
        15 USC Section 18 (Clayton Act Section 7): prohibits stock or asset acquisitions where effect may be substantially to lessen
        competition or tend to create monopoly.
        2023 DOJ/FTC Merger Guidelines (replaced 2010 Horizontal Merger Guidelines):
        - Guideline 1: Mergers should not significantly increase concentration in highly concentrated markets
        - HHI thresholds: HHI >1800 is highly concentrated, increase >100 points presumptively anticompetitive
        - Guideline 2: Mergers should not eliminate substantial competition between firms
        - Guideline 3: Mergers should not increase risk of coordination
        - Guideline 4: Mergers should not eliminate potential entrant
        - Guideline 5: Mergers creating firm controlling products/services that rivals need (foreclosure)
        Market definition: SSNIP test (5-10% price increase), hypothetical monopolist framework.
        Competitive effects: unilateral (loss of direct competition) or coordinated (increased likelihood of collusion).
        Entry analysis: timeliness (within 2 years), likelihood, sufficiency to deter or counteract competitive harm.
        Efficiencies: merger-specific, verifiable, cognizable (benefit consumers, not just merging parties).
        Failing firm defense: rare, requires imminent failure, no less anticompetitive buyer, assets would exit market.
        """,
        key_factors=[
            "Post-merger HHI and delta HHI",
            "Market shares of merging parties",
            "Closeness of competition between merging firms",
            "Likelihood of coordinated effects",
            "Entry barriers and timing",
            "Merger-specific efficiencies",
            "Trend toward concentration in market",
            "Elimination of potential entrant"
        ],
        primary_authority=[
            "15 USC Section 18 (Clayton Act Section 7)",
            "2023 DOJ/FTC Merger Guidelines",
            "United States v. Philadelphia National Bank, 374 U.S. 321 (1963)",
            "FTC v. H.J. Heinz Co., 246 F.3d 708 (D.C. Cir. 2001)",
            "United States v. Baker Hughes Inc., 908 F.2d 981 (D.C. Cir. 1990)"
        ],
        burden_holder="Government initially, then shifts based on evidence",
        adversary_position="Low concentration, robust entry, strong efficiencies, no competitive overlap",
        counter_arguments=[
            "Post-merger HHI below enforcement thresholds",
            "Merging firms not close competitors",
            "Timely and likely entry constrains market power",
            "Substantial merger-specific efficiencies",
            "Broader market definition reduces concentration",
            "Failing firm or flailing division (exiting assets)"
        ],
        resolution_strategy="Rigorous market definition, HHI calculation, competitive effects modeling, entry analysis, efficiencies verification",
        entity_scope="Merging firms and relevant markets affected",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="2023 Guidelines more skeptical of mergers, lower HHI safe harbors, heightened scrutiny of vertical and tech mergers",
        controlling_precedent="Philadelphia National Bank (structural presumption), Baker Hughes (rebuttal framework)",
        categories=[IssueCategory.MERGER_REVIEW]
    ),
    DoctrineBlock(
        topic="Vertical Merger Analysis - Foreclosure Concerns",
        keywords=["vertical merger", "input foreclosure", "customer foreclosure", "raising rivals costs"],
        conclusion_template=[
            "Vertical mergers integrate firms at different supply chain levels - supplier and customer.",
            "Primary concern is foreclosure - denying rivals access to inputs or customers.",
            "2023 Guidelines apply structural presumptions to vertical mergers exceeding market share thresholds."
        ],
        reasoning_framework="""
        Vertical merger: integration of supplier and customer (e.g., content producer acquiring distributor).
        Theories of harm: (1) input foreclosure (denying rivals access to key inputs), (2) customer foreclosure (denying
        rivals access to distribution), (3) increased ability to coordinate (information sharing).
        2023 Merger Guidelines Guideline 5: mergers creating firm controlling products/services rivals need.
        Structural presumption if related-product market shares >50% and foreclosure share >50%.
        Brown Shoe factors: vertical integration may lessen competition by foreclosing access.
        Efficiencies: elimination of double marginalization (EDM), improved coordination, innovation incentives.
        Remedy: behavioral (non-discrimination commitments) vs. structural (divestiture).
        Recent enforcement: AT&T/Time Warner (government loss), vertical merger challenges increasing post-2020.
        """,
        key_factors=[
            "Market share in upstream and downstream markets",
            "Availability of alternative suppliers or customers",
            "Cost or quality disadvantage if foreclosed",
            "Incentive to foreclose vs. dealing with rivals",
            "Vertical integration by competitors",
            "Elimination of double marginalization benefits"
        ],
        primary_authority=[
            "15 USC Section 18",
            "2023 DOJ/FTC Merger Guidelines Guideline 5",
            "Brown Shoe Co. v. United States, 370 U.S. 294 (1962)",
            "United States v. AT&T Inc., 310 F. Supp. 3d 161 (D.D.C. 2018)"
        ],
        burden_holder="Government",
        adversary_position="Numerous alternative suppliers/customers, no incentive to foreclose, strong efficiencies",
        counter_arguments=[
            "Foreclosure unprofitable - need rival distribution or supply",
            "Abundant alternatives for foreclosed rivals",
            "Efficiencies (EDM) outweigh foreclosure risk",
            "Vertical integration common in industry",
            "No historical foreclosure by vertically integrated rivals"
        ],
        resolution_strategy="Model foreclosure incentives, assess alternatives, quantify EDM and other efficiencies",
        entity_scope="Vertically related markets",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="2023 Guidelines increase scrutiny, but foreclosure cases remain challenging absent clear harm",
        controlling_precedent="AT&T/Time Warner (government must prove harm, not just theory)",
        categories=[IssueCategory.MERGER_REVIEW, IssueCategory.VERTICAL_RESTRAINT]
    ),
    DoctrineBlock(
        topic="Tying Arrangements - Jefferson Parish Test",
        keywords=["tying", "tied product", "tying product", "separate products", "coercion", "foreclosure"],
        conclusion_template=[
            "Tying is conditioning sale of one product (tying) on purchase of another (tied).",
            "Requires (1) separate products, (2) market power in tying product, (3) anticompetitive foreclosure in tied market.",
            "Per se illegal if elements met, though modern cases apply modified rule of reason."
        ],
        reasoning_framework="""
        Tying: seller with market power in tying product conditions its sale on buyer purchasing tied product.
        Jefferson Parish Hospital v. Hyde, 466 U.S. 2 (1984): elements are (1) two separate products, (2) market power in
        tying product, (3) coercion (conditioning sale), (4) substantial anticompetitive foreclosure in tied market.
        Separate products: determined by consumer demand - would consumers want one without the other?
        Market power: ability to force purchases of unwanted product - appreciable economic power in tying market.
        Per se vs. rule of reason: traditionally per se, but modern cases (Illinois Tool Works) require proof of market power
        and anticompetitive effects, collapsing into modified rule of reason.
        Foreclosure: substantial share of tied product market foreclosed to rivals.
        Procompetitive justifications: quality control, efficiencies, new product introduction (single product defense).
        Clayton Act Section 3 (15 USC 14) applies to goods; Sherman Act Section 1 applies to services and broader conduct.
        """,
        key_factors=[
            "Consumer demand treats products as separate",
            "Market power in tying product",
            "Coercion or conditioning of sale",
            "Substantial foreclosure in tied market",
            "Lack of business justification",
            "Anticompetitive effects outweigh efficiencies"
        ],
        primary_authority=[
            "15 USC Section 1, 15 USC Section 14",
            "Jefferson Parish Hospital Dist. No. 2 v. Hyde, 466 U.S. 2 (1984)",
            "Illinois Tool Works Inc. v. Independent Ink, Inc., 547 U.S. 28 (2006)",
            "Eastman Kodak Co. v. Image Technical Services, Inc., 504 U.S. 451 (1992)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Single product, no market power, no coercion, procompetitive justifications",
        counter_arguments=[
            "Products are components of single integrated offering",
            "No market power in tying product",
            "No coercion - buyers choose package voluntarily",
            "Minimal foreclosure in tied market",
            "Efficiencies require bundling (quality control, cost savings)"
        ],
        resolution_strategy="Assess consumer demand for separate purchase, measure market power, quantify foreclosure, weigh efficiencies",
        entity_scope="Seller with market power in one product market",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Modern cases skeptical of per se treatment, require substantial anticompetitive effects",
        controlling_precedent="Illinois Tool Works (market power not presumed from patent/copyright)",
        categories=[IssueCategory.TYING_EXCLUSIVE, IssueCategory.MONOPOLIZATION]
    ),
    DoctrineBlock(
        topic="Exclusive Dealing - Anticompetitive Foreclosure Standard",
        keywords=["exclusive dealing", "requirements contract", "foreclosure", "market share", "duration"],
        conclusion_template=[
            "Exclusive dealing requires buyer to purchase all or substantial share of needs from single seller.",
            "Illegal under Section 1 (Sherman) or Section 3 (Clayton) if forecloses substantial share of market to rivals.",
            "Rule of reason analysis - foreclosure percentage, duration, and market context determine legality."
        ],
        reasoning_framework="""
        Exclusive dealing: contract requiring buyer to purchase exclusively or predominantly from one seller.
        Clayton Act Section 3 (15 USC 14): applies to goods, prohibits exclusive dealing where effect may substantially lessen competition.
        Sherman Act Section 1: applies to services and broader range of exclusivity arrangements.
        Tampa Electric Co. v. Nashville Coal Co., 365 U.S. 320 (1961): examine (1) share of market foreclosed, (2) probable
        effect on competition, (3) procompetitive justifications.
        Foreclosure safe harbor: <40% market foreclosure typically lawful; >40% raises concerns; >50% presumptively problematic.
        Duration matters: long-term contracts (5+ years) more likely anticompetitive if substantial foreclosure.
        Procompetitive justifications: assurance of supply, incentivizes investment, prevents free-riding, quality assurance.
        Distinction from tying: exclusive dealing is single product, no coerced purchase of separate product.
        """,
        key_factors=[
            "Percentage of market foreclosed to rivals",
            "Duration of exclusive arrangement",
            "Ability of foreclosed rivals to compete elsewhere",
            "Entry barriers in foreclosed market",
            "Procompetitive justifications for exclusivity",
            "Market power of party imposing exclusivity"
        ],
        primary_authority=[
            "15 USC Section 1, 15 USC Section 14",
            "Tampa Electric Co. v. Nashville Coal Co., 365 U.S. 320 (1961)",
            "United States v. Microsoft Corp., 253 F.3d 34 (D.C. Cir. 2001)",
            "McWane, Inc. v. FTC, 783 F.3d 814 (11th Cir. 2015)"
        ],
        burden_holder="Plaintiff or government",
        adversary_position="Low foreclosure, procompetitive benefits, no market power, short duration",
        counter_arguments=[
            "Foreclosure below 40% safe harbor threshold",
            "Short-term contracts permit easy switching",
            "Alternative distribution channels available to rivals",
            "Justifications (supply assurance, investment incentives) outweigh foreclosure",
            "No market power to impose anticompetitive exclusivity"
        ],
        resolution_strategy="Calculate foreclosure share accurately, assess entry barriers and alternatives, weigh justifications",
        entity_scope="Seller or buyer with ability to foreclose substantial market share",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fact-intensive, foreclosure percentage critical, strong justifications may save arrangements",
        controlling_precedent="Tampa Electric (foreclosure standard), Microsoft (anticompetitive exclusivity)",
        categories=[IssueCategory.TYING_EXCLUSIVE, IssueCategory.VERTICAL_RESTRAINT]
    ),
    DoctrineBlock(
        topic="Robinson-Patman Act - Price Discrimination",
        keywords=["price discrimination", "Robinson-Patman", "competitive injury", "cost justification", "meeting competition"],
        conclusion_template=[
            "Robinson-Patman Act prohibits price discrimination in sale of commodities of like grade and quality where effect may injure competition.",
            "Requires (1) commodity sales, (2) different prices to different purchasers, (3) competitive injury, (4) interstate commerce.",
            "Defenses: cost justification or meeting competition in good faith."
        ],
        reasoning_framework="""
        15 USC Section 13 (Robinson-Patman Act, Clayton Act Section 2): prohibits sellers from discriminating in price between
        different purchasers of commodities of like grade and quality where effect may substantially lessen competition or
        injure, destroy, or prevent competition.
        Elements: (1) sales of commodities (not services), (2) like grade and quality, (3) different prices to different purchasers,
        (4) competitive injury (primary line [seller level] or secondary line [buyer level]), (5) interstate commerce.
        Primary line injury (predatory pricing): seller sells below cost to injure competing sellers (Brooke Group standard applies).
        Secondary line injury: favored buyers gain competitive advantage over disfavored buyers (Volvo Trucks standard).
        Cost justification defense: price difference reflects cost savings in manufacturing, delivery, or sale to favored buyer.
        Meeting competition defense: price reduction made in good faith to meet equally low price of competitor.
        Functional discount: different prices to buyers at different distribution levels may be justified.
        Robinson-Patman enforcement rare post-1990s - FTC has brought few cases, DOJ never enforces.
        """,
        key_factors=[
            "Sales of commodities (tangible goods), not services",
            "Price differences to competing purchasers",
            "Competitive injury at seller or buyer level",
            "Lack of cost justification for price difference",
            "Failure to meet competition defense",
            "Interstate commerce jurisdictional element"
        ],
        primary_authority=[
            "15 USC Section 13 (Robinson-Patman Act)",
            "Brooke Group Ltd. v. Brown & Williamson Tobacco Corp., 509 U.S. 209 (1993)",
            "Volvo Trucks North America, Inc. v. Reeder-Simco GMC, Inc., 546 U.S. 164 (2006)",
            "FTC v. Morton Salt Co., 334 U.S. 37 (1948)"
        ],
        burden_holder="Plaintiff to prove discrimination and injury, defendant to prove cost justification or meeting competition",
        adversary_position="No competitive injury, cost justification, meeting competition defense, functional discount, services not commodities",
        counter_arguments=[
            "Sales are of services, not commodities (outside Robinson-Patman)",
            "Buyers are not competing purchasers (different markets)",
            "Price differences justified by cost savings",
            "Good faith meeting of competitor's lower price",
            "Functional discount to different distribution level",
            "No competitive injury proven at either level"
        ],
        resolution_strategy="Determine if commodities, assess competitive injury, verify cost justification, evaluate meeting competition defense",
        entity_scope="Sellers of commodities to competing purchasers",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Rarely enforced by FTC/DOJ, private plaintiffs face high bar, many defenses available",
        controlling_precedent="Brooke Group (primary line), Volvo Trucks (secondary line)",
        categories=[IssueCategory.PRICE_DISCRIMINATION]
    ),
    DoctrineBlock(
        topic="Resale Price Maintenance - Leegin Analysis",
        keywords=["RPM", "resale price maintenance", "minimum pricing", "vertical price fixing", "Leegin"],
        conclusion_template=[
            "Vertical minimum resale price maintenance (RPM) is analyzed under rule of reason, not per se illegal.",
            "Leegin overruled 96-year Dr. Miles per se rule in 2007.",
            "Many states retain per se illegality under state antitrust laws."
        ],
        reasoning_framework="""
        Resale price maintenance (RPM): manufacturer sets minimum (or maximum) resale prices for retailers.
        Leegin Creative Leather Products v. PSKS, Inc., 551 U.S. 877 (2007): minimum RPM is rule of reason, not per se illegal.
        Overruled Dr. Miles Medical Co. v. John D. Park & Sons Co., 220 U.S. 373 (1911).
        Procompetitive justifications for RPM: prevents free-riding on retailer services (showrooms, demos), encourages
        retailer investment in brand promotion, enables market entry by new brands, ensures product quality reputation.
        Anticompetitive risks: facilitates horizontal price fixing among retailers or manufacturers, reduces intrabrand competition.
        Rule of reason factors: market power of manufacturer, horizontal agreement likelihood, interbrand competition intensity.
        Unilateral RPM (manufacturer's independent policy) analyzed under Colgate doctrine - legal if truly unilateral, no agreement.
        Agreement requirement: RPM violates Section 1 only if vertical agreement exists between manufacturer and retailer.
        State law caution: California, Maryland, New York and others retain per se illegality under state antitrust statutes.
        """,
        key_factors=[
            "Manufacturer's market power",
            "Intensity of interbrand competition",
            "Evidence of horizontal agreement among dealers or manufacturers",
            "Free-riding risk justifying RPM",
            "Dealer services incentivized by RPM",
            "Price increase or output reduction effects"
        ],
        primary_authority=[
            "15 USC Section 1",
            "Leegin Creative Leather Products, Inc. v. PSKS, Inc., 551 U.S. 877 (2007)",
            "United States v. Colgate & Co., 250 U.S. 300 (1919)",
            "Dr. Miles Medical Co. v. John D. Park & Sons Co., 220 U.S. 373 (1911) (overruled)",
            "State antitrust laws (CA, MD, NY retain per se illegality)"
        ],
        burden_holder="Plaintiff to prove agreement and anticompetitive effects under rule of reason",
        adversary_position="No agreement (unilateral policy), procompetitive justifications, strong interbrand competition",
        counter_arguments=[
            "Unilateral policy, no vertical agreement (Colgate)",
            "Interbrand competition constrains pricing power",
            "RPM prevents free-riding on dealer services",
            "New brand needs RPM to incentivize retailer support",
            "No price increase or output reduction shown"
        ],
        resolution_strategy="Verify vertical agreement exists, assess market power and interbrand competition, evaluate free-riding and service justifications",
        entity_scope="Manufacturer and retailers in vertical relationship",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Leegin makes federal cases harder for plaintiffs, but state law may apply per se rule",
        controlling_precedent="Leegin (rule of reason), Colgate (unilateral conduct exception)",
        categories=[IssueCategory.VERTICAL_RESTRAINT]
    ),
    DoctrineBlock(
        topic="State Action Immunity - Parker Doctrine",
        keywords=["state action immunity", "Parker", "Midcal test", "active supervision", "clearly articulated"],
        conclusion_template=[
            "State action immunity exempts conduct from antitrust scrutiny if authorized by state sovereignty.",
            "Requires (1) clear articulation of state policy to displace competition and (2) active state supervision.",
            "Applies to state governments and private parties acting pursuant to state regulatory schemes."
        ],
        reasoning_framework="""
        Parker v. Brown, 317 U.S. 341 (1943): federalism doctrine - Sherman Act does not apply to state sovereign acts.
        Midcal test for private parties claiming state action immunity:
        (1) Clear articulation: challenged restraint must be clearly articulated and affirmatively expressed as state policy.
        (2) Active supervision: state must actively supervise private party's anticompetitive conduct.
        Clear articulation: mere authorization insufficient - state must foreseeably contemplate anticompetitive effects.
        Active supervision: state exercises meaningful review - not rubber stamp - of specific anticompetitive acts.
        States themselves are immune without supervision requirement (Town of Hallie).
        Municipalities and state subdivisions: must meet both Midcal prongs unless exercising delegated state authority.
        North Carolina State Board of Dental Examiners v. FTC, 574 U.S. 494 (2015): active market participants on state boards
        (e.g., dentists regulating dentistry) must meet both Midcal prongs including active supervision.
        Narrow doctrine: strictly construed, does not extend to federal regulatory immunity.
        """,
        key_factors=[
            "State statute clearly contemplates displacement of competition",
            "Private party acts pursuant to state regulatory scheme",
            "State actively supervises specific conduct (not mere statutory authorization)",
            "State's substantive review of anticompetitive decisions",
            "Whether actor is state itself vs. private party or controlled board"
        ],
        primary_authority=[
            "Parker v. Brown, 317 U.S. 341 (1943)",
            "California Retail Liquor Dealers Assn v. Midcal Aluminum, Inc., 445 U.S. 97 (1980)",
            "North Carolina State Board of Dental Examiners v. FTC, 574 U.S. 494 (2015)",
            "Town of Hallie v. City of Eau Claire, 471 U.S. 34 (1985)"
        ],
        burden_holder="Party claiming immunity",
        adversary_position="No clear articulation, lack of active supervision, private conduct not state policy",
        counter_arguments=[
            "State statute does not clearly articulate anticompetitive policy",
            "No active state supervision of challenged conduct",
            "Private actors dominate regulatory board (Dental Examiners)",
            "Conduct exceeds scope of state authorization",
            "State merely authorized, did not require anticompetitive conduct"
        ],
        resolution_strategy="Examine state statute for clear articulation, assess actual state supervision mechanisms, distinguish state vs. private conduct",
        entity_scope="Private parties or subdivisions claiming state action immunity",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Narrow doctrine, strictly applied post-Dental Examiners, supervision requirement often fails",
        controlling_precedent="Midcal (two-prong test), Dental Examiners (active supervision required for controlled boards)",
        categories=[IssueCategory.IMMUNITY_EXEMPTION]
    ),
    DoctrineBlock(
        topic="Noerr-Pennington Immunity - Petitioning Government",
        keywords=["Noerr-Pennington", "petitioning immunity", "sham exception", "First Amendment", "government lobbying"],
        conclusion_template=[
            "Noerr-Pennington doctrine immunizes concerted efforts to petition government, even if anticompetitive result.",
            "Based on First Amendment right to petition - Sherman Act does not apply to genuine petitioning.",
            "Sham exception: immunity does not apply to sham petitioning objectively baseless and subjectively intended to harm competitor."
        ],
        reasoning_framework="""
        Eastern Railroad Presidents Conference v. Noerr Motor Freight, Inc., 365 U.S. 127 (1961): efforts to influence legislation
        immune even if intended to eliminate competition, based on right to petition government.
        United Mine Workers v. Pennington, 381 U.S. 657 (1965): extended to executive and administrative petitioning.
        California Motor Transport Co. v. Trucking Unlimited, 404 U.S. 508 (1972): sham exception - immunity does not apply
        to sham litigation or petitioning that is mere cover for anticompetitive conduct.
        Professional Real Estate Investors, Inc. v. Columbia Pictures Industries, Inc., 508 U.S. 49 (1993) (PRE): two-part sham test:
        (1) Objective: lawsuit or petition must be objectively baseless (no reasonable litigant could expect success), AND
        (2) Subjective: subjective motivation to interfere with competitors through government process, not genuine petitioning.
        Both prongs required - objectively reasonable petition is immune even if anticompetitive motive.
        Applies to litigation, legislative lobbying, administrative proceedings, permit applications.
        Does not protect anticompetitive agreements separate from petitioning (conspiracy to petition vs. conspiracy implemented through petition).
        """,
        key_factors=[
            "Genuineness of petitioning government",
            "Objective baselessness of petition or lawsuit",
            "Subjective anticompetitive motive (if objectively baseless)",
            "Pattern of sham petitioning or litigation abuse",
            "Petitioning vs. underlying anticompetitive agreement",
            "First Amendment petitioning rights"
        ],
        primary_authority=[
            "Eastern Railroad Presidents Conference v. Noerr Motor Freight, Inc., 365 U.S. 127 (1961)",
            "United Mine Workers v. Pennington, 381 U.S. 657 (1965)",
            "California Motor Transport Co. v. Trucking Unlimited, 404 U.S. 508 (1972)",
            "Professional Real Estate Investors, Inc. v. Columbia Pictures Industries, Inc., 508 U.S. 49 (1993)"
        ],
        burden_holder="Plaintiff challenging immunity",
        adversary_position="Genuine petitioning protected by First Amendment, objectively reasonable petition, no sham",
        counter_arguments=[
            "Petitioning is genuine exercise of First Amendment rights",
            "Petition or lawsuit objectively reasonable (not baseless)",
            "No pattern of abusive litigation",
            "Underlying agreement lawful, petitioning merely implements it",
            "Government decision is intervening cause, not conspiracy"
        ],
        resolution_strategy="Apply PRE two-part sham test strictly, distinguish petitioning from underlying agreements",
        entity_scope="Parties petitioning government (legislation, litigation, regulation)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Broad immunity, sham exception narrowly applied, plaintiff must prove objective baselessness",
        controlling_precedent="PRE (sham test)",
        categories=[IssueCategory.IMMUNITY_EXEMPTION]
    ),
    DoctrineBlock(
        topic="Market Definition - SSNIP Test and HHI",
        keywords=["market definition", "SSNIP", "HHI", "Herfindahl-Hirschman Index", "relevant market", "product market", "geographic market"],
        conclusion_template=[
            "Relevant market has product and geographic dimensions - smallest group of products and areas where hypothetical monopolist could profitably impose SSNIP.",
            "SSNIP test: small but significant non-transitory increase in price (typically 5-10% for at least one year).",
            "HHI measures concentration: sum of squared market shares, with thresholds defining enforcement zones."
        ],
        reasoning_framework="""
        Market definition critical in monopolization (Section 2), merger (Section 7), and rule of reason (Section 1) cases.
        SSNIP test (2023 Merger Guidelines): would hypothetical monopolist controlling candidate market profitably impose
        small but significant non-transitory increase in price (5-10% for 1+ year)? If customers would switch to substitutes
        defeating price increase, expand market to include substitutes.
        Product dimension: demand-side substitutability (functional interchangeability, cross-price elasticity) and supply-side
        substitutability (ease of entry or repositioning by suppliers).
        Geographic dimension: where do buyers turn for alternatives? Shipping costs, trade barriers, local preferences.
        Brown Shoe factors (product market): industry recognition, product characteristics, uses, price, production facilities.
        HHI calculation: sum of squared market shares (e.g., 4 firms with 30%, 30%, 20%, 20% shares -> HHI = 900+900+400+400 = 2600).
        2023 Merger Guidelines HHI thresholds: <1800 unconcentrated, 1800-2500 moderately concentrated, >2500 highly concentrated.
        Increase >100 points in highly concentrated market (HHI >1800) presumptively anticompetitive.
        Cellophane fallacy: measuring substitution at elevated monopoly price overstates market breadth (use competitive price baseline).
        """,
        key_factors=[
            "Demand-side substitutability (cross-elasticity)",
            "Supply-side substitutability and entry",
            "SSNIP test outcome (profitable or defeated by switching)",
            "Product characteristics and uses",
            "Geographic scope of buyer alternatives",
            "HHI level and change from transaction",
            "Competitive price baseline (avoiding Cellophane fallacy)"
        ],
        primary_authority=[
            "2023 DOJ/FTC Merger Guidelines Section 4",
            "United States v. E.I. du Pont de Nemours & Co., 351 U.S. 377 (1956) (Cellophane)",
            "Brown Shoe Co. v. United States, 370 U.S. 294 (1962)",
            "FTC v. Whole Foods Market, Inc., 548 F.3d 1028 (D.C. Cir. 2008)"
        ],
        burden_holder="Plaintiff or government initially, subject to rebuttal",
        adversary_position="Broader market includes more substitutes, lower concentration, SSNIP defeated by switching",
        counter_arguments=[
            "Broader product market includes substitutes (lower HHI)",
            "Geographic market is national or global (more competitors)",
            "SSNIP would be defeated by customer switching",
            "Supply-side substitution constrains pricing",
            "Low barriers to entry negate concentration concerns"
        ],
        resolution_strategy="Apply SSNIP rigorously, use competitive price baseline, analyze switching patterns empirically, calculate HHI accurately",
        entity_scope="All antitrust cases requiring market power or concentration analysis",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Heavily disputed in litigation, economic evidence critical, expert testimony often dueling",
        controlling_precedent="2023 Merger Guidelines (SSNIP), Cellophane (fallacy caution)",
        categories=[IssueCategory.MARKET_DEFINITION]
    ),
    DoctrineBlock(
        topic="Conscious Parallelism - Plus Factors for Agreement",
        keywords=["conscious parallelism", "plus factors", "oligopoly", "tacit collusion", "parallel conduct"],
        conclusion_template=[
            "Conscious parallelism (parallel pricing without agreement) is lawful.",
            "Sherman Act Section 1 requires agreement, not mere parallel conduct.",
            "Plus factors beyond parallelism may permit inference of agreement: motive, identical action against self-interest, communications, facilitating practices."
        ],
        reasoning_framework="""
        Parallel conduct alone does not violate Sherman Act Section 1 - agreement required.
        Theatre Enterprises v. Paramount Film Distributing Corp., 346 U.S. 537 (1954): conscious parallelism insufficient,
        agreement must be shown by direct or circumstantial evidence.
        Plus factors that support agreement inference:
        (1) Motive to conspire (oligopoly with mutual interdependence)
        (2) Actions against self-interest (pricing against individual firm's economic interest)
        (3) Identical conduct (prices, terms, timing) despite different costs or conditions
        (4) Communications among competitors
        (5) Facilitating practices (advance price announcements, most-favored-nation clauses, information exchanges)
        (6) Industry practices enabling coordination (standardized products, transparent pricing)
        Bell Atlantic v. Twombly, 550 U.S. 544 (2007): parallel conduct + context suggesting agreement needed to survive motion to dismiss.
        Matsushita Electric v. Zenith Radio, 475 U.S. 574 (1986): parallel conduct equally consistent with independent action
        does not support conspiracy inference.
        Hub-and-spoke conspiracies: vertical relationships used to coordinate horizontal conspiracy among competitors (each competitor
        is spoke, common supplier/buyer is hub).
        """,
        key_factors=[
            "Parallel pricing or conduct timing and precision",
            "Plus factors: motive, against-interest actions, communications",
            "Facilitating practices (price announcements, MFNs, information exchange)",
            "Structural oligopoly conditions (few firms, barriers to entry)",
            "Economic irrationality of conduct without coordination",
            "Direct evidence (communications, meetings)"
        ],
        primary_authority=[
            "15 USC Section 1",
            "Theatre Enterprises, Inc. v. Paramount Film Distributing Corp., 346 U.S. 537 (1954)",
            "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)",
            "Matsushita Electric Industrial Co. v. Zenith Radio Corp., 475 U.S. 574 (1986)",
            "In re Text Messaging Antitrust Litigation, 782 F.3d 862 (7th Cir. 2015)"
        ],
        burden_holder="Plaintiff to prove agreement, not just parallelism",
        adversary_position="Independent decisions, no communications, rational individual conduct, no plus factors",
        counter_arguments=[
            "Parallel conduct explained by common cost or demand changes",
            "No communications or meetings among competitors",
            "Each firm acted in individual economic interest",
            "Price differences exist, no perfect parallelism",
            "Legitimate trade association or benchmarking activity"
        ],
        resolution_strategy="Identify plus factors rigorously, assess economic rationality of independent parallelism, seek direct evidence",
        entity_scope="Oligopoly industries with parallel conduct",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="High pleading and proof burdens post-Twombly, plus factors often disputed",
        controlling_precedent="Twombly (plausibility standard), Theatre Enterprises (parallelism insufficient)",
        categories=[IssueCategory.HORIZONTAL_AGREEMENT]
    ),
    DoctrineBlock(
        topic="Predatory Pricing - Brooke Group Standard",
        keywords=["predatory pricing", "below-cost pricing", "recoupment", "marginal cost", "average variable cost"],
        conclusion_template=[
            "Predatory pricing requires (1) below-cost pricing and (2) dangerous probability of recouping losses through monopoly pricing.",
            "Brooke Group sets high bar: prices above average variable cost are presumptively lawful.",
            "Recoupment analysis examines barriers to entry and ability to sustain monopoly pricing long enough to recover losses."
        ],
        reasoning_framework="""
        Brooke Group Ltd. v. Brown & Williamson Tobacco Corp., 509 U.S. 209 (1993): two elements required:
        (1) Below-cost pricing: prices below average variable cost (or average total cost in some circuits).
        (2) Dangerous probability of recoupment: predator can recoup losses by later charging monopoly prices.
        Rationale: low pricing benefits consumers, should not be chilled; predatory pricing rarely rational strategy.
        Cost benchmark: average variable cost (AVC) is usual standard - costs that vary with output (materials, direct labor).
        Pricing above AVC presumptively lawful (profit-maximizing even in short run).
        Recoupment requires: (1) ability to raise prices to monopoly level after driving out rivals, (2) barriers to entry
        preventing re-entry or new entry, (3) duration of monopoly pricing sufficient to recover predation losses.
        Applies to primary line Robinson-Patman cases and Section 2 monopolization/attempt.
        High bar: few predatory pricing cases succeed post-Brooke Group.
        """,
        key_factors=[
            "Prices below average variable cost",
            "Sustained below-cost pricing over relevant period",
            "Market share and ability to achieve monopoly pricing",
            "Barriers to entry or re-entry",
            "Duration required to recoup predation losses",
            "Alternative explanations for low pricing (promotional, cost reduction, excess capacity)"
        ],
        primary_authority=[
            "15 USC Section 2, 15 USC Section 13",
            "Brooke Group Ltd. v. Brown & Williamson Tobacco Corp., 509 U.S. 209 (1993)",
            "Weyerhaeuser Co. v. Ross-Simmons Hardwood Lumber Co., 549 U.S. 312 (2007)",
            "Matsushita Electric Industrial Co. v. Zenith Radio Corp., 475 U.S. 574 (1986)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Prices above cost, no recoupment possible, procompetitive pricing, low barriers to entry",
        counter_arguments=[
            "Prices above average variable cost (presumptively lawful)",
            "Low barriers to entry prevent recoupment",
            "Short duration of low pricing insufficient to recoup",
            "Pricing explained by excess capacity or promotion",
            "No monopoly power or dangerous probability of monopoly"
        ],
        resolution_strategy="Measure costs accurately (AVC), model recoupment feasibility, assess entry barriers rigorously",
        entity_scope="Dominant or near-dominant firm with pricing discretion",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Very high bar post-Brooke Group, recoupment often implausible, few plaintiffs succeed",
        controlling_precedent="Brooke Group (two-element test)",
        categories=[IssueCategory.MONOPOLIZATION, IssueCategory.PRICE_DISCRIMINATION]
    ),
    DoctrineBlock(
        topic="FTC Act Section 5 - Unfair Methods of Competition",
        keywords=["FTC Act", "unfair methods", "Section 5", "standalone liability", "incipient violations"],
        conclusion_template=[
            "FTC Act Section 5 prohibits unfair methods of competition, broader than Sherman or Clayton Acts.",
            "Can reach incipient violations and conduct outside traditional antitrust rules.",
            "2022 FTC Policy Statement asserts broad standalone Section 5 authority independent of Sherman/Clayton standards."
        ],
        reasoning_framework="""
        15 USC Section 45: unfair methods of competition in or affecting commerce declared unlawful (FTC Act Section 5).
        Broader than Sherman Act - reaches incipient antitrust violations and conduct violating spirit but not letter of antitrust laws.
        FTC v. Indiana Federation of Dentists, 476 U.S. 447 (1986): restraints unjustified by procompetitive benefits are unfair methods.
        2022 FTC Policy Statement on Section 5: FTC may challenge conduct as standalone Section 5 violation without proving
        Sherman or Clayton Act violation. Factors: (1) violation of antitrust spirit, (2) tendency to negatively affect competitive
        conditions, (3) lack of countervailing procompetitive justification.
        Controversial: 2015 FTC Policy Statement (rescinded 2022) limited standalone Section 5 to conduct likely to harm competition
        and lacking cognizable efficiencies.
        Applies only to FTC enforcement, not private plaintiffs (no private right of action under Section 5).
        Examples: invitations to collude, loyalty rebates not meeting rule of reason standard, unfair contract terms in standard-setting.
        """,
        key_factors=[
            "Conduct violates antitrust spirit or policy",
            "Tendency to harm competitive process",
            "Lack of procompetitive justification",
            "Incipient violation or borderline conduct",
            "Coercive, deceptive, or collusive nature",
            "FTC enforcement discretion (no private right of action)"
        ],
        primary_authority=[
            "15 USC Section 45 (FTC Act Section 5)",
            "FTC v. Indiana Federation of Dentists, 476 U.S. 447 (1986)",
            "FTC Policy Statement on Section 5 (Nov. 2022)",
            "FTC v. Sperry & Hutchinson Co., 405 U.S. 233 (1972)"
        ],
        burden_holder="FTC",
        adversary_position="Conduct lawful under Sherman/Clayton Acts, procompetitive justifications, no competitive harm",
        counter_arguments=[
            "Conduct does not violate Sherman or Clayton Acts",
            "Procompetitive justifications outweigh harms",
            "No actual or likely competitive harm shown",
            "2022 Policy Statement exceeds statutory authority (challenge in court)",
            "Conduct is unilateral and protected (Trinko, Brooke Group)"
        ],
        resolution_strategy="Understand FTC's broader Section 5 authority, distinguish from Sherman/Clayton standards, assess policy factors",
        entity_scope="FTC enforcement targets (no private actions)",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="2022 Policy Statement expansive but untested in courts, legal authority contested",
        controlling_precedent="Indiana Federation of Dentists (unfair methods), 2022 FTC Policy Statement (controversial)",
        categories=[IssueCategory.HORIZONTAL_AGREEMENT, IssueCategory.VERTICAL_RESTRAINT, IssueCategory.MONOPOLIZATION]
    ),
    DoctrineBlock(
        topic="Joint Ventures - Rule of Reason and Integration Analysis",
        keywords=["joint venture", "integration", "ancillary restraints", "efficiency", "collaboration"],
        conclusion_template=[
            "Joint ventures integrating economic activity to create efficiencies are analyzed under rule of reason.",
            "Ancillary restraints reasonably necessary to achieve venture's procompetitive benefits may be lawful.",
            "Naked restraints without integration remain per se illegal or highly suspect."
        ],
        reasoning_framework="""
        Joint ventures: collaboration among competitors to integrate functions (production, R&D, distribution).
        Ancillary restraints doctrine (Addyston Pipe): restraints reasonably necessary to effectuate legitimate collaboration
        are ancillary and analyzed under rule of reason; naked restraints (no legitimate collaboration) are per se illegal.
        Texaco Inc. v. Dagher, 547 U.S. 1 (2006): pricing decisions of legitimate joint venture (single economic entity)
        are not per se illegal price fixing.
        Broadcast Music, Inc. v. CBS, 441 U.S. 1 (1979): joint licensing arrangement creating new product (blanket license)
        is procompetitive integration, analyzed under rule of reason despite price setting.
        Rule of reason analysis: (1) legitimate integration creating efficiencies, (2) restraints ancillary to integration,
        (3) competitive harms do not outweigh benefits, (4) no less restrictive alternatives.
        Competitor Collaboration Guidelines (2000): ventures integrating significant capital or technology, sharing risks,
        creating new products are likely procompetitive.
        Examples: R&D consortia, production joint ventures, joint bidding (if necessary for project scale), standard-setting.
        Naked restraints: no integration - price fixing, market allocation, bid rigging among competitors without efficiency-creating venture.
        """,
        key_factors=[
            "Legitimate economic integration of capital, technology, or risk",
            "Creation of new product or significant efficiencies",
            "Restraints ancillary and reasonably necessary to venture",
            "Limited scope and duration of restraints",
            "Preservation of competition outside venture (e.g., interbrand)",
            "Market share of venture and parents"
        ],
        primary_authority=[
            "15 USC Section 1",
            "Texaco Inc. v. Dagher, 547 U.S. 1 (2006)",
            "Broadcast Music, Inc. v. Columbia Broadcasting System, Inc., 441 U.S. 1 (1979)",
            "United States v. Addyston Pipe & Steel Co., 85 F. 271 (6th Cir. 1898), aff'd 175 U.S. 211 (1899)",
            "DOJ/FTC Competitor Collaboration Guidelines (2000)"
        ],
        burden_holder="Plaintiff to prove anticompetitive effects, defendant to show integration and efficiencies",
        adversary_position="Legitimate integration, ancillary restraints necessary, strong efficiencies, interbrand competition robust",
        counter_arguments=[
            "Venture integrates significant capital or technology",
            "New product or cost savings created by collaboration",
            "Restraints necessary to prevent free-riding or accomplish venture goals",
            "Limited market share, interbrand competition constrains",
            "Less restrictive alternatives infeasible or ineffective"
        ],
        resolution_strategy="Assess integration substantiveness, verify ancillary necessity of restraints, quantify efficiencies",
        entity_scope="Collaborations among actual or potential competitors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established rule of reason framework, fact-intensive, integration key",
        controlling_precedent="Texaco (single entity doctrine), BMI (integration creating new product)",
        categories=[IssueCategory.HORIZONTAL_AGREEMENT]
    ),
    DoctrineBlock(
        topic="Refusal to Deal - Aspen Skiing and Trinko Limits",
        keywords=["refusal to deal", "essential facility", "duty to deal", "Aspen Skiing", "Trinko"],
        conclusion_template=[
            "Unilateral refusal to deal generally lawful - no antitrust duty to help competitors.",
            "Exception: refusal to continue profitable course of dealing (Aspen Skiing) may violate Section 2.",
            "Trinko narrowed exception - no duty to deal absent prior voluntary cooperation, regulated industries unlikely to face liability."
        ],
        reasoning_framework="""
        General rule: firm with monopoly power has no duty to deal with rivals - Verizon v. Trinko, 540 U.S. 398 (2004).
        Aspen Skiing exception: if monopolist terminates profitable voluntary cooperation, sacrificing short-term profits to
        eliminate rival, refusal may be exclusionary conduct violating Section 2.
        Aspen Skiing Co. v. Aspen Highlands Skiing Corp., 472 U.S. 585 (1985): refusal to sell joint ski lift tickets after
        years of cooperation, with no efficiency justification, is monopolization.
        Trinko limits Aspen: (1) prior course of dealing required (Trinko no prior dealing), (2) regulatory context creates
        alternative remedies (telecom regulation), (3) forced sharing risks chilling innovation, (4) difficult to administer.
        Essential facility doctrine: disfavored - no Supreme Court endorsement, lower courts split.
        Elements if recognized: (1) control of essential facility, (2) inability to duplicate, (3) denial of access, (4) feasibility of providing access.
        2023 Merger Guidelines Guideline 5 addresses input foreclosure (related to refusal to deal in merger context).
        """,
        key_factors=[
            "Prior voluntary course of dealing",
            "Profit sacrifice from refusal (short-term loss for long-term monopoly gain)",
            "Lack of legitimate efficiency justification",
            "Termination of cooperation vs. never dealing",
            "Regulatory regime providing alternative remedies",
            "Essentiality and inimitability of resource"
        ],
        primary_authority=[
            "15 USC Section 2",
            "Verizon Communications Inc. v. Law Offices of Curtis V. Trinko, LLP, 540 U.S. 398 (2004)",
            "Aspen Skiing Co. v. Aspen Highlands Skiing Corp., 472 U.S. 585 (1985)",
            "United States v. Terminal Railroad Assn, 224 U.S. 383 (1912) (essential facility origins)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No duty to deal, no prior dealing, efficiency justification, regulated industry",
        counter_arguments=[
            "No prior voluntary course of dealing (Trinko)",
            "Efficiency or cost justification for refusal",
            "Alternative remedies in regulated industry",
            "Resource not essential - rivals can compete without it",
            "Forced sharing chills investment and innovation"
        ],
        resolution_strategy="Distinguish Aspen scenario (prior dealing, profit sacrifice) from general refusal (no duty), assess Trinko factors",
        entity_scope="Monopolist refusing access to input or facility",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Very narrow exception post-Trinko, high bar for plaintiffs, essential facility doctrine disfavored",
        controlling_precedent="Trinko (no general duty to deal), Aspen Skiing (exception for prior dealing termination)",
        categories=[IssueCategory.MONOPOLIZATION]
    ),
    DoctrineBlock(
        topic="Hart-Scott-Rodino Act - Merger Notification Thresholds",
        keywords=["HSR", "Hart-Scott-Rodino", "premerger notification", "waiting period", "size of transaction"],
        conclusion_template=[
            "Hart-Scott-Rodino Act requires premerger notification to FTC and DOJ for transactions meeting size thresholds.",
            "2024 thresholds (adjusted annually): >$119.5M transaction size triggers filing if size-of-person test met.",
            "30-day waiting period (15 days for cash tender offers) before closing, extendable by Second Request."
        ],
        reasoning_framework="""
        15 USC Section 18a (Hart-Scott-Rodino Antitrust Improvements Act of 1976): premerger notification and waiting period.
        Purpose: give FTC and DOJ opportunity to review and challenge anticompetitive mergers before consummation.
        2024 thresholds (adjusted annually for GNP changes):
        - Size of transaction: >$119.5M (reportable), <$478M (size-of-person test applies), >$478M (always reportable).
        - Size of person test (if transaction $119.5M-$478M): one party >$239M assets/sales, other >$23.9M assets/sales.
        Exemptions: normal course purchases <$119.5M, certain asset classes (real property for personal use), foreign transactions
        not affecting US commerce.
        Filing: HSR form, filing fee (tiered: $30K for <$176.5M, up to $2.25M for >$5B transactions), documents.
        Waiting period: 30 days from filing (15 days cash tender, 30 days for others), clock stops if Second Request issued.
        Second Request: FTC/DOJ demand for additional documents and information - burdensome, extends waiting indefinitely until compliance.
        Violations: $50,120 per day civil penalty (2024 inflation-adjusted) for gun-jumping (closing before clearance).
        """,
        key_factors=[
            "Size of transaction value",
            "Size of person (assets or annual net sales)",
            "Exemptions (real property, foreign, securities)",
            "Filing completeness and certification",
            "Waiting period expiration or early termination",
            "Second Request compliance burden"
        ],
        primary_authority=[
            "15 USC Section 18a (HSR Act)",
            "16 CFR Part 801-803 (HSR Rules)",
            "FTC Premerger Notification Office guidance",
            "Annual threshold adjustments (published in Federal Register)"
        ],
        burden_holder="Merging parties to file and comply",
        adversary_position="Transaction below thresholds, exempt, foreign with no US effects, filing complete and waiting period expired",
        counter_arguments=[
            "Transaction size below $119.5M threshold",
            "Size-of-person test not met (both parties small)",
            "Exemption applies (real property, securities, foreign)",
            "Waiting period expired without Second Request",
            "Early termination granted by agencies"
        ],
        resolution_strategy="Calculate transaction value and party sizes accurately, assess exemptions, prepare for possible Second Request",
        entity_scope="Mergers and acquisitions meeting size thresholds",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Procedural compliance mandatory, penalties severe for gun-jumping, thresholds clear but annual adjustments",
        controlling_precedent="HSR Act statute and regulations, FTC enforcement actions for violations",
        categories=[IssueCategory.MERGER_REVIEW]
    ),
    DoctrineBlock(
        topic="2023 Merger Guidelines - Key Shifts and Presumptions",
        keywords=["2023 Merger Guidelines", "structural presumption", "HHI thresholds", "guideline 1", "guideline 5"],
        conclusion_template=[
            "2023 Merger Guidelines reflect more aggressive enforcement stance than 2010 Guidelines.",
            "Structural presumptions apply at lower HHI thresholds, guideline-based framework replaces unified analysis.",
            "Vertical mergers face structural presumptions (Guideline 5), serial acquisitions scrutinized (Guideline 7)."
        ],
        reasoning_framework="""
        Released December 2023 by DOJ and FTC, replacing 2010 Horizontal Merger Guidelines and 2020 Vertical Merger Guidelines.
        13 Guidelines organized by theory of harm:
        1. Mergers should not significantly increase concentration in highly concentrated markets (HHI >1800, delta >100 presumption)
        2. Mergers should not eliminate substantial competition between firms (close competitors, head-to-head)
        3. Mergers should not increase risk of coordination (oligopoly, transparency, history of coordination)
        4. Mergers should not eliminate potential entrant (perceived or actual potential competition)
        5. Mergers should not create firm controlling products/services rivals need (vertical and foreclosure)
        6. Mergers should not entrench or extend dominant position (self-reinforcing advantages)
        7. Mergers should not further trend toward concentration (serial acquisitions, concentration creep)
        8. Mergers should not eliminate maverick firm (disruptive competitor constraining rivals)
        9. Mergers should not give buyer power to reduce workers' wages/benefits (labor market monopsony)
        10. Mergers should not involve multi-sided platforms in ways that may substantially lessen competition
        11. Mergers should not involve competing buyers (monopsony, supplier foreclosure)
        12. Mergers should not entrench or extend dominant position via data advantages
        13. Mergers should not eliminate direct competition for innovative products or threats to dominant firms
        Lower HHI safe harbors, skepticism of efficiencies, emphasis on qualitative factors (e.g., innovation harm).
        """,
        key_factors=[
            "Post-merger HHI and delta (Guideline 1 thresholds)",
            "Elimination of close competitor (Guideline 2)",
            "Coordinated effects risk (Guideline 3)",
            "Potential competition loss (Guideline 4)",
            "Vertical foreclosure (Guideline 5)",
            "Serial acquisitions and concentration trend (Guideline 7)",
            "Innovation competition harm (Guideline 13)"
        ],
        primary_authority=[
            "2023 DOJ/FTC Merger Guidelines (Dec. 2023)",
            "15 USC Section 18 (Clayton Act Section 7)",
            "Philadelphia National Bank (structural presumption)",
            "Baker Hughes (rebuttal of presumption)"
        ],
        burden_holder="Government to establish prima facie case, parties to rebut",
        adversary_position="Below thresholds, no close competition, robust entry, efficiencies, failing firm",
        counter_arguments=[
            "HHI below Guideline 1 thresholds",
            "Merging firms not close competitors (differentiated products)",
            "Timely and likely entry sufficient to deter harm",
            "Substantial verifiable merger-specific efficiencies",
            "Broader market definition reduces concentration",
            "No credible theory of competitive harm"
        ],
        resolution_strategy="Analyze under all 13 Guidelines, emphasize qualitative competitive effects, assess innovation and labor market impacts",
        entity_scope="All merger reviews by DOJ and FTC",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Guidelines shift enforcement posture more aggressive, but courts may not adopt all presumptions, challenges likely",
        controlling_precedent="2023 Merger Guidelines (agency policy, not binding law but persuasive)",
        categories=[IssueCategory.MERGER_REVIEW]
    )
]

class QueryRequest(BaseModel):
    query: str = Field(..., description="Antitrust legal query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis zone for position separation")

class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    response: str
    triggered_doctrines: List[str]
    issue_categories: List[IssueCategory]
    confidence: ConfidenceLevel
    determinism_hash: str
    query_id: str
    timestamp: str
    latency_ms: float
    response_layer: str

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float

app = FastAPI(title=ENGINE_NAME, version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

start_time = datetime.now()
query_count = 0
total_latency_ms = 0.0
doctrine_hit_counts: Dict[str, int] = defaultdict(int)
error_counts: Dict[str, int] = defaultdict(int)

logger.add(
    Path(__file__).parent / "logs" / "engine_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

def normalize_query(query: str) -> str:
    """Normalize query for semantic matching"""
    return query.lower().strip()

def match_doctrines(query: str) -> List[DoctrineBlock]:
    """Match query to doctrine blocks via keyword matching"""
    normalized = normalize_query(query)
    tokens = set(normalized.split())

    scored = []
    for doctrine in DOCTRINE_CACHE:
        keywords_lower = [kw.lower() for kw in doctrine.keywords]
        matches = sum(1 for kw in keywords_lower if kw in normalized or any(kw in token for token in tokens))
        if matches > 0:
            scored.append((matches, doctrine))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:5]]

def build_fast_response(doctrines: List[DoctrineBlock], query: str) -> str:
    """Layer 0: Fast response from doctrine cache"""
    if not doctrines:
        return "No specific antitrust doctrine matched. Please refine query with terms like Sherman Act, Clayton Act, merger, monopolization, price fixing, tying, exclusive dealing, etc."

    top = doctrines[0]
    conclusions = " ".join(top.conclusion_template)
    authority = ", ".join(top.primary_authority[:3])
    return f"{conclusions} Authority: {authority}."

def build_defense_response(doctrines: List[DoctrineBlock], query: str, zone: AnalysisZone) -> str:
    """Layer 1: Defense-ready response with authority and framework"""
    if not doctrines:
        return build_fast_response(doctrines, query)

    top = doctrines[0]
    sections = [
        f"ANTITRUST ANALYSIS - {top.topic.upper()}",
        "",
        "CONCLUSION:",
        "\n".join(f"- {c}" for c in top.conclusion_template),
        "",
        "LEGAL FRAMEWORK:",
        top.reasoning_framework.strip(),
        "",
        "KEY FACTORS:",
        "\n".join(f"- {f}" for f in top.key_factors),
        "",
        "PRIMARY AUTHORITY:",
        "\n".join(f"- {a}" for a in top.primary_authority),
        "",
        f"BURDEN: {top.burden_holder}",
        f"CONFIDENCE: {top.confidence.value} - {top.confidence_stratification}"
    ]

    if zone == AnalysisZone.PLANNING:
        sections.extend([
            "",
            "PLANNING CONSIDERATIONS:",
            f"- {top.resolution_strategy}",
            "- Gather evidence on key factors listed above",
            "- Anticipate adversary position and counter-arguments"
        ])
    elif zone == AnalysisZone.AUDIT:
        sections.extend([
            "",
            "AUDIT TRAIL:",
            f"- Doctrine: {top.topic}",
            f"- Authority: {top.controlling_precedent}",
            f"- Entity Scope: {top.entity_scope}",
            f"- Categories: {', '.join(c.value for c in top.categories)}"
        ])

    return "\n".join(sections)

def build_memo_response(doctrines: List[DoctrineBlock], query: str, zone: AnalysisZone) -> str:
    """Layer 2: Full memorandum with multi-doctrine synthesis"""
    if not doctrines:
        return build_defense_response(doctrines, query, zone)

    sections = [
        "ANTITRUST LEGAL MEMORANDUM",
        "=" * 60,
        "",
        f"QUERY: {query}",
        f"ZONE: {zone.value}",
        "",
        "APPLICABLE DOCTRINES:",
        ""
    ]

    for i, doctrine in enumerate(doctrines[:3], 1):
        sections.extend([
            f"{i}. {doctrine.topic}",
            f"   Categories: {', '.join(c.value for c in doctrine.categories)}",
            f"   Confidence: {doctrine.confidence.value}",
            ""
        ])

    primary = doctrines[0]
    sections.extend([
        "PRIMARY ANALYSIS:",
        "-" * 60,
        "",
        "LEGAL STANDARD:",
        primary.reasoning_framework.strip(),
        "",
        "ELEMENTS AND FACTORS:",
        "\n".join(f"- {f}" for f in primary.key_factors),
        "",
        "BURDEN OF PROOF:",
        f"- {primary.burden_holder}",
        "",
        "CONTROLLING AUTHORITY:",
        "\n".join(f"- {a}" for a in primary.primary_authority),
        "",
        "ADVERSARY POSITION:",
        f"- {primary.adversary_position}",
        "",
        "COUNTER-ARGUMENTS:",
        "\n".join(f"- {c}" for c in primary.counter_arguments),
        "",
        "RESOLUTION STRATEGY:",
        f"- {primary.resolution_strategy}",
        "",
        "CONFIDENCE ASSESSMENT:",
        f"- Level: {primary.confidence.value}",
        f"- Stratification: {primary.confidence_stratification}",
        ""
    ])

    if zone == AnalysisZone.PLANNING:
        sections.extend([
            "PLANNING ROADMAP:",
            "- Define relevant market (product and geographic dimensions)",
            "- Calculate market shares and HHI if merger or monopolization",
            "- Gather evidence on communications, agreements, or unilateral conduct",
            "- Identify procompetitive justifications and efficiencies",
            "- Assess less restrictive alternatives",
            "- Prepare for burden-shifting (prima facie case, rebuttal, alternatives)",
            ""
        ])
    elif zone == AnalysisZone.REPORTING:
        sections.extend([
            "REPORTING CONSIDERATIONS:",
            "- Present findings objectively with clear factual support",
            "- Cite primary authority for all legal conclusions",
            "- Flag areas of legal uncertainty or factual gaps",
            "- Avoid advocacy in reporting zone (save for planning/audit zones)",
            ""
        ])
    elif zone == AnalysisZone.AUDIT:
        sections.extend([
            "AUDIT VERIFICATION:",
            f"- Doctrine ID: {primary.topic}",
            f"- Authority Chain: {primary.controlling_precedent}",
            f"- Entity Scope: {primary.entity_scope}",
            f"- Issue Categories: {', '.join(c.value for c in primary.categories)}",
            f"- Confidence Basis: {primary.confidence_stratification}",
            ""
        ])

    if len(doctrines) > 1:
        sections.extend([
            "RELATED DOCTRINES:",
            ""
        ])
        for doctrine in doctrines[1:3]:
            sections.extend([
                f"- {doctrine.topic}",
                f"  {doctrine.conclusion_template[0]}",
                f"  Authority: {doctrine.controlling_precedent}",
                ""
            ])

    return "\n".join(sections)

def compute_determinism_hash(query: str, mode: ResponseMode, zone: AnalysisZone, response: str) -> str:
    """SHA-256 hash for deterministic verification"""
    content = f"{query}|{mode.value}|{zone.value}|{response}"
    return hashlib.sha256(content.encode()).hexdigest()

@app.post("/query", response_model=QueryResponse)
async def query_engine(req: QueryRequest):
    """Main query endpoint with three-layer response"""
    global query_count, total_latency_ms

    start = datetime.now()
    query_id = hashlib.sha256(f"{req.query}{start.isoformat()}".encode()).hexdigest()[:16]

    try:
        doctrines = match_doctrines(req.query)

        for d in doctrines:
            doctrine_hit_counts[d.topic] += 1

        if req.mode == ResponseMode.FAST:
            response_text = build_fast_response(doctrines, req.query)
            layer = "DOCTRINE_CACHE"
        elif req.mode == ResponseMode.DEFENSE:
            response_text = build_defense_response(doctrines, req.query, req.zone)
            layer = "SEMANTIC_RETRIEVAL"
        else:
            response_text = build_memo_response(doctrines, req.query, req.zone)
            layer = "DEEP_ANALYSIS"

        categories = list(set(cat for d in doctrines for cat in d.categories))
        confidence = doctrines[0].confidence if doctrines else ConfidenceLevel.HIGH_RISK

        end = datetime.now()
        latency = (end - start).total_seconds() * 1000

        query_count += 1
        total_latency_ms += latency

        det_hash = compute_determinism_hash(req.query, req.mode, req.zone, response_text)

        logger.info(f"Query {query_id} | Mode: {req.mode.value} | Zone: {req.zone.value} | Latency: {latency:.2f}ms | Doctrines: {len(doctrines)}")

        return QueryResponse(
            query=req.query,
            mode=req.mode,
            zone=req.zone,
            response=response_text,
            triggered_doctrines=[d.topic for d in doctrines],
            issue_categories=categories,
            confidence=confidence,
            determinism_hash=det_hash,
            query_id=query_id,
            timestamp=start.isoformat(),
            latency_ms=round(latency, 2),
            response_layer=layer
        )

    except Exception as e:
        error_counts[type(e).__name__] += 1
        logger.error(f"Query {query_id} failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health endpoint with operational metrics"""
    uptime = (datetime.now() - start_time).total_seconds()

    return HealthResponse(
        status="operational",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=round(uptime, 2)
    )

@app.get("/metrics")
async def get_metrics():
    """Telemetry metrics endpoint"""
    uptime = (datetime.now() - start_time).total_seconds()
    avg_latency = total_latency_ms / query_count if query_count > 0 else 0

    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": VERSION,
        "uptime_seconds": round(uptime, 2),
        "total_queries": query_count,
        "average_latency_ms": round(avg_latency, 2),
        "doctrine_hits": dict(doctrine_hit_counts),
        "error_counts": dict(error_counts),
        "doctrines_loaded": len(DOCTRINE_CACHE)
    }

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
