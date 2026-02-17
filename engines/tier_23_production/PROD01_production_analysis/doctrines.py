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
        topic="Vogel IPR for Solution Gas Drive Reservoirs",
        keywords=["IPR", "Vogel", "solution gas drive", "reservoir", "productivity"],
        conclusion_template="The inflow performance relationship for a solution gas drive reservoir is best modeled using Vogel's empirical equation.",
        reasoning_framework=(
            "Vogel's IPR equation is derived from empirical studies of solution gas drive reservoirs, "
            "where the relationship between flowing bottomhole pressure (Pwf) and production rate (Q) is non-linear. "
            "The equation accounts for the reduction in productivity as reservoir pressure declines, "
            "and is expressed as: Q/Qmax = 1 - 0.8*(Pwf/Pres) - 0.2*(Pwf/Pres)^2. "
            "This framework assumes single-phase flow and neglects effects such as water encroachment or gas breakthrough. "
            "Key factors include reservoir pressure, maximum flow rate, and bottomhole pressure. "
            "The primary authority is Vogel (1968), and the doctrine is widely accepted in petroleum engineering. "
            "Counter arguments may arise regarding applicability in multi-phase or unconventional reservoirs, "
            "but the doctrine remains robust for classical solution gas drive systems. "
            "Resolution involves calibration with field data and consideration of reservoir heterogeneity."
        ),
        key_factors=["Reservoir pressure", "Maximum flow rate", "Bottomhole pressure", "Reservoir drive mechanism"],
        primary_authority=["Vogel, J.C. (1968)", "SPE Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Vogel's equation may not account for multiphase flow or complex reservoir heterogeneity.",
        counter_arguments=[
            "Vogel's IPR is empirical and may not fit reservoirs with significant water or gas breakthrough.",
            "Alternative models (e.g., Fetkovich) may be more appropriate for certain gas wells."
        ],
        resolution_strategy="Validate Vogel's IPR with field production data and adjust parameters as needed.",
        entity_scope="Conventional oil reservoirs with solution gas drive",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Vogel, J.C. (1968) SPE 2625"
    ),
    DoctrineBlock(
        topic="Fetkovich IPR for Gas Wells",
        keywords=["IPR", "Fetkovich", "gas wells", "productivity", "flow rate"],
        conclusion_template="Fetkovich's IPR provides a robust analytical model for gas well inflow performance.",
        reasoning_framework=(
            "Fetkovich's IPR combines the analytical approach of Darcy's law with empirical adjustments for gas compressibility. "
            "The equation relates flow rate to pressure drop, accounting for non-linearities due to gas properties. "
            "The model is particularly effective for dry gas wells and is expressed as: Q = C*(Pavg^2 - Pwf^2)^n, "
            "where C and n are empirical constants. "
            "Key factors include average reservoir pressure, flowing bottomhole pressure, and gas compressibility. "
            "Primary authority is Fetkovich (1973), and the model is standard in gas well analysis. "
            "Counter arguments focus on limitations in multiphase flow or wells with significant liquid loading. "
            "Resolution involves calibration with well test data and consideration of reservoir conditions."
        ),
        key_factors=["Average reservoir pressure", "Flowing bottomhole pressure", "Gas compressibility", "Empirical constants"],
        primary_authority=["Fetkovich, M.J. (1973)", "SPE Gas Well Performance Analysis"],
        burden_holder="Production Engineer",
        adversary_position="Fetkovich's IPR may not accurately represent wells with liquid loading or multiphase flow.",
        counter_arguments=[
            "Empirical constants may not be transferable across different reservoirs.",
            "Alternative models may be required for unconventional or liquid-rich gas wells."
        ],
        resolution_strategy="Use well test data to calibrate Fetkovich parameters; apply alternative models as needed.",
        entity_scope="Conventional dry gas wells",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fetkovich, M.J. (1973) SPE 5542"
    ),
    DoctrineBlock(
        topic="Nodal Analysis - System Optimization",
        keywords=["nodal analysis", "system optimization", "production system", "well performance"],
        conclusion_template="Nodal analysis is the preferred method for optimizing production systems by evaluating pressure drops across each node.",
        reasoning_framework=(
            "Nodal analysis decomposes the production system into discrete nodes (reservoir, wellbore, surface equipment) "
            "and calculates pressure profiles and flow rates at each node. "
            "This approach enables identification of bottlenecks and optimization of system performance. "
            "The framework involves iterative calculations using IPR and VLP curves, "
            "and considers factors such as reservoir deliverability, wellbore hydraulics, and surface constraints. "
            "Primary authority is Brown (1984), and nodal analysis is standard practice in production engineering. "
            "Counter arguments may arise regarding computational complexity or data requirements, "
            "but the doctrine is robust for integrated system optimization. "
            "Resolution involves using validated models and field data to ensure accuracy."
        ),
        key_factors=["Node definition", "Pressure profile", "Flow rate", "System constraints"],
        primary_authority=["Brown, K.E. (1984)", "SPE Nodal Analysis Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Nodal analysis may be limited by data quality or computational complexity.",
        counter_arguments=[
            "Inaccurate input data can lead to erroneous optimization results.",
            "Simplified models may overlook critical system interactions."
        ],
        resolution_strategy="Ensure high-quality input data and use validated modeling software.",
        entity_scope="Integrated production systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown, K.E. (1984) Nodal Analysis"
    ),
    DoctrineBlock(
        topic="Skin Factor and Flow Efficiency",
        keywords=["skin factor", "flow efficiency", "well performance", "damage", "stimulation"],
        conclusion_template="Skin factor quantifies wellbore damage or stimulation, directly impacting flow efficiency.",
        reasoning_framework=(
            "Skin factor is a dimensionless parameter representing the effect of near-wellbore damage or stimulation on flow efficiency. "
            "Positive skin indicates damage, reducing productivity, while negative skin indicates stimulation, enhancing flow. "
            "The calculation involves pressure transient analysis and comparison to ideal well performance. "
            "Key factors include permeability, wellbore radius, and pressure drop. "
            "Primary authority is Hawkins (1956), and skin factor analysis is standard in well testing. "
            "Counter arguments focus on uncertainty in skin estimation and its variability with operational changes. "
            "Resolution involves repeated testing and calibration with production data."
        ),
        key_factors=["Permeability", "Wellbore radius", "Pressure drop", "Stimulation effectiveness"],
        primary_authority=["Hawkins, M.F. (1956)", "SPE Well Testing Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Skin factor estimation may be uncertain due to variable reservoir conditions.",
        counter_arguments=[
            "Transient effects and operational changes can alter skin factor.",
            "Pressure data may be insufficient for accurate estimation."
        ],
        resolution_strategy="Conduct repeated well tests and calibrate skin factor with production history.",
        entity_scope="Wellbore and near-wellbore region",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hawkins, M.F. (1956) Skin Factor"
    ),
    DoctrineBlock(
        topic="Productivity Index and Reservoir Deliverability",
        keywords=["productivity index", "reservoir deliverability", "well performance", "flow rate"],
        conclusion_template="Productivity Index (PI) is a key metric for assessing reservoir deliverability and well performance.",
        reasoning_framework=(
            "Productivity Index is defined as the ratio of production rate to pressure drawdown, PI = Q/(Pavg - Pwf). "
            "It quantifies the efficiency of a well in delivering fluids from the reservoir. "
            "PI is influenced by reservoir permeability, skin factor, and fluid properties. "
            "Primary authority is Muskat (1937), and PI is a standard metric in production engineering. "
            "Counter arguments focus on PI variability with changing reservoir conditions and operational practices. "
            "Resolution involves periodic PI calculation and adjustment based on production data."
        ),
        key_factors=["Production rate", "Pressure drawdown", "Permeability", "Skin factor"],
        primary_authority=["Muskat, M. (1937)", "SPE Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="PI may change over time due to reservoir depletion or operational changes.",
        counter_arguments=[
            "PI is not constant and must be recalculated periodically.",
            "Complex reservoirs may require more advanced deliverability models."
        ],
        resolution_strategy="Monitor PI regularly and adjust operational strategies as needed.",
        entity_scope="Reservoir and wellbore",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Muskat, M. (1937) Productivity Index"
    ),
    DoctrineBlock(
        topic="Water Cut and GOR Trending - Reservoir Surveillance",
        keywords=["water cut", "GOR", "reservoir surveillance", "production monitoring"],
        conclusion_template="Water cut and GOR trending are essential surveillance tools for reservoir management.",
        reasoning_framework=(
            "Water cut (fraction of produced water) and Gas-Oil Ratio (GOR) are monitored to assess reservoir performance and identify breakthrough events. "
            "Trending these parameters helps detect water or gas encroachment, optimize production strategy, and forecast reservoir behavior. "
            "Key factors include production rates, fluid properties, and reservoir heterogeneity. "
            "Primary authority is SPE Surveillance Guidelines, and trending is standard in reservoir management. "
            "Counter arguments focus on measurement uncertainty and interpretation complexity. "
            "Resolution involves integrating surveillance data with reservoir models."
        ),
        key_factors=["Production rates", "Fluid properties", "Reservoir heterogeneity", "Measurement accuracy"],
        primary_authority=["SPE Surveillance Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Measurement uncertainty may obscure true reservoir behavior.",
        counter_arguments=[
            "Water cut and GOR may fluctuate due to operational changes.",
            "Interpretation requires integration with geological and geophysical data."
        ],
        resolution_strategy="Use high-frequency data acquisition and integrate with reservoir simulation.",
        entity_scope="Reservoir and production system",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Surveillance Guidelines"
    ),
    DoctrineBlock(
        topic="Pressure Buildup Test Analysis",
        keywords=["pressure buildup", "well testing", "reservoir pressure", "transient analysis"],
        conclusion_template="Pressure buildup tests are the primary method for estimating reservoir pressure and permeability.",
        reasoning_framework=(
            "Pressure buildup tests involve shutting in a producing well and monitoring pressure recovery. "
            "Analysis of the pressure transient response yields estimates of reservoir permeability, skin factor, and average reservoir pressure. "
            "The method relies on Horner plot interpretation and is standard in well testing. "
            "Key factors include shut-in duration, pressure measurement accuracy, and reservoir heterogeneity. "
            "Primary authority is Horner (1951), and the doctrine is widely accepted. "
            "Counter arguments focus on limitations in heterogeneous reservoirs and operational constraints. "
            "Resolution involves careful test design and data interpretation."
        ),
        key_factors=["Shut-in duration", "Pressure measurement", "Reservoir permeability", "Skin factor"],
        primary_authority=["Horner, D.R. (1951)", "SPE Well Testing Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Heterogeneous reservoirs may complicate pressure transient interpretation.",
        counter_arguments=[
            "Operational constraints may limit test duration and quality.",
            "Complex reservoir geometry may distort pressure response."
        ],
        resolution_strategy="Design tests to minimize operational constraints and use advanced interpretation techniques.",
        entity_scope="Reservoir and wellbore",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Horner, D.R. (1951) Pressure Buildup"
    ),
    DoctrineBlock(
        topic="Material Balance Equation - Reservoir Drive",
        keywords=["material balance", "reservoir drive", "reservoir engineering", "fluid movement"],
        conclusion_template="Material balance equations are fundamental for quantifying reservoir drive mechanisms and reserves.",
        reasoning_framework=(
            "Material balance equations relate changes in reservoir fluid volumes to production and pressure changes, "
            "enabling quantification of drive mechanisms (solution gas, water, gas cap). "
            "The framework involves accounting for produced fluids, reservoir expansion, and aquifer influx. "
            "Key factors include reservoir pressure, produced volumes, and drive mechanism identification. "
            "Primary authority is Schilthuis (1936), and material balance is foundational in reservoir engineering. "
            "Counter arguments focus on uncertainty in input data and aquifer modeling. "
            "Resolution involves integrating material balance with reservoir simulation and surveillance data."
        ),
        key_factors=["Reservoir pressure", "Produced volumes", "Drive mechanism", "Aquifer influx"],
        primary_authority=["Schilthuis, J.A. (1936)", "SPE Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Material balance may be limited by uncertainty in aquifer influx and reservoir heterogeneity.",
        counter_arguments=[
            "Input data uncertainty can lead to erroneous reserve estimates.",
            "Complex reservoirs may require simulation-based approaches."
        ],
        resolution_strategy="Integrate material balance with simulation and update input data regularly.",
        entity_scope="Reservoir",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Schilthuis, J.A. (1936) Material Balance"
    ),
    DoctrineBlock(
        topic="Flowing Bottomhole Pressure Estimation",
        keywords=["bottomhole pressure", "flowing pressure", "estimation", "well performance"],
        conclusion_template="Accurate estimation of flowing bottomhole pressure is critical for well performance analysis.",
        reasoning_framework=(
            "Flowing bottomhole pressure (FBHP) is estimated using surface pressure measurements, wellbore hydraulics, and multiphase flow correlations. "
            "The estimation involves accounting for pressure losses due to friction, hydrostatic head, and acceleration. "
            "Key factors include wellbore geometry, fluid properties, and flow regime. "
            "Primary authority is SPE Well Testing Handbook, and FBHP estimation is standard practice. "
            "Counter arguments focus on uncertainty in multiphase flow modeling and measurement limitations. "
            "Resolution involves using validated correlations and calibration with well test data."
        ),
        key_factors=["Surface pressure", "Wellbore geometry", "Fluid properties", "Flow regime"],
        primary_authority=["SPE Well Testing Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Multiphase flow modeling introduces uncertainty in FBHP estimation.",
        counter_arguments=[
            "Measurement limitations may affect accuracy.",
            "Complex wellbore geometry may require advanced modeling."
        ],
        resolution_strategy="Use validated multiphase flow correlations and calibrate with field data.",
        entity_scope="Wellbore",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Well Testing Handbook"
    ),
    DoctrineBlock(
        topic="Choke Sizing and Critical Flow",
        keywords=["choke sizing", "critical flow", "production optimization", "well control"],
        conclusion_template="Proper choke sizing ensures optimal production rates and prevents critical flow conditions.",
        reasoning_framework=(
            "Choke sizing involves selecting the appropriate choke diameter to regulate well flow and prevent critical flow (sonic velocity). "
            "Critical flow occurs when upstream pressure cannot influence downstream conditions, limiting production rate. "
            "The framework involves calculating flow rates using multiphase correlations and considering well control requirements. "
            "Key factors include upstream pressure, choke diameter, and flow regime. "
            "Primary authority is SPE Production Handbook, and choke sizing is standard in well operations. "
            "Counter arguments focus on uncertainty in flow correlations and operational constraints. "
            "Resolution involves iterative sizing and monitoring well performance."
        ),
        key_factors=["Upstream pressure", "Choke diameter", "Flow regime", "Well control"],
        primary_authority=["SPE Production Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Flow correlations may not accurately predict critical flow in multiphase conditions.",
        counter_arguments=[
            "Operational constraints may limit choke adjustment.",
            "Critical flow may lead to well instability."
        ],
        resolution_strategy="Monitor well performance and adjust choke size as needed.",
        entity_scope="Wellhead and surface facilities",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Production Handbook"
    ),
    DoctrineBlock(
        topic="Production System Optimization - Economic Limit",
        keywords=["production optimization", "economic limit", "system analysis", "cost management"],
        conclusion_template="Production system optimization must account for economic limits to maximize asset value.",
        reasoning_framework=(
            "Economic limit is reached when operating costs exceed revenue from production. "
            "Optimization involves balancing production rates, operational costs, and market prices. "
            "The framework includes nodal analysis, cost modeling, and forecasting. "
            "Key factors include production rate, operating cost, market price, and system constraints. "
            "Primary authority is SPE Asset Management Guidelines. "
            "Counter arguments focus on uncertainty in price forecasting and cost allocation. "
            "Resolution involves regular economic evaluation and scenario analysis."
        ),
        key_factors=["Production rate", "Operating cost", "Market price", "System constraints"],
        primary_authority=["SPE Asset Management Guidelines", "Petroleum Economics Handbook"],
        burden_holder="Asset Manager",
        adversary_position="Uncertainty in price forecasting may affect economic limit determination.",
        counter_arguments=[
            "Cost allocation may be complex in commingled production.",
            "Market volatility can rapidly change economic limits."
        ],
        resolution_strategy="Conduct regular economic reviews and update optimization models.",
        entity_scope="Production system and asset",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Asset Management Guidelines"
    ),
    DoctrineBlock(
        topic="Artificial Lift Selection - Transition from Natural Flow",
        keywords=["artificial lift", "natural flow", "lift selection", "production optimization"],
        conclusion_template="Transition to artificial lift is required when natural flow declines below economic rates.",
        reasoning_framework=(
            "Artificial lift methods (ESP, gas lift, rod pump) are selected based on well characteristics and production requirements. "
            "Transition occurs when reservoir pressure is insufficient for natural flow. "
            "Selection criteria include production rate, fluid properties, well depth, and operational constraints. "
            "Primary authority is SPE Artificial Lift Handbook. "
            "Counter arguments focus on lift method suitability and operational complexity. "
            "Resolution involves detailed well analysis and lift system design."
        ),
        key_factors=["Production rate", "Reservoir pressure", "Fluid properties", "Well depth"],
        primary_authority=["SPE Artificial Lift Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Artificial lift selection may be constrained by well geometry and operational limitations.",
        counter_arguments=[
            "Lift method may not be suitable for all well conditions.",
            "Operational complexity and cost may limit implementation."
        ],
        resolution_strategy="Conduct detailed well analysis and select lift method based on technical and economic criteria.",
        entity_scope="Wellbore and production system",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Artificial Lift Handbook"
    ),
    DoctrineBlock(
        topic="Horizontal Well Productivity - Permian Unconventionals",
        keywords=["horizontal wells", "productivity", "Permian Basin", "unconventional reservoirs"],
        conclusion_template="Horizontal well productivity in Permian unconventionals is governed by fracture network and reservoir properties.",
        reasoning_framework=(
            "Horizontal wells in unconventional reservoirs rely on hydraulic fracturing to enhance productivity. "
            "Key factors include fracture length, spacing, conductivity, and reservoir permeability. "
            "The framework involves modeling stimulated reservoir volume (SRV) and integrating production data. "
            "Primary authority is SPE Unconventional Reservoir Handbook. "
            "Counter arguments focus on uncertainty in fracture modeling and reservoir heterogeneity. "
            "Resolution involves calibration with production history and advanced simulation."
        ),
        key_factors=["Fracture network", "Reservoir permeability", "SRV", "Production history"],
        primary_authority=["SPE Unconventional Reservoir Handbook", "Permian Basin Studies"],
        burden_holder="Reservoir Engineer",
        adversary_position="Fracture modeling uncertainty may affect productivity predictions.",
        counter_arguments=[
            "Reservoir heterogeneity complicates productivity estimation.",
            "SRV may not be accurately defined in all cases."
        ],
        resolution_strategy="Calibrate models with production history and use advanced simulation tools.",
        entity_scope="Permian Basin unconventional reservoirs",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Unconventional Reservoir Handbook"
    ),
    DoctrineBlock(
        topic="Production Data Quality Control and Validation",
        keywords=["production data", "quality control", "validation", "data integrity"],
        conclusion_template="Rigorous quality control and validation are essential for reliable production data analysis.",
        reasoning_framework=(
            "Production data must be validated for accuracy, completeness, and consistency before analysis. "
            "Quality control involves checking for missing values, outliers, and measurement errors. "
            "The framework includes automated validation routines and manual review. "
            "Primary authority is SPE Data Management Guidelines. "
            "Counter arguments focus on resource requirements and potential for human error. "
            "Resolution involves implementing robust data management systems and regular audits."
        ),
        key_factors=["Data accuracy", "Completeness", "Consistency", "Validation routines"],
        primary_authority=["SPE Data Management Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Data Analyst",
        adversary_position="Resource requirements may limit thorough data validation.",
        counter_arguments=[
            "Automated routines may miss context-specific errors.",
            "Human review is subject to error and bias."
        ],
        resolution_strategy="Implement automated and manual validation; conduct regular data audits.",
        entity_scope="Production data systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Data Management Guidelines"
    ),
    DoctrineBlock(
        topic="Multiphase Flow Correlations - Hagedorn-Brown",
        keywords=["multiphase flow", "Hagedorn-Brown", "correlations", "wellbore hydraulics"],
        conclusion_template="Hagedorn-Brown correlation is a standard for estimating multiphase flow pressure drop in vertical wells.",
        reasoning_framework=(
            "Hagedorn-Brown correlation provides empirical equations for pressure drop estimation in vertical wells with multiphase flow. "
            "It accounts for fluid properties, flow regime, and wellbore geometry. "
            "The framework involves calculating pressure losses due to friction, hydrostatic head, and acceleration. "
            "Primary authority is Hagedorn & Brown (1965), and the correlation is widely used in production engineering. "
            "Counter arguments focus on applicability to deviated or horizontal wells. "
            "Resolution involves using alternative correlations for non-vertical wells."
        ),
        key_factors=["Fluid properties", "Flow regime", "Wellbore geometry", "Pressure drop"],
        primary_authority=["Hagedorn & Brown (1965)", "SPE Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Hagedorn-Brown may not be applicable to horizontal or highly deviated wells.",
        counter_arguments=[
            "Empirical nature limits applicability to specific well conditions.",
            "Alternative correlations may be required for complex well geometries."
        ],
        resolution_strategy="Use Hagedorn-Brown for vertical wells; apply alternative correlations as needed.",
        entity_scope="Vertical wells",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hagedorn & Brown (1965) Multiphase Flow"
    ),
    DoctrineBlock(
        topic="Beggs-Brill Correlation - Inclined Multiphase Flow",
        keywords=["Beggs-Brill", "multiphase flow", "inclined wells", "correlations"],
        conclusion_template="Beggs-Brill correlation is preferred for estimating multiphase flow in inclined or horizontal wells.",
        reasoning_framework=(
            "Beggs-Brill correlation provides empirical equations for pressure drop estimation in inclined and horizontal wells with multiphase flow. "
            "It accounts for inclination angle, fluid properties, and flow regime transitions. "
            "The framework involves iterative calculations and selection of appropriate flow regime. "
            "Primary authority is Beggs & Brill (1973), and the correlation is standard for non-vertical wells. "
            "Counter arguments focus on complexity and input data requirements. "
            "Resolution involves careful input data validation and model calibration."
        ),
        key_factors=["Inclination angle", "Fluid properties", "Flow regime", "Pressure drop"],
        primary_authority=["Beggs & Brill (1973)", "SPE Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Beggs-Brill correlation may be complex and require extensive input data.",
        counter_arguments=[
            "Input data quality affects accuracy.",
            "Empirical nature may limit applicability to extreme well conditions."
        ],
        resolution_strategy="Validate input data and calibrate model with field measurements.",
        entity_scope="Inclined and horizontal wells",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Beggs & Brill (1973) Multiphase Flow"
    ),
    DoctrineBlock(
        topic="Decline Curve Analysis - Arps Equations",
        keywords=["decline curve", "Arps equations", "production forecasting", "reservoir engineering"],
        conclusion_template="Arps equations are the industry standard for decline curve analysis and production forecasting.",
        reasoning_framework=(
            "Arps equations model production rate decline over time using exponential, hyperbolic, or harmonic forms. "
            "The framework involves fitting historical production data to the appropriate decline model and forecasting future production. "
            "Key factors include decline rate, initial production, and reservoir drive mechanism. "
            "Primary authority is Arps (1945), and the equations are foundational in reservoir engineering. "
            "Counter arguments focus on limitations in unconventional reservoirs and changing operational conditions. "
            "Resolution involves periodic model recalibration and integration with reservoir simulation."
        ),
        key_factors=["Decline rate", "Initial production", "Reservoir drive mechanism", "Production history"],
        primary_authority=["Arps, J.J. (1945)", "SPE Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Arps equations may not accurately forecast production in unconventional reservoirs.",
        counter_arguments=[
            "Changing operational conditions may alter decline behavior.",
            "Alternative models may be required for complex reservoirs."
        ],
        resolution_strategy="Recalibrate decline models regularly and integrate with simulation results.",
        entity_scope="Reservoir and production system",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Arps, J.J. (1945) Decline Curve"
    ),
    DoctrineBlock(
        topic="Wellbore Storage Effect in Well Testing",
        keywords=["wellbore storage", "well testing", "pressure transient", "reservoir analysis"],
        conclusion_template="Wellbore storage effect must be accounted for in early-time well test analysis.",
        reasoning_framework=(
            "Wellbore storage effect dominates early-time pressure transient response, masking reservoir properties. "
            "The framework involves identifying the wellbore storage period and excluding it from reservoir parameter estimation. "
            "Key factors include wellbore volume, shut-in procedure, and pressure measurement frequency. "
            "Primary authority is SPE Well Testing Handbook. "
            "Counter arguments focus on difficulty in distinguishing wellbore storage from reservoir effects. "
            "Resolution involves using diagnostic plots and advanced interpretation techniques."
        ),
        key_factors=["Wellbore volume", "Shut-in procedure", "Pressure measurement", "Diagnostic plots"],
        primary_authority=["SPE Well Testing Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Distinguishing wellbore storage from reservoir effects may be challenging.",
        counter_arguments=[
            "Measurement frequency may be insufficient.",
            "Complex well geometry complicates interpretation."
        ],
        resolution_strategy="Use diagnostic plots and exclude early-time data from reservoir analysis.",
        entity_scope="Wellbore and reservoir",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Well Testing Handbook"
    ),
    DoctrineBlock(
        topic="Permian Basin Production Characteristics",
        keywords=["Permian Basin", "production characteristics", "unconventional reservoirs", "regional analysis"],
        conclusion_template="Permian Basin production is characterized by high initial rates and rapid decline, governed by unconventional reservoir properties.",
        reasoning_framework=(
            "Permian Basin production relies on horizontal drilling and hydraulic fracturing in unconventional reservoirs. "
            "High initial production rates are followed by rapid decline, reflecting limited reservoir connectivity and fracture-driven flow. "
            "Key factors include reservoir heterogeneity, fracture network, and operational practices. "
            "Primary authority is Permian Basin Studies and SPE Unconventional Reservoir Handbook. "
            "Counter arguments focus on variability across sub-basins and uncertainty in long-term forecasts. "
            "Resolution involves integrating regional studies and production history analysis."
        ),
        key_factors=["Reservoir heterogeneity", "Fracture network", "Operational practices", "Production history"],
        primary_authority=["Permian Basin Studies", "SPE Unconventional Reservoir Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Sub-basin variability complicates production forecasting.",
        counter_arguments=[
            "Long-term forecasts may be uncertain.",
            "Operational practices vary across operators."
        ],
        resolution_strategy="Integrate regional studies and calibrate models with production history.",
        entity_scope="Permian Basin unconventional reservoirs",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Permian Basin Studies"
    ),
    DoctrineBlock(
        topic="Production Allocation and Commingled Flow",
        keywords=["production allocation", "commingled flow", "multi-well analysis", "data management"],
        conclusion_template="Production allocation in commingled flow systems requires rigorous data management and allocation algorithms.",
        reasoning_framework=(
            "Commingled flow occurs when multiple wells or zones produce into a common system, complicating production allocation. "
            "The framework involves using allocation algorithms based on well tests, tracer studies, and production data. "
            "Key factors include well test frequency, tracer reliability, and allocation accuracy. "
            "Primary authority is SPE Production Allocation Guidelines. "
            "Counter arguments focus on allocation uncertainty and operational complexity. "
            "Resolution involves regular well testing and integration of allocation algorithms."
        ),
        key_factors=["Well test frequency", "Tracer reliability", "Allocation accuracy", "Data management"],
        primary_authority=["SPE Production Allocation Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Allocation uncertainty may affect revenue distribution and reservoir management.",
        counter_arguments=[
            "Operational complexity increases with number of commingled wells.",
            "Tracer studies may be limited by cost and logistics."
        ],
        resolution_strategy="Conduct regular well tests and use robust allocation algorithms.",
        entity_scope="Commingled production systems",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Production Allocation Guidelines"
    ),
    DoctrineBlock(
        topic="Reservoir Surveillance - Integrated Approach",
        keywords=["reservoir surveillance", "integrated approach", "production monitoring", "data integration"],
        conclusion_template="Integrated reservoir surveillance combines production, pressure, and geophysical data for optimal reservoir management.",
        reasoning_framework=(
            "Integrated surveillance involves combining production data, pressure measurements, and geophysical surveys to monitor reservoir performance. "
            "The framework enables early detection of breakthrough events and optimization of production strategy. "
            "Key factors include data integration, surveillance frequency, and interpretation accuracy. "
            "Primary authority is SPE Surveillance Guidelines. "
            "Counter arguments focus on data integration challenges and resource requirements. "
            "Resolution involves implementing data management systems and regular surveillance reviews."
        ),
        key_factors=["Data integration", "Surveillance frequency", "Interpretation accuracy", "Resource allocation"],
        primary_authority=["SPE Surveillance Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Data integration challenges may limit surveillance effectiveness.",
        counter_arguments=[
            "Resource allocation may constrain surveillance frequency.",
            "Interpretation requires multidisciplinary expertise."
        ],
        resolution_strategy="Implement robust data management systems and multidisciplinary review teams.",
        entity_scope="Reservoir and production system",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Surveillance Guidelines"
    ),
    DoctrineBlock(
        topic="Reservoir Drive Mechanisms - Classification",
        keywords=["reservoir drive", "mechanisms", "classification", "reservoir engineering"],
        conclusion_template="Reservoir drive mechanisms are classified as solution gas, water, gas cap, or combination drives.",
        reasoning_framework=(
            "Drive mechanisms determine reservoir energy and production behavior. "
            "Classification includes solution gas drive, water drive, gas cap drive, and combination drive. "
            "The framework involves identifying drive mechanism based on production data, pressure trends, and material balance analysis. "
            "Primary authority is SPE Petroleum Engineering Handbook. "
            "Counter arguments focus on mixed or transitional drive mechanisms. "
            "Resolution involves integrating material balance and surveillance data."
        ),
        key_factors=["Production data", "Pressure trends", "Material balance", "Drive mechanism identification"],
        primary_authority=["SPE Petroleum Engineering Handbook", "Reservoir Engineering Textbooks"],
        burden_holder="Reservoir Engineer",
        adversary_position="Mixed drive mechanisms may complicate classification.",
        counter_arguments=[
            "Transitional drives may require advanced modeling.",
            "Material balance may be limited by input data uncertainty."
        ],
        resolution_strategy="Integrate material balance and surveillance data for accurate classification.",
        entity_scope="Reservoir",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Petroleum Engineering Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Surveillance and Optimization",
        keywords=["reservoir management", "surveillance", "optimization", "production strategy"],
        conclusion_template="Effective reservoir management requires continuous surveillance and optimization of production strategy.",
        reasoning_framework=(
            "Reservoir management involves monitoring production, pressure, and fluid properties to optimize recovery. "
            "Surveillance enables early detection of breakthrough events and adjustment of production strategy. "
            "Key factors include surveillance frequency, data integration, and optimization techniques. "
            "Primary authority is SPE Reservoir Management Guidelines. "
            "Counter arguments focus on resource allocation and surveillance challenges. "
            "Resolution involves implementing surveillance protocols and optimization models."
        ),
        key_factors=["Surveillance frequency", "Data integration", "Optimization techniques", "Resource allocation"],
        primary_authority=["SPE Reservoir Management Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Resource allocation may constrain surveillance and optimization efforts.",
        counter_arguments=[
            "Surveillance challenges may limit data quality.",
            "Optimization requires multidisciplinary expertise."
        ],
        resolution_strategy="Implement surveillance protocols and multidisciplinary optimization teams.",
        entity_scope="Reservoir and production system",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Reservoir Management Guidelines"
    ),
    DoctrineBlock(
        topic="Reservoir Simulation - History Matching",
        keywords=["reservoir simulation", "history matching", "model calibration", "production forecasting"],
        conclusion_template="History matching is essential for calibrating reservoir simulation models and improving production forecasts.",
        reasoning_framework=(
            "History matching involves adjusting simulation model parameters to fit historical production and pressure data. "
            "The framework includes iterative parameter adjustment, error minimization, and integration of surveillance data. "
            "Key factors include model complexity, data quality, and calibration accuracy. "
            "Primary authority is SPE Simulation Guidelines. "
            "Counter arguments focus on uncertainty in input data and model limitations. "
            "Resolution involves regular model updates and integration with surveillance data."
        ),
        key_factors=["Model complexity", "Data quality", "Calibration accuracy", "Surveillance data"],
        primary_authority=["SPE Simulation Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Input data uncertainty may limit history matching accuracy.",
        counter_arguments=[
            "Model limitations may affect calibration.",
            "Surveillance data may be incomplete."
        ],
        resolution_strategy="Update models regularly and integrate comprehensive surveillance data.",
        entity_scope="Reservoir simulation models",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Simulation Guidelines"
    ),
    DoctrineBlock(
        topic="Reservoir Pressure Maintenance - Water Injection",
        keywords=["pressure maintenance", "water injection", "reservoir engineering", "secondary recovery"],
        conclusion_template="Water injection is the primary method for reservoir pressure maintenance and secondary recovery.",
        reasoning_framework=(
            "Water injection maintains reservoir pressure and enhances recovery by displacing oil towards production wells. "
            "The framework involves designing injection patterns, monitoring injection rates, and integrating surveillance data. "
            "Key factors include injection rate, reservoir permeability, and sweep efficiency. "
            "Primary authority is SPE Waterflooding Handbook. "
            "Counter arguments focus on injection-induced reservoir damage and operational complexity. "
            "Resolution involves careful injection design and monitoring."
        ),
        key_factors=["Injection rate", "Reservoir permeability", "Sweep efficiency", "Surveillance data"],
        primary_authority=["SPE Waterflooding Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Water injection may induce reservoir damage or operational complexity.",
        counter_arguments=[
            "Injection-induced damage may reduce permeability.",
            "Operational complexity increases with injection pattern design."
        ],
        resolution_strategy="Design injection patterns carefully and monitor injection performance.",
        entity_scope="Reservoir and injection wells",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Waterflooding Handbook"
    ),
    DoctrineBlock(
        topic="Gas Lift Optimization - Production Enhancement",
        keywords=["gas lift", "optimization", "production enhancement", "artificial lift"],
        conclusion_template="Gas lift optimization enhances production by adjusting injection rates and lift gas distribution.",
        reasoning_framework=(
            "Gas lift optimization involves adjusting injection rates, lift gas distribution, and monitoring well performance. "
            "The framework includes nodal analysis, production monitoring, and iterative optimization. "
            "Key factors include injection rate, lift gas availability, and well response. "
            "Primary authority is SPE Gas Lift Handbook. "
            "Counter arguments focus on operational complexity and gas supply constraints. "
            "Resolution involves regular performance monitoring and optimization."
        ),
        key_factors=["Injection rate", "Lift gas availability", "Well response", "Production monitoring"],
        primary_authority=["SPE Gas Lift Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Gas supply constraints may limit optimization.",
        counter_arguments=[
            "Operational complexity increases with multiple wells.",
            "Lift gas distribution may be affected by system constraints."
        ],
        resolution_strategy="Monitor well performance and optimize injection rates regularly.",
        entity_scope="Gas lift wells and production system",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Gas Lift Handbook"
    ),
    DoctrineBlock(
        topic="ESP Selection and Optimization",
        keywords=["ESP", "selection", "optimization", "artificial lift", "production enhancement"],
        conclusion_template="ESP selection and optimization is based on well characteristics, production requirements, and operational constraints.",
        reasoning_framework=(
            "ESP (Electric Submersible Pump) selection involves evaluating well depth, production rate, fluid properties, and operational constraints. "
            "Optimization includes monitoring pump performance, adjusting operational parameters, and integrating surveillance data. "
            "Key factors include pump capacity, well depth, fluid properties, and system reliability. "
            "Primary authority is SPE ESP Handbook. "
            "Counter arguments focus on operational complexity and reliability issues. "
            "Resolution involves regular performance monitoring and maintenance."
        ),
        key_factors=["Pump capacity", "Well depth", "Fluid properties", "System reliability"],
        primary_authority=["SPE ESP Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="ESP reliability issues may affect production optimization.",
        counter_arguments=[
            "Operational complexity increases with deep wells.",
            "Maintenance requirements may be significant."
        ],
        resolution_strategy="Monitor pump performance and conduct regular maintenance.",
        entity_scope="ESP wells and production system",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE ESP Handbook"
    ),
    DoctrineBlock(
        topic="Rod Pump Optimization - Artificial Lift",
        keywords=["rod pump", "optimization", "artificial lift", "production enhancement"],
        conclusion_template="Rod pump optimization involves adjusting stroke length, speed, and pump design for enhanced production.",
        reasoning_framework=(
            "Rod pump optimization includes adjusting stroke length, speed, and pump design based on well characteristics and production requirements. "
            "The framework involves monitoring pump performance, diagnosing operational issues, and integrating surveillance data. "
            "Key factors include stroke length, pump speed, well depth, and fluid properties. "
            "Primary authority is SPE Rod Pump Handbook. "
            "Counter arguments focus on operational complexity and maintenance requirements. "
            "Resolution involves regular performance monitoring and maintenance."
        ),
        key_factors=["Stroke length", "Pump speed", "Well depth", "Fluid properties"],
        primary_authority=["SPE Rod Pump Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Rod pump maintenance requirements may affect optimization.",
        counter_arguments=[
            "Operational complexity increases with deep wells.",
            "Pump design may need frequent adjustment."
        ],
        resolution_strategy="Monitor pump performance and conduct regular maintenance.",
        entity_scope="Rod pump wells and production system",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Rod Pump Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Characterization - Core and Log Analysis",
        keywords=["reservoir characterization", "core analysis", "log analysis", "petrophysics"],
        conclusion_template="Core and log analysis are essential for reservoir characterization and property estimation.",
        reasoning_framework=(
            "Reservoir characterization involves analyzing core samples and well logs to estimate porosity, permeability, and fluid saturation. "
            "The framework includes integrating petrophysical data, geological interpretation, and production history. "
            "Key factors include core quality, log interpretation accuracy, and data integration. "
            "Primary authority is SPE Petrophysics Handbook. "
            "Counter arguments focus on data quality and interpretation uncertainty. "
            "Resolution involves integrating multiple data sources and regular review."
        ),
        key_factors=["Core quality", "Log interpretation accuracy", "Data integration", "Production history"],
        primary_authority=["SPE Petrophysics Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Petrophysicist",
        adversary_position="Data quality and interpretation uncertainty may affect characterization accuracy.",
        counter_arguments=[
            "Core samples may be limited or damaged.",
            "Log interpretation may be subjective."
        ],
        resolution_strategy="Integrate multiple data sources and conduct regular reviews.",
        entity_scope="Reservoir",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Petrophysics Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Modeling - Static and Dynamic Models",
        keywords=["reservoir modeling", "static model", "dynamic model", "simulation"],
        conclusion_template="Static and dynamic reservoir models are essential for production forecasting and optimization.",
        reasoning_framework=(
            "Static models define reservoir geometry, properties, and structure, while dynamic models simulate fluid flow and production behavior. "
            "The framework involves integrating geological, petrophysical, and production data. "
            "Key factors include model accuracy, data integration, and calibration. "
            "Primary authority is SPE Reservoir Modeling Guidelines. "
            "Counter arguments focus on model limitations and data uncertainty. "
            "Resolution involves regular model updates and integration with surveillance data."
        ),
        key_factors=["Model accuracy", "Data integration", "Calibration", "Surveillance data"],
        primary_authority=["SPE Reservoir Modeling Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Model limitations and data uncertainty may affect forecasting accuracy.",
        counter_arguments=[
            "Static models may not capture dynamic behavior.",
            "Data integration may be challenging."
        ],
        resolution_strategy="Update models regularly and integrate comprehensive data sources.",
        entity_scope="Reservoir models",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Reservoir Modeling Guidelines"
    ),
    DoctrineBlock(
        topic="Reservoir Fluid Characterization",
        keywords=["fluid characterization", "reservoir fluids", "PVT analysis", "petrophysics"],
        conclusion_template="Reservoir fluid characterization is essential for production forecasting and reservoir management.",
        reasoning_framework=(
            "Fluid characterization involves PVT (Pressure-Volume-Temperature) analysis to estimate fluid properties and phase behavior. "
            "The framework includes laboratory analysis, integration with production data, and reservoir modeling. "
            "Key factors include sample quality, PVT analysis accuracy, and data integration. "
            "Primary authority is SPE Fluid Characterization Handbook. "
            "Counter arguments focus on sample quality and laboratory limitations. "
            "Resolution involves integrating multiple data sources and regular review."
        ),
        key_factors=["Sample quality", "PVT analysis accuracy", "Data integration", "Production history"],
        primary_authority=["SPE Fluid Characterization Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Petrophysicist",
        adversary_position="Sample quality and laboratory limitations may affect characterization accuracy.",
        counter_arguments=[
            "Sample contamination may affect results.",
            "Laboratory analysis may be limited by equipment."
        ],
        resolution_strategy="Integrate multiple data sources and conduct regular reviews.",
        entity_scope="Reservoir fluids",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Fluid Characterization Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Enhanced Oil Recovery (EOR)",
        keywords=["reservoir management", "EOR", "enhanced oil recovery", "production optimization"],
        conclusion_template="EOR techniques are applied to maximize recovery and optimize reservoir management.",
        reasoning_framework=(
            "Enhanced Oil Recovery (EOR) involves applying chemical, thermal, or gas injection techniques to increase recovery. "
            "The framework includes screening for suitable EOR methods, pilot testing, and integrating surveillance data. "
            "Key factors include reservoir properties, EOR method suitability, and operational constraints. "
            "Primary authority is SPE EOR Handbook. "
            "Counter arguments focus on operational complexity and economic viability. "
            "Resolution involves pilot testing and economic evaluation."
        ),
        key_factors=["Reservoir properties", "EOR method suitability", "Operational constraints", "Economic evaluation"],
        primary_authority=["SPE EOR Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Operational complexity and economic viability may limit EOR implementation.",
        counter_arguments=[
            "EOR methods may not be suitable for all reservoirs.",
            "Economic evaluation may be uncertain."
        ],
        resolution_strategy="Conduct pilot testing and regular economic evaluation.",
        entity_scope="Reservoir and production system",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE EOR Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Integrated Asset Modeling",
        keywords=["reservoir management", "integrated asset modeling", "production optimization", "system analysis"],
        conclusion_template="Integrated asset modeling combines reservoir, well, and surface facility models for optimal production management.",
        reasoning_framework=(
            "Integrated asset modeling involves combining reservoir, well, and surface facility models to optimize production and asset value. "
            "The framework includes nodal analysis, production forecasting, and economic evaluation. "
            "Key factors include model integration, data quality, and optimization techniques. "
            "Primary authority is SPE Asset Management Guidelines. "
            "Counter arguments focus on model complexity and data integration challenges. "
            "Resolution involves regular model updates and multidisciplinary review."
        ),
        key_factors=["Model integration", "Data quality", "Optimization techniques", "Economic evaluation"],
        primary_authority=["SPE Asset Management Guidelines", "Petroleum Engineering Handbook"],
        burden_holder="Asset Manager",
        adversary_position="Model complexity and data integration challenges may affect optimization.",
        counter_arguments=[
            "Integration may require multidisciplinary expertise.",
            "Data quality affects model accuracy."
        ],
        resolution_strategy="Update models regularly and conduct multidisciplinary reviews.",
        entity_scope="Production system and asset",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Asset Management Guidelines"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Unconventional Asset Optimization",
        keywords=["reservoir management", "unconventional asset", "optimization", "Permian Basin"],
        conclusion_template="Optimization of unconventional assets requires integrating reservoir, completion, and production data.",
        reasoning_framework=(
            "Unconventional asset optimization involves integrating reservoir, completion, and production data to maximize recovery. "
            "The framework includes advanced simulation, production monitoring, and completion design optimization. "
            "Key factors include reservoir heterogeneity, completion design, and production history. "
            "Primary authority is SPE Unconventional Asset Optimization Handbook. "
            "Counter arguments focus on data integration challenges and operational complexity. "
            "Resolution involves multidisciplinary teams and advanced modeling."
        ),
        key_factors=["Reservoir heterogeneity", "Completion design", "Production history", "Data integration"],
        primary_authority=["SPE Unconventional Asset Optimization Handbook", "Permian Basin Studies"],
        burden_holder="Asset Manager",
        adversary_position="Data integration challenges and operational complexity may affect optimization.",
        counter_arguments=[
            "Multidisciplinary expertise required.",
            "Operational complexity increases with asset scale."
        ],
        resolution_strategy="Form multidisciplinary teams and use advanced modeling tools.",
        entity_scope="Unconventional assets",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Unconventional Asset Optimization Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Data Analytics and Machine Learning",
        keywords=["reservoir management", "data analytics", "machine learning", "production optimization"],
        conclusion_template="Data analytics and machine learning enhance reservoir management through predictive modeling and optimization.",
        reasoning_framework=(
            "Data analytics and machine learning are applied to production and reservoir data for predictive modeling and optimization. "
            "The framework includes data preprocessing, model training, and integration with surveillance data. "
            "Key factors include data quality, model accuracy, and integration with engineering workflows. "
            "Primary authority is SPE Data Analytics Handbook. "
            "Counter arguments focus on data quality and model interpretability. "
            "Resolution involves regular model validation and integration with engineering expertise."
        ),
        key_factors=["Data quality", "Model accuracy", "Integration with engineering workflows", "Surveillance data"],
        primary_authority=["SPE Data Analytics Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Data Scientist",
        adversary_position="Data quality and model interpretability may affect optimization.",
        counter_arguments=[
            "Model results may be difficult to interpret.",
            "Data quality affects predictive accuracy."
        ],
        resolution_strategy="Validate models regularly and integrate with engineering workflows.",
        entity_scope="Reservoir and production system",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Data Analytics Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Digital Oilfield",
        keywords=["reservoir management", "digital oilfield", "automation", "production optimization"],
        conclusion_template="Digital oilfield technologies automate production optimization and enhance reservoir management.",
        reasoning_framework=(
            "Digital oilfield technologies include automation, remote monitoring, and data integration for production optimization. "
            "The framework involves deploying sensors, integrating data streams, and automating operational decisions. "
            "Key factors include sensor reliability, data integration, and operational automation. "
            "Primary authority is SPE Digital Oilfield Handbook. "
            "Counter arguments focus on technology adoption and integration challenges. "
            "Resolution involves phased deployment and regular system review."
        ),
        key_factors=["Sensor reliability", "Data integration", "Operational automation", "System review"],
        primary_authority=["SPE Digital Oilfield Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Technology adoption and integration challenges may affect optimization.",
        counter_arguments=[
            "Integration may require significant investment.",
            "Operational automation may be limited by system reliability."
        ],
        resolution_strategy="Deploy technologies in phases and conduct regular system reviews.",
        entity_scope="Production system and reservoir",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Digital Oilfield Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Production Forecasting",
        keywords=["reservoir management", "production forecasting", "decline curve analysis", "simulation"],
        conclusion_template="Production forecasting is based on decline curve analysis and reservoir simulation.",
        reasoning_framework=(
            "Production forecasting involves fitting historical production data to decline curve models and integrating with reservoir simulation. "
            "The framework includes model calibration, scenario analysis, and integration with surveillance data. "
            "Key factors include decline rate, model accuracy, and data integration. "
            "Primary authority is SPE Production Forecasting Handbook. "
            "Counter arguments focus on model limitations and data uncertainty. "
            "Resolution involves regular model updates and scenario analysis."
        ),
        key_factors=["Decline rate", "Model accuracy", "Data integration", "Surveillance data"],
        primary_authority=["SPE Production Forecasting Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Reservoir Engineer",
        adversary_position="Model limitations and data uncertainty may affect forecasting accuracy.",
        counter_arguments=[
            "Decline curve models may not fit unconventional reservoirs.",
            "Simulation may be limited by input data quality."
        ],
        resolution_strategy="Update models regularly and conduct scenario analysis.",
        entity_scope="Reservoir and production system",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Production Forecasting Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Well Intervention and Workover",
        keywords=["reservoir management", "well intervention", "workover", "production optimization"],
        conclusion_template="Well intervention and workover operations are essential for maintaining and optimizing production.",
        reasoning_framework=(
            "Well intervention and workover operations include mechanical, chemical, and hydraulic techniques to restore or enhance production. "
            "The framework involves diagnosing production issues, selecting appropriate intervention techniques, and monitoring results. "
            "Key factors include intervention technique, well condition, and production response. "
            "Primary authority is SPE Well Intervention Handbook. "
            "Counter arguments focus on operational complexity and cost. "
            "Resolution involves careful planning and post-intervention monitoring."
        ),
        key_factors=["Intervention technique", "Well condition", "Production response", "Monitoring"],
        primary_authority=["SPE Well Intervention Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Operational complexity and cost may limit intervention effectiveness.",
        counter_arguments=[
            "Intervention may not restore production in all cases.",
            "Cost may exceed economic benefit."
        ],
        resolution_strategy="Plan interventions carefully and monitor production response.",
        entity_scope="Wellbore and production system",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Well Intervention Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Well Integrity",
        keywords=["reservoir management", "well integrity", "production optimization", "safety"],
        conclusion_template="Well integrity management is essential for safe and optimized production operations.",
        reasoning_framework=(
            "Well integrity management involves monitoring well condition, conducting regular inspections, and implementing safety protocols. "
            "The framework includes integrity testing, surveillance, and remediation of integrity issues. "
            "Key factors include well condition, integrity testing, and safety protocols. "
            "Primary authority is SPE Well Integrity Handbook. "
            "Counter arguments focus on operational complexity and resource requirements. "
            "Resolution involves regular inspections and implementation of safety protocols."
        ),
        key_factors=["Well condition", "Integrity testing", "Safety protocols", "Surveillance"],
        primary_authority=["SPE Well Integrity Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Operational complexity and resource requirements may affect integrity management.",
        counter_arguments=[
            "Integrity issues may be difficult to detect.",
            "Resource allocation may limit inspection frequency."
        ],
        resolution_strategy="Conduct regular inspections and implement safety protocols.",
        entity_scope="Wellbore and production system",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Well Integrity Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Production Optimization Workflow",
        keywords=["reservoir management", "production optimization", "workflow", "system analysis"],
        conclusion_template="Production optimization workflow integrates surveillance, modeling, and operational adjustments for maximum recovery.",
        reasoning_framework=(
            "Production optimization workflow involves integrating surveillance data, modeling, and operational adjustments to maximize recovery. "
            "The framework includes regular surveillance, model updates, and scenario analysis. "
            "Key factors include workflow design, data integration, and optimization techniques. "
            "Primary authority is SPE Production Optimization Handbook. "
            "Counter arguments focus on workflow complexity and resource requirements. "
            "Resolution involves regular workflow review and multidisciplinary teams."
        ),
        key_factors=["Workflow design", "Data integration", "Optimization techniques", "Surveillance"],
        primary_authority=["SPE Production Optimization Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Workflow complexity and resource requirements may affect optimization.",
        counter_arguments=[
            "Workflow may be difficult to implement in large assets.",
            "Resource allocation may constrain optimization efforts."
        ],
        resolution_strategy="Review workflow regularly and form multidisciplinary teams.",
        entity_scope="Production system and reservoir",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Production Optimization Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Surveillance Technology Selection",
        keywords=["reservoir management", "surveillance technology", "selection", "production optimization"],
        conclusion_template="Selection of surveillance technologies is based on reservoir characteristics, production requirements, and operational constraints.",
        reasoning_framework=(
            "Surveillance technology selection involves evaluating reservoir characteristics, production requirements, and operational constraints. "
            "The framework includes screening available technologies, pilot testing, and integrating surveillance data. "
            "Key factors include technology suitability, data quality, and operational complexity. "
            "Primary authority is SPE Surveillance Technology Handbook. "
            "Counter arguments focus on technology adoption and integration challenges. "
            "Resolution involves pilot testing and regular technology review."
        ),
        key_factors=["Technology suitability", "Data quality", "Operational complexity", "Surveillance data"],
        primary_authority=["SPE Surveillance Technology Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Technology adoption and integration challenges may affect surveillance effectiveness.",
        counter_arguments=[
            "Technology may not be suitable for all reservoirs.",
            "Integration may require significant investment."
        ],
        resolution_strategy="Conduct pilot testing and regular technology reviews.",
        entity_scope="Reservoir and production system",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Surveillance Technology Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Completions Optimization",
        keywords=["reservoir management", "completions optimization", "production enhancement", "well design"],
        conclusion_template="Completions optimization enhances production by adjusting well design and completion techniques.",
        reasoning_framework=(
            "Completions optimization involves adjusting well design and completion techniques to enhance production. "
            "The framework includes evaluating completion effectiveness, monitoring production response, and integrating surveillance data. "
            "Key factors include completion design, production response, and surveillance data. "
            "Primary authority is SPE Completions Optimization Handbook. "
            "Counter arguments focus on operational complexity and cost. "
            "Resolution involves regular completion reviews and performance monitoring."
        ),
        key_factors=["Completion design", "Production response", "Surveillance data", "Operational complexity"],
        primary_authority=["SPE Completions Optimization Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Operational complexity and cost may limit optimization.",
        counter_arguments=[
            "Completion effectiveness may vary across wells.",
            "Cost may exceed economic benefit."
        ],
        resolution_strategy="Review completions regularly and monitor production response.",
        entity_scope="Wellbore and production system",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Completions Optimization Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Hydraulic Fracturing Optimization",
        keywords=["reservoir management", "hydraulic fracturing", "optimization", "production enhancement"],
        conclusion_template="Hydraulic fracturing optimization maximizes production by adjusting fracture design and monitoring response.",
        reasoning_framework=(
            "Hydraulic fracturing optimization involves adjusting fracture design, monitoring production response, and integrating surveillance data. "
            "The framework includes evaluating fracture effectiveness, calibrating models, and scenario analysis. "
            "Key factors include fracture design, production response, and surveillance data. "
            "Primary authority is SPE Hydraulic Fracturing Handbook. "
            "Counter arguments focus on operational complexity and cost. "
            "Resolution involves regular fracture reviews and performance monitoring."
        ),
        key_factors=["Fracture design", "Production response", "Surveillance data", "Operational complexity"],
        primary_authority=["SPE Hydraulic Fracturing Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Operational complexity and cost may limit optimization.",
        counter_arguments=[
            "Fracture effectiveness may vary across wells.",
            "Cost may exceed economic benefit."
        ],
        resolution_strategy="Review fracture designs regularly and monitor production response.",
        entity_scope="Wellbore and production system",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Hydraulic Fracturing Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Well Spacing Optimization",
        keywords=["reservoir management", "well spacing", "optimization", "production enhancement"],
        conclusion_template="Well spacing optimization maximizes recovery by balancing reservoir drainage and operational efficiency.",
        reasoning_framework=(
            "Well spacing optimization involves balancing reservoir drainage, production rates, and operational efficiency. "
            "The framework includes scenario analysis, production monitoring, and integration with reservoir models. "
            "Key factors include spacing design, production response, and surveillance data. "
            "Primary authority is SPE Well Spacing Handbook. "
            "Counter arguments focus on operational complexity and cost. "
            "Resolution involves regular spacing reviews and performance monitoring."
        ),
        key_factors=["Spacing design", "Production response", "Surveillance data", "Operational complexity"],
        primary_authority=["SPE Well Spacing Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Operational complexity and cost may limit optimization.",
        counter_arguments=[
            "Spacing effectiveness may vary across reservoirs.",
            "Cost may exceed economic benefit."
        ],
        resolution_strategy="Review spacing designs regularly and monitor production response.",
        entity_scope="Reservoir and production system",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Well Spacing Handbook"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Production Surveillance Workflow",
        keywords=["reservoir management", "production surveillance", "workflow", "data integration"],
        conclusion_template="Production surveillance workflow integrates data acquisition, analysis, and operational adjustments for optimized production.",
        reasoning_framework=(
            "Production surveillance workflow involves integrating data acquisition, analysis, and operational adjustments to optimize production. "
            "The framework includes regular data acquisition, analysis, and scenario evaluation. "
            "Key factors include workflow design, data integration, and optimization techniques. "
            "Primary authority is SPE Production Surveillance Handbook. "
            "Counter arguments focus on workflow complexity and resource requirements. "
            "Resolution involves regular workflow review and multidisciplinary teams."
        ),
        key_factors=["Workflow design", "Data integration", "Optimization techniques", "Surveillance"],
        primary_authority=["SPE Production Surveillance Handbook", "Petroleum Engineering Handbook"],
        burden_holder="Production Engineer",
        adversary_position="Workflow complexity and resource requirements may affect optimization.",
        counter_arguments=[
            "Workflow may be difficult to implement in large assets.",
            "Resource allocation may constrain optimization efforts."
        ],
        resolution_strategy="Review workflow regularly and form multidisciplinary teams.",
        entity_scope="Production system and reservoir",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Production Surveillance Handbook"
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