import enum
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

class ConfidenceZone(enum.Enum):
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
        topic="Brayton Cycle Efficiency Optimization",
        keywords=["brayton cycle", "thermal efficiency", "optimization", "AERO04"],
        conclusion_template="For the AERO04 engine, maximizing Brayton cycle efficiency requires optimizing pressure ratio and turbine inlet temperature within material and operational constraints.",
        reasoning_framework="""
The Brayton cycle efficiency is primarily governed by the pressure ratio (PR) across the compressor and the maximum allowable turbine inlet temperature (TIT). For the AERO04, the optimal PR is determined by balancing the increase in thermal efficiency with the diminishing returns and increased compressor work at higher PRs. TIT is limited by turbine blade material properties and cooling technology. The cycle analysis should include real gas effects, component efficiencies (compressor and turbine polytropic efficiencies), and pressure losses in combustor and ducts. The trade-off between higher PR (which increases efficiency) and the associated increase in compressor work and cooling requirements must be evaluated. The optimal point is where the marginal gain in efficiency equals the marginal cost in complexity, weight, and cooling demand.
""",
        key_factors=[
            "Compressor pressure ratio",
            "Turbine inlet temperature",
            "Component efficiencies",
            "Material temperature limits",
            "Cooling technology",
            "Pressure losses"
        ],
        primary_authority=[
            "Saravanamuttoo, Cohen & Rogers, Gas Turbine Theory (7th Ed.)",
            "Rolls-Royce, The Jet Engine (5th Ed.)"
        ],
        burden_holder="Engine design authority",
        adversary_position="Advocates for higher pressure ratios regardless of material/cooling limits",
        counter_arguments=[
            "Excessive PR increases compressor work disproportionately",
            "Material limits may be exceeded, risking failure",
            "Cooling requirements may become impractical"
        ],
        resolution_strategy="Conduct parametric cycle analysis and validate with component test data; select PR and TIT within validated operational envelope.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brayton Cycle Optimization, RR Trent 7000, 2016"
    ),
    DoctrineBlock(
        topic="Axial Compressor Stage Matching",
        keywords=["axial compressor", "stage matching", "AERO04", "compressor map"],
        conclusion_template="Stage matching in the AERO04 axial compressor must ensure stable operation across the flight envelope, minimizing surge and stall risk.",
        reasoning_framework="""
Axial compressor stage matching involves aligning the operating points of each stage so that the overall compressor operates within the stable region of the compressor map. For the AERO04, this requires detailed analysis of stage-by-stage flow coefficients, blade angles, and velocity triangles. The matching process must account for variable inlet guide vanes (if present), bleed flows, and off-design conditions. Surge margin must be maintained at all power settings, especially during acceleration and deceleration transients. Computational tools and empirical data from similar engines should be used to validate the matching.
""",
        key_factors=[
            "Stage flow coefficients",
            "Blade angles and velocity triangles",
            "Variable geometry (if any)",
            "Bleed flows",
            "Surge margin"
        ],
        primary_authority=[
            "Kurzke, GasTurb 12 Manual",
            "Saravanamuttoo, Gas Turbine Theory"
        ],
        burden_holder="Compressor design team",
        adversary_position="Proposes aggressive stage loading for compactness",
        counter_arguments=[
            "Aggressive loading reduces surge margin",
            "Stage mismatch increases risk of rotating stall",
            "Off-design performance may degrade"
        ],
        resolution_strategy="Iterative design using compressor maps and CFD; validate with rig testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Compressor Design, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Emissions Compliance",
        keywords=["combustor", "emissions", "NOx", "CO", "AERO04"],
        conclusion_template="AERO04 combustor design must comply with ICAO Annex 16 emission limits for NOx, CO, and UHC under all certified operating conditions.",
        reasoning_framework="""
Combustor emissions are regulated by ICAO Annex 16, which sets limits for NOx, CO, and unburned hydrocarbons (UHC). For AERO04, the combustor must be designed to minimize local flame temperatures (to reduce NOx) while ensuring complete combustion (to minimize CO and UHC). Lean-burn or staged combustion techniques may be necessary. Emissions must be validated through full-scale combustor rig testing and engine certification tests. Trade-offs between emissions, combustion stability, and efficiency must be carefully managed.
""",
        key_factors=[
            "ICAO Annex 16 limits",
            "Combustor temperature profile",
            "Combustion efficiency",
            "Stability margin",
            "Testing data"
        ],
        primary_authority=[
            "ICAO Annex 16, Volume II",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor design authority",
        adversary_position="Advocates for higher efficiency at the expense of emissions",
        counter_arguments=[
            "Non-compliance with emissions regulations leads to certification failure",
            "High flame temperatures increase NOx",
            "Incomplete combustion increases CO/UHC"
        ],
        resolution_strategy="Optimize combustor design using CFD and rig testing; ensure compliance through certification testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent XWB Emissions Certification, 2014"
    ),
    DoctrineBlock(
        topic="Turbine Blade Cooling Design",
        keywords=["turbine", "blade cooling", "thermal management", "AERO04"],
        conclusion_template="AERO04 turbine blades must employ advanced cooling (e.g., film or transpiration) to withstand TIT and ensure durability.",
        reasoning_framework="""
The turbine inlet temperature (TIT) in modern engines such as AERO04 exceeds the melting point of superalloy blades. Effective cooling is essential for blade life and engine reliability. Film cooling, transpiration cooling, and internal convection are common techniques. The cooling design must minimize cooling air usage (to preserve cycle efficiency) while maintaining blade temperature below critical limits. The design should be validated with thermal analysis, material testing, and engine endurance trials.
""",
        key_factors=[
            "Turbine inlet temperature",
            "Blade material properties",
            "Cooling air availability",
            "Thermal analysis data",
            "Durability requirements"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "NASA SP-8122, Turbine Cooling Technology"
        ],
        burden_holder="Turbine design authority",
        adversary_position="Proposes reduced cooling to improve cycle efficiency",
        counter_arguments=[
            "Insufficient cooling leads to blade failure",
            "Reduced cooling shortens component life",
            "Thermal fatigue risk increases"
        ],
        resolution_strategy="Balance cooling air allocation with cycle efficiency; validate with rig and engine tests.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE9X Turbine Cooling, 2017"
    ),
    DoctrineBlock(
        topic="Compressor Surge Margin Requirement",
        keywords=["compressor", "surge margin", "operational safety", "AERO04"],
        conclusion_template="A minimum surge margin of 15% must be maintained in the AERO04 compressor across the entire operating envelope.",
        reasoning_framework="""
Surge margin is the buffer between the operating line and the surge line on the compressor map, expressed as a percentage. For safe operation, industry practice and certification standards require a minimum surge margin (typically 10-20%). For AERO04, a 15% minimum is mandated to account for manufacturing tolerances, deterioration, and transient conditions. Surge events can cause catastrophic damage; thus, surge margin must be validated through both analysis and engine testing.
""",
        key_factors=[
            "Compressor map",
            "Operating envelope",
            "Transient conditions",
            "Manufacturing tolerances",
            "Test data"
        ],
        primary_authority=[
            "FAA AC 33.90-1",
            "Saravanamuttoo, Gas Turbine Theory"
        ],
        burden_holder="Compressor performance engineer",
        adversary_position="Proposes operating closer to surge line for higher efficiency",
        counter_arguments=[
            "Reduced surge margin increases risk of surge",
            "Compressor damage and loss of thrust possible",
            "Certification may be denied"
        ],
        resolution_strategy="Design and validate compressor maps to ensure 15% margin; monitor in service.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PW1000G Compressor Certification, 2013"
    ),
    DoctrineBlock(
        topic="Material Selection for High-Pressure Turbine",
        keywords=["materials", "high-pressure turbine", "superalloys", "AERO04"],
        conclusion_template="AERO04 high-pressure turbine must use single-crystal superalloys with thermal barrier coatings for optimal performance.",
        reasoning_framework="""
High-pressure turbine (HPT) components in AERO04 are exposed to extreme temperatures and stresses. Single-crystal superalloys provide superior creep and fatigue resistance compared to polycrystalline materials. Thermal barrier coatings (TBCs) further protect against oxidation and thermal fatigue. Material selection must consider manufacturability, cost, and proven service history. The use of directionally solidified or single-crystal blades is industry best practice for engines in this class.
""",
        key_factors=[
            "Operating temperature",
            "Creep and fatigue resistance",
            "Oxidation resistance",
            "Manufacturability",
            "Cost"
        ],
        primary_authority=[
            "Donachie, Superalloys: A Technical Guide",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Materials engineering lead",
        adversary_position="Advocates for lower-cost, polycrystalline alloys",
        counter_arguments=[
            "Polycrystalline alloys have lower creep resistance",
            "Reduced durability and higher maintenance",
            "Potential for premature failure"
        ],
        resolution_strategy="Select materials based on proven service record and lifecycle cost analysis.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 900 HPT Material Selection, 2007"
    ),
    DoctrineBlock(
        topic="Compressor Bleed Air Management",
        keywords=["compressor", "bleed air", "systems integration", "AERO04"],
        conclusion_template="Bleed air extraction in AERO04 must be minimized and managed to prevent adverse effects on compressor stability and engine efficiency.",
        reasoning_framework="""
Bleed air is extracted from the compressor for various aircraft systems (e.g., anti-ice, cabin pressurization). Excessive bleed reduces compressor pressure ratio and can move the operating point closer to surge. For AERO04, bleed extraction must be balanced to meet aircraft needs without compromising engine stability or efficiency. Bleed schedules should be optimized and validated through engine testing and integration analysis.
""",
        key_factors=[
            "Bleed air requirements",
            "Compressor stability",
            "Engine efficiency",
            "Aircraft systems integration",
            "Test data"
        ],
        primary_authority=[
            "FAA AC 33.90-1",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Systems integration engineer",
        adversary_position="Proposes unrestricted bleed for aircraft systems",
        counter_arguments=[
            "Unrestricted bleed reduces surge margin",
            "Impacts engine efficiency",
            "May lead to compressor stall"
        ],
        resolution_strategy="Define and enforce bleed schedules; validate through integrated testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFM56 Bleed Air Management, 1998"
    ),
    DoctrineBlock(
        topic="Combustor Liner Durability",
        keywords=["combustor", "liner", "durability", "thermal fatigue", "AERO04"],
        conclusion_template="AERO04 combustor liner must be designed for a minimum life of 20,000 cycles, using advanced alloys and cooling techniques.",
        reasoning_framework="""
Combustor liners are subject to high thermal gradients and cyclic loading, leading to thermal fatigue and oxidation. For AERO04, the liner must be constructed from high-temperature alloys (e.g., Hastelloy X, Haynes 230) and feature effective cooling (e.g., effusion cooling). Life prediction models should be validated with cyclic rig testing. Maintenance intervals and inspection criteria must be established based on durability analysis.
""",
        key_factors=[
            "Thermal fatigue resistance",
            "Oxidation resistance",
            "Cooling effectiveness",
            "Cycle life requirements",
            "Test data"
        ],
        primary_authority=[
            "Donachie, Superalloys",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor component engineer",
        adversary_position="Proposes lower-cost materials or reduced cooling",
        counter_arguments=[
            "Lower-cost materials may not meet life requirements",
            "Reduced cooling increases thermal fatigue",
            "Higher maintenance costs"
        ],
        resolution_strategy="Select materials and cooling based on validated life models and test data.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Combustor Liner, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Fouling and Performance Degradation",
        keywords=["compressor", "fouling", "performance degradation", "maintenance", "AERO04"],
        conclusion_template="AERO04 compressor design and maintenance must mitigate fouling to preserve performance and efficiency over time.",
        reasoning_framework="""
Compressor fouling from airborne contaminants reduces airflow and efficiency, increasing fuel consumption. For AERO04, design features such as inlet screens and self-cleaning coatings can reduce fouling. Regular on-wing water washes and scheduled maintenance are required. Performance monitoring should trigger cleaning or inspection when degradation exceeds defined thresholds. Data from similar engines should inform maintenance intervals.
""",
        key_factors=[
            "Airborne contaminant exposure",
            "Inlet protection",
            "Cleaning technology",
            "Performance monitoring",
            "Maintenance intervals"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "FAA AC 33.90-1"
        ],
        burden_holder="Maintenance engineering",
        adversary_position="Proposes less frequent cleaning to reduce downtime",
        counter_arguments=[
            "Less cleaning increases performance loss",
            "Higher fuel burn and emissions",
            "Potential for unscheduled maintenance"
        ],
        resolution_strategy="Implement predictive maintenance and regular cleaning based on performance data.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CF6-80 Compressor Fouling, 2002"
    ),
    DoctrineBlock(
        topic="Combustor Pressure Loss Limit",
        keywords=["combustor", "pressure loss", "cycle efficiency", "AERO04"],
        conclusion_template="AERO04 combustor pressure loss must not exceed 5% of total pressure at cruise to preserve cycle efficiency.",
        reasoning_framework="""
Pressure loss in the combustor reduces the pressure available to the turbine, lowering overall cycle efficiency. For AERO04, a maximum pressure loss of 5% at cruise is set based on industry best practice. This requires careful combustor aerodynamics design, including optimized liner hole patterns and flow distribution. Pressure loss must be validated through rig and engine testing.
""",
        key_factors=[
            "Combustor aerodynamics",
            "Liner hole patterns",
            "Flow distribution",
            "Test data",
            "Cycle analysis"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Saravanamuttoo, Gas Turbine Theory"
        ],
        burden_holder="Combustor aerodynamics engineer",
        adversary_position="Proposes relaxed pressure loss limits for easier design",
        counter_arguments=[
            "Higher pressure loss reduces cycle efficiency",
            "May require larger turbine",
            "Increased fuel consumption"
        ],
        resolution_strategy="Optimize combustor design and validate pressure loss in testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="V2500 Combustor Pressure Loss, 1993"
    ),
    DoctrineBlock(
        topic="Axial Compressor Tip Clearance Control",
        keywords=["axial compressor", "tip clearance", "efficiency", "AERO04"],
        conclusion_template="AERO04 must employ active or passive tip clearance control to minimize leakage and maximize compressor efficiency.",
        reasoning_framework="""
Tip clearance between rotating blades and casing affects compressor efficiency and surge margin. Excessive clearance increases leakage, reducing efficiency; too little risks blade rubs. For AERO04, thermal and centrifugal growth must be accounted for. Active clearance control (e.g., casing cooling) or abradable linings can be used. Design must be validated with thermal/mechanical analysis and engine testing.
""",
        key_factors=[
            "Thermal/centrifugal growth",
            "Leakage losses",
            "Blade/casing interaction",
            "Clearance control technology",
            "Test data"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Kurzke, GasTurb 12 Manual"
        ],
        burden_holder="Compressor mechanical design team",
        adversary_position="Proposes fixed clearance for simplicity",
        counter_arguments=[
            "Fixed clearance may be excessive at some conditions",
            "Efficiency penalty",
            "Increased risk of blade rubs"
        ],
        resolution_strategy="Implement clearance control and validate with analysis and testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Tip Clearance Control, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Stability Margin",
        keywords=["combustor", "stability", "lean blowout", "AERO04"],
        conclusion_template="AERO04 combustor must maintain a stability margin sufficient to avoid lean blowout and combustion oscillations under all conditions.",
        reasoning_framework="""
Combustor stability is critical for safe engine operation. Lean blowout (LBO) occurs at low fuel/air ratios, while combustion oscillations can cause hardware damage. For AERO04, the combustor must be designed and tested to avoid LBO and maintain stable operation across the flight envelope. Stability margin must be validated through rig and engine testing, including transient conditions.
""",
        key_factors=[
            "Fuel/air ratio range",
            "Ignition limits",
            "Combustion oscillation data",
            "Test results",
            "Transient operation"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "ICAO Annex 16"
        ],
        burden_holder="Combustor design authority",
        adversary_position="Proposes leaner operation for lower emissions",
        counter_arguments=[
            "Leaner operation increases LBO risk",
            "Oscillations can damage hardware",
            "Certification may be denied"
        ],
        resolution_strategy="Optimize combustor design and validate with stability margin testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 700 Combustor Stability, 1997"
    ),
    DoctrineBlock(
        topic="Compressor Map Validation",
        keywords=["compressor", "map", "validation", "AERO04"],
        conclusion_template="AERO04 compressor maps must be validated against rig and engine test data to ensure accuracy for performance prediction.",
        reasoning_framework="""
Compressor maps are essential for engine performance modeling and control logic. For AERO04, initial maps are generated from CFD and empirical correlations, but must be validated and adjusted using rig and engine test data. Discrepancies must be analyzed and resolved to ensure accurate prediction of surge margin, efficiency, and flow capacity.
""",
        key_factors=[
            "CFD and empirical data",
            "Rig test results",
            "Engine test results",
            "Map adjustment methodology",
            "Performance prediction"
        ],
        primary_authority=[
            "Kurzke, GasTurb 12 Manual",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Performance engineering",
        adversary_position="Relies solely on CFD/empirical data",
        counter_arguments=[
            "CFD/empirical models may not capture all effects",
            "Test data is required for certification",
            "Unvalidated maps risk inaccurate control"
        ],
        resolution_strategy="Iterative map adjustment using test data; document all changes.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PW4000 Compressor Map Validation, 2001"
    ),
    DoctrineBlock(
        topic="Turbine Cooling Air Allocation",
        keywords=["turbine", "cooling air", "cycle efficiency", "AERO04"],
        conclusion_template="AERO04 turbine cooling air allocation must be minimized to preserve cycle efficiency while ensuring blade life.",
        reasoning_framework="""
Cooling air for turbine blades is bled from the compressor, reducing the mass flow available for the core and thus cycle efficiency. For AERO04, the allocation must be minimized through advanced cooling techniques and materials. However, blade life and durability cannot be compromised. The allocation should be determined through thermal analysis and validated with rig and engine testing.
""",
        key_factors=[
            "Cooling air flow rate",
            "Blade temperature limits",
            "Material properties",
            "Cycle analysis",
            "Test data"
        ],
        primary_authority=[
            "NASA SP-8122, Turbine Cooling Technology",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Turbine cooling design team",
        adversary_position="Proposes increased cooling for conservative design",
        counter_arguments=[
            "Excessive cooling reduces cycle efficiency",
            "Increases compressor load",
            "May not be necessary with advanced materials"
        ],
        resolution_strategy="Optimize cooling air allocation based on validated analysis and testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE9X Cooling Air Optimization, 2017"
    ),
    DoctrineBlock(
        topic="Compressor Variable Geometry Utilization",
        keywords=["compressor", "variable geometry", "IGV", "VSV", "AERO04"],
        conclusion_template="AERO04 must utilize variable geometry (IGV/VSV) to optimize compressor performance and surge margin across the flight envelope.",
        reasoning_framework="""
Variable geometry, such as inlet guide vanes (IGV) and variable stator vanes (VSV), allows adjustment of airflow and incidence angles in the compressor. For AERO04, this enables optimal performance at both takeoff and cruise, and maintains surge margin during transients. Control logic must be validated through simulation and engine testing to ensure reliability and responsiveness.
""",
        key_factors=[
            "IGV/VSV actuation",
            "Control logic",
            "Surge margin",
            "Performance at off-design points",
            "Test data"
        ],
        primary_authority=[
            "Kurzke, GasTurb 12 Manual",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Compressor control systems engineer",
        adversary_position="Proposes fixed geometry for simplicity",
        counter_arguments=[
            "Fixed geometry cannot optimize across all conditions",
            "Reduced surge margin at off-design",
            "Lower efficiency"
        ],
        resolution_strategy="Implement and validate variable geometry with simulation and testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CF6-80 Variable Geometry, 1985"
    ),
    DoctrineBlock(
        topic="Combustor Ignition Reliability",
        keywords=["combustor", "ignition", "reliability", "AERO04"],
        conclusion_template="AERO04 combustor ignition system must achieve 99.99% reliability under all certified starting and relight conditions.",
        reasoning_framework="""
Ignition reliability is critical for safe engine start and in-flight relight. For AERO04, the ignition system must function at low temperatures, high altitudes, and during rapid relight scenarios. Redundant igniters and robust control logic are required. Reliability must be demonstrated through statistical analysis of test data and in-service experience.
""",
        key_factors=[
            "Igniter redundancy",
            "Control logic",
            "Environmental conditions",
            "Test data",
            "Reliability analysis"
        ],
        primary_authority=[
            "FAA AC 33.90-1",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Ignition system engineer",
        adversary_position="Proposes single igniter for weight savings",
        counter_arguments=[
            "Single igniter reduces reliability",
            "Certification may be denied",
            "Increased risk of in-flight shutdown"
        ],
        resolution_strategy="Design for redundancy and validate with reliability testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 700 Ignition System, 1997"
    ),
    DoctrineBlock(
        topic="Compressor Rotor Dynamics and Critical Speed Avoidance",
        keywords=["compressor", "rotor dynamics", "critical speed", "AERO04"],
        conclusion_template="AERO04 compressor rotor design must avoid operation at or near critical speeds throughout the engine envelope.",
        reasoning_framework="""
Compressor rotors have natural frequencies (critical speeds) that, if excited, can lead to high vibration and failure. For AERO04, rotor design must ensure that critical speeds are outside the normal operating range, including transients. Finite element analysis and rotor dynamic modeling are required. Validation must include spin pit and engine vibration testing.
""",
        key_factors=[
            "Rotor natural frequencies",
            "Operating speed range",
            "Finite element analysis",
            "Vibration test data",
            "Transient operation"
        ],
        primary_authority=[
            "API 684, Machinery Vibration",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Rotor dynamics engineer",
        adversary_position="Proposes lighter rotor with higher critical speed",
        counter_arguments=[
            "Critical speed within operating range increases risk",
            "Potential for catastrophic failure",
            "Certification may be denied"
        ],
        resolution_strategy="Model and test rotor dynamics; adjust design as needed.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Rotor Dynamics, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Pattern Factor Control",
        keywords=["combustor", "pattern factor", "temperature distribution", "AERO04"],
        conclusion_template="AERO04 combustor must achieve a pattern factor ≤ 0.25 at cruise to ensure uniform turbine inlet temperature.",
        reasoning_framework="""
Pattern factor quantifies the uniformity of temperature at the combustor exit. High pattern factors cause local overheating of turbine blades, reducing life. For AERO04, a pattern factor of 0.25 or less is required at cruise, achieved through optimized fuel nozzle design and liner hole distribution. Validation must include rig and engine testing with temperature mapping.
""",
        key_factors=[
            "Fuel nozzle design",
            "Liner hole distribution",
            "Temperature mapping",
            "Test data",
            "Turbine durability"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Saravanamuttoo, Gas Turbine Theory"
        ],
        burden_holder="Combustor aerodynamics engineer",
        adversary_position="Proposes relaxed pattern factor for easier design",
        counter_arguments=[
            "High pattern factor reduces turbine life",
            "Increases maintenance costs",
            "Certification may be denied"
        ],
        resolution_strategy="Optimize combustor design and validate with temperature mapping.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="V2500 Combustor Pattern Factor, 1993"
    ),
    DoctrineBlock(
        topic="Compressor Blade Aerodynamic Loading Limit",
        keywords=["compressor", "blade loading", "aerodynamics", "AERO04"],
        conclusion_template="AERO04 compressor blade loading must not exceed a diffusion factor of 0.6 to avoid flow separation.",
        reasoning_framework="""
Blade loading is quantified by the diffusion factor, which relates to the risk of flow separation on the blade surface. For AERO04, a maximum diffusion factor of 0.6 is set to ensure robust operation and avoid stall. Blade profiles must be designed and validated through CFD and wind tunnel testing.
""",
        key_factors=[
            "Diffusion factor",
            "Blade profile",
            "CFD analysis",
            "Test data",
            "Stall margin"
        ],
        primary_authority=[
            "Lieblein, Diffusion Factor for Axial Compressor Blades",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Compressor aerodynamicist",
        adversary_position="Proposes higher loading for compact design",
        counter_arguments=[
            "High loading increases stall risk",
            "Reduces surge margin",
            "May require more frequent maintenance"
        ],
        resolution_strategy="Design blades within diffusion factor limits and validate with testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PW4000 Compressor Blade Design, 2001"
    ),
    DoctrineBlock(
        topic="Combustor Altitude Relight Envelope",
        keywords=["combustor", "altitude relight", "envelope", "AERO04"],
        conclusion_template="AERO04 combustor must achieve relight capability up to 30,000 ft and -40°C, per certification requirements.",
        reasoning_framework="""
Altitude relight is a critical safety requirement. For AERO04, the combustor and ignition system must be capable of reliable relight up to 30,000 ft and -40°C ambient. This requires robust atomization, ignition energy, and fuel control. Validation must include altitude chamber and flight testing.
""",
        key_factors=[
            "Altitude and temperature limits",
            "Ignition system performance",
            "Fuel atomization",
            "Test data",
            "Certification requirements"
        ],
        primary_authority=[
            "FAA AC 33.90-1",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor and ignition system engineer",
        adversary_position="Proposes relaxed envelope for easier design",
        counter_arguments=[
            "Non-compliance risks certification",
            "Safety risk in flight",
            "Potential for in-flight shutdown"
        ],
        resolution_strategy="Design and validate relight envelope with altitude testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 700 Altitude Relight, 1997"
    ),
    DoctrineBlock(
        topic="Compressor Blade Erosion Protection",
        keywords=["compressor", "blade erosion", "protection", "AERO04"],
        conclusion_template="AERO04 compressor blades must be coated or treated to resist erosion from airborne particulates.",
        reasoning_framework="""
Compressor blades are exposed to erosion from dust, sand, and other particulates. For AERO04, protective coatings (e.g., titanium nitride) or surface treatments are required to maintain blade profile and efficiency. Erosion resistance must be validated through laboratory and field testing. Maintenance intervals should be established based on erosion rate data.
""",
        key_factors=[
            "Erosion environment",
            "Coating technology",
            "Blade material",
            "Test data",
            "Maintenance intervals"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Donachie, Superalloys"
        ],
        burden_holder="Compressor materials engineer",
        adversary_position="Proposes uncoated blades for cost savings",
        counter_arguments=[
            "Uncoated blades erode faster",
            "Loss of efficiency",
            "Higher maintenance costs"
        ],
        resolution_strategy="Select and validate coatings based on erosion testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFM56 Erosion Protection, 1998"
    ),
    DoctrineBlock(
        topic="Combustor Fuel Atomization Requirement",
        keywords=["combustor", "fuel atomization", "spray quality", "AERO04"],
        conclusion_template="AERO04 combustor fuel nozzles must achieve Sauter Mean Diameter (SMD) ≤ 30 μm for efficient combustion.",
        reasoning_framework="""
Efficient combustion requires fine fuel atomization. For AERO04, fuel nozzles must produce a spray with SMD ≤ 30 μm, ensuring rapid evaporation and mixing. Poor atomization increases emissions and reduces stability. Atomization quality must be validated through laboratory spray testing and engine trials.
""",
        key_factors=[
            "SMD measurement",
            "Nozzle design",
            "Spray pattern",
            "Test data",
            "Combustion efficiency"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Saravanamuttoo, Gas Turbine Theory"
        ],
        burden_holder="Combustor fuel system engineer",
        adversary_position="Proposes larger SMD for simpler nozzle design",
        counter_arguments=[
            "Larger SMD reduces combustion efficiency",
            "Increases emissions",
            "May cause stability issues"
        ],
        resolution_strategy="Design and validate nozzles for SMD ≤ 30 μm.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Fuel Atomization, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Rotor-Stator Clearance Monitoring",
        keywords=["compressor", "rotor-stator clearance", "monitoring", "AERO04"],
        conclusion_template="AERO04 must implement clearance monitoring to detect excessive rotor-stator gap and prevent efficiency loss.",
        reasoning_framework="""
Rotor-stator clearance increases due to wear or thermal distortion, reducing compressor efficiency. For AERO04, clearance monitoring systems (e.g., eddy current sensors) should be installed to provide real-time data. Maintenance actions should be triggered when clearance exceeds defined limits. Validation includes sensor calibration and in-service data analysis.
""",
        key_factors=[
            "Clearance measurement technology",
            "Sensor calibration",
            "Data analysis",
            "Maintenance triggers",
            "Test data"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "FAA AC 33.90-1"
        ],
        burden_holder="Compressor mechanical systems engineer",
        adversary_position="Proposes no monitoring for cost savings",
        counter_arguments=[
            "No monitoring risks undetected efficiency loss",
            "Potential for surge or rubs",
            "Higher maintenance costs"
        ],
        resolution_strategy="Implement and validate clearance monitoring system.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Clearance Monitoring, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Liner Cooling Effectiveness",
        keywords=["combustor", "liner cooling", "effectiveness", "AERO04"],
        conclusion_template="AERO04 combustor liner cooling must maintain metal temperature below 950°C for 20,000 cycle life.",
        reasoning_framework="""
Combustor liner cooling is essential to prevent thermal fatigue and oxidation. For AERO04, cooling effectiveness must be validated to keep liner metal temperature below 950°C, ensuring 20,000 cycle life. Techniques include effusion cooling and optimized hole patterns. Validation includes thermal analysis and cyclic rig testing.
""",
        key_factors=[
            "Cooling technique",
            "Metal temperature",
            "Thermal analysis",
            "Cycle life",
            "Test data"
        ],
        primary_authority=[
            "Donachie, Superalloys",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor cooling design engineer",
        adversary_position="Proposes reduced cooling for higher efficiency",
        counter_arguments=[
            "Reduced cooling increases liner temperature",
            "Shortens component life",
            "Increases maintenance costs"
        ],
        resolution_strategy="Optimize cooling and validate with analysis and testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Combustor Liner Cooling, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Inlet Distortion Tolerance",
        keywords=["compressor", "inlet distortion", "tolerance", "AERO04"],
        conclusion_template="AERO04 compressor must tolerate inlet distortion up to 60° sector with 20% total pressure distortion without surge.",
        reasoning_framework="""
Inlet distortion can occur due to crosswinds, aircraft maneuvers, or damaged inlets. For AERO04, the compressor must tolerate a 60° sector with 20% total pressure distortion without entering surge. Validation includes wind tunnel and engine inlet distortion testing. Control logic may be required to adjust variable geometry in response to distortion.
""",
        key_factors=[
            "Inlet distortion pattern",
            "Compressor surge margin",
            "Test data",
            "Control logic",
            "Certification requirements"
        ],
        primary_authority=[
            "FAA AC 33.90-1",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Compressor aerodynamics and controls engineer",
        adversary_position="Proposes lower tolerance for easier design",
        counter_arguments=[
            "Lower tolerance increases risk of surge",
            "May not meet certification",
            "Safety risk"
        ],
        resolution_strategy="Design and validate for distortion tolerance with testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CF6-80 Inlet Distortion, 2002"
    ),
    DoctrineBlock(
        topic="Combustor Smoke Number Limit",
        keywords=["combustor", "smoke number", "emissions", "AERO04"],
        conclusion_template="AERO04 combustor must achieve a smoke number ≤ 20 at all certified power settings.",
        reasoning_framework="""
Smoke number is a measure of visible particulate emissions. ICAO Annex 16 sets maximum allowable smoke numbers. For AERO04, combustor design must achieve a smoke number ≤ 20 at all power settings, through optimized fuel/air mixing and combustion temperature control. Validation includes emissions testing at all certified points.
""",
        key_factors=[
            "Fuel/air mixing",
            "Combustion temperature",
            "Emissions test data",
            "Certification limits",
            "Combustor design"
        ],
        primary_authority=[
            "ICAO Annex 16, Volume II",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor emissions engineer",
        adversary_position="Proposes relaxed smoke limits for easier design",
        counter_arguments=[
            "Non-compliance risks certification",
            "Increased environmental impact",
            "Potential for operational restrictions"
        ],
        resolution_strategy="Optimize combustor and validate with emissions testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent XWB Smoke Number, 2014"
    ),
    DoctrineBlock(
        topic="Compressor Blade Foreign Object Damage (FOD) Resistance",
        keywords=["compressor", "FOD", "blade resistance", "AERO04"],
        conclusion_template="AERO04 compressor blades must be designed and tested to resist FOD per FAA AC 33.77 requirements.",
        reasoning_framework="""
Foreign object damage (FOD) is a leading cause of compressor blade failure. For AERO04, blade design must include material selection and geometry to resist FOD, and must be validated through impact testing per FAA AC 33.77. Maintenance procedures should include regular inspections and FOD prevention measures.
""",
        key_factors=[
            "Blade material and geometry",
            "Impact test data",
            "Inspection procedures",
            "Certification requirements",
            "Maintenance intervals"
        ],
        primary_authority=[
            "FAA AC 33.77",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Compressor mechanical design engineer",
        adversary_position="Proposes lighter blades with less FOD resistance",
        counter_arguments=[
            "Reduced FOD resistance increases risk of failure",
            "Safety and reliability concerns",
            "Certification may be denied"
        ],
        resolution_strategy="Design and test blades for FOD resistance per standards.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFM56 FOD Resistance, 1998"
    ),
    DoctrineBlock(
        topic="Combustor Acoustic Liner Requirement",
        keywords=["combustor", "acoustic liner", "noise reduction", "AERO04"],
        conclusion_template="AERO04 combustor must incorporate acoustic liners to meet ICAO Annex 16 noise limits.",
        reasoning_framework="""
Aircraft engine noise is regulated by ICAO Annex 16. For AERO04, combustor acoustic liners are required to attenuate combustion noise and meet certification limits. Liner design must be validated through acoustic analysis and engine noise testing. Trade-offs between liner weight, durability, and noise reduction must be balanced.
""",
        key_factors=[
            "Acoustic liner design",
            "Noise attenuation",
            "Test data",
            "Weight and durability",
            "Certification limits"
        ],
        primary_authority=[
            "ICAO Annex 16, Volume I",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor noise and emissions engineer",
        adversary_position="Proposes omitting liners for weight savings",
        counter_arguments=[
            "Omitting liners risks non-compliance",
            "Increased cabin and community noise",
            "Certification may be denied"
        ],
        resolution_strategy="Design and validate liners for required noise attenuation.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Acoustic Liner, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Blade Tip Shroud Design",
        keywords=["compressor", "blade tip shroud", "vibration", "AERO04"],
        conclusion_template="AERO04 compressor blade tip shrouds must be designed to minimize vibration and prevent blade flutter.",
        reasoning_framework="""
Blade tip shrouds reduce vibration and suppress flutter, improving blade life. For AERO04, shroud design must balance aerodynamic losses with vibration reduction. Finite element analysis and engine vibration testing are required to validate design. Shrouds must not increase tip leakage excessively.
""",
        key_factors=[
            "Shroud geometry",
            "Vibration analysis",
            "Aerodynamic losses",
            "Test data",
            "Blade life"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "API 684, Machinery Vibration"
        ],
        burden_holder="Compressor mechanical design engineer",
        adversary_position="Proposes unshrouded blades for lower weight",
        counter_arguments=[
            "Unshrouded blades have higher vibration risk",
            "Potential for flutter and failure",
            "Reduced blade life"
        ],
        resolution_strategy="Design and validate shrouds with analysis and testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Blade Tip Shroud, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Liner Thermal Barrier Coating (TBC) Use",
        keywords=["combustor", "liner", "thermal barrier coating", "TBC", "AERO04"],
        conclusion_template="AERO04 combustor liner must use TBC to extend life and reduce oxidation at high temperatures.",
        reasoning_framework="""
Thermal barrier coatings (TBCs) protect combustor liners from high-temperature oxidation and thermal fatigue. For AERO04, TBC application is required to achieve 20,000 cycle life at high metal temperatures. Coating selection and application process must be validated through laboratory and engine testing.
""",
        key_factors=[
            "TBC material and thickness",
            "Application process",
            "Thermal cycling resistance",
            "Test data",
            "Liner life"
        ],
        primary_authority=[
            "Donachie, Superalloys",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor materials engineer",
        adversary_position="Proposes omitting TBC for cost savings",
        counter_arguments=[
            "Omitting TBC reduces liner life",
            "Increases oxidation and maintenance",
            "Certification may be denied"
        ],
        resolution_strategy="Select and validate TBC for required durability.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Liner TBC, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Casing Thermal Growth Allowance",
        keywords=["compressor", "casing", "thermal growth", "AERO04"],
        conclusion_template="AERO04 compressor casing must be designed to accommodate thermal growth and maintain tip clearance at all conditions.",
        reasoning_framework="""
Compressor casing expands with temperature, affecting tip clearance. For AERO04, casing design must include thermal growth analysis to ensure tip clearance is maintained at all operating conditions. Materials selection and structural design must be validated with thermal/mechanical analysis and engine testing.
""",
        key_factors=[
            "Casing material properties",
            "Thermal analysis",
            "Tip clearance control",
            "Test data",
            "Operating temperature range"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Kurzke, GasTurb 12 Manual"
        ],
        burden_holder="Compressor structural engineer",
        adversary_position="Proposes minimal allowance for weight savings",
        counter_arguments=[
            "Insufficient allowance risks blade rubs",
            "Reduced efficiency",
            "Potential for in-service events"
        ],
        resolution_strategy="Analyze and validate casing growth with testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Casing Growth, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Liner Inspection Interval",
        keywords=["combustor", "liner", "inspection interval", "AERO04"],
        conclusion_template="AERO04 combustor liner must be inspected at intervals not exceeding 5,000 cycles to detect early signs of distress.",
        reasoning_framework="""
Regular inspection of combustor liners is required to detect cracking, oxidation, or TBC spallation. For AERO04, inspection interval is set at 5,000 cycles based on durability analysis and in-service experience. Inspection methods include borescope and non-destructive evaluation. Data should inform maintenance planning and liner replacement.
""",
        key_factors=[
            "Durability analysis",
            "Inspection methods",
            "Cycle life data",
            "Maintenance planning",
            "Test data"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "FAA AC 33.90-1"
        ],
        burden_holder="Maintenance engineering",
        adversary_position="Proposes longer intervals for cost savings",
        counter_arguments=[
            "Longer intervals risk undetected damage",
            "Potential for in-service failure",
            "Higher long-term costs"
        ],
        resolution_strategy="Set and enforce inspection intervals based on data.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Liner Inspection, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Blade Frequency Avoidance",
        keywords=["compressor", "blade frequency", "resonance", "AERO04"],
        conclusion_template="AERO04 compressor blade design must avoid resonance with engine harmonics throughout the operating range.",
        reasoning_framework="""
Blade resonance with engine harmonics can cause high-cycle fatigue and failure. For AERO04, blade natural frequencies must be analyzed and designed to avoid excitation by engine orders. Validation includes finite element analysis and engine vibration testing.
""",
        key_factors=[
            "Blade natural frequency",
            "Engine order analysis",
            "Finite element modeling",
            "Test data",
            "Operating speed range"
        ],
        primary_authority=[
            "API 684, Machinery Vibration",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Compressor mechanical design engineer",
        adversary_position="Proposes lighter blades with higher frequency",
        counter_arguments=[
            "Higher frequency may coincide with engine orders",
            "Increases risk of fatigue failure",
            "Certification may be denied"
        ],
        resolution_strategy="Analyze and validate blade frequencies with testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Blade Frequency, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Fuel Flexibility",
        keywords=["combustor", "fuel flexibility", "alternative fuels", "AERO04"],
        conclusion_template="AERO04 combustor must be capable of operating on approved alternative fuels without exceeding emissions or durability limits.",
        reasoning_framework="""
Alternative fuels (e.g., synthetic paraffinic kerosene) are increasingly used in aviation. For AERO04, combustor design must ensure stable operation and emissions compliance with approved alternative fuels. Validation includes rig and engine testing with representative fuel blends. Durability and maintenance intervals must not be adversely affected.
""",
        key_factors=[
            "Approved fuel list",
            "Combustion stability",
            "Emissions compliance",
            "Durability data",
            "Test results"
        ],
        primary_authority=[
            "ASTM D7566",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor design authority",
        adversary_position="Proposes limiting to conventional Jet A-1",
        counter_arguments=[
            "Limits operational flexibility",
            "May not meet future regulatory requirements",
            "Potential for reduced marketability"
        ],
        resolution_strategy="Design and validate for fuel flexibility with testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent XWB Alternative Fuels, 2014"
    ),
    DoctrineBlock(
        topic="Compressor Blade Damping Requirement",
        keywords=["compressor", "blade damping", "vibration", "AERO04"],
        conclusion_template="AERO04 compressor blades must incorporate damping features to suppress vibration and extend life.",
        reasoning_framework="""
Damping reduces blade vibration and fatigue. For AERO04, damping features such as shrouds, friction dampers, or material selection must be included in blade design. Validation includes vibration analysis and engine testing. Damping effectiveness must be demonstrated for all operating conditions.
""",
        key_factors=[
            "Damping feature design",
            "Vibration analysis",
            "Material selection",
            "Test data",
            "Blade life"
        ],
        primary_authority=[
            "API 684, Machinery Vibration",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Compressor mechanical design engineer",
        adversary_position="Proposes omitting damping for weight savings",
        counter_arguments=[
            "Omitting damping increases vibration",
            "Reduces blade life",
            "Increases maintenance costs"
        ],
        resolution_strategy="Design and validate damping features with testing.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Blade Damping, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Liner Creep Resistance",
        keywords=["combustor", "liner", "creep resistance", "AERO04"],
        conclusion_template="AERO04 combustor liner material must provide sufficient creep resistance for 20,000 cycle life at operating temperature.",
        reasoning_framework="""
Creep is time-dependent deformation under stress at high temperature. For AERO04, liner material must be selected for high creep resistance at operating temperature. Validation includes material testing and life prediction modeling. Maintenance intervals should be based on creep life data.
""",
        key_factors=[
            "Material creep properties",
            "Operating temperature",
            "Life prediction modeling",
            "Test data",
            "Maintenance planning"
        ],
        primary_authority=[
            "Donachie, Superalloys",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor materials engineer",
        adversary_position="Proposes lower-cost material with lower creep resistance",
        counter_arguments=[
            "Lower creep resistance reduces liner life",
            "Increases maintenance costs",
            "Potential for in-service failure"
        ],
        resolution_strategy="Select and validate material for required creep resistance.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Liner Creep, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Blade Coating for Corrosion Resistance",
        keywords=["compressor", "blade coating", "corrosion resistance", "AERO04"],
        conclusion_template="AERO04 compressor blades must be coated for corrosion resistance in marine and humid environments.",
        reasoning_framework="""
Corrosion reduces blade life, especially in marine or humid environments. For AERO04, protective coatings (e.g., aluminum or chromium-based) are required. Coating selection must be validated through environmental exposure testing and in-service data. Maintenance intervals should be adjusted based on corrosion rate.
""",
        key_factors=[
            "Coating material and thickness",
            "Environmental exposure",
            "Test data",
            "Maintenance intervals",
            "Blade life"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Donachie, Superalloys"
        ],
        burden_holder="Compressor materials engineer",
        adversary_position="Proposes omitting coating for cost savings",
        counter_arguments=[
            "Omitting coating reduces blade life",
            "Increases maintenance costs",
            "Potential for in-service failure"
        ],
        resolution_strategy="Select and validate coating for required corrosion resistance.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CF6-80 Corrosion Protection, 2002"
    ),
    DoctrineBlock(
        topic="Combustor Liner Weld Quality Assurance",
        keywords=["combustor", "liner", "weld quality", "AERO04"],
        conclusion_template="AERO04 combustor liner welds must be inspected and certified to meet aerospace quality standards.",
        reasoning_framework="""
Weld quality affects liner durability and safety. For AERO04, all liner welds must be inspected using non-destructive evaluation (NDE) and certified to aerospace standards (e.g., AWS D17.1). Weld procedures and personnel must be qualified. Inspection data should be retained for traceability.
""",
        key_factors=[
            "Weld procedure qualification",
            "NDE methods",
            "Certification standards",
            "Inspection data",
            "Traceability"
        ],
        primary_authority=[
            "AWS D17.1",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor manufacturing engineer",
        adversary_position="Proposes relaxed weld inspection for cost savings",
        counter_arguments=[
            "Relaxed inspection increases risk of weld failure",
            "Potential for in-service events",
            "Certification may be denied"
        ],
        resolution_strategy="Qualify and inspect welds per standards; retain records.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Liner Weld QA, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Blade Manufacturing Tolerance",
        keywords=["compressor", "blade manufacturing", "tolerance", "AERO04"],
        conclusion_template="AERO04 compressor blades must be manufactured to a tolerance of ±0.05 mm on critical dimensions.",
        reasoning_framework="""
Manufacturing tolerance affects aerodynamic performance and balance. For AERO04, critical blade dimensions must be held to ±0.05 mm to ensure performance and avoid vibration. Tolerances must be validated through inspection and statistical process control. Non-conforming blades must be rejected or reworked.
""",
        key_factors=[
            "Critical dimensions",
            "Inspection methods",
            "Statistical process control",
            "Test data",
            "Balance and vibration"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "ISO 9001"
        ],
        burden_holder="Compressor manufacturing engineer",
        adversary_position="Proposes relaxed tolerance for cost savings",
        counter_arguments=[
            "Relaxed tolerance reduces performance",
            "Increases vibration risk",
            "Potential for in-service events"
        ],
        resolution_strategy="Enforce and validate manufacturing tolerance with inspection.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Blade Manufacturing, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Liner Hot Streak Avoidance",
        keywords=["combustor", "liner", "hot streak", "AERO04"],
        conclusion_template="AERO04 combustor design must minimize hot streaks at turbine inlet to avoid local blade overheating.",
        reasoning_framework="""
Hot streaks are localized high-temperature regions at the turbine inlet, causing blade overheating and reduced life. For AERO04, combustor and fuel nozzle design must ensure uniform temperature distribution. Validation includes temperature mapping at combustor exit in rig and engine tests.
""",
        key_factors=[
            "Temperature mapping",
            "Fuel nozzle design",
            "Combustor aerodynamics",
            "Test data",
            "Turbine durability"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "Saravanamuttoo, Gas Turbine Theory"
        ],
        burden_holder="Combustor design engineer",
        adversary_position="Proposes relaxed uniformity for easier design",
        counter_arguments=[
            "Hot streaks reduce turbine life",
            "Increase maintenance costs",
            "Certification may be denied"
        ],
        resolution_strategy="Optimize combustor and nozzle design; validate with temperature mapping.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="V2500 Hot Streak Avoidance, 1993"
    ),
    DoctrineBlock(
        topic="Compressor Blade Surface Finish Requirement",
        keywords=["compressor", "blade surface finish", "roughness", "AERO04"],
        conclusion_template="AERO04 compressor blades must have a surface finish of Ra ≤ 0.8 μm to minimize boundary layer losses.",
        reasoning_framework="""
Surface finish affects boundary layer development and aerodynamic losses. For AERO04, a maximum roughness of Ra ≤ 0.8 μm is required on blade surfaces. Validation includes surface profilometry and inspection. Poor finish increases drag and reduces efficiency.
""",
        key_factors=[
            "Surface roughness measurement",
            "Manufacturing process",
            "Inspection methods",
            "Aerodynamic analysis",
            "Test data"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "ISO 4287"
        ],
        burden_holder="Compressor manufacturing engineer",
        adversary_position="Proposes rougher finish for cost savings",
        counter_arguments=[
            "Rougher finish increases losses",
            "Reduces efficiency",
            "Potential for in-service events"
        ],
        resolution_strategy="Enforce and validate surface finish with inspection.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Blade Surface Finish, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Liner Oxidation Resistance",
        keywords=["combustor", "liner", "oxidation resistance", "AERO04"],
        conclusion_template="AERO04 combustor liner material and coatings must provide oxidation resistance for 20,000 cycle life.",
        reasoning_framework="""
Oxidation reduces liner life at high temperature. For AERO04, material and coating selection must ensure oxidation resistance for 20,000 cycles. Validation includes laboratory and engine testing. Maintenance intervals should be based on oxidation rate data.
""",
        key_factors=[
            "Material and coating selection",
            "Oxidation rate data",
            "Test data",
            "Cycle life",
            "Maintenance planning"
        ],
        primary_authority=[
            "Donachie, Superalloys",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Combustor materials engineer",
        adversary_position="Proposes lower-cost material with lower oxidation resistance",
        counter_arguments=[
            "Lower oxidation resistance reduces liner life",
            "Increases maintenance costs",
            "Potential for in-service failure"
        ],
        resolution_strategy="Select and validate material/coating for required oxidation resistance.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Liner Oxidation, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Blade Leading Edge Radius Control",
        keywords=["compressor", "blade leading edge", "radius control", "AERO04"],
        conclusion_template="AERO04 compressor blade leading edge radius must be controlled to ±0.02 mm for optimal aerodynamic performance.",
        reasoning_framework="""
Leading edge radius affects flow attachment and stall margin. For AERO04, leading edge radius must be controlled to ±0.02 mm. Validation includes inspection and aerodynamic analysis. Poor control increases risk of flow separation and reduces efficiency.
""",
        key_factors=[
            "Leading edge radius measurement",
            "Manufacturing process",
            "Inspection methods",
            "Aerodynamic analysis",
            "Test data"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "ISO 9001"
        ],
        burden_holder="Compressor manufacturing engineer",
        adversary_position="Proposes relaxed control for cost savings",
        counter_arguments=[
            "Relaxed control increases stall risk",
            "Reduces efficiency",
            "Potential for in-service events"
        ],
        resolution_strategy="Enforce and validate leading edge radius control.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE90 Leading Edge Control, 1995"
    ),
    DoctrineBlock(
        topic="Combustor Liner Field Repairability",
        keywords=["combustor", "liner", "field repair", "AERO04"],
        conclusion_template="AERO04 combustor liner design must allow for field repair of minor cracks and TBC damage.",
        reasoning_framework="""
Field repairability reduces maintenance costs and downtime. For AERO04, liner design must allow for repair of minor cracks and TBC damage using approved methods. Repair procedures must be validated and personnel qualified. Repair limits must be defined to ensure continued airworthiness.
""",
        key_factors=[
            "Repair procedure qualification",
            "Repair limits",
            "Personnel qualification",
            "Test data",
            "Maintenance planning"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "FAA AC 43.13-1B"
        ],
        burden_holder="Maintenance engineering",
        adversary_position="Proposes no field repair for cost savings",
        counter_arguments=[
            "No field repair increases downtime",
            "Higher maintenance costs",
            "Reduced operational availability"
        ],
        resolution_strategy="Define and validate field repair procedures and limits.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Liner Field Repair, 2010"
    ),
    DoctrineBlock(
        topic="Compressor Blade Foreign Object Ingestion Detection",
        keywords=["compressor", "blade", "foreign object ingestion", "detection", "AERO04"],
        conclusion_template="AERO04 must implement detection systems or inspection protocols for foreign object ingestion events.",
        reasoning_framework="""
Foreign object ingestion can cause blade damage and performance loss. For AERO04, detection systems (e.g., vibration monitoring) or inspection protocols must be in place to identify ingestion events. Maintenance actions should be triggered based on detection or inspection findings. Validation includes system testing and in-service data analysis.
""",
        key_factors=[
            "Detection system design",
            "Inspection protocols",
            "Maintenance triggers",
            "Test data",
            "In-service data"
        ],
        primary_authority=[
            "FAA AC 33.77",
            "Rolls-Royce, The Jet Engine"
        ],
        burden_holder="Compressor systems engineer",
        adversary_position="Proposes no detection for cost savings",
        counter_arguments=[
            "No detection increases risk of undetected damage",
            "Potential for in-service failure",
            "Higher maintenance costs"
        ],
        resolution_strategy="Implement and validate detection/inspection protocols.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFM56 FOD Detection, 1998"
    ),
    DoctrineBlock(
        topic="Combustor Liner Out-of-Roundness Tolerance",
        keywords=["combustor", "liner", "out-of-roundness", "tolerance", "AERO04"],
        conclusion_template="AERO04 combustor liner out-of-roundness must not exceed 0.5 mm to ensure proper fit and cooling.",
        reasoning_framework="""
Out-of-roundness affects liner fit, cooling, and durability. For AERO04, maximum out-of-roundness is set at 0.5 mm. Validation includes inspection and fit checks during assembly. Excessive out-of-roundness increases risk of hot spots and reduced life.
""",
        key_factors=[
            "Out-of-roundness measurement",
            "Manufacturing process",
            "Inspection methods",
            "Fit checks",
            "Test data"
        ],
        primary_authority=[
            "Rolls-Royce, The Jet Engine",
            "ISO 1101"
        ],
        burden_holder="Combustor manufacturing engineer",
        adversary_position="Proposes relaxed tolerance for cost savings",
        counter_arguments=[
            "Relaxed tolerance increases risk of hot spots",
            "Reduces liner life",
            "Potential for in-service events"
        ],
        resolution_strategy="Enforce and validate out-of-roundness tolerance.",
        entity_scope="AERO04_gas_turbine_engines",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Trent 1000 Liner Out-of-Roundness, 2010"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]