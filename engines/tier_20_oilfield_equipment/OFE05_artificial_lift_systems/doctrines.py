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
        topic="Beam Pump Selection and Sizing",
        keywords=["beam pump", "artificial lift", "pump sizing", "well productivity", "stroke length", "pump capacity"],
        conclusion_template="Select and size beam pump based on reservoir deliverability, production targets, and mechanical constraints.",
        reasoning_framework=(
            "Beam pump selection and sizing is governed by the interplay between reservoir inflow performance, "
            "desired production rate, and mechanical limitations of the pumping system. The process begins with "
            "calculating the expected fluid production rate using inflow performance relationships (IPR) and "
            "matching this to the pump's volumetric capacity. Stroke length, pump diameter, and strokes per minute "
            "are optimized to maximize efficiency while minimizing rod load and surface unit stress. The selection "
            "must account for produced fluid characteristics, depth, and tubing size. API 11E and 11L standards "
            "provide guidelines for component ratings and operational envelopes. The sizing process incorporates "
            "pump-off controllers and considers potential gas interference, sand production, and corrosion. "
            "Economic evaluation is performed to ensure lifecycle cost effectiveness. The final selection is "
            "validated against historical well performance and field precedent."
        ),
        key_factors=[
            "Reservoir inflow performance",
            "Production rate targets",
            "Pump stroke length and diameter",
            "Rod string load limits",
            "Surface unit geometry",
            "Fluid properties (viscosity, gas content)",
            "Tubing size",
            "API 11E/11L standards"
        ],
        primary_authority=[
            "API 11E: Specification for Pumping Units",
            "API 11L: Specification for Rods and Pumps",
            "SPE Monograph: Artificial Lift Design"
        ],
        burden_holder="Production Engineer",
        adversary_position="Pump selection may be oversized or undersized, leading to inefficiency or mechanical failure.",
        counter_arguments=[
            "Oversizing increases capital and operational costs.",
            "Undersizing results in suboptimal production and frequent pump-off.",
            "Ignoring fluid properties leads to premature wear."
        ],
        resolution_strategy="Iterative sizing using field data, simulation, and adherence to API standards.",
        entity_scope="Oil and gas wells utilizing beam pumps",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 11E/11L, SPE Artificial Lift Guidelines"
    ),
    DoctrineBlock(
        topic="Dynamometer Card Analysis",
        keywords=["dynamometer", "pump diagnostics", "surface card", "downhole card", "pump efficiency", "load profile"],
        conclusion_template="Interpret dynamometer cards to diagnose beam pump performance and identify failure modes.",
        reasoning_framework=(
            "Dynamometer card analysis is a diagnostic tool for beam pump systems, using load vs. position data "
            "to evaluate pump operation. Surface and downhole cards are compared to detect anomalies such as gas "
            "interference, fluid pound, or rod/tubing friction. The shape of the card reveals pump fill efficiency, "
            "mechanical integrity, and system balance. Interpretation follows API guidelines and leverages historical "
            "card libraries. Advanced analysis includes pattern recognition and statistical correlation with failure "
            "events. Remediation strategies are developed based on card findings, including adjusting stroke length, "
            "changing pump size, or implementing pump-off controllers. The process is iterative, with periodic card "
            "collection to monitor trends and validate corrective actions."
        ),
        key_factors=[
            "Card shape and area",
            "Surface vs. downhole comparison",
            "Pump fill efficiency",
            "Load distribution",
            "Historical card patterns",
            "API dynamometer standards"
        ],
        primary_authority=[
            "API RP 11L: Recommended Practice for Pump Analysis",
            "SPE Technical Paper: Dynamometer Card Interpretation"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Card interpretation may be subjective and lead to misdiagnosis.",
        counter_arguments=[
            "Pattern recognition may be confounded by multi-factor anomalies.",
            "Surface card may not reflect downhole conditions due to rod stretch.",
            "Data quality issues can obscure true failure modes."
        ],
        resolution_strategy="Combine card analysis with physical inspection and production data.",
        entity_scope="Beam pump operated wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 11L, SPE Card Analysis Best Practices"
    ),
    DoctrineBlock(
        topic="ESP Selection and Sizing",
        keywords=["ESP", "electric submersible pump", "pump sizing", "well productivity", "motor rating", "stage selection"],
        conclusion_template="Select and size ESP based on well inflow, fluid properties, and operational constraints.",
        reasoning_framework=(
            "ESP selection and sizing involves matching the pump's capacity and head to the well's production "
            "requirements and fluid characteristics. The process starts with inflow performance analysis, followed "
            "by pump curve evaluation to determine the number of stages and motor horsepower needed. Fluid viscosity, "
            "gas content, and solids are considered to prevent pump damage and optimize efficiency. The selection "
            "must comply with API 11B standards and manufacturer recommendations. Motor cooling, cable sizing, and "
            "downhole temperature limits are assessed to ensure reliability. Economic analysis includes power costs, "
            "equipment longevity, and maintenance intervals. The final selection is validated through simulation and "
            "historical ESP performance in similar wells."
        ),
        key_factors=[
            "Well inflow performance",
            "Pump curve matching",
            "Fluid viscosity and gas content",
            "Motor horsepower and cooling",
            "Stage selection",
            "Cable and voltage rating",
            "API 11B standards"
        ],
        primary_authority=[
            "API 11B: Specification for ESP Systems",
            "SPE ESP Design Handbook"
        ],
        burden_holder="Artificial Lift Engineer",
        adversary_position="ESP may be undersized or oversized, leading to inefficiency or premature failure.",
        counter_arguments=[
            "Undersized ESP cannot meet production targets.",
            "Oversized ESP increases power consumption and costs.",
            "Ignoring gas content leads to gas lock and pump damage."
        ],
        resolution_strategy="Iterative sizing with simulation and field validation.",
        entity_scope="Oil and gas wells utilizing ESPs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Guidelines"
    ),
    DoctrineBlock(
        topic="ESP Failure Analysis",
        keywords=["ESP failure", "root cause", "pump diagnostics", "motor burnout", "gas lock", "solids damage"],
        conclusion_template="Conduct root cause analysis for ESP failures and recommend corrective actions.",
        reasoning_framework=(
            "ESP failure analysis is a systematic process to identify the underlying causes of pump malfunction. "
            "Common failure modes include motor burnout, gas lock, solids abrasion, and cable faults. The analysis "
            "begins with production data review, followed by inspection of failed components and comparison with "
            "historical failure patterns. Diagnostic tools such as vibration monitoring, electrical testing, and "
            "downhole video are employed. Recommendations are formulated based on root cause findings, including "
            "design changes, operational adjustments, and preventive maintenance schedules. The process is governed "
            "by API 11B and manufacturer failure reporting standards."
        ),
        key_factors=[
            "Failure mode identification",
            "Production data trends",
            "Component inspection",
            "Diagnostic tool results",
            "Historical failure patterns",
            "API 11B failure reporting"
        ],
        primary_authority=[
            "API 11B: ESP Failure Reporting",
            "SPE ESP Reliability Studies"
        ],
        burden_holder="Reliability Engineer",
        adversary_position="Failure analysis may overlook multi-factor causes or external influences.",
        counter_arguments=[
            "Single cause attribution may miss systemic issues.",
            "Data gaps can obscure true failure mechanisms.",
            "Manufacturer bias in failure reporting."
        ],
        resolution_strategy="Comprehensive root cause analysis with cross-functional review.",
        entity_scope="ESP operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Reliability"
    ),
    DoctrineBlock(
        topic="Gas Lift Valve Spacing and Design",
        keywords=["gas lift", "valve spacing", "artificial lift", "injection pressure", "design optimization"],
        conclusion_template="Design gas lift valve spacing to optimize injection efficiency and production rate.",
        reasoning_framework=(
            "Gas lift valve spacing and design is based on the well's injection pressure profile, production rate, "
            "and depth. The process involves calculating the optimal placement of valves to ensure efficient gas "
            "injection and minimize backpressure. Valve opening pressures are set using API 11V guidelines and "
            "manufacturer specifications. The design accounts for variable injection rates, fluid properties, and "
            "well trajectory. Simulation tools are used to model gas injection performance and validate spacing. "
            "Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Injection pressure profile",
            "Valve opening pressure",
            "Production rate",
            "Well depth and trajectory",
            "Fluid properties",
            "API 11V standards"
        ],
        primary_authority=[
            "API 11V: Gas Lift Valve Specification",
            "SPE Gas Lift Design Manual"
        ],
        burden_holder="Gas Lift Engineer",
        adversary_position="Incorrect valve spacing reduces lift efficiency and increases operational costs.",
        counter_arguments=[
            "Overly tight spacing increases equipment costs.",
            "Wide spacing reduces injection control.",
            "Ignoring well trajectory leads to uneven injection."
        ],
        resolution_strategy="Simulation and field validation of valve placement.",
        entity_scope="Gas lift operated wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 11V, SPE Gas Lift Design"
    ),
    DoctrineBlock(
        topic="Progressive Cavity Pump (PCP) Applications",
        keywords=["PCP", "progressive cavity pump", "artificial lift", "heavy oil", "sand tolerance", "pump selection"],
        conclusion_template="Apply PCPs in wells with heavy oil, sand production, and low gas content.",
        reasoning_framework=(
            "Progressive cavity pumps are selected for wells producing heavy oil, sand-laden fluids, and low gas "
            "content. PCPs offer high tolerance to solids and abrasive materials, making them ideal for unconsolidated "
            "reservoirs. The selection process evaluates fluid viscosity, sand concentration, and well depth. Pump "
            "geometry and elastomer selection are optimized to minimize wear and maximize efficiency. PCP sizing "
            "follows API 11AX standards and manufacturer guidelines. Operational strategies include variable speed "
            "drives and periodic maintenance to address elastomer degradation. Economic evaluation considers pump "
            "longevity and maintenance intervals."
        ),
        key_factors=[
            "Fluid viscosity",
            "Sand concentration",
            "Well depth",
            "Pump geometry",
            "Elastomer selection",
            "API 11AX standards"
        ],
        primary_authority=[
            "API 11AX: PCP Specification",
            "SPE PCP Application Guidelines"
        ],
        burden_holder="Production Engineer",
        adversary_position="PCP may fail prematurely in high gas or extreme abrasive environments.",
        counter_arguments=[
            "High gas content causes pump cavitation.",
            "Extreme abrasives accelerate elastomer wear.",
            "Incorrect sizing reduces efficiency."
        ],
        resolution_strategy="Field testing and periodic maintenance.",
        entity_scope="PCP operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11AX, SPE PCP Guidelines"
    ),
    DoctrineBlock(
        topic="Plunger Lift Systems",
        keywords=["plunger lift", "artificial lift", "gas wells", "liquid unloading", "cycle optimization"],
        conclusion_template="Implement plunger lift for intermittent liquid removal in gas wells.",
        reasoning_framework=(
            "Plunger lift systems are used to remove liquids from gas wells, restoring production by cycling a plunger "
            "between the surface and downhole. The system design considers well pressure, liquid load, and cycle timing. "
            "Optimization involves adjusting shut-in and flow periods to maximize liquid removal and minimize downtime. "
            "API 11PL standards and manufacturer recommendations guide equipment selection and operational parameters. "
            "Periodic monitoring and adjustment are required to maintain system efficiency and prevent plunger sticking."
        ),
        key_factors=[
            "Well pressure",
            "Liquid load",
            "Cycle timing",
            "Plunger selection",
            "API 11PL standards"
        ],
        primary_authority=[
            "API 11PL: Plunger Lift Specification",
            "SPE Plunger Lift Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Incorrect cycle timing reduces efficiency and increases wear.",
        counter_arguments=[
            "Overly frequent cycles cause plunger wear.",
            "Long shut-in periods reduce production.",
            "Ignoring liquid load leads to incomplete removal."
        ],
        resolution_strategy="Continuous monitoring and cycle adjustment.",
        entity_scope="Gas wells with plunger lift",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 11PL, SPE Plunger Lift Guidelines"
    ),
    DoctrineBlock(
        topic="Hydraulic Jet Pump Systems",
        keywords=["hydraulic jet pump", "artificial lift", "well stimulation", "pump selection", "fluid injection"],
        conclusion_template="Select hydraulic jet pumps for wells requiring flexible lift and stimulation.",
        reasoning_framework=(
            "Hydraulic jet pumps are chosen for wells needing flexible artificial lift and stimulation. The selection "
            "process evaluates injection fluid properties, pump nozzle size, and well depth. Jet pump efficiency is "
            "optimized by matching injection rate and pressure to reservoir conditions. API 11HJ standards and "
            "manufacturer guidelines inform component selection and operational envelopes. Jet pumps are favored in "
            "wells with variable production rates and limited access for conventional lift systems. Periodic review "
            "of injection performance and pump wear is required."
        ),
        key_factors=[
            "Injection fluid properties",
            "Nozzle size",
            "Well depth",
            "Injection rate and pressure",
            "API 11HJ standards"
        ],
        primary_authority=[
            "API 11HJ: Hydraulic Jet Pump Specification",
            "SPE Jet Pump Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Jet pumps may be inefficient in high solids or low injection pressure wells.",
        counter_arguments=[
            "High solids cause nozzle plugging.",
            "Low injection pressure reduces lift efficiency.",
            "Incorrect nozzle sizing decreases performance."
        ],
        resolution_strategy="Regular maintenance and performance monitoring.",
        entity_scope="Wells with hydraulic jet pumps",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="API 11HJ, SPE Jet Pump Guidelines"
    ),
    DoctrineBlock(
        topic="Rod String Design and API 11L",
        keywords=["rod string", "design", "beam pump", "API 11L", "fatigue analysis", "load distribution"],
        conclusion_template="Design rod string per API 11L to ensure mechanical integrity and optimal load distribution.",
        reasoning_framework=(
            "Rod string design for beam pumps follows API 11L guidelines, focusing on mechanical integrity, fatigue "
            "resistance, and optimal load distribution. The process involves selecting rod grades, diameters, and "
            "lengths based on well depth, pump load, and fluid properties. Fatigue analysis is performed to estimate "
            "rod life and prevent premature failure. Rod couplings and centralizers are specified to minimize wear "
            "and ensure alignment. The design is validated through simulation and comparison with field data. "
            "Periodic inspection and maintenance are recommended to address wear and corrosion."
        ),
        key_factors=[
            "Rod grade and diameter",
            "Well depth",
            "Pump load",
            "Fatigue analysis",
            "Coupling and centralizer selection",
            "API 11L standards"
        ],
        primary_authority=[
            "API 11L: Rod String Specification",
            "SPE Rod String Design Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Incorrect rod design leads to fatigue failure and production loss.",
        counter_arguments=[
            "Underestimating load causes rod breakage.",
            "Overdesign increases material costs.",
            "Ignoring corrosion leads to premature failure."
        ],
        resolution_strategy="Simulation and field validation of rod design.",
        entity_scope="Beam pump operated wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 11L, SPE Rod String Design"
    ),
    DoctrineBlock(
        topic="VFD (Variable Frequency Drive) for ESP",
        keywords=["VFD", "variable frequency drive", "ESP", "motor control", "speed optimization", "power efficiency"],
        conclusion_template="Implement VFDs to optimize ESP speed, power consumption, and operational flexibility.",
        reasoning_framework=(
            "Variable frequency drives are used with ESPs to control motor speed, optimize power consumption, and "
            "provide operational flexibility. VFD selection considers motor rating, voltage compatibility, and "
            "harmonic mitigation. The drive is programmed to match pump speed to production requirements, reducing "
            "energy use and extending equipment life. API 11B and IEEE standards guide VFD integration and safety. "
            "Periodic monitoring of drive performance and motor temperature is required to prevent overheating and "
            "electrical faults. VFDs enable remote control and automation, supporting production optimization."
        ),
        key_factors=[
            "Motor rating and voltage",
            "Speed control range",
            "Harmonic mitigation",
            "API 11B and IEEE standards",
            "Drive programming"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "IEEE 519: Harmonic Control",
            "SPE ESP Automation Handbook"
        ],
        burden_holder="Electrical Engineer",
        adversary_position="Incorrect VFD settings cause motor damage and production loss.",
        counter_arguments=[
            "Over-speeding leads to pump failure.",
            "Poor harmonic control damages electrical systems.",
            "Ignoring temperature limits causes motor burnout."
        ],
        resolution_strategy="Periodic monitoring and drive adjustment.",
        entity_scope="ESP operated wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 11B, IEEE 519, SPE ESP Automation"
    ),
    DoctrineBlock(
        topic="Lift Method Selection Decision Tree",
        keywords=["lift method", "decision tree", "artificial lift", "well productivity", "fluid properties", "economic analysis"],
        conclusion_template="Select optimal lift method using a decision tree based on well and reservoir characteristics.",
        reasoning_framework=(
            "Lift method selection is guided by a structured decision tree that evaluates well productivity, fluid "
            "properties, reservoir pressure, and economic factors. The process begins with inflow performance analysis, "
            "followed by screening for artificial lift feasibility. Each lift method is assessed for compatibility with "
            "well conditions, operational constraints, and lifecycle costs. The decision tree incorporates field "
            "precedent, API standards, and simulation results. Final selection is validated through pilot testing and "
            "production monitoring. Periodic review is performed to adapt to changing well conditions."
        ),
        key_factors=[
            "Well productivity",
            "Fluid properties",
            "Reservoir pressure",
            "Operational constraints",
            "Economic analysis",
            "Field precedent"
        ],
        primary_authority=[
            "API Artificial Lift Standards",
            "SPE Lift Method Selection Guide"
        ],
        burden_holder="Production Engineer",
        adversary_position="Decision tree may oversimplify complex well conditions.",
        counter_arguments=[
            "Unique well conditions may not fit standard tree.",
            "Economic analysis may be incomplete.",
            "Field precedent may not apply to new reservoirs."
        ],
        resolution_strategy="Pilot testing and periodic review.",
        entity_scope="Oil and gas wells requiring artificial lift",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API Standards, SPE Lift Method Selection"
    ),
    DoctrineBlock(
        topic="Gas Anchor and Separator Design",
        keywords=["gas anchor", "separator", "artificial lift", "ESP", "beam pump", "gas separation"],
        conclusion_template="Design gas anchors and separators to minimize gas interference in artificial lift systems.",
        reasoning_framework=(
            "Gas anchor and separator design is critical for minimizing gas interference in artificial lift systems. "
            "The process involves sizing anchors and separators based on gas-liquid ratios, well depth, and lift method. "
            "API 11G standards and manufacturer guidelines inform component selection and operational envelopes. "
            "Design optimization includes placement relative to pump intake, flow rate, and pressure drop. Simulation "
            "tools are used to model separation efficiency and validate design. Periodic inspection and maintenance are "
            "recommended to address plugging and wear."
        ),
        key_factors=[
            "Gas-liquid ratio",
            "Well depth",
            "Lift method",
            "Separator sizing",
            "API 11G standards"
        ],
        primary_authority=[
            "API 11G: Gas Anchor and Separator Specification",
            "SPE Gas Separation Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Incorrect separator sizing increases gas interference and reduces lift efficiency.",
        counter_arguments=[
            "Oversized separators increase equipment costs.",
            "Undersized anchors fail to remove gas.",
            "Improper placement reduces separation efficiency."
        ],
        resolution_strategy="Simulation and periodic maintenance.",
        entity_scope="Artificial lift operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11G, SPE Gas Separation"
    ),
    DoctrineBlock(
        topic="Tubing Anchor and Catcher Design",
        keywords=["tubing anchor", "catcher", "artificial lift", "well completion", "mechanical integrity"],
        conclusion_template="Design tubing anchors and catchers to ensure mechanical integrity and prevent tubing movement.",
        reasoning_framework=(
            "Tubing anchor and catcher design focuses on preventing tubing movement and ensuring mechanical integrity "
            "in artificial lift wells. The process involves selecting anchor and catcher types based on well depth, "
            "completion design, and expected loads. API 11TA standards and manufacturer guidelines inform component "
            "selection. Placement is optimized to minimize tubing buckling and prevent fishing operations. Periodic "
            "inspection and maintenance are recommended to address wear and corrosion."
        ),
        key_factors=[
            "Well depth",
            "Completion design",
            "Expected loads",
            "Anchor and catcher type",
            "API 11TA standards"
        ],
        primary_authority=[
            "API 11TA: Tubing Anchor Specification",
            "SPE Tubing Anchor Handbook"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Incorrect anchor design leads to tubing movement and production loss.",
        counter_arguments=[
            "Underestimating loads causes anchor failure.",
            "Overdesign increases material costs.",
            "Ignoring corrosion leads to premature failure."
        ],
        resolution_strategy="Periodic inspection and maintenance.",
        entity_scope="Artificial lift operated wells",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 11TA, SPE Tubing Anchor"
    ),
    DoctrineBlock(
        topic="Pumping Unit Geometry and API 11E Classes",
        keywords=["pumping unit", "geometry", "beam pump", "API 11E", "unit class", "mechanical efficiency"],
        conclusion_template="Select pumping unit geometry and API 11E class to match well load and optimize efficiency.",
        reasoning_framework=(
            "Pumping unit geometry and API 11E class selection is based on well load, stroke length, and mechanical "
            "efficiency. The process involves evaluating unit geometry (conventional, air-balanced, or hydraulic) and "
            "matching API 11E class to expected loads. Unit selection considers surface constraints, maintenance access, "
            "and operational flexibility. API 11E standards provide guidelines for rating and classification. Periodic "
            "inspection and maintenance are recommended to address wear and alignment."
        ),
        key_factors=[
            "Well load",
            "Stroke length",
            "Unit geometry",
            "API 11E class",
            "Surface constraints"
        ],
        primary_authority=[
            "API 11E: Pumping Unit Specification",
            "SPE Pumping Unit Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Incorrect unit selection reduces efficiency and increases maintenance.",
        counter_arguments=[
            "Oversized units increase capital costs.",
            "Undersized units fail to meet production targets.",
            "Ignoring surface constraints leads to installation issues."
        ],
        resolution_strategy="Field validation and periodic maintenance.",
        entity_scope="Beam pump operated wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 11E, SPE Pumping Unit"
    ),
    DoctrineBlock(
        topic="Polished Rod Clamp and Stuffing Box",
        keywords=["polished rod", "clamp", "stuffing box", "beam pump", "seal integrity", "rod alignment"],
        conclusion_template="Select and install polished rod clamps and stuffing boxes to ensure seal integrity and rod alignment.",
        reasoning_framework=(
            "Polished rod clamp and stuffing box selection is critical for maintaining seal integrity and rod alignment "
            "in beam pump systems. The process involves matching clamp and stuffing box size to rod diameter and well "
            "pressure. API 11PR standards and manufacturer guidelines inform component selection. Installation is "
            "performed with attention to alignment and torque specifications. Periodic inspection and maintenance are "
            "required to address seal wear and prevent leaks."
        ),
        key_factors=[
            "Rod diameter",
            "Well pressure",
            "Clamp and stuffing box type",
            "Seal material",
            "API 11PR standards"
        ],
        primary_authority=[
            "API 11PR: Polished Rod Specification",
            "SPE Stuffing Box Handbook"
        ],
        burden_holder="Field Technician",
        adversary_position="Incorrect clamp or stuffing box selection leads to leaks and rod misalignment.",
        counter_arguments=[
            "Underestimating pressure causes seal failure.",
            "Overtightening damages rod and seals.",
            "Ignoring material compatibility leads to premature wear."
        ],
        resolution_strategy="Periodic inspection and seal replacement.",
        entity_scope="Beam pump operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11PR, SPE Stuffing Box"
    ),
    DoctrineBlock(
        topic="Production Optimization via Lift Method",
        keywords=["production optimization", "artificial lift", "lift method", "well productivity", "cycle adjustment"],
        conclusion_template="Optimize production by adjusting lift method parameters and monitoring well response.",
        reasoning_framework=(
            "Production optimization via lift method involves adjusting operational parameters such as pump speed, "
            "cycle timing, and injection rates to maximize well productivity. The process begins with baseline "
            "production analysis, followed by iterative parameter adjustment and monitoring. API standards and field "
            "precedent guide optimization strategies. Advanced techniques include automation, remote monitoring, and "
            "data analytics. Periodic review is performed to adapt to changing well conditions and maintain optimal "
            "production."
        ),
        key_factors=[
            "Baseline production analysis",
            "Parameter adjustment",
            "Automation and remote monitoring",
            "API standards",
            "Field precedent"
        ],
        primary_authority=[
            "API Artificial Lift Standards",
            "SPE Production Optimization Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Optimization may increase wear or reduce equipment life.",
        counter_arguments=[
            "Over-optimization causes premature equipment failure.",
            "Ignoring well response leads to suboptimal results.",
            "Economic analysis may be incomplete."
        ],
        resolution_strategy="Iterative optimization with periodic review.",
        entity_scope="Artificial lift operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API Standards, SPE Production Optimization"
    ),
    DoctrineBlock(
        topic="ESP Motor Cooling and Shrouding",
        keywords=["ESP", "motor cooling", "shrouding", "temperature management", "pump reliability"],
        conclusion_template="Design motor cooling and shrouding for ESPs to prevent overheating and ensure reliability.",
        reasoning_framework=(
            "ESP motor cooling and shrouding design is essential for preventing overheating and ensuring pump reliability. "
            "The process involves evaluating downhole temperature, fluid flow rate, and motor placement. Shrouds are "
            "used to direct fluid flow over the motor, enhancing cooling. API 11B and manufacturer guidelines inform "
            "component selection and installation. Periodic monitoring of motor temperature and fluid flow is required "
            "to detect cooling issues and prevent motor burnout."
        ),
        key_factors=[
            "Downhole temperature",
            "Fluid flow rate",
            "Motor placement",
            "Shroud design",
            "API 11B standards"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Cooling Handbook"
        ],
        burden_holder="Electrical Engineer",
        adversary_position="Insufficient cooling leads to motor burnout and pump failure.",
        counter_arguments=[
            "Low fluid flow reduces cooling effectiveness.",
            "Improper shroud design fails to direct flow.",
            "Ignoring temperature limits causes reliability issues."
        ],
        resolution_strategy="Periodic monitoring and shroud maintenance.",
        entity_scope="ESP operated wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Cooling"
    ),
    DoctrineBlock(
        topic="Beam Pump Prime Mover Selection",
        keywords=["beam pump", "prime mover", "motor selection", "engine selection", "power optimization"],
        conclusion_template="Select prime mover for beam pump based on power requirements and operational constraints.",
        reasoning_framework=(
            "Beam pump prime mover selection involves matching motor or engine power to well load and operational "
            "constraints. The process evaluates electrical and mechanical options, considering reliability, efficiency, "
            "and maintenance requirements. API 11E and manufacturer guidelines inform selection and installation. "
            "Economic analysis includes power costs, equipment longevity, and maintenance intervals. Periodic review "
            "is performed to adapt to changing well conditions and optimize power consumption."
        ),
        key_factors=[
            "Well load",
            "Power requirements",
            "Motor or engine type",
            "Reliability and efficiency",
            "API 11E standards"
        ],
        primary_authority=[
            "API 11E: Pumping Unit Specification",
            "SPE Prime Mover Selection Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Incorrect prime mover selection increases costs and reduces reliability.",
        counter_arguments=[
            "Oversized prime mover increases capital and operational costs.",
            "Undersized mover fails to meet production targets.",
            "Ignoring maintenance requirements reduces reliability."
        ],
        resolution_strategy="Economic analysis and periodic review.",
        entity_scope="Beam pump operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11E, SPE Prime Mover Selection"
    ),
    DoctrineBlock(
        topic="ESP Cable Selection and Installation",
        keywords=["ESP", "cable selection", "installation", "voltage rating", "temperature rating", "mechanical protection"],
        conclusion_template="Select and install ESP cables based on voltage, temperature, and mechanical protection requirements.",
        reasoning_framework=(
            "ESP cable selection and installation is governed by voltage and temperature ratings, mechanical protection, "
            "and compatibility with downhole conditions. The process involves evaluating cable length, insulation type, "
            "and armor for abrasion resistance. API 11B and manufacturer guidelines inform selection and installation. "
            "Periodic inspection is required to detect wear, corrosion, and electrical faults. Cable routing and "
            "termination are performed according to safety standards."
        ),
        key_factors=[
            "Voltage rating",
            "Temperature rating",
            "Cable length",
            "Insulation and armor type",
            "API 11B standards"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Cable Handbook"
        ],
        burden_holder="Electrical Engineer",
        adversary_position="Incorrect cable selection leads to electrical faults and pump failure.",
        counter_arguments=[
            "Underestimating voltage causes insulation breakdown.",
            "Ignoring temperature rating leads to cable failure.",
            "Improper installation increases wear."
        ],
        resolution_strategy="Periodic inspection and cable maintenance.",
        entity_scope="ESP operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11B, SPE ESP Cable"
    ),
    DoctrineBlock(
        topic="Gas Lift Injection Rate Optimization",
        keywords=["gas lift", "injection rate", "optimization", "production rate", "well response"],
        conclusion_template="Optimize gas lift injection rate to maximize production and minimize gas usage.",
        reasoning_framework=(
            "Gas lift injection rate optimization involves adjusting gas injection to maximize production while minimizing "
            "gas usage. The process begins with baseline production analysis, followed by iterative injection rate adjustment "
            "and monitoring of well response. API 11V standards and field precedent guide optimization strategies. Advanced "
            "techniques include automation, remote monitoring, and data analytics. Periodic review is performed to adapt to "
            "changing well conditions and maintain optimal production."
        ),
        key_factors=[
            "Baseline production analysis",
            "Injection rate adjustment",
            "Automation and remote monitoring",
            "API 11V standards",
            "Field precedent"
        ],
        primary_authority=[
            "API 11V: Gas Lift Specification",
            "SPE Gas Lift Optimization Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Over-injection increases gas cost and reduces efficiency.",
        counter_arguments=[
            "Under-injection limits production.",
            "Ignoring well response leads to suboptimal results.",
            "Economic analysis may be incomplete."
        ],
        resolution_strategy="Iterative optimization with periodic review.",
        entity_scope="Gas lift operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11V, SPE Gas Lift Optimization"
    ),
    DoctrineBlock(
        topic="PCP Elastomer Selection",
        keywords=["PCP", "elastomer selection", "pump longevity", "chemical compatibility", "abrasion resistance"],
        conclusion_template="Select PCP elastomer based on fluid chemistry, temperature, and abrasion resistance.",
        reasoning_framework=(
            "PCP elastomer selection is critical for pump longevity and performance. The process involves evaluating fluid "
            "chemistry, temperature, and abrasion resistance. API 11AX and manufacturer guidelines inform elastomer selection. "
            "Field testing and periodic inspection are recommended to validate compatibility and detect wear. Elastomer "
            "replacement schedules are developed based on production trends and failure analysis."
        ),
        key_factors=[
            "Fluid chemistry",
            "Temperature",
            "Abrasion resistance",
            "API 11AX standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11AX: PCP Specification",
            "SPE PCP Elastomer Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Incorrect elastomer selection leads to premature pump failure.",
        counter_arguments=[
            "Ignoring chemical compatibility causes elastomer degradation.",
            "Underestimating abrasion leads to rapid wear.",
            "Improper replacement schedule reduces pump life."
        ],
        resolution_strategy="Field testing and periodic inspection.",
        entity_scope="PCP operated wells",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 11AX, SPE PCP Elastomer"
    ),
    DoctrineBlock(
        topic="Plunger Lift Cycle Optimization",
        keywords=["plunger lift", "cycle optimization", "production rate", "liquid removal", "well response"],
        conclusion_template="Optimize plunger lift cycle timing to maximize liquid removal and production rate.",
        reasoning_framework=(
            "Plunger lift cycle optimization involves adjusting shut-in and flow periods to maximize liquid removal and "
            "production rate. The process begins with baseline production analysis, followed by iterative cycle timing "
            "adjustment and monitoring of well response. API 11PL standards and field precedent guide optimization strategies. "
            "Advanced techniques include automation, remote monitoring, and data analytics. Periodic review is performed to "
            "adapt to changing well conditions and maintain optimal production."
        ),
        key_factors=[
            "Baseline production analysis",
            "Cycle timing adjustment",
            "Automation and remote monitoring",
            "API 11PL standards",
            "Field precedent"
        ],
        primary_authority=[
            "API 11PL: Plunger Lift Specification",
            "SPE Plunger Lift Optimization Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Incorrect cycle timing reduces efficiency and increases wear.",
        counter_arguments=[
            "Overly frequent cycles cause plunger wear.",
            "Long shut-in periods reduce production.",
            "Ignoring well response leads to suboptimal results."
        ],
        resolution_strategy="Iterative optimization with periodic review.",
        entity_scope="Plunger lift operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11PL, SPE Plunger Lift Optimization"
    ),
    DoctrineBlock(
        topic="Hydraulic Jet Pump Nozzle Sizing",
        keywords=["hydraulic jet pump", "nozzle sizing", "injection rate", "lift efficiency", "well depth"],
        conclusion_template="Size hydraulic jet pump nozzle to match injection rate and optimize lift efficiency.",
        reasoning_framework=(
            "Hydraulic jet pump nozzle sizing is based on injection rate, well depth, and desired lift efficiency. The process "
            "involves calculating nozzle diameter and throat area using API 11HJ standards and manufacturer guidelines. Simulation "
            "tools are used to model injection performance and validate sizing. Periodic review and adjustment are performed based "
            "on production data and well changes."
        ),
        key_factors=[
            "Injection rate",
            "Well depth",
            "Nozzle diameter",
            "Lift efficiency",
            "API 11HJ standards"
        ],
        primary_authority=[
            "API 11HJ: Hydraulic Jet Pump Specification",
            "SPE Jet Pump Sizing Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Incorrect nozzle sizing reduces lift efficiency and increases wear.",
        counter_arguments=[
            "Oversized nozzle reduces injection pressure.",
            "Undersized nozzle limits production.",
            "Ignoring well depth leads to suboptimal sizing."
        ],
        resolution_strategy="Simulation and field validation.",
        entity_scope="Hydraulic jet pump operated wells",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 11HJ, SPE Jet Pump Sizing"
    ),
    DoctrineBlock(
        topic="Rod Guide Selection and Placement",
        keywords=["rod guide", "selection", "placement", "beam pump", "wear reduction", "alignment"],
        conclusion_template="Select and place rod guides to minimize wear and ensure rod alignment in beam pump wells.",
        reasoning_framework=(
            "Rod guide selection and placement is critical for minimizing wear and ensuring rod alignment in beam pump wells. "
            "The process involves evaluating well trajectory, rod diameter, and expected loads. API 11L and manufacturer guidelines "
            "inform guide selection and placement intervals. Periodic inspection and replacement are recommended to address wear "
            "and maintain alignment."
        ),
        key_factors=[
            "Well trajectory",
            "Rod diameter",
            "Expected loads",
            "Guide material",
            "API 11L standards"
        ],
        primary_authority=[
            "API 11L: Rod String Specification",
            "SPE Rod Guide Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Incorrect guide selection increases wear and reduces rod life.",
        counter_arguments=[
            "Underestimating loads causes guide failure.",
            "Overdesign increases material costs.",
            "Ignoring trajectory leads to misalignment."
        ],
        resolution_strategy="Periodic inspection and guide replacement.",
        entity_scope="Beam pump operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11L, SPE Rod Guide"
    ),
    DoctrineBlock(
        topic="ESP Intake Placement Optimization",
        keywords=["ESP", "intake placement", "optimization", "fluid inflow", "gas separation"],
        conclusion_template="Optimize ESP intake placement to maximize fluid inflow and minimize gas interference.",
        reasoning_framework=(
            "ESP intake placement optimization involves positioning the pump intake to maximize fluid inflow and minimize gas interference. "
            "The process evaluates reservoir inflow profile, gas-liquid ratio, and well trajectory. API 11B and manufacturer guidelines "
            "inform placement strategies. Simulation tools are used to model inflow performance and validate placement. Periodic review "
            "is performed to adapt to changing well conditions."
        ),
        key_factors=[
            "Reservoir inflow profile",
            "Gas-liquid ratio",
            "Well trajectory",
            "Intake placement",
            "API 11B standards"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Intake Placement Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Incorrect intake placement reduces production and increases gas lock risk.",
        counter_arguments=[
            "Placing intake too high increases gas interference.",
            "Placing intake too low limits fluid inflow.",
            "Ignoring trajectory leads to suboptimal placement."
        ],
        resolution_strategy="Simulation and field validation.",
        entity_scope="ESP operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Intake Placement"
    ),
    DoctrineBlock(
        topic="Gas Lift Valve Opening Pressure Calibration",
        keywords=["gas lift", "valve opening pressure", "calibration", "injection efficiency", "production rate"],
        conclusion_template="Calibrate gas lift valve opening pressure to optimize injection efficiency and production rate.",
        reasoning_framework=(
            "Gas lift valve opening pressure calibration is essential for optimizing injection efficiency and production rate. The process "
            "involves setting valve opening pressures based on well injection profile, production targets, and API 11V standards. Manufacturer "
            "guidelines and field precedent inform calibration procedures. Periodic review and adjustment are performed based on production data "
            "and well changes."
        ),
        key_factors=[
            "Injection profile",
            "Production targets",
            "Valve opening pressure",
            "API 11V standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11V: Gas Lift Specification",
            "SPE Gas Lift Valve Calibration Handbook"
        ],
        burden_holder="Gas Lift Engineer",
        adversary_position="Incorrect calibration reduces injection efficiency and production.",
        counter_arguments=[
            "Over-calibration increases gas usage.",
            "Under-calibration limits production.",
            "Ignoring well changes leads to suboptimal results."
        ],
        resolution_strategy="Periodic review and calibration adjustment.",
        entity_scope="Gas lift operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11V, SPE Gas Lift Valve Calibration"
    ),
    DoctrineBlock(
        topic="PCP Drivehead Selection and Maintenance",
        keywords=["PCP", "drivehead selection", "maintenance", "pump longevity", "operational reliability"],
        conclusion_template="Select and maintain PCP driveheads to ensure pump longevity and operational reliability.",
        reasoning_framework=(
            "PCP drivehead selection and maintenance is critical for pump longevity and operational reliability. The process involves evaluating "
            "drivehead torque rating, speed control, and compatibility with well conditions. API 11AX and manufacturer guidelines inform selection "
            "and maintenance procedures. Periodic inspection and lubrication are recommended to detect wear and prevent failure."
        ),
        key_factors=[
            "Drivehead torque rating",
            "Speed control",
            "Compatibility with well conditions",
            "API 11AX standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11AX: PCP Specification",
            "SPE PCP Drivehead Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Incorrect drivehead selection or maintenance reduces pump life and reliability.",
        counter_arguments=[
            "Underestimating torque causes drivehead failure.",
            "Ignoring maintenance leads to premature wear.",
            "Improper speed control reduces efficiency."
        ],
        resolution_strategy="Periodic inspection and lubrication.",
        entity_scope="PCP operated wells",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 11AX, SPE PCP Drivehead"
    ),
    DoctrineBlock(
        topic="ESP Sand Handling and Abrasion Mitigation",
        keywords=["ESP", "sand handling", "abrasion mitigation", "pump longevity", "solids management"],
        conclusion_template="Implement sand handling and abrasion mitigation strategies for ESPs to ensure pump longevity.",
        reasoning_framework=(
            "ESP sand handling and abrasion mitigation strategies are essential for ensuring pump longevity in wells producing solids. The process "
            "involves evaluating sand concentration, pump material selection, and solids management techniques. API 11B and manufacturer guidelines "
            "inform component selection and operational strategies. Periodic inspection and maintenance are required to detect wear and prevent failure."
        ),
        key_factors=[
            "Sand concentration",
            "Pump material selection",
            "Solids management techniques",
            "API 11B standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Sand Handling Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Insufficient sand handling increases abrasion and reduces pump life.",
        counter_arguments=[
            "Ignoring sand concentration causes rapid wear.",
            "Improper material selection reduces longevity.",
            "Lack of solids management leads to pump failure."
        ],
        resolution_strategy="Periodic inspection and solids management.",
        entity_scope="ESP operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11B, SPE ESP Sand Handling"
    ),
    DoctrineBlock(
        topic="Beam Pump Rod Load Monitoring",
        keywords=["beam pump", "rod load monitoring", "fatigue analysis", "production optimization", "failure prevention"],
        conclusion_template="Monitor beam pump rod loads to optimize production and prevent fatigue failure.",
        reasoning_framework=(
            "Beam pump rod load monitoring is essential for optimizing production and preventing fatigue failure. The process involves periodic "
            "measurement of rod loads using dynamometers and data analytics. API 11L and manufacturer guidelines inform monitoring procedures. "
            "Fatigue analysis is performed to estimate rod life and detect anomalies. Periodic review and adjustment are performed based on production "
            "data and well changes."
        ),
        key_factors=[
            "Rod load measurement",
            "Fatigue analysis",
            "Production data",
            "API 11L standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11L: Rod String Specification",
            "SPE Rod Load Monitoring Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient monitoring increases risk of rod failure and production loss.",
        counter_arguments=[
            "Ignoring load anomalies causes premature failure.",
            "Underestimating fatigue reduces rod life.",
            "Improper adjustment leads to suboptimal production."
        ],
        resolution_strategy="Periodic monitoring and fatigue analysis.",
        entity_scope="Beam pump operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11L, SPE Rod Load Monitoring"
    ),
    DoctrineBlock(
        topic="Gas Lift Mandrel Selection and Installation",
        keywords=["gas lift", "mandrel selection", "installation", "valve compatibility", "mechanical integrity"],
        conclusion_template="Select and install gas lift mandrels to ensure valve compatibility and mechanical integrity.",
        reasoning_framework=(
            "Gas lift mandrel selection and installation is critical for ensuring valve compatibility and mechanical integrity. The process involves "
            "evaluating mandrel type, valve compatibility, and well completion design. API 11V and manufacturer guidelines inform selection and installation "
            "procedures. Periodic inspection and maintenance are recommended to detect wear and prevent failure."
        ),
        key_factors=[
            "Mandrel type",
            "Valve compatibility",
            "Completion design",
            "API 11V standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11V: Gas Lift Specification",
            "SPE Gas Lift Mandrel Handbook"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Incorrect mandrel selection or installation reduces injection efficiency and mechanical integrity.",
        counter_arguments=[
            "Underestimating compatibility causes valve failure.",
            "Ignoring completion design leads to installation issues.",
            "Improper maintenance reduces longevity."
        ],
        resolution_strategy="Periodic inspection and maintenance.",
        entity_scope="Gas lift operated wells",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 11V, SPE Gas Lift Mandrel"
    ),
    DoctrineBlock(
        topic="PCP Torque Monitoring and Control",
        keywords=["PCP", "torque monitoring", "control", "pump longevity", "failure prevention"],
        conclusion_template="Monitor and control PCP torque to ensure pump longevity and prevent failure.",
        reasoning_framework=(
            "PCP torque monitoring and control is essential for ensuring pump longevity and preventing failure. The process involves periodic measurement "
            "of drivehead torque using sensors and data analytics. API 11AX and manufacturer guidelines inform monitoring procedures. Control strategies "
            "include adjusting speed and load to maintain optimal torque. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Drivehead torque measurement",
            "Speed and load adjustment",
            "Production data",
            "API 11AX standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11AX: PCP Specification",
            "SPE PCP Torque Monitoring Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient torque monitoring increases risk of pump failure and production loss.",
        counter_arguments=[
            "Ignoring torque anomalies causes premature failure.",
            "Improper control reduces pump longevity.",
            "Underestimating load leads to drivehead failure."
        ],
        resolution_strategy="Periodic monitoring and control adjustment.",
        entity_scope="PCP operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11AX, SPE PCP Torque Monitoring"
    ),
    DoctrineBlock(
        topic="ESP Voltage and Current Monitoring",
        keywords=["ESP", "voltage monitoring", "current monitoring", "electrical faults", "production optimization"],
        conclusion_template="Monitor ESP voltage and current to detect electrical faults and optimize production.",
        reasoning_framework=(
            "ESP voltage and current monitoring is critical for detecting electrical faults and optimizing production. The process involves periodic measurement "
            "using sensors and data analytics. API 11B and manufacturer guidelines inform monitoring procedures. Fault detection strategies include threshold "
            "analysis and pattern recognition. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Voltage and current measurement",
            "Fault detection",
            "Production data",
            "API 11B standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Electrical Monitoring Handbook"
        ],
        burden_holder="Electrical Engineer",
        adversary_position="Insufficient monitoring increases risk of electrical faults and production loss.",
        counter_arguments=[
            "Ignoring anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating electrical faults leads to pump failure."
        ],
        resolution_strategy="Periodic monitoring and fault detection.",
        entity_scope="ESP operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Electrical Monitoring"
    ),
    DoctrineBlock(
        topic="Beam Pump Stroke Length Optimization",
        keywords=["beam pump", "stroke length", "optimization", "production rate", "mechanical efficiency"],
        conclusion_template="Optimize beam pump stroke length to maximize production rate and mechanical efficiency.",
        reasoning_framework=(
            "Beam pump stroke length optimization involves adjusting stroke length to maximize production rate and mechanical efficiency. The process begins with "
            "baseline production analysis, followed by iterative stroke length adjustment and monitoring of well response. API 11E standards and field precedent "
            "guide optimization strategies. Advanced techniques include automation, remote monitoring, and data analytics. Periodic review is performed to adapt to "
            "changing well conditions and maintain optimal production."
        ),
        key_factors=[
            "Baseline production analysis",
            "Stroke length adjustment",
            "Automation and remote monitoring",
            "API 11E standards",
            "Field precedent"
        ],
        primary_authority=[
            "API 11E: Pumping Unit Specification",
            "SPE Beam Pump Optimization Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Incorrect stroke length reduces efficiency and increases wear.",
        counter_arguments=[
            "Overly long strokes cause mechanical failure.",
            "Short strokes limit production.",
            "Ignoring well response leads to suboptimal results."
        ],
        resolution_strategy="Iterative optimization with periodic review.",
        entity_scope="Beam pump operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11E, SPE Beam Pump Optimization"
    ),
    DoctrineBlock(
        topic="Gas Lift Valve Erosion Monitoring",
        keywords=["gas lift", "valve erosion", "monitoring", "failure prevention", "production optimization"],
        conclusion_template="Monitor gas lift valve erosion to prevent failure and optimize production.",
        reasoning_framework=(
            "Gas lift valve erosion monitoring is essential for preventing failure and optimizing production. The process involves periodic inspection and "
            "measurement of valve wear using sensors and data analytics. API 11V and manufacturer guidelines inform monitoring procedures. Erosion detection "
            "strategies include threshold analysis and pattern recognition. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Valve wear measurement",
            "Erosion detection",
            "Production data",
            "API 11V standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11V: Gas Lift Specification",
            "SPE Gas Lift Valve Erosion Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient monitoring increases risk of valve failure and production loss.",
        counter_arguments=[
            "Ignoring wear anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating erosion leads to valve failure."
        ],
        resolution_strategy="Periodic monitoring and erosion detection.",
        entity_scope="Gas lift operated wells",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API 11V, SPE Gas Lift Valve Erosion"
    ),
    DoctrineBlock(
        topic="PCP Speed Control and Automation",
        keywords=["PCP", "speed control", "automation", "production optimization", "pump longevity"],
        conclusion_template="Implement PCP speed control and automation to optimize production and ensure pump longevity.",
        reasoning_framework=(
            "PCP speed control and automation are essential for optimizing production and ensuring pump longevity. The process involves adjusting pump speed using "
            "variable frequency drives and automation systems. API 11AX and manufacturer guidelines inform control strategies. Periodic monitoring and adjustment "
            "are performed based on production data and well changes."
        ),
        key_factors=[
            "Pump speed adjustment",
            "Automation system integration",
            "Production data",
            "API 11AX standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11AX: PCP Specification",
            "SPE PCP Automation Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Incorrect speed control reduces pump longevity and production.",
        counter_arguments=[
            "Over-speeding causes premature failure.",
            "Ignoring automation limits optimization.",
            "Improper adjustment reduces efficiency."
        ],
        resolution_strategy="Periodic monitoring and automation adjustment.",
        entity_scope="PCP operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11AX, SPE PCP Automation"
    ),
    DoctrineBlock(
        topic="ESP Gas Lock Prevention",
        keywords=["ESP", "gas lock prevention", "production optimization", "failure prevention", "well response"],
        conclusion_template="Implement gas lock prevention strategies for ESPs to optimize production and prevent failure.",
        reasoning_framework=(
            "ESP gas lock prevention strategies are essential for optimizing production and preventing failure. The process involves adjusting pump speed, intake placement, "
            "and gas separator design. API 11B and manufacturer guidelines inform prevention strategies. Periodic monitoring and adjustment are performed based on production "
            "data and well changes."
        ),
        key_factors=[
            "Pump speed adjustment",
            "Intake placement",
            "Gas separator design",
            "API 11B standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Gas Lock Prevention Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient prevention increases risk of gas lock and production loss.",
        counter_arguments=[
            "Ignoring gas lock anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating gas separator design leads to gas lock."
        ],
        resolution_strategy="Periodic monitoring and prevention adjustment.",
        entity_scope="ESP operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Gas Lock Prevention"
    ),
    DoctrineBlock(
        topic="Beam Pump Surface Unit Alignment",
        keywords=["beam pump", "surface unit alignment", "mechanical integrity", "production optimization", "failure prevention"],
        conclusion_template="Ensure beam pump surface unit alignment to maintain mechanical integrity and optimize production.",
        reasoning_framework=(
            "Beam pump surface unit alignment is critical for maintaining mechanical integrity and optimizing production. The process involves periodic inspection and "
            "alignment measurement using tools and data analytics. API 11E and manufacturer guidelines inform alignment procedures. Periodic review and adjustment are "
            "performed based on production data and well changes."
        ),
        key_factors=[
            "Alignment measurement",
            "Mechanical integrity",
            "Production data",
            "API 11E standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11E: Pumping Unit Specification",
            "SPE Beam Pump Alignment Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Insufficient alignment increases risk of mechanical failure and production loss.",
        counter_arguments=[
            "Ignoring alignment anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating mechanical integrity leads to failure."
        ],
        resolution_strategy="Periodic inspection and alignment adjustment.",
        entity_scope="Beam pump operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11E, SPE Beam Pump Alignment"
    ),
    DoctrineBlock(
        topic="Gas Lift Injection Pressure Monitoring",
        keywords=["gas lift", "injection pressure monitoring", "production optimization", "failure prevention", "well response"],
        conclusion_template="Monitor gas lift injection pressure to optimize production and prevent failure.",
        reasoning_framework=(
            "Gas lift injection pressure monitoring is essential for optimizing production and preventing failure. The process involves periodic measurement of injection "
            "pressure using sensors and data analytics. API 11V and manufacturer guidelines inform monitoring procedures. Periodic review and adjustment are performed based "
            "on production data and well changes."
        ),
        key_factors=[
            "Injection pressure measurement",
            "Production data",
            "API 11V standards",
            "Manufacturer guidelines",
            "Failure prevention"
        ],
        primary_authority=[
            "API 11V: Gas Lift Specification",
            "SPE Gas Lift Injection Pressure Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient monitoring increases risk of injection failure and production loss.",
        counter_arguments=[
            "Ignoring pressure anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating injection pressure leads to failure."
        ],
        resolution_strategy="Periodic monitoring and pressure adjustment.",
        entity_scope="Gas lift operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11V, SPE Gas Lift Injection Pressure"
    ),
    DoctrineBlock(
        topic="PCP Pumping System Automation",
        keywords=["PCP", "pumping system automation", "production optimization", "failure prevention", "well response"],
        conclusion_template="Automate PCP pumping system to optimize production and prevent failure.",
        reasoning_framework=(
            "PCP pumping system automation is essential for optimizing production and preventing failure. The process involves integrating automation systems with pump controls, "
            "monitoring production data, and adjusting operational parameters. API 11AX and manufacturer guidelines inform automation strategies. Periodic review and adjustment are "
            "performed based on production data and well changes."
        ),
        key_factors=[
            "Automation system integration",
            "Production data",
            "API 11AX standards",
            "Manufacturer guidelines",
            "Failure prevention"
        ],
        primary_authority=[
            "API 11AX: PCP Specification",
            "SPE PCP Pumping System Automation Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient automation increases risk of failure and reduces optimization.",
        counter_arguments=[
            "Ignoring automation anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating automation integration leads to failure."
        ],
        resolution_strategy="Periodic review and automation adjustment.",
        entity_scope="PCP operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11AX, SPE PCP Pumping System Automation"
    ),
    DoctrineBlock(
        topic="ESP Downhole Sensor Integration",
        keywords=["ESP", "downhole sensor integration", "production optimization", "failure prevention", "data analytics"],
        conclusion_template="Integrate downhole sensors with ESPs to optimize production and prevent failure.",
        reasoning_framework=(
            "ESP downhole sensor integration is essential for optimizing production and preventing failure. The process involves selecting sensor types, integrating with pump controls, "
            "and analyzing production data. API 11B and manufacturer guidelines inform integration strategies. Periodic review and adjustment are performed based on sensor data and well changes."
        ),
        key_factors=[
            "Sensor type selection",
            "Integration with pump controls",
            "Production data analysis",
            "API 11B standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Downhole Sensor Integration Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient sensor integration increases risk of failure and reduces optimization.",
        counter_arguments=[
            "Ignoring sensor anomalies causes premature failure.",
            "Improper integration reduces production.",
            "Underestimating sensor data leads to failure."
        ],
        resolution_strategy="Periodic review and sensor integration adjustment.",
        entity_scope="ESP operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Downhole Sensor Integration"
    ),
    DoctrineBlock(
        topic="Beam Pump Counterbalance Adjustment",
        keywords=["beam pump", "counterbalance adjustment", "mechanical efficiency", "production optimization", "failure prevention"],
        conclusion_template="Adjust beam pump counterbalance to optimize mechanical efficiency and prevent failure.",
        reasoning_framework=(
            "Beam pump counterbalance adjustment is critical for optimizing mechanical efficiency and preventing failure. The process involves periodic measurement and adjustment of counterbalance weights "
            "using tools and data analytics. API 11E and manufacturer guidelines inform adjustment procedures. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Counterbalance weight measurement",
            "Mechanical efficiency",
            "Production data",
            "API 11E standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11E: Pumping Unit Specification",
            "SPE Beam Pump Counterbalance Adjustment Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Insufficient adjustment increases risk of mechanical failure and production loss.",
        counter_arguments=[
            "Ignoring adjustment anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating mechanical efficiency leads to failure."
        ],
        resolution_strategy="Periodic measurement and adjustment.",
        entity_scope="Beam pump operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11E, SPE Beam Pump Counterbalance Adjustment"
    ),
    DoctrineBlock(
        topic="Gas Lift Valve Replacement Scheduling",
        keywords=["gas lift", "valve replacement scheduling", "failure prevention", "production optimization", "maintenance planning"],
        conclusion_template="Schedule gas lift valve replacement to prevent failure and optimize production.",
        reasoning_framework=(
            "Gas lift valve replacement scheduling is essential for preventing failure and optimizing production. The process involves developing replacement schedules based on valve wear, production data, "
            "and API 11V standards. Manufacturer guidelines and field precedent inform scheduling procedures. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Valve wear analysis",
            "Replacement scheduling",
            "Production data",
            "API 11V standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11V: Gas Lift Specification",
            "SPE Gas Lift Valve Replacement Scheduling Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient scheduling increases risk of valve failure and production loss.",
        counter_arguments=[
            "Ignoring wear analysis causes premature failure.",
            "Improper scheduling reduces production.",
            "Underestimating replacement needs leads to failure."
        ],
        resolution_strategy="Periodic review and scheduling adjustment.",
        entity_scope="Gas lift operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11V, SPE Gas Lift Valve Replacement Scheduling"
    ),
    DoctrineBlock(
        topic="PCP Pumping System Failure Analysis",
        keywords=["PCP", "pumping system failure analysis", "root cause", "production optimization", "failure prevention"],
        conclusion_template="Conduct root cause analysis for PCP pumping system failures to optimize production and prevent recurrence.",
        reasoning_framework=(
            "PCP pumping system failure analysis is essential for optimizing production and preventing recurrence. The process involves reviewing production data, inspecting failed components, and analyzing root causes. "
            "API 11AX and manufacturer guidelines inform analysis procedures. Recommendations are formulated based on root cause findings, including design changes, operational adjustments, and preventive maintenance schedules."
        ),
        key_factors=[
            "Production data review",
            "Component inspection",
            "Root cause analysis",
            "API 11AX standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11AX: PCP Specification",
            "SPE PCP Pumping System Failure Analysis Handbook"
        ],
        burden_holder="Reliability Engineer",
        adversary_position="Insufficient analysis increases risk of recurrence and production loss.",
        counter_arguments=[
            "Ignoring root causes causes premature failure.",
            "Improper recommendations reduce production.",
            "Underestimating failure mechanisms leads to recurrence."
        ],
        resolution_strategy="Comprehensive root cause analysis and preventive maintenance.",
        entity_scope="PCP operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11AX, SPE PCP Pumping System Failure Analysis"
    ),
    DoctrineBlock(
        topic="ESP Pump Curve Analysis",
        keywords=["ESP", "pump curve analysis", "production optimization", "failure prevention", "well response"],
        conclusion_template="Analyze ESP pump curves to optimize production and prevent failure.",
        reasoning_framework=(
            "ESP pump curve analysis is essential for optimizing production and preventing failure. The process involves reviewing pump curves, matching production targets, and analyzing well response. API 11B and manufacturer "
            "guidelines inform analysis procedures. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Pump curve review",
            "Production target matching",
            "Well response analysis",
            "API 11B standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11B: ESP Specification",
            "SPE ESP Pump Curve Analysis Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient analysis increases risk of failure and production loss.",
        counter_arguments=[
            "Ignoring curve anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating well response leads to failure."
        ],
        resolution_strategy="Periodic review and curve adjustment.",
        entity_scope="ESP operated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 11B, SPE ESP Pump Curve Analysis"
    ),
    DoctrineBlock(
        topic="Beam Pump Unit Lubrication Scheduling",
        keywords=["beam pump", "unit lubrication scheduling", "failure prevention", "production optimization", "maintenance planning"],
        conclusion_template="Schedule beam pump unit lubrication to prevent failure and optimize production.",
        reasoning_framework=(
            "Beam pump unit lubrication scheduling is essential for preventing failure and optimizing production. The process involves developing lubrication schedules based on unit wear, production data, and API 11E standards. "
            "Manufacturer guidelines and field precedent inform scheduling procedures. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Unit wear analysis",
            "Lubrication scheduling",
            "Production data",
            "API 11E standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11E: Pumping Unit Specification",
            "SPE Beam Pump Unit Lubrication Scheduling Handbook"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Insufficient scheduling increases risk of unit failure and production loss.",
        counter_arguments=[
            "Ignoring wear analysis causes premature failure.",
            "Improper scheduling reduces production.",
            "Underestimating lubrication needs leads to failure."
        ],
        resolution_strategy="Periodic review and scheduling adjustment.",
        entity_scope="Beam pump operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11E, SPE Beam Pump Unit Lubrication Scheduling"
    ),
    DoctrineBlock(
        topic="Gas Lift System Automation",
        keywords=["gas lift", "system automation", "production optimization", "failure prevention", "well response"],
        conclusion_template="Automate gas lift system to optimize production and prevent failure.",
        reasoning_framework=(
            "Gas lift system automation is essential for optimizing production and preventing failure. The process involves integrating automation systems with injection controls, monitoring production data, and adjusting operational parameters. "
            "API 11V and manufacturer guidelines inform automation strategies. Periodic review and adjustment are performed based on production data and well changes."
        ),
        key_factors=[
            "Automation system integration",
            "Injection control adjustment",
            "Production data",
            "API 11V standards",
            "Manufacturer guidelines"
        ],
        primary_authority=[
            "API 11V: Gas Lift Specification",
            "SPE Gas Lift System Automation Handbook"
        ],
        burden_holder="Production Optimization Specialist",
        adversary_position="Insufficient automation increases risk of failure and reduces optimization.",
        counter_arguments=[
            "Ignoring automation anomalies causes premature failure.",
            "Improper adjustment reduces production.",
            "Underestimating automation integration leads to failure."
        ],
        resolution_strategy="Periodic review and automation adjustment.",
        entity_scope="Gas lift operated wells",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="API 11V, SPE Gas Lift System Automation"
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