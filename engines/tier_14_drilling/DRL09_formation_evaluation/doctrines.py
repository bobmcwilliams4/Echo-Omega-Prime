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
        topic="Gamma Ray Log Lithology Identification",
        keywords=["gamma ray", "lithology", "shale", "sandstone", "carbonate", "log interpretation"],
        conclusion_template="Based on the gamma ray log response, the dominant lithology is {lithology}, indicated by a gamma ray value of {gamma_ray_value} API units.",
        reasoning_framework="""
Gamma ray logs measure the natural radioactivity of formations, primarily from potassium, thorium, and uranium. Shales typically exhibit higher gamma ray readings due to their clay content, while sandstones and carbonates show lower values. The log is analyzed by setting baseline values for clean formations (sandstone or carbonate) and shales. Crossplots and histogram analysis may be used to refine cutoffs. The presence of radioactive minerals or feldspathic sands may complicate interpretation, requiring integration with other logs or core data. Environmental corrections and calibration to local stratigraphy are essential for accurate lithology identification.
""",
        key_factors=[
            "Gamma ray API value",
            "Baseline calibration",
            "Radioactive mineral presence",
            "Environmental corrections",
            "Integration with other logs"
        ],
        primary_authority=[
            "Asquith & Krygowski, Basic Well Log Analysis, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Interpreter",
        adversary_position="Gamma ray log alone cannot distinguish between all lithologies, especially in radioactive sandstones or non-shale clays.",
        counter_arguments=[
            "Integration with density/neutron logs improves lithology discrimination.",
            "Core data or spectral gamma ray logs can resolve ambiguities."
        ],
        resolution_strategy="Correlate gamma ray log with other petrophysical logs and core data; apply environmental corrections.",
        entity_scope="All sedimentary basins",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Shale Volume Calculation Models",
        keywords=["shale volume", "Vsh", "gamma ray", "linear method", "Larionov", "Stieber", "Clavier", "log analysis"],
        conclusion_template="Estimated shale volume (Vsh) is {vsh} using the {model} model based on gamma ray readings.",
        reasoning_framework="""
Shale volume (Vsh) is calculated from gamma ray logs using several empirical models. The linear method assumes a direct proportion between gamma ray index (GRI) and Vsh. The Larionov, Stieber, and Clavier models introduce corrections for older or younger formations and account for non-linear responses. Model selection depends on formation age, lithology, and calibration to core or regional data. The gamma ray index is computed as (GR_log - GR_clean) / (GR_shale - GR_clean). Each model applies a mathematical transformation to the GRI to estimate Vsh. Cross-validation with core or spectral gamma ray data is recommended.
""",
        key_factors=[
            "Gamma ray index (GRI)",
            "Model selection (linear, Larionov, Stieber, Clavier)",
            "Formation age",
            "Calibration to core data"
        ],
        primary_authority=[
            "Larionov, 1969",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Linear model overestimates Vsh in older formations; non-linear models may not fit all lithologies.",
        counter_arguments=[
            "Use of spectral gamma ray logs to distinguish clay types.",
            "Calibration with core measurements for local accuracy."
        ],
        resolution_strategy="Select model based on formation characteristics; validate with core or advanced logs.",
        entity_scope="Clastic reservoirs",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Larionov, 1969"
    ),
    DoctrineBlock(
        topic="Deep Resistivity Tools - Laterolog vs Induction",
        keywords=["deep resistivity", "laterolog", "induction", "tool selection", "formation conductivity", "log response"],
        conclusion_template="For {formation_type} formations, the preferred deep resistivity tool is {tool_type}, based on its response characteristics.",
        reasoning_framework="""
Laterolog tools inject current into the formation and measure potential differences, making them suitable for low-resistivity (conductive) muds and high-resistivity formations (e.g., carbonates, tight sands). Induction tools induce electromagnetic fields and measure the resulting currents, performing better in high-resistivity (non-conductive) muds and low-resistivity formations (e.g., shales, unconsolidated sands). Tool selection is based on mud type, formation resistivity, and borehole conditions. Calibration and environmental corrections are necessary for accurate interpretation. Crossplotting laterolog and induction responses can identify tool limitations and formation characteristics.
""",
        key_factors=[
            "Mud conductivity",
            "Formation resistivity",
            "Tool physics",
            "Environmental corrections"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Principles, 1989",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Logging engineer",
        adversary_position="Tool responses may be ambiguous in mixed lithologies or complex borehole environments.",
        counter_arguments=[
            "Use both tool types and compare responses.",
            "Apply borehole correction algorithms."
        ],
        resolution_strategy="Select tool based on mud and formation properties; validate with cross-tool comparison.",
        entity_scope="All formations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Schlumberger, 1989"
    ),
    DoctrineBlock(
        topic="Micro-Resistivity and Rxo Measurement",
        keywords=["micro-resistivity", "Rxo", "flushed zone", "invasion", "mud filtrate", "log interpretation"],
        conclusion_template="The flushed zone resistivity (Rxo) is measured as {rxo_value} ohm-m, indicating {invasion_characteristics}.",
        reasoning_framework="""
Micro-resistivity tools (e.g., Micro SFL, Microlog) measure the resistivity of the flushed zone (Rxo), which is invaded by mud filtrate. Rxo is compared with deep resistivity (Rt) to assess invasion profiles and hydrocarbon presence. A high Rxo/Rt ratio suggests low invasion or oil-based mud, while a low ratio may indicate water invasion or formation damage. Interpretation requires correction for borehole effects and mudcake. Integration with invasion profile models and core data enhances reliability. Rxo is critical for evaluating formation permeability and hydrocarbon mobility.
""",
        key_factors=[
            "Micro-resistivity log response",
            "Rxo/Rt ratio",
            "Invasion profile",
            "Mud type"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Rxo measurements can be distorted by mudcake or borehole rugosity.",
        counter_arguments=[
            "Apply mudcake and borehole corrections.",
            "Correlate with core invasion profiles."
        ],
        resolution_strategy="Use corrected micro-resistivity logs; integrate with core and invasion models.",
        entity_scope="All reservoirs",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Density Log - Bulk Density and Porosity",
        keywords=["density log", "bulk density", "porosity", "matrix density", "fluid density", "log interpretation"],
        conclusion_template="Calculated porosity is {porosity} using bulk density of {bulk_density} g/cc and matrix density of {matrix_density} g/cc.",
        reasoning_framework="""
Density logs measure electron density, which correlates with bulk density. Porosity is calculated using the formula: PHI = (RHOB_matrix - RHOB_log) / (RHOB_matrix - RHOB_fluid). Matrix density is selected based on lithology (2.65 g/cc for sandstone, 2.71 g/cc for limestone, 2.87 g/cc for dolomite). Fluid density is typically 1.0 g/cc for fresh water, adjusted for brine or hydrocarbons. Corrections for borehole size, mudcake, and invasion are applied. Integration with neutron and sonic logs improves porosity estimation, especially in shaly or gas-bearing zones.
""",
        key_factors=[
            "Bulk density (RHOB)",
            "Matrix density",
            "Fluid density",
            "Environmental corrections"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Gas effect and shaliness can distort density-derived porosity.",
        counter_arguments=[
            "Crossplot with neutron and sonic logs.",
            "Apply shale and gas corrections."
        ],
        resolution_strategy="Use multi-log integration and apply corrections for shaliness and gas.",
        entity_scope="All reservoirs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Neutron Log - Hydrogen Index Porosity",
        keywords=["neutron log", "hydrogen index", "porosity", "gas effect", "log interpretation"],
        conclusion_template="Neutron log indicates a porosity of {porosity}, with a hydrogen index of {hydrogen_index}.",
        reasoning_framework="""
Neutron logs measure hydrogen content, which correlates with formation porosity. The hydrogen index is affected by the presence of gas, which reduces apparent porosity, and by shaliness, which increases it. Calibration is performed using known lithologies and fluids. Gas-bearing zones are identified by a crossover with density logs (density-neutron separation). Corrections for borehole size, mudcake, and lithology are applied. Integration with density and sonic logs is essential for accurate porosity and lithology determination.
""",
        key_factors=[
            "Hydrogen index",
            "Lithology calibration",
            "Gas effect",
            "Shaliness"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Gas zones cause underestimation of porosity; shaliness causes overestimation.",
        counter_arguments=[
            "Use density-neutron crossplot to identify gas effect.",
            "Apply shale corrections."
        ],
        resolution_strategy="Integrate neutron log with density and sonic logs; apply corrections as needed.",
        entity_scope="All reservoirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Sonic Log - Wyllie Time Average Equation",
        keywords=["sonic log", "Wyllie equation", "porosity", "acoustic travel time", "log interpretation"],
        conclusion_template="Porosity is calculated as {porosity} using the Wyllie time average equation with travel time {delta_t}.",
        reasoning_framework="""
The Wyllie time average equation relates acoustic travel time (Δt) to porosity: PHI = (Δt_log - Δt_matrix) / (Δt_fluid - Δt_matrix). Matrix and fluid travel times are selected based on lithology and fluid type. The equation assumes a linear relationship and is most accurate in clean, consolidated formations. The presence of shale, gas, or secondary porosity (fractures, vugs) can distort results. Integration with density and neutron logs is recommended for improved accuracy. Corrections for borehole effects and tool standoff are applied.
""",
        key_factors=[
            "Acoustic travel time (Δt)",
            "Matrix and fluid Δt values",
            "Lithology",
            "Secondary porosity"
        ],
        primary_authority=[
            "Wyllie et al., 1956",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Equation underestimates porosity in fractured or vuggy formations.",
        counter_arguments=[
            "Use crossplot with density and neutron logs.",
            "Apply corrections for secondary porosity."
        ],
        resolution_strategy="Integrate sonic log with other porosity logs; apply corrections for formation characteristics.",
        entity_scope="All consolidated formations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Wyllie et al., 1956"
    ),
    DoctrineBlock(
        topic="Archie Equation - Water Saturation Calculation",
        keywords=["Archie equation", "water saturation", "Sw", "formation resistivity", "porosity", "Rw", "log analysis"],
        conclusion_template="Calculated water saturation (Sw) is {sw} using the Archie equation with Rt={rt}, Rw={rw}, and porosity={porosity}.",
        reasoning_framework="""
The Archie equation estimates water saturation (Sw) in clean, water-wet formations: Sw^n = (a / (porosity^m)) * (Rw / Rt), where a, m, and n are empirical constants. Rw (formation water resistivity) is determined from SP log, water sample, or empirical methods. Rt is the true formation resistivity from deep resistivity logs. The equation assumes no conductive minerals (clays) and water-wet conditions. In shaly or oil-wet formations, modified models (e.g., Simandoux, Waxman-Smits) are used. Calibration to core measurements is recommended.
""",
        key_factors=[
            "Rt (true resistivity)",
            "Rw (formation water resistivity)",
            "Porosity",
            "Empirical constants (a, m, n)"
        ],
        primary_authority=[
            "Archie, 1942",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Archie equation fails in shaly or oil-wet formations.",
        counter_arguments=[
            "Use shaly sand models (Simandoux, Waxman-Smits) as appropriate.",
            "Calibrate with core data."
        ],
        resolution_strategy="Apply Archie equation in clean sands; use alternative models in shaly or complex lithologies.",
        entity_scope="Clean, water-wet reservoirs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Archie, 1942"
    ),
    DoctrineBlock(
        topic="Formation Water Resistivity (Rw) Determination",
        keywords=["Rw", "formation water resistivity", "SP log", "water sample", "log analysis"],
        conclusion_template="Formation water resistivity (Rw) is determined as {rw} ohm-m using the {method} method.",
        reasoning_framework="""
Rw is a critical input for water saturation calculations. It can be determined from water samples, SP log analysis, or empirical equations (e.g., Pickett plot). SP log provides Rw by comparing static SP deflection with known formation and mud filtrate properties. Water samples offer direct measurement but may be contaminated. Empirical methods use crossplots of resistivity and porosity logs to estimate Rw. Selection of method depends on data availability, formation characteristics, and quality control. Calibration with core or laboratory measurements enhances reliability.
""",
        key_factors=[
            "SP log response",
            "Water sample quality",
            "Empirical crossplots",
            "Formation and mud properties"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="SP log may be unreliable in oil-based muds or thin beds.",
        counter_arguments=[
            "Use multiple methods and cross-validate results.",
            "Apply corrections for mud type and bed thickness."
        ],
        resolution_strategy="Combine SP log, water sample, and empirical methods; calibrate with core data.",
        entity_scope="All reservoirs",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Spontaneous Potential (SP) Log Interpretation",
        keywords=["SP log", "spontaneous potential", "permeability", "shale baseline", "log analysis"],
        conclusion_template="SP log indicates {permeability} and {shale_content} based on deflection and baseline analysis.",
        reasoning_framework="""
SP logs measure the natural electrical potential between borehole and formation, primarily reflecting permeability and shale content. The SP deflection from the shale baseline is proportional to formation permeability and the contrast in salinity between formation water and mud filtrate. Interpretation involves identifying the shale baseline, measuring SP deflection, and correlating with lithology and permeability. Limitations include oil-based muds, thin beds, and complex salinity profiles. Integration with resistivity and porosity logs improves formation evaluation.
""",
        key_factors=[
            "SP deflection",
            "Shale baseline",
            "Salinity contrast",
            "Permeability"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="SP log is ineffective in oil-based muds or where salinity contrast is low.",
        counter_arguments=[
            "Use alternative logs (resistivity, porosity) for formation evaluation.",
            "Apply corrections for mud type and salinity."
        ],
        resolution_strategy="Integrate SP log with other logs; apply corrections as needed.",
        entity_scope="Water-based mud environments",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Caliper Log - Borehole Size and Formation Quality",
        keywords=["caliper log", "borehole size", "formation quality", "washout", "log correction"],
        conclusion_template="Caliper log shows borehole diameter of {diameter} inches, indicating {formation_quality}.",
        reasoning_framework="""
Caliper logs measure borehole diameter and identify washouts, caving, or tight spots. Large borehole diameters suggest poor formation quality (e.g., unconsolidated sands, shales), while stable diameters indicate competent rock. Caliper data are used to correct other logs (density, neutron) for borehole effects. Integration with lithology and resistivity logs helps distinguish between mechanical and chemical enlargement. Caliper logs also aid in casing and cementing decisions.
""",
        key_factors=[
            "Borehole diameter",
            "Washout/caving",
            "Formation lithology",
            "Log correction needs"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Logging engineer",
        adversary_position="Caliper logs may be affected by tool eccentricity or mudcake.",
        counter_arguments=[
            "Use multi-arm caliper tools.",
            "Cross-validate with other logs and drilling data."
        ],
        resolution_strategy="Apply corrections for tool and borehole effects; integrate with other logs.",
        entity_scope="All boreholes",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="NMR Logging - T2 Distributions and Permeability",
        keywords=["NMR log", "T2 distribution", "permeability", "porosity", "fluid typing", "log interpretation"],
        conclusion_template="NMR log indicates a T2 distribution with {t2_peak} ms, suggesting {pore_size} and estimated permeability of {permeability}.",
        reasoning_framework="""
NMR (Nuclear Magnetic Resonance) logs measure the relaxation time (T2) of hydrogen nuclei, providing direct porosity and pore size distribution. Short T2 times indicate small pores (clay-bound water), while long T2 times indicate larger, producible pores. Permeability is estimated using empirical relationships (e.g., Coates or Timur equations) based on T2 distribution. NMR distinguishes between bound and free fluids, aiding in fluid typing and movable hydrocarbon identification. Integration with conventional logs and core data enhances interpretation.
""",
        key_factors=[
            "T2 distribution",
            "Porosity",
            "Permeability estimation model",
            "Fluid typing"
        ],
        primary_authority=[
            "Coates et al., 1999",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="NMR logs are expensive and may be affected by magnetic minerals.",
        counter_arguments=[
            "Use NMR selectively in key intervals.",
            "Correct for magnetic susceptibility effects."
        ],
        resolution_strategy="Integrate NMR with conventional logs; apply corrections for mineralogy.",
        entity_scope="All reservoirs",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Coates et al., 1999"
    ),
    DoctrineBlock(
        topic="Formation Pressure Testing - MDT, RFT, DST",
        keywords=["formation pressure", "MDT", "RFT", "DST", "pressure gradient", "fluid sampling"],
        conclusion_template="Formation pressure measured as {pressure} psi using {tool_type}, indicating {fluid_type} gradient.",
        reasoning_framework="""
Formation pressure testing tools (MDT, RFT, DST) measure reservoir pressure and collect fluid samples. MDT (Modular Formation Dynamics Tester) and RFT (Repeat Formation Tester) provide point pressure measurements and gradient profiles. DST (Drill Stem Test) offers extended flow and pressure data. Tool selection depends on reservoir properties, operational constraints, and data objectives. Pressure gradients are used to identify fluid contacts and reservoir compartmentalization. Data quality depends on tool sealing, mudcake, and formation permeability.
""",
        key_factors=[
            "Tool type (MDT, RFT, DST)",
            "Pressure measurement quality",
            "Fluid sampling",
            "Pressure gradient analysis"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Poor tool sealing or low permeability may yield unreliable pressure data.",
        counter_arguments=[
            "Repeat measurements and validate with other data.",
            "Apply corrections for mudcake and tool effects."
        ],
        resolution_strategy="Select appropriate tool; ensure quality control and data validation.",
        entity_scope="All reservoirs",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Mud Logging - Gas Shows and Cuttings Analysis",
        keywords=["mud logging", "gas shows", "cuttings", "hydrocarbon detection", "drilling monitoring"],
        conclusion_template="Mud log indicates gas show at {depth} ft with {gas_type} and cuttings analysis suggests {lithology}.",
        reasoning_framework="""
Mud logging involves continuous monitoring of drilling mud for gas shows and analysis of cuttings for lithology and hydrocarbon presence. Gas shows are detected using chromatographs and total gas meters. Cuttings are examined under microscopes for mineralogy, hydrocarbon staining, and fluorescence. Data are used to correlate with wireline logs and identify hydrocarbon-bearing zones. Limitations include lag time, sample contamination, and depth uncertainty. Integration with wireline and LWD logs improves interpretation.
""",
        key_factors=[
            "Gas show detection",
            "Cuttings analysis",
            "Lag time correction",
            "Correlation with logs"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Mud logger",
        adversary_position="Gas shows may be contaminated or misinterpreted due to drilling fluids.",
        counter_arguments=[
            "Apply lag time corrections.",
            "Cross-validate with wireline and LWD logs."
        ],
        resolution_strategy="Integrate mud log data with wireline and LWD logs; apply corrections for drilling effects.",
        entity_scope="All drilling operations",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 13B-1, 2009"
    ),
    DoctrineBlock(
        topic="LWD (Logging While Drilling) vs Wireline Comparison",
        keywords=["LWD", "wireline", "real-time logging", "log quality", "borehole conditions"],
        conclusion_template="LWD provides {advantages} over wireline in {conditions}, but wireline offers {advantages} in {other_conditions}.",
        reasoning_framework="""
LWD tools acquire log data in real time during drilling, enabling immediate decision-making and reducing operational risk. LWD is advantageous in highly deviated or horizontal wells and unstable boreholes where wireline may not be feasible. Wireline logs generally offer higher resolution and broader tool selection. Data quality may differ due to borehole conditions, tool standoff, and mud properties. Integration of LWD and wireline data provides comprehensive formation evaluation.
""",
        key_factors=[
            "Well deviation",
            "Borehole stability",
            "Tool resolution",
            "Operational constraints"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Logging engineer",
        adversary_position="LWD logs may have lower resolution and limited tool options.",
        counter_arguments=[
            "Use wireline for detailed evaluation where feasible.",
            "Integrate both datasets for optimal results."
        ],
        resolution_strategy="Select logging method based on well conditions and data requirements; integrate datasets.",
        entity_scope="All wells",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Neutron-Density Crossplot for Lithology and Gas",
        keywords=["neutron-density crossplot", "lithology identification", "gas detection", "porosity logs"],
        conclusion_template="Neutron-density crossplot indicates {lithology} with gas effect evidenced by {crossplot_pattern}.",
        reasoning_framework="""
Neutron and density logs are crossplotted to distinguish lithology and detect gas zones. Clean formations plot along characteristic lithology lines (sandstone, limestone, dolomite). Gas-bearing zones show density-neutron separation (crossover), with density porosity reading lower than neutron. Shaly formations may complicate interpretation. Crossplotting aids in identifying lithology, porosity, and gas presence. Integration with core and other logs enhances reliability.
""",
        key_factors=[
            "Crossplot pattern",
            "Density-neutron separation",
            "Lithology lines",
            "Shaliness"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Shaliness and tool calibration errors can distort crossplot interpretation.",
        counter_arguments=[
            "Apply shale corrections.",
            "Calibrate tools and validate with core data."
        ],
        resolution_strategy="Use crossplot with corrections and calibration; integrate with core data.",
        entity_scope="All reservoirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="M-N Plot and MID Plot for Complex Lithology",
        keywords=["M-N plot", "MID plot", "complex lithology", "porosity logs", "lithology discrimination"],
        conclusion_template="M-N plot indicates {lithology} with M={m_value} and N={n_value}; MID plot confirms with {mid_pattern}.",
        reasoning_framework="""
M-N plots use density, neutron, and sonic logs to discriminate lithology in complex formations. M and N parameters are calculated from log responses and plotted to identify lithology clusters. MID (Mineral Identification) plots extend this approach using additional log data. These plots are effective in distinguishing mixed lithologies, shaly sands, and carbonates. Calibration with core and regional data improves accuracy. Limitations include tool calibration errors and secondary porosity effects.
""",
        key_factors=[
            "M and N values",
            "MID plot pattern",
            "Log calibration",
            "Lithology clusters"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Secondary porosity and tool errors can distort plot interpretation.",
        counter_arguments=[
            "Calibrate tools and validate with core data.",
            "Apply corrections for secondary porosity."
        ],
        resolution_strategy="Use M-N and MID plots with calibration and corrections; integrate with core data.",
        entity_scope="Complex lithologies",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Thin Bed Analysis and Vertical Resolution",
        keywords=["thin beds", "vertical resolution", "log response", "bed thickness", "tool physics"],
        conclusion_template="Log response indicates thin bed of {thickness} ft, with vertical resolution limit of {resolution} ft.",
        reasoning_framework="""
Wireline and LWD logs have finite vertical resolution, typically 2-3 ft for resistivity and 1-2 ft for density/neutron logs. Thin beds below tool resolution appear as blended responses, leading to underestimation of net pay and porosity. Deconvolution algorithms and high-resolution tools (e.g., micro-resistivity, image logs) improve thin bed analysis. Integration with core and image data is essential for accurate net pay and reservoir characterization.
""",
        key_factors=[
            "Bed thickness",
            "Tool vertical resolution",
            "Deconvolution algorithms",
            "Integration with core/image data"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Thin beds below tool resolution cannot be reliably quantified with standard logs.",
        counter_arguments=[
            "Use high-resolution or image logs.",
            "Apply deconvolution and integrate with core data."
        ],
        resolution_strategy="Apply advanced logging and processing; integrate with core/image data.",
        entity_scope="Thinly bedded reservoirs",
        confidence=0.84,
        confidence_zone="Moderate",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Invasion Profile and Radial Resistivity Variations",
        keywords=["invasion profile", "radial resistivity", "invasion zone", "Rt", "Rxo", "log analysis"],
        conclusion_template="Radial resistivity profile shows {invasion_depth} invasion with Rt={rt}, Rxo={rxo}, and Rm={rm}.",
        reasoning_framework="""
Invasion profiles are interpreted by comparing resistivity measurements at different depths of investigation (Rxo, Rm, Rt). The profile reveals the extent of mud filtrate invasion and helps identify movable hydrocarbons. A steep resistivity gradient indicates deep invasion or high permeability. Radial resistivity analysis aids in formation evaluation, invasion correction, and hydrocarbon identification. Integration with core and pressure data enhances reliability.
""",
        key_factors=[
            "Resistivity at multiple depths",
            "Invasion depth",
            "Formation permeability",
            "Mud filtrate properties"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Complex invasion profiles may be misinterpreted without supporting data.",
        counter_arguments=[
            "Integrate with core and pressure data.",
            "Apply invasion correction models."
        ],
        resolution_strategy="Use multi-depth resistivity logs; integrate with supporting data.",
        entity_scope="All reservoirs",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Formation Damage Identification via Logs",
        keywords=["formation damage", "log interpretation", "invasion", "permeability reduction", "skin effect"],
        conclusion_template="Log analysis indicates formation damage characterized by {damage_type} and {log_signature}.",
        reasoning_framework="""
Formation damage is identified by log signatures such as reduced permeability, altered invasion profiles, and changes in resistivity or porosity logs. Damage may result from drilling fluids, completion operations, or fines migration. Key indicators include low Rxo/Rt ratio, decreased porosity, and anomalous pressure gradients. Integration with core, pressure, and production data is essential for confirmation. Remediation strategies depend on damage type and severity.
""",
        key_factors=[
            "Rxo/Rt ratio",
            "Porosity reduction",
            "Pressure gradient anomalies",
            "Integration with core/production data"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Log signatures may be ambiguous and require supporting evidence.",
        counter_arguments=[
            "Correlate with core and production data.",
            "Apply advanced log interpretation techniques."
        ],
        resolution_strategy="Integrate logs with core and production data; apply remediation as needed.",
        entity_scope="All reservoirs",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Core Analysis Correlation with Log Data",
        keywords=["core analysis", "log correlation", "porosity", "permeability", "calibration"],
        conclusion_template="Core analysis confirms log-derived porosity of {porosity} and permeability of {permeability}.",
        reasoning_framework="""
Core analysis provides ground truth for log-derived petrophysical properties. Porosity and permeability from core plugs are compared with log estimates for calibration and model refinement. Discrepancies may arise from scale differences, core damage, or heterogeneity. Statistical analysis and crossplots are used for correlation. Calibration improves log interpretation accuracy and supports reservoir characterization.
""",
        key_factors=[
            "Core porosity and permeability",
            "Log-derived estimates",
            "Calibration and correction",
            "Scale and heterogeneity"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Core data may be affected by sampling bias or core damage.",
        counter_arguments=[
            "Apply corrections for core damage.",
            "Use statistical methods for calibration."
        ],
        resolution_strategy="Calibrate logs with core data; apply corrections as needed.",
        entity_scope="All reservoirs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Pay Zone Identification Criteria",
        keywords=["pay zone", "net pay", "hydrocarbon indication", "log cutoffs", "formation evaluation"],
        conclusion_template="Pay zone identified from {depth_start} to {depth_end} ft based on log cutoffs: porosity > {porosity_cutoff}, Sw < {sw_cutoff}.",
        reasoning_framework="""
Pay zones are identified using log-derived cutoffs for porosity, water saturation (Sw), and hydrocarbon indicators (e.g., resistivity, gas effect). Cutoff values are selected based on reservoir characteristics, core data, and production history. Net pay is calculated as the sum of intervals meeting all criteria. Integration with core, test, and production data refines pay identification. Sensitivity analysis is performed to optimize cutoff selection.
""",
        key_factors=[
            "Porosity cutoff",
            "Sw cutoff",
            "Hydrocarbon indicators",
            "Integration with core/test data"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Cutoff selection is subjective and may miss marginal pay.",
        counter_arguments=[
            "Use sensitivity analysis and integrate with production data.",
            "Adjust cutoffs based on reservoir performance."
        ],
        resolution_strategy="Optimize cutoffs with multi-source data; validate with production results.",
        entity_scope="All reservoirs",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Net-to-Gross Calculation and Reservoir Volume",
        keywords=["net-to-gross", "reservoir volume", "pay thickness", "log cutoffs", "formation evaluation"],
        conclusion_template="Net-to-gross ratio is {ntg} with net reservoir thickness of {net_thickness} ft over gross interval {gross_interval} ft.",
        reasoning_framework="""
Net-to-gross (NTG) ratio is calculated as the proportion of net reservoir (meeting porosity and Sw cutoffs) to gross interval. Accurate NTG estimation requires consistent log cutoffs, correction for thin beds, and integration with core data. NTG is used to estimate hydrocarbon volume and support reservoir modeling. Sensitivity analysis and calibration with production data improve reliability.
""",
        key_factors=[
            "Porosity and Sw cutoffs",
            "Gross interval definition",
            "Thin bed correction",
            "Calibration with core/production data"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Thin beds and heterogeneity may lead to NTG underestimation.",
        counter_arguments=[
            "Apply thin bed correction algorithms.",
            "Integrate with core and production data."
        ],
        resolution_strategy="Use advanced logging and calibration; apply corrections for thin beds.",
        entity_scope="All reservoirs",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Petrophysical Cutoff Optimization",
        keywords=["petrophysical cutoff", "optimization", "porosity cutoff", "Sw cutoff", "formation evaluation"],
        conclusion_template="Optimized cutoffs: porosity > {porosity_cutoff}, Sw < {sw_cutoff}, based on {optimization_method}.",
        reasoning_framework="""
Petrophysical cutoffs for porosity and water saturation are optimized using core data, production history, and statistical analysis. Sensitivity analysis evaluates the impact of different cutoffs on net pay and reservoir volume. Cutoff selection balances hydrocarbon recovery with operational constraints. Machine learning and multivariate analysis may be used for advanced optimization. Continuous review and adjustment are recommended as more data become available.
""",
        key_factors=[
            "Core and production data",
            "Sensitivity analysis",
            "Statistical/machine learning methods",
            "Operational constraints"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Overly strict or lenient cutoffs may misclassify pay zones.",
        counter_arguments=[
            "Validate cutoffs with production performance.",
            "Use multi-disciplinary input for cutoff selection."
        ],
        resolution_strategy="Optimize cutoffs with integrated data and advanced analysis.",
        entity_scope="All reservoirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Permian Basin - Spraberry Formation Characteristics",
        keywords=["Permian Basin", "Spraberry Formation", "lithology", "petrophysics", "reservoir quality"],
        conclusion_template="Spraberry Formation characterized by {lithology}, porosity {porosity_range}, permeability {permeability_range}, and {reservoir_quality}.",
        reasoning_framework="""
The Spraberry Formation is a mixed siliciclastic-carbonate sequence with low to moderate porosity (6-12%) and low permeability (<1 mD). Reservoir quality is controlled by grain size, cementation, and natural fractures. Gamma ray, density, and resistivity logs are used for lithology and fluid identification. Hydraulic fracturing is typically required for economic production. Integration of core, log, and production data is essential for reservoir characterization.
""",
        key_factors=[
            "Lithology",
            "Porosity and permeability",
            "Natural fractures",
            "Integration with core/log data"
        ],
        primary_authority=[
            "Dutton et al., 2005",
            "USGS, 2016"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Heterogeneity and low permeability challenge reservoir development.",
        counter_arguments=[
            "Use advanced logging and core analysis.",
            "Apply hydraulic fracturing for productivity."
        ],
        resolution_strategy="Integrate multi-source data; apply stimulation as needed.",
        entity_scope="Permian Basin - Spraberry",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="USGS, 2016"
    ),
    DoctrineBlock(
        topic="Permian Basin - Wolfcamp Formation Evaluation",
        keywords=["Permian Basin", "Wolfcamp Formation", "shale", "petrophysics", "TOC", "reservoir quality"],
        conclusion_template="Wolfcamp Formation has TOC of {toc}%, porosity {porosity_range}, and {reservoir_quality}.",
        reasoning_framework="""
The Wolfcamp Formation is an organic-rich shale and carbonate sequence with high TOC (3-8%) and variable porosity (4-12%). Reservoir quality depends on mineralogy, organic content, and natural fractures. Gamma ray, resistivity, and NMR logs are used for TOC and porosity estimation. Hydraulic fracturing is essential for economic production. Integration with core, log, and production data supports reservoir evaluation and completion design.
""",
        key_factors=[
            "TOC (Total Organic Carbon)",
            "Porosity",
            "Mineralogy",
            "Natural fractures"
        ],
        primary_authority=[
            "USGS, 2016",
            "Dutton et al., 2005"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Complex mineralogy and variable TOC complicate evaluation.",
        counter_arguments=[
            "Use advanced logs (NMR, spectral gamma ray).",
            "Integrate with core and production data."
        ],
        resolution_strategy="Apply integrated petrophysical and geochemical analysis.",
        entity_scope="Permian Basin - Wolfcamp",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="USGS, 2016"
    ),
    DoctrineBlock(
        topic="Permian Basin - Bone Spring Formation (Delaware Basin)",
        keywords=["Permian Basin", "Bone Spring Formation", "Delaware Basin", "lithology", "petrophysics"],
        conclusion_template="Bone Spring Formation characterized by {lithology}, porosity {porosity_range}, and {reservoir_quality}.",
        reasoning_framework="""
The Bone Spring Formation is a mixed carbonate-siliciclastic sequence with moderate porosity (6-14%) and variable permeability. Reservoir quality is influenced by depositional facies, diagenesis, and natural fractures. Gamma ray, density, and resistivity logs are used for lithology and fluid identification. Hydraulic fracturing is commonly applied to enhance productivity. Integration of core, log, and production data is critical for reservoir evaluation.
""",
        key_factors=[
            "Lithology",
            "Porosity and permeability",
            "Depositional facies",
            "Natural fractures"
        ],
        primary_authority=[
            "USGS, 2016",
            "Dutton et al., 2005"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Facies variability and diagenesis complicate reservoir characterization.",
        counter_arguments=[
            "Use detailed core and log analysis.",
            "Apply advanced petrophysical models."
        ],
        resolution_strategy="Integrate core, log, and production data for comprehensive evaluation.",
        entity_scope="Permian Basin - Bone Spring",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="USGS, 2016"
    ),
    DoctrineBlock(
        topic="Spectral Gamma Ray Logging - Clay Type Discrimination",
        keywords=["spectral gamma ray", "clay type", "potassium", "thorium", "uranium", "log interpretation"],
        conclusion_template="Spectral gamma ray log indicates dominant clay type is {clay_type} based on K, Th, U concentrations.",
        reasoning_framework="""
Spectral gamma ray logs measure individual contributions of potassium (K), thorium (Th), and uranium (U) to total radioactivity. Clay minerals have characteristic signatures: illite is rich in K, kaolinite is low in K and Th, and smectite is low in all three. High U may indicate organic-rich shales. Discrimination of clay types aids in reservoir quality assessment and shale volume estimation. Integration with XRD and core data enhances interpretation.
""",
        key_factors=[
            "K, Th, U concentrations",
            "Clay mineralogy",
            "Integration with XRD/core data",
            "Environmental corrections"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Overlap in elemental signatures may cause misclassification.",
        counter_arguments=[
            "Integrate with mineralogical and core data.",
            "Apply statistical analysis for discrimination."
        ],
        resolution_strategy="Combine spectral gamma ray with core/XRD data for clay typing.",
        entity_scope="All shaly formations",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Resistivity Image Logging - Fracture and Bed Boundary Identification",
        keywords=["resistivity image log", "fracture identification", "bed boundaries", "borehole imaging"],
        conclusion_template="Image log reveals {fracture_density} fractures and {bed_boundary_type} boundaries at {depth}.",
        reasoning_framework="""
Resistivity image logs provide high-resolution images of borehole walls, enabling identification of fractures, bed boundaries, and sedimentary structures. Fractures appear as sinusoidal features, while bed boundaries are linear. Image logs are used for structural interpretation, fracture density analysis, and sedimentology. Integration with core and conventional logs enhances reservoir characterization. Limitations include borehole rugosity and tool standoff.
""",
        key_factors=[
            "Image log resolution",
            "Fracture and bed boundary features",
            "Borehole conditions",
            "Integration with core/log data"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Image quality may be degraded in rugose or enlarged boreholes.",
        counter_arguments=[
            "Use centralizers and optimize tool deployment.",
            "Cross-validate with core and other logs."
        ],
        resolution_strategy="Optimize logging conditions; integrate with core and log data.",
        entity_scope="All boreholes",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Cement Bond Log Interpretation",
        keywords=["cement bond log", "CBL", "cement evaluation", "well integrity", "acoustic log"],
        conclusion_template="CBL shows {cement_quality} cement bond at {depth}, indicating {well_integrity_status}.",
        reasoning_framework="""
Cement bond logs use acoustic signals to evaluate the quality of cement behind casing. Good cement shows high attenuation and low amplitude, while poor cement or channels show high amplitude. Interpretation includes amplitude and VDL (Variable Density Log) analysis. Integration with ultrasonic logs and well construction data improves reliability. CBL is critical for well integrity and zonal isolation assessment.
""",
        key_factors=[
            "Amplitude and VDL response",
            "Cement quality",
            "Well construction data",
            "Integration with ultrasonic logs"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "API RP 10B-2, 2013"
        ],
        burden_holder="Well engineer",
        adversary_position="CBL may be ambiguous in micro-annulus or fast formations.",
        counter_arguments=[
            "Use ultrasonic logs for confirmation.",
            "Integrate with well construction records."
        ],
        resolution_strategy="Combine CBL with ultrasonic logs and well data for evaluation.",
        entity_scope="Cased wells",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 10B-2, 2013"
    ),
    DoctrineBlock(
        topic="Shaly Sand Models - Simandoux and Waxman-Smits",
        keywords=["shaly sand", "Simandoux model", "Waxman-Smits model", "water saturation", "log analysis"],
        conclusion_template="Water saturation (Sw) calculated as {sw} using the {model} model for shaly sands.",
        reasoning_framework="""
Shaly sand models account for the conductivity of clay minerals in water saturation calculations. The Simandoux model introduces a dual-conduction term for clay and water. The Waxman-Smits model incorporates cation exchange capacity (CEC) of clays. Model selection depends on clay content, type, and data availability. Calibration with core and laboratory data is recommended. These models improve Sw estimation in shaly reservoirs compared to the Archie equation.
""",
        key_factors=[
            "Clay content and type",
            "CEC measurement",
            "Model calibration",
            "Integration with core/lab data"
        ],
        primary_authority=[
            "Simandoux, 1963",
            "Waxman & Smits, 1968"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Model parameters may be difficult to measure or estimate.",
        counter_arguments=[
            "Use laboratory measurements for CEC.",
            "Apply sensitivity analysis for parameter selection."
        ],
        resolution_strategy="Select model based on data availability; calibrate with core/lab data.",
        entity_scope="Shaly sand reservoirs",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Simandoux, 1963"
    ),
    DoctrineBlock(
        topic="TOC Estimation from Logs (Passey Method)",
        keywords=["TOC", "total organic carbon", "Passey method", "log analysis", "source rock"],
        conclusion_template="Estimated TOC is {toc}% using the Passey method based on ΔlogR and sonic/resistivity logs.",
        reasoning_framework="""
The Passey method estimates TOC by comparing sonic and resistivity logs to establish a baseline for non-source rocks. The ΔlogR parameter quantifies the separation between logs in organic-rich intervals. TOC is calculated using empirical equations calibrated to core data. The method is widely used in shale plays and requires careful baseline selection and calibration. Integration with core and geochemical data improves accuracy.
""",
        key_factors=[
            "ΔlogR parameter",
            "Baseline selection",
            "Calibration to core data",
            "Integration with geochemical analysis"
        ],
        primary_authority=[
            "Passey et al., 1990",
            "USGS, 2016"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Baseline selection is subjective and may affect TOC estimation.",
        counter_arguments=[
            "Use multiple baseline intervals.",
            "Calibrate with core and geochemical data."
        ],
        resolution_strategy="Apply Passey method with careful baseline selection and calibration.",
        entity_scope="Source rock intervals",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Passey et al., 1990"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Effectiveness Evaluation via Logs",
        keywords=["hydraulic fracturing", "effectiveness", "log analysis", "production logging", "fracture identification"],
        conclusion_template="Hydraulic fracturing effectiveness evaluated as {effectiveness} based on production log and image log data.",
        reasoning_framework="""
Effectiveness of hydraulic fracturing is evaluated using production logs (spinner, temperature), image logs, and microseismic data. Increased flow rates and temperature anomalies indicate successful stimulation. Image logs reveal induced fractures and fracture density. Integration with pre- and post-frac log data provides evidence of fracture propagation and reservoir contact. Limitations include tool resolution and complex fracture networks.
""",
        key_factors=[
            "Production log response",
            "Image log fracture analysis",
            "Pre- and post-frac log comparison",
            "Microseismic data"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "USGS, 2016"
        ],
        burden_holder="Completion engineer",
        adversary_position="Complex fracture networks may be difficult to interpret with logs alone.",
        counter_arguments=[
            "Use microseismic and tracer data.",
            "Integrate with production performance."
        ],
        resolution_strategy="Combine multiple log types and production data for evaluation.",
        entity_scope="Hydraulically fractured wells",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="USGS, 2016"
    ),
    DoctrineBlock(
        topic="Water Saturation Uncertainty Quantification",
        keywords=["water saturation", "uncertainty", "Sw", "log analysis", "sensitivity analysis"],
        conclusion_template="Water saturation (Sw) uncertainty estimated as ±{sw_uncertainty} based on sensitivity to Rw, porosity, and m/n parameters.",
        reasoning_framework="""
Uncertainty in water saturation estimation arises from errors in Rw, porosity, and Archie parameters (m, n). Sensitivity analysis quantifies the impact of each parameter on Sw. Monte Carlo simulation and probabilistic methods provide uncertainty ranges. Integration with core and production data reduces uncertainty. Reporting Sw with uncertainty supports risk-based reservoir management.
""",
        key_factors=[
            "Rw, porosity, m/n parameter uncertainty",
            "Sensitivity analysis",
            "Monte Carlo/probabilistic methods",
            "Integration with core/production data"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Uncertainty quantification may be limited by data availability.",
        counter_arguments=[
            "Use probabilistic methods with available data.",
            "Report uncertainty ranges transparently."
        ],
        resolution_strategy="Apply sensitivity and probabilistic analysis; integrate with supporting data.",
        entity_scope="All reservoirs",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Porosity Partitioning - Effective vs Total Porosity",
        keywords=["porosity", "effective porosity", "total porosity", "shale effect", "log interpretation"],
        conclusion_template="Effective porosity is {effective_porosity}, total porosity is {total_porosity}, based on log and shale volume analysis.",
        reasoning_framework="""
Total porosity includes all pore space, while effective porosity excludes bound water in clays and non-connected pores. Effective porosity is more relevant for hydrocarbon production. Shale volume is estimated from gamma ray or spectral logs and used to correct total porosity. Integration of density, neutron, and NMR logs improves partitioning. Calibration with core data enhances accuracy.
""",
        key_factors=[
            "Shale volume estimation",
            "Porosity log integration",
            "Core calibration",
            "Bound water correction"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Porosity partitioning may be uncertain in complex lithologies.",
        counter_arguments=[
            "Use NMR and advanced logs.",
            "Calibrate with core data."
        ],
        resolution_strategy="Integrate multiple logs and calibrate with core for porosity partitioning.",
        entity_scope="All reservoirs",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Capillary Pressure and Height Functions from Logs",
        keywords=["capillary pressure", "height function", "log analysis", "hydrocarbon column", "reservoir modeling"],
        conclusion_template="Capillary pressure curve derived from log data indicates hydrocarbon column height of {height} ft.",
        reasoning_framework="""
Capillary pressure and height functions are estimated from log-derived porosity, permeability, and water saturation. Empirical relationships (e.g., Leverett J-function) relate log data to capillary pressure curves. These functions are used to estimate hydrocarbon column height and free water level. Calibration with core capillary pressure measurements improves accuracy. Integration with reservoir modeling supports volumetric estimation and field development.
""",
        key_factors=[
            "Porosity and permeability from logs",
            "Water saturation profile",
            "Empirical capillary pressure models",
            "Core calibration"
        ],
        primary_authority=[
            "Leverett, 1941",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Empirical models may not capture local reservoir heterogeneity.",
        counter_arguments=[
            "Calibrate with core capillary pressure data.",
            "Use reservoir modeling for validation."
        ],
        resolution_strategy="Apply empirical models with core calibration; integrate with reservoir models.",
        entity_scope="All reservoirs",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="Leverett, 1941"
    ),
    DoctrineBlock(
        topic="Mineral Volumetric Analysis from Logs",
        keywords=["mineral volumetric analysis", "log interpretation", "multi-mineral model", "lithology quantification"],
        conclusion_template="Mineral volumes estimated as: quartz {quartz_vol}%, calcite {calcite_vol}%, clay {clay_vol}% from log analysis.",
        reasoning_framework="""
Mineral volumetric analysis uses multi-mineral models (e.g., inverse modeling, crossplotting) to quantify mineral fractions from log data. Density, neutron, and spectral gamma ray logs provide inputs for solving mineral volume equations. Calibration with core and XRD data improves accuracy. Limitations include tool calibration errors and complex mineralogy. Integration with core and laboratory data is essential for reliable results.
""",
        key_factors=[
            "Log response for key minerals",
            "Multi-mineral model selection",
            "Calibration with core/XRD data",
            "Tool calibration"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Complex mineralogy and tool errors may limit accuracy.",
        counter_arguments=[
            "Use advanced models and core calibration.",
            "Apply statistical analysis for uncertainty."
        ],
        resolution_strategy="Integrate logs with core/XRD data; use advanced modeling.",
        entity_scope="All reservoirs",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Permeability Estimation from Logs",
        keywords=["permeability", "log analysis", "empirical models", "Coates equation", "Timur equation"],
        conclusion_template="Estimated permeability is {permeability} mD using the {model} model based on log-derived porosity and irreducible water saturation.",
        reasoning_framework="""
Permeability is estimated from logs using empirical models such as the Coates and Timur equations, which relate permeability to porosity and irreducible water saturation (Swirr). NMR logs provide direct input for these models. Calibration with core permeability measurements improves reliability. Limitations include heterogeneity and scale effects. Integration with core and production data supports reservoir modeling.
""",
        key_factors=[
            "Porosity and Swirr from logs",
            "Model selection (Coates, Timur)",
            "Core calibration",
            "Heterogeneity"
        ],
        primary_authority=[
            "Coates et al., 1999",
            "Timur, 1968"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Empirical models may not be valid in all lithologies.",
        counter_arguments=[
            "Calibrate with core data.",
            "Use multiple models for comparison."
        ],
        resolution_strategy="Apply empirical models with core calibration; integrate with production data.",
        entity_scope="All reservoirs",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Coates et al., 1999"
    ),
    DoctrineBlock(
        topic="Reservoir Compartmentalization Detection via Logs",
        keywords=["reservoir compartmentalization", "log analysis", "pressure gradient", "fluid contacts", "faults"],
        conclusion_template="Reservoir compartmentalization indicated by pressure gradient changes and log signatures at {depth}.",
        reasoning_framework="""
Reservoir compartmentalization is detected by log signatures (e.g., abrupt changes in resistivity, porosity) and pressure gradient analysis. Fluid contacts and pressure data from MDT/RFT tools support identification of compartments. Integration with seismic and structural data confirms compartment boundaries. Compartmentalization impacts reservoir management and development planning.
""",
        key_factors=[
            "Log signature changes",
            "Pressure gradient data",
            "Fluid contact identification",
            "Integration with seismic/structural data"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Log and pressure data may be ambiguous without supporting seismic data.",
        counter_arguments=[
            "Integrate with seismic and structural interpretation.",
            "Use multiple data types for confirmation."
        ],
        resolution_strategy="Combine log, pressure, and seismic data for compartmentalization analysis.",
        entity_scope="All reservoirs",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="Schlumberger, 2009"
    ),
    DoctrineBlock(
        topic="Reservoir Quality Index (RQI) and Flow Zone Indicator (FZI) from Logs",
        keywords=["RQI", "FZI", "reservoir quality", "log analysis", "flow units"],
        conclusion_template="RQI is {rqi}, FZI is {fzi}, indicating {flow_unit_type} flow unit in the reservoir.",
        reasoning_framework="""
RQI and FZI are calculated from log-derived porosity and permeability to characterize reservoir flow units. RQI = 0.0314 * sqrt(k/phi), FZI = RQI / (phi / (1-phi)). These indices help identify flow units and support reservoir modeling. Calibration with core and production data improves accuracy. Limitations include scale effects and log-derived permeability uncertainty.
""",
        key_factors=[
            "Porosity and permeability from logs",
            "RQI and FZI calculation",
            "Core and production data calibration",
            "Flow unit identification"
        ],
        primary_authority=[
            "Amaefule et al., 1993",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Log-derived permeability may be uncertain, affecting RQI/FZI accuracy.",
        counter_arguments=[
            "Calibrate with core and production data.",
            "Use multiple indices for flow unit analysis."
        ],
        resolution_strategy="Integrate log, core, and production data for RQI/FZI calculation.",
        entity_scope="All reservoirs",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Amaefule et al., 1993"
    ),
    DoctrineBlock(
        topic="Salinity Estimation from Logs",
        keywords=["salinity", "log analysis", "formation water", "SP log", "resistivity"],
        conclusion_template="Formation water salinity estimated as {salinity} ppm using SP and resistivity logs.",
        reasoning_framework="""
Formation water salinity is estimated from SP and resistivity logs using empirical relationships. SP log deflection is related to salinity contrast between formation water and mud filtrate. Resistivity logs provide input for water resistivity (Rw) estimation, which is then converted to salinity using standard charts or equations. Calibration with water samples improves reliability. Limitations include oil-based muds and complex salinity profiles.
""",
        key_factors=[
            "SP log response",
            "Resistivity-derived Rw",
            "Empirical salinity equations",
            "Water sample calibration"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="SP log is unreliable in oil-based muds or thin beds.",
        counter_arguments=[
            "Use resistivity and water sample data.",
            "Apply corrections for mud type and bed thickness."
        ],
        resolution_strategy="Integrate SP, resistivity, and water sample data for salinity estimation.",
        entity_scope="All reservoirs",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Hydrocarbon Typing from Logs",
        keywords=["hydrocarbon typing", "log analysis", "gas", "oil", "fluid identification"],
        conclusion_template="Log analysis indicates presence of {hydrocarbon_type} based on {log_signature}.",
        reasoning_framework="""
Hydrocarbon type is inferred from log signatures such as density-neutron separation (gas effect), resistivity response, and NMR T2 distribution. Gas zones show density-neutron crossover and low hydrogen index. Oil zones have high resistivity and characteristic NMR signatures. Integration with mud log gas shows and core data improves reliability. Limitations include shaliness and tool calibration errors.
""",
        key_factors=[
            "Density-neutron separation",
            "Resistivity response",
            "NMR T2 distribution",
            "Integration with mud log/core data"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Shaliness and calibration errors may confound hydrocarbon typing.",
        counter_arguments=[
            "Apply shale corrections.",
            "Integrate with core and mud log data."
        ],
        resolution_strategy="Use multi-log integration and corrections for hydrocarbon typing.",
        entity_scope="All reservoirs",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Overpressure Detection via Logs",
        keywords=["overpressure", "log analysis", "pressure gradient", "sonic log", "drilling safety"],
        conclusion_template="Overpressure detected at {depth} ft based on {log_signature} and pressure gradient analysis.",
        reasoning_framework="""
Overpressure is detected by log signatures such as abrupt decreases in sonic velocity, high resistivity, and abnormal drilling parameters. Sonic logs show increased travel time in overpressured shales. Pressure gradient analysis from MDT/RFT tools confirms overpressure zones. Early detection is critical for drilling safety and well control. Integration with seismic and mud logging data improves reliability.
""",
        key_factors=[
            "Sonic log response",
            "Resistivity anomalies",
            "Pressure gradient data",
            "Integration with drilling/seismic data"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Drilling engineer",
        adversary_position="Log signatures may be ambiguous without supporting pressure data.",
        counter_arguments=[
            "Integrate with pressure and drilling data.",
            "Use multiple indicators for confirmation."
        ],
        resolution_strategy="Combine log, pressure, and drilling data for overpressure detection.",
        entity_scope="All wells",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 53, 2007"
    ),
    DoctrineBlock(
        topic="Shale Brittleness Index from Logs",
        keywords=["shale brittleness", "brittleness index", "log analysis", "mechanical properties", "completion design"],
        conclusion_template="Shale brittleness index is {brittleness_index} based on log-derived mineralogy and mechanical properties.",
        reasoning_framework="""
Shale brittleness is estimated from log-derived mineralogy (e.g., quartz, carbonate, clay content) and mechanical properties (Young's modulus, Poisson's ratio). Brittleness index guides completion design and hydraulic fracturing. Logs used include density, sonic, and spectral gamma ray. Calibration with core mechanical tests improves accuracy. Limitations include log resolution and mineralogical complexity.
""",
        key_factors=[
            "Mineralogy from logs",
            "Mechanical property calculation",
            "Core calibration",
            "Integration with completion design"
        ],
        primary_authority=[
            "Rickman et al., 2008",
            "USGS, 2016"
        ],
        burden_holder="Completion engineer",
        adversary_position="Complex mineralogy may limit brittleness estimation accuracy.",
        counter_arguments=[
            "Calibrate with core mechanical tests.",
            "Use advanced log interpretation techniques."
        ],
        resolution_strategy="Integrate logs with core data for brittleness estimation.",
        entity_scope="Shale reservoirs",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Rickman et al., 2008"
    ),
    DoctrineBlock(
        topic="Organic-Rich Interval Identification from Logs",
        keywords=["organic-rich interval", "log analysis", "TOC", "source rock", "gamma ray"],
        conclusion_template="Organic-rich interval identified from {depth_start} to {depth_end} ft based on TOC > {toc_cutoff}%.",
        reasoning_framework="""
Organic-rich intervals are identified using log-derived TOC (Passey method), high gamma ray, and resistivity response. Integration with core and geochemical data confirms source rock potential. Cutoff selection for TOC is based on regional studies and production history. These intervals are targets for unconventional resource development.
""",
        key_factors=[
            "TOC estimation",
            "Gamma ray response",
            "Core and geochemical calibration",
            "Cutoff selection"
        ],
        primary_authority=[
            "Passey et al., 1990",
            "USGS, 2016"
        ],
        burden_holder="Petrophysicist",
        adversary_position="TOC estimation from logs may be uncertain without core calibration.",
        counter_arguments=[
            "Calibrate with core and geochemical data.",
            "Use multiple log indicators."
        ],
        resolution_strategy="Integrate log, core, and geochemical data for interval identification.",
        entity_scope="Source rock intervals",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Passey et al., 1990"
    ),
    DoctrineBlock(
        topic="Fracture Porosity Estimation from Logs",
        keywords=["fracture porosity", "log analysis", "image log", "sonic log", "reservoir quality"],
        conclusion_template="Fracture porosity estimated as {fracture_porosity}% based on image and sonic log analysis.",
        reasoning_framework="""
Fracture porosity is estimated from image log fracture density and sonic log velocity anomalies. Image logs provide direct fracture counts and orientation. Sonic logs show increased travel time in fractured intervals. Integration with core and production data improves reliability. Limitations include tool resolution and borehole conditions.
""",
        key_factors=[
            "Image log fracture density",
            "Sonic log anomalies",
            "Core and production calibration",
            "Borehole conditions"
        ],
        primary_authority=[
            "Schlumberger, Log Interpretation Charts, 2009",
            "Asquith & Krygowski, 2004"
        ],
        burden_holder="Petrophysicist",
        adversary_position="Fracture porosity may be underestimated in poor image log conditions.",
        counter_arguments=[
            "Use multiple log types and core data.",
            "Apply corrections for borehole effects."
        ],
        resolution_strategy="Integrate image, sonic, and core data for fracture porosity estimation.",
        entity_scope="Fractured reservoirs",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 40, 1990"
    ),
    DoctrineBlock(
        topic="Reservoir Net Pay Mapping from Logs",
        keywords=["net pay mapping", "log analysis", "pay thickness", "formation evaluation", "mapping"],
        conclusion_template="Net pay map constructed using log-derived pay thickness with cutoff: porosity > {porosity_cutoff}, Sw < {sw_cutoff}.",
        reasoning_framework="""
Net pay mapping uses log-derived pay thickness across wells to construct reservoir maps. Consistent cutoff selection for porosity and Sw is critical. Integration with core, test, and production data refines mapping. GIS and reservoir modeling tools are used for map construction. Sensitivity analysis supports uncertainty quantification.
""",
        key_factors=[
            "Consistent log cutoffs",
            "Integration with core/test data",
            "GIS and modeling tools",
            "Uncertainty analysis"
        ],
        primary_authority=[
            "Asquith & Krygowski, 2004",
            "Schlumberger, Log Interpretation Charts, 2009"
        ],
        burden_holder="Reservoir engineer",
        adversary_position="Cutoff inconsistency and data gaps may affect map accuracy.",
        counter_arguments=[
            "Standardize cutoffs and integrate multiple data sources.",
            "Apply uncertainty analysis."
        ],
        resolution_strategy="Use standardized methodology and integrated data for net pay mapping.",
        entity_scope="All reservoirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 40, 1990"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search