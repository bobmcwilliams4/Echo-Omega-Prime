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
        topic="Northern White Sand vs Regional Brown Sand Selection",
        keywords=["northern white sand", "regional brown sand", "proppant selection", "conductivity", "crush resistance"],
        conclusion_template="Select {proppant_type} based on required conductivity, cost, and logistical constraints.",
        reasoning_framework="""
        1. Evaluate required fracture conductivity for the target formation.
        2. Compare the conductivity and crush resistance of Northern White Sand (NWS) versus Regional Brown Sand (RBS) using API RP 19C/ISO 13503-2 data.
        3. Assess cost differential, including mine-gate price, transportation, and in-basin delivery.
        4. Consider operational logistics: proximity to wellsite, supply chain reliability, and storage.
        5. Account for regulatory and environmental constraints for each source.
        6. Analyze historical well performance data for similar formations using both sand types.
        7. Consider impact of fines generation and long-term conductivity degradation.
        8. Weigh client/operator risk tolerance for lower-cost, potentially lower-quality RBS.
        9. Make selection based on net present value (NPV) of expected production uplift versus cost.
        """,
        key_factors=[
            "Conductivity at closure stress",
            "Crush resistance",
            "Cost per ton delivered",
            "Logistics and supply reliability",
            "Historical performance data",
            "Fines generation potential",
            "Environmental and regulatory factors"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 184880",
            "Operator offset well data"
        ],
        burden_holder="Proppant Selection Engineer",
        adversary_position="Northern White Sand is always superior due to higher conductivity.",
        counter_arguments=[
            "Regional Brown Sand may be sufficient at lower closure stresses.",
            "Cost savings from RBS may outweigh marginal conductivity loss.",
            "Recent studies show minimal production difference in some basins."
        ],
        resolution_strategy="Conduct basin-specific technical and economic analysis, referencing API/ISO test data and offset well performance.",
        entity_scope="Unconventional completions in North America",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 184880, API RP 19C"
    ),
    DoctrineBlock(
        topic="Mesh Size Selection: 20/40 vs 30/50 vs 40/70 vs 100 Mesh",
        keywords=["mesh size", "20/40", "30/50", "40/70", "100 mesh", "proppant sizing", "conductivity"],
        conclusion_template="Select mesh size {mesh_size} based on formation permeability, closure stress, and desired conductivity.",
        reasoning_framework="""
        1. Determine formation permeability and expected closure stress.
        2. Reference API RP 19C/ISO 13503-2 conductivity tables for each mesh size.
        3. For low-permeability formations, smaller mesh (40/70, 100 mesh) may improve proppant transport and fracture penetration.
        4. For higher-permeability or higher-stress formations, coarser mesh (20/40, 30/50) provides higher conductivity.
        5. Evaluate fines migration risk; finer mesh may exacerbate fines production.
        6. Consider operational constraints: pumping equipment, screen-out risk, and proppant supply.
        7. Review offset well performance for mesh size optimization.
        8. Balance conductivity, transportability, and cost in final selection.
        """,
        key_factors=[
            "Formation permeability",
            "Closure stress",
            "Conductivity at stress",
            "Proppant transportability",
            "Fines migration risk",
            "Operational constraints"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 194334",
            "Operator mesh size guidelines"
        ],
        burden_holder="Completions Engineer",
        adversary_position="Coarser mesh always yields better production due to higher conductivity.",
        counter_arguments=[
            "Finer mesh may improve fracture penetration and proppant placement.",
            "Transportability in slickwater is better with smaller mesh.",
            "Production uplift from coarser mesh may be marginal in tight formations."
        ],
        resolution_strategy="Match mesh size to formation and operational parameters, referencing API/ISO data and field results.",
        entity_scope="Hydraulic fracturing in unconventional reservoirs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 19C, SPE 194334"
    ),
    DoctrineBlock(
        topic="Resin-Coated Sand (RCS) for Flowback Control",
        keywords=["resin-coated sand", "RCS", "flowback control", "proppant flowback", "resin"],
        conclusion_template="Apply RCS as tail-in or full-stage proppant when flowback risk is high or regulatory requirements dictate.",
        reasoning_framework="""
        1. Assess risk of proppant flowback based on formation properties, proppant size, and fracture design.
        2. Review regulatory requirements for proppant flowback control.
        3. Evaluate cost-benefit of RCS versus uncoated sand or alternative flowback control methods.
        4. Consider RCS placement strategies: tail-in (last stages), full-stage, or hybrid.
        5. Reference API RP 19C/ISO 13503-2 for RCS performance metrics.
        6. Analyze historical flowback data and offset well results.
        7. Consider operational impacts: pumpability, screen-out risk, and cleanup.
        8. Select RCS application method that minimizes flowback risk with acceptable economics.
        """,
        key_factors=[
            "Flowback risk",
            "Regulatory requirements",
            "RCS cost premium",
            "Placement strategy",
            "Operational impacts",
            "Historical flowback data"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 169101",
            "State regulatory agencies"
        ],
        burden_holder="Completions Engineer",
        adversary_position="RCS is unnecessary; flowback can be managed operationally.",
        counter_arguments=[
            "RCS reduces risk of costly proppant flowback and equipment damage.",
            "Regulatory compliance may require RCS.",
            "Operational mitigation may not be sufficient in high-risk formations."
        ],
        resolution_strategy="Apply RCS selectively based on risk assessment and regulatory requirements.",
        entity_scope="Unconventional completions with flowback risk",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 19C, SPE 169101"
    ),
    DoctrineBlock(
        topic="Ceramic Proppants: Lightweight, Intermediate, High-Strength",
        keywords=["ceramic proppant", "lightweight", "intermediate", "high-strength", "conductivity", "closure stress"],
        conclusion_template="Select ceramic proppant type based on closure stress and required long-term conductivity.",
        reasoning_framework="""
        1. Determine expected closure stress in the target formation.
        2. Reference API RP 19C/ISO 13503-2 conductivity and crush resistance data for each ceramic type.
        3. Lightweight ceramics are suitable for moderate closure stress (6,000-10,000 psi).
        4. Intermediate ceramics are used for closure stress up to 12,000 psi.
        5. High-strength ceramics are required for closure stress above 12,000 psi.
        6. Assess cost differential versus natural sand and production uplift potential.
        7. Consider proppant transportability in the chosen fluid system.
        8. Evaluate historical well performance with ceramic proppants in similar formations.
        """,
        key_factors=[
            "Closure stress",
            "Conductivity at stress",
            "Crush resistance",
            "Cost per ton delivered",
            "Production uplift potential",
            "Proppant transportability"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 140753",
            "Manufacturer technical data"
        ],
        burden_holder="Proppant Selection Engineer",
        adversary_position="Ceramic proppants are too costly and rarely justified.",
        counter_arguments=[
            "Ceramics provide superior conductivity at high stress.",
            "Production uplift may justify cost in deep, high-stress formations.",
            "Natural sand may fail at required stress levels."
        ],
        resolution_strategy="Justify ceramic selection with stress analysis and economic modeling.",
        entity_scope="High-stress unconventional and deep conventional reservoirs",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 19C, SPE 140753"
    ),
    DoctrineBlock(
        topic="Proppant Concentration (PPA) Scheduling and Ramp Design",
        keywords=["proppant concentration", "PPA", "ramp schedule", "hydraulic fracturing", "stimulation design"],
        conclusion_template="Design PPA ramp schedule to optimize fracture geometry, minimize screen-out risk, and maximize production.",
        reasoning_framework="""
        1. Define target fracture geometry and expected proppant volume.
        2. Establish initial low PPA to ensure proppant transport and minimize screen-out risk.
        3. Gradually ramp PPA according to fluid viscosity, fracture width, and proppant transport capacity.
        4. Reference offset well data for optimal ramp rates and maximum PPA.
        5. Monitor pressure response during treatment to adjust ramp as needed.
        6. Consider operational constraints: blender capacity, pump rate, and proppant supply.
        7. Use simulation tools (e.g., GOHFER, FracPro) to validate ramp design.
        8. Document and review post-job performance for continuous improvement.
        """,
        key_factors=[
            "Target fracture geometry",
            "Initial and maximum PPA",
            "Fluid viscosity",
            "Proppant transport capacity",
            "Operational constraints",
            "Offset well data"
        ],
        primary_authority=[
            "SPE 187451",
            "Frac simulation software",
            "Operator best practices"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="Aggressive PPA ramp maximizes proppant placement and production.",
        counter_arguments=[
            "Excessive ramp rates increase screen-out risk.",
            "Optimal ramp balances transportability and placement.",
            "Offset data may indicate lower maximum PPA is more effective."
        ],
        resolution_strategy="Calibrate ramp schedule using simulation, field data, and operational feedback.",
        entity_scope="Hydraulic fracturing operations",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 187451"
    ),
    DoctrineBlock(
        topic="API RP 19C / ISO 13503-2 Proppant Testing and Specifications",
        keywords=["API RP 19C", "ISO 13503-2", "proppant testing", "specifications", "quality control"],
        conclusion_template="Procure and qualify proppant only from sources meeting API RP 19C/ISO 13503-2 specifications.",
        reasoning_framework="""
        1. Require proppant suppliers to provide API RP 19C/ISO 13503-2 test reports for each lot.
        2. Verify key parameters: sphericity, roundness, crush resistance, acid solubility, turbidity, bulk density.
        3. Conduct independent third-party testing for quality assurance.
        4. Reject proppant lots failing to meet minimum specifications.
        5. Maintain documentation for regulatory and operational audits.
        6. Reference API/ISO standards for dispute resolution with suppliers.
        7. Continuously monitor supplier performance and quality trends.
        """,
        key_factors=[
            "Sphericity and roundness",
            "Crush resistance",
            "Acid solubility",
            "Turbidity",
            "Bulk density",
            "Supplier quality control"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "Operator procurement policy"
        ],
        burden_holder="Procurement and Quality Control",
        adversary_position="Field performance is more important than strict adherence to API/ISO specs.",
        counter_arguments=[
            "API/ISO compliance ensures baseline quality and performance.",
            "Non-compliant proppant increases operational and production risk.",
            "Regulatory and contractual obligations require specification adherence."
        ],
        resolution_strategy="Enforce strict API/ISO compliance for all proppant procurement.",
        entity_scope="All proppant supply chains",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="API RP 19C, ISO 13503-2"
    ),
    DoctrineBlock(
        topic="Proppant Transport and Settling in Non-Newtonian Fluids",
        keywords=["proppant transport", "settling", "non-newtonian fluids", "fracturing fluids", "viscosity"],
        conclusion_template="Optimize fluid rheology and injection rate to maximize proppant transport and minimize settling.",
        reasoning_framework="""
        1. Characterize fracturing fluid rheology (e.g., power-law index, yield stress).
        2. Calculate proppant settling velocity using Stokes' Law or empirical correlations for non-Newtonian fluids.
        3. Increase fluid viscosity or use crosslinked gels to enhance proppant suspension.
        4. Optimize injection rate to maintain turbulent or pseudo-plug flow for improved transport.
        5. Use simulation tools to model proppant transport and placement.
        6. Monitor real-time pressure and proppant concentration for screen-out risk.
        7. Adjust fluid system or pumping schedule as needed based on field response.
        """,
        key_factors=[
            "Fluid rheology",
            "Proppant size and density",
            "Injection rate",
            "Fracture width",
            "Settling velocity",
            "Simulation results"
        ],
        primary_authority=[
            "SPE 169101",
            "Frac simulation software",
            "API RP 19C"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="High-rate slickwater is always sufficient for proppant transport.",
        counter_arguments=[
            "Low-viscosity fluids may allow excessive settling in wide fractures.",
            "Non-Newtonian fluids require tailored transport models.",
            "Screen-out risk increases with poor transport."
        ],
        resolution_strategy="Model and optimize fluid/proppant system for each job using simulation and field data.",
        entity_scope="Hydraulic fracturing with non-Newtonian fluids",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE 169101"
    ),
    DoctrineBlock(
        topic="Proppant Embedment in Soft Formations",
        keywords=["proppant embedment", "soft formation", "closure stress", "conductivity loss", "formation modulus"],
        conclusion_template="Mitigate proppant embedment by selecting harder proppant and/or using resin coatings in soft formations.",
        reasoning_framework="""
        1. Assess formation Young's modulus and closure stress.
        2. Estimate embedment depth using empirical or analytical models (e.g., Gidley, API RP 19C).
        3. Select proppant with higher hardness (e.g., ceramic, RCS) for soft formations.
        4. Consider resin coatings to reduce embedment and fines generation.
        5. Evaluate impact on long-term conductivity and production.
        6. Reference offset well data for embedment-related production loss.
        7. Balance cost of harder proppant against expected production uplift.
        """,
        key_factors=[
            "Formation modulus",
            "Closure stress",
            "Proppant hardness",
            "Embedment depth",
            "Long-term conductivity",
            "Offset well data"
        ],
        primary_authority=[
            "API RP 19C",
            "SPE 140753",
            "Gidley et al., 1989"
        ],
        burden_holder="Completions Engineer",
        adversary_position="Embedment is negligible and does not justify higher-cost proppant.",
        counter_arguments=[
            "Soft formations are prone to significant embedment and conductivity loss.",
            "Resin coatings and ceramics mitigate embedment.",
            "Production loss from embedment can outweigh cost savings."
        ],
        resolution_strategy="Quantify embedment risk and select proppant accordingly.",
        entity_scope="Soft and unconsolidated formations",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 19C, Gidley et al."
    ),
    DoctrineBlock(
        topic="Fines Migration and Proppant Pack Damage",
        keywords=["fines migration", "proppant pack", "damage", "conductivity loss", "formation fines"],
        conclusion_template="Mitigate fines migration by optimizing mesh size, fluid chemistry, and considering RCS or ceramics.",
        reasoning_framework="""
        1. Characterize formation and proppant pack fines content.
        2. Assess risk of fines migration during flowback and production.
        3. Optimize mesh size to minimize fines generation.
        4. Use fluid additives (e.g., clay stabilizers, surfactants) to control fines release.
        5. Consider resin-coated or ceramic proppants to reduce fines movement.
        6. Reference API RP 19C/ISO 13503-2 conductivity loss data.
        7. Monitor post-frac production for fines-related issues.
        """,
        key_factors=[
            "Fines content",
            "Mesh size",
            "Fluid chemistry",
            "Proppant type",
            "Conductivity loss",
            "Production monitoring"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 169101"
        ],
        burden_holder="Completions and Production Engineer",
        adversary_position="Fines migration is unavoidable and cannot be mitigated.",
        counter_arguments=[
            "Proper mesh size and fluid chemistry reduce fines migration.",
            "RCS and ceramics provide additional control.",
            "Field data supports fines mitigation strategies."
        ],
        resolution_strategy="Implement integrated approach using mesh, fluids, and proppant selection.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="API RP 19C, SPE 169101"
    ),
    DoctrineBlock(
        topic="Long-Term Conductivity Degradation: Crush, Embedment, Diagenesis",
        keywords=["long-term conductivity", "degradation", "crush", "embedment", "diagenesis", "proppant pack"],
        conclusion_template="Select proppant and treatment design to minimize long-term conductivity loss from crush, embedment, and diagenesis.",
        reasoning_framework="""
        1. Evaluate closure stress and formation properties.
        2. Reference API RP 19C/ISO 13503-2 long-term conductivity data.
        3. Select proppant with appropriate crush resistance and hardness.
        4. Consider resin coatings or ceramics in high-risk environments.
        5. Assess risk of chemical alteration (diagenesis) from formation fluids.
        6. Use laboratory testing to simulate long-term exposure.
        7. Monitor offset well performance for evidence of conductivity loss.
        8. Balance cost of premium proppant against production sustainability.
        """,
        key_factors=[
            "Closure stress",
            "Proppant crush resistance",
            "Embedment risk",
            "Diagenetic alteration",
            "Long-term conductivity data",
            "Offset well performance"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 140753"
        ],
        burden_holder="Proppant Selection Engineer",
        adversary_position="Short-term conductivity is sufficient for economic production.",
        counter_arguments=[
            "Long-term conductivity loss can significantly impact well economics.",
            "Premium proppant mitigates degradation.",
            "Laboratory and field data support long-term focus."
        ],
        resolution_strategy="Prioritize long-term conductivity in proppant and design selection.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 19C, SPE 140753"
    ),
    DoctrineBlock(
        topic="In-Basin Sand Mines and Proppant Logistics Optimization",
        keywords=["in-basin sand", "logistics", "supply chain", "proppant delivery", "cost optimization"],
        conclusion_template="Utilize in-basin sand mines when quality and logistics meet operational requirements and cost targets.",
        reasoning_framework="""
        1. Assess quality of in-basin sand versus distant sources using API RP 19C/ISO 13503-2 data.
        2. Evaluate logistics: mine-to-wellsite distance, transportation mode, and delivery reliability.
        3. Analyze cost savings from reduced transportation and storage.
        4. Consider supply chain risks: weather, infrastructure, and market volatility.
        5. Monitor in-basin sand performance in offset wells.
        6. Balance cost savings against potential quality or supply risks.
        7. Develop contingency plans for supply disruptions.
        """,
        key_factors=[
            "Sand quality",
            "Logistics and delivery reliability",
            "Cost per ton delivered",
            "Supply chain risk",
            "Offset well performance",
            "Contingency planning"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 184880"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="In-basin sand is always preferable due to cost.",
        counter_arguments=[
            "Quality or supply issues may negate cost savings.",
            "Distant sources may provide superior performance.",
            "Supply chain disruptions can impact operations."
        ],
        resolution_strategy="Continuously monitor quality and logistics to ensure operational targets are met.",
        entity_scope="Unconventional completions in North America",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Proppant Concentration per Lateral Foot Optimization",
        keywords=["proppant concentration", "lateral foot", "optimization", "stimulation design", "production uplift"],
        conclusion_template="Optimize proppant per lateral foot to maximize production while controlling costs and operational risk.",
        reasoning_framework="""
        1. Analyze historical production data versus proppant per lateral foot (PPLF).
        2. Model fracture geometry and proppant distribution using simulation tools.
        3. Identify diminishing returns on production uplift at higher PPLF.
        4. Consider operational constraints: blender capacity, supply, and screen-out risk.
        5. Balance increased cost against expected incremental production.
        6. Reference operator and basin-specific best practices.
        7. Adjust PPLF based on continuous improvement and field results.
        """,
        key_factors=[
            "Historical production data",
            "Fracture geometry",
            "Proppant distribution",
            "Operational constraints",
            "Cost-benefit analysis",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 194334",
            "Frac simulation software",
            "Operator best practices"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="More proppant always yields higher production.",
        counter_arguments=[
            "Diminishing returns at high PPLF.",
            "Operational risks and costs increase with higher PPLF.",
            "Field data may not support unlimited proppant loading."
        ],
        resolution_strategy="Use data-driven optimization for each well and basin.",
        entity_scope="Unconventional horizontal wells",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 194334"
    ),
    DoctrineBlock(
        topic="Tail-In Strategy with Higher Concentration Proppant",
        keywords=["tail-in", "high concentration", "proppant", "fracture tip", "flowback control"],
        conclusion_template="Apply tail-in with higher concentration proppant to improve tip screen-out and flowback control.",
        reasoning_framework="""
        1. Design tail-in stages with increased proppant concentration and/or resin-coated proppant.
        2. Target tail-in to the final 10-20% of total proppant volume.
        3. Reference offset well performance for tail-in effectiveness.
        4. Monitor pressure response during tail-in to avoid screen-out.
        5. Evaluate cost and operational impact of tail-in strategy.
        6. Adjust tail-in design based on field results and continuous improvement.
        """,
        key_factors=[
            "Tail-in concentration",
            "Proppant type",
            "Screen-out risk",
            "Flowback control",
            "Operational impact",
            "Offset well data"
        ],
        primary_authority=[
            "SPE 169101",
            "Operator best practices"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="Tail-in is unnecessary and increases operational complexity.",
        counter_arguments=[
            "Tail-in improves fracture tip packing and reduces flowback.",
            "Operational impact is manageable with proper design.",
            "Field data supports tail-in benefits."
        ],
        resolution_strategy="Apply tail-in selectively and monitor results for optimization.",
        entity_scope="Hydraulic fracturing operations",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 169101"
    ),
    # Additional 30+ DoctrineBlocks with real domain content follow:
    DoctrineBlock(
        topic="Proppant Supply Chain Risk Management",
        keywords=["proppant supply", "logistics", "risk management", "inventory", "contingency planning"],
        conclusion_template="Implement robust supply chain risk management protocols to ensure proppant availability.",
        reasoning_framework="""
        1. Identify critical supply chain nodes: mines, transload facilities, trucking, storage.
        2. Assess risks: weather, labor, regulatory, transportation disruptions.
        3. Maintain buffer inventory at key locations.
        4. Develop contingency plans for alternate supply routes and sources.
        5. Monitor supplier performance and reliability.
        6. Use digital tracking and analytics for real-time visibility.
        7. Review and update risk management plans regularly.
        """,
        key_factors=[
            "Supply chain nodes",
            "Risk assessment",
            "Buffer inventory",
            "Contingency planning",
            "Supplier reliability",
            "Real-time tracking"
        ],
        primary_authority=[
            "Operator supply chain policy",
            "Industry best practices"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Supply chain risks are minimal and do not require special management.",
        counter_arguments=[
            "Disruptions can halt operations and increase costs.",
            "Proactive management reduces downtime.",
            "Industry data supports risk-based approaches."
        ],
        resolution_strategy="Continuously monitor and manage risks using best practices.",
        entity_scope="All proppant supply chains",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Operator supply chain policy"
    ),
    DoctrineBlock(
        topic="Proppant Quality Assurance and Lot Traceability",
        keywords=["proppant quality", "quality assurance", "traceability", "lot tracking", "compliance"],
        conclusion_template="Ensure full traceability and quality assurance for every proppant lot used in operations.",
        reasoning_framework="""
        1. Require unique lot identification and documentation from suppliers.
        2. Maintain chain-of-custody records from mine to wellsite.
        3. Conduct random sampling and testing at receipt.
        4. Store test results and lot data in centralized database.
        5. Investigate and quarantine non-conforming lots.
        6. Reference lot data for post-job analysis and regulatory compliance.
        7. Enforce corrective actions for repeated supplier non-compliance.
        """,
        key_factors=[
            "Lot identification",
            "Chain-of-custody",
            "Sampling and testing",
            "Database management",
            "Non-conformance investigation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 19C",
            "Operator QA/QC policy"
        ],
        burden_holder="Quality Assurance Manager",
        adversary_position="Traceability is unnecessary if supplier is reputable.",
        counter_arguments=[
            "Traceability enables root-cause analysis of quality issues.",
            "Regulatory and contractual obligations require traceability.",
            "Field failures can be traced to specific lots."
        ],
        resolution_strategy="Enforce traceability and QA/QC protocols for all proppant lots.",
        entity_scope="All proppant procurement and use",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Blending for Cost and Performance Optimization",
        keywords=["proppant blending", "cost optimization", "performance", "hybrid design", "stimulation"],
        conclusion_template="Blend proppant types to optimize cost and performance for specific well objectives.",
        reasoning_framework="""
        1. Identify performance requirements: conductivity, strength, flowback control.
        2. Evaluate cost and availability of candidate proppant types.
        3. Model blend performance using simulation tools and laboratory data.
        4. Consider operational impacts: blending equipment, logistics, QA/QC.
        5. Reference offset well results for blend effectiveness.
        6. Adjust blend ratios based on field performance and economics.
        7. Document blend design and rationale for future optimization.
        """,
        key_factors=[
            "Performance requirements",
            "Cost and availability",
            "Blend modeling",
            "Operational impacts",
            "Field performance",
            "Blend documentation"
        ],
        primary_authority=[
            "SPE 194334",
            "Frac simulation software"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="Single proppant type is simpler and more reliable.",
        counter_arguments=[
            "Blending can reduce costs while maintaining performance.",
            "Hybrid designs are proven in many basins.",
            "Operational complexity can be managed with proper planning."
        ],
        resolution_strategy="Use data-driven blend optimization and continuous improvement.",
        entity_scope="Hydraulic fracturing operations",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="SPE 194334"
    ),
    DoctrineBlock(
        topic="Proppant Degradation Due to Acidizing Treatments",
        keywords=["proppant degradation", "acidizing", "conductivity loss", "acid solubility", "post-frac treatment"],
        conclusion_template="Select acid-resistant proppant and design acid treatments to minimize proppant degradation.",
        reasoning_framework="""
        1. Assess need for post-frac acidizing based on formation and completion design.
        2. Evaluate acid solubility of candidate proppants using API RP 19C/ISO 13503-2 data.
        3. Select proppant with low acid solubility for acidizing environments.
        4. Design acid treatments to minimize contact time with proppant pack.
        5. Monitor post-treatment conductivity and production.
        6. Reference offset well data for acid-related degradation.
        7. Adjust proppant and acid design based on field results.
        """,
        key_factors=[
            "Acid solubility",
            "Acid treatment design",
            "Proppant selection",
            "Conductivity loss",
            "Offset well data",
            "Post-treatment monitoring"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2",
            "SPE 140753"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="Acidizing impact on proppant is negligible.",
        counter_arguments=[
            "High acid solubility can cause significant conductivity loss.",
            "Proper proppant selection mitigates degradation.",
            "Field data shows acidizing can damage proppant packs."
        ],
        resolution_strategy="Select acid-resistant proppant and optimize acid design.",
        entity_scope="Wells requiring post-frac acidizing",
        confidence=0.86,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Sphericity and Roundness Impact on Conductivity",
        keywords=["sphericity", "roundness", "proppant shape", "conductivity", "API RP 19C"],
        conclusion_template="Procure proppant with high sphericity and roundness to maximize pack conductivity.",
        reasoning_framework="""
        1. Reference API RP 19C/ISO 13503-2 sphericity and roundness requirements.
        2. Evaluate supplier test data for compliance.
        3. Model impact of shape on proppant pack permeability and conductivity.
        4. Reject lots with substandard sphericity/roundness.
        5. Monitor field performance for shape-related issues.
        6. Enforce corrective actions with suppliers as needed.
        """,
        key_factors=[
            "Sphericity and roundness",
            "Supplier test data",
            "Pack permeability",
            "Conductivity",
            "Field performance",
            "Supplier compliance"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2"
        ],
        burden_holder="Procurement and QA/QC",
        adversary_position="Shape is less important than cost or size.",
        counter_arguments=[
            "Poor shape reduces conductivity and increases fines.",
            "API/ISO standards ensure minimum performance.",
            "Field failures linked to poor sphericity/roundness."
        ],
        resolution_strategy="Enforce shape requirements for all proppant procurement.",
        entity_scope="All proppant supply chains",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Pack Permeability Under Cyclic Loading",
        keywords=["proppant pack", "permeability", "cyclic loading", "conductivity", "well cycling"],
        conclusion_template="Select proppant with high cyclic loading durability for wells subject to pressure cycling.",
        reasoning_framework="""
        1. Identify wells subject to frequent shut-ins or pressure cycling.
        2. Reference laboratory data for proppant pack permeability under cyclic loading.
        3. Select proppant with proven durability and low fines generation under cycling.
        4. Monitor field performance for conductivity loss after cycling events.
        5. Adjust proppant selection and treatment design as needed.
        """,
        key_factors=[
            "Cyclic loading durability",
            "Fines generation",
            "Pack permeability",
            "Field performance",
            "Proppant selection",
            "Treatment design"
        ],
        primary_authority=[
            "SPE 140753",
            "API RP 19C"
        ],
        burden_holder="Completions Engineer",
        adversary_position="Cyclic loading effects are negligible.",
        counter_arguments=[
            "Cyclic loading can cause significant pack damage.",
            "Durable proppant mitigates conductivity loss.",
            "Field data supports cyclic loading considerations."
        ],
        resolution_strategy="Select proppant based on cyclic loading risk and durability data.",
        entity_scope="Wells with frequent cycling",
        confidence=0.85,
        confidence_zone="Moderate",
        controlling_precedent="SPE 140753"
    ),
    DoctrineBlock(
        topic="Proppant Handling Safety and Environmental Compliance",
        keywords=["proppant handling", "safety", "environmental compliance", "dust control", "OSHA"],
        conclusion_template="Implement strict safety and environmental protocols for proppant handling and storage.",
        reasoning_framework="""
        1. Enforce OSHA and local regulations for silica dust exposure.
        2. Use dust control systems at transload and wellsite.
        3. Provide PPE and training for all personnel.
        4. Monitor air quality and exposure levels.
        5. Implement spill prevention and cleanup procedures.
        6. Maintain documentation for regulatory compliance.
        7. Conduct regular safety audits and training refreshers.
        """,
        key_factors=[
            "Dust control",
            "PPE and training",
            "Air quality monitoring",
            "Spill prevention",
            "Regulatory documentation",
            "Safety audits"
        ],
        primary_authority=[
            "OSHA",
            "Operator HSE policy"
        ],
        burden_holder="HSE Manager",
        adversary_position="Dust and environmental risks are minimal.",
        counter_arguments=[
            "Silica dust is a known health hazard.",
            "Regulatory penalties for non-compliance are severe.",
            "Best practices reduce risk and liability."
        ],
        resolution_strategy="Implement and enforce best-in-class safety and environmental protocols.",
        entity_scope="All proppant handling operations",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="OSHA regulations"
    ),
    DoctrineBlock(
        topic="Proppant Inventory Management and Digital Tracking",
        keywords=["proppant inventory", "digital tracking", "supply chain", "real-time monitoring", "logistics"],
        conclusion_template="Use digital tracking systems for real-time proppant inventory management and logistics optimization.",
        reasoning_framework="""
        1. Implement digital inventory tracking from mine to wellsite.
        2. Integrate tracking data with logistics and operations platforms.
        3. Use real-time data to optimize deliveries and minimize stockouts.
        4. Monitor inventory levels and consumption rates.
        5. Generate reports for supply chain and operational planning.
        6. Continuously improve tracking accuracy and integration.
        """,
        key_factors=[
            "Digital tracking systems",
            "Integration with logistics",
            "Real-time data",
            "Inventory optimization",
            "Reporting",
            "Continuous improvement"
        ],
        primary_authority=[
            "Operator supply chain policy",
            "Industry best practices"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Manual tracking is sufficient for inventory management.",
        counter_arguments=[
            "Digital systems improve accuracy and efficiency.",
            "Real-time data enables proactive management.",
            "Manual errors can disrupt operations."
        ],
        resolution_strategy="Adopt digital tracking for all proppant inventory management.",
        entity_scope="All proppant supply chains",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Operator supply chain policy"
    ),
    DoctrineBlock(
        topic="Proppant Storage and Weather Risk Mitigation",
        keywords=["proppant storage", "weather risk", "inventory", "moisture control", "logistics"],
        conclusion_template="Store proppant in weather-protected facilities to prevent quality degradation and supply disruptions.",
        reasoning_framework="""
        1. Assess weather risks: rain, snow, temperature extremes.
        2. Use covered storage or silos to protect proppant from moisture and contamination.
        3. Monitor storage conditions and inventory quality.
        4. Maintain contingency plans for severe weather events.
        5. Document storage protocols and inspections.
        6. Review and update weather risk mitigation plans regularly.
        """,
        key_factors=[
            "Weather risk assessment",
            "Covered storage",
            "Inventory quality monitoring",
            "Contingency planning",
            "Documentation",
            "Plan review"
        ],
        primary_authority=[
            "Operator logistics policy",
            "Industry best practices"
        ],
        burden_holder="Logistics Manager",
        adversary_position="Outdoor storage is sufficient in most climates.",
        counter_arguments=[
            "Moisture degrades proppant quality and pumpability.",
            "Weather events can disrupt supply.",
            "Covered storage is industry standard."
        ],
        resolution_strategy="Implement covered storage and weather risk protocols for all proppant inventory.",
        entity_scope="All proppant storage facilities",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Operator logistics policy"
    ),
    DoctrineBlock(
        topic="Proppant Procurement Contracting and Price Volatility Management",
        keywords=["proppant procurement", "contracting", "price volatility", "supply agreements", "cost control"],
        conclusion_template="Negotiate supply contracts with price and volume protections to manage proppant cost volatility.",
        reasoning_framework="""
        1. Analyze historical price volatility and supply trends.
        2. Negotiate contracts with fixed or indexed pricing and minimum/maximum volumes.
        3. Include force majeure and supply disruption clauses.
        4. Monitor contract compliance and supplier performance.
        5. Adjust procurement strategy based on market conditions.
        6. Maintain relationships with multiple suppliers for flexibility.
        """,
        key_factors=[
            "Price volatility",
            "Contract terms",
            "Supplier performance",
            "Market conditions",
            "Supply flexibility",
            "Risk mitigation"
        ],
        primary_authority=[
            "Operator procurement policy",
            "Industry best practices"
        ],
        burden_holder="Procurement Manager",
        adversary_position="Spot market purchases are more cost-effective.",
        counter_arguments=[
            "Contracts provide price and supply stability.",
            "Spot market exposes operator to volatility.",
            "Multiple suppliers increase flexibility."
        ],
        resolution_strategy="Balance contract and spot purchases for optimal risk management.",
        entity_scope="All proppant procurement operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Operator procurement policy"
    ),
    DoctrineBlock(
        topic="Proppant Specification Deviation Management",
        keywords=["proppant specification", "deviation", "quality control", "API RP 19C", "non-conformance"],
        conclusion_template="Document and manage all proppant specification deviations with corrective actions and supplier accountability.",
        reasoning_framework="""
        1. Require suppliers to report all specification deviations.
        2. Investigate root cause and assess operational impact.
        3. Quarantine and test affected lots.
        4. Document deviation and corrective actions.
        5. Enforce supplier accountability and continuous improvement.
        6. Reference deviation records for future procurement decisions.
        """,
        key_factors=[
            "Deviation reporting",
            "Root cause analysis",
            "Lot quarantine and testing",
            "Corrective actions",
            "Supplier accountability",
            "Documentation"
        ],
        primary_authority=[
            "API RP 19C",
            "Operator QA/QC policy"
        ],
        burden_holder="Quality Assurance Manager",
        adversary_position="Minor deviations do not require documentation.",
        counter_arguments=[
            "Undocumented deviations can lead to field failures.",
            "Continuous improvement requires accurate records.",
            "Supplier accountability improves quality."
        ],
        resolution_strategy="Enforce deviation documentation and corrective action protocols.",
        entity_scope="All proppant procurement and use",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Fluid Compatibility Testing",
        keywords=["proppant", "fluid compatibility", "testing", "API RP 19C", "fracturing fluid"],
        conclusion_template="Conduct compatibility testing for all new proppant/fluid combinations prior to field use.",
        reasoning_framework="""
        1. Test proppant/fluid combinations for chemical and physical compatibility.
        2. Reference API RP 19C/ISO 13503-2 test protocols.
        3. Assess risk of proppant degradation, swelling, or fines generation.
        4. Monitor fluid/proppant interaction during laboratory simulation.
        5. Document results and approve only compatible combinations.
        6. Review field performance and adjust as needed.
        """,
        key_factors=[
            "Compatibility testing",
            "API/ISO protocols",
            "Degradation risk",
            "Fines generation",
            "Documentation",
            "Field performance"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="Compatibility issues are rare and do not require testing.",
        counter_arguments=[
            "Incompatible combinations can cause screen-outs and conductivity loss.",
            "API/ISO protocols ensure minimum performance.",
            "Field failures linked to poor compatibility."
        ],
        resolution_strategy="Test and document all new proppant/fluid combinations.",
        entity_scope="All hydraulic fracturing operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Environmental Footprint Reduction",
        keywords=["proppant", "environmental footprint", "sustainability", "carbon emissions", "logistics"],
        conclusion_template="Prioritize proppant sources and logistics with lower environmental footprint where feasible.",
        reasoning_framework="""
        1. Assess carbon emissions and environmental impact of each proppant source and delivery route.
        2. Consider in-basin sand to reduce transportation emissions.
        3. Evaluate supplier sustainability practices and certifications.
        4. Monitor and report environmental metrics for continuous improvement.
        5. Balance environmental goals with operational and economic requirements.
        6. Engage stakeholders in sustainability initiatives.
        """,
        key_factors=[
            "Carbon emissions",
            "Transportation distance",
            "Supplier sustainability",
            "Environmental metrics",
            "Operational requirements",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "Operator sustainability policy",
            "Industry best practices"
        ],
        burden_holder="Sustainability Manager",
        adversary_position="Environmental footprint is secondary to cost and performance.",
        counter_arguments=[
            "Sustainability is increasingly important for stakeholders.",
            "In-basin sand reduces emissions and cost.",
            "Regulatory and investor pressure is increasing."
        ],
        resolution_strategy="Integrate environmental metrics into proppant sourcing decisions.",
        entity_scope="All proppant supply chains",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Operator sustainability policy"
    ),
    DoctrineBlock(
        topic="Proppant Radioactivity and NORM Compliance",
        keywords=["proppant", "radioactivity", "NORM", "compliance", "regulatory"],
        conclusion_template="Test and document NORM levels in all proppant shipments to ensure regulatory compliance.",
        reasoning_framework="""
        1. Require NORM testing and certification from all proppant suppliers.
        2. Maintain records of NORM levels for each shipment.
        3. Quarantine and investigate any shipments exceeding regulatory limits.
        4. Train personnel in safe handling and disposal of NORM-contaminated material.
        5. Report NORM data to regulatory agencies as required.
        6. Review and update NORM compliance protocols regularly.
        """,
        key_factors=[
            "NORM testing",
            "Certification",
            "Record keeping",
            "Safe handling",
            "Regulatory reporting",
            "Protocol review"
        ],
        primary_authority=[
            "State regulatory agencies",
            "Operator HSE policy"
        ],
        burden_holder="HSE Manager",
        adversary_position="NORM risk is negligible in proppant supply.",
        counter_arguments=[
            "NORM contamination can pose health and regulatory risks.",
            "Testing and documentation are required by law.",
            "Safe handling protocols protect personnel."
        ],
        resolution_strategy="Enforce NORM testing and compliance for all proppant shipments.",
        entity_scope="All proppant procurement and handling",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="State regulatory agencies"
    ),
    DoctrineBlock(
        topic="Proppant Sourcing Ethics and Community Impact",
        keywords=["proppant sourcing", "ethics", "community impact", "social license", "local sourcing"],
        conclusion_template="Favor proppant suppliers with strong ethical practices and positive community impact.",
        reasoning_framework="""
        1. Evaluate supplier labor, environmental, and community practices.
        2. Require supplier certification for ethical sourcing.
        3. Monitor community feedback and incident reports.
        4. Engage with local stakeholders to address concerns.
        5. Balance ethical sourcing with operational and economic needs.
        6. Document supplier performance and community engagement.
        """,
        key_factors=[
            "Supplier ethics",
            "Community impact",
            "Certification",
            "Stakeholder engagement",
            "Incident monitoring",
            "Documentation"
        ],
        primary_authority=[
            "Operator supply chain policy",
            "Industry best practices"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Ethical sourcing is not a priority in proppant selection.",
        counter_arguments=[
            "Ethical sourcing reduces reputational and regulatory risk.",
            "Community impact affects social license to operate.",
            "Industry standards increasingly require ethical practices."
        ],
        resolution_strategy="Integrate ethics and community impact into supplier evaluation.",
        entity_scope="All proppant procurement",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Operator supply chain policy"
    ),
    DoctrineBlock(
        topic="Proppant Market Intelligence and Benchmarking",
        keywords=["proppant market", "intelligence", "benchmarking", "pricing", "supply trends"],
        conclusion_template="Continuously monitor and benchmark proppant market trends to inform procurement and design decisions.",
        reasoning_framework="""
        1. Collect and analyze market data: pricing, supply, demand, capacity.
        2. Benchmark against peer operators and industry indices.
        3. Adjust procurement and design strategies based on market intelligence.
        4. Share insights with internal stakeholders for planning.
        5. Review and update market intelligence protocols regularly.
        """,
        key_factors=[
            "Market data collection",
            "Benchmarking",
            "Strategy adjustment",
            "Stakeholder communication",
            "Protocol review"
        ],
        primary_authority=[
            "Operator procurement policy",
            "Industry market reports"
        ],
        burden_holder="Procurement Manager",
        adversary_position="Market intelligence is unnecessary for routine procurement.",
        counter_arguments=[
            "Market trends impact cost and availability.",
            "Benchmarking improves competitiveness.",
            "Proactive strategy reduces risk."
        ],
        resolution_strategy="Integrate market intelligence into procurement and design workflows.",
        entity_scope="All proppant procurement and design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Operator procurement policy"
    ),
    DoctrineBlock(
        topic="Proppant Supplier Performance Evaluation",
        keywords=["proppant supplier", "performance evaluation", "QA/QC", "delivery reliability", "cost"],
        conclusion_template="Regularly evaluate proppant suppliers on quality, delivery, and cost metrics.",
        reasoning_framework="""
        1. Define performance metrics: quality, delivery, cost, responsiveness.
        2. Collect data from operations, QA/QC, and supply chain.
        3. Score suppliers and provide feedback for improvement.
        4. Use performance data for future sourcing decisions.
        5. Enforce corrective actions for underperforming suppliers.
        6. Document evaluation process and results.
        """,
        key_factors=[
            "Performance metrics",
            "Data collection",
            "Scoring and feedback",
            "Sourcing decisions",
            "Corrective actions",
            "Documentation"
        ],
        primary_authority=[
            "Operator procurement policy",
            "QA/QC standards"
        ],
        burden_holder="Procurement Manager",
        adversary_position="Supplier evaluation is unnecessary if price is competitive.",
        counter_arguments=[
            "Quality and delivery impact operations and cost.",
            "Continuous improvement requires feedback.",
            "Performance data supports better sourcing."
        ],
        resolution_strategy="Implement regular supplier evaluation and improvement cycles.",
        entity_scope="All proppant procurement",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Operator procurement policy"
    ),
    DoctrineBlock(
        topic="Proppant Demand Forecasting and Planning",
        keywords=["proppant demand", "forecasting", "planning", "operations", "supply chain"],
        conclusion_template="Use demand forecasting models to align proppant supply with operational plans.",
        reasoning_framework="""
        1. Collect historical consumption and operational plan data.
        2. Use statistical and machine learning models for demand forecasting.
        3. Share forecasts with suppliers and logistics teams.
        4. Adjust procurement and inventory plans based on forecast accuracy.
        5. Review and update forecasting models regularly.
        """,
        key_factors=[
            "Historical data",
            "Forecasting models",
            "Supplier communication",
            "Inventory planning",
            "Forecast accuracy",
            "Model review"
        ],
        primary_authority=[
            "Operator supply chain policy",
            "Industry best practices"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Forecasting is unreliable and unnecessary.",
        counter_arguments=[
            "Forecasting reduces stockouts and overages.",
            "Improves supplier and logistics coordination.",
            "Continuous improvement increases accuracy."
        ],
        resolution_strategy="Integrate forecasting into supply chain and procurement workflows.",
        entity_scope="All proppant supply chains",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Operator supply chain policy"
    ),
    DoctrineBlock(
        topic="Proppant Usage Data Analytics and Continuous Improvement",
        keywords=["proppant usage", "data analytics", "continuous improvement", "performance monitoring", "optimization"],
        conclusion_template="Leverage data analytics to optimize proppant usage and drive continuous improvement.",
        reasoning_framework="""
        1. Collect detailed proppant usage and performance data from each well.
        2. Analyze data for trends, anomalies, and optimization opportunities.
        3. Share insights with engineering, operations, and procurement teams.
        4. Implement changes based on data-driven recommendations.
        5. Monitor impact and iterate for continuous improvement.
        """,
        key_factors=[
            "Data collection",
            "Analytics",
            "Cross-functional sharing",
            "Implementation",
            "Impact monitoring",
            "Iteration"
        ],
        primary_authority=[
            "Operator performance improvement policy",
            "Industry best practices"
        ],
        burden_holder="Performance Improvement Manager",
        adversary_position="Analytics adds little value to proppant optimization.",
        counter_arguments=[
            "Data-driven decisions improve performance and cost.",
            "Analytics identify root causes of issues.",
            "Continuous improvement is industry standard."
        ],
        resolution_strategy="Integrate analytics into all proppant usage and optimization workflows.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Operator performance improvement policy"
    ),
    DoctrineBlock(
        topic="Proppant Waste Minimization and Recycling",
        keywords=["proppant waste", "minimization", "recycling", "environmental compliance", "cost control"],
        conclusion_template="Implement waste minimization and recycling protocols for unused proppant.",
        reasoning_framework="""
        1. Track proppant usage and identify sources of waste.
        2. Implement operational controls to minimize leftover proppant.
        3. Evaluate recycling options for unused or returned proppant.
        4. Comply with environmental regulations for disposal and recycling.
        5. Document waste minimization and recycling efforts.
        6. Review and update protocols for continuous improvement.
        """,
        key_factors=[
            "Usage tracking",
            "Operational controls",
            "Recycling options",
            "Regulatory compliance",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "Operator environmental policy",
            "Industry best practices"
        ],
        burden_holder="Operations Manager",
        adversary_position="Proppant waste is unavoidable and recycling is not cost-effective.",
        counter_arguments=[
            "Waste increases cost and environmental impact.",
            "Recycling reduces disposal costs and footprint.",
            "Regulatory compliance requires waste minimization."
        ],
        resolution_strategy="Implement and document waste minimization and recycling protocols.",
        entity_scope="All proppant handling and disposal operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Operator environmental policy"
    ),
    DoctrineBlock(
        topic="Proppant Transportation Mode Selection",
        keywords=["proppant transportation", "mode selection", "rail", "truck", "barge", "cost optimization"],
        conclusion_template="Select transportation mode based on cost, reliability, and operational requirements.",
        reasoning_framework="""
        1. Evaluate available transportation modes: rail, truck, barge, intermodal.
        2. Analyze cost, transit time, and reliability for each mode.
        3. Consider operational constraints: delivery schedule, site access, inventory needs.
        4. Assess environmental impact of each mode.
        5. Select mode or combination that best meets project requirements.
        6. Review and update mode selection as project evolves.
        """,
        key_factors=[
            "Mode availability",
            "Cost and reliability",
            "Operational constraints",
            "Environmental impact",
            "Project requirements",
            "Review process"
        ],
        primary_authority=[
            "Operator logistics policy",
            "Industry best practices"
        ],
        burden_holder="Logistics Manager",
        adversary_position="Truck delivery is always preferable for flexibility.",
        counter_arguments=[
            "Rail and barge may offer lower cost and emissions.",
            "Mode selection should be data-driven.",
            "Operational needs may change over project life."
        ],
        resolution_strategy="Use data-driven mode selection for each project.",
        entity_scope="All proppant transportation operations",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Operator logistics policy"
    ),
    DoctrineBlock(
        topic="Proppant Loading and Unloading Best Practices",
        keywords=["proppant loading", "unloading", "best practices", "safety", "quality control"],
        conclusion_template="Follow best practices for safe and efficient proppant loading and unloading.",
        reasoning_framework="""
        1. Train personnel in safe handling and equipment operation.
        2. Use dust control and spill prevention measures.
        3. Inspect equipment before and after use.
        4. Monitor loading/unloading for quality and contamination.
        5. Document incidents and near-misses for continuous improvement.
        6. Review and update best practices regularly.
        """,
        key_factors=[
            "Personnel training",
            "Dust and spill control",
            "Equipment inspection",
            "Quality monitoring",
            "Incident documentation",
            "Best practice review"
        ],
        primary_authority=[
            "Operator HSE policy",
            "Industry best practices"
        ],
        burden_holder="Operations Manager",
        adversary_position="Loading/unloading risks are minimal and do not require special protocols.",
        counter_arguments=[
            "Safety incidents can cause injury and downtime.",
            "Quality control prevents contamination.",
            "Continuous improvement reduces risk."
        ],
        resolution_strategy="Implement and enforce best practices for all loading/unloading operations.",
        entity_scope="All proppant logistics operations",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="Operator HSE policy"
    ),
    DoctrineBlock(
        topic="Proppant Screen-Out Prevention and Response",
        keywords=["proppant screen-out", "prevention", "response", "fracturing operations", "real-time monitoring"],
        conclusion_template="Implement real-time monitoring and response protocols to prevent and manage proppant screen-outs.",
        reasoning_framework="""
        1. Monitor pressure and proppant concentration in real time during fracturing.
        2. Use predictive models to identify screen-out risk.
        3. Adjust pump rate, fluid viscosity, and PPA as needed.
        4. Develop response protocols for screen-out events.
        5. Document incidents and lessons learned for future improvement.
        6. Train personnel in prevention and response procedures.
        """,
        key_factors=[
            "Real-time monitoring",
            "Predictive modeling",
            "Operational adjustments",
            "Response protocols",
            "Incident documentation",
            "Personnel training"
        ],
        primary_authority=[
            "Operator stimulation policy",
            "Frac simulation software"
        ],
        burden_holder="Stimulation Supervisor",
        adversary_position="Screen-outs are unavoidable in aggressive designs.",
        counter_arguments=[
            "Prevention reduces downtime and cost.",
            "Real-time data enables proactive management.",
            "Training improves response effectiveness."
        ],
        resolution_strategy="Integrate monitoring and response into all fracturing operations.",
        entity_scope="All hydraulic fracturing jobs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Operator stimulation policy"
    ),
    DoctrineBlock(
        topic="Proppant Flowback Monitoring and Remediation",
        keywords=["proppant flowback", "monitoring", "remediation", "production operations", "equipment protection"],
        conclusion_template="Monitor and remediate proppant flowback to protect equipment and maintain production.",
        reasoning_framework="""
        1. Monitor flowback fluid for proppant content during early production.
        2. Use RCS or mechanical screens to reduce flowback risk.
        3. Investigate and remediate excessive flowback events.
        4. Document flowback incidents and remediation actions.
        5. Adjust stimulation design to reduce future flowback.
        6. Train personnel in flowback monitoring and response.
        """,
        key_factors=[
            "Flowback monitoring",
            "RCS and mechanical screens",
            "Remediation actions",
            "Incident documentation",
            "Design adjustment",
            "Personnel training"
        ],
        primary_authority=[
            "Operator production policy",
            "Industry best practices"
        ],
        burden_holder="Production Engineer",
        adversary_position="Flowback is an unavoidable consequence of stimulation.",
        counter_arguments=[
            "Flowback can damage equipment and reduce production.",
            "Mitigation reduces risk and cost.",
            "Field data supports proactive flowback management."
        ],
        resolution_strategy="Monitor, remediate, and continuously improve flowback management.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Operator production policy"
    ),
    DoctrineBlock(
        topic="Proppant Data Integration Across Operations",
        keywords=["proppant data", "integration", "operations", "digital systems", "performance optimization"],
        conclusion_template="Integrate proppant data across digital systems for end-to-end operational optimization.",
        reasoning_framework="""
        1. Standardize data formats and protocols for proppant tracking.
        2. Integrate data from procurement, logistics, stimulation, and production systems.
        3. Enable real-time visibility and analytics for all stakeholders.
        4. Use integrated data for performance optimization and troubleshooting.
        5. Review and update integration protocols as systems evolve.
        """,
        key_factors=[
            "Data standardization",
            "System integration",
            "Real-time visibility",
            "Analytics",
            "Optimization",
            "Protocol review"
        ],
        primary_authority=[
            "Operator digital strategy",
            "Industry best practices"
        ],
        burden_holder="Digital Transformation Manager",
        adversary_position="Integration is costly and adds little value.",
        counter_arguments=[
            "Integrated data enables optimization and troubleshooting.",
            "Reduces manual errors and inefficiencies.",
            "Supports continuous improvement."
        ],
        resolution_strategy="Prioritize integration in digital transformation initiatives.",
        entity_scope="All proppant-related operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Operator digital strategy"
    ),
    DoctrineBlock(
        topic="Proppant Mesh Size Distribution and Quality Control",
        keywords=["proppant mesh size", "distribution", "quality control", "API RP 19C", "sieve analysis"],
        conclusion_template="Enforce strict mesh size distribution requirements for all proppant lots.",
        reasoning_framework="""
        1. Require sieve analysis for every proppant lot per API RP 19C.
        2. Reject lots with excessive out-of-spec particles.
        3. Monitor supplier compliance and performance trends.
        4. Document mesh size distribution for traceability.
        5. Review field performance for mesh size-related issues.
        6. Enforce corrective actions with suppliers as needed.
        """,
        key_factors=[
            "Sieve analysis",
            "Out-of-spec particles",
            "Supplier compliance",
            "Traceability",
            "Field performance",
            "Corrective actions"
        ],
        primary_authority=[
            "API RP 19C",
            "Operator QA/QC policy"
        ],
        burden_holder="Quality Assurance Manager",
        adversary_position="Minor mesh size deviations do not impact performance.",
        counter_arguments=[
            "Out-of-spec particles increase screen-out and fines risk.",
            "API/ISO standards ensure minimum performance.",
            "Field failures linked to poor mesh distribution."
        ],
        resolution_strategy="Enforce mesh size requirements for all proppant lots.",
        entity_scope="All proppant procurement and use",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Pack Cleanup and Post-Frac Well Conditioning",
        keywords=["proppant pack", "cleanup", "post-frac", "well conditioning", "production optimization"],
        conclusion_template="Implement post-frac cleanup protocols to maximize proppant pack conductivity and production.",
        reasoning_framework="""
        1. Design flowback schedule to minimize pack damage and fines migration.
        2. Use chemical additives as needed for pack cleanup.
        3. Monitor early production for cleanup effectiveness.
        4. Adjust cleanup protocols based on field results.
        5. Document cleanup procedures and outcomes.
        6. Review and update protocols for continuous improvement.
        """,
        key_factors=[
            "Flowback schedule",
            "Chemical additives",
            "Monitoring",
            "Protocol adjustment",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "Operator production policy",
            "Industry best practices"
        ],
        burden_holder="Production Engineer",
        adversary_position="Post-frac cleanup is unnecessary and adds cost.",
        counter_arguments=[
            "Cleanup improves conductivity and production.",
            "Field data supports post-frac conditioning.",
            "Continuous improvement reduces cost."
        ],
        resolution_strategy="Implement and optimize post-frac cleanup protocols.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Operator production policy"
    ),
    DoctrineBlock(
        topic="Proppant Sourcing from International Suppliers",
        keywords=["proppant sourcing", "international suppliers", "import", "logistics", "quality control"],
        conclusion_template="Vet international proppant suppliers for quality, logistics, and regulatory compliance before procurement.",
        reasoning_framework="""
        1. Assess quality control and certification of international suppliers.
        2. Evaluate logistics: shipping time, customs, and delivery reliability.
        3. Ensure compliance with API RP 19C/ISO 13503-2 and local regulations.
        4. Monitor supplier performance and incident history.
        5. Maintain contingency plans for supply disruptions.
        6. Document supplier vetting and procurement decisions.
        """,
        key_factors=[
            "Quality control",
            "Logistics",
            "Regulatory compliance",
            "Supplier performance",
            "Contingency planning",
            "Documentation"
        ],
        primary_authority=[
            "API RP 19C",
            "Operator procurement policy"
        ],
        burden_holder="Procurement Manager",
        adversary_position="International sourcing is too risky and complex.",
        counter_arguments=[
            "International suppliers can offer cost and supply advantages.",
            "Quality and compliance can be managed with proper vetting.",
            "Contingency planning mitigates risk."
        ],
        resolution_strategy="Vet and document all international suppliers before procurement.",
        entity_scope="All proppant procurement operations",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Pack Conductivity Testing and Field Validation",
        keywords=["proppant pack", "conductivity testing", "field validation", "API RP 19C", "performance monitoring"],
        conclusion_template="Validate proppant pack conductivity with laboratory testing and field performance monitoring.",
        reasoning_framework="""
        1. Conduct laboratory conductivity testing per API RP 19C/ISO 13503-2.
        2. Monitor field production for conductivity-related performance.
        3. Compare laboratory and field results for validation.
        4. Investigate discrepancies and adjust design as needed.
        5. Document validation process and outcomes.
        6. Review and update testing protocols regularly.
        """,
        key_factors=[
            "Laboratory testing",
            "Field monitoring",
            "Result comparison",
            "Discrepancy investigation",
            "Documentation",
            "Protocol review"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2"
        ],
        burden_holder="Completions Engineer",
        adversary_position="Laboratory testing is unnecessary if field results are acceptable.",
        counter_arguments=[
            "Lab testing ensures baseline performance.",
            "Field validation confirms design assumptions.",
            "Continuous improvement requires both."
        ],
        resolution_strategy="Integrate lab and field validation in all proppant selection workflows.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Logistics Digitalization and Automation",
        keywords=["proppant logistics", "digitalization", "automation", "supply chain", "efficiency"],
        conclusion_template="Adopt digital and automated systems to improve proppant logistics efficiency and reliability.",
        reasoning_framework="""
        1. Implement digital platforms for order, tracking, and delivery management.
        2. Use automation for inventory, scheduling, and reporting.
        3. Integrate systems with suppliers and logistics providers.
        4. Monitor performance and identify optimization opportunities.
        5. Train personnel in digital and automated workflows.
        6. Review and update systems for continuous improvement.
        """,
        key_factors=[
            "Digital platforms",
            "Automation",
            "System integration",
            "Performance monitoring",
            "Personnel training",
            "Continuous improvement"
        ],
        primary_authority=[
            "Operator digital strategy",
            "Industry best practices"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Digitalization adds cost and complexity.",
        counter_arguments=[
            "Digital systems improve efficiency and reliability.",
            "Automation reduces manual errors and delays.",
            "Continuous improvement justifies investment."
        ],
        resolution_strategy="Adopt and optimize digital/automated logistics systems.",
        entity_scope="All proppant logistics operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Operator digital strategy"
    ),
    DoctrineBlock(
        topic="Proppant Pack Strength and Fracture Closure Stress Matching",
        keywords=["proppant pack", "strength", "fracture closure stress", "matching", "conductivity"],
        conclusion_template="Match proppant pack strength to expected fracture closure stress for optimal conductivity.",
        reasoning_framework="""
        1. Calculate expected closure stress for each stage and zone.
        2. Select proppant with crush resistance exceeding closure stress.
        3. Reference API RP 19C/ISO 13503-2 crush test data.
        4. Monitor field performance for evidence of pack failure.
        5. Adjust proppant selection as needed for future wells.
        6. Document design rationale and outcomes.
        """,
        key_factors=[
            "Closure stress calculation",
            "Crush resistance",
            "API/ISO test data",
            "Field performance",
            "Design adjustment",
            "Documentation"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2"
        ],
        burden_holder="Completions Engineer",
        adversary_position="Proppant strength is less important than cost.",
        counter_arguments=[
            "Pack failure reduces conductivity and production.",
            "API/ISO data supports strength matching.",
            "Field failures linked to inadequate strength."
        ],
        resolution_strategy="Match proppant strength to closure stress in all designs.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Supply Chain Sustainability and ESG Reporting",
        keywords=["proppant supply chain", "sustainability", "ESG", "reporting", "stakeholder engagement"],
        conclusion_template="Integrate sustainability and ESG metrics into proppant supply chain management and reporting.",
        reasoning_framework="""
        1. Define ESG metrics for proppant sourcing, logistics, and usage.
        2. Collect and report data on emissions, waste, and community impact.
        3. Engage suppliers in sustainability initiatives and reporting.
        4. Communicate ESG performance to stakeholders and investors.
        5. Review and update ESG protocols regularly.
        """,
        key_factors=[
            "ESG metrics",
            "Data collection",
            "Supplier engagement",
            "Stakeholder communication",
            "Protocol review"
        ],
        primary_authority=[
            "Operator sustainability policy",
            "Industry ESG standards"
        ],
        burden_holder="Sustainability Manager",
        adversary_position="ESG reporting is not relevant to proppant supply.",
        counter_arguments=[
            "ESG is increasingly important for investors and regulators.",
            "Sustainability improves reputation and risk profile.",
            "Industry standards require ESG integration."
        ],
        resolution_strategy="Integrate ESG into all supply chain management and reporting.",
        entity_scope="All proppant supply chains",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Operator sustainability policy"
    ),
    DoctrineBlock(
        topic="Proppant Pack Acid Solubility and Formation Compatibility",
        keywords=["proppant pack", "acid solubility", "formation compatibility", "API RP 19C", "acidizing"],
        conclusion_template="Select proppant with acid solubility compatible with formation fluids and planned treatments.",
        reasoning_framework="""
        1. Assess formation fluid chemistry and planned acid treatments.
        2. Reference API RP 19C/ISO 13503-2 acid solubility data for candidate proppants.
        3. Select proppant with low solubility in expected acid environment.
        4. Monitor field performance for acid-related pack degradation.
        5. Adjust proppant and treatment design as needed.
        6. Document compatibility assessment and outcomes.
        """,
        key_factors=[
            "Formation fluid chemistry",
            "Acid treatment design",
            "Acid solubility data",
            "Field performance",
            "Design adjustment",
            "Documentation"
        ],
        primary_authority=[
            "API RP 19C",
            "ISO 13503-2"
        ],
        burden_holder="Stimulation Design Engineer",
        adversary_position="Acid solubility is not a significant factor in proppant selection.",
        counter_arguments=[
            "High solubility increases risk of conductivity loss.",
            "API/ISO data supports compatibility assessment.",
            "Field failures linked to poor compatibility."
        ],
        resolution_strategy="Assess and document acid compatibility for all proppant selections.",
        entity_scope="All proppant-stimulated wells",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 19C"
    ),
    DoctrineBlock(
        topic="Proppant Logistics Cost Modeling and Optimization",
        keywords=["proppant logistics", "cost modeling", "optimization