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
        topic="ESP Selection and Sizing",
        keywords=["ESP", "Selection", "Sizing", "Artificial Lift", "Pump", "Well"],
        conclusion_template="The recommended ESP configuration for well {well_id} is {esp_model} with a motor rated at {hp} HP, based on reservoir and production parameters.",
        reasoning_framework=(
            "Selection and sizing of Electric Submersible Pumps (ESP) is guided by a systematic evaluation of reservoir production "
            "requirements, fluid properties, well geometry, and expected flow rates. The process begins with a detailed analysis of "
            "well inflow performance (IPR), followed by calculation of required pump capacity and head. Fluid characteristics such as "
            "viscosity, gas content, and solids are assessed to determine compatibility with ESP components. The selection matrix "
            "incorporates manufacturer performance curves, motor sizing (HP and voltage), and cable specifications. Sizing is validated "
            "against anticipated production decline and operational constraints. The doctrine mandates adherence to API RP 11S2 and "
            "manufacturer guidelines, with iterative review for optimization. Key decision points include pump stage count, motor load, "
            "and cable ampacity. The doctrine emphasizes risk mitigation for gas lock, scaling, and sand production. Final selection is "
            "subject to peer review and field validation, with documentation of all assumptions and calculations."
        ),
        key_factors=[
            "Reservoir inflow performance (IPR)",
            "Fluid properties (viscosity, gas content, solids)",
            "Required flow rate and head",
            "Well geometry",
            "Pump performance curves",
            "Motor sizing",
            "Cable specifications",
            "Operational constraints",
            "Production decline forecast"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer ESP selection guides",
            "SPE 53827",
            "Petroleum Engineering Handbook, Chapter 13"
        ],
        burden_holder="Production Engineer",
        adversary_position="ESP selection may be oversized, leading to inefficiency and premature failure.",
        counter_arguments=[
            "Oversizing mitigates risk of production decline.",
            "Conservative selection ensures operational flexibility.",
            "Manufacturer recommendations support larger pump sizing."
        ],
        resolution_strategy="Iterative review with field validation and peer consultation; adherence to API standards.",
        entity_scope="Well-level ESP application",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 3.1"
    ),
    DoctrineBlock(
        topic="ESP Performance Curve Analysis",
        keywords=["ESP", "Performance Curve", "Pump Efficiency", "Head", "Flowrate"],
        conclusion_template="The ESP performance curve for {esp_model} indicates optimal operation at {flowrate} bpd and {head} ft.",
        reasoning_framework=(
            "ESP performance curve analysis is central to optimizing pump operation and longevity. The doctrine requires plotting "
            "manufacturer-supplied curves for head, efficiency, and power consumption against flowrate. The intersection of the well's "
            "required head and flowrate with the pump curve determines operational feasibility. Analysis includes evaluation of best "
            "efficiency point (BEP), avoidance of operation at extremes (runout or shutoff), and consideration of gas handling capacity. "
            "The doctrine mandates cross-checking actual field data with predicted performance, adjusting for fluid density and viscosity. "
            "Performance degradation due to scaling, wear, or gas lock is monitored via periodic curve re-evaluation. The doctrine "
            "emphasizes continuous monitoring and adjustment, leveraging SCADA data and field feedback."
        ),
        key_factors=[
            "Pump head vs. flowrate",
            "Efficiency curve",
            "Power consumption",
            "Gas handling capability",
            "Field data comparison",
            "Fluid properties"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer performance curves",
            "SPE 53827",
            "Petroleum Engineering Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Performance curves may not reflect real-world conditions due to fluid variability.",
        counter_arguments=[
            "Curves are adjusted for field-specific fluid properties.",
            "Continuous monitoring allows for real-time correction.",
            "Manufacturer curves are validated by extensive testing."
        ],
        resolution_strategy="Regular field validation and curve adjustment; use of SCADA for real-time performance tracking.",
        entity_scope="ESP operation in producing wells",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 4.2"
    ),
    DoctrineBlock(
        topic="ESP Motor, Protector, Intake, and Cable Design",
        keywords=["ESP", "Motor", "Protector", "Intake", "Cable", "Design"],
        conclusion_template="The ESP motor, protector, intake, and cable design for well {well_id} meets operational and environmental requirements.",
        reasoning_framework=(
            "Design of ESP motor, protector, intake, and cable is governed by operational load, environmental conditions, and compatibility "
            "with well fluids. Motor selection is based on required horsepower, voltage, and cooling requirements. Protector design ensures "
            "isolation of motor from well fluids, preventing contamination and pressure imbalance. Intake configuration is tailored to fluid "
            "entry, minimizing gas lock and sand ingress. Cable design considers ampacity, voltage drop, and mechanical protection, with "
            "reference to API RP 11S5. The doctrine mandates selection of corrosion-resistant materials, proper cable routing, and "
            "compliance with manufacturer recommendations. Field-specific adjustments are made for high-temperature, high-gas, or abrasive "
            "environments. Documentation of all design parameters and field validation is required."
        ),
        key_factors=[
            "Motor horsepower and voltage",
            "Protector sealing and pressure balance",
            "Intake configuration",
            "Cable ampacity and voltage drop",
            "Corrosion resistance",
            "Environmental compatibility"
        ],
        primary_authority=[
            "API RP 11S5",
            "Manufacturer ESP component guides",
            "SPE 53827",
            "Petroleum Engineering Handbook"
        ],
        burden_holder="Production Engineer",
        adversary_position="Design may fail under extreme conditions, leading to ESP failure.",
        counter_arguments=[
            "Design incorporates field-specific adjustments.",
            "Materials selected for corrosion and abrasion resistance.",
            "Manufacturer guidelines ensure reliability."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP system design for producing wells",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S5 Section 2.1"
    ),
    DoctrineBlock(
        topic="ESP Gas Handling: Gas Separator and Charge Trap",
        keywords=["ESP", "Gas Handling", "Gas Separator", "Charge Trap", "Gas Lock"],
        conclusion_template="The ESP gas handling system for well {well_id} is optimized with a gas separator and charge trap to mitigate gas lock.",
        reasoning_framework=(
            "ESP gas handling doctrine mandates the use of gas separators and charge traps to prevent gas lock and maintain pump efficiency. "
            "Gas separator selection is based on expected gas-liquid ratio (GLR), separator efficiency, and compatibility with ESP intake. "
            "Charge traps are employed to stabilize pressure and prevent gas migration into the pump stages. The doctrine requires "
            "assessment of reservoir gas content, production rate, and separator performance curves. Field validation includes monitoring "
            "for signs of gas lock, such as erratic pump operation and reduced flowrate. Design is adjusted for high-GLR wells, with "
            "consideration of separator geometry and charge trap placement. Manufacturer recommendations and API RP 11S2 are followed."
        ),
        key_factors=[
            "Gas-liquid ratio (GLR)",
            "Separator efficiency",
            "Charge trap effectiveness",
            "Pump intake configuration",
            "Field monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer gas separator guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Gas handling systems may not prevent gas lock in high-GLR wells.",
        counter_arguments=[
            "Design incorporates enhanced separator and charge trap configurations.",
            "Continuous monitoring allows for rapid response to gas lock.",
            "Manufacturer recommendations are field-proven."
        ],
        resolution_strategy="Field validation, iterative design adjustment, and adherence to API standards.",
        entity_scope="ESP gas handling in producing wells",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 5.1"
    ),
    DoctrineBlock(
        topic="ESP Variable Speed Drive (VSD) Frequency Optimization",
        keywords=["ESP", "Variable Speed Drive", "VSD", "Frequency", "Optimization"],
        conclusion_template="The optimal VSD frequency for ESP operation in well {well_id} is {frequency} Hz, maximizing pump efficiency and run life.",
        reasoning_framework=(
            "Optimization of ESP Variable Speed Drive (VSD) frequency is critical for maximizing pump efficiency and extending run life. "
            "The doctrine requires analysis of pump performance curves at varying frequencies, assessment of motor load, and monitoring of "
            "vibration and heat generation. Frequency adjustment is guided by production rate, reservoir inflow, and fluid properties. "
            "The doctrine mandates use of SCADA systems for real-time monitoring and adjustment, with reference to manufacturer guidelines "
            "for safe operating ranges. VSD optimization includes ramp-up and ramp-down protocols to minimize mechanical stress. Field "
            "validation is performed through periodic review of pump performance and failure rates. Documentation of all frequency "
            "adjustments and operational outcomes is required."
        ),
        key_factors=[
            "Pump performance at varying frequencies",
            "Motor load and efficiency",
            "Vibration and heat generation",
            "Production rate",
            "SCADA monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer VSD guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="VSD frequency optimization may induce mechanical stress and reduce ESP run life.",
        counter_arguments=[
            "Ramp-up and ramp-down protocols minimize stress.",
            "Continuous monitoring allows for real-time adjustment.",
            "Manufacturer guidelines ensure safe operation."
        ],
        resolution_strategy="Periodic field validation and adjustment; adherence to manufacturer and API standards.",
        entity_scope="ESP operation with VSD in producing wells",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 6.2"
    ),
    DoctrineBlock(
        topic="Rod Pump Sucker Rod and Beam Unit Design",
        keywords=["Rod Pump", "Sucker Rod", "Beam Unit", "Design", "Artificial Lift"],
        conclusion_template="The sucker rod and beam unit design for well {well_id} meets API RP 11B requirements and optimizes production.",
        reasoning_framework=(
            "Design of rod pump sucker rod and beam unit is governed by API RP 11B and field-specific production requirements. The doctrine "
            "requires calculation of rod string load, selection of rod material (steel, fiberglass), and sizing based on well depth and "
            "production rate. Beam unit design incorporates stroke length, strokes per minute, and counterbalance. The doctrine mandates "
            "evaluation of fatigue life, corrosion resistance, and compatibility with produced fluids. Manufacturer recommendations are "
            "followed for rod coupling and beam unit configuration. Field validation includes monitoring for rod wear, breakage, and "
            "beam unit performance. Documentation of all design parameters and operational outcomes is required."
        ),
        key_factors=[
            "Rod string load",
            "Rod material selection",
            "Well depth",
            "Production rate",
            "Beam unit stroke length and frequency",
            "Corrosion resistance"
        ],
        primary_authority=[
            "API RP 11B",
            "Manufacturer rod pump guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Rod and beam unit design may not withstand fatigue and corrosion, leading to frequent failures.",
        counter_arguments=[
            "Design incorporates fatigue and corrosion analysis.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Rod pump operation in producing wells",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11B Section 2.1"
    ),
    DoctrineBlock(
        topic="Rod Pump Dynamometer Card Interpretation",
        keywords=["Rod Pump", "Dynamometer Card", "Interpretation", "Artificial Lift"],
        conclusion_template="The dynamometer card analysis for well {well_id} indicates {failure_mode} and recommends corrective action.",
        reasoning_framework=(
            "Interpretation of rod pump dynamometer cards is essential for diagnosing pump performance and failure modes. The doctrine "
            "requires analysis of surface and downhole cards, identification of characteristic shapes (normal, pump-off, gas interference, "
            "fluid pound), and correlation with production data. The doctrine mandates use of specialized software for card analysis, "
            "with reference to API RP 11BR. Field validation includes comparison of card interpretation with observed well behavior. "
            "Corrective actions are recommended based on diagnosed failure mode, such as adjusting stroke length, frequency, or rod string "
            "configuration. Documentation of all interpretations and actions is required."
        ),
        key_factors=[
            "Dynamometer card shape",
            "Production data correlation",
            "Failure mode identification",
            "Corrective action",
            "Field validation"
        ],
        primary_authority=[
            "API RP 11BR",
            "Manufacturer dynamometer guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Card interpretation may be subjective and lead to incorrect diagnosis.",
        counter_arguments=[
            "Use of specialized software reduces subjectivity.",
            "Field validation ensures accuracy.",
            "API standards provide authoritative guidance."
        ],
        resolution_strategy="Peer review and field validation; adherence to API standards.",
        entity_scope="Rod pump operation in producing wells",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11BR Section 3.1"
    ),
    DoctrineBlock(
        topic="Rod Pump Rod String Design (API RP 11BR)",
        keywords=["Rod Pump", "Rod String", "Design", "API RP 11BR", "Artificial Lift"],
        conclusion_template="The rod string design for well {well_id} complies with API RP 11BR and optimizes production and run life.",
        reasoning_framework=(
            "Rod string design is governed by API RP 11BR, requiring calculation of rod load, selection of material and diameter, and "
            "configuration for well depth and production rate. The doctrine mandates evaluation of fatigue life, corrosion resistance, "
            "and compatibility with produced fluids. Manufacturer recommendations are followed for rod coupling and string configuration. "
            "Field validation includes monitoring for rod wear, breakage, and production performance. Documentation of all design "
            "parameters and operational outcomes is required."
        ),
        key_factors=[
            "Rod load calculation",
            "Material and diameter selection",
            "Well depth",
            "Production rate",
            "Corrosion resistance",
            "Fatigue life"
        ],
        primary_authority=[
            "API RP 11BR",
            "Manufacturer rod pump guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Rod string design may fail under high load or corrosive conditions.",
        counter_arguments=[
            "Design incorporates fatigue and corrosion analysis.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Rod pump operation in producing wells",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11BR Section 2.1"
    ),
    DoctrineBlock(
        topic="Rod Pump Pump-Off Controller (POC) Optimization",
        keywords=["Rod Pump", "Pump-Off Controller", "POC", "Optimization", "Artificial Lift"],
        conclusion_template="The POC settings for well {well_id} are optimized to minimize pump-off and maximize production.",
        reasoning_framework=(
            "Optimization of rod pump Pump-Off Controller (POC) settings is essential for maximizing production and minimizing pump-off "
            "events. The doctrine requires analysis of production rate, well inflow, and dynamometer card data. POC settings are adjusted "
            "based on observed pump-off frequency, fluid level, and rod load. Manufacturer recommendations and API RP 11BR are followed "
            "for safe operating ranges. Field validation includes monitoring for pump-off events, production decline, and rod wear. "
            "Documentation of all POC adjustments and operational outcomes is required."
        ),
        key_factors=[
            "Production rate",
            "Well inflow",
            "Dynamometer card data",
            "POC settings",
            "Pump-off frequency",
            "Rod load"
        ],
        primary_authority=[
            "API RP 11BR",
            "Manufacturer POC guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="POC optimization may lead to underproduction or increased rod wear.",
        counter_arguments=[
            "Settings are adjusted based on real-time data.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Rod pump operation in producing wells",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11BR Section 4.1"
    ),
    DoctrineBlock(
        topic="Gas Lift Design: Valve Spacing and Injection Rate",
        keywords=["Gas Lift", "Valve Spacing", "Injection Rate", "Design", "Artificial Lift"],
        conclusion_template="Gas lift valve spacing and injection rate for well {well_id} are optimized for maximum production efficiency.",
        reasoning_framework=(
            "Gas lift design doctrine mandates calculation of optimal valve spacing and injection rate based on well depth, production "
            "rate, and reservoir pressure. The doctrine requires use of gas lift design software, reference to API RP 11V7, and "
            "manufacturer recommendations. Valve spacing is determined by pressure profile and production gradient, ensuring efficient "
            "gas injection and lift. Injection rate is calculated to maximize production without inducing instability or excessive gas "
            "breakthrough. Field validation includes monitoring of production response, gas utilization, and valve performance. "
            "Documentation of all design parameters and operational outcomes is required."
        ),
        key_factors=[
            "Well depth",
            "Production rate",
            "Reservoir pressure",
            "Valve spacing",
            "Injection rate",
            "Pressure profile"
        ],
        primary_authority=[
            "API RP 11V7",
            "Manufacturer gas lift guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Valve spacing and injection rate may not optimize production in variable reservoir conditions.",
        counter_arguments=[
            "Design incorporates reservoir-specific adjustments.",
            "Field validation allows for iterative improvement.",
            "Manufacturer recommendations ensure reliability."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Gas lift operation in producing wells",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11V7 Section 2.1"
    ),
    DoctrineBlock(
        topic="Gas Lift Optimization: Continuous vs. Intermittent",
        keywords=["Gas Lift", "Optimization", "Continuous", "Intermittent", "Artificial Lift"],
        conclusion_template="The gas lift method for well {well_id} is {method}, based on reservoir and production parameters.",
        reasoning_framework=(
            "Optimization of gas lift method (continuous vs. intermittent) is based on reservoir inflow, production rate, and fluid "
            "properties. The doctrine requires analysis of well response to gas injection, evaluation of production stability, and "
            "assessment of gas utilization efficiency. Continuous gas lift is preferred for high-rate wells with stable inflow, while "
            "intermittent gas lift is used for low-rate wells or those with variable inflow. The doctrine mandates field validation, "
            "monitoring of production response, and adjustment of injection parameters. Manufacturer recommendations and API RP 11V7 are "
            "followed. Documentation of all optimization decisions and outcomes is required."
        ),
        key_factors=[
            "Reservoir inflow",
            "Production rate",
            "Fluid properties",
            "Gas utilization efficiency",
            "Production stability"
        ],
        primary_authority=[
            "API RP 11V7",
            "Manufacturer gas lift guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Continuous gas lift may waste gas; intermittent may induce production instability.",
        counter_arguments=[
            "Method selection is based on reservoir-specific analysis.",
            "Field validation ensures optimal gas utilization.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Gas lift operation in producing wells",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11V7 Section 3.1"
    ),
    DoctrineBlock(
        topic="Gas Lift Mandrel and Valve Performance (IPR)",
        keywords=["Gas Lift", "Mandrel", "Valve", "Performance", "IPR", "Artificial Lift"],
        conclusion_template="Gas lift mandrel and valve performance for well {well_id} is optimized based on IPR and production requirements.",
        reasoning_framework=(
            "Gas lift mandrel and valve performance is evaluated based on inflow performance relationship (IPR), production rate, and "
            "reservoir pressure. The doctrine requires analysis of mandrel placement, valve opening pressure, and compatibility with gas "
            "injection parameters. Manufacturer performance curves and API RP 11V7 are referenced. Field validation includes monitoring "
            "for valve malfunction, gas breakthrough, and production response. Design adjustments are made for variable reservoir "
            "conditions. Documentation of all performance evaluations and outcomes is required."
        ),
        key_factors=[
            "IPR analysis",
            "Mandrel placement",
            "Valve opening pressure",
            "Gas injection parameters",
            "Production response"
        ],
        primary_authority=[
            "API RP 11V7",
            "Manufacturer gas lift guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Mandrel and valve performance may degrade under variable reservoir conditions.",
        counter_arguments=[
            "Design incorporates reservoir-specific adjustments.",
            "Field validation ensures optimal performance.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Gas lift operation in producing wells",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11V7 Section 4.1"
    ),
    DoctrineBlock(
        topic="Plunger Lift Candidate Selection (Gas-Liquid Ratio)",
        keywords=["Plunger Lift", "Candidate Selection", "Gas-Liquid Ratio", "Artificial Lift"],
        conclusion_template="Well {well_id} is a candidate for plunger lift based on gas-liquid ratio and production parameters.",
        reasoning_framework=(
            "Selection of plunger lift candidates is based on gas-liquid ratio (GLR), production rate, and well geometry. The doctrine "
            "requires analysis of well inflow, GLR, and compatibility with plunger lift system. Manufacturer recommendations and API RP "
            "11PL are referenced. Field validation includes monitoring of production response, plunger arrival velocity, and system "
            "performance. Candidate selection is refined through iterative review and adjustment. Documentation of all selection criteria "
            "and outcomes is required."
        ),
        key_factors=[
            "Gas-liquid ratio (GLR)",
            "Production rate",
            "Well geometry",
            "Plunger lift system compatibility",
            "Production response"
        ],
        primary_authority=[
            "API RP 11PL",
            "Manufacturer plunger lift guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Plunger lift may not be effective in low-GLR wells.",
        counter_arguments=[
            "Candidate selection is based on GLR analysis.",
            "Field validation ensures effectiveness.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Plunger lift operation in producing wells",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11PL Section 2.1"
    ),
    DoctrineBlock(
        topic="Plunger Lift Cycle Optimization (Arrival Velocity)",
        keywords=["Plunger Lift", "Cycle Optimization", "Arrival Velocity", "Artificial Lift"],
        conclusion_template="Plunger lift cycle for well {well_id} is optimized with arrival velocity of {velocity} ft/s.",
        reasoning_framework=(
            "Optimization of plunger lift cycle is based on arrival velocity, production rate, and well geometry. The doctrine requires "
            "analysis of plunger arrival velocity, cycle timing, and production response. Manufacturer recommendations and API RP 11PL "
            "are referenced. Field validation includes monitoring of plunger arrival, production rate, and system performance. Cycle "
            "optimization is refined through iterative adjustment and review. Documentation of all optimization parameters and outcomes "
            "is required."
        ),
        key_factors=[
            "Plunger arrival velocity",
            "Cycle timing",
            "Production rate",
            "Well geometry",
            "System performance"
        ],
        primary_authority=[
            "API RP 11PL",
            "Manufacturer plunger lift guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Cycle optimization may induce excessive wear or production instability.",
        counter_arguments=[
            "Optimization is based on field data and manufacturer guidelines.",
            "Iterative adjustment allows for refinement.",
            "Field validation ensures effectiveness."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Plunger lift operation in producing wells",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11PL Section 3.1"
    ),
    DoctrineBlock(
        topic="Jet Pump Design (Nozzle/Throat Area Ratio)",
        keywords=["Jet Pump", "Design", "Nozzle", "Throat Area Ratio", "Artificial Lift"],
        conclusion_template="Jet pump design for well {well_id} is optimized with nozzle/throat area ratio of {ratio}.",
        reasoning_framework=(
            "Jet pump design doctrine mandates calculation of optimal nozzle/throat area ratio based on production rate, reservoir "
            "pressure, and fluid properties. The doctrine requires analysis of jet pump performance curves, reference to manufacturer "
            "guidelines, and API RP 11JP. Design is adjusted for well-specific conditions, including fluid viscosity and solids content. "
            "Field validation includes monitoring of jet pump performance, production rate, and system reliability. Documentation of all "
            "design parameters and outcomes is required."
        ),
        key_factors=[
            "Nozzle/throat area ratio",
            "Production rate",
            "Reservoir pressure",
            "Fluid properties",
            "Jet pump performance curves"
        ],
        primary_authority=[
            "API RP 11JP",
            "Manufacturer jet pump guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Jet pump design may not optimize production in variable reservoir conditions.",
        counter_arguments=[
            "Design incorporates reservoir-specific adjustments.",
            "Field validation ensures optimal performance.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Jet pump operation in producing wells",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11JP Section 2.1"
    ),
    DoctrineBlock(
        topic="Artificial Lift Selection Matrix (Flowrate/Depth)",
        keywords=["Artificial Lift", "Selection Matrix", "Flowrate", "Depth", "Optimization"],
        conclusion_template="The artificial lift method for well {well_id} is {lift_method}, based on flowrate and depth selection matrix.",
        reasoning_framework=(
            "Artificial lift selection matrix doctrine mandates evaluation of well flowrate and depth to determine optimal lift method. "
            "The doctrine requires reference to SPE selection matrices, API RP 11AL, and manufacturer recommendations. Selection is "
            "guided by production rate, reservoir pressure, well geometry, and fluid properties. Field validation includes monitoring of "
            "production response and system reliability. Selection matrix is updated periodically based on field data and technology "
            "advancements. Documentation of all selection criteria and outcomes is required."
        ),
        key_factors=[
            "Flowrate",
            "Well depth",
            "Reservoir pressure",
            "Well geometry",
            "Fluid properties"
        ],
        primary_authority=[
            "API RP 11AL",
            "SPE selection matrices",
            "Manufacturer lift guides"
        ],
        burden_holder="Production Engineer",
        adversary_position="Selection matrix may not account for all field-specific variables.",
        counter_arguments=[
            "Matrix is updated with field data and technology advancements.",
            "Field validation ensures optimal selection.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Periodic review and update of selection matrix; field validation and peer review.",
        entity_scope="Artificial lift selection in producing wells",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11AL Section 2.1"
    ),
    DoctrineBlock(
        topic="Artificial Lift Economics (Operating Cost/CAPEX)",
        keywords=["Artificial Lift", "Economics", "Operating Cost", "CAPEX", "Optimization"],
        conclusion_template="The economic analysis for artificial lift in well {well_id} indicates {lift_method} is optimal based on operating cost and CAPEX.",
        reasoning_framework=(
            "Artificial lift economics doctrine mandates comprehensive analysis of operating cost and capital expenditure (CAPEX) for "
            "each lift method. The doctrine requires calculation of installation cost, maintenance cost, energy consumption, and expected "
            "run life. Reference is made to SPE economic models, API RP 11AL, and manufacturer cost guides. Economic analysis is "
            "performed using discounted cash flow (DCF) and net present value (NPV) methods. Field validation includes monitoring of "
            "actual costs and production outcomes. Economic models are updated periodically based on field data and technology "
            "advancements. Documentation of all economic analyses and outcomes is required."
        ),
        key_factors=[
            "Installation cost",
            "Maintenance cost",
            "Energy consumption",
            "Expected run life",
            "Discounted cash flow (DCF)",
            "Net present value (NPV)"
        ],
        primary_authority=[
            "API RP 11AL",
            "SPE economic models",
            "Manufacturer cost guides"
        ],
        burden_holder="Production Engineer",
        adversary_position="Economic analysis may not reflect actual field costs or production outcomes.",
        counter_arguments=[
            "Models are updated with field data and technology advancements.",
            "Field validation ensures accuracy.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Periodic review and update of economic models; field validation and peer review.",
        entity_scope="Artificial lift economics in producing wells",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11AL Section 3.1"
    ),
    DoctrineBlock(
        topic="Artificial Lift Run Life and MTBF Comparison",
        keywords=["Artificial Lift", "Run Life", "MTBF", "Comparison", "Reliability"],
        conclusion_template="The run life and MTBF comparison for well {well_id} indicates {lift_method} is optimal for reliability.",
        reasoning_framework=(
            "Artificial lift run life and mean time between failures (MTBF) doctrine mandates comparison of reliability metrics for each "
            "lift method. The doctrine requires reference to field data, manufacturer reliability guides, and API RP 11AL. Run life and "
            "MTBF are calculated based on installation date, failure history, and maintenance records. Comparison is performed using "
            "statistical analysis of field data. Field validation includes monitoring of actual run life and failure rates. Reliability "
            "models are updated periodically based on field data and technology advancements. Documentation of all reliability analyses "
            "and outcomes is required."
        ),
        key_factors=[
            "Run life",
            "Mean time between failures (MTBF)",
            "Failure history",
            "Maintenance records",
            "Statistical analysis"
        ],
        primary_authority=[
            "API RP 11AL",
            "Manufacturer reliability guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Reliability comparison may not account for all field-specific variables.",
        counter_arguments=[
            "Models are updated with field data and technology advancements.",
            "Field validation ensures accuracy.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Periodic review and update of reliability models; field validation and peer review.",
        entity_scope="Artificial lift reliability in producing wells",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11AL Section 4.1"
    ),
    DoctrineBlock(
        topic="Artificial Lift Automation and Remote Monitoring",
        keywords=["Artificial Lift", "Automation", "Remote Monitoring", "SCADA", "Optimization"],
        conclusion_template="Artificial lift automation and remote monitoring for well {well_id} is implemented with SCADA system for real-time optimization.",
        reasoning_framework=(
            "Artificial lift automation and remote monitoring doctrine mandates implementation of SCADA systems for real-time data "
            "collection, analysis, and optimization. The doctrine requires integration of lift system sensors, remote control "
            "capabilities, and automated adjustment protocols. Reference is made to manufacturer automation guides, API RP 11AL, and SPE "
            "automation papers. Automation is validated through field testing, monitoring of production response, and system reliability. "
            "Documentation of all automation protocols and outcomes is required."
        ),
        key_factors=[
            "SCADA system integration",
            "Sensor data collection",
            "Remote control capabilities",
            "Automated adjustment protocols",
            "Field validation"
        ],
        primary_authority=[
            "API RP 11AL",
            "Manufacturer automation guides",
            "SPE automation papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Automation may induce system instability or fail under field conditions.",
        counter_arguments=[
            "Protocols are validated through field testing.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="Artificial lift automation in producing wells",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11AL Section 5.1"
    ),
    DoctrineBlock(
        topic="Permian Basin Lift Selection: ESP vs. Rod Pump",
        keywords=["Permian Basin", "Lift Selection", "ESP", "Rod Pump", "Artificial Lift"],
        conclusion_template="For Permian Basin well {well_id}, {lift_method} is recommended based on reservoir and production parameters.",
        reasoning_framework=(
            "Permian Basin lift selection doctrine mandates evaluation of reservoir properties, production rate, and well geometry to "
            "determine optimal artificial lift method (ESP vs. Rod Pump). The doctrine requires reference to Permian Basin field data, "
            "SPE selection matrices, and manufacturer recommendations. Selection is guided by production rate, reservoir pressure, "
            "fluid properties, and well depth. Field validation includes monitoring of production response and system reliability. "
            "Selection matrix is updated periodically based on field data and technology advancements. Documentation of all selection "
            "criteria and outcomes is required."
        ),
        key_factors=[
            "Reservoir properties",
            "Production rate",
            "Well geometry",
            "Fluid properties",
            "Well depth"
        ],
        primary_authority=[
            "SPE Permian Basin selection matrices",
            "Manufacturer lift guides",
            "API RP 11AL"
        ],
        burden_holder="Production Engineer",
        adversary_position="Selection may not account for all Permian Basin field-specific variables.",
        counter_arguments=[
            "Matrix is updated with field data and technology advancements.",
            "Field validation ensures optimal selection.",
            "Manufacturer recommendations provide guidance."
        ],
        resolution_strategy="Periodic review and update of selection matrix; field validation and peer review.",
        entity_scope="Artificial lift selection in Permian Basin wells",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Permian Basin selection matrices Section 2.1"
    ),
    DoctrineBlock(
        topic="ESP Downhole Sensor Integration",
        keywords=["ESP", "Downhole Sensor", "Integration", "Monitoring", "Automation"],
        conclusion_template="ESP downhole sensor integration for well {well_id} is implemented for real-time monitoring and optimization.",
        reasoning_framework=(
            "ESP downhole sensor integration doctrine mandates installation of temperature, pressure, and vibration sensors for real-time "
            "monitoring and optimization. The doctrine requires reference to manufacturer sensor integration guides, API RP 11S2, and SPE "
            "automation papers. Sensor data is used for predictive maintenance, performance optimization, and failure prevention. Field "
            "validation includes monitoring of sensor reliability, data accuracy, and system response. Documentation of all sensor "
            "integration protocols and outcomes is required."
        ),
        key_factors=[
            "Sensor installation",
            "Data accuracy",
            "Predictive maintenance",
            "Performance optimization",
            "Failure prevention"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer sensor integration guides",
            "SPE automation papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Sensor integration may fail under extreme downhole conditions.",
        counter_arguments=[
            "Sensors are selected for high reliability and field validation.",
            "Manufacturer recommendations ensure compatibility.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 7.1"
    ),
    DoctrineBlock(
        topic="ESP Cable Routing and Protection",
        keywords=["ESP", "Cable Routing", "Protection", "Design", "Artificial Lift"],
        conclusion_template="ESP cable routing and protection for well {well_id} is designed to minimize mechanical and environmental risk.",
        reasoning_framework=(
            "ESP cable routing and protection doctrine mandates careful planning of cable path, use of protective materials, and adherence "
            "to manufacturer guidelines. The doctrine requires reference to API RP 11S5, field data, and manufacturer cable guides. Cable "
            "routing is designed to minimize mechanical stress, avoid sharp bends, and protect against abrasion and corrosion. Field "
            "validation includes monitoring of cable integrity, ampacity, and voltage drop. Documentation of all cable routing and "
            "protection protocols and outcomes is required."
        ),
        key_factors=[
            "Cable path planning",
            "Protective materials",
            "Mechanical stress minimization",
            "Abrasion and corrosion protection",
            "Ampacity and voltage drop"
        ],
        primary_authority=[
            "API RP 11S5",
            "Manufacturer cable guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Cable routing may fail under mechanical or environmental stress.",
        counter_arguments=[
            "Design incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S5 Section 3.1"
    ),
    DoctrineBlock(
        topic="ESP Sand Handling and Abrasion Mitigation",
        keywords=["ESP", "Sand Handling", "Abrasion Mitigation", "Design", "Artificial Lift"],
        conclusion_template="ESP sand handling and abrasion mitigation for well {well_id} is implemented to maximize run life.",
        reasoning_framework=(
            "ESP sand handling and abrasion mitigation doctrine mandates selection of abrasion-resistant materials, use of sand handling "
            "devices, and adherence to manufacturer guidelines. The doctrine requires reference to API RP 11S2, field data, and "
            "manufacturer sand handling guides. Design is adjusted for wells with high sand production, including use of special coatings, "
            "sand separators, and modified intake configurations. Field validation includes monitoring of ESP wear, production rate, and "
            "system reliability. Documentation of all sand handling and abrasion mitigation protocols and outcomes is required."
        ),
        key_factors=[
            "Abrasion-resistant materials",
            "Sand handling devices",
            "Special coatings",
            "Sand separator use",
            "Modified intake configuration"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer sand handling guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Sand handling may not prevent ESP failure in high-sand wells.",
        counter_arguments=[
            "Design incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 8.1"
    ),
    DoctrineBlock(
        topic="ESP High Temperature Operation",
        keywords=["ESP", "High Temperature", "Operation", "Design", "Artificial Lift"],
        conclusion_template="ESP high temperature operation for well {well_id} is implemented with temperature-rated components.",
        reasoning_framework=(
            "ESP high temperature operation doctrine mandates selection of temperature-rated components, use of cooling protocols, and "
            "adherence to manufacturer guidelines. The doctrine requires reference to API RP 11S2, field data, and manufacturer high "
            "temperature guides. Design is adjusted for wells with high bottomhole temperature, including use of special motor windings, "
            "protectors, and cable insulation. Field validation includes monitoring of ESP performance, temperature data, and system "
            "reliability. Documentation of all high temperature operation protocols and outcomes is required."
        ),
        key_factors=[
            "Temperature-rated components",
            "Cooling protocols",
            "Special motor windings",
            "Protectors and cable insulation",
            "Field validation"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer high temperature guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="High temperature operation may induce ESP failure.",
        counter_arguments=[
            "Design incorporates temperature-rated components.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 9.1"
    ),
    DoctrineBlock(
        topic="ESP Gas Lock Prevention Protocols",
        keywords=["ESP", "Gas Lock", "Prevention", "Protocols", "Artificial Lift"],
        conclusion_template="ESP gas lock prevention protocols for well {well_id} are implemented to maximize production and run life.",
        reasoning_framework=(
            "ESP gas lock prevention protocols doctrine mandates use of gas separators, charge traps, and operational adjustments to "
            "prevent gas lock. The doctrine requires reference to API RP 11S2, field data, and manufacturer gas lock prevention guides. "
            "Protocols include adjustment of pump intake configuration, monitoring of gas-liquid ratio, and real-time response to gas lock "
            "events. Field validation includes monitoring of ESP performance, production rate, and system reliability. Documentation of "
            "all gas lock prevention protocols and outcomes is required."
        ),
        key_factors=[
            "Gas separator use",
            "Charge trap implementation",
            "Pump intake configuration",
            "Gas-liquid ratio monitoring",
            "Real-time response"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer gas lock prevention guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Gas lock prevention protocols may not prevent ESP failure in high-GLR wells.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 10.1"
    ),
    DoctrineBlock(
        topic="ESP Motor Cooling and Overload Protection",
        keywords=["ESP", "Motor Cooling", "Overload Protection", "Design", "Artificial Lift"],
        conclusion_template="ESP motor cooling and overload protection for well {well_id} is implemented to maximize run life.",
        reasoning_framework=(
            "ESP motor cooling and overload protection doctrine mandates use of cooling protocols, overload protection devices, and "
            "adherence to manufacturer guidelines. The doctrine requires reference to API RP 11S2, field data, and manufacturer motor "
            "protection guides. Design is adjusted for wells with high load or temperature, including use of special cooling fluids, "
            "overload relays, and real-time monitoring. Field validation includes monitoring of motor performance, temperature data, and "
            "system reliability. Documentation of all motor cooling and overload protection protocols and outcomes is required."
        ),
        key_factors=[
            "Cooling protocols",
            "Overload protection devices",
            "Special cooling fluids",
            "Overload relays",
            "Real-time monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer motor protection guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Motor cooling and overload protection may not prevent ESP failure under extreme conditions.",
        counter_arguments=[
            "Design incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 11.1"
    ),
    DoctrineBlock(
        topic="ESP Start-Up and Shut-Down Protocols",
        keywords=["ESP", "Start-Up", "Shut-Down", "Protocols", "Artificial Lift"],
        conclusion_template="ESP start-up and shut-down protocols for well {well_id} are implemented to minimize mechanical stress.",
        reasoning_framework=(
            "ESP start-up and shut-down protocols doctrine mandates use of ramp-up and ramp-down procedures, real-time monitoring, and "
            "adherence to manufacturer guidelines. The doctrine requires reference to API RP 11S2, field data, and manufacturer start-up "
            "and shut-down guides. Protocols are designed to minimize mechanical stress, avoid sudden load changes, and maximize ESP run "
            "life. Field validation includes monitoring of ESP performance, production rate, and system reliability. Documentation of all "
            "start-up and shut-down protocols and outcomes is required."
        ),
        key_factors=[
            "Ramp-up and ramp-down procedures",
            "Real-time monitoring",
            "Mechanical stress minimization",
            "Sudden load change avoidance",
            "Field validation"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer start-up and shut-down guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Start-up and shut-down protocols may not prevent ESP failure under extreme conditions.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 12.1"
    ),
    DoctrineBlock(
        topic="ESP Failure Analysis and Root Cause Investigation",
        keywords=["ESP", "Failure Analysis", "Root Cause", "Investigation", "Artificial Lift"],
        conclusion_template="ESP failure analysis and root cause investigation for well {well_id} identifies {failure_mode} and recommends corrective action.",
        reasoning_framework=(
            "ESP failure analysis and root cause investigation doctrine mandates systematic review of failure history, operational data, "
            "and field conditions. The doctrine requires reference to API RP 11S2, manufacturer failure analysis guides, and SPE failure "
            "papers. Investigation includes analysis of run life, failure mode, and contributing factors. Corrective actions are "
            "recommended based on root cause identification. Field validation includes monitoring of corrective action effectiveness and "
            "system reliability. Documentation of all failure analyses and outcomes is required."
        ),
        key_factors=[
            "Failure history review",
            "Operational data analysis",
            "Field conditions assessment",
            "Root cause identification",
            "Corrective action recommendation"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer failure analysis guides",
            "SPE failure papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Failure analysis may not identify all contributing factors.",
        counter_arguments=[
            "Investigation incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 13.1"
    ),
    DoctrineBlock(
        topic="ESP System Integration with Surface Facilities",
        keywords=["ESP", "System Integration", "Surface Facilities", "Design", "Artificial Lift"],
        conclusion_template="ESP system integration with surface facilities for well {well_id} is implemented for optimal production.",
        reasoning_framework=(
            "ESP system integration with surface facilities doctrine mandates coordination of ESP operation with surface equipment, "
            "including separators, tanks, and control systems. The doctrine requires reference to API RP 11S2, manufacturer integration "
            "guides, and SPE surface facility papers. Integration is designed to optimize production, minimize downtime, and ensure "
            "compatibility with surface equipment. Field validation includes monitoring of system performance, production rate, and "
            "reliability. Documentation of all integration protocols and outcomes is required."
        ),
        key_factors=[
            "Surface equipment compatibility",
            "Production optimization",
            "Downtime minimization",
            "System performance monitoring",
            "Field validation"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer integration guides",
            "SPE surface facility papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="System integration may induce production instability or incompatibility.",
        counter_arguments=[
            "Integration incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 14.1"
    ),
    DoctrineBlock(
        topic="ESP Environmental Compliance and Safety Protocols",
        keywords=["ESP", "Environmental Compliance", "Safety Protocols", "Artificial Lift"],
        conclusion_template="ESP environmental compliance and safety protocols for well {well_id} are implemented to meet regulatory requirements.",
        reasoning_framework=(
            "ESP environmental compliance and safety protocols doctrine mandates adherence to regulatory requirements, use of safety "
            "devices, and implementation of environmental protection measures. The doctrine requires reference to API RP 11S2, "
            "manufacturer safety guides, and SPE environmental papers. Protocols include use of safety shut-off devices, spill prevention "
            "measures, and regular safety audits. Field validation includes monitoring of compliance, safety incidents, and system "
            "reliability. Documentation of all compliance and safety protocols and outcomes is required."
        ),
        key_factors=[
            "Regulatory requirements",
            "Safety device implementation",
            "Environmental protection measures",
            "Safety audits",
            "Compliance monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer safety guides",
            "SPE environmental papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Protocols may not prevent all safety incidents or environmental violations.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards and regulatory requirements.",
        entity_scope="ESP operation in producing wells",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 15.1"
    ),
    DoctrineBlock(
        topic="ESP Power Supply and Voltage Regulation",
        keywords=["ESP", "Power Supply", "Voltage Regulation", "Design", "Artificial Lift"],
        conclusion_template="ESP power supply and voltage regulation for well {well_id} is implemented to ensure stable operation.",
        reasoning_framework=(
            "ESP power supply and voltage regulation doctrine mandates use of stable power sources, voltage regulation devices, and "
            "adherence to manufacturer guidelines. The doctrine requires reference to API RP 11S2, field data, and manufacturer power "
            "guides. Design is adjusted for wells with variable power supply, including use of voltage stabilizers, surge protectors, and "
            "real-time monitoring. Field validation includes monitoring of power supply stability, voltage data, and system reliability. "
            "Documentation of all power supply and voltage regulation protocols and outcomes is required."
        ),
        key_factors=[
            "Stable power sources",
            "Voltage regulation devices",
            "Voltage stabilizers",
            "Surge protectors",
            "Real-time monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer power guides",
            "SPE 53827"
        ],
        burden_holder="Production Engineer",
        adversary_position="Power supply and voltage regulation may not prevent ESP failure under unstable conditions.",
        counter_arguments=[
            "Design incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.80,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 16.1"
    ),
    DoctrineBlock(
        topic="ESP Cable Splicing and Repair Protocols",
        keywords=["ESP", "Cable Splicing", "Repair Protocols", "Artificial Lift"],
        conclusion_template="ESP cable splicing and repair protocols for well {well_id} are implemented to maximize cable integrity.",
        reasoning_framework=(
            "ESP cable splicing and repair protocols doctrine mandates use of manufacturer-approved splicing methods, repair materials, "
            "and adherence to API RP 11S5. The doctrine requires reference to manufacturer cable guides, field data, and SPE repair "
            "papers. Protocols include use of heat-shrink sleeves, waterproof connectors, and real-time monitoring of cable integrity. "
            "Field validation includes monitoring of cable performance, ampacity, and voltage drop. Documentation of all splicing and "
            "repair protocols and outcomes is required."
        ),
        key_factors=[
            "Manufacturer-approved splicing methods",
            "Repair materials",
            "Heat-shrink sleeves",
            "Waterproof connectors",
            "Cable integrity monitoring"
        ],
        primary_authority=[
            "API RP 11S5",
            "Manufacturer cable guides",
            "SPE repair papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Cable splicing and repair may not restore full cable integrity.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.79,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S5 Section 4.1"
    ),
    DoctrineBlock(
        topic="ESP System Redundancy and Backup Protocols",
        keywords=["ESP", "System Redundancy", "Backup Protocols", "Artificial Lift"],
        conclusion_template="ESP system redundancy and backup protocols for well {well_id} are implemented to minimize downtime.",
        reasoning_framework=(
            "ESP system redundancy and backup protocols doctrine mandates installation of backup pumps, power sources, and control "
            "systems to minimize downtime. The doctrine requires reference to API RP 11S2, manufacturer redundancy guides, and SPE "
            "reliability papers. Protocols include use of dual pump systems, backup generators, and automated switchover devices. Field "
            "validation includes monitoring of system performance, downtime, and reliability. Documentation of all redundancy and backup "
            "protocols and outcomes is required."
        ),
        key_factors=[
            "Backup pumps",
            "Backup power sources",
            "Automated switchover devices",
            "Dual pump systems",
            "Downtime monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer redundancy guides",
            "SPE reliability papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Redundancy and backup protocols may not prevent all downtime events.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.78,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 17.1"
    ),
    DoctrineBlock(
        topic="ESP Wellbore Cleanout Protocols",
        keywords=["ESP", "Wellbore Cleanout", "Protocols", "Artificial Lift"],
        conclusion_template="ESP wellbore cleanout protocols for well {well_id} are implemented to maximize production and run life.",
        reasoning_framework=(
            "ESP wellbore cleanout protocols doctrine mandates use of chemical and mechanical cleanout methods to remove debris and "
            "scale. The doctrine requires reference to API RP 11S2, manufacturer cleanout guides, and SPE cleanout papers. Protocols "
            "include use of acid treatments, wireline brushes, and real-time monitoring of wellbore cleanliness. Field validation "
            "includes monitoring of ESP performance, production rate, and system reliability. Documentation of all cleanout protocols "
            "and outcomes is required."
        ),
        key_factors=[
            "Chemical cleanout methods",
            "Mechanical cleanout methods",
            "Acid treatments",
            "Wireline brushes",
            "Wellbore cleanliness monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer cleanout guides",
            "SPE cleanout papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Cleanout protocols may not remove all debris or scale.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.77,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 18.1"
    ),
    DoctrineBlock(
        topic="ESP System Performance Benchmarking",
        keywords=["ESP", "System Performance", "Benchmarking", "Artificial Lift"],
        conclusion_template="ESP system performance benchmarking for well {well_id} is implemented to optimize production and reliability.",
        reasoning_framework=(
            "ESP system performance benchmarking doctrine mandates comparison of ESP performance metrics against industry standards and "
            "field data. The doctrine requires reference to API RP 11S2, manufacturer benchmarking guides, and SPE benchmarking papers. "
            "Benchmarking includes analysis of production rate, run life, failure rate, and efficiency. Field validation includes "
            "monitoring of ESP performance, production response, and reliability. Documentation of all benchmarking protocols and "
            "outcomes is required."
        ),
        key_factors=[
            "Industry standards comparison",
            "Production rate analysis",
            "Run life benchmarking",
            "Failure rate benchmarking",
            "Efficiency analysis"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer benchmarking guides",
            "SPE benchmarking papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Benchmarking may not reflect all field-specific variables.",
        counter_arguments=[
            "Benchmarking incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.76,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 19.1"
    ),
    DoctrineBlock(
        topic="ESP System Data Analytics and Predictive Maintenance",
        keywords=["ESP", "Data Analytics", "Predictive Maintenance", "Artificial Lift"],
        conclusion_template="ESP system data analytics and predictive maintenance for well {well_id} is implemented to maximize run life.",
        reasoning_framework=(
            "ESP system data analytics and predictive maintenance doctrine mandates use of advanced data analytics tools, real-time "
            "monitoring, and predictive maintenance protocols. The doctrine requires reference to API RP 11S2, manufacturer analytics "
            "guides, and SPE predictive maintenance papers. Analytics include analysis of sensor data, failure history, and operational "
            "parameters. Predictive maintenance protocols are implemented based on data trends and failure prediction models. Field "
            "validation includes monitoring of maintenance effectiveness, run life, and reliability. Documentation of all analytics and "
            "maintenance protocols and outcomes is required."
        ),
        key_factors=[
            "Advanced data analytics tools",
            "Real-time monitoring",
            "Predictive maintenance protocols",
            "Sensor data analysis",
            "Failure prediction models"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer analytics guides",
            "SPE predictive maintenance papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Data analytics and predictive maintenance may not prevent all ESP failures.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.75,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 20.1"
    ),
    DoctrineBlock(
        topic="ESP System Lifecycle Management",
        keywords=["ESP", "System Lifecycle", "Management", "Artificial Lift"],
        conclusion_template="ESP system lifecycle management for well {well_id} is implemented to maximize production and reliability.",
        reasoning_framework=(
            "ESP system lifecycle management doctrine mandates comprehensive planning of ESP installation, operation, maintenance, and "
            "decommissioning. The doctrine requires reference to API RP 11S2, manufacturer lifecycle guides, and SPE lifecycle papers. "
            "Lifecycle management includes analysis of installation protocols, maintenance schedules, run life optimization, and "
            "decommissioning procedures. Field validation includes monitoring of lifecycle management effectiveness, production rate, and "
            "reliability. Documentation of all lifecycle management protocols and outcomes is required."
        ),
        key_factors=[
            "Installation protocols",
            "Maintenance schedules",
            "Run life optimization",
            "Decommissioning procedures",
            "Lifecycle management effectiveness"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer lifecycle guides",
            "SPE lifecycle papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Lifecycle management may not optimize production or reliability.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.74,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 21.1"
    ),
    DoctrineBlock(
        topic="ESP System Documentation and Record Keeping",
        keywords=["ESP", "Documentation", "Record Keeping", "Artificial Lift"],
        conclusion_template="ESP system documentation and record keeping for well {well_id} is implemented to ensure compliance and optimization.",
        reasoning_framework=(
            "ESP system documentation and record keeping doctrine mandates comprehensive recording of installation, operation, maintenance, "
            "and failure history. The doctrine requires reference to API RP 11S2, manufacturer documentation guides, and SPE record keeping "
            "papers. Documentation includes installation reports, maintenance logs, failure analysis records, and production data. Field "
            "validation includes review of documentation accuracy, completeness, and compliance. Documentation protocols are updated "
            "periodically based on field data and regulatory requirements."
        ),
        key_factors=[
            "Installation reports",
            "Maintenance logs",
            "Failure analysis records",
            "Production data",
            "Documentation accuracy and completeness"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer documentation guides",
            "SPE record keeping papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Documentation and record keeping may not ensure compliance or optimization.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards and regulatory requirements.",
        entity_scope="ESP operation in producing wells",
        confidence=0.73,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 22.1"
    ),
    DoctrineBlock(
        topic="ESP System Training and Competency Protocols",
        keywords=["ESP", "Training", "Competency", "Protocols", "Artificial Lift"],
        conclusion_template="ESP system training and competency protocols for well {well_id} are implemented to ensure operational excellence.",
        reasoning_framework=(
            "ESP system training and competency protocols doctrine mandates comprehensive training of personnel in ESP installation, "
            "operation, maintenance, and troubleshooting. The doctrine requires reference to API RP 11S2, manufacturer training guides, "
            "and SPE competency papers. Training includes classroom instruction, field training, and competency assessment. Field "
            "validation includes monitoring of training effectiveness, operational excellence, and safety incidents. Training protocols "
            "are updated periodically based on field data and technology advancements."
        ),
        key_factors=[
            "Classroom instruction",
            "Field training",
            "Competency assessment",
            "Training effectiveness monitoring",
            "Operational excellence"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer training guides",
            "SPE competency papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Training and competency protocols may not ensure operational excellence.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.72,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 23.1"
    ),
    DoctrineBlock(
        topic="ESP System Technology Advancement and Innovation",
        keywords=["ESP", "Technology Advancement", "Innovation", "Artificial Lift"],
        conclusion_template="ESP system technology advancement and innovation for well {well_id} is implemented to optimize production and reliability.",
        reasoning_framework=(
            "ESP system technology advancement and innovation doctrine mandates adoption of new technologies, materials, and protocols to "
            "optimize production and reliability. The doctrine requires reference to API RP 11S2, manufacturer innovation guides, and SPE "
            "technology papers. Innovation includes use of advanced materials, automation protocols, and data analytics tools. Field "
            "validation includes monitoring of technology effectiveness, production rate, and reliability. Innovation protocols are "
            "updated periodically based on field data and technology advancements."
        ),
        key_factors=[
            "Advanced materials",
            "Automation protocols",
            "Data analytics tools",
            "Technology effectiveness monitoring",
            "Production optimization"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer innovation guides",
            "SPE technology papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Technology advancement and innovation may not optimize production or reliability.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards.",
        entity_scope="ESP operation in producing wells",
        confidence=0.71,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 24.1"
    ),
    DoctrineBlock(
        topic="ESP System Regulatory Compliance and Audit Protocols",
        keywords=["ESP", "Regulatory Compliance", "Audit Protocols", "Artificial Lift"],
        conclusion_template="ESP system regulatory compliance and audit protocols for well {well_id} are implemented to ensure legal and operational compliance.",
        reasoning_framework=(
            "ESP system regulatory compliance and audit protocols doctrine mandates adherence to regulatory requirements, regular audits, "
            "and documentation of compliance. The doctrine requires reference to API RP 11S2, manufacturer compliance guides, and SPE "
            "regulatory papers. Compliance includes use of safety devices, environmental protection measures, and regular audits. Field "
            "validation includes monitoring of compliance, audit effectiveness, and system reliability. Compliance protocols are updated "
            "periodically based on regulatory changes and field data."
        ),
        key_factors=[
            "Regulatory requirements",
            "Safety device implementation",
            "Environmental protection measures",
            "Audit effectiveness monitoring",
            "Compliance documentation"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer compliance guides",
            "SPE regulatory papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Regulatory compliance and audit protocols may not ensure legal or operational compliance.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards and regulatory requirements.",
        entity_scope="ESP operation in producing wells",
        confidence=0.70,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 25.1"
    ),
    DoctrineBlock(
        topic="ESP System Environmental Impact Assessment",
        keywords=["ESP", "Environmental Impact", "Assessment", "Artificial Lift"],
        conclusion_template="ESP system environmental impact assessment for well {well_id} is implemented to minimize environmental risk.",
        reasoning_framework=(
            "ESP system environmental impact assessment doctrine mandates comprehensive evaluation of environmental risks, use of "
            "mitigation measures, and adherence to regulatory requirements. The doctrine requires reference to API RP 11S2, manufacturer "
            "environmental guides, and SPE environmental papers. Assessment includes analysis of spill risk, emissions, and waste "
            "management. Field validation includes monitoring of environmental incidents, mitigation effectiveness, and compliance. "
            "Assessment protocols are updated periodically based on regulatory changes and field data."
        ),
        key_factors=[
            "Environmental risk evaluation",
            "Mitigation measures",
            "Regulatory requirements",
            "Spill risk analysis",
            "Emissions and waste management"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer environmental guides",
            "SPE environmental papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Environmental impact assessment may not minimize all environmental risks.",
        counter_arguments=[
            "Assessment incorporates field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards and regulatory requirements.",
        entity_scope="ESP operation in producing wells",
        confidence=0.69,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 26.1"
    ),
    DoctrineBlock(
        topic="ESP System Emergency Response Protocols",
        keywords=["ESP", "Emergency Response", "Protocols", "Artificial Lift"],
        conclusion_template="ESP system emergency response protocols for well {well_id} are implemented to minimize risk and downtime.",
        reasoning_framework=(
            "ESP system emergency response protocols doctrine mandates development of emergency response plans, use of safety devices, "
            "and regular training. The doctrine requires reference to API RP 11S2, manufacturer emergency response guides, and SPE "
            "emergency papers. Protocols include use of safety shut-off devices, spill prevention measures, and regular emergency drills. "
            "Field validation includes monitoring of emergency response effectiveness, safety incidents, and downtime. Emergency response "
            "protocols are updated periodically based on field data and regulatory requirements."
        ),
        key_factors=[
            "Emergency response plan development",
            "Safety device implementation",
            "Spill prevention measures",
            "Emergency drill effectiveness",
            "Downtime monitoring"
        ],
        primary_authority=[
            "API RP 11S2",
            "Manufacturer emergency response guides",
            "SPE emergency papers"
        ],
        burden_holder="Production Engineer",
        adversary_position="Emergency response protocols may not minimize all risks or downtime.",
        counter_arguments=[
            "Protocols incorporate field-specific adjustments.",
            "Manufacturer recommendations ensure reliability.",
            "Field validation allows for iterative improvement."
        ],
        resolution_strategy="Field validation, peer review, and adherence to API standards and regulatory requirements.",
        entity_scope="ESP operation in producing wells",
        confidence=0.68,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 11S2 Section 27.1"
    ),
    DoctrineBlock(
        topic="ESP System Health, Safety, and Environment (HSE) Management",
        keywords=["ESP", "HSE", "Health", "Safety", "Environment", "Management", "Artificial Lift"],
        conclusion_template="ESP system HSE management for well {well_id} is implemented to ensure health, safety, and environmental compliance.",
        reasoning_framework=(
            "ESP system health, safety, and environment (HSE) management doctrine mandates comprehensive planning and implementation of "
            "HSE protocols. The doctrine requires