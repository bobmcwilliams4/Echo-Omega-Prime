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
        topic="Refrigeration Cycle Fundamentals",
        keywords=["refrigeration cycle", "thermodynamics", "phase change", "latent heat", "pressure-temperature relationship"],
        conclusion_template="The automotive HVAC system operates on the principle of the vapor-compression refrigeration cycle, utilizing phase changes of refrigerant to transfer heat from the cabin to the external environment.",
        reasoning_framework=(
            "1. The refrigeration cycle consists of four main components: compressor, condenser, expansion device, and evaporator.\n"
            "2. Refrigerant absorbs heat in the evaporator (low pressure, low temperature) and releases it in the condenser (high pressure, high temperature).\n"
            "3. The compressor increases refrigerant pressure and temperature, enabling heat rejection in the condenser.\n"
            "4. The expansion device creates a pressure drop, allowing refrigerant to vaporize in the evaporator and absorb cabin heat.\n"
            "5. The cycle relies on the refrigerant's latent heat of vaporization and condensation.\n"
            "6. System performance depends on proper charge, component function, and absence of non-condensables.\n"
            "7. The pressure-temperature relationship of the refrigerant is foundational to diagnosis and operation.\n"
            "8. Any deviation from expected pressures or temperatures indicates a system fault.\n"
            "9. The cycle is closed, with refrigerant recirculating unless a leak occurs.\n"
            "10. Environmental and regulatory considerations mandate use of approved refrigerants and recovery procedures."
        ),
        key_factors=[
            "Component integrity",
            "Refrigerant type and charge",
            "Pressure-temperature relationship",
            "Phase change efficiency",
            "Thermal load"
        ],
        primary_authority=[
            "SAE J639",
            "ASHRAE Fundamentals Handbook",
            "EPA 609 Certification Guidelines"
        ],
        burden_holder="HVAC system designer/technician",
        adversary_position="Alternative cooling cycles (e.g., absorption, ejector) are more efficient or suitable.",
        counter_arguments=[
            "Vapor-compression cycle remains the industry standard for automotive applications due to efficiency, compactness, and reliability.",
            "Alternative cycles have higher complexity and cost, with limited adoption in automotive HVAC."
        ],
        resolution_strategy="Reference SAE and ASHRAE standards; compare cycle COP and practical implementation in automotive context.",
        entity_scope="Automotive HVAC systems (passenger vehicles, light trucks)",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="Compressor Technology & Diagnosis",
        keywords=["compressor", "swash plate", "scroll", "variable displacement", "diagnosis", "NVH", "lubrication"],
        conclusion_template="Proper compressor selection and diagnosis are critical for efficient HVAC operation, with variable displacement and scroll compressors offering improved control and NVH characteristics.",
        reasoning_framework=(
            "1. Compressor types include fixed displacement (piston, swash plate) and variable displacement (swash plate, scroll).\n"
            "2. Variable displacement compressors adjust output to match cooling demand, improving efficiency and reducing cycling.\n"
            "3. Scroll compressors offer smoother operation and lower noise/vibration.\n"
            "4. Diagnosis involves assessing clutch engagement, pressure readings, noise, and temperature differentials.\n"
            "5. Common faults: clutch failure, internal wear, loss of lubrication, valve plate damage, and contamination.\n"
            "6. Proper oil type and quantity are essential for compressor longevity.\n"
            "7. Use manifold gauges to compare high/low side pressures against specifications.\n"
            "8. NVH (noise, vibration, harshness) complaints may indicate internal damage or mounting issues.\n"
            "9. Replacement requires system flushing and correct oil charge.\n"
            "10. Always verify compressor control signals (electrical or mechanical) in variable systems."
        ),
        key_factors=[
            "Compressor type and control",
            "Lubrication",
            "System cleanliness",
            "Pressure readings",
            "NVH symptoms"
        ],
        primary_authority=[
            "SAE J2064",
            "Automotive Air Conditioning Training Manual",
            "OEM Service Information"
        ],
        burden_holder="Technician/diagnostician",
        adversary_position="All compressors are interchangeable if the mounting and displacement match.",
        counter_arguments=[
            "Compressor type must match system control logic and refrigerant compatibility.",
            "Incorrect compressor selection leads to poor performance and premature failure."
        ],
        resolution_strategy="Reference OEM service procedures and SAE standards; match compressor type to system design.",
        entity_scope="Passenger vehicle HVAC compressors",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="Condenser Design & Airflow",
        keywords=["condenser", "heat rejection", "parallel flow", "microchannel", "airflow", "cooling fan"],
        conclusion_template="Condenser efficiency is maximized by optimal airflow and advanced designs (parallel flow, microchannel), ensuring effective heat rejection and system performance.",
        reasoning_framework=(
            "1. The condenser's role is to reject heat from the refrigerant, condensing it from vapor to liquid.\n"
            "2. Modern condensers use parallel flow or microchannel designs for increased surface area and heat transfer.\n"
            "3. Airflow is critical; obstructions (debris, bent fins) or weak cooling fans reduce efficiency.\n"
            "4. Insufficient heat rejection leads to high head pressures and reduced cooling.\n"
            "5. Fan operation (mechanical, electric, variable speed) must be verified during diagnosis.\n"
            "6. Condenser location (in front of radiator) exposes it to road debris; regular inspection is necessary.\n"
            "7. Replacement condensers must match OE design for refrigerant flow and mounting.\n"
            "8. System retrofits (e.g., R-134a to R-1234yf) may require condenser upgrades for compatibility.\n"
            "9. Airflow testing includes smoke, anemometer, or temperature drop measurement.\n"
            "10. Always check for parallel flow blockages, which are not easily flushed."
        ),
        key_factors=[
            "Airflow rate",
            "Condenser design",
            "Cleanliness",
            "Fan operation",
            "Refrigerant compatibility"
        ],
        primary_authority=[
            "SAE J639",
            "ASHRAE Fundamentals Handbook",
            "OEM Service Manuals"
        ],
        burden_holder="System designer/technician",
        adversary_position="Any condenser with similar size will perform equally.",
        counter_arguments=[
            "Heat transfer efficiency varies with design; microchannel and parallel flow outperform older tube-fin types.",
            "Incorrect condenser selection can lead to high pressures and poor cooling."
        ],
        resolution_strategy="Use manufacturer specifications for condenser selection and verify airflow with diagnostic tools.",
        entity_scope="Automotive HVAC condensers",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="Evaporator Design & Icing Prevention",
        keywords=["evaporator", "icing", "thermal expansion valve", "TXV", "orifice tube", "frost", "airflow"],
        conclusion_template="Evaporator icing is prevented by controlling refrigerant flow, maintaining proper airflow, and ensuring correct thermal load.",
        reasoning_framework=(
            "1. The evaporator absorbs cabin heat, causing refrigerant to vaporize and cool the air.\n"
            "2. Excessive cooling or low airflow can cause surface temperatures to drop below freezing, leading to icing.\n"
            "3. Icing reduces airflow and cooling, potentially damaging the compressor.\n"
            "4. Thermal expansion valves (TXVs) modulate refrigerant flow to prevent icing by maintaining superheat.\n"
            "5. Orifice tube systems rely on accumulator design and cycling switches for icing prevention.\n"
            "6. Blower speed, recirculation mode, and cabin humidity affect icing risk.\n"
            "7. Diagnosis includes checking for restricted airflow (dirty cabin filter, blocked ducts) and proper refrigerant charge.\n"
            "8. Icing may indicate TXV malfunction, low charge, or sensor failure.\n"
            "9. System design must balance cooling capacity with icing risk.\n"
            "10. Modern systems use evaporator temperature sensors to cycle the compressor and prevent icing."
        ),
        key_factors=[
            "Refrigerant flow control",
            "Airflow rate",
            "Thermal load",
            "Humidity",
            "Sensor function"
        ],
        primary_authority=[
            "SAE J2064",
            "Automotive HVAC System Design",
            "OEM Service Manuals"
        ],
        burden_holder="System designer/technician",
        adversary_position="Icing is unavoidable in humid climates.",
        counter_arguments=[
            "Proper system design and control strategies effectively prevent icing in all climates.",
            "Sensor-based cycling and airflow management mitigate icing risk."
        ],
        resolution_strategy="Verify system controls, airflow, and refrigerant charge; reference OEM and SAE guidelines.",
        entity_scope="Automotive HVAC evaporators",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="Expansion Devices - TXV vs. Orifice Tube",
        keywords=["expansion device", "TXV", "orifice tube", "superheat", "refrigerant metering", "system design"],
        conclusion_template="Selection between TXV and orifice tube expansion devices depends on system requirements for control, cost, and performance.",
        reasoning_framework=(
            "1. TXVs (Thermal Expansion Valves) modulate refrigerant flow based on evaporator temperature and pressure, maintaining optimal superheat.\n"
            "2. Orifice tubes provide fixed restriction, relying on accumulator and cycling clutch for control.\n"
            "3. TXV systems offer superior control, efficiency, and adaptability to varying loads.\n"
            "4. Orifice tube systems are simpler, less expensive, and easier to service.\n"
            "5. TXVs are preferred in dual evaporator or automatic climate control systems.\n"
            "6. Orifice tubes are common in fixed-displacement compressor systems.\n"
            "7. Diagnosis differs: TXV faults cause low superheat, while orifice tube blockages cause high side pressure rise.\n"
            "8. Retrofitting from orifice tube to TXV requires system redesign.\n"
            "9. Refrigerant compatibility must be ensured for both devices.\n"
            "10. Selection impacts system response, efficiency, and icing risk."
        ),
        key_factors=[
            "System complexity",
            "Control requirements",
            "Cost",
            "Serviceability",
            "Performance"
        ],
        primary_authority=[
            "SAE J2064",
            "Automotive HVAC System Design",
            "OEM Service Manuals"
        ],
        burden_holder="System designer",
        adversary_position="TXVs are always superior to orifice tubes.",
        counter_arguments=[
            "Orifice tubes are adequate for many applications and offer cost/service advantages.",
            "TXVs add complexity and cost, not always justified by performance gains."
        ],
        resolution_strategy="Match expansion device to system requirements and reference OEM recommendations.",
        entity_scope="Automotive HVAC expansion devices",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="Receiver-Drier vs. Accumulator Function",
        keywords=["receiver-drier", "accumulator", "moisture removal", "liquid storage", "system type"],
        conclusion_template="Receiver-driers are used with TXV systems for liquid storage and moisture removal; accumulators are used with orifice tube systems to prevent liquid slugging.",
        reasoning_framework=(
            "1. Receiver-driers are located on the high-pressure side, storing liquid refrigerant and removing moisture with desiccant.\n"
            "2. Accumulators are located on the low-pressure side, storing excess refrigerant and preventing liquid entry to the compressor.\n"
            "3. TXV systems require receiver-driers to ensure a steady supply of liquid refrigerant.\n"
            "4. Orifice tube systems use accumulators to manage refrigerant charge and protect the compressor.\n"
            "5. Moisture removal is critical to prevent acid formation and corrosion.\n"
            "6. Desiccant life is limited; receiver-driers/accumulators should be replaced after system opening.\n"
            "7. Incorrect component selection leads to poor performance and compressor damage.\n"
            "8. Diagnosis includes checking for desiccant breakdown, clogging, and refrigerant flow restriction.\n"
            "9. System retrofits may require conversion between receiver-drier and accumulator.\n"
            "10. Always use OEM-specified components for compatibility and performance."
        ),
        key_factors=[
            "System type (TXV or orifice tube)",
            "Moisture removal",
            "Refrigerant storage",
            "Compressor protection",
            "Desiccant condition"
        ],
        primary_authority=[
            "SAE J2064",
            "Automotive HVAC System Design",
            "OEM Service Manuals"
        ],
        burden_holder="System designer/technician",
        adversary_position="Receiver-driers and accumulators are interchangeable.",
        counter_arguments=[
            "System design dictates correct component; interchange leads to malfunction.",
            "Moisture and liquid management requirements differ between systems."
        ],
        resolution_strategy="Reference system type and OEM documentation for correct component selection.",
        entity_scope="Automotive HVAC receiver-driers and accumulators",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="A/C System Pressure Diagnosis",
        keywords=["pressure diagnosis", "manifold gauge", "high side", "low side", "overcharge", "undercharge"],
        conclusion_template="Accurate pressure diagnosis using manifold gauges is essential for identifying system faults such as overcharge, undercharge, or component failure.",
        reasoning_framework=(
            "1. Manifold gauges measure high and low side pressures, compared to system specifications.\n"
            "2. High low-side and low high-side pressures indicate compressor inefficiency or internal leakage.\n"
            "3. Low low-side and high high-side pressures suggest overcharge or condenser airflow restriction.\n"
            "4. Both low pressures may indicate undercharge or severe restriction (e.g., clogged orifice tube).\n"
            "5. Rapid pressure equalization after shutdown points to compressor reed valve failure.\n"
            "6. Pressure readings must be taken with proper ambient temperature and engine speed.\n"
            "7. Diagnosis should include temperature readings at key points (inlet/outlet, evaporator, condenser).\n"
            "8. Non-condensable gases (air) cause abnormally high pressures and poor cooling.\n"
            "9. Always verify gauge calibration and hose integrity.\n"
            "10. Use pressure/temperature charts for refrigerant in use."
        ),
        key_factors=[
            "Pressure readings",
            "Ambient temperature",
            "System charge",
            "Component function",
            "Gauge calibration"
        ],
        primary_authority=[
            "SAE J639",
            "Automotive HVAC Diagnosis Manuals",
            "OEM Service Information"
        ],
        burden_holder="Technician",
        adversary_position="Pressure readings are unreliable due to system variability.",
        counter_arguments=[
            "Pressure diagnosis is standardized and effective when performed correctly.",
            "System variability is accounted for in OEM specifications and charts."
        ],
        resolution_strategy="Follow OEM diagnostic procedures and use calibrated tools.",
        entity_scope="Automotive HVAC systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="Refrigerant Recovery & EPA 609 Compliance",
        keywords=["refrigerant recovery", "EPA 609", "environmental compliance", "recycling", "venting prohibition"],
        conclusion_template="All refrigerant recovery, recycling, and recharging must comply with EPA 609, prohibiting venting and mandating certified equipment and technicians.",
        reasoning_framework=(
            "1. The Clean Air Act prohibits venting refrigerants during service or repair.\n"
            "2. EPA 609 certification is required for all technicians servicing MVAC systems.\n"
            "3. Certified recovery/recycling equipment must be used to capture refrigerant.\n"
            "4. Recovered refrigerant must be recycled or disposed of per EPA regulations.\n"
            "5. Service records must document recovery/recycling and technician certification.\n"
            "6. Fines and penalties apply for non-compliance.\n"
            "7. Only approved refrigerants (e.g., R-134a, R-1234yf) may be used in MVAC systems.\n"
            "8. Cross-contamination of refrigerants is prohibited; dedicated equipment required.\n"
            "9. Leak testing and repair must precede system recharge.\n"
            "10. Compliance ensures environmental protection and legal operation."
        ),
        key_factors=[
            "Technician certification",
            "Recovery/recycling equipment",
            "Service documentation",
            "Refrigerant type",
            "Leak repair"
        ],
        primary_authority=[
            "EPA 609",
            "Clean Air Act Section 609",
            "SAE J2210"
        ],
        burden_holder="Service provider/technician",
        adversary_position="Small releases are acceptable if unintentional.",
        counter_arguments=[
            "EPA regulations prohibit all venting, intentional or accidental.",
            "Proper procedures prevent unintentional releases."
        ],
        resolution_strategy="Follow EPA and SAE guidelines; maintain certification and documentation.",
        entity_scope="Mobile Vehicle Air Conditioning (MVAC) service",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="EPA 609"
    ),
    DoctrineBlock(
        topic="Cabin Air Filtration & Air Quality",
        keywords=["cabin air filter", "particulate filtration", "HEPA", "activated carbon", "air quality"],
        conclusion_template="Cabin air filtration is essential for occupant health and HVAC performance, with filter selection (particulate, HEPA, carbon) based on vehicle application and air quality requirements.",
        reasoning_framework=(
            "1. Cabin air filters remove particulates, pollen, and in some cases odors and gases from incoming air.\n"
            "2. Filter types include particulate (standard), HEPA (high efficiency), and activated carbon (odor/gas removal).\n"
            "3. Filter location (fresh air intake, HVAC housing) impacts serviceability and effectiveness.\n"
            "4. Clogged filters reduce airflow, increase blower load, and may contribute to evaporator icing.\n"
            "5. Replacement intervals are specified by OEMs, typically 12,000-20,000 miles or annually.\n"
            "6. HEPA and carbon filters are recommended for urban/high-pollution environments.\n"
            "7. Filter efficiency is measured by particle size removal (e.g., 0.3 micron for HEPA).\n"
            "8. Poor air quality impacts occupant health, especially for sensitive individuals.\n"
            "9. Aftermarket filters must meet or exceed OEM specifications.\n"
            "10. Always verify correct filter installation and orientation."
        ),
        key_factors=[
            "Filter type and efficiency",
            "Replacement interval",
            "Airflow rate",
            "Occupant health",
            "Installation quality"
        ],
        primary_authority=[
            "ASHRAE Standard 52.2",
            "OEM Service Manuals",
            "EPA Indoor Air Quality Guidelines"
        ],
        burden_holder="Vehicle owner/service provider",
        adversary_position="Cabin air filters are unnecessary in most climates.",
        counter_arguments=[
            "Modern vehicles require cabin filtration for HVAC performance and occupant health.",
            "Omission leads to reduced air quality and system issues."
        ],
        resolution_strategy="Follow OEM recommendations and select appropriate filter type for environment.",
        entity_scope="Automotive HVAC cabin filtration",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASHRAE Standard 52.2"
    ),
    DoctrineBlock(
        topic="Heater Core Operation & Diagnosis",
        keywords=["heater core", "coolant flow", "heat exchanger", "diagnosis", "leak", "airlock"],
        conclusion_template="Heater core function depends on unobstructed coolant flow and heat exchange; diagnosis focuses on flow restriction, leaks, and airlocks.",
        reasoning_framework=(
            "1. The heater core transfers engine coolant heat to cabin air via a finned heat exchanger.\n"
            "2. Proper coolant flow is essential; restrictions (scale, debris) reduce heating.\n"
            "3. Leaks manifest as coolant odor, fogged windows, or wet carpet.\n"
            "4. Airlocks prevent coolant circulation, causing poor heating and potential overheating.\n"
            "5. Diagnosis includes temperature drop measurement across the core, visual inspection, and pressure testing.\n"
            "6. Heater control valves regulate flow in some systems; valve failure mimics core restriction.\n"
            "7. Flushing may restore flow but cannot repair leaks.\n"
            "8. Replacement requires draining coolant and careful HVAC housing disassembly.\n"
            "9. Use only OEM-specified coolant to prevent corrosion and scale.\n"
            "10. Always bleed air from the system after service."
        ),
        key_factors=[
            "Coolant flow",
            "Heat exchanger integrity",
            "Leak detection",
            "Airlock removal",
            "Coolant type"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064",
            "Automotive HVAC Diagnosis Texts"
        ],
        burden_holder="Technician",
        adversary_position="Heater core issues are always due to coolant leaks.",
        counter_arguments=[
            "Flow restriction and airlocks are common non-leak causes of poor heating.",
            "Diagnosis must distinguish between leak and flow issues."
        ],
        resolution_strategy="Use temperature, pressure, and flow diagnostics per OEM procedure.",
        entity_scope="Automotive HVAC heater cores",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="Blend Door Actuators & Mode Door Control",
        keywords=["blend door", "mode door", "actuator", "HVAC control", "diagnosis", "calibration"],
        conclusion_template="Accurate blend and mode door control is essential for temperature and airflow management; diagnosis involves actuator testing and recalibration.",
        reasoning_framework=(
            "1. Blend doors regulate air temperature by mixing heated and cooled air streams.\n"
            "2. Mode doors direct airflow to selected outlets (defrost, floor, dash vents).\n"
            "3. Actuators may be electric, vacuum, or cable-driven; electric actuators are common in modern vehicles.\n"
            "4. Faults include stuck doors, failed actuators, and control module errors.\n"
            "5. Symptoms: incorrect temperature, airflow from wrong outlets, or clicking noises.\n"
            "6. Diagnosis includes actuator command testing, position sensor feedback, and recalibration procedures.\n"
            "7. Some systems require scan tool calibration after repair or battery disconnect.\n"
            "8. Physical obstruction (debris, broken linkage) may prevent door movement.\n"
            "9. Replacement actuators must match OE specifications for torque and travel.\n"
            "10. Calibration ensures correct door position and response to controls."
        ),
        key_factors=[
            "Actuator type and function",
            "Control module logic",
            "Calibration procedure",
            "Physical obstructions",
            "Feedback sensors"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "Automotive HVAC Control System Texts",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="Actuator replacement alone resolves all blend/mode door issues.",
        counter_arguments=[
            "Calibration and control logic faults may persist after actuator replacement.",
            "Physical obstructions must be ruled out."
        ],
        resolution_strategy="Follow OEM diagnostic and calibration procedures; verify actuator and control module function.",
        entity_scope="Automotive HVAC blend/mode door systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="Automatic Climate Control Systems",
        keywords=["automatic climate control", "HVAC control module", "temperature sensor", "feedback", "setpoint"],
        conclusion_template="Automatic climate control systems use multiple sensors and feedback loops to maintain cabin temperature at user-set levels, requiring precise calibration and diagnosis.",
        reasoning_framework=(
            "1. Automatic systems regulate temperature, airflow, and mode based on user setpoint and sensor feedback.\n"
            "2. Sensors include cabin, ambient, sunload, and evaporator temperature.\n"
            "3. The HVAC control module processes sensor data and commands actuators (blend, mode, fan speed).\n"
            "4. Faults manifest as incorrect temperature, erratic operation, or loss of automatic function.\n"
            "5. Diagnosis includes sensor value reading (scan tool), actuator testing, and self-diagnostic routines.\n"
            "6. Calibration is required after component replacement or battery disconnect.\n"
            "7. Software updates may resolve control logic issues.\n"
            "8. Sensor contamination (dust, debris) affects accuracy.\n"
            "9. System may default to manual mode if faults are detected.\n"
            "10. Always verify correct setpoint and sensor operation before component replacement."
        ),
        key_factors=[
            "Sensor accuracy",
            "Control module logic",
            "Calibration",
            "Actuator response",
            "Software updates"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064",
            "Automotive HVAC Control System Texts"
        ],
        burden_holder="Technician",
        adversary_position="Automatic systems are unreliable and difficult to diagnose.",
        counter_arguments=[
            "Modern systems include self-diagnostics and scan tool support.",
            "Proper training and tools enable effective diagnosis."
        ],
        resolution_strategy="Use OEM diagnostic procedures and scan tools; verify calibration and sensor function.",
        entity_scope="Automotive automatic climate control systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="Heat Pump Systems for Electric Vehicles",
        keywords=["heat pump", "electric vehicle", "reversible cycle", "thermal management", "efficiency"],
        conclusion_template="Heat pump HVAC systems in electric vehicles provide efficient heating and cooling by reversing the refrigeration cycle, reducing energy consumption compared to resistive heating.",
        reasoning_framework=(
            "1. Heat pumps transfer heat from ambient air to the cabin in heating mode, and vice versa for cooling.\n"
            "2. Reversible flow is achieved with a four-way valve and control logic.\n"
            "3. Heat pumps are more energy-efficient than resistive heaters, preserving EV driving range.\n"
            "4. System performance declines at low ambient temperatures; supplemental heating may be required.\n"
            "5. Diagnosis includes checking valve operation, refrigerant charge, and sensor feedback.\n"
            "6. Advanced systems integrate battery thermal management for optimal efficiency.\n"
            "7. Control software is critical for mode switching and fault detection.\n"
            "8. Heat pump systems require refrigerants with suitable low-temperature properties (e.g., R-1234yf).\n"
            "9. Service procedures differ from conventional HVAC; technician training is essential.\n"
            "10. System retrofits are complex and not generally feasible."
        ),
        key_factors=[
            "System configuration",
            "Refrigerant properties",
            "Control logic",
            "Ambient temperature",
            "Technician training"
        ],
        primary_authority=[
            "SAE J2773",
            "OEM EV Service Manuals",
            "ASHRAE Fundamentals Handbook"
        ],
        burden_holder="System designer/technician",
        adversary_position="Heat pumps are unsuitable for automotive use due to low ambient performance.",
        counter_arguments=[
            "Supplemental heating and advanced controls mitigate low-temperature limitations.",
            "Efficiency gains outweigh limitations in most climates."
        ],
        resolution_strategy="Reference SAE and OEM guidelines; assess climate suitability and system integration.",
        entity_scope="Electric vehicle HVAC systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J2773"
    ),
    DoctrineBlock(
        topic="A/C System Leak Detection Methods",
        keywords=["leak detection", "UV dye", "electronic detector", "nitrogen pressure", "soap solution"],
        conclusion_template="Effective A/C leak detection combines visual, electronic, and pressure-based methods to ensure system integrity before recharging.",
        reasoning_framework=(
            "1. Leaks are the most common cause of A/C underperformance and environmental release.\n"
            "2. UV dye is added to refrigerant; leaks fluoresce under UV light for visual detection.\n"
            "3. Electronic leak detectors sense refrigerant molecules and pinpoint small leaks.\n"
            "4. Nitrogen pressure testing (with trace hydrogen or forming gas) is used when the system is empty.\n"
            "5. Soap solution reveals leaks by bubbling at the fault site.\n"
            "6. All methods have limitations; small or intermittent leaks may require multiple techniques.\n"
            "7. System must be leak-free before recharging to prevent environmental harm and callbacks.\n"
            "8. Always clean suspected leak areas before testing.\n"
            "9. Replace O-rings and seals as needed during service.\n"
            "10. Document leak location and repair for compliance."
        ),
        key_factors=[
            "Detection method",
            "Leak size",
            "System pressure",
            "Environmental conditions",
            "Documentation"
        ],
        primary_authority=[
            "EPA 609",
            "SAE J1628",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Electronic detectors alone are sufficient for all leaks.",
        counter_arguments=[
            "No single method detects all leaks; combined approaches are necessary.",
            "Visual confirmation is required for repair documentation."
        ],
        resolution_strategy="Use multiple detection methods and verify repair before system recharge.",
        entity_scope="Automotive HVAC systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="SAE J1628"
    ),
    # 25+ additional DoctrineBlock instances with real content follow:
    DoctrineBlock(
        topic="Clutch Cycling Switch Operation",
        keywords=["clutch cycling switch", "compressor control", "low pressure", "evaporator temperature"],
        conclusion_template="Clutch cycling switches protect the compressor and prevent evaporator icing by disengaging the clutch at low pressure thresholds.",
        reasoning_framework=(
            "1. The clutch cycling switch monitors low-side pressure and cycles the compressor clutch to maintain evaporator temperature above freezing.\n"
            "2. If pressure drops below the setpoint, the switch opens, disengaging the clutch.\n"
            "3. This prevents evaporator icing and compressor damage from liquid slugging.\n"
            "4. Faulty switches may cause no cooling (open circuit) or icing (failed closed).\n"
            "5. Diagnosis includes pressure reading, switch continuity, and system response to bypass.\n"
            "6. Replacement switches must match OEM pressure setpoints.\n"
            "7. Some systems use evaporator temperature sensors instead of pressure switches.\n"
            "8. Verify wiring and connector integrity during diagnosis.\n"
            "9. Cycling frequency should match system design; rapid cycling indicates low charge or restriction.\n"
            "10. Always recalibrate or reset system as required after switch replacement."
        ),
        key_factors=[
            "Switch setpoint",
            "System pressure",
            "Wiring integrity",
            "Evaporator temperature",
            "Compressor protection"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="Clutch cycling switches are unnecessary with modern control modules.",
        counter_arguments=[
            "Many systems still rely on pressure switches for primary compressor protection.",
            "Redundancy improves system reliability."
        ],
        resolution_strategy="Follow OEM wiring diagrams and diagnostic procedures.",
        entity_scope="Automotive HVAC compressor control",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="Orifice Tube Contamination Diagnosis",
        keywords=["orifice tube", "contamination", "restriction", "metal debris", "black death"],
        conclusion_template="Contaminated orifice tubes indicate compressor failure or system contamination, requiring thorough flushing and component replacement.",
        reasoning_framework=(
            "1. Orifice tubes filter debris as refrigerant passes through a fine mesh screen.\n"
            "2. Metal shavings or black sludge (black death) on the tube indicate compressor wear or internal breakdown.\n"
            "3. Contamination restricts refrigerant flow, causing high-side pressure rise and poor cooling.\n"
            "4. Diagnosis involves tube removal and inspection for debris.\n"
            "5. System must be flushed with approved solvent; all affected components replaced.\n"
            "6. Failure to remove contamination leads to repeat failures.\n"
            "7. Always replace the orifice tube after compressor failure.\n"
            "8. Use inline filters as recommended by OEMs.\n"
            "9. Verify oil type and quantity during reassembly.\n"
            "10. Document findings for warranty and repair records."
        ),
        key_factors=[
            "Debris type",
            "Compressor condition",
            "Flushing procedure",
            "Component replacement",
            "Oil management"
        ],
        primary_authority=[
            "SAE J2064",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Flushing alone is sufficient after orifice tube contamination.",
        counter_arguments=[
            "Component replacement is necessary to remove all contamination.",
            "Flushing cannot remove debris from parallel flow condensers."
        ],
        resolution_strategy="Follow SAE and OEM service bulletins for contamination events.",
        entity_scope="Automotive HVAC orifice tube systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="Dual-Zone HVAC System Design",
        keywords=["dual-zone", "HVAC", "independent control", "blend door", "occupant comfort"],
        conclusion_template="Dual-zone HVAC systems provide independent temperature control for driver and passenger, requiring additional sensors, blend doors, and control logic.",
        reasoning_framework=(
            "1. Dual-zone systems use separate temperature sensors and blend doors for each zone.\n"
            "2. The HVAC control module manages independent setpoints and actuator positions.\n"
            "3. Additional ducting and airflow management are required for effective separation.\n"
            "4. Faults may include actuator failure, sensor error, or control logic issues.\n"
            "5. Diagnosis involves scan tool reading of sensor values and actuator commands.\n"
            "6. Calibration is required after component replacement.\n"
            "7. System complexity increases service time and cost.\n"
            "8. Proper operation improves occupant comfort and satisfaction.\n"
            "9. Aftermarket retrofits are not recommended due to integration challenges.\n"
            "10. Always verify correct operation after repair."
        ),
        key_factors=[
            "Sensor accuracy",
            "Actuator function",
            "Control module logic",
            "Airflow management",
            "Calibration"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="System designer/technician",
        adversary_position="Dual-zone systems are unnecessary complexity.",
        counter_arguments=[
            "Occupant comfort and market demand justify dual-zone systems.",
            "Proper design and diagnosis mitigate complexity concerns."
        ],
        resolution_strategy="Follow OEM design and diagnostic procedures.",
        entity_scope="Passenger vehicle HVAC systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="HVAC Blower Motor Diagnosis",
        keywords=["blower motor", "fan speed", "resistor", "control module", "diagnosis"],
        conclusion_template="Blower motor performance is critical for HVAC operation; diagnosis includes electrical testing, resistor/module inspection, and airflow verification.",
        reasoning_framework=(
            "1. Blower motors provide airflow across the evaporator and heater core.\n"
            "2. Speed control is achieved with resistors (manual systems) or electronic modules (automatic systems).\n"
            "3. Faults include open circuits, worn brushes, resistor/module failure, or airflow obstruction.\n"
            "4. Diagnosis involves voltage and current testing at the motor, control switch, and resistor/module.\n"
            "5. Reduced airflow may indicate clogged cabin filter or blocked ducts.\n"
            "6. Noise or vibration suggests worn bearings or debris in the fan.\n"
            "7. Replacement motors must match OE specifications for speed and airflow.\n"
            "8. Always verify control signal integrity and ground connections.\n"
            "9. After repair, confirm all speed settings and airflow at outlets.\n"
            "10. Document findings for warranty and repair records."
        ),
        key_factors=[
            "Electrical supply",
            "Control module/resistor",
            "Airflow rate",
            "Physical obstruction",
            "Motor integrity"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="Blower motor issues are always due to resistor failure.",
        counter_arguments=[
            "Motor wear and wiring faults are common causes.",
            "Comprehensive diagnosis prevents unnecessary part replacement."
        ],
        resolution_strategy="Follow OEM diagnostic procedures and verify all circuit components.",
        entity_scope="Automotive HVAC blower systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="A/C Compressor Clutch Control Circuit Diagnosis",
        keywords=["compressor clutch", "control circuit", "relay", "fuse", "diagnosis"],
        conclusion_template="Compressor clutch control circuit faults are diagnosed by systematic testing of relays, fuses, wiring, and control signals.",
        reasoning_framework=(
            "1. The clutch control circuit includes the A/C switch, relay, fuse, pressure switches, and PCM/BCM control.\n"
            "2. Loss of clutch engagement may result from relay/fuse failure, wiring faults, or module command issues.\n"
            "3. Diagnosis involves voltage testing at each point in the circuit.\n"
            "4. Bypass testing can isolate relay or switch faults.\n"
            "5. PCM/BCM may inhibit clutch operation for engine protection (overheat, WOT, low idle).\n"
            "6. Always verify control module outputs with a scan tool.\n"
            "7. Replace relays/fuses with OE parts only.\n"
            "8. Inspect connectors for corrosion or loose pins.\n"
            "9. Document findings and repairs for warranty compliance.\n"
            "10. Reset or recalibrate system as required after repair."
        ),
        key_factors=[
            "Relay/fuse integrity",
            "Wiring condition",
            "Control module logic",
            "Switch function",
            "Scan tool data"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="Clutch control faults are always due to low refrigerant.",
        counter_arguments=[
            "Electrical faults are common and must be ruled out.",
            "Low refrigerant disables clutch via pressure switch, but circuit faults are independent."
        ],
        resolution_strategy="Use wiring diagrams and systematic voltage testing.",
        entity_scope="Automotive HVAC compressor control",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="HVAC System Odor Remediation",
        keywords=["odor", "evaporator", "mold", "bacteria", "cleaning", "disinfectant"],
        conclusion_template="Persistent HVAC odors are addressed by cleaning the evaporator, applying disinfectant, and ensuring proper drainage and filtration.",
        reasoning_framework=(
            "1. Odors originate from mold and bacteria growth on the evaporator surface due to moisture accumulation.\n"
            "2. Cabin air filters reduce particulate buildup but do not eliminate microbial growth.\n"
            "3. Cleaning involves applying approved disinfectant to the evaporator and HVAC housing.\n"
            "4. Drainage must be verified to prevent standing water.\n"
            "5. Running the blower on high with A/C off after use helps dry the evaporator.\n"
            "6. Persistent odors may require HVAC housing disassembly and deep cleaning.\n"
            "7. Use only EPA-registered disinfectants to avoid material damage.\n"
            "8. Replace cabin air filter after remediation.\n"
            "9. Educate vehicle owners on preventive measures.\n"
            "10. Document remediation for warranty and customer records."
        ),
        key_factors=[
            "Moisture control",
            "Evaporator cleaning",
            "Disinfectant use",
            "Drainage verification",
            "Cabin filter replacement"
        ],
        primary_authority=[
            "EPA Indoor Air Quality Guidelines",
            "OEM Service Manuals"
        ],
        burden_holder="Technician/vehicle owner",
        adversary_position="Odor remediation is unnecessary if the system cools properly.",
        counter_arguments=[
            "Odors impact occupant health and satisfaction.",
            "Microbial growth can damage HVAC components."
        ],
        resolution_strategy="Follow EPA and OEM cleaning procedures; educate owners on prevention.",
        entity_scope="Automotive HVAC systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA Indoor Air Quality Guidelines"
    ),
    DoctrineBlock(
        topic="A/C System Retrofit for Alternative Refrigerants",
        keywords=["retrofit", "alternative refrigerant", "R-1234yf", "R-134a", "compatibility"],
        conclusion_template="A/C system retrofits for alternative refrigerants require component compatibility verification, proper labeling, and adherence to regulatory guidelines.",
        reasoning_framework=(
            "1. Retrofitting from R-134a to R-1234yf or other alternatives requires assessment of compressor, seals, hoses, and condenser compatibility.\n"
            "2. System must be evacuated and flushed to remove old oil and refrigerant.\n"
            "3. Only approved lubricants (e.g., PAG, POE) may be used with new refrigerant.\n"
            "4. Retrofit label must be affixed per EPA and SAE standards.\n"
            "5. Leak testing is mandatory before charging with new refrigerant.\n"
            "6. Some components (e.g., condenser, O-rings) may require replacement for compatibility.\n"
            "7. Cross-contamination of refrigerants is prohibited.\n"
            "8. Service equipment must be dedicated to each refrigerant type.\n"
            "9. Retrofit procedures must follow OEM and regulatory guidelines.\n"
            "10. Document all retrofit steps for compliance."
        ),
        key_factors=[
            "Component compatibility",
            "Lubricant selection",
            "Labeling",
            "Leak testing",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EPA 609",
            "SAE J639",
            "OEM Service Bulletins"
        ],
        burden_holder="Technician/service provider",
        adversary_position="Any refrigerant can be used if system is evacuated.",
        counter_arguments=[
            "Component and lubricant compatibility are critical for performance and safety.",
            "Regulations require proper labeling and documentation."
        ],
        resolution_strategy="Follow EPA, SAE, and OEM retrofit procedures.",
        entity_scope="Automotive HVAC systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="Thermal Expansion Valve (TXV) Superheat Adjustment",
        keywords=["TXV", "superheat", "adjustment", "evaporator", "diagnosis"],
        conclusion_template="TXV superheat adjustment ensures optimal evaporator performance and compressor protection; improper adjustment leads to icing or poor cooling.",
        reasoning_framework=(
            "1. Superheat is the temperature difference between evaporator outlet vapor and saturation temperature at outlet pressure.\n"
            "2. TXVs are factory-set but may be adjustable in some applications.\n"
            "3. Low superheat (valve too open) risks liquid slugging and compressor damage.\n"
            "4. High superheat (valve too closed) reduces cooling and increases evaporator temperature.\n"
            "5. Diagnosis involves measuring outlet temperature and pressure, calculating superheat, and comparing to specifications.\n"
            "6. Adjustment is made per OEM procedure, typically by turning an external screw.\n"
            "7. Always verify refrigerant charge and airflow before adjusting TXV.\n"
            "8. Document adjustment and final superheat value.\n"
            "9. Non-adjustable TXVs must be replaced if out of specification.\n"
            "10. Use calibrated instruments for accurate measurement."
        ),
        key_factors=[
            "Superheat value",
            "Valve adjustment",
            "Refrigerant charge",
            "Airflow",
            "Measurement accuracy"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="TXVs do not require adjustment in any circumstance.",
        counter_arguments=[
            "Some applications require field adjustment for optimal performance.",
            "Diagnosis must precede adjustment."
        ],
        resolution_strategy="Follow OEM procedure and verify all system parameters.",
        entity_scope="Automotive HVAC TXV systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="Accumulator Desiccant Replacement",
        keywords=["accumulator", "desiccant", "moisture", "replacement", "system opening"],
        conclusion_template="Accumulator desiccant must be replaced after system opening to ensure moisture removal and prevent acid formation.",
        reasoning_framework=(
            "1. Accumulators contain desiccant to absorb moisture from refrigerant.\n"
            "2. Moisture leads to acid formation, corrosion, and component failure.\n"
            "3. Desiccant is depleted over time or after system opening.\n"
            "4. Replacement is required after compressor failure, major repair, or leak repair.\n"
            "5. Some accumulators allow desiccant bag replacement; others require full unit replacement.\n"
            "6. Always use OEM-specified desiccant type and quantity.\n"
            "7. Failure to replace desiccant voids warranty and risks repeat failure.\n"
            "8. Document replacement in service records.\n"
            "9. Verify accumulator integrity and refrigerant flow after service.\n"
            "10. Proper evacuation removes residual moisture before recharge."
        ),
        key_factors=[
            "Moisture content",
            "Desiccant condition",
            "System opening",
            "Component compatibility",
            "Documentation"
        ],
        primary_authority=[
            "SAE J2064",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Desiccant replacement is unnecessary if accumulator is not leaking.",
        counter_arguments=[
            "Moisture enters during any system opening; desiccant must be renewed.",
            "OEM and SAE standards require replacement."
        ],
        resolution_strategy="Replace desiccant or accumulator after any system opening.",
        entity_scope="Automotive HVAC accumulator systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="A/C System Oil Management",
        keywords=["oil", "PAG", "POE", "lubrication", "compressor", "oil balancing"],
        conclusion_template="Proper oil type and quantity are essential for compressor lubrication and system reliability; oil balancing is required after component replacement.",
        reasoning_framework=(
            "1. A/C systems use specific oils (PAG, POE) compatible with refrigerant and component materials.\n"
            "2. Oil circulates with refrigerant, lubricating compressor and seals.\n"
            "3. Incorrect oil type or quantity leads to poor lubrication, acid formation, and failure.\n"
            "4. Oil balancing replaces oil lost during component replacement or flushing.\n"
            "5. Overfilling reduces cooling efficiency and risks slugging; underfilling causes wear.\n"
            "6. Always measure oil removed from old components and add equivalent amount to new parts.\n"
            "7. Use only OEM-specified oil type and viscosity.\n"
            "8. Document oil type and quantity in service records.\n"
            "9. Aftermarket additives are not recommended unless approved by OEM.\n"
            "10. Verify system performance after service."
        ),
        key_factors=[
            "Oil type",
            "Oil quantity",
            "Component replacement",
            "Lubrication",
            "Documentation"
        ],
        primary_authority=[
            "SAE J2064",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Oil quantity is not critical as long as some oil is present.",
        counter_arguments=[
            "Precise oil quantity is essential for system reliability.",
            "OEM and SAE standards specify oil management procedures."
        ],
        resolution_strategy="Follow OEM oil balancing procedures and use correct oil type.",
        entity_scope="Automotive HVAC systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="A/C System Electrical Load Management",
        keywords=["electrical load", "compressor clutch", "blower motor", "alternator", "load shedding"],
        conclusion_template="A/C system electrical loads are managed by control modules to prevent battery drain and maintain engine performance, especially at idle or high demand.",
        reasoning_framework=(
            "1. Compressor clutch and blower motor are significant electrical loads.\n"
            "2. Control modules (PCM/BCM) may shed A/C load during low voltage, high temperature, or wide-open throttle.\n"
            "3. Symptoms of load shedding include intermittent A/C operation or blower speed reduction.\n"
            "4. Diagnosis involves scan tool monitoring of control module commands and voltage levels.\n"
            "5. Alternator output must be verified under full load.\n"
            "6. Battery condition affects A/C system reliability.\n"
            "7. Aftermarket electrical accessories may impact load management.\n"
            "8. Always verify ground and power connections.\n"
            "9. Document findings and repairs for warranty compliance.\n"
            "10. Educate owners on system operation under high electrical demand."
        ),
        key_factors=[
            "Control module logic",
            "Voltage levels",
            "Alternator output",
            "Battery condition",
            "Accessory load"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="A/C electrical loads are insignificant and do not affect vehicle operation.",
        counter_arguments=[
            "A/C loads are substantial and managed by control logic for reliability.",
            "Diagnosis must include electrical system assessment."
        ],
        resolution_strategy="Monitor system operation with scan tool and verify electrical system health.",
        entity_scope="Automotive HVAC systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="A/C System High Pressure Relief Valve Function",
        keywords=["high pressure", "relief valve", "safety", "overpressure", "system protection"],
        conclusion_template="High pressure relief valves protect the A/C system from dangerous overpressure by venting refrigerant in fault conditions.",
        reasoning_framework=(
            "1. Relief valves are installed on compressors or receiver-driers to vent refrigerant if pressure exceeds safe limits.\n"
            "2. Overpressure may result from condenser blockage, fan failure, or overcharge.\n"
            "3. Valve activation prevents hose rupture and component damage.\n"
            "4. After activation, the system must be inspected for root cause and repaired before recharge.\n"
            "5. Relief valves are single-use and must be replaced after activation.\n"
            "6. Always use OEM-specified valves for correct pressure rating.\n"
            "7. Document valve activation and repairs for compliance.\n"
            "8. Educate vehicle owners on the importance of prompt service after relief event.\n"
            "9. Verify system operation and pressures after repair.\n"
            "10. Never bypass or disable relief valves."
        ),
        key_factors=[
            "Pressure rating",
            "Root cause diagnosis",
            "Valve replacement",
            "System inspection",
            "Documentation"
        ],
        primary_authority=[
            "SAE J639",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Relief valves are unnecessary if system is properly charged.",
        counter_arguments=[
            "Component failure or blockage can cause overpressure even in properly charged systems.",
            "Relief valves are a critical safety feature."
        ],
        resolution_strategy="Replace activated valves and address root cause before system recharge.",
        entity_scope="Automotive HVAC systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="A/C System Flushing Procedure",
        keywords=["flushing", "contamination", "solvent", "component replacement", "procedure"],
        conclusion_template="A/C system flushing removes contaminants after compressor failure or major repair; only approved solvents and procedures must be used.",
        reasoning_framework=(
            "1. Flushing is required after compressor failure, black death, or major component replacement.\n"
            "2. Only approved solvents (not R-134a or other refrigerants) may be used for flushing.\n"
            "3. Parallel flow condensers cannot be effectively flushed and must be replaced if contaminated.\n"
            "4. All hoses, evaporators, and accumulators/receiver-driers must be flushed or replaced as required.\n"
            "5. Flushing removes oil, debris, and moisture.\n"
            "6. System must be thoroughly dried with compressed air or nitrogen.\n"
            "7. Add correct oil quantity after flushing.\n"
            "8. Document procedure and replaced components.\n"
            "9. Verify system operation after reassembly.\n"
            "10. Follow OEM and SAE guidelines for all flushing operations."
        ),
        key_factors=[
            "Solvent selection",
            "Component replacement",
            "Drying procedure",
            "Oil management",
            "Documentation"
        ],
        primary_authority=[
            "SAE J2210",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Flushing with refrigerant is acceptable and effective.",
        counter_arguments=[
            "Environmental regulations prohibit refrigerant flushing.",
            "Only approved solvents and procedures are effective and compliant."
        ],
        resolution_strategy="Follow SAE and OEM flushing procedures; replace components as required.",
        entity_scope="Automotive HVAC systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2210"
    ),
    DoctrineBlock(
        topic="A/C System Performance Testing",
        keywords=["performance test", "vent temperature", "ambient temperature", "pressure", "diagnosis"],
        conclusion_template="A/C system performance is evaluated by measuring vent temperature, system pressures, and comparing to OEM specifications under controlled conditions.",
        reasoning_framework=(
            "1. Performance testing verifies cooling capacity and system health.\n"
            "2. Test is performed with doors/windows closed, blower on high, and engine at specified RPM.\n"
            "3. Measure vent temperature, ambient temperature, high and low side pressures.\n"
            "4. Compare results to OEM performance charts for given ambient conditions.\n"
            "5. Deviations indicate faults such as low charge, airflow restriction, or component failure.\n"
            "6. Record all measurements and test conditions.\n"
            "7. Repeat test after repairs to confirm resolution.\n"
            "8. Use calibrated instruments for accuracy.\n"
            "9. Document results for warranty and customer records.\n"
            "10. Educate owners on expected performance in extreme conditions."
        ),
        key_factors=[
            "Vent temperature",
            "System pressures",
            "Ambient conditions",
            "Test procedure",
            "Documentation"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="Performance testing is unnecessary if system is cold to the touch.",
        counter_arguments=[
            "Objective measurements are required for accurate diagnosis and warranty.",
            "Subjective assessment is unreliable."
        ],
        resolution_strategy="Follow OEM test procedures and record all results.",
        entity_scope="Automotive HVAC systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="A/C System Noise Diagnosis",
        keywords=["noise", "compressor", "expansion valve", "blower motor", "diagnosis"],
        conclusion_template="A/C system noise diagnosis distinguishes between normal and abnormal sounds, identifying component faults such as compressor wear, valve chatter, or airflow obstruction.",
        reasoning_framework=(
            "1. Normal noises include compressor engagement click, refrigerant flow hiss, and blower operation.\n"
            "2. Abnormal noises: grinding (compressor wear), squeal (belt), rattle (mounting), or valve chatter (TXV/orifice tube).\n"
            "3. Diagnosis involves isolating noise source with stethoscope, listening at various speeds and modes.\n"
            "4. Blower motor noise may indicate debris or worn bearings.\n"
            "5. Expansion valve noise may be normal at certain loads but persistent chatter indicates malfunction.\n"
            "6. Document noise type, frequency, and operating conditions.\n"
            "7. Replace or repair faulty components as required.\n"
            "8. Verify noise resolution after repair.\n"
            "9. Educate owners on normal system sounds.\n"
            "10. Use OEM guidelines for noise diagnosis and repair."
        ),
        key_factors=[
            "Noise type",
            "Operating condition",
            "Component isolation",
            "Repair verification",
            "Documentation"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="All A/C system noises indicate failure.",
        counter_arguments=[
            "Some noises are normal and do not require repair.",
            "Diagnosis must distinguish between normal and abnormal sounds."
        ],
        resolution_strategy="Use systematic diagnosis and OEM guidelines.",
        entity_scope="Automotive HVAC systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="A/C System Refrigerant Identification",
        keywords=["refrigerant identification", "R-134a", "R-1234yf", "contamination", "identifier"],
        conclusion_template="Refrigerant identification is mandatory before service to prevent cross-contamination and ensure system compatibility.",
        reasoning_framework=(
            "1. Use electronic refrigerant identifiers to verify type and purity before recovery or service.\n"
            "2. Cross-contamination leads to system failure, environmental harm, and warranty denial.\n"
            "3. Only approved refrigerants may be used in MVAC systems.\n"
            "4. Dedicated service equipment is required for each refrigerant type.\n"
            "5. Document refrigerant type and purity in service records.\n"
            "6. Contaminated refrigerant must be recovered and disposed of per EPA guidelines.\n"
            "7. System retrofits require proper labeling and documentation.\n"
            "8. Always verify refrigerant before adding oil or dye.\n"
            "9. Educate technicians on identifier use and interpretation.\n"
            "10. Follow OEM and EPA procedures for all refrigerant handling."
        ),
        key_factors=[
            "Identifier accuracy",
            "Service equipment",
            "Documentation",
            "Regulatory compliance",
            "Technician training"
        ],
        primary_authority=[
            "EPA 609",
            "SAE J2912",
            "OEM Service Manuals"
        ],
        burden_holder="Technician/service provider",
        adversary_position="Refrigerant identification is unnecessary if system is cooling.",
        counter_arguments=[
            "Contaminated or incorrect refrigerant may cause long-term damage.",
            "Regulations require identification before service."
        ],
        resolution_strategy="Use identifiers before recovery or service; document all findings.",
        entity_scope="Automotive HVAC systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="SAE J2912"
    ),
    DoctrineBlock(
        topic="A/C System O-Ring and Seal Replacement",
        keywords=["O-ring", "seal", "leak prevention", "compatibility", "replacement"],
        conclusion_template="O-rings and seals must be replaced with compatible materials during A/C service to ensure leak-free operation.",
        reasoning_framework=(
            "1. O-rings and seals degrade over time and with exposure to refrigerant and oil.\n"
            "2. Use only materials compatible with refrigerant and oil type (e.g., HNBR for R-134a, R-1234yf).\n"
            "3. Always replace O-rings and seals when opening system connections.\n"
            "4. Lubricate new O-rings with system oil before installation.\n"
            "5. Inspect sealing surfaces for damage or corrosion.\n"
            "6. Use correct size and cross-section for each application.\n"
            "7. Document replacement in service records.\n"
            "8. Leak test system after reassembly.\n"
            "9. Aftermarket kits must meet or exceed OEM specifications.\n"
            "10. Educate technicians on correct seal selection and installation."
        ),
        key_factors=[
            "Material compatibility",
            "Seal size",
            "Lubrication",
            "Installation quality",
            "Leak testing"
        ],
        primary_authority=[
            "SAE J2064",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Old O-rings can be reused if undamaged.",
        counter_arguments=[
            "Aged O-rings lose elasticity and sealing ability.",
            "Replacement is required for leak-free service."
        ],
        resolution_strategy="Replace all O-rings and seals during service; verify with leak test.",
        entity_scope="Automotive HVAC systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="A/C System Service Port Protection",
        keywords=["service port", "Schrader valve", "cap", "contamination", "leak prevention"],
        conclusion_template="Service port caps are the primary seal against refrigerant leaks and contamination; always install and verify caps after service.",
        reasoning_framework=(
            "1. Service port caps provide the final seal and prevent refrigerant leaks if Schrader valve fails.\n"
            "2. Caps prevent dirt, moisture, and debris from entering the service port.\n"
            "3. Always install caps with intact O-rings after service.\n"
            "4. Replace damaged or missing caps immediately.\n"
            "5. Document cap installation in service records.\n"
            "6. Use only OEM-specified caps for correct fit and sealing.\n"
            "7. Educate technicians and owners on importance of caps.\n"
            "8. Leak test service ports after service.\n"
            "9. Aftermarket caps must meet or exceed OEM standards.\n"
            "10. Service port leaks are a common cause of refrigerant loss."
        ),
        key_factors=[
            "Cap integrity",
            "O-ring condition",
            "Leak testing",
            "Contamination prevention",
            "Documentation"
        ],
        primary_authority=[
            "SAE J639",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="Caps are unnecessary if Schrader valves are leak-free.",
        counter_arguments=[
            "Caps provide redundant sealing and contamination protection.",
            "Omission leads to common service port leaks."
        ],
        resolution_strategy="Install and verify all caps after service; document in records.",
        entity_scope="Automotive HVAC systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="A/C System Vacuum Leak Diagnosis",
        keywords=["vacuum leak", "actuator", "mode door", "control", "diagnosis"],
        conclusion_template="Vacuum leaks in HVAC control systems cause mode door malfunction and must be diagnosed with vacuum gauges and smoke testing.",
        reasoning_framework=(
            "1. Many HVAC systems use vacuum actuators for mode door control.\n"
            "2. Leaks in vacuum lines, actuators, or control switches cause loss of control, defaulting to defrost or floor mode.\n"
            "3. Diagnosis involves vacuum gauge testing at various points and smoke testing for leak location.\n"
            "4. Common leak points: cracked hoses, disconnected lines, failed actuators.\n"
            "5. Repair involves replacing damaged components and verifying operation.\n"
            "6. After repair, recalibrate system as required.\n"
            "7. Document all findings and repairs.\n"
            "8. Educate owners on symptoms of vacuum leaks.\n"
            "9. Aftermarket repairs must use vacuum-rated hose.\n"
            "10. Verify all modes function after repair."
        ),
        key_factors=[
            "Vacuum integrity",
            "Actuator function",
            "Leak location",
            "Repair quality",
            "System calibration"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2064"
        ],
        burden_holder="Technician",
        adversary_position="Vacuum leaks are rare and not a common cause of mode door issues.",
        counter_arguments=[
            "Vacuum leaks are a frequent cause of mode door malfunction in older systems.",
            "Diagnosis must include vacuum integrity testing."
        ],
        resolution_strategy="Use vacuum gauges and smoke testing per OEM procedure.",
        entity_scope="Automotive HVAC vacuum control systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="A/C System Pressure Cycling vs. Variable Displacement Control",
        keywords=["pressure cycling", "variable displacement", "compressor control", "efficiency", "system design"],
        conclusion_template="Variable displacement compressors provide superior efficiency and comfort compared to pressure cycling systems, but require more complex control logic.",
        reasoning_framework=(
            "1. Pressure cycling systems use a fixed displacement compressor and cycle clutch engagement based on low-side pressure.\n"
            "2. Variable displacement compressors adjust output to match cooling demand, reducing cycling and improving efficiency.\n"
            "3. Control is achieved via solenoid or mechanical means, managed by the HVAC control module.\n"
            "4. Variable systems provide more stable vent temperatures and lower energy consumption.\n"
            "5. Diagnosis differs: variable systems require scan tool data and solenoid testing.\n"
            "6. System design must match compressor type and control logic.\n"
            "7. Retrofitting from one type to another is complex and not recommended.\n"
            "8. Variable displacement is preferred in modern automatic climate control systems.\n"
            "9. Service procedures must follow OEM guidelines for each system type.\n"
            "10. Educate technicians on differences in diagnosis and repair."
        ),
        key_factors=[
            "Compressor type",
            "Control logic",
            "System efficiency",
            "Diagnosis procedure",
            "Serviceability"
        ],
        primary_authority=[
            "SAE J2064",
            "OEM Service Manuals"
        ],
        burden_holder="System designer/technician",
        adversary_position="Pressure cycling is equally efficient and comfortable.",
        counter_arguments=[
            "Variable displacement offers measurable gains in efficiency and comfort.",
            "System complexity is justified by performance improvements."
        ],
        resolution_strategy="Match system design to application and follow OEM procedures.",
        entity_scope="Automotive HVAC systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2064"
    ),
    DoctrineBlock(
        topic="Cabin Air Recirculation Control",
        keywords=["recirculation", "fresh air", "air quality", "HVAC control", "mode door"],
        conclusion_template="Cabin air recirculation improves cooling efficiency and reduces outside pollutant entry, but must be managed to prevent window fogging and maintain air quality.",
        reasoning_framework=(
            "1. Recirculation mode closes the fresh air intake and recycles cabin air through the HVAC system.\n"
            "2. Cooling efficiency increases as cabin air is already cooled and dried.\n"
            "3. Prolonged recirculation may cause CO2 buildup and window fogging.\n"
            "4. Automatic systems switch between fresh and recirculated air based on sensor input and setpoint.\n"
            "5. Manual systems rely on user selection; educate owners on proper use.\n"
            "6. Recirculation is preferred in high pollution or high temperature conditions.\n"
            "7. Mode door actuator faults may prevent proper operation.\n"
            "8. Diagnosis includes actuator testing and control module logic verification.\n"
            "9. After repair, verify all modes function as designed.\n"
            "10. Document findings and educate owners on recirculation use."
        ),
        key_factors=[
            "Control logic",
            "Actuator function",
            "Air quality",
            "Window fogging",
            "Owner education"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "ASHRAE Fundamentals Handbook"
        ],
        burden_holder="Technician/vehicle owner",
        adversary_position="Recirculation should be used at all times for maximum cooling.",
        counter_arguments=[
            "Continuous recirculation degrades air quality and causes fogging.",
            "Proper management balances efficiency and occupant health."
        ],
        resolution_strategy="Educate owners and verify system function after repair.",
        entity_scope="Automotive HVAC systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="A/C System Control Module Software Updates",
        keywords=["control module", "software update", "reflash", "HVAC", "diagnosis"],
        conclusion_template="HVAC control module software updates resolve operational issues and improve system performance; always verify latest calibration during diagnosis.",
        reasoning_framework=(
            "1. Control module software governs HVAC operation, including actuator control and fault detection.\n"
            "2. OEMs release software updates to address bugs, improve performance, or add features.\n"
            "3. Symptoms of outdated software include erratic operation, incorrect temperature, or fault codes.\n"
            "4. Diagnosis involves checking calibration level with a scan tool.\n"
            "5. Reflash procedures require OEM-approved tools and software.\n"
            "6. Always document software version before and after update.\n"
            "7. Some updates require system recalibration or actuator initialization.\n"
            "8. Educate owners on benefits of software updates.\n"
            "9. Verify system operation after update.\n"
            "10. Follow OEM guidelines for all software updates."
        ),
        key_factors=[
            "Software version",
            "Update procedure",
            "Calibration",
            "Scan tool use",
            "Owner education"
        ],
        primary_authority=[
            "OEM Service Manuals",
            "SAE J2534"
        ],
        burden_holder="Technician",
        adversary_position="Software updates are unnecessary if no fault codes are present.",
        counter_arguments=[
            "Updates may resolve issues not indicated by fault codes.",
            "OEMs recommend updates for optimal system performance."
        ],
        resolution_strategy="Check for and install latest software during diagnosis.",
        entity_scope="Automotive HVAC control modules",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Service Manuals"
    ),
    DoctrineBlock(
        topic="A/C System High Side Service Precautions",
        keywords=["high side", "service", "pressure", "safety", "precaution"],
        conclusion_template="High side service requires strict safety precautions due to elevated pressures; always depressurize and wear protective equipment.",
        reasoning_framework=(
            "1. High side pressures can exceed 300 psi under normal operation.\n"
            "2. Service must only be performed with system off and pressure relieved.\n"
            "3. Always wear eye and hand protection when connecting/disconnecting service equipment.\n"
            "4. Use only approved, pressure-rated hoses and gauges.\n"
            "5. Never open high side fittings with system charged and running.\n"
            "6. Document all service operations and safety checks.\n"
            "7. Educate technicians on high side hazards.\n"
            "8. Replace any damaged high side fittings or hoses immediately.\n"
            "9. Verify system integrity after service.\n"
            "10. Follow OEM and SAE safety guidelines at all times."
        ),
        key_factors=[
            "Pressure rating",
            "Protective equipment",
            "Service procedure",
            "Documentation",
            "Technician training"
        ],
        primary_authority=[
            "SAE J639",
            "OEM Service Manuals"
        ],
        burden_holder="Technician",
        adversary_position="High side service is no more dangerous than low side.",
        counter_arguments=[
            "High side pressures are significantly greater and pose higher risk.",
            "Strict precautions are required for safety."
        ],
        resolution_strategy="Follow all safety procedures and use proper equipment.",
        entity_scope="Automotive HVAC systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="SAE J639"
    ),
    DoctrineBlock(
        topic="A/C System Moisture Ingress Prevention",
        keywords=["moisture ingress", "vacuum", "evacuation", "leak", "system opening"],
        conclusion_template="Moisture ingress is prevented by minimizing system exposure, performing thorough evacuation, and replacing desiccant after opening.",
        reasoning_framework=(
            "1. Moisture enters the system during component replacement or leak events.\n"
            "2. Moisture reacts with refrigerant to form acids, causing corrosion and failure.\n"
            "3. Minimize open time by preparing all parts and tools before opening system.\n"
            "4. Perform vacuum evacuation for at least 30 minutes to remove air and moisture.\n"
            "5. Replace accumulator or receiver-drier/desiccant after any system opening.\n"
            "6. Verify vacuum holds for specified time to confirm leak-free system.\n"
            "7. Use only approved vacuum pumps and gauges.\n"
            "8. Document evacuation time and vacuum level in service records.\n"
            "9. Educate technicians on importance of moisture prevention.\n"
            "10. Verify system performance after service."
        ),
        key_factors=[
            "Evacuation procedure",
            "Desiccant replacement",
            "System exposure time",
            "Vacuum hold test",
            "Documentation