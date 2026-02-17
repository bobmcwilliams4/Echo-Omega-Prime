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
        topic="Material Balance Equation - Havlena-Odeh Method",
        keywords=["material balance", "Havlena-Odeh", "reservoir management", "OOIP", "OGIP", "drive mechanism"],
        conclusion_template="The Havlena-Odeh material balance method determines the original hydrocarbons in place and identifies the dominant drive mechanism based on reservoir production and pressure data.",
        reasoning_framework=(
            "1. Gather production, injection, and pressure data for the reservoir.\n"
            "2. Apply the Havlena-Odeh material balance equation, separating terms for each drive mechanism (water, gas, gravity).\n"
            "3. Plot relevant variables (e.g., F vs. Eo) to identify linear relationships indicating dominant drive.\n"
            "4. Estimate OOIP or OGIP using slope/intercept analysis.\n"
            "5. Validate against volumetric and simulation estimates.\n"
            "6. Consider uncertainties in PVT, pressure, and production measurements.\n"
            "7. Reconcile discrepancies with additional data or alternative methods.\n"
            "8. Document assumptions and limitations in the analysis.\n"
            "9. Use results to inform reservoir management decisions, such as infill drilling or secondary recovery.\n"
            "10. Update calculations periodically as new data becomes available."
        ),
        key_factors=[
            "Production history accuracy",
            "Pressure measurement reliability",
            "PVT property determination",
            "Reservoir heterogeneity",
            "Aquifer support",
            "Gas cap presence",
            "Fluid compressibility"
        ],
        primary_authority=[
            "Havlena, D. and Odeh, A.S. (1963) Material Balance Method for Reservoirs with Multiple Drive Mechanisms",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Material balance may not accurately reflect complex reservoirs with significant heterogeneity or uncertain aquifer behavior.",
        counter_arguments=[
            "Integrate material balance with simulation and volumetric methods for cross-validation.",
            "Use advanced pressure transient analysis to refine drive mechanism identification.",
            "Apply uncertainty quantification to material balance results."
        ],
        resolution_strategy="Triangulate material balance findings with simulation and volumetric estimates; update with new data and advanced analytics.",
        entity_scope="Conventional oil and gas reservoirs",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Havlena-Odeh (1963), SPE 462"
    ),
    DoctrineBlock(
        topic="Drive Mechanism Identification",
        keywords=["drive mechanism", "reservoir management", "material balance", "water drive", "gas cap", "solution gas"],
        conclusion_template="Drive mechanism identification is achieved by analyzing production, pressure, and material balance data to determine the dominant reservoir energy source.",
        reasoning_framework=(
            "1. Review production and pressure history for characteristic trends (e.g., pressure decline rate).\n"
            "2. Apply material balance equations to separate contributions from water, gas, and solution gas drives.\n"
            "3. Analyze water production and gas-oil ratio changes to infer water or gas cap drive.\n"
            "4. Use reservoir simulation to validate drive mechanism hypotheses.\n"
            "5. Consider geological and petrophysical data (e.g., aquifer size, gas cap extent).\n"
            "6. Document uncertainties and alternative interpretations.\n"
            "7. Integrate findings into reservoir management strategy."
        ),
        key_factors=[
            "Pressure decline rate",
            "Water production trends",
            "Gas-oil ratio evolution",
            "Reservoir connectivity",
            "Aquifer strength",
            "Gas cap size"
        ],
        primary_authority=[
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering",
            "Dake, Fundamentals of Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Drive mechanism identification may be ambiguous in reservoirs with mixed or complex energy sources.",
        counter_arguments=[
            "Use multiple diagnostic tools and cross-validation.",
            "Employ reservoir simulation for scenario testing.",
            "Update drive mechanism assessment as new data emerges."
        ],
        resolution_strategy="Iterative assessment using material balance, simulation, and production diagnostics.",
        entity_scope="All reservoir types",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Craft & Hawkins, 1991"
    ),
    DoctrineBlock(
        topic="Recovery Factor Estimation by Drive Type",
        keywords=["recovery factor", "drive mechanism", "water drive", "gas cap", "solution gas", "reservoir management"],
        conclusion_template="Recovery factor is estimated based on the dominant drive mechanism, reservoir properties, and historical analogs.",
        reasoning_framework=(
            "1. Identify dominant drive mechanism using material balance and production diagnostics.\n"
            "2. Review recovery factor ranges for each drive type (water drive: 35-60%, gas cap: 15-40%, solution gas: 5-20%).\n"
            "3. Adjust estimates based on reservoir heterogeneity, permeability, and sweep efficiency.\n"
            "4. Compare with analog reservoirs and published case studies.\n"
            "5. Use simulation to refine recovery factor estimates.\n"
            "6. Document assumptions and uncertainties.\n"
            "7. Update recovery factor as new production and reservoir data becomes available."
        ),
        key_factors=[
            "Drive mechanism",
            "Sweep efficiency",
            "Reservoir heterogeneity",
            "Analog performance",
            "Simulation results"
        ],
        primary_authority=[
            "Dake, Fundamentals of Reservoir Engineering",
            "SPE Monograph 1: Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Recovery factor estimates may be overly optimistic or pessimistic due to data limitations.",
        counter_arguments=[
            "Use conservative estimates and sensitivity analysis.",
            "Refine with simulation and analog comparison.",
            "Document uncertainty ranges."
        ],
        resolution_strategy="Triangulate recovery factor using material balance, simulation, and analog data.",
        entity_scope="Conventional reservoirs",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="Dake, 1978"
    ),
    DoctrineBlock(
        topic="Waterflood Design - Pattern Selection",
        keywords=["waterflood", "pattern selection", "reservoir management", "secondary recovery", "five-spot", "line drive"],
        conclusion_template="Waterflood pattern selection is based on reservoir geometry, well spacing, heterogeneity, and operational constraints.",
        reasoning_framework=(
            "1. Evaluate reservoir geometry and boundaries.\n"
            "2. Assess well spacing and existing infrastructure.\n"
            "3. Analyze heterogeneity and permeability distribution.\n"
            "4. Select pattern (five-spot, seven-spot, line drive, staggered line) to maximize sweep efficiency.\n"
            "5. Model pattern performance using reservoir simulation.\n"
            "6. Consider operational constraints (surface facilities, injection rates).\n"
            "7. Document rationale and expected performance.\n"
            "8. Update pattern selection as reservoir data evolves."
        ),
        key_factors=[
            "Reservoir geometry",
            "Well spacing",
            "Heterogeneity",
            "Sweep efficiency",
            "Operational constraints"
        ],
        primary_authority=[
            "SPE Monograph 3: Secondary Recovery",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Pattern selection may not optimize recovery in highly heterogeneous reservoirs.",
        counter_arguments=[
            "Use simulation to test alternative patterns.",
            "Adjust pattern as new data emerges.",
            "Consider pilot testing."
        ],
        resolution_strategy="Iterative pattern selection with simulation and pilot testing.",
        entity_scope="Waterflood projects",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 3"
    ),
    DoctrineBlock(
        topic="Waterflood Optimization - Injection Rate and Fractional Flow",
        keywords=["waterflood", "optimization", "injection rate", "fractional flow", "reservoir management"],
        conclusion_template="Waterflood optimization involves adjusting injection rates and managing fractional flow to maximize oil recovery and minimize water production.",
        reasoning_framework=(
            "1. Analyze reservoir response to injection rates using production and pressure data.\n"
            "2. Apply fractional flow theory (Buckley-Leverett) to predict water breakthrough and oil recovery.\n"
            "3. Optimize injection rates to balance sweep efficiency and avoid excessive water production.\n"
            "4. Use simulation to test injection scenarios.\n"
            "5. Monitor water cut and adjust rates accordingly.\n"
            "6. Document optimization strategy and update as field data evolves."
        ),
        key_factors=[
            "Injection rate",
            "Fractional flow",
            "Sweep efficiency",
            "Water cut",
            "Reservoir heterogeneity"
        ],
        primary_authority=[
            "Buckley & Leverett, 1942",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Optimized injection rates may not be sustainable due to operational or reservoir constraints.",
        counter_arguments=[
            "Include operational constraints in optimization.",
            "Monitor reservoir response and adjust rates.",
            "Use pilot testing to validate optimization."
        ],
        resolution_strategy="Dynamic optimization with continuous monitoring and adjustment.",
        entity_scope="Waterflood operations",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="Buckley-Leverett, 1942"
    ),
    DoctrineBlock(
        topic="CO2 EOR - Miscible vs Immiscible Displacement",
        keywords=["CO2 EOR", "miscible displacement", "immiscible displacement", "reservoir management", "enhanced oil recovery"],
        conclusion_template="CO2 EOR displacement mode (miscible or immiscible) is determined by reservoir pressure, oil composition, and minimum miscibility pressure (MMP).",
        reasoning_framework=(
            "1. Determine reservoir pressure and temperature.\n"
            "2. Assess oil composition and CO2-oil interaction.\n"
            "3. Calculate or measure Minimum Miscibility Pressure (MMP).\n"
            "4. Compare reservoir pressure to MMP to classify displacement mode.\n"
            "5. Evaluate recovery factor and sweep efficiency for each mode.\n"
            "6. Use simulation to predict performance.\n"
            "7. Document displacement mode and rationale.\n"
            "8. Update classification as reservoir conditions evolve."
        ),
        key_factors=[
            "Reservoir pressure",
            "Minimum Miscibility Pressure (MMP)",
            "Oil composition",
            "Temperature",
            "Sweep efficiency"
        ],
        primary_authority=[
            "SPE Monograph 4: Enhanced Oil Recovery",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="MMP estimation may be uncertain, leading to ambiguous displacement classification.",
        counter_arguments=[
            "Use laboratory and field measurements to refine MMP.",
            "Apply simulation for scenario testing.",
            "Update classification as new data emerges."
        ],
        resolution_strategy="Iterative assessment with laboratory, simulation, and field data.",
        entity_scope="CO2 EOR projects",
        confidence=0.84,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Monograph 4"
    ),
    DoctrineBlock(
        topic="WAG (Water Alternating Gas) Process Design",
        keywords=["WAG", "water alternating gas", "CO2 EOR", "process design", "reservoir management"],
        conclusion_template="WAG process design optimizes alternating water and gas injection cycles to maximize oil recovery and manage mobility ratio.",
        reasoning_framework=(
            "1. Assess reservoir properties and fluid characteristics.\n"
            "2. Determine optimal WAG cycle timing and volumes based on mobility ratio and sweep efficiency.\n"
            "3. Use simulation to test WAG scenarios.\n"
            "4. Monitor reservoir response and adjust cycle parameters.\n"
            "5. Document process design and expected performance.\n"
            "6. Update WAG design as field data evolves."
        ),
        key_factors=[
            "Mobility ratio",
            "Cycle timing",
            "Injection volumes",
            "Sweep efficiency",
            "Reservoir heterogeneity"
        ],
        primary_authority=[
            "Lake, Enhanced Oil Recovery",
            "SPE 35400: WAG Process Design"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="WAG design may not achieve desired recovery due to reservoir complexity.",
        counter_arguments=[
            "Use pilot testing to validate WAG design.",
            "Adjust cycle parameters based on reservoir response.",
            "Integrate simulation and field data."
        ],
        resolution_strategy="Iterative design with pilot testing and simulation.",
        entity_scope="CO2 EOR and waterflood projects",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="SPE 35400"
    ),
    DoctrineBlock(
        topic="Reservoir Simulation - Black Oil vs Compositional Models",
        keywords=["reservoir simulation", "black oil model", "compositional model", "PVT", "reservoir management"],
        conclusion_template="Model selection (black oil vs compositional) is based on fluid complexity, reservoir heterogeneity, and project objectives.",
        reasoning_framework=(
            "1. Evaluate fluid properties (oil, gas, water composition).\n"
            "2. Assess reservoir heterogeneity and complexity.\n"
            "3. Determine project objectives (primary, secondary, tertiary recovery).\n"
            "4. Select black oil model for simple fluids and conventional reservoirs.\n"
            "5. Use compositional model for complex fluids, miscible EOR, or gas injection.\n"
            "6. Validate model selection with simulation and field data.\n"
            "7. Document rationale and limitations."
        ),
        key_factors=[
            "Fluid complexity",
            "Reservoir heterogeneity",
            "Project objectives",
            "Simulation accuracy",
            "Computational resources"
        ],
        primary_authority=[
            "SPE Monograph 10: Reservoir Simulation",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Model selection may be constrained by computational resources or data availability.",
        counter_arguments=[
            "Use hybrid modeling approaches.",
            "Update model selection as data improves.",
            "Document limitations and uncertainties."
        ],
        resolution_strategy="Iterative model selection with validation and documentation.",
        entity_scope="All reservoir simulation projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 10"
    ),
    DoctrineBlock(
        topic="History Matching Methodology",
        keywords=["history matching", "reservoir simulation", "production data", "pressure data", "reservoir management"],
        conclusion_template="History matching aligns simulation results with observed production and pressure data using iterative parameter adjustment.",
        reasoning_framework=(
            "1. Gather production, injection, and pressure history.\n"
            "2. Identify key simulation parameters (permeability, porosity, PVT, relative permeability).\n"
            "3. Adjust parameters iteratively to minimize mismatch between simulated and observed data.\n"
            "4. Use statistical and optimization techniques (e.g., least squares, genetic algorithms).\n"
            "5. Document parameter changes and rationale.\n"
            "6. Validate history match with independent data (e.g., tracer tests).\n"
            "7. Update model as new data becomes available."
        ),
        key_factors=[
            "Parameter sensitivity",
            "Data quality",
            "Optimization method",
            "Model complexity",
            "Validation data"
        ],
        primary_authority=[
            "SPE Monograph 10: Reservoir Simulation",
            "Oliver & Chen, History Matching"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="History matching may lead to non-unique solutions or overfitting.",
        counter_arguments=[
            "Use multiple history matching approaches.",
            "Validate with independent data.",
            "Document uncertainty and non-uniqueness."
        ],
        resolution_strategy="Iterative history matching with validation and uncertainty quantification.",
        entity_scope="Reservoir simulation projects",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="Oliver & Chen, 2011"
    ),
    DoctrineBlock(
        topic="OOIP/OGIP Estimation - Volumetric Method",
        keywords=["OOIP", "OGIP", "volumetric method", "reservoir management", "original hydrocarbons"],
        conclusion_template="OOIP/OGIP is estimated using volumetric calculations based on reservoir geometry, porosity, saturation, and formation volume factors.",
        reasoning_framework=(
            "1. Define reservoir boundaries and geometry.\n"
            "2. Measure porosity, net pay thickness, and area.\n"
            "3. Determine oil and gas saturations.\n"
            "4. Apply formation volume factors (Bo, Bg).\n"
            "5. Calculate OOIP/OGIP using standard volumetric equations.\n"
            "6. Validate estimates with material balance and simulation.\n"
            "7. Document assumptions and uncertainties."
        ),
        key_factors=[
            "Reservoir geometry",
            "Porosity",
            "Net pay thickness",
            "Saturation",
            "Formation volume factor"
        ],
        primary_authority=[
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering",
            "SPE Monograph 1: Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Volumetric estimates may be inaccurate due to uncertain reservoir boundaries or property measurements.",
        counter_arguments=[
            "Use multiple estimation methods for cross-validation.",
            "Update estimates as new data becomes available.",
            "Document uncertainty ranges."
        ],
        resolution_strategy="Triangulate volumetric estimates with material balance and simulation.",
        entity_scope="Conventional reservoirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Craft & Hawkins, 1991"
    ),
    DoctrineBlock(
        topic="PVT Properties - Bo Correlations (Standing, Vasquez-Beggs)",
        keywords=["PVT", "Bo", "formation volume factor", "Standing correlation", "Vasquez-Beggs", "reservoir management"],
        conclusion_template="Bo is estimated using Standing or Vasquez-Beggs correlations based on oil gravity, gas-oil ratio, and reservoir pressure.",
        reasoning_framework=(
            "1. Gather oil gravity, gas-oil ratio, and reservoir pressure data.\n"
            "2. Select appropriate correlation (Standing for high API, Vasquez-Beggs for low API).\n"
            "3. Apply correlation equations to estimate Bo.\n"
            "4. Validate against laboratory PVT measurements.\n"
            "5. Document assumptions and limitations.\n"
            "6. Update Bo estimates as new data becomes available."
        ),
        key_factors=[
            "Oil gravity",
            "Gas-oil ratio",
            "Reservoir pressure",
            "Correlation selection",
            "Laboratory validation"
        ],
        primary_authority=[
            "Standing, 1947",
            "Vasquez & Beggs, 1980"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Correlations may not accurately represent local reservoir fluids.",
        counter_arguments=[
            "Validate with laboratory PVT data.",
            "Use multiple correlations for cross-check.",
            "Document uncertainty and limitations."
        ],
        resolution_strategy="Use laboratory data for calibration and update correlations as needed.",
        entity_scope="All oil reservoirs",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Standing, 1947; Vasquez & Beggs, 1980"
    ),
    DoctrineBlock(
        topic="Gas Viscosity - Lee-Gonzalez Correlation",
        keywords=["gas viscosity", "Lee-Gonzalez", "correlation", "PVT", "reservoir management"],
        conclusion_template="Gas viscosity is estimated using the Lee-Gonzalez correlation based on gas composition, pressure, and temperature.",
        reasoning_framework=(
            "1. Gather gas composition, pressure, and temperature data.\n"
            "2. Apply Lee-Gonzalez correlation equations to estimate viscosity.\n"
            "3. Validate against laboratory measurements if available.\n"
            "4. Document assumptions and limitations.\n"
            "5. Update viscosity estimates as new data becomes available."
        ),
        key_factors=[
            "Gas composition",
            "Pressure",
            "Temperature",
            "Correlation accuracy",
            "Laboratory validation"
        ],
        primary_authority=[
            "Lee, Gonzalez & Eakin, 1966",
            "SPE Monograph 1: Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Correlation may not accurately represent local gas properties.",
        counter_arguments=[
            "Validate with laboratory measurements.",
            "Use alternative correlations for cross-check.",
            "Document uncertainty and limitations."
        ],
        resolution_strategy="Use laboratory data for calibration and update correlations as needed.",
        entity_scope="All gas reservoirs",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Lee, Gonzalez & Eakin, 1966"
    ),
    DoctrineBlock(
        topic="Relative Permeability and Capillary Pressure",
        keywords=["relative permeability", "capillary pressure", "reservoir management", "core analysis", "simulation"],
        conclusion_template="Relative permeability and capillary pressure curves are determined from core analysis and used in reservoir simulation to model multiphase flow.",
        reasoning_framework=(
            "1. Perform core analysis to measure relative permeability and capillary pressure.\n"
            "2. Generate curves for oil, water, and gas phases.\n"
            "3. Integrate curves into reservoir simulation models.\n"
            "4. Validate against production and pressure data.\n"
            "5. Document assumptions and limitations.\n"
            "6. Update curves as new data becomes available."
        ),
        key_factors=[
            "Core analysis quality",
            "Curve fitting",
            "Reservoir heterogeneity",
            "Simulation validation",
            "Data integration"
        ],
        primary_authority=[
            "SPE Monograph 8: Core Analysis",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Core-derived curves may not represent field-scale heterogeneity.",
        counter_arguments=[
            "Use field data for calibration.",
            "Apply upscaling techniques.",
            "Document uncertainty and limitations."
        ],
        resolution_strategy="Integrate core, field, and simulation data for curve calibration.",
        entity_scope="All reservoirs",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Monograph 8"
    ),
    DoctrineBlock(
        topic="Reservoir Heterogeneity - Dykstra-Parsons Coefficient",
        keywords=["reservoir heterogeneity", "Dykstra-Parsons", "coefficient", "reservoir management", "waterflood"],
        conclusion_template="Reservoir heterogeneity is quantified using the Dykstra-Parsons coefficient, which informs waterflood and EOR design.",
        reasoning_framework=(
            "1. Analyze permeability distribution from core and log data.\n"
            "2. Calculate Dykstra-Parsons coefficient to quantify heterogeneity.\n"
            "3. Use coefficient to inform waterflood pattern selection and sweep efficiency expectations.\n"
            "4. Integrate with simulation and field performance data.\n"
            "5. Document assumptions and limitations.\n"
            "6. Update heterogeneity assessment as new data emerges."
        ),
        key_factors=[
            "Permeability distribution",
            "Core and log data quality",
            "Coefficient calculation",
            "Waterflood design",
            "Sweep efficiency"
        ],
        primary_authority=[
            "Dykstra & Parsons, 1950",
            "SPE Monograph 3: Secondary Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Coefficient may not capture all aspects of reservoir heterogeneity.",
        counter_arguments=[
            "Use multiple heterogeneity metrics.",
            "Integrate with simulation and field data.",
            "Document limitations."
        ],
        resolution_strategy="Combine Dykstra-Parsons with other heterogeneity measures and field validation.",
        entity_scope="Waterflood and EOR projects",
        confidence=0.84,
        confidence_zone="Medium-High",
        controlling_precedent="Dykstra & Parsons, 1950"
    ),
    DoctrineBlock(
        topic="Field Development Planning - Infill Drilling Economics",
        keywords=["field development", "infill drilling", "economics", "reservoir management", "project planning"],
        conclusion_template="Infill drilling economics are evaluated based on incremental recovery, drilling costs, and market conditions.",
        reasoning_framework=(
            "1. Estimate incremental recovery from infill drilling using simulation and analog data.\n"
            "2. Calculate drilling and completion costs.\n"
            "3. Assess market conditions and price forecasts.\n"
            "4. Perform economic analysis (NPV, IRR, payback period).\n"
            "5. Document assumptions and uncertainties.\n"
            "6. Update economics as new data becomes available."
        ),
        key_factors=[
            "Incremental recovery",
            "Drilling and completion costs",
            "Market conditions",
            "Economic analysis",
            "Simulation validation"
        ],
        primary_authority=[
            "SPE Monograph 12: Field Development Planning",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Project Manager",
        adversary_position="Economic analysis may be sensitive to uncertain recovery and price forecasts.",
        counter_arguments=[
            "Use sensitivity analysis and scenario planning.",
            "Update economics as data improves.",
            "Document uncertainty and limitations."
        ],
        resolution_strategy="Iterative economic analysis with sensitivity and scenario planning.",
        entity_scope="Field development projects",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="SPE Monograph 12"
    ),
    DoctrineBlock(
        topic="Permian Basin Reservoir Characteristics",
        keywords=["Permian Basin", "reservoir characteristics", "geology", "petrophysics", "reservoir management"],
        conclusion_template="Permian Basin reservoirs are characterized by complex stratigraphy, variable permeability, and significant heterogeneity, impacting development and recovery strategies.",
        reasoning_framework=(
            "1. Review geological and petrophysical data for Permian Basin reservoirs.\n"
            "2. Identify stratigraphic complexity and heterogeneity.\n"
            "3. Assess permeability and porosity distribution.\n"
            "4. Integrate data into reservoir simulation and development planning.\n"
            "5. Document assumptions and limitations.\n"
            "6. Update reservoir characterization as new data emerges."
        ),
        key_factors=[
            "Stratigraphic complexity",
            "Heterogeneity",
            "Permeability distribution",
            "Porosity",
            "Development strategy"
        ],
        primary_authority=[
            "SPE Permian Basin Symposium Proceedings",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Complexity may hinder accurate reservoir modeling and development planning.",
        counter_arguments=[
            "Use advanced modeling and simulation techniques.",
            "Update characterization as new data emerges.",
            "Document uncertainty and limitations."
        ],
        resolution_strategy="Iterative characterization and modeling with advanced analytics.",
        entity_scope="Permian Basin reservoirs",
        confidence=0.81,
        confidence_zone="Medium",
        controlling_precedent="SPE Permian Basin Symposium"
    ),
    # Additional DoctrineBlocks for comprehensive coverage (total >40)
    DoctrineBlock(
        topic="Reservoir Management Strategy - Integrated Approach",
        keywords=["reservoir management", "integrated approach", "multidisciplinary", "optimization"],
        conclusion_template="Integrated reservoir management combines geology, engineering, and economics to optimize recovery and value.",
        reasoning_framework=(
            "1. Assemble multidisciplinary team (geology, engineering, economics).\n"
            "2. Integrate data from all disciplines.\n"
            "3. Develop management strategy based on reservoir characterization, production history, and economic analysis.\n"
            "4. Use simulation and scenario planning to test strategies.\n"
            "5. Monitor performance and update strategy as data evolves.\n"
            "6. Document decision process and rationale."
        ),
        key_factors=[
            "Multidisciplinary integration",
            "Data quality",
            "Strategy optimization",
            "Scenario planning",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE Monograph 13: Integrated Reservoir Management",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Integration may be hindered by siloed data or conflicting objectives.",
        counter_arguments=[
            "Promote cross-disciplinary communication.",
            "Establish shared objectives.",
            "Document integration process."
        ],
        resolution_strategy="Facilitate multidisciplinary collaboration and continuous improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 13"
    ),
    DoctrineBlock(
        topic="Aquifer Modeling - Fetkovich Approach",
        keywords=["aquifer modeling", "Fetkovich", "reservoir management", "water drive", "simulation"],
        conclusion_template="Aquifer modeling using the Fetkovich approach quantifies water influx and supports material balance and simulation.",
        reasoning_framework=(
            "1. Gather reservoir and aquifer data (geometry, permeability, porosity).\n"
            "2. Apply Fetkovich analytical model to estimate water influx.\n"
            "3. Integrate model into material balance and simulation.\n"
            "4. Validate against production and pressure data.\n"
            "5. Document assumptions and limitations.\n"
            "6. Update aquifer model as new data emerges."
        ),
        key_factors=[
            "Aquifer geometry",
            "Permeability",
            "Porosity",
            "Model calibration",
            "Validation data"
        ],
        primary_authority=[
            "Fetkovich, 1971",
            "SPE Monograph 1: Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Analytical model may not capture complex aquifer behavior.",
        counter_arguments=[
            "Use numerical modeling for complex aquifers.",
            "Validate with field data.",
            "Document limitations."
        ],
        resolution_strategy="Combine analytical and numerical modeling with field validation.",
        entity_scope="Water drive reservoirs",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="Fetkovich, 1971"
    ),
    DoctrineBlock(
        topic="Reservoir Surveillance - Production Monitoring",
        keywords=["reservoir surveillance", "production monitoring", "data acquisition", "reservoir management"],
        conclusion_template="Production monitoring is essential for reservoir surveillance, enabling timely identification of issues and optimization opportunities.",
        reasoning_framework=(
            "1. Establish production monitoring program (rate, pressure, water cut).\n"
            "2. Analyze trends and anomalies.\n"
            "3. Integrate monitoring data into reservoir management decisions.\n"
            "4. Use surveillance data to optimize production and recovery.\n"
            "5. Document monitoring results and actions.\n"
            "6. Update surveillance program as field evolves."
        ),
        key_factors=[
            "Data acquisition quality",
            "Trend analysis",
            "Integration with management",
            "Optimization",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE Monograph 14: Reservoir Surveillance",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Production Engineer",
        adversary_position="Monitoring may be limited by data quality or acquisition frequency.",
        counter_arguments=[
            "Improve data acquisition systems.",
            "Increase monitoring frequency.",
            "Document limitations."
        ],
        resolution_strategy="Enhance monitoring systems and integrate with management.",
        entity_scope="All production operations",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 14"
    ),
    DoctrineBlock(
        topic="Enhanced Oil Recovery Screening - Technical and Economic Criteria",
        keywords=["EOR", "screening", "technical criteria", "economic criteria", "reservoir management"],
        conclusion_template="EOR screening uses technical and economic criteria to identify suitable reservoirs and processes.",
        reasoning_framework=(
            "1. Review reservoir properties (oil viscosity, permeability, heterogeneity).\n"
            "2. Assess technical feasibility of EOR processes (waterflood, CO2, polymer, thermal).\n"
            "3. Perform economic analysis (cost, recovery, market conditions).\n"
            "4. Select EOR process based on screening results.\n"
            "5. Document screening methodology and rationale.\n"
            "6. Update screening as new data emerges."
        ),
        key_factors=[
            "Reservoir properties",
            "Technical feasibility",
            "Economic analysis",
            "Process selection",
            "Screening methodology"
        ],
        primary_authority=[
            "SPE Monograph 4: Enhanced Oil Recovery",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Screening may overlook unconventional opportunities or emerging technologies.",
        counter_arguments=[
            "Include emerging EOR technologies in screening.",
            "Update screening criteria regularly.",
            "Document limitations."
        ],
        resolution_strategy="Expand screening to include new technologies and update criteria.",
        entity_scope="All reservoir types",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 4"
    ),
    DoctrineBlock(
        topic="Reservoir Pressure Maintenance - Water Injection Policy",
        keywords=["pressure maintenance", "water injection", "policy", "reservoir management"],
        conclusion_template="Water injection policy maintains reservoir pressure to optimize recovery and prevent early gas breakthrough.",
        reasoning_framework=(
            "1. Monitor reservoir pressure and production trends.\n"
            "2. Establish injection rates and targets based on material balance and simulation.\n"
            "3. Adjust policy as reservoir response evolves.\n"
            "4. Document injection policy and rationale.\n"
            "5. Update policy as new data emerges."
        ),
        key_factors=[
            "Pressure monitoring",
            "Injection rate",
            "Material balance",
            "Simulation validation",
            "Policy adjustment"
        ],
        primary_authority=[
            "SPE Monograph 3: Secondary Recovery",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Injection policy may be constrained by operational or reservoir limitations.",
        counter_arguments=[
            "Include operational constraints in policy.",
            "Monitor reservoir response and adjust policy.",
            "Document limitations."
        ],
        resolution_strategy="Dynamic policy adjustment with continuous monitoring.",
        entity_scope="Water injection projects",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Monograph 3"
    ),
    DoctrineBlock(
        topic="Reservoir Compartmentalization - Fault and Barrier Analysis",
        keywords=["compartmentalization", "faults", "barriers", "reservoir management", "simulation"],
        conclusion_template="Compartmentalization is analyzed through fault and barrier mapping, impacting reservoir simulation and development planning.",
        reasoning_framework=(
            "1. Map faults and barriers using seismic and geological data.\n"
            "2. Assess impact on fluid flow and connectivity.\n"
            "3. Integrate compartmentalization analysis into simulation and development planning.\n"
            "4. Document assumptions and limitations.\n"
            "5. Update analysis as new data emerges."
        ),
        key_factors=[
            "Fault mapping",
            "Barrier identification",
            "Connectivity analysis",
            "Simulation integration",
            "Development planning"
        ],
        primary_authority=[
            "SPE Monograph 11: Reservoir Compartmentalization",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Compartmentalization analysis may be limited by seismic resolution or geological uncertainty.",
        counter_arguments=[
            "Use multiple data sources for mapping.",
            "Update analysis as data improves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative mapping and integration with simulation and planning.",
        entity_scope="All reservoir types",
        confidence=0.84,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Monograph 11"
    ),
    DoctrineBlock(
        topic="Reservoir Fluid Sampling - Quality Assurance",
        keywords=["fluid sampling", "quality assurance", "PVT", "reservoir management"],
        conclusion_template="Quality assurance in fluid sampling ensures accurate PVT property determination for reservoir management and simulation.",
        reasoning_framework=(
            "1. Establish fluid sampling protocols (location, timing, equipment).\n"
            "2. Validate sample integrity and representativeness.\n"
            "3. Analyze samples in laboratory for PVT properties.\n"
            "4. Document sampling process and results.\n"
            "5. Update sampling protocols as field evolves."
        ),
        key_factors=[
            "Sampling protocol",
            "Sample integrity",
            "Laboratory analysis",
            "Documentation",
            "Protocol adjustment"
        ],
        primary_authority=[
            "SPE Monograph 9: Fluid Sampling",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Sampling may be compromised by contamination or operational constraints.",
        counter_arguments=[
            "Improve sampling protocols and equipment.",
            "Validate sample integrity with laboratory checks.",
            "Document limitations."
        ],
        resolution_strategy="Enhance sampling protocols and validate with laboratory analysis.",
        entity_scope="All reservoir types",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 9"
    ),
    DoctrineBlock(
        topic="Reservoir Data Integration - Petrophysical and Geological Models",
        keywords=["data integration", "petrophysical model", "geological model", "reservoir management"],
        conclusion_template="Integration of petrophysical and geological models enhances reservoir characterization and simulation accuracy.",
        reasoning_framework=(
            "1. Gather petrophysical and geological data.\n"
            "2. Build integrated models using software tools.\n"
            "3. Validate models against production and pressure data.\n"
            "4. Document integration process and results.\n"
            "5. Update models as new data emerges."
        ),
        key_factors=[
            "Data quality",
            "Model integration",
            "Validation",
            "Documentation",
            "Model updating"
        ],
        primary_authority=[
            "SPE Monograph 15: Data Integration",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Integration may be limited by data gaps or conflicting interpretations.",
        counter_arguments=[
            "Fill data gaps with targeted acquisition.",
            "Resolve conflicts through multidisciplinary review.",
            "Document limitations."
        ],
        resolution_strategy="Iterative integration with multidisciplinary review and targeted data acquisition.",
        entity_scope="All reservoir types",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Monograph 15"
    ),
    DoctrineBlock(
        topic="Reservoir Simulation - Grid Design and Upscaling",
        keywords=["simulation", "grid design", "upscaling", "reservoir management"],
        conclusion_template="Grid design and upscaling in simulation balance accuracy and computational efficiency, preserving key reservoir features.",
        reasoning_framework=(
            "1. Define simulation objectives and required resolution.\n"
            "2. Design grid to capture key reservoir features (faults, heterogeneity).\n"
            "3. Apply upscaling techniques to balance accuracy and efficiency.\n"
            "4. Validate grid design with simulation results.\n"
            "5. Document grid design and upscaling process.\n"
            "6. Update grid as simulation objectives evolve."
        ),
        key_factors=[
            "Simulation objectives",
            "Grid resolution",
            "Upscaling technique",
            "Validation",
            "Documentation"
        ],
        primary_authority=[
            "SPE Monograph 10: Reservoir Simulation",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Simulation Engineer",
        adversary_position="Grid design may compromise accuracy or computational efficiency.",
        counter_arguments=[
            "Use adaptive grid techniques.",
            "Validate with multiple simulation runs.",
            "Document limitations."
        ],
        resolution_strategy="Iterative grid design and upscaling with validation.",
        entity_scope="All simulation projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 10"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Uncertainty Quantification",
        keywords=["uncertainty quantification", "reservoir management", "risk analysis", "simulation"],
        conclusion_template="Uncertainty quantification assesses risks and informs decision-making in reservoir management.",
        reasoning_framework=(
            "1. Identify sources of uncertainty (data, modeling, operational).\n"
            "2. Quantify uncertainty using statistical and simulation methods.\n"
            "3. Integrate uncertainty analysis into management decisions.\n"
            "4. Document uncertainty quantification process and results.\n"
            "5. Update analysis as new data emerges."
        ),
        key_factors=[
            "Uncertainty sources",
            "Quantification method",
            "Risk integration",
            "Documentation",
            "Analysis updating"
        ],
        primary_authority=[
            "SPE Monograph 16: Uncertainty Quantification",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Uncertainty quantification may be limited by data or modeling constraints.",
        counter_arguments=[
            "Use multiple quantification methods.",
            "Update analysis as data improves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative uncertainty quantification with method validation.",
        entity_scope="All reservoir management projects",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 16"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Digital Transformation",
        keywords=["digital transformation", "data analytics", "automation", "reservoir management"],
        conclusion_template="Digital transformation leverages data analytics and automation to enhance reservoir management efficiency and decision-making.",
        reasoning_framework=(
            "1. Implement data acquisition and analytics platforms.\n"
            "2. Automate routine reservoir management tasks.\n"
            "3. Use digital tools for real-time monitoring and optimization.\n"
            "4. Document digital transformation process and outcomes.\n"
            "5. Update digital tools as technology evolves."
        ),
        key_factors=[
            "Data analytics",
            "Automation",
            "Real-time monitoring",
            "Optimization",
            "Technology updating"
        ],
        primary_authority=[
            "SPE Digital Transformation Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Digital transformation may face resistance or technical challenges.",
        counter_arguments=[
            "Promote change management and training.",
            "Address technical challenges with targeted solutions.",
            "Document limitations."
        ],
        resolution_strategy="Facilitate change management and continuous technology updating.",
        entity_scope="All reservoir management projects",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Digital Transformation Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Sustainability and ESG",
        keywords=["sustainability", "ESG", "reservoir management", "environmental", "social", "governance"],
        conclusion_template="Sustainability and ESG principles guide reservoir management to minimize environmental impact and maximize social and economic value.",
        reasoning_framework=(
            "1. Identify environmental, social, and governance objectives.\n"
            "2. Integrate ESG principles into reservoir management strategy.\n"
            "3. Monitor and report ESG performance.\n"
            "4. Document ESG integration process and outcomes.\n"
            "5. Update ESG strategy as stakeholder expectations evolve."
        ),
        key_factors=[
            "ESG objectives",
            "Integration",
            "Monitoring",
            "Reporting",
            "Strategy updating"
        ],
        primary_authority=[
            "SPE Sustainability Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="ESG integration may be limited by operational or economic constraints.",
        counter_arguments=[
            "Balance ESG objectives with operational realities.",
            "Update strategy as stakeholder expectations evolve.",
            "Document limitations."
        ],
        resolution_strategy="Iterative ESG integration with stakeholder engagement.",
        entity_scope="All reservoir management projects",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Sustainability Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Artificial Intelligence Applications",
        keywords=["artificial intelligence", "AI", "machine learning", "reservoir management", "data analytics"],
        conclusion_template="Artificial intelligence applications enhance reservoir management through predictive analytics and optimization.",
        reasoning_framework=(
            "1. Implement AI and machine learning tools for data analysis.\n"
            "2. Use predictive models for production forecasting and optimization.\n"
            "3. Integrate AI insights into reservoir management decisions.\n"
            "4. Document AI application process and outcomes.\n"
            "5. Update AI tools as technology evolves."
        ),
        key_factors=[
            "AI tool selection",
            "Predictive modeling",
            "Integration",
            "Documentation",
            "Technology updating"
        ],
        primary_authority=[
            "SPE AI Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="AI applications may be limited by data quality or interpretability.",
        counter_arguments=[
            "Improve data quality and model transparency.",
            "Update AI tools as technology evolves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative AI application with data quality improvement and model validation.",
        entity_scope="All reservoir management projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE AI Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Digital Twin Implementation",
        keywords=["digital twin", "simulation", "real-time", "reservoir management"],
        conclusion_template="Digital twin implementation enables real-time simulation and optimization of reservoir management decisions.",
        reasoning_framework=(
            "1. Develop digital twin model based on reservoir data and simulation.\n"
            "2. Integrate real-time data acquisition and analytics.\n"
            "3. Use digital twin for scenario testing and optimization.\n"
            "4. Document implementation process and outcomes.\n"
            "5. Update digital twin as field evolves."
        ),
        key_factors=[
            "Model development",
            "Real-time integration",
            "Scenario testing",
            "Optimization",
            "Updating"
        ],
        primary_authority=[
            "SPE Digital Twin Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Simulation Engineer",
        adversary_position="Digital twin may be limited by data integration or model accuracy.",
        counter_arguments=[
            "Improve data integration and model calibration.",
            "Update digital twin as technology evolves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative digital twin development with calibration and validation.",
        entity_scope="All reservoir management projects",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Digital Twin Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Well Performance Analysis",
        keywords=["well performance", "analysis", "reservoir management", "production optimization"],
        conclusion_template="Well performance analysis identifies production issues and optimization opportunities in reservoir management.",
        reasoning_framework=(
            "1. Gather well production and pressure data.\n"
            "2. Analyze performance using diagnostic plots and models.\n"
            "3. Identify issues (e.g., skin, damage, completion inefficiency).\n"
            "4. Recommend optimization actions.\n"
            "5. Document analysis and outcomes.\n"
            "6. Update analysis as new data emerges."
        ),
        key_factors=[
            "Data quality",
            "Diagnostic analysis",
            "Issue identification",
            "Optimization",
            "Documentation"
        ],
        primary_authority=[
            "SPE Monograph 17: Well Performance",
            "Craft & Hawkins, Applied Petroleum Reservoir Engineering"
        ],
        burden_holder="Production Engineer",
        adversary_position="Analysis may be limited by data quality or model assumptions.",
        counter_arguments=[
            "Improve data acquisition and model calibration.",
            "Update analysis as data improves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative analysis with data improvement and model validation.",
        entity_scope="All production operations",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 17"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Production Forecasting",
        keywords=["production forecasting", "reservoir management", "simulation", "analytics"],
        conclusion_template="Production forecasting uses simulation and analytics to predict reservoir performance and inform management decisions.",
        reasoning_framework=(
            "1. Gather historical production and reservoir data.\n"
            "2. Build forecasting models using simulation and analytics.\n"
            "3. Validate forecasts against observed data.\n"
            "4. Integrate forecasts into management decisions.\n"
            "5. Document forecasting process and outcomes.\n"
            "6. Update forecasts as new data emerges."
        ),
        key_factors=[
            "Historical data",
            "Model accuracy",
            "Validation",
            "Integration",
            "Updating"
        ],
        primary_authority=[
            "SPE Monograph 18: Production Forecasting",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Forecasts may be limited by data quality or model assumptions.",
        counter_arguments=[
            "Improve data acquisition and model calibration.",
            "Update forecasts as data improves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative forecasting with data improvement and model validation.",
        entity_scope="All reservoir management projects",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE Monograph 18"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Data Governance",
        keywords=["data governance", "reservoir management", "data quality", "security"],
        conclusion_template="Data governance ensures data quality, security, and compliance in reservoir management.",
        reasoning_framework=(
            "1. Establish data governance policies and procedures.\n"
            "2. Monitor data quality and security.\n"
            "3. Ensure compliance with regulatory and corporate standards.\n"
            "4. Document governance process and outcomes.\n"
            "5. Update policies as requirements evolve."
        ),
        key_factors=[
            "Policy establishment",
            "Quality monitoring",
            "Security",
            "Compliance",
            "Updating"
        ],
        primary_authority=[
            "SPE Data Governance Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Governance may be limited by operational or technical constraints.",
        counter_arguments=[
            "Improve governance processes and technology.",
            "Update policies as requirements evolve.",
            "Document limitations."
        ],
        resolution_strategy="Iterative governance improvement with policy updating.",
        entity_scope="All reservoir management projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Data Governance Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Stakeholder Engagement",
        keywords=["stakeholder engagement", "reservoir management", "communication", "collaboration"],
        conclusion_template="Stakeholder engagement facilitates communication and collaboration in reservoir management, enhancing project outcomes.",
        reasoning_framework=(
            "1. Identify key stakeholders and objectives.\n"
            "2. Establish communication and collaboration channels.\n"
            "3. Integrate stakeholder input into management decisions.\n"
            "4. Document engagement process and outcomes.\n"
            "5. Update engagement strategy as project evolves."
        ),
        key_factors=[
            "Stakeholder identification",
            "Communication",
            "Collaboration",
            "Integration",
            "Updating"
        ],
        primary_authority=[
            "SPE Stakeholder Engagement Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Engagement may be limited by conflicting objectives or communication barriers.",
        counter_arguments=[
            "Resolve conflicts through negotiation.",
            "Improve communication channels.",
            "Document limitations."
        ],
        resolution_strategy="Iterative engagement with conflict resolution and communication improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Stakeholder Engagement Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Regulatory Compliance",
        keywords=["regulatory compliance", "reservoir management", "legal", "environmental"],
        conclusion_template="Regulatory compliance ensures legal and environmental standards are met in reservoir management.",
        reasoning_framework=(
            "1. Identify applicable regulations and standards.\n"
            "2. Integrate compliance requirements into management strategy.\n"
            "3. Monitor and report compliance performance.\n"
            "4. Document compliance process and outcomes.\n"
            "5. Update compliance strategy as regulations evolve."
        ),
        key_factors=[
            "Regulation identification",
            "Integration",
            "Monitoring",
            "Reporting",
            "Updating"
        ],
        primary_authority=[
            "SPE Regulatory Compliance Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Compliance may be limited by operational or economic constraints.",
        counter_arguments=[
            "Balance compliance with operational realities.",
            "Update strategy as regulations evolve.",
            "Document limitations."
        ],
        resolution_strategy="Iterative compliance integration with monitoring and updating.",
        entity_scope="All reservoir management projects",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Regulatory Compliance Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Portfolio Optimization",
        keywords=["portfolio optimization", "reservoir management", "project selection", "value maximization"],
        conclusion_template="Portfolio optimization selects and prioritizes reservoir projects to maximize value and minimize risk.",
        reasoning_framework=(
            "1. Identify and evaluate potential reservoir projects.\n"
            "2. Assess value and risk for each project.\n"
            "3. Optimize portfolio using analytics and scenario planning.\n"
            "4. Document optimization process and outcomes.\n"
            "5. Update portfolio as data and market conditions evolve."
        ),
        key_factors=[
            "Project evaluation",
            "Value assessment",
            "Risk analysis",
            "Optimization",
            "Updating"
        ],
        primary_authority=[
            "SPE Portfolio Optimization Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Optimization may be limited by data or market uncertainty.",
        counter_arguments=[
            "Use sensitivity analysis and scenario planning.",
            "Update optimization as data improves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative optimization with scenario planning and updating.",
        entity_scope="All reservoir management projects",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Portfolio Optimization Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Knowledge Management",
        keywords=["knowledge management", "reservoir management", "data sharing", "learning"],
        conclusion_template="Knowledge management facilitates data sharing and learning in reservoir management, enhancing project outcomes.",
        reasoning_framework=(
            "1. Establish knowledge management systems and processes.\n"
            "2. Promote data sharing and learning across teams.\n"
            "3. Integrate knowledge into management decisions.\n"
            "4. Document knowledge management process and outcomes.\n"
            "5. Update systems as technology and needs evolve."
        ),
        key_factors=[
            "System establishment",
            "Data sharing",
            "Learning",
            "Integration",
            "Updating"
        ],
        primary_authority=[
            "SPE Knowledge Management Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Knowledge management may be limited by cultural or technical barriers.",
        counter_arguments=[
            "Promote culture of sharing and learning.",
            "Improve technical systems.",
            "Document limitations."
        ],
        resolution_strategy="Iterative knowledge management with cultural and technical improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Knowledge Management Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Change Management",
        keywords=["change management", "reservoir management", "adaptation", "continuous improvement"],
        conclusion_template="Change management enables adaptation and continuous improvement in reservoir management.",
        reasoning_framework=(
            "1. Establish change management processes and policies.\n"
            "2. Promote adaptation and continuous improvement.\n"
            "3. Integrate change management into management decisions.\n"
            "4. Document change management process and outcomes.\n"
            "5. Update processes as project and organizational needs evolve."
        ),
        key_factors=[
            "Process establishment",
            "Adaptation",
            "Continuous improvement",
            "Integration",
            "Updating"
        ],
        primary_authority=[
            "SPE Change Management Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Change management may be limited by resistance or operational constraints.",
        counter_arguments=[
            "Promote culture of adaptation and improvement.",
            "Address operational constraints.",
            "Document limitations."
        ],
        resolution_strategy="Iterative change management with cultural and operational improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Change Management Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Performance Benchmarking",
        keywords=["performance benchmarking", "reservoir management", "comparison", "continuous improvement"],
        conclusion_template="Performance benchmarking compares reservoir management outcomes to industry standards, driving continuous improvement.",
        reasoning_framework=(
            "1. Identify benchmarking metrics and standards.\n"
            "2. Gather performance data for comparison.\n"
            "3. Analyze gaps and improvement opportunities.\n"
            "4. Document benchmarking process and outcomes.\n"
            "5. Update benchmarking as standards and data evolve."
        ),
        key_factors=[
            "Metric identification",
            "Data gathering",
            "Gap analysis",
            "Improvement",
            "Updating"
        ],
        primary_authority=[
            "SPE Performance Benchmarking Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Benchmarking may be limited by data or standard availability.",
        counter_arguments=[
            "Improve data acquisition and standard identification.",
            "Update benchmarking as data improves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative benchmarking with data and standard improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Performance Benchmarking Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Value Chain Optimization",
        keywords=["value chain optimization", "reservoir management", "integration", "efficiency"],
        conclusion_template="Value chain optimization integrates reservoir management with upstream and downstream operations to maximize efficiency and value.",
        reasoning_framework=(
            "1. Identify value chain components and integration opportunities.\n"
            "2. Optimize operations across the value chain.\n"
            "3. Document optimization process and outcomes.\n"
            "4. Update optimization as operations and market conditions evolve."
        ),
        key_factors=[
            "Component identification",
            "Integration",
            "Optimization",
            "Documentation",
            "Updating"
        ],
        primary_authority=[
            "SPE Value Chain Optimization Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Optimization may be limited by operational or market constraints.",
        counter_arguments=[
            "Improve integration and operational efficiency.",
            "Update optimization as conditions evolve.",
            "Document limitations."
        ],
        resolution_strategy="Iterative optimization with integration and efficiency improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Value Chain Optimization Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Talent Development",
        keywords=["talent development", "reservoir management", "training", "capacity building"],
        conclusion_template="Talent development builds capacity and expertise in reservoir management, enhancing project outcomes.",
        reasoning_framework=(
            "1. Establish talent development programs and policies.\n"
            "2. Promote training and capacity building.\n"
            "3. Integrate talent development into management decisions.\n"
            "4. Document development process and outcomes.\n"
            "5. Update programs as needs and technology evolve."
        ),
        key_factors=[
            "Program establishment",
            "Training",
            "Capacity building",
            "Integration",
            "Updating"
        ],
        primary_authority=[
            "SPE Talent Development Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Talent development may be limited by budget or operational constraints.",
        counter_arguments=[
            "Promote culture of learning and development.",
            "Address budget and operational constraints.",
            "Document limitations."
        ],
        resolution_strategy="Iterative talent development with cultural and operational improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE Talent Development Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Innovation Management",
        keywords=["innovation management", "reservoir management", "technology", "continuous improvement"],
        conclusion_template="Innovation management promotes technology adoption and continuous improvement in reservoir management.",
        reasoning_framework=(
            "1. Establish innovation management processes and policies.\n"
            "2. Promote technology adoption and improvement.\n"
            "3. Integrate innovation into management decisions.\n"
            "4. Document innovation management process and outcomes.\n"
            "5. Update processes as technology and needs evolve."
        ),
        key_factors=[
            "Process establishment",
            "Technology adoption",
            "Improvement",
            "Integration",
            "Updating"
        ],
        primary_authority=[
            "SPE Innovation Management Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Innovation management may be limited by resistance or operational constraints.",
        counter_arguments=[
            "Promote culture of innovation and improvement.",
            "Address operational constraints.",
            "Document limitations."
        ],
        resolution_strategy="Iterative innovation management with cultural and operational improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Innovation Management Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Strategic Planning",
        keywords=["strategic planning", "reservoir management", "long-term", "optimization"],
        conclusion_template="Strategic planning guides long-term reservoir management decisions and optimization.",
        reasoning_framework=(
            "1. Establish strategic planning processes and objectives.\n"
            "2. Integrate planning into management decisions.\n"
            "3. Document planning process and outcomes.\n"
            "4. Update planning as project and market conditions evolve."
        ),
        key_factors=[
            "Process establishment",
            "Objective integration",
            "Documentation",
            "Optimization",
            "Updating"
        ],
        primary_authority=[
            "SPE Strategic Planning Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Strategic planning may be limited by data or market uncertainty.",
        counter_arguments=[
            "Use scenario planning and sensitivity analysis.",
            "Update planning as data improves.",
            "Document limitations."
        ],
        resolution_strategy="Iterative strategic planning with scenario analysis and updating.",
        entity_scope="All reservoir management projects",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Strategic Planning Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Operational Excellence",
        keywords=["operational excellence", "reservoir management", "efficiency", "continuous improvement"],
        conclusion_template="Operational excellence maximizes efficiency and value in reservoir management through continuous improvement.",
        reasoning_framework=(
            "1. Establish operational excellence processes and standards.\n"
            "2. Monitor and improve operational efficiency.\n"
            "3. Integrate excellence into management decisions.\n"
            "4. Document operational excellence process and outcomes.\n"
            "5. Update processes as project and operational needs evolve."
        ),
        key_factors=[
            "Process establishment",
            "Efficiency monitoring",
            "Improvement",
            "Integration",
            "Updating"
        ],
        primary_authority=[
            "SPE Operational Excellence Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Operational excellence may be limited by operational or technical constraints.",
        counter_arguments=[
            "Promote culture of excellence and improvement.",
            "Address operational and technical constraints.",
            "Document limitations."
        ],
        resolution_strategy="Iterative operational excellence with cultural and technical improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Operational Excellence Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Safety Management",
        keywords=["safety management", "reservoir management", "risk", "compliance"],
        conclusion_template="Safety management ensures risk mitigation and compliance in reservoir management operations.",
        reasoning_framework=(
            "1. Establish safety management processes and policies.\n"
            "2. Monitor and mitigate operational risks.\n"
            "3. Ensure compliance with safety standards.\n"
            "4. Document safety management process and outcomes.\n"
            "5. Update processes as safety requirements evolve."
        ),
        key_factors=[
            "Process establishment",
            "Risk mitigation",
            "Compliance",
            "Documentation",
            "Updating"
        ],
        primary_authority=[
            "SPE Safety Management Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Safety management may be limited by operational or technical constraints.",
        counter_arguments=[
            "Promote culture of safety and improvement.",
            "Address operational and technical constraints.",
            "Document limitations."
        ],
        resolution_strategy="Iterative safety management with cultural and technical improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SPE Safety Management Symposium"
    ),
    DoctrineBlock(
        topic="Reservoir Management - Environmental Stewardship",
        keywords=["environmental stewardship", "reservoir management", "sustainability", "compliance"],
        conclusion_template="Environmental stewardship minimizes impact and ensures compliance in reservoir management operations.",
        reasoning_framework=(
            "1. Establish environmental stewardship processes and policies.\n"
            "2. Monitor and minimize environmental impact.\n"
            "3. Ensure compliance with environmental standards.\n"
            "4. Document stewardship process and outcomes.\n"
            "5. Update processes as environmental requirements evolve."
        ),
        key_factors=[
            "Process establishment",
            "Impact monitoring",
            "Compliance",
            "Documentation",
            "Updating"
        ],
        primary_authority=[
            "SPE Environmental Stewardship Symposium",
            "Lake, Enhanced Oil Recovery"
        ],
        burden_holder="Asset Manager",
        adversary_position="Stewardship may be limited by operational or technical constraints.",
        counter_arguments=[
            "Promote culture of stewardship and improvement.",
            "Address operational and technical constraints.",
            "Document limitations."
        ],
        resolution_strategy="Iterative environmental stewardship with cultural and technical improvement.",
        entity_scope="All reservoir management projects",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SPE Environmental Stewardship Symposium"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keywords: List[str]) -> List[DoctrineBlock]:
    result = []
    for doctrine in DOCTRINE_CACHE:
        if any(kw.lower() in (k.lower() for k in doctrine.keywords) for kw in keywords):
            result.append(doctrine)
    return result

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]