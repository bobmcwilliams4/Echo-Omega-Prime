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
        topic="UIC 406 Line Capacity Methodology",
        keywords=["line capacity", "UIC 406", "rail network", "scheduling", "infrastructure"],
        conclusion_template="The application of UIC 406 methodology determines the maximum number of trains per hour that can be reliably operated on a given line segment.",
        reasoning_framework=(
            "UIC 406 provides a standardized approach to line capacity assessment by modeling train movements "
            "using graphical methods and calculating occupation times. The methodology considers infrastructure constraints, "
            "train mix, signaling systems, and operational rules. Key steps include mapping train paths, identifying bottlenecks, "
            "and quantifying capacity in terms of train slots per hour. Capacity enhancement options are evaluated by simulating "
            "alternative timetables and infrastructure upgrades. The framework emphasizes the importance of realistic train performance data, "
            "dwell times, and buffer times to ensure robust results. The methodology is widely accepted in Europe and increasingly adopted globally."
        ),
        key_factors=[
            "Infrastructure layout",
            "Signaling system type",
            "Train mix and performance",
            "Timetable structure",
            "Dwell times",
            "Buffer times",
            "Bottleneck identification"
        ],
        primary_authority=["UIC 406", "European Rail Agency", "Network Rail"],
        burden_holder="Infrastructure Manager",
        adversary_position="Operators may argue for higher capacity based on theoretical train performance.",
        counter_arguments=[
            "Theoretical performance often ignores real-world delays and variability.",
            "Safety margins are necessary for reliable operations.",
            "Infrastructure constraints limit practical capacity."
        ],
        resolution_strategy="Capacity is determined by simulation and empirical validation, with stakeholder review.",
        entity_scope="Rail infrastructure planning and operations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="UIC 406: Capacity Manual"
    ),
    DoctrineBlock(
        topic="Train Performance Calculation (TPC Curves)",
        keywords=["train performance", "TPC", "acceleration", "braking", "speed profile"],
        conclusion_template="Train Performance Calculation curves provide accurate speed-distance profiles for various train types under specific operating conditions.",
        reasoning_framework=(
            "TPC curves are derived from detailed modeling of train dynamics, including acceleration, braking, and resistance forces. "
            "The calculation incorporates locomotive power, rolling stock characteristics, gradient, curvature, and environmental factors. "
            "TPC curves are essential for timetable construction, capacity analysis, and infrastructure design. The framework requires validated input data, "
            "calibration against real-world measurements, and iterative refinement. Modern tools use simulation software to generate and analyze TPC curves, "
            "ensuring alignment with operational requirements and safety standards."
        ),
        key_factors=[
            "Locomotive power and traction characteristics",
            "Rolling stock mass and configuration",
            "Track gradient and curvature",
            "Environmental conditions",
            "Braking system performance"
        ],
        primary_authority=["Federal Railroad Administration (FRA)", "UIC", "Association of American Railroads (AAR)"],
        burden_holder="Rail Operator",
        adversary_position="Infrastructure managers may challenge train performance assumptions for capacity planning.",
        counter_arguments=[
            "Empirical validation is required to ensure accuracy.",
            "Safety margins must be maintained.",
            "Performance assumptions should reflect typical operating conditions."
        ],
        resolution_strategy="TPC curves are validated through field trials and simulation, with regulatory oversight.",
        entity_scope="Timetable planning, capacity analysis, infrastructure design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FRA Locomotive Performance Standards"
    ),
    DoctrineBlock(
        topic="Intermodal Terminal Capacity and Design",
        keywords=["intermodal", "terminal", "capacity", "design", "container handling"],
        conclusion_template="Intermodal terminal capacity is determined by throughput analysis, yard layout, and equipment efficiency, ensuring optimal container handling and train operations.",
        reasoning_framework=(
            "Terminal capacity is evaluated using throughput models that account for container arrival rates, dwell times, and equipment utilization. "
            "Design principles emphasize efficient yard layout, adequate track length, and scalable handling equipment. Simulation tools assess bottlenecks, "
            "queue lengths, and operational scenarios. The framework integrates safety, environmental, and regulatory requirements, with iterative design refinement "
            "based on stakeholder feedback. Capacity expansion options are analyzed for cost-effectiveness and operational impact."
        ),
        key_factors=[
            "Container arrival and departure rates",
            "Yard layout and track configuration",
            "Handling equipment type and capacity",
            "Dwell times",
            "Regulatory and safety requirements"
        ],
        primary_authority=["Intermodal Association of North America (IANA)", "FRA", "AAR"],
        burden_holder="Terminal Operator",
        adversary_position="Rail operators may demand higher throughput than feasible.",
        counter_arguments=[
            "Physical constraints limit expansion.",
            "Equipment upgrades require significant investment.",
            "Regulatory compliance may restrict operational flexibility."
        ],
        resolution_strategy="Capacity is optimized through simulation, stakeholder engagement, and phased investment.",
        entity_scope="Intermodal terminal planning and operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="IANA Terminal Design Guidelines"
    ),
    DoctrineBlock(
        topic="Centralized Traffic Control (CTC) Dispatching Optimization",
        keywords=["CTC", "dispatching", "optimization", "rail operations", "signal control"],
        conclusion_template="CTC dispatching optimization ensures efficient train movement and minimizes conflicts through advanced scheduling and real-time control algorithms.",
        reasoning_framework=(
            "CTC systems centralize train control, enabling dispatchers to manage train movements across large network segments. Optimization involves real-time scheduling, "
            "conflict resolution, and prioritization of train movements based on operational objectives. The framework leverages predictive analytics, historical data, "
            "and simulation to identify optimal routing and minimize delays. Integration with Positive Train Control (PTC) enhances safety and reliability. "
            "Stakeholder collaboration is essential for balancing freight and passenger priorities."
        ),
        key_factors=[
            "Network topology",
            "Train mix and priorities",
            "Signal system capabilities",
            "Real-time data availability",
            "Integration with PTC"
        ],
        primary_authority=["FRA", "AAR", "RailSys", "OpenTrack"],
        burden_holder="Rail Dispatcher",
        adversary_position="Operators may contest dispatching decisions affecting train priority.",
        counter_arguments=[
            "Dispatching must balance network-wide efficiency.",
            "Safety overrides operational preferences.",
            "Real-time constraints limit flexibility."
        ],
        resolution_strategy="Optimization algorithms and stakeholder review guide dispatching decisions.",
        entity_scope="Rail network operations and control",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA CTC Dispatching Standards"
    ),
    DoctrineBlock(
        topic="Benefit-Cost Analysis for Rail Infrastructure Investment",
        keywords=["benefit-cost analysis", "rail investment", "economic evaluation", "project appraisal"],
        conclusion_template="Benefit-cost analysis quantifies the economic viability of rail infrastructure projects by comparing projected benefits to costs over the asset lifecycle.",
        reasoning_framework=(
            "Benefit-cost analysis (BCA) applies economic principles to evaluate rail infrastructure investments. The framework identifies direct and indirect benefits, "
            "including travel time savings, safety improvements, environmental gains, and economic development. Costs encompass capital, operating, and maintenance expenses. "
            "Discount rates, risk assessment, and sensitivity analysis are integral to robust BCA. Regulatory guidelines mandate transparent documentation and stakeholder engagement. "
            "Results inform funding decisions and project prioritization."
        ),
        key_factors=[
            "Capital and operating costs",
            "Projected benefits (time, safety, environment)",
            "Discount rate selection",
            "Risk and uncertainty analysis",
            "Stakeholder input"
        ],
        primary_authority=["USDOT", "FRA", "World Bank", "AAR"],
        burden_holder="Project Sponsor",
        adversary_position="Opponents may challenge benefit assumptions or cost estimates.",
        counter_arguments=[
            "Benefit projections must be evidence-based.",
            "Cost overruns are common in large projects.",
            "Sensitivity analysis addresses uncertainty."
        ],
        resolution_strategy="Transparent methodology and independent review ensure credible BCA results.",
        entity_scope="Rail infrastructure investment planning",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="USDOT Benefit-Cost Analysis Guidance"
    ),
    DoctrineBlock(
        topic="Double-Stack Clearance Requirements",
        keywords=["double-stack", "clearance", "rail infrastructure", "freight", "tunnel", "bridge"],
        conclusion_template="Double-stack clearance is achieved by verifying vertical and horizontal clearances along the route, ensuring safe passage of stacked containers.",
        reasoning_framework=(
            "Clearance requirements are determined by measuring the height and width of double-stack railcars and comparing them to tunnel, bridge, and overhead structure dimensions. "
            "The framework involves route surveys, engineering assessments, and regulatory compliance checks. Infrastructure modifications, such as raising bridges or lowering track, "
            "are evaluated for feasibility and cost. Safety standards mandate minimum clearance buffers to account for dynamic movement and loading variability."
        ),
        key_factors=[
            "Railcar dimensions",
            "Structure height and width",
            "Route survey data",
            "Engineering feasibility",
            "Regulatory standards"
        ],
        primary_authority=["FRA", "AAR", "USDOT"],
        burden_holder="Infrastructure Owner",
        adversary_position="Operators may push for expedited clearance upgrades.",
        counter_arguments=[
            "Upgrades require significant investment.",
            "Safety cannot be compromised.",
            "Regulatory approval is mandatory."
        ],
        resolution_strategy="Clearance upgrades are prioritized based on traffic demand and cost-benefit analysis.",
        entity_scope="Freight rail infrastructure planning",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRA Clearance Standards"
    ),
    DoctrineBlock(
        topic="Rail Yard Classification and Design",
        keywords=["rail yard", "classification", "design", "operations", "capacity"],
        conclusion_template="Rail yard classification and design optimize train sorting, assembly, and dispatch, balancing throughput, safety, and operational flexibility.",
        reasoning_framework=(
            "Yard design principles focus on efficient classification tracks, adequate lead tracks, and robust switching operations. The framework evaluates yard capacity, "
            "layout, and operational scenarios using simulation and empirical data. Safety, environmental, and regulatory requirements are integrated into design decisions. "
            "Stakeholder input guides yard expansion and modernization, with emphasis on minimizing bottlenecks and maximizing throughput."
        ),
        key_factors=[
            "Classification track layout",
            "Switching operations",
            "Lead track length",
            "Safety and environmental standards",
            "Operational flexibility"
        ],
        primary_authority=["AAR", "FRA", "RailSys"],
        burden_holder="Yard Manager",
        adversary_position="Operators may demand higher throughput or faster sorting.",
        counter_arguments=[
            "Physical constraints limit yard expansion.",
            "Safety standards restrict operational changes.",
            "Environmental regulations must be observed."
        ],
        resolution_strategy="Yard design is optimized through simulation and stakeholder engagement.",
        entity_scope="Rail yard planning and operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="AAR Yard Design Guidelines"
    ),
    DoctrineBlock(
        topic="Grade Crossing Elimination and Priority Ranking",
        keywords=["grade crossing", "elimination", "priority", "safety", "ranking"],
        conclusion_template="Grade crossing elimination is prioritized based on safety risk, traffic volume, and cost-benefit analysis, with high-risk crossings targeted first.",
        reasoning_framework=(
            "The framework ranks grade crossings using risk assessment models that consider accident history, traffic volume, train frequency, and proximity to schools or hospitals. "
            "Elimination options include grade separation, closure, or enhanced warning systems. Cost-benefit analysis guides investment decisions, with regulatory mandates for high-risk crossings. "
            "Stakeholder engagement ensures community needs are addressed."
        ),
        key_factors=[
            "Accident history",
            "Traffic volume",
            "Train frequency",
            "Proximity to sensitive locations",
            "Cost-benefit analysis"
        ],
        primary_authority=["FRA", "USDOT", "State DOTs"],
        burden_holder="Infrastructure Owner",
        adversary_position="Local communities may oppose crossing closures.",
        counter_arguments=[
            "Safety benefits outweigh inconvenience.",
            "Alternative access can be provided.",
            "Regulatory mandates require action."
        ],
        resolution_strategy="Priority ranking and transparent communication guide elimination decisions.",
        entity_scope="Rail safety and infrastructure planning",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Grade Crossing Safety Regulations"
    ),
    DoctrineBlock(
        topic="Network Simulation with RailSys and OpenTrack",
        keywords=["network simulation", "RailSys", "OpenTrack", "modeling", "capacity"],
        conclusion_template="Network simulation using RailSys and OpenTrack enables detailed analysis of train movements, capacity, and operational scenarios.",
        reasoning_framework=(
            "Simulation tools model train movements, infrastructure constraints, and operational rules to assess network performance. The framework involves data input, scenario definition, "
            "and iterative simulation runs. Results inform capacity planning, timetable optimization, and infrastructure investment decisions. Validation against real-world data ensures accuracy. "
            "Stakeholder collaboration is essential for scenario selection and interpretation."
        ),
        key_factors=[
            "Input data quality",
            "Scenario definition",
            "Infrastructure constraints",
            "Operational rules",
            "Validation against empirical data"
        ],
        primary_authority=["RailSys", "OpenTrack", "FRA"],
        burden_holder="Simulation Analyst",
        adversary_position="Operators may dispute simulation assumptions or results.",
        counter_arguments=[
            "Assumptions must be transparent and evidence-based.",
            "Validation is required for credibility.",
            "Stakeholder input enhances scenario relevance."
        ],
        resolution_strategy="Simulation results are reviewed and validated with stakeholders.",
        entity_scope="Rail network planning and operations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="RailSys/OpenTrack Simulation Standards"
    ),
    DoctrineBlock(
        topic="Short Line Railroad Economics and Viability",
        keywords=["short line", "railroad", "economics", "viability", "business model"],
        conclusion_template="Short line railroad viability is assessed through financial analysis, market demand, and operational efficiency, with emphasis on sustainable business models.",
        reasoning_framework=(
            "Economic viability is determined by analyzing revenue streams, cost structures, and market demand. The framework evaluates freight volumes, customer base, and competitive landscape. "
            "Operational efficiency, access to Class I connections, and regulatory compliance are critical factors. Financial modeling and risk assessment guide investment and operational decisions. "
            "Stakeholder engagement, including local governments and shippers, supports sustainability."
        ),
        key_factors=[
            "Revenue and cost analysis",
            "Freight volume and market demand",
            "Operational efficiency",
            "Class I railroad connections",
            "Regulatory compliance"
        ],
        primary_authority=["AAR", "FRA", "Short Line Railroad Association"],
        burden_holder="Short Line Operator",
        adversary_position="Investors may question long-term viability.",
        counter_arguments=[
            "Diversification of revenue streams enhances sustainability.",
            "Operational improvements reduce costs.",
            "Public-private partnerships support investment."
        ],
        resolution_strategy="Viability is supported by robust financial modeling and stakeholder collaboration.",
        entity_scope="Short line railroad planning and operations",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="AAR Short Line Viability Studies"
    ),
    DoctrineBlock(
        topic="Class I Railroad Operations Planning and PSR",
        keywords=["Class I", "railroad", "operations planning", "Precision Scheduled Railroading", "PSR"],
        conclusion_template="Class I railroad operations planning under PSR focuses on optimizing train schedules, asset utilization, and service reliability.",
        reasoning_framework=(
            "Precision Scheduled Railroading (PSR) applies disciplined scheduling, asset management, and operational efficiency principles to Class I railroads. The framework emphasizes fixed train schedules, "
            "minimized dwell times, and streamlined yard operations. Asset utilization is maximized through data analytics and real-time monitoring. Service reliability is prioritized, with continuous improvement initiatives. "
            "Stakeholder engagement addresses concerns about workforce impacts and service changes."
        ),
        key_factors=[
            "Train scheduling discipline",
            "Asset utilization",
            "Yard operations efficiency",
            "Service reliability",
            "Workforce management"
        ],
        primary_authority=["AAR", "FRA", "Class I Railroads"],
        burden_holder="Operations Planner",
        adversary_position="Labor unions may oppose workforce reductions.",
        counter_arguments=[
            "Efficiency gains benefit overall network performance.",
            "Workforce impacts can be mitigated through retraining.",
            "Service reliability supports customer satisfaction."
        ],
        resolution_strategy="Continuous improvement and stakeholder engagement guide PSR implementation.",
        entity_scope="Class I railroad operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Class I PSR Implementation Reports"
    ),
    DoctrineBlock(
        topic="Positive Train Control (PTC) Implementation and Impact",
        keywords=["PTC", "positive train control", "implementation", "safety", "impact"],
        conclusion_template="PTC implementation enhances rail safety by preventing collisions, overspeed derailments, and unauthorized train movements.",
        reasoning_framework=(
            "PTC systems integrate GPS, radio communications, and centralized control to monitor and enforce train movements. Implementation involves hardware installation, software integration, "
            "and operator training. The framework assesses safety impacts, operational changes, and compliance with regulatory mandates. Challenges include interoperability, cost, and system reliability. "
            "Stakeholder collaboration is essential for successful deployment and ongoing maintenance."
        ),
        key_factors=[
            "System interoperability",
            "Hardware and software integration",
            "Operator training",
            "Regulatory compliance",
            "Safety impact assessment"
        ],
        primary_authority=["FRA", "AAR", "USDOT"],
        burden_holder="Rail Operator",
        adversary_position="Operators may cite high implementation costs.",
        counter_arguments=[
            "Safety benefits outweigh costs.",
            "Regulatory mandates require compliance.",
            "Federal funding supports implementation."
        ],
        resolution_strategy="Implementation is phased, with regulatory oversight and stakeholder engagement.",
        entity_scope="Rail safety and operations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA PTC Implementation Regulations"
    ),
    DoctrineBlock(
        topic="Rail Corridor Environmental Impact Assessment",
        keywords=["environmental impact", "rail corridor", "assessment", "EIA", "regulatory compliance"],
        conclusion_template="Environmental impact assessment evaluates rail corridor projects for effects on ecosystems, air quality, noise, and community health, ensuring regulatory compliance.",
        reasoning_framework=(
            "EIA applies scientific and regulatory frameworks to assess project impacts on natural and human environments. The process includes baseline studies, impact prediction, mitigation planning, "
            "and stakeholder consultation. Regulatory compliance with NEPA and state laws is mandatory. The framework emphasizes transparency, public participation, and adaptive management to address emerging concerns."
        ),
        key_factors=[
            "Baseline environmental studies",
            "Impact prediction and modeling",
            "Mitigation planning",
            "Regulatory compliance",
            "Stakeholder consultation"
        ],
        primary_authority=["NEPA", "EPA", "FRA", "State Environmental Agencies"],
        burden_holder="Project Sponsor",
        adversary_position="Environmental groups may challenge impact findings.",
        counter_arguments=[
            "Scientific evidence supports impact predictions.",
            "Mitigation measures address key concerns.",
            "Public participation enhances transparency."
        ],
        resolution_strategy="EIA is conducted with regulatory oversight and stakeholder engagement.",
        entity_scope="Rail corridor planning and development",
        confidence=0.86,
        confidence_zone="Medium",
        controlling_precedent="NEPA Environmental Impact Assessment Standards"
    ),
    DoctrineBlock(
        topic="Rail Infrastructure Financing Mechanisms",
        keywords=["financing", "rail infrastructure", "public-private partnership", "funding", "investment"],
        conclusion_template="Rail infrastructure financing is achieved through a mix of public funding, private investment, and innovative mechanisms such as PPPs and tax credits.",
        reasoning_framework=(
            "The financing framework evaluates funding sources, investment structures, and risk allocation. Public funding includes federal grants, state programs, and municipal bonds. "
            "Private investment is facilitated through PPPs, equity, and debt instruments. Tax credits and innovative mechanisms, such as value capture, support project viability. "
            "Risk assessment and stakeholder negotiation guide financing decisions, with regulatory compliance and transparency as core principles."
        ),
        key_factors=[
            "Funding source identification",
            "Investment structure",
            "Risk allocation",
            "Regulatory compliance",
            "Stakeholder negotiation"
        ],
        primary_authority=["USDOT", "FRA", "World Bank", "Private Investors"],
        burden_holder="Project Sponsor",
        adversary_position="Opponents may challenge risk allocation or funding adequacy.",
        counter_arguments=[
            "Risk sharing enhances project viability.",
            "Public funding supports essential infrastructure.",
            "Innovative mechanisms attract private investment."
        ],
        resolution_strategy="Financing is structured through negotiation and regulatory review.",
        entity_scope="Rail infrastructure investment",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="USDOT Financing Guidance"
    ),
    DoctrineBlock(
        topic="Rail Freight Demand Forecasting Methodology",
        keywords=["freight demand", "forecasting", "rail", "market analysis", "modeling"],
        conclusion_template="Rail freight demand forecasting uses econometric models, market analysis, and historical data to predict future volumes and inform capacity planning.",
        reasoning_framework=(
            "Forecasting methodology applies statistical and econometric models to analyze historical freight volumes, market trends, and economic indicators. The framework incorporates scenario analysis, "
            "stakeholder input, and validation against industry benchmarks. Results guide capacity planning, investment decisions, and service development. Transparency and methodological rigor are essential for credibility."
        ),
        key_factors=[
            "Historical freight volume data",
            "Market trends",
            "Economic indicators",
            "Scenario analysis",
            "Stakeholder input"
        ],
        primary_authority=["AAR", "FRA", "USDOT"],
        burden_holder="Market Analyst",
        adversary_position="Operators may dispute forecast assumptions.",
        counter_arguments=[
            "Assumptions must be evidence-based.",
            "Validation enhances forecast accuracy.",
            "Scenario analysis addresses uncertainty."
        ],
        resolution_strategy="Forecasts are reviewed and validated with stakeholders.",
        entity_scope="Rail freight planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="AAR Freight Forecasting Standards"
    ),
    DoctrineBlock(
        topic="Passenger Rail Service Planning and Operating Cost Estimation",
        keywords=["passenger rail", "service planning", "operating cost", "estimation", "timetable"],
        conclusion_template="Passenger rail service planning integrates timetable design, ridership forecasting, and operating cost estimation to ensure sustainable service delivery.",
        reasoning_framework=(
            "Service planning involves timetable construction, ridership forecasting, and cost estimation. The framework applies demand modeling, operational analysis, and stakeholder engagement. "
            "Operating costs are estimated using historical data, unit cost models, and scenario analysis. Results inform service design, funding decisions, and fare policy. Regulatory compliance and public input are essential."
        ),
        key_factors=[
            "Timetable design",
            "Ridership forecasting",
            "Operating cost modeling",
            "Scenario analysis",
            "Stakeholder engagement"
        ],
        primary_authority=["FRA", "USDOT", "Amtrak"],
        burden_holder="Service Planner",
        adversary_position="Operators may dispute cost estimates or timetable assumptions.",
        counter_arguments=[
            "Cost models must be evidence-based.",
            "Ridership forecasts require validation.",
            "Stakeholder input enhances service design."
        ],
        resolution_strategy="Service plans are reviewed and refined with stakeholders.",
        entity_scope="Passenger rail planning and operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Passenger Service Planning Standards"
    ),
    DoctrineBlock(
        topic="Rail Bridge Load Rating and Replacement Priority",
        keywords=["rail bridge", "load rating", "replacement", "priority", "structural assessment"],
        conclusion_template="Rail bridge load rating determines structural capacity and guides replacement priority based on safety risk, traffic demand, and asset condition.",
        reasoning_framework=(
            "Load rating applies engineering analysis to assess bridge structural capacity under various train loads. The framework incorporates material properties, inspection data, "
            "and historical performance. Replacement priority is determined by safety risk, traffic demand, and asset condition. Regulatory standards mandate periodic assessment and reporting."
        ),
        key_factors=[
            "Structural analysis",
            "Material properties",
            "Inspection data",
            "Traffic demand",
            "Safety risk assessment"
        ],
        primary_authority=["FRA", "AAR", "USDOT"],
        burden_holder="Infrastructure Owner",
        adversary_position="Operators may request expedited replacement.",
        counter_arguments=[
            "Replacement must be prioritized based on risk and demand.",
            "Budget constraints limit immediate action.",
            "Regulatory standards guide assessment."
        ],
        resolution_strategy="Replacement priority is determined by risk assessment and stakeholder review.",
        entity_scope="Rail bridge asset management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FRA Bridge Load Rating Standards"
    ),
    DoctrineBlock(
        topic="Rail Electrification Feasibility and Economics",
        keywords=["rail electrification", "feasibility", "economics", "infrastructure", "energy"],
        conclusion_template="Rail electrification feasibility is evaluated through technical, economic, and environmental analysis, with emphasis on lifecycle costs and operational benefits.",
        reasoning_framework=(
            "Feasibility analysis assesses technical requirements, infrastructure modifications, and energy supply options. Economic evaluation includes capital costs, operating savings, and environmental benefits. "
            "The framework applies lifecycle cost modeling, scenario analysis, and stakeholder engagement. Regulatory compliance and funding mechanisms are integral to project viability."
        ),
        key_factors=[
            "Technical requirements",
            "Infrastructure modifications",
            "Energy supply options",
            "Lifecycle cost modeling",
            "Environmental benefits"
        ],
        primary_authority=["FRA", "USDOT", "World Bank"],
        burden_holder="Project Sponsor",
        adversary_position="Operators may cite high capital costs.",
        counter_arguments=[
            "Operating savings offset capital investment.",
            "Environmental benefits support funding.",
            "Lifecycle cost modeling provides robust analysis."
        ],
        resolution_strategy="Feasibility is determined through comprehensive analysis and stakeholder input.",
        entity_scope="Rail infrastructure planning",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="World Bank Rail Electrification Guidelines"
    ),
    DoctrineBlock(
        topic="Rail Network Resilience and Disaster Recovery",
        keywords=["network resilience", "disaster recovery", "rail", "emergency planning", "business continuity"],
        conclusion_template="Rail network resilience is achieved through risk assessment, emergency planning, and investment in robust infrastructure and recovery capabilities.",
        reasoning_framework=(
            "Resilience framework applies risk assessment, scenario planning, and investment in robust infrastructure. Disaster recovery plans include emergency response protocols, asset redundancy, "
            "and stakeholder coordination. Regulatory standards mandate business continuity planning and periodic drills. Continuous improvement and adaptive management enhance resilience."
        ),
        key_factors=[
            "Risk assessment",
            "Emergency response protocols",
            "Asset redundancy",
            "Stakeholder coordination",
            "Business continuity planning"
        ],
        primary_authority=["FRA", "USDOT", "Homeland Security"],
        burden_holder="Infrastructure Owner",
        adversary_position="Operators may challenge investment priorities.",
        counter_arguments=[
            "Resilience investments reduce long-term risk.",
            "Regulatory mandates require planning.",
            "Stakeholder coordination enhances recovery."
        ],
        resolution_strategy="Resilience is enhanced through continuous improvement and stakeholder engagement.",
        entity_scope="Rail network planning and operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Network Resilience Standards"
    ),
    DoctrineBlock(
        topic="Rail Corridor Land Use and Transit-Oriented Development (TOD)",
        keywords=["land use", "rail corridor", "TOD", "development", "planning"],
        conclusion_template="Rail corridor land use planning integrates transit-oriented development principles to maximize economic, environmental, and community benefits.",
        reasoning_framework=(
            "Land use planning applies TOD principles to promote mixed-use development, increased ridership, and reduced environmental impact. The framework involves stakeholder engagement, zoning analysis, "
            "and economic modeling. Regulatory compliance with local and state laws is mandatory. Results inform corridor development, investment decisions, and community outreach."
        ),
        key_factors=[
            "Zoning analysis",
            "Stakeholder engagement",
            "Economic modeling",
            "Regulatory compliance",
            "Community outreach"
        ],
        primary_authority=["USDOT", "FRA", "Local Planning Agencies"],
        burden_holder="Planning Agency",
        adversary_position="Local communities may resist development changes.",
        counter_arguments=[
            "TOD enhances economic and environmental outcomes.",
            "Stakeholder engagement addresses concerns.",
            "Regulatory compliance ensures transparency."
        ],
        resolution_strategy="Development is guided by TOD principles and stakeholder collaboration.",
        entity_scope="Rail corridor planning and development",
        confidence=0.86,
        confidence_zone="Medium",
        controlling_precedent="USDOT TOD Planning Guidelines"
    ),
    DoctrineBlock(
        topic="Rail Safety Performance Metrics and FRA Reporting",
        keywords=["safety metrics", "FRA reporting", "performance", "rail", "regulatory compliance"],
        conclusion_template="Rail safety performance metrics are tracked and reported to FRA, guiding safety improvement initiatives and regulatory compliance.",
        reasoning_framework=(
            "Safety metrics include accident rates, near-miss incidents, and compliance with operational standards. The framework applies data collection, analysis, and reporting protocols mandated by FRA. "
            "Continuous improvement initiatives are informed by metric trends and stakeholder feedback. Regulatory compliance is monitored through periodic audits and reporting."
        ),
        key_factors=[
            "Accident and incident data",
            "Operational standards compliance",
            "Data collection protocols",
            "Continuous improvement",
            "Regulatory audits"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Rail Operator",
        adversary_position="Operators may dispute metric definitions or reporting requirements.",
        counter_arguments=[
            "Standardized metrics ensure comparability.",
            "Regulatory mandates require reporting.",
            "Continuous improvement benefits all stakeholders."
        ],
        resolution_strategy="Metrics are reviewed and refined through stakeholder engagement and regulatory oversight.",
        entity_scope="Rail safety and operations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRA Safety Reporting Standards"
    ),
    DoctrineBlock(
        topic="High-Speed Rail Corridor Planning and Engineering Standards",
        keywords=["high-speed rail", "corridor planning", "engineering standards", "infrastructure", "operations"],
        conclusion_template="High-speed rail corridor planning applies engineering standards to ensure safety, performance, and operational reliability.",
        reasoning_framework=(
            "Planning framework integrates engineering standards for track geometry, signaling, rolling stock, and station design. Safety and performance requirements are prioritized, "
            "with scenario analysis and stakeholder engagement guiding corridor development. Regulatory compliance with FRA and international standards is mandatory. Investment decisions are informed by cost-benefit analysis and risk assessment."
        ),
        key_factors=[
            "Track geometry",
            "Signaling system",
            "Rolling stock specifications",
            "Station design",
            "Safety and performance requirements"
        ],
        primary_authority=["FRA", "USDOT", "UIC"],
        burden_holder="Project Sponsor",
        adversary_position="Operators may challenge engineering requirements or investment priorities.",
        counter_arguments=[
            "Safety and performance standards are non-negotiable.",
            "Investment decisions require robust analysis.",
            "Stakeholder engagement enhances corridor planning."
        ],
        resolution_strategy="Corridor planning is guided by engineering standards and stakeholder input.",
        entity_scope="High-speed rail planning and operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA High-Speed Rail Engineering Standards"
    ),
    DoctrineBlock(
        topic="Rail Infrastructure Asset Management and Life-Cycle Costing",
        keywords=["asset management", "life-cycle costing", "rail infrastructure", "maintenance", "investment"],
        conclusion_template="Asset management applies life-cycle costing to optimize maintenance, renewal, and investment decisions for rail infrastructure.",
        reasoning_framework=(
            "Asset management framework evaluates asset condition, maintenance history, and renewal needs. Life-cycle costing models estimate total costs over asset lifespan, "
            "informing maintenance and investment decisions. Regulatory compliance and stakeholder engagement are integral to robust asset management. Continuous improvement and adaptive management enhance asset performance."
        ),
        key_factors=[
            "Asset condition assessment",
            "Maintenance history",
            "Renewal needs",
            "Life-cycle cost modeling",
            "Regulatory compliance"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Asset Manager",
        adversary_position="Operators may dispute maintenance priorities or cost estimates.",
        counter_arguments=[
            "Life-cycle costing ensures optimal investment.",
            "Regulatory mandates require asset management.",
            "Continuous improvement enhances asset performance."
        ],
        resolution_strategy="Asset management is guided by life-cycle costing and stakeholder input.",
        entity_scope="Rail infrastructure planning and operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FRA Asset Management Standards"
    ),
    DoctrineBlock(
        topic="Rail Cybersecurity and SCADA System Protection",
        keywords=["cybersecurity", "SCADA", "rail", "system protection", "IT security"],
        conclusion_template="Rail cybersecurity framework protects SCADA systems through risk assessment, technical controls, and regulatory compliance.",
        reasoning_framework=(
            "Cybersecurity framework applies risk assessment, technical controls, and regulatory compliance to protect SCADA systems. The process includes vulnerability analysis, access control, "
            "and incident response planning. Regulatory standards mandate periodic audits and reporting. Stakeholder engagement and continuous improvement enhance system protection."
        ),
        key_factors=[
            "Risk assessment",
            "Technical controls",
            "Vulnerability analysis",
            "Incident response planning",
            "Regulatory compliance"
        ],
        primary_authority=["FRA", "USDOT", "Homeland Security"],
        burden_holder="IT Security Manager",
        adversary_position="Operators may challenge investment in cybersecurity.",
        counter_arguments=[
            "Cyber threats pose significant risk.",
            "Regulatory mandates require protection.",
            "Continuous improvement enhances security."
        ],
        resolution_strategy="System protection is enhanced through technical controls and stakeholder engagement.",
        entity_scope="Rail IT and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Cybersecurity Standards"
    ),
    DoctrineBlock(
        topic="Rail Labor Agreements and Crew Scheduling Optimization",
        keywords=["labor agreements", "crew scheduling", "optimization", "rail", "workforce"],
        conclusion_template="Crew scheduling optimization balances operational efficiency with compliance to labor agreements and regulatory requirements.",
        reasoning_framework=(
            "Scheduling framework applies optimization algorithms, labor agreement analysis, and regulatory compliance. The process includes shift planning, fatigue management, and stakeholder negotiation. "
            "Continuous improvement and adaptive management enhance scheduling outcomes. Regulatory standards mandate periodic review and reporting."
        ),
        key_factors=[
            "Optimization algorithms",
            "Labor agreement analysis",
            "Regulatory compliance",
            "Fatigue management",
            "Stakeholder negotiation"
        ],
        primary_authority=["FRA", "USDOT", "Labor Unions"],
        burden_holder="Operations Manager",
        adversary_position="Labor unions may dispute scheduling changes.",
        counter_arguments=[
            "Operational efficiency benefits all stakeholders.",
            "Regulatory mandates require compliance.",
            "Stakeholder negotiation addresses concerns."
        ],
        resolution_strategy="Scheduling is optimized through negotiation and regulatory review.",
        entity_scope="Rail workforce planning and operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Crew Scheduling Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Interoperability and Standards Compliance",
        keywords=["interoperability", "standards compliance", "rail network", "operations", "regulatory"],
        conclusion_template="Rail network interoperability is achieved through adherence to technical standards and regulatory requirements, ensuring seamless operations across operators.",
        reasoning_framework=(
            "Interoperability framework applies technical standards for signaling, rolling stock, and infrastructure. Regulatory compliance ensures compatibility and safety. Stakeholder engagement addresses operational challenges. "
            "Continuous improvement and periodic audits enhance interoperability outcomes."
        ),
        key_factors=[
            "Technical standards adherence",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Operational compatibility",
            "Periodic audits"
        ],
        primary_authority=["FRA", "USDOT", "UIC"],
        burden_holder="Infrastructure Owner",
        adversary_position="Operators may challenge technical requirements.",
        counter_arguments=[
            "Standards ensure safety and compatibility.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Interoperability is enhanced through standards adherence and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="UIC Interoperability Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Capacity Enhancement Strategies",
        keywords=["capacity enhancement", "rail network", "strategies", "infrastructure", "operations"],
        conclusion_template="Capacity enhancement strategies include infrastructure upgrades, operational improvements, and timetable optimization to maximize network throughput.",
        reasoning_framework=(
            "Enhancement framework evaluates infrastructure upgrades (e.g., double-tracking, signaling improvements), operational changes (e.g., train scheduling, dwell time reduction), and timetable optimization. "
            "Cost-benefit analysis and stakeholder engagement guide investment decisions. Regulatory compliance and continuous improvement are integral to robust capacity enhancement."
        ),
        key_factors=[
            "Infrastructure upgrades",
            "Operational improvements",
            "Timetable optimization",
            "Cost-benefit analysis",
            "Stakeholder engagement"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Infrastructure Owner",
        adversary_position="Operators may dispute enhancement priorities.",
        counter_arguments=[
            "Enhancements must be prioritized based on demand and feasibility.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Strategies are implemented through phased investment and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FRA Capacity Enhancement Guidelines"
    ),
    DoctrineBlock(
        topic="Rail Network Bottleneck Identification and Mitigation",
        keywords=["bottleneck", "identification", "mitigation", "rail network", "operations"],
        conclusion_template="Bottleneck identification and mitigation apply data analysis, simulation, and operational changes to improve network performance.",
        reasoning_framework=(
            "Bottleneck framework applies data analysis, simulation, and operational review to identify constraints. Mitigation strategies include infrastructure upgrades, timetable changes, and operational improvements. "
            "Stakeholder engagement and cost-benefit analysis guide decision-making. Continuous improvement and regulatory compliance are integral to robust mitigation."
        ),
        key_factors=[
            "Data analysis",
            "Simulation",
            "Operational review",
            "Infrastructure upgrades",
            "Timetable changes"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Operations Manager",
        adversary_position="Operators may dispute mitigation priorities.",
        counter_arguments=[
            "Mitigation must be prioritized based on impact and feasibility.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Mitigation strategies are implemented through phased investment and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Bottleneck Mitigation Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Timetable Construction and Validation",
        keywords=["timetable construction", "validation", "rail network", "operations", "scheduling"],
        conclusion_template="Timetable construction and validation apply simulation, operational analysis, and stakeholder engagement to ensure feasible and reliable train schedules.",
        reasoning_framework=(
            "Timetable framework applies simulation, operational analysis, and stakeholder engagement to construct and validate train schedules. The process includes scenario analysis, conflict resolution, and empirical validation. "
            "Regulatory compliance and continuous improvement enhance timetable reliability and feasibility."
        ),
        key_factors=[
            "Simulation",
            "Operational analysis",
            "Stakeholder engagement",
            "Scenario analysis",
            "Conflict resolution"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Scheduling Analyst",
        adversary_position="Operators may dispute timetable assumptions.",
        counter_arguments=[
            "Assumptions must be evidence-based.",
            "Validation enhances reliability.",
            "Stakeholder engagement improves outcomes."
        ],
        resolution_strategy="Timetables are reviewed and refined through simulation and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Timetable Construction Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Maintenance Planning and Optimization",
        keywords=["maintenance planning", "optimization", "rail network", "asset management", "operations"],
        conclusion_template="Maintenance planning and optimization apply asset condition assessment, scheduling algorithms, and stakeholder engagement to ensure reliable network performance.",
        reasoning_framework=(
            "Maintenance framework applies asset condition assessment, scheduling algorithms, and stakeholder engagement to optimize maintenance activities. The process includes risk assessment, cost modeling, and regulatory compliance. "
            "Continuous improvement and adaptive management enhance maintenance outcomes."
        ),
        key_factors=[
            "Asset condition assessment",
            "Scheduling algorithms",
            "Stakeholder engagement",
            "Risk assessment",
            "Cost modeling"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Maintenance Manager",
        adversary_position="Operators may dispute maintenance priorities.",
        counter_arguments=[
            "Priorities must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement improves outcomes."
        ],
        resolution_strategy="Maintenance plans are reviewed and refined through stakeholder collaboration and regulatory oversight.",
        entity_scope="Rail network planning and operations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FRA Maintenance Planning Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Investment Prioritization and Stakeholder Engagement",
        keywords=["investment prioritization", "stakeholder engagement", "rail network", "planning", "operations"],
        conclusion_template="Investment prioritization applies cost-benefit analysis, risk assessment, and stakeholder engagement to guide rail network funding decisions.",
        reasoning_framework=(
            "Prioritization framework applies cost-benefit analysis, risk assessment, and stakeholder engagement to guide investment decisions. The process includes scenario analysis, regulatory compliance, and continuous improvement. "
            "Stakeholder collaboration ensures transparency and alignment with operational objectives."
        ),
        key_factors=[
            "Cost-benefit analysis",
            "Risk assessment",
            "Stakeholder engagement",
            "Scenario analysis",
            "Regulatory compliance"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Investment Manager",
        adversary_position="Operators may dispute prioritization outcomes.",
        counter_arguments=[
            "Outcomes must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement improves transparency."
        ],
        resolution_strategy="Prioritization is guided by robust analysis and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Investment Prioritization Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Sustainability and Environmental Stewardship",
        keywords=["sustainability", "environmental stewardship", "rail network", "operations", "planning"],
        conclusion_template="Sustainability and environmental stewardship apply best practices, regulatory compliance, and stakeholder engagement to minimize rail network environmental impact.",
        reasoning_framework=(
            "Sustainability framework applies best practices, regulatory compliance, and stakeholder engagement to minimize environmental impact. The process includes impact assessment, mitigation planning, and continuous improvement. "
            "Regulatory mandates and public input guide stewardship initiatives."
        ),
        key_factors=[
            "Best practices",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Impact assessment",
            "Mitigation planning"
        ],
        primary_authority=["EPA", "FRA", "USDOT"],
        burden_holder="Environmental Manager",
        adversary_position="Operators may dispute stewardship requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Stewardship initiatives are guided by best practices and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="EPA Rail Sustainability Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Digitalization and Data Analytics",
        keywords=["digitalization", "data analytics", "rail network", "operations", "planning"],
        conclusion_template="Digitalization and data analytics apply advanced technologies, regulatory compliance, and stakeholder engagement to optimize rail network performance.",
        reasoning_framework=(
            "Digitalization framework applies advanced technologies, regulatory compliance, and stakeholder engagement to optimize performance. The process includes data collection, analysis, and continuous improvement. "
            "Regulatory mandates and stakeholder input guide digitalization initiatives."
        ),
        key_factors=[
            "Advanced technologies",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Data collection and analysis",
            "Continuous improvement"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="IT Manager",
        adversary_position="Operators may dispute technology investment priorities.",
        counter_arguments=[
            "Priorities must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement improves outcomes."
        ],
        resolution_strategy="Digitalization is guided by technology adoption and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Digitalization Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Accessibility and Universal Design",
        keywords=["accessibility", "universal design", "rail network", "operations", "planning"],
        conclusion_template="Accessibility and universal design apply regulatory standards, best practices, and stakeholder engagement to ensure inclusive rail network operations.",
        reasoning_framework=(
            "Accessibility framework applies regulatory standards, best practices, and stakeholder engagement to ensure inclusivity. The process includes design review, impact assessment, and continuous improvement. "
            "Regulatory mandates and public input guide accessibility initiatives."
        ),
        key_factors=[
            "Regulatory standards",
            "Best practices",
            "Stakeholder engagement",
            "Design review",
            "Impact assessment"
        ],
        primary_authority=["ADA", "FRA", "USDOT"],
        burden_holder="Design Manager",
        adversary_position="Operators may dispute accessibility requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Accessibility initiatives are guided by regulatory standards and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="ADA Rail Accessibility Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Noise and Vibration Mitigation",
        keywords=["noise", "vibration", "mitigation", "rail network", "operations"],
        conclusion_template="Noise and vibration mitigation applies engineering controls, regulatory compliance, and stakeholder engagement to minimize community impact.",
        reasoning_framework=(
            "Mitigation framework applies engineering controls, regulatory compliance, and stakeholder engagement to minimize noise and vibration impact. The process includes impact assessment, technology adoption, and continuous improvement. "
            "Regulatory mandates and public input guide mitigation initiatives."
        ),
        key_factors=[
            "Engineering controls",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Impact assessment",
            "Technology adoption"
        ],
        primary_authority=["EPA", "FRA", "USDOT"],
        burden_holder="Environmental Manager",
        adversary_position="Operators may dispute mitigation requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Mitigation initiatives are guided by engineering controls and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="EPA Rail Noise Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Climate Adaptation and Risk Management",
        keywords=["climate adaptation", "risk management", "rail network", "operations"],
        conclusion_template="Climate adaptation and risk management apply scenario analysis, regulatory compliance, and stakeholder engagement to enhance rail network resilience.",
        reasoning_framework=(
            "Adaptation framework applies scenario analysis, regulatory compliance, and stakeholder engagement to enhance resilience. The process includes risk assessment, impact modeling, and continuous improvement. "
            "Regulatory mandates and stakeholder input guide adaptation initiatives."
        ),
        key_factors=[
            "Scenario analysis",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Risk assessment",
            "Impact modeling"
        ],
        primary_authority=["EPA", "FRA", "USDOT"],
        burden_holder="Risk Manager",
        adversary_position="Operators may dispute adaptation priorities.",
        counter_arguments=[
            "Priorities must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement improves outcomes."
        ],
        resolution_strategy="Adaptation initiatives are guided by scenario analysis and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="EPA Rail Climate Adaptation Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Energy Efficiency and Emissions Reduction",
        keywords=["energy efficiency", "emissions reduction", "rail network", "operations"],
        conclusion_template="Energy efficiency and emissions reduction apply best practices, regulatory compliance, and stakeholder engagement to minimize rail network environmental impact.",
        reasoning_framework=(
            "Efficiency framework applies best practices, regulatory compliance, and stakeholder engagement to minimize environmental impact. The process includes impact assessment, technology adoption, and continuous improvement. "
            "Regulatory mandates and public input guide efficiency initiatives."
        ),
        key_factors=[
            "Best practices",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Impact assessment",
            "Technology adoption"
        ],
        primary_authority=["EPA", "FRA", "USDOT"],
        burden_holder="Environmental Manager",
        adversary_position="Operators may dispute efficiency requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Efficiency initiatives are guided by best practices and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="EPA Rail Energy Efficiency Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Innovation and Technology Adoption",
        keywords=["innovation", "technology adoption", "rail network", "operations"],
        conclusion_template="Innovation and technology adoption apply advanced technologies, regulatory compliance, and stakeholder engagement to optimize rail network performance.",
        reasoning_framework=(
            "Innovation framework applies advanced technologies, regulatory compliance, and stakeholder engagement to optimize performance. The process includes technology evaluation, impact assessment, and continuous improvement. "
            "Regulatory mandates and stakeholder input guide innovation initiatives."
        ),
        key_factors=[
            "Advanced technologies",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Technology evaluation",
            "Impact assessment"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Innovation Manager",
        adversary_position="Operators may dispute technology investment priorities.",
        counter_arguments=[
            "Priorities must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement improves outcomes."
        ],
        resolution_strategy="Innovation is guided by technology adoption and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Innovation Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Public Engagement and Communication",
        keywords=["public engagement", "communication", "rail network", "operations"],
        conclusion_template="Public engagement and communication apply best practices, regulatory compliance, and stakeholder collaboration to ensure transparent rail network operations.",
        reasoning_framework=(
            "Engagement framework applies best practices, regulatory compliance, and stakeholder collaboration to ensure transparency. The process includes communication planning, public input, and continuous improvement. "
            "Regulatory mandates and stakeholder input guide engagement initiatives."
        ),
        key_factors=[
            "Best practices",
            "Regulatory compliance",
            "Stakeholder collaboration",
            "Communication planning",
            "Public input"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Communications Manager",
        adversary_position="Operators may dispute engagement requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder collaboration enhances outcomes."
        ],
        resolution_strategy="Engagement initiatives are guided by best practices and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Public Engagement Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Equity and Social Impact Assessment",
        keywords=["equity", "social impact", "rail network", "operations"],
        conclusion_template="Equity and social impact assessment apply best practices, regulatory compliance, and stakeholder engagement to ensure inclusive rail network operations.",
        reasoning_framework=(
            "Equity framework applies best practices, regulatory compliance, and stakeholder engagement to ensure inclusivity. The process includes impact assessment, mitigation planning, and continuous improvement. "
            "Regulatory mandates and public input guide equity initiatives."
        ),
        key_factors=[
            "Best practices",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Impact assessment",
            "Mitigation planning"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Equity Manager",
        adversary_position="Operators may dispute equity requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Equity initiatives are guided by best practices and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Equity Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Incident Management and Emergency Response",
        keywords=["incident management", "emergency response", "rail network", "operations"],
        conclusion_template="Incident management and emergency response apply best practices, regulatory compliance, and stakeholder engagement to ensure rapid and effective rail network recovery.",
        reasoning_framework=(
            "Incident management framework applies best practices, regulatory compliance, and stakeholder engagement to ensure rapid recovery. The process includes response planning, impact assessment, and continuous improvement. "
            "Regulatory mandates and stakeholder input guide incident management initiatives."
        ),
        key_factors=[
            "Best practices",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Response planning",
            "Impact assessment"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Incident Manager",
        adversary_position="Operators may dispute response requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Incident management is guided by best practices and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Incident Management Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Workforce Development and Training",
        keywords=["workforce development", "training", "rail network", "operations"],
        conclusion_template="Workforce development and training apply best practices, regulatory compliance, and stakeholder engagement to ensure skilled rail network operations.",
        reasoning_framework=(
            "Workforce development framework applies best practices, regulatory compliance, and stakeholder engagement to ensure skilled operations. The process includes training planning, skill assessment, and continuous improvement. "
            "Regulatory mandates and stakeholder input guide workforce development initiatives."
        ),
        key_factors=[
            "Best practices",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Training planning",
            "Skill assessment"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Training Manager",
        adversary_position="Operators may dispute training requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Workforce development is guided by best practices and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Workforce Development Standards"
    ),
    DoctrineBlock(
        topic="Rail Network Data Governance and Quality Assurance",
        keywords=["data governance", "quality assurance", "rail network", "operations"],
        conclusion_template="Data governance and quality assurance apply best practices, regulatory compliance, and stakeholder engagement to ensure reliable rail network data management.",
        reasoning_framework=(
            "Data governance framework applies best practices, regulatory compliance, and stakeholder engagement to ensure reliable data management. The process includes quality assurance planning, impact assessment, and continuous improvement. "
            "Regulatory mandates and stakeholder input guide data governance initiatives."
        ),
        key_factors=[
            "Best practices",
            "Regulatory compliance",
            "Stakeholder engagement",
            "Quality assurance planning",
            "Impact assessment"
        ],
        primary_authority=["FRA", "USDOT", "AAR"],
        burden_holder="Data Manager",
        adversary_position="Operators may dispute data governance requirements.",
        counter_arguments=[
            "Requirements must be evidence-based.",
            "Regulatory mandates require compliance.",
            "Stakeholder engagement enhances outcomes."
        ],
        resolution_strategy="Data governance is guided by best practices and stakeholder collaboration.",
        entity_scope="Rail network planning and operations",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="FRA Data Governance Standards"
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