from dataclasses import dataclass, field
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
        topic="Arps Decline Curve Analysis - Exponential",
        keywords=["Arps", "decline curve", "exponential", "production forecasting", "DCA"],
        conclusion_template="The exponential decline model is appropriate when the decline rate remains constant over the production period.",
        reasoning_framework=(
            "The exponential decline model, as formulated by J.J. Arps in 1945, assumes that the production rate declines at a constant percentage per unit time. "
            "This model is mathematically represented as q = q_i * exp(-D * t), where q is the production rate at time t, q_i is the initial production rate, and D is the decline rate. "
            "The model is best suited for wells in boundary-dominated flow or reservoirs with stable pressure support. "
            "Key steps include: (1) plotting historical production data, (2) fitting the exponential model using regression or curve-fitting techniques, (3) validating the fit with statistical measures (R^2, residuals), "
            "(4) extrapolating future production, and (5) calculating reserves and economic indicators based on the forecast. "
            "The model's simplicity makes it widely used, but it may not capture early-time transient behavior or late-time tailing effects. "
            "The analyst must ensure that the decline rate is indeed constant and that the reservoir conditions justify the exponential assumption. "
            "Sensitivity analysis should be performed to assess the impact of uncertainty in D and q_i. "
            "The model is less appropriate for unconventional reservoirs with variable decline rates. "
            "Regulatory and reporting standards (e.g., SEC, PRMS) may require justification of the chosen decline method."
        ),
        key_factors=[
            "Historical production data quality",
            "Stability of decline rate",
            "Reservoir drive mechanism",
            "Length of production history",
            "Fit to exponential model"
        ],
        primary_authority=[
            "Arps, J.J. (1945), Analysis of Decline Curves, Transactions of the AIME",
            "Society of Petroleum Engineers (SPE) Monograph Vol. 3",
            "SEC Regulation S-X Rule 4-10(a)"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="The decline rate is not constant; exponential model overestimates reserves.",
        counter_arguments=[
            "Demonstrate statistical fit to exponential model",
            "Show reservoir pressure data supporting boundary-dominated flow",
            "Provide sensitivity analysis on decline rate"
        ],
        resolution_strategy="Validate model fit with historical data and document assumptions; consider alternative models if fit is poor.",
        entity_scope="Conventional oil & gas wells with stable production history",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Arps (1945); SEC Staff Accounting Bulletin No. 113"
    ),
    DoctrineBlock(
        topic="Arps Decline Curve Analysis - Hyperbolic",
        keywords=["Arps", "decline curve", "hyperbolic", "b-factor", "production forecasting"],
        conclusion_template="The hyperbolic decline model should be used when the decline rate decreases over time, as indicated by a b-factor between 0 and 1.",
        reasoning_framework=(
            "The hyperbolic decline model extends the exponential model by introducing a variable decline rate, characterized by the b-factor (0 < b < 1). "
            "The production rate is given by q = q_i / (1 + b*D_i*t)^(1/b), where D_i is the initial decline rate. "
            "This model is suitable for reservoirs exhibiting transient flow or variable decline rates, commonly seen in unconventional reservoirs. "
            "The fitting process involves: (1) plotting production data on log-log scales, (2) estimating q_i, D_i, and b using nonlinear regression, (3) checking for overfitting, "
            "(4) validating the model with out-of-sample data, and (5) performing sensitivity analysis on the b-factor. "
            "A higher b-factor indicates a slower reduction in decline rate over time. "
            "The model can overestimate reserves if b is set too high; regulatory guidelines often cap b at 1.0. "
            "The analyst should justify the chosen b-factor with analog wells and reservoir characteristics. "
            "Hyperbolic decline is widely accepted for shale and tight reservoirs but requires careful calibration."
        ),
        key_factors=[
            "Production data variability",
            "Estimated b-factor",
            "Reservoir heterogeneity",
            "Model fit quality",
            "Regulatory limits on b-factor"
        ],
        primary_authority=[
            "Arps, J.J. (1945), Analysis of Decline Curves",
            "SPE Decline Curve Analysis Best Practices",
            "SEC Staff Accounting Bulletin No. 113"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="The b-factor is too high, leading to inflated EUR estimates.",
        counter_arguments=[
            "Provide analog well comparisons",
            "Demonstrate fit to historical data",
            "Apply regulatory cap on b-factor"
        ],
        resolution_strategy="Document b-factor selection process and compare with industry benchmarks.",
        entity_scope="Unconventional and heterogeneous reservoirs",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Arps (1945); SEC SAB 113"
    ),
    DoctrineBlock(
        topic="Arps Decline Curve Analysis - Harmonic",
        keywords=["Arps", "decline curve", "harmonic", "production forecasting"],
        conclusion_template="The harmonic decline model is appropriate when the decline rate decreases rapidly over time, typically for mature wells.",
        reasoning_framework=(
            "The harmonic decline model is a special case of the hyperbolic model with b=1. "
            "It is represented by q = q_i / (1 + D_i*t), where q_i is the initial production rate and D_i is the initial decline rate. "
            "This model is best applied to mature wells where the decline rate slows significantly as production continues. "
            "The fitting process includes: (1) plotting production data, (2) fitting the harmonic model, (3) validating with residual analysis, "
            "(4) comparing with exponential and hyperbolic models, and (5) justifying the choice based on reservoir behavior. "
            "The harmonic model tends to predict higher EURs due to the slow decline at late times. "
            "Regulatory authorities may scrutinize the use of harmonic decline due to its optimistic forecasts. "
            "Analysts should provide robust justification for its use, including analogs and reservoir studies."
        ),
        key_factors=[
            "Late-time production behavior",
            "Model fit to historical data",
            "Reservoir maturity",
            "Comparison with other decline models",
            "Regulatory acceptance"
        ],
        primary_authority=[
            "Arps, J.J. (1945), Analysis of Decline Curves",
            "SPE Decline Curve Analysis Best Practices"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Harmonic decline overestimates reserves for this well.",
        counter_arguments=[
            "Demonstrate late-time production flattening",
            "Compare forecasts with analog wells",
            "Provide sensitivity analysis"
        ],
        resolution_strategy="Use harmonic decline only when supported by data and reservoir understanding.",
        entity_scope="Mature oil & gas wells",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="Arps (1945)"
    ),
    DoctrineBlock(
        topic="b-factor Estimation in Decline Curve Analysis",
        keywords=["b-factor", "decline curve", "hyperbolic", "model calibration"],
        conclusion_template="The b-factor should be estimated using robust statistical methods and validated against analog wells and reservoir characteristics.",
        reasoning_framework=(
            "The b-factor determines the curvature of the hyperbolic decline model and is critical for accurate production forecasting. "
            "Estimation methods include nonlinear regression on historical production data, visual fitting on log-log plots, and comparison with analog wells. "
            "The analyst should: (1) ensure sufficient production history, (2) avoid overfitting by limiting the number of parameters, (3) use cross-validation, "
            "(4) compare estimated b-factor with regional analogs, and (5) document the estimation process. "
            "Regulatory guidelines may cap the b-factor (typically at 1.0) to prevent overestimation of reserves. "
            "Uncertainty analysis should be performed to assess the impact of b-factor variability on EUR and economic outcomes."
        ),
        key_factors=[
            "Length and quality of production history",
            "Analog well data",
            "Reservoir heterogeneity",
            "Model fit statistics",
            "Regulatory caps on b-factor"
        ],
        primary_authority=[
            "SPE Decline Curve Analysis Best Practices",
            "SEC Staff Accounting Bulletin No. 113"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="The b-factor is not supported by data or analogs.",
        counter_arguments=[
            "Present statistical fit metrics",
            "Show analog well comparisons",
            "Apply regulatory caps"
        ],
        resolution_strategy="Document estimation methodology and justify b-factor selection with supporting evidence.",
        entity_scope="All wells using hyperbolic decline analysis",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Monograph Vol. 3"
    ),
    DoctrineBlock(
        topic="Initial Production (IP) Rate Determination",
        keywords=["initial production", "IP rate", "production forecasting", "well performance"],
        conclusion_template="The initial production rate should be determined from stabilized production data, excluding early-time transients and operational upsets.",
        reasoning_framework=(
            "The IP rate is a key input for decline curve analysis and reserve estimation. "
            "It should be based on a representative period after well cleanup and stabilization, typically the first 30 days of production (IP30) or after reaching steady-state flow. "
            "Exclude data affected by well interventions, shut-ins, or mechanical issues. "
            "Use daily or monthly production data, and apply statistical smoothing if necessary to remove noise. "
            "Document the selection window and justify its representativeness. "
            "If the well has not stabilized, use analog wells or type curves to estimate a reasonable IP rate."
        ),
        key_factors=[
            "Well stabilization period",
            "Data quality and completeness",
            "Operational events",
            "Analog well performance",
            "Type curve matching"
        ],
        primary_authority=[
            "SPE Guidelines for Production Data Analysis",
            "PRMS (Petroleum Resources Management System)"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="The selected IP rate is not representative of stabilized production.",
        counter_arguments=[
            "Show data exclusion criteria",
            "Provide analog well comparisons",
            "Demonstrate statistical smoothing"
        ],
        resolution_strategy="Clearly document IP rate selection and provide supporting data.",
        entity_scope="All producing wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="PRMS 2018 Section 3.1"
    ),
    DoctrineBlock(
        topic="Estimated Ultimate Recovery (EUR) Calculation",
        keywords=["EUR", "estimated ultimate recovery", "reserves", "decline curve"],
        conclusion_template="EUR should be calculated by integrating the decline curve to economic limit, using validated model parameters.",
        reasoning_framework=(
            "EUR is the total recoverable volume of hydrocarbons expected from a well or reservoir. "
            "It is calculated by integrating the chosen decline curve (exponential, hyperbolic, or harmonic) from the start of production to the economic limit. "
            "The economic limit is defined by the point at which net revenue becomes zero or negative. "
            "Key steps: (1) select and fit the decline model, (2) determine model parameters (q_i, D, b), (3) define economic limit rate, "
            "(4) integrate the model to the economic limit, and (5) validate results with analog wells and material balance if available. "
            "Document all assumptions and sensitivity analyses. "
            "Regulatory and reporting standards require transparent and auditable EUR calculations."
        ),
        key_factors=[
            "Model parameter accuracy",
            "Economic limit definition",
            "Production data quality",
            "Analog well validation",
            "Sensitivity analysis"
        ],
        primary_authority=[
            "PRMS 2018 Section 3.2",
            "SEC Regulation S-X Rule 4-10(a)"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="EUR is overstated due to optimistic decline parameters.",
        counter_arguments=[
            "Provide sensitivity analysis",
            "Compare with analog wells",
            "Document economic limit assumptions"
        ],
        resolution_strategy="Use conservative assumptions and document all calculations.",
        entity_scope="All wells and reservoirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="PRMS 2018; SEC SAB 113"
    ),
    DoctrineBlock(
        topic="Type Curve Construction",
        keywords=["type curve", "production forecasting", "analog wells", "well performance"],
        conclusion_template="Type curves should be constructed from normalized production data of analog wells with similar reservoir and completion characteristics.",
        reasoning_framework=(
            "Type curve construction involves aggregating and normalizing production data from a set of analog wells to create a representative production profile. "
            "Steps include: (1) selecting analog wells with similar geology, completion, and operational history, (2) normalizing production rates and cumulative production (e.g., per 1,000 ft lateral), "
            "(3) aligning production timelines (e.g., from first production), (4) calculating statistical measures (P10, P50, P90), and (5) constructing the type curve using median or mean values. "
            "Type curves are used for forecasting new wells and for reserves classification. "
            "Document selection criteria, normalization methods, and statistical measures. "
            "Update type curves regularly as more data becomes available."
        ),
        key_factors=[
            "Analog well selection",
            "Normalization methodology",
            "Reservoir and completion similarity",
            "Statistical aggregation",
            "Documentation of process"
        ],
        primary_authority=[
            "SPE Monograph Vol. 3",
            "PRMS 2018 Section 3.3"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Type curve does not represent the subject well's performance.",
        counter_arguments=[
            "Show analog selection criteria",
            "Provide normalization methodology",
            "Compare with subject well data"
        ],
        resolution_strategy="Regularly update type curves and document all assumptions.",
        entity_scope="Development planning and forecasting",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Monograph Vol. 3"
    ),
    DoctrineBlock(
        topic="Net Revenue Interest (NRI) Calculation",
        keywords=["NRI", "net revenue interest", "royalty", "ownership", "revenue allocation"],
        conclusion_template="NRI is calculated as the working interest minus the royalty burden and other non-operating interests.",
        reasoning_framework=(
            "Net Revenue Interest (NRI) represents the portion of production revenue allocated to the working interest owner after deducting royalties and other burdens. "
            "The formula is NRI = Working Interest (WI) * (1 - Total Royalty Burden). "
            "Identify all royalty owners and their respective percentages, including overriding royalties and non-participating interests. "
            "Verify ownership through title documents, division orders, and lease agreements. "
            "Document all calculations and ensure they align with legal agreements. "
            "Update NRI calculations if ownership changes or new burdens are recorded."
        ),
        key_factors=[
            "Working interest percentage",
            "Royalty and overriding royalty percentages",
            "Title and lease documentation",
            "Division order accuracy",
            "Ownership changes"
        ],
        primary_authority=[
            "Lease agreements",
            "Division orders",
            "Texas Natural Resources Code"
        ],
        burden_holder="Land Department",
        adversary_position="NRI calculation does not reflect all royalty burdens.",
        counter_arguments=[
            "Provide title documentation",
            "Show calculation breakdown",
            "Verify with division order"
        ],
        resolution_strategy="Audit ownership and royalty records; update NRI as needed.",
        entity_scope="All working interest owners",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Texas Natural Resources Code §91.402"
    ),
    DoctrineBlock(
        topic="Working Interest Cash Flow Calculation",
        keywords=["working interest", "cash flow", "revenue", "expenses", "ownership"],
        conclusion_template="Working interest cash flow is calculated as gross revenue times NRI, less all applicable expenses and taxes.",
        reasoning_framework=(
            "Working interest cash flow analysis involves calculating the net cash generated from a well or project attributable to the working interest owner. "
            "Steps: (1) calculate gross revenue from production volumes and commodity prices, (2) apply NRI to determine the owner's share, "
            "(3) subtract lease operating expenses (LOE), severance and ad valorem taxes, gathering/transportation/processing fees, and overhead charges, "
            "(4) account for capital expenditures (CAPEX) as appropriate, and (5) calculate net cash flow for each period. "
            "Document all expense assumptions and tax rates. "
            "Use actual expense data when available; otherwise, use reasonable estimates based on historical averages."
        ),
        key_factors=[
            "Gross revenue calculation",
            "NRI accuracy",
            "Expense and tax assumptions",
            "CAPEX allocation",
            "Documentation of methodology"
        ],
        primary_authority=[
            "COPAS Accounting Procedures",
            "Texas Comptroller Oil & Gas Tax Rules"
        ],
        burden_holder="Accounting Department",
        adversary_position="Cash flow calculation omits certain expenses or uses incorrect NRI.",
        counter_arguments=[
            "Provide detailed expense breakdown",
            "Show NRI calculation",
            "Reconcile with financial statements"
        ],
        resolution_strategy="Reconcile cash flow models with actual accounting records.",
        entity_scope="All working interest owners",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="COPAS Accounting Procedures 2005"
    ),
    DoctrineBlock(
        topic="Severance Tax Rates - Texas",
        keywords=["severance tax", "Texas", "oil and gas", "tax rates", "state tax"],
        conclusion_template="Texas imposes a 4.6% severance tax on oil and a 7.5% severance tax on natural gas, calculated on gross value at the wellhead.",
        reasoning_framework=(
            "Severance tax is a state-imposed tax on the extraction of oil and gas resources. "
            "In Texas, the standard oil severance tax rate is 4.6% of the market value of oil at the wellhead, and the gas severance tax rate is 7.5% of the market value of gas. "
            "Condensate is taxed at the oil rate. "
            "Reduced rates may apply for certain enhanced recovery projects, low-producing wells, or high-cost gas wells. "
            "Tax is calculated monthly and remitted to the Texas Comptroller. "
            "Accurate reporting of production volumes and sales prices is essential. "
            "Operators must stay current with legislative changes affecting severance tax rates."
        ),
        key_factors=[
            "Commodity type (oil, gas, condensate)",
            "Market value determination",
            "Eligibility for reduced rates",
            "Accurate production reporting",
            "Compliance with Texas Comptroller rules"
        ],
        primary_authority=[
            "Texas Tax Code §201 (Gas) and §202 (Oil)",
            "Texas Comptroller Oil & Gas Tax Rules"
        ],
        burden_holder="Operator",
        adversary_position="Incorrect tax rate or value basis applied.",
        counter_arguments=[
            "Provide tax code references",
            "Show calculation methodology",
            "Demonstrate eligibility for reduced rates"
        ],
        resolution_strategy="Regularly review tax code updates and audit tax filings.",
        entity_scope="All oil and gas operators in Texas",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Tax Code §201, §202"
    ),
    DoctrineBlock(
        topic="Ad Valorem Tax Deduction",
        keywords=["ad valorem tax", "property tax", "deduction", "Texas", "oil and gas"],
        conclusion_template="Ad valorem taxes are deductible as an expense against gross revenue for working interest cash flow calculations.",
        reasoning_framework=(
            "Ad valorem taxes are property taxes assessed by local taxing authorities on the value of oil and gas interests. "
            "These taxes are typically billed annually and are based on the appraised value of the mineral interest, including reserves and equipment. "
            "For cash flow and economic analysis, ad valorem taxes are treated as a deductible expense. "
            "Operators should use actual tax bills when available, or estimate based on recent assessments. "
            "Document the source and calculation of ad valorem tax deductions in all financial models."
        ),
        key_factors=[
            "Appraised property value",
            "Local tax rates",
            "Assessment methodology",
            "Actual tax bills",
            "Expense documentation"
        ],
        primary_authority=[
            "Texas Property Tax Code",
            "County Appraisal District Guidelines"
        ],
        burden_holder="Operator/Working Interest Owner",
        adversary_position="Ad valorem deduction is overstated or not supported by documentation.",
        counter_arguments=[
            "Provide tax bills or assessment notices",
            "Show calculation methodology",
            "Reconcile with county records"
        ],
        resolution_strategy="Use actual tax bills and maintain documentation for audits.",
        entity_scope="All Texas oil and gas properties",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas Property Tax Code §23.175"
    ),
    DoctrineBlock(
        topic="Gathering, Transportation, and Processing Deductions",
        keywords=["gathering", "transportation", "processing", "midstream", "deductions", "netback"],
        conclusion_template="Gathering, transportation, and processing (GTP) costs are deductible from gross revenue when calculating net revenue to the working interest owner.",
        reasoning_framework=(
            "GTP costs represent the expenses incurred to move hydrocarbons from the wellhead to the point of sale and to process them into marketable products. "
            "These costs are typically deducted from gross revenue in the calculation of net revenue. "
            "The deduction should be based on actual invoices or contractual rates with midstream providers. "
            "Operators must ensure that only allowable costs are deducted, as defined in the lease or operating agreement. "
            "Document all GTP deductions and reconcile with financial statements."
        ),
        key_factors=[
            "Contractual terms for GTP costs",
            "Actual invoices and rates",
            "Lease agreement provisions",
            "Expense documentation",
            "Reconciliation with revenue statements"
        ],
        primary_authority=[
            "Lease agreements",
            "COPAS Accounting Procedures"
        ],
        burden_holder="Operator/Working Interest Owner",
        adversary_position="Non-allowable costs are being deducted from revenue.",
        counter_arguments=[
            "Provide lease and contract documentation",
            "Show actual invoices",
            "Reconcile deductions with agreements"
        ],
        resolution_strategy="Deduct only contractually-allowed costs and maintain supporting documentation.",
        entity_scope="All working interest owners",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="COPAS Accounting Procedures 2005"
    ),
    DoctrineBlock(
        topic="COPAS Overhead Charges",
        keywords=["COPAS", "overhead", "joint interest billing", "JIB", "accounting"],
        conclusion_template="COPAS overhead charges should be applied as specified in the joint operating agreement and in accordance with the latest COPAS guidelines.",
        reasoning_framework=(
            "COPAS (Council of Petroleum Accountants Societies) overhead charges compensate the operator for administrative costs associated with managing joint operations. "
            "The applicable overhead rates and chargeable items are specified in the joint operating agreement (JOA) and updated periodically by COPAS bulletins. "
            "Operators should apply the agreed-upon rates for drilling and producing overhead, and only charge allowable costs. "
            "All charges must be documented and included in joint interest billings (JIBs). "
            "Disputes should be resolved by reference to the JOA and COPAS bulletins in effect at the time of the charge."
        ),
        key_factors=[
            "JOA provisions",
            "COPAS bulletin in effect",
            "Allowable and non-allowable costs",
            "Documentation in JIBs",
            "Auditability"
        ],
        primary_authority=[
            "Joint Operating Agreement",
            "COPAS Accounting Procedures and Bulletins"
        ],
        burden_holder="Operator",
        adversary_position="Overhead charges exceed allowable rates or include non-allowable costs.",
        counter_arguments=[
            "Provide JOA and COPAS references",
            "Show calculation of overhead charges",
            "Document all charges in JIBs"
        ],
        resolution_strategy="Strictly adhere to JOA and COPAS guidelines; resolve disputes through audit.",
        entity_scope="All parties to a joint operating agreement",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="COPAS Bulletin 5"
    ),
    DoctrineBlock(
        topic="Lease Operating Expense (LOE) Deduction",
        keywords=["LOE", "lease operating expense", "deduction", "cash flow", "expenses"],
        conclusion_template="LOE should be deducted from gross revenue based on actual incurred costs, or reasonable estimates if actuals are unavailable.",
        reasoning_framework=(
            "LOE includes all recurring costs necessary to operate and maintain a producing lease, such as labor, utilities, repairs, chemicals, and insurance. "
            "For cash flow and economic analysis, LOE should be based on actual historical costs when available. "
            "If actuals are unavailable (e.g., for new wells), use estimates based on analog wells or industry benchmarks. "
            "Document all LOE assumptions and update estimates as actual data becomes available. "
            "Exclude capital expenditures and non-recurring costs from LOE."
        ),
        key_factors=[
            "Actual LOE data",
            "Analog well benchmarks",
            "Expense categorization",
            "Documentation of assumptions",
            "Exclusion of CAPEX"
        ],
        primary_authority=[
            "COPAS Accounting Procedures",
            "SPE Guidelines for Economic Evaluation"
        ],
        burden_holder="Operator/Working Interest Owner",
        adversary_position="LOE deduction is overstated or includes non-allowable items.",
        counter_arguments=[
            "Provide detailed LOE breakdown",
            "Show analog benchmarks",
            "Reconcile with accounting records"
        ],
        resolution_strategy="Use actual LOE data when available and maintain documentation.",
        entity_scope="All producing leases",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="COPAS Accounting Procedures 2005"
    ),
    DoctrineBlock(
        topic="CAPEX Recovery - AFE vs Actual",
        keywords=["CAPEX", "capital expenditure", "AFE", "actual costs", "recovery"],
        conclusion_template="CAPEX recovery should be based on actual incurred costs, with AFE amounts used only as estimates until actuals are available.",
        reasoning_framework=(
            "Capital expenditures (CAPEX) are initially estimated using an Authorization for Expenditure (AFE) prior to project execution. "
            "Actual costs may differ from AFE estimates due to operational changes, market conditions, or unforeseen events. "
            "For financial reporting and payout calculations, use actual incurred CAPEX. "
            "Reconcile AFE estimates with actuals post-project, and document all variances. "
            "Update economic models and payout calculations as actual CAPEX data becomes available."
        ),
        key_factors=[
            "AFE estimate accuracy",
            "Actual cost tracking",
            "Variance documentation",
            "Timely updates to models",
            "Reconciliation process"
        ],
        primary_authority=[
            "COPAS Accounting Procedures",
            "Internal Capital Tracking Policies"
        ],
        burden_holder="Operator/Project Manager",
        adversary_position="CAPEX recovery is based on outdated or inaccurate estimates.",
        counter_arguments=[
            "Provide actual cost reports",
            "Show reconciliation with AFE",
            "Document variance explanations"
        ],
        resolution_strategy="Update models with actual costs and maintain audit trail.",
        entity_scope="All capital projects",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="COPAS Accounting Procedures 2005"
    ),
    DoctrineBlock(
        topic="Payout Calculation",
        keywords=["payout", "cost recovery", "cash flow", "project economics"],
        conclusion_template="Payout occurs when cumulative net cash flow equals cumulative capital investment; calculations should be updated with actual costs and revenues.",
        reasoning_framework=(
            "Payout is the point at which the working interest owner's cumulative net cash flow equals the cumulative capital investment (CAPEX). "
            "Calculate payout by summing net cash flow (after all expenses and taxes) each period and comparing to cumulative CAPEX. "
            "Update calculations with actual cost and revenue data as it becomes available. "
            "Document the payout calculation and provide sensitivity analysis for key variables (commodity prices, LOE, taxes). "
            "Payout timing may affect ownership reversion or other contractual terms."
        ),
        key_factors=[
            "Accurate net cash flow calculation",
            "Actual CAPEX data",
            "Expense and tax assumptions",
            "Sensitivity analysis",
            "Contractual payout provisions"
        ],
        primary_authority=[
            "Joint Operating Agreement",
            "COPAS Accounting Procedures"
        ],
        burden_holder="Operator/Working Interest Owner",
        adversary_position="Payout calculation uses outdated or estimated data.",
        counter_arguments=[
            "Provide actual cash flow and CAPEX data",
            "Show calculation methodology",
            "Document contractual provisions"
        ],
        resolution_strategy="Update payout models regularly and maintain documentation.",
        entity_scope="All working interest owners",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="COPAS Accounting Procedures 2005"
    ),
    DoctrineBlock(
        topic="Rate of Return Analysis",
        keywords=["rate of return", "ROR", "IRR", "project economics", "investment analysis"],
        conclusion_template="Rate of return should be calculated using discounted cash flow methods, with assumptions documented and sensitivity analysis performed.",
        reasoning_framework=(
            "Rate of return (ROR), including internal rate of return (IRR), measures the profitability of an investment. "
            "Calculate ROR by discounting net cash flows to present value and solving for the discount rate that sets NPV to zero. "
            "Use actual or forecasted cash flows, and document all assumptions (commodity prices, LOE, taxes, CAPEX). "
            "Perform sensitivity analysis on key variables to assess risk and uncertainty. "
            "Compare ROR to company hurdle rates and industry benchmarks. "
            "Document all calculations and update as new data becomes available."
        ),
        key_factors=[
            "Cash flow forecast accuracy",
            "Discount rate selection",
            "Assumption documentation",
            "Sensitivity analysis",
            "Benchmarking"
        ],
        primary_authority=[
            "SPE Guidelines for Economic Evaluation",
            "PRMS 2018 Section 3.4"
        ],
        burden_holder="Project Evaluator",
        adversary_position="ROR calculation is based on unrealistic assumptions.",
        counter_arguments=[
            "Provide sensitivity analysis",
            "Document all assumptions",
            "Compare with benchmarks"
        ],
        resolution_strategy="Use conservative assumptions and document all calculations.",
        entity_scope="All oil and gas projects",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE Guidelines for Economic Evaluation"
    ),
    DoctrineBlock(
        topic="PV-10 Valuation",
        keywords=["PV-10", "present value", "discounted cash flow", "valuation", "reserves"],
        conclusion_template="PV-10 is calculated by discounting future net cash flows at a 10% annual rate, before income taxes, as required by SEC reporting standards.",
        reasoning_framework=(
            "PV-10 is a standard measure of the present value of future net cash flows from proved oil and gas reserves, discounted at 10% per annum. "
            "The calculation excludes income taxes and uses SEC-mandated pricing (12-month average, first-day-of-month prices). "
            "Steps: (1) forecast net cash flows for each period, (2) apply a 10% annual discount rate, (3) sum discounted cash flows, and (4) exclude income taxes. "
            "Document all assumptions and reconcile with reserve reports. "
            "PV-10 is used for reserve reporting, asset valuation, and investment analysis."
        ),
        key_factors=[
            "Accurate cash flow forecast",
            "SEC pricing assumptions",
            "Exclusion of income taxes",
            "Discount rate application",
            "Documentation and reconciliation"
        ],
        primary_authority=[
            "SEC Regulation S-X Rule 4-10(a)",
            "PRMS 2018 Section 3.5"
        ],
        burden_holder="Reserves Evaluator",
        adversary_position="PV-10 calculation does not comply with SEC requirements.",
        counter_arguments=[
            "Provide calculation worksheet",
            "Show SEC pricing assumptions",
            "Document exclusion of income taxes"
        ],
        resolution_strategy="Follow SEC and PRMS guidelines; document all calculations.",
        entity_scope="SEC reserve reporting",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="SEC Regulation S-X Rule 4-10(a)"
    ),
    DoctrineBlock(
        topic="NYMEX Strip Pricing",
        keywords=["NYMEX", "strip pricing", "commodity prices", "forecast", "valuation"],
        conclusion_template="NYMEX strip pricing should be used for internal forecasts and asset valuations, but SEC reporting requires 12-month average prices.",
        reasoning_framework=(
            "NYMEX strip pricing refers to the use of forward futures prices for oil and gas as published by the New York Mercantile Exchange. "
            "Strip pricing is commonly used for internal economic evaluations, budgeting, and asset valuations, as it reflects market expectations. "
            "For SEC reserve reporting, use the 12-month average of historical first-day-of-month prices. "
            "Document the source and date of NYMEX strip prices used in forecasts. "
            "Perform sensitivity analysis to assess the impact of price volatility on economic outcomes."
        ),
        key_factors=[
            "Source and date of strip prices",
            "SEC vs internal reporting requirements",
            "Price volatility",
            "Documentation of assumptions",
            "Sensitivity analysis"
        ],
        primary_authority=[
            "SEC Regulation S-X Rule 4-10(a)",
            "Company Internal Policies"
        ],
        burden_holder="Reserves/Economic Evaluator",
        adversary_position="Strip pricing does not comply with SEC reporting standards.",
        counter_arguments=[
            "Document use of strip pricing for internal purposes",
            "Provide SEC-compliant price decks for reporting",
            "Show sensitivity analysis"
        ],
        resolution_strategy="Use strip pricing for internal analysis and SEC pricing for external reporting.",
        entity_scope="Asset valuation and internal forecasting",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SEC Regulation S-X Rule 4-10(a)"
    ),
    DoctrineBlock(
        topic="Basis Differential Adjustment",
        keywords=["basis differential", "price adjustment", "commodity pricing", "netback"],
        conclusion_template="Basis differentials should be applied to NYMEX or index prices to reflect the actual sales price received at the point of sale.",
        reasoning_framework=(
            "Basis differential is the adjustment between a commodity's benchmark price (e.g., NYMEX) and the actual price received at the sales point. "
            "Adjustments account for location, quality, and transportation differences. "
            "Document the source and calculation of basis differentials, using actual sales data or published indices. "
            "Apply the differential consistently in all cash flow and valuation models. "
            "Update basis differentials regularly to reflect market conditions."
        ),
        key_factors=[
            "Source of basis differential",
            "Consistency of application",
            "Market conditions",
            "Documentation",
            "Frequency of updates"
        ],
        primary_authority=[
            "Sales contracts",
            "Platts and Argus indices"
        ],
        burden_holder="Economic Evaluator",
        adversary_position="Basis differentials are outdated or not representative.",
        counter_arguments=[
            "Provide recent sales data",
            "Show calculation methodology",
            "Update differentials regularly"
        ],
        resolution_strategy="Use actual sales data and update basis differentials as needed.",
        entity_scope="All commodity pricing models",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Sales contract terms"
    ),
    DoctrineBlock(
        topic="BTU Adjustment for Gas Revenue",
        keywords=["BTU adjustment", "gas revenue", "heating value", "sales price"],
        conclusion_template="Gas revenue should be adjusted for BTU content based on contract specifications and actual gas analysis.",
        reasoning_framework=(
            "Natural gas is sold based on energy content, typically measured in MMBtu. "
            "If the gas stream's BTU content differs from the contract standard (usually 1,000 BTU/scf), a BTU adjustment is applied to the sales price. "
            "Obtain actual gas analysis data and apply the contract formula to calculate the adjustment. "
            "Document the source of gas analysis and contract terms. "
            "Update BTU adjustments as new analysis data becomes available."
        ),
        key_factors=[
            "Actual gas BTU content",
            "Contractual BTU standard",
            "Gas analysis frequency",
            "Documentation",
            "Adjustment formula"
        ],
        primary_authority=[
            "Gas sales contracts",
            "API MPMS Chapter 14"
        ],
        burden_holder="Operator/Revenue Accountant",
        adversary_position="BTU adjustment is not supported by current gas analysis.",
        counter_arguments=[
            "Provide recent gas analysis reports",
            "Show contract adjustment formula",
            "Document all calculations"
        ],
        resolution_strategy="Use current gas analysis and contract terms for all adjustments.",
        entity_scope="All gas sales",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API MPMS Chapter 14"
    ),
    DoctrineBlock(
        topic="Condensate Yield Projection",
        keywords=["condensate yield", "gas condensate", "production forecasting", "liquids recovery"],
        conclusion_template="Condensate yield should be projected based on historical gas/condensate ratios and reservoir fluid properties.",
        reasoning_framework=(
            "Condensate yield is typically expressed as barrels of condensate per MMcf of produced gas. "
            "Project yield by analyzing historical production data and gas/condensate ratios. "
            "Adjust for changes in reservoir pressure, temperature, and fluid properties over time. "
            "Use reservoir simulation or material balance if available. "
            "Document all assumptions and update projections as new data becomes available."
        ),
        key_factors=[
            "Historical gas/condensate ratio",
            "Reservoir pressure and temperature",
            "Fluid properties",
            "Production data quality",
            "Modeling methodology"
        ],
        primary_authority=[
            "SPE Guidelines for Production Forecasting",
            "PRMS 2018 Section 3.6"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Condensate yield projection is not supported by data or fluid analysis.",
        counter_arguments=[
            "Provide historical production data",
            "Show fluid property analysis",
            "Document modeling approach"
        ],
        resolution_strategy="Update projections with new data and document all assumptions.",
        entity_scope="Gas condensate reservoirs",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE Guidelines for Production Forecasting"
    ),
    # Additional doctrine blocks for comprehensive coverage (20+ more for 40+ total)
    DoctrineBlock(
        topic="Economic Limit Rate Determination",
        keywords=["economic limit", "rate determination", "production cutoff", "cash flow"],
        conclusion_template="The economic limit rate is the production rate at which net revenue becomes zero or negative, and should be calculated using current cost and price assumptions.",
        reasoning_framework=(
            "The economic limit rate is the minimum production rate at which a well or lease remains economically viable. "
            "Calculate by setting net revenue (after all expenses and taxes) to zero and solving for the corresponding production rate. "
            "Include all recurring expenses (LOE, taxes, GTP costs) and use current or forecasted commodity prices. "
            "Document all assumptions and update the economic limit rate as costs or prices change. "
            "The economic limit rate defines the endpoint for EUR and reserve calculations."
        ),
        key_factors=[
            "Current cost structure",
            "Commodity price assumptions",
            "Expense inclusions",
            "Documentation",
            "Update frequency"
        ],
        primary_authority=[
            "SPE Guidelines for Economic Evaluation",
            "PRMS 2018 Section 3.7"
        ],
        burden_holder="Reservoir/Economic Evaluator",
        adversary_position="Economic limit rate is outdated or based on unrealistic assumptions.",
        counter_arguments=[
            "Provide updated cost and price data",
            "Show calculation methodology",
            "Document all assumptions"
        ],
        resolution_strategy="Update economic limit rate regularly and document all calculations.",
        entity_scope="All producing wells and leases",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="PRMS 2018 Section 3.7"
    ),
    DoctrineBlock(
        topic="Production Data Quality Assurance",
        keywords=["production data", "quality assurance", "data validation", "forecasting"],
        conclusion_template="Production data should be validated for completeness, accuracy, and consistency before use in forecasting or reserve estimation.",
        reasoning_framework=(
            "Reliable production forecasts and reserve estimates depend on high-quality production data. "
            "Implement data validation checks for completeness (no missing periods), accuracy (cross-check with meter readings and sales records), and consistency (identify and correct anomalies). "
            "Document all data cleaning steps and maintain an audit trail. "
            "Use automated tools where possible to flag outliers and gaps. "
            "Update forecasts and reserves if data corrections materially affect results."
        ),
        key_factors=[
            "Data completeness",
            "Accuracy verification",
            "Consistency checks",
            "Audit trail",
            "Impact assessment"
        ],
        primary_authority=[
            "SPE Data Management Guidelines",
            "Company Data Quality Policies"
        ],
        burden_holder="Production Analyst",
        adversary_position="Forecasts are based on incomplete or inaccurate data.",
        counter_arguments=[
            "Provide data validation reports",
            "Show audit trail",
            "Update forecasts as needed"
        ],
        resolution_strategy="Implement robust data QA/QC processes and document all corrections.",
        entity_scope="All production data users",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="SPE Data Management Guidelines"
    ),
    DoctrineBlock(
        topic="Probabilistic Reserve Estimation",
        keywords=["probabilistic", "reserve estimation", "P10", "P50", "P90", "uncertainty"],
        conclusion_template="Probabilistic methods should be used to quantify uncertainty in reserve estimates, reporting P10, P50, and P90 values.",
        reasoning_framework=(
            "Probabilistic reserve estimation involves generating a range of possible outcomes using Monte Carlo simulation or similar techniques. "
            "Define probability distributions for key inputs (IP rate, decline parameters, costs, prices), run simulations, and report P10 (high case), P50 (median), and P90 (low case) reserves. "
            "Document all input distributions and simulation methodology. "
            "Probabilistic estimates provide a more complete picture of uncertainty than deterministic methods."
        ),
        key_factors=[
            "Input parameter distributions",
            "Simulation methodology",
            "Documentation",
            "Interpretation of results",
            "Regulatory acceptance"
        ],
        primary_authority=[
            "PRMS 2018 Section 2.5",
            "SPE Guidelines for Probabilistic Methods"
        ],
        burden_holder="Reserves Evaluator",
        adversary_position="Probabilistic estimates are not supported by sufficient data.",
        counter_arguments=[
            "Provide input data sources",
            "Show simulation outputs",
            "Document methodology"
        ],
        resolution_strategy="Use probabilistic methods where data supports; document all assumptions.",
        entity_scope="All reserve estimation projects",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="PRMS 2018 Section 2.5"
    ),
    DoctrineBlock(
        topic="Material Balance Cross-Check",
        keywords=["material balance", "cross-check", "reserves validation", "volumetrics"],
        conclusion_template="Material balance calculations should be used to cross-check decline curve and volumetric reserve estimates.",
        reasoning_framework=(
            "Material balance analysis provides an independent estimate of recoverable reserves based on reservoir pressure and production data. "
            "Use material balance as a cross-check for decline curve and volumetric estimates, especially in conventional reservoirs. "
            "Document all input data, assumptions, and results. "
            "Investigate and reconcile significant discrepancies between methods."
        ),
        key_factors=[
            "Reservoir pressure data",
            "Production history",
            "Material balance model selection",
            "Documentation",
            "Discrepancy reconciliation"
        ],
        primary_authority=[
            "SPE Monograph Vol. 1",
            "PRMS 2018 Section 3.8"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Material balance results conflict with decline curve estimates.",
        counter_arguments=[
            "Provide input data and assumptions",
            "Show reconciliation process",
            "Document all results"
        ],
        resolution_strategy="Use material balance as a validation tool and document all findings.",
        entity_scope="Conventional reservoirs",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Monograph Vol. 1"
    ),
    DoctrineBlock(
        topic="Forecasting Shut-In and Downtime",
        keywords=["shut-in", "downtime", "forecasting", "production interruptions"],
        conclusion_template="Production forecasts should account for expected shut-in and downtime based on historical averages and operational plans.",
        reasoning_framework=(
            "Wells may experience periods of shut-in or downtime due to maintenance, equipment failure, or market conditions. "
            "Analyze historical downtime records and operational plans to estimate future downtime percentages. "
            "Apply these factors to production forecasts to avoid overestimating output. "
            "Document all assumptions and update as operational plans change."
        ),
        key_factors=[
            "Historical downtime data",
            "Operational plans",
            "Downtime percentage calculation",
            "Documentation",
            "Forecast updates"
        ],
        primary_authority=[
            "SPE Production Forecasting Guidelines",
            "Company Operations Reports"
        ],
        burden_holder="Production Forecaster",
        adversary_position="Forecasts do not account for realistic downtime.",
        counter_arguments=[
            "Provide downtime analysis",
            "Show operational plans",
            "Document all assumptions"
        ],
        resolution_strategy="Incorporate downtime factors and update regularly.",
        entity_scope="All production forecasts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE Production Forecasting Guidelines"
    ),
    DoctrineBlock(
        topic="Accounting for Non-Productive Intervals",
        keywords=["non-productive intervals", "downtime", "forecast adjustment", "production data"],
        conclusion_template="Non-productive intervals should be excluded from decline curve fitting and production forecasts.",
        reasoning_framework=(
            "Periods when the well is shut-in or not producing due to operational issues should be excluded from decline curve analysis. "
            "Identify and remove non-productive intervals from the production dataset before fitting decline models. "
            "Document all exclusions and the rationale. "
            "Failure to exclude these periods may bias decline parameters and overstate reserves."
        ),
        key_factors=[
            "Identification of non-productive intervals",
            "Data exclusion methodology",
            "Documentation",
            "Impact assessment",
            "Model fit quality"
        ],
        primary_authority=[
            "SPE Decline Curve Analysis Best Practices",
            "Company Data Quality Policies"
        ],
        burden_holder="Production Analyst",
        adversary_position="Decline curve fit is biased by inclusion of non-productive periods.",
        counter_arguments=[
            "Provide data exclusion log",
            "Show impact on model fit",
            "Document rationale"
        ],
        resolution_strategy="Systematically exclude non-productive intervals and document process.",
        entity_scope="All decline curve analyses",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE Decline Curve Analysis Best Practices"
    ),
    DoctrineBlock(
        topic="Forecasting for Multi-Well Pads",
        keywords=["multi-well pad", "production interference", "forecasting", "parent-child wells"],
        conclusion_template="Production forecasts for multi-well pads should account for potential interference and parent-child well effects.",
        reasoning_framework=(
            "Multi-well pads may experience production interference due to pressure communication between wells, especially in tight reservoirs. "
            "Analyze historical production data for evidence of interference (e.g., rate drops after new well completions). "
            "Adjust forecasts to account for parent-child well effects and reduced productivity. "
            "Document all assumptions and provide sensitivity analysis."
        ),
        key_factors=[
            "Well spacing and completion timing",
            "Historical interference evidence",
            "Parent-child well identification",
            "Forecast adjustment methodology",
            "Documentation"
        ],
        primary_authority=[
            "SPE Guidelines for Unconventional Reservoirs",
            "Company Reservoir Engineering Policies"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Forecasts do not account for interference effects.",
        counter_arguments=[
            "Provide interference analysis",
            "Show forecast adjustments",
            "Document all assumptions"
        ],
        resolution_strategy="Incorporate interference effects and update as new data becomes available.",
        entity_scope="Multi-well pad developments",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE Guidelines for Unconventional Reservoirs"
    ),
    DoctrineBlock(
        topic="Accounting for Artificial Lift Installations",
        keywords=["artificial lift", "ESP", "rod pump", "forecast adjustment", "production enhancement"],
        conclusion_template="Production forecasts should be adjusted to reflect the impact of artificial lift installations, using analog data where possible.",
        reasoning_framework=(
            "Artificial lift systems (e.g., ESPs, rod pumps) can significantly alter production rates and decline trends. "
            "Analyze pre- and post-installation production data to quantify the impact. "
            "Use analog wells with similar lift installations to estimate expected improvements. "
            "Adjust decline curve parameters as needed and document all changes."
        ),
        key_factors=[
            "Type of artificial lift",
            "Pre- and post-installation data",
            "Analog well performance",
            "Forecast adjustment methodology",
            "Documentation"
        ],
        primary_authority=[
            "SPE Artificial Lift Handbook",
            "Company Production Engineering Guidelines"
        ],
        burden_holder="Production Engineer",
        adversary_position="Forecasts do not reflect artificial lift impact.",
        counter_arguments=[
            "Provide analog well data",
            "Show adjustment methodology",
            "Document all assumptions"
        ],
        resolution_strategy="Update forecasts with artificial lift impact and document process.",
        entity_scope="All wells with artificial lift",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE Artificial Lift Handbook"
    ),
    DoctrineBlock(
        topic="Accounting for Recompletion and Workover Events",
        keywords=["recompletion", "workover", "forecast adjustment", "production data"],
        conclusion_template="Production forecasts should be segmented and adjusted to account for major recompletion or workover events.",
        reasoning_framework=(
            "Recompletion or workover events can cause step-changes in production rates and alter decline trends. "
            "Segment the production history at the event date and fit separate decline models to each segment. "
            "Document the timing and nature of each event. "
            "Aggregate forecasts from each segment for total production projection."
        ),
        key_factors=[
            "Event identification and timing",
            "Segmented decline curve fitting",
            "Documentation",
            "Impact assessment",
            "Forecast aggregation"
        ],
        primary_authority=[
            "SPE Decline Curve Analysis Best Practices",
            "Company Operations Reports"
        ],
        burden_holder="Production Engineer",
        adversary_position="Forecasts do not account for step-changes due to workovers.",
        counter_arguments=[
            "Provide event logs",
            "Show segmented model fits",
            "Document all assumptions"
        ],
        resolution_strategy="Segment production history and fit models accordingly.",
        entity_scope="All wells with major workovers",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE Decline Curve Analysis Best Practices"
    ),
    DoctrineBlock(
        topic="Accounting for Facility Constraints",
        keywords=["facility constraints", "production limits", "forecast adjustment", "infrastructure"],
        conclusion_template="Production forecasts should be capped at facility or pipeline capacity limits, with documentation of all constraints.",
        reasoning_framework=(
            "Production may be limited by facility or pipeline capacity, regardless of well potential. "
            "Identify all relevant constraints (e.g., separator, compressor, pipeline limits) and cap forecasts accordingly. "
            "Document the source and magnitude of each constraint. "
            "Update forecasts if constraints change due to facility upgrades or new infrastructure."
        ),
        key_factors=[
            "Facility and pipeline capacity",
            "Constraint identification",
            "Documentation",
            "Forecast capping methodology",
            "Update process"
        ],
        primary_authority=[
            "Facility Design Reports",
            "Company Infrastructure Guidelines"
        ],
        burden_holder="Production/Facility Engineer",
        adversary_position="Forecasts exceed facility or pipeline capacity.",
        counter_arguments=[
            "Provide facility design specs",
            "Show capping methodology",
            "Document all constraints"
        ],
        resolution_strategy="Cap forecasts at constraint limits and update as needed.",
        entity_scope="All constrained facilities",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Facility Design Reports"
    ),
    DoctrineBlock(
        topic="Accounting for Regulatory Production Limits",
        keywords=["regulatory limits", "production quotas", "forecast adjustment", "compliance"],
        conclusion_template="Production forecasts must comply with all regulatory production limits or quotas, with documentation of applicable rules.",
        reasoning_framework=(
            "State or federal agencies may impose production limits or quotas on wells or fields. "
            "Identify all applicable regulations and incorporate limits into production forecasts. "
            "Document the source and details of each limit. "
            "Update forecasts if regulatory limits change."
        ),
        key_factors=[
            "Applicable regulations",
            "Limit identification",
            "Documentation",
            "Forecast adjustment methodology",
            "Compliance monitoring"
        ],
        primary_authority=[
            "Texas Railroad Commission Rules",
            "Federal Production Regulations"
        ],
        burden_holder="Regulatory Compliance Officer",
        adversary_position="Forecasts exceed regulatory production limits.",
        counter_arguments=[
            "Provide regulatory references",
            "Show forecast adjustments",
            "Document compliance process"
        ],
        resolution_strategy="Incorporate all regulatory limits and monitor for changes.",
        entity_scope="All regulated wells and fields",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Texas Railroad Commission Rules"
    ),
    DoctrineBlock(
        topic="Accounting for Non-Operating Interest Owners",
        keywords=["non-operating interest", "NRI", "revenue allocation", "joint venture"],
        conclusion_template="Revenue and expenses should be allocated to non-operating interest owners based on their NRI and in accordance with the joint operating agreement.",
        reasoning_framework=(
            "Non-operating interest owners are entitled to their share of revenue and responsible for their share of expenses, as defined by their NRI. "
            "Allocate all revenues and expenses in accordance with the joint operating agreement and division orders. "
            "Document all allocations and provide regular statements to non-operators. "
            "Resolve disputes through reference to the JOA and division orders."
        ),
        key_factors=[
            "NRI accuracy",
            "JOA provisions",
            "Division order compliance",
            "Documentation",
            "Dispute resolution process"
        ],
        primary_authority=[
            "Joint Operating Agreement",
            "Division Orders"
        ],
        burden_holder="Operator",
        adversary_position="Allocations do not match NRI or JOA terms.",
        counter_arguments=[
            "Provide JOA and division order documentation",
            "Show allocation calculations",
            "Document all statements"
        ],
        resolution_strategy="Allocate strictly according to JOA and division orders; maintain audit trail.",
        entity_scope="All non-operating interest owners",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Joint Operating Agreement"
    ),
    DoctrineBlock(
        topic="Accounting for Overriding Royalty Interests",
        keywords=["overriding royalty", "ORI", "revenue allocation", "deduction"],
        conclusion_template="Overriding royalty interests must be deducted from gross revenue before allocating net revenue to working interest owners.",
        reasoning_framework=(
            "Overriding royalty interests (ORIs) are non-operating burdens that entitle the holder to a share of production revenue, free of production costs. "
            "Deduct all ORIs from gross revenue before calculating net revenue for working interest owners. "
            "Verify ORI percentages through title documents and division orders. "
            "Document all deductions and update as ownership changes."
        ),
        key_factors=[
            "ORI percentage accuracy",
            "Title and division order verification",
            "Deduction methodology",
            "Documentation",
            "Ownership updates"
        ],
        primary_authority=[
            "Lease agreements",
            "Division Orders"
        ],
        burden_holder="Operator",
        adversary_position="ORI deductions are incorrect or not supported by documentation.",
        counter_arguments=[
            "Provide title and division order documentation",
            "Show deduction calculations",
            "Update for ownership changes"
        ],
        resolution_strategy="Deduct ORIs as specified in agreements and maintain documentation.",
        entity_scope="All properties with ORIs",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Lease agreements and division orders"
    ),
    DoctrineBlock(
        topic="Accounting for Marketing Fees",
        keywords=["marketing fees", "sales deduction", "netback", "revenue calculation"],
        conclusion_template="Marketing fees should be deducted from gross revenue only if allowed by contract and documented with invoices.",
        reasoning_framework=(
            "Marketing fees may be charged by third parties or affiliates for arranging the sale of oil and gas. "
            "Deduct marketing fees from gross revenue only if such deductions are allowed by the sales contract or lease agreement. "
            "Document all fees with invoices and ensure transparency in revenue statements. "
            "Disclose all marketing fee arrangements to working interest owners."
        ),
        key_factors=[
            "Contractual allowance for fees",
            "Invoice documentation",
            "Transparency in statements",
            "Disclosure to owners",
            "Fee calculation methodology"
        ],
        primary_authority=[
            "Sales contracts",
            "Lease agreements"
        ],
        burden_holder="Operator/Revenue Accountant",
        adversary_position="Marketing fees are deducted without contractual basis or documentation.",
        counter_arguments=[
            "Provide contract and invoice documentation",
            "Show deduction methodology",
            "Disclose all arrangements"
        ],
        resolution_strategy="Deduct only contractually-allowed fees and maintain documentation.",
        entity_scope="All sales subject to marketing fees",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Sales contract terms"
    ),
    DoctrineBlock(
        topic="Accounting for Take-in-Kind Arrangements",
        keywords=["take-in-kind", "TIK", "revenue allocation", "sales arrangements"],
        conclusion_template="Take-in-kind arrangements should be documented and revenue allocated based on actual volumes taken by each party.",
        reasoning_framework=(
            "Take-in-kind (TIK) arrangements allow owners to take their share of production in kind rather than as cash proceeds. "
            "Document all TIK arrangements in division orders and sales contracts. "
            "Allocate revenue based on actual volumes taken by each party, and reconcile with sales records. "
            "Disclose all TIK arrangements to affected parties."
        ),
        key_factors=[
            "TIK documentation",
            "Actual volume tracking",
            "Revenue allocation methodology",
            "Reconciliation with sales records",
            "Disclosure to parties"
        ],
        primary_authority=[
            "Division Orders",
            "Sales contracts"
        ],
        burden_holder="Operator",
        adversary_position="TIK allocations are not supported by documentation or actual volumes.",
        counter_arguments=[
            "Provide division order and contract documentation",
            "Show volume tracking records",
            "Reconcile with sales statements"
        ],
        resolution_strategy="Document all TIK arrangements and reconcile allocations regularly.",
        entity_scope="All properties with TIK arrangements",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Division Orders and sales contracts"
    ),
    DoctrineBlock(
        topic="Accounting for Gas Shrinkage",
        keywords=["gas shrinkage", "processing loss", "netback", "revenue calculation"],
        conclusion_template="Gas shrinkage due to processing losses should be accounted for in net revenue calculations, using actual plant data where available.",
        reasoning_framework=(
            "Gas shrinkage refers to the reduction in gas volume due to removal of liquids and impurities during processing. "
            "Apply shrinkage factors based on actual plant data or contract specifications to calculate net sales volumes. "
            "Document the source and calculation of shrinkage factors. "
            "Update factors as plant operations or gas composition change."
        ),
        key_factors=[
            "Actual plant shrinkage data",
            "Contractual shrinkage factors",
            "Volume tracking methodology",
            "Documentation",
            "Update process"
        ],
        primary_authority=[
            "Gas processing contracts",
            "Plant operations data"
        ],
        burden_holder="Operator/Revenue Accountant",
        adversary_position="Shrinkage factors are outdated or not supported by plant data.",
        counter_arguments=[
            "Provide plant data and contract documentation",
            "Show calculation methodology",
            "Update factors regularly"
        ],
        resolution_strategy="Use current plant data and document all shrinkage calculations.",
        entity_scope="All gas processing arrangements",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Gas processing contracts"
    ),
    DoctrineBlock(
        topic="Accounting for Fuel and Flare Gas",
        keywords=["fuel gas", "flare gas", "production deduction", "netback"],
        conclusion_template="Fuel and flare gas volumes should be deducted from gross production before calculating sales revenue.",
        reasoning_framework=(
            "Fuel gas is used to power equipment on site, and flare gas is combusted for safety or operational reasons. "
            "Deduct these volumes from gross production to determine net sales volumes. "
            "Document all deductions with meter readings or estimates. "
            "Update deductions as operations change."
        ),
        key_factors=[
            "Metered fuel and flare volumes",
            "Deduction methodology",
            "Documentation",
            "Update frequency",
            "Impact on revenue"
        ],
        primary_authority=[
            "Production reports",
            "Company Operations Policies"
        ],
        burden_holder="Operator",
        adversary_position="Fuel and flare deductions are not supported by metered data.",
        counter_arguments=[
            "Provide meter readings",
            "Show calculation methodology",
            "Document all deductions"
        ],
        resolution_strategy="Use metered data where available and document all deductions.",
        entity_scope="All producing wells and facilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Production reports"
    ),
    DoctrineBlock(
        topic="Accounting for Measurement Uncertainty",
        keywords=["measurement uncertainty", "metering", "production data", "revenue calculation"],
        conclusion_template="Measurement uncertainty should be quantified and disclosed in production and revenue reports.",
        reasoning_framework=(
            "All measurement systems have inherent uncertainty due to equipment limitations and operational factors. "
            "Quantify uncertainty using manufacturer specifications and calibration records. "
            "Disclose uncertainty ranges in production and revenue reports, especially for custody transfer points. "
            "Document all calibration and maintenance activities."
        ),
        key_factors=[
            "Meter specifications",
            "Calibration records",
            "Uncertainty calculation methodology",
            "Disclosure in reports",
            "Documentation"
        ],
        primary_authority=[
            "API MPMS Chapter 21",
            "Custody Transfer Agreements"
        ],
        burden_holder="Operator/Measurement Technician",
        adversary_position="Measurement uncertainty is not disclosed or quantified.",
        counter_arguments=[
            "Provide meter specs and calibration logs",
            "Show uncertainty calculations",
            "Disclose in reports"
        ],
        resolution_strategy="Quantify and disclose measurement uncertainty; maintain documentation.",
        entity_scope="All metered production and sales",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API MPMS Chapter 21"
    ),
    DoctrineBlock(
        topic="Accounting for Commodity Price Hedging",
        keywords=["hedging", "commodity price", "derivatives", "revenue adjustment"],
        conclusion_template="Hedge settlements should be accounted for separately from physical sales revenue and disclosed in financial statements.",
        reasoning_framework=(
            "Commodity price hedges (e.g., swaps, collars, options) are financial instruments used to manage price risk. "
            "Account for hedge settlements separately from physical sales revenue in cash flow and financial statements. "
            "Disclose the impact of hedges on net revenue and provide reconciliation with physical sales. "
            "Document all hedge contracts and settlement calculations."
        ),
        key_factors=[
            "Hedge contract terms",
            "Settlement calculation methodology",
            "Disclosure in financial statements",
            "Reconciliation with physical sales",
            "Documentation"
        ],
        primary_authority=[
            "FASB ASC 815",
            "Company Hedging Policies"
        ],
        burden_holder="Treasury/Accounting Department",
        adversary_position="Hedge impacts are not properly disclosed or reconciled.",
        counter_arguments=[
            "Provide hedge contract documentation",
            "Show settlement calculations",
            "Disclose in financial statements"
        ],
        resolution_strategy="Account for hedges separately and provide full disclosure.",
        entity_scope="All hedged production",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FASB ASC 815"
    ),
    DoctrineBlock(
        topic="Accounting for Deferred Revenue",
        keywords=["deferred revenue", "prepaid sales", "revenue recognition", "accounting"],
        conclusion_template="Deferred revenue from prepaid sales should be recognized as income only when hydrocarbons are delivered.",
        reasoning_framework=(
            "Deferred revenue arises when payment is received before delivery of hydrocarbons. "
            "Recognize revenue only as production is delivered, in accordance with accrual accounting principles and ASC 606. "
            "Track deferred revenue balances and reconcile with delivery records. "
            "Disclose deferred revenue in financial statements."
        ),
        key_factors=[
            "Sales contract terms",
            "Delivery tracking",
            "Revenue recognition policy",
            "Financial statement disclosure",
            "Reconciliation process"
        ],
        primary_authority=[
            "FASB ASC 606",
            "Company Revenue Recognition Policies"
        ],
        burden_holder="Accounting Department",
        adversary_position="Revenue is recognized before delivery, violating accounting standards.",
        counter_arguments=[
            "Provide delivery records",
            "Show revenue recognition policy",
            "Disclose deferred revenue balances"
        ],
        resolution_strategy="Recognize revenue only upon delivery and maintain documentation.",
        entity_scope="All prepaid sales arrangements",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FASB ASC 606"
    ),
    DoctrineBlock(
        topic="Accounting for Imbalances in Gas Sales",
        keywords=["gas imbalance", "over/under production", "revenue allocation", "balancing agreement"],
        conclusion_template="Gas imbalances should be tracked and settled according to the balancing agreement, with revenue allocated based on actual takes.",
        reasoning_framework=(
            "Gas imbalances occur when parties take more or less than their entitled share of production. "
            "Track imbalances using balancing agreements and allocate revenue based on actual takes. "
            "Settle imbalances through cash payments or future production adjustments. "
            "Document all imbalances and settlements."
        ),
        key_factors=[
            "Balancing agreement terms",
            "Actual take tracking",
            "Settlement methodology",
            "Documentation",
            "Disclosure to parties"
        ],
        primary_authority=[
            "Balancing Agreements",
            "FERC Regulations"
        ],
        burden_holder="Operator",
        adversary_position="Imbalances are not tracked or settled per agreement.",
        counter_arguments=[
            "Provide balancing agreement documentation",
            "Show imbalance tracking records",
            "Document settlements"
        ],
        resolution_strategy="Track and settle imbalances per agreement and maintain documentation.",
        entity_scope="All gas sales subject to balancing",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Balancing Agreements"
    ),
    DoctrineBlock(
        topic="Accounting for Revenue Suspense",
        keywords=["revenue suspense", "title defect", "ownership dispute", "revenue withholding"],
        conclusion_template="Revenue should be placed in suspense and not distributed until title defects or ownership disputes are resolved.",
        reasoning_framework=(
            "Revenue suspense accounts are used to withhold distributions when there are unresolved title defects or ownership disputes. "
            "Place affected revenue in suspense and document the reason and affected parties. "
            "Release revenue only upon resolution and update all records accordingly. "
            "Disclose suspense balances in owner statements."
        ),
        key_factors=[
            "Title and ownership documentation",
            "Suspense account tracking",
            "Resolution process",
            "Disclosure to owners",
            "Record updates"
        ],
        primary_authority=[
            "Division Orders",
            "Texas Natural Resources Code §91.402"
        ],
        burden_holder="Operator/Land Department",
        adversary_position="Revenue is withheld without proper documentation or notification.",
        counter_arguments=[
            "Provide title documentation",
            "Show suspense account records",
            "Disclose to affected parties"
        ],
        resolution_strategy="Maintain clear documentation and communicate with affected parties.",
        entity_scope="All revenue subject to suspense",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Texas Natural Resources Code §91.402"
    ),
    DoctrineBlock(
        topic="Accounting for Unclaimed Property",
        keywords=["unclaimed property", "escheat", "dormant funds", "state reporting"],
        conclusion_template="Unclaimed revenue must be reported and remitted to the state after statutory dormancy periods, in compliance with unclaimed property laws.",
        reasoning_framework=(
            "Unclaimed property laws require holders of dormant funds (e.g., uncashed royalty checks) to report and remit such funds to the state after a statutory dormancy period. "
            "Track all unclaimed funds, attempt to contact owners, and report to the appropriate state agency. "
            "Maintain documentation of all efforts and comply with reporting deadlines. "
            "Disclose unclaimed property in financial statements."
        ),
        key_factors=[
            "Dormancy period tracking",
            "Owner contact attempts",
            "State reporting requirements",
            "Documentation",
            "Financial statement disclosure"
        ],
        primary_authority=[
            "Texas Property Code Chapter 74",
            "Company Unclaimed Property Policies"
        ],
        burden_holder="Accounting Department",
        adversary_position="Unclaimed property is not reported or remitted in compliance with law.",
        counter_arguments=[
            "Provide dormancy tracking records",
            "Show owner contact documentation",
            "Report to state agency"
        ],
        resolution_strategy="Comply with all unclaimed property laws and maintain documentation.",
        entity_scope="All unclaimed revenue",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Property Code Chapter 74"
    ),
    DoctrineBlock(
        topic="Accounting for Joint Interest Billing Disputes",
        keywords=["joint interest billing", "JIB", "dispute resolution", "cost allocation"],
        conclusion_template="JIB disputes should be resolved according to the joint operating agreement and documented in operator records.",
        reasoning_framework=(
            "Joint interest billing (JIB) disputes may arise over allocation of costs among working interest owners. "
            "Resolve disputes according to the procedures in the joint operating agreement (JOA), including audit rights and dispute resolution mechanisms. "
            "Document all disputes, resolutions, and communications. "
            "Update cost allocations as needed and provide revised statements to all parties."
        ),
        key_factors=[
            "JOA dispute resolution provisions",
            "Audit rights",
            "Documentation",
            "Cost allocation methodology",
            "Communication with parties"
        ],
        primary_authority=[
            "Joint Operating Agreement",
            "COPAS Accounting Procedures"
        ],
        burden_holder="Operator",
        adversary_position="JIB disputes are not resolved per JOA or not documented.",
        counter_arguments=[
            "Provide JOA documentation",
            "Show dispute resolution process",
            "Document all communications"
        ],
        resolution_strategy="Follow JOA procedures and maintain documentation.",
        entity_scope="All JIB participants",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Joint Operating Agreement"
    ),
    DoctrineBlock(
        topic="Accounting for Abandonment and Reclamation Costs",
        keywords=["abandonment", "reclamation", "asset retirement obligation", "ARO", "cost allocation"],
        conclusion_template="Abandonment and reclamation costs should be estimated and accrued as asset retirement obligations in accordance with accounting standards.",
        reasoning_framework=(
            "Abandonment and reclamation costs are incurred to plug wells and restore sites at the end of production. "
            "Estimate future costs and accrue as asset retirement obligations (ARO) in financial statements, per FASB ASC 410. "
            "Update estimates as regulations or site conditions change. "
            "Document all assumptions and reconcile with actual costs upon abandonment."
        ),
        key_factors=[
            "ARO estimation methodology",
            "Regulatory requirements",
            "Financial statement disclosure",
            "Documentation",
            "Reconciliation with actual costs"
        ],
        primary_authority=[
            "FASB ASC 410",
            "State Abandonment Regulations"
        ],
        burden_holder="Accounting Department",
        adversary_position="ARO estimates are not accurate or not updated.",
        counter_arguments=[
            "Provide estimation methodology",
            "Show regulatory compliance",
            "Reconcile with actual costs"
        ],
        resolution_strategy="Update ARO estimates regularly and document all assumptions.",
        entity_scope="All producing assets",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FASB ASC 410"
    ),
    DoctrineBlock(
        topic="Accounting for Environmental Remediation Liabilities",
        keywords=["environmental remediation", "liability", "cost accrual", "regulatory compliance"],
        conclusion_template="Environmental remediation liabilities should be estimated and accrued when a legal obligation exists, per accounting standards.",
        reasoning_framework=(
            "Environmental remediation liabilities arise when a company is legally obligated to remediate contamination. "
            "Estimate and accrue costs in financial statements when the obligation is probable and can be reasonably estimated, per FASB ASC 450. "
            "Update estimates as site assessments or regulations change. "
            "Document all assumptions and disclose in financial statements."
        ),
        key_factors=[
            "Legal obligation assessment",
            "Cost estimation methodology",
            "Financial statement disclosure",
            "Documentation",
            "Regulatory updates"
        ],
        primary_authority=[
            "FASB ASC 450",
            "EPA and State Environmental Regulations"
        ],
        burden_holder="Accounting/Environmental Department",
        adversary_position="Remediation liabilities are not accrued or disclosed as required.",
        counter_arguments=[
            "Provide legal and regulatory documentation",
            "Show cost estimation methodology",
            "Disclose in financial statements"
        ],
        resolution_strategy="Accrue and disclose liabilities as required and document all assumptions.",
        entity_scope