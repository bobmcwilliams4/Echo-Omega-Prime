from dataclasses import dataclass, field
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
        topic="Deep Penetrating vs Big Hole Charge Design",
        keywords=["perforation", "charge design", "deep penetrating", "big hole", "completion", "FRAC03"],
        conclusion_template="Select charge design based on reservoir permeability and stimulation objectives.",
        reasoning_framework="""
        The selection between deep penetrating and big hole charges is governed by the reservoir characteristics and the completion objectives. Deep penetrating charges are preferred in low-permeability formations where maximizing penetration depth improves connectivity to the reservoir, facilitating effective stimulation. Big hole charges are advantageous in high-permeability formations or when sand control is required, as they create larger entry holes that reduce near-wellbore pressure drop and minimize plugging risk. The choice must also consider casing thickness, gun standoff, and the risk of casing damage. Laboratory testing per API RP 19B and field trials provide empirical data to support the design selection. The final decision should balance productivity, operational safety, and well integrity.
        """,
        key_factors=[
            "Reservoir permeability",
            "Completion objectives",
            "Casing thickness",
            "Gun standoff",
            "Risk of casing damage",
            "API RP 19B test data"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE Monograph 18: Perforating"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Advocates for alternative charge design based on cost or operational simplicity.",
        counter_arguments=[
            "Alternative design may not optimize reservoir connectivity.",
            "Cost savings may be offset by reduced productivity."
        ],
        resolution_strategy="Conduct comparative analysis using API RP 19B test data and field performance metrics.",
        entity_scope="Well completion and stimulation engineering teams.",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 6.2"
    ),
    DoctrineBlock(
        topic="Shot Density and Phasing for Horizontal Wells",
        keywords=["shot density", "phasing", "horizontal wells", "perforation", "FRAC03"],
        conclusion_template="Optimize shot density and phasing to maximize fracture initiation and reservoir contact.",
        reasoning_framework="""
        Shot density and phasing are critical parameters in horizontal well perforation design. High shot density (e.g., 6 spf or greater) increases the probability of uniform fracture initiation and enhances cluster efficiency during hydraulic fracturing. Phasing (e.g., 60°, 90°, 120°, 180°) affects the azimuthal distribution of perforations, influencing fracture geometry and complexity. In horizontal wells, even phasing (e.g., 60° or 90°) is often preferred to promote uniform fracture propagation around the wellbore. The design must also account for casing strength, gun type, and operational constraints. Simulation and field diagnostics (e.g., fiber optics, microseismic) validate the effectiveness of the selected parameters.
        """,
        key_factors=[
            "Desired fracture geometry",
            "Cluster efficiency",
            "Casing strength",
            "Gun type and size",
            "Operational constraints"
        ],
        primary_authority=[
            "SPE 168632",
            "API RP 19B"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Prefers lower shot density to reduce cost and operational complexity.",
        counter_arguments=[
            "Lower shot density may reduce fracture complexity and production.",
            "Cost savings may not justify reduced reservoir contact."
        ],
        resolution_strategy="Model fracture initiation and propagation using simulation software and validate with field diagnostics.",
        entity_scope="Stimulation and completion engineering teams.",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 168632"
    ),
    DoctrineBlock(
        topic="Limited Entry Perforation Friction Diversion",
        keywords=["limited entry", "perforation", "friction diversion", "hydraulic fracturing", "FRAC03"],
        conclusion_template="Apply limited entry perforation to achieve uniform fluid distribution across clusters.",
        reasoning_framework="""
        Limited entry perforation is a technique used to promote even fluid distribution during multi-cluster hydraulic fracturing. By restricting the total perforation area (using fewer or smaller diameter perforations), a pressure drop is created at each cluster, ensuring that fracturing fluid is diverted more uniformly. The design requires accurate calculation of perforation friction, accounting for fluid properties, rate, and perforation geometry. Overly restrictive designs can cause excessive pressure, risking casing failure or screen-out, while insufficient restriction leads to uneven cluster stimulation. Field calibration and pressure monitoring are essential to optimize the approach.
        """,
        key_factors=[
            "Perforation area",
            "Fluid rate and properties",
            "Cluster spacing",
            "Casing pressure rating",
            "Field calibration data"
        ],
        primary_authority=[
            "SPE 184880",
            "API RP 19B"
        ],
        burden_holder="Fracturing Engineer",
        adversary_position="Argues for open entry to minimize operational risk.",
        counter_arguments=[
            "Open entry may result in poor cluster efficiency.",
            "Risk of under-stimulating certain clusters."
        ],
        resolution_strategy="Iterative design with field calibration and real-time pressure monitoring.",
        entity_scope="Hydraulic fracturing operations.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Underbalanced vs Overbalanced Perforating",
        keywords=["underbalanced", "overbalanced", "perforating", "well control", "completion", "FRAC03"],
        conclusion_template="Select perforating balance based on formation sensitivity, well control, and completion objectives.",
        reasoning_framework="""
        Underbalanced perforating involves creating a lower wellbore pressure than formation pressure during perforation, promoting immediate inflow and minimizing perforation damage. It is preferred in damage-sensitive formations or when immediate cleanup is desired. Overbalanced perforating, where wellbore pressure exceeds formation pressure, is used for well control or when formation influx is undesirable. The choice depends on reservoir sensitivity, fluid loss risk, and operational safety. Well control procedures and contingency planning are essential for underbalanced operations. The final decision should be supported by risk assessment and formation evaluation.
        """,
        key_factors=[
            "Formation sensitivity to damage",
            "Well control requirements",
            "Fluid loss risk",
            "Operational safety",
            "Cleanup objectives"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 120779"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers overbalanced for operational simplicity and safety.",
        counter_arguments=[
            "Overbalanced may increase perforation damage.",
            "Underbalanced may pose well control risks."
        ],
        resolution_strategy="Conduct risk assessment and review formation evaluation data.",
        entity_scope="Well completion and perforation teams.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 7.3"
    ),
    DoctrineBlock(
        topic="API RP 19B Perforating Performance Testing",
        keywords=["API RP 19B", "perforating", "performance testing", "charge evaluation", "FRAC03"],
        conclusion_template="Utilize API RP 19B test data to select and qualify perforating charges.",
        reasoning_framework="""
        API RP 19B provides standardized procedures for evaluating perforating charge performance, including penetration depth, hole size, and debris generation. Laboratory testing under controlled conditions allows for comparison between different charges and gun systems. Test results must be interpreted in the context of actual well conditions, including casing grade, cement sheath, and formation properties. Selection of charges should prioritize those with proven performance in analogous environments. Regular review of updated API RP 19B data ensures continued optimization of perforation design.
        """,
        key_factors=[
            "Charge penetration depth",
            "Hole diameter",
            "Debris generation",
            "Test conditions",
            "Casing and cement properties"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Perforating Engineer",
        adversary_position="Questions relevance of lab data to field performance.",
        counter_arguments=[
            "Lab conditions may not replicate field complexities.",
            "Field validation is necessary."
        ],
        resolution_strategy="Correlate lab results with field performance and adjust design as needed.",
        entity_scope="Perforating and completion engineering teams.",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B"
    ),
    DoctrineBlock(
        topic="Tubing-Conveyed Perforating (TCP) vs Wireline Operations",
        keywords=["TCP", "wireline", "perforating", "conveyance", "completion", "FRAC03"],
        conclusion_template="Select conveyance method based on well geometry, operational risk, and completion objectives.",
        reasoning_framework="""
        TCP is preferred in highly deviated or horizontal wells where wireline conveyance is challenging, or when large gun systems are required. It allows for perforating under pressure and can be integrated with completion operations. Wireline is suitable for vertical or mildly deviated wells, offering operational simplicity and rapid deployment. The choice must consider well geometry, pressure control requirements, gun size, and risk of stuck tools. Safety protocols and contingency planning are critical for both methods. Economic analysis and operational logistics also influence the decision.
        """,
        key_factors=[
            "Well deviation and geometry",
            "Gun size and length",
            "Pressure control requirements",
            "Operational risk",
            "Economic considerations"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 187451"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Advocates for wireline due to simplicity and cost.",
        counter_arguments=[
            "Wireline may not be feasible in highly deviated wells.",
            "TCP offers operational flexibility."
        ],
        resolution_strategy="Evaluate well geometry and operational requirements before selecting conveyance method.",
        entity_scope="Completion and perforation operations.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 187451"
    ),
    DoctrineBlock(
        topic="Perforation Friction Pressure Calculation",
        keywords=["perforation friction", "pressure calculation", "hydraulic fracturing", "FRAC03"],
        conclusion_template="Accurately calculate perforation friction to ensure effective limited entry design.",
        reasoning_framework="""
        Perforation friction pressure is calculated based on fluid rate, viscosity, perforation diameter, and number of perforations. The calculation ensures that sufficient pressure drop is created to divert fluid across all clusters during hydraulic fracturing. Empirical correlations and computational fluid dynamics (CFD) models are used to predict friction losses. Overestimating friction can lead to excessive treating pressures and operational risk; underestimating can result in poor diversion. Field calibration with pressure data is essential to refine the model and optimize design.
        """,
        key_factors=[
            "Fluid rate and viscosity",
            "Perforation diameter and number",
            "Cluster spacing",
            "CFD modeling accuracy",
            "Field calibration data"
        ],
        primary_authority=[
            "SPE 184880",
            "API RP 19B"
        ],
        burden_holder="Fracturing Engineer",
        adversary_position="Questions necessity of detailed friction calculations.",
        counter_arguments=[
            "Simplified calculations may lead to poor diversion.",
            "Operational risks increase without accurate modeling."
        ],
        resolution_strategy="Use validated models and calibrate with field data.",
        entity_scope="Hydraulic fracturing design teams.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Gun Debris Management and Wellbore Cleanout",
        keywords=["gun debris", "wellbore cleanout", "perforating", "completion", "FRAC03"],
        conclusion_template="Implement debris management and cleanout protocols to maintain wellbore integrity post-perforation.",
        reasoning_framework="""
        Perforating operations generate debris from charge liners, gun carriers, and casing fragments. Effective debris management is essential to prevent equipment malfunction, production impairment, or wellbore obstruction. Cleanout procedures include circulating debris out of the wellbore, deploying debris catchers, and conducting post-perforation wellbore imaging. The design of perforating guns should prioritize minimal debris generation and compatibility with cleanout tools. Regular review of debris management protocols and field experience informs continuous improvement.
        """,
        key_factors=[
            "Debris generation characteristics",
            "Cleanout tool selection",
            "Circulation procedures",
            "Wellbore imaging",
            "Gun design"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions cost and necessity of extensive cleanout.",
        counter_arguments=[
            "Debris can impair production and damage equipment.",
            "Cleanout reduces long-term operational risk."
        ],
        resolution_strategy="Assess debris risk and implement cleanout based on well criticality.",
        entity_scope="Completion and production operations.",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 8.4"
    ),
    DoctrineBlock(
        topic="Oriented Perforating for Fracture Initiation",
        keywords=["oriented perforating", "fracture initiation", "azimuthal control", "FRAC03"],
        conclusion_template="Use oriented perforating to align perforations with preferred fracture azimuth.",
        reasoning_framework="""
        Oriented perforating aligns perforation tunnels with the anticipated fracture azimuth, maximizing fracture complexity and reservoir contact. Orientation is achieved using gyroscopic or magnetic tools, and is particularly valuable in deviated or horizontal wells where natural fracture orientation is known. The effectiveness of oriented perforating depends on tool accuracy, wellbore deviation, and formation stress regime. Field diagnostics and microseismic monitoring validate the impact of orientation on fracture propagation. The approach is most effective when integrated with geomechanical modeling.
        """,
        key_factors=[
            "Fracture azimuth prediction",
            "Tool orientation accuracy",
            "Wellbore deviation",
            "Formation stress regime",
            "Field diagnostics"
        ],
        primary_authority=[
            "SPE 185044",
            "API RP 19B"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions added complexity and cost.",
        counter_arguments=[
            "Improved fracture initiation may justify additional cost.",
            "Orientation may not be critical in isotropic stress environments."
        ],
        resolution_strategy="Conduct cost-benefit analysis and review geomechanical data.",
        entity_scope="Completion and stimulation teams.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 185044"
    ),
    DoctrineBlock(
        topic="Extreme Overbalanced Perforating (EOP)",
        keywords=["extreme overbalanced", "EOP", "perforating", "well control", "FRAC03"],
        conclusion_template="Apply EOP in wells with high overpressure or severe well control requirements.",
        reasoning_framework="""
        Extreme overbalanced perforating (EOP) is used in wells with high formation pressure or when well control is paramount. By maintaining a large overbalance, influx of formation fluids is prevented during perforation, reducing risk of blowout or uncontrolled flow. EOP may result in increased perforation damage and debris, requiring subsequent cleanup. The method is typically reserved for HPHT wells, sour service, or when regulatory requirements dictate. Risk assessment and contingency planning are mandatory, and the approach should be validated with well control specialists.
        """,
        key_factors=[
            "Formation pressure",
            "Well control requirements",
            "Regulatory compliance",
            "Perforation damage risk",
            "Cleanup procedures"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 120779"
        ],
        burden_holder="Wellsite Supervisor",
        adversary_position="Prefers standard overbalanced or underbalanced for reduced damage.",
        counter_arguments=[
            "EOP may increase perforation damage.",
            "Standard methods may not provide adequate well control."
        ],
        resolution_strategy="Conduct risk assessment and consult with well control experts.",
        entity_scope="Wellsite operations and engineering.",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="API RP 19B Section 7.3"
    ),
    DoctrineBlock(
        topic="Cluster Efficiency in Plug-and-Perf Completions",
        keywords=["cluster efficiency", "plug-and-perf", "completion", "hydraulic fracturing", "FRAC03"],
        conclusion_template="Design perforation clusters to maximize stimulation efficiency and reservoir contact.",
        reasoning_framework="""
        Cluster efficiency refers to the proportion of perforation clusters that effectively initiate and propagate fractures during plug-and-perf completions. High cluster efficiency is achieved through optimized shot density, phasing, and limited entry design. Diagnostics such as fiber optics and production logging quantify cluster contribution. Poor efficiency leads to uneven stimulation and suboptimal production. Design should be validated with field data and adjusted iteratively to improve performance.
        """,
        key_factors=[
            "Shot density and phasing",
            "Limited entry design",
            "Cluster spacing",
            "Diagnostic data",
            "Field performance"
        ],
        primary_authority=[
            "SPE 184880",
            "SPE 168632"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Questions necessity of high cluster count.",
        counter_arguments=[
            "Fewer clusters may reduce stimulation efficiency.",
            "High cluster count increases operational complexity."
        ],
        resolution_strategy="Use diagnostics to evaluate and optimize cluster efficiency.",
        entity_scope="Stimulation and completion teams.",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Perforation Design for Hydraulic Fracturing",
        keywords=["perforation design", "hydraulic fracturing", "completion", "FRAC03"],
        conclusion_template="Integrate perforation design with fracturing objectives to maximize reservoir stimulation.",
        reasoning_framework="""
        Effective hydraulic fracturing requires perforation designs that promote uniform fracture initiation and propagation. Key design parameters include shot density, phasing, perforation diameter, and cluster spacing. The design must account for reservoir heterogeneity, stress anisotropy, and operational constraints. Simulation and diagnostic tools guide optimization. Field validation is essential to ensure that design objectives are met and to inform iterative improvement.
        """,
        key_factors=[
            "Shot density and phasing",
            "Perforation diameter",
            "Cluster spacing",
            "Reservoir heterogeneity",
            "Field diagnostics"
        ],
        primary_authority=[
            "SPE 184880",
            "API RP 19B"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers simplified design for operational efficiency.",
        counter_arguments=[
            "Simplified design may compromise stimulation effectiveness.",
            "Complexity may be justified by improved production."
        ],
        resolution_strategy="Balance operational efficiency with stimulation objectives using simulation and diagnostics.",
        entity_scope="Completion and stimulation engineering teams.",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Casing Gun vs Through-Tubing Gun Selection",
        keywords=["casing gun", "through-tubing gun", "perforating", "gun selection", "FRAC03"],
        conclusion_template="Select gun type based on completion configuration and operational constraints.",
        reasoning_framework="""
        Casing guns are deployed before tubing installation and allow for larger diameter charges, maximizing penetration and hole size. Through-tubing guns are used for perforating after tubing is in place, offering operational flexibility for re-perforation or remedial work. The choice depends on completion sequence, required perforation characteristics, and well access. Casing guns are preferred for primary completions, while through-tubing guns are used for interventions or in wells with restricted access. Safety and compatibility with well hardware must be considered.
        """,
        key_factors=[
            "Completion sequence",
            "Required perforation size",
            "Well access and restrictions",
            "Safety considerations",
            "Hardware compatibility"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers through-tubing for operational flexibility.",
        counter_arguments=[
            "Through-tubing guns may have limited performance.",
            "Casing guns offer superior perforation characteristics."
        ],
        resolution_strategy="Evaluate completion objectives and operational constraints before selecting gun type.",
        entity_scope="Completion and intervention teams.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 6.2"
    ),
    DoctrineBlock(
        topic="Perforation Erosion During Hydraulic Fracturing",
        keywords=["perforation erosion", "hydraulic fracturing", "completion", "FRAC03"],
        conclusion_template="Account for perforation erosion in fracturing design to ensure effective stimulation.",
        reasoning_framework="""
        Perforation erosion occurs when high-velocity fracturing fluids enlarge perforation tunnels, altering entry friction and fluid distribution. Erosion can lead to uneven stimulation and reduced cluster efficiency. Design must predict erosion rates based on fluid properties, proppant concentration, and treatment duration. Field diagnostics and post-fracture imaging inform model calibration. Adjusting perforation size and number can mitigate erosion effects and maintain stimulation effectiveness.
        """,
        key_factors=[
            "Fluid velocity and properties",
            "Proppant concentration",
            "Treatment duration",
            "Erosion modeling",
            "Field diagnostics"
        ],
        primary_authority=[
            "SPE 184880",
            "API RP 19B"
        ],
        burden_holder="Fracturing Engineer",
        adversary_position="Questions significance of erosion on overall stimulation.",
        counter_arguments=[
            "Significant erosion can compromise stimulation design.",
            "Neglecting erosion may reduce cluster efficiency."
        ],
        resolution_strategy="Model erosion and validate with field diagnostics.",
        entity_scope="Fracturing and completion engineering teams.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 184880"
    ),
    DoctrineBlock(
        topic="Perforating in HPHT (High Pressure High Temperature) Environments",
        keywords=["HPHT", "high pressure", "high temperature", "perforating", "FRAC03"],
        conclusion_template="Use HPHT-rated perforating systems and validate performance under extreme conditions.",
        reasoning_framework="""
        HPHT environments require perforating systems rated for elevated pressures and temperatures. Charge performance, gun integrity, and tool electronics must be validated for HPHT conditions. Material selection, pressure testing, and thermal cycling are essential. API RP 19B provides guidance on HPHT testing protocols. Operational procedures must address safety, tool reliability, and contingency planning. Field validation and post-job analysis ensure that HPHT-specific risks are managed effectively.
        """,
        key_factors=[
            "Pressure and temperature ratings",
            "Material selection",
            "Tool reliability",
            "API RP 19B HPHT protocols",
            "Safety procedures"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 120779"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions additional cost and complexity of HPHT-rated systems.",
        counter_arguments=[
            "Non-HPHT systems may fail under extreme conditions.",
            "Safety and reliability justify additional investment."
        ],
        resolution_strategy="Select HPHT-rated equipment and validate with field trials.",
        entity_scope="HPHT well operations.",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 10"
    ),
    DoctrineBlock(
        topic="Propellant-Assisted Perforating Systems",
        keywords=["propellant-assisted", "perforating", "stimulation", "FRAC03"],
        conclusion_template="Consider propellant-assisted perforating to enhance near-wellbore fracture complexity.",
        reasoning_framework="""
        Propellant-assisted perforating uses energetic materials to generate additional pressure pulses after perforation, promoting near-wellbore fracture complexity and improved connectivity. The technique is particularly effective in tight formations or when conventional fracturing is limited. Design must ensure compatibility with well hardware and manage safety risks associated with energetic materials. Field trials and diagnostics assess effectiveness. Regulatory compliance and operational safety are paramount.
        """,
        key_factors=[
            "Formation tightness",
            "Compatibility with well hardware",
            "Safety and regulatory compliance",
            "Field diagnostics",
            "Operational procedures"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions safety and regulatory complexity.",
        counter_arguments=[
            "Proper procedures mitigate safety risks.",
            "Enhanced stimulation may justify complexity."
        ],
        resolution_strategy="Conduct risk assessment and field trials before implementation.",
        entity_scope="Completion and stimulation operations.",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="API RP 19B Section 9"
    ),
    DoctrineBlock(
        topic="Abrasive Jetting as Perforating Alternative",
        keywords=["abrasive jetting", "perforating alternative", "completion", "FRAC03"],
        conclusion_template="Evaluate abrasive jetting for perforation in challenging or damaged wells.",
        reasoning_framework="""
        Abrasive jetting uses high-velocity fluid with abrasive particles to create perforations, offering an alternative to explosive charges in wells with damaged casing, restricted access, or high risk of charge misfire. The method allows for precise placement and minimal debris generation. Limitations include lower penetration depth and potential for tool wear. Field trials and comparative analysis with conventional perforating inform selection. Regulatory approval and operational safety must be ensured.
        """,
        key_factors=[
            "Casing condition",
            "Well access restrictions",
            "Penetration depth requirements",
            "Tool wear and maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 168632"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers conventional perforating for proven performance.",
        counter_arguments=[
            "Abrasive jetting may be necessary in damaged wells.",
            "Conventional charges may be unsafe or ineffective."
        ],
        resolution_strategy="Compare performance and risk profiles before selecting method.",
        entity_scope="Completion and intervention teams.",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="API RP 19B Section 11"
    ),
    DoctrineBlock(
        topic="Gun Loading and Safety Procedures",
        keywords=["gun loading", "safety procedures", "perforating", "completion", "FRAC03"],
        conclusion_template="Follow standardized gun loading and safety protocols to prevent accidents.",
        reasoning_framework="""
        Gun loading involves handling and assembling explosive charges, requiring strict adherence to safety protocols. Procedures include controlled environment, use of personal protective equipment (PPE), and compliance with regulatory standards (e.g., ATF, DOT). Training, documentation, and regular audits ensure safety and regulatory compliance. Incident reporting and root cause analysis drive continuous improvement. Safety is prioritized over operational efficiency in all gun loading activities.
        """,
        key_factors=[
            "Explosive handling procedures",
            "PPE and controlled environment",
            "Regulatory compliance",
            "Training and documentation",
            "Incident reporting"
        ],
        primary_authority=[
            "API RP 19B",
            "ATF Regulations"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions time and cost of comprehensive safety protocols.",
        counter_arguments=[
            "Safety incidents have severe consequences.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Enforce strict adherence to protocols and conduct regular safety audits.",
        entity_scope="Perforating and completion operations.",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Tunnel Cleanup and Damage Mitigation",
        keywords=["tunnel cleanup", "damage mitigation", "perforating", "completion", "FRAC03"],
        conclusion_template="Implement cleanup procedures post-perforation to minimize formation damage.",
        reasoning_framework="""
        Perforation tunnels may be filled with debris, mud, or compacted formation material, reducing effective flow area. Cleanup methods include underbalanced perforating, acidizing, and mechanical washing. The choice depends on formation sensitivity, well fluids, and operational constraints. Proper cleanup improves productivity and reduces skin. Field diagnostics and production testing validate effectiveness. Continuous improvement is achieved through post-job analysis.
        """,
        key_factors=[
            "Formation sensitivity",
            "Cleanup method selection",
            "Operational constraints",
            "Field diagnostics",
            "Production testing"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 120779"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions necessity of post-perforation cleanup.",
        counter_arguments=[
            "Neglecting cleanup increases formation damage.",
            "Productivity gains justify additional steps."
        ],
        resolution_strategy="Assess formation damage risk and select appropriate cleanup method.",
        entity_scope="Completion and production operations.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 8.5"
    ),
    DoctrineBlock(
        topic="Perforation Entry Hole Size Optimization",
        keywords=["entry hole size", "optimization", "perforating", "completion", "FRAC03"],
        conclusion_template="Optimize entry hole size to balance productivity and sand control requirements.",
        reasoning_framework="""
        Entry hole size affects near-wellbore pressure drop, sand production, and equipment compatibility. Larger holes reduce pressure drop and improve productivity but may increase sand ingress and risk of screen plugging. Smaller holes provide better sand control but may restrict flow. The optimal size is determined by reservoir properties, sand control strategy, and completion hardware. API RP 19B test data and field experience guide selection.
        """,
        key_factors=[
            "Reservoir properties",
            "Sand control requirements",
            "Completion hardware",
            "API RP 19B test data",
            "Field experience"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers largest possible holes for maximum flow.",
        counter_arguments=[
            "Large holes may compromise sand control.",
            "Smaller holes may reduce productivity."
        ],
        resolution_strategy="Balance productivity and sand control using test data and field results.",
        entity_scope="Completion and sand control teams.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 6.2"
    ),
    DoctrineBlock(
        topic="Perforation Depth Consistency and Quality Assurance",
        keywords=["perforation depth", "consistency", "quality assurance", "perforating", "FRAC03"],
        conclusion_template="Ensure consistent perforation depth through QA/QC of charges and gun systems.",
        reasoning_framework="""
        Consistent perforation depth is critical for uniform stimulation and well productivity. QA/QC procedures include charge lot testing, gun assembly inspection, and post-job evaluation. Deviations may result from charge variability, gun misalignment, or operational errors. Regular audits and adherence to API RP 19B protocols ensure quality. Field diagnostics and imaging provide feedback for continuous improvement.
        """,
        key_factors=[
            "Charge lot testing",
            "Gun assembly inspection",
            "Operational procedures",
            "API RP 19B compliance",
            "Field diagnostics"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions cost of extensive QA/QC.",
        counter_arguments=[
            "Inconsistent depth reduces stimulation effectiveness.",
            "QA/QC prevents costly remedial work."
        ],
        resolution_strategy="Enforce QA/QC protocols and review field performance data.",
        entity_scope="Perforating and completion operations.",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 6.3"
    ),
    DoctrineBlock(
        topic="Perforation Phasing for Sand Control Completions",
        keywords=["phasing", "sand control", "perforating", "completion", "FRAC03"],
        conclusion_template="Select phasing to minimize sand production and optimize inflow in sand control completions.",
        reasoning_framework="""
        In sand control completions, phasing affects inflow distribution and sand production risk. Even phasing (e.g., 120° or 90°) promotes uniform inflow, reducing localized sand influx. Phasing must be compatible with screen or gravel pack hardware. Field experience and simulation guide selection. The approach balances productivity and sand control objectives.
        """,
        key_factors=[
            "Sand control hardware",
            "Inflow distribution",
            "Sand production risk",
            "Field experience",
            "Simulation results"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 168632"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers phasing for maximum productivity.",
        counter_arguments=[
            "Productivity gains may increase sand risk.",
            "Sand control objectives take precedence."
        ],
        resolution_strategy="Optimize phasing using simulation and field diagnostics.",
        entity_scope="Sand control and completion teams.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 6.4"
    ),
    DoctrineBlock(
        topic="Perforation Gun Debris Characterization",
        keywords=["gun debris", "characterization", "perforating", "completion", "FRAC03"],
        conclusion_template="Characterize gun debris to inform cleanout and risk mitigation strategies.",
        reasoning_framework="""
        Gun debris characterization involves analyzing size, composition, and distribution of debris generated during perforation. Data informs cleanout tool selection, risk assessment, and operational planning. API RP 19B outlines debris measurement protocols. Field experience and post-job analysis refine debris management strategies, reducing risk of equipment malfunction or wellbore obstruction.
        """,
        key_factors=[
            "Debris size and composition",
            "Measurement protocols",
            "Cleanout tool compatibility",
            "Operational risk",
            "Field analysis"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions necessity of detailed debris analysis.",
        counter_arguments=[
            "Debris can impair production and equipment.",
            "Characterization informs risk mitigation."
        ],
        resolution_strategy="Conduct debris analysis and adjust cleanout protocols as needed.",
        entity_scope="Completion and production operations.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 8.4"
    ),
    DoctrineBlock(
        topic="Perforation Charge Selection for Multi-Stage Fracturing",
        keywords=["charge selection", "multi-stage fracturing", "perforating", "completion", "FRAC03"],
        conclusion_template="Select charges compatible with multi-stage fracturing objectives and operational constraints.",
        reasoning_framework="""
        Multi-stage fracturing requires charges that provide consistent penetration and entry hole size across all stages. Selection is based on formation properties, casing thickness, and stimulation objectives. API RP 19B test data and field trials guide charge selection. Compatibility with limited entry and cluster efficiency objectives is critical. Regular review of performance data ensures continuous optimization.
        """,
        key_factors=[
            "Formation properties",
            "Casing thickness",
            "Stimulation objectives",
            "API RP 19B test data",
            "Cluster efficiency"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 184880"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers standard charges for simplicity.",
        counter_arguments=[
            "Standard charges may not meet multi-stage requirements.",
            "Optimized charges improve stimulation effectiveness."
        ],
        resolution_strategy="Review test data and field performance before selecting charges.",
        entity_scope="Completion and stimulation engineering teams.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 6.2"
    ),
    DoctrineBlock(
        topic="Perforation Debris Impact on Artificial Lift Systems",
        keywords=["debris", "artificial lift", "perforating", "completion", "FRAC03"],
        conclusion_template="Mitigate perforation debris to protect artificial lift equipment and maintain production.",
        reasoning_framework="""
        Perforation debris can damage artificial lift systems (e.g., ESPs, PCPs, rod pumps) by causing abrasion, plugging, or mechanical failure. Debris management strategies include pre-job planning, debris catchers, and post-perforation cleanout. Equipment selection should consider debris tolerance. Field diagnostics and maintenance records inform continuous improvement. The objective is to minimize downtime and equipment failure.
        """,
        key_factors=[
            "Debris generation and management",
            "Artificial lift equipment tolerance",
            "Cleanout procedures",
            "Field diagnostics",
            "Maintenance records"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Production Engineer",
        adversary_position="Questions cost of extensive debris mitigation.",
        counter_arguments=[
            "Equipment failure leads to costly downtime.",
            "Debris mitigation reduces long-term costs."
        ],
        resolution_strategy="Assess debris risk and implement mitigation based on equipment sensitivity.",
        entity_scope="Production and completion operations.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 8.4"
    ),
    DoctrineBlock(
        topic="Perforation Gun Selection for Ultra-Deep Wells",
        keywords=["gun selection", "ultra-deep wells", "perforating", "completion", "FRAC03"],
        conclusion_template="Select guns rated for ultra-deep well conditions and validate deployment procedures.",
        reasoning_framework="""
        Ultra-deep wells require guns with high pressure and temperature ratings, robust mechanical integrity, and reliable deployment systems. Selection criteria include tool length, diameter, pressure rating, and compatibility with well hardware. API RP 19B and field trials guide selection. Deployment procedures must address conveyance challenges, pressure control, and contingency planning. Post-job analysis ensures continuous improvement.
        """,
        key_factors=[
            "Pressure and temperature ratings",
            "Mechanical integrity",
            "Deployment procedures",
            "API RP 19B test data",
            "Field trials"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 120779"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions cost and complexity of ultra-deep rated guns.",
        counter_arguments=[
            "Non-rated guns may fail under extreme conditions.",
            "Safety and reliability justify additional investment."
        ],
        resolution_strategy="Select ultra-deep rated equipment and validate with field trials.",
        entity_scope="Ultra-deep well operations.",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 10"
    ),
    DoctrineBlock(
        topic="Perforation Damage Mechanisms and Remediation",
        keywords=["damage mechanisms", "remediation", "perforating", "completion", "FRAC03"],
        conclusion_template="Identify and remediate perforation damage to restore productivity.",
        reasoning_framework="""
        Perforation damage mechanisms include crushed zone formation, debris plugging, and chemical alteration. Remediation methods include acidizing, solvent washes, and mechanical cleanout. Diagnosis is based on production testing, well logs, and imaging. The remediation plan should be tailored to the identified damage mechanism and validated with post-treatment diagnostics.
        """,
        key_factors=[
            "Damage mechanism identification",
            "Remediation method selection",
            "Production testing",
            "Well logs and imaging",
            "Post-treatment diagnostics"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 120779"
        ],
        burden_holder="Production Engineer",
        adversary_position="Questions cost-effectiveness of remediation.",
        counter_arguments=[
            "Unremediated damage reduces long-term productivity.",
            "Remediation may restore or enhance production."
        ],
        resolution_strategy="Diagnose damage and select cost-effective remediation method.",
        entity_scope="Production and completion operations.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 8.5"
    ),
    DoctrineBlock(
        topic="Perforation Gun Pressure Control and Safety",
        keywords=["gun pressure control", "safety", "perforating", "completion", "FRAC03"],
        conclusion_template="Implement pressure control protocols to ensure safe gun deployment and retrieval.",
        reasoning_framework="""
        Pressure control during gun deployment and retrieval prevents well control incidents and equipment damage. Protocols include use of lubricators, blowout preventers (BOPs), and pressure monitoring. Training and adherence to standard operating procedures are essential. Incident reporting and root cause analysis inform continuous improvement. Regulatory compliance is mandatory.
        """,
        key_factors=[
            "Pressure control equipment",
            "Standard operating procedures",
            "Training and documentation",
            "Incident reporting",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 19B",
            "OSHA Regulations"
        ],
        burden_holder="Wellsite Supervisor",
        adversary_position="Questions time and cost of comprehensive pressure control.",
        counter_arguments=[
            "Pressure incidents have severe consequences.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Enforce pressure control protocols and conduct regular safety audits.",
        entity_scope="Perforating and completion operations.",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Gun Conveyance in Extended Reach Wells",
        keywords=["gun conveyance", "extended reach wells", "perforating", "completion", "FRAC03"],
        conclusion_template="Select conveyance method compatible with extended reach well geometry and operational constraints.",
        reasoning_framework="""
        Extended reach wells present unique conveyance challenges due to high deviation, long lateral sections, and frictional drag. TCP is often preferred, but coiled tubing or tractor conveyance may be required. Selection depends on well geometry, gun size, and operational risk. Pre-job modeling and field trials inform decision. Safety and contingency planning are critical.
        """,
        key_factors=[
            "Well geometry and deviation",
            "Gun size and weight",
            "Conveyance method compatibility",
            "Operational risk",
            "Field trials"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 187451"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Prefers wireline for simplicity.",
        counter_arguments=[
            "Wireline may not reach target depth.",
            "Alternative conveyance ensures access."
        ],
        resolution_strategy="Model conveyance options and validate with field trials.",
        entity_scope="Extended reach well operations.",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 187451"
    ),
    DoctrineBlock(
        topic="Perforation Gun Selection for Sour Service Wells",
        keywords=["gun selection", "sour service", "perforating", "completion", "FRAC03"],
        conclusion_template="Use sour service-rated guns and charges to ensure safety and equipment integrity.",
        reasoning_framework="""
        Sour service wells (containing H2S) require guns and charges with corrosion-resistant materials and validated performance in sour environments. API RP 19B provides guidance on material selection and testing. Operational procedures must address safety, regulatory compliance, and contingency planning. Field validation and post-job analysis ensure continuous improvement.
        """,
        key_factors=[
            "Material corrosion resistance",
            "API RP 19B sour service protocols",
            "Safety procedures",
            "Regulatory compliance",
            "Field validation"
        ],
        primary_authority=[
            "API RP 19B",
            "NACE MR0175"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions additional cost and complexity of sour service-rated systems.",
        counter_arguments=[
            "Non-rated systems may fail or pose safety risk.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Select sour service-rated equipment and validate with field trials.",
        entity_scope="Sour service well operations.",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 10"
    ),
    DoctrineBlock(
        topic="Perforation Gun Firing Systems and Redundancy",
        keywords=["gun firing systems", "redundancy", "perforating", "completion", "FRAC03"],
        conclusion_template="Implement redundant firing systems to ensure successful perforation in critical wells.",
        reasoning_framework="""
        Redundant firing systems (e.g., dual initiators, backup detonators) increase reliability in critical or high-cost wells. Selection depends on well criticality, operational risk, and regulatory requirements. API RP 19B and manufacturer guidelines inform system design. Field experience and post-job analysis validate effectiveness. Cost-benefit analysis guides implementation.
        """,
        key_factors=[
            "Well criticality",
            "Operational risk",
            "API RP 19B and manufacturer guidelines",
            "Field experience",
            "Cost-benefit analysis"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions cost and complexity of redundancy.",
        counter_arguments=[
            "Redundancy reduces risk of misfire.",
            "Critical wells justify additional investment."
        ],
        resolution_strategy="Assess well criticality and implement redundancy as needed.",
        entity_scope="Critical well operations.",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Gun Temperature Management",
        keywords=["gun temperature", "management", "perforating", "completion", "FRAC03"],
        conclusion_template="Manage gun temperature exposure to maintain charge performance and safety.",
        reasoning_framework="""
        High downhole temperatures can degrade charge performance and compromise gun safety. Temperature management includes selecting temperature-rated charges, minimizing surface exposure, and monitoring downhole conditions. API RP 19B provides test protocols for high-temperature performance. Field diagnostics and post-job analysis inform continuous improvement.
        """,
        key_factors=[
            "Downhole temperature",
            "Charge temperature rating",
            "Surface exposure management",
            "API RP 19B protocols",
            "Field diagnostics"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 120779"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions necessity of temperature management in moderate wells.",
        counter_arguments=[
            "Unexpected temperature spikes can compromise safety.",
            "Temperature-rated charges ensure reliability."
        ],
        resolution_strategy="Monitor temperature and select appropriate charges for well conditions.",
        entity_scope="Completion and perforating operations.",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 10"
    ),
    DoctrineBlock(
        topic="Perforation Gun Debris Impact on Well Integrity",
        keywords=["gun debris", "well integrity", "perforating", "completion", "FRAC03"],
        conclusion_template="Mitigate gun debris to preserve well integrity and prevent operational issues.",
        reasoning_framework="""
        Gun debris can compromise well integrity by obstructing flow paths, damaging equipment, or causing casing wear. Debris management strategies include gun design optimization, debris catchers, and post-perforation cleanout. API RP 19B outlines debris measurement and mitigation protocols. Field diagnostics and incident analysis inform continuous improvement.
        """,
        key_factors=[
            "Debris generation and management",
            "Well integrity risk assessment",
            "API RP 19B protocols",
            "Field diagnostics",
            "Incident analysis"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions cost of comprehensive debris mitigation.",
        counter_arguments=[
            "Well integrity is critical for safe operations.",
            "Debris mitigation reduces long-term risk."
        ],
        resolution_strategy="Implement debris mitigation protocols and review field performance.",
        entity_scope="Completion and well integrity teams.",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 8.4"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Compatibility with Well Hardware",
        keywords=["gun system", "compatibility", "well hardware", "perforating", "completion", "FRAC03"],
        conclusion_template="Ensure gun system compatibility with well hardware to prevent operational issues.",
        reasoning_framework="""
        Gun system compatibility includes physical dimensions, pressure ratings, and connection types. Incompatible systems can cause deployment failure, equipment damage, or safety incidents. Pre-job planning, hardware verification, and API RP 19B compliance ensure compatibility. Field experience and incident analysis inform continuous improvement.
        """,
        key_factors=[
            "Physical dimensions",
            "Pressure ratings",
            "Connection types",
            "Pre-job planning",
            "API RP 19B compliance"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions necessity of detailed compatibility checks.",
        counter_arguments=[
            "Incompatibility can cause costly failures.",
            "Compatibility checks prevent operational issues."
        ],
        resolution_strategy="Conduct compatibility checks during planning and pre-job verification.",
        entity_scope="Completion and perforating operations.",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 6.2"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Maintenance and Inspection",
        keywords=["gun system", "maintenance", "inspection", "perforating", "completion", "FRAC03"],
        conclusion_template="Implement regular maintenance and inspection to ensure gun system reliability.",
        reasoning_framework="""
        Regular maintenance and inspection of gun systems prevent operational failures and safety incidents. Procedures include visual inspection, functional testing, and documentation. API RP 19B and manufacturer guidelines inform maintenance schedules. Incident reporting and root cause analysis drive continuous improvement.
        """,
        key_factors=[
            "Maintenance schedules",
            "Inspection procedures",
            "API RP 19B and manufacturer guidelines",
            "Incident reporting",
            "Documentation"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions cost and time of regular maintenance.",
        counter_arguments=[
            "Maintenance prevents costly failures.",
            "Reliability justifies investment."
        ],
        resolution_strategy="Follow maintenance schedules and review incident data.",
        entity_scope="Perforating and completion operations.",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Redress and Reuse",
        keywords=["gun system", "redress", "reuse", "perforating", "completion", "FRAC03"],
        conclusion_template="Redress and reuse gun systems only after thorough inspection and compliance with standards.",
        reasoning_framework="""
        Redressing and reusing gun systems can reduce costs but must not compromise safety or performance. Inspection for mechanical integrity, corrosion, and residual explosives is mandatory. API RP 19B and manufacturer guidelines inform redress procedures. Documentation and traceability are essential. Field experience and incident analysis guide continuous improvement.
        """,
        key_factors=[
            "Mechanical integrity",
            "Corrosion inspection",
            "Residual explosives check",
            "API RP 19B and manufacturer guidelines",
            "Documentation"
        ],
        primary_authority=[
            "API RP 19B",
            "SPE 185044"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions cost-effectiveness of redress procedures.",
        counter_arguments=[
            "Improper redress can cause failures.",
            "Safety and reliability justify procedures."
        ],
        resolution_strategy="Follow redress procedures and maintain documentation.",
        entity_scope="Perforating and completion operations.",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Explosive Traceability",
        keywords=["gun system", "explosive traceability", "perforating", "completion", "FRAC03"],
        conclusion_template="Maintain explosive traceability for regulatory compliance and safety.",
        reasoning_framework="""
        Explosive traceability ensures accountability and regulatory compliance (e.g., ATF, DOT). Procedures include documentation of explosive lot numbers, chain of custody, and usage records. Incident reporting and audits are mandatory. API RP 19B and regulatory guidelines inform traceability protocols. Field experience and incident analysis drive continuous improvement.
        """,
        key_factors=[
            "Explosive lot documentation",
            "Chain of custody",
            "Regulatory compliance",
            "API RP 19B and regulatory guidelines",
            "Incident reporting"
        ],
        primary_authority=[
            "API RP 19B",
            "ATF Regulations"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions administrative burden of traceability.",
        counter_arguments=[
            "Traceability is required by law.",
            "Ensures safety and accountability."
        ],
        resolution_strategy="Maintain documentation and conduct regular audits.",
        entity_scope="Perforating and completion operations.",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Environmental Impact Mitigation",
        keywords=["gun system", "environmental impact", "mitigation", "perforating", "completion", "FRAC03"],
        conclusion_template="Mitigate environmental impact of perforating operations through best practices.",
        reasoning_framework="""
        Perforating operations can generate waste, noise, and emissions. Environmental mitigation includes proper disposal of spent guns and debris, noise abatement, and emissions control. Compliance with local regulations and API RP 19B guidelines is mandatory. Environmental monitoring and incident reporting inform continuous improvement.
        """,
        key_factors=[
            "Waste disposal procedures",
            "Noise abatement",
            "Emissions control",
            "Regulatory compliance",
            "Environmental monitoring"
        ],
        primary_authority=[
            "API RP 19B",
            "Local Environmental Regulations"
        ],
        burden_holder="Completion Engineer",
        adversary_position="Questions cost of environmental mitigation.",
        counter_arguments=[
            "Environmental compliance is mandatory.",
            "Mitigation reduces long-term liability."
        ],
        resolution_strategy="Implement mitigation measures and monitor environmental impact.",
        entity_scope="Perforating and completion operations.",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 13"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Logistics and Supply Chain Management",
        keywords=["gun system", "logistics", "supply chain", "perforating", "completion", "FRAC03"],
        conclusion_template="Optimize logistics and supply chain management to ensure timely and safe gun delivery.",
        reasoning_framework="""
        Efficient logistics and supply chain management ensure timely delivery of gun systems and explosives, minimizing project delays. Procedures include inventory management, transportation planning, and regulatory compliance (e.g., ATF, DOT). Incident reporting and audits inform continuous improvement. API RP 19B and industry best practices guide logistics planning.
        """,
        key_factors=[
            "Inventory management",
            "Transportation planning",
            "Regulatory compliance",
            "API RP 19B and industry best practices",
            "Incident reporting"
        ],
        primary_authority=[
            "API RP 19B",
            "ATF Regulations"
        ],
        burden_holder="Logistics Coordinator",
        adversary_position="Questions cost of comprehensive logistics planning.",
        counter_arguments=[
            "Delays can cause costly project overruns.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Implement logistics planning and conduct regular audits.",
        entity_scope="Perforating and completion operations.",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 14"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Training and Competency",
        keywords=["gun system", "training", "competency", "perforating", "completion", "FRAC03"],
        conclusion_template="Ensure personnel are trained and competent in gun system operations.",
        reasoning_framework="""
        Training and competency are critical for safe and effective gun system operations. Procedures include formal training, competency assessments, and refresher courses. API RP 19B and company policies inform training requirements. Incident reporting and performance reviews drive continuous improvement. Documentation and certification are mandatory.
        """,
        key_factors=[
            "Formal training programs",
            "Competency assessments",
            "API RP 19B and company policies",
            "Incident reporting",
            "Documentation"
        ],
        primary_authority=[
            "API RP 19B",
            "Company Training Policies"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions time and cost of training programs.",
        counter_arguments=[
            "Training reduces risk of incidents.",
            "Competency ensures operational effectiveness."
        ],
        resolution_strategy="Implement training programs and maintain competency records.",
        entity_scope="Perforating and completion operations.",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Incident Investigation and Reporting",
        keywords=["gun system", "incident investigation", "reporting", "perforating", "completion", "FRAC03"],
        conclusion_template="Investigate and report all gun system incidents to drive safety and performance improvement.",
        reasoning_framework="""
        Incident investigation and reporting identify root causes and inform corrective actions. Procedures include immediate reporting, root cause analysis, and documentation. API RP 19B and company policies guide investigation protocols. Lessons learned are shared to prevent recurrence. Regulatory compliance is mandatory.
        """,
        key_factors=[
            "Immediate reporting",
            "Root cause analysis",
            "API RP 19B and company policies",
            "Documentation",
            "Lessons learned"
        ],
        primary_authority=[
            "API RP 19B",
            "Company HSE Policies"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions administrative burden of incident reporting.",
        counter_arguments=[
            "Incident reporting prevents recurrence.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Implement reporting protocols and share lessons learned.",
        entity_scope="Perforating and completion operations.",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
    ),
    DoctrineBlock(
        topic="Perforation Gun System Documentation and Record Keeping",
        keywords=["gun system", "documentation", "record keeping", "perforating", "completion", "FRAC03"],
        conclusion_template="Maintain comprehensive documentation and records for all gun system operations.",
        reasoning_framework="""
        Documentation and record keeping ensure traceability, regulatory compliance, and operational efficiency. Procedures include job reports, explosive usage records, maintenance logs, and incident reports. API RP 19B and regulatory guidelines inform documentation requirements. Regular audits and reviews drive continuous improvement.
        """,
        key_factors=[
            "Job reports",
            "Explosive usage records",
            "Maintenance logs",
            "Incident reports",
            "API RP 19B and regulatory guidelines"
        ],
        primary_authority=[
            "API RP 19B",
            "ATF Regulations"
        ],
        burden_holder="Perforating Supervisor",
        adversary_position="Questions administrative burden of record keeping.",
        counter_arguments=[
            "Documentation is required by law.",
            "Ensures operational efficiency and accountability."
        ],
        resolution_strategy="Maintain records and conduct regular audits.",
        entity_scope="Perforating and completion operations.",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 19B Section 12"
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