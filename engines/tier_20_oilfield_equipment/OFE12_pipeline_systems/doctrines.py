from dataclasses import dataclass
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
        topic="Pipeline Hydraulics: Darcy-Weisbach Equation",
        keywords=["hydraulics", "Darcy-Weisbach", "friction", "pressure drop", "flow"],
        conclusion_template="The Darcy-Weisbach equation is the governing formula for calculating pressure drop due to friction in pipeline flow.",
        reasoning_framework=(
            "The Darcy-Weisbach equation relates the pressure drop in a pipe to the flow velocity, pipe diameter, length, and friction factor. "
            "The friction factor is determined by the Reynolds number and pipe roughness, often using the Moody chart. "
            "For turbulent flow, the friction factor is calculated iteratively or via empirical correlations. "
            "The equation is applicable for both gas and liquid pipelines, provided the flow regime and pipe material are correctly characterized. "
            "Accurate determination of the friction factor is critical for reliable hydraulic modeling. "
            "Boundary conditions, such as inlet/outlet pressure and temperature, must be accounted for. "
            "The equation is widely accepted in industry standards and forms the basis for pipeline design and operation. "
            "Limitations include assumptions of steady-state flow and uniform pipe geometry. "
            "For complex geometries or transient conditions, computational fluid dynamics (CFD) may be required. "
            "The equation's validity is supported by ASME B31.4 and B31.8 codes. "
            "Disputes typically arise over friction factor selection and roughness values, which can be resolved by referencing authoritative charts and empirical data. "
            "The burden of proof lies with the designer to justify parameter selection. "
            "Counter arguments may cite alternative equations (e.g., Hazen-Williams) but are generally less applicable for hydrocarbon pipelines. "
            "Resolution involves adherence to industry standards and documented calculation methodologies."
        ),
        key_factors=[
            "Flow velocity",
            "Pipe diameter",
            "Pipe length",
            "Friction factor",
            "Fluid properties",
            "Pipe roughness"
        ],
        primary_authority=[
            "ASME B31.4",
            "ASME B31.8",
            "Moody Chart"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Alternative friction equations may be more appropriate for certain fluids.",
        counter_arguments=[
            "Hazen-Williams equation is less accurate for hydrocarbons.",
            "Empirical correlations may not reflect actual pipe conditions."
        ],
        resolution_strategy="Reference ASME codes and Moody chart for friction factor determination.",
        entity_scope="Pipeline Engineering",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 403.2.2"
    ),
    DoctrineBlock(
        topic="Pipeline Hydraulics: Moody Friction Factor",
        keywords=["hydraulics", "Moody chart", "friction factor", "Reynolds number", "pipe roughness"],
        conclusion_template="The Moody chart is the authoritative source for determining friction factor in pipeline hydraulics.",
        reasoning_framework=(
            "The Moody chart provides a graphical representation of the relationship between Reynolds number, relative roughness, and friction factor. "
            "It is used to determine the friction factor for both laminar and turbulent flow regimes. "
            "For laminar flow (Re < 2000), the friction factor is calculated directly as f = 64/Re. "
            "For turbulent flow, the chart or Colebrook-White equation is used. "
            "The chart is based on extensive experimental data and is referenced in all major pipeline design codes. "
            "Selection of pipe roughness must be based on material specifications and condition (new, aged, coated). "
            "Errors in friction factor selection can lead to significant inaccuracies in hydraulic modeling. "
            "Disputes may arise regarding roughness values, which should be resolved by referencing API and ASME standards. "
            "The burden of proof is on the designer to document parameter selection. "
            "Alternative charts or correlations may be used, but Moody remains the industry standard."
        ),
        key_factors=[
            "Reynolds number",
            "Relative roughness",
            "Pipe material",
            "Flow regime"
        ],
        primary_authority=[
            "Moody Chart",
            "ASME B31.4",
            "API 5L"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Alternative friction factor correlations may be more accurate for specific cases.",
        counter_arguments=[
            "Colebrook-White equation provides numerical solution.",
            "Swamee-Jain equation offers simplified calculation."
        ],
        resolution_strategy="Use Moody chart unless specific conditions warrant alternative correlations.",
        entity_scope="Pipeline Engineering",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 403.2.2"
    ),
    DoctrineBlock(
        topic="Pipeline Sizing: Velocity Criteria",
        keywords=["sizing", "velocity", "design", "erosion", "throughput"],
        conclusion_template="Pipeline sizing must ensure that flow velocity remains within industry-accepted limits to prevent erosion and optimize throughput.",
        reasoning_framework=(
            "Pipeline velocity is a critical parameter in sizing, affecting erosion, noise, and pressure drop. "
            "Industry standards recommend maximum velocities for different fluids: typically 1-3 m/s for crude oil, 5-10 m/s for natural gas. "
            "Exceeding velocity limits can cause internal erosion, vibration, and reduce pipeline lifespan. "
            "Velocity is calculated based on desired throughput and pipe diameter. "
            "Sizing must balance throughput requirements with velocity constraints. "
            "Regulatory codes (ASME B31.4, B31.8) specify velocity limits for safety and integrity. "
            "Disputes may arise over optimal velocity selection, often resolved by referencing code requirements and operational experience. "
            "The burden of proof is on the designer to justify sizing decisions. "
            "Counter arguments may cite economic benefits of higher velocities, but safety and longevity take precedence."
        ),
        key_factors=[
            "Fluid type",
            "Pipe diameter",
            "Throughput",
            "Velocity limits",
            "Erosion risk"
        ],
        primary_authority=[
            "ASME B31.4",
            "ASME B31.8",
            "API 5L"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Higher velocities increase throughput and reduce capital costs.",
        counter_arguments=[
            "Erosion and noise risks outweigh economic benefits.",
            "Regulatory codes mandate velocity limits."
        ],
        resolution_strategy="Adhere to code-specified velocity limits and document rationale.",
        entity_scope="Pipeline Engineering",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 403.3"
    ),
    DoctrineBlock(
        topic="Pipeline Sizing: Pressure Drop Calculation",
        keywords=["sizing", "pressure drop", "hydraulics", "design", "throughput"],
        conclusion_template="Pressure drop calculations are essential for pipeline sizing and must conform to industry standards.",
        reasoning_framework=(
            "Pressure drop is calculated using hydraulic equations (Darcy-Weisbach) and is influenced by pipe diameter, length, flow rate, and friction factor. "
            "Accurate pressure drop estimation ensures proper selection of pumps and compressors. "
            "Regulatory codes require documentation of pressure drop calculations for new and modified pipelines. "
            "Disputes may arise over calculation methodology, often resolved by referencing ASME and API standards. "
            "The burden of proof is on the designer to demonstrate compliance with codes and justify parameter selection. "
            "Counter arguments may cite alternative calculation methods, but industry standards prevail."
        ),
        key_factors=[
            "Pipe diameter",
            "Pipe length",
            "Flow rate",
            "Friction factor",
            "Fluid properties"
        ],
        primary_authority=[
            "ASME B31.4",
            "ASME B31.8",
            "API 5L"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Alternative calculation methods may yield different results.",
        counter_arguments=[
            "Industry standards specify calculation methodology.",
            "Empirical methods may lack accuracy."
        ],
        resolution_strategy="Follow ASME and API calculation procedures.",
        entity_scope="Pipeline Engineering",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 403.2"
    ),
    DoctrineBlock(
        topic="Pipeline Sizing: Throughput Optimization",
        keywords=["sizing", "throughput", "optimization", "capacity", "design"],
        conclusion_template="Pipeline sizing must optimize throughput while maintaining compliance with velocity and pressure drop limits.",
        reasoning_framework=(
            "Throughput optimization involves balancing pipe diameter, flow velocity, and pressure drop to maximize capacity. "
            "Economic analysis is required to determine optimal sizing, considering capital and operational costs. "
            "Regulatory codes constrain velocity and pressure drop, limiting throughput. "
            "Optimization models may be used to evaluate multiple sizing scenarios. "
            "Disputes may arise over economic assumptions and risk tolerance. "
            "The burden of proof is on the designer to justify sizing decisions based on documented analysis. "
            "Counter arguments may cite alternative optimization criteria, but safety and compliance take precedence."
        ),
        key_factors=[
            "Pipe diameter",
            "Flow velocity",
            "Pressure drop",
            "Economic analysis",
            "Regulatory limits"
        ],
        primary_authority=[
            "ASME B31.4",
            "ASME B31.8",
            "API 5L"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Higher throughput may justify increased risk.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Long-term operational risks outweigh short-term gains."
        ],
        resolution_strategy="Document optimization analysis and ensure compliance with codes.",
        entity_scope="Pipeline Engineering",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 403.3"
    ),
    DoctrineBlock(
        topic="Pipeline Materials: API 5L Grade X52",
        keywords=["materials", "API 5L", "X52", "steel", "mechanical properties"],
        conclusion_template="API 5L Grade X52 is a standard material for pipeline construction, offering balanced strength and weldability.",
        reasoning_framework=(
            "API 5L Grade X52 is widely used for oil and gas pipelines due to its mechanical properties and compliance with industry standards. "
            "It offers moderate yield strength (52,000 psi) and is suitable for most onshore and offshore applications. "
            "Weldability is good, allowing use of standard welding procedures. "
            "Material selection must consider design pressure, environmental conditions, and regulatory requirements. "
            "Disputes may arise over material suitability for specific applications, resolved by referencing API and ASME codes. "
            "The burden of proof is on the designer to justify material selection based on documented analysis. "
            "Counter arguments may cite higher grades for increased strength, but cost and weldability must be considered."
        ),
        key_factors=[
            "Yield strength",
            "Weldability",
            "Corrosion resistance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 5L",
            "ASME B31.4",
            "ASME B31.8"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Higher grade materials may offer better performance.",
        counter_arguments=[
            "Cost and weldability are critical factors.",
            "API 5L X52 meets most design requirements."
        ],
        resolution_strategy="Document material selection and justify based on design requirements.",
        entity_scope="Pipeline Engineering",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 5L Section 6"
    ),
    DoctrineBlock(
        topic="Pipeline Materials: API 5L Grade X65",
        keywords=["materials", "API 5L", "X65", "steel", "mechanical properties"],
        conclusion_template="API 5L Grade X65 provides higher strength for pipelines requiring increased pressure ratings.",
        reasoning_framework=(
            "API 5L Grade X65 is selected for pipelines with higher design pressures or longer spans. "
            "It offers yield strength of 65,000 psi, allowing for reduced wall thickness and lower material costs. "
            "Weldability is slightly reduced compared to X52, requiring more stringent welding procedures. "
            "Material selection must consider operational pressures, environmental factors, and regulatory compliance. "
            "Disputes may arise over weldability and fracture toughness, resolved by referencing API and ASME standards. "
            "The burden of proof is on the designer to justify material selection. "
            "Counter arguments may cite increased welding complexity, but strength benefits often outweigh drawbacks."
        ),
        key_factors=[
            "Yield strength",
            "Weldability",
            "Fracture toughness",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 5L",
            "ASME B31.4",
            "ASME B31.8"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Welding procedures may be more complex for X65.",
        counter_arguments=[
            "Strength benefits allow reduced wall thickness.",
            "API 5L X65 is industry standard for high-pressure pipelines."
        ],
        resolution_strategy="Document welding procedures and material selection rationale.",
        entity_scope="Pipeline Engineering",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 5L Section 6"
    ),
    DoctrineBlock(
        topic="Pipeline Materials: API 5L Grade X70",
        keywords=["materials", "API 5L", "X70", "steel", "high strength"],
        conclusion_template="API 5L Grade X70 is used for high-pressure pipelines, offering superior strength and reduced wall thickness.",
        reasoning_framework=(
            "API 5L Grade X70 provides yield strength of 70,000 psi, enabling construction of pipelines with high pressure ratings and long spans. "
            "Material selection must consider weldability, fracture toughness, and susceptibility to hydrogen-induced cracking. "
            "Welding procedures must be carefully documented and qualified. "
            "Disputes may arise over material suitability for harsh environments, resolved by referencing API and ASME codes. "
            "The burden of proof is on the designer to justify material selection and welding procedures. "
            "Counter arguments may cite increased risk of cracking and reduced weldability, but proper procedures mitigate these risks."
        ),
        key_factors=[
            "Yield strength",
            "Weldability",
            "Hydrogen-induced cracking",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 5L",
            "ASME B31.4",
            "ASME B31.8"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="High-strength steels may be more susceptible to cracking.",
        counter_arguments=[
            "Qualified welding procedures mitigate risks.",
            "API 5L X70 is standard for high-pressure pipelines."
        ],
        resolution_strategy="Qualify welding procedures and document material selection.",
        entity_scope="Pipeline Engineering",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 5L Section 6"
    ),
    DoctrineBlock(
        topic="Pipeline Materials: API 5L Grade X80",
        keywords=["materials", "API 5L", "X80", "steel", "ultra-high strength"],
        conclusion_template="API 5L Grade X80 is used for ultra-high pressure pipelines, requiring advanced welding and inspection procedures.",
        reasoning_framework=(
            "API 5L Grade X80 offers yield strength of 80,000 psi and is used for pipelines with extreme pressure requirements. "
            "Material selection must consider weldability, fracture toughness, and susceptibility to brittle fracture. "
            "Advanced welding procedures and inspection techniques are required. "
            "Disputes may arise over material suitability and welding complexity, resolved by referencing API and ASME codes. "
            "The burden of proof is on the designer to justify material and procedure selection. "
            "Counter arguments may cite increased risk of brittle fracture, but proper procedures and inspection mitigate risks."
        ),
        key_factors=[
            "Yield strength",
            "Weldability",
            "Brittle fracture risk",
            "Inspection procedures"
        ],
        primary_authority=[
            "API 5L",
            "ASME B31.4",
            "ASME B31.8"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="X80 requires advanced welding and inspection.",
        counter_arguments=[
            "Strength benefits justify complexity.",
            "API 5L X80 is standard for ultra-high pressure pipelines."
        ],
        resolution_strategy="Implement advanced welding and inspection procedures.",
        entity_scope="Pipeline Engineering",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 5L Section 6"
    ),
    DoctrineBlock(
        topic="Pipeline Welding Procedures: WPS and PQR",
        keywords=["welding", "WPS", "PQR", "procedure qualification", "documentation"],
        conclusion_template="Welding Procedure Specification (WPS) and Procedure Qualification Record (PQR) are mandatory for pipeline welding.",
        reasoning_framework=(
            "WPS and PQR documents are required for all pipeline welding operations. "
            "WPS outlines the welding process, parameters, and materials, while PQR documents the qualification of the procedure through testing. "
            "Regulatory codes (ASME B31.4, B31.8) mandate the use of qualified procedures. "
            "Disputes may arise over procedure qualification, resolved by referencing code requirements and test results. "
            "The burden of proof is on the contractor to provide qualified procedures and documentation. "
            "Counter arguments may cite alternative procedures, but only qualified and documented procedures are acceptable."
        ),
        key_factors=[
            "Welding process",
            "Procedure qualification",
            "Documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "ASME B31.8",
            "API 1104"
        ],
        burden_holder="Contractor",
        adversary_position="Alternative procedures may be faster or cheaper.",
        counter_arguments=[
            "Regulatory codes mandate qualified procedures.",
            "Unqualified procedures are not acceptable."
        ],
        resolution_strategy="Require WPS and PQR documentation for all welding operations.",
        entity_scope="Pipeline Construction",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 434"
    ),
    DoctrineBlock(
        topic="Pipeline Welding Procedures: SMAW",
        keywords=["welding", "SMAW", "shielded metal arc", "manual welding", "procedure"],
        conclusion_template="Shielded Metal Arc Welding (SMAW) is a standard manual welding process for pipeline construction.",
        reasoning_framework=(
            "SMAW is widely used for manual welding of pipeline joints, offering flexibility and reliability. "
            "Procedure qualification is required, including WPS and PQR documentation. "
            "SMAW is suitable for field conditions and various pipe materials. "
            "Disputes may arise over weld quality and productivity, resolved by referencing code requirements and inspection results. "
            "The burden of proof is on the contractor to demonstrate procedure qualification and weld quality. "
            "Counter arguments may cite alternative processes, but SMAW remains industry standard for manual welding."
        ),
        key_factors=[
            "Welding process",
            "Procedure qualification",
            "Weld quality",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "ASME B31.8",
            "API 1104"
        ],
        burden_holder="Contractor",
        adversary_position="Alternative processes may offer higher productivity.",
        counter_arguments=[
            "SMAW is proven and reliable for field welding.",
            "Regulatory codes mandate procedure qualification."
        ],
        resolution_strategy="Document procedure qualification and inspect welds per code.",
        entity_scope="Pipeline Construction",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1104 Section 5"
    ),
    DoctrineBlock(
        topic="Pipeline Welding Procedures: GMAW",
        keywords=["welding", "GMAW", "gas metal arc", "semi-automatic welding", "procedure"],
        conclusion_template="Gas Metal Arc Welding (GMAW) is a semi-automatic process used for pipeline welding, offering increased productivity.",
        reasoning_framework=(
            "GMAW is used for semi-automatic welding of pipelines, particularly in shop and controlled environments. "
            "The process offers higher productivity and consistent weld quality compared to manual methods. "
            "Procedure qualification is required, including WPS and PQR documentation. "
            "Disputes may arise over suitability for field conditions, resolved by referencing code requirements and procedure qualification. "
            "The burden of proof is on the contractor to demonstrate procedure qualification and weld quality. "
            "Counter arguments may cite limitations in field application, but GMAW is increasingly used for pipeline construction."
        ),
        key_factors=[
            "Welding process",
            "Procedure qualification",
            "Weld quality",
            "Productivity"
        ],
        primary_authority=[
            "ASME B31.4",
            "ASME B31.8",
            "API 1104"
        ],
        burden_holder="Contractor",
        adversary_position="GMAW may not be suitable for field conditions.",
        counter_arguments=[
            "Procedure qualification ensures suitability.",
            "GMAW offers higher productivity and quality."
        ],
        resolution_strategy="Qualify procedures and document weld quality.",
        entity_scope="Pipeline Construction",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1104 Section 6"
    ),
    DoctrineBlock(
        topic="Pipeline Coating: FBE",
        keywords=["coating", "FBE", "fusion bonded epoxy", "corrosion protection", "pipeline"],
        conclusion_template="Fusion Bonded Epoxy (FBE) coating is the industry standard for corrosion protection of pipelines.",
        reasoning_framework=(
            "FBE coating provides durable corrosion protection for steel pipelines, meeting industry and regulatory requirements. "
            "Application procedures must ensure proper surface preparation, coating thickness, and curing. "
            "Disputes may arise over coating quality and performance, resolved by referencing manufacturer specifications and inspection results. "
            "The burden of proof is on the contractor to document coating procedures and quality. "
            "Counter arguments may cite alternative coatings, but FBE remains the industry standard for most applications."
        ),
        key_factors=[
            "Coating thickness",
            "Surface preparation",
            "Curing",
            "Inspection"
        ],
        primary_authority=[
            "API RP 5L2",
            "ASME B31.4",
            "ASME B31.8"
        ],
        burden_holder="Contractor",
        adversary_position="Alternative coatings may offer improved performance.",
        counter_arguments=[
            "FBE is proven and widely used.",
            "Regulatory codes mandate coating quality."
        ],
        resolution_strategy="Document coating procedures and inspect per manufacturer specifications.",
        entity_scope="Pipeline Construction",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5L2 Section 4"
    ),
    DoctrineBlock(
        topic="Pipeline Coating: Three-Layer Polyethylene",
        keywords=["coating", "three-layer polyethylene", "corrosion protection", "pipeline", "external coating"],
        conclusion_template="Three-layer polyethylene coating offers enhanced corrosion protection and mechanical strength for pipelines.",
        reasoning_framework=(
            "Three-layer polyethylene coating consists of FBE primer, adhesive, and polyethylene topcoat, providing superior corrosion protection and mechanical strength. "
            "Application procedures must ensure proper layer adhesion and thickness. "
            "Disputes may arise over coating performance, resolved by referencing manufacturer specifications and inspection results. "
            "The burden of proof is on the contractor to document coating procedures and quality. "
            "Counter arguments may cite cost and complexity, but performance benefits justify use in harsh environments."
        ),
        key_factors=[
            "Layer adhesion",
            "Coating thickness",
            "Surface preparation",
            "Inspection"
        ],
        primary_authority=[
            "API RP 5L2",
            "ASME B31.4",
            "ASME B31.8"
        ],
        burden_holder="Contractor",
        adversary_position="Cost and complexity may outweigh benefits.",
        counter_arguments=[
            "Performance benefits justify use.",
            "Regulatory codes mandate coating quality."
        ],
        resolution_strategy="Document procedures and inspect per manufacturer specifications.",
        entity_scope="Pipeline Construction",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 5L2 Section 5"
    ),
    DoctrineBlock(
        topic="Pipeline Construction: ROW Clearing",
        keywords=["construction", "ROW", "right of way", "clearing", "environmental"],
        conclusion_template="Right of Way (ROW) clearing is a critical step in pipeline construction, requiring compliance with environmental and regulatory requirements.",
        reasoning_framework=(
            "ROW clearing involves removal of vegetation and obstacles to prepare for pipeline installation. "
            "Environmental impact assessments and permits are required. "
            "Procedures must minimize environmental disturbance and comply with regulatory requirements. "
            "Disputes may arise over environmental impact, resolved by referencing permits and mitigation plans. "
            "The burden of proof is on the contractor to document compliance and mitigation measures. "
            "Counter arguments may cite environmental risks, but proper planning and compliance mitigate impacts."
        ),
        key_factors=[
            "Environmental impact",
            "Permits",
            "Mitigation measures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "EPA",
            "Local permitting agencies"
        ],
        burden_holder="Contractor",
        adversary_position="Environmental risks may outweigh benefits.",
        counter_arguments=[
            "Mitigation measures reduce impact.",
            "Permits and compliance are mandatory."
        ],
        resolution_strategy="Document compliance and implement mitigation measures.",
        entity_scope="Pipeline Construction",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 200"
    ),
    DoctrineBlock(
        topic="Pipeline Construction: Trenching",
        keywords=["construction", "trenching", "excavation", "pipeline", "safety"],
        conclusion_template="Trenching must be performed in accordance with safety and environmental regulations.",
        reasoning_framework=(
            "Trenching involves excavation for pipeline installation. "
            "Safety procedures must be followed to prevent collapse and protect workers. "
            "Environmental impact must be minimized. "
            "Regulatory codes specify trench depth, width, and backfill requirements. "
            "Disputes may arise over safety and environmental compliance, resolved by referencing code requirements and inspection results. "
            "The burden of proof is on the contractor to document compliance and safety procedures. "
            "Counter arguments may cite alternative installation methods, but trenching remains standard for most pipelines."
        ),
        key_factors=[
            "Trench depth",
            "Safety procedures",
            "Environmental impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "OSHA",
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4"
        ],
        burden_holder="Contractor",
        adversary_position="Alternative methods may offer improved safety.",
        counter_arguments=[
            "Trenching is standard and proven.",
            "Safety procedures mitigate risks."
        ],
        resolution_strategy="Follow regulatory codes and document safety procedures.",
        entity_scope="Pipeline Construction",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1926 Subpart P"
    ),
    DoctrineBlock(
        topic="Pipeline Construction: Backfill",
        keywords=["construction", "backfill", "pipeline", "compaction", "safety"],
        conclusion_template="Backfill procedures must ensure proper compaction and protection of the pipeline.",
        reasoning_framework=(
            "Backfill involves placement and compaction of material around the pipeline to protect it and restore the ROW. "
            "Procedures must ensure proper compaction to prevent settlement and damage. "
            "Regulatory codes specify material requirements and compaction standards. "
            "Disputes may arise over backfill quality, resolved by referencing inspection results and code requirements. "
            "The burden of proof is on the contractor to document procedures and quality. "
            "Counter arguments may cite alternative materials, but code requirements prevail."
        ),
        key_factors=[
            "Material quality",
            "Compaction",
            "Pipeline protection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "Local permitting agencies"
        ],
        burden_holder="Contractor",
        adversary_position="Alternative materials may offer improved performance.",
        counter_arguments=[
            "Regulatory codes specify material requirements.",
            "Proper compaction prevents settlement."
        ],
        resolution_strategy="Document procedures and inspect per code requirements.",
        entity_scope="Pipeline Construction",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 434"
    ),
    DoctrineBlock(
        topic="Pipeline Construction: Horizontal Directional Drilling (HDD)",
        keywords=["construction", "HDD", "horizontal directional drilling", "bore crossing", "pipeline"],
        conclusion_template="Horizontal Directional Drilling (HDD) is used for pipeline crossings under obstacles, requiring specialized procedures and permits.",
        reasoning_framework=(
            "HDD is used for pipeline installation under rivers, roads, and other obstacles. "
            "Procedures must ensure proper bore alignment, pipe integrity, and environmental protection. "
            "Permits and environmental impact assessments are required. "
            "Disputes may arise over bore quality and environmental impact, resolved by referencing inspection results and permit requirements. "
            "The burden of proof is on the contractor to document procedures and compliance. "
            "Counter arguments may cite risks of bore collapse and environmental disturbance, but proper planning and procedures mitigate risks."
        ),
        key_factors=[
            "Bore alignment",
            "Pipe integrity",
            "Environmental impact",
            "Permits"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "EPA",
            "Local permitting agencies"
        ],
        burden_holder="Contractor",
        adversary_position="HDD may pose risks of bore collapse and environmental disturbance.",
        counter_arguments=[
            "Proper planning and procedures mitigate risks.",
            "Permits and compliance are mandatory."
        ],
        resolution_strategy="Document procedures and implement mitigation measures.",
        entity_scope="Pipeline Construction",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 200"
    ),
    DoctrineBlock(
        topic="Pipeline Pigging: Cleaning",
        keywords=["pigging", "cleaning", "pipeline", "maintenance", "debris removal"],
        conclusion_template="Cleaning pigging is essential for pipeline maintenance and integrity, removing debris and buildup.",
        reasoning_framework=(
            "Cleaning pigging involves running mechanical pigs through the pipeline to remove debris, scale, and buildup. "
            "Regular pigging maintains pipeline integrity and prevents corrosion. "
            "Procedures must ensure proper pig selection and operation. "
            "Disputes may arise over pigging frequency and effectiveness, resolved by referencing inspection results and maintenance records. "
            "The burden of proof is on the operator to document pigging procedures and results. "
            "Counter arguments may cite operational disruptions, but maintenance benefits outweigh drawbacks."
        ),
        key_factors=[
            "Pig selection",
            "Pigging frequency",
            "Debris removal",
            "Pipeline integrity"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Pigging may disrupt operations.",
        counter_arguments=[
            "Maintenance benefits outweigh disruptions.",
            "Regulatory codes mandate pipeline integrity."
        ],
        resolution_strategy="Document pigging procedures and schedule maintenance.",
        entity_scope="Pipeline Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 7"
    ),
    DoctrineBlock(
        topic="Pipeline Pigging: Gauging",
        keywords=["pigging", "gauging", "pipeline", "inspection", "internal diameter"],
        conclusion_template="Gauging pigging is used to assess internal diameter and detect deformations in pipelines.",
        reasoning_framework=(
            "Gauging pigs are run through pipelines to detect internal diameter changes and deformations. "
            "Procedures must ensure proper pig selection and data interpretation. "
            "Disputes may arise over pigging results, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in pig accuracy, but industry standards mandate gauging for integrity assessment."
        ),
        key_factors=[
            "Pig selection",
            "Data interpretation",
            "Pipeline integrity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Pigging accuracy may be limited.",
        counter_arguments=[
            "Industry standards mandate gauging.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 7"
    ),
    DoctrineBlock(
        topic="Pipeline Pigging: Intelligent Pigging",
        keywords=["pigging", "intelligent", "ILI", "inspection", "pipeline integrity"],
        conclusion_template="Intelligent pigging uses advanced tools to assess pipeline integrity, detecting corrosion, cracks, and other defects.",
        reasoning_framework=(
            "Intelligent pigging (ILI) employs advanced inspection tools (MFL, ultrasonic, caliper) to detect corrosion, cracks, and defects. "
            "Procedures must ensure proper tool selection, data interpretation, and follow-up actions. "
            "Regulatory codes mandate periodic ILI for pipeline integrity management. "
            "Disputes may arise over data accuracy and interpretation, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in tool accuracy, but industry standards mandate ILI for integrity assessment."
        ),
        key_factors=[
            "Tool selection",
            "Data interpretation",
            "Pipeline integrity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Tool accuracy may be limited.",
        counter_arguments=[
            "Industry standards mandate ILI.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 8"
    ),
    DoctrineBlock(
        topic="Inline Inspection (ILI): Magnetic Flux Leakage (MFL)",
        keywords=["ILI", "MFL", "inspection", "pipeline integrity", "corrosion detection"],
        conclusion_template="Magnetic Flux Leakage (MFL) is a standard ILI method for detecting corrosion and metal loss in pipelines.",
        reasoning_framework=(
            "MFL tools detect corrosion and metal loss by measuring magnetic field changes in the pipeline wall. "
            "Procedures must ensure proper tool calibration and data interpretation. "
            "Regulatory codes mandate periodic MFL inspection for pipeline integrity. "
            "Disputes may arise over data accuracy and interpretation, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in detection sensitivity, but MFL remains industry standard for corrosion detection."
        ),
        key_factors=[
            "Tool calibration",
            "Data interpretation",
            "Detection sensitivity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Detection sensitivity may be limited.",
        counter_arguments=[
            "MFL is proven for corrosion detection.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 8"
    ),
    DoctrineBlock(
        topic="Inline Inspection (ILI): Ultrasonic Testing",
        keywords=["ILI", "ultrasonic", "inspection", "pipeline integrity", "crack detection"],
        conclusion_template="Ultrasonic testing is a standard ILI method for detecting cracks and wall thickness changes in pipelines.",
        reasoning_framework=(
            "Ultrasonic tools detect cracks and wall thickness changes by measuring sound wave reflections in the pipeline wall. "
            "Procedures must ensure proper tool calibration and data interpretation. "
            "Regulatory codes mandate periodic ultrasonic inspection for pipeline integrity. "
            "Disputes may arise over data accuracy and interpretation, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in detection sensitivity, but ultrasonic testing remains industry standard for crack detection."
        ),
        key_factors=[
            "Tool calibration",
            "Data interpretation",
            "Detection sensitivity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Detection sensitivity may be limited.",
        counter_arguments=[
            "Ultrasonic testing is proven for crack detection.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 8"
    ),
    DoctrineBlock(
        topic="Inline Inspection (ILI): Caliper Pigging",
        keywords=["ILI", "caliper", "pigging", "inspection", "pipeline deformation"],
        conclusion_template="Caliper pigging is used to detect pipeline deformations and internal diameter changes.",
        reasoning_framework=(
            "Caliper pigs measure internal diameter and detect deformations such as dents and ovality. "
            "Procedures must ensure proper pig selection and data interpretation. "
            "Regulatory codes mandate periodic caliper inspection for pipeline integrity. "
            "Disputes may arise over data accuracy and interpretation, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in detection sensitivity, but caliper pigging remains industry standard for deformation detection."
        ),
        key_factors=[
            "Pig selection",
            "Data interpretation",
            "Detection sensitivity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Detection sensitivity may be limited.",
        counter_arguments=[
            "Caliper pigging is proven for deformation detection.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 8"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management: PIMS",
        keywords=["integrity management", "PIMS", "pipeline", "risk assessment", "maintenance"],
        conclusion_template="Pipeline Integrity Management Systems (PIMS) are required for risk assessment and maintenance planning.",
        reasoning_framework=(
            "PIMS involves systematic risk assessment, inspection, and maintenance planning for pipelines. "
            "Regulatory codes mandate implementation of PIMS for all operators. "
            "Procedures must ensure proper data collection, risk analysis, and documentation. "
            "Disputes may arise over risk assessment methodology, resolved by referencing code requirements and industry standards. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in risk models, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Risk assessment",
            "Inspection",
            "Maintenance planning",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Risk models may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Industry standards guide methodology."
        ],
        resolution_strategy="Document procedures and follow industry standards.",
        entity_scope="Pipeline Operations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 3"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management: API 1160",
        keywords=["integrity management", "API 1160", "pipeline", "risk assessment", "inspection"],
        conclusion_template="API 1160 is the controlling standard for pipeline integrity management, risk assessment, and inspection.",
        reasoning_framework=(
            "API 1160 provides guidelines for pipeline integrity management, including risk assessment, inspection, and maintenance. "
            "Regulatory codes reference API 1160 as the controlling standard. "
            "Procedures must ensure compliance with API 1160 requirements. "
            "Disputes may arise over interpretation of guidelines, resolved by referencing code requirements and industry standards. "
            "The burden of proof is on the operator to document compliance and procedures. "
            "Counter arguments may cite limitations in guidelines, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Risk assessment",
            "Inspection",
            "Maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API 1160",
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Guidelines may be open to interpretation.",
        counter_arguments=[
            "Regulatory codes reference API 1160.",
            "Industry standards guide methodology."
        ],
        resolution_strategy="Document compliance and follow API 1160 guidelines.",
        entity_scope="Pipeline Operations",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 1160 Section 2"
    ),
    DoctrineBlock(
        topic="Pipeline Stress Analysis: ASME B31.4",
        keywords=["stress analysis", "ASME B31.4", "pipeline", "design", "safety"],
        conclusion_template="ASME B31.4 is the controlling standard for pipeline stress analysis and design.",
        reasoning_framework=(
            "ASME B31.4 specifies requirements for pipeline stress analysis, including allowable stresses, load cases, and safety factors. "
            "Design must ensure compliance with allowable stress limits and account for internal pressure, external loads, and thermal effects. "
            "Disputes may arise over calculation methodology, resolved by referencing code requirements and documented analysis. "
            "The burden of proof is on the designer to document compliance and calculations. "
            "Counter arguments may cite alternative standards, but ASME B31.4 is controlling for liquid pipelines."
        ),
        key_factors=[
            "Allowable stress",
            "Load cases",
            "Safety factors",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 5L"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Alternative standards may be applicable.",
        counter_arguments=[
            "ASME B31.4 is controlling for liquid pipelines.",
            "Documented analysis ensures compliance."
        ],
        resolution_strategy="Document calculations and follow ASME B31.4 requirements.",
        entity_scope="Pipeline Engineering",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 402"
    ),
    DoctrineBlock(
        topic="Pipeline Stress Analysis: ASME B31.8",
        keywords=["stress analysis", "ASME B31.8", "pipeline", "design", "safety"],
        conclusion_template="ASME B31.8 is the controlling standard for pipeline stress analysis and design for gas pipelines.",
        reasoning_framework=(
            "ASME B31.8 specifies requirements for pipeline stress analysis, including allowable stresses, load cases, and safety factors for gas pipelines. "
            "Design must ensure compliance with allowable stress limits and account for internal pressure, external loads, and thermal effects. "
            "Disputes may arise over calculation methodology, resolved by referencing code requirements and documented analysis. "
            "The burden of proof is on the designer to document compliance and calculations. "
            "Counter arguments may cite alternative standards, but ASME B31.8 is controlling for gas pipelines."
        ),
        key_factors=[
            "Allowable stress",
            "Load cases",
            "Safety factors",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.8",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 5L"
        ],
        burden_holder="Pipeline Designer",
        adversary_position="Alternative standards may be applicable.",
        counter_arguments=[
            "ASME B31.8 is controlling for gas pipelines.",
            "Documented analysis ensures compliance."
        ],
        resolution_strategy="Document calculations and follow ASME B31.8 requirements.",
        entity_scope="Pipeline Engineering",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.8 Section 802"
    ),
    DoctrineBlock(
        topic="Pipeline Cathodic Protection: CP Survey",
        keywords=["cathodic protection", "CP survey", "pipeline", "corrosion", "inspection"],
        conclusion_template="Cathodic Protection (CP) surveys are required to assess pipeline corrosion protection effectiveness.",
        reasoning_framework=(
            "CP surveys measure pipe-to-soil potential to assess effectiveness of corrosion protection systems. "
            "Procedures must ensure proper data collection and interpretation. "
            "Regulatory codes mandate periodic CP surveys for all pipelines. "
            "Disputes may arise over survey results and interpretation, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in survey accuracy, but industry standards mandate CP surveys."
        ),
        key_factors=[
            "Data collection",
            "Potential measurement",
            "Corrosion protection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160",
            "NACE SP0169"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Survey accuracy may be limited.",
        counter_arguments=[
            "Industry standards mandate CP surveys.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0169 Section 5"
    ),
    DoctrineBlock(
        topic="Pipeline Cathodic Protection: CIPS",
        keywords=["cathodic protection", "CIPS", "close interval potential survey", "pipeline", "corrosion"],
        conclusion_template="Close Interval Potential Surveys (CIPS) provide detailed assessment of cathodic protection effectiveness.",
        reasoning_framework=(
            "CIPS involves measuring pipe-to-soil potential at close intervals along the pipeline to detect corrosion risks. "
            "Procedures must ensure proper data collection and interpretation. "
            "Regulatory codes mandate periodic CIPS for high-risk pipelines. "
            "Disputes may arise over survey results and interpretation, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in survey accuracy, but CIPS provides detailed assessment of corrosion protection."
        ),
        key_factors=[
            "Data collection",
            "Potential measurement",
            "Corrosion protection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160",
            "NACE SP0169"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Survey accuracy may be limited.",
        counter_arguments=[
            "CIPS provides detailed assessment.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0169 Section 6"
    ),
    DoctrineBlock(
        topic="Pipeline Cathodic Protection: DCVG",
        keywords=["cathodic protection", "DCVG", "direct current voltage gradient", "pipeline", "coating defect"],
        conclusion_template="Direct Current Voltage Gradient (DCVG) surveys detect coating defects and assess cathodic protection effectiveness.",
        reasoning_framework=(
            "DCVG surveys measure voltage gradients to detect coating defects and assess cathodic protection effectiveness. "
            "Procedures must ensure proper data collection and interpretation. "
            "Regulatory codes mandate periodic DCVG surveys for pipelines with known coating defects. "
            "Disputes may arise over survey results and interpretation, resolved by referencing inspection records and code requirements. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in survey accuracy, but DCVG provides targeted assessment of coating integrity."
        ),
        key_factors=[
            "Data collection",
            "Voltage gradient measurement",
            "Coating integrity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160",
            "NACE SP0169"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Survey accuracy may be limited.",
        counter_arguments=[
            "DCVG provides targeted assessment.",
            "Inspection records validate results."
        ],
        resolution_strategy="Document procedures and interpret results per code.",
        entity_scope="Pipeline Operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0169 Section 7"
    ),
    DoctrineBlock(
        topic="Pipeline SCADA: Leak Detection",
        keywords=["SCADA", "leak detection", "pipeline", "monitoring", "safety"],
        conclusion_template="SCADA systems must include leak detection capabilities to ensure pipeline safety and regulatory compliance.",
        reasoning_framework=(
            "SCADA systems monitor pipeline operations and must include leak detection algorithms. "
            "Regulatory codes mandate leak detection for all pipelines. "
            "Procedures must ensure proper system configuration and alarm management. "
            "Disputes may arise over system accuracy and response, resolved by referencing code requirements and system documentation. "
            "The burden of proof is on the operator to document system configuration and response procedures. "
            "Counter arguments may cite limitations in detection sensitivity, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "System configuration",
            "Detection sensitivity",
            "Alarm management",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Detection sensitivity may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "System documentation ensures accuracy."
        ],
        resolution_strategy="Document system configuration and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 452"
    ),
    DoctrineBlock(
        topic="Pipeline SCADA: Computational Pipeline Monitoring (CPM)",
        keywords=["SCADA", "CPM", "computational pipeline monitoring", "pipeline", "leak detection"],
        conclusion_template="Computational Pipeline Monitoring (CPM) is required for advanced leak detection and operational control.",
        reasoning_framework=(
            "CPM uses mathematical models to detect leaks and monitor pipeline operations in real time. "
            "Regulatory codes mandate CPM for high-risk pipelines. "
            "Procedures must ensure proper model calibration and alarm management. "
            "Disputes may arise over model accuracy and response, resolved by referencing code requirements and system documentation. "
            "The burden of proof is on the operator to document model calibration and response procedures. "
            "Counter arguments may cite limitations in model sensitivity, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Model calibration",
            "Detection sensitivity",
            "Alarm management",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Model sensitivity may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "System documentation ensures accuracy."
        ],
        resolution_strategy="Document model calibration and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 452"
    ),
    DoctrineBlock(
        topic="Pipeline SCADA: Real-Time Transient Model (RTTM)",
        keywords=["SCADA", "RTTM", "real-time transient model", "pipeline", "leak detection"],
        conclusion_template="Real-Time Transient Model (RTTM) is used for advanced leak detection in SCADA systems.",
        reasoning_framework=(
            "RTTM uses real-time data and transient flow models to detect leaks and monitor pipeline operations. "
            "Regulatory codes mandate RTTM for high-risk pipelines. "
            "Procedures must ensure proper model calibration and alarm management. "
            "Disputes may arise over model accuracy and response, resolved by referencing code requirements and system documentation. "
            "The burden of proof is on the operator to document model calibration and response procedures. "
            "Counter arguments may cite limitations in model sensitivity, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Model calibration",
            "Detection sensitivity",
            "Alarm management",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Model sensitivity may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "System documentation ensures accuracy."
        ],
        resolution_strategy="Document model calibration and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 452"
    ),
    DoctrineBlock(
        topic="Pipeline Right of Way Acquisition: Easement",
        keywords=["ROW", "easement", "right of way", "pipeline", "land acquisition"],
        conclusion_template="Easement agreements are required for pipeline right of way acquisition, ensuring legal access and compliance.",
        reasoning_framework=(
            "Easement agreements grant legal access for pipeline installation and maintenance. "
            "Procedures must ensure proper negotiation, documentation, and compliance with local laws. "
            "Disputes may arise over terms and compensation, resolved by referencing legal requirements and precedent. "
            "The burden of proof is on the operator to document agreements and compliance. "
            "Counter arguments may cite landowner rights, but legal agreements ensure access and compliance."
        ),
        key_factors=[
            "Negotiation",
            "Documentation",
            "Legal compliance",
            "Compensation"
        ],
        primary_authority=[
            "Local property laws",
            "PHMSA CFR 49 Parts 192 & 195",
            "EPA"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Landowner rights may limit access.",
        counter_arguments=[
            "Legal agreements ensure access.",
            "Compensation resolves disputes."
        ],
        resolution_strategy="Document agreements and follow legal requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 200"
    ),
    DoctrineBlock(
        topic="Pipeline Regulatory Compliance: PHMSA CFR 49 Parts 192 & 195",
        keywords=["regulatory compliance", "PHMSA", "CFR 49", "pipeline", "safety"],
        conclusion_template="PHMSA CFR 49 Parts 192 & 195 are the controlling regulations for pipeline safety and compliance.",
        reasoning_framework=(
            "PHMSA CFR 49 Parts 192 & 195 specify requirements for pipeline safety, design, construction, operation, and maintenance. "
            "Compliance is mandatory for all operators. "
            "Procedures must ensure proper documentation and adherence to regulatory requirements. "
            "Disputes may arise over interpretation of regulations, resolved by referencing code requirements and legal precedent. "
            "The burden of proof is on the operator to document compliance and procedures. "
            "Counter arguments may cite limitations in regulations, but compliance is mandatory."
        ),
        key_factors=[
            "Safety",
            "Design",
            "Construction",
            "Operation",
            "Maintenance",
            "Documentation"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "API 1160",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Regulations may be open to interpretation.",
        counter_arguments=[
            "Compliance is mandatory.",
            "Legal precedent guides interpretation."
        ],
        resolution_strategy="Document compliance and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Parts 192 & 195"
    ),
    DoctrineBlock(
        topic="Pipeline Hydrostatic Testing: Strength Test",
        keywords=["hydrostatic testing", "strength test", "pipeline", "pressure", "integrity"],
        conclusion_template="Hydrostatic strength testing is required to verify pipeline integrity and pressure rating.",
        reasoning_framework=(
            "Hydrostatic strength testing involves pressurizing the pipeline above its maximum operating pressure to verify integrity. "
            "Regulatory codes specify test pressure, duration, and acceptance criteria. "
            "Procedures must ensure proper test documentation and safety measures. "
            "Disputes may arise over test results and acceptance, resolved by referencing code requirements and test records. "
            "The burden of proof is on the operator to document test procedures and results. "
            "Counter arguments may cite risks of over-pressurization, but proper procedures mitigate risks."
        ),
        key_factors=[
            "Test pressure",
            "Duration",
            "Acceptance criteria",
            "Safety measures"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4",
            "API 5L"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Over-pressurization may damage pipeline.",
        counter_arguments=[
            "Proper procedures mitigate risks.",
            "Regulatory codes specify test requirements."
        ],
        resolution_strategy="Document procedures and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 302"
    ),
    DoctrineBlock(
        topic="Pipeline Hydrostatic Testing: Leak Test",
        keywords=["hydrostatic testing", "leak test", "pipeline", "pressure", "integrity"],
        conclusion_template="Hydrostatic leak testing is required to verify pipeline tightness and detect leaks.",
        reasoning_framework=(
            "Hydrostatic leak testing involves pressurizing the pipeline and monitoring for pressure loss to detect leaks. "
            "Regulatory codes specify test pressure, duration, and acceptance criteria. "
            "Procedures must ensure proper test documentation and safety measures. "
            "Disputes may arise over test results and acceptance, resolved by referencing code requirements and test records. "
            "The burden of proof is on the operator to document test procedures and results. "
            "Counter arguments may cite limitations in leak detection sensitivity, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Test pressure",
            "Duration",
            "Acceptance criteria",
            "Leak detection sensitivity"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "ASME B31.4",
            "API 5L"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Leak detection sensitivity may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Test records validate results."
        ],
        resolution_strategy="Document procedures and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 302"
    ),
    DoctrineBlock(
        topic="Compressor Station: Centrifugal Compressor",
        keywords=["compressor station", "centrifugal compressor", "pipeline", "gas", "operation"],
        conclusion_template="Centrifugal compressors are standard for gas pipeline stations, offering reliable and efficient operation.",
        reasoning_framework=(
            "Centrifugal compressors are widely used for gas pipeline stations due to their reliability and efficiency. "
            "Procedures must ensure proper selection, operation, and maintenance. "
            "Regulatory codes specify performance and safety requirements. "
            "Disputes may arise over compressor selection and performance, resolved by referencing manufacturer specifications and code requirements. "
            "The burden of proof is on the operator to document selection and maintenance procedures. "
            "Counter arguments may cite alternative compressor types, but centrifugal compressors remain industry standard."
        ),
        key_factors=[
            "Compressor selection",
            "Performance",
            "Maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.8",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 618"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Alternative compressor types may offer improved performance.",
        counter_arguments=[
            "Centrifugal compressors are proven and reliable.",
            "Regulatory codes specify requirements."
        ],
        resolution_strategy="Document selection and follow manufacturer specifications.",
        entity_scope="Pipeline Operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 618 Section 4"
    ),
    DoctrineBlock(
        topic="Compressor Station: Reciprocating Compressor",
        keywords=["compressor station", "reciprocating compressor", "pipeline", "gas", "operation"],
        conclusion_template="Reciprocating compressors are used for gas pipeline stations requiring variable flow and high pressure.",
        reasoning_framework=(
            "Reciprocating compressors are used for gas pipeline stations requiring variable flow and high pressure. "
            "Procedures must ensure proper selection, operation, and maintenance. "
            "Regulatory codes specify performance and safety requirements. "
            "Disputes may arise over compressor selection and performance, resolved by referencing manufacturer specifications and code requirements. "
            "The burden of proof is on the operator to document selection and maintenance procedures. "
            "Counter arguments may cite alternative compressor types, but reciprocating compressors offer flexibility for specific applications."
        ),
        key_factors=[
            "Compressor selection",
            "Performance",
            "Maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.8",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 618"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Alternative compressor types may offer improved performance.",
        counter_arguments=[
            "Reciprocating compressors offer flexibility.",
            "Regulatory codes specify requirements."
        ],
        resolution_strategy="Document selection and follow manufacturer specifications.",
        entity_scope="Pipeline Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 618 Section 5"
    ),
    DoctrineBlock(
        topic="Pump Station: Centrifugal Pump",
        keywords=["pump station", "centrifugal pump", "pipeline", "liquid", "operation"],
        conclusion_template="Centrifugal pumps are standard for liquid pipeline stations, offering reliable and efficient operation.",
        reasoning_framework=(
            "Centrifugal pumps are widely used for liquid pipeline stations due to their reliability and efficiency. "
            "Procedures must ensure proper selection, operation, and maintenance. "
            "Regulatory codes specify performance and safety requirements. "
            "Disputes may arise over pump selection and performance, resolved by referencing manufacturer specifications and code requirements. "
            "The burden of proof is on the operator to document selection and maintenance procedures. "
            "Counter arguments may cite alternative pump types, but centrifugal pumps remain industry standard."
        ),
        key_factors=[
            "Pump selection",
            "Performance",
            "Maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 610"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Alternative pump types may offer improved performance.",
        counter_arguments=[
            "Centrifugal pumps are proven and reliable.",
            "Regulatory codes specify requirements."
        ],
        resolution_strategy="Document selection and follow manufacturer specifications.",
        entity_scope="Pipeline Operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 610 Section 4"
    ),
    DoctrineBlock(
        topic="Pump Station: Positive Displacement Pump",
        keywords=["pump station", "positive displacement pump", "pipeline", "liquid", "operation"],
        conclusion_template="Positive displacement pumps are used for liquid pipeline stations requiring variable flow and high pressure.",
        reasoning_framework=(
            "Positive displacement pumps are used for liquid pipeline stations requiring variable flow and high pressure. "
            "Procedures must ensure proper selection, operation, and maintenance. "
            "Regulatory codes specify performance and safety requirements. "
            "Disputes may arise over pump selection and performance, resolved by referencing manufacturer specifications and code requirements. "
            "The burden of proof is on the operator to document selection and maintenance procedures. "
            "Counter arguments may cite alternative pump types, but positive displacement pumps offer flexibility for specific applications."
        ),
        key_factors=[
            "Pump selection",
            "Performance",
            "Maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 674"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Alternative pump types may offer improved performance.",
        counter_arguments=[
            "Positive displacement pumps offer flexibility.",
            "Regulatory codes specify requirements."
        ],
        resolution_strategy="Document selection and follow manufacturer specifications.",
        entity_scope="Pipeline Operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 674 Section 5"
    ),
    DoctrineBlock(
        topic="Pipeline Flow Assurance: Hydrate Management",
        keywords=["flow assurance", "hydrate", "pipeline", "gas", "management"],
        conclusion_template="Hydrate management is required for gas pipelines to prevent blockages and ensure flow assurance.",
        reasoning_framework=(
            "Hydrate formation can block gas pipelines, requiring management strategies such as dehydration, heating, and chemical injection. "
            "Procedures must ensure proper monitoring and mitigation. "
            "Regulatory codes mandate flow assurance for gas pipelines. "
            "Disputes may arise over management strategies, resolved by referencing code requirements and operational experience. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in mitigation effectiveness, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Monitoring",
            "Mitigation",
            "Chemical injection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.8",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 17A"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Mitigation effectiveness may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Operational experience guides strategy."
        ],
        resolution_strategy="Document procedures and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 17A Section 6"
    ),
    DoctrineBlock(
        topic="Pipeline Flow Assurance: Wax Management",
        keywords=["flow assurance", "wax", "pipeline", "crude oil", "management"],
        conclusion_template="Wax management is required for crude oil pipelines to prevent blockages and ensure flow assurance.",
        reasoning_framework=(
            "Wax deposition can block crude oil pipelines, requiring management strategies such as heating, pigging, and chemical injection. "
            "Procedures must ensure proper monitoring and mitigation. "
            "Regulatory codes mandate flow assurance for crude oil pipelines. "
            "Disputes may arise over management strategies, resolved by referencing code requirements and operational experience. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in mitigation effectiveness, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Monitoring",
            "Mitigation",
            "Pigging",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 17A"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Mitigation effectiveness may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Operational experience guides strategy."
        ],
        resolution_strategy="Document procedures and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 17A Section 7"
    ),
    DoctrineBlock(
        topic="Pipeline Flow Assurance: Asphaltene Management",
        keywords=["flow assurance", "asphaltene", "pipeline", "crude oil", "management"],
        conclusion_template="Asphaltene management is required for crude oil pipelines to prevent blockages and ensure flow assurance.",
        reasoning_framework=(
            "Asphaltene deposition can block crude oil pipelines, requiring management strategies such as chemical injection and pigging. "
            "Procedures must ensure proper monitoring and mitigation. "
            "Regulatory codes mandate flow assurance for crude oil pipelines. "
            "Disputes may arise over management strategies, resolved by referencing code requirements and operational experience. "
            "The burden of proof is on the operator to document procedures and results. "
            "Counter arguments may cite limitations in mitigation effectiveness, but regulatory compliance is mandatory."
        ),
        key_factors=[
            "Monitoring",
            "Mitigation",
            "Chemical injection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.4",
            "PHMSA CFR 49 Parts 192 & 195",
            "API 17A"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Mitigation effectiveness may be limited.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Operational experience guides strategy."
        ],
        resolution_strategy="Document procedures and follow regulatory requirements.",
        entity_scope="Pipeline Operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 17A Section 8"
    ),
    DoctrineBlock(
        topic="Pipeline Decommissioning: Abandonment",
        keywords=["decommissioning", "abandonment", "pipeline", "regulatory compliance", "environmental"],
        conclusion_template="Pipeline abandonment must be performed in accordance with regulatory and environmental requirements.",
        reasoning_framework=(
            "Pipeline abandonment involves removal or permanent deactivation of pipelines. "
            "Regulatory codes specify procedures for abandonment, including environmental impact assessments and documentation. "
            "Procedures must ensure proper deactivation and mitigation of environmental risks. "
            "Disputes may arise over abandonment procedures and environmental impact, resolved by referencing code requirements and mitigation plans. "
            "The burden of proof is on the operator to document procedures and compliance. "
            "Counter arguments may cite environmental risks, but proper planning and compliance mitigate impacts."
        ),
        key_factors=[
            "Deactivation",
            "Environmental impact",
            "Documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "PHMSA CFR 49 Parts 192 & 195",
            "EPA",
            "ASME B31.4"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Environmental risks may outweigh benefits.",
        counter_arguments=[
            "Mitigation measures reduce impact.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Document procedures and implement mitigation measures.",
        entity_scope="Pipeline Operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="PHMSA CFR 49 Part 195 Section 402"
    ),
    DoctrineBlock(
        topic="Pipeline Decommissioning: Purging",
        keywords=["decommissioning", "purging", "pipeline", "safety", "regulatory compliance"],
        conclusion_template="Pipeline purging is required during decommissioning to ensure safety and prevent environmental risks.",
        reasoning_framework=(
            "Pipeline purging involves removal of hydrocarbons and gases prior to abandonment or deactivation. "
            "Regulatory codes specify procedures for purging, including safety measures and documentation. "
            "Procedures must ensure proper purging and mitigation of environmental risks. "
            "Disputes may arise over purging procedures and effectiveness, resolved by referencing code requirements and inspection results. "
            "The burden of proof is on the operator to document procedures and compliance. "
            "Counter arguments may