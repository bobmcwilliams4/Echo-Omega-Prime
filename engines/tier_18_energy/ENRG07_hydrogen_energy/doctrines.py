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
        topic="Green Hydrogen Production via PEM Electrolysis",
        keywords=["green hydrogen", "PEM electrolysis", "renewable energy", "water splitting", "zero-carbon"],
        conclusion_template="Green hydrogen produced via PEM electrolysis using renewable electricity qualifies as zero-carbon hydrogen under current regulatory frameworks.",
        reasoning_framework="""
        1. Assess the source of electricity: Only electricity from renewable sources (wind, solar, hydro) ensures zero-carbon status.
        2. Evaluate PEM electrolyzer efficiency and operational emissions.
        3. Review grid connection and potential for indirect emissions.
        4. Cross-reference with EU RED II, US DOE Clean Hydrogen Standard, and other relevant standards.
        5. Confirm traceability of renewable energy certificates (RECs) or guarantees of origin (GOs).
        6. Consider lifecycle analysis (LCA) for upstream and downstream impacts.
        7. Determine compliance with local and international hydrogen color classification schemes.
        8. Evaluate water sourcing and environmental impact.
        9. Analyze scalability, cost, and supply chain constraints.
        10. Synthesize findings to determine qualification for green hydrogen designation.
        """,
        key_factors=[
            "Electricity source and traceability",
            "Electrolyzer efficiency",
            "Grid emissions factor",
            "Lifecycle GHG emissions",
            "Water sourcing and purity"
        ],
        primary_authority=[
            "EU Renewable Energy Directive II (RED II)",
            "US DOE Clean Hydrogen Production Standard",
            "ISO 22734:2019"
        ],
        burden_holder="Hydrogen producer",
        adversary_position="Hydrogen produced via PEM electrolysis may not be truly zero-carbon if grid electricity is used without proper certification.",
        counter_arguments=[
            "Use of RECs/GOs ensures renewable sourcing.",
            "Lifecycle analysis demonstrates net-zero emissions.",
            "Grid balancing with storage can mitigate indirect emissions."
        ],
        resolution_strategy="Require third-party certification of renewable electricity and periodic lifecycle GHG audits.",
        entity_scope="Hydrogen producers, regulatory agencies, certification bodies",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EU RED II Art. 25; US DOE Clean Hydrogen Standard"
    ),
    DoctrineBlock(
        topic="Blue Hydrogen via Steam Methane Reforming with CCS",
        keywords=["blue hydrogen", "steam methane reforming", "SMR", "carbon capture", "CCS", "fossil hydrogen"],
        conclusion_template="Blue hydrogen produced via SMR with CCS qualifies as low-carbon hydrogen if capture rates exceed regulatory thresholds and lifecycle emissions are below mandated limits.",
        reasoning_framework="""
        1. Determine SMR process emissions and CO2 capture rate.
        2. Evaluate CCS technology effectiveness and permanence of storage.
        3. Review methane leakage rates in upstream natural gas supply.
        4. Compare lifecycle GHG emissions to regulatory thresholds (e.g., <3.4 kg CO2e/kg H2).
        5. Assess monitoring, reporting, and verification (MRV) protocols for CCS.
        6. Examine regulatory definitions of 'low-carbon' or 'blue' hydrogen.
        7. Consider public perception and market acceptance.
        8. Analyze economic feasibility and cost competitiveness.
        9. Synthesize findings to determine qualification for blue hydrogen designation.
        """,
        key_factors=[
            "CO2 capture rate",
            "Methane leakage",
            "Lifecycle GHG emissions",
            "CCS permanence",
            "MRV compliance"
        ],
        primary_authority=[
            "IEA Hydrogen Roadmap",
            "US DOE Clean Hydrogen Standard",
            "ISO/TC 265 Carbon dioxide capture, transportation, and geological storage"
        ],
        burden_holder="Hydrogen producer",
        adversary_position="Blue hydrogen remains carbon-intensive due to upstream methane leakage and incomplete CO2 capture.",
        counter_arguments=[
            "Advanced CCS can achieve >95% capture.",
            "Stringent MRV reduces leakage risk.",
            "Lifecycle emissions can be below green hydrogen in some cases."
        ],
        resolution_strategy="Mandate independent lifecycle GHG assessments and enforce methane leakage limits.",
        entity_scope="Hydrogen producers, CCS operators, regulators",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="US DOE Clean Hydrogen Standard; ISO 27919-1:2022"
    ),
    DoctrineBlock(
        topic="Alkaline Electrolysis Technology",
        keywords=["alkaline electrolysis", "hydrogen production", "electrolyzer", "alkaline cell", "renewable hydrogen"],
        conclusion_template="Alkaline electrolysis is a mature and cost-effective technology for large-scale hydrogen production, but offers lower dynamic response compared to PEM.",
        reasoning_framework="""
        1. Compare efficiency and CAPEX/OPEX of alkaline vs. PEM electrolysis.
        2. Assess scalability and operational flexibility.
        3. Evaluate purity of hydrogen output and water requirements.
        4. Consider integration with intermittent renewable energy sources.
        5. Review safety and maintenance considerations.
        6. Examine regulatory acceptance and market trends.
        7. Synthesize technical and economic findings for deployment decisions.
        """,
        key_factors=[
            "CAPEX/OPEX",
            "Efficiency",
            "Dynamic response",
            "Hydrogen purity",
            "Integration with renewables"
        ],
        primary_authority=[
            "IEA Technology Roadmap: Hydrogen and Fuel Cells",
            "ISO 22734:2019"
        ],
        burden_holder="Project developer",
        adversary_position="Alkaline electrolysis is less suitable for variable renewable integration due to slow ramp rates.",
        counter_arguments=[
            "Hybrid systems can mitigate response limitations.",
            "Lower cost offsets some flexibility constraints.",
            "Recent advances have improved dynamic response."
        ],
        resolution_strategy="Select technology based on project-specific flexibility and cost requirements.",
        entity_scope="Project developers, electrolyzer manufacturers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IEA Hydrogen Projects Database"
    ),
    DoctrineBlock(
        topic="Type IV Compressed Hydrogen Storage at 700 bar",
        keywords=["hydrogen storage", "type IV cylinder", "700 bar", "compressed hydrogen", "high-pressure storage"],
        conclusion_template="Type IV composite cylinders at 700 bar are the industry standard for onboard hydrogen storage in FCEVs, balancing weight, safety, and volumetric efficiency.",
        reasoning_framework="""
        1. Review material properties and burst/working pressure ratings of Type IV cylinders.
        2. Assess compliance with ISO 19881 and SAE J2600.
        3. Evaluate safety features: pressure relief devices, impact resistance, fire testing.
        4. Compare gravimetric and volumetric storage densities.
        5. Examine cost, manufacturability, and recyclability.
        6. Analyze field performance and incident data.
        7. Synthesize technical, safety, and economic considerations.
        """,
        key_factors=[
            "Cylinder material and construction",
            "Pressure rating",
            "Safety features",
            "Storage density",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISO 19881:2018",
            "SAE J2600",
            "UN ECE R134"
        ],
        burden_holder="Vehicle manufacturer",
        adversary_position="700 bar storage increases cost and complexity compared to lower-pressure or alternative storage technologies.",
        counter_arguments=[
            "Higher pressure enables longer driving range.",
            "Composite materials reduce weight.",
            "Safety record is strong with proper design."
        ],
        resolution_strategy="Adopt 700 bar Type IV storage for FCEVs; consider alternatives for stationary or heavy-duty applications.",
        entity_scope="Automotive OEMs, cylinder manufacturers",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 19881:2018; SAE J2600"
    ),
    DoctrineBlock(
        topic="Liquid Hydrogen (LH2) Storage and Boil-Off",
        keywords=["liquid hydrogen", "LH2", "cryogenic storage", "boil-off", "hydrogen liquefaction"],
        conclusion_template="LH2 storage enables high-density hydrogen storage but requires robust boil-off management and cryogenic safety measures.",
        reasoning_framework="""
        1. Evaluate LH2 storage vessel design: insulation, pressure relief, venting.
        2. Quantify boil-off rates under operational and standby conditions.
        3. Assess safety protocols for cryogenic handling and vapor management.
        4. Compare LH2 with compressed and solid-state storage for specific applications.
        5. Review regulatory standards (ISO 21009-2, CGA H-3).
        6. Analyze economic impact of boil-off losses.
        7. Synthesize technical, safety, and economic findings.
        """,
        key_factors=[
            "Boil-off rate",
            "Insulation effectiveness",
            "Cryogenic safety",
            "Storage density",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISO 21009-2:2015",
            "CGA H-3",
            "NFPA 55"
        ],
        burden_holder="Storage operator",
        adversary_position="Boil-off losses and cryogenic hazards make LH2 impractical for many applications.",
        counter_arguments=[
            "Advanced insulation reduces boil-off.",
            "Boil-off gas can be recovered or used.",
            "LH2 is essential for long-range and aerospace applications."
        ],
        resolution_strategy="Implement best-practice boil-off management and safety protocols; select LH2 for applications requiring high energy density.",
        entity_scope="Hydrogen storage operators, transporters",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 21009-2:2015; CGA H-3"
    ),
    DoctrineBlock(
        topic="PEM Fuel Cell Membrane Electrode Assembly (MEA)",
        keywords=["PEM fuel cell", "MEA", "membrane electrode assembly", "proton exchange membrane", "fuel cell stack"],
        conclusion_template="High-performance MEAs are critical for PEM fuel cell efficiency, durability, and cost reduction.",
        reasoning_framework="""
        1. Analyze MEA structure: membrane, catalyst layers, gas diffusion layers.
        2. Evaluate performance metrics: power density, efficiency, durability.
        3. Review degradation mechanisms: catalyst poisoning, membrane thinning, flooding.
        4. Assess material advances: low-PGM catalysts, reinforced membranes.
        5. Compare manufacturing techniques and scalability.
        6. Examine cost breakdown and reduction pathways.
        7. Synthesize technical and economic findings for MEA selection.
        """,
        key_factors=[
            "Catalyst loading and composition",
            "Membrane durability",
            "Manufacturing scalability",
            "Performance metrics",
            "Cost"
        ],
        primary_authority=[
            "DOE Fuel Cell Technologies Office",
            "ISO 14687",
            "SAE J2615"
        ],
        burden_holder="Fuel cell manufacturer",
        adversary_position="High MEA cost and limited durability hinder PEM fuel cell commercialization.",
        counter_arguments=[
            "Low-PGM and non-PGM catalysts reduce cost.",
            "Advanced membranes extend lifetime.",
            "Mass production reduces unit cost."
        ],
        resolution_strategy="Adopt advanced MEA materials and manufacturing; target cost and durability benchmarks.",
        entity_scope="Fuel cell manufacturers, automotive OEMs",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Fuel Cell Technologies Office Technical Targets"
    ),
    DoctrineBlock(
        topic="Solid Oxide Fuel Cell (SOFC) for Stationary Power",
        keywords=["SOFC", "solid oxide fuel cell", "stationary power", "high temperature fuel cell", "distributed generation"],
        conclusion_template="SOFCs offer high efficiency and fuel flexibility for stationary power, but require careful thermal management and long start-up times.",
        reasoning_framework="""
        1. Assess SOFC operating temperature and impact on efficiency.
        2. Evaluate fuel flexibility: natural gas, biogas, hydrogen.
        3. Review degradation mechanisms: thermal cycling, material compatibility.
        4. Analyze system integration: combined heat and power (CHP), grid support.
        5. Examine cost, scalability, and market readiness.
        6. Synthesize technical, economic, and operational considerations.
        """,
        key_factors=[
            "Operating temperature",
            "Fuel flexibility",
            "Thermal management",
            "System integration",
            "Cost"
        ],
        primary_authority=[
            "DOE Fuel Cell Technologies Office",
            "IEA Technology Roadmap: Hydrogen and Fuel Cells"
        ],
        burden_holder="Stationary power provider",
        adversary_position="High temperature and slow start-up limit SOFC use in dynamic applications.",
        counter_arguments=[
            "CHP integration maximizes efficiency.",
            "SOFCs excel in baseload and distributed generation.",
            "Material advances improve cycling tolerance."
        ],
        resolution_strategy="Deploy SOFCs in applications prioritizing efficiency and fuel flexibility over rapid cycling.",
        entity_scope="Stationary power providers, utilities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Fuel Cell Technologies Office Technical Targets"
    ),
    DoctrineBlock(
        topic="Hydrogen Pipeline and Embrittlement per ASME B31.12",
        keywords=["hydrogen pipeline", "embrittlement", "ASME B31.12", "pipeline integrity", "hydrogen transport"],
        conclusion_template="Hydrogen pipelines must comply with ASME B31.12 to mitigate embrittlement and ensure long-term integrity.",
        reasoning_framework="""
        1. Identify materials susceptible to hydrogen embrittlement.
        2. Review ASME B31.12 design and material selection criteria.
        3. Assess operational parameters: pressure, temperature, cycling.
        4. Evaluate inspection and monitoring protocols.
        5. Examine mitigation strategies: coatings, inhibitors, material upgrades.
        6. Analyze incident data and failure modes.
        7. Synthesize findings for pipeline design and operation.
        """,
        key_factors=[
            "Material selection",
            "Operating conditions",
            "Inspection protocols",
            "Mitigation strategies",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.12",
            "API RP 941",
            "ISO 15156"
        ],
        burden_holder="Pipeline operator",
        adversary_position="Existing pipelines may not be suitable for hydrogen due to embrittlement risk.",
        counter_arguments=[
            "Retrofit and material upgrades can enable safe hydrogen transport.",
            "ASME B31.12 provides robust design guidance.",
            "Ongoing monitoring mitigates risk."
        ],
        resolution_strategy="Require ASME B31.12 compliance and periodic integrity assessments for hydrogen pipelines.",
        entity_scope="Pipeline operators, regulators",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.12"
    ),
    DoctrineBlock(
        topic="Hydrogen Refueling Station Design per ISO 19880-1",
        keywords=["hydrogen refueling station", "ISO 19880-1", "station design", "safety", "FCEV"],
        conclusion_template="Hydrogen refueling stations must comply with ISO 19880-1 to ensure safety, reliability, and interoperability.",
        reasoning_framework="""
        1. Review ISO 19880-1 requirements for station layout, equipment, and safety distances.
        2. Assess hydrogen storage, compression, and dispensing systems.
        3. Evaluate safety systems: leak detection, emergency shutdown, fire protection.
        4. Examine interoperability with FCEVs and other stations.
        5. Analyze permitting and regulatory compliance.
        6. Synthesize technical and regulatory requirements for station deployment.
        """,
        key_factors=[
            "Station layout and safety distances",
            "Equipment standards",
            "Safety systems",
            "Interoperability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISO 19880-1:2020",
            "SAE J2601",
            "NFPA 2"
        ],
        burden_holder="Station developer",
        adversary_position="Complex safety and permitting requirements delay station deployment.",
        counter_arguments=[
            "ISO 19880-1 streamlines design and approval.",
            "Standardization reduces risk and cost.",
            "Best practices enable rapid deployment."
        ],
        resolution_strategy="Adopt ISO 19880-1 as baseline for all new hydrogen refueling stations.",
        entity_scope="Station developers, regulators, FCEV OEMs",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 19880-1:2020"
    ),
    DoctrineBlock(
        topic="Hydrogen Safety per NFPA 2",
        keywords=["hydrogen safety", "NFPA 2", "fire code", "hazard mitigation", "emergency response"],
        conclusion_template="NFPA 2 provides the foundational safety code for hydrogen installations in the US, covering storage, handling, and emergency response.",
        reasoning_framework="""
        1. Review NFPA 2 requirements for storage, piping, and equipment.
        2. Assess hazard mitigation: ventilation, leak detection, ignition control.
        3. Evaluate emergency response planning and training.
        4. Examine integration with local fire codes and AHJ requirements.
        5. Analyze incident data and lessons learned.
        6. Synthesize safety and regulatory requirements for hydrogen installations.
        """,
        key_factors=[
            "Storage and handling requirements",
            "Hazard mitigation systems",
            "Emergency response",
            "Code compliance",
            "Incident history"
        ],
        primary_authority=[
            "NFPA 2",
            "NFPA 55",
            "OSHA 1910.103"
        ],
        burden_holder="Facility operator",
        adversary_position="Hydrogen’s unique properties require additional safety measures beyond standard codes.",
        counter_arguments=[
            "NFPA 2 is hydrogen-specific and regularly updated.",
            "Training and best practices mitigate unique hazards.",
            "Integration with local codes ensures comprehensive coverage."
        ],
        resolution_strategy="Mandate NFPA 2 compliance and regular safety training for all hydrogen facilities.",
        entity_scope="Facility operators, emergency responders, AHJs",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 2"
    ),
    DoctrineBlock(
        topic="Levelized Cost of Hydrogen (LCOH) Analysis",
        keywords=["LCOH", "levelized cost", "hydrogen economics", "cost analysis", "project finance"],
        conclusion_template="LCOH provides a standardized metric for comparing hydrogen production pathways, incorporating CAPEX, OPEX, and utilization.",
        reasoning_framework="""
        1. Define system boundaries and time horizon for analysis.
        2. Calculate total CAPEX and OPEX over plant lifetime.
        3. Include feedstock, energy, labor, maintenance, and financing costs.
        4. Factor in plant utilization rate and capacity factor.
        5. Discount future cash flows to present value.
        6. Compare LCOH across production technologies (PEM, alkaline, SMR+CCS, etc.).
        7. Synthesize findings for investment and policy decisions.
        """,
        key_factors=[
            "CAPEX",
            "OPEX",
            "Utilization rate",
            "Discount rate",
            "System boundaries"
        ],
        primary_authority=[
            "IEA Hydrogen Projects Database",
            "DOE H2A Analysis",
            "IEA Levelized Cost Methodology"
        ],
        burden_holder="Project developer",
        adversary_position="LCOH does not capture externalities or market volatility.",
        counter_arguments=[
            "LCOH is a widely accepted financial metric.",
            "Sensitivity analysis can address uncertainties.",
            "Externalities can be included in extended models."
        ],
        resolution_strategy="Use LCOH as baseline, supplemented by scenario and sensitivity analysis.",
        entity_scope="Project developers, investors, policymakers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE H2A Analysis"
    ),
    DoctrineBlock(
        topic="Hydrogen Color Classification and Carbon Intensity",
        keywords=["hydrogen color", "carbon intensity", "green hydrogen", "blue hydrogen", "gray hydrogen"],
        conclusion_template="Hydrogen color classification is based on production method and associated carbon intensity, with regulatory definitions evolving toward quantitative GHG thresholds.",
        reasoning_framework="""
        1. Map production pathways to color codes: green, blue, gray, turquoise, pink, etc.
        2. Review regulatory definitions and thresholds for carbon intensity (e.g., kg CO2e/kg H2).
        3. Assess lifecycle analysis methodologies and system boundaries.
        4. Compare international standards and market requirements.
        5. Evaluate implications for incentives, certification, and trade.
        6. Synthesize findings for project and policy alignment.
        """,
        key_factors=[
            "Production method",
            "Lifecycle GHG emissions",
            "Regulatory definitions",
            "Certification schemes",
            "Market requirements"
        ],
        primary_authority=[
            "EU RED II",
            "US DOE Clean Hydrogen Standard",
            "CertifHy"
        ],
        burden_holder="Hydrogen producer",
        adversary_position="Color codes oversimplify carbon intensity and create market confusion.",
        counter_arguments=[
            "Quantitative thresholds are replacing color codes.",
            "Certification schemes provide clarity.",
            "Lifecycle analysis ensures comparability."
        ],
        resolution_strategy="Adopt carbon intensity thresholds and third-party certification for hydrogen classification.",
        entity_scope="Hydrogen producers, regulators, certifiers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EU RED II; CertifHy"
    ),
    DoctrineBlock(
        topic="Solid-State Hydrogen Storage in Metal Hydrides",
        keywords=["solid-state storage", "metal hydrides", "hydrogen storage", "absorption", "desorption"],
        conclusion_template="Metal hydride storage offers high volumetric density and safety, but is limited by weight and thermal management requirements.",
        reasoning_framework="""
        1. Evaluate storage capacity and kinetics of candidate hydrides.
        2. Assess operating temperature and pressure requirements.
        3. Review safety and handling protocols.
        4. Compare with compressed and liquid storage for target applications.
        5. Analyze cost, scalability, and material availability.
        6. Synthesize technical and economic findings.
        """,
        key_factors=[
            "Storage capacity",
            "Operating conditions",
            "Thermal management",
            "Safety",
            "Cost"
        ],
        primary_authority=[
            "DOE Hydrogen Storage Program",
            "ISO 16111",
            "IEA Hydrogen TCP"
        ],
        burden_holder="Storage system developer",
        adversary_position="Weight and thermal management challenges limit hydride adoption.",
        counter_arguments=[
            "High safety and density for stationary and niche mobile uses.",
            "Advances in material science are improving performance.",
            "Thermal integration can mitigate management issues."
        ],
        resolution_strategy="Deploy metal hydrides in applications prioritizing safety and density over weight.",
        entity_scope="Storage developers, stationary power providers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="DOE Hydrogen Storage Program"
    ),
    DoctrineBlock(
        topic="Hydrogen Fuel Quality per ISO 14687 and SAE J2719",
        keywords=["hydrogen fuel quality", "ISO 14687", "SAE J2719", "impurities", "fuel cell"],
        conclusion_template="Hydrogen for fuel cells must meet ISO 14687 and SAE J2719 purity standards to ensure performance and durability.",
        reasoning_framework="""
        1. Review impurity limits for H2 fuel (CO, CO2, H2O, NH3, etc.).
        2. Assess impact of impurities on fuel cell performance and lifetime.
        3. Evaluate analytical methods for fuel quality verification.
        4. Examine supply chain and delivery system contamination risks.
        5. Analyze regulatory and warranty implications.
        6. Synthesize technical and compliance requirements.
        """,
        key_factors=[
            "Impurity limits",
            "Analytical verification",
            "Supply chain contamination",
            "Fuel cell sensitivity",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISO 14687:2019",
            "SAE J2719",
            "ISO 21087"
        ],
        burden_holder="Hydrogen supplier",
        adversary_position="Strict purity standards increase production and delivery costs.",
        counter_arguments=[
            "High purity is essential for fuel cell durability.",
            "Analytical methods are well-established.",
            "Cost can be reduced with scale and process optimization."
        ],
        resolution_strategy="Mandate ISO 14687 and SAE J2719 compliance for all hydrogen supplied to fuel cell vehicles.",
        entity_scope="Hydrogen suppliers, fuel cell OEMs",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14687:2019; SAE J2719"
    ),
    # Additional doctrines for comprehensive coverage (to reach 40+)
    DoctrineBlock(
        topic="Hydrogen Blending in Natural Gas Pipelines",
        keywords=["hydrogen blending", "natural gas pipeline", "H2NG", "pipeline integrity", "gas grid"],
        conclusion_template="Hydrogen blending up to 20% by volume is feasible in many existing natural gas grids with minimal modifications, but requires case-by-case assessment.",
        reasoning_framework="""
        1. Assess material compatibility and embrittlement risk for pipeline components.
        2. Evaluate impact on end-use appliances and industrial users.
        3. Review regulatory limits and standards for blending (e.g., EN 16726).
        4. Analyze gas quality monitoring and billing implications.
        5. Examine safety, odorization, and leak detection requirements.
        6. Synthesize technical, regulatory, and economic findings.
        """,
        key_factors=[
            "Pipeline material compatibility",
            "End-use appliance tolerance",
            "Regulatory blending limits",
            "Gas quality monitoring",
            "Safety protocols"
        ],
        primary_authority=[
            "EN 16726",
            "CEN/TC 234",
            "IEA Hydrogen TCP"
        ],
        burden_holder="Gas grid operator",
        adversary_position="Hydrogen blending may damage infrastructure and appliances.",
        counter_arguments=[
            "Case studies show up to 20% blending is safe in many systems.",
            "Monitoring and upgrades can mitigate risks.",
            "Blending is a transitional strategy toward full decarbonization."
        ],
        resolution_strategy="Conduct site-specific assessments and adhere to regulatory blending limits.",
        entity_scope="Gas grid operators, regulators, appliance manufacturers",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="EN 16726"
    ),
    DoctrineBlock(
        topic="Hydrogen Permeation and Leakage Control",
        keywords=["hydrogen leakage", "permeation", "pipeline integrity", "environmental impact", "safety"],
        conclusion_template="Hydrogen’s small molecule size increases leakage risk; robust detection and mitigation strategies are essential for safe system operation.",
        reasoning_framework="""
        1. Quantify hydrogen permeation rates for common materials.
        2. Assess environmental and safety impacts of leakage.
        3. Review detection technologies: sensors, mass spectrometry, acoustic monitoring.
        4. Evaluate regulatory leakage limits and reporting requirements.
        5. Analyze best practices for sealing, maintenance, and repair.
        6. Synthesize technical and regulatory findings.
        """,
        key_factors=[
            "Material permeability",
            "Detection technology",
            "Leakage limits",
            "Maintenance protocols",
            "Environmental impact"
        ],
        primary_authority=[
            "ISO 26142",
            "EPA GHGRP",
            "ASME B31.12"
        ],
        burden_holder="System operator",
        adversary_position="Hydrogen leakage undermines climate benefits and increases safety risks.",
        counter_arguments=[
            "Modern sensors enable rapid leak detection.",
            "Best practices minimize leakage.",
            "Regulatory compliance ensures environmental protection."
        ],
        resolution_strategy="Implement continuous monitoring and rapid response protocols for all hydrogen systems.",
        entity_scope="System operators, regulators",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 26142"
    ),
    DoctrineBlock(
        topic="Hydrogen Compression Technology Selection",
        keywords=["hydrogen compression", "compressor", "technology selection", "refueling station", "energy efficiency"],
        conclusion_template="Diaphragm and reciprocating compressors are preferred for hydrogen refueling stations, balancing purity, reliability, and efficiency.",
        reasoning_framework="""
        1. Compare compressor types: diaphragm, reciprocating, ionic liquid, electrochemical.
        2. Assess purity requirements and risk of oil contamination.
        3. Evaluate energy efficiency and maintenance needs.
        4. Review cost, scalability, and operational flexibility.
        5. Examine safety features and failure modes.
        6. Synthesize technical and economic findings for technology selection.
        """,
        key_factors=[
            "Purity requirements",
            "Energy efficiency",
            "Reliability",
            "Cost",
            "Maintenance"
        ],
        primary_authority=[
            "ISO 19880-3",
            "SAE J2601",
            "DOE Hydrogen Refueling Protocols"
        ],
        burden_holder="Station developer",
        adversary_position="Compressor failures are a leading cause of station downtime and high OPEX.",
        counter_arguments=[
            "Diaphragm compressors offer high purity and reliability.",
            "Redundancy and predictive maintenance reduce downtime.",
            "Emerging technologies may further improve performance."
        ],
        resolution_strategy="Select proven compressor technologies and implement robust maintenance protocols.",
        entity_scope="Station developers, compressor OEMs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 19880-3"
    ),
    DoctrineBlock(
        topic="Hydrogen Purification via Pressure Swing Adsorption (PSA)",
        keywords=["hydrogen purification", "PSA", "pressure swing adsorption", "impurities", "purity"],
        conclusion_template="PSA is the industry standard for hydrogen purification, achieving >99.99% purity for fuel cell and industrial applications.",
        reasoning_framework="""
        1. Review PSA process fundamentals and operating parameters.
        2. Assess impurity removal efficiency for CO, CO2, CH4, N2, H2O.
        3. Compare PSA with alternative purification methods (membrane, cryogenic).
        4. Evaluate cost, energy consumption, and scalability.
        5. Examine maintenance and operational reliability.
        6. Synthesize technical and economic findings.
        """,
        key_factors=[
            "Purity requirements",
            "Impurity removal efficiency",
            "Cost and energy use",
            "Reliability",
            "Scalability"
        ],
        primary_authority=[
            "DOE Hydrogen Production Handbook",
            "ISO 14687",
            "IEA Hydrogen TCP"
        ],
        burden_holder="Hydrogen producer",
        adversary_position="PSA is energy-intensive and may not remove all impurities to fuel cell grade.",
        counter_arguments=[
            "PSA achieves required purity for most applications.",
            "Hybrid systems can address specific impurities.",
            "Process optimization reduces energy use."
        ],
        resolution_strategy="Adopt PSA as baseline; supplement with additional purification as needed for fuel cell applications.",
        entity_scope="Hydrogen producers, purification system OEMs",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Hydrogen Production Handbook"
    ),
    DoctrineBlock(
        topic="Hydrogen Liquefaction Energy Consumption",
        keywords=["hydrogen liquefaction", "energy consumption", "cryogenic", "liquid hydrogen", "efficiency"],
        conclusion_template="Hydrogen liquefaction consumes 10-13 kWh/kg H2, representing a significant energy penalty relative to compressed storage.",
        reasoning_framework="""
        1. Quantify energy requirements for major liquefaction processes (Claude, Linde-Hampson, etc.).
        2. Assess pre-cooling, ortho-para conversion, and boil-off management.
        3. Compare with compressed and solid-state storage options.
        4. Evaluate cost implications and carbon footprint.
        5. Analyze advances in process integration and efficiency.
        6. Synthesize technical and economic findings.
        """,
        key_factors=[
            "Process energy consumption",
            "Boil-off management",
            "Cost",
            "Carbon footprint",
            "Process integration"
        ],
        primary_authority=[
            "IEA Hydrogen Projects Database",
            "DOE Hydrogen Program Record",
            "ISO 21009-2"
        ],
        burden_holder="Liquefaction plant operator",
        adversary_position="High energy consumption undermines the climate benefits of LH2.",
        counter_arguments=[
            "Renewable electricity can offset emissions.",
            "Process improvements are reducing energy use.",
            "LH2 is necessary for long-distance transport."
        ],
        resolution_strategy="Prioritize efficiency improvements and renewable energy sourcing for liquefaction plants.",
        entity_scope="Liquefaction plant operators, transporters",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="DOE Hydrogen Program Record 20004"
    ),
    DoctrineBlock(
        topic="Hydrogen Vehicle Crashworthiness and Safety",
        keywords=["hydrogen vehicle", "crashworthiness", "safety", "FCEV", "impact resistance"],
        conclusion_template="Hydrogen vehicles must meet rigorous crashworthiness and safety standards, with Type IV tanks and automated shutoff systems minimizing risk.",
        reasoning_framework="""
        1. Review crash test protocols for hydrogen vehicles (FMVSS, UN ECE R134).
        2. Assess tank integrity under impact, fire, and penetration scenarios.
        3. Evaluate automated safety systems: leak detection, shutoff valves, venting.
        4. Analyze incident data and safety record.
        5. Compare with conventional vehicles for risk assessment.
        6. Synthesize technical and regulatory findings.
        """,
        key_factors=[
            "Tank integrity",
            "Automated safety systems",
            "Crash test compliance",
            "Incident history",
            "Regulatory standards"
        ],
        primary_authority=[
            "FMVSS 304",
            "UN ECE R134",
            "SAE J2579"
        ],
        burden_holder="Vehicle manufacturer",
        adversary_position="Hydrogen tanks may rupture or leak in severe crashes.",
        counter_arguments=[
            "Type IV tanks have exceptional impact resistance.",
            "Automated systems rapidly isolate hydrogen.",
            "Crash data shows low incident rates."
        ],
        resolution_strategy="Mandate compliance with FMVSS 304 and UN ECE R134 for all hydrogen vehicles.",
        entity_scope="Automotive OEMs, regulators",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FMVSS 304; UN ECE R134"
    ),
    DoctrineBlock(
        topic="Hydrogen Embrittlement in Metallic Alloys",
        keywords=["hydrogen embrittlement", "metallic alloys", "pipeline", "failure modes", "material selection"],
        conclusion_template="Material selection per ASME B31.12 and ISO 15156 is critical to prevent hydrogen embrittlement in pipelines and pressure vessels.",
        reasoning_framework="""
        1. Identify susceptible alloys (carbon steel, high-strength steel).
        2. Review embrittlement mechanisms: hydrogen-induced cracking, blistering.
        3. Assess mitigation strategies: alloy selection, coatings, operational controls.
        4. Evaluate inspection and monitoring protocols.
        5. Analyze incident data and failure case studies.
        6. Synthesize technical and regulatory findings.
        """,
        key_factors=[
            "Alloy susceptibility",
            "Mitigation strategies",
            "Inspection protocols",
            "Operational controls",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ASME B31.12",
            "ISO 15156",
            "API RP 941"
        ],
        burden_holder="Pipeline and vessel designer",
        adversary_position="Legacy infrastructure may not meet modern embrittlement standards.",
        counter_arguments=[
            "Retrofit and material upgrades can address risks.",
            "Regular inspection mitigates failure risk.",
            "Standards are evolving to address new findings."
        ],
        resolution_strategy="Require material certification and periodic inspection for all hydrogen infrastructure.",
        entity_scope="Pipeline operators, vessel manufacturers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.12; ISO 15156"
    ),
    DoctrineBlock(
        topic="Hydrogen Permeation in Polymer Liners",
        keywords=["hydrogen permeation", "polymer liner", "Type IV cylinder", "storage tank", "leakage"],
        conclusion_template="Polymer liners in Type IV cylinders must be qualified for hydrogen permeation rates per ISO 11119-3 to ensure long-term safety.",
        reasoning_framework="""
        1. Assess permeation rates for candidate polymers (HDPE, PA, etc.).
        2. Review ISO 11119-3 qualification tests for Type IV liners.
        3. Evaluate impact of temperature, pressure, and aging on permeation.
        4. Analyze field data on liner performance and leakage.
        5. Synthesize technical and regulatory findings for liner selection.
        """,
        key_factors=[
            "Polymer selection",
            "Permeation rate",
            "Qualification testing",
            "Aging effects",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISO 11119-3",
            "ISO 19881",
            "SAE J2579"
        ],
        burden_holder="Cylinder manufacturer",
        adversary_position="Polymer liners may degrade or leak over time, compromising safety.",
        counter_arguments=[
            "Qualification testing ensures long-term integrity.",
            "Advanced polymers have low permeation rates.",
            "Periodic inspection detects early degradation."
        ],
        resolution_strategy="Mandate ISO 11119-3 qualification and periodic inspection for all Type IV cylinders.",
        entity_scope="Cylinder manufacturers, automotive OEMs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 11119-3"
    ),
    DoctrineBlock(
        topic="Hydrogen Refueling Protocols for FCEVs",
        keywords=["hydrogen refueling", "protocol", "FCEV", "SAE J2601", "station interoperability"],
        conclusion_template="SAE J2601 defines standardized hydrogen refueling protocols for light-duty FCEVs, ensuring safety and interoperability.",
        reasoning_framework="""
        1. Review SAE J2601 protocol for pressure, temperature, and flow rate control.
        2. Assess station and vehicle communication requirements.
        3. Evaluate safety interlocks and emergency shutdown systems.
        4. Analyze field data on protocol compliance and interoperability.
        5. Synthesize technical and regulatory findings for station deployment.
        """,
        key_factors=[
            "Pressure and temperature control",
            "Communication protocols",
            "Safety interlocks",
            "Interoperability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "SAE J2601",
            "ISO 19880-1",
            "SAE J2799"
        ],
        burden_holder="Station developer",
        adversary_position="Protocol complexity increases station cost and downtime.",
        counter_arguments=[
            "Standardization reduces risk and improves user experience.",
            "Protocols are evolving to address operational challenges.",
            "Interoperability is essential for market growth."
        ],
        resolution_strategy="Mandate SAE J2601 compliance for all new hydrogen refueling stations.",
        entity_scope="Station developers, FCEV OEMs",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2601"
    ),
    DoctrineBlock(
        topic="Hydrogen Odorization for Leak Detection",
        keywords=["hydrogen odorization", "leak detection", "safety", "odorant", "pipeline"],
        conclusion_template="Odorization of hydrogen is technically challenging and not currently required for most applications due to fuel cell sensitivity and detection alternatives.",
        reasoning_framework="""
        1. Assess impact of odorants on fuel cell performance and catalyst poisoning.
        2. Review technical feasibility of hydrogen odorization.
        3. Evaluate alternative leak detection technologies (sensors, acoustic).
        4. Analyze regulatory requirements for odorization.
        5. Synthesize safety and technical findings for leak detection strategy.
        """,
        key_factors=[
            "Odorant compatibility",
            "Detection technology",
            "Regulatory requirements",
            "Safety",
            "Fuel cell sensitivity"
        ],
        primary_authority=[
            "ISO 26142",
            "NFPA 2",
            "DOE Hydrogen Safety Panel"
        ],
        burden_holder="System operator",
        adversary_position="Lack of odorization increases undetected leak risk.",
        counter_arguments=[
            "Sensors provide rapid and reliable detection.",
            "Odorants can damage fuel cells.",
            "Regulations allow for alternative detection methods."
        ],
        resolution_strategy="Deploy advanced leak detection systems in lieu of odorization for hydrogen pipelines and stations.",
        entity_scope="System operators, regulators",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="ISO 26142"
    ),
    DoctrineBlock(
        topic="Hydrogen Storage Site Selection and Permitting",
        keywords=["hydrogen storage", "site selection", "permitting", "safety", "environmental impact"],
        conclusion_template="Site selection for hydrogen storage must balance safety, environmental, and permitting requirements, with robust risk assessment and community engagement.",
        reasoning_framework="""
        1. Evaluate proximity to population centers, critical infrastructure, and natural hazards.
        2. Assess environmental impact: groundwater, air quality, ecosystem.
        3. Review permitting requirements: local, state, federal.
        4. Analyze emergency response and access considerations.
        5. Engage stakeholders and address public concerns.
        6. Synthesize findings for site selection and permitting decision.
        """,
        key_factors=[
            "Safety distance",
            "Environmental impact",
            "Permitting requirements",
            "Emergency response",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "NFPA 2",
            "EPA NEPA",
            "ISO 19880-1"
        ],
        burden_holder="Storage developer",
        adversary_position="Permitting delays and public opposition hinder project deployment.",
        counter_arguments=[
            "Early engagement reduces opposition.",
            "Best practices streamline permitting.",
            "Comprehensive risk assessment builds trust."
        ],
        resolution_strategy="Follow best-practice site selection and engage stakeholders early in the process.",
        entity_scope="Storage developers, permitting agencies",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 2; EPA NEPA"
    ),
    DoctrineBlock(
        topic="Hydrogen Dispensing Metering and Accuracy",
        keywords=["hydrogen dispensing", "metering", "accuracy", "SAE J2601", "trade"],
        conclusion_template="Hydrogen dispensers must meet metering accuracy requirements per SAE J2601 and OIML R139 to ensure fair trade and customer trust.",
        reasoning_framework="""
        1. Review metering technologies: Coriolis, thermal mass, pressure-based.
        2. Assess calibration and verification protocols.
        3. Evaluate regulatory requirements for accuracy and reporting.
        4. Analyze impact of temperature and pressure on metering.
        5. Synthesize technical and regulatory findings for dispenser selection.
        """,
        key_factors=[
            "Metering technology",
            "Calibration protocols",
            "Regulatory accuracy requirements",
            "Temperature/pressure compensation",
            "Trade compliance"
        ],
        primary_authority=[
            "SAE J2601",
            "OIML R139",
            "ISO 19880-1"
        ],
        burden_holder="Station operator",
        adversary_position="Metering errors undermine consumer confidence and regulatory compliance.",
        counter_arguments=[
            "Modern meters achieve high accuracy.",
            "Regular calibration ensures compliance.",
            "Protocols address compensation for environmental factors."
        ],
        resolution_strategy="Mandate use of certified meters and regular calibration for all hydrogen dispensers.",
        entity_scope="Station operators, regulators",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2601; OIML R139"
    ),
    DoctrineBlock(
        topic="Hydrogen Storage in Salt Caverns",
        keywords=["hydrogen storage", "salt cavern", "geological storage", "underground storage", "bulk storage"],
        conclusion_template="Salt caverns offer cost-effective, large-scale hydrogen storage with proven safety and operational experience.",
        reasoning_framework="""
        1. Evaluate geological suitability of salt formations.
        2. Assess cavern design, leaching, and operational protocols.
        3. Review safety, monitoring, and environmental protection measures.
        4. Compare with alternative storage options (depleted fields, aquifers).
        5. Analyze cost, scalability, and market readiness.
        6. Synthesize technical, economic, and regulatory findings.
        """,
        key_factors=[
            "Geological suitability",
            "Cavern design",
            "Safety and monitoring",
            "Cost and scalability",
            "Environmental impact"
        ],
        primary_authority=[
            "IEA Hydrogen TCP",
            "DOE Hydrogen Storage Program",
            "API RP 1170"
        ],
        burden_holder="Storage operator",
        adversary_position="Geographical limitations restrict salt cavern deployment.",
        counter_arguments=[
            "Salt caverns are available in key hydrogen markets.",
            "Other geological options can supplement storage.",
            "Salt caverns have a strong safety record."
        ],
        resolution_strategy="Prioritize salt cavern storage where geology permits; develop alternatives elsewhere.",
        entity_scope="Storage operators, utilities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 1170"
    ),
    DoctrineBlock(
        topic="Hydrogen Market Certification and Guarantees of Origin",
        keywords=["hydrogen certification", "guarantee of origin", "GO", "CertifHy", "traceability"],
        conclusion_template="Guarantees of Origin (GOs) and certification schemes like CertifHy provide traceability and market differentiation for low-carbon hydrogen.",
        reasoning_framework="""
        1. Review certification scheme requirements (CertifHy, EU RED II, etc.).
        2. Assess traceability of production, transport, and consumption.
        3. Evaluate market acceptance and interoperability.
        4. Analyze regulatory and incentive implications.
        5. Synthesize technical, regulatory, and market findings.
        """,
        key_factors=[
            "Certification scheme requirements",
            "Traceability",
            "Market acceptance",
            "Regulatory compliance",
            "Incentive eligibility"
        ],
        primary_authority=[
            "CertifHy",
            "EU RED II",
            "IEA Hydrogen TCP"
        ],
        burden_holder="Hydrogen producer",
        adversary_position="Certification increases administrative burden and cost.",
        counter_arguments=[
            "Certification enables market access and premium pricing.",
            "Digital platforms streamline certification.",
            "Regulatory incentives depend on certification."
        ],
        resolution_strategy="Adopt recognized certification schemes and digital GOs for all low-carbon hydrogen.",
        entity_scope="Hydrogen producers, traders, regulators",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CertifHy; EU RED II"
    ),
    DoctrineBlock(
        topic="Hydrogen Electrolyzer Stack Lifetime and Degradation",
        keywords=["electrolyzer", "stack lifetime", "degradation", "PEM", "alkaline"],
        conclusion_template="Electrolyzer stack lifetime is a key determinant of project economics, with PEM stacks typically lasting 60,000-80,000 hours and alkaline stacks up to 90,000 hours.",
        reasoning_framework="""
        1. Review degradation mechanisms: catalyst poisoning, membrane thinning, scaling.
        2. Assess impact of operating conditions: current density, cycling, water quality.
        3. Evaluate maintenance and replacement protocols.
        4. Analyze cost implications of stack replacement.
        5. Synthesize technical and economic findings for project planning.
        """,
        key_factors=[
            "Degradation mechanisms",
            "Operating conditions",
            "Maintenance protocols",
            "Stack replacement cost",
            "Project economics"
        ],
        primary_authority=[
            "DOE Hydrogen Program Record",
            "IEA Hydrogen TCP",
            "ISO 22734"
        ],
        burden_holder="Electrolyzer operator",
        adversary_position="Short stack lifetime increases LCOH and project risk.",
        counter_arguments=[
            "Advances in materials are extending stack life.",
            "Predictive maintenance reduces unplanned downtime.",
            "Stack replacement is a manageable OPEX item."
        ],
        resolution_strategy="Incorporate conservative stack lifetime estimates in project models and adopt best-practice maintenance.",
        entity_scope="Electrolyzer operators, project developers",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Hydrogen Program Record 21007"
    ),
    DoctrineBlock(
        topic="Hydrogen Fueling Station Uptime and Reliability",
        keywords=["hydrogen fueling station", "uptime", "reliability", "maintenance", "availability"],
        conclusion_template="High station uptime (>98%) is essential for FCEV adoption, requiring robust maintenance, redundancy, and remote monitoring.",
        reasoning_framework="""
        1. Identify common causes of station downtime (compressor failure, dispenser faults, supply interruptions).
        2. Assess maintenance protocols and spare parts availability.
        3. Evaluate redundancy in critical systems.
        4. Analyze role of remote monitoring and predictive analytics.
        5. Synthesize operational and technical findings for reliability improvement.
        """,
        key_factors=[
            "Maintenance protocols",
            "System redundancy",
            "Remote monitoring",
            "Spare parts availability",
            "Operational analytics"
        ],
        primary_authority=[
            "DOE Hydrogen Refueling Protocols",
            "SAE J2601",
            "ISO 19880-1"
        ],
        burden_holder="Station operator",
        adversary_position="Low reliability discourages FCEV adoption and undermines market confidence.",
        counter_arguments=[
            "Best practices achieve >98% uptime.",
            "Remote diagnostics enable rapid response.",
            "Redundancy mitigates single-point failures."
        ],
        resolution_strategy="Implement robust maintenance, redundancy, and monitoring for all hydrogen stations.",
        entity_scope="Station operators, FCEV OEMs",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Hydrogen Refueling Protocols"
    ),
    DoctrineBlock(
        topic="Hydrogen Fuel Cell System Thermal Management",
        keywords=["fuel cell", "thermal management", "cooling", "system integration", "efficiency"],
        conclusion_template="Effective thermal management is critical for fuel cell performance, lifetime, and safety, requiring integrated cooling and heat rejection systems.",
        reasoning_framework="""
        1. Review heat generation and removal requirements for PEM and SOFC systems.
        2. Assess cooling system design: liquid, air, hybrid.
        3. Evaluate impact on efficiency, durability, and packaging.
        4. Analyze integration with vehicle or building HVAC systems.
        5. Synthesize technical and operational findings for system design.
        """,
        key_factors=[
            "Heat rejection requirements",
            "Cooling system design",
            "Integration with host system",
            "Efficiency impact",
            "Durability"
        ],
        primary_authority=[
            "DOE Fuel Cell Technologies Office",
            "SAE J2578",
            "ISO 14687"
        ],
        burden_holder="Fuel cell system integrator",
        adversary_position="Thermal management adds complexity and cost to fuel cell systems.",
        counter_arguments=[
            "Integrated systems improve efficiency.",
            "Thermal management extends system life.",
            "Design optimization reduces cost and complexity."
        ],
        resolution_strategy="Adopt best-practice thermal management for all fuel cell deployments.",
        entity_scope="Fuel cell system integrators, OEMs",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Fuel Cell Technologies Office Technical Targets"
    ),
    DoctrineBlock(
        topic="Hydrogen Fuel Cell System Start-Up and Freeze Tolerance",
        keywords=["fuel cell", "start-up", "freeze tolerance", "cold weather", "PEM"],
        conclusion_template="PEM fuel cell systems must demonstrate freeze tolerance and rapid start-up per SAE J2719 and OEM requirements for automotive use.",
        reasoning_framework="""
        1. Review start-up protocols and freeze mitigation strategies.
        2. Assess impact of cold weather on performance and durability.
        3. Evaluate system design for water management and insulation.
        4. Analyze field data on cold start reliability.
        5. Synthesize technical and operational findings for automotive deployment.
        """,
        key_factors=[
            "Freeze tolerance",
            "Start-up time",
            "Water management",
            "System insulation",
            "Field reliability"
        ],
        primary_authority=[
            "SAE J2719",
            "DOE Fuel Cell Technologies Office",
            "ISO 14687"
        ],
        burden_holder="Fuel cell OEM",
        adversary_position="Freeze events cause irreversible damage and reduce system life.",
        counter_arguments=[
            "Modern PEM systems achieve rapid cold start.",
            "Water management strategies prevent freeze damage.",
            "Field data supports robust cold weather performance."
        ],
        resolution_strategy="Mandate freeze tolerance and rapid start-up testing for all automotive PEM fuel cells.",
        entity_scope="Fuel cell OEMs, automotive integrators",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SAE J2719"
    ),
    DoctrineBlock(
        topic="Hydrogen Fueling Station Fire Protection",
        keywords=["hydrogen fueling station", "fire protection", "NFPA 2", "safety", "emergency response"],
        conclusion_template="Hydrogen fueling stations must implement fire protection measures per NFPA 2, including separation distances, detection, and suppression systems.",
        reasoning_framework="""
        1. Review NFPA 2 requirements for fire protection at hydrogen stations.
        2. Assess station layout for separation and access.
        3. Evaluate detection, alarm, and suppression systems.
        4. Analyze emergency response protocols and training.
        5. Synthesize technical and regulatory findings for station safety.
        """,
        key_factors=[
            "Separation distance",
            "Detection and alarm systems",
            "Suppression systems",
            "Emergency response",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NFPA 2",
            "ISO 19880-1",
            "DOE Hydrogen Safety Panel"
        ],
        burden_holder="Station operator",
        adversary_position="Fire protection increases station cost and complexity.",
        counter_arguments=[
            "NFPA 2 provides clear, actionable requirements.",
            "Fire protection is essential for public safety.",
            "Best practices minimize incremental cost."
        ],
        resolution_strategy="Mandate NFPA 2 compliance and regular fire protection audits for all hydrogen stations.",
        entity_scope="Station operators, regulators, emergency responders",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 2"
    ),
    DoctrineBlock(
        topic="Hydrogen Fuel Cell System End-of-Life and Recycling",
        keywords=["fuel cell", "end-of-life", "recycling", "PGM recovery", "sustainability"],
        conclusion_template="End-of-life management for fuel cell systems must prioritize recycling of platinum group metals (PGMs) and safe disposal of membranes and components.",
        reasoning_framework="""
        1. Assess recycling technologies for PGMs and other valuable materials.
        2. Review regulatory requirements for hazardous waste disposal.
        3. Evaluate OEM take-back and circular economy programs.
        4. Analyze cost and environmental impact of recycling vs. disposal.
        5. Synthesize technical, regulatory, and economic findings for EOL management.
        """,
        key_factors=[
            "PGM recovery",
            "Hazardous waste management",
            "OEM take-back programs",
            "Cost and environmental impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EU End-of-Life Vehicles Directive",
            "DOE Fuel Cell Technologies Office",
            "ISO 14001"
        ],
        burden_holder="Fuel cell OEM",
        adversary_position="Recycling adds cost and complexity to fuel cell deployment.",
        counter_arguments=[
            "PGM recovery offsets recycling costs.",
            "Circular economy reduces environmental impact.",
            "Regulations require responsible EOL management."
        ],
        resolution_strategy="Mandate OEM take-back and certified recycling for all fuel cell systems.",
        entity_scope="Fuel cell OEMs, recyclers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="EU End-of-Life Vehicles Directive"
    ),
    DoctrineBlock(
        topic="Hydrogen Fuel Cell System Warranty and Performance Guarantees",
        keywords=["fuel cell", "warranty", "performance guarantee", "OEM", "durability"],
        conclusion_template="OEMs must provide warranties and performance guarantees for fuel cell systems, typically covering 5 years or 5,000 hours for automotive applications.",
        reasoning_framework="""
        1. Review industry standard warranty terms for fuel cell systems.
        2. Assess performance guarantee metrics: power output, efficiency, degradation rate.
        3. Evaluate impact of operating conditions and maintenance on warranty claims.
        4. Analyze regulatory and market requirements for warranty disclosure.
        5. Synthesize technical, legal, and commercial findings for warranty policy.
        """,
        key_factors=[
            "Warranty term",
            "Performance metrics",
            "Operating conditions",
            "Maintenance requirements",
            "Regulatory disclosure"
        ],
        primary_authority=[
            "DOE Fuel Cell Technologies Office",
            "SAE J2578",
            "ISO 14687"
        ],
        burden_holder="Fuel cell OEM",
        adversary_position="Warranty claims may be denied due to improper operation or maintenance.",
        counter_arguments=[
            "Clear warranty terms reduce disputes.",
            "OEM training and support minimize improper operation.",
            "Performance guarantees build market confidence."
        ],
        resolution_strategy="Standardize warranty terms and provide clear documentation and support for all customers.",
        entity_scope="Fuel cell OEMs, automotive integrators",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Fuel Cell Technologies Office Technical Targets"
    ),
    DoctrineBlock(
        topic="Hydrogen Fuel Cell System Certification and Type Approval",
        keywords=["fuel cell", "certification", "type approval", "regulatory compliance", "safety"],
        conclusion_template="Fuel cell systems must obtain certification and type approval per regional and international standards prior to market entry.",
        reasoning_framework="""
        1. Review certification requirements for target markets (UN ECE, FMVSS, etc.).
        2. Assess conformity assessment procedures and documentation.
        3. Evaluate testing protocols for safety, performance, and durability.
        4. Analyze impact of certification on time-to-market and cost.
        5. Synthesize technical, regulatory, and commercial findings for certification strategy.
        """,
        key_factors=[
            "Certification requirements",
            "Testing protocols",
            "Documentation",
            "Time-to-market",
            "Regulatory compliance"
        ],
        primary_authority=[
            "UN ECE R134",
            "FMVSS 304",
            "ISO 14687"
        ],
        burden_holder="Fuel cell OEM",
        adversary_position="Certification increases time-to-market and cost.",
        counter_arguments=[
            "Certification ensures safety and market access.",
            "Harmonization reduces duplication.",
            "Early planning streamlines approval."
        ],
        resolution_strategy="Integrate certification planning into product development for all fuel cell systems.",
        entity_scope="Fuel cell OEMs, regulators",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="UN ECE R134; FMVSS 304"
    ),
    DoctrineBlock(
        topic="Hydrogen Fueling Station Data Management and Cybersecurity",
        keywords=["hydrogen fueling station", "data management", "cybersecurity", "IT", "critical infrastructure"],
        conclusion_template="Hydrogen fueling stations must implement robust data management and cybersecurity measures to protect operational integrity and customer data.",
        reasoning_framework="""
        1. Identify critical data streams: metering, payment, station control.
        2. Assess cybersecurity threats and vulnerabilities.
        3. Review regulatory requirements for data protection (NIST, IEC 62443).
        4. Evaluate best practices for access control, encryption, and incident response.
        5. Synthesize technical and regulatory findings for station IT systems.
        """,
        key_factors=[
            "Critical data identification",
            "Threat assessment",
            "Regulatory compliance",
            "Access control",
            "Incident response"
        ],
        primary_authority=[
            "NIST Cybersecurity Framework",
            "IEC 62443",
            "DOE Hydrogen Safety Panel"
        ],
        burden_holder="Station operator",
        adversary_position="Cyberattacks could disrupt station operation or compromise customer data.",
        counter_arguments=[
            "Best practices mitigate cybersecurity risk.",
            "Regulatory compliance ensures minimum standards.",
            "Incident response plans enable rapid recovery."
        ],
        resolution_strategy="Mandate cybersecurity risk assessment and best-practice controls for all hydrogen stations.",
        entity_scope="Station operators, IT vendors",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="NIST Cybersecurity Framework"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Environmental Impact Assessment (EIA)",
        keywords=["hydrogen project", "environmental impact assessment", "EIA", "permitting", "NEPA"],
        conclusion_template="Hydrogen projects must undergo EIA per NEPA or local regulations, addressing air, water, and ecological impacts.",
        reasoning_framework="""
        1. Define project scope and affected environment.
        2. Assess potential impacts: emissions, water use, land disturbance.
        3. Review mitigation measures and alternatives.
        4. Engage stakeholders and solicit public comment.
        5. Synthesize findings for permitting and project approval.
        """,
        key_factors=[
            "Project scope",
            "Impact assessment",
            "Mitigation measures",
            "Stakeholder engagement",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NEPA",
            "EPA EIA Guidelines",
            "ISO 14001"
        ],
        burden_holder="Project developer",
        adversary_position="EIA adds time and cost to project development.",
        counter_arguments=[
            "EIA ensures environmental protection and social license.",
            "Early planning streamlines permitting.",
            "Mitigation measures reduce long-term risk."
        ],
        resolution_strategy="Integrate EIA into project planning and engage stakeholders early.",
        entity_scope="Project developers, permitting agencies",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NEPA"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Financing and Bankability",
        keywords=["hydrogen project", "financing", "bankability", "risk assessment", "investment"],
        conclusion_template="Bankability of hydrogen projects depends on robust risk assessment, offtake agreements, and regulatory stability.",
        reasoning_framework="""
        1. Assess project risks: technology, market, regulatory, supply chain.
        2. Review offtake agreements and revenue certainty.
        3. Evaluate lender and investor requirements.
        4. Analyze impact of policy incentives and market trends.
        5. Synthesize financial, technical, and regulatory findings for bankability assessment.
        """,
        key_factors=[
            "Risk assessment",
            "Offtake agreements",
            "Regulatory stability",
            "Financing structure",
            "Policy incentives"
        ],
        primary_authority=[
            "IEA Hydrogen Projects Database",
            "DOE H2A Analysis",
            "World Bank Guidelines"
        ],
        burden_holder="Project developer",
        adversary_position="Unproven technology and policy uncertainty increase financing risk.",
        counter_arguments=[
            "Long-term offtake contracts reduce risk.",
            "Policy incentives improve project economics.",
            "Risk-sharing structures attract investment."
        ],
        resolution_strategy="Develop robust risk mitigation and secure offtake agreements for all hydrogen projects.",
        entity_scope="Project developers, lenders, investors",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="IEA Hydrogen Projects Database"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Insurance and Risk Transfer",
        keywords=["hydrogen project", "insurance", "risk transfer", "liability", "project finance"],
        conclusion_template="Comprehensive insurance and risk transfer mechanisms are essential for hydrogen project bankability and stakeholder confidence.",
        reasoning_framework="""
        1. Identify insurable project risks: construction, operation, liability, environmental.
        2. Assess available insurance products and coverage limits.
        3. Review contractual risk transfer mechanisms (EPC, O&M, offtake).
        4. Evaluate impact of insurance on project finance and lender requirements.
        5. Synthesize legal, financial, and operational findings for risk management.
        """,
        key_factors=[
            "Insurable risks",
            "Coverage limits",
            "Contractual risk transfer",
            "Lender requirements",
            "Project finance"
        ],
        primary_authority=[
            "World Bank Guidelines",
            "IEA Hydrogen Projects Database",
            "DOE H2A Analysis"
        ],
        burden_holder="Project developer",
        adversary_position="Insurance is costly and may exclude key hydrogen risks.",
        counter_arguments=[
            "Specialized products are emerging for hydrogen.",
            "Risk transfer reduces exposure for all parties.",
            "Lenders require comprehensive coverage."
        ],
        resolution_strategy="Engage insurance specialists early and structure contracts for optimal risk transfer.",
        entity_scope="Project developers, insurers, lenders",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="World Bank Guidelines"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Stakeholder Engagement and Social License",
        keywords=["hydrogen project", "stakeholder engagement", "social license", "community", "public acceptance"],
        conclusion_template="Early and transparent stakeholder engagement is critical for hydrogen project success and social license to operate.",
        reasoning_framework="""
        1. Identify all relevant stakeholders: community, regulators, NGOs, customers.
        2. Assess potential concerns and impacts.
        3. Develop engagement plan: meetings, information sessions, feedback channels.
        4. Review regulatory requirements for public consultation.
        5. Synthesize findings for project planning and risk management.
        """,
        key_factors=[
            "Stakeholder identification",
            "Engagement plan",
            "Public consultation",
            "Risk management",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISO 26000",
            "EPA NEPA",
            "World Bank Guidelines"
        ],
        burden_holder="Project developer",
        adversary_position="Public opposition can delay or derail projects.",
        counter_arguments=[
            "Early engagement builds trust.",
            "Transparent communication reduces opposition.",
            "Best practices streamline permitting."
        ],
        resolution_strategy="Integrate stakeholder engagement into project planning from the outset.",
        entity_scope="Project developers, permitting agencies",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 26000"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Supply Chain and Critical Materials",
        keywords=["hydrogen project", "supply chain", "critical materials", "PGM", "resilience"],
        conclusion_template="Supply chain resilience and secure access to critical materials (e.g., PGMs, membranes) are essential for hydrogen project delivery.",
        reasoning_framework="""
        1. Identify critical supply chain components and materials.
        2. Assess risk of supply disruption and price volatility.
        3. Review sourcing strategies: diversification, recycling, local content.
        4. Evaluate impact on project schedule and cost.
        5. Synthesize findings for supply chain risk management.
        """,
        key_factors=[
            "Critical material identification",
            "Supply disruption risk",
            "Sourcing strategies",
            "Project schedule impact",
            "Cost management"
        ],
        primary_authority=[
            "DOE Critical Materials Strategy",
            "IEA Hydrogen TCP",
            "ISO 14001"
        ],
        burden_holder="Project developer",
        adversary_position="Material shortages and price spikes can delay projects.",
        counter_arguments=[
            "Diversified sourcing reduces risk.",
            "Recycling and circular economy improve resilience.",
            "Long-term contracts stabilize supply."
        ],
        resolution_strategy="Develop supply chain risk management plans for all hydrogen projects.",
        entity_scope="Project developers, OEMs, suppliers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="DOE Critical Materials Strategy"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Workforce Training and Certification",
        keywords=["hydrogen project", "workforce training", "certification", "safety", "competence"],
        conclusion_template="Comprehensive workforce training and certification are required for safe and effective hydrogen project delivery and operation.",
        reasoning_framework="""
        1. Identify required skills and competencies for project roles.
        2. Review available training and certification programs.
        3. Assess regulatory and industry requirements for workforce qualification.
        4. Evaluate impact of training on safety and performance.
        5. Synthesize findings for project HR planning.
        """,
        key_factors=[
            "Skill and competency requirements",
            "Training programs",
            "Certification standards",
            "Safety and performance impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "DOE Hydrogen Safety Panel",
            "ISO 29990",
            "NFPA 2"
        ],
        burden_holder="Project developer",
        adversary_position="Training increases project cost and schedule.",
        counter_arguments=[
            "Training reduces safety incidents.",
            "Certification ensures competence.",
            "Best practices improve project outcomes."
        ],
        resolution_strategy="Mandate certified training for all hydrogen project personnel.",
        entity_scope="Project developers, contractors, operators",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DOE Hydrogen Safety Panel"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Intellectual Property and Technology Licensing",
        keywords=["hydrogen project", "intellectual property", "technology licensing", "patent", "innovation"],
        conclusion_template="IP management and technology licensing are critical for hydrogen project success, requiring clear agreements and freedom-to-operate analysis.",
        reasoning_framework="""
        1. Identify relevant IP and technology for the project.
        2. Assess patent landscape and freedom-to-operate.
        3. Review licensing agreements and terms.
        4. Evaluate impact of IP on project cost and schedule.
        5. Synthesize findings for project legal and commercial planning.
        """,
        key_factors=[
            "IP identification",
            "Patent landscape",
            "Licensing terms",
            "Cost and schedule impact",
            "Legal compliance"
        ],
        primary_authority=[
            "WIPO Patent Landscape Reports",
            "DOE Hydrogen Program",
            "ISO 14001"
        ],
        burden_holder="Project developer",
        adversary_position="IP disputes can delay or block project delivery.",
        counter_arguments=[
            "Early FTO analysis reduces risk.",
            "Clear licensing agreements enable technology access.",
            "IP management supports innovation."
        ],
        resolution_strategy="Conduct FTO analysis and secure necessary licenses before project execution.",
        entity_scope="Project developers, legal counsel, licensors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="WIPO Patent Landscape Reports"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Decommissioning and Site Restoration",
        keywords=["hydrogen project", "decommissioning", "site restoration", "closure", "environmental liability"],
        conclusion_template="Decommissioning and site restoration plans are required for all hydrogen projects to manage environmental liability and regulatory compliance.",
        reasoning_framework="""
        1. Define project end-of-life and decommissioning triggers.
        2. Assess regulatory requirements for closure and restoration.
        3. Review technical protocols for equipment removal and site remediation.
        4. Evaluate cost and liability management strategies.
        5. Synthesize findings for project closure planning.
        """,
        key_factors=[
            "Decommissioning triggers",
            "Regulatory requirements",
            "Technical protocols",
            "Cost and liability management",
            "Environmental impact"
        ],
        primary_authority=[
            "EPA NEPA",
            "ISO 14001",
            "DOE Hydrogen Program"
        ],
        burden_holder="Project developer",
        adversary_position="Decommissioning adds cost and complexity to project planning.",
        counter_arguments=[
            "Early planning reduces closure risk.",
            "Regulatory compliance avoids penalties.",
            "Best practices minimize environmental impact."
        ],
        resolution_strategy="Develop decommissioning and restoration plans as part of project permitting.",
        entity_scope="Project developers, permitting agencies",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA NEPA"
    ),
    DoctrineBlock(
        topic="Hydrogen Project Monitoring, Reporting, and Verification (MRV)",
        keywords=["hydrogen project", "monitoring", "reporting", "verification", "MRV", "GHG emissions"],
        conclusion_template="Robust MRV systems are essential for regulatory compliance, carbon intensity certification, and market access for hydrogen projects.",
        reasoning_framework="""
        1. Define MRV requirements for project scope and regulatory context.
        2. Assess data collection, management, and reporting protocols.
        3. Review third-party verification and audit procedures.
        4. Evaluate impact of MRV on certification and incentives.
        5. Synthesize findings for project compliance and market strategy.
        """,
        key_factors=[
            "MRV requirements",
            "Data management",
            "Third-party verification",
            "Certification impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EU RED II",
            "ISO 14064",
            "DOE Hydrogen Program"
        ],
        burden_holder="Project developer",
        adversary_position="MRV increases administrative burden and cost.",
        counter_arguments=[
            "MRV is required for certification and incentives.",
            "Digital platforms streamline reporting.",
            "Verification builds market trust."
        ],
        resolution_strategy="Integrate MRV systems into project design and operations.",
        entity_scope="Project developers, certifiers, regulators",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EU RED II; ISO 14064"
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in kw.lower() for kw in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]