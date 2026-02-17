from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Sherman Act Section 1 - Horizontal Price Fixing",
        keywords=["Sherman Act", "Section 1", "horizontal", "price fixing", "agreement", "per se illegal"],
        conclusion_template="If competitors agree to fix prices, such conduct constitutes a per se violation of Section 1 of the Sherman Act.",
        reasoning_framework=(
            "Horizontal price fixing involves agreements among competitors to set prices or price-related terms. "
            "Courts treat such conduct as per se illegal, meaning no inquiry into market power or anticompetitive effects is required. "
            "The plaintiff must show: (1) an agreement or concerted action among competitors; (2) the agreement relates to price or price-related terms. "
            "Direct evidence of agreement (such as explicit communications) is sufficient, but circumstantial evidence (such as parallel conduct plus 'plus factors') may also suffice. "
            "Defendants may argue lack of agreement or independent decision-making, but the existence of an agreement is determinative. "
            "No procompetitive justification is permitted under the per se rule. Remedies include injunctions, treble damages, and criminal penalties."
        ),
        key_factors=[
            "Existence of an agreement among competitors",
            "Nature of price-related terms fixed",
            "Direct or circumstantial evidence",
            "Market structure and opportunity for collusion",
            "Absence of legitimate joint venture or integration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. Socony-Vacuum Oil Co., 310 U.S. 150 (1940)",
            "United States v. Trenton Potteries Co., 273 U.S. 392 (1927)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement existed; actions were independent; conduct was procompetitive or justified",
        counter_arguments=[
            "No evidence of actual agreement",
            "Parallel conduct is not sufficient",
            "Joint venture exception applies"
        ],
        resolution_strategy="Evaluate evidence for explicit or tacit agreement; apply per se rule if agreement found; reject defenses based on procompetitive justification.",
        entity_scope="Competitors in the same market",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Socony-Vacuum Oil Co."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Bid Rigging",
        keywords=["Sherman Act", "Section 1", "bid rigging", "collusion", "per se illegal"],
        conclusion_template="Bid rigging agreements among competitors are per se violations of Section 1 of the Sherman Act.",
        reasoning_framework=(
            "Bid rigging involves competitors agreeing to manipulate bids, such as rotating winning bids, suppressing bids, or submitting complementary bids. "
            "Such conduct is per se illegal under Section 1. The plaintiff must demonstrate: (1) an agreement among competitors; (2) the agreement affects the bidding process. "
            "Evidence may include communications, patterns of winning, or statistical anomalies. Defendants may argue lack of agreement or legitimate joint ventures, but courts rarely accept such defenses. "
            "Remedies include criminal prosecution, injunctions, and treble damages."
        ),
        key_factors=[
            "Existence of an agreement",
            "Nature of bid manipulation",
            "Evidence of communication or coordination",
            "Pattern of winning bids",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. Portsmouth Paving Corp., 694 F.2d 312 (4th Cir. 1982)",
            "United States v. Koppers Co., 652 F.2d 290 (2d Cir. 1981)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; independent bidding; legitimate joint venture",
        counter_arguments=[
            "No evidence of collusion",
            "Bid patterns explained by market conditions",
            "Joint venture exception applies"
        ],
        resolution_strategy="Assess evidence for collusion; apply per se rule; reject defenses based on market conditions unless credible.",
        entity_scope="Competitors submitting bids",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Portsmouth Paving Corp."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Market Allocation",
        keywords=["Sherman Act", "Section 1", "market allocation", "territory", "customer", "per se illegal"],
        conclusion_template="Agreements among competitors to allocate markets, territories, or customers are per se violations of Section 1.",
        reasoning_framework=(
            "Market allocation agreements divide markets, territories, or customers among competitors, suppressing competition. "
            "Such conduct is per se illegal under Section 1. Plaintiff must show: (1) an agreement among competitors; (2) allocation of market, territory, or customer base. "
            "Evidence may include explicit agreements, patterns of non-competition, or communications. Defendants may argue lack of agreement or legitimate joint ventures, but courts rarely accept such defenses. "
            "Remedies include injunctions, treble damages, and criminal penalties."
        ),
        key_factors=[
            "Existence of agreement",
            "Nature of allocation (territory, customer, product)",
            "Evidence of communication",
            "Pattern of non-competition",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. Topco Associates, Inc., 405 U.S. 596 (1972)",
            "United States v. Addyston Pipe & Steel Co., 85 F. 271 (6th Cir. 1898)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; independent conduct; legitimate joint venture",
        counter_arguments=[
            "No evidence of allocation",
            "Market division explained by business strategy",
            "Joint venture exception applies"
        ],
        resolution_strategy="Analyze evidence for explicit or tacit allocation; apply per se rule if agreement found.",
        entity_scope="Competitors in the same market",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Topco Associates, Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Rule of Reason Framework",
        keywords=["Sherman Act", "Section 1", "rule of reason", "competitive effects", "analysis"],
        conclusion_template="If conduct is not per se illegal, apply the rule of reason to assess whether it unreasonably restrains trade.",
        reasoning_framework=(
            "The rule of reason requires a comprehensive analysis of the challenged restraint's competitive effects. "
            "Plaintiff must show: (1) an agreement; (2) actual or potential anticompetitive effects in the relevant market. "
            "Court evaluates: market definition, market power, procompetitive justifications, and less restrictive alternatives. "
            "Defendant may present evidence of procompetitive benefits (efficiency, innovation, consumer welfare). "
            "Plaintiff may rebut by showing less restrictive means or that anticompetitive effects outweigh benefits. "
            "Burden shifts between parties: plaintiff shows prima facie anticompetitive effect; defendant rebuts with justification; plaintiff rebuts with less restrictive alternatives. "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Market definition",
            "Market power",
            "Nature of restraint",
            "Procompetitive justifications",
            "Availability of less restrictive alternatives"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "Continental T.V., Inc. v. GTE Sylvania, Inc., 433 U.S. 36 (1977)",
            "NCAA v. Board of Regents, 468 U.S. 85 (1984)"
        ],
        burden_holder="Plaintiff (initial), Defendant (justification), Plaintiff (rebuttal)",
        adversary_position="Restraint is procompetitive; no anticompetitive effect; less restrictive alternatives unavailable",
        counter_arguments=[
            "Restraint enhances competition",
            "Market power insufficient",
            "No less restrictive alternatives"
        ],
        resolution_strategy="Apply burden-shifting framework; weigh anticompetitive effects against procompetitive justifications.",
        entity_scope="All entities subject to Section 1",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Continental T.V., Inc. v. GTE Sylvania, Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 2 - Monopolization Elements",
        keywords=["Sherman Act", "Section 2", "monopolization", "market power", "exclusionary conduct"],
        conclusion_template="A violation of Section 2 requires (1) possession of monopoly power and (2) willful acquisition or maintenance of that power through exclusionary conduct.",
        reasoning_framework=(
            "Section 2 prohibits monopolization, requiring proof of: (1) monopoly power in the relevant market; (2) willful acquisition or maintenance of that power, as opposed to growth through superior product, business acumen, or historic accident. "
            "Monopoly power is defined as the power to control prices or exclude competition. "
            "Exclusionary conduct includes actions that harm competition, not merely competitors. "
            "Plaintiff must define the relevant market and show defendant's power and exclusionary acts. "
            "Defendant may argue lack of monopoly power or that conduct was competition on the merits. "
            "Remedies include injunctions and treble damages."
        ),
        key_factors=[
            "Relevant market definition",
            "Market share and power",
            "Nature of exclusionary conduct",
            "Intent to monopolize",
            "Harm to competition"
        ],
        primary_authority=[
            "Sherman Act §2, 15 U.S.C. §2",
            "United States v. Grinnell Corp., 384 U.S. 563 (1966)",
            "Aspen Skiing Co. v. Aspen Highlands Skiing Corp., 472 U.S. 585 (1985)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No monopoly power; conduct was lawful competition; no exclusionary effect",
        counter_arguments=[
            "Market share insufficient",
            "Conduct was procompetitive",
            "No harm to competition"
        ],
        resolution_strategy="Define relevant market; assess market power; evaluate exclusionary conduct and intent.",
        entity_scope="Dominant firms in relevant markets",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Grinnell Corp."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 2 - Attempted Monopolization",
        keywords=["Sherman Act", "Section 2", "attempted monopolization", "dangerous probability", "anticompetitive conduct"],
        conclusion_template="Attempted monopolization requires (1) anticompetitive conduct, (2) specific intent to monopolize, and (3) dangerous probability of success.",
        reasoning_framework=(
            "Attempted monopolization is established by showing: (1) anticompetitive or exclusionary conduct; (2) specific intent to monopolize; (3) dangerous probability of achieving monopoly power. "
            "Plaintiff must define the relevant market and demonstrate defendant's conduct and intent. "
            "Dangerous probability is assessed by market share, barriers to entry, and conduct. "
            "Defendant may argue lack of intent, insufficient probability, or lawful conduct. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Relevant market definition",
            "Nature of conduct",
            "Specific intent",
            "Market share",
            "Barriers to entry"
        ],
        primary_authority=[
            "Sherman Act §2, 15 U.S.C. §2",
            "Spectrum Sports, Inc. v. McQuillan, 506 U.S. 447 (1993)",
            "United States v. American Airlines, Inc., 743 F.2d 1114 (5th Cir. 1984)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No intent; conduct was lawful; no dangerous probability",
        counter_arguments=[
            "Market share insufficient",
            "Conduct was procompetitive",
            "No specific intent"
        ],
        resolution_strategy="Define market; assess conduct and intent; evaluate probability of monopoly power.",
        entity_scope="Firms with significant market share",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Spectrum Sports, Inc. v. McQuillan"
    ),
    DoctrineBlock(
        topic="Clayton Act Section 7 - Merger Analysis Framework",
        keywords=["Clayton Act", "Section 7", "merger", "acquisition", "substantial lessening", "competitive effects"],
        conclusion_template="A merger violates Section 7 if it may substantially lessen competition or tend to create a monopoly.",
        reasoning_framework=(
            "Section 7 prohibits mergers and acquisitions where the effect may be substantially to lessen competition or tend to create a monopoly. "
            "Analysis includes: (1) relevant market definition; (2) assessment of market concentration (HHI); (3) competitive effects (unilateral and coordinated); (4) entry barriers; (5) efficiencies and failing firm defense. "
            "Agencies apply thresholds for market concentration and presumptions of illegality. "
            "Defendants may argue efficiencies, failing firm, or lack of competitive harm. "
            "Remedies include blocking, divestiture, or behavioral remedies."
        ),
        key_factors=[
            "Relevant market definition",
            "Market concentration (HHI)",
            "Competitive effects",
            "Entry barriers",
            "Efficiencies"
        ],
        primary_authority=[
            "Clayton Act §7, 15 U.S.C. §18",
            "United States v. Philadelphia National Bank, 374 U.S. 321 (1963)",
            "FTC v. H.J. Heinz Co., 246 F.3d 708 (D.C. Cir. 2001)"
        ],
        burden_holder="Plaintiff (government or private)",
        adversary_position="Merger is procompetitive; efficiencies outweigh harm; failing firm defense applies",
        counter_arguments=[
            "No substantial lessening of competition",
            "Efficiencies benefit consumers",
            "Entry barriers are low"
        ],
        resolution_strategy="Apply market definition and concentration analysis; weigh competitive effects and defenses.",
        entity_scope="Merging firms",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Philadelphia National Bank"
    ),
    DoctrineBlock(
        topic="Vertical Merger Analysis - Foreclosure Concerns",
        keywords=["vertical merger", "foreclosure", "input", "customer", "competitive effects"],
        conclusion_template="Vertical mergers may be challenged if they create foreclosure of inputs or customers, leading to anticompetitive effects.",
        reasoning_framework=(
            "Vertical mergers combine firms at different levels of the supply chain. "
            "Foreclosure concerns arise when the merged entity can deny rivals access to inputs or customers, raising rivals' costs or reducing competition. "
            "Analysis includes: (1) relevant market definition; (2) share of input or customer controlled; (3) likelihood and extent of foreclosure; (4) competitive effects; (5) efficiencies. "
            "Defendants may argue efficiencies or lack of foreclosure. "
            "Remedies may include divestiture or behavioral commitments."
        ),
        key_factors=[
            "Market definition",
            "Share of input/customer controlled",
            "Likelihood of foreclosure",
            "Competitive effects",
            "Efficiencies"
        ],
        primary_authority=[
            "2023 Merger Guidelines",
            "Brown Shoe Co. v. United States, 370 U.S. 294 (1962)",
            "FTC v. Staples, Inc., 970 F. Supp. 1066 (D.D.C. 1997)"
        ],
        burden_holder="Plaintiff (government or private)",
        adversary_position="Merger is procompetitive; no foreclosure; efficiencies outweigh harm",
        counter_arguments=[
            "No significant foreclosure",
            "Efficiencies benefit consumers",
            "Rivals have alternative sources"
        ],
        resolution_strategy="Assess foreclosure risk; weigh competitive effects and efficiencies; consider remedies.",
        entity_scope="Firms in vertical relationship",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown Shoe Co. v. United States"
    ),
    DoctrineBlock(
        topic="Tying Arrangements - Jefferson Parish Test",
        keywords=["tying", "Jefferson Parish", "Sherman Act", "Clayton Act", "market power", "coercion"],
        conclusion_template="A tying arrangement violates antitrust law if the seller has market power in the tying product and forces buyers to purchase a tied product.",
        reasoning_framework=(
            "Tying occurs when a seller conditions the sale of one product (tying) on the purchase of another (tied). "
            "The Jefferson Parish test requires: (1) two distinct products; (2) seller has market power in the tying product; (3) conditioning purchase; (4) substantial amount of commerce affected. "
            "If proven, tying may violate Section 1 (per se or rule of reason) or Section 3 of the Clayton Act. "
            "Defendants may argue lack of market power, no coercion, or procompetitive justification. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Distinct products",
            "Market power in tying product",
            "Coercion or conditioning",
            "Amount of commerce affected",
            "Procompetitive justifications"
        ],
        primary_authority=[
            "Jefferson Parish Hospital District No. 2 v. Hyde, 466 U.S. 2 (1984)",
            "Sherman Act §1, 15 U.S.C. §1",
            "Clayton Act §3, 15 U.S.C. §14"
        ],
        burden_holder="Plaintiff",
        adversary_position="No market power; no coercion; products not distinct; procompetitive justification",
        counter_arguments=[
            "No market power in tying product",
            "No coercion or conditioning",
            "Products are not distinct"
        ],
        resolution_strategy="Apply Jefferson Parish test; assess market power and coercion; weigh justifications.",
        entity_scope="Sellers with market power",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Jefferson Parish Hospital District No. 2 v. Hyde"
    ),
    DoctrineBlock(
        topic="Exclusive Dealing - Anticompetitive Foreclosure Standard",
        keywords=["exclusive dealing", "foreclosure", "Sherman Act", "Clayton Act", "rule of reason"],
        conclusion_template="Exclusive dealing violates antitrust law if it substantially forecloses rivals from the market and harms competition.",
        reasoning_framework=(
            "Exclusive dealing involves agreements that restrict buyers or sellers from dealing with rivals. "
            "Such arrangements are analyzed under the rule of reason. "
            "Plaintiff must show: (1) substantial foreclosure of rivals; (2) harm to competition, not just competitors; (3) relevant market definition. "
            "Defendants may argue procompetitive benefits (efficiency, quality control) or insufficient foreclosure. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Extent of foreclosure",
            "Market definition",
            "Duration and scope of agreement",
            "Procompetitive justifications",
            "Entry barriers"
        ],
        primary_authority=[
            "Tampa Electric Co. v. Nashville Coal Co., 365 U.S. 320 (1961)",
            "Sherman Act §1, 15 U.S.C. §1",
            "Clayton Act §3, 15 U.S.C. §14"
        ],
        burden_holder="Plaintiff",
        adversary_position="No substantial foreclosure; procompetitive benefits; low entry barriers",
        counter_arguments=[
            "Foreclosure is minimal",
            "Agreement enhances efficiency",
            "Rivals have alternative channels"
        ],
        resolution_strategy="Assess foreclosure percentage; weigh competitive effects; consider procompetitive justifications.",
        entity_scope="Manufacturers, distributors, retailers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tampa Electric Co. v. Nashville Coal Co."
    ),
    DoctrineBlock(
        topic="Robinson-Patman Act - Price Discrimination",
        keywords=["Robinson-Patman Act", "price discrimination", "injury to competition", "sales", "commodities"],
        conclusion_template="Price discrimination violates the Robinson-Patman Act if it lessens competition or injures competitors.",
        reasoning_framework=(
            "The Robinson-Patman Act prohibits price discrimination in sales of commodities where the effect may be to substantially lessen competition or injure competitors. "
            "Plaintiff must show: (1) sales to different buyers at different prices; (2) sales of commodities; (3) injury to competition or competitors. "
            "Defendants may argue cost justification, changing market conditions, or meeting competition. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Different prices to different buyers",
            "Commodity sales",
            "Injury to competition or competitors",
            "Cost justification",
            "Meeting competition defense"
        ],
        primary_authority=[
            "Robinson-Patman Act, 15 U.S.C. §13",
            "FTC v. Morton Salt Co., 334 U.S. 37 (1948)",
            "Texaco Inc. v. Hasbrouck, 496 U.S. 543 (1990)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Price difference justified; no injury; meeting competition defense",
        counter_arguments=[
            "Cost justification applies",
            "No injury to competition",
            "Price difference due to market conditions"
        ],
        resolution_strategy="Assess price differences; evaluate injury; consider defenses.",
        entity_scope="Sellers of commodities",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FTC v. Morton Salt Co."
    ),
    DoctrineBlock(
        topic="Resale Price Maintenance - Leegin Analysis",
        keywords=["resale price maintenance", "RPM", "Leegin", "rule of reason", "vertical restraints"],
        conclusion_template="Resale price maintenance is analyzed under the rule of reason; it may violate antitrust law if it unreasonably restrains trade.",
        reasoning_framework=(
            "Resale price maintenance (RPM) involves manufacturers setting minimum or maximum prices at which retailers may sell products. "
            "After Leegin, RPM is analyzed under the rule of reason. "
            "Plaintiff must show: (1) agreement on resale price; (2) anticompetitive effects in the relevant market. "
            "Defendants may argue procompetitive benefits (brand reputation, service). "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement on resale price",
            "Market definition",
            "Anticompetitive effects",
            "Procompetitive justifications",
            "Market power"
        ],
        primary_authority=[
            "Leegin Creative Leather Products, Inc. v. PSKS, Inc., 551 U.S. 877 (2007)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="RPM enhances competition; procompetitive benefits; no anticompetitive effect",
        counter_arguments=[
            "RPM promotes brand and service",
            "No market power",
            "No anticompetitive effect"
        ],
        resolution_strategy="Apply rule of reason; weigh anticompetitive effects against procompetitive justifications.",
        entity_scope="Manufacturers and retailers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Leegin Creative Leather Products, Inc. v. PSKS, Inc."
    ),
    DoctrineBlock(
        topic="State Action Immunity - Parker Doctrine",
        keywords=["state action immunity", "Parker doctrine", "antitrust immunity", "state policy", "active supervision"],
        conclusion_template="Conduct is immune from antitrust liability if it is taken pursuant to a clearly articulated state policy and actively supervised by the state.",
        reasoning_framework=(
            "State action immunity, under the Parker doctrine, exempts conduct from antitrust liability if: (1) the challenged action is taken pursuant to a clearly articulated and affirmatively expressed state policy; (2) the conduct is actively supervised by the state. "
            "Entities must demonstrate both prongs. "
            "Defendants may argue state policy and supervision; plaintiffs may challenge the sufficiency of articulation and supervision. "
            "Remedies include dismissal of antitrust claims."
        ),
        key_factors=[
            "Clear articulation of state policy",
            "Active state supervision",
            "Nature of entity (state or private)",
            "Scope of conduct",
            "Consistency with state objectives"
        ],
        primary_authority=[
            "Parker v. Brown, 317 U.S. 341 (1943)",
            "California Retail Liquor Dealers Ass'n v. Midcal Aluminum, Inc., 445 U.S. 97 (1980)"
        ],
        burden_holder="Defendant",
        adversary_position="No clear state policy; insufficient supervision; conduct is private",
        counter_arguments=[
            "State policy not clearly articulated",
            "No active supervision",
            "Conduct is not pursuant to state policy"
        ],
        resolution_strategy="Apply two-prong test; assess articulation and supervision; dismiss if immunity applies.",
        entity_scope="State entities and private actors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="California Retail Liquor Dealers Ass'n v. Midcal Aluminum, Inc."
    ),
    DoctrineBlock(
        topic="Noerr-Pennington Immunity - Petitioning Government",
        keywords=["Noerr-Pennington", "immunity", "petitioning", "government", "antitrust"],
        conclusion_template="Petitioning government for redress is immune from antitrust liability unless conduct is a sham.",
        reasoning_framework=(
            "Noerr-Pennington immunity protects efforts to petition government, including lobbying, litigation, and administrative proceedings. "
            "Immunity applies unless conduct is a sham (objectively baseless and intended to interfere through process rather than outcome). "
            "Plaintiff must show sham exception applies. "
            "Defendants may argue legitimate petitioning. "
            "Remedies include dismissal of antitrust claims."
        ),
        key_factors=[
            "Nature of petitioning activity",
            "Objective basis for petition",
            "Intent to interfere",
            "Sham exception",
            "Scope of immunity"
        ],
        primary_authority=[
            "Eastern R.R. Presidents Conference v. Noerr Motor Freight, Inc., 365 U.S. 127 (1961)",
            "California Motor Transport Co. v. Trucking Unlimited, 404 U.S. 508 (1972)"
        ],
        burden_holder="Plaintiff (to show sham)",
        adversary_position="Petitioning was legitimate; not a sham; protected by immunity",
        counter_arguments=[
            "Petitioning was objectively reasonable",
            "No intent to interfere",
            "Activity is protected"
        ],
        resolution_strategy="Assess objective basis and intent; apply sham exception if warranted.",
        entity_scope="Entities petitioning government",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Eastern R.R. Presidents Conference v. Noerr Motor Freight, Inc."
    ),
    DoctrineBlock(
        topic="Market Definition - SSNIP Test and HHI",
        keywords=["market definition", "SSNIP", "HHI", "relevant market", "antitrust analysis"],
        conclusion_template="Relevant market is defined by substitutability using the SSNIP test; market concentration is measured by HHI.",
        reasoning_framework=(
            "Market definition is critical in antitrust analysis. "
            "The SSNIP (Small but Significant and Non-transitory Increase in Price) test determines whether products are substitutes. "
            "Market concentration is measured by the Herfindahl-Hirschman Index (HHI). "
            "Plaintiff must define product and geographic market; agencies use SSNIP and HHI to assess competitive effects. "
            "Defendants may challenge market definition or concentration. "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Product substitutability",
            "Geographic scope",
            "SSNIP test results",
            "HHI calculation",
            "Market participants"
        ],
        primary_authority=[
            "2023 Merger Guidelines",
            "United States v. Philadelphia National Bank, 374 U.S. 321 (1963)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Market is broader/narrower; concentration is overstated; substitutes exist",
        counter_arguments=[
            "Market definition is incorrect",
            "HHI calculation flawed",
            "Substitutes constrain market power"
        ],
        resolution_strategy="Apply SSNIP test; calculate HHI; assess substitutability and concentration.",
        entity_scope="All entities in antitrust analysis",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Philadelphia National Bank"
    ),
    DoctrineBlock(
        topic="Conscious Parallelism - Plus Factors for Agreement",
        keywords=["conscious parallelism", "plus factors", "agreement", "Sherman Act", "circumstantial evidence"],
        conclusion_template="Conscious parallelism alone does not violate Section 1; plus factors are required to infer agreement.",
        reasoning_framework=(
            "Conscious parallelism refers to competitors acting similarly without explicit agreement. "
            "Section 1 requires proof of agreement, which may be inferred from circumstantial evidence and 'plus factors' such as communications, actions against self-interest, or market structure. "
            "Plaintiff must show parallel conduct and plus factors. "
            "Defendants may argue independent action. "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Parallel conduct",
            "Plus factors (communication, self-interest, market structure)",
            "Circumstantial evidence",
            "Market conditions",
            "Opportunity for collusion"
        ],
        primary_authority=[
            "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="Conduct was independent; no plus factors; market conditions explain behavior",
        counter_arguments=[
            "No evidence of agreement",
            "Plus factors absent",
            "Conduct explained by market"
        ],
        resolution_strategy="Assess parallel conduct and plus factors; infer agreement if evidence sufficient.",
        entity_scope="Competitors in the same market",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bell Atlantic Corp. v. Twombly"
    ),
    DoctrineBlock(
        topic="Predatory Pricing - Brooke Group Standard",
        keywords=["predatory pricing", "Brooke Group", "below cost", "recoupment", "Sherman Act", "Section 2"],
        conclusion_template="Predatory pricing violates Section 2 if prices are below cost and there is a dangerous probability of recoupment.",
        reasoning_framework=(
            "Predatory pricing involves setting prices below cost to drive rivals out and recoup losses later. "
            "Brooke Group standard requires: (1) pricing below an appropriate measure of cost; (2) dangerous probability of recoupment. "
            "Plaintiff must show both elements. "
            "Defendants may argue prices are above cost or recoupment is unlikely. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Pricing below cost",
            "Appropriate cost measure",
            "Probability of recoupment",
            "Market structure",
            "Barriers to entry"
        ],
        primary_authority=[
            "Brooke Group Ltd. v. Brown & Williamson Tobacco Corp., 509 U.S. 209 (1993)",
            "Sherman Act §2, 15 U.S.C. §2"
        ],
        burden_holder="Plaintiff",
        adversary_position="Prices above cost; no recoupment; competition is vigorous",
        counter_arguments=[
            "Prices are above cost",
            "Recoupment is impossible",
            "Market entry is easy"
        ],
        resolution_strategy="Apply Brooke Group test; assess cost and recoupment probability.",
        entity_scope="Dominant firms in relevant markets",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brooke Group Ltd. v. Brown & Williamson Tobacco Corp."
    ),
    DoctrineBlock(
        topic="FTC Act Section 5 - Unfair Methods of Competition",
        keywords=["FTC Act", "Section 5", "unfair methods", "competition", "antitrust"],
        conclusion_template="Section 5 prohibits unfair methods of competition, including conduct beyond Sherman and Clayton Acts.",
        reasoning_framework=(
            "Section 5 of the FTC Act prohibits unfair methods of competition. "
            "The FTC may challenge conduct that violates the spirit, but not the letter, of antitrust laws. "
            "Analysis includes: (1) nature of conduct; (2) harm to competition; (3) consumer welfare; (4) whether conduct is covered by other statutes. "
            "Defendants may argue conduct is lawful or procompetitive. "
            "Remedies include injunctions and cease-and-desist orders."
        ),
        key_factors=[
            "Nature of conduct",
            "Harm to competition",
            "Consumer welfare",
            "Overlap with other statutes",
            "FTC enforcement discretion"
        ],
        primary_authority=[
            "FTC Act §5, 15 U.S.C. §45",
            "FTC Policy Statement on Section 5 (2022)"
        ],
        burden_holder="FTC",
        adversary_position="Conduct is lawful; no harm to competition; procompetitive justification",
        counter_arguments=[
            "Conduct is covered by other statutes",
            "No harm to competition",
            "Procompetitive effects"
        ],
        resolution_strategy="Assess conduct and harm; apply FTC Policy Statement; consider remedies.",
        entity_scope="All entities subject to FTC jurisdiction",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FTC Policy Statement on Section 5"
    ),
    DoctrineBlock(
        topic="Joint Ventures - Rule of Reason and Integration Analysis",
        keywords=["joint venture", "rule of reason", "integration", "antitrust", "Section 1"],
        conclusion_template="Joint ventures are analyzed under the rule of reason; integration and procompetitive benefits may justify restraints.",
        reasoning_framework=(
            "Joint ventures involve collaboration among competitors. "
            "Analysis under the rule of reason considers: (1) degree of integration; (2) procompetitive benefits; (3) anticompetitive effects; (4) necessity of restraints. "
            "Plaintiff must show anticompetitive harm; defendant may argue integration and benefits. "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Degree of integration",
            "Procompetitive benefits",
            "Anticompetitive effects",
            "Necessity of restraints",
            "Market power"
        ],
        primary_authority=[
            "Texaco Inc. v. Dagher, 547 U.S. 1 (2006)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="Joint venture is integrated; procompetitive benefits; restraints are necessary",
        counter_arguments=[
            "Integration is genuine",
            "Restraints are necessary",
            "Benefits outweigh harm"
        ],
        resolution_strategy="Apply rule of reason; assess integration and necessity; weigh benefits and harm.",
        entity_scope="Competitors forming joint ventures",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texaco Inc. v. Dagher"
    ),
    DoctrineBlock(
        topic="Refusal to Deal - Aspen Skiing and Trinko Limits",
        keywords=["refusal to deal", "Aspen Skiing", "Trinko", "Section 2", "antitrust"],
        conclusion_template="Refusal to deal may violate Section 2 if it is a departure from prior course of dealing and lacks legitimate justification.",
        reasoning_framework=(
            "Section 2 does not generally require firms to deal with rivals. "
            "Aspen Skiing recognized liability where refusal was a departure from prior course of dealing and lacked legitimate justification. "
            "Trinko limited liability, emphasizing that refusal to deal is rarely actionable. "
            "Plaintiff must show prior dealing, abrupt refusal, and anticompetitive effect. "
            "Defendants may argue legitimate business reasons. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Prior course of dealing",
            "Abrupt refusal",
            "Lack of legitimate justification",
            "Anticompetitive effect",
            "Market power"
        ],
        primary_authority=[
            "Aspen Skiing Co. v. Aspen Highlands Skiing Corp., 472 U.S. 585 (1985)",
            "Verizon Communications Inc. v. Trinko, 540 U.S. 398 (2004)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Refusal was justified; no prior dealing; no anticompetitive effect",
        counter_arguments=[
            "Legitimate business reasons",
            "No prior course of dealing",
            "Refusal is lawful"
        ],
        resolution_strategy="Apply Aspen Skiing and Trinko standards; assess justification and effect.",
        entity_scope="Dominant firms in relevant markets",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Aspen Skiing Co. v. Aspen Highlands Skiing Corp."
    ),
    DoctrineBlock(
        topic="Hart-Scott-Rodino Act - Merger Notification Thresholds",
        keywords=["Hart-Scott-Rodino", "HSR", "merger notification", "thresholds", "premerger review"],
        conclusion_template="Mergers exceeding HSR thresholds must be notified to the FTC and DOJ for premerger review.",
        reasoning_framework=(
            "The Hart-Scott-Rodino Act requires parties to mergers and acquisitions above certain thresholds to file notification with the FTC and DOJ. "
            "Thresholds are adjusted annually. "
            "Failure to file may result in penalties. "
            "Defendants may argue transaction is below threshold or exempt. "
            "Remedies include fines and injunctions."
        ),
        key_factors=[
            "Transaction value",
            "Annual threshold adjustment",
            "Exemptions",
            "Filing requirements",
            "Penalties for non-compliance"
        ],
        primary_authority=[
            "Hart-Scott-Rodino Act, 15 U.S.C. §18a",
            "HSR Rules, 16 C.F.R. Part 801"
        ],
        burden_holder="Merging parties",
        adversary_position="Transaction is exempt; below threshold; filing not required",
        counter_arguments=[
            "Transaction value below threshold",
            "Exemption applies",
            "No filing required"
        ],
        resolution_strategy="Assess transaction value; apply exemptions; ensure compliance.",
        entity_scope="Merging parties",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hart-Scott-Rodino Act"
    ),
    DoctrineBlock(
        topic="2023 Merger Guidelines - Key Shifts and Presumptions",
        keywords=["2023 Merger Guidelines", "presumptions", "market concentration", "competitive effects", "thresholds"],
        conclusion_template="The 2023 Merger Guidelines establish new presumptions and thresholds for merger enforcement.",
        reasoning_framework=(
            "The 2023 Merger Guidelines update enforcement presumptions, market concentration thresholds, and competitive effects analysis. "
            "Key shifts include lower HHI thresholds, focus on potential competition, and expanded scrutiny of vertical and conglomerate mergers. "
            "Agencies presume illegality at lower concentration levels and emphasize effects on labor markets. "
            "Defendants may challenge presumptions or present efficiencies. "
            "Remedies include blocking, divestiture, or behavioral commitments."
        ),
        key_factors=[
            "HHI thresholds",
            "Presumptions of illegality",
            "Potential competition",
            "Labor market effects",
            "Efficiencies"
        ],
        primary_authority=[
            "2023 Merger Guidelines",
            "Clayton Act §7, 15 U.S.C. §18"
        ],
        burden_holder="Plaintiff (government or private)",
        adversary_position="Merger is procompetitive; efficiencies outweigh harm; presumptions do not apply",
        counter_arguments=[
            "Efficiencies benefit consumers",
            "Presumptions are rebutted",
            "Labor market effects are positive"
        ],
        resolution_strategy="Apply new guidelines; assess concentration and effects; weigh efficiencies.",
        entity_scope="Merging firms",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="2023 Merger Guidelines"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Vertical Restraints",
        keywords=["Sherman Act", "Section 1", "vertical restraints", "rule of reason", "distribution"],
        conclusion_template="Vertical restraints are analyzed under the rule of reason and may violate Section 1 if they unreasonably restrain trade.",
        reasoning_framework=(
            "Vertical restraints involve agreements between firms at different levels of the supply chain (e.g., manufacturer and retailer). "
            "Courts apply the rule of reason, assessing: (1) agreement; (2) anticompetitive effects; (3) procompetitive justifications. "
            "Plaintiff must show harm to competition; defendant may argue benefits. "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Nature of restraint",
            "Market definition",
            "Anticompetitive effects",
            "Procompetitive justifications",
            "Market power"
        ],
        primary_authority=[
            "Continental T.V., Inc. v. GTE Sylvania, Inc., 433 U.S. 36 (1977)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="Restraint is procompetitive; no anticompetitive effect; benefits outweigh harm",
        counter_arguments=[
            "Restraint enhances competition",
            "No market power",
            "No anticompetitive effect"
        ],
        resolution_strategy="Apply rule of reason; weigh effects and justifications.",
        entity_scope="Manufacturers and distributors",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Continental T.V., Inc. v. GTE Sylvania, Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 2 - Exclusive Access to Essential Facilities",
        keywords=["Sherman Act", "Section 2", "essential facilities", "exclusive access", "monopolization"],
        conclusion_template="Exclusive access to an essential facility may violate Section 2 if rivals are denied access and competition is harmed.",
        reasoning_framework=(
            "The essential facilities doctrine requires that a monopolist controlling a facility essential to competition must provide access to rivals on reasonable terms. "
            "Plaintiff must show: (1) control of essential facility; (2) denial of access; (3) inability to duplicate facility; (4) harm to competition. "
            "Defendants may argue facility is not essential or access is provided. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Control of facility",
            "Essentiality to competition",
            "Denial of access",
            "Ability to duplicate",
            "Harm to competition"
        ],
        primary_authority=[
            "United States v. Terminal Railroad Association, 224 U.S. 383 (1912)",
            "MCI Communications Corp. v. AT&T, 708 F.2d 1081 (7th Cir. 1983)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Facility is not essential; access is provided; duplication is possible",
        counter_arguments=[
            "Facility is not essential",
            "Access is available",
            "Duplication is feasible"
        ],
        resolution_strategy="Apply essential facilities test; assess access and harm.",
        entity_scope="Monopolists controlling facilities",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Terminal Railroad Association"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Group Boycotts",
        keywords=["Sherman Act", "Section 1", "group boycott", "concerted refusal", "per se illegal"],
        conclusion_template="Group boycotts may be per se illegal or analyzed under the rule of reason depending on context.",
        reasoning_framework=(
            "Group boycotts involve concerted refusals to deal with a target. "
            "Some boycotts are per se illegal (when competitors exclude a rival without legitimate justification); others are analyzed under the rule of reason. "
            "Plaintiff must show agreement and harm to competition. "
            "Defendants may argue procompetitive justification or lack of agreement. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among competitors",
            "Nature of boycott",
            "Harm to competition",
            "Procompetitive justification",
            "Market power"
        ],
        primary_authority=[
            "Klor's, Inc. v. Broadway-Hale Stores, Inc., 359 U.S. 207 (1959)",
            "Northwest Wholesale Stationers, Inc. v. Pacific Stationery & Printing Co., 472 U.S. 284 (1985)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Boycott is justified; no agreement; no harm to competition",
        counter_arguments=[
            "Procompetitive justification",
            "No agreement",
            "No harm to competition"
        ],
        resolution_strategy="Determine per se or rule of reason; assess agreement and harm.",
        entity_scope="Competitors and trade associations",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Klor's, Inc. v. Broadway-Hale Stores, Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Information Exchange",
        keywords=["Sherman Act", "Section 1", "information exchange", "competitors", "rule of reason"],
        conclusion_template="Information exchange among competitors may violate Section 1 if it facilitates collusion and harms competition.",
        reasoning_framework=(
            "Information exchange involves sharing price, output, or strategic data among competitors. "
            "Such conduct is analyzed under the rule of reason. "
            "Plaintiff must show exchange facilitates collusion or harms competition. "
            "Defendants may argue procompetitive benefits (efficiency, transparency). "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Nature of information exchanged",
            "Frequency and detail",
            "Facilitation of collusion",
            "Procompetitive benefits",
            "Market structure"
        ],
        primary_authority=[
            "United States v. United States Gypsum Co., 438 U.S. 422 (1978)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="Exchange is procompetitive; no facilitation of collusion; benefits outweigh harm",
        counter_arguments=[
            "Exchange enhances efficiency",
            "No facilitation of collusion",
            "Market structure prevents harm"
        ],
        resolution_strategy="Apply rule of reason; assess facilitation and benefits.",
        entity_scope="Competitors in the same market",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. United States Gypsum Co."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Non-Compete Agreements",
        keywords=["Sherman Act", "Section 1", "non-compete", "employment", "rule of reason"],
        conclusion_template="Non-compete agreements are analyzed under the rule of reason; unreasonable restraints may violate Section 1.",
        reasoning_framework=(
            "Non-compete agreements restrict employees or firms from competing after termination. "
            "Courts apply the rule of reason, assessing: (1) scope and duration; (2) necessity; (3) harm to competition. "
            "Plaintiff must show restraint is unreasonable and harms competition. "
            "Defendants may argue necessity and procompetitive benefits. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Scope and duration",
            "Necessity",
            "Harm to competition",
            "Procompetitive justification",
            "Market power"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "2023 Merger Guidelines"
        ],
        burden_holder="Plaintiff",
        adversary_position="Agreement is necessary; procompetitive; no harm to competition",
        counter_arguments=[
            "Agreement is necessary",
            "Procompetitive benefits",
            "No harm to competition"
        ],
        resolution_strategy="Apply rule of reason; assess scope, necessity, and harm.",
        entity_scope="Employers and employees",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="2023 Merger Guidelines"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Most-Favored-Nation Clauses",
        keywords=["Sherman Act", "Section 1", "most-favored-nation", "MFN", "rule of reason"],
        conclusion_template="MFN clauses are analyzed under the rule of reason; they may violate Section 1 if they facilitate collusion or harm competition.",
        reasoning_framework=(
            "Most-favored-nation (MFN) clauses require sellers to offer buyers the lowest price given to any customer. "
            "MFNs are analyzed under the rule of reason. "
            "Plaintiff must show MFN facilitates collusion or harms competition. "
            "Defendants may argue procompetitive benefits (price transparency, efficiency). "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Nature of MFN clause",
            "Facilitation of collusion",
            "Procompetitive benefits",
            "Market structure",
            "Market power"
        ],
        primary_authority=[
            "United States v. Apple Inc., 791 F.3d 290 (2d Cir. 2015)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="MFN is procompetitive; no facilitation of collusion; benefits outweigh harm",
        counter_arguments=[
            "MFN enhances transparency",
            "No facilitation of collusion",
            "Market structure prevents harm"
        ],
        resolution_strategy="Apply rule of reason; assess facilitation and benefits.",
        entity_scope="Buyers and sellers",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Apple Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Hub-and-Spoke Conspiracies",
        keywords=["Sherman Act", "Section 1", "hub-and-spoke", "conspiracy", "agreement"],
        conclusion_template="Hub-and-spoke conspiracies violate Section 1 if spokes are aware of and participate in a common scheme.",
        reasoning_framework=(
            "Hub-and-spoke conspiracies involve a central actor (hub) coordinating agreements with multiple parties (spokes), who are aware of and participate in a common scheme. "
            "Plaintiff must show agreement among spokes and hub, and awareness of common scheme. "
            "Defendants may argue independent conduct or lack of awareness. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Existence of hub",
            "Agreement among spokes",
            "Awareness of common scheme",
            "Harm to competition",
            "Market power"
        ],
        primary_authority=[
            "United States v. Apple Inc., 791 F.3d 290 (2d Cir. 2015)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="Conduct was independent; no common scheme; no harm to competition",
        counter_arguments=[
            "No awareness of scheme",
            "Conduct was independent",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of common scheme; apply Section 1 analysis.",
        entity_scope="Central actors and spokes",
        confidence=0.73,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Apple Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Restraints on Innovation",
        keywords=["Sherman Act", "Section 1", "innovation", "restraint", "rule of reason"],
        conclusion_template="Restraints on innovation are analyzed under the rule of reason; unreasonable restraints may violate Section 1.",
        reasoning_framework=(
            "Restraints on innovation include agreements limiting research, development, or adoption of new technologies. "
            "Courts apply the rule of reason, assessing: (1) nature and scope of restraint; (2) harm to competition; (3) procompetitive justification. "
            "Plaintiff must show restraint is unreasonable and harms competition. "
            "Defendants may argue necessity and procompetitive benefits. "
            "Remedies depend on findings."
        ),
        key_factors=[
            "Scope of restraint",
            "Harm to innovation",
            "Procompetitive justification",
            "Market power",
            "Market structure"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "FTC Act §5, 15 U.S.C. §45"
        ],
        burden_holder="Plaintiff",
        adversary_position="Restraint is necessary; procompetitive; no harm to innovation",
        counter_arguments=[
            "Restraint is necessary",
            "Procompetitive benefits",
            "No harm to innovation"
        ],
        resolution_strategy="Apply rule of reason; assess scope, necessity, and harm.",
        entity_scope="Firms in innovative markets",
        confidence=0.72,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FTC Act §5"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Restrict Output",
        keywords=["Sherman Act", "Section 1", "restrict output", "agreement", "per se illegal"],
        conclusion_template="Agreements among competitors to restrict output are per se violations of Section 1.",
        reasoning_framework=(
            "Output restriction agreements involve competitors agreeing to limit production or supply. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and restriction of output. "
            "Defendants may argue lack of agreement or legitimate joint venture. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among competitors",
            "Restriction of output",
            "Evidence of communication",
            "Market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "United States v. Socony-Vacuum Oil Co., 310 U.S. 150 (1940)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Competitors in the same market",
        confidence=0.71,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Socony-Vacuum Oil Co."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Fix Wages",
        keywords=["Sherman Act", "Section 1", "fix wages", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to fix wages are per se violations of Section 1.",
        reasoning_framework=(
            "Wage-fixing agreements involve employers agreeing to set wages or compensation levels. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and wage-fixing. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Fixing of wages",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "United States v. DaVita Inc., 2022 WL 266759 (D. Colo.)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.70,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. DaVita Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - No-Poach Agreements",
        keywords=["Sherman Act", "Section 1", "no-poach", "labor market", "per se illegal"],
        conclusion_template="No-poach agreements among employers are per se violations of Section 1.",
        reasoning_framework=(
            "No-poach agreements involve employers agreeing not to hire or solicit each other's employees. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and no-poach conduct. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "No-poach conduct",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "United States v. Jindal, 2021 WL 5578687 (E.D. Tex.)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.69,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Jindal"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Allocate Employees",
        keywords=["Sherman Act", "Section 1", "allocate employees", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to allocate employees are per se violations of Section 1.",
        reasoning_framework=(
            "Employee allocation agreements involve employers agreeing to divide employees or restrict hiring to certain groups. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and allocation conduct. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Allocation of employees",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "United States v. Jindal, 2021 WL 5578687 (E.D. Tex.)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.68,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Jindal"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Restrict Hiring",
        keywords=["Sherman Act", "Section 1", "restrict hiring", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to restrict hiring are per se violations of Section 1.",
        reasoning_framework=(
            "Hiring restriction agreements involve employers agreeing to limit hiring or recruitment. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and hiring restriction. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Restriction of hiring",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "United States v. DaVita Inc., 2022 WL 266759 (D. Colo.)",
            "Sherman Act §1, 15 U.S.C. §1"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.67,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. DaVita Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Limit Hours",
        keywords=["Sherman Act", "Section 1", "limit hours", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to limit employee hours are per se violations of Section 1.",
        reasoning_framework=(
            "Hour limitation agreements involve employers agreeing to restrict employee work hours. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and hour limitation. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Limitation of hours",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. Jindal, 2021 WL 5578687 (E.D. Tex.)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.66,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Jindal"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Limit Benefits",
        keywords=["Sherman Act", "Section 1", "limit benefits", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to limit employee benefits are per se violations of Section 1.",
        reasoning_framework=(
            "Benefit limitation agreements involve employers agreeing to restrict employee benefits. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and benefit limitation. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Limitation of benefits",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. DaVita Inc., 2022 WL 266759 (D. Colo.)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.65,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. DaVita Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Limit Training",
        keywords=["Sherman Act", "Section 1", "limit training", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to limit employee training are per se violations of Section 1.",
        reasoning_framework=(
            "Training limitation agreements involve employers agreeing to restrict employee training opportunities. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and training limitation. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Limitation of training",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. Jindal, 2021 WL 5578687 (E.D. Tex.)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.64,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Jindal"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Limit Advancement",
        keywords=["Sherman Act", "Section 1", "limit advancement", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to limit employee advancement are per se violations of Section 1.",
        reasoning_framework=(
            "Advancement limitation agreements involve employers agreeing to restrict employee promotion or advancement. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and advancement limitation. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Limitation of advancement",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. DaVita Inc., 2022 WL 266759 (D. Colo.)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.63,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. DaVita Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Limit Mobility",
        keywords=["Sherman Act", "Section 1", "limit mobility", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to limit employee mobility are per se violations of Section 1.",
        reasoning_framework=(
            "Mobility limitation agreements involve employers agreeing to restrict employee movement between firms. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and mobility limitation. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Limitation of mobility",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. Jindal, 2021 WL 5578687 (E.D. Tex.)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.62,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Jindal"
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Limit Recruitment",
        keywords=["Sherman Act", "Section 1", "limit recruitment", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to limit recruitment are per se violations of Section 1.",
        reasoning_framework=(
            "Recruitment limitation agreements involve employers agreeing to restrict recruitment efforts. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and recruitment limitation. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Limitation of recruitment",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. DaVita Inc., 2022 WL 266759 (D. Colo.)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.61,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. DaVita Inc."
    ),
    DoctrineBlock(
        topic="Sherman Act Section 1 - Agreements to Limit Compensation",
        keywords=["Sherman Act", "Section 1", "limit compensation", "labor market", "per se illegal"],
        conclusion_template="Agreements among employers to limit compensation are per se violations of Section 1.",
        reasoning_framework=(
            "Compensation limitation agreements involve employers agreeing to restrict employee compensation. "
            "Such conduct is per se illegal under Section 1. "
            "Plaintiff must show agreement and compensation limitation. "
            "Defendants may argue lack of agreement or legitimate collaboration. "
            "Remedies include injunctions and damages."
        ),
        key_factors=[
            "Agreement among employers",
            "Limitation of compensation",
            "Evidence of communication",
            "Labor market structure",
            "Absence of legitimate collaboration"
        ],
        primary_authority=[
            "Sherman Act §1, 15 U.S.C. §1",
            "United States v. Jindal, 2021 WL 5578687 (E.D. Tex.)"
        ],
        burden_holder="Plaintiff",
        adversary_position="No agreement; legitimate collaboration; no harm to competition",
        counter_arguments=[
            "No evidence of agreement",
            "Collaboration is legitimate",
            "No harm to competition"
        ],
        resolution_strategy="Assess evidence of agreement; apply per se rule.",
        entity_scope="Employers in labor markets",
        confidence=0.60,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Jindal"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords) or keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]