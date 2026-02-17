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
        topic="Bernoulli vs Circulation Theory of Lift",
        keywords=["Bernoulli", "Circulation", "Lift", "Aerodynamics", "Kutta-Joukowski", "Pressure Differential"],
        conclusion_template="Lift generation in subsonic airfoils is best explained by circulation theory, with Bernoulli's principle providing a partial but incomplete description.",
        reasoning_framework=(
            "The Bernoulli principle posits that faster airflow over the wing results in lower pressure, creating lift. However, this explanation is incomplete, "
            "as it does not account for the necessity of circulation around the airfoil. The circulation theory, formalized by the Kutta-Joukowski theorem, "
            "explains lift as a result of the net circulation of air induced by the airfoil shape and angle of attack. Experimental evidence shows that lift "
            "cannot be fully explained by Bernoulli's equation alone, especially in cases involving complex flow patterns, separated flows, or high angles of attack. "
            "The circulation theory incorporates boundary conditions at the trailing edge (Kutta condition) and matches observed lift values across a wide range of airfoil geometries. "
            "Both theories are interconnected: circulation creates velocity differences, which Bernoulli's principle translates into pressure differences. "
            "However, circulation theory is the primary framework for quantitative lift prediction in modern aerodynamics."
        ),
        key_factors=["Airfoil shape", "Angle of attack", "Flow velocity", "Boundary conditions", "Viscous effects"],
        primary_authority=["Kutta-Joukowski theorem", "Prandtl's lifting line theory", "NASA Aerodynamics Reference"],
        burden_holder="Proponent of Bernoulli-only explanation",
        adversary_position="Circulation theory is unnecessary; Bernoulli alone suffices",
        counter_arguments=[
            "Bernoulli's principle does not explain the origin of velocity differences",
            "Experimental lift values do not match Bernoulli-only predictions",
            "Circulation theory accounts for trailing edge effects and vortex formation"
        ],
        resolution_strategy="Demonstrate lift prediction accuracy using circulation theory and compare with Bernoulli-only results",
        entity_scope="Subsonic fixed-wing aircraft",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Kutta-Joukowski theorem"
    ),
    DoctrineBlock(
        topic="Drag Decomposition: Parasitic, Induced, Wave",
        keywords=["Drag", "Parasitic", "Induced", "Wave", "Aerodynamics", "Decomposition"],
        conclusion_template="Total aircraft drag is the sum of parasitic, induced, and wave drag components, each governed by distinct physical mechanisms.",
        reasoning_framework=(
            "Drag on an aircraft is decomposed into three principal components: parasitic drag, induced drag, and wave drag. "
            "Parasitic drag includes form drag, skin friction, and interference drag, all arising from viscous effects and surface interactions. "
            "Induced drag is a consequence of lift generation, resulting from the creation of wingtip vortices and the associated downwash. "
            "Wave drag becomes significant at transonic and supersonic speeds due to shock wave formation and compressibility effects. "
            "Each drag component is quantified using empirical and theoretical models: parasitic drag scales with the square of velocity, "
            "induced drag inversely with aspect ratio and increases with lift coefficient, and wave drag is a function of Mach number and airfoil thickness. "
            "Accurate drag decomposition is essential for performance prediction, design optimization, and regulatory compliance."
        ),
        key_factors=["Aircraft speed", "Wing aspect ratio", "Airfoil thickness", "Mach number", "Surface roughness"],
        primary_authority=["Raymer's Aircraft Design", "NASA Technical Reports", "Prandtl's lifting line theory"],
        burden_holder="Designer seeking drag minimization",
        adversary_position="Drag cannot be reliably decomposed; components overlap",
        counter_arguments=[
            "Empirical data supports distinct drag components",
            "Mathematical models accurately predict drag breakdown",
            "Design interventions target specific drag types"
        ],
        resolution_strategy="Apply validated drag models and compare with wind tunnel data",
        entity_scope="All aircraft types",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Raymer's Aircraft Design"
    ),
    DoctrineBlock(
        topic="NACA Airfoil Designation and Characteristics",
        keywords=["NACA", "Airfoil", "Designation", "Characteristics", "Aerodynamics"],
        conclusion_template="NACA airfoil designation encodes geometric parameters that determine aerodynamic characteristics, enabling systematic selection for design requirements.",
        reasoning_framework=(
            "The NACA airfoil designation system uses a numerical code to specify airfoil geometry. For example, the NACA 2412 airfoil: "
            "the first digit (2) indicates maximum camber as a percentage of chord, the second digit (4) is the location of maximum camber in tenths of chord, "
            "and the last two digits (12) represent maximum thickness as a percentage of chord. "
            "NACA airfoils are extensively documented, with performance curves available for lift, drag, and stall characteristics. "
            "Designers select airfoils based on desired performance, structural constraints, and Reynolds number regime. "
            "The system facilitates rapid comparison and optimization, with modifications (e.g., NACA 5-digit series) providing enhanced control over leading edge radius and camber distribution."
        ),
        key_factors=["Camber", "Thickness", "Chord length", "Reynolds number", "Performance curves"],
        primary_authority=["NACA Technical Reports", "Abbott & von Doenhoff's Theory of Wing Sections"],
        burden_holder="Designer proposing airfoil selection",
        adversary_position="NACA designation is insufficient; empirical testing is required",
        counter_arguments=[
            "NACA airfoils are validated by extensive wind tunnel data",
            "Designation system enables systematic selection",
            "Empirical testing supplements but does not replace designation"
        ],
        resolution_strategy="Combine designation-based selection with empirical validation",
        entity_scope="Fixed-wing aircraft",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Abbott & von Doenhoff's Theory of Wing Sections"
    ),
    DoctrineBlock(
        topic="Boundary Layer Transition and Turbulence",
        keywords=["Boundary Layer", "Transition", "Turbulence", "Laminar", "Aerodynamics"],
        conclusion_template="Boundary layer transition from laminar to turbulent flow is governed by Reynolds number, surface roughness, and pressure gradients, affecting drag and heat transfer.",
        reasoning_framework=(
            "The boundary layer initially forms as laminar flow near the leading edge, transitioning to turbulence as Reynolds number increases or surface roughness is encountered. "
            "Turbulent boundary layers have higher momentum transfer, increasing skin friction drag but reducing flow separation. "
            "Transition location is influenced by pressure gradients, surface contamination, and environmental factors. "
            "Designers may employ laminar flow control techniques, such as smooth surfaces and favorable pressure gradients, to delay transition and reduce drag. "
            "However, turbulent boundary layers are more resilient to adverse pressure gradients, providing stability against stall and separation."
        ),
        key_factors=["Reynolds number", "Surface roughness", "Pressure gradient", "Environmental contamination", "Flow velocity"],
        primary_authority=["Schlichting's Boundary Layer Theory", "NASA Flow Transition Studies"],
        burden_holder="Designer advocating laminar flow control",
        adversary_position="Turbulence is inevitable; laminar flow is impractical",
        counter_arguments=[
            "Laminar flow can be sustained with careful design",
            "Turbulent transition is predictable and manageable",
            "Hybrid boundary layers optimize performance"
        ],
        resolution_strategy="Use flow visualization and surface treatments to manage transition",
        entity_scope="Aircraft surfaces",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Schlichting's Boundary Layer Theory"
    ),
    DoctrineBlock(
        topic="Stall Characteristics: Leading Edge vs Trailing Edge",
        keywords=["Stall", "Leading Edge", "Trailing Edge", "Aerodynamics", "Airfoil"],
        conclusion_template="Stall onset and progression are determined by airfoil geometry, with leading edge stall associated with abrupt lift loss and trailing edge stall with gradual degradation.",
        reasoning_framework=(
            "Stall occurs when the airflow separates from the airfoil, reducing lift. Leading edge stall is characterized by abrupt separation near the nose, resulting in rapid loss of lift and control. "
            "Trailing edge stall involves gradual separation starting at the rear, leading to more predictable and controllable behavior. "
            "Airfoil shape, camber, and thickness influence stall type: thin, sharp-nosed airfoils tend toward leading edge stall, while thicker, more cambered airfoils favor trailing edge stall. "
            "Designers select airfoils and wing planforms to optimize stall characteristics for safety and handling."
        ),
        key_factors=["Airfoil geometry", "Angle of attack", "Camber", "Thickness", "Surface roughness"],
        primary_authority=["Abbott & von Doenhoff", "NASA Stall Studies"],
        burden_holder="Manufacturer claiming benign stall",
        adversary_position="All stalls are abrupt and dangerous",
        counter_arguments=[
            "Airfoil selection controls stall behavior",
            "Trailing edge stall is more manageable",
            "Flight testing confirms stall characteristics"
        ],
        resolution_strategy="Validate stall type via wind tunnel and flight testing",
        entity_scope="Fixed-wing aircraft",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="Abbott & von Doenhoff"
    ),
    DoctrineBlock(
        topic="High-Lift Devices: Slats, Flaps, Krueger Flaps",
        keywords=["High-Lift", "Slats", "Flaps", "Krueger Flaps", "Aerodynamics"],
        conclusion_template="High-lift devices increase maximum lift coefficient and delay stall, enabling lower takeoff and landing speeds.",
        reasoning_framework=(
            "Slats, flaps, and Krueger flaps are deployed to modify wing geometry, increasing camber and surface area. "
            "Slats create a slot at the leading edge, energizing the boundary layer and delaying stall. "
            "Flaps (plain, split, Fowler, etc.) increase trailing edge camber, enhancing lift. "
            "Krueger flaps deploy from the lower leading edge, providing similar benefits to slats but with simpler mechanisms. "
            "The combined effect is higher maximum lift coefficient (CLmax), reduced stall speed, and improved low-speed handling. "
            "Deployment schedules are optimized for takeoff, approach, and landing phases."
        ),
        key_factors=["Device type", "Deployment angle", "Wing geometry", "Flight phase", "Lift coefficient"],
        primary_authority=["Raymer's Aircraft Design", "NASA High-Lift Studies"],
        burden_holder="Manufacturer claiming improved low-speed performance",
        adversary_position="High-lift devices add complexity and weight",
        counter_arguments=[
            "Performance gains outweigh complexity",
            "Modern designs minimize weight penalties",
            "Operational safety is enhanced"
        ],
        resolution_strategy="Quantify lift gains and compare with weight/complexity trade-offs",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Raymer's Aircraft Design"
    ),
    DoctrineBlock(
        topic="Wing Planform Design: Aspect Ratio, Sweep, Taper",
        keywords=["Wing Planform", "Aspect Ratio", "Sweep", "Taper", "Aerodynamics"],
        conclusion_template="Wing planform parameters—aspect ratio, sweep, and taper—determine aerodynamic efficiency, stability, and performance across speed regimes.",
        reasoning_framework=(
            "Aspect ratio (span squared divided by area) influences induced drag and lift efficiency; higher aspect ratios reduce induced drag but increase structural weight. "
            "Sweep angle delays compressibility effects, allowing higher critical Mach numbers and improved transonic performance. "
            "Taper ratio affects lift distribution and stall progression, with moderate taper optimizing both. "
            "Planform selection balances aerodynamic gains against structural and manufacturing constraints, tailored to mission requirements."
        ),
        key_factors=["Aspect ratio", "Sweep angle", "Taper ratio", "Structural weight", "Mission profile"],
        primary_authority=["Raymer's Aircraft Design", "NASA Wing Design Studies"],
        burden_holder="Designer proposing planform changes",
        adversary_position="Planform changes yield marginal benefits",
        counter_arguments=[
            "Planform optimization is central to performance",
            "Empirical data supports planform effects",
            "Structural advances enable high aspect ratios"
        ],
        resolution_strategy="Model planform effects and validate with flight data",
        entity_scope="All aircraft",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Raymer's Aircraft Design"
    ),
    DoctrineBlock(
        topic="Compressibility Effects and Critical Mach Number",
        keywords=["Compressibility", "Critical Mach", "Aerodynamics", "Transonic", "Shock Waves"],
        conclusion_template="Compressibility effects become significant near critical Mach number, leading to shock formation, drag rise, and flow separation.",
        reasoning_framework=(
            "As aircraft speed approaches the critical Mach number, local airflow over the wing exceeds Mach 1, causing shock waves and abrupt drag rise. "
            "Compressibility alters pressure distribution, reduces lift, and can induce flow separation. "
            "Designers mitigate these effects with swept wings, thinner airfoils, and area ruling. "
            "Critical Mach number is determined by airfoil shape and thickness, with modern designs targeting higher values for improved performance."
        ),
        key_factors=["Mach number", "Airfoil thickness", "Sweep angle", "Pressure distribution", "Shock strength"],
        primary_authority=["NASA Compressibility Studies", "Raymer's Aircraft Design"],
        burden_holder="Designer proposing high-speed improvements",
        adversary_position="Compressibility effects are negligible below Mach 1",
        counter_arguments=[
            "Drag rise occurs well below Mach 1",
            "Shock formation is observed in wind tunnel tests",
            "Design interventions are effective"
        ],
        resolution_strategy="Analyze flow using CFD and wind tunnel data",
        entity_scope="Transonic and supersonic aircraft",
        confidence=0.93,
        confidence_zone="Medium-High",
        controlling_precedent="NASA Compressibility Studies"
    ),
    DoctrineBlock(
        topic="Supersonic Aerodynamics: Shocks, Expansion Fans, Wave Drag",
        keywords=["Supersonic", "Shocks", "Expansion Fans", "Wave Drag", "Aerodynamics"],
        conclusion_template="Supersonic flight is dominated by shock waves, expansion fans, and wave drag, requiring specialized airfoil and fuselage designs.",
        reasoning_framework=(
            "At supersonic speeds, shock waves form at leading and trailing edges, causing abrupt changes in pressure and temperature. "
            "Expansion fans occur at convex surfaces, accelerating flow and reducing pressure. "
            "Wave drag arises from shock formation, scaling with Mach number and airfoil thickness. "
            "Designs employ thin, sharp-edged airfoils, area ruling, and variable sweep to minimize wave drag and manage shock locations. "
            "Flight control and stability are affected by shock-induced separation and pressure gradients."
        ),
        key_factors=["Mach number", "Airfoil shape", "Area ruling", "Shock strength", "Expansion fan geometry"],
        primary_authority=["NASA Supersonic Studies", "Anderson's Fundamentals of Aerodynamics"],
        burden_holder="Designer proposing supersonic configuration",
        adversary_position="Supersonic effects are similar to subsonic",
        counter_arguments=[
            "Shock waves fundamentally alter flow",
            "Wave drag dominates at supersonic speeds",
            "Designs must address unique challenges"
        ],
        resolution_strategy="Model supersonic flow and validate with wind tunnel and flight data",
        entity_scope="Supersonic aircraft",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NASA Supersonic Studies"
    ),
    DoctrineBlock(
        topic="Longitudinal Stability: Static Margin and Neutral Point",
        keywords=["Longitudinal Stability", "Static Margin", "Neutral Point", "Aerodynamics"],
        conclusion_template="Longitudinal stability is ensured by maintaining a positive static margin, with the center of gravity ahead of the neutral point.",
        reasoning_framework=(
            "Longitudinal stability requires the aircraft to return to equilibrium after pitch disturbances. "
            "Static margin is defined as the distance between the center of gravity (CG) and the neutral point, expressed as a percentage of mean aerodynamic chord. "
            "A positive static margin ensures stable pitch response; negative margin leads to instability. "
            "The neutral point is determined by aerodynamic center locations of wing and tail surfaces. "
            "Designers balance CG location, tail volume, and control surface sizing to achieve desired stability and handling."
        ),
        key_factors=["Center of gravity", "Neutral point", "Tail volume", "Aerodynamic center", "Control surfaces"],
        primary_authority=["Raymer's Aircraft Design", "NASA Stability Studies"],
        burden_holder="Manufacturer claiming stable configuration",
        adversary_position="Static margin is irrelevant; CG location suffices",
        counter_arguments=[
            "Static margin quantifies stability",
            "Neutral point is aerodynamic, not geometric",
            "Flight testing confirms stability predictions"
        ],
        resolution_strategy="Calculate static margin and validate with flight tests",
        entity_scope="All aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Raymer's Aircraft Design"
    ),
    DoctrineBlock(
        topic="Aircraft Performance: Breguet Range Equation",
        keywords=["Performance", "Breguet Range", "Fuel Efficiency", "Aerodynamics"],
        conclusion_template="The Breguet range equation relates aircraft range to fuel efficiency, aerodynamic parameters, and engine performance.",
        reasoning_framework=(
            "The Breguet range equation models the maximum range of an aircraft based on lift-to-drag ratio, fuel consumption, and initial/final weight. "
            "Range increases with higher aerodynamic efficiency (L/D), lower specific fuel consumption, and greater fuel fraction. "
            "The equation is derived from energy conservation principles and validated by operational data. "
            "Designers use the equation to optimize configuration and mission planning."
        ),
        key_factors=["Lift-to-drag ratio", "Fuel consumption", "Weight fraction", "Engine efficiency", "Mission profile"],
        primary_authority=["Raymer's Aircraft Design", "Breguet's Original Papers"],
        burden_holder="Operator claiming extended range",
        adversary_position="Range equations are simplistic; real-world factors dominate",
        counter_arguments=[
            "Breguet equation is validated by operational data",
            "Additional factors can be incorporated",
            "Equation provides baseline for optimization"
        ],
        resolution_strategy="Combine equation with empirical corrections for operational factors",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Raymer's Aircraft Design"
    ),
    DoctrineBlock(
        topic="V-Speeds: Vs, Vmc, Vr, V1, Vx, Vy, Vne",
        keywords=["V-Speeds", "Vs", "Vmc", "Vr", "V1", "Vx", "Vy", "Vne", "Performance"],
        conclusion_template="V-speeds define critical velocity thresholds for safe operation, takeoff, climb, and structural limits.",
        reasoning_framework=(
            "Vs (stall speed), Vmc (minimum control speed), Vr (rotation speed), V1 (decision speed), Vx (best angle climb), Vy (best rate climb), and Vne (never exceed speed) are standardized for operational safety. "
            "Each speed is determined by aerodynamic, engine, and structural parameters. "
            "Pilots must adhere to V-speeds for safe takeoff, climb, and cruise. "
            "Regulatory authorities mandate V-speed determination and documentation."
        ),
        key_factors=["Aircraft weight", "Configuration", "Engine power", "Aerodynamic limits", "Regulatory standards"],
        primary_authority=["FAA Regulations", "Raymer's Aircraft Design", "Aircraft Flight Manuals"],
        burden_holder="Operator ensuring compliance",
        adversary_position="V-speeds are arbitrary; pilot judgment suffices",
        counter_arguments=[
            "V-speeds are empirically determined",
            "Regulations require adherence",
            "Safety depends on V-speed observance"
        ],
        resolution_strategy="Document V-speeds and train pilots in their application",
        entity_scope="All aircraft",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Propeller Aerodynamics: Blade Element Theory",
        keywords=["Propeller", "Blade Element Theory", "Aerodynamics", "Performance"],
        conclusion_template="Blade element theory enables detailed analysis of propeller performance by modeling each blade section as an independent airfoil.",
        reasoning_framework=(
            "Blade element theory divides the propeller blade into small segments, each analyzed as an airfoil with local angle of attack and velocity. "
            "Performance is integrated across the blade, accounting for induced velocities and rotational effects. "
            "Theory supports optimization of blade twist, pitch, and planform for efficiency. "
            "Empirical corrections address three-dimensional effects and compressibility at high speeds."
        ),
        key_factors=["Blade geometry", "Twist", "Pitch", "Local velocity", "Induced effects"],
        primary_authority=["NASA Propeller Studies", "Raymer's Aircraft Design"],
        burden_holder="Manufacturer claiming propeller efficiency",
        adversary_position="Blade element theory is too simplistic",
        counter_arguments=[
            "Theory is validated by wind tunnel and flight tests",
            "Empirical corrections improve accuracy",
            "Designs use blade element theory for optimization"
        ],
        resolution_strategy="Combine theory with empirical corrections and validate performance",
        entity_scope="Propeller-driven aircraft",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NASA Propeller Studies"
    ),
    DoctrineBlock(
        topic="Rotary Wing Aerodynamics: Momentum Theory and Blade Flapping",
        keywords=["Rotary Wing", "Momentum Theory", "Blade Flapping", "Helicopter", "Aerodynamics"],
        conclusion_template="Momentum theory and blade flapping explain lift generation and control in rotary wing aircraft, enabling stable hover and maneuvering.",
        reasoning_framework=(
            "Momentum theory models the helicopter rotor as an actuator disk, relating lift to induced velocity and power. "
            "Blade flapping compensates for dissymmetry of lift between advancing and retreating blades, maintaining stability and control. "
            "Designers optimize rotor geometry and control systems to manage induced drag, power requirements, and vibration. "
            "Empirical and theoretical models guide design and operational procedures."
        ),
        key_factors=["Rotor geometry", "Induced velocity", "Blade flapping", "Control systems", "Power requirements"],
        primary_authority=["Leishman's Principles of Helicopter Aerodynamics", "NASA Rotary Wing Studies"],
        burden_holder="Manufacturer claiming stable hover",
        adversary_position="Momentum theory is too idealized; real-world effects dominate",
        counter_arguments=[
            "Blade flapping addresses real-world dissymmetry",
            "Empirical data supports theory",
            "Designs combine theory and empirical corrections"
        ],
        resolution_strategy="Validate theory with flight tests and operational data",
        entity_scope="Helicopters and rotary wing aircraft",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Leishman's Principles of Helicopter Aerodynamics"
    ),
    DoctrineBlock(
        topic="Wind Tunnel Testing: Scaling, Reynolds Number Effects",
        keywords=["Wind Tunnel", "Testing", "Scaling", "Reynolds Number", "Aerodynamics"],
        conclusion_template="Wind tunnel testing requires careful scaling and Reynolds number matching to ensure valid aerodynamic data for full-scale aircraft.",
        reasoning_framework=(
            "Wind tunnel models are typically smaller than full-scale aircraft, requiring scaling of geometric and flow parameters. "
            "Reynolds number matching is critical, as aerodynamic phenomena (e.g., boundary layer transition, separation) depend on flow regime. "
            "Corrections for wall effects, turbulence, and compressibility are applied to ensure data validity. "
            "Designers use wind tunnel data to validate computational models and optimize configurations."
        ),
        key_factors=["Model scale", "Reynolds number", "Wall effects", "Turbulence", "Compressibility"],
        primary_authority=["NASA Wind Tunnel Studies", "Raymer's Aircraft Design"],
        burden_holder="Designer claiming wind tunnel validation",
        adversary_position="Wind tunnel data is unreliable for full-scale aircraft",
        counter_arguments=[
            "Scaling laws and corrections are well established",
            "Reynolds number matching is achievable",
            "Wind tunnel data is widely used in design"
        ],
        resolution_strategy="Apply scaling corrections and validate with flight data",
        entity_scope="All aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NASA Wind Tunnel Studies"
    ),
    DoctrineBlock(
        topic="Ground Effect: Reduced Induced Drag, Increased Lift",
        keywords=["Ground Effect", "Induced Drag", "Lift", "Aerodynamics"],
        conclusion_template="Ground effect reduces induced drag and increases lift near the surface, improving takeoff and landing performance.",
        reasoning_framework=(
            "When an aircraft operates close to the ground, the formation of wingtip vortices is inhibited, reducing induced drag and increasing lift. "
            "Ground effect is most pronounced within one wingspan of the surface. "
            "Pilots experience reduced power requirements and altered handling during takeoff and landing. "
            "Designers account for ground effect in performance calculations and operational procedures."
        ),
        key_factors=["Altitude", "Wingspan", "Induced drag", "Lift coefficient", "Surface proximity"],
        primary_authority=["Raymer's Aircraft Design", "NASA Ground Effect Studies"],
        burden_holder="Operator claiming improved performance",
        adversary_position="Ground effect is negligible",
        counter_arguments=[
            "Empirical data shows significant drag reduction",
            "Lift increase is observed in flight tests",
            "Operational procedures account for ground effect"
        ],
        resolution_strategy="Quantify ground effect using flight and wind tunnel data",
        entity_scope="All aircraft",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Raymer's Aircraft Design"
    ),
    DoctrineBlock(
        topic="Atmospheric Effects: Density Altitude, Wind Shear, Icing",
        keywords=["Atmospheric Effects", "Density Altitude", "Wind Shear", "Icing", "Aerodynamics"],
        conclusion_template="Atmospheric effects—density altitude, wind shear, and icing—impact aircraft performance, safety, and operational planning.",
        reasoning_framework=(
            "Density altitude affects engine power, lift, and climb rate; higher altitude reduces performance. "
            "Wind shear causes abrupt changes in velocity and direction, posing hazards during takeoff and landing. "
            "Icing alters airfoil shape, increases drag, and reduces lift, potentially leading to stall. "
            "Pilots and operators must monitor atmospheric conditions, employ de-icing systems, and adjust operational procedures to mitigate risks."
        ),
        key_factors=["Altitude", "Temperature", "Humidity", "Wind shear", "Icing conditions"],
        primary_authority=["FAA Regulations", "NASA Atmospheric Studies"],
        burden_holder="Operator ensuring safe operation",
        adversary_position="Atmospheric effects are minor; standard procedures suffice",
        counter_arguments=[
            "Performance degradation is well documented",
            "Safety incidents highlight atmospheric hazards",
            "Regulations require mitigation measures"
        ],
        resolution_strategy="Integrate atmospheric monitoring and mitigation into operational planning",
        entity_scope="All aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    # Additional doctrine blocks for coverage (20+ more for 40+ total)
    DoctrineBlock(
        topic="Airfoil Camber and Lift Coefficient",
        keywords=["Airfoil", "Camber", "Lift Coefficient", "Aerodynamics"],
        conclusion_template="Increasing airfoil camber increases lift coefficient at a given angle of attack, but may affect stall and drag characteristics.",
        reasoning_framework=(
            "Airfoil camber is the curvature of the mean line. Higher camber increases lift for a given angle of attack, shifting the zero-lift angle. "
            "However, excessive camber can lead to early stall and increased drag. "
            "Designers balance camber to optimize lift, drag, and stall behavior for mission requirements."
        ),
        key_factors=["Camber", "Angle of attack", "Stall", "Drag", "Mission profile"],
        primary_authority=["Abbott & von Doenhoff", "NASA Airfoil Studies"],
        burden_holder="Designer proposing cambered airfoil",
        adversary_position="Camber increases drag and is undesirable",
        counter_arguments=[
            "Camber improves lift at low speeds",
            "Drag penalty is manageable",
            "Stall behavior can be controlled"
        ],
        resolution_strategy="Validate camber effects with wind tunnel and flight data",
        entity_scope="Fixed-wing aircraft",
        confidence=0.93,
        confidence_zone="Medium-High",
        controlling_precedent="Abbott & von Doenhoff"
    ),
    DoctrineBlock(
        topic="Laminar Flow Airfoil Design",
        keywords=["Laminar Flow", "Airfoil", "Design", "Aerodynamics"],
        conclusion_template="Laminar flow airfoils delay boundary layer transition, reducing drag and improving efficiency at moderate Reynolds numbers.",
        reasoning_framework=(
            "Laminar flow airfoils feature smooth contours and favorable pressure gradients to maintain laminar boundary layer over a large portion of the chord. "
            "Drag is reduced compared to conventional airfoils, but laminar flow is sensitive to surface contamination and manufacturing tolerances. "
            "Designers employ laminar flow airfoils for high-efficiency applications, balancing performance gains against operational challenges."
        ),
        key_factors=["Surface smoothness", "Pressure gradient", "Reynolds number", "Contamination", "Manufacturing tolerance"],
        primary_authority=["NASA Laminar Flow Studies", "Abbott & von Doenhoff"],
        burden_holder="Designer claiming laminar flow benefits",
        adversary_position="Laminar flow is impractical in real-world conditions",
        counter_arguments=[
            "Laminar flow is achievable with careful design",
            "Performance gains are documented",
            "Hybrid designs combine laminar and turbulent flow"
        ],
        resolution_strategy="Validate laminar flow with wind tunnel and operational data",
        entity_scope="Fixed-wing aircraft",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="NASA Laminar Flow Studies"
    ),
    DoctrineBlock(
        topic="Winglets: Reduction of Induced Drag",
        keywords=["Winglets", "Induced Drag", "Aerodynamics", "Efficiency"],
        conclusion_template="Winglets reduce induced drag by modifying wingtip vortex structure, improving fuel efficiency and climb performance.",
        reasoning_framework=(
            "Winglets are vertical or angled surfaces at wingtips that alter vortex formation, reducing induced drag. "
            "They increase effective aspect ratio without increasing span, improving lift-to-drag ratio. "
            "Empirical data shows fuel savings and improved climb rates. "
            "Designers optimize winglet geometry for specific aircraft and mission profiles."
        ),
        key_factors=["Winglet geometry", "Aspect ratio", "Vortex structure", "Fuel efficiency", "Climb performance"],
        primary_authority=["NASA Winglet Studies", "Raymer's Aircraft Design"],
        burden_holder="Manufacturer claiming winglet benefits",
        adversary_position="Winglets add weight and complexity",
        counter_arguments=[
            "Performance gains outweigh penalties",
            "Winglets are standard on modern aircraft",
            "Operational data confirms benefits"
        ],
        resolution_strategy="Quantify winglet effects with flight and wind tunnel data",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NASA Winglet Studies"
    ),
    DoctrineBlock(
        topic="Control Surface Effectiveness: Ailerons, Elevators, Rudders",
        keywords=["Control Surface", "Ailerons", "Elevators", "Rudders", "Effectiveness"],
        conclusion_template="Control surface effectiveness is determined by surface area, hinge moment, and aerodynamic balance, affecting maneuverability and stability.",
        reasoning_framework=(
            "Ailerons, elevators, and rudders provide roll, pitch, and yaw control. Effectiveness depends on surface area, deflection angle, and aerodynamic balance. "
            "Hinge moments must be manageable for pilot or actuator force. "
            "Designers optimize control surfaces for responsiveness, stability, and safety, using aerodynamic balancing and mass balancing techniques."
        ),
        key_factors=["Surface area", "Deflection angle", "Hinge moment", "Aerodynamic balance", "Actuation"],
        primary_authority=["Raymer's Aircraft Design", "NASA Control Surface Studies"],
        burden_holder="Designer claiming control effectiveness",
        adversary_position="Control surfaces are limited by aerodynamic forces",
        counter_arguments=[
            "Balancing techniques improve effectiveness",
            "Empirical data supports design optimization",
            "Flight testing confirms control authority"
        ],
        resolution_strategy="Validate effectiveness with wind tunnel and flight tests",
        entity_scope="All aircraft",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Raymer's Aircraft Design"
    ),
    DoctrineBlock(
        topic="Aircraft Stability and Control: Dutch Roll, Phugoid, Spiral Modes",
        keywords=["Stability", "Control", "Dutch Roll", "Phugoid", "Spiral Mode"],
        conclusion_template="Aircraft stability and control are characterized by dynamic modes—Dutch roll, phugoid, and spiral—each requiring specific damping and control strategies.",
        reasoning_framework=(
            "Dutch roll is a coupled yaw and roll oscillation, damped by yaw damper systems. "
            "Phugoid mode is a long-period oscillation in pitch and speed, managed by aerodynamic and control surface design. "
            "Spiral mode is a slow divergence in bank angle, requiring pilot or autopilot intervention. "
            "Designers analyze and damp these modes for safe operation."
        ),
        key_factors=["Dynamic modes", "Damping", "Control surfaces", "Autopilot", "Aerodynamic design"],
        primary_authority=["NASA Stability Studies", "Raymer's Aircraft Design"],
        burden_holder="Manufacturer ensuring stability",
        adversary_position="Dynamic modes are uncontrollable",
        counter_arguments=[
            "Damping systems are effective",
            "Design optimization reduces mode severity",
            "Operational procedures manage modes"
        ],
        resolution_strategy="Analyze modes and validate with flight data",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NASA Stability Studies"
    ),
    DoctrineBlock(
        topic="Aircraft Weight and Balance: Center of Gravity Limits",
        keywords=["Weight", "Balance", "Center of Gravity", "Limits", "Safety"],
        conclusion_template="Aircraft weight and balance must be maintained within center of gravity limits for safe operation and stability.",
        reasoning_framework=(
            "Center of gravity (CG) location affects stability, control, and structural loading. "
            "Regulatory authorities specify CG limits for each aircraft. "
            "Operators must calculate weight and balance before flight, adjusting loading as necessary. "
            "Exceeding CG limits can lead to instability, control loss, or structural failure."
        ),
        key_factors=["CG location", "Weight distribution", "Loading", "Regulatory limits", "Stability"],
        primary_authority=["FAA Regulations", "Raymer's Aircraft Design"],
        burden_holder="Operator ensuring safe loading",
        adversary_position="CG limits are arbitrary",
        counter_arguments=[
            "CG limits are based on stability and structural analysis",
            "Safety incidents highlight importance",
            "Regulations require compliance"
        ],
        resolution_strategy="Document and monitor CG during operations",
        entity_scope="All aircraft",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Structural Design: Load Factors and Fatigue",
        keywords=["Structural Design", "Load Factor", "Fatigue", "Safety"],
        conclusion_template="Aircraft structural design must account for load factors and fatigue, ensuring safety and longevity under operational stresses.",
        reasoning_framework=(
            "Load factors (g-forces) during maneuvers and turbulence impose stresses on aircraft structure. "
            "Fatigue accumulates over repeated load cycles, leading to crack initiation and growth. "
            "Designers use safety margins, material selection, and inspection protocols to manage load and fatigue. "
            "Regulations specify load factor limits and fatigue life requirements."
        ),
        key_factors=["Load factor", "Material properties", "Fatigue life", "Safety margin", "Inspection"],
        primary_authority=["FAA Regulations", "NASA Structural Studies"],
        burden_holder="Manufacturer ensuring structural integrity",
        adversary_position="Fatigue is unpredictable; design is insufficient",
        counter_arguments=[
            "Fatigue analysis is well established",
            "Safety margins are conservative",
            "Inspection protocols detect early signs"
        ],
        resolution_strategy="Combine design analysis with operational monitoring",
        entity_scope="All aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Certification: Airworthiness Standards",
        keywords=["Certification", "Airworthiness", "Standards", "Regulations"],
        conclusion_template="Aircraft certification requires compliance with airworthiness standards, ensuring safety, performance, and reliability.",
        reasoning_framework=(
            "Airworthiness standards (e.g., FAR Part 23/25) specify requirements for structure, systems, performance, and safety. "
            "Manufacturers must demonstrate compliance through testing, analysis, and documentation. "
            "Certification authorities review submissions and conduct inspections. "
            "Non-compliance results in certification denial or operational restrictions."
        ),
        key_factors=["Regulatory standards", "Testing", "Analysis", "Documentation", "Inspection"],
        primary_authority=["FAA Regulations", "EASA Standards"],
        burden_holder="Manufacturer seeking certification",
        adversary_position="Certification is bureaucratic and unnecessary",
        counter_arguments=[
            "Standards ensure safety and reliability",
            "Certification is required for operation",
            "Incidents highlight importance"
        ],
        resolution_strategy="Document compliance and engage with authorities",
        entity_scope="All aircraft",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Noise: Mitigation Strategies",
        keywords=["Noise", "Mitigation", "Aerodynamics", "Regulations"],
        conclusion_template="Aircraft noise is mitigated through aerodynamic design, engine technology, and operational procedures, complying with regulatory limits.",
        reasoning_framework=(
            "Noise sources include engine, propeller, and aerodynamic interactions. "
            "Designers employ quiet engines, optimized propeller geometry, and noise-reducing airfoil shapes. "
            "Operational procedures (e.g., climb profiles) further reduce noise exposure. "
            "Regulations specify noise limits for certification and operation."
        ),
        key_factors=["Noise source", "Engine technology", "Propeller design", "Operational procedures", "Regulatory limits"],
        primary_authority=["FAA Regulations", "NASA Noise Studies"],
        burden_holder="Manufacturer ensuring noise compliance",
        adversary_position="Noise mitigation is ineffective",
        counter_arguments=[
            "Design and operational strategies are effective",
            "Regulations require compliance",
            "Community concerns drive innovation"
        ],
        resolution_strategy="Combine design and operational measures, validate with testing",
        entity_scope="All aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Fuel Systems: Safety and Reliability",
        keywords=["Fuel Systems", "Safety", "Reliability", "Design"],
        conclusion_template="Aircraft fuel systems are designed for safety and reliability, incorporating redundancy, monitoring, and fail-safe mechanisms.",
        reasoning_framework=(
            "Fuel system design includes multiple tanks, pumps, and valves to ensure continuous supply. "
            "Monitoring systems detect leaks, contamination, and failures. "
            "Redundancy and fail-safe design minimize risk of fuel starvation or fire. "
            "Regulations specify safety and reliability requirements."
        ),
        key_factors=["Redundancy", "Monitoring", "Fail-safe design", "Regulatory requirements", "Maintenance"],
        primary_authority=["FAA Regulations", "NASA Fuel System Studies"],
        burden_holder="Manufacturer ensuring fuel system safety",
        adversary_position="Fuel systems are prone to failure",
        counter_arguments=[
            "Redundancy reduces risk",
            "Monitoring detects issues early",
            "Design meets regulatory standards"
        ],
        resolution_strategy="Validate design with testing and operational data",
        entity_scope="All aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft De-Icing and Anti-Icing Systems",
        keywords=["De-Icing", "Anti-Icing", "Systems", "Safety"],
        conclusion_template="De-icing and anti-icing systems prevent hazardous ice accumulation, ensuring safe operation in adverse weather.",
        reasoning_framework=(
            "Ice accumulation alters airfoil shape, increases drag, and reduces lift. "
            "De-icing systems (e.g., pneumatic boots, electric heaters) remove ice after formation. "
            "Anti-icing systems (e.g., heated surfaces, fluid application) prevent ice formation. "
            "Regulations require de-icing/anti-icing capability for certification."
        ),
        key_factors=["Ice accumulation", "System type", "Operational procedures", "Regulatory requirements", "Maintenance"],
        primary_authority=["FAA Regulations", "NASA Icing Studies"],
        burden_holder="Operator ensuring safe operation in icing conditions",
        adversary_position="De-icing systems are unreliable",
        counter_arguments=[
            "Systems are validated by testing",
            "Operational procedures ensure effectiveness",
            "Regulations require capability"
        ],
        resolution_strategy="Combine system design with operational training",
        entity_scope="All aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Avionics: Flight Management and Navigation",
        keywords=["Avionics", "Flight Management", "Navigation", "Systems"],
        conclusion_template="Modern avionics provide integrated flight management and navigation, enhancing safety, efficiency, and situational awareness.",
        reasoning_framework=(
            "Avionics systems include flight management computers, GPS, inertial navigation, and autopilot. "
            "Integration enables precise route planning, fuel management, and real-time monitoring. "
            "Safety is enhanced through redundancy and error-checking. "
            "Regulations specify avionics requirements for certification."
        ),
        key_factors=["System integration", "Redundancy", "Navigation accuracy", "Safety", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Avionics Studies"],
        burden_holder="Manufacturer ensuring avionics capability",
        adversary_position="Avionics are prone to failure",
        counter_arguments=[
            "Redundancy and error-checking reduce risk",
            "Operational data confirms reliability",
            "Regulations require capability"
        ],
        resolution_strategy="Validate systems with operational testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Environmental Control: Cabin Pressurization and Ventilation",
        keywords=["Environmental Control", "Cabin Pressurization", "Ventilation", "Safety"],
        conclusion_template="Cabin pressurization and ventilation systems maintain safe and comfortable conditions, complying with regulatory standards.",
        reasoning_framework=(
            "Pressurization systems maintain cabin pressure at safe levels during high-altitude flight. "
            "Ventilation ensures air quality and temperature control. "
            "Redundancy and monitoring systems detect and mitigate failures. "
            "Regulations specify environmental control requirements for certification."
        ),
        key_factors=["Pressurization", "Ventilation", "Monitoring", "Redundancy", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Environmental Studies"],
        burden_holder="Manufacturer ensuring environmental control",
        adversary_position="Systems are prone to failure",
        counter_arguments=[
            "Redundancy and monitoring reduce risk",
            "Operational data confirms reliability",
            "Regulations require capability"
        ],
        resolution_strategy="Validate systems with operational testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Emergency Procedures: Training and Compliance",
        keywords=["Emergency Procedures", "Training", "Compliance", "Safety"],
        conclusion_template="Emergency procedures and training ensure crew and passenger safety, complying with regulatory requirements.",
        reasoning_framework=(
            "Emergency procedures cover fire, evacuation, system failure, and medical emergencies. "
            "Training ensures crew proficiency and compliance with regulations. "
            "Documentation and drills validate preparedness. "
            "Regulations require emergency procedure documentation and training."
        ),
        key_factors=["Procedure documentation", "Training", "Compliance", "Regulatory requirements", "Preparedness"],
        primary_authority=["FAA Regulations", "NASA Safety Studies"],
        burden_holder="Operator ensuring safety",
        adversary_position="Training is insufficient",
        counter_arguments=[
            "Training and drills improve preparedness",
            "Regulations require compliance",
            "Operational data confirms effectiveness"
        ],
        resolution_strategy="Combine training, documentation, and drills",
        entity_scope="All aircraft",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Maintenance: Inspection and Reliability",
        keywords=["Maintenance", "Inspection", "Reliability", "Safety"],
        conclusion_template="Regular maintenance and inspection ensure aircraft reliability and safety, complying with regulatory requirements.",
        reasoning_framework=(
            "Maintenance schedules specify inspection intervals for structure, systems, and engines. "
            "Reliability is enhanced through preventive maintenance and replacement of worn components. "
            "Regulations require documentation and compliance. "
            "Operational data confirms reliability improvements."
        ),
        key_factors=["Inspection interval", "Preventive maintenance", "Reliability", "Regulatory requirements", "Documentation"],
        primary_authority=["FAA Regulations", "NASA Maintenance Studies"],
        burden_holder="Operator ensuring reliability",
        adversary_position="Maintenance is ineffective",
        counter_arguments=[
            "Preventive maintenance reduces failures",
            "Regulations require compliance",
            "Operational data confirms reliability"
        ],
        resolution_strategy="Combine maintenance schedules with operational monitoring",
        entity_scope="All aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Human Factors: Ergonomics and Crew Resource Management",
        keywords=["Human Factors", "Ergonomics", "Crew Resource Management", "Safety"],
        conclusion_template="Human factors engineering and crew resource management enhance safety, efficiency, and operational effectiveness.",
        reasoning_framework=(
            "Ergonomic cockpit design reduces workload and improves situational awareness. "
            "Crew resource management (CRM) fosters communication, teamwork, and decision-making. "
            "Training and operational procedures integrate human factors principles. "
            "Regulations specify human factors requirements for certification."
        ),
        key_factors=["Ergonomics", "CRM", "Training", "Operational procedures", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Human Factors Studies"],
        burden_holder="Operator ensuring safety",
        adversary_position="Human factors are secondary to technical design",
        counter_arguments=[
            "Human factors incidents highlight importance",
            "CRM improves operational effectiveness",
            "Regulations require compliance"
        ],
        resolution_strategy="Integrate human factors into design and training",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Fire Protection: Detection and Suppression",
        keywords=["Fire Protection", "Detection", "Suppression", "Safety"],
        conclusion_template="Fire detection and suppression systems are essential for safety, complying with regulatory requirements.",
        reasoning_framework=(
            "Fire detection systems monitor engines, cabins, and cargo for heat and smoke. "
            "Suppression systems (e.g., extinguishers, inert gas) mitigate fire risk. "
            "Redundancy and monitoring ensure reliability. "
            "Regulations specify fire protection requirements for certification."
        ),
        key_factors=["Detection", "Suppression", "Redundancy", "Monitoring", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Fire Protection Studies"],
        burden_holder="Manufacturer ensuring fire protection",
        adversary_position="Systems are unreliable",
        counter_arguments=[
            "Redundancy and monitoring reduce risk",
            "Operational data confirms effectiveness",
            "Regulations require capability"
        ],
        resolution_strategy="Validate systems with operational testing",
        entity_scope="All aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Electrical Systems: Redundancy and Safety",
        keywords=["Electrical Systems", "Redundancy", "Safety", "Reliability"],
        conclusion_template="Aircraft electrical systems incorporate redundancy and safety features, ensuring reliability and compliance with regulations.",
        reasoning_framework=(
            "Electrical systems include multiple generators, batteries, and distribution networks. "
            "Redundancy ensures continued operation during failures. "
            "Safety features (e.g., circuit breakers, monitoring) mitigate risk. "
            "Regulations specify electrical system requirements for certification."
        ),
        key_factors=["Redundancy", "Safety features", "Monitoring", "Regulatory requirements", "Reliability"],
        primary_authority=["FAA Regulations", "NASA Electrical Studies"],
        burden_holder="Manufacturer ensuring electrical system reliability",
        adversary_position="Systems are prone to failure",
        counter_arguments=[
            "Redundancy reduces risk",
            "Safety features mitigate failures",
            "Regulations require capability"
        ],
        resolution_strategy="Validate systems with operational testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Landing Gear: Design and Reliability",
        keywords=["Landing Gear", "Design", "Reliability", "Safety"],
        conclusion_template="Landing gear design prioritizes reliability, strength, and safety, complying with regulatory requirements.",
        reasoning_framework=(
            "Landing gear must withstand landing loads, provide stability, and enable safe ground operations. "
            "Design includes redundancy, shock absorption, and monitoring systems. "
            "Regulations specify strength and reliability requirements for certification."
        ),
        key_factors=["Strength", "Redundancy", "Shock absorption", "Monitoring", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Landing Gear Studies"],
        burden_holder="Manufacturer ensuring landing gear reliability",
        adversary_position="Landing gear is prone to failure",
        counter_arguments=[
            "Design and testing ensure reliability",
            "Redundancy reduces risk",
            "Regulations require capability"
        ],
        resolution_strategy="Validate design with testing and operational data",
        entity_scope="All aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Hydraulics: System Design and Safety",
        keywords=["Hydraulics", "System Design", "Safety", "Reliability"],
        conclusion_template="Hydraulic systems are designed for reliability and safety, incorporating redundancy and monitoring, complying with regulatory requirements.",
        reasoning_framework=(
            "Hydraulic systems power control surfaces, landing gear, and brakes. "
            "Redundancy and monitoring ensure continued operation during failures. "
            "Safety features (e.g., pressure relief, leak detection) mitigate risk. "
            "Regulations specify hydraulic system requirements for certification."
        ),
        key_factors=["Redundancy", "Monitoring", "Safety features", "Regulatory requirements", "Reliability"],
        primary_authority=["FAA Regulations", "NASA Hydraulics Studies"],
        burden_holder="Manufacturer ensuring hydraulic system reliability",
        adversary_position="Systems are prone to failure",
        counter_arguments=[
            "Redundancy reduces risk",
            "Safety features mitigate failures",
            "Regulations require capability"
        ],
        resolution_strategy="Validate systems with operational testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Flight Data Monitoring: Safety and Compliance",
        keywords=["Flight Data Monitoring", "Safety", "Compliance", "Regulations"],
        conclusion_template="Flight data monitoring enhances safety and compliance, enabling incident analysis and operational improvement.",
        reasoning_framework=(
            "Flight data monitoring (FDM) records operational parameters for analysis and safety improvement. "
            "Data is used for incident investigation, trend analysis, and regulatory compliance. "
            "Regulations require FDM capability for certification and operation."
        ),
        key_factors=["Data recording", "Analysis", "Safety", "Regulatory requirements", "Operational improvement"],
        primary_authority=["FAA Regulations", "NASA FDM Studies"],
        burden_holder="Operator ensuring safety and compliance",
        adversary_position="FDM is intrusive and unnecessary",
        counter_arguments=[
            "FDM improves safety and operational effectiveness",
            "Regulations require capability",
            "Incidents highlight importance"
        ],
        resolution_strategy="Integrate FDM into operations and analyze data",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Fuel Efficiency: Aerodynamic and Engine Optimization",
        keywords=["Fuel Efficiency", "Aerodynamics", "Engine Optimization", "Performance"],
        conclusion_template="Fuel efficiency is maximized through aerodynamic optimization and advanced engine technology, reducing operational costs and environmental impact.",
        reasoning_framework=(
            "Aerodynamic optimization reduces drag and improves lift-to-drag ratio. "
            "Engine technology advances (e.g., high bypass turbofans, FADEC) improve fuel consumption. "
            "Designers balance aerodynamic and engine improvements for maximum efficiency. "
            "Regulations and environmental concerns drive innovation."
        ),
        key_factors=["Aerodynamic design", "Engine technology", "Fuel consumption", "Regulatory requirements", "Environmental impact"],
        primary_authority=["NASA Fuel Efficiency Studies", "Raymer's Aircraft Design"],
        burden_holder="Manufacturer claiming fuel efficiency",
        adversary_position="Efficiency gains are marginal",
        counter_arguments=[
            "Operational data confirms significant gains",
            "Design and technology advances are effective",
            "Regulations require improvements"
        ],
        resolution_strategy="Combine aerodynamic and engine optimization, validate with operational data",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NASA Fuel Efficiency Studies"
    ),
    DoctrineBlock(
        topic="Aircraft Aerodynamic Optimization: CFD and Wind Tunnel Validation",
        keywords=["Aerodynamic Optimization", "CFD", "Wind Tunnel", "Validation"],
        conclusion_template="Aerodynamic optimization uses CFD and wind tunnel validation to improve performance, reduce drag, and ensure safety.",
        reasoning_framework=(
            "Computational Fluid Dynamics (CFD) enables detailed analysis of flow, drag, and lift. "
            "Wind tunnel validation confirms CFD predictions and identifies real-world effects. "
            "Designers iterate between CFD and wind tunnel testing for optimal configuration. "
            "Regulations require validation for certification."
        ),
        key_factors=["CFD analysis", "Wind tunnel testing", "Drag reduction", "Lift optimization", "Regulatory requirements"],
        primary_authority=["NASA CFD Studies", "Raymer's Aircraft Design"],
        burden_holder="Designer claiming aerodynamic optimization",
        adversary_position="CFD is unreliable; wind tunnel is insufficient",
        counter_arguments=[
            "Combined approach improves accuracy",
            "Operational data confirms effectiveness",
            "Regulations require validation"
        ],
        resolution_strategy="Integrate CFD and wind tunnel testing, validate with flight data",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NASA CFD Studies"
    ),
    DoctrineBlock(
        topic="Aircraft Environmental Impact: Emissions and Noise",
        keywords=["Environmental Impact", "Emissions", "Noise", "Regulations"],
        conclusion_template="Aircraft environmental impact is managed through emissions reduction and noise mitigation, complying with regulatory and community standards.",
        reasoning_framework=(
            "Emissions reduction is achieved through engine technology, fuel optimization, and operational procedures. "
            "Noise mitigation uses aerodynamic design and operational profiles. "
            "Regulations specify limits for certification and operation. "
            "Community concerns drive ongoing innovation."
        ),
        key_factors=["Emissions", "Noise", "Engine technology", "Operational procedures", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Environmental Studies"],
        burden_holder="Manufacturer ensuring environmental compliance",
        adversary_position="Impact is unavoidable",
        counter_arguments=[
            "Technological advances reduce impact",
            "Regulations require compliance",
            "Community concerns drive innovation"
        ],
        resolution_strategy="Combine technology and operational measures, validate with testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Flight Envelope Protection: Systems and Safety",
        keywords=["Flight Envelope Protection", "Systems", "Safety", "Regulations"],
        conclusion_template="Flight envelope protection systems prevent unsafe operation, enhancing safety and complying with regulatory requirements.",
        reasoning_framework=(
            "Flight envelope protection monitors speed, altitude, and attitude, preventing exceedance of safe limits. "
            "Systems intervene to prevent stalls, overspeed, or structural overload. "
            "Regulations specify requirements for certification. "
            "Operational data confirms safety improvements."
        ),
        key_factors=["Monitoring", "Intervention", "Safety", "Regulatory requirements", "Operational data"],
        primary_authority=["FAA Regulations", "NASA Flight Envelope Studies"],
        burden_holder="Manufacturer ensuring safety",
        adversary_position="Systems are intrusive and unreliable",
        counter_arguments=[
            "Systems prevent accidents",
            "Operational data confirms effectiveness",
            "Regulations require capability"
        ],
        resolution_strategy="Validate systems with operational testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Takeoff and Landing Performance: Runway Requirements",
        keywords=["Takeoff", "Landing", "Performance", "Runway", "Safety"],
        conclusion_template="Takeoff and landing performance determines runway requirements, ensuring safe operation and compliance with regulations.",
        reasoning_framework=(
            "Performance calculations include weight, speed, atmospheric conditions, and runway length. "
            "Regulations specify minimum runway requirements for certification and operation. "
            "Operational data confirms safety and compliance."
        ),
        key_factors=["Weight", "Speed", "Atmospheric conditions", "Runway length", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Performance Studies"],
        burden_holder="Operator ensuring safe operation",
        adversary_position="Runway requirements are arbitrary",
        counter_arguments=[
            "Performance calculations are validated",
            "Regulations require compliance",
            "Operational data confirms safety"
        ],
        resolution_strategy="Combine calculations with operational monitoring",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Flight Planning: Weather and Airspace Management",
        keywords=["Flight Planning", "Weather", "Airspace Management", "Safety"],
        conclusion_template="Flight planning integrates weather and airspace management, ensuring safety, efficiency, and regulatory compliance.",
        reasoning_framework=(
            "Weather analysis informs route selection, fuel planning, and alternate airports. "
            "Airspace management ensures compliance with regulations and avoids conflicts. "
            "Operational data confirms safety and efficiency improvements."
        ),
        key_factors=["Weather", "Route selection", "Fuel planning", "Airspace management", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Flight Planning Studies"],
        burden_holder="Operator ensuring safe and efficient operation",
        adversary_position="Planning is unnecessary; pilot judgment suffices",
        counter_arguments=[
            "Planning improves safety and efficiency",
            "Regulations require compliance",
            "Operational data confirms effectiveness"
        ],
        resolution_strategy="Integrate planning with operational monitoring",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
    DoctrineBlock(
        topic="Aircraft Engine Performance: Thrust and Efficiency",
        keywords=["Engine Performance", "Thrust", "Efficiency", "Aerodynamics"],
        conclusion_template="Engine performance is characterized by thrust and efficiency, optimized through aerodynamic and technological advances.",
        reasoning_framework=(
            "Thrust is generated by jet or propeller engines, dependent on aerodynamic and technological factors. "
            "Efficiency is improved through high bypass ratios, advanced materials, and FADEC systems. "
            "Designers balance thrust and efficiency for mission requirements. "
            "Regulations specify performance requirements for certification."
        ),
        key_factors=["Thrust", "Efficiency", "Aerodynamic design", "Technology", "Regulatory requirements"],
        primary_authority=["NASA Engine Studies", "Raymer's Aircraft Design"],
        burden_holder="Manufacturer claiming engine performance",
        adversary_position="Performance gains are marginal",
        counter_arguments=[
            "Technological advances improve performance",
            "Operational data confirms gains",
            "Regulations require capability"
        ],
        resolution_strategy="Validate performance with operational testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NASA Engine Studies"
    ),
    DoctrineBlock(
        topic="Aircraft Engine Control: FADEC and Manual Systems",
        keywords=["Engine Control", "FADEC", "Manual Systems", "Safety"],
        conclusion_template="Engine control systems, including FADEC and manual controls, optimize performance and safety, complying with regulatory requirements.",
        reasoning_framework=(
            "FADEC (Full Authority Digital Engine Control) automates engine management, optimizing performance and reducing pilot workload. "
            "Manual systems provide backup and flexibility. "
            "Regulations specify requirements for certification and operation. "
            "Operational data confirms safety and efficiency improvements."
        ),
        key_factors=["FADEC", "Manual control", "Performance", "Safety", "Regulatory requirements"],
        primary_authority=["FAA Regulations", "NASA Engine Control Studies"],
        burden_holder="Manufacturer ensuring engine control reliability",
        adversary_position="FADEC is unreliable; manual control is preferable",
        counter_arguments=[
            "FADEC improves performance and safety",
            "Manual systems provide backup",
            "Regulations require capability"
        ],
        resolution_strategy="Validate systems with operational testing",
        entity_scope="Transport and general aviation aircraft",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FAA Regulations"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    matched = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            matched.append(doctrine)
    return matched

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]