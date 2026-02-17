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
        topic="Cyclic Timetabling and PESP Model",
        keywords=["timetabling", "periodic event scheduling", "PESP", "rail operations", "schedule optimization"],
        conclusion_template="The application of cyclic timetabling via the PESP model ensures robust, repeatable schedules that maximize passenger convenience and operational efficiency.",
        reasoning_framework="""
The Periodic Event Scheduling Problem (PESP) is a mathematical model used to design cyclic timetables for passenger rail systems. The model optimizes event times (departures, arrivals) within a cycle (typically hourly) to minimize passenger transfer times and maximize resource utilization. Key constraints include track capacity, rolling stock availability, and crew scheduling. The framework integrates passenger demand data, station dwell times, and operational reliability targets. Solutions are evaluated for feasibility, robustness against disruptions, and compliance with regulatory requirements. The model is solved using integer programming, with sensitivity analysis to assess impacts of parameter changes. Stakeholder input (passenger, operator, regulator) is incorporated to refine objectives and constraints.
""",
        key_factors=[
            "Passenger transfer times",
            "Rolling stock utilization",
            "Crew scheduling constraints",
            "Track and platform capacity",
            "Regulatory timetable requirements",
            "Robustness against disruptions"
        ],
        primary_authority=[
            "EN 50126 Railway Applications",
            "UIC Code 406",
            "Federal Railroad Administration (FRA)"
        ],
        burden_holder="Rail Operator",
        adversary_position="Non-cyclic or ad-hoc scheduling offers greater flexibility and responsiveness.",
        counter_arguments=[
            "Cyclic timetabling can reduce adaptability to real-time demand fluctuations.",
            "Complexity of integer programming may limit practical implementation.",
            "Potential for increased operational rigidity."
        ],
        resolution_strategy="Hybrid scheduling with periodic review and real-time adjustments.",
        entity_scope="Passenger Rail Network",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Swiss Federal Railways (SBB) Cyclic Timetable Implementation"
    ),
    DoctrineBlock(
        topic="Rolling Stock Assignment and Fleet Optimization",
        keywords=["rolling stock", "fleet management", "assignment", "optimization", "resource allocation"],
        conclusion_template="Optimal rolling stock assignment ensures efficient fleet utilization, minimizes operational costs, and meets passenger demand reliably.",
        reasoning_framework="""
Fleet optimization involves assigning rolling stock units to scheduled services based on capacity, maintenance cycles, and operational constraints. The process uses mixed-integer programming to balance vehicle availability, minimize empty runs, and reduce maintenance downtime. Demand forecasting informs assignment, ensuring adequate capacity during peak periods. Maintenance windows, regulatory compliance (FRA, AAR standards), and interoperability (cross-border operations) are factored. The framework includes scenario analysis for disruptions (equipment failure, demand spikes) and integrates real-time monitoring for dynamic reassignment. Stakeholder engagement (maintenance teams, operations, passengers) guides prioritization.
""",
        key_factors=[
            "Fleet size and composition",
            "Maintenance scheduling",
            "Passenger demand patterns",
            "Regulatory compliance",
            "Interoperability requirements"
        ],
        primary_authority=[
            "FRA Passenger Equipment Safety Standards",
            "AAR Manual of Standards",
            "EN 15227 Crashworthiness"
        ],
        burden_holder="Fleet Manager",
        adversary_position="Static assignment reduces flexibility and may lead to underutilization.",
        counter_arguments=[
            "Dynamic assignment increases complexity and may disrupt maintenance cycles.",
            "Over-optimization can reduce redundancy needed for reliability.",
            "Interoperability challenges with mixed fleets."
        ],
        resolution_strategy="Integrated fleet management system with real-time data and periodic optimization reviews.",
        entity_scope="Rolling Stock Fleet",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Deutsche Bahn Rolling Stock Optimization Model"
    ),
    DoctrineBlock(
        topic="Crew Scheduling and Labor Compliance",
        keywords=["crew scheduling", "labor compliance", "shift optimization", "fatigue management", "union agreements"],
        conclusion_template="Crew scheduling must comply with labor regulations, optimize shift patterns, and ensure operational reliability.",
        reasoning_framework="""
Crew scheduling is governed by labor laws, union agreements, and operational requirements. The framework uses constraint-based optimization to assign shifts, minimize fatigue, and ensure coverage. Key factors include maximum hours, mandatory rest periods, skill requirements, and route familiarity. Scheduling integrates real-time changes (delays, absences) and supports dynamic reassignment. Compliance is monitored via automated systems, with regular audits. Stakeholder input from unions and management shapes policy. Dispute resolution mechanisms address conflicts between operational needs and labor protections.
""",
        key_factors=[
            "Labor law compliance",
            "Union contract terms",
            "Fatigue management",
            "Skill and route requirements",
            "Operational reliability"
        ],
        primary_authority=[
            "FRA Hours of Service Regulations",
            "Railway Labor Act",
            "National Mediation Board"
        ],
        burden_holder="Operations Manager",
        adversary_position="Flexible scheduling increases efficiency but may violate labor protections.",
        counter_arguments=[
            "Strict compliance can reduce operational flexibility.",
            "Dynamic reassignment may conflict with union agreements.",
            "Fatigue management requirements increase complexity."
        ],
        resolution_strategy="Collaborative scheduling platform with compliance monitoring and dispute resolution.",
        entity_scope="Crew Operations",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak Crew Scheduling Compliance Program"
    ),
    DoctrineBlock(
        topic="Station Dwell Time Analysis and Passenger Flow",
        keywords=["station dwell time", "passenger flow", "boarding", "alighting", "platform management"],
        conclusion_template="Optimizing station dwell times improves passenger flow, reduces delays, and enhances service reliability.",
        reasoning_framework="""
Dwell time analysis uses empirical data on boarding/alighting rates, platform design, and train configuration. The framework models passenger flow using queuing theory and simulation, identifying bottlenecks and optimizing platform layouts. Key factors include train frequency, passenger density, accessibility features, and information systems. Real-time monitoring enables adaptive dwell time management. Regulatory standards (ADA, FRA) guide design. Stakeholder feedback (passengers, station staff) informs improvements. Periodic reviews assess effectiveness and update strategies.
""",
        key_factors=[
            "Passenger boarding/alighting rates",
            "Platform design",
            "Train frequency",
            "Accessibility features",
            "Real-time monitoring"
        ],
        primary_authority=[
            "ADA Accessibility Guidelines",
            "FRA Station Standards",
            "EN 14752 Doors and Dwell Times"
        ],
        burden_holder="Station Manager",
        adversary_position="Short dwell times increase punctuality but may compromise passenger safety and comfort.",
        counter_arguments=[
            "Long dwell times reduce operational efficiency.",
            "Insufficient dwell time increases risk of accidents.",
            "Platform congestion impacts passenger experience."
        ],
        resolution_strategy="Adaptive dwell time management with real-time passenger flow monitoring.",
        entity_scope="Station Operations",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="London Underground Dwell Time Optimization"
    ),
    DoctrineBlock(
        topic="Fare Structure Design and Revenue Optimization",
        keywords=["fare structure", "revenue optimization", "pricing", "ticketing", "passenger segmentation"],
        conclusion_template="A well-designed fare structure balances revenue optimization, passenger affordability, and equitable access.",
        reasoning_framework="""
Fare structure design employs economic modeling, demand elasticity analysis, and segmentation strategies. The framework evaluates flat, zonal, and distance-based fares, considering operational costs, revenue targets, and passenger demographics. Regulatory requirements (public service obligations, anti-discrimination laws) are integrated. Stakeholder engagement (passenger groups, regulators) informs policy. Dynamic pricing and loyalty programs are assessed for revenue impact. Periodic reviews and pilot programs test effectiveness. Data analytics support real-time adjustments and fraud detection.
""",
        key_factors=[
            "Passenger demand elasticity",
            "Operational costs",
            "Regulatory requirements",
            "Demographic segmentation",
            "Revenue targets"
        ],
        primary_authority=[
            "FTA Fare Policy Guidelines",
            "FRA Revenue Standards",
            "Public Service Obligation Regulations"
        ],
        burden_holder="Finance Manager",
        adversary_position="Complex fare structures may reduce transparency and passenger satisfaction.",
        counter_arguments=[
            "Flat fares can limit revenue potential.",
            "Dynamic pricing may be perceived as unfair.",
            "Complexity increases administrative costs."
        ],
        resolution_strategy="Hybrid fare structures with periodic review and stakeholder consultation.",
        entity_scope="Passenger Rail Network",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Fare Structure Model"
    ),
    DoctrineBlock(
        topic="On-Time Performance (OTP) Metrics and Reliability",
        keywords=["on-time performance", "OTP", "reliability", "punctuality", "service quality"],
        conclusion_template="OTP metrics are essential for measuring reliability, informing operational improvements, and meeting regulatory targets.",
        reasoning_framework="""
OTP is measured by the percentage of trains arriving within a defined window of scheduled time. The framework incorporates delay attribution, root cause analysis, and corrective action planning. Key factors include infrastructure reliability, rolling stock performance, crew punctuality, and external disruptions. Regulatory standards (FRA, FTA) set minimum targets. Data analytics support real-time monitoring and predictive maintenance. Stakeholder feedback (passengers, operators) guides improvement initiatives. Periodic benchmarking against peer systems informs strategy.
""",
        key_factors=[
            "Delay attribution",
            "Infrastructure reliability",
            "Rolling stock performance",
            "Crew punctuality",
            "External disruptions"
        ],
        primary_authority=[
            "FRA On-Time Performance Standards",
            "FTA Service Quality Guidelines",
            "EN 50126 Reliability"
        ],
        burden_holder="Operations Manager",
        adversary_position="Strict OTP targets may incentivize schedule padding and reduce service frequency.",
        counter_arguments=[
            "OTP metrics can be manipulated.",
            "Focus on punctuality may overlook passenger experience.",
            "External factors limit control."
        ],
        resolution_strategy="Balanced scorecard approach with multi-dimensional performance metrics.",
        entity_scope="Passenger Rail Network",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak OTP Reporting Framework"
    ),
    DoctrineBlock(
        topic="Platform Screen Doors (PSD) Safety and Operations",
        keywords=["platform screen doors", "PSD", "safety", "operations", "passenger protection"],
        conclusion_template="PSD implementation enhances passenger safety, reduces accidents, and supports efficient station operations.",
        reasoning_framework="""
PSD systems are evaluated for safety, operational integration, and passenger flow impact. The framework assesses technical compatibility with rolling stock, emergency procedures, and maintenance requirements. Regulatory standards (EN 50126, ADA) guide design. Stakeholder input (passengers, station staff, emergency services) informs operational protocols. Cost-benefit analysis evaluates investment versus safety gains. Periodic testing and drills ensure readiness. Real-time monitoring supports incident response and maintenance scheduling.
""",
        key_factors=[
            "Technical compatibility",
            "Safety standards",
            "Emergency procedures",
            "Maintenance requirements",
            "Passenger flow impact"
        ],
        primary_authority=[
            "EN 50126 Railway Safety",
            "ADA Accessibility Guidelines",
            "FRA Station Safety Standards"
        ],
        burden_holder="Station Manager",
        adversary_position="PSD installation increases capital and maintenance costs, and may impede passenger flow.",
        counter_arguments=[
            "PSD may limit flexibility in train operations.",
            "Maintenance complexity increases operational risk.",
            "Cost may outweigh safety benefits in low-volume stations."
        ],
        resolution_strategy="Risk-based PSD deployment with periodic safety audits.",
        entity_scope="Station Operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hong Kong MTR PSD Safety Program"
    ),
    DoctrineBlock(
        topic="ADA Accessibility Compliance and Universal Design",
        keywords=["ADA", "accessibility", "universal design", "station compliance", "passenger inclusion"],
        conclusion_template="ADA compliance and universal design principles ensure equitable access for all passengers and reduce legal risk.",
        reasoning_framework="""
Accessibility compliance is mandated by ADA and reinforced by universal design principles. The framework evaluates station and rolling stock features (ramps, lifts, signage, auditory/visual information), integrating passenger feedback and regulatory audits. Key factors include physical access, information accessibility, and staff training. Stakeholder engagement (disability advocacy groups, regulators) informs improvements. Periodic reviews and upgrades maintain compliance. Legal risk assessment guides prioritization. Universal design supports broader passenger inclusion and operational flexibility.
""",
        key_factors=[
            "Physical access features",
            "Information accessibility",
            "Staff training",
            "Regulatory audits",
            "Passenger feedback"
        ],
        primary_authority=[
            "ADA Accessibility Guidelines",
            "FRA Station Standards",
            "EN 301549 Accessibility"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Accessibility upgrades increase capital costs and may disrupt operations.",
        counter_arguments=[
            "Universal design can reduce operational efficiency.",
            "Compliance requirements may exceed passenger demand.",
            "Retrofits are costly and complex."
        ],
        resolution_strategy="Phased accessibility upgrades with stakeholder consultation and risk assessment.",
        entity_scope="Station and Rolling Stock",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="New York City Transit ADA Compliance Program"
    ),
    DoctrineBlock(
        topic="Positive Train Control (PTC) for Passenger Rail",
        keywords=["positive train control", "PTC", "safety", "signal systems", "collision prevention"],
        conclusion_template="PTC implementation is critical for passenger rail safety, regulatory compliance, and operational reliability.",
        reasoning_framework="""
PTC systems prevent train-to-train collisions, overspeed derailments, and unauthorized incursions. The framework evaluates technical integration, interoperability, and regulatory compliance. Key factors include signal system compatibility, communication infrastructure, and maintenance protocols. Stakeholder input (operators, regulators, technology vendors) guides deployment. Cost-benefit analysis assesses investment versus safety gains. Periodic testing and incident reviews ensure effectiveness. Regulatory deadlines (FRA) drive prioritization. Real-time monitoring supports operational reliability.
""",
        key_factors=[
            "Signal system compatibility",
            "Communication infrastructure",
            "Regulatory compliance",
            "Maintenance protocols",
            "Interoperability"
        ],
        primary_authority=[
            "FRA PTC Regulations",
            "EN 50126 Safety",
            "AAR Signal Standards"
        ],
        burden_holder="Safety Manager",
        adversary_position="PTC implementation increases capital and operational costs, and may disrupt legacy systems.",
        counter_arguments=[
            "Technical integration challenges.",
            "Cost may outweigh safety benefits in low-risk corridors.",
            "Interoperability issues with mixed fleets."
        ],
        resolution_strategy="Phased PTC deployment with risk-based prioritization and interoperability testing.",
        entity_scope="Passenger Rail Network",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak PTC Implementation Program"
    ),
    DoctrineBlock(
        topic="Passenger Demand Forecasting and Ridership Modeling",
        keywords=["demand forecasting", "ridership modeling", "passenger analytics", "service planning", "capacity management"],
        conclusion_template="Accurate demand forecasting and ridership modeling inform service planning, capacity management, and revenue optimization.",
        reasoning_framework="""
Demand forecasting uses historical data, demographic trends, and econometric modeling to predict ridership. The framework integrates real-time data, special event impacts, and seasonal variations. Key factors include population growth, economic indicators, and competing modes. Stakeholder input (passengers, planners, regulators) refines models. Scenario analysis assesses impacts of service changes, fare adjustments, and external disruptions. Data analytics and machine learning support continuous improvement. Periodic validation ensures accuracy.
""",
        key_factors=[
            "Historical ridership data",
            "Demographic trends",
            "Economic indicators",
            "Competing transport modes",
            "Special events"
        ],
        primary_authority=[
            "FTA Ridership Modeling Guidelines",
            "FRA Service Planning Standards",
            "EN 50126 Reliability"
        ],
        burden_holder="Planning Manager",
        adversary_position="Forecasting models may fail to capture real-time demand fluctuations and external shocks.",
        counter_arguments=[
            "Model complexity increases resource requirements.",
            "Over-reliance on historical data may reduce adaptability.",
            "External disruptions limit predictive accuracy."
        ],
        resolution_strategy="Hybrid modeling with real-time data integration and periodic model validation.",
        entity_scope="Passenger Rail Network",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Ridership Forecasting Model"
    ),
    DoctrineBlock(
        topic="Load Factor and Crowding Management",
        keywords=["load factor", "crowding", "capacity management", "passenger comfort", "service reliability"],
        conclusion_template="Effective load factor and crowding management enhance passenger comfort, safety, and operational reliability.",
        reasoning_framework="""
Load factor analysis evaluates passenger density relative to vehicle capacity. The framework models crowding impacts on safety, comfort, and dwell times. Real-time monitoring informs dynamic capacity adjustments (train length, frequency). Key factors include demand patterns, rolling stock configuration, and station design. Regulatory standards (FRA, ADA) guide minimum comfort and safety levels. Stakeholder feedback (passengers, staff) informs improvements. Scenario analysis assesses impacts of service changes and disruptions.
""",
        key_factors=[
            "Passenger density",
            "Vehicle capacity",
            "Rolling stock configuration",
            "Station design",
            "Real-time monitoring"
        ],
        primary_authority=[
            "FRA Passenger Comfort Standards",
            "ADA Accessibility Guidelines",
            "EN 14752 Dwell Times"
        ],
        burden_holder="Operations Manager",
        adversary_position="Increasing capacity may reduce operational efficiency and increase costs.",
        counter_arguments=[
            "Crowding can reduce passenger satisfaction.",
            "Excess capacity increases operational costs.",
            "Dynamic adjustments may disrupt schedules."
        ],
        resolution_strategy="Adaptive capacity management with real-time monitoring and periodic reviews.",
        entity_scope="Passenger Rail Network",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tokyo Metro Load Factor Management"
    ),
    DoctrineBlock(
        topic="FRA Passenger Equipment Safety Standards",
        keywords=["FRA", "passenger equipment", "safety standards", "regulatory compliance", "rolling stock"],
        conclusion_template="Compliance with FRA passenger equipment safety standards is mandatory for operational approval and passenger protection.",
        reasoning_framework="""
FRA standards govern structural integrity, crashworthiness, fire safety, and emergency systems for passenger rolling stock. The framework evaluates design, manufacturing, and maintenance practices. Key factors include material selection, safety system integration, and periodic inspections. Regulatory audits and certification processes ensure compliance. Stakeholder input (manufacturers, operators, regulators) guides continuous improvement. Incident reviews inform updates. Non-compliance results in operational restrictions and legal penalties.
""",
        key_factors=[
            "Structural integrity",
            "Crashworthiness",
            "Fire safety",
            "Emergency systems",
            "Maintenance practices"
        ],
        primary_authority=[
            "FRA Passenger Equipment Safety Standards",
            "EN 15227 Crashworthiness",
            "AAR Manual of Standards"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Safety upgrades increase capital costs and may disrupt operations.",
        counter_arguments=[
            "Compliance requirements may exceed operational needs.",
            "Retrofits are costly and complex.",
            "Certification delays impact service launch."
        ],
        resolution_strategy="Phased compliance upgrades with risk assessment and stakeholder engagement.",
        entity_scope="Rolling Stock Fleet",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak FRA Compliance Program"
    ),
    DoctrineBlock(
        topic="Station Parking and Park-and-Ride Facilities",
        keywords=["station parking", "park-and-ride", "accessibility", "passenger convenience", "land use"],
        conclusion_template="Effective station parking and park-and-ride facilities enhance accessibility, increase ridership, and support transit-oriented development.",
        reasoning_framework="""
Station parking and park-and-ride facilities are evaluated for capacity, accessibility, and integration with local land use. The framework considers demand forecasting, pricing strategies, and environmental impacts. Key factors include passenger demographics, station location, and competing transport modes. Regulatory standards (ADA, local zoning) guide design. Stakeholder input (passengers, local authorities) informs planning. Scenario analysis assesses impacts of facility expansion, pricing changes, and modal shifts. Periodic reviews ensure alignment with ridership targets and land use policies.
""",
        key_factors=[
            "Parking capacity",
            "Accessibility",
            "Pricing strategies",
            "Environmental impact",
            "Land use integration"
        ],
        primary_authority=[
            "ADA Accessibility Guidelines",
            "Local Zoning Regulations",
            "FTA Park-and-Ride Guidelines"
        ],
        burden_holder="Planning Manager",
        adversary_position="Parking expansion may increase car dependency and conflict with transit-oriented development goals.",
        counter_arguments=[
            "Limited parking reduces accessibility.",
            "Excess parking increases environmental impact.",
            "Pricing changes may reduce ridership."
        ],
        resolution_strategy="Balanced facility planning with stakeholder engagement and environmental assessment.",
        entity_scope="Station Operations",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bay Area Rapid Transit Park-and-Ride Program"
    ),
    DoctrineBlock(
        topic="Passenger Information Systems (PIS) and Real-Time Data",
        keywords=["passenger information systems", "PIS", "real-time data", "service updates", "communication"],
        conclusion_template="Robust PIS and real-time data systems improve passenger experience, operational efficiency, and incident response.",
        reasoning_framework="""
PIS integrates real-time service updates, delay notifications, and multimodal information. The framework evaluates technical reliability, accessibility, and data accuracy. Key factors include system integration, user interface design, and communication protocols. Regulatory standards (ADA, FRA) guide information accessibility. Stakeholder feedback (passengers, staff) informs improvements. Incident reviews assess effectiveness. Periodic upgrades maintain system reliability and relevance. Data analytics support predictive incident management.
""",
        key_factors=[
            "Technical reliability",
            "Information accessibility",
            "User interface design",
            "Data accuracy",
            "System integration"
        ],
        primary_authority=[
            "ADA Accessibility Guidelines",
            "FRA Information Standards",
            "EN 301549 Accessibility"
        ],
        burden_holder="IT Manager",
        adversary_position="System upgrades increase capital costs and may disrupt operations.",
        counter_arguments=[
            "Technical failures impact passenger experience.",
            "Complexity increases maintenance requirements.",
            "Data privacy concerns."
        ],
        resolution_strategy="Phased system upgrades with stakeholder consultation and risk assessment.",
        entity_scope="Passenger Rail Network",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London PIS Implementation"
    ),
    DoctrineBlock(
        topic="Cross-Border and Inter-City Passenger Rail Operations",
        keywords=["cross-border", "inter-city", "passenger rail", "interoperability", "regulatory compliance"],
        conclusion_template="Cross-border and inter-city operations require robust interoperability, regulatory compliance, and coordinated service planning.",
        reasoning_framework="""
Cross-border and inter-city operations are governed by international agreements, technical standards, and regulatory compliance. The framework evaluates interoperability (track gauge, signaling, rolling stock), customs procedures, and service coordination. Key factors include passenger demand, infrastructure compatibility, and legal requirements. Stakeholder engagement (operators, regulators, passengers) guides planning. Scenario analysis assesses impacts of service changes, disruptions, and regulatory updates. Periodic reviews ensure alignment with international standards and passenger needs.
""",
        key_factors=[
            "Interoperability",
            "Regulatory compliance",
            "Customs procedures",
            "Infrastructure compatibility",
            "Service coordination"
        ],
        primary_authority=[
            "UIC International Rail Standards",
            "FRA Cross-Border Regulations",
            "EN 50126 Reliability"
        ],
        burden_holder="Operations Manager",
        adversary_position="Interoperability challenges increase operational complexity and cost.",
        counter_arguments=[
            "Regulatory differences limit service integration.",
            "Customs procedures increase passenger inconvenience.",
            "Infrastructure upgrades are costly."
        ],
        resolution_strategy="Coordinated planning with international stakeholders and phased interoperability upgrades.",
        entity_scope="Passenger Rail Network",
        confidence=0.81,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Eurostar Cross-Border Operations"
    ),
    DoctrineBlock(
        topic="Energy Consumption and Regenerative Braking",
        keywords=["energy consumption", "regenerative braking", "sustainability", "operational efficiency", "environmental impact"],
        conclusion_template="Optimizing energy consumption and deploying regenerative braking reduces operational costs and environmental impact.",
        reasoning_framework="""
Energy consumption is analyzed using real-time monitoring, operational modeling, and sustainability targets. Regenerative braking systems recover energy during deceleration, reducing net consumption. The framework evaluates technical integration, maintenance requirements, and regulatory incentives. Key factors include rolling stock configuration, service frequency, and infrastructure compatibility. Stakeholder input (operators, regulators, environmental groups) informs policy. Cost-benefit analysis assesses investment versus savings. Periodic reviews and upgrades maintain efficiency.
""",
        key_factors=[
            "Rolling stock configuration",
            "Service frequency",
            "Infrastructure compatibility",
            "Maintenance requirements",
            "Regulatory incentives"
        ],
        primary_authority=[
            "EN 50126 Energy Efficiency",
            "FRA Environmental Standards",
            "UIC Sustainability Guidelines"
        ],
        burden_holder="Sustainability Manager",
        adversary_position="Regenerative braking increases maintenance complexity and may not deliver expected savings.",
        counter_arguments=[
            "Technical integration challenges.",
            "Savings depend on operational patterns.",
            "Maintenance costs may offset benefits."
        ],
        resolution_strategy="Phased deployment with real-time monitoring and periodic efficiency reviews.",
        entity_scope="Rolling Stock Fleet",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Deutsche Bahn Regenerative Braking Program"
    ),
    DoctrineBlock(
        topic="Station Design and Passenger Flow Optimization",
        keywords=["station design", "passenger flow", "optimization", "layout", "accessibility"],
        conclusion_template="Optimized station design improves passenger flow, accessibility, and operational reliability.",
        reasoning_framework="""
Station design is evaluated for passenger flow efficiency, accessibility, and operational reliability. The framework models layout using simulation and queuing theory, identifying bottlenecks and optimizing pathways. Key factors include platform configuration, signage, accessibility features, and emergency procedures. Regulatory standards (ADA, FRA) guide design. Stakeholder input (passengers, staff, emergency services) informs improvements. Periodic reviews and upgrades maintain effectiveness. Scenario analysis assesses impacts of service changes and disruptions.
""",
        key_factors=[
            "Platform configuration",
            "Signage",
            "Accessibility features",
            "Emergency procedures",
            "Passenger flow modeling"
        ],
        primary_authority=[
            "ADA Accessibility Guidelines",
            "FRA Station Standards",
            "EN 14752 Station Design"
        ],
        burden_holder="Station Manager",
        adversary_position="Design upgrades increase capital costs and may disrupt operations.",
        counter_arguments=[
            "Complex layouts reduce passenger convenience.",
            "Accessibility features increase maintenance requirements.",
            "Retrofits are costly and complex."
        ],
        resolution_strategy="Phased design upgrades with stakeholder consultation and risk assessment.",
        entity_scope="Station Operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Tokyo Metro Station Design Optimization"
    ),
    DoctrineBlock(
        topic="Service Reliability and Mean Distance Between Failures (MDBF)",
        keywords=["service reliability", "MDBF", "maintenance", "operational efficiency", "failure analysis"],
        conclusion_template="High MDBF and robust reliability engineering minimize disruptions and enhance passenger satisfaction.",
        reasoning_framework="""
MDBF measures average distance between rolling stock failures, informing maintenance and reliability strategies. The framework uses failure analysis, predictive maintenance, and root cause identification. Key factors include maintenance protocols, component quality, operational patterns, and environmental conditions. Regulatory standards (FRA, EN 50126) set minimum reliability targets. Stakeholder input (maintenance teams, operators) guides improvements. Data analytics support real-time monitoring and incident response. Periodic reviews and upgrades maintain reliability.
""",
        key_factors=[
            "Maintenance protocols",
            "Component quality",
            "Operational patterns",
            "Environmental conditions",
            "Predictive maintenance"
        ],
        primary_authority=[
            "FRA Reliability Standards",
            "EN 50126 Reliability",
            "AAR Maintenance Guidelines"
        ],
        burden_holder="Maintenance Manager",
        adversary_position="Reliability targets increase maintenance costs and may reduce operational flexibility.",
        counter_arguments=[
            "High reliability requires significant investment.",
            "Predictive maintenance increases complexity.",
            "Component quality may vary by supplier."
        ],
        resolution_strategy="Integrated reliability engineering with periodic reviews and data-driven maintenance.",
        entity_scope="Rolling Stock Fleet",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Siemens MDBF Reliability Program"
    ),
    DoctrineBlock(
        topic="Transit-Oriented Development (TOD) and Land Use Integration",
        keywords=["transit-oriented development", "TOD", "land use", "urban planning", "ridership"],
        conclusion_template="TOD and land use integration increase ridership, support sustainable urban growth, and enhance station accessibility.",
        reasoning_framework="""
TOD integrates passenger rail stations with mixed-use development, increasing accessibility and ridership. The framework evaluates land use policies, zoning regulations, and stakeholder engagement. Key factors include station location, demographic trends, and environmental impact. Regulatory standards (local zoning, ADA) guide planning. Scenario analysis assesses impacts of development, ridership, and modal shifts. Periodic reviews ensure alignment with urban growth and sustainability targets. Stakeholder input (local authorities, developers, passengers) informs strategy.
""",
        key_factors=[
            "Station location",
            "Land use policies",
            "Demographic trends",
            "Environmental impact",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "Local Zoning Regulations",
            "ADA Accessibility Guidelines",
            "FTA TOD Guidelines"
        ],
        burden_holder="Planning Manager",
        adversary_position="TOD may increase property values and reduce affordability for low-income passengers.",
        counter_arguments=[
            "Development may conflict with operational needs.",
            "Land use integration increases complexity.",
            "Environmental impact may be negative."
        ],
        resolution_strategy="Balanced TOD planning with stakeholder engagement and environmental assessment.",
        entity_scope="Station Operations",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bay Area Rapid Transit TOD Program"
    ),
    DoctrineBlock(
        topic="Emergency Preparedness and Incident Response",
        keywords=["emergency preparedness", "incident response", "safety", "evacuation", "crisis management"],
        conclusion_template="Comprehensive emergency preparedness and incident response protocols minimize risk and ensure passenger safety.",
        reasoning_framework="""
Emergency preparedness is governed by regulatory standards and best practices in crisis management. The framework evaluates evacuation procedures, communication protocols, and staff training. Key factors include infrastructure design, passenger demographics, and incident history. Stakeholder input (emergency services, passengers, staff) informs planning. Periodic drills and reviews ensure readiness. Incident analysis supports continuous improvement. Regulatory audits and certification processes maintain compliance.
""",
        key_factors=[
            "Evacuation procedures",
            "Communication protocols",
            "Staff training",
            "Infrastructure design",
            "Incident history"
        ],
        primary_authority=[
            "FRA Emergency Preparedness Standards",
            "EN 50126 Safety",
            "National Fire Protection Association (NFPA)"
        ],
        burden_holder="Safety Manager",
        adversary_position="Preparedness protocols increase operational complexity and may disrupt service.",
        counter_arguments=[
            "Drills may inconvenience passengers.",
            "Staff training increases resource requirements.",
            "Incident response may be delayed by infrastructure limitations."
        ],
        resolution_strategy="Integrated emergency planning with periodic drills and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="New York City Transit Emergency Preparedness Program"
    ),
    DoctrineBlock(
        topic="Passenger Security and Surveillance Systems",
        keywords=["passenger security", "surveillance", "CCTV", "incident prevention", "privacy"],
        conclusion_template="Robust security and surveillance systems deter incidents, support passenger safety, and balance privacy concerns.",
        reasoning_framework="""
Security systems integrate CCTV, access control, and incident detection. The framework evaluates technical reliability, privacy compliance, and operational integration. Key factors include system coverage, data retention policies, and staff training. Regulatory standards (FRA, ADA, GDPR) guide design. Stakeholder input (passengers, staff, regulators) informs improvements. Incident reviews assess effectiveness. Periodic upgrades maintain system reliability and relevance. Privacy impact assessments balance security and passenger rights.
""",
        key_factors=[
            "System coverage",
            "Technical reliability",
            "Privacy compliance",
            "Staff training",
            "Incident detection"
        ],
        primary_authority=[
            "FRA Security Standards",
            "ADA Accessibility Guidelines",
            "GDPR Privacy Regulations"
        ],
        burden_holder="Security Manager",
        adversary_position="Surveillance increases privacy concerns and may reduce passenger satisfaction.",
        counter_arguments=[
            "Technical failures impact security.",
            "Privacy impact assessments increase complexity.",
            "Data retention policies may conflict with regulations."
        ],
        resolution_strategy="Balanced security planning with privacy impact assessments and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="London Underground Security and Surveillance Program"
    ),
    DoctrineBlock(
        topic="Ticketing Systems and Fraud Prevention",
        keywords=["ticketing systems", "fraud prevention", "revenue protection", "technology", "passenger experience"],
        conclusion_template="Modern ticketing systems and robust fraud prevention measures protect revenue and enhance passenger experience.",
        reasoning_framework="""
Ticketing systems integrate electronic, mobile, and contactless technologies. The framework evaluates technical reliability, fraud detection, and user interface design. Key factors include system integration, data security, and regulatory compliance. Stakeholder input (passengers, staff, regulators) informs improvements. Incident reviews assess effectiveness. Periodic upgrades maintain system reliability and relevance. Data analytics support real-time fraud detection and response. Regulatory standards (FRA, ADA, PCI DSS) guide design.
""",
        key_factors=[
            "Technical reliability",
            "Fraud detection",
            "Data security",
            "User interface design",
            "System integration"
        ],
        primary_authority=[
            "FRA Ticketing Standards",
            "ADA Accessibility Guidelines",
            "PCI DSS Payment Security"
        ],
        burden_holder="IT Manager",
        adversary_position="System upgrades increase capital costs and may disrupt operations.",
        counter_arguments=[
            "Technical failures impact revenue.",
            "Complexity increases maintenance requirements.",
            "Data privacy concerns."
        ],
        resolution_strategy="Phased system upgrades with stakeholder consultation and risk assessment.",
        entity_scope="Passenger Rail Network",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Ticketing and Fraud Prevention Program"
    ),
    DoctrineBlock(
        topic="Noise and Vibration Mitigation",
        keywords=["noise mitigation", "vibration", "passenger comfort", "environmental impact", "regulatory compliance"],
        conclusion_template="Effective noise and vibration mitigation enhances passenger comfort and meets environmental and regulatory standards.",
        reasoning_framework="""
Noise and vibration mitigation uses technical solutions (track design, rolling stock upgrades, barriers) and operational adjustments. The framework evaluates environmental impact, passenger feedback, and regulatory compliance. Key factors include infrastructure design, rolling stock configuration, and service frequency. Stakeholder input (passengers, local authorities, regulators) informs improvements. Scenario analysis assesses impacts of mitigation measures. Periodic reviews and upgrades maintain effectiveness. Regulatory standards (FRA, EPA, EN 50126) guide planning.
""",
        key_factors=[
            "Infrastructure design",
            "Rolling stock configuration",
            "Service frequency",
            "Environmental impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA Noise Standards",
            "EPA Environmental Regulations",
            "EN 50126 Comfort"
        ],
        burden_holder="Environmental Manager",
        adversary_position="Mitigation measures increase capital costs and may reduce operational flexibility.",
        counter_arguments=[
            "Technical solutions may be ineffective.",
            "Operational adjustments reduce service efficiency.",
            "Environmental impact may persist."
        ],
        resolution_strategy="Phased mitigation planning with stakeholder engagement and environmental assessment.",
        entity_scope="Passenger Rail Network",
        confidence=0.84,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Deutsche Bahn Noise Mitigation Program"
    ),
    DoctrineBlock(
        topic="Environmental Sustainability and Carbon Reduction",
        keywords=["environmental sustainability", "carbon reduction", "energy efficiency", "regulatory compliance", "passenger rail"],
        conclusion_template="Sustainability and carbon reduction initiatives support regulatory compliance, operational efficiency, and positive public perception.",
        reasoning_framework="""
Sustainability initiatives focus on energy efficiency, renewable energy integration, and carbon reduction. The framework evaluates operational practices, infrastructure upgrades, and regulatory incentives. Key factors include rolling stock efficiency, service patterns, and environmental impact. Stakeholder input (passengers, environmental groups, regulators) informs policy. Cost-benefit analysis assesses investment versus savings. Periodic reviews and upgrades maintain effectiveness. Regulatory standards (FRA, EPA, EN 50126) guide planning.
""",
        key_factors=[
            "Rolling stock efficiency",
            "Service patterns",
            "Infrastructure upgrades",
            "Regulatory incentives",
            "Environmental impact"
        ],
        primary_authority=[
            "FRA Environmental Standards",
            "EPA Carbon Reduction Regulations",
            "EN 50126 Sustainability"
        ],
        burden_holder="Sustainability Manager",
        adversary_position="Sustainability upgrades increase capital costs and may disrupt operations.",
        counter_arguments=[
            "Technical integration challenges.",
            "Savings depend on operational patterns.",
            "Regulatory incentives may change."
        ],
        resolution_strategy="Phased sustainability planning with stakeholder engagement and periodic reviews.",
        entity_scope="Passenger Rail Network",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Carbon Reduction Program"
    ),
    DoctrineBlock(
        topic="Passenger Comfort and Interior Design",
        keywords=["passenger comfort", "interior design", "rolling stock", "accessibility", "service quality"],
        conclusion_template="Optimized interior design enhances passenger comfort, accessibility, and service quality.",
        reasoning_framework="""
Interior design is evaluated for comfort, accessibility, and operational reliability. The framework models seating configuration, lighting, climate control, and accessibility features. Key factors include passenger demographics, rolling stock configuration, and regulatory standards. Stakeholder input (passengers, staff, regulators) informs improvements. Periodic reviews and upgrades maintain effectiveness. Scenario analysis assesses impacts of design changes. Regulatory standards (ADA, FRA, EN 50126) guide planning.
""",
        key_factors=[
            "Seating configuration",
            "Lighting",
            "Climate control",
            "Accessibility features",
            "Passenger demographics"
        ],
        primary_authority=[
            "ADA Accessibility Guidelines",
            "FRA Comfort Standards",
            "EN 50126 Interior Design"
        ],
        burden_holder="Design Manager",
        adversary_position="Design upgrades increase capital costs and may reduce operational flexibility.",
        counter_arguments=[
            "Complex layouts reduce passenger convenience.",
            "Accessibility features increase maintenance requirements.",
            "Retrofits are costly and complex."
        ],
        resolution_strategy="Phased design upgrades with stakeholder consultation and risk assessment.",
        entity_scope="Rolling Stock Fleet",
        confidence=0.85,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Siemens Interior Design Optimization"
    ),
    DoctrineBlock(
        topic="Service Expansion and Network Planning",
        keywords=["service expansion", "network planning", "ridership", "capacity", "regulatory compliance"],
        conclusion_template="Strategic service expansion and network planning increase ridership, optimize capacity, and ensure regulatory compliance.",
        reasoning_framework="""
Service expansion and network planning are governed by demand forecasting, regulatory standards, and operational constraints. The framework evaluates infrastructure upgrades, rolling stock procurement, and stakeholder engagement. Key factors include passenger demand, capacity, and environmental impact. Scenario analysis assesses impacts of expansion, ridership, and modal shifts. Periodic reviews ensure alignment with urban growth and sustainability targets. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Passenger demand",
            "Capacity",
            "Infrastructure upgrades",
            "Rolling stock procurement",
            "Environmental impact"
        ],
        primary_authority=[
            "FRA Expansion Standards",
            "FTA Network Planning Guidelines",
            "EN 50126 Reliability"
        ],
        burden_holder="Planning Manager",
        adversary_position="Expansion increases capital costs and may reduce operational efficiency.",
        counter_arguments=[
            "Infrastructure upgrades are costly.",
            "Procurement delays impact service launch.",
            "Environmental impact may be negative."
        ],
        resolution_strategy="Phased expansion planning with stakeholder engagement and environmental assessment.",
        entity_scope="Passenger Rail Network",
        confidence=0.83,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bay Area Rapid Transit Network Expansion Program"
    ),
    DoctrineBlock(
        topic="Intermodal Integration and Connectivity",
        keywords=["intermodal integration", "connectivity", "passenger rail", "service planning", "ridership"],
        conclusion_template="Intermodal integration and connectivity increase ridership, optimize service planning, and enhance passenger experience.",
        reasoning_framework="""
Intermodal integration connects passenger rail with other transport modes (bus, metro, bike, car). The framework evaluates service coordination, ticketing integration, and infrastructure upgrades. Key factors include passenger demand, station location, and regulatory standards. Stakeholder input (passengers, operators, local authorities) informs planning. Scenario analysis assesses impacts of integration, ridership, and modal shifts. Periodic reviews ensure alignment with urban growth and sustainability targets. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Service coordination",
            "Ticketing integration",
            "Infrastructure upgrades",
            "Station location",
            "Passenger demand"
        ],
        primary_authority=[
            "FRA Intermodal Standards",
            "FTA Connectivity Guidelines",
            "EN 50126 Reliability"
        ],
        burden_holder="Planning Manager",
        adversary_position="Integration increases operational complexity and may reduce service efficiency.",
        counter_arguments=[
            "Ticketing integration increases technical complexity.",
            "Infrastructure upgrades are costly.",
            "Service coordination may be challenging."
        ],
        resolution_strategy="Phased integration planning with stakeholder engagement and technical assessment.",
        entity_scope="Passenger Rail Network",
        confidence=0.82,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Intermodal Integration Program"
    ),
    DoctrineBlock(
        topic="Passenger Feedback and Service Quality Improvement",
        keywords=["passenger feedback", "service quality", "improvement", "customer satisfaction", "data analytics"],
        conclusion_template="Continuous passenger feedback and service quality improvement initiatives enhance customer satisfaction and operational reliability.",
        reasoning_framework="""
Passenger feedback is collected via surveys, digital platforms, and incident reports. The framework evaluates service quality, operational reliability, and improvement initiatives. Key factors include feedback frequency, data analytics, and stakeholder engagement. Scenario analysis assesses impacts of improvement measures. Periodic reviews ensure alignment with passenger needs and regulatory standards. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Feedback frequency",
            "Data analytics",
            "Stakeholder engagement",
            "Service quality",
            "Operational reliability"
        ],
        primary_authority=[
            "FRA Service Quality Standards",
            "FTA Customer Satisfaction Guidelines",
            "EN 50126 Reliability"
        ],
        burden_holder="Customer Experience Manager",
        adversary_position="Feedback initiatives increase resource requirements and may disrupt operations.",
        counter_arguments=[
            "Surveys may inconvenience passengers.",
            "Data analytics increases technical complexity.",
            "Improvement measures may be costly."
        ],
        resolution_strategy="Integrated feedback platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Service Quality Improvement Program"
    ),
    DoctrineBlock(
        topic="Maintenance Scheduling and Asset Management",
        keywords=["maintenance scheduling", "asset management", "rolling stock", "infrastructure", "operational reliability"],
        conclusion_template="Effective maintenance scheduling and asset management minimize disruptions and enhance operational reliability.",
        reasoning_framework="""
Maintenance scheduling uses predictive analytics, failure history, and regulatory standards to optimize asset utilization. The framework evaluates rolling stock and infrastructure maintenance, integrating real-time monitoring and incident response. Key factors include maintenance protocols, asset quality, and operational patterns. Stakeholder input (maintenance teams, operators) guides improvements. Scenario analysis assesses impacts of maintenance measures. Periodic reviews and upgrades maintain reliability. Regulatory standards (FRA, EN 50126) guide planning.
""",
        key_factors=[
            "Maintenance protocols",
            "Asset quality",
            "Operational patterns",
            "Real-time monitoring",
            "Incident response"
        ],
        primary_authority=[
            "FRA Maintenance Standards",
            "EN 50126 Reliability",
            "AAR Asset Management Guidelines"
        ],
        burden_holder="Maintenance Manager",
        adversary_position="Maintenance scheduling increases operational complexity and may reduce service efficiency.",
        counter_arguments=[
            "Predictive analytics increases technical complexity.",
            "Asset quality may vary by supplier.",
            "Maintenance delays impact reliability."
        ],
        resolution_strategy="Integrated maintenance platform with periodic reviews and stakeholder engagement.",
        entity_scope="Rolling Stock Fleet",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Siemens Maintenance Scheduling Program"
    ),
    DoctrineBlock(
        topic="Regulatory Compliance and Legal Risk Management",
        keywords=["regulatory compliance", "legal risk", "passenger rail", "operations", "audit"],
        conclusion_template="Robust regulatory compliance and legal risk management ensure operational approval and minimize liability.",
        reasoning_framework="""
Regulatory compliance is governed by FRA, FTA, ADA, and local standards. The framework evaluates operational practices, audit protocols, and legal risk assessment. Key factors include compliance monitoring, staff training, and incident history. Stakeholder input (regulators, operators, legal counsel) informs planning. Scenario analysis assesses impacts of compliance measures. Periodic reviews and audits maintain compliance. Non-compliance results in operational restrictions and legal penalties.
""",
        key_factors=[
            "Compliance monitoring",
            "Staff training",
            "Incident history",
            "Audit protocols",
            "Legal risk assessment"
        ],
        primary_authority=[
            "FRA Regulatory Standards",
            "FTA Compliance Guidelines",
            "ADA Accessibility Guidelines"
        ],
        burden_holder="Compliance Officer",
        adversary_position="Compliance measures increase resource requirements and may disrupt operations.",
        counter_arguments=[
            "Audit protocols increase complexity.",
            "Staff training may be costly.",
            "Legal risk assessment may be subjective."
        ],
        resolution_strategy="Integrated compliance platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak Regulatory Compliance Program"
    ),
    DoctrineBlock(
        topic="Data Analytics and Predictive Operations",
        keywords=["data analytics", "predictive operations", "service reliability", "maintenance", "passenger experience"],
        conclusion_template="Advanced data analytics and predictive operations improve service reliability, maintenance efficiency, and passenger experience.",
        reasoning_framework="""
Data analytics uses real-time monitoring, historical data, and machine learning to predict operational disruptions and optimize maintenance. The framework evaluates technical integration, data quality, and regulatory compliance. Key factors include system reliability, asset quality, and operational patterns. Stakeholder input (IT teams, operators, passengers) informs improvements. Scenario analysis assesses impacts of predictive measures. Periodic reviews and upgrades maintain effectiveness. Regulatory standards (FRA, EN 50126) guide planning.
""",
        key_factors=[
            "System reliability",
            "Asset quality",
            "Operational patterns",
            "Data quality",
            "Technical integration"
        ],
        primary_authority=[
            "FRA Data Analytics Standards",
            "EN 50126 Reliability",
            "AAR Predictive Maintenance Guidelines"
        ],
        burden_holder="IT Manager",
        adversary_position="Predictive operations increase technical complexity and may disrupt traditional maintenance cycles.",
        counter_arguments=[
            "Data quality may be inconsistent.",
            "Technical integration challenges.",
            "Predictive measures may be costly."
        ],
        resolution_strategy="Integrated analytics platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Siemens Predictive Operations Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Marketing and Public Engagement",
        keywords=["marketing", "public engagement", "ridership", "service quality", "passenger rail"],
        conclusion_template="Strategic marketing and public engagement increase ridership, improve service quality, and enhance public perception.",
        reasoning_framework="""
Marketing and public engagement use targeted campaigns, community outreach, and feedback platforms. The framework evaluates campaign effectiveness, stakeholder engagement, and regulatory compliance. Key factors include passenger demographics, service quality, and public perception. Scenario analysis assesses impacts of marketing measures. Periodic reviews ensure alignment with ridership targets and regulatory standards. Stakeholder input (passengers, local authorities, operators) informs strategy. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Passenger demographics",
            "Service quality",
            "Public perception",
            "Campaign effectiveness",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "FRA Marketing Standards",
            "FTA Public Engagement Guidelines",
            "EN 50126 Service Quality"
        ],
        burden_holder="Marketing Manager",
        adversary_position="Marketing initiatives increase resource requirements and may not deliver expected ridership gains.",
        counter_arguments=[
            "Campaign effectiveness may be limited.",
            "Public engagement increases operational complexity.",
            "Resource requirements may be high."
        ],
        resolution_strategy="Integrated marketing platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Marketing and Public Engagement Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Digital Transformation",
        keywords=["digital transformation", "technology", "service quality", "operational efficiency", "passenger experience"],
        conclusion_template="Digital transformation initiatives improve service quality, operational efficiency, and passenger experience.",
        reasoning_framework="""
Digital transformation integrates advanced technologies (IoT, AI, mobile platforms) into passenger rail operations. The framework evaluates technical integration, data security, and regulatory compliance. Key factors include system reliability, user interface design, and operational patterns. Stakeholder input (IT teams, operators, passengers) informs improvements. Scenario analysis assesses impacts of digital measures. Periodic reviews and upgrades maintain effectiveness. Regulatory standards (FRA, ADA, EN 50126) guide planning.
""",
        key_factors=[
            "System reliability",
            "User interface design",
            "Operational patterns",
            "Data security",
            "Technical integration"
        ],
        primary_authority=[
            "FRA Digital Standards",
            "ADA Accessibility Guidelines",
            "EN 50126 Technology"
        ],
        burden_holder="IT Manager",
        adversary_position="Digital transformation increases technical complexity and may disrupt traditional operations.",
        counter_arguments=[
            "Technical integration challenges.",
            "Data security may be compromised.",
            "Digital measures may be costly."
        ],
        resolution_strategy="Integrated digital platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Siemens Digital Transformation Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Workforce Development",
        keywords=["workforce development", "training", "skills", "labor compliance", "service quality"],
        conclusion_template="Workforce development initiatives improve skills, ensure labor compliance, and enhance service quality.",
        reasoning_framework="""
Workforce development uses training programs, skill assessments, and compliance monitoring. The framework evaluates training effectiveness, labor compliance, and operational reliability. Key factors include staff demographics, skill requirements, and regulatory standards. Stakeholder input (unions, operators, regulators) informs planning. Scenario analysis assesses impacts of development measures. Periodic reviews ensure alignment with service quality targets and regulatory standards. Regulatory standards (FRA, FTA, ADA) guide planning.
""",
        key_factors=[
            "Staff demographics",
            "Skill requirements",
            "Training effectiveness",
            "Labor compliance",
            "Operational reliability"
        ],
        primary_authority=[
            "FRA Workforce Standards",
            "FTA Training Guidelines",
            "ADA Accessibility Guidelines"
        ],
        burden_holder="HR Manager",
        adversary_position="Development initiatives increase resource requirements and may disrupt operations.",
        counter_arguments=[
            "Training effectiveness may be limited.",
            "Labor compliance increases operational complexity.",
            "Resource requirements may be high."
        ],
        resolution_strategy="Integrated workforce development platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak Workforce Development Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Innovation and Research",
        keywords=["innovation", "research", "technology", "service quality", "operational efficiency"],
        conclusion_template="Innovation and research initiatives drive technology adoption, improve service quality, and enhance operational efficiency.",
        reasoning_framework="""
Innovation and research use pilot programs, technology trials, and academic partnerships. The framework evaluates adoption effectiveness, operational impact, and regulatory compliance. Key factors include technology readiness, service quality, and operational patterns. Stakeholder input (operators, passengers, regulators) informs planning. Scenario analysis assesses impacts of innovation measures. Periodic reviews ensure alignment with operational targets and regulatory standards. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Technology readiness",
            "Service quality",
            "Operational patterns",
            "Adoption effectiveness",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "FRA Innovation Standards",
            "FTA Research Guidelines",
            "EN 50126 Technology"
        ],
        burden_holder="Innovation Manager",
        adversary_position="Innovation initiatives increase resource requirements and may disrupt traditional operations.",
        counter_arguments=[
            "Adoption effectiveness may be limited.",
            "Operational impact may be negative.",
            "Resource requirements may be high."
        ],
        resolution_strategy="Integrated innovation platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Innovation and Research Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Safety Culture and Leadership",
        keywords=["safety culture", "leadership", "passenger rail", "operations", "service quality"],
        conclusion_template="Strong safety culture and leadership minimize risk, ensure regulatory compliance, and enhance service quality.",
        reasoning_framework="""
Safety culture and leadership use training programs, incident reviews, and compliance monitoring. The framework evaluates leadership effectiveness, staff engagement, and operational reliability. Key factors include staff demographics, leadership skills, and regulatory standards. Stakeholder input (unions, operators, regulators) informs planning. Scenario analysis assesses impacts of safety measures. Periodic reviews ensure alignment with service quality targets and regulatory standards. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Staff demographics",
            "Leadership skills",
            "Training effectiveness",
            "Safety compliance",
            "Operational reliability"
        ],
        primary_authority=[
            "FRA Safety Standards",
            "FTA Leadership Guidelines",
            "EN 50126 Safety"
        ],
        burden_holder="Safety Manager",
        adversary_position="Safety culture initiatives increase resource requirements and may disrupt operations.",
        counter_arguments=[
            "Leadership effectiveness may be limited.",
            "Safety compliance increases operational complexity.",
            "Resource requirements may be high."
        ],
        resolution_strategy="Integrated safety culture platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak Safety Culture Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Cybersecurity and Data Protection",
        keywords=["cybersecurity", "data protection", "passenger rail", "technology", "regulatory compliance"],
        conclusion_template="Robust cybersecurity and data protection measures ensure regulatory compliance, operational reliability, and passenger trust.",
        reasoning_framework="""
Cybersecurity and data protection use technical solutions (firewalls, encryption, access control) and operational protocols. The framework evaluates system reliability, data quality, and regulatory compliance. Key factors include technical integration, staff training, and incident history. Stakeholder input (IT teams, operators, regulators) informs planning. Scenario analysis assesses impacts of cybersecurity measures. Periodic reviews and upgrades maintain effectiveness. Regulatory standards (FRA, ADA, GDPR) guide planning.
""",
        key_factors=[
            "Technical integration",
            "Staff training",
            "Incident history",
            "System reliability",
            "Data quality"
        ],
        primary_authority=[
            "FRA Cybersecurity Standards",
            "ADA Accessibility Guidelines",
            "GDPR Data Protection Regulations"
        ],
        burden_holder="IT Manager",
        adversary_position="Cybersecurity measures increase technical complexity and may disrupt operations.",
        counter_arguments=[
            "Technical integration challenges.",
            "Staff training may be costly.",
            "Data quality may be inconsistent."
        ],
        resolution_strategy="Integrated cybersecurity platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Cybersecurity Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Financial Management and Cost Control",
        keywords=["financial management", "cost control", "passenger rail", "operations", "revenue"],
        conclusion_template="Effective financial management and cost control ensure operational sustainability and regulatory compliance.",
        reasoning_framework="""
Financial management and cost control use budgeting, revenue analysis, and operational efficiency measures. The framework evaluates cost structures, revenue streams, and regulatory compliance. Key factors include operational patterns, asset quality, and stakeholder engagement. Scenario analysis assesses impacts of cost control measures. Periodic reviews ensure alignment with operational targets and regulatory standards. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Operational patterns",
            "Asset quality",
            "Cost structures",
            "Revenue streams",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "FRA Financial Standards",
            "FTA Cost Control Guidelines",
            "EN 50126 Operations"
        ],
        burden_holder="Finance Manager",
        adversary_position="Cost control measures may reduce service quality and passenger satisfaction.",
        counter_arguments=[
            "Operational efficiency may be compromised.",
            "Asset quality may decline.",
            "Revenue streams may be limited."
        ],
        resolution_strategy="Integrated financial management platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak Financial Management Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Asset Lifecycle Management",
        keywords=["asset lifecycle", "management", "passenger rail", "operations", "maintenance"],
        conclusion_template="Effective asset lifecycle management minimizes disruptions, optimizes maintenance, and ensures operational reliability.",
        reasoning_framework="""
