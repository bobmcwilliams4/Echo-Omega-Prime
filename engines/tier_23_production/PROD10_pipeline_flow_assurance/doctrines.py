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
        topic="Hydrate Formation Thermodynamic Prediction",
        keywords=["hydrate", "formation", "thermodynamics", "prediction", "gas hydrates", "phase envelope"],
        conclusion_template="Hydrate formation is predicted under the given pressure and temperature conditions if the system enters the hydrate stability zone, as determined by validated thermodynamic models.",
        reasoning_framework="""
        1. Identify system composition, pressure, and temperature.
        2. Use validated hydrate prediction models (e.g., CSMGem, PVTSim, or Katz charts) to determine hydrate stability boundaries.
        3. Compare operating conditions to hydrate phase envelope.
        4. Consider the presence of inhibitors and their effect on shifting the hydrate boundary.
        5. Assess uncertainties in input data and model limitations.
        6. Evaluate operational margins and safety factors.
        7. Reference field experience and laboratory data for similar systems.
        8. Document assumptions and rationale for prediction.
        """,
        key_factors=[
            "Gas composition",
            "Water content",
            "Pressure and temperature profiles",
            "Presence and concentration of inhibitors",
            "Model selection and calibration",
            "Uncertainty in input data"
        ],
        primary_authority=[
            "Sloan, E.D. & Koh, C.A. (2008) Clathrate Hydrates of Natural Gases",
            "API Technical Report 17TR6",
            "ISO 13691"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="Hydrate formation is unlikely under current conditions; models overpredict risk.",
        counter_arguments=[
            "Field data shows hydrate plugs at similar conditions.",
            "Inhibitor effectiveness may be overestimated.",
            "Model uncertainties necessitate conservative approach."
        ],
        resolution_strategy="Apply conservative safety margins and validate predictions with field or laboratory data.",
        entity_scope="Production pipelines, subsea flowlines, and process equipment",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Chevron North Sea hydrate management case studies"
    ),
    DoctrineBlock(
        topic="Monoethylene Glycol (MEG) Hydrate Inhibition",
        keywords=["MEG", "hydrate inhibition", "thermodynamics", "glycol", "inhibitor", "dosage"],
        conclusion_template="MEG injection at the calculated dosage will suppress hydrate formation below the minimum operating temperature for the specified pipeline segment.",
        reasoning_framework="""
        1. Determine hydrate formation temperature (HFT) without inhibitor.
        2. Calculate required MEG concentration to depress HFT below minimum expected temperature.
        3. Use validated thermodynamic models (e.g., PVTSim, Multiflash) for MEG-water-hydrocarbon systems.
        4. Factor in MEG losses due to partitioning, dilution, and carryover.
        5. Account for operational upsets and injection reliability.
        6. Reference field experience for similar systems.
        7. Document calculations and safety margins.
        """,
        key_factors=[
            "Hydrate formation temperature",
            "Minimum pipeline temperature",
            "MEG partitioning and losses",
            "Injection reliability",
            "Thermodynamic model accuracy"
        ],
        primary_authority=[
            "API Technical Report 17TR6",
            "Sloan & Koh (2008)",
            "DNVGL-RP-F112"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="MEG dosage is excessive; operational cost can be reduced.",
        counter_arguments=[
            "Under-dosing risks hydrate plug formation.",
            "Partitioning losses may be underestimated.",
            "Operational upsets require conservative dosing."
        ],
        resolution_strategy="Validate dosage with laboratory and field data; apply safety factors.",
        entity_scope="Subsea and topside production systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Statoil Åsgard MEG management program"
    ),
    DoctrineBlock(
        topic="Low Dosage Hydrate Inhibitor (LDHI) Application",
        keywords=["LDHI", "hydrate inhibitor", "KHI", "AA", "low dosage", "flow assurance"],
        conclusion_template="LDHI application is feasible for the specified system if subcooling does not exceed the validated performance envelope for the selected chemical.",
        reasoning_framework="""
        1. Assess system subcooling (difference between hydrate formation temperature and minimum operating temperature).
        2. Select LDHI type: kinetic hydrate inhibitor (KHI) or anti-agglomerant (AA).
        3. Review laboratory and field performance data for candidate LDHIs.
        4. Evaluate compatibility with system fluids and materials.
        5. Determine required dosage and injection strategy.
        6. Consider potential for chemical degradation, partitioning, and loss.
        7. Assess operational risks and mitigation measures.
        8. Document selection rationale and performance envelope.
        """,
        key_factors=[
            "System subcooling",
            "LDHI performance envelope",
            "Fluid compatibility",
            "Chemical stability",
            "Injection reliability"
        ],
        primary_authority=[
            "API 17TR6",
            "SPE 100568",
            "DNVGL-RP-F112"
        ],
        burden_holder="Chemical engineer/flow assurance specialist",
        adversary_position="LDHI is not reliable under high subcooling or variable flow regimes.",
        counter_arguments=[
            "Field trials demonstrate LDHI effectiveness within validated envelope.",
            "Conservative subcooling limits applied.",
            "Backup thermodynamic inhibition strategy available."
        ],
        resolution_strategy="Limit LDHI use to validated conditions; monitor performance and adjust strategy as needed.",
        entity_scope="Subsea tiebacks, deepwater flowlines",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="BP King Field LDHI deployment"
    ),
    DoctrineBlock(
        topic="Wax Appearance Temperature (WAT) and Cloud Point",
        keywords=["wax", "WAT", "cloud point", "paraffin", "deposition", "thermodynamics"],
        conclusion_template="WAT is determined by laboratory analysis and model prediction; wax management is required if operating temperatures fall below WAT.",
        reasoning_framework="""
        1. Obtain representative fluid samples.
        2. Conduct laboratory measurements (e.g., DSC, viscometry) to determine WAT and cloud point.
        3. Use thermodynamic models (e.g., PVTsim, Multiflash) to predict WAT under varying pressures.
        4. Compare operating temperature profiles to WAT.
        5. Assess uncertainty in laboratory and model results.
        6. Consider compositional changes over field life.
        7. Document WAT determination and implications for flow assurance.
        """,
        key_factors=[
            "Fluid composition",
            "Laboratory WAT/Cloud Point data",
            "Thermodynamic model calibration",
            "Operating temperature profile",
            "Compositional changes"
        ],
        primary_authority=[
            "API Technical Report 18TR3",
            "SPE 124584",
            "DNVGL-RP-F103"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="WAT is overestimated; risk of wax deposition is minimal.",
        counter_arguments=[
            "Field experience shows wax deposition below WAT.",
            "Model and lab uncertainties require conservative approach.",
            "Compositional changes may lower WAT over time."
        ],
        resolution_strategy="Use conservative WAT estimates; monitor for wax deposition in operation.",
        entity_scope="Production pipelines, risers, and process equipment",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Shell Bonga wax management program"
    ),
    DoctrineBlock(
        topic="Wax Deposition Modeling and Prediction",
        keywords=["wax", "deposition", "modeling", "prediction", "paraffin", "flow assurance"],
        conclusion_template="Wax deposition risk is predicted using validated models; mitigation is required if predicted deposit thickness exceeds operational limits.",
        reasoning_framework="""
        1. Characterize fluid composition and wax content.
        2. Determine WAT and wax precipitation curve.
        3. Select appropriate wax deposition model (e.g., multilayer, heat/mass transfer).
        4. Input pipeline geometry, temperature, and flow regime.
        5. Calibrate model with laboratory or field data.
        6. Predict wax deposition rate and thickness over time.
        7. Assess impact on pressure drop and pigging frequency.
        8. Document assumptions, uncertainties, and mitigation requirements.
        """,
        key_factors=[
            "Wax content and composition",
            "Pipeline temperature profile",
            "Flow regime",
            "Model calibration",
            "Pigging and chemical inhibition strategy"
        ],
        primary_authority=[
            "SPE 124584",
            "API 18TR3",
            "DNVGL-RP-F103"
        ],
        burden_holder="Flow assurance team",
        adversary_position="Models overpredict wax risk; actual deposition is less severe.",
        counter_arguments=[
            "Field data supports model predictions.",
            "Uncertainties in wax precipitation require conservative approach.",
            "Pigging and chemical mitigation are standard practice."
        ],
        resolution_strategy="Validate models with field data; adjust mitigation as needed.",
        entity_scope="Long subsea pipelines, multiphase flowlines",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="Total Girassol wax management"
    ),
    DoctrineBlock(
        topic="Chemical Wax Inhibitors and Pour Point Depressants",
        keywords=["wax inhibitor", "pour point depressant", "PPD", "chemical treatment", "wax management"],
        conclusion_template="Chemical wax inhibitors and PPDs are recommended if laboratory and field data demonstrate effective reduction in wax deposition and pour point.",
        reasoning_framework="""
        1. Screen candidate chemicals for compatibility with system fluids.
        2. Conduct laboratory tests (cold finger, PPD tests) to determine effectiveness.
        3. Evaluate impact on wax deposition rate and pour point.
        4. Assess chemical stability, partitioning, and injection logistics.
        5. Review field trial data and operational experience.
        6. Determine optimal dosage and injection points.
        7. Monitor performance and adjust strategy as needed.
        8. Document selection rationale and performance envelope.
        """,
        key_factors=[
            "Chemical effectiveness",
            "Fluid compatibility",
            "Injection logistics",
            "Field trial results",
            "Operational monitoring"
        ],
        primary_authority=[
            "API 18TR3",
            "SPE 124584",
            "DNVGL-RP-F103"
        ],
        burden_holder="Chemical engineer",
        adversary_position="Chemical treatment is unnecessary; pigging alone is sufficient.",
        counter_arguments=[
            "Pigging frequency may be operationally constrained.",
            "Chemicals provide continuous mitigation.",
            "Field data supports combined strategy."
        ],
        resolution_strategy="Implement combined chemical and mechanical mitigation; monitor and optimize.",
        entity_scope="Subsea and onshore pipelines",
        confidence=0.84,
        confidence_zone="Medium-High",
        controlling_precedent="Chevron Agbami wax inhibitor program"
    ),
    DoctrineBlock(
        topic="Asphaltene Onset Pressure and Precipitation Envelope",
        keywords=["asphaltene", "onset pressure", "precipitation", "envelope", "phase behavior"],
        conclusion_template="Asphaltene onset pressure and precipitation envelope are defined by laboratory PVT analysis and model prediction; risk management is required if operating conditions cross these boundaries.",
        reasoning_framework="""
        1. Obtain representative fluid samples for PVT analysis.
        2. Conduct laboratory tests (e.g., filtration, microscopy, light scattering) to determine asphaltene onset pressure (AOP).
        3. Use equation of state (EOS) models to predict precipitation envelope.
        4. Compare operating pressure and temperature profiles to AOP and envelope.
        5. Assess uncertainty in laboratory and model results.
        6. Consider compositional changes and pressure cycling.
        7. Document findings and implications for flow assurance.
        """,
        key_factors=[
            "Fluid composition",
            "Laboratory AOP data",
            "EOS model calibration",
            "Operating pressure/temperature profile",
            "Compositional changes"
        ],
        primary_authority=[
            "SPE 71434",
            "API 18TR3",
            "DNVGL-RP-F103"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="Asphaltene risk is overstated; field experience shows no deposition.",
        counter_arguments=[
            "Pressure cycling may trigger asphaltene precipitation.",
            "Compositional changes over field life increase risk.",
            "Model and lab uncertainties require conservative approach."
        ],
        resolution_strategy="Monitor for asphaltene deposition; apply chemical or operational mitigation as needed.",
        entity_scope="Production wells, pipelines, and separators",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="Petrobras deepwater asphaltene management"
    ),
    DoctrineBlock(
        topic="Scale Prediction and Saturation Index Modeling",
        keywords=["scale", "prediction", "saturation index", "mineral scale", "modeling", "inorganic"],
        conclusion_template="Scale risk is predicted using validated saturation index models; mitigation is required if supersaturation is indicated under operating conditions.",
        reasoning_framework="""
        1. Analyze produced water composition (major ions, pH, temperature, pressure).
        2. Use validated scale prediction software (e.g., ScaleChem, OLI) to calculate saturation indices for key minerals (e.g., CaCO3, BaSO4).
        3. Identify conditions where supersaturation and scale precipitation are likely.
        4. Assess impact of pressure/temperature changes and mixing with incompatible waters.
        5. Consider uncertainties in water analysis and model predictions.
        6. Document findings and recommend mitigation if required.
        """,
        key_factors=[
            "Produced water composition",
            "Saturation index calculation",
            "Mixing of incompatible waters",
            "Pressure/temperature changes",
            "Model calibration"
        ],
        primary_authority=[
            "API RP 14J",
            "SPE 169747",
            "DNVGL-RP-O501"
        ],
        burden_holder="Production chemist/flow assurance engineer",
        adversary_position="Scale risk is minimal; water analysis is conservative.",
        counter_arguments=[
            "Mixing with seawater or other sources increases risk.",
            "Uncertainties in water analysis require conservative approach.",
            "Field experience supports model predictions."
        ],
        resolution_strategy="Implement scale inhibition or water management as required; monitor for scale formation.",
        entity_scope="Production wells, pipelines, and process equipment",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="BP North Sea scale management"
    ),
    DoctrineBlock(
        topic="Scale Inhibitor Squeeze Treatment Design",
        keywords=["scale inhibitor", "squeeze", "treatment", "design", "scale management"],
        conclusion_template="Squeeze treatment is designed based on formation properties, scale risk, and inhibitor return profile to ensure effective scale control over the planned interval.",
        reasoning_framework="""
        1. Characterize formation properties (porosity, permeability, mineralogy).
        2. Assess scale risk and required protection interval.
        3. Select appropriate scale inhibitor chemistry and loading.
        4. Design squeeze treatment volume, rate, and placement.
        5. Model inhibitor return profile and treatment lifetime.
        6. Consider operational constraints and compatibility.
        7. Monitor inhibitor return and adjust treatment as needed.
        8. Document design basis and performance monitoring plan.
        """,
        key_factors=[
            "Formation properties",
            "Scale risk assessment",
            "Inhibitor chemistry selection",
            "Treatment volume and placement",
            "Return profile modeling"
        ],
        primary_authority=[
            "API RP 14J",
            "SPE 169747",
            "DNVGL-RP-O501"
        ],
        burden_holder="Production chemist/reservoir engineer",
        adversary_position="Squeeze treatments are costly and may damage formation.",
        counter_arguments=[
            "Proper design minimizes formation damage.",
            "Squeeze extends scale control interval, reducing downtime.",
            "Field experience supports squeeze effectiveness."
        ],
        resolution_strategy="Optimize squeeze design; monitor performance and minimize formation damage.",
        entity_scope="Production wells and near-wellbore regions",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="Shell North Sea squeeze programs"
    ),
    DoctrineBlock(
        topic="Terrain-Induced Slugging in Hilly Pipelines",
        keywords=["terrain slugging", "hilly pipelines", "multiphase flow", "slugging", "flow assurance"],
        conclusion_template="Terrain-induced slugging is predicted if pipeline elevation profile and flow regime analysis indicate liquid accumulation and periodic slug formation.",
        reasoning_framework="""
        1. Obtain detailed pipeline elevation profile.
        2. Analyze flow regime using multiphase flow models (e.g., OLGA, LedaFlow).
        3. Identify low points and potential for liquid holdup.
        4. Assess operating conditions (flow rates, pressures, temperatures).
        5. Predict slug frequency and magnitude.
        6. Evaluate impact on downstream facilities and equipment.
        7. Consider operational mitigation (e.g., flow rate adjustment, slug catchers).
        8. Document findings and recommended actions.
        """,
        key_factors=[
            "Pipeline elevation profile",
            "Multiphase flow regime",
            "Liquid holdup potential",
            "Operating conditions",
            "Mitigation options"
        ],
        primary_authority=[
            "API RP 14E",
            "SPE 124584",
            "DNVGL-RP-F103"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="Slugging is transient and manageable; no intervention required.",
        counter_arguments=[
            "Slugging can cause process upsets and equipment damage.",
            "Model predictions validated by field data.",
            "Mitigation reduces operational risk."
        ],
        resolution_strategy="Implement operational or design mitigation as required; monitor for slugging events.",
        entity_scope="Onshore and offshore multiphase pipelines",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="Equinor Troll field terrain slugging management"
    ),
    DoctrineBlock(
        topic="Multiphase Flow Correlations and Pressure Drop Prediction",
        keywords=["multiphase flow", "correlations", "pressure drop", "prediction", "flow regime"],
        conclusion_template="Pressure drop is predicted using validated multiphase flow correlations; design and operation must account for model uncertainty and calibration.",
        reasoning_framework="""
        1. Characterize fluid properties and pipeline geometry.
        2. Select appropriate multiphase flow correlation (e.g., Beggs & Brill, TUFFP, OLGA).
        3. Input operating conditions (flow rates, pressures, temperatures).
        4. Calibrate model with field or laboratory data if available.
        5. Predict pressure drop and flow regime along pipeline.
        6. Assess model limitations and uncertainty.
        7. Document correlation selection and calibration process.
        """,
        key_factors=[
            "Fluid properties",
            "Pipeline geometry",
            "Flow regime",
            "Model calibration",
            "Operating conditions"
        ],
        primary_authority=[
            "API RP 14E",
            "SPE 124584",
            "DNVGL-RP-F103"
        ],
        burden_holder="Flow assurance/process engineer",
        adversary_position="Correlation is not representative for this system; results are unreliable.",
        counter_arguments=[
            "Calibration with field data improves accuracy.",
            "Multiple correlations can be compared.",
            "Uncertainty is addressed in design margins."
        ],
        resolution_strategy="Use calibrated models and conservative design margins; validate predictions with field data.",
        entity_scope="Production pipelines and flowlines",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Chevron multiphase pipeline design"
    ),
    DoctrineBlock(
        topic="Intelligent Pigging for Pipeline Inspection",
        keywords=["intelligent pigging", "pipeline inspection", "ILI", "corrosion", "integrity"],
        conclusion_template="Intelligent pigging is required at intervals determined by risk assessment to detect corrosion, wall loss, and other integrity threats.",
        reasoning_framework="""
        1. Assess pipeline age, material, and operating history.
        2. Conduct risk assessment for internal and external threats (corrosion, erosion, mechanical damage).
        3. Determine inspection interval based on risk and regulatory requirements.
        4. Select appropriate ILI technology (MFL, UT, EMAT).
        5. Plan and execute pigging operation.
        6. Analyze inspection data and identify anomalies.
        7. Document findings and recommend remedial actions.
        """,
        key_factors=[
            "Pipeline material and age",
            "Corrosion/erosion risk",
            "Regulatory requirements",
            "ILI technology selection",
            "Inspection interval"
        ],
        primary_authority=[
            "API 1163",
            "DNVGL-RP-F116",
            "PHMSA regulations"
        ],
        burden_holder="Pipeline integrity engineer",
        adversary_position="Pigging frequency is excessive; cost can be reduced.",
        counter_arguments=[
            "Regulatory compliance requires minimum inspection frequency.",
            "ILI detects early-stage threats, reducing long-term risk.",
            "Industry experience supports current intervals."
        ],
        resolution_strategy="Base inspection interval on risk assessment and regulatory requirements.",
        entity_scope="Onshore and offshore pipelines",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Transco pipeline ILI program"
    ),
    DoctrineBlock(
        topic="Pigging Frequency Optimization for Wax Removal",
        keywords=["pigging", "frequency", "wax removal", "optimization", "pipeline cleaning"],
        conclusion_template="Pigging frequency is optimized based on wax deposition rate, operational constraints, and risk of blockage.",
        reasoning_framework="""
        1. Predict wax deposition rate using validated models.
        2. Monitor pipeline pressure drop and pig return data.
        3. Assess operational constraints (e.g., production schedule, pig launcher/receiver availability).
        4. Optimize pigging frequency to balance wax removal and operational cost.
        5. Adjust frequency based on field experience and monitoring data.
        6. Document optimization process and rationale.
        """,
        key_factors=[
            "Wax deposition rate",
            "Pressure drop monitoring",
            "Operational constraints",
            "Pigging logistics",
            "Field experience"
        ],
        primary_authority=[
            "API 18TR3",
            "SPE 124584",
            "DNVGL-RP-F103"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="Pigging is too frequent; operational efficiency is reduced.",
        counter_arguments=[
            "Reduced frequency increases risk of blockage.",
            "Monitoring data supports current schedule.",
            "Optimization balances risk and cost."
        ],
        resolution_strategy="Continuously optimize frequency based on monitoring and operational feedback.",
        entity_scope="Wax-prone pipelines",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Shell Bonga pigging optimization"
    ),
    DoctrineBlock(
        topic="Emergency Depressurization and Hydrate Dissociation Risk",
        keywords=["emergency depressurization", "hydrate dissociation", "risk", "flow assurance", "pipeline safety"],
        conclusion_template="Emergency depressurization is permitted if hydrate dissociation risk is assessed and mitigated by pre-injection of inhibitors or thermal management.",
        reasoning_framework="""
        1. Assess pipeline inventory and hydrate risk under depressurization.
        2. Predict temperature drop and hydrate stability using thermodynamic models.
        3. Evaluate risk of hydrate plug formation during/after depressurization.
        4. Plan mitigation (e.g., pre-injection of MEG, thermal insulation, controlled depressurization rate).
        5. Document risk assessment and mitigation plan.
        6. Train operations personnel on emergency procedures.
        """,
        key_factors=[
            "Pipeline inventory and composition",
            "Temperature drop during depressurization",
            "Hydrate stability envelope",
            "Mitigation strategy",
            "Operational procedures"
        ],
        primary_authority=[
            "API 521",
            "SPE 100568",
            "DNVGL-RP-F112"
        ],
        burden_holder="Operations/flow assurance engineer",
        adversary_position="Depressurization should be avoided; hydrate risk is too high.",
        counter_arguments=[
            "Mitigation strategies reduce risk to acceptable levels.",
            "Emergency procedures are necessary for safety.",
            "Field experience supports controlled depressurization."
        ],
        resolution_strategy="Implement mitigation and train personnel; review procedures regularly.",
        entity_scope="Subsea and onshore pipelines",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="BP Thunder Horse depressurization protocol"
    ),
    DoctrineBlock(
        topic="Sweet Corrosion from CO2 in Production Systems",
        keywords=["sweet corrosion", "CO2", "corrosion", "production systems", "carbonic acid"],
        conclusion_template="Sweet corrosion risk is managed by material selection, corrosion inhibition, and monitoring if CO2 partial pressure exceeds threshold values.",
        reasoning_framework="""
        1. Determine CO2 partial pressure in produced fluids.
        2. Assess corrosion risk using NACE MR0175/ISO 15156 guidelines.
        3. Select corrosion-resistant materials or apply chemical inhibition.
        4. Implement corrosion monitoring (e.g., coupons, ER probes).
        5. Adjust mitigation strategy based on monitoring data.
        6. Document risk assessment and mitigation plan.
        """,
        key_factors=[
            "CO2 partial pressure",
            "Material selection",
            "Corrosion inhibitor effectiveness",
            "Monitoring data",
            "Industry standards"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156",
            "API RP 14E",
            "DNVGL-RP-F103"
        ],
        burden_holder="Corrosion engineer",
        adversary_position="Corrosion risk is overstated; inhibitor is unnecessary.",
        counter_arguments=[
            "Field failures have occurred at low CO2 levels.",
            "Monitoring data supports need for inhibition.",
            "Industry standards require mitigation above threshold."
        ],
        resolution_strategy="Follow industry standards and monitoring; adjust mitigation as needed.",
        entity_scope="Production wells, pipelines, and facilities",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ConocoPhillips Ekofisk corrosion management"
    ),
    DoctrineBlock(
        topic="Erosional Velocity and API RP 14E Criterion",
        keywords=["erosional velocity", "API RP 14E", "velocity limit", "erosion", "pipeline design"],
        conclusion_template="Design and operation must ensure that fluid velocity does not exceed the erosional velocity limit as defined by API RP 14E to prevent pipe wall thinning.",
        reasoning_framework="""
        1. Calculate erosional velocity using API RP 14E formula: V_e = C * sqrt(2g(ρ_s - ρ_f)/ρ_f).
        2. Select appropriate C-factor based on fluid phase and solids content.
        3. Compare predicted operating velocity to erosional velocity limit.
        4. Assess risk of erosion-corrosion and sand production.
        5. Document design and operational controls to maintain velocity below limit.
        6. Monitor for erosion using inspection data.
        """,
        key_factors=[
            "Fluid properties (density, phase)",
            "C-factor selection",
            "Operating velocity",
            "Sand production risk",
            "Inspection/monitoring data"
        ],
        primary_authority=[
            "API RP 14E",
            "DNVGL-RP-O501",
            "SPE 169747"
        ],
        burden_holder="Pipeline/process engineer",
        adversary_position="Higher velocities are acceptable; API RP 14E is conservative.",
        counter_arguments=[
            "Field failures have occurred above API limits.",
            "Inspection data supports conservative limits.",
            "Industry standards require compliance."
        ],
        resolution_strategy="Design and operate within API RP 14E limits; monitor for erosion.",
        entity_scope="Production pipelines and flowlines",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="API RP 14E global adoption"
    ),
    # 25+ more DoctrineBlock instances with real domain content follow:
    DoctrineBlock(
        topic="Hydrate Plug Remediation Strategies",
        keywords=["hydrate plug", "remediation", "dissociation", "depressurization", "thermal", "chemical"],
        conclusion_template="Hydrate plug remediation is selected based on plug location, system configuration, and safety considerations, prioritizing depressurization, thermal, or chemical methods as appropriate.",
        reasoning_framework="""
        1. Locate hydrate plug using pressure/temperature data and pig tracking.
        2. Assess system configuration and isolation options.
        3. Evaluate feasibility of depressurization, thermal, or chemical remediation.
        4. Prioritize depressurization if safe and practical.
        5. Consider thermal remediation (e.g., heating, hot oil) if accessible.
        6. Use chemical injection (e.g., MEG, methanol) if other methods are impractical.
        7. Monitor progress and adjust strategy as needed.
        8. Document remediation plan and safety precautions.
        """,
        key_factors=[
            "Plug location and accessibility",
            "System isolation capability",
            "Remediation method feasibility",
            "Safety considerations",
            "Monitoring and control"
        ],
        primary_authority=[
            "API 17TR6",
            "SPE 100568",
            "DNVGL-RP-F112"
        ],
        burden_holder="Operations/flow assurance engineer",
        adversary_position="Plug remediation is too risky; system should remain shut-in.",
        counter_arguments=[
            "Controlled remediation reduces downtime.",
            "Safety protocols mitigate risk.",
            "Field experience supports remediation effectiveness."
        ],
        resolution_strategy="Follow established remediation protocols; prioritize safety and system integrity.",
        entity_scope="Subsea and onshore pipelines",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="BP Thunder Horse hydrate plug remediation"
    ),
    DoctrineBlock(
        topic="Thermal Insulation for Flow Assurance",
        keywords=["thermal insulation", "flow assurance", "heat loss", "pipeline", "cold flow"],
        conclusion_template="Thermal insulation is required if heat loss modeling predicts fluid temperature will fall below hydrate or wax appearance temperature before reaching destination.",
        reasoning_framework="""
        1. Model heat loss along pipeline using validated thermal models.
        2. Compare predicted fluid temperature to hydrate and wax appearance temperatures.
        3. Assess insulation options (e.g., wet insulation, pipe-in-pipe, active heating).
        4. Evaluate cost, installation, and operational constraints.
        5. Select insulation system to maintain temperature above critical thresholds.
        6. Document design basis and performance monitoring plan.
        """,
        key_factors=[
            "Heat loss modeling",
            "Critical temperature thresholds",
            "Insulation system selection",
            "Cost and installation constraints",
            "Performance monitoring"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Pipeline/project engineer",
        adversary_position="Insulation is unnecessary; chemical inhibition is sufficient.",
        counter_arguments=[
            "Combined insulation and inhibition provides redundancy.",
            "Insulation reduces chemical consumption.",
            "Field data supports insulation effectiveness."
        ],
        resolution_strategy="Implement insulation if modeling predicts subcooling; monitor performance.",
        entity_scope="Subsea and cold-climate pipelines",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Shell Bonga subsea insulation"
    ),
    DoctrineBlock(
        topic="Sand Production and Erosion Control",
        keywords=["sand production", "erosion", "control", "sand management", "pipeline integrity"],
        conclusion_template="Sand production is managed by monitoring, sand control completions, and erosion-resistant materials to prevent pipeline and equipment damage.",
        reasoning_framework="""
        1. Assess sand production risk using formation and well data.
        2. Implement sand control completions (e.g., screens, gravel packs) if required.
        3. Select erosion-resistant materials for high-risk areas.
        4. Monitor sand production using acoustic detectors or sand probes.
        5. Adjust production rates to minimize sand transport.
        6. Document sand management strategy and monitoring plan.
        """,
        key_factors=[
            "Formation sand risk",
            "Sand control completion design",
            "Material selection",
            "Sand monitoring",
            "Production rate management"
        ],
        primary_authority=[
            "API RP 14E",
            "DNVGL-RP-O501",
            "SPE 169747"
        ],
        burden_holder="Production/operations engineer",
        adversary_position="Sand control is unnecessary; production rates are low.",
        counter_arguments=[
            "Unexpected sand production can cause rapid damage.",
            "Monitoring provides early warning.",
            "Industry standards recommend proactive management."
        ],
        resolution_strategy="Implement monitoring and control; adjust strategy based on data.",
        entity_scope="Production wells, pipelines, and facilities",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="ExxonMobil sand management"
    ),
    DoctrineBlock(
        topic="Produced Water Management and Discharge",
        keywords=["produced water", "management", "discharge", "regulation", "treatment"],
        conclusion_template="Produced water must be treated to meet regulatory discharge limits; management strategy includes reinjection, treatment, or disposal as appropriate.",
        reasoning_framework="""
        1. Analyze produced water composition and volume.
        2. Identify applicable regulatory discharge limits.
        3. Evaluate treatment options (e.g., hydrocyclones, flotation, membranes).
        4. Assess feasibility of reinjection or alternative disposal.
        5. Monitor discharge quality and compliance.
        6. Document management strategy and contingency plans.
        """,
        key_factors=[
            "Produced water composition",
            "Regulatory limits",
            "Treatment technology selection",
            "Discharge monitoring",
            "Disposal/reinjection feasibility"
        ],
        primary_authority=[
            "US EPA NPDES",
            "OSPAR Convention",
            "API RP 45"
        ],
        burden_holder="Environmental/production engineer",
        adversary_position="Treatment is excessive; discharge quality is adequate without it.",
        counter_arguments=[
            "Regulatory non-compliance risks fines and shutdown.",
            "Treatment ensures environmental protection.",
            "Monitoring verifies performance."
        ],
        resolution_strategy="Meet or exceed regulatory limits; monitor and optimize treatment.",
        entity_scope="Offshore and onshore production facilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="North Sea produced water management"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management Systems (PIMS)",
        keywords=["pipeline integrity", "PIMS", "management system", "integrity", "risk"],
        conclusion_template="A Pipeline Integrity Management System is required to ensure safe operation, regulatory compliance, and risk reduction throughout pipeline lifecycle.",
        reasoning_framework="""
        1. Develop and implement a documented PIMS in accordance with industry standards.
        2. Conduct regular risk assessments and integrity reviews.
        3. Integrate inspection, monitoring, and maintenance data.
        4. Establish procedures for anomaly response and repair.
        5. Train personnel and maintain records.
        6. Continuously improve system based on performance and incidents.
        """,
        key_factors=[
            "Risk assessment",
            "Inspection and monitoring",
            "Maintenance and repair procedures",
            "Personnel training",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA 49 CFR 192/195",
            "DNVGL-RP-F116"
        ],
        burden_holder="Pipeline operator",
        adversary_position="PIMS is bureaucratic and adds little value.",
        counter_arguments=[
            "PIMS reduces incident frequency and severity.",
            "Regulatory compliance is mandatory.",
            "Continuous improvement enhances safety."
        ],
        resolution_strategy="Implement and maintain PIMS; audit regularly.",
        entity_scope="All pipeline assets",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="TransCanada PIMS implementation"
    ),
    DoctrineBlock(
        topic="Microbial Induced Corrosion (MIC) Management",
        keywords=["MIC", "microbial corrosion", "bacteria", "corrosion management", "pipeline integrity"],
        conclusion_template="MIC risk is managed by monitoring, biocide treatment, and material selection in systems with water and nutrients supporting microbial growth.",
        reasoning_framework="""
        1. Assess MIC risk based on water chemistry and operating conditions.
        2. Monitor for microbial activity using culture and molecular methods.
        3. Apply biocide treatment as needed.
        4. Select materials resistant to microbial corrosion.
        5. Document monitoring and mitigation strategy.
        6. Adjust treatment based on monitoring data.
        """,
        key_factors=[
            "Water chemistry",
            "Microbial monitoring data",
            "Biocide selection and application",
            "Material selection",
            "Operational adjustments"
        ],
        primary_authority=[
            "NACE SP0775",
            "API RP 14E",
            "DNVGL-RP-F103"
        ],
        burden_holder="Corrosion/production chemist",
        adversary_position="MIC is not a significant risk in this system.",
        counter_arguments=[
            "MIC can cause rapid localized corrosion.",
            "Monitoring provides early detection.",
            "Biocide treatment is cost-effective."
        ],
        resolution_strategy="Monitor and treat for MIC as indicated; review strategy regularly.",
        entity_scope="Water-handling pipelines and facilities",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="BP North Sea MIC management"
    ),
    DoctrineBlock(
        topic="Pipeline Leak Detection and Response",
        keywords=["pipeline leak", "detection", "response", "integrity", "monitoring"],
        conclusion_template="Leak detection systems and response protocols are required to minimize environmental impact and loss of containment.",
        reasoning_framework="""
        1. Implement leak detection systems (e.g., mass balance, acoustic, fiber optic).
        2. Establish response protocols for suspected leaks.
        3. Train personnel in leak detection and response.
        4. Regularly test and calibrate detection systems.
        5. Document incidents and corrective actions.
        6. Continuously improve leak detection and response based on performance.
        """,
        key_factors=[
            "Detection technology selection",
            "Response protocol effectiveness",
            "Personnel training",
            "System calibration",
            "Incident documentation"
        ],
        primary_authority=[
            "API 1130",
            "PHMSA 49 CFR 195.444",
            "DNVGL-RP-F116"
        ],
        burden_holder="Pipeline operator",
        adversary_position="Leak detection systems are costly and unnecessary.",
        counter_arguments=[
            "Early detection minimizes environmental and financial impact.",
            "Regulatory compliance is required.",
            "Continuous improvement reduces risk."
        ],
        resolution_strategy="Implement, test, and improve leak detection and response systems.",
        entity_scope="All pipelines",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="Enbridge leak detection program"
    ),
    DoctrineBlock(
        topic="Pipeline Decommissioning and Abandonment",
        keywords=["pipeline decommissioning", "abandonment", "regulation", "environmental", "integrity"],
        conclusion_template="Decommissioning and abandonment must follow regulatory requirements and minimize environmental and safety risks.",
        reasoning_framework="""
        1. Develop decommissioning plan in accordance with regulations.
        2. Assess environmental and safety risks.
        3. Remove hydrocarbons and hazardous materials.
        4. Plug and abandon pipeline as required.
        5. Monitor site post-abandonment.
        6. Document process and regulatory compliance.
        """,
        key_factors=[
            "Regulatory requirements",
            "Environmental risk assessment",
            "Hydrocarbon removal",
            "Plugging and abandonment procedures",
            "Post-abandonment monitoring"
        ],
        primary_authority=[
            "API 1102",
            "OSPAR Decision 98/3",
            "PHMSA 49 CFR 192/195"
        ],
        burden_holder="Pipeline operator",
        adversary_position="Decommissioning is premature; pipeline can be repurposed.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Environmental risks must be managed.",
            "Repurposing is evaluated as part of planning."
        ],
        resolution_strategy="Follow regulatory process; evaluate repurposing as part of planning.",
        entity_scope="All pipeline assets",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Shell Brent decommissioning"
    ),
    DoctrineBlock(
        topic="Subsea Tieback Flow Assurance Integration",
        keywords=["subsea tieback", "flow assurance", "integration", "project design", "risk"],
        conclusion_template="Flow assurance integration is required in early project design for subsea tiebacks to identify and mitigate hydrate, wax, asphaltene, and scale risks.",
        reasoning_framework="""
        1. Conduct early flow assurance risk assessment for tieback.
        2. Integrate hydrate, wax, asphaltene, and scale management into design.
        3. Evaluate insulation, chemical injection, and pigging options.
        4. Model transient and steady-state flow conditions.
        5. Document integrated flow assurance strategy.
        6. Update strategy as project progresses.
        """,
        key_factors=[
            "Early risk assessment",
            "Integrated mitigation options",
            "Modeling of flow conditions",
            "Design flexibility",
            "Project documentation"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Project/flow assurance engineer",
        adversary_position="Integration delays project and adds cost.",
        counter_arguments=[
            "Early integration reduces lifecycle risk and cost.",
            "Design flexibility improves project outcomes.",
            "Industry experience supports integration."
        ],
        resolution_strategy="Integrate flow assurance early; update as project evolves.",
        entity_scope="Subsea tiebacks and brownfield expansions",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Chevron Jack/St. Malo tieback"
    ),
    DoctrineBlock(
        topic="Transient Simulation for Flow Assurance",
        keywords=["transient simulation", "flow assurance", "dynamic modeling", "OLGA", "startup", "shutdown"],
        conclusion_template="Transient simulation is required for critical operations (startup, shutdown, pigging) to predict flow assurance risks and optimize procedures.",
        reasoning_framework="""
        1. Identify critical operations requiring transient analysis.
        2. Build dynamic model using validated software (e.g., OLGA, LedaFlow).
        3. Input accurate fluid, geometry, and operating data.
        4. Simulate scenarios (startup, shutdown, pigging).
        5. Analyze results for hydrate, wax, and slugging risks.
        6. Optimize procedures based on simulation outcomes.
        7. Document modeling assumptions and recommendations.
        """,
        key_factors=[
            "Critical operation identification",
            "Model accuracy and validation",
            "Scenario simulation",
            "Risk analysis",
            "Procedure optimization"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="Steady-state analysis is sufficient; transient modeling is unnecessary.",
        counter_arguments=[
            "Transient risks are not captured by steady-state models.",
            "Simulation optimizes procedures and reduces risk.",
            "Industry experience supports transient analysis."
        ],
        resolution_strategy="Use transient simulation for critical operations; update models as data improves.",
        entity_scope="Complex and deepwater production systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="BP Thunder Horse transient modeling"
    ),
    DoctrineBlock(
        topic="Chemical Injection System Reliability",
        keywords=["chemical injection", "system reliability", "flow assurance", "inhibitor", "maintenance"],
        conclusion_template="Chemical injection system reliability must be ensured through redundancy, monitoring, and maintenance to prevent flow assurance upsets.",
        reasoning_framework="""
        1. Assess criticality of chemical injection for flow assurance.
        2. Design system with redundancy (e.g., dual pumps, backup lines).
        3. Implement real-time monitoring of injection rates and pressures.
        4. Schedule regular maintenance and testing.
        5. Document reliability strategy and contingency plans.
        6. Review system performance and update as needed.
        """,
        key_factors=[
            "System redundancy",
            "Real-time monitoring",
            "Maintenance schedule",
            "Contingency planning",
            "Performance review"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F112",
            "SPE 100568"
        ],
        burden_holder="Operations/maintenance engineer",
        adversary_position="Redundancy is excessive; cost can be reduced.",
        counter_arguments=[
            "Injection failure can cause flow assurance upsets.",
            "Redundancy reduces downtime risk.",
            "Monitoring ensures early detection of issues."
        ],
        resolution_strategy="Design for reliability; monitor and maintain system proactively.",
        entity_scope="Subsea and topside chemical injection systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Shell Bonga chemical injection reliability"
    ),
    DoctrineBlock(
        topic="Flow Assurance Risk Register Management",
        keywords=["flow assurance", "risk register", "management", "project", "mitigation"],
        conclusion_template="A flow assurance risk register must be maintained and updated throughout project lifecycle to track risks, mitigation, and residual exposure.",
        reasoning_framework="""
        1. Establish risk register at project inception.
        2. Identify and assess flow assurance risks.
        3. Document mitigation measures and responsible parties.
        4. Update register as risks evolve or are retired.
        5. Review register regularly with project team.
        6. Use register to inform decision-making and reporting.
        """,
        key_factors=[
            "Risk identification and assessment",
            "Mitigation documentation",
            "Regular review and update",
            "Stakeholder communication",
            "Decision-making support"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Project/flow assurance manager",
        adversary_position="Risk register is administrative overhead.",
        counter_arguments=[
            "Register improves risk visibility and management.",
            "Supports informed decision-making.",
            "Industry best practice."
        ],
        resolution_strategy="Maintain and review risk register; integrate with project management.",
        entity_scope="All flow assurance projects",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Chevron deepwater risk register management"
    ),
    DoctrineBlock(
        topic="Hydrate Risk Management During Extended Shutdown",
        keywords=["hydrate risk", "extended shutdown", "flow assurance", "preservation", "restart"],
        conclusion_template="Hydrate risk during extended shutdown is managed by pre-injection of inhibitors, thermal preservation, or controlled depressurization.",
        reasoning_framework="""
        1. Assess risk of hydrate formation during shutdown based on temperature and pressure.
        2. Pre-inject thermodynamic or low-dosage inhibitors as required.
        3. Apply thermal preservation (e.g., insulation, active heating) if feasible.
        4. Consider controlled depressurization to move system out of hydrate stability zone.
        5. Document shutdown and restart procedures.
        6. Monitor system during shutdown and restart.
        """,
        key_factors=[
            "Shutdown duration and conditions",
            "Inhibitor injection strategy",
            "Thermal preservation capability",
            "Depressurization feasibility",
            "Monitoring and procedures"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F112",
            "SPE 100568"
        ],
        burden_holder="Operations/flow assurance engineer",
        adversary_position="Shutdown risk is minimal; mitigation is unnecessary.",
        counter_arguments=[
            "Hydrate plugs can form rapidly in shut-in systems.",
            "Mitigation ensures safe restart.",
            "Field experience supports proactive management."
        ],
        resolution_strategy="Implement mitigation prior to shutdown; monitor and document.",
        entity_scope="Subsea and onshore pipelines",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="BP Thunder Horse extended shutdown protocol"
    ),
    DoctrineBlock(
        topic="Wax Management During Cold Restarts",
        keywords=["wax management", "cold restart", "pipeline", "flow assurance", "restart procedures"],
        conclusion_template="Cold restart procedures must include wax management strategy (e.g., pigging, chemical injection, heating) to prevent blockage.",
        reasoning_framework="""
        1. Assess wax deposition risk during cold restart.
        2. Pre-inject wax inhibitors or PPDs as required.
        3. Plan pigging operation prior to or during restart.
        4. Consider thermal management (e.g., heating) if feasible.
        5. Document restart procedure and monitoring plan.
        6. Adjust strategy based on field experience.
        """,
        key_factors=[
            "Wax deposition risk",
            "Chemical and mechanical mitigation",
            "Thermal management options",
            "Restart procedure documentation",
            "Field experience"
        ],
        primary_authority=[
            "API 18TR3",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Operations/flow assurance engineer",
        adversary_position="Wax risk is overstated; restart can proceed without mitigation.",
        counter_arguments=[
            "Blockage risk increases after cold shutdown.",
            "Mitigation ensures safe and reliable restart.",
            "Field data supports combined strategy."
        ],
        resolution_strategy="Implement wax management prior to restart; monitor and optimize.",
        entity_scope="Wax-prone pipelines",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="Shell Bonga cold restart protocol"
    ),
    DoctrineBlock(
        topic="Pigging Tool Selection and Compatibility",
        keywords=["pigging", "tool selection", "compatibility", "pipeline cleaning", "inspection"],
        conclusion_template="Pigging tool selection must ensure compatibility with pipeline geometry, fluid, and cleaning or inspection objectives.",
        reasoning_framework="""
        1. Assess pipeline geometry (diameter, bends, valves, restrictions).
        2. Identify pigging objectives (cleaning, inspection, batching).
        3. Select pig type (foam, brush, intelligent) based on objectives and compatibility.
        4. Evaluate risk of pig sticking or bypass.
        5. Document tool selection and contingency plans.
        6. Review performance after pig runs.
        """,
        key_factors=[
            "Pipeline geometry",
            "Pigging objectives",
            "Tool compatibility",
            "Risk of sticking or bypass",
            "Performance review"
        ],
        primary_authority=[
            "API 1163",
            "DNVGL-RP-F116",
            "SPE 124584"
        ],
        burden_holder="Pipeline/operations engineer",
        adversary_position="Simpler tools are sufficient; intelligent pigs are unnecessary.",
        counter_arguments=[
            "Intelligent pigs provide valuable integrity data.",
            "Tool selection improves cleaning effectiveness.",
            "Contingency planning reduces risk."
        ],
        resolution_strategy="Select tools based on objectives and compatibility; review performance.",
        entity_scope="All piggable pipelines",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Transco pigging tool selection"
    ),
    DoctrineBlock(
        topic="Flow Assurance Data Management and Analytics",
        keywords=["data management", "analytics", "flow assurance", "monitoring", "digital"],
        conclusion_template="Flow assurance data must be managed and analyzed using digital tools to support decision-making and continuous improvement.",
        reasoning_framework="""
        1. Collect and store flow assurance data (temperature, pressure, chemical injection, pigging, inspection).
        2. Implement data quality control and validation.
        3. Analyze data using digital tools and analytics platforms.
        4. Use analytics to identify trends, anomalies, and optimization opportunities.
        5. Document insights and integrate into decision-making.
        6. Continuously improve data management processes.
        """,
        key_factors=[
            "Data collection and storage",
            "Quality control",
            "Analytics tool selection",
            "Insight documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Flow assurance/data engineer",
        adversary_position="Data management is not a priority; manual review is sufficient.",
        counter_arguments=[
            "Digital tools improve efficiency and insight.",
            "Analytics identify issues early.",
            "Continuous improvement supports reliability."
        ],
        resolution_strategy="Implement digital data management and analytics; review regularly.",
        entity_scope="All flow assurance operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Chevron digital flow assurance analytics"
    ),
    DoctrineBlock(
        topic="Hydrate Inhibitor Regeneration and Reclamation",
        keywords=["hydrate inhibitor", "regeneration", "reclamation", "MEG", "TEG", "recycle"],
        conclusion_template="Hydrate inhibitor regeneration and reclamation systems must be designed to meet purity requirements and minimize losses for sustainable operation.",
        reasoning_framework="""
        1. Assess required inhibitor purity for effective hydrate inhibition.
        2. Design regeneration system (e.g., distillation, filtration) to achieve target purity.
        3. Monitor inhibitor losses and make-up requirements.
        4. Evaluate environmental and operational constraints.
        5. Document system design, monitoring, and maintenance plan.
        6. Optimize operation for efficiency and sustainability.
        """,
        key_factors=[
            "Inhibitor purity requirements",
            "Regeneration system design",
            "Loss monitoring",
            "Environmental constraints",
            "Operational optimization"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F112",
            "SPE 100568"
        ],
        burden_holder="Process/operations engineer",
        adversary_position="Regeneration is unnecessary; fresh inhibitor is cheaper.",
        counter_arguments=[
            "Regeneration reduces operating cost and environmental impact.",
            "System design ensures purity and reliability.",
            "Industry experience supports reclamation."
        ],
        resolution_strategy="Design and operate regeneration system; monitor and optimize.",
        entity_scope="Subsea and topside hydrate management systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Statoil Åsgard MEG regeneration"
    ),
    DoctrineBlock(
        topic="Scale Inhibitor Residual Monitoring",
        keywords=["scale inhibitor", "residual monitoring", "scale management", "chemical monitoring", "flow assurance"],
        conclusion_template="Residual scale inhibitor concentration must be monitored to ensure effective scale control and optimize chemical usage.",
        reasoning_framework="""
        1. Establish target residual concentration based on laboratory and field data.
        2. Implement regular sampling and analysis (e.g., colorimetry, ICP).
        3. Adjust injection rates based on monitoring results.
        4. Document monitoring program and results.
        5. Optimize chemical usage for cost and effectiveness.
        6. Review and update program as needed.
        """,
        key_factors=[
            "Target residual concentration",
            "Sampling and analysis frequency",
            "Injection rate adjustment",
            "Documentation",
            "Program optimization"
        ],
        primary_authority=[
            "API RP 14J",
            "DNVGL-RP-O501",
            "SPE 169747"
        ],
        burden_holder="Production chemist/operations engineer",
        adversary_position="Monitoring is unnecessary; injection rates are fixed.",
        counter_arguments=[
            "Monitoring ensures effective scale control.",
            "Optimizes chemical usage and cost.",
            "Field data supports adaptive approach."
        ],
        resolution_strategy="Monitor and adjust injection rates; document and review program.",
        entity_scope="Production wells and pipelines",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="BP North Sea scale inhibitor monitoring"
    ),
    DoctrineBlock(
        topic="Asphaltene Inhibitor Application and Monitoring",
        keywords=["asphaltene inhibitor", "application", "monitoring", "precipitation", "flow assurance"],
        conclusion_template="Asphaltene inhibitor application and monitoring are required if precipitation risk is predicted under operating conditions.",
        reasoning_framework="""
        1. Assess asphaltene precipitation risk using laboratory and model data.
        2. Select appropriate inhibitor based on compatibility and effectiveness.
        3. Implement injection and monitoring program.
        4. Adjust dosage based on monitoring and performance.
        5. Document application and results.
        6. Review and update strategy as needed.
        """,
        key_factors=[
            "Precipitation risk assessment",
            "Inhibitor selection",
            "Injection and monitoring program",
            "Dosage adjustment",
            "Documentation and review"
        ],
        primary_authority=[
            "API 18TR3",
            "DNVGL-RP-F103",
            "SPE 71434"
        ],
        burden_holder="Production chemist/flow assurance engineer",
        adversary_position="Inhibitor is unnecessary; precipitation risk is low.",
        counter_arguments=[
            "Risk may increase with operating changes.",
            "Monitoring ensures timely mitigation.",
            "Industry experience supports inhibitor use."
        ],
        resolution_strategy="Apply and monitor inhibitor as indicated; review strategy regularly.",
        entity_scope="Production wells, pipelines, and facilities",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="Petrobras asphaltene inhibitor program"
    ),
    DoctrineBlock(
        topic="Scale Management During Waterflood Operations",
        keywords=["scale management", "waterflood", "injection", "scale risk", "flow assurance"],
        conclusion_template="Scale management during waterflood operations requires compatibility assessment, monitoring, and chemical treatment to prevent precipitation.",
        reasoning_framework="""
        1. Assess compatibility of injection and formation waters.
        2. Predict scale risk using saturation index modeling.
        3. Implement monitoring of produced water composition.
        4. Apply scale inhibitor as required.
        5. Document management strategy and results.
        6. Adjust program based on monitoring data.
        """,
        key_factors=[
            "Water compatibility assessment",
            "Scale risk modeling",
            "Monitoring program",
            "Chemical treatment",
            "Program adjustment"
        ],
        primary_authority=[
            "API RP 14J",
            "DNVGL-RP-O501",
            "SPE 169747"
        ],
        burden_holder="Production chemist/reservoir engineer",
        adversary_position="Scale risk is overstated; monitoring alone is sufficient.",
        counter_arguments=[
            "Precipitation can cause injectivity loss.",
            "Chemical treatment is cost-effective.",
            "Monitoring supports adaptive management."
        ],
        resolution_strategy="Assess, monitor, and treat as required; review program regularly.",
        entity_scope="Waterflood injection and production systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="BP North Sea waterflood scale management"
    ),
    DoctrineBlock(
        topic="Wax and Hydrate Co-Management Strategies",
        keywords=["wax", "hydrate", "co-management", "flow assurance", "chemical inhibition"],
        conclusion_template="Co-management strategies are required when both wax and hydrate risks exist, integrating chemical, thermal, and mechanical mitigation.",
        reasoning_framework="""
        1. Assess simultaneous wax and hydrate risks.
        2. Evaluate compatibility of chemical inhibitors (e.g., MEG and PPDs).
        3. Integrate thermal management and pigging as needed.
        4. Monitor system for deposition and plugging.
        5. Document co-management strategy and performance.
        6. Adjust approach based on monitoring and field experience.
        """,
        key_factors=[
            "Simultaneous risk assessment",
            "Chemical compatibility",
            "Thermal and mechanical mitigation",
            "Monitoring and documentation",
            "Strategy adjustment"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Flow assurance engineer",
        adversary_position="Separate management is sufficient; co-management adds complexity.",
        counter_arguments=[
            "Integrated strategy reduces operational risk.",
            "Chemical compatibility is critical.",
            "Field experience supports co-management."
        ],
        resolution_strategy="Integrate mitigation strategies; monitor and adjust as needed.",
        entity_scope="Pipelines with both wax and hydrate risk",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Chevron deepwater co-management"
    ),
    DoctrineBlock(
        topic="Multiphase Metering for Flow Assurance Monitoring",
        keywords=["multiphase metering", "flow assurance", "monitoring", "production measurement", "allocation"],
        conclusion_template="Multiphase metering is required for accurate flow assurance monitoring and production allocation in multiphase systems.",
        reasoning_framework="""
        1. Assess need for multiphase metering based on system configuration.
        2. Select appropriate metering technology (e.g., Venturi, Coriolis, gamma-ray).
        3. Install and calibrate meters as per manufacturer and industry standards.
        4. Integrate metering data into flow assurance monitoring.
        5. Document installation, calibration, and maintenance.
        6. Review metering performance regularly.
        """,
        key_factors=[
            "System configuration",
            "Metering technology selection",
            "Calibration and maintenance",
            "Data integration",
            "Performance review"
        ],
        primary_authority=[
            "API MPMS",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Production/flow assurance engineer",
        adversary_position="Test separators are sufficient; multiphase meters are unnecessary.",
        counter_arguments=[
            "Meters provide continuous, real-time data.",
            "Improves flow assurance monitoring.",
            "Supports accurate allocation."
        ],
        resolution_strategy="Implement metering as required; monitor and maintain.",
        entity_scope="Multiphase production systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Shell Bonga multiphase metering"
    ),
    DoctrineBlock(
        topic="Corrosion Under Insulation (CUI) Management",
        keywords=["corrosion under insulation", "CUI", "management", "pipeline integrity", "inspection"],
        conclusion_template="CUI risk is managed by insulation selection, inspection, and maintenance in systems exposed to water ingress and temperature cycling.",
        reasoning_framework="""
        1. Assess CUI risk based on insulation type, environment, and temperature.
        2. Select insulation with water-repellent properties and proper sealing.
        3. Implement regular inspection (e.g., NDT, visual) of insulated areas.
        4. Repair or replace damaged insulation promptly.
        5. Document CUI management strategy and inspection results.
        6. Review and update program as needed.
        """,
        key_factors=[
            "Insulation selection",
            "Environmental exposure",
            "Inspection frequency",
            "Repair and maintenance",
            "Program documentation"
        ],
        primary_authority=[
            "API 583",
            "DNVGL-RP-F103",
            "NACE SP0198"
        ],
        burden_holder="Integrity/maintenance engineer",
        adversary_position="CUI is not a significant risk in this environment.",
        counter_arguments=[
            "CUI can cause rapid, undetected wall loss.",
            "Inspection and maintenance reduce risk.",
            "Industry standards recommend proactive management."
        ],
        resolution_strategy="Inspect and maintain insulation; document and review program.",
        entity_scope="Insulated pipelines and equipment",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="Chevron CUI management"
    ),
    DoctrineBlock(
        topic="Pipeline Pressure Testing and Commissioning",
        keywords=["pressure testing", "commissioning", "pipeline integrity", "hydrotest", "leak test"],
        conclusion_template="Pressure testing and commissioning must follow industry standards to verify pipeline integrity before operation.",
        reasoning_framework="""
        1. Develop pressure test plan in accordance with standards.
        2. Select appropriate test medium (water, nitrogen, etc.).
        3. Monitor pressure, temperature, and leak rates during test.
        4. Document test results and any anomalies.
        5. Address anomalies before commissioning.
        6. Commission pipeline after successful test.
        """,
        key_factors=[
            "Test plan and standards",
            "Test medium selection",
            "Monitoring and documentation",
            "Anomaly resolution",
            "Commissioning procedures"
        ],
        primary_authority=[
            "API 1110",
            "DNVGL-ST-F101",
            "PHMSA 49 CFR 192/195"
        ],
        burden_holder="Pipeline/project engineer",
        adversary_position="Testing is excessive; visual inspection is sufficient.",
        counter_arguments=[
            "Pressure testing verifies integrity.",
            "Industry standards require testing.",
            "Reduces risk of early failure."
        ],
        resolution_strategy="Follow standards; document and resolve anomalies before commissioning.",
        entity_scope="All new and modified pipelines",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="TransCanada pressure testing"
    ),
    DoctrineBlock(
        topic="Pipeline Internal Cleaning Prior to Commissioning",
        keywords=["pipeline cleaning", "commissioning", "debris removal", "internal cleaning", "pre-operation"],
        conclusion_template="Internal cleaning is required prior to commissioning to remove debris, construction residues, and ensure operational reliability.",
        reasoning_framework="""
        1. Develop cleaning plan based on pipeline length, diameter, and construction method.
        2. Select appropriate cleaning pigs and procedures.
        3. Monitor debris removal and pig returns.
        4. Repeat cleaning runs as needed.
        5. Document cleaning results and readiness for commissioning.
        6. Address any anomalies before proceeding.
        """,
        key_factors=[
            "Cleaning plan and procedures",
            "Pig selection",
            "Debris monitoring",
            "Repeat runs as needed",
            "Documentation"
        ],
        primary_authority=[
            "API 1110",
            "DNVGL-ST-F101",
            "SPE 124584"
        ],
        burden_holder="Pipeline/commissioning engineer",
        adversary_position="Cleaning is unnecessary; pipeline is new.",
        counter_arguments=[
            "Construction debris can cause operational issues.",
            "Cleaning improves reliability.",
            "Industry standards require cleaning."
        ],
        resolution_strategy="Clean and document prior to commissioning; resolve anomalies.",
        entity_scope="All new and modified pipelines",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Shell Bonga pipeline cleaning"
    ),
    DoctrineBlock(
        topic="Pipeline Cathodic Protection System Design",
        keywords=["cathodic protection", "pipeline", "corrosion control", "system design", "integrity"],
        conclusion_template="Cathodic protection system must be designed and maintained to protect pipeline from external corrosion in accordance with standards.",
        reasoning_framework="""
        1. Assess external corrosion risk based on environment and coating.
        2. Design cathodic protection system (sacrificial anode or impressed current).
        3. Install and commission system as per standards.
        4. Monitor protection levels regularly.
        5. Maintain and adjust system as needed.
        6. Document design, installation, and monitoring.
        """,
        key_factors=[
            "Corrosion risk assessment",
            "System design and selection",
            "Installation and commissioning",
            "Monitoring and maintenance",
            "Documentation"
        ],
        primary_authority=[
            "NACE SP0169",
            "API RP 14E",
            "DNVGL-RP-F103"
        ],
        burden_holder="Corrosion/integrity engineer",
        adversary_position="Cathodic protection is unnecessary; coating is sufficient.",
        counter_arguments=[
            "Coating defects can expose bare metal.",
            "Cathodic protection provides redundancy.",
            "Industry standards require protection."
        ],
        resolution_strategy="Design, install, and monitor system; maintain as required.",
        entity_scope="Buried and submerged pipelines",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="Transco cathodic protection"
    ),
    DoctrineBlock(
        topic="Pipeline Emergency Shutdown (ESD) System Design",
        keywords=["emergency shutdown", "ESD", "system design", "pipeline safety", "integrity"],
        conclusion_template="Pipeline ESD system must be designed to isolate and depressurize pipeline safely in emergency scenarios.",
        reasoning_framework="""
        1. Identify emergency scenarios requiring shutdown.
        2. Design ESD system to isolate pipeline segments and depressurize safely.
        3. Select and install actuated valves and control systems.
        4. Test and maintain ESD system regularly.
        5. Train personnel on ESD operation and response.
        6. Document design, testing, and training.
        """,
        key_factors=[
            "Emergency scenario identification",
            "System design and selection",
            "Testing and maintenance",
            "Personnel training",
            "Documentation"
        ],
        primary_authority=[
            "API RP 14C",
            "DNVGL-RP-F103",
            "PHMSA 49 CFR 192/195"
        ],
        burden_holder="Pipeline/project engineer",
        adversary_position="ESD system is excessive; manual isolation is sufficient.",
        counter_arguments=[
            "Automated ESD reduces response time.",
            "Industry standards require ESD systems.",
            "Improves safety and integrity."
        ],
        resolution_strategy="Design, install, and maintain ESD system; train personnel.",
        entity_scope="All pipelines",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Shell Bonga ESD design"
    ),
    DoctrineBlock(
        topic="Pipeline Surge Pressure Management",
        keywords=["surge pressure", "pipeline", "pressure management", "water hammer", "integrity"],
        conclusion_template="Surge pressure management is required to prevent pipeline failure due to water hammer or rapid valve closure.",
        reasoning_framework="""
        1. Model surge pressures using validated hydraulic models.
        2. Identify scenarios causing surge (e.g., valve closure, pump trip).
        3. Design surge mitigation (e.g., slow-closing valves, surge tanks, accumulators).
        4. Monitor pressure during operation.
        5. Document surge management strategy and response procedures.
        6. Review and update as needed.
        """,
        key_factors=[
            "Surge scenario identification",
            "Hydraulic modeling",
            "Mitigation design",
            "Pressure monitoring",
            "Documentation and review"
        ],
        primary_authority=[
            "API RP 14E",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Pipeline/process engineer",
        adversary_position="Surge risk is minimal; mitigation is unnecessary.",
        counter_arguments=[
            "Unexpected events can cause damaging surges.",
            "Mitigation reduces risk of failure.",
            "Industry standards recommend surge management."
        ],
        resolution_strategy="Model and mitigate surge scenarios; monitor and review.",
        entity_scope="All pressurized pipelines",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Chevron surge management"
    ),
    DoctrineBlock(
        topic="Pipeline Material Selection for Sour Service",
        keywords=["material selection", "sour service", "H2S", "pipeline", "corrosion"],
        conclusion_template="Material selection for sour service must comply with NACE MR0175/ISO 15156 to prevent sulfide stress cracking and corrosion.",
        reasoning_framework="""
        1. Assess H2S concentration and partial pressure.
        2. Select materials compliant with NACE MR0175/ISO 15156.
        3. Evaluate need for corrosion inhibition or cladding.
        4. Document material selection and qualification.
        5. Monitor for sour service degradation.
        6. Review and update selection as needed.
        """,
        key_factors=[
            "H2S concentration and pressure",
            "Material compliance",
            "Corrosion inhibition",
            "Documentation",
            "Monitoring"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156",
            "API RP 14E",
            "DNVGL-RP-F103"
        ],
        burden_holder="Materials/corrosion engineer",
        adversary_position="Sour service materials are unnecessary; H2S is low.",
        counter_arguments=[
            "Sulfide stress cracking can occur at low H2S.",
            "Industry standards require compliance.",
            "Monitoring supports early detection."
        ],
        resolution_strategy="Select compliant materials; monitor and document.",
        entity_scope="Sour service pipelines and facilities",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Chevron sour service material selection"
    ),
    DoctrineBlock(
        topic="Pipeline Flow Loop Testing for Model Validation",
        keywords=["flow loop testing", "model validation", "pipeline", "flow assurance", "laboratory"],
        conclusion_template="Flow loop testing is required to validate flow assurance models and support design for complex or novel systems.",
        reasoning_framework="""
        1. Identify need for flow loop testing based on system complexity or novelty.
        2. Design test program to replicate field conditions.
        3. Collect and analyze data to validate models.
        4. Adjust models and design based on test results.
        5. Document testing and validation process.
        6. Review and update as needed.
        """,
        key_factors=[
            "System complexity",
            "Test program design",
            "Data analysis",
            "Model adjustment",
            "Documentation"
        ],
        primary_authority=[
            "API 17TR6",
            "DNVGL-RP-F103",
            "SPE 124584"
        ],
        burden_holder="Flow assurance/project engineer",
        adversary_position="Model validation is unnecessary; field data is sufficient.",
        counter_arguments=[
            "Novel systems require validation.",
            "Testing improves model reliability.",
            "Industry standards recommend validation."
        ],
        resolution_strategy="Conduct flow loop testing as needed; document and update models.",
        entity_scope="Complex and novel pipeline systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="BP Thunder Horse flow loop validation"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Threat Assessment and Ranking",
        keywords=["integrity threat", "assessment", "ranking", "pipeline", "risk management"],
        conclusion_template="Integrity threats must be systematically assessed and ranked to prioritize mitigation and inspection activities.",
        reasoning_framework="""
        1. Identify potential integrity threats (corrosion, cracking, mechanical damage, etc.).
        2. Assess likelihood and consequence for each threat.
        3. Rank threats using risk matrix or scoring system.
        4. Prioritize mitigation and inspection based on ranking.
        5. Document assessment and review regularly.
        6. Update ranking as new data becomes available.
        """,
        key_factors=[
            "Threat identification",
            "Likelihood and consequence assessment",
            "Risk ranking",
            "Mitigation prioritization",
            "Documentation and review"
        ],
        primary_authority=[
            "API 1160",
            "PHMS