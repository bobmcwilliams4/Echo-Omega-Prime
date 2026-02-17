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
        topic="Stribeck Curve Analysis - Lubrication Regime Identification",
        keywords=["Stribeck Curve", "lubrication regime", "boundary lubrication", "mixed lubrication", "hydrodynamic lubrication", "tribology", "friction coefficient"],
        conclusion_template="Based on the Stribeck curve analysis, the lubrication regime is identified as {regime} under the given operating conditions.",
        reasoning_framework="""
The Stribeck curve is a fundamental tool in tribology for identifying lubrication regimes as a function of the Hersey number (viscosity x speed / load). The curve is divided into three primary regimes:
1. Boundary lubrication: Direct asperity contact dominates, high friction.
2. Mixed lubrication: Partial film formation, both asperity contact and fluid film contribute.
3. Hydrodynamic lubrication: Full fluid film separates surfaces, lowest friction.
To determine the regime:
- Calculate the Hersey number using the system's viscosity, speed, and load.
- Plot or reference the Stribeck curve for the material/lubricant pair.
- Identify the regime corresponding to the calculated Hersey number.
- Consider surface roughness and lubricant additives, which can shift regime boundaries.
""",
        key_factors=[
            "Viscosity of lubricant",
            "Relative speed of surfaces",
            "Applied load",
            "Surface roughness",
            "Lubricant additives"
        ],
        primary_authority=[
            "Stachowiak, G. W., & Batchelor, A. W. (2014). Engineering Tribology.",
            "Stribeck, R. (1902). Die wesentlichen Eigenschaften der Gleit- und Rollenlager."
        ],
        burden_holder="System designer/analyst",
        adversary_position="Regime identification is ambiguous due to overlapping boundaries and real-world deviations from idealized curves.",
        counter_arguments=[
            "Empirical data and advanced surface characterization can refine regime identification.",
            "Modern lubricants with additives can extend hydrodynamic regime."
        ],
        resolution_strategy="Use experimental validation and advanced surface/lubricant analysis to confirm regime.",
        entity_scope="All lubricated mechanical contacts in MECH13 engine systems.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Stachowiak & Batchelor, Engineering Tribology, Ch. 6"
    ),
    DoctrineBlock(
        topic="Archard Wear Equation - Adhesive Wear Prediction",
        keywords=["Archard equation", "adhesive wear", "wear coefficient", "tribology", "contact mechanics"],
        conclusion_template="The predicted adhesive wear volume is {wear_volume} mm³, calculated using the Archard equation.",
        reasoning_framework="""
The Archard wear equation relates the volume of material lost due to adhesive wear to the applied load, sliding distance, hardness, and a dimensionless wear coefficient:
    V = (k * L * s) / H
Where:
- V = wear volume (mm³)
- k = wear coefficient (dimensionless, typically 10^-8 to 10^-2)
- L = normal load (N)
- s = sliding distance (m)
- H = hardness of softer material (Pa)
To apply:
- Determine or estimate k from literature or experiments for the material pair and lubrication condition.
- Measure or specify L, s, and H.
- Calculate V.
Limitations:
- Assumes steady-state conditions and uniform contact.
- Does not account for third-body effects or severe wear transitions.
""",
        key_factors=[
            "Wear coefficient (k)",
            "Normal load",
            "Sliding distance",
            "Material hardness",
            "Lubrication condition"
        ],
        primary_authority=[
            "Archard, J. F. (1953). Contact and rubbing of flat surfaces. J. Appl. Phys.",
            "Hutchings, I. M., & Shipway, P. (2017). Tribology: Friction and Wear of Engineering Materials."
        ],
        burden_holder="Tribology analyst or design engineer",
        adversary_position="Archard equation oversimplifies real wear processes and ignores complex surface interactions.",
        counter_arguments=[
            "The equation provides a first-order estimate; for critical applications, supplement with experimental data.",
            "Advanced models can be used for severe or non-adhesive wear."
        ],
        resolution_strategy="Validate predictions with wear testing and adjust k accordingly.",
        entity_scope="Sliding contacts in MECH13 tribological systems.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Archard, J. F. (1953); Hutchings & Shipway (2017)"
    ),
    DoctrineBlock(
        topic="Reynolds Equation for Hydrodynamic Bearings - Film Pressure Distribution",
        keywords=["Reynolds equation", "hydrodynamic bearing", "film pressure", "fluid film lubrication", "bearing design"],
        conclusion_template="The hydrodynamic film pressure distribution is determined by solving the Reynolds equation for the specified bearing geometry and operating conditions.",
        reasoning_framework="""
The Reynolds equation describes the pressure distribution in a thin lubricant film between two surfaces in relative motion:
    ∂/∂x (h³ ∂p/∂x) + ∂/∂z (h³ ∂p/∂z) = 6ηU ∂h/∂x + 12η ∂h/∂t
Where:
- h = film thickness
- p = pressure
- η = lubricant viscosity
- U = sliding speed
- x, z = spatial coordinates
- t = time
For steady-state, isothermal, and 1D cases, the equation simplifies.
To apply:
- Define bearing geometry (e.g., journal, pad).
- Specify boundary conditions (e.g., pressure at edges = ambient).
- Input operating parameters (speed, load, viscosity).
- Numerically solve for p(x) or p(x, z).
- Use results for load-carrying capacity and minimum film thickness.
""",
        key_factors=[
            "Bearing geometry",
            "Lubricant viscosity",
            "Operating speed",
            "Applied load",
            "Boundary conditions"
        ],
        primary_authority=[
            "Hamrock, B. J., Schmid, S. R., & Jacobson, B. O. (2004). Fundamentals of Fluid Film Lubrication.",
            "Reynolds, O. (1886). On the Theory of Lubrication."
        ],
        burden_holder="Bearing designer or tribologist",
        adversary_position="Reynolds equation neglects turbulence, temperature gradients, and non-Newtonian effects.",
        counter_arguments=[
            "For most engineering bearings, the classical Reynolds equation provides accurate predictions.",
            "Advanced models exist for turbulent or non-Newtonian lubrication."
        ],
        resolution_strategy="Use CFD or extended Reynolds models for complex cases; validate with experimental data.",
        entity_scope="Hydrodynamic bearings in MECH13 engine assemblies.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Hamrock et al., Fundamentals of Fluid Film Lubrication, Ch. 2"
    ),
    DoctrineBlock(
        topic="Elastohydrodynamic Lubrication (EHL) - Rolling Contact Film Thickness",
        keywords=["EHL", "elastohydrodynamic lubrication", "film thickness", "rolling contact", "Hertzian contact", "tribology"],
        conclusion_template="The minimum EHL film thickness is calculated as {film_thickness} μm for the specified rolling contact.",
        reasoning_framework="""
EHL occurs in concentrated contacts (e.g., gears, rolling bearings) where elastic deformation and high pressure affect film formation. The Hamrock-Dowson formula is widely used:
    h_min = 3.63 U^0.68 G^0.49 W^-0.073 (1 - e^-0.68k)
Where:
- h_min = minimum film thickness (μm)
- U = dimensionless speed parameter
- G = dimensionless material parameter
- W = dimensionless load parameter
- k = ellipticity parameter
To apply:
- Calculate U, G, W using material properties, speed, load, and viscosity.
- Use appropriate formula for point or line contact.
- Consider temperature effects and surface roughness.
- Ensure lambda ratio (h_min / composite roughness) > 1 for full EHL.
""",
        key_factors=[
            "Rolling speed",
            "Load",
            "Material elastic modulus",
            "Lubricant viscosity",
            "Contact geometry"
        ],
        primary_authority=[
            "Hamrock, B. J., & Dowson, D. (1977). Isothermal elastohydrodynamic lubrication of point contacts.",
            "Dowson, D., & Higginson, G. R. (1977). Elastohydrodynamic Lubrication."
        ],
        burden_holder="Rolling element designer or analyst",
        adversary_position="EHL models may not account for thermal or starvation effects in real contacts.",
        counter_arguments=[
            "Thermal correction factors and starvation models can be incorporated.",
            "Empirical validation is recommended for critical applications."
        ],
        resolution_strategy="Apply correction factors as needed; validate with film thickness measurements.",
        entity_scope="Rolling contacts in MECH13 gearboxes and bearings.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Hamrock & Dowson (1977); Dowson & Higginson (1977)"
    ),
    DoctrineBlock(
        topic="Oil Analysis Interpretation - Wear Metals and Contamination Limits",
        keywords=["oil analysis", "wear metals", "contamination", "spectrometric analysis", "lubricant monitoring", "limits"],
        conclusion_template="Oil analysis results indicate {condition} based on wear metal and contamination levels relative to established limits.",
        reasoning_framework="""
Oil analysis is a proactive tool for monitoring machine health. Key steps:
- Collect oil sample following ASTM D4057 or ISO 3170.
- Analyze for wear metals (Fe, Cu, Pb, Al, etc.), contaminants (Si, Na, water), and additive elements.
- Compare results to established limits (OEM, ASTM, or industry standards).
- Trending is critical: sudden increases suggest abnormal wear or contamination ingress.
- Consider equipment type, age, and operating environment.
- Use particle count (ISO 4406) and water content (Karl Fischer) for comprehensive assessment.
""",
        key_factors=[
            "Wear metal concentration",
            "Contaminant levels",
            "Sampling procedure",
            "Equipment operating history",
            "OEM/industry limits"
        ],
        primary_authority=[
            "ASTM D6595 - Standard Test Method for Determination of Wear Metals and Contaminants in Used Lubricating Oils",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Maintenance engineer or oil analyst",
        adversary_position="Oil analysis may yield false positives/negatives due to sampling errors or dilution.",
        counter_arguments=[
            "Strict adherence to sampling protocols minimizes errors.",
            "Trend analysis reduces impact of single anomalous results."
        ],
        resolution_strategy="Repeat sampling and confirmatory testing if results are ambiguous.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D6595; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Base Oil Groups (API) - Performance Characteristics",
        keywords=["base oil", "API groups", "Group I", "Group II", "Group III", "Group IV", "Group V", "lubricant performance"],
        conclusion_template="The selected lubricant base oil group ({api_group}) provides the following performance characteristics: {performance_summary}.",
        reasoning_framework="""
API classifies base oils into five groups:
- Group I: Solvent-refined, 90% saturates, <0.03% sulfur, VI 80-120.
- Group II: Hydroprocessed, >90% saturates, <0.03% sulfur, VI 80-120.
- Group III: Severely hydrocracked, >90% saturates, <0.03% sulfur, VI >120.
- Group IV: Polyalphaolefins (PAO), synthetic, VI >120.
- Group V: All others (esters, naphthenics, etc.).
Performance implications:
- Group III/IV/V: Superior oxidation stability, low volatility, high VI.
- Group I/II: Lower cost, suitable for less demanding applications.
Selection depends on temperature range, volatility, oxidation resistance, and compatibility.
""",
        key_factors=[
            "Base oil group",
            "Viscosity index",
            "Oxidation stability",
            "Volatility",
            "Application requirements"
        ],
        primary_authority=[
            "API 1509 - Engine Oil Licensing and Certification System",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="Base oil group alone does not determine finished lubricant performance; additive package is critical.",
        counter_arguments=[
            "Base oil defines fundamental properties; additives enhance or modify performance.",
            "Finished lubricant testing validates suitability."
        ],
        resolution_strategy="Consider both base oil and additive system; validate with application-specific testing.",
        entity_scope="All lubricants used in MECH13 engine systems.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API 1509; Totten (2016)"
    ),
    DoctrineBlock(
        topic="EP and AW Additives - Extreme Pressure and Anti-Wear Mechanisms",
        keywords=["EP additives", "AW additives", "extreme pressure", "anti-wear", "tribochemistry", "ZDDP", "phosphorus", "sulfur"],
        conclusion_template="The selected lubricant formulation provides {level} of EP/AW protection based on additive chemistry and concentration.",
        reasoning_framework="""
EP (Extreme Pressure) and AW (Anti-Wear) additives protect surfaces under high load:
- EP additives (e.g., sulfur, phosphorus, chlorinated compounds) react at high temperatures to form protective films, preventing welding and scuffing.
- AW additives (e.g., ZDDP) form sacrificial films at moderate temperatures, reducing adhesive wear.
Key considerations:
- Additive concentration and compatibility with base oil.
- Impact on catalyst and seal materials (especially phosphorus and sulfur).
- Regulatory limits on phosphorus (e.g., for emissions compliance).
- Synergy or antagonism between additive components.
""",
        key_factors=[
            "Additive type and concentration",
            "Operating temperature",
            "Load conditions",
            "Compatibility with materials",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Mang, T., & Dresel, W. (2017). Lubricants and Lubrication.",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or tribologist",
        adversary_position="High EP/AW additive levels may cause corrosion or catalyst poisoning.",
        counter_arguments=[
            "Modern additive chemistry balances protection with material compatibility.",
            "Testing ensures compliance with OEM and regulatory requirements."
        ],
        resolution_strategy="Optimize additive package for application; validate with tribological and compatibility tests.",
        entity_scope="All lubricants in MECH13 tribological systems.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Mang & Dresel (2017); Totten (2016)"
    ),
    DoctrineBlock(
        topic="Grease Selection - NLGI Grade, Thickener Type, and Dropping Point",
        keywords=["grease", "NLGI grade", "thickener", "dropping point", "consistency", "lubricant selection"],
        conclusion_template="The recommended grease is NLGI {nlgi_grade} with {thickener_type} thickener and a dropping point of {dropping_point}°C for the specified application.",
        reasoning_framework="""
Grease selection is based on:
- NLGI grade (consistency): 000 (fluid) to 6 (block); most rolling bearings use NLGI 2.
- Thickener type: lithium (general purpose), calcium (water resistance), polyurea (high temperature), etc.
- Dropping point: temperature at which grease becomes fluid; higher is better for high-temp applications.
- Base oil viscosity and compatibility with seals/materials.
- Application speed, load, and environment.
""",
        key_factors=[
            "NLGI grade",
            "Thickener type",
            "Dropping point",
            "Base oil viscosity",
            "Application environment"
        ],
        primary_authority=[
            "NLGI Lubricating Grease Guide",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Maintenance engineer or lubricant supplier",
        adversary_position="Incorrect grease selection leads to premature failure or incompatibility.",
        counter_arguments=[
            "Consult NLGI and OEM guidelines for specific applications.",
            "Compatibility testing can prevent adverse reactions."
        ],
        resolution_strategy="Cross-reference NLGI, OEM, and application requirements; validate with field trials.",
        entity_scope="All greased components in MECH13 engine systems.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NLGI Lubricating Grease Guide; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Surface Engineering - Nitriding, PVD Coatings, and DLC for Wear Resistance",
        keywords=["surface engineering", "nitriding", "PVD", "DLC", "wear resistance", "coatings", "tribology"],
        conclusion_template="The recommended surface engineering solution is {treatment} to achieve the required wear resistance for the application.",
        reasoning_framework="""
Surface engineering enhances wear resistance by modifying the surface layer:
- Nitriding: Thermochemical diffusion of nitrogen; increases surface hardness, fatigue strength, and wear resistance.
- PVD (Physical Vapor Deposition): Deposits hard, thin coatings (e.g., TiN, CrN) for low friction and high hardness.
- DLC (Diamond-Like Carbon): Amorphous carbon coating; extremely low friction, high hardness, chemical inertness.
Selection depends on:
- Substrate material and geometry.
- Operating temperature and load.
- Required hardness, friction, and corrosion resistance.
- Cost and process compatibility.
""",
        key_factors=[
            "Substrate material",
            "Operating conditions",
            "Required surface properties",
            "Coating thickness",
            "Process cost"
        ],
        primary_authority=[
            "ASM Handbook, Vol. 18: Friction, Lubrication, and Wear Technology",
            "Holmberg, K., Matthews, A. (2009). Coatings Tribology."
        ],
        burden_holder="Component designer or surface engineer",
        adversary_position="Surface treatments may introduce residual stresses or reduce toughness.",
        counter_arguments=[
            "Process optimization and post-treatment can mitigate adverse effects.",
            "Coating selection can be tailored for specific applications."
        ],
        resolution_strategy="Conduct application-specific testing and failure analysis.",
        entity_scope="Wear-critical components in MECH13 engine assemblies.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASM Handbook Vol. 18; Holmberg & Matthews (2009)"
    ),
    DoctrineBlock(
        topic="Bearing Lubrication Design - Minimum Film Thickness Calculation",
        keywords=["bearing lubrication", "minimum film thickness", "tribology", "film formation", "bearing design"],
        conclusion_template="The minimum lubricant film thickness is calculated as {film_thickness} μm, ensuring separation of bearing surfaces under operating conditions.",
        reasoning_framework="""
Minimum film thickness is critical to prevent metal-to-metal contact in bearings. For hydrodynamic and EHL regimes, use Hamrock-Dowson or similar equations:
- For journal bearings: h_min = C * (η * N / P)^x, where C and x depend on geometry.
- For rolling bearings: Use EHL formulas as in Hamrock-Dowson.
- Ensure lambda ratio (h_min / composite roughness) > 1 for full separation.
- Consider temperature effects on viscosity and thermal expansion.
""",
        key_factors=[
            "Operating speed",
            "Load",
            "Lubricant viscosity",
            "Bearing geometry",
            "Surface roughness"
        ],
        primary_authority=[
            "Hamrock, B. J., Schmid, S. R., & Jacobson, B. O. (2004). Fundamentals of Fluid Film Lubrication.",
            "ISO 281: Rolling bearings — Dynamic load ratings and rating life"
        ],
        burden_holder="Bearing designer or tribologist",
        adversary_position="Film thickness models may not account for transient loads or contamination.",
        counter_arguments=[
            "Safety factors and real-world testing can address model limitations.",
            "Contamination control is essential for reliable operation."
        ],
        resolution_strategy="Apply conservative design margins and validate with in-service monitoring.",
        entity_scope="Bearings in MECH13 engine systems.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Hamrock et al. (2004); ISO 281"
    ),
    DoctrineBlock(
        topic="Viscosity Index Improvers - Shear Stability and Temporary vs Permanent Loss",
        keywords=["viscosity index improver", "shear stability", "temporary shear loss", "permanent shear loss", "polymeric additives"],
        conclusion_template="The selected VI improver demonstrates {shear_stability} under the specified operating conditions.",
        reasoning_framework="""
Viscosity Index (VI) improvers are polymeric additives that reduce viscosity change with temperature. Shear stability is critical:
- Temporary shear loss: Polymer chains align under shear, reducing viscosity, reversible upon rest.
- Permanent shear loss: Polymer chains break (mechanical degradation), irreversible viscosity loss.
- High-shear environments (e.g., gearboxes, high-speed bearings) require VI improvers with high mechanical stability (e.g., olefin copolymers, hydrogenated styrene-diene).
- ASTM D6278 and CEC L-14-A-93 test methods assess shear stability.
""",
        key_factors=[
            "Type of VI improver",
            "Operating shear rate",
            "Temperature",
            "Additive concentration",
            "Application environment"
        ],
        primary_authority=[
            "Totten, G. E. (2016). Lubrication and Lubricant Selection.",
            "ASTM D6278 - Standard Test Method for Shear Stability of Polymer Containing Fluids"
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="VI improvers may degrade rapidly in severe applications, compromising viscosity.",
        counter_arguments=[
            "Selection of high-stability polymers mitigates degradation.",
            "Routine oil analysis can detect viscosity loss early."
        ],
        resolution_strategy="Match VI improver to application severity; monitor in-service viscosity.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Totten (2016); ASTM D6278"
    ),
    # --- Additional doctrines for comprehensive coverage ---
    DoctrineBlock(
        topic="Boundary Lubrication - Additive Film Formation and Wear Control",
        keywords=["boundary lubrication", "additive film", "tribochemistry", "anti-wear", "EP additives"],
        conclusion_template="Boundary lubrication is achieved primarily through additive-derived films, minimizing direct asperity contact and wear.",
        reasoning_framework="""
In boundary lubrication, the lubricant film is too thin to fully separate surfaces. Protection relies on chemical additives (e.g., ZDDP, MoDTC, sulfur-phosphorus compounds) that react with metal surfaces to form protective films. These films reduce friction and wear by preventing direct metal-to-metal contact. The effectiveness depends on additive concentration, reactivity, and operating temperature.
""",
        key_factors=[
            "Additive chemistry",
            "Surface reactivity",
            "Operating temperature",
            "Contact pressure",
            "Lubricant replenishment"
        ],
        primary_authority=[
            "Mang, T., & Dresel, W. (2017). Lubricants and Lubrication.",
            "Stachowiak, G. W., & Batchelor, A. W. (2014). Engineering Tribology."
        ],
        burden_holder="Lubricant formulator",
        adversary_position="Boundary films may be depleted or removed under high load or temperature.",
        counter_arguments=[
            "Continuous additive supply and optimized chemistry prolong film life.",
            "Surface texturing can enhance film retention."
        ],
        resolution_strategy="Monitor wear rates and replenish or upgrade lubricant as needed.",
        entity_scope="All boundary-lubricated contacts in MECH13 systems.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Mang & Dresel (2017); Stachowiak & Batchelor (2014)"
    ),
    DoctrineBlock(
        topic="Mixed Lubrication - Transition Regime Management",
        keywords=["mixed lubrication", "transition regime", "asperity contact", "tribology", "film thickness"],
        conclusion_template="Mixed lubrication is managed by optimizing surface finish and lubricant properties to minimize asperity contact.",
        reasoning_framework="""
Mixed lubrication occurs when the lubricant film is comparable to surface roughness, resulting in partial asperity contact. To manage this regime:
- Optimize surface finish to reduce roughness.
- Use lubricants with effective anti-wear additives.
- Maintain appropriate viscosity to maximize film thickness.
- Monitor operating conditions to avoid excessive load or temperature.
""",
        key_factors=[
            "Surface roughness",
            "Lubricant viscosity",
            "Additive package",
            "Operating load and speed",
            "Temperature"
        ],
        primary_authority=[
            "Stachowiak, G. W., & Batchelor, A. W. (2014). Engineering Tribology.",
            "Mang, T., & Dresel, W. (2017). Lubricants and Lubrication."
        ],
        burden_holder="System designer or maintenance engineer",
        adversary_position="Mixed regime is inherently unstable and difficult to control.",
        counter_arguments=[
            "Advanced surface engineering and lubricant technology can stabilize the regime.",
            "Condition monitoring enables early detection of problems."
        ],
        resolution_strategy="Implement predictive maintenance and optimize design for regime stability.",
        entity_scope="All mixed-lubricated contacts in MECH13 systems.",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Stachowiak & Batchelor (2014); Mang & Dresel (2017)"
    ),
    DoctrineBlock(
        topic="Hydrodynamic Lubrication - Full Film Formation and Load Support",
        keywords=["hydrodynamic lubrication", "full film", "load support", "fluid film", "bearing design"],
        conclusion_template="Hydrodynamic lubrication is achieved when operating conditions allow formation of a full fluid film, supporting the applied load.",
        reasoning_framework="""
Hydrodynamic lubrication occurs when relative motion and lubricant viscosity generate a pressure profile sufficient to separate surfaces completely. The film thickness and load-carrying capacity depend on speed, viscosity, geometry, and load. Proper design ensures operation within the hydrodynamic regime, minimizing wear and friction.
""",
        key_factors=[
            "Relative speed",
            "Lubricant viscosity",
            "Bearing geometry",
            "Applied load",
            "Surface finish"
        ],
        primary_authority=[
            "Hamrock, B. J., Schmid, S. R., & Jacobson, B. O. (2004). Fundamentals of Fluid Film Lubrication.",
            "Reynolds, O. (1886). On the Theory of Lubrication."
        ],
        burden_holder="Bearing designer",
        adversary_position="Hydrodynamic regime may be lost during start/stop or overload.",
        counter_arguments=[
            "Use of auxiliary lubrication systems or soft start procedures can mitigate risk.",
            "Design for minimum load and speed requirements."
        ],
        resolution_strategy="Monitor operating parameters and design for worst-case conditions.",
        entity_scope="All hydrodynamically-lubricated bearings in MECH13 systems.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Hamrock et al. (2004); Reynolds (1886)"
    ),
    DoctrineBlock(
        topic="Wear Particle Analysis - Root Cause Diagnosis",
        keywords=["wear particle analysis", "ferrography", "root cause", "oil analysis", "failure diagnosis"],
        conclusion_template="Wear particle analysis indicates {wear_type} wear, suggesting {root_cause} as the primary cause.",
        reasoning_framework="""
Wear particle analysis (ferrography, SEM, etc.) identifies the type, size, and morphology of debris in lubricants. Interpretation:
- Large, severe particles: Indicate abnormal or catastrophic wear (e.g., spalling, scuffing).
- Fine, spherical particles: Suggest normal rubbing wear.
- Composition analysis (EDS) links debris to specific components.
- Trending particle count and morphology enables early detection of failure modes.
""",
        key_factors=[
            "Particle size and shape",
            "Particle composition",
            "Wear rate trends",
            "Equipment history",
            "Operating conditions"
        ],
        primary_authority=[
            "STLE, Lubrication Fundamentals",
            "ASTM D7684 - Standard Guide for Microscopic Characterization of Particles from In-Service Lubricants"
        ],
        burden_holder="Oil analyst or reliability engineer",
        adversary_position="Particle analysis may misidentify wear type due to contamination or sampling errors.",
        counter_arguments=[
            "Cross-reference with other diagnostic tools (vibration, temperature).",
            "Repeat sampling and confirmatory analysis."
        ],
        resolution_strategy="Integrate multiple condition monitoring techniques.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="STLE Lubrication Fundamentals; ASTM D7684"
    ),
    DoctrineBlock(
        topic="Lubricant Oxidation and Degradation - Monitoring and Control",
        keywords=["lubricant oxidation", "degradation", "monitoring", "oil change interval", "acid number", "oxidation stability"],
        conclusion_template="Lubricant condition is {status} based on oxidation and degradation indicators; oil change is {recommended_action}.",
        reasoning_framework="""
Lubricant oxidation leads to acid buildup, viscosity increase, and deposit formation. Monitoring involves:
- Acid number (ASTM D664): Indicates oxidation products.
- FTIR and RPVOT: Assess oxidation stability.
- Visual inspection for discoloration or sludge.
- Oil change intervals are based on trend analysis, not just fixed hours.
""",
        key_factors=[
            "Acid number",
            "Oxidation stability",
            "Operating temperature",
            "Oil age",
            "Contaminant levels"
        ],
        primary_authority=[
            "ASTM D664 - Standard Test Method for Acid Number of Petroleum Products",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Maintenance engineer",
        adversary_position="Oxidation indicators may lag behind actual lubricant degradation.",
        counter_arguments=[
            "Combine multiple indicators for robust assessment.",
            "Use real-time sensors for critical systems."
        ],
        resolution_strategy="Implement condition-based oil change schedules.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D664; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Grease Compatibility - Mixing and Changeover Protocols",
        keywords=["grease compatibility", "mixing", "changeover", "thickener compatibility", "lubricant management"],
        conclusion_template="Grease changeover protocol requires {procedure} due to compatibility between existing and new grease types.",
        reasoning_framework="""
Mixing incompatible greases can cause softening, hardening, or separation. Compatibility depends on thickener type (e.g., lithium, calcium, polyurea) and base oil. NLGI provides compatibility charts. During changeover:
- If compatible: purge old grease, refill.
- If incompatible: complete disassembly and cleaning required.
""",
        key_factors=[
            "Existing grease thickener",
            "New grease thickener",
            "Base oil type",
            "Application criticality",
            "Purge effectiveness"
        ],
        primary_authority=[
            "NLGI Lubricating Grease Guide",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Maintenance engineer",
        adversary_position="Field conditions may prevent complete removal of old grease.",
        counter_arguments=[
            "Use compatible greases or schedule full cleaning during major overhauls.",
            "Monitor for signs of incompatibility post-changeover."
        ],
        resolution_strategy="Follow NLGI compatibility charts and best practices.",
        entity_scope="All greased components in MECH13 engine systems.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="NLGI Lubricating Grease Guide; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Cleanliness - ISO 4406 Codes and Filtration",
        keywords=["lubricant cleanliness", "ISO 4406", "filtration", "particle count", "hydraulic systems"],
        conclusion_template="Lubricant cleanliness is maintained at ISO 4406 code {cleanliness_code} through appropriate filtration and monitoring.",
        reasoning_framework="""
ISO 4406 classifies lubricant cleanliness by counting particles >4μm, >6μm, and >14μm per mL. Cleanliness targets depend on component sensitivity:
- High-precision hydraulics: 16/14/11 or better.
- Gearboxes: 18/16/13.
Filtration system design (beta ratio, flow rate) and regular monitoring ensure compliance.
""",
        key_factors=[
            "ISO 4406 code",
            "Filtration efficiency",
            "System sensitivity",
            "Sampling frequency",
            "Contaminant sources"
        ],
        primary_authority=[
            "ISO 4406: Hydraulic fluid power — Fluid contamination",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Maintenance engineer",
        adversary_position="Contaminant ingress may exceed filtration capacity during abnormal events.",
        counter_arguments=[
            "Redundant filtration and contamination control procedures mitigate risk.",
            "Real-time monitoring enables rapid response."
        ],
        resolution_strategy="Design for worst-case contamination and implement proactive monitoring.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 4406; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Selection for High-Temperature Applications",
        keywords=["lubricant selection", "high temperature", "oxidation stability", "synthetic oil", "thermal degradation"],
        conclusion_template="For high-temperature operation, select a lubricant with {base_oil_type}, oxidation stability rating of {rating}, and suitable additive package.",
        reasoning_framework="""
High-temperature applications require lubricants with:
- High oxidation and thermal stability (Group III/IV/V base oils, esters, PAO, silicone).
- Low volatility to minimize evaporation losses.
- Additives for deposit control and anti-wear protection.
- Compatibility with seals and materials at elevated temperatures.
""",
        key_factors=[
            "Base oil type",
            "Oxidation stability",
            "Volatility",
            "Additive package",
            "Seal compatibility"
        ],
        primary_authority=[
            "Totten, G. E. (2016). Lubrication and Lubricant Selection.",
            "API 1509"
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="High-performance lubricants may be cost-prohibitive or incompatible with legacy systems.",
        counter_arguments=[
            "Cost-benefit analysis often justifies premium lubricants for critical assets.",
            "Compatibility testing can prevent failures."
        ],
        resolution_strategy="Balance performance, cost, and compatibility through testing and analysis.",
        entity_scope="High-temperature components in MECH13 engine systems.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Totten (2016); API 1509"
    ),
    DoctrineBlock(
        topic="Lubricant Selection for Low-Temperature Applications",
        keywords=["lubricant selection", "low temperature", "pour point", "viscosity", "synthetic oil"],
        conclusion_template="For low-temperature operation, select a lubricant with pour point below {min_temp}°C and sufficient low-temperature viscosity.",
        reasoning_framework="""
Low-temperature operation requires lubricants with:
- Low pour point (well below minimum ambient temperature).
- Low-temperature viscosity meeting OEM requirements (CCS, MRV).
- Synthetic base oils (PAO, esters) offer superior low-temp flow.
- Additives to prevent wax crystallization and maintain pumpability.
""",
        key_factors=[
            "Pour point",
            "Low-temperature viscosity",
            "Base oil type",
            "Additive package",
            "Pumpability"
        ],
        primary_authority=[
            "Totten, G. E. (2016). Lubrication and Lubricant Selection.",
            "API 1509"
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="Low-viscosity oils may compromise protection at higher temperatures.",
        counter_arguments=[
            "Multi-grade oils and VI improvers can balance low- and high-temp performance.",
            "OEM approvals ensure suitability."
        ],
        resolution_strategy="Select multi-grade or synthetic oils and validate with cold-cranking tests.",
        entity_scope="Low-temperature components in MECH13 engine systems.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Totten (2016); API 1509"
    ),
    DoctrineBlock(
        topic="Lubricant Compatibility with Seals and Elastomers",
        keywords=["lubricant compatibility", "seals", "elastomers", "swelling", "chemical attack"],
        conclusion_template="Lubricant is compatible with {seal_material} based on swelling, hardness change, and chemical resistance testing.",
        reasoning_framework="""
Lubricant-seal compatibility is essential to prevent leaks and degradation:
- Test for swelling, hardness change, and chemical attack (ASTM D471).
- Consider base oil type, additive chemistry, and operating temperature.
- Nitrile, FKM, and silicone elastomers have different compatibility profiles.
- Incompatible lubricants may cause excessive swelling or embrittlement.
""",
        key_factors=[
            "Seal material",
            "Base oil type",
            "Additive chemistry",
            "Operating temperature",
            "Test results"
        ],
        primary_authority=[
            "ASTM D471 - Standard Test Method for Rubber Property—Effect of Liquids",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or design engineer",
        adversary_position="Field conditions may differ from laboratory compatibility tests.",
        counter_arguments=[
            "Accelerated aging and field trials provide additional assurance.",
            "OEM approvals validate compatibility."
        ],
        resolution_strategy="Conduct both laboratory and field compatibility testing.",
        entity_scope="All lubricated seals in MECH13 engine platform.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D471; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Additive Depletion - Monitoring and Replenishment",
        keywords=["additive depletion", "oil analysis", "replenishment", "tribology", "lubricant monitoring"],
        conclusion_template="Additive depletion is at {depletion_level}; replenishment or oil change is {recommended_action}.",
        reasoning_framework="""
Additives (AW, EP, detergents, dispersants) are consumed during operation. Monitoring involves:
- Elemental analysis (ICP, XRF) for additive metals (Zn, P, Ca, Mg).
- FTIR for organic additive depletion.
- Trend analysis to predict remaining useful life.
- Replenishment is possible in some systems; otherwise, oil change is required.
""",
        key_factors=[
            "Additive concentration",
            "Operating hours",
            "Contaminant levels",
            "Oil top-up history",
            "Equipment criticality"
        ],
        primary_authority=[
            "ASTM D6595",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Maintenance engineer or oil analyst",
        adversary_position="Additive depletion rates may vary with load and contamination.",
        counter_arguments=[
            "Frequent monitoring and trending improve prediction accuracy.",
            "Critical systems may require more frequent oil changes."
        ],
        resolution_strategy="Implement condition-based maintenance and regular oil analysis.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D6595; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Foaming - Causes, Effects, and Control",
        keywords=["lubricant foaming", "air entrainment", "antifoam additives", "oil system", "tribology"],
        conclusion_template="Foaming risk is {risk_level}; control measures include {control_measures}.",
        reasoning_framework="""
Foaming occurs when air is entrained in lubricants, leading to poor lubrication and potential pump cavitation. Causes:
- High agitation, return line splashing, or leaks.
- Incompatible antifoam additives or contamination.
Control:
- Use antifoam additives (silicone, organic polymers).
- Design sump and return lines to minimize agitation.
- Regularly monitor for foaming and address root causes.
""",
        key_factors=[
            "System design",
            "Antifoam additive concentration",
            "Operating speed",
            "Contaminant presence",
            "Oil level"
        ],
        primary_authority=[
            "Totten, G. E. (2016). Lubrication and Lubricant Selection.",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="System designer or maintenance engineer",
        adversary_position="Antifoam additives may be depleted or incompatible with other additives.",
        counter_arguments=[
            "Routine monitoring and additive replenishment maintain control.",
            "System design improvements can eliminate chronic foaming."
        ],
        resolution_strategy="Combine chemical and mechanical control measures.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Totten (2016); STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Water Contamination - Detection and Mitigation",
        keywords=["water contamination", "lubricant", "Karl Fischer", "demulsibility", "oil analysis"],
        conclusion_template="Water contamination is {contamination_level}; mitigation measures include {mitigation_measures}.",
        reasoning_framework="""
Water in lubricants causes corrosion, additive depletion, and accelerated wear. Detection:
- Karl Fischer titration for quantitative analysis.
- Crackle test for field screening.
- Monitor demulsibility (ASTM D1401) for water separation capability.
Mitigation:
- Use water-resistant lubricants and seals.
- Remove water via vacuum dehydration, centrifugation, or filtration.
""",
        key_factors=[
            "Water content",
            "Demulsibility",
            "Source of ingress",
            "Operating environment",
            "Removal method"
        ],
        primary_authority=[
            "ASTM D6304 - Standard Test Method for Water in Petroleum Products",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Maintenance engineer or oil analyst",
        adversary_position="Chronic water ingress may overwhelm mitigation measures.",
        counter_arguments=[
            "System design improvements and regular monitoring reduce risk.",
            "Use of water-tolerant lubricants for severe environments."
        ],
        resolution_strategy="Implement proactive monitoring and rapid response protocols.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ASTM D6304; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Acid Number - Monitoring and Interpretation",
        keywords=["acid number", "TAN", "lubricant monitoring", "oil analysis", "oxidation"],
        conclusion_template="Acid number is {acid_number}; interpretation indicates {condition} of the lubricant.",
        reasoning_framework="""
Acid number (TAN) measures acidic constituents in lubricants, indicating oxidation or contamination. High TAN signals degradation or additive depletion. Monitoring:
- ASTM D664 for measurement.
- Trending TAN over time is more informative than single values.
- Sudden increases may indicate coolant ingress or severe oxidation.
""",
        key_factors=[
            "Acid number",
            "Trend over time",
            "Operating hours",
            "Contaminant ingress",
            "Additive package"
        ],
        primary_authority=[
            "ASTM D664 - Standard Test Method for Acid Number of Petroleum Products",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Oil analyst or maintenance engineer",
        adversary_position="TAN may increase due to additive chemistry, not just oxidation.",
        counter_arguments=[
            "Interpret TAN in context of additive package and other indicators.",
            "Use base number (BN) for balanced assessment in engine oils."
        ],
        resolution_strategy="Combine TAN with other oil analysis parameters for diagnosis.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D664; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Base Number - Monitoring for Engine Oils",
        keywords=["base number", "TBN", "engine oil", "oil analysis", "acid neutralization"],
        conclusion_template="Base number is {base_number}; interpretation indicates {condition} of the engine oil.",
        reasoning_framework="""
Base number (TBN) measures the alkaline reserve in engine oils for neutralizing acids. Monitoring:
- ASTM D2896 for measurement.
- Low TBN signals depletion of detergents and risk of corrosion.
- Trending TBN and comparing with TAN provides comprehensive assessment.
""",
        key_factors=[
            "Base number",
            "Trend over time",
            "Operating hours",
            "Fuel sulfur content",
            "Additive package"
        ],
        primary_authority=[
            "ASTM D2896 - Standard Test Method for Base Number of Petroleum Products",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Oil analyst or maintenance engineer",
        adversary_position="TBN may not correlate directly with acid neutralization in modern low-SAPS oils.",
        counter_arguments=[
            "Use TBN in conjunction with TAN and wear metals for diagnosis.",
            "Monitor for new oil formulations and adapt interpretation."
        ],
        resolution_strategy="Combine TBN with other oil analysis parameters for diagnosis.",
        entity_scope="Engine oils in MECH13 engine platform.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D2896; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Volatility - Noack Test and High-Temperature Performance",
        keywords=["volatility", "Noack test", "oil consumption", "high temperature", "evaporation loss"],
        conclusion_template="Lubricant volatility is {volatility_level} as measured by Noack test; suitability for high-temperature operation is {suitability}.",
        reasoning_framework="""
Noack volatility (ASTM D5800) measures evaporation loss at high temperature. High volatility leads to oil consumption and deposit formation. Synthetic base oils (PAO, esters) have lower volatility than mineral oils. Select lubricants with low Noack values for high-temp applications.
""",
        key_factors=[
            "Noack volatility",
            "Base oil type",
            "Operating temperature",
            "Oil consumption rate",
            "Additive volatility"
        ],
        primary_authority=[
            "ASTM D5800 - Standard Test Method for Evaporation Loss of Lubricating Oils",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="Low volatility oils may be more expensive or less compatible with legacy systems.",
        counter_arguments=[
            "Cost-benefit analysis supports premium oils for critical assets.",
            "Compatibility testing ensures suitability."
        ],
        resolution_strategy="Select low-volatility oils for high-temp or low-consumption requirements.",
        entity_scope="High-temperature components in MECH13 engine systems.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D5800; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Shear Stability - Polymer Degradation in Service",
        keywords=["shear stability", "polymer degradation", "VI improver", "lubricant", "mechanical shear"],
        conclusion_template="Shear stability is {stability_level}; lubricant is {suitability} for high-shear applications.",
        reasoning_framework="""
Shear stability refers to the resistance of VI improvers to mechanical degradation. Loss of viscosity can compromise protection. Test using ASTM D6278 or CEC L-14-A-93. Select VI improvers with proven stability for gearboxes and high-speed bearings.
""",
        key_factors=[
            "VI improver type",
            "Shear stability index",
            "Operating shear rate",
            "Application type",
            "Oil analysis results"
        ],
        primary_authority=[
            "ASTM D6278",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="All VI improvers degrade eventually under severe conditions.",
        counter_arguments=[
            "Routine oil analysis and top-up maintain performance.",
            "Use of high-stability polymers extends service life."
        ],
        resolution_strategy="Monitor viscosity in service and select polymers for application severity.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D6278; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Detergent and Dispersant Additives - Engine Cleanliness",
        keywords=["detergent additives", "dispersant additives", "engine cleanliness", "deposit control", "oil formulation"],
        conclusion_template="Detergent and dispersant additive levels are {additive_levels}; engine cleanliness is {cleanliness_status}.",
        reasoning_framework="""
Detergents neutralize acids and keep surfaces clean; dispersants suspend insolubles and prevent sludge. Monitor additive levels via elemental analysis (Ca, Mg, B for detergents; organic nitrogen for dispersants). Depletion leads to deposits and wear.
""",
        key_factors=[
            "Additive concentration",
            "Engine operating hours",
            "Fuel quality",
            "Oil analysis results",
            "Deposit formation"
        ],
        primary_authority=[
            "Totten, G. E. (2016). Lubrication and Lubricant Selection.",
            "API 1509"
        ],
        burden_holder="Lubricant formulator or oil analyst",
        adversary_position="High detergent/dispersant levels may cause ash or catalyst fouling.",
        counter_arguments=[
            "Low-SAPS formulations balance cleanliness with emissions compliance.",
            "Monitor for compatibility with aftertreatment systems."
        ],
        resolution_strategy="Select additive levels based on engine design and emissions requirements.",
        entity_scope="Engine oils in MECH13 engine platform.",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Totten (2016); API 1509"
    ),
    DoctrineBlock(
        topic="Lubricant Sulfated Ash, Phosphorus, and Sulfur (SAPS) - Emissions Compliance",
        keywords=["SAPS", "sulfated ash", "phosphorus", "sulfur", "emissions compliance", "engine oil"],
        conclusion_template="SAPS content is {saps_level}; compliance with emissions regulations is {compliance_status}.",
        reasoning_framework="""
SAPS components affect aftertreatment systems (DPF, SCR, TWC). Regulations limit SAPS to protect catalysts and filters. Low-SAPS oils are required for modern engines with advanced emissions controls. Monitor via ASTM D874 (ash), D5185 (P, S).
""",
        key_factors=[
            "SAPS content",
            "Engine emissions system",
            "Regulatory limits",
            "Oil analysis results",
            "Additive package"
        ],
        primary_authority=[
            "API 1509",
            "ACEA Oil Sequences"
        ],
        burden_holder="Lubricant formulator or emissions compliance engineer",
        adversary_position="Low-SAPS oils may compromise wear protection or cleanliness.",
        counter_arguments=[
            "Advanced additive technology maintains performance with low SAPS.",
            "OEM approvals validate oil suitability."
        ],
        resolution_strategy="Select oils certified for engine and emissions system type.",
        entity_scope="Engine oils in MECH13 engine platform.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="API 1509; ACEA Oil Sequences"
    ),
    DoctrineBlock(
        topic="Lubricant Demulsibility - Water Separation Performance",
        keywords=["demulsibility", "water separation", "lubricant", "ASTM D1401", "oil analysis"],
        conclusion_template="Demulsibility is {demulsibility_level}; lubricant is {suitability} for water-prone environments.",
        reasoning_framework="""
Demulsibility is the ability of a lubricant to separate from water. High demulsibility prevents emulsion formation and protects equipment. Test using ASTM D1401. Select lubricants with high demulsibility for gearboxes, hydraulics, and marine applications.
""",
        key_factors=[
            "Demulsibility rating",
            "Base oil type",
            "Additive package",
            "Operating environment",
            "Water contamination risk"
        ],
        primary_authority=[
            "ASTM D1401 - Standard Test Method for Water Separability of Petroleum Oils",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="Some additives may reduce demulsibility.",
        counter_arguments=[
            "Balance additive selection for performance and water separation.",
            "Monitor demulsibility in service."
        ],
        resolution_strategy="Select lubricants based on application and water exposure risk.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D1401; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Air Release - Prevention of Cavitation and Pump Damage",
        keywords=["air release", "cavitation", "pump damage", "lubricant", "ASTM D3427"],
        conclusion_template="Air release time is {air_release_time}; lubricant is {suitability} for high-speed circulation systems.",
        reasoning_framework="""
Air release is the ability of a lubricant to separate entrained air. Poor air release leads to cavitation and pump damage. Test using ASTM D3427. Select lubricants with rapid air release for high-speed or high-pressure systems.
""",
        key_factors=[
            "Air release time",
            "Base oil type",
            "System design",
            "Operating speed",
            "Oil temperature"
        ],
        primary_authority=[
            "ASTM D3427 - Standard Test Method for Air Release Properties of Petroleum Oils",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="Additives may impair air release properties.",
        counter_arguments=[
            "Balance additive selection for all performance aspects.",
            "Monitor air release in service."
        ],
        resolution_strategy="Select lubricants based on system requirements and test results.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D3427; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Filterability - Hydraulic and Circulating Systems",
        keywords=["filterability", "hydraulic oil", "circulating oil", "filter plugging", "ASTM D7899"],
        conclusion_template="Filterability is {filterability_rating}; lubricant is {suitability} for fine filtration systems.",
        reasoning_framework="""
Filterability is the ability of a lubricant to pass through fine filters without plugging. Poor filterability leads to pressure drop and bypass. Test using ASTM D7899. Select lubricants with high filterability for hydraulic and circulating systems.
""",
        key_factors=[
            "Filterability rating",
            "Additive package",
            "Contaminant load",
            "Filter pore size",
            "Operating environment"
        ],
        primary_authority=[
            "ASTM D7899 - Standard Test Method for Filterability of Lubricating Oils",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Lubricant formulator or maintenance engineer",
        adversary_position="Some additives or contaminants may cause filter plugging.",
        counter_arguments=[
            "Monitor filter differential pressure and change filters as needed.",
            "Select lubricants tested for filterability with system filters."
        ],
        resolution_strategy="Match lubricant and filter selection to application requirements.",
        entity_scope="Hydraulic and circulating systems in MECH13 engine platform.",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D7899; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Compatibility with Non-Ferrous Metals",
        keywords=["lubricant compatibility", "non-ferrous metals", "copper corrosion", "ASTM D130", "tribology"],
        conclusion_template="Lubricant is {compatibility_status} with non-ferrous metals based on copper corrosion test results.",
        reasoning_framework="""
Some lubricants or additives may corrode non-ferrous metals (copper, brass, bronze). Test using ASTM D130. Select lubricants with low corrosivity for systems with non-ferrous components.
""",
        key_factors=[
            "Copper corrosion rating",
            "Additive chemistry",
            "Base oil type",
            "Operating temperature",
            "Component material"
        ],
        primary_authority=[
            "ASTM D130 - Standard Test Method for Corrosiveness to Copper from Petroleum Products",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Lubricant formulator or design engineer",
        adversary_position="Field conditions may accelerate corrosion beyond lab test results.",
        counter_arguments=[
            "Monitor in-service corrosion and adjust lubricant selection as needed.",
            "Use passivating additives for sensitive systems."
        ],
        resolution_strategy="Select lubricants based on component materials and test results.",
        entity_scope="All lubricated systems with non-ferrous metals in MECH13 engine platform.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="ASTM D130; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Compatibility with Paints and Plastics",
        keywords=["lubricant compatibility", "paints", "plastics", "chemical attack", "tribology"],
        conclusion_template="Lubricant is {compatibility_status} with specified paints and plastics based on compatibility testing.",
        reasoning_framework="""
Some lubricants or additives may soften, swell, or discolor paints and plastics. Compatibility testing involves exposure of materials to lubricant at operating temperature and assessment of physical changes. Select lubricants with proven compatibility for systems with sensitive materials.
""",
        key_factors=[
            "Material type",
            "Base oil type",
            "Additive chemistry",
            "Operating temperature",
            "Test results"
        ],
        primary_authority=[
            "Totten, G. E. (2016). Lubrication and Lubricant Selection.",
            "ASTM D471"
        ],
        burden_holder="Lubricant formulator or design engineer",
        adversary_position="Unexpected interactions may occur with new materials or formulations.",
        counter_arguments=[
            "Conduct comprehensive compatibility testing for all materials.",
            "Monitor for field issues and adjust lubricant as needed."
        ],
        resolution_strategy="Test all materials in contact with lubricant under representative conditions.",
        entity_scope="All lubricated systems with paints/plastics in MECH13 engine platform.",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Totten (2016); ASTM D471"
    ),
    DoctrineBlock(
        topic="Lubricant Replenishment Interval Optimization",
        keywords=["lubricant replenishment", "interval optimization", "oil change", "condition monitoring", "tribology"],
        conclusion_template="Optimal lubricant replenishment interval is {interval} hours based on condition monitoring and operating environment.",
        reasoning_framework="""
Lubricant change intervals should be based on oil analysis (TAN, TBN, viscosity, wear metals), not just fixed hours. Condition-based maintenance reduces costs and prevents failures. Adjust intervals for severe service, contamination, or additive depletion.
""",
        key_factors=[
            "Oil analysis results",
            "Operating hours",
            "Contamination level",
            "Additive depletion",
            "Operating environment"
        ],
        primary_authority=[
            "STLE, Lubrication Fundamentals",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Maintenance engineer",
        adversary_position="Condition monitoring may miss sudden failures or contamination events.",
        counter_arguments=[
            "Combine fixed and condition-based intervals for critical assets.",
            "Rapid response protocols for abnormal results."
        ],
        resolution_strategy="Implement hybrid maintenance schedules and frequent monitoring.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="STLE Lubrication Fundamentals; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Storage and Handling - Contamination Prevention",
        keywords=["lubricant storage", "handling", "contamination prevention", "best practices", "tribology"],
        conclusion_template="Lubricant storage and handling procedures are {compliance_status} with best practices for contamination prevention.",
        reasoning_framework="""
Proper storage and handling prevent contamination and degradation:
- Use sealed, labeled containers.
- Store in cool, dry, clean areas away from chemicals.
- Use dedicated transfer equipment.
- Filter new oil before use.
- Train personnel in best practices.
""",
        key_factors=[
            "Storage conditions",
            "Container integrity",
            "Transfer equipment",
            "Personnel training",
            "Contamination incidents"
        ],
        primary_authority=[
            "STLE, Lubrication Fundamentals",
            "Totten, G. E. (2016). Lubrication and Lubricant Selection."
        ],
        burden_holder="Maintenance engineer or lubricant supplier",
        adversary_position="Field conditions may not allow ideal storage or handling.",
        counter_arguments=[
            "Implement practical best practices and continuous improvement.",
            "Monitor for contamination and address root causes."
        ],
        resolution_strategy="Regular audits and training to maintain best practices.",
        entity_scope="All lubricants in MECH13 engine platform.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="STLE Lubrication Fundamentals; Totten (2016)"
    ),
    DoctrineBlock(
        topic="Lubricant Disposal and Environmental Compliance",
        keywords=["lubricant disposal", "environmental compliance", "waste oil", "regulations", "tribology"],
        conclusion_template="Lubricant disposal procedures are {compliance_status} with environmental regulations and best practices.",
        reasoning_framework="""
Used lubricants must be disposed of in accordance with local, national, and international regulations:
- Segregate waste oil from other wastes.
- Use licensed waste handlers.
- Maintain records of disposal.
- Consider recycling or re-refining options.
- Train personnel in environmental compliance.
""",
        key_factors=[
            "Disposal method",
            "Regulatory compliance",
            "Record keeping",
            "Waste segregation",
            "Personnel training"
        ],
        primary_authority=[
            "EPA regulations",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Maintenance engineer or facility manager",
        adversary_position="Improper disposal may result in environmental harm and legal penalties.",
        counter_arguments=[
            "Strict adherence to regulations and training minimizes risk.",
            "Regular audits ensure compliance."
        ],
        resolution_strategy="Implement robust disposal protocols and maintain compliance documentation.",
        entity_scope="All lubricants in MECH13 engine platform.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA regulations; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Fire Safety - Flash Point and Storage Precautions",
        keywords=["fire safety", "flash point", "lubricant storage", "combustion risk", "tribology"],
        conclusion_template="Fire safety risk is {risk_level}; storage and handling procedures are {compliance_status} with fire safety guidelines.",
        reasoning_framework="""
Flash point is the lowest temperature at which lubricant vapors ignite. Store lubricants away from ignition sources, in fire-rated cabinets if required. Use lubricants with high flash points for high-temperature applications. Train personnel in fire safety.
""",
        key_factors=[
            "Flash point",
            "Storage conditions",
            "Ignition sources",
            "Personnel training",
            "Fire suppression systems"
        ],
        primary_authority=[
            "NFPA codes",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Maintenance engineer or facility manager",
        adversary_position="Accidental ignition may occur due to human error or equipment failure.",
        counter_arguments=[
            "Implement fire safety training and maintain fire suppression systems.",
            "Regular audits and risk assessments."
        ],
        resolution_strategy="Follow NFPA and facility fire safety protocols.",
        entity_scope="All lubricants in MECH13 engine platform.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NFPA codes; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Labeling and Traceability - Quality Assurance",
        keywords=["labeling", "traceability", "quality assurance", "lubricant", "inventory control"],
        conclusion_template="Lubricant labeling and traceability procedures are {compliance_status} with quality assurance standards.",
        reasoning_framework="""
Label all lubricant containers with product name, batch number, and expiration date. Maintain records for traceability. Use barcode or RFID systems for inventory control. Traceability ensures rapid response to quality issues or recalls.
""",
        key_factors=[
            "Labeling accuracy",
            "Batch traceability",
            "Inventory records",
            "Quality audits",
            "Recall procedures"
        ],
        primary_authority=[
            "ISO 9001",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Maintenance engineer or lubricant supplier",
        adversary_position="Labeling errors or record loss may compromise traceability.",
        counter_arguments=[
            "Implement redundant record-keeping and regular audits.",
            "Use digital inventory management systems."
        ],
        resolution_strategy="Follow ISO 9001 and facility quality assurance protocols.",
        entity_scope="All lubricants in MECH13 engine platform.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 9001; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Sampling Best Practices - Representative Analysis",
        keywords=["sampling", "oil analysis", "best practices", "representative sample", "tribology"],
        conclusion_template="Sampling procedure is {compliance_status} with best practices, ensuring representative oil analysis results.",
        reasoning_framework="""
Proper sampling ensures oil analysis accuracy:
- Sample from active system flow, not stagnant areas.
- Use clean, sealed bottles and tools.
- Label samples with date, time, and location.
- Follow ASTM D4057 or ISO 3170 procedures.
- Train personnel in sampling techniques.
""",
        key_factors=[
            "Sampling location",
            "Cleanliness of tools",
            "Labeling accuracy",
            "Personnel training",
            "Sampling frequency"
        ],
        primary_authority=[
            "ASTM D4057 - Standard Practice for Manual Sampling of Petroleum and Petroleum Products",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Maintenance engineer or oil analyst",
        adversary_position="Improper sampling may yield misleading analysis results.",
        counter_arguments=[
            "Regular training and audits improve sampling quality.",
            "Repeat sampling if results are suspect."
        ],
        resolution_strategy="Implement robust sampling protocols and continuous improvement.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D4057; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Viscosity Classification - SAE, ISO, and AGMA Standards",
        keywords=["viscosity classification", "SAE", "ISO", "AGMA", "lubricant selection", "tribology"],
        conclusion_template="Viscosity grade is selected as {viscosity_grade} according to {standard} for the application.",
        reasoning_framework="""
Viscosity classification ensures proper lubricant selection:
- SAE grades for engine and gear oils (e.g., SAE 5W-30, 80W-90).
- ISO VG for industrial oils (e.g., ISO VG 32, 68, 100).
- AGMA grades for gear lubricants.
Select grade based on OEM recommendations, operating temperature, and load.
""",
        key_factors=[
            "Operating temperature",
            "OEM recommendations",
            "Load conditions",
            "Viscosity index",
            "Application type"
        ],
        primary_authority=[
            "SAE J300, J306",
            "ISO 3448",
            "AGMA 9005"
        ],
        burden_holder="Lubricant formulator or application engineer",
        adversary_position="Viscosity grade alone does not guarantee performance under all conditions.",
        counter_arguments=[
            "Combine viscosity selection with additive and base oil considerations.",
            "Monitor in-service viscosity for confirmation."
        ],
        resolution_strategy="Follow OEM and industry standards; validate with field performance.",
        entity_scope="All lubricated systems in MECH13 engine platform.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J300/J306; ISO 3448; AGMA 9005"
    ),
    DoctrineBlock(
        topic="Lubricant Reuse and Re-Refining - Circular Economy Considerations",
        keywords=["lubricant reuse", "re-refining", "circular economy", "waste oil", "sustainability"],
        conclusion_template="Lubricant reuse and re-refining practices are {compliance_status} with circular economy and sustainability goals.",
        reasoning_framework="""
Re-refining converts used oil into high-quality base oil. Reuse and recycling reduce environmental impact and resource consumption. Follow regulatory guidelines for collection, processing, and quality assurance of re-refined oils.
""",
        key_factors=[
            "Re-refining process quality",
            "Regulatory compliance",
            "Quality assurance",
            "Environmental impact",
            "Cost-benefit analysis"
        ],
        primary_authority=[
            "API 1509",
            "EPA regulations",
            "STLE, Lubrication Fundamentals"
        ],
        burden_holder="Facility manager or lubricant supplier",
        adversary_position="Re-refined oils may have inconsistent quality or limited OEM approvals.",
        counter_arguments=[
            "Modern re-refining achieves base oil quality equal to virgin oils.",
            "OEM approvals and certification ensure suitability."
        ],
        resolution_strategy="Source re-refined oils from reputable suppliers and monitor quality.",
        entity_scope="All lubricants in MECH13 engine platform.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API 1509; EPA regulations; STLE Lubrication Fundamentals"
    ),
    DoctrineBlock(
        topic="Lubricant Additive Synergy and Antagonism - Formulation Optimization",
        keywords=["additive synergy", "additive antagonism", "formulation", "lubricant", "tribology"],
        conclusion_template="Additive package is {optimization_status} for synergy and minimal antagonism, ensuring optimal lubricant performance.",
        reasoning_framework="""
Some additives enhance each other's performance (synergy), while others interfere (antagonism). For example, detergents may inhibit AW/EP film formation. Formulation optimization involves balancing additive concentrations and testing for performance in target applications.
""",
        key_factors=[
            "Additive compatibility",
            "Performance testing",
            "Application requirements",
            "OEM approvals",
            "Field experience"
        ],
        primary_authority=[
            "Totten, G. E. (2016). Lubrication and Lubricant Selection.",
            "API 1509"
        ],
        burden_holder="Lubricant formulator",
        adversary_position="Unexpected additive interactions may occur with new formulations.",
        counter_arguments=[
            "Comprehensive laboratory and field testing minimize risk.",
            "Continuous improvement and feedback from service data."
        ],
        resolution_strategy="Test formulations thoroughly and monitor field performance.",
        entity_scope="All lubricants in MECH13 engine platform.",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Totten (2016); API 1509"
    ),
    DoctrineBlock(
        topic="Lubricant Tribofilm Formation - Surface Protection Mechanisms",
        keywords=["tribofilm", "surface protection", "additive film", "tribology", "anti-wear"],
        conclusion_template="Tribofilm formation is {effectiveness_level}, providing {protection_level} surface protection under operating conditions.",
        reasoning_framework="""
Tribofilms are protective layers formed by chemical reaction of additives with surfaces under load and temperature. Effectiveness depends on additive chemistry, surface reactivity, and operating conditions. Monitor via surface analysis (XPS, AES) and wear testing.
""",
        key_factors=[
            "Additive chemistry",
            "Surface reactivity",
            "Operating temperature",
            "Contact pressure",
            "Wear test results"
        ],
        primary_authority=[
            "Mang, T., & Dresel, W. (2017). Lubricants and Lubrication.",
            "Stachowiak, G. W., & Batchelor, A. W. (2014). Engineering Tribology."
        ],
        burden_holder="Lubricant formulator or tribologist",
        adversary_position="Tribofilm formation may be hindered by contaminants or surface passivation.",
        counter_arguments=[
            "Surface pre-treatment and additive optimization enhance tribofilm formation.",
            "Monitor for contaminants and maintain lubricant cleanliness."
        ],
        resolution_strategy="Optimize additive package and maintain clean operating environment.",
        entity_scope="All tribological contacts in MECH13 engine platform.",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Mang & Dresel (2017); Stachowiak & Batchelor (2014)"
    ),
    DoctrineBlock(
        topic="Lubricant Micro-Pitting Resistance - Gear and