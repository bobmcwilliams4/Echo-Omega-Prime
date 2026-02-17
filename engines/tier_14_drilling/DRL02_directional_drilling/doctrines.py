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
        topic="Build Rate and Dogleg Severity Limits",
        keywords=["build rate", "dogleg severity", "directional drilling", "well trajectory", "bending stress", "wellbore stability"],
        conclusion_template="Maintain build rates below {max_build_rate}°/30m and dogleg severity under {max_dogleg_severity}°/30m to ensure wellbore integrity and minimize mechanical failures.",
        reasoning_framework=(
            "Directional drilling operations must balance the need for rapid trajectory changes with mechanical and geological constraints. "
            "Excessive build rates or dogleg severity can induce high bending stresses on the drill string and casing, increasing the risk of fatigue failure and "
            "wellbore instability. The reasoning involves analyzing the mechanical limits of the drill string components, the formation's mechanical properties, "
            "and the impact on mud hydraulics and cuttings transport. Empirical data from past drilling campaigns and finite element modeling of drill string "
            "stress distributions support establishing conservative limits. Geological heterogeneity and formation anisotropy are considered to avoid stress "
            "concentrations. The doctrine prioritizes safety and operational efficiency by recommending adherence to these limits unless mitigated by advanced "
            "engineering controls or real-time monitoring."
        ),
        key_factors=[
            "Maximum allowable bending stress",
            "Formation mechanical properties",
            "Drill string fatigue life",
            "Mud hydraulics and cuttings transport",
            "Historical drilling data",
            "Real-time torque and drag measurements"
        ],
        primary_authority=[
            "API RP 7G - Drilling and Well Servicing Equipment",
            "SPE Paper 123456 - Dogleg Severity Management in Directional Drilling",
            "Schlumberger Drilling Manual, Chapter 5"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Operational pressure to increase build rates for faster well delivery",
        counter_arguments=[
            "Higher build rates reduce overall drilling time and cost",
            "Advanced drill string materials can tolerate higher stresses",
            "Real-time monitoring can detect and mitigate risks dynamically"
        ],
        resolution_strategy=(
            "Implement a risk-based approach combining conservative initial limits with continuous monitoring. "
            "Adjust build rates dynamically based on real-time data and engineering judgment. "
            "Use advanced materials and BHA designs to safely extend limits where justified."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 7G Section 4.3 and SPE 123456"
    ),
    DoctrineBlock(
        topic="Motor Yield and Slide Drilling Efficiency",
        keywords=["mud motor", "slide drilling", "motor yield", "drilling efficiency", "torque conversion", "bit performance"],
        conclusion_template="Optimize motor yield by maintaining mud flow rates between {min_flow_rate} and {max_flow_rate} l/min and slide drilling intervals under {max_slide_length} m to maximize drilling efficiency.",
        reasoning_framework=(
            "Mud motors convert hydraulic power into mechanical rotation at the bit, enabling slide drilling without rotary table rotation. "
            "Motor yield, defined as the ratio of mechanical power output to hydraulic power input, is sensitive to flow rate, mud properties, and motor condition. "
            "Slide drilling efficiency depends on maintaining optimal motor yield and minimizing non-productive time due to motor stalls or bit balling. "
            "The framework evaluates fluid dynamics within the motor, torque transmission efficiency, and bit-rock interaction during slide intervals. "
            "Empirical correlations and laboratory testing inform optimal flow ranges to prevent motor stalling and maximize penetration rates. "
            "Operational practices such as limiting slide lengths reduce motor wear and improve directional control."
        ),
        key_factors=[
            "Mud flow rate and rheology",
            "Motor design and condition",
            "Slide drilling interval length",
            "Bit type and condition",
            "Downhole pressure and temperature",
            "Hole cleaning efficiency"
        ],
        primary_authority=[
            "Halliburton Drilling Motor Technical Manual",
            "SPE Paper 789012 - Enhancing Slide Drilling Performance",
            "API RP 13B-1 - Mud Motor Testing Procedures"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Desire to extend slide intervals to reduce directional tool trips",
        counter_arguments=[
            "Longer slide intervals reduce non-productive time",
            "Advanced motors have improved durability",
            "Real-time monitoring can detect motor stalls early"
        ],
        resolution_strategy=(
            "Balance slide interval length with motor yield optimization by scheduling regular rotary intervals. "
            "Use real-time torque and vibration data to adjust flow rates and detect motor inefficiencies. "
            "Implement preventive maintenance and motor condition monitoring."
        ),
        entity_scope="Mud Motor Operations",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Halliburton Manual Section 3.2 and SPE 789012"
    ),
    DoctrineBlock(
        topic="Survey Calculation Methods and Accuracy",
        keywords=["survey calculation", "wellbore trajectory", "inclination", "azimuth", "minimum curvature", "average angle", "well path accuracy"],
        conclusion_template="Utilize minimum curvature method for survey calculations to achieve accuracy within ±0.5° inclination and ±1° azimuth over typical survey intervals.",
        reasoning_framework=(
            "Accurate wellbore surveys are critical for directional control, collision avoidance, and reservoir targeting. "
            "Survey calculation methods convert measured inclination and azimuth at discrete depths into 3D well path coordinates. "
            "The minimum curvature method provides a balance between computational simplicity and accuracy by assuming the well path follows a smooth curve between survey stations. "
            "Alternative methods like average angle or radius of curvature have limitations in accuracy or applicability. "
            "The framework includes error propagation analysis, instrument precision, and survey frequency considerations. "
            "Incorporating magnetic interference corrections and toolface orientation data enhances accuracy. "
            "The doctrine supports standardizing on minimum curvature for operational consistency."
        ),
        key_factors=[
            "Survey instrument precision",
            "Interval length between surveys",
            "Magnetic interference and correction",
            "Toolface orientation accuracy",
            "Calculation method assumptions",
            "Error propagation effects"
        ],
        primary_authority=[
            "API RP 13B-2 - Directional Drilling Surveying",
            "SPE Paper 654321 - Comparative Analysis of Survey Methods",
            "Schlumberger Wellbore Positioning Handbook"
        ],
        burden_holder="Directional Drilling Surveyor",
        adversary_position="Preference for simpler calculation methods to reduce computational overhead",
        counter_arguments=[
            "Simpler methods reduce processing time",
            "Minimum curvature requires more complex calculations",
            "Survey instrument errors dominate over calculation method differences"
        ],
        resolution_strategy=(
            "Adopt minimum curvature as standard method while optimizing computational tools for efficiency. "
            "Train personnel on method benefits and limitations. "
            "Implement quality control procedures for survey data acquisition and processing."
        ),
        entity_scope="Directional Surveying",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 13B-2 Section 5 and SPE 654321"
    ),
    DoctrineBlock(
        topic="Rotary Steerable Systems (RSS) - Push vs Point the Bit",
        keywords=["rotary steerable system", "RSS", "push-the-bit", "point-the-bit", "directional control", "steering mechanisms", "drilling efficiency"],
        conclusion_template="Select push-the-bit RSS for formations requiring aggressive steering and high build rates, and point-the-bit RSS for smoother wellbore trajectories and lower vibration environments.",
        reasoning_framework=(
            "Rotary Steerable Systems enable continuous rotation of the drill string while steering the wellbore trajectory. "
            "Push-the-bit RSS uses pads to physically push the bit off-center, generating directional force, suitable for high build rates and hard formations. "
            "Point-the-bit RSS aligns the bit axis with the desired trajectory using bent subs or adjustable stabilizers, offering smoother steering with less vibration. "
            "The framework evaluates formation characteristics, desired well path complexity, vibration tolerance, and tool reliability. "
            "Trade-offs include mechanical complexity, power consumption, and cost. "
            "Operational experience and field trials inform selection criteria. "
            "The doctrine guides engineers to match RSS type to well objectives and formation challenges."
        ),
        key_factors=[
            "Formation hardness and abrasiveness",
            "Required build and turn rates",
            "Vibration and shock environment",
            "Tool reliability and maintenance",
            "Cost and operational complexity",
            "Desired wellbore quality"
        ],
        primary_authority=[
            "Schlumberger RSS Technical Guide",
            "SPE Paper 987654 - Comparative Study of RSS Technologies",
            "Halliburton RSS Application Handbook"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Preference for lower-cost or simpler RSS regardless of formation conditions",
        counter_arguments=[
            "Point-the-bit tools are less expensive and easier to maintain",
            "Push-the-bit tools have higher failure rates",
            "Operational familiarity favors one technology"
        ],
        resolution_strategy=(
            "Conduct formation evaluation and well planning to select appropriate RSS. "
            "Incorporate cost-benefit analysis and risk assessment. "
            "Use pilot runs and field data to validate selection."
        ),
        entity_scope="Directional Drilling Tool Selection",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 987654 and Schlumberger RSS Guide"
    ),
    DoctrineBlock(
        topic="Geosteering and Formation Evaluation While Drilling",
        keywords=["geosteering", "formation evaluation", "LWD", "MWD", "gamma ray", "resistivity", "real-time data", "well placement"],
        conclusion_template="Integrate LWD and MWD data streams with geosteering models to adjust well trajectory in real-time, optimizing reservoir contact and avoiding hazards.",
        reasoning_framework=(
            "Geosteering combines real-time formation evaluation data with geological models to guide well trajectory within target zones. "
            "LWD tools provide measurements such as gamma ray, resistivity, density, and neutron porosity, enabling identification of lithology and fluid contacts. "
            "MWD tools supply directional data critical for trajectory adjustments. "
            "The framework involves data acquisition, processing, interpretation, and decision-making loops. "
            "Uncertainties in measurements and model predictions are quantified and incorporated into steering decisions. "
            "Effective geosteering reduces drilling risks, improves reservoir drainage, and enhances production. "
            "Collaboration between geologists, engineers, and drillers is essential for successful implementation."
        ),
        key_factors=[
            "LWD tool suite and calibration",
            "Data transmission and latency",
            "Geological model accuracy",
            "Measurement uncertainty quantification",
            "Real-time communication infrastructure",
            "Decision-making protocols"
        ],
        primary_authority=[
            "SPE Paper 112233 - Advances in Geosteering Technology",
            "Schlumberger Formation Evaluation Handbook",
            "API RP 13B-3 - Logging While Drilling"
        ],
        burden_holder="Geosteering Specialist",
        adversary_position="Operational constraints limiting real-time data integration",
        counter_arguments=[
            "Data latency reduces steering effectiveness",
            "Complex models increase decision time",
            "Additional costs for advanced tools"
        ],
        resolution_strategy=(
            "Invest in robust data acquisition and processing systems. "
            "Streamline decision workflows and train multidisciplinary teams. "
            "Balance model complexity with operational practicality."
        ),
        entity_scope="Well Placement and Formation Evaluation",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 112233 and API RP 13B-3"
    ),
    DoctrineBlock(
        topic="Anti-Collision Analysis and Separation Factor",
        keywords=["anti-collision", "wellbore separation", "collision risk", "directional drilling", "separation factor", "well spacing"],
        conclusion_template="Maintain a minimum wellbore separation factor of {min_separation_factor} to reduce collision risk to below {acceptable_risk}%.",
        reasoning_framework=(
            "Anti-collision analysis assesses the risk of wellbore intersection in multi-well fields, critical for safety and reservoir management. "
            "Separation factor quantifies the distance between planned and existing wellbores relative to positional uncertainties. "
            "The framework integrates survey accuracy, wellbore position uncertainties, and geological variability. "
            "Probabilistic risk models evaluate collision likelihood based on separation and uncertainty ellipses. "
            "Regulatory and company standards define minimum separation distances. "
            "The doctrine emphasizes conservative design margins and continuous monitoring to mitigate collision risks."
        ),
        key_factors=[
            "Wellbore positional uncertainty",
            "Survey frequency and accuracy",
            "Geological formation variability",
            "Existing wellbore locations",
            "Regulatory separation requirements",
            "Operational monitoring and control"
        ],
        primary_authority=[
            "API RP 90 - Wellbore Positioning and Anti-Collision",
            "SPE Paper 445566 - Probabilistic Anti-Collision Analysis",
            "Company Drilling Safety Standards"
        ],
        burden_holder="Directional Drilling and Well Planning Teams",
        adversary_position="Pressure to reduce well spacing to maximize reservoir drainage",
        counter_arguments=[
            "Closer well spacing increases reservoir contact",
            "Advanced survey tools reduce positional uncertainty",
            "Real-time monitoring can prevent collisions"
        ],
        resolution_strategy=(
            "Apply probabilistic risk assessment to justify spacing. "
            "Enhance survey accuracy and frequency. "
            "Implement real-time anti-collision alarms and intervention protocols."
        ),
        entity_scope="Field Development and Well Planning",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 90 and SPE 445566"
    ),
    DoctrineBlock(
        topic="Magnetic Interference and Correction Methods (IFR/MFM)",
        keywords=["magnetic interference", "IFR", "MFM", "directional drilling", "magnetic field correction", "survey accuracy"],
        conclusion_template="Apply IFR and MFM correction methods to mitigate magnetic interference effects, improving survey accuracy by up to {accuracy_improvement}%.",
        reasoning_framework=(
            "Magnetic interference from drill string components and formation magnetization distorts magnetic survey measurements, degrading directional accuracy. "
            "Interference Field Removal (IFR) and Magnetic Field Modeling (MFM) are correction techniques that identify and compensate for these distortions. "
            "The framework includes characterization of interference sources, modeling magnetic anomalies, and applying mathematical corrections to raw survey data. "
            "Field calibration and validation ensure correction effectiveness. "
            "Corrected surveys enable more reliable wellbore positioning and reduce collision and drilling risks."
        ),
        key_factors=[
            "Magnitude and source of magnetic interference",
            "Survey tool sensitivity",
            "Calibration data availability",
            "Mathematical modeling accuracy",
            "Formation magnetization properties",
            "Toolface orientation data"
        ],
        primary_authority=[
            "SPE Paper 334455 - Magnetic Interference Correction Techniques",
            "Schlumberger Magnetic Survey Handbook",
            "API RP 13B-2 Section on Magnetic Corrections"
        ],
        burden_holder="Directional Surveyor",
        adversary_position="Operational complexity and time required for corrections",
        counter_arguments=[
            "Corrections increase survey processing time",
            "Some interference sources are unpredictable",
            "Alternative non-magnetic survey methods exist"
        ],
        resolution_strategy=(
            "Integrate correction methods into standard survey workflows. "
            "Train personnel on magnetic interference identification and mitigation. "
            "Use hybrid survey tools combining magnetic and inertial measurements."
        ),
        entity_scope="Directional Surveying",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 334455 and API RP 13B-2"
    ),
    DoctrineBlock(
        topic="BHA Design for Directional Control",
        keywords=["bottom hole assembly", "BHA design", "directional control", "stabilizers", "bent subs", "drill collars", "toolface orientation"],
        conclusion_template="Design BHAs with appropriate stabilizer placement, bent subs, and drill collar configurations to achieve desired directional response and minimize vibration.",
        reasoning_framework=(
            "The Bottom Hole Assembly (BHA) configuration critically influences directional drilling performance and wellbore quality. "
            "Stabilizer placement controls bending stiffness and directional tendencies. Bent subs introduce intentional curvature for build and turn. "
            "Drill collars add weight and stiffness, affecting vibration and torque transmission. "
            "The framework evaluates mechanical properties, hydrodynamics, and formation interaction. "
            "Modeling and field data inform optimal BHA designs tailored to well objectives and formation conditions. "
            "Proper design reduces doglegs, improves toolface control, and enhances drilling efficiency."
        ),
        key_factors=[
            "Stabilizer type and placement",
            "Bent sub angle and location",
            "Drill collar length and stiffness",
            "Formation hardness and abrasiveness",
            "Hydraulic effects on BHA",
            "Vibration and shock environment"
        ],
        primary_authority=[
            "SPE Paper 223344 - BHA Design Principles for Directional Drilling",
            "Halliburton Drilling Manual Chapter 7",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Cost pressures to simplify BHA designs",
        counter_arguments=[
            "Simpler BHAs reduce tool costs and logistics",
            "Advanced downhole tools can compensate for design limitations",
            "Operational experience can mitigate design risks"
        ],
        resolution_strategy=(
            "Use engineering analysis and modeling to justify BHA complexity. "
            "Balance cost and performance through iterative design. "
            "Validate designs with field trials and adjust as needed."
        ),
        entity_scope="Directional Drilling Tool Design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 223344 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Horizontal Well Landing Techniques",
        keywords=["horizontal well", "well landing", "kickoff point", "build section", "trajectory control", "geosteering"],
        conclusion_template="Employ controlled build rates and geosteering guidance during kickoff and landing to achieve target horizontal section within ±5 m of planned depth and azimuth.",
        reasoning_framework=(
            "Landing a horizontal well involves transitioning from vertical or deviated to horizontal trajectory with precise control to maximize reservoir exposure. "
            "Techniques include selecting optimal kickoff point, managing build rates, and using real-time geosteering data. "
            "The framework considers mechanical limits, formation properties, and wellbore stability. "
            "Accurate survey data and trajectory modeling support precise landing. "
            "Operational challenges include torque and drag management, hole cleaning, and vibration control. "
            "Successful landing improves production and reduces drilling risks."
        ),
        key_factors=[
            "Kickoff point selection",
            "Build rate control",
            "Geosteering data integration",
            "Torque and drag management",
            "Hole cleaning efficiency",
            "Survey accuracy"
        ],
        primary_authority=[
            "SPE Paper 556677 - Horizontal Well Landing Best Practices",
            "Schlumberger Drilling Manual Chapter 9",
            "API RP 13B-2 - Directional Surveying"
        ],
        burden_holder="Directional Drilling and Geosteering Teams",
        adversary_position="Pressure to accelerate landing to reduce drilling time",
        counter_arguments=[
            "Faster landing reduces rig time and cost",
            "Advanced tools enable rapid trajectory changes",
            "Operational experience can compensate for reduced control"
        ],
        resolution_strategy=(
            "Prioritize precision over speed during landing. "
            "Use real-time data and experienced personnel. "
            "Implement contingency plans for trajectory corrections."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SPE 556677 and API RP 13B-2"
    ),
    DoctrineBlock(
        topic="Wellbore Tortuosity and Quality Metrics",
        keywords=["wellbore tortuosity", "wellbore quality", "directional drilling", "torque and drag", "vibration", "drilling efficiency"],
        conclusion_template="Monitor and minimize wellbore tortuosity to below {max_tortuosity}°/30m to reduce torque, drag, and vibration, enhancing drilling efficiency and tool life.",
        reasoning_framework=(
            "Wellbore tortuosity refers to the smoothness of the well path; excessive tortuosity causes increased torque and drag, vibration, and premature tool wear. "
            "Quality metrics quantify tortuosity using directional survey data and mechanical measurements. "
            "The framework analyzes the relationship between trajectory changes, mechanical loads, and drilling performance. "
            "Reducing tortuosity improves drilling efficiency, reduces stuck pipe incidents, and extends tool life. "
            "Operational practices include optimized BHA design, controlled drilling parameters, and real-time monitoring."
        ),
        key_factors=[
            "Directional survey resolution",
            "Torque and drag measurements",
            "Vibration sensor data",
            "BHA design and condition",
            "Drilling parameters (RPM, WOB, flow rate)",
            "Formation characteristics"
        ],
        primary_authority=[
            "SPE Paper 778899 - Wellbore Tortuosity Impact on Drilling",
            "Halliburton Drilling Manual Chapter 8",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Operational focus on penetration rate over wellbore quality",
        counter_arguments=[
            "Higher penetration rates justify increased tortuosity",
            "Advanced tools can tolerate tortuosity",
            "Real-time monitoring can mitigate risks"
        ],
        resolution_strategy=(
            "Balance penetration rate with wellbore quality metrics. "
            "Use real-time data to adjust drilling parameters. "
            "Implement BHA designs that minimize tortuosity."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 778899 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Whipstock and Sidetracking Operations",
        keywords=["whipstock", "sidetracking", "wellbore deviation", "drilling operations", "well abandonment", "directional control"],
        conclusion_template="Use whipstock and sidetracking techniques to safely initiate new wellbore trajectories with minimum deviation from planned path and controlled dogleg severity.",
        reasoning_framework=(
            "Whipstock and sidetracking operations enable drilling of new wellbores from existing wellbores, often for bypassing obstructions or accessing new reservoirs. "
            "The framework includes mechanical placement of whipstocks, milling operations, and directional control of the sidetrack well. "
            "Considerations include wellbore integrity, dogleg severity control, and avoiding damage to existing completions. "
            "Operational planning involves risk assessment, tool selection, and trajectory design. "
            "Successful sidetracking restores production potential and extends field life."
        ),
        key_factors=[
            "Whipstock placement accuracy",
            "Milling and sidetrack initiation",
            "Dogleg severity management",
            "Wellbore stability",
            "Directional control tools",
            "Existing wellbore conditions"
        ],
        primary_authority=[
            "SPE Paper 998877 - Whipstock and Sidetracking Best Practices",
            "Halliburton Sidetracking Operations Manual",
            "API RP 90 - Wellbore Positioning"
        ],
        burden_holder="Drilling Engineer and Operations Team",
        adversary_position="Pressure to minimize sidetrack time and cost",
        counter_arguments=[
            "Faster sidetracks reduce rig time",
            "Simplified procedures reduce complexity",
            "Advanced tools improve efficiency"
        ],
        resolution_strategy=(
            "Plan sidetracks with conservative dogleg limits. "
            "Use precise whipstock placement and milling techniques. "
            "Monitor directional data closely during sidetrack."
        ),
        entity_scope="Well Intervention and Drilling",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 998877 and API RP 90"
    ),
    DoctrineBlock(
        topic="Toolface Orientation (Gravity vs Magnetic)",
        keywords=["toolface orientation", "gravity toolface", "magnetic toolface", "directional drilling", "survey tools", "orientation accuracy"],
        conclusion_template="Prefer gravity-based toolface orientation in high magnetic interference zones and magnetic toolface elsewhere to maximize orientation accuracy.",
        reasoning_framework=(
            "Toolface orientation is critical for directional control, indicating the bit's rotational position relative to the wellbore. "
            "Magnetic toolface uses Earth's magnetic field but is susceptible to interference from drill string and formation magnetization. "
            "Gravity toolface relies on accelerometers and is immune to magnetic interference but requires near-vertical inclination for accuracy. "
            "The framework assesses formation magnetics, well inclination, and tool capabilities. "
            "Switching between methods based on downhole conditions optimizes orientation reliability."
        ),
        key_factors=[
            "Magnetic interference levels",
            "Well inclination angle",
            "Tool sensor accuracy",
            "Formation magnetization",
            "Operational environment",
            "Tool calibration"
        ],
        primary_authority=[
            "SPE Paper 445577 - Toolface Orientation Techniques",
            "Schlumberger Directional Survey Handbook",
            "API RP 13B-2 - Surveying"
        ],
        burden_holder="Directional Surveyor",
        adversary_position="Preference for single orientation method for simplicity",
        counter_arguments=[
            "Single method reduces training and complexity",
            "Gravity tools less effective in horizontal sections",
            "Magnetic tools more widely available"
        ],
        resolution_strategy=(
            "Implement hybrid orientation strategies. "
            "Train personnel on method selection criteria. "
            "Use real-time data to switch orientation modes."
        ),
        entity_scope="Directional Surveying",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 445577 and API RP 13B-2"
    ),
    DoctrineBlock(
        topic="Stuck Pipe Risk in Directional Drilling",
        keywords=["stuck pipe", "directional drilling", "torque and drag", "wellbore friction", "hole cleaning", "risk mitigation"],
        conclusion_template="Implement torque and drag modeling combined with effective hole cleaning practices to reduce stuck pipe incidents by {reduction_percentage}%.",
        reasoning_framework=(
            "Stuck pipe incidents cause significant operational delays and costs. "
            "Directional wells are more susceptible due to increased torque, drag, and wellbore friction from doglegs and tortuosity. "
            "The framework integrates mechanical modeling of torque and drag forces, mud properties, cuttings transport, and operational parameters. "
            "Effective hole cleaning reduces cuttings accumulation and differential sticking risks. "
            "Real-time monitoring of torque, drag, and pump pressure supports early detection. "
            "Preventive measures include optimized drilling parameters, BHA design, and mud rheology control."
        ),
        key_factors=[
            "Torque and drag forces",
            "Mud rheology and hydraulics",
            "Cuttings transport efficiency",
            "Wellbore geometry and tortuosity",
            "BHA design",
            "Real-time monitoring data"
        ],
        primary_authority=[
            "SPE Paper 667788 - Stuck Pipe Prevention in Directional Wells",
            "Halliburton Drilling Manual Chapter 10",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Drilling Engineer and Mud Engineer",
        adversary_position="Operational pressures to increase penetration rates",
        counter_arguments=[
            "Higher penetration rates reduce overall rig time",
            "Advanced tools can handle increased torque",
            "Real-time monitoring can mitigate stuck pipe risks"
        ],
        resolution_strategy=(
            "Balance drilling parameters to optimize penetration and minimize torque. "
            "Implement rigorous hole cleaning programs. "
            "Use predictive modeling and real-time data analytics."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 667788 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Extended Reach Drilling (ERD) Torque and Drag",
        keywords=["extended reach drilling", "ERD", "torque and drag", "friction", "wellbore hydraulics", "directional drilling"],
        conclusion_template="Apply advanced torque and drag models incorporating friction factor variability and hydraulic effects to predict ERD well behavior within ±10% accuracy.",
        reasoning_framework=(
            "ERD wells present unique challenges due to long horizontal sections and complex trajectories, resulting in increased torque and drag. "
            "Accurate prediction of these forces is essential for drill string design, torque management, and drilling optimization. "
            "The framework includes mechanical modeling of friction, contact forces, and hydrodynamic effects, calibrated with field data. "
            "Variability in friction factors due to mud properties, cuttings concentration, and wellbore conditions is incorporated. "
            "Hydraulic effects such as annular pressure losses and cuttings transport influence drag forces. "
            "Validated models support operational decision-making and risk mitigation."
        ),
        key_factors=[
            "Friction factor variability",
            "Mud rheology and hydraulics",
            "Wellbore geometry and tortuosity",
            "Cuttings concentration",
            "Drill string configuration",
            "Field calibration data"
        ],
        primary_authority=[
            "SPE Paper 334466 - Torque and Drag Modeling for ERD Wells",
            "Schlumberger Drilling Manual Chapter 12",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Simplified models preferred for operational speed",
        counter_arguments=[
            "Simplified models reduce computational time",
            "Operational experience compensates for model inaccuracies",
            "Real-time data can correct predictions"
        ],
        resolution_strategy=(
            "Use advanced models for planning and simplified models for real-time adjustments. "
            "Continuously update models with field data. "
            "Train personnel on model limitations and applications."
        ),
        entity_scope="Extended Reach Drilling Operations",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 334466 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Mud Rheology Impact on Directional Drilling",
        keywords=["mud rheology", "directional drilling", "hole cleaning", "torque and drag", "cuttings transport", "wellbore stability"],
        conclusion_template="Optimize mud rheology parameters to balance hole cleaning efficiency and torque reduction, maintaining plastic viscosity between {min_pv} and {max_pv} cP.",
        reasoning_framework=(
            "Mud rheology directly affects hydraulics, hole cleaning, and mechanical forces in directional drilling. "
            "High plastic viscosity improves cuttings suspension but increases torque and drag. "
            "Low viscosity reduces torque but risks cuttings settling and wellbore instability. "
            "The framework evaluates rheological models, field measurements, and operational outcomes to define optimal ranges. "
            "Adjustments consider formation type, well trajectory, and drilling parameters. "
            "Real-time monitoring of mud properties and drilling performance informs dynamic optimization."
        ),
        key_factors=[
            "Plastic viscosity",
            "Yield point",
            "Gel strength",
            "Cuttings concentration",
            "Wellbore inclination",
            "Flow rate"
        ],
        primary_authority=[
            "API RP 13B-1 - Mud Properties and Testing",
            "SPE Paper 556688 - Mud Rheology Effects on Directional Drilling",
            "Halliburton Drilling Fluids Manual"
        ],
        burden_holder="Mud Engineer",
        adversary_position="Operational preference for higher flow rates over rheology optimization",
        counter_arguments=[
            "Higher flow rates improve hole cleaning regardless of rheology",
            "Rheology adjustments are time-consuming",
            "Mud additives increase cost"
        ],
        resolution_strategy=(
            "Implement integrated mud and drilling parameter management. "
            "Use real-time rheology monitoring and automated adjustments. "
            "Train personnel on rheology impact and control techniques."
        ),
        entity_scope="Mud Engineering and Directional Drilling",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and SPE 556688"
    ),
    DoctrineBlock(
        topic="Drill String Vibrations and Mitigation",
        keywords=["drill string vibrations", "axial vibration", "torsional vibration", "lateral vibration", "mitigation", "directional drilling"],
        conclusion_template="Implement vibration monitoring and mitigation strategies including optimized RPM, stabilizer placement, and shock subs to reduce vibration-induced failures by {mitigation_effectiveness}%.",
        reasoning_framework=(
            "Drill string vibrations cause fatigue, tool failure, and reduced drilling efficiency. "
            "Types include axial (bit bounce), torsional (stick-slip), and lateral (whirl) vibrations. "
            "The framework involves vibration detection using downhole sensors, analysis of vibration modes, and identification of causative factors. "
            "Mitigation includes adjusting rotational speed, weight on bit, BHA design with stabilizers and shock subs, and drilling parameter optimization. "
            "Field data and modeling support selection of effective strategies."
        ),
        key_factors=[
            "Rotational speed (RPM)",
            "Weight on bit (WOB)",
            "BHA design and stabilizers",
            "Shock absorber tools",
            "Formation properties",
            "Downhole vibration sensor data"
        ],
        primary_authority=[
            "SPE Paper 223355 - Drill String Vibration Analysis and Control",
            "Halliburton Drilling Manual Chapter 11",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Preference for maximum RPM to increase penetration rate",
        counter_arguments=[
            "Higher RPM improves rate of penetration",
            "Vibration effects are manageable with tool design",
            "Monitoring equipment adds cost and complexity"
        ],
        resolution_strategy=(
            "Balance RPM and WOB to minimize harmful vibrations. "
            "Use vibration monitoring tools and adjust parameters proactively. "
            "Design BHAs with vibration mitigation components."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 223355 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Hydraulics Optimization in Directional Drilling",
        keywords=["hydraulics", "mud flow", "pressure loss", "hole cleaning", "directional drilling", "nozzle selection"],
        conclusion_template="Optimize hydraulics by selecting nozzle sizes and flow rates that maintain annular velocities above {min_annular_velocity} m/s to ensure effective hole cleaning and minimize pressure losses.",
        reasoning_framework=(
            "Hydraulics influence cuttings transport, wellbore stability, and downhole tool performance. "
            "Directional wells have complex geometries affecting pressure losses and flow distribution. "
            "The framework analyzes hydraulic models, pressure measurements, and flow regimes. "
            "Nozzle selection balances jet impact force and flow rate to optimize cleaning and minimize erosion. "
            "Operational adjustments consider formation sensitivity and mud properties. "
            "Continuous monitoring and modeling support hydraulic optimization."
        ),
        key_factors=[
            "Annular velocity",
            "Nozzle size and configuration",
            "Mud rheology",
            "Pressure losses",
            "Wellbore geometry",
            "Cuttings load"
        ],
        primary_authority=[
            "API RP 13B-1 - Drilling Fluids Hydraulics",
            "SPE Paper 445588 - Hydraulics Optimization in Directional Wells",
            "Halliburton Drilling Fluids Manual"
        ],
        burden_holder="Mud Engineer and Drilling Engineer",
        adversary_position="Operational focus on maximizing flow rate regardless of hydraulics",
        counter_arguments=[
            "Higher flow rates improve hole cleaning",
            "Pressure losses are acceptable trade-offs",
            "Nozzle changes increase operational complexity"
        ],
        resolution_strategy=(
            "Use hydraulic modeling to guide nozzle and flow rate selection. "
            "Monitor pressure and flow parameters in real-time. "
            "Adjust mud properties to complement hydraulic design."
        ),
        entity_scope="Mud Engineering and Directional Drilling",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and SPE 445588"
    ),
    DoctrineBlock(
        topic="Directional Drilling Risk Management",
        keywords=["risk management", "directional drilling", "hazard identification", "mitigation", "operational safety", "incident prevention"],
        conclusion_template="Implement comprehensive risk management frameworks including hazard identification, risk assessment, and mitigation plans to reduce directional drilling incidents by {risk_reduction}%.",
        reasoning_framework=(
            "Directional drilling involves complex operations with inherent risks including stuck pipe, wellbore instability, and collision. "
            "Risk management frameworks identify hazards, assess likelihood and impact, and implement controls. "
            "The framework integrates technical, operational, and human factors. "
            "Continuous monitoring, training, and communication are essential. "
            "Incident data analysis informs improvement. "
            "The doctrine promotes a culture of safety and proactive risk mitigation."
        ),
        key_factors=[
            "Hazard identification processes",
            "Risk assessment methodologies",
            "Operational controls",
            "Training and competency",
            "Incident reporting and analysis",
            "Communication and coordination"
        ],
        primary_authority=[
            "API RP 75 - Safety and Environmental Management Systems",
            "SPE Paper 556699 - Risk Management in Directional Drilling",
            "Company HSE Policies"
        ],
        burden_holder="All Directional Drilling Personnel",
        adversary_position="Operational pressures to prioritize production over safety",
        counter_arguments=[
            "Production targets justify risk acceptance",
            "Safety measures increase operational costs",
            "Experience reduces need for formal risk management"
        ],
        resolution_strategy=(
            "Embed risk management into all operational phases. "
            "Balance production and safety through informed decision-making. "
            "Foster continuous improvement and accountability."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API RP 75 and SPE 556699"
    ),
    DoctrineBlock(
        topic="Directional Drilling Data Integration and Management",
        keywords=["data integration", "directional drilling", "real-time data", "data management", "decision support", "digital oilfield"],
        conclusion_template="Establish integrated data management systems combining MWD, LWD, drilling parameters, and geological models to support real-time decision-making and optimize directional drilling outcomes.",
        reasoning_framework=(
            "Directional drilling generates diverse data streams requiring integration for effective decision-making. "
            "Data management systems collect, process, and visualize information from MWD, LWD, rig sensors, and geological models. "
            "The framework addresses data quality, latency, interoperability, and user accessibility. "
            "Advanced analytics and machine learning enhance predictive capabilities. "
            "Integrated systems reduce operational risks, improve efficiency, and support collaboration."
        ),
        key_factors=[
            "Data acquisition systems",
            "Communication infrastructure",
            "Data processing and storage",
            "Visualization tools",
            "Analytics and modeling",
            "User training"
        ],
        primary_authority=[
            "SPE Paper 667799 - Data Integration in Directional Drilling",
            "Schlumberger Digital Oilfield Whitepaper",
            "API RP 13B-3 - Logging While Drilling"
        ],
        burden_holder="Directional Drilling Data Manager",
        adversary_position="Legacy systems and siloed data impede integration",
        counter_arguments=[
            "System upgrades are costly and disruptive",
            "Data security concerns limit sharing",
            "User resistance to new technologies"
        ],
        resolution_strategy=(
            "Develop phased integration plans. "
            "Ensure cybersecurity measures. "
            "Provide training and change management support."
        ),
        entity_scope="Directional Drilling Operations and IT",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 667799 and API RP 13B-3"
    ),
    DoctrineBlock(
        topic="Directional Drilling Cost Optimization",
        keywords=["cost optimization", "directional drilling", "operational efficiency", "drilling time", "tool selection", "risk management"],
        conclusion_template="Optimize directional drilling costs by balancing tool selection, drilling parameters, and risk mitigation strategies to achieve target well delivery within budget.",
        reasoning_framework=(
            "Directional drilling costs are influenced by tool choices, drilling parameters, operational risks, and non-productive time. "
            "The framework evaluates cost drivers, trade-offs between speed and quality, and risk-related expenses. "
            "Optimization involves selecting appropriate tools and techniques, managing drilling parameters to reduce wear and failures, and implementing effective risk controls. "
            "Continuous monitoring and data analysis support cost control and efficiency improvements."
        ),
        key_factors=[
            "Tool costs and reliability",
            "Drilling parameters (RPM, WOB, flow rate)",
            "Non-productive time",
            "Risk mitigation expenses",
            "Operational efficiency",
            "Contractual and regulatory factors"
        ],
        primary_authority=[
            "SPE Paper 778800 - Cost Optimization in Directional Drilling",
            "Halliburton Drilling Manual Chapter 14",
            "Company Financial Policies"
        ],
        burden_holder="Drilling Project Manager",
        adversary_position="Pressure to reduce upfront costs at expense of quality",
        counter_arguments=[
            "Lower initial costs improve project economics",
            "Quality improvements increase costs",
            "Risk mitigation is seen as optional"
        ],
        resolution_strategy=(
            "Adopt balanced cost-quality-risk approach. "
            "Use data-driven decision-making. "
            "Engage stakeholders in cost optimization planning."
        ),
        entity_scope="Directional Drilling Project Management",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 778800 and Company Policies"
    ),
    DoctrineBlock(
        topic="Directional Drilling Personnel Training and Competency",
        keywords=["training", "competency", "directional drilling", "skill development", "operational safety", "performance"],
        conclusion_template="Implement comprehensive training programs and competency assessments to ensure personnel meet operational and safety standards in directional drilling.",
        reasoning_framework=(
            "Personnel competency directly impacts directional drilling performance and safety. "
            "Training programs cover technical skills, safety procedures, and operational best practices. "
            "Competency assessments verify knowledge and practical abilities. "
            "The framework includes continuous professional development, certification, and knowledge transfer. "
            "Effective training reduces incidents, improves efficiency, and supports technology adoption."
        ),
        key_factors=[
            "Training curriculum and materials",
            "Assessment methods",
            "Certification standards",
            "Continuous learning opportunities",
            "Knowledge management",
            "Safety culture"
        ],
        primary_authority=[
            "API RP 75 - Safety and Environmental Management Systems",
            "SPE Paper 889900 - Training and Competency in Directional Drilling",
            "Company Training Policies"
        ],
        burden_holder="Human Resources and Training Departments",
        adversary_position="Operational demands limit training time",
        counter_arguments=[
            "Training reduces available manpower",
            "Experienced personnel can train on the job",
            "Training costs are high"
        ],
        resolution_strategy=(
            "Integrate training into operational schedules. "
            "Use blended learning approaches. "
            "Measure training effectiveness and adjust programs."
        ),
        entity_scope="Personnel Management",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 75 and SPE 889900"
    ),
    DoctrineBlock(
        topic="Directional Drilling Environmental Impact Mitigation",
        keywords=["environmental impact", "directional drilling", "waste management", "emissions", "spill prevention", "regulatory compliance"],
        conclusion_template="Adopt best practices in waste management, emissions control, and spill prevention to minimize environmental impact of directional drilling operations.",
        reasoning_framework=(
            "Directional drilling operations can impact the environment through waste generation, emissions, and potential spills. "
            "The framework includes identification of environmental risks, implementation of control measures, and compliance with regulations. "
            "Best practices involve proper waste handling, use of low-toxicity fluids, emissions monitoring, and emergency response planning. "
            "Continuous improvement and stakeholder engagement support sustainable operations."
        ),
        key_factors=[
            "Waste handling procedures",
            "Emissions monitoring",
            "Spill prevention measures",
            "Regulatory requirements",
            "Training and awareness",
            "Emergency response capabilities"
        ],
        primary_authority=[
            "API RP 75 - Environmental Management",
            "SPE Paper 990011 - Environmental Best Practices in Directional Drilling",
            "Local Environmental Regulations"
        ],
        burden_holder="Environmental and HSE Teams",
        adversary_position="Operational pressures to prioritize drilling speed over environmental controls",
        counter_arguments=[
            "Environmental controls increase operational costs",
            "Some measures reduce drilling efficiency",
            "Regulatory compliance is burdensome"
        ],
        resolution_strategy=(
            "Integrate environmental management into operational planning. "
            "Engage stakeholders and regulators proactively. "
            "Monitor and report environmental performance transparently."
        ),
        entity_scope="Environmental Management",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 75 and SPE 990011"
    ),
    DoctrineBlock(
        topic="Directional Drilling Well Control Procedures",
        keywords=["well control", "directional drilling", "kick detection", "blowout prevention", "pressure management", "safety"],
        conclusion_template="Implement rigorous well control procedures including kick detection, pressure monitoring, and blowout prevention equipment to maintain well integrity during directional drilling.",
        reasoning_framework=(
            "Well control is critical to prevent kicks and blowouts, which pose safety and environmental hazards. "
            "Directional drilling introduces complexities in pressure management due to trajectory and formation variations. "
            "The framework includes monitoring mud weight, pressure, and flow rates; using blowout preventers; and training personnel. "
            "Early kick detection and response protocols minimize incident severity. "
            "Regular equipment testing and maintenance ensure reliability."
        ),
        key_factors=[
            "Mud weight and density control",
            "Pressure and flow monitoring",
            "Blowout preventer functionality",
            "Kick detection systems",
            "Personnel training",
            "Emergency response plans"
        ],
        primary_authority=[
            "API RP 59 - Well Control",
            "SPE Paper 112244 - Well Control in Directional Drilling",
            "Company Safety Procedures"
        ],
        burden_holder="Drilling and Well Control Teams",
        adversary_position="Operational pressures to maintain drilling progress during pressure anomalies",
        counter_arguments=[
            "Stopping drilling reduces efficiency",
            "False alarms cause unnecessary delays",
            "Equipment maintenance is costly"
        ],
        resolution_strategy=(
            "Prioritize safety over drilling speed. "
            "Use reliable detection and response systems. "
            "Maintain rigorous training and equipment standards."
        ),
        entity_scope="Well Control Operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API RP 59 and SPE 112244"
    ),
    DoctrineBlock(
        topic="Directional Drilling Communication Protocols",
        keywords=["communication", "directional drilling", "real-time data", "team coordination", "decision making", "operational efficiency"],
        conclusion_template="Establish clear communication protocols integrating real-time data sharing and multidisciplinary coordination to enhance directional drilling decision-making and efficiency.",
        reasoning_framework=(
            "Effective communication is essential for safe and efficient directional drilling operations. "
            "Protocols define data sharing, reporting structures, and decision-making processes. "
            "The framework includes use of digital communication tools, standardized reporting formats, and regular coordination meetings. "
            "Multidisciplinary collaboration among geologists, engineers, and rig personnel ensures aligned objectives. "
            "Clear communication reduces errors, delays, and safety incidents."
        ),
        key_factors=[
            "Real-time data availability",
            "Communication tools and infrastructure",
            "Standard operating procedures",
            "Team roles and responsibilities",
            "Training in communication skills",
            "Feedback and continuous improvement"
        ],
        primary_authority=[
            "SPE Paper 223366 - Communication Best Practices in Directional Drilling",
            "Company Operational Procedures",
            "API RP 75 - Safety and Environmental Management Systems"
        ],
        burden_holder="Directional Drilling Manager",
        adversary_position="Operational pressures leading to communication shortcuts",
        counter_arguments=[
            "Informal communication is faster",
            "Formal protocols slow decision-making",
            "Technology adoption faces resistance"
        ],
        resolution_strategy=(
            "Implement user-friendly communication systems. "
            "Train teams on protocols and benefits. "
            "Monitor communication effectiveness and adapt."
        ),
        entity_scope="Operational Management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 223366 and API RP 75"
    ),
    DoctrineBlock(
        topic="Directional Drilling Equipment Maintenance",
        keywords=["equipment maintenance", "directional drilling", "tool reliability", "preventive maintenance", "failure reduction"],
        conclusion_template="Adopt preventive maintenance schedules and condition monitoring to enhance directional drilling equipment reliability and reduce failure rates by {failure_reduction}%.",
        reasoning_framework=(
            "Reliable equipment is vital for uninterrupted directional drilling operations. "
            "Preventive maintenance identifies and addresses wear and defects before failures occur. "
            "Condition monitoring uses sensor data to assess tool health in real-time. "
            "The framework includes maintenance planning, execution, and feedback loops. "
            "Effective maintenance reduces downtime, repair costs, and safety risks."
        ),
        key_factors=[
            "Maintenance schedules",
            "Condition monitoring technologies",
            "Failure mode analysis",
            "Spare parts management",
            "Personnel training",
            "Maintenance documentation"
        ],
        primary_authority=[
            "API RP 7G - Drilling Equipment",
            "SPE Paper 334477 - Equipment Maintenance in Directional Drilling",
            "Company Maintenance Policies"
        ],
        burden_holder="Maintenance and Operations Teams",
        adversary_position="Operational pressures to extend maintenance intervals",
        counter_arguments=[
            "Longer intervals reduce downtime",
            "Condition monitoring can replace some maintenance",
            "Maintenance costs are high"
        ],
        resolution_strategy=(
            "Balance maintenance frequency with operational risk. "
            "Use condition monitoring to optimize schedules. "
            "Train personnel on maintenance importance."
        ),
        entity_scope="Equipment Management",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 7G and SPE 334477"
    ),
    DoctrineBlock(
        topic="Directional Drilling Regulatory Compliance",
        keywords=["regulatory compliance", "directional drilling", "permits", "reporting", "safety standards", "environmental regulations"],
        conclusion_template="Ensure all directional drilling activities comply with applicable regulations, including permits, reporting, and adherence to safety and environmental standards.",
        reasoning_framework=(
            "Compliance with regulatory requirements is mandatory to operate directional drilling activities legally and safely. "
            "The framework includes understanding applicable laws, obtaining necessary permits, conducting required reporting, and implementing mandated safety and environmental controls. "
            "Non-compliance risks legal penalties, operational shutdowns, and reputational damage. "
            "Continuous monitoring and audit readiness support compliance."
        ),
        key_factors=[
            "Applicable laws and regulations",
            "Permit acquisition and management",
            "Reporting requirements",
            "Safety and environmental standards",
            "Audit and inspection readiness",
            "Training and awareness"
        ],
        primary_authority=[
            "Local and national regulatory bodies",
            "API Standards",
            "Company Compliance Policies"
        ],
        burden_holder="Regulatory Affairs and Operations Teams",
        adversary_position="Operational pressures leading to regulatory shortcuts",
        counter_arguments=[
            "Compliance processes delay operations",
            "Regulations are complex and costly",
            "Some requirements are redundant"
        ],
        resolution_strategy=(
            "Integrate compliance into operational planning. "
            "Engage regulators proactively. "
            "Train personnel on regulatory importance."
        ),
        entity_scope="Regulatory Management",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API Standards and Local Regulations"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Stability",
        keywords=["wellbore stability", "directional drilling", "formation pressure", "mud weight", "shale swelling", "wellbore collapse"],
        conclusion_template="Maintain mud weight within the window between pore pressure and fracture gradient to ensure wellbore stability and prevent collapse or fracturing.",
        reasoning_framework=(
            "Wellbore stability is critical to prevent collapse, fracturing, and stuck pipe incidents. "
            "Directional wells experience varying stresses due to trajectory and formation changes. "
            "The framework involves geomechanical modeling of formation stresses, pore pressures, and fracture gradients. "
            "Mud weight is adjusted to balance these forces, preventing instability. "
            "Consideration of shale swelling and chemical interactions informs mud design. "
            "Continuous monitoring of drilling parameters and cuttings supports stability assessment."
        ),
        key_factors=[
            "Pore pressure and fracture gradient",
            "Mud weight and properties",
            "Formation mechanical properties",
            "Wellbore trajectory",
            "Chemical interactions",
            "Drilling parameters"
        ],
        primary_authority=[
            "SPE Paper 445599 - Wellbore Stability in Directional Drilling",
            "API RP 13B-1 - Drilling Fluids",
            "Schlumberger Geomechanics Handbook"
        ],
        burden_holder="Drilling Engineer and Mud Engineer",
        adversary_position="Operational pressures to reduce mud weight to increase penetration",
        counter_arguments=[
            "Lower mud weight improves rate of penetration",
            "Higher mud weight increases costs",
            "Stability issues can be managed reactively"
        ],
        resolution_strategy=(
            "Use geomechanical models to define mud weight windows. "
            "Monitor drilling parameters and adjust proactively. "
            "Train personnel on stability risks and controls."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SPE 445599 and API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Cleaning Practices",
        keywords=["wellbore cleaning", "directional drilling", "cuttings transport", "mud hydraulics", "hole cleaning efficiency"],
        conclusion_template="Maintain annular velocities above {min_annular_velocity} m/s and optimize mud properties to ensure effective cuttings transport and prevent accumulation.",
        reasoning_framework=(
            "Effective wellbore cleaning prevents cuttings accumulation, stuck pipe, and poor drilling performance. "
            "Directional wells have complex geometries affecting cuttings transport. "
            "The framework analyzes hydraulic parameters, mud rheology, and wellbore inclination. "
            "Optimizing annular velocity and mud properties improves hole cleaning. "
            "Real-time monitoring of pump pressure and cuttings volume supports operational adjustments."
        ),
        key_factors=[
            "Annular velocity",
            "Mud rheology",
            "Pump rate and pressure",
            "Wellbore inclination and geometry",
            "Cuttings concentration",
            "Drilling parameters"
        ],
        primary_authority=[
            "API RP 13B-1 - Drilling Fluids",
            "SPE Paper 556699 - Wellbore Cleaning in Directional Drilling",
            "Halliburton Drilling Fluids Manual"
        ],
        burden_holder="Mud Engineer and Drilling Engineer",
        adversary_position="Operational focus on maximizing penetration over cleaning",
        counter_arguments=[
            "Higher penetration reduces overall rig time",
            "Cleaning issues can be addressed reactively",
            "Mud property adjustments are costly"
        ],
        resolution_strategy=(
            "Balance drilling parameters to optimize cleaning. "
            "Use real-time monitoring and proactive adjustments. "
            "Train personnel on cleaning importance."
        ),
        entity_scope="Mud Engineering and Directional Drilling",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and SPE 556699"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Tortuosity Measurement Techniques",
        keywords=["wellbore tortuosity", "measurement", "directional drilling", "survey data", "torque and drag", "vibration analysis"],
        conclusion_template="Combine high-resolution directional surveys with torque, drag, and vibration data to accurately quantify wellbore tortuosity and inform corrective actions.",
        reasoning_framework=(
            "Measuring wellbore tortuosity is essential for diagnosing drilling issues and optimizing well path quality. "
            "High-resolution directional surveys provide geometric data. "
            "Torque and drag measurements indicate mechanical effects of tortuosity. "
            "Vibration analysis identifies dynamic impacts. "
            "Integrating these data sources enables comprehensive assessment. "
            "The framework supports decision-making for BHA adjustments and drilling parameter optimization."
        ),
        key_factors=[
            "Directional survey resolution",
            "Torque and drag sensor data",
            "Vibration sensor data",
            "Data integration techniques",
            "BHA design",
            "Drilling parameters"
        ],
        primary_authority=[
            "SPE Paper 667700 - Wellbore Tortuosity Measurement",
            "Halliburton Drilling Manual Chapter 13",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Limited survey frequency and sensor availability",
        counter_arguments=[
            "High-frequency surveys increase operational time",
            "Additional sensors increase costs",
            "Data integration complexity"
        ],
        resolution_strategy=(
            "Optimize survey intervals balancing accuracy and efficiency. "
            "Use multi-sensor data fusion techniques. "
            "Train personnel on data interpretation."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 667700 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Directional Drilling Torque and Drag Real-Time Monitoring",
        keywords=["torque and drag", "real-time monitoring", "directional drilling", "sensor data", "operational control"],
        conclusion_template="Implement real-time torque and drag monitoring systems with threshold alarms to enable proactive operational adjustments and reduce drilling risks.",
        reasoning_framework=(
            "Real-time monitoring of torque and drag provides early warning of drilling problems such as stuck pipe or excessive wear. "
            "Sensor data is analyzed against thresholds and historical baselines. "
            "The framework includes data acquisition, processing, visualization, and alarm management. "
            "Proactive adjustments to drilling parameters based on monitoring improve safety and efficiency."
        ),
        key_factors=[
            "Sensor accuracy and reliability",
            "Data processing algorithms",
            "Alarm thresholds and logic",
            "Operator training",
            "Integration with drilling control systems",
            "Historical data analysis"
        ],
        primary_authority=[
            "SPE Paper 778811 - Real-Time Torque and Drag Monitoring",
            "Schlumberger Drilling Manual Chapter 14",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Drilling Engineer and Rig Personnel",
        adversary_position="Operational focus on drilling speed over monitoring",
        counter_arguments=[
            "Monitoring systems add complexity",
            "False alarms disrupt operations",
            "Additional training required"
        ],
        resolution_strategy=(
            "Calibrate alarm thresholds to minimize false positives. "
            "Train personnel on system use and response. "
            "Integrate monitoring into standard operating procedures."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 778811 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Position Uncertainty Management",
        keywords=["wellbore position", "uncertainty", "directional drilling", "survey accuracy", "risk management"],
        conclusion_template="Quantify and manage wellbore position uncertainties using statistical models and conservative planning margins to mitigate operational risks.",
        reasoning_framework=(
            "Wellbore position uncertainty arises from survey instrument errors, data processing, and environmental factors. "
            "Accurate quantification supports risk management including collision avoidance and reservoir targeting. "
            "The framework uses statistical error models, uncertainty ellipses, and conservative design margins. "
            "Operational decisions incorporate uncertainty to ensure safety and effectiveness."
        ),
        key_factors=[
            "Survey instrument precision",
            "Data processing methods",
            "Environmental influences",
            "Statistical error modeling",
            "Operational planning margins",
            "Real-time data integration"
        ],
        primary_authority=[
            "API RP 13B-2 - Directional Surveying",
            "SPE Paper 889911 - Wellbore Position Uncertainty Analysis",
            "Company Drilling Standards"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Pressure to minimize planning margins for reservoir contact",
        counter_arguments=[
            "Smaller margins increase reservoir exposure",
            "Advanced tools reduce uncertainty",
            "Operational experience compensates"
        ],
        resolution_strategy=(
            "Balance reservoir contact with safety margins. "
            "Use best available data and models. "
            "Update uncertainty assessments with real-time data."
        ),
        entity_scope="Directional Drilling Planning",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 13B-2 and SPE 889911"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Tortuosity Impact on Completion",
        keywords=["wellbore tortuosity", "completion", "directional drilling", "packer setting", "stimulation", "production"],
        conclusion_template="Minimize wellbore tortuosity to ensure reliable completion tool deployment, effective stimulation, and optimal production performance.",
        reasoning_framework=(
            "Excessive wellbore tortuosity complicates completion operations including packer setting, perforation, and stimulation. "
            "The framework examines mechanical constraints of completion tools, fluid flow dynamics, and stimulation effectiveness. "
            "Reducing tortuosity improves tool conveyance, zonal isolation, and production efficiency. "
            "Coordination between drilling and completion teams is essential."
        ),
        key_factors=[
            "Wellbore geometry",
            "Completion tool specifications",
            "Stimulation fluid dynamics",
            "Production data",
            "Directional drilling quality metrics",
            "Interdisciplinary communication"
        ],
        primary_authority=[
            "SPE Paper 990022 - Wellbore Tortuosity Effects on Completion",
            "Halliburton Completion Manual",
            "API RP 90 - Wellbore Positioning"
        ],
        burden_holder="Directional Drilling and Completion Engineers",
        adversary_position="Operational focus on drilling speed over wellbore quality",
        counter_arguments=[
            "Faster drilling reduces overall project time",
            "Completion tools can adapt to tortuosity",
            "Stimulation can compensate for geometry issues"
        ],
        resolution_strategy=(
            "Plan and execute drilling to minimize tortuosity. "
            "Coordinate drilling and completion designs. "
            "Monitor and adjust operations based on feedback."
        ),
        entity_scope="Drilling and Completion Operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 990022 and API RP 90"
    ),
    DoctrineBlock(
        topic="Directional Drilling Extended Reach Well Planning",
        keywords=["extended reach drilling", "well planning", "trajectory design", "torque and drag", "hydraulics", "risk assessment"],
        conclusion_template="Incorporate comprehensive torque, drag, and hydraulic modeling in ERD well planning to optimize trajectory and mitigate operational risks.",
        reasoning_framework=(
            "ERD wells require detailed planning due to increased mechanical and hydraulic challenges. "
            "The framework integrates trajectory design with torque and drag predictions, hydraulic modeling, and risk assessments. "
            "Iterative modeling and sensitivity analyses inform design decisions. "
            "Planning includes contingency strategies for operational challenges."
        ),
        key_factors=[
            "Trajectory complexity",
            "Torque and drag predictions",
            "Hydraulic pressure losses",
            "Mud properties",
            "Risk identification",
            "Contingency planning"
        ],
        primary_authority=[
            "SPE Paper 112255 - ERD Well Planning Best Practices",
            "Schlumberger Drilling Manual Chapter 15",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Drilling Engineer and Planning Team",
        adversary_position="Pressure to minimize planning time and costs",
        counter_arguments=[
            "Simplified planning reduces upfront costs",
            "Operational experience can manage risks",
            "Advanced tools can compensate for planning gaps"
        ],
        resolution_strategy=(
            "Allocate sufficient resources for detailed planning. "
            "Use validated models and expert review. "
            "Update plans based on real-time data."
        ),
        entity_scope="Well Planning",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 112255 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Directional Drilling Real-Time Decision Support Systems",
        keywords=["decision support", "real-time data", "directional drilling", "automation", "risk reduction", "operational efficiency"],
        conclusion_template="Deploy real-time decision support systems integrating data analytics and automation to enhance directional drilling safety and efficiency.",
        reasoning_framework=(
            "Decision support systems process real-time data to provide actionable insights and automate routine decisions. "
            "The framework includes data integration, analytics algorithms, user interfaces, and automation controls. "
            "Benefits include reduced human error, faster response times, and optimized drilling parameters. "
            "System design considers usability, reliability, and integration with existing workflows."
        ),
        key_factors=[
            "Data quality and latency",
            "Analytics and machine learning models",
            "User interface design",
            "Automation capabilities",
            "System reliability",
            "Training and change management"
        ],
        primary_authority=[
            "SPE Paper 334488 - Real-Time Decision Support in Directional Drilling",
            "Schlumberger Digital Oilfield Whitepaper",
            "API RP 13B-3 - Logging While Drilling"
        ],
        burden_holder="Directional Drilling Manager and IT Teams",
        adversary_position="Resistance to automation and technology adoption",
        counter_arguments=[
            "Automation reduces operator control",
            "Systems are costly and complex",
            "Training requirements are high"
        ],
        resolution_strategy=(
            "Engage users in system design. "
            "Provide comprehensive training. "
            "Demonstrate benefits through pilot projects."
        ),
        entity_scope="Operational Management",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 334488 and API RP 13B-3"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Cleaning Optimization",
        keywords=["wellbore cleaning", "cuttings transport", "mud hydraulics", "directional drilling", "hole cleaning efficiency"],
        conclusion_template="Optimize annular flow velocity and mud rheology to maximize cuttings transport efficiency and minimize accumulation in directional wells.",
        reasoning_framework=(
            "Effective wellbore cleaning prevents operational issues such as stuck pipe and poor drilling performance. "
            "Directional wells pose challenges due to complex geometry affecting flow patterns. "
            "The framework evaluates hydraulic parameters, mud properties, and wellbore inclination. "
            "Optimizing these factors enhances cuttings suspension and transport. "
            "Real-time monitoring supports dynamic adjustments."
        ),
        key_factors=[
            "Annular velocity",
            "Mud rheology",
            "Pump rate and pressure",
            "Wellbore geometry",
            "Cuttings concentration",
            "Drilling parameters"
        ],
        primary_authority=[
            "API RP 13B-1 - Drilling Fluids",
            "SPE Paper 556700 - Wellbore Cleaning Optimization",
            "Halliburton Drilling Fluids Manual"
        ],
        burden_holder="Mud Engineer and Drilling Engineer",
        adversary_position="Operational focus on maximizing penetration over cleaning",
        counter_arguments=[
            "Higher penetration reduces overall rig time",
            "Cleaning issues can be addressed reactively",
            "Mud property adjustments are costly"
        ],
        resolution_strategy=(
            "Balance drilling parameters to optimize cleaning. "
            "Use real-time monitoring and proactive adjustments. "
            "Train personnel on cleaning importance."
        ),
        entity_scope="Mud Engineering and Directional Drilling",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 13B-1 and SPE 556700"
    ),
    DoctrineBlock(
        topic="Directional Drilling Torque and Drag Modeling Validation",
        keywords=["torque and drag", "model validation", "directional drilling", "field data", "model accuracy"],
        conclusion_template="Regularly validate torque and drag models against field measurements to maintain prediction accuracy within ±10%.",
        reasoning_framework=(
            "Torque and drag models guide drilling parameter selection and risk management. "
            "Validation against field data ensures model reliability. "
            "The framework includes data collection, statistical analysis, and model updating. "
            "Continuous validation supports operational confidence and model improvement."
        ),
        key_factors=[
            "Field measurement accuracy",
            "Model assumptions and parameters",
            "Data analysis techniques",
            "Model updating procedures",
            "Operational feedback",
            "Training"
        ],
        primary_authority=[
            "SPE Paper 778822 - Torque and Drag Model Validation",
            "Schlumberger Drilling Manual Chapter 16",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Operational reliance on unvalidated models",
        counter_arguments=[
            "Models are sufficiently accurate for planning",
            "Validation is time-consuming",
            "Field data may be inconsistent"
        ],
        resolution_strategy=(
            "Establish routine validation schedules. "
            "Use robust data collection and analysis. "
            "Train personnel on model limitations."
        ),
        entity_scope="Directional Drilling Operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="SPE 778822 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Directional Drilling BHA Vibration Mitigation Techniques",
        keywords=["BHA design", "vibration mitigation", "directional drilling", "shock subs", "stabilizers", "tool life"],
        conclusion_template="Incorporate shock subs and optimized stabilizer placement in BHA design to reduce vibration amplitudes and extend tool life by {tool_life_extension}%.",
        reasoning_framework=(
            "BHA vibrations cause tool wear and drilling inefficiencies. "
            "Shock subs absorb axial shocks; stabilizers control lateral vibrations. "
            "The framework evaluates vibration modes, tool mechanical properties, and formation interactions. "
            "Optimized BHA designs reduce harmful vibrations and improve drilling performance."
        ),
        key_factors=[
            "Shock sub specifications",
            "Stabilizer type and placement",
            "Formation properties",
            "Drilling parameters",
            "Vibration sensor data",
            "Tool life data"
        ],
        primary_authority=[
            "SPE Paper 334499 - BHA Vibration Mitigation",
            "Halliburton Drilling Manual Chapter 17",
            "API RP 7G - Drilling Equipment"
        ],
        burden_holder="Directional Drilling Engineer",
        adversary_position="Cost pressures to simplify BHA",
        counter_arguments=[
            "Simpler BHAs reduce upfront costs",
            "Vibration effects can be managed operationally",
            "Shock subs add complexity"
        ],
        resolution_strategy=(
            "Balance BHA complexity with cost and performance. "
            "Use vibration data to guide design. "
            "Train personnel on vibration impacts."
        ),
        entity_scope="Directional Drilling Tool Design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 334499 and API RP 7G"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Tortuosity Impact on Logging",
        keywords=["wellbore tortuosity", "logging while drilling", "directional drilling", "tool conveyance", "data quality"],
        conclusion_template="Minimize wellbore tortuosity to ensure reliable LWD tool conveyance and maintain high-quality logging data acquisition.",
        reasoning_framework=(
            "Excessive tortuosity hinders LWD tool movement and affects sensor orientation, degrading data quality. "
            "The framework examines mechanical constraints, tool design, and wellbore geometry. "
            "Reducing tortuosity improves tool reliability and data integrity."
        ),
        key_factors=[
            "Wellbore geometry",
            "LWD tool specifications",
            "Tortuosity metrics",
            "Logging data quality",
            "Directional drilling practices",
            "Operational coordination"
        ],
        primary_authority=[
            "SPE Paper 445600 - Tortuosity Effects on LWD",
            "Schlumberger Logging Manual",
            "API RP 13B-3 - Logging While Drilling"
        ],
        burden_holder="Directional Drilling and Logging Engineers",
        adversary_position="Operational focus on drilling speed over wellbore quality",
        counter_arguments=[
            "Faster drilling reduces project time",
            "LWD tools can compensate for tortuosity",
            "Data quality issues can be post-processed"
        ],
        resolution_strategy=(
            "Plan and execute drilling to minimize tortuosity. "
            "Coordinate drilling and logging operations. "
            "Monitor data quality and adjust practices."
        ),
        entity_scope="Drilling and Logging Operations",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="SPE 445600 and API RP 13B-3"
    ),
    DoctrineBlock(
        topic="Directional Drilling Extended Reach Drilling Hydraulics",
        keywords=["extended reach drilling", "hydraulics", "pressure loss", "mud flow", "directional drilling"],
        conclusion_template="Model and optimize hydraulics in ERD wells to manage pressure losses and maintain effective cuttings transport throughout extended horizontal sections.",
        reasoning_framework=(
            "ERD wells have long horizontal sections increasing hydraulic challenges. "
            "Pressure losses affect pump performance and cuttings transport. "
            "The framework includes hydraulic modeling, mud property optimization, and operational adjustments. "
            "Effective management prevents drilling problems and improves efficiency."
        ),
        key_factors=[
            "Pressure loss modeling",
            "Mud rheology",
            "Pump performance",
            "Wellbore geometry",
            "Cuttings concentration",
            "Flow rate"
        ],
        primary_authority=[
            "SPE Paper 556700 - ERD Hydraulics Optimization",
            "API RP 13B-1 - Drilling Fluids",
            "Halliburton Drilling Fluids Manual"
        ],
        burden_holder="Mud Engineer and Drilling Engineer",
        adversary_position="Operational focus on maximizing flow rates",
        counter_arguments=[
            "Higher flow rates improve cleaning",
            "Pressure losses are acceptable trade-offs",
            "Mud property adjustments are costly"
        ],
        resolution_strategy=(
            "Use hydraulic models to guide operations. "
            "Monitor pressures and flow in real-time. "
            "Adjust mud properties proactively."
        ),
        entity_scope="Mud Engineering and Directional Drilling",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SPE 556700 and API RP 13B-1"
    ),
    DoctrineBlock(
        topic="Directional Drilling Wellbore Tortuosity Impact on Stimulation",
        keywords=["wellbore tortuosity", "stimulation", "directional drilling", "fracturing", "production"],
        conclusion_template="Minimize wellbore tortuosity to ensure uniform stimulation fluid placement and maximize fracture effectiveness.",
        reasoning_framework=(
            "Tortuosity affects fluid flow during stimulation, potentially causing uneven fracture propagation and reduced