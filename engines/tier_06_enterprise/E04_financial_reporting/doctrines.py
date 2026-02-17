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
        topic="ASC 606 Revenue Recognition - Five-Step Model",
        keywords=["revenue recognition", "ASC 606", "five-step model", "performance obligations", "contract", "transaction price"],
        conclusion_template="Revenue is recognized when control of goods or services is transferred to the customer, following the five-step model.",
        reasoning_framework="""
1. Identify the contract(s) with a customer.
2. Identify the performance obligations in the contract.
3. Determine the transaction price.
4. Allocate the transaction price to the performance obligations.
5. Recognize revenue when (or as) the entity satisfies a performance obligation.
Key considerations include contract modifications, variable consideration, significant financing components, non-cash consideration, and consideration payable to a customer. The entity must assess transfer of control, which may occur over time or at a point in time, based on indicators such as legal title, physical possession, risks and rewards, and customer acceptance.
        """,
        key_factors=[
            "Existence of a contract",
            "Distinct performance obligations",
            "Transaction price determination",
            "Allocation of price to obligations",
            "Timing of satisfaction of obligations"
        ],
        primary_authority=["ASC 606", "FASB ASU 2014-09"],
        burden_holder="Reporting entity",
        adversary_position="Revenue should be recognized earlier/later based on alternative interpretations of transfer of control.",
        counter_arguments=[
            "Substance over form: focus on actual transfer of control, not just legal title.",
            "Variable consideration must be constrained to avoid overstatement."
        ],
        resolution_strategy="Apply the five-step model rigorously, document judgments, and disclose significant estimates and judgments.",
        entity_scope="All entities entering into contracts with customers (except those scoped out by ASC 606-10-15-2).",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2014-09, SEC SAB Topic 13"
    ),
    DoctrineBlock(
        topic="ASC 842 Lease Accounting - Lessee Model",
        keywords=["lease accounting", "ASC 842", "lessee", "right-of-use asset", "lease liability", "operating lease", "finance lease"],
        conclusion_template="Lessee recognizes a right-of-use asset and a lease liability for most leases, classified as either finance or operating.",
        reasoning_framework="""
ASC 842 requires lessees to recognize a right-of-use (ROU) asset and a corresponding lease liability for substantially all leases. The lease liability is measured at the present value of lease payments not yet paid, discounted using the rate implicit in the lease or the lessee's incremental borrowing rate. The ROU asset is initially measured at the amount of the lease liability, adjusted for lease incentives, initial direct costs, and prepaid or accrued lease payments.
Leases are classified as finance or operating based on criteria similar to legacy capital lease tests. Finance leases recognize interest and amortization expense separately; operating leases recognize a single lease expense.
Short-term leases (12 months or less) may be exempted.
        """,
        key_factors=[
            "Lease term and renewal options",
            "Discount rate determination",
            "Lease incentives and initial direct costs",
            "Classification criteria",
            "Short-term lease exemption"
        ],
        primary_authority=["ASC 842", "FASB ASU 2016-02"],
        burden_holder="Lessee",
        adversary_position="Leases should be kept off-balance sheet or classified differently.",
        counter_arguments=[
            "Substance over form: arrangements that convey control of an asset are leases.",
            "Short-term lease exemption is narrowly defined."
        ],
        resolution_strategy="Apply ASC 842 definitions and criteria, document judgments, and disclose significant assumptions.",
        entity_scope="All lessees except those specifically exempted (e.g., certain short-term leases).",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2016-02"
    ),
    DoctrineBlock(
        topic="ASC 326 Current Expected Credit Losses (CECL)",
        keywords=["credit losses", "ASC 326", "CECL", "allowance", "financial instruments", "expected loss"],
        conclusion_template="Entities recognize an allowance for expected credit losses on financial assets measured at amortized cost.",
        reasoning_framework="""
ASC 326 requires entities to estimate and recognize lifetime expected credit losses for financial assets measured at amortized cost, including trade receivables, loans, and held-to-maturity debt securities. The CECL model is forward-looking and incorporates historical experience, current conditions, and reasonable and supportable forecasts. The allowance is updated at each reporting date, with changes recognized in earnings.
Entities may use various estimation methods, including discounted cash flow, loss-rate, roll-rate, probability of default, or aging schedules, provided they are reasonable and supportable.
        """,
        key_factors=[
            "Historical loss experience",
            "Current economic conditions",
            "Reasonable and supportable forecasts",
            "Pooling of assets with similar risk characteristics",
            "Reversion to historical loss information"
        ],
        primary_authority=["ASC 326", "FASB ASU 2016-13"],
        burden_holder="Reporting entity",
        adversary_position="Losses should be recognized only when probable (incurred loss model).",
        counter_arguments=[
            "CECL requires recognition of expected, not just incurred, losses.",
            "Forecasts must be reasonable and supportable."
        ],
        resolution_strategy="Develop robust estimation methodologies, document assumptions, and update allowance regularly.",
        entity_scope="All entities holding financial assets measured at amortized cost.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2016-13"
    ),
    DoctrineBlock(
        topic="Income Statement Presentation and Classification",
        keywords=["income statement", "presentation", "classification", "operating income", "non-operating", "extraordinary items"],
        conclusion_template="Income statement should present revenues, expenses, gains, and losses in a manner that is clear, consistent, and in accordance with authoritative guidance.",
        reasoning_framework="""
The income statement must clearly distinguish between operating and non-operating items, and present material components separately. Extraordinary items are no longer permitted under US GAAP. Unusual or infrequent items are disclosed separately. Classification of items such as interest, dividends, and gains/losses must be consistent with the entity's business model and industry practice.
Multiple-step and single-step formats are permitted, but the chosen format must enhance understandability and comparability.
        """,
        key_factors=[
            "Nature of revenues and expenses",
            "Materiality and frequency",
            "Industry-specific guidance",
            "Consistency in classification",
            "Disclosure of significant items"
        ],
        primary_authority=["ASC 205", "ASC 220"],
        burden_holder="Reporting entity",
        adversary_position="Alternative classifications may be more informative or misleading.",
        counter_arguments=[
            "Consistency and comparability are paramount.",
            "Disclosures can supplement, but not replace, proper classification."
        ],
        resolution_strategy="Follow authoritative guidance, document policy choices, and provide adequate disclosures.",
        entity_scope="All entities preparing income statements under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Concepts Statement No. 6"
    ),
    DoctrineBlock(
        topic="Balance Sheet Classification and Presentation",
        keywords=["balance sheet", "classification", "current assets", "current liabilities", "presentation", "liquidity"],
        conclusion_template="Assets and liabilities are classified as current or noncurrent based on liquidity and maturity.",
        reasoning_framework="""
The balance sheet must present assets and liabilities in a classified format, distinguishing current from noncurrent based on their expected realization or settlement within one year or the operating cycle, whichever is longer. Certain items, such as deferred tax assets/liabilities and pension obligations, have specific classification rules. The presentation must provide clarity regarding liquidity and financial flexibility.
        """,
        key_factors=[
            "Expected realization/settlement period",
            "Operating cycle definition",
            "Specific guidance for certain items",
            "Materiality",
            "Industry practices"
        ],
        primary_authority=["ASC 210"],
        burden_holder="Reporting entity",
        adversary_position="Alternative classification may better reflect financial position.",
        counter_arguments=[
            "Authoritative guidance prescribes standard classifications.",
            "Disclosures can supplement, not replace, required classifications."
        ],
        resolution_strategy="Apply ASC 210 guidance, document judgments, and disclose significant classification policies.",
        entity_scope="All entities preparing balance sheets under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Concepts Statement No. 6"
    ),
    DoctrineBlock(
        topic="Statement of Cash Flows - ASC 230",
        keywords=["cash flows", "statement of cash flows", "ASC 230", "operating activities", "investing activities", "financing activities"],
        conclusion_template="Cash flows are classified and presented as operating, investing, or financing activities in accordance with ASC 230.",
        reasoning_framework="""
ASC 230 requires entities to present cash flows in three categories: operating, investing, and financing. Operating activities generally result from the principal revenue-producing activities. Investing activities relate to acquisition and disposal of long-term assets. Financing activities involve changes in equity and borrowings.
Entities may use the direct or indirect method for operating cash flows, but must reconcile net income to net cash from operating activities if the direct method is used. Noncash investing and financing activities must be disclosed separately.
        """,
        key_factors=[
            "Nature of cash flows",
            "Direct vs indirect method",
            "Noncash activities",
            "Industry-specific guidance",
            "Materiality"
        ],
        primary_authority=["ASC 230"],
        burden_holder="Reporting entity",
        adversary_position="Alternative classification of cash flows may be more informative.",
        counter_arguments=[
            "Consistency and comparability are required.",
            "Authoritative guidance prescribes standard classifications."
        ],
        resolution_strategy="Apply ASC 230 guidance, document policy choices, and disclose noncash activities.",
        entity_scope="All entities preparing statements of cash flows under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2016-15"
    ),
    DoctrineBlock(
        topic="DuPont Analysis Framework",
        keywords=["DuPont analysis", "ROE", "return on equity", "profitability", "efficiency", "leverage"],
        conclusion_template="DuPont analysis decomposes return on equity into profitability, efficiency, and leverage components.",
        reasoning_framework="""
The DuPont framework breaks down ROE into three components: net profit margin (profitability), asset turnover (efficiency), and equity multiplier (leverage). This analysis helps identify drivers of ROE and areas for improvement. It is used for internal performance evaluation and benchmarking.
ROE = (Net Income / Sales) * (Sales / Assets) * (Assets / Equity)
        """,
        key_factors=[
            "Net profit margin",
            "Asset turnover",
            "Equity multiplier",
            "Industry benchmarks",
            "Sustainability of components"
        ],
        primary_authority=["Financial statement analysis literature"],
        burden_holder="Analyst/management",
        adversary_position="ROE alone may not capture all risks or drivers.",
        counter_arguments=[
            "DuPont analysis provides deeper insight into ROE components.",
            "Supplement with additional ratios as needed."
        ],
        resolution_strategy="Use DuPont analysis as part of a broader financial analysis toolkit.",
        entity_scope="All entities subject to financial analysis.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DuPont Corporation, 1920s"
    ),
    DoctrineBlock(
        topic="Altman Z-Score Bankruptcy Prediction",
        keywords=["Altman Z-Score", "bankruptcy prediction", "financial distress", "credit risk", "ratio analysis"],
        conclusion_template="Altman Z-Score combines multiple financial ratios to assess bankruptcy risk.",
        reasoning_framework="""
The Altman Z-Score is a weighted sum of five key financial ratios: working capital/total assets, retained earnings/total assets, EBIT/total assets, market value of equity/total liabilities, and sales/total assets. The resulting score predicts the likelihood of bankruptcy, with lower scores indicating higher risk.
Z = 1.2*(WC/TA) + 1.4*(RE/TA) + 3.3*(EBIT/TA) + 0.6*(MVE/TL) + 1.0*(S/TA)
        """,
        key_factors=[
            "Working capital",
            "Retained earnings",
            "EBIT",
            "Market value of equity",
            "Sales"
        ],
        primary_authority=["Altman, E.I. (1968)"],
        burden_holder="Analyst/creditor",
        adversary_position="Z-Score may not capture all relevant risks or be applicable to all industries.",
        counter_arguments=[
            "Adjust model for industry-specific factors.",
            "Use in conjunction with qualitative analysis."
        ],
        resolution_strategy="Apply Z-Score as a screening tool, supplement with additional analysis.",
        entity_scope="Public manufacturing entities; adapted models for other sectors.",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="Altman, E.I. (1968)"
    ),
    DoctrineBlock(
        topic="Sarbanes-Oxley Section 404 - Internal Controls",
        keywords=["Sarbanes-Oxley", "SOX 404", "internal controls", "ICFR", "management assessment", "audit"],
        conclusion_template="Management must assess and report on the effectiveness of internal control over financial reporting; auditors must attest for accelerated filers.",
        reasoning_framework="""
SOX Section 404 requires management to design, implement, and maintain adequate internal control over financial reporting (ICFR), assess its effectiveness annually, and disclose the results. Accelerated filers must obtain auditor attestation. Controls must address risks of material misstatement, including entity-level and process-level controls. Deficiencies must be evaluated and disclosed as material weaknesses or significant deficiencies.
        """,
        key_factors=[
            "Design and operating effectiveness of controls",
            "Risk assessment",
            "Documentation and testing",
            "Deficiency evaluation",
            "Disclosure requirements"
        ],
        primary_authority=["Sarbanes-Oxley Act of 2002", "SEC Release No. 33-8238"],
        burden_holder="Management (and auditors for accelerated filers)",
        adversary_position="Controls are sufficient without formal documentation or testing.",
        counter_arguments=[
            "Documentation and testing are required for effective assessment.",
            "Auditor attestation provides independent assurance."
        ],
        resolution_strategy="Establish robust ICFR, document and test controls, remediate deficiencies, and disclose appropriately.",
        entity_scope="Public companies subject to SEC reporting; certain exemptions for smaller filers.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="SEC Release No. 33-8238"
    ),
    DoctrineBlock(
        topic="PCAOB Audit Standards - Materiality and Risk",
        keywords=["PCAOB", "audit standards", "materiality", "audit risk", "planning", "sampling"],
        conclusion_template="Auditors must assess materiality and audit risk to design effective audit procedures.",
        reasoning_framework="""
PCAOB standards require auditors to determine materiality for the financial statements as a whole and for particular classes of transactions, account balances, or disclosures. Audit risk is the risk that the auditor expresses an inappropriate opinion when the financial statements are materially misstated. Auditors must plan and perform the audit to obtain reasonable assurance, using risk assessment procedures, sampling, and substantive testing.
        """,
        key_factors=[
            "Quantitative and qualitative factors",
            "Risk of material misstatement",
            "Nature and extent of audit procedures",
            "Sampling techniques",
            "Professional judgment"
        ],
        primary_authority=["PCAOB AS 2105", "PCAOB AS 2110"],
        burden_holder="Auditor",
        adversary_position="Lower materiality thresholds or different risk assessments may be appropriate.",
        counter_arguments=[
            "Materiality is a matter of professional judgment.",
            "Audit risk must be reduced to an acceptably low level."
        ],
        resolution_strategy="Apply PCAOB standards, document judgments, and adjust procedures as needed.",
        entity_scope="Audits of public companies under PCAOB jurisdiction.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="PCAOB AS 2105, 2110"
    ),
    DoctrineBlock(
        topic="ASC 740 Income Tax Provision",
        keywords=["income tax", "ASC 740", "tax provision", "deferred tax", "uncertain tax positions"],
        conclusion_template="Entities must recognize current and deferred tax assets and liabilities, and account for uncertain tax positions.",
        reasoning_framework="""
ASC 740 requires recognition of current tax expense/benefit and deferred tax assets/liabilities for temporary differences between book and tax bases. Deferred tax assets are reduced by a valuation allowance if it is more likely than not that some portion will not be realized. Uncertain tax positions are recognized if it is more likely than not that the position will be sustained upon examination, and measured as the largest amount that is more than 50% likely to be realized.
        """,
        key_factors=[
            "Temporary differences",
            "Valuation allowance assessment",
            "Uncertain tax positions",
            "Tax rates and laws",
            "Recognition and measurement thresholds"
        ],
        primary_authority=["ASC 740"],
        burden_holder="Reporting entity",
        adversary_position="Deferred tax assets/liabilities should not be recognized or measured differently.",
        counter_arguments=[
            "ASC 740 prescribes recognition and measurement criteria.",
            "Valuation allowance is required for deferred tax assets not expected to be realized."
        ],
        resolution_strategy="Apply ASC 740 guidance, document tax positions, and disclose significant judgments.",
        entity_scope="All entities subject to income taxes under US GAAP.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FASB Interpretation No. 48"
    ),
    DoctrineBlock(
        topic="Multi-Entity Consolidation - ASC 810",
        keywords=["consolidation", "ASC 810", "variable interest entity", "VIE", "controlling financial interest"],
        conclusion_template="Entities must consolidate subsidiaries and VIEs when they have a controlling financial interest.",
        reasoning_framework="""
ASC 810 requires consolidation of entities in which the reporting entity has a controlling financial interest, either through voting interests or as the primary beneficiary of a variable interest entity (VIE). For VIEs, the primary beneficiary is the party with both the power to direct significant activities and the obligation to absorb losses or receive benefits.
Noncontrolling interests are presented separately in equity.
        """,
        key_factors=[
            "Voting rights",
            "Power to direct activities",
            "Obligation to absorb losses/receive benefits",
            "Related party relationships",
            "Noncontrolling interests"
        ],
        primary_authority=["ASC 810"],
        burden_holder="Parent/primary beneficiary",
        adversary_position="Entities should not be consolidated due to lack of legal ownership.",
        counter_arguments=[
            "Substance over form: control may exist without majority ownership.",
            "VIE model captures off-balance sheet risks."
        ],
        resolution_strategy="Apply ASC 810 guidance, assess VIE status, and document consolidation decisions.",
        entity_scope="All entities with subsidiaries or variable interests.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB Interpretation No. 46(R)"
    ),
    DoctrineBlock(
        topic="Foreign Currency Translation - ASC 830",
        keywords=["foreign currency", "translation", "ASC 830", "functional currency", "exchange rate", "cumulative translation adjustment"],
        conclusion_template="Foreign currency financial statements are translated using the functional currency approach; adjustments are recorded in OCI.",
        reasoning_framework="""
ASC 830 requires identification of the functional currency for each entity. Assets and liabilities are translated at the balance sheet date rate; income and expenses at average rates. Translation adjustments are recorded in other comprehensive income (OCI) until realized. Remeasurement is required when the reporting currency differs from the functional currency.
        """,
        key_factors=[
            "Functional currency determination",
            "Translation vs remeasurement",
            "Exchange rates used",
            "OCI treatment",
            "Disclosures"
        ],
        primary_authority=["ASC 830"],
        burden_holder="Reporting entity",
        adversary_position="Alternative translation methods may better reflect economic reality.",
        counter_arguments=[
            "ASC 830 prescribes the functional currency approach.",
            "Translation adjustments are not recognized in net income until realized."
        ],
        resolution_strategy="Apply ASC 830 guidance, document currency determinations, and disclose translation adjustments.",
        entity_scope="Entities with foreign operations or transactions.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 52"
    ),
    DoctrineBlock(
        topic="Fair Value Measurement - ASC 820",
        keywords=["fair value", "ASC 820", "valuation", "market participants", "level 1", "level 2", "level 3"],
        conclusion_template="Fair value is the price that would be received to sell an asset or paid to transfer a liability in an orderly transaction between market participants.",
        reasoning_framework="""
ASC 820 defines fair value as an exit price and establishes a hierarchy for inputs: Level 1 (quoted prices in active markets), Level 2 (observable inputs other than Level 1), and Level 3 (unobservable inputs). Entities must maximize observable inputs and minimize unobservable inputs. Valuation techniques include market, income, and cost approaches. Disclosures are required for valuation methods and inputs.
        """,
        key_factors=[
            "Principal or most advantageous market",
            "Observable vs unobservable inputs",
            "Valuation techniques",
            "Hierarchy classification",
            "Disclosures"
        ],
        primary_authority=["ASC 820"],
        burden_holder="Reporting entity",
        adversary_position="Alternative valuation methods may be more appropriate.",
        counter_arguments=[
            "ASC 820 requires maximizing observable inputs.",
            "Disclosures provide transparency for estimates."
        ],
        resolution_strategy="Apply ASC 820 hierarchy, document valuation methods, and provide required disclosures.",
        entity_scope="All entities measuring assets/liabilities at fair value under US GAAP.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 157"
    ),
    DoctrineBlock(
        topic="Goodwill Impairment Testing - ASC 350",
        keywords=["goodwill", "impairment", "ASC 350", "reporting unit", "fair value", "qualitative assessment"],
        conclusion_template="Goodwill is tested for impairment at the reporting unit level at least annually, or when triggering events occur.",
        reasoning_framework="""
ASC 350 requires entities to test goodwill for impairment at the reporting unit level. Entities may first perform a qualitative assessment (step zero) to determine if it is more likely than not that goodwill is impaired. If so, a quantitative test compares the fair value of the reporting unit to its carrying amount. Impairment is recognized if carrying amount exceeds fair value, limited to the amount of goodwill.
        """,
        key_factors=[
            "Reporting unit identification",
            "Qualitative indicators of impairment",
            "Fair value measurement",
            "Triggering events",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 350"],
        burden_holder="Reporting entity",
        adversary_position="Impairment testing is unnecessary or should be performed differently.",
        counter_arguments=[
            "Annual and interim testing is required.",
            "Qualitative assessment can reduce cost if no impairment is likely."
        ],
        resolution_strategy="Apply ASC 350 guidance, document assessments, and disclose impairment losses.",
        entity_scope="Entities with recorded goodwill.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2017-04"
    ),
    DoctrineBlock(
        topic="Stock-Based Compensation - ASC 718",
        keywords=["stock-based compensation", "ASC 718", "share-based payment", "fair value", "vesting", "expense recognition"],
        conclusion_template="Stock-based compensation is measured at grant-date fair value and recognized over the vesting period.",
        reasoning_framework="""
ASC 718 requires entities to measure the fair value of equity awards at the grant date and recognize compensation expense over the requisite service period (vesting period). For options, fair value is estimated using option-pricing models. Modifications, forfeitures, and non-employee awards have specific guidance.
        """,
        key_factors=[
            "Grant-date fair value",
            "Vesting conditions",
            "Option-pricing models",
            "Modifications and forfeitures",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 718"],
        burden_holder="Reporting entity",
        adversary_position="Intrinsic value or alternative measurement methods should be used.",
        counter_arguments=[
            "ASC 718 requires fair value measurement.",
            "Expense recognition aligns with service period."
        ],
        resolution_strategy="Apply ASC 718 guidance, use appropriate valuation models, and disclose assumptions.",
        entity_scope="Entities granting share-based payment awards.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 123(R)"
    ),
    DoctrineBlock(
        topic="Segment Reporting - ASC 280",
        keywords=["segment reporting", "ASC 280", "operating segment", "disclosure", "chief operating decision maker"],
        conclusion_template="Entities must disclose financial information about operating segments based on internal reporting to the chief operating decision maker.",
        reasoning_framework="""
ASC 280 requires identification of operating segments based on internal organization and reporting. Disclosures include segment profit or loss, assets, and certain items, reconciled to consolidated totals. Aggregation of segments is permitted if they have similar economic characteristics.
        """,
        key_factors=[
            "Internal reporting structure",
            "Chief operating decision maker",
            "Aggregation criteria",
            "Disclosure requirements",
            "Reconciliation to consolidated totals"
        ],
        primary_authority=["ASC 280"],
        burden_holder="Reporting entity",
        adversary_position="Alternative segmentation may provide more useful information.",
        counter_arguments=[
            "ASC 280 aligns with management's view.",
            "Aggregation is permitted only with similar characteristics."
        ],
        resolution_strategy="Apply ASC 280 criteria, document segment identification, and provide required disclosures.",
        entity_scope="Public entities; voluntary for others.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 131"
    ),
    DoctrineBlock(
        topic="Pension and Post-Retirement Benefits - ASC 715",
        keywords=["pension", "post-retirement benefits", "ASC 715", "defined benefit", "plan assets", "projected benefit obligation"],
        conclusion_template="Entities must recognize the funded status of defined benefit plans and disclose key assumptions and risks.",
        reasoning_framework="""
ASC 715 requires recognition of the funded status (plan assets less projected benefit obligation) on the balance sheet. Changes in funded status are recognized in OCI. Entities must use actuarial assumptions for discount rate, expected return, and compensation increases. Disclosures include plan descriptions, assumptions, and risks.
        """,
        key_factors=[
            "Funded status",
            "Actuarial assumptions",
            "Plan assets and obligations",
            "Recognition in OCI",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 715"],
        burden_holder="Plan sponsor",
        adversary_position="Alternative measurement or recognition methods may be preferable.",
        counter_arguments=[
            "ASC 715 prescribes recognition and measurement.",
            "Disclosures enhance transparency."
        ],
        resolution_strategy="Apply ASC 715 guidance, use reasonable assumptions, and disclose plan information.",
        entity_scope="Entities sponsoring defined benefit or post-retirement plans.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 158"
    ),
    DoctrineBlock(
        topic="ASC 815 Hedge Accounting",
        keywords=["hedge accounting", "ASC 815", "derivatives", "fair value hedge", "cash flow hedge", "effectiveness"],
        conclusion_template="Hedge accounting is permitted for qualifying relationships that are documented and highly effective.",
        reasoning_framework="""
ASC 815 permits hedge accounting for fair value, cash flow, and net investment hedges if the relationship is formally documented and highly effective. Hedge effectiveness must be assessed at inception and on an ongoing basis. Ineffective portions are recognized in earnings. Disclosures are required for objectives, strategies, and results.
        """,
        key_factors=[
            "Formal documentation",
            "Hedge effectiveness",
            "Type of hedge",
            "Measurement of ineffectiveness",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 815"],
        burden_holder="Reporting entity",
        adversary_position="Hedge accounting should be applied more broadly or narrowly.",
        counter_arguments=[
            "ASC 815 prescribes strict criteria for hedge accounting.",
            "Documentation and effectiveness testing are required."
        ],
        resolution_strategy="Apply ASC 815 guidance, document relationships, and assess effectiveness regularly.",
        entity_scope="Entities using derivatives for risk management.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 133"
    ),
    DoctrineBlock(
        topic="Going Concern Assessment - ASC 205-40",
        keywords=["going concern", "ASC 205-40", "substantial doubt", "disclosure", "mitigating plans"],
        conclusion_template="Management must evaluate whether there is substantial doubt about the entity's ability to continue as a going concern within one year after the financial statements are issued.",
        reasoning_framework="""
ASC 205-40 requires management to assess the entity's ability to meet obligations as they become due within one year after the date the financial statements are issued. If substantial doubt exists, management must consider mitigating plans and disclose the conditions and management's plans. If substantial doubt is alleviated by management's plans, disclosure is still required.
        """,
        key_factors=[
            "Cash flow projections",
            "Obligations due within one year",
            "Mitigating plans",
            "Disclosure requirements",
            "Timing of assessment"
        ],
        primary_authority=["ASC 205-40"],
        burden_holder="Management",
        adversary_position="Assessment should be based on longer/shorter periods or different criteria.",
        counter_arguments=[
            "ASC 205-40 prescribes a one-year look-forward period.",
            "Disclosure is required even if doubt is alleviated."
        ],
        resolution_strategy="Apply ASC 205-40 guidance, document assessment, and disclose as required.",
        entity_scope="All entities preparing financial statements under US GAAP.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2014-15"
    ),
    DoctrineBlock(
        topic="IFRS Convergence - Key Differences from US GAAP",
        keywords=["IFRS", "US GAAP", "convergence", "differences", "financial reporting"],
        conclusion_template="Entities must be aware of key differences between IFRS and US GAAP when preparing or reconciling financial statements.",
        reasoning_framework="""
Key differences exist between IFRS and US GAAP in areas such as revenue recognition, leases, financial instruments, impairment, and consolidation. Entities preparing dual reports or reconciling to IFRS must identify and disclose material differences. Convergence efforts have reduced, but not eliminated, differences.
        """,
        key_factors=[
            "Recognition and measurement differences",
            "Disclosure requirements",
            "Industry-specific guidance",
            "Transition provisions",
            "Materiality of differences"
        ],
        primary_authority=["IFRS Standards", "FASB/IASB publications"],
        burden_holder="Reporting entity",
        adversary_position="Differences are immaterial or can be ignored.",
        counter_arguments=[
            "Material differences must be disclosed.",
            "Users rely on reconciliations for comparability."
        ],
        resolution_strategy="Identify, quantify, and disclose material differences; monitor convergence developments.",
        entity_scope="Entities reporting under both IFRS and US GAAP.",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="SEC Release No. 33-8879"
    ),
    DoctrineBlock(
        topic="Liquidity Ratio Analysis",
        keywords=["liquidity", "current ratio", "quick ratio", "working capital", "short-term solvency"],
        conclusion_template="Liquidity ratios assess an entity's ability to meet short-term obligations.",
        reasoning_framework="""
Liquidity ratios such as the current ratio (current assets/current liabilities) and quick ratio (quick assets/current liabilities) provide insight into an entity's short-term financial health. Working capital analysis complements ratio analysis. Industry benchmarks and trends over time are important for interpretation.
        """,
        key_factors=[
            "Current assets and liabilities",
            "Composition of quick assets",
            "Industry benchmarks",
            "Trends over time",
            "Seasonality"
        ],
        primary_authority=["Financial statement analysis literature"],
        burden_holder="Analyst/creditor",
        adversary_position="Liquidity ratios may not capture all relevant risks.",
        counter_arguments=[
            "Ratios are starting points for analysis.",
            "Supplement with cash flow analysis and qualitative factors."
        ],
        resolution_strategy="Use liquidity ratios as part of a comprehensive financial analysis.",
        entity_scope="All entities subject to financial analysis.",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="Standard & Poor's, Moody's methodologies"
    ),
    DoctrineBlock(
        topic="Profitability Ratio Analysis",
        keywords=["profitability", "gross margin", "operating margin", "net margin", "return on assets", "return on equity"],
        conclusion_template="Profitability ratios measure an entity's ability to generate earnings relative to sales, assets, or equity.",
        reasoning_framework="""
Key profitability ratios include gross margin (gross profit/sales), operating margin (operating income/sales), net margin (net income/sales), return on assets (net income/assets), and return on equity (net income/equity). These ratios are used to assess performance, compare to peers, and evaluate trends.
        """,
        key_factors=[
            "Earnings measures",
            "Sales, assets, equity bases",
            "Industry benchmarks",
            "Trends over time",
            "Nonrecurring items"
        ],
        primary_authority=["Financial statement analysis literature"],
        burden_holder="Analyst/management",
        adversary_position="Ratios may be distorted by nonrecurring items or accounting policies.",
        counter_arguments=[
            "Adjust ratios for nonrecurring items.",
            "Disclose and explain significant fluctuations."
        ],
        resolution_strategy="Use profitability ratios in context, adjust for unusual items, and compare to benchmarks.",
        entity_scope="All entities subject to financial analysis.",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="Standard & Poor's, Moody's methodologies"
    ),
    DoctrineBlock(
        topic="Leverage and Solvency Ratio Analysis",
        keywords=["leverage", "solvency", "debt ratio", "debt to equity", "interest coverage", "financial risk"],
        conclusion_template="Leverage and solvency ratios assess an entity's ability to meet long-term obligations and manage financial risk.",
        reasoning_framework="""
Key ratios include debt ratio (total debt/total assets), debt to equity (total debt/total equity), and interest coverage (EBIT/interest expense). These ratios help assess the entity's capital structure, risk of default, and ability to service debt.
        """,
        key_factors=[
            "Total debt and equity",
            "Interest expense and coverage",
            "Industry norms",
            "Trends over time",
            "Off-balance sheet obligations"
        ],
        primary_authority=["Financial statement analysis literature"],
        burden_holder="Analyst/creditor",
        adversary_position="Ratios may not reflect all risks, such as off-balance sheet financing.",
        counter_arguments=[
            "Supplement ratio analysis with qualitative assessment.",
            "Disclose significant off-balance sheet items."
        ],
        resolution_strategy="Use leverage ratios as part of a comprehensive risk assessment.",
        entity_scope="All entities subject to financial analysis.",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="Standard & Poor's, Moody's methodologies"
    ),
    DoctrineBlock(
        topic="Variance Analysis - Budget vs Actual",
        keywords=["variance analysis", "budget", "actual", "performance measurement", "management accounting"],
        conclusion_template="Variance analysis identifies and explains differences between budgeted and actual results.",
        reasoning_framework="""
Variance analysis involves comparing actual results to budgeted amounts, identifying significant variances, and investigating causes. Variances may be favorable or unfavorable and can relate to price, quantity, or efficiency. Management uses variance analysis to improve operations and accountability.
        """,
        key_factors=[
            "Budgeted vs actual amounts",
            "Nature and magnitude of variances",
            "Root cause analysis",
            "Responsibility assignment",
            "Corrective actions"
        ],
        primary_authority=["Management accounting literature"],
        burden_holder="Management",
        adversary_position="Variance analysis may not capture all drivers of performance.",
        counter_arguments=[
            "Supplement with qualitative analysis.",
            "Focus on actionable variances."
        ],
        resolution_strategy="Use variance analysis as part of performance management and continuous improvement.",
        entity_scope="All entities using budgets for performance measurement.",
        confidence=0.90,
        confidence_zone="Moderate-High",
        controlling_precedent="IMA Statements on Management Accounting"
    ),
    DoctrineBlock(
        topic="Inventory Accounting - ASC 330",
        keywords=["inventory", "ASC 330", "lower of cost or market", "FIFO", "LIFO", "write-down"],
        conclusion_template="Inventory is measured at the lower of cost or net realizable value (except for LIFO and retail inventory methods).",
        reasoning_framework="""
ASC 330 requires inventory to be measured at the lower of cost or net realizable value (NRV), except for inventory measured using LIFO or the retail inventory method, which use lower of cost or market. Cost methods include FIFO, LIFO, and weighted average. Write-downs to NRV are recognized in the period incurred and cannot be reversed.
        """,
        key_factors=[
            "Cost determination method",
            "Net realizable value",
            "Write-downs and reversals",
            "Disclosure requirements",
            "Obsolescence and slow-moving inventory"
        ],
        primary_authority=["ASC 330"],
        burden_holder="Reporting entity",
        adversary_position="Alternative measurement methods may better reflect value.",
        counter_arguments=[
            "ASC 330 prescribes measurement and write-down rules.",
            "Reversals of write-downs are not permitted under US GAAP."
        ],
        resolution_strategy="Apply ASC 330 guidance, document cost methods, and disclose write-downs.",
        entity_scope="Entities with inventory under US GAAP.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2015-11"
    ),
    DoctrineBlock(
        topic="Business Combinations - ASC 805",
        keywords=["business combinations", "ASC 805", "acquisition method", "goodwill", "identifiable assets"],
        conclusion_template="Business combinations are accounted for using the acquisition method, recognizing identifiable assets and liabilities at fair value.",
        reasoning_framework="""
ASC 805 requires the acquisition method for business combinations: identify the acquirer, determine the acquisition date, recognize and measure identifiable assets acquired and liabilities assumed at fair value, and recognize goodwill or a gain from a bargain purchase. Transaction costs are expensed as incurred.
        """,
        key_factors=[
            "Identification of acquirer",
            "Acquisition date determination",
            "Fair value measurement",
            "Recognition of goodwill or gain",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 805"],
        burden_holder="Acquirer",
        adversary_position="Alternative methods (e.g., pooling of interests) should be used.",
        counter_arguments=[
            "ASC 805 prohibits pooling of interests.",
            "Acquisition method provides transparency."
        ],
        resolution_strategy="Apply ASC 805 guidance, document judgments, and disclose combination details.",
        entity_scope="Entities involved in business combinations under US GAAP.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 141(R)"
    ),
    DoctrineBlock(
        topic="Debt and Equity Classification - ASC 480/ASC 815",
        keywords=["debt", "equity", "classification", "ASC 480", "ASC 815", "financial instruments"],
        conclusion_template="Financial instruments are classified as debt or equity based on substance and contractual terms, with specific guidance for certain instruments.",
        reasoning_framework="""
ASC 480 requires certain financial instruments to be classified as liabilities, including mandatorily redeemable shares and certain obligations to repurchase equity. ASC 815 addresses derivatives and embedded features. Classification is based on substance over form and contractual terms, not legal form alone.
        """,
        key_factors=[
            "Contractual terms",
            "Redemption features",
            "Embedded derivatives",
            "Substance over form",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 480", "ASC 815"],
        burden_holder="Issuer",
        adversary_position="Legal form should determine classification.",
        counter_arguments=[
            "US GAAP emphasizes substance over form.",
            "Specific guidance for complex instruments."
        ],
        resolution_strategy="Apply ASC 480/815 guidance, analyze contractual terms, and disclose classification judgments.",
        entity_scope="Entities issuing complex financial instruments.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 150"
    ),
    DoctrineBlock(
        topic="Revenue Disaggregation and Contract Assets/Liabilities",
        keywords=["revenue disaggregation", "contract assets", "contract liabilities", "ASC 606", "disclosure"],
        conclusion_template="Entities must disaggregate revenue and disclose contract assets and liabilities in accordance with ASC 606.",
        reasoning_framework="""
ASC 606 requires disaggregation of revenue into categories that depict how revenue and cash flows are affected by economic factors. Entities must disclose opening and closing balances of contract assets and liabilities, and significant changes. Disclosures provide users with insight into the nature, amount, timing, and uncertainty of revenue.
        """,
        key_factors=[
            "Nature and timing of revenue streams",
            "Contract asset/liability balances",
            "Significant changes in balances",
            "Disclosure requirements",
            "Judgments and estimates"
        ],
        primary_authority=["ASC 606"],
        burden_holder="Reporting entity",
        adversary_position="Disaggregation is unnecessary or burdensome.",
        counter_arguments=[
            "Disaggregation enhances transparency.",
            "Required for compliance with ASC 606."
        ],
        resolution_strategy="Apply ASC 606 disclosure guidance, document categories, and disclose contract balances.",
        entity_scope="Entities recognizing revenue under ASC 606.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2014-09"
    ),
    DoctrineBlock(
        topic="Subsequent Events - ASC 855",
        keywords=["subsequent events", "ASC 855", "recognition", "disclosure", "reporting period"],
        conclusion_template="Entities must evaluate events after the balance sheet date but before financial statements are issued, for recognition or disclosure.",
        reasoning_framework="""
ASC 855 requires entities to identify subsequent events occurring after the balance sheet date but before the financial statements are issued or available to be issued. Recognized subsequent events provide additional evidence about conditions existing at the balance sheet date. Nonrecognized events are disclosed if material.
        """,
        key_factors=[
            "Timing of events",
            "Nature of event (recognized vs nonrecognized)",
            "Materiality",
            "Disclosure requirements",
            "Date financial statements are issued"
        ],
        primary_authority=["ASC 855"],
        burden_holder="Reporting entity",
        adversary_position="Subsequent events should not be recognized or disclosed.",
        counter_arguments=[
            "ASC 855 prescribes recognition and disclosure criteria.",
            "Users need information about significant subsequent events."
        ],
        resolution_strategy="Apply ASC 855 guidance, document event evaluation, and disclose as required.",
        entity_scope="All entities preparing financial statements under US GAAP.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 165"
    ),
    DoctrineBlock(
        topic="Materiality in Financial Reporting",
        keywords=["materiality", "financial reporting", "disclosure", "judgment", "qualitative factors"],
        conclusion_template="Materiality is a matter of professional judgment, considering both quantitative and qualitative factors.",
        reasoning_framework="""
Materiality is defined as the magnitude of an omission or misstatement that would influence the judgment of a reasonable user. Both quantitative (size) and qualitative (nature, circumstances) factors are considered. Materiality affects recognition, measurement, and disclosure decisions throughout financial reporting.
        """,
        key_factors=[
            "Magnitude of item",
            "Nature and circumstances",
            "User perspective",
            "Cumulative effects",
            "Professional judgment"
        ],
        primary_authority=["FASB Concepts Statement No. 8", "SEC SAB Topic 1.M"],
        burden_holder="Management/auditor",
        adversary_position="Strict quantitative thresholds should apply.",
        counter_arguments=[
            "Qualitative factors can render small amounts material.",
            "Materiality is context-dependent."
        ],
        resolution_strategy="Apply professional judgment, document rationale, and disclose significant judgments.",
        entity_scope="All entities preparing financial statements.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Concepts Statement No. 8"
    ),
    DoctrineBlock(
        topic="Earnings Per Share (EPS) - ASC 260",
        keywords=["earnings per share", "EPS", "ASC 260", "basic EPS", "diluted EPS", "weighted average shares"],
        conclusion_template="Entities must present basic and diluted EPS on the face of the income statement for each period presented.",
        reasoning_framework="""
ASC 260 requires calculation of basic EPS (net income available to common shareholders divided by weighted average shares outstanding) and diluted EPS (including the effect of potentially dilutive securities). Entities must disclose the methods and assumptions used.
        """,
        key_factors=[
            "Net income available to common shareholders",
            "Weighted average shares",
            "Potentially dilutive securities",
            "Disclosure requirements",
            "Antidilutive effects"
        ],
        primary_authority=["ASC 260"],
        burden_holder="Reporting entity",
        adversary_position="EPS is not meaningful for all entities or should be calculated differently.",
        counter_arguments=[
            "ASC 260 prescribes calculation and disclosure.",
            "EPS is a key performance measure for public companies."
        ],
        resolution_strategy="Apply ASC 260 guidance, document calculations, and disclose assumptions.",
        entity_scope="Public entities; voluntary for others.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 128"
    ),
    DoctrineBlock(
        topic="Related Party Transactions - ASC 850",
        keywords=["related party", "transactions", "ASC 850", "disclosure", "conflict of interest"],
        conclusion_template="Entities must disclose material related party transactions, relationships, and terms.",
        reasoning_framework="""
ASC 850 requires disclosure of material transactions with related parties, including the nature of the relationship, description of transactions, dollar amounts, and any amounts due to or from related parties. Disclosure is required even if transactions are conducted at arm's length.
        """,
        key_factors=[
            "Nature of relationship",
            "Materiality of transactions",
            "Terms and conditions",
            "Amounts due to/from related parties",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 850"],
        burden_holder="Reporting entity",
        adversary_position="Disclosure is unnecessary if transactions are at arm's length.",
        counter_arguments=[
            "Users need information about potential conflicts of interest.",
            "Disclosure is required regardless of arm's length terms."
        ],
        resolution_strategy="Identify related parties, document transactions, and disclose as required.",
        entity_scope="All entities preparing financial statements under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 57"
    ),
    DoctrineBlock(
        topic="Impairment of Long-Lived Assets - ASC 360",
        keywords=["impairment", "long-lived assets", "ASC 360", "recoverability test", "fair value"],
        conclusion_template="Long-lived assets are tested for impairment when events or changes in circumstances indicate that carrying amount may not be recoverable.",
        reasoning_framework="""
ASC 360 requires a recoverability test when indicators of impairment exist. If undiscounted cash flows are less than carrying amount, an impairment loss is recognized for the excess of carrying amount over fair value. Assets held for sale are measured at lower of carrying amount or fair value less costs to sell.
        """,
        key_factors=[
            "Indicators of impairment",
            "Recoverability test",
            "Fair value measurement",
            "Held for sale classification",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 360"],
        burden_holder="Reporting entity",
        adversary_position="Impairment testing is unnecessary or should use different methods.",
        counter_arguments=[
            "ASC 360 prescribes recoverability and measurement steps.",
            "Disclosure is required for impairment losses."
        ],
        resolution_strategy="Apply ASC 360 guidance, document impairment assessments, and disclose losses.",
        entity_scope="Entities with long-lived assets under US GAAP.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 144"
    ),
    DoctrineBlock(
        topic="Accounting Changes and Error Corrections - ASC 250",
        keywords=["accounting changes", "error corrections", "ASC 250", "retrospective application", "disclosure"],
        conclusion_template="Entities must account for changes in accounting principle retrospectively and correct errors in prior-period financial statements.",
        reasoning_framework="""
ASC 250 requires retrospective application for changes in accounting principle unless impracticable. Error corrections are treated as prior-period adjustments and require restatement of prior financial statements. Disclosures must explain the nature, reason, and effects of changes and corrections.
        """,
        key_factors=[
            "Nature of change or error",
            "Retrospective application",
            "Restatement of prior periods",
            "Disclosure requirements",
            "Impracticability exceptions"
        ],
        primary_authority=["ASC 250"],
        burden_holder="Reporting entity",
        adversary_position="Prospective application or limited disclosure is sufficient.",
        counter_arguments=[
            "Retrospective application enhances comparability.",
            "Disclosure is required for transparency."
        ],
        resolution_strategy="Apply ASC 250 guidance, restate as required, and disclose changes and corrections.",
        entity_scope="All entities preparing financial statements under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 154"
    ),
    DoctrineBlock(
        topic="Noncontrolling Interests - ASC 810",
        keywords=["noncontrolling interest", "ASC 810", "consolidation", "equity", "presentation"],
        conclusion_template="Noncontrolling interests are presented as a separate component of equity in consolidated financial statements.",
        reasoning_framework="""
ASC 810 requires noncontrolling interests to be presented in the consolidated balance sheet within equity, separately from the parent’s equity. Net income attributable to noncontrolling interests is shown separately in the income statement. Changes in ownership that do not result in loss of control are accounted for as equity transactions.
        """,
        key_factors=[
            "Ownership structure",
            "Presentation in equity",
            "Attribution of net income",
            "Disclosure requirements",
            "Changes in ownership"
        ],
        primary_authority=["ASC 810"],
        burden_holder="Parent entity",
        adversary_position="Noncontrolling interests should be presented outside equity.",
        counter_arguments=[
            "ASC 810 requires presentation within equity.",
            "Separate disclosure enhances transparency."
        ],
        resolution_strategy="Apply ASC 810 guidance, present and disclose noncontrolling interests appropriately.",
        entity_scope="Entities with consolidated subsidiaries under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 160"
    ),
    DoctrineBlock(
        topic="Discontinued Operations - ASC 205-20",
        keywords=["discontinued operations", "ASC 205-20", "component", "disposal", "presentation"],
        conclusion_template="A component of an entity that has been disposed of or is classified as held for sale is reported as a discontinued operation if it represents a strategic shift.",
        reasoning_framework="""
ASC 205-20 requires reporting of discontinued operations when a component has been disposed of or is classified as held for sale and the disposal represents a strategic shift that has a major effect on operations and financial results. Results of discontinued operations are presented separately in the income statement and statement of cash flows.
        """,
        key_factors=[
            "Nature of component",
            "Strategic shift assessment",
            "Timing of disposal",
            "Presentation and disclosure",
            "Measurement of disposal group"
        ],
        primary_authority=["ASC 205-20"],
        burden_holder="Reporting entity",
        adversary_position="Alternative presentation or broader/narrower definition of discontinued operations.",
        counter_arguments=[
            "ASC 205-20 prescribes criteria and presentation.",
            "Separate disclosure enhances comparability."
        ],
        resolution_strategy="Apply ASC 205-20 guidance, document strategic shift, and disclose results.",
        entity_scope="Entities disposing of components under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2014-08"
    ),
    DoctrineBlock(
        topic="Interim Reporting - ASC 270",
        keywords=["interim reporting", "ASC 270", "quarterly", "interim financial statements", "disclosure"],
        conclusion_template="Interim financial statements are prepared using the same accounting principles as annual statements, with certain modifications and disclosures.",
        reasoning_framework="""
ASC 270 requires interim financial statements to be prepared using the same accounting principles as annual statements, except for accounting for income taxes and certain estimates. Disclosures focus on significant changes since the last annual report. Interim periods are integral parts of the annual period.
        """,
        key_factors=[
            "Consistency of accounting principles",
            "Interim period estimates",
            "Income tax accounting",
            "Disclosure requirements",
            "Materiality"
        ],
        primary_authority=["ASC 270"],
        burden_holder="Reporting entity",
        adversary_position="Different principles or limited disclosure should be permitted.",
        counter_arguments=[
            "Consistency enhances comparability.",
            "Disclosures focus on significant changes."
        ],
        resolution_strategy="Apply ASC 270 guidance, use consistent principles, and disclose significant changes.",
        entity_scope="Entities preparing interim financial statements under US GAAP.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 3"
    ),
    DoctrineBlock(
        topic="Accounting for Intangible Assets - ASC 350",
        keywords=["intangible assets", "ASC 350", "amortization", "indefinite-lived", "impairment"],
        conclusion_template="Intangible assets with finite lives are amortized; indefinite-lived intangibles are tested for impairment annually.",
        reasoning_framework="""
ASC 350 requires intangible assets with finite useful lives to be amortized over their estimated useful lives. Indefinite-lived intangibles are not amortized but tested for impairment at least annually or when triggering events occur. Impairment is recognized if carrying amount exceeds fair value.
        """,
        key_factors=[
            "Useful life assessment",
            "Amortization method",
            "Impairment indicators",
            "Fair value measurement",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 350"],
        burden_holder="Reporting entity",
        adversary_position="All intangibles should be amortized or tested differently.",
        counter_arguments=[
            "ASC 350 distinguishes between finite and indefinite-lived intangibles.",
            "Annual impairment testing is required for indefinite-lived assets."
        ],
        resolution_strategy="Apply ASC 350 guidance, document useful life assessments, and disclose impairment losses.",
        entity_scope="Entities with intangible assets under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 142"
    ),
    DoctrineBlock(
        topic="Environmental Liabilities - ASC 410",
        keywords=["environmental liabilities", "ASC 410", "asset retirement obligation", "ARO", "contingency"],
        conclusion_template="Entities must recognize a liability for asset retirement obligations when incurred, measured at fair value.",
        reasoning_framework="""
ASC 410 requires recognition of a liability for the fair value of an asset retirement obligation (ARO) when incurred, typically when the asset is placed in service. The liability is accreted over time and the related asset is depreciated. Environmental remediation liabilities are recognized when a loss is probable and reasonably estimable.
        """,
        key_factors=[
            "Timing of obligation incurrence",
            "Fair value measurement",
            "Accretion and depreciation",
            "Probability and estimability",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 410"],
        burden_holder="Reporting entity",
        adversary_position="Recognition should be delayed or based on different criteria.",
        counter_arguments=[
            "ASC 410 prescribes recognition when incurred.",
            "Fair value measurement enhances comparability."
        ],
        resolution_strategy="Apply ASC 410 guidance, estimate fair value, and disclose AROs and remediation liabilities.",
        entity_scope="Entities with asset retirement or environmental obligations.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 143"
    ),
    DoctrineBlock(
        topic="Revenue Gross vs Net Presentation",
        keywords=["revenue", "gross", "net", "principal", "agent", "ASC 606"],
        conclusion_template="Entities must determine whether to present revenue gross or net based on whether they are principal or agent in the transaction.",
        reasoning_framework="""
ASC 606 requires entities to assess whether they control the specified good or service before it is transferred to the customer (principal) or arrange for another party to provide it (agent). Principals recognize revenue gross; agents recognize net revenue for the fee or commission.
        """,
        key_factors=[
            "Control of goods or services",
            "Principal vs agent indicators",
            "Contractual terms",
            "Disclosure requirements",
            "Judgment and estimates"
        ],
        primary_authority=["ASC 606"],
        burden_holder="Reporting entity",
        adversary_position="Gross/net presentation should be based on legal form or other criteria.",
        counter_arguments=[
            "Control is the key determinant under ASC 606.",
            "Disclosures provide transparency for judgments."
        ],
        resolution_strategy="Apply ASC 606 principal/agent guidance, document assessments, and disclose presentation basis.",
        entity_scope="Entities recognizing revenue under ASC 606.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2016-08"
    ),
    DoctrineBlock(
        topic="Accounting for Debt Modifications and Extinguishments - ASC 470",
        keywords=["debt", "modification", "extinguishment", "ASC 470", "gain or loss"],
        conclusion_template="Entities must assess whether a debt modification is a troubled debt restructuring, a modification, or an extinguishment, and account accordingly.",
        reasoning_framework="""
ASC 470 requires entities to evaluate whether changes to debt terms constitute a troubled debt restructuring, a modification, or an extinguishment. Modifications that are not substantial are accounted for prospectively; substantial modifications or extinguishments result in derecognition of old debt and recognition of new debt, with gain or loss recognized.
        """,
        key_factors=[
            "Nature and extent of modification",
            "Troubled debt restructuring criteria",
            "Substantiality assessment",
            "Gain or loss recognition",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 470"],
        burden_holder="Debtor",
        adversary_position="All modifications should be treated as extinguishments or vice versa.",
        counter_arguments=[
            "ASC 470 provides criteria for classification.",
            "Disclosure enhances transparency."
        ],
        resolution_strategy="Apply ASC 470 guidance, assess modifications, and disclose results.",
        entity_scope="Entities modifying or extinguishing debt under US GAAP.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 140"
    ),
    DoctrineBlock(
        topic="Accounting for Research and Development Costs - ASC 730",
        keywords=["research and development", "R&D", "ASC 730", "expense", "capitalization"],
        conclusion_template="Research and development costs are expensed as incurred, except for certain software development costs.",
        reasoning_framework="""
ASC 730 requires R&D costs to be expensed as incurred, except for certain software development costs after technological feasibility is established (ASC 985-20). Capitalization is not permitted for most R&D activities. Disclosures are required for total R&D expense and significant arrangements.
        """,
        key_factors=[
            "Nature of R&D activities",
            "Software development exceptions",
            "Expense recognition",
            "Disclosure requirements",
            "Materiality"
        ],
        primary_authority=["ASC 730"],
        burden_holder="Reporting entity",
        adversary_position="R&D costs should be capitalized to match benefits.",
        counter_arguments=[
            "ASC 730 prohibits capitalization except as specified.",
            "Expense recognition enhances comparability."
        ],
        resolution_strategy="Apply ASC 730 guidance, expense R&D costs, and disclose as required.",
        entity_scope="Entities incurring R&D costs under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 2"
    ),
    DoctrineBlock(
        topic="Accounting for Contingencies - ASC 450",
        keywords=["contingencies", "ASC 450", "loss contingency", "probable", "reasonably estimable"],
        conclusion_template="Entities must accrue a loss contingency if it is probable and the amount can be reasonably estimated.",
        reasoning_framework="""
ASC 450 requires accrual of a loss contingency when it is probable that a liability has been incurred and the amount can be reasonably estimated. If only a range of loss can be estimated, the minimum amount is accrued. Disclosures are required for material contingencies not accrued.
        """,
        key_factors=[
            "Probability of loss",
            "Reasonable estimability",
            "Range of loss",
            "Disclosure requirements",
            "Materiality"
        ],
        primary_authority=["ASC 450"],
        burden_holder="Reporting entity",
        adversary_position="Accrual should be delayed until more certain.",
        counter_arguments=[
            "ASC 450 requires accrual when criteria are met.",
            "Disclosure is required for unaccrued material contingencies."
        ],
        resolution_strategy="Apply ASC 450 guidance, document assessments, and disclose contingencies.",
        entity_scope="All entities preparing financial statements under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 5"
    ),
    DoctrineBlock(
        topic="Segment Profit or Loss Measurement - ASC 280",
        keywords=["segment profit", "segment loss", "ASC 280", "measurement", "disclosure"],
        conclusion_template="Segment profit or loss is measured consistently with the internal reports provided to the chief operating decision maker.",
        reasoning_framework="""
ASC 280 requires that segment profit or loss be measured on the same basis as internal reports used by the chief operating decision maker. Adjustments and eliminations are disclosed, and reconciliations to consolidated amounts are provided.
        """,
        key_factors=[
            "Internal reporting basis",
            "Adjustments and eliminations",
            "Disclosure requirements",
            "Reconciliation to consolidated results",
            "Consistency"
        ],
        primary_authority=["ASC 280"],
        burden_holder="Reporting entity",
        adversary_position="External GAAP measures should be used for all segments.",
        counter_arguments=[
            "ASC 280 aligns with management's view.",
            "Reconciliations provide transparency."
        ],
        resolution_strategy="Apply ASC 280 guidance, disclose measurement basis, and reconcile to consolidated results.",
        entity_scope="Public entities; voluntary for others.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 131"
    ),
    DoctrineBlock(
        topic="Accounting for Nonmonetary Transactions - ASC 845",
        keywords=["nonmonetary transactions", "ASC 845", "fair value", "commercial substance", "exchange"],
        conclusion_template="Nonmonetary exchanges are measured at fair value if the transaction has commercial substance.",
        reasoning_framework="""
ASC 845 requires nonmonetary exchanges to be measured at fair value unless the exchange lacks commercial substance, fair value is not determinable, or the transaction is an exchange of inventory in the same line of business. Gains and losses are recognized as appropriate.
        """,
        key_factors=[
            "Commercial substance",
            "Determinability of fair value",
            "Nature of assets exchanged",
            "Recognition of gains/losses",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 845"],
        burden_holder="Reporting entity",
        adversary_position="Historical cost or other measures should be used.",
        counter_arguments=[
            "ASC 845 prescribes fair value measurement for exchanges with commercial substance.",
            "Exceptions are narrowly defined."
        ],
        resolution_strategy="Apply ASC 845 guidance, assess commercial substance, and disclose as required.",
        entity_scope="Entities engaging in nonmonetary exchanges under US GAAP.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 153"
    ),
    DoctrineBlock(
        topic="Accounting for Software Costs - ASC 350-40/985-20",
        keywords=["software costs", "ASC 350-40", "ASC 985-20", "capitalization", "amortization"],
        conclusion_template="Software development costs are capitalized after technological feasibility is established (internal-use or sale), and amortized over the useful life.",
        reasoning_framework="""
ASC 350-40 covers internal-use software; ASC 985-20 covers software to be sold. Costs incurred during preliminary project stage are expensed; costs incurred after technological feasibility are capitalized. Amortization begins when software is ready for use or sale. Impairment is recognized if carrying amount exceeds fair value.
        """,
        key_factors=[
            "Stage of development",
            "Technological feasibility",
            "Capitalization criteria",
            "Amortization method",
            "Impairment assessment"
        ],
        primary_authority=["ASC 350-40", "ASC 985-20"],
        burden_holder="Reporting entity",
        adversary_position="All software costs should be expensed or capitalized.",
        counter_arguments=[
            "ASC 350-40/985-20 distinguish stages and criteria.",
            "Amortization aligns cost with benefit period."
        ],
        resolution_strategy="Apply ASC 350-40/985-20 guidance, document stages, and disclose software costs.",
        entity_scope="Entities developing software for internal use or sale.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 86"
    ),
    DoctrineBlock(
        topic="Accounting for Investments - ASC 320/321/323",
        keywords=["investments", "ASC 320", "ASC 321", "ASC 323", "equity method", "fair value"],
        conclusion_template="Investments are classified and accounted for based on intent and ability: fair value, equity method, or cost.",
        reasoning_framework="""
ASC 320 covers debt securities (trading, available-for-sale, held-to-maturity); ASC 321 covers equity securities (fair value through net income); ASC 323 covers equity method investments (20-50% ownership or significant influence). Classification determines measurement and recognition of gains/losses.
        """,
        key_factors=[
            "Type of investment",
            "Ownership percentage",
            "Intent and ability",
            "Measurement basis",
            "Disclosure requirements"
        ],
        primary_authority=["ASC 320", "ASC 321", "ASC 323"],
        burden_holder="Investor",
        adversary_position="Alternative classification or measurement should be used.",
        counter_arguments=[
            "ASC 320/321/323 provide clear criteria.",
            "Disclosure enhances transparency."
        ],
        resolution_strategy="Apply relevant ASC guidance, classify investments, and disclose as required.",
        entity_scope="Entities holding investments under US GAAP.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 115, 124, 94"
    ),
    DoctrineBlock(
        topic="Accounting for Deferred Compensation Arrangements",
        keywords=["deferred compensation", "liability", "vesting", "expense recognition", "disclosure"],
        conclusion_template="Deferred compensation arrangements are recognized as liabilities and expensed over the vesting period.",
        reasoning_framework="""
Deferred compensation arrangements, such as nonqualified plans, are recognized as liabilities when earned and expensed over the vesting period. The liability is measured at the present value of future payments. Disclosures include plan terms, amounts recognized, and payment timing.
        """,
        key_factors=[
            "Vesting conditions",
            "Present value measurement",
            "Expense recognition",
            "Disclosure requirements",
            "Payment timing"
        ],
        primary_authority=["EITF 97-14", "ASC 710"],
        burden_holder="Employer",
        adversary_position="Expense recognition should be delayed until payment.",
        counter_arguments=[
            "Expense recognition aligns with service period.",
            "Liability reflects obligation to employees."
        ],
        resolution_strategy="Apply relevant guidance, accrue liability, and disclose plan terms.",
        entity_scope="Entities with deferred compensation arrangements.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EITF 97-14"
    ),
    DoctrineBlock(
        topic="Accounting for Treasury Stock - ASC 505-30",
        keywords=["treasury stock", "ASC 505-30", "cost method", "par value method", "equity"],
        conclusion_template="Treasury stock is recorded at cost or par value and presented as a deduction from equity.",
        reasoning_framework="""
ASC 505-30 permits either the cost method or par value method for accounting for treasury stock. Treasury shares are not assets and are presented as a deduction from total equity. Gains and losses on reissuance are not recognized in income but may affect additional paid-in capital.
        """,
        key_factors=[
            "Acquisition method",
            "Presentation in equity",
            "Reissuance of shares",
            "Disclosure requirements",
            "Restrictions on treasury shares"
        ],
        primary_authority=["ASC 505-30"],
        burden_holder="Reporting entity",
        adversary_position="Alternative presentation or recognition of gains/losses.",
        counter_arguments=[
            "ASC 505-30 prescribes presentation as a deduction from equity.",
            "Gains/losses are not recognized in income."
        ],
        resolution_strategy="Apply ASC 505-30 guidance, present treasury stock appropriately, and disclose as required.",
        entity_scope="Entities acquiring treasury shares under US GAAP.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 150"
    ),
    DoctrineBlock(
        topic="Accounting for Government Grants",
        keywords=["government grants", "recognition", "measurement", "disclosure", "ASC 958"],
        conclusion_template="Government grants are recognized when there is reasonable assurance that conditions will be met and the grant will be received.",
        reasoning_framework="""
US GAAP does not have comprehensive guidance for business entities; ASC 958 applies to not-for-profits. For business entities, analogy to IAS 20 is common: recognize grant income when reasonable assurance exists that conditions will be met. Disclosures include nature, terms, and amounts recognized.
        """,
        key_factors=[
            "Reasonable assurance of receipt",
            "Conditions attached to grant",
            "Timing of recognition",
            "Disclosure requirements",
            "Measurement of grant income"
        ],
        primary_authority=["ASC 958", "IAS 20 (by analogy)"],
        burden_holder="Recipient entity",
        adversary_position="Recognition should be delayed until cash is received.",
        counter_arguments=[
            "Reasonable assurance is sufficient for recognition.",
            "Disclosure provides transparency for judgments."
        ],
        resolution_strategy="Apply ASC 958 or IAS 20 by analogy, document judgments, and disclose grant details.",
        entity_scope="Entities receiving government grants.",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="IAS 20 (by analogy)"
    ),
    DoctrineBlock(
        topic="Accounting for Share Repurchases (Buybacks)",
        keywords=["share repurchase", "buyback", "treasury stock", "ASC 505-30", "equity"],
        conclusion_template="Share repurchases are recorded as treasury stock at cost and reduce shareholders' equity.",
        reasoning_framework="""
When an entity repurchases its own shares, the shares are recorded as treasury stock at cost and presented as a deduction from equity. If reissued, any excess or deficiency over cost is recorded in additional paid-in capital. No gain or loss is recognized in income.
        """,
        key_factors=[
            "Cost of repurchase",
            "Presentation as treasury stock",
            "Reissuance accounting",
            "Disclosure requirements",
            "Legal restrictions"
        ],
        primary_authority=["ASC 505-30"],
        burden_holder="Reporting entity",
        adversary_position="Gains/losses on repurchase should be recognized in income.",
        counter_arguments=[
            "ASC 505-30 prohibits income statement recognition.",
            "Equity presentation reflects substance."
        ],
        resolution_strategy="Apply ASC 505-30 guidance, present buybacks as treasury stock, and disclose as required.",
        entity_scope="Entities repurchasing shares under US GAAP.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB Statement No. 150"
    ),
    DoctrineBlock(
        topic="Accounting for Nonrefundable Advance Payments",
        keywords=["nonrefundable advance", "revenue recognition", "ASC 606", "contract liability", "breakage"],
        conclusion_template="Nonrefundable advance payments are recognized as contract liabilities and revenue is recognized when performance obligations are satisfied.",
        reasoning_framework="""
Under ASC 606, nonrefundable advance payments (e.g., upfront fees, gift cards) are recorded as contract liabilities until the entity satisfies its performance obligations. Breakage (expected non-redemption) is recognized as revenue when it is probable that the customer will not exercise its rights.
        """,
        key_factors=[
            "Nature of advance payment",
            "Performance obligations",
            "Breakage estimation",
            "Disclosure requirements",
            "Timing of revenue recognition"
        ],
        primary_authority=["ASC 606"],
        burden_holder="Reporting entity",
        adversary_position="Advance payments should be recognized as revenue upon receipt.",
        counter_arguments=[
            "Revenue is recognized when obligations are satisfied.",
            "Breakage is recognized only when probable."
        ],
        resolution_strategy="Apply ASC 606 guidance, record contract liabilities, and disclose revenue recognition policies.",
        entity_scope="Entities receiving nonrefundable advances under ASC 606.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FASB ASU 2016-04"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctr