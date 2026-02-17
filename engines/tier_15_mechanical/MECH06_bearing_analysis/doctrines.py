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
        topic="Rolling Bearing Life Calculation - ISO 281",
        keywords=["bearing life", "ISO 281", "L10", "dynamic load rating", "fatigue"],
        conclusion_template="The basic rating life (L10) of a rolling bearing is calculated using ISO 281, considering dynamic load rating and applied equivalent load.",
        reasoning_framework=(
            "ISO 281 provides the standard method for calculating the basic rating life (L10) of rolling bearings. "
            "The L10 life is the number of revolutions at which 90% of a group of identical bearings will still be operational. "
            "The formula is L10 = (C/P)^p * 10^6 revolutions, where C is the dynamic load rating, P is the equivalent dynamic bearing load, "
            "and p is 3 for ball bearings and 10/3 for roller bearings. Application factors, lubrication, contamination, and material quality "
            "can affect actual bearing life. Modern approaches may use modified life calculations (ISO 281:2007) incorporating reliability, lubrication, and contamination factors."
        ),
        key_factors=["Dynamic load rating (C)", "Equivalent dynamic load (P)", "Bearing type", "Reliability", "Lubrication", "Contamination"],
        primary_authority=["ISO 281:2007", "SKF Bearing Life Theory", "NSK Technical Handbook"],
        burden_holder="Design Engineer",
        adversary_position="The calculated life is overly optimistic and does not account for real-world conditions such as contamination and improper lubrication.",
        counter_arguments=[
            "ISO 281:2007 includes adjustment factors for lubrication and contamination.",
            "Field data supports use of modified life calculations.",
            "Proper maintenance and monitoring can mitigate real-world deviations."
        ],
        resolution_strategy="Apply modified life calculation per ISO 281:2007, including all relevant adjustment factors and field data where available.",
        entity_scope="All rolling bearings in MECH06 engine assemblies",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 281:2007"
    ),
    DoctrineBlock(
        topic="Bearing Fit Selection - Shaft and Housing",
        keywords=["bearing fit", "shaft tolerance", "housing tolerance", "interference fit", "clearance fit"],
        conclusion_template="Bearing fits for shaft and housing are selected based on load direction, operating temperature, and mounting conditions, following ISO 286-1/2.",
        reasoning_framework=(
            "Proper selection of bearing fits is critical to prevent bearing creep, fretting, or excessive preload. "
            "ISO 286-1/2 specifies tolerance classes for shafts (h, k, m, n, p, r, s) and housings (H, J, K, M, N, P, R, S). "
            "Rotating inner rings under load require interference fits (e.g., k5, m5), while stationary rings may use clearance fits (e.g., H7). "
            "Thermal expansion, shaft/housing material, and mounting/dismounting requirements must be considered. "
            "For high-speed or temperature applications, additional allowance for expansion is necessary."
        ),
        key_factors=["Load direction", "Ring rotation", "Temperature", "Mounting/dismounting", "Material properties"],
        primary_authority=["ISO 286-1:2010", "SKF Bearing Fitting Practices", "NSK Bearing Fit Tables"],
        burden_holder="Mechanical Designer",
        adversary_position="Standard fits may not accommodate thermal expansion or high-speed operation, leading to bearing damage.",
        counter_arguments=[
            "Fit selection tables include recommendations for temperature and speed.",
            "Special fits can be specified for extreme conditions.",
            "Field experience supports standard fits with proper allowances."
        ],
        resolution_strategy="Select fits per ISO 286-1/2, adjusting for temperature and speed as needed; document any deviations.",
        entity_scope="All bearing seats in MECH06 engine",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 286-1:2010"
    ),
    DoctrineBlock(
        topic="Bearing Lubrication Selection - Grease vs Oil",
        keywords=["lubrication", "grease", "oil", "bearing life", "operating temperature"],
        conclusion_template="Lubrication method (grease or oil) is selected based on speed, temperature, load, and maintenance interval requirements.",
        reasoning_framework=(
            "Grease lubrication is preferred for moderate speeds, lower temperatures, and where maintenance intervals are long. "
            "Oil lubrication is required for high-speed, high-temperature, or heavily loaded applications. "
            "Grease provides better sealing and contaminant exclusion, but has limited heat dissipation. "
            "Oil can be circulated and cooled, extending bearing life under demanding conditions. "
            "Selection should consider DN value (bearing bore x speed), operating temperature, and environmental contamination."
        ),
        key_factors=["Speed (DN value)", "Temperature", "Load", "Maintenance interval", "Contamination"],
        primary_authority=["SKF Lubrication Handbook", "NSK Lubrication Guide", "ISO 281"],
        burden_holder="Maintenance Engineer",
        adversary_position="Grease may degrade under high temperature or speed, leading to premature failure.",
        counter_arguments=[
            "Oil lubrication systems are more complex and costly.",
            "Modern greases can operate at higher temperatures.",
            "Condition monitoring can extend grease intervals."
        ],
        resolution_strategy="Select lubrication per bearing manufacturer guidelines and application DN value; validate with field trials.",
        entity_scope="All lubricated bearings in MECH06 engine",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SKF Lubrication Handbook"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Fatigue Spalling",
        keywords=["bearing failure", "fatigue", "spalling", "surface distress", "subsurface cracks"],
        conclusion_template="Fatigue spalling is diagnosed by characteristic flaking of raceways or rolling elements, typically after expected life.",
        reasoning_framework=(
            "Fatigue spalling occurs when cyclic stresses exceed material endurance, leading to subsurface crack initiation and propagation. "
            "Spalling appears as flaked or pitted areas on raceways or rolling elements. "
            "Root causes include excessive load, inadequate lubrication, contamination, or improper fit. "
            "Analysis involves visual inspection, metallurgical examination, and review of operating history. "
            "Corrective actions focus on load reduction, improved lubrication, and contamination control."
        ),
        key_factors=["Operating load", "Lubrication", "Contamination", "Fit", "Material quality"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Other failure modes (e.g., brinelling, electrical erosion) may mimic spalling.",
        counter_arguments=[
            "Metallurgical analysis distinguishes fatigue spalling from other modes.",
            "Operating history supports fatigue diagnosis.",
            "Surface morphology is characteristic."
        ],
        resolution_strategy="Confirm diagnosis with metallurgical analysis and operating data; implement corrective actions per root cause.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Vibration Analysis - Bearing Defect Frequencies",
        keywords=["vibration analysis", "defect frequencies", "BPFO", "BPFI", "FFT", "condition monitoring"],
        conclusion_template="Characteristic bearing defect frequencies (BPFO, BPFI, BSF, FTF) are used in vibration analysis to detect faults.",
        reasoning_framework=(
            "Vibration analysis employs Fast Fourier Transform (FFT) to identify characteristic frequencies associated with bearing defects. "
            "BPFO (Ball Pass Frequency Outer), BPFI (Ball Pass Frequency Inner), BSF (Ball Spin Frequency), and FTF (Fundamental Train Frequency) "
            "are calculated from bearing geometry and shaft speed. Peaks at these frequencies indicate localized defects. "
            "Analysis should consider harmonics, sidebands, and modulation effects. Early detection enables predictive maintenance."
        ),
        key_factors=["Bearing geometry", "Shaft speed", "FFT spectrum", "Harmonics", "Modulation"],
        primary_authority=["ISO 13373-2", "SKF Vibration Diagnostic Chart", "Mobius Institute"],
        burden_holder="Condition Monitoring Specialist",
        adversary_position="Other machine faults can produce similar spectral features.",
        counter_arguments=[
            "Defect frequencies are unique to bearing geometry.",
            "Correlation with operating events improves diagnosis.",
            "Multiple methods (envelope analysis, demodulation) increase confidence."
        ],
        resolution_strategy="Combine vibration analysis with operating history and other diagnostics for confirmation.",
        entity_scope="All monitored bearings in MECH06 engine",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 13373-2"
    ),
    DoctrineBlock(
        topic="API 610 Bearing Requirements - Centrifugal Pumps",
        keywords=["API 610", "centrifugal pump", "bearing requirements", "minimum L10 life", "oil lubrication"],
        conclusion_template="Bearings in centrifugal pumps must comply with API 610, including minimum L10 life and lubrication requirements.",
        reasoning_framework=(
            "API 610 specifies design and performance requirements for centrifugal pumps in petroleum, petrochemical, and gas industry services. "
            "Bearings must achieve a minimum L10 life of 25,000 hours at rated load and speed. "
            "Oil lubrication is generally required, with provisions for oil rings, mist, or forced lubrication. "
            "Temperature monitoring and vibration limits are mandated. "
            "Compliance ensures reliability and safety in critical applications."
        ),
        key_factors=["L10 life", "Lubrication method", "Temperature monitoring", "Vibration limits", "Material selection"],
        primary_authority=["API 610 12th Edition", "ANSI/HI 9.6.5", "OEM Specifications"],
        burden_holder="Project Engineer",
        adversary_position="API 610 requirements may exceed application needs, increasing cost.",
        counter_arguments=[
            "API 610 compliance is often a client or regulatory requirement.",
            "Longer bearing life reduces downtime and maintenance.",
            "Standardization simplifies procurement and support."
        ],
        resolution_strategy="Design and specify bearings per API 610; document any deviations and obtain client approval.",
        entity_scope="All centrifugal pump bearings in MECH06 engine",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 610 12th Edition"
    ),
    DoctrineBlock(
        topic="Journal Bearing Design - Hydrodynamic Lubrication",
        keywords=["journal bearing", "hydrodynamic lubrication", "film thickness", "Sommerfeld number", "viscosity"],
        conclusion_template="Journal bearings are designed to maintain a hydrodynamic film under all operating conditions, ensuring separation of surfaces.",
        reasoning_framework=(
            "Hydrodynamic journal bearings rely on a continuous lubricant film to separate shaft and bearing surfaces, preventing metal-to-metal contact. "
            "Design involves calculating minimum film thickness, pressure distribution, and temperature rise. "
            "The Sommerfeld number characterizes operating conditions. Lubricant viscosity, shaft speed, load, and bearing geometry are critical. "
            "Failure to maintain film leads to wear, seizure, or catastrophic failure. Monitoring and control of operating parameters is essential."
        ),
        key_factors=["Film thickness", "Viscosity", "Shaft speed", "Load", "Bearing geometry", "Temperature"],
        primary_authority=["ISO 12130-1", "Kingsbury Bearing Design Guide", "MIT Tribology Lecture Notes"],
        burden_holder="Bearing Designer",
        adversary_position="Transient loads or start/stop conditions may cause film breakdown.",
        counter_arguments=[
            "Proper selection of start-up procedures and lubricant minimizes risk.",
            "Auxiliary systems (jacking oil) can support film formation.",
            "Design margins account for transient events."
        ],
        resolution_strategy="Design for worst-case conditions; implement monitoring and auxiliary systems as needed.",
        entity_scope="All journal bearings in MECH06 engine",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 12130-1"
    ),
    DoctrineBlock(
        topic="Tilting Pad Bearing Design - Turbomachinery",
        keywords=["tilting pad", "journal bearing", "turbomachinery", "load capacity", "dynamic stability"],
        conclusion_template="Tilting pad bearings are used in high-speed turbomachinery for superior stability and load capacity.",
        reasoning_framework=(
            "Tilting pad bearings consist of multiple pads that pivot to form a self-aligning hydrodynamic film. "
            "They accommodate shaft misalignment, reduce vibration, and provide high load capacity. "
            "Design considers pad geometry, pivot location, preload, and lubrication method. "
            "Dynamic stability is enhanced, making them suitable for turbines, compressors, and generators. "
            "Proper selection ensures reliability in critical rotating equipment."
        ),
        key_factors=["Pad geometry", "Pivot location", "Preload", "Lubrication", "Operating speed"],
        primary_authority=["API 612", "Kingsbury Tilting Pad Handbook", "ISO 12130-2"],
        burden_holder="Rotordynamics Engineer",
        adversary_position="Tilting pad bearings are more complex and costly than fixed geometry designs.",
        counter_arguments=[
            "Performance benefits justify cost in high-speed applications.",
            "Reduced vibration extends machine life.",
            "Field experience supports reliability."
        ],
        resolution_strategy="Specify tilting pad bearings for high-speed, high-load applications; justify selection with rotordynamic analysis.",
        entity_scope="All turbomachinery in MECH06 engine",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 612"
    ),
    DoctrineBlock(
        topic="Bearing Contamination Control - ISO 4406 Codes",
        keywords=["contamination", "ISO 4406", "particle count", "lubricant cleanliness", "wear"],
        conclusion_template="Bearing lubricant cleanliness is controlled per ISO 4406 codes, with target levels based on application criticality.",
        reasoning_framework=(
            "ISO 4406 defines cleanliness codes for lubricants based on particle counts at 4, 6, and 14 microns. "
            "Contamination accelerates bearing wear and failure. Target codes (e.g., 18/16/13) are set based on bearing size, speed, and criticality. "
            "Filtration, sealing, and regular monitoring are essential for control. Exceeding limits requires corrective action."
        ),
        key_factors=["Particle count", "Lubricant type", "Bearing size", "Filtration", "Monitoring frequency"],
        primary_authority=["ISO 4406:2017", "SKF Lubrication Guide", "ASTM D7647"],
        burden_holder="Maintenance Supervisor",
        adversary_position="Strict cleanliness targets increase maintenance cost and complexity.",
        counter_arguments=[
            "Cleanliness directly correlates with bearing life.",
            "Improved filtration reduces long-term costs.",
            "Condition monitoring optimizes maintenance intervals."
        ],
        resolution_strategy="Implement filtration and monitoring to maintain ISO 4406 targets; adjust intervals based on field data.",
        entity_scope="All lubricated bearings in MECH06 engine",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 4406:2017"
    ),
    DoctrineBlock(
        topic="Bearing Brinelling vs False Brinelling",
        keywords=["brinelling", "false brinelling", "indentation", "vibration", "static load"],
        conclusion_template="True brinelling is caused by static overload, while false brinelling results from vibration-induced micro-movement.",
        reasoning_framework=(
            "Brinelling refers to permanent indentations in bearing raceways caused by static overload or impact. "
            "False brinelling produces similar marks but results from vibration or oscillation under light load, causing lubricant film breakdown. "
            "Distinguishing features include the shape, location, and surface appearance of indentations. "
            "Prevention focuses on proper handling, storage, and vibration isolation."
        ),
        key_factors=["Load history", "Vibration exposure", "Indentation morphology", "Lubrication", "Handling procedures"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Failure Analyst",
        adversary_position="False brinelling may be misdiagnosed as true brinelling, leading to incorrect corrective actions.",
        counter_arguments=[
            "Detailed inspection reveals distinguishing features.",
            "Operating history clarifies failure mode.",
            "Preventive measures differ for each mode."
        ],
        resolution_strategy="Conduct thorough failure analysis and review operating conditions to determine root cause.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Electrical Erosion - VFD-Induced Bearing Damage",
        keywords=["electrical erosion", "VFD", "fluting", "EDM", "shaft voltage"],
        conclusion_template="Variable Frequency Drives (VFDs) can induce shaft voltages, causing electrical erosion and fluting in bearings.",
        reasoning_framework=(
            "VFDs generate high-frequency switching that induces shaft voltages and circulating currents. "
            "These discharge through bearing contacts, causing electrical discharge machining (EDM) and fluting damage. "
            "Symptoms include pitting, frosting, and characteristic fluted patterns on raceways. "
            "Mitigation includes insulated bearings, shaft grounding brushes, and ceramic coatings."
        ),
        key_factors=["VFD use", "Shaft voltage", "Bearing insulation", "Grounding", "Damage morphology"],
        primary_authority=["NEMA MG1", "SKF Electrical Discharge Handbook", "IEEE 841"],
        burden_holder="Electrical Engineer",
        adversary_position="Mitigation measures increase cost and complexity.",
        counter_arguments=[
            "Failure to mitigate leads to premature bearing failure.",
            "Field retrofits are more costly than initial design.",
            "Industry standards recommend mitigation."
        ],
        resolution_strategy="Specify mitigation measures for all VFD-driven motors; verify effectiveness with shaft voltage testing.",
        entity_scope="All VFD-driven motors in MECH06 engine",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NEMA MG1"
    ),
    DoctrineBlock(
        topic="Bearing Preload - Angular Contact and Tapered Roller",
        keywords=["preload", "angular contact", "tapered roller", "axial rigidity", "bearing arrangement"],
        conclusion_template="Preload is applied to angular contact and tapered roller bearings to increase rigidity and control axial movement.",
        reasoning_framework=(
            "Preload eliminates internal clearance, increasing axial and radial rigidity. "
            "It is essential for high-speed, high-precision applications. "
            "Preload can be achieved by axial displacement, matched bearing sets, or springs. "
            "Excessive preload increases friction and heat, risking failure. "
            "Calculation and control of preload are critical during assembly."
        ),
        key_factors=["Bearing type", "Preload method", "Axial load", "Operating speed", "Assembly procedure"],
        primary_authority=["ISO 1132-1", "SKF Preload Guidelines", "NSK Precision Bearing Handbook"],
        burden_holder="Assembly Technician",
        adversary_position="Improper preload leads to excessive heat or reduced bearing life.",
        counter_arguments=[
            "Use of matched sets and precision spacers controls preload.",
            "Assembly procedures include preload checks.",
            "Field failures are often due to assembly errors."
        ],
        resolution_strategy="Follow manufacturer preload recommendations and verify during assembly.",
        entity_scope="All angular contact and tapered roller bearings in MECH06 engine",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 1132-1"
    ),
    DoctrineBlock(
        topic="Bearing Mounting and Dismounting Procedures",
        keywords=["mounting", "dismounting", "heating", "mechanical tools", "safety"],
        conclusion_template="Proper mounting and dismounting procedures are essential to avoid bearing damage and ensure safety.",
        reasoning_framework=(
            "Bearings must be mounted using correct tools and methods to prevent damage. "
            "Thermal expansion (heating) is used for interference fits, while mechanical or hydraulic tools are used for removal. "
            "Forcing bearings onto seats without proper support can cause brinelling or misalignment. "
            "Personal protective equipment and safety protocols are mandatory. "
            "Documentation of procedures and training reduces risk of failure."
        ),
        key_factors=["Fit type", "Tool selection", "Heating method", "Safety procedures", "Training"],
        primary_authority=["ISO 15243:2017", "SKF Mounting Handbook", "OSHA Safety Standards"],
        burden_holder="Maintenance Technician",
        adversary_position="Improper procedures lead to hidden damage and reduced bearing life.",
        counter_arguments=[
            "Standardized procedures minimize risk.",
            "Training and certification improve outcomes.",
            "Field audits confirm compliance."
        ],
        resolution_strategy="Implement and audit standardized mounting/dismounting procedures; require training and PPE.",
        entity_scope="All bearing maintenance in MECH06 engine",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Clearance Selection - C2, CN, C3, C4",
        keywords=["bearing clearance", "C2", "CN", "C3", "C4", "thermal expansion"],
        conclusion_template="Internal bearing clearance is selected based on fit, temperature, and operating conditions.",
        reasoning_framework=(
            "Bearing internal clearance affects load distribution, heat generation, and service life. "
            "C2 is less than normal, CN is normal, C3/C4 are greater than normal. "
            "Tight fits and high operating temperatures reduce effective clearance. "
            "Selection must account for shaft/housing fits, thermal expansion, and application requirements. "
            "Incorrect clearance leads to noise, vibration, or premature failure."
        ),
        key_factors=["Fit type", "Operating temperature", "Application", "Shaft/housing material", "Speed"],
        primary_authority=["ISO 5753-1", "SKF Clearance Tables", "NSK Application Guide"],
        burden_holder="Design Engineer",
        adversary_position="Standard clearance may be inadequate for high temperature or interference fits.",
        counter_arguments=[
            "Manufacturer tables provide guidance for fit and temperature.",
            "Field experience supports selection adjustments.",
            "Clearance can be measured after assembly."
        ],
        resolution_strategy="Select clearance per manufacturer guidelines; verify after assembly and adjust if necessary.",
        entity_scope="All rolling bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 5753-1"
    ),
    DoctrineBlock(
        topic="Bearing Material Selection - Through-Hardened vs Case-Hardened",
        keywords=["bearing material", "through-hardened", "case-hardened", "fatigue", "contamination"],
        conclusion_template="Material selection (through-hardened or case-hardened) is based on load, contamination, and application requirements.",
        reasoning_framework=(
            "Through-hardened bearings offer uniform hardness and are suitable for clean, moderate-load applications. "
            "Case-hardened bearings have a tough core and hard surface, providing better resistance to shock and contamination. "
            "Material selection impacts fatigue life, wear resistance, and failure modes. "
            "Application environment and expected loads guide the choice."
        ),
        key_factors=["Load", "Contamination", "Shock loading", "Application environment", "Cost"],
        primary_authority=["ISO 683-17", "SKF Material Guide", "ASTM A485"],
        burden_holder="Design Engineer",
        adversary_position="Case-hardened bearings are more expensive and may not be necessary for all applications.",
        counter_arguments=[
            "Contaminated environments justify higher cost.",
            "Field failures support use of case-hardened materials.",
            "Life-cycle cost analysis favors durability."
        ],
        resolution_strategy="Select material based on application risk assessment and field experience.",
        entity_scope="All rolling bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 683-17"
    ),
    DoctrineBlock(
        topic="Bearing Sealing - Contact vs Non-Contact",
        keywords=["sealing", "contact seal", "non-contact seal", "contamination", "friction"],
        conclusion_template="Seal type is selected based on contamination risk, speed, and allowable friction.",
        reasoning_framework=(
            "Contact seals provide superior exclusion of contaminants but increase friction and heat. "
            "Non-contact seals (shields, labyrinth) offer lower friction and are suitable for high-speed or low-contamination environments. "
            "Seal selection impacts bearing life, maintenance intervals, and energy consumption. "
            "Application risk assessment guides the choice."
        ),
        key_factors=["Contamination risk", "Operating speed", "Temperature", "Maintenance interval", "Energy efficiency"],
        primary_authority=["ISO 15243:2017", "SKF Sealing Handbook", "NSK Application Guide"],
        burden_holder="Design Engineer",
        adversary_position="Contact seals may overheat at high speed, while non-contact seals may admit contaminants.",
        counter_arguments=[
            "Hybrid designs (e.g., labyrinth + contact) can be used.",
            "Field testing validates seal selection.",
            "Maintenance intervals can be adjusted."
        ],
        resolution_strategy="Select seal type based on contamination and speed; validate with field performance data.",
        entity_scope="All sealed bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Cage Material and Design",
        keywords=["cage material", "steel cage", "polyamide cage", "brass cage", "high speed"],
        conclusion_template="Cage material and design are selected based on speed, temperature, and application requirements.",
        reasoning_framework=(
            "Steel cages are standard for most applications, offering strength and durability. "
            "Polyamide cages reduce weight and friction, suitable for high-speed, low-temperature environments. "
            "Brass cages provide superior resistance to shock and vibration. "
            "Cage design (rivet, snap, machined) impacts performance and reliability. "
            "Selection must consider compatibility with lubricant and operating conditions."
        ),
        key_factors=["Operating speed", "Temperature", "Shock/vibration", "Lubricant compatibility", "Cost"],
        primary_authority=["ISO 15243:2017", "SKF Cage Design Guide", "NSK Application Guide"],
        burden_holder="Design Engineer",
        adversary_position="Polyamide cages may degrade at high temperature; brass cages increase cost.",
        counter_arguments=[
            "Material selection tables provide guidance.",
            "Field failures inform design improvements.",
            "Testing validates cage performance."
        ],
        resolution_strategy="Select cage material per manufacturer recommendations and application conditions.",
        entity_scope="All rolling bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Lubricant Replenishment Interval",
        keywords=["lubricant interval", "grease life", "oil change", "maintenance schedule"],
        conclusion_template="Lubricant replenishment intervals are determined by bearing type, operating conditions, and manufacturer guidelines.",
        reasoning_framework=(
            "Grease life is influenced by bearing size, speed, temperature, and contamination. "
            "Oil change intervals depend on lubricant degradation, contamination, and monitoring results. "
            "Manufacturer charts and condition monitoring guide interval selection. "
            "Failure to replenish lubricant leads to premature failure."
        ),
        key_factors=["Bearing type", "Operating speed", "Temperature", "Contamination", "Lubricant type"],
        primary_authority=["SKF Lubrication Handbook", "NSK Maintenance Guide", "ISO 281"],
        burden_holder="Maintenance Planner",
        adversary_position="Intervals may be too conservative or aggressive for actual conditions.",
        counter_arguments=[
            "Condition monitoring allows interval optimization.",
            "Field data supports adjustment.",
            "Manufacturer guidelines are based on extensive testing."
        ],
        resolution_strategy="Set intervals per guidelines and adjust based on condition monitoring and field experience.",
        entity_scope="All lubricated bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SKF Lubrication Handbook"
    ),
    DoctrineBlock(
        topic="Bearing Misalignment Tolerance",
        keywords=["misalignment", "tolerance", "self-aligning bearing", "failure mode"],
        conclusion_template="Misalignment tolerance is determined by bearing type and mounting accuracy.",
        reasoning_framework=(
            "Self-aligning bearings (e.g., spherical roller, self-aligning ball) tolerate greater misalignment than rigid types. "
            "Excessive misalignment causes edge loading, increased stress, and premature failure. "
            "Mounting accuracy and shaft/housing geometry are critical. "
            "Manufacturer specifications provide allowable misalignment values."
        ),
        key_factors=["Bearing type", "Mounting accuracy", "Shaft/housing geometry", "Operating load"],
        primary_authority=["ISO 15243:2017", "SKF Application Guide", "NSK Technical Handbook"],
        burden_holder="Assembly Technician",
        adversary_position="Actual misalignment may exceed bearing tolerance, leading to hidden failures.",
        counter_arguments=[
            "Precision alignment tools reduce error.",
            "Field measurements verify installation.",
            "Design margins account for minor misalignment."
        ],
        resolution_strategy="Select bearing type for expected misalignment; verify alignment during assembly.",
        entity_scope="All bearing assemblies in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Operating Temperature Limits",
        keywords=["operating temperature", "limit", "lubricant degradation", "bearing steel"],
        conclusion_template="Operating temperature limits are set by bearing material, lubricant, and application.",
        reasoning_framework=(
            "Standard bearing steels operate up to 120°C; special materials extend limits. "
            "Lubricant degradation often sets the practical limit. "
            "Continuous operation above limits reduces life, increases wear, and risks failure. "
            "Temperature monitoring and alarms are recommended for critical applications."
        ),
        key_factors=["Bearing material", "Lubricant type", "Application", "Monitoring", "Ambient temperature"],
        primary_authority=["SKF Application Guide", "NSK Technical Handbook", "ISO 15243:2017"],
        burden_holder="Design Engineer",
        adversary_position="Transient temperature excursions may not be detected by average monitoring.",
        counter_arguments=[
            "Peak temperature logging improves detection.",
            "Material selection can provide margin.",
            "Field experience informs alarm settings."
        ],
        resolution_strategy="Set limits per lowest-rated component; implement monitoring and alarms.",
        entity_scope="All bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SKF Application Guide"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Lubrication Starvation",
        keywords=["failure analysis", "lubrication starvation", "scoring", "discoloration"],
        conclusion_template="Lubrication starvation is diagnosed by scoring, discoloration, and evidence of lubricant loss.",
        reasoning_framework=(
            "Lubrication starvation occurs when insufficient lubricant reaches the contact surfaces, causing metal-to-metal contact. "
            "Symptoms include scoring, bluing/discoloration, and rapid wear. "
            "Root causes include blocked passages, incorrect lubricant, or excessive speed. "
            "Analysis involves inspection, review of lubrication system, and operating history."
        ),
        key_factors=["Lubricant supply", "Operating speed", "System design", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Other failure modes (e.g., contamination) may produce similar symptoms.",
        counter_arguments=[
            "Inspection of lubricant passages clarifies cause.",
            "Operating history supports diagnosis.",
            "Contamination produces different wear patterns."
        ],
        resolution_strategy="Confirm diagnosis with inspection and system review; correct root cause.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Contamination",
        keywords=["failure analysis", "contamination", "abrasive wear", "particle ingress"],
        conclusion_template="Contamination failure is diagnosed by abrasive wear, embedded particles, and lubricant analysis.",
        reasoning_framework=(
            "Contaminants (dirt, wear particles, water) enter bearings via seals, lubricant, or assembly. "
            "Abrasive wear, surface scoring, and embedded particles are characteristic. "
            "Lubricant analysis reveals elevated particle counts. "
            "Prevention focuses on sealing, filtration, and clean assembly procedures."
        ),
        key_factors=["Particle count", "Seal condition", "Lubricant analysis", "Assembly procedures"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Contamination may be secondary to other failure modes.",
        counter_arguments=[
            "Lubricant analysis distinguishes primary from secondary contamination.",
            "Seal inspection supports diagnosis.",
            "Field experience informs corrective actions."
        ],
        resolution_strategy="Confirm contamination as root cause; implement preventive measures.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Overload",
        keywords=["failure analysis", "overload", "plastic deformation", "spalling"],
        conclusion_template="Overload failure is diagnosed by plastic deformation, excessive spalling, and evidence of excessive load.",
        reasoning_framework=(
            "Overload occurs when applied loads exceed bearing capacity, causing plastic deformation, excessive spalling, and rapid failure. "
            "Root causes include incorrect selection, unexpected process loads, or misassembly. "
            "Analysis involves review of load history, inspection for deformation, and verification of bearing selection."
        ),
        key_factors=["Load history", "Deformation", "Selection review", "Operating conditions"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Other failure modes may cause similar damage.",
        counter_arguments=[
            "Load history and selection review clarify root cause.",
            "Plastic deformation is characteristic of overload.",
            "Field data supports diagnosis."
        ],
        resolution_strategy="Confirm overload as root cause; review selection and operating conditions.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Corrosion",
        keywords=["failure analysis", "corrosion", "rust", "moisture ingress"],
        conclusion_template="Corrosion failure is diagnosed by rust, pitting, and evidence of moisture ingress.",
        reasoning_framework=(
            "Corrosion occurs when moisture or chemicals enter the bearing, causing rust, pitting, and surface degradation. "
            "Root causes include poor sealing, condensation, or improper storage. "
            "Analysis involves visual inspection, lubricant analysis, and review of environmental conditions."
        ),
        key_factors=["Moisture ingress", "Seal condition", "Storage conditions", "Lubricant analysis"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Corrosion may be secondary to other failure modes.",
        counter_arguments=[
            "Lubricant analysis and seal inspection clarify root cause.",
            "Environmental monitoring supports diagnosis.",
            "Preventive measures reduce recurrence."
        ],
        resolution_strategy="Confirm corrosion as root cause; improve sealing and storage.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Electrical Erosion",
        keywords=["failure analysis", "electrical erosion", "fluting", "pitting"],
        conclusion_template="Electrical erosion is diagnosed by fluting, pitting, and evidence of electrical discharge.",
        reasoning_framework=(
            "Electrical erosion results from current passing through bearing contacts, causing localized melting, pitting, and fluted patterns. "
            "Root causes include VFD operation, inadequate grounding, or insulation failure. "
            "Analysis involves inspection, shaft voltage measurement, and review of electrical system."
        ),
        key_factors=["Shaft voltage", "Grounding", "Damage morphology", "Electrical system review"],
        primary_authority=["NEMA MG1", "SKF Electrical Discharge Handbook", "IEEE 841"],
        burden_holder="Reliability Engineer",
        adversary_position="Other failure modes may produce similar surface features.",
        counter_arguments=[
            "Fluting is characteristic of electrical erosion.",
            "Shaft voltage measurements confirm diagnosis.",
            "Field experience supports corrective actions."
        ],
        resolution_strategy="Confirm electrical erosion as root cause; implement mitigation measures.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NEMA MG1"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Cage Failure",
        keywords=["failure analysis", "cage failure", "fracture", "wear"],
        conclusion_template="Cage failure is diagnosed by fracture, excessive wear, and evidence of misalignment or lubrication issues.",
        reasoning_framework=(
            "Cage failure may result from material defects, misalignment, lubrication starvation, or excessive vibration. "
            "Symptoms include cage fracture, wear, or displacement. "
            "Root cause analysis involves inspection, review of operating conditions, and material evaluation."
        ),
        key_factors=["Cage material", "Misalignment", "Lubrication", "Operating conditions"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Cage failure may be secondary to other failure modes.",
        counter_arguments=[
            "Inspection and operating history clarify root cause.",
            "Material analysis supports diagnosis.",
            "Preventive measures reduce recurrence."
        ],
        resolution_strategy="Confirm cage failure as root cause; address underlying issues.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Creep",
        keywords=["failure analysis", "creep", "raceway movement", "fit"],
        conclusion_template="Creep is diagnosed by evidence of raceway movement relative to shaft or housing.",
        reasoning_framework=(
            "Creep occurs when bearing rings move relative to their seats due to inadequate fit or improper mounting. "
            "Symptoms include shiny bands, wear marks, or fretting corrosion at the seat interface. "
            "Root causes include insufficient interference, thermal expansion, or vibration. "
            "Analysis involves inspection and review of fit selection and mounting procedures."
        ),
        key_factors=["Fit selection", "Mounting procedure", "Thermal expansion", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Creep may be mistaken for other forms of wear.",
        counter_arguments=[
            "Inspection of seat interface clarifies diagnosis.",
            "Fit and mounting review supports findings.",
            "Field experience informs corrective actions."
        ],
        resolution_strategy="Confirm creep as root cause; improve fit and mounting procedures.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Fretting Corrosion",
        keywords=["failure analysis", "fretting corrosion", "vibration", "micro-movement"],
        conclusion_template="Fretting corrosion is diagnosed by reddish-brown deposits and wear at contact interfaces.",
        reasoning_framework=(
            "Fretting corrosion results from micro-movement between bearing rings and seats under vibration. "
            "Symptoms include reddish-brown oxide deposits, pitting, and wear at the interface. "
            "Root causes include inadequate fit, vibration, or insufficient preload. "
            "Analysis involves inspection and review of operating conditions."
        ),
        key_factors=["Fit selection", "Vibration exposure", "Preload", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Fretting corrosion may be mistaken for other forms of corrosion.",
        counter_arguments=[
            "Deposit color and location are characteristic.",
            "Operating history supports diagnosis.",
            "Preventive measures are well established."
        ],
        resolution_strategy="Confirm fretting corrosion as root cause; improve fit and vibration isolation.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - False Brinelling",
        keywords=["failure analysis", "false brinelling", "vibration", "micro-movement"],
        conclusion_template="False brinelling is diagnosed by shallow indentations at rolling element spacing, without plastic deformation.",
        reasoning_framework=(
            "False brinelling occurs due to vibration or oscillation under light load, causing lubricant film breakdown and micro-movement. "
            "Symptoms include shallow, regularly spaced indentations without plastic deformation. "
            "Root causes include transport vibration, improper storage, or standby operation. "
            "Analysis involves inspection and review of operating history."
        ),
        key_factors=["Vibration exposure", "Load history", "Storage conditions", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="False brinelling may be confused with true brinelling.",
        counter_arguments=[
            "Indentation morphology and operating history distinguish modes.",
            "Preventive measures differ.",
            "Field experience supports diagnosis."
        ],
        resolution_strategy="Confirm false brinelling as root cause; improve storage and vibration isolation.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - True Brinelling",
        keywords=["failure analysis", "true brinelling", "static overload", "indentation"],
        conclusion_template="True brinelling is diagnosed by deep indentations matching rolling element geometry, with evidence of overload.",
        reasoning_framework=(
            "True brinelling results from static overload or impact, causing deep, permanent indentations in raceways. "
            "Symptoms include indentations matching rolling element geometry, often accompanied by plastic deformation. "
            "Root causes include improper handling, assembly, or excessive static load. "
            "Analysis involves inspection and review of load history."
        ),
        key_factors=["Load history", "Handling procedures", "Indentation morphology", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="True brinelling may be confused with false brinelling.",
        counter_arguments=[
            "Indentation depth and morphology distinguish modes.",
            "Load history supports diagnosis.",
            "Preventive measures are well established."
        ],
        resolution_strategy="Confirm true brinelling as root cause; improve handling and assembly procedures.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Smearing",
        keywords=["failure analysis", "smearing", "adhesive wear", "high speed"],
        conclusion_template="Smearing is diagnosed by streaks or smears on raceways and rolling elements, often in high-speed applications.",
        reasoning_framework=(
            "Smearing occurs when lubricant film breaks down under high speed or acceleration, causing adhesive transfer of material. "
            "Symptoms include streaks, smears, and surface roughening. "
            "Root causes include inadequate lubrication, rapid acceleration, or improper clearance. "
            "Analysis involves inspection and review of operating conditions."
        ),
        key_factors=["Operating speed", "Lubrication", "Clearance", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Smearing may be mistaken for other forms of wear.",
        counter_arguments=[
            "Surface morphology and operating history clarify diagnosis.",
            "Preventive measures are well established.",
            "Field experience supports findings."
        ],
        resolution_strategy="Confirm smearing as root cause; improve lubrication and clearance selection.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Wear",
        keywords=["failure analysis", "wear", "surface degradation", "abrasion"],
        conclusion_template="Wear is diagnosed by surface degradation, loss of material, and increased clearance.",
        reasoning_framework=(
            "Wear results from prolonged operation, inadequate lubrication, or contamination. "
            "Symptoms include surface roughening, loss of material, and increased clearance. "
            "Root causes include lubricant breakdown, ingress of particles, or improper fit. "
            "Analysis involves inspection and review of maintenance history."
        ),
        key_factors=["Lubrication", "Contamination", "Fit", "Maintenance history"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Wear may be secondary to other failure modes.",
        counter_arguments=[
            "Inspection and maintenance history clarify root cause.",
            "Preventive measures are well established.",
            "Field experience supports findings."
        ],
        resolution_strategy="Confirm wear as root cause; improve lubrication and contamination control.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Fracture",
        keywords=["failure analysis", "fracture", "crack", "brittle failure"],
        conclusion_template="Fracture is diagnosed by crack propagation, sudden failure, and evidence of overload or material defect.",
        reasoning_framework=(
            "Fracture occurs due to overload, material defect, or fatigue crack propagation. "
            "Symptoms include visible cracks, sudden failure, and separation of components. "
            "Root causes include excessive load, improper material, or undetected fatigue. "
            "Analysis involves inspection, material evaluation, and review of operating history."
        ),
        key_factors=["Load history", "Material quality", "Inspection findings", "Operating conditions"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Fracture may be secondary to other failure modes.",
        counter_arguments=[
            "Material analysis and load history clarify root cause.",
            "Field experience supports findings.",
            "Preventive measures are well established."
        ],
        resolution_strategy="Confirm fracture as root cause; improve material selection and load control.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Plastic Deformation",
        keywords=["failure analysis", "plastic deformation", "overload", "indentation"],
        conclusion_template="Plastic deformation is diagnosed by permanent distortion of bearing components, typically due to overload.",
        reasoning_framework=(
            "Plastic deformation occurs when loads exceed material yield strength, causing permanent distortion. "
            "Symptoms include bent cages, deformed rings, or altered geometry. "
            "Root causes include excessive load, improper assembly, or impact. "
            "Analysis involves inspection and review of load history."
        ),
        key_factors=["Load history", "Material properties", "Assembly procedures", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Plastic deformation may be mistaken for brinelling or fracture.",
        counter_arguments=[
            "Morphology and load history clarify diagnosis.",
            "Preventive measures are well established.",
            "Field experience supports findings."
        ],
        resolution_strategy="Confirm plastic deformation as root cause; improve load control and assembly procedures.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    DoctrineBlock(
        topic="Bearing Failure Analysis - Surface Distress",
        keywords=["failure analysis", "surface distress", "micropitting", "grey staining"],
        conclusion_template="Surface distress is diagnosed by micropitting, grey staining, and surface roughening.",
        reasoning_framework=(
            "Surface distress (micropitting) results from lubricant film breakdown and high contact stress. "
            "Symptoms include grey staining, surface roughening, and micropitting. "
            "Root causes include inadequate lubrication, excessive load, or improper surface finish. "
            "Analysis involves inspection and review of operating conditions."
        ),
        key_factors=["Lubrication", "Load", "Surface finish", "Inspection findings"],
        primary_authority=["ISO 15243:2017", "SKF Bearing Damage Guide", "ASTM E1820"],
        burden_holder="Reliability Engineer",
        adversary_position="Surface distress may be mistaken for fatigue or wear.",
        counter_arguments=[
            "Morphology and operating history clarify diagnosis.",
            "Preventive measures are well established.",
            "Field experience supports findings."
        ],
        resolution_strategy="Confirm surface distress as root cause; improve lubrication and surface finish.",
        entity_scope="All failed bearings in MECH06 engine",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15243:2017"
    ),
    # Add additional doctrine blocks as needed to reach 40+
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