Asset lifecycle management uses predictive analytics, maintenance history, and regulatory standards to optimize asset utilization. The framework evaluates rolling stock and infrastructure lifecycle, integrating real-time monitoring and incident response. Key factors include maintenance protocols, asset quality, and operational patterns. Stakeholder input (maintenance teams, operators) guides improvements. Scenario analysis assesses impacts of lifecycle measures. Periodic reviews and upgrades maintain reliability. Regulatory standards (FRA, EN 50126) guide planning.
""",
        key_factors=[
            "Maintenance protocols",
            "Asset quality",
            "Operational patterns",
            "Real-time monitoring",
            "Incident response"
        ],
        primary_authority=[
            "FRA Asset Management Standards",
            "EN 50126 Reliability",
            "AAR Lifecycle Guidelines"
        ],
        burden_holder="Asset Manager",
        adversary_position="Lifecycle management increases operational complexity and may reduce service efficiency.",
        counter_arguments=[
            "Predictive analytics increases technical complexity.",
            "Asset quality may vary by supplier.",
            "Lifecycle delays impact reliability."
        ],
        resolution_strategy="Integrated asset management platform with periodic reviews and stakeholder engagement.",
        entity_scope="Rolling Stock Fleet",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Siemens Asset Lifecycle Management Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Service Disruption Management",
        keywords=["service disruption", "management", "passenger rail", "operations", "incident response"],
        conclusion_template="Effective service disruption management minimizes passenger inconvenience and ensures operational reliability.",
        reasoning_framework="""
