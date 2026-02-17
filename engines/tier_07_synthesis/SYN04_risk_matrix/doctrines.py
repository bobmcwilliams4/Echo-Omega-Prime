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
        topic="probability_assessment_scales",
        keywords=["probability", "assessment", "scales", "likelihood", "risk matrix"],
        conclusion_template="Probability is assessed using a standardized scale to ensure consistency and comparability across risk events.",
        reasoning_framework="""
        1. Define the probability assessment scale (e.g., 1-5 or qualitative bands).
        2. Calibrate scales with historical data and expert judgment.
        3. Ensure clarity in scale definitions (e.g., 'Rare' = <5% chance, 'Almost Certain' = >95%).
        4. Apply the scale to each risk event, documenting rationale.
        5. Review and update scales periodically to reflect changes in risk environment.
        6. Cross-validate probability assessments with external benchmarks.
        7. Train assessors to minimize subjectivity and bias.
        8. Use probability scales as input for risk scoring and aggregation.
        9. Integrate with risk register and reporting tools.
        10. Ensure traceability of probability assignments for auditability.
        """,
        key_factors=[
            "Historical frequency of risk events",
            "Expert judgment calibration",
            "Clarity of scale definitions",
            "Consistency across risk types",
            "Periodic review and update"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM Guidance"],
        burden_holder="Risk Owner",
        adversary_position="Probability scales are arbitrary and introduce subjectivity.",
        counter_arguments=[
            "Standardized scales reduce subjectivity compared to ad hoc assessments.",
            "Calibration with data and expert input increases reliability."
        ],
        resolution_strategy="Adopt industry-accepted scales, provide training, and document rationale for assessments.",
        entity_scope="Enterprise-wide risk management",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 31010:2019, Section 5.4"
    ),
    DoctrineBlock(
        topic="impact_severity_classification",
        keywords=["impact", "severity", "classification", "risk matrix", "consequence"],
        conclusion_template="Impact severity is classified using defined thresholds to ensure objective risk evaluation.",
        reasoning_framework="""
        1. Establish impact categories (e.g., financial, reputational, operational, safety).
        2. Define quantitative and qualitative thresholds for each category.
        3. Map impact levels to a standardized scale (e.g., Insignificant to Catastrophic).
        4. Align impact definitions with organizational risk appetite and tolerance.
        5. Document rationale for classification decisions.
        6. Engage stakeholders to validate impact thresholds.
        7. Update classifications as business context evolves.
        8. Use impact severity in risk scoring and prioritization.
        9. Ensure consistency in application across risk registers.
        10. Audit impact classifications for accuracy and completeness.
        """,
        key_factors=[
            "Financial loss thresholds",
            "Reputational damage criteria",
            "Health and safety implications",
            "Alignment with risk appetite",
            "Stakeholder validation"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "Basel II/III"],
        burden_holder="Risk Assessor",
        adversary_position="Impact thresholds are arbitrary and may not reflect true business priorities.",
        counter_arguments=[
            "Thresholds are developed collaboratively and reviewed regularly.",
            "Alignment with risk appetite ensures business relevance."
        ],
        resolution_strategy="Establish clear, documented thresholds and review them annually with stakeholders.",
        entity_scope="All business units",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 11"
    ),
    DoctrineBlock(
        topic="risk_scoring_models",
        keywords=["risk scoring", "models", "quantitative", "qualitative", "risk matrix"],
        conclusion_template="Risk scoring models combine probability and impact to prioritize risks for treatment.",
        reasoning_framework="""
        1. Select an appropriate risk scoring methodology (e.g., matrix, quantitative, semi-quantitative).
        2. Define scoring formulas (e.g., Risk Score = Probability x Impact).
        3. Calibrate scoring models with historical loss data and scenario analysis.
        4. Document model assumptions and limitations.
        5. Validate models with cross-functional stakeholders.
        6. Integrate scoring outputs with risk registers and dashboards.
        7. Review and update models to reflect changes in risk landscape.
        8. Ensure transparency and auditability of scoring process.
        9. Provide training on model use and interpretation.
        10. Use risk scores to inform risk response and resource allocation.
        """,
        key_factors=[
            "Model selection (qualitative vs. quantitative)",
            "Calibration with historical data",
            "Transparency of assumptions",
            "Stakeholder validation",
            "Integration with risk management processes"
        ],
        primary_authority=["ISO 31010", "COSO ERM", "GARP"],
        burden_holder="Risk Management Function",
        adversary_position="Scoring models oversimplify complex risks and may mislead decision-makers.",
        counter_arguments=[
            "Models are tools to support, not replace, expert judgment.",
            "Regular validation and calibration mitigate oversimplification."
        ],
        resolution_strategy="Use models as decision aids, not substitutes for expert input; review regularly.",
        entity_scope="Enterprise risk portfolio",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ISO 31010:2019, Section 6.3"
    ),
    DoctrineBlock(
        topic="coso_erm_framework",
        keywords=["COSO", "ERM", "framework", "risk management", "governance"],
        conclusion_template="The COSO ERM Framework provides a structured approach to enterprise risk management, integrating risk with strategy and performance.",
        reasoning_framework="""
        1. Understand the COSO ERM components: Governance & Culture, Strategy & Objective-Setting, Performance, Review & Revision, Information, Communication & Reporting.
        2. Map organizational risk processes to COSO principles.
        3. Ensure board and executive oversight of risk management.
        4. Integrate risk management with strategic planning.
        5. Embed risk appetite and tolerance in decision-making.
        6. Promote a risk-aware culture throughout the organization.
        7. Monitor and report on risk performance and emerging risks.
        8. Review and revise risk processes in response to changes.
        9. Document and communicate risk management roles and responsibilities.
        10. Leverage COSO guidance for continuous improvement.
        """,
        key_factors=[
            "Alignment with COSO principles",
            "Board and executive engagement",
            "Integration with strategy",
            "Risk culture development",
            "Continuous improvement"
        ],
        primary_authority=["COSO ERM 2017", "SEC Guidance"],
        burden_holder="Board of Directors",
        adversary_position="COSO ERM is too generic and lacks industry specificity.",
        counter_arguments=[
            "COSO provides a flexible framework adaptable to any industry.",
            "Supplement with industry-specific standards as needed."
        ],
        resolution_strategy="Adopt COSO as a foundation and tailor to organizational context.",
        entity_scope="Enterprise risk management",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="COSO ERM 2017, Executive Summary"
    ),
    DoctrineBlock(
        topic="iso_31000_risk_management",
        keywords=["ISO 31000", "risk management", "framework", "principles", "guidelines"],
        conclusion_template="ISO 31000 sets out principles and guidelines for effective risk management applicable to any organization.",
        reasoning_framework="""
        1. Adopt ISO 31000 principles: integrated, structured, comprehensive, customized, inclusive, dynamic, best available information, human and cultural factors, continual improvement.
        2. Establish a risk management framework aligned with ISO 31000.
        3. Integrate risk management into governance and decision-making.
        4. Define risk context, appetite, and tolerance.
        5. Identify, assess, and treat risks systematically.
        6. Monitor, review, and communicate risk information.
        7. Ensure leadership commitment and resource allocation.
        8. Tailor risk processes to organizational needs.
        9. Promote a culture of risk awareness and accountability.
        10. Review framework effectiveness and update as needed.
        """,
        key_factors=[
            "Alignment with ISO 31000 principles",
            "Leadership commitment",
            "Integration with governance",
            "Customization to context",
            "Continuous improvement"
        ],
        primary_authority=["ISO 31000:2018", "IRM"],
        burden_holder="Risk Management Function",
        adversary_position="ISO 31000 is too broad and lacks implementation detail.",
        counter_arguments=[
            "ISO 31000 is intentionally flexible to suit diverse organizations.",
            "Implementation guidance is available from industry bodies."
        ],
        resolution_strategy="Adopt ISO 31000 as a guiding framework and supplement with detailed procedures.",
        entity_scope="All organizational levels",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="ISO 31000:2018, Section 4"
    ),
    DoctrineBlock(
        topic="risk_appetite_definitions",
        keywords=["risk appetite", "tolerance", "risk threshold", "limits"],
        conclusion_template="Risk appetite is defined as the amount and type of risk an organization is willing to pursue or retain.",
        reasoning_framework="""
        1. Engage board and executive leadership to articulate risk appetite.
        2. Align risk appetite with strategic objectives and stakeholder expectations.
        3. Define risk appetite statements for key risk categories.
        4. Set quantitative and qualitative risk limits.
        5. Communicate risk appetite throughout the organization.
        6. Integrate risk appetite into decision-making processes.
        7. Monitor risk exposures against appetite and escalate breaches.
        8. Review and update risk appetite regularly.
        9. Document rationale for risk appetite levels.
        10. Ensure risk appetite informs risk response and resource allocation.
        """,
        key_factors=[
            "Board and executive input",
            "Alignment with strategy",
            "Clear risk appetite statements",
            "Communication and integration",
            "Monitoring and escalation"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "Basel III"],
        burden_holder="Board of Directors",
        adversary_position="Risk appetite statements are vague and not actionable.",
        counter_arguments=[
            "Risk appetite is operationalized through specific limits and monitoring.",
            "Regular review ensures relevance and clarity."
        ],
        resolution_strategy="Translate risk appetite into actionable limits and embed in processes.",
        entity_scope="Enterprise-wide",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 6"
    ),
    DoctrineBlock(
        topic="inherent_vs_residual_risk",
        keywords=["inherent risk", "residual risk", "controls", "risk reduction"],
        conclusion_template="Inherent risk is the exposure before controls; residual risk is the remaining exposure after controls are applied.",
        reasoning_framework="""
        1. Identify risk events and assess their inherent risk (before controls).
        2. Document existing controls and their effectiveness.
        3. Reassess risk exposure considering control effectiveness (residual risk).
        4. Use both inherent and residual risk to prioritize risk treatment.
        5. Communicate the distinction to stakeholders for clarity.
        6. Monitor controls for changes in effectiveness.
        7. Update risk assessments as control environment evolves.
        8. Ensure documentation supports audit and regulatory requirements.
        9. Integrate inherent and residual risk into risk reporting.
        10. Use residual risk to inform risk acceptance or further mitigation.
        """,
        key_factors=[
            "Quality and effectiveness of controls",
            "Accurate assessment of inherent risk",
            "Documentation of control environment",
            "Regular reassessment",
            "Stakeholder understanding"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "Basel II"],
        burden_holder="Risk Owner",
        adversary_position="Distinction between inherent and residual risk is unclear and subjective.",
        counter_arguments=[
            "Clear definitions and documentation reduce ambiguity.",
            "Regular training and review enhance understanding."
        ],
        resolution_strategy="Standardize definitions and provide guidance on assessment.",
        entity_scope="All risk categories",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Basel II, Pillar 2"
    ),
    DoctrineBlock(
        topic="control_effectiveness_rating",
        keywords=["control effectiveness", "rating", "assessment", "internal controls"],
        conclusion_template="Control effectiveness is rated using defined criteria to inform residual risk assessment.",
        reasoning_framework="""
        1. Define criteria for control effectiveness (e.g., design, implementation, operation).
        2. Use a standardized rating scale (e.g., Effective, Partially Effective, Ineffective).
        3. Assess controls based on evidence and testing.
        4. Document rationale for ratings and supporting evidence.
        5. Review ratings with control owners and auditors.
        6. Update ratings as control environment changes.
        7. Integrate control ratings into risk assessment and reporting.
        8. Use ratings to prioritize control improvements.
        9. Ensure transparency and traceability for audit purposes.
        10. Provide training on control assessment methodology.
        """,
        key_factors=[
            "Defined rating criteria",
            "Evidence-based assessment",
            "Stakeholder review",
            "Integration with risk assessment",
            "Auditability"
        ],
        primary_authority=["COSO Internal Control Framework", "ISO 31000"],
        burden_holder="Control Owner",
        adversary_position="Control ratings are subjective and may not reflect actual effectiveness.",
        counter_arguments=[
            "Use of evidence and standardized criteria reduces subjectivity.",
            "Independent review enhances reliability."
        ],
        resolution_strategy="Adopt standardized criteria and require supporting evidence for ratings.",
        entity_scope="Internal controls",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="COSO Internal Control 2013, Principle 16"
    ),
    DoctrineBlock(
        topic="monte_carlo_simulation",
        keywords=["monte carlo", "simulation", "quantitative analysis", "risk modeling"],
        conclusion_template="Monte Carlo simulation is used to model risk distributions and quantify uncertainty in risk assessments.",
        reasoning_framework="""
        1. Identify risk variables and their probability distributions.
        2. Develop simulation models reflecting risk interdependencies.
        3. Run a large number of iterations to generate outcome distributions.
        4. Analyze simulation outputs (e.g., Value-at-Risk, expected loss).
        5. Validate simulation assumptions and input data.
        6. Use results to inform risk appetite, capital allocation, and decision-making.
        7. Document model structure, assumptions, and limitations.
        8. Review and update models as new data becomes available.
        9. Communicate results to stakeholders in accessible formats.
        10. Integrate simulation outputs with risk reporting and dashboards.
        """,
        key_factors=[
            "Quality of input data",
            "Accuracy of probability distributions",
            "Model validation",
            "Interpretation of results",
            "Stakeholder communication"
        ],
        primary_authority=["GARP", "Basel II/III", "ISO 31010"],
        burden_holder="Risk Quantitative Analyst",
        adversary_position="Monte Carlo models are complex and may be misunderstood by decision-makers.",
        counter_arguments=[
            "Clear communication of assumptions and results mitigates misunderstanding.",
            "Training and visualization tools enhance accessibility."
        ],
        resolution_strategy="Provide training and clear documentation for simulation results.",
        entity_scope="Quantitative risk analysis",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="Basel II, Annex 4"
    ),
    DoctrineBlock(
        topic="sensitivity_analysis_tornado",
        keywords=["sensitivity analysis", "tornado diagram", "risk drivers", "scenario analysis"],
        conclusion_template="Tornado diagrams are used in sensitivity analysis to identify key risk drivers and prioritize mitigation efforts.",
        reasoning_framework="""
        1. Identify key input variables affecting risk outcomes.
        2. Vary each input across its plausible range while holding others constant.
        3. Quantify the impact on risk outcomes (e.g., loss, probability).
        4. Rank variables by their impact to create a tornado diagram.
        5. Use analysis to focus mitigation on most influential drivers.
        6. Document assumptions and ranges used in analysis.
        7. Communicate findings to stakeholders for informed decision-making.
        8. Integrate results with risk registers and action plans.
        9. Review and update analysis as new data emerges.
        10. Use sensitivity analysis to validate risk models and scenarios.
        """,
        key_factors=[
            "Selection of input variables",
            "Range of variation",
            "Quantification of impact",
            "Visualization clarity",
            "Stakeholder engagement"
        ],
        primary_authority=["ISO 31010", "GARP", "IRM"],
        burden_holder="Risk Analyst",
        adversary_position="Sensitivity analysis may overlook complex interactions between variables.",
        counter_arguments=[
            "Sensitivity analysis is complemented by scenario and simulation methods.",
            "Focus is on identifying primary drivers, not all interactions."
        ],
        resolution_strategy="Combine sensitivity analysis with other quantitative techniques.",
        entity_scope="Risk modeling and analysis",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="ISO 31010:2019, Section 6.5"
    ),
    DoctrineBlock(
        topic="risk_register_structure",
        keywords=["risk register", "structure", "documentation", "risk inventory"],
        conclusion_template="A risk register is structured to capture essential information for each risk, supporting effective management and reporting.",
        reasoning_framework="""
        1. Define mandatory fields for each risk (e.g., description, owner, category, probability, impact, controls, status).
        2. Ensure alignment with organizational risk taxonomy.
        3. Include fields for inherent and residual risk, control effectiveness, and mitigation actions.
        4. Provide space for qualitative and quantitative data.
        5. Enable tracking of risk status and action progress.
        6. Integrate with risk reporting and dashboard tools.
        7. Maintain version control and audit trail.
        8. Review register structure annually for relevance.
        9. Train users on register use and data entry standards.
        10. Ensure security and confidentiality of risk data.
        """,
        key_factors=[
            "Comprehensive field definitions",
            "Alignment with risk taxonomy",
            "Integration with reporting tools",
            "Version control",
            "User training"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Coordinator",
        adversary_position="Overly complex registers discourage use and lead to incomplete data.",
        counter_arguments=[
            "Balance comprehensiveness with usability.",
            "Provide training and user support."
        ],
        resolution_strategy="Streamline register fields and provide clear guidance to users.",
        entity_scope="All risk owners and coordinators",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 6.3"
    ),
    DoctrineBlock(
        topic="key_risk_indicators",
        keywords=["key risk indicators", "KRIs", "metrics", "early warning"],
        conclusion_template="Key Risk Indicators (KRIs) are metrics used to provide early warning of increasing risk exposures.",
        reasoning_framework="""
        1. Identify leading and lagging indicators for key risk categories.
        2. Define thresholds and escalation triggers for each KRI.
        3. Align KRIs with organizational risk appetite and objectives.
        4. Validate KRIs with business units and risk owners.
        5. Integrate KRIs into risk monitoring and reporting processes.
        6. Review and update KRIs regularly to maintain relevance.
        7. Document rationale for KRI selection and thresholds.
        8. Use KRIs to inform proactive risk management actions.
        9. Train staff on interpretation and use of KRIs.
        10. Audit KRI data quality and reporting accuracy.
        """,
        key_factors=[
            "Relevance to key risks",
            "Threshold definition",
            "Alignment with risk appetite",
            "Stakeholder validation",
            "Data quality"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "Basel III"],
        burden_holder="Risk Monitoring Function",
        adversary_position="KRIs are backward-looking and may not provide timely warnings.",
        counter_arguments=[
            "Emphasis on leading indicators enhances early warning capability.",
            "Regular review ensures KRIs remain predictive."
        ],
        resolution_strategy="Prioritize leading indicators and review KRI effectiveness regularly.",
        entity_scope="Enterprise risk monitoring",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 14"
    ),
    DoctrineBlock(
        topic="risk_adjusted_return",
        keywords=["risk-adjusted return", "RAROC", "capital allocation", "performance measurement"],
        conclusion_template="Risk-adjusted return metrics are used to evaluate performance by considering both risk and reward.",
        reasoning_framework="""
        1. Select appropriate risk-adjusted return metrics (e.g., RAROC, EVA, Sharpe Ratio).
        2. Calculate expected returns and associated risk capital.
        3. Allocate capital based on risk contributions.
        4. Compare risk-adjusted returns across business units and investments.
        5. Integrate metrics into performance management and incentive systems.
        6. Document assumptions and calculation methodologies.
        7. Review and update metrics as business and regulatory requirements evolve.
        8. Communicate results to stakeholders for informed decision-making.
        9. Use risk-adjusted returns to guide resource allocation.
        10. Audit calculations for accuracy and consistency.
        """,
        key_factors=[
            "Selection of appropriate metrics",
            "Accuracy of risk capital calculations",
            "Integration with performance management",
            "Transparency of assumptions",
            "Regulatory compliance"
        ],
        primary_authority=["Basel III", "GARP", "COSO ERM"],
        burden_holder="Finance and Risk Management",
        adversary_position="Risk-adjusted metrics are complex and may obscure true performance.",
        counter_arguments=[
            "Metrics provide a more complete view by incorporating risk.",
            "Transparency and documentation mitigate complexity."
        ],
        resolution_strategy="Provide clear documentation and training on metric interpretation.",
        entity_scope="Business units and investments",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Basel III, Annex 6"
    ),
    DoctrineBlock(
        topic="expected_value_analysis",
        keywords=["expected value", "risk quantification", "decision analysis", "probability-weighted"],
        conclusion_template="Expected value analysis quantifies risk by calculating the probability-weighted average of possible outcomes.",
        reasoning_framework="""
        1. Identify all possible risk outcomes and their probabilities.
        2. Assign monetary or quantitative values to each outcome.
        3. Calculate expected value: sum of (probability x value) for all outcomes.
        4. Use expected value to compare and prioritize risk responses.
        5. Document assumptions and data sources.
        6. Integrate expected value analysis with risk scoring and reporting.
        7. Review and update analysis as new data becomes available.
        8. Communicate findings to decision-makers.
        9. Use expected value in scenario planning and capital allocation.
        10. Audit calculations for accuracy and completeness.
        """,
        key_factors=[
            "Accurate probability estimates",
            "Comprehensive outcome identification",
            "Data quality",
            "Transparency of assumptions",
            "Integration with decision processes"
        ],
        primary_authority=["ISO 31010", "GARP", "IRM"],
        burden_holder="Risk Analyst",
        adversary_position="Expected value analysis ignores risk variability and tail events.",
        counter_arguments=[
            "Expected value is supplemented by variance and scenario analysis.",
            "Tail risks are addressed through additional quantitative methods."
        ],
        resolution_strategy="Use expected value as one input among several in risk decision-making.",
        entity_scope="Quantitative risk assessment",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ISO 31010:2019, Section 6.2"
    ),
    DoctrineBlock(
        topic="risk_heat_map_generation",
        keywords=["risk heat map", "visualization", "risk matrix", "reporting"],
        conclusion_template="Risk heat maps visually represent risk exposure by plotting probability against impact.",
        reasoning_framework="""
        1. Define axes for probability and impact based on standardized scales.
        2. Assign each risk to a cell in the matrix according to its assessed values.
        3. Use color coding to indicate severity (e.g., green, yellow, red).
        4. Aggregate risks by category or business unit as needed.
        5. Update heat maps regularly to reflect current risk assessments.
        6. Integrate heat maps into risk reporting and dashboards.
        7. Provide explanatory notes and legends for clarity.
        8. Validate heat maps with stakeholders for accuracy.
        9. Use heat maps to prioritize risk mitigation efforts.
        10. Archive historical heat maps for trend analysis.
        """,
        key_factors=[
            "Accuracy of risk assessments",
            "Clarity of visualization",
            "Stakeholder validation",
            "Integration with reporting",
            "Historical trend analysis"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Reporting Function",
        adversary_position="Heat maps oversimplify risk and may obscure important details.",
        counter_arguments=[
            "Heat maps are complemented by detailed risk registers and narratives.",
            "They provide a high-level overview for decision-makers."
        ],
        resolution_strategy="Use heat maps as a summary tool, not a substitute for detailed analysis.",
        entity_scope="Risk reporting and communication",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 13"
    ),
    DoctrineBlock(
        topic="risk_mitigation_strategies",
        keywords=["risk mitigation", "treatment", "controls", "response strategies"],
        conclusion_template="Risk mitigation strategies are selected based on risk appetite, cost-benefit analysis, and effectiveness.",
        reasoning_framework="""
        1. Identify possible risk response options: avoid, reduce, transfer, accept, exploit.
        2. Evaluate each option based on effectiveness, cost, and alignment with risk appetite.
        3. Select and implement preferred mitigation strategies.
        4. Assign responsibility for implementation and monitoring.
        5. Document rationale for selected strategies.
        6. Monitor effectiveness and adjust strategies as needed.
        7. Integrate mitigation actions into risk register and action plans.
        8. Communicate strategies to stakeholders.
        9. Review and update strategies as risk environment changes.
        10. Audit mitigation actions for completion and effectiveness.
        """,
        key_factors=[
            "Alignment with risk appetite",
            "Cost-benefit analysis",
            "Effectiveness of controls",
            "Responsibility assignment",
            "Monitoring and review"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Owner",
        adversary_position="Mitigation strategies are costly and may not eliminate risk.",
        counter_arguments=[
            "Strategies are selected based on cost-effectiveness and residual risk.",
            "Complete elimination of risk is rarely feasible."
        ],
        resolution_strategy="Prioritize mitigation based on risk appetite and resource constraints.",
        entity_scope="All risk categories",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 6.5"
    ),
    DoctrineBlock(
        topic="risk_category_classification",
        keywords=["risk categories", "classification", "taxonomy", "risk register"],
        conclusion_template="Risks are classified into categories to facilitate aggregation, reporting, and management.",
        reasoning_framework="""
        1. Develop a risk taxonomy tailored to organizational context (e.g., strategic, operational, financial, compliance).
        2. Assign each risk to one or more categories in the risk register.
        3. Use categories to aggregate and analyze risk exposures.
        4. Align categories with reporting requirements and stakeholder needs.
        5. Review and update taxonomy as business evolves.
        6. Document rationale for category assignments.
        7. Integrate categories with risk reporting and dashboards.
        8. Provide training on taxonomy use and updates.
        9. Ensure consistency in application across business units.
        10. Audit category assignments for accuracy.
        """,
        key_factors=[
            "Relevance of taxonomy",
            "Consistency of application",
            "Alignment with reporting",
            "Stakeholder input",
            "Periodic review"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Coordinator",
        adversary_position="Rigid categories may obscure cross-cutting risks.",
        counter_arguments=[
            "Categories are reviewed and updated to reflect emerging risks.",
            "Cross-referencing and multi-category assignment are possible."
        ],
        resolution_strategy="Maintain flexible taxonomy and allow for multiple category assignments.",
        entity_scope="Enterprise risk register",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 12"
    ),
    DoctrineBlock(
        topic="risk_aggregation_methods",
        keywords=["risk aggregation", "portfolio risk", "correlation", "aggregation methods"],
        conclusion_template="Risk aggregation methods are used to estimate total risk exposure, accounting for correlations and dependencies.",
        reasoning_framework="""
        1. Identify all relevant risks and their individual exposures.
        2. Assess correlations and dependencies between risks.
        3. Select aggregation method (e.g., simple sum, variance-covariance, copula models).
        4. Calculate aggregate risk exposure for portfolios or business units.
        5. Document assumptions and limitations of aggregation methods.
        6. Validate aggregation results with scenario analysis and stress testing.
        7. Integrate aggregated risk into capital planning and risk appetite monitoring.
        8. Review and update aggregation methods as risk profile evolves.
        9. Communicate aggregate risk to stakeholders.
        10. Audit aggregation process for accuracy and transparency.
        """,
        key_factors=[
            "Risk correlations",
            "Choice of aggregation method",
            "Data quality",
            "Validation and stress testing",
            "Transparency of assumptions"
        ],
        primary_authority=["Basel III", "GARP", "ISO 31010"],
        burden_holder="Risk Quantitative Analyst",
        adversary_position="Aggregation may underestimate risk due to hidden dependencies.",
        counter_arguments=[
            "Advanced methods and stress testing address hidden dependencies.",
            "Regular validation reduces aggregation error."
        ],
        resolution_strategy="Use conservative assumptions and validate with multiple methods.",
        entity_scope="Portfolio and enterprise risk",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Basel III, Annex 5"
    ),
    DoctrineBlock(
        topic="risk_appetite_cascade",
        keywords=["risk appetite", "cascade", "limits", "delegation", "risk governance"],
        conclusion_template="Risk appetite is cascaded through the organization via delegated limits and aligned objectives.",
        reasoning_framework="""
        1. Define enterprise-level risk appetite statements and limits.
        2. Cascade limits to business units and functions based on risk profile.
        3. Align delegated limits with business objectives and accountability.
        4. Monitor risk exposures against delegated limits.
        5. Escalate breaches according to governance protocols.
        6. Review and update cascaded limits as business and risk environment changes.
        7. Document rationale for delegation and limit setting.
        8. Communicate limits and escalation protocols to all relevant staff.
        9. Integrate cascaded limits into performance management.
        10. Audit cascade process for effectiveness and compliance.
        """,
        key_factors=[
            "Alignment with enterprise risk appetite",
            "Clarity of delegated limits",
            "Monitoring and escalation",
            "Documentation and communication",
            "Periodic review"
        ],
        primary_authority=["COSO ERM", "Basel III", "IRM"],
        burden_holder="Risk Governance Function",
        adversary_position="Cascading risk appetite may dilute accountability and clarity.",
        counter_arguments=[
            "Clear delegation protocols and monitoring maintain accountability.",
            "Regular review ensures limits remain aligned and clear."
        ],
        resolution_strategy="Document delegation protocols and provide training on accountability.",
        entity_scope="All business units and functions",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 6"
    ),
    DoctrineBlock(
        topic="scenario_analysis_design",
        keywords=["scenario analysis", "stress testing", "risk modeling", "design"],
        conclusion_template="Scenario analysis is designed to test the impact of plausible adverse events on risk exposures.",
        reasoning_framework="""
        1. Identify relevant risk scenarios based on emerging threats and vulnerabilities.
        2. Define scenario parameters and assumptions.
        3. Model the impact of scenarios on key risk exposures.
        4. Validate scenarios with subject matter experts.
        5. Document scenario design, assumptions, and rationale.
        6. Integrate scenario results into risk reporting and decision-making.
        7. Review and update scenarios as risk environment evolves.
        8. Communicate scenario outcomes to stakeholders.
        9. Use scenario analysis to inform capital planning and risk appetite.
        10. Audit scenario analysis process for completeness and accuracy.
        """,
        key_factors=[
            "Relevance of scenarios",
            "Assumption transparency",
            "Expert validation",
            "Integration with decision-making",
            "Review and update"
        ],
        primary_authority=["Basel III", "ISO 31010", "GARP"],
        burden_holder="Risk Modeling Function",
        adversary_position="Scenario analysis is speculative and may not reflect real-world outcomes.",
        counter_arguments=[
            "Scenarios are validated with experts and updated regularly.",
            "They complement historical analysis to capture emerging risks."
        ],
        resolution_strategy="Use scenario analysis as a supplement to quantitative models.",
        entity_scope="Enterprise risk management",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Basel III, Pillar 2"
    ),
    DoctrineBlock(
        topic="bow_tie_analysis",
        keywords=["bow tie analysis", "risk visualization", "controls", "barriers"],
        conclusion_template="Bow tie analysis visually maps risk pathways, controls, and consequences to enhance understanding and management.",
        reasoning_framework="""
        1. Define the central risk event (the 'knot' of the bow tie).
        2. Identify threats leading to the event (left side) and consequences (right side).
        3. Map preventive controls (barriers) for threats and mitigative controls for consequences.
        4. Visualize the bow tie diagram for clarity.
        5. Engage stakeholders in bow tie workshops.
        6. Document control effectiveness and gaps.
        7. Integrate bow tie analysis with risk register and action plans.
        8. Review and update diagrams as risk environment changes.
        9. Use bow tie analysis to prioritize control improvements.
        10. Communicate findings to all relevant staff.
        """,
        key_factors=[
            "Clarity of risk pathways",
            "Identification of controls",
            "Stakeholder engagement",
            "Integration with risk register",
            "Review and update"
        ],
        primary_authority=["ISO 31010", "IRM", "COSO ERM"],
        burden_holder="Risk Facilitator",
        adversary_position="Bow tie analysis is time-consuming and may not add value for all risks.",
        counter_arguments=[
            "It is reserved for high-impact or complex risks.",
            "Improves understanding and control prioritization."
        ],
        resolution_strategy="Apply bow tie analysis selectively to critical risks.",
        entity_scope="High-impact risk events",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ISO 31010:2019, Section 6.4"
    ),
    DoctrineBlock(
        topic="risk_velocity_assessment",
        keywords=["risk velocity", "speed of onset", "risk assessment", "timing"],
        conclusion_template="Risk velocity assessment evaluates how quickly a risk can materialize, informing prioritization and response.",
        reasoning_framework="""
        1. Define risk velocity criteria (e.g., immediate, short-term, medium-term, long-term).
        2. Assess each risk for speed of onset and time to impact.
        3. Integrate velocity into risk scoring and prioritization.
        4. Document rationale for velocity ratings.
        5. Use velocity to inform response planning and resource allocation.
        6. Review and update velocity assessments as risk environment changes.
        7. Communicate velocity considerations to stakeholders.
        8. Integrate with risk register and reporting.
        9. Provide training on velocity assessment methodology.
        10. Audit velocity ratings for consistency and accuracy.
        """,
        key_factors=[
            "Clear velocity criteria",
            "Consistency of assessment",
            "Integration with risk scoring",
            "Documentation",
            "Review and update"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "IRM"],
        burden_holder="Risk Assessor",
        adversary_position="Velocity is difficult to assess and may be speculative.",
        counter_arguments=[
            "Defined criteria and training improve reliability.",
            "Regular review ensures ongoing relevance."
        ],
        resolution_strategy="Standardize velocity criteria and provide guidance to assessors.",
        entity_scope="All risk categories",
        confidence=0.85,
        confidence_zone="Moderate-High",
        controlling_precedent="COSO ERM 2017, Principle 13"
    ),
    DoctrineBlock(
        topic="risk_culture_assessment",
        keywords=["risk culture", "assessment", "organizational culture", "behavior"],
        conclusion_template="Risk culture assessment evaluates attitudes, behaviors, and values related to risk management across the organization.",
        reasoning_framework="""
        1. Define risk culture dimensions (e.g., risk awareness, openness, accountability, challenge).
        2. Use surveys, interviews, and focus groups to assess culture.
        3. Analyze results to identify strengths and areas for improvement.
        4. Benchmark against industry standards and best practices.
        5. Integrate findings into risk management strategy and training.
        6. Monitor changes in risk culture over time.
        7. Communicate assessment results to leadership and staff.
        8. Develop action plans to address cultural gaps.
        9. Review and update assessment tools regularly.
        10. Audit the effectiveness of culture initiatives.
        """,
        key_factors=[
            "Comprehensive assessment tools",
            "Leadership engagement",
            "Benchmarking",
            "Action planning",
            "Ongoing monitoring"
        ],
        primary_authority=["IRM", "COSO ERM", "ISO 31000"],
        burden_holder="Chief Risk Officer",
        adversary_position="Cultural assessments are subjective and difficult to measure.",
        counter_arguments=[
            "Use of validated tools and external benchmarks increases objectivity.",
            "Regular monitoring tracks progress over time."
        ],
        resolution_strategy="Adopt validated assessment tools and benchmark results.",
        entity_scope="Organization-wide",
        confidence=0.84,
        confidence_zone="Moderate-High",
        controlling_precedent="COSO ERM 2017, Principle 4"
    ),
    DoctrineBlock(
        topic="emerging_risk_identification",
        keywords=["emerging risks", "identification", "horizon scanning", "trend analysis"],
        conclusion_template="Emerging risk identification involves systematic scanning for new or evolving threats and opportunities.",
        reasoning_framework="""
        1. Establish horizon scanning processes using internal and external sources.
        2. Engage cross-functional teams to identify emerging risks.
        3. Use trend analysis, scenario planning, and expert input.
        4. Document identified emerging risks and potential impacts.
        5. Integrate emerging risks into risk register and reporting.
        6. Review and update emerging risk list regularly.
        7. Communicate emerging risks to leadership and stakeholders.
        8. Develop early warning indicators and monitoring protocols.
        9. Allocate resources for further analysis and response planning.
        10. Benchmark emerging risk processes against industry practices.
        """,
        key_factors=[
            "Robust scanning processes",
            "Cross-functional engagement",
            "Trend analysis",
            "Integration with risk register",
            "Regular review"
        ],
        primary_authority=["IRM", "ISO 31000", "COSO ERM"],
        burden_holder="Risk Intelligence Function",
        adversary_position="Emerging risk identification is speculative and resource-intensive.",
        counter_arguments=[
            "Early identification enables proactive management.",
            "Processes are scaled to available resources and risk profile."
        ],
        resolution_strategy="Prioritize high-impact emerging risks and use scalable processes.",
        entity_scope="Enterprise risk management",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 6.4"
    ),
    DoctrineBlock(
        topic="risk_reporting_structure",
        keywords=["risk reporting", "structure", "governance", "escalation"],
        conclusion_template="Risk reporting structure defines the flow of risk information, escalation protocols, and governance oversight.",
        reasoning_framework="""
        1. Map reporting lines for risk information from operational to board level.
        2. Define escalation thresholds and protocols for risk events.
        3. Align reporting structure with governance and regulatory requirements.
        4. Standardize report formats and frequency.
        5. Integrate risk reporting with performance and compliance reporting.
        6. Ensure timely and accurate dissemination of risk information.
        7. Review and update reporting structure as organization evolves.
        8. Document roles and responsibilities for risk reporting.
        9. Provide training on reporting protocols and tools.
        10. Audit reporting structure for effectiveness and compliance.
        """,
        key_factors=[
            "Clarity of reporting lines",
            "Escalation protocols",
            "Standardization",
            "Regulatory alignment",
            "Review and update"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "Basel III"],
        burden_holder="Risk Reporting Function",
        adversary_position="Complex reporting structures slow down risk communication.",
        counter_arguments=[
            "Standardization and clear protocols streamline reporting.",
            "Regular review ensures efficiency."
        ],
        resolution_strategy="Simplify reporting lines and automate where possible.",
        entity_scope="All business units",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 15"
    ),
    DoctrineBlock(
        topic="three_lines_model",
        keywords=["three lines model", "governance", "risk management", "assurance"],
        conclusion_template="The Three Lines Model clarifies roles and responsibilities for risk management, assurance, and oversight.",
        reasoning_framework="""
        1. Define the three lines: operational management, risk and compliance functions, internal audit.
        2. Assign clear roles and responsibilities for each line.
        3. Ensure independence of internal audit from management.
        4. Integrate the model into governance and risk frameworks.
        5. Communicate roles to all staff and stakeholders.
        6. Review and update role definitions as organization evolves.
        7. Monitor effectiveness of the model in practice.
        8. Provide training on the Three Lines Model.
        9. Document interactions and escalation protocols between lines.
        10. Audit model implementation for compliance and effectiveness.
        """,
        key_factors=[
            "Clarity of roles",
            "Independence of assurance functions",
            "Integration with governance",
            "Communication and training",
            "Monitoring and review"
        ],
        primary_authority=["IIA", "COSO ERM", "ISO 31000"],
        burden_holder="Board of Directors",
        adversary_position="Rigid application of the model may hinder collaboration.",
        counter_arguments=[
            "Model is adaptable to organizational context.",
            "Emphasizes collaboration and communication."
        ],
        resolution_strategy="Tailor the model to fit organizational needs and promote collaboration.",
        entity_scope="Enterprise risk governance",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="IIA Three Lines Model 2020"
    ),
    # Additional doctrine blocks for comprehensive coverage (21 more for 40+ total)
    DoctrineBlock(
        topic="risk_communication_protocols",
        keywords=["risk communication", "protocols", "stakeholder engagement", "information flow"],
        conclusion_template="Risk communication protocols ensure timely, accurate, and relevant information reaches all stakeholders.",
        reasoning_framework="""
        1. Identify key internal and external stakeholders.
        2. Define communication objectives for each stakeholder group.
        3. Establish channels and frequency for risk communication.
        4. Standardize risk reporting formats and language.
        5. Integrate communication protocols with crisis management plans.
        6. Monitor effectiveness of communication and solicit feedback.
        7. Update protocols to reflect changes in stakeholder needs or risk environment.
        8. Document communication responsibilities and escalation paths.
        9. Provide training on risk communication best practices.
        10. Audit communication protocols for compliance and effectiveness.
        """,
        key_factors=[
            "Stakeholder identification",
            "Standardization of communication",
            "Feedback mechanisms",
            "Integration with crisis management",
            "Training and documentation"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Communication Function",
        adversary_position="Protocols may slow down urgent risk communication.",
        counter_arguments=[
            "Protocols include escalation for urgent risks.",
            "Regular review ensures protocols remain agile."
        ],
        resolution_strategy="Balance standardization with flexibility for urgent situations.",
        entity_scope="All stakeholders",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 8"
    ),
    DoctrineBlock(
        topic="risk_policy_documentation",
        keywords=["risk policy", "documentation", "governance", "standards"],
        conclusion_template="Comprehensive risk policy documentation underpins consistent and effective risk management.",
        reasoning_framework="""
        1. Define scope and objectives of the risk policy.
        2. Align policy with regulatory requirements and industry standards.
        3. Document risk management principles, roles, and responsibilities.
        4. Specify risk assessment, treatment, and reporting procedures.
        5. Establish policy review and update cycles.
        6. Communicate policy to all staff and stakeholders.
        7. Integrate policy with other governance documents.
        8. Monitor compliance with policy requirements.
        9. Provide training on policy content and application.
        10. Audit policy implementation for effectiveness.
        """,
        key_factors=[
            "Alignment with standards",
            "Clarity of roles and procedures",
            "Communication",
            "Review and update",
            "Compliance monitoring"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "Basel III"],
        burden_holder="Risk Governance Function",
        adversary_position="Lengthy policies may be ignored by staff.",
        counter_arguments=[
            "Summarize key points and provide accessible formats.",
            "Training reinforces policy awareness."
        ],
        resolution_strategy="Provide executive summaries and targeted training.",
        entity_scope="All staff and management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 5"
    ),
    DoctrineBlock(
        topic="risk_training_and_awareness",
        keywords=["risk training", "awareness", "capacity building", "culture"],
        conclusion_template="Ongoing risk training and awareness programs build organizational capacity for effective risk management.",
        reasoning_framework="""
        1. Assess training needs across roles and levels.
        2. Develop tailored training content for different audiences.
        3. Integrate risk training into onboarding and professional development.
        4. Use a mix of delivery methods (e.g., e-learning, workshops, simulations).
        5. Evaluate training effectiveness through assessments and feedback.
        6. Update training materials to reflect evolving risks and best practices.
        7. Promote risk awareness through campaigns and communications.
        8. Recognize and reward risk-aware behaviors.
        9. Monitor participation and completion rates.
        10. Audit training program for coverage and impact.
        """,
        key_factors=[
            "Needs assessment",
            "Tailored content",
            "Diverse delivery methods",
            "Evaluation and feedback",
            "Ongoing updates"
        ],
        primary_authority=["IRM", "ISO 31000", "COSO ERM"],
        burden_holder="Risk Training Function",
        adversary_position="Training is costly and may not change behavior.",
        counter_arguments=[
            "Targeted, engaging content increases effectiveness.",
            "Behavioral change is tracked and reinforced."
        ],
        resolution_strategy="Focus on high-impact training and measure behavioral outcomes.",
        entity_scope="All employees",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 4"
    ),
    DoctrineBlock(
        topic="risk_data_quality_management",
        keywords=["risk data", "quality management", "accuracy", "integrity"],
        conclusion_template="Risk data quality management ensures accuracy, completeness, and reliability of risk information.",
        reasoning_framework="""
        1. Define data quality standards for risk information.
        2. Implement data validation and verification processes.
        3. Assign data stewardship responsibilities.
        4. Monitor data quality metrics and report issues.
        5. Integrate data quality checks into risk systems.
        6. Provide training on data entry and management.
        7. Review and update data quality standards regularly.
        8. Escalate and remediate data quality issues promptly.
        9. Audit data quality processes for compliance.
        10. Communicate importance of data quality to all users.
        """,
        key_factors=[
            "Defined standards",
            "Validation processes",
            "Data stewardship",
            "Monitoring and reporting",
            "Training"
        ],
        primary_authority=["Basel III", "ISO 31000", "IRM"],
        burden_holder="Risk Data Steward",
        adversary_position="Data quality management is resource-intensive.",
        counter_arguments=[
            "High-quality data is essential for effective risk management.",
            "Automation reduces resource burden."
        ],
        resolution_strategy="Automate data quality checks and prioritize critical data elements.",
        entity_scope="Risk information systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Basel III, Annex 7"
    ),
    DoctrineBlock(
        topic="risk_systems_integration",
        keywords=["risk systems", "integration", "IT", "automation"],
        conclusion_template="Integration of risk systems enhances data consistency, efficiency, and reporting capabilities.",
        reasoning_framework="""
        1. Map existing risk management systems and data flows.
        2. Identify integration points and data exchange requirements.
        3. Select integration technologies and standards.
        4. Develop interfaces and automate data transfers.
        5. Test integration for accuracy and reliability.
        6. Document system architecture and integration protocols.
        7. Train users on integrated system functionality.
        8. Monitor system performance and resolve issues.
        9. Review integration as business and technology evolve.
        10. Audit integration for security and compliance.
        """,
        key_factors=[
            "System mapping",
            "Integration technology",
            "Testing and validation",
            "User training",
            "Ongoing monitoring"
        ],
        primary_authority=["ISO 31000", "IRM", "Basel III"],
        burden_holder="Risk IT Function",
        adversary_position="Integration projects are costly and disruptive.",
        counter_arguments=[
            "Long-term efficiency and data quality gains outweigh initial costs.",
            "Phased implementation reduces disruption."
        ],
        resolution_strategy="Implement integration in phases and communicate benefits.",
        entity_scope="Risk management systems",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 7"
    ),
    DoctrineBlock(
        topic="risk_governance_committee_structure",
        keywords=["risk governance", "committee", "structure", "oversight"],
        conclusion_template="A clear risk governance committee structure ensures effective oversight and accountability.",
        reasoning_framework="""
        1. Define roles and responsibilities for risk committees (e.g., board, executive, operational).
        2. Establish committee charters and meeting schedules.
        3. Align committee structure with organizational governance.
        4. Integrate risk committees with other oversight functions (e.g., audit, compliance).
        5. Document escalation and reporting protocols.
        6. Review committee effectiveness regularly.
        7. Communicate committee structure to all stakeholders.
        8. Provide training for committee members.
        9. Update structure as organization and risk environment evolve.
        10. Audit committee activities for compliance and effectiveness.
        """,
        key_factors=[
            "Defined roles",
            "Charters and schedules",
            "Integration with governance",
            "Communication",
            "Review and audit"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "Basel III"],
        burden_holder="Board Risk Committee",
        adversary_position="Multiple committees create confusion and overlap.",
        counter_arguments=[
            "Clear charters and protocols prevent overlap.",
            "Regular review ensures clarity."
        ],
        resolution_strategy="Document committee mandates and streamline reporting lines.",
        entity_scope="All governance levels",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 2"
    ),
    DoctrineBlock(
        topic="risk_event_escalation_protocols",
        keywords=["risk event", "escalation", "protocols", "incident management"],
        conclusion_template="Risk event escalation protocols ensure timely response and management of significant risk incidents.",
        reasoning_framework="""
        1. Define escalation thresholds for different risk events.
        2. Document escalation paths and responsible parties.
        3. Integrate escalation protocols with incident management systems.
        4. Communicate protocols to all relevant staff.
        5. Monitor adherence to escalation protocols.
        6. Review and update protocols based on incident experience.
        7. Provide training and simulations for escalation procedures.
        8. Audit escalation process for compliance and effectiveness.
        9. Align protocols with regulatory and contractual requirements.
        10. Document lessons learned from escalated incidents.
        """,
        key_factors=[
            "Clear thresholds",
            "Documented paths",
            "Integration with incident management",
            "Training",
            "Review and update"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Incident Manager",
        adversary_position="Escalation protocols may be bypassed in urgent situations.",
        counter_arguments=[
            "Protocols include flexibility for urgent escalation.",
            "Regular training reinforces adherence."
        ],
        resolution_strategy="Test protocols regularly and update for real-world applicability.",
        entity_scope="All business units",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 8"
    ),
    DoctrineBlock(
        topic="risk_appetite_statement_review",
        keywords=["risk appetite", "statement", "review", "governance"],
        conclusion_template="Regular review of risk appetite statements ensures ongoing alignment with strategy and risk environment.",
        reasoning_framework="""
        1. Schedule annual or event-driven reviews of risk appetite statements.
        2. Involve board and executive leadership in review process.
        3. Assess alignment with current strategy, objectives, and risk profile.
        4. Update statements to reflect changes in business or external environment.
        5. Communicate updates to all relevant stakeholders.
        6. Integrate revised statements into risk management processes.
        7. Document rationale for changes.
        8. Monitor adherence to updated risk appetite.
        9. Provide training on new statements.
        10. Audit review process for completeness and effectiveness.
        """,
        key_factors=[
            "Regular review schedule",
            "Leadership involvement",
            "Alignment with strategy",
            "Communication",
            "Integration with processes"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "Basel III"],
        burden_holder="Board of Directors",
        adversary_position="Frequent changes to statements create uncertainty.",
        counter_arguments=[
            "Reviews are event-driven and changes are communicated clearly.",
            "Stability is balanced with adaptability."
        ],
        resolution_strategy="Balance frequency of review with need for stability.",
        entity_scope="Enterprise-wide",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 6"
    ),
    DoctrineBlock(
        topic="risk_model_validation",
        keywords=["risk model", "validation", "quantitative", "assumptions"],
        conclusion_template="Risk model validation ensures quantitative models are accurate, reliable, and fit for purpose.",
        reasoning_framework="""
        1. Define validation criteria and scope for each model.
        2. Test model assumptions, inputs, and outputs.
        3. Compare model results with historical data and benchmarks.
        4. Document validation process and findings.
        5. Engage independent reviewers or validators.
        6. Update models based on validation outcomes.
        7. Communicate validation results to stakeholders.
        8. Integrate validation into model governance framework.
        9. Review validation process regularly.
        10. Audit model validation for compliance and effectiveness.
        """,
        key_factors=[
            "Validation criteria",
            "Independent review",
            "Benchmarking",
            "Documentation",
            "Model governance"
        ],
        primary_authority=["Basel III", "GARP", "ISO 31010"],
        burden_holder="Model Owner",
        adversary_position="Validation adds cost and delays model deployment.",
        counter_arguments=[
            "Validation is essential for model reliability and regulatory compliance.",
            "Efficient processes minimize delays."
        ],
        resolution_strategy="Integrate validation into model development lifecycle.",
        entity_scope="Quantitative risk models",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Basel III, Annex 8"
    ),
    DoctrineBlock(
        topic="risk_tolerance_setting",
        keywords=["risk tolerance", "limits", "risk appetite", "thresholds"],
        conclusion_template="Risk tolerance is set as the acceptable range of variation in risk exposure, supporting risk appetite implementation.",
        reasoning_framework="""
        1. Define risk tolerance levels for key risk categories.
        2. Align tolerance with risk appetite and business objectives.
        3. Set quantitative and qualitative thresholds.
        4. Communicate tolerance levels to all relevant staff.
        5. Monitor exposures against tolerance limits.
        6. Escalate breaches according to governance protocols.
        7. Review and update tolerance levels regularly.
        8. Document rationale for tolerance settings.
        9. Integrate tolerance into risk management processes.
        10. Audit tolerance adherence for compliance.
        """,
        key_factors=[
            "Alignment with risk appetite",
            "Clear thresholds",
            "Communication",
            "Monitoring and escalation",
            "Review and update"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "Basel III"],
        burden_holder="Risk Governance Function",
        adversary_position="Tolerance levels are arbitrary and may not reflect business needs.",
        counter_arguments=[
            "Levels are set collaboratively and reviewed regularly.",
            "Alignment with appetite ensures business relevance."
        ],
        resolution_strategy="Review tolerance settings annually and involve key stakeholders.",
        entity_scope="All risk categories",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 7"
    ),
    DoctrineBlock(
        topic="risk_acceptance_criteria",
        keywords=["risk acceptance", "criteria", "thresholds", "decision-making"],
        conclusion_template="Risk acceptance criteria define when residual risk is tolerable and does not require further mitigation.",
        reasoning_framework="""
        1. Establish clear criteria for risk acceptance based on risk appetite and tolerance.
        2. Document rationale for accepting specific risks.
        3. Integrate acceptance criteria into risk assessment and treatment processes.
        4. Communicate criteria to all risk owners.
        5. Review accepted risks regularly for changes in exposure.
        6. Escalate risks that exceed acceptance criteria.
        7. Audit acceptance decisions for compliance and consistency.
        8. Provide training on acceptance criteria and decision-making.
        9. Benchmark criteria against industry standards.
        10. Update criteria as business and risk environment evolve.
        """,
        key_factors=[
            "Alignment with appetite and tolerance",
            "Documentation",
            "Communication",
            "Regular review",
            "Benchmarking"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Owner",
        adversary_position="Acceptance criteria may be inconsistently applied.",
        counter_arguments=[
            "Standardized criteria and documentation ensure consistency.",
            "Regular audits reinforce adherence."
        ],
        resolution_strategy="Standardize criteria and require documentation for all acceptance decisions.",
        entity_scope="All risk owners",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 6.5"
    ),
    DoctrineBlock(
        topic="risk_response_documentation",
        keywords=["risk response", "documentation", "action plans", "tracking"],
        conclusion_template="Risk response documentation ensures actions are tracked, monitored, and completed.",
        reasoning_framework="""
        1. Document selected risk responses and rationale.
        2. Assign responsibility and deadlines for each action.
        3. Integrate response documentation with risk register.
        4. Monitor progress and update status regularly.
        5. Communicate status to stakeholders and escalate delays.
        6. Review effectiveness of completed actions.
        7. Audit documentation for completeness and accuracy.
        8. Provide templates and guidance for response documentation.
        9. Archive completed actions for future reference.
        10. Update documentation protocols as needed.
        """,
        key_factors=[
            "Clear documentation",
            "Responsibility assignment",
            "Monitoring and escalation",
            "Templates and guidance",
            "Review and audit"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Owner",
        adversary_position="Documentation adds administrative burden.",
        counter_arguments=[
            "Documentation enables tracking and accountability.",
            "Templates streamline the process."
        ],
        resolution_strategy="Provide user-friendly templates and integrate with existing systems.",
        entity_scope="All risk responses",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 6.5"
    ),
    DoctrineBlock(
        topic="risk_monitoring_and_review",
        keywords=["risk monitoring", "review", "continuous improvement", "oversight"],
        conclusion_template="Ongoing risk monitoring and review ensure risk management remains effective and relevant.",
        reasoning_framework="""
        1. Establish regular monitoring and review cycles for all risks.
        2. Use key risk indicators and risk reports to track exposures.
        3. Update risk assessments as new information emerges.
        4. Review effectiveness of controls and mitigation actions.
        5. Escalate significant changes or breaches.
        6. Document monitoring and review activities.
        7. Integrate findings into risk reporting and governance.
        8. Provide training on monitoring tools and processes.
        9. Audit monitoring and review for completeness.
        10. Use findings to drive continuous improvement.
        """,
        key_factors=[
            "Regular review cycles",
            "Use of KRIs",
            "Control effectiveness",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Monitoring Function",
        adversary_position="Monitoring is resource-intensive and may not detect all risks.",
        counter_arguments=[
            "Prioritization and automation increase efficiency.",
            "Continuous improvement addresses gaps."
        ],
        resolution_strategy="Automate monitoring where possible and focus on key risks.",
        entity_scope="All risk categories",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 6.7"
    ),
    DoctrineBlock(
        topic="risk_reporting_to_regulators",
        keywords=["risk reporting", "regulators", "compliance", "disclosure"],
        conclusion_template="Risk reporting to regulators ensures compliance with legal and regulatory requirements.",
        reasoning_framework="""
        1. Identify applicable regulatory reporting requirements.
        2. Align internal risk reporting with external disclosure obligations.
        3. Standardize data formats and definitions.
        4. Assign responsibility for regulatory reporting.
        5. Monitor changes in regulatory requirements.
        6. Document reporting processes and controls.
        7. Review and validate data before submission.
        8. Communicate reporting obligations to relevant staff.
        9. Audit reporting process for compliance and accuracy.
        10. Engage with regulators to clarify requirements.
        """,
        key_factors=[
            "Regulatory requirements",
            "Standardization",
            "Responsibility assignment",
            "Data validation",
            "Audit and review"
        ],
        primary_authority=["Basel III", "SEC", "EBA"],
        burden_holder="Compliance Function",
        adversary_position="Frequent regulatory changes increase reporting burden.",
        counter_arguments=[
            "Monitoring and automation reduce manual effort.",
            "Regular communication with regulators clarifies changes."
        ],
        resolution_strategy="Automate reporting processes and maintain regulatory watch.",
        entity_scope="Regulated entities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Basel III, Pillar 3"
    ),
    DoctrineBlock(
        topic="risk_management_maturity_assessment",
        keywords=["risk management", "maturity assessment", "benchmarking", "continuous improvement"],
        conclusion_template="Risk management maturity assessment benchmarks processes against best practices and identifies improvement opportunities.",
        reasoning_framework="""
        1. Select a maturity assessment framework (e.g., CMMI, ISO 31000 maturity model).
        2. Assess current state of risk management processes.
        3. Benchmark against industry peers and best practices.
        4. Identify strengths, gaps, and improvement opportunities.
        5. Develop action plans to address gaps.
        6. Communicate assessment results to leadership.
        7. Monitor progress on improvement actions.
        8. Review and update maturity assessment regularly.
        9. Integrate findings into risk strategy and planning.
        10. Audit assessment process for completeness and accuracy.
        """,
        key_factors=[
            "Selection of framework",
            "Benchmarking",
            "Gap analysis",
            "Action planning",
            "Monitoring progress"
        ],
        primary_authority=["IRM", "ISO 31000", "COSO ERM"],
        burden_holder="Risk Management Function",
        adversary_position="Maturity assessments are subjective and may not drive real change.",
        counter_arguments=[
            "Use of external benchmarks increases objectivity.",
            "Action plans ensure follow-through."
        ],
        resolution_strategy="Benchmark externally and tie assessment to improvement plans.",
        entity_scope="Enterprise risk management",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="IRM Risk Maturity Model"
    ),
    DoctrineBlock(
        topic="risk_technology_selection",
        keywords=["risk technology", "selection", "tools", "automation"],
        conclusion_template="Selection of risk technology tools is based on business needs, scalability, and integration capabilities.",
        reasoning_framework="""
        1. Assess business requirements for risk management technology.
        2. Evaluate available tools for functionality, scalability, and integration.
        3. Engage stakeholders in selection process.
        4. Pilot shortlisted tools and gather user feedback.
        5. Assess vendor support and security features.
        6. Document selection criteria and decision rationale.
        7. Plan for implementation, training, and change management.
        8. Monitor tool performance post-implementation.
        9. Review technology needs as business evolves.
        10. Audit technology selection and implementation process.
        """,
        key_factors=[
            "Business requirements",
            "Scalability",
            "Integration",
            "User feedback",
            "Vendor support"
        ],
        primary_authority=["ISO 31000", "IRM", "GARP"],
        burden_holder="Risk IT Function",
        adversary_position="Technology selection is driven by trends, not needs.",
        counter_arguments=[
            "Needs assessment and stakeholder input drive selection.",
            "Piloting ensures fit for purpose."
        ],
        resolution_strategy="Base selection on documented needs and pilot results.",
        entity_scope="Risk management systems",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 7"
    ),
    DoctrineBlock(
        topic="risk_management_resource_allocation",
        keywords=["risk management", "resource allocation", "budget", "prioritization"],
        conclusion_template="Resource allocation for risk management is prioritized based on risk exposure and strategic objectives.",
        reasoning_framework="""
        1. Assess risk exposures and prioritize based on impact and likelihood.
        2. Align resource allocation with risk appetite and business strategy.
        3. Develop risk-based budgeting and staffing plans.
        4. Monitor resource utilization and adjust as needed.
        5. Document allocation decisions and rationale.
        6. Communicate resource plans to stakeholders.
        7. Review allocation effectiveness regularly.
        8. Integrate resource allocation with performance management.
        9. Audit resource allocation for transparency and effectiveness.
        10. Update allocation in response to changes in risk profile.
        """,
        key_factors=[
            "Risk-based prioritization",
            "Alignment with strategy",
            "Monitoring utilization",
            "Documentation",
            "Review and audit"
        ],
        primary_authority=["COSO ERM", "ISO 31000", "IRM"],
        burden_holder="Risk Management Function",
        adversary_position="Resource allocation is often reactive, not proactive.",
        counter_arguments=[
            "Risk-based planning ensures proactive allocation.",
            "Regular review allows for adjustment."
        ],
        resolution_strategy="Integrate risk assessment into budgeting and planning cycles.",
        entity_scope="All risk management activities",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="COSO ERM 2017, Principle 10"
    ),
    DoctrineBlock(
        topic="risk_management_performance_metrics",
        keywords=["risk management", "performance metrics", "KPIs", "effectiveness"],
        conclusion_template="Risk management performance metrics track effectiveness and support continuous improvement.",
        reasoning_framework="""
        1. Define key performance indicators (KPIs) for risk management activities.
        2. Align metrics with risk management objectives and strategy.
        3. Monitor and report on KPIs regularly.
        4. Use metrics to identify strengths and areas for improvement.
        5. Integrate performance metrics into management dashboards.
        6. Review and update metrics as objectives evolve.
        7. Communicate performance results to stakeholders.
        8. Use metrics to inform resource allocation and training.
        9. Audit metrics for accuracy and relevance.
        10. Benchmark against industry standards.
        """,
        key_factors=[
            "Relevant KPIs",
            "Alignment with objectives",
            "Regular monitoring",
            "Communication",
            "Benchmarking"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Risk Management Function",
        adversary_position="Metrics may drive focus on quantity over quality.",
        counter_arguments=[
            "Balanced scorecards include both quantitative and qualitative metrics.",
            "Regular review ensures relevance."
        ],
        resolution_strategy="Use balanced metrics and review for unintended consequences.",
        entity_scope="All risk management activities",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 6.7"
    ),
    DoctrineBlock(
        topic="risk_management_external_assurance",
        keywords=["risk management", "external assurance", "audit", "validation"],
        conclusion_template="External assurance provides independent validation of risk management effectiveness.",
        reasoning_framework="""
        1. Define scope and objectives for external assurance engagements.
        2. Select qualified external auditors or consultants.
        3. Provide access to relevant documentation and personnel.
        4. Review assurance findings and recommendations.
        5. Develop action plans to address findings.
        6. Communicate assurance results to leadership and stakeholders.
        7. Monitor implementation of recommendations.
        8. Integrate assurance into risk governance framework.
        9. Schedule regular external assurance reviews.
        10. Audit follow-up actions for completion.
        """,
        key_factors=[
            "Qualified assurance providers",
            "Scope definition",
            "Action planning",
            "Communication",
            "Follow-up monitoring"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IIA"],
        burden_holder="Risk Management Function",
        adversary_position="External assurance is costly and may duplicate internal efforts.",
        counter_arguments=[
            "External perspective adds value and credibility.",
            "Scope is tailored to avoid duplication."
        ],
        resolution_strategy="Align assurance scope with internal audit and risk priorities.",
        entity_scope="Enterprise risk management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IIA Standards, Section 1300"
    ),
    DoctrineBlock(
        topic="risk_management_policy_breaches",
        keywords=["risk management", "policy breaches", "non-compliance", "escalation"],
        conclusion_template="Policy breaches are managed through defined escalation, investigation, and remediation protocols.",
        reasoning_framework="""
        1. Define what constitutes a policy breach.
        2. Establish escalation and reporting protocols for breaches.
        3. Investigate breaches and document findings.
        4. Develop and implement remediation actions.
        5. Communicate breaches and actions to relevant stakeholders.
        6. Monitor recurrence and effectiveness of remediation.
        7. Review and update breach management protocols.
        8. Provide training on breach identification and reporting.
        9. Audit breach management for compliance and effectiveness.
        10. Integrate lessons learned into policy updates.
        """,
        key_factors=[
            "Clear breach definitions",
            "Escalation protocols",
            "Remediation",
            "Communication",
            "Review and audit"
        ],
        primary_authority=["ISO 31000", "COSO ERM", "IRM"],
        burden_holder="Compliance Function",
        adversary_position="Strict protocols may discourage breach reporting.",
        counter_arguments=[
            "Confidential reporting channels encourage transparency.",
            "Non-punitive culture supports reporting."
        ],
        resolution_strategy="Promote a just culture and provide confidential reporting mechanisms.",
        entity_scope="All staff and management",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ISO 31000:2018, Section 8"
    ),
    DoctrineBlock(
        topic="risk_management_continuity_planning",
        keywords=["risk management", "continuity planning", "business continuity", "resilience"],
        conclusion_template="Continuity planning ensures critical operations can continue during and after disruptive risk events.",
        reasoning_framework="""
        1. Identify critical business functions and dependencies.
        2. Assess risks to continuity and develop response strategies.
        3. Document business continuity and disaster recovery plans.
        4. Assign