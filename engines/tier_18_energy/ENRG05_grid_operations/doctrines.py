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
        topic="AC Power Fundamentals - Three-Phase Systems",
        keywords=["three-phase", "AC", "power", "phasor", "symmetrical components", "line-to-line", "line-to-neutral"],
        conclusion_template="Three-phase systems provide balanced power delivery and efficient transmission, forming the backbone of modern AC power grids.",
        reasoning_framework=(
            "Three-phase AC systems utilize three sinusoidal voltages, each phase separated by 120 degrees. "
            "This configuration allows for constant power transfer, reduces conductor material for a given power, "
            "and enables the use of symmetrical components for fault analysis. The system can be connected in star (wye) "
            "or delta configurations, with line-to-line and line-to-neutral voltages determined by the connection type. "
            "The analysis of three-phase systems is essential for load flow, fault studies, and equipment specification. "
            "Balanced operation minimizes neutral currents and voltage unbalance, improving system reliability."
        ),
        key_factors=[
            "Phase displacement",
            "System configuration (wye/delta)",
            "Load balancing",
            "Neutral current",
            "Voltage unbalance"
        ],
        primary_authority=[
            "IEEE Std 141 (Red Book)",
            "IEC 60038"
        ],
        burden_holder="System designer",
        adversary_position="Single-phase systems are sufficient for most applications.",
        counter_arguments=[
            "Single-phase systems are less efficient for large-scale transmission.",
            "Three-phase systems enable easier fault analysis and equipment standardization."
        ],
        resolution_strategy="Demonstrate efficiency and reliability improvements in three-phase systems for grid-scale applications.",
        entity_scope="Transmission and distribution networks",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="IEEE Std 141"
    ),
    DoctrineBlock(
        topic="Power Factor and Reactive Power Management",
        keywords=["power factor", "reactive power", "VAR", "PF correction", "capacitor banks", "inductive loads"],
        conclusion_template="Effective reactive power management and power factor correction are essential for grid efficiency and voltage regulation.",
        reasoning_framework=(
            "Power factor (PF) is the ratio of real power to apparent power in an AC circuit. Inductive loads such as motors "
            "cause lagging PF, increasing system losses and reducing capacity. Utilities often require PF correction to reduce "
            "transmission losses and improve voltage profiles. Correction is typically achieved using capacitor banks or synchronous condensers. "
            "Reactive power (measured in VARs) does not perform work but is necessary for voltage support. Poor PF can result in utility penalties."
        ),
        key_factors=[
            "Load type (inductive/capacitive)",
            "Utility tariffs",
            "Voltage regulation",
            "System losses",
            "Correction equipment"
        ],
        primary_authority=[
            "IEEE Std 399 (Brown Book)",
            "IEC 61921"
        ],
        burden_holder="Facility operator",
        adversary_position="PF correction is unnecessary if utility does not penalize low PF.",
        counter_arguments=[
            "Even without penalties, poor PF increases losses and reduces system capacity.",
            "Voltage regulation may be compromised without PF correction."
        ],
        resolution_strategy="Quantify cost savings and system improvements from PF correction.",
        entity_scope="Industrial and commercial facilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEEE Std 399"
    ),
    DoctrineBlock(
        topic="Transmission System Voltage Levels - HV/EHV/UHV",
        keywords=["transmission", "HV", "EHV", "UHV", "voltage levels", "grid", "long-distance"],
        conclusion_template="Selection of transmission voltage levels is governed by distance, power transfer requirements, and economic optimization.",
        reasoning_framework=(
            "Transmission systems are classified by voltage: High Voltage (HV, 100-230 kV), Extra High Voltage (EHV, 345-765 kV), "
            "and Ultra High Voltage (UHV, >800 kV AC or >600 kV DC). Higher voltages reduce line losses and allow greater power transfer, "
            "but require more expensive insulation and equipment. The choice involves trade-offs between capital cost, right-of-way, "
            "and operational efficiency. International standards (IEC, IEEE) define voltage classes and insulation requirements."
        ),
        key_factors=[
            "Transmission distance",
            "Power transfer capacity",
            "Line losses",
            "Equipment cost",
            "Right-of-way constraints"
        ],
        primary_authority=[
            "IEC 60038",
            "IEEE Std C37.100"
        ],
        burden_holder="Transmission planner",
        adversary_position="Lower voltage levels are sufficient and less costly.",
        counter_arguments=[
            "Lower voltages increase losses and require larger conductors.",
            "Higher voltages enable bulk power transfer with fewer lines."
        ],
        resolution_strategy="Perform cost-benefit analysis considering losses, capacity, and long-term planning.",
        entity_scope="Bulk transmission networks",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 60038"
    ),
    DoctrineBlock(
        topic="HVDC Transmission Systems",
        keywords=["HVDC", "high-voltage direct current", "converter", "rectifier", "inverter", "long-distance", "interconnection"],
        conclusion_template="HVDC systems are preferred for long-distance, high-capacity, and asynchronous interconnections due to lower losses and controllability.",
        reasoning_framework=(
            "HVDC transmission uses direct current for bulk power transfer, offering lower line losses and no reactive power flow. "
            "HVDC is advantageous for submarine cables, long-distance overhead lines, and connecting asynchronous grids. "
            "Converter stations (rectifiers and inverters) are required at each end, increasing terminal costs but enabling precise power flow control. "
            "HVDC also mitigates stability issues in large interconnected systems."
        ),
        key_factors=[
            "Transmission distance",
            "Interconnection of asynchronous grids",
            "Submarine/underground cable feasibility",
            "Power flow control",
            "Converter station cost"
        ],
        primary_authority=[
            "CIGRÉ Technical Brochures",
            "IEEE Std 115"
        ],
        burden_holder="Transmission developer",
        adversary_position="HVDC is too costly compared to HVAC for most applications.",
        counter_arguments=[
            "For distances >600 km overhead or >50 km submarine, HVDC is more economical.",
            "HVDC enables interconnection of grids with different frequencies."
        ],
        resolution_strategy="Evaluate project economics and technical requirements for HVDC vs HVAC.",
        entity_scope="Inter-regional transmission",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CIGRÉ TB 563"
    ),
    DoctrineBlock(
        topic="Distribution System Configurations - Radial, Loop, Network",
        keywords=["distribution", "radial", "loop", "network", "topology", "reliability", "urban", "rural"],
        conclusion_template="Distribution system configuration is selected based on reliability, cost, and load density requirements.",
        reasoning_framework=(
            "Radial systems are simple and cost-effective, suitable for rural areas with low load density but limited reliability. "
            "Loop (ring) systems offer improved reliability by providing alternate paths for power flow, common in suburban areas. "
            "Networked systems, prevalent in urban centers, provide high reliability and flexibility but are more complex and costly. "
            "The choice depends on customer criticality, outage tolerance, and economic considerations."
        ),
        key_factors=[
            "Load density",
            "Customer reliability requirements",
            "Cost constraints",
            "Urban vs rural setting",
            "Restoration time"
        ],
        primary_authority=[
            "IEEE Std 141",
            "IEC 60909"
        ],
        burden_holder="Distribution planner",
        adversary_position="Networked systems are unnecessarily complex for most areas.",
        counter_arguments=[
            "Critical loads and urban centers require high reliability.",
            "Radial systems may not meet restoration time targets."
        ],
        resolution_strategy="Match configuration to reliability and economic requirements.",
        entity_scope="Distribution networks",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE Std 141"
    ),
    DoctrineBlock(
        topic="Power Transformers - Design and Operation",
        keywords=["transformer", "design", "operation", "impedance", "cooling", "tap changer", "losses"],
        conclusion_template="Transformer selection and operation must ensure voltage regulation, thermal limits, and protection coordination.",
        reasoning_framework=(
            "Power transformers step voltage up or down in transmission and distribution systems. Key design parameters include "
            "impedance (affecting fault currents and voltage drop), cooling method (ONAN, ONAF, OFAF, etc.), and tap changer type "
            "(on-load or off-load). Proper operation requires monitoring of temperature, oil quality, and dissolved gases. "
            "Protection schemes (differential, Buchholz relay) are essential for reliability."
        ),
        key_factors=[
            "Impedance",
            "Cooling method",
            "Tap changer type",
            "Protection scheme",
            "Thermal rating"
        ],
        primary_authority=[
            "IEC 60076",
            "IEEE Std C57.12"
        ],
        burden_holder="Asset manager",
        adversary_position="Standard transformers suffice without detailed analysis.",
        counter_arguments=[
            "Site-specific requirements may necessitate custom design.",
            "Improper operation reduces transformer life and reliability."
        ],
        resolution_strategy="Conduct detailed specification and monitoring based on site conditions.",
        entity_scope="Substations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 60076"
    ),
    DoctrineBlock(
        topic="Circuit Breaker Technologies - SF6, Vacuum, Oil",
        keywords=["circuit breaker", "SF6", "vacuum", "oil", "interrupting medium", "arc quenching"],
        conclusion_template="Selection of circuit breaker technology is based on voltage level, interrupting rating, and environmental considerations.",
        reasoning_framework=(
            "SF6 circuit breakers are widely used for high-voltage applications due to excellent arc quenching and dielectric properties, "
            "but SF6 is a potent greenhouse gas. Vacuum circuit breakers are preferred for medium-voltage due to low maintenance and "
            "environmental safety. Oil circuit breakers are largely obsolete but may still be found in legacy installations. "
            "Selection must consider interrupting rating, maintenance, and environmental regulations."
        ),
        key_factors=[
            "Voltage level",
            "Interrupting rating",
            "Maintenance requirements",
            "Environmental impact",
            "Regulatory compliance"
        ],
        primary_authority=[
            "IEC 62271-100",
            "IEEE Std C37.04"
        ],
        burden_holder="Substation designer",
        adversary_position="All breaker types are interchangeable.",
        counter_arguments=[
            "Environmental and maintenance factors differ significantly.",
            "Some technologies are not suitable for certain voltage levels."
        ],
        resolution_strategy="Select breaker type based on application, regulations, and life-cycle cost.",
        entity_scope="Substations and switchgear",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 62271-100"
    ),
    DoctrineBlock(
        topic="Protective Relaying - Overcurrent, Distance, Differential",
        keywords=["protective relay", "overcurrent", "distance", "differential", "protection", "coordination"],
        conclusion_template="Protective relaying schemes must be coordinated to ensure selectivity, speed, and security for system protection.",
        reasoning_framework=(
            "Overcurrent relays provide basic protection for feeders and transformers but may lack selectivity in complex networks. "
            "Distance relays are used for transmission line protection, measuring impedance to fault. Differential relays offer "
            "sensitive and selective protection for transformers and buses by comparing currents at both ends. Coordination of "
            "relays ensures only the faulted section is isolated, minimizing system disruption."
        ),
        key_factors=[
            "System configuration",
            "Relay settings",
            "Coordination study",
            "Communication channels",
            "Protection zones"
        ],
        primary_authority=[
            "IEEE Std C37.2",
            "IEC 60255"
        ],
        burden_holder="Protection engineer",
        adversary_position="Simple overcurrent relays suffice for all protection needs.",
        counter_arguments=[
            "Complex networks require advanced schemes for selectivity.",
            "Differential and distance relays improve reliability and speed."
        ],
        resolution_strategy="Perform protection coordination studies and select appropriate relaying schemes.",
        entity_scope="Transmission and distribution protection",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEEE Std C37.2"
    ),
    DoctrineBlock(
        topic="SCADA and Energy Management Systems",
        keywords=["SCADA", "EMS", "supervisory control", "data acquisition", "remote terminal unit", "HMI"],
        conclusion_template="SCADA and EMS are critical for real-time monitoring, control, and optimization of power system operations.",
        reasoning_framework=(
            "SCADA (Supervisory Control and Data Acquisition) systems collect and transmit real-time data from substations and field devices "
            "to control centers. Energy Management Systems (EMS) build on SCADA to provide advanced applications such as load forecasting, "
            "contingency analysis, and optimal power flow. Integration with communication protocols (IEC 61850, DNP3) and cybersecurity "
            "measures is essential for reliable operation."
        ),
        key_factors=[
            "Communication reliability",
            "Data integrity",
            "Cybersecurity",
            "System integration",
            "Operator training"
        ],
        primary_authority=[
            "IEC 60870-5",
            "NERC CIP Standards"
        ],
        burden_holder="System operator",
        adversary_position="Manual operation is sufficient for grid management.",
        counter_arguments=[
            "Modern grids require real-time situational awareness.",
            "Manual operation is prone to errors and delays."
        ],
        resolution_strategy="Demonstrate operational improvements and compliance benefits of SCADA/EMS.",
        entity_scope="Control centers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 60870-5"
    ),
    DoctrineBlock(
        topic="Load Flow Analysis - Power System Planning",
        keywords=["load flow", "power flow", "planning", "steady-state", "voltage profile", "network analysis"],
        conclusion_template="Load flow analysis is essential for planning, operation, and expansion of power systems.",
        reasoning_framework=(
            "Load flow studies determine voltage, current, and power flows under steady-state conditions. "
            "They are used to assess system adequacy, voltage profiles, and equipment loading. "
            "Common methods include Gauss-Seidel, Newton-Raphson, and Fast Decoupled Load Flow. "
            "Accurate modeling of system topology, load, and generation is critical for reliable results."
        ),
        key_factors=[
            "System topology",
            "Load and generation data",
            "Model accuracy",
            "Contingency scenarios",
            "Voltage limits"
        ],
        primary_authority=[
            "IEEE Std 399",
            "IEC 60909"
        ],
        burden_holder="Planning engineer",
        adversary_position="Rule-of-thumb estimates are sufficient for planning.",
        counter_arguments=[
            "Complex networks require detailed analysis.",
            "Inaccurate planning leads to reliability and economic issues."
        ],
        resolution_strategy="Use validated load flow software and data for planning studies.",
        entity_scope="System planning and operations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="IEEE Std 399"
    ),
    DoctrineBlock(
        topic="Fault Analysis - Symmetrical and Asymmetrical Faults",
        keywords=["fault analysis", "symmetrical fault", "asymmetrical fault", "short-circuit", "sequence components"],
        conclusion_template="Comprehensive fault analysis is necessary for equipment specification and protection coordination.",
        reasoning_framework=(
            "Fault analysis involves calculating currents and voltages during system faults. Symmetrical faults (three-phase) are rare but "
            "produce the highest fault currents. Asymmetrical faults (single line-to-ground, line-to-line, double line-to-ground) are more common. "
            "The method of symmetrical components is used to analyze unbalanced faults. Results inform equipment ratings and relay settings."
        ),
        key_factors=[
            "System impedance",
            "Fault type and location",
            "Sequence networks",
            "Equipment ratings",
            "Protection settings"
        ],
        primary_authority=[
            "IEC 60909",
            "IEEE Std 242 (Buff Book)"
        ],
        burden_holder="Protection engineer",
        adversary_position="Only three-phase faults need to be considered.",
        counter_arguments=[
            "Most faults are asymmetrical and require detailed analysis.",
            "Neglecting unbalanced faults can compromise protection."
        ],
        resolution_strategy="Perform comprehensive fault studies including all fault types.",
        entity_scope="System protection and equipment specification",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEC 60909"
    ),
    DoctrineBlock(
        topic="Power Quality - Harmonics, Sag, Swell, Flicker",
        keywords=["power quality", "harmonics", "voltage sag", "swell", "flicker", "THD", "PQ monitoring"],
        conclusion_template="Maintaining power quality is essential to protect sensitive loads and comply with standards.",
        reasoning_framework=(
            "Power quality issues such as harmonics, voltage sags/swells, and flicker can damage equipment and disrupt operations. "
            "Harmonics are caused by nonlinear loads and are quantified by Total Harmonic Distortion (THD). Voltage sags and swells "
            "result from faults or switching events. Flicker is caused by rapid voltage fluctuations. Monitoring and mitigation "
            "are required to comply with IEEE 519 and IEC 61000 standards."
        ),
        key_factors=[
            "Load sensitivity",
            "Source impedance",
            "Nonlinear load prevalence",
            "Mitigation equipment",
            "Compliance standards"
        ],
        primary_authority=[
            "IEEE Std 519",
            "IEC 61000-4-30"
        ],
        burden_holder="Facility operator",
        adversary_position="Power quality issues are rare and not worth monitoring.",
        counter_arguments=[
            "Modern loads are increasingly sensitive to PQ disturbances.",
            "Non-compliance can result in utility penalties."
        ],
        resolution_strategy="Implement PQ monitoring and mitigation as part of asset management.",
        entity_scope="Industrial and commercial facilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEEE Std 519"
    ),
    DoctrineBlock(
        topic="Voltage Regulation - Tap Changers, Regulators, Capacitors",
        keywords=["voltage regulation", "tap changer", "regulator", "capacitor bank", "line drop compensation"],
        conclusion_template="Voltage regulation devices are deployed to maintain voltage within prescribed limits under varying load conditions.",
        reasoning_framework=(
            "Voltage regulation is achieved using on-load tap changers (OLTC) on transformers, line voltage regulators, and shunt capacitor banks. "
            "OLTCs adjust transformer ratios under load, regulators provide step voltage control on feeders, and capacitors supply reactive power. "
            "Proper coordination ensures voltage remains within ANSI C84.1 or IEC 60038 limits."
        ),
        key_factors=[
            "Load variation",
            "Feeder length",
            "Regulation device settings",
            "Reactive power compensation",
            "Standard voltage limits"
        ],
        primary_authority=[
            "ANSI C84.1",
            "IEC 60038"
        ],
        burden_holder="Distribution engineer",
        adversary_position="Voltage regulation is unnecessary with modern equipment.",
        counter_arguments=[
            "Voltage must remain within statutory limits for all customers.",
            "Load variations and long feeders require active regulation."
        ],
        resolution_strategy="Deploy and coordinate regulation devices based on system studies.",
        entity_scope="Distribution feeders and substations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ANSI C84.1"
    ),
    DoctrineBlock(
        topic="NERC Reliability Standards - Compliance Requirements",
        keywords=["NERC", "reliability standards", "compliance", "CIP", "PRC", "BAL", "FAC"],
        conclusion_template="Compliance with NERC Reliability Standards is mandatory for bulk electric system operators in North America.",
        reasoning_framework=(
            "NERC develops and enforces reliability standards covering system planning, operations, protection, and cybersecurity. "
            "Entities subject to NERC must implement and document compliance with standards such as CIP (Critical Infrastructure Protection), "
            "PRC (Protection and Control), BAL (Balancing), and FAC (Facilities Design). Non-compliance can result in significant penalties."
        ),
        key_factors=[
            "Registration as BES entity",
            "Standard applicability",
            "Documentation and evidence",
            "Audit readiness",
            "Penalty structure"
        ],
        primary_authority=[
            "NERC Reliability Standards",
            "FERC Orders"
        ],
        burden_holder="Registered entity",
        adversary_position="Compliance is burdensome and non-essential.",
        counter_arguments=[
            "Reliability and security of the grid depend on compliance.",
            "Penalties for non-compliance are severe."
        ],
        resolution_strategy="Implement compliance management programs and maintain audit readiness.",
        entity_scope="Bulk electric system operators",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NERC Reliability Standards"
    ),
    DoctrineBlock(
        topic="Grid Interconnection - IEEE 1547 for Distributed Energy Resources",
        keywords=["interconnection", "distributed energy resources", "DER", "IEEE 1547", "inverter", "grid code"],
        conclusion_template="DER interconnection must comply with IEEE 1547 to ensure safety, reliability, and power quality.",
        reasoning_framework=(
            "IEEE 1547 defines technical requirements for interconnecting DERs (solar, wind, storage) to the grid. "
            "It covers voltage and frequency ride-through, anti-islanding, and interoperability. Compliance ensures DERs do not compromise "
            "system stability or power quality. Utilities may impose additional requirements based on local grid conditions."
        ),
        key_factors=[
            "DER type and size",
            "Interconnection location",
            "Protection and control",
            "Grid code compliance",
            "Utility requirements"
        ],
        primary_authority=[
            "IEEE Std 1547",
            "FERC Order 2006"
        ],
        burden_holder="DER owner/operator",
        adversary_position="DERs can be connected without standardized requirements.",
        counter_arguments=[
            "Non-compliance can cause safety and reliability issues.",
            "IEEE 1547 is widely adopted as the interconnection standard."
        ],
        resolution_strategy="Ensure DER interconnection studies and compliance documentation.",
        entity_scope="Distribution networks",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEEE Std 1547"
    ),
    DoctrineBlock(
        topic="Energy Storage - Battery, Pumped Hydro, Flywheel",
        keywords=["energy storage", "battery", "pumped hydro", "flywheel", "frequency regulation", "peak shaving"],
        conclusion_template="Energy storage technologies enhance grid flexibility, reliability, and support renewable integration.",
        reasoning_framework=(
            "Energy storage systems (ESS) provide services such as frequency regulation, peak shaving, and backup power. "
            "Battery storage offers fast response but limited duration; pumped hydro provides large-scale, long-duration storage; "
            "flywheels offer high power for short durations. Selection depends on application, cost, and site constraints."
        ),
        key_factors=[
            "Application (frequency regulation, backup, etc.)",
            "Response time",
            "Storage duration",
            "Site suitability",
            "Cost and lifecycle"
        ],
        primary_authority=[
            "DOE Energy Storage Handbook",
            "IEC 62933"
        ],
        burden_holder="Project developer",
        adversary_position="Storage is too costly and unnecessary for most grids.",
        counter_arguments=[
            "Storage supports renewable integration and grid stability.",
            "Costs are declining with technology advances."
        ],
        resolution_strategy="Conduct application-specific cost-benefit analysis.",
        entity_scope="Transmission, distribution, and microgrids",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="DOE Energy Storage Handbook"
    ),
    DoctrineBlock(
        topic="Renewable Integration Challenges - Variability and Inverter Dynamics",
        keywords=["renewable integration", "variability", "inverter", "grid-forming", "grid-following", "stability"],
        conclusion_template="Addressing variability and inverter dynamics is essential for reliable renewable integration.",
        reasoning_framework=(
            "Renewable generation introduces variability and uncertainty in power supply. Inverter-based resources (IBRs) "
            "may lack inertia and exhibit different dynamic responses compared to synchronous machines. Grid-forming inverters "
            "can provide synthetic inertia and voltage support. System studies must address frequency stability, ride-through, "
            "and protection coordination for high renewable penetration."
        ),
        key_factors=[
            "Renewable penetration level",
            "Inverter control strategy",
            "System inertia",
            "Protection scheme compatibility",
            "Forecasting accuracy"
        ],
        primary_authority=[
            "NERC Inverter-Based Resource Task Force",
            "IEEE Std 1547"
        ],
        burden_holder="System operator",
        adversary_position="Renewables can be integrated without special considerations.",
        counter_arguments=[
            "High penetration can compromise stability and protection.",
            "Inverter controls must be coordinated with grid requirements."
        ],
        resolution_strategy="Perform dynamic studies and implement advanced inverter controls.",
        entity_scope="Bulk and distribution systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NERC IBR Task Force Reports"
    ),
    DoctrineBlock(
        topic="Microgrid Operation - Islanded and Grid-Connected Modes",
        keywords=["microgrid", "islanded operation", "grid-connected", "seamless transition", "black start"],
        conclusion_template="Microgrids must be capable of seamless transition between grid-connected and islanded modes.",
        reasoning_framework=(
            "Microgrids can operate connected to the main grid or islanded during disturbances. Seamless transition requires "
            "synchronization, load shedding, and black start capability. Control strategies must manage voltage, frequency, "
            "and protection coordination under both modes. Regulatory and interconnection requirements must be addressed."
        ),
        key_factors=[
            "Transition strategy",
            "Load and generation balance",
            "Protection scheme",
            "Synchronization",
            "Regulatory compliance"
        ],
        primary_authority=[
            "DOE Microgrid Guide",
            "IEEE Std 2030.7"
        ],
        burden_holder="Microgrid operator",
        adversary_position="Microgrids can operate without special transition controls.",
        counter_arguments=[
            "Uncoordinated transitions can cause outages or equipment damage.",
            "Regulatory requirements mandate safe operation."
        ],
        resolution_strategy="Implement advanced controls and test transition scenarios.",
        entity_scope="Microgrids",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEEE Std 2030.7"
    ),
    DoctrineBlock(
        topic="Power Market Operations - LMP and Ancillary Services",
        keywords=["power market", "LMP", "locational marginal pricing", "ancillary services", "market clearing", "reserve"],
        conclusion_template="LMP and ancillary services markets ensure efficient dispatch and reliability in competitive power systems.",
        reasoning_framework=(
            "Locational Marginal Pricing (LMP) reflects the cost of delivering the next increment of electricity at each node, "
            "accounting for losses and congestion. Ancillary services (frequency regulation, reserves, voltage support) are procured "
            "to maintain reliability. Market participants must understand market rules, settlement processes, and compliance obligations."
        ),
        key_factors=[
            "Market design",
            "Congestion management",
            "Ancillary service requirements",
            "Settlement procedures",
            "Regulatory oversight"
        ],
        primary_authority=[
            "FERC Order 888",
            "NERC Operating Standards"
        ],
        burden_holder="Market participant",
        adversary_position="Energy-only markets are sufficient for grid operation.",
        counter_arguments=[
            "Ancillary services are essential for reliability.",
            "LMP provides transparent price signals for investment."
        ],
        resolution_strategy="Participate in market design and compliance processes.",
        entity_scope="ISO/RTO markets",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Order 888"
    ),
    DoctrineBlock(
        topic="Static VAR Compensator (SVC) and STATCOM",
        keywords=["SVC", "STATCOM", "reactive power compensation", "voltage support", "dynamic compensation"],
        conclusion_template="SVC and STATCOM provide dynamic reactive power compensation for voltage stability.",
        reasoning_framework=(
            "SVCs use thyristor-controlled reactors and capacitors to provide fast-acting reactive power support. "
            "STATCOMs use power electronics to inject or absorb reactive current, offering superior dynamic performance. "
            "Both technologies are deployed for voltage regulation, stability enhancement, and power quality improvement."
        ),
        key_factors=[
            "System voltage stability",
            "Dynamic response requirements",
            "Installation cost",
            "Control integration",
            "Harmonic performance"
        ],
        primary_authority=[
            "IEEE Std 1031",
            "CIGRÉ TB 144"
        ],
        burden_holder="Transmission planner",
        adversary_position="Fixed compensation is sufficient for voltage support.",
        counter_arguments=[
            "Dynamic compensation is required for fast voltage disturbances.",
            "STATCOMs offer better performance at low voltages."
        ],
        resolution_strategy="Evaluate system needs and select appropriate technology.",
        entity_scope="Transmission and industrial systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE Std 1031"
    ),
    DoctrineBlock(
        topic="Smart Grid Technologies - AMI, DA, DMS, DERMS",
        keywords=["smart grid", "AMI", "advanced metering", "distribution automation", "DMS", "DERMS", "integration"],
        conclusion_template="Smart grid technologies enable advanced monitoring, automation, and integration of distributed resources.",
        reasoning_framework=(
            "Advanced Metering Infrastructure (AMI) provides granular consumption data and supports demand response. "
            "Distribution Automation (DA) enhances reliability through remote switching and fault isolation. "
            "Distribution Management Systems (DMS) and Distributed Energy Resource Management Systems (DERMS) "
            "enable real-time optimization and integration of DERs. Cybersecurity and interoperability are critical considerations."
        ),
        key_factors=[
            "Data communication infrastructure",
            "System interoperability",
            "Cybersecurity",
            "Customer engagement",
            "DER integration"
        ],
        primary_authority=[
            "NIST Smart Grid Framework",
            "IEC 61968"
        ],
        burden_holder="Utility operator",
        adversary_position="Traditional grid technologies are adequate.",
        counter_arguments=[
            "Smart grid improves reliability, efficiency, and customer service.",
            "DER integration requires advanced management systems."
        ],
        resolution_strategy="Develop smart grid roadmap and invest in enabling technologies.",
        entity_scope="Distribution networks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NIST Smart Grid Framework"
    ),
    DoctrineBlock(
        topic="Demand Response and Load Management",
        keywords=["demand response", "load management", "peak shaving", "load shifting", "customer incentive"],
        conclusion_template="Demand response programs enhance grid flexibility and reduce peak demand through customer participation.",
        reasoning_framework=(
            "Demand response (DR) involves adjusting customer load in response to price signals or grid needs. "
            "Programs include direct load control, time-of-use pricing, and incentive-based curtailment. "
            "DR reduces the need for peaking generation and supports renewable integration. Effective communication "
            "and customer engagement are key to program success."
        ),
        key_factors=[
            "Program design",
            "Customer participation",
            "Communication infrastructure",
            "Measurement and verification",
            "Regulatory support"
        ],
        primary_authority=[
            "FERC Order 745",
            "DOE DR Handbook"
        ],
        burden_holder="Utility or aggregator",
        adversary_position="DR has limited impact on grid operations.",
        counter_arguments=[
            "DR can provide significant peak reduction and ancillary services.",
            "Regulatory frameworks support DR participation in markets."
        ],
        resolution_strategy="Design effective DR programs and measure performance.",
        entity_scope="Retail and wholesale markets",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 745"
    ),
    DoctrineBlock(
        topic="Arc Flash Hazard Analysis - NFPA 70E and IEEE 1584",
        keywords=["arc flash", "hazard analysis", "NFPA 70E", "IEEE 1584", "PPE", "incident energy"],
        conclusion_template="Arc flash hazard analysis is required to protect personnel and comply with safety standards.",
        reasoning_framework=(
            "Arc flash studies calculate incident energy and required PPE for electrical workers. NFPA 70E and IEEE 1584 "
            "provide methodologies for hazard assessment and mitigation. Labeling, training, and engineering controls "
            "are mandated to reduce risk. Regular review and updates are necessary as system configurations change."
        ),
        key_factors=[
            "System fault levels",
            "Protective device settings",
            "Working distance",
            "PPE selection",
            "Labeling and training"
        ],
        primary_authority=[
            "NFPA 70E",
            "IEEE Std 1584"
        ],
        burden_holder="Facility owner",
        adversary_position="Arc flash analysis is unnecessary for low-voltage systems.",
        counter_arguments=[
            "Serious injuries can occur even at low voltages.",
            "Regulations require hazard assessment for all energized work."
        ],
        resolution_strategy="Conduct and document arc flash studies for all relevant equipment.",
        entity_scope="Industrial and commercial facilities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NFPA 70E"
    ),
    # Additional doctrines to reach 40+ entries
    DoctrineBlock(
        topic="Black Start Capability and Restoration Planning",
        keywords=["black start", "restoration", "system recovery", "generator", "islanding"],
        conclusion_template="Black start capability is essential for system restoration after a total or partial blackout.",
        reasoning_framework=(
            "Black start units are capable of starting without external power and energizing portions of the grid. "
            "Restoration plans coordinate black start resources, transmission paths, and load pickup sequences. "
            "Periodic drills and coordination with system operators are required to ensure readiness."
        ),
        key_factors=[
            "Black start resource availability",
            "Restoration sequence",
            "Communication protocols",
            "Operator training",
            "Contingency planning"
        ],
        primary_authority=[
            "NERC EOP-005",
            "IEEE Std 1547"
        ],
        burden_holder="System operator",
        adversary_position="Black start planning is unnecessary due to grid redundancy.",
        counter_arguments=[
            "Major blackouts require coordinated restoration.",
            "Regulatory standards mandate black start capability."
        ],
        resolution_strategy="Develop and test restoration plans regularly.",
        entity_scope="Bulk power system",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NERC EOP-005"
    ),
    DoctrineBlock(
        topic="Synchrophasor Technology and Wide Area Monitoring",
        keywords=["synchrophasor", "PMU", "phasor measurement unit", "WAMS", "real-time monitoring"],
        conclusion_template="Synchrophasor technology enables real-time wide-area monitoring and enhances situational awareness.",
        reasoning_framework=(
            "Phasor Measurement Units (PMUs) provide time-synchronized voltage and current measurements for dynamic system monitoring. "
            "Wide Area Monitoring Systems (WAMS) use PMU data for oscillation detection, stability assessment, and event analysis. "
            "Deployment improves grid reliability and supports advanced control schemes."
        ),
        key_factors=[
            "PMU placement",
            "Data latency",
            "Communication infrastructure",
            "Data analytics",
            "Integration with EMS"
        ],
        primary_authority=[
            "IEEE Std C37.118",
            "NERC PRC-002"
        ],
        burden_holder="System operator",
        adversary_position="Traditional SCADA is sufficient for monitoring.",
        counter_arguments=[
            "SCADA lacks dynamic and time-synchronized data.",
            "PMUs enable early detection of instability."
        ],
        resolution_strategy="Integrate PMUs and WAMS into control center operations.",
        entity_scope="Transmission networks",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEEE Std C37.118"
    ),
    DoctrineBlock(
        topic="Dynamic Line Rating (DLR) for Transmission Optimization",
        keywords=["dynamic line rating", "DLR", "transmission optimization", "ampacity", "weather monitoring"],
        conclusion_template="DLR enables real-time optimization of transmission capacity based on environmental conditions.",
        reasoning_framework=(
            "Dynamic Line Rating systems use real-time weather and line condition data to determine actual conductor ampacity. "
            "This allows operators to safely increase line loading above static ratings during favorable conditions, improving asset utilization. "
            "Implementation requires sensors, data analytics, and integration with EMS."
        ),
        key_factors=[
            "Weather monitoring",
            "Conductor temperature",
            "Line sag",
            "System integration",
            "Operational procedures"
        ],
        primary_authority=[
            "CIGRÉ TB 498",
            "IEEE Std 738"
        ],
        burden_holder="Transmission operator",
        adversary_position="Static ratings are sufficient for reliable operation.",
        counter_arguments=[
            "Static ratings are conservative and limit capacity.",
            "DLR improves flexibility and asset utilization."
        ],
        resolution_strategy="Pilot DLR projects and assess operational benefits.",
        entity_scope="Transmission lines",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IEEE Std 738"
    ),
    DoctrineBlock(
        topic="Substation Automation and IEC 61850",
        keywords=["substation automation", "IEC 61850", "GOOSE", "MMS", "interoperability"],
        conclusion_template="IEC 61850 enables interoperable, automated substation systems with advanced communication capabilities.",
        reasoning_framework=(
            "IEC 61850 defines communication protocols for substation automation, supporting interoperability among devices from different vendors. "
            "Features include GOOSE messaging for fast protection, MMS for data exchange, and standardized data models. "
            "Automation improves reliability, reduces operating costs, and enables remote management."
        ),
        key_factors=[
            "Protocol compliance",
            "Device interoperability",
            "System integration",
            "Cybersecurity",
            "Operator training"
        ],
        primary_authority=[
            "IEC 61850",
            "IEEE Std 1613"
        ],
        burden_holder="Substation designer",
        adversary_position="Proprietary protocols are sufficient.",
        counter_arguments=[
            "IEC 61850 future-proofs investments and simplifies integration.",
            "Standardization reduces engineering and maintenance costs."
        ],
        resolution_strategy="Specify IEC 61850 in new substation projects.",
        entity_scope="Substations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61850"
    ),
    DoctrineBlock(
        topic="Asset Management and Condition-Based Maintenance",
        keywords=["asset management", "CBM", "condition-based maintenance", "predictive analytics", "lifecycle"],
        conclusion_template="Condition-based maintenance improves asset reliability and optimizes lifecycle costs.",
        reasoning_framework=(
            "CBM uses real-time monitoring and predictive analytics to schedule maintenance based on asset condition rather than fixed intervals. "
            "This approach reduces unplanned outages, extends asset life, and optimizes maintenance budgets. Implementation requires sensors, data analytics, and integration with asset management systems."
        ),
        key_factors=[
            "Asset criticality",
            "Condition monitoring",
            "Predictive analytics",
            "Maintenance scheduling",
            "Integration with EAM systems"
        ],
        primary_authority=[
            "ISO 55000",
            "IEC 61943"
        ],
        burden_holder="Asset manager",
        adversary_position="Time-based maintenance is sufficient.",
        counter_arguments=[
            "CBM reduces failures and maintenance costs.",
            "Data-driven decisions improve reliability."
        ],
        resolution_strategy="Deploy pilot CBM projects and measure performance.",
        entity_scope="Transmission and distribution assets",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 55000"
    ),
    DoctrineBlock(
        topic="Transmission Line Protection - Pilot Schemes",
        keywords=["transmission protection", "pilot scheme", "current differential", "teleprotection", "line protection"],
        conclusion_template="Pilot protection schemes provide fast and selective protection for critical transmission lines.",
        reasoning_framework=(
            "Pilot schemes use communication channels to compare current or voltage at both ends of a line. "
            "Current differential and permissive overreaching transfer trip (POTT) schemes offer high-speed, selective protection. "
            "Reliable communication and coordination with backup protection are essential."
        ),
        key_factors=[
            "Communication reliability",
            "Scheme selection",
            "Coordination with backup protection",
            "Channel latency",
            "Testing and maintenance"
        ],
        primary_authority=[
            "IEEE Std C37.113",
            "IEC 60255"
        ],
        burden_holder="Protection engineer",
        adversary_position="Conventional distance relays are sufficient.",
        counter_arguments=[
            "Pilot schemes improve speed and selectivity for critical lines.",
            "Communication failures are mitigated by backup protection."
        ],
        resolution_strategy="Implement pilot schemes on critical and long lines.",
        entity_scope="Transmission lines",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEEE Std C37.113"
    ),
    DoctrineBlock(
        topic="Grounding Practices for Power Systems",
        keywords=["grounding", "earthing", "system grounding", "safety", "fault current"],
        conclusion_template="Proper grounding ensures safety, equipment protection, and reliable system operation.",
        reasoning_framework=(
            "System grounding (solid, resistance, reactance, or ungrounded) affects fault currents, protection, and voltage stability. "
            "Equipment grounding provides a path for fault currents and protects personnel. Grounding practices must comply with IEEE 142 and local codes."
        ),
        key_factors=[
            "Grounding method",
            "Fault current magnitude",
            "Touch and step voltage",
            "Protection coordination",
            "Regulatory compliance"
        ],
        primary_authority=[
            "IEEE Std 142 (Green Book)",
            "IEC 60364"
        ],
        burden_holder="System designer",
        adversary_position="Grounding is only necessary for lightning protection.",
        counter_arguments=[
            "Improper grounding can cause equipment damage and safety hazards.",
            "Protection schemes depend on grounding method."
        ],
        resolution_strategy="Follow standards and conduct grounding studies.",
        entity_scope="All power system installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEEE Std 142"
    ),
    DoctrineBlock(
        topic="Insulation Coordination and Surge Protection",
        keywords=["insulation coordination", "surge protection", "BIL", "arrester", "overvoltage"],
        conclusion_template="Insulation coordination and surge protection are critical for equipment reliability and safety.",
        reasoning_framework=(
            "Insulation coordination involves selecting insulation levels to withstand expected overvoltages. "
            "Surge arresters protect against lightning and switching surges. Basic Insulation Level (BIL) is specified based on system voltage and exposure. "
            "Coordination ensures protection without unnecessary cost."
        ),
        key_factors=[
            "System voltage",
            "Exposure to surges",
            "BIL selection",
            "Arrester rating",
            "Installation practices"
        ],
        primary_authority=[
            "IEC 60071",
            "IEEE Std C62.22"
        ],
        burden_holder="Design engineer",
        adversary_position="Standard insulation is sufficient for all locations.",
        counter_arguments=[
            "High exposure areas require enhanced protection.",
            "Improper coordination can lead to equipment failure."
        ],
        resolution_strategy="Perform insulation coordination studies and specify appropriate surge protection.",
        entity_scope="Transmission and distribution substations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 60071"
    ),
    DoctrineBlock(
        topic="Harmonic Filtering and Mitigation",
        keywords=["harmonic filter", "mitigation", "THD", "passive filter", "active filter"],
        conclusion_template="Harmonic filtering is necessary to maintain power quality and comply with standards.",
        reasoning_framework=(
            "Harmonic filters (passive, active, hybrid) are deployed to reduce Total Harmonic Distortion (THD) caused by nonlinear loads. "
            "Filter selection depends on harmonic spectrum, load profile, and system impedance. Compliance with IEEE 519 is required."
        ),
        key_factors=[
            "Harmonic spectrum",
            "Filter type",
            "System impedance",
            "Load profile",
            "Standard limits"
        ],
        primary_authority=[
            "IEEE Std 519",
            "IEC 61000-4-7"
        ],
        burden_holder="Facility operator",
        adversary_position="Harmonics are not a significant issue.",
        counter_arguments=[
            "Sensitive loads and utility requirements mandate harmonic mitigation.",
            "Non-compliance can result in penalties."
        ],
        resolution_strategy="Conduct harmonic studies and install appropriate filters.",
        entity_scope="Industrial and commercial facilities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEEE Std 519"
    ),
    DoctrineBlock(
        topic="Transmission Right-of-Way and Environmental Considerations",
        keywords=["right-of-way", "ROW", "environmental impact", "permitting", "EMF"],
        conclusion_template="Transmission line siting must balance technical, environmental, and social considerations.",
        reasoning_framework=(
            "Securing right-of-way for transmission lines involves environmental studies, public consultation, and regulatory permitting. "
            "Considerations include land use, EMF exposure, visual impact, and habitat disruption. Early stakeholder engagement and "
            "mitigation measures are essential for project success."
        ),
        key_factors=[
            "Land use",
            "Environmental studies",
            "Stakeholder engagement",
            "Permitting process",
            "Mitigation measures"
        ],
        primary_authority=[
            "FERC NEPA Guidelines",
            "DOE Transmission Siting Guide"
        ],
        burden_holder="Project developer",
        adversary_position="Technical need overrides environmental concerns.",
        counter_arguments=[
            "Regulatory approval requires environmental compliance.",
            "Stakeholder opposition can delay or halt projects."
        ],
        resolution_strategy="Integrate environmental and social considerations into project planning.",
        entity_scope="Transmission projects",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC NEPA Guidelines"
    ),
    DoctrineBlock(
        topic="Distribution Automation and Fault Location, Isolation, and Service Restoration (FLISR)",
        keywords=["distribution automation", "FLISR", "fault location", "isolation", "restoration", "self-healing"],
        conclusion_template="FLISR systems improve reliability by automating fault detection, isolation, and service restoration.",
        reasoning_framework=(
            "FLISR uses sensors, communication, and automation to quickly detect faults, isolate affected sections, and restore service to unaffected areas. "
            "Self-healing grids reduce outage duration and improve reliability indices (SAIDI, SAIFI). Integration with DMS and robust communication are required."
        ),
        key_factors=[
            "Sensor deployment",
            "Communication reliability",
            "Automation scheme",
            "Integration with DMS",
            "Reliability metrics"
        ],
        primary_authority=[
            "IEEE Std 1646",
            "IEC 60870-5-104"
        ],
        burden_holder="Distribution operator",
        adversary_position="Manual switching is adequate for restoration.",
        counter_arguments=[
            "Automation reduces outage duration and improves customer satisfaction.",
            "Regulatory incentives favor reliability improvements."
        ],
        resolution_strategy="Deploy FLISR on feeders with high outage rates.",
        entity_scope="Distribution networks",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEEE Std 1646"
    ),
    DoctrineBlock(
        topic="Transmission System Stability - Small Signal and Transient",
        keywords=["system stability", "small signal", "transient stability", "dynamic analysis", "oscillation"],
        conclusion_template="Stability analysis is essential to prevent system collapse and ensure reliable operation.",
        reasoning_framework=(
            "Small signal stability addresses the system's ability to withstand small disturbances, while transient stability concerns large disturbances such as faults. "
            "Dynamic simulations identify critical clearing times and oscillatory modes. Remedial action schemes and system upgrades may be required."
        ),
        key_factors=[
            "System inertia",
            "Disturbance magnitude",
            "Critical clearing time",
            "Remedial action schemes",
            "Dynamic modeling"
        ],
        primary_authority=[
            "IEEE Std 399",
            "NERC PRC-012"
        ],
        burden_holder="System planner",
        adversary_position="Stability is not a concern in modern grids.",
        counter_arguments=[
            "High renewable penetration reduces system inertia.",
            "Stability issues can lead to widespread blackouts."
        ],
        resolution_strategy="Conduct regular stability studies and implement mitigation measures.",
        entity_scope="Bulk power system",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NERC PRC-012"
    ),
    DoctrineBlock(
        topic="Protective Device Coordination and Selectivity",
        keywords=["protection coordination", "selectivity", "relay setting", "time-current curve", "cascading"],
        conclusion_template="Protective device coordination ensures only the faulted section is isolated, preserving system integrity.",
        reasoning_framework=(
            "Coordination studies determine relay and fuse settings to achieve selectivity. Time-current curves are analyzed to ensure upstream devices operate after downstream devices. "
            "Improper coordination can cause unnecessary outages or equipment damage."
        ),
        key_factors=[
            "Device characteristics",
            "System topology",
            "Time-current settings",
            "Coordination margin",
            "Protection zones"
        ],
        primary_authority=[
            "IEEE Std 242",
            "IEC 60255"
        ],
        burden_holder="Protection engineer",
        adversary_position="Default settings are adequate.",
        counter_arguments=[
            "System changes require updated coordination studies.",
            "Selectivity is critical for reliability."
        ],
        resolution_strategy="Update coordination studies after system modifications.",
        entity_scope="All power system protection",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEEE Std 242"
    ),
    DoctrineBlock(
        topic="Transformer Inrush and Protection",
        keywords=["transformer inrush", "magnetizing inrush", "protection", "harmonic restraint", "relay"],
        conclusion_template="Transformer protection schemes must distinguish inrush from internal faults.",
        reasoning_framework=(
            "Energizing transformers causes inrush currents that may be mistaken for faults. Differential relays with harmonic restraint "
            "can differentiate inrush (rich in second harmonic) from internal faults. Proper relay settings prevent nuisance tripping."
        ),
        key_factors=[
            "Inrush current magnitude",
            "Harmonic content",
            "Relay settings",
            "Transformer size",
            "System configuration"
        ],
        primary_authority=[
            "IEEE Std C37.91",
            "IEC 60255-149"
        ],
        burden_holder="Protection engineer",
        adversary_position="All differential current should trip the relay.",
        counter_arguments=[
            "Inrush is a normal phenomenon during energization.",
            "Harmonic restraint prevents unnecessary outages."
        ],
        resolution_strategy="Apply harmonic restraint and test relay response.",
        entity_scope="Transformer protection",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEEE Std C37.91"
    ),
    DoctrineBlock(
        topic="Substation Grounding Grid Design",
        keywords=["substation grounding", "grid design", "touch voltage", "step voltage", "safety"],
        conclusion_template="Substation grounding grids must be designed to limit touch and step voltages to safe levels.",
        reasoning_framework=(
            "Grounding grid design involves calculating grid resistance, mesh and step voltages, and conductor sizing. "
            "IEEE Std 80 and IEC 60479 provide methodologies for safe design. Soil resistivity measurements are essential for accurate modeling."
        ),
        key_factors=[
            "Soil resistivity",
            "Grid geometry",
            "Fault current magnitude",
            "Conductor size",
            "Safety standards"
        ],
        primary_authority=[
            "IEEE Std 80",
            "IEC 60479"
        ],
        burden_holder="Design engineer",
        adversary_position="Any ground grid is sufficient.",
        counter_arguments=[
            "Improper design can result in hazardous voltages.",
            "Standards specify safe limits for personnel protection."
        ],
        resolution_strategy="Perform detailed grounding studies and verify compliance.",
        entity_scope="Substations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="IEEE Std 80"
    ),
    DoctrineBlock(
        topic="Distribution Feeder Reconfiguration for Loss Reduction",
        keywords=["feeder reconfiguration", "loss reduction", "distribution", "switching", "optimization"],
        conclusion_template="Feeder reconfiguration reduces losses and improves voltage profiles in distribution networks.",
        reasoning_framework=(
            "Automated or manual switching of feeder ties can balance load, reduce losses, and improve voltage. "
            "Optimization algorithms (e.g., genetic algorithms, network flow) are used to identify optimal switching actions. "
            "Coordination with protection and voltage regulation is required."
        ),
        key_factors=[
            "Network topology",
            "Load distribution",
            "Switching constraints",
            "Protection coordination",
            "Voltage regulation"
        ],
        primary_authority=[
            "IEEE Std 1366",
            "IEC 61970"
        ],
        burden_holder="Distribution planner",
        adversary_position="Static feeder configuration is sufficient.",
        counter_arguments=[
            "Dynamic reconfiguration improves efficiency and reliability.",
            "Automation enables real-time optimization."
        ],
        resolution_strategy="Implement reconfiguration schemes and monitor performance.",
        entity_scope="Distribution networks",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE Std 1366"
    ),
    DoctrineBlock(
        topic="Voltage Flicker and Mitigation Techniques",
        keywords=["voltage flicker", "mitigation", "arc furnace", "flicker meter", "IEC 61000-4-15"],
        conclusion_template="Voltage flicker must be monitored and mitigated to prevent equipment malfunction and customer complaints.",
        reasoning_framework=(
            "Flicker is caused by rapid voltage fluctuations from fluctuating loads (e.g., arc furnaces). "
            "Flicker severity is measured using standardized meters (IEC 61000-4-15). Mitigation includes installation of SVC/STATCOM, "
            "load scheduling, and network reinforcement."
        ),
        key_factors=[
            "Flicker source",
            "Severity measurement",
            "Mitigation equipment",
            "Customer sensitivity",
            "Standard compliance"
        ],
        primary_authority=[
            "IEC 61000-4-15",
            "IEEE Std 519"
        ],
        burden_holder="Utility or facility operator",
        adversary_position="Flicker is a minor nuisance.",
        counter_arguments=[
            "Flicker can cause equipment malfunction and customer dissatisfaction.",
            "Regulatory limits must be met."
        ],
        resolution_strategy="Monitor flicker and implement mitigation as needed.",
        entity_scope="Industrial and distribution networks",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 61000-4-15"
    ),
    DoctrineBlock(
        topic="Underground Cable System Design and Installation",
        keywords=["underground cable", "installation", "thermal rating", "sheath bonding", "jointing"],
        conclusion_template="Proper design and installation of underground cables ensure reliability and safety.",
        reasoning_framework=(
            "Underground cable systems require careful design for thermal rating, ampacity, and sheath bonding. "
            "Installation practices affect cable life and reliability. Standards specify minimum bending radius, jointing techniques, and testing requirements."
        ),
        key_factors=[
            "Cable type and rating",
            "Installation method",
            "Thermal environment",
            "Sheath bonding",
            "Testing and commissioning"
        ],
        primary_authority=[
            "IEC 60287",
            "IEEE Std 400"
        ],
        burden_holder="Design engineer",
        adversary_position="Overhead line practices are sufficient for cables.",
        counter_arguments=[
            "Cables have unique design and installation requirements.",
            "Improper installation can lead to premature failure."
        ],
        resolution_strategy="Follow standards and manufacturer recommendations.",
        entity_scope="Transmission and distribution cables",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEC 60287"
    ),
    DoctrineBlock(
        topic="DER Aggregation and Virtual Power Plants",
        keywords=["DER aggregation", "virtual power plant", "VPP", "distributed energy", "market participation"],
        conclusion_template="DER aggregation enables small resources to participate in markets and provide grid services.",
        reasoning_framework=(
            "Aggregators combine multiple DERs (solar, storage, demand response) to form a Virtual Power Plant (VPP). "
            "VPPs can bid into energy and ancillary service markets, providing flexibility and balancing services. "
            "Communication, control, and regulatory compliance are essential for effective aggregation."
        ),
        key_factors=[
            "DER type and location",
            "Communication infrastructure",
            "Market rules",
            "Control systems",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FERC Order 2222",
            "IEEE Std 2030.5"
        ],
        burden_holder="Aggregator",
        adversary_position="Small DERs have negligible grid impact.",
        counter_arguments=[
            "Aggregation enables meaningful participation and grid support.",
            "Regulations increasingly support DER aggregation."
        ],
        resolution_strategy="Develop aggregation platforms and ensure compliance.",
        entity_scope="Retail and wholesale markets",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC Order 2222"
    ),
    DoctrineBlock(
        topic="Frequency Control and Automatic Generation Control (AGC)",
        keywords=["frequency control", "AGC", "governor response", "balancing", "NERC BAL"],
        conclusion_template="Frequency control and AGC maintain system balance and prevent frequency excursions.",
        reasoning_framework=(
            "System frequency is maintained by balancing generation and load. Primary control is provided by generator governors, "
            "while AGC adjusts setpoints to correct Area Control Error (ACE). Compliance with NERC BAL standards is mandatory for balancing authorities."
        ),
        key_factors=[
            "Governor response",
            "AGC performance",
            "ACE calculation",
            "Balancing authority",
            "Compliance monitoring"
        ],
        primary_authority=[
            "NERC BAL Standards",
            "IEEE Std 1048"
        ],
        burden_holder="Balancing authority",
        adversary_position="Manual control is sufficient for frequency regulation.",
        counter_arguments=[
            "Automatic control improves response time and compliance.",
            "Frequency excursions can damage equipment and cause outages."
        ],
        resolution_strategy="Implement and monitor AGC performance.",
        entity_scope="Bulk power system",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NERC BAL Standards"
    ),
    DoctrineBlock(
        topic="Islanding Detection and Anti-Islanding Protection",
        keywords=["islanding", "anti-islanding", "detection", "inverter", "IEEE 1547"],
        conclusion_template="Anti-islanding protection is required to ensure safety and reliability with DER integration.",
        reasoning_framework=(
            "Islanding occurs when a DER continues to energize a portion of the grid after loss of utility supply. "
            "Anti-islanding schemes (active and passive) are required by IEEE 1547 to detect and disconnect DERs. "
            "Failure to detect islanding can endanger personnel and equipment."
        ),
        key_factors=[
            "DER type and size",
            "Detection method",
            "Trip settings",
            "Coordination with utility protection",
            "Standard compliance"
        ],
        primary_authority=[
            "IEEE Std 1547",
            "UL 1741"
        ],
        burden_holder="DER owner/operator",
        adversary_position="Islanding is unlikely and not a concern.",
        counter_arguments=[
            "Undetected islanding poses safety risks.",
            "Standards mandate anti-islanding protection."
        ],
        resolution_strategy="Test and document anti-islanding schemes for all DER installations.",
        entity_scope="Distribution networks",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="IEEE Std 1547"
    ),
    DoctrineBlock(
        topic="High-Impact, Low-Frequency (HILF) Event Preparedness",
        keywords=["HILF", "event preparedness", "geomagnetic disturbance", "GMD", "EMP", "pandemic"],
        conclusion_template="Preparedness for HILF events is critical for grid resilience and national security.",
        reasoning_framework=(
            "HILF events (GMD, EMP, extreme weather, pandemic) can cause widespread grid disruption. "
            "Preparedness includes risk assessment, mitigation strategies, and coordination with government agencies. "
            "NERC CIP and EOP standards provide guidance for critical infrastructure protection."
        ),
        key_factors=[
            "Risk assessment",
            "Mitigation planning",
            "Coordination with authorities",
            "Critical infrastructure identification",
            "Training and exercises"
        ],
        primary_authority=[
            "NERC CIP Standards",
            "DOE HILF Guidance"
        ],
        burden_holder="System operator",
        adversary_position="HILF events are too rare to warrant investment.",
        counter_arguments=[
            "Consequences of unpreparedness are severe.",
            "Regulatory requirements mandate preparedness."
        ],
        resolution_strategy="Develop and test HILF response plans.",
        entity_scope="Bulk power system",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NERC CIP Standards"
    ),
    DoctrineBlock(
        topic="IEC 61850 GOOSE Messaging for Protection and Control",
        keywords=["IEC 61850", "GOOSE", "messaging", "protection", "control"],
        conclusion_template="GOOSE messaging enables high-speed, peer-to-peer communication for protection and control.",
        reasoning_framework=(
            "GOOSE (Generic Object Oriented Substation Event) messaging is a feature of IEC 61850 enabling fast, reliable communication "
            "between IEDs for protection and control. It replaces hardwired signals, reduces wiring complexity, and supports advanced automation."
        ),
        key_factors=[
            "Network reliability",
            "IED configuration",
            "Cybersecurity",
            "Testing and commissioning",
            "Interoperability"
        ],
        primary_authority=[
            "IEC 61850-8-1",
            "IEEE Std 1613"
        ],
        burden_holder="Protection engineer",
        adversary_position="Hardwired signals are more reliable.",
        counter_arguments=[
            "GOOSE offers faster response and greater flexibility.",
            "Redundant network design ensures reliability."
        ],
        resolution_strategy="Deploy GOOSE messaging with robust network design.",
        entity_scope="Substations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 61850-8-1"
    ),
    DoctrineBlock(
        topic="IEC 62351 Cybersecurity for Power System Communications",
        keywords=["IEC 62351", "cybersecurity", "power system communication", "encryption", "authentication"],
        conclusion_template="IEC 62351 provides cybersecurity measures for power system communication protocols.",
        reasoning_framework=(
            "IEC 62351 specifies security for protocols such as IEC 61850, DNP3, and IEC 60870-5. "
            "Measures include encryption, authentication, and intrusion detection. Compliance is essential to protect critical infrastructure."
        ),
        key_factors=[
            "Protocol in use",
            "Encryption implementation",
            "Authentication methods",
            "Intrusion detection",
            "Compliance monitoring"
        ],
        primary_authority=[
            "IEC 62351",
            "NERC CIP Standards"
        ],
        burden_holder="System operator",
        adversary_position="Legacy protocols are sufficient.",
        counter_arguments=[
            "Cyber threats are increasing.",
            "Regulations require cybersecurity measures."
        ],
        resolution_strategy="Implement IEC 62351 for all new and upgraded systems.",
        entity_scope="All power system communications",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 62351"
    ),
    DoctrineBlock(
        topic="DER Hosting Capacity Analysis",
        keywords=["DER hosting capacity", "analysis", "distribution", "voltage rise", "thermal limits"],
        conclusion_template="Hosting capacity analysis determines the maximum DER penetration without adverse grid impacts.",
        reasoning_framework=(
            "Hosting capacity studies assess the ability of distribution feeders to accommodate DERs without violating voltage, thermal, or protection limits. "
            "Analysis includes voltage rise, reverse power flow, and coordination with voltage regulation devices. Results inform interconnection policies."
        ),
        key_factors=[
            "Feeder voltage profile",
            "Thermal loading",
            "Protection coordination",
            "Voltage regulation",
            "DER penetration level"
        ],
        primary_authority=[
            "IEEE Std 1547.7",
            "EPRI Hosting Capacity Guide"
        ],
        burden_holder="Utility planner",
        adversary_position="DERs can be added without analysis.",
        counter_arguments=[
            "Unstudied DER additions can cause voltage and protection issues.",
            "Analysis supports safe and reliable integration."
        ],
        resolution_strategy="Conduct hosting capacity studies for all DER applications.",
        entity_scope="Distribution networks",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IEEE Std 1547.7"
    ),
    DoctrineBlock(
        topic="Transformer Paralleling and Load Sharing",
        keywords=["transformer paralleling", "load sharing", "impedance matching", "circulating current"],
        conclusion_template="Proper paralleling ensures transformers share load proportionally and operate reliably.",
        reasoning_framework=(
            "Parallel operation of transformers requires matching voltage ratio, impedance, and phase displacement. "
            "Mismatches cause circulating currents and unequal load sharing, potentially overloading one unit. "
            "IEEE and IEC standards provide guidelines for paralleling."
        ),
        key_factors=[
            "Voltage ratio",
            "Impedance",
            "Phase displacement",
            "Tap settings",
            "Load monitoring"
        ],
        primary_authority=[
            "IEEE Std C57.12",
            "IEC 60076-1"
        ],
        burden_holder="Substation engineer",
        adversary_position="Any transformers can be paralleled.",
        counter_arguments=[
            "Mismatched units can cause equipment damage.",
            "Proper paralleling improves reliability and flexibility."
        ],
        resolution_strategy="Verify compatibility before paralleling and monitor operation.",
        entity_scope="Substations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEEE Std C57.12"
    ),
    DoctrineBlock(
        topic="Load Shedding Schemes and Underfrequency Protection",
        keywords=["load shedding", "underfrequency", "UFLS", "system protection", "automatic"],
        conclusion_template="Automatic load shedding prevents system collapse during severe disturbances.",
        reasoning_framework=(
            "UFLS schemes disconnect load in stages when system frequency drops below setpoints, preventing total blackout. "
            "Coordination with generation and system studies is required to set trip levels and ensure effectiveness."
        ),
        key_factors=[
            "Frequency setpoints",
            "Load block selection",
            "Coordination with generation",
            "System studies",
            "Testing and maintenance"
        ],
        primary_authority=[
            "NERC PRC-006",
            "IEEE Std 1547"
        ],
        burden_holder="System operator",
        adversary_position="Manual intervention is sufficient.",
        counter_arguments=[
            "Automatic schemes respond faster than manual actions.",
            "UFLS is mandated by reliability standards."
        ],
        resolution_strategy="Design and test UFLS schemes.",
        entity_scope="Bulk power system",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NERC PRC-006"
    ),
    DoctrineBlock(
        topic="Transmission Congestion Management",
        keywords=["congestion management", "transmission", "LMP", "redispatch", "market"],
        conclusion_template="Congestion management ensures reliable and economic operation of the transmission system.",
        reasoning_framework=(
            "Congestion occurs when transmission limits prevent economic dispatch. LMP reflects congestion costs, and redispatch or curtailment is used to relieve congestion. "
            "Market rules and operational procedures govern congestion management."
        ),
        key_factors=[
            "Transmission limits",
            "Market design",
            "Redispatch options",
            "Curtailment procedures",
            "Regulatory oversight"
        ],
        primary_authority=[
            "FERC Order 2000",
            "NERC Standards"
        ],
        burden_holder="ISO/RTO",
        adversary_position="Congestion is rare and not a concern.",
        counter_arguments=[
            "Congestion can lead to high prices and reliability risks.",
            "Effective management supports market efficiency."
        ],
        resolution_strategy="Implement congestion management tools and procedures.",
        entity_scope="ISO/RTO markets",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Order 2000"
    ),
    DoctrineBlock(
        topic="Distribution Transformer Sizing and Loss Evaluation",
        keywords=["distribution transformer", "sizing", "loss evaluation", "load profile", "efficiency"],
        conclusion_template="Proper transformer sizing balances efficiency, cost, and reliability.",
        reasoning_framework=(
            "Transformer size is selected based on load profile, future growth, and loss evaluation. "
            "Oversized units waste energy at low load; undersized units risk overload. Total cost of ownership includes capital and loss costs."
        ),
        key_factors=[
            "Load profile",
            "Future growth",
            "Loss evaluation",
            "Efficiency",
            "Cost analysis"
        ],
        primary_authority=[
            "DOE Transformer Efficiency Standards",
            "IEC 60076-8"
        ],
        burden_holder="Distribution planner",
        adversary_position="Bigger transformers are always better.",
        counter_arguments=[
            "Oversizing increases losses and costs.",
            "Proper sizing optimizes efficiency and reliability."
        ],
        resolution_strategy="Perform load and loss analysis for transformer selection.",
        entity_scope="Distribution networks",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="DOE Transformer Efficiency Standards"
    ),
    DoctrineBlock(
        topic="Protective Relay Testing and Commissioning",
        keywords=["relay testing", "commissioning", "protection", "secondary injection", "end-to-end"],
        conclusion_template="Comprehensive relay testing ensures protection systems operate as designed.",
        reasoning_framework=(
            "Testing includes secondary injection, functional checks, and end-to-end tests for communication-assisted schemes. "
            "Commissioning verifies correct wiring, settings, and coordination. Documentation is essential for compliance and maintenance."
        ),
        key_factors=[
            "Test procedures",
            "Documentation",
            "Coordination with system studies",
            "Communication channel testing",
            "Regulatory compliance"
        ],
        primary_authority=[
            "IEEE Std C37.103",
            "IEC 61850-10"
        ],
        burden_holder="Protection engineer",
        adversary_position="Factory testing is sufficient.",
        counter_arguments=[
            "Field conditions may differ from factory tests.",
            "Commissioning ensures system integration."
        ],
        resolution_strategy="Follow comprehensive test plans and document results.",
        entity_scope="All protection systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="IEEE Std C37.103"
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