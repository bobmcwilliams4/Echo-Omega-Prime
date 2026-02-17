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
        topic="Amine Gas Sweetening Selection: MDEA vs DEA vs MEA",
        keywords=["amine", "gas sweetening", "MDEA", "DEA", "MEA", "acid gas removal", "CO2", "H2S"],
        conclusion_template="Select MDEA for selective H2S removal and low energy consumption; DEA for moderate CO2/H2S removal; MEA for high CO2/H2S removal but with higher energy and corrosion risk.",
        reasoning_framework="""
        1. Evaluate inlet gas composition (CO2, H2S, hydrocarbons, BTEX).
        2. Assess required outlet specifications for CO2 and H2S.
        3. Consider solvent characteristics:
            - MDEA: High selectivity for H2S, lower energy, less corrosion.
            - DEA: Moderate selectivity, higher energy than MDEA, less stable than MDEA.
            - MEA: High reactivity, high energy, significant corrosion risk.
        4. Analyze process constraints (regeneration energy, corrosion, solvent losses).
        5. Review operational experience and solvent cost.
        6. Factor in environmental and safety regulations.
        7. Select solvent balancing selectivity, energy, cost, and operational risk.
        """,
        key_factors=[
            "Inlet gas composition",
            "Required outlet specifications",
            "Solvent selectivity and reactivity",
            "Regeneration energy requirements",
            "Corrosion potential",
            "Solvent degradation and losses",
            "Operational experience",
            "Environmental regulations"
        ],
        primary_authority=[
            "GPSA Engineering Data Book",
            "API RP 942",
            "UOP Amine Treating Guidelines",
            "Shell DEP 31.40.10.13"
        ],
        burden_holder="Process Design Engineer",
        adversary_position="MEA is always preferred due to high reactivity.",
        counter_arguments=[
            "MEA has higher energy consumption and corrosion risk.",
            "MDEA provides selective H2S removal with lower energy.",
            "DEA is less stable and less selective than MDEA."
        ],
        resolution_strategy="Perform comparative simulation and cost analysis; select solvent based on process requirements and risk assessment.",
        entity_scope="Natural Gas Processing Facilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 19"
    ),
    DoctrineBlock(
        topic="Triethylene Glycol (TEG) Dehydration System Design",
        keywords=["TEG", "dehydration", "water removal", "glycol", "dew point", "regeneration"],
        conclusion_template="Design TEG dehydration units to achieve pipeline water dew point specification, typically -40°C, with proper contactor and regenerator sizing.",
        reasoning_framework="""
        1. Determine required water dew point for pipeline or process.
        2. Calculate water content in feed gas at operating pressure and temperature.
        3. Size contactor to ensure sufficient gas-liquid contact (typically 6-8 trays or equivalent packing).
        4. Select TEG circulation rate to achieve target dew point.
        5. Design regenerator to minimize TEG losses and thermal degradation.
        6. Incorporate stripping gas or vacuum regeneration for very low dew points.
        7. Address foaming, carryover, and corrosion risks.
        8. Ensure compliance with environmental discharge limits for TEG and water.
        """,
        key_factors=[
            "Required water dew point",
            "Feed gas water content",
            "Contactor design (trays/packing)",
            "TEG circulation rate",
            "Regeneration method",
            "Foaming and carryover control",
            "Corrosion management"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 20",
            "API 12J",
            "UOP Glycol Dehydration Guidelines"
        ],
        burden_holder="Process Engineer",
        adversary_position="TEG dehydration is unnecessary if gas is compressed.",
        counter_arguments=[
            "Compression alone does not remove water vapor.",
            "Pipeline specifications require low water content.",
            "TEG dehydration is proven and cost-effective."
        ],
        resolution_strategy="Demonstrate water content at pipeline pressure without dehydration exceeds specification; justify TEG system.",
        entity_scope="Natural Gas Processing Plants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 12J"
    ),
    DoctrineBlock(
        topic="NGL Recovery: Turboexpander vs Refrigeration Process Selection",
        keywords=["NGL", "recovery", "turboexpander", "refrigeration", "cryogenic", "LPG", "ethane", "propane"],
        conclusion_template="Select turboexpander for high ethane recovery (>85%) and large capacities; refrigeration for moderate recovery and smaller plants.",
        reasoning_framework="""
        1. Define NGL recovery targets (ethane, propane, butane).
        2. Assess feed gas composition and flow rate.
        3. Evaluate process economics and energy integration.
        4. Turboexpander:
            - High ethane recovery (>85%),
            - Suitable for large capacities,
            - Higher capital cost, lower operating cost.
        5. Refrigeration:
            - Moderate recovery (50-75%),
            - Simpler, lower capital cost,
            - Higher operating cost per unit NGL.
        6. Consider product specifications and downstream requirements.
        7. Review site utilities and integration opportunities.
        """,
        key_factors=[
            "NGL recovery targets",
            "Feed gas composition",
            "Plant capacity",
            "Capital and operating costs",
            "Product specifications",
            "Utility availability"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 21",
            "API 617",
            "UOP NGL Recovery Guidelines"
        ],
        burden_holder="Process Design Engineer",
        adversary_position="Refrigeration is always more economical for NGL recovery.",
        counter_arguments=[
            "Turboexpander is more efficient for high recovery and large plants.",
            "Refrigeration is limited in ethane recovery.",
            "Process selection depends on specific project economics."
        ],
        resolution_strategy="Perform process simulation and economic analysis for both options; select based on recovery targets and lifecycle cost.",
        entity_scope="NGL Recovery Units",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 21"
    ),
    DoctrineBlock(
        topic="Demethanizer Column Design and Operation",
        keywords=["demethanizer", "column", "NGL", "cryogenic", "fractionation", "methane removal", "reboiler"],
        conclusion_template="Design demethanizer columns for efficient methane removal from NGL, with proper tray or packing selection, reflux ratio, and reboiler duty.",
        reasoning_framework="""
        1. Define feed composition and required methane content in NGL product.
        2. Select column internals (trays or structured packing) for optimal separation.
        3. Determine number of theoretical stages via simulation (typically 20-40).
        4. Set reflux ratio to balance recovery and energy consumption.
        5. Size reboiler and condenser for required duties.
        6. Address control strategies for pressure, temperature, and composition.
        7. Consider start-up, shutdown, and upset conditions.
        8. Ensure compliance with safety and environmental standards.
        """,
        key_factors=[
            "Feed composition",
            "Methane content specification",
            "Column internals",
            "Number of stages",
            "Reflux ratio",
            "Reboiler and condenser sizing",
            "Control strategies"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 22",
            "API 521",
            "UOP Cryogenic Fractionation Guidelines"
        ],
        burden_holder="Process Engineer",
        adversary_position="Demethanizer design can be standardized for all feed compositions.",
        counter_arguments=[
            "Feed composition significantly impacts column design.",
            "Number of stages and reflux must be tailored to each case.",
            "Standardization may lead to off-spec product."
        ],
        resolution_strategy="Perform case-specific simulation and design; validate with pilot data if available.",
        entity_scope="NGL Fractionation Plants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 22"
    ),
    DoctrineBlock(
        topic="Pipeline Quality Specifications: H2S, CO2, Water Dewpoint, BTU",
        keywords=["pipeline", "quality", "specifications", "H2S", "CO2", "water dewpoint", "BTU", "sales gas"],
        conclusion_template="Ensure processed gas meets pipeline specifications: H2S < 4 ppmv, CO2 < 2%, water dewpoint < -40°C, BTU within contractual range.",
        reasoning_framework="""
        1. Obtain pipeline or sales contract specifications for H2S, CO2, water, and heating value.
        2. Design processing steps to achieve each specification:
            - Amine sweetening for H2S/CO2,
            - Glycol or molecular sieve dehydration for water,
            - NGL recovery for BTU adjustment.
        3. Monitor and control product gas quality continuously.
        4. Implement alarms and shutdowns for off-spec conditions.
        5. Maintain documentation and compliance records.
        6. Review and update specifications as contracts or regulations change.
        """,
        key_factors=[
            "Pipeline contract specifications",
            "Gas composition",
            "Process performance",
            "Monitoring and control systems",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FERC 18 CFR Part 284",
            "API 14E",
            "GPSA Engineering Data Book, Section 24"
        ],
        burden_holder="Plant Operator",
        adversary_position="Minor deviations from specifications are acceptable.",
        counter_arguments=[
            "Pipeline operators may reject off-spec gas.",
            "Contract penalties may apply.",
            "Safety and environmental risks increase with off-spec gas."
        ],
        resolution_strategy="Implement strict QA/QC and real-time monitoring; shut-in or divert off-spec gas.",
        entity_scope="Sales Gas Pipelines",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="FERC 18 CFR Part 284"
    ),
    DoctrineBlock(
        topic="Reciprocating vs Centrifugal Compressor Selection for Gas Processing",
        keywords=["compressor", "reciprocating", "centrifugal", "gas processing", "compression", "selection"],
        conclusion_template="Select reciprocating compressors for high-pressure, low-flow, variable duty; centrifugal for high-flow, steady-state applications.",
        reasoning_framework="""
        1. Define required discharge pressure and flow rate.
        2. Reciprocating compressors:
            - High pressure, low to moderate flow,
            - Good for variable duty,
            - Higher maintenance, lower capital cost.
        3. Centrifugal compressors:
            - High flow, moderate pressure,
            - Best for steady-state operation,
            - Lower maintenance, higher capital cost.
        4. Consider gas composition, presence of liquids, and site utilities.
        5. Evaluate lifecycle cost, reliability, and maintenance.
        6. Review noise, vibration, and footprint constraints.
        """,
        key_factors=[
            "Discharge pressure",
            "Flow rate",
            "Duty cycle",
            "Gas composition",
            "Maintenance requirements",
            "Capital and operating cost"
        ],
        primary_authority=[
            "API 618",
            "API 617",
            "GPSA Engineering Data Book, Section 13"
        ],
        burden_holder="Mechanical Engineer",
        adversary_position="Centrifugal compressors are always more reliable.",
        counter_arguments=[
            "Reciprocating compressors are more reliable for variable duty.",
            "Centrifugal compressors can surge at low flow.",
            "Selection depends on application specifics."
        ],
        resolution_strategy="Perform application-specific analysis; select compressor type based on duty and lifecycle cost.",
        entity_scope="Gas Compression Systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 618"
    ),
    DoctrineBlock(
        topic="Claus Sulfur Recovery Process from Acid Gas",
        keywords=["Claus", "sulfur recovery", "acid gas", "H2S", "SO2", "SRU", "tail gas"],
        conclusion_template="Apply Claus process for sulfur recovery from acid gas streams with >25% H2S; ensure >95% recovery with proper tail gas treatment.",
        reasoning_framework="""
        1. Assess acid gas composition and flow rate.
        2. Claus process is suitable for H2S-rich streams (>25% H2S).
        3. Design reaction furnace, waste heat boiler, and catalytic converters.
        4. Achieve >95% sulfur recovery with 2-3 catalytic stages.
        5. Implement tail gas treatment for higher recovery (>99.5%) if required.
        6. Address SO2 emissions and environmental compliance.
        7. Ensure safe handling and storage of elemental sulfur.
        """,
        key_factors=[
            "Acid gas composition",
            "Sulfur recovery target",
            "Process configuration",
            "Tail gas treatment",
            "SO2 emissions control"
        ],
        primary_authority=[
            "API 942",
            "GPSA Engineering Data Book, Section 24",
            "Shell DEP 31.40.10.13"
        ],
        burden_holder="Process Engineer",
        adversary_position="Claus process is inefficient for all acid gas streams.",
        counter_arguments=[
            "Claus process is highly efficient for H2S-rich streams.",
            "Tail gas treatment enhances recovery.",
            "Alternative processes are less proven for large-scale applications."
        ],
        resolution_strategy="Validate process selection with simulation and regulatory requirements; implement tail gas treatment as needed.",
        entity_scope="Sulfur Recovery Units",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API 942"
    ),
    DoctrineBlock(
        topic="Molecular Sieve Dehydration for Very Low Dewpoints",
        keywords=["molecular sieve", "dehydration", "water removal", "dew point", "adsorption", "regeneration"],
        conclusion_template="Use molecular sieve dehydration for gas dew points below -60°C or for cryogenic processing feed.",
        reasoning_framework="""
        1. Determine required water dew point for downstream processes (e.g., cryogenic NGL recovery).
        2. Glycol dehydration is insufficient for dew points below -40°C.
        3. Molecular sieves can achieve dew points below -100°C.
        4. Design adsorption beds with sufficient capacity and cycle time.
        5. Implement proper regeneration with dry gas or inert gas.
        6. Address potential for bed fouling and pressure drop.
        7. Monitor breakthrough and schedule timely regeneration.
        """,
        key_factors=[
            "Target water dew point",
            "Feed gas composition",
            "Adsorbent selection",
            "Regeneration method",
            "Bed sizing and cycle time"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 20",
            "UOP Molecular Sieve Design Manual"
        ],
        burden_holder="Process Engineer",
        adversary_position="Glycol dehydration is sufficient for all applications.",
        counter_arguments=[
            "Glycol systems cannot reach ultra-low dew points.",
            "Cryogenic processes require very dry gas.",
            "Molecular sieves are industry standard for such cases."
        ],
        resolution_strategy="Demonstrate via simulation and dew point analysis; specify molecular sieve for ultra-dry gas.",
        entity_scope="Dehydration Units for Cryogenic Plants",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 20"
    ),
    DoctrineBlock(
        topic="Gas Chromatograph Analysis and BTU Calculation (GPA 2172)",
        keywords=["gas chromatograph", "analysis", "BTU", "GPA 2172", "heating value", "composition"],
        conclusion_template="Use GPA 2172 for gas composition analysis and BTU calculation; calibrate chromatograph regularly.",
        reasoning_framework="""
        1. Collect representative gas samples at process conditions.
        2. Analyze samples with a calibrated gas chromatograph.
        3. Apply GPA 2172 methodology for BTU and component analysis.
        4. Validate results with standard reference gases.
        5. Use results for custody transfer, process control, and reporting.
        6. Maintain calibration and QA/QC records.
        7. Update analysis procedures as standards evolve.
        """,
        key_factors=[
            "Sampling method",
            "Chromatograph calibration",
            "GPA 2172 compliance",
            "Data validation",
            "QA/QC procedures"
        ],
        primary_authority=[
            "GPA 2172",
            "API 14.1",
            "ASTM D1945"
        ],
        burden_holder="Laboratory Technician",
        adversary_position="BTU can be estimated without chromatograph analysis.",
        counter_arguments=[
            "Direct analysis is required for custody transfer.",
            "Estimates are not contractually valid.",
            "Chromatograph ensures accuracy and traceability."
        ],
        resolution_strategy="Enforce chromatograph analysis and GPA 2172 calculations for all custody transfer points.",
        entity_scope="Natural Gas Laboratories and Metering",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="GPA 2172"
    ),
    DoctrineBlock(
        topic="Inlet Separation and Slug Catching Design",
        keywords=["inlet separation", "slug catcher", "liquid removal", "gas processing", "separator", "design"],
        conclusion_template="Design inlet separators and slug catchers to handle maximum liquid slugs and protect downstream equipment.",
        reasoning_framework="""
        1. Analyze expected gas and liquid flow rates, including slugs.
        2. Size separators for normal and upset conditions.
        3. Select slug catcher type (finger, vessel, or hybrid) based on slug volume and site constraints.
        4. Provide adequate liquid handling and drainage systems.
        5. Implement instrumentation for level, pressure, and flow monitoring.
        6. Ensure safe access for maintenance and cleaning.
        7. Comply with ASME and API vessel codes.
        """,
        key_factors=[
            "Slug volume and frequency",
            "Separator sizing",
            "Slug catcher type",
            "Instrumentation and control",
            "Maintenance access",
            "Code compliance"
        ],
        primary_authority=[
            "API 12J",
            "GPSA Engineering Data Book, Section 7",
            "ASME BPVC Section VIII"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Standard separators are sufficient for all inlet conditions.",
        counter_arguments=[
            "Large slugs can overwhelm standard separators.",
            "Slug catchers are designed for high-volume events.",
            "Proper design prevents downstream upsets."
        ],
        resolution_strategy="Conduct flow assurance study; design slug catcher for worst-case scenario.",
        entity_scope="Gas Plant Inlet Facilities",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 12J"
    ),
    DoctrineBlock(
        topic="Amine Solvent Regeneration Optimization",
        keywords=["amine", "regeneration", "optimization", "energy", "steam", "stripper", "reboiler"],
        conclusion_template="Optimize amine regeneration by minimizing reboiler duty while maintaining solvent purity and gas quality.",
        reasoning_framework="""
        1. Monitor lean amine loading and purity.
        2. Adjust reboiler temperature to minimize energy use.
        3. Control steam rate to avoid solvent degradation.
        4. Use heat integration (e.g., lean/rich exchangers) for energy savings.
        5. Monitor acid gas slip and solvent losses.
        6. Implement advanced controls for stable operation.
        7. Review performance regularly and adjust setpoints.
        """,
        key_factors=[
            "Lean amine purity",
            "Reboiler duty",
            "Solvent degradation",
            "Heat integration",
            "Process control"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 19",
            "UOP Amine Treating Guidelines"
        ],
        burden_holder="Process Engineer",
        adversary_position="Higher reboiler duty always improves solvent quality.",
        counter_arguments=[
            "Excessive heat increases solvent degradation.",
            "Optimal duty balances purity and energy use.",
            "Heat integration reduces overall energy consumption."
        ],
        resolution_strategy="Implement performance monitoring and optimization routines.",
        entity_scope="Amine Sweetening Units",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 19"
    ),
    DoctrineBlock(
        topic="BTEX and Heavy Hydrocarbon Management in Amine Systems",
        keywords=["BTEX", "heavy hydrocarbons", "amine", "contamination", "foaming", "solvent losses"],
        conclusion_template="Implement BTEX and heavy hydrocarbon removal upstream of amine systems to prevent foaming and solvent losses.",
        reasoning_framework="""
        1. Analyze feed gas for BTEX and heavy hydrocarbon content.
        2. Install upstream removal systems (e.g., activated carbon, liquid-liquid extraction).
        3. Monitor amine system for foaming and solvent carryover.
        4. Use antifoam agents only as a last resort.
        5. Schedule regular solvent analysis for BTEX content.
        6. Train operators on contamination risks and mitigation.
        """,
        key_factors=[
            "Feed gas BTEX content",
            "Removal system effectiveness",
            "Foaming tendency",
            "Solvent analysis frequency"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 19",
            "API RP 942"
        ],
        burden_holder="Process Engineer",
        adversary_position="BTEX in amine systems is not a significant issue.",
        counter_arguments=[
            "BTEX causes foaming and solvent losses.",
            "Upstream removal is cost-effective.",
            "Antifoam use is not a sustainable solution."
        ],
        resolution_strategy="Install and maintain BTEX removal systems; monitor amine quality.",
        entity_scope="Amine Sweetening Units",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 942"
    ),
    DoctrineBlock(
        topic="TEG System Emissions and Environmental Compliance",
        keywords=["TEG", "emissions", "environmental", "compliance", "BTEX", "vent", "regulations"],
        conclusion_template="Design TEG systems with emission controls for BTEX and glycol vapors to meet environmental regulations.",
        reasoning_framework="""
        1. Quantify expected BTEX and glycol emissions from TEG regenerator vents.
        2. Apply emission control technologies (condensers, incinerators, carbon beds).
        3. Monitor vent streams for compliance with local and federal regulations.
        4. Maintain records of emissions and control system performance.
        5. Implement maintenance and inspection programs for emission controls.
        6. Update controls as regulations evolve.
        """,
        key_factors=[
            "Emission rates",
            "Control technology selection",
            "Regulatory limits",
            "Monitoring and reporting"
        ],
        primary_authority=[
            "US EPA 40 CFR 63 Subpart HH",
            "API 12J",
            "GPSA Engineering Data Book, Section 20"
        ],
        burden_holder="Environmental Engineer",
        adversary_position="TEG emissions are negligible and do not require control.",
        counter_arguments=[
            "BTEX emissions are regulated and can be significant.",
            "Non-compliance leads to fines and shutdowns.",
            "Emission controls are proven and cost-effective."
        ],
        resolution_strategy="Install emission controls and monitor vent streams; report as required.",
        entity_scope="TEG Dehydration Units",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="US EPA 40 CFR 63 Subpart HH"
    ),
    DoctrineBlock(
        topic="TEG System Foaming and Carryover Control",
        keywords=["TEG", "foaming", "carryover", "dehydration", "contamination", "antifoam"],
        conclusion_template="Control TEG system foaming and carryover by removing contaminants and minimizing antifoam use.",
        reasoning_framework="""
        1. Identify sources of foaming (hydrocarbons, solids, surfactants).
        2. Install upstream liquid separation and filtration.
        3. Use antifoam agents sparingly and only as needed.
        4. Monitor TEG quality and replace as required.
        5. Train operators on foaming risks and control methods.
        """,
        key_factors=[
            "Contaminant removal",
            "Antifoam usage",
            "TEG quality monitoring",
            "Operator training"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 20",
            "API 12J"
        ],
        burden_holder="Process Engineer",
        adversary_position="Antifoam is a complete solution to foaming.",
        counter_arguments=[
            "Antifoam does not address root causes.",
            "Contaminant removal is more effective.",
            "Excess antifoam can cause downstream issues."
        ],
        resolution_strategy="Focus on contaminant removal and TEG quality; limit antifoam use.",
        entity_scope="TEG Dehydration Units",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 20"
    ),
    DoctrineBlock(
        topic="TEG Regeneration: Stripping Gas vs Vacuum Operation",
        keywords=["TEG", "regeneration", "stripping gas", "vacuum", "dehydration", "dew point"],
        conclusion_template="Use stripping gas or vacuum operation for TEG regeneration when ultra-low water dew points are required.",
        reasoning_framework="""
        1. Assess required water dew point for downstream processes.
        2. Standard TEG regeneration achieves -40°C dew point.
        3. For lower dew points, add stripping gas or operate regenerator under vacuum.
        4. Evaluate cost, complexity, and safety of each method.
        5. Monitor TEG purity and regenerator performance.
        6. Select method based on dew point target and site constraints.
        """,
        key_factors=[
            "Target dew point",
            "Stripping gas availability",
            "Vacuum system complexity",
            "Safety considerations"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 20",
            "API 12J"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard regeneration is sufficient for all cases.",
        counter_arguments=[
            "Ultra-low dew points require enhanced regeneration.",
            "Stripping gas and vacuum are proven methods.",
            "Selection depends on site-specific factors."
        ],
        resolution_strategy="Analyze dew point requirements and site utilities; select appropriate regeneration method.",
        entity_scope="TEG Dehydration Units",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 20"
    ),
    DoctrineBlock(
        topic="NGL Product Specification and Fractionation Train Design",
        keywords=["NGL", "product specification", "fractionation", "train design", "purity", "propane", "butane"],
        conclusion_template="Design fractionation trains to meet NGL product specifications for purity and composition.",
        reasoning_framework="""
        1. Obtain product specifications for propane, butane, and other NGLs.
        2. Design deethanizer, depropanizer, and debutanizer columns accordingly.
        3. Select appropriate number of stages and reflux ratios.
        4. Size reboilers and condensers for each column.
        5. Implement advanced controls for product quality.
        6. Monitor and adjust operation to maintain specifications.
        """,
        key_factors=[
            "Product purity requirements",
            "Column design",
            "Reflux and reboiler sizing",
            "Process control"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 22",
            "API 521"
        ],
        burden_holder="Process Engineer",
        adversary_position="Fractionation train design can be standardized.",
        counter_arguments=[
            "Product specs vary by market and contract.",
            "Column design must be tailored to feed and specs.",
            "Standardization may lead to off-spec products."
        ],
        resolution_strategy="Design and simulate fractionation train for each project.",
        entity_scope="NGL Fractionation Plants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 22"
    ),
    DoctrineBlock(
        topic="Mercury Removal in Natural Gas Processing",
        keywords=["mercury", "removal", "natural gas", "activated carbon", "molecular sieve", "corrosion"],
        conclusion_template="Install mercury removal units upstream of cryogenic and aluminum equipment to prevent corrosion and contamination.",
        reasoning_framework="""
        1. Analyze feed gas for mercury content.
        2. Mercury corrodes aluminum heat exchangers and contaminates products.
        3. Use activated carbon or molecular sieve beds for removal.
        4. Monitor bed performance and replace media as required.
        5. Ensure safe handling and disposal of spent media.
        6. Comply with environmental regulations for mercury emissions.
        """,
        key_factors=[
            "Feed gas mercury content",
            "Removal technology",
            "Bed monitoring",
            "Spent media disposal"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 24",
            "API 14E"
        ],
        burden_holder="Process Engineer",
        adversary_position="Mercury removal is unnecessary for most plants.",
        counter_arguments=[
            "Mercury is highly corrosive to aluminum.",
            "Even trace amounts can cause equipment failure.",
            "Removal is standard for cryogenic plants."
        ],
        resolution_strategy="Install mercury removal upstream of sensitive equipment; monitor and maintain beds.",
        entity_scope="Natural Gas Processing Plants",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 24"
    ),
    DoctrineBlock(
        topic="Acid Gas Injection vs Sulfur Recovery Selection",
        keywords=["acid gas", "injection", "sulfur recovery", "Claus", "sequestration", "CO2", "H2S"],
        conclusion_template="Select acid gas injection for remote sites or when sulfur market is limited; Claus process for large, marketable sulfur volumes.",
        reasoning_framework="""
        1. Assess acid gas volume and composition.
        2. Evaluate local sulfur market and logistics.
        3. Acid gas injection:
            - Suitable for remote sites,
            - Reduces emissions,
            - Requires suitable geological formation.
        4. Claus process:
            - Converts H2S to elemental sulfur,
            - Requires market or disposal for sulfur.
        5. Consider regulatory and environmental requirements.
        6. Perform cost-benefit analysis for both options.
        """,
        key_factors=[
            "Acid gas volume",
            "Sulfur market",
            "Site remoteness",
            "Geological suitability",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API 942",
            "GPSA Engineering Data Book, Section 24"
        ],
        burden_holder="Project Engineer",
        adversary_position="Claus process is always preferred.",
        counter_arguments=[
            "Injection is more practical for remote or small sites.",
            "Claus requires sulfur market or disposal.",
            "Environmental regulations may favor injection."
        ],
        resolution_strategy="Assess site-specific factors and perform economic analysis.",
        entity_scope="Acid Gas Disposal and Sulfur Recovery",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API 942"
    ),
    DoctrineBlock(
        topic="Hydrate Inhibition: Methanol Injection vs Glycol",
        keywords=["hydrate", "inhibition", "methanol", "glycol", "injection", "pipeline", "prevention"],
        conclusion_template="Use methanol injection for temporary hydrate control; glycol for continuous, long-term inhibition.",
        reasoning_framework="""
        1. Identify hydrate formation risk in pipelines or process equipment.
        2. Methanol injection:
            - Effective for short-term or upset conditions,
            - High operating cost,
            - Recovery and reuse possible but complex.
        3. Glycol injection (MEG or DEG):
            - Suitable for continuous inhibition,
            - Lower operating cost,
            - Requires regeneration and reclamation systems.
        4. Select method based on duration, cost, and system design.
        5. Monitor injection rates and effectiveness.
        """,
        key_factors=[
            "Hydrate risk",
            "Duration of inhibition needed",
            "Operating cost",
            "System complexity"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 20",
            "API 14E"
        ],
        burden_holder="Process Engineer",
        adversary_position="Methanol is always the best hydrate inhibitor.",
        counter_arguments=[
            "Methanol is costly for continuous use.",
            "Glycol is more economical for long-term operation.",
            "Selection depends on system requirements."
        ],
        resolution_strategy="Evaluate hydrate risk and economics; select inhibitor accordingly.",
        entity_scope="Gas Pipelines and Processing Plants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 20"
    ),
    DoctrineBlock(
        topic="Gas Plant Flare System Design",
        keywords=["flare", "system design", "emergency", "relief", "API 521", "combustion"],
        conclusion_template="Design flare systems to safely handle emergency relief loads per API 521, with proper dispersion and combustion.",
        reasoning_framework="""
        1. Identify all relief and emergency sources.
        2. Calculate maximum relief load under worst-case scenario.
        3. Size flare header, knockout drum, and stack for safe operation.
        4. Ensure adequate dispersion and combustion at stack tip.
        5. Implement monitoring for pilot and flame presence.
        6. Comply with environmental and safety regulations.
        7. Maintain and test flare system regularly.
        """,
        key_factors=[
            "Relief load calculation",
            "Header and stack sizing",
            "Dispersion modeling",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 521",
            "GPSA Engineering Data Book, Section 5"
        ],
        burden_holder="Process Safety Engineer",
        adversary_position="Flare systems can be undersized to save cost.",
        counter_arguments=[
            "Undersized flare risks catastrophic failure.",
            "API 521 sets minimum requirements.",
            "Proper sizing ensures safety and compliance."
        ],
        resolution_strategy="Follow API 521 and perform dispersion modeling; document all calculations.",
        entity_scope="Gas Processing Plants",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 521"
    ),
    DoctrineBlock(
        topic="Pressure Relief Valve (PRV) Sizing for Gas Plants",
        keywords=["pressure relief valve", "PRV", "sizing", "API 520", "overpressure", "safety"],
        conclusion_template="Size PRVs per API 520 for worst-case overpressure scenarios, considering all credible relief cases.",
        reasoning_framework="""
        1. Identify all credible overpressure scenarios (fire, blocked outlet, thermal expansion).
        2. Calculate required relief rates for each scenario.
        3. Size PRVs using API 520 equations and methods.
        4. Consider backpressure, set pressure, and accumulation.
        5. Document all assumptions and calculations.
        6. Review sizing regularly as process changes.
        """,
        key_factors=[
            "Overpressure scenarios",
            "Relief rate calculation",
            "PRV sizing equations",
            "Backpressure effects"
        ],
        primary_authority=[
            "API 520",
            "API 521",
            "ASME BPVC Section VIII"
        ],
        burden_holder="Process Safety Engineer",
        adversary_position="PRV sizing can be based on normal operating conditions.",
        counter_arguments=[
            "Sizing must consider worst-case scenarios.",
            "API 520 provides industry standard methods.",
            "Improper sizing risks equipment and personnel."
        ],
        resolution_strategy="Follow API 520 for all PRV sizing; review regularly.",
        entity_scope="Gas Processing Plants",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API 520"
    ),
    DoctrineBlock(
        topic="Gas Plant Utility System Design: Air, Nitrogen, Instrument Air",
        keywords=["utility system", "air", "nitrogen", "instrument air", "design", "gas plant"],
        conclusion_template="Design utility systems (air, nitrogen, instrument air) for reliability and capacity, with redundancy for critical services.",
        reasoning_framework="""
        1. Identify all utility requirements for process and safety.
        2. Size air and nitrogen systems for peak and emergency loads.
        3. Provide redundancy (e.g., dual compressors, backup cylinders) for critical services.
        4. Ensure adequate distribution and pressure control.
        5. Monitor system performance and maintain regularly.
        6. Comply with safety and quality standards.
        """,
        key_factors=[
            "Utility demand",
            "Redundancy",
            "Distribution system design",
            "Monitoring and maintenance"
        ],
        primary_authority=[
            "API 14E",
            "GPSA Engineering Data Book, Section 15"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Single utility trains are sufficient for all services.",
        counter_arguments=[
            "Redundancy is critical for safety and reliability.",
            "Utility failures can shut down entire plant.",
            "Dual trains are industry standard for critical utilities."
        ],
        resolution_strategy="Design for redundancy and monitor system health.",
        entity_scope="Gas Processing Plants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 14E"
    ),
    DoctrineBlock(
        topic="Pipeline Dew Point Control: Refrigeration vs Membrane Systems",
        keywords=["pipeline", "dew point control", "refrigeration", "membrane", "hydrocarbon dew point"],
        conclusion_template="Use refrigeration for deep hydrocarbon dew point control; membranes for moderate control and lower capital cost.",
        reasoning_framework="""
        1. Determine required hydrocarbon dew point for pipeline specification.
        2. Refrigeration:
            - Achieves deep dew point control,
            - Higher capital and operating cost,
            - Suitable for high BTU gas.
        3. Membranes:
            - Moderate dew point control,
            - Lower capital cost,
            - Simpler operation.
        4. Select method based on dew point target, economics, and site constraints.
        5. Monitor product quality and adjust operation as needed.
        """,
        key_factors=[
            "Dew point specification",
            "Feed gas BTU",
            "Capital and operating cost",
            "System complexity"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 21",
            "API 14E"
        ],
        burden_holder="Process Engineer",
        adversary_position="Membranes are always sufficient for dew point control.",
        counter_arguments=[
            "Membranes have limited dew point reduction capability.",
            "Refrigeration is required for deep control.",
            "Selection depends on specification and economics."
        ],
        resolution_strategy="Evaluate dew point requirements and perform economic analysis.",
        entity_scope="Pipeline Gas Conditioning",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 21"
    ),
    DoctrineBlock(
        topic="Natural Gas Liquids (NGL) Storage and Handling",
        keywords=["NGL", "storage", "handling", "tank", "safety", "vapor recovery"],
        conclusion_template="Design NGL storage for pressure and temperature control, with vapor recovery and safety systems.",
        reasoning_framework="""
        1. Select storage tanks for NGL based on pressure and temperature requirements.
        2. Provide vapor recovery to minimize emissions.
        3. Implement safety systems (pressure relief, fire protection).
        4. Monitor tank levels and pressure continuously.
        5. Comply with API and local regulations for storage and handling.
        6. Train operators on safe handling procedures.
        """,
        key_factors=[
            "Tank selection",
            "Vapor recovery",
            "Safety systems",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 650",
            "API 2510",
            "GPSA Engineering Data Book, Section 23"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="NGL can be stored in standard atmospheric tanks.",
        counter_arguments=[
            "NGL requires pressurized or refrigerated storage.",
            "Atmospheric tanks risk vapor loss and safety incidents.",
            "API standards specify storage requirements."
        ],
        resolution_strategy="Design storage per API 2510 and local regulations.",
        entity_scope="NGL Storage Facilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 2510"
    ),
    DoctrineBlock(
        topic="Gas Plant Control System Architecture: DCS vs PLC",
        keywords=["control system", "DCS", "PLC", "architecture", "automation", "gas plant"],
        conclusion_template="Use DCS for large, integrated gas plants; PLCs for small, discrete systems or as subsystems.",
        reasoning_framework="""
        1. Assess plant size, complexity, and integration needs.
        2. DCS:
            - Centralized control,
            - Scalable for large plants,
            - Advanced process control features.
        3. PLC:
            - Suited for small, discrete systems,
            - Fast response, simple logic,
            - Used as subsystems within DCS.
        4. Consider reliability, expandability, and lifecycle cost.
        5. Integrate safety instrumented systems as required.
        """,
        key_factors=[
            "Plant size and complexity",
            "Integration requirements",
            "Control system reliability",
            "Lifecycle cost"
        ],
        primary_authority=[
            "ISA 88",
            "API 14C",
            "GPSA Engineering Data Book, Section 16"
        ],
        burden_holder="Automation Engineer",
        adversary_position="PLCs are sufficient for all gas plant control needs.",
        counter_arguments=[
            "DCS provides better integration for large plants.",
            "PLCs are best for small or discrete systems.",
            "Hybrid architectures are common."
        ],
        resolution_strategy="Select architecture based on plant requirements and future expansion.",
        entity_scope="Gas Plant Control Systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ISA 88"
    ),
    DoctrineBlock(
        topic="Gas Metering: Orifice vs Ultrasonic Flow Measurement",
        keywords=["gas metering", "orifice", "ultrasonic", "flow measurement", "custody transfer"],
        conclusion_template="Use ultrasonic meters for high-accuracy custody transfer and large pipelines; orifice meters for smaller lines and lower cost.",
        reasoning_framework="""
        1. Determine metering accuracy and range requirements.
        2. Orifice meters:
            - Lower capital cost,
            - Suitable for small to medium lines,
            - Requires regular plate inspection.
        3. Ultrasonic meters:
            - High accuracy, low pressure drop,
            - Best for large pipelines and custody transfer,
            - Higher capital cost, lower maintenance.
        4. Select meter type based on application, accuracy, and cost.
        5. Calibrate and maintain meters per standards.
        """,
        key_factors=[
            "Accuracy requirements",
            "Pipeline size",
            "Capital and maintenance cost",
            "Custody transfer standards"
        ],
        primary_authority=[
            "AGA Report No. 3",
            "AGA Report No. 9",
            "API 14.3"
        ],
        burden_holder="Measurement Engineer",
        adversary_position="Orifice meters are obsolete.",
        counter_arguments=[
            "Orifice meters are still widely used for small lines.",
            "Ultrasonic meters are preferred for large lines.",
            "Selection depends on application and cost."
        ],
        resolution_strategy="Select meter type based on project requirements and standards.",
        entity_scope="Gas Metering Stations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AGA Report No. 9"
    ),
    DoctrineBlock(
        topic="Gas Plant Start-up and Commissioning Procedures",
        keywords=["start-up", "commissioning", "gas plant", "procedures", "safety", "checklist"],
        conclusion_template="Follow detailed start-up and commissioning procedures to ensure safety and performance before introducing hydrocarbons.",
        reasoning_framework="""
        1. Develop comprehensive start-up and commissioning plan.
        2. Verify mechanical completion and system integrity.
        3. Perform pre-commissioning checks (flushing, leak testing, calibration).
        4. Test all safety and control systems.
        5. Introduce inert gas for purging and pressure testing.
        6. Gradually introduce hydrocarbons and monitor system response.
        7. Document all steps and obtain management approval.
        """,
        key_factors=[
            "Commissioning plan",
            "System integrity",
            "Safety system testing",
            "Documentation"
        ],
        primary_authority=[
            "API 14C",
            "GPSA Engineering Data Book, Section 2"
        ],
        burden_holder="Commissioning Manager",
        adversary_position="Start-up can be expedited by skipping some checks.",
        counter_arguments=[
            "Skipping checks risks safety and equipment damage.",
            "Proper commissioning ensures reliable operation.",
            "Documentation is required for regulatory compliance."
        ],
        resolution_strategy="Follow detailed procedures and obtain sign-off at each stage.",
        entity_scope="Gas Processing Plants",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API 14C"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring and Control in Gas Plants",
        keywords=["corrosion", "monitoring", "control", "gas plant", "inspection", "mitigation"],
        conclusion_template="Implement corrosion monitoring and control programs to ensure equipment integrity and prevent failures.",
        reasoning_framework="""
        1. Identify corrosion risks (wet gas, acid gas, amine systems).
        2. Install corrosion monitoring devices (probes, coupons).
        3. Perform regular inspections and thickness measurements.
        4. Apply corrosion inhibitors as needed.
        5. Replace or repair corroded equipment promptly.
        6. Maintain records and trend data for analysis.
        """,
        key_factors=[
            "Corrosion risk assessment",
            "Monitoring device selection",
            "Inspection frequency",
            "Inhibitor application"
        ],
        primary_authority=[
            "API 510",
            "API 570",
            "NACE SP0106"
        ],
        burden_holder="Integrity Engineer",
        adversary_position="Corrosion monitoring is unnecessary with new equipment.",
        counter_arguments=[
            "Corrosion can occur rapidly in gas plants.",
            "Monitoring is essential for early detection.",
            "API and NACE standards require monitoring."
        ],
        resolution_strategy="Implement comprehensive monitoring and control program.",
        entity_scope="Gas Processing Plants",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 510"
    ),
    DoctrineBlock(
        topic="Gas Plant Emergency Shutdown (ESD) System Design",
        keywords=["emergency shutdown", "ESD", "system design", "gas plant", "safety", "API 14C"],
        conclusion_template="Design ESD systems to safely isolate and depressurize gas plants during emergencies, per API 14C.",
        reasoning_framework="""
        1. Identify all emergency scenarios requiring shutdown.
        2. Design ESD system to isolate, depressurize, and vent as needed.
        3. Provide redundant power and control for ESD valves.
        4. Test ESD system regularly and maintain documentation.
        5. Integrate ESD with fire and gas detection systems.
        6. Comply with API 14C and local safety regulations.
        """,
        key_factors=[
            "Emergency scenario identification",
            "System redundancy",
            "Testing and maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 14C",
            "GPSA Engineering Data Book, Section 16"
        ],
        burden_holder="Process Safety Engineer",
        adversary_position="ESD systems can be simplified to reduce cost.",
        counter_arguments=[
            "ESD is critical for plant safety.",
            "Redundancy and regular testing are required.",
            "API 14C sets minimum requirements."
        ],
        resolution_strategy="Design and maintain ESD per API 14C; test regularly.",
        entity_scope="Gas Processing Plants",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 14C"
    ),
    DoctrineBlock(
        topic="Sour Water Stripping in Gas Plants",
        keywords=["sour water", "stripping", "H2S", "ammonia", "treatment", "gas plant"],
        conclusion_template="Strip H2S and ammonia from sour water before discharge or reuse; comply with environmental regulations.",
        reasoning_framework="""
        1. Analyze sour water composition for H2S and ammonia.
        2. Design stripper column with sufficient stages for removal.
        3. Provide steam or reboiler heat for stripping.
        4. Monitor effluent quality and adjust operation as needed.
        5. Comply with discharge and reuse regulations.
        6. Safely handle and treat stripped gases.
        """,
        key_factors=[
            "Sour water composition",
            "Stripper design",
            "Effluent quality monitoring",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 12J",
            "GPSA Engineering Data Book, Section 24"
        ],
        burden_holder="Process Engineer",
        adversary_position="Sour water can be discharged without treatment.",
        counter_arguments=[
            "H2S and ammonia are regulated contaminants.",
            "Stripping is standard practice.",
            "Non-compliance leads to penalties."
        ],
        resolution_strategy="Design and operate sour water stripper per regulations.",
        entity_scope="Gas Processing Plants",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 12J"
    ),
    DoctrineBlock(
        topic="Gas Plant Waste Heat Recovery",
        keywords=["waste heat", "recovery", "energy efficiency", "heat exchanger", "gas plant"],
        conclusion_template="Implement waste heat recovery from process streams to improve energy efficiency and reduce operating costs.",
        reasoning_framework="""
        1. Identify process streams with recoverable heat.
        2. Install heat exchangers for preheating or steam generation.
        3. Integrate waste heat recovery into overall energy balance.
        4. Monitor performance and maintain equipment.
        5. Evaluate economic benefits and payback period.
        6. Comply with safety and design standards.
        """,
        key_factors=[
            "Heat source identification",
            "Exchanger design",
            "Integration with process",
            "Economic analysis"
        ],
        primary_authority=[
            "API 521",
            "GPSA Engineering Data Book, Section 5"
        ],
        burden_holder="Process Engineer",
        adversary_position="Waste heat recovery is not cost-effective.",
        counter_arguments=[
            "Energy savings reduce operating costs.",
            "Payback periods are typically short.",
            "Waste heat recovery is industry best practice."
        ],
        resolution_strategy="Perform energy balance and economic analysis; implement where feasible.",
        entity_scope="Gas Processing Plants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 521"
    ),
    DoctrineBlock(
        topic="Gas Plant Noise and Vibration Control",
        keywords=["noise", "vibration", "control", "gas plant", "compressor", "health"],
        conclusion_template="Implement noise and vibration control measures to protect personnel and equipment, complying with health and safety standards.",
        reasoning_framework="""
        1. Identify major noise and vibration sources (compressors, pumps).
        2. Install silencers, acoustic enclosures, and vibration isolators.
        3. Monitor noise and vibration levels regularly.
        4. Maintain equipment to minimize abnormal noise/vibration.
        5. Train personnel on exposure risks and controls.
        6. Comply with OSHA and local standards.
        """,
        key_factors=[
            "Source identification",
            "Control measure selection",
            "Monitoring and maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "OSHA 1910.95",
            "API 618",
            "GPSA Engineering Data Book, Section 13"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Noise and vibration control is unnecessary.",
        counter_arguments=[
            "Excessive noise/vibration harms personnel and equipment.",
            "Controls are required by law.",
            "Prevention reduces long-term costs."
        ],
        resolution_strategy="Implement controls and monitor compliance.",
        entity_scope="Gas Processing Plants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="OSHA 1910.95"
    ),
    DoctrineBlock(
        topic="Gas Plant Fire Protection System Design",
        keywords=["fire protection", "system design", "gas plant", "safety", "NFPA", "API 2218"],
        conclusion_template="Design fire protection systems per NFPA and API 2218, including detection, suppression, and emergency response.",
        reasoning_framework="""
        1. Identify fire risks and critical equipment.
        2. Install fire detection (smoke, heat, flame detectors).
        3. Provide suppression systems (sprinklers, deluge, foam).
        4. Develop emergency response and evacuation plans.
        5. Train personnel and conduct drills.
        6. Maintain and test fire protection systems regularly.
        7. Comply with NFPA and API standards.
        """,
        key_factors=[
            "Fire risk assessment",
            "Detection and suppression",
            "Emergency response planning",
            "System maintenance"
        ],
        primary_authority=[
            "NFPA 30",
            "API 2218",
            "GPSA Engineering Data Book, Section 17"
        ],
        burden_holder="Safety Engineer",
        adversary_position="Fire protection can be limited to portable extinguishers.",
        counter_arguments=[
            "Fixed systems provide faster, more reliable response.",
            "NFPA and API standards require comprehensive systems.",
            "Personnel safety depends on robust protection."
        ],
        resolution_strategy="Design and maintain fire protection per standards; train personnel.",
        entity_scope="Gas Processing Plants",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NFPA 30"
    ),
    DoctrineBlock(
        topic="Gas Plant Fugitive Emissions Monitoring and Control",
        keywords=["fugitive emissions", "monitoring", "control", "LDAR", "gas plant", "VOC"],
        conclusion_template="Implement LDAR programs to monitor and control fugitive emissions per environmental regulations.",
        reasoning_framework="""
        1. Identify all potential sources of fugitive emissions (valves, flanges, pumps).
        2. Develop and implement Leak Detection and Repair (LDAR) program.
        3. Monitor emissions regularly using approved methods.
        4. Repair leaks promptly and document actions.
        5. Report emissions as required by regulations.
        6. Train personnel on LDAR procedures.
        """,
        key_factors=[
            "Emission source identification",
            "Monitoring frequency",
            "Repair response time",
            "Regulatory reporting"
        ],
        primary_authority=[
            "US EPA 40 CFR 60 Subpart OOOOa",
            "API 624",
            "GPSA Engineering Data Book, Section 24"
        ],
        burden_holder="Environmental Engineer",
        adversary_position="Fugitive emissions are negligible and do not require monitoring.",
        counter_arguments=[
            "Fugitive emissions are regulated and can be significant.",
            "LDAR programs are required by law.",
            "Prompt repair reduces emissions and cost."
        ],
        resolution_strategy="Implement and maintain LDAR program; monitor and report as required.",
        entity_scope="Gas Processing Plants",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="US EPA 40 CFR 60 Subpart OOOOa"
    ),
    DoctrineBlock(
        topic="Gas Plant Turnaround Planning and Execution",
        keywords=["turnaround", "planning", "execution", "gas plant", "maintenance", "shutdown"],
        conclusion_template="Plan and execute gas plant turnarounds with detailed scope, schedule, and safety procedures to minimize downtime.",
        reasoning_framework="""
        1. Develop comprehensive turnaround scope and schedule.
        2. Identify all maintenance, inspection, and upgrade activities.
        3. Coordinate with operations, maintenance, and contractors.
        4. Implement safety procedures and permit-to-work system.
        5. Monitor progress and adjust schedule as needed.
        6. Document all work and lessons learned.
        """,
        key_factors=[
            "Scope definition",
            "Scheduling",
            "Safety procedures",
            "Coordination and communication"
        ],
        primary_authority=[
            "API 510",
            "API 570",
            "GPSA Engineering Data Book, Section 2"
        ],
        burden_holder="Turnaround Manager",
        adversary_position="Turnarounds can be managed on an ad hoc basis.",
        counter_arguments=[
            "Detailed planning reduces downtime and cost.",
            "Safety risks increase without proper procedures.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Develop and execute detailed turnaround plan.",
        entity_scope="Gas Processing Plants",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 510"
    ),
    DoctrineBlock(
        topic="Gas Plant Water Disposal and Reuse",
        keywords=["water disposal", "reuse", "gas plant", "treatment", "environmental", "regulations"],
        conclusion_template="Treat and dispose of gas plant water streams per environmental regulations; maximize reuse where feasible.",
        reasoning_framework="""
        1. Characterize all water streams (produced water, sour water, condensate).
        2. Select appropriate treatment technologies (oil removal, stripping, filtration).
        3. Monitor effluent quality and comply with discharge permits.
        4. Evaluate opportunities for water reuse within the plant.
        5. Document treatment and disposal activities.
        6. Update treatment as regulations evolve.
        """,
        key_factors=[
            "Water stream characterization",
            "Treatment technology selection",
            "Effluent quality monitoring",
            "Regulatory compliance"
        ],
        primary_authority=[
            "US EPA 40 CFR 435",
            "API 12J",
            "GPSA Engineering Data Book, Section 24"
        ],
        burden_holder="Environmental Engineer",
        adversary_position="Produced water can be discharged without treatment.",
        counter_arguments=[
            "Produced water contains regulated contaminants.",
            "Treatment is required for compliance.",
            "Reuse reduces water consumption and cost."
        ],
        resolution_strategy="Treat all water streams per regulations; maximize reuse.",
        entity_scope="Gas Processing Plants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="US EPA 40 CFR 435"
    ),
    DoctrineBlock(
        topic="Gas Plant Process Simulation and Optimization",
        keywords=["process simulation", "optimization", "gas plant", "modeling", "Aspen HYSYS", "ProMax"],
        conclusion_template="Use process simulation software for design, optimization, and troubleshooting of gas plant operations.",
        reasoning_framework="""
        1. Develop accurate process models using validated software (e.g., Aspen HYSYS, ProMax).
        2. Input representative feed and operating data.
        3. Calibrate model with plant data and lab results.
        4. Use simulation for design, debottlenecking, and optimization studies.
        5. Document assumptions, results, and recommendations.
        6. Update models as plant or feed changes.
        """,
        key_factors=[
            "Model accuracy",
            "Data validation",
            "Simulation objectives",
            "Documentation"
        ],
        primary_authority=[
            "GPSA Engineering Data Book, Section 2",
            "API 14E"
        ],
        burden_holder="Process Engineer",
        adversary_position="Simulation is unnecessary for experienced operators.",
        counter_arguments=[
            "Simulation improves design and troubleshooting.",
            "Models identify optimization opportunities.",
            "Industry standards require simulation for major changes."
        ],
        resolution_strategy="Develop and maintain accurate process models.",
        entity_scope="Gas Processing Plants",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="GPSA Engineering Data Book, Section 2"
    ),
    DoctrineBlock(
        topic="Gas Plant Operator Training and Competency",
        keywords=["operator training", "competency", "gas plant", "procedures", "safety", "certification"],
        conclusion_template="Implement comprehensive operator training and competency programs to ensure safe and efficient gas plant operation.",
        reasoning_framework="""
        1. Develop training curriculum covering all plant systems and procedures.
        2. Certify operators on safety, emergency response, and process operation.
        3. Conduct regular refresher training and assessments.
        4. Maintain training records and competency matrices.
        5. Update training as plant or regulatory requirements change.
        """,
        key_factors=[
            "Training curriculum",
            "Certification",
            "Refresher training",
            "Recordkeeping"
        ],
        primary_authority=[
            "API 1161",
            "GPSA Engineering Data Book, Section 2"
        ],
        burden_holder="Operations Manager",
        adversary_position="On-the-job training is sufficient.",
        counter_arguments=[
            "Formal training improves safety and efficiency.",
            "Certification is required by many regulators.",
            "Refresher training addresses knowledge gaps."
        ],
        resolution_strategy="Implement and document comprehensive training program.",
        entity_scope="Gas Processing Plants",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 1161"
    ),
    DoctrineBlock(
        topic="Gas Plant Process Safety Management (PSM)",
        keywords=["process safety management", "PSM", "gas plant", "OSHA", "risk assessment", "procedures"],
        conclusion_template="Implement PSM programs per OSHA 1910.119 to manage process risks and ensure safe operation.",
        reasoning_framework="""
        1. Develop and document all PSM elements (procedures, training, MOC, PHA).
        2. Conduct regular process hazard analyses (PHA).
        3. Manage changes through formal MOC process.
        4. Investigate incidents and implement corrective actions.
        5. Train personnel on PSM requirements.
        6. Audit and update PSM program regularly.
        """,
        key_factors=[
            "PSM element implementation",
            "PHA frequency",
            "Incident investigation",
            "Training and auditing"
        ],
        primary_authority=[
            "OSHA 1910.119",
            "API RP 750"
        ],
        burden_holder="Process Safety Manager",
        adversary_position="PSM is only required for large plants.",
        counter_arguments=[
            "OSHA applies to all covered processes.",
            "PSM reduces risk and incidents.",
            "Auditing ensures program effectiveness."
        ],
        resolution_strategy="Implement and maintain PSM for all covered processes.",
        entity_scope="Gas Processing Plants",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="OSHA 1910.119"
    ),
    DoctrineBlock(
        topic="Gas Plant Data Management and Digitalization",
        keywords=["data management", "digitalization", "gas plant", "automation", "historian", "analytics"],
        conclusion_template="Implement digital data management systems for real-time monitoring, analytics, and decision support.",
        reasoning_framework="""
        1. Install data historian and real-time monitoring systems.
        2. Integrate process data with analytics and reporting tools.
        3. Ensure data security and backup.
        4. Train personnel on data access and interpretation.
        5. Use analytics for predictive maintenance and optimization.
        6. Update systems as technology evolves.
        """,
        key_factors=[
            "Data historian implementation",
            "Analytics integration",
            "Data security",
            "Personnel training"
        ],
        primary_authority=[
            "ISA 95",
            "API 1165"
        ],
        burden_holder="IT/Automation Engineer",
        adversary_position="Manual data collection is sufficient.",
        counter_arguments=[
            "Digital systems improve efficiency and reliability.",
            "Analytics enable predictive maintenance.",
            "Manual collection is error-prone and slow."
        ],
        resolution_strategy="Implement and maintain digital data management systems.",
        entity_scope="Gas Processing Plants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISA 95"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]