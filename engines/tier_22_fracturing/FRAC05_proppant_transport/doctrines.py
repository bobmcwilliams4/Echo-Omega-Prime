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
        topic="Proppant Settling: Stokes Law",
        keywords=["proppant", "settling", "Stokes law", "terminal velocity", "laminar flow"],
        conclusion_template="Proppant settling velocity in dilute, laminar flow regimes is governed by Stokes Law, subject to particle size, fluid viscosity, and density contrast.",
        reasoning_framework="""
        Stokes Law applies to the settling of small, spherical particles in a Newtonian fluid under laminar flow conditions (Re < 0.1). The terminal settling velocity is calculated as:
            v = (2/9) * (r^2 * (ρ_p - ρ_f) * g) / μ
        where r is particle radius, ρ_p is proppant density, ρ_f is fluid density, g is gravity, and μ is fluid viscosity. Assumptions include negligible particle-particle interactions and no turbulence. Deviations occur at higher concentrations or Reynolds numbers.
        """,
        key_factors=["Particle diameter", "Fluid viscosity", "Density difference", "Laminar regime"],
        primary_authority=["C.W. Stokes (1851)", "API RP 19C", "SPE Monograph 12"],
        burden_holder="Design Engineer",
        adversary_position="Settling is overestimated in field conditions due to turbulence and hindered effects.",
        counter_arguments=[
            "Field conditions often deviate from ideal Stokes regime.",
            "Particle shape and non-Newtonian fluids alter settling rates."
        ],
        resolution_strategy="Validate regime applicability via Reynolds number; adjust for hindered settling if concentration is high.",
        entity_scope="Hydraulic Fracturing Fluids",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SPE 122887"
    ),
    DoctrineBlock(
        topic="Proppant Settling: Hindered Settling",
        keywords=["proppant", "settling", "hindered settling", "concentration", "settling velocity"],
        conclusion_template="At elevated proppant concentrations, settling velocity is reduced due to hindered settling effects, requiring empirical or semi-empirical corrections.",
        reasoning_framework="""
        Hindered settling occurs when particle concentration increases, causing interactions that reduce individual particle velocities. The Richardson-Zaki equation is commonly used:
            v_h = v_0 * (1 - C/C_max)^n
        where v_h is hindered velocity, v_0 is single-particle velocity, C is solids volume fraction, C_max is maximum packing, and n is an empirical exponent. Laboratory calibration is required for accurate field application.
        """,
        key_factors=["Proppant concentration", "Particle interactions", "Empirical exponent", "Maximum packing"],
        primary_authority=["Richardson & Zaki (1954)", "SPE 169009", "API RP 19C"],
        burden_holder="Fracture Modeler",
        adversary_position="Hindered settling is overcorrected, leading to underestimation of proppant transport.",
        counter_arguments=[
            "Empirical exponents may not match field conditions.",
            "Non-spherical particles deviate from theory."
        ],
        resolution_strategy="Calibrate hindered settling models with lab/field data; use conservative estimates for design.",
        entity_scope="Proppant-Laden Fluids",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Convection: Tip Accumulation",
        keywords=["proppant", "convection", "tip accumulation", "fracture tip", "transport"],
        conclusion_template="Proppant accumulation at the fracture tip is governed by the balance of convective transport and settling, impacting fracture extension and conductivity.",
        reasoning_framework="""
        As slurry advances, proppant is transported by fluid convection toward the fracture tip. Settling and filtration at the tip can cause accumulation, potentially leading to tip screen-out (TSO). The interplay between fluid velocity, proppant concentration, and settling rate determines the extent of tip accumulation. Design must ensure proppant does not bridge prematurely, allowing for desired fracture geometry.
        """,
        key_factors=["Slurry velocity", "Proppant concentration", "Settling rate", "Fracture width"],
        primary_authority=["SPE 152232", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Tip accumulation is overstated; field fractures rarely screen out at the tip.",
        counter_arguments=[
            "Field diagnostics show TSO is common in low-viscosity fluids.",
            "High proppant loading increases risk of tip bridging."
        ],
        resolution_strategy="Model tip accumulation using coupled transport-settling equations; monitor for TSO indicators.",
        entity_scope="Hydraulic Fracture Tips",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 152232"
    ),
    DoctrineBlock(
        topic="Proppant Convection: Gravity Currents",
        keywords=["proppant", "gravity current", "convection", "density", "transport"],
        conclusion_template="Gravity-driven proppant currents can enhance lateral transport, especially in low-viscosity fluids and wide fractures.",
        reasoning_framework="""
        Proppant-laden fluids are denser than clear fracturing fluids, creating gravity currents that flow along the fracture bottom. The current's advance is governed by the density difference, fracture aperture, and fluid viscosity. Gravity currents are modeled using shallow-water equations and can significantly increase proppant distribution distance, particularly in slickwater treatments.
        """,
        key_factors=["Density difference", "Fracture aperture", "Fluid viscosity", "Injection rate"],
        primary_authority=["SPE 123456", "Barree & Conway (1995)", "API RP 19C"],
        burden_holder="Fracture Modeler",
        adversary_position="Gravity currents are negligible in narrow, high-viscosity fractures.",
        counter_arguments=[
            "Field evidence shows enhanced transport in slickwater jobs.",
            "Gravity effects diminish at high viscosity."
        ],
        resolution_strategy="Assess gravity current potential based on fluid and fracture properties; adjust design as needed.",
        entity_scope="Fracture Lateral Transport",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 123456"
    ),
    DoctrineBlock(
        topic="Slurry Rheology: Power Law Model",
        keywords=["slurry", "rheology", "power law", "non-Newtonian", "viscosity"],
        conclusion_template="The Power Law model describes the shear-thinning behavior of fracturing slurries, informing viscosity and pressure drop calculations.",
        reasoning_framework="""
        Many fracturing fluids exhibit non-Newtonian, shear-thinning behavior, well described by the Power Law:
            τ = K * (γ̇)^n
        where τ is shear stress, K is consistency index, γ̇ is shear rate, and n is flow behavior index (<1 for shear-thinning). The apparent viscosity decreases with increasing shear rate. Accurate rheological characterization is essential for pressure prediction and proppant transport modeling.
        """,
        key_factors=["Consistency index (K)", "Flow behavior index (n)", "Shear rate", "Temperature"],
        primary_authority=["API RP 13B-1", "SPE 169009", "SPE Monograph 12"],
        burden_holder="Fluid Engineer",
        adversary_position="Power Law oversimplifies real fluid behavior, especially at low shear rates.",
        counter_arguments=[
            "Yield stress and thixotropy are not captured.",
            "Lab-measured parameters may not match field conditions."
        ],
        resolution_strategy="Use Power Law for first-order design; validate with field data and advanced models as needed.",
        entity_scope="Fracturing Fluids",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Slurry Rheology: Herschel-Bulkley Model",
        keywords=["slurry", "rheology", "Herschel-Bulkley", "yield stress", "non-Newtonian"],
        conclusion_template="The Herschel-Bulkley model extends the Power Law to include yield stress, providing a more accurate description of fracturing fluid rheology.",
        reasoning_framework="""
        The Herschel-Bulkley model is defined as:
            τ = τ_y + K * (γ̇)^n
        where τ_y is the yield stress, K is consistency index, γ̇ is shear rate, and n is flow behavior index. This model captures both shear-thinning and the minimum stress required for flow. It is especially relevant for gels and crosslinked fluids. Accurate yield stress measurement is critical for predicting proppant suspension and transport.
        """,
        key_factors=["Yield stress (τ_y)", "Consistency index (K)", "Flow behavior index (n)", "Shear rate"],
        primary_authority=["API RP 13B-1", "SPE 169009", "SPE 18212"],
        burden_holder="Fluid Engineer",
        adversary_position="Yield stress is often overestimated in field conditions.",
        counter_arguments=[
            "Temperature and shear history affect yield stress.",
            "Field measurements are challenging."
        ],
        resolution_strategy="Calibrate model parameters with field/lab data; use conservative values for design.",
        entity_scope="Fracturing Fluids",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 18212"
    ),
    DoctrineBlock(
        topic="Proppant Concentration: Maximum Packing Fraction",
        keywords=["proppant", "concentration", "packing fraction", "maximum", "slurry"],
        conclusion_template="The maximum proppant concentration in slurry is limited by the maximum packing fraction, typically 0.55-0.64 for spherical particles.",
        reasoning_framework="""
        The maximum packing fraction (C_max) is the highest volume fraction of proppant achievable in a slurry before bridging or plugging occurs. For monodisperse, spherical particles, C_max is about 0.64 (random close packing). In practice, due to particle shape and size distribution, C_max is often lower. Exceeding C_max leads to rapid viscosity increase and loss of mobility.
        """,
        key_factors=["Particle size distribution", "Particle shape", "Slurry mixing", "Bridging risk"],
        primary_authority=["SPE 169009", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Design Engineer",
        adversary_position="Higher concentrations can be achieved with optimized blends.",
        counter_arguments=[
            "Field mixing often results in lower effective packing.",
            "Non-spherical particles reduce C_max."
        ],
        resolution_strategy="Determine C_max experimentally for each proppant blend; avoid exceeding during design.",
        entity_scope="Proppant-Laden Slurries",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Distribution: Microseismic Mapping",
        keywords=["proppant", "distribution", "microseismic", "mapping", "diagnostics"],
        conclusion_template="Microseismic mapping provides indirect evidence of fracture geometry and proppant distribution, but does not directly image proppant placement.",
        reasoning_framework="""
        Microseismic monitoring detects acoustic emissions from fracture propagation, allowing inference of fracture geometry. While it provides valuable spatial and temporal information, it does not directly image proppant. Correlation with injection data and other diagnostics is needed to estimate proppant placement. Uncertainties arise from event location accuracy and interpretation assumptions.
        """,
        key_factors=["Event location accuracy", "Fracture geometry", "Injection data", "Interpretation methods"],
        primary_authority=["SPE 119896", "API RP 19C", "Warpinski et al. (2005)"],
        burden_holder="Geophysicist",
        adversary_position="Microseismic data overstates proppant coverage.",
        counter_arguments=[
            "Events may not correlate with proppant transport.",
            "Interpretation is model-dependent."
        ],
        resolution_strategy="Integrate microseismic with other diagnostics (e.g., tracers, fiber optics) for robust interpretation.",
        entity_scope="Hydraulic Fracturing Diagnostics",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="SPE 119896"
    ),
    DoctrineBlock(
        topic="Proppant Distribution: Fiber Optic Mapping",
        keywords=["proppant", "distribution", "fiber optic", "DAS", "DTS", "mapping"],
        conclusion_template="Fiber optic sensing (DAS/DTS) enables high-resolution mapping of proppant placement via temperature and acoustic signatures.",
        reasoning_framework="""
        Distributed Acoustic Sensing (DAS) and Distributed Temperature Sensing (DTS) use fiber optic cables to monitor acoustic and thermal changes along the wellbore. Proppant placement alters fluid flow and heat transfer, producing detectable signals. These methods provide continuous, real-time data, but interpretation requires advanced analytics and calibration.
        """,
        key_factors=["Fiber optic installation", "Signal processing", "Calibration", "Integration with other diagnostics"],
        primary_authority=["SPE 187451", "API RP 19C", "Schlumberger FiberSensing"],
        burden_holder="Production Engineer",
        adversary_position="Fiber optic signals are ambiguous and may not uniquely indicate proppant.",
        counter_arguments=[
            "Noise and environmental factors affect signal quality.",
            "Requires correlation with other data."
        ],
        resolution_strategy="Use fiber optics as part of a multi-diagnostic approach; validate with tracers or microseismic.",
        entity_scope="Fracture Diagnostics",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 187451"
    ),
    DoctrineBlock(
        topic="Proppant Flowback: Screen-Out",
        keywords=["proppant", "flowback", "screen-out", "fracture closure", "production"],
        conclusion_template="Screen-out occurs when proppant bridges or plugs the fracture, halting fluid flow and potentially damaging conductivity.",
        reasoning_framework="""
        Screen-out is the cessation of proppant and fluid injection due to bridging or plugging within the fracture or at the wellbore. Causes include excessive proppant concentration, rapid closure, or insufficient fluid velocity. Screen-out can reduce fracture conductivity and complicate well cleanup. Prevention involves careful design of ramp schedules and monitoring of pressure trends.
        """,
        key_factors=["Proppant concentration", "Fracture width", "Closure rate", "Injection pressure"],
        primary_authority=["API RP 19C", "SPE 169009", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Screen-out risk is overstated with modern fluids and monitoring.",
        counter_arguments=[
            "Unexpected formation heterogeneity can cause screen-out.",
            "Real-time monitoring may not prevent all incidents."
        ],
        resolution_strategy="Implement real-time monitoring and adaptive ramp schedules; design for contingencies.",
        entity_scope="Fracture Treatment Operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Flowback: Bridging",
        keywords=["proppant", "flowback", "bridging", "fracture width", "particle size"],
        conclusion_template="Bridging occurs when proppant particles span the fracture width, impeding flow and risking screen-out.",
        reasoning_framework="""
        Proppant bridging is a function of particle size relative to fracture width. When the width approaches 2-3 times the particle diameter, bridging is likely. This can halt proppant transport and cause screen-out. Design must ensure fracture width exceeds bridging threshold throughout treatment.
        """,
        key_factors=["Particle size", "Fracture width", "Proppant concentration", "Fluid velocity"],
        primary_authority=["SPE 169009", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Design Engineer",
        adversary_position="Bridging is rare with properly selected proppant sizes.",
        counter_arguments=[
            "Fracture width can decrease rapidly during closure.",
            "Heterogeneous formations increase bridging risk."
        ],
        resolution_strategy="Select proppant size based on minimum expected fracture width; monitor for pressure spikes.",
        entity_scope="Fracture Geometry",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Flowback: Tail-In",
        keywords=["proppant", "flowback", "tail-in", "fine proppant", "screen-out prevention"],
        conclusion_template="Tail-in with fine proppant at the end of treatment reduces screen-out risk and improves fracture conductivity near the wellbore.",
        reasoning_framework="""
        The tail-in stage involves switching to finer proppant (e.g., 100-mesh) during the final phase of pumping. This reduces bridging and screen-out risk as the fracture closes and narrows. Fine proppant also enhances near-wellbore conductivity and cleanup. Tail-in design must balance screen-out prevention with long-term conductivity requirements.
        """,
        key_factors=["Proppant size", "Fracture closure", "Pumping schedule", "Conductivity"],
        primary_authority=["API RP 19C", "SPE 169009", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Fine proppant reduces long-term conductivity due to embedment and crush.",
        counter_arguments=[
            "Field data show improved cleanup with tail-in.",
            "Conductivity loss can be mitigated by blend optimization."
        ],
        resolution_strategy="Optimize tail-in schedule and proppant blend; monitor post-treatment conductivity.",
        entity_scope="Fracture Treatment Design",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Crush Strength: API RP 19C Conductivity",
        keywords=["proppant", "crush strength", "API RP 19C", "conductivity", "stress"],
        conclusion_template="Proppant crush strength, as measured by API RP 19C, is a key determinant of retained fracture conductivity under closure stress.",
        reasoning_framework="""
        API RP 19C specifies standardized methods for measuring proppant crush resistance and conductivity under stress. Higher crush strength correlates with better long-term conductivity, especially in deep, high-stress reservoirs. However, lab results may overestimate field performance due to embedment and fines generation.
        """,
        key_factors=["Closure stress", "Proppant type", "Fines generation", "Lab vs field conditions"],
        primary_authority=["API RP 19C", "SPE 169009", "SPE 18212"],
        burden_holder="Completion Engineer",
        adversary_position="API tests do not reflect field embedment and fines migration.",
        counter_arguments=[
            "Field corrections are available for embedment effects.",
            "Ceramic proppants outperform sand at high stress."
        ],
        resolution_strategy="Apply field correction factors to lab data; select proppant based on in-situ stress.",
        entity_scope="Proppant Selection",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Embedment: Soft Formation Conductivity Loss",
        keywords=["proppant", "embedment", "soft formation", "conductivity loss", "closure stress"],
        conclusion_template="Proppant embedment in soft formations reduces fracture conductivity, especially at high closure stress.",
        reasoning_framework="""
        In soft or unconsolidated formations, proppant particles can embed into the fracture faces under closure stress, reducing fracture width and conductivity. The extent of embedment depends on rock hardness, proppant size, and stress magnitude. Laboratory tests and field data are used to estimate embedment and adjust conductivity predictions.
        """,
        key_factors=["Rock hardness", "Closure stress", "Proppant size", "Formation mineralogy"],
        primary_authority=["SPE 169009", "API RP 19C", "SPE 18212"],
        burden_holder="Reservoir Engineer",
        adversary_position="Embedment is negligible in competent formations.",
        counter_arguments=[
            "Soft formations are common in unconventionals.",
            "Embedment is a leading cause of conductivity loss."
        ],
        resolution_strategy="Assess formation hardness; apply embedment corrections in conductivity models.",
        entity_scope="Fracture Conductivity",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Conductivity: Lab vs Field Correction Factors",
        keywords=["proppant", "conductivity", "lab", "field", "correction factors"],
        conclusion_template="Lab-measured proppant conductivity must be corrected for field conditions, including embedment, fines migration, and stress cycling.",
        reasoning_framework="""
        Laboratory conductivity tests are performed under controlled conditions, often not representative of field environments. Factors such as formation embedment, fines migration, and cyclic stress reduce field conductivity. Correction factors, derived from field studies and empirical models, are applied to lab data for realistic predictions.
        """,
        key_factors=["Embedment", "Fines migration", "Stress cycling", "Temperature"],
        primary_authority=["API RP 19C", "SPE 169009", "SPE 18212"],
        burden_holder="Completion Engineer",
        adversary_position="Lab corrections are overly conservative, underestimating field performance.",
        counter_arguments=[
            "Field data show significant conductivity loss.",
            "Correction factors are based on extensive field studies."
        ],
        resolution_strategy="Apply recommended correction factors; validate with post-frac production data.",
        entity_scope="Proppant Performance Prediction",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Long-Term Conductivity Degradation: Temperature & Stress Cycling",
        keywords=["proppant", "conductivity", "degradation", "temperature", "stress cycling"],
        conclusion_template="Long-term proppant conductivity degrades due to elevated temperature and cyclic stress, necessitating conservative design.",
        reasoning_framework="""
        Over time, elevated temperature accelerates chemical reactions and fines generation, while cyclic stress from production and shut-ins causes proppant crushing and embedment. Laboratory aging tests and field studies quantify degradation rates. Conservative design margins are recommended for high-temperature, high-stress reservoirs.
        """,
        key_factors=["Reservoir temperature", "Stress cycling", "Proppant type", "Aging tests"],
        primary_authority=["API RP 19C", "SPE 169009", "SPE 18212"],
        burden_holder="Reservoir Engineer",
        adversary_position="Degradation rates are overestimated; modern proppants are more resilient.",
        counter_arguments=[
            "Field failures are documented in high-temperature wells.",
            "Ceramic proppants show improved stability."
        ],
        resolution_strategy="Select proppant based on long-term tests; apply degradation factors in design.",
        entity_scope="Long-Term Fracture Conductivity",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Ceramic Proppant Strength: Sintered Bauxite",
        keywords=["ceramic proppant", "sintered bauxite", "strength", "conductivity", "high stress"],
        conclusion_template="Sintered bauxite proppants provide the highest crush strength and conductivity retention under extreme closure stress.",
        reasoning_framework="""
        Sintered bauxite is manufactured by high-temperature sintering of bauxite ore, resulting in a dense, high-strength proppant. It retains conductivity at closure stresses exceeding 10,000 psi, making it suitable for deep, high-pressure reservoirs. Cost and density are higher than alternatives, limiting use to critical applications.
        """,
        key_factors=["Closure stress", "Proppant density", "Cost", "Conductivity retention"],
        primary_authority=["API RP 19C", "SPE 169009", "SPE 18212"],
        burden_holder="Completion Engineer",
        adversary_position="High cost and density increase operational challenges.",
        counter_arguments=[
            "Alternatives lack comparable strength at high stress.",
            "Density can be managed with fluid selection."
        ],
        resolution_strategy="Use sintered bauxite for high-stress wells; optimize fluid for proppant transport.",
        entity_scope="High-Stress Reservoirs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Ceramic Proppant Strength: Lightweight Economy",
        keywords=["ceramic proppant", "lightweight", "economy", "strength", "conductivity"],
        conclusion_template="Lightweight ceramic proppants offer a balance of strength, density, and cost for moderate-stress reservoirs.",
        reasoning_framework="""
        Lightweight ceramics are produced by sintering kaolin or other clays, resulting in lower density and moderate strength. They provide improved transport and reduced settling compared to sand, with higher conductivity retention at moderate closure stresses (5,000-8,000 psi). Cost is higher than sand but lower than sintered bauxite.
        """,
        key_factors=["Proppant density", "Closure stress", "Cost", "Transportability"],
        primary_authority=["API RP 19C", "SPE 169009", "SPE 18212"],
        burden_holder="Completion Engineer",
        adversary_position="Strength is insufficient for deep, high-stress wells.",
        counter_arguments=[
            "Field data support use in moderate-stress environments.",
            "Lower density improves placement efficiency."
        ],
        resolution_strategy="Select based on reservoir stress profile; balance cost and performance.",
        entity_scope="Moderate-Stress Reservoirs",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Resin-Coated Proppant: Curable Consolidation",
        keywords=["resin-coated proppant", "curable", "consolidation", "flowback control", "conductivity"],
        conclusion_template="Curable resin-coated proppants consolidate in-situ, reducing flowback and fines migration while retaining conductivity.",
        reasoning_framework="""
        Curable resin coatings activate under closure stress and temperature, bonding proppant grains together. This reduces proppant flowback and fines migration, improving fracture cleanup and conductivity retention. Proper curing conditions are essential; premature or incomplete curing reduces effectiveness.
        """,
        key_factors=["Curing conditions", "Closure stress", "Temperature", "Proppant placement"],
        primary_authority=["API RP 19C", "SPE 169009", "SPE 18212"],
        burden_holder="Completion Engineer",
        adversary_position="Incomplete curing leads to poor consolidation and fines generation.",
        counter_arguments=[
            "Field QA/QC ensures proper curing.",
            "Alternative flowback controls exist."
        ],
        resolution_strategy="Monitor curing conditions; use QA/QC protocols for resin application.",
        entity_scope="Proppant Flowback Control",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Resin-Coated Proppant: Precured Consolidation",
        keywords=["resin-coated proppant", "precured", "consolidation", "flowback control", "conductivity"],
        conclusion_template="Precured resin-coated proppants provide immediate consolidation and fines control, but may have lower conductivity than curable types.",
        reasoning_framework="""
        Precured resin coatings bond proppant grains during manufacturing, offering immediate consolidation upon placement. This reduces flowback and fines migration, but the resin layer can reduce conductivity compared to uncoated or curable types. Selection depends on flowback risk and conductivity requirements.
        """,
        key_factors=["Resin thickness", "Proppant size", "Conductivity", "Flowback risk"],
        primary_authority=["API RP 19C", "SPE 169009", "SPE 18212"],
        burden_holder="Completion Engineer",
        adversary_position="Lower conductivity limits use in high-rate wells.",
        counter_arguments=[
            "Field data show adequate performance in most wells.",
            "Curable resins offer higher conductivity but require curing."
        ],
        resolution_strategy="Select resin type based on well conditions and flowback risk.",
        entity_scope="Proppant Flowback Control",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="100-Mesh Sand Pumping: Microproppant Near-Wellbore",
        keywords=["100-mesh", "microproppant", "near-wellbore", "sand", "placement"],
        conclusion_template="100-mesh sand is effective for near-wellbore proppant placement, reducing screen-out risk and improving cleanup.",
        reasoning_framework="""
        Fine sand (100-mesh) is used in the early and tail-in stages to enhance near-wellbore proppant distribution. Its small size reduces bridging and screen-out risk as the fracture narrows. Microproppant also aids in fracture cleanup and can improve initial production rates. However, long-term conductivity may be lower due to embedment and crush.
        """,
        key_factors=["Proppant size", "Fracture width", "Screen-out risk", "Conductivity"],
        primary_authority=["API RP 19C", "SPE 169009", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Microproppant lacks durability for long-term conductivity.",
        counter_arguments=[
            "Field results show improved cleanup and initial rates.",
            "Blend optimization can mitigate conductivity loss."
        ],
        resolution_strategy="Use 100-mesh sand for near-wellbore placement; monitor long-term performance.",
        entity_scope="Fracture Treatment Design",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="In-Situ Proppant Generation: ISPS",
        keywords=["in-situ proppant", "ISPS", "generation", "channel fracturing", "placement"],
        conclusion_template="In-Situ Proppant Synthesis (ISPS) enables proppant generation within the fracture, reducing logistics and enhancing placement.",
        reasoning_framework="""
        ISPS involves injecting precursor fluids that react in-situ to form solid proppant particles. This reduces surface logistics and can improve proppant placement in complex fracture networks. Channel fracturing techniques use ISPS to create conductive pathways. Challenges include controlling particle size, reaction kinetics, and ensuring uniform distribution.
        """,
        key_factors=["Precursor chemistry", "Reaction kinetics", "Placement control", "Conductivity"],
        primary_authority=["SPE 174063", "API RP 19C", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="ISPS proppant has inconsistent quality and placement.",
        counter_arguments=[
            "Field trials show promising results.",
            "Quality control is improving with new chemistries."
        ],
        resolution_strategy="Pilot ISPS in suitable reservoirs; monitor placement and conductivity.",
        entity_scope="Advanced Fracturing Techniques",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="SPE 174063"
    ),
    DoctrineBlock(
        topic="In-Situ Proppant Generation: Channel Fracturing",
        keywords=["in-situ proppant", "channel fracturing", "placement", "conductivity", "ISPS"],
        conclusion_template="Channel fracturing with in-situ proppant generation creates conductive channels, improving fracture conductivity and production.",
        reasoning_framework="""
        Channel fracturing techniques alternate proppant-laden and proppant-free fluid stages, creating channels of high conductivity. ISPS can be used to generate proppant in-situ within these channels. Benefits include improved conductivity and reduced proppant requirements. Challenges include channel stability and placement control.
        """,
        key_factors=["Stage design", "Proppant placement", "Channel stability", "Conductivity"],
        primary_authority=["SPE 174063", "API RP 19C", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Channels may collapse or become bypassed over time.",
        counter_arguments=[
            "Field data show improved production in channel-fractured wells.",
            "Channel stability can be enhanced with optimized fluids."
        ],
        resolution_strategy="Design channel stages based on reservoir properties; monitor post-frac conductivity.",
        entity_scope="Advanced Fracturing Techniques",
        confidence=0.81,
        confidence_zone="Medium",
        controlling_precedent="SPE 174063"
    ),
    DoctrineBlock(
        topic="Proppant Placement Diagnostics: Radioactive Tracer",
        keywords=["proppant", "placement", "diagnostics", "radioactive tracer", "mapping"],
        conclusion_template="Radioactive tracers enable direct mapping of proppant placement, providing high-confidence diagnostics for fracture evaluation.",
        reasoning_framework="""
        Radioactive tracers are incorporated into proppant batches and detected using gamma logging tools after treatment. This provides direct evidence of proppant distribution and fracture height. Regulatory and safety considerations limit use, but results are highly reliable for evaluating placement efficiency.
        """,
        key_factors=["Tracer selection", "Regulatory compliance", "Detection sensitivity", "Health and safety"],
        primary_authority=["API RP 19C", "SPE 169009", "DOE Hydraulic Fracturing Primer"],
        burden_holder="Production Engineer",
        adversary_position="Tracer use is limited by regulations and cost.",
        counter_arguments=[
            "Alternative tracers (chemical, fiber optic) are less direct.",
            "Tracer doses can be minimized for safety."
        ],
        resolution_strategy="Use radioactive tracers selectively; comply with all regulations and safety protocols.",
        entity_scope="Fracture Diagnostics",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Distributed Acoustic Sensing (DAS): Proppant Placement",
        keywords=["DAS", "distributed acoustic sensing", "proppant placement", "fiber optic", "mapping"],
        conclusion_template="DAS provides real-time, high-resolution data on proppant placement dynamics, enabling optimization of fracturing operations.",
        reasoning_framework="""
        DAS systems use fiber optic cables to detect acoustic signals generated during fracturing. Changes in acoustic response correlate with fluid and proppant movement, allowing inference of placement patterns. Data analysis requires advanced algorithms and integration with other diagnostics for robust interpretation.
        """,
        key_factors=["Fiber optic installation", "Signal processing", "Data integration", "Calibration"],
        primary_authority=["SPE 187451", "API RP 19C", "Schlumberger FiberSensing"],
        burden_holder="Production Engineer",
        adversary_position="DAS signals are ambiguous and require complex interpretation.",
        counter_arguments=[
            "Multi-diagnostic integration improves confidence.",
            "Field validation supports DAS utility."
        ],
        resolution_strategy="Combine DAS with tracers and microseismic for comprehensive diagnostics.",
        entity_scope="Fracture Diagnostics",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 187451"
    ),
    DoctrineBlock(
        topic="Fiber Optic Distributed Temperature Sensing (DTS): Placement Mapping",
        keywords=["DTS", "distributed temperature sensing", "fiber optic", "placement mapping", "proppant"],
        conclusion_template="DTS enables mapping of proppant placement by detecting temperature anomalies associated with fluid and proppant movement.",
        reasoning_framework="""
        DTS systems measure temperature profiles along the wellbore using fiber optic cables. Proppant-laden fluids alter heat transfer, producing detectable temperature changes. DTS data, combined with injection records and other diagnostics, provide insights into proppant placement and fracture geometry.
        """,
        key_factors=["Fiber optic installation", "Temperature resolution", "Data integration", "Calibration"],
        primary_authority=["SPE 187451", "API RP 19C", "Schlumberger FiberSensing"],
        burden_holder="Production Engineer",
        adversary_position="Temperature signals may be confounded by other thermal effects.",
        counter_arguments=[
            "Data integration reduces ambiguity.",
            "Calibration with known events improves accuracy."
        ],
        resolution_strategy="Integrate DTS with DAS and tracers; validate with post-frac production data.",
        entity_scope="Fracture Diagnostics",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 187451"
    ),
    DoctrineBlock(
        topic="Proppant-Laden Fluid: Friction Pressure Prediction",
        keywords=["proppant-laden fluid", "friction pressure", "prediction", "slurry", "hydraulics"],
        conclusion_template="Friction pressure in proppant-laden fluids is higher than in clear fluids and must be predicted using appropriate rheological models.",
        reasoning_framework="""
        The presence of proppant increases slurry viscosity and turbulence, raising friction pressure during pumping. Prediction requires accurate rheological characterization (Power Law, Herschel-Bulkley) and consideration of proppant concentration. Empirical correlations and computational models are used for design.
        """,
        key_factors=["Slurry viscosity", "Proppant concentration", "Pipe diameter", "Pumping rate"],
        primary_authority=["API RP 13B-1", "SPE 169009", "SPE Monograph 12"],
        burden_holder="Design Engineer",
        adversary_position="Design models overpredict friction, leading to conservative designs.",
        counter_arguments=[
            "Field data validate model predictions.",
            "Safety margins are necessary for reliable operations."
        ],
        resolution_strategy="Calibrate models with field data; use conservative estimates for critical operations.",
        entity_scope="Surface and Downhole Hydraulics",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Proppant Ramp Schedule Optimization: Maximum Concentration",
        keywords=["proppant", "ramp schedule", "optimization", "maximum concentration", "screen-out"],
        conclusion_template="Optimized ramp schedules maximize proppant concentration while minimizing screen-out risk and ensuring effective placement.",
        reasoning_framework="""
        Proppant ramp schedules gradually increase concentration to reduce screen-out risk and ensure uniform placement. Optimization balances maximum achievable concentration, fluid viscosity, and fracture width. Real-time monitoring and adaptive control improve outcomes. Excessive ramp rates or concentrations increase bridging and screen-out risk.
        """,
        key_factors=["Ramp rate", "Maximum concentration", "Fluid viscosity", "Fracture width"],
        primary_authority=["API RP 19C", "SPE 169009", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Conservative ramping reduces operational efficiency.",
        counter_arguments=[
            "Aggressive ramping increases screen-out risk.",
            "Field data support gradual ramp schedules."
        ],
        resolution_strategy="Use real-time monitoring to adapt ramp schedules; optimize based on formation response.",
        entity_scope="Fracture Treatment Operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Multi-Layer Proppant Placement: Vertical Coverage",
        keywords=["multi-layer", "proppant placement", "vertical coverage", "fracture height", "zonal isolation"],
        conclusion_template="Multi-layer proppant placement techniques improve vertical fracture coverage and zonal isolation.",
        reasoning_framework="""
        Multi-layer placement alternates proppant-laden and proppant-free fluid stages, promoting vertical dispersion and coverage. This enhances conductivity across the fracture height and improves zonal isolation. Design must consider fluid properties, stage timing, and proppant transport dynamics.
        """,
        key_factors=["Stage design", "Fluid properties", "Fracture height", "Proppant transport"],
        primary_authority=["SPE 174063", "API RP 19C", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Layering increases operational complexity and cost.",
        counter_arguments=[
            "Improved vertical coverage enhances production.",
            "Operational complexity can be managed with automation."
        ],
        resolution_strategy="Optimize stage design for target vertical coverage; monitor with diagnostics.",
        entity_scope="Fracture Treatment Design",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="SPE 174063"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Viscous Drag vs Gravity Settling",
        keywords=["proppant transport", "viscous drag", "gravity settling", "slurry", "placement"],
        conclusion_template="Proppant transport is determined by the balance between viscous drag and gravity settling, with fluid viscosity and velocity as key controls.",
        reasoning_framework="""
        Proppant particles are transported by viscous drag from the flowing fluid, counteracted by gravity-induced settling. High fluid viscosity and velocity enhance transport, while large, dense particles settle faster. Design must optimize fluid and proppant properties to maximize placement efficiency.
        """,
        key_factors=["Fluid viscosity", "Flow velocity", "Particle size", "Density difference"],
        primary_authority=["SPE 169009", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Design Engineer",
        adversary_position="Gravity settling dominates in low-viscosity fluids, limiting transport.",
        counter_arguments=[
            "Viscous drag can be increased with fluid additives.",
            "Fine proppant improves transport in slickwater."
        ],
        resolution_strategy="Select fluid and proppant for optimal transport; monitor placement with diagnostics.",
        entity_scope="Fracture Treatment Design",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Turbulent vs Laminar Flow",
        keywords=["proppant transport", "turbulent flow", "laminar flow", "slurry", "hydraulics"],
        conclusion_template="Turbulent flow enhances proppant suspension and transport compared to laminar flow, especially in wide fractures and high-rate treatments.",
        reasoning_framework="""
        In turbulent flow regimes (Re > 2000), mixing and eddies suspend proppant particles, reducing settling and improving transport. Laminar flow is less effective for suspension, increasing risk of settling and bridging. Treatment design should target turbulent flow where possible, within operational constraints.
        """,
        key_factors=["Reynolds number", "Flow rate", "Fracture width", "Fluid viscosity"],
        primary_authority=["SPE 169009", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Turbulent flow is difficult to maintain in narrow fractures.",
        counter_arguments=[
            "High-rate slickwater treatments achieve turbulence.",
            "Laminar flow can be mitigated with fluid additives."
        ],
        resolution_strategy="Design for turbulent flow where feasible; monitor flow regime during treatment.",
        entity_scope="Fracture Treatment Operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Non-Newtonian Effects",
        keywords=["proppant transport", "non-Newtonian", "slurry", "rheology", "placement"],
        conclusion_template="Non-Newtonian fluid behavior significantly affects proppant transport, with shear-thinning enhancing suspension and placement.",
        reasoning_framework="""
        Shear-thinning fluids (n < 1) exhibit lower viscosity at high shear rates (near wellbore) and higher viscosity at low shear rates (far field), aiding proppant suspension during transport and placement. Accurate rheological modeling is essential for predicting transport efficiency and avoiding screen-out.
        """,
        key_factors=["Flow behavior index (n)", "Consistency index (K)", "Shear rate", "Proppant concentration"],
        primary_authority=["API RP 13B-1", "SPE 169009", "SPE Monograph 12"],
        burden_holder="Fluid Engineer",
        adversary_position="Non-Newtonian effects are overemphasized in field-scale models.",
        counter_arguments=[
            "Field data confirm improved transport with shear-thinning fluids.",
            "Newtonian models underpredict suspension."
        ],
        resolution_strategy="Use non-Newtonian models for design; validate with field measurements.",
        entity_scope="Fracturing Fluids",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Bridging Criteria",
        keywords=["proppant transport", "bridging", "criteria", "fracture width", "particle size"],
        conclusion_template="Proppant bridging is predicted when fracture width approaches 2-3 times the particle diameter, guiding proppant selection and treatment design.",
        reasoning_framework="""
        Bridging occurs when particles span the fracture width, halting transport and risking screen-out. The critical width is typically 2-3 times the median particle diameter. Treatment design must ensure fracture width remains above this threshold throughout pumping.
        """,
        key_factors=["Particle diameter", "Fracture width", "Closure rate", "Proppant concentration"],
        primary_authority=["SPE 169009", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Design Engineer",
        adversary_position="Bridging criteria are conservative and may limit operational flexibility.",
        counter_arguments=[
            "Field incidents confirm bridging at predicted thresholds.",
            "Conservative design reduces screen-out risk."
        ],
        resolution_strategy="Select proppant and design schedule to avoid bridging; monitor pressure for early detection.",
        entity_scope="Fracture Treatment Design",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Slugging",
        keywords=["proppant transport", "slugging", "batch injection", "placement", "screen-out"],
        conclusion_template="Proppant slugging (batch injection) can improve placement efficiency but increases risk of localized screen-out if not carefully managed.",
        reasoning_framework="""
        Slugging involves injecting discrete batches of proppant-laden fluid, separated by clear fluid. This can enhance placement in complex fractures but may cause localized bridging and screen-out if slug size or interval is not optimized. Real-time monitoring and adaptive control are essential for success.
        """,
        key_factors=["Slug size", "Interval timing", "Fracture geometry", "Monitoring"],
        primary_authority=["SPE 174063", "API RP 19C", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Slugging increases operational complexity and screen-out risk.",
        counter_arguments=[
            "Optimized slugging improves placement in complex reservoirs.",
            "Monitoring mitigates screen-out risk."
        ],
        resolution_strategy="Pilot slugging in suitable wells; use real-time data for adaptive control.",
        entity_scope="Advanced Fracturing Techniques",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="SPE 174063"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Bank Formation",
        keywords=["proppant transport", "bank formation", "settling", "placement", "conductivity"],
        conclusion_template="Proppant bank formation occurs due to settling and filtration, impacting fracture conductivity and cleanup.",
        reasoning_framework="""
        As proppant settles or is filtered at fracture faces, banks of proppant can form, especially in low-viscosity fluids or near the fracture tip. These banks may impede cleanup and reduce effective conductivity. Design must minimize bank formation through fluid selection and pumping strategy.
        """,
        key_factors=["Settling rate", "Fluid viscosity", "Pumping rate", "Fracture geometry"],
        primary_authority=["SPE 169009", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Bank formation is rare with modern slickwater treatments.",
        counter_arguments=[
            "Field observations confirm bank formation in some wells.",
            "Optimized fluids reduce risk."
        ],
        resolution_strategy="Monitor for bank formation with diagnostics; adjust fluid and pumping as needed.",
        entity_scope="Fracture Treatment Operations",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Flowback Control Devices",
        keywords=["proppant transport", "flowback control", "devices", "screen", "wellbore"],
        conclusion_template="Proppant flowback control devices (screens, valves) reduce proppant production and improve well cleanup.",
        reasoning_framework="""
        Mechanical devices such as screens and flowback control valves are installed at the wellbore to prevent proppant production during flowback. These devices protect surface equipment and maintain fracture conductivity. Selection depends on proppant size, expected flow rates, and operational requirements.
        """,
        key_factors=["Device type", "Proppant size", "Flow rate", "Installation method"],
        primary_authority=["API RP 19C", "SPE 169009", "DOE Hydraulic Fracturing Primer"],
        burden_holder="Production Engineer",
        adversary_position="Devices increase cost and may restrict production rates.",
        counter_arguments=[
            "Field experience shows improved cleanup and equipment protection.",
            "Proper sizing minimizes flow restriction."
        ],
        resolution_strategy="Select devices based on well conditions; monitor performance during flowback.",
        entity_scope="Well Completion",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in Horizontal Wells",
        keywords=["proppant transport", "horizontal wells", "placement", "settling", "convection"],
        conclusion_template="Proppant transport in horizontal wells is challenged by settling and gravity segregation, requiring tailored fluid and pumping strategies.",
        reasoning_framework="""
        In horizontal wells, gravity causes proppant to settle along the bottom of the wellbore and fractures, reducing placement efficiency. Fluid selection (high viscosity, shear-thinning) and pumping strategies (high rate, pulsed injection) are used to mitigate settling and enhance uniform distribution.
        """,
        key_factors=["Well orientation", "Fluid viscosity", "Pumping rate", "Proppant size"],
        primary_authority=["SPE 169009", "API RP 19C", "Barree & Conway (1995)"],
        burden_holder="Stimulation Engineer",
        adversary_position="Gravity effects are overstated; high-rate pumping overcomes settling.",
        counter_arguments=[
            "Field data show uneven placement in some horizontals.",
            "Optimized fluids and rates improve outcomes."
        ],
        resolution_strategy="Tailor fluid and pumping to well geometry; monitor placement with diagnostics.",
        entity_scope="Horizontal Well Completions",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="SPE 169009"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in Multistage Fracturing",
        keywords=["proppant transport", "multistage fracturing", "placement", "zonal isolation", "diverters"],
        conclusion_template="Multistage fracturing requires careful proppant transport design to ensure uniform placement and zonal isolation.",
        reasoning_framework="""
        In multistage fracturing, diverters and stage sequencing are used to direct proppant to target zones. Fluid and proppant properties must be optimized for each stage to prevent premature screen-out and ensure even distribution. Diagnostics are used to verify placement and adjust future stages.
        """,
        key_factors=["Stage design", "Diverter selection", "Proppant properties", "Monitoring"],
        primary_authority=["SPE 174063", "API RP 19C", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Uniform placement is difficult to achieve in heterogeneous formations.",
        counter_arguments=[
            "Diverters and diagnostics improve placement control.",
            "Stage-by-stage optimization enhances outcomes."
        ],
        resolution_strategy="Use diagnostics to guide stage design; adapt strategy based on results.",
        entity_scope="Multistage Completions",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="SPE 174063"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in High-Temperature Reservoirs",
        keywords=["proppant transport", "high-temperature", "placement", "conductivity", "thermal stability"],
        conclusion_template="High-temperature reservoirs require thermally stable proppants and fluids to maintain placement and conductivity.",
        reasoning_framework="""
        Elevated temperatures accelerate fluid degradation and proppant fines generation, reducing placement efficiency and conductivity. Thermally stable proppants (ceramics, resin-coated) and high-temperature fluids are used to mitigate these effects. Laboratory and field testing inform selection.
        """,
        key_factors=["Reservoir temperature", "Proppant type", "Fluid stability", "Conductivity retention"],
        primary_authority=["API RP 19C", "SPE 18212", "SPE 169009"],
        burden_holder="Completion Engineer",
        adversary_position="High-temperature effects are manageable with modern materials.",
        counter_arguments=[
            "Field failures have occurred with inadequate materials.",
            "Testing ensures suitability."
        ],
        resolution_strategy="Select materials based on temperature rating; validate with lab and field data.",
        entity_scope="High-Temperature Reservoirs",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in Unconsolidated Formations",
        keywords=["proppant transport", "unconsolidated formations", "placement", "embedment", "conductivity"],
        conclusion_template="Unconsolidated formations increase proppant embedment and conductivity loss, requiring careful selection of proppant and fluids.",
        reasoning_framework="""
        In unconsolidated formations, proppant embedment is significant due to low rock strength. High-strength proppants (ceramic, resin-coated) and fluids with high viscosity or yield stress are used to minimize embedment and maintain conductivity. Laboratory embedment tests guide selection.
        """,
        key_factors=["Formation strength", "Proppant type", "Fluid viscosity", "Embedment tests"],
        primary_authority=["API RP 19C", "SPE 18212", "SPE 169009"],
        burden_holder="Reservoir Engineer",
        adversary_position="Embedment can be mitigated with proper design.",
        counter_arguments=[
            "Field data confirm persistent conductivity loss.",
            "Embedment corrections are essential for accurate prediction."
        ],
        resolution_strategy="Assess formation strength; select proppant and fluids accordingly.",
        entity_scope="Unconsolidated Reservoirs",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in Tight Gas Reservoirs",
        keywords=["proppant transport", "tight gas", "placement", "conductivity", "fracture complexity"],
        conclusion_template="Tight gas reservoirs require optimized proppant transport to ensure placement in complex, low-permeability fractures.",
        reasoning_framework="""
        In tight gas, fracture complexity and low permeability challenge proppant placement. High-rate slickwater treatments, fine proppant, and advanced diagnostics are used to maximize placement efficiency. Conductivity retention is critical for economic production.
        """,
        key_factors=["Fracture complexity", "Proppant size", "Pumping rate", "Diagnostics"],
        primary_authority=["API RP 19C", "SPE 18212", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Proppant placement is limited by fracture tortuosity.",
        counter_arguments=[
            "Fine proppant and high-rate treatments improve placement.",
            "Diagnostics enable adaptive design."
        ],
        resolution_strategy="Optimize treatment for fracture complexity; monitor with diagnostics.",
        entity_scope="Tight Gas Reservoirs",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in Naturally Fractured Reservoirs",
        keywords=["proppant transport", "naturally fractured", "placement", "leakoff", "conductivity"],
        conclusion_template="Naturally fractured reservoirs require tailored proppant transport to address leakoff and ensure placement in primary fractures.",
        reasoning_framework="""
        Natural fractures increase fluid leakoff, reducing proppant transport efficiency. High-viscosity fluids, rapid pumping, and diversion techniques are used to direct proppant into primary fractures. Diagnostics verify placement and inform adaptive strategies.
        """,
        key_factors=["Natural fracture density", "Leakoff rate", "Fluid viscosity", "Diversion methods"],
        primary_authority=["API RP 19C", "SPE 18212", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Leakoff prevents effective proppant placement.",
        counter_arguments=[
            "Diversion and rapid pumping mitigate leakoff.",
            "Diagnostics confirm placement."
        ],
        resolution_strategy="Assess natural fracture network; design fluids and schedule for effective placement.",
        entity_scope="Naturally Fractured Reservoirs",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in Shale Reservoirs",
        keywords=["proppant transport", "shale", "placement", "complex fractures", "conductivity"],
        conclusion_template="Shale reservoirs require fine proppant and high-rate treatments to maximize placement in complex fracture networks.",
        reasoning_framework="""
        Shale formations exhibit complex, branching fracture networks. Fine proppant and high-rate slickwater treatments are used to enhance placement efficiency. Diagnostics (fiber optic, tracers) are essential for verifying distribution and optimizing future treatments.
        """,
        key_factors=["Fracture complexity", "Proppant size", "Pumping rate", "Diagnostics"],
        primary_authority=["API RP 19C", "SPE 18212", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Complexity limits proppant placement and conductivity.",
        counter_arguments=[
            "Fine proppant improves placement in narrow fractures.",
            "Diagnostics enable adaptive optimization."
        ],
        resolution_strategy="Use fine proppant and diagnostics; adapt design based on results.",
        entity_scope="Shale Reservoirs",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Transport: Proppant Transport in Carbonate Reservoirs",
        keywords=["proppant transport", "carbonate", "placement", "acidizing", "conductivity"],
        conclusion_template="Carbonate reservoirs may require acidizing and tailored proppant transport to ensure placement and conductivity retention.",
        reasoning_framework="""
        Carbonates often require acidizing to create wormholes and enhance fracture conductivity. Proppant transport must be coordinated with acid stages to ensure placement in created channels. High-strength proppants and compatible fluids are used to maintain conductivity.
        """,
        key_factors=["Acidizing strategy", "Proppant type", "Fluid compatibility", "Conductivity retention"],
        primary_authority=["API RP 19C", "SPE 18212", "SPE 169009"],
        burden_holder="Stimulation Engineer",
        adversary_position="Acidizing complicates proppant placement and may reduce conductivity.",
        counter_arguments=[
            "Coordinated design improves outcomes.",
            "High-strength proppants resist acid degradation."
        ],
        resolution_strategy="Integrate acidizing and proppant stages; select materials for acid resistance.",
        entity_scope="Carbonate Reservoirs",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="API RP 19C"
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