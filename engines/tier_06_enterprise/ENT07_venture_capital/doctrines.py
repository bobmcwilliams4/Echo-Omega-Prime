from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

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
        topic="Participating vs Non-Participating Preferred Stock",
        keywords=["preferred stock", "participating", "non-participating", "liquidation preference", "venture capital"],
        conclusion_template="The preferred stock is {participating/non-participating}, entitling holders to {participate/not participate} in common distributions after liquidation preference.",
        reasoning_framework="""
        1. Review the term sheet or charter provisions to identify whether the preferred stock is participating or non-participating.
        2. Participating preferred allows holders to first receive their liquidation preference, then participate pro-rata with common in remaining proceeds.
        3. Non-participating preferred only receives the greater of the liquidation preference or the as-converted common amount.
        4. Analyze the economic impact for both scenarios, considering company exit values and cap tables.
        5. Assess market norms for the company's stage and sector.
        6. Consider investor leverage and negotiation context.
        7. Evaluate the effect on founder and employee equity.
        8. Reference NVCA model documents and relevant case law.
        9. Confirm enforceability under Delaware law or applicable jurisdiction.
        10. Advise on negotiation points and possible trade-offs.
        """,
        key_factors=[
            "Charter and term sheet language",
            "Liquidation preference multiple",
            "Participation cap (if any)",
            "Company valuation and exit scenarios",
            "Market norms for stage/sector"
        ],
        primary_authority=[
            "Delaware General Corporation Law (DGCL)",
            "NVCA Model Legal Documents",
            "Relevant Delaware Chancery Court decisions"
        ],
        burden_holder="Investor (to negotiate for participation)",
        adversary_position="Founders/management may oppose participation due to dilution risk",
        counter_arguments=[
            "Participating preferred is uncommon in competitive markets",
            "Double-dipping is viewed as investor overreach",
            "Non-participating aligns interests with common holders"
        ],
        resolution_strategy="Negotiate for non-participating preferred with capped participation as compromise if necessary.",
        entity_scope="Delaware C-corporations issuing preferred stock",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="In re Trados Inc. S'holder Litig., 73 A.3d 17 (Del. Ch. 2013)"
    ),
    DoctrineBlock(
        topic="Weighted Average vs Full Ratchet Anti-Dilution",
        keywords=["anti-dilution", "weighted average", "full ratchet", "down round", "preferred stock"],
        conclusion_template="The anti-dilution protection is {weighted average/full ratchet}, adjusting conversion price upon dilutive issuances.",
        reasoning_framework="""
        1. Identify the anti-dilution provision in the charter or investment agreement.
        2. Full ratchet resets conversion price to the lowest price at which new shares are issued.
        3. Weighted average adjusts conversion price based on a formula reflecting the number and price of new shares.
        4. Calculate the impact of each method in hypothetical down round scenarios.
        5. Assess fairness to founders and prior investors.
        6. Consider market standards for the company's stage.
        7. Evaluate investor bargaining power.
        8. Review any carve-outs for employee equity or strategic issuances.
        9. Reference NVCA model language and Delaware law.
        10. Advise on negotiation leverage and possible alternatives.
        """,
        key_factors=[
            "Type of anti-dilution protection",
            "Formula used for weighted average",
            "Exclusions/carve-outs",
            "Investor leverage",
            "Market norms"
        ],
        primary_authority=[
            "DGCL Section 242",
            "NVCA Model Term Sheet",
            "ABA Model Stock Purchase Agreement"
        ],
        burden_holder="Investor (to negotiate for stronger protection)",
        adversary_position="Founders prefer weighted average to avoid punitive dilution",
        counter_arguments=[
            "Full ratchet is rare in competitive deals",
            "Weighted average is more balanced",
            "Carve-outs for employee equity are standard"
        ],
        resolution_strategy="Negotiate for broad-based weighted average anti-dilution with standard carve-outs.",
        entity_scope="Venture-backed corporations issuing preferred stock",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Benchmark Capital Partners IV, L.P. v. Vague, 2002 WL 1732423 (Del. Ch. 2002)"
    ),
    DoctrineBlock(
        topic="SAFE Post-Money Valuation Mechanics",
        keywords=["SAFE", "post-money", "valuation cap", "discount", "convertible security"],
        conclusion_template="The SAFE's post-money valuation cap determines conversion price based on the company's valuation immediately after the SAFE round.",
        reasoning_framework="""
        1. Review the SAFE agreement to confirm post-money or pre-money structure.
        2. Post-money SAFEs set the valuation cap based on the company's value after all SAFEs are issued, including the current round.
        3. Calculate conversion price: Valuation cap divided by company capitalization post-SAFE.
        4. Include all SAFEs, convertible notes, and option pool increases in the denominator.
        5. Assess impact on founder and employee dilution.
        6. Compare to pre-money SAFE mechanics.
        7. Consider Y Combinator's model SAFE language and guidance.
        8. Advise on disclosure and cap table modeling.
        9. Confirm compliance with securities laws.
        10. Address investor expectations and negotiation points.
        """,
        key_factors=[
            "SAFE agreement language",
            "Valuation cap and discount terms",
            "Company capitalization table",
            "Treatment of other convertible securities",
            "Option pool increases"
        ],
        primary_authority=[
            "Y Combinator SAFE Model Agreements",
            "SEC Regulation D",
            "DGCL Section 151"
        ],
        burden_holder="Company (to model and disclose post-money impact)",
        adversary_position="Investors may push for lower cap or larger discount",
        counter_arguments=[
            "Post-money SAFEs can cause unexpected dilution",
            "Pre-money SAFEs are less common in current market",
            "Clear modeling and disclosure mitigate disputes"
        ],
        resolution_strategy="Use detailed cap table modeling and clear SAFE documentation to align expectations.",
        entity_scope="Early-stage startups issuing SAFEs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="No controlling precedent; Y Combinator guidance is industry standard"
    ),
    DoctrineBlock(
        topic="409A Valuation Safe Harbors",
        keywords=["409A", "valuation", "safe harbor", "stock options", "fair market value"],
        conclusion_template="The company may rely on a 409A safe harbor if a qualified independent appraisal is obtained within 12 months prior to the grant date.",
        reasoning_framework="""
        1. IRC Section 409A requires that stock options be granted at or above fair market value to avoid adverse tax consequences.
        2. The most reliable safe harbor is a valuation by a qualified independent appraiser within 12 months of the grant.
        3. Alternative safe harbors include illiquid start-up valuation and binding formula valuation.
        4. Review the independence and credentials of the appraiser.
        5. Confirm the valuation methodology is reasonable and consistent with AICPA guidelines.
        6. Ensure the valuation date is within 12 months of the option grant.
        7. Document all relevant company information provided to the appraiser.
        8. Maintain records in case of IRS audit.
        9. Advise on timing of grants relative to valuation updates.
        10. Address impact of material events (e.g., financings, M&A) on valuation validity.
        """,
        key_factors=[
            "Appraiser independence",
            "Valuation methodology",
            "Timing of appraisal",
            "Material company events",
            "Documentation and recordkeeping"
        ],
        primary_authority=[
            "IRC Section 409A",
            "Treas. Reg. § 1.409A-1(b)(5)(iv)(B)",
            "AICPA Practice Aid: Valuation of Privately-Held Company Equity Securities"
        ],
        burden_holder="Company (to obtain and rely on safe harbor appraisal)",
        adversary_position="IRS may challenge valuation if not properly documented",
        counter_arguments=[
            "Failure to update valuation after material events voids safe harbor",
            "Non-independent appraisals are not reliable",
            "Option grants outside 12-month window are not protected"
        ],
        resolution_strategy="Engage a qualified independent appraiser annually and after material events.",
        entity_scope="Private companies granting stock options",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="IRC Section 409A; no significant case law"
    ),
    DoctrineBlock(
        topic="Section 83(b) Election Timing",
        keywords=["83(b) election", "IRS", "stock vesting", "founder equity", "tax"],
        conclusion_template="The 83(b) election must be filed within 30 days of the stock grant to avoid ordinary income recognition upon vesting.",
        reasoning_framework="""
        1. Section 83(b) allows taxpayers to elect to recognize income on the date of stock grant, rather than as it vests.
        2. The election must be filed with the IRS within 30 days of the grant date.
        3. Failure to timely file results in ordinary income recognition upon each vesting event.
        4. Review grant and vesting documents to confirm eligibility.
        5. Advise founders and employees of the strict deadline.
        6. Prepare and file the 83(b) election form, with proof of mailing.
        7. Provide a copy to the company and retain for records.
        8. Consider state tax implications.
        9. Evaluate risk of forfeiture and potential downside.
        10. Advise on best practices for documentation and reminders.
        """,
        key_factors=[
            "Grant date and vesting schedule",
            "Timely filing with IRS",
            "Risk of forfeiture",
            "Taxpayer's risk tolerance",
            "Company recordkeeping"
        ],
        primary_authority=[
            "IRC Section 83(b)",
            "Treas. Reg. § 1.83-2",
            "IRS Notice 2005-1"
        ],
        burden_holder="Taxpayer (founder/employee) to file election",
        adversary_position="IRS will deny late or incomplete elections",
        counter_arguments=[
            "Missed deadline is generally not waivable",
            "Election is irrevocable",
            "Downside risk if stock is forfeited"
        ],
        resolution_strategy="Implement automated reminders and provide template forms at grant.",
        entity_scope="Founders/employees receiving restricted stock",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Treas. Reg. § 1.83-2"
    ),
    DoctrineBlock(
        topic="QSBS Section 1202 Exclusion Requirements",
        keywords=["QSBS", "Section 1202", "capital gains", "exclusion", "holding period"],
        conclusion_template="If the stock meets Section 1202 requirements, up to 100% of gain may be excluded from federal tax upon sale after five years.",
        reasoning_framework="""
        1. Confirm the stock was issued by a qualified small business (C-corp, gross assets ≤ $50M).
        2. Verify the stock was acquired at original issuance for money, property, or services.
        3. Ensure the taxpayer is a non-corporate holder.
        4. Confirm the five-year holding period is satisfied.
        5. Assess whether the company engaged in qualified active business during the holding period.
        6. Exclude certain businesses (e.g., finance, professional services).
        7. Calculate the amount eligible for exclusion (up to $10M or 10x basis).
        8. Address aggregation and rollover rules.
        9. Review documentation and tax filings.
        10. Advise on planning for liquidity events and transfers.
        """,
        key_factors=[
            "Issuer qualification",
            "Original issuance",
            "Holding period",
            "Active business requirement",
            "Exclusion limits"
        ],
        primary_authority=[
            "IRC Section 1202",
            "IRS Notice 2018-18",
            "Treas. Reg. § 1.1202-2"
        ],
        burden_holder="Taxpayer (to prove eligibility)",
        adversary_position="IRS may challenge qualification or holding period",
        counter_arguments=[
            "Company may lose status due to asset growth or business change",
            "Transfers may break original issuance requirement",
            "Certain redemptions disqualify stock"
        ],
        resolution_strategy="Maintain detailed stock records and obtain company QSBS representations.",
        entity_scope="Qualified small business C-corporations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IRC Section 1202; no significant case law"
    ),
    DoctrineBlock(
        topic="Protective Provisions - Investor Veto Rights",
        keywords=["protective provisions", "veto rights", "investor consent", "charter amendment", "preferred stock"],
        conclusion_template="Protective provisions grant investors veto rights over specified corporate actions, requiring their consent.",
        reasoning_framework="""
        1. Review the charter and investor rights agreement for enumerated protective provisions.
        2. Common veto rights include amendments to charter/bylaws, issuance of new securities, mergers, asset sales, and dividend declarations.
        3. Confirm the class or series of preferred stock entitled to these rights.
        4. Assess the scope and breadth of the provisions.
        5. Evaluate the balance between investor protection and management flexibility.
        6. Consider market norms for the company's stage.
        7. Analyze the voting thresholds (majority, supermajority, or unanimous).
        8. Reference NVCA model documents and Delaware law.
        9. Advise on negotiation points and possible carve-outs.
        10. Confirm enforceability and board approval requirements.
        """,
        key_factors=[
            "Scope of protective provisions",
            "Voting thresholds",
            "Class/series entitled to rights",
            "Market norms",
            "Company stage"
        ],
        primary_authority=[
            "DGCL Section 242(b)(2)",
            "NVCA Model Charter",
            "ABA Model Stock Purchase Agreement"
        ],
        burden_holder="Investor (to negotiate for broad protections)",
        adversary_position="Founders may seek to limit veto scope",
        counter_arguments=[
            "Overly broad vetoes can paralyze company",
            "Narrow vetoes may not protect key investor interests",
            "Supermajority thresholds can be difficult to achieve"
        ],
        resolution_strategy="Negotiate for standard protective provisions with reasonable thresholds and clear definitions.",
        entity_scope="Venture-backed corporations with preferred stock",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="DGCL Section 242(b)(2)"
    ),
    DoctrineBlock(
        topic="Drag-Along and Tag-Along Rights",
        keywords=["drag-along", "tag-along", "co-sale", "liquidity event", "investor rights"],
        conclusion_template="Drag-along rights compel minority holders to participate in a sale; tag-along rights allow them to join a sale on the same terms.",
        reasoning_framework="""
        1. Review the stockholders' agreement for drag-along and tag-along provisions.
        2. Drag-along rights allow majority holders to force minority holders to sell on the same terms in a change of control.
        3. Tag-along rights allow minority holders to participate pro-rata in sales by major holders.
        4. Confirm triggering events and required approvals.
        5. Assess the scope of covered securities (common, preferred, options).
        6. Evaluate exceptions and carve-outs (e.g., IPOs, affiliate transfers).
        7. Consider fiduciary duties and fairness requirements.
        8. Reference NVCA and ABA model provisions.
        9. Advise on negotiation points and enforceability.
        10. Confirm compliance with state law and company charter.
        """,
        key_factors=[
            "Triggering events",
            "Approval thresholds",
            "Scope of covered securities",
            "Exceptions and carve-outs",
            "Fiduciary duties"
        ],
        primary_authority=[
            "NVCA Model Voting Agreement",
            "DGCL Section 251",
            "ABA Model Stockholders' Agreement"
        ],
        burden_holder="Majority holders (to enforce drag-along); minority holders (to invoke tag-along)",
        adversary_position="Minority holders may object to forced sale",
        counter_arguments=[
            "Drag-along must be exercised in good faith",
            "Tag-along can complicate sale negotiations",
            "Exceptions may undermine minority protection"
        ],
        resolution_strategy="Draft clear, balanced provisions with defined triggers and fair process.",
        entity_scope="Venture-backed corporations with multiple stockholder classes",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Trados Inc. S'holder Litig., 73 A.3d 17 (Del. Ch. 2013)"
    ),
    DoctrineBlock(
        topic="Board Composition and Observer Rights",
        keywords=["board composition", "observer rights", "corporate governance", "venture capital", "investor rights"],
        conclusion_template="The board is composed of {number} directors, with observer rights granted to specified investors as detailed in the agreement.",
        reasoning_framework="""
        1. Review the voting agreement and charter for board composition provisions.
        2. Identify the number of board seats allocated to common, preferred, and independent directors.
        3. Confirm the process for appointment and removal of directors.
        4. Observer rights allow designated investors to attend board meetings without voting power.
        5. Assess the scope of observer rights (access to materials, confidentiality obligations).
        6. Evaluate the balance of control among founders, investors, and independents.
        7. Consider market norms for company stage and sector.
        8. Reference NVCA model voting agreements.
        9. Advise on negotiation points and possible conflicts of interest.
        10. Confirm compliance with DGCL and company bylaws.
        """,
        key_factors=[
            "Board seat allocation",
            "Appointment/removal procedures",
            "Scope of observer rights",
            "Market norms",
            "Company stage"
        ],
        primary_authority=[
            "DGCL Section 141",
            "NVCA Model Voting Agreement",
            "Company bylaws"
        ],
        burden_holder="Company (to implement agreed board structure)",
        adversary_position="Investors may seek greater board control",
        counter_arguments=[
            "Too many investor seats can stifle founder autonomy",
            "Observer rights may raise confidentiality concerns",
            "Balanced boards foster better governance"
        ],
        resolution_strategy="Negotiate for balanced board composition and clear observer rights with confidentiality protections.",
        entity_scope="Venture-backed corporations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="DGCL Section 141"
    ),
    DoctrineBlock(
        topic="Registration Rights - Demand and Piggyback",
        keywords=["registration rights", "demand registration", "piggyback registration", "IPO", "liquidity"],
        conclusion_template="Investors are granted {demand/piggyback} registration rights, allowing them to require or join company-initiated public offerings.",
        reasoning_framework="""
        1. Review the registration rights agreement for demand and piggyback provisions.
        2. Demand rights allow investors to require the company to register shares for public sale.
        3. Piggyback rights allow investors to include their shares in company-initiated registrations.
        4. Confirm the number and frequency of demand rights.
        5. Assess blackout periods and underwriter cutbacks.
        6. Evaluate the impact on company IPO plans.
        7. Consider market standards for registration rights.
        8. Reference NVCA model agreements and SEC rules.
        9. Advise on negotiation points and timing.
        10. Confirm compliance with SEC and state blue sky laws.
        """,
        key_factors=[
            "Number and type of registration rights",
            "Blackout periods",
            "Underwriter cutbacks",
            "Market standards",
            "Company IPO plans"
        ],
        primary_authority=[
            "Securities Act of 1933, Section 5",
            "NVCA Model Registration Rights Agreement",
            "SEC Rule 415"
        ],
        burden_holder="Company (to facilitate registration)",
        adversary_position="Company may seek to limit frequency or scope",
        counter_arguments=[
            "Excessive demand rights can disrupt IPO process",
            "Piggyback rights may be subject to underwriter cutbacks",
            "Market standards favor limited demand rights"
        ],
        resolution_strategy="Negotiate for standard demand and piggyback rights with reasonable limitations.",
        entity_scope="Venture-backed corporations planning public offerings",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SEC Rule 415"
    ),
    DoctrineBlock(
        topic="Information Rights and Financial Reporting",
        keywords=["information rights", "financial reporting", "investor rights", "quarterly statements", "audited financials"],
        conclusion_template="Investors are entitled to receive {quarterly/annual} financial statements and other information as specified in the agreement.",
        reasoning_framework="""
        1. Review the investor rights agreement for information rights provisions.
        2. Common rights include quarterly unaudited and annual audited financial statements.
        3. Confirm timing and format of required disclosures.
        4. Assess additional rights to budgets, cap tables, and board materials.
        5. Evaluate confidentiality obligations and exceptions.
        6. Consider market norms for company stage and investor type.
        7. Reference NVCA model agreements.
        8. Advise on negotiation points and compliance.
        9. Confirm compatibility with company reporting systems.
        10. Address consequences of non-compliance.
        """,
        key_factors=[
            "Scope of information rights",
            "Reporting frequency",
            "Confidentiality obligations",
            "Company stage",
            "Investor type"
        ],
        primary_authority=[
            "NVCA Model Investor Rights Agreement",
            "DGCL Section 220",
            "Company bylaws"
        ],
        burden_holder="Company (to provide timely information)",
        adversary_position="Investors may seek broader or more frequent disclosures",
        counter_arguments=[
            "Overly broad rights can burden company",
            "Confidentiality is critical for sensitive information",
            "Market norms guide reasonable scope"
        ],
        resolution_strategy="Negotiate for standard information rights with confidentiality protections.",
        entity_scope="Venture-backed corporations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="DGCL Section 220"
    ),
    DoctrineBlock(
        topic="Vesting Schedules and Acceleration",
        keywords=["vesting", "acceleration", "founder equity", "employee stock", "change of control"],
        conclusion_template="Equity grants are subject to a {standard/custom} vesting schedule, with {single/double} trigger acceleration upon specified events.",
        reasoning_framework="""
        1. Review the equity grant agreements for vesting terms.
        2. Standard vesting is 4 years with a 1-year cliff.
        3. Single-trigger acceleration vests equity upon a change of control.
        4. Double-trigger acceleration requires both a change of control and termination without cause.
        5. Assess market norms for company stage and role (founder, executive, employee).
        6. Evaluate impact on retention and incentives.
        7. Consider investor concerns about over-acceleration.
        8. Reference NVCA and Y Combinator model documents.
        9. Advise on negotiation points and alternatives.
        10. Confirm compliance with plan documents and board approvals.
        """,
        key_factors=[
            "Vesting schedule and cliff",
            "Acceleration triggers",
            "Role of recipient",
            "Market norms",
            "Plan document terms"
        ],
        primary_authority=[
            "NVCA Model Stock Option Plan",
            "IRC Section 409A",
            "Company equity plan"
        ],
        burden_holder="Company (to administer vesting and acceleration)",
        adversary_position="Investors may oppose broad acceleration rights",
        counter_arguments=[
            "Overly generous acceleration can undermine retention",
            "Double-trigger is market standard for executives",
            "Founders may require protection in change of control"
        ],
        resolution_strategy="Adopt standard vesting with double-trigger acceleration for key personnel.",
        entity_scope="Startups and growth-stage companies",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="No controlling precedent; market practice governs"
    ),
    DoctrineBlock(
        topic="Right of First Refusal and Co-Sale Rights",
        keywords=["right of first refusal", "ROFR", "co-sale", "founder stock", "investor rights"],
        conclusion_template="The company and investors have a right of first refusal and co-sale rights on transfers of specified shares.",
        reasoning_framework="""
        1. Review the investor rights and stockholder agreements for ROFR and co-sale provisions.
        2. ROFR allows the company and/or investors to purchase shares before they are sold to third parties.
        3. Co-sale rights allow investors to participate pro-rata in sales by founders or other major holders.
        4. Confirm the order of exercise (company first, then investors).
        5. Assess scope of covered shares and exceptions (e.g., estate planning, affiliate transfers).
        6. Evaluate impact on founder liquidity and company control.
        7. Reference NVCA and ABA model agreements.
        8. Advise on negotiation points and market norms.
        9. Confirm compliance with securities laws and transfer restrictions.
        10. Address enforcement and notice procedures.
        """,
        key_factors=[
            "Order of exercise",
            "Scope of covered shares",
            "Exceptions and carve-outs",
            "Notice and enforcement procedures",
            "Market norms"
        ],
        primary_authority=[
            "NVCA Model Right of First Refusal and Co-Sale Agreement",
            "DGCL Section 202",
            "ABA Model Stockholders' Agreement"
        ],
        burden_holder="Company/investors (to exercise rights timely)",
        adversary_position="Founders may seek to limit ROFR/co-sale scope",
        counter_arguments=[
            "Overly broad rights can impede founder liquidity",
            "Exceptions for estate planning are standard",
            "ROFR/co-sale balance investor protection and founder interests"
        ],
        resolution_strategy="Negotiate for standard ROFR/co-sale rights with reasonable exceptions.",
        entity_scope="Venture-backed corporations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DGCL Section 202"
    ),
    DoctrineBlock(
        topic="Pay-to-Play Provisions",
        keywords=["pay-to-play", "down round", "preferred stock", "conversion", "investor participation"],
        conclusion_template="Pay-to-play provisions require investors to participate pro-rata in future financings to retain preferred rights.",
        reasoning_framework="""
        1. Review the charter and investor agreements for pay-to-play clauses.
        2. Pay-to-play provisions convert non-participating investors' preferred shares to common if they do not participate in future rounds.
        3. Confirm the scope (full or partial conversion) and triggering events.
        4. Assess impact on investor incentives and company fundraising.
        5. Evaluate market norms and investor leverage.
        6. Reference NVCA model documents.
        7. Advise on negotiation points and possible carve-outs.
        8. Confirm enforceability under state law.
        9. Address communication and notice procedures.
        10. Model impact on cap table and investor rights.
        """,
        key_factors=[
            "Scope of pay-to-play",
            "Triggering events",
            "Conversion mechanics",
            "Investor leverage",
            "Market norms"
        ],
        primary_authority=[
            "NVCA Model Charter",
            "DGCL Section 151",
            "ABA Model Stock Purchase Agreement"
        ],
        burden_holder="Investors (to participate in financings)",
        adversary_position="Investors may oppose harsh conversion terms",
        counter_arguments=[
            "Pay-to-play aligns incentives in down rounds",
            "Soft pay-to-play (partial conversion) is more common",
            "Harsh terms may deter future investment"
        ],
        resolution_strategy="Negotiate for soft pay-to-play with clear notice and conversion mechanics.",
        entity_scope="Venture-backed corporations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="DGCL Section 151"
    ),
    DoctrineBlock(
        topic="No-Shop and Exclusivity in Term Sheets",
        keywords=["no-shop", "exclusivity", "term sheet", "negotiation", "venture financing"],
        conclusion_template="The term sheet includes a {binding/non-binding} no-shop provision, restricting the company from soliciting competing offers for a specified period.",
        reasoning_framework="""
        1. Review the term sheet for no-shop or exclusivity clauses.
        2. No-shop provisions prohibit the company from soliciting or negotiating alternative offers during the exclusivity period.
        3. Confirm the duration and scope of the restriction.
        4. Assess enforceability under state law.
        5. Evaluate exceptions (e.g., fiduciary out).
        6. Consider investor need for deal certainty versus company flexibility.
        7. Reference NVCA model term sheets.
        8. Advise on negotiation points and possible modifications.
        9. Address remedies for breach (e.g., break-up fee, specific performance).
        10. Confirm clarity and mutual understanding of the provision.
        """,
        key_factors=[
            "Duration and scope",
            "Binding or non-binding nature",
            "Exceptions and carve-outs",
            "Remedies for breach",
            "Market norms"
        ],
        primary_authority=[
            "NVCA Model Term Sheet",
            "Delaware contract law",
            "ABA Model Term Sheet"
        ],
        burden_holder="Company (to comply with no-shop)",
        adversary_position="Company may seek shorter or non-binding exclusivity",
        counter_arguments=[
            "Overly long no-shop can hinder company flexibility",
            "Fiduciary out is standard for board protection",
            "Binding no-shops may be unenforceable in some jurisdictions"
        ],
        resolution_strategy="Negotiate for short, clearly defined no-shop with standard exceptions.",
        entity_scope="Venture financings and M&A transactions",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Delaware contract law"
    ),
    DoctrineBlock(
        topic="Convertible Note Terms - Interest and Conversion Mechanics",
        keywords=["convertible note", "interest", "conversion", "valuation cap", "discount"],
        conclusion_template="The convertible note accrues {simple/compound} interest and converts into equity at the next qualified financing per the agreed terms.",
        reasoning_framework="""
        1. Review the convertible note agreement for interest rate and accrual method.
        2. Confirm conversion triggers (qualified financing, maturity, sale).
        3. Assess conversion price mechanics (valuation cap, discount, or both).
        4. Calculate impact of accrued interest on conversion amount.
        5. Evaluate treatment of unqualified financings and maturity events.
        6. Consider investor and company preferences for conversion terms.
        7. Reference Y Combinator and NVCA model notes.
        8. Advise on negotiation points and market norms.
        9. Confirm compliance with securities laws and usury statutes.
        10. Address documentation and notice procedures.
        """,
        key_factors=[
            "Interest rate and accrual",
            "Conversion triggers",
            "Valuation cap and discount",
            "Treatment at maturity",
            "Market norms"
        ],
        primary_authority=[
            "Y Combinator Model Convertible Note",
            "NVCA Model Note",
            "State usury laws"
        ],
        burden_holder="Company (to honor conversion mechanics)",
        adversary_position="Investors may seek higher interest or better conversion terms",
        counter_arguments=[
            "High interest rates may trigger usury concerns",
            "Conversion at maturity can be contentious",
            "Market norms favor balanced terms"
        ],
        resolution_strategy="Negotiate for standard interest and conversion mechanics with clear triggers.",
        entity_scope="Startups issuing convertible notes",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="No controlling precedent; market practice governs"
    ),
    DoctrineBlock(
        topic="Accredited Investor and Reg D Exemptions",
        keywords=["accredited investor", "Regulation D", "private placement", "SEC", "exemption"],
        conclusion_template="The offering is exempt from registration under Regulation D if all purchasers are accredited investors and required filings are made.",
        reasoning_framework="""
        1. Review investor questionnaires and subscription documents for accredited investor status.
        2. Confirm compliance with Regulation D Rule 506(b) or 506(c).
        3. Assess whether general solicitation is used (506(c) requires verification).
        4. File Form D with the SEC within 15 days of first sale.
        5. Confirm compliance with state blue sky laws (notice filings).
        6. Advise on investor verification procedures.
        7. Reference SEC guidance and enforcement actions.
        8. Address consequences of non-compliance (rescission risk, penalties).
        9. Advise on best practices for recordkeeping.
        10. Confirm ongoing compliance for follow-on offerings.
        """,
        key_factors=[
            "Investor accreditation",
            "Type of Reg D exemption",
            "Form D filing",
            "State law compliance",
            "Solicitation methods"
        ],
        primary_authority=[
            "Securities Act of 1933, Regulation D",
            "SEC Rule 501-506",
            "SEC Form D"
        ],
        burden_holder="Company (to ensure exemption compliance)",
        adversary_position="Investors may challenge accredited status or disclosure adequacy",
        counter_arguments=[
            "Failure to verify status can void exemption",
            "Non-accredited investors trigger additional requirements",
            "Timely filings are critical"
        ],
        resolution_strategy="Implement robust investor verification and timely filings.",
        entity_scope="Private companies raising capital under Reg D",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="SEC Regulation D"
    ),
    DoctrineBlock(
        topic="Equity Compensation - ISOs vs NSOs",
        keywords=["equity compensation", "ISO", "NSO", "stock options", "tax"],
        conclusion_template="The company grants {ISOs/NSOs}, with differing tax treatment and eligibility requirements.",
        reasoning_framework="""
        1. Review the equity plan and grant agreements for option type.
        2. ISOs (Incentive Stock Options) offer favorable tax treatment but are limited to employees and subject to $100,000 annual vesting limit.
        3. NSOs (Non-Qualified Stock Options) can be granted to non-employees and have ordinary income tax upon exercise.
        4. Confirm compliance with IRC Sections 421, 422, and 409A.
        5. Assess eligibility of recipients.
        6. Evaluate impact on company and recipient tax reporting.
        7. Consider AMT implications for ISOs.
        8. Advise on plan design and grant practices.
        9. Reference IRS guidance and AICPA practice aids.
        10. Address state tax considerations.
        """,
        key_factors=[
            "Option type and eligibility",
            "Vesting and exercise terms",
            "Tax treatment",
            "Plan document compliance",
            "Recipient status"
        ],
        primary_authority=[
            "IRC Sections 421, 422, 409A",
            "AICPA Practice Aid",
            "IRS Publication 525"
        ],
        burden_holder="Company (to administer grants correctly)",
        adversary_position="Recipients may prefer ISOs for tax reasons",
        counter_arguments=[
            "ISOs are limited to employees",
            "NSOs are more flexible but less tax-advantaged",
            "AMT risk for ISOs"
        ],
        resolution_strategy="Grant ISOs to employees within limits; use NSOs for others.",
        entity_scope="Private companies granting stock options",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IRC Section 422"
    ),
    DoctrineBlock(
        topic="Liquidation Preference Stacking and Seniority",
        keywords=["liquidation preference", "stacking", "seniority", "preferred stock", "waterfall"],
        conclusion_template="Liquidation preferences are {stacked/pari passu}, with {senior/junior} preferred receiving proceeds before others.",
        reasoning_framework="""
        1. Review the charter for liquidation preference terms and seniority structure.
        2. Stacked preferences pay each series in order of seniority before junior series.
        3. Pari passu preferences share proceeds pro-rata among series.
        4. Confirm preference multiples and participation rights.
        5. Model exit scenarios to illustrate impact on each class.
        6. Assess market norms for stacking versus pari passu.
        7. Evaluate negotiation leverage and investor priorities.
        8. Reference NVCA model documents.
        9. Advise on trade-offs and founder dilution.
        10. Confirm enforceability under state law.
        """,
        key_factors=[
            "Preference structure (stacked/pari passu)",
            "Seniority of each series",
            "Preference multiples",
            "Participation rights",
            "Market norms"
        ],
        primary_authority=[
            "NVCA Model Charter",
            "DGCL Section 151",
            "ABA Model Stock Purchase Agreement"
        ],
        burden_holder="Investors (to negotiate for seniority)",
        adversary_position="Founders may seek pari passu to avoid overhang",
        counter_arguments=[
            "Stacked preferences can deter future investment",
            "Pari passu is more founder-friendly",
            "Market trends fluctuate"
        ],
        resolution_strategy="Negotiate for pari passu preferences where possible, or cap stacking.",
        entity_scope="Venture-backed corporations with multiple preferred series",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="DGCL Section 151"
    ),
    DoctrineBlock(
        topic="Pro-Rata Rights and Super Pro-Rata Allocation",
        keywords=["pro-rata rights", "super pro-rata", "follow-on investment", "preferred stock", "investor rights"],
        conclusion_template="Investors have the right to purchase their pro-rata (or greater) share of future financings, preserving ownership.",
        reasoning_framework="""
        1. Review the investor rights agreement for pro-rata and super pro-rata provisions.
        2. Pro-rata rights allow investors to maintain their percentage ownership in future rounds.
        3. Super pro-rata grants the right to purchase more than pro-rata, often for lead investors.
        4. Confirm calculation basis (as-converted basis, fully diluted).
        5. Assess impact on founder dilution and new investor allocation.
        6. Evaluate market norms and negotiation leverage.
        7. Reference NVCA model agreements.
        8. Advise on notice and exercise procedures.
        9. Address conflicts with new investor demands.
        10. Confirm enforceability and documentation.
        """,
        key_factors=[
            "Calculation of pro-rata share",
            "Scope of rights (pro-rata/super pro-rata)",
            "Notice and exercise procedures",
            "Market norms",
            "Impact on new investor allocation"
        ],
        primary_authority=[
            "NVCA Model Investor Rights Agreement",
            "DGCL Section 151",
            "ABA Model Stock Purchase Agreement"
        ],
        burden_holder="Investors (to exercise rights timely)",
        adversary_position="Founders may seek to limit super pro-rata to avoid over-concentration",
        counter_arguments=[
            "Super pro-rata can crowd out new investors",
            "Pro-rata is standard for all major investors",
            "Notice periods must be reasonable"
        ],
        resolution_strategy="Grant pro-rata to all major investors; limit super pro-rata to lead investors.",
        entity_scope="Venture-backed corporations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NVCA Model Investor Rights Agreement"
    ),
    DoctrineBlock(
        topic="Founder Stock Repurchase and Vesting Cliffs",
        keywords=["founder stock", "repurchase", "vesting cliff", "restricted stock", "company buyback"],
        conclusion_template="Founder stock is subject to company repurchase at cost if unvested shares are forfeited before the vesting cliff.",
        reasoning_framework="""
        1. Review the restricted stock purchase agreement for repurchase and vesting terms.
        2. Standard vesting is 4 years with a 1-year cliff.
        3. If a founder departs before the cliff, all unvested shares are subject to repurchase at cost.
        4. Confirm repurchase price and notice procedures.
        5. Assess impact on founder incentives and company control.
        6. Evaluate market norms for vesting and cliffs.
        7. Reference NVCA and Y Combinator model documents.
        8. Advise on negotiation points and possible exceptions.
        9. Address tax implications (83(b) election).
        10. Confirm enforceability under state law.
        """,
        key_factors=[
            "Vesting schedule and cliff",
            "Repurchase price",
            "Notice and exercise procedures",
            "Market norms",
            "Tax implications"
        ],
        primary_authority=[
            "NVCA Model Restricted Stock Purchase Agreement",
            "DGCL Section 202",
            "IRC Section 83(b)"
        ],
        burden_holder="Company (to exercise repurchase right timely)",
        adversary_position="Founders may seek shorter cliffs or higher repurchase price",
        counter_arguments=[
            "Cliffs align incentives and protect company",
            "Repurchase at cost is market standard",
            "Exceptions may be negotiated for key founders"
        ],
        resolution_strategy="Adopt standard 1-year cliff with repurchase at cost; negotiate exceptions as needed.",
        entity_scope="Startups issuing founder equity",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NVCA Model Restricted Stock Purchase Agreement"
    ),
    DoctrineBlock(
        topic="Management Rights Letters and ERISA/BHC Compliance",
        keywords=["management rights letter", "ERISA", "BHC", "venture capital operating company", "compliance"],
        conclusion_template="A management rights letter is provided to qualifying investors to ensure ERISA and BHC compliance.",
        reasoning_framework="""
        1. Review investor requests for management rights letters (MRLs).
        2. MRLs allow certain institutional investors to qualify as venture capital operating companies (VCOCs) under ERISA.
        3. Confirm the scope of rights granted (e.g., right to consult with management, inspect books).
        4. Assess whether the investor is subject to ERISA or BHC regulations.
        5. Reference NVCA model MRLs and DOL guidance.
        6. Advise on negotiation points and company obligations.
        7. Confirm compliance with ERISA plan asset regulations.
        8. Address confidentiality and competitive concerns.
        9. Advise on recordkeeping and delivery procedures.
        10. Confirm enforceability and ongoing compliance.
        """,
        key_factors=[
            "Investor status (ERISA/BHC)",
            "Scope of management rights",
            "Company compliance procedures",
            "Confidentiality obligations",
            "Market practice"
        ],
        primary_authority=[
            "ERISA Section 3(42)",
            "DOL Plan Asset Regulation (29 CFR 2510.3-101)",
            "NVCA Model Management Rights Letter"
        ],
        burden_holder="Company (to provide MRL as requested)",
        adversary_position="Investors may seek broader rights than necessary",
        counter_arguments=[
            "Overly broad rights can burden company",
            "MRLs are standard for VCOC compliance",
            "Confidentiality is critical"
        ],
        resolution_strategy="Provide standard MRL upon request; limit scope to required rights.",
        entity_scope="Venture-backed companies with institutional investors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="DOL Plan Asset Regulation"
    ),
    DoctrineBlock(
        topic="Founder Restricted Covenants - Non-Compete and IP Assignment",
        keywords=["founder covenants", "non-compete", "IP assignment", "restrictive covenant", "employment agreement"],
        conclusion_template="Founders are subject to non-compete and IP assignment covenants as a condition of equity grants and employment.",
        reasoning_framework="""
        1. Review founder employment and equity agreements for restrictive covenants.
        2. Non-compete clauses restrict founders from engaging in competing businesses for a defined period and geography.
        3. IP assignment ensures company ownership of inventions and works created during employment.
        4. Confirm enforceability under state law (e.g., California limits non-competes).
        5. Assess scope, duration, and geographic reach of covenants.
        6. Reference NVCA and Y Combinator model agreements.
        7. Advise on negotiation points and possible exceptions.
        8. Address consequences of breach (forfeiture, injunctive relief).
        9. Confirm compliance with applicable employment laws.
        10. Advise on best practices for onboarding and documentation.
        """,
        key_factors=[
            "Scope and duration of non-compete",
            "IP assignment language",
            "State law enforceability",
            "Consequences of breach",
            "Market norms"
        ],
        primary_authority=[
            "State employment law (e.g., Cal. Bus. & Prof. Code § 16600)",
            "NVCA Model Employment Agreement",
            "Y Combinator Founder Agreement"
        ],
        burden_holder="Company (to draft and enforce covenants)",
        adversary_position="Founders may resist broad non-competes",
        counter_arguments=[
            "Non-competes are unenforceable in some states",
            "IP assignment is essential for company protection",
            "Reasonable scope is key to enforceability"
        ],
        resolution_strategy="Adopt enforceable, narrowly tailored covenants consistent with state law.",
        entity_scope="Startups and growth-stage companies",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Cal. Bus. & Prof. Code § 16600"
    ),
    # Additional doctrine blocks for comprehensive coverage (examples below)
    DoctrineBlock(
        topic="Option Pool Sizing and Pre-Money vs Post-Money Impact",
        keywords=["option pool", "pre-money", "post-money", "dilution", "cap table"],
        conclusion_template="The option pool is {sized pre/post-money}, impacting founder and investor dilution accordingly.",
        reasoning_framework="""
        1. Review the term sheet for option pool sizing mechanics.
        2. Pre-money pools increase effective dilution for founders.
        3. Post-money pools allocate dilution between founders and new investors.
        4. Model cap table scenarios to illustrate impact.
        5. Assess market norms for pool size by stage.
        6. Advise on negotiation points and alternatives.
        7. Reference NVCA and Y Combinator model term sheets.
        8. Confirm clarity in documentation.
        9. Address timing of pool increases.
        10. Advise on best practices for transparency.
        """,
        key_factors=[
            "Option pool size",
            "Pre-money vs post-money calculation",
            "Cap table modeling",
            "Market norms",
            "Stage of company"
        ],
        primary_authority=[
            "NVCA Model Term Sheet",
            "Y Combinator SAFE Guidance"
        ],
        burden_holder="Company (to disclose and model pool impact)",
        adversary_position="Investors may push for larger pre-money pools",
        counter_arguments=[
            "Large pre-money pools unfairly dilute founders",
            "Post-money pools are more transparent",
            "Clear modeling prevents disputes"
        ],
        resolution_strategy="Negotiate for post-money pool sizing and detailed cap table disclosure.",
        entity_scope="Startups raising venture capital",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NVCA Model Term Sheet"
    ),
    DoctrineBlock(
        topic="Major Investor Definition and Rights",
        keywords=["major investor", "definition", "rights", "threshold", "investor rights agreement"],
        conclusion_template="A major investor is defined as one holding at least {threshold} shares, entitling them to specified enhanced rights.",
        reasoning_framework="""
        1. Review the investor rights agreement for the definition of major investor.
        2. Common thresholds include a minimum number of shares or investment amount.
        3. Major investors often receive enhanced rights (e.g., information, pro-rata, board observer).
        4. Assess impact on investor relations and company governance.
        5. Evaluate market norms for thresholds and rights.
        6. Advise on negotiation points and possible exceptions.
        7. Reference NVCA model agreements.
        8. Confirm clarity and enforceability of definitions.
        9. Address changes in status due to transfers or dilution.
        10. Advise on best practices for documentation.
        """,
        key_factors=[
            "Threshold for major investor status",
            "Enhanced rights granted",
            "Market norms",
            "Impact of transfers/dilution",
            "Clarity of definitions"
        ],
        primary_authority=[
            "NVCA Model Investor Rights Agreement",
            "ABA Model Stock Purchase Agreement"
        ],
        burden_holder="Company (to administer major investor rights)",
        adversary_position="Investors may seek lower thresholds",
        counter_arguments=[
            "Low thresholds can dilute the value of major investor rights",
            "Clear definitions prevent disputes",
            "Market norms guide threshold setting"
        ],
        resolution_strategy="Set thresholds consistent with market practice and company needs.",
        entity_scope="Venture-backed companies",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="NVCA Model Investor Rights Agreement"
    ),
    DoctrineBlock(
        topic="Founder Reverse Vesting and Acceleration",
        keywords=["reverse vesting", "founder equity", "acceleration", "restricted stock", "change of control"],
        conclusion_template="Founder shares are subject to reverse vesting with {single/double} trigger acceleration upon specified events.",
        reasoning_framework="""
        1. Review founder stock agreements for reverse vesting terms.
        2. Reverse vesting subjects founder shares to repurchase if the founder leaves before vesting.
        3. Confirm vesting schedule and cliff.
        4. Assess acceleration triggers (change of control, termination).
        5. Evaluate market norms for acceleration.
        6. Advise on negotiation points and possible exceptions.
        7. Reference NVCA and Y Combinator model documents.
        8. Address tax implications (83(b) election).
        9. Confirm enforceability under state law.
        10. Advise on best practices for founder retention.
        """,
        key_factors=[
            "Vesting schedule and cliff",
            "Acceleration triggers",
            "Repurchase price",
            "Market norms",
            "Tax implications"
        ],
        primary_authority=[
            "NVCA Model Restricted Stock Purchase Agreement",
            "IRC Section 83(b)"
        ],
        burden_holder="Company (to administer reverse vesting)",
        adversary_position="Founders may seek broader acceleration",
        counter_arguments=[
            "Overly broad acceleration undermines retention",
            "Double-trigger is market standard",
            "Exceptions may be negotiated for key founders"
        ],
        resolution_strategy="Adopt standard reverse vesting with double-trigger acceleration for founders.",
        entity_scope="Startups issuing founder equity",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NVCA Model Restricted Stock Purchase Agreement"
    ),
    DoctrineBlock(
        topic="Employee Option Exercise Windows Post-Termination",
        keywords=["option exercise window", "employee stock options", "termination", "ISO", "NSO"],
        conclusion_template="Departing employees have {90-day/custom} window to exercise vested options post-termination, per plan terms.",
        reasoning_framework="""
        1. Review the equity plan and grant agreements for post-termination exercise window.
        2. Standard window for ISOs is 90 days to preserve ISO status.
        3. NSOs may allow longer exercise periods, subject to plan limits.
        4. Assess impact on employee retention and incentives.
        5. Evaluate market norms and company stage.
        6. Advise on negotiation points and possible exceptions.
        7. Reference IRS and AICPA guidance.
        8. Address tax implications of extended windows.
        9. Confirm compliance with plan documents and board approvals.
        10. Advise on best practices for communication and documentation.
        """,
        key_factors=[
            "Type of option (ISO/NSO)",
            "Exercise window duration",
            "Plan document terms",
            "Tax implications",
            "Market norms"
        ],
        primary_authority=[
            "IRC Section 422",
            "AICPA Practice Aid",
            "Company equity plan"
        ],
        burden_holder="Company (to administer exercise windows)",
        adversary_position="Employees may seek longer windows",
        counter_arguments=[
            "Extended windows may forfeit ISO status",
            "Short windows can disadvantage employees",
            "Market practice is evolving"
        ],
        resolution_strategy="Adopt standard 90-day window for ISOs; consider longer windows for NSOs with clear disclosure.",
        entity_scope="Private companies granting stock options",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IRC Section 422"
    ),
    DoctrineBlock(
        topic="Founder Reinvestment and Participation in Follow-On Rounds",
        keywords=["founder reinvestment", "follow-on round", "participation rights", "founder equity"],
        conclusion_template="Founders may participate in follow-on rounds, subject to board approval and pro-rata allocation.",
        reasoning_framework="""
        1. Review financing agreements for founder participation rights.
        2. Confirm any restrictions or board approval requirements.
        3. Assess impact on cap table and investor relations.
        4. Evaluate market norms for founder reinvestment.
        5. Advise on negotiation points and possible exceptions.
        6. Reference NVCA and ABA model documents.
        7. Address conflicts of interest and disclosure requirements.
        8. Confirm compliance with securities laws.
        9. Advise on best practices for transparency.
        10. Document all approvals and allocations.
        """,
        key_factors=[
            "Board approval requirements",
            "Pro-rata allocation",
            "Market norms",
            "Disclosure and conflicts",
            "Cap table impact"
        ],
        primary_authority=[
            "NVCA Model Stock Purchase Agreement",
            "DGCL Section 144"
        ],
        burden_holder="Founders (to seek approval and comply with allocation)",
        adversary_position="Investors may oppose founder over-concentration",
        counter_arguments=[
            "Founder participation can signal confidence",
            "Over-concentration may deter new investors",
            "Board approval mitigates conflicts"
        ],
        resolution_strategy="Allow founder participation subject to board approval and pro-rata limits.",
        entity_scope="Venture-backed companies",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="DGCL Section 144"
    ),
    DoctrineBlock(
        topic="Down Round Financing and Cram-Down Terms",
        keywords=["down round", "cram-down", "financing", "preferred stock", "anti-dilution"],
        conclusion_template="Down round financings may include cram-down terms, such as forced conversion or punitive anti-dilution adjustments.",
        reasoning_framework="""
        1. Review the financing documents for cram-down provisions.
        2. Cram-downs may force non-participating investors to convert preferred to common or accept punitive anti-dilution.
        3. Confirm triggers and mechanics of cram-down.
        4. Assess impact on investor relations and future fundraising.
        5. Evaluate market norms and negotiation leverage.
        6. Advise on alternatives and possible mitigations.
        7. Reference NVCA and ABA model documents.
        8. Address disclosure and fairness considerations.
        9. Confirm enforceability under state law.
        10. Advise on best practices for communication and documentation.
        """,
        key_factors=[
            "Triggers and mechanics",
            "Anti-dilution adjustments",
            "Investor participation",
            "Market norms",
            "Disclosure and fairness"
        ],
        primary_authority=[
            "NVCA Model Charter",
            "DGCL Section 151"
        ],
        burden_holder="Company (to implement cram-down terms)",
        adversary_position="Investors may resist punitive terms",
        counter_arguments=[
            "Cram-downs can damage investor relations",
            "Disclosure and fairness are critical",
            "Alternatives may be preferable"
        ],
        resolution_strategy="Use cram-downs only as last resort with full disclosure and fairness review.",
        entity_scope="Venture-backed companies in distress",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="DGCL Section 151"
    ),
    DoctrineBlock(
        topic="Side Letters and Most Favored Nation (MFN) Clauses",
        keywords=["side letter", "MFN", "most favored nation", "investor rights", "venture capital"],
        conclusion_template="Side letters may include MFN clauses, entitling investors to terms as favorable as those granted to others.",
        reasoning_framework="""
        1. Review all side letters and main agreements for MFN clauses.
        2. MFN entitles the investor to receive any more favorable terms granted to subsequent investors.
        3. Confirm scope and duration of MFN.
        4. Assess impact on company flexibility and future negotiations.
        5. Evaluate market norms and negotiation leverage.
        6. Advise on possible carve-outs and limitations.
        7. Reference NVCA and ABA model documents.
        8. Address disclosure and fairness considerations.
        9. Confirm enforceability under contract law.
        10. Advise on best practices for recordkeeping and disclosure.
        """,
        key_factors=[
            "Scope and duration of MFN",
            "Disclosure and recordkeeping",
            "Impact on future negotiations",
            "Market norms",
            "Carve-outs and limitations"
        ],
        primary_authority=[
            "NVCA Model Side Letter",
            "Delaware contract law"
        ],
        burden_holder="Company (to disclose and administer MFN)",
        adversary_position="Investors may seek broad MFN rights",
        counter_arguments=[
            "Broad MFN can complicate future financings",
            "Carve-outs are standard",
            "Disclosure is critical"
        ],
        resolution_strategy="Limit MFN scope and duration; maintain comprehensive disclosure.",
        entity_scope="Venture-backed companies",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Delaware contract law"
    ),
    DoctrineBlock(
        topic="Waiver and Amendment of Investor Rights Agreements",
        keywords=["waiver", "amendment", "investor rights agreement", "majority consent", "venture capital"],
        conclusion_template="Investor rights agreements may be amended or waived with the consent of specified majority of holders.",
        reasoning_framework="""
        1. Review the investor rights agreement for amendment and waiver provisions.
        2. Confirm required consent threshold (e.g., majority, supermajority).
        3. Assess impact on minority investors.
        4. Evaluate market norms for amendment procedures.
        5. Advise on negotiation points and possible exceptions.
        6. Reference NVCA and ABA model agreements.
        7. Address notice and documentation requirements.
        8. Confirm enforceability under contract law.
        9. Advise on best practices for transparency and fairness.
        10. Document all amendments and waivers.
        """,
        key_factors=[
            "Consent threshold",
            "Notice and documentation",
            "Impact on minority holders",
            "Market norms",
            "Clarity of amendment procedures"
        ],
        primary_authority=[
            "NVCA Model Investor Rights Agreement",
            "Delaware contract law"
        ],
        burden_holder="Company (to obtain required consents)",
        adversary_position="Minority investors may oppose amendments",
        counter_arguments=[
            "Majority consent is standard",
            "Notice and transparency mitigate disputes",
            "Carve-outs may be negotiated"
        ],
        resolution_strategy="Require majority consent with notice to all holders; document all changes.",
        entity_scope="Venture-backed companies",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NVCA Model Investor Rights Agreement"
    ),
    DoctrineBlock(
        topic="Founder Departure and Bad Leaver Provisions",
        keywords=["founder departure", "bad leaver", "repurchase", "forfeiture", "venture capital"],
        conclusion_template="Bad leaver provisions allow the company to repurchase founder shares at cost or nominal value upon certain departures.",
        reasoning_framework="""
        1. Review founder agreements for bad leaver definitions and triggers.
        2. Bad leaver typically includes termination for cause, voluntary resignation, or breach of covenants.
        3. Confirm repurchase price and notice procedures.
        4. Assess impact on founder incentives and company control.
        5. Evaluate market norms and negotiation leverage.
        6. Advise on possible exceptions and carve-outs.
        7. Reference NVCA and Y Combinator model documents.
        8. Address enforceability under state law.
        9. Advise on best practices for communication and documentation.
        10. Document all departures and repurchases.
        """,
        key_factors=[
            "Definition of bad leaver",
            "Repurchase price",
            "Notice and documentation",
            "Market norms",
            "Impact on founder incentives"
        ],
        primary_authority=[
            "NVCA Model Restricted Stock Purchase Agreement",
            "DGCL Section 202"
        ],
        burden_holder="Company (to enforce bad leaver provisions)",
        adversary_position="Founders may seek narrower definitions",
        counter_arguments=[
            "Broad definitions can deter founder commitment",
            "Clear definitions prevent disputes",
            "Market norms guide scope"
        ],
        resolution_strategy="Adopt clear, market-standard definitions and procedures for bad leaver provisions.",
        entity_scope="Startups issuing founder equity",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NVCA Model Restricted Stock Purchase Agreement"
    ),
    DoctrineBlock(
        topic="Preferred Stock Dividends - Cumulative vs Non-Cumulative",
        keywords=["preferred stock", "dividends", "cumulative", "non-cumulative", "venture capital"],
        conclusion_template="Preferred stock may have {cumulative/non-cumulative} dividends, accruing annually or only when declared.",
        reasoning_framework="""
        1. Review the charter for preferred stock dividend provisions.
        2. Cumulative dividends accrue annually and are payable on liquidation or redemption.
        3. Non-cumulative dividends are paid only if and when declared by the board.
        4. Confirm dividend rate and payment mechanics.
        5. Assess impact on company cash flow and cap table.
        6. Evaluate market norms for cumulative versus non-cumulative.
        7. Advise on negotiation points and possible alternatives.
        8. Reference NVCA model documents.
        9. Address tax implications for company and holders.
        10. Confirm enforceability under state law.
        """,
        key_factors=[
            "Dividend type (cumulative/non-cumulative)",
            "Dividend rate",
            "Payment mechanics",
            "Market norms",
            "Tax implications"
        ],
        primary_authority=[
            "NVCA Model Charter",
            "DGCL Section 151"
        ],
        burden_holder="Company (to pay or accrue dividends as required)",
        adversary_position="Investors may seek cumulative dividends for downside protection",
        counter_arguments=[
            "Cumulative dividends are rare in early-stage deals",
            "Non-cumulative is more founder-friendly",
            "Market trends vary by stage"
        ],
        resolution_strategy="Negotiate for non-cumulative dividends in early rounds; consider cumulative only in later-stage or distressed deals.",
        entity_scope="Venture-backed companies issuing preferred stock",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NVCA Model Charter"
    ),
    DoctrineBlock(
        topic="Protective Provisions - Series-Specific vs Class-Wide",
        keywords=["protective provisions", "series-specific", "class-wide", "preferred stock", "investor rights"],
        conclusion_template="Protective provisions may apply to a specific series or all preferred stockholders, affecting voting dynamics.",
        reasoning_framework="""
        1. Review the charter and investor agreements for the scope of protective provisions.
        2. Series-specific provisions require consent of a particular series; class-wide require all preferred holders.
        3. Assess impact on company flexibility and investor protection.
        4. Evaluate market norms for series-specific versus class-wide.
        5. Advise on negotiation points and possible compromises.
        6. Reference NVCA model documents.
        7. Address conflicts between series and classes.
        8. Confirm enforceability under state law.
        9. Advise on best practices for clarity and documentation.
        10. Document all consents and approvals.
        """,
        key_factors=[
            "Scope of protective provisions",
            "Voting thresholds",
            "Series vs class dynamics",
            "Market norms",
            "Clarity of documentation"
        ],
        primary_authority=[
            "NVCA Model Charter",
            "DGCL Section 242(b)(2)"
        ],
        burden_holder="Company (to obtain required consents)",
        adversary_position="Investors may seek series-specific vetoes for greater protection",
        counter_arguments=[
            "Class-wide provisions are simpler to administer",
            "Series-specific can complicate governance",
            "Market norms vary by stage"
        ],
        resolution_strategy="Balance series-specific and class-wide provisions based on investor mix and company needs.",
        entity_scope="Venture-backed companies with multiple preferred series",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="NVCA Model Charter"
    ),
    DoctrineBlock(
        topic="Founder IP Assignment and Prior Inventions Disclosure",
        keywords=["founder IP assignment", "prior inventions", "disclosure", "employment agreement", "venture capital"],
        conclusion_template="Founders must assign all company-related IP and disclose prior inventions as a condition of equity grants.",
        reasoning_framework="""
        1. Review founder employment and equity agreements for IP assignment and disclosure provisions.
        2. IP assignment ensures company ownership of inventions created during employment.
        3. Prior inventions disclosure protects founders' pre-existing IP.
        4. Confirm scope and exceptions for prior inventions.
        5. Assess enforceability under state law.
        6. Advise on negotiation points and possible carve-outs.
        7. Reference NVCA and Y Combinator model agreements.
        8. Address consequences of failure to disclose.
        9. Advise on best practices for onboarding and documentation.
        10. Document all disclosures and assignments.
        """,
        key_factors=[
            "Scope of IP assignment",
            "Disclosure of prior inventions",
            "Exceptions and carve-outs",
            "Market norms",
            "Documentation and recordkeeping"
        ],
        primary_authority=[
            "NVCA Model Employment Agreement",
            "Y Combinator Founder Agreement"
        ],
        burden_holder="Company (to obtain assignments and disclosures)",
        adversary_position="Founders may seek broader exceptions",
        counter_arguments=[
            "Broad assignment is essential for company protection",
            "Clear disclosure prevents disputes",
            "Exceptions may be negotiated for pre-existing IP"
        ],
        resolution_strategy="Require comprehensive assignment and disclosure with reasonable carve-outs.",
        entity_scope="Startups and growth-stage companies",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NVCA Model Employment Agreement"
    ),
    DoctrineBlock(
        topic="Preferred Stock Redemption Rights",
        keywords=["preferred stock", "redemption", "redemption rights", "venture capital", "investor exit"],
        conclusion_template="Preferred stock may include redemption rights, allowing investors to require company repurchase after a specified period.",
        reasoning_framework="""
        1. Review the charter for redemption rights provisions.
        2. Redemption allows investors to require the company to repurchase preferred shares after a holding period (typically 5-7 years).
        3. Confirm redemption price, timing, and payment mechanics.
        4. Assess impact on company cash flow and operations.
        5. Evaluate market norms for redemption rights.
        6. Advise on negotiation points and possible alternatives.
        7. Reference NVCA model documents.
        8. Address enforceability under state law and solvency requirements.
        9. Advise on best practices for disclosure and planning.
        10. Document all redemption notices and payments.
        """,
        key_factors=[
            "Redemption period and price",
            "Payment mechanics",
            "Company solvency",
            "Market norms",
            "Disclosure and planning"
        ],
        primary_authority=[
            "NVCA Model Charter",
            "DGCL Section 160"
        ],
        burden_holder="Company (to honor redemption rights)",
        adversary_position="Investors may seek earlier or mandatory redemption",
        counter_arguments=[
            "Early redemption can strain company resources",
            "Mandatory redemption is rare",
            "Solvency requirements limit redemption"
        ],
        resolution_strategy="Negotiate for optional redemption after standard holding period, subject to solvency.",
        entity_scope="Venture-backed companies issuing preferred stock",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="DGCL Section 160"
    ),
    DoctrineBlock(
        topic="Founder Non-Solicit and Confidentiality Covenants",
        keywords=["founder non-solicit", "confidentiality", "restrictive covenant", "venture capital", "employment agreement"],
        conclusion_template="Founders are subject to non-solicit and confidentiality covenants as a condition of employment and equity grants.",
        reasoning_framework="""
        1. Review founder employment and equity agreements for non-solicit and confidentiality provisions.
        2. Non-solicit restricts founders from soliciting employees or customers post-departure.
        3. Confidentiality protects company trade secrets and sensitive information.
        4. Confirm scope, duration, and enforceability under state law.
        5. Assess impact on founder mobility and company protection.
        6. Advise on negotiation points and possible exceptions.
        7. Reference NVCA and Y Combinator model agreements.
        8. Address consequences of breach (injunctive relief, damages).
        9. Advise on best practices for onboarding and documentation.
        10. Document all covenants and exceptions.
        """,
        key_factors=[
            "Scope and duration of non-solicit",
            "Confidentiality obligations",
            "State law enforceability",
            "Consequences of breach",
            "Market norms"
        ],
        primary_authority=[
            "NVCA Model Employment Agreement",
            "State employment law"
        ],
        burden_holder="Company (to draft and enforce covenants)",
        adversary_position="Founders may seek narrower scope or shorter duration",
        counter_arguments=[
            "Non-solicit is more enforceable than non-compete",
            "Confidentiality is essential for company protection",
            "Reasonable scope is key to enforceability"
        ],
        resolution_strategy="Adopt enforceable, narrowly tailored covenants consistent with state law.",
        entity_scope="Startups and growth-stage companies",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NVCA Model Employment Agreement"
    ),
    DoctrineBlock(
        topic="Change of Control Definitions and Triggers",
        keywords=["change of control", "definition", "trigger", "acceleration", "venture capital"],
        conclusion_template="Change of control is defined as {merger/sale/IPO}, triggering specified rights and obligations.",
        reasoning_framework="""
        1. Review all relevant agreements for change of control definitions.
        2. Common triggers include merger, sale of substantially all assets, or IPO.
        3. Confirm impact on vesting, acceleration, and investor rights.
        4. Assess clarity and consistency across documents.
        5. Evaluate market norms for definitions and triggers.
        6. Advise on negotiation points and possible exceptions.
        7. Reference NVCA and ABA model documents.
        8. Address conflicts between agreements.
        9. Advise on best practices for clarity and documentation.
        10. Document all triggers and resulting actions.
        """,
        key_factors=[
            "Definition of change of control",
            "Triggering events",
            "Impact on rights and obligations",
            "Consistency across documents",
            "Market norms"
        ],
        primary_authority=[
            "NVCA Model Stock Option Plan",
            "NVCA Model Charter"
        ],
        burden_holder="Company (to define and administer triggers)",
        adversary_position="Investors and employees may seek broader triggers",
        counter_arguments=[
            "Overly broad triggers can complicate transactions",
            "Clarity prevents disputes",
            "Market norms guide definitions"
        ],
        resolution_strategy="Adopt clear, market-standard definitions and triggers for change of control.",
        entity_scope="Venture-backed companies",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NVCA Model Charter"
    ),
    DoctrineBlock(
        topic="Founder Equity Repricing and Option Exchange Programs",
        keywords=["founder equity", "repricing", "option exchange", "stock options", "venture capital"],
        conclusion_template="Option exchange programs may allow repricing of underwater options, subject to board and investor approval.",
        reasoning_framework="""
        1. Review equity plan and grant agreements for repricing and exchange provisions.
        2. Confirm board and investor approval requirements.
        3. Assess impact on employee retention and incentives.
        4. Evaluate market norms for repricing programs.
        5. Advise on disclosure and communication.
        6. Reference SEC and IRS guidance.
        7. Address tax and accounting implications.
        8. Advise on best practices for fairness and transparency.
        9. Confirm compliance with plan documents and securities laws.
        10. Document all approvals and exchanges.
        """,
        key_factors=[
            "Approval requirements",
            "Disclosure and communication",
            "Tax and accounting implications",
            "Market norms",
            "Plan document terms"
        ],
        primary_authority=[
            "SEC Rule 701",
            "IRC Section 409A",
            "Company equity plan"
        ],
        burden_holder="Company (to obtain approvals and administer program)",
        adversary_position="Investors may oppose repricing due to dilution",
        counter_arguments=[
            "Repricing can improve retention",
            "Dilution must be balanced",
            "Disclosure mitigates disputes"
        ],
        resolution_strategy="Implement repricing programs with full disclosure and required approvals.",
        entity_scope="Private companies granting stock options",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SEC Rule 701"
    ),
    DoctrineBlock(
        topic="Preferred Stock Automatic Conversion on IPO",
        keywords=["preferred stock", "automatic conversion", "IPO", "venture capital", "conversion mechanics"],
        conclusion_template="Preferred stock automatically converts to common upon a qualified IPO meeting specified criteria.",
        reasoning_framework="""
        1. Review the charter for automatic conversion provisions.
        2. Confirm IPO criteria (minimum proceeds, listing exchange, price per share).
        3. Assess mechanics and timing of conversion.
        4. Evaluate impact on cap table and investor rights.
        5. Advise on negotiation points and possible exceptions.
        6. Reference NVCA model documents.
        7. Address conflicts between series and classes.
        8. Confirm enforceability under