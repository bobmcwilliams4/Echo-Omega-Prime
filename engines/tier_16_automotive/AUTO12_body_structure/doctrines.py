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
        topic="body_in_white_design_principles",
        keywords=["body-in-white", "design", "structure", "stiffness", "manufacturing"],
        conclusion_template="Body-in-white design must prioritize structural integrity, manufacturability, and cost efficiency.",
        reasoning_framework=(
            "Body-in-white (BIW) design is foundational to vehicle safety, NVH, and manufacturing efficiency. "
            "The framework involves evaluating load paths, optimizing joint placement, and balancing material selection "
            "with manufacturing constraints. BIW must provide sufficient torsional and bending stiffness to support "
            "crashworthiness and ride quality. Key considerations include minimizing weight while maintaining rigidity, "
            "ensuring accessibility for joining methods, and integrating corrosion protection strategies. "
            "Designs should be validated through CAE simulations and physical testing. Trade-offs between cost, "
            "performance, and manufacturability are resolved through iterative design reviews and benchmarking against "
            "industry standards. Material selection (e.g., AHSS, aluminum) is guided by performance targets and joining compatibility. "
            "The BIW must also accommodate packaging requirements for powertrain, suspension, and occupant safety systems. "
            "Final approval is contingent upon compliance with regulatory crash and durability standards."
        ),
        key_factors=[
            "Structural stiffness",
            "Crashworthiness",
            "Manufacturability",
            "Material selection",
            "Corrosion protection",
            "NVH performance",
            "Weight optimization"
        ],
        primary_authority=[
            "Euro NCAP",
            "SAE J2340",
            "OEM engineering standards"
        ],
        burden_holder="Design engineering team",
        adversary_position="Cost reduction advocates may argue for less expensive materials or simplified structures.",
        counter_arguments=[
            "Reduced material cost may compromise safety and durability.",
            "Simplified structures can lead to NVH and crash performance issues."
        ],
        resolution_strategy="Balance cost with performance through iterative optimization and benchmarking.",
        entity_scope="AUTO12 body structure engineering",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2340: Advanced High Strength Steel Standard"
    ),
    DoctrineBlock(
        topic="frontal_crash_structure_design",
        keywords=["frontal crash", "energy absorption", "crumple zone", "load path", "impact"],
        conclusion_template="Frontal crash structure must maximize energy absorption and maintain occupant survival space.",
        reasoning_framework=(
            "Frontal crash structure design is governed by principles of controlled deformation and energy management. "
            "The primary objective is to absorb impact energy through progressive crumple zones while maintaining the integrity "
            "of the passenger compartment. Load paths are engineered to direct forces away from occupants, utilizing tailored blanks, "
            "reinforcements, and high-strength materials. The design process includes simulation of various crash scenarios, "
            "validation against FMVSS 208 and Euro NCAP frontal impact standards, and physical testing. The structure must also "
            "accommodate packaging constraints for powertrain and accessories. Trade-offs involve balancing weight, manufacturability, "
            "and cost with crash performance. Adversaries may advocate for lighter or cheaper materials, but these must be evaluated "
            "against safety requirements. Final resolution is achieved through compliance testing and iterative design refinement."
        ),
        key_factors=[
            "Energy absorption",
            "Load path optimization",
            "Crumple zone effectiveness",
            "Material selection",
            "Passenger compartment integrity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 208",
            "Euro NCAP",
            "OEM crash test data"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Weight reduction advocates may propose thinner materials or less reinforcement.",
        counter_arguments=[
            "Reduced reinforcement may compromise occupant safety.",
            "Thinner materials may fail regulatory crash tests."
        ],
        resolution_strategy="Validate through simulation and physical crash testing; prioritize occupant safety.",
        entity_scope="AUTO12 frontal structure engineering",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 208: Occupant Crash Protection"
    ),
    DoctrineBlock(
        topic="side_impact_structure_design",
        keywords=["side impact", "intrusion", "energy absorption", "door beam", "B-pillar"],
        conclusion_template="Side impact structure must minimize intrusion and protect occupants through reinforced load paths.",
        reasoning_framework=(
            "Side impact structure design focuses on minimizing intrusion into the passenger compartment and absorbing impact energy. "
            "Key elements include reinforced B-pillars, door beams, and cross-members, often constructed from advanced high-strength steel. "
            "Designs are validated against FMVSS 214 and Euro NCAP side impact protocols. Simulation and physical testing are used to "
            "assess deformation, intrusion, and injury metrics. Trade-offs involve balancing weight and cost with reinforcement levels. "
            "Adversaries may argue for reduced reinforcement to save weight, but safety requirements take precedence. Resolution is achieved "
            "through compliance testing and iterative design optimization."
        ),
        key_factors=[
            "Intrusion minimization",
            "Energy absorption",
            "Reinforcement placement",
            "Material selection",
            "Passenger protection",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 214",
            "Euro NCAP",
            "OEM side impact test data"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Weight reduction advocates may propose less reinforcement.",
        counter_arguments=[
            "Reduced reinforcement increases risk of occupant injury.",
            "May fail regulatory side impact tests."
        ],
        resolution_strategy="Prioritize occupant protection and regulatory compliance; optimize reinforcement placement.",
        entity_scope="AUTO12 side structure engineering",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 214: Side Impact Protection"
    ),
    DoctrineBlock(
        topic="roof_crush_and_rollover_protection",
        keywords=["roof crush", "rollover", "strength", "A-pillar", "roof rail"],
        conclusion_template="Roof structure must withstand rollover loads and prevent excessive deformation.",
        reasoning_framework=(
            "Roof crush and rollover protection require the roof structure to resist deformation under extreme loads. "
            "Key components include reinforced A-pillars, roof rails, and cross-members, typically made from ultra-high-strength steel. "
            "Designs are validated against FMVSS 216 and IIHS roof strength tests. Simulation and physical testing assess load capacity "
            "and deformation. Trade-offs involve balancing weight, visibility, and cost with reinforcement levels. Adversaries may argue "
            "for thinner pillars to improve visibility, but safety requirements are paramount. Resolution is achieved through compliance testing "
            "and design optimization."
        ),
        key_factors=[
            "Roof strength",
            "Rollover protection",
            "A-pillar reinforcement",
            "Material selection",
            "Passenger safety",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FMVSS 216",
            "IIHS",
            "OEM roof strength test data"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Visibility advocates may propose thinner pillars.",
        counter_arguments=[
            "Thinner pillars may compromise roof strength.",
            "May fail rollover protection tests."
        ],
        resolution_strategy="Optimize pillar geometry for both strength and visibility; validate through testing.",
        entity_scope="AUTO12 roof structure engineering",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 216: Roof Crush Resistance"
    ),
    DoctrineBlock(
        topic="corrosion_protection_strategies",
        keywords=["corrosion", "protection", "coating", "electrogalvanizing", "sealing"],
        conclusion_template="Corrosion protection must ensure long-term durability through coatings, sealing, and material selection.",
        reasoning_framework=(
            "Corrosion protection strategies involve the application of coatings, sealants, and material selection to prevent degradation. "
            "Electrogalvanized steel, e-coat, and seam sealing are standard practices. The framework includes evaluating environmental exposure, "
            "salt spray testing, and field performance data. Trade-offs involve balancing cost and process complexity with durability. "
            "Adversaries may argue for reduced coating thickness or elimination of certain processes, but long-term warranty and customer satisfaction "
            "are critical. Resolution is achieved through benchmarking, testing, and adherence to OEM durability standards."
        ),
        key_factors=[
            "Coating effectiveness",
            "Material selection",
            "Sealing quality",
            "Environmental exposure",
            "Durability",
            "Warranty requirements"
        ],
        primary_authority=[
            "OEM corrosion standards",
            "ASTM B117",
            "SAE J2334"
        ],
        burden_holder="Materials engineering team",
        adversary_position="Cost reduction advocates may propose thinner coatings or fewer processes.",
        counter_arguments=[
            "Reduced protection increases risk of premature corrosion.",
            "May lead to warranty claims and customer dissatisfaction."
        ],
        resolution_strategy="Benchmark against industry standards; validate through accelerated corrosion testing.",
        entity_scope="AUTO12 body structure durability",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM B117: Salt Spray Test Standard"
    ),
    DoctrineBlock(
        topic="nvh_body_structure_contribution",
        keywords=["NVH", "noise", "vibration", "harshness", "body structure"],
        conclusion_template="Body structure must minimize NVH through optimized geometry, materials, and joining methods.",
        reasoning_framework=(
            "NVH (Noise, Vibration, Harshness) performance is influenced by body structure geometry, material selection, and joining methods. "
            "The framework involves identifying vibration sources, optimizing load paths, and using damping materials and structural adhesives. "
            "Simulation and physical testing (modal analysis, acoustic measurements) are used to validate performance. Trade-offs involve balancing "
            "weight, cost, and manufacturability with NVH targets. Adversaries may argue for cost reduction by eliminating damping materials, but "
            "customer satisfaction and competitive benchmarks are critical. Resolution is achieved through iterative design and testing."
        ),
        key_factors=[
            "Structural stiffness",
            "Damping materials",
            "Joining methods",
            "Geometry optimization",
            "NVH target achievement"
        ],
        primary_authority=[
            "OEM NVH standards",
            "SAE J1400",
            "Benchmarking data"
        ],
        burden_holder="NVH engineering team",
        adversary_position="Cost reduction advocates may propose eliminating damping materials.",
        counter_arguments=[
            "Reduced damping increases cabin noise and vibration.",
            "May compromise customer satisfaction and competitive positioning."
        ],
        resolution_strategy="Iterative design and testing; prioritize NVH targets within cost constraints.",
        entity_scope="AUTO12 NVH engineering",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J1400: NVH Measurement Standard"
    ),
    DoctrineBlock(
        topic="aerodynamic_body_optimization",
        keywords=["aerodynamics", "drag", "body structure", "fuel efficiency", "wind tunnel"],
        conclusion_template="Body structure must be optimized for aerodynamics to reduce drag and improve efficiency.",
        reasoning_framework=(
            "Aerodynamic optimization involves shaping the body structure to minimize drag and turbulence. The framework includes wind tunnel testing, "
            "CFD simulations, and benchmarking against competitive vehicles. Key factors include surface smoothness, panel fit, and integration of aerodynamic "
            "features (e.g., underbody panels, spoilers). Trade-offs involve balancing styling, manufacturing complexity, and cost with aerodynamic targets. "
            "Adversaries may argue for simplified shapes to reduce tooling costs, but efficiency and regulatory targets must be met. Resolution is achieved "
            "through iterative design, simulation, and validation."
        ),
        key_factors=[
            "Drag coefficient",
            "Surface smoothness",
            "Panel fit",
            "Aerodynamic features",
            "Fuel efficiency"
        ],
        primary_authority=[
            "OEM aerodynamic standards",
            "SAE J2082",
            "Wind tunnel test data"
        ],
        burden_holder="Aerodynamics engineering team",
        adversary_position="Styling and manufacturing advocates may propose simplified shapes.",
        counter_arguments=[
            "Simplified shapes may increase drag and reduce efficiency.",
            "May fail to meet regulatory fuel economy targets."
        ],
        resolution_strategy="Iterative optimization; validate through wind tunnel testing and CFD.",
        entity_scope="AUTO12 aerodynamic engineering",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2082: Aerodynamic Testing Standard"
    ),
    DoctrineBlock(
        topic="structural_durability_and_fatigue",
        keywords=["durability", "fatigue", "body structure", "life cycle", "testing"],
        conclusion_template="Body structure must be designed for durability and fatigue resistance over the vehicle life cycle.",
        reasoning_framework=(
            "Structural durability and fatigue resistance are achieved through material selection, geometry optimization, and joining method reliability. "
            "The framework includes CAE fatigue analysis, accelerated durability testing, and field data evaluation. Key factors are load spectrum, stress concentration, "
            "and environmental exposure. Trade-offs involve balancing weight, cost, and manufacturing complexity with durability targets. Adversaries may argue for "
            "cost reduction by eliminating reinforcements, but long-term reliability and warranty requirements are critical. Resolution is achieved through iterative "
            "design, testing, and benchmarking."
        ),
        key_factors=[
            "Material fatigue properties",
            "Geometry optimization",
            "Joining reliability",
            "Load spectrum",
            "Environmental exposure"
        ],
        primary_authority=[
            "OEM durability standards",
            "SAE J1099",
            "Field performance data"
        ],
        burden_holder="Durability engineering team",
        adversary_position="Cost reduction advocates may propose eliminating reinforcements.",
        counter_arguments=[
            "Eliminating reinforcements increases risk of fatigue failure.",
            "May lead to warranty claims and customer dissatisfaction."
        ],
        resolution_strategy="Validate through CAE and physical durability testing; prioritize reliability.",
        entity_scope="AUTO12 durability engineering",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J1099: Fatigue Testing Standard"
    ),
    DoctrineBlock(
        topic="advanced_high_strength_steel_selection",
        keywords=["AHSS", "steel", "material selection", "body structure", "performance"],
        conclusion_template="Advanced high-strength steel must be selected based on performance, manufacturability, and cost.",
        reasoning_framework=(
            "Advanced high-strength steel (AHSS) selection is guided by performance targets, manufacturability, and cost constraints. "
            "The framework includes evaluating mechanical properties, joining compatibility, and forming limits. Key factors are crash performance, "
            "weight reduction, and corrosion resistance. Trade-offs involve balancing cost and process complexity with performance. Adversaries may argue "
            "for less expensive materials, but safety and durability requirements are paramount. Resolution is achieved through benchmarking, testing, "
            "and adherence to OEM material standards."
        ),
        key_factors=[
            "Mechanical properties",
            "Joining compatibility",
            "Forming limits",
            "Crash performance",
            "Corrosion resistance"
        ],
        primary_authority=[
            "OEM material standards",
            "SAE J2340",
            "Supplier data"
        ],
        burden_holder="Materials engineering team",
        adversary_position="Cost reduction advocates may propose less expensive steels.",
        counter_arguments=[
            "Lower grade steels may compromise safety and durability.",
            "May fail to meet crash and corrosion targets."
        ],
        resolution_strategy="Benchmark against industry standards; validate through testing.",
        entity_scope="AUTO12 material engineering",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2340: Advanced High Strength Steel Standard"
    ),
    DoctrineBlock(
        topic="joining_methods_comparison",
        keywords=["joining", "welding", "adhesives", "riveting", "body structure"],
        conclusion_template="Joining methods must be selected based on strength, durability, manufacturability, and material compatibility.",
        reasoning_framework=(
            "Joining methods comparison involves evaluating welding, adhesives, riveting, and mechanical fasteners for body structure assembly. "
            "The framework includes assessing joint strength, fatigue resistance, corrosion protection, and manufacturability. Key factors are material compatibility, "
            "process reliability, and cost. Trade-offs involve balancing performance with manufacturing complexity and cost. Adversaries may argue for simpler or cheaper "
            "joining methods, but long-term durability and safety requirements are critical. Resolution is achieved through benchmarking, testing, and adherence to OEM joining standards."
        ),
        key_factors=[
            "Joint strength",
            "Fatigue resistance",
            "Corrosion protection",
            "Material compatibility",
            "Manufacturability"
        ],
        primary_authority=[
            "OEM joining standards",
            "SAE J2217",
            "Supplier data"
        ],
        burden_holder="Manufacturing engineering team",
        adversary_position="Cost reduction advocates may propose simpler joining methods.",
        counter_arguments=[
            "Simpler methods may compromise joint strength and durability.",
            "May fail to meet safety and corrosion targets."
        ],
        resolution_strategy="Benchmark against industry standards; validate through testing.",
        entity_scope="AUTO12 manufacturing engineering",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2217: Joining Methods Standard"
    ),
    DoctrineBlock(
        topic="body_structure_weight_optimization",
        keywords=["weight", "optimization", "body structure", "material selection", "performance"],
        conclusion_template="Body structure weight must be optimized without compromising safety, durability, or performance.",
        reasoning_framework=(
            "Weight optimization involves reducing body structure mass through material selection, geometry refinement, and manufacturing process improvements. "
            "The framework includes CAE analysis, benchmarking, and iterative design. Key factors are crash performance, durability, NVH, and manufacturability. "
            "Trade-offs involve balancing weight reduction with cost, complexity, and regulatory compliance. Adversaries may argue for aggressive weight reduction, "
            "but safety and durability requirements are paramount. Resolution is achieved through iterative optimization and validation."
        ),
        key_factors=[
            "Material selection",
            "Geometry refinement",
            "Manufacturing process",
            "Crash performance",
            "Durability"
        ],
        primary_authority=[
            "OEM weight targets",
            "SAE J1269",
            "Benchmarking data"
        ],
        burden_holder="Design engineering team",
        adversary_position="Aggressive weight reduction advocates may propose extreme measures.",
        counter_arguments=[
            "Extreme weight reduction may compromise safety and durability.",
            "May fail to meet regulatory and customer expectations."
        ],
        resolution_strategy="Optimize within performance and regulatory constraints; validate through testing.",
        entity_scope="AUTO12 body structure engineering",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J1269: Weight Optimization Standard"
    ),
    DoctrineBlock(
        topic="load_path_analysis",
        keywords=["load path", "analysis", "body structure", "crash", "stiffness"],
        conclusion_template="Load paths must be optimized to ensure efficient force transmission and occupant protection.",
        reasoning_framework=(
            "Load path analysis involves mapping and optimizing the transmission of forces through the body structure during crash and operational events. "
            "The framework includes CAE simulation, physical testing, and benchmarking. Key factors are force distribution, joint placement, and material selection. "
            "Trade-offs involve balancing stiffness, weight, and manufacturability. Adversaries may argue for simplified load paths to reduce complexity, "
            "but safety and performance requirements are critical. Resolution is achieved through iterative analysis and validation."
        ),
        key_factors=[
            "Force distribution",
            "Joint placement",
            "Material selection",
            "Stiffness",
            "Crash performance"
        ],
        primary_authority=[
            "OEM crash standards",
            "SAE J2435",
            "CAE simulation data"
        ],
        burden_holder="Structural engineering team",
        adversary_position="Manufacturing advocates may propose simplified load paths.",
        counter_arguments=[
            "Simplified load paths may compromise force transmission and occupant protection.",
            "May fail to meet crash performance targets."
        ],
        resolution_strategy="Optimize load paths through simulation and testing; prioritize safety.",
        entity_scope="AUTO12 structural engineering",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2435: Load Path Analysis Standard"
    ),
    DoctrineBlock(
        topic="tailored_blank_utilization",
        keywords=["tailored blank", "material", "body structure", "weight", "performance"],
        conclusion_template="Tailored blanks must be utilized to optimize material usage and enhance performance.",
        reasoning_framework=(
            "Tailored blank utilization involves using sheets of varying thickness and material properties in body structure components. "
            "The framework includes evaluating crash performance, weight reduction, and manufacturability. Key factors are material distribution, "
            "joining compatibility, and cost. Trade-offs involve balancing performance with process complexity and cost. Adversaries may argue for "
            "uniform materials to simplify manufacturing, but tailored blanks offer significant performance advantages. Resolution is achieved through "
            "benchmarking, testing, and optimization."
        ),
        key_factors=[
            "Material distribution",
            "Crash performance",
            "Weight reduction",
            "Joining compatibility",
            "Manufacturability"
        ],
        primary_authority=[
            "OEM tailored blank standards",
            "SAE J2340",
            "Supplier data"
        ],
        burden_holder="Materials engineering team",
        adversary_position="Manufacturing advocates may propose uniform materials.",
        counter_arguments=[
            "Uniform materials may increase weight and reduce performance.",
            "May fail to meet crash and weight targets."
        ],
        resolution_strategy="Optimize tailored blank usage through simulation and testing.",
        entity_scope="AUTO12 materials engineering",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2340: Advanced High Strength Steel Standard"
    ),
    DoctrineBlock(
        topic="seam_welding_vs_structural_adhesives",
        keywords=["seam welding", "structural adhesives", "joining", "body structure", "fatigue"],
        conclusion_template="Seam welding and structural adhesives must be selected based on joint strength, fatigue resistance, and manufacturing constraints.",
        reasoning_framework=(
            "Comparison of seam welding and structural adhesives involves evaluating joint strength, fatigue resistance, corrosion protection, and manufacturability. "
            "Seam welding offers high strength but may introduce heat-affected zones and corrosion risk. Structural adhesives provide improved fatigue resistance and "
            "corrosion protection but require precise application and curing. Trade-offs involve balancing performance with process complexity and cost. Adversaries may "
            "argue for exclusive use of one method, but hybrid joining often yields optimal results. Resolution is achieved through benchmarking, testing, and optimization."
        ),
        key_factors=[
            "Joint strength",
            "Fatigue resistance",
            "Corrosion protection",
            "Manufacturing constraints",
            "Process reliability"
        ],
        primary_authority=[
            "OEM joining standards",
            "SAE J2217",
            "Supplier data"
        ],
        burden_holder="Manufacturing engineering team",
        adversary_position="Process simplification advocates may propose exclusive use of one method.",
        counter_arguments=[
            "Exclusive use may compromise joint performance.",
            "Hybrid joining offers superior results."
        ],
        resolution_strategy="Optimize joining methods through benchmarking and testing.",
        entity_scope="AUTO12 manufacturing engineering",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2217: Joining Methods Standard"
    ),
    DoctrineBlock(
        topic="panel_fit_and_gap_management",
        keywords=["panel fit", "gap", "body structure", "manufacturing", "quality"],
        conclusion_template="Panel fit and gap management must ensure consistent quality and minimize NVH and aerodynamic losses.",
        reasoning_framework=(
            "Panel fit and gap management involves controlling tolerances during manufacturing to ensure consistent quality, minimize NVH, and optimize aerodynamics. "
            "The framework includes statistical process control, measurement systems, and benchmarking. Key factors are tolerance stack-up, joining method, and material stability. "
            "Trade-offs involve balancing manufacturing complexity, cost, and quality targets. Adversaries may argue for relaxed tolerances to reduce cost, but customer satisfaction "
            "and competitive benchmarks are critical. Resolution is achieved through process optimization and quality control."
        ),
        key_factors=[
            "Tolerance control",
            "Joining method",
            "Material stability",
            "Quality targets",
            "NVH and aerodynamic performance"
        ],
        primary_authority=[
            "OEM quality standards",
            "SAE J2117",
            "Benchmarking data"
        ],
        burden_holder="Manufacturing quality team",
        adversary_position="Cost reduction advocates may propose relaxed tolerances.",
        counter_arguments=[
            "Relaxed tolerances compromise quality and performance.",
            "May lead to customer dissatisfaction."
        ],
        resolution_strategy="Optimize process control; prioritize quality and performance.",
        entity_scope="AUTO12 manufacturing quality",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2117: Panel Fit and Gap Standard"
    ),
    DoctrineBlock(
        topic="body_structure_modularity",
        keywords=["modularity", "body structure", "platform", "manufacturing", "flexibility"],
        conclusion_template="Body structure modularity must enable platform flexibility and manufacturing efficiency.",
        reasoning_framework=(
            "Body structure modularity involves designing components and assemblies for platform flexibility and manufacturing efficiency. "
            "The framework includes evaluating interchangeability, scalability, and assembly complexity. Key factors are commonality, joining method, and material compatibility. "
            "Trade-offs involve balancing flexibility, cost, and performance. Adversaries may argue for bespoke designs to optimize performance, but modularity offers significant "
            "manufacturing and cost advantages. Resolution is achieved through benchmarking, design optimization, and process validation."
        ),
        key_factors=[
            "Component interchangeability",
            "Platform scalability",
            "Assembly complexity",
            "Commonality",
            "Material compatibility"
        ],
        primary_authority=[
            "OEM platform standards",
            "SAE J3000",
            "Benchmarking data"
        ],
        burden_holder="Platform engineering team",
        adversary_position="Performance advocates may propose bespoke designs.",
        counter_arguments=[
            "Bespoke designs increase manufacturing complexity and cost.",
            "Modularity enables flexibility and efficiency."
        ],
        resolution_strategy="Optimize modularity through benchmarking and design validation.",
        entity_scope="AUTO12 platform engineering",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J3000: Platform Modularity Standard"
    ),
    DoctrineBlock(
        topic="thermal_management_in_body_structure",
        keywords=["thermal management", "body structure", "heat dissipation", "insulation", "material"],
        conclusion_template="Thermal management must be integrated into body structure to ensure occupant comfort and component reliability.",
        reasoning_framework=(
            "Thermal management in body structure involves integrating heat dissipation and insulation features to maintain occupant comfort and component reliability. "
            "The framework includes evaluating material thermal properties, insulation placement, and heat dissipation strategies. Key factors are environmental exposure, "
            "component packaging, and manufacturability. Trade-offs involve balancing cost, weight, and performance. Adversaries may argue for reduced insulation to save weight, "
            "but comfort and reliability requirements are critical. Resolution is achieved through benchmarking, testing, and optimization."
        ),
        key_factors=[
            "Material thermal properties",
            "Insulation placement",
            "Heat dissipation",
            "Component packaging",
            "Occupant comfort"
        ],
        primary_authority=[
            "OEM thermal standards",
            "SAE J2234",
            "Supplier data"
        ],
        burden_holder="Thermal engineering team",
        adversary_position="Weight reduction advocates may propose reduced insulation.",
        counter_arguments=[
            "Reduced insulation may compromise comfort and reliability.",
            "May lead to customer dissatisfaction."
        ],
        resolution_strategy="Optimize thermal management through benchmarking and testing.",
        entity_scope="AUTO12 thermal engineering",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2234: Thermal Management Standard"
    ),
    DoctrineBlock(
        topic="body_structure_repairability",
        keywords=["repairability", "body structure", "service", "joining", "material"],
        conclusion_template="Body structure must be designed for repairability to minimize service costs and downtime.",
        reasoning_framework=(
            "Body structure repairability involves designing components and assemblies for ease of service and repair. "
            "The framework includes evaluating joining methods, material selection, and accessibility. Key factors are component modularity, joining compatibility, "
            "and service procedures. Trade-offs involve balancing performance, cost, and repairability. Adversaries may argue for performance-optimized designs that "
            "are difficult to repair, but service and warranty requirements are critical. Resolution is achieved through benchmarking, design optimization, and service validation."
        ),
        key_factors=[
            "Component modularity",
            "Joining compatibility",
            "Material selection",
            "Service accessibility",
            "Repair procedures"
        ],
        primary_authority=[
            "OEM service standards",
            "SAE J2335",
            "Service manuals"
        ],
        burden_holder="Service engineering team",
        adversary_position="Performance advocates may propose designs that are difficult to repair.",
        counter_arguments=[
            "Difficult repairs increase service costs and downtime.",
            "May lead to customer dissatisfaction and warranty claims."
        ],
        resolution_strategy="Optimize repairability through design and service validation.",
        entity_scope="AUTO12 service engineering",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2335: Body Structure Repairability Standard"
    ),
    DoctrineBlock(
        topic="body_structure_recyclability",
        keywords=["recyclability", "body structure", "material", "environment", "end-of-life"],
        conclusion_template="Body structure must be designed for recyclability to meet environmental and regulatory requirements.",
        reasoning_framework=(
            "Body structure recyclability involves selecting materials and joining methods that facilitate end-of-life recycling. "
            "The framework includes evaluating material compatibility, disassembly procedures, and environmental impact. Key factors are material selection, joining method, "
            "and regulatory compliance. Trade-offs involve balancing performance, cost, and recyclability. Adversaries may argue for performance-optimized materials that are difficult "
            "to recycle, but environmental and regulatory requirements are critical. Resolution is achieved through benchmarking, design optimization, and compliance validation."
        ),
        key_factors=[
            "Material selection",
            "Joining method",
            "Disassembly procedures",
            "Environmental impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "OEM environmental standards",
            "ISO 22628",
            "Regulatory guidelines"
        ],
        burden_holder="Environmental engineering team",
        adversary_position="Performance advocates may propose materials that are difficult to recycle.",
        counter_arguments=[
            "Difficult-to-recycle materials increase environmental impact.",
            "May fail to meet regulatory requirements."
        ],
        resolution_strategy="Optimize recyclability through material selection and joining method.",
        entity_scope="AUTO12 environmental engineering",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 22628: Recyclability Standard"
    ),
    DoctrineBlock(
        topic="body_structure_cost_management",
        keywords=["cost management", "body structure", "material", "manufacturing", "optimization"],
        conclusion_template="Body structure cost must be managed through material selection, manufacturing efficiency, and design optimization.",
        reasoning_framework=(
            "Cost management in body structure involves optimizing material selection, manufacturing processes, and design to minimize total cost. "
            "The framework includes evaluating material cost, process complexity, and assembly efficiency. Key factors are material selection, joining method, "
            "and manufacturing process. Trade-offs involve balancing cost with performance and quality targets. Adversaries may argue for aggressive cost reduction, "
            "but safety, durability, and quality requirements are critical. Resolution is achieved through benchmarking, process optimization, and design validation."
        ),
        key_factors=[
            "Material cost",
            "Process complexity",
            "Assembly efficiency",
            "Performance targets",
            "Quality targets"
        ],
        primary_authority=[
            "OEM cost standards",
            "SAE J2340",
            "Benchmarking data"
        ],
        burden_holder="Cost engineering team",
        adversary_position="Aggressive cost reduction advocates may propose extreme measures.",
        counter_arguments=[
            "Extreme cost reduction may compromise safety, durability, and quality.",
            "May lead to customer dissatisfaction and warranty claims."
        ],
        resolution_strategy="Optimize cost management through benchmarking and process optimization.",
        entity_scope="AUTO12 cost engineering",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2340: Advanced High Strength Steel Standard"
    ),
    DoctrineBlock(
        topic="body_structure_sustainability",
        keywords=["sustainability", "body structure", "material", "environment", "manufacturing"],
        conclusion_template="Body structure must be designed for sustainability through material selection, manufacturing processes, and recyclability.",
        reasoning_framework=(
            "Sustainability in body structure involves selecting environmentally friendly materials, optimizing manufacturing processes, and ensuring recyclability. "
            "The framework includes evaluating environmental impact, energy consumption, and end-of-life recycling. Key factors are material selection, manufacturing process, "
            "and regulatory compliance. Trade-offs involve balancing performance, cost, and sustainability. Adversaries may argue for performance-optimized materials that are less sustainable, "
            "but environmental and regulatory requirements are critical. Resolution is achieved through benchmarking, design optimization, and compliance validation."
        ),
        key_factors=[
            "Material selection",
            "Manufacturing process",
            "Environmental impact",
            "Energy consumption",
            "Regulatory compliance"
        ],
        primary_authority=[
            "OEM sustainability standards",
            "ISO 14001",
            "Regulatory guidelines"
        ],
        burden_holder="Sustainability engineering team",
        adversary_position="Performance advocates may propose less sustainable materials.",
        counter_arguments=[
            "Less sustainable materials increase environmental impact.",
            "May fail to meet regulatory requirements."
        ],
        resolution_strategy="Optimize sustainability through material selection and manufacturing process.",
        entity_scope="AUTO12 sustainability engineering",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14001: Environmental Management Standard"
    ),
    DoctrineBlock(
        topic="body_structure_assembly_line_optimization",
        keywords=["assembly line", "optimization", "body structure", "manufacturing", "efficiency"],
        conclusion_template="Body structure assembly line must be optimized for efficiency, quality, and cost.",
        reasoning_framework=(
            "Assembly line optimization involves refining manufacturing processes, equipment layout, and workflow to maximize efficiency, quality, and cost effectiveness. "
            "The framework includes evaluating process flow, automation, and quality control. Key factors are process reliability, equipment utilization, and labor efficiency. "
            "Trade-offs involve balancing automation, cost, and flexibility. Adversaries may argue for manual processes to reduce automation cost, but efficiency and quality targets are critical. "
            "Resolution is achieved through benchmarking, process optimization, and validation."
        ),
        key_factors=[
            "Process reliability",
            "Equipment utilization",
            "Labor efficiency",
            "Automation",
            "Quality control"
        ],
        primary_authority=[
            "OEM manufacturing standards",
            "SAE J2178",
            "Benchmarking data"
        ],
        burden_holder="Manufacturing engineering team",
        adversary_position="Manual process advocates may propose reduced automation.",
        counter_arguments=[
            "Reduced automation may compromise efficiency and quality.",
            "May fail to meet manufacturing targets."
        ],
        resolution_strategy="Optimize assembly line through benchmarking and process validation.",
        entity_scope="AUTO12 manufacturing engineering",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2178: Assembly Line Optimization Standard"
    ),
    DoctrineBlock(
        topic="body_structure_quality_control",
        keywords=["quality control", "body structure", "manufacturing", "inspection", "process"],
        conclusion_template="Body structure quality control must ensure consistent manufacturing and compliance with standards.",
        reasoning_framework=(
            "Quality control in body structure involves implementing inspection and process control measures to ensure consistent manufacturing and compliance with standards. "
            "The framework includes statistical process control, automated inspection, and root cause analysis. Key factors are process reliability, inspection accuracy, and corrective action. "
            "Trade-offs involve balancing inspection cost, process complexity, and quality targets. Adversaries may argue for reduced inspection to save cost, but quality and compliance requirements are critical. "
            "Resolution is achieved through process optimization and quality validation."
        ),
        key_factors=[
            "Process reliability",
            "Inspection accuracy",
            "Corrective action",
            "Quality targets",
            "Compliance"
        ],
        primary_authority=[
            "OEM quality standards",
            "SAE J2117",
            "Benchmarking data"
        ],
        burden_holder="Quality engineering team",
        adversary_position="Cost reduction advocates may propose reduced inspection.",
        counter_arguments=[
            "Reduced inspection may compromise quality and compliance.",
            "May lead to customer dissatisfaction and warranty claims."
        ],
        resolution_strategy="Optimize quality control through process and inspection validation.",
        entity_scope="AUTO12 quality engineering",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2117: Quality Control Standard"
    ),
    DoctrineBlock(
        topic="body_structure_material_traceability",
        keywords=["material traceability", "body structure", "manufacturing", "quality", "compliance"],
        conclusion_template="Material traceability must be maintained throughout body structure manufacturing to ensure quality and compliance.",
        reasoning_framework=(
            "Material traceability involves tracking materials from supplier to finished product to ensure quality and compliance. "
            "The framework includes barcode tracking, documentation, and process validation. Key factors are supplier quality, process reliability, and regulatory compliance. "
            "Trade-offs involve balancing traceability cost, process complexity, and quality targets. Adversaries may argue for reduced traceability to save cost, but quality and compliance requirements are critical. "
            "Resolution is achieved through process optimization and traceability validation."
        ),
        key_factors=[
            "Supplier quality",
            "Process reliability",
            "Documentation",
            "Regulatory compliance",
            "Quality targets"
        ],
        primary_authority=[
            "OEM traceability standards",
            "ISO 9001",
            "Supplier data"
        ],
        burden_holder="Quality engineering team",
        adversary_position="Cost reduction advocates may propose reduced traceability.",
        counter_arguments=[
            "Reduced traceability may compromise quality and compliance.",
            "May lead to regulatory violations and warranty claims."
        ],
        resolution_strategy="Optimize traceability through process and documentation validation.",
        entity_scope="AUTO12 quality engineering",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001: Quality Management Standard"
    ),
    DoctrineBlock(
        topic="body_structure_innovation_management",
        keywords=["innovation", "body structure", "technology", "process", "performance"],
        conclusion_template="Innovation management must foster new technologies and processes to enhance body structure performance.",
        reasoning_framework=(
            "Innovation management involves fostering new technologies and processes to enhance body structure performance. "
            "The framework includes evaluating emerging materials, joining methods, and manufacturing processes. Key factors are performance improvement, cost, and manufacturability. "
            "Trade-offs involve balancing innovation risk, cost, and performance targets. Adversaries may argue for conservative approaches to minimize risk, but innovation is critical for competitive advantage. "
            "Resolution is achieved through benchmarking, pilot testing, and process validation."
        ),
        key_factors=[
            "Performance improvement",
            "Cost",
            "Manufacturability",
            "Innovation risk",
            "Competitive advantage"
        ],
        primary_authority=[
            "OEM innovation standards",
            "SAE J3000",
            "Benchmarking data"
        ],
        burden_holder="Innovation engineering team",
        adversary_position="Conservative advocates may propose minimizing innovation risk.",
        counter_arguments=[
            "Minimizing innovation risk may compromise competitive advantage.",
            "Innovation is critical for performance improvement."
        ],
        resolution_strategy="Foster innovation through benchmarking and pilot testing.",
        entity_scope="AUTO12 innovation engineering",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J3000: Innovation Management Standard"
    ),
    DoctrineBlock(
        topic="body_structure_supplier_management",
        keywords=["supplier management", "body structure", "quality", "cost", "manufacturing"],
        conclusion_template="Supplier management must ensure quality, cost, and reliability in body structure manufacturing.",
        reasoning_framework=(
            "Supplier management involves selecting and monitoring suppliers to ensure quality, cost, and reliability in body structure manufacturing. "
            "The framework includes evaluating supplier quality, cost, and delivery performance. Key factors are supplier selection, quality control, and process reliability. "
            "Trade-offs involve balancing supplier cost, quality, and delivery performance. Adversaries may argue for cost-focused supplier selection, but quality and reliability requirements are critical. "
            "Resolution is achieved through benchmarking, supplier audits, and process validation."
        ),
        key_factors=[
            "Supplier selection",
            "Quality control",
            "Cost",
            "Delivery performance",
            "Process reliability"
        ],
        primary_authority=[
            "OEM supplier standards",
            "ISO 9001",
            "Supplier audit data"
        ],
        burden_holder="Supplier engineering team",
        adversary_position="Cost-focused advocates may propose selecting lower-cost suppliers.",
        counter_arguments=[
            "Lower-cost suppliers may compromise quality and reliability.",
            "May lead to manufacturing disruptions and warranty claims."
        ],
        resolution_strategy="Optimize supplier management through benchmarking and audits.",
        entity_scope="AUTO12 supplier engineering",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001: Quality Management Standard"
    ),
    DoctrineBlock(
        topic="body_structure_standardization",
        keywords=["standardization", "body structure", "platform", "manufacturing", "quality"],
        conclusion_template="Standardization must be implemented to ensure quality, efficiency, and platform flexibility in body structure manufacturing.",
        reasoning_framework=(
            "Standardization involves implementing common components, processes, and specifications to ensure quality, efficiency, and platform flexibility. "
            "The framework includes evaluating component commonality, process standardization, and platform scalability. Key factors are quality, efficiency, and flexibility. "
            "Trade-offs involve balancing standardization with performance and customization. Adversaries may argue for bespoke designs to optimize performance, but standardization offers significant advantages. "
            "Resolution is achieved through benchmarking, design optimization, and process validation."
        ),
        key_factors=[
            "Component commonality",
            "Process standardization",
            "Platform scalability",
            "Quality",
            "Efficiency"
        ],
        primary_authority=[
            "OEM platform standards",
            "SAE J3000",
            "Benchmarking data"
        ],
        burden_holder="Platform engineering team",
        adversary_position="Performance advocates may propose bespoke designs.",
        counter_arguments=[
            "Bespoke designs increase manufacturing complexity and cost.",
            "Standardization enables quality and efficiency."
        ],
        resolution_strategy="Optimize standardization through benchmarking and design validation.",
        entity_scope="AUTO12 platform engineering",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J3000: Platform Standardization Standard"
    ),
    DoctrineBlock(
        topic="body_structure_automation_integration",
        keywords=["automation", "integration", "body structure", "manufacturing", "efficiency"],
        conclusion_template="Automation integration must be implemented to enhance manufacturing efficiency and quality in body structure assembly.",
        reasoning_framework=(
            "Automation integration involves implementing automated processes and equipment to enhance manufacturing efficiency and quality. "
            "The framework includes evaluating process reliability, equipment utilization, and quality control. Key factors are automation, efficiency, and quality. "
            "Trade-offs involve balancing automation cost, flexibility, and performance. Adversaries may argue for manual processes to reduce automation cost, but efficiency and quality targets are critical. "
            "Resolution is achieved through benchmarking, process optimization, and validation."
        ),
        key_factors=[
            "Process reliability",
            "Equipment utilization",
            "Automation",
            "Efficiency",
            "Quality control"
        ],
        primary_authority=[
            "OEM automation standards",
            "SAE J2178",
            "Benchmarking data"
        ],
        burden_holder="Manufacturing engineering team",
        adversary_position="Manual process advocates may propose reduced automation.",
        counter_arguments=[
            "Reduced automation may compromise efficiency and quality.",
            "May fail to meet manufacturing targets."
        ],
        resolution_strategy="Optimize automation integration through benchmarking and process validation.",
        entity_scope="AUTO12 manufacturing engineering",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2178: Automation Integration Standard"
    ),
    DoctrineBlock(
        topic="body_structure_digital_twin_application",
        keywords=["digital twin", "body structure", "simulation", "manufacturing", "optimization"],
        conclusion_template="Digital twin application must be utilized to optimize body structure design and manufacturing processes.",
        reasoning_framework=(
            "Digital twin application involves creating virtual models of body structure and manufacturing processes to optimize design and production. "
            "The framework includes simulation, process validation, and benchmarking. Key factors are simulation accuracy, process optimization, and quality control. "
            "Trade-offs involve balancing digital twin implementation cost, complexity, and performance. Adversaries may argue for traditional methods to reduce cost, but digital twin offers significant advantages. "
            "Resolution is achieved through benchmarking, simulation, and process validation."
        ),
        key_factors=[
            "Simulation accuracy",
            "Process optimization",
            "Quality control",
            "Implementation cost",
            "Performance"
        ],
        primary_authority=[
            "OEM digital twin standards",
            "ISO 23247",
            "Benchmarking data"
        ],
        burden_holder="Simulation engineering team",
        adversary_position="Traditional method advocates may propose minimizing digital twin implementation.",
        counter_arguments=[
            "Minimizing digital twin implementation may compromise optimization and quality.",
            "Digital twin offers significant advantages."
        ],
        resolution_strategy="Optimize digital twin application through benchmarking and simulation.",
        entity_scope="AUTO12 simulation engineering",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 23247: Digital Twin Standard"
    ),
    DoctrineBlock(
        topic="body_structure_virtual_validation",
        keywords=["virtual validation", "body structure", "simulation", "testing", "optimization"],
        conclusion_template="Virtual validation must be implemented to optimize body structure design and reduce physical testing requirements.",
        reasoning_framework=(
            "Virtual validation involves using simulation tools to optimize body structure design and reduce physical testing requirements. "
            "The framework includes CAE analysis, benchmarking, and process validation. Key factors are simulation accuracy, process optimization, and quality control. "
            "Trade-offs involve balancing simulation cost, complexity, and performance. Adversaries may argue for exclusive reliance on physical testing, but virtual validation offers significant advantages. "
            "Resolution is achieved through benchmarking, simulation, and process validation."
        ),
        key_factors=[
            "Simulation accuracy",
            "Process optimization",
            "Quality control",
            "Testing requirements",
            "Performance"
        ],
        primary_authority=[
            "OEM virtual validation standards",
            "SAE J2435",
            "Benchmarking data"
        ],
        burden_holder="Simulation engineering team",
        adversary_position="Physical testing advocates may propose exclusive reliance on physical testing.",
        counter_arguments=[
            "Exclusive reliance on physical testing increases cost and time.",
            "Virtual validation offers significant advantages."
        ],
        resolution_strategy="Optimize virtual validation through benchmarking and simulation.",
        entity_scope="AUTO12 simulation engineering",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2435: Virtual Validation Standard"
    ),
    DoctrineBlock(
        topic="body_structure_safety_feature_integration",
        keywords=["safety feature", "integration", "body structure", "crash", "occupant protection"],
        conclusion_template="Safety features must be integrated into body structure to maximize occupant protection and regulatory compliance.",
        reasoning_framework=(
            "Safety feature integration involves incorporating crash protection systems into body structure to maximize occupant protection and regulatory compliance. "
            "The framework includes evaluating crash performance, system compatibility, and regulatory requirements. Key factors are crash performance, occupant protection, and compliance. "
            "Trade-offs involve balancing safety feature integration with cost and manufacturing complexity. Adversaries may argue for reduced safety features to save cost, but safety and compliance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Crash performance",
            "Occupant protection",
            "System compatibility",
            "Regulatory compliance",
            "Cost"
        ],
        primary_authority=[
            "OEM safety standards",
            "FMVSS 208",
            "Euro NCAP"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Cost reduction advocates may propose reduced safety features.",
        counter_arguments=[
            "Reduced safety features compromise occupant protection and compliance.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize safety feature integration through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 208: Occupant Crash Protection"
    ),
    DoctrineBlock(
        topic="body_structure_occupant_space_management",
        keywords=["occupant space", "management", "body structure", "packaging", "comfort"],
        conclusion_template="Occupant space must be managed to maximize comfort, safety, and packaging efficiency.",
        reasoning_framework=(
            "Occupant space management involves optimizing body structure geometry and packaging to maximize comfort, safety, and efficiency. "
            "The framework includes evaluating occupant ergonomics, packaging constraints, and crash performance. Key factors are comfort, safety, and packaging efficiency. "
            "Trade-offs involve balancing occupant space with structural performance and manufacturing complexity. Adversaries may argue for reduced occupant space to optimize structure, but comfort and safety requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Occupant ergonomics",
            "Packaging constraints",
            "Crash performance",
            "Comfort",
            "Safety"
        ],
        primary_authority=[
            "OEM packaging standards",
            "SAE J1100",
            "Benchmarking data"
        ],
        burden_holder="Packaging engineering team",
        adversary_position="Structural advocates may propose reduced occupant space.",
        counter_arguments=[
            "Reduced occupant space compromises comfort and safety.",
            "May lead to customer dissatisfaction."
        ],
        resolution_strategy="Optimize occupant space management through benchmarking and design validation.",
        entity_scope="AUTO12 packaging engineering",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J1100: Occupant Packaging Standard"
    ),
    DoctrineBlock(
        topic="body_structure_electrical_integration",
        keywords=["electrical integration", "body structure", "wiring", "component", "packaging"],
        conclusion_template="Electrical integration must be optimized in body structure to ensure reliability, safety, and packaging efficiency.",
        reasoning_framework=(
            "Electrical integration involves optimizing wiring and component placement within body structure to ensure reliability, safety, and packaging efficiency. "
            "The framework includes evaluating wiring routing, component packaging, and safety requirements. Key factors are reliability, safety, and packaging efficiency. "
            "Trade-offs involve balancing electrical integration with structural performance and manufacturing complexity. Adversaries may argue for simplified electrical integration to reduce cost, but reliability and safety requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Wiring routing",
            "Component packaging",
            "Reliability",
            "Safety",
            "Packaging efficiency"
        ],
        primary_authority=[
            "OEM electrical standards",
            "SAE J1939",
            "Benchmarking data"
        ],
        burden_holder="Electrical engineering team",
        adversary_position="Cost reduction advocates may propose simplified electrical integration.",
        counter_arguments=[
            "Simplified integration may compromise reliability and safety.",
            "May lead to customer dissatisfaction."
        ],
        resolution_strategy="Optimize electrical integration through benchmarking and design validation.",
        entity_scope="AUTO12 electrical engineering",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J1939: Electrical Integration Standard"
    ),
    DoctrineBlock(
        topic="body_structure_water_management",
        keywords=["water management", "body structure", "sealing", "drainage", "durability"],
        conclusion_template="Water management must be integrated into body structure to ensure durability and prevent corrosion.",
        reasoning_framework=(
            "Water management involves integrating sealing and drainage features into body structure to ensure durability and prevent corrosion. "
            "The framework includes evaluating sealing quality, drainage design, and environmental exposure. Key factors are durability, corrosion prevention, and environmental exposure. "
            "Trade-offs involve balancing water management with manufacturing complexity and cost. Adversaries may argue for reduced water management features to save cost, but durability and corrosion prevention requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Sealing quality",
            "Drainage design",
            "Durability",
            "Corrosion prevention",
            "Environmental exposure"
        ],
        primary_authority=[
            "OEM water management standards",
            "SAE J2334",
            "Benchmarking data"
        ],
        burden_holder="Durability engineering team",
        adversary_position="Cost reduction advocates may propose reduced water management features.",
        counter_arguments=[
            "Reduced features compromise durability and corrosion prevention.",
            "May lead to warranty claims and customer dissatisfaction."
        ],
        resolution_strategy="Optimize water management through benchmarking and design validation.",
        entity_scope="AUTO12 durability engineering",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2334: Corrosion Protection Standard"
    ),
    DoctrineBlock(
        topic="body_structure_passive_safety_systems",
        keywords=["passive safety", "body structure", "airbags", "seat belts", "crash"],
        conclusion_template="Passive safety systems must be integrated into body structure to maximize occupant protection.",
        reasoning_framework=(
            "Passive safety system integration involves incorporating airbags, seat belts, and crash protection features into body structure to maximize occupant protection. "
            "The framework includes evaluating crash performance, system compatibility, and regulatory requirements. Key factors are crash performance, occupant protection, and compliance. "
            "Trade-offs involve balancing passive safety system integration with cost and manufacturing complexity. Adversaries may argue for reduced passive safety systems to save cost, but safety and compliance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Crash performance",
            "Occupant protection",
            "System compatibility",
            "Regulatory compliance",
            "Cost"
        ],
        primary_authority=[
            "OEM safety standards",
            "FMVSS 208",
            "Euro NCAP"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Cost reduction advocates may propose reduced passive safety systems.",
        counter_arguments=[
            "Reduced systems compromise occupant protection and compliance.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize passive safety system integration through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 208: Occupant Crash Protection"
    ),
    DoctrineBlock(
        topic="body_structure_active_safety_systems",
        keywords=["active safety", "body structure", "sensors", "electronics", "crash avoidance"],
        conclusion_template="Active safety systems must be integrated into body structure to maximize crash avoidance and occupant protection.",
        reasoning_framework=(
            "Active safety system integration involves incorporating sensors, electronics, and crash avoidance features into body structure to maximize occupant protection. "
            "The framework includes evaluating system compatibility, crash avoidance performance, and regulatory requirements. Key factors are crash avoidance, occupant protection, and compliance. "
            "Trade-offs involve balancing active safety system integration with cost and manufacturing complexity. Adversaries may argue for reduced active safety systems to save cost, but safety and compliance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Crash avoidance",
            "Occupant protection",
            "System compatibility",
            "Regulatory compliance",
            "Cost"
        ],
        primary_authority=[
            "OEM safety standards",
            "FMVSS 126",
            "Euro NCAP"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Cost reduction advocates may propose reduced active safety systems.",
        counter_arguments=[
            "Reduced systems compromise crash avoidance and occupant protection.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize active safety system integration through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 126: Electronic Stability Control"
    ),
    DoctrineBlock(
        topic="body_structure_ergonomics",
        keywords=["ergonomics", "body structure", "comfort", "packaging", "design"],
        conclusion_template="Body structure ergonomics must be optimized to maximize occupant comfort and accessibility.",
        reasoning_framework=(
            "Ergonomics in body structure involves optimizing geometry and packaging to maximize occupant comfort and accessibility. "
            "The framework includes evaluating occupant ergonomics, packaging constraints, and accessibility. Key factors are comfort, accessibility, and packaging efficiency. "
            "Trade-offs involve balancing ergonomics with structural performance and manufacturing complexity. Adversaries may argue for reduced ergonomics to optimize structure, but comfort and accessibility requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Occupant ergonomics",
            "Packaging constraints",
            "Accessibility",
            "Comfort",
            "Structural performance"
        ],
        primary_authority=[
            "OEM ergonomics standards",
            "SAE J1100",
            "Benchmarking data"
        ],
        burden_holder="Ergonomics engineering team",
        adversary_position="Structural advocates may propose reduced ergonomics.",
        counter_arguments=[
            "Reduced ergonomics compromise comfort and accessibility.",
            "May lead to customer dissatisfaction."
        ],
        resolution_strategy="Optimize ergonomics through benchmarking and design validation.",
        entity_scope="AUTO12 ergonomics engineering",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J1100: Ergonomics Standard"
    ),
    DoctrineBlock(
        topic="body_structure_pedestrian_protection",
        keywords=["pedestrian protection", "body structure", "crash", "safety", "regulatory"],
        conclusion_template="Pedestrian protection must be integrated into body structure to comply with safety regulations and minimize injury risk.",
        reasoning_framework=(
            "Pedestrian protection involves designing body structure features to minimize injury risk and comply with safety regulations. "
            "The framework includes evaluating crash performance, injury metrics, and regulatory requirements. Key factors are crash performance, injury risk, and compliance. "
            "Trade-offs involve balancing pedestrian protection with styling and manufacturing complexity. Adversaries may argue for reduced protection to optimize styling, but safety and compliance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Crash performance",
            "Injury risk",
            "Regulatory compliance",
            "Styling",
            "Manufacturing complexity"
        ],
        primary_authority=[
            "OEM safety standards",
            "Euro NCAP",
            "FMVSS 201"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Styling advocates may propose reduced pedestrian protection.",
        counter_arguments=[
            "Reduced protection compromises safety and compliance.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize pedestrian protection through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 201: Occupant Protection in Interior Impact"
    ),
    DoctrineBlock(
        topic="body_structure_child_occupant_protection",
        keywords=["child occupant protection", "body structure", "safety", "crash", "regulatory"],
        conclusion_template="Child occupant protection must be integrated into body structure to comply with safety regulations and maximize protection.",
        reasoning_framework=(
            "Child occupant protection involves designing body structure features to maximize protection and comply with safety regulations. "
            "The framework includes evaluating crash performance, injury metrics, and regulatory requirements. Key factors are crash performance, injury risk, and compliance. "
            "Trade-offs involve balancing child occupant protection with cost and manufacturing complexity. Adversaries may argue for reduced protection to save cost, but safety and compliance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Crash performance",
            "Injury risk",
            "Regulatory compliance",
            "Cost",
            "Manufacturing complexity"
        ],
        primary_authority=[
            "OEM safety standards",
            "Euro NCAP",
            "FMVSS 213"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Cost reduction advocates may propose reduced child occupant protection.",
        counter_arguments=[
            "Reduced protection compromises safety and compliance.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize child occupant protection through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 213: Child Restraint Systems"
    ),
    DoctrineBlock(
        topic="body_structure_interior_injury_mitigation",
        keywords=["interior injury mitigation", "body structure", "crash", "safety", "regulatory"],
        conclusion_template="Interior injury mitigation must be integrated into body structure to comply with safety regulations and minimize injury risk.",
        reasoning_framework=(
            "Interior injury mitigation involves designing body structure features to minimize injury risk and comply with safety regulations. "
            "The framework includes evaluating crash performance, injury metrics, and regulatory requirements. Key factors are crash performance, injury risk, and compliance. "
            "Trade-offs involve balancing injury mitigation with cost and manufacturing complexity. Adversaries may argue for reduced mitigation features to save cost, but safety and compliance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Crash performance",
            "Injury risk",
            "Regulatory compliance",
            "Cost",
            "Manufacturing complexity"
        ],
        primary_authority=[
            "OEM safety standards",
            "FMVSS 201",
            "Euro NCAP"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Cost reduction advocates may propose reduced injury mitigation features.",
        counter_arguments=[
            "Reduced features compromise safety and compliance.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize injury mitigation through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 201: Occupant Protection in Interior Impact"
    ),
    DoctrineBlock(
        topic="body_structure_fire_protection",
        keywords=["fire protection", "body structure", "material", "safety", "regulatory"],
        conclusion_template="Fire protection must be integrated into body structure to comply with safety regulations and minimize risk.",
        reasoning_framework=(
            "Fire protection involves selecting materials and designing body structure features to minimize fire risk and comply with safety regulations. "
            "The framework includes evaluating material fire resistance, system compatibility, and regulatory requirements. Key factors are fire resistance, safety, and compliance. "
            "Trade-offs involve balancing fire protection with cost and manufacturing complexity. Adversaries may argue for reduced fire protection features to save cost, but safety and compliance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Material fire resistance",
            "System compatibility",
            "Safety",
            "Regulatory compliance",
            "Cost"
        ],
        primary_authority=[
            "OEM safety standards",
            "FMVSS 302",
            "Euro NCAP"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Cost reduction advocates may propose reduced fire protection features.",
        counter_arguments=[
            "Reduced features compromise safety and compliance.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize fire protection through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 302: Flammability of Interior Materials"
    ),
    DoctrineBlock(
        topic="body_structure_torsional_stiffness_optimization",
        keywords=["torsional stiffness", "body structure", "performance", "NVH", "crash"],
        conclusion_template="Torsional stiffness must be optimized in body structure to maximize performance, NVH, and crash protection.",
        reasoning_framework=(
            "Torsional stiffness optimization involves refining body structure geometry and material selection to maximize performance, NVH, and crash protection. "
            "The framework includes evaluating stiffness, crash performance, and NVH targets. Key factors are geometry, material selection, and joining method. "
            "Trade-offs involve balancing torsional stiffness with weight and cost. Adversaries may argue for reduced stiffness to save weight, but performance and safety requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Geometry",
            "Material selection",
            "Joining method",
            "Performance",
            "NVH"
        ],
        primary_authority=[
            "OEM performance standards",
            "SAE J2340",
            "Benchmarking data"
        ],
        burden_holder="Performance engineering team",
        adversary_position="Weight reduction advocates may propose reduced stiffness.",
        counter_arguments=[
            "Reduced stiffness compromises performance, NVH, and crash protection.",
            "May lead to customer dissatisfaction."
        ],
        resolution_strategy="Optimize torsional stiffness through benchmarking and design validation.",
        entity_scope="AUTO12 performance engineering",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2340: Advanced High Strength Steel Standard"
    ),
    DoctrineBlock(
        topic="body_structure_bending_stiffness_optimization",
        keywords=["bending stiffness", "body structure", "performance", "NVH", "crash"],
        conclusion_template="Bending stiffness must be optimized in body structure to maximize performance, NVH, and crash protection.",
        reasoning_framework=(
            "Bending stiffness optimization involves refining body structure geometry and material selection to maximize performance, NVH, and crash protection. "
            "The framework includes evaluating stiffness, crash performance, and NVH targets. Key factors are geometry, material selection, and joining method. "
            "Trade-offs involve balancing bending stiffness with weight and cost. Adversaries may argue for reduced stiffness to save weight, but performance and safety requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Geometry",
            "Material selection",
            "Joining method",
            "Performance",
            "NVH"
        ],
        primary_authority=[
            "OEM performance standards",
            "SAE J2340",
            "Benchmarking data"
        ],
        burden_holder="Performance engineering team",
        adversary_position="Weight reduction advocates may propose reduced stiffness.",
        counter_arguments=[
            "Reduced stiffness compromises performance, NVH, and crash protection.",
            "May lead to customer dissatisfaction."
        ],
        resolution_strategy="Optimize bending stiffness through benchmarking and design validation.",
        entity_scope="AUTO12 performance engineering",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2340: Advanced High Strength Steel Standard"
    ),
    DoctrineBlock(
        topic="body_structure_impact_energy_management",
        keywords=["impact energy management", "body structure", "crash", "safety", "performance"],
        conclusion_template="Impact energy management must be optimized in body structure to maximize crash protection and performance.",
        reasoning_framework=(
            "Impact energy management involves designing body structure features to absorb and dissipate crash energy to maximize occupant protection and performance. "
            "The framework includes evaluating crash performance, energy absorption, and regulatory requirements. Key factors are material selection, geometry, and joining method. "
            "Trade-offs involve balancing energy management with weight and cost. Adversaries may argue for reduced energy management features to save weight, but safety and performance requirements are critical. "
            "Resolution is achieved through benchmarking, design optimization, and validation."
        ),
        key_factors=[
            "Material selection",
            "Geometry",
            "Joining method",
            "Crash performance",
            "Energy absorption"
        ],
        primary_authority=[
            "OEM safety standards",
            "FMVSS 208",
            "Euro NCAP"
        ],
        burden_holder="Safety engineering team",
        adversary_position="Weight reduction advocates may propose reduced energy management features.",
        counter_arguments=[
            "Reduced features compromise crash protection and performance.",
            "May lead to regulatory violations and customer dissatisfaction."
        ],
        resolution_strategy="Optimize impact energy management through benchmarking and validation.",
        entity_scope="AUTO12 safety engineering",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 208: Occupant Crash Protection"
    ),
    DoctrineBlock(
        topic="body_structure_advanced_material_integration",
        keywords=["advanced material", "integration", "body structure", "performance", "manufacturing"],
        conclusion_template="Advanced materials must be integrated into body structure to maximize performance and manufacturing efficiency.",
        reasoning_framework=(
            "Advanced material integration involves selecting and incorporating materials such as AHSS, aluminum, and composites to maximize performance and manufacturing efficiency. "
            "The framework includes evaluating material properties, joining compatibility, and manufacturing process. Key factors are performance, manufacturability, and cost. "
            "Trade-offs involve balancing advanced material integration with cost and manufacturing complexity. Adversaries may argue for traditional materials to reduce cost, but performance and efficiency requirements are critical. "
            "Resolution is achieved through benchmarking, material testing, and process validation."
        ),
        key_factors=[
            "Material properties",
            "Joining compatibility",
            "Manufacturing process",
            "Performance",
            "Cost"
        ],
        primary_authority=[
            "OEM material standards",
            "SAE J2340",
            "Supplier data"
        ],
        burden_holder="Materials engineering team",
        adversary_position="Cost reduction advocates may propose traditional materials.",
        counter_arguments=[
            "Traditional materials may compromise performance and efficiency.",
            "Advanced materials offer significant advantages."
        ],
        resolution_strategy="Optimize advanced material integration through benchmarking and testing.",
        entity_scope="AUTO12 materials engineering",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2340: Advanced High Strength Steel Standard"
    ),
    DoctrineBlock(
        topic="body_structure_assembly_sequence_optimization",
        keywords=["assembly sequence", "optimization", "body structure", "manufacturing", "efficiency"],
        conclusion_template="Assembly sequence must be optimized in body structure manufacturing to maximize efficiency and quality.",
        reasoning_framework=(
            "Assembly sequence optimization involves refining manufacturing steps and process flow to maximize efficiency and quality. "
            "The framework includes evaluating process reliability, equipment utilization, and quality control. Key factors are assembly sequence, efficiency, and quality. "
            "Trade-offs involve balancing assembly sequence optimization with cost and flexibility. Adversaries may argue for traditional assembly sequences to reduce complexity, but efficiency and quality targets are critical. "
            "Resolution is achieved through benchmarking, process optimization, and validation."
        ),
        key_factors=[
            "Assembly sequence",
            "Process reliability",
            "Equipment utilization",
            "Efficiency",
            "Quality"
        ],
        primary_authority=[
            "OEM manufacturing standards",
            "SAE J2178",
            "Benchmarking data"
        ],
        burden_holder="Manufacturing engineering team",
        adversary_position="Traditional sequence advocates may propose minimizing optimization.",
        counter_arguments=[
            "Minimizing optimization may compromise efficiency and quality.",
            "Optimized sequence offers significant advantages."
        ],
        resolution_strategy="Optimize assembly sequence through benchmarking and process validation.",
        entity_scope="AUTO12 manufacturing engineering",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2178: Assembly Sequence Optimization Standard"
    ),
    DoctrineBlock(
        topic="body_structure_automation_flexibility",
        keywords=["automation flexibility", "body structure", "manufacturing", "efficiency", "quality"],
        conclusion_template="Automation flexibility must be implemented in body structure manufacturing to maximize efficiency and adaptability.",
        reasoning_framework=(
            "Automation flexibility involves designing manufacturing processes and equipment to adapt to changing requirements and maximize efficiency. "
            "The framework includes evaluating process reliability, equipment utilization, and adaptability. Key factors are automation, flexibility, and efficiency. "
            "Trade-offs involve balancing automation flexibility with cost and complexity. Adversaries may argue for fixed automation to reduce cost, but flexibility and efficiency targets are critical. "
            "Resolution is achieved through benchmarking, process optimization, and validation."
        ),
        key_factors=[
            "Process reliability",
            "Equipment utilization",
            "Adaptability",
            "Efficiency",
            "Quality"
        ],
        primary_authority=[
            "OEM automation standards",
            "SAE J2178",
            "Benchmarking data"
        ],
        burden_holder="Manufacturing engineering team",
        adversary_position="Fixed automation advocates may propose minimizing flexibility.",
        counter_arguments=[
            "Minimizing flexibility may compromise efficiency and adaptability.",
            "Flexible automation offers significant advantages."
        ],
        resolution_strategy="Optimize automation flexibility through benchmarking and process validation.",
        entity_scope="AUTO12 manufacturing engineering",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2178: Automation Flexibility Standard"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    result = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            result.append(doctrine)
    return result

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]