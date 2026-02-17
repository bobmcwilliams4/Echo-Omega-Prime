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
        topic="Common Rail High Pressure Fuel System Diagnostics",
        keywords=[
            "common rail", "high pressure", "fuel system", "diagnostics",
            "pressure sensor", "injector", "leakage", "rail pressure",
            "fuel pump", "pressure fluctuations"
        ],
        conclusion_template=(
            "Based on the analysis of rail pressure stability and injector "
            "response times, the high-pressure fuel system is {status}."
        ),
        reasoning_framework=(
            "The common rail system maintains fuel at high pressure to ensure "
            "optimal injection timing and atomization. Diagnostics involve "
            "monitoring rail pressure sensors for stability and detecting "
            "pressure drops indicative of leaks or pump failures. Injector "
            "performance is assessed by correlating pressure data with engine "
            "load and RPM. Fluctuations beyond specified thresholds suggest "
            "component degradation or system faults. The framework integrates "
            "sensor data fusion, temporal trend analysis, and fault code "
            "correlation to isolate issues."
        ),
        key_factors=[
            "Rail pressure sensor accuracy",
            "Injector opening and closing times",
            "Fuel pump delivery rate",
            "Pressure fluctuation amplitude",
            "Engine load correlation"
        ],
        primary_authority=[
            "Bosch Common Rail System Technical Manual",
            "SAE J2716 - Common Rail Fuel Injection System",
            "ISO 20896-1:2019 - Fuel Injection Equipment"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position=(
            "System pressure fluctuations are within acceptable limits and "
            "do not indicate a fault."
        ),
        counter_arguments=[
            "Transient pressure dips during rapid load changes are normal.",
            "Sensor calibration errors can mimic pressure instability."
        ],
        resolution_strategy=(
            "Perform sensor calibration verification, conduct static pressure "
            "tests, and cross-reference with injector performance data to "
            "confirm fault presence."
        ),
        entity_scope="Engine Fuel System Subsystem",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Bosch Diagnostic Procedures for Common Rail Systems"
    ),
    DoctrineBlock(
        topic="Turbocharger Boost Control and Compressor Surge Analysis",
        keywords=[
            "turbocharger", "boost control", "compressor surge",
            "wastegate", "boost pressure", "compressor map", "surge line",
            "pressure ratio", "mass flow rate", "engine load"
        ],
        conclusion_template=(
            "The turbocharger boost control system is {status} with respect "
            "to compressor surge occurrences under tested conditions."
        ),
        reasoning_framework=(
            "Turbocharger boost control regulates intake manifold pressure "
            "via wastegate actuation to optimize engine performance and "
            "prevent compressor surge. Surge occurs when flow falls below "
            "the compressor's stable operating range, causing flow reversal "
            "and potential damage. Analysis involves mapping boost pressure "
            "against engine load and RPM, comparing operating points to the "
            "compressor surge line on the compressor map. Control system "
            "response times and wastegate functionality are evaluated to "
            "ensure surge prevention."
        ),
        key_factors=[
            "Wastegate actuator response time",
            "Boost pressure stability",
            "Compressor map surge line proximity",
            "Engine RPM and load correlation",
            "Pressure ratio and mass flow rate"
        ],
        primary_authority=[
            "Garrett Turbocharger Technical Guide",
            "SAE J1849 - Turbocharger Compressor Surge Testing",
            "ISO 1585 - Engine Power Measurement"
        ],
        burden_holder="Engine Control Unit (ECU) Calibration Team",
        adversary_position=(
            "Observed pressure fluctuations are due to normal transient engine "
            "behavior, not compressor surge."
        ),
        counter_arguments=[
            "Transient boost pressure dips during gear shifts are expected.",
            "Wastegate hysteresis can cause minor pressure oscillations."
        ],
        resolution_strategy=(
            "Conduct steady-state and transient tests, analyze pressure and "
            "flow data against compressor maps, and validate wastegate "
            "actuation timing."
        ),
        entity_scope="Turbocharger System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Garrett Turbocharger Surge Prevention Guidelines"
    ),
    DoctrineBlock(
        topic="Diesel Particulate Filter Regeneration and Ash Loading",
        keywords=[
            "diesel particulate filter", "DPF", "regeneration",
            "ash loading", "soot accumulation", "backpressure",
            "exhaust temperature", "filter efficiency", "passive regeneration",
            "active regeneration"
        ],
        conclusion_template=(
            "DPF regeneration is {status} and ash loading levels are {ash_status}, "
            "impacting filter efficiency accordingly."
        ),
        reasoning_framework=(
            "The diesel particulate filter captures soot particles from exhaust "
            "gases to reduce emissions. Over time, soot accumulates and requires "
            "regeneration to oxidize the particulate matter. Ash, a non-combustible "
            "residue, accumulates separately and increases backpressure, reducing "
            "engine efficiency. Regeneration strategies include passive (continuous "
            "oxidation at high exhaust temperatures) and active (fuel injection to "
            "raise temperature). Monitoring involves measuring backpressure, exhaust "
            "temperature profiles, and filter differential pressure to assess "
            "regeneration effectiveness and ash accumulation."
        ),
        key_factors=[
            "Filter backpressure",
            "Exhaust temperature during regeneration",
            "Frequency and duration of active regeneration",
            "Ash accumulation rate",
            "Soot loading levels"
        ],
        primary_authority=[
            "Cummins DPF Maintenance Manual",
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "SAE J2711 - DPF Regeneration Testing"
        ],
        burden_holder="Fleet Maintenance Manager",
        adversary_position=(
            "Increased backpressure is due to exhaust system restrictions, not ash loading."
        ),
        counter_arguments=[
            "Exhaust leaks or damaged pipes can cause pressure anomalies.",
            "Sensor drift may misrepresent backpressure readings."
        ],
        resolution_strategy=(
            "Perform filter removal and weighing, validate sensor calibration, "
            "and conduct controlled regeneration cycles to isolate ash effects."
        ),
        entity_scope="Exhaust Aftertreatment System",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Cummins DPF Regeneration Protocols"
    ),
    DoctrineBlock(
        topic="Selective Catalytic Reduction DEF System Diagnostics",
        keywords=[
            "selective catalytic reduction", "SCR", "DEF", "diesel exhaust fluid",
            "NOx reduction", "injector diagnostics", "urea dosing", "sensor feedback",
            "catalyst efficiency", "emission control"
        ],
        conclusion_template=(
            "SCR DEF system diagnostics indicate {status} with respect to urea dosing "
            "accuracy and catalyst performance."
        ),
        reasoning_framework=(
            "The SCR system reduces NOx emissions by injecting diesel exhaust fluid "
            "(urea solution) into the exhaust stream, which reacts in the catalyst "
            "to convert NOx into nitrogen and water. Diagnostics focus on verifying "
            "DEF injector operation, urea concentration, dosing rates, and sensor "
            "feedback from NOx sensors upstream and downstream of the catalyst. "
            "Catalyst efficiency is inferred from NOx reduction rates and temperature "
            "profiles. Fault detection includes identifying injector clogging, sensor "
            "failures, and DEF quality issues."
        ),
        key_factors=[
            "DEF injector pulse width and frequency",
            "NOx sensor readings pre- and post-catalyst",
            "DEF tank level and quality",
            "Catalyst temperature",
            "Urea dosing accuracy"
        ],
        primary_authority=[
            "AdBlue/DEF System Manufacturer Guidelines",
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "SAE J2719 - SCR System Diagnostics"
        ],
        burden_holder="Emission Control Technician",
        adversary_position=(
            "NOx sensor discrepancies are due to sensor aging, not SCR system faults."
        ),
        counter_arguments=[
            "Sensor drift is common and can be compensated by ECU algorithms.",
            "DEF crystallization can cause intermittent injector issues."
        ],
        resolution_strategy=(
            "Calibrate NOx sensors, inspect DEF injector operation, and verify DEF "
            "fluid quality through chemical analysis."
        ),
        entity_scope="Exhaust Aftertreatment System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SCR System Diagnostic Procedures by OEM"
    ),
    DoctrineBlock(
        topic="Glow Plug System Operation and Pre-Heat Diagnostics",
        keywords=[
            "glow plug", "pre-heat", "cold start", "ignition aid",
            "resistance measurement", "control module", "heating time",
            "battery voltage", "engine start delay", "temperature sensor"
        ],
        conclusion_template=(
            "Glow plug system operation is {status} based on resistance checks and "
            "pre-heat cycle timing."
        ),
        reasoning_framework=(
            "Glow plugs provide necessary heat to aid diesel combustion during cold "
            "starts. Diagnostics involve measuring glow plug resistance to detect "
            "open or short circuits, verifying control module timing for pre-heat "
            "cycles, and monitoring battery voltage to ensure sufficient power. "
            "Engine start delay and exhaust temperature are correlated with glow plug "
            "performance to assess effectiveness. Faults include failed plugs, wiring "
            "issues, and control logic errors."
        ),
        key_factors=[
            "Glow plug resistance values",
            "Pre-heat cycle duration",
            "Battery voltage during pre-heat",
            "Engine start delay time",
            "Ambient temperature"
        ],
        primary_authority=[
            "Delphi Diesel Systems Technical Manual",
            "SAE J1939 - Glow Plug Control",
            "ISO 8178 - Engine Emission Measurement"
        ],
        burden_holder="Vehicle Maintenance Technician",
        adversary_position=(
            "Extended engine start delay is due to fuel system issues, not glow plug failure."
        ),
        counter_arguments=[
            "Fuel injector clogging can cause hard starts.",
            "Battery condition affects pre-heat performance."
        ],
        resolution_strategy=(
            "Perform electrical resistance tests, verify control signals, and cross-check "
            "fuel system diagnostics."
        ),
        entity_scope="Engine Starting System",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Delphi Glow Plug Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Fuel Quality Assessment and Contamination Analysis",
        keywords=[
            "diesel fuel", "quality assessment", "contamination",
            "water content", "microbial growth", "fuel filter clogging",
            "cetane number", "fuel additives", "particulate contamination",
            "fuel sampling"
        ],
        conclusion_template=(
            "Diesel fuel quality is {status} with contamination levels {contamination_level} "
            "affecting engine performance."
        ),
        reasoning_framework=(
            "Fuel quality directly impacts engine combustion efficiency and component "
            "longevity. Assessment involves sampling fuel for water content, microbial "
            "contamination, particulate matter, and cetane number. Water presence "
            "promotes corrosion and microbial growth, leading to filter clogging and "
            "injector damage. Fuel additives may mitigate contamination but require "
            "verification. Laboratory analysis combined with field filter clogging data "
            "provides a comprehensive contamination profile."
        ),
        key_factors=[
            "Water content percentage",
            "Microbial contamination presence",
            "Particulate matter size and concentration",
            "Cetane number",
            "Fuel additive concentration"
        ],
        primary_authority=[
            "ASTM D975 - Diesel Fuel Specifications",
            "ISO 4406 - Contamination Control",
            "SAE J1488 - Fuel Quality Analysis"
        ],
        burden_holder="Fuel Quality Assurance Team",
        adversary_position=(
            "Observed engine issues are unrelated to fuel quality but due to mechanical faults."
        ),
        counter_arguments=[
            "Injector wear can mimic fuel contamination symptoms.",
            "Fuel system maintenance history affects contamination impact."
        ],
        resolution_strategy=(
            "Conduct comprehensive fuel sampling, laboratory testing, and correlate with "
            "engine fault codes and maintenance records."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ASTM and ISO Fuel Quality Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Compression Testing and Cylinder Sealing",
        keywords=[
            "compression testing", "cylinder sealing", "leak-down test",
            "compression ratio", "valve sealing", "piston rings",
            "cylinder head gasket", "engine wear", "pressure decay",
            "engine performance"
        ],
        conclusion_template=(
            "Compression test results indicate cylinder sealing is {status} with "
            "pressure decay rates {decay_status}."
        ),
        reasoning_framework=(
            "Compression testing evaluates the integrity of the combustion chamber by "
            "measuring pressure buildup during the compression stroke. Leak-down tests "
            "quantify pressure loss over time to identify sealing issues in valves, "
            "piston rings, or head gaskets. Consistent compression across cylinders "
            "indicates good sealing, while deviations suggest wear or damage. Pressure "
            "decay analysis helps localize leaks by correlating with audible or sensor "
            "feedback. Engine performance data is used to support compression test findings."
        ),
        key_factors=[
            "Compression pressure values per cylinder",
            "Leak-down pressure decay rate",
            "Valve sealing condition",
            "Piston ring wear",
            "Cylinder head gasket integrity"
        ],
        primary_authority=[
            "SAE J1349 - Engine Power and Torque Measurement",
            "ISO 17025 - Testing and Calibration Laboratories",
            "Engine Manufacturer Compression Test Guidelines"
        ],
        burden_holder="Engine Diagnostic Specialist",
        adversary_position=(
            "Low compression readings are due to testing errors, not actual sealing faults."
        ),
        counter_arguments=[
            "Incorrect test procedure or equipment calibration can skew results.",
            "Cold engine temperature affects compression readings."
        ],
        resolution_strategy=(
            "Repeat tests under controlled conditions, verify equipment calibration, "
            "and perform complementary leak-down tests."
        ),
        entity_scope="Engine Mechanical System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Engine Manufacturer Compression Testing Protocols"
    ),
    DoctrineBlock(
        topic="Diesel Injection Timing and Valve Train Synchronization",
        keywords=[
            "injection timing", "valve train", "synchronization",
            "camshaft position", "fuel injection pump", "timing advance",
            "engine control unit", "valve overlap", "ignition delay",
            "engine performance"
        ],
        conclusion_template=(
            "Injection timing and valve train synchronization are {status}, ensuring "
            "optimal combustion and engine performance."
        ),
        reasoning_framework=(
            "Precise timing of fuel injection relative to valve events is critical for "
            "efficient combustion and emissions control. Synchronization involves aligning "
            "camshaft and crankshaft positions with injection pump timing. Deviations cause "
            "ignition delays, incomplete combustion, and increased emissions. Diagnostics "
            "include sensor data analysis from camshaft and crankshaft position sensors, "
            "timing marks inspection, and ECU timing parameter verification. Valve overlap "
            "and injection advance are adjusted to optimize performance across operating "
            "ranges."
        ),
        key_factors=[
            "Camshaft and crankshaft sensor signals",
            "Injection pump timing settings",
            "Valve opening and closing timing",
            "Ignition delay measurements",
            "ECU timing parameters"
        ],
        primary_authority=[
            "Bosch Diesel Injection Systems Manual",
            "SAE J1939 - Engine Timing Diagnostics",
            "ISO 8178 - Engine Emission Measurement"
        ],
        burden_holder="Engine Calibration Engineer",
        adversary_position=(
            "Timing variations are within manufacturer tolerances and do not affect engine performance."
        ),
        counter_arguments=[
            "Sensor signal noise can cause apparent timing discrepancies.",
            "Normal wear affects valve timing slightly without performance loss."
        ],
        resolution_strategy=(
            "Use high-precision timing equipment, perform sensor diagnostics, and "
            "cross-validate with engine performance data."
        ),
        entity_scope="Fuel Injection and Valve Train System",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Bosch Injection Timing Calibration Procedures"
    ),
    DoctrineBlock(
        topic="EGR System Diagnostics and Cooler Fouling Analysis",
        keywords=[
            "EGR", "exhaust gas recirculation", "cooler fouling",
            "EGR valve", "particulate buildup", "cooler efficiency",
            "exhaust backpressure", "NOx emissions", "temperature sensors",
            "flow rate"
        ],
        conclusion_template=(
            "EGR system diagnostics reveal {status} with cooler fouling levels "
            "{fouling_status} impacting system efficiency."
        ),
        reasoning_framework=(
            "The EGR system reduces NOx emissions by recirculating a portion of exhaust "
            "gases back into the intake manifold. Cooler fouling occurs due to particulate "
            "deposition inside the EGR cooler, reducing heat exchange efficiency and causing "
            "increased backpressure. Diagnostics involve measuring EGR flow rates, cooler "
            "temperature differentials, and exhaust backpressure. Valve operation is monitored "
            "for proper opening and closing. Fouling severity is assessed by comparing expected "
            "and actual cooler performance metrics."
        ),
        key_factors=[
            "EGR valve position and response",
            "Cooler inlet and outlet temperatures",
            "Exhaust backpressure",
            "Particulate deposition rate",
            "NOx emission levels"
        ],
        primary_authority=[
            "Cummins EGR System Service Manual",
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "SAE J2711 - EGR System Testing"
        ],
        burden_holder="Emission Control Specialist",
        adversary_position=(
            "Increased backpressure is due to exhaust restrictions unrelated to EGR cooler fouling."
        ),
        counter_arguments=[
            "Exhaust system damage or leaks can affect pressure readings.",
            "Sensor inaccuracies may misrepresent temperature differentials."
        ],
        resolution_strategy=(
            "Conduct physical inspection of EGR cooler, verify sensor calibration, "
            "and perform flow rate tests."
        ),
        entity_scope="Exhaust Gas Recirculation System",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Cummins EGR Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Oil Analysis and Wear Metal Trending",
        keywords=[
            "engine oil analysis", "wear metals", "oil contamination",
            "particle count", "viscosity", "oil degradation",
            "spectrometric analysis", "oil change interval",
            "engine wear monitoring", "oil additives"
        ],
        conclusion_template=(
            "Engine oil analysis indicates {status} wear metal levels and oil condition, "
            "suggesting {maintenance_action}."
        ),
        reasoning_framework=(
            "Regular engine oil analysis detects wear metals and contaminants that indicate "
            "engine component wear or oil degradation. Spectrometric analysis identifies "
            "elements such as iron, copper, and chromium, which correlate with wear of "
            "specific engine parts. Particle count and viscosity measurements assess oil "
            "cleanliness and lubrication quality. Trending these parameters over time enables "
            "predictive maintenance and optimized oil change intervals."
        ),
        key_factors=[
            "Concentration of wear metals (Fe, Cu, Cr, Al)",
            "Particle count per milliliter",
            "Oil viscosity at operating temperature",
            "Presence of contaminants (water, fuel dilution)",
            "Oil additive depletion"
        ],
        primary_authority=[
            "ASTM D5185 - Oil Analysis",
            "ISO 4406 - Contamination Control",
            "SAE J1839 - Engine Oil Analysis"
        ],
        burden_holder="Maintenance Planning Engineer",
        adversary_position=(
            "Elevated wear metals are due to transient operating conditions, not indicative of damage."
        ),
        counter_arguments=[
            "Short-term spikes may not reflect long-term wear trends.",
            "Sampling errors can affect analysis results."
        ],
        resolution_strategy=(
            "Perform repeated sampling, verify lab procedures, and correlate with engine operating history."
        ),
        entity_scope="Lubrication System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="ASTM and SAE Oil Analysis Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Cooling System and Cavitation Analysis",
        keywords=[
            "cooling system", "cavitation", "water pump",
            "coolant flow", "radiator efficiency", "temperature sensors",
            "coolant pressure", "cavitation damage", "engine overheating",
            "coolant quality"
        ],
        conclusion_template=(
            "Cooling system performance is {status} with cavitation presence {cavitation_status} "
            "affecting engine thermal management."
        ),
        reasoning_framework=(
            "The cooling system maintains engine temperature within operational limits. Cavitation "
            "occurs in the water pump or coolant passages when vapor bubbles form due to pressure "
            "drops, causing damage and reduced flow. Diagnostics include monitoring coolant flow rate, "
            "pressure, and temperature gradients across the radiator and engine. Visual inspection for "
            "cavitation damage and coolant quality tests are also performed. System inefficiencies lead "
            "to overheating and engine damage."
        ),
        key_factors=[
            "Coolant flow rate",
            "Water pump cavitation evidence",
            "Radiator inlet and outlet temperatures",
            "Coolant pressure",
            "Coolant chemical properties"
        ],
        primary_authority=[
            "SAE J1940 - Engine Cooling System Testing",
            "ISO 13709 - Pumps",
            "Engine Manufacturer Cooling System Guidelines"
        ],
        burden_holder="Engine Cooling System Technician",
        adversary_position=(
            "Temperature fluctuations are due to ambient conditions, not cooling system faults."
        ),
        counter_arguments=[
            "Environmental temperature changes affect coolant temperature readings.",
            "Sensor placement can cause measurement discrepancies."
        ],
        resolution_strategy=(
            "Conduct flow and pressure tests under controlled conditions, inspect pump for cavitation damage, "
            "and analyze coolant chemistry."
        ),
        entity_scope="Engine Cooling System",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SAE Cooling System Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Electrical System and Charging Analysis",
        keywords=[
            "electrical system", "charging system", "alternator",
            "battery voltage", "starter motor", "voltage regulator",
            "electrical load", "charging voltage", "battery health",
            "engine starting"
        ],
        conclusion_template=(
            "Electrical system charging performance is {status} with battery and alternator "
            "parameters within {parameter_status}."
        ),
        reasoning_framework=(
            "The electrical system supplies power for engine starting and operation of electrical "
            "components. The alternator charges the battery and powers loads during engine running. "
            "Diagnostics involve measuring battery voltage at rest and during cranking, alternator "
            "output voltage and current, voltage regulator operation, and electrical load demands. "
            "Battery health is assessed via conductance and capacity tests. Faults include weak batteries, "
            "alternator failures, and wiring issues."
        ),
        key_factors=[
            "Battery resting voltage",
            "Voltage during engine cranking",
            "Alternator output voltage and current",
            "Voltage regulator response",
            "Electrical load profile"
        ],
        primary_authority=[
            "SAE J1939 - Electrical System Diagnostics",
            "Battery Council International Standards",
            "ISO 16750 - Electrical and Electronic Equipment"
        ],
        burden_holder="Electrical Systems Technician",
        adversary_position=(
            "Battery voltage fluctuations are due to load variations, not system faults."
        ),
        counter_arguments=[
            "High electrical loads can cause temporary voltage drops.",
            "Battery aging affects voltage stability."
        ],
        resolution_strategy=(
            "Perform load tests, alternator bench testing, and battery capacity analysis."
        ),
        entity_scope="Engine Electrical System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE Electrical System Testing Guidelines"
    ),
    DoctrineBlock(
        topic="Diesel Fuel Injector Flow Balance and Pattern Testing",
        keywords=[
            "fuel injector", "flow balance", "spray pattern",
            "injector testing", "fuel atomization", "injection pressure",
            "nozzle condition", "fuel delivery", "engine performance",
            "emissions"
        ],
        conclusion_template=(
            "Fuel injector flow balance and spray pattern testing indicate injector "
            "condition is {status} with flow rates {flow_status}."
        ),
        reasoning_framework=(
            "Injectors must deliver precise fuel quantities with consistent spray patterns "
            "to ensure efficient combustion. Flow balance testing compares fuel delivery "
            "across injectors to detect deviations. Spray pattern analysis assesses atomization "
            "quality and nozzle condition. Testing involves bench flow measurements at specified "
            "pressures and visual inspection of spray patterns. Deviations indicate wear, clogging, "
            "or nozzle damage affecting engine performance and emissions."
        ),
        key_factors=[
            "Injector flow rate consistency",
            "Spray pattern uniformity",
            "Injection pressure",
            "Nozzle wear or damage",
            "Fuel delivery timing"
        ],
        primary_authority=[
            "Bosch Fuel Injector Testing Manual",
            "SAE J2716 - Common Rail Fuel Injection System",
            "ISO 4113 - Fuel Injector Testing"
        ],
        burden_holder="Fuel System Maintenance Technician",
        adversary_position=(
            "Injector flow variations are within acceptable manufacturing tolerances."
        ),
        counter_arguments=[
            "Minor flow differences do not significantly affect engine operation.",
            "Testing equipment calibration affects measurement accuracy."
        ],
        resolution_strategy=(
            "Use calibrated test benches, perform repeated tests, and correlate with engine performance data."
        ),
        entity_scope="Fuel Injection System",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Bosch Injector Testing Standards"
    ),
    DoctrineBlock(
        topic="Diesel Crankcase Ventilation and Blowby Management",
        keywords=[
            "crankcase ventilation", "blowby", "PCV valve",
            "oil mist", "pressure regulation", "engine emissions",
            "ventilation flow rate", "contaminant removal",
            "engine wear", "emission control"
        ],
        conclusion_template=(
            "Crankcase ventilation system is {status} with blowby levels {blowby_status} "
            "and ventilation flow rates {flow_status}."
        ),
        reasoning_framework=(
            "Crankcase ventilation manages gases that escape past piston rings (blowby) to "
            "reduce pressure buildup and remove contaminants. The Positive Crankcase Ventilation "
            "(PCV) valve regulates flow to the intake manifold. Diagnostics include measuring "
            "blowby gas volume, ventilation flow rates, and oil mist concentration. Excessive "
            "blowby indicates piston ring wear and increases emissions. Proper ventilation prevents "
            "oil contamination and pressure-related engine damage."
        ),
        key_factors=[
            "Blowby gas volume",
            "PCV valve operation",
            "Ventilation flow rate",
            "Oil mist concentration",
            "Engine wear indicators"
        ],
        primary_authority=[
            "SAE J1667 - Crankcase Emission Control",
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "Engine Manufacturer Ventilation Guidelines"
        ],
        burden_holder="Engine Emission Compliance Officer",
        adversary_position=(
            "Blowby levels are within normal limits and do not require intervention."
        ),
        counter_arguments=[
            "Engine age and operating conditions affect blowby rates.",
            "Measurement variability can cause inaccurate blowby assessment."
        ],
        resolution_strategy=(
            "Perform standardized blowby tests, inspect PCV valve function, and monitor engine wear."
        ),
        entity_scope="Crankcase Ventilation System",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SAE and EPA Crankcase Ventilation Standards"
    ),
    DoctrineBlock(
        topic="Common Rail Injector Nozzle Coking and Cleaning Procedures",
        keywords=[
            "common rail", "injector nozzle", "coking",
            "carbon deposits", "cleaning procedures", "fuel additives",
            "injector performance", "spray pattern", "combustion efficiency",
            "maintenance"
        ],
        conclusion_template=(
            "Injector nozzle coking level is {coking_level} and cleaning procedures "
            "are {cleaning_status} effective."
        ),
        reasoning_framework=(
            "Carbon deposits (coking) on injector nozzles impair spray patterns and fuel atomization, "
            "leading to incomplete combustion and increased emissions. Diagnosis involves visual inspection, "
            "performance testing, and fuel additive analysis. Cleaning procedures include chemical soaking, "
            "ultrasonic cleaning, and fuel system additives. Effectiveness is evaluated by restored spray "
            "pattern uniformity and engine performance improvements."
        ),
        key_factors=[
            "Injector nozzle deposit thickness",
            "Spray pattern degradation",
            "Fuel additive compatibility",
            "Cleaning method applied",
            "Post-cleaning injector flow rates"
        ],
        primary_authority=[
            "Bosch Injector Maintenance Manual",
            "SAE J2716 - Fuel Injector Cleaning",
            "ISO 4113 - Injector Cleaning Procedures"
        ],
        burden_holder="Fuel System Maintenance Technician",
        adversary_position=(
            "Observed injector performance issues are due to fuel quality, not nozzle coking."
        ),
        counter_arguments=[
            "Fuel contamination can mimic coking symptoms.",
            "Injector wear may cause similar performance degradation."
        ],
        resolution_strategy=(
            "Perform injector cleaning, verify fuel quality, and conduct flow and spray pattern tests."
        ),
        entity_scope="Fuel Injection System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Bosch Injector Cleaning Protocols"
    ),
    DoctrineBlock(
        topic="Turbocharger Bearing Wear and Lubrication Analysis",
        keywords=[
            "turbocharger", "bearing wear", "lubrication",
            "oil supply", "shaft play", "vibration analysis",
            "oil contamination", "bearing temperature", "engine load",
            "maintenance"
        ],
        conclusion_template=(
            "Turbocharger bearing wear is {wear_status} with lubrication system "
            "performance {lubrication_status}."
        ),
        reasoning_framework=(
            "Turbocharger bearings require continuous lubrication to prevent wear and overheating. "
            "Diagnostics include measuring shaft play, vibration signatures, bearing temperature, "
            "and oil contamination levels. Oil supply pressure and cleanliness are critical. Excessive "
            "bearing wear leads to turbocharger failure and engine performance loss. Vibration analysis "
            "helps detect early wear stages."
        ),
        key_factors=[
            "Shaft axial and radial play",
            "Bearing temperature",
            "Oil pressure and flow rate",
            "Oil contamination levels",
            "Vibration frequency and amplitude"
        ],
        primary_authority=[
            "Garrett Turbocharger Maintenance Manual",
            "SAE J1939 - Turbocharger Diagnostics",
            "ISO 10816 - Vibration Severity"
        ],
        burden_holder="Turbocharger Maintenance Engineer",
        adversary_position=(
            "Shaft play measurements are within tolerance and do not indicate bearing wear."
        ),
        counter_arguments=[
            "Normal operational wear can cause minor shaft play.",
            "Measurement errors can affect vibration analysis."
        ],
        resolution_strategy=(
            "Perform repeated measurements, oil analysis, and vibration monitoring over time."
        ),
        entity_scope="Turbocharger System",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Garrett Turbocharger Bearing Maintenance"
    ),
    DoctrineBlock(
        topic="Diesel Engine Exhaust Gas Temperature Sensor Diagnostics",
        keywords=[
            "exhaust gas temperature", "EGT sensor",
            "sensor calibration", "temperature range", "sensor drift",
            "emission control", "sensor failure", "engine protection",
            "thermal management", "diagnostics"
        ],
        conclusion_template=(
            "EGT sensor diagnostics indicate sensor status is {status} with calibration "
            "and response within {response_status}."
        ),
        reasoning_framework=(
            "Exhaust Gas Temperature sensors monitor thermal conditions critical for emission control "
            "and engine protection. Sensor diagnostics involve calibration verification, response time "
            "measurement, and drift detection. Faulty sensors can cause incorrect engine control actions, "
            "leading to emission violations or engine damage. Cross-referencing sensor data with expected "
            "temperature profiles and other sensors ensures reliability."
        ),
        key_factors=[
            "Sensor calibration accuracy",
            "Response time to temperature changes",
            "Sensor drift over time",
            "Signal noise and stability",
            "Cross-sensor data correlation"
        ],
        primary_authority=[
            "SAE J1939 - Temperature Sensor Diagnostics",
            "ISO 27145 - Sensor Calibration",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Engine Control Technician",
        adversary_position=(
            "Sensor anomalies are due to transient engine conditions, not sensor faults."
        ),
        counter_arguments=[
            "Rapid temperature changes can cause temporary sensor reading variations.",
            "Electrical interference may affect sensor signals."
        ],
        resolution_strategy=(
            "Perform sensor calibration checks, signal filtering, and comparative analysis with redundant sensors."
        ),
        entity_scope="Engine Sensor System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE and ISO Sensor Diagnostic Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Intake Air Filter Condition and Restriction Analysis",
        keywords=[
            "intake air filter", "filter restriction",
            "pressure drop", "airflow measurement", "engine performance",
            "filter clogging", "maintenance interval", "sensor data",
            "fuel efficiency", "emissions"
        ],
        conclusion_template=(
            "Intake air filter condition is {condition} with restriction levels "
            "{restriction_level} affecting engine airflow and performance."
        ),
        reasoning_framework=(
            "The intake air filter prevents particulate ingress into the engine. Filter clogging increases "
            "pressure drop across the filter, reducing airflow and affecting combustion efficiency. Diagnostics "
            "include measuring pressure differential, airflow rates, and correlating with engine performance "
            "metrics such as fuel efficiency and emissions. Regular maintenance intervals are established based "
            "on restriction thresholds."
        ),
        key_factors=[
            "Pressure drop across filter",
            "Airflow rate measurement",
            "Filter particulate loading",
            "Engine fuel efficiency",
            "Emission levels"
        ],
        primary_authority=[
            "SAE J726 - Air Cleaner Testing",
            "ISO 5011 - Air Filter Testing",
            "Engine Manufacturer Maintenance Guidelines"
        ],
        burden_holder="Vehicle Maintenance Supervisor",
        adversary_position=(
            "Pressure drop variations are due to ambient conditions, not filter clogging."
        ),
        counter_arguments=[
            "Humidity and temperature affect pressure readings.",
            "Sensor placement can influence measurement accuracy."
        ],
        resolution_strategy=(
            "Conduct filter inspection, perform controlled airflow tests, and compare with baseline data."
        ),
        entity_scope="Engine Air Intake System",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SAE and ISO Air Filter Testing Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Crankshaft Position Sensor Fault Analysis",
        keywords=[
            "crankshaft position sensor", "sensor fault",
            "signal integrity", "engine timing", "sensor wiring",
            "ECU input", "diagnostic trouble codes", "engine misfire",
            "sensor replacement", "signal noise"
        ],
        conclusion_template=(
            "Crankshaft position sensor fault analysis indicates sensor status is {status} "
            "with signal integrity {signal_status}."
        ),
        reasoning_framework=(
            "The crankshaft position sensor provides critical timing information to the ECU for fuel injection "
            "and ignition control. Faults manifest as signal loss, noise, or incorrect timing data. Diagnostics "
            "include signal waveform analysis, wiring continuity checks, and DTC retrieval. Sensor faults cause "
            "engine misfires, stalling, or failure to start. Replacement or repair is guided by diagnostic results."
        ),
        key_factors=[
            "Signal waveform quality",
            "Wiring harness condition",
            "Diagnostic trouble codes",
            "Engine performance symptoms",
            "Sensor mounting and alignment"
        ],
        primary_authority=[
            "SAE J1939 - Sensor Diagnostics",
            "ISO 14229 - Diagnostic Communication",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Engine Electrical Technician",
        adversary_position=(
            "Intermittent sensor signals are due to engine vibrations, not sensor faults."
        ),
        counter_arguments=[
            "Mechanical vibrations can affect sensor signal stability.",
            "Connector corrosion may cause intermittent faults."
        ],
        resolution_strategy=(
            "Perform signal capture with oscilloscope, inspect wiring and connectors, and replace sensor if needed."
        ),
        entity_scope="Engine Sensor System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE Sensor Fault Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Pump Pressure Regulation and Leakage Detection",
        keywords=[
            "fuel pump", "pressure regulation",
            "leakage detection", "pressure relief valve",
            "fuel delivery rate", "pump wear", "pressure sensor",
            "fuel system integrity", "engine performance", "diagnostics"
        ],
        conclusion_template=(
            "Fuel pump pressure regulation is {status} with leakage levels {leakage_status} "
            "affecting fuel system integrity."
        ),
        reasoning_framework=(
            "The fuel pump maintains required pressure for injection. Pressure regulation is achieved via relief valves "
            "and pump control mechanisms. Leakage reduces pressure and fuel delivery efficiency. Diagnostics involve "
            "pressure sensor data analysis, flow rate measurements, and inspection for external or internal leaks. "
            "Pump wear affects pressure stability and leakage rates. Maintaining fuel system integrity ensures engine "
            "performance and emissions compliance."
        ),
        key_factors=[
            "Fuel pump outlet pressure",
            "Pressure relief valve operation",
            "Leakage detection (internal/external)",
            "Fuel delivery rate consistency",
            "Pump wear indicators"
        ],
        primary_authority=[
            "Bosch Fuel Pump Technical Manual",
            "SAE J2716 - Fuel System Diagnostics",
            "ISO 20896-1:2019 - Fuel Injection Equipment"
        ],
        burden_holder="Fuel System Maintenance Engineer",
        adversary_position=(
            "Pressure fluctuations are due to transient engine load changes, not pump faults."
        ),
        counter_arguments=[
            "Rapid load changes cause temporary pressure variations.",
            "Sensor inaccuracies can mimic pressure instability."
        ],
        resolution_strategy=(
            "Perform static pressure tests, inspect pump components, and verify sensor calibration."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Bosch Fuel Pump Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Valve Lash Adjustment and Wear Analysis",
        keywords=[
            "valve lash", "valve clearance",
            "wear analysis", "camshaft", "valve train",
            "engine noise", "performance", "adjustment procedure",
            "thermal expansion", "maintenance"
        ],
        conclusion_template=(
            "Valve lash measurements indicate adjustment is {adjustment_status} with wear levels "
            "{wear_status} affecting valve train performance."
        ),
        reasoning_framework=(
            "Valve lash is the clearance between valve components allowing thermal expansion without valve damage. "
            "Incorrect lash causes noise, performance loss, and accelerated wear. Measurements are taken at specified "
            "temperatures, and adjustments are made to manufacturer specifications. Wear analysis includes inspecting "
            "cam lobes, rocker arms, and valve stems. Proper lash ensures optimal valve timing and engine efficiency."
        ),
        key_factors=[
            "Valve clearance measurements",
            "Camshaft lobe wear",
            "Rocker arm condition",
            "Thermal expansion compensation",
            "Engine noise and performance indicators"
        ],
        primary_authority=[
            "Engine Manufacturer Maintenance Manual",
            "SAE J1349 - Engine Valve Train Diagnostics",
            "ISO 8178 - Engine Emission Measurement"
        ],
        burden_holder="Engine Maintenance Technician",
        adversary_position=(
            "Valve lash variations are within acceptable limits and do not require adjustment."
        ),
        counter_arguments=[
            "Normal wear causes minor lash changes.",
            "Measurement errors due to temperature variations."
        ],
        resolution_strategy=(
            "Perform measurements at specified temperatures, adjust lash as needed, and monitor engine performance."
        ),
        entity_scope="Valve Train System",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Engine Manufacturer Valve Lash Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Turbocharger Wastegate Actuator Diagnostics",
        keywords=[
            "turbocharger", "wastegate actuator",
            "diagnostics", "actuator response",
            "boost pressure control", "electronic actuator",
            "vacuum actuator", "fault codes", "engine performance",
            "maintenance"
        ],
        conclusion_template=(
            "Wastegate actuator diagnostics indicate actuator is {status} with response "
            "times {response_status} affecting boost control."
        ),
        reasoning_framework=(
            "The wastegate actuator controls exhaust flow to the turbocharger turbine, regulating boost pressure. "
            "Diagnostics include actuator response time measurement, position sensor feedback, and fault code analysis. "
            "Actuator types include electronic and vacuum-operated. Faults cause boost pressure deviations, affecting "
            "engine performance and emissions. Testing involves command signal verification and mechanical inspection."
        ),
        key_factors=[
            "Actuator response time",
            "Position sensor accuracy",
            "Boost pressure correlation",
            "Fault code presence",
            "Mechanical linkage condition"
        ],
        primary_authority=[
            "Garrett Turbocharger Technical Manual",
            "SAE J1939 - Wastegate Actuator Diagnostics",
            "Engine Manufacturer Service Guidelines"
        ],
        burden_holder="Turbocharger Service Technician",
        adversary_position=(
            "Boost pressure variations are due to engine load changes, not actuator faults."
        ),
        counter_arguments=[
            "Transient engine conditions affect boost pressure.",
            "Sensor inaccuracies may cause false fault indications."
        ],
        resolution_strategy=(
            "Perform actuator bench testing, verify sensor signals, and cross-check boost pressure data."
        ),
        entity_scope="Turbocharger System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Garrett Wastegate Actuator Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Exhaust Backpressure Monitoring and Diagnostics",
        keywords=[
            "exhaust backpressure", "monitoring",
            "diagnostics", "DPF restriction",
            "EGR system", "turbocharger performance",
            "pressure sensors", "engine load",
            "emissions", "fault detection"
        ],
        conclusion_template=(
            "Exhaust backpressure levels are {pressure_status} indicating system "
            "{system_status} under current operating conditions."
        ),
        reasoning_framework=(
            "Exhaust backpressure affects engine breathing and performance. Elevated backpressure may indicate "
            "DPF restriction, EGR system faults, or turbocharger issues. Monitoring involves pressure sensor data "
            "analysis, correlation with engine load and RPM, and fault code evaluation. Accurate backpressure "
            "diagnostics enable timely maintenance and prevent engine damage."
        ),
        key_factors=[
            "Exhaust pressure sensor readings",
            "Engine load and RPM correlation",
            "DPF condition",
            "EGR valve operation",
            "Turbocharger performance"
        ],
        primary_authority=[
            "SAE J2711 - Exhaust System Diagnostics",
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "Engine Manufacturer Diagnostic Guidelines"
        ],
        burden_holder="Emission Control Technician",
        adversary_position=(
            "Backpressure variations are normal transient phenomena, not indicative of faults."
        ),
        counter_arguments=[
            "Transient load changes affect backpressure.",
            "Sensor errors can cause false readings."
        ],
        resolution_strategy=(
            "Perform steady-state tests, sensor calibration, and physical inspection of exhaust components."
        ),
        entity_scope="Exhaust System",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE Exhaust System Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Heater Operation and Diagnostics",
        keywords=[
            "fuel heater", "operation",
            "diagnostics", "cold start",
            "fuel viscosity", "heater element",
            "temperature control", "electrical supply",
            "fuel flow", "maintenance"
        ],
        conclusion_template=(
            "Fuel heater operation is {status} with temperature control and electrical "
            "supply {supply_status} ensuring proper fuel viscosity."
        ),
        reasoning_framework=(
            "Fuel heaters reduce fuel viscosity during cold starts to improve atomization and combustion. "
            "Diagnostics include verifying heater element resistance, electrical supply voltage, temperature "
            "sensor feedback, and fuel temperature rise. Faults cause poor cold start performance and increased "
            "emissions. Testing involves electrical continuity checks and temperature monitoring."
        ),
        key_factors=[
            "Heater element resistance",
            "Electrical supply voltage",
            "Fuel temperature before and after heater",
            "Temperature sensor accuracy",
            "Cold start engine performance"
        ],
        primary_authority=[
            "Engine Manufacturer Fuel System Manual",
            "SAE J1939 - Fuel Heater Diagnostics",
            "ISO 8178 - Engine Emission Measurement"
        ],
        burden_holder="Fuel System Technician",
        adversary_position=(
            "Cold start issues are due to battery condition, not fuel heater faults."
        ),
        counter_arguments=[
            "Battery voltage affects heater operation.",
            "Fuel system airlocks can cause start problems."
        ],
        resolution_strategy=(
            "Perform electrical tests, verify fuel temperature rise, and inspect fuel system."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Engine Manufacturer Fuel Heater Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Camshaft Position Sensor Signal Integrity",
        keywords=[
            "camshaft position sensor", "signal integrity",
            "waveform analysis", "engine timing",
            "sensor wiring", "ECU input",
            "diagnostic trouble codes", "sensor replacement",
            "signal noise", "engine performance"
        ],
        conclusion_template=(
            "Camshaft position sensor signal integrity is {status} with waveform "
            "quality {quality_status} supporting engine timing accuracy."
        ),
        reasoning_framework=(
            "The camshaft position sensor provides critical timing data for fuel injection and valve timing. "
            "Signal integrity is assessed via waveform analysis, wiring inspections, and fault code retrieval. "
            "Signal noise or loss affects engine timing, causing misfires or performance issues. Diagnostics "
            "include oscilloscope waveform capture and connector checks."
        ),
        key_factors=[
            "Waveform shape and amplitude",
            "Wiring harness condition",
            "Diagnostic trouble codes",
            "Engine performance symptoms",
            "Sensor mounting and alignment"
        ],
        primary_authority=[
            "SAE J1939 - Sensor Diagnostics",
            "ISO 14229 - Diagnostic Communication",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Engine Electrical Technician",
        adversary_position=(
            "Signal variations are due to engine vibrations, not sensor faults."
        ),
        counter_arguments=[
            "Mechanical vibrations can affect sensor signals.",
            "Connector corrosion may cause intermittent faults."
        ],
        resolution_strategy=(
            "Perform signal capture, wiring inspection, and sensor replacement if necessary."
        ),
        entity_scope="Engine Sensor System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE Sensor Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Tank Ventilation and Vapor Management",
        keywords=[
            "fuel tank ventilation", "vapor management",
            "pressure relief", "fuel evaporation",
            "vent valve", "emission control",
            "tank pressure sensors", "fuel system integrity",
            "maintenance", "diagnostics"
        ],
        conclusion_template=(
            "Fuel tank ventilation system is {status} with vapor pressure levels "
            "{pressure_status} ensuring emission control compliance."
        ),
        reasoning_framework=(
            "Fuel tank ventilation manages vapor pressure and prevents vapor lock or excessive emissions. "
            "Vent valves regulate pressure and allow air exchange. Diagnostics include pressure sensor data, "
            "vent valve operation checks, and vapor emission measurements. Faults cause pressure buildup, "
            "fuel delivery issues, or increased evaporative emissions."
        ),
        key_factors=[
            "Tank vapor pressure",
            "Vent valve operation",
            "Emission levels",
            "Sensor accuracy",
            "Fuel system integrity"
        ],
        primary_authority=[
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "SAE J2260 - Fuel System Diagnostics",
            "Engine Manufacturer Fuel System Guidelines"
        ],
        burden_holder="Emission Control Technician",
        adversary_position=(
            "Pressure variations are due to ambient temperature changes, not system faults."
        ),
        counter_arguments=[
            "Temperature affects vapor pressure.",
            "Sensor placement influences readings."
        ],
        resolution_strategy=(
            "Perform controlled pressure tests, inspect vent valves, and verify sensor calibration."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="EPA and SAE Fuel System Ventilation Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Intake Manifold Pressure Sensor Calibration and Fault Detection",
        keywords=[
            "intake manifold pressure sensor", "calibration",
            "fault detection", "sensor drift",
            "engine load estimation", "ECU input",
            "diagnostic trouble codes", "sensor replacement",
            "signal noise", "engine performance"
        ],
        conclusion_template=(
            "Intake manifold pressure sensor calibration is {status} with fault detection "
            "indicating sensor condition is {condition}."
        ),
        reasoning_framework=(
            "The intake manifold pressure sensor provides critical data for engine load estimation and fuel injection control. "
            "Calibration ensures sensor accuracy. Fault detection includes monitoring sensor output range, drift, and fault codes. "
            "Sensor faults cause incorrect load estimation, affecting engine performance and emissions. Diagnostics involve sensor "
            "signal analysis and cross-checking with other sensors."
        ),
        key_factors=[
            "Sensor output voltage or frequency",
            "Calibration status",
            "Diagnostic trouble codes",
            "Signal noise and stability",
            "Engine performance correlation"
        ],
        primary_authority=[
            "SAE J1939 - Sensor Diagnostics",
            "ISO 14229 - Diagnostic Communication",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Engine Control Technician",
        adversary_position=(
            "Sensor output variations are due to normal engine operation, not sensor faults."
        ),
        counter_arguments=[
            "Transient engine conditions affect sensor readings.",
            "Electrical interference may cause signal noise."
        ],
        resolution_strategy=(
            "Perform sensor calibration, signal filtering, and cross-sensor validation."
        ),
        entity_scope="Engine Sensor System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE and ISO Sensor Diagnostic Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Pressure Sensor Fault Analysis",
        keywords=[
            "fuel pressure sensor", "fault analysis",
            "sensor calibration", "signal integrity",
            "fuel system diagnostics", "ECU input",
            "diagnostic trouble codes", "sensor replacement",
            "signal noise", "engine performance"
        ],
        conclusion_template=(
            "Fuel pressure sensor fault analysis indicates sensor status is {status} "
            "with calibration and signal integrity {integrity_status}."
        ),
        reasoning_framework=(
            "Fuel pressure sensors monitor pressure in the fuel rail or pump output. Faults affect fuel delivery control. "
            "Diagnostics include sensor calibration checks, signal waveform analysis, and fault code retrieval. Sensor faults "
            "cause fuel pressure anomalies, affecting engine performance and emissions."
        ),
        key_factors=[
            "Sensor calibration accuracy",
            "Signal waveform quality",
            "Diagnostic trouble codes",
            "Engine performance symptoms",
            "Sensor wiring and connectors"
        ],
        primary_authority=[
            "Bosch Fuel System Diagnostics Manual",
            "SAE J1939 - Sensor Diagnostics",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Fuel System Technician",
        adversary_position=(
            "Sensor anomalies are due to transient fuel system conditions, not sensor faults."
        ),
        counter_arguments=[
            "Rapid fuel pressure changes affect sensor readings.",
            "Connector corrosion may cause intermittent faults."
        ],
        resolution_strategy=(
            "Perform sensor calibration, wiring inspection, and replacement if necessary."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Bosch Fuel Pressure Sensor Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Starter Motor Performance and Diagnostics",
        keywords=[
            "starter motor", "performance",
            "diagnostics", "cranking speed",
            "battery voltage", "starter relay",
            "engine start", "electrical load",
            "fault codes", "maintenance"
        ],
        conclusion_template=(
            "Starter motor performance is {status} with cranking speed and electrical "
            "parameters {parameter_status}."
        ),
        reasoning_framework=(
            "The starter motor initiates engine cranking. Performance diagnostics include measuring cranking speed, "
            "battery voltage during cranking, relay operation, and electrical load. Faults cause slow cranking or failure "
            "to start. Testing involves voltage drop measurements, relay function tests, and starter motor bench testing."
        ),
        key_factors=[
            "Cranking speed (RPM)",
            "Battery voltage during cranking",
            "Starter relay operation",
            "Electrical load during start",
            "Diagnostic trouble codes"
        ],
        primary_authority=[
            "SAE J1939 - Starter System Diagnostics",
            "Battery Council International Standards",
            "Engine Manufacturer Maintenance Guidelines"
        ],
        burden_holder="Electrical Systems Technician",
        adversary_position=(
            "Slow cranking is due to battery condition, not starter motor faults."
        ),
        counter_arguments=[
            "Battery state of charge affects cranking speed.",
            "Electrical connections can cause voltage drops."
        ],
        resolution_strategy=(
            "Perform battery load test, inspect wiring, and bench test starter motor."
        ),
        entity_scope="Engine Electrical System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE Starter System Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Exhaust Gas Recirculation Valve Sticking and Cleaning",
        keywords=[
            "EGR valve", "sticking",
            "cleaning", "carbon deposits",
            "valve operation", "emission control",
            "diagnostics", "engine performance",
            "maintenance", "fault codes"
        ],
        conclusion_template=(
            "EGR valve is {status} with sticking levels {sticking_level} and cleaning "
            "procedures {cleaning_status} effectiveness."
        ),
        reasoning_framework=(
            "EGR valves can stick due to carbon deposits, impairing valve operation and emission control. "
            "Diagnostics include valve position feedback, fault codes, and engine performance symptoms. "
            "Cleaning involves chemical or mechanical removal of deposits. Effectiveness is measured by restored "
            "valve movement and emission improvements."
        ),
        key_factors=[
            "Valve position sensor feedback",
            "Carbon deposit thickness",
            "Fault code presence",
            "Engine performance metrics",
            "Cleaning method applied"
        ],
        primary_authority=[
            "Cummins EGR System Service Manual",
            "SAE J2711 - EGR System Diagnostics",
            "Engine Manufacturer Maintenance Guidelines"
        ],
        burden_holder="Emission Control Technician",
        adversary_position=(
            "Valve operation issues are due to sensor faults, not sticking."
        ),
        counter_arguments=[
            "Sensor faults can mimic valve sticking symptoms.",
            "Intermittent sticking may be hard to detect."
        ],
        resolution_strategy=(
            "Perform valve cleaning, sensor diagnostics, and monitor engine performance."
        ),
        entity_scope="Exhaust Gas Recirculation System",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Cummins EGR Valve Maintenance Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Oil Pressure Sensor Calibration and Fault Detection",
        keywords=[
            "oil pressure sensor", "calibration",
            "fault detection", "signal integrity",
            "engine lubrication", "diagnostic trouble codes",
            "sensor replacement", "signal noise",
            "engine performance", "maintenance"
        ],
        conclusion_template=(
            "Oil pressure sensor calibration is {status} with fault detection indicating "
            "sensor condition is {condition}."
        ),
        reasoning_framework=(
            "Oil pressure sensors monitor lubrication system pressure critical for engine health. "
            "Calibration ensures accurate readings. Fault detection includes monitoring sensor output "
            "range, drift, and fault codes. Sensor faults cause false low or high pressure indications, "
            "affecting engine protection systems."
        ),
        key_factors=[
            "Sensor output voltage or frequency",
            "Calibration status",
            "Diagnostic trouble codes",
            "Signal noise and stability",
            "Engine performance correlation"
        ],
        primary_authority=[
            "SAE J1939 - Sensor Diagnostics",
            "ISO 14229 - Diagnostic Communication",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Engine Maintenance Technician",
        adversary_position=(
            "Sensor output variations are due to normal engine operation, not sensor faults."
        ),
        counter_arguments=[
            "Transient engine conditions affect sensor readings.",
            "Electrical interference may cause signal noise."
        ],
        resolution_strategy=(
            "Perform sensor calibration, signal filtering, and cross-sensor validation."
        ),
        entity_scope="Engine Sensor System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE and ISO Sensor Diagnostic Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Cooling Fan Operation and Control Diagnostics",
        keywords=[
            "cooling fan", "operation",
            "control diagnostics", "fan clutch",
            "temperature sensors", "engine cooling",
            "electrical control", "fan speed",
            "fault codes", "maintenance"
        ],
        conclusion_template=(
            "Cooling fan operation and control diagnostics indicate system is {status} "
            "with fan speed and temperature control {control_status}."
        ),
        reasoning_framework=(
            "Cooling fans regulate engine temperature by increasing airflow through the radiator. "
            "Diagnostics include fan clutch operation, electrical control signals, temperature sensor "
            "feedback, and fault code analysis. Fan speed is correlated with engine temperature to "
            "ensure proper cooling. Faults cause overheating or excessive power consumption."
        ),
        key_factors=[
            "Fan clutch engagement",
            "Electrical control signals",
            "Radiator inlet and outlet temperatures",
            "Fan speed measurements",
            "Diagnostic trouble codes"
        ],
        primary_authority=[
            "SAE J1939 - Cooling System Diagnostics",
            "Engine Manufacturer Maintenance Guidelines",
            "ISO 13709 - Pumps and Fans"
        ],
        burden_holder="Cooling System Technician",
        adversary_position=(
            "Fan speed variations are due to ambient temperature changes, not system faults."
        ),
        counter_arguments=[
            "Environmental conditions affect cooling requirements.",
            "Sensor inaccuracies may cause false readings."
        ],
        resolution_strategy=(
            "Perform electrical tests, fan clutch inspection, and temperature sensor calibration."
        ),
        entity_scope="Engine Cooling System",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE Cooling System Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Battery State of Charge and Health Monitoring",
        keywords=[
            "battery", "state of charge",
            "health monitoring", "capacity test",
            "conductance", "voltage measurement",
            "engine starting", "electrical load",
            "maintenance", "diagnostics"
        ],
        conclusion_template=(
            "Battery state of charge and health are {status} with capacity and conductance "
            "tests indicating {health_status}."
        ),
        reasoning_framework=(
            "Battery health affects engine starting and electrical system stability. Diagnostics include "
            "state of charge measurement, capacity testing, conductance analysis, and voltage monitoring. "
            "Degraded batteries cause starting issues and electrical faults. Regular monitoring enables "
            "timely replacement and maintenance."
        ),
        key_factors=[
            "State of charge percentage",
            "Capacity test results",
            "Conductance values",
            "Voltage under load",
            "Battery age and usage history"
        ],
        primary_authority=[
            "Battery Council International Standards",
            "SAE J1939 - Battery Diagnostics",
            "Engine Manufacturer Maintenance Guidelines"
        ],
        burden_holder="Electrical Systems Technician",
        adversary_position=(
            "Battery voltage fluctuations are due to load variations, not battery health."
        ),
        counter_arguments=[
            "High electrical loads cause temporary voltage drops.",
            "Battery aging affects voltage stability."
        ],
        resolution_strategy=(
            "Perform load tests, conductance measurements, and monitor battery usage history."
        ),
        entity_scope="Engine Electrical System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Battery Council International Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Filter Condition and Water Separation Diagnostics",
        keywords=[
            "fuel filter", "condition",
            "water separation", "filter clogging",
            "pressure differential", "water sensor",
            "fuel contamination", "maintenance",
            "diagnostics", "engine performance"
        ],
        conclusion_template=(
            "Fuel filter condition is {condition} with water separation and clogging levels "
            "{clogging_status} affecting fuel system performance."
        ),
        reasoning_framework=(
            "Fuel filters remove particulates and separate water to protect the fuel system. Diagnostics include "
            "pressure differential measurement across the filter, water sensor status, and fuel contamination analysis. "
            "Clogged filters reduce fuel flow causing engine performance issues. Water accumulation promotes corrosion "
            "and microbial growth."
        ),
        key_factors=[
            "Pressure differential across filter",
            "Water sensor activation",
            "Filter particulate loading",
            "Fuel contamination levels",
            "Engine performance symptoms"
        ],
        primary_authority=[
            "SAE J726 - Fuel Filter Testing",
            "ISO 4406 - Contamination Control",
            "Engine Manufacturer Maintenance Guidelines"
        ],
        burden_holder="Fuel System Maintenance Technician",
        adversary_position=(
            "Pressure drops are due to fuel temperature changes, not filter clogging."
        ),
        counter_arguments=[
            "Temperature affects fuel viscosity and pressure readings.",
            "Sensor inaccuracies may cause false water detection."
        ],
        resolution_strategy=(
            "Perform filter inspection, sensor calibration, and fuel contamination analysis."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="SAE and ISO Fuel Filter Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Exhaust Temperature Sensor Placement and Accuracy",
        keywords=[
            "exhaust temperature sensor", "placement",
            "accuracy", "sensor calibration",
            "thermal gradients", "engine emissions",
            "diagnostics", "sensor drift",
            "maintenance", "engine protection"
        ],
        conclusion_template=(
            "Exhaust temperature sensor placement and accuracy are {status} ensuring "
            "reliable temperature measurement for emission control."
        ),
        reasoning_framework=(
            "Proper sensor placement minimizes thermal gradients and ensures accurate temperature readings critical "
            "for emission control and engine protection. Calibration verifies sensor accuracy. Diagnostics include "
            "temperature profile analysis, sensor drift detection, and fault code retrieval."
        ),
        key_factors=[
            "Sensor mounting location",
            "Calibration status",
            "Temperature profile consistency",
            "Sensor drift over time",
            "Fault code presence"
        ],
        primary_authority=[
            "SAE J1939 - Sensor Placement Guidelines",
            "ISO 27145 - Sensor Calibration",
            "Engine Manufacturer Sensor Installation Standards"
        ],
        burden_holder="Engine Sensor Technician",
        adversary_position=(
            "Temperature measurement variations are due to engine operation, not sensor placement."
        ),
        counter_arguments=[
            "Engine thermal dynamics cause temperature fluctuations.",
            "Sensor aging affects accuracy."
        ],
        resolution_strategy=(
            "Verify sensor installation, perform calibration, and monitor temperature profiles."
        ),
        entity_scope="Engine Sensor System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE and ISO Sensor Installation Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Rail Pressure Sensor Calibration and Diagnostics",
        keywords=[
            "fuel rail pressure sensor", "calibration",
            "diagnostics", "signal integrity",
            "fuel system control", "fault codes",
            "sensor replacement", "signal noise",
            "engine performance", "maintenance"
        ],
        conclusion_template=(
            "Fuel rail pressure sensor calibration and diagnostics indicate sensor status "
            "is {status} with signal integrity {integrity_status}."
        ),
        reasoning_framework=(
            "Fuel rail pressure sensors provide critical data for fuel injection control. Calibration ensures accuracy. "
            "Diagnostics include signal waveform analysis, fault code retrieval, and sensor replacement decisions. "
            "Sensor faults cause fuel pressure anomalies affecting engine performance."
        ),
        key_factors=[
            "Sensor calibration accuracy",
            "Signal waveform quality",
            "Diagnostic trouble codes",
            "Engine performance symptoms",
            "Sensor wiring and connectors"
        ],
        primary_authority=[
            "Bosch Fuel System Diagnostics Manual",
            "SAE J1939 - Sensor Diagnostics",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Fuel System Technician",
        adversary_position=(
            "Sensor anomalies are due to transient fuel system conditions, not sensor faults."
        ),
        counter_arguments=[
            "Rapid fuel pressure changes affect sensor readings.",
            "Connector corrosion may cause intermittent faults."
        ],
        resolution_strategy=(
            "Perform sensor calibration, wiring inspection, and replacement if necessary."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Bosch Fuel Rail Pressure Sensor Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Crankcase Pressure Sensor Diagnostics",
        keywords=[
            "crankcase pressure sensor", "diagnostics",
            "blowby measurement", "sensor calibration",
            "engine wear", "signal integrity",
            "fault codes", "maintenance",
            "engine emissions", "sensor replacement"
        ],
        conclusion_template=(
            "Crankcase pressure sensor diagnostics indicate sensor status is {status} "
            "with blowby measurement accuracy {accuracy_status}."
        ),
        reasoning_framework=(
            "Crankcase pressure sensors measure blowby gases indicating engine wear. Calibration ensures accuracy. "
            "Diagnostics include signal integrity checks, fault code analysis, and sensor replacement decisions. "
            "Accurate blowby measurement supports maintenance planning and emission control."
        ),
        key_factors=[
            "Sensor calibration status",
            "Signal waveform quality",
            "Diagnostic trouble codes",
            "Blowby measurement accuracy",
            "Engine wear indicators"
        ],
        primary_authority=[
            "SAE J1667 - Crankcase Emission Control",
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "Engine Manufacturer Sensor Guidelines"
        ],
        burden_holder="Engine Emission Compliance Officer",
        adversary_position=(
            "Sensor anomalies are due to transient engine conditions, not sensor faults."
        ),
        counter_arguments=[
            "Engine operating conditions affect sensor readings.",
            "Electrical interference may cause signal noise."
        ],
        resolution_strategy=(
            "Perform sensor calibration, signal filtering, and cross-sensor validation."
        ),
        entity_scope="Crankcase Ventilation System",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="SAE and EPA Crankcase Pressure Sensor Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Injector Control Module Diagnostics",
        keywords=[
            "fuel injector control module", "diagnostics",
            "ECU communication", "signal integrity",
            "fault codes", "injector timing",
            "control signals", "engine performance",
            "maintenance", "software updates"
        ],
        conclusion_template=(
            "Fuel injector control module diagnostics indicate module status is {status} "
            "with communication and control signal integrity {integrity_status}."
        ),
        reasoning_framework=(
            "The injector control module manages injector timing and pulse width. Diagnostics include ECU communication checks, "
            "signal integrity analysis, fault code retrieval, and software update verification. Faults cause injector misfires "
            "and engine performance issues."
        ),
        key_factors=[
            "ECU communication status",
            "Control signal waveform quality",
            "Diagnostic trouble codes",
            "Injector timing accuracy",
            "Software version and updates"
        ],
        primary_authority=[
            "Engine Manufacturer ECU Diagnostics Manual",
            "SAE J1939 - ECU Communication",
            "ISO 14229 - Diagnostic Communication"
        ],
        burden_holder="Engine Control Technician",
        adversary_position=(
            "Injector performance issues are due to mechanical faults, not control module errors."
        ),
        counter_arguments=[
            "Mechanical injector faults can mimic control module issues.",
            "Communication errors may be transient."
        ],
        resolution_strategy=(
            "Perform ECU communication tests, update software, and cross-check injector diagnostics."
        ),
        entity_scope="Fuel Injection Control System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="Engine Manufacturer ECU Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Exhaust Aftertreatment Temperature Management",
        keywords=[
            "exhaust aftertreatment", "temperature management",
            "DPF regeneration", "SCR catalyst",
            "temperature sensors", "thermal gradients",
            "emission control", "diagnostics",
            "fault codes", "maintenance"
        ],
        conclusion_template=(
            "Exhaust aftertreatment temperature management is {status} with sensor readings "
            "and thermal profiles {profile_status}."
        ),
        reasoning_framework=(
            "Temperature management in aftertreatment systems ensures effective DPF regeneration and SCR catalyst function. "
            "Diagnostics include temperature sensor data analysis, thermal gradient assessment, and fault code retrieval. "
            "Proper temperature profiles prevent catalyst damage and ensure emission compliance."
        ),
        key_factors=[
            "Temperature sensor accuracy",
            "Thermal gradient consistency",
            "DPF regeneration temperature thresholds",
            "SCR catalyst operating temperature",
            "Diagnostic trouble codes"
        ],
        primary_authority=[
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "SAE J2711 - Aftertreatment System Diagnostics",
            "Engine Manufacturer Maintenance Guidelines"
        ],
        burden_holder="Emission Control Technician",
        adversary_position=(
            "Temperature variations are due to engine load changes, not system faults."
        ),
        counter_arguments=[
            "Transient engine conditions affect temperature readings.",
            "Sensor drift may cause false indications."
        ],
        resolution_strategy=(
            "Perform sensor calibration, thermal imaging, and controlled regeneration tests."
        ),
        entity_scope="Exhaust Aftertreatment System",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EPA and SAE Aftertreatment Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel System Leak Detection and Diagnostics",
        keywords=[
            "fuel system", "leak detection",
            "pressure testing", "sensor data",
            "fuel loss", "emission control",
            "maintenance", "diagnostics",
            "fault codes", "safety"
        ],
        conclusion_template=(
            "Fuel system leak detection diagnostics indicate leak presence is {presence} "
            "with pressure test results {test_status}."
        ),
        reasoning_framework=(
            "Fuel system leaks cause fuel loss, emission increases, and safety hazards. Diagnostics include pressure testing, "
            "sensor data analysis, and fault code retrieval. Leak detection involves static and dynamic pressure tests and "
            "visual inspections. Timely detection prevents environmental and operational risks."
        ),
        key_factors=[
            "Pressure test results",
            "Sensor data anomalies",
            "Fuel consumption discrepancies",
            "Visual leak inspection",
            "Diagnostic trouble codes"
        ],
        primary_authority=[
            "EPA 40 CFR Part 1065 - Emission Measurement",
            "SAE J2716 - Fuel System Diagnostics",
            "Engine Manufacturer Maintenance Guidelines"
        ],
        burden_holder="Fuel System Maintenance Engineer",
        adversary_position=(
            "Pressure variations are due to normal operation, not leaks."
        ),
        counter_arguments=[
            "Transient pressure changes occur during engine operation.",
            "Sensor errors may cause false leak indications."
        ],
        resolution_strategy=(
            "Perform controlled pressure tests, sensor calibration, and visual inspections."
        ),
        entity_scope="Fuel Supply System",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="EPA and SAE Fuel System Leak Detection Standards"
    ),
    DoctrineBlock(
        topic="Diesel Engine Exhaust Gas Temperature Sensor Failure Modes",
        keywords=[
            "exhaust gas temperature sensor", "failure modes",
            "signal loss", "sensor drift",
            "thermal shock", "wiring faults",
            "diagnostics", "fault codes",
            "engine protection", "maintenance"
        ],
        conclusion_template=(
            "Exhaust gas temperature sensor failure mode analysis indicates failure type "
            "is {failure_type} with diagnostic confidence {confidence_level}."
        ),
        reasoning_framework=(
            "EGT sensor failures include signal loss, drift, thermal shock damage, and wiring faults. Diagnostics involve "
            "signal analysis, fault code retrieval, and sensor inspection. Identifying failure modes supports targeted maintenance "
            "and prevents engine damage."
        ),
        key_factors=[
            "Signal continuity",
            "Calibration drift",
            "Thermal damage evidence",
            "Wiring and connector condition",
            "Diagnostic trouble codes"
        ],
        primary_authority=[
            "SAE J1939 - Sensor Failure Diagnostics",
            "ISO 14229 - Diagnostic Communication",
            "Engine Manufacturer Sensor Maintenance Guidelines"
        ],
        burden_holder="Engine Maintenance Technician",
        adversary_position=(
            "Sensor anomalies are due to transient engine conditions, not sensor failures."
        ),
        counter_arguments=[
            "Engine thermal dynamics cause temporary sensor issues.",
            "Connector corrosion may cause intermittent faults."
        ],
        resolution_strategy=(
            "Perform sensor inspection, wiring checks, and replacement if necessary."
        ),
        entity_scope="Engine Sensor System",
        confidence=0.9,
        confidence_zone="High",
        controlling_precedent="SAE and ISO Sensor Failure Diagnostic Procedures"
    ),
    DoctrineBlock(
        topic="Diesel Engine Fuel Injector Electrical Connector Diagnostics",
        keywords=[
            "fuel injector", "electrical connector",
            "diagnostics", "signal integrity",
            "wiring harness", "connector corrosion",
            "fault codes", "engine performance",
            "maintenance", "repair procedures"
        ],
        conclusion_template=(
            "Fuel injector electrical connector diagnostics indicate connector status is {status} "
            "with signal integrity {integrity_status}."
        ),
        reasoning_framework=(
            "Electrical connectors provide signal and power to fuel injectors. Diagnostics include visual inspection, "
            "signal integrity testing, and fault code retrieval. Connector corrosion or wiring damage causes injector "
            "malfunction and engine performance issues. Repair involves cleaning, replacement, and wiring