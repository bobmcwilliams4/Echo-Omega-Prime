from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="Centrifugal Pump Specific Speed Selection",
        keywords=["specific speed", "centrifugal pump", "Ns", "impeller type", "performance"],
        conclusion_template="For the given flow and head, select a pump with a specific speed (Ns) that optimizes efficiency and stability.",
        reasoning_framework="""Evaluate the required flow rate (Q) and head (H) for the application. Calculate the specific speed (Ns) using the formula Ns = N * sqrt(Q) / H^0.75, where N is the pump speed in RPM. Compare the calculated Ns to standard ranges for radial, mixed, and axial flow impellers. Select an impeller type that matches the calculated Ns, ensuring the pump operates within its best efficiency range. Consider the effects of viscosity, suction conditions, and system variability. Validate selection against manufacturer curves and industry guidelines (e.g., Hydraulic Institute, API 610).""",
        key_factors=["Flow rate", "Head", "Pump speed", "Impeller geometry", "Fluid viscosity", "System curve"],
        primary_authority=["Hydraulic Institute Standards", "API 610", "Pump Manufacturer Data"],
        burden_holder="Pump System Designer",
        adversary_position="Selection based solely on availability or cost, disregarding specific speed implications.",
        counter_arguments=[
            "Ignoring specific speed can lead to inefficient operation and increased risk of cavitation.",
            "Selecting a pump outside its optimal Ns range may result in instability and premature failure."
        ],
        resolution_strategy="Require calculation and documentation of specific speed during design review. Cross-check with manufacturer recommendations and industry standards.",
        entity_scope="Centrifugal Pump Selection for MECH01_pump_systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 6.1.2; Hydraulic Institute Standards 1.3.2"
    ),
    DoctrineBlock(
        topic="NPSH Calculations and Cavitation Prevention",
        keywords=["NPSH", "Net Positive Suction Head", "cavitation", "pump suction", "vapor pressure"],
        conclusion_template="Ensure NPSHa exceeds NPSHr by a minimum margin to prevent cavitation in the pump.",
        reasoning_framework="""Calculate Net Positive Suction Head Available (NPSHa) by accounting for atmospheric pressure, static head, fluid vapor pressure, friction losses, and elevation. Obtain Net Positive Suction Head Required (NPSHr) from the pump manufacturer at the operating point. Ensure NPSHa exceeds NPSHr by at least 0.5–1.0 m (or as per API 610 recommendations) to provide a safety margin. Consider fluid temperature, altitude, and transient conditions. Address deficiencies by increasing suction head, reducing losses, or selecting a pump with lower NPSHr. Document calculations and verify during commissioning.""",
        key_factors=["Atmospheric pressure", "Fluid temperature", "Suction line losses", "Pump NPSHr", "Vapor pressure"],
        primary_authority=["API 610", "Hydraulic Institute Standards", "Pump Manufacturer Curves"],
        burden_holder="System Engineer",
        adversary_position="Assuming NPSHa is always sufficient without calculation or margin.",
        counter_arguments=[
            "Transient conditions (e.g., startup, shutdown) can reduce NPSHa below safe limits.",
            "Ignoring NPSH margins increases risk of cavitation, leading to impeller damage."
        ],
        resolution_strategy="Mandate NPSH calculations for all pump installations. Require documented margin and periodic review.",
        entity_scope="All MECH01_pump_systems installations",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 6.3.2; HI 9.6.1"
    ),
    DoctrineBlock(
        topic="Pump Affinity Laws",
        keywords=["affinity laws", "speed", "impeller diameter", "flow", "head", "power"],
        conclusion_template="Apply pump affinity laws to predict changes in flow, head, and power with speed or impeller diameter adjustments.",
        reasoning_framework="""Use the affinity laws: Q2/Q1 = N2/N1 (flow varies linearly with speed), H2/H1 = (N2/N1)^2 (head varies with square of speed), and P2/P1 = (N2/N1)^3 (power varies with cube of speed). For impeller diameter changes, similar relationships apply. Validate predictions with manufacturer data. Consider limits imposed by NPSH, system curve, and mechanical constraints. Document all calculations and verify against actual performance post-modification.""",
        key_factors=["Pump speed", "Impeller diameter", "System curve", "NPSH", "Power availability"],
        primary_authority=["Hydraulic Institute Standards", "Pump Manufacturer Manuals"],
        burden_holder="Pump System Analyst",
        adversary_position="Assuming linear relationships for all parameters or ignoring system curve effects.",
        counter_arguments=[
            "Affinity laws are idealized; actual performance may deviate due to hydraulic losses.",
            "Ignoring NPSH or power limits can result in unsafe operation."
        ],
        resolution_strategy="Require validation of affinity law predictions with actual data and system modeling.",
        entity_scope="MECH01_pump_systems modifications",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 1.3.3; API 610 Section 6.1.4"
    ),
    DoctrineBlock(
        topic="Pump Curve Analysis - Operating Point Determination",
        keywords=["pump curve", "system curve", "operating point", "flow", "head"],
        conclusion_template="Determine the pump operating point by intersecting the pump and system curves.",
        reasoning_framework="""Plot the pump performance curve (head vs. flow) provided by the manufacturer. Superimpose the system curve, representing the relationship between head and flow imposed by the piping and process. The intersection defines the operating point (actual flow and head delivered). Analyze the proximity to the Best Efficiency Point (BEP) and check for potential issues such as operation near shutoff or runout. Adjust system or pump selection as needed to ensure stable and efficient operation. Document findings and recommendations.""",
        key_factors=["Pump curve", "System curve", "BEP", "Flow demand", "Process variability"],
        primary_authority=["Pump Manufacturer Data", "Hydraulic Institute Standards"],
        burden_holder="Design Engineer",
        adversary_position="Operating pumps at points far from BEP or without system curve analysis.",
        counter_arguments=[
            "Operating away from BEP increases vibration, reduces efficiency, and shortens pump life.",
            "Failure to analyze system curve can lead to mismatched pump selection."
        ],
        resolution_strategy="Require documented curve analysis for all new and modified pump installations.",
        entity_scope="MECH01_pump_systems design and commissioning",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 9.6.3; API 610 Section 6.1.7"
    ),
    DoctrineBlock(
        topic="Positive Displacement Pump Selection - Reciprocating vs Rotary",
        keywords=["positive displacement", "reciprocating pump", "rotary pump", "selection criteria"],
        conclusion_template="Select reciprocating or rotary positive displacement pumps based on fluid properties, pressure, and pulsation requirements.",
        reasoning_framework="""Evaluate the application requirements: flow rate, discharge pressure, fluid viscosity, solids content, and pulsation tolerance. Reciprocating pumps are preferred for high pressure, low flow, and precise metering, but produce pulsating flow. Rotary pumps are suitable for moderate pressure, higher flow, and viscous fluids, with smoother output. Consider maintenance, efficiency, and compatibility with process control. Reference API 674 for reciprocating and API 676 for rotary pumps. Document selection rationale and verify with manufacturer recommendations.""",
        key_factors=["Discharge pressure", "Flow rate", "Fluid viscosity", "Pulsation sensitivity", "Solids content"],
        primary_authority=["API 674", "API 676", "Pump Manufacturer Data"],
        burden_holder="Process Engineer",
        adversary_position="Selecting pump type based solely on cost or availability.",
        counter_arguments=[
            "Improper selection can lead to excessive maintenance, process instability, or equipment failure.",
            "Ignoring pulsation effects may necessitate additional dampening equipment."
        ],
        resolution_strategy="Require application-specific selection matrix and peer review.",
        entity_scope="Positive displacement pumps in MECH01_pump_systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 674 Section 5; API 676 Section 4"
    ),
    DoctrineBlock(
        topic="Pump Materials Selection - Metallurgy",
        keywords=["materials selection", "corrosion", "erosion", "metallurgy", "pump construction"],
        conclusion_template="Select pump materials based on fluid corrosivity, erosion potential, and mechanical requirements.",
        reasoning_framework="""Assess the chemical composition, temperature, and abrasiveness of the pumped fluid. Reference corrosion resistance charts and consult with materials engineers. For corrosive fluids, consider stainless steels, duplex alloys, or non-metallic materials. For abrasive service, utilize hard coatings or wear-resistant alloys. Ensure compatibility with mechanical seals and gaskets. Reference API 610 material tables and manufacturer recommendations. Document selection and provide justification in design documentation.""",
        key_factors=["Fluid composition", "Temperature", "Abrasiveness", "Corrosion resistance", "Mechanical strength"],
        primary_authority=["API 610", "NACE MR0175", "Pump Manufacturer Data"],
        burden_holder="Materials Engineer",
        adversary_position="Selecting materials based solely on cost or standard practice.",
        counter_arguments=[
            "Inadequate materials selection can lead to rapid failure and safety hazards.",
            "Over-specification increases cost without added benefit."
        ],
        resolution_strategy="Require corrosion/erosion analysis and documented materials selection review.",
        entity_scope="All pump installations in MECH01_pump_systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 6.5; NACE MR0175"
    ),
    DoctrineBlock(
        topic="Mechanical Seal Selection and Flush Plans",
        keywords=["mechanical seal", "seal plan", "API seal plans", "flush", "leakage"],
        conclusion_template="Select mechanical seal type and flush plan based on process fluid, pressure, and temperature.",
        reasoning_framework="""Identify process fluid properties, including temperature, pressure, and chemical compatibility. Refer to API 682 for seal type selection (single, double, cartridge) and appropriate flush plan (Plan 11, 21, 23, etc.). Ensure seal materials are compatible with process fluid and that flush plan provides adequate cooling and lubrication. Consider environmental regulations regarding leakage. Document seal and flush plan selection, and review with reliability and process safety teams.""",
        key_factors=["Process fluid", "Pressure", "Temperature", "Seal material compatibility", "Environmental regulations"],
        primary_authority=["API 682", "Pump Manufacturer Data"],
        burden_holder="Reliability Engineer",
        adversary_position="Using default seal plans without consideration of process specifics.",
        counter_arguments=[
            "Improper seal or flush plan selection can result in leakage, environmental violations, or seal failure.",
            "Overly complex flush plans increase maintenance burden."
        ],
        resolution_strategy="Require seal selection worksheet and cross-functional review.",
        entity_scope="Centrifugal and positive displacement pumps in MECH01_pump_systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 682 Section 4; API 610 Section 7.3"
    ),
    DoctrineBlock(
        topic="Pump Bearing Selection - Radial vs Thrust Loads",
        keywords=["bearing selection", "radial load", "thrust load", "bearing life", "lubrication"],
        conclusion_template="Select bearing types and arrangements to accommodate both radial and thrust loads as per application requirements.",
        reasoning_framework="""Analyze pump hydraulic and mechanical loads to determine radial and thrust forces on bearings. Consult manufacturer data for recommended bearing types (ball, roller, angular contact, thrust). Ensure bearing life meets or exceeds design requirements (typically L10 > 25,000 hours). Consider lubrication method (grease, oil bath, forced lubrication) and environmental conditions. Reference API 610 and manufacturer guidelines. Document bearing selection and maintenance plan.""",
        key_factors=["Hydraulic loads", "Mechanical loads", "Bearing type", "Lubrication", "Operating environment"],
        primary_authority=["API 610", "Pump Manufacturer Data"],
        burden_holder="Mechanical Engineer",
        adversary_position="Selecting bearings based solely on catalog ratings without load analysis.",
        counter_arguments=[
            "Ignoring thrust loads can lead to premature bearing failure.",
            "Improper lubrication selection increases maintenance and failure risk."
        ],
        resolution_strategy="Mandate bearing load calculations and peer review for all pump designs.",
        entity_scope="MECH01_pump_systems rotating equipment",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 7.1; HI 9.6.5"
    ),
    DoctrineBlock(
        topic="Pump Vibration Analysis and Diagnostics",
        keywords=["vibration", "diagnostics", "condition monitoring", "predictive maintenance", "ISO 10816"],
        conclusion_template="Implement vibration monitoring and diagnostics to detect and address pump faults proactively.",
        reasoning_framework="""Establish baseline vibration levels for each pump using ISO 10816 standards. Install vibration sensors at bearing housings and critical points. Monitor for increases in amplitude or changes in frequency spectrum, indicating imbalance, misalignment, bearing wear, or hydraulic issues. Analyze data trends and correlate with maintenance records. Schedule corrective actions based on severity and root cause analysis. Document findings and update maintenance procedures accordingly.""",
        key_factors=["Vibration amplitude", "Frequency spectrum", "Baseline data", "Maintenance records", "ISO standards"],
        primary_authority=["ISO 10816", "Pump Manufacturer Guidelines"],
        burden_holder="Maintenance Engineer",
        adversary_position="Relying solely on periodic manual inspections or ignoring vibration data.",
        counter_arguments=[
            "Unmonitored vibration increases risk of catastrophic failure.",
            "Manual inspections may miss early warning signs."
        ],
        resolution_strategy="Mandate continuous vibration monitoring for critical pumps and periodic analysis for all others.",
        entity_scope="All rotating equipment in MECH01_pump_systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 10816; API 610 Section 7.8"
    ),
    DoctrineBlock(
        topic="API 610 Centrifugal Pump Standard Compliance",
        keywords=["API 610", "compliance", "centrifugal pump", "design", "testing"],
        conclusion_template="Ensure all centrifugal pumps meet API 610 requirements for design, materials, and testing.",
        reasoning_framework="""Review pump design and procurement specifications against API 610 requirements, including materials, construction, testing, and documentation. Verify compliance during design review, factory acceptance testing (FAT), and site acceptance testing (SAT). Address deviations with formal engineering justification and risk assessment. Maintain records of compliance for regulatory and client audits.""",
        key_factors=["Design specifications", "Material traceability", "Testing procedures", "Documentation"],
        primary_authority=["API 610", "Company Engineering Standards"],
        burden_holder="Project Engineer",
        adversary_position="Accepting non-compliant pumps to reduce cost or expedite delivery.",
        counter_arguments=[
            "Non-compliance can result in safety, reliability, and legal issues.",
            "API 610 compliance is often contractually required."
        ],
        resolution_strategy="Require documented compliance verification and management approval for any deviations.",
        entity_scope="Centrifugal pumps in MECH01_pump_systems",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610; Project Specifications"
    ),
    DoctrineBlock(
        topic="Pump Alignment - Laser vs Reverse Indicator Methods",
        keywords=["alignment", "laser alignment", "reverse indicator", "shaft alignment", "installation"],
        conclusion_template="Use laser alignment as the preferred method for pump and driver alignment; reverse indicator as backup.",
        reasoning_framework="""Assess alignment requirements during pump installation and maintenance. Laser alignment provides higher accuracy, faster setup, and better documentation than reverse indicator methods. Use reverse indicator as a backup or where laser tools are unavailable. Document alignment results and verify against manufacturer tolerances. Recheck alignment after initial operation and thermal growth. Train personnel in both methods and maintain calibration of alignment tools.""",
        key_factors=["Alignment accuracy", "Tool availability", "Personnel training", "Thermal growth", "Documentation"],
        primary_authority=["Pump Manufacturer Guidelines", "API 610", "ISO 1940"],
        burden_holder="Installation Supervisor",
        adversary_position="Using only visual or feeler gauge alignment methods.",
        counter_arguments=[
            "Inaccurate alignment increases vibration and reduces bearing and seal life.",
            "Laser alignment reduces human error and improves repeatability."
        ],
        resolution_strategy="Mandate laser alignment for all critical pumps; document exceptions and corrective actions.",
        entity_scope="Pump installations in MECH01_pump_systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 7.4; ISO 1940"
    ),
    DoctrineBlock(
        topic="Variable Speed Drives for Pump Energy Savings",
        keywords=["variable speed drive", "VSD", "energy savings", "pump control", "affinity laws"],
        conclusion_template="Implement variable speed drives (VSDs) to optimize pump energy consumption and process control.",
        reasoning_framework="""Analyze pump duty cycle and process variability. Where flow demand varies, VSDs allow pump speed adjustment to match system requirements, reducing energy consumption per affinity laws. Evaluate VSD compatibility with pump and motor. Consider harmonic distortion, cooling requirements, and control integration. Document energy savings projections and monitor actual performance. Reference utility incentives and regulatory requirements for energy efficiency.""",
        key_factors=["Duty cycle", "Process variability", "Pump/motor compatibility", "Energy savings", "Control integration"],
        primary_authority=["Hydraulic Institute Standards", "Pump Manufacturer Data", "IEEE 519"],
        burden_holder="Energy Manager",
        adversary_position="Using throttling valves or bypass for flow control instead of VSDs.",
        counter_arguments=[
            "Throttling wastes energy and increases wear.",
            "VSDs provide better process control and lower lifecycle costs."
        ],
        resolution_strategy="Require energy analysis for all new and retrofit pump installations; prioritize VSDs where feasible.",
        entity_scope="MECH01_pump_systems with variable flow requirements",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 1.3.4; IEEE 519"
    ),
    DoctrineBlock(
        topic="Multistage Pump Design and Application",
        keywords=["multistage pump", "high head", "series impellers", "pressure boosting"],
        conclusion_template="Select multistage pumps for applications requiring high head at moderate flow rates.",
        reasoning_framework="""Identify applications where single-stage pumps cannot provide required head. Evaluate flow and head requirements, fluid properties, and space constraints. Multistage pumps use multiple impellers in series to incrementally increase pressure. Analyze mechanical complexity, maintenance requirements, and cost. Reference manufacturer curves and API 610 guidelines. Document selection and ensure proper installation and commissioning procedures are followed.""",
        key_factors=["Required head", "Flow rate", "Space constraints", "Maintenance", "Cost"],
        primary_authority=["API 610", "Pump Manufacturer Data"],
        burden_holder="Design Engineer",
        adversary_position="Oversizing single-stage pumps or using multiple pumps in series without justification.",
        counter_arguments=[
            "Multistage pumps are more efficient and reliable for high head applications.",
            "Improper selection increases energy and maintenance costs."
        ],
        resolution_strategy="Require justification and review for all high-head pump selections.",
        entity_scope="High head applications in MECH01_pump_systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 6.2; HI 9.6.4"
    ),
    DoctrineBlock(
        topic="Slurry Pump Design and Abrasive Wear Considerations",
        keywords=["slurry pump", "abrasive wear", "hard materials", "impeller design", "solids handling"],
        conclusion_template="Design slurry pumps with materials and geometries optimized for abrasive service.",
        reasoning_framework="""Assess slurry properties: solids concentration, particle size, hardness, and fluid chemistry. Select pump materials with high hardness (e.g., high-chrome alloys, ceramics, rubber linings). Use open or recessed impeller designs to reduce clogging and wear. Increase clearances and consider replaceable wear parts. Reference manufacturer recommendations and industry standards. Document design choices and maintenance strategies for abrasive service.""",
        key_factors=["Solids concentration", "Particle size", "Material hardness", "Impeller design", "Maintenance strategy"],
        primary_authority=["Hydraulic Institute Standards", "Pump Manufacturer Data"],
        burden_holder="Process Engineer",
        adversary_position="Using standard pumps for abrasive slurries without modification.",
        counter_arguments=[
            "Standard pumps will fail prematurely in abrasive service.",
            "Proper design reduces downtime and total cost of ownership."
        ],
        resolution_strategy="Mandate slurry analysis and specialized pump selection for all abrasive applications.",
        entity_scope="Slurry handling in MECH01_pump_systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 12.1-12.6; Manufacturer Application Guides"
    ),
    # Additional 28+ DoctrineBlocks with real domain content follow:
    DoctrineBlock(
        topic="Pump System Curve Development",
        keywords=["system curve", "piping losses", "static head", "friction loss", "curve calculation"],
        conclusion_template="Develop accurate system curves by calculating static and dynamic head losses for all operating scenarios.",
        reasoning_framework="""Identify all sources of static head (elevation differences) and dynamic losses (pipe friction, fittings, valves). Use Darcy-Weisbach or Hazen-Williams equations for friction loss calculations. Sum static and dynamic components for each flow rate to plot the system curve. Consider minimum, normal, and maximum flow scenarios. Validate calculations with field measurements where possible. Update system curve as modifications are made to the piping or process.""",
        key_factors=["Elevation difference", "Pipe diameter", "Friction factor", "Fittings/valves", "Flow scenarios"],
        primary_authority=["Hydraulic Institute Standards", "Company Engineering Standards"],
        burden_holder="System Designer",
        adversary_position="Using generic or outdated system curves without site-specific calculations.",
        counter_arguments=[
            "Inaccurate system curves lead to improper pump selection and operation.",
            "Field validation is essential for critical systems."
        ],
        resolution_strategy="Require documented system curve calculations and periodic review.",
        entity_scope="All MECH01_pump_systems installations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 9.6.3; Company Standard ENG-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Minimum Flow Protection",
        keywords=["minimum flow", "recirculation", "thermal damage", "protection", "control valve"],
        conclusion_template="Implement minimum flow protection to prevent pump overheating and damage during low-flow conditions.",
        reasoning_framework="""Determine minimum continuous stable flow (MCSF) from manufacturer data. Install recirculation lines or automatic minimum flow control valves to maintain flow above MCSF. Monitor flow rates and alarm on low-flow conditions. Consider thermal and mechanical risks of operating below minimum flow. Document protection scheme and test during commissioning.""",
        key_factors=["MCSF", "Recirculation line", "Control valve", "Flow monitoring", "Alarm setpoints"],
        primary_authority=["API 610", "Pump Manufacturer Data"],
        burden_holder="Control Systems Engineer",
        adversary_position="Relying on operator intervention alone for minimum flow protection.",
        counter_arguments=[
            "Manual intervention is unreliable for critical protection.",
            "Thermal damage can occur rapidly at low flows."
        ],
        resolution_strategy="Mandate automated minimum flow protection for all critical pumps.",
        entity_scope="Centrifugal pumps in MECH01_pump_systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 6.1.8; Company Standard ENG-PS-002"
    ),
    DoctrineBlock(
        topic="Pump Start-up and Commissioning Procedures",
        keywords=["start-up", "commissioning", "pre-start checks", "run-in", "acceptance testing"],
        conclusion_template="Follow standardized start-up and commissioning procedures to ensure safe and reliable pump operation.",
        reasoning_framework="""Perform pre-start checks: alignment, lubrication, rotation direction, seal integrity, and instrumentation. Gradually introduce process fluid and monitor for abnormal vibration, noise, or leakage. Conduct run-in per manufacturer recommendations. Complete acceptance testing (flow, head, power, vibration). Document all results and resolve deficiencies before handover. Train operators on normal and emergency procedures.""",
        key_factors=["Pre-start checklist", "Instrumentation", "Acceptance testing", "Operator training", "Documentation"],
        primary_authority=["API 610", "Company Commissioning Procedures"],
        burden_holder="Commissioning Engineer",
        adversary_position="Skipping or abbreviating start-up procedures to save time.",
        counter_arguments=[
            "Improper commissioning increases risk of early failure.",
            "Documentation is critical for warranty and regulatory compliance."
        ],
        resolution_strategy="Enforce commissioning checklists and require management sign-off.",
        entity_scope="All new and overhauled MECH01_pump_systems",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 8; Company Procedure COM-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Shutdown and Isolation Procedures",
        keywords=["shutdown", "isolation", "lockout/tagout", "depressurization", "draining"],
        conclusion_template="Follow standardized shutdown and isolation procedures to ensure personnel and equipment safety.",
        reasoning_framework="""Initiate controlled shutdown by gradually reducing flow and pressure. Isolate pump using block valves. Depressurize and drain pump and associated piping as required. Apply lockout/tagout procedures before maintenance. Verify zero energy state before opening equipment. Document all steps and communicate with affected personnel.""",
        key_factors=["Shutdown sequence", "Isolation valves", "Depressurization", "Lockout/tagout", "Communication"],
        primary_authority=["OSHA 1910.147", "Company Safety Procedures"],
        burden_holder="Operations Supervisor",
        adversary_position="Bypassing isolation or lockout procedures for convenience.",
        counter_arguments=[
            "Failure to isolate can result in injury or fatality.",
            "Proper shutdown prevents equipment damage."
        ],
        resolution_strategy="Require safety audits and enforce disciplinary action for non-compliance.",
        entity_scope="All MECH01_pump_systems maintenance activities",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910.147; Company Procedure SAF-PS-002"
    ),
    DoctrineBlock(
        topic="Pump Lubrication Management",
        keywords=["lubrication", "oil analysis", "grease", "maintenance", "bearing life"],
        conclusion_template="Implement lubrication management program to maximize bearing and seal life.",
        reasoning_framework="""Establish lubrication schedules based on manufacturer recommendations and operating conditions. Use appropriate lubricant type and grade. Conduct periodic oil analysis to detect contamination and degradation. Monitor lubricant levels and temperatures. Train maintenance personnel in proper lubrication techniques. Document all activities and adjust schedules based on condition monitoring data.""",
        key_factors=["Lubricant type", "Schedule", "Oil analysis", "Temperature monitoring", "Training"],
        primary_authority=["API 610", "Pump Manufacturer Data", "ASTM D4378"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Using generic lubrication schedules or untrained personnel.",
        counter_arguments=[
            "Improper lubrication is a leading cause of pump failure.",
            "Condition-based lubrication reduces costs and extends equipment life."
        ],
        resolution_strategy="Mandate lubrication program audits and continuous improvement.",
        entity_scope="All rotating equipment in MECH01_pump_systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 7.2; ASTM D4378"
    ),
    DoctrineBlock(
        topic="Pump Instrumentation and Control",
        keywords=["instrumentation", "control", "flow measurement", "pressure monitoring", "automation"],
        conclusion_template="Equip pumps with appropriate instrumentation and control systems for safe and efficient operation.",
        reasoning_framework="""Install flow, pressure, temperature, and vibration sensors at critical points. Integrate with control system (PLC/DCS) for automated start/stop, alarm, and interlock functions. Calibrate instruments regularly and maintain documentation. Use control logic to prevent unsafe operation (e.g., low flow, high temperature). Reference ISA standards and manufacturer guidelines.""",
        key_factors=["Sensor selection", "Control integration", "Calibration", "Alarm setpoints", "Documentation"],
        primary_authority=["ISA Standards", "Pump Manufacturer Data"],
        burden_holder="Instrumentation Engineer",
        adversary_position="Relying solely on manual operation or inadequate instrumentation.",
        counter_arguments=[
            "Lack of instrumentation increases risk of undetected failures.",
            "Automation improves safety and reliability."
        ],
        resolution_strategy="Require instrumentation review for all pump installations.",
        entity_scope="MECH01_pump_systems process control",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 5.1; Company Standard ENG-PS-003"
    ),
    DoctrineBlock(
        topic="Pump Noise and Acoustic Analysis",
        keywords=["noise", "acoustics", "sound pressure", "regulations", "vibration"],
        conclusion_template="Conduct acoustic analysis and implement noise control measures to meet regulatory and occupational limits.",
        reasoning_framework="""Measure baseline noise levels during pump operation. Compare to regulatory and company limits (e.g., OSHA, local ordinances). Identify sources of excessive noise (vibration, cavitation, flow turbulence). Implement control measures: isolation pads, acoustic enclosures, piping modifications. Monitor effectiveness and document compliance. Train personnel in noise hazard awareness.""",
        key_factors=["Sound pressure level", "Regulatory limits", "Noise sources", "Control measures", "Personnel exposure"],
        primary_authority=["OSHA 1910.95", "Company Safety Standards"],
        burden_holder="Health & Safety Officer",
        adversary_position="Ignoring noise issues or relying on PPE alone.",
        counter_arguments=[
            "Excessive noise causes hearing loss and regulatory violations.",
            "Engineering controls are more effective than PPE."
        ],
        resolution_strategy="Require noise surveys and corrective action plans for all high-noise areas.",
        entity_scope="MECH01_pump_systems installations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910.95; Company Procedure SAF-PS-003"
    ),
    DoctrineBlock(
        topic="Pump Foundation and Baseplate Design",
        keywords=["foundation", "baseplate", "grouting", "vibration", "installation"],
        conclusion_template="Design pump foundations and baseplates to minimize vibration and ensure long-term alignment.",
        reasoning_framework="""Determine static and dynamic loads from pump and driver. Design reinforced concrete foundation with mass at least 3 times that of the pump set. Use rigid baseplates and precision grouting. Allow for anchor bolt access and alignment adjustments. Reference API 610 and manufacturer installation guidelines. Inspect foundation and baseplate before and after installation.""",
        key_factors=["Load calculation", "Foundation mass", "Baseplate rigidity", "Grouting", "Alignment"],
        primary_authority=["API 610", "ACI 351.3R", "Pump Manufacturer Data"],
        burden_holder="Civil/Structural Engineer",
        adversary_position="Using undersized or unreinforced foundations.",
        counter_arguments=[
            "Inadequate foundations increase vibration and misalignment risk.",
            "Proper design extends equipment life."
        ],
        resolution_strategy="Require foundation design review and inspection reports.",
        entity_scope="Pump installations in MECH01_pump_systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 7.5; ACI 351.3R"
    ),
    DoctrineBlock(
        topic="Pump Spare Parts Management",
        keywords=["spare parts", "inventory", "critical spares", "lead time", "maintenance"],
        conclusion_template="Maintain inventory of critical spare parts to minimize downtime and support maintenance.",
        reasoning_framework="""Identify critical spare parts based on failure modes and lead times. Maintain inventory levels to support planned and unplanned maintenance. Use manufacturer-recommended spare parts lists. Track usage and adjust inventory based on reliability data. Document all transactions and reconcile with maintenance records. Review spare parts strategy annually.""",
        key_factors=["Failure modes", "Lead time", "Inventory levels", "Usage tracking", "Maintenance planning"],
        primary_authority=["Company Maintenance Standards", "Pump Manufacturer Data"],
        burden_holder="Maintenance Planner",
        adversary_position="Relying on just-in-time ordering for all spare parts.",
        counter_arguments=[
            "Long lead times can result in extended downtime.",
            "Overstocking increases carrying costs."
        ],
        resolution_strategy="Balance inventory using criticality and reliability analysis.",
        entity_scope="All MECH01_pump_systems maintenance",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard MNT-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Operator Training and Competency",
        keywords=["operator training", "competency", "procedures", "safety", "certification"],
        conclusion_template="Provide comprehensive training and certification for all pump operators.",
        reasoning_framework="""Develop training programs covering pump operation, safety, emergency procedures, and troubleshooting. Use classroom, hands-on, and simulation-based methods. Assess competency through testing and observation. Require periodic refresher training and certification renewal. Maintain training records and address gaps promptly.""",
        key_factors=["Training content", "Assessment", "Certification", "Refresher frequency", "Records management"],
        primary_authority=["Company Training Standards", "OSHA 1910.119"],
        burden_holder="Training Coordinator",
        adversary_position="Allowing untrained personnel to operate pumps.",
        counter_arguments=[
            "Lack of training increases risk of accidents and equipment damage.",
            "Certification ensures minimum competency standards."
        ],
        resolution_strategy="Mandate certification for all operators and enforce access controls.",
        entity_scope="All MECH01_pump_systems operations",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Procedure TRN-PS-001; OSHA 1910.119"
    ),
    DoctrineBlock(
        topic="Pump Performance Testing and Verification",
        keywords=["performance testing", "verification", "factory acceptance test", "site acceptance test", "flow measurement"],
        conclusion_template="Conduct performance testing to verify pump meets specified flow, head, and efficiency.",
        reasoning_framework="""Perform factory acceptance testing (FAT) per API 610 and manufacturer procedures. Measure flow, head, power, and vibration at specified points. Compare results to guaranteed values. Repeat testing at site (SAT) after installation. Document all results and resolve discrepancies before acceptance. Maintain test records for warranty and regulatory compliance.""",
        key_factors=["Test procedures", "Measurement accuracy", "Acceptance criteria", "Documentation", "Warranty"],
        primary_authority=["API 610", "Pump Manufacturer Data"],
        burden_holder="Quality Engineer",
        adversary_position="Relying solely on manufacturer data without independent verification.",
        counter_arguments=[
            "Site conditions can differ from factory conditions.",
            "Independent testing ensures contract compliance."
        ],
        resolution_strategy="Require documented test plans and third-party witness for critical pumps.",
        entity_scope="All new and overhauled MECH01_pump_systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 8; Company Procedure QLT-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Reliability-Centered Maintenance (RCM)",
        keywords=["RCM", "reliability", "maintenance strategy", "failure modes", "predictive maintenance"],
        conclusion_template="Implement reliability-centered maintenance to optimize pump uptime and reduce lifecycle costs.",
        reasoning_framework="""Analyze failure modes and effects (FMEA) for each pump type. Develop maintenance strategies combining preventive, predictive, and corrective actions. Use condition monitoring data (vibration, oil analysis, temperature) to schedule maintenance. Review reliability data and adjust strategies accordingly. Document all activities and measure effectiveness using KPIs (MTBF, MTTR).""",
        key_factors=["Failure modes", "Condition monitoring", "Maintenance schedule", "Reliability data", "KPIs"],
        primary_authority=["Company Maintenance Standards", "Hydraulic Institute Standards"],
        burden_holder="Reliability Engineer",
        adversary_position="Using fixed-interval preventive maintenance without regard to condition data.",
        counter_arguments=[
            "RCM reduces unplanned downtime and maintenance costs.",
            "Condition-based maintenance improves resource allocation."
        ],
        resolution_strategy="Mandate RCM analysis for all critical pumps and periodic review of maintenance strategies.",
        entity_scope="MECH01_pump_systems maintenance",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard MNT-PS-002"
    ),
    DoctrineBlock(
        topic="Pump Root Cause Failure Analysis (RCFA)",
        keywords=["RCFA", "failure investigation", "root cause", "corrective action", "incident analysis"],
        conclusion_template="Conduct root cause failure analysis for all significant pump failures to prevent recurrence.",
        reasoning_framework="""Initiate RCFA for failures resulting in unplanned downtime, safety incidents, or significant cost. Collect evidence: operating data, maintenance records, failed components. Use structured analysis methods (e.g., 5 Whys, Fishbone Diagram). Identify root causes and implement corrective actions. Document findings and share lessons learned across organization.""",
        key_factors=["Failure data", "Analysis method", "Corrective action", "Documentation", "Knowledge sharing"],
        primary_authority=["Company Reliability Standards", "API 610"],
        burden_holder="Reliability Engineer",
        adversary_position="Treating symptoms without addressing underlying causes.",
        counter_arguments=[
            "RCFA reduces repeat failures and improves reliability.",
            "Superficial analysis leads to recurring problems."
        ],
        resolution_strategy="Require RCFA for all major failures and management review of corrective actions.",
        entity_scope="All MECH01_pump_systems failures",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Procedure RCF-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Seal System API Plan Selection",
        keywords=["API seal plan", "seal system", "Plan 11", "Plan 23", "Plan 52", "Plan 53"],
        conclusion_template="Select API seal plan based on process fluid, pressure, and environmental requirements.",
        reasoning_framework="""Evaluate process fluid properties, pressure, temperature, and potential for hazardous emissions. Reference API 682 for seal plan selection: Plan 11 (simple flush), Plan 23 (cooling), Plan 52/53 (dual seals with buffer/barrier fluid). Ensure compatibility with process and environmental regulations. Document selection and review with process safety and reliability teams.""",
        key_factors=["Process fluid", "Pressure", "Temperature", "Emissions", "Regulations"],
        primary_authority=["API 682", "Pump Manufacturer Data"],
        burden_holder="Process Engineer",
        adversary_position="Using default seal plans without process-specific analysis.",
        counter_arguments=[
            "Improper seal plan selection increases risk of leakage and environmental non-compliance.",
            "Overly complex plans increase maintenance burden."
        ],
        resolution_strategy="Require seal plan selection worksheet and cross-functional review.",
        entity_scope="Centrifugal pumps in MECH01_pump_systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 682 Section 4"
    ),
    DoctrineBlock(
        topic="Pump Backflow and Reverse Rotation Prevention",
        keywords=["backflow", "reverse rotation", "check valve", "non-return valve", "system protection"],
        conclusion_template="Install check valves to prevent pump backflow and reverse rotation during shutdown.",
        reasoning_framework="""Assess system configuration for potential backflow scenarios. Install check valves (non-return valves) downstream of pump discharge. Select valve type and sizing to minimize pressure drop and prevent slam. Verify valve operation during commissioning. Document installation and maintenance procedures.""",
        key_factors=["System configuration", "Valve selection", "Pressure drop", "Commissioning", "Maintenance"],
        primary_authority=["Hydraulic Institute Standards", "Company Engineering Standards"],
        burden_holder="System Designer",
        adversary_position="Omitting check valves to reduce cost or complexity.",
        counter_arguments=[
            "Backflow can cause reverse rotation, damaging pump and driver.",
            "Check valves are essential for system protection."
        ],
        resolution_strategy="Mandate check valve installation for all pumps with backflow risk.",
        entity_scope="MECH01_pump_systems with backflow potential",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 9.6.6; Company Standard ENG-PS-004"
    ),
    DoctrineBlock(
        topic="Pump Suction Piping Design",
        keywords=["suction piping", "NPSH", "piping layout", "velocity", "entrainment"],
        conclusion_template="Design suction piping to minimize losses, entrainment, and ensure adequate NPSH.",
        reasoning_framework="""Use straight, short, and adequately sized suction piping. Limit velocity to 1–2 m/s for water and 0.8–1.2 m/s for viscous fluids. Avoid elbows and fittings immediately before pump suction. Install eccentric reducers flat side up to prevent air pockets. Ensure piping is free of leaks and properly supported. Reference Hydraulic Institute and manufacturer guidelines.""",
        key_factors=["Pipe diameter", "Velocity", "Fittings", "Reducer orientation", "Support"],
        primary_authority=["Hydraulic Institute Standards", "Pump Manufacturer Data"],
        burden_holder="Piping Designer",
        adversary_position="Using undersized or complex suction piping layouts.",
        counter_arguments=[
            "Poor suction piping increases NPSH losses and risk of cavitation.",
            "Proper design improves reliability and efficiency."
        ],
        resolution_strategy="Require suction piping review and field inspection before commissioning.",
        entity_scope="All MECH01_pump_systems installations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 9.6.6; Company Standard ENG-PS-005"
    ),
    DoctrineBlock(
        topic="Pump Discharge Piping and Pressure Control",
        keywords=["discharge piping", "pressure control", "valves", "water hammer", "pipe stress"],
        conclusion_template="Design discharge piping and pressure control systems to prevent water hammer and excessive stress.",
        reasoning_framework="""Select appropriate pipe diameter and schedule for discharge pressure. Install pressure control valves and slow-closing check valves to minimize water hammer. Use pipe supports and expansion joints to accommodate thermal movement. Analyze pipe stress and anchor points. Reference ASME B31.3 and manufacturer guidelines. Document design and verify during commissioning.""",
        key_factors=["Pipe diameter", "Pressure rating", "Valve selection", "Water hammer", "Pipe stress"],
        primary_authority=["ASME B31.3", "Pump Manufacturer Data"],
        burden_holder="Piping Designer",
        adversary_position="Ignoring water hammer or using inadequate pipe supports.",
        counter_arguments=[
            "Water hammer can cause catastrophic pipe failure.",
            "Proper design reduces maintenance and downtime."
        ],
        resolution_strategy="Require discharge piping stress analysis and commissioning checks.",
        entity_scope="All MECH01_pump_systems installations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.3; Company Standard ENG-PS-006"
    ),
    DoctrineBlock(
        topic="Pump Thermal Expansion and Pipe Stress Management",
        keywords=["thermal expansion", "pipe stress", "expansion joints", "anchor points", "temperature"],
        conclusion_template="Manage thermal expansion in pump piping to prevent excessive stress and misalignment.",
        reasoning_framework="""Calculate thermal expansion for all pump-connected piping based on temperature range. Install expansion joints or loops as required. Locate anchor points to control movement. Analyze pipe stress using CAESAR II or equivalent software. Verify alignment after thermal cycling. Document all calculations and field adjustments.""",
        key_factors=["Temperature range", "Pipe material", "Expansion joints", "Anchor points", "Stress analysis"],
        primary_authority=["ASME B31.3", "Company Engineering Standards"],
        burden_holder="Piping Designer",
        adversary_position="Omitting expansion joints or relying on flexible hoses.",
        counter_arguments=[
            "Unmanaged thermal expansion causes misalignment and equipment damage.",
            "Proper management extends equipment and piping life."
        ],
        resolution_strategy="Require thermal expansion analysis and field verification.",
        entity_scope="All MECH01_pump_systems piping",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.3 Section 319; Company Standard ENG-PS-007"
    ),
    DoctrineBlock(
        topic="Pump Electrical Motor Sizing and Selection",
        keywords=["motor sizing", "electrical", "service factor", "starting torque", "efficiency"],
        conclusion_template="Select electric motors with adequate power, service factor, and starting torque for pump applications.",
        reasoning_framework="""Calculate required motor power based on pump curve (flow, head, efficiency). Apply service factor (typically 1.15) to account for overloads. Ensure starting torque exceeds pump breakaway torque. Select high-efficiency motors (IE3/IE4) where feasible. Verify compatibility with VSDs if used. Reference NEMA MG 1 and manufacturer data. Document selection and commissioning tests.""",
        key_factors=["Pump power", "Service factor", "Starting torque", "Efficiency", "VSD compatibility"],
        primary_authority=["NEMA MG 1", "Pump Manufacturer Data"],
        burden_holder="Electrical Engineer",
        adversary_position="Undersizing motors to reduce cost.",
        counter_arguments=[
            "Undersized motors overheat and fail prematurely.",
            "Proper sizing improves reliability and efficiency."
        ],
        resolution_strategy="Require motor sizing calculations and peer review.",
        entity_scope="All MECH01_pump_systems motor-driven pumps",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEMA MG 1; Company Standard ENG-EL-001"
    ),
    DoctrineBlock(
        topic="Pump Emergency Shutdown (ESD) Integration",
        keywords=["emergency shutdown", "ESD", "safety systems", "interlocks", "fail-safe"],
        conclusion_template="Integrate pumps with ESD systems to ensure safe shutdown during emergencies.",
        reasoning_framework="""Identify emergency scenarios requiring pump shutdown (fire, leak, overpressure). Integrate pump controls with plant ESD system. Use hardwired interlocks and fail-safe logic. Test ESD function during commissioning and periodically thereafter. Document all interlock logic and test results. Train operators on ESD procedures.""",
        key_factors=["ESD scenarios", "Interlock logic", "Testing", "Documentation", "Operator training"],
        primary_authority=["ISA 84", "Company Safety Standards"],
        burden_holder="Control Systems Engineer",
        adversary_position="Relying on manual shutdown or omitting ESD integration.",
        counter_arguments=[
            "Manual shutdown is unreliable in emergencies.",
            "ESD integration is required for process safety compliance."
        ],
        resolution_strategy="Mandate ESD integration for all critical pumps and periodic testing.",
        entity_scope="MECH01_pump_systems in safety-critical applications",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 84; Company Procedure SAF-PS-004"
    ),
    DoctrineBlock(
        topic="Pump Fire Protection and Safety",
        keywords=["fire protection", "safety", "fire pump", "NFPA 20", "emergency response"],
        conclusion_template="Provide fire protection pumps and systems in accordance with NFPA 20 and local regulations.",
        reasoning_framework="""Assess fire protection requirements for facility. Select fire pumps and controllers per NFPA 20. Ensure dedicated water supply, reliable power, and automatic start. Test fire pumps weekly and document results. Train personnel in emergency response and maintenance. Maintain compliance records for regulatory authorities.""",
        key_factors=["Fire protection requirements", "NFPA 20 compliance", "Testing", "Training", "Documentation"],
        primary_authority=["NFPA 20", "Local Fire Codes"],
        burden_holder="Fire Protection Engineer",
        adversary_position="Using process pumps for fire protection or omitting required systems.",
        counter_arguments=[
            "Dedicated fire pumps are required for code compliance.",
            "Improper systems increase risk to life and property."
        ],
        resolution_strategy="Require fire protection system review and authority approval.",
        entity_scope="MECH01_pump_systems in fire protection applications",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 20; Local Fire Code"
    ),
    DoctrineBlock(
        topic="Pump Environmental Compliance and Spill Control",
        keywords=["environmental compliance", "spill control", "secondary containment", "leak detection", "regulations"],
        conclusion_template="Implement spill control and leak detection systems to meet environmental regulations.",
        reasoning_framework="""Identify environmental risks from pump operation (leaks, spills). Install secondary containment and leak detection sensors. Develop spill response plans and train personnel. Maintain compliance with local, state, and federal regulations. Document inspections, incidents, and corrective actions. Review systems annually and update as needed.""",
        key_factors=["Containment", "Leak detection", "Response plans", "Training", "Regulatory compliance"],
        primary_authority=["EPA Regulations", "Company Environmental Standards"],
        burden_holder="Environmental Manager",
        adversary_position="Omitting containment or relying solely on operator observation.",
        counter_arguments=[
            "Environmental violations result in fines and reputational damage.",
            "Automated systems improve detection and response."
        ],
        resolution_strategy="Mandate spill control systems and periodic compliance audits.",
        entity_scope="All MECH01_pump_systems installations",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA 40 CFR 112; Company Procedure ENV-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Documentation and Records Management",
        keywords=["documentation", "records", "drawings", "maintenance logs", "compliance"],
        conclusion_template="Maintain comprehensive documentation and records for all pump systems.",
        reasoning_framework="""Store and update all pump-related documents: P&IDs, datasheets, manuals, test records, maintenance logs. Use electronic document management systems with version control. Ensure accessibility for operations, maintenance, and audits. Review and update records after modifications or major maintenance. Archive obsolete documents per company policy.""",
        key_factors=["Document types", "Version control", "Accessibility", "Review process", "Archiving"],
        primary_authority=["Company Document Control Standards"],
        burden_holder="Document Control Coordinator",
        adversary_position="Relying on paper records or outdated documentation.",
        counter_arguments=[
            "Incomplete records hinder maintenance and compliance.",
            "Electronic systems improve access and traceability."
        ],
        resolution_strategy="Mandate electronic document management and periodic audits.",
        entity_scope="All MECH01_pump_systems documentation",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard DOC-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Energy Efficiency Optimization",
        keywords=["energy efficiency", "optimization", "system audit", "pump upgrade", "variable speed"],
        conclusion_template="Optimize pump energy efficiency through system audits and upgrades.",
        reasoning_framework="""Conduct energy audits to identify inefficiencies (oversized pumps, throttling, leaks). Upgrade to high-efficiency pumps and motors where justified. Implement variable speed drives and control strategies. Monitor energy consumption and compare to benchmarks. Document savings and reinvest in further improvements.""",
        key_factors=["Audit results", "Pump sizing", "Control strategy", "Energy monitoring", "Benchmarking"],
        primary_authority=["Hydraulic Institute Standards", "Company Energy Policy"],
        burden_holder="Energy Manager",
        adversary_position="Accepting existing inefficiencies as unavoidable.",
        counter_arguments=[
            "Energy costs are a major component of lifecycle cost.",
            "Optimization reduces emissions and operating expenses."
        ],
        resolution_strategy="Mandate periodic energy audits and implementation of cost-effective measures.",
        entity_scope="All MECH01_pump_systems operations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 1.3.4; Company Energy Policy"
    ),
    DoctrineBlock(
        topic="Pump Lifecycle Cost Analysis",
        keywords=["lifecycle cost", "LCC", "capital cost", "maintenance", "energy cost"],
        conclusion_template="Perform lifecycle cost analysis to inform pump selection and upgrade decisions.",
        reasoning_framework="""Estimate total cost of ownership: capital, installation, energy, maintenance, downtime, and disposal. Use LCC models per Hydraulic Institute and ISO 15663. Compare alternatives based on net present value (NPV) and payback period. Document assumptions and sensitivity analysis. Use results to justify investments and upgrades.""",
        key_factors=["Capital cost", "Energy cost", "Maintenance", "Downtime", "Disposal"],
        primary_authority=["Hydraulic Institute Standards", "ISO 15663"],
        burden_holder="Project Engineer",
        adversary_position="Selecting pumps based solely on lowest capital cost.",
        counter_arguments=[
            "Lowest initial cost may result in higher total cost.",
            "LCC analysis supports informed decision-making."
        ],
        resolution_strategy="Require LCC analysis for all major pump projects.",
        entity_scope="All MECH01_pump_systems projects",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 1.3.5; ISO 15663"
    ),
    DoctrineBlock(
        topic="Pump Obsolescence and Upgrade Planning",
        keywords=["obsolescence", "upgrade", "technology", "spare parts", "risk management"],
        conclusion_template="Plan for pump obsolescence and upgrades to mitigate operational and supply chain risks.",
        reasoning_framework="""Identify pumps at risk of obsolescence due to age, technology, or spare parts availability. Develop upgrade or replacement plans based on risk assessment. Engage with manufacturers and suppliers to anticipate changes. Document plans and communicate with stakeholders. Review and update plans annually.""",
        key_factors=["Age", "Technology", "Spare parts", "Risk assessment", "Stakeholder communication"],
        primary_authority=["Company Asset Management Standards"],
        burden_holder="Asset Manager",
        adversary_position="Ignoring obsolescence until failure occurs.",
        counter_arguments=[
            "Unplanned obsolescence increases downtime and costs.",
            "Proactive planning reduces risk and improves reliability."
        ],
        resolution_strategy="Mandate annual obsolescence reviews and documented upgrade plans.",
        entity_scope="All MECH01_pump_systems assets",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard ASM-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Cybersecurity and Control System Protection",
        keywords=["cybersecurity", "control system", "PLC", "SCADA", "network security"],
        conclusion_template="Implement cybersecurity measures to protect pump control systems from unauthorized access and threats.",
        reasoning_framework="""Assess control system architecture for vulnerabilities. Implement network segmentation, firewalls, and access controls. Regularly update software and firmware. Train personnel in cybersecurity awareness. Conduct periodic penetration testing and incident response drills. Document all measures and review after system changes.""",
        key_factors=["Network architecture", "Access controls", "Software updates", "Training", "Incident response"],
        primary_authority=["NIST SP 800-82", "Company IT Security Standards"],
        burden_holder="Control Systems Engineer",
        adversary_position="Relying on default passwords or unsecured networks.",
        counter_arguments=[
            "Cyberattacks can disrupt operations and cause safety incidents.",
            "Proactive measures reduce risk and support compliance."
        ],
        resolution_strategy="Mandate cybersecurity risk assessments and periodic audits.",
        entity_scope="All MECH01_pump_systems control systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST SP 800-82; Company IT Policy"
    ),
    DoctrineBlock(
        topic="Pump Remote Monitoring and Diagnostics",
        keywords=["remote monitoring", "diagnostics", "IoT", "predictive maintenance", "data analytics"],
        conclusion_template="Implement remote monitoring and diagnostics to enhance pump reliability and reduce maintenance costs.",
        reasoning_framework="""Install IoT-enabled sensors for vibration, temperature, pressure, and flow. Transmit data to centralized monitoring platform. Use analytics to detect anomalies and predict failures. Integrate with maintenance management systems for automated work order generation. Review performance data regularly and adjust maintenance strategies accordingly.""",
        key_factors=["Sensor deployment", "Data transmission", "Analytics", "Integration", "Maintenance response"],
        primary_authority=["Hydraulic Institute Standards", "Company Digital Strategy"],
        burden_holder="Reliability Engineer",
        adversary_position="Relying solely on local monitoring and manual data collection.",
        counter_arguments=[
            "Remote monitoring enables early detection and faster response.",
            "Manual methods are less effective and more labor-intensive."
        ],
        resolution_strategy="Mandate remote monitoring for all critical pumps and periodic review of analytics.",
        entity_scope="MECH01_pump_systems with remote monitoring capability",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 1.3.6; Company Digital Policy"
    ),
    DoctrineBlock(
        topic="Pump Asset Tagging and Identification",
        keywords=["asset tagging", "identification", "barcoding", "RFID", "asset management"],
        conclusion_template="Tag and identify all pump assets for effective management and traceability.",
        reasoning_framework="""Assign unique asset tags to all pumps and major components. Use barcodes or RFID for automated identification. Link tags to asset management system with complete history and documentation. Update records after maintenance or modification. Conduct periodic audits to verify asset inventory.""",
        key_factors=["Tagging method", "Asset management system", "Record updates", "Audit frequency", "Traceability"],
        primary_authority=["Company Asset Management Standards"],
        burden_holder="Asset Manager",
        adversary_position="Using generic or duplicate asset numbers.",
        counter_arguments=[
            "Proper tagging improves traceability and maintenance efficiency.",
            "Duplicate or missing tags hinder asset management."
        ],
        resolution_strategy="Mandate asset tagging and periodic inventory audits.",
        entity_scope="All MECH01_pump_systems assets",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard ASM-PS-002"
    ),
    DoctrineBlock(
        topic="Pump Change Management and Modification Control",
        keywords=["change management", "modification", "MOC", "documentation", "risk assessment"],
        conclusion_template="Control all pump system modifications through formal change management procedures.",
        reasoning_framework="""Initiate Management of Change (MOC) for all modifications affecting pump systems. Assess risks, update documentation, and obtain approvals before implementation. Communicate changes to affected personnel. Verify and document completion. Review effectiveness and update procedures as needed.""",
        key_factors=["MOC process", "Risk assessment", "Documentation", "Communication", "Verification"],
        primary_authority=["OSHA 1910.119", "Company MOC Standards"],
        burden_holder="Project Manager",
        adversary_position="Making undocumented or unauthorized changes.",
        counter_arguments=[
            "Uncontrolled changes increase risk of failure and non-compliance.",
            "MOC ensures safety and traceability."
        ],
        resolution_strategy="Mandate MOC for all pump system changes and periodic audits.",
        entity_scope="All MECH01_pump_systems modifications",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910.119; Company Procedure MOC-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Spare Capacity and Redundancy Planning",
        keywords=["spare capacity", "redundancy", "N+1", "reliability", "critical service"],
        conclusion_template="Plan for spare capacity and redundancy in critical pump applications.",
        reasoning_framework="""Identify critical services requiring high reliability. Design systems with N+1 redundancy (one spare for N required pumps). Size pumps and piping to allow for seamless switchover. Test redundancy during commissioning and periodically. Document redundancy philosophy and maintenance procedures.""",
        key_factors=["Criticality", "Redundancy level", "Sizing", "Testing", "Documentation"],
        primary_authority=["Company Reliability Standards", "Hydraulic Institute Standards"],
        burden_holder="System Designer",
        adversary_position="Operating without redundancy in critical services.",
        counter_arguments=[
            "Lack of redundancy increases risk of unplanned outages.",
            "Proper planning improves reliability and safety."
        ],
        resolution_strategy="Mandate redundancy review for all critical pump systems.",
        entity_scope="Critical MECH01_pump_systems applications",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="HI 1.3.7; Company Reliability Policy"
    ),
    DoctrineBlock(
        topic="Pump Vendor Qualification and Procurement",
        keywords=["vendor qualification", "procurement", "approved vendor list", "quality assurance", "bid evaluation"],
        conclusion_template="Qualify pump vendors and follow standardized procurement procedures to ensure quality and compliance.",
        reasoning_framework="""Evaluate vendors based on technical capability, quality systems, financial stability, and past performance. Maintain approved vendor list (AVL). Use standardized bid evaluation and contract terms. Inspect and test pumps before acceptance. Document all procurement activities and vendor performance reviews.""",
        key_factors=["Vendor capability", "Quality systems", "AVL", "Inspection", "Documentation"],
        primary_authority=["Company Procurement Standards", "API 610"],
        burden_holder="Procurement Manager",
        adversary_position="Selecting vendors based solely on lowest price.",
        counter_arguments=[
            "Unqualified vendors increase risk of non-compliance and poor performance.",
            "Standardized procurement improves quality and traceability."
        ],
        resolution_strategy="Mandate vendor qualification and periodic performance review.",
        entity_scope="All MECH01_pump_systems procurement",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard PRC-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Environmental Noise Impact Assessment",
        keywords=["environmental noise", "impact assessment", "community", "regulations", "mitigation"],
        conclusion_template="Assess and mitigate environmental noise impact from pump installations.",
        reasoning_framework="""Conduct noise impact assessments for new and modified pump installations. Model sound propagation to nearby receptors (community, wildlife). Compare predicted levels to regulatory limits. Implement mitigation measures (barriers, enclosures, operational limits) as needed. Document assessments and monitor post-installation noise levels.""",
        key_factors=["Noise modeling", "Receptor identification", "Regulatory limits", "Mitigation", "Monitoring"],
        primary_authority=["Local Environmental Regulations", "Company Environmental Standards"],
        burden_holder="Environmental Engineer",
        adversary_position="Ignoring offsite noise impacts or relying solely on in-plant measurements.",
        counter_arguments=[
            "Environmental noise complaints can halt operations.",
            "Proactive assessment supports community relations."
        ],
        resolution_strategy="Mandate environmental noise assessments for all new projects.",
        entity_scope="All MECH01_pump_systems installations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Local Regulations; Company Procedure ENV-PS-002"
    ),
    DoctrineBlock(
        topic="Pump Asset Criticality Ranking",
        keywords=["criticality ranking", "risk assessment", "maintenance prioritization", "asset management"],
        conclusion_template="Rank pump assets by criticality to prioritize maintenance and resource allocation.",
        reasoning_framework="""Assess each pump's impact on safety, environment, production, and cost. Assign criticality scores using risk matrices. Use rankings to prioritize preventive maintenance, spares, and upgrades. Review rankings annually and after major process changes. Document methodology and communicate to stakeholders.""",
        key_factors=["Safety impact", "Production impact", "Environmental risk", "Cost", "Risk matrix"],
        primary_authority=["Company Asset Management Standards"],
        burden_holder="Asset Manager",
        adversary_position="Treating all pumps equally regardless of risk.",
        counter_arguments=[
            "Criticality ranking optimizes resource allocation.",
            "Ignoring criticality increases risk of unplanned outages."
        ],
        resolution_strategy="Mandate criticality ranking and periodic review.",
        entity_scope="All MECH01_pump_systems assets",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard ASM-PS-003"
    ),
    DoctrineBlock(
        topic="Pump Spare Parts Interchangeability",
        keywords=["spare parts", "interchangeability", "standardization", "inventory", "maintenance"],
        conclusion_template="Standardize and document spare parts interchangeability to optimize inventory and maintenance.",
        reasoning_framework="""Identify pumps and components with interchangeable parts. Standardize part numbers and descriptions. Maintain interchangeability matrix and update as equipment changes. Train maintenance personnel in correct usage. Review and update matrix annually.""",
        key_factors=["Part standardization", "Interchangeability matrix", "Training", "Inventory management", "Documentation"],
        primary_authority=["Company Maintenance Standards"],
        burden_holder="Maintenance Planner",
        adversary_position="Using non-standard or undocumented parts.",
        counter_arguments=[
            "Standardization reduces inventory and errors.",
            "Non-interchangeable parts increase downtime."
        ],
        resolution_strategy="Mandate interchangeability matrix and periodic review.",
        entity_scope="All MECH01_pump_systems maintenance",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Company Standard MNT-PS-003"
    ),
    DoctrineBlock(
        topic="Pump Process Safety Management (PSM) Integration",
        keywords=["process safety management", "PSM", "hazard analysis", "compliance", "risk reduction"],
        conclusion_template="Integrate pump systems into facility PSM program to ensure hazard identification and risk reduction.",
        reasoning_framework="""Include pumps in process hazard analysis (PHA) and layer of protection analysis (LOPA). Document safety instrumented functions (SIFs) and safeguards. Train personnel in PSM requirements. Maintain compliance records and review after incidents or changes. Reference OSHA 1910.119 and company PSM standards.""",
        key_factors=["PHA", "LOPA", "SIFs", "Training", "Compliance records"],
        primary_authority=["OSHA 1910.119", "Company PSM Standards"],
        burden_holder="Process Safety Manager",
        adversary_position="Omitting pumps from PSM scope or documentation.",
        counter_arguments=[
            "PSM integration reduces risk of major incidents.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Mandate PSM review for all pump system changes.",
        entity_scope="All MECH01_pump_systems in PSM-regulated facilities",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910.119; Company Procedure PSM-PS-001"
    ),
    DoctrineBlock(
        topic="Pump Environmental Permitting and Reporting",
        keywords=["environmental permitting", "reporting", "compliance", "emissions", "regulations"],
        conclusion_template="Obtain required environmental permits and maintain reporting for pump operations.",
        reasoning_framework="""Identify applicable environmental permits for pump operations (air, water, waste). Submit applications and supporting documentation to regulatory agencies. Monitor compliance and submit periodic reports. Maintain records for inspections and audits. Review permit requirements annually and after process changes.""",
        key_factors=["Permit identification", "Application process", "Monitoring", "Reporting", "Recordkeeping"],
        primary_authority=["EPA Regulations", "Local Environmental Agencies"],
        burden_holder="Environmental Manager",
        adversary_position="Operating without required permits or failing to report.",
        counter_arguments=[
            "Permit violations result in fines and operational shutdowns.",
            "Proactive compliance supports business continuity."
        ],
        resolution_strategy="Mandate permit review and compliance audits for all pump operations.",
        entity_scope="All MECH01_pump_systems subject to environmental regulation",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA 40 CFR; Company Procedure ENV-PS-003"
    ),
    DoctrineBlock(
        topic="Pump System Integration with Process Control",
        keywords=["system integration", "process control", "PLC", "DCS", "automation"],
        conclusion_template="Integrate pump systems with process control for optimized operation and safety.",
        reasoning_framework="""Connect pump instrumentation and controls to plant PLC/DCS. Implement automated start/stop, speed control, and alarm management. Ensure fail-safe logic and redundancy for critical applications. Test integration during commissioning and after changes. Document control logic and maintain version control.""",
        key_factors=["Control system", "Integration testing", "Alarm management", "Redundancy", "Documentation"],
        primary_authority=["ISA Standards", "Company Automation Standards"],
        burden_holder="Control Systems Engineer",
        adversary_position="Operating pumps in manual mode or with inadequate integration.",
        counter_arguments=[
            "Integration improves safety, efficiency, and response time.",
            "Manual operation increases risk of error."
        ],
        resolution_strategy="Mandate integration review and testing for all pump systems.",
        entity_scope="All MECH01_pump_systems process control",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 5.1; Company Standard ENG-PS-008"
    ),
    DoctrineBlock(
        topic="Pump System Decommissioning and Disposal",
        keywords=["decommissioning", "disposal", "environmental compliance", "asset retirement", "documentation"],
        conclusion_template="Follow standardized decommissioning and disposal procedures for pump systems.",
        reasoning_framework="""Develop decommissioning plan including isolation, draining, cleaning, and removal. Dispose of pumps and associated materials per environmental regulations. Document asset retirement and update records. Recover and recycle materials where feasible. Review process for lessons learned and continuous improvement.""",
        key_factors=["Decommissioning plan", "Environmental compliance", "Asset records", "Recycling", "Lessons learned"],
        primary_authority=["EPA Regulations", "Company Asset Management Standards"],
        burden_holder="Project Manager",
        adversary_position="Abandoning equipment in place or improper disposal.",
        counter_arguments=[
            "Improper disposal results in environmental violations.",
            "Proper decommissioning supports sustainability and compliance."
        ],
        resolution_strategy="Mandate decommissioning plans and compliance audits.",
        entity_scope="All MECH01_pump_systems retirements",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA 40 CFR; Company Procedure ASM-PS-004"
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
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]