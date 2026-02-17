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
        topic="Diesel-Electric Locomotive Prime Movers",
        keywords=["prime mover", "diesel engine", "locomotive", "powerplant", "EMD", "GE", "horsepower"],
        conclusion_template="The prime mover selected must meet the operational, efficiency, and emissions requirements for the intended service profile.",
        reasoning_framework="""
Prime movers in diesel-electric locomotives are selected based on a balance of power output, fuel efficiency, emissions compliance, reliability, and maintenance requirements. The selection process involves evaluating the duty cycle (freight vs. passenger), expected load profiles, ambient conditions, and regulatory constraints (EPA Tier standards). Engine manufacturers such as EMD and GE provide models with varying cylinder counts, turbocharging, and electronic controls to optimize performance. The integration with the traction alternator/generator and compatibility with onboard systems is critical. Historical performance data, OEM technical bulletins, and fleet experience inform the final selection.
        """,
        key_factors=[
            "Horsepower rating",
            "Fuel consumption rate",
            "Emissions certification (EPA Tier)",
            "Reliability and mean time between failures",
            "Maintenance intervals and costs",
            "Compatibility with traction system",
            "Ambient operating conditions"
        ],
        primary_authority=[
            "OEM Technical Manuals (EMD, GE)",
            "EPA Locomotive Emissions Regulations",
            "AAR Recommended Practices"
        ],
        burden_holder="Locomotive manufacturer and operator",
        adversary_position="Alternative prime mover technologies (e.g., LNG, hybrid, battery-electric) may offer superior efficiency or emissions performance.",
        counter_arguments=[
            "Diesel-electric systems have proven reliability and established support infrastructure.",
            "Alternative technologies may not be mature or scalable for mainline operations.",
            "Total cost of ownership for alternatives is not yet competitive."
        ],
        resolution_strategy="Conduct a lifecycle cost analysis and emissions impact study, referencing OEM data and regulatory requirements.",
        entity_scope="North American mainline locomotives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="EPA Tier 4 Locomotive Emissions Standards"
    ),
    DoctrineBlock(
        topic="AC vs DC Traction Systems",
        keywords=["traction motors", "AC", "DC", "inverter", "locomotive", "efficiency", "maintenance"],
        conclusion_template="AC traction systems are preferred for heavy-haul and high-adhesion applications, while DC systems remain viable for certain legacy and light-duty operations.",
        reasoning_framework="""
The choice between AC and DC traction systems is determined by performance requirements, lifecycle costs, and operational context. AC traction motors, controlled by inverters, offer superior adhesion, lower maintenance, and better performance under slip conditions. DC systems, while less expensive upfront, require more frequent maintenance (brushes, commutators) and are less tolerant of wheel slip. The transition to AC has been driven by advances in power electronics and the need for higher tractive effort in heavy-haul freight. Fleet standardization, crew familiarity, and maintenance infrastructure also influence the decision.
        """,
        key_factors=[
            "Adhesion and tractive effort",
            "Maintenance requirements",
            "Initial and lifecycle costs",
            "Operational environment",
            "Power electronics reliability",
            "Fleet standardization"
        ],
        primary_authority=[
            "IEEE Std 16-2004",
            "AAR Locomotive Committee Reports",
            "OEM Technical Bulletins"
        ],
        burden_holder="Locomotive purchaser/operator",
        adversary_position="DC systems are simpler and less costly, and may suffice for certain applications.",
        counter_arguments=[
            "AC systems reduce wheel slip and increase haulage capacity.",
            "Long-term maintenance savings favor AC.",
            "DC systems face obsolescence and parts scarcity."
        ],
        resolution_strategy="Evaluate total cost of ownership and operational requirements; pilot AC units in representative service.",
        entity_scope="Freight and passenger locomotives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Class I railroad fleet conversions (1990s-present)"
    ),
    DoctrineBlock(
        topic="Dynamic Braking Systems",
        keywords=["dynamic brake", "regenerative", "rheostatic", "traction motor", "braking effort"],
        conclusion_template="Dynamic braking is essential for controlling train speed on grades and reducing wear on friction brakes.",
        reasoning_framework="""
Dynamic braking converts the kinetic energy of the train into electrical energy via the traction motors operating as generators. This energy is dissipated as heat in resistor grids (rheostatic) or, in some advanced systems, returned to the grid (regenerative). The effectiveness of dynamic braking depends on the design of the traction system, the resistor grid capacity, and the train's speed. Dynamic brakes reduce the load on air brakes, extending their life and improving safety on long descents. System monitoring and proper crew training are critical to prevent overheating and ensure safe operation.
        """,
        key_factors=[
            "Dynamic brake effort curve",
            "Resistor grid capacity and cooling",
            "Integration with air brake system",
            "Speed dependency",
            "Crew training and procedures"
        ],
        primary_authority=[
            "OEM Locomotive Manuals",
            "AAR Brake System Standards",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive operator and crew",
        adversary_position="Dynamic brakes add complexity and maintenance; not all routes require them.",
        counter_arguments=[
            "Dynamic brakes are critical for mountainous and heavy-haul operations.",
            "Reduced friction brake wear lowers maintenance costs.",
            "Modern systems are highly reliable."
        ],
        resolution_strategy="Mandate dynamic brakes for routes with significant grades; monitor system health and provide crew training.",
        entity_scope="Mainline freight and passenger locomotives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Safety Advisory 2016-01"
    ),
    DoctrineBlock(
        topic="Air Brake Systems - 26-L and CCBII",
        keywords=["air brake", "26-L", "CCBII", "pneumatic", "electronic", "brake pipe", "locomotive"],
        conclusion_template="Both 26-L and CCBII air brake systems must meet FRA safety standards, with CCBII offering enhanced diagnostics and control.",
        reasoning_framework="""
The 26-L pneumatic air brake system has been the industry standard for decades, providing reliable control via mechanical valves and relays. The CCBII (Computer Controlled Brake II) system introduces electronic control and diagnostics, enabling faster response, self-testing, and integration with trainline communications. Both systems must comply with FRA Part 229 and AAR standards. Transitioning to CCBII requires crew training and infrastructure upgrades but yields operational and safety benefits. Maintenance practices differ, with CCBII requiring specialized diagnostic tools.
        """,
        key_factors=[
            "Compliance with FRA Part 229",
            "Response time and control precision",
            "Diagnostic capabilities",
            "Crew training requirements",
            "Maintenance infrastructure"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229",
            "AAR S-4200",
            "OEM Brake System Manuals"
        ],
        burden_holder="Railroad operator",
        adversary_position="Legacy 26-L systems are proven and simpler to maintain; electronic systems may introduce new failure modes.",
        counter_arguments=[
            "CCBII improves safety and operational efficiency.",
            "Electronic diagnostics reduce troubleshooting time.",
            "Redundancy and fail-safes mitigate new risks."
        ],
        resolution_strategy="Phase in CCBII systems with comprehensive training and support; maintain legacy systems where justified.",
        entity_scope="North American locomotive fleets",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Locomotive Safety Standards"
    ),
    DoctrineBlock(
        topic="Electronically Controlled Pneumatic (ECP) Brakes",
        keywords=["ECP brakes", "trainline", "brake control", "safety", "response time", "distributed power"],
        conclusion_template="ECP brakes provide superior train control and safety, especially for long and heavy trains, but require significant investment in rolling stock and infrastructure.",
        reasoning_framework="""
ECP brakes use electronic signals to control brake application and release simultaneously throughout the train, eliminating the delay inherent in pneumatic propagation. This results in shorter stopping distances, improved train handling, and better integration with distributed power. ECP systems also enable real-time health monitoring and predictive maintenance. However, widespread adoption is limited by the need to retrofit rolling stock and the lack of interoperability with conventional brake systems. Regulatory incentives and industry standards are evolving to support ECP deployment.
        """,
        key_factors=[
            "Brake application and release time",
            "Train length and weight",
            "Interoperability with legacy systems",
            "Cost of retrofitting",
            "Regulatory environment"
        ],
        primary_authority=[
            "FRA ECP Brake Waivers",
            "AAR S-4200",
            "OEM ECP System Manuals"
        ],
        burden_holder="Railroad operator and equipment owner",
        adversary_position="High retrofit costs and interoperability issues hinder ECP adoption.",
        counter_arguments=[
            "ECP improves safety and reduces accident risk.",
            "Long-term operational savings offset upfront costs.",
            "Regulatory incentives may accelerate adoption."
        ],
        resolution_strategy="Target ECP deployment on unit trains and high-risk routes; pursue grants and regulatory waivers.",
        entity_scope="Unit trains, hazardous materials, heavy-haul",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="FRA ECP Brake Pilot Programs"
    ),
    DoctrineBlock(
        topic="Distributed Power and LOCOTROL",
        keywords=["distributed power", "DP", "LOCOTROL", "train handling", "radio control", "in-train forces"],
        conclusion_template="Distributed power systems, such as LOCOTROL, are essential for managing in-train forces and improving operational efficiency on long trains.",
        reasoning_framework="""
Distributed power (DP) systems enable remote control of locomotives placed throughout the train, reducing in-train forces, improving braking response, and enhancing fuel efficiency. LOCOTROL is the industry standard DP system, using radio communication to synchronize power and brake commands. DP is especially beneficial on long, heavy trains and in mountainous territory. Implementation requires compatible locomotives, crew training, and robust radio infrastructure. DP also facilitates ECP brake integration and supports Positive Train Control (PTC) systems.
        """,
        key_factors=[
            "Train length and configuration",
            "Radio communication reliability",
            "Locomotive compatibility",
            "Crew training",
            "Integration with braking and PTC systems"
        ],
        primary_authority=[
            "OEM LOCOTROL Manuals",
            "AAR DP Guidelines",
            "FRA Safety Advisories"
        ],
        burden_holder="Railroad operator",
        adversary_position="DP systems add complexity and require significant investment in equipment and training.",
        counter_arguments=[
            "DP reduces derailment risk and improves train handling.",
            "Operational savings and increased capacity justify investment.",
            "Industry experience demonstrates reliability."
        ],
        resolution_strategy="Deploy DP on long and heavy trains; maintain conventional operations where justified by cost-benefit analysis.",
        entity_scope="Freight railroads, especially Class I",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AAR DP Implementation Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Fuel Systems and Fuel Efficiency",
        keywords=["fuel system", "fuel efficiency", "consumption", "injection", "prime mover", "emissions"],
        conclusion_template="Optimizing locomotive fuel systems is critical for reducing operating costs and meeting emissions standards.",
        reasoning_framework="""
Locomotive fuel systems encompass storage, delivery, filtration, and injection components. Modern systems employ electronic fuel injection and advanced filtration to maximize combustion efficiency and minimize emissions. Fuel efficiency is influenced by duty cycle, idle reduction technologies, and operator practices. Compliance with EPA emissions standards requires precise control of fuel delivery and combustion parameters. Regular maintenance and use of high-quality fuel are essential for system reliability and longevity.
        """,
        key_factors=[
            "Fuel injection technology",
            "Idle reduction systems",
            "Fuel quality and filtration",
            "Maintenance practices",
            "Operator training"
        ],
        primary_authority=[
            "OEM Fuel System Manuals",
            "EPA Locomotive Emissions Regulations",
            "AAR Recommended Practices"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Fuel system upgrades are costly and may not yield immediate savings.",
        counter_arguments=[
            "Long-term fuel savings and emissions compliance justify investment.",
            "Idle reduction reduces both fuel use and engine wear.",
            "Regulatory penalties for non-compliance are significant."
        ],
        resolution_strategy="Implement fuel management programs and monitor system performance; prioritize upgrades for high-utilization units.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="EPA Tier 4 Fuel System Requirements"
    ),
    DoctrineBlock(
        topic="Locomotive Cooling Systems",
        keywords=["cooling system", "radiator", "fan", "thermal management", "prime mover", "overheating"],
        conclusion_template="Effective cooling system design and maintenance are essential for locomotive reliability and performance.",
        reasoning_framework="""
Locomotive cooling systems regulate engine temperature through radiators, fans, thermostats, and coolant pumps. Overheating can lead to engine damage, reduced efficiency, and emissions violations. Modern systems use electronically controlled fans and temperature sensors to optimize cooling and reduce parasitic losses. Regular inspection for leaks, blockages, and coolant quality is critical. Cooling system failures are a leading cause of locomotive downtime and must be addressed proactively.
        """,
        key_factors=[
            "Radiator and fan design",
            "Coolant quality and level",
            "Sensor and control system reliability",
            "Maintenance intervals",
            "Ambient temperature extremes"
        ],
        primary_authority=[
            "OEM Cooling System Manuals",
            "AAR Maintenance Standards",
            "EPA Emissions Compliance"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Advanced cooling systems may increase maintenance complexity and costs.",
        counter_arguments=[
            "Improved cooling reduces engine wear and emissions.",
            "Electronic controls enable predictive maintenance.",
            "Downtime due to overheating is more costly than preventive maintenance."
        ],
        resolution_strategy="Adopt predictive maintenance and regular inspection schedules; upgrade controls where feasible.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Maintenance Rule 236"
    ),
    DoctrineBlock(
        topic="Turbocharger Systems",
        keywords=["turbocharger", "boost", "prime mover", "efficiency", "power output", "maintenance"],
        conclusion_template="Turbocharger systems are critical for maximizing locomotive engine power and efficiency, but require diligent maintenance.",
        reasoning_framework="""
Turbochargers increase the amount of air supplied to the engine, enabling higher power output and improved fuel efficiency. Locomotive turbochargers are subject to high thermal and mechanical stresses, necessitating regular inspection and maintenance. Failure modes include bearing wear, oil contamination, and turbine damage. Turbocharger performance directly affects emissions and engine reliability. Upgrades to variable geometry or electronically controlled turbochargers can yield further efficiency gains.
        """,
        key_factors=[
            "Turbocharger design and control",
            "Maintenance intervals",
            "Oil quality and filtration",
            "Failure detection systems",
            "Integration with engine management"
        ],
        primary_authority=[
            "OEM Turbocharger Manuals",
            "AAR Recommended Practices",
            "EPA Emissions Standards"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Turbocharger failures can cause catastrophic engine damage and increase maintenance costs.",
        counter_arguments=[
            "Routine maintenance and monitoring mitigate failure risks.",
            "Efficiency gains offset maintenance costs.",
            "OEM support and parts availability are robust."
        ],
        resolution_strategy="Implement condition-based maintenance and oil analysis; train personnel in turbocharger diagnostics.",
        entity_scope="All turbocharged diesel locomotives",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="AAR Turbocharger Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Wheel-Rail Adhesion and Creep Control",
        keywords=["adhesion", "creep control", "wheel slip", "traction", "sanding", "AC traction"],
        conclusion_template="Effective adhesion management is essential for maximizing tractive effort and minimizing wheel and rail wear.",
        reasoning_framework="""
Wheel-rail adhesion is influenced by rail condition, weather, locomotive weight, and traction control systems. Modern AC traction systems employ creep control algorithms to maintain optimal slip for maximum tractive effort. Sanding systems provide additional adhesion when needed. Monitoring wheel slip and integrating with train handling systems reduces derailment risk and improves fuel efficiency. Regular inspection of wheels, rails, and traction control hardware is necessary for reliable operation.
        """,
        key_factors=[
            "Traction control system design",
            "Sanding system effectiveness",
            "Wheel and rail condition",
            "Weather and environmental factors",
            "Operator technique"
        ],
        primary_authority=[
            "OEM Traction Control Manuals",
            "AAR Adhesion Standards",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Adhesion control systems add complexity and may be prone to false positives or failures.",
        counter_arguments=[
            "Advanced systems improve safety and reduce wear.",
            "Operator training mitigates misuse.",
            "Redundancy and diagnostics enhance reliability."
        ],
        resolution_strategy="Adopt best practices for wheel-rail interface management; invest in advanced traction control where justified.",
        entity_scope="All mainline locomotives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAR Adhesion Control Guidelines"
    ),
    DoctrineBlock(
        topic="FRA Part 229 Locomotive Safety Standards",
        keywords=["FRA", "Part 229", "locomotive safety", "inspection", "compliance", "regulations"],
        conclusion_template="Locomotives must comply with all FRA Part 229 requirements to operate in revenue service.",
        reasoning_framework="""
FRA Part 229 establishes minimum safety standards for locomotive design, inspection, maintenance, and operation. Key provisions include daily and periodic inspections, event recorders, cab safety, brake systems, and lighting. Non-compliance can result in fines, service interruptions, and increased accident risk. Compliance is verified through documentation, inspection records, and periodic audits. Operators must ensure all personnel are trained and that maintenance programs meet or exceed regulatory requirements.
        """,
        key_factors=[
            "Inspection frequency and thoroughness",
            "Recordkeeping and documentation",
            "Personnel training",
            "Corrective action procedures",
            "Audit readiness"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229",
            "AAR Safety Standards",
            "OEM Compliance Bulletins"
        ],
        burden_holder="Railroad operator",
        adversary_position="Compliance imposes administrative and operational burdens.",
        counter_arguments=[
            "Safety and regulatory compliance are non-negotiable.",
            "Proactive compliance reduces accident risk and liability.",
            "Modern recordkeeping systems streamline compliance."
        ],
        resolution_strategy="Implement robust compliance management systems and regular training; conduct internal audits.",
        entity_scope="All US railroads operating locomotives",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FRA Enforcement Actions"
    ),
    DoctrineBlock(
        topic="Positive Train Control (PTC)",
        keywords=["PTC", "positive train control", "safety", "collision avoidance", "FRA", "interoperability"],
        conclusion_template="PTC is mandatory for most mainline operations and must be fully interoperable and maintained to FRA standards.",
        reasoning_framework="""
Positive Train Control (PTC) is a federally mandated safety overlay system designed to prevent train-to-train collisions, overspeed derailments, and unauthorized train movements. PTC systems integrate GPS, wireless communications, onboard computers, and wayside devices. Implementation challenges include interoperability across railroads, system reliability, and integration with legacy equipment. FRA regulations specify performance, testing, and maintenance requirements. Continuous monitoring and periodic updates are necessary to maintain compliance and effectiveness.
        """,
        key_factors=[
            "System interoperability",
            "Reliability and fail-safe operation",
            "Integration with existing equipment",
            "Crew training and procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236 Subpart I",
            "AAR PTC Standards",
            "OEM PTC Manuals"
        ],
        burden_holder="Railroad operator",
        adversary_position="PTC implementation is costly and complex, with ongoing maintenance burdens.",
        counter_arguments=[
            "PTC significantly reduces accident risk.",
            "Federal funding and grants are available.",
            "Long-term operational benefits outweigh costs."
        ],
        resolution_strategy="Leverage industry partnerships for interoperability; invest in crew training and system monitoring.",
        entity_scope="US mainline railroads",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Rail Safety Improvement Act of 2008"
    ),
    DoctrineBlock(
        topic="Event Recorder Data Analysis",
        keywords=["event recorder", "data analysis", "accident investigation", "FRA", "compliance", "download"],
        conclusion_template="Event recorder data must be preserved, analyzed, and reported in accordance with FRA regulations.",
        reasoning_framework="""
Locomotive event recorders capture critical operational data, including speed, throttle position, brake applications, and crew actions. FRA regulations require event recorders to meet survivability and data retention standards. Data analysis is essential for accident investigation, compliance verification, and performance monitoring. Secure data download, chain of custody, and timely reporting are mandatory. Advanced analytics can identify trends and support proactive safety management.
        """,
        key_factors=[
            "Data retention and survivability",
            "Download and analysis procedures",
            "Chain of custody",
            "Compliance with FRA standards",
            "Integration with safety management systems"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229.135",
            "AAR Event Recorder Guidelines",
            "OEM Event Recorder Manuals"
        ],
        burden_holder="Railroad operator and accident investigators",
        adversary_position="Event recorder management adds administrative burden and may raise privacy concerns.",
        counter_arguments=[
            "Event recorders are critical for safety and compliance.",
            "Automated systems streamline data management.",
            "Privacy is protected by regulatory controls."
        ],
        resolution_strategy="Automate event recorder data management and ensure secure storage; train personnel in analysis procedures.",
        entity_scope="All FRA-regulated locomotives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Event Recorder Final Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Weight and Tractive Effort Calculations",
        keywords=["weight", "tractive effort", "adhesion", "axle load", "drawbar pull", "calculations"],
        conclusion_template="Locomotive weight and tractive effort must be matched to service requirements and track infrastructure limits.",
        reasoning_framework="""
The relationship between locomotive weight, axle load, and tractive effort determines the ability to start and move trains without excessive wheel slip or track damage. Calculations must account for adhesion limits, grade, curve resistance, and train length. Overweight locomotives may exceed track structure limits, while underweight units may lack sufficient tractive effort. Proper balancing ensures safe and efficient operations. Regulatory and infrastructure constraints must be observed.
        """,
        key_factors=[
            "Locomotive weight and axle load",
            "Adhesion coefficient",
            "Grade and curvature",
            "Train length and tonnage",
            "Track infrastructure limits"
        ],
        primary_authority=[
            "AAR Manual of Standards and Recommended Practices",
            "OEM Locomotive Data Sheets",
            "FRA Track Safety Standards"
        ],
        burden_holder="Locomotive designer and operator",
        adversary_position="Overly conservative calculations may limit operational flexibility.",
        counter_arguments=[
            "Safety and infrastructure protection are paramount.",
            "Optimized calculations maximize efficiency within safe limits.",
            "Modern simulation tools improve accuracy."
        ],
        resolution_strategy="Use validated calculation methods and consult infrastructure owners; review regularly as conditions change.",
        entity_scope="All mainline locomotives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AAR Tractive Effort Calculation Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Emissions Standards (EPA Tier 0-4)",
        keywords=["emissions", "EPA", "Tier 0", "Tier 4", "NOx", "PM", "compliance"],
        conclusion_template="Locomotives must meet or be upgraded to the applicable EPA Tier emissions standard for their build date and service.",
        reasoning_framework="""
EPA emissions standards for locomotives are divided into Tiers 0 through 4, with increasing stringency for NOx, PM, and other pollutants. Compliance is based on build date, remanufacture status, and service type. Upgrades may include engine modifications, aftertreatment systems, and electronic controls. Non-compliance can result in fines and operational restrictions. Recordkeeping and periodic testing are required. Fleet strategies may involve targeted upgrades or replacement of older units.
        """,
        key_factors=[
            "Locomotive build date and status",
            "Emissions certification",
            "Upgrade feasibility and cost",
            "Recordkeeping and testing",
            "Operational impact"
        ],
        primary_authority=[
            "EPA 40 CFR Part 1033",
            "OEM Emissions Compliance Bulletins",
            "AAR Environmental Standards"
        ],
        burden_holder="Locomotive owner/operator",
        adversary_position="Upgrading older locomotives is costly and may not be technically feasible.",
        counter_arguments=[
            "Regulatory penalties for non-compliance are significant.",
            "Targeted upgrades can maximize return on investment.",
            "Replacement may be more cost-effective for some units."
        ],
        resolution_strategy="Develop a fleet emissions compliance plan; prioritize upgrades based on age, usage, and cost-benefit analysis.",
        entity_scope="All US locomotives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="EPA Locomotive Emissions Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Maintenance Programs (FRA 229 Compliance)",
        keywords=["maintenance", "FRA 229", "inspection", "preventive", "corrective", "recordkeeping"],
        conclusion_template="Locomotive maintenance programs must ensure compliance with FRA 229 and support safe, reliable operations.",
        reasoning_framework="""
FRA 229 requires regular inspection and maintenance of locomotives, including daily, periodic, and annual checks. Maintenance programs should be preventive, data-driven, and documented. Key components include brake systems, safety appliances, event recorders, and prime movers. Non-compliance increases accident risk and liability. Modern programs use computerized maintenance management systems (CMMS) to track work and ensure timely inspections. Training and accountability are essential.
        """,
        key_factors=[
            "Inspection intervals and thoroughness",
            "Documentation and recordkeeping",
            "Personnel training",
            "Use of CMMS",
            "Corrective action procedures"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229",
            "AAR Maintenance Standards",
            "OEM Maintenance Manuals"
        ],
        burden_holder="Railroad operator and maintenance personnel",
        adversary_position="Maintenance programs are resource-intensive and may disrupt operations.",
        counter_arguments=[
            "Preventive maintenance reduces unplanned downtime.",
            "Regulatory compliance is mandatory.",
            "CMMS improves efficiency and accountability."
        ],
        resolution_strategy="Implement CMMS and regular training; audit maintenance practices for continuous improvement.",
        entity_scope="All US railroads",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FRA Locomotive Maintenance Enforcement"
    ),
    DoctrineBlock(
        topic="Locomotive Cab Ergonomics and Human Factors",
        keywords=["cab design", "ergonomics", "human factors", "crew comfort", "safety", "controls"],
        conclusion_template="Cab design must prioritize crew safety, comfort, and operational efficiency, following human factors engineering principles.",
        reasoning_framework="""
Locomotive cab ergonomics directly impact crew performance, fatigue, and safety. Key considerations include control layout, visibility, seating, climate control, and noise reduction. Human factors engineering standards guide the placement of displays, switches, and emergency equipment. Compliance with FRA cab safety rules is mandatory. Regular feedback from operating crews and post-incident reviews inform continuous improvement. Upgrades to lighting, HVAC, and noise insulation enhance crew well-being and reduce error rates.
        """,
        key_factors=[
            "Control layout and accessibility",
            "Visibility and sightlines",
            "Seating and comfort",
            "Climate control and noise reduction",
            "Compliance with safety standards"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229 Subpart B",
            "AAR Human Factors Guidelines",
            "OEM Cab Design Manuals"
        ],
        burden_holder="Locomotive designer and operator",
        adversary_position="Ergonomic upgrades increase design and retrofit costs.",
        counter_arguments=[
            "Improved ergonomics reduce fatigue and accidents.",
            "Crew retention and satisfaction are improved.",
            "Long-term savings from reduced incidents."
        ],
        resolution_strategy="Incorporate crew feedback and human factors standards in design and retrofits.",
        entity_scope="All new and existing locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Cab Safety Rules"
    ),
    DoctrineBlock(
        topic="Locomotive Crashworthiness Standards",
        keywords=["crashworthiness", "cab structure", "collision", "FRA", "energy absorption", "safety"],
        conclusion_template="Locomotive crashworthiness standards must be met to protect crew in collision scenarios.",
        reasoning_framework="""
Crashworthiness standards specify structural requirements for locomotive cabs, including collision posts, energy-absorbing elements, and anti-climbing devices. FRA regulations mandate testing and certification for new designs. Retrofitting older units may be required for certain service types. Compliance reduces crew injury risk and liability in the event of a collision. Design trade-offs include weight, cost, and operational impact. Regular inspection and maintenance of crashworthy features are essential.
        """,
        key_factors=[
            "Cab structure and energy absorption",
            "Compliance with FRA standards",
            "Testing and certification",
            "Retrofitting feasibility",
            "Inspection and maintenance"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229 Subpart D",
            "AAR Crashworthiness Guidelines",
            "OEM Structural Design Manuals"
        ],
        burden_holder="Locomotive manufacturer and operator",
        adversary_position="Crashworthy designs increase weight and cost; retrofitting is challenging.",
        counter_arguments=[
            "Crew safety is paramount.",
            "Regulatory compliance is mandatory.",
            "Design innovations can minimize weight impact."
        ],
        resolution_strategy="Adopt crashworthy designs for new builds; prioritize retrofits based on risk assessment.",
        entity_scope="All new and high-risk locomotives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Locomotive Crashworthiness Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Lighting and Visibility Standards",
        keywords=["lighting", "visibility", "headlights", "ditch lights", "FRA", "safety"],
        conclusion_template="Locomotive lighting systems must meet FRA standards for visibility and safety.",
        reasoning_framework="""
FRA regulations specify requirements for locomotive headlights, ditch lights, marker lights, and reflective materials. Proper lighting enhances visibility at crossings and in adverse weather, reducing accident risk. Maintenance includes regular inspection, bulb replacement, and aiming adjustments. Upgrades to LED technology improve reliability and energy efficiency. Non-compliance can result in fines and increased liability.
        """,
        key_factors=[
            "Headlight and ditch light intensity",
            "Placement and aiming",
            "Reflective materials",
            "Maintenance and inspection",
            "Compliance with FRA standards"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229 Subpart A",
            "AAR Lighting Guidelines",
            "OEM Lighting Manuals"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Lighting upgrades increase costs and may require electrical system modifications.",
        counter_arguments=[
            "Improved visibility reduces accidents.",
            "LED upgrades lower long-term maintenance costs.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Adopt LED lighting and regular inspection schedules; ensure compliance with aiming and intensity standards.",
        entity_scope="All US locomotives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Locomotive Lighting Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Horn and Bell Standards",
        keywords=["horn", "bell", "audible warning", "FRA", "safety", "crossings"],
        conclusion_template="Locomotive horns and bells must meet FRA audibility and operational standards for safety.",
        reasoning_framework="""
FRA rules specify minimum sound levels and operational requirements for locomotive horns and bells. Proper use is critical at grade crossings and in yard operations. Maintenance includes regular testing, adjustment, and repair. Failure to comply increases accident risk and liability. Community noise concerns may require use of quiet zones, but only with approved supplemental safety measures.
        """,
        key_factors=[
            "Sound level and frequency",
            "Operational procedures",
            "Maintenance and testing",
            "Compliance with quiet zone rules",
            "Crew training"
        ],
        primary_authority=[
            "FRA 49 CFR Part 222",
            "AAR Audible Warning Guidelines",
            "OEM Horn and Bell Manuals"
        ],
        burden_holder="Locomotive operator and crew",
        adversary_position="Noise complaints and quiet zone restrictions complicate compliance.",
        counter_arguments=[
            "Audible warnings are essential for safety.",
            "Quiet zones require supplemental safety measures.",
            "Regular testing ensures reliability."
        ],
        resolution_strategy="Maintain compliance through regular testing and crew training; coordinate with communities on quiet zones.",
        entity_scope="All US locomotives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Locomotive Horn Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Sanding Systems",
        keywords=["sanding", "adhesion", "wheel slip", "traction", "maintenance", "safety"],
        conclusion_template="Sanding systems are critical for maintaining adhesion and safe operation, especially in low-adhesion conditions.",
        reasoning_framework="""
Sanding systems deliver sand to the rail ahead of the wheels to increase friction and reduce wheel slip. Proper operation and maintenance are essential for effectiveness. System failures can lead to loss of traction, increased wheel wear, and derailment risk. Modern systems may be automated and integrated with traction control. Regular inspection and refilling are required, especially in adverse weather.
        """,
        key_factors=[
            "System design and reliability",
            "Integration with traction control",
            "Maintenance and inspection",
            "Sand quality and supply",
            "Operator training"
        ],
        primary_authority=[
            "AAR Sanding System Guidelines",
            "OEM Sanding System Manuals",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Sanding increases rail and wheel wear; system failures can go unnoticed.",
        counter_arguments=[
            "Properly managed sanding minimizes wear and maximizes safety.",
            "Automated systems improve reliability.",
            "Regular inspection prevents unnoticed failures."
        ],
        resolution_strategy="Implement regular inspection and maintenance; upgrade to automated systems where feasible.",
        entity_scope="All mainline locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Sanding System Standards"
    ),
    DoctrineBlock(
        topic="Locomotive HVAC and Climate Control",
        keywords=["HVAC", "climate control", "crew comfort", "safety", "maintenance"],
        conclusion_template="Effective HVAC systems are essential for crew comfort, safety, and regulatory compliance.",
        reasoning_framework="""
HVAC systems regulate cab temperature and air quality, directly affecting crew alertness and safety. FRA standards require functional heating and ventilation. Air conditioning is increasingly standard, especially in extreme climates. Maintenance includes filter replacement, refrigerant checks, and system diagnostics. Malfunctioning HVAC can lead to crew fatigue and regulatory violations.
        """,
        key_factors=[
            "System reliability and capacity",
            "Maintenance and inspection",
            "Air quality and filtration",
            "Compliance with FRA standards",
            "Crew feedback"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229.119",
            "AAR HVAC Guidelines",
            "OEM HVAC Manuals"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="HVAC systems add complexity and maintenance costs.",
        counter_arguments=[
            "Crew comfort and safety are critical.",
            "Proper maintenance reduces failure rates.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Implement preventive maintenance and crew reporting; upgrade systems in extreme climates.",
        entity_scope="All US locomotives",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Locomotive Cab Standards"
    ),
    DoctrineBlock(
        topic="Locomotive Battery and Electrical Systems",
        keywords=["battery", "electrical system", "starting", "auxiliary power", "maintenance"],
        conclusion_template="Reliable battery and electrical systems are essential for locomotive starting, control, and safety.",
        reasoning_framework="""
Locomotive batteries provide starting power and support auxiliary systems. Electrical systems include charging, distribution, and protection components. Failures can result in no-start, loss of control, or safety system outages. Regular inspection, load testing, and preventive maintenance are necessary. Upgrades to sealed or maintenance-free batteries can improve reliability. Compliance with OEM and AAR standards is required.
        """,
        key_factors=[
            "Battery type and capacity",
            "Charging system reliability",
            "Maintenance and inspection",
            "Electrical protection devices",
            "Compliance with standards"
        ],
        primary_authority=[
            "AAR Electrical System Standards",
            "OEM Electrical System Manuals",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Battery upgrades and electrical diagnostics increase maintenance costs.",
        counter_arguments=[
            "Improved reliability reduces downtime.",
            "Preventive maintenance extends battery life.",
            "Safety-critical systems depend on electrical reliability."
        ],
        resolution_strategy="Adopt preventive maintenance and consider battery upgrades; train personnel in diagnostics.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAR Electrical System Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Fire Detection and Suppression",
        keywords=["fire detection", "suppression", "safety", "engine compartment", "FRA", "maintenance"],
        conclusion_template="Fire detection and suppression systems are critical for crew safety and asset protection, especially in high-risk environments.",
        reasoning_framework="""
Locomotive fire detection systems monitor engine compartments and other high-risk areas for smoke, heat, or flame. Suppression systems may be automatic or manual, using agents such as foam or dry chemical. FRA and AAR standards specify requirements for certain service types. Regular inspection, testing, and crew training are essential. System failures can result in catastrophic loss and regulatory penalties.
        """,
        key_factors=[
            "System design and coverage",
            "Detection and response time",
            "Maintenance and inspection",
            "Crew training",
            "Compliance with standards"
        ],
        primary_authority=[
            "AAR Fire Safety Standards",
            "OEM Fire Suppression Manuals",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Fire suppression systems add cost and complexity; false alarms can disrupt operations.",
        counter_arguments=[
            "Fire risk justifies investment.",
            "Proper maintenance minimizes false alarms.",
            "Insurance and regulatory benefits."
        ],
        resolution_strategy="Implement regular inspection and crew training; prioritize high-risk units for upgrades.",
        entity_scope="All new and high-risk locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Fire Safety Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Remote Monitoring and Telematics",
        keywords=["remote monitoring", "telematics", "predictive maintenance", "data analytics", "fleet management"],
        conclusion_template="Remote monitoring and telematics systems enhance fleet management and predictive maintenance capabilities.",
        reasoning_framework="""
Telematics systems collect and transmit real-time data on locomotive health, location, and performance. Predictive analytics enable early detection of faults, reducing unplanned downtime. Integration with maintenance management systems streamlines scheduling and parts inventory. Data security and privacy must be managed. Investment in telematics yields operational savings and improved reliability.
        """,
        key_factors=[
            "System integration and data quality",
            "Predictive analytics capability",
            "Maintenance workflow integration",
            "Data security and privacy",
            "Return on investment"
        ],
        primary_authority=[
            "AAR Telematics Standards",
            "OEM Telematics Manuals",
            "FRA Data Security Guidelines"
        ],
        burden_holder="Railroad operator and IT personnel",
        adversary_position="Telematics systems require significant investment and may raise data privacy concerns.",
        counter_arguments=[
            "Operational savings and reduced downtime justify investment.",
            "Data security protocols mitigate privacy risks.",
            "Industry trend toward digitalization."
        ],
        resolution_strategy="Pilot telematics on select units; develop data governance policies.",
        entity_scope="All modern locomotive fleets",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="AAR Telematics Implementation Reports"
    ),
    DoctrineBlock(
        topic="Locomotive Air Intake and Filtration Systems",
        keywords=["air intake", "filtration", "engine protection", "maintenance", "emissions"],
        conclusion_template="Effective air intake and filtration systems are essential for engine performance and emissions compliance.",
        reasoning_framework="""
Air intake systems supply clean air to the engine, with filtration removing particulates and contaminants. Clogged or ineffective filters reduce engine efficiency, increase wear, and can lead to emissions violations. Maintenance includes regular inspection, filter replacement, and monitoring of differential pressure. Upgrades to high-efficiency filters may be warranted in dusty environments.
        """,
        key_factors=[
            "Filter efficiency and capacity",
            "Maintenance intervals",
            "Operating environment",
            "Integration with engine management",
            "Emissions compliance"
        ],
        primary_authority=[
            "OEM Air Intake Manuals",
            "AAR Maintenance Standards",
            "EPA Emissions Regulations"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="High-efficiency filters increase costs and may reduce airflow.",
        counter_arguments=[
            "Engine protection and emissions compliance are critical.",
            "Proper sizing maintains airflow.",
            "Long-term savings from reduced engine wear."
        ],
        resolution_strategy="Adopt filter maintenance schedules and monitor performance; upgrade in high-dust areas.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Air Intake Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Lubrication Systems",
        keywords=["lubrication", "oil", "engine protection", "maintenance", "wear"],
        conclusion_template="Proper lubrication system maintenance is critical for engine longevity and reliability.",
        reasoning_framework="""
Lubrication systems deliver oil to critical engine components, reducing friction and wear. Oil quality, viscosity, and change intervals must match OEM recommendations. Monitoring for contamination, leaks, and pressure anomalies is essential. Oil analysis supports predictive maintenance. Upgrades to synthetic oils may improve performance in extreme conditions.
        """,
        key_factors=[
            "Oil quality and viscosity",
            "Change intervals",
            "Contamination monitoring",
            "System pressure and flow",
            "OEM recommendations"
        ],
        primary_authority=[
            "OEM Lubrication Manuals",
            "AAR Lubrication Standards",
            "EPA Emissions Compliance"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Synthetic oils and frequent changes increase costs.",
        counter_arguments=[
            "Proper lubrication prevents costly engine failures.",
            "Oil analysis optimizes change intervals.",
            "Synthetic oils may reduce wear and extend intervals."
        ],
        resolution_strategy="Implement oil analysis and follow OEM guidelines; consider synthetic oils for high-stress applications.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAR Lubrication Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Traction Alternators and Generators",
        keywords=["traction alternator", "generator", "power conversion", "maintenance", "efficiency"],
        conclusion_template="Traction alternators and generators must be maintained to ensure reliable power delivery to traction motors.",
        reasoning_framework="""
Traction alternators convert mechanical energy from the prime mover into electrical energy for traction motors. Maintenance includes inspection of windings, bearings, and cooling systems. Failure can result in loss of propulsion and safety system outages. Upgrades to higher-efficiency or electronically controlled units may improve performance. Compliance with OEM and AAR standards is required.
        """,
        key_factors=[
            "Alternator/generator design and rating",
            "Maintenance and inspection",
            "Cooling system performance",
            "Integration with traction control",
            "OEM and AAR standards"
        ],
        primary_authority=[
            "OEM Alternator Manuals",
            "AAR Electrical Standards",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Upgrades and repairs are costly and may require extended downtime.",
        counter_arguments=[
            "Reliable power delivery is critical for safety and performance.",
            "Preventive maintenance reduces unplanned failures.",
            "Efficiency gains offset upgrade costs."
        ],
        resolution_strategy="Implement regular inspection and preventive maintenance; upgrade where justified by cost-benefit analysis.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Alternator Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Traction Motor Maintenance",
        keywords=["traction motor", "maintenance", "brushes", "bearings", "overhaul"],
        conclusion_template="Regular traction motor maintenance is essential for reliable locomotive operation.",
        reasoning_framework="""
Traction motors convert electrical energy into mechanical motion. Maintenance includes inspection and replacement of brushes (for DC motors), bearings, and insulation. Overheating, contamination, and vibration are common failure modes. Upgrades to AC motors reduce maintenance requirements. Compliance with OEM and AAR standards is required. Predictive diagnostics can extend service intervals.
        """,
        key_factors=[
            "Motor type (AC vs DC)",
            "Maintenance intervals",
            "Failure mode monitoring",
            "Predictive diagnostics",
            "OEM and AAR standards"
        ],
        primary_authority=[
            "OEM Traction Motor Manuals",
            "AAR Maintenance Standards",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Traction motor maintenance is labor-intensive and costly.",
        counter_arguments=[
            "Preventive maintenance reduces catastrophic failures.",
            "AC motors offer lower lifecycle costs.",
            "Predictive diagnostics improve efficiency."
        ],
        resolution_strategy="Adopt predictive diagnostics and schedule regular overhauls; consider AC motor upgrades.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="AAR Traction Motor Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Control Stand and Interface Standards",
        keywords=["control stand", "interface", "crew", "ergonomics", "standardization"],
        conclusion_template="Control stand design must balance standardization, ergonomics, and technological integration.",
        reasoning_framework="""
Control stands are the primary crew interface for locomotive operation. Standardization improves crew familiarity and reduces training time. Ergonomic design reduces fatigue and error rates. Integration with electronic displays, PTC, and diagnostic systems is increasingly important. Compliance with FRA and AAR standards is required. Crew feedback and post-incident reviews inform continuous improvement.
        """,
        key_factors=[
            "Standardization and compatibility",
            "Ergonomic layout",
            "Integration with electronic systems",
            "Crew feedback",
            "Compliance with standards"
        ],
        primary_authority=[
            "AAR Control Stand Guidelines",
            "FRA Cab Design Standards",
            "OEM Interface Manuals"
        ],
        burden_holder="Locomotive designer and operator",
        adversary_position="Upgrades and standardization may require retraining and retrofitting.",
        counter_arguments=[
            "Improved safety and efficiency justify investment.",
            "Standardization reduces training costs.",
            "Crew acceptance improves with ergonomic design."
        ],
        resolution_strategy="Phase in standardized and ergonomic control stands; solicit crew input on design.",
        entity_scope="All new and existing locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Control Stand Standard"
    ),
    DoctrineBlock(
        topic="Locomotive Head End Power (HEP) Systems",
        keywords=["HEP", "head end power", "passenger", "auxiliary power", "maintenance"],
        conclusion_template="HEP systems must provide reliable auxiliary power for passenger service, meeting regulatory and operational requirements.",
        reasoning_framework="""
HEP systems supply electrical power for passenger car lighting, HVAC, and other systems. Reliability is critical for passenger comfort and safety. Maintenance includes inspection of generators, inverters, and distribution systems. Compliance with FRA and AAR standards is required. Upgrades to higher-capacity or electronically controlled HEP systems may be needed for modern passenger cars.
        """,
        key_factors=[
            "System capacity and reliability",
            "Maintenance and inspection",
            "Integration with locomotive systems",
            "Compliance with standards",
            "Passenger comfort and safety"
        ],
        primary_authority=[
            "FRA 49 CFR Part 238",
            "AAR HEP Guidelines",
            "OEM HEP Manuals"
        ],
        burden_holder="Passenger railroad operator",
        adversary_position="HEP system failures disrupt service and increase maintenance costs.",
        counter_arguments=[
            "Preventive maintenance reduces failures.",
            "Upgrades improve reliability and capacity.",
            "Passenger satisfaction depends on system reliability."
        ],
        resolution_strategy="Implement preventive maintenance and consider system upgrades; monitor passenger feedback.",
        entity_scope="All passenger locomotives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAR HEP Implementation Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Auxiliary Power Units (APUs) and Idle Reduction",
        keywords=["APU", "auxiliary power unit", "idle reduction", "fuel savings", "emissions"],
        conclusion_template="APUs and idle reduction technologies are essential for reducing fuel consumption and emissions during layovers.",
        reasoning_framework="""
APUs provide electrical and climate control power when the main engine is shut down, reducing fuel use and emissions. Idle reduction is mandated in many jurisdictions and incentivized by regulatory credits. Maintenance includes inspection of APU engines, controls, and integration with locomotive systems. Upgrades to more efficient APUs or battery-based systems may yield further savings. Crew training and monitoring are essential for effective use.
        """,
        key_factors=[
            "System reliability and integration",
            "Fuel and emissions savings",
            "Maintenance and inspection",
            "Regulatory compliance",
            "Crew training"
        ],
        primary_authority=[
            "EPA Idle Reduction Guidelines",
            "AAR APU Standards",
            "OEM APU Manuals"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="APUs add complexity and maintenance costs; savings may not justify investment.",
        counter_arguments=[
            "Regulatory compliance is mandatory.",
            "Long-term savings and emissions reductions are significant.",
            "Crew comfort is improved."
        ],
        resolution_strategy="Implement idle reduction policies and monitor APU performance; upgrade where justified by cost-benefit analysis.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA Locomotive Idle Reduction Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Cab Signaling and Train Control Systems",
        keywords=["cab signaling", "train control", "safety", "interoperability", "FRA"],
        conclusion_template="Cab signaling and train control systems must meet safety and interoperability standards for the intended route.",
        reasoning_framework="""
Cab signaling provides in-cab indications of signal aspects and enforces speed restrictions. Integration with train control systems (e.g., ATC, PTC) enhances safety and operational efficiency. Compliance with FRA and AAR standards is required. Maintenance includes regular testing, calibration, and crew training. Interoperability across railroads and with legacy systems is a key challenge.
        """,
        key_factors=[
            "System reliability and accuracy",
            "Interoperability",
            "Maintenance and testing",
            "Crew training",
            "Compliance with standards"
        ],
        primary_authority=[
            "FRA 49 CFR Part 236",
            "AAR Signaling Standards",
            "OEM Signaling Manuals"
        ],
        burden_holder="Railroad operator and signaling personnel",
        adversary_position="Upgrades and interoperability challenges increase costs and complexity.",
        counter_arguments=[
            "Safety and regulatory compliance are paramount.",
            "Operational efficiency is improved.",
            "Federal funding may be available."
        ],
        resolution_strategy="Phase in upgrades and interoperability solutions; provide comprehensive crew training.",
        entity_scope="All signaled mainline routes",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Cab Signaling Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Crew Training and Qualification Standards",
        keywords=["crew training", "qualification", "FRA", "safety", "certification"],
        conclusion_template="Crew training and qualification must meet or exceed FRA standards for safe locomotive operation.",
        reasoning_framework="""
FRA regulations specify minimum training and certification requirements for locomotive engineers and conductors. Programs must cover rules, equipment operation, emergency procedures, and periodic requalification. Training records must be maintained and available for inspection. Ongoing education and simulation-based training improve safety and performance. Non-compliance increases accident risk and liability.
        """,
        key_factors=[
            "Training curriculum and delivery",
            "Certification and requalification",
            "Recordkeeping",
            "Use of simulators",
            "Compliance with standards"
        ],
        primary_authority=[
            "FRA 49 CFR Part 240",
            "AAR Training Standards",
            "OEM Training Materials"
        ],
        burden_holder="Railroad operator and training personnel",
        adversary_position="Training programs are resource-intensive and may disrupt operations.",
        counter_arguments=[
            "Well-trained crews reduce accidents and incidents.",
            "Simulation improves retention and performance.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Invest in comprehensive training and simulation; maintain accurate records.",
        entity_scope="All US railroads",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Crew Qualification Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Safety Appliance Standards",
        keywords=["safety appliance", "handhold", "steps", "FRA", "inspection"],
        conclusion_template="Safety appliances must be maintained and inspected to meet FRA standards for crew safety.",
        reasoning_framework="""
FRA rules require locomotives to be equipped with approved safety appliances, including handholds, steps, and ladders. Regular inspection and maintenance are required to ensure integrity and compliance. Defective appliances must be repaired before the locomotive is placed in service. Non-compliance increases risk of crew injury and regulatory penalties.
        """,
        key_factors=[
            "Appliance design and placement",
            "Inspection and maintenance",
            "Repair procedures",
            "Compliance with standards",
            "Crew feedback"
        ],
        primary_authority=[
            "FRA 49 CFR Part 231",
            "AAR Safety Appliance Standards",
            "OEM Safety Appliance Manuals"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Maintenance and inspection add operational burden.",
        counter_arguments=[
            "Crew safety is paramount.",
            "Preventive maintenance reduces liability.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Implement regular inspection and prompt repair; train crews to report defects.",
        entity_scope="All US locomotives",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Safety Appliance Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Fuel Tank Crashworthiness",
        keywords=["fuel tank", "crashworthiness", "FRA", "safety", "collision"],
        conclusion_template="Fuel tanks must meet FRA crashworthiness standards to minimize fire risk in collisions.",
        reasoning_framework="""
FRA rules specify structural requirements for locomotive fuel tanks, including puncture resistance, reinforcement, and mounting. Compliance is mandatory for new builds and certain retrofits. Regular inspection and maintenance are required to ensure integrity. Non-compliance increases fire risk and liability in accidents.
        """,
        key_factors=[
            "Tank design and materials",
            "Structural reinforcement",
            "Inspection and maintenance",
            "Compliance with standards",
            "Retrofit feasibility"
        ],
        primary_authority=[
            "FRA 49 CFR Part 238",
            "AAR Fuel Tank Standards",
            "OEM Fuel Tank Manuals"
        ],
        burden_holder="Locomotive manufacturer and operator",
        adversary_position="Crashworthy tanks add weight and cost; retrofitting is challenging.",
        counter_arguments=[
            "Fire risk justifies investment.",
            "Regulatory compliance is mandatory.",
            "Design innovations can minimize weight impact."
        ],
        resolution_strategy="Adopt crashworthy designs for new builds; prioritize retrofits based on risk assessment.",
        entity_scope="All new and high-risk locomotives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Fuel Tank Crashworthiness Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Noise and Vibration Standards",
        keywords=["noise", "vibration", "crew comfort", "FRA", "maintenance"],
        conclusion_template="Locomotive noise and vibration must be managed to meet regulatory and crew comfort standards.",
        reasoning_framework="""
FRA and EPA regulations specify maximum allowable noise and vibration levels for locomotives. Excessive noise and vibration contribute to crew fatigue and health risks. Maintenance includes inspection of exhaust systems, suspension, and cab insulation. Upgrades to noise-reducing technologies may be warranted. Compliance improves crew retention and reduces liability.
        """,
        key_factors=[
            "Noise and vibration measurement",
            "Maintenance and inspection",
            "Cab insulation and suspension",
            "Compliance with standards",
            "Crew feedback"
        ],
        primary_authority=[
            "FRA 49 CFR Part 210",
            "EPA Noise Regulations",
            "AAR Noise and Vibration Guidelines"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Noise and vibration mitigation increases costs and complexity.",
        counter_arguments=[
            "Crew health and retention are improved.",
            "Regulatory compliance is mandatory.",
            "Long-term savings from reduced incidents."
        ],
        resolution_strategy="Implement regular measurement and maintenance; upgrade insulation and suspension where justified.",
        entity_scope="All US locomotives",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Noise and Vibration Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Emissions Aftertreatment Systems",
        keywords=["aftertreatment", "emissions", "SCR", "DPF", "EPA", "maintenance"],
        conclusion_template="Aftertreatment systems must be maintained to ensure emissions compliance and engine performance.",
        reasoning_framework="""
Aftertreatment systems, including Selective Catalytic Reduction (SCR) and Diesel Particulate Filters (DPF), reduce NOx and PM emissions. Maintenance includes inspection, cleaning, and monitoring of system health. Malfunctioning aftertreatment can lead to emissions violations and engine derating. Upgrades may be required to meet newer standards. Compliance with EPA and OEM requirements is mandatory.
        """,
        key_factors=[
            "System design and integration",
            "Maintenance and inspection",
            "Monitoring and diagnostics",
            "Upgrade feasibility",
            "Compliance with standards"
        ],
        primary_authority=[
            "EPA 40 CFR Part 1033",
            "OEM Aftertreatment Manuals",
            "AAR Environmental Standards"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Aftertreatment systems add cost and complexity; failures can disrupt operations.",
        counter_arguments=[
            "Emissions compliance is mandatory.",
            "Proper maintenance reduces failure risk.",
            "Upgrades may improve fuel efficiency."
        ],
        resolution_strategy="Implement regular inspection and diagnostics; upgrade systems as required.",
        entity_scope="All Tier 4 and upgraded locomotives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA Locomotive Aftertreatment Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Data Security and Cybersecurity",
        keywords=["data security", "cybersecurity", "telematics", "PTC", "FRA", "IT"],
        conclusion_template="Locomotive data and control systems must be secured against cyber threats to ensure operational safety and regulatory compliance.",
        reasoning_framework="""
Increasing connectivity via telematics and PTC exposes locomotives to cybersecurity risks. FRA and AAR guidelines specify minimum security controls, including encryption, access control, and incident response. Regular vulnerability assessments, employee training, and software updates are required. Data breaches or cyberattacks can disrupt operations and compromise safety. Compliance with industry best practices is essential.
        """,
        key_factors=[
            "System architecture and access control",
            "Encryption and data protection",
            "Incident response planning",
            "Employee training",
            "Compliance with standards"
        ],
        primary_authority=[
            "FRA Cybersecurity Guidelines",
            "AAR Cybersecurity Standards",
            "OEM IT Security Manuals"
        ],
        burden_holder="Railroad operator and IT personnel",
        adversary_position="Cybersecurity measures increase costs and may disrupt operations.",
        counter_arguments=[
            "Operational safety and regulatory compliance are paramount.",
            "Industry best practices reduce risk.",
            "Insurance and liability considerations."
        ],
        resolution_strategy="Implement layered security controls and regular training; conduct vulnerability assessments.",
        entity_scope="All connected locomotive systems",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Cybersecurity Advisory"
    ),
    DoctrineBlock(
        topic="Locomotive Environmental and Hazardous Materials Compliance",
        keywords=["environmental compliance", "hazardous materials", "EPA", "spill response", "training"],
        conclusion_template="Locomotive operations must comply with environmental and hazardous materials regulations to prevent and mitigate spills and releases.",
        reasoning_framework="""
Locomotives carry fuel, lubricants, and other hazardous materials. EPA and FRA regulations require spill prevention, containment, and response plans. Crew training and regular drills are essential. Recordkeeping and reporting are mandatory. Non-compliance can result in fines, cleanup costs, and reputational damage. Upgrades to containment systems and spill kits may be required.
        """,
        key_factors=[
            "Spill prevention and containment",
            "Crew training and drills",
            "Recordkeeping and reporting",
            "System upgrades",
            "Compliance with standards"
        ],
        primary_authority=[
            "EPA Spill Prevention, Control, and Countermeasure (SPCC) Rule",
            "FRA Hazardous Materials Regulations",
            "AAR Environmental Guidelines"
        ],
        burden_holder="Locomotive operator and crew",
        adversary_position="Compliance adds operational burden and costs.",
        counter_arguments=[
            "Environmental protection is a legal and ethical obligation.",
            "Proper planning reduces incident impact.",
            "Insurance and regulatory benefits."
        ],
        resolution_strategy="Develop and maintain spill response plans; conduct regular training and drills.",
        entity_scope="All US locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="EPA SPCC Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Wheel and Axle Inspection Standards",
        keywords=["wheel inspection", "axle inspection", "FRA", "ultrasonic testing", "maintenance"],
        conclusion_template="Regular wheel and axle inspection is essential for safety and compliance with FRA standards.",
        reasoning_framework="""
FRA and AAR standards require regular inspection of wheels and axles for defects, wear, and cracks. Methods include visual inspection, ultrasonic testing, and measurement of profiles. Defective components must be repaired or replaced before the locomotive is returned to service. Non-compliance increases derailment risk and liability.
        """,
        key_factors=[
            "Inspection frequency and methods",
            "Defect criteria",
            "Repair and replacement procedures",
            "Recordkeeping",
            "Compliance with standards"
        ],
        primary_authority=[
            "FRA 49 CFR Part 229.75",
            "AAR Wheel and Axle Standards",
            "OEM Maintenance Manuals"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Inspection and repair add operational burden and cost.",
        counter_arguments=[
            "Safety and regulatory compliance are paramount.",
            "Preventive maintenance reduces derailment risk.",
            "Modern inspection methods improve efficiency."
        ],
        resolution_strategy="Implement regular inspection schedules and advanced testing methods; maintain accurate records.",
        entity_scope="All US locomotives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FRA Wheel and Axle Inspection Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Paint and Corrosion Protection",
        keywords=["paint", "corrosion", "maintenance", "appearance", "asset protection"],
        conclusion_template="Proper paint and corrosion protection extends locomotive service life and maintains appearance.",
        reasoning_framework="""
Paint and coatings protect locomotive structures from corrosion, especially in harsh environments. Regular inspection and touch-up prevent rust and structural degradation. Upgrades to advanced coatings may improve durability. Compliance with environmental standards for paint application and removal is required. Asset appearance also affects public perception and branding.
        """,
        key_factors=[
            "Coating type and application",
            "Inspection and touch-up",
            "Environmental compliance",
            "Operating environment",
            "Asset branding"
        ],
        primary_authority=[
            "AAR Paint and Coating Standards",
            "OEM Maintenance Manuals",
            "EPA Environmental Regulations"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Advanced coatings and frequent touch-up increase costs.",
        counter_arguments=[
            "Corrosion protection reduces long-term repair costs.",
            "Asset appearance supports branding.",
            "Environmental compliance is mandatory."
        ],
        resolution_strategy="Implement regular inspection and touch-up; upgrade coatings where justified.",
        entity_scope="All US locomotives",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="AAR Paint and Corrosion Protection Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Air Compressor and Pneumatic Systems",
        keywords=["air compressor", "pneumatic system", "brake system", "maintenance", "FRA"],
        conclusion_template="Reliable air compressor and pneumatic systems are essential for brake operation and safety.",
        reasoning_framework="""
Air compressors supply compressed air for brake and auxiliary systems. Maintenance includes inspection of compressors, dryers, reservoirs, and piping. Failure can result in loss of braking and safety system outages. Upgrades to more efficient or electronically controlled compressors may improve reliability. Compliance with FRA and AAR standards is required.
        """,
        key_factors=[
            "Compressor type and capacity",
            "Maintenance and inspection",
            "Air quality and drying",
            "System integration",
            "Compliance with standards"
        ],
        primary_authority=[
            "AAR Pneumatic System Standards",
            "OEM Compressor Manuals",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Upgrades and maintenance increase costs and complexity.",
        counter_arguments=[
            "Reliable braking is critical for safety.",
            "Preventive maintenance reduces failures.",
            "Efficiency gains offset upgrade costs."
        ],
        resolution_strategy="Implement preventive maintenance and consider system upgrades; monitor air quality.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AAR Pneumatic System Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Onboard Diagnostics and Fault Reporting",
        keywords=["diagnostics", "fault reporting", "maintenance", "crew interface", "OEM"],
        conclusion_template="Onboard diagnostics and fault reporting systems improve maintenance efficiency and operational safety.",
        reasoning_framework="""
Modern locomotives are equipped with onboard diagnostics that monitor system health and report faults to crews and maintenance personnel. Early detection of issues reduces downtime and repair costs. Integration with telematics and maintenance management systems enhances effectiveness. Crew training is required to interpret and act on diagnostic messages. Compliance with OEM and AAR standards is required.
        """,
        key_factors=[
            "System integration and accuracy",
            "Crew interface and training",
            "Maintenance workflow integration",
            "Data retention and analysis",
            "Compliance with standards"
        ],
        primary_authority=[
            "OEM Diagnostic Manuals",
            "AAR Diagnostic Standards",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="System complexity and false alarms increase maintenance burden.",
        counter_arguments=[
            "Early detection reduces catastrophic failures.",
            "Integration with maintenance systems improves efficiency.",
            "Crew training minimizes false alarms."
        ],
        resolution_strategy="Implement regular crew training and system updates; monitor diagnostic performance.",
        entity_scope="All modern locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Diagnostic System Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Air Dryer and Moisture Management",
        keywords=["air dryer", "moisture", "pneumatic system", "brake system", "maintenance"],
        conclusion_template="Effective air dryer and moisture management is essential for reliable pneumatic and brake system operation.",
        reasoning_framework="""
Air dryers remove moisture from compressed air, preventing corrosion and freezing in brake and auxiliary systems. Maintenance includes regular inspection, desiccant replacement, and monitoring of dryer performance. Failures can result in brake system malfunctions and increased maintenance costs. Upgrades to advanced dryers may improve reliability. Compliance with OEM and AAR standards is required.
        """,
        key_factors=[
            "Dryer type and capacity",
            "Maintenance and inspection",
            "Desiccant replacement",
            "System integration",
            "Compliance with standards"
        ],
        primary_authority=[
            "AAR Air Dryer Standards",
            "OEM Dryer Manuals",
            "FRA Safety Advisories"
        ],
        burden_holder="Locomotive maintenance personnel",
        adversary_position="Dryer maintenance adds cost and complexity.",
        counter_arguments=[
            "Proper moisture management prevents costly failures.",
            "Upgrades improve reliability.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Implement preventive maintenance and monitor dryer performance; upgrade where justified.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.92,
        confidence_zone="Medium-High",
        controlling_precedent="AAR Air Dryer Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Fuel Quality Management",
        keywords=["fuel quality", "contamination", "filtration", "maintenance", "engine performance"],
        conclusion_template="Fuel quality management is essential for engine performance, emissions compliance, and reliability.",
        reasoning_framework="""
Contaminated or poor-quality fuel can cause engine damage, increased emissions, and unplanned downtime. Fuel management includes sourcing from reputable suppliers, regular testing, and filtration. Maintenance includes inspection of tanks, filters, and delivery systems. Upgrades to advanced filtration may be warranted in high-risk environments. Compliance with OEM and EPA standards is required.
        """,
        key_factors=[
            "Supplier quality assurance",
            "Testing and filtration",
            "Maintenance and inspection",
            "Operating environment",
            "Compliance with standards"
        ],
        primary_authority=[
            "OEM Fuel System Manuals",
            "AAR Fuel Quality Guidelines",
            "EPA Emissions Regulations"
        ],
        burden_holder="Locomotive operator and maintenance personnel",
        adversary_position="Advanced filtration and testing increase costs.",
        counter_arguments=[
            "Engine protection and emissions compliance are critical.",
            "Proper fuel management reduces long-term costs.",
            "Regulatory compliance is mandatory."
        ],
        resolution_strategy="Implement regular fuel testing and filtration; upgrade systems in high-risk areas.",
        entity_scope="All diesel-electric locomotives",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AAR Fuel Quality Management Guidelines"
    ),
    DoctrineBlock(
        topic="Locomotive Operator Fatigue Management",
        keywords=["fatigue", "crew scheduling", "FRA", "safety", "human factors"],
        conclusion_template="Fatigue management programs are essential for safe locomotive operation and regulatory compliance.",
        reasoning_framework="""
FRA regulations and industry best practices require management of crew fatigue through scheduling, education, and monitoring. Fatigue increases accident risk and reduces crew performance. Programs include limits on hours of service, mandatory rest periods, and fatigue awareness training. Monitoring and reporting are required. Non-compliance increases liability and accident risk.
        """,
        key_factors=[
            "Scheduling and hours of service",
            "Rest period enforcement",
            "Fatigue awareness training",
            "Monitoring and reporting",
            "Compliance with standards"
        ],
        primary_authority=[
            "FRA 49 CFR Part 228",
            "AAR Fatigue Management Guidelines",
            "OEM Training Materials"
        ],
        burden_holder="Railroad operator and crew",
        adversary_position="Fatigue management programs add administrative burden and may disrupt operations.",
        counter_arguments=[
            "Crew safety and performance are improved.",
            "Regulatory compliance is mandatory.",
            "Accident risk is reduced."
        ],
        resolution_strategy="Implement scheduling systems and training; monitor compliance and adjust as needed.",
        entity_scope="All US railroads",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Fatigue Management Rule"
    ),
    DoctrineBlock(
        topic="Locomotive Emergency Response and Incident Management",
        keywords=["emergency response", "incident management", "FRA", "training", "safety"],
        conclusion_template="Comprehensive emergency response and incident management programs are essential for crew safety and regulatory compliance.",
        reasoning_framework="""
FRA and AAR standards require railroads to have emergency response plans, crew training, and regular drills. Plans must cover accident scenarios, hazardous materials, and coordination with first responders. Recordkeeping and reporting are mandatory. Regular review and updates improve effectiveness. Non-compliance increases liability and accident risk.
        """,
        key_factors=[
            "Emergency response planning",
            "Crew training and drills",
            "Coordination with first responders",
            "Recordkeeping and reporting",
            "Compliance with standards"
        ],
        primary_authority=[
            "FRA Emergency Response Guidelines",
            "AAR Incident Management Standards",
            "OEM Training Materials"
        ],
        burden_holder="Railroad operator and crew",
        adversary_position="Planning and training add operational burden and cost.",
        counter_arguments=[
            "Crew safety and regulatory compliance are paramount.",
            "Effective response reduces incident impact.",
            "Insurance and liability benefits."
        ],
        resolution_strategy="Develop and maintain emergency response plans; conduct regular training and drills.",
        entity_scope="All US railroads",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRA Emergency Response Rule"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() ==