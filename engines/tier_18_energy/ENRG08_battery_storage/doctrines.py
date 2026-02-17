from dataclasses import dataclass, field
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
        topic="LFP vs NMC Chemistry Selection for Grid-Scale BESS",
        keywords=["LFP", "NMC", "battery chemistry", "grid-scale", "BESS", "energy storage", "safety", "cost"],
        conclusion_template="For grid-scale BESS, LFP chemistry is generally preferred due to superior safety, longer cycle life, and lower cost, except where high energy density is a critical constraint.",
        reasoning_framework="""
        The selection between LFP (Lithium Iron Phosphate) and NMC (Nickel Manganese Cobalt) chemistries for grid-scale Battery Energy Storage Systems (BESS) involves evaluating trade-offs in safety, cost, cycle life, and energy density. LFP offers enhanced thermal stability, lower risk of thermal runaway, and a longer cycle life, making it favorable for stationary applications where safety and longevity are paramount. NMC provides higher energy density, which can be advantageous in space-constrained installations but introduces higher costs and greater safety risks. Recent market trends and regulatory guidance (e.g., NFPA 855) increasingly favor LFP for large-scale deployments. The decision should also consider supply chain stability, environmental impact, and total cost of ownership.
        """,
        key_factors=[
            "Thermal stability and safety profile",
            "Cycle life and degradation rates",
            "Energy density requirements",
            "Cost per kWh and total cost of ownership",
            "Regulatory compliance (NFPA 855, UL 9540A)",
            "Supply chain and material availability"
        ],
        primary_authority=[
            "NFPA 855",
            "UL 9540A",
            "DOE Energy Storage Handbook",
            "Sandia National Laboratories BESS Reports"
        ],
        burden_holder="System Integrator",
        adversary_position="NMC offers higher energy density and is more established in EV applications, thus should be preferred for BESS.",
        counter_arguments=[
            "Grid-scale BESS are not typically space-constrained.",
            "Safety and cycle life outweigh marginal energy density gains.",
            "LFP costs are lower and supply chains are more stable."
        ],
        resolution_strategy="Conduct a site-specific risk and cost assessment, referencing regulatory guidance and recent incident data.",
        entity_scope="Grid-scale BESS integrators and developers",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 855 Section 4.3.6; UL 9540A Test Reports"
    ),
    DoctrineBlock(
        topic="Battery Management System Cell Balancing Strategies",
        keywords=["BMS", "cell balancing", "active balancing", "passive balancing", "battery management", "BESS"],
        conclusion_template="Active cell balancing is recommended for large-scale BESS to maximize usable capacity and extend battery life, despite higher initial complexity and cost.",
        reasoning_framework="""
        Cell balancing in BMS is critical to prevent cell overcharge/overdischarge and to ensure uniform aging. Passive balancing dissipates excess charge as heat and is simple but inefficient for large systems. Active balancing redistributes charge between cells, improving overall efficiency and extending battery life. For grid-scale BESS, the benefits of active balancing—such as increased usable capacity and reduced degradation—typically outweigh the higher upfront cost and complexity. The choice must also consider maintenance requirements, system redundancy, and integration with monitoring platforms.
        """,
        key_factors=[
            "System size and cell count",
            "Efficiency requirements",
            "Maintenance and operational complexity",
            "Cost-benefit analysis over system lifetime",
            "Integration with monitoring and control systems"
        ],
        primary_authority=[
            "IEEE 1679.1",
            "DOE BMS Guidelines",
            "UL 1973"
        ],
        burden_holder="BESS System Designer",
        adversary_position="Passive balancing is sufficient and less costly for most stationary applications.",
        counter_arguments=[
            "Passive balancing leads to increased cell divergence over time.",
            "Active balancing reduces maintenance and extends system life.",
            "Efficiency losses in passive balancing are significant at scale."
        ],
        resolution_strategy="Perform a lifecycle cost analysis and pilot active balancing in a representative system.",
        entity_scope="BESS integrators and BMS vendors",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1679.1 Section 7.2"
    ),
    DoctrineBlock(
        topic="State of Charge Estimation Using Extended Kalman Filter",
        keywords=["SOC", "state of charge", "EKF", "battery modeling", "BMS", "estimation", "grid-scale BESS"],
        conclusion_template="Extended Kalman Filter (EKF) is the preferred algorithm for SOC estimation in grid-scale BESS due to its robustness to model and measurement uncertainties.",
        reasoning_framework="""
        Accurate SOC estimation is essential for safe and efficient BESS operation. The EKF algorithm provides a recursive solution that accounts for nonlinear battery behavior and measurement noise, outperforming simple Coulomb counting or voltage-based methods. EKF requires a validated battery model and careful tuning but offers superior accuracy, especially under dynamic load conditions. Implementation should include periodic recalibration and validation against empirical data. The approach must also consider computational requirements and integration with the BMS hardware platform.
        """,
        key_factors=[
            "Battery model accuracy",
            "Measurement noise and sensor quality",
            "Computational resources available",
            "Integration with BMS firmware",
            "Validation and recalibration procedures"
        ],
        primary_authority=[
            "IEEE 1679.1",
            "Sandia National Laboratories SOC Estimation Reports",
            "UL 1973"
        ],
        burden_holder="BMS Algorithm Engineer",
        adversary_position="Simpler SOC estimation methods are sufficient and easier to implement.",
        counter_arguments=[
            "Simple methods accumulate error over time.",
            "EKF provides better performance under variable loads.",
            "Regulatory standards increasingly require robust SOC estimation."
        ],
        resolution_strategy="Benchmark EKF against alternative methods in a controlled test environment.",
        entity_scope="BMS developers and integrators",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1679.1 Section 8.4"
    ),
    DoctrineBlock(
        topic="Grid-Scale BESS Sizing for 4-Hour Duration Standard",
        keywords=["BESS sizing", "4-hour duration", "grid-scale", "energy storage", "project development"],
        conclusion_template="Grid-scale BESS should be sized to deliver rated power for at least 4 hours to meet utility and market requirements in most North American jurisdictions.",
        reasoning_framework="""
        The 4-hour duration standard has become the de facto requirement for grid-scale BESS participating in capacity, resource adequacy, and energy arbitrage markets. This sizing ensures sufficient energy to support grid reliability and maximize revenue streams. Sizing must account for degradation, round-trip efficiency, and auxiliary loads. Developers should also consider site-specific requirements, such as local utility interconnection standards and project-specific revenue stacking opportunities.
        """,
        key_factors=[
            "Market participation requirements",
            "Expected degradation over system life",
            "Round-trip efficiency",
            "Auxiliary and HVAC loads",
            "Revenue stacking opportunities"
        ],
        primary_authority=[
            "FERC Order 841",
            "CAISO Resource Adequacy Standards",
            "NYISO Market Participation Guide"
        ],
        burden_holder="Project Developer",
        adversary_position="Shorter duration systems can be more cost-effective and still participate in some markets.",
        counter_arguments=[
            "Most capacity markets require 4-hour duration.",
            "Shorter duration limits revenue opportunities.",
            "Degradation can reduce effective duration below 4 hours."
        ],
        resolution_strategy="Conduct market analysis and consult with interconnection authorities.",
        entity_scope="Utility-scale BESS developers",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 841; CAISO BPM for Resource Adequacy"
    ),
    DoctrineBlock(
        topic="SEI Layer Growth and Capacity Fade Mechanisms",
        keywords=["SEI", "solid electrolyte interphase", "capacity fade", "degradation", "battery aging", "BESS"],
        conclusion_template="SEI layer growth is the primary driver of capacity fade in lithium-ion BESS; mitigation requires optimized charging protocols and thermal management.",
        reasoning_framework="""
        The SEI (Solid Electrolyte Interphase) layer forms on the anode during initial battery cycling and continues to grow over time, consuming lithium and reducing available capacity. Growth is accelerated by high temperatures, high SOC, and aggressive cycling. Effective mitigation involves optimizing charge/discharge protocols, maintaining moderate temperatures, and avoiding prolonged high-SOC storage. Monitoring SEI growth via impedance spectroscopy and periodic capacity tests is recommended for predictive maintenance.
        """,
        key_factors=[
            "Operating temperature",
            "SOC window and cycling profile",
            "Charging/discharging rates",
            "Battery chemistry and additives",
            "Monitoring and diagnostic tools"
        ],
        primary_authority=[
            "DOE Battery Degradation Study",
            "Journal of Power Sources (Volume 273, 2015)",
            "UL 1973"
        ],
        burden_holder="O&M Provider",
        adversary_position="Capacity fade is inevitable and cannot be meaningfully mitigated in grid-scale BESS.",
        counter_arguments=[
            "Optimized protocols can reduce fade rates by 30-50%.",
            "Thermal management is effective in slowing SEI growth.",
            "Predictive maintenance extends usable life."
        ],
        resolution_strategy="Implement adaptive BMS algorithms and periodic diagnostic testing.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Battery Degradation Study (2018)"
    ),
    DoctrineBlock(
        topic="Thermal Runaway Propagation and NFPA 855 Compliance",
        keywords=["thermal runaway", "NFPA 855", "fire safety", "propagation", "BESS", "compliance"],
        conclusion_template="NFPA 855 mandates robust thermal runaway mitigation strategies, including compartmentalization, fire suppression, and UL 9540A testing for all grid-scale BESS installations.",
        reasoning_framework="""
        Thermal runaway in lithium-ion BESS can lead to catastrophic fires and propagation to adjacent cells or modules. NFPA 855 establishes requirements for fire detection, suppression, and system compartmentalization to limit propagation. Compliance requires passing UL 9540A testing, which evaluates the effectiveness of mitigation measures. Strategies include thermal barriers, active cooling, gas detection, and emergency ventilation. Site-specific risk assessments and coordination with local AHJs are essential for permitting.
        """,
        key_factors=[
            "Thermal runaway initiation and propagation risk",
            "Fire detection and suppression systems",
            "Compartmentalization and spacing",
            "UL 9540A test results",
            "Coordination with AHJ and permitting"
        ],
        primary_authority=[
            "NFPA 855",
            "UL 9540A",
            "International Fire Code (IFC) 2021"
        ],
        burden_holder="System Integrator",
        adversary_position="Thermal runaway is rare and does not justify extensive mitigation measures.",
        counter_arguments=[
            "Recent incidents demonstrate propagation risk.",
            "NFPA 855 and UL 9540A are mandatory in most jurisdictions.",
            "Insurance and permitting require compliance."
        ],
        resolution_strategy="Design to exceed minimum code requirements and document all mitigation measures.",
        entity_scope="BESS integrators, developers, and AHJs",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 855 Section 4.3; UL 9540A Test Protocol"
    ),
    DoctrineBlock(
        topic="Levelized Cost of Storage (LCOS) Economic Analysis",
        keywords=["LCOS", "levelized cost", "economic analysis", "BESS", "project finance", "cost modeling"],
        conclusion_template="LCOS should be the primary metric for evaluating BESS project economics, incorporating all capital, operating, and degradation-related costs over the system lifetime.",
        reasoning_framework="""
        Levelized Cost of Storage (LCOS) provides a comprehensive measure of the cost per MWh delivered over the system's lifetime. It accounts for capital expenditure, O&M, degradation, augmentation, and end-of-life costs. LCOS enables comparison across technologies and project configurations. Accurate LCOS modeling requires realistic assumptions for degradation, augmentation cycles, and revenue streams. Sensitivity analysis is recommended to account for market volatility and regulatory changes.
        """,
        key_factors=[
            "Capital and installation costs",
            "O&M and augmentation costs",
            "Degradation and replacement schedules",
            "Revenue projections and market volatility",
            "Discount rate and project lifetime"
        ],
        primary_authority=[
            "DOE Energy Storage Cost and Performance Database",
            "NREL LCOS Methodology",
            "IEA Energy Storage Reports"
        ],
        burden_holder="Project Developer",
        adversary_position="Simple payback or IRR is sufficient for BESS project evaluation.",
        counter_arguments=[
            "LCOS provides a more accurate, apples-to-apples comparison.",
            "IRR and payback ignore degradation and replacement costs.",
            "LCOS is industry standard for utility-scale projects."
        ],
        resolution_strategy="Develop detailed LCOS models and validate with third-party benchmarks.",
        entity_scope="Project developers, financiers, and regulators",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL LCOS Methodology (2022)"
    ),
    DoctrineBlock(
        topic="Investment Tax Credit and Inflation Reduction Act Benefits",
        keywords=["ITC", "Inflation Reduction Act", "tax credit", "BESS", "project finance", "policy"],
        conclusion_template="Standalone BESS projects are eligible for the 30% ITC under the Inflation Reduction Act, significantly improving project economics.",
        reasoning_framework="""
        The Inflation Reduction Act (IRA) of 2022 extended the Investment Tax Credit (ITC) to standalone energy storage projects, including BESS. Eligible projects can claim a 30% tax credit on capital costs, with potential adders for domestic content and siting in energy communities. Compliance requires meeting prevailing wage and apprenticeship standards. The ITC substantially reduces project payback periods and increases IRR, making BESS more competitive in wholesale and retail markets.
        """,
        key_factors=[
            "Project eligibility and compliance",
            "Prevailing wage and apprenticeship requirements",
            "Domestic content and energy community adders",
            "Tax equity structuring",
            "Documentation and IRS filing"
        ],
        primary_authority=[
            "Inflation Reduction Act of 2022",
            "IRS Notice 2023-29",
            "DOE ITC Guidance"
        ],
        burden_holder="Project Developer",
        adversary_position="ITC benefits are uncertain and complex to claim for BESS.",
        counter_arguments=[
            "IRS has issued clear guidance for BESS eligibility.",
            "Most major developers have successfully claimed ITC.",
            "Tax equity market is well-established for storage."
        ],
        resolution_strategy="Engage tax counsel and structure projects to maximize ITC benefits.",
        entity_scope="BESS project developers and financiers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS Notice 2023-29"
    ),
    DoctrineBlock(
        topic="Frequency Regulation Service Revenue and Performance Requirements",
        keywords=["frequency regulation", "ancillary services", "BESS", "performance", "market participation"],
        conclusion_template="BESS can capture significant revenue from frequency regulation markets, provided they meet stringent response time and accuracy requirements.",
        reasoning_framework="""
        Frequency regulation is a key ancillary service in many electricity markets, requiring fast, accurate response to grid signals. BESS are well-suited due to rapid ramp rates and bidirectional power flow. Market participation requires compliance with response time (typically <1 second), accuracy, and telemetry requirements. Revenue potential depends on market size, participation rules, and system availability. Performance penalties apply for non-compliance, so robust controls and monitoring are essential.
        """,
        key_factors=[
            "Market rules and participation requirements",
            "Response time and accuracy",
            "Telemetry and data reporting",
            "System availability and reliability",
            "Performance penalties"
        ],
        primary_authority=[
            "FERC Order 755",
            "PJM Manual 12",
            "CAISO Ancillary Services BPM"
        ],
        burden_holder="BESS Operator",
        adversary_position="Frequency regulation markets are saturated and do not justify BESS investment.",
        counter_arguments=[
            "BESS offer unmatched response speed and flexibility.",
            "New markets are opening as renewables increase.",
            "Revenue stacking with other services is feasible."
        ],
        resolution_strategy="Model revenue potential and ensure system meets all technical requirements.",
        entity_scope="BESS operators and market participants",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 755"
    ),
    DoctrineBlock(
        topic="Cylindrical vs Prismatic vs Pouch Cell Format Selection",
        keywords=["cell format", "cylindrical", "prismatic", "pouch", "battery design", "BESS"],
        conclusion_template="Prismatic cells are generally preferred for grid-scale BESS due to higher packing efficiency and ease of thermal management, though cylindrical cells offer superior mechanical robustness.",
        reasoning_framework="""
        Cell format selection impacts packing density, thermal management, mechanical stability, and cost. Prismatic cells offer high volumetric efficiency and are easier to integrate into modular BESS enclosures. Cylindrical cells are robust and have well-understood failure modes but are less space-efficient. Pouch cells offer flexibility but are more susceptible to swelling and mechanical damage. The choice should balance energy density, safety, manufacturability, and total cost.
        """,
        key_factors=[
            "Packing density and volumetric efficiency",
            "Thermal management requirements",
            "Mechanical robustness",
            "Manufacturing scalability",
            "Cost per kWh"
        ],
        primary_authority=[
            "DOE Battery Design Handbook",
            "UL 1973",
            "Sandia National Laboratories BESS Reports"
        ],
        burden_holder="Cell Manufacturer",
        adversary_position="Cylindrical cells are more reliable and should be used exclusively.",
        counter_arguments=[
            "Prismatic cells are dominant in current BESS deployments.",
            "Thermal management is simpler with prismatic cells.",
            "Cylindrical cells increase system complexity at scale."
        ],
        resolution_strategy="Evaluate cell format in the context of specific project requirements and supply chain constraints.",
        entity_scope="BESS integrators and cell manufacturers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Battery Design Handbook Section 5.2"
    ),
    DoctrineBlock(
        topic="Grid-Forming vs Grid-Following Inverter Control Strategies",
        keywords=["inverter", "grid-forming", "grid-following", "control strategy", "BESS", "grid support"],
        conclusion_template="Grid-forming inverters are increasingly required for BESS to provide grid stability and support high renewable penetration, though grid-following remains common in legacy systems.",
        reasoning_framework="""
        Grid-forming inverters can establish voltage and frequency reference, enabling BESS to operate in weak or islanded grids and support black start. Grid-following inverters require an external grid reference and are less capable of providing stability services. As renewable penetration increases, grid-forming capabilities are being mandated by some ISOs and utilities. The transition requires advanced controls and coordination with grid operators.
        """,
        key_factors=[
            "Grid code requirements",
            "System stability and inertia support",
            "Black start capability",
            "Integration complexity",
            "Cost and vendor support"
        ],
        primary_authority=[
            "IEEE 1547-2018",
            "CAISO GFM Requirements",
            "NERC Inverter-Based Resource Guidelines"
        ],
        burden_holder="Inverter OEM",
        adversary_position="Grid-following inverters are sufficient for most BESS applications.",
        counter_arguments=[
            "Grid-forming is required for high-renewable grids.",
            "Provides additional revenue from stability services.",
            "Future-proofing against evolving grid codes."
        ],
        resolution_strategy="Adopt grid-forming controls where required and maintain flexibility for grid-following operation.",
        entity_scope="BESS integrators and inverter OEMs",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547-2018 Section 4.1"
    ),
    DoctrineBlock(
        topic="State of Health Estimation and Remaining Useful Life Prediction",
        keywords=["SOH", "state of health", "RUL", "battery aging", "prognostics", "BESS"],
        conclusion_template="Model-based SOH estimation combined with machine learning techniques provides the most accurate prediction of remaining useful life for grid-scale BESS.",
        reasoning_framework="""
        Accurate SOH and RUL prediction is essential for maintenance planning and financial modeling. Model-based approaches use physical and empirical battery models, while machine learning leverages operational data to identify degradation patterns. Combining both approaches improves accuracy and robustness. Implementation requires high-quality data, periodic calibration, and integration with asset management systems. Predictive SOH/RUL enables proactive maintenance and optimal augmentation scheduling.
        """,
        key_factors=[
            "Data quality and availability",
            "Model selection and calibration",
            "Integration with asset management",
            "Update frequency and validation",
            "Impact on O&M and financial planning"
        ],
        primary_authority=[
            "IEEE 1679.1",
            "Sandia National Laboratories Prognostics Reports",
            "NREL BESS SOH Guidelines"
        ],
        burden_holder="O&M Provider",
        adversary_position="Simple cycle counting is sufficient for SOH estimation.",
        counter_arguments=[
            "Cycle counting ignores calendar aging and operational variability.",
            "Model-based and ML methods are more accurate.",
            "Improved SOH/RUL reduces O&M costs."
        ],
        resolution_strategy="Implement hybrid SOH/RUL estimation and validate against field data.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1679.1 Section 9.3"
    ),
    DoctrineBlock(
        topic="HVAC Thermal Management System Design for Container-Based BESS",
        keywords=["HVAC", "thermal management", "container", "BESS", "cooling", "system design"],
        conclusion_template="Active HVAC systems are required for container-based BESS to maintain optimal temperature and prevent accelerated degradation or safety incidents.",
        reasoning_framework="""
        Container-based BESS are subject to significant thermal loads due to high energy density and limited passive dissipation. Active HVAC systems (cooling and, where necessary, heating) are essential to maintain cell temperatures within manufacturer-specified limits. Poor thermal management accelerates degradation, increases safety risks, and may void warranties. System design should include redundancy, real-time monitoring, and integration with BMS alarms. Energy consumption of HVAC must be included in LCOS calculations.
        """,
        key_factors=[
            "Thermal load and dissipation",
            "Redundancy and failover",
            "Integration with BMS and alarms",
            "Energy consumption and LCOS impact",
            "Ambient environmental conditions"
        ],
        primary_authority=[
            "UL 9540",
            "NFPA 855",
            "ASHRAE HVAC Design Guide"
        ],
        burden_holder="System Integrator",
        adversary_position="Passive cooling is sufficient for most container-based BESS.",
        counter_arguments=[
            "Active HVAC is required by most warranties and codes.",
            "Passive cooling is inadequate for high-density systems.",
            "Redundancy is essential for safety and uptime."
        ],
        resolution_strategy="Design HVAC to exceed minimum code and warranty requirements, with real-time monitoring.",
        entity_scope="BESS integrators and HVAC vendors",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="UL 9540 Section 6.2"
    ),
    DoctrineBlock(
        topic="Augmentation vs Full Replacement Strategy for Degraded Systems",
        keywords=["augmentation", "replacement", "degradation", "BESS", "asset management", "O&M"],
        conclusion_template="Augmentation with new battery modules is typically more cost-effective than full system replacement for grid-scale BESS experiencing capacity fade.",
        reasoning_framework="""
        As BESS degrade, operators face the choice of augmenting with new modules or replacing the entire system. Augmentation allows for incremental capacity restoration, lower upfront cost, and minimal disruption. Compatibility of new and old modules, warranty implications, and integration with existing controls must be considered. Full replacement may be warranted if system architecture or controls are obsolete. Financial modeling should compare LCOS, downtime, and long-term O&M costs.
        """,
        key_factors=[
            "Compatibility of new and old modules",
            "Warranty and support implications",
            "System downtime and disruption",
            "Cost comparison (augmentation vs replacement)",
            "Integration with controls and monitoring"
        ],
        primary_authority=[
            "NREL BESS Augmentation Guidelines",
            "DOE Energy Storage Handbook",
            "OEM Warranty Policies"
        ],
        burden_holder="Asset Owner",
        adversary_position="Full replacement ensures uniform performance and is simpler to manage.",
        counter_arguments=[
            "Augmentation is less capital-intensive.",
            "Modern controls can manage mixed module populations.",
            "OEMs increasingly support augmentation strategies."
        ],
        resolution_strategy="Conduct a detailed cost-benefit analysis and consult with OEMs on compatibility.",
        entity_scope="BESS asset owners and O&M providers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS Augmentation Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="UL 9540A Thermal Runaway Testing Protocol and Pass Criteria",
        keywords=["UL 9540A", "thermal runaway", "testing", "BESS", "compliance", "fire safety"],
        conclusion_template="Passing UL 9540A testing is required for permitting and insurance of grid-scale BESS; systems must demonstrate limited propagation and effective mitigation.",
        reasoning_framework="""
        UL 9540A is the industry standard for evaluating thermal runaway propagation in BESS. The protocol involves cell, module, unit, and installation-level tests to assess fire and gas release risks. Pass criteria include limited propagation, effective fire suppression, and compliance with local codes. Test results inform system design, permitting, and insurance underwriting. Failure to pass may require redesign or additional mitigation measures.
        """,
        key_factors=[
            "Test protocol adherence",
            "Propagation limitation",
            "Fire suppression effectiveness",
            "Gas release and ventilation",
            "Documentation and reporting"
        ],
        primary_authority=[
            "UL 9540A",
            "NFPA 855",
            "Local AHJ requirements"
        ],
        burden_holder="System Integrator",
        adversary_position="UL 9540A is overly conservative and not always enforced.",
        counter_arguments=[
            "Most AHJs require UL 9540A for permitting.",
            "Insurance providers mandate compliance.",
            "Test results improve system safety and marketability."
        ],
        resolution_strategy="Design for compliance and engage with test labs early in the project.",
        entity_scope="BESS integrators, developers, and AHJs",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="UL 9540A Test Protocol (2020)"
    ),
    DoctrineBlock(
        topic="Energy Arbitrage Revenue Optimization and Market Volatility",
        keywords=["energy arbitrage", "revenue optimization", "market volatility", "BESS", "dispatch", "trading"],
        conclusion_template="Advanced forecasting and optimization algorithms are required to maximize arbitrage revenue in volatile energy markets.",
        reasoning_framework="""
        Energy arbitrage involves charging BESS during low-price periods and discharging during high-price periods. Market volatility increases revenue potential but also risk. Advanced algorithms leveraging price forecasting, stochastic optimization, and real-time dispatch can significantly improve returns. Manual or rule-based strategies underperform in volatile markets. Integration with market data feeds and automated bidding platforms is essential for success.
        """,
        key_factors=[
            "Market price volatility",
            "Forecasting accuracy",
            "Optimization algorithm sophistication",
            "Integration with market platforms",
            "Risk management"
        ],
        primary_authority=[
            "FERC Order 841",
            "NREL BESS Market Participation Reports",
            "CAISO Market Rules"
        ],
        burden_holder="BESS Operator",
        adversary_position="Simple rule-based dispatch is sufficient for arbitrage revenue.",
        counter_arguments=[
            "Advanced algorithms outperform manual strategies.",
            "Market volatility increases the value of optimization.",
            "Automated bidding is required for fast-moving markets."
        ],
        resolution_strategy="Deploy and continuously refine forecasting and optimization tools.",
        entity_scope="BESS operators and traders",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS Market Participation Reports (2022)"
    ),
    # 25+ additional DoctrineBlock instances with real domain content follow...
    DoctrineBlock(
        topic="Battery Fire Suppression System Design and Integration",
        keywords=["fire suppression", "BESS", "system design", "integration", "safety", "NFPA 855"],
        conclusion_template="Integrated fire suppression systems using clean agents or water mist are required for BESS compliance with NFPA 855 and insurance underwriting.",
        reasoning_framework="""
        Fire suppression in BESS enclosures must be tailored to lithium-ion battery hazards, including thermal runaway and toxic gas release. NFPA 855 and UL 9540A require suppression systems that are effective, non-damaging to electronics, and capable of rapid deployment. Clean agents (e.g., Novec 1230, FM-200) and water mist are preferred. Integration with BMS and fire detection is critical for automated response. System design must consider enclosure size, ventilation, and maintenance access.
        """,
        key_factors=[
            "Suppression agent selection",
            "Integration with detection and BMS",
            "Enclosure size and ventilation",
            "Maintenance and inspection",
            "Regulatory and insurance requirements"
        ],
        primary_authority=[
            "NFPA 855",
            "UL 9540A",
            "FM Global Data Sheets"
        ],
        burden_holder="System Integrator",
        adversary_position="Standard building fire suppression is adequate for BESS.",
        counter_arguments=[
            "Lithium-ion fires require specialized suppression.",
            "NFPA 855 mandates BESS-specific systems.",
            "Insurance may deny coverage without compliance."
        ],
        resolution_strategy="Design and certify suppression systems to NFPA 855 and UL 9540A standards.",
        entity_scope="BESS integrators, fire protection engineers",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 855 Section 4.3.7"
    ),
    DoctrineBlock(
        topic="Battery Module-to-Module Isolation and Fault Detection",
        keywords=["module isolation", "fault detection", "BESS", "safety", "system design"],
        conclusion_template="Automatic module-to-module isolation and fault detection are essential for limiting fault propagation and maintaining system uptime in grid-scale BESS.",
        reasoning_framework="""
        Module-level isolation enables rapid disconnection of faulty modules, preventing fault propagation and reducing downtime. Fault detection algorithms should leverage voltage, current, and temperature monitoring to identify abnormal behavior. Integration with BMS and remote monitoring platforms is required for timely response. System design should ensure that isolation does not compromise overall system performance or safety.
        """,
        key_factors=[
            "Isolation switch reliability",
            "Fault detection algorithm accuracy",
            "Integration with BMS",
            "Impact on system availability",
            "Regulatory requirements"
        ],
        primary_authority=[
            "UL 9540",
            "IEEE 1679.1",
            "NFPA 855"
        ],
        burden_holder="System Integrator",
        adversary_position="System-level protection is sufficient; module isolation adds unnecessary complexity.",
        counter_arguments=[
            "Module isolation limits fault impact.",
            "Reduces repair time and downtime.",
            "Increasingly required by codes and insurers."
        ],
        resolution_strategy="Implement module isolation and validate with fault simulation testing.",
        entity_scope="BESS integrators and system designers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="UL 9540 Section 7.1"
    ),
    DoctrineBlock(
        topic="DC Overcurrent Protection and Coordination",
        keywords=["DC protection", "overcurrent", "coordination", "BESS", "system safety"],
        conclusion_template="Coordinated DC overcurrent protection is required to prevent cascading failures and ensure safe operation of BESS.",
        reasoning_framework="""
        DC overcurrent protection devices (fuses, breakers) must be coordinated to ensure selective tripping and minimize system impact. Protection settings should account for battery fault currents, inverter characteristics, and cable ratings. Coordination studies are required to validate protection schemes. Compliance with UL 9540 and NFPA 855 is mandatory. Regular testing and maintenance are essential for reliable operation.
        """,
        key_factors=[
            "Protection device selection and rating",
            "Coordination study results",
            "Battery and inverter fault current profiles",
            "Cable sizing and routing",
            "Testing and maintenance procedures"
        ],
        primary_authority=[
            "UL 9540",
            "NFPA 855",
            "IEEE 1375"
        ],
        burden_holder="System Integrator",
        adversary_position="AC-side protection is sufficient for BESS safety.",
        counter_arguments=[
            "DC faults can propagate rapidly and cause major damage.",
            "Codes require DC-side protection.",
            "Proper coordination reduces nuisance trips."
        ],
        resolution_strategy="Conduct coordination studies and implement tiered protection schemes.",
        entity_scope="BESS integrators and protection engineers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="UL 9540 Section 7.2"
    ),
    DoctrineBlock(
        topic="Remote Monitoring and Predictive Maintenance for BESS",
        keywords=["remote monitoring", "predictive maintenance", "BESS", "O&M", "asset management"],
        conclusion_template="Comprehensive remote monitoring and predictive maintenance platforms are essential for maximizing BESS uptime and reducing O&M costs.",
        reasoning_framework="""
        Remote monitoring enables real-time visibility into BESS performance, health, and alarms. Predictive maintenance leverages data analytics to anticipate failures and schedule interventions, reducing unplanned downtime. Integration with asset management systems and secure data transmission are critical. Platforms should support automated reporting, alarm escalation, and remote firmware updates. Predictive analytics require high-quality data and periodic model validation.
        """,
        key_factors=[
            "Data acquisition and quality",
            "Integration with asset management",
            "Alarm and escalation protocols",
            "Predictive analytics capabilities",
            "Cybersecurity and data privacy"
        ],
        primary_authority=[
            "NREL BESS O&M Guidelines",
            "DOE Energy Storage Handbook",
            "UL 9540"
        ],
        burden_holder="O&M Provider",
        adversary_position="On-site maintenance is sufficient for BESS reliability.",
        counter_arguments=[
            "Remote monitoring reduces O&M costs.",
            "Predictive maintenance prevents major failures.",
            "Industry trend is toward remote, data-driven O&M."
        ],
        resolution_strategy="Deploy and continuously improve remote monitoring and analytics platforms.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS O&M Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="Cybersecurity Requirements for Grid-Connected BESS",
        keywords=["cybersecurity", "BESS", "grid-connected", "NERC CIP", "data security"],
        conclusion_template="Grid-connected BESS must implement cybersecurity controls in accordance with NERC CIP standards to protect against data breaches and grid disruptions.",
        reasoning_framework="""
        As BESS become critical grid assets, they are increasingly targeted by cyber threats. NERC CIP standards require access control, network segmentation, incident response, and regular vulnerability assessments. Integration with utility SCADA and market platforms increases risk. Cybersecurity measures must be incorporated from design through operation, with regular training and audits. Failure to comply can result in regulatory penalties and operational disruptions.
        """,
        key_factors=[
            "Access control and authentication",
            "Network segmentation and firewalling",
            "Incident response planning",
            "Vulnerability assessment and patching",
            "Integration with utility systems"
        ],
        primary_authority=[
            "NERC CIP Standards",
            "DOE Cybersecurity for Energy Delivery Systems",
            "UL 2900"
        ],
        burden_holder="BESS Operator",
        adversary_position="Cybersecurity requirements are excessive for BESS and increase costs.",
        counter_arguments=[
            "Grid disruptions from cyber attacks are increasing.",
            "Regulatory penalties for non-compliance are severe.",
            "Cybersecurity is a prerequisite for market participation."
        ],
        resolution_strategy="Implement NERC CIP controls and conduct regular audits.",
        entity_scope="BESS operators and IT teams",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC CIP-003-9"
    ),
    DoctrineBlock(
        topic="BESS Interconnection Standards and Utility Coordination",
        keywords=["interconnection", "utility coordination", "BESS", "IEEE 1547", "grid integration"],
        conclusion_template="Compliance with IEEE 1547 and utility-specific interconnection standards is mandatory for grid-connected BESS.",
        reasoning_framework="""
        Interconnection standards ensure safe and reliable integration of BESS with the utility grid. IEEE 1547 specifies requirements for voltage, frequency, anti-islanding, and communications. Utilities may impose additional requirements for protection, telemetry, and operational coordination. Early engagement with utilities and AHJs is critical to avoid project delays. Documentation and testing are required for approval.
        """,
        key_factors=[
            "IEEE 1547 compliance",
            "Utility-specific requirements",
            "Protection and anti-islanding",
            "Telemetry and communications",
            "Testing and documentation"
        ],
        primary_authority=[
            "IEEE 1547-2018",
            "FERC Order 841",
            "Utility Interconnection Handbooks"
        ],
        burden_holder="Project Developer",
        adversary_position="IEEE 1547 is sufficient; utility-specific requirements are redundant.",
        counter_arguments=[
            "Utilities have unique operational needs.",
            "Non-compliance can delay or block interconnection.",
            "Early coordination reduces risk."
        ],
        resolution_strategy="Engage utilities early and design for both IEEE 1547 and local requirements.",
        entity_scope="BESS project developers and integrators",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 1547-2018 Section 10"
    ),
    DoctrineBlock(
        topic="BESS Warranty Structure and Performance Guarantees",
        keywords=["warranty", "performance guarantee", "BESS", "OEM", "contracting"],
        conclusion_template="BESS warranties should include explicit performance guarantees for capacity retention, round-trip efficiency, and response time, with clear remedies for underperformance.",
        reasoning_framework="""
        BESS warranties are critical for project bankability. Key terms include guaranteed capacity retention (typically 70-80% at year 10), round-trip efficiency, and response time. Remedies for underperformance may include module replacement, augmentation, or financial compensation. Warranty exclusions (abuse, non-compliant operation) must be clearly defined. Negotiation should ensure alignment with project revenue models and O&M practices.
        """,
        key_factors=[
            "Capacity retention guarantee",
            "Round-trip efficiency guarantee",
            "Response time and availability",
            "Remedies and exclusions",
            "Alignment with project revenue model"
        ],
        primary_authority=[
            "OEM Warranty Policies",
            "NREL BESS Contracting Guidelines",
            "DOE Energy Storage Handbook"
        ],
        burden_holder="OEM",
        adversary_position="Standard warranties are sufficient; performance guarantees are unnecessary.",
        counter_arguments=[
            "Performance guarantees are required for project finance.",
            "Clear remedies reduce project risk.",
            "Alignment with O&M is critical for long-term success."
        ],
        resolution_strategy="Negotiate warranties to include explicit performance guarantees and remedies.",
        entity_scope="BESS project developers and financiers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS Contracting Guidelines (2022)"
    ),
    DoctrineBlock(
        topic="BESS End-of-Life Management and Recycling",
        keywords=["end-of-life", "recycling", "BESS", "sustainability", "circular economy"],
        conclusion_template="End-of-life planning and recycling are essential for BESS sustainability and regulatory compliance; partnerships with certified recyclers are recommended.",
        reasoning_framework="""
        BESS end-of-life management includes decommissioning, recycling, and disposal of battery modules and system components. Regulatory requirements (e.g., RCRA, EU Battery Directive) mandate proper handling of hazardous materials. Recycling recovers valuable metals and reduces environmental impact. Partnerships with certified recyclers and documentation of material flows are recommended. Early planning ensures compliance and reduces costs.
        """,
        key_factors=[
            "Regulatory compliance (RCRA, EU Battery Directive)",
            "Recycling partner certification",
            "Material flow documentation",
            "Cost and logistics",
            "Environmental impact"
        ],
        primary_authority=[
            "EPA RCRA",
            "EU Battery Directive",
            "DOE Energy Storage Handbook"
        ],
        burden_holder="Asset Owner",
        adversary_position="End-of-life planning can be deferred until system retirement.",
        counter_arguments=[
            "Early planning reduces cost and risk.",
            "Regulatory penalties for improper disposal are severe.",
            "Recycling recovers valuable materials."
        ],
        resolution_strategy="Establish recycling partnerships and document end-of-life plans during project development.",
        entity_scope="BESS asset owners and developers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA RCRA Subtitle C"
    ),
    DoctrineBlock(
        topic="BESS Insurance Requirements and Risk Mitigation",
        keywords=["insurance", "risk mitigation", "BESS", "project finance", "compliance"],
        conclusion_template="Comprehensive insurance coverage, including property, liability, and business interruption, is required for BESS project finance and compliance.",
        reasoning_framework="""
        Insurance is a prerequisite for BESS project finance and operation. Coverage should include property damage, liability, business interruption, and environmental liability. Insurers require compliance with NFPA 855, UL 9540A, and other standards. Risk mitigation measures (fire suppression, monitoring, cybersecurity) reduce premiums and improve insurability. Early engagement with insurers and documentation of risk controls are recommended.
        """,
        key_factors=[
            "Coverage types and limits",
            "Compliance with codes and standards",
            "Risk mitigation measures",
            "Premiums and deductibles",
            "Claims process and documentation"
        ],
        primary_authority=[
            "FM Global Data Sheets",
            "NFPA 855",
            "UL 9540A"
        ],
        burden_holder="Project Developer",
        adversary_position="Insurance is a minor consideration and can be arranged post-commissioning.",
        counter_arguments=[
            "Insurance is required for project finance.",
            "Non-compliance increases premiums or denies coverage.",
            "Early engagement reduces risk."
        ],
        resolution_strategy="Engage insurers early and document all risk mitigation measures.",
        entity_scope="BESS project developers and owners",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FM Global Data Sheets 5-33"
    ),
    DoctrineBlock(
        topic="BESS Commissioning and Acceptance Testing Protocols",
        keywords=["commissioning", "acceptance testing", "BESS", "protocols", "project delivery"],
        conclusion_template="Comprehensive commissioning and acceptance testing are required to validate BESS performance and ensure safe, reliable operation.",
        reasoning_framework="""
        Commissioning protocols include functional testing, safety checks, performance validation, and integration with utility SCADA. Acceptance criteria should be defined in contracts and include capacity, efficiency, response time, and safety system operation. Documentation and witness testing by third parties or utilities are recommended. Failure to meet criteria may require remediation or delay project acceptance.
        """,
        key_factors=[
            "Functional and safety testing",
            "Performance validation",
            "Integration with utility systems",
            "Documentation and witness testing",
            "Remediation procedures"
        ],
        primary_authority=[
            "NREL BESS Commissioning Guidelines",
            "UL 9540",
            "Utility Interconnection Handbooks"
        ],
        burden_holder="System Integrator",
        adversary_position="Factory testing is sufficient; field commissioning adds little value.",
        counter_arguments=[
            "Field commissioning validates integration and site-specific issues.",
            "Required by utilities and financiers.",
            "Reduces risk of post-commissioning failures."
        ],
        resolution_strategy="Define and execute comprehensive commissioning protocols with third-party oversight.",
        entity_scope="BESS integrators and project owners",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS Commissioning Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="BESS Round-Trip Efficiency Measurement and Reporting",
        keywords=["round-trip efficiency", "measurement", "reporting", "BESS", "performance"],
        conclusion_template="Round-trip efficiency should be measured under representative operating conditions and reported in accordance with industry standards.",
        reasoning_framework="""
        Round-trip efficiency (RTE) is a key performance metric for BESS, reflecting energy losses during charge/discharge cycles. Measurement should account for auxiliary loads (HVAC, controls) and be conducted under representative temperature and load conditions. Reporting should follow industry standards (e.g., IEC 62933-2-2) and be included in performance guarantees and LCOS calculations. Regular measurement supports warranty claims and O&M optimization.
        """,
        key_factors=[
            "Measurement protocol",
            "Inclusion of auxiliary loads",
            "Operating conditions",
            "Reporting standards",
            "Impact on performance guarantees"
        ],
        primary_authority=[
            "IEC 62933-2-2",
            "NREL BESS Performance Testing",
            "OEM Warranty Policies"
        ],
        burden_holder="System Integrator",
        adversary_position="Nameplate efficiency is sufficient for project evaluation.",
        counter_arguments=[
            "Actual RTE can vary significantly from nameplate.",
            "Auxiliary loads reduce effective efficiency.",
            "Accurate measurement supports warranty and LCOS."
        ],
        resolution_strategy="Conduct regular RTE measurement and report in accordance with IEC 62933-2-2.",
        entity_scope="BESS integrators and project owners",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEC 62933-2-2"
    ),
    DoctrineBlock(
        topic="BESS System Integration with Renewable Generation",
        keywords=["system integration", "renewable generation", "BESS", "solar", "wind", "hybrid projects"],
        conclusion_template="Integrated BESS-renewable systems require coordinated controls and communications to maximize value and ensure grid compliance.",
        reasoning_framework="""
        Hybrid projects combining BESS with solar or wind generation require coordinated controls for optimal dispatch, grid compliance, and revenue stacking. Integration challenges include inverter sizing, control system interoperability, and compliance with grid codes. Communication protocols (e.g., Modbus, DNP3) and cybersecurity must be addressed. Early design coordination with renewable OEMs and utilities is recommended.
        """,
        key_factors=[
            "Control system interoperability",
            "Inverter sizing and configuration",
            "Grid code compliance",
            "Communications and cybersecurity",
            "Revenue stacking opportunities"
        ],
        primary_authority=[
            "IEEE 1547-2018",
            "NREL Hybrid Project Guidelines",
            "Utility Interconnection Handbooks"
        ],
        burden_holder="Project Developer",
        adversary_position="Separate operation of BESS and renewables is simpler and sufficient.",
        counter_arguments=[
            "Integrated controls maximize project value.",
            "Grid codes increasingly require coordination.",
            "Hybrid projects improve financing and market access."
        ],
        resolution_strategy="Design for integrated controls and engage all stakeholders early.",
        entity_scope="BESS project developers and integrators",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL Hybrid Project Guidelines (2022)"
    ),
    DoctrineBlock(
        topic="BESS Operating Envelope and Environmental Limits",
        keywords=["operating envelope", "environmental limits", "BESS", "temperature", "humidity", "altitude"],
        conclusion_template="BESS must be operated within manufacturer-specified environmental limits to maintain warranty and ensure safe, reliable performance.",
        reasoning_framework="""
        Manufacturer specifications for temperature, humidity, and altitude define the safe operating envelope for BESS. Exceeding these limits accelerates degradation, increases safety risk, and may void warranties. Site selection and system design should account for local climate and provide necessary HVAC or environmental controls. Monitoring and alarms are required to detect excursions and trigger protective actions.
        """,
        key_factors=[
            "Manufacturer environmental specifications",
            "Site climate and conditions",
            "HVAC and environmental controls",
            "Monitoring and alarms",
            "Warranty implications"
        ],
        primary_authority=[
            "OEM Product Specifications",
            "UL 9540",
            "NREL BESS O&M Guidelines"
        ],
        burden_holder="O&M Provider",
        adversary_position="BESS can tolerate short-term excursions beyond specified limits.",
        counter_arguments=[
            "Even short-term excursions can cause damage.",
            "Warranty coverage may be voided.",
            "Monitoring and controls are standard industry practice."
        ],
        resolution_strategy="Design for environmental compliance and implement continuous monitoring.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OEM Product Specifications"
    ),
    DoctrineBlock(
        topic="BESS Emergency Shutdown and Black Start Procedures",
        keywords=["emergency shutdown", "black start", "BESS", "procedures", "grid support"],
        conclusion_template="Documented emergency shutdown and black start procedures are required for safe BESS operation and grid support.",
        reasoning_framework="""
        Emergency shutdown procedures ensure safe isolation of BESS during faults or external hazards. Black start capability enables BESS to restore grid segments after outages. Procedures must be documented, tested, and integrated with utility protocols. Training and drills are required for O&M personnel. Automated controls should support manual intervention as needed.
        """,
        key_factors=[
            "Procedure documentation",
            "Integration with utility protocols",
            "Training and drills",
            "Automated and manual controls",
            "Testing and validation"
        ],
        primary_authority=[
            "NERC Reliability Standards",
            "Utility Emergency Procedures",
            "NREL BESS O&M Guidelines"
        ],
        burden_holder="O&M Provider",
        adversary_position="Emergency procedures are rarely needed and can be generic.",
        counter_arguments=[
            "Site-specific hazards require tailored procedures.",
            "Grid support requires reliable black start capability.",
            "Training reduces risk of human error."
        ],
        resolution_strategy="Develop, document, and regularly test site-specific procedures.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NERC EOP-005-3"
    ),
    DoctrineBlock(
        topic="BESS Data Logging, Retention, and Regulatory Reporting",
        keywords=["data logging", "retention", "regulatory reporting", "BESS", "compliance"],
        conclusion_template="Comprehensive data logging and retention are required for BESS regulatory compliance, warranty support, and performance optimization.",
        reasoning_framework="""
        BESS data logging must capture operational, safety, and performance parameters at sufficient resolution for regulatory, warranty, and O&M purposes. Retention periods are defined by contracts and regulations (typically 5-10 years). Secure storage and backup are required. Automated reporting supports compliance with utility, market, and environmental regulations. Data integrity and privacy must be maintained.
        """,
        key_factors=[
            "Logging resolution and parameters",
            "Retention period and storage",
            "Automated reporting",
            "Data integrity and privacy",
            "Compliance with regulations and contracts"
        ],
        primary_authority=[
            "FERC Order 841",
            "NERC Reliability Standards",
            "OEM Warranty Policies"
        ],
        burden_holder="BESS Operator",
        adversary_position="Minimal data logging is sufficient for BESS operation.",
        counter_arguments=[
            "Regulations require detailed logging and retention.",
            "Data supports warranty and performance claims.",
            "Automated reporting reduces O&M burden."
        ],
        resolution_strategy="Implement comprehensive logging, secure storage, and automated reporting.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FERC Order 841"
    ),
    DoctrineBlock(
        topic="BESS Auxiliary Power Supply Reliability",
        keywords=["auxiliary power", "reliability", "BESS", "HVAC", "controls", "safety"],
        conclusion_template="Redundant auxiliary power supplies are required for critical BESS subsystems (HVAC, controls, safety) to ensure continuous operation.",
        reasoning_framework="""
        Auxiliary power supplies support critical BESS subsystems, including HVAC, controls, and safety systems. Loss of auxiliary power can lead to thermal excursions, loss of monitoring, and safety incidents. Redundant supplies (e.g., dual feeds, UPS) are required for reliability. Monitoring and alarms should detect failures and trigger corrective actions. Design must comply with UL 9540 and NFPA 855.
        """,
        key_factors=[
            "Redundancy and failover",
            "Subsystem criticality",
            "Monitoring and alarms",
            "Compliance with codes",
            "Maintenance and testing"
        ],
        primary_authority=[
            "UL 9540",
            "NFPA 855",
            "NREL BESS O&M Guidelines"
        ],
        burden_holder="System Integrator",
        adversary_position="Single auxiliary power supply is sufficient for most BESS.",
        counter_arguments=[
            "Redundancy is standard for critical systems.",
            "Loss of auxiliary power can cause major incidents.",
            "Codes require reliable auxiliary power."
        ],
        resolution_strategy="Design and test redundant auxiliary power supplies for all critical subsystems.",
        entity_scope="BESS integrators and project owners",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="UL 9540 Section 6.3"
    ),
    DoctrineBlock(
        topic="BESS SCADA Integration and Interoperability",
        keywords=["SCADA", "integration", "interoperability", "BESS", "control systems"],
        conclusion_template="SCADA integration with open protocols and standardized data models is required for BESS interoperability and utility coordination.",
        reasoning_framework="""
        SCADA integration enables remote monitoring, control, and coordination of BESS with utility operations. Open protocols (e.g., Modbus, DNP3, IEC 61850) and standardized data models ensure interoperability and future-proofing. Integration must address cybersecurity, data mapping, and alarm management. Testing and documentation are required for utility acceptance.
        """,
        key_factors=[
            "Protocol selection and compatibility",
            "Data model standardization",
            "Cybersecurity and access control",
            "Alarm and event management",
            "Testing and documentation"
        ],
        primary_authority=[
            "IEEE 2030.5",
            "IEC 61850",
            "Utility SCADA Integration Guides"
        ],
        burden_holder="System Integrator",
        adversary_position="Proprietary protocols are sufficient for BESS SCADA integration.",
        counter_arguments=[
            "Open protocols enable interoperability and reduce vendor lock-in.",
            "Utilities increasingly require standardized integration.",
            "Cybersecurity is easier to manage with open standards."
        ],
        resolution_strategy="Design for open protocol integration and validate with utility SCADA teams.",
        entity_scope="BESS integrators and utilities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 2030.5"
    ),
    DoctrineBlock(
        topic="BESS Harmonics and Power Quality Compliance",
        keywords=["harmonics", "power quality", "BESS", "IEEE 519", "grid compliance"],
        conclusion_template="BESS inverters must comply with IEEE 519 harmonic limits to avoid grid disturbances and ensure interconnection approval.",
        reasoning_framework="""
        BESS inverters can introduce harmonics that affect grid power quality. IEEE 519 defines limits for harmonic distortion at the point of common coupling. Compliance is required for interconnection approval and grid stability. Harmonic filters and advanced inverter controls may be necessary. Regular testing and reporting are recommended.
        """,
        key_factors=[
            "Harmonic measurement and reporting",
            "Inverter control algorithms",
            "Filter design and sizing",
            "Grid code compliance",
            "Testing and documentation"
        ],
        primary_authority=[
            "IEEE 519",
            "Utility Interconnection Handbooks",
            "NREL BESS Grid Integration Reports"
        ],
        burden_holder="System Integrator",
        adversary_position="Harmonics from BESS are negligible and do not require mitigation.",
        counter_arguments=[
            "Grid codes require compliance with IEEE 519.",
            "Harmonics can cause grid disturbances.",
            "Mitigation is standard practice for large BESS."
        ],
        resolution_strategy="Test and document harmonic compliance as part of commissioning.",
        entity_scope="BESS integrators and utilities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEEE 519-2014"
    ),
    DoctrineBlock(
        topic="BESS Emergency Response Planning and Community Engagement",
        keywords=["emergency response", "community engagement", "BESS", "safety", "permitting"],
        conclusion_template="Comprehensive emergency response plans and community engagement are required for BESS permitting and social license to operate.",
        reasoning_framework="""
        Emergency response planning includes coordination with local fire departments, training, and drills. Community engagement addresses public concerns about safety, noise, and environmental impact. Transparent communication and documented response plans are required for permitting and insurance. Engagement reduces opposition and improves project acceptance.
        """,
        key_factors=[
            "Coordination with emergency services",
            "Training and drills",
            "Community outreach and communication",
            "Documentation and permitting",
            "Insurance and regulatory requirements"
        ],
        primary_authority=[
            "NFPA 855",
            "Local permitting authorities",
            "NREL BESS Community Engagement Guide"
        ],
        burden_holder="Project Developer",
        adversary_position="Emergency response planning is the responsibility of local authorities.",
        counter_arguments=[
            "Project owner is responsible for site-specific planning.",
            "Community engagement reduces project risk.",
            "Permitting requires documented plans."
        ],
        resolution_strategy="Develop and communicate emergency response plans and engage with stakeholders early.",
        entity_scope="BESS project developers and owners",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 855 Section 4.4"
    ),
    DoctrineBlock(
        topic="BESS Noise and Environmental Impact Mitigation",
        keywords=["noise", "environmental impact", "BESS", "mitigation", "permitting"],
        conclusion_template="Noise and environmental impact mitigation measures are required for BESS permitting and community acceptance.",
        reasoning_framework="""
        BESS installations generate noise from HVAC, inverters, and transformers. Environmental impacts include land use, visual effects, and potential contamination. Permitting authorities require noise studies and mitigation (e.g., barriers, equipment selection). Environmental impact assessments may be required. Early identification and mitigation of impacts improve project acceptance and reduce permitting risk.
        """,
        key_factors=[
            "Noise study and mitigation",
            "Environmental impact assessment",
            "Equipment selection and siting",
            "Community engagement",
            "Permitting requirements"
        ],
        primary_authority=[
            "Local permitting authorities",
            "EPA Noise Guidelines",
            "NREL BESS Environmental Impact Reports"
        ],
        burden_holder="Project Developer",
        adversary_position="Noise and environmental impacts are minimal for BESS.",
        counter_arguments=[
            "Permitting authorities require mitigation measures.",
            "Community acceptance depends on impact management.",
            "Proactive mitigation reduces project risk."
        ],
        resolution_strategy="Conduct studies and implement mitigation measures as part of project design.",
        entity_scope="BESS project developers and owners",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Noise Guidelines"
    ),
    DoctrineBlock(
        topic="BESS Spare Parts Inventory and O&M Planning",
        keywords=["spare parts", "inventory", "O&M", "BESS", "asset management"],
        conclusion_template="Maintaining a strategic spare parts inventory is essential for minimizing BESS downtime and supporting O&M activities.",
        reasoning_framework="""
        Spare parts inventory should include critical components (modules, fuses, HVAC parts) with long lead times or high failure rates. Inventory planning should be based on failure mode analysis and historical data. Integration with asset management systems enables tracking and forecasting. Regular review and adjustment of inventory levels are required. OEM support agreements can supplement inventory for rare or high-value parts.
        """,
        key_factors=[
            "Critical component identification",
            "Failure mode and historical analysis",
            "Inventory tracking and forecasting",
            "OEM support agreements",
            "O&M planning and budgeting"
        ],
        primary_authority=[
            "NREL BESS O&M Guidelines",
            "DOE Energy Storage Handbook",
            "OEM Support Policies"
        ],
        burden_holder="O&M Provider",
        adversary_position="Just-in-time ordering is sufficient for BESS spare parts.",
        counter_arguments=[
            "Lead times for critical parts can be long.",
            "Downtime costs outweigh inventory costs.",
            "Inventory supports rapid response to failures."
        ],
        resolution_strategy="Develop and maintain a strategic spare parts inventory and review regularly.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS O&M Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="BESS System Scalability and Modular Design",
        keywords=["scalability", "modular design", "BESS", "system architecture", "expansion"],
        conclusion_template="Modular system architecture enables scalable BESS deployment and simplifies future expansion or augmentation.",
        reasoning_framework="""
        Modular design allows BESS to be deployed in increments and expanded as needs evolve. Standardized modules simplify integration, maintenance, and augmentation. Scalability reduces project risk and improves financing options. System architecture should support plug-and-play expansion, with controls and communications designed for modularity.
        """,
        key_factors=[
            "Module standardization",
            "Plug-and-play integration",
            "Controls and communications scalability",
            "Expansion and augmentation planning",
            "Financing and risk reduction"
        ],
        primary_authority=[
            "NREL BESS System Design Guidelines",
            "DOE Energy Storage Handbook",
            "OEM Product Specifications"
        ],
        burden_holder="System Integrator",
        adversary_position="Custom system design is required for each project.",
        counter_arguments=[
            "Modular design reduces engineering and integration costs.",
            "Simplifies future expansion and O&M.",
            "Improves project bankability."
        ],
        resolution_strategy="Adopt modular architecture and standardize interfaces across projects.",
        entity_scope="BESS integrators and project developers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS System Design Guidelines (2022)"
    ),
    DoctrineBlock(
        topic="BESS Vendor Qualification and Bankability Assessment",
        keywords=["vendor qualification", "bankability", "BESS", "procurement", "project finance"],
        conclusion_template="Vendor qualification and bankability assessment are required to ensure BESS project reliability and financeability.",
        reasoning_framework="""
        Vendor qualification assesses technical capability, financial stability, and track record. Bankability assessment evaluates warranty terms, service support, and project references. Due diligence reduces risk of vendor failure and supports project finance. Third-party assessments and reference checks are recommended. Procurement should include clear technical and commercial requirements.
        """,
        key_factors=[
            "Technical capability and product quality",
            "Financial stability and track record",
            "Warranty and service support",
            "Project references and third-party assessments",
            "Procurement process and requirements"
        ],
        primary_authority=[
            "NREL BESS Procurement Guidelines",
            "DOE Energy Storage Handbook",
            "Project Finance Best Practices"
        ],
        burden_holder="Project Developer",
        adversary_position="Vendor qualification is unnecessary for established brands.",
        counter_arguments=[
            "Bankability is required for project finance.",
            "Track record and support are critical for long-term success.",
            "Due diligence reduces project risk."
        ],
        resolution_strategy="Conduct thorough qualification and bankability assessment for all vendors.",
        entity_scope="BESS project developers and financiers",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS Procurement Guidelines (2022)"
    ),
    DoctrineBlock(
        topic="BESS System Availability and Performance Monitoring",
        keywords=["system availability", "performance monitoring", "BESS", "O&M", "asset management"],
        conclusion_template="Continuous system availability and performance monitoring are required to meet contractual obligations and optimize BESS operation.",
        reasoning_framework="""
        System availability is a key performance indicator in BESS contracts. Continuous monitoring enables rapid detection and resolution of faults, supporting uptime guarantees. Performance monitoring includes capacity, efficiency, response time, and safety system operation. Integration with asset management and automated reporting supports O&M and warranty claims. Regular review and improvement of monitoring protocols are recommended.
        """,
        key_factors=[
            "Availability and performance metrics",
            "Continuous monitoring and alarms",
            "Integration with asset management",
            "Automated reporting",
            "O&M and warranty support"
        ],
        primary_authority=[
            "NREL BESS O&M Guidelines",
            "OEM Warranty Policies",
            "DOE Energy Storage Handbook"
        ],
        burden_holder="O&M Provider",
        adversary_position="Periodic manual checks are sufficient for BESS performance.",
        counter_arguments=[
            "Continuous monitoring is standard industry practice.",
            "Supports uptime guarantees and rapid fault response.",
            "Improves O&M efficiency and warranty support."
        ],
        resolution_strategy="Implement continuous monitoring and automated reporting for all BESS.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS O&M Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="BESS System Documentation and Change Management",
        keywords=["documentation", "change management", "BESS", "O&M", "compliance"],
        conclusion_template="Comprehensive system documentation and formal change management processes are required for BESS compliance, O&M, and warranty support.",
        reasoning_framework="""
        Documentation includes system design, as-built drawings, operating procedures, and maintenance records. Change management tracks modifications to hardware, software, or procedures, ensuring traceability and compliance. Formal processes reduce risk of errors, support warranty claims, and are required by codes and insurers. Regular review and updates are recommended.
        """,
        key_factors=[
            "System design and as-built documentation",
            "Operating procedures and maintenance records",
            "Change management process",
            "Compliance with codes and contracts",
            "O&M and warranty support"
        ],
        primary_authority=[
            "NREL BESS O&M Guidelines",
            "UL 9540",
            "OEM Warranty Policies"
        ],
        burden_holder="O&M Provider",
        adversary_position="Informal documentation and change tracking are sufficient.",
        counter_arguments=[
            "Formal processes reduce risk of errors and non-compliance.",
            "Required for warranty and insurance support.",
            "Supports efficient O&M and project handover."
        ],
        resolution_strategy="Maintain comprehensive documentation and implement formal change management for all BESS.",
        entity_scope="BESS operators and O&M providers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS O&M Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="BESS System Decommissioning and Site Restoration",
        keywords=["decommissioning", "site restoration", "BESS", "end-of-life", "compliance"],
        conclusion_template="Planned decommissioning and site restoration are required for BESS end-of-life compliance and community acceptance.",
        reasoning_framework="""
        Decommissioning includes safe removal of batteries, disposal or recycling of components, and restoration of the site to pre-project conditions. Regulatory requirements define procedures for hazardous material handling and site remediation. Early planning and engagement with local authorities reduce cost and risk. Documentation of decommissioning and restoration is required for regulatory and community acceptance.
        """,
        key_factors=[
            "Decommissioning planning and procedures",
            "Hazardous material handling",
            "Site remediation and restoration",
            "Regulatory compliance",
            "Community engagement"
        ],
        primary_authority=[
            "EPA RCRA",
            "Local permitting authorities",
            "NREL BESS Decommissioning Guidelines"
        ],
        burden_holder="Asset Owner",
        adversary_position="Decommissioning can be addressed at end-of-life without advance planning.",
        counter_arguments=[
            "Early planning reduces cost and risk.",
            "Regulatory compliance requires documentation.",
            "Community acceptance depends on responsible site restoration."
        ],
        resolution_strategy="Develop decommissioning and restoration plans during project development.",
        entity_scope="BESS asset owners and developers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA RCRA Subtitle C"
    ),
    DoctrineBlock(
        topic="BESS System Expansion and Repowering Strategies",
        keywords=["expansion", "repowering", "BESS", "augmentation", "asset management"],
        conclusion_template="Planned system expansion and repowering strategies enable BESS to adapt to evolving market and operational requirements.",
        reasoning_framework="""
        Expansion and repowering involve adding new capacity or replacing aging components to extend BESS life and adapt to market changes. Strategies should consider compatibility, controls integration, and warranty implications. Financial modeling should include LCOS, downtime, and revenue impacts. Early planning enables flexible response to future needs and maximizes asset value.
        """,
        key_factors=[
            "Compatibility and integration",
            "Controls and communications",
            "Warranty and support",
            "Financial modeling and LCOS",
            "Regulatory and market requirements"
        ],
        primary_authority=[
            "NREL BESS Asset Management Guidelines",
            "DOE Energy Storage Handbook",
            "OEM Support Policies"
        ],
        burden_holder="Asset Owner",
        adversary_position="Expansion and repowering are rarely needed and can be managed ad hoc.",
        counter_arguments=[
            "Planned strategies reduce cost and risk.",
            "Market and regulatory changes may require adaptation.",
            "Maximizes long-term asset value."
        ],
        resolution_strategy="Develop expansion and repowering strategies as part of asset management planning.",
        entity_scope="BESS asset owners and developers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NREL BESS Asset Management Guidelines (2022)"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]