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
        topic="ASME B31.3 Process Piping Code Applicability",
        keywords=["ASME B31.3", "process piping", "code applicability", "chemical plants", "refineries"],
        conclusion_template="ASME B31.3 applies to process piping systems in chemical plants, petroleum refineries, and related processing plants.",
        reasoning_framework="""
        The ASME B31.3 code establishes requirements for the design, materials, fabrication, assembly, erection, examination, inspection, and testing of piping. Applicability is determined by the nature of the facility (process plants), the service conditions (pressure, temperature, fluid type), and the boundaries defined by the code (from the connection to equipment to the point of delivery to the user). Exclusions include power boilers, building services, and pipelines covered by other B31 codes. The code's scope is clarified in Section 300.1, and interpretations by the ASME committee provide further guidance on borderline cases. 
        """,
        key_factors=[
            "Facility type (process plant, refinery, chemical plant)",
            "Fluid service (hazardous, flammable, toxic)",
            "Pressure and temperature conditions",
            "Boundaries of piping system",
            "Exclusions as per ASME B31.3 Section 300.1"
        ],
        primary_authority=["ASME B31.3-2022 Section 300.1", "ASME Interpretations"],
        burden_holder="Project piping engineer",
        adversary_position="Project may argue for less stringent code to reduce cost",
        counter_arguments=[
            "Process safety requirements mandate B31.3 for hazardous fluids",
            "Insurance and regulatory compliance require adherence to B31.3"
        ],
        resolution_strategy="Review facility classification and fluid service; consult ASME B31.3 scope and interpretations.",
        entity_scope="All process piping systems within defined facility boundaries",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B31.3-2022 Section 300.1"
    ),
    DoctrineBlock(
        topic="ASME B31.4 Pipeline Transportation Code",
        keywords=["ASME B31.4", "pipeline", "liquid transportation", "oil pipelines", "code applicability"],
        conclusion_template="ASME B31.4 governs the design and construction of pipelines transporting liquids, including crude oil, refined products, and liquid hydrocarbons.",
        reasoning_framework="""
        ASME B31.4 applies to pipelines transporting liquid hydrocarbons, liquid anhydrous ammonia, and carbon dioxide. The code covers design, materials, construction, inspection, testing, operation, and maintenance. Applicability is determined by the transported fluid and the pipeline's function (transportation, not process). The code excludes piping within process plants, which falls under B31.3, and gas pipelines, which are under B31.8. Section 400.1.1 defines the scope, and regulatory requirements may further specify applicability.
        """,
        key_factors=[
            "Type of fluid transported (liquid hydrocarbons, ammonia, CO2)",
            "Pipeline function (transportation vs. process)",
            "Geographical extent (cross-country, gathering, transmission)",
            "Exclusions (process plant piping, gas pipelines)"
        ],
        primary_authority=["ASME B31.4-2019 Section 400.1.1", "49 CFR Part 195"],
        burden_holder="Pipeline design engineer",
        adversary_position="Project may seek to apply less stringent code for cost savings",
        counter_arguments=[
            "Federal regulations require B31.4 for liquid pipelines",
            "Insurance and public safety concerns mandate compliance"
        ],
        resolution_strategy="Verify fluid type and pipeline function; consult B31.4 scope and federal regulations.",
        entity_scope="All liquid transportation pipelines outside process plants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME B31.4-2019 Section 400.1.1"
    ),
    DoctrineBlock(
        topic="ASME B31.8 Gas Transmission and Distribution",
        keywords=["ASME B31.8", "gas pipeline", "transmission", "distribution", "natural gas"],
        conclusion_template="ASME B31.8 applies to the design, construction, and operation of gas transmission and distribution pipelines.",
        reasoning_framework="""
        The ASME B31.8 code covers pipelines transporting natural gas, hydrogen, and other gases. It applies to transmission and distribution systems, including gathering lines, compressor stations, and related facilities. The code excludes piping within process plants (B31.3) and liquid pipelines (B31.4). Section 800.1.1 defines the scope, and federal regulations (49 CFR Part 192) mandate compliance for public safety. The code addresses design pressure, material selection, welding, testing, and integrity management.
        """,
        key_factors=[
            "Type of gas transported",
            "Pipeline function (transmission, distribution, gathering)",
            "Geographical extent",
            "Exclusions (process plant piping, liquid pipelines)"
        ],
        primary_authority=["ASME B31.8-2020 Section 800.1.1", "49 CFR Part 192"],
        burden_holder="Gas pipeline engineer",
        adversary_position="Project may argue for less stringent code",
        counter_arguments=[
            "Federal law requires B31.8 for gas pipelines",
            "Public safety and environmental protection"
        ],
        resolution_strategy="Confirm gas type and pipeline function; consult B31.8 scope and federal regulations.",
        entity_scope="All gas transmission and distribution pipelines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B31.8-2020 Section 800.1.1"
    ),
    DoctrineBlock(
        topic="Pipe Sizing for Liquid Flow - Darcy-Weisbach Equation",
        keywords=["pipe sizing", "Darcy-Weisbach", "liquid flow", "pressure drop", "hydraulics"],
        conclusion_template="The Darcy-Weisbach equation is used to calculate pressure drop and determine pipe size for liquid flow in process and pipeline systems.",
        reasoning_framework="""
        The Darcy-Weisbach equation relates pressure drop to flow rate, pipe diameter, length, fluid density, and friction factor. It is applicable to both laminar and turbulent flow regimes. The friction factor is determined from the Moody chart or Colebrook-White equation, depending on Reynolds number and pipe roughness. Pipe sizing involves selecting a diameter that limits velocity and pressure drop within acceptable limits, considering pump capacity and process requirements. The equation provides a rigorous, general approach suitable for all fluids.
        """,
        key_factors=[
            "Required flow rate",
            "Allowable pressure drop",
            "Fluid properties (density, viscosity)",
            "Pipe length and roughness",
            "Friction factor determination"
        ],
        primary_authority=["Crane TP-410", "Perry's Chemical Engineers' Handbook, Section 6"],
        burden_holder="Piping hydraulics engineer",
        adversary_position="Project may propose empirical methods for simplicity",
        counter_arguments=[
            "Darcy-Weisbach is universally applicable and accurate",
            "Empirical methods may not apply to all fluids"
        ],
        resolution_strategy="Use Darcy-Weisbach for all non-water fluids and critical applications.",
        entity_scope="All liquid process and pipeline systems",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Crane TP-410"
    ),
    DoctrineBlock(
        topic="Hazen-Williams Equation for Water Flow",
        keywords=["Hazen-Williams", "water flow", "pipe sizing", "pressure drop", "empirical equation"],
        conclusion_template="The Hazen-Williams equation is used for sizing pipes and calculating pressure drop in water systems at moderate temperatures.",
        reasoning_framework="""
        The Hazen-Williams equation is an empirical formula for calculating pressure drop and velocity of water in pipes. It is valid for water at temperatures between 40°F and 75°F, and for turbulent flow in relatively smooth pipes. The equation is not suitable for fluids other than water or for high viscosity, high temperature, or laminar flow conditions. It is widely used for municipal water distribution and fire protection systems due to its simplicity.
        """,
        key_factors=[
            "Fluid type (water only)",
            "Temperature range",
            "Pipe material and roughness",
            "Flow regime (turbulent)",
            "System application (municipal, fire protection)"
        ],
        primary_authority=["AWWA M11", "NFPA 13"],
        burden_holder="Water system designer",
        adversary_position="Use of Hazen-Williams for non-water fluids",
        counter_arguments=[
            "Equation is not valid for fluids other than water",
            "Darcy-Weisbach is preferred for other fluids"
        ],
        resolution_strategy="Limit Hazen-Williams to water systems within specified conditions.",
        entity_scope="Municipal water and fire protection piping",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AWWA M11"
    ),
    DoctrineBlock(
        topic="Pipe Schedule and Wall Thickness Calculation",
        keywords=["pipe schedule", "wall thickness", "pressure design", "ASME B31.3", "corrosion allowance"],
        conclusion_template="Pipe wall thickness is determined based on internal pressure, material strength, corrosion allowance, and mechanical loads, following ASME B31.3 or relevant code.",
        reasoning_framework="""
        Pipe wall thickness is calculated using the formulae in ASME B31.3 Section 304.1. The minimum required thickness is based on design pressure, allowable stress, pipe diameter, and joint efficiency. Additional thickness is added for corrosion and mechanical loads (e.g., bending, external pressure). The selected schedule must meet or exceed the calculated thickness. Verification against manufacturer pipe schedules (ASME B36.10/36.19) ensures availability. Special attention is required for high-pressure, high-temperature, or corrosive services.
        """,
        key_factors=[
            "Design pressure and temperature",
            "Pipe material and allowable stress",
            "Corrosion and erosion allowance",
            "Mechanical loads (external, bending)",
            "Manufactured pipe schedules"
        ],
        primary_authority=["ASME B31.3 Section 304.1", "ASME B36.10/36.19"],
        burden_holder="Piping design engineer",
        adversary_position="Selection of thinner wall for cost savings",
        counter_arguments=[
            "Code minimums must be met for safety",
            "Corrosion and mechanical loads require additional thickness"
        ],
        resolution_strategy="Calculate required thickness; select next higher standard schedule.",
        entity_scope="All process and pipeline piping",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 304.1"
    ),
    DoctrineBlock(
        topic="Material Specifications - Carbon Steel Pipe",
        keywords=["carbon steel", "pipe material", "ASTM A106", "ASTM A53", "material selection"],
        conclusion_template="ASTM A106 and A53 are the standard specifications for seamless and welded carbon steel pipe in process and pipeline applications.",
        reasoning_framework="""
        Material selection for carbon steel pipe is governed by ASME B31.3 and B31.4/8, which reference ASTM standards. ASTM A106 covers seamless carbon steel pipe for high-temperature service, while ASTM A53 covers both seamless and welded pipe for general use. Selection depends on service conditions, required mechanical properties, and code requirements. Material must be traceable, certified, and meet specified chemical and mechanical properties. Impact testing may be required for low-temperature service.
        """,
        key_factors=[
            "Service temperature and pressure",
            "Required mechanical properties",
            "Seamless vs. welded construction",
            "Code and client requirements",
            "Material traceability"
        ],
        primary_authority=["ASTM A106", "ASTM A53", "ASME B31.3 Table A-1"],
        burden_holder="Materials engineer",
        adversary_position="Use of non-standard or unlisted materials",
        counter_arguments=[
            "Code requires listed materials for pressure piping",
            "Non-listed materials require additional qualification"
        ],
        resolution_strategy="Select ASTM A106 or A53 as appropriate; ensure certification and traceability.",
        entity_scope="All carbon steel process and pipeline piping",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Table A-1"
    ),
    DoctrineBlock(
        topic="Low-Temperature Carbon Steel - ASTM A333",
        keywords=["low temperature", "carbon steel", "ASTM A333", "impact testing", "cryogenic"],
        conclusion_template="ASTM A333 is the standard specification for seamless and welded carbon steel pipe for low-temperature service, requiring impact testing.",
        reasoning_framework="""
        For piping operating below -29°C (-20°F), ASME B31.3 and B31.8 require materials with proven toughness at low temperatures. ASTM A333 specifies chemical composition, mechanical properties, and mandatory Charpy V-notch impact testing at the minimum design temperature. Material must be properly marked and certified. Substitution of standard carbon steel (A106/A53) is not permitted for low-temperature service without additional qualification.
        """,
        key_factors=[
            "Minimum design temperature",
            "Required impact toughness",
            "Material certification and testing",
            "Code requirements for low-temperature service"
        ],
        primary_authority=["ASTM A333", "ASME B31.3 Section 323.2.2"],
        burden_holder="Materials engineer",
        adversary_position="Use of standard carbon steel without impact testing",
        counter_arguments=[
            "Code prohibits use of unqualified materials at low temperature",
            "Impact testing ensures safe operation"
        ],
        resolution_strategy="Specify ASTM A333 for all low-temperature piping; verify certification and test results.",
        entity_scope="All low-temperature carbon steel piping",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 323.2.2"
    ),
    DoctrineBlock(
        topic="Stainless Steel Pipe - ASTM A312 Austenitic Grades",
        keywords=["stainless steel", "ASTM A312", "austenitic", "corrosion resistance", "material specification"],
        conclusion_template="ASTM A312 covers seamless and welded austenitic stainless steel pipe for corrosion-resistant service in process and pipeline systems.",
        reasoning_framework="""
        Austenitic stainless steels (such as 304, 304L, 316, 316L) are specified for corrosion resistance in process piping. ASTM A312 defines chemical composition, mechanical properties, and manufacturing methods for seamless and welded pipe. Selection is based on fluid corrosivity, temperature, and code requirements. Low-carbon grades (L) are preferred for welded construction to minimize sensitization. Material must be certified and traceable.
        """,
        key_factors=[
            "Corrosive nature of process fluid",
            "Temperature and pressure",
            "Welded vs. seamless pipe",
            "Low-carbon grades for welding",
            "Material certification"
        ],
        primary_authority=["ASTM A312", "ASME B31.3 Table A-1"],
        burden_holder="Materials engineer",
        adversary_position="Use of non-austenitic or unlisted grades",
        counter_arguments=[
            "Austenitic grades offer superior corrosion resistance",
            "Code requires listed materials"
        ],
        resolution_strategy="Specify ASTM A312 austenitic grades for corrosion-resistant service.",
        entity_scope="All stainless steel process and pipeline piping",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Table A-1"
    ),
    DoctrineBlock(
        topic="Duplex Stainless Steel - ASTM A790",
        keywords=["duplex stainless", "ASTM A790", "corrosion resistance", "high strength", "material specification"],
        conclusion_template="ASTM A790 covers seamless and welded duplex stainless steel pipe for high strength and corrosion resistance in demanding applications.",
        reasoning_framework="""
        Duplex stainless steels (e.g., 2205, 2507) combine high strength and excellent resistance to chloride stress corrosion cracking. ASTM A790 specifies requirements for duplex grades, including chemical composition, mechanical properties, and manufacturing. Selection is driven by process conditions (chlorides, high pressure), and welding procedures must preserve duplex microstructure. Material must be certified and meet code requirements. Additional testing (e.g., ferrite content, pitting resistance) may be required.
        """,
        key_factors=[
            "Chloride concentration and corrosion risk",
            "Required mechanical strength",
            "Welding procedures and qualification",
            "Material certification and testing"
        ],
        primary_authority=["ASTM A790", "ASME B31.3 Table A-1"],
        burden_holder="Materials engineer",
        adversary_position="Use of austenitic grades in high-chloride service",
        counter_arguments=[
            "Duplex grades offer superior resistance to chloride attack",
            "Code requires listed materials and proper welding"
        ],
        resolution_strategy="Specify ASTM A790 duplex grades for high-chloride or high-strength applications.",
        entity_scope="All duplex stainless steel piping",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Table A-1"
    ),
    DoctrineBlock(
        topic="Flange Ratings and Selection - ASME B16.5",
        keywords=["flange", "ASME B16.5", "pressure class", "rating", "selection"],
        conclusion_template="Flange selection is based on ASME B16.5 pressure class, material group, and service conditions to ensure compatibility and safety.",
        reasoning_framework="""
        ASME B16.5 defines dimensions, pressure-temperature ratings, and materials for pipe flanges and flanged fittings. Flange class (150, 300, 600, etc.) is selected based on design pressure, temperature, and material group. Compatibility with pipe material and gasket type is essential. Flange facing (RF, RTJ, FF) is chosen based on service and leakage risk. Verification against pressure-temperature tables in B16.5 ensures compliance. Flange selection must consider corrosion, cyclic loading, and connected equipment.
        """,
        key_factors=[
            "Design pressure and temperature",
            "Flange material group",
            "Required pressure class",
            "Facing type and gasket compatibility",
            "Corrosion and cyclic loading"
        ],
        primary_authority=["ASME B16.5", "ASME B31.3 Section 304.5"],
        burden_holder="Piping designer",
        adversary_position="Use of lower class or non-standard flanges",
        counter_arguments=[
            "Code requires rated flanges for design conditions",
            "Improper selection can lead to leakage or failure"
        ],
        resolution_strategy="Select flange class and material per ASME B16.5 tables for design conditions.",
        entity_scope="All flanged piping connections",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="ASME B16.5"
    ),
    DoctrineBlock(
        topic="Gasket Selection - Spiral Wound, Ring Joint, Compressed Fiber",
        keywords=["gasket", "spiral wound", "ring joint", "compressed fiber", "leakage prevention"],
        conclusion_template="Gasket type is selected based on flange facing, pressure class, temperature, and fluid compatibility to ensure leak-tight joints.",
        reasoning_framework="""
        Gasket selection depends on flange facing (RF, RTJ, FF), pressure and temperature rating, and process fluid. Spiral wound gaskets are preferred for raised face flanges in moderate to high pressure/temperature service. Ring joint gaskets are used with RTJ flanges for high-pressure, critical applications. Compressed fiber gaskets are suitable for low-pressure, non-critical services. Material compatibility with process fluid is essential to prevent degradation. ASME B16.20 and B16.21 provide standards for gasket dimensions and materials.
        """,
        key_factors=[
            "Flange facing type",
            "Design pressure and temperature",
            "Process fluid compatibility",
            "Gasket material and construction",
            "Service criticality"
        ],
        primary_authority=["ASME B16.20", "ASME B16.21"],
        burden_holder="Piping designer",
        adversary_position="Use of non-compatible or low-grade gaskets",
        counter_arguments=[
            "Improper gasket selection leads to leakage",
            "Code and standards require compatible gaskets"
        ],
        resolution_strategy="Select gasket type and material per ASME B16.20/21 and service requirements.",
        entity_scope="All flanged piping joints",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B16.20"
    ),
    DoctrineBlock(
        topic="Pipe Stress Analysis - Sustained, Thermal Expansion, Occasional Loads",
        keywords=["pipe stress", "thermal expansion", "sustained loads", "occasional loads", "ASME B31.3"],
        conclusion_template="Pipe stress analysis must consider sustained, thermal expansion, and occasional loads to ensure code compliance and safe operation.",
        reasoning_framework="""
        ASME B31.3 Section 319 requires analysis of piping systems for sustained loads (weight, pressure), thermal expansion, and occasional loads (wind, earthquake). The allowable stresses for each load case are defined in the code. Expansion loops, anchors, and flexible supports are used to control thermal stresses. Computer analysis (e.g., CAESAR II) is typically employed for complex systems. Documentation of analysis and compliance with code limits is mandatory.
        """,
        key_factors=[
            "System layout and flexibility",
            "Operating and design temperatures",
            "Support and anchor locations",
            "External loads (wind, seismic)",
            "Allowable stress limits"
        ],
        primary_authority=["ASME B31.3 Section 319", "ASME B31.1 Section 121"],
        burden_holder="Pipe stress analyst",
        adversary_position="Neglecting thermal or occasional loads",
        counter_arguments=[
            "Code requires consideration of all load cases",
            "Failure to analyze can lead to fatigue or rupture"
        ],
        resolution_strategy="Perform comprehensive stress analysis per ASME B31.3 Section 319.",
        entity_scope="All process piping systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 319"
    ),
    DoctrineBlock(
        topic="Pipe Support Design - Types and Applications",
        keywords=["pipe support", "hanger", "restraint", "spring support", "design"],
        conclusion_template="Pipe supports are selected and designed based on load, movement, and environmental conditions to ensure system integrity.",
        reasoning_framework="""
        Pipe supports include rigid hangers, guides, anchors, and spring supports. Selection depends on pipe size, weight, thermal movement, and external loads. Supports must prevent excessive deflection, vibration, and stress. ASME B31.1 and B31.3 provide guidance on support spacing and design. Special supports (e.g., variable or constant spring hangers) are used for large thermal movements. Corrosion protection and environmental considerations (outdoor, offshore) are addressed in support design.
        """,
        key_factors=[
            "Pipe weight and size",
            "Thermal movement and expansion",
            "Support spacing and type",
            "Environmental exposure",
            "Vibration and dynamic loads"
        ],
        primary_authority=["ASME B31.1 Section 121", "ASME B31.3 Section 321"],
        burden_holder="Piping support designer",
        adversary_position="Under-designing supports to reduce cost",
        counter_arguments=[
            "Inadequate supports lead to excessive stress and failure",
            "Code requires proper support design"
        ],
        resolution_strategy="Design supports per code and project requirements; verify with stress analysis.",
        entity_scope="All supported piping systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 321"
    ),
    DoctrineBlock(
        topic="ASME B16.9 Fittings - Elbows, Tees, Reducers, Caps",
        keywords=["ASME B16.9", "fittings", "elbows", "tees", "reducers", "caps"],
        conclusion_template="ASME B16.9 fittings are used for butt-welded connections and must conform to dimensional and material requirements for pressure piping.",
        reasoning_framework="""
        ASME B16.9 covers factory-made wrought steel butt-welding fittings, including elbows, tees, reducers, and caps. Fittings must meet dimensional tolerances, wall thickness, and material specifications compatible with the connected pipe. Use of B16.9 fittings ensures code compliance and reliable welded joints. Non-standard or fabricated fittings require additional qualification and approval. Material certification and traceability are mandatory.
        """,
        key_factors=[
            "Fitting type and configuration",
            "Material compatibility",
            "Dimensional and wall thickness requirements",
            "Certification and traceability",
            "Code compliance"
        ],
        primary_authority=["ASME B16.9", "ASME B31.3 Section 304.2"],
        burden_holder="Piping designer",
        adversary_position="Use of non-standard or fabricated fittings",
        counter_arguments=[
            "ASME B16.9 ensures quality and compatibility",
            "Non-standard fittings require additional qualification"
        ],
        resolution_strategy="Specify ASME B16.9 fittings for all butt-welded connections.",
        entity_scope="All butt-welded piping systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B16.9"
    ),
    DoctrineBlock(
        topic="Pipe Welding - WPS, PQR, Welder Qualification",
        keywords=["pipe welding", "WPS", "PQR", "welder qualification", "ASME IX"],
        conclusion_template="Pipe welding must be performed in accordance with qualified WPS and PQR, and by welders certified per ASME Section IX.",
        reasoning_framework="""
        Welding Procedure Specifications (WPS) and Procedure Qualification Records (PQR) are required for all pressure piping welds. Welders must be qualified for the process, position, and material per ASME Section IX. WPS defines essential variables, joint design, and inspection requirements. PQR documents test results for procedure qualification. Welder performance qualification ensures skill and compliance. All records must be maintained and traceable.
        """,
        key_factors=[
            "Welding process and procedure",
            "Material and thickness range",
            "Welder qualification and certification",
            "Documentation and traceability",
            "Inspection and testing"
        ],
        primary_authority=["ASME Section IX", "ASME B31.3 Section 328"],
        burden_holder="Welding engineer",
        adversary_position="Use of unqualified procedures or welders",
        counter_arguments=[
            "Code requires qualified procedures and personnel",
            "Unqualified welding risks failure and non-compliance"
        ],
        resolution_strategy="Ensure all welding is per qualified WPS/PQR and by certified welders.",
        entity_scope="All welded piping systems",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="ASME Section IX"
    ),
    DoctrineBlock(
        topic="Two-Phase Flow in Pipelines - Flow Regimes and Baker Chart",
        keywords=["two-phase flow", "flow regime", "Baker chart", "gas-liquid", "pipeline"],
        conclusion_template="Two-phase flow regime identification using the Baker chart is essential for accurate pressure drop and flow assurance calculations in pipelines.",
        reasoning_framework="""
        Two-phase (gas-liquid) flow in pipelines exhibits different regimes (slug, annular, stratified, bubbly) that affect pressure drop, flow stability, and erosion risk. The Baker chart provides a graphical method to predict flow regime based on superficial velocities of gas and liquid. Correct regime identification informs selection of pressure drop correlations and mitigation of flow assurance issues (e.g., slugging, liquid holdup). Empirical correlations and field data are used for validation.
        """,
        key_factors=[
            "Gas and liquid flow rates",
            "Pipe diameter and inclination",
            "Fluid properties",
            "Operating pressure and temperature",
            "Empirical regime maps (Baker chart)"
        ],
        primary_authority=["Baker, O. (1954)", "API RP 14E"],
        burden_holder="Pipeline hydraulics engineer",
        adversary_position="Neglecting flow regime effects",
        counter_arguments=[
            "Incorrect regime prediction leads to design errors",
            "Industry practice requires regime identification"
        ],
        resolution_strategy="Use Baker chart for initial regime prediction; validate with field data.",
        entity_scope="All two-phase pipeline systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Baker, O. (1954)"
    ),
    DoctrineBlock(
        topic="Pipeline Pigging - Cleaning and Inspection",
        keywords=["pipeline pigging", "cleaning", "inspection", "maintenance", "pipeline integrity"],
        conclusion_template="Pipeline pigging is required for cleaning, inspection, and maintenance of pipelines to ensure integrity and compliance with regulations.",
        reasoning_framework="""
        Pigging involves inserting a device (pig) into the pipeline to clean, inspect, or separate fluids. Regular pigging removes deposits, prevents corrosion, and allows in-line inspection (ILI) for wall thickness and defects. Regulatory requirements (e.g., 49 CFR Part 195/192) mandate periodic pigging for certain pipelines. Pig launcher and receiver facilities must be designed for safe operation. Pig selection depends on pipeline diameter, configuration, and service.
        """,
        key_factors=[
            "Pipeline diameter and configuration",
            "Service fluid and deposit risk",
            "Regulatory requirements",
            "Pig type and compatibility",
            "Launcher and receiver design"
        ],
        primary_authority=["API RP 1163", "49 CFR Part 195/192"],
        burden_holder="Pipeline operations engineer",
        adversary_position="Omitting pigging to reduce OPEX",
        counter_arguments=[
            "Pigging is required for integrity management",
            "Neglect increases risk of failure and regulatory penalties"
        ],
        resolution_strategy="Implement pigging program per regulatory and industry standards.",
        entity_scope="All pipelines subject to cleaning and inspection",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API RP 1163"
    ),
    DoctrineBlock(
        topic="Cathodic Protection for Buried Pipelines",
        keywords=["cathodic protection", "buried pipeline", "corrosion control", "impressed current", "sacrificial anode"],
        conclusion_template="Cathodic protection is required for buried pipelines to prevent external corrosion, using impressed current or sacrificial anode systems.",
        reasoning_framework="""
        Buried steel pipelines are susceptible to external corrosion. Cathodic protection (CP) applies a direct current to counteract corrosion reactions. Impressed current systems use rectifiers and anodes; sacrificial anode systems use reactive metals. CP system design considers soil resistivity, pipeline coating, and current requirements. Monitoring and testing (e.g., pipe-to-soil potential) are required to ensure effectiveness. Regulatory standards (NACE SP0169, 49 CFR Part 195/192) mandate CP for buried pipelines.
        """,
        key_factors=[
            "Pipeline material and coating",
            "Soil resistivity and environment",
            "CP system type and design",
            "Monitoring and maintenance",
            "Regulatory compliance"
        ],
        primary_authority=["NACE SP0169", "49 CFR Part 195/192"],
        burden_holder="Pipeline corrosion engineer",
        adversary_position="Relying solely on coatings for corrosion protection",
        counter_arguments=[
            "Coatings alone are insufficient for long-term protection",
            "Regulations require cathodic protection"
        ],
        resolution_strategy="Design and maintain CP system per NACE and regulatory standards.",
        entity_scope="All buried steel pipelines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE SP0169"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management - ASME B31.8S and 49 CFR Part 192",
        keywords=["pipeline integrity", "management", "ASME B31.8S", "49 CFR Part 192", "risk assessment"],
        conclusion_template="Pipeline integrity management programs are required to assess, monitor, and mitigate risks to pipeline safety and reliability.",
        reasoning_framework="""
        ASME B31.8S and 49 CFR Part 192 require operators to implement integrity management programs (IMP) for gas pipelines. IMP includes risk assessment, baseline assessment (ILI, hydrotest), ongoing monitoring, and mitigation of identified threats (corrosion, third-party damage, geohazards). Documentation, data integration, and periodic reassessment are mandatory. High Consequence Areas (HCA) require enhanced assessment and mitigation. Non-compliance can result in regulatory penalties and increased risk of failure.
        """,
        key_factors=[
            "Pipeline location and HCA designation",
            "Threat identification and risk assessment",
            "Assessment methods (ILI, hydrotest, direct assessment)",
            "Mitigation and repair actions",
            "Documentation and regulatory compliance"
        ],
        primary_authority=["ASME B31.8S", "49 CFR Part 192 Subpart O"],
        burden_holder="Pipeline integrity manager",
        adversary_position="Minimal compliance or reactive management",
        counter_arguments=[
            "Proactive IMP reduces failure risk and liability",
            "Regulations mandate comprehensive IMP"
        ],
        resolution_strategy="Implement and maintain IMP per ASME B31.8S and federal regulations.",
        entity_scope="All regulated gas pipelines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME B31.8S"
    ),
    DoctrineBlock(
        topic="Oilfield Flowline and Gathering System Design",
        keywords=["oilfield", "flowline", "gathering system", "API RP 14E", "design"],
        conclusion_template="Oilfield flowlines and gathering systems are designed per API RP 14E, considering multiphase flow, erosion, and corrosion risks.",
        reasoning_framework="""
        Oilfield flowlines transport multiphase fluids from wells to processing facilities. API RP 14E provides guidelines for sizing, velocity limits (to prevent erosion), and corrosion control. Design considers fluid composition, pressure, temperature, and potential for slugging. Materials are selected for compatibility with produced fluids (CO2, H2S). Corrosion inhibition and pigging provisions are included. Regulatory and operator standards may impose additional requirements.
        """,
        key_factors=[
            "Fluid composition and phase behavior",
            "Erosion and corrosion risk",
            "Velocity and pressure drop limits",
            "Material selection",
            "Pigging and corrosion inhibition"
        ],
        primary_authority=["API RP 14E", "ASME B31.4"],
        burden_holder="Oilfield facilities engineer",
        adversary_position="Oversizing or undersizing lines for cost or production",
        counter_arguments=[
            "Improper sizing increases erosion or flow assurance risks",
            "API RP 14E provides industry-accepted guidelines"
        ],
        resolution_strategy="Design per API RP 14E and operator standards; validate with flow assurance analysis.",
        entity_scope="All oilfield flowlines and gathering systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 14E"
    ),
    # Additional doctrine blocks to reach 40+ entries
    DoctrineBlock(
        topic="Pipe Corrosion Allowance Determination",
        keywords=["corrosion allowance", "pipe design", "material loss", "lifetime", "ASME B31.3"],
        conclusion_template="A corrosion allowance is added to pipe wall thickness based on expected material loss during service life, per code and client requirements.",
        reasoning_framework="""
        Corrosion allowance compensates for expected wall loss due to internal and external corrosion. The value is determined from process fluid corrosivity, anticipated service life, inspection frequency, and historical data. ASME B31.3 does not mandate a specific value but requires consideration of corrosion in thickness calculations. Typical values range from 1.5 to 3 mm for carbon steel. For non-corrosive fluids or corrosion-resistant alloys, the allowance may be reduced or omitted.
        """,
        key_factors=[
            "Process fluid corrosivity",
            "Anticipated service life",
            "Inspection and maintenance frequency",
            "Material selection",
            "Historical corrosion data"
        ],
        primary_authority=["ASME B31.3 Section 301.2.2", "API 570"],
        burden_holder="Piping design engineer",
        adversary_position="Minimizing allowance to reduce cost",
        counter_arguments=[
            "Insufficient allowance increases risk of failure",
            "Industry practice supports conservative values"
        ],
        resolution_strategy="Determine allowance based on fluid, material, and client standards.",
        entity_scope="All process and pipeline piping",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 301.2.2"
    ),
    DoctrineBlock(
        topic="Pipe Joint Efficiency in Wall Thickness Calculations",
        keywords=["joint efficiency", "welded pipe", "wall thickness", "ASME B31.3", "seam type"],
        conclusion_template="Joint efficiency is applied in wall thickness calculations based on pipe seam type and inspection, per ASME B31.3 Table A-1B.",
        reasoning_framework="""
        Welded pipe may have reduced strength at the seam. ASME B31.3 assigns joint efficiency factors (E) based on seam type (ERW, SAW, seamless) and extent of radiographic inspection. Seamless pipe has E=1.0; ERW and SAW have E<1.0 unless fully inspected. The selected E value directly affects calculated minimum wall thickness. Documentation of inspection and pipe certification is required.
        """,
        key_factors=[
            "Pipe manufacturing process",
            "Extent of NDE (radiography)",
            "Code-assigned joint efficiency",
            "Documentation and certification"
        ],
        primary_authority=["ASME B31.3 Table A-1B"],
        burden_holder="Piping design engineer",
        adversary_position="Assuming E=1.0 for all pipes",
        counter_arguments=[
            "Code assigns lower E for uninspected seams",
            "Overestimating E risks under-designed pipe"
        ],
        resolution_strategy="Apply joint efficiency per code and inspection records.",
        entity_scope="All welded process and pipeline piping",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Table A-1B"
    ),
    DoctrineBlock(
        topic="Minimum Pipe Slope for Drainage",
        keywords=["pipe slope", "drainage", "gravity flow", "minimum slope", "ASME B31.3"],
        conclusion_template="Minimum pipe slope is provided to ensure gravity drainage of liquids, typically 1:100 (1%) or as required by process.",
        reasoning_framework="""
        For gravity drainage, a minimum slope is required to prevent liquid accumulation and ensure flow. ASME B31.3 does not specify a universal value, but industry practice is 1:100 (1%) for process drains. Greater slope may be needed for viscous fluids or long runs. Slope must be maintained throughout the run, verified by field survey. Local codes or client standards may impose stricter requirements.
        """,
        key_factors=[
            "Fluid type and viscosity",
            "Pipe length and configuration",
            "Process requirements",
            "Client or local standards"
        ],
        primary_authority=["ASME B31.3", "API 650"],
        burden_holder="Piping designer",
        adversary_position="Reducing slope to minimize elevation change",
        counter_arguments=[
            "Insufficient slope leads to pooling and corrosion",
            "Industry standards support 1% minimum"
        ],
        resolution_strategy="Provide minimum 1% slope unless otherwise justified.",
        entity_scope="All gravity drain piping",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Industry practice"
    ),
    DoctrineBlock(
        topic="Pipe Expansion Loops and Offsets",
        keywords=["expansion loop", "thermal expansion", "pipe flexibility", "ASME B31.3", "offset"],
        conclusion_template="Expansion loops and offsets are used to accommodate thermal expansion in long piping runs, per flexibility analysis.",
        reasoning_framework="""
        Thermal expansion in long, straight piping can cause excessive stress and displacement. Expansion loops or offsets provide flexibility to absorb movement. ASME B31.3 Section 319 requires analysis of thermal expansion and provision of adequate flexibility. The size and location of loops are determined by calculation or software analysis. Expansion joints may be used where loops are impractical, but require careful design and maintenance.
        """,
        key_factors=[
            "Pipe length and temperature change",
            "System layout and anchor points",
            "Flexibility analysis results",
            "Space constraints",
            "Expansion joint suitability"
        ],
        primary_authority=["ASME B31.3 Section 319", "Piping Handbook (Mohinder Nayyar)"],
        burden_holder="Pipe stress analyst",
        adversary_position="Omitting loops to save space",
        counter_arguments=[
            "Lack of flexibility leads to overstress and failure",
            "Code requires expansion analysis"
        ],
        resolution_strategy="Provide loops or offsets as indicated by flexibility analysis.",
        entity_scope="Long, straight piping runs subject to thermal expansion",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 319"
    ),
    DoctrineBlock(
        topic="Allowable Pipe Span Between Supports",
        keywords=["pipe span", "support spacing", "deflection", "ASME B31.1", "ASME B31.3"],
        conclusion_template="Allowable span between pipe supports is determined by pipe size, material, and loading, per code and industry tables.",
        reasoning_framework="""
        Support spacing is based on pipe size, material, fluid weight, and allowable deflection. ASME B31.1 and B31.3 provide guidance, but detailed tables (e.g., MSS SP-69) are commonly used. Spans are reduced for insulated, water-filled, or high-temperature lines. Excessive span causes sagging, overstress, and vibration. Field conditions (wind, seismic, valves) may require closer spacing.
        """,
        key_factors=[
            "Pipe size and material",
            "Operating condition (empty, full, insulated)",
            "Allowable deflection",
            "External loads (valves, wind, seismic)",
            "Industry span tables"
        ],
        primary_authority=["MSS SP-69", "ASME B31.1 Section 121.5"],
        burden_holder="Piping support designer",
        adversary_position="Increasing span to reduce number of supports",
        counter_arguments=[
            "Excessive span causes overstress and failure",
            "Industry tables provide proven guidance"
        ],
        resolution_strategy="Determine span from tables; adjust for field conditions.",
        entity_scope="All supported piping systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="MSS SP-69"
    ),
    DoctrineBlock(
        topic="Hydrostatic Testing of Piping Systems",
        keywords=["hydrostatic test", "pressure test", "ASME B31.3", "leak test", "commissioning"],
        conclusion_template="Hydrostatic testing is performed at 1.5 times design pressure to verify integrity and leak-tightness of piping systems.",
        reasoning_framework="""
        ASME B31.3 Section 345 requires hydrostatic testing of new piping at not less than 1.5 times the design pressure, held for a specified duration. Test fluid is typically water with corrosion inhibitor. Pneumatic testing may be used only when hydrotest is impractical, with additional safety precautions. All joints and welds are inspected for leaks. Documentation of test conditions and results is required for turnover.
        """,
        key_factors=[
            "Design pressure and test factor",
            "Test medium and safety",
            "Duration and inspection",
            "Documentation",
            "Exceptions for pneumatic testing"
        ],
        primary_authority=["ASME B31.3 Section 345"],
        burden_holder="Commissioning engineer",
        adversary_position="Reducing test pressure or duration",
        counter_arguments=[
            "Code mandates minimum test pressure and duration",
            "Insufficient testing risks undetected leaks"
        ],
        resolution_strategy="Perform hydrotest per code; document all results.",
        entity_scope="All new and modified piping systems",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 345"
    ),
    DoctrineBlock(
        topic="Pneumatic Testing of Piping Systems",
        keywords=["pneumatic test", "pressure test", "ASME B31.3", "air test", "safety"],
        conclusion_template="Pneumatic testing is allowed only when hydrostatic testing is impractical, with test pressure limited to 1.1 times design pressure and enhanced safety measures.",
        reasoning_framework="""
        ASME B31.3 Section 345.5 permits pneumatic testing when hydrotesting is not feasible (e.g., water-sensitive systems). Test pressure is limited to 1.1 times design pressure due to stored energy risk. All personnel must be evacuated from the test area, and leak detection is performed with soap solution or other methods. Documentation and justification for pneumatic testing are required.
        """,
        key_factors=[
            "Justification for pneumatic test",
            "Test pressure and safety precautions",
            "Leak detection method",
            "Documentation",
            "Code compliance"
        ],
        primary_authority=["ASME B31.3 Section 345.5"],
        burden_holder="Commissioning engineer",
        adversary_position="Using pneumatic test for convenience",
        counter_arguments=[
            "Pneumatic testing is higher risk and restricted by code",
            "Hydrotest is preferred for safety"
        ],
        resolution_strategy="Use pneumatic test only with justification and enhanced safety measures.",
        entity_scope="Piping systems where hydrotest is impractical",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 345.5"
    ),
    DoctrineBlock(
        topic="Positive Material Identification (PMI) in Piping Systems",
        keywords=["PMI", "positive material identification", "material verification", "ASME B31.3", "quality control"],
        conclusion_template="PMI is required for alloy piping systems to verify material composition and prevent material mix-up.",
        reasoning_framework="""
        Positive Material Identification (PMI) uses portable analyzers to verify alloy composition (e.g., stainless, duplex, alloy steel) before installation. ASME B31.3 and client specifications require PMI for critical services (e.g., sour, high temperature) to prevent material mix-up. PMI is performed at receipt, fabrication, and installation stages. Records are maintained for traceability. Carbon steel may be exempt unless specified.
        """,
        key_factors=[
            "Alloy type and criticality",
            "Client and code requirements",
            "PMI method and frequency",
            "Documentation and traceability",
            "Risk of material mix-up"
        ],
        primary_authority=["ASME B31.3", "API 578"],
        burden_holder="Quality control inspector",
        adversary_position="Skipping PMI to reduce cost",
        counter_arguments=[
            "Material mix-up can cause catastrophic failure",
            "PMI is industry standard for critical alloys"
        ],
        resolution_strategy="Perform PMI per code and client requirements; maintain records.",
        entity_scope="Alloy piping systems in critical service",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 578"
    ),
    DoctrineBlock(
        topic="Hot Tapping of Live Pipelines",
        keywords=["hot tap", "live pipeline", "modification", "safety", "API RP 2201"],
        conclusion_template="Hot tapping is performed on live pipelines using qualified procedures and equipment, with risk assessment and safety controls per API RP 2201.",
        reasoning_framework="""
        Hot tapping allows connection to a pressurized pipeline without shutdown. API RP 2201 provides procedures for risk assessment, equipment selection, and execution. Key risks include leak, fire, and explosion. Only qualified personnel and approved equipment are used. Isolation, pressure control, and continuous monitoring are mandatory. Documentation and permits are required. Not all pipelines are suitable for hot tapping (e.g., high H2S, unstable fluids).
        """,
        key_factors=[
            "Pipeline pressure and fluid type",
            "Risk assessment and safety controls",
            "Qualified personnel and equipment",
            "Permit and documentation",
            "Suitability of pipeline for hot tap"
        ],
        primary_authority=["API RP 2201", "ASME B31.3 Section 341"],
        burden_holder="Pipeline operations engineer",
        adversary_position="Performing hot tap without full controls",
        counter_arguments=[
            "Improper hot tap can cause catastrophic failure",
            "API RP 2201 is industry standard"
        ],
        resolution_strategy="Follow API RP 2201 procedures; obtain all permits and approvals.",
        entity_scope="Live pipeline modifications",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 2201"
    ),
    DoctrineBlock(
        topic="Fire Protection for Process Piping",
        keywords=["fire protection", "process piping", "fireproofing", "NFPA", "API 2218"],
        conclusion_template="Fire protection measures for process piping include fireproofing, isolation, and emergency depressurization per NFPA and API 2218.",
        reasoning_framework="""
        Process piping in fire-prone areas may require fireproofing (e.g., intumescent coatings), isolation valves, and emergency depressurization systems. NFPA codes and API 2218 provide guidance on fire protection design. Fire risk assessment determines required measures. Fireproofing is applied to critical supports and valves. Emergency isolation and blowdown systems are designed for rapid response. Documentation and periodic inspection are required.
        """,
        key_factors=[
            "Fire risk assessment",
            "Location and criticality of piping",
            "Fireproofing materials and application",
            "Isolation and depressurization systems",
            "Inspection and maintenance"
        ],
        primary_authority=["NFPA 30", "API 2218"],
        burden_holder="Process safety engineer",
        adversary_position="Omitting fire protection to reduce cost",
        counter_arguments=[
            "Fire can cause catastrophic piping failure",
            "NFPA and API codes require protection"
        ],
        resolution_strategy="Implement fire protection per risk assessment and codes.",
        entity_scope="Process piping in fire-prone areas",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 2218"
    ),
    DoctrineBlock(
        topic="Design for Slug Flow in Pipelines",
        keywords=["slug flow", "pipeline", "two-phase", "flow assurance", "API RP 14E"],
        conclusion_template="Pipelines subject to slug flow are designed with provisions for surge, separation, and flow assurance per API RP 14E.",
        reasoning_framework="""
        Slug flow causes large, intermittent surges of liquid in gas pipelines, leading to pressure transients and potential equipment damage. API RP 14E recommends design measures such as surge vessels, separators, and control of pipeline inclination. Flow assurance analysis predicts slug frequency and magnitude. Instrumentation and control systems are used to manage slugs. Documentation of analysis and mitigation is required.
        """,
        key_factors=[
            "Two-phase flow regime",
            "Pipeline inclination and layout",
            "Surge and separation equipment",
            "Flow assurance analysis",
            "Instrumentation and control"
        ],
        primary_authority=["API RP 14E", "PIP PNE00003"],
        burden_holder="Pipeline design engineer",
        adversary_position="Ignoring slug flow effects",
        counter_arguments=[
            "Slug flow can cause equipment failure",
            "API RP 14E requires consideration of flow regime"
        ],
        resolution_strategy="Analyze for slug flow and implement mitigation measures.",
        entity_scope="Two-phase pipelines",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 14E"
    ),
    DoctrineBlock(
        topic="Pipe Insulation Selection and Thickness",
        keywords=["pipe insulation", "thermal insulation", "thickness", "energy conservation", "CINI"],
        conclusion_template="Pipe insulation type and thickness are selected based on heat loss/gain requirements, process temperature, and safety, per CINI or equivalent standards.",
        reasoning_framework="""
        Insulation minimizes heat loss/gain, prevents freezing, and protects personnel. Selection considers process temperature, ambient conditions, and energy conservation. CINI and ASTM standards provide guidance on insulation materials (e.g., mineral wool, calcium silicate) and required thickness for given temperature differentials. Fire and moisture resistance are also considered. Insulation is installed with vapor barriers and jacketing as required.
        """,
        key_factors=[
            "Process and ambient temperature",
            "Required heat loss/gain limit",
            "Material selection",
            "Personnel protection",
            "Fire and moisture resistance"
        ],
        primary_authority=["CINI Manual", "ASTM C680"],
        burden_holder="Piping designer",
        adversary_position="Reducing insulation to save cost",
        counter_arguments=[
            "Insufficient insulation increases energy loss and safety risk",
            "CINI and ASTM provide proven guidance"
        ],
        resolution_strategy="Select insulation per CINI/ASTM and process requirements.",
        entity_scope="Insulated piping systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="CINI Manual"
    ),
    DoctrineBlock(
        topic="Underground Piping Design and Burial Depth",
        keywords=["underground piping", "burial depth", "external loads", "ASME B31.3", "API 1102"],
        conclusion_template="Underground piping is designed for minimum burial depth and protection against external loads per ASME B31.3 and API 1102.",
        reasoning_framework="""
        Burial depth protects piping from mechanical damage, frost, and external loads (traffic, soil movement). ASME B31.3 and API 1102 specify minimum cover (typically 0.9-1.2 m) and requirements for bedding, backfill, and warning tape. Deeper burial may be required for road crossings or high-traffic areas. Pipe material and coating are selected for soil conditions. Cathodic protection is provided for steel pipe.
        """,
        key_factors=[
            "Minimum cover requirement",
            "External load assessment",
            "Soil conditions and frost depth",
            "Bedding and backfill quality",
            "Warning and identification"
        ],
        primary_authority=["ASME B31.3 Section 313", "API 1102"],
        burden_holder="Civil/pipeline engineer",
        adversary_position="Reducing burial depth to save cost",
        counter_arguments=[
            "Insufficient cover increases risk of damage",
            "Codes specify minimum requirements"
        ],
        resolution_strategy="Design burial depth per code and site assessment.",
        entity_scope="All underground piping",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 1102"
    ),
    DoctrineBlock(
        topic="Design for Sour Service (H2S) in Piping Systems",
        keywords=["sour service", "H2S", "NACE MR0175", "material selection", "sulfide stress cracking"],
        conclusion_template="Piping in sour service is designed and constructed per NACE MR0175, with qualified materials and welding procedures to prevent sulfide stress cracking.",
        reasoning_framework="""
        Hydrogen sulfide (H2S) in process fluids causes sulfide stress cracking in susceptible materials. NACE MR0175/ISO 15156 specifies material selection, hardness limits, and welding procedures for sour service. Carbon steels must meet maximum hardness and be free of cold work. Austenitic and duplex stainless steels are selected for resistance. All materials and welds are certified for compliance. Inspection and documentation are required.
        """,
        key_factors=[
            "H2S concentration and partial pressure",
            "Material hardness and composition",
            "Welding procedure qualification",
            "Certification and traceability",
            "Inspection and documentation"
        ],
        primary_authority=["NACE MR0175/ISO 15156", "ASME B31.3 Section 323.2.3"],
        burden_holder="Materials/welding engineer",
        adversary_position="Using non-qualified materials or procedures",
        counter_arguments=[
            "Non-compliance risks catastrophic failure",
            "NACE MR0175 is mandatory for sour service"
        ],
        resolution_strategy="Specify and verify materials/welds per NACE MR0175.",
        entity_scope="All piping in sour service",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NACE MR0175/ISO 15156"
    ),
    DoctrineBlock(
        topic="Pipe Flange Bolt Torqueing and Tightening Procedures",
        keywords=["flange bolt", "torque", "tightening", "leak prevention", "ASME PCC-1"],
        conclusion_template="Flange bolts are tightened using controlled torque and approved procedures per ASME PCC-1 to ensure leak-tight joints.",
        reasoning_framework="""
        Improper bolt tightening is a major cause of flange leaks. ASME PCC-1 provides procedures for bolt torqueing, including sequence, lubrication, and use of calibrated tools. Torque values are determined from bolt size, material, and gasket type. Controlled tightening (star pattern, multiple passes) ensures even gasket compression. Documentation of torque values and personnel training is required.
        """,
        key_factors=[
            "Bolt size and material",
            "Gasket type and compression",
            "Torque value calculation",
            "Tightening sequence and method",
            "Personnel training"
        ],
        primary_authority=["ASME PCC-1"],
        burden_holder="Mechanical technician",
        adversary_position="Hand tightening or skipping torque procedure",
        counter_arguments=[
            "Improper tightening causes leaks and failures",
            "ASME PCC-1 is industry standard"
        ],
        resolution_strategy="Follow ASME PCC-1 torqueing procedures; document results.",
        entity_scope="All flanged joints",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME PCC-1"
    ),
    DoctrineBlock(
        topic="Valve Selection and Sizing for Piping Systems",
        keywords=["valve selection", "valve sizing", "control valve", "API 6D", "ASME B16.34"],
        conclusion_template="Valves are selected and sized based on service conditions, flow requirements, and code standards (API 6D, ASME B16.34).",
        reasoning_framework="""
        Valve selection considers fluid type, pressure, temperature, required function (isolation, control), and compatibility with piping. Sizing is based on flow rate, pressure drop, and valve characteristics (Cv). API 6D covers pipeline valves; ASME B16.34 covers valves for general service. Valve material, end connections, and actuation are selected for process and safety requirements. Certification and testing are required.
        """,
        key_factors=[
            "Service pressure and temperature",
            "Fluid type and properties",
            "Required function (on/off, control)",
            "Valve material and rating",
            "Sizing for flow and pressure drop"
        ],
        primary_authority=["API 6D", "ASME B16.34"],
        burden_holder="Piping designer",
        adversary_position="Selecting undersized or non-compliant valves",
        counter_arguments=[
            "Improper valve selection risks failure and non-compliance",
            "API and ASME codes provide sizing and selection criteria"
        ],
        resolution_strategy="Select and size valves per API/ASME and process requirements.",
        entity_scope="All process and pipeline valves",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="API 6D"
    ),
    DoctrineBlock(
        topic="Pipe Painting and Coating for Corrosion Protection",
        keywords=["pipe painting", "coating", "corrosion protection", "surface preparation", "NACE"],
        conclusion_template="Pipe painting and coating are applied per NACE and project standards to protect against external corrosion and provide identification.",
        reasoning_framework="""
        External coatings protect steel pipe from atmospheric and buried corrosion. NACE and SSPC standards specify surface preparation (e.g., blast cleaning), coating type (epoxy, polyurethane), and application method. Coating selection considers environment, temperature, and mechanical damage risk. Color coding is used for identification per client or ISO standards. Inspection and holiday testing verify coating integrity.
        """,
        key_factors=[
            "Environmental exposure",
            "Surface preparation quality",
            "Coating material and thickness",
            "Color coding and identification",
            "Inspection and testing"
        ],
        primary_authority=["NACE SP0108", "SSPC PA 2"],
        burden_holder="Coating inspector",
        adversary_position="Skipping surface prep or using inferior coating",
        counter_arguments=[
            "Poor coating increases corrosion risk",
            "NACE/SSPC standards ensure long-term protection"
        ],
        resolution_strategy="Apply coating per NACE/SSPC and inspect for compliance.",
        entity_scope="All coated piping systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NACE SP0108"
    ),
    DoctrineBlock(
        topic="Thermal Expansion Allowance for Aboveground Piping",
        keywords=["thermal expansion", "aboveground piping", "expansion joint", "flexibility", "ASME B31.3"],
        conclusion_template="Thermal expansion is accommodated by piping flexibility, expansion joints, or loops as required by ASME B31.3 Section 319.",
        reasoning_framework="""
        Aboveground piping expands and contracts with temperature changes. ASME B31.3 Section 319 requires analysis of thermal movement and provision of adequate flexibility. Expansion joints or loops are used where space is limited. Anchors, guides, and sliding supports control movement. Expansion analysis is documented, and expansion devices are maintained per manufacturer instructions.
        """,
        key_factors=[
            "Temperature differential",
            "Pipe length and layout",
            "Support and anchor locations",
            "Expansion device selection",
            "Analysis and documentation"
        ],
        primary_authority=["ASME B31.3 Section 319"],
        burden_holder="Pipe stress analyst",
        adversary_position="Omitting expansion provisions",
        counter_arguments=[
            "Lack of flexibility causes overstress and failure",
            "Code requires expansion analysis"
        ],
        resolution_strategy="Analyze and provide expansion allowance per code.",
        entity_scope="All aboveground piping subject to temperature change",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 319"
    ),
    DoctrineBlock(
        topic="Pipe Wall Thickness for External Pressure",
        keywords=["external pressure", "pipe wall thickness", "vacuum service", "ASME VIII", "buckling"],
        conclusion_template="Pipe wall thickness for external pressure (vacuum service) is determined per ASME Section VIII, Division 1, to prevent buckling.",
        reasoning_framework="""
        Piping subject to external pressure (e.g., vacuum, buried, jacketed) must be checked for buckling. ASME Section VIII, Division 1, provides formulas and charts for minimum wall thickness based on diameter, length, and material. Calculations consider external pressure, pipe ovality, and support spacing. Documentation of analysis is required.
        """,
        key_factors=[
            "External pressure magnitude",
            "Pipe diameter and length",
            "Material properties",
            "Support and stiffening",
            "Code calculations"
        ],
        primary_authority=["ASME Section VIII, Division 1", "ASME B31.3 Section 304.1.3"],
        burden_holder="Piping design engineer",
        adversary_position="Neglecting external pressure in design",
        counter_arguments=[
            "Buckling can cause catastrophic failure",
            "Code requires external pressure check"
        ],
        resolution_strategy="Perform external pressure check per ASME VIII and document results.",
        entity_scope="Piping subject to vacuum or external pressure",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII, Division 1"
    ),
    DoctrineBlock(
        topic="Pipe Flange Face Finish Requirements",
        keywords=["flange face", "surface finish", "ASME B16.5", "gasket sealing", "leak prevention"],
        conclusion_template="Flange face finish is specified per ASME B16.5 to ensure proper gasket sealing and leak prevention.",
        reasoning_framework="""
        Flange face finish (surface roughness) affects gasket compression and sealing. ASME B16.5 specifies finish requirements (e.g., 125-250 AARH for RF flanges). Improper finish can cause leakage or gasket damage. Inspection of flange faces is performed before assembly. Damaged or out-of-tolerance faces are repaired or replaced.
        """,
        key_factors=[
            "Flange type and facing",
            "Surface roughness (AARH)",
            "Gasket type",
            "Inspection and repair",
            "Code compliance"
        ],
        primary_authority=["ASME B16.5"],
        burden_holder="Quality control inspector",
        adversary_position="Ignoring or relaxing finish requirements",
        counter_arguments=[
            "Improper finish increases leak risk",
            "ASME B16.5 is mandatory"
        ],
        resolution_strategy="Specify and inspect flange finish per ASME B16.5.",
        entity_scope="All flanged joints",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B16.5"
    ),
    DoctrineBlock(
        topic="Pipe Branch Reinforcement Requirements",
        keywords=["branch reinforcement", "pipe branch", "ASME B31.3", "pad", "weldolet"],
        conclusion_template="Branch connections are reinforced as required by ASME B31.3 Section 304.3 to ensure adequate strength.",
        reasoning_framework="""
        Branches (e.g., tees, weldolets) introduce local stress concentrations. ASME B31.3 Section 304.3 requires reinforcement when the branch size or configuration exceeds code limits. Reinforcement is provided by integrally reinforced fittings, pads, or increased wall thickness. Calculations determine required area of reinforcement. Inspection and documentation are required.
        """,
        key_factors=[
            "Branch size and configuration",
            "Header and branch wall thickness",
            "Reinforcement area calculation",
            "Fitting type (integral, pad, weldolet)",
            "Inspection and documentation"
        ],
        primary_authority=["ASME B31.3 Section 304.3"],
        burden_holder="Piping designer",
        adversary_position="Omitting reinforcement for cost savings",
        counter_arguments=[
            "Unreinforced branches risk failure",
            "Code requires reinforcement when limits are exceeded"
        ],
        resolution_strategy="Calculate and provide reinforcement per ASME B31.3.",
        entity_scope="All branch connections",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 304.3"
    ),
    DoctrineBlock(
        topic="Pipe Flange Gasket Stress Requirements",
        keywords=["gasket stress", "flange", "ASME VIII", "leak prevention", "bolt load"],
        conclusion_template="Gasket stress is calculated to ensure sufficient bolt load for sealing without damaging gasket or flange, per ASME Section VIII.",
        reasoning_framework="""
        Proper gasket stress is essential for leak-tight flanged joints. ASME Section VIII provides formulas for minimum and maximum gasket seating stress based on gasket type and material. Bolt torque is calculated to achieve required stress. Over-tightening can crush gasket or flange; under-tightening leads to leaks. Documentation of calculations and torque values is required.
        """,
        key_factors=[
            "Gasket type and material",
            "Flange size and rating",
            "Bolt size and material",
            "Required seating stress",
            "Torque calculation"
        ],
        primary_authority=["ASME Section VIII", "ASME PCC-1"],
        burden_holder="Mechanical engineer",
        adversary_position="Neglecting gasket stress calculation",
        counter_arguments=[
            "Improper stress causes leaks or damage",
            "ASME codes require calculation"
        ],
        resolution_strategy="Calculate gasket stress and specify bolt torque per code.",
        entity_scope="All flanged joints",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII"
    ),
    DoctrineBlock(
        topic="Pipe Support Corrosion Protection",
        keywords=["pipe support", "corrosion protection", "galvanizing", "coating", "maintenance"],
        conclusion_template="Pipe supports are protected from corrosion by galvanizing, painting, or coating per project and industry standards.",
        reasoning_framework="""
        Pipe supports are exposed to weather, chemicals, and condensation, leading to corrosion. Protection is provided by hot-dip galvanizing, painting, or application of protective coatings. Selection depends on environment and client standards. Regular inspection and maintenance are required. Stainless steel supports may be used in highly corrosive areas.
        """,
        key_factors=[
            "Support material and environment",
            "Protection method (galvanizing, coating)",
            "Inspection and maintenance",
            "Client and industry standards",
            "Replacement intervals"
        ],
        primary_authority=["ASTM A123", "NACE SP0108"],
        burden_holder="Maintenance engineer",
        adversary_position="Omitting protection to reduce cost",
        counter_arguments=[
            "Corroded supports compromise pipe integrity",
            "Industry standards require protection"
        ],
        resolution_strategy="Specify and maintain corrosion protection for all supports.",
        entity_scope="All pipe supports",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ASTM A123"
    ),
    DoctrineBlock(
        topic="Pipe Vibration Analysis and Mitigation",
        keywords=["pipe vibration", "analysis", "mitigation", "dynamic loads", "API 618"],
        conclusion_template="Pipe vibration is analyzed and mitigated using supports, dampers, and layout changes per API 618 and industry practice.",
        reasoning_framework="""
        Vibration can be caused by flow-induced forces, rotating equipment, or external loads. API 618 and industry guidelines recommend analysis of vibration sources, frequency, and amplitude. Mitigation includes adding supports, dampers, or changing pipe layout. Excessive vibration leads to fatigue and failure. Monitoring and periodic inspection are required.
        """,
        key_factors=[
            "Vibration source and frequency",
            "Pipe span and support",
            "Mitigation methods",
            "Monitoring and inspection",
            "Industry guidelines"
        ],
        primary_authority=["API 618", "ASME B31.3"],
        burden_holder="Mechanical engineer",
        adversary_position="Ignoring vibration analysis",
        counter_arguments=[
            "Vibration causes fatigue and failure",
            "Industry guidelines require analysis"
        ],
        resolution_strategy="Analyze and mitigate vibration per API 618.",
        entity_scope="All piping subject to dynamic loads",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618"
    ),
    DoctrineBlock(
        topic="Pipe Wall Thickness for Erosion Allowance",
        keywords=["erosion allowance", "pipe wall thickness", "abrasive service", "API RP 14E"],
        conclusion_template="Erosion allowance is added to pipe wall thickness for abrasive or high-velocity service per API RP 14E.",
        reasoning_framework="""
        Abrasive fluids or high-velocity flow cause erosion of pipe wall. API RP 14E recommends adding erosion allowance based on fluid properties, velocity, and historical data. Typical values range from 1.5 to 3 mm for severe service. Inspection and monitoring are required to track wall loss. Material selection and velocity limits also mitigate erosion.
        """,
        key_factors=[
            "Fluid abrasiveness and velocity",
            "Service life and inspection frequency",
            "Material selection",
            "Historical erosion data",
            "Industry guidelines"
        ],
        primary_authority=["API RP 14E"],
        burden_holder="Piping design engineer",
        adversary_position="Omitting allowance to reduce cost",
        counter_arguments=[
            "Erosion can cause premature failure",
            "API RP 14E provides guidance"
        ],
        resolution_strategy="Add erosion allowance per API RP 14E and monitor wall thickness.",
        entity_scope="Abrasive or high-velocity piping",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API RP 14E"
    ),
    DoctrineBlock(
        topic="Pipe System Documentation and Turnover Requirements",
        keywords=["documentation", "turnover", "as-built", "inspection records", "QA/QC"],
        conclusion_template="Complete documentation (as-built drawings, inspection records, test certificates) is required for piping system turnover per project QA/QC requirements.",
        reasoning_framework="""
        Turnover documentation includes as-built drawings, material certificates, welding and inspection records, test reports, and operating manuals. QA/QC procedures require review and approval of all documents before system handover. Incomplete documentation delays commissioning and may violate regulatory requirements. Electronic document management systems are used for traceability.
        """,
        key_factors=[
            "As-built drawings and records",
            "Material and test certificates",
            "Inspection and QA/QC documentation",
            "Regulatory and client requirements",
            "Traceability"
        ],
        primary_authority=["Project QA/QC Plan", "ASME B31.3 Section 341"],
        burden_holder="QA/QC coordinator",
        adversary_position="Incomplete or missing documentation",
        counter_arguments=[
            "Incomplete records delay commissioning",
            "QA/QC and regulatory requirements are mandatory"
        ],
        resolution_strategy="Compile and review all documentation before turnover.",
        entity_scope="All piping system projects",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Project QA/QC Plan"
    ),
    DoctrineBlock(
        topic="Pipe System Leak Testing for Commissioning",
        keywords=["leak test", "commissioning", "ASME B31.3", "pressure test", "integrity"],
        conclusion_template="Leak testing is performed after installation to verify system integrity, using hydrostatic or pneumatic methods per ASME B31.3.",
        reasoning_framework="""
        Leak testing is required after installation and before commissioning. ASME B31.3 Section 345 specifies test pressure, method (hydrostatic or pneumatic), and duration. All joints and connections are inspected for leaks. Test results are documented. Exceptions and waivers require engineering justification and approval.
        """,
        key_factors=[
            "Test pressure and method",
            "Inspection of joints and connections",
            "Documentation of results",
            "Exceptions and waivers",
            "Code compliance"
        ],
        primary_authority=["ASME B31.3 Section 345"],
        burden_holder="Commissioning engineer",
        adversary_position="Skipping or reducing scope of leak test",
        counter_arguments=[
            "Leak testing is mandatory for safety",
            "Code specifies minimum requirements"
        ],
        resolution_strategy="Perform and document leak test per code.",
        entity_scope="All new and modified piping systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ASME B31.3 Section 345"
    ),
    DoctrineBlock(
        topic="Pipe System Flushing and Cleaning Prior to Service",
        keywords=["flushing", "cleaning", "debris removal", "commissioning", "ASME B31.3"],
        conclusion_template="Piping systems are flushed and cleaned prior to service to remove debris, scale, and contaminants per project and code requirements.",
        reasoning_framework="""
        Flushing and cleaning remove construction debris, scale, and contaminants that could damage equipment or affect process quality. Methods include water flushing, air blowing, chemical cleaning, or pigging. Acceptance criteria are defined in project specifications. Inspection and documentation of cleaning are required before commissioning.
        """,
        key_factors=[
            "Cleaning method and acceptance criteria",
            "Inspection and verification",
            "Project and code requirements",
            "Documentation",
            "Impact on downstream equipment"
        ],
        primary_authority=["ASME B31.3", "Project