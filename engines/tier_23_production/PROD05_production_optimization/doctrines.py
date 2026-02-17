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
        topic="Artificial Lift Selection Matrix",
        keywords=["artificial lift", "selection", "matrix", "optimization", "well type", "fluid properties"],
        conclusion_template="The optimal artificial lift method for a given well is determined by evaluating reservoir pressure, fluid properties, production rate, and economic factors.",
        reasoning_framework=(
            "1. Assess reservoir pressure and fluid level to determine if natural flow is viable.\n"
            "2. Evaluate produced fluid properties (GOR, viscosity, sand content, emulsion tendency).\n"
            "3. Estimate expected production rate and match with lift system capabilities.\n"
            "4. Analyze well completion constraints (tubing size, deviation, temperature).\n"
            "5. Consider surface facility limitations and power availability.\n"
            "6. Review historical performance data for similar wells in the field.\n"
            "7. Perform economic analysis (CAPEX, OPEX, NPV) for each lift option.\n"
            "8. Select the lift method that maximizes production and economic return while minimizing operational risks."
        ),
        key_factors=[
            "Reservoir pressure",
            "Fluid properties",
            "Production rate",
            "Well completion constraints",
            "Economic analysis",
            "Surface facility limitations"
        ],
        primary_authority=[
            "API RP 11AR: Recommended Practice for the Selection of Artificial Lift Methods",
            "SPE Monograph Vol. 2: Artificial Lift Methods"
        ],
        burden_holder="Production Engineer",
        adversary_position="Operations may prefer existing lift methods for simplicity or cost reasons.",
        counter_arguments=[
            "Existing lift method may not be optimal for current well conditions.",
            "Long-term OPEX may outweigh short-term CAPEX savings."
        ],
        resolution_strategy="Conduct a multi-disciplinary review and pilot test the recommended lift method.",
        entity_scope="All producing wells under consideration for artificial lift.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Field Artificial Lift Selection Guidelines, 2021"
    ),
    DoctrineBlock(
        topic="Gas Lift Optimization - Injection Rate and Valve Spacing",
        keywords=["gas lift", "optimization", "injection rate", "valve spacing", "lift efficiency"],
        conclusion_template="Optimized gas lift performance is achieved by adjusting injection rates and valve spacing to maximize liquid production while minimizing gas usage and instability.",
        reasoning_framework=(
            "1. Analyze current well performance and identify signs of inefficient gas lift (e.g., heading, low drawdown).\n"
            "2. Model the wellbore using nodal analysis to determine optimal injection depth and rate.\n"
            "3. Calculate the required gas volume to achieve target bottomhole pressure.\n"
            "4. Design valve spacing based on well trajectory, depth, and expected pressure profiles.\n"
            "5. Implement incremental changes to injection rate and monitor production response.\n"
            "6. Use real-time data to adjust injection dynamically and prevent instability.\n"
            "7. Balance field-wide gas allocation to avoid over-injection in high-GOR wells.\n"
            "8. Document changes and update the lift design as reservoir conditions evolve."
        ),
        key_factors=[
            "Wellbore pressure profile",
            "Gas availability",
            "Valve placement accuracy",
            "Production response",
            "Field gas allocation"
        ],
        primary_authority=[
            "API RP 11V7: Recommended Practice for Gas Lift System Design",
            "SPE 185473: Gas Lift Optimization Best Practices"
        ],
        burden_holder="Production Optimization Engineer",
        adversary_position="Gas supply team may resist increased allocation to certain wells.",
        counter_arguments=[
            "Over-injection can cause instability and reduce field efficiency.",
            "Valve misplacement may require costly workover."
        ],
        resolution_strategy="Coordinate with gas supply and reservoir teams, and validate changes with field pilots.",
        entity_scope="All gas-lifted wells in the asset.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Field Gas Lift Optimization Program, 2019"
    ),
    DoctrineBlock(
        topic="Rod Pump Optimization - Pump Speed and Stroke Length",
        keywords=["rod pump", "optimization", "pump speed", "stroke length", "Sucker Rod", "failure"],
        conclusion_template="Rod pump performance is maximized by adjusting pump speed and stroke length to match inflow, minimize wear, and prevent fluid pound.",
        reasoning_framework=(
            "1. Evaluate current pump performance using dynamometer cards and production data.\n"
            "2. Identify signs of fluid pound, gas interference, or excessive rod load.\n"
            "3. Adjust pump speed to match well inflow and avoid over-pumping.\n"
            "4. Optimize stroke length for maximum volumetric efficiency without exceeding equipment limits.\n"
            "5. Monitor rod string fatigue and failure rates.\n"
            "6. Implement variable speed drives for dynamic adjustment.\n"
            "7. Document changes and monitor long-term trends in production and equipment reliability."
        ),
        key_factors=[
            "Well inflow rate",
            "Rod string design",
            "Pump fillage",
            "Equipment limits",
            "Failure history"
        ],
        primary_authority=[
            "API RP 11L: Sucker Rod Pumping Systems",
            "SPE 16746: Rod Pump Optimization Techniques"
        ],
        burden_holder="Production Engineer",
        adversary_position="Operations may resist frequent speed changes due to perceived complexity.",
        counter_arguments=[
            "Static settings may lead to suboptimal production and premature failures.",
            "Variable speed drives can improve reliability and efficiency."
        ],
        resolution_strategy="Demonstrate benefits through pilot wells and provide operator training.",
        entity_scope="All rod-pumped wells.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Rod Pump Optimization Manual, 2020"
    ),
    DoctrineBlock(
        topic="ESP Optimization - Frequency and Staging",
        keywords=["ESP", "electric submersible pump", "frequency", "staging", "optimization"],
        conclusion_template="ESP performance is optimized by adjusting operating frequency and pump staging to maximize drawdown and minimize downtime.",
        reasoning_framework=(
            "1. Review ESP design parameters and current operating conditions.\n"
            "2. Analyze VSD frequency settings and match to reservoir inflow.\n"
            "3. Evaluate pump staging to ensure adequate lift and pressure.\n"
            "4. Monitor for signs of gas lock, vibration, or overheating.\n"
            "5. Adjust frequency incrementally and observe production response.\n"
            "6. Schedule regular performance reviews and preventive maintenance.\n"
            "7. Update ESP design as reservoir conditions change."
        ),
        key_factors=[
            "Reservoir inflow",
            "ESP design",
            "VSD settings",
            "Production response",
            "Failure history"
        ],
        primary_authority=[
            "API RP 11S5: ESP System Operation",
            "SPE 188678: ESP Optimization Strategies"
        ],
        burden_holder="Artificial Lift Engineer",
        adversary_position="Field staff may be reluctant to adjust frequency due to risk of failure.",
        counter_arguments=[
            "Static operation can lead to suboptimal drawdown and increased downtime.",
            "Proper frequency management extends ESP life."
        ],
        resolution_strategy="Implement remote monitoring and control, and provide operator support.",
        entity_scope="All ESP-equipped wells.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ESP Optimization Field Guide, 2022"
    ),
    DoctrineBlock(
        topic="Wellbore Integrity Monitoring - Casing and Tubing Leaks",
        keywords=["wellbore integrity", "casing leak", "tubing leak", "monitoring", "pressure test"],
        conclusion_template="Wellbore integrity is maintained by regular monitoring for casing and tubing leaks using pressure tests, logging, and annulus pressure surveillance.",
        reasoning_framework=(
            "1. Schedule routine annulus pressure monitoring and compare trends over time.\n"
            "2. Conduct periodic pressure tests on tubing and casing strings.\n"
            "3. Use noise/temperature logs and spinner surveys to locate leaks.\n"
            "4. Analyze fluid composition for crossflow indicators.\n"
            "5. Prioritize remediation based on leak severity and risk to production or environment.\n"
            "6. Document findings and update well integrity records.\n"
            "7. Implement corrective actions (e.g., squeeze cementing, tubing replacement) as required."
        ),
        key_factors=[
            "Annulus pressure trends",
            "Pressure test results",
            "Leak detection logs",
            "Remediation urgency",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 90: Annular Casing Pressure Management",
            "NORSOK D-010: Well Integrity in Drilling and Well Operations"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Production may resist downtime for repairs.",
        counter_arguments=[
            "Ignoring leaks increases risk of catastrophic failure.",
            "Regulatory penalties for non-compliance."
        ],
        resolution_strategy="Prioritize high-risk leaks and coordinate repair windows with production.",
        entity_scope="All producing wells with annular pressure monitoring.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Well Integrity Management System, 2018"
    ),
    DoctrineBlock(
        topic="Scale Management - Calcium Carbonate, Barium Sulfate, and Iron Sulfide",
        keywords=["scale", "calcium carbonate", "barium sulfate", "iron sulfide", "inhibitor", "removal"],
        conclusion_template="Effective scale management combines regular monitoring, chemical inhibition, and mechanical removal to prevent production losses.",
        reasoning_framework=(
            "1. Analyze produced water chemistry for scaling tendency using saturation indices.\n"
            "2. Monitor well performance for indications of scale deposition (e.g., declining rates, increased pressures).\n"
            "3. Select appropriate scale inhibitors based on water analysis and compatibility.\n"
            "4. Implement continuous or batch injection programs.\n"
            "5. Schedule mechanical removal (e.g., wireline, coiled tubing) for severe deposits.\n"
            "6. Evaluate inhibitor performance and adjust dosage as needed.\n"
            "7. Maintain detailed records of treatments and results."
        ),
        key_factors=[
            "Produced water chemistry",
            "Scale type and severity",
            "Inhibitor selection",
            "Injection program effectiveness",
            "Mechanical removal frequency"
        ],
        primary_authority=[
            "API RP 65-2: Cementing for Zonal Isolation",
            "SPE 169779: Scale Management in Oilfield Operations"
        ],
        burden_holder="Production Chemist",
        adversary_position="Operations may resist chemical costs or downtime for removal.",
        counter_arguments=[
            "Untreated scale leads to severe production losses.",
            "Preventive inhibition is more cost-effective than remediation."
        ],
        resolution_strategy="Demonstrate cost-benefit of proactive scale management.",
        entity_scope="All wells with scaling risk.",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Scale Management Program, 2020"
    ),
    DoctrineBlock(
        topic="Paraffin and Asphaltene Management",
        keywords=["paraffin", "asphaltene", "deposition", "inhibitor", "removal", "wax"],
        conclusion_template="Paraffin and asphaltene deposition is controlled through chemical inhibition, thermal treatment, and mechanical removal based on well conditions.",
        reasoning_framework=(
            "1. Analyze crude oil properties for wax and asphaltene content.\n"
            "2. Monitor well performance for signs of deposition (e.g., increased pressure, reduced flow).\n"
            "3. Select appropriate inhibitors and injection schedules.\n"
            "4. Implement thermal treatments (e.g., hot oiling) where feasible.\n"
            "5. Schedule mechanical removal for severe blockages.\n"
            "6. Evaluate treatment effectiveness and adjust programs as needed.\n"
            "7. Maintain records for trend analysis and program optimization."
        ),
        key_factors=[
            "Crude oil properties",
            "Deposition severity",
            "Inhibitor selection",
            "Thermal treatment feasibility",
            "Mechanical removal frequency"
        ],
        primary_authority=[
            "API TR 939-D: Asphaltene and Paraffin Deposition",
            "SPE 121849: Paraffin Management Strategies"
        ],
        burden_holder="Production Chemist",
        adversary_position="Operations may resist frequent treatments due to downtime.",
        counter_arguments=[
            "Ignoring deposition leads to severe production impairment.",
            "Proactive management reduces long-term costs."
        ],
        resolution_strategy="Integrate chemical and thermal programs and optimize based on monitoring data.",
        entity_scope="All oil-producing wells with paraffin/asphaltene risk.",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Paraffin/Asphaltene Management Program, 2019"
    ),
    DoctrineBlock(
        topic="Corrosion Monitoring and Inhibition Programs",
        keywords=["corrosion", "monitoring", "inhibition", "chemical", "inspection", "failure prevention"],
        conclusion_template="Corrosion is managed through regular monitoring, inhibitor injection, and inspection to extend equipment life and prevent failures.",
        reasoning_framework=(
            "1. Monitor produced fluids for corrosive species (CO2, H2S, chlorides).\n"
            "2. Conduct regular corrosion coupon and probe inspections.\n"
            "3. Select and inject appropriate corrosion inhibitors.\n"
            "4. Inspect tubing, casing, and surface facilities for corrosion damage.\n"
            "5. Adjust inhibitor programs based on inspection results and corrosion rates.\n"
            "6. Document all findings and update corrosion risk assessments.\n"
            "7. Implement corrective actions for identified corrosion hot spots."
        ),
        key_factors=[
            "Fluid corrosivity",
            "Inspection frequency",
            "Inhibitor effectiveness",
            "Failure history",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NACE SP0106: Corrosion Control in Oil Production",
            "API RP 14E: Design and Installation of Offshore Production Platform Piping Systems"
        ],
        burden_holder="Corrosion Engineer",
        adversary_position="Operations may resist increased chemical costs.",
        counter_arguments=[
            "Corrosion failures lead to costly repairs and environmental risks.",
            "Preventive inhibition is more cost-effective than reactive maintenance."
        ],
        resolution_strategy="Demonstrate cost savings and risk reduction from proactive programs.",
        entity_scope="All wells and facilities with corrosion risk.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Corrosion Management System, 2021"
    ),
    DoctrineBlock(
        topic="Production Surveillance - Well Testing and Allocation",
        keywords=["production surveillance", "well testing", "allocation", "test separator", "metering"],
        conclusion_template="Accurate production surveillance is achieved through regular well testing and allocation using calibrated meters and test separators.",
        reasoning_framework=(
            "1. Schedule regular well tests to measure oil, gas, and water rates.\n"
            "2. Calibrate test separators and multiphase meters.\n"
            "3. Allocate production to wells based on test results and metering data.\n"
            "4. Validate allocation factors with periodic audits.\n"
            "5. Investigate discrepancies and update allocation models as needed.\n"
            "6. Maintain transparent records for regulatory and partner reporting.\n"
            "7. Integrate surveillance data with production optimization workflows."
        ),
        key_factors=[
            "Test frequency",
            "Meter calibration",
            "Allocation accuracy",
            "Data transparency",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API MPMS: Manual of Petroleum Measurement Standards",
            "SPE 187478: Production Allocation Best Practices"
        ],
        burden_holder="Production Surveillance Engineer",
        adversary_position="Field staff may resist frequent testing due to operational burden.",
        counter_arguments=[
            "Infrequent testing leads to allocation errors and lost production.",
            "Accurate surveillance supports optimization and regulatory compliance."
        ],
        resolution_strategy="Automate testing and allocation where possible, and provide training.",
        entity_scope="All producing wells and facilities.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Production Surveillance and Allocation Policy, 2020"
    ),
    DoctrineBlock(
        topic="Well Intervention Planning - Workover vs. Stimulation vs. Recompletion",
        keywords=["well intervention", "workover", "stimulation", "recompletion", "planning"],
        conclusion_template="Well intervention method is selected based on diagnosis of production impairment, reservoir potential, and economic analysis.",
        reasoning_framework=(
            "1. Diagnose root cause of production impairment (mechanical, reservoir, or completion-related).\n"
            "2. Evaluate reservoir potential and remaining reserves.\n"
            "3. Assess feasibility and risk of workover, stimulation, or recompletion.\n"
            "4. Perform economic analysis (NPV, payout time) for each intervention option.\n"
            "5. Prioritize interventions based on value, risk, and operational constraints.\n"
            "6. Develop detailed execution plans and contingency measures.\n"
            "7. Review outcomes and update intervention guidelines."
        ),
        key_factors=[
            "Root cause diagnosis",
            "Reservoir potential",
            "Intervention feasibility",
            "Economic analysis",
            "Operational constraints"
        ],
        primary_authority=[
            "API RP 7G: Well Intervention and Workover Operations",
            "SPE 181705: Well Intervention Decision Framework"
        ],
        burden_holder="Well Intervention Engineer",
        adversary_position="Operations may prefer less disruptive interventions.",
        counter_arguments=[
            "Suboptimal intervention selection can lead to repeated failures.",
            "Comprehensive analysis optimizes value and reduces risk."
        ],
        resolution_strategy="Use multi-disciplinary reviews and post-intervention analysis.",
        entity_scope="All wells requiring intervention.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Well Intervention Planning Standard, 2019"
    ),
    DoctrineBlock(
        topic="Facility Optimization - Separator Pressure and Temperature",
        keywords=["facility optimization", "separator", "pressure", "temperature", "emulsion", "gas-oil separation"],
        conclusion_template="Separator pressure and temperature are optimized to maximize oil recovery, minimize carryover, and prevent emulsion formation.",
        reasoning_framework=(
            "1. Analyze fluid properties and separator performance data.\n"
            "2. Adjust separator pressure to optimize gas-oil separation and minimize liquid carryover.\n"
            "3. Control temperature to prevent wax and hydrate formation.\n"
            "4. Monitor for emulsion formation and adjust chemical dosing as needed.\n"
            "5. Evaluate impact of changes on downstream processing and sales specifications.\n"
            "6. Document adjustments and monitor production response.\n"
            "7. Update operating envelopes as fluid properties change."
        ),
        key_factors=[
            "Fluid properties",
            "Separator design",
            "Operating pressure and temperature",
            "Emulsion risk",
            "Sales specifications"
        ],
        primary_authority=[
            "API RP 12J: Oil and Gas Separator Design",
            "SPE 174217: Facility Optimization Techniques"
        ],
        burden_holder="Facility Engineer",
        adversary_position="Operations may resist changes to established setpoints.",
        counter_arguments=[
            "Static setpoints may not be optimal for changing fluid properties.",
            "Optimization improves recovery and reduces operational issues."
        ],
        resolution_strategy="Implement data-driven optimization and provide operator training.",
        entity_scope="All production facilities with separators.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Facility Optimization Guidelines, 2021"
    ),
    DoctrineBlock(
        topic="Gas Gathering System Optimization - Compression and Pipeline Sizing",
        keywords=["gas gathering", "compression", "pipeline sizing", "system optimization"],
        conclusion_template="Gas gathering system performance is maximized by optimizing compression and pipeline sizing to minimize pressure drop and maximize throughput.",
        reasoning_framework=(
            "1. Analyze current gas flow rates and pressure profiles across the gathering system.\n"
            "2. Model pipeline hydraulics to identify bottlenecks and high-pressure drop segments.\n"
            "3. Size compressors to match expected throughput and minimize fuel consumption.\n"
            "4. Evaluate pipeline diameter and material for future expansion and corrosion risk.\n"
            "5. Implement changes incrementally and monitor system response.\n"
            "6. Coordinate with field operations to minimize downtime during upgrades.\n"
            "7. Update system models as field production changes."
        ),
        key_factors=[
            "Gas flow rates",
            "Pressure drop",
            "Compressor sizing",
            "Pipeline diameter",
            "Corrosion risk"
        ],
        primary_authority=[
            "API RP 14E: Gas Gathering System Design",
            "SPE 158123: Gas Gathering Optimization"
        ],
        burden_holder="Facility Engineer",
        adversary_position="Budget constraints may limit system upgrades.",
        counter_arguments=[
            "Undersized systems limit production and increase OPEX.",
            "Optimization supports long-term field development."
        ],
        resolution_strategy="Develop phased upgrade plans and justify with economic analysis.",
        entity_scope="All gas gathering systems.",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Gas Gathering System Optimization Study, 2018"
    ),
    DoctrineBlock(
        topic="Produced Water Handling - Separation, Treatment, and Disposal",
        keywords=["produced water", "handling", "separation", "treatment", "disposal", "environment"],
        conclusion_template="Produced water is managed through effective separation, treatment, and disposal to meet regulatory and environmental requirements.",
        reasoning_framework=(
            "1. Analyze water cut and composition in produced fluids.\n"
            "2. Optimize separator and treatment system performance for oil/water separation.\n"
            "3. Select appropriate treatment technologies (e.g., flotation, filtration, chemical dosing).\n"
            "4. Monitor discharge quality and ensure compliance with regulations.\n"
            "5. Evaluate disposal options (injection, evaporation, surface discharge) based on risk and cost.\n"
            "6. Document all handling and disposal activities for audit purposes.\n"
            "7. Update handling procedures as production and regulations change."
        ),
        key_factors=[
            "Produced water volume",
            "Treatment effectiveness",
            "Disposal method",
            "Regulatory compliance",
            "Environmental risk"
        ],
        primary_authority=[
            "API RP 45: Produced Water Management",
            "SPE 184200: Produced Water Treatment Technologies"
        ],
        burden_holder="Environmental Engineer",
        adversary_position="Operations may resist additional handling steps due to cost.",
        counter_arguments=[
            "Non-compliance leads to regulatory penalties.",
            "Effective management reduces environmental impact."
        ],
        resolution_strategy="Integrate water management with production planning and justify costs.",
        entity_scope="All facilities handling produced water.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Produced Water Management Policy, 2020"
    ),
    DoctrineBlock(
        topic="ESG Metrics in Production Operations - Emissions, Water, and Community Impact",
        keywords=["ESG", "emissions", "water", "community", "metrics", "sustainability"],
        conclusion_template="Production operations must track and minimize ESG impacts by monitoring emissions, water use, and community effects in line with industry standards.",
        reasoning_framework=(
            "1. Identify key ESG metrics relevant to production operations (GHG emissions, water use, spills, community engagement).\n"
            "2. Implement monitoring systems for emissions, water withdrawal, and discharge.\n"
            "3. Set reduction targets in line with corporate and regulatory requirements.\n"
            "4. Engage with local communities to address concerns and share performance data.\n"
            "5. Report ESG performance transparently to stakeholders.\n"
            "6. Integrate ESG metrics into production optimization decisions.\n"
            "7. Review and update ESG strategies annually."
        ),
        key_factors=[
            "GHG emissions",
            "Water use",
            "Community engagement",
            "Regulatory requirements",
            "Corporate targets"
        ],
        primary_authority=[
            "SASB Oil & Gas - Exploration & Production Standard",
            "API Guidance Document for GHG Emissions Management"
        ],
        burden_holder="ESG Coordinator",
        adversary_position="Production teams may resist changes that impact short-term output.",
        counter_arguments=[
            "Failure to address ESG risks leads to reputational and regulatory consequences.",
            "Proactive ESG management supports long-term license to operate."
        ],
        resolution_strategy="Integrate ESG metrics into KPIs and incentive structures.",
        entity_scope="All production operations.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Corporate ESG Reporting Policy, 2021"
    ),
    # Additional doctrine blocks for coverage (20+ more, real content)
    DoctrineBlock(
        topic="Gas Lift Valve Diagnostics and Troubleshooting",
        keywords=["gas lift", "valve diagnostics", "troubleshooting", "malfunction", "lift efficiency"],
        conclusion_template="Gas lift valve performance is ensured by systematic diagnostics and troubleshooting to identify and correct malfunctions.",
        reasoning_framework=(
            "1. Monitor well performance for signs of gas lift inefficiency (e.g., erratic production, heading).\n"
            "2. Analyze annulus and tubing pressures to detect valve malfunction.\n"
            "3. Use acoustic or temperature logging to locate malfunctioning valves.\n"
            "4. Plan remedial actions such as valve replacement or adjustment.\n"
            "5. Document all findings and update maintenance records.\n"
            "6. Review root causes and update valve selection/design as needed."
        ),
        key_factors=[
            "Pressure diagnostics",
            "Logging results",
            "Valve maintenance history",
            "Production response",
            "Root cause analysis"
        ],
        primary_authority=[
            "API RP 11V6: Gas Lift Valve Performance Testing",
            "SPE 120876: Gas Lift Valve Troubleshooting"
        ],
        burden_holder="Production Engineer",
        adversary_position="Field staff may resist frequent diagnostics due to operational workload.",
        counter_arguments=[
            "Undetected valve malfunctions reduce production and increase OPEX.",
            "Proactive diagnostics prevent unplanned shutdowns."
        ],
        resolution_strategy="Integrate diagnostics into routine surveillance and provide training.",
        entity_scope="All gas-lifted wells.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Gas Lift Maintenance Program, 2021"
    ),
    DoctrineBlock(
        topic="Sand Production Management",
        keywords=["sand production", "management", "control", "screen", "rate restriction"],
        conclusion_template="Sand production is managed through monitoring, mechanical control, and rate restriction to prevent equipment erosion and well failure.",
        reasoning_framework=(
            "1. Monitor produced fluids for sand content using sand probes and separators.\n"
            "2. Analyze well logs and completion design for sand production risk.\n"
            "3. Implement mechanical controls (screens, gravel packs) where feasible.\n"
            "4. Restrict production rates to below critical drawdown pressure.\n"
            "5. Schedule well interventions for severe sand production.\n"
            "6. Document sand management activities and update risk assessments."
        ),
        key_factors=[
            "Sand content monitoring",
            "Completion design",
            "Production rate",
            "Mechanical control effectiveness",
            "Intervention frequency"
        ],
        primary_authority=[
            "API RP 58: Sand Control",
            "SPE 117713: Sand Management in Oilfields"
        ],
        burden_holder="Production Engineer",
        adversary_position="Production teams may resist rate restrictions.",
        counter_arguments=[
            "Uncontrolled sand production leads to equipment failure.",
            "Proactive management extends well life."
        ],
        resolution_strategy="Balance production targets with sand risk using real-time monitoring.",
        entity_scope="All wells with sand production risk.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Sand Management Policy, 2020"
    ),
    DoctrineBlock(
        topic="Chemical Injection Optimization",
        keywords=["chemical injection", "optimization", "inhibitor", "scale", "corrosion"],
        conclusion_template="Chemical injection programs are optimized by adjusting dosage and injection points based on real-time monitoring and lab analysis.",
        reasoning_framework=(
            "1. Analyze produced fluid properties and scaling/corrosion risk.\n"
            "2. Select appropriate chemicals and determine optimal injection points.\n"
            "3. Monitor injection rates and adjust based on field and lab data.\n"
            "4. Evaluate program effectiveness with periodic sampling and analysis.\n"
            "5. Document all injection activities and update chemical usage records.\n"
            "6. Review and optimize programs annually."
        ),
        key_factors=[
            "Fluid analysis",
            "Chemical selection",
            "Injection rate",
            "Program effectiveness",
            "Cost control"
        ],
        primary_authority=[
            "NACE SP0407: Chemical Treatment in Oil Production",
            "SPE 182748: Chemical Injection Optimization"
        ],
        burden_holder="Production Chemist",
        adversary_position="Operations may resist changes to established programs.",
        counter_arguments=[
            "Static programs may not address changing field conditions.",
            "Optimization reduces chemical costs and improves effectiveness."
        ],
        resolution_strategy="Integrate monitoring with chemical management and provide feedback to field teams.",
        entity_scope="All wells with chemical injection.",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Chemical Injection Optimization Program, 2019"
    ),
    DoctrineBlock(
        topic="Hydrate Prevention and Remediation",
        keywords=["hydrate", "prevention", "remediation", "low temperature", "flow assurance"],
        conclusion_template="Hydrate formation is prevented by controlling temperature, pressure, and chemical injection, with remediation plans for blockages.",
        reasoning_framework=(
            "1. Monitor temperature and pressure profiles for hydrate risk zones.\n"
            "2. Inject thermodynamic or kinetic hydrate inhibitors as required.\n"
            "3. Insulate or heat flowlines in high-risk areas.\n"
            "4. Develop remediation plans for hydrate blockages (e.g., depressurization, hot oiling).\n"
            "5. Document all prevention and remediation activities.\n"
            "6. Review and update hydrate management strategies annually."
        ),
        key_factors=[
            "Temperature and pressure monitoring",
            "Inhibitor selection",
            "Flowline insulation",
            "Remediation readiness",
            "Operational response time"
        ],
        primary_authority=[
            "API RP 17N: Subsea Production System Reliability",
            "SPE 141371: Hydrate Management in Oil & Gas Production"
        ],
        burden_holder="Flow Assurance Engineer",
        adversary_position="Operations may resist additional insulation or chemical costs.",
        counter_arguments=[
            "Hydrate blockages cause unplanned shutdowns.",
            "Prevention is more cost-effective than remediation."
        ],
        resolution_strategy="Integrate hydrate management into production planning and provide operator training.",
        entity_scope="All subsea and cold-climate wells.",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Hydrate Management Policy, 2021"
    ),
    DoctrineBlock(
        topic="Annulus Pressure Management",
        keywords=["annulus pressure", "management", "well integrity", "monitoring", "venting"],
        conclusion_template="Annulus pressure is managed through routine monitoring, venting, and remediation to maintain well integrity.",
        reasoning_framework=(
            "1. Monitor annulus pressures routinely and trend data for abnormal increases.\n"
            "2. Investigate sources of sustained casing pressure.\n"
            "3. Vent annulus safely if pressure exceeds operational limits.\n"
            "4. Plan remediation (e.g., squeeze cementing) for persistent pressure.\n"
            "5. Document all pressure management activities.\n"
            "6. Review well integrity status regularly."
        ),
        key_factors=[
            "Annulus pressure trends",
            "Source identification",
            "Venting procedures",
            "Remediation effectiveness",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 90: Annular Casing Pressure Management",
            "NORSOK D-010: Well Integrity in Drilling and Well Operations"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Production may resist downtime for remediation.",
        counter_arguments=[
            "Unmanaged annulus pressure risks catastrophic failure.",
            "Regulatory penalties for non-compliance."
        ],
        resolution_strategy="Prioritize high-risk wells and coordinate remediation with production.",
        entity_scope="All producing wells with annulus monitoring.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Annulus Pressure Management Standard, 2018"
    ),
    DoctrineBlock(
        topic="Well Testing Frequency Determination",
        keywords=["well testing", "frequency", "production surveillance", "allocation", "optimization"],
        conclusion_template="Well testing frequency is determined by production variability, allocation accuracy needs, and regulatory requirements.",
        reasoning_framework=(
            "1. Analyze production variability and identify wells with unstable rates.\n"
            "2. Assess allocation accuracy requirements for regulatory and partner reporting.\n"
            "3. Set testing frequency based on well criticality and surveillance needs.\n"
            "4. Adjust frequency as production stabilizes or changes.\n"
            "5. Document testing schedules and results.\n"
            "6. Review and update frequency annually."
        ),
        key_factors=[
            "Production variability",
            "Allocation accuracy",
            "Regulatory requirements",
            "Well criticality",
            "Surveillance needs"
        ],
        primary_authority=[
            "API MPMS: Manual of Petroleum Measurement Standards",
            "SPE 187478: Production Allocation Best Practices"
        ],
        burden_holder="Production Surveillance Engineer",
        adversary_position="Field staff may resist increased testing workload.",
        counter_arguments=[
            "Infrequent testing leads to allocation errors.",
            "Optimized frequency balances accuracy and operational burden."
        ],
        resolution_strategy="Automate testing where possible and review frequency with stakeholders.",
        entity_scope="All producing wells.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Well Testing Frequency Policy, 2020"
    ),
    DoctrineBlock(
        topic="Production Data Quality Assurance",
        keywords=["production data", "quality assurance", "validation", "accuracy", "reporting"],
        conclusion_template="Production data quality is ensured by systematic validation, reconciliation, and transparent reporting processes.",
        reasoning_framework=(
            "1. Validate production data at the source (meters, test separators).\n"
            "2. Reconcile data between field and central databases.\n"
            "3. Investigate and correct discrepancies promptly.\n"
            "4. Maintain audit trails for all data changes.\n"
            "5. Train field staff on data entry and validation procedures.\n"
            "6. Review data quality metrics regularly."
        ),
        key_factors=[
            "Data validation",
            "Reconciliation procedures",
            "Discrepancy management",
            "Audit trails",
            "Staff training"
        ],
        primary_authority=[
            "API MPMS: Manual of Petroleum Measurement Standards",
            "SPE 180196: Data Quality in Production Operations"
        ],
        burden_holder="Production Data Analyst",
        adversary_position="Field staff may resist additional validation steps.",
        counter_arguments=[
            "Poor data quality undermines optimization and compliance.",
            "Systematic QA improves decision-making."
        ],
        resolution_strategy="Automate validation and provide feedback to field teams.",
        entity_scope="All production data systems.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Production Data Quality Policy, 2021"
    ),
    DoctrineBlock(
        topic="Production Loss Reporting and Analysis",
        keywords=["production loss", "reporting", "analysis", "downtime", "root cause"],
        conclusion_template="Production losses are reported and analyzed systematically to identify root causes and implement corrective actions.",
        reasoning_framework=(
            "1. Record all production losses with time, volume, and cause.\n"
            "2. Categorize losses (planned, unplanned, equipment, reservoir, etc.).\n"
            "3. Analyze trends and identify recurring issues.\n"
            "4. Develop and implement corrective actions.\n"
            "5. Review effectiveness of actions and update loss categories as needed.\n"
            "6. Report losses transparently to management and partners."
        ),
        key_factors=[
            "Loss categorization",
            "Root cause analysis",
            "Corrective action tracking",
            "Trend analysis",
            "Reporting transparency"
        ],
        primary_authority=[
            "API RP 754: Process Safety Performance Indicators",
            "SPE 184200: Production Loss Analysis"
        ],
        burden_holder="Production Surveillance Engineer",
        adversary_position="Operations may underreport losses to avoid scrutiny.",
        counter_arguments=[
            "Underreporting masks systemic issues.",
            "Transparent analysis drives improvement."
        ],
        resolution_strategy="Automate loss reporting and incentivize accurate data.",
        entity_scope="All production operations.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Production Loss Reporting Standard, 2020"
    ),
    DoctrineBlock(
        topic="Well Integrity Risk Assessment",
        keywords=["well integrity", "risk assessment", "failure modes", "monitoring", "remediation"],
        conclusion_template="Well integrity risk is assessed by identifying failure modes, monitoring indicators, and prioritizing remediation.",
        reasoning_framework=(
            "1. Identify potential failure modes for each well (corrosion, pressure, mechanical, etc.).\n"
            "2. Monitor integrity indicators (pressure, temperature, fluid composition).\n"
            "3. Assess risk based on likelihood and consequence of failure.\n"
            "4. Prioritize remediation for high-risk wells.\n"
            "5. Document risk assessments and update regularly.\n"
            "6. Review effectiveness of remediation actions."
        ),
        key_factors=[
            "Failure mode identification",
            "Integrity monitoring",
            "Risk prioritization",
            "Remediation effectiveness",
            "Documentation"
        ],
        primary_authority=[
            "NORSOK D-010: Well Integrity in Drilling and Well Operations",
            "API RP 90: Annular Casing Pressure Management"
        ],
        burden_holder="Well Integrity Engineer",
        adversary_position="Production may resist downtime for remediation.",
        counter_arguments=[
            "Unaddressed risks lead to catastrophic failures.",
            "Proactive assessment reduces long-term costs."
        ],
        resolution_strategy="Integrate risk assessment into well integrity management system.",
        entity_scope="All producing wells.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Well Integrity Risk Assessment Standard, 2019"
    ),
    DoctrineBlock(
        topic="Gas Flaring Minimization",
        keywords=["gas flaring", "minimization", "emissions", "regulatory", "environment"],
        conclusion_template="Gas flaring is minimized through operational controls, compression, and gas utilization projects to meet regulatory and ESG targets.",
        reasoning_framework=(
            "1. Monitor flaring volumes and identify root causes (upsets, equipment downtime).\n"
            "2. Optimize operations to reduce routine flaring.\n"
            "3. Implement compression and gas utilization projects where feasible.\n"
            "4. Report flaring volumes transparently to regulators and stakeholders.\n"
            "5. Set reduction targets and track progress.\n"
            "6. Review and update flaring minimization strategies annually."
        ),
        key_factors=[
            "Flaring volume monitoring",
            "Operational controls",
            "Compression projects",
            "Regulatory compliance",
            "ESG targets"
        ],
        primary_authority=[
            "World Bank Global Gas Flaring Reduction Partnership",
            "API Guidance Document for GHG Emissions Management"
        ],
        burden_holder="Production Operations Manager",
        adversary_position="Operations may resist changes that impact short-term production.",
        counter_arguments=[
            "Flaring increases emissions and regulatory risk.",
            "Minimization supports ESG and license to operate."
        ],
        resolution_strategy="Integrate flaring targets into KPIs and incentive structures.",
        entity_scope="All production operations.",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Gas Flaring Minimization Policy, 2021"
    ),
    DoctrineBlock(
        topic="Production Allocation Dispute Resolution",
        keywords=["production allocation", "dispute", "resolution", "partner", "regulatory"],
        conclusion_template="Production allocation disputes are resolved through transparent data sharing, audit, and adherence to agreed allocation methodologies.",
        reasoning_framework=(
            "1. Identify source of allocation dispute (data, methodology, interpretation).\n"
            "2. Share raw data and allocation calculations with all stakeholders.\n"
            "3. Conduct independent audit if required.\n"
            "4. Refer to agreed allocation methodology and regulatory requirements.\n"
            "5. Negotiate resolution and document outcome.\n"
            "6. Update allocation procedures if necessary."
        ),
        key_factors=[
            "Data transparency",
            "Auditability",
            "Methodology adherence",
            "Regulatory requirements",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "Joint Operating Agreement (JOA)",
            "API MPMS: Manual of Petroleum Measurement Standards"
        ],
        burden_holder="Asset Manager",
        adversary_position="Partners may challenge allocation for commercial reasons.",
        counter_arguments=[
            "Opaque allocation undermines trust.",
            "Transparent resolution supports partnership."
        ],
        resolution_strategy="Maintain open data access and regular audits.",
        entity_scope="All joint venture assets.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Production Allocation Dispute Resolution Procedure, 2020"
    ),
    DoctrineBlock(
        topic="Separator Emulsion Control",
        keywords=["separator", "emulsion", "control", "chemical", "temperature"],
        conclusion_template="Emulsion formation in separators is controlled by adjusting temperature, chemical dosing, and residence time.",
        reasoning_framework=(
            "1. Monitor separator performance for emulsion carryover.\n"
            "2. Adjust temperature to improve oil-water separation.\n"
            "3. Optimize chemical demulsifier dosing.\n"
            "4. Increase residence time if feasible.\n"
            "5. Sample and analyze emulsion properties regularly.\n"
            "6. Update control strategies as fluid properties change."
        ),
        key_factors=[
            "Emulsion monitoring",
            "Temperature control",
            "Chemical dosing",
            "Residence time",
            "Fluid property changes"
        ],
        primary_authority=[
            "API RP 12J: Oil and Gas Separator Design",
            "SPE 174217: Facility Optimization Techniques"
        ],
        burden_holder="Facility Engineer",
        adversary_position="Operations may resist changes to chemical or temperature setpoints.",
        counter_arguments=[
            "Uncontrolled emulsions reduce oil recovery.",
            "Optimization reduces chemical costs."
        ],
        resolution_strategy="Integrate emulsion control into facility optimization workflows.",
        entity_scope="All production separators.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Separator Emulsion Control Guidelines, 2021"
    ),
    DoctrineBlock(
        topic="Produced Water Reuse and Recycling",
        keywords=["produced water", "reuse", "recycling", "treatment", "ESG"],
        conclusion_template="Produced water reuse and recycling is maximized by advanced treatment and integration into field water management strategies.",
        reasoning_framework=(
            "1. Analyze produced water quality and treatment requirements for reuse.\n"
            "2. Select advanced treatment technologies (membranes, filtration, chemical).\n"
            "3. Integrate treated water into field operations (e.g., waterflood, drilling).\n"
            "4. Monitor reuse rates and environmental impact.\n"
            "5. Document all reuse and recycling activities.\n"
            "6. Review and update strategies annually."
        ),
        key_factors=[
            "Water quality",
            "Treatment technology",
            "Reuse integration",
            "Environmental impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 45: Produced Water Management",
            "SPE 184200: Produced Water Treatment Technologies"
        ],
        burden_holder="Water Management Engineer",
        adversary_position="Operations may resist integration due to perceived complexity.",
        counter_arguments=[
            "Reuse reduces disposal costs and environmental impact.",
            "Advanced treatment enables field integration."
        ],
        resolution_strategy="Demonstrate cost and ESG benefits of reuse.",
        entity_scope="All facilities with produced water.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Produced Water Reuse Policy, 2021"
    ),
    DoctrineBlock(
        topic="Pipeline Integrity Management",
        keywords=["pipeline", "integrity", "management", "corrosion", "inspection"],
        conclusion_template="Pipeline integrity is maintained by regular inspection, corrosion monitoring, and timely repairs.",
        reasoning_framework=(
            "1. Schedule routine pipeline inspections (pigging, smart pigs, ultrasonic testing).\n"
            "2. Monitor for corrosion and mechanical damage.\n"
            "3. Implement corrosion inhibition programs.\n"
            "4. Repair or replace damaged sections promptly.\n"
            "5. Document all inspection and maintenance activities.\n"
            "6. Review integrity status annually."
        ),
        key_factors=[
            "Inspection frequency",
            "Corrosion monitoring",
            "Repair timeliness",
            "Documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 1160: Pipeline Integrity Management",
            "NACE SP0102: Pipeline Integrity Management"
        ],
        burden_holder="Pipeline Integrity Engineer",
        adversary_position="Operations may resist downtime for inspection.",
        counter_arguments=[
            "Unmanaged integrity risks lead to leaks and regulatory penalties.",
            "Proactive management reduces long-term costs."
        ],
        resolution_strategy="Integrate inspection with maintenance planning.",
        entity_scope="All production pipelines.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Pipeline Integrity Management System, 2020"
    ),
    DoctrineBlock(
        topic="Compressor Reliability and Maintenance",
        keywords=["compressor", "reliability", "maintenance", "downtime", "optimization"],
        conclusion_template="Compressor reliability is maximized by predictive maintenance, vibration monitoring, and timely overhauls.",
        reasoning_framework=(
            "1. Monitor compressor performance and vibration data.\n"
            "2. Implement predictive maintenance based on condition monitoring.\n"
            "3. Schedule routine overhauls and inspections.\n"
            "4. Document all maintenance activities and failures.\n"
            "5. Review reliability metrics and update maintenance plans.\n"
            "6. Train operators on early warning signs."
        ),
        key_factors=[
            "Condition monitoring",
            "Maintenance scheduling",
            "Failure tracking",
            "Operator training",
            "Reliability metrics"
        ],
        primary_authority=[
            "API 618: Reciprocating Compressor Standard",
            "SPE 180196: Compressor Reliability"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Operations may resist downtime for maintenance.",
        counter_arguments=[
            "Unplanned failures cause greater downtime.",
            "Predictive maintenance reduces total cost."
        ],
        resolution_strategy="Integrate reliability metrics into maintenance planning.",
        entity_scope="All production compressors.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Compressor Maintenance Program, 2021"
    ),
    DoctrineBlock(
        topic="Field Production Optimization Workflow",
        keywords=["field", "production optimization", "workflow", "multidisciplinary", "continuous improvement"],
        conclusion_template="Field production optimization is achieved through a structured, multidisciplinary workflow integrating surveillance, diagnosis, and intervention.",
        reasoning_framework=(
            "1. Establish multidisciplinary teams for surveillance and optimization.\n"
            "2. Monitor production data and identify underperforming wells.\n"
            "3. Diagnose root causes and prioritize interventions.\n"
            "4. Implement optimization actions and monitor results.\n"
            "5. Document all activities and lessons learned.\n"
            "6. Review workflow effectiveness and update regularly."
        ),
        key_factors=[
            "Team integration",
            "Surveillance data",
            "Diagnosis accuracy",
            "Intervention effectiveness",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 16746: Production Optimization Workflows",
            "API RP 11AR: Artificial Lift Selection"
        ],
        burden_holder="Production Optimization Team",
        adversary_position="Functional silos may resist multidisciplinary approach.",
        counter_arguments=[
            "Siloed workflows miss optimization opportunities.",
            "Integrated teams drive continuous improvement."
        ],
        resolution_strategy="Formalize workflow and incentivize collaboration.",
        entity_scope="All production assets.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Field Production Optimization Workflow, 2020"
    ),
    DoctrineBlock(
        topic="Production Forecasting and Decline Analysis",
        keywords=["production forecasting", "decline analysis", "type curve", "optimization"],
        conclusion_template="Production forecasting is based on decline analysis, type curves, and integration with optimization plans.",
        reasoning_framework=(
            "1. Collect historical production data for each well.\n"
            "2. Fit decline models (exponential, hyperbolic, harmonic) to data.\n"
            "3. Validate model fit and adjust for operational changes.\n"
            "4. Integrate forecast with field optimization plans.\n"
            "5. Update forecasts as new data becomes available.\n"
            "6. Document assumptions and uncertainties."
        ),
        key_factors=[
            "Data quality",
            "Model selection",
            "Operational changes",
            "Forecast integration",
            "Uncertainty management"
        ],
        primary_authority=[
            "SPE 13344: Decline Curve Analysis",
            "API RP 11AR: Artificial Lift Selection"
        ],
        burden_holder="Reservoir Engineer",
        adversary_position="Production may challenge forecast assumptions.",
        counter_arguments=[
            "Unrealistic forecasts undermine planning.",
            "Transparent analysis supports optimization."
        ],
        resolution_strategy="Review forecasts with multidisciplinary teams.",
        entity_scope="All producing wells.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Production Forecasting Standard, 2021"
    ),
    DoctrineBlock(
        topic="Artificial Lift System Failure Analysis",
        keywords=["artificial lift", "failure analysis", "root cause", "downtime", "optimization"],
        conclusion_template="Artificial lift failures are analyzed systematically to identify root causes and implement corrective actions.",
        reasoning_framework=(
            "1. Record all artificial lift failures with time, cause, and impact.\n"
            "2. Categorize failures (mechanical, electrical, operational, etc.).\n"
            "3. Analyze trends and identify recurring issues.\n"
            "4. Develop corrective actions and update lift design as needed.\n"
            "5. Review effectiveness of actions and update failure database.\n"
            "6. Share lessons learned with field teams."
        ),
        key_factors=[
            "Failure categorization",
            "Root cause analysis",
            "Corrective action tracking",
            "Trend analysis",
            "Knowledge sharing"
        ],
        primary_authority=[
            "API RP 11S5: ESP System Operation",
            "SPE 16746: Rod Pump Optimization"
        ],
        burden_holder="Artificial Lift Engineer",
        adversary_position="Operations may underreport failures.",
        counter_arguments=[
            "Incomplete analysis leads to repeated failures.",
            "Systematic analysis improves reliability."
        ],
        resolution_strategy="Automate failure reporting and incentivize accurate data.",
        entity_scope="All artificial lift systems.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Artificial Lift Failure Analysis Program, 2020"
    ),
    DoctrineBlock(
        topic="Well Shut-in and Restart Procedures",
        keywords=["well shut-in", "restart", "procedure", "optimization", "integrity"],
        conclusion_template="Well shut-in and restart procedures are standardized to minimize production loss and maintain well integrity.",
        reasoning_framework=(
            "1. Develop standardized shut-in and restart procedures for all well types.\n"
            "2. Train field staff on procedures and rationale.\n"
            "3. Monitor well response during and after restart.\n"
            "4. Document all shut-in and restart events.\n"
            "5. Review procedures and update based on lessons learned."
        ),
        key_factors=[
            "Procedure standardization",
            "Staff training",
            "Monitoring",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "API RP 7G: Well Intervention and Workover Operations",
            "SPE 181705: Well Intervention Decision Framework"
        ],
        burden_holder="Production Operations Supervisor",
        adversary_position="Field staff may resist changes to established procedures.",
        counter_arguments=[
            "Inconsistent procedures increase risk of well damage.",
            "Standardization improves safety and efficiency."
        ],
        resolution_strategy="Integrate procedures into field manuals and provide refresher training.",
        entity_scope="All producing wells.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Well Shut-in and Restart Policy, 2019"
    ),
    DoctrineBlock(
        topic="Remote Production Monitoring and Control",
        keywords=["remote monitoring", "production control", "SCADA", "automation", "optimization"],
        conclusion_template="Remote production monitoring and control is implemented via SCADA and automation to enable real-time optimization.",
        reasoning_framework=(
            "1. Deploy SCADA systems for real-time data acquisition and control.\n"
            "2. Integrate field devices with central control room.\n"
            "3. Automate routine control actions (e.g., pump speed, valve position).\n"
            "4. Monitor system performance and reliability.\n"
            "5. Document all control actions and system changes.\n"
            "6. Review and update automation strategies regularly."
        ),
        key_factors=[
            "SCADA deployment",
            "Device integration",
            "Automation effectiveness",
            "System reliability",
            "Documentation"
        ],
        primary_authority=[
            "ISA-95: Enterprise-Control System Integration",
            "SPE 180196: Remote Production Optimization"
        ],
        burden_holder="Automation Engineer",
        adversary_position="Field staff may resist automation due to job security concerns.",
        counter_arguments=[
            "Manual control limits optimization potential.",
            "Automation improves efficiency and safety."
        ],
        resolution_strategy="Provide training and integrate automation with field workflows.",
        entity_scope="All production assets with remote monitoring.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Remote Production Monitoring Program, 2021"
    ),
    DoctrineBlock(
        topic="Production Optimization Under Reservoir Pressure Decline",
        keywords=["production optimization", "reservoir pressure decline", "artificial lift", "well intervention"],
        conclusion_template="Production is optimized under declining reservoir pressure by timely artificial lift upgrades and well interventions.",
        reasoning_framework=(
            "1. Monitor reservoir pressure trends and forecast decline.\n"
            "2. Assess well performance and identify candidates for artificial lift upgrades.\n"
            "3. Plan and execute well interventions to restore or enhance production.\n"
            "4. Evaluate economic impact of interventions and upgrades.\n"
            "5. Document all optimization activities and update field plans."
        ),
        key_factors=[
            "Reservoir pressure monitoring",
            "Artificial lift selection",
            "Intervention timing",
            "Economic analysis",
            "Documentation"
        ],
        primary_authority=[
            "SPE 16746: Production Optimization Techniques",
            "API RP 11AR: Artificial Lift Selection"
        ],
        burden_holder="Production Optimization Engineer",
        adversary_position="Budget constraints may delay upgrades.",
        counter_arguments=[
            "Delayed optimization leads to lost production.",
            "Timely upgrades maximize field value."
        ],
        resolution_strategy="Integrate optimization with reservoir management and justify with economic analysis.",
        entity_scope="All declining fields.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Reservoir Pressure Decline Optimization Policy, 2020"
    ),
    DoctrineBlock(
        topic="Artificial Lift System Selection for Unconventional Wells",
        keywords=["artificial lift", "unconventional wells", "selection", "optimization", "shale"],
        conclusion_template="Artificial lift for unconventional wells is selected based on reservoir deliverability, fluid properties, and completion design.",
        reasoning_framework=(
            "1. Analyze reservoir deliverability and expected production profile.\n"
            "2. Evaluate fluid properties (GOR, viscosity, sand content).\n"
            "3. Assess completion design and lateral length.\n"
            "4. Select lift system (e.g., ESP, rod pump, gas lift) based on well conditions.\n"
            "5. Monitor performance and adjust lift strategy as production declines.\n"
            "6. Document selection rationale and update field guidelines."
        ),
        key_factors=[
            "Reservoir deliverability",
            "Fluid properties",
            "Completion design",
            "Lift system adaptability",
            "Performance monitoring"
        ],
        primary_authority=[
            "SPE 16746: Artificial Lift in Unconventional Wells",
            "API RP 11AR: Artificial Lift Selection"
        ],
        burden_holder="Production Engineer",
        adversary_position="Operations may prefer standard lift systems for simplicity.",
        counter_arguments=[
            "Unconventional wells require tailored lift strategies.",
            "Adaptive selection maximizes recovery."
        ],
        resolution_strategy="Pilot multiple lift systems and update selection matrix.",
        entity_scope="All unconventional wells.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Unconventional Artificial Lift Selection Matrix, 2021"
    ),
    DoctrineBlock(
        topic="Well Surveillance Automation",
        keywords=["well surveillance", "automation", "data acquisition", "optimization"],
        conclusion_template="Well surveillance is automated to enable real-time optimization and reduce manual workload.",
        reasoning_framework=(
            "1. Deploy automated data acquisition systems on all producing wells.\n"
            "2. Integrate surveillance data with central databases and analytics tools.\n"
            "3. Automate routine surveillance tasks (e.g., rate calculation, alarm generation).\n"
            "4. Monitor system reliability and data quality.\n"
            "5. Review and update automation strategies regularly."
        ),
        key_factors=[
            "Data acquisition",
            "System integration",
            "Automation effectiveness",
            "Reliability",
            "Data quality"
        ],
        primary_authority=[
            "ISA-95: Enterprise-Control System Integration",
            "SPE 180196: Well Surveillance Automation"
        ],
        burden_holder="Production Surveillance Engineer",
        adversary_position="Field staff may resist automation due to job security concerns.",
        counter_arguments=[
            "Manual surveillance limits optimization.",
            "Automation improves efficiency and accuracy."
        ],
        resolution_strategy="Provide training and integrate automation with field workflows.",
        entity_scope="All producing wells.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Well Surveillance Automation Program, 2021"
    ),
    DoctrineBlock(
        topic="Field Production Optimization KPI Framework",
        keywords=["production optimization", "KPI", "framework", "performance", "continuous improvement"],
        conclusion_template="Field production optimization is tracked using a standardized KPI framework aligned with business objectives.",
        reasoning_framework=(
            "1. Define key performance indicators (KPIs) for production optimization (e.g., uptime, loss rate, OPEX/bbl).\n"
            "2. Align KPIs with business objectives and stakeholder requirements.\n"
            "3. Monitor and report KPIs regularly.\n"
            "4. Analyze trends and identify improvement opportunities.\n"
            "5. Review and update KPI framework annually."
        ),
        key_factors=[
            "KPI selection",
            "Business alignment",
            "Monitoring",
            "Reporting",
            "Continuous improvement"
        ],
        primary_authority=[
            "SPE 180196: Production Optimization KPIs",
            "API RP 11AR: Artificial Lift Selection"
        ],
        burden_holder="Production Optimization Manager",
        adversary_position="Field teams may resist new KPIs.",
        counter_arguments=[
            "Lack of KPIs limits performance tracking.",
            "Standardized KPIs drive improvement."
        ],
        resolution_strategy="Engage stakeholders in KPI selection and provide regular feedback.",
        entity_scope="All production assets.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Production Optimization KPI Framework, 2020"
    ),
    DoctrineBlock(
        topic="Production Optimization Opportunity Identification",
        keywords=["production optimization", "opportunity identification", "surveillance", "diagnosis"],
        conclusion_template="Optimization opportunities are identified through systematic surveillance, diagnosis, and multidisciplinary review.",
        reasoning_framework=(
            "1. Monitor production data for deviations from expected performance.\n"
            "2. Diagnose root causes of underperformance.\n"
            "3. Prioritize opportunities based on value, risk, and feasibility.\n"
            "4. Review opportunities with multidisciplinary teams.\n"
            "5. Document and track implementation and results."
        ),
        key_factors=[
            "Surveillance data",
            "Diagnosis accuracy",
            "Opportunity prioritization",
            "Multidisciplinary review",
            "Implementation tracking"
        ],
        primary_authority=[
            "SPE 16746: Production Optimization Techniques",
            "API RP 11AR: Artificial Lift Selection"
        ],
        burden_holder="Production Optimization Team",
        adversary_position="Functional silos may resist opportunity sharing.",
        counter_arguments=[
            "Missed opportunities reduce field value.",
            "Systematic identification maximizes optimization."
        ],
        resolution_strategy="Formalize opportunity identification in field workflows.",
        entity_scope="All production assets.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Production Optimization Opportunity Register, 2021"
    ),
    DoctrineBlock(
        topic="Artificial Lift System Automation",
        keywords=["artificial lift", "automation", "remote control", "optimization"],
        conclusion_template="Artificial lift systems are automated for remote control and real-time optimization.",
        reasoning_framework=(
            "1. Integrate artificial lift equipment with SCADA and automation systems.\n"
            "2. Automate routine control actions (e.g., speed, injection rate).\n"
            "3. Monitor performance and adjust parameters remotely.\n"
            "4. Document all control actions and system changes.\n"
            "5. Review automation effectiveness regularly."
        ),
        key_factors=[
            "System integration",
            "Control automation",
            "Performance monitoring",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "ISA-95: Enterprise-Control System Integration",
            "SPE 180196: Artificial Lift Automation"
        ],
        burden_holder="Artificial Lift Engineer",
        adversary_position="Field staff may resist automation due to job security concerns.",
        counter_arguments=[
            "Manual control limits optimization.",
            "Automation improves efficiency and reliability."
        ],
        resolution_strategy="Provide training and integrate automation with field workflows.",
        entity_scope="All artificial lift systems.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Artificial Lift Automation Program, 2021"
    ),
    DoctrineBlock(
        topic="Production Optimization Under Facility Constraints",
        keywords=["production optimization", "facility constraints", "bottleneck", "debottlenecking"],
        conclusion_template="Production is optimized under facility constraints by identifying bottlenecks and implementing debottlenecking projects.",
        reasoning_framework=(
            "1. Analyze facility performance and identify bottlenecks (e.g., separator, compressor, pipeline).\n"
            "2. Quantify impact of constraints on field production.\n"
            "3. Develop debottlenecking projects and prioritize based on value.\n"
            "4. Implement projects and monitor production response.\n"
            "5. Document all activities and update facility models."
        ),
        key_factors=[
            "Facility performance analysis",
            "Bottleneck identification",
            "Debottlenecking project value",
            "Implementation tracking",
            "Model updates"
        ],
        primary_authority=[
            "SPE 174217: Facility Optimization Techniques",
            "API RP 12J: Oil and Gas Separator Design"
        ],
        burden_holder="Facility Engineer",
        adversary_position="Budget constraints may delay debottlenecking.",
        counter_arguments=[
            "Unaddressed bottlenecks limit field value.",
            "Debottlenecking maximizes production."
        ],
        resolution_strategy="Justify projects with economic analysis and integrate with field planning.",
        entity_scope="All production facilities.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Facility Debottlenecking Program, 2020"
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