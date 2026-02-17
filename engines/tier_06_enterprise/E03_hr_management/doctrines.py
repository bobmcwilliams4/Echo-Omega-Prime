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
        topic="flsa_overtime_classification",
        keywords=["FLSA", "overtime", "exempt", "non-exempt", "salary threshold", "duties test"],
        conclusion_template="Employee is classified as {classification} under FLSA overtime rules.",
        reasoning_framework="""
        1. Identify the employee's job title and responsibilities.
        2. Apply the FLSA duties test to determine if the role qualifies as exempt (executive, administrative, professional, computer, outside sales).
        3. Verify salary threshold: employee must earn at least $684/week to qualify as exempt.
        4. Consider state-specific overtime requirements, which may be more stringent.
        5. Review any applicable collective bargaining agreements.
        6. Document the rationale for classification and maintain records.
        7. Monitor for changes in job duties or compensation that may affect classification.
        8. Communicate classification status to employee and maintain compliance.
        9. Audit classifications annually or upon regulatory updates.
        10. Address misclassification risks proactively.
        """,
        key_factors=[
            "Job duties",
            "Salary threshold",
            "State law variations",
            "Collective bargaining agreements",
            "Regulatory updates"
        ],
        primary_authority=[
            "Fair Labor Standards Act (FLSA)",
            "Department of Labor (DOL) Wage & Hour Division"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims misclassification and seeks back pay.",
        counter_arguments=[
            "Employee's duties do not meet exemption criteria.",
            "Salary threshold not met.",
            "State law overrides federal exemption."
        ],
        resolution_strategy="Conduct thorough job analysis, apply FLSA tests, consult legal counsel, and correct misclassifications promptly.",
        entity_scope="Private and public employers subject to FLSA",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="29 CFR Part 541"
    ),
    DoctrineBlock(
        topic="fmla_eligibility_and_entitlement",
        keywords=["FMLA", "leave", "eligibility", "entitlement", "serious health condition", "12 months", "1,250 hours"],
        conclusion_template="Employee is {eligible/not eligible} for FMLA leave and entitled to {amount} weeks.",
        reasoning_framework="""
        1. Confirm employer coverage: 50+ employees within 75-mile radius.
        2. Assess employee eligibility: employed for at least 12 months and worked 1,250 hours in preceding 12 months.
        3. Determine qualifying reason: serious health condition, birth/adoption, military exigency.
        4. Calculate entitlement: up to 12 weeks of unpaid, job-protected leave per year.
        5. Review documentation requirements and notice provisions.
        6. Ensure restoration to same or equivalent position upon return.
        7. Address intermittent leave and reduced schedule requests.
        8. Monitor for retaliation or interference claims.
        9. Coordinate with state family leave laws and employer policies.
        10. Maintain accurate leave records.
        """,
        key_factors=[
            "Employer size",
            "Employee tenure",
            "Hours worked",
            "Qualifying event",
            "Documentation"
        ],
        primary_authority=[
            "Family and Medical Leave Act (FMLA)",
            "29 CFR Part 825"
        ],
        burden_holder="Employee",
        adversary_position="Employer disputes eligibility or entitlement.",
        counter_arguments=[
            "Employee did not meet hours threshold.",
            "Employer not covered.",
            "Leave not for qualifying reason."
        ],
        resolution_strategy="Verify eligibility, review documentation, apply FMLA regulations, and communicate decisions transparently.",
        entity_scope="Covered employers and eligible employees",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="29 CFR Part 825"
    ),
    DoctrineBlock(
        topic="pay_equity_analysis",
        keywords=["pay equity", "compensation", "gender", "race", "equal pay", "disparities", "analysis"],
        conclusion_template="Pay equity assessment reveals {level} of disparity and recommends {action}.",
        reasoning_framework="""
        1. Gather compensation data across job families, levels, and demographics.
        2. Normalize data for job content, tenure, and location.
        3. Apply statistical analysis to identify disparities by gender, race, or other protected classes.
        4. Compare against market benchmarks and internal equity standards.
        5. Evaluate root causes: hiring, promotion, performance, negotiation practices.
        6. Document findings and develop remediation plan.
        7. Communicate results to stakeholders and ensure transparency.
        8. Monitor ongoing pay equity through regular audits.
        9. Address legal risks and regulatory requirements.
        10. Integrate pay equity into compensation philosophy.
        """,
        key_factors=[
            "Compensation data",
            "Demographic information",
            "Job content",
            "Market benchmarks",
            "Statistical analysis"
        ],
        primary_authority=[
            "Equal Pay Act of 1963",
            "Title VII of the Civil Rights Act",
            "EEOC Guidelines"
        ],
        burden_holder="Employer",
        adversary_position="Employee or regulator alleges pay discrimination.",
        counter_arguments=[
            "Disparities due to legitimate factors (performance, tenure).",
            "Market-driven compensation differences.",
            "Job content not comparable."
        ],
        resolution_strategy="Conduct robust pay equity audits, remediate disparities, and maintain compliance with legal standards.",
        entity_scope="All employers subject to federal/state pay equity laws",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EEOC v. Walmart Stores, Inc. (2020)"
    ),
    DoctrineBlock(
        topic="ada_reasonable_accommodation",
        keywords=["ADA", "reasonable accommodation", "disability", "interactive process", "undue hardship"],
        conclusion_template="Accommodation request is {approved/denied} based on ADA analysis.",
        reasoning_framework="""
        1. Identify whether employee has a qualifying disability under ADA.
        2. Engage in interactive process to determine accommodation needs.
        3. Evaluate requested accommodation for reasonableness and effectiveness.
        4. Assess potential undue hardship on employer operations.
        5. Consider alternative accommodations if initial request is not feasible.
        6. Document all communications and decisions.
        7. Ensure confidentiality and non-retaliation.
        8. Monitor accommodation effectiveness and adjust as needed.
        9. Train managers on ADA compliance and interactive process.
        10. Address disputes through mediation or legal review.
        """,
        key_factors=[
            "Disability status",
            "Accommodation request",
            "Undue hardship",
            "Interactive process",
            "Documentation"
        ],
        primary_authority=[
            "Americans with Disabilities Act (ADA)",
            "EEOC Enforcement Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Employee claims denial or insufficient accommodation.",
        counter_arguments=[
            "Accommodation imposes undue hardship.",
            "Employee not qualified under ADA.",
            "Alternative accommodation offered."
        ],
        resolution_strategy="Engage in interactive process, document decisions, and seek legal counsel for complex cases.",
        entity_scope="Covered employers and qualified employees",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="US Airways, Inc. v. Barnett (2002)"
    ),
    DoctrineBlock(
        topic="workforce_turnover_analysis",
        keywords=["turnover", "attrition", "retention", "exit interviews", "analysis", "HR metrics"],
        conclusion_template="Turnover rate is {rate} and primary drivers are {drivers}.",
        reasoning_framework="""
        1. Collect turnover data: voluntary and involuntary separations.
        2. Segment data by department, tenure, demographics, and performance.
        3. Analyze exit interview feedback for root causes.
        4. Calculate turnover rates and benchmark against industry standards.
        5. Identify high-risk areas and trends.
        6. Develop retention strategies targeting key drivers.
        7. Monitor impact of interventions and adjust as needed.
        8. Communicate findings to leadership and stakeholders.
        9. Integrate turnover analysis into workforce planning.
        10. Conduct periodic reviews to ensure ongoing improvement.
        """,
        key_factors=[
            "Turnover data",
            "Exit interview feedback",
            "Benchmarking",
            "Retention strategies",
            "Demographics"
        ],
        primary_authority=[
            "SHRM Turnover Metrics",
            "Bureau of Labor Statistics"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge retention strategies or data accuracy.",
        counter_arguments=[
            "Turnover is industry-driven.",
            "Retention strategies ineffective.",
            "Data collection incomplete."
        ],
        resolution_strategy="Implement robust data collection, analyze root causes, and tailor retention initiatives.",
        entity_scope="All employers",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Turnover Analysis Guidelines"
    ),
    DoctrineBlock(
        topic="compensation_band_design",
        keywords=["compensation", "salary bands", "pay ranges", "job evaluation", "market pricing"],
        conclusion_template="Compensation bands are designed to align with {market/internal} benchmarks.",
        reasoning_framework="""
        1. Conduct job evaluation to determine relative value of roles.
        2. Gather market compensation data for comparable positions.
        3. Establish pay bands based on job families, levels, and geographic differentials.
        4. Define minimum, midpoint, and maximum for each band.
        5. Ensure internal equity and external competitiveness.
        6. Document band structure and rationale.
        7. Communicate bands to managers and employees.
        8. Review and update bands annually or upon market changes.
        9. Integrate bands into performance and promotion processes.
        10. Address exceptions through governance and approval processes.
        """,
        key_factors=[
            "Job evaluation",
            "Market data",
            "Internal equity",
            "Geographic differentials",
            "Governance"
        ],
        primary_authority=[
            "SHRM Compensation Guidelines",
            "WorldatWork Salary Survey"
        ],
        burden_holder="Employer",
        adversary_position="Employee challenges pay band placement or fairness.",
        counter_arguments=[
            "Market data outdated.",
            "Internal equity not maintained.",
            "Band structure lacks transparency."
        ],
        resolution_strategy="Update market data regularly, apply rigorous job evaluation, and ensure transparent communication.",
        entity_scope="All employers implementing structured compensation",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="WorldatWork Compensation Banding Standards"
    ),
    DoctrineBlock(
        topic="performance_calibration_process",
        keywords=["performance", "calibration", "ratings", "bias", "HR process", "fairness"],
        conclusion_template="Performance calibration results in {distribution} of ratings.",
        reasoning_framework="""
        1. Collect performance ratings from managers across departments.
        2. Convene calibration sessions to review ratings and ensure consistency.
        3. Identify and address rating biases (leniency, severity, central tendency).
        4. Align ratings with organizational performance standards and goals.
        5. Document rationale for rating adjustments.
        6. Communicate calibration outcomes to managers and employees.
        7. Integrate calibration into compensation, promotion, and development decisions.
        8. Monitor calibration process for fairness and effectiveness.
        9. Train managers on calibration best practices.
        10. Review calibration process annually for improvements.
        """,
        key_factors=[
            "Performance ratings",
            "Calibration sessions",
            "Bias mitigation",
            "Documentation",
            "Manager training"
        ],
        primary_authority=[
            "SHRM Performance Management Standards",
            "Harvard Business Review Calibration Research"
        ],
        burden_holder="Employer",
        adversary_position="Employee alleges unfair rating or bias.",
        counter_arguments=[
            "Calibration process lacks transparency.",
            "Ratings not aligned with performance.",
            "Bias not adequately addressed."
        ],
        resolution_strategy="Implement structured calibration sessions, document decisions, and provide manager training.",
        entity_scope="Employers with formal performance management systems",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Performance Calibration Guidelines"
    ),
    DoctrineBlock(
        topic="succession_planning_framework",
        keywords=["succession planning", "leadership", "talent pipeline", "critical roles", "bench strength"],
        conclusion_template="Succession plan identifies {candidates} for {critical roles}.",
        reasoning_framework="""
        1. Identify critical roles essential to organizational success.
        2. Assess current bench strength and talent pipeline.
        3. Evaluate potential successors based on performance, potential, and readiness.
        4. Develop individualized development plans for successors.
        5. Document succession plan and communicate to leadership.
        6. Monitor progress and update plans annually.
        7. Integrate succession planning with talent management and workforce planning.
        8. Address diversity and inclusion in succession decisions.
        9. Mitigate risks of leadership gaps through proactive planning.
        10. Review succession plan effectiveness post-transition.
        """,
        key_factors=[
            "Critical roles",
            "Talent pipeline",
            "Successor evaluation",
            "Development plans",
            "Diversity and inclusion"
        ],
        primary_authority=[
            "SHRM Succession Planning Toolkit",
            "Harvard Business Review Leadership Succession"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge succession plan transparency or fairness.",
        counter_arguments=[
            "Successor selection lacks objectivity.",
            "Development plans not implemented.",
            "Diversity not considered."
        ],
        resolution_strategy="Apply structured evaluation, document decisions, and ensure alignment with organizational goals.",
        entity_scope="Employers with leadership succession needs",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Succession Planning Standards"
    ),
    DoctrineBlock(
        topic="benefits_cost_optimization",
        keywords=["benefits", "cost optimization", "healthcare", "plan design", "employee contribution"],
        conclusion_template="Benefits plan achieves {level} of cost optimization and employee satisfaction.",
        reasoning_framework="""
        1. Analyze current benefits costs and utilization rates.
        2. Benchmark against industry standards and peer organizations.
        3. Evaluate plan design options for cost containment and value.
        4. Assess employee preferences and satisfaction through surveys.
        5. Negotiate with benefits providers for competitive rates.
        6. Implement wellness and preventive care initiatives.
        7. Communicate changes and rationale to employees.
        8. Monitor impact of changes on costs and satisfaction.
        9. Adjust plan design annually based on feedback and market trends.
        10. Ensure compliance with ACA and other regulatory requirements.
        """,
        key_factors=[
            "Benefits costs",
            "Plan design",
            "Employee satisfaction",
            "Provider negotiations",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Affordable Care Act (ACA)",
            "SHRM Benefits Benchmarking"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge plan changes or cost increases.",
        counter_arguments=[
            "Plan design reduces value.",
            "Employee contributions too high.",
            "Compliance risks."
        ],
        resolution_strategy="Balance cost optimization with employee satisfaction and legal compliance.",
        entity_scope="Employers offering benefits plans",
        confidence=0.86,
        confidence_zone="Medium",
        controlling_precedent="ACA Benefits Compliance Standards"
    ),
    DoctrineBlock(
        topic="recruiting_metrics_pipeline",
        keywords=["recruiting", "metrics", "pipeline", "time to fill", "quality of hire", "source effectiveness"],
        conclusion_template="Recruiting pipeline metrics show {performance} in {areas}.",
        reasoning_framework="""
        1. Define key recruiting metrics: time to fill, quality of hire, source effectiveness, candidate experience.
        2. Collect data across recruiting stages: sourcing, screening, interviewing, offer, onboarding.
        3. Analyze pipeline conversion rates and bottlenecks.
        4. Benchmark metrics against industry standards.
        5. Identify high-performing sources and channels.
        6. Assess candidate quality through post-hire performance.
        7. Document findings and share with recruiting team.
        8. Implement process improvements based on data.
        9. Monitor impact of changes on recruiting outcomes.
        10. Review metrics quarterly for continuous improvement.
        """,
        key_factors=[
            "Time to fill",
            "Quality of hire",
            "Source effectiveness",
            "Candidate experience",
            "Benchmarking"
        ],
        primary_authority=[
            "SHRM Recruiting Metrics",
            "LinkedIn Talent Solutions"
        ],
        burden_holder="Employer",
        adversary_position="Hiring managers challenge recruiting effectiveness.",
        counter_arguments=[
            "Metrics not aligned with business needs.",
            "Data collection incomplete.",
            "Quality of hire not accurately measured."
        ],
        resolution_strategy="Implement robust metrics tracking, analyze pipeline data, and adjust recruiting strategies.",
        entity_scope="Employers with formal recruiting processes",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Recruiting Metrics Standards"
    ),
    DoctrineBlock(
        topic="employee_engagement_measurement",
        keywords=["employee engagement", "measurement", "survey", "retention", "productivity"],
        conclusion_template="Employee engagement score is {score} with key drivers {drivers}.",
        reasoning_framework="""
        1. Develop or select validated engagement survey instrument.
        2. Administer survey to all employees and ensure confidentiality.
        3. Analyze survey results for overall engagement score and key drivers.
        4. Segment results by department, tenure, and demographics.
        5. Identify areas of strength and improvement.
        6. Share results with leadership and employees.
        7. Develop action plans to address engagement gaps.
        8. Monitor impact of interventions on engagement scores.
        9. Repeat survey annually or biannually.
        10. Integrate engagement measurement into HR strategy.
        """,
        key_factors=[
            "Survey instrument",
            "Confidentiality",
            "Segmentation",
            "Action planning",
            "Leadership communication"
        ],
        primary_authority=[
            "Gallup Q12 Engagement Survey",
            "SHRM Engagement Measurement Standards"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge survey validity or follow-up actions.",
        counter_arguments=[
            "Survey lacks confidentiality.",
            "Action plans not implemented.",
            "Engagement drivers not addressed."
        ],
        resolution_strategy="Use validated surveys, ensure confidentiality, and follow through on action plans.",
        entity_scope="Employers measuring engagement",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Gallup Engagement Research"
    ),
    DoctrineBlock(
        topic="title_vii_discrimination",
        keywords=["Title VII", "discrimination", "protected classes", "EEOC", "employment practices"],
        conclusion_template="Title VII analysis finds {presence/absence} of discrimination.",
        reasoning_framework="""
        1. Identify alleged discriminatory practice or policy.
        2. Determine if affected individuals are members of protected classes (race, color, religion, sex, national origin).
        3. Analyze evidence of disparate treatment or impact.
        4. Review employer's legitimate, non-discriminatory reasons.
        5. Evaluate history of similar practices and outcomes.
        6. Document findings and rationale.
        7. Address retaliation risks and ensure confidentiality.
        8. Implement corrective actions if discrimination found.
        9. Communicate outcomes to affected parties.
        10. Monitor for recurrence and update policies as needed.
        """,
        key_factors=[
            "Protected class status",
            "Disparate treatment/impact",
            "Employer rationale",
            "Documentation",
            "Retaliation risks"
        ],
        primary_authority=[
            "Title VII of the Civil Rights Act",
            "EEOC Enforcement Guidance"
        ],
        burden_holder="Employee",
        adversary_position="Employer denies discrimination or offers legitimate reasons.",
        counter_arguments=[
            "Legitimate, non-discriminatory reasons.",
            "No evidence of disparate impact.",
            "Policy applied consistently."
        ],
        resolution_strategy="Conduct thorough investigation, apply Title VII standards, and implement corrective actions.",
        entity_scope="Employers subject to Title VII",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="McDonnell Douglas Corp. v. Green (1973)"
    ),
    DoctrineBlock(
        topic="workplace_harassment_prevention",
        keywords=["harassment", "prevention", "training", "policy", "EEOC", "hostile work environment"],
        conclusion_template="Harassment prevention measures are {effective/ineffective} based on analysis.",
        reasoning_framework="""
        1. Review harassment prevention policy for clarity and coverage.
        2. Assess training programs for frequency and effectiveness.
        3. Evaluate reporting mechanisms and confidentiality protections.
        4. Analyze incident data for trends and recurrence.
        5. Interview employees to gauge awareness and comfort with reporting.
        6. Implement corrective actions for identified gaps.
        7. Monitor impact of interventions on harassment rates.
        8. Communicate policy updates and training outcomes.
        9. Address retaliation risks proactively.
        10. Review prevention measures annually.
        """,
        key_factors=[
            "Policy clarity",
            "Training effectiveness",
            "Reporting mechanisms",
            "Incident data",
            "Retaliation risks"
        ],
        primary_authority=[
            "EEOC Harassment Guidance",
            "Title VII of the Civil Rights Act"
        ],
        burden_holder="Employer",
        adversary_position="Employees allege ineffective prevention or retaliation.",
        counter_arguments=[
            "Policy not communicated.",
            "Training insufficient.",
            "Reporting mechanisms inadequate."
        ],
        resolution_strategy="Strengthen policy, enhance training, and ensure robust reporting and follow-up.",
        entity_scope="Employers subject to harassment laws",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Faragher v. City of Boca Raton (1998)"
    ),
    DoctrineBlock(
        topic="warn_act_compliance",
        keywords=["WARN Act", "layoff", "notice", "employment loss", "compliance"],
        conclusion_template="WARN Act compliance requires {notice period} and {actions}.",
        reasoning_framework="""
        1. Determine if layoff or plant closing meets WARN Act thresholds (50+ employees, 30-day period).
        2. Calculate number of affected employees and employment loss.
        3. Assess notice period requirements (60 days).
        4. Review exceptions: faltering company, unforeseen circumstances, natural disaster.
        5. Document notice delivery to employees, union, and government agencies.
        6. Monitor for compliance with state mini-WARN laws.
        7. Address penalties for non-compliance.
        8. Communicate rationale and support to affected employees.
        9. Maintain records of notice and communications.
        10. Review compliance post-layoff.
        """,
        key_factors=[
            "Layoff thresholds",
            "Notice period",
            "Exceptions",
            "Documentation",
            "State laws"
        ],
        primary_authority=[
            "Worker Adjustment and Retraining Notification (WARN) Act",
            "Department of Labor Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Employees allege insufficient notice or non-compliance.",
        counter_arguments=[
            "Layoff does not meet threshold.",
            "Exception applies.",
            "Notice delivered as required."
        ],
        resolution_strategy="Apply WARN Act thresholds, deliver timely notice, and document compliance.",
        entity_scope="Employers with large layoffs or plant closings",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="WARN Act Enforcement Cases"
    ),
    DoctrineBlock(
        topic="flight_risk_assessment",
        keywords=["flight risk", "retention", "predictive analytics", "turnover", "talent management"],
        conclusion_template="Flight risk assessment identifies {employees} at risk and recommends {actions}.",
        reasoning_framework="""
        1. Collect data on employee tenure, performance, engagement, and compensation.
        2. Apply predictive analytics to identify high-risk employees.
        3. Segment risk by department, role, and demographics.
        4. Analyze root causes: compensation, engagement, career opportunities.
        5. Develop targeted retention strategies for high-risk groups.
        6. Monitor impact of interventions and adjust as needed.
        7. Communicate findings to leadership and managers.
        8. Integrate flight risk assessment into workforce planning.
        9. Review assessment quarterly for accuracy.
        10. Address privacy and ethical considerations in data use.
        """,
        key_factors=[
            "Predictive analytics",
            "Employee data",
            "Root causes",
            "Retention strategies",
            "Privacy"
        ],
        primary_authority=[
            "SHRM Retention Analytics",
            "Harvard Business Review Flight Risk Research"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge data use or retention strategies.",
        counter_arguments=[
            "Predictive model lacks accuracy.",
            "Retention strategies ineffective.",
            "Privacy concerns."
        ],
        resolution_strategy="Apply robust analytics, tailor retention strategies, and address privacy issues.",
        entity_scope="Employers using flight risk analytics",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="SHRM Flight Risk Assessment Standards"
    ),
    DoctrineBlock(
        topic="organizational_design_principles",
        keywords=["organizational design", "structure", "hierarchy", "span of control", "alignment"],
        conclusion_template="Organizational design aligns with {strategy} and {principles}.",
        reasoning_framework="""
        1. Assess current organizational structure and alignment with business strategy.
        2. Evaluate span of control, reporting relationships, and role clarity.
        3. Identify inefficiencies or redundancies.
        4. Develop design principles: agility, scalability, collaboration.
        5. Document proposed changes and rationale.
        6. Communicate design changes to stakeholders.
        7. Implement changes and monitor impact.
        8. Review alignment with strategy and adjust as needed.
        9. Address resistance and change management challenges.
        10. Integrate design principles into ongoing organizational development.
        """,
        key_factors=[
            "Business strategy",
            "Structure",
            "Span of control",
            "Role clarity",
            "Change management"
        ],
        primary_authority=[
            "Harvard Business Review Organizational Design",
            "SHRM Organizational Structure Standards"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge design changes or alignment.",
        counter_arguments=[
            "Design lacks alignment with strategy.",
            "Change management insufficient.",
            "Role clarity not achieved."
        ],
        resolution_strategy="Apply design principles, communicate changes, and monitor alignment.",
        entity_scope="Employers undergoing organizational redesign",
        confidence=0.86,
        confidence_zone="Medium",
        controlling_precedent="HBR Organizational Design Research"
    ),
    DoctrineBlock(
        topic="learning_and_development_roi",
        keywords=["learning", "development", "ROI", "training effectiveness", "skills"],
        conclusion_template="Learning and development ROI is {value} based on {metrics}.",
        reasoning_framework="""
        1. Define learning objectives and outcomes.
        2. Collect data on training participation, completion, and post-training performance.
        3. Apply ROI calculation: (benefits - costs) / costs.
        4. Analyze impact on productivity, retention, and skill development.
        5. Segment results by department and role.
        6. Document findings and share with leadership.
        7. Adjust learning programs based on ROI analysis.
        8. Monitor ongoing effectiveness and update metrics.
        9. Integrate learning ROI into talent management strategy.
        10. Review ROI annually for continuous improvement.
        """,
        key_factors=[
            "Learning objectives",
            "Participation data",
            "ROI calculation",
            "Productivity impact",
            "Talent management"
        ],
        primary_authority=[
            "Kirkpatrick Model",
            "SHRM Learning ROI Standards"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge training effectiveness or ROI calculation.",
        counter_arguments=[
            "ROI calculation lacks accuracy.",
            "Training not aligned with business needs.",
            "Data incomplete."
        ],
        resolution_strategy="Apply validated ROI models, collect robust data, and adjust programs.",
        entity_scope="Employers investing in learning and development",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Kirkpatrick Model Research"
    ),
    DoctrineBlock(
        topic="dei_strategy_and_metrics",
        keywords=["DEI", "diversity", "equity", "inclusion", "metrics", "strategy"],
        conclusion_template="DEI strategy achieves {level} of progress based on {metrics}.",
        reasoning_framework="""
        1. Define DEI goals and objectives aligned with organizational values.
        2. Collect demographic and engagement data.
        3. Develop DEI metrics: representation, pay equity, promotion rates, engagement scores.
        4. Analyze progress against goals and benchmarks.
        5. Document findings and share with stakeholders.
        6. Implement targeted initiatives to address gaps.
        7. Monitor impact of initiatives and adjust as needed.
        8. Communicate progress transparently.
        9. Integrate DEI metrics into talent management and compensation.
        10. Review strategy annually for continuous improvement.
        """,
        key_factors=[
            "DEI goals",
            "Demographic data",
            "Metrics",
            "Initiatives",
            "Transparency"
        ],
        primary_authority=[
            "EEOC Diversity Guidance",
            "SHRM DEI Standards"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge DEI progress or metric validity.",
        counter_arguments=[
            "Metrics lack accuracy.",
            "Initiatives not effective.",
            "Transparency insufficient."
        ],
        resolution_strategy="Develop robust metrics, implement targeted initiatives, and communicate progress.",
        entity_scope="Employers implementing DEI strategies",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="EEOC Diversity Guidance"
    ),
    DoctrineBlock(
        topic="hr_technology_selection",
        keywords=["HR technology", "selection", "systems", "vendor evaluation", "implementation"],
        conclusion_template="HR technology selection aligns with {needs} and {criteria}.",
        reasoning_framework="""
        1. Define HR technology needs and requirements.
        2. Evaluate vendors based on functionality, scalability, integration, and cost.
        3. Conduct demos and proof of concept.
        4. Assess user experience and adoption potential.
        5. Review data security and compliance features.
        6. Document selection criteria and rationale.
        7. Negotiate contract terms and implementation timeline.
        8. Communicate selection to stakeholders.
        9. Monitor implementation and user adoption.
        10. Review technology effectiveness post-implementation.
        """,
        key_factors=[
            "Needs assessment",
            "Vendor evaluation",
            "Integration",
            "Security",
            "Adoption"
        ],
        primary_authority=[
            "SHRM HR Technology Standards",
            "Gartner HR Tech Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge technology selection or implementation.",
        counter_arguments=[
            "Needs not accurately defined.",
            "Vendor lacks required features.",
            "User adoption insufficient."
        ],
        resolution_strategy="Apply structured selection process, document decisions, and monitor implementation.",
        entity_scope="Employers selecting HR technology",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Gartner HR Tech Selection Research"
    ),
    DoctrineBlock(
        topic="employee_relations_investigation",
        keywords=["employee relations", "investigation", "discipline", "complaint", "HR process"],
        conclusion_template="Employee relations investigation finds {outcome} and recommends {actions}.",
        reasoning_framework="""
        1. Receive and document employee complaint or issue.
        2. Define scope and objectives of investigation.
        3. Collect evidence: interviews, documents, emails.
        4. Maintain confidentiality and impartiality.
        5. Analyze evidence and determine findings.
        6. Document investigation process and outcomes.
        7. Communicate findings to relevant parties.
        8. Implement corrective actions as needed.
        9. Monitor for retaliation or recurrence.
        10. Review investigation process for improvements.
        """,
        key_factors=[
            "Complaint documentation",
            "Evidence collection",
            "Confidentiality",
            "Impartiality",
            "Corrective actions"
        ],
        primary_authority=[
            "SHRM Employee Relations Standards",
            "EEOC Investigation Guidelines"
        ],
        burden_holder="Employer",
        adversary_position="Employee challenges investigation fairness or outcome.",
        counter_arguments=[
            "Investigation lacks impartiality.",
            "Evidence insufficient.",
            "Corrective actions not implemented."
        ],
        resolution_strategy="Apply structured investigation process, document findings, and ensure corrective actions.",
        entity_scope="Employers conducting employee relations investigations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EEOC Investigation Guidelines"
    ),
    DoctrineBlock(
        topic="total_rewards_strategy",
        keywords=["total rewards", "compensation", "benefits", "recognition", "strategy"],
        conclusion_template="Total rewards strategy delivers {value} and aligns with {objectives}.",
        reasoning_framework="""
        1. Define total rewards philosophy and objectives.
        2. Assess current compensation, benefits, and recognition programs.
        3. Benchmark against industry standards and peer organizations.
        4. Develop integrated rewards strategy: pay, benefits, recognition, development.
        5. Document strategy and communicate to employees.
        6. Monitor impact on attraction, retention, and engagement.
        7. Adjust strategy based on feedback and market trends.
        8. Ensure compliance with legal and regulatory requirements.
        9. Integrate total rewards into talent management.
        10. Review strategy annually for continuous improvement.
        """,
        key_factors=[
            "Philosophy",
            "Benchmarking",
            "Integration",
            "Communication",
            "Compliance"
        ],
        primary_authority=[
            "WorldatWork Total Rewards Standards",
            "SHRM Total Rewards Toolkit"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge rewards value or alignment.",
        counter_arguments=[
            "Strategy lacks integration.",
            "Benchmarking outdated.",
            "Communication insufficient."
        ],
        resolution_strategy="Develop integrated strategy, benchmark regularly, and communicate effectively.",
        entity_scope="Employers implementing total rewards",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="WorldatWork Total Rewards Standards"
    ),
    DoctrineBlock(
        topic="workforce_planning_methodology",
        keywords=["workforce planning", "methodology", "forecasting", "talent gaps", "strategy"],
        conclusion_template="Workforce planning identifies {gaps} and recommends {actions}.",
        reasoning_framework="""
        1. Define business objectives and talent requirements.
        2. Collect data on current workforce: skills, demographics, turnover.
        3. Forecast future talent needs based on business growth and trends.
        4. Identify talent gaps and risks.
        5. Develop action plans: hiring, development, retention.
        6. Document methodology and rationale.
        7. Communicate plans to leadership and stakeholders.
        8. Monitor progress and adjust as needed.
        9. Integrate planning into HR and business strategy.
        10. Review methodology annually for improvements.
        """,
        key_factors=[
            "Business objectives",
            "Workforce data",
            "Forecasting",
            "Talent gaps",
            "Action plans"
        ],
        primary_authority=[
            "SHRM Workforce Planning Toolkit",
            "Harvard Business Review Workforce Planning Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge planning accuracy or methodology.",
        counter_arguments=[
            "Forecasting lacks accuracy.",
            "Talent gaps not addressed.",
            "Methodology not documented."
        ],
        resolution_strategy="Apply structured methodology, document plans, and monitor progress.",
        entity_scope="Employers conducting workforce planning",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Workforce Planning Standards"
    ),
    DoctrineBlock(
        topic="employee_handbook_essentials",
        keywords=["employee handbook", "policy", "compliance", "communication", "HR"],
        conclusion_template="Employee handbook includes {policies} and meets {compliance} requirements.",
        reasoning_framework="""
        1. Identify essential policies: code of conduct, anti-discrimination, leave, benefits, safety.
        2. Review legal and regulatory requirements for handbook content.
        3. Draft clear and accessible policies.
        4. Communicate handbook to employees and obtain acknowledgment.
        5. Update handbook annually or upon regulatory changes.
        6. Document distribution and acknowledgments.
        7. Monitor compliance with handbook policies.
        8. Address employee questions and feedback.
        9. Integrate handbook into onboarding and training.
        10. Review handbook effectiveness periodically.
        """,
        key_factors=[
            "Essential policies",
            "Legal requirements",
            "Communication",
            "Acknowledgment",
            "Updates"
        ],
        primary_authority=[
            "SHRM Employee Handbook Standards",
            "EEOC Policy Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge policy clarity or compliance.",
        counter_arguments=[
            "Handbook lacks essential policies.",
            "Compliance requirements not met.",
            "Communication insufficient."
        ],
        resolution_strategy="Include essential policies, update regularly, and communicate effectively.",
        entity_scope="Employers distributing handbooks",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SHRM Employee Handbook Standards"
    ),
    DoctrineBlock(
        topic="hr_analytics_maturity",
        keywords=["HR analytics", "maturity", "data", "metrics", "decision-making"],
        conclusion_template="HR analytics maturity is {level} based on {criteria}.",
        reasoning_framework="""
        1. Assess current HR analytics capabilities: data collection, reporting, predictive analytics.
        2. Define maturity levels: descriptive, diagnostic, predictive, prescriptive.
        3. Evaluate data quality, integration, and accessibility.
        4. Analyze impact of analytics on HR decision-making.
        5. Document maturity assessment and share with leadership.
        6. Develop roadmap for analytics advancement.
        7. Monitor progress and adjust roadmap as needed.
        8. Integrate analytics into HR strategy and processes.
        9. Review maturity annually for improvements.
        10. Address data privacy and security risks.
        """,
        key_factors=[
            "Analytics capabilities",
            "Data quality",
            "Integration",
            "Impact",
            "Roadmap"
        ],
        primary_authority=[
            "SHRM HR Analytics Standards",
            "Harvard Business Review Analytics Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge analytics maturity or impact.",
        counter_arguments=[
            "Data quality insufficient.",
            "Analytics not integrated.",
            "Impact not demonstrated."
        ],
        resolution_strategy="Assess maturity, develop roadmap, and integrate analytics.",
        entity_scope="Employers advancing HR analytics",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM HR Analytics Standards"
    ),
    DoctrineBlock(
        topic="shrm_competency_model",
        keywords=["SHRM", "competency model", "HR competencies", "professional development"],
        conclusion_template="SHRM competency model identifies {competencies} for HR professionals.",
        reasoning_framework="""
        1. Review SHRM competency model: leadership, ethical practice, business acumen, relationship management.
        2. Assess current HR staff against competency requirements.
        3. Develop professional development plans to address gaps.
        4. Document competency assessment and development plans.
        5. Communicate competency expectations to HR staff.
        6. Monitor progress and adjust plans as needed.
        7. Integrate competency model into performance management.
        8. Review competency model annually for updates.
        9. Address certification and credentialing requirements.
        10. Align competency model with organizational HR strategy.
        """,
        key_factors=[
            "Competency model",
            "Assessment",
            "Development plans",
            "Communication",
            "Certification"
        ],
        primary_authority=[
            "SHRM Competency Model",
            "SHRM Certification Standards"
        ],
        burden_holder="Employer",
        adversary_position="HR staff challenge competency expectations or development plans.",
        counter_arguments=[
            "Competency model not aligned.",
            "Development plans not implemented.",
            "Certification requirements unclear."
        ],
        resolution_strategy="Apply SHRM model, assess staff, and develop plans.",
        entity_scope="Employers using SHRM competency model",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SHRM Competency Model"
    ),
    DoctrineBlock(
        topic="workers_compensation_management",
        keywords=["workers compensation", "management", "claims", "safety", "compliance"],
        conclusion_template="Workers compensation management achieves {outcome} and meets {compliance} standards.",
        reasoning_framework="""
        1. Review workers compensation insurance coverage and requirements.
        2. Document and report workplace injuries promptly.
        3. Manage claims process: investigation, communication, medical care.
        4. Implement safety and prevention programs.
        5. Monitor claims data for trends and risks.
        6. Communicate process and support to employees.
        7. Ensure compliance with state and federal regulations.
        8. Address fraud and abuse risks.
        9. Review claims management process annually.
        10. Integrate workers compensation into safety strategy.
        """,
        key_factors=[
            "Insurance coverage",
            "Claims management",
            "Safety programs",
            "Compliance",
            "Fraud prevention"
        ],
        primary_authority=[
            "State Workers Compensation Laws",
            "OSHA Standards"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge claims management or safety.",
        counter_arguments=[
            "Claims process lacks transparency.",
            "Safety programs insufficient.",
            "Compliance risks."
        ],
        resolution_strategy="Manage claims effectively, implement safety programs, and ensure compliance.",
        entity_scope="Employers managing workers compensation",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="State Workers Compensation Precedents"
    ),
    DoctrineBlock(
        topic="remote_hybrid_work_policy",
        keywords=["remote work", "hybrid work", "policy", "flexibility", "compliance"],
        conclusion_template="Remote/hybrid work policy delivers {flexibility} and meets {compliance} requirements.",
        reasoning_framework="""
        1. Define remote and hybrid work policy objectives.
        2. Assess eligibility criteria and job suitability.
        3. Document policy: expectations, communication, technology, security.
        4. Ensure compliance with wage and hour, safety, and privacy laws.
        5. Communicate policy to employees and managers.
        6. Monitor impact on productivity, engagement, and retention.
        7. Address challenges: isolation, collaboration, performance management.
        8. Review policy effectiveness annually.
        9. Adjust policy based on feedback and business needs.
        10. Integrate remote/hybrid work into talent strategy.
        """,
        key_factors=[
            "Policy objectives",
            "Eligibility",
            "Compliance",
            "Communication",
            "Productivity"
        ],
        primary_authority=[
            "SHRM Remote Work Standards",
            "Department of Labor Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge policy fairness or compliance.",
        counter_arguments=[
            "Eligibility criteria unclear.",
            "Compliance risks.",
            "Policy lacks flexibility."
        ],
        resolution_strategy="Document policy, communicate clearly, and monitor effectiveness.",
        entity_scope="Employers implementing remote/hybrid work",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Remote Work Standards"
    ),
    DoctrineBlock(
        topic="okr_kpi_framework",
        keywords=["OKR", "KPI", "framework", "goal setting", "performance measurement"],
        conclusion_template="OKR/KPI framework aligns goals with {strategy} and measures {performance}.",
        reasoning_framework="""
        1. Define organizational strategy and objectives.
        2. Develop OKRs (Objectives and Key Results) and KPIs (Key Performance Indicators).
        3. Align OKRs/KPIs with department and individual goals.
        4. Document framework and communicate to employees.
        5. Monitor progress and adjust goals as needed.
        6. Integrate OKR/KPI framework into performance management.
        7. Review framework effectiveness quarterly.
        8. Address challenges: goal clarity, measurement, alignment.
        9. Provide training on OKR/KPI methodology.
        10. Update framework based on feedback and business needs.
        """,
        key_factors=[
            "Strategy alignment",
            "Goal clarity",
            "Measurement",
            "Communication",
            "Training"
        ],
        primary_authority=[
            "SHRM Goal Setting Standards",
            "Harvard Business Review OKR Research"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge goal clarity or measurement.",
        counter_arguments=[
            "Goals not aligned.",
            "Measurement lacks accuracy.",
            "Communication insufficient."
        ],
        resolution_strategy="Develop clear framework, communicate goals, and monitor progress.",
        entity_scope="Employers using OKR/KPI frameworks",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="HBR OKR/KPI Research"
    ),
    DoctrineBlock(
        topic="i9_employment_verification",
        keywords=["I-9", "employment verification", "compliance", "documentation", "immigration"],
        conclusion_template="I-9 employment verification is {complete/incomplete} and meets {compliance} standards.",
        reasoning_framework="""
        1. Collect required I-9 documentation from new hires.
        2. Review documents for authenticity and completeness.
        3. Complete I-9 form within three business days of hire.
        4. Maintain I-9 records for required retention period.
        5. Monitor for compliance with E-Verify and immigration laws.
        6. Address errors or omissions promptly.
        7. Train HR staff on I-9 requirements.
        8. Conduct periodic audits for compliance.
        9. Communicate verification process to new hires.
        10. Review process annually for improvements.
        """,
        key_factors=[
            "Documentation",
            "Timeliness",
            "Authenticity",
            "Record retention",
            "Compliance"
        ],
        primary_authority=[
            "Immigration Reform and Control Act (IRCA)",
            "Department of Homeland Security Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Regulators challenge verification process or compliance.",
        counter_arguments=[
            "Documentation incomplete.",
            "Timeliness not met.",
            "Compliance risks."
        ],
        resolution_strategy="Collect documentation promptly, train staff, and audit regularly.",
        entity_scope="Employers hiring new employees",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IRCA Employment Verification Standards"
    ),
    DoctrineBlock(
        topic="progressive_discipline_framework",
        keywords=["progressive discipline", "framework", "policy", "performance", "compliance"],
        conclusion_template="Progressive discipline framework applies {steps} and achieves {outcome}.",
        reasoning_framework="""
        1. Define progressive discipline policy: verbal warning, written warning, suspension, termination.
        2. Document performance or conduct issues.
        3. Apply discipline steps consistently and fairly.
        4. Communicate expectations and consequences to employee.
        5. Maintain records of discipline actions.
        6. Monitor for improvement or recurrence.
        7. Address retaliation risks and ensure confidentiality.
        8. Review framework effectiveness annually.
        9. Adjust policy based on feedback and legal requirements.
        10. Integrate discipline framework into performance management.
        """,
        key_factors=[
            "Policy definition",
            "Documentation",
            "Consistency",
            "Communication",
            "Record keeping"
        ],
        primary_authority=[
            "SHRM Discipline Standards",
            "EEOC Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge discipline fairness or consistency.",
        counter_arguments=[
            "Policy not applied consistently.",
            "Documentation insufficient.",
            "Retaliation risks."
        ],
        resolution_strategy="Apply policy consistently, document actions, and monitor effectiveness.",
        entity_scope="Employers implementing discipline frameworks",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SHRM Discipline Standards"
    ),
    DoctrineBlock(
        topic="talent_acquisition_strategy",
        keywords=["talent acquisition", "strategy", "recruiting", "employer branding", "pipeline"],
        conclusion_template="Talent acquisition strategy achieves {outcome} and aligns with {objectives}.",
        reasoning_framework="""
        1. Define talent acquisition objectives and employer value proposition.
        2. Develop sourcing and recruiting channels.
        3. Implement employer branding initiatives.
        4. Monitor pipeline metrics: time to fill, quality of hire, diversity.
        5. Document strategy and communicate to stakeholders.
        6. Adjust strategy based on feedback and market trends.
        7. Integrate talent acquisition into workforce planning.
        8. Review strategy effectiveness quarterly.
        9. Provide recruiter training and development.
        10. Update strategy annually for continuous improvement.
        """,
        key_factors=[
            "Objectives",
            "Branding",
            "Pipeline metrics",
            "Communication",
            "Training"
        ],
        primary_authority=[
            "SHRM Talent Acquisition Standards",
            "LinkedIn Talent Solutions"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge strategy effectiveness or alignment.",
        counter_arguments=[
            "Objectives not defined.",
            "Branding ineffective.",
            "Pipeline metrics not monitored."
        ],
        resolution_strategy="Develop clear strategy, monitor metrics, and adjust as needed.",
        entity_scope="Employers acquiring talent",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Talent Acquisition Standards"
    ),
    DoctrineBlock(
        topic="employee_wellness_programs",
        keywords=["employee wellness", "programs", "health", "engagement", "ROI"],
        conclusion_template="Employee wellness program achieves {outcome} and delivers {ROI}.",
        reasoning_framework="""
        1. Define wellness program objectives and offerings.
        2. Assess employee health needs and preferences.
        3. Implement wellness initiatives: fitness, nutrition, mental health, preventive care.
        4. Monitor participation rates and engagement.
        5. Analyze impact on health outcomes, productivity, and ROI.
        6. Document program and communicate to employees.
        7. Adjust offerings based on feedback and utilization.
        8. Ensure compliance with privacy and nondiscrimination laws.
        9. Review program effectiveness annually.
        10. Integrate wellness into benefits and talent strategy.
        """,
        key_factors=[
            "Objectives",
            "Offerings",
            "Participation",
            "Health outcomes",
            "Compliance"
        ],
        primary_authority=[
            "SHRM Wellness Standards",
            "CDC Workplace Health Promotion"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge program value or privacy.",
        counter_arguments=[
            "Participation low.",
            "Health outcomes not achieved.",
            "Privacy concerns."
        ],
        resolution_strategy="Develop targeted offerings, monitor outcomes, and ensure compliance.",
        entity_scope="Employers offering wellness programs",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="CDC Workplace Health Promotion"
    ),
    DoctrineBlock(
        topic="hr_policy_audit",
        keywords=["HR policy", "audit", "compliance", "risk", "review"],
        conclusion_template="HR policy audit finds {compliance/gaps} and recommends {actions}.",
        reasoning_framework="""
        1. Identify HR policies subject to audit: leave, discrimination, compensation, safety.
        2. Review policies for legal and regulatory compliance.
        3. Document audit findings and gaps.
        4. Develop remediation plan for identified risks.
        5. Communicate audit outcomes to leadership.
        6. Monitor implementation of remediation actions.
        7. Review audit process annually.
        8. Integrate audit findings into policy updates.
        9. Address stakeholder concerns and feedback.
        10. Ensure audit documentation and record keeping.
        """,
        key_factors=[
            "Policy identification",
            "Compliance review",
            "Documentation",
            "Remediation",
            "Communication"
        ],
        primary_authority=[
            "SHRM Policy Audit Standards",
            "EEOC Compliance Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Regulators or stakeholders challenge audit findings.",
        counter_arguments=[
            "Audit lacks thoroughness.",
            "Remediation not implemented.",
            "Documentation insufficient."
        ],
        resolution_strategy="Conduct thorough audit, document findings, and implement remediation.",
        entity_scope="Employers conducting HR policy audits",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Policy Audit Standards"
    ),
    DoctrineBlock(
        topic="leadership_development_programs",
        keywords=["leadership development", "programs", "succession", "training", "ROI"],
        conclusion_template="Leadership development program delivers {outcome} and supports {succession}.",
        reasoning_framework="""
        1. Define leadership competencies and development objectives.
        2. Assess current leadership pipeline and gaps.
        3. Implement development programs: training, coaching, mentoring.
        4. Monitor participation and progress.
        5. Analyze impact on succession and organizational performance.
        6. Document program and communicate to stakeholders.
        7. Adjust offerings based on feedback and outcomes.
        8. Integrate leadership development into talent strategy.
        9. Review program effectiveness annually.
        10. Address diversity and inclusion in leadership development.
        """,
        key_factors=[
            "Competencies",
            "Pipeline",
            "Training",
            "Succession",
            "Diversity"
        ],
        primary_authority=[
            "SHRM Leadership Development Standards",
            "Harvard Business Review Leadership Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge program effectiveness or diversity.",
        counter_arguments=[
            "Competencies not defined.",
            "Pipeline gaps not addressed.",
            "Diversity insufficient."
        ],
        resolution_strategy="Define competencies, monitor pipeline, and address diversity.",
        entity_scope="Employers developing leadership",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Leadership Development Standards"
    ),
    DoctrineBlock(
        topic="hr_compliance_training",
        keywords=["HR compliance", "training", "regulations", "risk", "education"],
        conclusion_template="HR compliance training achieves {outcome} and reduces {risk}.",
        reasoning_framework="""
        1. Identify regulatory requirements for HR compliance training.
        2. Develop training curriculum: discrimination, harassment, wage and hour, safety.
        3. Deliver training to employees and managers.
        4. Document training participation and completion.
        5. Monitor impact on compliance and risk reduction.
        6. Update training annually or upon regulatory changes.
        7. Communicate training outcomes to leadership.
        8. Address challenges: engagement, retention, effectiveness.
        9. Integrate compliance training into onboarding.
        10. Review training effectiveness periodically.
        """,
        key_factors=[
            "Regulatory requirements",
            "Curriculum",
            "Documentation",
            "Risk reduction",
            "Updates"
        ],
        primary_authority=[
            "SHRM Compliance Training Standards",
            "EEOC Training Guidance"
        ],
        burden_holder="Employer",
        adversary_position="Regulators or employees challenge training effectiveness.",
        counter_arguments=[
            "Training not delivered.",
            "Documentation insufficient.",
            "Risk not reduced."
        ],
        resolution_strategy="Develop robust curriculum, document participation, and monitor effectiveness.",
        entity_scope="Employers delivering compliance training",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SHRM Compliance Training Standards"
    ),
    DoctrineBlock(
        topic="hr_shared_services_model",
        keywords=["HR shared services", "model", "centralization", "efficiency", "service delivery"],
        conclusion_template="HR shared services model achieves {efficiency} and improves {service delivery}.",
        reasoning_framework="""
        1. Define objectives for HR shared services: efficiency, cost reduction, service quality.
        2. Assess current HR processes and structure.
        3. Develop shared services model: centralization, technology, process standardization.
        4. Document model and communicate to stakeholders.
        5. Monitor impact on efficiency and service delivery.
        6. Adjust model based on feedback and outcomes.
        7. Integrate shared services into HR strategy.
        8. Review model effectiveness annually.
        9. Address challenges: change management, technology adoption.
        10. Ensure compliance with service standards and regulations.
        """,
        key_factors=[
            "Objectives",
            "Process assessment",
            "Centralization",
            "Technology",
            "Service quality"
        ],
        primary_authority=[
            "SHRM Shared Services Standards",
            "Harvard Business Review Shared Services Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge efficiency or service quality.",
        counter_arguments=[
            "Objectives not achieved.",
            "Process standardization insufficient.",
            "Technology adoption challenges."
        ],
        resolution_strategy="Develop clear model, monitor outcomes, and address challenges.",
        entity_scope="Employers implementing shared services",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Shared Services Standards"
    ),
    DoctrineBlock(
        topic="employee_recognition_programs",
        keywords=["employee recognition", "programs", "engagement", "retention", "motivation"],
        conclusion_template="Employee recognition program delivers {outcome} and improves {engagement}.",
        reasoning_framework="""
        1. Define recognition program objectives and offerings.
        2. Assess employee preferences and motivation drivers.
        3. Implement recognition initiatives: awards, peer recognition, spot bonuses.
        4. Monitor participation and impact on engagement and retention.
        5. Document program and communicate to employees.
        6. Adjust offerings based on feedback and outcomes.
        7. Integrate recognition into performance management.
        8. Review program effectiveness annually.
        9. Address challenges: fairness, consistency, inclusivity.
        10. Ensure compliance with compensation and tax regulations.
        """,
        key_factors=[
            "Objectives",
            "Offerings",
            "Participation",
            "Engagement",
            "Compliance"
        ],
        primary_authority=[
            "SHRM Recognition Standards",
            "Harvard Business Review Recognition Research"
        ],
        burden_holder="Employer",
        adversary_position="Employees challenge program fairness or value.",
        counter_arguments=[
            "Offerings not valued.",
            "Participation low.",
            "Fairness concerns."
        ],
        resolution_strategy="Develop targeted offerings, monitor impact, and ensure fairness.",
        entity_scope="Employers offering recognition programs",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Recognition Standards"
    ),
    DoctrineBlock(
        topic="hr_data_privacy_and_security",
        keywords=["HR data", "privacy", "security", "compliance", "risk"],
        conclusion_template="HR data privacy and security measures achieve {compliance} and reduce {risk}.",
        reasoning_framework="""
        1. Identify HR data subject to privacy and security requirements.
        2. Assess compliance with GDPR, CCPA, and other regulations.
        3. Implement data security measures: encryption, access controls, audits.
        4. Document privacy policies and communicate to employees.
        5. Monitor for data breaches and risks.
        6. Review compliance annually or upon regulatory changes.
        7. Address employee concerns and feedback.
        8. Integrate privacy and security into HR technology.
        9. Train HR staff on data privacy requirements.
        10. Ensure record keeping and audit trails.
        """,
        key_factors=[
            "Data identification",
            "Compliance",
            "Security measures",
            "Communication",
            "Training"
        ],
        primary_authority=[
            "GDPR",
            "CCPA",
            "SHRM Data Privacy Standards"
        ],
        burden_holder="Employer",
        adversary_position="Regulators or employees challenge privacy or security.",
        counter_arguments=[
            "Compliance gaps.",
            "Security measures insufficient.",
            "Communication unclear."
        ],
        resolution_strategy="Implement robust security, document policies, and train staff.",
        entity_scope="Employers managing HR data",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="GDPR/CCPA Enforcement"
    ),
    DoctrineBlock(
        topic="hr_vendor_management",
        keywords=["HR vendor", "management", "contracts", "performance", "risk"],
        conclusion_template="HR vendor management achieves {performance} and reduces {risk}.",
        reasoning_framework="""
        1. Identify HR vendors and contract requirements.
        2. Assess vendor performance and compliance.
        3. Document vendor selection and management process.
        4. Monitor contract terms and service delivery.
        5. Address risks: data privacy, service quality, cost.
        6. Communicate vendor management process to stakeholders.
        7. Review vendor performance annually.
        8. Integrate vendor management into HR strategy.
        9. Adjust contracts based on feedback and outcomes.
        10. Ensure compliance with legal and regulatory requirements.
        """,
        key_factors=[
            "Vendor identification",
            "Performance",
            "Compliance",
            "Risk management",
            "Contract terms"
        ],
        primary_authority=[
            "SHRM Vendor Management Standards",
            "Harvard Business Review Vendor Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge vendor performance or risk.",
        counter_arguments=[
            "Performance insufficient.",
            "Compliance gaps.",
            "Risk not managed."
        ],
        resolution_strategy="Monitor performance, manage risks, and adjust contracts.",
        entity_scope="Employers managing HR vendors",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Vendor Management Standards"
    ),
    DoctrineBlock(
        topic="hr_budgeting_and_forecasting",
        keywords=["HR budgeting", "forecasting", "cost", "planning", "strategy"],
        conclusion_template="HR budgeting and forecasting achieves {accuracy} and supports {strategy}.",
        reasoning_framework="""
        1. Define HR budgeting objectives and requirements.
        2. Collect data on HR costs: compensation, benefits, training, technology.
        3. Develop forecasting models based on business growth and trends.
        4. Document budgeting and forecasting process.
        5. Monitor accuracy and adjust models as needed.
        6. Communicate process and outcomes to leadership.
        7. Integrate budgeting into HR and business strategy.
        8. Review process annually for improvements.
        9. Address challenges: cost control, alignment, accuracy.
        10. Ensure compliance with financial standards.
        """,
        key_factors=[
            "Objectives",
            "Data collection",
            "Forecasting models",
            "Accuracy",
            "Alignment"
        ],
        primary_authority=[
            "SHRM Budgeting Standards",
            "Harvard Business Review Budgeting Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge accuracy or alignment.",
        counter_arguments=[
            "Models lack accuracy.",
            "Alignment insufficient.",
            "Cost control challenges."
        ],
        resolution_strategy="Develop robust models, monitor accuracy, and align with strategy.",
        entity_scope="Employers budgeting HR costs",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Budgeting Standards"
    ),
    DoctrineBlock(
        topic="hr_change_management",
        keywords=["HR change management", "strategy", "communication", "adoption", "resistance"],
        conclusion_template="HR change management strategy achieves {adoption} and reduces {resistance}.",
        reasoning_framework="""
        1. Define change management objectives and scope.
        2. Assess stakeholder impact and readiness.
        3. Develop communication plan for change.
        4. Document change management process and rationale.
        5. Monitor adoption and resistance.
        6. Adjust strategy based on feedback and outcomes.
        7. Integrate change management into HR and business processes.
        8. Review effectiveness annually.
        9. Provide training and support for change.
        10. Address challenges: resistance, communication, alignment.
        """,
        key_factors=[
            "Objectives",
            "Stakeholder impact",
            "Communication",
            "Adoption",
            "Training"
        ],
        primary_authority=[
            "SHRM Change Management Standards",
            "Harvard Business Review Change Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge adoption or communication.",
        counter_arguments=[
            "Resistance high.",
            "Communication unclear.",
            "Alignment insufficient."
        ],
        resolution_strategy="Develop clear strategy, communicate effectively, and monitor adoption.",
        entity_scope="Employers managing HR change",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Change Management Standards"
    ),
    DoctrineBlock(
        topic="hr_culture_transformation",
        keywords=["HR culture", "transformation", "strategy", "engagement", "alignment"],
        conclusion_template="HR culture transformation achieves {alignment} and improves {engagement}.",
        reasoning_framework="""
        1. Define culture transformation objectives and desired outcomes.
        2. Assess current culture and gaps.
        3. Develop transformation strategy: values, behaviors, leadership.
        4. Document strategy and communicate to employees.
        5. Monitor impact on engagement and alignment.
        6. Adjust strategy based on feedback and outcomes.
        7. Integrate culture transformation into HR and business processes.
        8. Review effectiveness annually.
        9. Provide training and support for culture change.
        10. Address challenges: resistance, communication, sustainability.
        """,
        key_factors=[
            "Objectives",
            "Assessment",
            "Strategy",
            "Communication",
            "Sustainability"
        ],
        primary_authority=[
            "SHRM Culture Standards",
            "Harvard Business Review Culture Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge alignment or sustainability.",
        counter_arguments=[
            "Alignment insufficient.",
            "Sustainability not achieved.",
            "Communication unclear."
        ],
        resolution_strategy="Develop clear strategy, communicate effectively, and monitor alignment.",
        entity_scope="Employers transforming culture",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Culture Standards"
    ),
    DoctrineBlock(
        topic="hr_talent_retention_strategy",
        keywords=["HR talent retention", "strategy", "engagement", "compensation", "development"],
        conclusion_template="Talent retention strategy achieves {outcome} and reduces {turnover}.",
        reasoning_framework="""
        1. Define retention objectives and key drivers.
        2. Assess turnover data and root causes.
        3. Develop retention initiatives: compensation, development, engagement, recognition.
        4. Monitor impact on turnover and engagement.
        5. Document strategy and communicate to employees.
        6. Adjust initiatives based on feedback and outcomes.
        7. Integrate retention strategy into HR and business processes.
        8. Review effectiveness annually.
        9. Provide training and support for retention.
        10. Address challenges: compensation, development, engagement.
        """,
        key_factors=[
            "Objectives",
            "Turnover data",
            "Initiatives",
            "Engagement",
            "Compensation"
        ],
        primary_authority=[
            "SHRM Retention Standards",
            "Harvard Business Review Retention Research"
        ],
        burden_holder="Employer",
        adversary_position="Stakeholders challenge retention effectiveness or drivers.",
        counter_arguments=[
            "Initiatives not effective.",
            "Compensation insufficient.",
            "Engagement low."
        ],
        resolution_strategy="Develop targeted initiatives, monitor impact, and adjust as needed.",
        entity_scope="Employers retaining talent",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SHRM Retention Standards"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword.lower() in doctrine.topic.lower() or any(keyword.lower() in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]