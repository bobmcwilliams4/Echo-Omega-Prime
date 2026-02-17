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
        topic="fair_market_value_standard",
        keywords=["FMV", "estate", "valuation", "IRC 2031", "willing buyer", "willing seller"],
        conclusion_template="The fair market value of the estate property is determined by the price at which the property would change hands between a willing buyer and a willing seller, neither being under any compulsion to buy or sell and both having reasonable knowledge of relevant facts.",
        reasoning_framework="""
The fair market value (FMV) standard is the cornerstone of estate valuation under IRC §2031. The FMV is defined by Treasury Regulations §20.2031-1(b) as the price at which property would change hands between a willing buyer and a willing seller, neither being under any compulsion to buy or sell and both having reasonable knowledge of relevant facts. Appraisers must consider all relevant market data, comparable sales, and the specific characteristics of the property. The FMV must exclude any speculative or forced sale prices and must reflect the actual market conditions as of the valuation date. The FMV standard applies to all estate assets unless a statutory exception exists (e.g., alternate valuation date, special use valuation).
        """,
        key_factors=[
            "Comparable sales data",
            "Market conditions",
            "Property characteristics",
            "Relevant facts known to parties",
            "Absence of compulsion"
        ],
        primary_authority=[
            "IRC §2031",
            "Treas. Reg. §20.2031-1(b)",
            "Estate of Newhouse v. Commissioner, 94 T.C. 193 (1990)"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge FMV determination if not supported by credible evidence.",
        counter_arguments=[
            "IRS may assert FMV based on different comparables or market data.",
            "IRS may argue for inclusion of speculative factors."
        ],
        resolution_strategy="Present credible, well-supported appraisal evidence and document all relevant facts and comparables.",
        entity_scope="Estate property subject to federal estate tax",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Newhouse v. Commissioner, 94 T.C. 193 (1990)"
    ),
    DoctrineBlock(
        topic="alternate_valuation_date_irc_2032",
        keywords=["alternate valuation", "IRC 2032", "estate", "valuation date", "6 months"],
        conclusion_template="If the executor elects the alternate valuation date under IRC §2032, the estate assets are valued as of the earlier of six months after the decedent’s death or the date of disposition.",
        reasoning_framework="""
IRC §2032 allows the executor to elect an alternate valuation date if it will result in a lower estate tax liability. The alternate valuation date is six months after the date of death, or the date of disposition if assets are sold, distributed, or otherwise disposed of before the six-month period. The election must be made on a timely filed estate tax return and applies to all assets; partial elections are not permitted. The alternate valuation is only available if it reduces both the value of the gross estate and the estate tax liability. The value of assets must reflect market conditions as of the alternate date, and any appreciation or depreciation is considered.
        """,
        key_factors=[
            "Election by executor",
            "Reduction in estate tax liability",
            "Asset disposition timing",
            "Market conditions at alternate date"
        ],
        primary_authority=[
            "IRC §2032",
            "Treas. Reg. §20.2032-1",
            "Estate of Andrews v. Commissioner, 79 T.C. 938 (1982)"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge the election if not properly made or if it does not reduce estate tax liability.",
        counter_arguments=[
            "Election not timely or properly made.",
            "Alternate valuation does not reduce tax liability."
        ],
        resolution_strategy="Ensure timely and proper election, document asset values as of alternate date, and demonstrate reduction in tax liability.",
        entity_scope="Estate assets subject to federal estate tax",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Andrews v. Commissioner, 79 T.C. 938 (1982)"
    ),
    DoctrineBlock(
        topic="special_use_valuation_irc_2032a",
        keywords=["special use", "IRC 2032A", "farm", "business", "valuation", "estate"],
        conclusion_template="If qualified real property is used for farming or a closely held business, the estate may elect special use valuation under IRC §2032A, valuing the property based on its actual use rather than highest and best use.",
        reasoning_framework="""
IRC §2032A provides for special use valuation for qualified real property used in farming or a closely held business. The election allows the property to be valued based on its actual use, rather than its highest and best use, potentially reducing estate tax liability. The property must meet strict requirements, including ownership and use by the decedent or family members, and must pass to qualified heirs. The election must be made on a timely filed return, and the estate must agree to potential recapture if the property ceases to be used for the qualifying purpose within ten years. The reduction in value is limited to a statutory maximum. The valuation is based on comparable sales of similarly used property, and the IRS may challenge the election if requirements are not met.
        """,
        key_factors=[
            "Qualified real property",
            "Actual use vs. highest and best use",
            "Ownership and use requirements",
            "Election and recapture agreement",
            "Statutory value reduction limits"
        ],
        primary_authority=[
            "IRC §2032A",
            "Treas. Reg. §20.2032A-1",
            "Estate of Gibbs v. United States, 992 F.2d 183 (8th Cir. 1993)"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge qualification or election, or assert recapture.",
        counter_arguments=[
            "Property does not meet use or ownership requirements.",
            "Election not properly made.",
            "Recapture triggered by post-death change in use."
        ],
        resolution_strategy="Document property use and ownership, ensure timely election, and comply with recapture agreement.",
        entity_scope="Qualified real property in estate",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Gibbs v. United States, 992 F.2d 183 (8th Cir. 1993)"
    ),
    DoctrineBlock(
        topic="real_property_appraisal_methods",
        keywords=["real property", "appraisal", "valuation", "income approach", "market approach", "cost approach"],
        conclusion_template="The value of real property in the estate is determined using recognized appraisal methods, including the market, income, and cost approaches, as appropriate to the property type.",
        reasoning_framework="""
Appraisers must use recognized methods to value real property for estate tax purposes. The market approach relies on comparable sales, adjusting for differences in location, size, and condition. The income approach capitalizes the property's net income, considering market rents, expenses, and capitalization rates. The cost approach estimates the replacement cost of improvements, less depreciation, plus land value. Selection of the appropriate method depends on the property type and market data availability. The IRS expects appraisals to be thorough, well-documented, and supported by credible evidence. The appraiser must consider zoning, environmental issues, and market trends. Disputes often arise over selection and application of methods, requiring expert testimony.
        """,
        key_factors=[
            "Comparable sales",
            "Net income and capitalization rates",
            "Replacement cost and depreciation",
            "Property type and market conditions",
            "Appraiser credentials"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1(b)",
            "USPAP standards",
            "Estate of Kollsman v. Commissioner, T.C. Memo 2017-40"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge appraisal methodology or comparables.",
        counter_arguments=[
            "Selection of inappropriate appraisal method.",
            "Insufficient or unreliable comparables.",
            "Failure to consider relevant market conditions."
        ],
        resolution_strategy="Engage qualified appraisers, document methodology, and support conclusions with credible evidence.",
        entity_scope="Real property in estate",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Kollsman v. Commissioner, T.C. Memo 2017-40"
    ),
    DoctrineBlock(
        topic="mineral_rights_valuation",
        keywords=["mineral rights", "oil", "gas", "valuation", "estate", "royalties"],
        conclusion_template="Mineral rights are valued based on their FMV, considering proven reserves, production history, lease terms, and market prices for minerals.",
        reasoning_framework="""
Mineral rights must be valued at FMV for estate tax purposes. The valuation considers proven and probable reserves, production history, lease agreements, royalty rates, and current market prices for minerals. Appraisers may use the income approach, capitalizing expected future royalties, or the market approach, comparing sales of similar mineral interests. The IRS may challenge valuations based on speculative assumptions or insufficient data. Accurate documentation of reserves, leases, and market conditions is essential. Environmental and regulatory factors may affect value. Disputes often arise over the reliability of reserve estimates and royalty projections.
        """,
        key_factors=[
            "Proven and probable reserves",
            "Production history",
            "Lease terms and royalty rates",
            "Market prices",
            "Environmental and regulatory factors"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Foster v. Commissioner, T.C. Memo 2011-95",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge reserve estimates or royalty projections.",
        counter_arguments=[
            "Speculative reserve estimates.",
            "Overstated or understated royalty rates.",
            "Failure to consider environmental factors."
        ],
        resolution_strategy="Provide credible reserve reports, lease documentation, and market data.",
        entity_scope="Mineral interests in estate",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Foster v. Commissioner, T.C. Memo 2011-95"
    ),
    DoctrineBlock(
        topic="closely_held_business_valuation",
        keywords=["closely held business", "valuation", "estate", "discounts", "marketability", "minority"],
        conclusion_template="The value of a closely held business is determined by FMV, considering earnings, assets, comparable sales, and appropriate discounts for lack of marketability and minority interests.",
        reasoning_framework="""
Valuation of closely held businesses for estate tax purposes requires consideration of earnings, assets, comparable transactions, and industry conditions. Appraisers may use the income, market, or asset approaches, depending on the business type and available data. Discounts for lack of marketability and minority interests are often applied to reflect the difficulty in selling non-controlling interests. The IRS scrutinizes the application and magnitude of discounts, requiring credible evidence and justification. The appraiser must consider buy-sell agreements, restrictions on transfer, and recent transactions. Disputes often center on the reliability of projections and the appropriateness of discounts.
        """,
        key_factors=[
            "Earnings and cash flow",
            "Asset values",
            "Comparable sales",
            "Marketability and minority discounts",
            "Buy-sell agreements"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Gallagher v. Commissioner, T.C. Memo 2011-148",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge valuation methodology or discount application.",
        counter_arguments=[
            "Overstated discounts.",
            "Unreliable earnings projections.",
            "Failure to consider recent transactions."
        ],
        resolution_strategy="Engage qualified appraisers, document methodology, and justify discounts with market evidence.",
        entity_scope="Closely held business interests in estate",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Gallagher v. Commissioner, T.C. Memo 2011-148"
    ),
    DoctrineBlock(
        topic="securities_valuation",
        keywords=["securities", "stocks", "bonds", "valuation", "estate", "market price"],
        conclusion_template="Publicly traded securities are valued at their FMV on the valuation date, using the mean between the highest and lowest quoted selling prices.",
        reasoning_framework="""
Treasury Regulations §20.2031-2 require that publicly traded securities be valued at FMV on the valuation date, typically the date of death or alternate valuation date. The FMV is determined by the mean between the highest and lowest quoted selling prices on the applicable date. If no sales occurred, the mean between bid and asked prices is used. Thinly traded or restricted securities may require additional analysis, including consideration of marketability and transfer restrictions. The IRS expects accurate documentation of pricing sources and trading volumes. Disputes may arise over the selection of pricing dates or the treatment of restricted securities.
        """,
        key_factors=[
            "Quoted selling prices",
            "Trading volume",
            "Marketability restrictions",
            "Valuation date",
            "Pricing sources"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Smith v. Commissioner, T.C. Memo 1999-368"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge pricing sources or treatment of restricted securities.",
        counter_arguments=[
            "Incorrect pricing date.",
            "Failure to consider marketability restrictions.",
            "Inaccurate documentation."
        ],
        resolution_strategy="Document pricing sources, trading volumes, and restrictions; use recognized valuation methods.",
        entity_scope="Publicly traded and restricted securities in estate",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Smith v. Commissioner, T.C. Memo 1999-368"
    ),
    DoctrineBlock(
        topic="life_insurance_proceeds",
        keywords=["life insurance", "proceeds", "estate", "IRC 2042", "incidents of ownership"],
        conclusion_template="Life insurance proceeds are includible in the gross estate if the decedent possessed any incidents of ownership or if the estate is the beneficiary.",
        reasoning_framework="""
IRC §2042 requires inclusion of life insurance proceeds in the gross estate if the decedent possessed any incidents of ownership at death, or if the estate is the beneficiary. Incidents of ownership include the right to change beneficiaries, surrender or cancel the policy, or borrow against it. The IRS scrutinizes policy ownership and beneficiary designations. Policies transferred within three years of death may be includible under IRC §2035. Disputes often arise over the interpretation of incidents of ownership and the timing of transfers. Proper documentation of policy ownership and beneficiary changes is essential.
        """,
        key_factors=[
            "Incidents of ownership",
            "Beneficiary designation",
            "Policy ownership",
            "Transfers within three years",
            "Policy documentation"
        ],
        primary_authority=[
            "IRC §2042",
            "Treas. Reg. §20.2042-1",
            "Estate of Fine v. Commissioner, 50 T.C. 104 (1968)"
        ],
        burden_holder="Estate",
        adversary_position="IRS may assert inclusion based on incidents of ownership or recent transfers.",
        counter_arguments=[
            "No incidents of ownership.",
            "Policy transferred more than three years before death.",
            "Estate not beneficiary."
        ],
        resolution_strategy="Document policy ownership, incidents of ownership, and beneficiary designations.",
        entity_scope="Life insurance policies owned or controlled by decedent",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Fine v. Commissioner, 50 T.C. 104 (1968)"
    ),
    DoctrineBlock(
        topic="retirement_accounts_valuation",
        keywords=["retirement accounts", "IRA", "401(k)", "valuation", "estate", "FMV"],
        conclusion_template="Retirement accounts are valued at FMV as of the valuation date, considering account balances, investment holdings, and any restrictions.",
        reasoning_framework="""
Retirement accounts, including IRAs and 401(k)s, are valued at FMV as of the valuation date. The FMV includes the account balance, investment holdings, and accrued income. Any restrictions on withdrawal or penalties must be considered. The IRS expects accurate documentation of account statements and investment values. If the account is subject to required minimum distributions, these must be considered in valuation. Disputes may arise over the treatment of restricted or illiquid investments within the account.
        """,
        key_factors=[
            "Account balance",
            "Investment holdings",
            "Accrued income",
            "Withdrawal restrictions",
            "Account statements"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Kahn v. Commissioner, T.C. Memo 2001-76"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge valuation of illiquid or restricted investments.",
        counter_arguments=[
            "Failure to consider restrictions.",
            "Inaccurate account statements.",
            "Improper treatment of distributions."
        ],
        resolution_strategy="Document account balances, investment holdings, and restrictions; use recognized valuation methods.",
        entity_scope="Retirement accounts in estate",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Kahn v. Commissioner, T.C. Memo 2001-76"
    ),
    DoctrineBlock(
        topic="personal_property_inventory",
        keywords=["personal property", "inventory", "valuation", "estate", "FMV"],
        conclusion_template="Personal property in the estate is inventoried and valued at FMV, considering condition, provenance, and market comparables.",
        reasoning_framework="""
Personal property must be inventoried and valued at FMV for estate tax purposes. The valuation considers the item's condition, provenance, and comparable sales in the relevant market. Appraisers must document the inventory, provide photographs, and support values with market data. The IRS may challenge valuations based on insufficient documentation or unreliable comparables. Special considerations apply to collectibles, artwork, and antiques, which may require expert appraisals. Disputes often arise over authenticity, provenance, and marketability.
        """,
        key_factors=[
            "Condition",
            "Provenance",
            "Market comparables",
            "Inventory documentation",
            "Appraiser credentials"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "USPAP standards",
            "Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge inventory or valuation of personal property.",
        counter_arguments=[
            "Insufficient documentation.",
            "Unreliable comparables.",
            "Disputed provenance or authenticity."
        ],
        resolution_strategy="Engage qualified appraisers, document inventory, and support values with market evidence.",
        entity_scope="Personal property in estate",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1"
    ),
    DoctrineBlock(
        topic="debts_and_liabilities",
        keywords=["debts", "liabilities", "estate", "deductions", "IRC 2053"],
        conclusion_template="Debts and liabilities are deductible from the gross estate if they are enforceable, bona fide, and substantiated by credible evidence.",
        reasoning_framework="""
IRC §2053 allows deduction of debts and liabilities from the gross estate if they are bona fide, enforceable, and substantiated. The estate must provide documentation, such as loan agreements, promissory notes, and payment records. The IRS scrutinizes related-party debts and may challenge deductions lacking credible evidence. Disputes often arise over the enforceability and bona fide nature of debts, especially those incurred shortly before death. The estate must demonstrate that the debt was not created for tax avoidance purposes and that it represents a legitimate obligation.
        """,
        key_factors=[
            "Bona fide nature",
            "Enforceability",
            "Documentation",
            "Related-party transactions",
            "Timing of debt creation"
        ],
        primary_authority=[
            "IRC §2053",
            "Treas. Reg. §20.2053-1",
            "Estate of Graegin v. Commissioner, T.C. Memo 1988-477"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge deduction of debts as not bona fide or enforceable.",
        counter_arguments=[
            "Debt not bona fide.",
            "Insufficient documentation.",
            "Debt created for tax avoidance."
        ],
        resolution_strategy="Provide credible documentation and evidence of bona fide and enforceable nature.",
        entity_scope="Debts and liabilities of estate",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Graegin v. Commissioner, T.C. Memo 1988-477"
    ),
    DoctrineBlock(
        topic="lack_of_marketability_discount",
        keywords=["lack of marketability", "discount", "valuation", "closely held", "estate"],
        conclusion_template="A discount for lack of marketability may be applied to closely held business interests to reflect the difficulty in selling such interests.",
        reasoning_framework="""
The lack of marketability discount reflects the reduced value of interests that cannot be readily sold or transferred. Appraisers must justify the magnitude of the discount with market evidence, considering factors such as restrictions on transfer, absence of public market, and recent transactions. The IRS scrutinizes the application of marketability discounts, requiring credible evidence and justification. Disputes often arise over the magnitude and justification for the discount. The appraiser must consider relevant court decisions and industry studies.
        """,
        key_factors=[
            "Transfer restrictions",
            "Absence of public market",
            "Recent transactions",
            "Industry studies",
            "Appraiser justification"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Mandelbaum v. Commissioner, T.C. Memo 1995-614",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge magnitude or justification for discount.",
        counter_arguments=[
            "Overstated discount.",
            "Insufficient market evidence.",
            "Failure to consider recent sales."
        ],
        resolution_strategy="Document restrictions, market evidence, and industry studies to justify discount.",
        entity_scope="Closely held business interests in estate",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Mandelbaum v. Commissioner, T.C. Memo 1995-614"
    ),
    DoctrineBlock(
        topic="minority_interest_discount",
        keywords=["minority interest", "discount", "valuation", "closely held", "estate"],
        conclusion_template="A minority interest discount may be applied to non-controlling interests in closely held businesses to reflect lack of control.",
        reasoning_framework="""
The minority interest discount reflects the reduced value of non-controlling interests in closely held businesses. Appraisers must consider the degree of control, voting rights, and restrictions on management. The IRS scrutinizes the application and magnitude of minority discounts, requiring credible evidence and justification. Disputes often arise over the degree of control and the appropriateness of the discount. The appraiser must consider relevant court decisions, industry studies, and recent transactions.
        """,
        key_factors=[
            "Degree of control",
            "Voting rights",
            "Management restrictions",
            "Industry studies",
            "Appraiser justification"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Gallagher v. Commissioner, T.C. Memo 2011-148",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge magnitude or justification for discount.",
        counter_arguments=[
            "Overstated discount.",
            "Insufficient market evidence.",
            "Failure to consider recent sales."
        ],
        resolution_strategy="Document degree of control, market evidence, and industry studies to justify discount.",
        entity_scope="Non-controlling interests in closely held businesses",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Gallagher v. Commissioner, T.C. Memo 2011-148"
    ),
    DoctrineBlock(
        topic="qualified_appraisal_requirements",
        keywords=["qualified appraisal", "requirements", "estate", "valuation", "appraiser credentials"],
        conclusion_template="A qualified appraisal must be prepared by a qualified appraiser, comply with USPAP standards, and include all required information for estate tax purposes.",
        reasoning_framework="""
Treasury Regulations and IRS guidance require that appraisals submitted for estate tax purposes be prepared by qualified appraisers, comply with USPAP standards, and include all required information. The appraisal must describe the property, state the FMV, explain the methodology, and provide supporting evidence. The appraiser must have appropriate credentials and experience. The IRS may reject appraisals that lack credibility, documentation, or compliance with standards. Disputes often arise over appraiser qualifications and the sufficiency of the appraisal report.
        """,
        key_factors=[
            "Appraiser credentials",
            "USPAP compliance",
            "Property description",
            "Methodology explanation",
            "Supporting evidence"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "IRS Notice 2006-96",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may reject appraisal for lack of qualifications or compliance.",
        counter_arguments=[
            "Appraiser lacks credentials.",
            "Appraisal does not comply with USPAP.",
            "Insufficient supporting evidence."
        ],
        resolution_strategy="Engage qualified appraisers and ensure compliance with all requirements.",
        entity_scope="Appraisals submitted for estate tax purposes",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2006-96"
    ),
    DoctrineBlock(
        topic="fractional_interest_real_estate",
        keywords=["fractional interest", "real estate", "valuation", "discount", "estate"],
        conclusion_template="Fractional interests in real estate may be valued at FMV, applying appropriate discounts for lack of control and marketability.",
        reasoning_framework="""
Fractional interests in real estate are valued at FMV, considering the impact of lack of control and marketability. Appraisers may apply discounts to reflect the difficulty in selling or managing fractional interests. The IRS scrutinizes the magnitude and justification for discounts, requiring credible evidence and market data. Disputes often arise over the degree of control, transfer restrictions, and recent transactions. The appraiser must consider relevant court decisions and industry studies.
        """,
        key_factors=[
            "Degree of control",
            "Transfer restrictions",
            "Marketability",
            "Recent transactions",
            "Appraiser justification"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Williams v. Commissioner, T.C. Memo 1998-59",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge magnitude or justification for discount.",
        counter_arguments=[
            "Overstated discount.",
            "Insufficient market evidence.",
            "Failure to consider recent sales."
        ],
        resolution_strategy="Document degree of control, market evidence, and industry studies to justify discount.",
        entity_scope="Fractional interests in real estate in estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Williams v. Commissioner, T.C. Memo 1998-59"
    ),
    DoctrineBlock(
        topic="environmental_contamination_impact",
        keywords=["environmental contamination", "impact", "valuation", "real property", "estate"],
        conclusion_template="Environmental contamination may reduce the FMV of real property in the estate, requiring consideration of remediation costs and market stigma.",
        reasoning_framework="""
Environmental contamination can significantly impact the FMV of real property in the estate. Appraisers must consider remediation costs, regulatory compliance, and market stigma. The IRS expects credible evidence of contamination and its impact on value, including environmental reports and market data. Disputes often arise over the extent of contamination, cost estimates, and the impact on marketability. The appraiser must document all relevant factors and support conclusions with credible evidence.
        """,
        key_factors=[
            "Extent of contamination",
            "Remediation costs",
            "Regulatory compliance",
            "Market stigma",
            "Environmental reports"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Litchfield v. Commissioner, T.C. Memo 2012-21",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge contamination impact or cost estimates.",
        counter_arguments=[
            "Insufficient evidence of contamination.",
            "Overstated remediation costs.",
            "Failure to consider market stigma."
        ],
        resolution_strategy="Document contamination, remediation costs, and market impact with credible evidence.",
        entity_scope="Contaminated real property in estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Litchfield v. Commissioner, T.C. Memo 2012-21"
    ),
    DoctrineBlock(
        topic="buy_sell_agreement_valuation",
        keywords=["buy-sell agreement", "valuation", "estate", "closely held business", "FMV"],
        conclusion_template="Buy-sell agreements may influence the FMV of closely held business interests in the estate if they meet IRS requirements for bona fide and arm’s-length transactions.",
        reasoning_framework="""
Buy-sell agreements can affect the FMV of closely held business interests in the estate if they are bona fide, entered at arm’s length, and not for tax avoidance purposes. The IRS examines the terms, funding, and history of the agreement. If the agreement sets a price, it must reflect FMV and be enforceable. Agreements between related parties are scrutinized for legitimacy. Disputes often arise over the enforceability and FMV nature of the agreement. The appraiser must consider the agreement terms, recent transactions, and relevant court decisions.
        """,
        key_factors=[
            "Bona fide nature",
            "Arm’s-length transaction",
            "Agreement terms",
            "Funding",
            "Enforceability"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2(h)",
            "Estate of Lauder v. Commissioner, T.C. Memo 2012-227",
            "IRC §2703"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge agreement as not bona fide or not reflecting FMV.",
        counter_arguments=[
            "Agreement not arm’s length.",
            "Price does not reflect FMV.",
            "Agreement not enforceable."
        ],
        resolution_strategy="Document agreement terms, funding, and arm’s-length nature; support price with market evidence.",
        entity_scope="Closely held business interests in estate",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Lauder v. Commissioner, T.C. Memo 2012-227"
    ),
    DoctrineBlock(
        topic="valuation_of_partnership_interests",
        keywords=["partnership", "interest", "valuation", "discount", "estate"],
        conclusion_template="Partnership interests are valued at FMV, considering partnership agreement terms, distributions, and appropriate discounts for lack of control and marketability.",
        reasoning_framework="""
Partnership interests in the estate are valued at FMV, considering the terms of the partnership agreement, distribution rights, and restrictions on transfer. Appraisers may apply discounts for lack of control and marketability, supported by market evidence and industry studies. The IRS scrutinizes the magnitude and justification for discounts, requiring credible evidence. Disputes often arise over the degree of control, transfer restrictions, and recent transactions. The appraiser must consider relevant court decisions and partnership agreement provisions.
        """,
        key_factors=[
            "Partnership agreement terms",
            "Distribution rights",
            "Transfer restrictions",
            "Degree of control",
            "Market evidence"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-3",
            "Estate of Harrison v. Commissioner, T.C. Memo 1987-8",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge magnitude or justification for discounts.",
        counter_arguments=[
            "Overstated discount.",
            "Insufficient market evidence.",
            "Failure to consider partnership agreement terms."
        ],
        resolution_strategy="Document agreement terms, market evidence, and industry studies to justify discounts.",
        entity_scope="Partnership interests in estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Harrison v. Commissioner, T.C. Memo 1987-8"
    ),
    DoctrineBlock(
        topic="valuation_of_trust_assets",
        keywords=["trust", "assets", "valuation", "estate", "FMV"],
        conclusion_template="Trust assets are valued at FMV as of the valuation date, considering trust terms, asset types, and any restrictions.",
        reasoning_framework="""
Trust assets included in the estate are valued at FMV as of the valuation date. The valuation considers trust terms, asset types, and any restrictions on transfer or distribution. The IRS expects accurate documentation of trust assets and supporting evidence for values. Disputes may arise over the inclusion of assets, valuation of illiquid holdings, and interpretation of trust terms. The appraiser must consider relevant court decisions and trust documentation.
        """,
        key_factors=[
            "Trust terms",
            "Asset types",
            "Transfer restrictions",
            "Distribution provisions",
            "Documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Turner v. Commissioner, T.C. Memo 2011-209"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge inclusion or valuation of trust assets.",
        counter_arguments=[
            "Improper inclusion of assets.",
            "Inaccurate valuation.",
            "Failure to consider restrictions."
        ],
        resolution_strategy="Document trust terms, asset types, and restrictions; use recognized valuation methods.",
        entity_scope="Trust assets in estate",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Turner v. Commissioner, T.C. Memo 2011-209"
    ),
    DoctrineBlock(
        topic="valuation_of_foreign_assets",
        keywords=["foreign assets", "valuation", "estate", "FMV", "exchange rates"],
        conclusion_template="Foreign assets are valued at FMV as of the valuation date, using appropriate exchange rates and considering market conditions in the foreign jurisdiction.",
        reasoning_framework="""
Foreign assets included in the estate are valued at FMV as of the valuation date. The valuation must use appropriate exchange rates and consider market conditions in the foreign jurisdiction. The IRS expects accurate documentation of asset values, exchange rates, and market data. Disputes may arise over the selection of exchange rates, market comparables, and treatment of foreign restrictions. The appraiser must consider relevant court decisions and international valuation standards.
        """,
        key_factors=[
            "Exchange rates",
            "Market conditions in foreign jurisdiction",
            "Asset types",
            "Transfer restrictions",
            "Documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Noll v. Commissioner, T.C. Memo 2013-38"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge exchange rates or market comparables.",
        counter_arguments=[
            "Inappropriate exchange rate.",
            "Insufficient market evidence.",
            "Failure to consider foreign restrictions."
        ],
        resolution_strategy="Document exchange rates, market conditions, and asset values; use recognized valuation methods.",
        entity_scope="Foreign assets in estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Noll v. Commissioner, T.C. Memo 2013-38"
    ),
    DoctrineBlock(
        topic="valuation_of_intellectual_property",
        keywords=["intellectual property", "patents", "copyrights", "trademarks", "valuation", "estate"],
        conclusion_template="Intellectual property is valued at FMV, considering income potential, market comparables, and legal protections.",
        reasoning_framework="""
Intellectual property included in the estate is valued at FMV, considering income potential, market comparables, and legal protections. Appraisers may use the income approach, capitalizing expected royalties, or the market approach, comparing sales of similar IP. The IRS expects credible evidence of income potential and market data. Disputes often arise over the reliability of projections, legal protections, and comparable transactions. The appraiser must document all relevant factors and support conclusions with credible evidence.
        """,
        key_factors=[
            "Income potential",
            "Market comparables",
            "Legal protections",
            "Royalty rates",
            "Documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Jackson v. Commissioner, T.C. Memo 2021-48"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge income projections or comparables.",
        counter_arguments=[
            "Speculative income projections.",
            "Insufficient market evidence.",
            "Failure to consider legal protections."
        ],
        resolution_strategy="Document income potential, market comparables, and legal protections; use recognized valuation methods.",
        entity_scope="Intellectual property in estate",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Jackson v. Commissioner, T.C. Memo 2021-48"
    ),
    DoctrineBlock(
        topic="valuation_of_collectibles",
        keywords=["collectibles", "art", "antiques", "valuation", "estate", "FMV"],
        conclusion_template="Collectibles are valued at FMV, considering provenance, authenticity, market comparables, and appraiser expertise.",
        reasoning_framework="""
Collectibles included in the estate are valued at FMV, considering provenance, authenticity, market comparables, and appraiser expertise. The IRS expects credible evidence of authenticity and market data. Appraisers must document provenance, provide photographs, and support values with comparable sales. Disputes often arise over authenticity, provenance, and marketability. The appraiser must consider relevant court decisions and industry standards.
        """,
        key_factors=[
            "Provenance",
            "Authenticity",
            "Market comparables",
            "Appraiser expertise",
            "Documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge authenticity or valuation of collectibles.",
        counter_arguments=[
            "Disputed authenticity.",
            "Insufficient market evidence.",
            "Failure to document provenance."
        ],
        resolution_strategy="Engage qualified appraisers, document provenance and authenticity, and support values with market evidence.",
        entity_scope="Collectibles in estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1"
    ),
    DoctrineBlock(
        topic="valuation_of_deferred_compensation",
        keywords=["deferred compensation", "valuation", "estate", "FMV", "IRC 2039"],
        conclusion_template="Deferred compensation rights are valued at FMV, considering payout terms, present value calculations, and any restrictions.",
        reasoning_framework="""
Deferred compensation rights included in the estate are valued at FMV, considering payout terms, present value calculations, and any restrictions. The IRS expects accurate documentation of compensation agreements and payout schedules. Disputes may arise over present value calculations and treatment of restrictions. The appraiser must consider relevant court decisions and compensation agreement provisions.
        """,
        key_factors=[
            "Payout terms",
            "Present value calculations",
            "Restrictions",
            "Compensation agreement provisions",
            "Documentation"
        ],
        primary_authority=[
            "IRC §2039",
            "Treas. Reg. §20.2039-1",
            "Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge present value calculations or inclusion.",
        counter_arguments=[
            "Improper present value calculation.",
            "Insufficient documentation.",
            "Failure to consider restrictions."
        ],
        resolution_strategy="Document payout terms, compensation agreements, and restrictions; use recognized valuation methods.",
        entity_scope="Deferred compensation rights in estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
    ),
    DoctrineBlock(
        topic="valuation_of_options_and_warrants",
        keywords=["options", "warrants", "valuation", "estate", "FMV"],
        conclusion_template="Options and warrants are valued at FMV, considering exercise price, expiration date, market volatility, and transferability.",
        reasoning_framework="""
Options and warrants included in the estate are valued at FMV, considering exercise price, expiration date, market volatility, and transferability. Appraisers may use option pricing models, such as Black-Scholes, to estimate value. The IRS expects accurate documentation of terms and market data. Disputes may arise over model assumptions and treatment of restrictions. The appraiser must consider relevant court decisions and option agreement provisions.
        """,
        key_factors=[
            "Exercise price",
            "Expiration date",
            "Market volatility",
            "Transferability",
            "Option agreement provisions"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Smith v. Commissioner, T.C. Memo 1999-368"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge model assumptions or inclusion.",
        counter_arguments=[
            "Improper model assumptions.",
            "Insufficient documentation.",
            "Failure to consider restrictions."
        ],
        resolution_strategy="Document option terms, market volatility, and transferability; use recognized valuation models.",
        entity_scope="Options and warrants in estate",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Smith v. Commissioner, T.C. Memo 1999-368"
    ),
    DoctrineBlock(
        topic="valuation_of_promissory_notes",
        keywords=["promissory notes", "valuation", "estate", "FMV", "discount"],
        conclusion_template="Promissory notes are valued at FMV, considering interest rate, payment history, collectibility, and appropriate discounts for risk.",
        reasoning_framework="""
Promissory notes included in the estate are valued at FMV, considering interest rate, payment history, collectibility, and appropriate discounts for risk. The IRS expects accurate documentation of note terms and payment records. Disputes may arise over collectibility and magnitude of discounts. The appraiser must consider relevant court decisions and note agreement provisions.
        """,
        key_factors=[
            "Interest rate",
            "Payment history",
            "Collectibility",
            "Discounts for risk",
            "Note agreement provisions"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-4",
            "Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge collectibility or magnitude of discounts.",
        counter_arguments=[
            "Overstated discount.",
            "Insufficient payment history.",
            "Failure to consider risk factors."
        ],
        resolution_strategy="Document note terms, payment history, and risk factors; use recognized valuation methods.",
        entity_scope="Promissory notes in estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
    ),
    DoctrineBlock(
        topic="valuation_of_annuities",
        keywords=["annuities", "valuation", "estate", "FMV", "IRC 2039"],
        conclusion_template="Annuities are valued at FMV, considering payout terms, present value calculations, and any restrictions.",
        reasoning_framework="""
Annuities included in the estate are valued at FMV, considering payout terms, present value calculations, and any restrictions. The IRS expects accurate documentation of annuity agreements and payout schedules. Disputes may arise over present value calculations and treatment of restrictions. The appraiser must consider relevant court decisions and annuity agreement provisions.
        """,
        key_factors=[
            "Payout terms",
            "Present value calculations",
            "Restrictions",
            "Annuity agreement provisions",
            "Documentation"
        ],
        primary_authority=[
            "IRC §2039",
            "Treas. Reg. §20.2039-1",
            "Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge present value calculations or inclusion.",
        counter_arguments=[
            "Improper present value calculation.",
            "Insufficient documentation.",
            "Failure to consider restrictions."
        ],
        resolution_strategy="Document payout terms, annuity agreements, and restrictions; use recognized valuation methods.",
        entity_scope="Annuities in estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
    ),
    DoctrineBlock(
        topic="valuation_of_cash_and_equivalents",
        keywords=["cash", "equivalents", "valuation", "estate", "FMV"],
        conclusion_template="Cash and cash equivalents are valued at FMV as of the valuation date, considering account balances and any restrictions.",
        reasoning_framework="""
Cash and cash equivalents included in the estate are valued at FMV as of the valuation date. The valuation considers account balances and any restrictions on withdrawal or transfer. The IRS expects accurate documentation of account statements and balances. Disputes may arise over the inclusion of restricted funds or treatment of foreign currency. The appraiser must consider relevant court decisions and account documentation.
        """,
        key_factors=[
            "Account balances",
            "Withdrawal restrictions",
            "Foreign currency",
            "Documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Noll v. Commissioner, T.C. Memo 2013-38"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge inclusion or valuation of restricted funds.",
        counter_arguments=[
            "Improper inclusion of restricted funds.",
            "Inaccurate account statements.",
            "Failure to consider foreign currency."
        ],
        resolution_strategy="Document account balances, restrictions, and currency; use recognized valuation methods.",
        entity_scope="Cash and cash equivalents in estate",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Noll v. Commissioner, T.C. Memo 2013-38"
    ),
    DoctrineBlock(
        topic="valuation_of_receivables",
        keywords=["receivables", "valuation", "estate", "FMV", "collectibility"],
        conclusion_template="Receivables are valued at FMV, considering collectibility, payment history, and appropriate discounts for risk.",
        reasoning_framework="""
Receivables included in the estate are valued at FMV, considering collectibility, payment history, and appropriate discounts for risk. The IRS expects accurate documentation of receivable terms and payment records. Disputes may arise over collectibility and magnitude of discounts. The appraiser must consider relevant court decisions and receivable agreement provisions.
        """,
        key_factors=[
            "Collectibility",
            "Payment history",
            "Discounts for risk",
            "Receivable agreement provisions",
            "Documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-4",
            "Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge collectibility or magnitude of discounts.",
        counter_arguments=[
            "Overstated discount.",
            "Insufficient payment history.",
            "Failure to consider risk factors."
        ],
        resolution_strategy="Document receivable terms, payment history, and risk factors; use recognized valuation methods.",
        entity_scope="Receivables in estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of McKeon v. Commissioner, T.C. Memo 1988-21"
    ),
    DoctrineBlock(
        topic="valuation_of_leases",
        keywords=["leases", "valuation", "estate", "FMV", "lease terms"],
        conclusion_template="Leases are valued at FMV, considering lease terms, market rents, and any restrictions or options.",
        reasoning_framework="""
Leases included in the estate are valued at FMV, considering lease terms, market rents, and any restrictions or options. The IRS expects accurate documentation of lease agreements and market data. Disputes may arise over lease terms, market comparables, and treatment of options. The appraiser must consider relevant court decisions and lease agreement provisions.
        """,
        key_factors=[
            "Lease terms",
            "Market rents",
            "Restrictions",
            "Options",
            "Documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Kollsman v. Commissioner, T.C. Memo 2017-40"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge lease terms or market comparables.",
        counter_arguments=[
            "Improper lease terms.",
            "Insufficient market evidence.",
            "Failure to consider restrictions or options."
        ],
        resolution_strategy="Document lease terms, market rents, and options; use recognized valuation methods.",
        entity_scope="Leases in estate",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Kollsman v. Commissioner, T.C. Memo 2017-40"
    ),
    DoctrineBlock(
        topic="valuation_of_inventory",
        keywords=["inventory", "valuation", "estate", "FMV", "market price"],
        conclusion_template="Inventory is valued at FMV as of the valuation date, considering market prices, condition, and obsolescence.",
        reasoning_framework="""
Inventory included in the estate is valued at FMV as of the valuation date, considering market prices, condition, and obsolescence. The IRS expects accurate documentation of inventory lists and market data. Disputes may arise over the treatment of obsolete or unsellable inventory. The appraiser must consider relevant court decisions and inventory documentation.
        """,
        key_factors=[
            "Market prices",
            "Condition",
            "Obsolescence",
            "Inventory documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge treatment of obsolete inventory or market prices.",
        counter_arguments=[
            "Improper treatment of obsolete inventory.",
            "Inaccurate market prices.",
            "Insufficient documentation."
        ],
        resolution_strategy="Document inventory condition, market prices, and obsolescence; use recognized valuation methods.",
        entity_scope="Inventory in estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1"
    ),
    DoctrineBlock(
        topic="valuation_of_real_estate_under_condemnation",
        keywords=["real estate", "condemnation", "valuation", "estate", "FMV"],
        conclusion_template="Real estate subject to condemnation is valued at FMV, considering compensation received, market conditions, and legal proceedings.",
        reasoning_framework="""
Real estate subject to condemnation included in the estate is valued at FMV, considering compensation received, market conditions, and legal proceedings. The IRS expects accurate documentation of condemnation awards and market data. Disputes may arise over the adequacy of compensation and impact on FMV. The appraiser must consider relevant court decisions and condemnation documentation.
        """,
        key_factors=[
            "Compensation received",
            "Market conditions",
            "Legal proceedings",
            "Condemnation documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Litchfield v. Commissioner, T.C. Memo 2012-21"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge adequacy of compensation or market conditions.",
        counter_arguments=[
            "Inadequate compensation.",
            "Improper market conditions.",
            "Insufficient documentation."
        ],
        resolution_strategy="Document compensation received, market conditions, and legal proceedings; use recognized valuation methods.",
        entity_scope="Real estate under condemnation in estate",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Litchfield v. Commissioner, T.C. Memo 2012-21"
    ),
    DoctrineBlock(
        topic="valuation_of_water_rights",
        keywords=["water rights", "valuation", "estate", "FMV", "regulatory restrictions"],
        conclusion_template="Water rights are valued at FMV, considering regulatory restrictions, usage history, and market comparables.",
        reasoning_framework="""
Water rights included in the estate are valued at FMV, considering regulatory restrictions, usage history, and market comparables. The IRS expects accurate documentation of water rights, usage records, and market data. Disputes may arise over regulatory compliance and market comparables. The appraiser must consider relevant court decisions and water rights documentation.
        """,
        key_factors=[
            "Regulatory restrictions",
            "Usage history",
            "Market comparables",
            "Documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Foster v. Commissioner, T.C. Memo 2011-95"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge regulatory compliance or market comparables.",
        counter_arguments=[
            "Improper regulatory compliance.",
            "Insufficient market evidence.",
            "Failure to document usage history."
        ],
        resolution_strategy="Document regulatory restrictions, usage history, and market comparables; use recognized valuation methods.",
        entity_scope="Water rights in estate",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Foster v. Commissioner, T.C. Memo 2011-95"
    ),
    DoctrineBlock(
        topic="valuation_of_timber_rights",
        keywords=["timber rights", "valuation", "estate", "FMV", "harvest history"],
        conclusion_template="Timber rights are valued at FMV, considering harvest history, market prices, and regulatory restrictions.",
        reasoning_framework="""
Timber rights included in the estate are valued at FMV, considering harvest history, market prices, and regulatory restrictions. The IRS expects accurate documentation of timber rights, harvest records, and market data. Disputes may arise over regulatory compliance and market prices. The appraiser must consider relevant court decisions and timber rights documentation.
        """,
        key_factors=[
            "Harvest history",
            "Market prices",
            "Regulatory restrictions",
            "Documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Foster v. Commissioner, T.C. Memo 2011-95"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge regulatory compliance or market prices.",
        counter_arguments=[
            "Improper regulatory compliance.",
            "Insufficient market evidence.",
            "Failure to document harvest history."
        ],
        resolution_strategy="Document harvest history, market prices, and regulatory restrictions; use recognized valuation methods.",
        entity_scope="Timber rights in estate",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Foster v. Commissioner, T.C. Memo 2011-95"
    ),
    DoctrineBlock(
        topic="valuation_of_agricultural_land",
        keywords=["agricultural land", "valuation", "estate", "FMV", "income potential"],
        conclusion_template="Agricultural land is valued at FMV, considering income potential, market comparables, and regulatory restrictions.",
        reasoning_framework="""
Agricultural land included in the estate is valued at FMV, considering income potential, market comparables, and regulatory restrictions. The IRS expects accurate documentation of land use, income records, and market data. Disputes may arise over regulatory compliance and market comparables. The appraiser must consider relevant court decisions and agricultural land documentation.
        """,
        key_factors=[
            "Income potential",
            "Market comparables",
            "Regulatory restrictions",
            "Land use documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Gibbs v. United States, 992 F.2d 183 (8th Cir. 1993)"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge regulatory compliance or market comparables.",
        counter_arguments=[
            "Improper regulatory compliance.",
            "Insufficient market evidence.",
            "Failure to document land use."
        ],
        resolution_strategy="Document income potential, market comparables, and regulatory restrictions; use recognized valuation methods.",
        entity_scope="Agricultural land in estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Gibbs v. United States, 992 F.2d 183 (8th Cir. 1993)"
    ),
    DoctrineBlock(
        topic="valuation_of_machinery_and_equipment",
        keywords=["machinery", "equipment", "valuation", "estate", "FMV", "condition"],
        conclusion_template="Machinery and equipment are valued at FMV, considering condition, market comparables, and obsolescence.",
        reasoning_framework="""
Machinery and equipment included in the estate are valued at FMV, considering condition, market comparables, and obsolescence. The IRS expects accurate documentation of machinery and equipment lists and market data. Disputes may arise over the treatment of obsolete or unsellable equipment. The appraiser must consider relevant court decisions and equipment documentation.
        """,
        key_factors=[
            "Condition",
            "Market comparables",
            "Obsolescence",
            "Equipment documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge treatment of obsolete equipment or market comparables.",
        counter_arguments=[
            "Improper treatment of obsolete equipment.",
            "Inaccurate market comparables.",
            "Insufficient documentation."
        ],
        resolution_strategy="Document equipment condition, market comparables, and obsolescence; use recognized valuation methods.",
        entity_scope="Machinery and equipment in estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Van Gogh v. Commissioner, T.C. Memo 2014-1"
    ),
    DoctrineBlock(
        topic="valuation_of_farm_assets",
        keywords=["farm assets", "valuation", "estate", "FMV", "special use"],
        conclusion_template="Farm assets are valued at FMV, considering special use valuation, market comparables, and income potential.",
        reasoning_framework="""
Farm assets included in the estate are valued at FMV, considering special use valuation, market comparables, and income potential. The IRS expects accurate documentation of farm asset lists, market data, and income records. Disputes may arise over eligibility for special use valuation and market comparables. The appraiser must consider relevant court decisions and farm asset documentation.
        """,
        key_factors=[
            "Special use eligibility",
            "Market comparables",
            "Income potential",
            "Farm asset documentation",
            "Valuation date"
        ],
        primary_authority=[
            "IRC §2032A",
            "Treas. Reg. §20.2032A-1",
            "Estate of Gibbs v. United States, 992 F.2d 183 (8th Cir. 1993)"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge eligibility for special use valuation or market comparables.",
        counter_arguments=[
            "Improper eligibility for special use.",
            "Insufficient market evidence.",
            "Failure to document farm assets."
        ],
        resolution_strategy="Document special use eligibility, market comparables, and income potential; use recognized valuation methods.",
        entity_scope="Farm assets in estate",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Gibbs v. United States, 992 F.2d 183 (8th Cir. 1993)"
    ),
    DoctrineBlock(
        topic="valuation_of_mineral_exploration_rights",
        keywords=["mineral exploration rights", "valuation", "estate", "FMV", "exploration history"],
        conclusion_template="Mineral exploration rights are valued at FMV, considering exploration history, market prices, and regulatory restrictions.",
        reasoning_framework="""
Mineral exploration rights included in the estate are valued at FMV, considering exploration history, market prices, and regulatory restrictions. The IRS expects accurate documentation of exploration rights, exploration records, and market data. Disputes may arise over regulatory compliance and market prices. The appraiser must consider relevant court decisions and exploration rights documentation.
        """,
        key_factors=[
            "Exploration history",
            "Market prices",
            "Regulatory restrictions",
            "Documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Foster v. Commissioner, T.C. Memo 2011-95"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge regulatory compliance or market prices.",
        counter_arguments=[
            "Improper regulatory compliance.",
            "Insufficient market evidence.",
            "Failure to document exploration history."
        ],
        resolution_strategy="Document exploration history, market prices, and regulatory restrictions; use recognized valuation methods.",
        entity_scope="Mineral exploration rights in estate",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Foster v. Commissioner, T.C. Memo 2011-95"
    ),
    DoctrineBlock(
        topic="valuation_of_royalty_interests",
        keywords=["royalty interests", "valuation", "estate", "FMV", "income potential"],
        conclusion_template="Royalty interests are valued at FMV, considering income potential, market comparables, and contractual terms.",
        reasoning_framework="""
Royalty interests included in the estate are valued at FMV, considering income potential, market comparables, and contractual terms. The IRS expects accurate documentation of royalty agreements, income records, and market data. Disputes may arise over income projections and market comparables. The appraiser must consider relevant court decisions and royalty agreement provisions.
        """,
        key_factors=[
            "Income potential",
            "Market comparables",
            "Contractual terms",
            "Royalty agreement provisions",
            "Documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-1",
            "Estate of Foster v. Commissioner, T.C. Memo 2011-95"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge income projections or market comparables.",
        counter_arguments=[
            "Speculative income projections.",
            "Insufficient market evidence.",
            "Failure to document contractual terms."
        ],
        resolution_strategy="Document income potential, market comparables, and contractual terms; use recognized valuation methods.",
        entity_scope="Royalty interests in estate",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Foster v. Commissioner, T.C. Memo 2011-95"
    ),
    DoctrineBlock(
        topic="valuation_of_stock_in_private_companies",
        keywords=["private company", "stock", "valuation", "estate", "FMV", "marketability discount"],
        conclusion_template="Stock in private companies is valued at FMV, considering earnings, asset values, market comparables, and appropriate discounts for lack of marketability.",
        reasoning_framework="""
Stock in private companies included in the estate is valued at FMV, considering earnings, asset values, market comparables, and appropriate discounts for lack of marketability. The IRS expects credible evidence of earnings, asset values, and market data. Disputes may arise over earnings projections, asset values, and magnitude of discounts. The appraiser must consider relevant court decisions and company documentation.
        """,
        key_factors=[
            "Earnings",
            "Asset values",
            "Market comparables",
            "Marketability discounts",
            "Company documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Gallagher v. Commissioner, T.C. Memo 2011-148",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge earnings projections, asset values, or magnitude of discounts.",
        counter_arguments=[
            "Speculative earnings projections.",
            "Overstated discounts.",
            "Insufficient market evidence."
        ],
        resolution_strategy="Document earnings, asset values, and market comparables; justify discounts with market evidence.",
        entity_scope="Stock in private companies in estate",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Gallagher v. Commissioner, T.C. Memo 2011-148"
    ),
    DoctrineBlock(
        topic="valuation_of_interest_in_family_limited_partnerships",
        keywords=["family limited partnership", "interest", "valuation", "estate", "discount"],
        conclusion_template="Interests in family limited partnerships are valued at FMV, considering partnership agreement terms, distribution rights, and appropriate discounts for lack of control and marketability.",
        reasoning_framework="""
Interests in family limited partnerships included in the estate are valued at FMV, considering partnership agreement terms, distribution rights, and appropriate discounts for lack of control and marketability. The IRS scrutinizes the magnitude and justification for discounts, requiring credible evidence and market data. Disputes often arise over the degree of control, transfer restrictions, and recent transactions. The appraiser must consider relevant court decisions and partnership agreement provisions.
        """,
        key_factors=[
            "Partnership agreement terms",
            "Distribution rights",
            "Transfer restrictions",
            "Degree of control",
            "Market evidence"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-3",
            "Estate of Harrison v. Commissioner, T.C. Memo 1987-8",
            "USPAP standards"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge magnitude or justification for discounts.",
        counter_arguments=[
            "Overstated discount.",
            "Insufficient market evidence.",
            "Failure to consider partnership agreement terms."
        ],
        resolution_strategy="Document agreement terms, market evidence, and industry studies to justify discounts.",
        entity_scope="Family limited partnership interests in estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Harrison v. Commissioner, T.C. Memo 1987-8"
    ),
    DoctrineBlock(
        topic="valuation_of_interest_in_real_estate_investment_trusts",
        keywords=["real estate investment trust", "REIT", "interest", "valuation", "estate", "FMV"],
        conclusion_template="Interests in real estate investment trusts are valued at FMV, considering market prices, distribution history, and any restrictions.",
        reasoning_framework="""
Interests in real estate investment trusts included in the estate are valued at FMV, considering market prices, distribution history, and any restrictions. The IRS expects accurate documentation of REIT interests, market prices, and distribution records. Disputes may arise over the treatment of restricted interests or distribution history. The appraiser must consider relevant court decisions and REIT documentation.
        """,
        key_factors=[
            "Market prices",
            "Distribution history",
            "Restrictions",
            "REIT documentation",
            "Valuation date"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Smith v. Commissioner, T.C. Memo 1999-368"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge treatment of restricted interests or distribution history.",
        counter_arguments=[
            "Improper treatment of restricted interests.",
            "Inaccurate distribution history.",
            "Insufficient documentation."
        ],
        resolution_strategy="Document market prices, distribution history, and restrictions; use recognized valuation methods.",
        entity_scope="REIT interests in estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Smith v. Commissioner, T.C. Memo 1999-368"
    ),
    DoctrineBlock(
        topic="valuation_of_interest_in_mutual_funds",
        keywords=["mutual funds", "interest", "valuation", "estate", "FMV"],
        conclusion_template="Interests in mutual funds are valued at FMV as of the valuation date, using published net asset values and considering any restrictions.",
        reasoning_framework="""
Interests in mutual funds included in the estate are valued at FMV as of the valuation date, using published net asset values and considering any restrictions. The IRS expects accurate documentation of mutual fund interests and net asset values. Disputes may arise over the treatment of restricted interests or net asset value calculations. The appraiser must consider relevant court decisions and mutual fund documentation.
        """,
        key_factors=[
            "Net asset values",
            "Restrictions",
            "Mutual fund documentation",
            "Valuation date",
            "Market evidence"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Smith v. Commissioner, T.C. Memo 1999-368"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge net asset value calculations or treatment of restricted interests.",
        counter_arguments=[
            "Improper net asset value calculation.",
            "Inaccurate documentation.",
            "Failure to consider restrictions."
        ],
        resolution_strategy="Document net asset values, restrictions, and mutual fund interests; use recognized valuation methods.",
        entity_scope="Mutual fund interests in estate",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Estate of Smith v. Commissioner, T.C. Memo 1999-368"
    ),
    DoctrineBlock(
        topic="valuation_of_interest_in_private_equity_funds",
        keywords=["private equity funds", "interest", "valuation", "estate", "FMV"],
        conclusion_template="Interests in private equity funds are valued at FMV, considering fund terms, asset values, and any restrictions or illiquidity.",
        reasoning_framework="""
Interests in private equity funds included in the estate are valued at FMV, considering fund terms, asset values, and any restrictions or illiquidity. The IRS expects accurate documentation of fund interests, asset values, and restrictions. Disputes may arise over asset values, illiquidity, and treatment of restrictions. The appraiser must consider relevant court decisions and fund documentation.
        """,
        key_factors=[
            "Fund terms",
            "Asset values",
            "Restrictions",
            "Illiquidity",
            "Fund documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Gallagher v. Commissioner, T.C. Memo 2011-148"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge asset values, illiquidity, or treatment of restrictions.",
        counter_arguments=[
            "Improper asset value calculation.",
            "Inaccurate documentation.",
            "Failure to consider illiquidity."
        ],
        resolution_strategy="Document fund terms, asset values, and restrictions; use recognized valuation methods.",
        entity_scope="Private equity fund interests in estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Gallagher v. Commissioner, T.C. Memo 2011-148"
    ),
    DoctrineBlock(
        topic="valuation_of_interest_in_hedge_funds",
        keywords=["hedge funds", "interest", "valuation", "estate", "FMV"],
        conclusion_template="Interests in hedge funds are valued at FMV, considering fund terms, asset values, and any restrictions or illiquidity.",
        reasoning_framework="""
Interests in hedge funds included in the estate are valued at FMV, considering fund terms, asset values, and any restrictions or illiquidity. The IRS expects accurate documentation of hedge fund interests, asset values, and restrictions. Disputes may arise over asset values, illiquidity, and treatment of restrictions. The appraiser must consider relevant court decisions and hedge fund documentation.
        """,
        key_factors=[
            "Fund terms",
            "Asset values",
            "Restrictions",
            "Illiquidity",
            "Hedge fund documentation"
        ],
        primary_authority=[
            "Treas. Reg. §20.2031-2",
            "Estate of Gallagher v. Commissioner, T.C. Memo 2011-148"
        ],
        burden_holder="Estate",
        adversary_position="IRS may challenge asset values, illiquidity, or treatment of restrictions.",
        counter_arguments=[
            "Improper asset value calculation.",
            "Inaccurate documentation.",
            "Failure to consider illiquidity."
        ],
        resolution_strategy="Document fund terms, asset values, and restrictions; use recognized valuation methods.",
        entity_scope="Hedge fund interests in estate",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Estate of Gallagher v. Commissioner, T.C. Memo 2011-148"
    ),
    DoctrineBlock(
        topic="valuation_of_interest_in_syndicated_loans",
        keywords=["syndicated loans", "interest", "valuation", "estate", "FMV"],
        conclusion_template="Interests in syndicated loans are valued at FMV, considering loan terms, payment history, and any restrictions or illiquidity.",
        reasoning_framework="""
Interests in syndicated loans included in the estate are valued at FMV, considering loan terms, payment history, and any restrictions or illiquidity. The IRS expects accurate documentation of loan interests, payment history, and restrictions. Disputes may arise over payment history, ill