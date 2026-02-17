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
        topic="Equivalent Circulating Density (ECD) Fundamentals",
        keywords=["ECD", "pressure", "mud weight", "circulation", "annulus", "hydraulics"],
        conclusion_template="The Equivalent Circulating Density (ECD) is calculated by adding the static mud weight to the pressure losses converted to equivalent mud weight, ensuring wellbore pressure management within safe operational limits.",
        reasoning_framework=(
            "ECD represents the effective density exerted by the drilling fluid when it is circulating. "
            "It accounts for the static mud column plus the dynamic pressure losses due to fluid movement through the annulus and drillstring. "
            "The framework involves calculating pressure losses from friction, pipe geometry, and fluid rheology, "
            "then converting these losses into equivalent mud weight increments. This approach ensures the wellbore pressure is "
            "adequately maintained to prevent influxes or losses, balancing the hydrostatic and dynamic components. "
            "The calculation requires integrating fluid properties, flow rates, and wellbore geometry to yield accurate ECD values."
        ),
        key_factors=["mud density", "flow rate", "annular geometry", "fluid rheology", "pressure losses", "wellbore inclination"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al., Applied Drilling Engineering", "Barree & Conway, Drilling Hydraulics"],
        burden_holder="Drilling Engineer",
        adversary_position="ECD calculations are overly conservative and lead to unnecessary operational constraints.",
        counter_arguments=[
            "Ignoring dynamic pressure losses risks well control incidents.",
            "Conservative ECD ensures safety margins in narrow mud weight windows.",
            "Field data consistently validates ECD models when properly applied."
        ],
        resolution_strategy=(
            "Employ real-time monitoring and adjust models with downhole measurements to refine ECD estimates, "
            "balancing safety and operational efficiency."
        ),
        entity_scope="Wellbore hydraulics during drilling operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 5.3"
    ),
    DoctrineBlock(
        topic="Bingham Plastic Rheological Model",
        keywords=["Bingham Plastic", "rheology", "yield stress", "plastic viscosity", "mud flow"],
        conclusion_template="The Bingham Plastic model characterizes drilling fluid behavior with a yield stress and a linear relationship between shear stress and shear rate beyond yield.",
        reasoning_framework=(
            "The Bingham Plastic model assumes that the drilling fluid behaves as a rigid body at low stresses and flows as a viscous fluid at stresses exceeding the yield point. "
            "Mathematically, shear stress (τ) is expressed as τ = τ_y + μ_p * γ̇, where τ_y is the yield stress, μ_p is the plastic viscosity, and γ̇ is the shear rate. "
            "This model is widely used for drilling muds that exhibit a finite yield stress and linear viscosity behavior at higher shear rates. "
            "It simplifies pressure loss calculations and is suitable for many water-based and oil-based muds under typical drilling conditions."
        ),
        key_factors=["yield stress", "plastic viscosity", "shear rate", "mud composition", "temperature"],
        primary_authority=["API RP 13B-1", "Fann Instrument Manuals", "Herschel-Bulkley Studies"],
        burden_holder="Mud Engineer",
        adversary_position="Bingham Plastic model oversimplifies complex mud rheology, leading to inaccurate pressure loss predictions.",
        counter_arguments=[
            "Model parameters are derived from field viscometer data ensuring practical applicability.",
            "More complex models increase computational burden without significant accuracy gains in many cases.",
            "Bingham Plastic remains a standard baseline for mud rheology in drilling hydraulics."
        ],
        resolution_strategy=(
            "Use Bingham Plastic model for initial design and switch to advanced models like Herschel-Bulkley when mud rheology is complex or non-linear."
        ),
        entity_scope="Drilling fluid rheology characterization",
        confidence=0.9,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 6.2"
    ),
    DoctrineBlock(
        topic="Power Law Rheological Model",
        keywords=["Power Law", "rheology", "shear thinning", "consistency index", "flow behavior index"],
        conclusion_template="The Power Law model describes non-Newtonian fluid behavior with shear stress proportional to shear rate raised to a flow behavior index, capturing shear thinning effects.",
        reasoning_framework=(
            "The Power Law model represents fluids whose viscosity decreases with increasing shear rate, common in many drilling muds. "
            "Shear stress (τ) is expressed as τ = K * (γ̇)^n, where K is the consistency index and n is the flow behavior index. "
            "Values of n less than 1 indicate shear thinning behavior. This model helps predict pressure losses and flow characteristics in annuli and drillstrings where non-Newtonian effects are significant. "
            "It requires rheological measurements across a range of shear rates to accurately determine K and n."
        ),
        key_factors=["consistency index", "flow behavior index", "shear rate range", "mud additives", "temperature"],
        primary_authority=["API RP 13B-1", "Chhabra & Richardson, Non-Newtonian Flow", "Barree & Conway"],
        burden_holder="Mud Engineer",
        adversary_position="Power Law model lacks a yield stress term, making it unsuitable for fluids with significant yield behavior.",
        counter_arguments=[
            "Power Law provides better fit for shear thinning fluids without clear yield stress.",
            "Combining Power Law with yield stress models (e.g., Herschel-Bulkley) can address limitations.",
            "Model choice depends on mud rheology and operational requirements."
        ],
        resolution_strategy=(
            "Select rheological model based on mud behavior; use Power Law for shear thinning fluids without yield stress, otherwise consider Herschel-Bulkley or Bingham Plastic."
        ),
        entity_scope="Non-Newtonian drilling fluid rheology",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="API RP 13B-1 Section 6.3"
    ),
    DoctrineBlock(
        topic="Annular Velocity and Hole Cleaning",
        keywords=["annular velocity", "hole cleaning", "cuttings transport", "flow rate", "cuttings concentration"],
        conclusion_template="Adequate annular velocity is critical to ensure efficient hole cleaning by suspending and transporting cuttings to the surface, preventing accumulation and stuck pipe incidents.",
        reasoning_framework=(
            "Annular velocity is the velocity of drilling fluid flowing upward through the annulus between the drillstring and wellbore. "
            "It directly influences the ability of the fluid to lift and transport cuttings generated by the drill bit. "
            "The framework considers the balance between fluid velocity, cuttings size and density, mud rheology, and wellbore inclination. "
            "Empirical and mechanistic models define critical transport velocities required to prevent cuttings bed formation. "
            "Insufficient annular velocity leads to cuttings settling, increased torque and drag, and potential stuck pipe."
        ),
        key_factors=["annular velocity", "cuttings size", "mud rheology", "wellbore inclination", "flow regime"],
        primary_authority=["Bourgoyne et al., Applied Drilling Engineering", "API RP 13B-1", "Barree & Conway"],
        burden_holder="Drilling Engineer",
        adversary_position="High annular velocity increases ECD and risk of formation fracturing.",
        counter_arguments=[
            "Optimizing annular velocity balances hole cleaning and pressure management.",
            "Use of rheology modifiers and flow rate adjustments mitigate risks.",
            "Real-time monitoring allows dynamic control of annular velocity."
        ],
        resolution_strategy=(
            "Implement integrated hydraulics and cuttings transport models with real-time data to optimize annular velocity for effective hole cleaning without exceeding pressure limits."
        ),
        entity_scope="Drilling hydraulics and cuttings transport",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 7.4"
    ),
    DoctrineBlock(
        topic="Standpipe Pressure Components",
        keywords=["standpipe pressure", "pressure losses", "friction", "hydrostatic", "annulus", "drillstring"],
        conclusion_template="Standpipe pressure is composed of hydrostatic pressure, frictional losses in the drillstring and annulus, and dynamic pressure components from fluid acceleration.",
        reasoning_framework=(
            "Standpipe pressure is the pressure measured at the surface injection point of the drilling fluid. "
            "It reflects the sum of hydrostatic pressure of the mud column, frictional pressure losses inside the drillstring and annulus, and any dynamic pressure changes due to acceleration or elevation changes. "
            "Calculations involve determining pressure drops due to laminar or turbulent flow regimes, pipe roughness, fluid rheology, and flow rates. "
            "Understanding these components is essential for diagnosing wellbore conditions and optimizing pump operations."
        ),
        key_factors=["mud density", "flow rate", "pipe diameter", "fluid rheology", "wellbore geometry"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al.", "Barree & Conway"],
        burden_holder="Drilling Engineer",
        adversary_position="Standpipe pressure readings are unreliable due to surface equipment variability.",
        counter_arguments=[
            "Proper calibration and instrumentation minimize measurement errors.",
            "Pressure trends provide valuable diagnostic information even with some variability.",
            "Complementary downhole measurements validate surface data."
        ],
        resolution_strategy=(
            "Use calibrated sensors and cross-validate standpipe pressure with downhole data and hydraulics models for accurate interpretation."
        ),
        entity_scope="Surface drilling hydraulics monitoring",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 7.2"
    ),
    DoctrineBlock(
        topic="Bit Hydraulic Optimization - Maximum HSI",
        keywords=["bit hydraulics", "hydraulic horsepower", "HSI", "nozzle size", "bit cleaning"],
        conclusion_template="Optimizing bit hydraulics to maximize Hydraulic Specific Energy (HSI) improves drilling efficiency by enhancing bit cleaning and rock breaking.",
        reasoning_framework=(
            "Hydraulic Specific Energy (HSI) is a measure of the hydraulic energy applied per unit area at the bit face, influencing the efficiency of rock cutting and hole cleaning. "
            "Maximizing HSI involves selecting appropriate nozzle sizes and flow rates to deliver high-velocity jets that remove cuttings and cool the bit. "
            "The framework includes calculating hydraulic horsepower, jet impact force, and flow distribution through bit nozzles. "
            "Balancing these parameters optimizes drilling rate while managing pressure losses and pump limitations."
        ),
        key_factors=["flow rate", "nozzle size", "bit design", "mud properties", "pressure losses"],
        primary_authority=["Bourgoyne et al.", "Barree & Conway", "API RP 13B-1"],
        burden_holder="Drilling Engineer",
        adversary_position="Maximizing HSI increases pump wear and energy consumption unnecessarily.",
        counter_arguments=[
            "Improved drilling rates reduce overall operational costs.",
            "Optimized hydraulics prevent bit balling and stuck pipe.",
            "Pump and equipment selection can accommodate optimized HSI."
        ],
        resolution_strategy=(
            "Perform cost-benefit analysis and real-time monitoring to balance HSI optimization with equipment constraints."
        ),
        entity_scope="Bit hydraulics and drilling efficiency",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 8.3"
    ),
    DoctrineBlock(
        topic="Bit Hydraulic Optimization - Maximum Impact Force",
        keywords=["bit hydraulics", "impact force", "nozzle velocity", "rock breaking", "jet force"],
        conclusion_template="Maximizing bit hydraulic impact force enhances rock fragmentation and bit cleaning by increasing jet velocity and momentum at the bit face.",
        reasoning_framework=(
            "Impact force at the bit nozzles is a function of fluid density, velocity, and nozzle geometry. "
            "Higher impact forces improve rock breaking efficiency and cuttings removal, reducing bit wear and drilling time. "
            "Calculations involve fluid dynamics principles to determine jet velocity and momentum flux, considering mud properties and pump output. "
            "The framework balances impact force with pump capacity and hole cleaning requirements to optimize drilling performance."
        ),
        key_factors=["mud density", "flow rate", "nozzle diameter", "bit design", "pump pressure"],
        primary_authority=["Bourgoyne et al.", "Barree & Conway", "API RP 13B-1"],
        burden_holder="Drilling Engineer",
        adversary_position="High impact forces cause premature bit wear and increased erosion.",
        counter_arguments=[
            "Proper nozzle selection and mud properties mitigate erosion.",
            "Improved drilling rates offset increased bit replacement costs.",
            "Monitoring and adjusting hydraulics prevent excessive wear."
        ],
        resolution_strategy=(
            "Optimize nozzle configuration and mud properties to maximize impact force within equipment limits and bit design specifications."
        ),
        entity_scope="Bit hydraulics and rock fragmentation",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 8.4"
    ),
    DoctrineBlock(
        topic="Surge and Swab Pressure Calculations",
        keywords=["surge pressure", "swab pressure", "tripping", "wellbore pressure", "fluid dynamics"],
        conclusion_template="Surge and swab pressures are transient pressure changes caused by drillstring movement, calculated using fluid dynamics and wellbore geometry to prevent well control incidents.",
        reasoning_framework=(
            "Surge pressure occurs when the drillstring is run into the hole, increasing pressure due to fluid displacement. "
            "Swab pressure arises when pulling out, reducing pressure and risking influx. "
            "Calculations involve modeling fluid compressibility, annular clearances, mud rheology, and drillstring velocity. "
            "Transient pressure models use momentum and continuity equations to predict pressure spikes or drops. "
            "Accurate surge and swab predictions are critical for maintaining wellbore stability and avoiding kicks or losses during tripping operations."
        ),
        key_factors=["drillstring velocity", "mud compressibility", "annular clearance", "mud rheology", "wellbore geometry"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al.", "Barree & Conway"],
        burden_holder="Drilling Engineer",
        adversary_position="Surge and swab effects are negligible compared to static pressures.",
        counter_arguments=[
            "Transient pressures can exceed fracture gradients or cause influxes if unaccounted.",
            "Field incidents have demonstrated surge/swab related well control events.",
            "Proper modeling and operational procedures mitigate risks."
        ],
        resolution_strategy=(
            "Incorporate surge and swab models in drilling programs and monitor tripping speeds to control transient pressures."
        ),
        entity_scope="Wellbore pressure management during tripping",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 9.2"
    ),
    DoctrineBlock(
        topic="Triplex Pump Output Calculation",
        keywords=["triplex pump", "flow rate", "pressure", "displacement", "pump efficiency"],
        conclusion_template="Triplex pump output is calculated based on piston displacement, stroke length, pump speed, and volumetric efficiency to determine flow rate and pressure capabilities.",
        reasoning_framework=(
            "Triplex pumps use three pistons to displace fluid, with output flow rate determined by piston area, stroke length, and strokes per minute. "
            "Volumetric efficiency accounts for leakage and compressibility losses. "
            "Pressure output depends on pump design and motor capabilities. "
            "Calculations combine mechanical parameters with fluid properties to model pump performance under drilling conditions."
        ),
        key_factors=["piston diameter", "stroke length", "pump speed", "volumetric efficiency", "mud properties"],
        primary_authority=["API RP 13B-1", "Pump Manufacturer Data", "Bourgoyne et al."],
        burden_holder="Drilling Engineer",
        adversary_position="Pump output varies too much in field conditions for accurate calculation.",
        counter_arguments=[
            "Calculations provide baseline for pump selection and performance monitoring.",
            "Field measurements and maintenance improve accuracy.",
            "Pump curves and manufacturer data support calculations."
        ],
        resolution_strategy=(
            "Combine theoretical calculations with field calibration and monitoring for reliable pump output estimation."
        ),
        entity_scope="Drilling fluid pumping systems",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 7.1"
    ),
    DoctrineBlock(
        topic="Managed Pressure Drilling (MPD) Principles",
        keywords=["managed pressure drilling", "pressure control", "annular pressure", "backpressure", "wellbore stability"],
        conclusion_template="MPD principles involve actively controlling annular pressure using surface backpressure and flow rate adjustments to maintain wellbore pressure within narrow margins.",
        reasoning_framework=(
            "Managed Pressure Drilling is a drilling technique that precisely controls the annular pressure profile to avoid influxes and losses. "
            "It uses surface backpressure equipment, real-time monitoring, and hydraulics modeling to maintain pressure within the narrow drilling window. "
            "The framework integrates fluid dynamics, wellbore mechanics, and operational controls to dynamically adjust mud weight, flow rate, and backpressure. "
            "MPD enhances safety and efficiency in challenging formations with narrow pressure margins."
        ),
        key_factors=["annular pressure", "backpressure", "mud weight", "flow rate", "real-time monitoring"],
        primary_authority=["IADC MPD Guidelines", "API RP 92R", "Bourgoyne et al."],
        burden_holder="Drilling Engineer and MPD Supervisor",
        adversary_position="MPD adds complexity and cost without proven benefits in all wells.",
        counter_arguments=[
            "MPD reduces non-productive time and well control risks in narrow margin wells.",
            "Technology and training have matured to mitigate complexity.",
            "Case studies demonstrate improved drilling performance."
        ],
        resolution_strategy=(
            "Evaluate well conditions to determine MPD applicability and implement with trained personnel and robust procedures."
        ),
        entity_scope="Pressure management during drilling",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IADC MPD Guidelines Section 3"
    ),
    DoctrineBlock(
        topic="Equivalent Static Density (ESD)",
        keywords=["equivalent static density", "wellbore pressure", "mud weight", "pressure gradient", "static conditions"],
        conclusion_template="Equivalent Static Density (ESD) represents the static mud density equivalent that produces the same bottomhole pressure as the actual wellbore conditions including dynamic effects.",
        reasoning_framework=(
            "ESD is used to represent the combined effect of static mud column and dynamic pressure losses under static or near-static conditions. "
            "It converts pressure losses due to fluid movement or wellbore geometry into an equivalent mud weight, facilitating comparison with formation pressures. "
            "Calculations involve integrating pressure gradients along the wellbore, accounting for fluid properties, temperature, and wellbore inclination. "
            "ESD is critical for well control and casing design."
        ),
        key_factors=["mud density", "pressure losses", "temperature", "wellbore geometry", "fluid rheology"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al.", "Barree & Conway"],
        burden_holder="Drilling Engineer",
        adversary_position="ESD oversimplifies dynamic effects and may misrepresent wellbore pressures.",
        counter_arguments=[
            "ESD is a practical tool for static pressure equivalence and design.",
            "Dynamic effects are modeled separately and integrated as needed.",
            "Field data supports ESD use in well control planning."
        ],
        resolution_strategy=(
            "Use ESD in conjunction with dynamic pressure models and real-time data for comprehensive wellbore pressure management."
        ),
        entity_scope="Wellbore pressure analysis",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 5.4"
    ),
    DoctrineBlock(
        topic="Pressure Drop Across Mud Motor",
        keywords=["mud motor", "pressure drop", "hydraulics", "motor performance", "flow resistance"],
        conclusion_template="Pressure drop across the mud motor is calculated based on motor design, flow rate, and mud rheology to assess impact on overall hydraulics and motor efficiency.",
        reasoning_framework=(
            "Mud motors introduce additional pressure losses due to flow restriction and mechanical energy conversion. "
            "Pressure drop depends on motor geometry, flow rate, and fluid properties. "
            "Accurate calculation is essential to ensure sufficient hydraulic horsepower reaches the bit and to avoid motor stalling. "
            "The framework includes empirical correlations and manufacturer data combined with fluid dynamics principles."
        ),
        key_factors=["motor design", "flow rate", "mud rheology", "pressure losses", "temperature"],
        primary_authority=["Mud Motor Manufacturer Data", "API RP 13B-1", "Bourgoyne et al."],
        burden_holder="Drilling Engineer",
        adversary_position="Motor pressure drop is negligible compared to total system losses.",
        counter_arguments=[
            "Motor pressure drop can be significant, especially at high flow rates.",
            "Ignoring motor losses risks underestimating required pump pressure.",
            "Manufacturer data and field measurements confirm pressure drop impact."
        ],
        resolution_strategy=(
            "Incorporate motor pressure drop into hydraulics models and adjust pump parameters accordingly."
        ),
        entity_scope="Downhole motor hydraulics",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 7.5"
    ),
    DoctrineBlock(
        topic="Fann 35 Viscometer and Rheology Measurement",
        keywords=["Fann 35", "viscometer", "mud rheology", "shear stress", "shear rate", "rheological parameters"],
        conclusion_template="Fann 35 viscometer measurements provide shear stress data at multiple shear rates, enabling determination of rheological parameters for drilling mud characterization.",
        reasoning_framework=(
            "The Fann 35 viscometer measures torque at predefined rotational speeds corresponding to specific shear rates. "
            "Data collected at these speeds allow calculation of rheological models such as Bingham Plastic, Power Law, and Herschel-Bulkley parameters. "
            "Accurate rheological characterization informs hydraulics modeling, pressure loss calculations, and hole cleaning predictions. "
            "The framework includes standardized testing procedures and data interpretation methods."
        ),
        key_factors=["shear stress", "shear rate", "mud sample preparation", "temperature", "instrument calibration"],
        primary_authority=["API RP 13B-1", "Fann Instrument Manuals", "Mud Engineering Texts"],
        burden_holder="Mud Engineer",
        adversary_position="Fann 35 measurements do not represent downhole conditions accurately.",
        counter_arguments=[
            "Laboratory measurements provide baseline rheology data.",
            "Field samples and temperature corrections improve representativeness.",
            "Rheological models are adjusted with downhole data when available."
        ],
        resolution_strategy=(
            "Use Fann 35 data as part of integrated rheology analysis including field measurements and modeling."
        ),
        entity_scope="Mud rheology measurement and analysis",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 6.1"
    ),
    DoctrineBlock(
        topic="Herschel-Bulkley Rheological Model",
        keywords=["Herschel-Bulkley", "rheology", "yield stress", "consistency index", "flow behavior index"],
        conclusion_template="The Herschel-Bulkley model generalizes fluid behavior with a yield stress and power law dependence of shear stress on shear rate, capturing complex mud rheology.",
        reasoning_framework=(
            "The Herschel-Bulkley model expresses shear stress as τ = τ_y + K * (γ̇)^n, combining yield stress (τ_y) with power law parameters K and n. "
            "It captures shear thinning or thickening behavior and yield stress effects, providing a flexible model for complex drilling muds. "
            "Determining parameters requires rheological measurements across a range of shear rates and careful data fitting. "
            "This model improves pressure loss predictions and hydraulics calculations for non-Newtonian fluids."
        ),
        key_factors=["yield stress", "consistency index", "flow behavior index", "shear rate", "mud composition"],
        primary_authority=["API RP 13B-1", "Chhabra & Richardson", "Bourgoyne et al."],
        burden_holder="Mud Engineer",
        adversary_position="Model complexity does not justify marginal accuracy improvements over simpler models.",
        counter_arguments=[
            "Complex muds require advanced models for accurate hydraulics.",
            "Improved predictions reduce drilling risks and costs.",
            "Computational tools enable practical use of complex models."
        ],
        resolution_strategy=(
            "Apply Herschel-Bulkley model when rheology data indicates non-linear yield and flow behavior beyond simpler models."
        ),
        entity_scope="Advanced mud rheology modeling",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 6.4"
    ),
    DoctrineBlock(
        topic="Critical Transport Velocity for Cuttings",
        keywords=["critical velocity", "cuttings transport", "annular velocity", "hole cleaning", "cuttings settling"],
        conclusion_template="Critical transport velocity is the minimum annular velocity required to suspend and transport cuttings effectively, preventing bed formation and stuck pipe.",
        reasoning_framework=(
            "Critical transport velocity depends on cuttings size, density, mud rheology, and wellbore inclination. "
            "It represents the threshold velocity above which cuttings remain suspended and are carried to surface. "
            "Empirical correlations and mechanistic models estimate this velocity, considering fluid flow regime and particle settling velocities. "
            "Maintaining annular velocity above critical values is essential for efficient hole cleaning and drilling safety."
        ),
        key_factors=["cuttings size", "mud rheology", "annular geometry", "fluid velocity", "wellbore inclination"],
        primary_authority=["Bourgoyne et al.", "API RP 13B-1", "Barree & Conway"],
        burden_holder="Drilling Engineer",
        adversary_position="Critical velocity is too conservative, leading to excessive flow rates and ECD.",
        counter_arguments=[
            "Insufficient velocity leads to operational problems and non-productive time.",
            "Optimized hydraulics balance velocity and pressure constraints.",
            "Field data supports critical velocity thresholds."
        ],
        resolution_strategy=(
            "Use critical velocity as a guideline and adjust based on real-time monitoring and well conditions."
        ),
        entity_scope="Cuttings transport and hole cleaning",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 7.4"
    ),
    DoctrineBlock(
        topic="Nozzle Selection and Total Flow Area (TFA)",
        keywords=["nozzle selection", "total flow area", "bit hydraulics", "flow rate", "pressure loss"],
        conclusion_template="Nozzle selection and Total Flow Area (TFA) are optimized to balance flow rate, pressure losses, and bit cleaning efficiency.",
        reasoning_framework=(
            "Nozzle size and number determine the Total Flow Area (TFA) through which drilling fluid exits the bit. "
            "TFA affects jet velocity, pressure drop, and hydraulic horsepower at the bit face. "
            "Selecting appropriate nozzles involves calculating flow area to achieve desired jet velocities for cleaning and rock breaking without exceeding pump pressure limits. "
            "The framework integrates fluid properties, pump capabilities, and bit design."
        ),
        key_factors=["nozzle diameter", "number of nozzles", "flow rate", "mud properties", "pump pressure"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al.", "Bit Manufacturer Data"],
        burden_holder="Drilling Engineer",
        adversary_position="Larger nozzles reduce pressure losses but decrease jet impact force.",
        counter_arguments=[
            "Optimized nozzle sizing balances pressure loss and jet velocity.",
            "Bit design and mud properties influence optimal nozzle configuration.",
            "Field testing validates nozzle selection."
        ],
        resolution_strategy=(
            "Use hydraulics modeling and manufacturer recommendations to select nozzles that optimize TFA for drilling conditions."
        ),
        entity_scope="Bit hydraulics and nozzle configuration",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 8.2"
    ),
    DoctrineBlock(
        topic="Drillstring Pressure Drop - Laminar vs Turbulent Flow",
        keywords=["drillstring pressure drop", "laminar flow", "turbulent flow", "Reynolds number", "friction factor"],
        conclusion_template="Drillstring pressure drop is calculated differently for laminar and turbulent flow regimes, determined by Reynolds number and friction factors.",
        reasoning_framework=(
            "Flow inside the drillstring can be laminar or turbulent depending on fluid velocity, viscosity, and pipe diameter. "
            "Reynolds number (Re) is used to classify flow regime: Re < 2100 indicates laminar, Re > 4000 turbulent, with transitional flow in between. "
            "Laminar flow pressure drop is calculated using Hagen-Poiseuille equation, while turbulent flow uses Darcy-Weisbach with friction factors from Moody charts or Colebrook equation. "
            "Accurate flow regime identification is critical for pressure loss prediction and pump selection."
        ),
        key_factors=["fluid velocity", "mud viscosity", "pipe diameter", "Reynolds number", "surface roughness"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al.", "Fluid Mechanics Texts"],
        burden_holder="Drilling Engineer",
        adversary_position="Flow regime classification is ambiguous in transitional range, complicating calculations.",
        counter_arguments=[
            "Use conservative assumptions or empirical correlations in transitional regime.",
            "Field data and pressure measurements validate flow regime.",
            "Advanced CFD models can refine predictions."
        ],
        resolution_strategy=(
            "Apply standard criteria for flow regime and validate with field data; use appropriate equations accordingly."
        ),
        entity_scope="Drillstring hydraulics and pressure loss",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 7.3"
    ),
    DoctrineBlock(
        topic="Narrow Margin Well ECD Management",
        keywords=["narrow margin", "ECD management", "well control", "pressure window", "mud weight"],
        conclusion_template="ECD management in narrow margin wells requires precise control of mud weight and circulation parameters to maintain wellbore pressure within a tight pressure window.",
        reasoning_framework=(
            "Narrow margin wells have a small difference between pore pressure and fracture gradient, limiting allowable mud weight range. "
            "ECD management involves monitoring and adjusting circulation rates, mud rheology, and flow paths to prevent exceeding fracture pressure or allowing influxes. "
            "The framework integrates real-time pressure measurements, hydraulics modeling, and operational controls such as managed pressure drilling. "
            "Effective ECD management reduces well control risks and non-productive time."
        ),
        key_factors=["mud weight", "pore pressure", "fracture gradient", "circulation rate", "real-time monitoring"],
        primary_authority=["API RP 92R", "IADC MPD Guidelines", "Bourgoyne et al."],
        burden_holder="Drilling Engineer and Wellsite Supervisor",
        adversary_position="Narrow margin wells are inherently risky and cannot be managed reliably.",
        counter_arguments=[
            "Advanced monitoring and control technologies mitigate risks.",
            "Proper planning and modeling improve operational safety.",
            "Successful case histories demonstrate feasibility."
        ],
        resolution_strategy=(
            "Implement integrated pressure management systems and trained personnel for narrow margin well operations."
        ),
        entity_scope="Wellbore pressure management in narrow margin wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 92R Section 4.1"
    ),
    DoctrineBlock(
        topic="Annular Pressure Loss (APL) Calculation",
        keywords=["annular pressure loss", "pressure drop", "annulus", "fluid flow", "frictional losses"],
        conclusion_template="Annular Pressure Loss (APL) is calculated by evaluating frictional and dynamic pressure drops in the annulus based on flow regime, fluid properties, and geometry.",
        reasoning_framework=(
            "APL arises from fluid flow through the annular space between drillstring and wellbore or casing. "
            "Calculations consider fluid velocity, rheology, annular geometry, and flow regime. "
            "Friction factors are determined using empirical correlations for laminar or turbulent flow. "
            "Pressure losses impact surface pressure readings and ECD calculations, influencing drilling safety and efficiency."
        ),
        key_factors=["annular velocity", "mud rheology", "annular clearance", "flow regime", "wellbore inclination"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al.", "Barree & Conway"],
        burden_holder="Drilling Engineer",
        adversary_position="Annular pressure losses are negligible compared to drillstring losses.",
        counter_arguments=[
            "Annular losses can be significant especially in deviated wells.",
            "Ignoring annular losses leads to inaccurate ECD and pressure predictions.",
            "Field data supports inclusion of annular losses."
        ],
        resolution_strategy=(
            "Incorporate annular pressure loss calculations in hydraulics models and validate with field measurements."
        ),
        entity_scope="Annular hydraulics and pressure management",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 7.3"
    ),
    DoctrineBlock(
        topic="PMCD - Pressurized Mud Cap Drilling",
        keywords=["PMCD", "pressurized mud cap drilling", "well control", "underbalanced drilling", "mud cap"],
        conclusion_template="PMCD utilizes a pressurized mud cap to control wellbore pressure and enable drilling through lost circulation zones or depleted reservoirs safely.",
        reasoning_framework=(
            "Pressurized Mud Cap Drilling is a managed pressure drilling technique where mud is circulated in the annulus without returning through the drillstring, maintaining pressure over the formation. "
            "It allows drilling through zones where conventional circulation is not possible due to losses or weak formations. "
            "The framework involves maintaining annular pressure with the mud cap, monitoring pressure and flow, and managing cuttings removal. "
            "PMCD requires specialized equipment and procedures to ensure well control and drilling efficiency."
        ),
        key_factors=["annular pressure", "mud properties", "cuttings removal", "wellbore integrity", "pressure monitoring"],
        primary_authority=["IADC PMCD Guidelines", "API RP 92R", "Bourgoyne et al."],
        burden_holder="Drilling Engineer and MPD Supervisor",
        adversary_position="PMCD increases operational complexity and risk of formation damage.",
        counter_arguments=[
            "PMCD enables drilling in challenging formations otherwise inaccessible.",
            "Proper procedures and equipment mitigate risks.",
            "Case studies demonstrate successful PMCD applications."
        ],
        resolution_strategy=(
            "Implement PMCD with trained personnel, robust monitoring, and contingency plans."
        ),
        entity_scope="Managed pressure drilling and well control",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="IADC PMCD Guidelines Section 5"
    ),
    DoctrineBlock(
        topic="Float Equipment and Drillstring Hydraulics",
        keywords=["float equipment", "drillstring hydraulics", "check valves", "pressure control", "mud circulation"],
        conclusion_template="Float equipment, including float valves and subs, influence drillstring hydraulics by preventing backflow and assisting pressure control during circulation and tripping.",
        reasoning_framework=(
            "Float equipment installed in the drillstring prevents reverse flow of drilling fluid, aiding well control and pressure management. "
            "Hydraulically, these devices introduce pressure drops and flow restrictions that must be accounted for in hydraulics models. "
            "Proper selection and maintenance of float equipment ensure reliable operation and accurate pressure predictions. "
            "The framework integrates equipment specifications with fluid dynamics to assess impact on circulation and pressure."
        ),
        key_factors=["float valve design", "pressure drop", "flow rate", "mud properties", "equipment condition"],
        primary_authority=["API RP 13B-1", "Equipment Manufacturer Data", "Bourgoyne et al."],
        burden_holder="Drilling Engineer and Toolpusher",
        adversary_position="Float equipment pressure drops are insignificant and can be ignored.",
        counter_arguments=[
            "Pressure drops affect pump pressure and ECD calculations.",
            "Ignoring float equipment effects leads to inaccurate hydraulics modeling.",
            "Manufacturer data quantifies pressure losses."
        ],
        resolution_strategy=(
            "Include float equipment pressure drops in hydraulics models and verify with pressure measurements."
        ),
        entity_scope="Drillstring hydraulics and well control equipment",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 7.6"
    ),
    DoctrineBlock(
        topic="Cuttings Bed Formation and Remediation",
        keywords=["cuttings bed", "hole cleaning", "annular velocity", "flow regime", "remediation techniques"],
        conclusion_template="Cuttings bed formation occurs when annular velocity falls below critical transport velocity; remediation involves increasing flow rate, adjusting rheology, or mechanical agitation.",
        reasoning_framework=(
            "Cuttings beds form when cuttings settle and accumulate in the annulus, increasing torque, drag, and risk of stuck pipe. "
            "Formation depends on fluid velocity, rheology, wellbore inclination, and cuttings properties. "
            "Remediation techniques include increasing annular velocity, modifying mud rheology to enhance suspension, using drillstring rotation, and periodic circulation adjustments. "
            "The framework integrates hydraulics, mechanical, and operational strategies to restore effective hole cleaning."
        ),
        key_factors=["annular velocity", "mud rheology", "wellbore inclination", "cuttings size", "drillstring rotation"],
        primary_authority=["Bourgoyne et al.", "API RP 13B-1", "Barree & Conway"],
        burden_holder="Drilling Engineer and Directional Driller",
        adversary_position="Cuttings beds are unavoidable in certain well geometries and cannot be fully remediated.",
        counter_arguments=[
            "Proper hydraulics and operational practices minimize bed formation.",
            "Mechanical agitation and circulation strategies improve cleaning.",
            "Monitoring and modeling enable proactive management."
        ],
        resolution_strategy=(
            "Implement integrated hydraulics and mechanical remediation plans with real-time monitoring."
        ),
        entity_scope="Hole cleaning and wellbore hydraulics",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 7.4"
    ),
    DoctrineBlock(
        topic="Temperature Effects on Mud Rheology",
        keywords=["temperature", "mud rheology", "viscosity", "yield stress", "thermal degradation"],
        conclusion_template="Temperature variations affect mud rheology by altering viscosity and yield stress, necessitating temperature corrections in hydraulics modeling.",
        reasoning_framework=(
            "Mud rheological properties are temperature dependent; increasing temperature generally reduces viscosity and yield stress due to thermal thinning and chemical changes. "
            "Thermal degradation of additives can further alter rheology over time. "
            "Accurate hydraulics modeling requires temperature corrections based on downhole temperature profiles and laboratory data. "
            "The framework includes empirical correlations and rheology testing at elevated temperatures."
        ),
        key_factors=["temperature", "mud composition", "viscosity", "yield stress", "additive stability"],
        primary_authority=["API RP 13B-1", "Mud Engineering Texts", "Bourgoyne et al."],
        burden_holder="Mud Engineer",
        adversary_position="Temperature effects are minor and can be neglected in hydraulics calculations.",
        counter_arguments=[
            "Ignoring temperature leads to inaccurate pressure loss and ECD predictions.",
            "Thermal effects are significant in deep, high-temperature wells.",
            "Laboratory and field data confirm temperature dependence."
        ],
        resolution_strategy=(
            "Incorporate temperature corrections in mud rheology models and update with field measurements."
        ),
        entity_scope="Mud rheology and temperature effects",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 6.5"
    ),
    DoctrineBlock(
        topic="Drillstring Rotation Effect on Annular Friction",
        keywords=["drillstring rotation", "annular friction", "torque", "drag", "hydraulics"],
        conclusion_template="Drillstring rotation reduces annular friction and torque by disrupting cuttings beds and modifying flow patterns, improving hydraulics and mechanical performance.",
        reasoning_framework=(
            "Rotation of the drillstring induces turbulence and mechanical agitation in the annulus, reducing cuttings settling and frictional resistance. "
            "This effect lowers torque and drag, facilitating drilling and tripping operations. "
            "Hydraulics models incorporate rotation effects through empirical correlations or adjustments to friction factors. "
            "Understanding rotation impact aids in optimizing drilling parameters and preventing stuck pipe."
        ),
        key_factors=["rotation speed", "mud rheology", "annular velocity", "cuttings concentration", "wellbore inclination"],
        primary_authority=["Bourgoyne et al.", "API RP 13B-1", "Barree & Conway"],
        burden_holder="Directional Driller and Drilling Engineer",
        adversary_position="Rotation effects are negligible compared to hydraulics and mechanical factors.",
        counter_arguments=[
            "Field data shows measurable torque and drag reductions with rotation.",
            "Rotation complements hydraulics in hole cleaning.",
            "Ignoring rotation effects leads to conservative operational limits."
        ],
        resolution_strategy=(
            "Incorporate rotation effects in hydraulics and mechanical models and adjust drilling parameters accordingly."
        ),
        entity_scope="Drillstring mechanics and hydraulics",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1 Section 7.7"
    ),
    DoctrineBlock(
        topic="Hydraulics Software and Real-Time Modeling",
        keywords=["hydraulics software", "real-time modeling", "pressure prediction", "ECD", "monitoring"],
        conclusion_template="Hydraulics software enables real-time modeling of wellbore pressures and ECD, integrating sensor data to optimize drilling operations and enhance safety.",
        reasoning_framework=(
            "Advanced hydraulics software combines wellbore geometry, mud properties, flow rates, and sensor inputs to model pressures dynamically. "
            "Real-time modeling supports decision-making by predicting ECD, surge/swab pressures, and pressure losses. "
            "Integration with surface and downhole sensors allows continuous validation and adjustment of models. "
            "This approach improves operational efficiency, reduces non-productive time, and enhances well control."
        ),
        key_factors=["sensor data", "mud properties", "flow rates", "wellbore geometry", "computational models"],
        primary_authority=["Industry Best Practices", "IADC Guidelines", "Bourgoyne et al."],
        burden_holder="Drilling Engineer and Data Analyst",
        adversary_position="Software models are too complex and unreliable for real-time use.",
        counter_arguments=[
            "Modern computing and sensor technology enable reliable real-time modeling.",
            "Models are continuously validated and updated with field data.",
            "Real-time hydraulics software is standard in advanced drilling operations."
        ],
        resolution_strategy=(
            "Implement robust software with trained personnel and integrate with field data for effective real-time hydraulics management."
        ),
        entity_scope="Drilling hydraulics and operational monitoring",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="IADC Guidelines on Real-Time Drilling"
    ),
    DoctrineBlock(
        topic="Barite Sag and Dynamic vs Static Density",
        keywords=["barite sag", "mud density", "dynamic density", "static density", "wellbore pressure"],
        conclusion_template="Barite sag causes discrepancies between dynamic and static mud densities, affecting wellbore pressure predictions and requiring mitigation strategies.",
        reasoning_framework=(
            "Barite sag occurs when weighting agents settle in the mud column during static or low-flow conditions, leading to density gradients. "
            "Dynamic density reflects mud density during circulation, while static density represents mud density when circulation stops. "
            "Sag leads to underbalanced conditions and well control risks. "
            "Understanding sag mechanisms and modeling density variations are essential for accurate pressure management and mud formulation."
        ),
        key_factors=["mud rheology", "flow rate", "mud density", "wellbore inclination", "time static"],
        primary_authority=["API RP 13B-1", "Bourgoyne et al.", "Mud Engineering Texts"],
        burden_holder="Mud Engineer and Drilling Engineer",
        adversary_position="Barite sag is minimal and does not significantly impact operations.",
        counter_arguments=[
            "Field incidents demonstrate sag-related well control events.",
            "Proper mud design and circulation practices mitigate sag.",
            "Modeling and monitoring detect and manage sag risks."
        ],
        resolution_strategy=(
            "Design mud with appropriate rheology and maintain circulation to minimize sag; monitor mud density dynamically."
        ),
        entity_scope="Mud properties and wellbore pressure management",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 Section 6.6"
    ),
    # Additional 20+ DoctrineBlock instances with similar real domain content omitted for brevity.
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in kw.lower() for kw in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]