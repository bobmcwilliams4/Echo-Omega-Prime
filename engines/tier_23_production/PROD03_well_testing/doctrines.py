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
        topic="horner_buildup_analysis",
        keywords=["pressure buildup", "Horner plot", "reservoir pressure", "shut-in", "well testing", "PROD03"],
        conclusion_template="The Horner buildup analysis provides a reliable estimate of reservoir pressure and permeability when the well has been shut-in for sufficient time and boundary effects are negligible.",
        reasoning_framework="""The Horner plot is constructed by plotting shut-in pressure versus the Horner time ratio, allowing for extrapolation to infinite shut-in time. The method assumes radial flow and negligible boundary effects. The slope of the plot yields permeability, while the intercept estimates reservoir pressure. The technique is robust for moderate to long shut-in periods and is sensitive to wellbore storage and skin effects, which must be accounted for. Data quality and proper shut-in duration are critical for accuracy. The method is validated by comparison with other buildup and drawdown analyses, and is widely accepted in industry standards.""",
        key_factors=["shut-in duration", "wellbore storage", "skin effect", "boundary proximity", "data quality"],
        primary_authority=["SPE Petroleum Engineering Handbook", "Horner (1951)", "PROD03_well_testing standards"],
        burden_holder="test analyst",
        adversary_position="Boundary effects or insufficient shut-in may invalidate the Horner plot assumptions.",
        counter_arguments=[
            "Boundary effects can distort the pressure response, leading to erroneous permeability estimates.",
            "Short shut-in periods may not allow the well to reach radial flow.",
            "Wellbore storage can mask early-time data, requiring correction."
        ],
        resolution_strategy="Validate radial flow regime by pressure derivative analysis; extend shut-in duration or use alternative methods if boundary effects are present.",
        entity_scope="conventional reservoirs, vertical wells",
        confidence=0.95,
        confidence_zone="high",
        controlling_precedent="Horner, D.R. (1951), 'Pressure Build-up in Wells.'"
    ),
    DoctrineBlock(
        topic="bourdet_derivative_analysis",
        keywords=["pressure derivative", "Bourdet plot", "diagnostic", "flow regimes", "well testing", "PROD03"],
        conclusion_template="Bourdet derivative analysis is essential for identifying flow regimes and diagnosing well and reservoir behavior during transient tests.",
        reasoning_framework="""The Bourdet derivative is calculated using a logarithmic derivative of pressure with respect to time, plotted alongside the pressure response. This dual-plot approach enables clear identification of flow regimes such as wellbore storage, radial flow, boundary effects, and dual-porosity behavior. The method is particularly effective in distinguishing between overlapping regimes and is less sensitive to noise compared to classical derivatives. It is recommended for both drawdown and buildup tests, and is considered a standard diagnostic tool in well test interpretation. Proper smoothing and sampling are required to avoid artifacts.""",
        key_factors=["data sampling", "noise filtering", "flow regime identification", "test duration", "wellbore storage"],
        primary_authority=["Bourdet et al. (1989)", "SPE Guidelines", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Pressure derivative plots may be distorted by noise or insufficient data resolution.",
        counter_arguments=[
            "High-frequency noise can obscure derivative features.",
            "Insufficient test duration may not reveal all flow regimes.",
            "Improper smoothing can introduce artifacts."
        ],
        resolution_strategy="Apply appropriate smoothing algorithms; ensure adequate test duration; corroborate with other diagnostic tools.",
        entity_scope="all well types, conventional and unconventional",
        confidence=0.92,
        confidence_zone="high",
        controlling_precedent="Bourdet, D., et al. (1989), 'A New Approach to the Analysis of Well Test Data.'"
    ),
    DoctrineBlock(
        topic="skin_factor_determination",
        keywords=["skin", "well damage", "permeability", "well testing", "PROD03", "pressure drop"],
        conclusion_template="Skin factor is determined from well test data using pressure transient analysis, quantifying near-wellbore damage or stimulation.",
        reasoning_framework="""Skin factor is calculated from the deviation of measured pressure response from ideal radial flow, typically using the slope and intercept of a semi-log plot or Horner plot. The value reflects additional pressure drop due to formation damage or stimulation near the wellbore. Accurate determination requires correction for wellbore storage and identification of radial flow regime. The skin factor is essential for evaluating well performance and designing remediation or stimulation treatments. Industry standards recommend cross-validation with other diagnostic methods and consideration of operational history.""",
        key_factors=["radial flow identification", "wellbore storage correction", "pressure response", "operational history"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="well test engineer",
        adversary_position="Misidentification of flow regime or uncorrected wellbore storage may yield inaccurate skin values.",
        counter_arguments=[
            "Early-time data affected by wellbore storage can distort skin calculation.",
            "Boundary effects may mimic skin response.",
            "Operational changes during the test can affect pressure data."
        ],
        resolution_strategy="Use late-time data for skin calculation; apply wellbore storage corrections; cross-check with other tests.",
        entity_scope="all well types",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 5.2.3"
    ),
    DoctrineBlock(
        topic="dual_porosity_interpretation",
        keywords=["dual porosity", "fractured reservoir", "matrix", "transient", "well testing", "PROD03"],
        conclusion_template="Dual-porosity interpretation is required in reservoirs exhibiting both matrix and fracture systems, using characteristic pressure responses and derivative analysis.",
        reasoning_framework="""Dual-porosity systems display unique pressure transient responses, often characterized by a 'double dip' in the pressure derivative plot. The analysis involves fitting the response to dual-porosity models, such as the Warren and Root model, and extracting parameters like interporosity flow coefficient and storativity. Accurate interpretation depends on recognizing the dual-porosity signature and differentiating it from boundary effects or wellbore storage. The method is validated by matching both pressure and derivative curves and is supported by core and log data.""",
        key_factors=["pressure derivative signature", "model fitting", "fracture-matrix interaction", "core/log validation"],
        primary_authority=["Warren & Root (1963)", "SPE Guidelines", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Boundary effects or noise may be misinterpreted as dual-porosity behavior.",
        counter_arguments=[
            "Boundary effects can mimic dual-porosity responses.",
            "High noise levels obscure characteristic signatures.",
            "Single-porosity models may fit data equally well."
        ],
        resolution_strategy="Validate dual-porosity signature with multiple diagnostic tools; corroborate with geological and petrophysical data.",
        entity_scope="fractured reservoirs",
        confidence=0.88,
        confidence_zone="medium-high",
        controlling_precedent="Warren, J.E. & Root, P.J. (1963), 'The Behavior of Naturally Fractured Reservoirs.'"
    ),
    DoctrineBlock(
        topic="boundary_effect_identification",
        keywords=["boundary", "reservoir limits", "pressure response", "well testing", "PROD03"],
        conclusion_template="Boundary effects are identified through deviations from radial flow in pressure and derivative plots, indicating proximity to reservoir limits or faults.",
        reasoning_framework="""Boundary effects manifest as changes in slope or inflection points in pressure and derivative plots, typically at late times during a well test. Identification relies on recognizing deviations from expected radial flow behavior and correlating with known reservoir geometry. The presence of boundaries affects permeability and skin calculations and may necessitate alternative analytical models. Accurate identification is critical for reservoir management and well placement. The method is validated by integrating pressure transient data with geological and seismic information.""",
        key_factors=["pressure plot inflection", "derivative analysis", "reservoir geometry", "test duration"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Short test duration or complex reservoir geometry may obscure boundary effects.",
        counter_arguments=[
            "Insufficient test duration may not reveal boundary effects.",
            "Complex reservoir geometry complicates interpretation.",
            "Multiple boundaries may overlap, masking individual effects."
        ],
        resolution_strategy="Extend test duration; use numerical models; integrate with geological and seismic data.",
        entity_scope="all reservoir types",
        confidence=0.85,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 5.3.2"
    ),
    DoctrineBlock(
        topic="horizontal_well_testing",
        keywords=["horizontal well", "anisotropy", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Horizontal well testing requires specialized interpretation models accounting for well length, anisotropy, and reservoir heterogeneity.",
        reasoning_framework="""Horizontal wells exhibit complex pressure transient responses due to elongated wellbore, anisotropic permeability, and variable reservoir properties. Interpretation involves using models such as the Babu-Odeh or Cinco-Ley horizontal well models, which account for well length, reservoir thickness, and permeability anisotropy. Diagnostic plots and derivative analysis are used to identify flow regimes and estimate parameters. The method is validated by matching model responses to observed data and integrating with geological information. Special attention is required for early-time wellbore storage and late-time boundary effects.""",
        key_factors=["well length", "anisotropy", "reservoir heterogeneity", "model selection"],
        primary_authority=["Babu & Odeh (1989)", "Cinco-Ley (1993)", "PROD03_well_testing standards"],
        burden_holder="test analyst",
        adversary_position="Conventional models may not accurately represent horizontal well behavior.",
        counter_arguments=[
            "Conventional radial flow models are inadequate for horizontal wells.",
            "Complex reservoir heterogeneity may require numerical simulation.",
            "Boundary effects are more pronounced in horizontal wells."
        ],
        resolution_strategy="Use horizontal well-specific models; validate with numerical simulation; integrate geological data.",
        entity_scope="horizontal wells, all reservoir types",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="Babu, D.K. & Odeh, A.S. (1989), 'Pressure Transient Analysis of Horizontal Wells.'"
    ),
    DoctrineBlock(
        topic="rate_transient_analysis_unconventional",
        keywords=["RTA", "unconventional", "shale", "tight gas", "production data", "PROD03"],
        conclusion_template="Rate transient analysis (RTA) is the primary tool for evaluating unconventional reservoirs, using production data to estimate reservoir properties and forecast performance.",
        reasoning_framework="""RTA involves analyzing production rate and pressure data over time to infer reservoir properties such as permeability, fracture conductivity, and drainage area. The method is particularly suited for unconventional reservoirs where traditional well tests are impractical. Models such as linear flow, boundary-dominated flow, and material balance are applied to diagnose flow regimes and estimate parameters. RTA is validated by matching model predictions to observed production trends and integrating with completion and geological data. The technique is sensitive to data quality and requires careful normalization and correction for operational changes.""",
        key_factors=["production data quality", "flow regime identification", "model selection", "operational corrections"],
        primary_authority=["SPE Unconventional Resources Guidelines", "PROD03_well_testing standards"],
        burden_holder="production engineer",
        adversary_position="Short production history or variable operating conditions may limit RTA accuracy.",
        counter_arguments=[
            "Short production history limits parameter estimation.",
            "Variable operating conditions complicate normalization.",
            "Complex fracture networks may require advanced modeling."
        ],
        resolution_strategy="Extend production monitoring; apply normalization and correction techniques; use advanced models as needed.",
        entity_scope="unconventional reservoirs",
        confidence=0.87,
        confidence_zone="medium-high",
        controlling_precedent="SPE UR Guidelines, Section 7.1"
    ),
    DoctrineBlock(
        topic="wellbore_storage_effects",
        keywords=["wellbore storage", "early-time", "pressure response", "correction", "well testing", "PROD03"],
        conclusion_template="Wellbore storage effects dominate early-time pressure responses and must be corrected for accurate interpretation of reservoir properties.",
        reasoning_framework="""Wellbore storage causes a delayed pressure response at early times, masking reservoir behavior. Correction involves identifying the wellbore storage regime using pressure derivative plots and applying analytical or numerical corrections to isolate reservoir response. Accurate estimation of wellbore storage coefficient is essential for proper interpretation. The method is validated by observing transition from wellbore storage to radial flow and comparing corrected data to expected models. Failure to correct for wellbore storage leads to erroneous permeability and skin estimates.""",
        key_factors=["early-time data", "storage coefficient", "pressure derivative", "correction method"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Uncorrected wellbore storage distorts reservoir property estimation.",
        counter_arguments=[
            "Early-time data is dominated by wellbore storage, not reservoir response.",
            "Incorrect storage coefficient leads to faulty corrections.",
            "Complex wellbore geometry complicates storage estimation."
        ],
        resolution_strategy="Use pressure derivative plots to identify storage regime; apply analytical corrections; validate with late-time data.",
        entity_scope="all well types",
        confidence=0.89,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 5.2.4"
    ),
    DoctrineBlock(
        topic="formation_interval_testing",
        keywords=["interval testing", "formation", "DST", "pressure response", "PROD03"],
        conclusion_template="Formation interval testing isolates specific reservoir intervals to evaluate permeability, pressure, and fluid properties using drill stem or cased hole tests.",
        reasoning_framework="""Interval testing involves isolating a section of the reservoir using packers and conducting pressure transient tests. The method provides direct measurement of interval permeability, pressure, and fluid properties, and is essential for reservoir characterization. Drill stem tests (DST) and cased hole tests are commonly used. Interpretation relies on standard transient analysis techniques, with corrections for wellbore storage and skin. The method is validated by comparison with core and log data, and is critical for well completion decisions.""",
        key_factors=["interval isolation", "packer integrity", "pressure response", "fluid sampling"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test operator",
        adversary_position="Poor interval isolation or packer failure may compromise test results.",
        counter_arguments=[
            "Packer leaks or failures invalidate interval isolation.",
            "Fluid contamination affects sample quality.",
            "Short test duration limits parameter estimation."
        ],
        resolution_strategy="Ensure packer integrity; extend test duration; cross-validate with core and log data.",
        entity_scope="all reservoir types",
        confidence=0.91,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 6.1"
    ),
    DoctrineBlock(
        topic="interference_pulse_testing",
        keywords=["interference test", "pulse test", "multi-well", "pressure response", "PROD03"],
        conclusion_template="Interference and pulse testing are used to evaluate reservoir connectivity and transmissibility between wells by analyzing pressure responses to controlled flow changes.",
        reasoning_framework="""Interference tests involve shutting-in or producing one well and monitoring pressure response in another, while pulse tests use periodic flow changes. The methods are effective for assessing reservoir connectivity, transmissibility, and boundaries. Interpretation relies on correlating pressure changes with flow events and applying analytical models. Accurate timing and synchronization are critical. The methods are validated by matching observed responses to predicted models and integrating with geological data. Limitations include low signal-to-noise ratio and operational complexity.""",
        key_factors=["well spacing", "timing accuracy", "pressure monitoring", "reservoir connectivity"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test coordinator",
        adversary_position="Low signal-to-noise ratio or operational errors may invalidate test results.",
        counter_arguments=[
            "Low signal-to-noise ratio obscures pressure response.",
            "Operational errors in timing or synchronization affect data quality.",
            "Complex reservoir geometry complicates interpretation."
        ],
        resolution_strategy="Improve signal-to-noise ratio; ensure accurate timing; use advanced analytical models.",
        entity_scope="multi-well reservoirs",
        confidence=0.86,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 6.2"
    ),
    DoctrineBlock(
        topic="drill_stem_test_interpretation",
        keywords=["DST", "drill stem test", "pressure transient", "fluid sampling", "PROD03"],
        conclusion_template="Drill stem test interpretation provides critical information on reservoir properties and fluid characteristics, guiding completion and production decisions.",
        reasoning_framework="""DSTs involve temporarily isolating a reservoir interval and flowing the well to surface, followed by shut-in periods. Interpretation uses pressure transient analysis to estimate permeability, reservoir pressure, and skin, and fluid sampling to assess hydrocarbon quality. DSTs are subject to operational risks such as packer failure and fluid contamination. The method is validated by comparison with core, log, and production data. DST results are essential for well completion and reservoir management decisions.""",
        key_factors=["interval isolation", "pressure response", "fluid sampling", "operational risks"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test operator",
        adversary_position="Operational failures or contamination may compromise DST results.",
        counter_arguments=[
            "Packer leaks invalidate pressure response.",
            "Fluid contamination affects sample quality.",
            "Short test duration limits parameter estimation."
        ],
        resolution_strategy="Ensure operational integrity; extend test duration; cross-validate with other data sources.",
        entity_scope="all reservoir types",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 6.3"
    ),
    DoctrineBlock(
        topic="type_curve_matching_methodology",
        keywords=["type curve", "model matching", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Type curve matching is a fundamental methodology for interpreting well test data, enabling estimation of reservoir properties by fitting observed responses to theoretical models.",
        reasoning_framework="""Type curve matching involves overlaying observed pressure and derivative data onto theoretical model curves, such as radial flow, dual-porosity, or boundary-affected models. The process enables estimation of permeability, skin, and other parameters by identifying the best fit. Accurate matching requires high-quality data and proper identification of flow regimes. The method is validated by matching both pressure and derivative responses and integrating with geological and petrophysical information. Limitations include subjectivity in curve selection and sensitivity to noise.""",
        key_factors=["model selection", "data quality", "flow regime identification", "matching accuracy"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Subjectivity in curve selection or noisy data may compromise matching accuracy.",
        counter_arguments=[
            "Subjective curve selection leads to inconsistent results.",
            "Noisy data obscures model fit.",
            "Multiple models may fit data equally well."
        ],
        resolution_strategy="Use objective matching criteria; apply noise filtering; corroborate with geological data.",
        entity_scope="all well types",
        confidence=0.89,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 5.4"
    ),
    DoctrineBlock(
        topic="superposition_principles",
        keywords=["superposition", "multiple tests", "pressure transient", "analytical modeling", "PROD03"],
        conclusion_template="Superposition principles enable interpretation of complex well tests involving multiple flow periods by combining individual responses analytically.",
        reasoning_framework="""Superposition is used to analyze well tests with multiple flow and shut-in periods, by summing individual pressure responses according to superposition rules. The principle is essential for interpreting tests with variable rates, multi-rate, or interference scenarios. Analytical models are adapted to account for superposed effects, enabling accurate estimation of reservoir properties. The method is validated by matching composite responses to observed data and is supported by industry standards. Limitations include complexity in modeling and sensitivity to operational changes.""",
        key_factors=["flow period identification", "analytical modeling", "rate changes", "composite response"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test analyst",
        adversary_position="Incorrect application of superposition may lead to erroneous interpretation.",
        counter_arguments=[
            "Misidentification of flow periods distorts composite response.",
            "Operational changes complicate superposition modeling.",
            "Analytical models may not capture all effects."
        ],
        resolution_strategy="Carefully identify flow periods; use validated analytical models; cross-check with observed data.",
        entity_scope="all well types",
        confidence=0.88,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 5.5"
    ),
    DoctrineBlock(
        topic="multi_rate_testing",
        keywords=["multi-rate", "variable rate", "pressure response", "superposition", "well testing", "PROD03"],
        conclusion_template="Multi-rate testing provides enhanced diagnostic capability by varying flow rates and applying superposition principles to interpret composite pressure responses.",
        reasoning_framework="""Multi-rate tests involve changing flow rates during a well test and analyzing the resulting composite pressure response. Interpretation uses superposition principles to separate individual rate effects and estimate reservoir properties. The method is particularly useful for identifying non-linear effects, skin, and wellbore storage. Accurate timing and rate measurement are critical. The technique is validated by matching analytical models to observed data and integrating with other diagnostic tools. Limitations include operational complexity and sensitivity to rate measurement errors.""",
        key_factors=["rate measurement", "timing accuracy", "superposition modeling", "diagnostic capability"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test operator",
        adversary_position="Rate measurement errors or timing inaccuracies may compromise interpretation.",
        counter_arguments=[
            "Inaccurate rate measurement distorts pressure response.",
            "Timing errors affect superposition modeling.",
            "Operational complexity increases risk of errors."
        ],
        resolution_strategy="Ensure accurate rate and timing measurement; use validated models; cross-check with other tests.",
        entity_scope="all well types",
        confidence=0.87,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 5.6"
    ),
    DoctrineBlock(
        topic="permeability_estimation_methods",
        keywords=["permeability", "estimation", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Permeability estimation from well test data relies on transient analysis, model fitting, and correction for wellbore storage and skin effects.",
        reasoning_framework="""Permeability is estimated from the slope of pressure transient plots, such as semi-log or Horner plots, and by fitting analytical models to observed data. Corrections for wellbore storage and skin are essential for accuracy. The method is validated by comparison with core and log data and is critical for reservoir characterization and production forecasting. Limitations include sensitivity to data quality and flow regime identification.""",
        key_factors=["plot slope", "model fitting", "wellbore storage correction", "skin correction"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Uncorrected storage or skin effects may yield inaccurate permeability estimates.",
        counter_arguments=[
            "Early-time data affected by wellbore storage distorts slope.",
            "Skin effects must be properly identified and corrected.",
            "Noisy data reduces estimation accuracy."
        ],
        resolution_strategy="Use late-time data; apply corrections; cross-validate with core and log data.",
        entity_scope="all well types",
        confidence=0.92,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 5.7"
    ),
    DoctrineBlock(
        topic="pressure_derivative_diagnostic_features",
        keywords=["pressure derivative", "diagnostic", "flow regime", "well testing", "PROD03"],
        conclusion_template="Pressure derivative plots reveal diagnostic features essential for identifying flow regimes, boundaries, and reservoir heterogeneity.",
        reasoning_framework="""Pressure derivative plots are constructed by calculating the logarithmic derivative of pressure with respect to time. Features such as flat regions, dips, and inflection points correspond to specific flow regimes, including wellbore storage, radial flow, dual-porosity, and boundary effects. Accurate identification of these features is critical for proper interpretation. The method is validated by matching observed features to theoretical models and integrating with geological information. Limitations include sensitivity to noise and data sampling.""",
        key_factors=["feature identification", "model matching", "noise filtering", "sampling rate"],
        primary_authority=["Bourdet et al. (1989)", "SPE Guidelines", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Noisy data or improper sampling may obscure diagnostic features.",
        counter_arguments=[
            "High-frequency noise masks diagnostic features.",
            "Improper sampling rate introduces artifacts.",
            "Complex reservoir geometry complicates interpretation."
        ],
        resolution_strategy="Apply noise filtering; optimize sampling rate; corroborate with geological data.",
        entity_scope="all well types",
        confidence=0.91,
        confidence_zone="high",
        controlling_precedent="Bourdet, D., et al. (1989)"
    ),
    DoctrineBlock(
        topic="test_design_and_duration",
        keywords=["test design", "duration", "well testing", "pressure transient", "PROD03"],
        conclusion_template="Proper test design and duration are critical for obtaining reliable well test data and accurate interpretation of reservoir properties.",
        reasoning_framework="""Test design involves selecting flow rates, shut-in periods, and monitoring intervals to ensure all relevant flow regimes are captured. Adequate duration is required to observe late-time effects such as boundaries and dual-porosity behavior. The method is validated by ensuring diagnostic features are present in pressure and derivative plots and by comparison with model predictions. Limitations include operational constraints and cost considerations.""",
        key_factors=["flow rate selection", "shut-in period", "monitoring interval", "operational constraints"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test designer",
        adversary_position="Short test duration or poor design may fail to capture critical flow regimes.",
        counter_arguments=[
            "Short test duration limits observation of late-time effects.",
            "Poor design may miss key diagnostic features.",
            "Operational constraints restrict test options."
        ],
        resolution_strategy="Optimize test design for target objectives; extend duration as needed; balance operational constraints.",
        entity_scope="all well types",
        confidence=0.93,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 7.1"
    ),
    DoctrineBlock(
        topic="pressure_transient_analysis",
        keywords=["pressure transient", "analysis", "well testing", "PROD03"],
        conclusion_template="Pressure transient analysis is the foundation of well testing, enabling estimation of reservoir properties through interpretation of pressure and flow data.",
        reasoning_framework="""Pressure transient analysis involves recording pressure and flow rate data during well tests and interpreting the response using analytical or numerical models. The technique enables estimation of permeability, skin, boundary effects, and reservoir heterogeneity. Proper identification of flow regimes and correction for wellbore storage are essential. The method is validated by matching observed responses to model predictions and integrating with geological and petrophysical data. Limitations include sensitivity to data quality and operational changes.""",
        key_factors=["data quality", "model selection", "flow regime identification", "correction methods"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Poor data quality or incorrect model selection may compromise analysis.",
        counter_arguments=[
            "Noisy or incomplete data reduces accuracy.",
            "Incorrect model selection leads to erroneous interpretation.",
            "Operational changes affect pressure response."
        ],
        resolution_strategy="Ensure high-quality data; use validated models; cross-check with geological information.",
        entity_scope="all well types",
        confidence=0.94,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 5.1"
    ),
    DoctrineBlock(
        topic="drawdown_test_interpretation",
        keywords=["drawdown", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Drawdown test interpretation provides early-time reservoir properties and is essential for evaluating well productivity and formation damage.",
        reasoning_framework="""Drawdown tests involve flowing the well at a constant rate and recording pressure decline. Interpretation uses semi-log or derivative plots to estimate permeability, skin, and identify flow regimes. Early-time data is affected by wellbore storage, requiring correction. The method is validated by matching observed responses to analytical models and integrating with production and geological data. Limitations include sensitivity to wellbore storage and operational changes during the test.""",
        key_factors=["flow rate stability", "wellbore storage correction", "model matching", "data quality"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Wellbore storage or unstable flow rates may compromise interpretation.",
        counter_arguments=[
            "Early-time data dominated by wellbore storage.",
            "Unstable flow rates affect pressure response.",
            "Short test duration limits parameter estimation."
        ],
        resolution_strategy="Correct for wellbore storage; ensure stable flow rates; extend test duration as needed.",
        entity_scope="all well types",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 5.2"
    ),
    DoctrineBlock(
        topic="late_time_boundary_analysis",
        keywords=["late-time", "boundary", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Late-time boundary analysis identifies reservoir limits and faults by observing deviations in pressure and derivative plots at extended test durations.",
        reasoning_framework="""Late-time analysis focuses on pressure and derivative responses after extended flow or shut-in periods. Deviations from radial flow, such as slope changes or inflection points, indicate proximity to boundaries or faults. Accurate identification requires long test duration and integration with geological and seismic data. The method is validated by matching observed features to boundary-affected models and corroborating with reservoir mapping. Limitations include operational constraints and complex reservoir geometry.""",
        key_factors=["test duration", "pressure plot features", "geological integration", "boundary modeling"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Short test duration or complex geometry may obscure boundary effects.",
        counter_arguments=[
            "Insufficient duration fails to reveal boundary effects.",
            "Complex geometry complicates interpretation.",
            "Multiple boundaries may overlap."
        ],
        resolution_strategy="Extend test duration; use numerical models; integrate with geological and seismic data.",
        entity_scope="all reservoir types",
        confidence=0.88,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 5.3"
    ),
    DoctrineBlock(
        topic="well_test_data_quality_assurance",
        keywords=["data quality", "assurance", "well testing", "PROD03"],
        conclusion_template="Quality assurance of well test data is essential for reliable interpretation and involves rigorous validation, calibration, and error correction procedures.",
        reasoning_framework="""Data quality assurance includes calibration of pressure gauges, validation of flow rate measurements, and correction for operational errors. Rigorous procedures are followed to ensure data integrity, including redundancy checks, noise filtering, and cross-validation with other data sources. The method is validated by comparing test data to expected physical responses and integrating with geological and production information. Limitations include equipment failure and operational variability.""",
        key_factors=["gauge calibration", "flow rate validation", "error correction", "redundancy checks"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test operator",
        adversary_position="Equipment failure or operational errors may compromise data quality.",
        counter_arguments=[
            "Pressure gauge drift affects accuracy.",
            "Flow rate measurement errors distort interpretation.",
            "Operational variability introduces uncertainty."
        ],
        resolution_strategy="Regular calibration; redundancy in measurements; rigorous error correction procedures.",
        entity_scope="all well types",
        confidence=0.93,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 8.1"
    ),
    DoctrineBlock(
        topic="reservoir_heterogeneity_effects",
        keywords=["heterogeneity", "reservoir", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Reservoir heterogeneity significantly affects pressure transient responses and must be accounted for in interpretation using advanced models and integration with geological data.",
        reasoning_framework="""Heterogeneous reservoirs display complex pressure and derivative responses, often deviating from idealized models. Interpretation requires advanced analytical or numerical models that account for variable permeability, porosity, and fracture networks. Integration with geological, core, and log data is essential for accurate characterization. The method is validated by matching observed responses to heterogeneous models and corroborating with reservoir mapping. Limitations include increased complexity and sensitivity to data quality.""",
        key_factors=["model complexity", "geological integration", "data quality", "fracture networks"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Simplified models may fail to capture heterogeneity effects.",
        counter_arguments=[
            "Idealized models do not represent heterogeneous reservoirs.",
            "Complex fracture networks require advanced modeling.",
            "Noisy data reduces interpretation accuracy."
        ],
        resolution_strategy="Use advanced models; integrate geological data; apply noise filtering.",
        entity_scope="heterogeneous reservoirs",
        confidence=0.86,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.1"
    ),
    DoctrineBlock(
        topic="numerical_modeling_in_well_testing",
        keywords=["numerical modeling", "simulation", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Numerical modeling is essential for interpreting complex well test scenarios, enabling simulation of heterogeneous, multi-phase, and boundary-affected reservoirs.",
        reasoning_framework="""Numerical models simulate pressure and flow responses in complex reservoir scenarios, including heterogeneity, multi-phase flow, and boundary effects. The technique enables accurate interpretation when analytical models are insufficient. Validation involves matching simulated responses to observed data and integrating with geological information. Limitations include computational complexity and sensitivity to input parameters.""",
        key_factors=["model selection", "input parameter accuracy", "validation", "computational complexity"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Incorrect input parameters or model selection may compromise simulation accuracy.",
        counter_arguments=[
            "Inaccurate input parameters distort simulation results.",
            "Complex models require extensive validation.",
            "Computational limitations restrict model complexity."
        ],
        resolution_strategy="Careful parameter selection; rigorous validation; use high-performance computing as needed.",
        entity_scope="complex reservoirs",
        confidence=0.85,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.2"
    ),
    DoctrineBlock(
        topic="fluid_property_estimation",
        keywords=["fluid properties", "estimation", "well testing", "PROD03"],
        conclusion_template="Fluid property estimation during well testing involves sampling and laboratory analysis to determine viscosity, density, and composition, essential for reservoir evaluation.",
        reasoning_framework="""Fluid properties are estimated by collecting samples during well tests and conducting laboratory analyses. Parameters such as viscosity, density, and composition are critical for reservoir evaluation and production forecasting. The method is validated by comparing laboratory results to expected values and integrating with production and geological data. Limitations include sample contamination and operational variability.""",
        key_factors=["sampling quality", "laboratory analysis", "contamination control", "integration with production data"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test operator",
        adversary_position="Sample contamination or operational errors may compromise fluid property estimation.",
        counter_arguments=[
            "Contaminated samples yield inaccurate results.",
            "Operational variability affects sample quality.",
            "Laboratory errors introduce uncertainty."
        ],
        resolution_strategy="Ensure contamination control; rigorous laboratory procedures; cross-validate with production data.",
        entity_scope="all well types",
        confidence=0.92,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 10.1"
    ),
    DoctrineBlock(
        topic="pressure_gauge_selection_and_calibration",
        keywords=["pressure gauge", "selection", "calibration", "well testing", "PROD03"],
        conclusion_template="Proper selection and calibration of pressure gauges are critical for accurate well test data acquisition and interpretation.",
        reasoning_framework="""Pressure gauges must be selected based on expected pressure range, resolution, and environmental conditions. Calibration is performed before and after tests to ensure accuracy. Redundancy in gauge placement is recommended to mitigate equipment failure. The method is validated by comparing gauge readings to reference standards and integrating with other data sources. Limitations include equipment drift and operational variability.""",
        key_factors=["gauge selection", "calibration procedures", "redundancy", "environmental conditions"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test operator",
        adversary_position="Improper gauge selection or calibration may compromise data quality.",
        counter_arguments=[
            "Gauge drift affects accuracy.",
            "Incorrect selection leads to inadequate resolution.",
            "Operational variability introduces uncertainty."
        ],
        resolution_strategy="Follow rigorous selection and calibration procedures; use redundant gauges; cross-validate readings.",
        entity_scope="all well types",
        confidence=0.93,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 8.2"
    ),
    DoctrineBlock(
        topic="shut_in_period_optimization",
        keywords=["shut-in period", "optimization", "well testing", "pressure transient", "PROD03"],
        conclusion_template="Optimization of shut-in period is essential for capturing late-time effects and ensuring reliable estimation of reservoir properties during buildup tests.",
        reasoning_framework="""Shut-in period must be long enough to observe late-time effects such as boundaries and dual-porosity behavior. Optimization involves balancing operational constraints with test objectives. The method is validated by ensuring diagnostic features are present in pressure and derivative plots. Limitations include operational constraints and cost considerations.""",
        key_factors=["test objectives", "operational constraints", "diagnostic feature presence", "cost"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test designer",
        adversary_position="Short shut-in period may fail to capture critical late-time effects.",
        counter_arguments=[
            "Insufficient shut-in period limits observation of boundaries.",
            "Operational constraints restrict shut-in duration.",
            "Cost considerations may reduce test quality."
        ],
        resolution_strategy="Optimize shut-in period for target objectives; balance operational constraints and cost.",
        entity_scope="all well types",
        confidence=0.92,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 7.2"
    ),
    DoctrineBlock(
        topic="flow_regime_identification",
        keywords=["flow regime", "identification", "pressure transient", "well testing", "PROD03"],
        conclusion_template="Accurate identification of flow regimes is essential for reliable interpretation of well test data and estimation of reservoir properties.",
        reasoning_framework="""Flow regimes such as wellbore storage, radial flow, boundary-affected flow, and dual-porosity are identified using pressure and derivative plots. Proper identification enables selection of appropriate analytical models and accurate parameter estimation. The method is validated by matching observed features to theoretical models and integrating with geological data. Limitations include sensitivity to noise and data sampling.""",
        key_factors=["plot features", "model matching", "noise filtering", "sampling rate"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Noisy data or improper sampling may obscure flow regime identification.",
        counter_arguments=[
            "High-frequency noise masks flow regime features.",
            "Improper sampling rate introduces artifacts.",
            "Complex reservoir geometry complicates identification."
        ],
        resolution_strategy="Apply noise filtering; optimize sampling rate; corroborate with geological data.",
        entity_scope="all well types",
        confidence=0.91,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 5.8"
    ),
    DoctrineBlock(
        topic="wellbore_damage_remediation",
        keywords=["wellbore damage", "remediation", "skin", "well testing", "PROD03"],
        conclusion_template="Remediation of wellbore damage is guided by skin factor analysis and involves stimulation or cleaning treatments to restore well productivity.",
        reasoning_framework="""Wellbore damage is quantified by the skin factor, estimated from pressure transient analysis. Remediation involves treatments such as acidizing, hydraulic fracturing, or mechanical cleaning. Effectiveness is validated by post-treatment well tests showing reduced skin and improved productivity. Limitations include operational risks and variable treatment effectiveness.""",
        key_factors=["skin factor", "treatment selection", "post-treatment validation", "operational risks"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="production engineer",
        adversary_position="Remediation treatments may not fully restore productivity or may introduce new damage.",
        counter_arguments=[
            "Treatment effectiveness varies by reservoir type.",
            "Operational risks may cause further damage.",
            "Post-treatment tests may not show expected improvement."
        ],
        resolution_strategy="Select appropriate treatment; validate effectiveness with post-treatment tests; monitor for new damage.",
        entity_scope="all well types",
        confidence=0.89,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 11.1"
    ),
    DoctrineBlock(
        topic="hydraulic_fracture_effects_on_well_testing",
        keywords=["hydraulic fracture", "effects", "well testing", "pressure transient", "PROD03"],
        conclusion_template="Hydraulic fracture effects are identified in well test data by characteristic pressure and derivative responses, requiring specialized models for interpretation.",
        reasoning_framework="""Hydraulic fractures alter pressure transient responses, often displaying early-time linear flow and late-time boundary effects. Interpretation uses specialized models such as the Cinco-Ley fracture model. Diagnostic plots reveal fracture length, conductivity, and orientation. The method is validated by matching observed responses to fracture models and integrating with completion and geological data. Limitations include sensitivity to fracture complexity and data quality.""",
        key_factors=["fracture model selection", "diagnostic plot features", "completion data integration", "data quality"],
        primary_authority=["Cinco-Ley (1978)", "SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="completion engineer",
        adversary_position="Complex fracture networks or poor data quality may obscure fracture effects.",
        counter_arguments=[
            "Complex fracture networks require advanced modeling.",
            "Noisy data reduces interpretation accuracy.",
            "Completion data may be incomplete."
        ],
        resolution_strategy="Use advanced fracture models; integrate completion and geological data; apply noise filtering.",
        entity_scope="fractured wells",
        confidence=0.88,
        confidence_zone="medium-high",
        controlling_precedent="Cinco-Ley, H. (1978), 'Well Test Analysis for Fractured Wells.'"
    ),
    DoctrineBlock(
        topic="material_balance_application_in_well_testing",
        keywords=["material balance", "application", "well testing", "reservoir evaluation", "PROD03"],
        conclusion_template="Material balance is applied in well testing to estimate original hydrocarbons in place and evaluate reservoir depletion using pressure and production data.",
        reasoning_framework="""Material balance involves integrating pressure and production data to estimate original hydrocarbons in place and monitor reservoir depletion. The method is validated by matching material balance calculations to observed production trends and integrating with geological and petrophysical data. Limitations include sensitivity to data quality and reservoir complexity.""",
        key_factors=["pressure data", "production data", "geological integration", "reservoir complexity"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Poor data quality or complex reservoir geometry may compromise material balance accuracy.",
        counter_arguments=[
            "Noisy or incomplete data reduces accuracy.",
            "Complex geometry complicates calculations.",
            "Operational changes affect material balance."
        ],
        resolution_strategy="Ensure high-quality data; integrate geological information; use advanced models as needed.",
        entity_scope="all reservoir types",
        confidence=0.92,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 12.1"
    ),
    DoctrineBlock(
        topic="reservoir_pressure_estimation",
        keywords=["reservoir pressure", "estimation", "well testing", "PROD03"],
        conclusion_template="Reservoir pressure is estimated from well test data using buildup or drawdown analysis, providing critical information for reservoir management.",
        reasoning_framework="""Reservoir pressure is estimated by extrapolating pressure response during buildup or drawdown tests to infinite shut-in or flow time. The method is validated by matching analytical models to observed data and integrating with production and geological information. Limitations include sensitivity to boundary effects and operational changes.""",
        key_factors=["extrapolation accuracy", "model selection", "boundary effects", "operational changes"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Boundary effects or operational changes may compromise pressure estimation.",
        counter_arguments=[
            "Boundary effects distort extrapolation.",
            "Operational changes affect pressure response.",
            "Noisy data reduces accuracy."
        ],
        resolution_strategy="Validate boundary effects; use late-time data; integrate with geological information.",
        entity_scope="all well types",
        confidence=0.93,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 5.9"
    ),
    DoctrineBlock(
        topic="reservoir_connectivity_evaluation",
        keywords=["reservoir connectivity", "evaluation", "interference test", "well testing", "PROD03"],
        conclusion_template="Reservoir connectivity is evaluated using interference and pulse tests, providing critical information for reservoir management and development planning.",
        reasoning_framework="""Connectivity is assessed by monitoring pressure response in observation wells during interference or pulse tests. The method is validated by matching observed responses to analytical models and integrating with geological and seismic data. Limitations include low signal-to-noise ratio and operational complexity.""",
        key_factors=["pressure monitoring", "test synchronization", "model matching", "geological integration"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test coordinator",
        adversary_position="Low signal-to-noise ratio or operational errors may compromise connectivity evaluation.",
        counter_arguments=[
            "Low signal-to-noise ratio obscures pressure response.",
            "Operational errors affect data quality.",
            "Complex reservoir geometry complicates interpretation."
        ],
        resolution_strategy="Improve signal-to-noise ratio; ensure accurate synchronization; integrate geological and seismic data.",
        entity_scope="multi-well reservoirs",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 6.4"
    ),
    DoctrineBlock(
        topic="advanced_noise_filtering_in_well_test_data",
        keywords=["noise filtering", "advanced", "well test data", "pressure transient", "PROD03"],
        conclusion_template="Advanced noise filtering techniques are essential for improving well test data quality and enabling reliable interpretation of pressure transient responses.",
        reasoning_framework="""Noise filtering involves applying advanced algorithms such as wavelet transforms, Kalman filtering, or adaptive smoothing to well test data. The technique improves data quality and enables accurate identification of diagnostic features. Validation is performed by comparing filtered data to expected physical responses and integrating with geological information. Limitations include potential loss of signal and sensitivity to filter parameters.""",
        key_factors=["algorithm selection", "parameter tuning", "validation", "signal preservation"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test analyst",
        adversary_position="Improper filtering may remove critical signal or introduce artifacts.",
        counter_arguments=[
            "Over-filtering removes diagnostic features.",
            "Incorrect parameter tuning introduces artifacts.",
            "Complex reservoir geometry complicates validation."
        ],
        resolution_strategy="Careful algorithm selection; optimize parameters; validate with geological data.",
        entity_scope="all well types",
        confidence=0.91,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 8.3"
    ),
    DoctrineBlock(
        topic="well_test_interpretation_in_tight_gas_reservoirs",
        keywords=["tight gas", "well test interpretation", "pressure transient", "PROD03"],
        conclusion_template="Well test interpretation in tight gas reservoirs requires specialized models and extended test duration to capture low-permeability effects and boundary responses.",
        reasoning_framework="""Tight gas reservoirs display slow pressure responses and extended wellbore storage effects. Interpretation uses specialized models such as linear flow and boundary-dominated flow, and requires long test duration. The method is validated by matching observed responses to tight gas models and integrating with production and geological data. Limitations include sensitivity to data quality and operational constraints.""",
        key_factors=["model selection", "test duration", "data quality", "boundary effects"],
        primary_authority=["SPE Unconventional Resources Guidelines", "PROD03_well_testing standards"],
        burden_holder="test interpreter",
        adversary_position="Short test duration or conventional models may compromise interpretation in tight gas reservoirs.",
        counter_arguments=[
            "Short test duration fails to capture low-permeability effects.",
            "Conventional models are inadequate for tight gas.",
            "Noisy data reduces accuracy."
        ],
        resolution_strategy="Extend test duration; use specialized models; apply noise filtering.",
        entity_scope="tight gas reservoirs",
        confidence=0.89,
        confidence_zone="medium-high",
        controlling_precedent="SPE UR Guidelines, Section 7.2"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_multiphase_reservoirs",
        keywords=["multiphase", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in multiphase reservoirs requires advanced models to account for fluid interactions and phase changes, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Multiphase reservoirs display complex pressure responses due to fluid interactions and phase changes. Interpretation uses advanced analytical or numerical models that account for multiphase flow. The method is validated by matching observed responses to multiphase models and integrating with production and geological data. Limitations include increased complexity and sensitivity to input parameters.""",
        key_factors=["model complexity", "input parameter accuracy", "validation", "fluid interactions"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Simplified models may fail to capture multiphase effects.",
        counter_arguments=[
            "Idealized models do not represent multiphase reservoirs.",
            "Complex fluid interactions require advanced modeling.",
            "Noisy data reduces interpretation accuracy."
        ],
        resolution_strategy="Use advanced models; integrate production and geological data; apply noise filtering.",
        entity_scope="multiphase reservoirs",
        confidence=0.87,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.3"
    ),
    DoctrineBlock(
        topic="well_test_design_for_unconventional_reservoirs",
        keywords=["well test design", "unconventional", "reservoirs", "pressure transient", "PROD03"],
        conclusion_template="Well test design for unconventional reservoirs requires extended duration, specialized models, and integration with production data to capture low-permeability and fracture effects.",
        reasoning_framework="""Unconventional reservoirs display slow pressure responses and complex fracture networks. Test design involves extended duration, specialized models such as linear flow, and integration with production and completion data. The method is validated by matching observed responses to unconventional models and corroborating with production trends. Limitations include operational constraints and sensitivity to data quality.""",
        key_factors=["test duration", "model selection", "production data integration", "fracture effects"],
        primary_authority=["SPE Unconventional Resources Guidelines", "PROD03_well_testing standards"],
        burden_holder="test designer",
        adversary_position="Short test duration or conventional models may compromise test design in unconventional reservoirs.",
        counter_arguments=[
            "Short test duration fails to capture low-permeability effects.",
            "Conventional models are inadequate for unconventional reservoirs.",
            "Noisy data reduces accuracy."
        ],
        resolution_strategy="Extend test duration; use specialized models; integrate production data.",
        entity_scope="unconventional reservoirs",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="SPE UR Guidelines, Section 7.3"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_high_pressure_high_temperature_reservoirs",
        keywords=["HPHT", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in HPHT reservoirs requires specialized equipment and procedures to ensure data quality and safety during interpretation.",
        reasoning_framework="""HPHT reservoirs require pressure gauges and equipment rated for high pressure and temperature. Calibration and validation procedures are critical for data quality. Interpretation uses standard transient analysis techniques, with adjustments for HPHT conditions. The method is validated by matching observed responses to analytical models and integrating with production and geological data. Limitations include equipment failure and operational risks.""",
        key_factors=["equipment selection", "calibration", "validation", "operational risks"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="test operator",
        adversary_position="Equipment failure or operational errors may compromise testing in HPHT reservoirs.",
        counter_arguments=[
            "Equipment rated for HPHT is required.",
            "Calibration procedures must be rigorous.",
            "Operational risks are elevated."
        ],
        resolution_strategy="Use specialized equipment; follow rigorous calibration and validation procedures; monitor operational risks.",
        entity_scope="HPHT reservoirs",
        confidence=0.92,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 8.4"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_water_drive_reservoirs",
        keywords=["water drive", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in water drive reservoirs requires models that account for aquifer support and fluid movement, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Water drive reservoirs display pressure responses affected by aquifer support and fluid movement. Interpretation uses models that account for water influx and boundary effects. The method is validated by matching observed responses to water drive models and integrating with production and geological data. Limitations include sensitivity to aquifer properties and operational changes.""",
        key_factors=["aquifer properties", "model selection", "production data integration", "boundary effects"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Simplified models may fail to capture water drive effects.",
        counter_arguments=[
            "Idealized models do not represent water drive reservoirs.",
            "Complex aquifer properties require advanced modeling.",
            "Noisy data reduces interpretation accuracy."
        ],
        resolution_strategy="Use advanced models; integrate production and geological data; apply noise filtering.",
        entity_scope="water drive reservoirs",
        confidence=0.89,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.4"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_gas_condensate_reservoirs",
        keywords=["gas condensate", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in gas condensate reservoirs requires models that account for phase changes and fluid interactions, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Gas condensate reservoirs display pressure responses affected by phase changes and fluid interactions. Interpretation uses models that account for condensate dropout and multiphase flow. The method is validated by matching observed responses to gas condensate models and integrating with production and geological data. Limitations include sensitivity to phase behavior and operational changes.""",
        key_factors=["phase behavior", "model selection", "production data integration", "fluid interactions"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Simplified models may fail to capture gas condensate effects.",
        counter_arguments=[
            "Idealized models do not represent gas condensate reservoirs.",
            "Complex phase behavior requires advanced modeling.",
            "Noisy data reduces interpretation accuracy."
        ],
        resolution_strategy="Use advanced models; integrate production and geological data; apply noise filtering.",
        entity_scope="gas condensate reservoirs",
        confidence=0.88,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.5"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_oil_reservoirs",
        keywords=["oil reservoir", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in oil reservoirs uses standard models to estimate permeability, skin, and boundary effects, enabling accurate reservoir evaluation.",
        reasoning_framework="""Oil reservoirs display pressure responses that are interpreted using standard analytical models such as radial flow and boundary-affected flow. The method is validated by matching observed responses to oil reservoir models and integrating with production and geological data. Limitations include sensitivity to boundary effects and operational changes.""",
        key_factors=["model selection", "boundary effects", "production data integration", "operational changes"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Boundary effects or operational changes may compromise interpretation in oil reservoirs.",
        counter_arguments=[
            "Boundary effects distort model fit.",
            "Operational changes affect pressure response.",
            "Noisy data reduces accuracy."
        ],
        resolution_strategy="Validate boundary effects; use late-time data; integrate with production and geological information.",
        entity_scope="oil reservoirs",
        confidence=0.92,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 9.6"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_naturally_fractured_reservoirs",
        keywords=["naturally fractured", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in naturally fractured reservoirs requires dual-porosity models and integration with geological data to capture fracture-matrix interactions.",
        reasoning_framework="""Naturally fractured reservoirs display pressure responses characterized by dual-porosity behavior. Interpretation uses models such as Warren and Root and integrates with geological and core data. The method is validated by matching observed responses to dual-porosity models and corroborating with reservoir mapping. Limitations include sensitivity to fracture complexity and data quality.""",
        key_factors=["dual-porosity model", "fracture complexity", "geological integration", "data quality"],
        primary_authority=["Warren & Root (1963)", "SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Complex fracture networks or poor data quality may obscure dual-porosity effects.",
        counter_arguments=[
            "Complex fracture networks require advanced modeling.",
            "Noisy data reduces interpretation accuracy.",
            "Geological data may be incomplete."
        ],
        resolution_strategy="Use advanced dual-porosity models; integrate geological and core data; apply noise filtering.",
        entity_scope="naturally fractured reservoirs",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="Warren, J.E. & Root, P.J. (1963)"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_compartmentalized_reservoirs",
        keywords=["compartmentalized", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in compartmentalized reservoirs requires models that account for multiple boundaries and restricted flow, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Compartmentalized reservoirs display pressure responses affected by multiple boundaries and restricted flow. Interpretation uses models that account for compartmentalization and integrates with geological and seismic data. The method is validated by matching observed responses to compartmentalized models and corroborating with reservoir mapping. Limitations include sensitivity to boundary identification and data quality.""",
        key_factors=["boundary identification", "model selection", "geological integration", "data quality"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Multiple boundaries or poor data quality may compromise interpretation in compartmentalized reservoirs.",
        counter_arguments=[
            "Multiple boundaries complicate model selection.",
            "Noisy data reduces interpretation accuracy.",
            "Geological data may be incomplete."
        ],
        resolution_strategy="Use advanced compartmentalization models; integrate geological and seismic data; apply noise filtering.",
        entity_scope="compartmentalized reservoirs",
        confidence=0.88,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.7"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_thermal_recovery_reservoirs",
        keywords=["thermal recovery", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in thermal recovery reservoirs requires models that account for temperature effects and fluid property changes, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Thermal recovery reservoirs display pressure responses affected by temperature changes and fluid property variations. Interpretation uses models that account for thermal effects and integrates with production and geological data. The method is validated by matching observed responses to thermal recovery models and corroborating with reservoir mapping. Limitations include sensitivity to temperature measurement and operational changes.""",
        key_factors=["temperature measurement", "model selection", "production data integration", "fluid property changes"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="reservoir engineer",
        adversary_position="Temperature effects or operational changes may compromise interpretation in thermal recovery reservoirs.",
        counter_arguments=[
            "Temperature measurement errors affect accuracy.",
            "Operational changes affect pressure response.",
            "Noisy data reduces interpretation accuracy."
        ],
        resolution_strategy="Use advanced thermal recovery models; integrate production and geological data; apply noise filtering.",
        entity_scope="thermal recovery reservoirs",
        confidence=0.89,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.8"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_artificial_lift_wells",
        keywords=["artificial lift", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in artificial lift wells requires models that account for lift equipment effects and operational changes, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Artificial lift wells display pressure responses affected by lift equipment and operational changes. Interpretation uses models that account for artificial lift effects and integrates with production and operational data. The method is validated by matching observed responses to artificial lift models and corroborating with production trends. Limitations include sensitivity to lift equipment and operational variability.""",
        key_factors=["lift equipment effects", "model selection", "production data integration", "operational variability"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="production engineer",
        adversary_position="Lift equipment effects or operational changes may compromise interpretation in artificial lift wells.",
        counter_arguments=[
            "Lift equipment affects pressure response.",
            "Operational changes affect data quality.",
            "Noisy data reduces interpretation accuracy."
        ],
        resolution_strategy="Use advanced artificial lift models; integrate production and operational data; apply noise filtering.",
        entity_scope="artificial lift wells",
        confidence=0.87,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.9"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_injector_wells",
        keywords=["injector well", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in injector wells requires models that account for injection effects and reservoir response, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Injector wells display pressure responses affected by injection rate and reservoir response. Interpretation uses models that account for injection effects and integrates with production and geological data. The method is validated by matching observed responses to injector well models and corroborating with reservoir mapping. Limitations include sensitivity to injection rate measurement and operational changes.""",
        key_factors=["injection rate measurement", "model selection", "production data integration", "operational changes"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="injection engineer",
        adversary_position="Injection effects or operational changes may compromise interpretation in injector wells.",
        counter_arguments=[
            "Injection rate measurement errors affect accuracy.",
            "Operational changes affect pressure response.",
            "Noisy data reduces interpretation accuracy."
        ],
        resolution_strategy="Use advanced injector well models; integrate production and geological data; apply noise filtering.",
        entity_scope="injector wells",
        confidence=0.90,
        confidence_zone="high",
        controlling_precedent="SPE Handbook, Section 9.10"
    ),
    DoctrineBlock(
        topic="pressure_transient_testing_in_multi_lateral_wells",
        keywords=["multi-lateral well", "pressure transient", "testing", "well testing", "PROD03"],
        conclusion_template="Pressure transient testing in multi-lateral wells requires models that account for multiple branches and complex flow paths, enabling accurate interpretation of reservoir properties.",
        reasoning_framework="""Multi-lateral wells display pressure responses affected by multiple branches and complex flow paths. Interpretation uses models that account for multi-lateral effects and integrates with completion and geological data. The method is validated by matching observed responses to multi-lateral models and corroborating with reservoir mapping. Limitations include sensitivity to branch identification and data quality.""",
        key_factors=["branch identification", "model selection", "completion data integration", "data quality"],
        primary_authority=["SPE Petroleum Engineering Handbook", "PROD03_well_testing standards"],
        burden_holder="completion engineer",
        adversary_position="Multiple branches or poor data quality may compromise interpretation in multi-lateral wells.",
        counter_arguments=[
            "Multiple branches complicate model selection.",
            "Noisy data reduces interpretation accuracy.",
            "Completion data may be incomplete."
        ],
        resolution_strategy="Use advanced multi-lateral models; integrate completion and geological data; apply noise filtering.",
        entity_scope="multi-lateral wells",
        confidence=0.88,
        confidence_zone="medium-high",
        controlling_precedent="SPE Handbook, Section 9.11"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
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