Service disruption management uses incident response protocols, real-time monitoring, and stakeholder engagement. The framework evaluates disruption causes, response effectiveness, and regulatory compliance. Key factors include operational patterns, incident history, and staff training. Scenario analysis assesses impacts of disruption measures. Periodic reviews ensure alignment with operational targets and regulatory standards. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Operational patterns",
            "Incident history",
            "Staff training",
            "Response effectiveness",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "FRA Disruption Management Standards",
            "FTA Incident Response Guidelines",
            "EN 50126 Operations"
        ],
        burden_holder="Operations Manager",
        adversary_position="Disruption management increases operational complexity and may reduce service efficiency.",
        counter_arguments=[
            "Incident response may be delayed.",
            "Staff training increases resource requirements.",
            "Operational patterns may be disrupted."
        ],
        resolution_strategy="Integrated disruption management platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amtrak Service Disruption Management Program"
    ),
    DoctrineBlock(
        topic="Passenger Rail Risk Assessment and Mitigation",
        keywords=["risk assessment", "mitigation", "passenger rail", "operations", "safety"],
        conclusion_template="Comprehensive risk assessment and mitigation minimize operational risk and ensure passenger safety.",
        reasoning_framework="""
Risk assessment and mitigation use technical analysis, incident history, and regulatory standards. The framework evaluates risk factors, mitigation measures, and operational reliability. Key factors include operational patterns, asset quality, and staff training. Scenario analysis assesses impacts of risk mitigation measures. Periodic reviews ensure alignment with operational targets and regulatory standards. Regulatory standards (FRA, FTA, EN 50126) guide planning.
""",
        key_factors=[
            "Operational patterns",
            "Asset quality",
            "Staff training",
            "Risk factors",
            "Mitigation measures"
        ],
        primary_authority=[
            "FRA Risk Assessment Standards",
            "FTA Mitigation Guidelines",
            "EN 50126 Safety"
        ],
        burden_holder="Risk Manager",
        adversary_position="Mitigation measures increase resource requirements and may disrupt operations.",
        counter_arguments=[
            "Risk factors may be underestimated.",
            "Mitigation measures may be costly.",
            "Operational patterns may be disrupted."
        ],
        resolution_strategy="Integrated risk assessment platform with periodic reviews and stakeholder engagement.",
        entity_scope="Passenger Rail Network",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Transport for London Risk Assessment and Mitigation Program"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if query_lower in doctrine.topic.lower():
            results.append(doctrine)
            continue
        for kw in doctrine.keywords:
            if query_lower in kw.lower():
                results.append(doctrine)
                break
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]