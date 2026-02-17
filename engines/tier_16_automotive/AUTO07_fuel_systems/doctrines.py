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
        topic="GDI High Pressure System Design",
        keywords=["GDI", "high pressure", "fuel system", "pump", "injector", "pressure dynamics"],
        conclusion_template="The design of the GDI high pressure system must ensure consistent pressure delivery within specified tolerances to optimize combustion efficiency and reduce emissions.",
        reasoning_framework=(
            "Gasoline Direct Injection (GDI) systems operate under significantly higher pressures than conventional fuel injection systems. "
            "The reasoning framework involves analyzing the pressure generation, regulation, and delivery mechanisms to the injectors. "
            "Key considerations include the pump capacity, pressure relief valves, accumulator sizing, and fuel rail integrity. "
            "Transient response of the system under varying engine loads and speeds must be modeled to ensure stable pressure. "
            "Material compatibility and fatigue resistance of components under cyclic high pressure are evaluated to prevent failure. "
            "The framework also integrates feedback from pressure sensors and ECU control algorithms to maintain target pressure. "
            "Failure modes such as cavitation, leakage, and pressure pulsations are identified and mitigated through design. "
            "Thermal effects on fuel viscosity and pressure dynamics are incorporated to ensure consistent performance across temperature ranges. "
            "The system design must comply with regulatory emissions standards by enabling precise fuel metering and injection timing. "
            "Overall, the framework balances performance, durability, cost, and safety considerations in the high pressure fuel system design."
        ),
        key_factors=[
            "Pump capacity and reliability",
            "Fuel rail pressure stability",
            "Material fatigue resistance",
            "Pressure sensor accuracy",
            "Thermal effects on fuel",
            "Regulatory compliance",
            "Transient pressure response"
        ],
        primary_authority=[
            "SAE J2719 - Fuel Injection Equipment",
            "ISO 22854 - GDI System Requirements",
            "Bosch Technical Documentation on GDI Pumps"
        ],
        burden_holder="Fuel system design engineers",
        adversary_position="Concerns over high pressure system complexity and potential failure modes leading to engine damage",
        counter_arguments=[
            "Redundant pressure sensors and fail-safe valves mitigate risks",
            "Extensive durability testing validates component reliability",
            "Advanced materials reduce fatigue and corrosion"
        ],
        resolution_strategy="Implement rigorous design validation and real-time monitoring to ensure system integrity under all operating conditions.",
        entity_scope="Automotive GDI fuel systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bosch GDI pump design guidelines and SAE J2719 standards"
    ),
    DoctrineBlock(
        topic="Port Fuel Injection Timing and Synchronization",
        keywords=["port fuel injection", "timing", "synchronization", "engine control", "ECU", "fuel delivery"],
        conclusion_template="Precise timing and synchronization of port fuel injection are critical to achieving optimal air-fuel mixture and combustion efficiency.",
        reasoning_framework=(
            "Port fuel injection (PFI) systems inject fuel into the intake ports just upstream of the intake valves. "
            "The timing of injection relative to the intake valve opening and engine cycle directly influences fuel atomization, mixture homogeneity, and combustion stability. "
            "The reasoning framework involves mapping injection events to crankshaft position sensors and camshaft timing signals to ensure synchronization. "
            "Injection timing must account for engine speed, load, temperature, and transient conditions to optimize performance and emissions. "
            "The ECU algorithms use feedback from oxygen sensors and manifold pressure sensors to adjust injection timing dynamically. "
            "Mis-timed injection can cause fuel wall wetting, incomplete vaporization, and increased hydrocarbon emissions. "
            "The framework also considers injector response time and fuel pressure to accurately schedule injection pulses. "
            "Synchronization with ignition timing is necessary to maximize combustion efficiency and minimize knock. "
            "The system must handle multi-cylinder engines with individual injector control for cylinder balancing. "
            "Diagnostics monitor injector performance and timing deviations to maintain system health."
        ),
        key_factors=[
            "Crankshaft and camshaft position accuracy",
            "Injector response time",
            "ECU timing algorithms",
            "Fuel pressure stability",
            "Engine operating conditions",
            "Sensor feedback loops",
            "Emission control requirements"
        ],
        primary_authority=[
            "SAE J1939 - Engine Control and Diagnostics",
            "ISO 26262 - Functional Safety for Automotive Systems",
            "Bosch PFI System Design Manuals"
        ],
        burden_holder="Powertrain calibration engineers",
        adversary_position="Potential timing errors causing drivability issues and increased emissions",
        counter_arguments=[
            "Use of high-resolution sensors and real-time ECU adjustments",
            "Closed-loop feedback control with oxygen sensors",
            "Injector characterization and calibration"
        ],
        resolution_strategy="Continuous monitoring and adaptive control algorithms to maintain precise injection timing under all conditions.",
        entity_scope="Port fuel injection systems in gasoline engines",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Bosch ECU calibration standards and SAE J1939 guidelines"
    ),
    DoctrineBlock(
        topic="Fuel Pump Performance and Failure Analysis",
        keywords=["fuel pump", "performance", "failure modes", "diagnostics", "pressure delivery", "wear"],
        conclusion_template="Fuel pump performance must be continuously monitored to detect early signs of failure and ensure reliable fuel delivery.",
        reasoning_framework=(
            "Fuel pumps are critical components responsible for delivering fuel at required pressures and flow rates. "
            "The reasoning framework involves analyzing pump performance parameters such as flow rate, pressure output, electrical current draw, and noise signatures. "
            "Common failure modes include mechanical wear, electrical faults, cavitation, and contamination-induced damage. "
            "Diagnostic strategies incorporate sensor data analysis, including pressure sensors, current sensors, and acoustic sensors. "
            "Trend analysis of pump parameters over time can reveal degradation before catastrophic failure. "
            "The framework also considers environmental factors such as fuel quality, temperature, and vibration that affect pump longevity. "
            "Failure analysis includes inspection of pump components for wear patterns, corrosion, and material fatigue. "
            "Corrective actions involve maintenance schedules, filter replacements, and design improvements to enhance durability. "
            "Integration with vehicle OBD systems enables fault code generation and driver alerts for pump issues. "
            "The framework supports root cause analysis to differentiate between pump failure and upstream/downstream system faults."
        ),
        key_factors=[
            "Pump flow rate and pressure output",
            "Electrical current consumption",
            "Fuel contamination levels",
            "Operating temperature",
            "Mechanical wear indicators",
            "Sensor data trends",
            "OBD fault codes"
        ],
        primary_authority=[
            "SAE J1127 - Fuel Pump Testing Procedures",
            "ISO 15500 - Fuel System Components",
            "Automotive OEM Failure Analysis Reports"
        ],
        burden_holder="Maintenance and diagnostic engineers",
        adversary_position="Fuel pump failures leading to engine stalling and drivability loss",
        counter_arguments=[
            "Predictive maintenance based on sensor data reduces unexpected failures",
            "Improved filtration minimizes contamination damage",
            "Robust design and materials extend pump life"
        ],
        resolution_strategy="Implement comprehensive monitoring and scheduled maintenance to ensure fuel pump reliability.",
        entity_scope="Automotive fuel pump systems",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J1127 testing standards and OEM failure analysis protocols"
    ),
    DoctrineBlock(
        topic="Fuel Rail Design and Pressure Dynamics",
        keywords=["fuel rail", "pressure dynamics", "design", "pulsation", "material selection", "flow distribution"],
        conclusion_template="Fuel rail design must ensure uniform pressure distribution and minimize pressure pulsations to optimize injector performance.",
        reasoning_framework=(
            "The fuel rail serves as a manifold distributing fuel to individual injectors at consistent pressure. "
            "The reasoning framework addresses hydraulic and mechanical design aspects to maintain pressure stability and flow uniformity. "
            "Pressure pulsations caused by injector opening and closing can induce pressure waves affecting fuel delivery consistency. "
            "Design strategies include optimizing rail volume, shape, and material to dampen pulsations and withstand pressure cycles. "
            "Material selection must consider corrosion resistance, thermal expansion, and fatigue strength. "
            "Flow distribution analysis ensures equal fuel supply to all injectors, preventing cylinder-to-cylinder variation. "
            "Computational fluid dynamics (CFD) simulations support design validation by modeling flow and pressure behavior. "
            "The framework also integrates sensor placement for real-time pressure monitoring and diagnostics. "
            "Manufacturing tolerances and assembly methods impact rail integrity and sealing performance. "
            "The design must comply with safety standards to prevent leaks and withstand crash scenarios."
        ),
        key_factors=[
            "Rail volume and geometry",
            "Material corrosion resistance",
            "Pressure pulsation damping",
            "Flow distribution uniformity",
            "Thermal expansion properties",
            "Sensor integration",
            "Manufacturing quality"
        ],
        primary_authority=[
            "SAE J2601 - Fuel System Components",
            "ISO 20884 - Fuel Rail Testing",
            "Automotive Engineering Handbook - Fuel Systems"
        ],
        burden_holder="Fuel system design engineers",
        adversary_position="Potential for pressure fluctuations causing inconsistent fuel delivery and injector damage",
        counter_arguments=[
            "Use of accumulators and dampers to reduce pulsations",
            "Advanced materials and coatings to prevent corrosion",
            "Precision manufacturing to ensure tight tolerances"
        ],
        resolution_strategy="Employ simulation-driven design and rigorous testing to achieve stable fuel rail performance.",
        entity_scope="Fuel rail assemblies in automotive engines",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J2601 and ISO 20884 standards"
    ),
    DoctrineBlock(
        topic="EVAP System and Fuel Vapor Management",
        keywords=["EVAP", "fuel vapor", "emissions control", "canister", "purge valve", "leak detection"],
        conclusion_template="Effective EVAP system design and management are essential to control fuel vapor emissions and comply with environmental regulations.",
        reasoning_framework=(
            "The Evaporative Emission Control (EVAP) system captures fuel vapors from the fuel tank and fuel system to prevent atmospheric release. "
            "The reasoning framework involves the design of vapor canisters, purge valves, vent valves, and associated sensors. "
            "Fuel vapor adsorption and desorption dynamics within the charcoal canister are analyzed to optimize vapor storage and purging cycles. "
            "The framework includes leak detection methodologies such as pressure decay and vacuum tests to ensure system integrity. "
            "Control algorithms regulate purge valve operation based on engine load, temperature, and vapor concentration sensors. "
            "Material compatibility with fuel vapors and resistance to degradation over time are critical for system longevity. "
            "The system must meet regulatory standards such as EPA and CARB for evaporative emissions. "
            "Diagnostics include monitoring for leaks, stuck valves, and sensor faults, with OBD-II codes generated accordingly. "
            "Integration with the vehicle ECU enables adaptive control and fault management. "
            "The framework also considers the impact of fuel composition, including ethanol blends, on vapor pressure and system performance."
        ),
        key_factors=[
            "Canister adsorption capacity",
            "Purge valve control strategy",
            "Leak detection sensitivity",
            "Material resistance to fuel vapors",
            "Sensor accuracy",
            "Regulatory compliance",
            "Fuel composition effects"
        ],
        primary_authority=[
            "EPA 40 CFR Part 86 - Evaporative Emission Standards",
            "CARB EVAP System Guidelines",
            "SAE J1979 - OBD-II Diagnostics"
        ],
        burden_holder="Emissions control engineers",
        adversary_position="System leaks or malfunctions causing increased evaporative emissions",
        counter_arguments=[
            "Robust leak detection and diagnostics",
            "Use of durable materials and components",
            "Adaptive purge control algorithms"
        ],
        resolution_strategy="Implement comprehensive testing and real-time monitoring to maintain EVAP system integrity.",
        entity_scope="Automotive evaporative emission control systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA and CARB regulations and SAE J1979 OBD-II standards"
    ),
    DoctrineBlock(
        topic="Fuel Quality Specifications and Testing",
        keywords=["fuel quality", "specifications", "testing", "contaminants", "octane rating", "fuel standards"],
        conclusion_template="Adherence to fuel quality specifications is vital to ensure engine performance, emissions compliance, and fuel system durability.",
        reasoning_framework=(
            "Fuel quality directly affects combustion efficiency, emissions, and component longevity. "
            "The reasoning framework encompasses chemical and physical property analysis including octane rating, sulfur content, volatility, and contaminant levels. "
            "Standardized testing methods such as ASTM D4814 for gasoline and ASTM D975 for diesel define acceptable fuel parameters. "
            "Contaminants like water, particulates, and microbial growth are evaluated for their impact on fuel system components. "
            "The framework includes sampling protocols, laboratory testing techniques, and in-field rapid testing methods. "
            "Fuel additives and their interactions with base fuel and engine materials are considered. "
            "Compliance with regional and international fuel standards ensures compatibility with engine designs. "
            "Fuel quality monitoring supports warranty claims and failure analysis by correlating fuel properties with observed issues. "
            "The framework also addresses the challenges posed by alternative fuels such as ethanol blends and biodiesel. "
            "Proper fuel handling and storage practices are integrated to maintain quality from production to end use."
        ),
        key_factors=[
            "Octane and cetane ratings",
            "Sulfur and contaminant levels",
            "Volatility and vapor pressure",
            "Additive compatibility",
            "Sampling and testing accuracy",
            "Regional fuel standards",
            "Storage and handling procedures"
        ],
        primary_authority=[
            "ASTM International Fuel Standards",
            "ISO 8217 - Marine Fuel Quality",
            "EPA Fuel Quality Regulations"
        ],
        burden_holder="Fuel suppliers and quality assurance teams",
        adversary_position="Variability in fuel quality causing engine performance degradation and damage",
        counter_arguments=[
            "Strict adherence to standardized testing and certification",
            "Use of fuel additives to mitigate contaminants",
            "Regular monitoring and supplier audits"
        ],
        resolution_strategy="Maintain rigorous fuel quality control programs and integrate testing data with engine calibration.",
        entity_scope="Fuel supply chain and automotive fuel systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASTM D4814 and D975 fuel standards"
    ),
    DoctrineBlock(
        topic="E85 and Flex-Fuel System Design",
        keywords=["E85", "flex-fuel", "ethanol", "fuel system", "compatibility", "engine calibration"],
        conclusion_template="Flex-fuel system design must accommodate variable ethanol content to maintain performance and emissions compliance.",
        reasoning_framework=(
            "Flex-fuel vehicles (FFVs) operate on gasoline-ethanol blends ranging from pure gasoline to E85 (85% ethanol). "
            "The reasoning framework addresses material compatibility, fuel system calibration, and sensor integration to handle variable fuel properties. "
            "Ethanol's higher oxygen content and different stoichiometric air-fuel ratio require adaptive engine control strategies. "
            "Fuel system components such as seals, pumps, and injectors must resist ethanol-induced corrosion and swelling. "
            "Fuel composition sensors (ethanol content sensors) provide real-time data for ECU adjustments. "
            "Cold start strategies are modified due to ethanol's lower vapor pressure and different combustion characteristics. "
            "The framework includes emissions testing across the fuel blend range to ensure regulatory compliance. "
            "Fuel trim algorithms dynamically adjust injection timing and duration based on ethanol content and engine operating conditions. "
            "Durability testing evaluates long-term effects of ethanol on fuel system materials and engine components. "
            "The system must maintain drivability, fuel economy, and emissions targets regardless of fuel blend."
        ),
        key_factors=[
            "Material compatibility with ethanol",
            "Fuel composition sensing accuracy",
            "Adaptive ECU calibration",
            "Cold start enrichment strategies",
            "Emissions compliance across blends",
            "Durability under ethanol exposure",
            "Fuel system component design"
        ],
        primary_authority=[
            "SAE J2719 - Flex-Fuel Vehicle Systems",
            "EPA FFV Certification Guidelines",
            "ASTM D5798 - Ethanol Fuel Specifications"
        ],
        burden_holder="Powertrain and fuel system engineers",
        adversary_position="Potential material degradation and calibration challenges with variable ethanol blends",
        counter_arguments=[
            "Use of ethanol-resistant materials and coatings",
            "Real-time fuel composition sensing and adaptive control",
            "Extensive durability and emissions testing"
        ],
        resolution_strategy="Integrate robust materials and adaptive calibration to ensure seamless operation across fuel blends.",
        entity_scope="Flex-fuel vehicle fuel systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J2719 and EPA FFV certification standards"
    ),
    DoctrineBlock(
        topic="CNG and LPG Conversion Systems",
        keywords=["CNG", "LPG", "conversion", "fuel system", "pressure regulation", "safety"],
        conclusion_template="Conversion systems for CNG and LPG must ensure safe, reliable fuel delivery and integration with existing engine controls.",
        reasoning_framework=(
            "Compressed Natural Gas (CNG) and Liquefied Petroleum Gas (LPG) conversions require specialized fuel storage, pressure regulation, and delivery systems. "
            "The reasoning framework evaluates high-pressure storage tanks, regulators, injectors, and safety devices. "
            "Fuel pressure regulation is critical to maintain consistent delivery despite varying tank pressures. "
            "Integration with engine management systems involves modifying fuel maps and ignition timing for gaseous fuels. "
            "Safety considerations include leak detection, overpressure protection, and emergency shutoff valves. "
            "Material compatibility with gaseous fuels and resistance to embrittlement are assessed. "
            "The framework includes certification requirements per NFPA 52 and local regulations. "
            "Performance testing validates power output, emissions, and drivability post-conversion. "
            "Diagnostics monitor system integrity and detect faults such as leaks or regulator failures. "
            "Conversion kits must maintain vehicle warranty and comply with environmental standards."
        ),
        key_factors=[
            "High-pressure storage tank integrity",
            "Pressure regulator accuracy",
            "Fuel injector compatibility",
            "Safety device functionality",
            "Engine control system integration",
            "Material resistance to gaseous fuels",
            "Regulatory certification"
        ],
        primary_authority=[
            "NFPA 52 - Vehicular Gaseous Fuel Systems Code",
            "SAE J2716 - CNG Fuel System Components",
            "ISO 15500 - CNG Fuel Quality"
        ],
        burden_holder="Conversion system designers and installers",
        adversary_position="Safety risks and performance degradation from improper conversions",
        counter_arguments=[
            "Strict adherence to safety codes and standards",
            "Comprehensive testing and certification",
            "Use of OEM-approved components and calibration"
        ],
        resolution_strategy="Implement certified conversion kits with integrated safety and control systems.",
        entity_scope="CNG and LPG automotive fuel conversion systems",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="NFPA 52 and SAE J2716 standards"
    ),
    DoctrineBlock(
        topic="Fuel Trim Analysis and Diagnostics",
        keywords=["fuel trim", "diagnostics", "ECU", "oxygen sensor", "closed-loop control", "fuel delivery"],
        conclusion_template="Fuel trim analysis provides critical insights into fuel delivery accuracy and engine combustion efficiency.",
        reasoning_framework=(
            "Fuel trim refers to the adjustments made by the ECU to the base fuel injection pulse width to maintain stoichiometric air-fuel ratio. "
            "The reasoning framework involves interpreting short-term and long-term fuel trim values derived from oxygen sensor feedback. "
            "Deviations in fuel trim indicate potential issues such as vacuum leaks, injector faults, or sensor malfunctions. "
            "Diagnostic algorithms correlate fuel trim data with other sensor inputs to isolate root causes. "
            "The framework includes threshold definitions for acceptable fuel trim ranges and fault detection criteria. "
            "Fuel trim data supports adaptive learning in ECU calibration to compensate for component aging or environmental changes. "
            "Analysis tools visualize fuel trim trends over time to detect gradual degradations. "
            "Integration with OBD-II systems enables fault code generation and driver alerts. "
            "The framework also considers the impact of fuel quality and engine operating conditions on fuel trim behavior. "
            "Corrective actions include component replacement, calibration updates, and system cleaning."
        ),
        key_factors=[
            "Short-term and long-term fuel trim values",
            "Oxygen sensor accuracy",
            "Vacuum leak detection",
            "Injector performance",
            "ECU adaptive learning",
            "OBD-II fault codes",
            "Fuel quality impact"
        ],
        primary_authority=[
            "SAE J1979 - OBD-II Diagnostic Standards",
            "ISO 14229 - Unified Diagnostic Services",
            "Automotive Diagnostic Protocols"
        ],
        burden_holder="Service technicians and calibration engineers",
        adversary_position="Misinterpretation of fuel trim data leading to incorrect diagnostics",
        counter_arguments=[
            "Use of comprehensive diagnostic protocols and cross-sensor validation",
            "Training and calibration of diagnostic tools",
            "Integration of multiple data sources for accurate fault isolation"
        ],
        resolution_strategy="Employ systematic diagnostic procedures and continuous monitoring to maintain fuel system health.",
        entity_scope="Automotive fuel injection diagnostics",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and ISO 14229 diagnostic frameworks"
    ),
    DoctrineBlock(
        topic="Common Rail Diesel Injection Systems",
        keywords=["common rail", "diesel injection", "pressure control", "injector", "ECU", "emissions"],
        conclusion_template="Common rail diesel injection systems must maintain precise pressure and injection timing to optimize combustion and reduce emissions.",
        reasoning_framework=(
            "Common rail systems use a high-pressure accumulator rail supplying fuel to electronically controlled injectors. "
            "The reasoning framework analyzes pressure generation, regulation, and injector control to achieve multiple injection events per cycle. "
            "Precise control of injection timing, duration, and pressure is essential to reduce NOx and particulate emissions. "
            "The framework includes sensor feedback loops from rail pressure sensors and crankshaft position sensors. "
            "Injector nozzle design and spray pattern influence combustion efficiency and emissions. "
            "The ECU implements complex algorithms for pilot, main, and post-injections based on engine load and speed. "
            "Diagnostics monitor injector performance, rail pressure stability, and system leaks. "
            "Material durability under high pressure and temperature is critical. "
            "The system must comply with emissions regulations such as Euro 6 and EPA Tier 3. "
            "Failure modes include injector clogging, rail leaks, and pressure sensor faults."
        ),
        key_factors=[
            "Rail pressure stability",
            "Injector timing and control",
            "Spray pattern and nozzle design",
            "Sensor accuracy",
            "ECU injection algorithms",
            "Material durability",
            "Emissions compliance"
        ],
        primary_authority=[
            "SAE J1939 - Diesel Engine Controls",
            "ISO 22241 - Diesel Exhaust Fluid",
            "European Emissions Regulations"
        ],
        burden_holder="Diesel powertrain engineers",
        adversary_position="Injection system failures causing emissions exceedances and engine damage",
        counter_arguments=[
            "Robust sensor and actuator design",
            "Advanced ECU control strategies",
            "Regular maintenance and diagnostics"
        ],
        resolution_strategy="Integrate precise control and monitoring systems to maintain common rail injection performance.",
        entity_scope="Diesel common rail fuel injection systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J1939 and Euro 6 emissions standards"
    ),
    DoctrineBlock(
        topic="Injector Flow Testing and Cleaning",
        keywords=["injector", "flow testing", "cleaning", "performance", "clogging", "maintenance"],
        conclusion_template="Regular injector flow testing and cleaning are essential to maintain optimal fuel delivery and engine performance.",
        reasoning_framework=(
            "Fuel injectors can accumulate deposits that restrict flow and alter spray patterns, leading to poor combustion. "
            "The reasoning framework involves quantitative flow testing using precision flow benches to measure injector delivery rates and spray characteristics. "
            "Cleaning methods include ultrasonic cleaning, chemical cleaning, and on-vehicle cleaning additives. "
            "The framework evaluates before-and-after flow rates to assess cleaning effectiveness. "
            "Injector electrical diagnostics complement flow testing by assessing coil resistance and response time. "
            "Maintenance intervals are established based on fuel quality, operating conditions, and vehicle usage. "
            "The framework also considers the impact of injector wear and nozzle erosion on flow characteristics. "
            "Proper cleaning restores injector performance, reduces emissions, and improves fuel economy. "
            "Diagnostic data guides targeted maintenance and replacement decisions. "
            "Safety protocols ensure cleaning procedures do not damage injectors or pose hazards."
        ),
        key_factors=[
            "Injector flow rate measurements",
            "Deposit accumulation and removal",
            "Electrical coil diagnostics",
            "Cleaning method effectiveness",
            "Maintenance scheduling",
            "Injector wear and erosion",
            "Safety procedures"
        ],
        primary_authority=[
            "SAE J1939 - Injector Testing Procedures",
            "ASTM Fuel Injector Testing Standards",
            "Automotive Service Manuals"
        ],
        burden_holder="Service technicians and maintenance planners",
        adversary_position="Neglecting injector maintenance leading to performance loss and increased emissions",
        counter_arguments=[
            "Scheduled testing and cleaning protocols",
            "Use of quality fuel and additives",
            "Training and certification of service personnel"
        ],
        resolution_strategy="Implement routine injector diagnostics and cleaning to sustain fuel system performance.",
        entity_scope="Automotive fuel injectors",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J1939 injector testing and cleaning guidelines"
    ),
    DoctrineBlock(
        topic="Returnless Fuel System Design",
        keywords=["returnless fuel system", "fuel pressure", "pump", "regulator", "emissions", "efficiency"],
        conclusion_template="Returnless fuel systems improve efficiency and emissions by eliminating fuel return lines and maintaining stable pressure.",
        reasoning_framework=(
            "Traditional fuel systems use a return line to regulate pressure, causing fuel heating and vapor formation. "
            "Returnless systems regulate fuel pressure at the pump or tank, reducing fuel temperature and evaporative emissions. "
            "The reasoning framework analyzes pump design, pressure regulators, and fuel line routing to maintain target pressure without return flow. "
            "Benefits include reduced fuel vapor generation, improved fuel economy, and simplified fuel system architecture. "
            "The framework considers pump electrical load, pressure sensor integration, and ECU control strategies. "
            "Material compatibility and durability under altered pressure dynamics are evaluated. "
            "Diagnostics focus on pressure stability, pump performance, and leak detection. "
            "The system must comply with EVAP and emissions regulations. "
            "Thermal management strategies are integrated to mitigate vapor lock risks. "
            "The framework supports retrofit considerations and OEM design implementations."
        ),
        key_factors=[
            "Pump pressure regulation",
            "Fuel temperature management",
            "Pressure sensor accuracy",
            "ECU control algorithms",
            "Material durability",
            "Emissions compliance",
            "System architecture"
        ],
        primary_authority=[
            "SAE J2719 - Fuel System Design",
            "EPA EVAP Regulations",
            "Automotive Engineering Fuel System Design"
        ],
        burden_holder="Fuel system design engineers",
        adversary_position="Concerns about pressure stability and pump wear in returnless systems",
        counter_arguments=[
            "Advanced pump and sensor technologies ensure stable pressure",
            "Thermal management reduces vapor lock risks",
            "Simplified architecture reduces leak points"
        ],
        resolution_strategy="Design and validate returnless systems with integrated pressure and thermal controls.",
        entity_scope="Automotive fuel delivery systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J2719 and EPA EVAP standards"
    ),
    DoctrineBlock(
        topic="Fuel Pressure Diagnostics and Testing",
        keywords=["fuel pressure", "diagnostics", "testing", "sensor", "pump", "leak detection"],
        conclusion_template="Accurate fuel pressure diagnostics are essential to identify system faults and maintain engine performance.",
        reasoning_framework=(
            "Fuel pressure diagnostics involve measuring static and dynamic pressure at various points in the fuel system. "
            "The reasoning framework includes sensor calibration, data acquisition, and interpretation of pressure waveforms. "
            "Testing procedures encompass pressure decay tests, pump output verification, and leak detection protocols. "
            "Pressure sensor faults are diagnosed through signal validation and cross-referencing with other sensor data. "
            "The framework addresses transient pressure behaviors during engine start, acceleration, and steady-state operation. "
            "Fault codes related to pressure deviations are mapped to specific failure modes. "
            "Diagnostic tools enable real-time monitoring and data logging for trend analysis. "
            "The framework supports root cause analysis differentiating between pump, regulator, sensor, and line faults. "
            "Safety considerations include handling high-pressure fuel and preventing ignition sources during testing. "
            "Corrective actions are guided by diagnostic outcomes and component specifications."
        ),
        key_factors=[
            "Pressure sensor calibration",
            "Pump output verification",
            "Leak detection sensitivity",
            "Transient pressure analysis",
            "Fault code interpretation",
            "Diagnostic tool capabilities",
            "Safety protocols"
        ],
        primary_authority=[
            "SAE J1127 - Fuel System Testing",
            "ISO 20884 - Fuel Rail Testing",
            "Automotive Diagnostic Standards"
        ],
        burden_holder="Service technicians and diagnostic engineers",
        adversary_position="Misdiagnosis of pressure faults leading to unnecessary repairs",
        counter_arguments=[
            "Use of comprehensive diagnostic procedures",
            "Cross-validation with multiple sensors",
            "Training and certification of diagnostic personnel"
        ],
        resolution_strategy="Apply systematic testing and diagnostics to accurately identify fuel pressure issues.",
        entity_scope="Automotive fuel system diagnostics",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1127 and ISO 20884 testing standards"
    ),
    DoctrineBlock(
        topic="Fuel System Contamination and Filtration",
        keywords=["fuel contamination", "filtration", "particulates", "water", "microbial growth", "fuel system damage"],
        conclusion_template="Effective filtration and contamination control are critical to prevent fuel system damage and maintain engine reliability.",
        reasoning_framework=(
            "Fuel contamination by particulates, water, and microbial growth can cause injector clogging, pump wear, and corrosion. "
            "The reasoning framework evaluates filtration media design, placement, and efficiency in removing contaminants. "
            "Water separation techniques and microbial inhibitors are integrated to address common contamination sources. "
            "Fuel sampling and analysis identify contamination levels and types. "
            "The framework considers fuel system component susceptibility to contamination-induced damage. "
            "Maintenance schedules for filter replacement and system cleaning are based on contamination risk assessments. "
            "Diagnostics detect contamination effects through pressure drops, flow restrictions, and injector performance changes. "
            "Material compatibility with filtration additives and microbial inhibitors is assessed. "
            "The framework supports fuel handling and storage best practices to minimize contamination ingress. "
            "Regulatory requirements for fuel cleanliness and emissions impact are incorporated."
        ),
        key_factors=[
            "Filtration media efficiency",
            "Water separation capability",
            "Microbial growth control",
            "Fuel sampling and analysis",
            "Component susceptibility",
            "Maintenance scheduling",
            "Diagnostic indicators"
        ],
        primary_authority=[
            "SAE J1488 - Fuel Filtration Standards",
            "ASTM D975 - Diesel Fuel Quality",
            "EPA Fuel Quality Regulations"
        ],
        burden_holder="Fuel system maintenance and quality control teams",
        adversary_position="Contamination causing premature component failure and emissions issues",
        counter_arguments=[
            "Use of high-efficiency filters and water separators",
            "Regular fuel quality monitoring",
            "Preventive maintenance and cleaning"
        ],
        resolution_strategy="Implement comprehensive contamination control and filtration programs.",
        entity_scope="Automotive fuel systems",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J1488 and ASTM fuel quality standards"
    ),
    DoctrineBlock(
        topic="Cold Start Enrichment and Warm-Up Control",
        keywords=["cold start", "enrichment", "warm-up", "fuel delivery", "engine temperature", "emissions"],
        conclusion_template="Cold start enrichment strategies must balance drivability, emissions, and fuel economy during engine warm-up.",
        reasoning_framework=(
            "During cold start, engines require richer air-fuel mixtures to compensate for poor vaporization and combustion instability. "
            "The reasoning framework analyzes temperature sensor inputs, fuel delivery adjustments, and ignition timing modifications. "
            "Enrichment duration and magnitude are calibrated based on ambient temperature, engine coolant temperature, and intake air temperature. "
            "The framework includes strategies to minimize hydrocarbon and CO emissions during warm-up. "
            "Fuel vapor pressure and fuel volatility characteristics influence enrichment requirements. "
            "Closed-loop feedback from oxygen sensors is delayed during cold start, requiring open-loop control strategies. "
            "Warm-up control also manages idle speed and ignition timing to stabilize combustion. "
            "Diagnostics monitor enrichment system performance and detect sensor faults. "
            "The framework supports adaptive learning to optimize enrichment over vehicle life. "
            "Safety considerations include preventing excessive enrichment that can cause catalyst damage."
        ),
        key_factors=[
            "Engine and ambient temperature sensors",
            "Fuel delivery enrichment calibration",
            "Ignition timing adjustments",
            "Emission control during warm-up",
            "Fuel volatility",
            "Closed-loop control delay",
            "Diagnostic monitoring"
        ],
        primary_authority=[
            "SAE J1979 - OBD-II Emission Controls",
            "EPA Cold Start Emission Regulations",
            "Automotive Engine Calibration Manuals"
        ],
        burden_holder="Powertrain calibration engineers",
        adversary_position="Excessive enrichment causing increased emissions and fuel consumption",
        counter_arguments=[
            "Precise sensor calibration and control algorithms",
            "Adaptive learning to optimize enrichment",
            "Emission monitoring and diagnostics"
        ],
        resolution_strategy="Develop calibrated enrichment profiles with real-time monitoring to balance performance and emissions.",
        entity_scope="Automotive engine cold start systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and EPA cold start regulations"
    ),
    DoctrineBlock(
        topic="Fuel System OBDII Diagnostics and DTCs",
        keywords=["OBDII", "diagnostics", "DTC", "fuel system", "fault codes", "monitoring"],
        conclusion_template="OBDII diagnostics and DTCs provide standardized fault detection and reporting for fuel system malfunctions.",
        reasoning_framework=(
            "On-Board Diagnostics II (OBDII) systems monitor fuel system parameters to detect faults affecting emissions and performance. "
            "The reasoning framework covers sensor monitoring, fault detection algorithms, and diagnostic trouble code (DTC) generation. "
            "Fuel system monitors include fuel pressure, injector performance, fuel trim, and vapor leak detection. "
            "The framework defines fault thresholds, fault confirmation criteria, and readiness monitors. "
            "DTCs provide standardized codes for technicians to identify and address fuel system issues. "
            "The system supports freeze frame data capture and diagnostic data logging. "
            "Integration with scan tools enables real-time data access and fault clearing. "
            "The framework includes strategies for false positive reduction and fault prioritization. "
            "Regulatory compliance mandates OBDII capabilities in light-duty vehicles. "
            "The framework supports continuous improvement through software updates and calibration refinements."
        ),
        key_factors=[
            "Sensor monitoring and validation",
            "Fault detection algorithms",
            "DTC definitions and thresholds",
            "Readiness monitor implementation",
            "Diagnostic data capture",
            "Scan tool integration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SAE J1979 - OBD-II Diagnostic Standards",
            "EPA OBD Regulations",
            "ISO 14229 - Unified Diagnostic Services"
        ],
        burden_holder="Vehicle manufacturers and calibration engineers",
        adversary_position="Complexity of diagnostics leading to misinterpretation and repair delays",
        counter_arguments=[
            "Standardized DTC codes and diagnostic procedures",
            "Training for service personnel",
            "Advanced diagnostic tools and software"
        ],
        resolution_strategy="Implement robust OBDII diagnostic systems with clear fault reporting and support tools.",
        entity_scope="Automotive fuel system diagnostics",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and EPA OBDII regulations"
    ),
    DoctrineBlock(
        topic="Performance Fuel System Modifications",
        keywords=["performance", "fuel system", "modifications", "injectors", "pumps", "tuning"],
        conclusion_template="Performance modifications to fuel systems require comprehensive tuning and component upgrades to ensure reliability and emissions compliance.",
        reasoning_framework=(
            "Upgrading fuel system components such as injectors, pumps, and rails is common in performance applications to support increased power output. "
            "The reasoning framework involves selecting components with appropriate flow rates and pressure ratings. "
            "Tuning ECU fuel maps to accommodate modified hardware ensures correct air-fuel ratios and ignition timing. "
            "The framework evaluates the impact of modifications on emissions and drivability. "
            "Fuel system reliability under increased loads and thermal stresses is assessed. "
            "Diagnostics are adapted to recognize modified component parameters and prevent false fault detection. "
            "The framework includes validation testing under various operating conditions. "
            "Safety considerations address fuel system integrity and fire prevention. "
            "Legal and warranty implications of modifications are analyzed. "
            "Integration with other performance systems such as forced induction is considered."
        ),
        key_factors=[
            "Component flow rate and pressure",
            "ECU calibration and tuning",
            "Emissions impact",
            "System reliability",
            "Diagnostic adaptation",
            "Safety and fire prevention",
            "Legal and warranty considerations"
        ],
        primary_authority=[
            "SAE J2729 - Performance Fuel Systems",
            "EPA Emissions Modification Guidelines",
            "Aftermarket Performance Engineering Manuals"
        ],
        burden_holder="Performance tuners and engineers",
        adversary_position="Risk of engine damage and emissions violations from improper modifications",
        counter_arguments=[
            "Comprehensive tuning and testing protocols",
            "Use of certified performance components",
            "Compliance with emissions regulations"
        ],
        resolution_strategy="Implement integrated modification and tuning strategies with thorough validation.",
        entity_scope="Automotive performance fuel systems",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J2729 and EPA modification guidelines"
    ),
    DoctrineBlock(
        topic="Fuel System Safety and Fire Prevention",
        keywords=["fuel system", "safety", "fire prevention", "leak detection", "material flammability", "crashworthiness"],
        conclusion_template="Fuel system safety design must minimize fire risks through leak prevention, material selection, and crashworthiness features.",
        reasoning_framework=(
            "Fuel systems pose inherent fire risks due to flammable liquids and vapors under pressure. "
            "The reasoning framework addresses leak prevention through robust sealing, hose and fitting design, and pressure regulation. "
            "Material selection prioritizes low flammability, chemical resistance, and durability. "
            "Crashworthiness features include breakaway fittings, rollover valves, and fuel shutoff devices. "
            "Leak detection systems integrate sensors and diagnostics to alert occupants and disable fuel pumps if needed. "
            "Thermal insulation and shielding protect fuel system components from engine and exhaust heat. "
            "The framework incorporates regulatory safety standards such as FMVSS 301 and ISO 26262 functional safety. "
            "Fire prevention strategies include proper routing, ventilation, and grounding to prevent static discharge. "
            "Maintenance and inspection protocols ensure ongoing system integrity. "
            "Emergency response procedures are established for fuel system incidents."
        ),
        key_factors=[
            "Leak prevention and sealing",
            "Material flammability and resistance",
            "Crashworthiness and safety devices",
            "Leak detection and diagnostics",
            "Thermal protection",
            "Regulatory safety standards",
            "Maintenance and emergency procedures"
        ],
        primary_authority=[
            "FMVSS 301 - Fuel System Integrity",
            "ISO 26262 - Functional Safety",
            "NFPA 30 - Flammable Liquids Code"
        ],
        burden_holder="Fuel system designers and safety engineers",
        adversary_position="Potential for catastrophic fires due to fuel leaks or failures",
        counter_arguments=[
            "Redundant safety features and diagnostics",
            "Use of fire-resistant materials",
            "Compliance with rigorous safety standards"
        ],
        resolution_strategy="Design fuel systems with multiple safety layers and continuous monitoring.",
        entity_scope="Automotive fuel system safety",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FMVSS 301 and ISO 26262 safety standards"
    ),
    DoctrineBlock(
        topic="Diesel Fuel Quality and Cold Weather Operation",
        keywords=["diesel fuel", "quality", "cold weather", "gelling", "additives", "fuel system"],
        conclusion_template="Maintaining diesel fuel quality and preventing gelling are essential for reliable cold weather engine operation.",
        reasoning_framework=(
            "Diesel fuel can gel or wax at low temperatures, causing filter clogging and fuel starvation. "
            "The reasoning framework evaluates fuel cold flow properties, additive effectiveness, and fuel system design adaptations. "
            "Fuel quality standards specify cold filter plugging point (CFPP) and pour point requirements. "
            "Additives such as anti-gel agents improve low-temperature operability. "
            "Fuel heating systems including tank heaters and fuel line heaters are integrated to maintain flow. "
            "Diagnostics monitor fuel filter pressure differentials to detect gelling. "
            "Material compatibility with additives and cold temperatures is assessed. "
            "Storage and handling practices minimize water contamination and microbial growth. "
            "The framework includes regional fuel formulation adjustments for winter conditions. "
            "Engine calibration adapts to cold start challenges associated with diesel fuel properties."
        ),
        key_factors=[
            "Fuel cold flow properties",
            "Additive effectiveness",
            "Fuel heating system design",
            "Filter clogging diagnostics",
            "Material compatibility",
            "Storage and handling",
            "Regional fuel formulations"
        ],
        primary_authority=[
            "ASTM D975 - Diesel Fuel Specifications",
            "SAE J1941 - Diesel Fuel Additives",
            "EPA Cold Weather Fuel Guidelines"
        ],
        burden_holder="Fuel suppliers and vehicle operators",
        adversary_position="Cold weather fuel issues causing engine start failures and damage",
        counter_arguments=[
            "Use of certified winter diesel fuels and additives",
            "Integration of fuel heating systems",
            "Regular maintenance and monitoring"
        ],
        resolution_strategy="Implement comprehensive cold weather fuel management and system adaptations.",
        entity_scope="Diesel fuel systems in cold climates",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="ASTM D975 and SAE J1941 standards"
    ),
    DoctrineBlock(
        topic="Fuel System Corrosion and Material Compatibility",
        keywords=["fuel system", "corrosion", "material compatibility", "fuel additives", "ethanol", "degradation"],
        conclusion_template="Selecting corrosion-resistant materials and ensuring compatibility with fuel additives are vital for fuel system longevity.",
        reasoning_framework=(
            "Fuel system components are exposed to various chemical agents including ethanol, biodiesel, and additives that can induce corrosion. "
            "The reasoning framework assesses material properties such as corrosion resistance, swelling, and degradation under fuel exposure. "
            "Compatibility testing includes immersion tests, mechanical property evaluation, and accelerated aging. "
            "The framework considers galvanic corrosion risks in mixed-metal assemblies. "
            "Fuel additive interactions with materials are analyzed to prevent adverse effects. "
            "Protective coatings and sealants are evaluated for effectiveness and durability. "
            "Diagnostics monitor for symptoms of corrosion such as leaks, pressure drops, and sensor faults. "
            "Material selection guidelines are aligned with fuel composition and expected operating conditions. "
            "Maintenance and inspection protocols detect early signs of corrosion. "
            "The framework supports design revisions and supplier quality control."
        ),
        key_factors=[
            "Material corrosion resistance",
            "Additive compatibility",
            "Galvanic corrosion risk",
            "Protective coatings",
            "Diagnostic indicators",
            "Operating environment",
            "Maintenance protocols"
        ],
        primary_authority=[
            "ASTM D7577 - Fuel System Materials Testing",
            "SAE J2719 - Fuel System Materials",
            "ISO 22241 - Diesel Exhaust Fluid Compatibility"
        ],
        burden_holder="Fuel system design and materials engineers",
        adversary_position="Material degradation leading to leaks and system failures",
        counter_arguments=[
            "Use of tested and certified materials",
            "Protective coatings and design best practices",
            "Regular inspection and maintenance"
        ],
        resolution_strategy="Implement rigorous material selection and testing programs for fuel system compatibility.",
        entity_scope="Automotive fuel system materials",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D7577 and SAE J2719 standards"
    ),
    DoctrineBlock(
        topic="Fuel Injector Electrical Diagnostics and Waveform Analysis",
        keywords=["fuel injector", "electrical diagnostics", "waveform analysis", "coil resistance", "injector driver"],
        conclusion_template="Electrical diagnostics and waveform analysis are essential tools for assessing fuel injector health and performance.",
        reasoning_framework=(
            "Fuel injectors are electromechanical devices controlled by ECU driver circuits. "
            "The reasoning framework involves measuring coil resistance, inductance, and analyzing injector drive waveforms. "
            "Waveform analysis includes examining voltage spikes, current ramps, and injector opening/closing times. "
            "Abnormal waveforms indicate faults such as coil shorts, opens, or driver circuit issues. "
            "Diagnostic tools capture and interpret waveforms in real time during engine operation. "
            "The framework integrates electrical measurements with fuel delivery performance data for comprehensive assessment. "
            "Calibration of diagnostic thresholds accounts for injector type and engine conditions. "
            "Safety precautions prevent damage to ECU and diagnostic equipment. "
            "Training for technicians ensures accurate interpretation of complex waveforms. "
            "The framework supports predictive maintenance and fault isolation."
        ),
        key_factors=[
            "Coil resistance and inductance",
            "Injector drive waveform characteristics",
            "Voltage and current analysis",
            "Diagnostic tool capabilities",
            "Integration with fuel delivery data",
            "Calibration of thresholds",
            "Technician training"
        ],
        primary_authority=[
            "SAE J1939 - Injector Diagnostics",
            "Automotive Service Excellence (ASE) Standards",
            "OEM Technical Service Bulletins"
        ],
        burden_holder="Service technicians and diagnostic engineers",
        adversary_position="Complexity of waveform interpretation leading to misdiagnosis",
        counter_arguments=[
            "Standardized diagnostic procedures",
            "Advanced diagnostic tools with automated analysis",
            "Comprehensive training programs"
        ],
        resolution_strategy="Utilize waveform analysis combined with electrical testing for accurate injector diagnostics.",
        entity_scope="Automotive fuel injector diagnostics",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1939 and ASE diagnostic standards"
    ),
    DoctrineBlock(
        topic="Injector Flow Testing and Cleaning",
        keywords=["injector", "flow testing", "cleaning", "performance", "clogging", "maintenance"],
        conclusion_template="Regular injector flow testing and cleaning are essential to maintain optimal fuel delivery and engine performance.",
        reasoning_framework=(
            "Fuel injectors can accumulate deposits that restrict flow and alter spray patterns, leading to poor combustion. "
            "The reasoning framework involves quantitative flow testing using precision flow benches to measure injector delivery rates and spray characteristics. "
            "Cleaning methods include ultrasonic cleaning, chemical cleaning, and on-vehicle cleaning additives. "
            "The framework evaluates before-and-after flow rates to assess cleaning effectiveness. "
            "Injector electrical diagnostics complement flow testing by assessing coil resistance and response time. "
            "Maintenance intervals are established based on fuel quality, operating conditions, and vehicle usage. "
            "The framework also considers the impact of injector wear and nozzle erosion on flow characteristics. "
            "Proper cleaning restores injector performance, reduces emissions, and improves fuel economy. "
            "Diagnostic data guides targeted maintenance and replacement decisions. "
            "Safety protocols ensure cleaning procedures do not damage injectors or pose hazards."
        ),
        key_factors=[
            "Injector flow rate measurements",
            "Deposit accumulation and removal",
            "Electrical coil diagnostics",
            "Cleaning method effectiveness",
            "Maintenance scheduling",
            "Injector wear and erosion",
            "Safety procedures"
        ],
        primary_authority=[
            "SAE J1939 - Injector Testing Procedures",
            "ASTM Fuel Injector Testing Standards",
            "Automotive Service Manuals"
        ],
        burden_holder="Service technicians and maintenance planners",
        adversary_position="Neglecting injector maintenance leading to performance loss and increased emissions",
        counter_arguments=[
            "Scheduled testing and cleaning protocols",
            "Use of quality fuel and additives",
            "Training and certification of service personnel"
        ],
        resolution_strategy="Implement routine injector diagnostics and cleaning to sustain fuel system performance.",
        entity_scope="Automotive fuel injectors",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J1939 injector testing and cleaning guidelines"
    ),
    DoctrineBlock(
        topic="Returnless Fuel System Design",
        keywords=["returnless fuel system", "fuel pressure", "pump", "regulator", "emissions", "efficiency"],
        conclusion_template="Returnless fuel systems improve efficiency and emissions by eliminating fuel return lines and maintaining stable pressure.",
        reasoning_framework=(
            "Traditional fuel systems use a return line to regulate pressure, causing fuel heating and vapor formation. "
            "Returnless systems regulate fuel pressure at the pump or tank, reducing fuel temperature and evaporative emissions. "
            "The reasoning framework analyzes pump design, pressure regulators, and fuel line routing to maintain target pressure without return flow. "
            "Benefits include reduced fuel vapor generation, improved fuel economy, and simplified fuel system architecture. "
            "The framework considers pump electrical load, pressure sensor integration, and ECU control strategies. "
            "Material compatibility and durability under altered pressure dynamics are evaluated. "
            "Diagnostics focus on pressure stability, pump performance, and leak detection. "
            "The system must comply with EVAP and emissions regulations. "
            "Thermal management strategies are integrated to mitigate vapor lock risks. "
            "The framework supports retrofit considerations and OEM design implementations."
        ),
        key_factors=[
            "Pump pressure regulation",
            "Fuel temperature management",
            "Pressure sensor accuracy",
            "ECU control algorithms",
            "Material durability",
            "Emissions compliance",
            "System architecture"
        ],
        primary_authority=[
            "SAE J2719 - Fuel System Design",
            "EPA EVAP Regulations",
            "Automotive Engineering Fuel System Design"
        ],
        burden_holder="Fuel system design engineers",
        adversary_position="Concerns about pressure stability and pump wear in returnless systems",
        counter_arguments=[
            "Advanced pump and sensor technologies ensure stable pressure",
            "Thermal management reduces vapor lock risks",
            "Simplified architecture reduces leak points"
        ],
        resolution_strategy="Design and validate returnless systems with integrated pressure and thermal controls.",
        entity_scope="Automotive fuel delivery systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J2719 and EPA EVAP standards"
    ),
    DoctrineBlock(
        topic="Fuel Pressure Diagnostics and Testing",
        keywords=["fuel pressure", "diagnostics", "testing", "sensor", "pump", "leak detection"],
        conclusion_template="Accurate fuel pressure diagnostics are essential to identify system faults and maintain engine performance.",
        reasoning_framework=(
            "Fuel pressure diagnostics involve measuring static and dynamic pressure at various points in the fuel system. "
            "The reasoning framework includes sensor calibration, data acquisition, and interpretation of pressure waveforms. "
            "Testing procedures encompass pressure decay tests, pump output verification, and leak detection protocols. "
            "Pressure sensor faults are diagnosed through signal validation and cross-referencing with other sensor data. "
            "The framework addresses transient pressure behaviors during engine start, acceleration, and steady-state operation. "
            "Fault codes related to pressure deviations are mapped to specific failure modes. "
            "Diagnostic tools enable real-time monitoring and data logging for trend analysis. "
            "The framework supports root cause analysis differentiating between pump, regulator, sensor, and line faults. "
            "Safety considerations include handling high-pressure fuel and preventing ignition sources during testing. "
            "Corrective actions are guided by diagnostic outcomes and component specifications."
        ),
        key_factors=[
            "Pressure sensor calibration",
            "Pump output verification",
            "Leak detection sensitivity",
            "Transient pressure analysis",
            "Fault code interpretation",
            "Diagnostic tool capabilities",
            "Safety protocols"
        ],
        primary_authority=[
            "SAE J1127 - Fuel System Testing",
            "ISO 20884 - Fuel Rail Testing",
            "Automotive Diagnostic Standards"
        ],
        burden_holder="Service technicians and diagnostic engineers",
        adversary_position="Misdiagnosis of pressure faults leading to unnecessary repairs",
        counter_arguments=[
            "Use of comprehensive diagnostic procedures",
            "Cross-validation with multiple sensors",
            "Training and certification of diagnostic personnel"
        ],
        resolution_strategy="Apply systematic testing and diagnostics to accurately identify fuel pressure issues.",
        entity_scope="Automotive fuel system diagnostics",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1127 and ISO 20884 testing standards"
    ),
    DoctrineBlock(
        topic="Fuel System Contamination and Filtration",
        keywords=["fuel contamination", "filtration", "particulates", "water", "microbial growth", "fuel system damage"],
        conclusion_template="Effective filtration and contamination control are critical to prevent fuel system damage and maintain engine reliability.",
        reasoning_framework=(
            "Fuel contamination by particulates, water, and microbial growth can cause injector clogging, pump wear, and corrosion. "
            "The reasoning framework evaluates filtration media design, placement, and efficiency in removing contaminants. "
            "Water separation techniques and microbial inhibitors are integrated to address common contamination sources. "
            "Fuel sampling and analysis identify contamination levels and types. "
            "The framework considers fuel system component susceptibility to contamination-induced damage. "
            "Maintenance schedules for filter replacement and system cleaning are based on contamination risk assessments. "
            "Diagnostics detect contamination effects through pressure drops, flow restrictions, and injector performance changes. "
            "Material compatibility with filtration additives and microbial inhibitors is assessed. "
            "The framework supports fuel handling and storage best practices to minimize contamination ingress. "
            "Regulatory requirements for fuel cleanliness and emissions impact are incorporated."
        ),
        key_factors=[
            "Filtration media efficiency",
            "Water separation capability",
            "Microbial growth control",
            "Fuel sampling and analysis",
            "Component susceptibility",
            "Maintenance scheduling",
            "Diagnostic indicators"
        ],
        primary_authority=[
            "SAE J1488 - Fuel Filtration Standards",
            "ASTM D975 - Diesel Fuel Quality",
            "EPA Fuel Quality Regulations"
        ],
        burden_holder="Fuel system maintenance and quality control teams",
        adversary_position="Contamination causing premature component failure and emissions issues",
        counter_arguments=[
            "Use of high-efficiency filters and water separators",
            "Regular fuel quality monitoring",
            "Preventive maintenance and cleaning"
        ],
        resolution_strategy="Implement comprehensive contamination control and filtration programs.",
        entity_scope="Automotive fuel systems",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J1488 and ASTM fuel quality standards"
    ),
    DoctrineBlock(
        topic="Cold Start Enrichment and Warm-Up Control",
        keywords=["cold start", "enrichment", "warm-up", "fuel delivery", "engine temperature", "emissions"],
        conclusion_template="Cold start enrichment strategies must balance drivability, emissions, and fuel economy during engine warm-up.",
        reasoning_framework=(
            "During cold start, engines require richer air-fuel mixtures to compensate for poor vaporization and combustion instability. "
            "The reasoning framework analyzes temperature sensor inputs, fuel delivery adjustments, and ignition timing modifications. "
            "Enrichment duration and magnitude are calibrated based on ambient temperature, engine coolant temperature, and intake air temperature. "
            "The framework includes strategies to minimize hydrocarbon and CO emissions during warm-up. "
            "Fuel vapor pressure and fuel volatility characteristics influence enrichment requirements. "
            "Closed-loop feedback from oxygen sensors is delayed during cold start, requiring open-loop control strategies. "
            "Warm-up control also manages idle speed and ignition timing to stabilize combustion. "
            "Diagnostics monitor enrichment system performance and detect sensor faults. "
            "The framework supports adaptive learning to optimize enrichment over vehicle life. "
            "Safety considerations include preventing excessive enrichment that can cause catalyst damage."
        ),
        key_factors=[
            "Engine and ambient temperature sensors",
            "Fuel delivery enrichment calibration",
            "Ignition timing adjustments",
            "Emission control during warm-up",
            "Fuel volatility",
            "Closed-loop control delay",
            "Diagnostic monitoring"
        ],
        primary_authority=[
            "SAE J1979 - OBD-II Emission Controls",
            "EPA Cold Start Emission Regulations",
            "Automotive Engine Calibration Manuals"
        ],
        burden_holder="Powertrain calibration engineers",
        adversary_position="Excessive enrichment causing increased emissions and fuel consumption",
        counter_arguments=[
            "Precise sensor calibration and control algorithms",
            "Adaptive learning to optimize enrichment",
            "Emission monitoring and diagnostics"
        ],
        resolution_strategy="Develop calibrated enrichment profiles with real-time monitoring to balance performance and emissions.",
        entity_scope="Automotive engine cold start systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and EPA cold start regulations"
    ),
    DoctrineBlock(
        topic="Fuel System OBDII Diagnostics and DTCs",
        keywords=["OBDII", "diagnostics", "DTC", "fuel system", "fault codes", "monitoring"],
        conclusion_template="OBDII diagnostics and DTCs provide standardized fault detection and reporting for fuel system malfunctions.",
        reasoning_framework=(
            "On-Board Diagnostics II (OBDII) systems monitor fuel system parameters to detect faults affecting emissions and performance. "
            "The reasoning framework covers sensor monitoring, fault detection algorithms, and diagnostic trouble code (DTC) generation. "
            "Fuel system monitors include fuel pressure, injector performance, fuel trim, and vapor leak detection. "
            "The framework defines fault thresholds, fault confirmation criteria, and readiness monitors. "
            "DTCs provide standardized codes for technicians to identify and address fuel system issues. "
            "The system supports freeze frame data capture and diagnostic data logging. "
            "Integration with scan tools enables real-time data access and fault clearing. "
            "The framework includes strategies for false positive reduction and fault prioritization. "
            "Regulatory compliance mandates OBDII capabilities in light-duty vehicles. "
            "The framework supports continuous improvement through software updates and calibration refinements."
        ),
        key_factors=[
            "Sensor monitoring and validation",
            "Fault detection algorithms",
            "DTC definitions and thresholds",
            "Readiness monitor implementation",
            "Diagnostic data capture",
            "Scan tool integration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SAE J1979 - OBD-II Diagnostic Standards",
            "EPA OBD Regulations",
            "ISO 14229 - Unified Diagnostic Services"
        ],
        burden_holder="Vehicle manufacturers and calibration engineers",
        adversary_position="Complexity of diagnostics leading to misinterpretation and repair delays",
        counter_arguments=[
            "Standardized DTC codes and diagnostic procedures",
            "Training for service personnel",
            "Advanced diagnostic tools and software"
        ],
        resolution_strategy="Implement robust OBDII diagnostic systems with clear fault reporting and support tools.",
        entity_scope="Automotive fuel system diagnostics",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and EPA OBDII regulations"
    ),
    DoctrineBlock(
        topic="Performance Fuel System Modifications",
        keywords=["performance", "fuel system", "modifications", "injectors", "pumps", "tuning"],
        conclusion_template="Performance modifications to fuel systems require comprehensive tuning and component upgrades to ensure reliability and emissions compliance.",
        reasoning_framework=(
            "Upgrading fuel system components such as injectors, pumps, and rails is common in performance applications to support increased power output. "
            "The reasoning framework involves selecting components with appropriate flow rates and pressure ratings. "
            "Tuning ECU fuel maps to accommodate modified hardware ensures correct air-fuel ratios and ignition timing. "
            "The framework evaluates the impact of modifications on emissions and drivability. "
            "Fuel system reliability under increased loads and thermal stresses is assessed. "
            "Diagnostics are adapted to recognize modified component parameters and prevent false fault detection. "
            "The framework includes validation testing under various operating conditions. "
            "Safety considerations address fuel system integrity and fire prevention. "
            "Legal and warranty implications of modifications are analyzed. "
            "Integration with other performance systems such as forced induction is considered."
        ),
        key_factors=[
            "Component flow rate and pressure",
            "ECU calibration and tuning",
            "Emissions impact",
            "System reliability",
            "Diagnostic adaptation",
            "Safety and fire prevention",
            "Legal and warranty considerations"
        ],
        primary_authority=[
            "SAE J2729 - Performance Fuel Systems",
            "EPA Emissions Modification Guidelines",
            "Aftermarket Performance Engineering Manuals"
        ],
        burden_holder="Performance tuners and engineers",
        adversary_position="Risk of engine damage and emissions violations from improper modifications",
        counter_arguments=[
            "Comprehensive tuning and testing protocols",
            "Use of certified performance components",
            "Compliance with emissions regulations"
        ],
        resolution_strategy="Implement integrated modification and tuning strategies with thorough validation.",
        entity_scope="Automotive performance fuel systems",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE J2729 and EPA modification guidelines"
    ),
    DoctrineBlock(
        topic="Fuel System Safety and Fire Prevention",
        keywords=["fuel system", "safety", "fire prevention", "leak detection", "material flammability", "crashworthiness"],
        conclusion_template="Fuel system safety design must minimize fire risks through leak prevention, material selection, and crashworthiness features.",
        reasoning_framework=(
            "Fuel systems pose inherent fire risks due to flammable liquids and vapors under pressure. "
            "The reasoning framework addresses leak prevention through robust sealing, hose and fitting design, and pressure regulation. "
            "Material selection prioritizes low flammability, chemical resistance, and durability. "
            "Crashworthiness features include breakaway fittings, rollover valves, and fuel shutoff devices. "
            "Leak detection systems integrate sensors and diagnostics to alert occupants and disable fuel pumps if needed. "
            "Thermal insulation and shielding protect fuel system components from engine and exhaust heat. "
            "The framework incorporates regulatory safety standards such as FMVSS 301 and ISO 26262 functional safety. "
            "Fire prevention strategies include proper routing, ventilation, and grounding to prevent static discharge. "
            "Maintenance and inspection protocols ensure ongoing system integrity. "
            "Emergency response procedures are established for fuel system incidents."
        ),
        key_factors=[
            "Leak prevention and sealing",
            "Material flammability and resistance",
            "Crashworthiness and safety devices",
            "Leak detection and diagnostics",
            "Thermal protection",
            "Regulatory safety standards",
            "Maintenance and emergency procedures"
        ],
        primary_authority=[
            "FMVSS 301 - Fuel System Integrity",
            "ISO 26262 - Functional Safety",
            "NFPA 30 - Flammable Liquids Code"
        ],
        burden_holder="Fuel system designers and safety engineers",
        adversary_position="Potential for catastrophic fires due to fuel leaks or failures",
        counter_arguments=[
            "Redundant safety features and diagnostics",
            "Use of fire-resistant materials",
            "Compliance with rigorous safety standards"
        ],
        resolution_strategy="Design fuel systems with multiple safety layers and continuous monitoring.",
        entity_scope="Automotive fuel system safety",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FMVSS 301 and ISO 26262 safety standards"
    ),
    DoctrineBlock(
        topic="Diesel Fuel Quality and Cold Weather Operation",
        keywords=["diesel fuel", "quality", "cold weather", "gelling", "additives", "fuel system"],
        conclusion_template="Maintaining diesel fuel quality and preventing gelling are essential for reliable cold weather engine operation.",
        reasoning_framework=(
            "Diesel fuel can gel or wax at low temperatures, causing filter clogging and fuel starvation. "
            "The reasoning framework evaluates fuel cold flow properties, additive effectiveness, and fuel system design adaptations. "
            "Fuel quality standards specify cold filter plugging point (CFPP) and pour point requirements. "
            "Additives such as anti-gel agents improve low-temperature operability. "
            "Fuel heating systems including tank heaters and fuel line heaters are integrated to maintain flow. "
            "Diagnostics monitor fuel filter pressure differentials to detect gelling. "
            "Material compatibility with additives and cold temperatures is assessed. "
            "Storage and handling practices minimize water contamination and microbial growth. "
            "The framework includes regional fuel formulation adjustments for winter conditions. "
            "Engine calibration adapts to cold start challenges associated with diesel fuel properties."
        ),
        key_factors=[
            "Fuel cold flow properties",
            "Additive effectiveness",
            "Fuel heating system design",
            "Filter clogging diagnostics",
            "Material compatibility",
            "Storage and handling",
            "Regional fuel formulations"
        ],
        primary_authority=[
            "ASTM D975 - Diesel Fuel Specifications",
            "SAE J1941 - Diesel Fuel Additives",
            "EPA Cold Weather Fuel Guidelines"
        ],
        burden_holder="Fuel suppliers and vehicle operators",
        adversary_position="Cold weather fuel issues causing engine start failures and damage",
        counter_arguments=[
            "Use of certified winter diesel fuels and additives",
            "Integration of fuel heating systems",
            "Regular maintenance and monitoring"
        ],
        resolution_strategy="Implement comprehensive cold weather fuel management and system adaptations.",
        entity_scope="Diesel fuel systems in cold climates",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="ASTM D975 and SAE J1941 standards"
    ),
    DoctrineBlock(
        topic="Fuel System Corrosion and Material Compatibility",
        keywords=["fuel system", "corrosion", "material compatibility", "fuel additives", "ethanol", "degradation"],
        conclusion_template="Selecting corrosion-resistant materials and ensuring compatibility with fuel additives are vital for fuel system longevity.",
        reasoning_framework=(
            "Fuel system components are exposed to various chemical agents including ethanol, biodiesel, and additives that can induce corrosion. "
            "The reasoning framework assesses material properties such as corrosion resistance, swelling, and degradation under fuel exposure. "
            "Compatibility testing includes immersion tests, mechanical property evaluation, and accelerated aging. "
            "The framework considers galvanic corrosion risks in mixed-metal assemblies. "
            "Fuel additive interactions with materials are analyzed to prevent adverse effects. "
            "Protective coatings and sealants are evaluated for effectiveness and durability. "
            "Diagnostics monitor for symptoms of corrosion such as leaks, pressure drops, and sensor faults. "
            "Material selection guidelines are aligned with fuel composition and expected operating conditions. "
            "Maintenance and inspection protocols detect early signs of corrosion. "
            "The framework supports design revisions and supplier quality control."
        ),
        key_factors=[
            "Material corrosion resistance",
            "Additive compatibility",
            "Galvanic corrosion risk",
            "Protective coatings",
            "Diagnostic indicators",
            "Operating environment",
            "Maintenance protocols"
        ],
        primary_authority=[
            "ASTM D7577 - Fuel System Materials Testing",
            "SAE J2719 - Fuel System Materials",
            "ISO 22241 - Diesel Exhaust Fluid Compatibility"
        ],
        burden_holder="Fuel system design and materials engineers",
        adversary_position="Material degradation leading to leaks and system failures",
        counter_arguments=[
            "Use of tested and certified materials",
            "Protective coatings and design best practices",
            "Regular inspection and maintenance"
        ],
        resolution_strategy="Implement rigorous material selection and testing programs for fuel system compatibility.",
        entity_scope="Automotive fuel system materials",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM D7577 and SAE J2719 standards"
    ),
    DoctrineBlock(
        topic="Fuel Injector Electrical Diagnostics and Waveform Analysis",
        keywords=["fuel injector", "electrical diagnostics", "waveform analysis", "coil resistance", "injector driver"],
        conclusion_template="Electrical diagnostics and waveform analysis are essential tools for assessing fuel injector health and performance.",
        reasoning_framework=(
            "Fuel injectors are electromechanical devices controlled by ECU driver circuits. "
            "The reasoning framework involves measuring coil resistance, inductance, and analyzing injector drive waveforms. "
            "Waveform analysis includes examining voltage spikes, current ramps, and injector opening/closing times. "
            "Abnormal waveforms indicate faults such as coil shorts, opens, or driver circuit issues. "
            "Diagnostic tools capture and interpret waveforms in real time during engine operation. "
            "The framework integrates electrical measurements with fuel delivery performance data for comprehensive assessment. "
            "Calibration of diagnostic thresholds accounts for injector type and engine conditions. "
            "Safety precautions prevent damage to ECU and diagnostic equipment. "
            "Training for technicians ensures accurate interpretation of complex waveforms. "
            "The framework supports predictive maintenance and fault isolation."
        ),
        key_factors=[
            "Coil resistance and inductance",
            "Injector drive waveform characteristics",
            "Voltage and current analysis",
            "Diagnostic tool capabilities",
            "Integration with fuel delivery data",
            "Calibration of thresholds",
            "Technician training"
        ],
        primary_authority=[
            "SAE J1939 - Injector Diagnostics",
            "Automotive Service Excellence (ASE) Standards",
            "OEM Technical Service Bulletins"
        ],
        burden_holder="Service technicians and diagnostic engineers",
        adversary_position="Complexity of waveform interpretation leading to misdiagnosis",
        counter_arguments=[
            "Standardized diagnostic procedures",
            "Advanced diagnostic tools with automated analysis",
            "Comprehensive training programs"
        ],
        resolution_strategy="Utilize waveform analysis combined with electrical testing for accurate injector diagnostics.",
        entity_scope="Automotive fuel injector diagnostics",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1939 and ASE diagnostic standards"
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in kw.lower() for kw in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]