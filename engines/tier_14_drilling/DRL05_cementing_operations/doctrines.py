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
        topic="API Cement Class Selection",
        keywords=["API", "cement class", "cementing", "standard", "classification", "API Spec 10A"],
        conclusion_template="The appropriate API cement class for the operation is {class}, ensuring compliance with API Spec 10A and operational requirements.",
        reasoning_framework=(
            "Selection of the API cement class is governed by the well conditions, including depth, temperature, "
            "pressure, and exposure to corrosive environments. The API Spec 10A provides standardized classes "
            "ranging from Class A to Class J, each tailored for specific operational parameters. The decision "
            "process involves matching the well's mechanical and chemical environment to the cement class properties, "
            "such as compressive strength, thickening time, and sulfate resistance. Consideration is also given "
            "to the compatibility with drilling fluids and additives. The reasoning follows a hierarchical evaluation "
            "starting with safety and integrity requirements, followed by economic and logistical factors."
        ),
        key_factors=[
            "Well depth and temperature",
            "Formation pressure and gradients",
            "Exposure to corrosive fluids",
            "Required compressive strength",
            "Compatibility with drilling fluids",
            "API Spec 10A classifications"
        ],
        primary_authority=[
            "API Spec 10A - Cementing Materials and Testing",
            "API Recommended Practice 10B-2",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Alternative cement classes may be proposed citing cost savings or availability, "
            "potentially compromising long-term well integrity."
        ),
        counter_arguments=[
            "Demonstrate that lower class cement does not meet mechanical or chemical requirements.",
            "Highlight risks of premature failure or contamination.",
            "Reference API standards mandating minimum class for given conditions."
        ],
        resolution_strategy=(
            "Conduct laboratory testing and simulations to validate cement class performance under "
            "expected downhole conditions, and obtain consensus from engineering and safety teams."
        ),
        entity_scope="Wellbore Cementing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API Spec 10A mandates minimum cement class based on well conditions."
    ),
    DoctrineBlock(
        topic="Cement Slurry Density Design",
        keywords=["cement slurry", "density", "design", "weight", "fluid column", "hydrostatic pressure"],
        conclusion_template="The cement slurry density is designed at {density} ppg to balance hydrostatic pressure and avoid formation fracturing or fluid influx.",
        reasoning_framework=(
            "Designing cement slurry density requires balancing the hydrostatic pressure exerted by the slurry "
            "against formation fracture gradients and pore pressures to prevent lost circulation or influx. "
            "The slurry must be heavy enough to provide zonal isolation and support casing, but not so heavy "
            "as to fracture the formation or cause mud contamination. The design process involves evaluating "
            "formation properties, mud weights, and anticipated pressure regimes. Adjustments are made considering "
            "temperature effects on slurry density and thickening time. The reasoning is iterative and involves "
            "risk assessment of under- or overbalanced conditions."
        ),
        key_factors=[
            "Formation fracture gradient",
            "Pore pressure",
            "Mud weight",
            "Slurry compressive strength",
            "Temperature and pressure downhole",
            "Additive effects on density"
        ],
        primary_authority=[
            "API RP 10B-2 - Recommended Practice for Testing Well Cements",
            "Halliburton Cementing Design Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Proposals to use slurry densities outside recommended ranges citing operational expediency or "
            "material availability."
        ),
        counter_arguments=[
            "Highlight risk of lost circulation or formation damage.",
            "Demonstrate potential for gas migration or fluid influx.",
            "Reference empirical data and case studies supporting density selection."
        ],
        resolution_strategy=(
            "Perform laboratory testing, pressure modeling, and consult formation evaluation data to optimize slurry density."
        ),
        entity_scope="Cement Slurry Formulation",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 guidelines on slurry density relative to formation gradients."
    ),
    DoctrineBlock(
        topic="Cement Additives - Retarders",
        keywords=["cement additives", "retarders", "thickening time", "set time", "temperature", "fluid loss control"],
        conclusion_template="Retarder additives are incorporated to achieve a thickening time of {thickening_time} minutes under anticipated downhole temperatures.",
        reasoning_framework=(
            "Retarder additives are critical in controlling the thickening time of cement slurry, especially in "
            "high-temperature wells where cement sets faster. The selection and dosage of retarders depend on "
            "expected downhole temperature, slurry composition, and required pump time. The reasoning includes "
            "understanding chemical interactions between retarders and cement hydration kinetics. Over-retardation "
            "can lead to insufficient early strength, while under-retardation risks premature setting and operational delays. "
            "Laboratory testing under simulated conditions is essential to validate retarder performance."
        ),
        key_factors=[
            "Downhole temperature",
            "Desired thickening time",
            "Cement composition",
            "Retarder chemical type and concentration",
            "Interaction with other additives",
            "Pump schedule and operational timing"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Cementing Additives Catalog",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Arguments against retarder use citing cost or additive compatibility concerns."
        ),
        counter_arguments=[
            "Demonstrate risks of premature setting and operational delays without retarders.",
            "Provide test data showing effective retarder performance.",
            "Highlight cost-benefit analysis favoring retarder use."
        ],
        resolution_strategy=(
            "Conduct laboratory thickening time tests at simulated temperatures and adjust retarder dosage accordingly."
        ),
        entity_scope="Cement Slurry Additive Design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API Spec 10A requirements for thickening time control."
    ),
    DoctrineBlock(
        topic="Cement Additives - Fluid Loss Control",
        keywords=["cement additives", "fluid loss control", "fluid loss reducers", "additives", "permeability"],
        conclusion_template="Fluid loss control additives are applied to limit slurry fluid loss to {fluid_loss_limit} mL/30 min, maintaining slurry integrity.",
        reasoning_framework=(
            "Fluid loss control additives reduce the rate at which water is lost from the cement slurry into the formation, "
            "which can cause premature setting, slurry dehydration, and poor zonal isolation. The selection of fluid loss reducers "
            "depends on formation permeability, slurry composition, and operational parameters. The reasoning involves balancing "
            "fluid loss reduction with maintaining pumpability and compressive strength. Excessive fluid loss control additives "
            "can adversely affect slurry rheology and set properties. Laboratory API fluid loss tests guide additive dosage."
        ),
        key_factors=[
            "Formation permeability",
            "Slurry composition",
            "Additive compatibility",
            "Desired fluid loss limit",
            "Impact on rheology and set time",
            "Downhole temperature and pressure"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Additives Catalog",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Claims that fluid loss additives are unnecessary or increase costs without operational benefit."
        ),
        counter_arguments=[
            "Show case histories where fluid loss caused cement failure.",
            "Present laboratory data demonstrating fluid loss reduction benefits.",
            "Explain long-term well integrity implications."
        ],
        resolution_strategy=(
            "Perform fluid loss testing and optimize additive dosage to meet operational and formation requirements."
        ),
        entity_scope="Cement Slurry Additive Design",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 fluid loss testing standards."
    ),
    DoctrineBlock(
        topic="Primary Cementing - Displacement Efficiency",
        keywords=["primary cementing", "displacement efficiency", "mud removal", "cement placement", "flow regime"],
        conclusion_template="Achieving displacement efficiency of {efficiency}% is critical to ensure mud removal and proper cement placement.",
        reasoning_framework=(
            "Displacement efficiency in primary cementing determines the extent to which drilling mud is removed from the annulus "
            "and replaced by cement slurry. High displacement efficiency reduces contamination and ensures good bonding. "
            "Factors influencing displacement include flow regime (laminar vs turbulent), rheology of mud and cement slurry, "
            "annular geometry, and pump rates. The reasoning involves fluid mechanics principles, rheological compatibility, "
            "and operational sequencing. Computational fluid dynamics and lab tests can predict displacement outcomes."
        ),
        key_factors=[
            "Mud and slurry rheology",
            "Annular geometry",
            "Pump rate and pressure",
            "Flow regime",
            "Mud contamination potential",
            "Operational timing"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Schlumberger Cementing Manual",
            "Halliburton Cementing Guidelines"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Assertions that standard displacement procedures suffice without optimization."
        ),
        counter_arguments=[
            "Demonstrate risk of mud channeling and poor cement bonding.",
            "Provide data showing improved displacement techniques enhance well integrity.",
            "Reference case studies of displacement failures."
        ],
        resolution_strategy=(
            "Use rheology measurements, displacement modeling, and field monitoring to optimize displacement parameters."
        ),
        entity_scope="Primary Cementing Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 recommendations on cement displacement."
    ),
    DoctrineBlock(
        topic="Cement Bond Log (CBL) Interpretation",
        keywords=["cement bond log", "CBL", "bond quality", "acoustic log", "cement evaluation"],
        conclusion_template="CBL data indicates {bond_quality} bonding quality between casing and formation.",
        reasoning_framework=(
            "Cement Bond Logs utilize acoustic signals to evaluate the integrity of the cement sheath around casing. "
            "Interpretation involves analyzing amplitude and travel time of acoustic waves to infer bonding quality. "
            "Good bonding attenuates casing signals and increases acoustic impedance, while poor bonding results in high amplitude signals. "
            "The reasoning includes understanding tool calibration, formation effects, and signal processing. "
            "Interpretation must consider wellbore conditions, tool centralization, and presence of microannuli or channels."
        ),
        key_factors=[
            "Acoustic signal amplitude",
            "Travel time and waveform",
            "Tool centralization",
            "Formation lithology",
            "Casing condition",
            "Presence of microannuli or channels"
        ],
        primary_authority=[
            "Schlumberger CBL Interpretation Manual",
            "API RP 10B-2",
            "Halliburton Cementing Evaluation Guidelines"
        ],
        burden_holder="Logging Engineer",
        adversary_position=(
            "Skepticism regarding CBL accuracy due to tool limitations or formation effects."
        ),
        counter_arguments=[
            "Correlate CBL data with other logs and pressure tests.",
            "Demonstrate calibration and quality control procedures.",
            "Use multiple runs and tool types for confirmation."
        ],
        resolution_strategy=(
            "Integrate CBL interpretation with other cement evaluation methods and operational data."
        ),
        entity_scope="Cement Evaluation",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Industry standards for CBL interpretation and validation."
    ),
    DoctrineBlock(
        topic="Remedial Cementing - Squeeze Operations",
        keywords=["remedial cementing", "squeeze cementing", "cement squeeze", "well integrity", "leak repair"],
        conclusion_template="Squeeze cementing is executed with a volume of {volume} bbls at a pressure of {pressure} psi to remediate identified leaks.",
        reasoning_framework=(
            "Squeeze cementing is a remedial operation designed to seal leaks or channels behind casing by injecting cement slurry "
            "under pressure into the affected zones. The operation requires precise volume and pressure control to ensure cement "
            "penetrates the leak path without fracturing the formation. The reasoning involves diagnosis of leak location, "
            "selection of appropriate slurry design, and pressure monitoring. Risks include formation damage, lost circulation, "
            "and incomplete sealing. Post-squeeze evaluation confirms success."
        ),
        key_factors=[
            "Leak location and size",
            "Formation fracture pressure",
            "Slurry volume and properties",
            "Injection pressure",
            "Wellbore configuration",
            "Post-operation evaluation"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Remedial Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Remedial Cementing Engineer",
        adversary_position=(
            "Arguments that squeeze operations are unnecessary or ineffective."
        ),
        counter_arguments=[
            "Present diagnostics confirming leak and need for squeeze.",
            "Show case studies of successful remedial cementing.",
            "Demonstrate risk of well integrity loss without remediation."
        ],
        resolution_strategy=(
            "Careful planning, pressure monitoring, and post-squeeze testing to ensure effective remediation."
        ),
        entity_scope="Remedial Cementing Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 guidelines on squeeze cementing."
    ),
    DoctrineBlock(
        topic="Gas Migration - Mechanisms and Prevention",
        keywords=["gas migration", "cementing", "gas influx", "microannulus", "pressure control"],
        conclusion_template="Preventive measures including optimized slurry design and displacement techniques reduce gas migration risk.",
        reasoning_framework=(
            "Gas migration occurs when gas channels through unset or poorly bonded cement, compromising well integrity. "
            "Mechanisms include microannulus formation, cement shrinkage, and inadequate displacement of drilling fluids. "
            "Prevention requires slurry designs with appropriate thickening time and compressive strength, effective mud removal, "
            "and pressure control during cementing. The reasoning involves understanding gas flow pathways, cement hydration, "
            "and operational parameters. Monitoring and contingency plans are essential."
        ),
        key_factors=[
            "Slurry thickening time",
            "Mud removal efficiency",
            "Cement compressive strength development",
            "Annulus pressure control",
            "Casing centralization",
            "Formation gas pressure"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Schlumberger Cementing Manual",
            "Halliburton Cementing Guidelines"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Claims that gas migration is unavoidable or unrelated to cementing practices."
        ),
        counter_arguments=[
            "Provide evidence linking cementing parameters to gas migration incidents.",
            "Demonstrate effectiveness of preventive measures.",
            "Reference industry best practices and standards."
        ],
        resolution_strategy=(
            "Implement rigorous slurry design, displacement procedures, and pressure monitoring to mitigate gas migration."
        ),
        entity_scope="Primary Cementing and Well Integrity",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 recommendations on gas migration prevention."
    ),
    DoctrineBlock(
        topic="Foamed Cement - Design and Application",
        keywords=["foamed cement", "cement design", "gas injection", "lightweight cement", "compressive strength"],
        conclusion_template="Foamed cement slurry is designed with a foam quality of {foam_quality}% to achieve a density of {density} ppg and required compressive strength.",
        reasoning_framework=(
            "Foamed cement incorporates gas bubbles into the slurry to reduce density while maintaining compressive strength, "
            "useful in low-pressure or weak formations. Design involves controlling foam quality, slurry composition, and stability. "
            "The reasoning includes balancing foam stability against pumpability and set characteristics. Gas injection rates, surfactants, "
            "and mixing equipment affect foam quality. Laboratory testing simulates downhole conditions to validate design. "
            "Application requires careful pressure and volume control to avoid formation damage or gas migration."
        ),
        key_factors=[
            "Foam quality (%)",
            "Slurry density",
            "Compressive strength",
            "Surfactant type and concentration",
            "Gas injection rate",
            "Downhole temperature and pressure"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Foamed Cement Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Concerns about foam stability and complexity of operations."
        ),
        counter_arguments=[
            "Present lab and field data demonstrating foam cement performance.",
            "Highlight benefits in specific well conditions.",
            "Address operational controls to mitigate risks."
        ],
        resolution_strategy=(
            "Comprehensive lab testing and field pilot programs to validate foamed cement designs."
        ),
        entity_scope="Specialty Cementing Operations",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="API Spec 10A and industry guidelines on foamed cement."
    ),
    DoctrineBlock(
        topic="HPHT Cementing - Challenges and Solutions",
        keywords=["HPHT", "high pressure high temperature", "cementing", "thickening time", "additives", "compressive strength"],
        conclusion_template="HPHT cement slurry design incorporates specialized additives to maintain thickening time and compressive strength under {temperature}°F and {pressure} psi conditions.",
        reasoning_framework=(
            "HPHT wells present challenges including accelerated cement hydration, increased fluid loss, and altered rheology. "
            "Specialized additives such as retarders, fluid loss agents, and dispersants are required to maintain slurry pumpability "
            "and set properties. The reasoning involves understanding chemical kinetics at elevated temperature and pressure, "
            "compatibility of additives, and mechanical stresses on set cement. Laboratory autoclave testing simulates downhole conditions. "
            "Operational procedures must adapt to shortened thickening times and potential for gas migration."
        ),
        key_factors=[
            "Downhole temperature and pressure",
            "Additive selection and dosage",
            "Slurry rheology",
            "Thickening time control",
            "Compressive strength development",
            "Fluid loss control"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton HPHT Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Skepticism regarding additive effectiveness or cost justification."
        ),
        counter_arguments=[
            "Provide autoclave test data and field case studies.",
            "Demonstrate risk mitigation and well integrity benefits.",
            "Highlight regulatory and safety requirements."
        ],
        resolution_strategy=(
            "Rigorous lab testing, field trials, and continuous monitoring during HPHT cementing operations."
        ),
        entity_scope="HPHT Well Cementing",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="API Spec 10A and industry HPHT cementing standards."
    ),
    DoctrineBlock(
        topic="Lost Circulation During Cementing",
        keywords=["lost circulation", "cementing", "formation fracture", "fluid loss", "pressure control"],
        conclusion_template="Lost circulation is mitigated by adjusting slurry density to {density} ppg and using lost circulation materials (LCMs).",
        reasoning_framework=(
            "Lost circulation occurs when cement slurry or drilling fluids are lost to formation fractures or highly permeable zones. "
            "It compromises cement placement and well control. Prevention involves managing slurry density to avoid exceeding formation fracture pressure, "
            "using LCMs to seal fractures, and controlling pump rates and pressures. The reasoning includes understanding formation properties, "
            "pressure gradients, and slurry rheology. Real-time monitoring and contingency plans are essential to respond to losses."
        ),
        key_factors=[
            "Formation fracture gradient",
            "Slurry density",
            "Use of lost circulation materials",
            "Pump rate and pressure",
            "Formation permeability",
            "Wellbore geometry"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Lost Circulation Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Claims that lost circulation is unavoidable or not related to cement slurry design."
        ),
        counter_arguments=[
            "Demonstrate correlation between slurry parameters and lost circulation incidents.",
            "Show effectiveness of LCMs and operational controls.",
            "Reference case studies and best practices."
        ],
        resolution_strategy=(
            "Pre-job planning, slurry design optimization, and real-time pressure monitoring to prevent and manage lost circulation."
        ),
        entity_scope="Cementing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 recommendations on lost circulation control."
    ),
    DoctrineBlock(
        topic="Two-Plug Cementing Method",
        keywords=["two-plug method", "cementing", "bottom plug", "top plug", "displacement", "well control"],
        conclusion_template="The two-plug method is employed with bottom and top plugs to ensure effective cement displacement and well control.",
        reasoning_framework=(
            "The two-plug cementing method uses a bottom plug to separate drilling fluid from cement slurry and a top plug to separate cement from displacement fluid. "
            "This method prevents contamination and ensures positive displacement of cement. The reasoning involves understanding plug design, sequencing, and pressure monitoring. "
            "Proper plug landing and pressure signatures confirm plug positions. The method enhances well control and cement integrity."
        ),
        key_factors=[
            "Plug design and materials",
            "Sequencing of plugs and fluids",
            "Pressure monitoring and interpretation",
            "Wellbore geometry",
            "Pump rates and volumes",
            "Operational procedures"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Cementing Procedures",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Arguments favoring single-plug or alternative methods citing simplicity."
        ),
        counter_arguments=[
            "Demonstrate contamination risks without two-plug method.",
            "Provide operational data supporting two-plug effectiveness.",
            "Highlight regulatory and safety standards."
        ],
        resolution_strategy=(
            "Strict adherence to two-plug procedures with training and pressure monitoring."
        ),
        entity_scope="Primary Cementing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API Spec 10A requirements for two-plug cementing."
    ),
    DoctrineBlock(
        topic="Liner Cementing with DV Tool",
        keywords=["liner cementing", "DV tool", "differential valve", "cement placement", "well integrity"],
        conclusion_template="Use of the DV tool in liner cementing ensures controlled cement placement and pressure isolation.",
        reasoning_framework=(
            "The Differential Valve (DV) tool is used in liner cementing to isolate annular pressure and control cement placement. "
            "It allows pressure equalization and prevents backflow during cementing. The reasoning involves understanding tool mechanics, "
            "pressure regimes, and cement slurry behavior. Proper use of the DV tool improves cement integrity and reduces risks of channeling."
        ),
        key_factors=[
            "Tool design and operation",
            "Annular pressure management",
            "Cement slurry properties",
            "Liner geometry",
            "Operational sequencing",
            "Pressure monitoring"
        ],
        primary_authority=[
            "Halliburton Liner Cementing Guidelines",
            "Schlumberger Cementing Manual",
            "API RP 10B-2"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Concerns about tool reliability or complexity."
        ),
        counter_arguments=[
            "Provide operational data demonstrating DV tool effectiveness.",
            "Highlight safety and integrity benefits.",
            "Address maintenance and training requirements."
        ],
        resolution_strategy=(
            "Comprehensive training, tool maintenance, and monitoring during liner cementing."
        ),
        entity_scope="Liner Cementing Operations",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Industry standards on DV tool use in liner cementing."
    ),
    DoctrineBlock(
        topic="Cement Contamination - Mud/Cement Mixing",
        keywords=["cement contamination", "mud contamination", "cement slurry", "fluid compatibility", "zonal isolation"],
        conclusion_template="Preventing mud contamination during cement mixing is essential to maintain slurry properties and zonal isolation.",
        reasoning_framework=(
            "Mud contamination occurs when drilling fluids mix with cement slurry, altering its rheology, thickening time, and strength. "
            "This compromises zonal isolation and well integrity. Prevention involves proper displacement techniques, fluid compatibility analysis, "
            "and operational controls. The reasoning includes understanding chemical interactions, slurry testing, and monitoring during mixing. "
            "Contaminated cement requires remedial actions or slurry redesign."
        ),
        key_factors=[
            "Fluid compatibility",
            "Displacement efficiency",
            "Slurry rheology",
            "Operational procedures",
            "Monitoring and testing",
            "Additive interactions"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Claims that contamination is negligible or unavoidable."
        ),
        counter_arguments=[
            "Demonstrate impact of contamination on cement properties.",
            "Provide case studies of failure due to contamination.",
            "Recommend best practices for prevention."
        ],
        resolution_strategy=(
            "Implement strict displacement and mixing protocols with real-time monitoring."
        ),
        entity_scope="Cement Slurry Preparation",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 guidelines on fluid compatibility."
    ),
    DoctrineBlock(
        topic="Free Water and Cement Settling",
        keywords=["free water", "cement settling", "slurry stability", "fluid separation", "cement integrity"],
        conclusion_template="Slurry design minimizes free water and settling to maintain homogeneity and cement integrity.",
        reasoning_framework=(
            "Free water and cement settling occur when water separates from the slurry or cement particles settle, leading to heterogeneous cement placement. "
            "This affects compressive strength and zonal isolation. The reasoning involves slurry rheology, additive selection, and temperature effects. "
            "Additives such as dispersants and stabilizers reduce settling. Laboratory tests assess slurry stability under simulated conditions."
        ),
        key_factors=[
            "Slurry rheology",
            "Additive selection",
            "Temperature and pressure",
            "Mixing procedures",
            "Time before placement",
            "Downhole conditions"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Additives Catalog",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Arguments that free water and settling are minor issues."
        ),
        counter_arguments=[
            "Present data showing impact on cement strength and bonding.",
            "Recommend additive use and mixing protocols.",
            "Highlight long-term well integrity risks."
        ],
        resolution_strategy=(
            "Design slurry with appropriate additives and monitor slurry stability pre-placement."
        ),
        entity_scope="Cement Slurry Stability",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 recommendations on slurry stability."
    ),
    DoctrineBlock(
        topic="Thickening Time and API Schedules",
        keywords=["thickening time", "API schedules", "cement setting", "pump time", "temperature effects"],
        conclusion_template="Cement slurry thickening time is designed to meet API Schedule {schedule} requirements for operational timing.",
        reasoning_framework=(
            "Thickening time defines the period during which cement slurry remains pumpable before setting. API schedules classify thickening times "
            "to guide operations. Design considers temperature, slurry composition, and additives. The reasoning involves balancing operational needs "
            "with set time to avoid premature setting or excessive delays. Laboratory testing simulates downhole conditions to validate thickening time."
        ),
        key_factors=[
            "API thickening time schedules",
            "Downhole temperature",
            "Additive dosage",
            "Slurry composition",
            "Pump schedule",
            "Operational constraints"
        ],
        primary_authority=[
            "API Spec 10A",
            "API RP 10B-2",
            "Halliburton Cementing Guidelines"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Claims that thickening time requirements can be relaxed."
        ),
        counter_arguments=[
            "Demonstrate risks of operational delays or cement failure.",
            "Provide lab test data supporting schedule adherence.",
            "Highlight regulatory compliance."
        ],
        resolution_strategy=(
            "Design and test slurry to meet API thickening time schedules with contingency planning."
        ),
        entity_scope="Cement Slurry Design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API Spec 10A thickening time schedules."
    ),
    DoctrineBlock(
        topic="Cement Slurry Compressive Strength Development",
        keywords=["compressive strength", "cement slurry", "set time", "curing", "well integrity"],
        conclusion_template="Cement slurry achieves compressive strength of {strength} psi within {time} hours to ensure zonal isolation.",
        reasoning_framework=(
            "Compressive strength development is critical for cement to provide mechanical support and zonal isolation. "
            "Strength gain depends on slurry composition, curing temperature, and time. The reasoning involves hydration chemistry, "
            "laboratory curing tests, and downhole condition simulation. Insufficient strength can lead to casing collapse or fluid migration."
        ),
        key_factors=[
            "Slurry composition",
            "Curing temperature and pressure",
            "Additives",
            "Time to set",
            "Laboratory strength tests",
            "Downhole conditions"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Arguments that strength development is adequate without testing."
        ),
        counter_arguments=[
            "Present lab and field data confirming strength development.",
            "Highlight risks of insufficient strength.",
            "Recommend testing protocols."
        ],
        resolution_strategy=(
            "Conduct compressive strength testing under simulated conditions and adjust slurry design accordingly."
        ),
        entity_scope="Cement Slurry Performance",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 strength testing standards."
    ),
    DoctrineBlock(
        topic="Cement Hydration Chemistry",
        keywords=["cement hydration", "chemical reactions", "set time", "strength development", "additives"],
        conclusion_template="Understanding cement hydration chemistry guides additive selection and slurry design to optimize set time and strength.",
        reasoning_framework=(
            "Cement hydration involves exothermic chemical reactions between cement compounds and water, forming calcium silicate hydrates that provide strength. "
            "Additives influence reaction rates, set time, and final properties. The reasoning includes chemical kinetics, thermodynamics, and interaction effects. "
            "Optimizing hydration chemistry ensures slurry performance under varying downhole conditions."
        ),
        key_factors=[
            "Cement compound composition",
            "Water-to-cement ratio",
            "Additive chemistry",
            "Temperature and pressure",
            "Reaction kinetics",
            "Hydration products"
        ],
        primary_authority=[
            "API Spec 10A",
            "Cement Chemistry Texts",
            "Halliburton Cementing Guidelines"
        ],
        burden_holder="Cement Chemist",
        adversary_position=(
            "Simplistic slurry design ignoring chemical interactions."
        ),
        counter_arguments=[
            "Provide chemical analysis and lab test results.",
            "Demonstrate performance improvements with optimized chemistry.",
            "Highlight failure cases due to poor chemistry."
        ],
        resolution_strategy=(
            "Integrate chemical analysis with slurry design and testing."
        ),
        entity_scope="Cement Slurry Chemistry",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API Spec 10A chemical requirements."
    ),
    DoctrineBlock(
        topic="Cement Slurry Rheology",
        keywords=["cement slurry", "rheology", "viscosity", "yield point", "flow behavior"],
        conclusion_template="Slurry rheology is optimized to maintain pumpability and effective displacement under operational conditions.",
        reasoning_framework=(
            "Rheology defines the flow behavior of cement slurry, impacting pump pressures, displacement efficiency, and contamination risk. "
            "Parameters such as plastic viscosity and yield point are measured and adjusted via additives. The reasoning involves fluid mechanics, "
            "particle interactions, and temperature effects. Proper rheology ensures laminar flow and minimizes channeling."
        ),
        key_factors=[
            "Plastic viscosity",
            "Yield point",
            "Temperature",
            "Additive effects",
            "Pump rates",
            "Annular geometry"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Neglecting rheology adjustments leading to operational issues."
        ),
        counter_arguments=[
            "Present rheology test data and operational outcomes.",
            "Demonstrate benefits of rheology optimization.",
            "Recommend testing and monitoring protocols."
        ],
        resolution_strategy=(
            "Regular rheology testing and adjustment of slurry design pre-job."
        ),
        entity_scope="Cement Slurry Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 rheology testing standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Thickening Time Testing",
        keywords=["thickening time", "testing", "API schedule", "temperature simulation", "pressure simulation"],
        conclusion_template="Thickening time testing under simulated downhole conditions confirms slurry meets API Schedule {schedule} requirements.",
        reasoning_framework=(
            "Thickening time testing simulates downhole temperature and pressure to determine pumpability window of cement slurry. "
            "Tests follow API RP 10B-2 procedures using consistometers. The reasoning involves replicating field conditions to validate slurry design. "
            "Results guide additive dosage and operational timing."
        ),
        key_factors=[
            "Temperature simulation",
            "Pressure simulation",
            "Additive dosage",
            "Slurry composition",
            "API schedule requirements",
            "Testing equipment calibration"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Skipping or minimizing thickening time testing."
        ),
        counter_arguments=[
            "Highlight risks of premature setting or operational delays.",
            "Provide test data supporting design.",
            "Recommend adherence to API standards."
        ],
        resolution_strategy=(
            "Conduct thorough thickening time testing pre-job and adjust slurry design accordingly."
        ),
        entity_scope="Cement Slurry Testing",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 thickening time testing procedures."
    ),
    DoctrineBlock(
        topic="Cement Slurry Fluid Loss Testing",
        keywords=["fluid loss", "testing", "API RP 10B-2", "permeability", "slurry stability"],
        conclusion_template="Fluid loss testing confirms slurry fluid loss is within {fluid_loss_limit} mL/30 min to maintain slurry integrity.",
        reasoning_framework=(
            "Fluid loss testing measures the volume of water lost from slurry under pressure over time, simulating formation conditions. "
            "Tests follow API RP 10B-2 procedures. The reasoning includes evaluating additive effectiveness and slurry composition. "
            "Results influence additive dosage and slurry design to prevent dehydration and maintain set properties."
        ),
        key_factors=[
            "Test pressure and temperature",
            "Additive dosage",
            "Slurry composition",
            "API fluid loss limits",
            "Testing equipment calibration",
            "Formation permeability"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Ignoring fluid loss testing or relying on default values."
        ),
        counter_arguments=[
            "Demonstrate impact of fluid loss on cement performance.",
            "Provide test data supporting slurry design.",
            "Recommend compliance with API standards."
        ],
        resolution_strategy=(
            "Perform fluid loss testing and optimize slurry design pre-job."
        ),
        entity_scope="Cement Slurry Testing",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 fluid loss testing standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Compatibility Testing",
        keywords=["compatibility", "cement slurry", "drilling fluid", "chemical interaction", "contamination"],
        conclusion_template="Compatibility testing confirms no adverse reactions between cement slurry and drilling fluids.",
        reasoning_framework=(
            "Compatibility testing assesses chemical and physical interactions between cement slurry and drilling fluids to prevent contamination. "
            "Tests include rheology, thickening time, and compressive strength evaluations. The reasoning involves identifying potential adverse reactions "
            "that degrade slurry performance. Results guide fluid selection and slurry design."
        ),
        key_factors=[
            "Drilling fluid composition",
            "Slurry composition",
            "Rheology changes",
            "Thickening time alterations",
            "Compressive strength impact",
            "Additive interactions"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Assuming compatibility without testing."
        ),
        counter_arguments=[
            "Present test data demonstrating compatibility or incompatibility.",
            "Highlight risks of contamination.",
            "Recommend testing protocols."
        ],
        resolution_strategy=(
            "Conduct compatibility testing pre-job and adjust fluids or slurry design accordingly."
        ),
        entity_scope="Cement Slurry Preparation",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 compatibility testing guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Mix Water Quality",
        keywords=["mix water", "cement slurry", "water quality", "contamination", "set properties"],
        conclusion_template="Mix water quality meets API standards to prevent contamination and ensure slurry performance.",
        reasoning_framework=(
            "Water used in cement slurry mixing must meet quality standards to avoid contamination that affects hydration and set properties. "
            "Parameters include salinity, pH, and presence of impurities. The reasoning involves chemical compatibility and impact on slurry rheology and strength. "
            "Water quality testing and treatment ensure compliance."
        ),
        key_factors=[
            "Salinity",
            "pH level",
            "Impurities and solids",
            "Microbial content",
            "Impact on hydration",
            "API water quality standards"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Using non-compliant water sources citing availability or cost."
        ),
        counter_arguments=[
            "Demonstrate risks of contamination and cement failure.",
            "Recommend water treatment options.",
            "Highlight regulatory requirements."
        ],
        resolution_strategy=(
            "Test and treat mix water to meet API standards before cement mixing."
        ),
        entity_scope="Cement Slurry Preparation",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API Spec 10A water quality requirements."
    ),
    DoctrineBlock(
        topic="Cement Slurry Mixing Procedures",
        keywords=["mixing", "cement slurry", "procedures", "equipment", "homogeneity"],
        conclusion_template="Adherence to standardized mixing procedures ensures slurry homogeneity and performance.",
        reasoning_framework=(
            "Proper mixing procedures ensure uniform slurry composition, preventing segregation and contamination. "
            "Procedures specify equipment, mixing times, sequence of additive addition, and quality control checks. "
            "The reasoning involves fluid mechanics, chemical interactions, and operational discipline."
        ),
        key_factors=[
            "Mixing equipment capabilities",
            "Sequence of additive addition",
            "Mixing time and speed",
            "Quality control measures",
            "Operator training",
            "Slurry homogeneity"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Deviations from standard procedures citing time constraints."
        ),
        counter_arguments=[
            "Demonstrate impact of improper mixing on slurry performance.",
            "Recommend training and supervision.",
            "Highlight operational risks."
        ],
        resolution_strategy=(
            "Implement standardized mixing procedures with monitoring and training."
        ),
        entity_scope="Cement Slurry Preparation",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 mixing procedure standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Pumping Procedures",
        keywords=["pumping", "cement slurry", "procedures", "pressure monitoring", "displacement"],
        conclusion_template="Following standardized pumping procedures with pressure monitoring ensures effective cement placement.",
        reasoning_framework=(
            "Pumping procedures define rates, pressures, and sequencing to place cement slurry effectively. "
            "Pressure monitoring detects anomalies indicating channeling or lost circulation. The reasoning involves fluid dynamics, "
            "wellbore geometry, and operational controls. Deviations can compromise cement integrity."
        ),
        key_factors=[
            "Pump rates",
            "Pressure monitoring",
            "Displacement volumes",
            "Annular geometry",
            "Operator training",
            "Contingency plans"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Ignoring pressure anomalies or deviating from procedures."
        ),
        counter_arguments=[
            "Highlight risks of poor cement placement.",
            "Recommend strict adherence and monitoring.",
            "Provide case studies."
        ],
        resolution_strategy=(
            "Enforce pumping procedures with real-time monitoring and trained personnel."
        ),
        entity_scope="Cementing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 pumping procedure standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Quality Control",
        keywords=["quality control", "cement slurry", "testing", "monitoring", "performance"],
        conclusion_template="Comprehensive quality control testing ensures cement slurry meets design specifications and performance criteria.",
        reasoning_framework=(
            "Quality control involves testing slurry properties such as density, rheology, thickening time, and compressive strength "
            "before and during cementing operations. The reasoning includes establishing acceptance criteria, monitoring deviations, "
            "and implementing corrective actions. Quality control ensures operational success and well integrity."
        ),
        key_factors=[
            "Density",
            "Rheology",
            "Thickening time",
            "Compressive strength",
            "Testing frequency",
            "Operator training"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Minimizing quality control efforts citing time or cost."
        ),
        counter_arguments=[
            "Demonstrate risks of poor quality control.",
            "Recommend testing protocols.",
            "Highlight regulatory requirements."
        ],
        resolution_strategy=(
            "Implement rigorous quality control with trained personnel and documented procedures."
        ),
        entity_scope="Cement Slurry Preparation and Placement",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 quality control standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Temperature Effects",
        keywords=["temperature", "cement slurry", "hydration", "thickening time", "strength development"],
        conclusion_template="Slurry design accounts for downhole temperature of {temperature}°F to optimize hydration and thickening time.",
        reasoning_framework=(
            "Temperature significantly affects cement hydration kinetics, thickening time, and strength development. "
            "Higher temperatures accelerate reactions, potentially causing premature setting. The reasoning involves adjusting additive dosages "
            "and slurry composition to compensate. Laboratory testing at simulated temperatures validates design."
        ),
        key_factors=[
            "Downhole temperature",
            "Additive dosage",
            "Slurry composition",
            "Hydration kinetics",
            "Thickening time",
            "Strength development"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Ignoring temperature effects in slurry design."
        ),
        counter_arguments=[
            "Present lab data showing temperature impact.",
            "Recommend design adjustments.",
            "Highlight operational risks."
        ],
        resolution_strategy=(
            "Conduct temperature simulation testing and adjust slurry design accordingly."
        ),
        entity_scope="Cement Slurry Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API Spec 10A temperature guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Pressure Effects",
        keywords=["pressure", "cement slurry", "hydration", "fluid loss", "set properties"],
        conclusion_template="Slurry design considers downhole pressure of {pressure} psi to ensure proper hydration and fluid loss control.",
        reasoning_framework=(
            "Pressure affects cement slurry hydration and fluid loss characteristics. Elevated pressures can alter pore structure and set properties. "
            "The reasoning involves simulating pressure conditions in laboratory tests and adjusting slurry design accordingly. "
            "Proper pressure consideration prevents premature setting and ensures cement integrity."
        ),
        key_factors=[
            "Downhole pressure",
            "Slurry composition",
            "Additive dosage",
            "Hydration kinetics",
            "Fluid loss control",
            "Set properties"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Neglecting pressure effects in slurry design."
        ),
        counter_arguments=[
            "Provide lab data demonstrating pressure impact.",
            "Recommend design adjustments.",
            "Highlight operational risks."
        ],
        resolution_strategy=(
            "Conduct pressure simulation testing and optimize slurry design."
        ),
        entity_scope="Cement Slurry Design",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API Spec 10A pressure guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Additive Compatibility",
        keywords=["additive compatibility", "cement slurry", "chemical interaction", "performance"],
        conclusion_template="Additive compatibility testing confirms no adverse interactions affecting slurry performance.",
        reasoning_framework=(
            "Additive compatibility ensures that combined chemicals do not react adversely, affecting slurry rheology, thickening time, or strength. "
            "Testing involves mixing additives in various sequences and concentrations, monitoring slurry properties. "
            "The reasoning includes chemical analysis and empirical testing."
        ),
        key_factors=[
            "Additive chemical properties",
            "Sequence of addition",
            "Concentration levels",
            "Slurry composition",
            "Rheology and thickening time",
            "Compressive strength"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Assuming additive compatibility without testing."
        ),
        counter_arguments=[
            "Provide test data demonstrating compatibility.",
            "Highlight risks of incompatibility.",
            "Recommend testing protocols."
        ],
        resolution_strategy=(
            "Conduct additive compatibility testing pre-job."
        ),
        entity_scope="Cement Slurry Additive Design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 additive compatibility guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Contamination Effects",
        keywords=["contamination", "cement slurry", "drilling fluid", "performance degradation"],
        conclusion_template="Contamination of cement slurry by drilling fluids degrades performance and must be prevented.",
        reasoning_framework=(
            "Contamination alters slurry rheology, thickening time, and strength, compromising cement integrity. "
            "The reasoning involves understanding chemical and physical interactions and their impact on slurry properties. "
            "Prevention requires effective displacement and fluid compatibility."
        ),
        key_factors=[
            "Type and amount of contaminant",
            "Slurry composition",
            "Rheology changes",
            "Thickening time alterations",
            "Compressive strength impact",
            "Displacement efficiency"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Underestimating contamination impact."
        ),
        counter_arguments=[
            "Present data on performance degradation.",
            "Recommend prevention measures.",
            "Highlight operational risks."
        ],
        resolution_strategy=(
            "Implement strict displacement and fluid compatibility protocols."
        ),
        entity_scope="Cement Slurry Preparation",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 contamination guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Pump Pressure Monitoring",
        keywords=["pump pressure", "cementing", "pressure monitoring", "well control", "anomaly detection"],
        conclusion_template="Continuous pump pressure monitoring detects anomalies indicative of cementing issues.",
        reasoning_framework=(
            "Monitoring pump pressure during cementing detects events such as lost circulation, channeling, or plug landing. "
            "Pressure trends and sudden changes inform operational decisions. The reasoning involves fluid mechanics and operational experience. "
            "Timely detection enables corrective actions to maintain well control and cement integrity."
        ),
        key_factors=[
            "Pump pressure trends",
            "Pressure spikes or drops",
            "Annular pressure",
            "Operational sequencing",
            "Operator training",
            "Instrumentation accuracy"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Ignoring pressure anomalies or inadequate monitoring."
        ),
        counter_arguments=[
            "Highlight risks of undetected cementing issues.",
            "Recommend monitoring protocols.",
            "Provide case studies."
        ],
        resolution_strategy=(
            "Implement continuous pressure monitoring with trained operators and alarms."
        ),
        entity_scope="Cementing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 pressure monitoring standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Annular Clearance Effects",
        keywords=["annular clearance", "cement slurry", "flow", "displacement efficiency", "channeling"],
        conclusion_template="Annular clearance is optimized to promote turbulent flow and maximize displacement efficiency.",
        reasoning_framework=(
            "Annular clearance affects flow regime during cement displacement. Larger clearances promote turbulent flow, enhancing mud removal. "
            "Narrow clearances may cause laminar flow and channeling. The reasoning involves fluid dynamics, rheology, and wellbore geometry. "
            "Design considers casing and formation dimensions to optimize slurry flow."
        ),
        key_factors=[
            "Annular geometry",
            "Slurry rheology",
            "Pump rates",
            "Flow regime",
            "Displacement efficiency",
            "Wellbore configuration"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Neglecting annular clearance effects."
        ),
        counter_arguments=[
            "Provide fluid dynamics analysis.",
            "Demonstrate impact on displacement efficiency.",
            "Recommend design adjustments."
        ],
        resolution_strategy=(
            "Model annular flow and adjust operational parameters accordingly."
        ),
        entity_scope="Cementing Operations",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 flow regime guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Centralization",
        keywords=["centralization", "cement slurry", "casing centralizer", "displacement efficiency", "channeling prevention"],
        conclusion_template="Proper casing centralization is essential to prevent channeling and ensure uniform cement placement.",
        reasoning_framework=(
            "Centralizers position casing centrally in the wellbore, promoting uniform annular clearance and slurry flow. "
            "This reduces channeling and improves displacement efficiency. The reasoning involves mechanical design, fluid flow, and operational practices. "
            "Selection and placement of centralizers depend on wellbore conditions and casing size."
        ),
        key_factors=[
            "Centralizer type and placement",
            "Annular clearance",
            "Slurry rheology",
            "Flow regime",
            "Wellbore geometry",
            "Operational procedures"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Minimizing centralizer use citing cost or complexity."
        ),
        counter_arguments=[
            "Demonstrate risks of channeling and poor cement bonding.",
            "Recommend centralizer placement strategies.",
            "Highlight operational benefits."
        ],
        resolution_strategy=(
            "Design and implement centralization plan based on well conditions."
        ),
        entity_scope="Cementing Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 centralization guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Volume Calculations",
        keywords=["slurry volume", "cementing", "annular volume", "excess volume", "displacement"],
        conclusion_template="Slurry volume is calculated to fill annular space with an excess of {excess_percentage}% to ensure complete displacement.",
        reasoning_framework=(
            "Accurate slurry volume calculation is critical to fill the annulus and compensate for losses or shrinkage. "
            "Calculations consider casing and formation geometry, displacement fluid volumes, and operational contingencies. "
            "The reasoning involves geometric computations and operational experience to determine appropriate excess."
        ),
        key_factors=[
            "Annular geometry",
            "Casing dimensions",
            "Displacement fluid volumes",
            "Shrinkage allowance",
            "Operational contingencies",
            "Measurement accuracy"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Underestimating slurry volume citing cost or logistics."
        ),
        counter_arguments=[
            "Highlight risks of incomplete cement placement.",
            "Recommend conservative volume calculations.",
            "Provide case studies."
        ],
        resolution_strategy=(
            "Perform detailed volume calculations with contingency allowances."
        ),
        entity_scope="Cementing Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 volume calculation standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Displacement Fluid Selection",
        keywords=["displacement fluid", "cementing", "fluid selection", "compatibility", "density"],
        conclusion_template="Displacement fluid is selected for compatibility with cement slurry and formation, with density of {density} ppg.",
        reasoning_framework=(
            "Displacement fluids push cement slurry into place and must be compatible chemically and physically. "
            "Selection considers density, rheology, and potential contamination effects. The reasoning involves fluid compatibility testing and operational constraints."
        ),
        key_factors=[
            "Fluid density",
            "Chemical compatibility",
            "Rheology",
            "Formation sensitivity",
            "Operational constraints",
            "Contamination risk"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Using incompatible displacement fluids citing availability."
        ),
        counter_arguments=[
            "Demonstrate contamination risks.",
            "Recommend compatible fluid options.",
            "Highlight operational benefits."
        ],
        resolution_strategy=(
            "Conduct compatibility testing and select appropriate displacement fluids."
        ),
        entity_scope="Cementing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 displacement fluid guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Hydration Heat Management",
        keywords=["hydration heat", "cement slurry", "temperature control", "thermal stress", "additives"],
        conclusion_template="Hydration heat is managed through slurry design and additives to minimize thermal stress and cracking.",
        reasoning_framework=(
            "Exothermic hydration reactions generate heat that can cause thermal stress and cracking in the cement sheath. "
            "Management involves slurry design with retarders, temperature control, and additives to moderate heat generation. "
            "The reasoning includes thermal modeling and laboratory testing."
        ),
        key_factors=[
            "Heat of hydration",
            "Additive selection",
            "Slurry composition",
            "Downhole temperature",
            "Thermal conductivity",
            "Curing conditions"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Ignoring hydration heat effects."
        ),
        counter_arguments=[
            "Present thermal modeling data.",
            "Recommend design adjustments.",
            "Highlight operational risks."
        ],
        resolution_strategy=(
            "Incorporate hydration heat management in slurry design and monitoring."
        ),
        entity_scope="Cement Slurry Design",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API Spec 10A hydration heat guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Set Time Control",
        keywords=["set time", "cement slurry", "additives", "temperature", "hydration"],
        conclusion_template="Set time is controlled through additive dosage and slurry design to meet operational requirements.",
        reasoning_framework=(
            "Set time defines when cement transitions from fluid to solid. Control is achieved by adjusting additives and slurry composition considering temperature and hydration kinetics. "
            "The reasoning involves balancing operational timing with cement performance."
        ),
        key_factors=[
            "Additive dosage",
            "Slurry composition",
            "Temperature",
            "Hydration kinetics",
            "Operational timing",
            "Laboratory testing"
        ],
        primary_authority=[
            "API Spec 10A",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Underestimating importance of set time control."
        ),
        counter_arguments=[
            "Provide test data and operational case studies.",
            "Recommend design protocols.",
            "Highlight risks of improper set time."
        ],
        resolution_strategy=(
            "Design slurry with controlled set time and validate with testing."
        ),
        entity_scope="Cement Slurry Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API Spec 10A set time guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Additive Dosage Optimization",
        keywords=["additive dosage", "cement slurry", "optimization", "performance", "cost"],
        conclusion_template="Additive dosages are optimized to balance slurry performance and cost-effectiveness.",
        reasoning_framework=(
            "Optimizing additive dosage ensures slurry meets performance criteria without unnecessary cost or adverse effects. "
            "The reasoning involves laboratory testing, performance evaluation, and economic analysis."
        ),
        key_factors=[
            "Additive performance",
            "Slurry properties",
            "Cost considerations",
            "Laboratory test results",
            "Operational requirements",
            "Compatibility"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Over- or under-dosing additives citing cost or availability."
        ),
        counter_arguments=[
            "Demonstrate performance impact of dosage variations.",
            "Recommend optimized dosage ranges.",
            "Highlight cost-benefit analysis."
        ],
        resolution_strategy=(
            "Conduct systematic dosage testing and economic evaluation."
        ),
        entity_scope="Cement Slurry Additive Design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 additive dosage guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Displacement Efficiency Monitoring",
        keywords=["displacement efficiency", "monitoring", "cementing", "real-time data", "quality assurance"],
        conclusion_template="Real-time monitoring of displacement efficiency ensures effective mud removal and cement placement.",
        reasoning_framework=(
            "Monitoring displacement efficiency during cementing uses pressure data, flow rates, and other indicators to assess mud removal. "
            "Real-time data enables adjustments to operations to improve cement placement. The reasoning involves fluid dynamics and operational control."
        ),
        key_factors=[
            "Pressure data",
            "Flow rates",
            "Operational sequencing",
            "Annular geometry",
            "Slurry rheology",
            "Operator training"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Halliburton Cementing Guidelines",
            "Schlumberger Cementing Manual"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Neglecting real-time monitoring citing complexity."
        ),
        counter_arguments=[
            "Demonstrate benefits of monitoring.",
            "Recommend monitoring technologies.",
            "Provide case studies."
        ],
        resolution_strategy=(
            "Implement real-time monitoring systems with trained personnel."
        ),
        entity_scope="Cementing Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 monitoring guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Environmental Considerations",
        keywords=["environmental impact", "cement slurry", "additives", "disposal", "regulations"],
        conclusion_template="Cement slurry design and operations comply with environmental regulations to minimize impact.",
        reasoning_framework=(
            "Environmental considerations include additive toxicity, slurry disposal, and spill prevention. "
            "Design and operational procedures comply with regulations and best practices to minimize environmental footprint."
        ),
        key_factors=[
            "Additive toxicity",
            "Disposal methods",
            "Spill prevention",
            "Regulatory compliance",
            "Operational procedures",
            "Environmental monitoring"
        ],
        primary_authority=[
            "EPA regulations",
            "API environmental guidelines",
            "Local regulatory bodies"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Minimizing environmental controls citing cost."
        ),
        counter_arguments=[
            "Highlight regulatory risks and penalties.",
            "Recommend best practices.",
            "Provide environmental impact assessments."
        ],
        resolution_strategy=(
            "Implement environmental management plans and compliance monitoring."
        ),
        entity_scope="Cementing Operations",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="EPA and API environmental regulations."
    ),
    DoctrineBlock(
        topic="Cement Slurry Safety Procedures",
        keywords=["safety", "cement slurry", "operations", "hazard management", "training"],
        conclusion_template="Safety procedures are enforced during cement slurry operations to protect personnel and equipment.",
        reasoning_framework=(
            "Safety procedures address hazards such as high pressure, chemical exposure, and equipment operation. "
            "Training, personal protective equipment, and emergency response plans are integral. The reasoning involves risk assessment and mitigation."
        ),
        key_factors=[
            "Hazard identification",
            "Training programs",
            "Personal protective equipment",
            "Emergency response",
            "Operational controls",
            "Incident reporting"
        ],
        primary_authority=[
            "OSHA regulations",
            "API safety guidelines",
            "Company safety policies"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Neglecting safety protocols citing operational pressure."
        ),
        counter_arguments=[
            "Highlight risks and regulatory requirements.",
            "Recommend safety training and audits.",
            "Provide incident case studies."
        ],
        resolution_strategy=(
            "Enforce safety management systems and continuous training."
        ),
        entity_scope="Cementing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OSHA and API safety regulations."
    ),
    DoctrineBlock(
        topic="Cement Slurry Documentation and Reporting",
        keywords=["documentation", "reporting", "cement slurry", "quality assurance", "regulatory compliance"],
        conclusion_template="Comprehensive documentation and reporting ensure traceability and compliance in cement slurry operations.",
        reasoning_framework=(
            "Documentation includes slurry design, testing results, operational parameters, and quality control records. "
            "Reporting supports regulatory compliance and operational review. The reasoning involves establishing traceability and accountability."
        ),
        key_factors=[
            "Design records",
            "Test results",
            "Operational logs",
            "Quality control reports",
            "Regulatory requirements",
            "Data management"
        ],
        primary_authority=[
            "API RP 10B-2",
            "Company policies",
            "Regulatory bodies"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Inadequate documentation citing operational burden."
        ),
        counter_arguments=[
            "Highlight importance for compliance and quality.",
            "Recommend documentation standards.",
            "Provide audit results."
        ],
        resolution_strategy=(
            "Implement standardized documentation and reporting systems."
        ),
        entity_scope="Cementing Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 10B-2 documentation guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Training and Competency",
        keywords=["training", "competency", "cement slurry", "personnel", "operations"],
        conclusion_template="Personnel involved in cement slurry operations are trained and certified to ensure competency.",
        reasoning_framework=(
            "Training programs cover slurry design, mixing, pumping, safety, and quality control. Competency assessments ensure personnel capability. "
            "The reasoning involves risk management and operational excellence."
        ),
        key_factors=[
            "Training curricula",
            "Certification programs",
            "Competency assessments",
            "Continuous education",
            "Operational procedures",
            "Safety protocols"
        ],
        primary_authority=[
            "API training guidelines",
            "Company policies",
            "Industry best practices"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Insufficient training citing cost or time."
        ),
        counter_arguments=[
            "Highlight risks of untrained personnel.",
            "Recommend training investments.",
            "Provide incident analyses."
        ],
        resolution_strategy=(
            "Implement comprehensive training and certification programs."
        ),
        entity_scope="Cementing Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API training and competency standards."
    ),
    DoctrineBlock(
        topic="Cement Slurry Operational Risk Management",
        keywords=["risk management", "cement slurry", "operations", "hazard identification", "mitigation"],
        conclusion_template="Operational risks are identified and mitigated through structured risk management processes.",
        reasoning_framework=(
            "Risk management involves hazard identification, risk assessment, mitigation planning, and monitoring. "
            "The reasoning includes systematic evaluation of operational, safety, and environmental risks."
        ),
        key_factors=[
            "Hazard identification",
            "Risk assessment",
            "Mitigation strategies",
            "Monitoring and review",
            "Training",
            "Incident response"
        ],
        primary_authority=[
            "API RP 75",
            "Company risk management policies",
            "Industry best practices"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Underestimating operational risks."
        ),
        counter_arguments=[
            "Provide risk assessments and mitigation plans.",
            "Recommend continuous monitoring.",
            "Highlight incident case studies."
        ],
        resolution_strategy=(
            "Implement comprehensive risk management frameworks."
        ),
        entity_scope="Cementing Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 75 risk management guidelines."
    ),
    DoctrineBlock(
        topic="Cement Slurry Regulatory Compliance",
        keywords=["regulatory compliance", "cement slurry", "standards", "reporting", "audits"],
        conclusion_template="Operations comply with applicable regulatory standards and reporting requirements.",
        reasoning_framework=(
            "Compliance involves adherence to API, EPA, OSHA, and local regulations governing cement slurry design, operations, safety, and environmental impact. "
            "The reasoning includes understanding regulatory frameworks and implementing necessary controls."
        ),
        key_factors=[
            "Applicable regulations",
            "Operational procedures",
            "Documentation",
            "Training",
            "Audits and inspections",
            "Corrective actions"
        ],
        primary_authority=[
            "API standards",
            "EPA regulations",
            "OSHA regulations",
            "Local regulatory bodies"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Non-compliance citing operational constraints."
        ),
        counter_arguments=[
            "Highlight legal and financial risks.",
            "Recommend compliance programs.",
            "Provide audit results."
        ],
        resolution_strategy=(
            "Implement compliance management systems and continuous improvement."
        ),
        entity_scope="Cementing Operations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API, EPA, OSHA regulatory frameworks."
    ),
    DoctrineBlock(
        topic="Cement Slurry Continuous Improvement",
        keywords=["continuous improvement", "cement slurry", "operations", "feedback", "optimization"],
        conclusion_template="Continuous improvement processes optimize cement slurry operations through feedback and innovation.",
        reasoning_framework=(
            "Continuous improvement involves collecting operational data, analyzing performance, identifying issues, and implementing improvements. "
            "The reasoning includes feedback loops, innovation adoption, and performance metrics."
        ),
        key_factors=[
            "Operational data collection",
            "Performance analysis",
            "Issue identification",
            "Improvement implementation",
            "Training updates",
            "Innovation adoption"
        ],
        primary_authority=[
            "ISO 9001",
            "Company quality management systems",
            "Industry best practices"
        ],
        burden_holder="Cementing Engineer",
        adversary_position=(
            "Resistance to change citing tradition or cost."
        ),
        counter_arguments=[
            "Demonstrate benefits of improvements.",
            "Recommend structured processes.",
            "Provide success stories."
        ],
        resolution_strategy=(
            "Establish continuous improvement programs with management support."
        ),
        entity_scope="Cementing Operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 9001 quality management standards."
    ),
]


def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    topic_lower = topic.lower()
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic_lower:
            return doctrine
    return None


def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
            continue
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
            continue
        if keyword_lower in doctrine.reasoning_framework.lower():
            results.append(doctrine)
            continue
    return results


def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]