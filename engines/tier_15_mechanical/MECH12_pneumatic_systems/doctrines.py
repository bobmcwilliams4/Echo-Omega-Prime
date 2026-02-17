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
        topic="Reciprocating Compressor Selection and Sizing",
        keywords=[
            "reciprocating compressor", "sizing", "selection", "capacity", "pressure", "duty cycle", "CFM", "horsepower"
        ],
        conclusion_template="Select a reciprocating compressor with a rated capacity and pressure that meets or exceeds the system's maximum demand, factoring in duty cycle and ambient conditions.",
        reasoning_framework="""
        1. Determine the system's maximum air demand (CFM) and required pressure (PSIG).
        2. Assess duty cycle requirements (continuous vs intermittent operation).
        3. Apply safety margin (typically 10-20%) to calculated demand.
        4. Evaluate ambient temperature and altitude for derating.
        5. Compare compressor performance curves and manufacturer data.
        6. Consider energy efficiency (specific power, kW/100CFM).
        7. Factor in maintenance intervals and expected service life.
        8. Ensure compliance with applicable standards (ISO 1217, CAGI).
        9. Review installation footprint, noise, and vibration constraints.
        10. Select model that best fits technical and operational needs.
        """,
        key_factors=[
            "System air demand (CFM)", "Required pressure (PSIG)", "Duty cycle", "Ambient conditions", "Safety margin", "Compressor efficiency", "Maintenance requirements"
        ],
        primary_authority=[
            "ISO 1217", "CAGI Data Sheets", "OEM Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Oversizing or undersizing compressors leads to inefficiency or inadequate supply.",
        counter_arguments=[
            "Oversizing increases capital and operating costs.",
            "Undersizing risks pressure drops and equipment malfunction."
        ],
        resolution_strategy="Apply demand analysis, consult authoritative data, and validate with simulation or field data.",
        entity_scope="Industrial pneumatic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 1217 Annex C"
    ),

    DoctrineBlock(
        topic="Rotary Screw Compressor Design and Application",
        keywords=[
            "rotary screw", "compressor", "design", "application", "oil-injected", "oil-free", "continuous duty"
        ],
        conclusion_template="Apply rotary screw compressors for continuous-duty, high-capacity applications where stable pressure and efficiency are required.",
        reasoning_framework="""
        1. Identify application duty cycle and air demand profile.
        2. Evaluate oil-injected vs oil-free design based on air quality needs.
        3. Assess energy efficiency (specific power, part-load performance).
        4. Consider variable speed drive (VSD) options for fluctuating demand.
        5. Review maintenance requirements and service intervals.
        6. Ensure compatibility with downstream air treatment equipment.
        7. Evaluate noise, vibration, and installation constraints.
        8. Reference ISO 8573-1 for air quality class.
        9. Consult OEM performance data and CAGI datasheets.
        10. Select configuration that aligns with operational and regulatory needs.
        """,
        key_factors=[
            "Duty cycle", "Air demand profile", "Air quality requirements", "Energy efficiency", "Maintenance", "Installation constraints"
        ],
        primary_authority=[
            "ISO 8573-1", "CAGI", "OEM Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Reciprocating compressors are sufficient for all applications.",
        counter_arguments=[
            "Reciprocating compressors have higher maintenance at high duty cycles.",
            "Rotary screw compressors offer better efficiency and reliability for continuous operation."
        ],
        resolution_strategy="Match compressor type to application profile and air quality needs.",
        entity_scope="Industrial and commercial pneumatic systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="CAGI Performance Verification Program"
    ),

    DoctrineBlock(
        topic="Air Receiver Tank Sizing and Pressure Stabilization",
        keywords=[
            "air receiver", "tank sizing", "pressure stabilization", "storage", "buffer", "compressor cycling"
        ],
        conclusion_template="Size air receiver tanks to provide adequate storage for pressure stabilization, compressor cycling reduction, and transient demand events.",
        reasoning_framework="""
        1. Calculate required storage volume using the formula: V = (Q x t x Pa) / (P1 - P2), where Q = flow rate, t = time, Pa = atmospheric pressure, P1 = max pressure, P2 = min pressure.
        2. Consider compressor type and control strategy (load/unload, start/stop, VSD).
        3. Account for peak demand events and desired pressure stability.
        4. Reference best practice: 1 gal per CFM for reciprocating, 2-4 gal per CFM for rotary screw.
        5. Evaluate receiver placement (wet vs dry side).
        6. Ensure compliance with ASME Section VIII and local codes.
        7. Factor in drain requirements and corrosion protection.
        8. Validate sizing with simulation or operational data.
        """,
        key_factors=[
            "System flow rate", "Pressure fluctuation tolerance", "Compressor control type", "Peak demand events", "Receiver location"
        ],
        primary_authority=[
            "ASME Section VIII", "CAGI", "OEM Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Minimal storage is sufficient for all systems.",
        counter_arguments=[
            "Insufficient storage causes pressure swings and frequent compressor cycling.",
            "Oversized tanks increase cost and footprint."
        ],
        resolution_strategy="Apply sizing formula, reference best practices, and validate with operational needs.",
        entity_scope="Compressed air systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII"
    ),

    DoctrineBlock(
        topic="Compressed Air Dryer Selection - Refrigerated vs Desiccant",
        keywords=[
            "air dryer", "refrigerated", "desiccant", "dew point", "moisture removal", "air quality"
        ],
        conclusion_template="Select refrigerated dryers for general industrial use (dew point ~35-50°F), and desiccant dryers for critical applications requiring low dew points (-40°F or lower).",
        reasoning_framework="""
        1. Determine required dew point based on application and ISO 8573-1 class.
        2. Assess ambient temperature and installation environment.
        3. Evaluate air flow rate and pressure.
        4. Compare refrigerated dryer (energy efficient, moderate dew point) vs desiccant dryer (low dew point, higher energy use).
        5. Consider purge air requirements for desiccant dryers.
        6. Factor in maintenance needs and operational costs.
        7. Review OEM performance data and warranty.
        8. Ensure compatibility with compressor and downstream equipment.
        9. Validate selection with air quality monitoring.
        """,
        key_factors=[
            "Required dew point", "Ambient temperature", "Air flow rate", "Energy consumption", "Maintenance"
        ],
        primary_authority=[
            "ISO 8573-1", "OEM Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Refrigerated dryers are sufficient for all applications.",
        counter_arguments=[
            "Critical processes (e.g., instrumentation, painting) require lower dew points.",
            "Desiccant dryers have higher operating costs but provide lower dew points."
        ],
        resolution_strategy="Match dryer type to dew point requirement and operational context.",
        entity_scope="Industrial pneumatic systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 8573-1"
    ),

    DoctrineBlock(
        topic="Pneumatic Cylinder Force and Sizing Calculations",
        keywords=[
            "pneumatic cylinder", "force calculation", "sizing", "bore", "stroke", "pressure", "load"
        ],
        conclusion_template="Size pneumatic cylinders by calculating required bore and stroke to deliver the necessary force at available pressure, accounting for load, friction, and safety margin.",
        reasoning_framework="""
        1. Calculate required force: F = P x A, where P = effective pressure, A = piston area.
        2. Determine load to be moved, including friction and acceleration.
        3. Apply safety margin (typically 20-50%).
        4. Select bore size to provide required force at available pressure.
        5. Determine stroke length based on application travel.
        6. Evaluate mounting style and side load conditions.
        7. Consider speed requirements and air consumption.
        8. Reference ISO 6431 for cylinder dimensions.
        9. Validate with prototype or simulation if possible.
        """,
        key_factors=[
            "Required force", "Available pressure", "Load characteristics", "Friction", "Stroke length", "Safety margin"
        ],
        primary_authority=[
            "ISO 6431", "OEM Cylinder Catalogs"
        ],
        burden_holder="Machine designer",
        adversary_position="Standard cylinder sizes are always sufficient.",
        counter_arguments=[
            "Incorrect sizing leads to poor performance or premature wear.",
            "Oversizing increases air consumption and costs."
        ],
        resolution_strategy="Perform detailed force calculations and validate with application data.",
        entity_scope="Pneumatic actuator systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ISO 6431"
    ),

    DoctrineBlock(
        topic="Directional Control Valve Selection - 3/2, 5/2, 5/3 Configurations",
        keywords=[
            "directional control valve", "3/2 valve", "5/2 valve", "5/3 valve", "actuator control", "valve selection"
        ],
        conclusion_template="Select directional control valves based on actuator type, required positions, and control logic, referencing 3/2 for single-acting and 5/2 or 5/3 for double-acting cylinders.",
        reasoning_framework="""
        1. Identify actuator type (single-acting or double-acting).
        2. Determine number of required positions (2 or 3).
        3. Select 3/2 valve for single-acting, 5/2 or 5/3 for double-acting cylinders.
        4. Evaluate valve actuation method (manual, solenoid, pneumatic).
        5. Assess flow capacity (Cv) and response time.
        6. Consider fail-safe and center position requirements (open, closed, pressure held).
        7. Review mounting and porting options.
        8. Reference ISO 5599-1 for valve interface standards.
        9. Validate selection with circuit simulation or prototyping.
        """,
        key_factors=[
            "Actuator type", "Required positions", "Flow capacity", "Actuation method", "Fail-safe requirements"
        ],
        primary_authority=[
            "ISO 5599-1", "OEM Valve Catalogs"
        ],
        burden_holder="System integrator",
        adversary_position="Any valve configuration can be used for any actuator.",
        counter_arguments=[
            "Incorrect valve selection leads to malfunction or safety risks.",
            "Over-specification increases cost and complexity."
        ],
        resolution_strategy="Match valve configuration to actuator and control logic requirements.",
        entity_scope="Pneumatic control systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 5599-1"
    ),

    DoctrineBlock(
        topic="Pneumatic Flow Control - Meter-In vs Meter-Out",
        keywords=[
            "flow control", "meter-in", "meter-out", "speed control", "cylinder", "exhaust flow"
        ],
        conclusion_template="Apply meter-in flow control for load-induced extension and meter-out for load-induced retraction or to prevent cylinder run-away.",
        reasoning_framework="""
        1. Identify direction of load and motion (extension or retraction).
        2. Use meter-in for controlling speed when load assists extension.
        3. Use meter-out for controlling speed when load assists retraction or to prevent over-speed.
        4. Evaluate risk of cylinder run-away or instability.
        5. Consider air cushioning and end-of-stroke deceleration.
        6. Reference ISO 4414 for safety and control recommendations.
        7. Validate with circuit simulation or field testing.
        """,
        key_factors=[
            "Load direction", "Motion type", "Risk of run-away", "Speed control precision"
        ],
        primary_authority=[
            "ISO 4414", "OEM Application Notes"
        ],
        burden_holder="System designer",
        adversary_position="Either flow control method is always acceptable.",
        counter_arguments=[
            "Incorrect flow control can cause unsafe operation or damage.",
            "Proper method depends on load and motion direction."
        ],
        resolution_strategy="Analyze load and motion, apply appropriate flow control method.",
        entity_scope="Pneumatic actuator circuits",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 4414"
    ),

    DoctrineBlock(
        topic="Vacuum Generation - Ejector vs Mechanical Pump Selection",
        keywords=[
            "vacuum generation", "ejector", "mechanical pump", "vacuum level", "response time", "energy efficiency"
        ],
        conclusion_template="Select ejectors for rapid, intermittent vacuum with low to moderate flow; use mechanical pumps for continuous, high-flow or deep vacuum applications.",
        reasoning_framework="""
        1. Define required vacuum level and flow rate.
        2. Assess duty cycle (intermittent vs continuous).
        3. Ejectors are suitable for short, rapid cycles and decentralized systems.
        4. Mechanical pumps are preferred for sustained, high-flow or deep vacuum.
        5. Evaluate energy consumption and maintenance requirements.
        6. Consider noise, footprint, and installation constraints.
        7. Reference ISO 8573-1 for air quality if using ejectors.
        8. Validate with application-specific performance data.
        """,
        key_factors=[
            "Vacuum level", "Flow rate", "Duty cycle", "Energy efficiency", "Maintenance"
        ],
        primary_authority=[
            "OEM Vacuum Equipment Manuals", "ISO 8573-1"
        ],
        burden_holder="System designer",
        adversary_position="Ejectors are always preferable due to simplicity.",
        counter_arguments=[
            "Ejectors consume more compressed air and are less efficient for continuous use.",
            "Mechanical pumps offer better performance for sustained vacuum."
        ],
        resolution_strategy="Match vacuum generation method to application profile and efficiency needs.",
        entity_scope="Pneumatic and vacuum systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Application Guidelines"
    ),

    DoctrineBlock(
        topic="Compressed Air Quality per ISO 8573-1 Classification",
        keywords=[
            "air quality", "ISO 8573-1", "particulate", "moisture", "oil", "classification", "contaminant"
        ],
        conclusion_template="Classify and specify compressed air quality according to ISO 8573-1, defining limits for particulate, water, and oil content based on application requirements.",
        reasoning_framework="""
        1. Identify application-specific air quality requirements.
        2. Reference ISO 8573-1 to select appropriate class for particulate, water, and oil.
        3. Specify filtration, drying, and oil removal equipment to meet class limits.
        4. Validate air quality with periodic testing and monitoring.
        5. Document air quality class in system specifications and maintenance plans.
        6. Upgrade treatment equipment if class is not met.
        """,
        key_factors=[
            "Application requirements", "ISO 8573-1 class", "Filtration and drying", "Monitoring"
        ],
        primary_authority=[
            "ISO 8573-1", "OEM Manuals"
        ],
        burden_holder="System owner",
        adversary_position="Basic filtration is sufficient for all applications.",
        counter_arguments=[
            "Sensitive equipment or processes require higher air quality.",
            "Non-compliance can cause product defects or equipment failure."
        ],
        resolution_strategy="Specify and monitor air quality class per ISO 8573-1.",
        entity_scope="All compressed air systems",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ISO 8573-1"
    ),

    DoctrineBlock(
        topic="Compressed Air Energy Audit and Specific Power Analysis",
        keywords=[
            "energy audit", "specific power", "kW/100CFM", "efficiency", "compressed air cost", "leakage"
        ],
        conclusion_template="Conduct periodic energy audits and analyze specific power (kW/100CFM) to identify inefficiencies and optimize compressed air system performance.",
        reasoning_framework="""
        1. Measure compressor power consumption and delivered air flow.
        2. Calculate specific power (kW/100CFM) for each compressor.
        3. Benchmark against industry best practices and OEM data.
        4. Identify sources of inefficiency (leaks, inappropriate pressure, poor controls).
        5. Quantify energy cost of compressed air production.
        6. Recommend corrective actions (leak repair, pressure reduction, VSD retrofit).
        7. Track improvements over time and repeat audit annually.
        """,
        key_factors=[
            "Power consumption", "Delivered air flow", "System leaks", "Control strategy", "Benchmark data"
        ],
        primary_authority=[
            "DOE Compressed Air Challenge", "CAGI", "ISO 11011"
        ],
        burden_holder="Facility manager",
        adversary_position="Compressed air energy use is unavoidable and cannot be improved.",
        counter_arguments=[
            "Significant savings are achievable through audits and targeted improvements.",
            "Specific power is a key metric for system efficiency."
        ],
        resolution_strategy="Implement regular audits and continuous improvement.",
        entity_scope="Industrial compressed air systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 11011"
    ),

    DoctrineBlock(
        topic="Compressed Air Leak Detection and Management Program",
        keywords=[
            "leak detection", "compressed air loss", "ultrasonic detector", "maintenance", "energy savings"
        ],
        conclusion_template="Implement a proactive leak detection and management program using ultrasonic detectors and scheduled maintenance to minimize compressed air losses.",
        reasoning_framework="""
        1. Survey system regularly for leaks using ultrasonic or acoustic detection.
        2. Quantify leak rate and prioritize largest leaks for repair.
        3. Document findings and corrective actions.
        4. Train maintenance staff in leak detection and repair techniques.
        5. Integrate leak management into preventive maintenance schedule.
        6. Track leak rate reduction and cost savings over time.
        7. Reference best practices from DOE and CAGI.
        """,
        key_factors=[
            "Leak rate", "Detection method", "Maintenance schedule", "Staff training", "Cost savings"
        ],
        primary_authority=[
            "DOE Compressed Air Challenge", "CAGI"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Leaks are inevitable and not worth addressing.",
        counter_arguments=[
            "Leaks can account for 20-30% of total air consumption.",
            "Leak repair is often low-cost with rapid payback."
        ],
        resolution_strategy="Establish ongoing leak detection and repair program.",
        entity_scope="All compressed air systems",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="DOE Compressed Air Challenge"
    ),

    DoctrineBlock(
        topic="Pneumatic Logic Circuits and Sequential Control",
        keywords=[
            "pneumatic logic", "sequential control", "AND/OR valve", "memory valve", "circuit design"
        ],
        conclusion_template="Design pneumatic logic circuits using standard logic elements (AND, OR, NOT, memory) to achieve required sequential control without electrical components.",
        reasoning_framework="""
        1. Define required sequence of operations and logic conditions.
        2. Select appropriate pneumatic logic elements (AND, OR, NOT, memory valves).
        3. Lay out circuit diagram to implement sequence.
        4. Validate timing and response with simulation or prototype.
        5. Ensure fail-safe operation and compliance with ISO 4414.
        6. Document logic and provide operator training.
        """,
        key_factors=[
            "Sequence requirements", "Logic element selection", "Timing", "Fail-safe design"
        ],
        primary_authority=[
            "ISO 4414", "OEM Application Notes"
        ],
        burden_holder="Control system designer",
        adversary_position="Electrical control is always preferable.",
        counter_arguments=[
            "Pneumatic logic is robust in hazardous or simple environments.",
            "Electrical control may not be feasible in all cases."
        ],
        resolution_strategy="Select control method based on environment and requirements.",
        entity_scope="Pneumatic automation systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 4414"
    ),

    DoctrineBlock(
        topic="Vacuum Cup Gripper Design and Suction Force Calculation",
        keywords=[
            "vacuum cup", "gripper", "suction force", "lifting", "safety factor", "surface condition"
        ],
        conclusion_template="Calculate vacuum cup suction force as F = A x (P_atm - P_vac), apply safety factor, and select cup type based on surface and load.",
        reasoning_framework="""
        1. Determine required lifting force based on load weight and orientation.
        2. Calculate suction force: F = A x (P_atm - P_vac), where A = cup area, P_atm = atmospheric pressure, P_vac = vacuum level.
        3. Apply safety factor (typically 2-3x).
        4. Select cup material and shape for surface condition (smooth, rough, porous).
        5. Evaluate number and arrangement of cups for load stability.
        6. Reference ISO 8573-1 for air quality to prevent cup contamination.
        7. Validate design with prototype or simulation.
        """,
        key_factors=[
            "Load weight", "Vacuum level", "Cup area", "Surface condition", "Safety factor"
        ],
        primary_authority=[
            "OEM Vacuum Cup Catalogs", "ISO 8573-1"
        ],
        burden_holder="End effector designer",
        adversary_position="Any cup size or shape can be used for any load.",
        counter_arguments=[
            "Incorrect cup selection risks dropping the load.",
            "Surface condition affects achievable suction force."
        ],
        resolution_strategy="Perform force calculations and select cups for application.",
        entity_scope="Pneumatic gripping systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OEM Vacuum Cup Guidelines"
    ),

    DoctrineBlock(
        topic="Pneumatic Pipe Sizing and Pressure Drop Calculation",
        keywords=[
            "pipe sizing", "pressure drop", "air velocity", "friction loss", "distribution piping"
        ],
        conclusion_template="Size pneumatic pipes to maintain air velocity below 20-30 ft/s and limit pressure drop to less than 5% of supply pressure over the distribution system.",
        reasoning_framework="""
        1. Calculate system flow rate and required pipe length.
        2. Select pipe diameter to keep air velocity below 20-30 ft/s.
        3. Use pressure drop charts or Darcy-Weisbach equation to estimate losses.
        4. Minimize bends, fittings, and restrictions.
        5. Consider future expansion and redundancy.
        6. Reference ISO 4414 and ASME B31.3 for design standards.
        7. Validate sizing with simulation or field measurement.
        """,
        key_factors=[
            "Flow rate", "Pipe length", "Air velocity", "Pressure drop", "Fittings and bends"
        ],
        primary_authority=[
            "ISO 4414", "ASME B31.3", "OEM Pipe Sizing Charts"
        ],
        burden_holder="System designer",
        adversary_position="Smaller pipes are always more cost-effective.",
        counter_arguments=[
            "Undersized pipes cause excessive pressure drop and energy loss.",
            "Oversized pipes increase cost and may cause condensation issues."
        ],
        resolution_strategy="Apply sizing calculations and reference standards.",
        entity_scope="Compressed air distribution systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 4414"
    ),

    DoctrineBlock(
        topic="OSHA Compressed Air Safety - 29 CFR 1910.242 and 1910.169",
        keywords=[
            "OSHA", "compressed air safety", "29 CFR 1910.242", "29 CFR 1910.169", "nozzle pressure", "equipment inspection"
        ],
        conclusion_template="Ensure all compressed air systems comply with OSHA 29 CFR 1910.242 and 1910.169, including nozzle pressure limits and regular equipment inspection.",
        reasoning_framework="""
        1. Limit compressed air used for cleaning to 30 PSIG when used with effective chip guarding.
        2. Inspect pressure vessels regularly for integrity and safety valve function.
        3. Maintain records of inspections and repairs.
        4. Train personnel in safe use of compressed air equipment.
        5. Reference OSHA guidelines for permissible practices.
        6. Address violations promptly to avoid penalties.
        """,
        key_factors=[
            "Nozzle pressure", "Inspection frequency", "Training", "Recordkeeping"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.242", "OSHA 29 CFR 1910.169"
        ],
        burden_holder="Facility safety officer",
        adversary_position="Higher pressures are acceptable if used briefly.",
        counter_arguments=[
            "Exceeding pressure limits increases risk of injury.",
            "Non-compliance may result in regulatory penalties."
        ],
        resolution_strategy="Implement OSHA-compliant procedures and training.",
        entity_scope="All compressed air systems in regulated workplaces",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="OSHA 29 CFR 1910.242"
    ),

    DoctrineBlock(
        topic="ISO 4414 Pneumatic System Design Rules and Safety",
        keywords=[
            "ISO 4414", "pneumatic system safety", "design rules", "fail-safe", "energy isolation"
        ],
        conclusion_template="Design pneumatic systems in accordance with ISO 4414, incorporating fail-safe features, energy isolation, and risk assessment.",
        reasoning_framework="""
        1. Conduct risk assessment for all pneumatic circuits.
        2. Incorporate energy isolation devices (lockout/tagout).
        3. Design for fail-safe operation in event of power or air loss.
        4. Provide pressure relief and exhaust paths.
        5. Use components rated for maximum system pressure.
        6. Document safety features and provide operator training.
        7. Reference ISO 4414 for detailed requirements.
        """,
        key_factors=[
            "Risk assessment", "Fail-safe design", "Energy isolation", "Component ratings"
        ],
        primary_authority=[
            "ISO 4414", "OEM Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Safety features are optional if system is simple.",
        counter_arguments=[
            "Lack of safety features increases risk of injury or damage.",
            "ISO 4414 compliance is often required by law or contract."
        ],
        resolution_strategy="Design and document systems per ISO 4414.",
        entity_scope="All pneumatic systems",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ISO 4414"
    ),

    DoctrineBlock(
        topic="Heat Recovery from Compressed Air Systems",
        keywords=[
            "heat recovery", "compressed air", "energy efficiency", "waste heat", "hot water"
        ],
        conclusion_template="Implement heat recovery systems to capture waste heat from compressors for space heating or process use, improving overall energy efficiency.",
        reasoning_framework="""
        1. Quantify waste heat available from compressor cooling system.
        2. Identify potential uses (space heating, water heating, process heat).
        3. Evaluate technical and economic feasibility.
        4. Integrate heat exchangers and controls as needed.
        5. Monitor recovered energy and track savings.
        6. Reference DOE and CAGI best practices.
        """,
        key_factors=[
            "Waste heat quantity", "Potential uses", "System integration", "Economic analysis"
        ],
        primary_authority=[
            "DOE Compressed Air Challenge", "CAGI"
        ],
        burden_holder="Facility energy manager",
        adversary_position="Heat recovery is too complex or costly.",
        counter_arguments=[
            "Up to 90% of compressor input energy is converted to heat.",
            "Heat recovery can provide rapid payback in many facilities."
        ],
        resolution_strategy="Perform feasibility study and implement where justified.",
        entity_scope="Industrial compressed air systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="DOE Compressed Air Challenge"
    ),

    DoctrineBlock(
        topic="Variable Speed Drive (VSD) Compressor Energy Savings",
        keywords=[
            "variable speed drive", "VSD", "compressor", "energy savings", "part-load efficiency"
        ],
        conclusion_template="Use VSD compressors to match air supply to demand, reducing energy consumption during part-load operation.",
        reasoning_framework="""
        1. Analyze air demand profile for variability.
        2. Compare fixed speed vs VSD compressor efficiency at part-load.
        3. Calculate potential energy savings using load profile data.
        4. Evaluate control integration and compatibility.
        5. Reference CAGI and DOE case studies.
        6. Monitor performance post-installation.
        """,
        key_factors=[
            "Demand variability", "Part-load efficiency", "Control integration", "Energy savings"
        ],
        primary_authority=[
            "CAGI", "DOE Compressed Air Challenge"
        ],
        burden_holder="Facility energy manager",
        adversary_position="VSDs add unnecessary complexity and cost.",
        counter_arguments=[
            "VSDs provide significant savings in systems with variable demand.",
            "Payback period is often less than 2 years."
        ],
        resolution_strategy="Apply VSD where demand profile justifies investment.",
        entity_scope="Industrial compressed air systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CAGI VSD Compressor Guidelines"
    ),

    DoctrineBlock(
        topic="Altitude Derating of Compressors and Pneumatic Equipment",
        keywords=[
            "altitude derating", "compressor", "pneumatic equipment", "air density", "performance"
        ],
        conclusion_template="Apply altitude derating factors to compressor and pneumatic equipment sizing above 1000 meters to account for reduced air density.",
        reasoning_framework="""
        1. Identify installation altitude above sea level.
        2. Reference OEM derating tables or calculate correction factor.
        3. Adjust compressor output and pneumatic actuator sizing accordingly.
        4. Validate system performance at reduced air density.
        5. Document derating in system specifications.
        """,
        key_factors=[
            "Installation altitude", "OEM derating factor", "Air density", "Equipment sizing"
        ],
        primary_authority=[
            "OEM Manuals", "ASHRAE Fundamentals"
        ],
        burden_holder="System designer",
        adversary_position="Altitude has negligible effect on performance.",
        counter_arguments=[
            "Reduced air density lowers compressor output and actuator force.",
            "Ignoring derating risks undersized equipment."
        ],
        resolution_strategy="Apply derating per OEM or ASHRAE guidance.",
        entity_scope="High-altitude pneumatic systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OEM Altitude Derating Tables"
    ),

    DoctrineBlock(
        topic="Filter-Regulator-Lubricator (FRL) Unit Selection and Maintenance",
        keywords=[
            "FRL", "filter", "regulator", "lubricator", "maintenance", "air preparation"
        ],
        conclusion_template="Select and maintain FRL units appropriate for system flow, pressure, and air quality requirements, ensuring regular inspection and servicing.",
        reasoning_framework="""
        1. Determine required flow rate and pressure for downstream equipment.
        2. Select filter element to achieve required particulate and moisture removal.
        3. Set regulator to maintain stable pressure within equipment limits.
        4. Use lubricator only if required by downstream components.
        5. Schedule regular inspection and element replacement.
        6. Reference ISO 8573-1 for air quality targets.
        7. Document maintenance procedures and intervals.
        """,
        key_factors=[
            "Flow rate", "Pressure", "Air quality", "Maintenance interval"
        ],
        primary_authority=[
            "ISO 8573-1", "OEM FRL Manuals"
        ],
        burden_holder="Maintenance technician",
        adversary_position="FRL maintenance is unnecessary if air is clean.",
        counter_arguments=[
            "Neglected FRLs cause pressure drop and equipment damage.",
            "Proper maintenance ensures system reliability."
        ],
        resolution_strategy="Select FRL for application and maintain per schedule.",
        entity_scope="All pneumatic systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OEM FRL Maintenance Guidelines"
    ),

    # Additional doctrines for comprehensive coverage (20+ more for 40+ total):

    DoctrineBlock(
        topic="Pressure Regulator Selection and Sizing",
        keywords=[
            "pressure regulator", "sizing", "setpoint", "flow capacity", "droop"
        ],
        conclusion_template="Select pressure regulators with adequate flow capacity and minimal droop to maintain stable downstream pressure under varying loads.",
        reasoning_framework="""
        1. Determine required downstream pressure setpoint.
        2. Calculate maximum and minimum flow rates.
        3. Select regulator with flow capacity exceeding peak demand.
        4. Evaluate droop characteristics from manufacturer data.
        5. Consider response time and sensitivity.
        6. Reference ISO 6953 for regulator performance.
        7. Validate selection with application testing.
        """,
        key_factors=[
            "Setpoint pressure", "Flow capacity", "Droop", "Response time"
        ],
        primary_authority=[
            "ISO 6953", "OEM Regulator Catalogs"
        ],
        burden_holder="System designer",
        adversary_position="Any regulator can maintain pressure under all loads.",
        counter_arguments=[
            "Undersized regulators cause pressure fluctuations.",
            "Oversized regulators may be less responsive."
        ],
        resolution_strategy="Match regulator to load and performance requirements.",
        entity_scope="Pneumatic distribution systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 6953"
    ),

    DoctrineBlock(
        topic="Quick Exhaust Valve Application in Pneumatic Circuits",
        keywords=[
            "quick exhaust valve", "cylinder speed", "exhaust flow", "cycle time"
        ],
        conclusion_template="Use quick exhaust valves to increase cylinder speed by providing a direct exhaust path, reducing cycle time.",
        reasoning_framework="""
        1. Identify applications requiring rapid cylinder movement.
        2. Install quick exhaust valve at cylinder port to bypass control valve exhaust path.
        3. Ensure valve flow capacity matches cylinder size.
        4. Validate improvement in cycle time and system response.
        5. Reference OEM application notes for best practices.
        """,
        key_factors=[
            "Cylinder size", "Required speed", "Valve flow capacity", "Installation location"
        ],
        primary_authority=[
            "OEM Valve Catalogs"
        ],
        burden_holder="System designer",
        adversary_position="Quick exhaust valves are unnecessary with large control valves.",
        counter_arguments=[
            "Control valve exhaust paths may be restrictive.",
            "Quick exhaust valves provide direct, high-flow exhaust."
        ],
        resolution_strategy="Apply quick exhaust valves where speed is critical.",
        entity_scope="Pneumatic actuator systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="OEM Application Notes"
    ),

    DoctrineBlock(
        topic="Double-Acting vs Single-Acting Cylinder Selection",
        keywords=[
            "double-acting cylinder", "single-acting cylinder", "actuator selection", "return spring"
        ],
        conclusion_template="Select double-acting cylinders for bidirectional force and control; use single-acting cylinders for simple return applications.",
        reasoning_framework="""
        1. Define motion requirements (one-way or two-way force).
        2. Use double-acting for applications requiring force in both directions.
        3. Use single-acting for simple extend/retract with spring return.
        4. Evaluate air consumption and control complexity.
        5. Reference ISO 6431 for cylinder selection.
        """,
        key_factors=[
            "Motion requirements", "Force direction", "Air consumption", "Control complexity"
        ],
        primary_authority=[
            "ISO 6431", "OEM Cylinder Catalogs"
        ],
        burden_holder="System designer",
        adversary_position="Single-acting cylinders are always sufficient.",
        counter_arguments=[
            "Double-acting cylinders provide greater control and force.",
            "Single-acting cylinders are limited to simple tasks."
        ],
        resolution_strategy="Match cylinder type to application needs.",
        entity_scope="Pneumatic actuator systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 6431"
    ),

    DoctrineBlock(
        topic="Check Valve Placement in Pneumatic Systems",
        keywords=[
            "check valve", "non-return valve", "placement", "backflow prevention"
        ],
        conclusion_template="Install check valves to prevent backflow and protect compressors and sensitive equipment in multi-compressor or branched systems.",
        reasoning_framework="""
        1. Identify points where backflow could damage equipment or cause cross-feed.
        2. Install check valves at compressor outlets and branch lines as needed.
        3. Select valve type (spring-loaded, pilot-operated) for application.
        4. Validate proper operation and minimal pressure drop.
        5. Reference OEM and ISO guidelines for placement.
        """,
        key_factors=[
            "Backflow risk", "System configuration", "Valve type", "Pressure drop"
        ],
        primary_authority=[
            "ISO 4414", "OEM Valve Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Check valves are unnecessary in single-compressor systems.",
        counter_arguments=[
            "Multi-compressor or branched systems require backflow prevention.",
            "Omitting check valves risks equipment damage."
        ],
        resolution_strategy="Install check valves per system configuration.",
        entity_scope="Compressed air distribution systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISO 4414"
    ),

    DoctrineBlock(
        topic="Blow Gun and Air Nozzle Safety Compliance",
        keywords=[
            "blow gun", "air nozzle", "safety", "OSHA", "chip guard"
        ],
        conclusion_template="Ensure all blow guns and air nozzles comply with OSHA pressure and chip guard requirements to prevent injury.",
        reasoning_framework="""
        1. Limit nozzle pressure to 30 PSIG when used for cleaning.
        2. Equip nozzles with effective chip guarding.
        3. Train users on safe operation and PPE use.
        4. Inspect nozzles regularly for damage or modification.
        5. Reference OSHA 29 CFR 1910.242(b) for compliance.
        """,
        key_factors=[
            "Nozzle pressure", "Chip guard", "Training", "Inspection"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.242(b)"
        ],
        burden_holder="Facility safety officer",
        adversary_position="Higher pressures are acceptable for stubborn debris.",
        counter_arguments=[
            "Excessive pressure increases injury risk.",
            "Non-compliance may result in fines."
        ],
        resolution_strategy="Specify and enforce OSHA-compliant nozzles.",
        entity_scope="All pneumatic cleaning operations",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="OSHA 29 CFR 1910.242(b)"
    ),

    DoctrineBlock(
        topic="Condensate Management and Drain Selection",
        keywords=[
            "condensate", "drain", "moisture removal", "automatic drain", "manual drain"
        ],
        conclusion_template="Install automatic or timed drains at all low points and receivers to manage condensate and prevent water accumulation.",
        reasoning_framework="""
        1. Identify all low points and receivers in the system.
        2. Select appropriate drain type (automatic, timed, manual).
        3. Ensure drains are sized for expected condensate volume.
        4. Schedule regular inspection and maintenance.
        5. Reference environmental regulations for condensate disposal.
        """,
        key_factors=[
            "Condensate volume", "Drain type", "Maintenance", "Disposal regulations"
        ],
        primary_authority=[
            "OEM Manuals", "EPA Guidelines"
        ],
        burden_holder="Maintenance technician",
        adversary_position="Manual drains are sufficient for all systems.",
        counter_arguments=[
            "Manual drains are often neglected, leading to water accumulation.",
            "Automatic drains improve reliability."
        ],
        resolution_strategy="Install and maintain automatic drains where feasible.",
        entity_scope="Compressed air systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OEM Drain Selection Guidelines"
    ),

    DoctrineBlock(
        topic="Compressed Air System Pressure Optimization",
        keywords=[
            "pressure optimization", "setpoint", "energy savings", "system pressure"
        ],
        conclusion_template="Optimize system pressure setpoints to the minimum required for process needs, reducing energy consumption and leakage.",
        reasoning_framework="""
        1. Survey all end uses for minimum pressure requirements.
        2. Set system pressure as low as possible while maintaining performance.
        3. Quantify energy savings for each 2 PSI reduction (~1% savings).
        4. Monitor for pressure drops at peak demand.
        5. Adjust setpoints as system changes.
        """,
        key_factors=[
            "Minimum process pressure", "System pressure drop", "Energy cost", "Performance margin"
        ],
        primary_authority=[
            "DOE Compressed Air Challenge", "CAGI"
        ],
        burden_holder="Facility energy manager",
        adversary_position="Higher pressure always improves performance.",
        counter_arguments=[
            "Excess pressure increases energy use and leakage.",
            "Lower pressure is sufficient for most processes."
        ],
        resolution_strategy="Set and monitor pressure for minimum required performance.",
        entity_scope="Industrial compressed air systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="DOE Compressed Air Challenge"
    ),

    DoctrineBlock(
        topic="Air Line Lubrication Best Practices",
        keywords=[
            "air line lubrication", "lubricator", "oil mist", "maintenance", "component life"
        ],
        conclusion_template="Use air line lubricators only when required by downstream equipment, and maintain oil level and type per manufacturer recommendations.",
        reasoning_framework="""
        1. Identify equipment requiring lubrication (older valves, tools).
        2. Select lubricator type and oil per OEM guidance.
        3. Adjust oil feed rate to minimize excess.
        4. Inspect and refill lubricators regularly.
        5. Avoid lubrication where not needed to prevent contamination.
        """,
        key_factors=[
            "Equipment lubrication needs", "Oil type", "Feed rate", "Maintenance"
        ],
        primary_authority=[
            "OEM Manuals"
        ],
        burden_holder="Maintenance technician",
        adversary_position="Lubricators should be installed on all air lines.",
        counter_arguments=[
            "Unnecessary lubrication contaminates air and equipment.",
            "Modern components often require no lubrication."
        ],
        resolution_strategy="Install lubricators only as needed and maintain properly.",
        entity_scope="Pneumatic systems with lubricated components",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OEM Lubrication Guidelines"
    ),

    DoctrineBlock(
        topic="Pneumatic Silencer Selection and Noise Control",
        keywords=[
            "silencer", "noise control", "exhaust", "OSHA noise", "pneumatic muffler"
        ],
        conclusion_template="Install silencers at exhaust ports to reduce noise to below OSHA limits, selecting type and size for flow and attenuation requirements.",
        reasoning_framework="""
        1. Measure exhaust noise levels at operator locations.
        2. Select silencer type (porous, baffled, combination) for required attenuation.
        3. Ensure silencer flow capacity matches exhaust rate.
        4. Inspect and clean silencers regularly to prevent clogging.
        5. Reference OSHA and local noise regulations.
        """,
        key_factors=[
            "Noise level", "Silencer type", "Flow capacity", "Maintenance"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.95", "OEM Silencer Catalogs"
        ],
        burden_holder="Facility safety officer",
        adversary_position="Silencers reduce flow and are unnecessary.",
        counter_arguments=[
            "Noise exposure above limits causes hearing loss.",
            "Properly sized silencers minimize flow restriction."
        ],
        resolution_strategy="Select and maintain silencers to meet noise limits.",
        entity_scope="All pneumatic exhaust systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OSHA 29 CFR 1910.95"
    ),

    DoctrineBlock(
        topic="Pressure Relief Valve Sizing and Placement",
        keywords=[
            "pressure relief valve", "safety valve", "sizing", "placement", "overpressure protection"
        ],
        conclusion_template="Install and size pressure relief valves per ASME and OSHA requirements to protect vessels and piping from overpressure.",
        reasoning_framework="""
        1. Identify all pressure vessels and piping requiring protection.
        2. Calculate maximum possible pressure and required relief capacity.
        3. Select valve setpoint below vessel MAWP.
        4. Install relief valves at all protected locations.
        5. Reference ASME Section VIII and OSHA 1910.169 for sizing and placement.
        """,
        key_factors=[
            "Protected volume", "Maximum allowable working pressure", "Relief capacity", "Setpoint"
        ],
        primary_authority=[
            "ASME Section VIII", "OSHA 1910.169"
        ],
        burden_holder="System designer",
        adversary_position="Relief valves are only needed at compressors.",
        counter_arguments=[
            "All pressure vessels and piping require overpressure protection.",
            "Improper sizing risks catastrophic failure."
        ],
        resolution_strategy="Size and install relief valves per code.",
        entity_scope="Compressed air systems",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="ASME Section VIII"
    ),

    DoctrineBlock(
        topic="Compressed Air System Zoning and Isolation",
        keywords=[
            "system zoning", "isolation valve", "maintenance", "energy savings", "leak isolation"
        ],
        conclusion_template="Divide compressed air systems into zones with isolation valves for maintenance, leak management, and energy savings.",
        reasoning_framework="""
        1. Identify logical zones based on process or building layout.
        2. Install isolation valves at zone boundaries.
        3. Use zoning to isolate leaks or perform maintenance without full shutdown.
        4. Reference best practices for valve selection and placement.
        5. Document zone boundaries and valve locations.
        """,
        key_factors=[
            "System layout", "Zone function", "Valve type", "Maintenance needs"
        ],
        primary_authority=[
            "CAGI", "OEM Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Zoning adds unnecessary complexity.",
        counter_arguments=[
            "Zoning improves reliability and reduces downtime.",
            "Isolation enables targeted leak management."
        ],
        resolution_strategy="Design and document zones with isolation capability.",
        entity_scope="Large or complex compressed air systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="CAGI System Design Guidelines"
    ),

    DoctrineBlock(
        topic="Compressed Air System Expansion Planning",
        keywords=[
            "system expansion", "future capacity", "modular design", "scalability"
        ],
        conclusion_template="Design compressed air systems with modularity and spare capacity to accommodate future expansion and changing demands.",
        reasoning_framework="""
        1. Forecast future air demand based on production plans.
        2. Size main distribution piping and compressors for anticipated growth.
        3. Use modular components and parallel compressor configurations.
        4. Document expansion provisions in system drawings.
        5. Reference best practices for scalable system design.
        """,
        key_factors=[
            "Future demand", "Modularity", "Spare capacity", "Documentation"
        ],
        primary_authority=[
            "CAGI", "OEM Manuals"
        ],
        burden_holder="System designer",
        adversary_position="Design for current needs only.",
        counter_arguments=[
            "Retrofitting is more costly than initial over-sizing.",
            "Modular design enables flexible expansion."
        ],
        resolution_strategy="Incorporate expansion capability in initial design.",
        entity_scope="Industrial compressed air systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="CAGI System Design Guidelines"
    ),

    DoctrineBlock(
        topic="Compressed Air System Monitoring and Data Logging",
        keywords=[
            "system monitoring", "data logging", "pressure", "flow", "energy consumption"
        ],
        conclusion_template="Implement continuous monitoring and data logging of pressure, flow, and energy to enable proactive maintenance and optimization.",
        reasoning_framework="""
        1. Install sensors for pressure, flow, and power at key locations.
        2. Log data for trend analysis and anomaly detection.
        3. Use monitoring to identify leaks, pressure drops, and inefficiencies.
        4. Integrate with building management or SCADA systems.
        5. Reference ISO 11011 for audit and monitoring practices.
        """,
        key_factors=[
            "Sensor placement", "Data accuracy", "Integration", "Analysis"
        ],
        primary_authority=[
            "ISO 11011", "OEM Manuals"
        ],
        burden_holder="Facility manager",
        adversary_position="Manual checks are sufficient.",
        counter_arguments=[
            "Continuous monitoring enables early detection of issues.",
            "Data logging supports optimization and reporting."
        ],
        resolution_strategy="Install and use monitoring systems for all major installations.",
        entity_scope="Industrial compressed air systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ISO 11011"
    ),

    DoctrineBlock(
        topic="Desiccant Dryer Purge Loss Minimization",
        keywords=[
            "desiccant dryer", "purge loss", "energy efficiency", "dew point control"
        ],
        conclusion_template="Minimize desiccant dryer purge losses by using demand-based controls and optimizing cycle timing.",
        reasoning_framework="""
        1. Quantify purge air consumption for existing dryers.
        2. Evaluate demand-based or dew point controlled purge systems.
        3. Adjust cycle timing for minimum required purge.
        4. Monitor dew point and adjust controls as needed.
        5. Reference OEM and CAGI best practices.
        """,
        key_factors=[
            "Purge air consumption", "Control method", "Dew point monitoring", "Cycle timing"
        ],
        primary_authority=[
            "CAGI", "OEM Manuals"
        ],
        burden_holder="Facility energy manager",
        adversary_position="Purge losses are unavoidable.",
        counter_arguments=[
            "Demand-based controls can reduce purge loss by 40-60%.",
            "Optimized cycles maintain dew point with less waste."
        ],
        resolution_strategy="Upgrade controls and monitor performance.",
        entity_scope="Systems with desiccant dryers",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CAGI Dryer Efficiency Guidelines"
    ),

    DoctrineBlock(
        topic="Pneumatic Tubing Material Selection",
        keywords=[
            "tubing", "material selection", "nylon", "polyurethane", "copper", "corrosion"
        ],
        conclusion_template="Select pneumatic tubing material based on pressure rating, flexibility, chemical compatibility, and environment.",
        reasoning_framework="""
        1. Determine required pressure rating and flexibility.
        2. Evaluate chemical compatibility with conveyed air and environment.
        3. Select material (nylon, polyurethane, copper, stainless) as appropriate.
        4. Consider cost, installation ease, and maintenance.
        5. Reference OEM and ISO 4414 guidelines.
        """,
        key_factors=[
            "Pressure rating", "Chemical compatibility", "Flexibility", "Cost"
        ],
        primary_authority=[
            "ISO 4414", "OEM Tubing Catalogs"
        ],
        burden_holder="System designer",
        adversary_position="Any tubing is suitable for all applications.",
        counter_arguments=[
            "Incorrect material risks failure or leaks.",
            "Material choice affects installation and durability."
        ],
        resolution_strategy="Match tubing material to application and environment.",
        entity_scope="All pneumatic systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 4414"
    ),

    DoctrineBlock(
        topic="Compressed Air System Color Coding and Labeling",
        keywords=[
            "color coding", "labeling", "piping identification", "safety", "maintenance"
        ],
        conclusion_template="Apply standardized color coding and labeling to compressed air piping for safety and maintenance efficiency.",
        reasoning_framework="""
        1. Reference ANSI/ASME A13.1 for pipe color coding standards.
        2. Label all compressed air lines at regular intervals and junctions.
        3. Use durable, legible labels and color bands.
        4. Document labeling scheme in system drawings.
        5. Train staff on identification and safety.
        """,
        key_factors=[
            "Color standard", "Label durability", "Documentation", "Training"
        ],
        primary_authority=[
            "ANSI/ASME A13.1", "OEM Manuals"
        ],
        burden_holder="Facility safety officer",
        adversary_position="Labeling is unnecessary for small systems.",
        counter_arguments=[
            "Proper labeling prevents errors and improves safety.",
            "Required by many safety codes."
        ],
        resolution_strategy="Implement and maintain standardized labeling.",
        entity_scope="All compressed air systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ANSI/ASME A13.1"
    ),

    DoctrineBlock(
        topic="Pneumatic System Start-Up and Commissioning Procedures",
        keywords=[
            "start-up", "commissioning", "testing", "leak check", "system validation"
        ],
        conclusion_template="Follow systematic start-up and commissioning procedures including leak checks, pressure testing, and functional validation.",
        reasoning_framework="""
        1. Inspect all piping, connections, and components for correct installation.
        2. Perform leak checks at operating pressure.
        3. Test safety devices and relief valves.
        4. Validate system operation against design specifications.
        5. Document commissioning results and corrective actions.
        """,
        key_factors=[
            "Installation quality", "Leak testing", "Safety device function", "Documentation"
        ],
        primary_authority=[
            "OEM Manuals", "ISO 4414"
        ],
        burden_holder="Commissioning engineer",
        adversary_position="Start-up can be informal if system is simple.",
        counter_arguments=[
            "Formal commissioning prevents early failures.",
            "Documentation supports warranty and compliance."
        ],
        resolution_strategy="Follow documented procedures for all start-ups.",
        entity_scope="All pneumatic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OEM Commissioning Guidelines"
    ),

    DoctrineBlock(
        topic="Compressed Air System Redundancy and Reliability Planning",
        keywords=[
            "redundancy", "reliability", "backup compressor", "N+1", "system uptime"
        ],
        conclusion_template="Design critical compressed air systems with N+1 redundancy for compressors and key components to ensure high reliability and uptime.",
        reasoning_framework="""
        1. Identify critical processes requiring continuous air supply.
        2. Size system for N+1 redundancy (one spare unit for each group).
        3. Include automatic changeover and alarm systems.
        4. Schedule regular testing of backup units.
        5. Reference CAGI and ISO 8573-1 for reliability planning.
        """,
        key_factors=[
            "Criticality", "Redundancy level", "Automatic controls", "Testing"
        ],
        primary_authority=[
            "CAGI", "ISO 8573-1"
        ],
        burden_holder="System designer",
        adversary_position="Redundancy is unnecessary for most systems.",
        counter_arguments=[
            "Critical processes cannot tolerate downtime.",
            "Redundancy improves reliability and safety."
        ],
        resolution_strategy="Design and test redundancy per criticality.",
        entity_scope="Critical compressed air systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CAGI Reliability Guidelines"
    ),

    DoctrineBlock(
        topic="Pneumatic System Preventive Maintenance Scheduling",
        keywords=[
            "preventive maintenance", "schedule", "inspection", "service interval", "component life"
        ],
        conclusion_template="Establish preventive maintenance schedules for all pneumatic components based on manufacturer recommendations and operating conditions.",
        reasoning_framework="""
        1. Inventory all pneumatic components and record service intervals.
        2. Schedule inspections and maintenance per OEM guidelines.
        3. Adjust intervals based on operating hours and environment.
        4. Track maintenance actions and component replacements.
        5. Reference ISO 4414 for maintenance best practices.
        """,
        key_factors=[
            "Component inventory", "Service interval", "Operating conditions", "Recordkeeping"
        ],
        primary_authority=[
            "ISO 4414", "OEM Manuals"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Reactive maintenance is sufficient.",
        counter_arguments=[
            "Preventive maintenance reduces failures and downtime.",
            "OEM intervals are based on tested reliability."
        ],
        resolution_strategy="Implement and track preventive maintenance.",
        entity_scope="All pneumatic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 4414"
    ),

    DoctrineBlock(
        topic="Pneumatic Actuator Cushioning Adjustment",
        keywords=[
            "actuator cushioning", "end-of-stroke", "shock absorption", "adjustment"
        ],
        conclusion_template="Adjust actuator cushioning to minimize end-of-stroke shock and noise, extending component life.",
        reasoning_framework="""
        1. Identify actuators with adjustable cushioning.
        2. Adjust cushioning screw to achieve smooth deceleration.
        3. Monitor for excessive noise or vibration at end of stroke.
        4. Reference OEM guidelines for adjustment procedure.
        5. Document settings for future maintenance.
        """,
        key_factors=[
            "Actuator type", "Cushioning adjustment", "Noise/vibration", "Documentation"
        ],
        primary_authority=[
            "OEM Manuals"
        ],
        burden_holder="Maintenance technician",
        adversary_position="Cushioning adjustment is unnecessary.",
        counter_arguments=[
            "Proper cushioning reduces wear and noise.",
            "Incorrect adjustment causes shock and damage."
        ],
        resolution_strategy="Adjust and document cushioning settings.",
        entity_scope="Pneumatic actuator systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OEM Cushioning Guidelines"
    ),

    DoctrineBlock(
        topic="Pneumatic System Emergency Shutdown Procedures",
        keywords=[
            "emergency shutdown", "energy isolation", "lockout/tagout", "safety"
        ],
        conclusion_template="Establish and train personnel on emergency shutdown and energy isolation procedures for all pneumatic systems.",
        reasoning_framework="""
        1. Identify all energy isolation points (main valve, lockout devices).
        2. Develop written emergency shutdown procedures.
        3. Train all personnel in shutdown and lockout/tagout.
        4. Test procedures during drills and audits.
        5. Reference OSHA and ISO 4414 for requirements.
        """,
        key_factors=[
            "Isolation points", "Procedure documentation", "Training", "Testing"
        ],
        primary_authority=[
            "OSHA 1910.147", "ISO 4414"
        ],
        burden_holder="Facility safety officer",
        adversary_position="Emergency shutdown is intuitive and needs no documentation.",
        counter_arguments=[
            "Written procedures and training prevent accidents.",
            "Regulatory compliance requires documentation."
        ],
        resolution_strategy="Document and train on emergency shutdown.",
        entity_scope="All pneumatic systems",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="OSHA 1910.147"
    ),

    DoctrineBlock(
        topic="Pneumatic System Documentation and Change Management",
        keywords=[
            "documentation", "change management", "as-built drawings", "revision control"
        ],
        conclusion_template="Maintain up-to-date documentation and implement change management for all pneumatic system modifications.",
        reasoning_framework="""
        1. Keep as-built drawings and component lists current.
        2. Document all changes with revision history.
        3. Review and approve changes before implementation.
        4. Train staff on documentation and change control procedures.
        5. Reference ISO 9001 for documentation best practices.
        """,
        key_factors=[
            "Drawing accuracy", "Revision control", "Approval process", "Training"
        ],
        primary_authority=[
            "ISO 9001", "OEM Manuals"
        ],
        burden_holder="System owner",
        adversary_position="Documentation is unnecessary for small changes.",
        counter_arguments=[
            "Accurate documentation supports maintenance and troubleshooting.",
            "Change control prevents errors and omissions."
        ],
        resolution_strategy="Implement formal documentation and change management.",
        entity_scope="All pneumatic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ISO 9001"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    return [
        doctrine for doctrine in DOCTRINE_CACHE
        if keyword_lower in doctrine.topic.lower()
        or any(keyword_lower in k.lower() for k in doctrine.keywords)
        or keyword_lower in doctrine.reasoning_framework.lower()
    ]

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]