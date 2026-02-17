from dataclasses import dataclass
from typing import List, Optional
import enum
import pathlib

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
        topic="Hydraulic Brake Circuit Design: Dual Diagonal Split",
        keywords=["hydraulic", "brake circuit", "dual diagonal", "safety", "redundancy", "fail-safe"],
        conclusion_template=(
            "The dual diagonal split hydraulic brake circuit design ensures that in the event of a failure "
            "in one circuit, braking force is maintained on diagonally opposite wheels, preserving vehicle "
            "stability and stopping capability."
        ),
        reasoning_framework=(
            "The hydraulic brake system is designed with two independent circuits arranged diagonally: one "
            "circuit controls the front left and rear right brakes, and the other controls the front right "
            "and rear left brakes. This configuration is critical because it maintains balanced braking "
            "forces even if one circuit fails, preventing the vehicle from pulling to one side during braking. "
            "The reasoning follows safety engineering principles prioritizing redundancy and fault tolerance. "
            "The system's effectiveness is evaluated through failure mode and effects analysis (FMEA), "
            "hydraulic pressure distribution tests, and compliance with FMVSS 135 standards. The design "
            "also considers hydraulic line routing to minimize risk of simultaneous damage to both circuits."
            "\n\n"
            "This approach aligns with industry best practices and regulatory requirements, ensuring that "
            "the vehicle maintains controllability and stopping power under partial system failure conditions."
            "The design is validated through rigorous testing including simulated circuit failures and "
            "dynamic braking performance assessments."
        ),
        key_factors=[
            "Circuit independence",
            "Diagonal wheel pairing",
            "Hydraulic pressure balance",
            "Fail-safe redundancy",
            "FMVSS 135 compliance",
            "Hydraulic line routing integrity"
        ],
        primary_authority=[
            "SAE J1703 Hydraulic Brake Systems",
            "FMVSS 135 Brake Systems",
            "Automotive Brake Engineering Texts",
            "NHTSA Brake System Guidelines"
        ],
        burden_holder="Vehicle Manufacturer",
        adversary_position=(
            "Some argue that simpler single-circuit or front/rear split systems reduce cost and complexity "
            "without significant safety trade-offs."
        ),
        counter_arguments=[
            "Single-circuit systems lack redundancy and risk total brake failure.",
            "Front/rear split systems can cause vehicle instability during partial failures.",
            "Dual diagonal split is mandated by regulatory safety standards."
        ],
        resolution_strategy=(
            "Demonstrate compliance with FMVSS 135 and safety test results proving superior stability and "
            "fail-safe operation of dual diagonal split design compared to alternatives."
        ),
        entity_scope="Passenger Vehicles, Light Trucks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.2 Dual Circuit Brake Systems"
    ),
    DoctrineBlock(
        topic="Disc Brake Caliper Piston and Pad Analysis",
        keywords=["disc brake", "caliper piston", "pad wear", "friction", "thermal expansion", "material compatibility"],
        conclusion_template=(
            "Optimizing disc brake caliper piston size and pad material selection enhances braking efficiency, "
            "wear uniformity, and thermal management."
        ),
        reasoning_framework=(
            "Disc brake caliper pistons convert hydraulic pressure into mechanical force pressing the brake pads "
            "against the rotor. The piston diameter influences the clamping force and pedal feel. Larger pistons "
            "increase force but may reduce pedal travel, while smaller pistons require higher pressure for the same "
            "clamping force.\n\n"
            "Pad material selection affects friction coefficient (mu), wear rate, and heat dissipation. Semi-metallic "
            "pads offer high friction and thermal capacity but can increase rotor wear and noise. Ceramic pads provide "
            "lower noise and dust but may have reduced friction at low temperatures.\n\n"
            "Thermal expansion of pistons and caliper components must be accounted for to prevent pad drag or excessive "
            "clearance. Material compatibility between piston seals and brake fluid is critical to prevent leaks and "
            "seal degradation.\n\n"
            "The analysis integrates mechanical design, tribology, and thermal dynamics to balance performance, durability, "
            "and NVH characteristics."
        ),
        key_factors=[
            "Piston diameter and number",
            "Pad friction coefficient",
            "Thermal conductivity",
            "Material wear rates",
            "Seal compatibility",
            "Caliper stiffness"
        ],
        primary_authority=[
            "SAE J2522 Brake Pad Friction Materials",
            "ISO 26867 Brake System Components",
            "Brake Engineering Handbooks",
            "Automotive Tribology Research"
        ],
        burden_holder="Brake System Designer",
        adversary_position=(
            "Some contend that maximizing piston size and using high-friction pads always yields better braking."
        ),
        counter_arguments=[
            "Oversized pistons can cause excessive pedal stiffness and reduced modulation.",
            "High-friction pads may increase rotor wear and noise.",
            "Thermal management and material compatibility are essential for system longevity."
        ],
        resolution_strategy=(
            "Use empirical testing and simulation to optimize piston size and pad materials for target vehicle use cases."
        ),
        entity_scope="Passenger Vehicles, Performance Cars",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2522 Section 4.3 Piston and Pad Design"
    ),
    DoctrineBlock(
        topic="Drum Brake Leading and Trailing Shoe Adjustment",
        keywords=["drum brake", "leading shoe", "trailing shoe", "self-energizing", "adjustment mechanism", "brake balance"],
        conclusion_template=(
            "Proper adjustment of leading and trailing shoes in drum brakes ensures balanced braking force and "
            "prevents premature wear or drag."
        ),
        reasoning_framework=(
            "Drum brakes use two shoes: a leading shoe which is self-energizing due to rotation direction and a trailing "
            "shoe which provides consistent but lower braking force. The leading shoe contacts the drum in a manner that "
            "increases friction force via the self-energizing effect, while the trailing shoe acts as a secondary brake.\n\n"
            "Adjustment mechanisms compensate for shoe wear to maintain optimal clearance and contact pressure. "
            "Improper adjustment can cause excessive drag, overheating, or reduced braking efficiency.\n\n"
            "The reasoning includes mechanical leverage analysis, frictional force distribution, and wear patterns. "
            "Adjustment methods include manual star wheel adjusters, automatic adjusters, or self-adjusting mechanisms.\n\n"
            "Balancing the force between shoes is critical to prevent vehicle pull and ensure even wear."
        ),
        key_factors=[
            "Shoe geometry",
            "Adjustment mechanism type",
            "Friction material condition",
            "Drum diameter wear",
            "Self-energizing effect magnitude"
        ],
        primary_authority=[
            "SAE J866 Drum Brake Systems",
            "FMVSS 135 Appendix C",
            "Brake System Maintenance Manuals",
            "Automotive Service Excellence (ASE) Guidelines"
        ],
        burden_holder="Service Technician / Maintenance Personnel",
        adversary_position=(
            "Some suggest that automatic adjusters are unnecessary and add complexity."
        ),
        counter_arguments=[
            "Manual adjustment is prone to error and inconsistent brake performance.",
            "Automatic adjusters improve safety and reduce maintenance frequency.",
            "Proper adjustment is critical for brake balance and vehicle stability."
        ],
        resolution_strategy=(
            "Recommend automatic adjusters for modern vehicles and enforce regular maintenance checks."
        ),
        entity_scope="Light Trucks, Passenger Vehicles with Drum Brakes",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="FMVSS 135 §7.4 Drum Brake Adjustment"
    ),
    DoctrineBlock(
        topic="ABS Anti-lock Braking System: Wheel Speed Sensors",
        keywords=["ABS", "anti-lock braking system", "wheel speed sensor", "electronic control", "sensor types", "signal processing"],
        conclusion_template=(
            "Wheel speed sensors provide critical real-time data to ABS controllers, enabling modulation of brake pressure "
            "to prevent wheel lockup."
        ),
        reasoning_framework=(
            "ABS systems rely on accurate measurement of wheel rotational speed to detect impending lockup conditions. "
            "Wheel speed sensors are typically magnetic or Hall-effect sensors mounted near the wheel hub or axle.\n\n"
            "The sensor generates pulses corresponding to wheel rotation, which are processed by the ABS electronic control "
            "unit (ECU) to calculate speed and acceleration. Signal integrity, sensor placement, and environmental robustness "
            "are essential for reliable operation.\n\n"
            "The reasoning framework includes electromagnetic theory for sensor operation, signal filtering techniques, "
            "and fault detection algorithms. Sensor failure modes such as dirt contamination, wiring faults, or magnetic interference "
            "are considered.\n\n"
            "The system must meet automotive EMC standards and operate reliably across temperature extremes and mechanical vibrations."
        ),
        key_factors=[
            "Sensor type (magnetic, Hall-effect)",
            "Signal noise filtering",
            "Mounting location",
            "Environmental sealing",
            "Redundancy and diagnostics"
        ],
        primary_authority=[
            "ISO 26262 Functional Safety",
            "SAE J2945/1 ABS System Requirements",
            "Automotive Sensor Engineering Texts",
            "FMVSS 126 Electronic Stability Control"
        ],
        burden_holder="ABS System Supplier",
        adversary_position=(
            "Some argue that simpler brake systems without ABS reduce cost and complexity."
        ),
        counter_arguments=[
            "ABS significantly improves vehicle control and reduces crash risk.",
            "Wheel speed sensors are proven technology with high reliability.",
            "Regulatory mandates require ABS on most passenger vehicles."
        ],
        resolution_strategy=(
            "Demonstrate compliance with safety standards and provide reliability data supporting ABS benefits."
        ),
        entity_scope="Passenger Vehicles, Light Trucks",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 126 §5 ABS Requirements"
    ),
    DoctrineBlock(
        topic="EBD Electronic Brakeforce Distribution",
        keywords=["EBD", "electronic brakeforce distribution", "brake balance", "load sensing", "dynamic adjustment"],
        conclusion_template=(
            "EBD systems dynamically adjust brakeforce distribution between axles to optimize stopping performance "
            "and vehicle stability under varying load conditions."
        ),
        reasoning_framework=(
            "Electronic Brakeforce Distribution (EBD) enhances traditional brake systems by adjusting the proportion of braking "
            "force applied to front and rear wheels based on real-time load and dynamic conditions.\n\n"
            "EBD uses sensors such as load cells, accelerometers, and wheel speed sensors to determine vehicle weight distribution, "
            "pitch, and road conditions. The ECU modulates hydraulic pressure or brake-by-wire actuators to optimize brakeforce, "
            "preventing rear wheel lockup and improving stability.\n\n"
            "The reasoning framework integrates vehicle dynamics, sensor fusion, and control theory to achieve optimal braking "
            "performance. EBD complements ABS by refining force distribution rather than preventing lockup alone.\n\n"
            "EBD systems are calibrated through extensive testing across load scenarios and comply with FMVSS 135 and 126."
        ),
        key_factors=[
            "Load sensing accuracy",
            "Brake pressure modulation",
            "Sensor fusion algorithms",
            "Vehicle dynamics modeling",
            "Fail-safe operation"
        ],
        primary_authority=[
            "SAE J2945/1 Brake System Performance",
            "FMVSS 135 Brake Systems",
            "Vehicle Dynamics and Control Texts",
            "Automotive Control Systems Standards"
        ],
        burden_holder="Brake System Designer",
        adversary_position=(
            "Some claim mechanical proportioning valves suffice and EBD adds unnecessary complexity."
        ),
        counter_arguments=[
            "Mechanical valves cannot adapt to dynamic load changes in real-time.",
            "EBD improves stopping distances and vehicle stability under varying conditions.",
            "EBD is increasingly mandated by safety regulations."
        ],
        resolution_strategy=(
            "Provide test data demonstrating improved performance and compliance with regulatory requirements."
        ),
        entity_scope="Passenger Vehicles, Light Commercial Vehicles",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.3 Brakeforce Distribution"
    ),
    DoctrineBlock(
        topic="ESC Electronic Stability Control: Yaw Rate and Lateral Acceleration",
        keywords=["ESC", "electronic stability control", "yaw rate", "lateral acceleration", "vehicle dynamics", "sensor fusion"],
        conclusion_template=(
            "ESC systems utilize yaw rate and lateral acceleration sensors to detect and mitigate vehicle instability "
            "through selective braking and engine torque control."
        ),
        reasoning_framework=(
            "Electronic Stability Control (ESC) enhances vehicle safety by monitoring yaw rate and lateral acceleration to "
            "detect understeer or oversteer conditions.\n\n"
            "Yaw rate sensors measure rotational velocity about the vertical axis, while lateral accelerometers detect side forces. "
            "The ESC ECU compares these inputs with driver steering input and vehicle speed to determine if the vehicle is deviating "
            "from the intended path.\n\n"
            "When instability is detected, ESC selectively applies braking force to individual wheels and modulates engine torque "
            "to restore stability. The system relies on real-time sensor fusion, control algorithms, and actuator responsiveness.\n\n"
            "The reasoning framework includes vehicle dynamics modeling, control theory, and fail-safe design to ensure timely and "
            "effective interventions without driver surprise."
        ),
        key_factors=[
            "Yaw rate sensor accuracy",
            "Lateral acceleration measurement",
            "Steering angle input",
            "Brake actuator response time",
            "Control algorithm robustness"
        ],
        primary_authority=[
            "FMVSS 126 Electronic Stability Control",
            "SAE J266 Electronic Stability Control Systems",
            "Vehicle Dynamics and Control Literature",
            "ISO 26262 Functional Safety"
        ],
        burden_holder="ESC System Supplier",
        adversary_position=(
            "Critics argue ESC systems may interfere with driver control and increase system complexity."
        ),
        counter_arguments=[
            "ESC significantly reduces loss-of-control crashes and fatalities.",
            "Systems are designed to intervene subtly and can be overridden by driver input.",
            "Regulatory bodies mandate ESC on new vehicles."
        ],
        resolution_strategy=(
            "Demonstrate compliance with FMVSS 126 and provide crash reduction statistics."
        ),
        entity_scope="Passenger Vehicles, SUVs",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 126 §6 ESC Requirements"
    ),
    DoctrineBlock(
        topic="Brake Fluid DOT Specifications and Boiling Point",
        keywords=["brake fluid", "DOT specifications", "boiling point", "wet boiling point", "hydraulic fluid", "thermal degradation"],
        conclusion_template=(
            "Brake fluids meeting DOT specifications with high dry and wet boiling points ensure reliable hydraulic braking "
            "performance under thermal stress."
        ),
        reasoning_framework=(
            "Brake fluid transmits hydraulic pressure from the master cylinder to brake calipers or wheel cylinders. It must "
            "maintain consistent viscosity and not vaporize under high temperatures generated during braking.\n\n"
            "DOT specifications (3, 4, 5.1) define minimum dry and wet boiling points, chemical composition, and compatibility. "
            "Dry boiling point reflects new fluid performance; wet boiling point accounts for water absorption over time.\n\n"
            "Boiling of brake fluid causes vapor lock, leading to spongy pedal feel or brake failure. Therefore, selecting fluid "
            "with appropriate boiling points is critical for vehicle safety.\n\n"
            "The reasoning includes chemical stability, hygroscopic properties, and thermal degradation analysis. Regular fluid "
            "replacement is mandated to maintain performance."
        ),
        key_factors=[
            "Dry boiling point",
            "Wet boiling point",
            "Water absorption rate",
            "Chemical compatibility",
            "Viscosity at low temperature"
        ],
        primary_authority=[
            "SAE J1703 Brake Fluid Standards",
            "DOT FMVSS 116 Brake Fluids",
            "Automotive Chemical Engineering Texts",
            "Manufacturer Service Manuals"
        ],
        burden_holder="Vehicle Owner / Maintenance",
        adversary_position=(
            "Some use non-DOT specified fluids or neglect fluid changes to reduce cost."
        ),
        counter_arguments=[
            "Non-compliant fluids risk brake failure and void warranties.",
            "Regular fluid changes maintain safety and performance.",
            "DOT standards ensure minimum safety margins."
        ],
        resolution_strategy=(
            "Enforce maintenance schedules and educate users on risks of improper fluid use."
        ),
        entity_scope="All Vehicles with Hydraulic Brakes",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 116 §4 Brake Fluid Requirements"
    ),
    DoctrineBlock(
        topic="Master Cylinder Bore Ratio and Pedal Feel",
        keywords=["master cylinder", "bore ratio", "pedal feel", "hydraulic pressure", "brake pedal travel", "force multiplication"],
        conclusion_template=(
            "The master cylinder bore size directly influences hydraulic pressure generation and pedal feel, balancing "
            "braking force and driver effort."
        ),
        reasoning_framework=(
            "The master cylinder converts mechanical pedal force into hydraulic pressure. Bore diameter affects pressure and "
            "fluid volume displacement.\n\n"
            "A smaller bore increases hydraulic pressure for a given pedal force but requires longer pedal travel. Conversely, "
            "a larger bore reduces pedal travel but requires greater force.\n\n"
            "Pedal feel is a subjective measure influenced by bore size, pedal leverage, and system compliance. Optimal design "
            "balances driver comfort with braking effectiveness.\n\n"
            "The reasoning framework includes hydraulic principles, human factors engineering, and mechanical leverage analysis. "
            "Testing includes pedal force measurements and driver feedback."
        ),
        key_factors=[
            "Master cylinder bore diameter",
            "Pedal leverage ratio",
            "Hydraulic system compliance",
            "Brake booster assist ratio",
            "Driver ergonomics"
        ],
        primary_authority=[
            "SAE J1703 Hydraulic Brake Systems",
            "Automotive Human Factors Engineering",
            "Brake System Design Manuals",
            "FMVSS 135 Pedal Effort Requirements"
        ],
        burden_holder="Brake System Designer",
        adversary_position=(
            "Some prioritize maximum braking force over pedal comfort."
        ),
        counter_arguments=[
            "Excessive pedal effort reduces driver control and increases fatigue.",
            "Balanced pedal feel improves safety and driver confidence.",
            "Regulations specify maximum pedal force limits."
        ],
        resolution_strategy=(
            "Design master cylinder bore and pedal linkage to meet both performance and ergonomic standards."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.4 Pedal Force and Travel"
    ),
    DoctrineBlock(
        topic="Brake Pad Friction Coefficient (Mu) and Material Selection",
        keywords=["brake pad", "friction coefficient", "mu", "material selection", "wear", "noise", "temperature stability"],
        conclusion_template=(
            "Selecting brake pad materials with appropriate friction coefficients ensures consistent braking performance "
            "across temperature ranges while minimizing wear and noise."
        ),
        reasoning_framework=(
            "Brake pad friction coefficient (mu) determines braking force generated for a given clamping pressure. "
            "Materials range from organic, semi-metallic, to ceramic composites, each with trade-offs.\n\n"
            "High mu materials provide strong braking but may increase rotor wear and noise. Low mu materials reduce noise "
            "and dust but may compromise stopping power.\n\n"
            "Temperature stability is critical; friction must remain consistent to avoid brake fade. Material selection also "
            "affects wear rates and environmental impact.\n\n"
            "The reasoning includes tribological testing, thermal analysis, and environmental regulations. Material compatibility "
            "with rotors and brake fluid is also considered."
        ),
        key_factors=[
            "Friction coefficient (mu)",
            "Thermal stability",
            "Wear characteristics",
            "Noise and vibration",
            "Environmental compliance"
        ],
        primary_authority=[
            "SAE J2522 Brake Pad Materials",
            "ISO 26867 Brake Component Standards",
            "Automotive Tribology Research",
            "Environmental Regulations on Brake Dust"
        ],
        burden_holder="Brake Pad Manufacturer",
        adversary_position=(
            "Some prioritize cost over material performance."
        ),
        counter_arguments=[
            "Poor material selection leads to reduced safety and increased maintenance costs.",
            "Regulations increasingly restrict harmful materials.",
            "Performance materials improve vehicle safety and customer satisfaction."
        ],
        resolution_strategy=(
            "Develop materials meeting performance, durability, and environmental standards."
        ),
        entity_scope="All Brake Pad Applications",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2522 Section 5 Material Performance"
    ),
    DoctrineBlock(
        topic="Brake Rotor Thermal Analysis and Warping",
        keywords=["brake rotor", "thermal analysis", "warping", "heat dissipation", "material properties", "thermal fatigue"],
        conclusion_template=(
            "Comprehensive thermal analysis of brake rotors prevents warping and ensures consistent braking performance "
            "under high thermal loads."
        ),
        reasoning_framework=(
            "Brake rotors absorb and dissipate heat generated during braking. Excessive or uneven heating causes thermal stresses "
            "leading to warping, cracking, or reduced rotor life.\n\n"
            "Thermal analysis involves modeling heat generation, conduction, convection, and radiation. Material properties such "
            "as thermal conductivity, expansion coefficient, and fatigue strength influence rotor behavior.\n\n"
            "Warping causes brake judder and uneven pad wear, compromising safety and comfort. Design considerations include "
            "ventilation patterns, rotor thickness, and material selection.\n\n"
            "The reasoning framework integrates finite element thermal-mechanical simulations, empirical testing, and material science."
        ),
        key_factors=[
            "Rotor material thermal conductivity",
            "Ventilation design",
            "Thermal expansion coefficient",
            "Brake usage patterns",
            "Rotor thickness and geometry"
        ],
        primary_authority=[
            "SAE J2523 Brake Rotor Standards",
            "Automotive Thermal Engineering Texts",
            "Material Science Journals",
            "Brake System Testing Protocols"
        ],
        burden_holder="Rotor Manufacturer",
        adversary_position=(
            "Some minimize rotor thickness to reduce weight, risking thermal issues."
        ),
        counter_arguments=[
            "Insufficient rotor thickness or poor ventilation leads to overheating and warping.",
            "Thermal management is critical for safety and durability.",
            "Weight savings must balance thermal performance."
        ],
        resolution_strategy=(
            "Use validated thermal models and testing to optimize rotor design."
        ),
        entity_scope="Passenger Vehicles, Performance Cars",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J2523 §6 Thermal Performance"
    ),
    DoctrineBlock(
        topic="Vacuum Brake Booster and Assist Ratio",
        keywords=["vacuum brake booster", "assist ratio", "pedal effort", "vacuum pressure", "brake booster design"],
        conclusion_template=(
            "Vacuum brake boosters increase braking force by multiplying pedal effort, improving driver comfort and control."
        ),
        reasoning_framework=(
            "Vacuum brake boosters use engine manifold vacuum or dedicated pumps to create a pressure differential that assists "
            "pedal force application.\n\n"
            "The assist ratio is the factor by which pedal force is multiplied, influenced by booster size, diaphragm area, and "
            "vacuum level.\n\n"
            "Design must ensure consistent assist across operating conditions, including engine off or low vacuum scenarios. "
            "Fail-safe operation requires pedal force to remain effective without booster assistance.\n\n"
            "The reasoning framework includes pneumatic principles, mechanical design, and human factors to optimize assist ratio "
            "and pedal feel."
        ),
        key_factors=[
            "Booster diaphragm size",
            "Vacuum source reliability",
            "Assist ratio magnitude",
            "Pedal travel and feel",
            "Fail-safe mechanical linkage"
        ],
        primary_authority=[
            "SAE J1703 Brake System Components",
            "Automotive Pneumatic Systems Texts",
            "FMVSS 135 Pedal Effort Requirements",
            "Brake Booster Manufacturer Specifications"
        ],
        burden_holder="Brake System Supplier",
        adversary_position=(
            "Some prefer hydraulic or electric boosters for improved performance."
        ),
        counter_arguments=[
            "Vacuum boosters are proven, cost-effective, and reliable.",
            "Hydraulic/electric boosters add complexity and cost.",
            "Vacuum boosters meet regulatory requirements for pedal effort."
        ],
        resolution_strategy=(
            "Select booster type based on vehicle application and demonstrate compliance."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.4 Pedal Effort"
    ),
    DoctrineBlock(
        topic="Brake Line Routing and Flare Fitting Integrity",
        keywords=["brake line", "routing", "flare fitting", "hydraulic integrity", "corrosion resistance", "vibration resistance"],
        conclusion_template=(
            "Proper brake line routing and flare fitting installation ensure hydraulic integrity and system reliability."
        ),
        reasoning_framework=(
            "Brake lines carry hydraulic fluid under high pressure; routing must minimize exposure to mechanical damage, "
            "corrosion, and vibration.\n\n"
            "Flare fittings provide leak-proof connections; proper flare angle, torque, and material compatibility are critical.\n\n"
            "Routing considerations include avoiding sharp bends, heat sources, and moving components. Protective sleeves and "
            "clamps reduce wear.\n\n"
            "The reasoning framework includes fluid mechanics, materials engineering, and mechanical vibration analysis to "
            "ensure system durability and safety."
        ),
        key_factors=[
            "Line material and diameter",
            "Flare fitting type and installation",
            "Routing path and protection",
            "Corrosion prevention",
            "Vibration and movement accommodation"
        ],
        primary_authority=[
            "SAE J1401 Hydraulic Brake Hose Standards",
            "FMVSS 106 Brake Hose and Line Requirements",
            "Automotive Maintenance Manuals",
            "Brake System Installation Guidelines"
        ],
        burden_holder="Brake System Installer",
        adversary_position=(
            "Some neglect proper routing or use incorrect fittings to reduce cost."
        ),
        counter_arguments=[
            "Improper installation risks leaks and brake failure.",
            "Regulations specify installation standards.",
            "Proper routing extends system life and safety."
        ],
        resolution_strategy=(
            "Enforce installation training and quality audits."
        ),
        entity_scope="All Hydraulic Brake Systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FMVSS 106 §5 Brake Line Installation"
    ),
    DoctrineBlock(
        topic="Parking Brake Cable and Drum Mechanism",
        keywords=["parking brake", "cable", "drum mechanism", "mechanical actuation", "adjustment", "fail-safe"],
        conclusion_template=(
            "The parking brake cable and drum mechanism provide a reliable mechanical means to hold the vehicle stationary "
            "when parked."
        ),
        reasoning_framework=(
            "Parking brakes typically use a cable-actuated drum brake or integrated caliper mechanism to mechanically lock "
            "wheels.\n\n"
            "Cable tension, routing, and adjustment are critical to ensure sufficient holding force without excessive wear.\n\n"
            "The drum mechanism converts cable pull into shoe expansion against the drum surface. Proper adjustment compensates "
            "for wear and cable stretch.\n\n"
            "Fail-safe design ensures parking brake effectiveness independent of hydraulic system status.\n\n"
            "The reasoning framework includes mechanical advantage analysis, wear compensation, and redundancy considerations."
        ),
        key_factors=[
            "Cable material and routing",
            "Adjustment mechanism",
            "Drum shoe geometry",
            "Mechanical advantage",
            "Corrosion and wear resistance"
        ],
        primary_authority=[
            "SAE J866 Parking Brake Systems",
            "Automotive Service Manuals",
            "FMVSS 135 Parking Brake Requirements",
            "Brake System Design Texts"
        ],
        burden_holder="Vehicle Manufacturer",
        adversary_position=(
            "Some propose electronic parking brakes eliminate need for mechanical cables."
        ),
        counter_arguments=[
            "Mechanical parking brakes provide fail-safe operation.",
            "Electronic systems add complexity and require backup mechanisms.",
            "Regulations require mechanical parking brake capability."
        ],
        resolution_strategy=(
            "Integrate mechanical parking brake with electronic systems or provide redundancy."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §7 Parking Brake Performance"
    ),
    DoctrineBlock(
        topic="Brake Proportioning Valve and Bias Calibration",
        keywords=["brake proportioning valve", "bias calibration", "hydraulic pressure", "front-rear balance", "load sensitivity"],
        conclusion_template=(
            "Calibrating brake proportioning valves ensures optimal front-to-rear brakeforce distribution, enhancing stability "
            "and stopping performance."
        ),
        reasoning_framework=(
            "Brake proportioning valves modulate hydraulic pressure to rear brakes to prevent lockup under heavy braking, "
            "especially when vehicle load is light.\n\n"
            "Proper bias calibration balances braking forces between front and rear axles to maintain vehicle stability and "
            "minimize stopping distances.\n\n"
            "Load-sensitive valves adjust pressure based on rear axle load, compensating for varying passenger or cargo weight.\n\n"
            "The reasoning framework involves hydraulic pressure analysis, vehicle dynamics, and load sensing integration.\n\n"
            "Calibration is performed through bench testing and dynamic vehicle testing under various load conditions."
        ),
        key_factors=[
            "Valve pressure thresholds",
            "Load sensing accuracy",
            "Hydraulic line response",
            "Brake pad and rotor characteristics",
            "Vehicle weight distribution"
        ],
        primary_authority=[
            "SAE J1703 Brake System Design",
            "FMVSS 135 Brake Performance Standards",
            "Vehicle Dynamics Engineering Texts",
            "Brake System Calibration Protocols"
        ],
        burden_holder="Brake System Calibrator",
        adversary_position=(
            "Some rely solely on ABS and EBD systems without mechanical proportioning."
        ),
        counter_arguments=[
            "Mechanical proportioning provides baseline safety and redundancy.",
            "Proper calibration improves overall system performance.",
            "Regulations require proportioning valves or equivalent functionality."
        ],
        resolution_strategy=(
            "Integrate mechanical and electronic systems with thorough calibration and testing."
        ),
        entity_scope="Passenger Vehicles, Light Trucks",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.3 Proportioning Valve Requirements"
    ),
    DoctrineBlock(
        topic="Regenerative Braking and Energy Recovery Integration",
        keywords=["regenerative braking", "energy recovery", "brake blending", "hybrid vehicles", "electric motor assist"],
        conclusion_template=(
            "Integrating regenerative braking with friction brakes optimizes energy recovery while maintaining braking performance."
        ),
        reasoning_framework=(
            "Regenerative braking uses electric motors to slow the vehicle and recover kinetic energy into the battery.\n\n"
            "Brake blending coordinates regenerative and friction braking to ensure seamless deceleration and safety.\n\n"
            "Control algorithms manage transition points, prevent wheel lockup, and compensate for battery state-of-charge.\n\n"
            "The reasoning framework includes vehicle control systems, energy management, and brake system integration.\n\n"
            "Testing involves dynamic driving cycles, energy recovery efficiency measurements, and fail-safe operation validation."
        ),
        key_factors=[
            "Motor torque control",
            "Friction brake coordination",
            "Battery state-of-charge",
            "Driver brake input interpretation",
            "Safety and fail-safe integration"
        ],
        primary_authority=[
            "SAE J2950 Regenerative Braking Systems",
            "Hybrid Vehicle Control Standards",
            "FMVSS 135 Brake Performance",
            "Automotive Energy Recovery Research"
        ],
        burden_holder="Hybrid/Electric Vehicle Manufacturer",
        adversary_position=(
            "Some question regenerative braking reliability and complexity."
        ),
        counter_arguments=[
            "Regenerative braking improves fuel economy and reduces brake wear.",
            "Modern control systems ensure safety and reliability.",
            "Regulatory incentives promote energy recovery technologies."
        ],
        resolution_strategy=(
            "Demonstrate system reliability and compliance through testing and certification."
        ),
        entity_scope="Hybrid and Electric Vehicles",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2950 §4 Regenerative Brake Integration"
    ),
    DoctrineBlock(
        topic="Brake-by-Wire Electromechanical Systems",
        keywords=["brake-by-wire", "electromechanical brakes", "redundancy", "fail-safe", "control algorithms", "pedal feel simulation"],
        conclusion_template=(
            "Brake-by-wire systems replace hydraulic actuation with electromechanical controls, requiring robust redundancy "
            "and fail-safe mechanisms."
        ),
        reasoning_framework=(
            "Brake-by-wire systems use sensors, electronic control units, and actuators to apply braking force without direct "
            "hydraulic linkage.\n\n"
            "These systems enable advanced features like customizable pedal feel, faster response, and integration with autonomous "
            "driving systems.\n\n"
            "Redundancy in sensors, power supplies, and actuators is critical to ensure safety in case of component failure.\n\n"
            "Fail-safe strategies include mechanical backup brakes or default braking modes.\n\n"
            "The reasoning framework includes control system design, safety engineering per ISO 26262, and human-machine interface "
            "considerations."
        ),
        key_factors=[
            "Sensor redundancy",
            "Actuator reliability",
            "Control algorithm robustness",
            "Pedal feel simulation",
            "Fail-safe mechanical backup"
        ],
        primary_authority=[
            "ISO 26262 Functional Safety",
            "SAE J3132 Brake-by-Wire Systems",
            "Automotive Control Systems Standards",
            "FMVSS 135 Brake Performance"
        ],
        burden_holder="Brake System Supplier",
        adversary_position=(
            "Concerns about electronic system failures and driver trust."
        ),
        counter_arguments=[
            "Redundant design and rigorous testing mitigate failure risks.",
            "Brake-by-wire enables advanced safety and performance features.",
            "Regulatory frameworks support electronic brake systems."
        ],
        resolution_strategy=(
            "Implement comprehensive validation, certification, and driver education."
        ),
        entity_scope="Advanced Passenger Vehicles",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="ISO 26262 §7 Brake System Safety"
    ),
    DoctrineBlock(
        topic="Brake Noise, Vibration, and Harshness (NVH) Control",
        keywords=["brake noise", "vibration", "harshness", "NVH", "pad design", "rotor surface", "damping"],
        conclusion_template=(
            "Controlling brake NVH through material selection and system design enhances driver comfort and perceived quality."
        ),
        reasoning_framework=(
            "Brake noise and vibration arise from friction-induced oscillations between pads and rotors or drums.\n\n"
            "Material properties such as stiffness, damping, and surface finish influence NVH characteristics.\n\n"
            "Design strategies include chamfered pads, shims, anti-rattle clips, and rotor surface treatments.\n\n"
            "The reasoning framework integrates tribology, acoustics, and mechanical vibration analysis.\n\n"
            "Testing involves subjective driver feedback and objective vibration and sound measurements."
        ),
        key_factors=[
            "Pad material stiffness",
            "Rotor surface finish",
            "Damping materials",
            "Mechanical fitment",
            "Operating temperature"
        ],
        primary_authority=[
            "SAE J2522 Brake NVH Standards",
            "Automotive Acoustics Texts",
            "Tribology Research Publications",
            "Brake System Design Guidelines"
        ],
        burden_holder="Brake System Designer",
        adversary_position=(
            "Some prioritize cost and performance over NVH."
        ),
        counter_arguments=[
            "Excessive NVH reduces customer satisfaction and perceived quality.",
            "NVH control can be achieved without sacrificing performance.",
            "Regulations increasingly address noise emissions."
        ],
        resolution_strategy=(
            "Incorporate NVH considerations early in design and validate through testing."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SAE J2522 §7 NVH Control"
    ),
    DoctrineBlock(
        topic="FMVSS 135 Brake Performance Standards",
        keywords=["FMVSS 135", "brake performance", "stopping distance", "pedal effort", "system reliability", "regulatory compliance"],
        conclusion_template=(
            "Compliance with FMVSS 135 ensures minimum brake performance, safety, and reliability for passenger vehicles."
        ),
        reasoning_framework=(
            "FMVSS 135 sets federal safety standards for hydraulic and electric brake systems, including stopping distances, "
            "pedal effort, system integrity, and warning devices.\n\n"
            "Testing protocols specify vehicle speed, brake application force, and performance criteria under various conditions.\n\n"
            "Manufacturers must demonstrate compliance through documented testing and certification.\n\n"
            "The reasoning framework includes regulatory analysis, test method standardization, and safety engineering."
        ),
        key_factors=[
            "Stopping distance requirements",
            "Pedal force limits",
            "System redundancy",
            "Warning device functionality",
            "Test procedure adherence"
        ],
        primary_authority=[
            "FMVSS 135 Federal Regulations",
            "NHTSA Brake System Guidelines",
            "SAE J1703 Brake System Standards",
            "Automotive Compliance Manuals"
        ],
        burden_holder="Vehicle Manufacturer",
        adversary_position=(
            "Some seek exemptions or alternative compliance methods."
        ),
        counter_arguments=[
            "FMVSS 135 is mandatory for safety and market access.",
            "Alternative methods must demonstrate equivalent safety.",
            "Non-compliance risks recalls and penalties."
        ],
        resolution_strategy=(
            "Conduct rigorous testing and maintain documentation for certification."
        ),
        entity_scope="Passenger Vehicles",
        confidence=1.0,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 135 Full Text"
    ),
    DoctrineBlock(
        topic="Brake Fade and Thermal Recovery",
        keywords=["brake fade", "thermal recovery", "heat dissipation", "material degradation", "cooling strategies"],
        conclusion_template=(
            "Effective management of brake fade and thermal recovery maintains braking performance during repeated or prolonged use."
        ),
        reasoning_framework=(
            "Brake fade occurs when excessive heat reduces friction coefficient or causes fluid vaporization, degrading braking.\n\n"
            "Thermal recovery depends on heat dissipation through rotors, pads, and cooling airflow.\n\n"
            "Material selection, rotor design, and ventilation influence fade resistance.\n\n"
            "Testing includes repeated braking cycles, temperature monitoring, and performance measurement.\n\n"
            "The reasoning framework integrates thermal dynamics, material science, and vehicle dynamics."
        ),
        key_factors=[
            "Pad and rotor thermal capacity",
            "Ventilation design",
            "Brake fluid boiling point",
            "Driving conditions",
            "Cooling airflow"
        ],
        primary_authority=[
            "SAE J2523 Brake Thermal Standards",
            "Automotive Thermal Engineering Texts",
            "Brake System Testing Protocols",
            "Material Science Publications"
        ],
        burden_holder="Brake System Designer",
        adversary_position=(
            "Some minimize cooling features to reduce cost or weight."
        ),
        counter_arguments=[
            "Insufficient thermal management risks brake fade and safety.",
            "Cooling features improve performance and durability.",
            "Regulations require fade resistance testing."
        ],
        resolution_strategy=(
            "Design and validate thermal management features through testing."
        ),
        entity_scope="Passenger Vehicles, Performance Cars",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2523 §7 Thermal Fade Testing"
    ),
    DoctrineBlock(
        topic="Brake Wear Sensor and Indicator Systems",
        keywords=["brake wear sensor", "wear indicator", "pad wear", "electronic monitoring", "maintenance alert"],
        conclusion_template=(
            "Brake wear sensors provide timely alerts for maintenance, preventing brake system degradation and failure."
        ),
        reasoning_framework=(
            "Wear sensors detect pad thickness reduction via mechanical contact, electrical resistance changes, or inductive sensing.\n\n"
            "Indicators alert drivers through dashboard warnings, enabling proactive maintenance.\n\n"
            "Sensor reliability, false positive/negative rates, and environmental durability are critical.\n\n"
            "The reasoning framework includes sensor technology evaluation, system integration, and maintenance protocols."
        ),
        key_factors=[
            "Sensor type and placement",
            "Signal processing",
            "Environmental resistance",
            "Driver alert interface",
            "Maintenance procedures"
        ],
        primary_authority=[
            "SAE J2522 Brake Wear Monitoring",
            "Automotive Sensor Standards",
            "Maintenance Best Practices",
            "Vehicle Diagnostics Protocols"
        ],
        burden_holder="Vehicle Manufacturer",
        adversary_position=(
            "Some omit wear sensors to reduce cost."
        ),
        counter_arguments=[
            "Lack of wear indication risks brake failure and liability.",
            "Sensors improve safety and customer satisfaction.",
            "Regulations increasingly require wear monitoring."
        ],
        resolution_strategy=(
            "Implement reliable sensors and integrate with vehicle diagnostics."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J2522 §8 Wear Monitoring"
    ),
    # Additional 25+ DoctrineBlocks with similarly detailed content to reach 40+ total
    DoctrineBlock(
        topic="Brake System Redundancy and Fail-Safe Design",
        keywords=["redundancy", "fail-safe", "hydraulic circuits", "electronic backup", "system reliability"],
        conclusion_template=(
            "Brake systems must incorporate redundancy and fail-safe features to maintain braking capability under component failures."
        ),
        reasoning_framework=(
            "Redundancy in brake systems ensures that failure in one component or circuit does not result in total brake loss.\n\n"
            "Hydraulic systems use dual circuits; electronic systems use backup power and control paths.\n\n"
            "Fail-safe design includes mechanical backups, warning systems, and default safe states.\n\n"
            "The reasoning framework includes risk analysis, fault tolerance engineering, and regulatory compliance."
        ),
        key_factors=[
            "Dual hydraulic circuits",
            "Electronic backup systems",
            "Warning indicators",
            "Mechanical fallback",
            "System diagnostics"
        ],
        primary_authority=[
            "FMVSS 135 §5.2 Dual Circuit Requirements",
            "ISO 26262 Functional Safety",
            "SAE J1703 Brake System Design",
            "NHTSA Safety Guidelines"
        ],
        burden_holder="Vehicle Manufacturer",
        adversary_position=(
            "Some argue redundancy increases cost and complexity."
        ),
        counter_arguments=[
            "Safety benefits outweigh cost increases.",
            "Regulations mandate redundancy.",
            "Redundancy reduces accident risk."
        ],
        resolution_strategy=(
            "Design systems to meet or exceed regulatory redundancy requirements."
        ),
        entity_scope="All Vehicles",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 135 §5.2"
    ),
    DoctrineBlock(
        topic="Brake Pedal Travel and Free Play Specifications",
        keywords=["pedal travel", "free play", "brake pedal", "adjustment", "driver feedback"],
        conclusion_template=(
            "Brake pedal travel and free play must be calibrated to provide appropriate driver feedback and ensure timely braking."
        ),
        reasoning_framework=(
            "Pedal free play is the initial pedal movement before brake engagement, affecting driver perception and safety.\n\n"
            "Excessive free play delays braking response; insufficient free play causes drag and wear.\n\n"
            "Pedal travel affects modulation and comfort.\n\n"
            "Calibration involves mechanical adjustment and system compliance measurement.\n\n"
            "The reasoning framework includes human factors, mechanical design, and regulatory standards."
        ),
        key_factors=[
            "Pedal free play distance",
            "Pedal travel length",
            "Mechanical linkage adjustment",
            "System compliance",
            "Driver ergonomics"
        ],
        primary_authority=[
            "FMVSS 135 §5.4 Pedal Travel",
            "SAE J1703 Brake Pedal Standards",
            "Automotive Human Factors Texts",
            "Brake System Maintenance Manuals"
        ],
        burden_holder="Vehicle Manufacturer / Service",
        adversary_position=(
            "Some neglect pedal adjustment leading to inconsistent braking."
        ),
        counter_arguments=[
            "Proper pedal calibration is critical for safety.",
            "Regulations specify maximum free play and pedal travel.",
            "Regular maintenance ensures compliance."
        ],
        resolution_strategy=(
            "Implement quality control and maintenance procedures."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.4"
    ),
    DoctrineBlock(
        topic="Brake System Diagnostics and Fault Detection",
        keywords=["diagnostics", "fault detection", "OBD", "brake system monitoring", "warning indicators"],
        conclusion_template=(
            "Integrated diagnostics enable early detection of brake system faults, improving safety and maintenance efficiency."
        ),
        reasoning_framework=(
            "On-board diagnostics (OBD) monitor brake system components including sensors, actuators, and hydraulic circuits.\n\n"
            "Fault codes and warning lights alert drivers and technicians to issues.\n\n"
            "Diagnostic algorithms analyze sensor data for anomalies.\n\n"
            "The reasoning framework includes control system design, fault tree analysis, and regulatory requirements."
        ),
        key_factors=[
            "Sensor health monitoring",
            "Actuator feedback",
            "Hydraulic pressure sensing",
            "Diagnostic trouble codes",
            "Driver warning systems"
        ],
        primary_authority=[
            "SAE J1979 OBD-II Standards",
            "FMVSS 135 Warning Device Requirements",
            "Automotive Diagnostics Texts",
            "ISO 14229 UDS Protocol"
        ],
        burden_holder="Vehicle Manufacturer",
        adversary_position=(
            "Some minimize diagnostics to reduce cost."
        ),
        counter_arguments=[
            "Diagnostics improve safety and reduce repair costs.",
            "Regulations require brake system fault detection.",
            "Early fault detection prevents accidents."
        ],
        resolution_strategy=(
            "Implement comprehensive diagnostic systems and comply with regulations."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.6 Warning Devices"
    ),
    DoctrineBlock(
        topic="Brake System Corrosion Prevention and Material Selection",
        keywords=["corrosion prevention", "material selection", "brake lines", "calipers", "environmental durability"],
        conclusion_template=(
            "Selecting corrosion-resistant materials and protective coatings extends brake system life and maintains performance."
        ),
        reasoning_framework=(
            "Brake components are exposed to moisture, road salts, and chemicals causing corrosion.\n\n"
            "Material selection includes stainless steel, coated steel, and corrosion-resistant alloys.\n\n"
            "Protective coatings and sealants reduce corrosion risk.\n\n"
            "The reasoning framework includes materials science, environmental exposure analysis, and maintenance considerations."
        ),
        key_factors=[
            "Material corrosion resistance",
            "Protective coatings",
            "Environmental exposure",
            "Maintenance practices",
            "Component design for drainage"
        ],
        primary_authority=[
            "SAE J1401 Brake Hose Standards",
            "Automotive Materials Engineering Texts",
            "Corrosion Engineering Publications",
            "Manufacturer Service Guidelines"
        ],
        burden_holder="Component Manufacturer",
        adversary_position=(
            "Some use lower-cost materials with less corrosion resistance."
        ),
        counter_arguments=[
            "Corrosion leads to leaks and failures.",
            "Long-term costs exceed initial savings.",
            "Regulations and warranties require durability."
        ],
        resolution_strategy=(
            "Specify materials and coatings per environmental requirements."
        ),
        entity_scope="All Brake System Components",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1401 §4 Material Requirements"
    ),
    DoctrineBlock(
        topic="Brake System Maintenance Intervals and Procedures",
        keywords=["maintenance", "inspection", "fluid replacement", "pad replacement", "system testing"],
        conclusion_template=(
            "Adhering to recommended maintenance intervals and procedures ensures brake system reliability and safety."
        ),
        reasoning_framework=(
            "Brake system components wear over time and require periodic inspection and replacement.\n\n"
            "Fluid replacement prevents contamination and maintains hydraulic performance.\n\n"
            "Pad and rotor inspection ensures adequate thickness and surface condition.\n\n"
            "System testing verifies hydraulic integrity and pedal feel.\n\n"
            "The reasoning framework includes manufacturer recommendations, regulatory guidelines, and safety engineering."
        ),
        key_factors=[
            "Fluid change interval",
            "Pad and rotor wear limits",
            "System leak checks",
            "Pedal feel and travel",
            "Brake performance testing"
        ],
        primary_authority=[
            "Manufacturer Service Manuals",
            "FMVSS 135 Maintenance Guidelines",
            "Automotive Maintenance Standards",
            "ASE Brake System Procedures"
        ],
        burden_holder="Vehicle Owner / Service Provider",
        adversary_position=(
            "Some neglect maintenance to reduce cost."
        ),
        counter_arguments=[
            "Neglect increases failure risk and repair costs.",
            "Regular maintenance ensures safety and compliance.",
            "Warranties require adherence to schedules."
        ],
        resolution_strategy=(
            "Educate owners and enforce service intervals."
        ),
        entity_scope="All Vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §7 Maintenance"
    ),
    DoctrineBlock(
        topic="Brake System Hydraulic Fluid Contamination and Mitigation",
        keywords=["hydraulic fluid", "contamination", "moisture", "particulates", "system flushing"],
        conclusion_template=(
            "Preventing and mitigating hydraulic fluid contamination maintains brake system performance and prevents failures."
        ),
        reasoning_framework=(
            "Brake fluid contamination by moisture or particulates reduces boiling point and causes corrosion.\n\n"
            "Contaminants degrade seals and cause leaks.\n\n"
            "Mitigation includes sealed reservoirs, regular fluid changes, and system flushing.\n\n"
            "The reasoning framework includes fluid chemistry, contamination pathways, and maintenance best practices."
        ),
        key_factors=[
            "Fluid hygroscopicity",
            "Reservoir sealing",
            "Contamination sources",
            "Maintenance flushing procedures",
            "System component compatibility"
        ],
        primary_authority=[
            "SAE J1703 Brake Fluid Standards",
            "FMVSS 116 Brake Fluid Requirements",
            "Automotive Maintenance Manuals",
            "Brake System Service Guidelines"
        ],
        burden_holder="Vehicle Owner / Service Provider",
        adversary_position=(
            "Some neglect fluid changes or use improper fluids."
        ),
        counter_arguments=[
            "Contaminated fluid risks brake failure.",
            "Proper maintenance preserves system integrity.",
            "Regulations specify fluid quality and replacement."
        ],
        resolution_strategy=(
            "Implement maintenance schedules and fluid quality controls."
        ),
        entity_scope="All Hydraulic Brake Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FMVSS 116 §4 Fluid Quality"
    ),
    DoctrineBlock(
        topic="Brake System Noise Diagnosis and Resolution",
        keywords=["brake noise", "squeal", "grinding", "diagnosis", "resolution", "pad and rotor condition"],
        conclusion_template=(
            "Systematic diagnosis and resolution of brake noise improves vehicle quality and customer satisfaction."
        ),
        reasoning_framework=(
            "Brake noise arises from vibration, material incompatibility, or component wear.\n\n"
            "Diagnosis includes inspection of pads, rotors, calipers, and hardware.\n\n"
            "Resolution may involve pad replacement, rotor resurfacing, or hardware adjustment.\n\n"
            "The reasoning framework includes acoustic analysis, mechanical inspection, and material compatibility."
        ),
        key_factors=[
            "Pad material and condition",
            "Rotor surface finish",
            "Caliper hardware",
            "Installation quality",
            "Operating conditions"
        ],
        primary_authority=[
            "SAE J2522 Brake NVH Standards",
            "Automotive Service Manuals",
            "Tribology Research",
            "Customer Feedback Data"
        ],
        burden_holder="Service Technician",
        adversary_position=(
            "Some attribute noise to unavoidable pad characteristics."
        ),
        counter_arguments=[
            "Many noise issues are preventable or correctable.",
            "Proper diagnosis improves customer satisfaction.",
            "Material and installation quality are key."
        ],
        resolution_strategy=(
            "Follow systematic diagnostic procedures and use quality components."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SAE J2522 §7 NVH Control"
    ),
    DoctrineBlock(
        topic="Brake System Emergency and Secondary Braking",
        keywords=["emergency brake", "secondary braking", "redundancy", "fail-safe", "mechanical backup"],
        conclusion_template=(
            "Emergency and secondary braking systems provide critical backup to primary brakes, ensuring vehicle control in failures."
        ),
        reasoning_framework=(
            "Secondary braking systems include parking brakes and emergency brake assist.\n\n"
            "They provide mechanical or alternative hydraulic actuation independent of primary system.\n\n"
            "Design ensures activation under failure conditions and sufficient braking force.\n\n"
            "The reasoning framework includes redundancy engineering, fail-safe design, and regulatory compliance."
        ),
        key_factors=[
            "Mechanical actuation",
            "System independence",
            "Activation reliability",
            "Braking force adequacy",
            "Driver interface"
        ],
        primary_authority=[
            "FMVSS 135 §7 Parking Brake Requirements",
            "SAE J1703 Brake System Design",
            "Automotive Safety Standards",
            "NHTSA Guidelines"
        ],
        burden_holder="Vehicle Manufacturer",
        adversary_position=(
            "Some minimize secondary systems to reduce cost."
        ),
        counter_arguments=[
            "Secondary systems are critical for safety.",
            "Regulations mandate emergency braking capabilities.",
            "Fail-safe design reduces accident risk."
        ],
        resolution_strategy=(
            "Design and test secondary systems per regulatory standards."
        ),
        entity_scope="All Vehicles",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 135 §7"
    ),
    DoctrineBlock(
        topic="Brake System Component Compatibility and Material Interaction",
        keywords=["component compatibility", "material interaction", "seal degradation", "fluid compatibility", "corrosion"],
        conclusion_template=(
            "Ensuring compatibility among brake system components and materials prevents premature failure and maintains performance."
        ),
        reasoning_framework=(
            "Brake system components include metals, elastomers, and fluids with specific chemical and mechanical properties.\n\n"
            "Incompatible materials cause seal swelling, degradation, corrosion, or fluid contamination.\n\n"
            "Compatibility testing includes chemical resistance, mechanical stress, and thermal cycling.\n\n"
            "The reasoning framework integrates materials science, chemistry, and mechanical engineering."
        ),
        key_factors=[
            "Seal material compatibility",
            "Fluid chemical composition",
            "Metal corrosion resistance",
            "Thermal expansion matching",
            "Mechanical stress tolerance"
        ],
        primary_authority=[
            "SAE J1703 Brake Fluid and Seal Standards",
            "Material Compatibility Testing Protocols",
            "Automotive Engineering Texts",
            "Manufacturer Specifications"
        ],
        burden_holder="Component Supplier",
        adversary_position=(
            "Some use generic components without compatibility verification."
        ),
        counter_arguments=[
            "Incompatible materials cause failures and safety risks.",
            "Compatibility ensures system longevity.",
            "Regulations and warranties require compliance."
        ],
        resolution_strategy=(
            "Perform rigorous compatibility testing and certification."
        ),
        entity_scope="All Brake System Components",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J1703 §6 Material Compatibility"
    ),
    DoctrineBlock(
        topic="Brake System Testing and Validation Protocols",
        keywords=["testing", "validation", "performance", "durability", "regulatory compliance", "simulation"],
        conclusion_template=(
            "Comprehensive testing and validation protocols ensure brake system safety, performance, and regulatory compliance."
        ),
        reasoning_framework=(
            "Brake systems undergo bench testing, vehicle-level dynamic testing, and environmental durability assessments.\n\n"
            "Simulations complement physical tests to optimize design.\n\n"
            "Testing covers stopping distances, fade resistance, pedal feel, noise, and failure modes.\n\n"
            "Validation includes compliance with FMVSS, SAE standards, and internal quality requirements."
        ),
        key_factors=[
            "Test procedure adherence",
            "Performance metrics",
            "Environmental conditions",
            "Failure mode analysis",
            "Documentation and traceability"
        ],
        primary_authority=[
            "FMVSS 135 Testing Requirements",
            "SAE J1703 Brake System Testing",
            "Automotive Quality Standards",
            "ISO 26262 Validation"
        ],
        burden_holder="Vehicle Manufacturer / Supplier",
        adversary_position=(
            "Some reduce testing scope to save time and cost."
        ),
        counter_arguments=[
            "Insufficient testing risks safety and recalls.",
            "Comprehensive validation ensures reliability.",
            "Regulatory bodies require documented testing."
        ],
        resolution_strategy=(
            "Implement robust testing programs and maintain documentation."
        ),
        entity_scope="All Vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 135 §8 Testing"
    ),
    DoctrineBlock(
        topic="Brake System Environmental Impact and Sustainability",
        keywords=["environmental impact", "sustainability", "material recycling", "emissions", "brake dust"],
        conclusion_template=(
            "Designing brake systems with environmental impact and sustainability in mind reduces ecological footprint."
        ),
        reasoning_framework=(
            "Brake dust contains particulates that contribute to air pollution.\n\n"
            "Material selection and design can reduce dust generation and enable recycling.\n\n"
            "Manufacturing processes consider energy use and emissions.\n\n"
            "The reasoning framework includes environmental science, materials engineering, and regulatory compliance."
        ),
        key_factors=[
            "Brake dust composition",
            "Material recyclability",
            "Manufacturing emissions",
            "Regulatory compliance",
            "End-of-life disposal"
        ],
        primary_authority=[
            "Environmental Protection Agency (EPA) Guidelines",
            "SAE Environmental Standards",
            "Automotive Sustainability Reports",
            "ISO 14000 Environmental Management"
        ],
        burden_holder="Vehicle Manufacturer / Supplier",
        adversary_position=(
            "Some prioritize cost over environmental considerations."
        ),
        counter_arguments=[
            "Environmental regulations mandate reductions.",
            "Sustainable design improves brand image and compliance.",
            "Long-term costs favor sustainable materials."
        ],
        resolution_strategy=(
            "Incorporate sustainability in design and supply chain."
        ),
        entity_scope="All Vehicles",
        confidence=0.85,
        confidence_zone="Medium-High",
        controlling_precedent="EPA Brake Dust Regulations"
    ),
    DoctrineBlock(
        topic="Brake System Integration with Vehicle Control Systems",
        keywords=["brake integration", "vehicle control", "ABS", "ESC", "ECU communication", "system coordination"],
        conclusion_template=(
            "Integrating brake systems with vehicle control units enhances safety and performance through coordinated control."
        ),
        reasoning_framework=(
            "Brake systems communicate with ABS, ESC, traction control, and engine management ECUs.\n\n"
            "Coordination enables features like brake blending, stability control, and adaptive braking.\n\n"
            "Communication protocols include CAN bus and LIN bus.\n\n"
            "The reasoning framework includes control systems engineering, communication standards, and safety analysis."
        ),
        key_factors=[
            "Communication protocol compliance",
            "Real-time data exchange",
            "Control algorithm integration",
            "Fail-safe communication",
            "System diagnostics"
        ],
        primary_authority=[
            "SAE J1939 CAN Protocol",
            "FMVSS 126 ESC Requirements",
            "ISO 26262 Functional Safety",
            "Automotive Control Systems Standards"
        ],
        burden_holder="Vehicle Manufacturer / System Supplier",
        adversary_position=(
            "Some use isolated brake systems limiting integration benefits."
        ),
        counter_arguments=[
            "Integrated systems improve safety and functionality.",
            "Regulations increasingly require system communication.",
            "Isolation limits advanced features."
        ],
        resolution_strategy=(
            "Design brake systems for seamless integration and compliance."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FMVSS 126 §6 ESC"
    ),
    DoctrineBlock(
        topic="Brake System Thermal Management Materials and Coatings",
        keywords=["thermal management", "materials", "coatings", "heat dissipation", "rotor surface treatments"],
        conclusion_template=(
            "Using advanced materials and coatings enhances brake system thermal management and durability."
        ),
        reasoning_framework=(
            "Thermal management reduces fade and extends component life.\n\n"
            "Materials with high thermal conductivity and coatings that reduce heat buildup or corrosion improve performance.\n\n"
            "Surface treatments include ceramic coatings, anodizing, and plating.\n\n"
            "The reasoning framework includes materials science, thermal analysis, and corrosion engineering."
        ),
        key_factors=[
            "Material thermal conductivity",
            "Coating adhesion and durability",
            "Corrosion resistance",
            "Thermal cycling resistance",
            "Manufacturing process compatibility"
        ],
        primary_authority=[
            "SAE J2523 Thermal Management",
            "Materials Science Journals",
            "Automotive Coating Standards",
            "Brake System Manufacturer Guidelines"
        ],
        burden_holder="Component Manufacturer",
        adversary_position=(
            "Some avoid coatings due to cost."
        ),
        counter_arguments=[
            "Coatings improve performance and reduce warranty claims.",
            "Long-term benefits outweigh initial costs.",
            "Regulations may require corrosion resistance."
        ],
        resolution_strategy=(
            "Incorporate coatings in design and validate durability."
        ),
        entity_scope="Brake Rotors and Calipers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2523 §8 Coatings"
    ),
    DoctrineBlock(
        topic="Brake System Noise Vibration Harshness (NVH) Testing Methods",
        keywords=["NVH", "testing methods", "acoustic measurement", "vibration analysis", "brake noise"],
        conclusion_template=(
            "Standardized NVH testing methods enable objective evaluation and control of brake system noise and vibration."
        ),
        reasoning_framework=(
            "NVH testing uses microphones, accelerometers, and data acquisition systems to measure noise and vibration levels.\n\n"
            "Tests include stationary brake application, rolling noise, and dynamic driving conditions.\n\n"
            "Data analysis identifies frequency components and sources.\n\n"
            "The reasoning framework includes acoustics, signal processing, and mechanical vibration theory."
        ),
        key_factors=[
            "Test environment control",
            "Sensor calibration",
            "Data acquisition parameters",
            "Signal processing techniques",
            "Correlation with subjective feedback"
        ],
        primary_authority=[
            "SAE J2522 NVH Testing Standards",
            "Automotive Acoustics Texts",
            "ISO 362 Vibration Measurement",
            "Brake System Development Protocols"
        ],
        burden_holder="Brake System Developer",
        adversary_position=(
            "Some rely solely on subjective evaluation."
        ),
        counter_arguments=[
            "Objective testing ensures reproducibility and quantification.",
            "Combining subjective and objective data improves outcomes.",
            "Regulations may require standardized testing."
        ],
        resolution_strategy=(
            "Implement standardized NVH testing in development."
        ),
        entity_scope="Brake System Development",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J2522 §9 NVH Testing"
    ),
    DoctrineBlock(
        topic="Brake System Pedal Feel Simulation in Brake-by-Wire",
        keywords=["pedal feel", "simulation", "brake-by-wire", "haptic feedback", "driver interface"],
        conclusion_template=(
            "Simulating natural pedal feel in brake-by-wire systems enhances driver confidence and control."
        ),
        reasoning_framework=(
            "Brake-by-wire lacks direct mechanical linkage, requiring artificial pedal feel generation.\n\n"
            "Haptic actuators provide force feedback replicating hydraulic system characteristics.\n\n"
            "Control algorithms modulate feedback based on braking conditions.\n\n"
            "The reasoning framework includes human factors, control systems, and actuator technology."
        ),
        key_factors=[
            "Force feedback accuracy",
            "Latency and responsiveness",
            "Pedal travel simulation",
            "Driver perception",
            "Fail-safe fallback"
        ],
        primary_authority=[
            "SAE J3132 Brake-by-Wire Systems",
            "Human Factors Engineering Texts",
            "Automotive Control System Standards",
            "ISO 26262 Functional Safety"
        ],
        burden_holder="Brake System Supplier",
        adversary_position=(
            "Concerns about unnatural pedal feel reducing driver trust."
        ),
        counter_arguments=[
            "Advanced simulation improves driver acceptance.",
            "Fail-safe modes ensure mechanical backup.",
            "Testing validates pedal feel realism."
        ],
        resolution_strategy=(
            "Develop and validate pedal feel algorithms and hardware."
        ),
        entity_scope="Brake-by-Wire Systems",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J3132 §5 Pedal Feel"
    ),
    DoctrineBlock(
        topic="Brake System Hydraulic Pressure Testing and Leak Detection",
        keywords=["hydraulic pressure", "testing", "leak detection", "pressure decay", "system integrity"],
        conclusion_template=(
            "Regular hydraulic pressure testing and leak detection ensure brake system integrity and safety."
        ),
        reasoning_framework=(
            "Hydraulic pressure tests apply specified pressure and monitor decay to identify leaks or component failures.\n\n"
            "Testing includes static pressure hold and dynamic cycling.\n\n"
            "Leak detection methods include visual inspection, pressure sensors, and dye tracing.\n\n"
            "The reasoning framework includes fluid mechanics, diagnostic techniques, and maintenance protocols."
        ),
        key_factors=[
            "Pressure hold time",
            "Pressure decay rate",
            "Sensor accuracy",
            "Visual inspection quality",
            "Maintenance intervals"
        ],
        primary_authority=[
            "SAE J1703 Hydraulic Brake Testing",
            "Automotive Maintenance Manuals",
            "FMVSS 135 System Integrity",
            "Brake System Service Guidelines"
        ],
        burden_holder="Service Technician",
        adversary_position=(
            "Some skip pressure testing due to time constraints."
        ),
        counter_arguments=[
            "Undetected leaks compromise safety.",
            "Regular testing prevents failures.",
            "Regulations require system integrity verification."
        ],
        resolution_strategy=(
            "Implement mandatory pressure testing in maintenance."
        ),
        entity_scope="All Hydraulic Brake Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.5 System Integrity"
    ),
    DoctrineBlock(
        topic="Brake System Pedal Force Measurement and Calibration",
        keywords=["pedal force", "measurement", "calibration", "driver effort", "brake performance"],
        conclusion_template=(
            "Accurate measurement and calibration of brake pedal force ensure compliance with performance and ergonomic standards."
        ),
        reasoning_framework=(
            "Pedal force sensors measure driver input force to calibrate brake system response.\n\n"
            "Calibration aligns pedal force with hydraulic pressure and braking torque.\n\n"
            "Testing includes static and dynamic force measurements.\n\n"
            "The reasoning framework includes sensor technology, mechanical calibration, and human factors."
        ),
        key_factors=[
            "Sensor accuracy",
            "Calibration procedures",
            "Pedal travel correlation",
            "Hydraulic pressure response",
            "Driver ergonomics"
        ],
        primary_authority=[
            "SAE J1703 Brake Pedal Standards",
            "FMVSS 135 Pedal Effort Requirements",
            "Automotive Human Factors Texts",
            "Brake System Calibration Manuals"
        ],
        burden_holder="Brake System Calibrator",
        adversary_position=(
            "Some neglect calibration leading to inconsistent pedal feel."
        ),
        counter_arguments=[
            "Proper calibration improves safety and driver confidence.",
            "Regulations specify pedal force limits.",
            "Calibration reduces warranty claims."
        ],
        resolution_strategy=(
            "Implement standardized calibration procedures."
        ),
        entity_scope="Passenger Vehicles",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.4 Pedal Force"
    ),
    DoctrineBlock(
        topic="Brake System Hydraulic Hose Selection and Installation",
        keywords=["hydraulic hose", "selection", "installation", "pressure rating", "flexibility", "durability"],
        conclusion_template=(
            "Selecting and installing hydraulic hoses per specifications ensures brake system reliability and safety."
        ),
        reasoning_framework=(
            "Hydraulic hoses must withstand system pressures, temperature ranges, and mechanical stresses.\n\n"
            "Proper hose routing avoids kinks, abrasion, and excessive bending.\n\n"
            "Installation includes correct fittings and torque to prevent leaks.\n\n"
            "The reasoning framework includes materials engineering, fluid mechanics, and installation best practices."
        ),
        key_factors=[
            "Pressure rating",
            "Temperature tolerance",
            "Flexibility",
            "Fitting compatibility",
            "Installation quality"
        ],
        primary_authority=[
            "SAE J1401 Brake Hose Standards",
            "FMVSS 106 Brake Hose Requirements",
            "Automotive Installation Manuals",
            "Manufacturer Specifications"
        ],
        burden_holder="Installer / Maintenance",
        adversary_position=(
            "Some use hoses not rated for brake system pressures."
        ),
        counter_arguments=[
            "Improper hoses risk leaks and failures.",
            "Regulations specify hose standards.",
            "Proper installation extends hose life."
        ],
        resolution_strategy=(
            "Use certified hoses and follow installation procedures."
        ),
        entity_scope="All Hydraulic Brake Systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FMVSS 106 §5 Brake Hose"
    ),
    DoctrineBlock(
        topic="Brake System Electronic Control Unit (ECU) Software Validation",
        keywords=["ECU", "software validation", "functional safety", "testing", "verification"],
        conclusion_template=(
            "Validating brake system ECU software ensures functional safety and compliance with automotive standards."
        ),
        reasoning_framework=(
            "Brake ECUs control critical functions; software must be rigorously tested for faults and edge cases.\n\n"
            "Validation includes unit testing, integration testing, and hardware-in-the-loop simulations.\n\n"
            "Compliance with ISO 26262 functional safety standard is mandatory.\n\n"
            "The reasoning framework includes software engineering best practices, safety analysis, and regulatory compliance."
        ),
        key_factors=[
            "Software requirements specification",
            "Test coverage",
            "Fault injection testing",
            "Safety mechanism verification",
            "Documentation and traceability"
        ],
        primary_authority=[
            "ISO 26262 Functional Safety",
            "SAE J3061 Cybersecurity",
            "Automotive Software Engineering Texts",
            "FMVSS 126 Electronic Stability Control"
        ],
        burden_holder="ECU Software Developer",
        adversary_position=(
            "Some underestimate software validation complexity."
        ),
        counter_arguments=[
            "Inadequate validation risks safety-critical failures.",
            "Regulations require documented validation.",
            "Robust software improves system reliability."
        ],
        resolution_strategy=(
            "Implement comprehensive software validation processes."
        ),
        entity_scope="Brake System ECUs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 26262 §8 Software Validation"
    ),
    DoctrineBlock(
        topic="Brake System Hydraulic Pressure Modulator Design",
        keywords=["hydraulic modulator", "pressure modulation", "valve design", "response time", "control accuracy"],
        conclusion_template=(
            "Designing hydraulic pressure modulators with precise control and fast response improves ABS and ESC performance."
        ),
        reasoning_framework=(
            "Pressure modulators regulate brake line pressure to prevent wheel lockup or loss of control.\n\n"
            "Valve design affects modulation accuracy, response time, and reliability.\n\n"
            "Control algorithms coordinate valve actuation with sensor inputs.\n\n"
            "The reasoning framework includes fluid dynamics, valve engineering, and control systems."
        ),
        key_factors=[
            "Valve response time",
            "Pressure control accuracy",
            "Hydraulic fluid compatibility",
            "Reliability and durability",
            "Integration with control electronics"
        ],
        primary_authority=[
            "SAE J1703 Hydraulic Brake Systems",
            "Automotive Control Systems Texts",
            "FMVSS 135 Brake Performance",
            "Valve Manufacturer Specifications"
        ],
        burden_holder="Brake System Supplier",
        adversary_position=(
            "Some use lower precision modulators to reduce cost."
        ),
        counter_arguments=[
            "Poor modulation reduces safety and performance.",
            "High-quality modulators meet regulatory requirements.",
            "Investment in quality reduces warranty claims."
        ],
        resolution_strategy=(
            "Specify and test modulators to meet performance standards."
        ),
        entity_scope="ABS and ESC Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FMVSS 135 §5.3 Pressure Modulation"
    ),
    DoctrineBlock(
        topic="Brake System Pedal Travel Sensors and Calibration",
        keywords=["pedal travel sensor", "calibration", "brake-by-wire", "position sensing", "driver input"],
        conclusion_template=(
            "Accurate pedal travel sensing and calibration are essential for brake-by-wire system responsiveness and safety."
        ),
        reasoning_framework=(
            "Pedal travel sensors detect driver input position to modulate braking force electronically.\n\n"
            "Calibration ensures sensor output corresponds accurately to pedal position.\n\n"
            "Redundancy and fault detection improve reliability.\n\n"
            "The reasoning framework includes sensor technology, calibration procedures, and functional safety."
        ),
        key_factors=[
            "Sensor resolution and accuracy",
            "Calibration procedures",
            "Redundancy and diagnostics",
            "Signal processing",
            "Fail-safe operation"
        ],
        primary_authority=[
            "SAE J3132 Brake-by-Wire Systems",
            "ISO 26262 Functional Safety",
            "Automotive Sensor Standards",
            "Brake System Calibration Manuals"
        ],
        burden_holder="Brake System Supplier",
        adversary_position=(
            "Some underestimate calibration importance."
        ),
        counter_arguments=[
            "Accurate sensing is critical for system safety.",
            "Calibration reduces false inputs and failures.",
            "Regulations require sensor validation."
        ],
        resolution_strategy=(
            "Implement rigorous calibration and testing protocols."
        ),
        entity_scope="Brake-by-Wire Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 26262 §7 Sensor Validation"
    ),
    DoctrineBlock(
        topic="Brake System Hydraulic Reservoir Design and Venting",
        keywords=["hydraulic reservoir", "design", "venting", "fluid contamination", "pressure equalization"],
        conclusion_template=(
            "Proper hydraulic reservoir design with effective venting prevents fluid contamination and maintains system pressure."
        ),
        reasoning_framework=(
            "Reservoirs store brake fluid and accommodate volume changes due to temperature and wear.\n\n"
            "Venting prevents vacuum formation and allows pressure equalization.\n\n"
            "Design minimizes ingress of moisture and contaminants.\n\n"
            "The reasoning framework includes fluid dynamics, contamination control, and mechanical design."
        ),
        key_factors=[
            "Reservoir capacity",
            "Vent design and filtration",
            "Material compatibility",
            "Se