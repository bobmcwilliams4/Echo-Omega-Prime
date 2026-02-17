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
        topic="S-Corporation Reasonable Compensation",
        keywords=["S-Corp", "reasonable compensation", "salary", "shareholder", "IRS"],
        conclusion_template="Determine if the compensation paid to S-Corporation shareholders is reasonable based on industry standards and facts and circumstances.",
        reasoning_framework="""1. Analyze the compensation structure for shareholder-employees.
2. Compare to industry standards for similar roles and responsibilities.
3. Assess the allocation between salary and distributions.
4. Evaluate the impact on payroll taxes and potential IRS scrutiny.
5. Consider relevant IRS guidance and case law (e.g., Watson v. United States).
6. Review supporting documentation (employment agreements, time logs).
7. Identify any attempts to minimize payroll taxes through low salaries.
8. Apply the 'facts and circumstances' test to determine reasonableness.
9. Document rationale for compensation decisions.
10. Prepare for potential IRS challenge under IRC §3121 and §530.
""",
        key_factors=[
            "Industry compensation benchmarks",
            "Shareholder's role and duties",
            "Time devoted to business",
            "Amount of distributions vs salary",
            "Supporting documentation",
            "IRS guidance and case law"
        ],
        primary_authority=["IRC §3121", "Treas. Reg. §31.3121(a)-1", "Watson v. United States, 668 F.3d 1008 (8th Cir. 2012)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert that compensation is unreasonably low to avoid payroll taxes.",
        counter_arguments=[
            "Compensation is consistent with industry standards.",
            "Shareholder's duties are limited.",
            "Distributions reflect return on investment."
        ],
        resolution_strategy="Document compensation rationale, obtain industry comparables, and maintain robust records.",
        entity_scope="S-Corporation shareholder-employees",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Watson v. United States"
    ),
    DoctrineBlock(
        topic="Capital vs Labor Profit Attribution",
        keywords=["capital", "labor", "profit attribution", "partnership", "allocation"],
        conclusion_template="Determine the proper allocation of profits between capital and labor contributions in a partnership or business entity.",
        reasoning_framework="""1. Identify the nature of contributions (capital vs labor).
2. Review partnership agreement or operating agreement for allocation provisions.
3. Apply IRC §704(b) substantial economic effect rules.
4. Consider the economic substance of allocations.
5. Evaluate whether allocations reflect actual economic arrangements.
6. Analyze relevant case law (e.g., Hines v. United States).
7. Assess risk of recharacterization by IRS.
8. Document rationale for allocation methodology.
9. Ensure allocations are consistent with entity's operations and industry norms.
10. Prepare for potential IRS challenge under anti-abuse rules.
""",
        key_factors=[
            "Nature of contributions",
            "Partnership agreement provisions",
            "Substantial economic effect",
            "Economic substance",
            "Industry norms"
        ],
        primary_authority=["IRC §704(b)", "Treas. Reg. §1.704-1(b)", "Hines v. United States, 551 F.2d 586 (3d Cir. 1977)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may argue allocations lack substantial economic effect or are abusive.",
        counter_arguments=[
            "Allocations are consistent with economic reality.",
            "Partnership agreement reflects actual arrangements."
        ],
        resolution_strategy="Maintain detailed records, document economic substance, and ensure compliance with IRC §704(b).",
        entity_scope="Partnerships, LLCs, S-Corporations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hines v. United States"
    ),
    DoctrineBlock(
        topic="Constructive Receipt Doctrine",
        keywords=["constructive receipt", "income", "cash basis", "taxable year"],
        conclusion_template="Determine whether income is constructively received by a taxpayer and thus taxable in the current year.",
        reasoning_framework="""1. Review timing of income availability to taxpayer.
2. Assess whether taxpayer had control over receipt of income.
3. Consider restrictions or limitations on access to funds.
4. Apply Treas. Reg. §1.451-2 guidance.
5. Evaluate relevant case law (e.g., Hornung v. Commissioner).
6. Analyze whether income was credited to account, set aside, or made available.
7. Identify any deferral arrangements.
8. Document facts and circumstances affecting receipt.
9. Prepare for IRS challenge based on constructive receipt.
10. Apply the doctrine to determine taxable year for income recognition.
""",
        key_factors=[
            "Control over income",
            "Availability of funds",
            "Deferral arrangements",
            "Restrictions on access"
        ],
        primary_authority=["IRC §451", "Treas. Reg. §1.451-2", "Hornung v. Commissioner, 47 T.C. 428 (1966)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert income was constructively received and taxable.",
        counter_arguments=[
            "Income was not available without substantial limitations.",
            "Deferral arrangements were bona fide."
        ],
        resolution_strategy="Document restrictions, maintain records of deferral, and apply Treas. Reg. §1.451-2.",
        entity_scope="Individuals, businesses (cash basis)",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hornung v. Commissioner"
    ),
    DoctrineBlock(
        topic="Economic Substance Doctrine",
        keywords=["economic substance", "tax avoidance", "transaction", "business purpose"],
        conclusion_template="Evaluate whether a transaction has sufficient economic substance and business purpose to withstand IRS scrutiny.",
        reasoning_framework="""1. Analyze the transaction's objective and intended outcomes.
2. Assess whether transaction changes taxpayer's economic position.
3. Evaluate presence of a substantial non-tax purpose.
4. Apply two-prong test: (a) objective economic effect, (b) subjective business purpose.
5. Review IRC §7701(o) and related guidance.
6. Consider relevant case law (e.g., Frank Lyon Co. v. United States).
7. Identify tax benefits and compare to non-tax benefits.
8. Document business rationale and supporting evidence.
9. Assess risk of IRS challenge under anti-abuse rules.
10. Prepare for potential penalties under IRC §6662.
""",
        key_factors=[
            "Objective economic effect",
            "Business purpose",
            "Transaction documentation",
            "Tax vs non-tax benefits"
        ],
        primary_authority=["IRC §7701(o)", "Frank Lyon Co. v. United States, 435 U.S. 561 (1978)", "Treas. Reg. §1.7701-1"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert transaction lacks economic substance and disallow tax benefits.",
        counter_arguments=[
            "Transaction has substantial business purpose.",
            "Economic effect is genuine and material."
        ],
        resolution_strategy="Document business purpose, maintain records, and ensure transaction alters economic position.",
        entity_scope="All taxpayers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Frank Lyon Co. v. United States"
    ),
    DoctrineBlock(
        topic="Hobby Loss Rules - IRC §183",
        keywords=["hobby loss", "not engaged for profit", "IRC §183", "activity", "deduction"],
        conclusion_template="Determine whether losses from an activity are deductible or disallowed as hobby losses under IRC §183.",
        reasoning_framework="""1. Analyze taxpayer's intent to make a profit from activity.
2. Apply nine-factor test from Treas. Reg. §1.183-2(b).
3. Review history of income and losses.
4. Assess manner of conducting activity (businesslike vs recreational).
5. Evaluate expertise and time devoted.
6. Consider elements of personal pleasure or recreation.
7. Document efforts to improve profitability.
8. Review relevant case law (e.g., Jackson v. Commissioner).
9. Prepare for IRS challenge under IRC §183.
10. Apply facts and circumstances to determine profit motive.
""",
        key_factors=[
            "Profit motive",
            "History of income/losses",
            "Businesslike conduct",
            "Personal pleasure/recreation"
        ],
        primary_authority=["IRC §183", "Treas. Reg. §1.183-2", "Jackson v. Commissioner, 59 T.C. 312 (1972)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert activity is not engaged for profit and disallow losses.",
        counter_arguments=[
            "Activity conducted in businesslike manner.",
            "Efforts to improve profitability are documented."
        ],
        resolution_strategy="Maintain records, document profit motive, and apply nine-factor test.",
        entity_scope="Individuals, sole proprietors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Jackson v. Commissioner"
    ),
    DoctrineBlock(
        topic="Home Office Deduction - IRC §280A",
        keywords=["home office", "deduction", "exclusive use", "principal place of business", "IRC §280A"],
        conclusion_template="Determine eligibility and calculation for home office deduction under IRC §280A.",
        reasoning_framework="""1. Assess whether space is used exclusively and regularly for business.
2. Determine if home office is principal place of business.
3. Apply IRC §280A(c) requirements.
4. Review documentation (floor plans, photos, logs).
5. Calculate allowable expenses (direct and indirect).
6. Consider simplified method vs actual expense method.
7. Evaluate relevant case law (e.g., Soliman v. Commissioner).
8. Prepare for IRS challenge regarding exclusive use.
9. Document business activities conducted in home office.
10. Apply deduction limitations under IRC §280A(c)(5).
""",
        key_factors=[
            "Exclusive and regular use",
            "Principal place of business",
            "Documentation",
            "Expense calculation"
        ],
        primary_authority=["IRC §280A", "Treas. Reg. §1.280A-2", "Soliman v. Commissioner, 506 U.S. 168 (1993)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert space is not used exclusively or regularly for business.",
        counter_arguments=[
            "Home office is principal place of business.",
            "Exclusive use is documented."
        ],
        resolution_strategy="Maintain logs, photos, and documentation; apply IRC §280A requirements.",
        entity_scope="Individuals, sole proprietors, partners",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Soliman v. Commissioner"
    ),
    DoctrineBlock(
        topic="Passive Activity Loss Rules - IRC §469",
        keywords=["passive activity", "loss limitation", "material participation", "IRC §469"],
        conclusion_template="Determine whether losses from passive activities are deductible or limited under IRC §469.",
        reasoning_framework="""1. Identify passive activities (rental, limited partnership, etc.).
2. Apply material participation tests (Treas. Reg. §1.469-5T).
3. Assess taxpayer's involvement in activity.
4. Calculate allowable losses and carryforwards.
5. Review aggregation and grouping rules.
6. Evaluate relevant case law (e.g., Madler v. Commissioner).
7. Document participation hours and activities.
8. Prepare for IRS challenge regarding material participation.
9. Apply PAL limitations and exceptions (real estate professionals).
10. Maintain records for substantiation.
""",
        key_factors=[
            "Material participation",
            "Nature of activity",
            "Participation hours",
            "Aggregation/grouping"
        ],
        primary_authority=["IRC §469", "Treas. Reg. §1.469-5T", "Madler v. Commissioner, T.C. Memo 1998-112"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert activity is passive and losses are limited.",
        counter_arguments=[
            "Taxpayer materially participates.",
            "Activity qualifies for exception."
        ],
        resolution_strategy="Maintain logs, apply material participation tests, and document activities.",
        entity_scope="Individuals, partnerships, S-Corporations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Madler v. Commissioner"
    ),
    DoctrineBlock(
        topic="Like-Kind Exchange - IRC §1031",
        keywords=["like-kind exchange", "IRC §1031", "deferral", "property", "real estate"],
        conclusion_template="Determine eligibility and requirements for like-kind exchange deferral under IRC §1031.",
        reasoning_framework="""1. Identify properties involved and confirm they are like-kind.
2. Apply IRC §1031(a) requirements for real property exchanges.
3. Assess timing rules (45-day identification, 180-day completion).
4. Review documentation and exchange agreements.
5. Evaluate use of qualified intermediaries.
6. Consider boot and partial exchanges.
7. Analyze relevant case law (e.g., Starker v. United States).
8. Prepare for IRS challenge regarding property qualification.
9. Document exchange process and compliance.
10. Apply reporting requirements (Form 8824).
""",
        key_factors=[
            "Like-kind property",
            "Timing rules",
            "Qualified intermediary",
            "Documentation"
        ],
        primary_authority=["IRC §1031", "Treas. Reg. §1.1031", "Starker v. United States, 602 F.2d 1341 (9th Cir. 1979)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert property is not like-kind or exchange does not meet timing requirements.",
        counter_arguments=[
            "Properties qualify as like-kind.",
            "Exchange complies with timing and intermediary rules."
        ],
        resolution_strategy="Maintain records, use qualified intermediaries, and comply with IRC §1031 requirements.",
        entity_scope="Individuals, businesses, real estate investors",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Starker v. United States"
    ),
    DoctrineBlock(
        topic="Percentage Depletion - Oil & Gas (IRC §613A)",
        keywords=["percentage depletion", "oil and gas", "IRC §613A", "natural resources"],
        conclusion_template="Determine eligibility and calculation for percentage depletion deduction for oil and gas properties under IRC §613A.",
        reasoning_framework="""1. Identify qualifying oil and gas properties.
2. Apply IRC §613A(c) limitations and eligibility.
3. Calculate percentage depletion rate (15% for independent producers).
4. Assess taxable income limitation.
5. Review documentation of production and sales.
6. Consider exceptions for integrated oil companies.
7. Evaluate relevant case law (e.g., Amoco Production Co. v. United States).
8. Prepare for IRS challenge regarding property qualification.
9. Document depletion calculation and substantiation.
10. Apply reporting requirements and maintain records.
""",
        key_factors=[
            "Qualifying property",
            "Depletion rate",
            "Taxable income limitation",
            "Documentation"
        ],
        primary_authority=["IRC §613A", "Treas. Reg. §1.613A-1", "Amoco Production Co. v. United States, 622 F.2d 1318 (8th Cir. 1980)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert property does not qualify or deduction exceeds limitations.",
        counter_arguments=[
            "Property qualifies under IRC §613A.",
            "Depletion calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply IRC §613A limitations, and document calculation.",
        entity_scope="Oil and gas producers",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amoco Production Co. v. United States"
    ),
    DoctrineBlock(
        topic="Intangible Drilling Costs (IDC) - IRC §263(c)",
        keywords=["intangible drilling costs", "IDC", "oil and gas", "IRC §263(c)", "deduction"],
        conclusion_template="Determine eligibility and calculation for deduction or capitalization of intangible drilling costs under IRC §263(c).",
        reasoning_framework="""1. Identify costs qualifying as IDC (labor, supplies, etc.).
2. Apply IRC §263(c) and Treas. Reg. §1.612-4 guidance.
3. Assess election to deduct or capitalize IDC.
4. Review documentation of drilling activities and expenses.
5. Evaluate impact on taxable income and depletion.
6. Consider relevant case law (e.g., F. W. Fitch Co. v. United States).
7. Prepare for IRS challenge regarding cost qualification.
8. Document election and calculation methodology.
9. Apply reporting requirements and maintain records.
10. Ensure compliance with IRS guidance and industry standards.
""",
        key_factors=[
            "Qualifying costs",
            "Election to deduct/capitalize",
            "Documentation",
            "Impact on taxable income"
        ],
        primary_authority=["IRC §263(c)", "Treas. Reg. §1.612-4", "F. W. Fitch Co. v. United States, 323 F.2d 756 (8th Cir. 1963)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert costs do not qualify or election is improper.",
        counter_arguments=[
            "Costs qualify as IDC under IRC §263(c).",
            "Election is properly documented."
        ],
        resolution_strategy="Maintain records, document election, and apply IRC §263(c) guidance.",
        entity_scope="Oil and gas producers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="F. W. Fitch Co. v. United States"
    ),
    DoctrineBlock(
        topic="Qualified Business Income Deduction - IRC §199A",
        keywords=["QBI", "qualified business income", "IRC §199A", "deduction", "pass-through"],
        conclusion_template="Determine eligibility and calculation for qualified business income deduction under IRC §199A.",
        reasoning_framework="""1. Identify qualifying business and income.
2. Apply IRC §199A requirements and limitations.
3. Assess impact of W-2 wages and qualified property.
4. Review documentation of business activities and income.
5. Calculate deduction (up to 20% of QBI).
6. Evaluate specified service trade or business (SSTB) limitations.
7. Consider aggregation rules and phase-out thresholds.
8. Analyze relevant case law and IRS guidance.
9. Prepare for IRS challenge regarding qualification.
10. Document calculation and maintain records.
""",
        key_factors=[
            "Qualifying business",
            "QBI calculation",
            "W-2 wages",
            "Qualified property"
        ],
        primary_authority=["IRC §199A", "Treas. Reg. §1.199A-1", "IRS Notice 2019-07"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert business does not qualify or deduction is improperly calculated.",
        counter_arguments=[
            "Business qualifies under IRC §199A.",
            "Calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply IRC §199A limitations, and document calculation.",
        entity_scope="Sole proprietors, partnerships, S-Corporations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2019-07"
    ),
    DoctrineBlock(
        topic="Statute of Limitations - Assessment & Collection",
        keywords=["statute of limitations", "assessment", "collection", "IRS", "tax"],
        conclusion_template="Determine whether the statute of limitations bars IRS assessment or collection actions.",
        reasoning_framework="""1. Identify relevant statute of limitations period (generally 3 years).
2. Review filing dates and extensions (e.g., substantial omission, fraud).
3. Apply IRC §6501 and §6502 requirements.
4. Assess impact of agreements to extend limitations (Form 872).
5. Evaluate relevant case law (e.g., Badaracco v. Commissioner).
6. Document dates of assessment and collection actions.
7. Prepare for IRS challenge regarding timeliness.
8. Apply exceptions for unfiled or fraudulent returns.
9. Maintain records of correspondence and filings.
10. Determine whether IRS actions are barred.
""",
        key_factors=[
            "Filing dates",
            "Extensions",
            "Fraud/substantial omission",
            "Documentation"
        ],
        primary_authority=["IRC §6501", "IRC §6502", "Badaracco v. Commissioner, 464 U.S. 386 (1984)"],
        burden_holder="IRS",
        adversary_position="Taxpayer may assert assessment or collection is barred by statute of limitations.",
        counter_arguments=[
            "Return was fraudulent or omitted substantial income.",
            "Extension agreement was executed."
        ],
        resolution_strategy="Review filing dates, apply IRC §6501/§6502, and document actions.",
        entity_scope="All taxpayers",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Badaracco v. Commissioner"
    ),
    DoctrineBlock(
        topic="Offer in Compromise (OIC) - IRC §7122",
        keywords=["offer in compromise", "OIC", "IRC §7122", "tax debt", "settlement"],
        conclusion_template="Evaluate eligibility and requirements for IRS Offer in Compromise under IRC §7122.",
        reasoning_framework="""1. Assess taxpayer's ability to pay and financial condition.
2. Apply IRC §7122 and IRS Form 656 requirements.
3. Review documentation of assets, income, and expenses.
4. Evaluate grounds for OIC (doubt as to collectibility, liability, or effective tax administration).
5. Analyze relevant case law (e.g., Murphy v. Commissioner).
6. Prepare for IRS challenge regarding eligibility.
7. Document OIC submission and supporting evidence.
8. Apply IRS guidelines and calculation methodology.
9. Maintain records of negotiation and correspondence.
10. Determine likelihood of acceptance and resolution.
""",
        key_factors=[
            "Ability to pay",
            "Grounds for OIC",
            "Documentation",
            "IRS guidelines"
        ],
        primary_authority=["IRC §7122", "IRS Form 656", "Murphy v. Commissioner, 125 T.C. 301 (2005)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may reject OIC based on financial analysis or lack of grounds.",
        counter_arguments=[
            "Taxpayer is unable to pay full liability.",
            "OIC meets IRS guidelines and is supported by documentation."
        ],
        resolution_strategy="Prepare thorough documentation, apply IRC §7122 requirements, and negotiate with IRS.",
        entity_scope="Individuals, businesses",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Murphy v. Commissioner"
    ),
    DoctrineBlock(
        topic="Employee Retention Credit (ERC) - COVID Relief",
        keywords=["employee retention credit", "ERC", "COVID relief", "CARES Act", "tax credit"],
        conclusion_template="Determine eligibility and calculation for Employee Retention Credit under COVID relief provisions.",
        reasoning_framework="""1. Identify qualifying wages and employees.
2. Apply CARES Act and subsequent guidance (IRS Notice 2021-20).
3. Assess impact of PPP loan and other relief programs.
4. Review documentation of business operations and shutdowns.
5. Calculate allowable credit and limitations.
6. Evaluate relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding eligibility.
8. Document calculation and substantiation.
9. Apply reporting requirements (Form 941).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying wages",
            "Business shutdowns",
            "PPP loan impact",
            "Documentation"
        ],
        primary_authority=["CARES Act", "IRS Notice 2021-20", "Form 941"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert business does not qualify or credit is improperly calculated.",
        counter_arguments=[
            "Business meets eligibility requirements.",
            "Calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply guidance, and document calculation.",
        entity_scope="Employers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2021-20"
    ),
    DoctrineBlock(
        topic="Worker Classification - Employee vs Independent Contractor",
        keywords=["worker classification", "employee", "independent contractor", "IRS", "tax"],
        conclusion_template="Determine proper classification of workers as employees or independent contractors for tax purposes.",
        reasoning_framework="""1. Apply IRS 20-factor test (Revenue Ruling 87-41).
2. Assess degree of control over worker.
3. Review documentation of work arrangements.
4. Evaluate impact on payroll taxes and reporting.
5. Consider relevant case law (e.g., Nationwide Mutual Insurance Co. v. Darden).
6. Prepare for IRS challenge regarding classification.
7. Document rationale and supporting evidence.
8. Apply facts and circumstances to determine classification.
9. Maintain records of contracts and communications.
10. Apply reporting requirements (Form 1099, W-2).
""",
        key_factors=[
            "Degree of control",
            "Work arrangements",
            "Documentation",
            "IRS guidance"
        ],
        primary_authority=["Revenue Ruling 87-41", "Treas. Reg. §31.3401(c)-1", "Nationwide Mutual Insurance Co. v. Darden, 503 U.S. 318 (1992)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert worker is employee and assess payroll taxes.",
        counter_arguments=[
            "Worker operates independently.",
            "Contracts and arrangements support contractor status."
        ],
        resolution_strategy="Maintain records, apply IRS 20-factor test, and document classification.",
        entity_scope="Employers, workers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Nationwide Mutual Insurance Co. v. Darden"
    ),
    DoctrineBlock(
        topic="Conservation Easements - Syndicated Transactions",
        keywords=["conservation easement", "syndicated transaction", "IRC §170", "deduction", "valuation"],
        conclusion_template="Evaluate eligibility and requirements for conservation easement deduction in syndicated transactions.",
        reasoning_framework="""1. Identify property and conservation purpose.
2. Apply IRC §170(h) requirements for qualified easements.
3. Assess valuation methodology and appraisal.
4. Review documentation of transaction and syndication.
5. Evaluate IRS Notice 2017-10 and recent guidance.
6. Analyze relevant case law (e.g., Pine Mountain Preserve, LLLP v. Commissioner).
7. Prepare for IRS challenge regarding valuation or qualification.
8. Document conservation purpose and supporting evidence.
9. Apply reporting requirements (Form 8886).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualified conservation purpose",
            "Valuation/appraisal",
            "Syndication structure",
            "Documentation"
        ],
        primary_authority=["IRC §170(h)", "IRS Notice 2017-10", "Pine Mountain Preserve, LLLP v. Commissioner, T.C. Memo 2022-43"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert deduction is inflated or easement does not qualify.",
        counter_arguments=[
            "Easement meets IRC §170(h) requirements.",
            "Valuation is supported by qualified appraisal."
        ],
        resolution_strategy="Maintain records, obtain qualified appraisal, and comply with reporting requirements.",
        entity_scope="Partnerships, investors",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Pine Mountain Preserve, LLLP v. Commissioner"
    ),
    DoctrineBlock(
        topic="Micro-Captive Insurance - §831(b) Elections",
        keywords=["micro-captive", "insurance", "IRC §831(b)", "election", "deduction"],
        conclusion_template="Evaluate eligibility and requirements for micro-captive insurance company election under IRC §831(b).",
        reasoning_framework="""1. Identify qualifying insurance company and risk coverage.
2. Apply IRC §831(b) requirements and limitations.
3. Assess risk distribution and insurance arrangement.
4. Review documentation of premiums and policies.
5. Evaluate IRS Notice 2016-66 and recent guidance.
6. Analyze relevant case law (e.g., Avrahami v. Commissioner).
7. Prepare for IRS challenge regarding insurance arrangement.
8. Document risk coverage and supporting evidence.
9. Apply reporting requirements (Form 8886).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Risk coverage",
            "Insurance arrangement",
            "Premiums/policies",
            "Documentation"
        ],
        primary_authority=["IRC §831(b)", "IRS Notice 2016-66", "Avrahami v. Commissioner, 149 T.C. 7 (2017)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert arrangement lacks risk distribution or is abusive.",
        counter_arguments=[
            "Insurance arrangement meets IRC §831(b) requirements.",
            "Risk coverage is genuine and documented."
        ],
        resolution_strategy="Maintain records, document risk coverage, and comply with reporting requirements.",
        entity_scope="Businesses, insurance companies",
        confidence=0.78,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Avrahami v. Commissioner"
    ),
    DoctrineBlock(
        topic="Related Party Transactions - §267 and §707(b)",
        keywords=["related party", "transactions", "IRC §267", "IRC §707(b)", "deduction"],
        conclusion_template="Determine limitations and requirements for related party transactions under IRC §267 and §707(b).",
        reasoning_framework="""1. Identify related parties and nature of transaction.
2. Apply IRC §267 and §707(b) requirements.
3. Assess timing and deductibility of expenses.
4. Review documentation of transaction and relationship.
5. Evaluate impact on income and deduction recognition.
6. Analyze relevant case law (e.g., Bittker v. Commissioner).
7. Prepare for IRS challenge regarding related party status.
8. Document transaction rationale and supporting evidence.
9. Apply reporting requirements and maintain records.
10. Ensure compliance with anti-abuse rules.
""",
        key_factors=[
            "Related party status",
            "Transaction documentation",
            "Timing of deductions",
            "Anti-abuse rules"
        ],
        primary_authority=["IRC §267", "IRC §707(b)", "Bittker v. Commissioner, T.C. Memo 1985-434"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert deduction is disallowed or transaction is abusive.",
        counter_arguments=[
            "Transaction is bona fide and documented.",
            "Related party status is properly disclosed."
        ],
        resolution_strategy="Maintain records, apply IRC §267/§707(b) requirements, and document transaction.",
        entity_scope="Businesses, partnerships",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bittker v. Commissioner"
    ),
    DoctrineBlock(
        topic="Partnership Special Allocations - §704(b)",
        keywords=["partnership", "special allocation", "IRC §704(b)", "substantial economic effect"],
        conclusion_template="Evaluate validity and requirements for partnership special allocations under IRC §704(b).",
        reasoning_framework="""1. Review partnership agreement for allocation provisions.
2. Apply IRC §704(b) substantial economic effect rules.
3. Assess economic substance of allocations.
4. Analyze relevant case law (e.g., Goldfine v. Commissioner).
5. Document rationale for allocation methodology.
6. Prepare for IRS challenge regarding economic effect.
7. Apply facts and circumstances to determine validity.
8. Maintain records of partnership operations and allocations.
9. Ensure compliance with Treas. Reg. §1.704-1(b).
10. Apply anti-abuse rules and document arrangements.
""",
        key_factors=[
            "Partnership agreement",
            "Economic substance",
            "Documentation",
            "Substantial economic effect"
        ],
        primary_authority=["IRC §704(b)", "Treas. Reg. §1.704-1(b)", "Goldfine v. Commissioner, T.C. Memo 1988-473"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert allocation lacks economic effect or is abusive.",
        counter_arguments=[
            "Allocation reflects economic reality.",
            "Partnership agreement is properly drafted."
        ],
        resolution_strategy="Maintain records, apply IRC §704(b) rules, and document allocations.",
        entity_scope="Partnerships, LLCs",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Goldfine v. Commissioner"
    ),
    DoctrineBlock(
        topic="Wash Sale Rules - §1091",
        keywords=["wash sale", "IRC §1091", "loss disallowance", "securities", "tax"],
        conclusion_template="Determine application and requirements for wash sale rules under IRC §1091.",
        reasoning_framework="""1. Identify sale and repurchase of substantially identical securities.
2. Apply IRC §1091 requirements for loss disallowance.
3. Assess timing of transactions (30-day window).
4. Review documentation of trades and holdings.
5. Evaluate impact on basis and holding period.
6. Analyze relevant case law (e.g., McWilliams v. Commissioner).
7. Prepare for IRS challenge regarding wash sale status.
8. Document rationale for transactions.
9. Apply reporting requirements and maintain records.
10. Ensure compliance with IRC §1091.
""",
        key_factors=[
            "Substantially identical securities",
            "Timing of transactions",
            "Documentation",
            "Basis adjustment"
        ],
        primary_authority=["IRC §1091", "Treas. Reg. §1.1091-1", "McWilliams v. Commissioner, 331 U.S. 694 (1947)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert loss is disallowed under wash sale rules.",
        counter_arguments=[
            "Transactions are not substantially identical.",
            "Timing does not trigger wash sale rule."
        ],
        resolution_strategy="Maintain records, apply IRC §1091 requirements, and document trades.",
        entity_scope="Individuals, investors",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="McWilliams v. Commissioner"
    ),
    DoctrineBlock(
        topic="Net Operating Losses - §172",
        keywords=["net operating loss", "NOL", "IRC §172", "carryforward", "carryback"],
        conclusion_template="Determine eligibility and calculation for net operating loss carryforward and carryback under IRC §172.",
        reasoning_framework="""1. Calculate NOL based on allowable deductions and income.
2. Apply IRC §172 requirements and limitations.
3. Assess carryforward and carryback periods.
4. Review documentation of losses and income.
5. Evaluate impact of CARES Act and recent changes.
6. Analyze relevant case law (e.g., Jones v. Commissioner).
7. Prepare for IRS challenge regarding NOL calculation.
8. Document rationale and supporting evidence.
9. Apply reporting requirements (Form 1045, 1139).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "NOL calculation",
            "Carryforward/carryback periods",
            "Documentation",
            "Recent legislative changes"
        ],
        primary_authority=["IRC §172", "CARES Act", "Jones v. Commissioner, T.C. Memo 2000-219"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert NOL is improperly calculated or applied.",
        counter_arguments=[
            "NOL calculation is accurate and documented.",
            "Carryforward/carryback is within allowable periods."
        ],
        resolution_strategy="Maintain records, apply IRC §172 requirements, and document calculation.",
        entity_scope="Individuals, businesses",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Jones v. Commissioner"
    ),
    DoctrineBlock(
        topic="S-Corporation Shareholder Basis - Loss Limitations",
        keywords=["S-Corporation", "shareholder basis", "loss limitation", "IRC §1366", "IRC §1367"],
        conclusion_template="Determine eligibility and calculation for S-Corporation shareholder basis and loss limitations.",
        reasoning_framework="""1. Calculate shareholder basis in S-Corporation stock and debt.
2. Apply IRC §1366 and §1367 requirements.
3. Assess impact of distributions and losses.
4. Review documentation of contributions and loans.
5. Evaluate relevant case law (e.g., Oren v. Commissioner).
6. Prepare for IRS challenge regarding basis calculation.
7. Document rationale and supporting evidence.
8. Apply reporting requirements and maintain records.
9. Ensure compliance with basis and loss limitation rules.
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Basis calculation",
            "Distributions/losses",
            "Documentation",
            "IRC §1366/§1367 rules"
        ],
        primary_authority=["IRC §1366", "IRC §1367", "Oren v. Commissioner, T.C. Memo 2002-172"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert loss exceeds basis or is improperly claimed.",
        counter_arguments=[
            "Basis calculation is accurate and documented.",
            "Loss is within allowable limits."
        ],
        resolution_strategy="Maintain records, apply IRC §1366/§1367 requirements, and document calculation.",
        entity_scope="S-Corporation shareholders",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Oren v. Commissioner"
    ),
    DoctrineBlock(
        topic="Self-Employment Tax - §1401",
        keywords=["self-employment tax", "IRC §1401", "sole proprietor", "partnership", "tax"],
        conclusion_template="Determine eligibility and calculation for self-employment tax under IRC §1401.",
        reasoning_framework="""1. Identify self-employment income and activities.
2. Apply IRC §1401 requirements and limitations.
3. Assess impact of partnership and S-Corporation arrangements.
4. Review documentation of income and expenses.
5. Evaluate relevant case law (e.g., Radtke v. United States).
6. Prepare for IRS challenge regarding self-employment status.
7. Document rationale and supporting evidence.
8. Apply reporting requirements (Schedule SE).
9. Maintain records for audit and compliance.
10. Ensure compliance with IRC §1401.
""",
        key_factors=[
            "Self-employment income",
            "Entity structure",
            "Documentation",
            "IRC §1401 requirements"
        ],
        primary_authority=["IRC §1401", "Schedule SE", "Radtke v. United States, 895 F.2d 1196 (7th Cir. 1990)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert income is subject to self-employment tax.",
        counter_arguments=[
            "Income is not self-employment income.",
            "Entity structure exempts income from tax."
        ],
        resolution_strategy="Maintain records, apply IRC §1401 requirements, and document income.",
        entity_scope="Sole proprietors, partners",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Radtke v. United States"
    ),
    DoctrineBlock(
        topic="Hobby Loss - §183 Activity Not Engaged for Profit",
        keywords=["hobby loss", "IRC §183", "not engaged for profit", "deduction", "activity"],
        conclusion_template="Determine whether losses from an activity are deductible or disallowed as hobby losses under IRC §183.",
        reasoning_framework="""1. Analyze taxpayer's intent to make a profit from activity.
2. Apply nine-factor test from Treas. Reg. §1.183-2(b).
3. Review history of income and losses.
4. Assess manner of conducting activity (businesslike vs recreational).
5. Evaluate expertise and time devoted.
6. Consider elements of personal pleasure or recreation.
7. Document efforts to improve profitability.
8. Review relevant case law (e.g., Jackson v. Commissioner).
9. Prepare for IRS challenge under IRC §183.
10. Apply facts and circumstances to determine profit motive.
""",
        key_factors=[
            "Profit motive",
            "History of income/losses",
            "Businesslike conduct",
            "Personal pleasure/recreation"
        ],
        primary_authority=["IRC §183", "Treas. Reg. §1.183-2", "Jackson v. Commissioner, 59 T.C. 312 (1972)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert activity is not engaged for profit and disallow losses.",
        counter_arguments=[
            "Activity conducted in businesslike manner.",
            "Efforts to improve profitability are documented."
        ],
        resolution_strategy="Maintain records, document profit motive, and apply nine-factor test.",
        entity_scope="Individuals, sole proprietors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Jackson v. Commissioner"
    ),
    DoctrineBlock(
        topic="Passive Activity Loss Limitations - §469",
        keywords=["passive activity", "loss limitation", "material participation", "IRC §469"],
        conclusion_template="Determine whether losses from passive activities are deductible or limited under IRC §469.",
        reasoning_framework="""1. Identify passive activities (rental, limited partnership, etc.).
2. Apply material participation tests (Treas. Reg. §1.469-5T).
3. Assess taxpayer's involvement in activity.
4. Calculate allowable losses and carryforwards.
5. Review aggregation and grouping rules.
6. Evaluate relevant case law (e.g., Madler v. Commissioner).
7. Document participation hours and activities.
8. Prepare for IRS challenge regarding material participation.
9. Apply PAL limitations and exceptions (real estate professionals).
10. Maintain records for substantiation.
""",
        key_factors=[
            "Material participation",
            "Nature of activity",
            "Participation hours",
            "Aggregation/grouping"
        ],
        primary_authority=["IRC §469", "Treas. Reg. §1.469-5T", "Madler v. Commissioner, T.C. Memo 1998-112"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert activity is passive and losses are limited.",
        counter_arguments=[
            "Taxpayer materially participates.",
            "Activity qualifies for exception."
        ],
        resolution_strategy="Maintain logs, apply material participation tests, and document activities.",
        entity_scope="Individuals, partnerships, S-Corporations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Madler v. Commissioner"
    ),
    DoctrineBlock(
        topic="At-Risk Limitations - §465",
        keywords=["at-risk limitation", "IRC §465", "loss limitation", "investment", "activity"],
        conclusion_template="Determine eligibility and calculation for at-risk limitations on losses under IRC §465.",
        reasoning_framework="""1. Identify investment and activity subject to at-risk rules.
2. Apply IRC §465 requirements and limitations.
3. Assess amount at risk and impact of nonrecourse financing.
4. Review documentation of investment and financing arrangements.
5. Evaluate relevant case law (e.g., Waters v. Commissioner).
6. Prepare for IRS challenge regarding at-risk calculation.
7. Document rationale and supporting evidence.
8. Apply reporting requirements and maintain records.
9. Ensure compliance with IRC §465.
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Amount at risk",
            "Nonrecourse financing",
            "Documentation",
            "IRC §465 requirements"
        ],
        primary_authority=["IRC §465", "Treas. Reg. §1.465-1", "Waters v. Commissioner, T.C. Memo 1991-462"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert loss exceeds amount at risk or is improperly claimed.",
        counter_arguments=[
            "Amount at risk is accurately calculated and documented.",
            "Financing arrangements comply with IRC §465."
        ],
        resolution_strategy="Maintain records, apply IRC §465 requirements, and document calculation.",
        entity_scope="Individuals, partnerships",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Waters v. Commissioner"
    ),
    DoctrineBlock(
        topic="Cancellation of Debt Income - §61/§108",
        keywords=["cancellation of debt", "COD income", "IRC §61", "IRC §108", "exclusion"],
        conclusion_template="Determine inclusion or exclusion of cancellation of debt income under IRC §61 and §108.",
        reasoning_framework="""1. Identify debt canceled and circumstances.
2. Apply IRC §61 inclusion rules.
3. Assess eligibility for exclusion under IRC §108 (insolvency, bankruptcy, etc.).
4. Review documentation of debt and financial condition.
5. Evaluate impact on taxable income and reporting.
6. Analyze relevant case law (e.g., Zarin v. Commissioner).
7. Prepare for IRS challenge regarding exclusion.
8. Document rationale and supporting evidence.
9. Apply reporting requirements (Form 982).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Debt cancellation",
            "Eligibility for exclusion",
            "Documentation",
            "IRC §61/§108 requirements"
        ],
        primary_authority=["IRC §61", "IRC §108", "Zarin v. Commissioner, 916 F.2d 151 (3d Cir. 1990)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert income is includible or exclusion is not applicable.",
        counter_arguments=[
            "Taxpayer meets exclusion requirements.",
            "Documentation supports exclusion."
        ],
        resolution_strategy="Maintain records, apply IRC §61/§108 requirements, and document exclusion.",
        entity_scope="Individuals, businesses",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Zarin v. Commissioner"
    ),
    DoctrineBlock(
        topic="Substantial Understatement Penalty - §6662",
        keywords=["substantial understatement", "penalty", "IRC §6662", "accuracy-related", "tax"],
        conclusion_template="Determine application and requirements for substantial understatement penalty under IRC §6662.",
        reasoning_framework="""1. Identify understatement of tax liability.
2. Apply IRC §6662 requirements and thresholds.
3. Assess reasonable cause and good faith defenses.
4. Review documentation of reporting and calculations.
5. Evaluate impact of disclosure and reporting.
6. Analyze relevant case law (e.g., Neonatology Associates v. Commissioner).
7. Prepare for IRS challenge regarding penalty.
8. Document rationale and supporting evidence.
9. Apply reporting requirements and maintain records.
10. Ensure compliance with IRC §6662.
""",
        key_factors=[
            "Understatement amount",
            "Reasonable cause/good faith",
            "Documentation",
            "IRC §6662 requirements"
        ],
        primary_authority=["IRC §6662", "Treas. Reg. §1.6662-4", "Neonatology Associates v. Commissioner, 115 T.C. 43 (2000)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert penalty applies due to substantial understatement.",
        counter_arguments=[
            "Taxpayer acted with reasonable cause and good faith.",
            "Disclosure was made as required."
        ],
        resolution_strategy="Maintain records, apply IRC §6662 requirements, and document defenses.",
        entity_scope="All taxpayers",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Neonatology Associates v. Commissioner"
    ),
    DoctrineBlock(
        topic="Home Office Deduction - §280A",
        keywords=["home office", "deduction", "exclusive use", "principal place of business", "IRC §280A"],
        conclusion_template="Determine eligibility and calculation for home office deduction under IRC §280A.",
        reasoning_framework="""1. Assess whether space is used exclusively and regularly for business.
2. Determine if home office is principal place of business.
3. Apply IRC §280A(c) requirements.
4. Review documentation (floor plans, photos, logs).
5. Calculate allowable expenses (direct and indirect).
6. Consider simplified method vs actual expense method.
7. Evaluate relevant case law (e.g., Soliman v. Commissioner).
8. Prepare for IRS challenge regarding exclusive use.
9. Document business activities conducted in home office.
10. Apply deduction limitations under IRC §280A(c)(5).
""",
        key_factors=[
            "Exclusive and regular use",
            "Principal place of business",
            "Documentation",
            "Expense calculation"
        ],
        primary_authority=["IRC §280A", "Treas. Reg. §1.280A-2", "Soliman v. Commissioner, 506 U.S. 168 (1993)"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert space is not used exclusively or regularly for business.",
        counter_arguments=[
            "Home office is principal place of business.",
            "Exclusive use is documented."
        ],
        resolution_strategy="Maintain logs, photos, and documentation; apply IRC §280A requirements.",
        entity_scope="Individuals, sole proprietors, partners",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Soliman v. Commissioner"
    ),
    DoctrineBlock(
        topic="Wind Energy Production Tax Credit - IRC §45",
        keywords=["wind energy", "production tax credit", "IRC §45", "renewable energy", "electricity"],
        conclusion_template="Determine eligibility and calculation for wind energy production tax credit under IRC §45.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply IRC §45 requirements for production tax credit.
3. Assess measurement and documentation of electricity produced.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures (partnerships, LLCs).
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and production records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Electricity production",
            "Ownership/operation"
        ],
        primary_authority=["IRC §45", "Form 8835", "IRS Notice 2013-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or production is not properly measured.",
        counter_arguments=[
            "Facility meets IRC §45 requirements.",
            "Production measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply IRC §45 requirements, and document production.",
        entity_scope="Wind energy producers, investors",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2013-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Investment Tax Credit - IRC §48",
        keywords=["wind energy", "investment tax credit", "IRC §48", "renewable energy", "facility"],
        conclusion_template="Determine eligibility and calculation for wind energy investment tax credit under IRC §48.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply IRC §48 requirements for investment tax credit.
3. Assess basis of qualifying property.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures (partnerships, LLCs).
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and basis calculation.
8. Document facility operations and property records.
9. Apply reporting requirements (Form 3468).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Basis calculation",
            "Ownership/operation"
        ],
        primary_authority=["IRC §48", "Form 3468", "IRS Notice 2013-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or basis is improperly calculated.",
        counter_arguments=[
            "Facility meets IRC §48 requirements.",
            "Basis calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply IRC §48 requirements, and document basis.",
        entity_scope="Wind energy producers, investors",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2013-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Depreciation - MACRS",
        keywords=["wind energy", "depreciation", "MACRS", "IRC §168", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for depreciation of wind energy facilities under MACRS.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply MACRS depreciation rules under IRC §168.
3. Assess classification and recovery period (5-year, 7-year).
4. Review documentation of facility and property records.
5. Evaluate impact of bonus depreciation and Section 179.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding classification and calculation.
8. Document facility operations and depreciation schedules.
9. Apply reporting requirements (Form 4562).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Recovery period",
            "Depreciation calculation",
            "Documentation"
        ],
        primary_authority=["IRC §168", "Form 4562", "IRS Publication 946"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or depreciation is improperly calculated.",
        counter_arguments=[
            "Facility meets MACRS requirements.",
            "Depreciation calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply IRC §168 requirements, and document depreciation.",
        entity_scope="Wind energy producers, investors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Publication 946"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 1603 Grant",
        keywords=["wind energy", "Section 1603 grant", "renewable energy", "Treasury", "cash grant"],
        conclusion_template="Determine eligibility and requirements for wind energy Section 1603 cash grant.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply Section 1603 grant requirements and limitations.
3. Assess basis of qualifying property and grant calculation.
4. Review ownership and operation of facility.
5. Evaluate impact of grant on depreciation and tax credits.
6. Analyze relevant case law and Treasury guidance.
7. Prepare for Treasury challenge regarding qualification and calculation.
8. Document facility operations and property records.
9. Apply reporting requirements and maintain records.
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Basis calculation",
            "Ownership/operation"
        ],
        primary_authority=["Section 1603", "Treasury Guidance", "Form 1603"],
        burden_holder="Taxpayer",
        adversary_position="Treasury may assert facility does not qualify or grant is improperly calculated.",
        counter_arguments=[
            "Facility meets Section 1603 requirements.",
            "Basis calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 1603 requirements, and document grant calculation.",
        entity_scope="Wind energy producers, investors",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Treasury Guidance"
    ),
    DoctrineBlock(
        topic="Wind Energy Partnership Tax Equity Structures",
        keywords=["wind energy", "partnership", "tax equity", "allocation", "IRC §704"],
        conclusion_template="Determine validity and requirements for wind energy partnership tax equity structures.",
        reasoning_framework="""1. Review partnership agreement for allocation provisions.
2. Apply IRC §704(b) substantial economic effect rules.
3. Assess economic substance of allocations.
4. Evaluate impact of tax equity investor arrangements.
5. Analyze relevant case law and IRS guidance.
6. Prepare for IRS challenge regarding economic effect and allocation.
7. Document rationale for allocation methodology.
8. Apply facts and circumstances to determine validity.
9. Maintain records of partnership operations and allocations.
10. Ensure compliance with Treas. Reg. §1.704-1(b).
""",
        key_factors=[
            "Partnership agreement",
            "Economic substance",
            "Tax equity investor arrangements",
            "Documentation"
        ],
        primary_authority=["IRC §704(b)", "Treas. Reg. §1.704-1(b)", "IRS Notice 2015-54"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert allocation lacks economic effect or is abusive.",
        counter_arguments=[
            "Allocation reflects economic reality.",
            "Partnership agreement is properly drafted."
        ],
        resolution_strategy="Maintain records, apply IRC §704(b) rules, and document allocations.",
        entity_scope="Wind energy producers, investors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2015-54"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45Q Carbon Capture Credit",
        keywords=["wind energy", "carbon capture", "Section 45Q", "tax credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy carbon capture tax credit under Section 45Q.",
        reasoning_framework="""1. Identify qualifying wind energy facility with carbon capture equipment.
2. Apply Section 45Q requirements for tax credit.
3. Assess measurement and documentation of carbon captured.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and capture records.
9. Apply reporting requirements (Form 8933).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Carbon capture equipment",
            "Measurement/documentation",
            "Ownership/operation"
        ],
        primary_authority=["Section 45Q", "Form 8933", "IRS Notice 2020-12"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or measurement is not properly documented.",
        counter_arguments=[
            "Facility meets Section 45Q requirements.",
            "Measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45Q requirements, and document capture.",
        entity_scope="Wind energy producers, investors",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2020-12"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 48C Advanced Energy Project Credit",
        keywords=["wind energy", "Section 48C", "advanced energy project", "tax credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy advanced energy project tax credit under Section 48C.",
        reasoning_framework="""1. Identify qualifying wind energy facility and project.
2. Apply Section 48C requirements and limitations.
3. Assess basis of qualifying property and credit calculation.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and calculation.
8. Document facility operations and property records.
9. Apply reporting requirements (Form 3468).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Project qualification",
            "Basis calculation",
            "Ownership/operation"
        ],
        primary_authority=["Section 48C", "Form 3468", "IRS Notice 2009-72"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or credit is improperly calculated.",
        counter_arguments=[
            "Facility meets Section 48C requirements.",
            "Basis calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 48C requirements, and document credit calculation.",
        entity_scope="Wind energy producers, investors",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2009-72"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45E Clean Electricity Production Credit",
        keywords=["wind energy", "Section 45E", "clean electricity", "production credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy clean electricity production credit under Section 45E.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply Section 45E requirements for production credit.
3. Assess measurement and documentation of electricity produced.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and production records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Electricity production",
            "Ownership/operation"
        ],
        primary_authority=["Section 45E", "Form 8835", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or production is not properly measured.",
        counter_arguments=[
            "Facility meets Section 45E requirements.",
            "Production measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45E requirements, and document production.",
        entity_scope="Wind energy producers, investors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 48E Clean Electricity Investment Credit",
        keywords=["wind energy", "Section 48E", "clean electricity", "investment credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy clean electricity investment credit under Section 48E.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply Section 48E requirements for investment credit.
3. Assess basis of qualifying property.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and basis calculation.
8. Document facility operations and property records.
9. Apply reporting requirements (Form 3468).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Basis calculation",
            "Ownership/operation"
        ],
        primary_authority=["Section 48E", "Form 3468", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or basis is improperly calculated.",
        counter_arguments=[
            "Facility meets Section 48E requirements.",
            "Basis calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 48E requirements, and document basis.",
        entity_scope="Wind energy producers, investors",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45X Advanced Manufacturing Production Credit",
        keywords=["wind energy", "Section 45X", "advanced manufacturing", "production credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy advanced manufacturing production credit under Section 45X.",
        reasoning_framework="""1. Identify qualifying wind energy facility and manufacturing activities.
2. Apply Section 45X requirements for production credit.
3. Assess measurement and documentation of manufactured components.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and production records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Manufacturing activities",
            "Measurement/documentation",
            "Ownership/operation"
        ],
        primary_authority=["Section 45X", "Form 8835", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or production is not properly measured.",
        counter_arguments=[
            "Facility meets Section 45X requirements.",
            "Production measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45X requirements, and document production.",
        entity_scope="Wind energy producers, manufacturers",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45Y Clean Electricity Production Credit",
        keywords=["wind energy", "Section 45Y", "clean electricity", "production credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy clean electricity production credit under Section 45Y.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply Section 45Y requirements for production credit.
3. Assess measurement and documentation of electricity produced.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and production records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Electricity production",
            "Ownership/operation"
        ],
        primary_authority=["Section 45Y", "Form 8835", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or production is not properly measured.",
        counter_arguments=[
            "Facility meets Section 45Y requirements.",
            "Production measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45Y requirements, and document production.",
        entity_scope="Wind energy producers, investors",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 48Y Clean Electricity Investment Credit",
        keywords=["wind energy", "Section 48Y", "clean electricity", "investment credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy clean electricity investment credit under Section 48Y.",
        reasoning_framework="""1. Identify qualifying wind energy facility and placed-in-service date.
2. Apply Section 48Y requirements for investment credit.
3. Assess basis of qualifying property.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and basis calculation.
8. Document facility operations and property records.
9. Apply reporting requirements (Form 3468).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Basis calculation",
            "Ownership/operation"
        ],
        primary_authority=["Section 48Y", "Form 3468", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or basis is improperly calculated.",
        counter_arguments=[
            "Facility meets Section 48Y requirements.",
            "Basis calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 48Y requirements, and document basis.",
        entity_scope="Wind energy producers, investors",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45Z Clean Fuel Production Credit",
        keywords=["wind energy", "Section 45Z", "clean fuel", "production credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for wind energy clean fuel production credit under Section 45Z.",
        reasoning_framework="""1. Identify qualifying wind energy facility and clean fuel production activities.
2. Apply Section 45Z requirements for production credit.
3. Assess measurement and documentation of clean fuel produced.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and production records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Clean fuel production",
            "Measurement/documentation",
            "Ownership/operation"
        ],
        primary_authority=["Section 45Z", "Form 8835", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or production is not properly measured.",
        counter_arguments=[
            "Facility meets Section 45Z requirements.",
            "Production measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45Z requirements, and document production.",
        entity_scope="Wind energy producers, manufacturers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45U Zero-Emission Nuclear Power Production Credit",
        keywords=["wind energy", "Section 45U", "zero-emission", "nuclear power", "production credit"],
        conclusion_template="Determine eligibility and calculation for zero-emission nuclear power production credit under Section 45U.",
        reasoning_framework="""1. Identify qualifying zero-emission nuclear power facility and placed-in-service date.
2. Apply Section 45U requirements for production credit.
3. Assess measurement and documentation of electricity produced.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and production records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Electricity production",
            "Ownership/operation"
        ],
        primary_authority=["Section 45U", "Form 8835", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or production is not properly measured.",
        counter_arguments=[
            "Facility meets Section 45U requirements.",
            "Production measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45U requirements, and document production.",
        entity_scope="Zero-emission nuclear power producers, investors",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45V Clean Hydrogen Production Credit",
        keywords=["wind energy", "Section 45V", "clean hydrogen", "production credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for clean hydrogen production credit under Section 45V.",
        reasoning_framework="""1. Identify qualifying wind energy facility and clean hydrogen production activities.
2. Apply Section 45V requirements for production credit.
3. Assess measurement and documentation of hydrogen produced.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and production records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Clean hydrogen production",
            "Measurement/documentation",
            "Ownership/operation"
        ],
        primary_authority=["Section 45V", "Form 8835", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or production is not properly measured.",
        counter_arguments=[
            "Facility meets Section 45V requirements.",
            "Production measurement is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45V requirements, and document production.",
        entity_scope="Wind energy producers, manufacturers",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45W Commercial Clean Vehicle Credit",
        keywords=["wind energy", "Section 45W", "commercial clean vehicle", "tax credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for commercial clean vehicle tax credit under Section 45W.",
        reasoning_framework="""1. Identify qualifying commercial clean vehicle and placed-in-service date.
2. Apply Section 45W requirements for tax credit.
3. Assess basis of qualifying property and credit calculation.
4. Review ownership and operation of vehicle.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and calculation.
8. Document vehicle operations and property records.
9. Apply reporting requirements (Form 8936).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying vehicle",
            "Placed-in-service date",
            "Basis calculation",
            "Ownership/operation"
        ],
        primary_authority=["Section 45W", "Form 8936", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert vehicle does not qualify or credit is improperly calculated.",
        counter_arguments=[
            "Vehicle meets Section 45W requirements.",
            "Basis calculation is accurate and documented."
        ],
        resolution_strategy="Maintain records, apply Section 45W requirements, and document credit calculation.",
        entity_scope="Commercial clean vehicle producers, investors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Wind Energy Section 45AA Clean Electricity Transmission Credit",
        keywords=["wind energy", "Section 45AA", "clean electricity", "transmission credit", "renewable energy"],
        conclusion_template="Determine eligibility and calculation for clean electricity transmission credit under Section 45AA.",
        reasoning_framework="""1. Identify qualifying wind energy transmission facility and placed-in-service date.
2. Apply Section 45AA requirements for transmission credit.
3. Assess measurement and documentation of electricity transmitted.
4. Review ownership and operation of facility.
5. Evaluate impact of tax equity structures.
6. Analyze relevant case law and IRS guidance.
7. Prepare for IRS challenge regarding qualification and measurement.
8. Document facility operations and transmission records.
9. Apply reporting requirements (Form 8835).
10. Maintain records for audit and compliance.
""",
        key_factors=[
            "Qualifying facility",
            "Placed-in-service date",
            "Electricity transmission",
            "Ownership/operation"
        ],
        primary_authority=["Section 45AA", "Form 8835", "IRS Notice 2023-29"],
        burden_holder="Taxpayer",
        adversary_position="IRS may assert facility does not qualify or transmission is not properly measured.",
        counter_arguments=[
            "Facility