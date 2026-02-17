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
        topic="Hydraulic Power Steering Fluid Contamination",
        keywords=["hydraulic", "power steering", "fluid", "contamination", "debris", "viscosity", "seal damage"],
        conclusion_template="Contaminated hydraulic fluid leads to accelerated wear and seal failure in the power steering system.",
        reasoning_framework=(
            "Hydraulic power steering systems rely on clean, uncontaminated fluid to maintain proper lubrication and "
            "pressure transmission. Contaminants such as dirt, metal particles, or degraded additives increase fluid "
            "abrasiveness and reduce viscosity, which compromises the sealing surfaces and moving components. Over time, "
            "this leads to accelerated wear of the pump, valves, and rack seals, resulting in leaks and loss of steering "
            "performance. The presence of contamination is typically confirmed through fluid analysis and visual inspection. "
            "Preventative maintenance including fluid replacement and filtration is critical to system longevity."
        ),
        key_factors=[
            "Fluid cleanliness level",
            "Presence of particulate matter",
            "Fluid viscosity degradation",
            "Seal material compatibility",
            "Maintenance intervals",
            "Operating temperature range"
        ],
        primary_authority=[
            "SAE J2807 - Power Steering Fluid Contamination Standards",
            "ISO 4406 - Hydraulic Fluid Cleanliness Code",
            "Bosch Hydraulic Steering System Manuals"
        ],
        burden_holder="Maintenance and service personnel responsible for fluid replacement and inspection.",
        adversary_position="Contend that fluid contamination is negligible and does not significantly affect system longevity.",
        counter_arguments=[
            "Empirical data shows correlation between contamination levels and seal failure rates.",
            "Laboratory fluid analysis confirms presence of abrasive particles.",
            "Field failure reports link contamination to pump and rack damage."
        ],
        resolution_strategy="Implement mandatory fluid cleanliness checks and enforce replacement schedules based on contamination thresholds.",
        entity_scope="Automotive hydraulic power steering systems in passenger vehicles.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE Technical Paper 2018-01-1234 on Hydraulic Fluid Contamination Effects"
    ),
    DoctrineBlock(
        topic="Electric Power Steering Torque Sensor Drift",
        keywords=["electric power steering", "torque sensor", "drift", "calibration", "signal noise", "fault diagnosis"],
        conclusion_template="Torque sensor drift causes inaccurate steering assist levels, leading to degraded driver feedback and potential safety risks.",
        reasoning_framework=(
            "Electric Power Steering (EPS) systems depend on accurate torque sensor readings to modulate motor assist. "
            "Sensor drift, caused by thermal effects, aging, or electromagnetic interference, results in offset errors and "
            "signal noise. This leads to incorrect torque estimation and inappropriate assist torque application. "
            "Symptoms include inconsistent steering feel, increased driver effort, or unexpected steering behavior. "
            "Diagnosis involves sensor calibration checks, signal waveform analysis, and cross-referencing with vehicle speed "
            "and steering angle sensors. Corrective action requires recalibration or sensor replacement."
        ),
        key_factors=[
            "Sensor temperature sensitivity",
            "Signal offset magnitude",
            "Calibration procedure adherence",
            "Electromagnetic interference levels",
            "Steering system fault codes"
        ],
        primary_authority=[
            "ISO 26262 - Functional Safety for EPS Systems",
            "SAE J2945/1 - EPS Sensor Diagnostics",
            "Bosch EPS Sensor Calibration Guidelines"
        ],
        burden_holder="EPS system manufacturers and vehicle maintenance technicians.",
        adversary_position="Argue that sensor drift is within acceptable tolerances and does not impact safety.",
        counter_arguments=[
            "Field data shows drift exceeding specification limits.",
            "Driver complaints correlate with sensor offset events.",
            "Safety standards require precise torque sensing for fail-safe operation."
        ],
        resolution_strategy="Enforce periodic sensor calibration and implement real-time drift compensation algorithms.",
        entity_scope="Electric power steering systems in passenger and commercial vehicles.",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ISO 26262 Part 6, Clause 7.4 on Sensor Drift Management"
    ),
    DoctrineBlock(
        topic="Rack and Pinion Inner Tie Rod Wear",
        keywords=["rack and pinion", "inner tie rod", "wear", "steering play", "alignment", "component fatigue"],
        conclusion_template="Wear in the inner tie rod causes increased steering play and misalignment, compromising vehicle handling.",
        reasoning_framework=(
            "The inner tie rod connects the rack to the steering knuckle, transmitting steering input to the wheels. "
            "Wear occurs due to mechanical fatigue, corrosion, and contamination ingress into the ball joint. This results "
            "in increased free play, which manifests as loose steering feel and reduced directional control. "
            "Progressive wear can cause misalignment, uneven tire wear, and potential failure under load. "
            "Inspection includes checking for excessive movement, noise, and visual degradation. Replacement restores "
            "steering precision and safety."
        ),
        key_factors=[
            "Tie rod end ball joint condition",
            "Protective boot integrity",
            "Corrosion presence",
            "Steering play measurement",
            "Vehicle usage and mileage"
        ],
        primary_authority=[
            "SAE J670 - Steering System Component Wear",
            "OEM Service Manuals (e.g., Toyota, Ford, GM)",
            "NHTSA Steering Component Safety Guidelines"
        ],
        burden_holder="Vehicle owners and maintenance providers to perform timely inspections.",
        adversary_position="Claim that minor tie rod wear does not significantly affect steering safety or performance.",
        counter_arguments=[
            "Quantified steering play beyond manufacturer limits reduces control.",
            "Alignment data shows correlation with tie rod wear.",
            "Safety recalls have been issued for tie rod failures."
        ],
        resolution_strategy="Mandate periodic tie rod inspections and replacement when wear exceeds thresholds.",
        entity_scope="Passenger vehicle rack and pinion steering assemblies.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="NHTSA Recall 20V-123 on Tie Rod Failures"
    ),
    DoctrineBlock(
        topic="Ackermann Steering Geometry Principles",
        keywords=["Ackermann", "steering geometry", "turning radius", "wheel alignment", "cornering", "vehicle dynamics"],
        conclusion_template="Proper Ackermann geometry ensures optimal tire slip angles during cornering, enhancing handling and tire life.",
        reasoning_framework=(
            "Ackermann steering geometry is designed so that the inner and outer front wheels turn at different angles during a "
            "corner, allowing them to follow concentric circles. This reduces tire scrub and improves handling stability. "
            "Incorrect geometry leads to increased tire wear, reduced steering precision, and compromised vehicle dynamics. "
            "Design considerations include steering arm lengths, kingpin inclination, and track width. "
            "Verification is through alignment measurements and dynamic testing."
        ),
        key_factors=[
            "Steering arm length ratios",
            "Kingpin inclination angles",
            "Track width and wheelbase",
            "Tire slip angle measurements",
            "Vehicle speed and corner radius"
        ],
        primary_authority=[
            "SAE J670 - Steering Geometry Standards",
            "Vehicle Dynamics textbooks (Milliken & Milliken)",
            "OEM Chassis Design Manuals"
        ],
        burden_holder="Chassis engineers and alignment technicians.",
        adversary_position="Suggest that perfect Ackermann geometry is unnecessary due to modern electronic stability controls.",
        counter_arguments=[
            "Mechanical geometry remains fundamental for baseline handling.",
            "Electronic aids cannot fully compensate for poor mechanical alignment.",
            "Tire wear patterns confirm geometry effects."
        ],
        resolution_strategy="Incorporate Ackermann principles in design and maintain alignment within specified tolerances.",
        entity_scope="Steering systems of passenger and commercial vehicles.",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Milliken & Milliken, Vehicle Dynamics, 3rd Edition"
    ),
    DoctrineBlock(
        topic="Steer-by-Wire Redundancy Architecture",
        keywords=["steer-by-wire", "redundancy", "fail-safe", "electronic control", "backup systems", "safety"],
        conclusion_template="Redundancy in steer-by-wire systems is critical to ensure fail-safe operation and maintain steering control during faults.",
        reasoning_framework=(
            "Steer-by-wire systems eliminate mechanical linkages, relying entirely on electronic sensors, actuators, and control units. "
            "This architecture mandates multiple layers of redundancy including dual sensors, backup power supplies, and failover control algorithms. "
            "Redundancy mitigates risks from sensor failure, actuator faults, or software errors. "
            "Safety standards require continuous monitoring and immediate fallback to safe states. "
            "Testing involves fault injection, system diagnostics, and compliance with ISO 26262 functional safety requirements."
        ),
        key_factors=[
            "Number and diversity of sensors",
            "Backup actuator capability",
            "Power supply redundancy",
            "Fault detection and isolation algorithms",
            "Compliance with functional safety standards"
        ],
        primary_authority=[
            "ISO 26262 - Functional Safety for Road Vehicles",
            "SAE J3130 - Steer-by-Wire System Requirements",
            "Automotive Safety Integrity Level (ASIL) Guidelines"
        ],
        burden_holder="Steer-by-wire system designers and vehicle manufacturers.",
        adversary_position="Argue that redundancy increases system complexity and cost without proportional safety benefit.",
        counter_arguments=[
            "Safety standards mandate redundancy for critical systems.",
            "Historical failures of non-redundant systems demonstrate risk.",
            "Redundancy enables safe degradation modes."
        ],
        resolution_strategy="Design and validate multi-layer redundancy architectures and conduct rigorous safety assessments.",
        entity_scope="Steer-by-wire systems in passenger and commercial vehicles.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 26262 Part 3 and Part 6 on Redundancy and Safety Mechanisms"
    ),
    DoctrineBlock(
        topic="Steering Column Intermediate Shaft U-Joint Failure",
        keywords=["steering column", "intermediate shaft", "universal joint", "failure", "play", "noise", "steering loss"],
        conclusion_template="Failure of the intermediate shaft U-joint leads to increased steering play, noise, and potential loss of steering control.",
        reasoning_framework=(
            "The intermediate shaft connects the steering wheel to the steering gear, often incorporating universal joints (U-joints) "
            "to accommodate angular misalignment. Over time, U-joints can wear due to lack of lubrication, corrosion, or mechanical fatigue. "
            "Symptoms include clunking noises, increased steering free play, and in severe cases, complete disconnection causing steering loss. "
            "Inspection involves checking for axial and rotational play, visual signs of wear, and noise during steering input. "
            "Replacement of worn U-joints is critical to maintain steering integrity and safety."
        ),
        key_factors=[
            "U-joint lubrication condition",
            "Corrosion and contamination",
            "Steering play measurements",
            "Noise during steering input",
            "Vehicle mileage and usage conditions"
        ],
        primary_authority=[
            "SAE J670 - Steering System Component Wear",
            "OEM Repair Manuals (e.g., Honda, BMW)",
            "NHTSA Steering Safety Bulletins"
        ],
        burden_holder="Vehicle owners and service technicians.",
        adversary_position="Minimize the impact of minor U-joint wear on steering safety.",
        counter_arguments=[
            "Measured play exceeds manufacturer safety limits.",
            "Documented incidents of steering loss linked to U-joint failure.",
            "Safety recalls and service campaigns addressing this issue."
        ],
        resolution_strategy="Implement regular inspection intervals and replace U-joints showing wear or damage.",
        entity_scope="Steering column intermediate shafts in passenger vehicles.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NHTSA Recall 19V-456 on Steering Intermediate Shaft Failures"
    ),
    DoctrineBlock(
        topic="Power Steering Pump Flow and Pressure Testing",
        keywords=["power steering pump", "flow rate", "pressure testing", "pump efficiency", "hydraulic system diagnostics"],
        conclusion_template="Accurate flow and pressure testing of the power steering pump is essential to diagnose system performance and detect faults.",
        reasoning_framework=(
            "The power steering pump generates hydraulic pressure and flow to assist steering effort. "
            "Testing involves measuring output flow rate and pressure under various engine speeds and load conditions. "
            "Deviations from specified values indicate pump wear, internal leakage, or blockages. "
            "Proper test procedures require calibrated gauges, flow meters, and adherence to OEM test protocols. "
            "Results guide maintenance decisions such as pump replacement or system flushing."
        ),
        key_factors=[
            "Pump output pressure at idle and rated speed",
            "Flow rate under load",
            "Noise and vibration during operation",
            "Hydraulic fluid condition",
            "Test equipment calibration"
        ],
        primary_authority=[
            "SAE J2807 - Power Steering Test Procedures",
            "OEM Service Manuals (e.g., GM, Ford)",
            "Hydraulic Pump Manufacturer Guidelines"
        ],
        burden_holder="Service technicians performing diagnostics and repairs.",
        adversary_position="Suggest that pressure testing is unnecessary if steering assist feels normal.",
        counter_arguments=[
            "Subtle pump degradation may not be perceptible but affects longevity.",
            "Pressure testing detects early faults preventing catastrophic failure.",
            "OEM service bulletins recommend regular testing."
        ],
        resolution_strategy="Incorporate flow and pressure testing in routine maintenance and fault diagnosis.",
        entity_scope="Hydraulic power steering pumps in automotive applications.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2807 Test Methodology for Power Steering Pumps"
    ),
    DoctrineBlock(
        topic="Electric Power Steering Motor Current Draw Analysis",
        keywords=["electric power steering", "motor current", "current draw", "diagnostics", "load analysis", "fault detection"],
        conclusion_template="Analyzing EPS motor current draw patterns enables early detection of mechanical binding, electrical faults, and system inefficiencies.",
        reasoning_framework=(
            "The EPS motor current draw correlates directly with the load on the steering system. "
            "Abnormal current patterns such as spikes, sustained high current, or irregular fluctuations indicate mechanical binding, "
            "bearing wear, or electrical faults like short circuits or sensor errors. "
            "Data acquisition involves high-frequency current sensing and correlation with steering angle and vehicle speed. "
            "Trend analysis and threshold alarms facilitate predictive maintenance and fault isolation."
        ),
        key_factors=[
            "Current draw magnitude and waveform",
            "Steering angle and torque correlation",
            "Ambient temperature effects",
            "Motor winding resistance and health",
            "Vehicle speed and driving conditions"
        ],
        primary_authority=[
            "SAE J3130 - EPS Diagnostic Procedures",
            "ISO 26262 - Electrical System Safety",
            "Bosch EPS Motor Control Documentation"
        ],
        burden_holder="Vehicle diagnostics engineers and maintenance personnel.",
        adversary_position="Claim that current draw variations are normal and do not indicate faults.",
        counter_arguments=[
            "Statistical analysis shows deviation from baseline correlates with failures.",
            "Fault codes and driver complaints align with abnormal current patterns.",
            "OEM diagnostic protocols mandate current monitoring."
        ],
        resolution_strategy="Implement real-time current monitoring with diagnostic fault codes and maintenance alerts.",
        entity_scope="Electric power steering motors in automotive systems.",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SAE J3130 Diagnostic Framework for EPS Motor Current Analysis"
    ),
    DoctrineBlock(
        topic="Toe Angle and Tire Wear Correlation",
        keywords=["toe angle", "tire wear", "alignment", "steering geometry", "vehicle handling", "suspension"],
        conclusion_template="Incorrect toe angle settings accelerate tire wear and degrade vehicle handling stability.",
        reasoning_framework=(
            "Toe angle defines the relative orientation of the tires in the horizontal plane. "
            "Excessive toe-in or toe-out causes uneven tire wear patterns such as feathering or scalloping. "
            "Misalignment increases rolling resistance and reduces fuel efficiency. "
            "Proper toe settings optimize tire contact patch and improve directional stability. "
            "Measurement and adjustment require precision alignment equipment and adherence to manufacturer specifications."
        ),
        key_factors=[
            "Toe angle measurement accuracy",
            "Tire wear pattern analysis",
            "Vehicle speed and load conditions",
            "Suspension component condition",
            "Alignment adjustment procedures"
        ],
        primary_authority=[
            "SAE J670 - Wheel Alignment Standards",
            "Tire Industry Association Guidelines",
            "OEM Alignment Specifications"
        ],
        burden_holder="Alignment technicians and vehicle owners.",
        adversary_position="Downplay the impact of minor toe deviations on tire wear and handling.",
        counter_arguments=[
            "Empirical tire wear data shows accelerated degradation with toe misalignment.",
            "Handling tests demonstrate reduced stability.",
            "OEM maintenance schedules specify toe alignment checks."
        ],
        resolution_strategy="Enforce regular alignment inspections and corrections to maintain toe within specified limits.",
        entity_scope="Passenger and commercial vehicle steering and suspension systems.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Tire Industry Association Report on Alignment and Tire Wear"
    ),
    DoctrineBlock(
        topic="Rack and Pinion Hydraulic Seal Leak Diagnosis",
        keywords=["rack and pinion", "hydraulic seal", "leak", "fluid loss", "pressure drop", "steering performance"],
        conclusion_template="Hydraulic seal leaks in the rack and pinion assembly cause fluid loss, pressure drops, and degraded steering assist.",
        reasoning_framework=(
            "The rack and pinion hydraulic seals maintain fluid containment under high pressure. "
            "Seal degradation from wear, contamination, or chemical attack leads to leaks. "
            "Symptoms include visible fluid loss, reduced assist pressure, and increased steering effort. "
            "Diagnosis involves pressure testing, fluid level monitoring, and visual inspection of seal areas. "
            "Timely replacement of seals prevents further damage to the rack assembly and maintains steering system integrity."
        ),
        key_factors=[
            "Seal material compatibility",
            "Fluid contamination levels",
            "Operating pressure and temperature",
            "Visual inspection for leaks",
            "Steering assist pressure measurements"
        ],
        primary_authority=[
            "SAE J2807 - Hydraulic Seal Standards",
            "OEM Service Manuals",
            "Hydraulic Seal Manufacturer Technical Bulletins"
        ],
        burden_holder="Service technicians and vehicle maintenance personnel.",
        adversary_position="Argue that minor leaks are acceptable and do not affect performance.",
        counter_arguments=[
            "Pressure loss measurements confirm performance degradation.",
            "Leaks lead to contamination ingress and accelerated wear.",
            "Safety standards require leak-free steering systems."
        ],
        resolution_strategy="Implement seal inspection and replacement protocols based on leak detection thresholds.",
        entity_scope="Hydraulic rack and pinion steering assemblies.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2807 Hydraulic Seal Leak Test Procedures"
    ),
    DoctrineBlock(
        topic="Steering Angle Sensor Calibration Procedures",
        keywords=["steering angle sensor", "calibration", "alignment", "fault codes", "driver assistance systems"],
        conclusion_template="Accurate calibration of steering angle sensors is essential for correct operation of stability and driver assistance systems.",
        reasoning_framework=(
            "Steering angle sensors provide critical input to electronic stability control (ESC), traction control, and advanced driver assistance systems (ADAS). "
            "Mis-calibration leads to erroneous data, triggering fault codes and impairing system performance. "
            "Calibration procedures involve zero-point setting, alignment with wheel position, and validation through test drives. "
            "OEM-specific diagnostic tools and software are required to ensure sensor accuracy and system integration."
        ),
        key_factors=[
            "Sensor zero-point accuracy",
            "Alignment with steering wheel position",
            "Diagnostic fault code presence",
            "Software calibration tools",
            "Vehicle speed and yaw rate correlation"
        ],
        primary_authority=[
            "SAE J2945/1 - ESC and Sensor Calibration",
            "OEM Calibration Procedures",
            "ISO 26262 - Sensor Functional Safety"
        ],
        burden_holder="Service technicians performing sensor calibration and diagnostics.",
        adversary_position="Suggest that minor calibration errors do not affect system safety.",
        counter_arguments=[
            "ESC system performance is sensitive to sensor accuracy.",
            "Fault codes and system warnings arise from mis-calibration.",
            "Safety standards require precise sensor calibration."
        ],
        resolution_strategy="Follow OEM calibration protocols and verify sensor accuracy post-calibration.",
        entity_scope="Steering angle sensors in passenger vehicles with ESC and ADAS.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J2945/1 ESC Sensor Calibration Guidelines"
    ),
    DoctrineBlock(
        topic="Variable Ratio Steering Analysis",
        keywords=["variable ratio steering", "steering ratio", "handling", "steering effort", "vehicle dynamics"],
        conclusion_template="Variable ratio steering systems optimize steering response and effort across different driving conditions.",
        reasoning_framework=(
            "Variable ratio steering changes the steering gear ratio depending on the steering angle or vehicle speed. "
            "At low speeds, a higher ratio reduces steering effort and improves maneuverability. "
            "At high speeds, a lower ratio enhances stability and steering precision. "
            "Design involves cam profiles, rack tooth geometry, and electronic control integration. "
            "Analysis includes evaluating steering response curves, driver feedback, and system reliability."
        ),
        key_factors=[
            "Steering ratio variation range",
            "Cam or gear profile design",
            "Vehicle speed sensing accuracy",
            "Driver feedback and effort",
            "System durability and maintenance"
        ],
        primary_authority=[
            "SAE J670 - Steering System Design",
            "OEM Engineering Design Manuals",
            "Vehicle Dynamics Textbooks"
        ],
        burden_holder="Chassis and steering system engineers.",
        adversary_position="Claim that fixed ratio steering is sufficient for all driving conditions.",
        counter_arguments=[
            "Variable ratio improves maneuverability and safety.",
            "Driver comfort and control are enhanced with variable ratios.",
            "OEMs widely adopt variable ratio systems."
        ],
        resolution_strategy="Incorporate variable ratio designs and validate through simulation and road testing.",
        entity_scope="Steering systems in passenger vehicles.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J670 Steering System Variable Ratio Analysis"
    ),
    DoctrineBlock(
        topic="Power Steering Hose Pressure Rating and Failure",
        keywords=["power steering hose", "pressure rating", "hose failure", "leak", "burst", "material fatigue"],
        conclusion_template="Power steering hoses must meet pressure ratings to prevent leaks and catastrophic failures under operating conditions.",
        reasoning_framework=(
            "Power steering hoses convey high-pressure hydraulic fluid between pump, rack, and reservoir. "
            "Hoses must be rated for maximum system pressure plus safety margin. "
            "Failure modes include burst, abrasion, and material fatigue due to heat and vibration. "
            "Leaks cause fluid loss, pressure drops, and potential steering assist failure. "
            "Inspection involves pressure testing, visual checks for cracks or bulges, and replacement per OEM intervals."
        ),
        key_factors=[
            "Hose pressure rating vs system pressure",
            "Material compatibility with fluid",
            "Operating temperature and environment",
            "Visual condition and abrasion signs",
            "Installation routing and support"
        ],
        primary_authority=[
            "SAE J1401 - Hydraulic Brake and Steering Hose Standards",
            "OEM Service Manuals",
            "Hydraulic Hose Manufacturer Specifications"
        ],
        burden_holder="Maintenance personnel and vehicle owners.",
        adversary_position="Minimize importance of hose pressure rating in failure prevention.",
        counter_arguments=[
            "Pressure testing confirms hose integrity requirements.",
            "Failure analysis links burst hoses to inadequate ratings.",
            "Safety standards mandate hose specifications."
        ],
        resolution_strategy="Use hoses meeting or exceeding OEM pressure ratings and perform regular inspections.",
        entity_scope="Hydraulic power steering hose assemblies.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J1401 Hydraulic Hose Pressure and Safety Standards"
    ),
    DoctrineBlock(
        topic="EPS Motor Position Sensor Hall Effect Failure",
        keywords=["EPS", "motor position sensor", "Hall effect sensor", "failure", "signal loss", "steering assist"],
        conclusion_template="Failure of the EPS motor position Hall effect sensor results in loss of accurate motor control and impaired steering assist.",
        reasoning_framework=(
            "EPS motors use Hall effect sensors to detect rotor position for precise commutation. "
            "Sensor failure due to electrical faults, contamination, or mechanical damage causes incorrect or lost position signals. "
            "This leads to erratic motor behavior, reduced assist, or system shutdown. "
            "Diagnosis includes sensor signal waveform analysis, resistance checks, and fault code retrieval. "
            "Replacement or repair restores system function and safety."
        ),
        key_factors=[
            "Sensor signal integrity",
            "Electrical continuity and resistance",
            "Contamination and physical damage",
            "Fault code presence",
            "Motor control unit diagnostics"
        ],
        primary_authority=[
            "SAE J3130 - EPS Sensor Diagnostics",
            "Hall Effect Sensor Manufacturer Datasheets",
            "OEM EPS System Repair Manuals"
        ],
        burden_holder="Vehicle maintenance technicians and EPS system manufacturers.",
        adversary_position="Claim sensor failures are rare and do not significantly impact system safety.",
        counter_arguments=[
            "Field failure data shows sensor faults cause assist loss.",
            "Safety standards require sensor redundancy or fault detection.",
            "OEM recalls and service bulletins address sensor issues."
        ],
        resolution_strategy="Implement sensor health monitoring and timely replacement upon fault detection.",
        entity_scope="Electric power steering motor position sensing systems.",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ISO 26262 Functional Safety Requirements for EPS Sensors"
    ),
    DoctrineBlock(
        topic="Kingpin Inclination and Scrub Radius Effects",
        keywords=["kingpin inclination", "scrub radius", "steering geometry", "vehicle stability", "tire wear"],
        conclusion_template="Proper kingpin inclination and scrub radius settings optimize steering effort, reduce tire wear, and enhance vehicle stability.",
        reasoning_framework=(
            "Kingpin inclination (KPI) is the angle of the steering axis relative to vertical, affecting camber and steering effort. "
            "Scrub radius is the horizontal distance between the tire contact patch center and the steering axis intersection with the ground. "
            "Correct KPI and scrub radius reduce steering torque, improve self-centering, and minimize tire scrub during turns. "
            "Incorrect settings cause increased steering effort, uneven tire wear, and instability. "
            "Measurement and adjustment require precise alignment tools and adherence to OEM specifications."
        ),
        key_factors=[
            "Kingpin inclination angle",
            "Scrub radius measurement",
            "Steering effort and feedback",
            "Tire wear patterns",
            "Suspension geometry and compliance"
        ],
        primary_authority=[
            "SAE J670 - Steering Geometry",
            "Vehicle Dynamics Textbooks",
            "OEM Alignment Specifications"
        ],
        burden_holder="Chassis engineers and alignment technicians.",
        adversary_position="Downplay the impact of scrub radius on handling and tire wear.",
        counter_arguments=[
            "Empirical data links scrub radius to steering effort and tire wear.",
            "Driver feedback confirms handling differences.",
            "OEM designs optimize these parameters for safety."
        ],
        resolution_strategy="Maintain kingpin inclination and scrub radius within OEM tolerances through precise alignment.",
        entity_scope="Steering and suspension systems of passenger vehicles.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Milliken & Milliken Vehicle Dynamics, Steering Geometry Chapter"
    ),
    DoctrineBlock(
        topic="Steering Column Tilt and Telescoping Mechanism Failure",
        keywords=["steering column", "tilt mechanism", "telescoping", "failure", "play", "noise", "adjustment"],
        conclusion_template="Failure of the steering column tilt or telescoping mechanism causes excessive play, noise, and compromised driver control.",
        reasoning_framework=(
            "Tilt and telescoping mechanisms allow driver adjustment of steering wheel position. "
            "Failures arise from worn locking components, broken detents, or corrosion. "
            "Symptoms include looseness, rattling noises, and inability to maintain set position. "
            "Inspection involves checking for excessive movement, visual damage, and proper locking function. "
            "Repair or replacement restores driver comfort and safety."
        ),
        key_factors=[
            "Locking mechanism integrity",
            "Wear of detents and gears",
            "Corrosion and contamination",
            "Steering column play measurement",
            "Driver adjustment feedback"
        ],
        primary_authority=[
            "OEM Repair Manuals",
            "SAE J670 - Steering Column Standards",
            "NHTSA Safety Bulletins"
        ],
        burden_holder="Vehicle owners and service technicians.",
        adversary_position="Minimize impact of minor tilt mechanism play on safety.",
        counter_arguments=[
            "Excessive play reduces driver control.",
            "Noise and distraction affect driver concentration.",
            "OEM guidelines specify maximum allowable play."
        ],
        resolution_strategy="Regular inspection and timely repair or replacement of faulty components.",
        entity_scope="Steering columns in passenger vehicles.",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NHTSA Safety Bulletin on Steering Column Adjustment Failures"
    ),
    DoctrineBlock(
        topic="Active Return-to-Center Steering Analysis",
        keywords=["active return-to-center", "steering system", "control algorithms", "driver feedback", "vehicle stability"],
        conclusion_template="Active return-to-center steering systems enhance vehicle stability by automatically correcting steering angle after turns.",
        reasoning_framework=(
            "Active return-to-center systems use sensors and actuators to apply torque that assists the driver in returning the steering wheel "
            "to the neutral position after cornering. This reduces driver effort and improves vehicle stability during lane changes and curves. "
            "Control algorithms consider vehicle speed, steering angle, and lateral acceleration. "
            "System performance is validated through dynamic testing and driver feedback evaluation."
        ),
        key_factors=[
            "Steering angle sensor accuracy",
            "Actuator response time",
            "Control algorithm tuning",
            "Driver feedback and acceptance",
            "System fault detection"
        ],
        primary_authority=[
            "SAE J3130 - Advanced Steering Systems",
            "OEM System Design Documents",
            "Vehicle Dynamics Research Papers"
        ],
        burden_holder="Steering system designers and vehicle manufacturers.",
        adversary_position="Argue that passive return-to-center mechanisms are sufficient.",
        counter_arguments=[
            "Active systems provide improved response and reduced driver fatigue.",
            "Dynamic testing shows enhanced stability with active return.",
            "OEMs increasingly adopt active systems."
        ],
        resolution_strategy="Develop and validate active return-to-center control strategies with robust fault management.",
        entity_scope="Active steering systems in passenger vehicles.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J3130 on Active Steering Control Systems"
    ),
    DoctrineBlock(
        topic="Rack and Pinion Mounting Bushing Wear",
        keywords=["rack and pinion", "mounting bushing", "wear", "steering play", "noise", "alignment"],
        conclusion_template="Wear of rack and pinion mounting bushings causes increased steering play, noise, and potential misalignment.",
        reasoning_framework=(
            "Mounting bushings secure the rack and pinion assembly to the vehicle frame, absorbing vibrations and maintaining alignment. "
            "Wear or deterioration due to age, heat, or contamination leads to looseness and movement under load. "
            "This manifests as steering play, clunking noises, and inconsistent steering response. "
            "Inspection includes visual checks, measurement of play, and noise detection during steering input. "
            "Replacement of worn bushings restores steering precision and reduces noise."
        ),
        key_factors=[
            "Bushing material condition",
            "Mounting bracket integrity",
            "Steering play measurement",
            "Noise during steering operation",
            "Vehicle mileage and operating conditions"
        ],
        primary_authority=[
            "SAE J670 - Steering System Component Wear",
            "OEM Repair Manuals",
            "NHTSA Safety Bulletins"
        ],
        burden_holder="Vehicle maintenance providers.",
        adversary_position="Minimize effect of bushing wear on steering safety.",
        counter_arguments=[
            "Measured play exceeds safety thresholds.",
            "Noise and handling complaints correlate with bushing wear.",
            "OEM service bulletins recommend replacement."
        ],
        resolution_strategy="Regular inspection and replacement of mounting bushings per maintenance schedule.",
        entity_scope="Rack and pinion steering assemblies in passenger vehicles.",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="NHTSA Recall 18V-789 on Rack Mounting Bushing Failures"
    ),
    DoctrineBlock(
        topic="EPS Column-Assist vs Rack-Assist Architecture",
        keywords=["electric power steering", "column-assist", "rack-assist", "architecture", "performance", "design trade-offs"],
        conclusion_template="Column-assist and rack-assist EPS architectures offer distinct advantages and trade-offs in performance and packaging.",
        reasoning_framework=(
            "Column-assist EPS places the electric motor on the steering column, providing compact design and ease of integration. "
            "Rack-assist EPS mounts the motor directly on the steering rack, offering more direct torque application and improved feedback. "
            "Column-assist systems typically have simpler mechanical linkages but may have reduced steering feel. "
            "Rack-assist systems provide better road feel and higher assist torque but are more complex and costly. "
            "Selection depends on vehicle size, packaging constraints, and desired steering characteristics."
        ),
        key_factors=[
            "Motor placement and integration",
            "Steering feedback quality",
            "Packaging and weight considerations",
            "Cost and complexity",
            "System reliability and maintenance"
        ],
        primary_authority=[
            "SAE J3130 - EPS System Architectures",
            "OEM Engineering Design Documents",
            "Vehicle Dynamics Research"
        ],
        burden_holder="Vehicle and EPS system designers.",
        adversary_position="Claim one architecture is universally superior.",
        counter_arguments=[
            "Trade-offs depend on vehicle application and design goals.",
            "Both architectures are widely used successfully.",
            "Customer preferences and cost influence choice."
        ],
        resolution_strategy="Evaluate application requirements and select architecture accordingly.",
        entity_scope="Electric power steering systems in passenger vehicles.",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SAE J3130 EPS Architecture Comparison Studies"
    ),
    DoctrineBlock(
        topic="Hydraulic Power Steering Pump Belt Failure Effects",
        keywords=["hydraulic power steering", "pump belt", "failure", "loss of assist", "noise", "engine accessory drive"],
        conclusion_template="Failure of the power steering pump drive belt results in immediate loss of steering assist and increased steering effort.",
        reasoning_framework=(
            "The power steering pump is driven by a belt connected to the engine accessory drive system. "
            "Belt failure due to wear, misalignment, or tension loss causes the pump to stop delivering hydraulic pressure. "
            "This leads to loss of power assist, making steering heavy and difficult, especially at low speeds. "
            "Additional symptoms include belt noise, engine accessory malfunction, and potential damage to belt-driven components. "
            "Inspection and maintenance of belt condition and tension are critical to prevent sudden failures."
        ),
        key_factors=[
            "Belt wear and cracking",
            "Tension and alignment",
            "Pulley condition",
            "Pump load and operating conditions",
            "Maintenance intervals"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2807 - Power Steering System Maintenance",
            "Belt Manufacturer Guidelines"
        ],
        burden_holder="Vehicle owners and maintenance technicians.",
        adversary_position="Argue that belt failure is rare and not critical to safety.",
        counter_arguments=[
            "Sudden loss of assist increases accident risk.",
            "OEMs recommend regular belt inspection.",
            "Field data shows belt failure incidents."
        ],
        resolution_strategy="Implement scheduled belt inspection and replacement protocols.",
        entity_scope="Hydraulic power steering pump drive systems.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2807 Maintenance Recommendations for Pump Drive Belts"
    ),
    DoctrineBlock(
        topic="Steering Wheel Vibration Diagnosis (Shimmy vs Shake)",
        keywords=["steering wheel", "vibration", "shimmy", "shake", "diagnosis", "wheel balance", "suspension"],
        conclusion_template="Differentiating between shimmy and shake vibrations is essential for accurate diagnosis and corrective action.",
        reasoning_framework=(
            "Shimmy is a low-frequency oscillation typically caused by wheel imbalance, tire defects, or suspension wear. "
            "Shake is a higher-frequency vibration often linked to brake rotor issues or driveline imbalance. "
            "Diagnosis involves frequency analysis, road testing, and component inspection. "
            "Correct identification guides targeted repairs such as wheel balancing, tire replacement, or suspension component servicing."
        ),
        key_factors=[
            "Vibration frequency and amplitude",
            "Vehicle speed correlation",
            "Wheel and tire condition",
            "Suspension and steering component wear",
            "Brake system condition"
        ],
        primary_authority=[
            "SAE J670 - Vibration Diagnosis",
            "Tire Industry Association",
            "OEM Service Manuals"
        ],
        burden_holder="Service technicians performing vibration diagnosis.",
        adversary_position="Confuse shimmy and shake symptoms leading to misdiagnosis.",
        counter_arguments=[
            "Proper diagnostic procedures distinguish vibration types.",
            "Targeted repairs improve customer satisfaction.",
            "OEM guidelines specify diagnostic protocols."
        ],
        resolution_strategy="Use frequency analysis tools and systematic inspection to differentiate and address vibration causes.",
        entity_scope="Steering and suspension systems of passenger vehicles.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J670 Vibration Diagnosis Procedures"
    ),
    DoctrineBlock(
        topic="Active Front Steering (AFS) Planetary Gear System",
        keywords=["active front steering", "planetary gear", "steering actuator", "torque transmission", "control system"],
        conclusion_template="The planetary gear system in AFS enables variable steering ratios and torque distribution for enhanced vehicle dynamics.",
        reasoning_framework=(
            "Active Front Steering systems use planetary gearsets to modulate steering input and provide variable steering ratios. "
            "The planetary gear mechanism allows the actuator to add or subtract torque from the driver input, enabling features like lane keeping and stability control. "
            "Design considerations include gear ratio selection, backlash minimization, and durability under cyclic loads. "
            "Control systems coordinate actuator commands with vehicle sensors to optimize steering response."
        ),
        key_factors=[
            "Planetary gear ratio and design",
            "Torque transmission efficiency",
            "Backlash and gear wear",
            "Actuator control precision",
            "Integration with vehicle dynamics control"
        ],
        primary_authority=[
            "SAE J3130 - Active Steering Systems",
            "OEM Engineering Design Documents",
            "Vehicle Dynamics Research Papers"
        ],
        burden_holder="Steering system designers and vehicle manufacturers.",
        adversary_position="Suggest simpler mechanical systems suffice for steering control.",
        counter_arguments=[
            "AFS provides superior handling and safety features.",
            "Planetary gear systems enable compact and efficient designs.",
            "OEM adoption of AFS is increasing."
        ],
        resolution_strategy="Design robust planetary gear systems and integrate with advanced control algorithms.",
        entity_scope="Active front steering systems in passenger vehicles.",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J3130 Active Steering Planetary Gear Analysis"
    ),
    DoctrineBlock(
        topic="Steering Gear Ratio Calculation and Effects",
        keywords=["steering gear ratio", "calculation", "steering effort", "vehicle handling", "response"],
        conclusion_template="Steering gear ratio directly influences steering effort, response speed, and vehicle handling characteristics.",
        reasoning_framework=(
            "The steering gear ratio defines how far the steering wheel must turn to achieve a given wheel turn angle. "
            "A higher ratio reduces steering effort but slows response, while a lower ratio increases responsiveness but requires more effort. "
            "Calculation involves measuring input and output shaft rotations and considering mechanical linkages. "
            "Design balances driver comfort, vehicle size, and intended use. "
            "Effects on handling are validated through dynamic testing and driver feedback."
        ),
        key_factors=[
            "Input to output shaft rotation ratio",
            "Steering effort measurements",
            "Vehicle speed and dynamics",
            "Driver feedback",
            "Mechanical linkage design"
        ],
        primary_authority=[
            "SAE J670 - Steering System Design",
            "Vehicle Dynamics Textbooks",
            "OEM Engineering Manuals"
        ],
        burden_holder="Chassis engineers and vehicle designers.",
        adversary_position="Claim gear ratio has minimal impact due to electronic assist.",
        counter_arguments=[
            "Mechanical ratio remains fundamental to steering feel.",
            "Electronic assist complements but does not replace mechanical design.",
            "Driver feedback confirms ratio influence."
        ],
        resolution_strategy="Calculate and optimize gear ratio for intended vehicle performance and driver comfort.",
        entity_scope="Steering gear systems in passenger vehicles.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Milliken & Milliken Vehicle Dynamics Steering Chapter"
    ),
    DoctrineBlock(
        topic="EPS Thermal Management and Overheating Protection",
        keywords=["electric power steering", "thermal management", "overheating", "motor temperature", "protection"],
        conclusion_template="Effective thermal management and overheating protection are essential to maintain EPS motor reliability and performance.",
        reasoning_framework=(
            "EPS motors generate heat during operation, especially under high load or continuous use. "
            "Thermal management includes heat sinks, cooling fans, and temperature sensors. "
            "Overheating can degrade motor windings, reduce efficiency, and cause system faults. "
            "Protection strategies involve thermal monitoring, derating assist levels, and fault shutdowns. "
            "Design validation includes thermal cycling tests and fault mode simulations."
        ),
        key_factors=[
            "Motor temperature sensor accuracy",
            "Cooling system effectiveness",
            "Thermal thresholds and fault logic",
            "Duty cycle and load profiles",
            "Ambient temperature conditions"
        ],
        primary_authority=[
            "ISO 26262 - Functional Safety",
            "SAE J3130 - EPS System Design",
            "Motor Manufacturer Thermal Guidelines"
        ],
        burden_holder="EPS system designers and vehicle manufacturers.",
        adversary_position="Minimize need for complex thermal management.",
        counter_arguments=[
            "Thermal faults cause field failures.",
            "Safety standards require thermal protection.",
            "OEMs implement robust thermal management."
        ],
        resolution_strategy="Integrate thermal sensors and control algorithms to prevent overheating.",
        entity_scope="Electric power steering systems.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 26262 Thermal Safety Requirements"
    ),
    DoctrineBlock(
        topic="Four-Wheel Steering (4WS) Rear Steering Control",
        keywords=["four-wheel steering", "rear steering", "control system", "vehicle dynamics", "stability"],
        conclusion_template="Rear wheel steering control in 4WS systems enhances maneuverability and stability across varying speeds.",
        reasoning_framework=(
            "Four-wheel steering systems actively control rear wheel angle to improve handling. "
            "At low speeds, rear wheels steer opposite to front wheels to reduce turning radius. "
            "At high speeds, rear wheels steer in the same direction to enhance stability. "
            "Control algorithms use vehicle speed, steering input, and yaw rate sensors to determine rear steering angle. "
            "System validation includes dynamic testing and driver feedback."
        ),
        key_factors=[
            "Rear steering actuator precision",
            "Control algorithm responsiveness",
            "Sensor accuracy (speed, yaw rate)",
            "Driver feedback and acceptance",
            "System fault detection"
        ],
        primary_authority=[
            "SAE J3130 - Advanced Steering Systems",
            "OEM 4WS System Design Documents",
            "Vehicle Dynamics Research"
        ],
        burden_holder="Vehicle manufacturers and system designers.",
        adversary_position="Claim 4WS complexity outweighs benefits.",
        counter_arguments=[
            "Improved maneuverability and safety demonstrated in tests.",
            "OEMs successfully deploy 4WS in production vehicles.",
            "Driver acceptance is high with proper tuning."
        ],
        resolution_strategy="Develop robust rear steering control with fail-safe features.",
        entity_scope="Four-wheel steering systems in passenger vehicles.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J3130 Four-Wheel Steering Control Studies"
    ),
    DoctrineBlock(
        topic="Steering Column Bearing Noise Diagnosis",
        keywords=["steering column", "bearing", "noise", "wear", "lubrication", "steering feel"],
        conclusion_template="Bearing noise in the steering column indicates wear or lubrication failure, affecting steering smoothness and safety.",
        reasoning_framework=(
            "Steering column bearings support rotational movement of the steering shaft. "
            "Wear or lack of lubrication causes noise such as grinding or creaking during steering input. "
            "Noise can lead to increased friction, steering effort, and eventual failure. "
            "Diagnosis involves auditory inspection, shaft play measurement, and lubrication checks. "
            "Replacement or lubrication restores smooth operation."
        ),
        key_factors=[
            "Bearing wear and damage",
            "Lubrication condition",
            "Shaft play and alignment",
            "Noise characteristics",
            "Vehicle usage and environment"
        ],
        primary_authority=[
            "OEM Repair Manuals",
            "SAE J670 - Steering System Maintenance",
            "NHTSA Safety Bulletins"
        ],
        burden_holder="Service technicians and vehicle owners.",
        adversary_position="Minimize noise as cosmetic issue.",
        counter_arguments=[
            "Noise indicates mechanical degradation.",
            "Increased steering effort affects safety.",
            "OEM guidelines require repair."
        ],
        resolution_strategy="Inspect and maintain steering column bearings regularly.",
        entity_scope="Steering columns in passenger vehicles.",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NHTSA Safety Bulletin on Steering Column Noise"
    ),
    DoctrineBlock(
        topic="Bump Steer Analysis and Correction",
        keywords=["bump steer", "steering geometry", "suspension travel", "alignment", "vehicle dynamics"],
        conclusion_template="Bump steer causes unintended steering input during suspension travel, which must be minimized through precise geometry and alignment.",
        reasoning_framework=(
            "Bump steer occurs when suspension movement causes changes in steering angle without driver input. "
            "It results from improper linkage geometry, worn components, or misalignment. "
            "Effects include vehicle instability, driver fatigue, and uneven tire wear. "
            "Analysis involves measuring toe changes during suspension travel and adjusting tie rod lengths, angles, and mounting points. "
            "Correction improves handling and safety."
        ),
        key_factors=[
            "Toe angle variation with suspension travel",
            "Tie rod length and angle",
            "Suspension geometry",
            "Component wear and play",
            "Alignment settings"
        ],
        primary_authority=[
            "SAE J670 - Steering and Suspension Geometry",
            "Vehicle Dynamics Textbooks",
            "OEM Alignment Procedures"
        ],
        burden_holder="Chassis engineers and alignment technicians.",
        adversary_position="Downplay bump steer impact on vehicle safety.",
        counter_arguments=[
            "Dynamic testing shows instability due to bump steer.",
            "Driver complaints correlate with bump steer symptoms.",
            "OEMs specify bump steer limits."
        ],
        resolution_strategy="Design and maintain suspension and steering geometry to minimize bump steer.",
        entity_scope="Passenger vehicle steering and suspension systems.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Milliken & Milliken Vehicle Dynamics Bump Steer Chapter"
    ),
    DoctrineBlock(
        topic="Hydraulic Power Steering Fluid Contamination - Particulate Effects",
        keywords=["hydraulic power steering", "fluid contamination", "particulates", "abrasion", "seal damage"],
        conclusion_template="Particulate contamination in hydraulic power steering fluid accelerates abrasion and seal damage, reducing system lifespan.",
        reasoning_framework=(
            "Particulates such as metal shavings, dirt, and degraded additives suspended in hydraulic fluid increase abrasive wear on pump components and seals. "
            "This contamination reduces fluid film thickness and causes micro-cutting of sealing surfaces. "
            "Over time, this leads to leaks, pressure loss, and component failure. "
            "Fluid analysis and filtration are critical to detect and mitigate particulate contamination."
        ),
        key_factors=[
            "Particulate size and concentration",
            "Filter efficiency",
            "Fluid change intervals",
            "Seal material hardness",
            "Operating pressure and temperature"
        ],
        primary_authority=[
            "ISO 4406 - Hydraulic Fluid Cleanliness",
            "SAE J2807 - Power Steering Fluid Standards",
            "OEM Maintenance Guidelines"
        ],
        burden_holder="Maintenance personnel responsible for fluid cleanliness.",
        adversary_position="Minimize impact of low-level particulates on system wear.",
        counter_arguments=[
            "Laboratory tests show increased wear with particulate presence.",
            "Field failures correlate with contamination levels.",
            "OEMs specify cleanliness standards."
        ],
        resolution_strategy="Implement filtration and fluid replacement schedules to maintain fluid cleanliness.",
        entity_scope="Hydraulic power steering systems.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 4406 Cleanliness Code Application"
    ),
    DoctrineBlock(
        topic="Electric Power Steering Sensor Fusion for Torque Estimation",
        keywords=["electric power steering", "sensor fusion", "torque estimation", "steering control", "fault tolerance"],
        conclusion_template="Combining multiple sensor inputs improves torque estimation accuracy and enhances EPS system fault tolerance.",
        reasoning_framework=(
            "EPS systems utilize inputs from torque sensors, steering angle sensors, and motor current sensors to estimate driver torque. "
            "Sensor fusion algorithms integrate these signals to provide robust and accurate torque estimation. "
            "This approach mitigates individual sensor errors and improves system responsiveness. "
            "Fault detection mechanisms identify sensor discrepancies and enable safe fallback modes."
        ),
        key_factors=[
            "Sensor accuracy and reliability",
            "Algorithm robustness",
            "Fault detection and isolation",
            "System latency",
            "Environmental noise"
        ],
        primary_authority=[
            "SAE J3130 - EPS Sensor Fusion",
            "ISO 26262 - Functional Safety",
            "OEM EPS System Design Documents"
        ],
        burden_holder="EPS system developers and vehicle manufacturers.",
        adversary_position="Rely on single sensor inputs for torque estimation.",
        counter_arguments=[
            "Sensor fusion improves accuracy and safety.",
            "Redundancy reduces risk of failure.",
            "OEMs adopt sensor fusion techniques."
        ],
        resolution_strategy="Implement multi-sensor fusion with fault management in EPS control units.",
        entity_scope="Electric power steering systems.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J3130 EPS Sensor Fusion Guidelines"
    ),
    DoctrineBlock(
        topic="Steering Column Energy Absorption in Collisions",
        keywords=["steering column", "energy absorption", "collisions", "safety", "deformation", "driver protection"],
        conclusion_template="Steering columns designed with energy absorption features reduce injury risk by deforming controllably during collisions.",
        reasoning_framework=(
            "Modern steering columns incorporate collapsible sections, energy-absorbing materials, and controlled deformation zones. "
            "These features dissipate kinetic energy during frontal impacts, reducing forces transmitted to the driver. "
            "Design validation includes crash testing, finite element analysis, and compliance with safety regulations. "
            "Proper maintenance ensures energy absorption features remain functional."
        ),
        key_factors=[
            "Column material properties",
            "Deformation zone design",
            "Crash test performance",
            "Maintenance and damage history",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 208 - Occupant Crash Protection",
            "SAE J670 - Steering Column Safety",
            "OEM Crash Test Reports"
        ],
        burden_holder="Vehicle manufacturers and safety engineers.",
        adversary_position="Minimize importance of energy absorption features.",
        counter_arguments=[
            "Crash data shows reduced injury with energy absorbing columns.",
            "Regulations mandate these features.",
            "OEMs design columns accordingly."
        ],
        resolution_strategy="Design, test, and maintain steering columns with effective energy absorption capabilities.",
        entity_scope="Steering columns in passenger vehicles.",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FMVSS 208 Steering Column Requirements"
    ),
    DoctrineBlock(
        topic="Steering Angle Sensor Redundancy and Fault Management",
        keywords=["steering angle sensor", "redundancy", "fault management", "ESC", "ADAS", "safety"],
        conclusion_template="Redundant steering angle sensors with fault management ensure reliable input for ESC and ADAS systems.",
        reasoning_framework=(
            "Critical safety systems rely on accurate steering angle data. "
            "Redundancy involves multiple sensors providing overlapping data streams. "
            "Fault management algorithms detect discrepancies and isolate faulty sensors, maintaining system integrity. "
            "Testing includes fault injection and validation of fail-safe responses."
        ),
        key_factors=[
            "Number of sensors and diversity",
            "Fault detection algorithms",
            "System response to sensor failure",
            "Calibration consistency",
            "Integration with vehicle safety systems"
        ],
        primary_authority=[
            "ISO 26262 - Functional Safety",
            "SAE J2945/1 - ESC Sensor Requirements",
            "OEM Safety System Design"
        ],
        burden_holder="Vehicle manufacturers and system designers.",
        adversary_position="Rely on single sensor without redundancy.",
        counter_arguments=[
            "Redundancy improves safety and reliability.",
            "Standards require redundant sensing for critical inputs.",
            "OEMs implement redundant sensor architectures."
        ],
        resolution_strategy="Design redundant sensor systems with robust fault management.",
        entity_scope="Steering angle sensing in safety-critical systems.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 26262 Steering Sensor Redundancy Requirements"
    ),
    DoctrineBlock(
        topic="Power Steering Pump Noise Diagnosis",
        keywords=["power steering pump", "noise", "whine", "cavitation", "bearing wear", "fluid condition"],
        conclusion_template="Power steering pump noise often indicates cavitation, bearing wear, or fluid contamination requiring diagnosis and repair.",
        reasoning_framework=(
            "Noises such as whining or groaning from the power steering pump can indicate cavitation caused by low fluid levels or air ingress. "
            "Bearing wear or damaged internal components also produce abnormal sounds. "
            "Fluid contamination exacerbates noise and wear. "
            "Diagnosis includes fluid level and condition checks, pressure testing, and pump inspection. "
            "Timely repair prevents further damage and steering failure."
        ),
        key_factors=[
            "Fluid level and quality",
            "Pump pressure and flow",
            "Noise frequency and characteristics",
            "Bearing condition",
            "System air ingress"
        ],
        primary_authority=[
            "SAE J2807 - Power Steering Diagnostics",
            "OEM Service Manuals",
            "Hydraulic Pump Manufacturer Guidelines"
        ],
        burden_holder="Service technicians and vehicle owners.",
        adversary_position="Attribute noise to normal operation.",
        counter_arguments=[
            "Noise correlates with pump wear and failure.",
            "OEMs specify noise limits and diagnostics.",
            "Field repairs confirm noise as fault indicator."
        ],
        resolution_strategy="Conduct thorough diagnostics and repair or replace faulty components.",
        entity_scope="Hydraulic power steering pumps.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2807 Power Steering Noise Diagnosis"
    ),
    DoctrineBlock(
        topic="Steering System Electronic Control Unit (ECU) Security",
        keywords=["steering ECU", "cybersecurity", "access control", "fault tolerance", "vehicle safety"],
        conclusion_template="Robust cybersecurity measures in steering ECUs prevent unauthorized access and ensure safe steering operation.",
        reasoning_framework=(
            "Modern steering systems employ ECUs for control and diagnostics. "
            "Cybersecurity threats include unauthorized access, data tampering, and denial of service. "
            "Security measures include encryption, authentication, intrusion detection, and fail-safe modes. "
            "Compliance with automotive cybersecurity standards is essential. "
            "Testing involves penetration testing and vulnerability assessments."
        ),
        key_factors=[
            "Access control mechanisms",
            "Data encryption standards",
            "Intrusion detection capabilities",
            "Fail-safe and fallback strategies",
            "Compliance with ISO/SAE 21434"
        ],
        primary_authority=[
            "ISO/SAE 21434 - Automotive Cybersecurity",
            "SAE J3061 - Cybersecurity Process",
            "OEM Security Policies"
        ],
        burden_holder="Vehicle manufacturers and ECU developers.",
        adversary_position="Underestimate cybersecurity risks in steering ECUs.",
        counter_arguments=[
            "Demonstrated vulnerabilities in automotive ECUs.",
            "Regulatory requirements for cybersecurity.",
            "OEMs implement comprehensive security frameworks."
        ],
        resolution_strategy="Integrate cybersecurity best practices in ECU design and maintenance.",
        entity_scope="Steering system electronic control units.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO/SAE 21434 Automotive Cybersecurity Standard"
    ),
    DoctrineBlock(
        topic="Steering System Noise, Vibration, and Harshness (NVH) Optimization",
        keywords=["steering system", "NVH", "noise", "vibration", "harshness", "driver comfort"],
        conclusion_template="Optimizing steering system NVH characteristics enhances driver comfort and perceived vehicle quality.",
        reasoning_framework=(
            "Steering system NVH arises from mechanical linkages, hydraulic components, and electric motors. "
            "Sources include gear mesh noise, fluid turbulence, and motor vibrations. "
            "Optimization involves component design, material selection, damping treatments, and control algorithms. "
            "Testing includes subjective driver evaluations and objective measurements using accelerometers and microphones."
        ),
        key_factors=[
            "Gear design and lubrication",
            "Hydraulic fluid properties",
            "Motor control smoothness",
            "Structural damping",
            "Driver feedback"
        ],
        primary_authority=[
            "SAE J670 - NVH in Steering Systems",
            "OEM Engineering Guidelines",
            "Vehicle Dynamics and NVH Textbooks"
        ],
        burden_holder="Steering system designers and vehicle manufacturers.",
        adversary_position="Minimize importance of NVH in steering systems.",
        counter_arguments=[
            "Driver comfort affects vehicle acceptance.",
            "OEMs prioritize NVH in design.",
            "NVH issues lead to warranty claims."
        ],
        resolution_strategy="Incorporate NVH considerations early in design and validate through testing.",
        entity_scope="Steering systems in passenger vehicles.",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J670 NVH Optimization Procedures"
    ),
    DoctrineBlock(
        topic="Steering System Lubrication Best Practices",
        keywords=["steering system", "lubrication", "maintenance", "wear prevention", "component longevity"],
        conclusion_template="Proper lubrication of steering system components reduces wear and extends system service life.",
        reasoning_framework=(
            "Lubrication minimizes friction and wear in moving parts such as bearings, joints, and gears. "
            "Selection of appropriate lubricants depends on operating temperature, load, and compatibility with materials. "
            "Regular maintenance includes inspection and replenishment or replacement of lubricants. "
            "Neglect leads to increased wear, noise, and potential failure."
        ),
        key_factors=[
            "Lubricant type and viscosity",
            "Application intervals",
            "Component compatibility",
            "Operating environment",
            "Contamination control"
        ],
        primary_authority=[
            "OEM Maintenance Manuals",
            "SAE J300 - Lubricant Viscosity Classification",
            "Lubricant Manufacturer Recommendations"
        ],
        burden_holder="Vehicle owners and maintenance personnel.",
        adversary_position="Underestimate importance of lubrication maintenance.",
        counter_arguments=[
            "Wear rates increase without proper lubrication.",
            "OEMs specify lubrication schedules.",
            "Field failures linked to lubrication neglect."
        ],
        resolution_strategy="Follow OEM lubrication schedules and use recommended products.",
        entity_scope="Steering system mechanical components.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J300 Lubrication Standards"
    ),
    DoctrineBlock(
        topic="Steering System Fault Code Interpretation and Resolution",
        keywords=["steering system", "fault codes", "diagnostics", "troubleshooting", "repair"],
        conclusion_template="Accurate interpretation of steering system fault codes enables efficient troubleshooting and repair.",
        reasoning_framework=(
            "Modern steering systems generate diagnostic trouble codes (DTCs) to indicate faults. "
            "Codes correspond to sensor failures, actuator issues, or communication errors. "
            "Proper interpretation requires understanding code definitions, freeze frame data, and system context. "
            "Resolution involves targeted testing, component replacement, or software updates."
        ),
        key_factors=[
            "DTC definitions and codes",
            "Diagnostic tool capabilities",
            "Freeze frame and live data",
            "System wiring and communication",
            "Repair procedures"
        ],
        primary_authority=[
            "SAE J2012 - Diagnostic Trouble Codes",
            "OEM Diagnostic Manuals",
            "OBD-II Standards"
        ],
        burden_holder="Service technicians and diagnostic specialists.",
        adversary_position="Misinterpret codes leading to unnecessary repairs.",
        counter_arguments=[
            "Following OEM diagnostic procedures improves accuracy.",
            "Training and tools reduce misdiagnosis.",
            "Proper interpretation reduces downtime."
        ],
        resolution_strategy="Use OEM tools and training to interpret and resolve steering system faults.",
        entity_scope="Steering system diagnostics in passenger vehicles.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J2012 Diagnostic Code Standards"
    ),
    DoctrineBlock(
        topic="Steering System Software Update and Calibration Management",
        keywords=["steering system", "software update", "calibration", "ECU", "maintenance"],
        conclusion_template="Regular software updates and calibration management ensure optimal steering system performance and safety.",
        reasoning_framework=(
            "Steering system ECUs require periodic software updates to fix bugs, improve algorithms, and add features. "
            "Calibration data ensures sensors and actuators operate within specifications. "
            "Updates and calibrations must follow OEM procedures to avoid introducing faults. "
            "Failure to update or calibrate can cause degraded performance or safety risks."
        ),
        key_factors=[
            "Software version control",
            "Calibration data accuracy",
            "Update procedures and tools",
            "Compatibility and validation",
            "Change management"
        ],
        primary_authority=[
            "OEM Software Management Policies",
            "ISO 26262 - Software Safety",
            "SAE J3130 - Steering System Software"
        ],
        burden_holder="Vehicle manufacturers and service providers.",
        adversary_position="Delay or avoid updates due to cost or complexity.",
        counter_arguments=[
            "Updates improve safety and functionality.",
            "OEMs provide critical fixes via updates.",
            "Calibration maintains system accuracy."
        ],
        resolution_strategy="Implement structured software update and calibration management processes.",
        entity_scope="Steering system ECUs and software.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 26262 Software Lifecycle Requirements"
    ),
    DoctrineBlock(
        topic="Steering System Environmental Impact on Component Durability",
        keywords=["steering system", "environmental factors", "corrosion", "temperature", "humidity", "durability"],
        conclusion_template="Environmental exposure significantly affects steering system component durability and maintenance requirements.",
        reasoning_framework=(
            "Exposure to moisture, salt, temperature extremes, and contaminants accelerates corrosion and material degradation. "
            "Components such as bushings, joints, and seals are particularly vulnerable. "
            "Protective coatings, material selection, and maintenance mitigate environmental impacts. "
            "Failure to address environmental factors leads to premature wear and safety issues."
        ),
        key_factors=[
            "Exposure to salt and moisture",
            "Temperature cycling",
            "Material corrosion resistance",
            "Protective coatings",
            "Maintenance frequency"
        ],
        primary_authority=[
            "OEM Corrosion Protection Guidelines",
            "SAE J670 - Environmental Effects on Steering",
            "Material Science Literature"
        ],
        burden_holder="Vehicle owners and maintenance personnel.",
        adversary_position="Underestimate environmental impact on steering components.",
        counter_arguments=[
            "Field data shows accelerated wear in harsh environments.",
            "OEMs recommend enhanced maintenance in such conditions.",
            "Corrosion leads to safety-critical failures."
        ],
        resolution_strategy="Apply protective measures and increase maintenance in adverse environments.",
        entity_scope="Steering system components exposed to environment.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J670 Environmental Durability Studies"
    ),
    DoctrineBlock(
        topic="Steering System Mechanical Backlash and Its Effects",
        keywords=["steering system", "mechanical backlash", "steering play", "response delay", "wear"],
        conclusion_template="Mechanical backlash in steering components causes steering play and delayed response, compromising vehicle control.",
        reasoning_framework=(
            "Backlash is the clearance between mating components allowing free movement before engagement. "
            "Excessive backlash arises from wear, manufacturing tolerances, or damage. "
            "It results in steering wheel free play, reduced precision, and delayed vehicle response. "
            "Measurement involves quantifying angular or linear movement under no load. "
            "Correction requires component replacement or adjustment."
        ),
        key_factors=[
            "Component wear levels",
            "Manufacturing tolerances",
            "Steering play measurement",
            "Driver feedback",
            "Maintenance history"
        ],
        primary_authority=[
            "SAE J670 - Steering System Standards",
            "OEM Repair Manuals",
            "Vehicle Dynamics Textbooks"
        ],
        burden_holder="Maintenance technicians and vehicle owners.",
        adversary_position="Minimize impact of minor backlash on safety.",
        counter_arguments=[
            "Excessive backlash reduces control and safety.",
            "OEMs specify maximum allowable backlash.",
            "Driver complaints correlate with backlash."
        ],
        resolution_strategy="Inspect and correct mechanical backlash within specified limits.",
        entity_scope="Steering system mechanical components.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J670 Steering Backlash Standards"
    ),
    DoctrineBlock(
        topic="Steering System Noise Diagnosis Using Frequency Analysis",
        keywords=["steering system", "noise", "frequency analysis", "diagnostics", "fault identification"],
        conclusion_template="Frequency analysis of steering system noise enables precise identification of fault sources.",
        reasoning_framework=(
            "Steering system noises have characteristic frequency signatures depending on source components. "
            "Using accelerometers and microphones, noise data is collected and analyzed in frequency domain. "
            "Patterns help distinguish between gear mesh noise, bearing defects, and hydraulic cavitation. "
            "Accurate diagnosis leads to targeted repairs and reduced diagnostic time."
        ),
        key_factors=[
            "Noise frequency spectrum",
            "Amplitude and harmonics",
            "Operating conditions during measurement",
            "Component fault signatures",
            "Diagnostic tool accuracy"
        ],
        primary_authority=[
            "SAE J670 - NVH Diagnostics",
            "OEM Diagnostic Procedures",
            "Acoustics Research Papers"
        ],
        burden_holder="Diagnostic engineers and service technicians.",
        adversary_position="Rely on subjective noise assessment.",
        counter_arguments=[
            "Objective frequency analysis improves diagnostic accuracy.",
            "OEMs incorporate frequency analysis in diagnostics.",
            "Reduced repair times and costs."
        ],
        resolution_strategy="Implement frequency analysis tools in steering system diagnostics.",
        entity_scope="Steering system NVH diagnostics.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J670 NVH Frequency Analysis Guidelines"
    ),
    DoctrineBlock(
        topic="Steering System Component Material Selection for Durability",
        keywords=["steering system", "material selection", "durability", "corrosion resistance", "fatigue strength"],
        conclusion_template="Selecting appropriate materials for steering components ensures durability and resistance to environmental and mechanical stresses.",
        reasoning_framework=(
            "Steering components are subject to cyclic loads, environmental exposure, and wear. "
            "Materials must have adequate fatigue strength, corrosion resistance, and compatibility with lubricants and fluids. "
            "Common materials include high-strength steels, aluminum alloys, and composites. "
            "Material selection impacts manufacturing cost, weight, and maintenance requirements."
        ),
        key_factors=[
            "Fatigue strength",
            "Corrosion resistance",
            "Weight and cost",
            "Manufacturing processes",
            "Compatibility with lubricants"
        ],
        primary_authority=[
            "Material Science Literature",
            "OEM Engineering Standards",
            "SAE J670 - Material Selection"
        ],
        burden_holder="Design engineers and material suppliers.",
        adversary_position="Prioritize cost over material performance.",
        counter_arguments=[
            "Material failures lead to safety risks and warranty costs.",
            "OEMs specify materials for critical components.",
            "Long-term durability justifies material investment."
        ],
        resolution_strategy="Select materials balancing performance, cost, and durability requirements.",
        entity_scope="Steering system components.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J670 Material Selection Guidelines"
    ),
    DoctrineBlock(
        topic="Steering System Assembly and Torque Specifications",
        keywords=["steering system", "assembly", "torque specifications", "fasteners", "safety"],
        conclusion_template="Adhering to specified torque values during steering system assembly ensures component integrity and safety.",
        reasoning_framework=(
            "Proper torque application on fasteners prevents loosening, deformation, or damage. "
            "Under-torquing leads to joint failure, while over-torquing causes thread stripping or component distortion. "
            "OEMs provide torque specifications for all steering system fasteners. "
            "Assembly procedures include torque sequence, use of calibrated tools, and verification."
        ),
        key_factors=[
            "Torque values and tolerances",
            "Fastener types and grades",
            "Assembly procedures",
            "Tool calibration",
            "Verification methods"
        ],
        primary_authority=[
            "OEM Assembly Manuals",
            "SAE J429 - Fastener Specifications",
            "Torque Tool Manufacturer Guidelines"
        ],
        burden_holder="Assembly technicians and quality control personnel.",
        adversary_position="Neglect torque specifications for expediency.",
        counter_arguments=[
            "Improper torque causes failures and safety risks.",
            "OEMs mandate torque adherence.",
            "Quality control detects torque deviations."
        ],
        resolution_strategy="Implement strict torque control and verification during assembly.",
        entity_scope="Steering system assembly processes.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J429 Fastener Torque Standards"
    ),
    DoctrineBlock(
        topic="Steering System Vibration Isolation Techniques",
        keywords=["steering system", "vibration isolation", "bushings", "dampers", "driver comfort"],
        conclusion_template="Effective vibration isolation in steering systems reduces transmitted vibrations, enhancing driver comfort and component longevity.",
        reasoning_framework=(
            "Vibrations from road irregularities and drivetrain are transmitted through steering components. "
            "Isolation techniques include elastomeric bushings, hydraulic dampers, and tuned mass dampers. "
            "Proper design balances isolation with steering precision and feedback. "
            "Testing involves vibration transmissibility measurements and subjective driver evaluations."
        ),
        key_factors=[
            "Isolation material properties",
            "Mounting configurations",
            "Frequency response",
            "Durability of isolators",
            "Impact on steering feel"
        ],
        primary_authority=[
            "SAE J670 - NVH and Vibration Control",
            "OEM Engineering Guidelines",
            "Vehicle Dynamics Textbooks"
        ],
        burden_holder="Steering system designers and vehicle manufacturers.",
        adversary_position="Prioritize steering feedback over vibration isolation.",
        counter_arguments=[
            "Excessive vibration reduces comfort and causes fatigue.",
            "OEMs balance isolation and feedback.",
            "Customer satisfaction improves with isolation."
        ],
        resolution_strategy="Incorporate vibration isolation components optimized for target frequencies.",
        entity_scope="Steering systems in passenger vehicles.",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J670 Vibration Isolation Studies"
    ),
    DoctrineBlock(
        topic="Steering System End-of-Line Testing Procedures",
        keywords=["steering system", "end-of-line testing", "quality control", "functional tests", "fault detection"],
        conclusion_template="Comprehensive end-of-line testing ensures steering system functionality and safety before vehicle delivery.",
        reasoning_framework=(
            "End-of-line testing includes mechanical, hydraulic, and electronic functional tests. "
            "Tests verify steering effort, response, sensor signals, and absence of leaks or noises. "
            "Automated test equipment and diagnostic tools detect faults early. "
            "Data logging and traceability support quality assurance and recall prevention."
        ),
        key_factors=[
            "Test coverage and procedures",
            "Equipment calibration",
            "Fault detection sensitivity",
            "Data management",
            "Operator training"
        ],
        primary_authority=[
            "OEM Quality Control Standards",
            "SAE J670 - Testing Procedures",
            "ISO 9001 - Quality Management"
        ],
        burden_holder="Manufacturers and quality assurance teams.",
        adversary_position="Reduce testing to save time and cost.",
        counter_arguments=[
            "Comprehensive testing reduces warranty costs.",
            "OEMs require full test coverage.",
            "Faults detected early prevent field failures."
        ],
        resolution_strategy="Implement robust end-of-line testing protocols with traceability.",
        entity_scope="Steering system manufacturing and assembly.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 9001 Quality Management Requirements"
    ),
    DoctrineBlock(
        topic="Steering System Maintenance Interval Optimization",
        keywords=["steering system", "maintenance interval", "service schedule", "component wear", "cost optimization"],
        conclusion_template="Optimizing maintenance intervals balances steering system reliability with service cost efficiency.",
        reasoning_framework=(
            "Maintenance intervals are based on component wear rates, operating conditions, and failure risk. "
            "Too frequent servicing increases cost without benefit; too infrequent risks failures. "
            "Data from field service, warranty claims, and laboratory testing inform interval optimization. "
            "Adaptive maintenance schedules consider vehicle usage and environment."
        ),
        key_factors=[
            "Component wear data",
            "Operating environment",
            "Failure modes and effects",
            "Service cost analysis",
            "Customer usage patterns"
        ],
        primary_authority=[
            "OEM Maintenance Guidelines",
            "SAE J670 - Maintenance Practices",
            "Reliability Engineering Literature"
        ],
        burden_holder="Vehicle manufacturers and service providers.",
        adversary_position="Apply fixed intervals regardless of usage.",
        counter_arguments=[
            "Adaptive intervals improve reliability and reduce cost.",
            "Field data supports variable maintenance needs.",
            "OEMs increasingly adopt condition-based maintenance."
        ],
        resolution_strategy="Develop and implement adaptive maintenance schedules based on data analytics.",
        entity_scope="Steering system maintenance planning.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J670 Maintenance Interval Studies"
    ),
    DoctrineBlock(
        topic="Steering System Failure Mode and Effects Analysis (FMEA)",
        keywords=["steering system", "FMEA", "failure modes", "risk assessment", "mitigation"],
        conclusion_template="Conducting FMEA identifies potential steering system failures and guides risk mitigation strategies.",
        reasoning_framework=(
            "FMEA systematically evaluates possible failure modes, their causes, effects, and severity. "
            "It prioritizes risks based on occurrence, detection, and impact. "
            "Results inform design improvements, testing focus, and maintenance planning. "
            "FMEA is integral to functional safety and quality management."
        ),
        key_factors=[
            "Identification of failure modes",
            "Risk priority number calculation",
            "Mitigation actions",
            "Design and process improvements",
            "Documentation and review"
        ],
        primary_authority=[
            "AIAG FMEA Handbook",
            "ISO 26262 - Functional Safety",
            "OEM Quality Management Standards"
        ],
        burden_holder="Design engineers and quality teams.",
        adversary_position="Neglect FMEA or perform superficially.",
        counter_arguments=[
            "FMEA reduces failures and recalls.",
            "Regulatory compliance requires FMEA.",
            "OEMs mandate thorough FMEA."
        ],