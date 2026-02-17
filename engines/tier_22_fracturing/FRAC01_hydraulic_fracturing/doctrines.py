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
        topic="Frac Design Fundamentals - Net Pressure and Closure Stress",
        keywords=["net pressure", "closure stress", "frac design", "hydraulic fracturing", "stress analysis"],
        conclusion_template="Net pressure must exceed closure stress to initiate and propagate a hydraulic fracture, but excessive net pressure can risk out-of-zone growth.",
        reasoning_framework=(
            "Net pressure is defined as the difference between the pressure inside the fracture and the minimum in-situ stress (closure stress) of the formation. "
            "Fracture initiation and propagation require that net pressure be positive and sufficient to overcome closure stress. "
            "However, excessive net pressure can drive the fracture into unintended zones or cause premature screenout. "
            "Designs should balance net pressure to optimize fracture geometry while minimizing risks. "
            "Closure stress is typically determined from diagnostic tests (e.g., mini-frac, DFIT) and core analysis. "
            "The interplay between net pressure and closure stress influences fracture height, length, and containment. "
            "Engineers must monitor treating pressure in real time and adjust pump rates or fluid viscosity to maintain optimal net pressure. "
            "The design must also account for stress contrasts between layers, which can act as barriers or conduits for fracture growth. "
            "Net pressure analysis is foundational for all subsequent treatment design decisions."
        ),
        key_factors=[
            "Accurate closure stress measurement",
            "Real-time pressure monitoring",
            "Formation stress contrasts",
            "Fluid and proppant selection",
            "Treatment schedule flexibility"
        ],
        primary_authority=[
            "Gidley, J.L. et al., 'Recent Advances in Hydraulic Fracturing', SPE Monograph Vol. 12",
            "Smith, M.B., 'Hydraulic Fracturing', SPE Textbook Series"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Net pressure can be reduced to minimize cost, regardless of closure stress.",
        counter_arguments=[
            "Insufficient net pressure leads to failed fracture initiation.",
            "Ignoring closure stress risks non-productive treatments.",
            "Cost savings are negated by poor stimulation results."
        ],
        resolution_strategy="Base net pressure targets on closure stress measurements and adjust in real time during treatment.",
        entity_scope="All unconventional and conventional reservoirs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SPE Monograph Vol. 12, Ch. 3"
    ),
    DoctrineBlock(
        topic="PKN vs KGD Fracture Geometry Models",
        keywords=["PKN", "KGD", "fracture geometry", "model selection", "hydraulic fracturing"],
        conclusion_template="PKN and KGD models are selected based on formation thickness and fracture height containment; PKN for tall, narrow fractures, KGD for short, wide fractures.",
        reasoning_framework=(
            "The PKN (Perkins-Kern-Nordgren) model assumes fracture height is constant and is best applied to formations where the fracture height is constrained by strong barriers, "
            "resulting in tall, narrow fractures. The KGD (Khristianovic-Geertsma-de Klerk) model assumes constant fracture width and is suitable for formations with limited height growth, "
            "producing short, wide fractures. Model selection is critical for accurate prediction of fracture dimensions, proppant placement, and fluid efficiency. "
            "The choice impacts treatment design, expected stimulated reservoir volume (SRV), and post-treatment production. "
            "Field diagnostics (e.g., microseismic, pressure analysis) can validate model assumptions. "
            "Hybrid or numerical models may be used when neither PKN nor KGD assumptions strictly apply."
        ),
        key_factors=[
            "Formation thickness",
            "Stress barriers",
            "Fracture height containment",
            "Diagnostic data",
            "Model validation"
        ],
        primary_authority=[
            "Perkins, T.K. and Kern, L.R., 'Width of Hydraulic Fractures', JPT, 1961",
            "Geertsma, J. and de Klerk, F., 'A Rapid Method of Predicting Width and Extent of Hydraulic-Fractured Layers', JPT, 1969"
        ],
        burden_holder="Frac Modeling Engineer",
        adversary_position="Either model can be used interchangeably without impact on design accuracy.",
        counter_arguments=[
            "Incorrect model selection leads to inaccurate fracture predictions.",
            "Mismatch between model and field conditions reduces treatment effectiveness."
        ],
        resolution_strategy="Select geometry model based on formation properties and validate with field data.",
        entity_scope="All hydraulic fracturing treatments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="JPT, 1961; JPT, 1969"
    ),
    DoctrineBlock(
        topic="Treatment Scheduling - Pad, Slurry Stages, Flush",
        keywords=["treatment schedule", "pad", "slurry", "flush", "staging"],
        conclusion_template="A standard treatment schedule consists of a pad stage to initiate fracture, slurry stages for proppant placement, and a flush to clear the wellbore.",
        reasoning_framework=(
            "Treatment scheduling is structured to optimize fracture initiation, proppant transport, and wellbore cleanup. "
            "The pad stage is a proppant-free fluid injection to open the fracture and establish geometry. "
            "Slurry stages introduce proppant-laden fluid to transport and place proppant within the fracture. "
            "The flush stage clears proppant from the wellbore, minimizing the risk of screenouts and facilitating flowback. "
            "Stage volumes, rates, and transitions are engineered based on formation properties, proppant type, and operational constraints. "
            "Real-time monitoring ensures stage effectiveness and allows for schedule adjustments as needed."
        ),
        key_factors=[
            "Pad volume and rate",
            "Slurry concentration and stage length",
            "Flush volume and timing",
            "Proppant transport efficiency",
            "Operational constraints"
        ],
        primary_authority=[
            "Economides, M.J. and Nolte, K.G., 'Reservoir Stimulation', 3rd Edition",
            "SPE Hydraulic Fracturing Technical Section"
        ],
        burden_holder="Frac Engineer",
        adversary_position="Skipping pad or flush stages reduces cost without impacting treatment effectiveness.",
        counter_arguments=[
            "Omitting pad can prevent proper fracture initiation.",
            "Skipping flush increases risk of wellbore blockage.",
            "Cost savings are offset by operational failures."
        ],
        resolution_strategy="Follow established scheduling protocols and adjust based on real-time data.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Reservoir Stimulation, 3rd Ed."
    ),
    DoctrineBlock(
        topic="Pump Rate Optimization for Fracture Geometry",
        keywords=["pump rate", "optimization", "fracture geometry", "treatment design"],
        conclusion_template="Pump rate should be optimized to balance fracture width, length, and height while preventing screenout and out-of-zone growth.",
        reasoning_framework=(
            "Pump rate directly influences fracture propagation, geometry, and proppant transport. "
            "Higher rates can increase fracture width and length but may risk out-of-zone growth or tip screenout. "
            "Lower rates may limit fracture dimensions and reduce proppant placement efficiency. "
            "Optimization involves modeling fracture response to various rates, considering formation permeability, stress profile, and fluid viscosity. "
            "Field diagnostics and real-time pressure monitoring inform rate adjustments during treatment. "
            "The goal is to maximize stimulated reservoir volume (SRV) and production while minimizing operational risks."
        ),
        key_factors=[
            "Formation permeability",
            "Stress profile",
            "Fluid viscosity",
            "Proppant transport",
            "Screenout risk"
        ],
        primary_authority=[
            "Smith, M.B., 'Hydraulic Fracturing', SPE Textbook Series",
            "Barree, R.D., 'A Practical Numerical Simulator for Fracturing Applications', SPE"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Maximum pump rates always yield the best fracture geometry.",
        counter_arguments=[
            "Excessive rates can cause out-of-zone growth.",
            "High rates increase risk of screenout.",
            "Optimal geometry depends on formation-specific factors."
        ],
        resolution_strategy="Model and monitor pump rates, adjusting in real time to optimize fracture geometry.",
        entity_scope="All hydraulic fracturing treatments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Hydraulic Fracturing, SPE Textbook Series"
    ),
    DoctrineBlock(
        topic="Formation Stress Profiling - Mini-Frac and DFIT Analysis",
        keywords=["formation stress", "profiling", "mini-frac", "DFIT", "closure stress"],
        conclusion_template="Mini-frac and DFIT tests are essential for accurate formation stress profiling, informing fracture design and containment strategies.",
        reasoning_framework=(
            "Formation stress profiling determines the minimum in-situ stress (closure stress) and is critical for fracture containment and design. "
            "Mini-frac tests involve injecting a small volume of fluid to create a short-lived fracture and monitoring pressure decline to estimate closure stress. "
            "Diagnostic Fracture Injection Tests (DFIT) use similar principles but focus on pressure transient analysis to derive stress and permeability. "
            "Accurate profiling ensures that fracture treatments are designed within containment limits, reducing the risk of out-of-zone growth. "
            "Data from these tests guide model selection, pump rate, and fluid/proppant choices. "
            "Regular profiling is recommended in heterogeneous or evolving reservoirs."
        ),
        key_factors=[
            "Test execution quality",
            "Pressure decline analysis",
            "Formation heterogeneity",
            "Data interpretation",
            "Containment strategy"
        ],
        primary_authority=[
            "Warpinski, N.R., 'Hydraulic Fracture Diagnostics', SPE Monograph",
            "SPE 39497, 'DFIT Analysis and Applications'"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Formation stress can be estimated from logs without field testing.",
        counter_arguments=[
            "Log-derived stress lacks field validation.",
            "DFIT/mini-frac provides direct, formation-specific data.",
            "Design errors increase without accurate stress profiling."
        ],
        resolution_strategy="Conduct mini-frac and DFIT tests prior to treatment design.",
        entity_scope="All unconventional and complex reservoirs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SPE Monograph; SPE 39497"
    ),
    DoctrineBlock(
        topic="Fracture Height Containment and Stress Barriers",
        keywords=["fracture height", "containment", "stress barriers", "zonal isolation"],
        conclusion_template="Fracture height containment relies on natural or engineered stress barriers to prevent out-of-zone fracture growth.",
        reasoning_framework=(
            "Fracture height containment is essential for targeting stimulation to the productive zone and avoiding water or gas breakthrough. "
            "Stress barriers are layers with significantly higher or lower minimum in-situ stress compared to the target zone, acting as natural limits to fracture growth. "
            "Engineered barriers (e.g., cement, mechanical packers) can supplement natural containment. "
            "Containment is evaluated using log data, core analysis, and field diagnostics. "
            "Designs should avoid exceeding the stress contrast to maintain fracture within the desired interval. "
            "Inadequate containment can lead to poor production and operational hazards."
        ),
        key_factors=[
            "Stress contrast magnitude",
            "Barrier integrity",
            "Formation evaluation",
            "Treatment pressure control",
            "Containment diagnostics"
        ],
        primary_authority=[
            "Warpinski, N.R., 'Fracture Growth in Layered Rocks', SPE 15261",
            "Economides, M.J., 'Reservoir Stimulation', 3rd Edition"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Containment is unnecessary if production zone is thick.",
        counter_arguments=[
            "Uncontained fractures risk water/gas breakthrough.",
            "Production losses and operational risks increase.",
            "Containment is critical regardless of zone thickness."
        ],
        resolution_strategy="Assess and design for stress barriers in all treatments.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 15261"
    ),
    DoctrineBlock(
        topic="Fracture Conductivity Calculations and Proppant Pack Permeability",
        keywords=["fracture conductivity", "proppant pack", "permeability", "conductivity calculation"],
        conclusion_template="Fracture conductivity is determined by proppant pack permeability and width, directly impacting post-frac production.",
        reasoning_framework=(
            "Fracture conductivity is the product of proppant pack permeability and fracture width, normalized by fracture length. "
            "High conductivity ensures efficient hydrocarbon flow from the reservoir to the wellbore. "
            "Proppant type, size, and concentration influence pack permeability, which can be degraded by closure stress and fines migration. "
            "Conductivity calculations inform proppant selection and treatment design. "
            "Laboratory measurements and field data are used to calibrate models. "
            "Designs should target conductivity values that exceed reservoir permeability to maximize production."
        ),
        key_factors=[
            "Proppant type and size",
            "Closure stress effects",
            "Fines migration",
            "Fracture width",
            "Conductivity degradation"
        ],
        primary_authority=[
            "McDaniel, B.W. and Economides, M.J., 'Proppant Pack Conductivity', SPE 1690",
            "SPE Monograph Vol. 12"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Any proppant will provide sufficient conductivity.",
        counter_arguments=[
            "Proppant selection impacts conductivity under closure stress.",
            "Improper selection reduces post-frac production.",
            "Conductivity must be engineered, not assumed."
        ],
        resolution_strategy="Calculate and optimize conductivity for each treatment.",
        entity_scope="All propped fracture treatments",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 1690"
    ),
    DoctrineBlock(
        topic="Tip Screenout (TSO) Design for Maximum Proppant Placement",
        keywords=["tip screenout", "TSO", "proppant placement", "design"],
        conclusion_template="TSO treatments are intentionally designed to maximize proppant placement by causing controlled tip screenout and subsequent fracture extension.",
        reasoning_framework=(
            "Tip screenout (TSO) occurs when proppant bridges at the fracture tip, halting further extension and causing pressure to rise. "
            "TSO designs exploit this phenomenon to maximize proppant concentration and pack width near the wellbore. "
            "After screenout, continued pumping extends the fracture laterally, increasing conductivity. "
            "TSO treatments require careful control of pump rate, proppant concentration, and fluid viscosity to avoid uncontrolled screenout. "
            "Real-time monitoring is essential to detect onset and manage post-TSO extension. "
            "TSO is particularly beneficial in low-permeability or high-stress reservoirs."
        ),
        key_factors=[
            "Proppant concentration ramp",
            "Pump rate control",
            "Fluid viscosity",
            "Pressure monitoring",
            "Reservoir permeability"
        ],
        primary_authority=[
            "Barree, R.D. and Conway, M.W., 'Design and Evaluation of Tip Screenout Treatments', SPE 18245",
            "SPE Monograph Vol. 12"
        ],
        burden_holder="Frac Treatment Engineer",
        adversary_position="TSO should be avoided due to operational risks.",
        counter_arguments=[
            "Controlled TSO maximizes proppant placement.",
            "Proper design mitigates operational risks.",
            "TSO is essential in certain reservoir conditions."
        ],
        resolution_strategy="Design and monitor TSO treatments with robust controls.",
        entity_scope="Low-permeability and high-stress reservoirs",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 18245"
    ),
    DoctrineBlock(
        topic="Multi-Stage Completion Design - Plug-and-Perf vs Sliding Sleeve",
        keywords=["multi-stage", "completion", "plug-and-perf", "sliding sleeve", "design"],
        conclusion_template="Plug-and-perf offers greater stage selectivity and cluster density, while sliding sleeves provide operational efficiency but less flexibility.",
        reasoning_framework=(
            "Multi-stage completions enable stimulation of long horizontal wells. "
            "Plug-and-perf involves setting plugs and perforating casing at each stage, allowing precise stage and cluster selection. "
            "Sliding sleeves use mechanical or hydraulic sleeves to open pre-set ports, enabling rapid stage transitions but with fixed cluster locations. "
            "Plug-and-perf is preferred for complex or variable geology, while sliding sleeves are favored for operational speed and simplicity. "
            "The choice impacts stage count, cluster spacing, and overall stimulation effectiveness."
        ),
        key_factors=[
            "Stage selectivity",
            "Operational efficiency",
            "Cluster density",
            "Geological variability",
            "Cost"
        ],
        primary_authority=[
            "King, G.E., 'Multi-Stage Hydraulic Fracturing', JPT, 2010",
            "SPE 140669"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Sliding sleeves are always superior due to faster operations.",
        counter_arguments=[
            "Plug-and-perf allows for tailored stage design.",
            "Geological complexity may require selective stimulation.",
            "Operational speed must be balanced with effectiveness."
        ],
        resolution_strategy="Select completion method based on reservoir and operational requirements.",
        entity_scope="All multi-stage horizontal wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="JPT, 2010"
    ),
    DoctrineBlock(
        topic="Permian Basin Frac Designs - Wolfcamp, Bone Spring, Spraberry",
        keywords=["Permian Basin", "frac design", "Wolfcamp", "Bone Spring", "Spraberry"],
        conclusion_template="Frac designs in the Permian Basin are tailored to formation-specific properties, with Wolfcamp favoring high-intensity treatments and Bone Spring/Spraberry requiring containment strategies.",
        reasoning_framework=(
            "The Permian Basin encompasses multiple stacked formations with varying properties. "
            "Wolfcamp is characterized by thick, over-pressured shales and responds well to high-intensity, high-proppant treatments. "
            "Bone Spring and Spraberry are more heterogeneous, with variable stress barriers and fluid sensitivity, requiring careful height containment and fluid selection. "
            "Frac designs must account for local stress profiles, natural fracture networks, and parent-child well interactions. "
            "Operational practices are informed by extensive field data and ongoing diagnostics."
        ),
        key_factors=[
            "Formation thickness",
            "Stress barriers",
            "Fluid sensitivity",
            "Natural fractures",
            "Parent-child interactions"
        ],
        primary_authority=[
            "SPE 191372, 'Permian Basin Completion Optimization'",
            "King, G.E., 'Hydraulic Fracturing in the Permian', JPT, 2018"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="A single frac design can be applied across all Permian formations.",
        counter_arguments=[
            "Formation-specific properties require tailored designs.",
            "Uniform designs risk poor production and operational issues."
        ],
        resolution_strategy="Customize frac designs for each formation based on diagnostics.",
        entity_scope="Permian Basin horizontal wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 191372"
    ),
    DoctrineBlock(
        topic="Delaware Basin vs Midland Basin Frac Design Differences",
        keywords=["Delaware Basin", "Midland Basin", "frac design", "Permian Basin", "differences"],
        conclusion_template="Delaware Basin designs prioritize containment and fluid efficiency, while Midland Basin designs emphasize proppant intensity and cluster density.",
        reasoning_framework=(
            "The Delaware and Midland sub-basins of the Permian have distinct geological and operational characteristics. "
            "Delaware Basin features higher formation pressure, more variable stress barriers, and greater risk of out-of-zone growth, necessitating strong containment and fluid efficiency. "
            "Midland Basin is more uniform, allowing for higher proppant intensity and tighter cluster spacing. "
            "Frac designs must be adapted to local conditions, with diagnostics guiding fluid, proppant, and stage selection. "
            "Parent-child interactions and offset well protection are critical in both sub-basins."
        ),
        key_factors=[
            "Formation pressure",
            "Stress barrier variability",
            "Cluster spacing",
            "Proppant intensity",
            "Offset well interactions"
        ],
        primary_authority=[
            "SPE 191372",
            "JPT, 2018"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Designs can be transferred between sub-basins without modification.",
        counter_arguments=[
            "Geological differences require unique designs.",
            "Transferred designs may underperform or cause operational issues."
        ],
        resolution_strategy="Adapt designs to sub-basin-specific diagnostics and field data.",
        entity_scope="Permian Basin horizontal wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 191372"
    ),
    DoctrineBlock(
        topic="Frac Hit Mitigation and Parent-Child Well Interactions",
        keywords=["frac hit", "mitigation", "parent-child", "well interactions", "pressure communication"],
        conclusion_template="Frac hit mitigation strategies are essential to protect parent wells and optimize child well performance in infill development.",
        reasoning_framework=(
            "Frac hits occur when hydraulic fractures from a new (child) well communicate with an existing (parent) well, causing pressure and fluid migration. "
            "This can damage parent well productivity and compromise child well stimulation. "
            "Mitigation strategies include pre-loading parent wells, optimizing stage sequencing, and adjusting cluster spacing. "
            "Pressure monitoring and real-time diagnostics are used to detect and respond to frac hits. "
            "Field experience and modeling inform best practices for infill development."
        ),
        key_factors=[
            "Well spacing",
            "Stage sequencing",
            "Pressure monitoring",
            "Parent well pre-loading",
            "Cluster optimization"
        ],
        primary_authority=[
            "SPE 189880, 'Frac Hit Mitigation in the Permian'",
            "King, G.E., 'Parent-Child Well Interactions', JPT, 2019"
        ],
        burden_holder="Development Engineer",
        adversary_position="Frac hits are unavoidable and do not impact long-term production.",
        counter_arguments=[
            "Frac hits can permanently damage parent wells.",
            "Mitigation improves overall field recovery.",
            "Operational strategies can reduce frac hit frequency."
        ],
        resolution_strategy="Implement mitigation strategies and monitor in real time.",
        entity_scope="Infill development projects",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 189880"
    ),
    DoctrineBlock(
        topic="Stress Shadowing Effects on Multi-Stage Completions",
        keywords=["stress shadowing", "multi-stage", "completions", "hydraulic fracturing"],
        conclusion_template="Stress shadowing must be accounted for in multi-stage completions to ensure uniform fracture growth and effective stimulation.",
        reasoning_framework=(
            "Stress shadowing occurs when fractures from one stage alter the local stress field, affecting subsequent fracture propagation. "
            "This can lead to non-uniform fracture geometry, reduced cluster efficiency, and uneven proppant placement. "
            "Designs should optimize stage and cluster spacing to minimize shadowing effects. "
            "Numerical modeling and field diagnostics are used to predict and manage stress shadowing. "
            "Uniform stimulation is critical for maximizing stimulated reservoir volume (SRV) and production."
        ),
        key_factors=[
            "Stage and cluster spacing",
            "Stress field modeling",
            "Diagnostic monitoring",
            "Fracture geometry",
            "Proppant placement"
        ],
        primary_authority=[
            "SPE 140669, 'Stress Shadowing in Multi-Stage Fracturing'",
            "JPT, 2015"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Stress shadowing is negligible in field-scale treatments.",
        counter_arguments=[
            "Field data shows significant impact on fracture geometry.",
            "Ignoring shadowing reduces stimulation effectiveness."
        ],
        resolution_strategy="Model and optimize designs to minimize stress shadowing.",
        entity_scope="Multi-stage horizontal wells",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 140669"
    ),
    DoctrineBlock(
        topic="Limited Entry Perforating for Uniform Flow Distribution",
        keywords=["limited entry", "perforating", "flow distribution", "cluster efficiency"],
        conclusion_template="Limited entry perforating is used to balance flow across clusters, improving stimulation uniformity and SRV.",
        reasoning_framework=(
            "Limited entry perforating involves reducing the number of perforations per cluster to increase entry pressure, forcing fluid to distribute more evenly across all clusters. "
            "This technique mitigates near-wellbore pressure losses and improves cluster efficiency. "
            "Design parameters include perforation diameter, shot density, and charge selection. "
            "Field diagnostics (e.g., fiber optic monitoring) are used to validate flow distribution. "
            "Uniform stimulation maximizes SRV and enhances production."
        ),
        key_factors=[
            "Perforation design",
            "Entry pressure calculation",
            "Cluster count",
            "Flow diagnostics",
            "Shot density"
        ],
        primary_authority=[
            "SPE 184880, 'Limited Entry Perforating Design'",
            "JPT, 2017"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Standard perforating is sufficient for all treatments.",
        counter_arguments=[
            "Limited entry improves cluster efficiency.",
            "Standard designs may cause uneven stimulation.",
            "Field data supports limited entry effectiveness."
        ],
        resolution_strategy="Design limited entry perforating based on cluster count and diagnostics.",
        entity_scope="Multi-cluster horizontal wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Chemical Diversion Agents for Improved Fracture Complexity",
        keywords=["chemical diversion", "diversion agents", "fracture complexity", "stimulation"],
        conclusion_template="Chemical diversion agents are deployed to temporarily block dominant flow paths, enhancing fracture complexity and SRV.",
        reasoning_framework=(
            "Chemical diversion agents (e.g., viscoelastic polymers, degradable particulates) are used to temporarily block open fractures or clusters, redirecting fluid to unstimulated zones. "
            "This increases fracture complexity and improves overall SRV. "
            "Diversion is particularly effective in heterogeneous reservoirs or multi-cluster treatments. "
            "Agent selection depends on reservoir temperature, fluid compatibility, and degradation profile. "
            "Field trials and diagnostics inform diversion strategy."
        ),
        key_factors=[
            "Agent selection",
            "Reservoir temperature",
            "Degradation profile",
            "Cluster heterogeneity",
            "Diagnostic validation"
        ],
        primary_authority=[
            "SPE 182821, 'Chemical Diversion in Hydraulic Fracturing'",
            "JPT, 2016"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Diversion agents add cost without measurable benefit.",
        counter_arguments=[
            "Diversion increases SRV and production.",
            "Field data shows improved cluster stimulation.",
            "Cost is offset by enhanced recovery."
        ],
        resolution_strategy="Select and deploy diversion agents based on reservoir diagnostics.",
        entity_scope="Heterogeneous and multi-cluster reservoirs",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 182821"
    ),
    DoctrineBlock(
        topic="Real-Time Frac Monitoring - Treating Pressure Interpretation",
        keywords=["real-time monitoring", "treating pressure", "interpretation", "frac diagnostics"],
        conclusion_template="Real-time treating pressure monitoring enables immediate detection of operational issues and optimization of treatment parameters.",
        reasoning_framework=(
            "Continuous monitoring of treating pressure during fracturing provides critical feedback on fracture propagation, fluid efficiency, and potential issues such as screenout or out-of-zone growth. "
            "Pressure trends are interpreted using diagnostic plots (e.g., pressure vs. time, net pressure analysis) to inform real-time adjustments. "
            "Anomalies are investigated promptly to avoid operational failures. "
            "Integration with other diagnostics (e.g., microseismic, fiber optics) enhances interpretation accuracy."
        ),
        key_factors=[
            "Pressure sensor accuracy",
            "Diagnostic plot interpretation",
            "Anomaly detection",
            "Real-time decision making",
            "Integration with other diagnostics"
        ],
        primary_authority=[
            "SPE 140669",
            "SPE 184880"
        ],
        burden_holder="Frac Supervisor",
        adversary_position="Post-job analysis is sufficient for treatment optimization.",
        counter_arguments=[
            "Real-time monitoring prevents operational failures.",
            "Immediate adjustments improve treatment outcomes.",
            "Post-job analysis cannot correct real-time issues."
        ],
        resolution_strategy="Implement real-time monitoring and empower field teams to adjust treatments.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 140669"
    ),
    DoctrineBlock(
        topic="Frac Gradient Calculations for Treatment Design",
        keywords=["frac gradient", "calculation", "treatment design", "pressure gradient"],
        conclusion_template="Frac gradient calculations are essential for determining required treating pressures and safe operational limits.",
        reasoning_framework=(
            "Frac gradient is the pressure required to initiate and propagate a fracture per unit depth, typically expressed in psi/ft. "
            "Accurate gradient calculations inform pump rate, fluid selection, and containment strategies. "
            "Gradients are determined from mini-frac, DFIT, or field data, and must account for overburden, pore pressure, and formation properties. "
            "Designs should avoid exceeding safe operational limits to prevent casing failure or out-of-zone growth."
        ),
        key_factors=[
            "Formation depth",
            "Overburden and pore pressure",
            "Field test data",
            "Operational safety margins",
            "Pressure monitoring"
        ],
        primary_authority=[
            "Economides, M.J., 'Reservoir Stimulation', 3rd Edition",
            "SPE Monograph Vol. 12"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Frac gradient can be estimated from regional averages.",
        counter_arguments=[
            "Local gradients vary significantly.",
            "Field tests provide more accurate data.",
            "Design errors increase with poor gradient estimation."
        ],
        resolution_strategy="Calculate frac gradients from field-specific data.",
        entity_scope="All hydraulic fracturing treatments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Reservoir Stimulation, 3rd Ed."
    ),
    DoctrineBlock(
        topic="Proppant Selection - Sand vs Ceramic vs Resin-Coated",
        keywords=["proppant selection", "sand", "ceramic", "resin-coated", "conductivity"],
        conclusion_template="Proppant selection is based on closure stress, conductivity requirements, and cost, with sand for moderate stress, ceramic for high stress, and resin-coated for fines control.",
        reasoning_framework=(
            "Sand is the most common and cost-effective proppant, suitable for moderate closure stress environments. "
            "Ceramic proppants offer higher strength and conductivity under high closure stress, but at greater cost. "
            "Resin-coated proppants are used where fines migration or proppant flowback is a concern. "
            "Selection should be based on laboratory and field data, balancing conductivity, cost, and operational risks. "
            "Hybrid designs may combine multiple proppant types for optimal performance."
        ),
        key_factors=[
            "Closure stress",
            "Conductivity requirements",
            "Cost",
            "Fines migration",
            "Operational risk"
        ],
        primary_authority=[
            "SPE 1690",
            "SPE 18245"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Sand is always the best choice due to cost.",
        counter_arguments=[
            "High stress can crush sand, reducing conductivity.",
            "Ceramic and resin-coated proppants address specific challenges.",
            "Cost must be balanced with performance."
        ],
        resolution_strategy="Select proppant based on closure stress and production goals.",
        entity_scope="All propped fracture treatments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 1690"
    ),
    DoctrineBlock(
        topic="Cluster Spacing Optimization for Stimulated Reservoir Volume",
        keywords=["cluster spacing", "optimization", "SRV", "stimulated reservoir volume"],
        conclusion_template="Cluster spacing should be optimized to maximize SRV and production, accounting for stress shadowing and reservoir heterogeneity.",
        reasoning_framework=(
            "Optimal cluster spacing ensures uniform stimulation and maximizes SRV. "
            "Too-tight spacing can lead to stress shadowing and reduced cluster efficiency, while too-wide spacing leaves reservoir volumes unstimulated. "
            "Spacing is determined using numerical modeling, diagnostics, and field trials. "
            "Reservoir heterogeneity and operational constraints must be considered. "
            "Continuous improvement is achieved through post-treatment evaluation and adjustment."
        ),
        key_factors=[
            "Stress shadowing",
            "Reservoir heterogeneity",
            "Numerical modeling",
            "Field diagnostics",
            "Operational constraints"
        ],
        primary_authority=[
            "SPE 140669",
            "SPE 191372"
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Uniform cluster spacing is always optimal.",
        counter_arguments=[
            "Reservoir properties may require variable spacing.",
            "Uniform spacing can reduce SRV in heterogeneous formations."
        ],
        resolution_strategy="Optimize cluster spacing using diagnostics and modeling.",
        entity_scope="Multi-stage horizontal wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 140669"
    ),
    DoctrineBlock(
        topic="Fracture Fluid Selection - Slickwater vs Crosslinked Gel vs Hybrid",
        keywords=["fracture fluid", "slickwater", "crosslinked gel", "hybrid", "fluid selection"],
        conclusion_template="Fluid selection is based on proppant transport, leakoff control, and reservoir compatibility; slickwater for high-rate, gel for high proppant loads, hybrid for balance.",
        reasoning_framework=(
            "Slickwater fluids are low-viscosity and enable high pump rates, suitable for long fractures and efficient proppant placement in low-permeability reservoirs. "
            "Crosslinked gels provide high viscosity for carrying large proppant loads and controlling fluid leakoff, but may leave damaging residues. "
            "Hybrid designs combine slickwater and gel stages to balance transport and cleanup. "
            "Selection depends on reservoir properties, proppant type, and operational goals. "
            "Laboratory and field testing guide fluid system optimization."
        ),
        key_factors=[
            "Proppant transport",
            "Leakoff control",
            "Residue potential",
            "Reservoir compatibility",
            "Operational goals"
        ],
        primary_authority=[
            "SPE 39497",
            "Economides, M.J., 'Reservoir Stimulation', 3rd Ed."
        ],
        burden_holder="Frac Design Engineer",
        adversary_position="Slickwater is always preferable due to lower cost.",
        counter_arguments=[
            "High proppant loads require gel or hybrid fluids.",
            "Reservoir compatibility may favor alternative fluids.",
            "Cost must be balanced with effectiveness."
        ],
        resolution_strategy="Select fluid system based on proppant load and reservoir diagnostics.",
        entity_scope="All hydraulic fracturing treatments",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 39497"
    ),
    DoctrineBlock(
        topic="Post-Frac Flowback and Cleanup Strategy",
        keywords=["post-frac", "flowback", "cleanup", "strategy"],
        conclusion_template="Controlled post-frac flowback is essential to remove treatment fluids, minimize proppant flowback, and protect fracture conductivity.",
        reasoning_framework=(
            "Post-frac flowback removes injected fluids and initiates production. "
            "Flowback rates must be controlled to avoid mobilizing proppant and damaging fracture conductivity. "
            "Gradual ramp-up allows for pressure normalization and minimizes fines migration. "
            "Chemical additives may be used to aid cleanup. "
            "Field monitoring and adjustment are required to optimize recovery and protect long-term well performance."
        ),
        key_factors=[
            "Flowback rate control",
            "Proppant flowback prevention",
            "Pressure normalization",
            "Chemical additives",
            "Field monitoring"
        ],
        primary_authority=[
            "SPE 1690",
            "SPE 18245"
        ],
        burden_holder="Production Engineer",
        adversary_position="Rapid flowback maximizes early production.",
        counter_arguments=[
            "Rapid flowback risks proppant production and conductivity loss.",
            "Controlled flowback protects long-term well performance."
        ],
        resolution_strategy="Implement controlled flowback protocols and monitor well response.",
        entity_scope="All post-frac wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 1690"
    ),
    # Additional doctrines to reach 40+ entries
    DoctrineBlock(
        topic="Perforation Erosion Management in High-Rate Treatments",
        keywords=["perforation erosion", "high-rate", "treatments", "well integrity"],
        conclusion_template="Perforation erosion must be managed in high-rate treatments to maintain entry pressure and well integrity.",
        reasoning_framework=(
            "High-rate fracturing treatments can cause significant perforation erosion, reducing entry pressure and potentially compromising well integrity. "
            "Erosion is influenced by fluid velocity, proppant concentration, and perforation design. "
            "Monitoring and modeling erosion rates enable engineers to adjust treatment parameters and perforation strategies. "
            "Use of erosion-resistant charges and staged pumping can mitigate risks."
        ),
        key_factors=[
            "Fluid velocity",
            "Proppant concentration",
            "Perforation design",
            "Erosion-resistant charges",
            "Monitoring"
        ],
        primary_authority=[
            "SPE 184880",
            "SPE 191372"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Perforation erosion is negligible in modern treatments.",
        counter_arguments=[
            "Field data shows significant erosion at high rates.",
            "Erosion reduces cluster efficiency and well integrity."
        ],
        resolution_strategy="Model and monitor erosion, adjust designs as needed.",
        entity_scope="High-rate fracturing treatments",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Water Management in Hydraulic Fracturing Operations",
        keywords=["water management", "hydraulic fracturing", "operations", "recycling"],
        conclusion_template="Effective water management, including recycling and sourcing, is critical for sustainable hydraulic fracturing operations.",
        reasoning_framework=(
            "Hydraulic fracturing requires large volumes of water, making sourcing, transport, and disposal key operational challenges. "
            "Water recycling reduces environmental impact and operational costs. "
            "Treatment of flowback and produced water must meet regulatory and operational standards. "
            "Sourcing strategies should prioritize local, non-potable, or recycled water where feasible. "
            "Integrated water management plans enhance sustainability and community relations."
        ),
        key_factors=[
            "Water sourcing",
            "Recycling technology",
            "Regulatory compliance",
            "Cost",
            "Community impact"
        ],
        primary_authority=[
            "SPE 163821",
            "JPT, 2015"
        ],
        burden_holder="Operations Manager",
        adversary_position="Freshwater is always preferable for fracturing.",
        counter_arguments=[
            "Recycling reduces cost and environmental impact.",
            "Freshwater use may face regulatory or community opposition."
        ],
        resolution_strategy="Implement water recycling and alternative sourcing strategies.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 163821"
    ),
    DoctrineBlock(
        topic="Microseismic Monitoring for Fracture Mapping",
        keywords=["microseismic", "monitoring", "fracture mapping", "diagnostics"],
        conclusion_template="Microseismic monitoring provides direct measurement of fracture geometry and complexity, informing treatment optimization.",
        reasoning_framework=(
            "Microseismic monitoring detects seismic events generated by fracture propagation, enabling real-time mapping of fracture geometry and complexity. "
            "Data is used to validate models, optimize treatment parameters, and assess SRV. "
            "Limitations include signal-to-noise ratio, sensor placement, and interpretation uncertainty. "
            "Integration with other diagnostics enhances reliability."
        ),
        key_factors=[
            "Sensor placement",
            "Data interpretation",
            "Signal quality",
            "Model validation",
            "Integration with other diagnostics"
        ],
        primary_authority=[
            "SPE 140669",
            "SPE 184880"
        ],
        burden_holder="Frac Diagnostics Engineer",
        adversary_position="Microseismic monitoring is unnecessary with modern modeling.",
        counter_arguments=[
            "Field data provides ground truth for models.",
            "Model-only approaches may miss critical complexity."
        ],
        resolution_strategy="Deploy microseismic in complex or high-value treatments.",
        entity_scope="Complex or high-value wells",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 140669"
    ),
    DoctrineBlock(
        topic="Well Spacing Optimization in Unconventional Reservoirs",
        keywords=["well spacing", "optimization", "unconventional", "reservoirs"],
        conclusion_template="Well spacing must be optimized to balance recovery, minimize interference, and maximize economic returns.",
        reasoning_framework=(
            "In unconventional reservoirs, well spacing impacts recovery efficiency, parent-child interactions, and economic outcomes. "
            "Too-tight spacing increases interference and frac hits, while too-wide spacing leaves reserves unrecovered. "
            "Optimization uses reservoir simulation, field diagnostics, and economic modeling. "
            "Spacing decisions are revisited as field data accumulates."
        ),
        key_factors=[
            "Reservoir heterogeneity",
            "Frac hit risk",
            "Economic modeling",
            "Field diagnostics",
            "Parent-child interactions"
        ],
        primary_authority=[
            "SPE 191372",
            "JPT, 2018"
        ],
        burden_holder="Development Engineer",
        adversary_position="Tightest possible spacing maximizes recovery.",
        counter_arguments=[
            "Interference reduces well productivity.",
            "Optimal spacing balances recovery and economics."
        ],
        resolution_strategy="Model and monitor spacing, adjust as field data warrants.",
        entity_scope="Unconventional field developments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 191372"
    ),
    DoctrineBlock(
        topic="Fiber Optic Diagnostics for Cluster Efficiency Evaluation",
        keywords=["fiber optic", "diagnostics", "cluster efficiency", "evaluation"],
        conclusion_template="Fiber optic diagnostics provide high-resolution data on cluster efficiency, informing design improvements.",
        reasoning_framework=(
            "Fiber optic sensing (DTS, DAS) enables real-time measurement of temperature and acoustic signals along the wellbore. "
            "This data is used to evaluate flow distribution, cluster efficiency, and fracture propagation. "
            "Results inform adjustments to perforation design, cluster spacing, and treatment parameters. "
            "Integration with other diagnostics enhances overall understanding."
        ),
        key_factors=[
            "Sensor deployment",
            "Data interpretation",
            "Integration with other diagnostics",
            "Design feedback",
            "Operational adjustment"
        ],
        primary_authority=[
            "SPE 184880",
            "JPT, 2017"
        ],
        burden_holder="Frac Diagnostics Engineer",
        adversary_position="Fiber optic diagnostics are too costly for routine use.",
        counter_arguments=[
            "High-value data justifies cost in complex wells.",
            "Design improvements offset diagnostic expenses."
        ],
        resolution_strategy="Deploy fiber optics in complex or high-value wells.",
        entity_scope="Complex or high-value wells",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Proppant Flowback Control Technologies",
        keywords=["proppant flowback", "control", "technologies", "well integrity"],
        conclusion_template="Proppant flowback control technologies, such as resin coatings and flowback aids, protect well integrity and fracture conductivity.",
        reasoning_framework=(
            "Proppant flowback can damage well equipment and reduce fracture conductivity. "
            "Control technologies include resin-coated proppants, chemical flowback aids, and mechanical screens. "
            "Selection depends on reservoir conditions, proppant type, and operational constraints. "
            "Monitoring and adjustment are required to optimize performance."
        ),
        key_factors=[
            "Proppant type",
            "Reservoir conditions",
            "Chemical aids",
            "Mechanical screens",
            "Monitoring"
        ],
        primary_authority=[
            "SPE 1690",
            "SPE 18245"
        ],
        burden_holder="Production Engineer",
        adversary_position="Proppant flowback is unavoidable and must be accepted.",
        counter_arguments=[
            "Control technologies reduce flowback and protect well integrity.",
            "Operational adjustments can minimize flowback."
        ],
        resolution_strategy="Select and deploy flowback control based on well diagnostics.",
        entity_scope="All propped fracture treatments",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 1690"
    ),
    DoctrineBlock(
        topic="Sand Logistics and Proppant Supply Chain Management",
        keywords=["sand logistics", "proppant", "supply chain", "management"],
        conclusion_template="Efficient sand logistics and supply chain management are critical to prevent operational delays and control costs.",
        reasoning_framework=(
            "Hydraulic fracturing requires timely delivery of large volumes of proppant. "
            "Supply chain management includes sourcing, transport, storage, and site delivery. "
            "Logistics failures can cause costly delays or treatment interruptions. "
            "Real-time tracking, inventory management, and contingency planning are essential for operational success."
        ),
        key_factors=[
            "Sourcing",
            "Transport logistics",
            "Inventory management",
            "Site delivery",
            "Contingency planning"
        ],
        primary_authority=[
            "SPE 191372",
            "JPT, 2018"
        ],
        burden_holder="Operations Manager",
        adversary_position="Sand supply is a minor operational concern.",
        counter_arguments=[
            "Supply interruptions halt treatments.",
            "Efficient logistics reduce cost and risk."
        ],
        resolution_strategy="Implement robust supply chain and logistics management.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 191372"
    ),
    DoctrineBlock(
        topic="Environmental Regulations Impacting Hydraulic Fracturing",
        keywords=["environmental regulations", "hydraulic fracturing", "compliance", "regulatory"],
        conclusion_template="Compliance with environmental regulations is mandatory and impacts water use, chemical disclosure, and waste management.",
        reasoning_framework=(
            "Hydraulic fracturing operations are subject to federal, state, and local environmental regulations. "
            "Key areas include water sourcing and disposal, chemical disclosure (e.g., FracFocus), air emissions, and waste management. "
            "Non-compliance can result in fines, operational shutdowns, and reputational damage. "
            "Operators must implement compliance programs and monitor regulatory changes."
        ),
        key_factors=[
            "Water use and disposal",
            "Chemical disclosure",
            "Air emissions",
            "Waste management",
            "Regulatory monitoring"
        ],
        primary_authority=[
            "EPA Hydraulic Fracturing Regulations",
            "FracFocus.org"
        ],
        burden_holder="Regulatory Compliance Manager",
        adversary_position="Regulatory compliance is a formality with little operational impact.",
        counter_arguments=[
            "Non-compliance risks operational shutdown.",
            "Reputation and community relations are impacted.",
            "Regulations are strictly enforced."
        ],
        resolution_strategy="Implement and audit compliance programs.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Regulations"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Additive Selection and Compatibility",
        keywords=["additive selection", "hydraulic fracturing", "compatibility", "chemicals"],
        conclusion_template="Additive selection must ensure chemical compatibility, operational effectiveness, and regulatory compliance.",
        reasoning_framework=(
            "Fracturing additives include friction reducers, biocides, scale inhibitors, and breakers. "
            "Selection is based on reservoir conditions, fluid system, and compatibility with other additives. "
            "Incompatible additives can cause precipitation, formation damage, or reduced effectiveness. "
            "Regulatory requirements may restrict certain chemicals. "
            "Laboratory testing and field trials guide additive selection."
        ),
        key_factors=[
            "Reservoir conditions",
            "Additive compatibility",
            "Operational effectiveness",
            "Regulatory compliance",
            "Laboratory testing"
        ],
        primary_authority=[
            "SPE 39497",
            "FracFocus.org"
        ],
        burden_holder="Frac Fluid Engineer",
        adversary_position="All additives are compatible by default.",
        counter_arguments=[
            "Incompatibility can cause operational failures.",
            "Testing is required to ensure effectiveness."
        ],
        resolution_strategy="Test and select additives for each treatment.",
        entity_scope="All hydraulic fracturing treatments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 39497"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Data Management and Analytics",
        keywords=["data management", "analytics", "hydraulic fracturing", "digital oilfield"],
        conclusion_template="Effective data management and analytics are essential for continuous improvement and operational optimization.",
        reasoning_framework=(
            "Hydraulic fracturing generates large volumes of operational and diagnostic data. "
            "Structured data management enables analysis, benchmarking, and continuous improvement. "
            "Analytics tools identify trends, optimize designs, and reduce operational risk. "
            "Data security and quality control are critical for reliable insights."
        ),
        key_factors=[
            "Data quality",
            "Analytics tools",
            "Benchmarking",
            "Continuous improvement",
            "Data security"
        ],
        primary_authority=[
            "SPE 191372",
            "JPT, 2018"
        ],
        burden_holder="Data Analytics Engineer",
        adversary_position="Data management is a low priority in field operations.",
        counter_arguments=[
            "Analytics drive operational improvement.",
            "Poor data quality leads to suboptimal decisions."
        ],
        resolution_strategy="Implement structured data management and analytics programs.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 191372"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Well Integrity and Casing Design",
        keywords=["well integrity", "casing design", "hydraulic fracturing", "zonal isolation"],
        conclusion_template="Well integrity and robust casing design are foundational for safe and effective hydraulic fracturing operations.",
        reasoning_framework=(
            "Casing and cement must withstand fracturing pressures and provide zonal isolation. "
            "Designs are based on expected treating pressures, formation properties, and regulatory requirements. "
            "Failure to ensure well integrity can lead to casing leaks, loss of containment, and environmental incidents. "
            "Regular integrity testing and monitoring are required."
        ),
        key_factors=[
            "Casing strength",
            "Cement quality",
            "Pressure rating",
            "Integrity testing",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 90",
            "SPE 39497"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Standard casing designs are sufficient for all treatments.",
        counter_arguments=[
            "High treating pressures may exceed standard ratings.",
            "Integrity failures have severe consequences."
        ],
        resolution_strategy="Design and test casing for each fracturing operation.",
        entity_scope="All hydraulic fracturing wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 90"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Induced Seismicity Management",
        keywords=["induced seismicity", "hydraulic fracturing", "management", "earthquakes"],
        conclusion_template="Induced seismicity must be monitored and managed to minimize risk of felt earthquakes and regulatory action.",
        reasoning_framework=(
            "Hydraulic fracturing can induce seismic events, particularly in areas with critically stressed faults. "
            "Monitoring includes microseismic networks and regulatory reporting. "
            "Operational adjustments (e.g., rate reduction, shut-in) are made if seismicity thresholds are approached. "
            "Risk assessment and mitigation planning are required in seismically sensitive areas."
        ),
        key_factors=[
            "Fault mapping",
            "Seismic monitoring",
            "Operational thresholds",
            "Regulatory reporting",
            "Mitigation planning"
        ],
        primary_authority=[
            "USGS Induced Seismicity Reports",
            "SPE 184880"
        ],
        burden_holder="Operations Manager",
        adversary_position="Induced seismicity is not a concern in hydraulic fracturing.",
        counter_arguments=[
            "Regulatory action can halt operations.",
            "Seismic events can cause public concern."
        ],
        resolution_strategy="Monitor and mitigate induced seismicity in all operations.",
        entity_scope="Seismically sensitive areas",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="USGS Reports"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Economic Evaluation and Cost Control",
        keywords=["economic evaluation", "cost control", "hydraulic fracturing", "project management"],
        conclusion_template="Economic evaluation and cost control are essential for project viability and capital efficiency in hydraulic fracturing.",
        reasoning_framework=(
            "Fracturing projects require detailed economic analysis, including capital and operating costs, production forecasts, and risk assessment. "
            "Cost control measures include supply chain optimization, operational efficiency, and technology selection. "
            "Continuous tracking and benchmarking ensure capital is deployed efficiently."
        ),
        key_factors=[
            "Cost tracking",
            "Production forecasting",
            "Supply chain optimization",
            "Operational efficiency",
            "Risk assessment"
        ],
        primary_authority=[
            "SPE 191372",
            "JPT, 2018"
        ],
        burden_holder="Project Manager",
        adversary_position="Cost control reduces treatment effectiveness.",
        counter_arguments=[
            "Efficient spending maximizes returns.",
            "Cost overruns can jeopardize project viability."
        ],
        resolution_strategy="Implement economic evaluation and cost control programs.",
        entity_scope="All hydraulic fracturing projects",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 191372"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Operational Safety Protocols",
        keywords=["operational safety", "protocols", "hydraulic fracturing", "HSE"],
        conclusion_template="Strict operational safety protocols are mandatory to protect personnel, assets, and the environment during hydraulic fracturing.",
        reasoning_framework=(
            "Hydraulic fracturing involves high pressures, heavy equipment, and hazardous chemicals. "
            "Comprehensive safety protocols include equipment inspection, PPE, emergency response planning, and crew training. "
            "Incident reporting and safety audits drive continuous improvement. "
            "Regulatory compliance is non-negotiable."
        ),
        key_factors=[
            "Equipment inspection",
            "PPE compliance",
            "Emergency response",
            "Crew training",
            "Incident reporting"
        ],
        primary_authority=[
            "OSHA Oil and Gas Safety Regulations",
            "API RP 54"
        ],
        burden_holder="HSE Manager",
        adversary_position="Standard field safety is sufficient for fracturing operations.",
        counter_arguments=[
            "Fracturing hazards require specialized protocols.",
            "Regulatory penalties for non-compliance are severe."
        ],
        resolution_strategy="Implement and audit safety protocols for all operations.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA Regulations"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Site Preparation and Logistics",
        keywords=["site preparation", "logistics", "hydraulic fracturing", "operations"],
        conclusion_template="Comprehensive site preparation and logistics planning are essential for safe, efficient hydraulic fracturing operations.",
        reasoning_framework=(
            "Site preparation includes access roads, pad construction, equipment staging, and safety barriers. "
            "Logistics planning ensures timely delivery of materials, equipment, and personnel. "
            "Coordination with local authorities and landowners is required. "
            "Poor preparation increases operational risk and cost."
        ),
        key_factors=[
            "Access and pad construction",
            "Equipment staging",
            "Material delivery",
            "Safety barriers",
            "Stakeholder coordination"
        ],
        primary_authority=[
            "API RP 54",
            "SPE 191372"
        ],
        burden_holder="Operations Manager",
        adversary_position="Minimal site preparation is sufficient for most treatments.",
        counter_arguments=[
            "Operational delays and safety incidents increase with poor preparation.",
            "Proper planning reduces cost and risk."
        ],
        resolution_strategy="Plan and execute comprehensive site preparation for all treatments.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 54"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Wellbore Cleanout Best Practices",
        keywords=["wellbore cleanout", "best practices", "hydraulic fracturing", "debris removal"],
        conclusion_template="Wellbore cleanout before and after fracturing is critical to remove debris and ensure treatment effectiveness.",
        reasoning_framework=(
            "Debris in the wellbore can block perforations, reduce flow, and cause screenouts. "
            "Cleanout operations include circulating fluids, mechanical scraping, and chemical washes. "
            "Pre-treatment cleanout ensures effective stimulation, while post-treatment cleanout protects well performance. "
            "Monitoring and verification are required for best results."
        ),
        key_factors=[
            "Debris removal",
            "Circulation and scraping",
            "Chemical washes",
            "Monitoring",
            "Verification"
        ],
        primary_authority=[
            "SPE 1690",
            "API RP 54"
        ],
        burden_holder="Wellsite Supervisor",
        adversary_position="Cleanout is unnecessary if well is cased and cemented.",
        counter_arguments=[
            "Debris can accumulate during drilling and completion.",
            "Cleanout reduces operational risk."
        ],
        resolution_strategy="Conduct cleanout operations before and after fracturing.",
        entity_scope="All hydraulic fracturing wells",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 1690"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Communication and Stakeholder Engagement",
        keywords=["communication", "stakeholder engagement", "hydraulic fracturing", "community relations"],
        conclusion_template="Proactive communication and stakeholder engagement are essential for project acceptance and operational continuity.",
        reasoning_framework=(
            "Hydraulic fracturing projects impact local communities and stakeholders. "
            "Proactive engagement includes public meetings, information sharing, and addressing concerns. "
            "Transparent communication builds trust and reduces opposition. "
            "Failure to engage can result in project delays or shutdowns."
        ),
        key_factors=[
            "Public meetings",
            "Information sharing",
            "Concern resolution",
            "Transparency",
            "Community trust"
        ],
        primary_authority=[
            "API Community Engagement Guidelines",
            "EPA Stakeholder Engagement Reports"
        ],
        burden_holder="Project Manager",
        adversary_position="Stakeholder engagement is unnecessary for technical projects.",
        counter_arguments=[
            "Community opposition can halt operations.",
            "Engagement builds trust and project support."
        ],
        resolution_strategy="Implement stakeholder engagement plans for all projects.",
        entity_scope="All hydraulic fracturing projects",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API Guidelines"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Equipment Maintenance and Reliability",
        keywords=["equipment maintenance", "reliability", "hydraulic fracturing", "operations"],
        conclusion_template="Regular equipment maintenance and reliability programs are essential to prevent downtime and ensure safe operations.",
        reasoning_framework=(
            "Fracturing equipment operates under high stress and must be maintained to prevent failures. "
            "Maintenance programs include scheduled inspections, preventive repairs, and real-time monitoring. "
            "Reliability engineering identifies failure modes and improves equipment design. "
            "Downtime increases cost and operational risk."
        ),
        key_factors=[
            "Scheduled maintenance",
            "Preventive repairs",
            "Real-time monitoring",
            "Reliability engineering",
            "Failure mode analysis"
        ],
        primary_authority=[
            "API RP 54",
            "SPE 191372"
        ],
        burden_holder="Maintenance Manager",
        adversary_position="Reactive maintenance is sufficient for field equipment.",
        counter_arguments=[
            "Preventive maintenance reduces failures.",
            "Downtime is costly and avoidable."
        ],
        resolution_strategy="Implement preventive maintenance and reliability programs.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 54"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Waste Management and Disposal",
        keywords=["waste management", "disposal", "hydraulic fracturing", "environmental"],
        conclusion_template="Proper waste management and disposal are required to meet environmental regulations and protect community health.",
        reasoning_framework=(
            "Hydraulic fracturing generates solid and liquid waste, including flowback fluids, drill cuttings, and chemical containers. "
            "Waste must be handled, transported, and disposed of according to regulatory standards. "
            "Improper disposal can result in environmental damage, fines, and loss of social license. "
            "Waste minimization and recycling are preferred where feasible."
        ),
        key_factors=[
            "Waste characterization",
            "Regulatory compliance",
            "Transport and disposal",
            "Minimization and recycling",
            "Community health"
        ],
        primary_authority=[
            "EPA Waste Management Regulations",
            "FracFocus.org"
        ],
        burden_holder="Environmental Manager",
        adversary_position="Waste disposal is a minor operational concern.",
        counter_arguments=[
            "Improper disposal risks fines and shutdowns.",
            "Community relations depend on responsible management."
        ],
        resolution_strategy="Implement waste management plans and monitor compliance.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA Regulations"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Supply Chain Resilience",
        keywords=["supply chain", "resilience", "hydraulic fracturing", "operations"],
        conclusion_template="Supply chain resilience planning is essential to mitigate disruptions and maintain operational continuity.",
        reasoning_framework=(
            "Hydraulic fracturing relies on complex supply chains for materials, equipment, and personnel. "
            "Disruptions can result from weather, transportation failures, or market volatility. "
            "Resilience planning includes inventory buffers, alternate suppliers, and contingency protocols. "
            "Continuous monitoring and risk assessment are required."
        ),
        key_factors=[
            "Inventory buffers",
            "Alternate suppliers",
            "Contingency planning",
            "Risk assessment",
            "Monitoring"
        ],
        primary_authority=[
            "SPE 191372",
            "JPT, 2018"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Supply chain disruptions are rare and not worth planning for.",
        counter_arguments=[
            "Operational delays are costly.",
            "Resilience planning reduces risk."
        ],
        resolution_strategy="Develop and maintain supply chain resilience plans.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 191372"
    ),
    DoctrineBlock(
        topic="Hydraulic Fracturing Technology Adoption and Field Pilots",
        keywords=["technology adoption", "field pilots", "hydraulic fracturing", "innovation"],
        conclusion_template="Field pilots are required to validate new hydraulic fracturing technologies before full-scale adoption.",
        reasoning_framework=(
            "New technologies must be field-tested to assess operational effectiveness, economic value, and compatibility. "
            "Pilots are designed with clear objectives and performance metrics. "
            "Results inform go/no-go decisions for broader adoption. "
            "Continuous innovation drives operational improvement and competitiveness."
        ),
        key_factors=[
            "Pilot design",
            "Performance metrics",
            "Operational compatibility",
            "Economic evaluation",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 191372",
            "JPT, 2018"
        ],
        burden_holder="Technology Manager",
        adversary_position="New technologies can be adopted without field validation.",
        counter_arguments=[
            "Pilots reduce risk of operational failures.",
            "Validated technologies deliver greater value."
        ],
        resolution_strategy="Conduct field pilots for all new technologies.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 191372"
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in kw.lower() for kw in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]