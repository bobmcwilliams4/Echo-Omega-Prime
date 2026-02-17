"""
TX11 Nonprofit Tax — Doctrine Library
Pre-compiled expert reasoning blocks for nonprofit and tax-exempt organization intelligence.

Each DoctrineBlock contains real domain expertise:
- topic: canonical doctrine identifier
- keywords: 5-8 trigger terms for cache matching
- conclusion_template: 3-5 sentence expert summary
- reasoning_framework: 20-40 lines of analytical steps
- key_factors: 5+ determinative elements
- primary_authority: 3-5 citations (statutes, cases, regulations)
- burden_holder: who bears proof burden
- adversary_position: opposing argument
- counter_arguments: 5+ rebuttal points
- resolution_strategy: path to resolution
- entity_scope: affected parties
- confidence: DEFENSIBLE/AGGRESSIVE/DISCLOSURE/HIGH_RISK
- controlling_precedent: lead case or statute

Author: ECHO OMEGA PRIME
Engine: TX11 Nonprofit Tax
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class DoctrineBlock:
    """Single pre-compiled doctrine reasoning block."""
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
    entity_scope: List[str]
    confidence: str
    confidence_stratification: str
    controlling_precedent: str


# =============================================================================
# DOCTRINE BLOCK 1: IRC 501(c)(3) QUALIFICATION REQUIREMENTS
# =============================================================================
IRC_501C3_QUALIFICATION = DoctrineBlock(
    topic="irc_501c3_qualification",
    keywords=["501(c)(3)", "exempt status", "charitable", "educational", "religious", "organizational test", "operational test"],
    conclusion_template=(
        "IRC §501(c)(3) exempts from federal income tax organizations organized and operated exclusively for "
        "religious, charitable, scientific, testing for public safety, literary, or educational purposes, or to "
        "foster national or international amateur sports competition, or for the prevention of cruelty to children "
        "or animals. Qualification requires both the organizational test (articles of incorporation contain proper "
        "purpose and dissolution clauses) and the operational test (activities further exempt purposes and do not "
        "involve substantial non-exempt activities). No part of net earnings may inure to the benefit of private "
        "shareholders or individuals, and the organization may not engage in substantial lobbying or any political "
        "campaign intervention."
    ),
    reasoning_framework=(
        "Step 1: Review articles of incorporation for proper exempt purpose language under Treas. Reg. §1.501(c)(3)-1(b)(1)(i). "
        "Articles must limit purposes to one or more exempt purposes and contain a dissolution clause dedicating assets to another "
        "exempt organization or government upon dissolution.\n"
        "Step 2: Apply the organizational test. Articles must not expressly empower the organization to carry on substantial "
        "activities that do not further exempt purposes. State law implied powers are generally permissible if not actually exercised.\n"
        "Step 3: Apply the operational test under Treas. Reg. §1.501(c)(3)-1(c)(1). The organization must be operated primarily "
        "for exempt purposes. 'Primarily' means more than 50% of activities further exempt purposes, though IRS historically applies "
        "a more stringent 'substantially all' standard approaching 85%.\n"
        "Step 4: Assess the private benefit doctrine. Any private benefit must be incidental both qualitatively (a necessary "
        "concomitant of the exempt activity) and quantitatively (insubstantial relative to public benefit).\n"
        "Step 5: Apply the private inurement prohibition. Absolutely no net earnings may inure to insiders (founders, directors, "
        "officers, substantial contributors). Even a single dollar of inurement is disqualifying.\n"
        "Step 6: Evaluate lobbying activity under the 'no substantial part' test or IRC §501(h) election. Substantial lobbying "
        "activity (generally exceeding 5% of expenditures under IRS historical practice) jeopardizes exemption. The §501(h) safe "
        "harbor provides precise percentage limits based on exempt purpose expenditures.\n"
        "Step 7: Apply the absolute prohibition on political campaign intervention under IRC §501(c)(3). Any direct or indirect "
        "participation in political campaigns for or against candidates for public office is prohibited. Issue advocacy is permissible "
        "if nonpartisan.\n"
        "Step 8: Consider the commensurate test. The organization's activities must be commensurate in scope with its financial "
        "resources. Accumulation of resources without corresponding charitable activities raises operational test issues."
    ),
    key_factors=[
        "Whether articles of incorporation contain proper purpose and dissolution clauses",
        "Percentage of activities and expenditures devoted to exempt versus non-exempt purposes",
        "Existence and magnitude of private benefit to individuals or entities",
        "Whether any net earnings inure to insiders (founders, directors, officers)",
        "Extent of lobbying activity relative to total activities and expenditures",
        "Whether organization engages in any political campaign intervention",
        "Whether programs and activities are commensurate in scope with financial resources",
        "Whether organization maintains arm's-length transactions with related parties",
    ],
    primary_authority=[
        "IRC §501(c)(3)",
        "Treas. Reg. §1.501(c)(3)-1",
        "Rev. Rul. 2007-41 (private benefit doctrine)",
        "Taxation With Representation v. Regan, 461 U.S. 540 (1983) (lobbying limitation)",
        "Branch Ministries v. Rossotti, 211 F.3d 137 (D.C. Cir. 2000) (political intervention prohibition)",
    ],
    burden_holder="Applicant organization bears burden to establish entitlement to exemption",
    adversary_position=(
        "IRS Exempt Organizations division argues that organizations operating commercial activities (fitness centers, "
        "gift shops, restaurants) fail the operational test because commercial activities are not inherently charitable "
        "even if profits are used for exempt purposes. They contend that the 'destination of income' test is insufficient "
        "and the nature of activities themselves must be charitable."
    ),
    counter_arguments=[
        "Treas. Reg. §1.501(c)(3)-1(e) expressly permits exempt organizations to operate a trade or business if substantially related to exempt purposes",
        "Better Business Bureau v. United States, 326 U.S. 279 (1945) establishes that an organization may qualify even if operated in a commercial manner, provided the business activity itself accomplishes exempt purposes",
        "The commensurate test focuses on whether programs match resources, not on the commercial nature of revenue-generating activities",
        "Rev. Rul. 69-545 (hospital gift shop), Rev. Rul. 69-267 (museum food service), and similar rulings permit commercial activities as incidental fundraising",
        "IRC §513 and UBIT provisions presuppose that exempt organizations can operate businesses; otherwise UBIT would be unnecessary",
    ],
    resolution_strategy=(
        "Document that primary activities directly accomplish exempt purposes. If commercial activities exist, establish "
        "they are either substantially related to exempt purposes under IRC §513 or are insubstantial (less than 15% of "
        "total activities). Structure compensation arrangements to ensure arm's-length terms and avoid private inurement. "
        "Adopt conflict of interest policy. Quantify lobbying expenditures and consider IRC §501(h) election for certainty. "
        "Maintain absolute prohibition on political campaign intervention through board policies and staff training."
    ),
    entity_scope=["501(c)(3) applicants", "501(c)(3) organizations", "donors", "IRS Exempt Organizations"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC §501(c)(3) and Treas. Reg. §1.501(c)(3)-1",
)


# =============================================================================
# DOCTRINE BLOCK 2: UNRELATED BUSINESS INCOME TAX (UBIT)
# =============================================================================
UBIT_FRAMEWORK = DoctrineBlock(
    topic="ubit_framework",
    keywords=["ubit", "unrelated business income", "512", "513", "514", "trade or business", "regularly carried on"],
    conclusion_template=(
        "IRC §§511-514 impose unrelated business income tax (UBIT) on the net income of tax-exempt organizations "
        "derived from regularly carried on trades or businesses that are not substantially related to exempt purposes. "
        "Three requirements must be met: (1) trade or business activity, (2) regularly carried on, and (3) not substantially "
        "related to exempt purposes. Numerous statutory exceptions exist under IRC §512(b) including dividends, interest, "
        "royalties, most rents from real property, and gains from sale of property. Modifications and deductions under "
        "IRC §512(a) result in unrelated business taxable income (UBTI), taxed at corporate rates under IRC §511."
    ),
    reasoning_framework=(
        "Step 1: Determine whether activity constitutes a 'trade or business' under IRC §513(c). An activity is a trade or "
        "business if it is carried on for the production of income from the sale of goods or performance of services. The "
        "activity must involve considerable effort and the relationship between gross receipts and expenses must be commercial.\n"
        "Step 2: Assess whether the activity is 'regularly carried on' under Treas. Reg. §1.513-1(c). Frequency and continuity "
        "of activities are compared to commercial equivalents. Seasonal activities are evaluated within their appropriate season. "
        "Intermittent or sporadic activities generally do not meet the regularly carried on test.\n"
        "Step 3: Evaluate whether the activity is 'substantially related' to exempt purposes under IRC §513(a) and Treas. Reg. "
        "§1.513-1(d). The activity must contribute importantly to accomplishment of exempt purposes, beyond merely generating funds. "
        "The conduct of the activity itself must have a causal relationship to exempt purposes and must be more than incidental.\n"
        "Step 4: Check for statutory exceptions under IRC §512(b). Excluded items include: passive investment income (dividends, "
        "interest, annuities), royalties, most rents from real property (unless debt-financed or with personal services), gains from "
        "disposition of property, income from research, income from businesses operated by volunteers, income from selling donated "
        "merchandise, income from certain bingo games, and income from distribution of low-cost articles with fundraising solicitations.\n"
        "Step 5: If activity generates UBI, compute UBTI under IRC §512(a). Start with gross income from unrelated trade or business, "
        "subtract directly connected expenses, apply the $1,000 specific deduction, and make required modifications (add back exempt "
        "function income, subtract passive income already excluded under §512(b)).\n"
        "Step 6: Consider debt-financed property rules under IRC §514. Income from property acquired with debt (acquisition indebtedness) "
        "is treated as UBI in proportion to debt financing, even if the income would otherwise be excluded (e.g., rents, dividends).\n"
        "Step 7: Aggregate all unrelated businesses for net operating loss purposes, but calculate UBTI separately for each unrelated "
        "trade or business to prevent cross-subsidization (TCJA §512(a)(6) siloing rule effective 2018).\n"
        "Step 8: File Form 990-T if gross UBI exceeds $1,000. Pay estimated taxes if UBIT liability expected to exceed $500."
    ),
    key_factors=[
        "Whether activity involves sale of goods or performance of services with profit motive",
        "Frequency and continuity of activity compared to commercial equivalents",
        "Whether activity contributes importantly to exempt purposes beyond fundraising",
        "Presence of volunteers in conducting the business (volunteer exception)",
        "Whether inventory consists of donated merchandise (donated goods exception)",
        "Extent of debt-financed property and percentage of acquisition indebtedness",
        "Whether activity falls within statutory exceptions (passive income, research, etc.)",
        "Profit margin and commercial character of operations",
    ],
    primary_authority=[
        "IRC §§511-514 (UBIT provisions)",
        "Treas. Reg. §1.513-1 (substantially related test)",
        "Treas. Reg. §1.514-1 (debt-financed property)",
        "Trinidad v. Sagrada Orden, 263 U.S. 578 (1924) (trade or business definition)",
        "Rev. Rul. 2000-12 (corporate sponsorship payments as royalties)",
    ],
    burden_holder="Exempt organization bears burden to establish exception or exclusion applicability",
    adversary_position=(
        "IRS argues that many museum gift shops, hospital pharmacies, and university food services constitute UBI because "
        "they are commercial activities conducted in competition with taxpaying businesses. The mere fact that profits are "
        "used for exempt purposes is irrelevant; the activity itself must accomplish exempt purposes. IRS contends the "
        "substantially related test requires more than a 'destination of income' analysis."
    ),
    counter_arguments=[
        "Educational organizations' sale of publications and materials related to their educational mission is substantially related (Treas. Reg. §1.513-1(d)(4)(iv))",
        "Museum gift shops selling reproductions of works in the museum's collection contribute to educational purposes (Rev. Rul. 73-104)",
        "Hospital pharmacies serving only patients and staff are substantially related to healthcare purposes (Rev. Rul. 68-374)",
        "The fragmentation rule allows separating substantially related activities from unrelated activities within the same business",
        "Volunteer exception under IRC §512(b)(4) applies if substantially all work is performed by volunteers, regardless of competition with commercial businesses",
    ],
    resolution_strategy=(
        "Document the relationship between the business activity and exempt purposes with evidence that the activity directly "
        "accomplishes exempt functions. Maximize use of volunteers to qualify for the volunteer exception. Separate donated "
        "merchandise sales to invoke the donated goods exception. Structure vendor relationships as royalties (passive payments "
        "tied to sales) rather than joint venture participation. Minimize debt financing to avoid IRC §514 inclusion. If UBTI "
        "is unavoidable, properly allocate expenses and maintain separate accounting for each unrelated business under the siloing rules."
    ),
    entity_scope=["501(c)(3) organizations", "501(c) exempt organizations", "IRS Exempt Organizations", "taxpaying competitors"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC §513 and Treas. Reg. §1.513-1",
)


# =============================================================================
# DOCTRINE BLOCK 3: PRIVATE FOUNDATION vs PUBLIC CHARITY (IRC 509(a))
# =============================================================================
PUBLIC_CHARITY_CLASSIFICATION = DoctrineBlock(
    topic="public_charity_classification",
    keywords=["509(a)", "public charity", "private foundation", "public support", "33 1/3 percent test", "facts and circumstances"],
    conclusion_template=(
        "IRC §509(a) classifies exempt organizations as either public charities or private foundations. Public charities "
        "under §509(a)(1) include churches, schools, hospitals, and organizations receiving substantial public support. "
        "Public support organizations under §509(a)(2) derive more than one-third of support from contributions, grants, "
        "and program service revenue. Supporting organizations under §509(a)(3) are operated in connection with one or more "
        "supported public charities. All other §501(c)(3) organizations are private foundations subject to restrictive rules "
        "under IRC §§4940-4945, including excise taxes on investment income, self-dealing, excess business holdings, jeopardizing "
        "investments, and taxable expenditures."
    ),
    reasoning_framework=(
        "Step 1: Identify the type of organization. Churches, schools, hospitals, medical research organizations, governmental "
        "units, and publicly supported organizations described in IRC §170(b)(1)(A)(i)-(vi) automatically qualify as public charities "
        "under §509(a)(1) without mathematical testing.\n"
        "Step 2: For organizations relying on public support, apply the IRC §509(a)(1) one-third support test. Calculate public "
        "support as contributions and grants from the general public, plus grants from public charities and governmental units, "
        "divided by total support. Must exceed 33 1/3% over a 4-year measuring period. Donations from any single donor exceeding "
        "2% of total support during the period are capped at the 2% threshold.\n"
        "Step 3: If the one-third test is not met but public support exceeds 10%, consider the facts and circumstances test under "
        "Treas. Reg. §1.170A-9(f)(3). Evaluate percentage of public support, sources of support, representativeness of governing "
        "board, availability of facilities to the public, and membership structure.\n"
        "Step 4: For service provider organizations (museums, symphonies, theaters), consider IRC §509(a)(2) classification. Calculate "
        "public support as contributions plus program service revenue (capped at greater of $5,000 or 1% of support from any single "
        "source) divided by total support. Must exceed 33 1/3%. Additionally, gross investment income and UBI must not exceed 33 1/3% "
        "of support.\n"
        "Step 5: For supporting organizations, verify the organization meets one of three relationship types under IRC §509(a)(3): "
        "Type I (operated, supervised, or controlled by), Type II (supervised or controlled in connection with), or Type III (operated "
        "in connection with). Type III must be either functionally integrated or pass the responsiveness and integral part tests.\n"
        "Step 6: If private foundation classification applies, determine which excise taxes are triggered: §4940 (2% tax on net "
        "investment income, reduced to 1% if distributions meet historical average), §4941 (self-dealing), §4942 (minimum distribution "
        "requirement of 5% of investment assets), §4943 (excess business holdings exceeding 20%), §4944 (jeopardizing investments), "
        "§4945 (taxable expenditures including lobbying and grants to individuals without IRS approval).\n"
        "Step 7: Evaluate termination of private foundation status through expenditure responsibility grants, transfer to public charity, "
        "or §507(b)(1)(B) 60-month termination by meeting public charity tests and distributing assets."
    ),
    key_factors=[
        "Whether organization qualifies as church, school, hospital, or other per se public charity",
        "Percentage of support from general public, government, and other public charities",
        "Number and diversity of donors (more donors with smaller gifts supports public charity status)",
        "Whether any donor provides more than 2% of total support over measuring period",
        "Percentage of support from program service revenue vs. investment income",
        "For supporting organizations, the nature and extent of relationship with supported organizations",
        "Composition of governing board (independent vs. insider control)",
        "Whether organization provides facilities or services to the general public",
    ],
    primary_authority=[
        "IRC §509(a)(1)-(3) (public charity definitions)",
        "IRC §170(b)(1)(A) (types of public charities)",
        "Treas. Reg. §1.170A-9(f) (public support tests)",
        "IRC §§4940-4945 (private foundation excise taxes)",
        "Treas. Reg. §1.509(a)-4 (supporting organizations)",
    ],
    burden_holder="Organization bears burden to establish public charity status; private foundation is default classification",
    adversary_position=(
        "IRS argues that supporting organizations classified as Type III non-functionally integrated have been abused as "
        "alternative donor-advised funds without the restrictions of §4966-4967. Pension Protection Act of 2006 added strict "
        "requirements for Type III supporting organizations including responsiveness test (timely communication with supported "
        "organization) and integral part test (attentiveness to supported organization's needs and substantial support provided). "
        "IRS contends these organizations should be subject to private foundation rules if they fail heightened tests."
    ),
    counter_arguments=[
        "Type III functionally integrated supporting organizations remain permissible without additional restrictions beyond historical requirements",
        "The facts and circumstances test provides flexibility for organizations with 10-33 1/3% public support if they demonstrate public charity characteristics",
        "IRC §509(a)(2) public support test includes program service revenue, benefiting museums and performing arts organizations",
        "The 2% cap applies to unusual grants under Treas. Reg. §1.170A-9(f)(6), allowing exclusion of one-time major gifts in appropriate circumstances",
        "Supporting organizations provide valuable services to public charities including permanent endowments and shared administrative services",
    ],
    resolution_strategy=(
        "Maximize number and diversity of donors to build cushion above one-third threshold. Seek government grants and grants "
        "from other public charities (not subject to 2% cap under §509(a)(1)). Develop earned income from program services to "
        "strengthen §509(a)(2) case. For supporting organizations, document organizational relationship through overlapping boards "
        "(Type I), common supervision (Type II), or responsiveness and support (Type III). If private foundation classification "
        "is unavoidable, structure investments and distributions to minimize excise taxes and establish expenditure responsibility "
        "procedures for grants."
    ),
    entity_scope=["501(c)(3) organizations", "donors", "supported organizations", "IRS Exempt Organizations"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC §509(a) and Treas. Reg. §1.170A-9",
)


# =============================================================================
# DOCTRINE BLOCK 4: INTERMEDIATE SANCTIONS (IRC 4958)
# =============================================================================
INTERMEDIATE_SANCTIONS = DoctrineBlock(
    topic="intermediate_sanctions_4958",
    keywords=["4958", "excess benefit", "disqualified person", "reasonable compensation", "rebuttable presumption"],
    conclusion_template=(
        "IRC §4958 imposes excise taxes on excess benefit transactions between applicable tax-exempt organizations and "
        "disqualified persons. An excess benefit transaction occurs when a disqualified person receives economic benefit "
        "exceeding the value of consideration provided in return. The initial tax is 25% of the excess benefit imposed on "
        "the disqualified person, and organization managers who knowingly participate face a 10% tax (capped at $20,000). "
        "If not corrected, an additional 200% tax applies. Rebuttable presumption of reasonableness arises if compensation "
        "is approved by independent board members after appropriate comparability data review with concurrent documentation."
    ),
    reasoning_framework=(
        "Step 1: Identify whether the organization is an 'applicable tax-exempt organization' under IRC §4958(e). This includes "
        "§501(c)(3) and §501(c)(4) organizations but not private foundations (already subject to self-dealing rules under §4941).\n"
        "Step 2: Determine whether the individual is a 'disqualified person' under IRC §4958(f)(1). This includes: (a) persons in "
        "position to exercise substantial influence over the organization's affairs at any time during the 5-year lookback period, "
        "(b) family members of disqualified persons, and (c) entities controlled 35% or more by disqualified persons. Treas. Reg. "
        "§53.4958-3 provides facts and circumstances test for substantial influence, with per se categories for voting directors, "
        "presidents, CEOs, CFOs, and treasurers.\n"
        "Step 3: Identify the economic benefit provided. This includes compensation, expense reimbursements, loans below market "
        "interest rates, sale or lease of property, provision of services, and any other transfer of value to the disqualified person "
        "or family member.\n"
        "Step 4: Determine the value of consideration provided in return. For compensation, this is the value of services rendered. "
        "For property transactions, this is fair market value. The excess benefit is the amount by which economic benefit exceeds "
        "the value of consideration.\n"
        "Step 5: Assess whether rebuttable presumption of reasonableness applies under Treas. Reg. §53.4958-6. Three requirements: "
        "(1) approved by authorized body composed entirely of individuals without conflict of interest, (2) authorized body obtained "
        "and relied upon appropriate comparability data before making determination, and (3) authorized body adequately documented "
        "basis for determination concurrently with decision.\n"
        "Step 6: Evaluate comparability data used. Acceptable data includes compensation levels paid by similarly situated organizations "
        "for functionally comparable positions, independent compensation surveys compiled by third parties, and actual written offers "
        "from similar organizations. Data must be recent (generally within 3 years) and relevant to the exempt organization's "
        "circumstances (size, location, industry).\n"
        "Step 7: Calculate the excess benefit and resulting excise taxes. Initial 25% tax on disqualified person, 10% tax on managers "
        "who knowingly participated (capped at $20,000 per transaction), and additional 200% tax if not corrected within taxable period.\n"
        "Step 8: Determine correction method. Correction requires disqualified person to repay the excess benefit plus interest to the "
        "organization, but not necessarily undo the entire transaction if doing so would not be economically feasible."
    ),
    key_factors=[
        "Whether individual holds title of director, officer, or key employee",
        "Whether individual has authority to control significant organizational resources or activities",
        "Existence and composition of independent compensation committee or board",
        "Quality and recency of comparability data used in compensation decision",
        "Whether comparability analysis and decision were documented contemporaneously",
        "Magnitude of excess benefit relative to reasonable compensation range",
        "Whether transaction involved family members or controlled entities",
        "Whether disqualified person or managers knew or should have known the transaction was improper",
    ],
    primary_authority=[
        "IRC §4958 (excess benefit transactions)",
        "Treas. Reg. §53.4958-1 through §53.4958-8",
        "Treas. Reg. §53.4958-6 (rebuttable presumption of reasonableness)",
        "IRS Notice 2007-78 (interim guidance on §4958)",
        "Rev. Proc. 2011-14 (disaster relief payments)",
    ],
    burden_holder="IRS bears burden to establish excess benefit transaction occurred; organization can rebut with presumption evidence",
    adversary_position=(
        "IRS Exempt Organizations division argues that many compensation arrangements for executives of large nonprofit health "
        "systems and universities constitute excess benefits because compensation exceeds reasonable amounts for the services "
        "rendered. They contend that comparability data from for-profit corporations is not appropriate for tax-exempt organizations "
        "because exempt organizations do not have the same market pressures or shareholder accountability. IRS asserts that lavish "
        "perquisites (country club memberships, first-class travel, luxury vehicles) are per se unreasonable regardless of comparability data."
    ),
    counter_arguments=[
        "Treas. Reg. §53.4958-4(b)(1)(ii)(A) expressly permits use of compensation data from both taxable and tax-exempt organizations in similar communities and with similar missions",
        "Rebuttable presumption of reasonableness applies if proper procedures are followed, shifting burden to IRS to overcome presumption",
        "Executive talent market is competitive across taxable and exempt sectors; exempt organizations must compete for qualified executives",
        "Courts have upheld substantial compensation packages where independent board followed proper procedures (e.g., Caracci v. Commissioner, 118 T.C. 379 (2002))",
        "Perquisites common in the industry and included in comparability data are permissible as ordinary and necessary business expenses",
    ],
    resolution_strategy=(
        "Establish independent compensation committee of board members without conflicts. Retain independent compensation consultant "
        "to provide comparability data from multiple sources including nonprofit compensation surveys (e.g., Guidestar, ERI). Document "
        "committee deliberations with detailed minutes describing data sources, methodology, and rationale for decisions. Prepare "
        "contemporaneous written record including comparability data relied upon. Review and approve all transactions with disqualified "
        "persons using same procedures. Adopt conflict of interest policy requiring disclosure and recusal. If excess benefit is "
        "identified, correct immediately to avoid additional 200% tax."
    ),
    entity_scope=["501(c)(3) and 501(c)(4) organizations", "directors", "officers", "key employees", "substantial contributors"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC §4958 and Treas. Reg. §53.4958-6",
)


# =============================================================================
# DOCTRINE BLOCK 5: POLITICAL CAMPAIGN INTERVENTION PROHIBITION
# =============================================================================
POLITICAL_CAMPAIGN_PROHIBITION = DoctrineBlock(
    topic="political_campaign_prohibition",
    keywords=["political campaign", "501(c)(3)", "intervention", "candidate", "election", "partisan"],
    conclusion_template=(
        "IRC §501(c)(3) contains an absolute prohibition on participation or intervention in political campaigns on behalf "
        "of or in opposition to candidates for public office. Any political campaign intervention, direct or indirect, jeopardizes "
        "exempt status. The prohibition applies to all forms of communication and activity including contributions, endorsements, "
        "distribution of campaign literature, statements by organization officials in official capacity, invitations to speak at "
        "events, voter guides that show bias, and rental of facilities on preferential terms. Nonpartisan voter education activities "
        "including candidate forums, voter registration, and issue advocacy are permissible if conducted without bias."
    ),
    reasoning_framework=(
        "Step 1: Identify whether the communication or activity relates to a candidate for public office. The prohibition applies "
        "to federal, state, and local elections. 'Candidate' includes individuals who have publicly announced candidacy or are "
        "widely recognized as candidates even without formal announcement.\n"
        "Step 2: Determine whether the activity constitutes 'intervention' or 'participation' in the campaign. Prohibited activities "
        "include: contributions to campaign funds or public statements of position in favor of or in opposition to a candidate, "
        "publishing or distributing statements on behalf of or in opposition to a candidate, allowing use of organization's assets "
        "or facilities for campaign purposes, and communications that identify a candidate and express approval or disapproval.\n"
        "Step 3: Apply the facts and circumstances test under Rev. Rul. 2007-41. Factors indicating political campaign intervention "
        "include: whether the communication identifies a candidate, whether timing coincides with campaign, whether the issue is subject "
        "of political debate distinguishing candidates, whether the communication is part of ongoing series or one-time event, whether "
        "other candidates are given equivalent opportunities, and overall context of the communication.\n"
        "Step 4: Assess individual actions by organization officials. Individuals who are officers, directors, or spokespersons may "
        "engage in political activity in individual capacity if: (a) clearly state they are not speaking on behalf of organization, "
        "(b) do not use organization resources, facilities, or letterhead, and (c) their position with organization is not identified "
        "or is identified only in passing.\n"
        "Step 5: Evaluate nonpartisan activities. Permissible activities include: voter registration and get-out-the-vote drives "
        "conducted in nonpartisan manner, candidate forums where all viable candidates are invited and questions are neutral, voter "
        "guides presenting all candidates' views on range of issues without editorial comment, and issue advocacy that does not identify "
        "candidates or show bias toward candidates.\n"
        "Step 6: Consider use of facilities. Rental of facilities to candidates is permissible if: available to all candidates on equal "
        "terms, charged at fair market value, and not timed to give undue advantage to one candidate.\n"
        "Step 7: Assess consequences of violation. Political campaign intervention results in: (a) revocation of exempt status, or "
        "(b) excise tax under IRC §4955 equal to 10% of expenditure on organization and 2.5% on managers who knowingly participated. "
        "There is no de minimis exception; even a single instance can be disqualifying.\n"
        "Step 8: Implement safeguards including written policy prohibiting political intervention, training for staff and board, "
        "pre-clearance procedures for communications during election seasons, and legal review of borderline activities."
    ),
    key_factors=[
        "Whether communication identifies a candidate for public office by name or clear reference",
        "Timing of communication relative to election and campaign cycle",
        "Whether the issue addressed is a subject distinguishing candidates in the campaign",
        "Whether communication expresses approval or disapproval of candidate explicitly or implicitly",
        "Whether organization provides equal opportunity to all candidates or shows bias",
        "Whether individual statements are made in official capacity or personal capacity",
        "Whether organization resources (funds, facilities, staff time) are used for political purposes",
        "Past pattern of similar communications and overall context",
    ],
    primary_authority=[
        "IRC §501(c)(3) (political campaign intervention prohibition)",
        "IRC §4955 (excise tax on political expenditures)",
        "Treas. Reg. §1.501(c)(3)-1(c)(3)(iii)",
        "Rev. Rul. 2007-41 (facts and circumstances test)",
        "Branch Ministries v. Rossotti, 211 F.3d 137 (D.C. Cir. 2000) (full-page newspaper ad opposing candidate)",
    ],
    burden_holder="Organization bears burden to avoid political intervention; IRS must prove intervention to impose tax or revoke status",
    adversary_position=(
        "IRS argues that churches and religious organizations that permit candidates to speak at services, publish voter guides "
        "that show clear bias, or make statements from the pulpit regarding candidate positions on issues such as abortion or "
        "same-sex marriage constitute prohibited political intervention. They contend the Johnson Amendment (adding political "
        "prohibition in 1954) is constitutionally valid and does not violate free speech or free exercise rights."
    ),
    counter_arguments=[
        "Churches may invite candidates to speak in non-candidate capacity (e.g., as government official) if no campaigning occurs and all candidates invited",
        "Issue advocacy on moral issues (abortion, marriage, war) is protected if it does not identify candidates or urge votes for/against them",
        "Candidate forums are permissible if all viable candidates invited, questions neutral, and equal time provided",
        "Individual clergy statements in personal capacity outside of services are protected speech not attributable to organization",
        "First Amendment protections for religious speech are heightened; complete prohibition may be unconstitutional overreach (though no court has so held)",
    ],
    resolution_strategy=(
        "Adopt and enforce strict policy prohibiting political campaign intervention. Train staff and board on prohibition including "
        "examples and case studies. Establish pre-clearance process for all communications during election seasons with legal counsel "
        "review. Document that candidate appearances are in non-candidate capacity and all candidates invited. Limit endorsements and "
        "partisan statements to purely personal capacity with clear disclaimers. Focus on nonpartisan issue advocacy without identifying "
        "candidates. If violation occurs, immediately disavow, correct, and document remedial steps to avoid future violations."
    ),
    entity_scope=["501(c)(3) organizations", "directors", "officers", "employees", "candidates", "IRS Exempt Organizations"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC §501(c)(3) and Branch Ministries v. Rossotti, 211 F.3d 137 (D.C. Cir. 2000)",
)


# =============================================================================
# DOCTRINE BLOCK 6: DONOR-ADVISED FUNDS (IRC 4966-4967)
# =============================================================================
DONOR_ADVISED_FUNDS = DoctrineBlock(
    topic="donor_advised_funds",
    keywords=["donor-advised fund", "daf", "4966", "4967", "sponsoring organization", "advisory privileges"],
    conclusion_template=(
        "IRC §4966-4967, enacted by Pension Protection Act of 2006, regulate donor-advised funds (DAFs). A DAF is a fund or "
        "account separately identified by reference to contributions of a donor or donors, where the donor has advisory privileges "
        "regarding distributions or investments. Excess benefit transactions under §4958 apply with extended 5-year lookback for "
        "DAF donors. IRC §4967 imposes excise taxes on prohibited benefits to donors and taxable distributions to non-charitable "
        "recipients. Sponsoring organizations must maintain adequate controls and reporting. DAF donors do not have legally "
        "enforceable rights to direct distributions; advisory privileges must remain advisory only."
    ),
    reasoning_framework=(
        "Step 1: Determine whether a fund constitutes a donor-advised fund under IRC §4966(d)(2). Three elements: (1) separately "
        "identified by reference to donor contributions, (2) owned and controlled by sponsoring organization (§501(c)(3) public charity), "
        "and (3) donor or donor advisor has advisory privileges regarding distributions or investments.\n"
        "Step 2: Identify the sponsoring organization under IRC §4966(d)(1). Must be a §501(c)(3) organization specifically maintaining "
        "donor-advised funds. Community foundations, religious organizations with DAF programs, and commercial DAF providers (Fidelity "
        "Charitable, Schwab Charitable) are common sponsoring organizations.\n"
        "Step 3: Evaluate donor advisory privileges. Treas. Reg. §53.4966-1(b) defines 'advisory privileges' as the privilege to provide "
        "nonbinding advice regarding distributions or investments. The sponsoring organization must retain ultimate control; donor cannot "
        "have legally enforceable rights to distributions. If donor has legal ownership or enforceable rights, the fund is not a DAF but "
        "may be a private foundation or split-interest trust.\n"
        "Step 4: Apply excess benefit transaction rules under IRC §4958 as modified by §4967(a). Donors and donor advisors to DAFs are "
        "automatically disqualified persons. Lookback period is extended to 5 years (vs. general 1-year for §4958). Any grant or benefit "
        "to donor, donor advisor, or related persons is presumed to be an excess benefit unless the sponsoring organization demonstrates "
        "it is exclusively for charitable purposes.\n"
        "Step 5: Identify prohibited benefits under IRC §4967. These include: goods, services, or facilities provided to donor or related "
        "persons (other than incidental benefits available to general public), and payment of compensation to donor or related persons.\n"
        "Step 6: Assess taxable distributions under IRC §4966(c). A distribution from a DAF to a natural person or to an organization "
        "not described in IRC §170(b)(1)(A) (i.e., not a public charity) is a taxable distribution subject to excise taxes. Distributions "
        "to private foundations are taxable unless the DAF conducts expenditure responsibility.\n"
        "Step 7: Calculate excise taxes. IRC §4967 imposes 125% tax on donor/advisor who advised the distribution and 10% tax on fund "
        "manager who agreed to the prohibited benefit or taxable distribution knowing it was such. If not corrected, an additional 100% "
        "tax applies to donor/advisor.\n"
        "Step 8: Evaluate exceptions. Certain grants are permissible including: disaster relief payments meeting requirements of Rev. "
        "Proc. 2007-50, scholarship grants if DAF is functionally integrated, and grants to foreign charities after equivalency determination."
    ),
    key_factors=[
        "Whether fund is separately identified by reference to donor contributions",
        "Whether sponsoring organization retains ultimate legal control over assets",
        "Whether donor has advisory (nonbinding) vs. directive (binding) authority",
        "Whether proposed distribution is to a public charity under IRC §170(b)(1)(A)",
        "Whether any benefits are provided to donor or related persons",
        "Whether compensation is paid to donor, advisor, or family members",
        "Whether distribution is for bona fide charitable purpose vs. personal benefit",
        "Whether sponsoring organization has adequate controls and variance power",
    ],
    primary_authority=[
        "IRC §4966 (taxable distributions from donor-advised funds)",
        "IRC §4967 (prohibited benefits from donor-advised funds)",
        "IRC §4958 (excess benefit transactions applicable to DAFs)",
        "Treas. Reg. §53.4966-1 through §53.4966-4",
        "Rev. Proc. 2007-50 (disaster relief from DAFs)",
    ],
    burden_holder="Sponsoring organization bears burden to demonstrate distributions are exclusively charitable; donors have no legally enforceable rights",
    adversary_position=(
        "IRS and policy critics argue that DAFs have become substitutes for private foundations without the required 5% annual "
        "distribution or public disclosure. Donors get immediate tax deduction but can delay grants indefinitely, warehousing charitable "
        "assets. IRS contends that recommendations from donors should be scrutinized carefully and sponsoring organizations should reject "
        "recommendations involving personal benefit, satisfaction of pledges, payment of tuition, or support of entities controlled by donors."
    ),
    counter_arguments=[
        "DAFs democratize philanthropy by providing access to sophisticated charitable giving tools at lower cost than private foundations",
        "Sponsoring organizations do enforce variance power and reject inappropriate recommendations as required by regulations",
        "DAF distribution rates (20-25% annually for many sponsors) exceed private foundation 5% requirement in practice",
        "Immediate tax deduction is justified because donor relinquishes legal control; economic reality is transfer to charity",
        "DAFs promote strategic giving by allowing donors time to research and evaluate charities before making grants",
    ],
    resolution_strategy=(
        "Sponsoring organizations must adopt and enforce policies including: (1) variance power clause reserving right to redirect "
        "assets if donor recommendation is not charitable, (2) prohibition on benefits to donors and related persons, (3) restriction "
        "of distributions to public charities and pre-approved recipients, (4) expenditure responsibility procedures for private "
        "foundation grants, (5) rejection of recommendations satisfying personal pledges unless independent charitable purpose exists, "
        "and (6) training for staff on prohibited benefits and taxable distributions. Donors should understand advisory privileges are "
        "nonbinding and sponsoring organization has final authority."
    ),
    entity_scope=["Sponsoring organizations", "donors", "donor advisors", "DAF recipients", "IRS Exempt Organizations"],
    confidence="DEFENSIBLE",
    confidence_stratification="DEFENSIBLE",
    controlling_precedent="IRC §§4966-4967 and Treas. Reg. §53.4966-1",
)


# =============================================================================
# DOCTRINE INTERACTIONS
# =============================================================================

# List of doctrine interaction edges showing how doctrines relate to each other
DOCTRINE_INTERACTIONS: List[Tuple[str, str, str]] = [
    ("irc_501c3_qualification", "ubit_framework", "Unrelated business income can jeopardize exempt status if substantial"),
    ("irc_501c3_qualification", "intermediate_sanctions_4958", "Private inurement prohibition enforced through §4958 excess benefit taxes"),
    ("irc_501c3_qualification", "political_campaign_prohibition", "Political intervention is absolute disqualifier under §501(c)(3)"),
    ("public_charity_classification", "donor_advised_funds", "DAFs must be sponsored by public charities, not private foundations"),
    ("intermediate_sanctions_4958", "donor_advised_funds", "DAF donors are automatically disqualified persons for §4958 purposes"),
    ("ubit_framework", "public_charity_classification", "UBIT and gross investment income affect §509(a)(2) public support calculation"),
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

ALL_DOCTRINES: List[DoctrineBlock] = [
    IRC_501C3_QUALIFICATION,
    UBIT_FRAMEWORK,
    PUBLIC_CHARITY_CLASSIFICATION,
    INTERMEDIATE_SANCTIONS,
    POLITICAL_CAMPAIGN_PROHIBITION,
    DONOR_ADVISED_FUNDS,
]


def get_all_doctrines() -> List[DoctrineBlock]:
    """Return all doctrine blocks."""
    return ALL_DOCTRINES


def get_doctrine_count() -> int:
    """Return total doctrine count."""
    return len(ALL_DOCTRINES)


def get_doctrine_topics() -> List[str]:
    """Return list of all doctrine topics."""
    return [d.topic for d in ALL_DOCTRINES]


def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    """Retrieve doctrine block by topic."""
    for doctrine in ALL_DOCTRINES:
        if doctrine.topic == topic:
            return doctrine
    return None


def search_doctrines(query: str, max_results: int = 3) -> List[DoctrineBlock]:
    """Search doctrines by keyword matching."""
    query_lower = query.lower()
    results = []

    for doctrine in ALL_DOCTRINES:
        # Check if any keyword appears in query
        matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
        if matches > 0:
            results.append((doctrine, matches))

    # Sort by match count descending
    results.sort(key=lambda x: x[1], reverse=True)

    return [d for d, _ in results[:max_results]]


def get_interaction_edges() -> List[Tuple[str, str, str]]:
    """Return doctrine interaction edges."""
    return DOCTRINE_INTERACTIONS
