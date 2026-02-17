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
        topic="CT Fatigue Life Prediction - Low-Cycle Fatigue",
        keywords=["coiled tubing", "fatigue", "life prediction", "low-cycle", "material failure", "bending", "cycling"],
        conclusion_template="The expected fatigue life of the CT string is determined by cumulative low-cycle fatigue damage, calculated using Miner's Rule and validated against manufacturer S-N curves.",
        reasoning_framework="""
Fatigue life prediction for coiled tubing (CT) in drilling operations is based on the accumulation of cyclic stresses as the tubing is repeatedly bent over the reel and gooseneck. The process involves:
1. Segmenting the CT string into discrete elements.
2. Calculating the strain range for each element per operational cycle.
3. Referencing manufacturer-provided S-N (stress-life) curves for the tubing material.
4. Applying Miner's Rule to sum the damage fraction for each cycle: D = Σ(n_i/N_i), where n_i is the number of cycles at stress level i, and N_i is the cycles to failure at that level.
5. Including correction factors for welds, corrosion, and operational anomalies.
6. Comparing the cumulative damage to a critical threshold (typically D=1) to determine end-of-life.
7. Incorporating real-time monitoring data (e.g., cycle counters, strain gauges) to refine predictions.
8. Validating the model with historical failure data and periodic NDT inspections.
""",
        key_factors=[
            "Bend diameter (reel/gooseneck)",
            "Material S-N curve",
            "Cycle count and amplitude",
            "Weld locations",
            "Corrosion presence",
            "Operational temperature",
            "Real-time monitoring data"
        ],
        primary_authority=[
            "API RP 5C7",
            "ICoTA Fatigue Guidelines",
            "Manufacturer S-N Data"
        ],
        burden_holder="CT Operator",
        adversary_position="Fatigue life is overestimated; actual cycles to failure are lower due to unaccounted factors.",
        counter_arguments=[
            "Model incorporates conservative safety factors.",
            "Real-time monitoring adjusts for operational anomalies.",
            "NDT inspections validate predicted life."
        ],
        resolution_strategy="Periodic validation with NDT and updating the fatigue model with field data.",
        entity_scope="CT Strings in DRL14 Operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 5C7 Section 7"
    ),
    DoctrineBlock(
        topic="CT String Design - OD Selection and Wall Thickness",
        keywords=["coiled tubing", "string design", "outer diameter", "wall thickness", "collapse", "burst", "tensile strength"],
        conclusion_template="The optimal OD and wall thickness for CT string are selected to balance collapse resistance, burst pressure, and tensile strength, ensuring safe operation under anticipated loads.",
        reasoning_framework="""
CT string design begins with load analysis for the intended well profile and operational envelope. The process involves:
1. Determining maximum anticipated internal and external pressures (burst/collapse).
2. Calculating required wall thickness using API equations for burst and collapse resistance.
3. Verifying tensile strength for pulling loads, including overpull and dynamic effects.
4. Selecting OD to optimize hydraulic performance and minimize friction.
5. Considering manufacturing tolerances and corrosion allowances.
6. Reviewing compatibility with BOPs, connectors, and downhole tools.
7. Consulting manufacturer recommendations and field experience.
8. Validating design with finite element analysis (FEA) if necessary.
""",
        key_factors=[
            "Maximum burst/collapse pressures",
            "Tensile load requirements",
            "Hydraulic performance",
            "Corrosion allowance",
            "Tool compatibility"
        ],
        primary_authority=[
            "API RP 5C7",
            "Manufacturer Design Guidelines"
        ],
        burden_holder="CT Design Engineer",
        adversary_position="Selected dimensions are insufficient for worst-case scenarios or future operations.",
        counter_arguments=[
            "Design includes safety factors per API.",
            "Corrosion and wear allowances are incorporated.",
            "Design validated with FEA and field data."
        ],
        resolution_strategy="Peer review and third-party verification of design calculations.",
        entity_scope="CT String Design for DRL14",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 5C7 Section 4"
    ),
    DoctrineBlock(
        topic="Downhole Motor Selection for CTD - PDM Sizing",
        keywords=["downhole motor", "positive displacement motor", "PDM", "coiled tubing drilling", "motor selection", "torque", "flow rate"],
        conclusion_template="The PDM is sized to deliver required torque and RPM at available flow rates, matching bit and formation requirements for CTD operations.",
        reasoning_framework="""
Downhole motor selection for CTD involves:
1. Identifying bit type and size, and corresponding torque and RPM requirements.
2. Reviewing available surface pump rates and pressures.
3. Selecting a PDM with compatible flow rate, pressure drop, and torque output.
4. Ensuring motor OD fits within CT and BHA constraints.
5. Considering temperature, drilling fluid compatibility, and expected motor life.
6. Factoring in operational contingencies (e.g., debris tolerance, stall resistance).
7. Consulting manufacturer performance charts.
8. Validating selection with field experience and post-job analysis.
""",
        key_factors=[
            "Bit torque and RPM requirements",
            "Available flow rate and pressure",
            "Motor OD and length",
            "Drilling fluid compatibility",
            "Formation characteristics"
        ],
        primary_authority=[
            "Motor Manufacturer Performance Charts",
            "ICoTA Motor Selection Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Selected motor cannot deliver required torque or fails prematurely.",
        counter_arguments=[
            "Selection based on validated performance charts.",
            "Contingency motors available on location.",
            "Motor performance monitored in real time."
        ],
        resolution_strategy="Pre-job simulation and post-job performance review.",
        entity_scope="CTD Operations in DRL14",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ICoTA Motor Selection Guidelines"
    ),
    DoctrineBlock(
        topic="Weight Transfer in Horizontal CTD - Friction and Buckling",
        keywords=["weight transfer", "horizontal well", "coiled tubing", "friction", "buckling", "lockup", "drilling"],
        conclusion_template="Effective weight transfer in horizontal CTD is managed by modeling friction and buckling, ensuring WOB is delivered to the bit without exceeding lockup limits.",
        reasoning_framework="""
Weight transfer in horizontal CTD is challenged by friction and helical/sinusoidal buckling. The doctrine involves:
1. Modeling friction forces using Lubinski's equations and field friction factors.
2. Calculating critical buckling loads and lockup length.
3. Monitoring WOB at surface and inferring downhole WOB via models and MWD data.
4. Optimizing CT OD, wall thickness, and lubricity to reduce friction.
5. Using friction reducers or lubricants in the drilling fluid.
6. Limiting horizontal reach based on lockup predictions.
7. Validating models with downhole sensor data.
8. Adjusting operational parameters (e.g., flow rate, CT movement) to optimize weight transfer.
""",
        key_factors=[
            "Friction factor",
            "CT OD and wall thickness",
            "Wellbore trajectory",
            "Drilling fluid properties",
            "Surface and downhole WOB"
        ],
        primary_authority=[
            "Lubinski Buckling Theory",
            "API RP 5C7",
            "ICoTA Best Practices"
        ],
        burden_holder="CTD Operations Engineer",
        adversary_position="WOB at bit is insufficient due to underestimating friction or buckling.",
        counter_arguments=[
            "Model validated with MWD data.",
            "Friction factors updated with field measurements.",
            "Operational adjustments made in real time."
        ],
        resolution_strategy="Continuous model validation and operational optimization.",
        entity_scope="Horizontal CTD in DRL14",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="Lubinski Buckling Theory"
    ),
    DoctrineBlock(
        topic="CT Drilling BHA Design - Orienting Tool, MWD, Check Valve",
        keywords=["BHA design", "coiled tubing drilling", "orienting tool", "MWD", "check valve", "bottom hole assembly"],
        conclusion_template="The CTD BHA incorporates orienting tools, MWD, and check valves to enable directional control, real-time data, and well control integrity.",
        reasoning_framework="""
CTD BHA design is structured to:
1. Include an orienting tool for slide drilling and directional control.
2. Integrate MWD for real-time inclination, azimuth, and toolface data.
3. Install a check valve to prevent backflow and maintain well control.
4. Sequence components to minimize BHA length and maximize tool compatibility.
5. Ensure all components are rated for anticipated pressures, temperatures, and flow rates.
6. Validate signal transmission (mud pulse or EM) through CT.
7. Consider redundancy for critical components.
8. Review with directional drilling and well control specialists.
""",
        key_factors=[
            "Directional control requirements",
            "MWD compatibility",
            "Check valve rating",
            "BHA length and OD",
            "Signal transmission"
        ],
        primary_authority=[
            "ICoTA BHA Design Guidelines",
            "MWD Manufacturer Specifications"
        ],
        burden_holder="BHA Design Engineer",
        adversary_position="BHA lacks necessary tools for directional control or well control.",
        counter_arguments=[
            "BHA design reviewed by multidisciplinary team.",
            "Redundancy and contingency tools included.",
            "All components rated for operational envelope."
        ],
        resolution_strategy="Design review and pre-job BHA testing.",
        entity_scope="CTD BHA for DRL14",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ICoTA BHA Design Guidelines"
    ),
    DoctrineBlock(
        topic="CT Milling Operations - Window Milling and Junk Milling",
        keywords=["coiled tubing", "milling", "window milling", "junk milling", "BHA", "debris management"],
        conclusion_template="CT milling operations employ specialized BHA and debris management to safely mill windows and remove junk, ensuring wellbore integrity.",
        reasoning_framework="""
CT milling operations require:
1. Selecting mill type (window, junk, or pilot) based on target.
2. Designing BHA for optimal weight transfer and debris bypass.
3. Monitoring torque and vibration to prevent BHA failure.
4. Using fluid circulation to remove cuttings and debris.
5. Implementing real-time monitoring for motor stalls or overtorque.
6. Planning contingency for stuck BHA or excessive debris.
7. Validating operation with post-mill caliper or imaging logs.
8. Reviewing lessons learned for future optimization.
""",
        key_factors=[
            "Mill type and size",
            "Debris management",
            "BHA torque and vibration",
            "Fluid circulation rate",
            "Contingency planning"
        ],
        primary_authority=[
            "ICoTA Milling Guidelines",
            "Mill Manufacturer Specifications"
        ],
        burden_holder="CTD Operations Supervisor",
        adversary_position="Milling operation risks stuck BHA or incomplete debris removal.",
        counter_arguments=[
            "BHA includes anti-stall and debris bypass features.",
            "Real-time monitoring mitigates risk.",
            "Contingency plans in place."
        ],
        resolution_strategy="Pre-job risk assessment and post-job review.",
        entity_scope="CT Milling in DRL14",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ICoTA Milling Guidelines"
    ),
    DoctrineBlock(
        topic="CT Acid Stimulation - Matrix Acidizing via CT",
        keywords=["acid stimulation", "matrix acidizing", "coiled tubing", "stimulation design", "zonal isolation"],
        conclusion_template="Matrix acidizing via CT is designed to optimize acid placement, minimize corrosion, and ensure zonal isolation for effective stimulation.",
        reasoning_framework="""
Matrix acidizing with CT involves:
1. Selecting acid type and concentration based on formation mineralogy.
2. Designing CT deployment for precise acid placement.
3. Using diverters or packers for zonal isolation.
4. Incorporating corrosion inhibitors and monitoring returns.
5. Modeling acid penetration and reaction kinetics.
6. Monitoring pressure and temperature during treatment.
7. Flushing and neutralizing post-treatment.
8. Validating effectiveness with production logs or tracer surveys.
""",
        key_factors=[
            "Formation mineralogy",
            "Acid type and volume",
            "Zonal isolation method",
            "Corrosion inhibition",
            "Treatment monitoring"
        ],
        primary_authority=[
            "SPE Acidizing Guidelines",
            "NACE MR0175"
        ],
        burden_holder="Stimulation Engineer",
        adversary_position="Acid placement is ineffective or causes excessive corrosion.",
        counter_arguments=[
            "Design validated with modeling and field experience.",
            "Corrosion inhibitors and monitoring are standard.",
            "Post-treatment evaluation confirms effectiveness."
        ],
        resolution_strategy="Pre-job simulation and post-job production analysis.",
        entity_scope="CT Acid Stimulation in DRL14",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="SPE Acidizing Guidelines"
    ),
    DoctrineBlock(
        topic="CT Nitrogen Kickoff - Gas Lift Unloading",
        keywords=["nitrogen kickoff", "gas lift", "unloading", "coiled tubing", "well cleanup"],
        conclusion_template="Nitrogen kickoff via CT is executed to unload completion fluids and initiate flow, following safety and operational protocols.",
        reasoning_framework="""
CT nitrogen kickoff involves:
1. Calculating required nitrogen volume and rate for effective unloading.
2. Deploying CT to target depth for optimal gas placement.
3. Monitoring wellhead pressure, flowback, and fluid returns.
4. Coordinating with surface nitrogen supply and pressure control.
5. Implementing safety protocols for high-pressure gas handling.
6. Adjusting injection parameters based on real-time response.
7. Flushing CT post-operation to prevent hydrate or corrosion.
8. Documenting operation and reviewing for lessons learned.
""",
        key_factors=[
            "Required nitrogen volume and rate",
            "Target depth for injection",
            "Wellhead pressure monitoring",
            "Safety protocols",
            "Fluid returns"
        ],
        primary_authority=[
            "ICoTA Nitrogen Kickoff Guidelines",
            "API RP 17A"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Nitrogen kickoff fails to unload well or causes safety incident.",
        counter_arguments=[
            "Operation planned with validated models.",
            "Safety protocols strictly enforced.",
            "Contingency plans for well control."
        ],
        resolution_strategy="Pre-job safety review and real-time monitoring.",
        entity_scope="CT Nitrogen Kickoff in DRL14",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="ICoTA Nitrogen Kickoff Guidelines"
    ),
    DoctrineBlock(
        topic="CT Cleanout Operations - Sand and Debris Removal",
        keywords=["cleanout", "sand removal", "debris removal", "coiled tubing", "well intervention"],
        conclusion_template="CT cleanout operations are designed to maximize debris removal efficiency while minimizing risk of stuck pipe and well control incidents.",
        reasoning_framework="""
CT cleanout involves:
1. Selecting appropriate BHA (e.g., jetting nozzle, venturi, or bailer).
2. Calculating optimal pump rate and fluid properties for debris transport.
3. Monitoring surface and downhole pressures to avoid well control issues.
4. Using real-time returns monitoring to assess cleanout progress.
5. Planning for staged cleanout if debris volume is high.
6. Flushing CT and BHA post-operation.
7. Validating cleanout with post-job logs or imaging.
8. Reviewing operation for continuous improvement.
""",
        key_factors=[
            "BHA selection",
            "Pump rate and fluid properties",
            "Debris volume",
            "Pressure monitoring",
            "Returns monitoring"
        ],
        primary_authority=[
            "ICoTA Cleanout Guidelines",
            "API RP 5C7"
        ],
        burden_holder="CT Operations Supervisor",
        adversary_position="Cleanout is incomplete or causes stuck CT.",
        counter_arguments=[
            "Operation monitored in real time.",
            "Contingency plans for stuck pipe.",
            "Post-job validation performed."
        ],
        resolution_strategy="Continuous monitoring and staged cleanout as needed.",
        entity_scope="CT Cleanout in DRL14",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ICoTA Cleanout Guidelines"
    ),
    DoctrineBlock(
        topic="CT Real-Time Monitoring - WHP, Pump Pressure, Weight",
        keywords=["real-time monitoring", "wellhead pressure", "pump pressure", "weight", "coiled tubing", "data acquisition"],
        conclusion_template="Real-time monitoring of WHP, pump pressure, and CT weight is mandatory for safe and efficient CT operations.",
        reasoning_framework="""
Real-time monitoring is implemented by:
1. Installing calibrated sensors for WHP, pump pressure, and CT weight.
2. Streaming data to surface displays and logging systems.
3. Setting alarm thresholds for abnormal conditions.
4. Integrating data with fatigue and lockup models.
5. Training personnel in data interpretation and response protocols.
6. Archiving data for post-job analysis and regulatory compliance.
7. Validating sensor calibration before and after operations.
8. Reviewing data integrity and redundancy.
""",
        key_factors=[
            "Sensor calibration",
            "Data acquisition system",
            "Alarm thresholds",
            "Personnel training",
            "Data archiving"
        ],
        primary_authority=[
            "API RP 5C7",
            "ICoTA Monitoring Guidelines"
        ],
        burden_holder="CT Supervisor",
        adversary_position="Lack of real-time monitoring increases operational risk.",
        counter_arguments=[
            "Monitoring is standard operating procedure.",
            "Alarm thresholds and response protocols in place.",
            "Data archived for review."
        ],
        resolution_strategy="Routine system checks and personnel training.",
        entity_scope="CT Operations in DRL14",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="API RP 5C7 Section 8"
    ),
    DoctrineBlock(
        topic="CT Reel Management and Inspection - ICoTA Guidelines",
        keywords=["reel management", "inspection", "coiled tubing", "ICoTA", "maintenance", "NDT"],
        conclusion_template="CT reel management and inspection follow ICoTA guidelines, including NDT, visual checks, and documentation for integrity assurance.",
        reasoning_framework="""
CT reel management includes:
1. Scheduling routine visual and NDT inspections per ICoTA guidelines.
2. Documenting reel and CT string history (cycles, repairs, incidents).
3. Inspecting for mechanical damage, corrosion, and weld integrity.
4. Recording and tracking fatigue cycles for each string segment.
5. Implementing corrective actions for detected anomalies.
6. Archiving inspection records for regulatory and operational review.
7. Training personnel in inspection procedures.
8. Reviewing inspection results in pre-job risk assessments.
""",
        key_factors=[
            "Inspection frequency",
            "NDT method",
            "Documentation",
            "Personnel training",
            "Corrective actions"
        ],
        primary_authority=[
            "ICoTA Reel Management Guidelines",
            "API RP 5C7"
        ],
        burden_holder="CT Maintenance Supervisor",
        adversary_position="Inspections are insufficient or poorly documented, risking CT failure.",
        counter_arguments=[
            "ICoTA guidelines strictly followed.",
            "Inspection records maintained and audited.",
            "Corrective actions tracked to closure."
        ],
        resolution_strategy="Routine audits and personnel certification.",
        entity_scope="CT Reel Management in DRL14",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ICoTA Reel Management Guidelines"
    ),
    DoctrineBlock(
        topic="CT Connector and Dimple Technology",
        keywords=["connector", "dimple", "coiled tubing", "makeup", "pressure integrity", "mechanical strength"],
        conclusion_template="CT connectors and dimples are selected and installed per manufacturer and ICoTA guidelines to ensure pressure integrity and mechanical strength.",
        reasoning_framework="""
Connector and dimple technology for CT involves:
1. Selecting connector type based on pressure rating, OD, and operational requirements.
2. Installing connectors using manufacturer-approved procedures.
3. Verifying dimple placement and quality with NDT or visual inspection.
4. Pressure testing assembled connectors before deployment.
5. Documenting connector installation and test results.
6. Training personnel in connector technology and installation.
7. Reviewing connector performance post-job.
8. Updating connector inventory and maintenance records.
""",
        key_factors=[
            "Connector type and rating",
            "Installation procedure",
            "Dimple quality",
            "Pressure testing",
            "Documentation"
        ],
        primary_authority=[
            "Connector Manufacturer Specifications",
            "ICoTA Connector Guidelines"
        ],
        burden_holder="CT Maintenance Technician",
        adversary_position="Connectors or dimples fail under pressure or load.",
        counter_arguments=[
            "Installation and testing per guidelines.",
            "Personnel trained and certified.",
            "Performance reviewed post-job."
        ],
        resolution_strategy="Routine testing and personnel certification.",
        entity_scope="CT Connectors in DRL14",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ICoTA Connector Guidelines"
    ),
    DoctrineBlock(
        topic="CT Well Intervention in Horizontal Wells - Extended Reach",
        keywords=["well intervention", "horizontal well", "extended reach", "coiled tubing", "lockup", "friction"],
        conclusion_template="CT well interventions in extended reach horizontals are planned with lockup modeling, friction reduction, and staged operations to maximize reach.",
        reasoning_framework="""
Extended reach CT interventions require:
1. Modeling lockup limits using well trajectory and CT properties.
2. Selecting CT OD and wall thickness for optimal reach.
3. Using friction reducers and lubricants in the fluid system.
4. Planning staged interventions with intermediate wiper trips as needed.
5. Monitoring downhole and surface parameters for early lockup detection.
6. Adjusting operational parameters in real time.
7. Validating reach with post-job logs.
8. Reviewing lessons learned for future interventions.
""",
        key_factors=[
            "Lockup modeling",
            "CT OD and wall thickness",
            "Friction reduction",
            "Staged operations",
            "Monitoring"
        ],
        primary_authority=[
            "ICoTA Extended Reach Guidelines",
            "API RP 5C7"
        ],
        burden_holder="CT Intervention Engineer",
        adversary_position="Lockup occurs before target depth, limiting intervention effectiveness.",
        counter_arguments=[
            "Lockup modeling validated with field data.",
            "Friction reducers and staged operations mitigate risk.",
            "Contingency plans in place."
        ],
        resolution_strategy="Pre-job modeling and real-time operational adjustments.",
        entity_scope="CT Interventions in DRL14",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ICoTA Extended Reach Guidelines"
    ),
    DoctrineBlock(
        topic="CT Drilling Rate of Penetration - ROP Optimization",
        keywords=["rate of penetration", "ROP", "optimization", "coiled tubing drilling", "drilling parameters"],
        conclusion_template="ROP in CT drilling is optimized by balancing WOB, RPM, and hydraulics, considering CT limits and formation response.",
        reasoning_framework="""
ROP optimization involves:
1. Monitoring WOB, RPM, and hydraulic parameters in real time.
2. Adjusting drilling parameters to maximize ROP without exceeding CT or BHA limits.
3. Analyzing formation response and bit wear.
4. Using MWD data to correlate drilling parameters with ROP.
5. Implementing best practices for slide drilling and motor operation.
6. Reviewing post-job data for continuous improvement.
7. Training personnel in ROP optimization techniques.
8. Updating drilling programs based on field results.
""",
        key_factors=[
            "WOB",
            "RPM",
            "Hydraulics",
            "Formation type",
            "Bit wear"
        ],
        primary_authority=[
            "ICoTA Drilling Guidelines",
            "Bit Manufacturer Recommendations"
        ],
        burden_holder="Drilling Supervisor",
        adversary_position="ROP is suboptimal due to conservative parameters or poor optimization.",
        counter_arguments=[
            "Parameters adjusted in real time.",
            "Post-job analysis for continuous improvement.",
            "Personnel trained in ROP optimization."
        ],
        resolution_strategy="Continuous monitoring and parameter adjustment.",
        entity_scope="CT Drilling in DRL14",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ICoTA Drilling Guidelines"
    ),
    DoctrineBlock(
        topic="CT Drilling Fluid Selection - Drilling Mud Properties",
        keywords=["drilling fluid", "mud properties", "coiled tubing drilling", "fluid selection", "hydraulics"],
        conclusion_template="Drilling fluid for CTD is selected to optimize hole cleaning, minimize friction, and ensure CT and formation compatibility.",
        reasoning_framework="""
Drilling fluid selection involves:
1. Assessing formation properties and anticipated cuttings load.
2. Selecting fluid type (water-based, oil-based, or specialty) for compatibility.
3. Optimizing viscosity and density for hole cleaning and pressure control.
4. Adding lubricants or friction reducers as needed.
5. Monitoring fluid properties in real time.
6. Ensuring fluid is compatible with CT material and BHA components.
7. Planning for fluid disposal or recycling.
8. Validating performance with post-job analysis.
""",
        key_factors=[
            "Formation compatibility",
            "Cuttings load",
            "Viscosity and density",
            "Lubricity",
            "CT and BHA compatibility"
        ],
        primary_authority=[
            "ICoTA Fluid Selection Guidelines",
            "API RP 13B"
        ],
        burden_holder="Drilling Fluids Engineer",
        adversary_position="Fluid selection leads to poor hole cleaning or CT/BHA damage.",
        counter_arguments=[
            "Fluid properties monitored and adjusted in real time.",
            "Compatibility validated with lab testing.",
            "Contingency fluids available."
        ],
        resolution_strategy="Continuous monitoring and post-job fluid analysis.",
        entity_scope="CTD Fluid Selection in DRL14",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="ICoTA Fluid Selection Guidelines"
    ),
    DoctrineBlock(
        topic="CT Drilling Directional Control - Slide Drilling with Bent Motor",
        keywords=["directional control", "slide drilling", "bent motor", "coiled tubing drilling", "BHA"],
        conclusion_template="Directional control in CTD is achieved by slide drilling with a bent motor, using MWD data for toolface orientation and trajectory correction.",
        reasoning_framework="""
Directional control doctrine:
1. Incorporate a bent motor in the BHA for slide drilling.
2. Use MWD data for real-time toolface and inclination monitoring.
3. Plan slide/rotate sequences for trajectory correction.
4. Monitor torque and drag to avoid excessive CT stress.
5. Validate directional response with post-job surveys.
6. Train personnel in slide drilling techniques.
7. Review BHA and motor performance after each run.
8. Update directional plan based on field results.
""",
        key_factors=[
            "Bent motor configuration",
            "MWD toolface data",
            "Slide/rotate sequence",
            "Torque and drag monitoring",
            "Personnel training"
        ],
        primary_authority=[
            "ICoTA Directional Drilling Guidelines",
            "MWD Manufacturer Recommendations"
        ],
        burden_holder="Directional Driller",
        adversary_position="Directional control is lost due to poor toolface monitoring or BHA design.",
        counter_arguments=[
            "MWD data validated in real time.",
            "Personnel trained in slide drilling.",
            "BHA design reviewed by experts."
        ],
        resolution_strategy="Continuous monitoring and post-job review.",
        entity_scope="CTD Directional Control in DRL14",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ICoTA Directional Drilling Guidelines"
    ),
    DoctrineBlock(
        topic="CT Drilling Well Control - Kick Detection and Response",
        keywords=["well control", "kick detection", "coiled tubing drilling", "pressure monitoring", "response protocol"],
        conclusion_template="Well control in CTD is maintained by continuous pressure monitoring, rapid kick detection, and pre-defined response protocols.",
        reasoning_framework="""
Well control doctrine:
1. Install and calibrate pressure sensors at surface and downhole.
2. Monitor for abnormal pressure trends indicating influx.
3. Train personnel in kick detection and response.
4. Maintain BOPs and check valves in ready condition.
5. Pre-define response protocols for various kick scenarios.
6. Conduct regular well control drills.
7. Document all well control events and responses.
8. Review and update protocols based on lessons learned.
""",
        key_factors=[
            "Pressure monitoring",
            "Sensor calibration",
            "Personnel training",
            "BOP and check valve readiness",
            "Response protocols"
        ],
        primary_authority=[
            "API RP 53",
            "ICoTA Well Control Guidelines"
        ],
        burden_holder="CTD Supervisor",
        adversary_position="Kick is not detected or response is delayed, risking blowout.",
        counter_arguments=[
            "Continuous monitoring and drills.",
            "Redundant sensors and alarms.",
            "Protocols reviewed and updated regularly."
        ],
        resolution_strategy="Routine drills and post-event analysis.",
        entity_scope="CTD Well Control in DRL14",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="API RP 53"
    ),
    # --- Additional doctrines for a total of 40+ ---
    DoctrineBlock(
        topic="CT String Corrosion Management",
        keywords=["corrosion", "coiled tubing", "corrosion inhibitor", "inspection", "material selection"],
        conclusion_template="Corrosion management for CT strings involves inhibitor use, material selection, and periodic inspection to extend service life.",
        reasoning_framework="""
Corrosion management steps:
1. Assess corrosivity of fluids and gases encountered.
2. Select CT material (e.g., low-alloy steel, CRA) for environment.
3. Inject corrosion inhibitors during operations.
4. Schedule periodic NDT and visual inspections for corrosion.
5. Document and track corrosion rates and mitigation actions.
6. Replace or repair CT segments as needed.
7. Review effectiveness of inhibitors and update selection.
8. Train personnel in corrosion management procedures.
""",
        key_factors=[
            "Fluid and gas corrosivity",
            "Material selection",
            "Inhibitor type and dosage",
            "Inspection frequency",
            "Documentation"
        ],
        primary_authority=[
            "NACE MR0175",
            "ICoTA Corrosion Guidelines"
        ],
        burden_holder="CT Maintenance Supervisor",
        adversary_position="Corrosion is underestimated, leading to premature CT failure.",
        counter_arguments=[
            "Inhibitor effectiveness validated by inspection data.",
            "Material selection based on environment.",
            "Corrosion rates tracked and reviewed."
        ],
        resolution_strategy="Routine inspection and inhibitor optimization.",
        entity_scope="CT Strings in DRL14",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="NACE MR0175"
    ),
    DoctrineBlock(
        topic="CT String Fatigue Tracking - Digital Logging",
        keywords=["fatigue tracking", "digital logging", "coiled tubing", "cycle count", "life prediction"],
        conclusion_template="Digital logging systems are used to track CT fatigue cycles, supporting accurate life prediction and risk management.",
        reasoning_framework="""
Fatigue tracking doctrine:
1. Install digital logging system to record CT movement and cycles.
2. Integrate with fatigue models for real-time life prediction.
3. Archive cycle data for each CT string segment.
4. Use data for maintenance planning and risk assessment.
5. Validate digital logs with periodic manual checks.
6. Update models based on field experience.
7. Train personnel in system operation and interpretation.
8. Review logs in pre-job risk assessments.
""",
        key_factors=[
            "Digital logging system",
            "Model integration",
            "Data archiving",
            "Manual validation",
            "Personnel training"
        ],
        primary_authority=[
            "ICoTA Fatigue Tracking Guidelines",
            "API RP 5C7"
        ],
        burden_holder="CT Operations Supervisor",
        adversary_position="Digital logs are incomplete or inaccurate, risking CT failure.",
        counter_arguments=[
            "Logs validated with manual checks.",
            "System maintained and updated.",
            "Personnel trained in use and interpretation."
        ],
        resolution_strategy="Routine system checks and data validation.",
        entity_scope="CT Operations in DRL14",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ICoTA Fatigue Tracking Guidelines"
    ),
    DoctrineBlock(
        topic="CT String Weld Management",
        keywords=["weld management", "coiled tubing", "weld inspection", "NDT", "fatigue"],
        conclusion_template="CT string welds are managed by NDT inspection, documentation, and operational limits to minimize fatigue risk.",
        reasoning_framework="""
Weld management steps:
1. Identify all weld locations in CT string.
2. Perform NDT (e.g., ultrasonic, radiographic) on all welds.
3. Document weld quality and repair history.
4. Apply operational limits (e.g., reduced fatigue cycles) at welds.
5. Monitor welds during periodic inspections.
6. Replace or repair welds with detected anomalies.
7. Train personnel in weld management procedures.
8. Review weld performance post-job.
""",
        key_factors=[
            "Weld location and quality",
            "NDT method",
            "Documentation",
            "Operational limits",
            "Personnel training"
        ],
        primary_authority=[
            "API RP 5C7",
            "ICoTA Weld Management Guidelines"
        ],
        burden_holder="CT Maintenance Supervisor",
        adversary_position="Welds are weak points leading to premature failure.",
        counter_arguments=[
            "NDT and documentation ensure weld integrity.",
            "Operational limits applied at welds.",
            "Welds monitored and replaced as needed."
        ],
        resolution_strategy="Routine NDT and documentation review.",
        entity_scope="CT Strings in DRL14",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 5C7 Section 6"
    ),
    DoctrineBlock(
        topic="CT String Pressure Testing",
        keywords=["pressure testing", "coiled tubing", "integrity", "hydrotest", "leak detection"],
        conclusion_template="CT strings are pressure tested before deployment to verify integrity and detect leaks, per API and ICoTA guidelines.",
        reasoning_framework="""
Pressure testing doctrine:
1. Conduct hydrostatic pressure test to at least 1.25x maximum anticipated pressure.
2. Monitor for pressure loss over specified hold period.
3. Document test parameters and results.
4. Repair or replace CT segments failing test.
5. Train personnel in pressure testing procedures.
6. Archive test records for regulatory compliance.
7. Review test results in pre-job risk assessments.
8. Update testing procedures based on lessons learned.
""",
        key_factors=[
            "Test pressure and hold time",
            "Leak detection",
            "Documentation",
            "Personnel training",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 5C7",
            "ICoTA Pressure Testing Guidelines"
        ],
        burden_holder="CT Maintenance Technician",
        adversary_position="Leaks or weak points are missed, risking failure.",
        counter_arguments=[
            "Test procedures validated by API and ICoTA.",
            "Personnel trained and certified.",
            "Records maintained and reviewed."
        ],
        resolution_strategy="Routine audits and procedure updates.",
        entity_scope="CT Strings in DRL14",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 5C7 Section 5"
    ),
    DoctrineBlock(
        topic="CT BHA Vibration Management",
        keywords=["BHA vibration", "coiled tubing", "vibration monitoring", "motor failure", "BHA design"],
        conclusion_template="BHA vibration is managed through design optimization, real-time monitoring, and operational adjustments to prevent tool failure.",
        reasoning_framework="""
Vibration management steps:
1. Design BHA to minimize resonance and vibration transmission.
2. Install vibration sensors in BHA or use MWD vibration data.
3. Monitor vibration in real time and adjust drilling parameters.
4. Replace or service BHA components showing excessive vibration.
5. Train personnel in vibration management.
6. Review vibration data post-job for continuous improvement.
7. Update BHA design based on field experience.
8. Document vibration incidents and responses.
""",
        key_factors=[
            "BHA design",
            "Vibration monitoring",
            "Operational adjustments",
            "Personnel training",
            "Documentation"
        ],
        primary_authority=[
            "ICoTA BHA Vibration Guidelines",
            "Motor Manufacturer Recommendations"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Excessive vibration leads to premature tool failure.",
        counter_arguments=[
            "Design and monitoring minimize vibration risk.",
            "Operational adjustments made in real time.",
            "Incidents documented and reviewed."
        ],
        resolution_strategy="Continuous monitoring and design updates.",
        entity_scope="CTD BHA in DRL14",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ICoTA BHA Vibration Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Bit Selection and Compatibility",
        keywords=["bit selection", "coiled tubing drilling", "bit compatibility", "formation", "motor"],
        conclusion_template="Bit selection for CTD is based on formation type, motor compatibility, and operational objectives, validated by field experience.",
        reasoning_framework="""
Bit selection doctrine:
1. Analyze formation properties and anticipated lithology.
2. Select bit type (PDC, tricone, etc.) for formation and motor compatibility.
3. Review bit size for BHA and CT constraints.
4. Validate bit performance with field data and manufacturer recommendations.
5. Monitor bit wear and ROP during operation.
6. Plan for contingency bits if needed.
7. Train personnel in bit selection and handling.
8. Review bit performance post-job.
""",
        key_factors=[
            "Formation type",
            "Bit type and size",
            "Motor compatibility",
            "BHA and CT constraints",
            "Field experience"
        ],
        primary_authority=[
            "Bit Manufacturer Recommendations",
            "ICoTA Bit Selection Guidelines"
        ],
        burden_holder="Drilling Engineer",
        adversary_position="Bit selection is suboptimal for formation or motor.",
        counter_arguments=[
            "Selection based on formation analysis and field data.",
            "Contingency bits available.",
            "Performance reviewed post-job."
        ],
        resolution_strategy="Pre-job analysis and post-job review.",
        entity_scope="CTD Bit Selection in DRL14",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ICoTA Bit Selection Guidelines"
    ),
    DoctrineBlock(
        topic="CTD MWD Tool Reliability",
        keywords=["MWD", "tool reliability", "coiled tubing drilling", "signal transmission", "maintenance"],
        conclusion_template="MWD tool reliability is ensured by pre-job testing, maintenance, and signal validation during CTD operations.",
        reasoning_framework="""
MWD reliability steps:
1. Conduct pre-job functional and signal transmission tests.
2. Maintain MWD tools per manufacturer schedule.
3. Monitor signal quality and data integrity in real time.
4. Replace or repair tools showing anomalies.
5. Train personnel in MWD operation and troubleshooting.
6. Archive MWD data for post-job analysis.
7. Review tool performance after each run.
8. Update maintenance procedures based on field experience.
""",
        key_factors=[
            "Pre-job testing",
            "Signal transmission",
            "Maintenance schedule",
            "Personnel training",
            "Data archiving"
        ],
        primary_authority=[
            "MWD Manufacturer Guidelines",
            "ICoTA MWD Best Practices"
        ],
        burden_holder="MWD Technician",
        adversary_position="MWD tool fails or provides unreliable data.",
        counter_arguments=[
            "Pre-job testing and maintenance minimize risk.",
            "Personnel trained in troubleshooting.",
            "Performance reviewed post-job."
        ],
        resolution_strategy="Routine testing and maintenance.",
        entity_scope="CTD MWD Tools in DRL14",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="MWD Manufacturer Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Wellbore Cleanliness - Pre- and Post-Drilling",
        keywords=["wellbore cleanliness", "pre-drilling", "post-drilling", "coiled tubing", "debris management"],
        conclusion_template="Wellbore cleanliness is ensured by pre- and post-drilling cleanout runs, debris monitoring, and validation with logs.",
        reasoning_framework="""
Cleanliness doctrine:
1. Conduct pre-drilling cleanout to remove debris and scale.
2. Monitor debris returns during drilling.
3. Plan post-drilling cleanout to ensure wellbore is free of cuttings and debris.
4. Validate cleanliness with caliper or imaging logs.
5. Document cleanout procedures and results.
6. Train personnel in cleanout operations.
7. Review effectiveness post-job.
8. Update procedures based on lessons learned.
""",
        key_factors=[
            "Cleanout runs",
            "Debris monitoring",
            "Validation logs",
            "Documentation",
            "Personnel training"
        ],
        primary_authority=[
            "ICoTA Cleanout Guidelines",
            "API RP 5C7"
        ],
        burden_holder="CT Operations Supervisor",
        adversary_position="Residual debris impairs subsequent operations.",
        counter_arguments=[
            "Cleanout validated with logs.",
            "Procedures updated based on results.",
            "Personnel trained in cleanout."
        ],
        resolution_strategy="Routine validation and procedure updates.",
        entity_scope="CTD Wellbore Cleanliness in DRL14",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ICoTA Cleanout Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Fluid Loss Control",
        keywords=["fluid loss", "control", "coiled tubing drilling", "lost circulation", "LCM"],
        conclusion_template="Fluid loss during CTD is managed by LCM addition, real-time monitoring, and contingency planning.",
        reasoning_framework="""
Fluid loss control steps:
1. Monitor fluid returns and losses in real time.
2. Add LCM (e.g., fibers, particulates) as needed.
3. Adjust drilling parameters to minimize losses.
4. Plan for contingency plugs or squeezes.
5. Document fluid loss events and responses.
6. Train personnel in fluid loss management.
7. Review effectiveness post-job.
8. Update fluid loss procedures based on experience.
""",
        key_factors=[
            "Real-time monitoring",
            "LCM selection",
            "Parameter adjustment",
            "Contingency planning",
            "Documentation"
        ],
        primary_authority=[
            "ICoTA Fluid Loss Guidelines",
            "API RP 13B"
        ],
        burden_holder="Drilling Fluids Engineer",
        adversary_position="Fluid loss leads to well control issues or formation damage.",
        counter_arguments=[
            "Real-time monitoring and LCM minimize risk.",
            "Contingency plans in place.",
            "Procedures updated based on results."
        ],
        resolution_strategy="Continuous monitoring and post-job review.",
        entity_scope="CTD Fluid Loss Control in DRL14",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="ICoTA Fluid Loss Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Stuck Pipe Prevention and Recovery",
        keywords=["stuck pipe", "prevention", "recovery", "coiled tubing drilling", "contingency"],
        conclusion_template="Stuck pipe risk is minimized by monitoring, BHA design, and contingency planning for recovery.",
        reasoning_framework="""
Stuck pipe doctrine:
1. Monitor torque, drag, and fluid returns for early stuck pipe indicators.
2. Design BHA for debris bypass and jarring capability.
3. Plan for contingency jars or fishing tools.
4. Train personnel in stuck pipe prevention and recovery.
5. Document stuck pipe events and responses.
6. Review effectiveness post-job.
7. Update procedures based on lessons learned.
8. Validate BHA design with field experience.
""",
        key_factors=[
            "Monitoring",
            "BHA design",
            "Contingency tools",
            "Personnel training",
            "Documentation"
        ],
        primary_authority=[
            "ICoTA Stuck Pipe Guidelines",
            "API RP 5C7"
        ],
        burden_holder="CTD Operations Supervisor",
        adversary_position="Stuck pipe event leads to lost time or equipment.",
        counter_arguments=[
            "Monitoring and BHA design minimize risk.",
            "Contingency tools available.",
            "Procedures updated based on results."
        ],
        resolution_strategy="Routine review and personnel training.",
        entity_scope="CTD Stuck Pipe Prevention in DRL14",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="ICoTA Stuck Pipe Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Annular Pressure Management",
        keywords=["annular pressure", "management", "coiled tubing drilling", "well control", "pressure monitoring"],
        conclusion_template="Annular pressure is managed by real-time monitoring, fluid selection, and operational adjustments to maintain well control.",
        reasoning_framework="""
Annular pressure management steps:
1. Install sensors for real-time annular pressure monitoring.
2. Select fluid density and rheology for pressure control.
3. Adjust pump rates and CT movement as needed.
4. Train personnel in pressure management.
5. Document pressure excursions and responses.
6. Review effectiveness post-job.
7. Update procedures based on lessons learned.
8. Validate sensor calibration regularly.
""",
        key_factors=[
            "Real-time monitoring",
            "Fluid properties",
            "Operational adjustments",
            "Personnel training",
            "Documentation"
        ],
        primary_authority=[
            "API RP 53",
            "ICoTA Pressure Management Guidelines"
        ],
        burden_holder="CTD Supervisor",
        adversary_position="Annular pressure excursions lead to well control incidents.",
        counter_arguments=[
            "Real-time monitoring and fluid selection minimize risk.",
            "Personnel trained in pressure management.",
            "Procedures updated based on results."
        ],
        resolution_strategy="Routine monitoring and procedure updates.",
        entity_scope="CTD Annular Pressure Management in DRL14",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 53"
    ),
    DoctrineBlock(
        topic="CTD Surface Equipment Redundancy",
        keywords=["surface equipment", "redundancy", "coiled tubing", "BOP", "pump", "power pack"],
        conclusion_template="Surface equipment redundancy is maintained by backup BOPs, pumps, and power packs to ensure operational continuity and safety.",
        reasoning_framework="""
Redundancy doctrine:
1. Maintain backup BOPs, pumps, and power packs on location.
2. Test redundancy systems before operation.
3. Document equipment readiness and test results.
4. Train personnel in redundancy system operation.
5. Review redundancy effectiveness post-job.
6. Update redundancy plans based on lessons learned.
7. Archive test and maintenance records.
8. Validate redundancy during drills.
""",
        key_factors=[
            "Backup equipment",
            "Testing",
            "Documentation",
            "Personnel training",
            "Maintenance records"
        ],
        primary_authority=[
            "API RP 53",
            "ICoTA Equipment Guidelines"
        ],
        burden_holder="CTD Supervisor",
        adversary_position="Redundancy is inadequate, risking operational delays or safety incidents.",
        counter_arguments=[
            "Redundancy tested before operation.",
            "Personnel trained in backup system use.",
            "Records maintained and reviewed."
        ],
        resolution_strategy="Routine testing and documentation.",
        entity_scope="CTD Surface Equipment in DRL14",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="API RP 53"
    ),
    DoctrineBlock(
        topic="CTD Data Management and Reporting",
        keywords=["data management", "reporting", "coiled tubing drilling", "regulatory compliance", "data archiving"],
        conclusion_template="CTD data is managed and reported per regulatory and company requirements, ensuring traceability and compliance.",
        reasoning_framework="""
Data management doctrine:
1. Archive all operational data (pressure, cycles, logs) in secure systems.
2. Report data per regulatory and company requirements.
3. Validate data integrity and completeness.
4. Train personnel in data management and reporting.
5. Review data for lessons learned and continuous improvement.
6. Update data management procedures as needed.
7. Maintain data security and backup.
8. Audit data management practices regularly.
""",
        key_factors=[
            "Data archiving",
            "Reporting requirements",
            "Data integrity",
            "Personnel training",
            "Auditing"
        ],
        primary_authority=[
            "Company Data Management Policy",
            "Regulatory Requirements"
        ],
        burden_holder="CTD Data Manager",
        adversary_position="Data is incomplete or inaccessible, risking compliance.",
        counter_arguments=[
            "Data archived and audited.",
            "Personnel trained in management and reporting.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Routine audits and personnel training.",
        entity_scope="CTD Data in DRL14",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Company Data Management Policy"
    ),
    DoctrineBlock(
        topic="CTD Environmental Protection and Waste Management",
        keywords=["environmental protection", "waste management", "coiled tubing drilling", "regulatory compliance", "fluid disposal"],
        conclusion_template="Environmental protection is ensured by proper waste management, fluid disposal, and regulatory compliance during CTD operations.",
        reasoning_framework="""
Environmental protection doctrine:
1. Identify all waste streams (fluids, cuttings, chemicals).
2. Dispose of waste per regulatory and company requirements.
3. Monitor for spills and contain immediately.
4. Train personnel in environmental protection procedures.
5. Document waste management actions.
6. Review compliance post-job.
7. Update procedures based on lessons learned.
8. Audit waste management practices regularly.
""",
        key_factors=[
            "Waste identification",
            "Disposal procedures",
            "Spill monitoring",
            "Personnel training",
            "Documentation"
        ],
        primary_authority=[
            "Regulatory Requirements",
            "Company Environmental Policy"
        ],
        burden_holder="CTD Environmental Coordinator",
        adversary_position="Improper waste management leads to environmental incidents.",
        counter_arguments=[
            "Procedures follow regulatory and company requirements.",
            "Personnel trained in environmental protection.",
            "Actions documented and reviewed."
        ],
        resolution_strategy="Routine audits and personnel training.",
        entity_scope="CTD Environmental Protection in DRL14",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Company Environmental Policy"
    ),
    DoctrineBlock(
        topic="CTD Personnel Competency and Certification",
        keywords=["personnel competency", "certification", "coiled tubing drilling", "training", "ICoTA"],
        conclusion_template="Personnel competency is ensured by certification, ongoing training, and competency assessment per ICoTA and company standards.",
        reasoning_framework="""
Competency doctrine:
1. Require ICoTA or equivalent certification for key personnel.
2. Provide ongoing training and competency assessments.
3. Document training and certification records.
4. Review personnel competency before critical operations.
5. Update training programs based on lessons learned.
6. Audit competency records regularly.
7. Train personnel in new technologies and procedures.
8. Maintain records for regulatory compliance.
""",
        key_factors=[
            "Certification",
            "Training",
            "Competency assessment",
            "Documentation",
            "Auditing"
        ],
        primary_authority=[
            "ICoTA Certification Standards",
            "Company Training Policy"
        ],
        burden_holder="CTD Operations Manager",
        adversary_position="Personnel lack required competency, risking safety and performance.",
        counter_arguments=[
            "Certification and training records maintained.",
            "Ongoing assessments performed.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Routine audits and training updates.",
        entity_scope="CTD Personnel in DRL14",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="ICoTA Certification Standards"
    ),
    DoctrineBlock(
        topic="CTD Emergency Response Planning",
        keywords=["emergency response", "planning", "coiled tubing drilling", "contingency", "well control"],
        conclusion_template="Emergency response plans are developed, communicated, and drilled to ensure rapid and effective response to CTD incidents.",
        reasoning_framework="""
Emergency response doctrine:
1. Develop site-specific emergency response plans.
2. Communicate plans to all personnel and stakeholders.
3. Conduct regular emergency drills (well control, fire, evacuation).
4. Document drill results and lessons learned.
5. Update plans based on regulatory changes and incidents.
6. Train personnel in emergency response procedures.
7. Maintain emergency equipment and supplies.
8. Review and audit plans regularly.
""",
        key_factors=[
            "Plan development",
            "Communication",
            "Drills",
            "Documentation",
            "Personnel training"
        ],
        primary_authority=[
            "Regulatory Requirements",
            "Company Emergency Response Policy"
        ],
        burden_holder="CTD Operations Manager",
        adversary_position="Emergency response is inadequate, risking personnel safety.",
        counter_arguments=[
            "Plans developed and communicated.",
            "Drills conducted and documented.",
            "Plans updated as needed."
        ],
        resolution_strategy="Routine drills and plan updates.",
        entity_scope="CTD Emergency Response in DRL14",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="Company Emergency Response Policy"
    ),
    DoctrineBlock(
        topic="CTD Regulatory Compliance and Audit",
        keywords=["regulatory compliance", "audit", "coiled tubing drilling", "documentation", "inspection"],
        conclusion_template="Regulatory compliance is maintained by documentation, periodic audits, and corrective actions for all CTD operations.",
        reasoning_framework="""
Compliance doctrine:
1. Identify applicable regulations for CTD operations.
2. Maintain documentation for all operational activities.
3. Conduct periodic internal and external audits.
4. Implement corrective actions for audit findings.
5. Train personnel in compliance requirements.
6. Archive audit records for regulatory review.
7. Update procedures based on regulatory changes.
8. Review compliance post-job.
""",
        key_factors=[
            "Regulation identification",
            "Documentation",
            "Auditing",
            "Corrective actions",
            "Personnel training"
        ],
        primary_authority=[
            "Regulatory Requirements",
            "Company Compliance Policy"
        ],
        burden_holder="CTD Compliance Officer",
        adversary_position="Non-compliance leads to regulatory penalties or operational shutdown.",
        counter_arguments=[
            "Documentation and audits ensure compliance.",
            "Corrective actions tracked to closure.",
            "Personnel trained in requirements."
        ],
        resolution_strategy="Routine audits and documentation review.",
        entity_scope="CTD Regulatory Compliance in DRL14",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Company Compliance Policy"
    ),
    DoctrineBlock(
        topic="CTD HSE Risk Assessment and Mitigation",
        keywords=["HSE", "risk assessment", "mitigation", "coiled tubing drilling", "safety"],
        conclusion_template="HSE risks are assessed and mitigated through formal risk assessments, controls, and ongoing review during CTD operations.",
        reasoning_framework="""
HSE risk doctrine:
1. Conduct formal risk assessments before each operation.
2. Identify hazards and implement controls.
3. Communicate risks and controls to all personnel.
4. Monitor HSE performance during operations.
5. Document incidents and near-misses.
6. Review and update risk assessments post-job.
7. Train personnel in HSE risk management.
8. Audit HSE performance and controls regularly.
""",
        key_factors=[
            "Risk assessment",
            "Hazard identification",
            "Control implementation",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "Company HSE Policy",
            "Regulatory Requirements"
        ],
        burden_holder="CTD HSE Manager",
        adversary_position="HSE risks are underestimated, leading to incidents.",
        counter_arguments=[
            "Formal assessments and controls implemented.",
            "Performance monitored and reviewed.",
            "Personnel trained in HSE risk management."
        ],
        resolution_strategy="Routine assessments and audits.",
        entity_scope="CTD HSE in DRL14",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="Company HSE Policy"
    ),
    DoctrineBlock(
        topic="CTD Equipment Maintenance and Reliability",
        keywords=["equipment maintenance", "reliability", "coiled tubing drilling", "preventive maintenance", "downtime"],
        conclusion_template="Equipment reliability is ensured by preventive maintenance, documentation, and real-time monitoring during CTD operations.",
        reasoning_framework="""
Maintenance doctrine:
1. Develop preventive maintenance schedule for all equipment.
2. Document maintenance actions and findings.
3. Monitor equipment performance in real time.
4. Replace or repair equipment showing anomalies.
5. Train personnel in maintenance procedures.
6. Review maintenance effectiveness post-job.
7. Update maintenance schedule based on field experience.
8. Audit maintenance records regularly.
""",
        key_factors=[
            "Preventive maintenance",
            "Documentation",
            "Real-time monitoring",
            "Personnel training",
            "Auditing"
        ],
        primary_authority=[
            "Manufacturer Maintenance Guidelines",
            "Company Maintenance Policy"
        ],
        burden_holder="CTD Maintenance Supervisor",
        adversary_position="Maintenance is inadequate, leading to equipment failure.",
        counter_arguments=[
            "Preventive maintenance schedule followed.",
            "Performance monitored in real time.",
            "Records audited regularly."
        ],
        resolution_strategy="Routine maintenance and audits.",
        entity_scope="CTD Equipment in DRL14",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Manufacturer Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Job Planning and Execution",
        keywords=["job planning", "execution", "coiled tubing drilling", "program", "risk assessment"],
        conclusion_template="CTD jobs are planned and executed per approved programs, with risk assessments and operational reviews.",
        reasoning_framework="""
Job planning doctrine:
1. Develop detailed job program with objectives, procedures, and contingencies.
2. Conduct risk assessment and pre-job safety meeting.
3. Communicate plan to all personnel.
4. Monitor execution and adjust as needed.
5. Document job performance and lessons learned.
6. Review execution post-job for continuous improvement.
7. Update planning procedures based on experience.
8. Archive job records for future reference.
""",
        key_factors=[
            "Job program",
            "Risk assessment",
            "Communication",
            "Monitoring",
            "Documentation"
        ],
        primary_authority=[
            "Company Job Planning Policy",
            "ICoTA Job Planning Guidelines"
        ],
        burden_holder="CTD Operations Supervisor",
        adversary_position="Job is poorly planned or executed, risking safety and performance.",
        counter_arguments=[
            "Detailed program and risk assessment conducted.",
            "Execution monitored and documented.",
            "Procedures updated based on lessons learned."
        ],
        resolution_strategy="Routine planning and post-job review.",
        entity_scope="CTD Jobs in DRL14",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ICoTA Job Planning Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Communication and Shift Handover",
        keywords=["communication", "shift handover", "coiled tubing drilling", "documentation", "continuity"],
        conclusion_template="Effective communication and documented shift handover are mandatory to ensure operational continuity and safety.",
        reasoning_framework="""
Communication doctrine:
1. Document all operational activities and status at shift change.
2. Conduct verbal handover between outgoing and incoming supervisors.
3. Review outstanding issues, risks, and planned activities.
4. Archive handover records for traceability.
5. Train personnel in handover procedures.
6. Audit handover effectiveness post-job.
7. Update procedures based on lessons learned.
8. Review handover process in incident investigations.
""",
        key_factors=[
            "Documentation",
            "Verbal handover",
            "Issue review",
            "Personnel training",
            "Auditing"
        ],
        primary_authority=[
            "Company Communication Policy",
            "ICoTA Handover Guidelines"
        ],
        burden_holder="CTD Supervisor",
        adversary_position="Poor handover leads to operational errors or incidents.",
        counter_arguments=[
            "Handover documented and conducted verbally.",
            "Personnel trained in procedures.",
            "Process audited post-job."
        ],
        resolution_strategy="Routine audits and procedure updates.",
        entity_scope="CTD Operations in DRL14",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="ICoTA Handover Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Third-Party Service Integration",
        keywords=["third-party", "service integration", "coiled tubing drilling", "vendor management", "coordination"],
        conclusion_template="Third-party services are integrated through pre-job coordination, documentation, and performance review.",
        reasoning_framework="""
Service integration doctrine:
1. Identify required third-party services and vendors.
2. Coordinate pre-job meetings to align objectives and procedures.
3. Document roles, responsibilities, and interfaces.
4. Monitor service performance during operation.
5. Review integration effectiveness post-job.
6. Update integration procedures based on lessons learned.
7. Archive service records for traceability.
8. Train personnel in vendor management.
""",
        key_factors=[
            "Service identification",
            "Pre-job coordination",
            "Documentation",
            "Performance monitoring",
            "Post-job review"
        ],
        primary_authority=[
            "Company Vendor Management Policy",
            "ICoTA Service Integration Guidelines"
        ],
        burden_holder="CTD Operations Supervisor",
        adversary_position="Poor integration leads to delays or operational errors.",
        counter_arguments=[
            "Pre-job coordination and documentation.",
            "Performance monitored and reviewed.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Routine review and personnel training.",
        entity_scope="CTD Operations in DRL14",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ICoTA Service Integration Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Logistics and Supply Chain Management",
        keywords=["logistics", "supply chain", "coiled tubing drilling", "inventory", "equipment mobilization"],
        conclusion_template="Logistics and supply chain management ensure timely mobilization, inventory control, and equipment readiness for CTD operations.",
        reasoning_framework="""
Logistics doctrine:
1. Plan equipment and material mobilization in advance.
2. Maintain inventory records for critical spares and consumables.
3. Coordinate logistics with vendors and transport providers.
4. Monitor equipment readiness and availability.
5. Document logistics actions and challenges.
6. Review logistics performance post-job.
7. Update logistics procedures based on lessons learned.
8. Train personnel in logistics management.
""",
        key_factors=[
            "Mobilization planning",
            "Inventory control",
            "Vendor coordination",
            "Equipment readiness",
            "Documentation"
        ],
        primary_authority=[
            "Company Logistics Policy",
            "ICoTA Logistics Guidelines"
        ],
        burden_holder="CTD Logistics Coordinator",
        adversary_position="Logistics failures cause delays or equipment shortages.",
        counter_arguments=[
            "Mobilization and inventory tracked.",
            "Coordination with vendors and providers.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Routine review and personnel training.",
        entity_scope="CTD Logistics in DRL14",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ICoTA Logistics Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Technology Evaluation and Adoption",
        keywords=["technology evaluation", "adoption", "coiled tubing drilling", "innovation", "field trial"],
        conclusion_template="New CTD technologies are evaluated and adopted through field trials, risk assessment, and performance review.",
        reasoning_framework="""
Technology evaluation doctrine:
1. Identify new technologies relevant to CTD operations.
2. Conduct risk assessment and feasibility study.
3. Plan and execute field trials.
4. Monitor performance and document results.
5. Review adoption decision with stakeholders.
6. Update operational procedures based on outcomes.
7. Archive evaluation records for traceability.
8. Train personnel in new technology use.
""",
        key_factors=[
            "Technology identification",
            "Risk assessment",
            "Field trial",
            "Performance monitoring",
            "Documentation"
        ],
        primary_authority=[
            "Company Technology Policy",
            "ICoTA Technology Guidelines"
        ],
        burden_holder="CTD Technology Manager",
        adversary_position="New technology adoption increases risk or fails to deliver benefits.",
        counter_arguments=[
            "Risk assessment and field trial conducted.",
            "Performance monitored and reviewed.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Routine review and stakeholder engagement.",
        entity_scope="CTD Technology in DRL14",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="ICoTA Technology Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Cost Control and Optimization",
        keywords=["cost control", "optimization", "coiled tubing drilling", "budget", "efficiency"],
        conclusion_template="Cost control is achieved by budget planning, performance monitoring, and continuous optimization of CTD operations.",
        reasoning_framework="""
Cost control doctrine:
1. Develop detailed budget for CTD operations.
2. Monitor costs in real time and compare to budget.
3. Identify and implement efficiency improvements.
4. Document cost drivers and savings.
5. Review cost performance post-job.
6. Update budget planning based on lessons learned.
7. Train personnel in cost control procedures.
8. Audit cost records regularly.
""",
        key_factors=[
            "Budget planning",
            "Performance monitoring",
            "Efficiency improvements",
            "Documentation",
            "Auditing"
        ],
        primary_authority=[
            "Company Finance Policy",
            "ICoTA Cost Control Guidelines"
        ],
        burden_holder="CTD Operations Manager",
        adversary_position="Costs exceed budget due to poor planning or inefficiency.",
        counter_arguments=[
            "Budget monitored in real time.",
            "Efficiency improvements implemented.",
            "Records audited regularly."
        ],
        resolution_strategy="Routine audits and continuous improvement.",
        entity_scope="CTD Operations in DRL14",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ICoTA Cost Control Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Stakeholder Engagement and Communication",
        keywords=["stakeholder engagement", "communication", "coiled tubing drilling", "transparency", "expectation management"],
        conclusion_template="Stakeholder engagement is maintained by transparent communication, regular updates, and expectation management for CTD operations.",
        reasoning_framework="""
Stakeholder engagement doctrine:
1. Identify all stakeholders for CTD operations.
2. Communicate objectives, plans, and risks transparently.
3. Provide regular updates during operations.
4. Document stakeholder concerns and responses.
5. Review engagement effectiveness post-job.
6. Update communication procedures as needed.
7. Train personnel in stakeholder engagement.
8. Archive communication records for traceability.
""",
        key_factors=[
            "Stakeholder identification",
            "Transparent communication",
            "Regular updates",
            "Documentation",
            "Personnel training"
        ],
        primary_authority=[
            "Company Stakeholder Policy",
            "ICoTA Communication Guidelines"
        ],
        burden_holder="CTD Project Manager",
        adversary_position="Stakeholder concerns are not addressed, leading to dissatisfaction.",
        counter_arguments=[
            "Communication documented and reviewed.",
            "Personnel trained in engagement.",
            "Procedures updated as needed."
        ],
        resolution_strategy="Routine review and stakeholder feedback.",
        entity_scope="CTD Projects in DRL14",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ICoTA Communication Guidelines"
    ),
    DoctrineBlock(
        topic="CTD Continuous Improvement and Lessons Learned",
        keywords=["continuous improvement", "lessons learned", "coiled tubing drilling", "performance review", "knowledge management"],
        conclusion_template="Continuous improvement is achieved by documenting lessons learned, reviewing performance, and updating procedures for CTD operations.",
        reasoning_framework="""
Continuous improvement doctrine:
1. Document lessons learned after each CTD operation.
2. Review performance data and identify improvement opportunities.
3. Update operational procedures based on findings.
4. Communicate improvements to all personnel.
5. Archive lessons learned for future reference.
6. Train personnel in continuous improvement practices.
7. Review effectiveness of improvements post-implementation.
8. Audit improvement process regularly.
""",
        key_factors=[
            "Lessons learned documentation",
            "Performance review",
            "Procedure updates",
            "Communication",
            "Auditing"
        ],
        primary_authority=[
            "Company Continuous Improvement Policy",
            "ICoTA Best Practices"
        ],
        burden_holder="CTD Operations Supervisor",
        adversary_position="Lessons learned are not implemented, leading to repeat issues.",
        counter_arguments=[
            "Lessons documented and communicated.",
            "Procedures updated regularly.",
            "Effectiveness reviewed post-implementation."
        ],
        resolution_strategy="Routine audits and personnel training.",
        entity_scope="CTD Operations in DRL14",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ICoTA Best Practices"
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