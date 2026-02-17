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
        topic="OBD-II P0xxx Powertrain Codes",
        keywords=["OBD-II", "P0xxx", "powertrain", "diagnostics", "DTC", "trouble codes"],
        conclusion_template="When a P0xxx code is present, the engine control module (ECM) has detected a malfunction in the powertrain system that requires targeted diagnostics and repair.",
        reasoning_framework=(
            "The OBD-II standard defines a set of diagnostic trouble codes (DTCs) that indicate specific malfunctions in the vehicle's powertrain. "
            "Codes starting with 'P0' are generic powertrain codes recognized across manufacturers. The ECM continuously monitors sensors and actuators "
            "and sets these codes when parameters deviate beyond predefined thresholds. Diagnosis involves interpreting the code, understanding the "
            "associated subsystem, and performing systematic tests to isolate the root cause. The framework includes verifying sensor signals, checking "
            "wiring and connectors, and evaluating mechanical components. Confirmatory tests such as freeze frame data analysis and live data monitoring "
            "are essential. Repair decisions are based on the confirmed fault and its impact on emissions and drivability."
        ),
        key_factors=[
            "Code specificity and definition",
            "Freeze frame data availability",
            "Live sensor data trends",
            "Sensor and actuator functional tests",
            "Wiring and connector integrity",
            "Manufacturer service bulletins"
        ],
        primary_authority=[
            "SAE J2012 Diagnostic Trouble Codes Standard",
            "OBD-II Federal Regulations (EPA CFR 40 Part 86)",
            "ISO 15031-6 Communication Protocols"
        ],
        burden_holder="Service technician or diagnostic engineer",
        adversary_position="Claim that the code is a false positive or intermittent glitch not requiring repair",
        counter_arguments=[
            "Repeatability of the code under test conditions",
            "Correlation with symptoms and sensor data",
            "Historical data from vehicle operation",
            "Cross-check with other related codes"
        ],
        resolution_strategy=(
            "Perform comprehensive diagnostics following manufacturer procedures, "
            "verify code persistence, and confirm fault through functional testing before authorizing repairs."
        ),
        entity_scope="All gasoline and diesel vehicles equipped with OBD-II compliant ECMs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J1979 OBD-II Mode $03 and $07 Diagnostic Data Retrieval"
    ),
    DoctrineBlock(
        topic="Engine Misfire Diagnosis (P030x Codes)",
        keywords=["engine misfire", "P030x", "cylinder misfire", "combustion", "ignition", "fuel delivery"],
        conclusion_template="A P030x code indicates a misfire detected in cylinder x, necessitating a focused diagnosis on ignition, fuel, and mechanical integrity of that cylinder.",
        reasoning_framework=(
            "Engine misfire codes (P0300-P0308) are set when the ECM detects incomplete or failed combustion in one or more cylinders. "
            "The misfire detection algorithm uses crankshaft position sensor data to identify irregularities in rotational speed indicative of misfire. "
            "Diagnosis requires isolating the affected cylinder(s) and evaluating ignition components (spark plugs, coils), fuel delivery (injectors, pressure), "
            "and mechanical conditions (compression, valve timing). The reasoning includes ruling out sensor faults, verifying ECM logic, and considering "
            "external factors such as vacuum leaks or sensor contamination. A systematic approach ensures accurate identification of root causes."
        ),
        key_factors=[
            "Misfire detection algorithm output",
            "Ignition coil and spark plug condition",
            "Fuel injector operation and fuel pressure",
            "Cylinder compression and leak-down test results",
            "Vacuum leak presence",
            "Crankshaft and camshaft sensor signals"
        ],
        primary_authority=[
            "SAE J1979 OBD-II Misfire Detection",
            "Manufacturer Technical Service Bulletins (TSBs)",
            "Automotive Diagnostic Reference Manuals"
        ],
        burden_holder="Diagnostic technician",
        adversary_position="Misfire codes are transient or caused by external factors unrelated to engine components",
        counter_arguments=[
            "Code persistence over multiple drive cycles",
            "Correlation with drivability symptoms",
            "Data from secondary sensors (MAF, MAP, O2 sensors)",
            "Compression and leak-down test confirmation"
        ],
        resolution_strategy=(
            "Use a stepwise diagnostic process starting with ignition and fuel systems, "
            "followed by mechanical testing, to confirm and repair the root cause of misfire."
        ),
        entity_scope="Gasoline and some diesel engines with OBD-II misfire detection",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 15031-6 Misfire Detection Algorithms and Thresholds"
    ),
    DoctrineBlock(
        topic="Gasoline Direct Injection (GDI) Systems",
        keywords=["GDI", "gasoline direct injection", "fuel injection", "combustion", "injector", "high pressure"],
        conclusion_template="GDI systems improve fuel atomization and combustion efficiency but require specialized diagnostics for high-pressure fuel delivery and injector function.",
        reasoning_framework=(
            "Gasoline Direct Injection (GDI) technology injects fuel directly into the combustion chamber at high pressure, enabling precise fuel metering and improved combustion. "
            "The system includes a high-pressure fuel pump, fuel rail, injectors, and electronic controls. Diagnostics focus on detecting injector faults, pressure irregularities, "
            "and combustion anomalies such as carbon buildup on intake valves. The reasoning involves monitoring fuel rail pressure sensors, injector pulse width, and feedback from "
            "oxygen sensors. Special attention is given to high-pressure pump operation and potential mechanical wear. Carbon deposits can cause drivability issues and require inspection."
        ),
        key_factors=[
            "Fuel rail pressure sensor readings",
            "Injector pulse width and response",
            "High-pressure fuel pump operation",
            "Intake valve carbon buildup presence",
            "Oxygen sensor feedback",
            "Engine knock and combustion stability"
        ],
        primary_authority=[
            "SAE J2716 GDI System Standards",
            "Manufacturer Service Manuals for GDI systems",
            "Technical Papers on GDI Combustion and Emissions"
        ],
        burden_holder="Automotive diagnostic technician",
        adversary_position="GDI issues are caused by fuel quality or external contamination rather than system faults",
        counter_arguments=[
            "Diagnostic trouble codes specific to GDI components",
            "Fuel pressure and injector diagnostic data",
            "Visual inspection of intake valves",
            "Fuel quality analysis reports"
        ],
        resolution_strategy=(
            "Employ pressure and injector diagnostics, combined with visual inspection and cleaning procedures, "
            "to maintain GDI system performance and address faults."
        ),
        entity_scope="Modern gasoline engines equipped with direct injection systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2716 Fuel Injection System Terminology and Diagnostics"
    ),
    DoctrineBlock(
        topic="Catalytic Converter Diagnostics",
        keywords=["catalytic converter", "emissions", "catalyst efficiency", "oxygen sensors", "exhaust system", "DTC P0420"],
        conclusion_template="Catalytic converter efficiency faults are diagnosed by analyzing oxygen sensor data and exhaust emissions to determine catalyst degradation or failure.",
        reasoning_framework=(
            "The catalytic converter reduces harmful exhaust emissions by catalyzing chemical reactions. Its efficiency is monitored by comparing upstream and downstream oxygen sensor signals. "
            "A failing converter shows reduced oxygen storage capacity and altered sensor voltage patterns. Diagnostics involve analyzing sensor waveforms, performing temperature measurements, "
            "and checking for physical damage or clogging. The reasoning framework includes ruling out sensor faults, exhaust leaks, and engine misfires that can affect catalyst performance. "
            "Confirming catalyst degradation requires correlating sensor data with emissions test results and visual inspection."
        ),
        key_factors=[
            "Upstream and downstream oxygen sensor voltage patterns",
            "Catalyst temperature readings",
            "Exhaust backpressure measurements",
            "Presence of DTCs such as P0420 or P0430",
            "Physical inspection for damage or clogging",
            "Engine operating conditions during testing"
        ],
        primary_authority=[
            "EPA OBD-II Regulations",
            "SAE J1979 Mode $06 Catalyst Monitor Data",
            "Manufacturer Service Procedures for Catalyst Testing"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="Oxygen sensor faults or engine conditions cause false catalyst efficiency codes",
        counter_arguments=[
            "Sensor cross-testing and replacement",
            "Engine performance verification",
            "Exhaust leak detection",
            "Catalyst temperature and backpressure correlation"
        ],
        resolution_strategy=(
            "Systematically verify sensor operation and engine condition before confirming catalytic converter replacement."
        ),
        entity_scope="All vehicles equipped with catalytic converters and OBD-II monitors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 OBD-II Catalyst Monitor Requirements"
    ),
    DoctrineBlock(
        topic="Mass Airflow (MAF) Sensor Diagnosis",
        keywords=["MAF sensor", "mass airflow", "air intake", "sensor calibration", "engine load", "fuel metering"],
        conclusion_template="MAF sensor faults are diagnosed by evaluating sensor output against expected airflow values and engine operating parameters to ensure accurate fuel metering.",
        reasoning_framework=(
            "The Mass Airflow (MAF) sensor measures the volume and density of air entering the engine, providing critical input for fuel injection calculations. "
            "Diagnosis involves comparing sensor voltage or frequency output to expected values based on engine speed, throttle position, and intake air temperature. "
            "The reasoning includes checking for sensor contamination, wiring faults, and calibration errors. Abnormal readings can cause lean or rich conditions, affecting emissions and performance. "
            "Cross-checking with manifold absolute pressure (MAP) sensor data and oxygen sensor feedback helps isolate MAF sensor issues."
        ),
        key_factors=[
            "MAF sensor voltage or frequency output",
            "Engine RPM and load correlation",
            "Throttle position sensor data",
            "Intake air temperature sensor readings",
            "Oxygen sensor feedback",
            "Wiring and connector integrity"
        ],
        primary_authority=[
            "SAE J1979 Mode $01 PID 10 (MAF Sensor Data)",
            "Manufacturer Calibration Specifications",
            "Automotive Sensor Diagnostic Guides"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="MAF sensor readings are affected by external factors such as air leaks or sensor contamination, not sensor failure",
        counter_arguments=[
            "Sensor cleaning and retesting",
            "Leak detection and repair",
            "Cross-sensor data comparison",
            "Sensor replacement and verification"
        ],
        resolution_strategy=(
            "Perform sensor output verification under controlled conditions, clean or replace sensor as needed, "
            "and confirm correction of fuel metering anomalies."
        ),
        entity_scope="All vehicles using MAF sensors for engine management",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J1979 PID Definitions and Sensor Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Turbocharger Diagnostics",
        keywords=["turbocharger", "boost pressure", "wastegate", "turbo lag", "compressor", "turbine"],
        conclusion_template="Turbocharger faults are diagnosed by evaluating boost pressure behavior, actuator operation, and mechanical integrity of the turbo system components.",
        reasoning_framework=(
            "Turbochargers increase engine power by forcing more air into the combustion chamber. Diagnostics focus on boost pressure levels, wastegate actuator function, and mechanical condition of the compressor and turbine. "
            "The reasoning includes analyzing boost pressure sensor data against expected values, checking for boost leaks, and verifying actuator control signals. Mechanical inspection for shaft play, bearing wear, and compressor damage is essential. "
            "Symptoms such as turbo lag, overboost, or underboost guide the diagnostic process. Cross-referencing with engine load and RPM data helps isolate turbo-related issues."
        ),
        key_factors=[
            "Boost pressure sensor readings",
            "Wastegate actuator position and control signals",
            "Compressor and turbine shaft play",
            "Exhaust backpressure",
            "Engine RPM and load correlation",
            "Presence of boost leaks or intake restrictions"
        ],
        primary_authority=[
            "Manufacturer Turbocharger Service Manuals",
            "SAE Turbocharger Performance and Diagnostics Papers",
            "Automotive Turbocharger Diagnostic Standards"
        ],
        burden_holder="Turbocharger system diagnostician",
        adversary_position="Boost irregularities caused by external factors such as intake leaks or sensor faults",
        counter_arguments=[
            "Leak detection and repair",
            "Sensor cross-verification",
            "Mechanical inspection and testing",
            "Actuator function testing"
        ],
        resolution_strategy=(
            "Combine sensor data analysis with mechanical inspection and actuator testing to confirm turbocharger faults before repair."
        ),
        entity_scope="Vehicles equipped with turbocharged engines",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J1939 Turbocharger Diagnostics and Monitoring"
    ),
    DoctrineBlock(
        topic="Variable Valve Timing (VVT) Systems",
        keywords=["VVT", "variable valve timing", "camshaft phaser", "timing control", "engine performance"],
        conclusion_template="VVT system faults are diagnosed by analyzing camshaft position sensor data, actuator control signals, and engine performance parameters to detect timing discrepancies.",
        reasoning_framework=(
            "Variable Valve Timing (VVT) systems adjust valve timing dynamically to optimize engine performance and emissions. Diagnostics involve monitoring camshaft position sensors, VVT actuator commands, and engine speed/load parameters. "
            "The reasoning framework includes detecting timing errors, actuator failures, and oil control valve issues. Symptoms such as rough idle, reduced power, or check engine light illuminate when VVT faults occur. "
            "Cross-checking timing data with crankshaft position sensors and evaluating oil pressure and quality are also important. Diagnosis requires a combination of sensor data analysis and mechanical inspection."
        ),
        key_factors=[
            "Camshaft and crankshaft position sensor signals",
            "VVT actuator command and feedback",
            "Engine RPM and load data",
            "Oil pressure and quality",
            "Presence of DTCs related to VVT",
            "Mechanical inspection of camshaft phasers"
        ],
        primary_authority=[
            "Manufacturer VVT System Service Manuals",
            "SAE J1979 Mode $01 PID Definitions",
            "Technical Papers on VVT System Diagnostics"
        ],
        burden_holder="Engine performance diagnostician",
        adversary_position="VVT faults caused by sensor errors or transient oil pressure fluctuations",
        counter_arguments=[
            "Sensor signal validation",
            "Oil pressure testing",
            "Repeatability of fault codes",
            "Mechanical inspection and testing"
        ],
        resolution_strategy=(
            "Integrate sensor data analysis with mechanical and oil system inspection to accurately diagnose VVT faults."
        ),
        entity_scope="Engines equipped with variable valve timing technology",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and Manufacturer VVT Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Diagnostics",
        keywords=["diesel engine", "compression ignition", "fuel injection", "glow plugs", "EGR", "NOx emissions"],
        conclusion_template="Diesel engine faults require diagnostics focused on compression, fuel injection timing, and emission control systems such as EGR and aftertreatment.",
        reasoning_framework=(
            "Diesel engines operate on compression ignition, requiring high compression ratios and precise fuel injection timing. Diagnostics include verifying compression levels, injector operation, glow plug function, and emission control devices such as EGR valves and particulate filters. "
            "The reasoning framework involves analyzing sensor data (fuel rail pressure, crankshaft position), performing compression and leak-down tests, and evaluating emission system performance. "
            "NOx and particulate emissions are tightly regulated, so emission control system diagnostics are critical. Fault codes related to these systems guide the diagnostic process."
        ),
        key_factors=[
            "Cylinder compression test results",
            "Fuel rail pressure and injector timing",
            "Glow plug operation and control",
            "EGR valve position and function",
            "Diesel particulate filter (DPF) status",
            "Emission sensor data (NOx sensors, O2 sensors)"
        ],
        primary_authority=[
            "SAE J1939 Diesel Engine Diagnostics",
            "EPA Diesel Emission Regulations",
            "Manufacturer Diesel Engine Service Manuals"
        ],
        burden_holder="Diesel engine diagnostic technician",
        adversary_position="Emission control faults caused by fuel quality or external contamination",
        counter_arguments=[
            "Fuel quality testing",
            "Sensor and actuator functional tests",
            "Emission system cleaning and regeneration verification",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Conduct comprehensive mechanical and emission system diagnostics to identify and repair diesel engine faults."
        ),
        entity_scope="Diesel-powered vehicles and equipment",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 1065 Diesel Engine Testing Procedures"
    ),
    DoctrineBlock(
        topic="Engine Cooling System Diagnostics",
        keywords=["engine cooling", "thermostat", "coolant temperature", "radiator", "coolant flow", "overheating"],
        conclusion_template="Cooling system faults are diagnosed by evaluating coolant temperature sensor data, thermostat operation, and coolant flow integrity to prevent engine overheating.",
        reasoning_framework=(
            "The engine cooling system maintains optimal operating temperature by circulating coolant through the engine and radiator. Diagnostics focus on coolant temperature sensor readings, thermostat function, radiator condition, and coolant flow. "
            "The reasoning includes detecting thermostat sticking, coolant leaks, radiator blockages, and water pump failures. Symptoms such as overheating, temperature fluctuations, or heater malfunction guide the diagnostic process. "
            "Cross-checking sensor data with physical inspection and pressure testing ensures accurate diagnosis."
        ),
        key_factors=[
            "Coolant temperature sensor output",
            "Thermostat opening and closing behavior",
            "Coolant flow rate and pressure",
            "Radiator condition and blockage",
            "Water pump operation",
            "Presence of coolant leaks"
        ],
        primary_authority=[
            "Manufacturer Cooling System Service Manuals",
            "SAE J1939 Cooling System Diagnostics",
            "Automotive Thermal Management Standards"
        ],
        burden_holder="Cooling system diagnostician",
        adversary_position="Temperature sensor faults or external factors causing false overheating indications",
        counter_arguments=[
            "Sensor cross-testing",
            "Pressure and flow testing",
            "Thermostat functional testing",
            "Visual inspection for leaks and blockages"
        ],
        resolution_strategy=(
            "Combine sensor data analysis with mechanical and hydraulic testing to confirm cooling system faults."
        ),
        entity_scope="All internal combustion engine vehicles",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1939 Thermal Management Diagnostics"
    ),
    DoctrineBlock(
        topic="Hybrid Vehicle Powertrain Basics",
        keywords=["hybrid vehicle", "powertrain", "electric motor", "battery management", "regenerative braking"],
        conclusion_template="Hybrid powertrain diagnostics require understanding the interaction between internal combustion engine and electric motor systems, including battery state and regenerative functions.",
        reasoning_framework=(
            "Hybrid vehicles combine an internal combustion engine with electric motors and battery packs to optimize fuel efficiency and emissions. Diagnostics involve monitoring battery state of charge, electric motor function, power electronics, and regenerative braking systems. "
            "The reasoning framework includes evaluating high-voltage system safety, state of health of battery modules, inverter operation, and control strategies coordinating engine and motor operation. Fault codes may relate to electric drive components or traditional engine systems. "
            "Understanding the hybrid architecture is essential for accurate diagnostics and repair."
        ),
        key_factors=[
            "Battery state of charge and health",
            "Electric motor torque and speed data",
            "Inverter and power electronics status",
            "Regenerative braking system operation",
            "High-voltage system safety interlocks",
            "Internal combustion engine integration"
        ],
        primary_authority=[
            "SAE J2954 Wireless Power Transfer and Hybrid Systems",
            "Manufacturer Hybrid System Service Manuals",
            "UL 2202 Electric Vehicle Charging System Standards"
        ],
        burden_holder="Hybrid system diagnostic technician",
        adversary_position="Faults attributed to hybrid system are caused by external electrical issues or user operation",
        counter_arguments=[
            "Systematic high-voltage system testing",
            "Battery module diagnostics",
            "Power electronics functional tests",
            "Cross-system data correlation"
        ],
        resolution_strategy=(
            "Use specialized hybrid diagnostic tools and procedures to isolate faults within electric and combustion subsystems."
        ),
        entity_scope="Hybrid electric vehicles with combined powertrains",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SAE J2847/1 Hybrid Vehicle Communication Protocols"
    ),
    DoctrineBlock(
        topic="No-Start Diagnosis Decision Tree",
        keywords=["no-start", "engine cranking", "fuel delivery", "ignition", "starter motor", "battery"],
        conclusion_template="No-start conditions are diagnosed through a systematic decision tree evaluating battery health, starter operation, fuel delivery, and ignition system functionality.",
        reasoning_framework=(
            "When an engine fails to start, diagnostics follow a structured decision tree beginning with verifying battery voltage and starter motor operation. "
            "Next, fuel delivery is assessed by checking fuel pump operation, pressure, and injector function. Ignition system components including coils, spark plugs, and control modules are evaluated. "
            "Sensor inputs such as crankshaft and camshaft position sensors are verified for proper signals. The reasoning framework emphasizes isolating electrical, fuel, and ignition faults sequentially to efficiently identify root causes."
        ),
        key_factors=[
            "Battery voltage and condition",
            "Starter motor engagement and current draw",
            "Fuel pump operation and pressure",
            "Ignition coil and spark plug condition",
            "Crankshaft and camshaft sensor signals",
            "ECM diagnostic trouble codes"
        ],
        primary_authority=[
            "Manufacturer No-Start Diagnostic Procedures",
            "SAE J1979 OBD-II Diagnostic Standards",
            "Automotive Electrical System Testing Guides"
        ],
        burden_holder="Diagnostic technician",
        adversary_position="No-start caused by intermittent or external conditions not related to vehicle systems",
        counter_arguments=[
            "Repeatability of no-start condition",
            "Comprehensive electrical and fuel system testing",
            "Sensor signal verification",
            "ECM data analysis"
        ],
        resolution_strategy=(
            "Follow a logical no-start diagnostic decision tree, verifying each subsystem before concluding fault."
        ),
        entity_scope="All internal combustion engine vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Manufacturer No-Start Troubleshooting Flowcharts"
    ),
    DoctrineBlock(
        topic="Oxygen Sensor Operation and Diagnosis",
        keywords=["oxygen sensor", "O2 sensor", "lambda sensor", "exhaust gas", "emissions", "sensor voltage"],
        conclusion_template="Oxygen sensor faults are diagnosed by analyzing sensor voltage signals and response times to ensure accurate air-fuel ratio feedback for engine control.",
        reasoning_framework=(
            "Oxygen sensors monitor the oxygen content in exhaust gases to provide feedback for air-fuel mixture control. Diagnostics involve evaluating sensor voltage output, switching frequency, and response time. "
            "The reasoning framework includes checking sensor heater operation, wiring integrity, and sensor contamination. Slow or erratic sensor response can cause fuel control issues and emissions faults. "
            "Cross-checking with fuel trim data and other emission sensors helps isolate oxygen sensor faults."
        ),
        key_factors=[
            "Sensor voltage output and waveform",
            "Heater circuit functionality",
            "Response time to air-fuel changes",
            "Wiring and connector condition",
            "Fuel trim adjustments",
            "Related DTCs (e.g., P0130-P0167)"
        ],
        primary_authority=[
            "SAE J1979 OBD-II Oxygen Sensor Monitoring",
            "Manufacturer Sensor Diagnostic Procedures",
            "EPA Emission Control Regulations"
        ],
        burden_holder="Emission system diagnostician",
        adversary_position="Sensor faults caused by exhaust leaks or fuel system issues",
        counter_arguments=[
            "Leak detection and repair",
            "Fuel system diagnostics",
            "Sensor replacement and retesting",
            "Cross-sensor data correlation"
        ],
        resolution_strategy=(
            "Perform sensor functional tests and verify related system conditions before sensor replacement."
        ),
        entity_scope="Vehicles equipped with oxygen sensors for emission control",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 OBD-II Oxygen Sensor Monitoring"
    ),
    DoctrineBlock(
        topic="EGR System Diagnosis",
        keywords=["EGR", "exhaust gas recirculation", "emissions", "EGR valve", "vacuum control", "DPFE sensor"],
        conclusion_template="EGR system faults are diagnosed by verifying valve operation, control signals, and sensor feedback to ensure proper exhaust gas recirculation and emissions control.",
        reasoning_framework=(
            "The Exhaust Gas Recirculation (EGR) system reduces NOx emissions by recirculating a portion of exhaust gases back into the intake manifold. Diagnostics focus on EGR valve operation, vacuum or electronic control signals, and feedback from sensors such as DPFE (differential pressure feedback EGR) sensors. "
            "The reasoning includes checking for valve sticking, vacuum leaks, sensor faults, and control module commands. Symptoms include rough idle, increased emissions, and fault codes. Cross-checking with engine load and temperature data aids diagnosis."
        ),
        key_factors=[
            "EGR valve position and movement",
            "Vacuum supply and control solenoids",
            "DPFE sensor voltage and response",
            "Engine load and temperature conditions",
            "Presence of DTCs related to EGR",
            "Vacuum leak detection"
        ],
        primary_authority=[
            "SAE J1979 OBD-II EGR System Monitoring",
            "Manufacturer EGR System Service Manuals",
            "EPA Emission Control Guidelines"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="EGR faults caused by sensor errors or external vacuum leaks",
        counter_arguments=[
            "Sensor and actuator functional testing",
            "Vacuum system inspection",
            "Repeatability of fault codes",
            "Cross-system data analysis"
        ],
        resolution_strategy=(
            "Verify EGR valve and sensor operation, repair vacuum leaks, and confirm system function before replacement."
        ),
        entity_scope="Vehicles equipped with EGR systems for emissions control",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 OBD-II EGR Monitor Requirements"
    ),
    DoctrineBlock(
        topic="EVAP System Diagnosis",
        keywords=["EVAP", "evaporative emissions", "fuel vapor", "purge valve", "vent valve", "leak detection"],
        conclusion_template="EVAP system faults are diagnosed by testing for leaks, verifying purge and vent valve operation, and analyzing sensor data to control fuel vapor emissions.",
        reasoning_framework=(
            "The Evaporative Emission Control (EVAP) system prevents fuel vapors from escaping into the atmosphere by capturing and purging them into the engine intake. Diagnostics involve leak detection using smoke machines or pressure tests, verifying purge and vent valve operation, and monitoring fuel tank pressure sensors. "
            "The reasoning framework includes identifying leaks, valve malfunctions, and sensor faults. Fault codes such as P0440-P0457 guide diagnostics. Confirming system integrity requires both functional and leak tests."
        ),
        key_factors=[
            "Fuel tank pressure sensor readings",
            "Purge valve operation and control signals",
            "Vent valve function",
            "Leak detection results",
            "Fuel cap condition",
            "Presence of EVAP-related DTCs"
        ],
        primary_authority=[
            "EPA EVAP System Regulations",
            "SAE J1979 OBD-II EVAP Monitor",
            "Manufacturer EVAP System Service Manuals"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="EVAP faults caused by external factors such as loose fuel caps or ambient conditions",
        counter_arguments=[
            "Fuel cap inspection and replacement",
            "Leak testing with smoke or pressure",
            "Valve functional testing",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Perform thorough leak and functional testing of EVAP components before repair or replacement."
        ),
        entity_scope="All vehicles equipped with EVAP systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 OBD-II EVAP Monitor Requirements"
    ),
    DoctrineBlock(
        topic="Crankshaft and Camshaft Position Sensors",
        keywords=["crankshaft position sensor", "camshaft position sensor", "engine timing", "sensor signals", "ignition timing"],
        conclusion_template="Crankshaft and camshaft position sensor faults are diagnosed by analyzing sensor signal integrity and timing correlation to ensure proper engine operation.",
        reasoning_framework=(
            "Crankshaft and camshaft position sensors provide critical timing information to the ECM for ignition and fuel injection control. Diagnostics involve verifying sensor signal waveform, frequency, and timing relative to engine rotation. "
            "The reasoning includes checking sensor wiring, connector condition, and sensor alignment. Faulty or intermittent signals cause misfires, no-start conditions, or poor performance. Cross-checking sensor data with ignition and injection timing confirms diagnosis."
        ),
        key_factors=[
            "Sensor signal waveform and frequency",
            "Timing correlation between crankshaft and camshaft sensors",
            "Wiring and connector integrity",
            "Presence of DTCs related to sensor faults",
            "Engine performance symptoms",
            "Sensor physical condition and alignment"
        ],
        primary_authority=[
            "SAE J1979 OBD-II Sensor Monitoring",
            "Manufacturer Sensor Service Manuals",
            "Automotive Engine Timing Diagnostic Guides"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="Sensor faults caused by ECM software or external electrical interference",
        counter_arguments=[
            "Sensor replacement and retesting",
            "Wiring and connector inspection",
            "ECM software update verification",
            "Signal integrity testing"
        ],
        resolution_strategy=(
            "Verify sensor signals and wiring before concluding sensor or ECM faults."
        ),
        entity_scope="All internal combustion engines with electronic timing control",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1979 PID Definitions and Sensor Diagnostics"
    ),
    DoctrineBlock(
        topic="Ignition Coil Diagnosis (Coil-on-Plug)",
        keywords=["ignition coil", "coil-on-plug", "spark generation", "ignition system", "misfire"],
        conclusion_template="Coil-on-plug ignition coil faults are diagnosed by evaluating coil primary and secondary circuits, spark output, and misfire data to ensure reliable ignition.",
        reasoning_framework=(
            "Coil-on-plug ignition systems eliminate spark plug wires by placing individual coils directly on spark plugs. Diagnostics include testing coil primary resistance, secondary spark output, and ECM control signals. "
            "Misfire detection data helps identify faulty coils. The reasoning framework involves isolating coil faults from wiring or spark plug issues, verifying ECM commands, and checking for intermittent faults. "
            "Proper coil function is critical for combustion stability and emissions compliance."
        ),
        key_factors=[
            "Coil primary and secondary resistance measurements",
            "Spark output verification",
            "ECM ignition control signals",
            "Misfire detection data",
            "Wiring and connector condition",
            "Spark plug condition"
        ],
        primary_authority=[
            "Manufacturer Ignition System Service Manuals",
            "SAE J1979 OBD-II Misfire Monitoring",
            "Automotive Ignition Diagnostics References"
        ],
        burden_holder="Ignition system diagnostician",
        adversary_position="Misfires attributed to coil faults caused by spark plugs or wiring issues",
        counter_arguments=[
            "Spark plug inspection and replacement",
            "Wiring continuity testing",
            "Coil replacement and retesting",
            "ECM command verification"
        ],
        resolution_strategy=(
            "Perform comprehensive ignition system testing to isolate coil faults before replacement."
        ),
        entity_scope="Vehicles equipped with coil-on-plug ignition systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J1979 Misfire Detection and Ignition Diagnostics"
    ),
    DoctrineBlock(
        topic="Fuel Injector Diagnosis",
        keywords=["fuel injector", "fuel delivery", "injector pulse", "fuel pressure", "spray pattern"],
        conclusion_template="Fuel injector faults are diagnosed by analyzing injector pulse signals, fuel pressure, and spray pattern to ensure proper fuel delivery and combustion.",
        reasoning_framework=(
            "Fuel injectors deliver precise amounts of fuel into the combustion chamber or intake manifold. Diagnostics involve verifying injector pulse width and frequency, fuel rail pressure, and injector spray pattern. "
            "The reasoning includes checking for injector electrical faults, clogging, leakage, and mechanical damage. Symptoms such as rough idle, misfire, or poor fuel economy indicate injector issues. "
            "Testing methods include electrical resistance measurement, injector balance testing, and visual inspection of spray."
        ),
        key_factors=[
            "Injector pulse width and frequency",
            "Fuel rail pressure stability",
            "Injector electrical resistance",
            "Spray pattern and atomization",
            "Presence of DTCs related to injectors",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Fuel System Service Manuals",
            "SAE J2716 Fuel Injector Standards",
            "Automotive Fuel System Diagnostic Guides"
        ],
        burden_holder="Fuel system diagnostician",
        adversary_position="Fuel delivery issues caused by fuel quality or external contamination",
        counter_arguments=[
            "Fuel quality testing",
            "Injector cleaning and flow testing",
            "Electrical testing and wiring inspection",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Use electrical, mechanical, and performance tests to confirm injector faults before replacement."
        ),
        entity_scope="All fuel-injected internal combustion engines",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2716 Fuel Injector Diagnostics and Testing"
    ),
    DoctrineBlock(
        topic="Throttle Position Sensor Diagnosis",
        keywords=["throttle position sensor", "TPS", "accelerator pedal", "engine load", "sensor calibration"],
        conclusion_template="Throttle position sensor faults are diagnosed by verifying sensor output voltage against throttle angle and accelerator pedal input to ensure accurate engine load sensing.",
        reasoning_framework=(
            "The Throttle Position Sensor (TPS) monitors the position of the throttle plate, providing input for engine load calculation and fuel delivery. Diagnostics involve checking sensor output voltage or resistance across the throttle range, ensuring smooth and consistent response. "
            "The reasoning includes verifying sensor calibration, wiring integrity, and correlation with accelerator pedal position sensors. Faults cause drivability issues such as hesitation or surging. Cross-checking with ECM data and other sensors aids diagnosis."
        ),
        key_factors=[
            "TPS output voltage or resistance",
            "Throttle plate angle correlation",
            "Accelerator pedal position sensor data",
            "Wiring and connector condition",
            "Presence of DTCs related to TPS",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Sensor Service Manuals",
            "SAE J1979 OBD-II Sensor Monitoring",
            "Automotive Engine Control Diagnostic References"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="TPS faults caused by ECM calibration or external mechanical issues",
        counter_arguments=[
            "Sensor calibration verification",
            "Wiring and connector inspection",
            "Mechanical throttle linkage inspection",
            "ECM software updates"
        ],
        resolution_strategy=(
            "Perform sensor output verification and mechanical inspection before sensor replacement."
        ),
        entity_scope="Vehicles equipped with electronic throttle control",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J1979 PID Definitions and Sensor Diagnostics"
    ),
    DoctrineBlock(
        topic="Knock Sensor Diagnosis",
        keywords=["knock sensor", "engine knock", "detonation", "sensor signal", "ignition timing"],
        conclusion_template="Knock sensor faults are diagnosed by analyzing sensor signal patterns and engine control responses to detect and mitigate engine detonation.",
        reasoning_framework=(
            "Knock sensors detect engine detonation or knock by sensing vibrations. Diagnostics involve analyzing sensor signal frequency and amplitude, verifying sensor wiring and mounting, and confirming ECM knock control strategies. "
            "The reasoning includes correlating sensor data with ignition timing adjustments and engine operating conditions. Faulty sensors can cause poor performance or engine damage. Cross-checking with other sensors and ECM data ensures accurate diagnosis."
        ),
        key_factors=[
            "Knock sensor signal waveform and frequency",
            "Sensor mounting and wiring condition",
            "ECM ignition timing adjustments",
            "Engine operating conditions",
            "Presence of knock-related DTCs",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Knock Sensor Service Manuals",
            "SAE J1979 OBD-II Knock Sensor Monitoring",
            "Automotive Engine Control Diagnostic Guides"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="Knock sensor faults caused by external vibrations or ECM software issues",
        counter_arguments=[
            "Sensor replacement and retesting",
            "Wiring and mounting inspection",
            "ECM software updates",
            "Signal integrity testing"
        ],
        resolution_strategy=(
            "Verify sensor signals and mounting before replacing sensors or ECM components."
        ),
        entity_scope="All internal combustion engines with knock sensors",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1979 Knock Sensor Monitoring Procedures"
    ),
    DoctrineBlock(
        topic="Battery Management System (BMS) Diagnostics",
        keywords=["battery management system", "BMS", "state of charge", "state of health", "battery monitoring"],
        conclusion_template="BMS faults are diagnosed by evaluating battery voltage, current, temperature, and state of charge/health parameters to ensure reliable battery operation.",
        reasoning_framework=(
            "The Battery Management System (BMS) monitors and manages battery pack parameters including voltage, current, temperature, and state of charge (SOC) and health (SOH). Diagnostics involve analyzing sensor data, communication with battery modules, and verifying BMS control algorithms. "
            "The reasoning framework includes detecting cell imbalances, temperature extremes, and communication faults. Accurate BMS operation is critical for battery longevity and vehicle safety."
        ),
        key_factors=[
            "Battery voltage and current measurements",
            "Temperature sensor readings",
            "State of charge and health calculations",
            "Communication bus integrity",
            "Presence of BMS-related fault codes",
            "Battery pack balancing status"
        ],
        primary_authority=[
            "SAE J2464 Battery Management System Standards",
            "Manufacturer BMS Service Manuals",
            "UL 2580 Battery Safety Standards"
        ],
        burden_holder="Battery system diagnostician",
        adversary_position="BMS faults caused by battery aging or external electrical issues",
        counter_arguments=[
            "Battery pack testing",
            "Communication bus diagnostics",
            "Sensor calibration and replacement",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Perform comprehensive battery and BMS diagnostics using specialized tools before repair."
        ),
        entity_scope="Electric and hybrid vehicle battery systems",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SAE J2464 and Manufacturer BMS Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Exhaust Gas Temperature Sensor Diagnostics",
        keywords=["exhaust gas temperature sensor", "EGT sensor", "temperature monitoring", "emission control", "thermal protection"],
        conclusion_template="EGT sensor faults are diagnosed by verifying sensor output voltage or resistance against expected temperature ranges to protect emission control components.",
        reasoning_framework=(
            "Exhaust Gas Temperature (EGT) sensors monitor the temperature of exhaust gases to protect components such as catalytic converters and turbochargers from thermal damage. Diagnostics involve checking sensor output signals, wiring integrity, and response times. "
            "The reasoning framework includes correlating sensor data with engine operating conditions and emission control system status. Faulty sensors can cause incorrect thermal management and trigger fault codes."
        ),
        key_factors=[
            "Sensor output voltage or resistance",
            "Response time to temperature changes",
            "Wiring and connector condition",
            "Engine operating parameters",
            "Presence of EGT-related DTCs",
            "Thermal protection system status"
        ],
        primary_authority=[
            "Manufacturer Sensor Service Manuals",
            "SAE J1939 Thermal Management Standards",
            "Automotive Emission Control Diagnostic References"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="EGT sensor faults caused by external wiring or ECM issues",
        counter_arguments=[
            "Sensor replacement and retesting",
            "Wiring inspection",
            "ECM software verification",
            "Cross-system data analysis"
        ],
        resolution_strategy=(
            "Verify sensor signals and wiring before replacing sensors or ECM components."
        ),
        entity_scope="Vehicles equipped with EGT sensors for emission control",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J1939 and Manufacturer EGT Sensor Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Fuel Pressure Regulator Diagnostics",
        keywords=["fuel pressure regulator", "fuel system", "fuel pressure", "vacuum reference", "fuel delivery"],
        conclusion_template="Fuel pressure regulator faults are diagnosed by measuring fuel pressure under various operating conditions and verifying vacuum reference integrity.",
        reasoning_framework=(
            "The fuel pressure regulator maintains consistent fuel pressure to the injectors relative to manifold vacuum. Diagnostics involve measuring fuel pressure at idle, acceleration, and deceleration, and checking for vacuum leaks or diaphragm failures. "
            "The reasoning framework includes correlating fuel pressure data with engine load and RPM, and verifying regulator response to vacuum changes. Faulty regulators cause fuel pressure fluctuations, leading to drivability issues."
        ),
        key_factors=[
            "Fuel pressure measurements at various engine conditions",
            "Vacuum line integrity and pressure",
            "Regulator diaphragm condition",
            "Presence of fuel pressure-related DTCs",
            "Engine performance symptoms",
            "Fuel pump operation"
        ],
        primary_authority=[
            "Manufacturer Fuel System Service Manuals",
            "SAE J2716 Fuel System Diagnostics",
            "Automotive Fuel Pressure Regulation Standards"
        ],
        burden_holder="Fuel system diagnostician",
        adversary_position="Fuel pressure issues caused by fuel pump or filter problems",
        counter_arguments=[
            "Fuel pump and filter testing",
            "Vacuum leak detection",
            "Regulator functional testing",
            "Repeatability of fuel pressure anomalies"
        ],
        resolution_strategy=(
            "Perform comprehensive fuel system testing to isolate regulator faults before replacement."
        ),
        entity_scope="Vehicles with fuel pressure regulators in fuel delivery systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2716 Fuel System Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Intake Manifold Pressure (MAP) Sensor Diagnosis",
        keywords=["MAP sensor", "manifold absolute pressure", "engine load", "sensor calibration", "fuel metering"],
        conclusion_template="MAP sensor faults are diagnosed by comparing sensor output to expected manifold pressure values under various engine loads to ensure accurate fuel metering.",
        reasoning_framework=(
            "The Manifold Absolute Pressure (MAP) sensor measures intake manifold pressure to assist in calculating engine load and fuel delivery. Diagnostics involve verifying sensor voltage or frequency output against expected values at idle, acceleration, and steady-state conditions. "
            "The reasoning includes checking sensor calibration, wiring integrity, and cross-referencing with other sensors such as MAF and throttle position. Faulty MAP sensors cause drivability and emission issues."
        ),
        key_factors=[
            "MAP sensor output voltage or frequency",
            "Engine RPM and load correlation",
            "Throttle position sensor data",
            "Wiring and connector condition",
            "Presence of MAP-related DTCs",
            "Cross-sensor data consistency"
        ],
        primary_authority=[
            "Manufacturer Sensor Service Manuals",
            "SAE J1979 OBD-II Sensor Monitoring",
            "Automotive Engine Control Diagnostic References"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="MAP sensor faults caused by vacuum leaks or external factors",
        counter_arguments=[
            "Vacuum leak detection and repair",
            "Sensor calibration verification",
            "Wiring inspection",
            "Cross-sensor data analysis"
        ],
        resolution_strategy=(
            "Verify sensor output and related system conditions before sensor replacement."
        ),
        entity_scope="Vehicles equipped with MAP sensors",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J1979 PID Definitions and Sensor Diagnostics"
    ),
    DoctrineBlock(
        topic="Crankcase Ventilation System Diagnosis",
        keywords=["crankcase ventilation", "PCV valve", "engine blow-by", "vacuum leaks", "emissions"],
        conclusion_template="Crankcase ventilation system faults are diagnosed by verifying PCV valve operation, detecting vacuum leaks, and assessing blow-by gas management to control emissions.",
        reasoning_framework=(
            "The Positive Crankcase Ventilation (PCV) system recirculates blow-by gases from the crankcase back into the intake for combustion, reducing emissions. Diagnostics involve checking PCV valve function, hose integrity, and vacuum leaks. "
            "The reasoning includes evaluating engine vacuum levels, detecting oil contamination, and verifying emission control compliance. Faulty PCV systems cause rough idle, oil leaks, and increased emissions."
        ),
        key_factors=[
            "PCV valve operation and flow",
            "Vacuum hose integrity",
            "Engine vacuum levels",
            "Presence of oil contamination",
            "Emission system status",
            "DTCs related to crankcase ventilation"
        ],
        primary_authority=[
            "Manufacturer Emission Control Service Manuals",
            "EPA Emission Regulations",
            "Automotive Emission Control Diagnostic Guides"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="Crankcase ventilation faults caused by engine wear or external contamination",
        counter_arguments=[
            "PCV valve functional testing",
            "Vacuum leak detection",
            "Oil contamination analysis",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Perform functional and leak testing to confirm crankcase ventilation system faults before repair."
        ),
        entity_scope="All internal combustion engine vehicles",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 Emission Control Requirements"
    ),
    DoctrineBlock(
        topic="Starter Motor Diagnostics",
        keywords=["starter motor", "engine cranking", "solenoid", "battery current", "starter relay"],
        conclusion_template="Starter motor faults are diagnosed by measuring current draw, verifying solenoid operation, and testing starter relay and wiring to ensure engine cranking.",
        reasoning_framework=(
            "The starter motor initiates engine rotation for starting. Diagnostics involve measuring battery voltage and current draw during cranking, verifying solenoid engagement, and testing starter relay and wiring integrity. "
            "The reasoning includes identifying mechanical failures, electrical faults, and battery condition. Symptoms include no crank or slow crank conditions. Cross-checking with battery and ignition system data aids diagnosis."
        ),
        key_factors=[
            "Battery voltage and current during cranking",
            "Starter solenoid operation",
            "Starter relay function",
            "Wiring and connector condition",
            "Mechanical condition of starter motor",
            "Presence of starter-related DTCs"
        ],
        primary_authority=[
            "Manufacturer Electrical System Service Manuals",
            "SAE J1939 Electrical Diagnostics",
            "Automotive Starter System Diagnostic Guides"
        ],
        burden_holder="Electrical system diagnostician",
        adversary_position="Starter faults caused by battery or wiring issues",
        counter_arguments=[
            "Battery load testing",
            "Wiring and connector inspection",
            "Starter motor bench testing",
            "Repeatability of faults"
        ],
        resolution_strategy=(
            "Perform electrical and mechanical testing to isolate starter motor faults before replacement."
        ),
        entity_scope="All internal combustion engine vehicles",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J1939 Electrical System Diagnostics"
    ),
    DoctrineBlock(
        topic="Glow Plug System Diagnostics",
        keywords=["glow plug", "diesel engine", "cold start", "heater relay", "glow plug controller"],
        conclusion_template="Glow plug system faults are diagnosed by verifying glow plug resistance, heater relay operation, and controller signals to ensure reliable cold starts.",
        reasoning_framework=(
            "Glow plugs provide heat to diesel engine cylinders for cold starting. Diagnostics involve measuring glow plug resistance, verifying heater relay and controller operation, and checking wiring integrity. "
            "The reasoning includes detecting open or shorted glow plugs, relay failures, and control module faults. Symptoms include hard starting or extended cranking times in cold conditions."
        ),
        key_factors=[
            "Glow plug electrical resistance",
            "Heater relay operation",
            "Glow plug controller signals",
            "Wiring and connector condition",
            "Cold start performance",
            "Presence of glow plug-related DTCs"
        ],
        primary_authority=[
            "Manufacturer Diesel Engine Service Manuals",
            "SAE J1939 Glow Plug System Diagnostics",
            "Automotive Cold Start Diagnostic References"
        ],
        burden_holder="Diesel engine diagnostic technician",
        adversary_position="Cold start issues caused by fuel or battery problems",
        counter_arguments=[
            "Fuel system testing",
            "Battery condition verification",
            "Glow plug functional testing",
            "Repeatability of cold start issues"
        ],
        resolution_strategy=(
            "Perform electrical and control system testing to confirm glow plug faults before repair."
        ),
        entity_scope="Diesel engine vehicles equipped with glow plug systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1939 Glow Plug Diagnostics and Control"
    ),
    DoctrineBlock(
        topic="Exhaust Gas Recirculation (EGR) Cooler Diagnostics",
        keywords=["EGR cooler", "exhaust gas recirculation", "cooling system", "coolant leaks", "emissions"],
        conclusion_template="EGR cooler faults are diagnosed by inspecting for coolant leaks, verifying cooling efficiency, and analyzing emission control performance.",
        reasoning_framework=(
            "The EGR cooler reduces temperature of recirculated exhaust gases to lower NOx emissions. Diagnostics involve inspecting for coolant leaks, verifying coolant flow and temperature, and analyzing emission system performance. "
            "The reasoning includes detecting cracks, blockages, or corrosion in the cooler, and correlating faults with engine overheating or emissions issues."
        ),
        key_factors=[
            "Coolant leak detection around EGR cooler",
            "Coolant temperature and flow measurements",
            "Emission system performance data",
            "Presence of EGR cooler-related DTCs",
            "Engine overheating symptoms",
            "Physical inspection of EGR cooler"
        ],
        primary_authority=[
            "Manufacturer Emission Control Service Manuals",
            "EPA Emission Regulations",
            "Automotive Emission Control Diagnostic Guides"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="EGR cooler faults caused by external cooling system issues",
        counter_arguments=[
            "Cooling system pressure testing",
            "Emission system diagnostics",
            "Physical inspection and leak testing",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Perform integrated cooling and emission system diagnostics to confirm EGR cooler faults."
        ),
        entity_scope="Vehicles equipped with EGR coolers",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 Emission Control Requirements"
    ),
    DoctrineBlock(
        topic="Transmission Control Module (TCM) Diagnostics",
        keywords=["transmission control module", "TCM", "shift solenoids", "gear selection", "communication"],
        conclusion_template="TCM faults are diagnosed by analyzing shift solenoid operation, gear selection logic, and communication with ECM to ensure proper transmission function.",
        reasoning_framework=(
            "The Transmission Control Module (TCM) manages automatic transmission operation including gear shifts and solenoid control. Diagnostics involve verifying solenoid activation, gear selection signals, and communication with the ECM. "
            "The reasoning includes detecting electrical faults, software errors, and mechanical transmission issues. Fault codes and symptom analysis guide the diagnostic process."
        ),
        key_factors=[
            "Shift solenoid activation and resistance",
            "Gear selection sensor signals",
            "TCM-ECM communication status",
            "Presence of transmission-related DTCs",
            "Transmission performance symptoms",
            "Wiring and connector condition"
        ],
        primary_authority=[
            "Manufacturer Transmission Service Manuals",
            "SAE J1939 Transmission Diagnostics",
            "Automotive Transmission Control Standards"
        ],
        burden_holder="Transmission system diagnostician",
        adversary_position="Transmission faults caused by mechanical wear or external electrical issues",
        counter_arguments=[
            "Mechanical transmission inspection",
            "Electrical testing of solenoids and wiring",
            "Communication bus diagnostics",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Integrate electrical, mechanical, and communication diagnostics to isolate TCM faults."
        ),
        entity_scope="Vehicles with electronically controlled automatic transmissions",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1939 and Manufacturer Transmission Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Battery State of Charge (SOC) Estimation",
        keywords=["battery state of charge", "SOC", "battery management", "voltage measurement", "current integration"],
        conclusion_template="Battery SOC estimation is performed by integrating current flow and measuring voltage to provide accurate battery charge status for vehicle control.",
        reasoning_framework=(
            "State of Charge (SOC) estimation combines voltage measurement, current integration (coulomb counting), and temperature compensation to assess battery charge level. Diagnostics involve verifying sensor accuracy, calibration, and algorithm integrity. "
            "The reasoning framework includes detecting sensor drift, communication errors, and battery aging effects. Accurate SOC estimation is critical for energy management and vehicle operation."
        ),
        key_factors=[
            "Battery voltage and current sensor accuracy",
            "Temperature sensor data",
            "SOC estimation algorithm performance",
            "Communication bus integrity",
            "Battery aging and capacity data",
            "Presence of BMS fault codes"
        ],
        primary_authority=[
            "SAE J2464 Battery Management Standards",
            "Manufacturer BMS Service Manuals",
            "Battery Technology Research Papers"
        ],
        burden_holder="Battery management system diagnostician",
        adversary_position="SOC errors caused by sensor faults or external conditions",
        counter_arguments=[
            "Sensor calibration and replacement",
            "Algorithm verification",
            "Communication diagnostics",
            "Battery capacity testing"
        ],
        resolution_strategy=(
            "Perform sensor and algorithm verification to ensure accurate SOC estimation."
        ),
        entity_scope="Electric and hybrid vehicle battery systems",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="SAE J2464 and Manufacturer BMS Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Fuel Tank Pressure Sensor Diagnostics",
        keywords=["fuel tank pressure sensor", "EVAP system", "pressure monitoring", "leak detection"],
        conclusion_template="Fuel tank pressure sensor faults are diagnosed by verifying sensor output against expected pressure ranges to support EVAP leak detection.",
        reasoning_framework=(
            "The fuel tank pressure sensor monitors pressure changes in the fuel tank to detect leaks in the EVAP system. Diagnostics involve checking sensor voltage or frequency output, response to pressure changes, and wiring integrity. "
            "The reasoning includes correlating sensor data with leak test results and other EVAP components. Faulty sensors can cause false leak detection or missed leaks."
        ),
        key_factors=[
            "Sensor output voltage or frequency",
            "Response to pressure changes during leak tests",
            "Wiring and connector condition",
            "Presence of EVAP-related DTCs",
            "Correlation with leak detection test results",
            "Fuel tank and EVAP system condition"
        ],
        primary_authority=[
            "EPA EVAP System Regulations",
            "Manufacturer EVAP System Service Manuals",
            "SAE J1979 OBD-II EVAP Monitor"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="Sensor faults caused by external factors or fuel tank issues",
        counter_arguments=[
            "Sensor replacement and retesting",
            "Wiring inspection",
            "Fuel tank inspection",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Verify sensor operation and system integrity before sensor replacement."
        ),
        entity_scope="Vehicles equipped with EVAP systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 OBD-II EVAP Monitor Requirements"
    ),
    DoctrineBlock(
        topic="Camshaft Phaser Diagnostics",
        keywords=["camshaft phaser", "VVT", "timing control", "actuator", "oil control valve"],
        conclusion_template="Camshaft phaser faults are diagnosed by analyzing actuator response, oil control valve operation, and camshaft timing relative to crankshaft signals.",
        reasoning_framework=(
            "Camshaft phasers adjust valve timing in VVT systems using hydraulic or electronic actuators controlled by oil control valves. Diagnostics involve verifying actuator movement, oil control valve operation, and timing correlation between camshaft and crankshaft sensors. "
            "The reasoning includes detecting mechanical wear, oil contamination, and control signal faults. Symptoms include rough idle, reduced power, and fault codes."
        ),
        key_factors=[
            "Actuator response and movement",
            "Oil control valve operation and control signals",
            "Camshaft and crankshaft sensor timing correlation",
            "Presence of VVT-related DTCs",
            "Oil quality and pressure",
            "Mechanical inspection of phaser components"
        ],
        primary_authority=[
            "Manufacturer VVT System Service Manuals",
            "SAE J1979 VVT Diagnostics",
            "Automotive Engine Timing Diagnostic Guides"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="Phaser faults caused by oil quality or sensor errors",
        counter_arguments=[
            "Oil analysis and replacement",
            "Sensor signal verification",
            "Mechanical inspection",
            "Repeatability of fault codes"
        ],
        resolution_strategy=(
            "Integrate actuator, sensor, and mechanical diagnostics to confirm camshaft phaser faults."
        ),
        entity_scope="Engines equipped with camshaft phasers for VVT",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and Manufacturer VVT Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Crankshaft Position Sensor Signal Integrity",
        keywords=["crankshaft position sensor", "signal integrity", "waveform", "engine timing", "sensor noise"],
        conclusion_template="Crankshaft position sensor signal faults are diagnosed by analyzing waveform quality, signal amplitude, and noise to ensure accurate engine timing.",
        reasoning_framework=(
            "The crankshaft position sensor provides critical timing signals to the ECM. Diagnostics involve capturing sensor waveforms using oscilloscopes or scan tools to evaluate signal amplitude, frequency, and noise. "
            "The reasoning includes detecting sensor misalignment, wiring interference, or sensor damage. Poor signal integrity causes misfires, no-starts, or erratic engine behavior."
        ),
        key_factors=[
            "Sensor waveform amplitude and shape",
            "Signal frequency and consistency",
            "Electrical noise and interference",
            "Wiring and connector condition",
            "Presence of sensor-related DTCs",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Sensor Service Manuals",
            "SAE J1979 Sensor Diagnostics",
            "Automotive Engine Timing Diagnostic References"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="Signal faults caused by ECM software or external interference",
        counter_arguments=[
            "Sensor replacement and retesting",
            "Wiring and shielding inspection",
            "ECM software verification",
            "Signal integrity testing"
        ],
        resolution_strategy=(
            "Verify sensor waveform and wiring before replacing sensors or ECM components."
        ),
        entity_scope="All internal combustion engines with crankshaft position sensors",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1979 PID Definitions and Sensor Diagnostics"
    ),
    DoctrineBlock(
        topic="Fuel Pump Diagnostics",
        keywords=["fuel pump", "fuel delivery", "fuel pressure", "pump current", "fuel system"],
        conclusion_template="Fuel pump faults are diagnosed by measuring fuel pressure, pump current draw, and verifying electrical supply to ensure consistent fuel delivery.",
        reasoning_framework=(
            "The fuel pump supplies fuel under pressure to the injectors. Diagnostics involve measuring fuel pressure at the rail, monitoring pump current draw, and verifying electrical supply and ground. "
            "The reasoning includes detecting pump wear, electrical faults, and fuel filter restrictions. Symptoms include hard start, stalling, or poor performance."
        ),
        key_factors=[
            "Fuel pressure measurements",
            "Pump current draw and voltage",
            "Electrical supply and ground integrity",
            "Fuel filter condition",
            "Presence of fuel system-related DTCs",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Fuel System Service Manuals",
            "SAE J2716 Fuel System Diagnostics",
            "Automotive Fuel Delivery System Guides"
        ],
        burden_holder="Fuel system diagnostician",
        adversary_position="Fuel delivery issues caused by fuel quality or external contamination",
        counter_arguments=[
            "Fuel quality testing",
            "Electrical testing",
            "Fuel filter inspection",
            "Repeatability of faults"
        ],
        resolution_strategy=(
            "Perform electrical and mechanical testing to isolate fuel pump faults before replacement."
        ),
        entity_scope="All fuel-injected internal combustion engines",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J2716 Fuel System Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Engine Oil Pressure Sensor Diagnostics",
        keywords=["engine oil pressure sensor", "oil pressure", "sensor output", "engine lubrication"],
        conclusion_template="Oil pressure sensor faults are diagnosed by verifying sensor output against actual oil pressure measurements to ensure proper engine lubrication monitoring.",
        reasoning_framework=(
            "The engine oil pressure sensor monitors oil pressure to protect engine lubrication. Diagnostics involve comparing sensor output voltage or resistance to mechanical oil pressure measurements using gauges. "
            "The reasoning includes checking sensor wiring, connector condition, and sensor calibration. Faulty sensors can cause false warnings or missed lubrication issues."
        ),
        key_factors=[
            "Sensor output voltage or resistance",
            "Mechanical oil pressure measurements",
            "Wiring and connector condition",
            "Presence of oil pressure-related DTCs",
            "Engine lubrication system status",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Engine Service Manuals",
            "SAE J1939 Engine Diagnostics",
            "Automotive Lubrication System Standards"
        ],
        burden_holder="Engine lubrication system diagnostician",
        adversary_position="Sensor faults caused by wiring or ECM issues",
        counter_arguments=[
            "Sensor replacement and retesting",
            "Wiring inspection",
            "ECM software verification",
            "Mechanical oil pressure testing"
        ],
        resolution_strategy=(
            "Verify sensor signals and mechanical oil pressure before replacing sensors."
        ),
        entity_scope="All internal combustion engines with oil pressure sensors",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1939 and Manufacturer Oil Pressure Sensor Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Idle Air Control Valve Diagnostics",
        keywords=["idle air control valve", "IAC", "idle speed", "airflow control", "engine idle"],
        conclusion_template="IAC valve faults are diagnosed by verifying valve operation, airflow changes, and ECM control signals to maintain stable engine idle speed.",
        reasoning_framework=(
            "The Idle Air Control (IAC) valve regulates airflow bypassing the throttle plate to control engine idle speed. Diagnostics involve verifying valve movement, airflow changes, and ECM command signals. "
            "The reasoning includes detecting valve sticking, electrical faults, and wiring issues. Faulty IAC valves cause unstable idle, stalling, or high idle speeds."
        ),
        key_factors=[
            "IAC valve movement and response",
            "Airflow changes during valve operation",
            "ECM control signals to IAC",
            "Wiring and connector condition",
            "Presence of idle-related DTCs",
            "Engine idle performance"
        ],
        primary_authority=[
            "Manufacturer Engine Control Service Manuals",
            "SAE J1979 OBD-II Idle Control Diagnostics",
            "Automotive Engine Idle Control References"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="Idle issues caused by vacuum leaks or sensor faults",
        counter_arguments=[
            "Vacuum leak detection",
            "Sensor cross-verification",
            "Valve cleaning and testing",
            "Repeatability of idle faults"
        ],
        resolution_strategy=(
            "Perform airflow and control signal diagnostics to confirm IAC valve faults."
        ),
        entity_scope="Vehicles equipped with IAC valves for idle control",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J1979 PID Definitions and Idle Control Diagnostics"
    ),
    DoctrineBlock(
        topic="Throttle Body Cleaning and Diagnostics",
        keywords=["throttle body", "cleaning", "carbon buildup", "idle control", "airflow restriction"],
        conclusion_template="Throttle body faults due to carbon buildup are diagnosed by inspecting airflow restriction and cleaning to restore proper idle and throttle response.",
        reasoning_framework=(
            "Carbon buildup on the throttle body can restrict airflow and affect idle control. Diagnostics involve visual inspection, airflow measurement, and evaluating idle stability. "
            "The reasoning includes correlating symptoms such as rough idle, hesitation, and stalling with throttle body condition. Cleaning procedures restore airflow and sensor accuracy."
        ),
        key_factors=[
            "Visual inspection of throttle body",
            "Airflow measurement",
            "Idle stability and performance",
            "Presence of related DTCs",
            "Throttle position sensor accuracy",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Engine Service Manuals",
            "Automotive Maintenance Guidelines",
            "SAE Technical Papers on Throttle Body Cleaning"
        ],
        burden_holder="Maintenance technician",
        adversary_position="Idle and performance issues caused by other engine systems",
        counter_arguments=[
            "Comprehensive engine diagnostics",
            "Sensor data analysis",
            "Repeatability of symptoms",
            "Post-cleaning performance verification"
        ],
        resolution_strategy=(
            "Perform throttle body cleaning and verify improvement before further diagnostics."
        ),
        entity_scope="All vehicles with electronic throttle bodies",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Manufacturer Maintenance Procedures and SAE Guidelines"
    ),
    DoctrineBlock(
        topic="Engine Knock Control Strategies",
        keywords=["engine knock", "knock control", "ignition timing", "sensor feedback", "ECM strategies"],
        conclusion_template="Engine knock control relies on sensor feedback to adjust ignition timing and prevent engine damage while maintaining performance.",
        reasoning_framework=(
            "Engine knock control systems use knock sensor feedback to detect detonation and adjust ignition timing accordingly. Diagnostics involve verifying sensor signals, ECM response, and timing adjustments. "
            "The reasoning includes ensuring sensor accuracy, ECM logic integrity, and mechanical engine condition. Effective knock control balances performance and engine protection."
        ),
        key_factors=[
            "Knock sensor signals",
            "ECM ignition timing adjustments",
            "Engine operating conditions",
            "Presence of knock-related DTCs",
            "Mechanical engine condition",
            "Sensor and ECM calibration"
        ],
        primary_authority=[
            "Manufacturer Engine Control Manuals",
            "SAE J1979 Knock Control Standards",
            "Automotive Engine Management References"
        ],
        burden_holder="Engine control system engineer",
        adversary_position="Knock control faults caused by sensor or ECM software issues",
        counter_arguments=[
            "Sensor and ECM software verification",
            "Mechanical engine inspection",
            "Signal integrity testing",
            "Repeatability of faults"
        ],
        resolution_strategy=(
            "Integrate sensor, ECM, and mechanical diagnostics to optimize knock control."
        ),
        entity_scope="All internal combustion engines with knock control",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and Manufacturer Knock Control Procedures"
    ),
    DoctrineBlock(
        topic="Engine Coolant Temperature Sensor Diagnostics",
        keywords=["engine coolant temperature sensor", "ECT sensor", "temperature monitoring", "engine warm-up"],
        conclusion_template="ECT sensor faults are diagnosed by verifying sensor output voltage or resistance against expected coolant temperature ranges to ensure proper engine warm-up and control.",
        reasoning_framework=(
            "The Engine Coolant Temperature (ECT) sensor monitors coolant temperature for engine management. Diagnostics involve checking sensor output signals, wiring integrity, and response to temperature changes. "
            "The reasoning includes correlating sensor data with engine warm-up behavior and fuel mixture control. Faulty sensors cause poor fuel economy, emissions, and drivability issues."
        ),
        key_factors=[
            "Sensor output voltage or resistance",
            "Response to coolant temperature changes",
            "Wiring and connector condition",
            "Engine warm-up performance",
            "Presence of ECT-related DTCs",
            "Fuel trim data"
        ],
        primary_authority=[
            "Manufacturer Engine Service Manuals",
            "SAE J1979 OBD-II Sensor Monitoring",
            "Automotive Engine Control Diagnostic References"
        ],
        burden_holder="Engine control system diagnostician",
        adversary_position="Sensor faults caused by wiring or ECM issues",
        counter_arguments=[
            "Sensor replacement and retesting",
            "Wiring inspection",
            "ECM software verification",
            "Cross-sensor data analysis"
        ],
        resolution_strategy=(
            "Verify sensor signals and wiring before replacing sensors."
        ),
        entity_scope="All internal combustion engines with ECT sensors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SAE J1979 PID Definitions and Sensor Diagnostics"
    ),
    DoctrineBlock(
        topic="Turbocharger Wastegate Actuator Diagnostics",
        keywords=["wastegate actuator", "turbocharger", "boost control", "actuator position", "vacuum control"],
        conclusion_template="Wastegate actuator faults are diagnosed by verifying actuator movement, control signals, and boost pressure response to maintain proper turbocharger operation.",
        reasoning_framework=(
            "The wastegate actuator controls exhaust flow to the turbocharger turbine, regulating boost pressure. Diagnostics involve verifying actuator movement via vacuum or electronic control, control signal integrity, and boost pressure response. "
            "The reasoning includes detecting actuator sticking, control valve faults, and mechanical linkage issues. Proper wastegate function prevents overboost and engine damage."
        ),
        key_factors=[
            "Actuator movement and response",
            "Control signal integrity",
            "Boost pressure sensor data",
            "Vacuum supply and control valves",
            "Presence of boost control-related DTCs",
            "Mechanical linkage condition"
        ],
        primary_authority=[
            "Manufacturer Turbocharger Service Manuals",
            "SAE J1939 Turbocharger Diagnostics",
            "Automotive Boost Control Standards"
        ],
        burden_holder="Turbocharger system diagnostician",
        adversary_position="Boost control faults caused by external leaks or sensor errors",
        counter_arguments=[
            "Leak detection and repair",
            "Sensor cross-verification",
            "Actuator functional testing",
            "Repeatability of faults"
        ],
        resolution_strategy=(
            "Combine actuator, sensor, and mechanical diagnostics to confirm wastegate actuator faults."
        ),
        entity_scope="Vehicles equipped with turbochargers and wastegate actuators",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SAE J1939 Turbocharger Control and Diagnostics"
    ),
    DoctrineBlock(
        topic="Engine Knock Sensor Calibration",
        keywords=["knock sensor", "calibration", "engine tuning", "sensor sensitivity", "ECM settings"],
        conclusion_template="Knock sensor calibration ensures sensor sensitivity and ECM settings optimize knock detection and engine performance.",
        reasoning_framework=(
            "Proper calibration of knock sensors and ECM settings is essential for accurate knock detection and engine tuning. Diagnostics involve verifying sensor sensitivity, ECM knock thresholds, and calibration parameters. "
            "The reasoning includes adjusting calibration to balance knock detection sensitivity and false positives, ensuring engine protection and performance."
        ),
        key_factors=[
            "Sensor sensitivity settings",
            "ECM knock detection thresholds",
            "Engine operating conditions",
            "Calibration parameter verification",
            "Presence of knock-related DTCs",
            "Engine performance data"
        ],
        primary_authority=[
            "Manufacturer Engine Control Calibration Manuals",
            "SAE J1979 Knock Sensor Standards",
            "Automotive Engine Tuning References"
        ],
        burden_holder="Engine calibration engineer",
        adversary_position="Knock sensor faults caused by improper calibration or software issues",
        counter_arguments=[
            "Calibration parameter review and adjustment",
            "Sensor functional testing",
            "ECM software updates",
            "Performance testing"
        ],
        resolution_strategy=(
            "Perform calibration verification and adjustment to optimize knock sensor performance."
        ),
        entity_scope="All internal combustion engines with knock sensors",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="SAE J1979 and Manufacturer Knock Sensor Calibration Procedures"
    ),
    DoctrineBlock(
        topic="Fuel Injector Electrical Circuit Diagnostics",
        keywords=["fuel injector", "electrical circuit", "resistance", "wiring", "ECM control"],
        conclusion_template="Fuel injector electrical circuit faults are diagnosed by measuring resistance, checking wiring continuity, and verifying ECM control signals.",
        reasoning_framework=(
            "Fuel injector operation depends on proper electrical circuit integrity. Diagnostics involve measuring injector coil resistance, checking wiring and connectors for continuity and shorts, and verifying ECM pulse signals. "
            "The reasoning includes isolating electrical faults from mechanical injector issues to ensure reliable fuel delivery."
        ),
        key_factors=[
            "Injector coil resistance measurements",
            "Wiring continuity and insulation",
            "Connector condition",
            "ECM injector control pulse verification",
            "Presence of injector-related DTCs",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "Manufacturer Fuel System Service Manuals",
            "SAE J2716 Fuel Injector Electrical Diagnostics",
            "Automotive Electrical System Diagnostic Guides"
        ],
        burden_holder="Fuel system diagnostician",
        adversary_position="Fuel delivery issues caused by mechanical injector faults",
        counter_arguments=[
            "Mechanical injector testing",
            "Electrical circuit testing",
            "Connector inspection",
            "Repeatability of faults"
        ],
        resolution_strategy=(
            "Perform electrical and mechanical testing to isolate injector circuit faults."
        ),
        entity_scope="All fuel-injected internal combustion engines",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2716 Fuel Injector Electrical Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Engine Crankcase Pressure Diagnostics",
        keywords=["crankcase pressure", "blow-by", "PCV system", "vacuum leaks", "emissions"],
        conclusion_template="Crankcase pressure faults are diagnosed by measuring pressure levels, detecting blow-by gases, and verifying PCV system operation to control emissions.",
        reasoning_framework=(
            "Excessive crankcase pressure indicates blow-by gases escaping past piston rings. Diagnostics involve measuring crankcase pressure, inspecting PCV system components, and detecting vacuum leaks. "
            "The reasoning includes correlating pressure levels with engine wear and emission control effectiveness."
        ),
        key_factors=[
            "Crankcase pressure measurements",
            "PCV valve operation",
            "Vacuum leak detection",
            "Engine wear indicators",
            "Emission system status",
            "Presence of related DTCs"
        ],
        primary_authority=[
            "Manufacturer Emission Control Service Manuals",
            "EPA Emission Regulations",
            "Automotive Emission Control Diagnostic Guides"
        ],
        burden_holder="Emission control system diagnostician",
        adversary_position="Crankcase pressure issues caused by external factors",
        counter_arguments=[
            "PCV system testing",
            "Vacuum leak repair",
            "Engine mechanical inspection",
            "Repeatability of faults"
        ],
        resolution_strategy=(
            "Perform pressure and system diagnostics to confirm crankcase pressure faults."
        ),
        entity_scope="All internal combustion engine vehicles",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EPA CFR 40 Part 86 Emission Control Requirements"
    ),
    DoctrineBlock(
        topic="Engine Oil Temperature Sensor Diagnostics",
        keywords=["engine oil temperature sensor", "