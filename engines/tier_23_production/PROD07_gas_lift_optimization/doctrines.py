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
        topic="Thornhill-Craver Gas Lift Valve Equation",
        keywords=[
            "gas lift", "valve equation", "Thornhill-Craver", "orifice flow", "pressure drop",
            "choked flow", "critical flow", "subcritical flow", "gas injection", "valve sizing"
        ],
        conclusion_template="The Thornhill-Craver equation is the controlling model for sizing and evaluating gas lift valve performance under both critical and subcritical flow regimes.",
        reasoning_framework=(
            "The Thornhill-Craver equation provides a fundamental basis for calculating the flow rate through a gas lift valve as a function of upstream and downstream pressures, "
            "temperature, and valve port area. For critical flow, the equation simplifies as downstream pressure becomes negligible compared to upstream pressure, while for subcritical flow, "
            "the pressure differential must be explicitly considered. The equation is validated by field data and is widely accepted in the industry for valve sizing and system design. "
            "Valve manufacturers and field engineers rely on this equation to ensure proper gas injection rates and to avoid operational issues such as unstable flow or valve chattering. "
            "The equation's parameters must be calibrated with actual well conditions, including gas composition and temperature, to ensure accuracy. Deviations from the equation are typically "
            "due to non-ideal gas behavior or valve wear, which must be accounted for in ongoing monitoring and maintenance. The equation is referenced in API RP 11V6 and SPE technical papers."
        ),
        key_factors=[
            "Upstream and downstream pressures", "Valve port area", "Gas temperature", "Gas composition",
            "Flow regime (critical/subcritical)", "Valve calibration", "Field validation"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Thornhill-Craver original publication"
        ],
        burden_holder="Gas lift system designer",
        adversary_position="Alternative valve sizing equations may be proposed, citing non-ideal flow or empirical field data.",
        counter_arguments=[
            "Thornhill-Craver equation is validated by decades of field application.",
            "Alternative equations often reduce to Thornhill-Craver under standard conditions.",
            "API and major manufacturers specify this equation as the default basis."
        ],
        resolution_strategy="Default to Thornhill-Craver unless field data demonstrates persistent, significant deviation; document any alternative methodology and obtain engineering approval.",
        entity_scope="All gas lift system designs using injection valves",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 6.2"
    ),
    DoctrineBlock(
        topic="Injection Pressure Design and Gradient Matching",
        keywords=[
            "injection pressure", "gradient matching", "gas lift design", "wellbore pressure profile",
            "annulus pressure", "tubing pressure", "valve opening", "set depth"
        ],
        conclusion_template="Injection pressure design must ensure that the annulus pressure gradient matches the tubing pressure gradient at each valve depth to guarantee sequential valve opening and efficient unloading.",
        reasoning_framework=(
            "Gradient matching is essential for proper gas lift valve operation during unloading. The annulus pressure at each valve depth must be sufficient to open the valve and inject gas into the tubing, "
            "but not so high as to cause simultaneous opening of multiple valves, which can lead to inefficient unloading and possible instability. The design process involves plotting the annulus and tubing pressure "
            "profiles and selecting valve set depths such that the annulus pressure gradient intersects the tubing pressure gradient at the desired points. This ensures that each valve opens in sequence as the well "
            "unloads, minimizing the risk of gas lock or incomplete unloading. The process is governed by API RP 11V6 and is supported by simulation tools and field experience. Deviations from the gradient matching "
            "principle are only justified in special cases such as dual string completions or highly deviated wells, and must be documented."
        ),
        key_factors=[
            "Annulus pressure profile", "Tubing pressure profile", "Valve set depths",
            "Well deviation", "Gas injection rate", "Reservoir pressure"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Gas Lift Design Manual"
        ],
        burden_holder="Gas lift design engineer",
        adversary_position="Some argue for simplified design without strict gradient matching, citing operational flexibility or cost.",
        counter_arguments=[
            "Lack of gradient matching leads to unpredictable valve operation and unstable unloading.",
            "API and industry best practices require gradient matching for reliable performance.",
            "Simulation and field data confirm the necessity of this approach."
        ],
        resolution_strategy="Enforce gradient matching in all standard designs; exceptions require engineering review and risk assessment.",
        entity_scope="All new and retrofit gas lift installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 7.1"
    ),
    DoctrineBlock(
        topic="Gas-Liquid Ratio (GLR) Optimization",
        keywords=[
            "GLR", "gas-liquid ratio", "optimization", "injection rate", "production rate",
            "economic limit", "gas lift efficiency", "lift gas allocation"
        ],
        conclusion_template="GLR should be optimized to maximize oil production while minimizing gas usage, subject to economic and operational constraints.",
        reasoning_framework=(
            "The optimal GLR is a function of reservoir characteristics, well geometry, and surface facility constraints. Excessive gas injection can lead to diminishing returns in oil production and increased "
            "compression costs, while insufficient gas reduces lift efficiency and production. The optimization process involves constructing a GLR vs. production rate curve, identifying the point of maximum "
            "economic benefit. This typically requires iterative simulation and field testing. The process must account for gas availability, compression horsepower, and potential for gas breakthrough. "
            "GLR optimization is a continuous process, as reservoir and facility conditions change over time. The doctrine is supported by SPE 1063 and API RP 11V6."
        ),
        key_factors=[
            "Reservoir pressure", "Well productivity index", "Gas availability",
            "Compression cost", "Production rate", "Facility constraints"
        ],
        primary_authority=[
            "SPE 1063", "API RP 11V6", "Gas Lift Optimization Guidelines"
        ],
        burden_holder="Production engineer",
        adversary_position="Operators may inject more gas than optimal to maximize short-term production.",
        counter_arguments=[
            "Excess gas injection increases operating costs and may reduce overall recovery.",
            "Optimization ensures sustainable production and cost control.",
            "Field studies confirm the economic benefit of GLR optimization."
        ],
        resolution_strategy="Implement continuous monitoring and periodic GLR optimization studies; enforce gas allocation limits based on economic analysis.",
        entity_scope="All gas lifted wells and fields",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE 1063, Section 4.3"
    ),
    DoctrineBlock(
        topic="Unloading Valve Spacing and Design",
        keywords=[
            "unloading valve", "valve spacing", "gas lift", "set depth", "unloading sequence",
            "wellbore geometry", "pressure profile"
        ],
        conclusion_template="Unloading valves must be spaced to ensure sequential opening and complete unloading, with set depths determined by pressure profile analysis.",
        reasoning_framework=(
            "Proper unloading valve spacing is critical for efficient well unloading and transition to continuous gas lift. Valves are typically set at intervals determined by the intersection of annulus and tubing "
            "pressure gradients, ensuring that each valve opens in sequence as the well unloads. The number and spacing of unloading valves depend on well depth, deviation, and expected pressure drops. "
            "Too few valves can result in incomplete unloading, while too many increase cost and complexity. The design process is outlined in API RP 11V6 and validated by field experience. Special consideration "
            "must be given to deviated wells, where fluid holdup may affect unloading dynamics."
        ),
        key_factors=[
            "Well depth", "Pressure gradient", "Deviation", "Fluid properties",
            "Valve response time", "Unloading sequence"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Gas Lift Design Manual"
        ],
        burden_holder="Gas lift design engineer",
        adversary_position="Some propose fewer valves to reduce cost, risking incomplete unloading.",
        counter_arguments=[
            "Inadequate valve spacing leads to operational failures and increased intervention.",
            "Industry standards specify minimum spacing requirements.",
            "Field data supports the recommended design approach."
        ],
        resolution_strategy="Follow standard spacing guidelines; deviations require risk assessment and management approval.",
        entity_scope="All new gas lift installations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 7.2"
    ),
    DoctrineBlock(
        topic="Continuous vs Intermittent Gas Lift Selection",
        keywords=[
            "continuous gas lift", "intermittent gas lift", "selection criteria", "well productivity",
            "reservoir pressure", "cycle time", "liquid fallback"
        ],
        conclusion_template="Continuous gas lift is preferred for wells with moderate to high productivity, while intermittent gas lift is suitable for low-productivity or high water cut wells.",
        reasoning_framework=(
            "The choice between continuous and intermittent gas lift depends on well deliverability, fluid properties, and operational objectives. Continuous gas lift provides steady production and is more efficient "
            "for wells with sufficient reservoir pressure and productivity. Intermittent gas lift is used where continuous injection is uneconomical, typically in low-rate or high water cut wells. The selection "
            "process involves evaluating well test data, production history, and economic analysis. Intermittent gas lift may require additional equipment such as plunger lift or controllers. The doctrine is "
            "supported by API RP 11V6 and field case studies."
        ),
        key_factors=[
            "Well productivity", "Reservoir pressure", "Water cut", "Production rate",
            "Surface facility constraints", "Economic analysis"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Gas Lift Operations Handbook"
        ],
        burden_holder="Production engineer",
        adversary_position="Operators may prefer continuous lift for operational simplicity, even in marginal wells.",
        counter_arguments=[
            "Intermittent lift reduces operating cost in low-rate wells.",
            "Continuous lift may result in gas wastage and low efficiency.",
            "Field experience supports selection based on well characteristics."
        ],
        resolution_strategy="Conduct well-by-well evaluation and document selection rationale; review periodically as well conditions change.",
        entity_scope="All gas lifted wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 8.1"
    ),
    DoctrineBlock(
        topic="Gas Lift Kickoff Procedures",
        keywords=[
            "kickoff", "well startup", "gas lift", "initial injection", "well unloading",
            "startup sequence", "pressure monitoring"
        ],
        conclusion_template="Gas lift kickoff must follow a controlled sequence of pressure and flow adjustments to ensure safe and effective well startup.",
        reasoning_framework=(
            "Kickoff procedures are critical to safely initiate gas lift in a well, especially after workover or extended shut-in. The process involves gradually increasing injection gas pressure, monitoring annulus "
            "and tubing pressures, and observing valve responses. The objective is to sequentially open unloading valves and transition to continuous lift without inducing gas lock or damaging equipment. "
            "Kickoff rates and pressures must be tailored to well conditions and documented in the operating procedure. API RP 11V6 provides guidelines for standard kickoff sequences. Deviations require "
            "engineering approval and risk assessment."
        ),
        key_factors=[
            "Initial well conditions", "Injection gas pressure", "Valve response", "Startup sequence",
            "Pressure monitoring", "Safety protocols"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Company Operating Procedures"
        ],
        burden_holder="Field operations supervisor",
        adversary_position="Some may advocate for rapid pressurization to minimize downtime.",
        counter_arguments=[
            "Rapid pressurization increases risk of valve damage and gas lock.",
            "Controlled procedures reduce startup failures and safety incidents.",
            "Industry standards specify gradual pressure increases."
        ],
        resolution_strategy="Enforce standard kickoff procedures; review incidents and update procedures as needed.",
        entity_scope="All gas lifted wells during startup",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 9.2"
    ),
    DoctrineBlock(
        topic="Gas Lift Troubleshooting - Flowing Pressure Surveys",
        keywords=[
            "troubleshooting", "pressure survey", "flowing pressure", "gas lift diagnostics",
            "valve performance", "wellbore survey"
        ],
        conclusion_template="Flowing pressure surveys are the primary diagnostic tool for identifying gas lift system malfunctions and optimizing valve performance.",
        reasoning_framework=(
            "Flowing pressure surveys involve measuring annulus and tubing pressures at various depths to diagnose gas lift system performance. The data is used to identify malfunctioning valves, improper unloading, "
            "or flow restrictions. Pressure profiles are compared to design expectations to pinpoint anomalies. The method is non-invasive and provides real-time insight into well behavior. Surveys should be "
            "conducted periodically and after any intervention. The doctrine is supported by API RP 11V6 and is standard practice in gas lift operations."
        ),
        key_factors=[
            "Pressure measurement accuracy", "Survey frequency", "Valve set depths",
            "Wellbore geometry", "Data interpretation"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Company Surveillance Guidelines"
        ],
        burden_holder="Production engineer",
        adversary_position="Some may rely solely on surface data, neglecting downhole surveys.",
        counter_arguments=[
            "Surface data cannot detect downhole anomalies or valve malfunctions.",
            "Pressure surveys provide direct evidence of system performance.",
            "Industry standards require periodic surveys."
        ],
        resolution_strategy="Schedule regular flowing pressure surveys and incorporate results into optimization workflow.",
        entity_scope="All gas lifted wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 10.1"
    ),
    DoctrineBlock(
        topic="Plunger-Assisted Gas Lift",
        keywords=[
            "plunger lift", "gas lift", "plunger-assisted", "liquid loading", "intermittent lift",
            "well cleanup", "plunger operation"
        ],
        conclusion_template="Plunger-assisted gas lift is recommended for wells with severe liquid loading or where intermittent lift efficiency is low.",
        reasoning_framework=(
            "Plunger-assisted gas lift combines the benefits of plunger lift and gas lift to improve liquid removal in wells with low pressure or high water cut. The plunger acts as a piston, carrying liquid to the "
            "surface during gas injection cycles. This method is particularly effective in marginal wells where conventional gas lift struggles to remove liquids. The selection of plunger-assisted lift is based on "
            "well test data, production history, and economic analysis. The doctrine is supported by SPE technical papers and field case studies."
        ),
        key_factors=[
            "Liquid loading severity", "Well pressure", "Plunger selection", "Cycle timing",
            "Surface facility compatibility"
        ],
        primary_authority=[
            "SPE 1063", "API RP 11V6", "Plunger Lift Operations Manual"
        ],
        burden_holder="Production engineer",
        adversary_position="Some may argue for conventional gas lift due to simplicity.",
        counter_arguments=[
            "Plunger-assisted lift improves production in liquid loaded wells.",
            "Conventional gas lift may be ineffective in severe cases.",
            "Field results demonstrate increased uptime and recovery."
        ],
        resolution_strategy="Evaluate plunger-assisted lift for all wells with persistent liquid loading; document selection process.",
        entity_scope="Marginal and liquid loaded wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="SPE 1063, Section 5.2"
    ),
    DoctrineBlock(
        topic="Multi-Well Gas Allocation Optimization",
        keywords=[
            "multi-well optimization", "gas allocation", "field optimization", "gas lift",
            "production allocation", "constraint management"
        ],
        conclusion_template="Gas allocation across multiple wells must be optimized to maximize total field production within gas supply and compression constraints.",
        reasoning_framework=(
            "In fields with limited lift gas supply, allocation must be optimized to achieve the highest aggregate oil production. This involves constructing response curves for each well, modeling the effect of "
            "incremental gas on oil production, and solving a constrained optimization problem. The process must account for facility limits, compression horsepower, and contractual obligations. Optimization is "
            "performed using specialized software or spreadsheet models, and is updated as well and facility conditions change. The doctrine is supported by SPE 1063 and field optimization case studies."
        ),
        key_factors=[
            "Gas supply limit", "Well response curves", "Compression capacity",
            "Production targets", "Facility constraints"
        ],
        primary_authority=[
            "SPE 1063", "API RP 11V6", "Field Optimization Guidelines"
        ],
        burden_holder="Field production engineer",
        adversary_position="Operators may allocate gas based on historical patterns rather than optimization.",
        counter_arguments=[
            "Optimization increases total field production and economic return.",
            "Historical allocation may not reflect current well performance.",
            "Software tools facilitate rapid optimization."
        ],
        resolution_strategy="Implement regular multi-well optimization reviews; update allocation as conditions change.",
        entity_scope="Fields with multiple gas lifted wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SPE 1063, Section 6.1"
    ),
    DoctrineBlock(
        topic="Gas Lift Valve Types and Selection",
        keywords=[
            "valve types", "gas lift valve", "orifice valve", "pressure operated valve",
            "pilot operated valve", "valve selection", "well conditions"
        ],
        conclusion_template="Valve type selection must be based on well conditions, required control precision, and operational objectives.",
        reasoning_framework=(
            "Gas lift valves are available in several types, including orifice, pressure operated, and pilot operated. Orifice valves provide fixed flow and are simple and reliable, but lack control flexibility. "
            "Pressure operated valves allow for dynamic control based on annulus or tubing pressure, and are preferred for unloading and variable conditions. Pilot operated valves offer the highest precision but "
            "are more complex and costly. Selection is based on well depth, pressure regime, expected flow variation, and maintenance considerations. The doctrine is supported by API RP 11V6 and manufacturer "
            "guidelines."
        ),
        key_factors=[
            "Well depth", "Pressure regime", "Flow variation", "Maintenance requirements",
            "Cost", "Control precision"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Valve Manufacturer Datasheets"
        ],
        burden_holder="Gas lift design engineer",
        adversary_position="Some may default to orifice valves for simplicity, ignoring operational needs.",
        counter_arguments=[
            "Incorrect valve selection can lead to operational inefficiency.",
            "Pressure and pilot operated valves provide better control in complex wells.",
            "Manufacturer recommendations should be followed."
        ],
        resolution_strategy="Evaluate well conditions and operational objectives before valve selection; document rationale.",
        entity_scope="All gas lifted wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 7.3"
    ),
    DoctrineBlock(
        topic="Gas Lift System Economics and Compression",
        keywords=[
            "economics", "compression", "gas lift cost", "operating expense", "capital expense",
            "compression horsepower", "economic limit"
        ],
        conclusion_template="Gas lift system design must include a comprehensive economic analysis, including compression costs, to determine project viability and operating limits.",
        reasoning_framework=(
            "Economic analysis is essential for gas lift projects, as compression costs often dominate operating expenses. The analysis includes capital cost of compressors, fuel or power costs, maintenance, and "
            "expected production gains. The economic limit is reached when incremental oil revenue no longer covers the cost of additional gas injection. Sensitivity analysis should be performed to account for "
            "oil price volatility, gas supply constraints, and equipment reliability. The doctrine is supported by SPE 1063 and company economic guidelines."
        ),
        key_factors=[
            "Compression cost", "Oil price", "Gas supply", "Equipment reliability",
            "Production forecast", "Operating expense"
        ],
        primary_authority=[
            "SPE 1063", "Company Economic Guidelines", "API RP 11V6"
        ],
        burden_holder="Project engineer",
        adversary_position="Some may focus on maximizing production without regard to cost.",
        counter_arguments=[
            "Economic analysis ensures sustainable and profitable operations.",
            "Ignoring compression cost can result in uneconomic projects.",
            "Company guidelines require documented economic justification."
        ],
        resolution_strategy="Require economic analysis for all gas lift projects; review periodically as conditions change.",
        entity_scope="All gas lift projects",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Company Economic Guidelines, Section 3.2"
    ),
    DoctrineBlock(
        topic="Gas Lift Instability and Heading",
        keywords=[
            "instability", "heading", "gas lift", "slugging", "flow oscillation",
            "wellbore dynamics", "production fluctuation"
        ],
        conclusion_template="Gas lift system must be designed and operated to minimize instability and heading, which can reduce production and damage equipment.",
        reasoning_framework=(
            "Instability and heading in gas lift wells are characterized by oscillating flow rates, pressure surges, and production fluctuations. Causes include improper valve spacing, excessive gas injection, "
            "and wellbore geometry. Instability can lead to equipment wear, increased downtime, and reduced oil recovery. Mitigation involves optimizing valve design, adjusting injection rates, and monitoring "
            "well performance. The doctrine is supported by SPE technical papers and field experience."
        ),
        key_factors=[
            "Valve spacing", "Injection rate", "Wellbore geometry", "Production monitoring",
            "Surface facility response"
        ],
        primary_authority=[
            "SPE 1063", "API RP 11V6", "Field Operations Manual"
        ],
        burden_holder="Production engineer",
        adversary_position="Some may accept instability as unavoidable in marginal wells.",
        counter_arguments=[
            "Instability can often be mitigated with proper design and operation.",
            "Field studies show improved uptime with instability control.",
            "Equipment life is extended by reducing heading."
        ],
        resolution_strategy="Monitor for instability and implement corrective actions; review design if persistent.",
        entity_scope="All gas lifted wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="SPE 1063, Section 7.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Monitoring and Performance Tracking",
        keywords=[
            "monitoring", "performance tracking", "gas lift", "well surveillance",
            "data acquisition", "optimization", "KPI"
        ],
        conclusion_template="Continuous monitoring and performance tracking are required to ensure gas lift system efficiency and identify optimization opportunities.",
        reasoning_framework=(
            "Effective gas lift operations depend on real-time monitoring of key parameters such as injection rate, annulus and tubing pressures, and production rate. Data acquisition systems should be installed "
            "on all critical wells, and performance should be tracked using KPIs such as gas utilization efficiency and uptime. Regular analysis of trends enables early detection of problems and supports "
            "optimization efforts. The doctrine is supported by API RP 11V6 and company surveillance guidelines."
        ),
        key_factors=[
            "Data acquisition", "KPI selection", "Trend analysis", "Alarm management",
            "Optimization workflow"
        ],
        primary_authority=[
            "API RP 11V6", "Company Surveillance Guidelines", "SPE 1063"
        ],
        burden_holder="Production engineer",
        adversary_position="Some may rely on periodic manual checks, missing optimization opportunities.",
        counter_arguments=[
            "Continuous monitoring enables proactive intervention.",
            "Manual checks are insufficient for complex fields.",
            "Industry standards require automated surveillance."
        ],
        resolution_strategy="Install data acquisition on all critical wells; review performance monthly.",
        entity_scope="All gas lifted wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 11.1"
    ),
    # 28 more DoctrineBlock instances with authoritative domain content follow...
    DoctrineBlock(
        topic="Gas Lift Mandrel Selection and Placement",
        keywords=[
            "mandrel selection", "mandrel placement", "gas lift", "side pocket mandrel",
            "well completion", "valve installation"
        ],
        conclusion_template="Mandrel type and placement must be selected based on well completion type, expected intervention frequency, and valve compatibility.",
        reasoning_framework=(
            "Side pocket mandrels are preferred for most modern gas lift installations due to their compatibility with wireline-retrievable valves and ease of intervention. Conventional mandrels may be used in "
            "older wells or where cost is a primary concern. Mandrel placement is determined by the unloading sequence and pressure profile, with each mandrel set at a depth corresponding to a specific valve "
            "function. The doctrine is supported by API RP 11V6 and manufacturer recommendations."
        ),
        key_factors=[
            "Well completion type", "Intervention requirements", "Valve compatibility",
            "Pressure profile", "Cost"
        ],
        primary_authority=[
            "API RP 11V6", "SPE 1063", "Mandrel Manufacturer Datasheets"
        ],
        burden_holder="Completion engineer",
        adversary_position="Some may select conventional mandrels to reduce upfront cost.",
        counter_arguments=[
            "Side pocket mandrels reduce long-term intervention cost.",
            "Wireline retrievability improves operational flexibility.",
            "Industry standards favor side pocket mandrels."
        ],
        resolution_strategy="Default to side pocket mandrels unless justified; document selection.",
        entity_scope="All new gas lift completions",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 7.4"
    ),
    DoctrineBlock(
        topic="Gas Lift Valve Testing and Calibration",
        keywords=[
            "valve testing", "calibration", "gas lift valve", "test rack", "set pressure",
            "quality assurance"
        ],
        conclusion_template="All gas lift valves must be tested and calibrated on a test rack prior to installation to ensure correct set pressure and performance.",
        reasoning_framework=(
            "Valve testing and calibration are critical to ensure that each valve opens at the specified set pressure and operates reliably in the field. Test racks simulate well conditions and allow for precise "
            "adjustment of set points. Calibration data must be recorded and compared to manufacturer specifications. The doctrine is supported by API RP 11V6 and company QA/QC procedures."
        ),
        key_factors=[
            "Test rack accuracy", "Set pressure", "Calibration records",
            "Manufacturer specifications", "Quality control"
        ],
        primary_authority=[
            "API RP 11V6", "Company QA/QC Procedures", "Valve Manufacturer Datasheets"
        ],
        burden_holder="Valve shop supervisor",
        adversary_position="Some may skip calibration to save time, risking field failures.",
        counter_arguments=[
            "Uncalibrated valves can cause unloading failures and production loss.",
            "Calibration is a standard QA/QC requirement.",
            "Field failures are more costly than proper testing."
        ],
        resolution_strategy="Enforce mandatory valve testing and calibration; audit compliance.",
        entity_scope="All gas lift valve installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 11V6, Section 7.5"
    ),
    DoctrineBlock(
        topic="Gas Lift System Surveillance Frequency",
        keywords=[
            "surveillance", "frequency", "gas lift", "well monitoring", "data acquisition",
            "optimization"
        ],
        conclusion_template="Surveillance frequency must be determined based on well criticality, production rate, and history of operational issues.",
        reasoning_framework=(
            "Critical wells with high production rates or history of operational problems require daily or real-time surveillance, while marginal wells may be monitored weekly or monthly. Surveillance frequency "
            "should be reviewed periodically and adjusted based on performance trends and incident history. The doctrine is supported by company surveillance guidelines and industry best practices."
        ),
        key_factors=[
            "Well criticality", "Production rate", "Operational history",
            "Surveillance resources", "Incident history"
        ],
        primary_authority=[
            "Company Surveillance Guidelines", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Field surveillance coordinator",
        adversary_position="Some may standardize frequency for all wells, ignoring criticality.",
        counter_arguments=[
            "Critical wells require more frequent monitoring to prevent losses.",
            "Resource allocation should be risk-based.",
            "Industry best practices support tailored surveillance."
        ],
        resolution_strategy="Classify wells by criticality and adjust surveillance frequency accordingly.",
        entity_scope="All gas lifted wells",
        confidence=0.92,
        confidence_zone="Medium",
        controlling_precedent="Company Surveillance Guidelines, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Failure Analysis",
        keywords=[
            "failure analysis", "root cause", "gas lift", "incident investigation",
            "corrective action"
        ],
        conclusion_template="All significant gas lift system failures must be investigated using root cause analysis to prevent recurrence.",
        reasoning_framework=(
            "Failure analysis involves collecting data on the incident, interviewing personnel, and reviewing system design and operation. Root cause analysis tools such as fishbone diagrams and 5 Whys are used "
            "to identify underlying causes. Corrective actions are documented and tracked to closure. The doctrine is supported by company incident investigation procedures and industry standards."
        ),
        key_factors=[
            "Incident data", "Personnel interviews", "Design review",
            "Root cause tools", "Corrective action tracking"
        ],
        primary_authority=[
            "Company Incident Investigation Procedures", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Production supervisor",
        adversary_position="Some may address only immediate symptoms, not root causes.",
        counter_arguments=[
            "Root cause analysis prevents repeat failures.",
            "Industry standards require thorough investigation.",
            "Corrective action tracking ensures accountability."
        ],
        resolution_strategy="Enforce root cause analysis for all significant failures; audit corrective actions.",
        entity_scope="All gas lift operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Incident Investigation Procedures, Section 4.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Debottlenecking",
        keywords=[
            "debottlenecking", "system optimization", "gas lift", "facility constraints",
            "production increase"
        ],
        conclusion_template="Debottlenecking studies must be conducted periodically to identify and remove constraints limiting gas lift system performance.",
        reasoning_framework=(
            "Debottlenecking involves reviewing the entire gas lift system, including surface facilities, compression, and wellbore equipment, to identify constraints. Solutions may include compressor upgrades, "
            "pipeline modifications, or valve changes. The process is iterative and should be repeated as field conditions evolve. The doctrine is supported by field optimization guidelines and SPE case studies."
        ),
        key_factors=[
            "Facility constraints", "Compression capacity", "Wellbore equipment",
            "Production targets", "Field conditions"
        ],
        primary_authority=[
            "Field Optimization Guidelines", "SPE 1063", "API RP 11V6"
        ],
        burden_holder="Field optimization engineer",
        adversary_position="Some may accept current constraints as fixed, missing optimization opportunities.",
        counter_arguments=[
            "Debottlenecking can yield significant production gains.",
            "Constraints often change as fields mature.",
            "Industry best practices encourage periodic review."
        ],
        resolution_strategy="Schedule debottlenecking studies every 2-3 years or after major changes.",
        entity_scope="All gas lift fields",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Field Optimization Guidelines, Section 5.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Environmental Compliance",
        keywords=[
            "environmental compliance", "emissions", "gas lift", "methane", "regulations",
            "venting", "flaring"
        ],
        conclusion_template="Gas lift operations must comply with all environmental regulations regarding gas venting, flaring, and emissions.",
        reasoning_framework=(
            "Environmental compliance requires monitoring and minimizing methane emissions, venting, and flaring during gas lift operations. Operators must adhere to local, national, and international regulations, "
            "and implement best practices to reduce environmental impact. Emission data must be recorded and reported as required. The doctrine is supported by regulatory agencies and company environmental policies."
        ),
        key_factors=[
            "Emission monitoring", "Regulatory requirements", "Venting and flaring limits",
            "Reporting procedures", "Best practices"
        ],
        primary_authority=[
            "EPA Regulations", "Company Environmental Policy", "API RP 11V6"
        ],
        burden_holder="Environmental compliance officer",
        adversary_position="Some may prioritize production over strict compliance.",
        counter_arguments=[
            "Non-compliance can result in fines and reputational damage.",
            "Best practices reduce both emissions and operating cost.",
            "Regulatory agencies conduct audits and inspections."
        ],
        resolution_strategy="Implement emission monitoring and reporting; review compliance quarterly.",
        entity_scope="All gas lift operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA Regulations, Section 40 CFR 60"
    ),
    DoctrineBlock(
        topic="Gas Lift System Automation and Remote Control",
        keywords=[
            "automation", "remote control", "gas lift", "SCADA", "digital oilfield",
            "control systems"
        ],
        conclusion_template="Automation and remote control systems should be implemented on all critical gas lift wells to improve efficiency and reduce downtime.",
        reasoning_framework=(
            "Automation enables real-time adjustment of injection rates, pressure set points, and system diagnostics. SCADA systems provide remote monitoring and control, reducing the need for field visits and "
            "enabling rapid response to operational issues. Implementation should follow company digital oilfield strategy and cybersecurity guidelines. The doctrine is supported by industry case studies and "
            "company automation standards."
        ),
        key_factors=[
            "SCADA system", "Cybersecurity", "Well criticality", "Operational efficiency",
            "Downtime reduction"
        ],
        primary_authority=[
            "Company Automation Standards", "SPE 1063", "API RP 11V6"
        ],
        burden_holder="Automation engineer",
        adversary_position="Some may resist automation due to cost or change management issues.",
        counter_arguments=[
            "Automation reduces operating cost and improves uptime.",
            "Remote control enables rapid response to problems.",
            "Industry trends favor increased automation."
        ],
        resolution_strategy="Prioritize automation for critical wells; develop business case for expansion.",
        entity_scope="All critical gas lift wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Automation Standards, Section 2.3"
    ),
    DoctrineBlock(
        topic="Gas Lift System Corrosion Management",
        keywords=[
            "corrosion management", "gas lift", "chemical treatment", "corrosion monitoring",
            "annulus corrosion", "tubing corrosion"
        ],
        conclusion_template="Corrosion management programs are required for all gas lift systems, including chemical treatment and periodic monitoring.",
        reasoning_framework=(
            "Gas lift systems are susceptible to corrosion due to wet gas, CO2, and H2S. Corrosion management includes regular chemical treatment, coupon monitoring, and periodic inspection of tubing and annulus. "
            "Corrosion data must be tracked and used to adjust treatment programs. The doctrine is supported by company corrosion management guidelines and industry standards."
        ),
        key_factors=[
            "Corrosive gas content", "Chemical treatment", "Monitoring frequency",
            "Inspection records", "Corrosion rate"
        ],
        primary_authority=[
            "Company Corrosion Management Guidelines", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Corrosion engineer",
        adversary_position="Some may reduce chemical treatment to cut costs.",
        counter_arguments=[
            "Corrosion failures lead to expensive workovers.",
            "Proactive management reduces long-term cost.",
            "Industry standards require corrosion programs."
        ],
        resolution_strategy="Maintain corrosion management for all gas lift systems; audit program effectiveness.",
        entity_scope="All gas lift operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Company Corrosion Management Guidelines, Section 3.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Safety and Emergency Shutdown",
        keywords=[
            "safety", "emergency shutdown", "gas lift", "ESD", "well control",
            "process safety"
        ],
        conclusion_template="All gas lift systems must be equipped with safety and emergency shutdown (ESD) systems to ensure well control and personnel safety.",
        reasoning_framework=(
            "Safety is paramount in gas lift operations. ESD systems must be installed to shut off gas injection in the event of abnormal pressure, fire, or other emergencies. Systems must be tested regularly and "
            "maintained in accordance with company safety standards and regulatory requirements. The doctrine is supported by API RP 11V6 and process safety guidelines."
        ),
        key_factors=[
            "ESD system design", "Testing frequency", "Regulatory requirements",
            "Personnel training", "Maintenance records"
        ],
        primary_authority=[
            "Company Safety Standards", "API RP 11V6", "Process Safety Guidelines"
        ],
        burden_holder="Field safety officer",
        adversary_position="Some may delay ESD testing to avoid production interruptions.",
        counter_arguments=[
            "Regular testing ensures system reliability.",
            "Safety is a non-negotiable priority.",
            "Regulatory agencies require ESD systems."
        ],
        resolution_strategy="Test ESD systems per schedule; document and address deficiencies.",
        entity_scope="All gas lift operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Company Safety Standards, Section 5.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Training and Competency",
        keywords=[
            "training", "competency", "gas lift", "personnel qualification",
            "operations training", "certification"
        ],
        conclusion_template="All personnel involved in gas lift operations must complete training and demonstrate competency in relevant procedures and safety practices.",
        reasoning_framework=(
            "Training ensures that personnel understand gas lift system operation, safety protocols, and emergency procedures. Competency must be demonstrated through assessment and periodic refresher courses. "
            "Records of training and certification must be maintained. The doctrine is supported by company HR policies and industry standards."
        ),
        key_factors=[
            "Training curriculum", "Competency assessment", "Refresher frequency",
            "Certification records", "Safety practices"
        ],
        primary_authority=[
            "Company HR Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Operations manager",
        adversary_position="Some may allow untrained personnel to operate equipment due to staffing shortages.",
        counter_arguments=[
            "Untrained personnel increase risk of incidents.",
            "Training reduces operational errors and downtime.",
            "Industry standards require documented competency."
        ],
        resolution_strategy="Enforce training requirements and maintain records; audit compliance.",
        entity_scope="All gas lift personnel",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Company HR Policy, Section 8.2"
    ),
    DoctrineBlock(
        topic="Gas Lift System Data Management",
        keywords=[
            "data management", "gas lift", "data integrity", "historian", "data retention",
            "data analysis"
        ],
        conclusion_template="All gas lift system data must be stored in a secure, accessible historian with appropriate retention and backup policies.",
        reasoning_framework=(
            "Data integrity and accessibility are essential for effective gas lift optimization and troubleshooting. Data must be stored in a central historian, with regular backups and access controls. Retention "
            "policies must comply with company and regulatory requirements. The doctrine is supported by company IT and data management policies."
        ),
        key_factors=[
            "Historian system", "Backup frequency", "Access control",
            "Retention policy", "Data integrity"
        ],
        primary_authority=[
            "Company IT Policy", "API RP 11V6", "Data Management Guidelines"
        ],
        burden_holder="IT manager",
        adversary_position="Some may store data locally, risking loss or inaccessibility.",
        counter_arguments=[
            "Centralized data enables analysis and optimization.",
            "Local storage is vulnerable to loss.",
            "Regulatory agencies require data retention."
        ],
        resolution_strategy="Store all data in historian; audit compliance and backup.",
        entity_scope="All gas lift operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company IT Policy, Section 6.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Change Management",
        keywords=[
            "change management", "gas lift", "MOC", "modification", "engineering change",
            "risk assessment"
        ],
        conclusion_template="All changes to gas lift system design or operation must follow the Management of Change (MOC) process, including risk assessment and documentation.",
        reasoning_framework=(
            "Change management ensures that modifications to gas lift systems are reviewed, risks are assessed, and documentation is updated. The MOC process includes engineering review, stakeholder approval, "
            "and communication of changes to affected personnel. The doctrine is supported by company MOC policy and industry standards."
        ),
        key_factors=[
            "MOC process", "Risk assessment", "Stakeholder approval",
            "Documentation update", "Communication"
        ],
        primary_authority=[
            "Company MOC Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Project manager",
        adversary_position="Some may bypass MOC for minor changes, increasing risk.",
        counter_arguments=[
            "Unmanaged changes can lead to incidents.",
            "MOC ensures all risks are considered.",
            "Industry standards require documented MOC."
        ],
        resolution_strategy="Enforce MOC for all changes; audit compliance.",
        entity_scope="All gas lift operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Company MOC Policy, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Well Integrity Management",
        keywords=[
            "well integrity", "gas lift", "annulus monitoring", "pressure testing",
            "well barrier", "leak detection"
        ],
        conclusion_template="Well integrity must be maintained through regular annulus pressure monitoring, pressure testing, and leak detection.",
        reasoning_framework=(
            "Well integrity is critical to safe and reliable gas lift operations. Regular monitoring of annulus pressure, periodic pressure testing, and leak detection surveys are required. Any anomalies must be "
            "investigated and remediated promptly. The doctrine is supported by company well integrity standards and API RP 11V6."
        ),
        key_factors=[
            "Annulus pressure monitoring", "Pressure testing", "Leak detection",
            "Remediation procedures", "Well barrier verification"
        ],
        primary_authority=[
            "Company Well Integrity Standards", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Well integrity engineer",
        adversary_position="Some may reduce monitoring frequency to save cost.",
        counter_arguments=[
            "Integrity failures can lead to catastrophic incidents.",
            "Proactive monitoring prevents loss of containment.",
            "Industry standards require regular testing."
        ],
        resolution_strategy="Follow well integrity program; escalate anomalies for investigation.",
        entity_scope="All gas lift wells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Company Well Integrity Standards, Section 4.2"
    ),
    DoctrineBlock(
        topic="Gas Lift System Optimization Workflow",
        keywords=[
            "optimization workflow", "gas lift", "continuous improvement", "production optimization",
            "workflow automation"
        ],
        conclusion_template="A structured optimization workflow must be implemented for all gas lift systems, including data collection, analysis, and action tracking.",
        reasoning_framework=(
            "Optimization is an ongoing process involving data collection, analysis, identification of opportunities, and implementation of actions. Workflow automation tools can streamline the process and ensure "
            "accountability. The doctrine is supported by company optimization guidelines and industry best practices."
        ),
        key_factors=[
            "Data collection", "Analysis tools", "Action tracking",
            "Workflow automation", "Continuous improvement"
        ],
        primary_authority=[
            "Company Optimization Guidelines", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Optimization engineer",
        adversary_position="Some may rely on ad hoc optimization, missing systematic gains.",
        counter_arguments=[
            "Structured workflow ensures all opportunities are captured.",
            "Automation improves efficiency and accountability.",
            "Industry best practices favor structured processes."
        ],
        resolution_strategy="Implement and maintain structured workflow; review effectiveness annually.",
        entity_scope="All gas lift operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Optimization Guidelines, Section 1.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Communication and Handover",
        keywords=[
            "communication", "handover", "gas lift", "shift change", "operations log",
            "information transfer"
        ],
        conclusion_template="Effective communication and handover procedures are required at all shift changes and operational handovers to ensure continuity and safety.",
        reasoning_framework=(
            "Handover procedures must include a review of current well status, outstanding actions, and any abnormal conditions. Operations logs should be updated and reviewed by incoming personnel. The doctrine "
            "is supported by company operations procedures and industry standards."
        ),
        key_factors=[
            "Handover checklist", "Operations log", "Abnormal condition reporting",
            "Shift change protocol", "Information transfer"
        ],
        primary_authority=[
            "Company Operations Procedures", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Operations supervisor",
        adversary_position="Some may conduct informal handovers, risking missed information.",
        counter_arguments=[
            "Formal handover reduces risk of incidents.",
            "Operations logs ensure accountability.",
            "Industry standards require documented handover."
        ],
        resolution_strategy="Enforce handover procedures and maintain logs; audit compliance.",
        entity_scope="All gas lift operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Operations Procedures, Section 3.2"
    ),
    DoctrineBlock(
        topic="Gas Lift System Documentation and Record Keeping",
        keywords=[
            "documentation", "record keeping", "gas lift", "design records", "maintenance logs",
            "regulatory compliance"
        ],
        conclusion_template="All gas lift system design, operation, and maintenance records must be maintained and accessible for regulatory and operational review.",
        reasoning_framework=(
            "Documentation is essential for regulatory compliance, troubleshooting, and continuous improvement. Records must include design calculations, maintenance logs, calibration certificates, and incident "
            "reports. Documents should be stored in a central repository with appropriate access controls. The doctrine is supported by company documentation policy and regulatory requirements."
        ),
        key_factors=[
            "Design records", "Maintenance logs", "Calibration certificates",
            "Incident reports", "Access control"
        ],
        primary_authority=[
            "Company Documentation Policy", "API RP 11V6", "Regulatory Requirements"
        ],
        burden_holder="Document controller",
        adversary_position="Some may keep incomplete or inaccessible records.",
        counter_arguments=[
            "Complete records support troubleshooting and audits.",
            "Regulators require documentation for compliance.",
            "Centralized records improve efficiency."
        ],
        resolution_strategy="Maintain all records in central repository; audit completeness annually.",
        entity_scope="All gas lift operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Company Documentation Policy, Section 7.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Spare Parts Management",
        keywords=[
            "spare parts", "inventory", "gas lift", "valve stock", "critical spares",
            "supply chain"
        ],
        conclusion_template="Critical spare parts for gas lift systems must be identified, stocked, and managed to ensure operational continuity.",
        reasoning_framework=(
            "Spare parts management includes identifying critical components such as valves, mandrels, and controllers, maintaining minimum stock levels, and tracking inventory. Supply chain lead times must be "
            "considered to avoid production interruptions. The doctrine is supported by company supply chain policy and industry best practices."
        ),
        key_factors=[
            "Criticality assessment", "Stock levels", "Inventory tracking",
            "Lead time", "Supply chain reliability"
        ],
        primary_authority=[
            "Company Supply Chain Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Materials manager",
        adversary_position="Some may minimize inventory to reduce cost, risking downtime.",
        counter_arguments=[
            "Lack of spares leads to extended downtime.",
            "Inventory management balances cost and risk.",
            "Industry standards require critical spares."
        ],
        resolution_strategy="Maintain critical spares inventory; review stock levels quarterly.",
        entity_scope="All gas lift operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Supply Chain Policy, Section 4.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Regulatory Reporting",
        keywords=[
            "regulatory reporting", "gas lift", "compliance", "emissions reporting",
            "production reporting"
        ],
        conclusion_template="All required regulatory reports for gas lift operations, including emissions and production, must be submitted accurately and on time.",
        reasoning_framework=(
            "Regulatory reporting is a legal requirement and includes emissions, production, and incident reports. Reports must be accurate, timely, and comply with all applicable regulations. Failure to report "
            "can result in fines and operational restrictions. The doctrine is supported by regulatory agency requirements and company compliance policy."
        ),
        key_factors=[
            "Reporting deadlines", "Data accuracy", "Regulatory requirements",
            "Compliance tracking", "Audit readiness"
        ],
        primary_authority=[
            "Regulatory Agency Requirements", "Company Compliance Policy", "API RP 11V6"
        ],
        burden_holder="Compliance officer",
        adversary_position="Some may delay or under-report to avoid scrutiny.",
        counter_arguments=[
            "Accurate reporting is a legal obligation.",
            "Non-compliance risks fines and license suspension.",
            "Company policy mandates full compliance."
        ],
        resolution_strategy="Track reporting deadlines and audit submissions; escalate non-compliance.",
        entity_scope="All gas lift operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Regulatory Agency Requirements, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Field Testing and Pilot Projects",
        keywords=[
            "field testing", "pilot project", "gas lift", "new technology", "validation",
            "performance evaluation"
        ],
        conclusion_template="All new gas lift technologies or methods must be validated through field testing or pilot projects before full-scale implementation.",
        reasoning_framework=(
            "Field testing and pilot projects provide real-world validation of new gas lift technologies, methods, or equipment. Performance data is collected and analyzed to assess benefits and risks. Only after "
            "successful validation should new approaches be adopted field-wide. The doctrine is supported by company technology management policy and industry best practices."
        ),
        key_factors=[
            "Pilot design", "Performance metrics", "Risk assessment",
            "Data analysis", "Scale-up criteria"
        ],
        primary_authority=[
            "Company Technology Management Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Technology manager",
        adversary_position="Some may bypass pilots to accelerate implementation.",
        counter_arguments=[
            "Pilots reduce risk of large-scale failures.",
            "Data-driven validation supports decision making.",
            "Industry standards require pilot validation."
        ],
        resolution_strategy="Require pilot projects for all new technologies; document results and lessons learned.",
        entity_scope="All gas lift operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Technology Management Policy, Section 5.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Vendor Qualification",
        keywords=[
            "vendor qualification", "gas lift", "supplier evaluation", "quality assurance",
            "approved vendor list"
        ],
        conclusion_template="All gas lift equipment vendors must be qualified and included on the approved vendor list prior to procurement.",
        reasoning_framework=(
            "Vendor qualification ensures that all supplied equipment meets company quality, safety, and performance standards. The process includes evaluation of technical capability, quality systems, and past "
            "performance. Only qualified vendors are included on the approved vendor list. The doctrine is supported by company procurement policy and industry standards."
        ),
        key_factors=[
            "Technical evaluation", "Quality system review", "Performance history",
            "Approved vendor list", "Procurement policy"
        ],
        primary_authority=[
            "Company Procurement Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Procurement manager",
        adversary_position="Some may use unqualified vendors to reduce cost.",
        counter_arguments=[
            "Unqualified vendors increase risk of equipment failure.",
            "Quality assurance protects long-term performance.",
            "Company policy mandates vendor qualification."
        ],
        resolution_strategy="Procure only from approved vendors; review vendor list annually.",
        entity_scope="All gas lift equipment procurement",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Company Procurement Policy, Section 3.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Well Testing and Allocation",
        keywords=[
            "well testing", "allocation", "gas lift", "production testing", "test separator",
            "allocation factor"
        ],
        conclusion_template="Regular well testing is required to allocate production accurately and optimize gas lift system performance.",
        reasoning_framework=(
            "Well testing provides data on individual well performance, enabling accurate allocation of production and optimization of gas lift parameters. Tests should be conducted using a test separator and "
            "allocation factors updated accordingly. The doctrine is supported by company production allocation policy and industry standards."
        ),
        key_factors=[
            "Test frequency", "Test separator", "Allocation factor",
            "Data accuracy", "Optimization input"
        ],
        primary_authority=[
            "Company Production Allocation Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Production engineer",
        adversary_position="Some may reduce test frequency to save cost.",
        counter_arguments=[
            "Accurate allocation supports optimization and compliance.",
            "Test data identifies underperforming wells.",
            "Industry standards require regular testing."
        ],
        resolution_strategy="Follow test schedule; review allocation factors after each test.",
        entity_scope="All gas lift wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Production Allocation Policy, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Maintenance Planning",
        keywords=[
            "maintenance planning", "gas lift", "preventive maintenance", "maintenance schedule",
            "workover planning"
        ],
        conclusion_template="Preventive maintenance plans must be developed and followed for all gas lift systems to minimize unplanned downtime.",
        reasoning_framework=(
            "Preventive maintenance includes scheduled inspection, testing, and replacement of critical components such as valves, mandrels, and controllers. Maintenance plans should be risk-based and reviewed "
            "annually. The doctrine is supported by company maintenance policy and industry best practices."
        ),
        key_factors=[
            "Maintenance schedule", "Risk assessment", "Component criticality",
            "Workover planning", "Maintenance records"
        ],
        primary_authority=[
            "Company Maintenance Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Maintenance planner",
        adversary_position="Some may rely on reactive maintenance, increasing downtime.",
        counter_arguments=[
            "Preventive maintenance reduces unplanned failures.",
            "Risk-based planning optimizes resource use.",
            "Industry standards require maintenance plans."
        ],
        resolution_strategy="Develop and follow maintenance plans; review effectiveness annually.",
        entity_scope="All gas lift operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Company Maintenance Policy, Section 6.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Well Intervention Planning",
        keywords=[
            "well intervention", "planning", "gas lift", "wireline", "workover",
            "intervention schedule"
        ],
        conclusion_template="Well intervention plans must be developed for all gas lift wells, including wireline and workover activities.",
        reasoning_framework=(
            "Well intervention planning ensures that required activities such as valve replacement, mandrel inspection, and remedial work are scheduled and executed efficiently. Plans should be risk-based and "
            "coordinated with production and maintenance schedules. The doctrine is supported by company intervention policy and industry best practices."
        ),
        key_factors=[
            "Intervention schedule", "Risk assessment", "Resource allocation",
            "Coordination with production", "Workover planning"
        ],
        primary_authority=[
            "Company Intervention Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Intervention planner",
        adversary_position="Some may delay interventions to minimize cost.",
        counter_arguments=[
            "Timely intervention prevents production loss.",
            "Risk-based planning optimizes resource use.",
            "Industry standards require intervention plans."
        ],
        resolution_strategy="Develop and follow intervention plans; review annually.",
        entity_scope="All gas lift wells",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Intervention Policy, Section 3.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Continuous Improvement",
        keywords=[
            "continuous improvement", "gas lift", "lessons learned", "best practices",
            "performance review"
        ],
        conclusion_template="Continuous improvement programs must be implemented for all gas lift operations, including lessons learned and best practice sharing.",
        reasoning_framework=(
            "Continuous improvement involves regular performance review, documentation of lessons learned, and sharing of best practices across teams. Programs should include periodic workshops and performance "
            "benchmarking. The doctrine is supported by company continuous improvement policy and industry standards."
        ),
        key_factors=[
            "Performance review", "Lessons learned", "Best practice sharing",
            "Workshops", "Benchmarking"
        ],
        primary_authority=[
            "Company Continuous Improvement Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Continuous improvement coordinator",
        adversary_position="Some may view improvement programs as non-essential.",
        counter_arguments=[
            "Continuous improvement drives long-term performance gains.",
            "Lessons learned prevent repeat mistakes.",
            "Industry standards encourage best practice sharing."
        ],
        resolution_strategy="Implement improvement programs and track participation.",
        entity_scope="All gas lift operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Continuous Improvement Policy, Section 1.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Stakeholder Engagement",
        keywords=[
            "stakeholder engagement", "gas lift", "communication", "cross-functional team",
            "project alignment"
        ],
        conclusion_template="Stakeholder engagement is required for all major gas lift projects to ensure alignment and effective communication.",
        reasoning_framework=(
            "Engagement of all stakeholders, including operations, engineering, maintenance, and management, ensures project alignment and addresses potential issues early. Regular meetings and communication plans "
            "are essential. The doctrine is supported by company project management policy and industry best practices."
        ),
        key_factors=[
            "Stakeholder identification", "Communication plan", "Meeting schedule",
            "Issue tracking", "Project alignment"
        ],
        primary_authority=[
            "Company Project Management Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Project manager",
        adversary_position="Some may limit engagement to core team, missing broader input.",
        counter_arguments=[
            "Broad engagement identifies risks and opportunities.",
            "Effective communication prevents misunderstandings.",
            "Industry standards require stakeholder engagement."
        ],
        resolution_strategy="Develop and follow stakeholder engagement plan for all projects.",
        entity_scope="All major gas lift projects",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Project Management Policy, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Technology Assessment",
        keywords=[
            "technology assessment", "gas lift", "innovation", "emerging technology",
            "technology review"
        ],
        conclusion_template="Periodic technology assessments must be conducted to evaluate emerging gas lift technologies and their applicability.",
        reasoning_framework=(
            "Technology assessment involves reviewing new developments in gas lift equipment, control systems, and optimization tools. Assessments should consider technical, economic, and operational impacts. "
            "The doctrine is supported by company technology management policy and industry best practices."
        ),
        key_factors=[
            "Emerging technology", "Technical evaluation", "Economic analysis",
            "Operational impact", "Implementation plan"
        ],
        primary_authority=[
            "Company Technology Management Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Technology manager",
        adversary_position="Some may resist new technology due to risk or cost.",
        counter_arguments=[
            "Assessment identifies opportunities for improvement.",
            "Structured review reduces implementation risk.",
            "Industry standards encourage technology assessment."
        ],
        resolution_strategy="Conduct technology assessments every 2-3 years; document findings.",
        entity_scope="All gas lift operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Company Technology Management Policy, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Cost Tracking and Benchmarking",
        keywords=[
            "cost tracking", "benchmarking", "gas lift", "operating expense", "cost analysis",
            "performance benchmarking"
        ],
        conclusion_template="Operating costs for gas lift systems must be tracked and benchmarked against industry standards to identify improvement opportunities.",
        reasoning_framework=(
            "Cost tracking includes monitoring of compression, maintenance, and intervention expenses. Benchmarking against industry peers identifies areas for improvement. The doctrine is supported by company "
            "cost management policy and industry best practices."
        ),
        key_factors=[
            "Cost tracking system", "Benchmarking data", "Expense categories",
            "Improvement identification", "Reporting"
        ],
        primary_authority=[
            "Company Cost Management Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Cost analyst",
        adversary_position="Some may not track costs at sufficient detail.",
        counter_arguments=[
            "Detailed tracking supports optimization.",
            "Benchmarking identifies competitive gaps.",
            "Industry standards require cost analysis."
        ],
        resolution_strategy="Implement cost tracking and benchmarking; review results annually.",
        entity_scope="All gas lift operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Cost Management Policy, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Risk Management",
        keywords=[
            "risk management", "gas lift", "risk assessment", "mitigation", "risk register",
            "operational risk"
        ],
        conclusion_template="Comprehensive risk management programs are required for all gas lift operations, including risk assessment and mitigation tracking.",
        reasoning_framework=(
            "Risk management involves identifying, assessing, and mitigating operational risks associated with gas lift systems. A risk register should be maintained and reviewed regularly. The doctrine is "
            "supported by company risk management policy and industry standards."
        ),
        key_factors=[
            "Risk identification", "Risk assessment", "Mitigation tracking",
            "Risk register", "Review frequency"
        ],
        primary_authority=[
            "Company Risk Management Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Risk manager",
        adversary_position="Some may view risk management as a formality.",
        counter_arguments=[
            "Structured risk management prevents incidents.",
            "Mitigation tracking ensures accountability.",
            "Industry standards require risk programs."
        ],
        resolution_strategy="Maintain risk register and review quarterly; update mitigation actions.",
        entity_scope="All gas lift operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Risk Management Policy, Section 1.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Audit and Compliance",
        keywords=[
            "audit", "compliance", "gas lift", "internal audit", "regulatory audit",
            "compliance tracking"
        ],
        conclusion_template="Regular audits are required to ensure compliance with company and regulatory requirements for gas lift operations.",
        reasoning_framework=(
            "Audits include review of documentation, operational practices, and compliance with standards. Findings must be documented and corrective actions tracked to closure. The doctrine is supported by "
            "company audit policy and regulatory requirements."
        ),
        key_factors=[
            "Audit schedule", "Documentation review", "Compliance tracking",
            "Corrective action", "Regulatory requirements"
        ],
        primary_authority=[
            "Company Audit Policy", "API RP 11V6", "Regulatory Requirements"
        ],
        burden_holder="Audit coordinator",
        adversary_position="Some may view audits as non-value-adding.",
        counter_arguments=[
            "Audits identify gaps and drive improvement.",
            "Compliance is a legal requirement.",
            "Industry standards require regular audits."
        ],
        resolution_strategy="Follow audit schedule; track findings and corrective actions.",
        entity_scope="All gas lift operations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Company Audit Policy, Section 3.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Incident Reporting",
        keywords=[
            "incident reporting", "gas lift", "near miss", "accident", "root cause analysis",
            "incident investigation"
        ],
        conclusion_template="All incidents and near misses in gas lift operations must be reported, investigated, and tracked to closure.",
        reasoning_framework=(
            "Incident reporting is essential for safety and continuous improvement. All incidents, including near misses, must be documented and investigated. Root cause analysis is required, and corrective actions "
            "must be tracked. The doctrine is supported by company safety policy and regulatory requirements."
        ),
        key_factors=[
            "Incident documentation", "Root cause analysis", "Corrective action tracking",
            "Near miss reporting", "Closure verification"
        ],
        primary_authority=[
            "Company Safety Policy", "API RP 11V6", "Regulatory Requirements"
        ],
        burden_holder="Safety officer",
        adversary_position="Some may under-report to avoid scrutiny.",
        counter_arguments=[
            "Accurate reporting improves safety.",
            "Root cause analysis prevents recurrence.",
            "Regulatory agencies require incident reporting."
        ],
        resolution_strategy="Enforce reporting and investigation; audit compliance.",
        entity_scope="All gas lift operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Company Safety Policy, Section 4.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Sustainability and Energy Efficiency",
        keywords=[
            "sustainability", "energy efficiency", "gas lift", "carbon footprint",
            "energy management"
        ],
        conclusion_template="Sustainability and energy efficiency must be considered in all gas lift system designs and operations.",
        reasoning_framework=(
            "Energy efficiency reduces operating cost and environmental impact. Sustainability initiatives include minimizing compression energy, optimizing gas usage, and reducing emissions. The doctrine is "
            "supported by company sustainability policy and industry best practices."
        ),
        key_factors=[
            "Energy consumption", "Emission reduction", "Sustainability initiatives",
            "Design optimization", "Performance tracking"
        ],
        primary_authority=[
            "Company Sustainability Policy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Sustainability officer",
        adversary_position="Some may prioritize production over efficiency.",
        counter_arguments=[
            "Efficiency reduces cost and environmental impact.",
            "Sustainability is increasingly required by stakeholders.",
            "Industry standards encourage efficiency."
        ],
        resolution_strategy="Incorporate efficiency metrics in design and operation; review annually.",
        entity_scope="All gas lift operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Company Sustainability Policy, Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift System Digitalization and Analytics",
        keywords=[
            "digitalization", "analytics", "gas lift", "data science", "predictive analytics",
            "digital oilfield"
        ],
        conclusion_template="Digitalization and advanced analytics should be leveraged to enhance gas lift system optimization and predictive maintenance.",
        reasoning_framework=(
            "Digitalization enables integration of data from multiple sources for advanced analytics, including predictive maintenance and optimization. Machine learning models can identify patterns and predict "
            "failures before they occur. The doctrine is supported by company digital oilfield strategy and industry case studies."
        ),
        key_factors=[
            "Data integration", "Analytics tools", "Predictive models",
            "Optimization algorithms", "Digital oilfield strategy"
        ],
        primary_authority=[
            "Company Digital Oilfield Strategy", "API RP 11V6", "SPE 1063"
        ],
        burden_holder="Digitalization lead",
        adversary_position="Some may resist digitalization due to cost or complexity.",
        counter_arguments=[
            "Analytics improves uptime and performance.",
            "Predictive models reduce unplanned failures.",
            "Industry trends favor digitalization."
        ],
        resolution_strategy="Develop digitalization roadmap and analytics use cases.",
        entity_scope="All gas lift operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Company Digital Oilfield Strategy, Section 1.1"
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